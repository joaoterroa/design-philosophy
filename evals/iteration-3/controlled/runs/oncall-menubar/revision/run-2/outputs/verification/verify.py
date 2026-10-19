from pathlib import Path
import json
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'outputs/verification'
URL=(ROOT/'outputs/app/index.html').as_uri()
results={'screens':[], 'interactions':[], 'errors':[]}
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True)
 page=browser.new_page(viewport={'width':400,'height':680},device_scale_factor=2)
 page.on('pageerror',lambda e:results['errors'].append(str(e)))
 page.on('console',lambda m: results['errors'].append(m.text) if m.type=='error' else None)
 external=[]
 page.on('request', lambda r: external.append(r.url) if not r.url.startswith('file:') else None)
 for theme in ['light','dark']:
  for display in ['laptop','tv']:
   for state in ['main','compose','pending','offline','empty','accepted']:
    page.goto(URL+f'?screen={state}&theme={theme}&display={display}')
    page.wait_for_selector('h1')
    geometry=page.locator('#app').evaluate('(el)=>{const r=el.getBoundingClientRect();return {x:r.x,y:r.y,width:r.width,height:r.height,overflow:el.scrollHeight>el.clientHeight,horizontal:el.scrollWidth>el.clientWidth}}')
    assert geometry['x']==20 and geometry['y']==20 and geometry['width']==360 and geometry['height']<=640, (state,geometry)
    assert not geometry['horizontal'],(state,geometry)
    assert not geometry['overflow'],(state,geometry)
    results['screens'].append({'state':state,'theme':theme,'display':display,**geometry})
    if display=='laptop' and (state=='main' or (theme=='dark' and state=='pending') or (theme=='light' and state=='compose')):
     page.screenshot(path=str(OUT/f'{state}-{theme}.png'))
 # Full keyboard path
 page.goto(URL+'?screen=main&theme=light')
 page.keyboard.press('Tab'); assert page.locator(':focus').inner_text().startswith('Hand over shift')
 page.keyboard.press('Enter'); assert page.get_by_role('heading',name='Who’s taking over?').is_visible()
 page.get_by_label('Hand over to').focus()
 page.keyboard.press('p')
 assert page.get_by_label('Hand over to').input_value()=='Priya Raman'
 page.keyboard.press('Tab'); page.keyboard.type('Watch the routing queue.')
 page.keyboard.press('Tab');page.keyboard.press('Enter')
 assert page.get_by_role('heading',name='Ready to hand over?').is_visible()
 assert page.locator('.note-display').inner_text()=='Watch the routing queue.'
 page.keyboard.press('Tab'); assert page.locator(':focus').get_attribute('aria-label')=='Handover note'
 page.keyboard.press('Tab'); assert page.locator(':focus').inner_text()=='Edit'
 page.keyboard.press('Enter')
 assert page.get_by_label('Handover note').input_value()=='Watch the routing queue.'
 page.keyboard.press('Tab');page.keyboard.press('Tab');page.keyboard.press('Enter')
 page.keyboard.press('Tab');page.keyboard.press('Tab');page.keyboard.press('Tab')
 assert page.locator(':focus').inner_text()=='Send request'
 assert page.locator(':focus').evaluate('(e)=>getComputedStyle(e).outlineWidth')=='3px'
 page.keyboard.press('Enter')
 assert page.get_by_role('heading',name='Waiting for Priya').is_visible()
 assert page.get_by_text('You’re still responsible.',exact=True).is_visible()
 page.wait_for_timeout(800)
 assert page.get_by_role('heading',name='Waiting for Priya').is_visible()
 page.get_by_role('button',name='Back to schedule').click()
 assert page.get_by_role('button',name='View handover request').is_visible()
 page.reload();assert page.get_by_role('button',name='View handover request').is_visible()
 page.get_by_role('button',name='View handover request').click()
 page.get_by_role('button',name='Cancel request',exact=True).click()
 assert page.get_by_role('button',name='Hand over shift').is_visible()
 results['interactions'].append('Full keyboard choose → note → review → edit → send; pending remains; main/reload preserves pending; cancel request restores ownership')
 page.get_by_role('button',name='Hand over shift').click();page.keyboard.press('Escape')
 assert page.get_by_role('heading',name='You’re on call').is_visible()
 results['interactions'].append('Escape returns from compose')
 page.goto(URL+'?screen=offline&theme=dark')
 page.get_by_role('button',name='Try again').click();assert page.get_by_text('Still offline. Showing the saved schedule. Handovers are unavailable.').is_visible()
 assert page.locator(':focus').inner_text()=='Try again'
 page.goto(URL+'?screen=empty');page.get_by_role('button',name='Refresh schedule').click()
 assert page.get_by_text('No schedule is available yet.').is_visible()
 results['interactions'].append('Offline retry and empty refresh stay honest; retry retains focus')
 page.goto((ROOT/'outputs/review.html').as_uri())
 frame=page.frame_locator('#preview')
 assert frame.get_by_role('heading',name='Waiting for Priya').is_visible()
 page.get_by_role('button',name='Simulate Priya accepting').click()
 frame.get_by_role('heading',name='Shift handed over').wait_for()
 frame.get_by_role('button',name='Back to schedule').click()
 frame.get_by_role('heading',name='Priya is on call').wait_for()
 results['interactions'].append('Explicit harness acceptance → accepted → main shows Priya responsible')
 page.goto(URL+'?screen=main');page.emulate_media(color_scheme='dark',reduced_motion='reduce');page.reload()
 assert page.locator('html').get_attribute('data-theme')=='dark'
 assert page.locator('button').first.evaluate('(el)=>getComputedStyle(el).transitionDuration')=='0s'
 results['interactions'].append('System dark preference and reduced motion honored')
 page.emulate_media(color_scheme='light',reduced_motion='reduce');page.goto(URL+'?screen=main&theme=dark')
 assert page.locator('html').get_attribute('data-theme')=='dark'
 # Native semantics snapshot useful for manual inspection, not a screen reader claim.
 (OUT/'accessibility-main.txt').write_text(page.locator('#app').aria_snapshot())
 assert external==[],external
 results['external_requests']=external
 browser.close()
(OUT/'results.json').write_text(json.dumps(results,indent=2))
print(json.dumps({'state_renders':len(results['screens']),'interactions':results['interactions'],'console_errors':results['errors'],'network_requests':external},indent=2))
assert not results['errors']
