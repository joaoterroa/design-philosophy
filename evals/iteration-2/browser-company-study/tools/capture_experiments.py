#!/usr/bin/env python3
"""Capture original/revision probes offline and record discriminating measurements.

Requires the iteration-1 comparison requirements. Run build_experiments.py first.
"""

from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import sys

from PIL import Image, ImageStat
from playwright.sync_api import sync_playwright

from build_experiments import EXPERIMENTS, REPO, STUDY

TIME = datetime(2026, 10, 18, 10, tzinfo=timezone.utc)

MEASURE = """() => {
 const rect = s => {const e=document.querySelector(s);if(!e)return null;const r=e.getBoundingClientRect();return {x:r.x,y:r.y,width:r.width,height:r.height,bottom:r.bottom};};
 const visible = s => [...document.querySelectorAll(s)].filter(e=>e.getBoundingClientRect().height && !e.closest('[hidden]')).length;
 const pop=document.querySelector('#popover');
 return {horizontalOverflow:document.documentElement.scrollWidth>innerWidth,
   viewport:[innerWidth,innerHeight],pop:rect('#popover'),
   dutyType:pop?getComputedStyle(pop.querySelector('.answer')||pop).fontSize:null,
   action:rect('#code-form button[type=submit]'),
   safety:rect('.preview-safety strong'),
   message:rect('#message'),
   visibleOpen:visible('#open-list > li'),totalOpen:document.querySelectorAll('#open-list > li').length,
   hiddenSummary:document.querySelector('#more:not([hidden])')?.textContent||'',
   phoneTargets:[...document.querySelectorAll('.screen:not([hidden]) button')].filter(e=>e.getBoundingClientRect().width).map(e=>({text:e.textContent.trim(),height:e.getBoundingClientRect().height})),
   menuText:pop?.textContent.replace(/\\s+/g,' ').trim()||null,
   bankText:document.querySelector('[data-screen=code]')?.textContent.replace(/\\s+/g,' ').trim()||null
 };
}"""


def cases(experiment):
    evaluation = EXPERIMENTS[experiment]["evaluation"]
    if evaluation == "oncall-menubar":
        return [(state, (1100, 800), f"?state={state}&theme={{theme}}", "#popover")
                for state in ("oncall", "pending", "accepted", "offline")]
    if evaluation == "banking-onboarding":
        return [(f"{width}-{state}", (width, height), f"?theme={{theme}}#{state}", None)
                for width, height in ((390, 844), (320, 568)) for state in ("code", "code-wrong", "code-help")]
    return [(f"{display}-{state}", size, f"?display={mode}&state={state}&theme={{theme}}&frozen", None)
            for display, mode, size in (("tv", "wall", (1920, 1080)), ("laptop", "desk", (1440, 900)))
            for state in ("live", "stale", "surge")]


