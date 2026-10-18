"""Render every onboarding state, take screenshots and run layout/accessibility checks.
Usage: python tools/verify.py   (from the outputs folder)"""
import json, sys, pathlib
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
URL = (ROOT / "app" / "index.html").as_uri()
SHOTS = ROOT / "screenshots"; SHOTS.mkdir(exist_ok=True)

STATES = ["welcome", "details", "details-errors", "details-notfound", "details-nocard",
          "code", "code-wrong", "code-expired", "code-help", "code-locked",
          "passcode", "passcode-errors", "biometrics", "working", "working-slow", "working-failed", "done"]
VARIANTS = [  # (label, width, height, query, states)
    ("390-light", 390, 844, "", STATES),
    ("390-dark", 390, 844, "theme=dark", STATES),
    ("320-light", 320, 568, "", STATES),
    ("430-light", 430, 932, "", ["welcome", "code", "done"]),
    ("390-text200", 390, 844, "scale=200", ["details", "details-errors", "code", "passcode", "biometrics", "done"]),
    ("390-help", 390, 844, "help=1", ["details", "code"]),
    ("390-help-dark", 390, 844, "help=1&theme=dark", ["code"]),
]

CHECK_JS = """() => {
  const out = {overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth, small: [], clipped: []};
  const vis = (el) => { const r = el.getBoundingClientRect(); const cs = getComputedStyle(el); return r.width > 0 && r.height > 0 && cs.visibility !== 'hidden'; };
  for (const el of document.querySelectorAll('button, a, input, [role=button]')) {
    if (!vis(el) || el.closest('[inert]') && !document.querySelector('#help:not([hidden])') ) continue;
    const r = el.getBoundingClientRect();
    const inline = el.tagName === 'A' && el.closest('p, li') && !el.classList.contains('btn');
    if (!inline && (r.height < 47.5 || r.width < 47.5)) out.small.push(`${el.tagName}#${el.id||''}.${el.className} ${Math.round(r.width)}x${Math.round(r.height)}`);
    if (r.right > innerWidth + 0.5 || r.left < -0.5) out.clipped.push(`${el.tagName}#${el.id} right=${Math.round(r.right)}`);
  }
  for (const el of document.querySelectorAll('h1, p, li, label, legend')) {
    if (vis(el) && !el.classList.contains('vh') && el.scrollWidth > el.clientWidth + 1) out.clipped.push(`${el.tagName} text overflow: ${el.textContent.slice(0,40)}`);
  }
  const h1 = [...document.querySelectorAll('.screen:not([hidden]) h1')];
  out.h1 = h1.map(h => h.textContent);
  out.firstActionY = (() => { const b = document.querySelector('.screen:not([hidden]) .btn-primary'); return b ? Math.round(b.getBoundingClientRect().top + scrollY) : null; })();
  out.active = document.activeElement && (document.activeElement.id || document.activeElement.tagName);
  out.pageHeight = document.documentElement.scrollHeight;
  return out;
}"""

def main():
    report, problems = {}, []
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium", args=["--headless=new"])
        for label, w, h, q, states in VARIANTS:
            ctx = b.new_context(viewport={"width": w, "height": h}, device_scale_factor=2, has_touch=True, is_mobile=True,
                                color_scheme="dark" if "dark" in q else "light")
            page = ctx.new_page()
            errors = []
            page.on("console", lambda m: m.type == "error" and errors.append(m.text))
            page.on("pageerror", lambda e: errors.append(str(e)))
            for s in states:
                page.goto("about:blank")
                page.goto(f"{URL}?{q}#{s}" if q else f"{URL}#{s}")
                page.evaluate("() => localStorage.clear()")
                page.wait_for_timeout(1700 if s.startswith("code") or s == "working" else 1000 if s.startswith("working") else 350)
                res = page.evaluate(CHECK_JS)
                res["console"] = list(errors); errors.clear()
                report[f"{label}/{s}"] = res
                full = "help" not in label
                page.screenshot(path=str(SHOTS / f"{label}--{s}.png"), full_page=full)
                for k in ("small", "clipped", "console"):
                    if res[k]: problems.append(f"{label}/{s} {k}: {res[k]}")
                if res["overflow"] > 0: problems.append(f"{label}/{s} horizontal overflow {res['overflow']}px")
            ctx.close()
        b.close()
    (ROOT / "tools" / "verify-report.json").write_text(json.dumps(report, indent=1))
    print("\n".join(problems) if problems else "No overflow, clipping, small targets or console errors.")
    for k in ["390-light/welcome", "390-light/details", "390-light/code", "320-light/code", "390-text200/code", "390-light/done"]:
        print(k, "first primary button at y =", report[k]["firstActionY"], "page height", report[k]["pageHeight"])

