#!/usr/bin/env python3
"""Verify committed captures and the file:// comparison UI in headless Chromium."""

import argparse
import json
from pathlib import Path
from tempfile import TemporaryDirectory

from playwright.sync_api import sync_playwright

from capture_pairs import ROOT, check_png
from comparison_pairs import pairs


def verify(folder, browser_path=None, screenshots=None):
    manifest = json.loads((folder / "manifest.json").read_text())
    expected_rows = pairs()
    assert [(p["eval"], p["screen"], p["routes"]) for p in manifest["pairs"]] == [
        (p["eval"], p["screen"], p["routes"]) for p in expected_rows]
    expected_files = set()
    for pair in manifest["pairs"]:
        for theme in pair["themes"]:
            for side, route in pair["routes"].items():
                if route is None:
                    assert side not in pair["shots"][theme]
                    continue
                shot = pair["shots"][theme][side]
                path = folder / shot["src"]
                assert path.name == f"{pair['screen']}__{theme}__{side}.png"
                assert check_png(path) == [shot["width"], shot["height"]]
                if not pair.get("crop"):
                    assert [shot["width"], shot["height"]] == pair["viewport"]
                expected_files.add(path)
        if pair["themes"] == ["light", "dark"]:
            for side in pair["shots"]["light"]:
                assert (folder / pair["shots"]["light"][side]["src"]).read_bytes() != (folder / pair["shots"]["dark"][side]["src"]).read_bytes(), f"Identical themes: {pair['screen']} {side}"
    assert expected_files == set((folder / "shots").glob("*/*.png"))
    errors = []
    with sync_playwright() as playwright, TemporaryDirectory(prefix="compare-export-") as temp:
        options = dict(headless=True)
        if browser_path:
            options["executable_path"] = browser_path
        browser = playwright.chromium.launch(**options)
        context = browser.new_context(viewport=dict(width=1280, height=900), accept_downloads=True)
        page = context.new_page()
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.on("console", lambda message: errors.append(message.text) if message.type == "error" else None)
        page.goto((folder / "index.html").as_uri())
        assert page.evaluate("JSON.parse(document.getElementById('manifest').textContent)") == manifest
        assert page.locator("article.pair").count() == len(expected_rows)
        # The inline manifest, not fetch(), must power the page from disk.
        assert page.evaluate("JSON.parse(document.getElementById('manifest').textContent).pairs.length") == len(expected_rows)
        assert page.locator(".caption:visible").count() == 0
        assert page.locator(".links a:visible").count() == 0
        assert page.locator("figcaption").all_text_contents()[0:2] == ["Left", "Right"]
        assert "With skill" not in page.locator("main").inner_text()
        assert "Without skill" not in page.locator("main").inner_text()
        orders = page.evaluate("[...orders.values()].map(order => order[0])")
        assert set(orders) == {"with", "without"}, "Every pair must shuffle independently"
        first = page.locator("article.pair").first
        first_id = first.get_attribute("data-pair")
        first.locator('input[value="left"]').check()
        chosen_winner = page.evaluate("Object.values(choices)[0].winner")
        first.locator(".reveal").click()
        assert first.locator(".caption").is_visible()
        assert first.locator(".links a").count() == 4
        assert all("skill" in text.lower() for text in first.locator("figcaption").all_text_contents())
        assert first.locator('input[value="left"]').is_checked()
        first.locator(".reveal").click()
        assert not first.locator(".caption").count()
        # Choices have identity semantics even when non-blind order differs.
        page.locator("#blind").uncheck()
        correct_position = "left" if chosen_winner == "with" else "right"
        assert first.locator(f'input[value="{correct_position}"]').is_checked()
        page.locator("#theme").select_option("dark")
        assert not first.locator("input:checked").count()
        first.locator('input[value="same"]').check()
        page.reload()
        assert page.evaluate("Object.keys(choices).length") == 2
        page.locator("#theme").select_option("dark")
        assert first.locator('input[value="same"]').is_checked()
        with page.expect_download() as download_info:
            page.locator("#export").click()
        export_path = Path(temp) / "choices.json"
        download_info.value.save_as(export_path)
        exported = json.loads(export_path.read_text())
        assert exported["schemaVersion"] == 1 and len(exported["choices"]) == 2
        assert {choice["theme"] for choice in exported["choices"]} == {"light", "dark"}
        assert next(choice for choice in exported["choices"] if choice["theme"] == "light")["winner"] == chosen_winner
        assert next(choice for choice in exported["choices"] if choice["theme"] == "light")["blind"]
        page.locator("#coverage").select_option("unmatched")
        assert page.locator(".missing").count() == page.locator("article.pair").count()
        page.locator("#coverage").select_option("matched")
        assert page.locator(".missing").count() == 0
        page.locator("#coverage").select_option("all")
        page.locator("#theme").select_option("light")
        page.locator("#blind").uncheck()
        # Visit every pair to trigger lazy loading and compare the actual CSS
        # pixel reduction on each side, including 340/360 native popovers.
        for article in page.locator("article.pair").all():
            article.scroll_into_view_if_needed()
            article.locator("img").evaluate_all("images => Promise.all(images.map(img => img.decode()))")
            scales = article.locator("img").evaluate_all("images => images.map(img => img.getBoundingClientRect().width/img.naturalWidth)")
            assert max(scales) - min(scales) < .001
            for anchor in article.locator("a").all():
                href = anchor.get_attribute("href").split("?")[0].split("#")[0]
                assert (folder / href).exists(), href
        for width in (1440, 1280, 390):
            page.set_viewport_size(dict(width=width, height=900))
            page.evaluate("window.scrollTo(0,0)")
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            if screenshots:
                screenshots.mkdir(parents=True, exist_ok=True)
                page.screenshot(path=str(screenshots / f"page-{width}.png"))
        if screenshots:
            page.set_viewport_size(dict(width=1280, height=1000))
            page.locator("#evaluation").select_option("incident-dashboard")
            page.locator("#theme").select_option("dark")
            page.locator("article.pair").first.scroll_into_view_if_needed()
            page.screenshot(path=str(screenshots / "dashboard-pair.png"))
            page.locator("#evaluation").select_option("banking-onboarding")
            page.locator("#theme").select_option("light")
            page.locator('[data-pair="banking-onboarding/390-code"]').scroll_into_view_if_needed()
            page.screenshot(path=str(screenshots / "banking-code-pair.png"))
        # A restricted browser must still offer in-memory choices and export.
        restricted = browser.new_context()
        restricted.add_init_script("Object.defineProperty(window, 'localStorage', {get(){throw new Error('Storage disabled')}})")
        restricted_page = restricted.new_page()
        restricted_page.goto((folder / "index.html").as_uri())
        restricted_page.locator('article.pair input[value="same"]').first.check()
        assert "memory only" in restricted_page.locator("#storage-status").inner_text()
        assert restricted_page.evaluate("Object.keys(choices).length") == 1
        browser.close()
    assert not errors, errors
    print(f"PASS: {len(expected_rows)} screen/size combinations, {len(expected_files)} non-uniform PNGs; "
          "file:// UI, blind shuffle/reveal, same scale, persistence, JSON export, links and responsive layout.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--folder", type=Path, default=ROOT / "evals/iteration-1/compare")
    parser.add_argument("--browser", help="Optional Chromium executable")
    parser.add_argument("--screenshots", type=Path, help="Optional directory for verification screenshots (outside git)")
    args = parser.parse_args()
    verify(args.folder.resolve(), args.browser, args.screenshots)
