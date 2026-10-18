"""Render every state to PNG and run behavioural accessibility checks.
Usage: python checks/render.py  (from the outputs folder)"""
import json, pathlib, sys
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
URL = (ROOT / "app" / "index.html").as_uri()
SHOTS = ROOT / "screenshots"
SHOTS.mkdir(exist_ok=True)

STATES = ["welcome", "prepare", "details", "details-errors", "help", "checking", "checking-slow",
          "checking-veryslow", "checking-failed", "checking-nomatch", "code", "code-wrong", "code-help",
          "timeout", "passcode", "passcode-easy", "passcode-mismatch", "fingerprint", "safety", "done"]

problems, notes = [], []

# Measures: targets under 48px, horizontal overflow, text under 17px.
AUDIT = """() => {
  const out = {small: [], tinyText: [], overflow: document.documentElement.scrollWidth > innerWidth + 1};
  const vis = el => { const r = el.getBoundingClientRect(); return r.width && r.height && getComputedStyle(el).visibility !== 'hidden'; };
  const scope = document.querySelector('dialog[open]') || document.querySelector('.app');
  scope.querySelectorAll('button, a, input:not([type=checkbox]), label.check').forEach(el => {
    if (!vis(el)) return;
    const r = el.getBoundingClientRect();
    if (r.height < 47.5 || (r.width < 47.5)) out.small.push((el.id || el.textContent.trim().slice(0, 30)) + ' ' + Math.round(r.width) + 'x' + Math.round(r.height));
  });
  scope.querySelectorAll('p, span, li, label, a, button, legend, h1, h2, h3').forEach(el => {
    if (!vis(el) || !el.childNodes.length) return;
    const own = [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim());
    if (own && parseFloat(getComputedStyle(el).fontSize) < 16.9) out.tinyText.push(el.textContent.trim().slice(0, 30) + ' ' + getComputedStyle(el).fontSize);
  });
  return out;
}"""

