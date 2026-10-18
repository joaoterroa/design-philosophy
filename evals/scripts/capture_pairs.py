#!/usr/bin/env python3
"""Capture offline, semantically matched iteration-1 prototypes.

python -m pip install -r evals/scripts/requirements-compare.txt
python -m playwright install chromium
python evals/scripts/capture_pairs.py

The file-based sources are read-only. Each shot gets fresh browser storage,
the same viewport/scheme/locale/time zone, DPR 1 and a controlled clock. Phone
and dashboard shots are viewport-only. Popovers are cropped to native bounds;
the comparison page pads, rather than stretches, unequal native panel sizes.
"""

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re

from PIL import Image, ImageStat
from playwright.sync_api import sync_playwright

from comparison_pairs import EVALS, SIDES, pairs

ROOT = Path(__file__).resolve().parents[2]
FIXED_TIME = datetime(2026, 10, 18, 10, 0, tzinfo=timezone.utc)


def check_png(path, expected=None):
    with Image.open(path) as image:
        image.load()
        if expected and list(image.size) != list(expected):
            raise AssertionError(f"{path}: {image.size} != {expected}")
        if max(ImageStat.Stat(image.convert("RGB")).var) < 1:
            raise AssertionError(f"Blank/uniform screenshot: {path}")
        return list(image.size)


def capture(root, output, browser_path=None):
    rows = pairs()
    metadata = {e: json.loads((root / "evals/iteration-1" / e / "eval_metadata.json").read_text()) for e in EVALS}
    report = []
    with sync_playwright() as playwright:
        options = dict(headless=True)
        if browser_path:
            options["executable_path"] = browser_path
        browser = playwright.chromium.launch(**options)
        try:
            for row in rows:
                row["shots"] = {}
                row["sources"] = {}
                for theme in row["themes"]:
                    row["shots"][theme] = {}
                    row["sources"][theme] = {}
                    for side in SIDES:
                        route = row["routes"][side]
                        if route is None:
                            continue
                        relative_source = Path(row["eval"]) / f"{side}_skill/outputs" / row.get("source", "app/index.html")
                        source = root / "evals/iteration-1" / relative_source
                        suffix = route.format(theme=theme)
                        row["sources"][theme][side] = "../" + relative_source.as_posix() + suffix
                        width, height = row["viewport"]
                        context = browser.new_context(
                            viewport=dict(width=width, height=height), device_scale_factor=1,
                            color_scheme=theme, reduced_motion="reduce", locale="en-GB",
                            timezone_id="Europe/London", service_workers="block",
                        )
                        errors, network = [], []
                        page = context.new_page()
                        page.on("pageerror", lambda error: errors.append(str(error)))
                        page.on("console", lambda message: errors.append(message.text) if message.type == "error" else None)

                        def offline(route):
                            if route.request.url.startswith(("http:", "https:")):
                                network.append(route.request.url)
                                route.abort()
                            else:
                                route.continue_()

                        context.route("**/*", offline)
                        page.clock.install(time=FIXED_TIME)
                        page.clock.pause_at(FIXED_TIME)
                        page.goto(source.as_uri() + suffix, wait_until="load")
                        # Remove only the baseline's explicitly prototype-only footer.
                        # No product styles, content, fonts or layout are normalised.
                        if row["eval"] == "banking-onboarding" and side == "without":
                            page.add_style_tag(content=".proto { display: none !important; }")
                        if row.get("action") == "passcode-mismatch" and side == "with":
                            page.locator("#pass").fill("583920")
                            page.locator("#pass2").fill("583921")
                            page.locator("#pass-form").evaluate("form => form.requestSubmit()")
                        # 1.5s delivers the text preview (1.2s) and slow-setup note
                        # (0.8s), without advancing normal checks to a later screen.
                        page.clock.run_for(1500)
                        page.evaluate("document.fonts.ready")
                        page.mouse.move(1099, 799)
                        page.evaluate("window.scrollTo(0, 0)")
                        details = page.evaluate("""() => ({
                            title: document.title,
                            theme: document.documentElement.dataset.theme || matchMedia('(prefers-color-scheme: dark)').matches && 'dark' || 'light',
                            documentHeight: document.documentElement.scrollHeight,
                            horizontalOverflow: document.documentElement.scrollWidth > innerWidth,
                            heading: [...document.querySelectorAll('h1')].filter(e => e.getBoundingClientRect().height).map(e => e.textContent.trim())
                        })""")
                        if details["theme"] != theme:
                            raise AssertionError(f"Wrong theme: {row['screen']} {side}: {details}")
                        destination = output / "shots" / row["eval"] / f"{row['screen']}__{theme}__{side}.png"
                        destination.parent.mkdir(parents=True, exist_ok=True)
                        target = page.locator(row["crop"][side]) if row.get("crop") else page
                        target.screenshot(path=str(destination), animations="disabled", caret="hide")
                        size = check_png(destination, None if row.get("crop") else row["viewport"])
                        if errors or network:
                            raise AssertionError(f"{row['screen']} {side}: errors={errors}, network={network}")
                        row["shots"][theme][side] = dict(src=destination.relative_to(output).as_posix(), width=size[0], height=size[1])
                        report.append(dict(eval=row["eval"], screen=row["screen"], side=side,
                                           pixels=size, **details))
                        context.close()
                print(f"Captured {row['eval']}/{row['screen']}", flush=True)
        finally:
            browser.close()
    manifest = dict(version=1, deviceScaleFactor=1, locale="en-GB", timezone="Europe/London",
                    clock="2026-10-18T10:00:00Z + 1500ms", viewportOnly=True,
                    evals=[dict(id=e, prompt=metadata[e]["prompt"]) for e in EVALS], pairs=rows)
    payload = json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"
    output.mkdir(parents=True, exist_ok=True)
    (output / "manifest.json").write_text(payload)
    (output / "capture-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    template = (ROOT / "evals/iteration-1/compare/index.html").read_text()
    # Inline the manifest: fetch(file://...) is blocked in some browsers.
    safe_payload = payload.replace("<", "\\u003c")
    template, count = re.subn(r'(?s)(<script id="manifest" type="application/json">).*?(</script>)',
                              lambda match: match[1] + "\n" + safe_payload + match[2], template)
    if count != 1:
        raise AssertionError("Comparison page must contain exactly one inline manifest")
    (output / "index.html").write_text(template)
    expected = {output / shot["src"] for row in rows for theme in row["shots"].values() for shot in theme.values()}
    actual = set((output / "shots").glob("*/*.png"))
    if actual != expected:
        raise AssertionError(f"Unexpected/missing PNGs: {actual ^ expected}")
    print(f"Verified {len(expected)} non-uniform PNGs across {len(rows)} screen pairs.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=ROOT, help="Read prototypes from this checkout")
    parser.add_argument("--output", type=Path, default=ROOT / "evals/iteration-1/compare")
    parser.add_argument("--browser", help="Optional Chromium executable (default: Playwright's installed Chromium)")
    args = parser.parse_args()
    capture(args.repo_root.resolve(), args.output.resolve(), args.browser)
