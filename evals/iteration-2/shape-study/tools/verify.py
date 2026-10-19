#!/usr/bin/env python3
"""Verify provenance, controlled captures and offline report interactions."""
import json
from pathlib import Path
import subprocess
from urllib.parse import urlparse, unquote
from PIL import Image, ImageStat
from playwright.sync_api import sync_playwright
from capture import STUDY, REPO, digest

QA=Path('/private/tmp/shape-study-qa');QA.mkdir(exist_ok=True)

def main():
    manifest=json.loads((STUDY/'experiments/manifest.json').read_text())
    results=json.loads((STUDY/'experiments/results.json').read_text())
    catalog=json.loads((STUDY/'evidence/catalog.json').read_text())
    assert len(results['records'])==20
    for source in manifest['sources']:
        for file,expected in source['sourceHashes'].items():
            assert digest(REPO/source['source']/file)==expected
            for variant in ('curve-only','radius-only','calibrated'):
                copy=STUDY/f"experiments/{source['evaluation']}/{variant}/app"/file
                if file=='index.html':
                    assert copy.read_text().replace('<link rel="stylesheet" href="shape.css">\n','')==(REPO/source['source']/file).read_text()
                else: assert digest(copy)==expected
    for c in results['records']:
        baseline=c['records'][0]
        for r in c['records']:
            assert digest(STUDY/r['file'])==r['sha256']
            with Image.open(STUDY/r['file']) as im:
                assert list(im.size)==r['pixels']==baseline['pixels']
                assert max(ImageStat.Stat(im.convert('RGB')).var)>1
            assert r['metrics']['boxes']==baseline['metrics']['boxes']
            assert r['metrics']['text']==baseline['metrics']['text']
    for r in catalog:
        assert digest(REPO/r['localSource'])==r['sha256']
        assert digest(STUDY/f"evidence/{r['id']}__corner.png")==r['cornerSha256']
    protected=subprocess.check_output(['git','diff','--name-only','--','SKILL.md','references','templates','evals/iteration-1'],cwd=REPO,text=True)
    assert not protected,protected
    checks=[]
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True)
        context=browser.new_context(viewport=dict(width=1440,height=1000),accept_downloads=True)
        network=[];errors=[]
        def offline(route):
            if route.request.url.startswith(('http:','https:')):network.append(route.request.url);route.abort()
            else:route.continue_()
        context.route('**/*',offline)
        page=context.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
        page.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
        page.goto((STUDY/'index.html').as_uri(),wait_until='load')
        assert page.title()=='Shape, craft, and the next iteration'
        for i in range(11):
            page.locator('#reference').select_option(str(i));page.locator('#referenceImage').evaluate('(e)=>e.decode()')
            assert page.locator('#referenceImage').evaluate('(e)=>e.naturalWidth>0')
        page.locator('#reference').select_option('0')
        ids=page.locator('#case option').evaluate_all('(es)=>es.map(e=>e.value)')
        for id in ids:
            page.locator('#case').select_option(id)
            for theme in ('light','dark'):
                page.locator('#shotTheme').select_option(theme)
                for variant in ('calibrated','curve-only','radius-only'):
                    page.locator('#variant').select_option(variant)
                    page.locator('#comparison img').evaluate_all('(es)=>Promise.all(es.map(e=>e.decode()))')
                    dims=page.locator('#comparison img').evaluate_all('(es)=>es.map(e=>({width:e.getBoundingClientRect().width,height:e.getBoundingClientRect().height,natural:e.naturalWidth}))')
                    assert dims[0]==dims[1],(id,theme,variant,dims)
        checks.append('All 60 full-screen pair combinations load at identical scale')
        page.locator('#case').select_option('bank-code-390');page.locator('#shotTheme').select_option('light');page.locator('#variant').select_option('calibrated')
        orders=set()
        for _ in range(24):
            page.locator('#blind').check();orders.add(tuple(page.evaluate('currentOrder')))
            labels=page.locator('#comparison h3').all_text_contents();assert labels==['Left','Right'],labels
            assert page.locator('#assessment').is_hidden() and page.locator('#liveLinks').is_hidden()
            page.locator('#blind').uncheck()
        assert len(orders)==2,'Randomization did not produce both orders'
        page.locator('#blind').check();page.locator('[data-choice=left]').click()
        assert 'Attribution remains hidden' in page.locator('#status').inner_text()
        page.locator('#reveal').click();assert page.locator('#assessment').is_visible()
        assert any('Original' in x for x in page.locator('#comparison h3').all_text_contents())
        with page.expect_download() as download:page.locator('#exportChoices').click()
        exported=json.loads(Path(download.value.path()).read_text());assert exported['reviews']['bank-code-390/light/calibrated']['choice']=='left'
        page.reload();assert 'Saved preference:' in page.locator('#status').inner_text()
        checks.append('Blind labels and assessments hidden; both random orders; reveal; preference persistence; valid JSON export')
        page.locator('#diagramMode').select_option('matched')
        with page.expect_download() as download:page.locator('#exportSettings').click()
        settings=json.loads(Path(download.value.path()).read_text());assert settings['squircleRadius']>settings['roundRadius']
        checks.append('Geometry diagram mode and settings JSON export')
        page.locator('#comparison img').first.click();assert page.locator('#zoom').is_visible();page.keyboard.press('Escape');assert not page.locator('#zoom').is_visible()
        checks.append('Keyboard/image zoom and Escape')
        # Check all relative link targets, excluding fragments.
        hrefs=page.locator('a[href]').evaluate_all('(es)=>es.map(e=>e.getAttribute("href"))')
        for href in hrefs:
            if href.startswith(('https:','http:','#')): continue
            parsed=urlparse(href)
            path=Path(unquote(parsed.path)) if parsed.scheme=='file' else STUDY/unquote(parsed.path)
            assert path.resolve().exists(),href
        checks.append('Local evidence and prototype links resolve')
        for width in (1440,1280,390):
            page.set_viewport_size(dict(width=width,height=1000 if width>400 else 844))
            for appearance in ('light','dark'):
                page.locator('#appearance').select_option(appearance)
                page.evaluate('scrollTo(0,0)')
                assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
                page.screenshot(path=str(QA/f'report-{width}-{appearance}.png'),full_page=True)
        checks.append('No horizontal overflow at 1440, 1280 and 390 in both report themes')
        page.set_viewport_size(dict(width=1440,height=1000));page.locator('#appearance').select_option('light')
        for id in ('bank-code-390','menu-oncall','bank-help-390','dashboard-tv-live'):
            page.locator('#case').select_option(id)
            for theme in ('light','dark'):
                page.locator('#shotTheme').select_option(theme)
                for detail in (False,True):
                    page.locator('#detail').set_checked(detail)
                    page.locator('#comparison').screenshot(path=str(QA/f'{id}-{theme}-{detail}.png'))
        assert not network and not errors,(network,errors)
        checks.append('No console errors or network requests')
        browser.close()
    report=dict(passed=True,primaryImages=len(catalog),captures=80,protectedFilesUnchanged=True,checks=checks,qaScreenshots=str(QA))
    (STUDY/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
if __name__=='__main__':main()