def tab_to(page, predicate_js, limit=40):
    for _ in range(limit):
        page.keyboard.press("Tab")
        if page.evaluate(predicate_js): return True
    return False

def keyboard_walk():
    """Complete the whole flow with the keyboard only, as a screen-reader or switch user would."""
    log = []
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium", args=["--headless=new"])
        page = b.new_page(viewport={"width": 390, "height": 844}, reduced_motion="reduce")
        errs = []; page.on("pageerror", lambda e: errs.append(str(e)))
        page.goto(URL); page.evaluate("() => localStorage.clear()"); page.reload()
        focused = lambda: page.evaluate("() => document.activeElement.id || document.activeElement.textContent.trim().slice(0,30)")
        h1 = lambda: page.evaluate("() => document.querySelector('.screen:not([hidden]) h1').textContent")
        assert tab_to(page, "() => document.activeElement.textContent.trim() === 'Start setting up'"); page.keyboard.press("Enter")
        log.append(f"details: h1='{h1()}', focus on '{focused()}'")
        # Help: open with keyboard, Escape closes, focus returns to Help
        page.focus("#help-open"); page.keyboard.press("Enter")
        log.append(f"help open: focus '{focused()}', app inert={page.evaluate('() => document.querySelector(\'.app\').hasAttribute(\'inert\')')}")
        page.keyboard.press("Escape"); log.append(f"help closed: focus returned to '{focused()}'")
        # Submit empty -> summary gets focus
        page.focus("#card"); page.keyboard.press("Enter")
        log.append(f"empty submit: focus '{focused()}', summary items={page.locator('#details-summary-list li').count()}")
        page.focus("#card"); page.keyboard.type("4921338801547712")
        log.append(f"card grouped as '{page.input_value('#card')}'")
        page.keyboard.press("Tab"); page.keyboard.type("27"); page.keyboard.press("Tab"); page.keyboard.type("3"); page.keyboard.press("Tab"); page.keyboard.type("1951")
        page.keyboard.press("Enter")
        log.append(f"code: h1='{h1()}', progress='{page.text_content('#progress-text')}'")
        page.wait_for_timeout(1400)
        log.append(f"message status: '{page.text_content('#message-status')}'")
        assert tab_to(page, "() => document.activeElement.id === 'otp'")
        page.keyboard.type("000000"); page.keyboard.press("Enter")
        log.append(f"wrong code: '{page.text_content('#code-error').strip()}' focus '{focused()}'")
        page.keyboard.type("482913"); page.keyboard.press("Enter")
        log.append(f"passcode: h1='{h1()}'")
        assert tab_to(page, "() => document.activeElement.id === 'pass'")
        page.keyboard.type("270351"); page.keyboard.press("Tab"); page.keyboard.type("270351"); page.keyboard.press("Enter")
        log.append(f"birthday passcode: '{page.text_content('#pass-error').strip()}'")
        page.fill("#pass", ""); page.focus("#pass"); page.keyboard.type("481937"); page.fill("#pass2", ""); page.focus("#pass2"); page.keyboard.type("481930"); page.keyboard.press("Enter")
        log.append(f"mismatch: '{page.text_content('#pass2-error').strip()}' focus '{focused()}'")
        page.keyboard.type("481937")
        page.focus("#pass-show"); page.keyboard.press("Enter")
        log.append(f"show toggle: pressed={page.get_attribute('#pass-show','aria-pressed')}, types={page.evaluate('() => [pass.type, pass2.type]')}")
        page.focus("#pass2"); page.keyboard.press("Enter")
        log.append(f"biometrics: h1='{h1()}'")
        assert tab_to(page, "() => document.activeElement.dataset.bio === 'no'"); page.keyboard.press("Enter")
        log.append(f"working: h1='{h1()}', back hidden={page.is_hidden('#back')}")
        page.wait_for_timeout(5200)
        log.append(f"done: h1='{h1()}', focus on '{focused()}'")
        log.append(f"page errors: {errs or 'none'}")
        b.close()
    print("\n".join(log))

if __name__ == "__main__":
    main()
    keyboard_walk()
