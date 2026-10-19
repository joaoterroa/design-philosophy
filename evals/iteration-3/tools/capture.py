#!/usr/bin/env python3
"""Capture task-specific final states without changing or repairing agent output.

Run after runner.py. Outputs are immutable source inputs here; capture failures,
errors and geometry issues are evidence. Four runs of each task produce 192 PNGs.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from urllib.parse import urlencode

from PIL import Image, ImageStat
from playwright.sync_api import sync_playwright
from study_paths import artifact_path

STUDY = Path(__file__).resolve().parents[1]
REPO = STUDY.parents[1]
FIXED_TIME = datetime(2026, 10, 18, 10, 0, tzinfo=timezone.utc)
SCREENS = {
    "oncall-menubar": ("main", "compose", "pending", "offline", "empty", "accepted"),
    "incident-dashboard": ("live", "stale", "surge"),
    "banking-onboarding": ("welcome", "details-error", "code", "code-error", "help", "done"),
}
DISPLAYS = {
    "oncall-menubar": (("menu", 400, 680),),
    "incident-dashboard": (("tv", 1920, 1080), ("laptop", 1440, 900)),
    "banking-onboarding": (("phone", 390, 844), ("small", 320, 568)),
}

METRICS = r"""() => {
  const rect = el => {const r=el.getBoundingClientRect(); return {
    x:r.x,y:r.y,width:r.width,height:r.height,bottom:r.bottom,right:r.right};};
  const shown = el => {const s=getComputedStyle(el),r=el.getBoundingClientRect();
    return s.display!=='none' && s.visibility!=='hidden' && +s.opacity!==0 && r.width>0 && r.height>0;};
  const inView=el=>{const r=el.getBoundingClientRect();return shown(el)&&r.bottom>0&&r.y<innerHeight&&r.right>0&&r.x<innerWidth;};
  const label=el=>(el.getAttribute('aria-label')||el.innerText||el.value||el.getAttribute('placeholder')||'').trim().slice(0,220);
  const all=[...document.querySelectorAll('body *')], visible=all.filter(shown);
  const counts = key => {const map={};visible.forEach(el=>{const value=getComputedStyle(el)[key];map[value]=(map[value]||0)+1;});
    return Object.entries(map).sort((a,b)=>b[1]-a[1]).slice(0,30).map(([value,count])=>({value,count}));};
  const controls=[...document.querySelectorAll('button,a,input,select,textarea,[role="button"]')].filter(shown).map(el=>({
    tag:el.tagName.toLowerCase(),role:el.getAttribute('role'),label:label(el),href:el.getAttribute('href'),
    type:el.getAttribute('type'),disabled:!!el.disabled,inViewport:inView(el),rect:rect(el),
    fontFamily:getComputedStyle(el).fontFamily,fontSize:getComputedStyle(el).fontSize,
    borderRadius:getComputedStyle(el).borderRadius,cornerShape:getComputedStyle(el).cornerShape||null,
  }));
  const itemSelector='[data-incident],.incident-row,.incident,.incident-card,tbody tr,[role="row"]';
  const items=[...document.querySelectorAll(itemSelector)].filter(shown).map(el=>({
    text:label(el),rect:rect(el),inViewport:inView(el),fullyInViewport:el.getBoundingClientRect().bottom<=innerHeight&&el.getBoundingClientRect().top>=0}));
  const textRuns=[];
  const walker=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);
  while(walker.nextNode()) {
    const node=walker.currentNode,el=node.parentElement;
    if(!node.textContent.trim()||!el||!shown(el)||['SCRIPT','STYLE'].includes(el.tagName))continue;
    const range=document.createRange();range.selectNodeContents(node);const r=range.getBoundingClientRect(),s=getComputedStyle(el);
    if(!r.width||!r.height)continue;
    textRuns.push({text:node.textContent.trim(),tag:el.tagName,rect:{x:r.x,y:r.y,width:r.width,height:r.height,bottom:r.bottom,right:r.right},
      fontSize:parseFloat(s.fontSize),fontWeight:s.fontWeight,color:s.color,inViewport:r.bottom>0&&r.y<innerHeight&&r.right>0&&r.x<innerWidth});
  }
  const unlabeledFields=[...document.querySelectorAll('input:not([type=hidden]),select,textarea')].filter(shown).filter(el=>!el.labels?.length&&!el.getAttribute('aria-label')&&!el.getAttribute('aria-labelledby')).map(el=>({id:el.id,name:el.name,type:el.type}));
  const app=document.querySelector('#app');
  return {
    title:document.title,lang:document.documentElement.lang,url:location.href,textRuns,unlabeledFields,
    bodyText:document.body.innerText,viewport:{width:innerWidth,height:innerHeight,dpr:devicePixelRatio},
    documentSize:{width:document.documentElement.scrollWidth,height:document.documentElement.scrollHeight},
    horizontalOverflow:document.documentElement.scrollWidth>innerWidth,
    app:app?rect(app):null,controls,links:controls.filter(c=>c.tag==='a'),
    smallTargets:controls.filter(c=>c.inViewport&&(c.rect.width<44||c.rect.height<44)),
    headings:[...document.querySelectorAll('h1,h2,h3,[role="heading"]')].filter(shown).map(el=>({text:label(el),rect:rect(el),fontSize:getComputedStyle(el).fontSize})),
    fonts:counts('fontFamily'),fontSizes:counts('fontSize'),colors:counts('color'),backgrounds:counts('backgroundColor'),
    radii:counts('borderRadius'),cornerShapes:counts('cornerShape'),items,
    visibleItemCount:items.filter(i=>i.inViewport).length,
    fullyVisibleItemCount:items.filter(i=>i.fullyInViewport).length,
    overflowElements:visible.filter(el=>{const r=el.getBoundingClientRect();return r.right>innerWidth+1||r.left< -1;}).slice(0,30).map(el=>({tag:el.tagName,id:el.id,classes:el.className,rect:rect(el)})),
    clock:new Date().toISOString(),prefersDark:matchMedia('(prefers-color-scheme: dark)').matches,
  };
}"""


def resolve_path(value, protocol):
    path = Path(value)
    if path.is_absolute():
        return path
    return (REPO if path.parts and path.parts[0] == "evals" else protocol.parent) / path


def write_json(path, data):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(data, indent=2) + "\n")
    temporary.replace(path)


def output_hash(root):
    digest = hashlib.sha256()
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        digest.update(path.relative_to(root).as_posix().encode() + b"\0")
        digest.update(path.read_bytes() + b"\0")
    return digest.hexdigest()


def check_png(path):
    with Image.open(path) as shot:
        shot.load()
        variance = max(ImageStat.Stat(shot.convert("RGB")).var)
        return {"dimensions": list(shot.size), "maxChannelVariance": variance,
                "nonUniform": variance >= 1, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def capture_run(browser, record, protocol, args):
    task = record["task"]
    if task not in SCREENS:
        raise ValueError(f"Unknown task {task}")
    artifact = artifact_path(record, protocol.parent).resolve()
    output = artifact / "outputs"
    app = output / "app/index.html"
    report_path = artifact / "capture.json"
    if report_path.exists() and not args.replace_capture:
        raise RuntimeError(f"{record['id']}: capture.json exists; use --replace-capture to repeat collection")
    report = {"runId": record["id"], "task": task, "fixedTime": FIXED_TIME.isoformat(),
              "locale": "en-GB", "timezone": "Europe/London", "DPR": 1,
              "reducedMotion": "reduce", "source": str(app), "shots": [],
              "expectedShots": len(SCREENS[task]) * len(DISPLAYS[task]) * 2}
    artifact.mkdir(parents=True, exist_ok=True)
    if not app.exists():
        report.update({"complete": False, "error": "Missing outputs/app/index.html"})
        write_json(report_path, report)
        return report
    before = output_hash(output)
    report["outputSha256Before"] = before
    shots = artifact / "shots"
    shots.mkdir(exist_ok=True)
    for display, width, height in DISPLAYS[task]:
        for screen in SCREENS[task]:
            for theme in ("light", "dark"):
                name = f"{screen}__{display}__{theme}"
                shot = {"id": name, "screen": screen, "display": display,
                        "theme": theme, "viewport": [width, height],
                        "path": f"shots/{name}.png", "consoleErrors": [],
                        "pageErrors": [], "blockedRequests": [], "failedRequests": []}
                context = browser.new_context(
                    viewport={"width": width, "height": height}, device_scale_factor=1,
                    locale="en-GB", timezone_id="Europe/London", color_scheme=theme,
                    reduced_motion="reduce", service_workers="block",
                )
                context.set_default_timeout(12000)
                page = context.new_page()
                page.on("pageerror", lambda e: shot["pageErrors"].append(str(e)))
                page.on("console", lambda e: shot["consoleErrors"].append(e.text) if e.type == "error" else None)
                page.on("requestfailed", lambda r: shot["failedRequests"].append({"url": r.url, "failure": r.failure}))

                def offline(route):
                    if route.request.url.startswith(("http:", "https:", "ws:", "wss:")):
                        shot["blockedRequests"].append(route.request.url)
                        route.abort()
                    else:
                        route.continue_()

                context.route("**/*", offline)
                try:
                    # Wall time is frozen but RAF/timers can settle for 1.5s.
                    page.clock.install(time=FIXED_TIME)
                    page.clock.pause_at(FIXED_TIME)
                    suffix = urlencode({"screen": screen, "theme": theme, "display": display})
                    shot["url"] = app.as_uri() + "?" + suffix
                    page.goto(shot["url"], wait_until="load", timeout=15000)
                    page.clock.run_for(1500)
                    page.clock.set_fixed_time(FIXED_TIME)
                    page.evaluate("document.fonts.ready")
                    page.evaluate("window.scrollTo(0,0)")
                    page.mouse.move(width - 1, height - 1)
                    shot["metrics"] = page.evaluate(METRICS)
                    path = shots / f"{name}.png"
                    if task == "oncall-menubar":
                        # Native 360px menu, no scaling. Capture the exact #app
                        # bounding box if it fits; otherwise retain viewport and flag.
                        bounds = page.locator("#app").bounding_box()
                        shot["menuBounds"] = bounds
                        fits = bounds and bounds["x"] >= 0 and bounds["y"] >= 0 and bounds["x"] + bounds["width"] <= width + .1 and bounds["y"] + bounds["height"] <= height + .1
                        shot["menuFitsViewport"] = bool(fits)
                        shot["menuExpectedWidth"] = bool(bounds and abs(bounds["width"] - 360) < 1)
                        if fits:
                            page.screenshot(path=str(path), clip=bounds, animations="disabled", caret="hide")
                        else:
                            page.screenshot(path=str(path), full_page=False, animations="disabled", caret="hide")
                    else:
                        page.screenshot(path=str(path), full_page=False, animations="disabled", caret="hide")
                    shot.update(check_png(path))
                    shot["captureSucceeded"] = True
                except Exception as error:
                    shot["captureSucceeded"] = False
                    shot["error"] = str(error)
                finally:
                    context.close()
                report["shots"].append(shot)
                write_json(report_path, report)
                print(f"CAPTURE {record['id']} {name} {'ok' if shot['captureSucceeded'] else 'FAILED'}", flush=True)
    report["outputSha256After"] = output_hash(output)
    report["sourceUnchanged"] = report["outputSha256After"] == before
    report["capturedShots"] = sum(s.get("captureSucceeded", False) for s in report["shots"])
    report["complete"] = (report["capturedShots"] == report["expectedShots"]
                          and all(s.get("nonUniform") for s in report["shots"])
                          and report["sourceUnchanged"])
    hashes = {}
    texts = {}
    for shot in report["shots"]:
        if shot.get("sha256"):
            hashes.setdefault(shot["sha256"], []).append(shot["id"])
        text = shot.get("metrics", {}).get("bodyText", "")
        if text:
            text_key = hashlib.sha256(text.encode()).hexdigest()
            texts.setdefault(text_key, []).append(shot["id"])
    # Equal images/text can be legitimate across themes and viewports. Keep the
    # groups for reviewers to identify ignored state/theme hooks; do not grade.
    report["identicalImageGroups"] = [ids for ids in hashes.values() if len(ids) > 1]
    report["identicalTextGroups"] = [ids for ids in texts.values() if len(ids) > 1]
    report["issues"] = {
        "consoleErrorShots": sum(bool(s["consoleErrors"]) for s in report["shots"]),
        "pageErrorShots": sum(bool(s["pageErrors"]) for s in report["shots"]),
        "networkDependentShots": sum(bool(s["blockedRequests"]) for s in report["shots"]),
        "horizontalOverflowShots": sum(bool(s.get("metrics", {}).get("horizontalOverflow")) for s in report["shots"]),
        "menuClippedShots": sum(s.get("menuFitsViewport") is False for s in report["shots"]),
    }
    write_json(report_path, report)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--protocol", type=Path, default=STUDY / "protocol.json")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--run", action="append")
    group.add_argument("--all", action="store_true")
    parser.add_argument("--browser-path")
    parser.add_argument("--replace-capture", action="store_true", help="Repeat screenshots only; never reruns or repairs agents")
    args = parser.parse_args()
    args.protocol = args.protocol.resolve()
    protocol = json.loads(args.protocol.read_text())
    records = protocol["runs"]
    if not args.all:
        unknown = set(args.run) - {r["id"] for r in records}
        if unknown:
            parser.error(f"Unknown IDs: {sorted(unknown)}")
        records = [r for r in records if r["id"] in args.run]
    results = []
    with sync_playwright() as playwright:
        launch = {"headless": True}
        if args.browser_path:
            launch["executable_path"] = args.browser_path
        browser = playwright.chromium.launch(**launch)
        try:
            for record in records:
                results.append(capture_run(browser, record, args.protocol, args))
        finally:
            browser.close()
    print(json.dumps({"runs": len(results), "completeRuns": sum(r["complete"] for r in results),
                      "capturedShots": sum(r.get("capturedShots", 0) for r in results)}), flush=True)
    return 0 if all(r["complete"] for r in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
