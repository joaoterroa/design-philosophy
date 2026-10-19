from pathlib import Path
from playwright.sync_api import sync_playwright
import json
ROOT=Path(__file__).resolve().parents[1]
URL=(ROOT/'app/index.html').as_uri()
results=[]
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True)
 page=browser.new_page(viewport={'width':400,'height':680},device_scale_factor=2)
 errors=[]
 external=[]
 page.on('request',lambda r: external.append(r.url) if r.url.startswith(('http:','https:')) else None)
 page.on('pageerror',lambda e:errors.append(str(e)))
 for theme in ['light','dark']:
  for display in ['laptop','tv']:
   for state in ['main','compose','pending','offline','empty','accepted']:
    page.goto(f'{URL}?screen={state}&theme={theme}&display={display}')
    page.wait_for_selector('#app h1, #app h2')
    metrics=page.evaluate('''() => {const a=document.querySelector('#app'), r=a.getBoundingClientRect();return {x:r.x,y:r.y,width:r.width,height:r.height,scroll:a.scrollHeight,client:a.clientHeight,bodyWidth:document.body.scrollWidth,overflow:[...a.querySelectorAll('*')].filter(e=>e.getBoundingClientRect().right>r.right+1).map(e=>e.tagName)}}''')
    
    assert metrics['x']==20 and metrics['y']==20 and metrics['width']==360,metrics
    assert metrics['height']<=640 and metrics['bodyWidth']<=400,metrics
    assert metrics['scroll']<=metrics['client']+1,metrics
    assert not metrics['overflow'],metrics
    targets=page.locator('button,select,textarea').evaluate_all('(es)=>es.map(e=>({tag:e.tagName,height:e.getBoundingClientRect().height}))')
    assert all(e['height']>=36 for e in targets),targets
    results.append({'screen':state,'theme':theme,'display':display,**metrics})
    if display=='laptop':page.screenshot(path=str(ROOT/'verification'/f'{state}-{theme}.png'))
 # keyboard-only main path
 page.goto(f'{URL}?screen=main&theme=light')
 page.keyboard.press('Tab');assert page.get_by_role('button',name='Hand over shift').evaluate('(e)=>document.activeElement===e')
 assert page.get_by_role('button',name='Hand over shift').evaluate('(e)=>getComputedStyle(e).outlineStyle')=='solid'
 page.keyboard.press('Enter');assert page.get_by_role('heading',name='Hand over your shift').evaluate('(e)=>document.activeElement===e')
 page.keyboard.press('Tab')
 assert page.locator('#recipient').evaluate('(e)=>document.activeElement===e')
 page.keyboard.press('p')
 assert page.locator('#recipient').input_value()=='Priya Raman'
 page.keyboard.press('Tab');page.keyboard.type('No open incidents. Watch the deploy at noon.')
 page.keyboard.press('Tab');page.keyboard.press('Enter')
 assert page.get_by_role('heading',name='Review handover').is_visible()
 assert page.get_by_text('No open incidents. Watch the deploy at noon.').is_visible()
 page.screenshot(path=str(ROOT/'verification/review-light.png'))
 page.keyboard.press('Tab');page.keyboard.press('Enter')
 assert page.get_by_role('heading',name='Awaiting Priya').is_visible()
 assert page.get_by_text('You’re still on call.',exact=True).is_visible()
 page.wait_for_timeout(500)
 assert 'screen=pending' in page.url
 page.get_by_role('button',name='On-call schedule').click()
 page.reload()
 assert page.get_by_role('button',name='View pending handover').is_visible()
 page.get_by_role('button',name='View pending handover').click()
 page.get_by_role('button',name='Cancel request').click()
 assert page.get_by_text('Request cancelled. You’re still on call.').is_visible()
 # cancel + Escape
 page.get_by_role('button',name='Hand over shift').click();page.keyboard.press('Escape')
 assert page.get_by_role('heading',name='On call now').is_visible()
 # Harness explicit simulated acceptance
 page.goto((ROOT/'review.html').as_uri())
 frame=page.frame_locator('#prototype')
 frame.get_by_role('button',name='Hand over shift').click()
 frame.locator('#recipient').select_option('Priya Raman')
 frame.get_by_role('button',name='Review handover').click()
 frame.get_by_role('button',name='Send handover request').click()
 page.get_by_role('button',name='Simulate Priya accepting').click()
 frame.get_by_role('heading',name='Handover accepted').wait_for(state='visible')
 frame.get_by_role('button',name='Back to schedule').click()
 assert frame.get_by_role('heading',name='Priya Raman').is_visible()
 assert frame.get_by_text('You’re off call').is_visible()
 # Offline and empty controls are honest
 page.goto(f'{URL}?screen=offline&theme=dark')
 assert page.get_by_role('button',name='Hand over shift').is_disabled()
 page.get_by_role('button',name='Try again').click()
 assert page.get_by_text('Still offline. Your saved schedule is unchanged.').is_visible()
 page.goto(f'{URL}?screen=empty')
 page.get_by_role('button',name='Refresh schedule').click()
 assert page.get_by_text('No schedule is available in this offline prototype.').is_visible()
 # system preference and reduced motion
 page.emulate_media(color_scheme='dark',reduced_motion='reduce')
 page.goto(f'{URL}?screen=compose')
 assert page.locator('html').get_attribute('data-theme')=='dark'
 assert page.locator('button').first.evaluate('(e)=>getComputedStyle(e).transitionDuration')=='0s'
 page.emulate_media(color_scheme='light')
 page.wait_for_function("document.documentElement.dataset.theme==='light'")
 assert not errors,errors
 assert not external,external
 browser.close()
(ROOT/'verification/results.json').write_text(json.dumps({'screens':results,'page_errors':errors,'external_requests':external,'interaction_checks':'passed','system_theme':'passed','reduced_motion':'passed'},indent=2))
print(f'PASS: {len(results)} direct URL variants, keyboard flow, cancel, pending, explicit acceptance, offline, empty, themes and reduced motion.')
