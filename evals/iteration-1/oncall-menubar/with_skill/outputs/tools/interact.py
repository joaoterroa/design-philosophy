"""Keyboard path through the main task: open handover, pick a range, pick a person, send, cancel.
Also measures layout shift above the reading point when a request is sent.
Run from outputs/: /home/user/vfuk-technical-memory/.venv/bin/python tools/interact.py
"""
import pathlib
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
URL = (ROOT / "app" / "index.html").as_uri()
results = []
def check(name, ok, detail=""):
    results.append((name, ok, detail)); print(("PASS " if ok else "FAIL ") + name + (f"  ({detail})" if detail else ""))

with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium", args=["--headless=new"])
    pg = b.new_page(viewport={"width": 1040, "height": 800})
    errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(URL + "?state=oncall")
    pg.wait_for_timeout(400)  # let the 220ms appear animation finish
    top_before = pg.evaluate("document.querySelector('.answer').getBoundingClientRect().top")
    strip_before = pg.evaluate("document.querySelector('.strip').getBoundingClientRect().top")

    pg.focus('[data-act="handover"]'); pg.keyboard.press("Enter")
    check("Hand over opens compose and focuses the first choice", pg.evaluate("document.activeElement.name") == "mode")
    pg.keyboard.press("ArrowDown")  # radio group wraps to "The rest of my shift"
    check("Arrow keys switch the range choice and hide the time fields", pg.is_hidden(".times"))
    pg.keyboard.press("ArrowUp")
    check("…and back to 'Part of it', focus kept", pg.evaluate("document.activeElement.value") == "part" and pg.is_visible(".times"))
    pg.select_option("select[name=start]", "34"); pg.select_option("select[name=end]", "42")
    check("Send disabled until someone is chosen", pg.is_disabled('[data-act="send"]'))
    pg.fill("input[name=q]", "zz")
    check("Search with no match says so", "matches" in pg.inner_text("#people"))
    pg.fill("input[name=q]", "pri")
    pg.focus("input[name=to][value=pr]"); pg.keyboard.press("Space")
    check("Choosing by keyboard keeps focus on the chosen person", pg.evaluate("document.activeElement.value") == "pr")
    check("Send label names the person", pg.inner_text('[data-act="send"]') == "Ask Priya")
    check("Preview segment appears with the recipient", pg.locator(".seg-preview").count() == 1 and "PR" in pg.inner_text(".seg-preview"))
    pg.fill("input[name=q]", "")
    check("Sam (already secondary) cannot be chosen", pg.is_disabled("input[name=to][value=so]"))
    pg.fill("textarea[name=note]", "Checkout alert still flappy.")
    pg.keyboard.press("Meta+Enter"); pg.wait_for_timeout(400)
    check("Cmd+Return sends; main view shows waiting state", pg.locator(".note-pending").count() == 1)
    check("Menu-bar title still shows you on call", "1d 19h" in pg.inner_text("#status-item"))
    top_after = pg.evaluate("document.querySelector('.answer').getBoundingClientRect().top")
    strip_after = pg.evaluate("document.querySelector('.strip').getBoundingClientRect().top")
    check("Nothing above the reading point moved", top_before == top_after and strip_before == strip_after, f"answer {top_before}->{top_after}, strip {strip_before}->{strip_after}")
    pg.click('[data-act="cancel-req"]')
    check("Cancel request returns focus to Hand over", pg.evaluate("document.activeElement.dataset.act") == "handover")
    pg.keyboard.press("Enter"); pg.keyboard.press("Escape")
    check("Escape backs out of compose to main", pg.locator(".you").count() == 1)
    pg.keyboard.press("Escape")
    check("Escape closes the popover and focuses the status item", pg.is_hidden("#popover") and pg.evaluate("document.activeElement.id") == "status-item")
    pg.keyboard.press("Enter")
    check("Status item reopens it", pg.is_visible("#popover"))
    pg.goto(URL + "?state=incoming"); pg.click('[data-act="inc-accept"]')
    check("Accepting incoming request confirms in words and clears the badge", "You’re covering Data Primary" in pg.inner_text("#popover") and "request waiting" not in pg.get_attribute("#status-item", "aria-label"))
    pg.goto(URL + "?state=connect"); pg.click('[data-act="connect"]')
    check("Sign-in shows the first-sync state", pg.locator(".loading").count() == 1)
    pg.wait_for_timeout(1400)
    check("…then the schedule", pg.locator(".you").count() == 1)
    check("No page errors", not errs, "; ".join(errs))
    b.close()
print(f"\n{sum(r[1] for r in results)}/{len(results)} passed")
