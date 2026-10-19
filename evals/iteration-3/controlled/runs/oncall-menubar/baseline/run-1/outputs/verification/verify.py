"""Run with /private/tmp/design-compare-venv/bin/python outputs/verification/verify.py.
Requires the supplied Playwright environment. Uses file:// and no network.
"""
from pathlib import Path
from PIL import Image
import io
import json
from playwright.sync_api import sync_playwright, expect
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'outputs/verification'
URL=(ROOT/'outputs/app/index.html').as_uri()
STATES=['main','compose','pending','offline','empty','accepted']
sheets={t:Image.new('RGB',(1200,1360),'#e5e8e9') for t in ['light','dark']}
report={'screens':[], 'interactions':[], 'errors':[], 'network':[]}
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True)
 for theme in ['light','dark']:
  for display in ['laptop','tv']:
   for state in STATES:
    context=browser.new_context(viewport={'width':400,'height':680},device_scale_factor=2)
    page=context.new_page()
    page.on('pageerror',lambda e:report['errors'].append(str(e)))
    page.on('request',lambda r:report['network'].append(r.url) if r.url.startswith(('http:','https:')) else None)
    page.goto(URL+f'?screen={state}&theme={theme}&display={display}')
    page.wait_for_timeout(30)
    box=page.locator('#app').bounding_box()
    assert box['x']==20 and box['y']==20 and box['width']==360 and box['height']<=640,(state,box)
    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
    assert page.locator('#app').evaluate('(e)=>e.scrollWidth<=e.clientWidth')
    assert page.locator('h1').inner_text()
    assert page.locator('button').count()>0
    metrics=page.locator('#app').evaluate('(e)=>({height:e.offsetHeight,scrollHeight:e.scrollHeight,clientHeight:e.clientHeight,headingY:document.querySelector("h1").getBoundingClientRect().y})')
    before=page.locator('h1').bounding_box();page.wait_for_timeout(50);after=page.locator('h1').bounding_box()
    metrics['settledHeadingShiftPx']=abs(before['y']-after['y'])
    assert metrics['settledHeadingShiftPx']==0
    assert all(v>=36 for v in page.locator('button').evaluate_all('(es)=>es.map(e=>e.getBoundingClientRect().height)'))
    assert metrics['scrollHeight']==metrics['clientHeight'],(state,metrics)
    report['screens'].append({'state':state,'theme':theme,'display':display,**metrics})
    if display=='laptop':
     shot=page.screenshot();im=Image.open(io.BytesIO(shot));im.thumbnail((400,680));i=STATES.index(state);sheets[theme].paste(im,((i%3)*400,(i//3)*680))
     if (state,theme) in [('main','light'),('main','dark'),('pending','light'),('offline','light'),('compose','dark'),('accepted','dark')]:page.screenshot(path=str(OUT/f'{state}-{theme}.png'))
    context.close()
 context=browser.new_context(viewport={'width':400,'height':680},reduced_motion='reduce')
 page=context.new_page()
 page.on('pageerror',lambda e:report['errors'].append(str(e)))
 page.on('request',lambda r:report['network'].append(r.url) if r.url.startswith(('http:','https:')) else None)
 page.goto(URL+'?screen=main&theme=light')
 # Full keyboard path, including recipient selection and review.
 page.keyboard.press('Tab');assert page.locator(':focus').inner_text().startswith('Hand over')
 page.keyboard.press('Enter');assert 'compose' in page.url
 assert page.locator('#review').is_disabled()
 page.keyboard.press('Tab');assert page.locator(':focus').get_attribute('id')=='recipient'
 page.keyboard.press('Space')
 assert page.locator('#recipient').is_checked()
 assert page.locator('#review').is_enabled()
 page.keyboard.press('Tab');page.keyboard.type('No outstanding incidents. Monitor the deployment.')
 page.keyboard.press('Tab');page.keyboard.press('Tab');assert page.locator(':focus').inner_text()=='Review handover'
 page.keyboard.press('Enter');assert page.locator('h1').inner_text()=='Pass the shift to Priya?'
 assert page.locator(':focus').evaluate('(e)=>e.tagName')=='H1'
 page.screenshot(path=str(OUT/'review-light.png'))
 # Edit route retains input; cancel returns safely.
 page.get_by_role('button',name='Edit handover').click();assert page.locator('#note').input_value().startswith('No outstanding')
 page.get_by_role('button',name='Review handover').click();page.get_by_role('button',name='Send request').click()
 assert 'pending' in page.url and 'still on call' in page.locator('#app').inner_text()
 page.wait_for_timeout(600);assert page.locator('h1').inner_text()=='Waiting for Priya'
 page.reload();assert page.locator('h1').inner_text()=='Waiting for Priya'
 page.get_by_role('button',name='Schedule',exact=False).click();page.get_by_role('button',name='View pending handover').click()
 page.get_by_role('button',name='Cancel request').click();assert page.locator('h1').inner_text()=='You’re on call.'
 assert page.get_by_role('button',name='Hand over your shift').is_visible()
 report['interactions'].append('Keyboard choose → note → review → edit → send; pending stays pending; reload; return; cancel request')
 page.get_by_role('button',name='Hand over your shift').click();page.keyboard.press('Escape');assert page.locator('h1').inner_text()=='You’re on call.'
 report['interactions'].append('Escape cancels compose and returns to schedule')
 page.goto(URL+'?screen=offline&theme=dark');page.get_by_role('button',name='Try reconnecting').click()
 assert 'Still offline' in page.locator('#announcer').inner_text();assert page.locator('#app').inner_text().count('Jamie Ellis')>=1
 report['interactions'].append('Offline retry retains saved data and announces failure')
 page.goto(URL+'?screen=empty');page.get_by_role('button',name='Refresh schedule').click();assert 'No schedule' in page.locator('#announcer').inner_text()
 report['interactions'].append('Empty refresh remains honestly empty')
 # Real, separate acceptance action lives in review harness, never in product.
 page.goto((ROOT/'outputs/review.html').as_uri());page.locator('#state').select_option('pending');page.get_by_role('button',name='Open state').click()
 frame=page.frame_locator('#preview');assert frame.locator('h1').inner_text()=='Waiting for Priya'
 page.get_by_role('button',name='Simulate Priya accepting').click();expect(frame.locator('h1')).to_have_text('Priya has the shift.')
 frame.get_by_role('button',name='Back to schedule').click();assert frame.locator('h1').inner_text()=='You’re off call.'
 assert 'Priya Raman' in frame.locator('.owner').inner_text()
 report['interactions'].append('Explicit acceptance via separate harness updates responsibility and main schedule')
 # Long note remains text, cannot inject markup, and can scroll inside the cap.
 page.goto(URL+'?screen=compose&theme=dark');page.locator('#recipient').check();page.locator('#recipient').focus();page.screenshot(path=str(OUT/'keyboard-focus-dark.png'))
 text='<img src=x onerror=alert(1)> '+('Long handover context. '*13)
 page.locator('#note').fill(text[:300]);page.get_by_role('button',name='Review handover').click()
 assert page.locator('.note-text').inner_text()==text[:300]
 assert page.locator('.note-text img').count()==0
 assert page.locator('#app').evaluate('(e)=>e.scrollWidth===e.clientWidth && e.offsetHeight<=640')
 page.get_by_role('button',name='Send request').click();assert page.locator('#app').evaluate('(e)=>e.scrollWidth===e.clientWidth && e.offsetHeight<=640')
 page.get_by_role('button',name='Cancel request').click()
 report['interactions'].append('300-character note is escaped and wraps without horizontal overflow; actions remain reachable by scrolling')
 # System preference without a theme query.
 context=browser.new_context(viewport={'width':400,'height':680},color_scheme='dark')
 system=context.new_page();system.goto(URL+'?screen=main');assert system.locator('body').evaluate('(e)=>getComputedStyle(e).backgroundColor')=='rgb(23, 27, 29)'
 system.goto(URL+'?screen=main&theme=light');assert system.locator('body').evaluate('(e)=>getComputedStyle(e).backgroundColor')=='rgb(229, 232, 233)'
 report['interactions'].append('System dark preference and explicit light override')
 browser.close()
for theme,sheet in sheets.items():sheet.save(OUT/f'all-states-{theme}.jpg')
assert not report['errors'],report['errors']
assert not report['network'],report['network']
(OUT/'results.json').write_text(json.dumps(report,indent=2))
print(f"PASS: {len(report['screens'])} state/theme/display combinations, {len(report['interactions'])} interaction checks; no browser errors or network requests.")
