#!/usr/bin/env python3
"""Build isolated corner probes and capture a 2 × 2 radius/curve experiment offline."""
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import shutil
from PIL import Image, ImageChops, ImageStat
from playwright.sync_api import sync_playwright

STUDY = Path(__file__).resolve().parents[1]
REPO = STUDY.parents[2]
FACTOR = (1 - 2**(-.5)) / (1 - 2**(-.25))
VARIANTS = {
    'original': (1, 'round'),
    'curve-only': (1, 'squircle'),
    'radius-only': (FACTOR, 'round'),
    'calibrated': (FACTOR, 'squircle'),
}
TARGETS = {
    'oncall-menubar': {'.popover': [12]*4},
    'banking-onboarding': {'.btn, .barbtn': [12]*4, 'input, .togglebtn': [10]*4,
        '.preview, .panel': [16]*4, '.message': [16,16,16,10], '.sheet': [20,20,0,0]},
    'incident-dashboard': {'.sev, .bar, .meter': [2]*4},
}
CASES = [
    ('menu-oncall','oncall-menubar',1100,800,'?state=oncall&theme={theme}','#popover'),
    ('menu-compose','oncall-menubar',1100,800,'?state=compose&theme={theme}','#popover'),
    ('menu-pending','oncall-menubar',1100,800,'?state=pending&theme={theme}','#popover'),
    ('bank-code-390','banking-onboarding',390,844,'?theme={theme}#code',None),
    ('bank-code-320','banking-onboarding',320,568,'?theme={theme}#code',None),
    ('bank-error-390','banking-onboarding',390,844,'?theme={theme}#code-wrong',None),
    ('bank-help-390','banking-onboarding',390,844,'?theme={theme}#code',None),
    ('dashboard-tv-live','incident-dashboard',1920,1080,'?display=wall&state=live&theme={theme}&frozen',None),
    ('dashboard-tv-surge','incident-dashboard',1920,1080,'?display=wall&state=surge&theme={theme}&frozen',None),
    ('dashboard-laptop','incident-dashboard',1440,900,'?display=desk&state=live&theme={theme}&frozen',None),
]
MEASURE = r'''() => {
 const root=document.querySelector('#popover')||document.querySelector('.app')||document.body;
 const rect=e=>{const r=e.getBoundingClientRect();return [r.x,r.y,r.width,r.height].map(v=>Math.round(v*1000)/1000)};
 const shown=e=>e.getClientRects().length && getComputedStyle(e).visibility!=='hidden';
 const items=[root,...root.querySelectorAll('*')].filter(shown);
 return {text:root.innerText, boxes:items.map(e=>({tag:e.tagName,cls:e.className?.baseVal??e.className,rect:rect(e)})),
   horizontalOverflow:document.documentElement.scrollWidth>innerWidth,
   targets:[...root.querySelectorAll('button,input')].filter(shown).map(e=>({label:e.textContent||e.name,rect:rect(e),focus: getComputedStyle(e).outlineStyle})),
   corners:[...document.querySelectorAll('.popover,.btn,.barbtn,input,.message,.preview,.sheet,.sev,.bar,.meter')].filter(shown).map(e=>({tag:e.tagName,cls:e.className,rect:rect(e),radius:getComputedStyle(e).borderTopLeftRadius,curve:getComputedStyle(e).cornerTopLeftShape})),
   incidents:[...document.querySelectorAll('#open-list > li')].filter(shown).length,
   more:document.querySelector('#more:not([hidden])')?.textContent||''};
}'''

def digest(path): return sha256(path.read_bytes()).hexdigest()

def build():
    manifests=[]
    for evaluation,targets in TARGETS.items():
        source=REPO/f'evals/iteration-1/{evaluation}/with_skill/outputs/app'
        hashes={p.relative_to(source).as_posix():digest(p) for p in source.rglob('*') if p.is_file()}
        for variant,(factor,curve) in VARIANTS.items():
            if variant=='original': continue
            dest=STUDY/f'experiments/{evaluation}/{variant}/app'
            if dest.exists(): shutil.rmtree(dest)
            shutil.copytree(source,dest)
            css='/* Corner-only research probe. Not a production style system or a Dia reconstruction. */\n'
            for selector,radii in targets.items():
                values=' '.join(f'{r*factor:.6f}px' for r in radii)
                css+=f'{selector} {{ border-radius: {values}; corner-shape: {curve}; }}\n'
            # Preserve the semantic open end of timeline segments.
            if evaluation=='incident-dashboard':
                css+='.bar.is-clipped {border-top-left-radius:0; border-bottom-left-radius:0;}\n'
            (dest/'shape.css').write_text(css)
            index=(dest/'index.html').read_text().replace('</head>','<link rel="stylesheet" href="shape.css">\n</head>')
            (dest/'index.html').write_text(index)
            for name,h in hashes.items():
                if name!='index.html': assert digest(dest/name)==h
        manifests.append(dict(evaluation=evaluation,source=source.relative_to(REPO).as_posix(),sourceHashes=hashes,targets=targets))
    (STUDY/'experiments/manifest.json').write_text(json.dumps(dict(factor=FACTOR,variants=VARIANTS,sources=manifests),indent=2)+'\n')