with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium", args=["--headless=new"])

    def page_for(width=390, height=844, scheme="light", motion="reduce"):
        ctx = b.new_context(viewport={"width": width, "height": height}, device_scale_factor=2,
                            color_scheme=scheme, reduced_motion=motion, has_touch=True, is_mobile=True)
        pg = ctx.new_page()
        pg.on("pageerror", lambda e: problems.append(f"JS error: {e}"))
        pg.on("console", lambda m: m.type == "error" and problems.append(f"console: {m.text}"))
        return pg

    pg = page_for()
    for i, s in enumerate(STATES):
        pg.goto("about:blank"); pg.goto(f"{URL}#{s}")   # fresh state per screenshot
        pg.add_style_tag(content=".proto{display:none}")
        pg.wait_for_timeout(350)
        a = pg.evaluate(AUDIT)
        if a["overflow"]: problems.append(f"{s}: horizontal scroll at 390px")
        for x in a["small"]: problems.append(f"{s}: small target {x}")
        for x in a["tinyText"]: problems.append(f"{s}: text under 17px: {x}")
        pg.screenshot(path=str(SHOTS / f"{i+1:02d}-{s}.png"), full_page=s not in ("help", "timeout"))

    # Dark mode, narrow phone and large text (200%) variants of the busiest screens
    dk = page_for(scheme="dark")
    for s in ["welcome", "details-errors", "checking-slow", "code", "done"]:
        dk.goto("about:blank"); dk.goto(f"{URL}#{s}"); dk.add_style_tag(content=".proto{display:none}"); dk.wait_for_timeout(300)
        dk.screenshot(path=str(SHOTS / f"dark-{s}.png"), full_page=True)

    for w in (320,):
        n = page_for(width=w, height=640)
        for s in STATES:
            n.goto("about:blank"); n.goto(f"{URL}#{s}"); n.wait_for_timeout(200)
            if n.evaluate(AUDIT)["overflow"]: problems.append(f"{s}: horizontal scroll at {w}px")
        n.goto("about:blank"); n.goto(f"{URL}#details-errors"); n.add_style_tag(content=".proto{display:none}"); n.wait_for_timeout(200)
        n.screenshot(path=str(SHOTS / f"w320-details-errors.png"), full_page=True)

    big = page_for(width=390)
    for s in STATES:
        big.goto("about:blank"); big.goto(f"{URL}#{s}"); big.wait_for_timeout(200)
        big.add_style_tag(content="html{font-size:200% !important}")
        big.wait_for_timeout(100)
        if big.evaluate(AUDIT)["overflow"]: problems.append(f"{s}: horizontal scroll at 200% text")
    for s in ["details-errors", "code"]:
        big.goto("about:blank"); big.goto(f"{URL}#{s}"); big.add_style_tag(content="html{font-size:200% !important}.proto{display:none}")
        big.wait_for_timeout(150)
        big.screenshot(path=str(SHOTS / f"text200-{s}.png"), full_page=True)

    # Happy path with keyboard and real input, plus the live slow check (sort code 11-11-11)
    k = page_for(motion="no-preference")
    k.goto(f"{URL}#welcome")
    k.get_by_role("button", name="I already bank with Larch").click()
    k.get_by_role("button", name="Start").click()
    k.get_by_role("button", name="Continue").click()
    focused = k.evaluate("document.activeElement.id")
    if focused != "error-summary": problems.append(f"empty submit: focus went to {focused!r}, not the error summary")
    k.keyboard.press("Tab")
    first_link = k.evaluate("document.activeElement.textContent")
    k.keyboard.press("Enter")
    if k.evaluate("document.activeElement.id") != "day": problems.append("error summary link did not move focus to the field")
    notes.append(f"error summary first link: {first_link!r}")
    inv = k.evaluate("[...document.querySelectorAll('[aria-invalid=true]')].map(e=>e.id)")
    notes.append(f"aria-invalid after empty submit: {inv}")
    k.fill("#day", "27"); k.fill("#month", "3"); k.fill("#year", "1951")
    k.fill("#sort", "11-11-11"); k.fill("#acct", "12345678")
    k.keyboard.press("Enter")
    k.wait_for_timeout(1000)
    k.screenshot(path=str(SHOTS / "live-checking-1s.png"))
    k.wait_for_timeout(3500)
    t = k.evaluate("location.hash")
    if t != "#checking-slow": problems.append(f"slow check did not switch to slow state ({t})")
    live = k.evaluate("document.getElementById('announce').textContent")
    notes.append(f"live region during slow check: {live!r}")
    k.wait_for_timeout(8500)
    if k.evaluate("location.hash") != "#checking-veryslow": problems.append("very slow state not reached")
    k.wait_for_timeout(6500)
    if k.evaluate("location.hash") != "#code": problems.append("did not reach code after slow check")
    k.fill("#code", "000000"); k.keyboard.press("Enter")
    msg = k.locator(".field-error").text_content()
    notes.append(f"wrong code message: {msg!r}")
    k.fill("#code", "482 913"); k.keyboard.press("Enter")
    k.fill("#passcode", "270351"); k.keyboard.press("Enter")
    notes.append("DOB passcode message: " + repr(k.locator('.field-error').text_content()))
    k.fill("#passcode", "583920"); k.keyboard.press("Enter")
    k.fill("#confirm", "583921"); k.keyboard.press("Enter")
    if not k.locator(".field-error").count(): problems.append("mismatch not caught")
    k.fill("#confirm", "583920"); k.keyboard.press("Enter")
    k.get_by_role("button", name="Not now, use my passcode").click()
    k.get_by_role("button", name="I understand").click()
    if k.evaluate("location.hash") != "#done": problems.append("happy path did not end on done")
    # Help sheet: opens as a modal, Escape closes it, focus returns to Help
    k.goto("about:blank"); k.goto(f"{URL}#code")
    k.get_by_role("button", name="Help").click()
    if not k.evaluate("document.getElementById('help-sheet').open"): problems.append("help did not open")
    k.keyboard.press("Escape")
    if k.evaluate("document.getElementById('help-sheet').open"): problems.append("Escape did not close help")
    notes.append("focus after closing help: " + k.evaluate("document.activeElement.id"))
    b.close()

print(json.dumps({"problems": problems, "notes": notes}, indent=1))
