#!/usr/bin/env python3
"""Check evidence integrity, protected sources, report interactions and layout."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory

from PIL import Image, ImageStat
from playwright.sync_api import sync_playwright

from build_experiments import REPO, STUDY


def verify(screenshots=None):
    catalog = json.loads((STUDY / "evidence/catalog.json").read_text())
    results = json.loads((STUDY / "experiments/results.json").read_text())
    assert len(catalog) == 21 and len(results) == 40
    for item in catalog:
        path = STUDY / "evidence" / item["file"]
        assert sha256(path.read_bytes()).hexdigest() == item["sha256"]
        with Image.open(path) as image:
            assert list(image.size) == item["pixels"]
    for video in json.loads((STUDY / "evidence/video-provenance.json").read_text()):
        assert sha256((STUDY / video["file"]).read_bytes()).hexdigest() == video["sha256"]
    expected = set()
    for pair in results:
        for record in pair["records"]:
            path = STUDY / record["src"]
            expected.add(path)
            with Image.open(path) as image:
                assert list(image.size) == record["pixels"]
                assert max(ImageStat.Stat(image.convert("RGB")).var) > 1
    assert expected == set((STUDY / "figures").glob("*.png")) and len(expected) == 80
    for experiment in json.loads((STUDY / "experiments/manifest.json").read_text()):
        for relative, expected_hash in experiment["sourceHashes"].items():
            assert sha256((REPO / experiment["source"] / relative).read_bytes()).hexdigest() == expected_hash
    protected = ["SKILL.md", "references", "templates", "evals/iteration-1"]
    assert not subprocess.check_output(["git", "diff", "HEAD", "--", *protected],cwd=REPO,text=True)
    errors, network = [], []
    with sync_playwright() as playwright, TemporaryDirectory(prefix="study-review-") as temp:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context(viewport=dict(width=1440,height=1000),accept_downloads=True)
        def offline(route):
            if route.request.url.startswith(("http:", "https:")):
                network.append(route.request.url);route.abort()
            else:
                route.continue_()
        context.route("**/*",offline)
        page=context.new_page()
        page.on("pageerror",lambda e:errors.append(str(e)))
        page.on("console",lambda m:errors.append(m.text) if m.type=="error" else None)
        page.goto((STUDY/"index.html").as_uri(),wait_until="load")
        assert page.title()=="Browser Company sensibility · evidence study"
        assert page.locator('.finding').count()==5
        assert page.locator('.recommendation').count()==6
        assert page.locator('.experiment').count()==4
        assert page.evaluate("data.study") == json.loads((STUDY/"study.json").read_text())
        assert page.evaluate("data.catalog") == catalog
        assert page.evaluate("data.results") == results
        assert page.locator('#source-gallery .source-card, #additional-sources .source-card').count()==21
        # Decode all embedded images, including lazy ones, without network.
        page.locator('img[src]').evaluate_all("images => {images.forEach(img=>img.loading='eager'); return Promise.race([Promise.all(images.map(img=>img.decode())),new Promise((_,reject)=>setTimeout(()=>reject(new Error('Image decode timeout')),30000))])}")
        for anchor in page.locator('a[href]').all():
            href=anchor.get_attribute('href')
            if href.startswith(('http:','https:','#','data:','blob:')):
                continue
            path=href.split('?')[0].split('#')[0]
            assert (STUDY/path).exists(), href
        # Inspect equal pixel reduction on each original/revision pair.
        for experiment in page.locator('.experiment').all():
            scales=experiment.locator('.stage img').evaluate_all('images=>images.map(img=>img.getBoundingClientRect().width/img.naturalWidth)')
            assert abs(scales[0]-scales[1])<.001
        first=page.locator('.experiment').first
        first.locator('input[value=left]').check()
        chosen=page.evaluate('Object.values(votes)[0].winner')
        page.locator('#blind').check()
        assert page.locator('.experiment .metrics').count()==0
        assert page.locator('.experiment .links').count()==0
        assert first.locator('.side-label').all_text_contents()==['Left','Right']
        assert page.evaluate("[...orders.values()].every(order=>order.length===2&&new Set(order).size===2)")
        first.locator('input[value=same]').check()
        page.locator('#shot-theme').select_option('dark')
        assert not first.locator('input:checked').count()
        first.locator('input[value=right]').check()
        page.reload()
        assert page.evaluate('Object.keys(votes).length')==2
        with page.expect_download() as download:
            page.locator('#export-votes').click()
        path=Path(temp)/'review.json';download.value.save_as(path)
        exported=json.loads(path.read_text())
        assert exported['schemaVersion']==1 and len(exported['choices'])==2
        assert {v['theme'] for v in exported['choices']}=={'light','dark'}
        assert all(v['labelsHidden'] for v in exported['choices'])
        # Zoom is keyboard-usable and dismisses through the native dialog.
        page.locator('.image-button').first.click()
        assert page.locator('#viewer').is_visible()
        page.keyboard.press('Escape');assert not page.locator('#viewer').is_visible()
        # All three clips must decode as actual video, not just show posters.
        for video in page.locator('video').all():
            video.evaluate("async v=>{v.preload='auto';v.load();await v.play();v.pause();}")
            assert video.evaluate('v=>v.duration>0&&v.videoWidth>0')
        for width in (1440,1280,390):
            page.set_viewport_size(dict(width=width,height=1000))
            page.evaluate('scrollTo(0,0)')
            assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
            if screenshots:
                screenshots.mkdir(parents=True,exist_ok=True)
                page.screenshot(path=str(screenshots/f'report-{width}.png'))
        if screenshots:
            page.set_viewport_size(dict(width=1440,height=1100))
            page.locator('#compare').scroll_into_view_if_needed()
            page.screenshot(path=str(screenshots/'comparison.png'))
            page.locator('[data-experiment=bank-message]').scroll_into_view_if_needed()
            page.screenshot(path=str(screenshots/'bank-experiment.png'))
            page.locator('#shot-theme').select_option('dark')
            page.locator('#chrome-theme').click()
            page.locator('[data-experiment=menu-object]').scroll_into_view_if_needed()
            page.screenshot(path=str(screenshots/'menu-dark-experiment.png'))
        browser.close()
    assert not errors and not network,(errors,network)
    record=dict(status='pass',referenceImages=len(catalog),experimentPairs=len(results),pngs=len(expected),
                consoleErrors=errors,networkRequests=network,viewports=[1440,1280,390],
                checks=['protected source hashes','reference image hashes/dimensions','nonuniform PNGs',
                        'offline file:// report','equal original/revision image scale','local links',
                        'label hiding and independent pair orders','theme-specific preferences',
                        'localStorage persistence','review JSON download','image dialog keyboard dismissal',
                        'three embedded videos decode','responsive layout'])
    (STUDY/'verification.json').write_text(json.dumps(record,indent=2)+'\n')
    print('PASS: 21 primary images, 80 captures, protected sources, offline page, videos, review/export and responsive layout.')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--screenshots',type=Path)
    args=parser.parse_args()
    verify(args.screenshots)