def run():
    build()
    results=[]
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True)
        for case,evaluation,width,height,suffix,crop in CASES:
            for theme in ('light','dark'):
                records=[]
                for variant in VARIANTS:
                    index=(REPO/f'evals/iteration-1/{evaluation}/with_skill/outputs/app/index.html' if variant=='original'
                        else STUDY/f'experiments/{evaluation}/{variant}/app/index.html')
                    context=browser.new_context(viewport=dict(width=width,height=height),device_scale_factor=1,
                        color_scheme=theme,reduced_motion='reduce',locale='en-GB',timezone_id='Europe/London',service_workers='block')
                    errors=[]; network=[]
                    def offline(route):
                        if route.request.url.startswith(('http:','https:')):
                            network.append(route.request.url); route.abort()
                        else: route.continue_()
                    context.route('**/*',offline)
                    page=context.new_page()
                    page.on('pageerror',lambda e: errors.append(str(e)))
                    page.on('console',lambda m: errors.append(m.text) if m.type=='error' else None)
                    assert page.evaluate("CSS.supports('corner-shape','squircle')"),'This experiment needs Chromium with corner-shape support.'
                    now=datetime(2026,10,18,10,tzinfo=timezone.utc)
                    page.clock.install(time=now); page.clock.pause_at(now)
                    page.goto(index.as_uri()+suffix.format(theme=theme),wait_until='load')
                    page.clock.run_for(1500); page.evaluate('document.fonts.ready')
                    if case=='bank-help-390':
                        page.locator('#help-open').click(); page.clock.run_for(500)
                    page.evaluate('scrollTo(0,0)'); page.mouse.move(width-1,height-1)
                    metrics=page.evaluate(MEASURE)
                    assert not errors and not network,(case,variant,errors,network)
                    assert not metrics['horizontalOverflow']
                    file=f'figures/{case}__{theme}__{variant}.png'
                    (page.locator(crop) if crop else page).screenshot(path=str(STUDY/file),animations='disabled',caret='hide')
                    with Image.open(STUDY/file) as im:
                        assert max(ImageStat.Stat(im.convert('RGB')).var)>1
                        pixels=list(im.size)
                    if records:
                        assert metrics['boxes']==records[0]['metrics']['boxes'],f'Layout changed: {case}/{variant}'
                        assert metrics['text']==records[0]['metrics']['text'],f'Content changed: {case}/{variant}'
                        with Image.open(STUDY/records[0]['file']) as original, Image.open(STUDY/file) as revision:
                            diff=ImageChops.difference(original.convert('RGB'),revision.convert('RGB'))
                            significant=diff.convert('L').point(lambda x:255 if x>8 else 0)
                            count=significant.histogram()[255]
                            changed=round(count/(pixels[0]*pixels[1])*100,5)
                    else: changed=0
                    records.append(dict(variant=variant,file=file,pixels=pixels,sha256=digest(STUDY/file),changedPercent=changed,metrics=metrics))
                    context.close()
                results.append(dict(id=case,evaluation=evaluation,theme=theme,viewport=[width,height],records=records))
                print(case,theme,'verified',flush=True)
        # Check real interaction and visible focus, using the strongest shape intervention.
        for evaluation in ('oncall-menubar','banking-onboarding'):
            page=browser.new_page(viewport=dict(width=1100 if evaluation=='oncall-menubar' else 390,height=844))
            index=STUDY/f'experiments/{evaluation}/calibrated/app/index.html'
            page.goto(index.as_uri()+ ('?state=oncall&theme=light' if evaluation=='oncall-menubar' else '?theme=light#code'))
            if evaluation=='oncall-menubar':
                page.locator('[data-act=handover]').click(); page.locator('input[name=to][value=pr]').check(force=True)
                page.locator('[data-act=send]').click(); assert 'until Priya accepts' in page.locator('#popover').inner_text()
                assert page.evaluate('rota.state.onCall')
            else:
                page.locator('#otp').fill('000000'); page.locator('#code-form button[type=submit]').click()
                assert page.locator('#code-error').is_visible()
                page.locator('#otp').fill('482913'); page.locator('#code-form button[type=submit]').click()
                assert page.locator('[data-screen=passcode]').is_visible()
                page.locator('#help-open').click(); assert page.locator('#help').is_visible()
                page.keyboard.press('Escape'); assert not page.locator('#help').is_visible()
                page.locator('input:visible').first.focus(); page.keyboard.press('Tab')
                assert page.evaluate("getComputedStyle(document.activeElement).outlineStyle != 'none'")
            page.close()
        report=dict(browser=browser.version,records=results,checks=['all visible element bounding boxes identical','content identical','offline','nonuniform PNGs','no console errors','menu handover','banking code/error/help','banking keyboard focus'])
        browser.close()
    (STUDY/'experiments/results.json').write_text(json.dumps(report,indent=2)+'\n')
    print(f'PASS: {len(results)*4} screenshots; geometry changed without layout/content changes.')

if __name__=='__main__': run()
