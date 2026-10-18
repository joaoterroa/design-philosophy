import sys, pathlib, json
from playwright.sync_api import sync_playwright
out = pathlib.Path(sys.argv[1]); app = pathlib.Path(sys.argv[2]).resolve()
states = ["off","on","choose","pending","accepted","declined","incoming","offline","schedule"]
report = {}
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/opt/pw-browsers/chromium', args=['--headless=new'])
    for theme in ["light","dark"]:
        ctx = b.new_context(viewport={"width":1100,"height":760}, device_scale_factor=2, color_scheme=theme)
        pg = ctx.new_page()
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.on("console", lambda m: errs.append(m.text) if m.type=="error" else None)
        for i, s in enumerate(states, 1):
            pg.goto(f"{app.as_uri()}?theme={theme}#{s}")
            pg.wait_for_timeout(700)
            pop = pg.locator("#pop").bounding_box()
            body = pg.evaluate("""() => { const b=document.querySelector('.pop-body'); return {sh:b.scrollHeight, ch:b.clientHeight, sw:b.scrollWidth, cw:b.clientWidth} }""")
            font = pg.evaluate("getComputedStyle(document.querySelector('.pop')).fontFamily")
            report[f"{theme}-{s}"] = {"pop": pop, "body": body}
            # crop: menu bar + panel
            clip = {"x": pop["x"]-24, "y": 0, "width": pop["width"]+48+110, "height": min(760, pop["y"]+pop["height"]+24)}
            pg.screenshot(path=str(out/f"{i:02d}-{s}-{theme}.png"), clip=clip)
        # hover state on the on-call screen
        pg.goto(f"{app.as_uri()}?theme={theme}#on"); pg.wait_for_timeout(400)
        pg.locator(".row").nth(1).hover(); pg.wait_for_timeout(300)
        pop = pg.locator("#pop").bounding_box()
        pg.screenshot(path=str(out/f"10-on-hover-{theme}.png"), clip={"x": pop["x"]-24, "y": 0, "width": pop["width"]+158, "height": pop["y"]+pop["height"]+24})
        if theme=="light":
            pg.screenshot(path=str(out/"00-full-page-light.png"))
        report[f"{theme}-errors"] = errs
        ctx.close()
    b.close()
print(json.dumps(report, indent=1))
print("font:", font)