def run():
    manifest = json.loads((STUDY / "experiments/manifest.json").read_text())
    for experiment in manifest:
        original = REPO / experiment["source"]
        copy = STUDY / "experiments" / experiment["id"] / "app"
        for relative, expected in experiment["sourceHashes"].items():
            assert sha256((original / relative).read_bytes()).hexdigest() == expected, f"Source changed: {relative}"
            if relative != "index.html":
                assert sha256((copy / relative).read_bytes()).hexdigest() == expected, f"Experimental app logic/data changed: {relative}"
    reports = []
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        for experiment in EXPERIMENTS:
            evaluation = EXPERIMENTS[experiment]["evaluation"]
            for screen, viewport, suffix, crop in cases(experiment):
                for theme in ("light", "dark"):
                    records = []
                    for variant in ("original", "revision"):
                        index = (REPO / f"evals/iteration-1/{evaluation}/with_skill/outputs/app/index.html" if variant == "original"
                                 else STUDY / f"experiments/{experiment}/app/index.html")
                        context = browser.new_context(viewport=dict(zip(("width", "height"), viewport)),
                                                      device_scale_factor=1, color_scheme=theme, reduced_motion="reduce",
                                                      locale="en-GB", timezone_id="Europe/London", service_workers="block")
                        errors, network = [], []
                        page = context.new_page()
                        page.on("pageerror", lambda error: errors.append(str(error)))
                        page.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" else None)
                        def offline(route):
                            if route.request.url.startswith(("http:", "https:")):
                                network.append(route.request.url); route.abort()
                            else:
                                route.continue_()
                        context.route("**/*", offline)
                        page.clock.install(time=TIME); page.clock.pause_at(TIME)
                        page.goto(index.as_uri() + suffix.format(theme=theme), wait_until="load")
                        page.clock.run_for(1500); page.evaluate("document.fonts.ready")
                        page.evaluate("scrollTo(0,0)")
                        page.mouse.move(1099, 799)
                        info = page.evaluate(MEASURE)
                        assert not errors and not network, (errors, network)
                        assert not info["horizontalOverflow"], (experiment, screen, theme, variant)
                        path = STUDY / "figures" / f"{experiment}__{screen}__{theme}__{variant}.png"
                        (page.locator(crop) if crop else page).screenshot(path=str(path), animations="disabled", caret="hide")
                        with Image.open(path) as image:
                            assert max(ImageStat.Stat(image.convert('RGB')).var) > 1
                            pixels = list(image.size)
                        records.append(dict(variant=variant,src=path.relative_to(STUDY).as_posix(),pixels=pixels,**info))
                        context.close()
                    if evaluation == "oncall-menubar":
                        assert records[0]["menuText"] == records[1]["menuText"], "Changed menu copy/data"
                        assert records[1]["pop"]["width"] == 340 and records[1]["pop"]["height"] <= 640
                    if evaluation == "banking-onboarding":
                        assert records[0]["bankText"] == records[1]["bankText"], "Changed SMS/safety copy"
                        assert records[0]["action"] == records[1]["action"], "Moved the critical code action"
                        assert all(t["height"] >= 48 for t in records[1]["phoneTargets"])
                    reports.append(dict(experiment=experiment,screen=screen,theme=theme,records=records))
            print(f"Captured {experiment}", flush=True)
        # Exercise actual main paths on revisions; screenshots alone cannot prove
        # that an overlay treatment left interaction and pending status intact.
        for experiment in ("menu-type", "menu-object"):
            page = browser.new_page(viewport=dict(width=1100,height=800))
            page.goto((STUDY / f"experiments/{experiment}/app/index.html").as_uri()+"?state=oncall&theme=light")
            page.locator('[data-act=handover]').click()
            page.locator('input[name=to][value=pr]').check(force=True)
            page.locator('[data-act=send]').click()
            assert "until Priya accepts" in page.locator('#popover').inner_text()
            assert page.evaluate('rota.state.onCall')
            page.close()
        page = browser.new_page(viewport=dict(width=390,height=844))
        page.goto((STUDY / "experiments/bank-message/app/index.html").as_uri()+"?theme=light#code")
        assert page.locator('.blank').text_content().strip() == '▬▬▬ ▬▬▬'
        page.locator('#otp').fill('000000'); page.locator('#code-form button[type=submit]').click()
        assert page.locator('#code-error').is_visible()
        page.locator('#otp').fill('482913'); page.locator('#code-form button[type=submit]').click()
        assert page.locator('[data-screen=passcode]').is_visible()
        page.locator('#help-open').click(); assert page.locator('#help').is_visible()
        page.keyboard.press('Escape'); assert not page.locator('#help').is_visible()
        browser.close()
    (STUDY / "experiments/results.json").write_text(json.dumps(reports, indent=2) + "\n")
    print(f"Verified {len(reports)*2} paired captures, content invariants, menu handover and banking code/help paths.")


if __name__ == "__main__":
    run()
