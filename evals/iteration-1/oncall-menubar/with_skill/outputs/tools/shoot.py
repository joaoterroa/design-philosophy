"""Render every prototype state in both themes at 2x (Retina) and run layout checks.

Run: /home/user/vfuk-technical-memory/.venv/bin/python tools/shoot.py   (from outputs/)
"""
import json, pathlib, sys
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
URL = (ROOT / "app" / "index.html").as_uri()
OUT = ROOT / "screenshots"
OUT.mkdir(exist_ok=True)
STATES = ["oncall", "offcall", "compose", "sendfail", "pending", "accepted", "declined", "incoming", "gap", "offline", "loading", "connect"]
THEMES = sys.argv[1:] or ["light", "dark"]

CHECK = """() => {
  const pop = document.querySelector('#popover');
  const r = pop.getBoundingClientRect();
  const over = [];
  pop.querySelectorAll('*').forEach(el => {
    const b = el.getBoundingClientRect();
    if (b.width && (b.right > r.right + 0.5 || b.left < r.left - 0.5) && !el.closest('.people') && !el.closest('.compose-body')) over.push(el.className || el.tagName);
    const cs = getComputedStyle(el);
    if (cs.textOverflow === 'ellipsis' && el.scrollWidth > el.clientWidth + 1) over.push('truncated:' + el.textContent.trim().slice(0, 40));
  });
  return { w: Math.round(r.width), h: Math.round(r.height), over, fonts: getComputedStyle(document.body).fontFamily };
}"""

with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium", args=["--headless=new"])
    report = {}
    for theme in THEMES:
        pg = b.new_page(viewport={"width": 1040, "height": 800}, device_scale_factor=2, color_scheme=theme)
        errors = []
        pg.on("pageerror", lambda e: errors.append(str(e)))
        pg.on("console", lambda m: m.type == "error" and errors.append(m.text))
        for s in STATES:
            pg.goto(f"{URL}?state={s}&theme={theme}")
            pg.wait_for_timeout(350)
            info = pg.evaluate(CHECK)
            report[f"{s}-{theme}"] = info
            box = pg.locator("#popover").bounding_box()
            clip = {"x": box["x"] - 340, "y": 0, "width": box["width"] + 380, "height": box["y"] + box["height"] + 24}
            pg.screenshot(path=str(OUT / f"{s}-{theme}.png"), clip=clip)
        report[f"errors-{theme}"] = errors
        pg.close()
    b.close()
print(json.dumps(report, indent=1))
