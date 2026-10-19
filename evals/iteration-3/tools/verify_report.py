#!/usr/bin/env python3
from study_paths import artifact_path
"""Verify offline comparison controls, geometry, links, exports and protected sources."""
from pathlib import Path
from hashlib import sha256
from urllib.parse import urlparse,unquote
import json,subprocess,argparse
from PIL import Image,ImageStat
from playwright.sync_api import sync_playwright
STUDY=Path(__file__).resolve().parents[1];ROOT=STUDY.parents[1]
QA=Path('/private/tmp/iteration-3-qa')

def main():
    proto=json.loads((STUDY/'protocol.json').read_text());count=0;incomplete=[]
    for record in proto['runs']:
        a=artifact_path(record, STUDY);p=a/'capture.json'
        if not p.exists():incomplete.append(record['id']);continue
        cap=json.loads(p.read_text())
        for shot in cap['shots']:
            if not shot.get('captureSucceeded'):continue
            path=a/shot['path'];assert sha256(path.read_bytes()).hexdigest()==shot['sha256']
            with Image.open(path) as im:
                assert list(im.size)==shot['dimensions'];assert max(ImageStat.Stat(im.convert('RGB')).var)>=1
            count+=1
        if not cap.get('complete'):incomplete.append(record['id'])
        assert cap.get('sourceUnchanged',True)
    expected=proto['design']['finalScreenshotsExpected']
    assert count==expected and not incomplete, {'captured':count,'expected':expected,'incompleteRuns':incomplete}
    for file,h in proto['skillHashes']['baseline'].items():
        assert sha256((ROOT/file).read_bytes()).hexdigest()==h,'Canonical source changed: '+file
        assert sha256((STUDY/'skills/baseline'/file).read_bytes()).hexdigest()==h
    for file,h in proto['skillHashes']['revision'].items():assert sha256((STUDY/'skills/revision'/file).read_bytes()).hexdigest()==h
    assert not subprocess.check_output(['git','diff','--name-only','--','SKILL.md','references','templates'],cwd=ROOT,text=True)
    QA.mkdir(exist_ok=True)
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True);context=browser.new_context(viewport=dict(width=1440,height=1000),accept_downloads=True)
        network=[];errors=[]
        def offline(route):
            if route.request.url.startswith(('http:','https:')):network.append(route.request.url);route.abort()
            else:route.continue_()
        context.route('**/*',offline);page=context.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
        page.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
        page.goto((STUDY/'index.html').as_uri(),wait_until='load')
        assert page.locator('.pair').count()==6
        assert page.locator('#overall-assessment').is_hidden()
        assert all('Current skill' not in t and 'Experimental revision' not in t for t in page.locator('.side-label').all_text_contents())
        available=page.locator('.pair').filter(has=page.locator('.shot-button'))
        scales=[]
        if available.count():
            pairids=available.evaluate_all('(es)=>es.map(e=>e.id)')
            for theme in ('light','dark'):
                page.locator('#shot-theme').select_option(theme)
                for pairid in pairids:
                    pair=page.locator('#'+pairid)
                    values=pair.locator('.state-select option').evaluate_all('(es)=>es.map(e=>e.value)')
                    for value in values:
                        pair.locator('.state-select').select_option(value);pair=page.locator('#'+pairid)
                        sizes=pair.locator('.display-select option').evaluate_all('(es)=>es.map(e=>e.value)')
                        for size in sizes:
                            pair.locator('.display-select').select_option(size);pair=page.locator('#'+pairid)
                            pair.locator('img').evaluate_all('(es)=>Promise.all(es.map(e=>e.decode()))')
                            data=pair.locator('.shot-button img').evaluate_all('(es)=>es.map(e=>({ratio:e.getBoundingClientRect().width/e.naturalWidth}))')
                            assert len(data)==2 and abs(data[0]['ratio']-data[1]['ratio'])<.002,data
                            scales.append(data)
            pair=available.first;pairid=pair.get_attribute('id')
            pair.locator('.vote[data-choice=left]').click();pair=page.locator('#'+pairid)
            assert 'Saved for' in pair.locator('.vote-status').inner_text()
            pair.locator('.reveal').click();pair=page.locator('#'+pairid)
            assert any('Current skill' in t or 'Experimental revision' in t for t in pair.locator('.side-label').all_text_contents())
            pair.locator('.shot-button').first.click();assert page.locator('#zoom').is_visible();page.keyboard.press('Escape');assert not page.locator('#zoom').is_visible()
            with page.expect_download() as download:page.locator('#export').click()
            exported=json.loads(Path(download.value.path()).read_text());assert exported['choices'] and exported['choices'][-1]['choice']=='left'
            page.reload();assert any('Saved for' in t for t in page.locator('.vote-status').all_text_contents())
        else:
            with page.expect_download() as download:page.locator('#export').click()
            exported=json.loads(Path(download.value.path()).read_text());assert exported['choices']==[]
        page.locator('#blind').uncheck();assert page.locator('#overall-assessment').is_visible()
        for href in page.locator('a[href]').evaluate_all('(es)=>es.map(e=>e.href)'):
            parsed=urlparse(href)
            if parsed.scheme=='file':assert Path(unquote(parsed.path)).is_file(),href
        page.locator('#blind').check()
        # Independent browser contexts have independent random orders, without using saved choices.
        observed=set()
        for _ in range(16):
            c=browser.new_context();q=c.new_page();q.goto((STUDY/'index.html').as_uri());saved=q.evaluate("JSON.parse(localStorage.getItem(Object.keys(localStorage).find(k=>k.endsWith('-review-v1')))).orders")
            observed.add(tuple(saved[next(iter(saved))]));c.close()
        assert len(observed)==2,'Both random orders should occur across fresh contexts'
        for width in (1440,1280,390):
            page.set_viewport_size(dict(width=width,height=1000 if width>400 else 844))
            for theme in ('light','dark'):
                page.locator('#page-theme').select_option(theme);page.evaluate('scrollTo(0,0)')
                assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),(width,theme)
                page.screenshot(path=str(QA/f'page-{width}-{theme}.png'),full_page=True)
        assert not errors and not network,(errors,network)
        browser.close()
    report=dict(passed=True,finalPNGs=count,expectedPNGs=192,incompleteRuns=incomplete,checks=['PNG hashes, dimensions and nonuniform pixels','frozen skill snapshots and canonical files unchanged','offline page no console/network errors','six comparison pairs','equal source-pixel scale across all96 paired state/size/theme combinations','blind/reveal/random order','preference persistence and JSON export','image zoom and Escape','no horizontal overflow at1440/1280/390 in both themes'],qa=str(QA))
    (STUDY/'verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--study',type=Path,default=STUDY);args=parser.parse_args();STUDY=args.study.resolve();QA=Path('/private/tmp/iteration-3-controlled-qa') if STUDY.name=='controlled' else QA;main()
