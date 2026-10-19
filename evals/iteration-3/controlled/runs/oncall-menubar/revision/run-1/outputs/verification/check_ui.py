from pathlib import Path
from playwright.sync_api import sync_playwright
import json
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'outputs'
url=(OUT/'app/index.html').as_uri()
results={'states':[], 'interactions':[], 'errors':[]}
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True)
    page=browser.new_page(viewport={'width':400,'height':680},device_scale_factor=2)
    page.context.set_offline(True)
    page.set_default_timeout(5000)
    page.on('pageerror',lambda err: results['errors'].append(str(err)))
    page.on('request',lambda req: results['errors'].append('External request: '+req.url) if req.url.startswith(('http:','https:')) else None)
    page.route('https://**',lambda route: route.abort())
    for theme in ['light','dark']:
        for display in ['laptop','tv']:
            for state in ['main','compose','pending','offline','empty','accepted']:
                page.goto(f'{url}?screen={state}&theme={theme}&display={display}')
                page.wait_for_selector('h1')
                box=page.locator('#app').bounding_box()
                assert box['x']==20 and box['y']==20 and box['width']==360,box
                assert box['height']<=640,box
                sizes=page.evaluate('({scroll:app.scrollHeight,client:app.clientHeight,width:app.scrollWidth,cw:app.clientWidth,body:document.body.scrollWidth})')
                assert sizes['width']==sizes['cw'],sizes
                assert sizes['scroll']<=sizes['client']+1,(state,theme,sizes)
                assert sizes['body']==400,sizes
                results['states'].append({'state':state,'theme':theme,'display':display,'box':box,'overflow':False})
                if display=='laptop':page.screenshot(path=str(OUT/'screenshots'/f'{state}-{theme}.png'))
    # Keyboard-only main flow, using native type-ahead P for Priya. Disabled review cannot send without recipient.
    page.goto(url+'?screen=main&theme=light')
    page.keyboard.press('Tab');assert page.locator(':focus').inner_text().startswith('Hand over shift')
    page.keyboard.press('Enter');assert page.locator('h1').inner_text()=='Hand over shift'
    assert page.locator('[data-action="review"]').is_disabled()
    page.keyboard.press('Tab');assert page.locator(':focus').get_attribute('id')=='recipient'
    page.keyboard.press('p');page.keyboard.press('Enter')
    assert page.locator('#recipient').input_value()=='Priya Raman'
    page.keyboard.press('Tab');page.keyboard.press('Tab');assert page.locator(':focus').inner_text()=='Review handover'
    page.keyboard.press('Enter');assert page.locator('h1').inner_text()=='Ready to hand over?'
    page.screenshot(path=str(OUT/'screenshots'/'review-light.png'))
    page.keyboard.press('Tab');assert page.locator(':focus').inner_text()=='Back'
    page.keyboard.press('Tab');page.keyboard.press('Enter')
    assert page.locator('h1').inner_text()=='Waiting for Priya'
    assert 'You’re still on call.' in page.locator('#app').inner_text()
    page.wait_for_timeout(700)
    assert page.locator('h1').inner_text()=='Waiting for Priya'
    page.go_back()
    assert page.locator('h1').inner_text()=='Waiting for Priya'
    page.get_by_role('button',name='Back to schedule').click()
    assert page.locator('#app').evaluate('(e)=>e.scrollHeight<=e.clientHeight+1')
    assert 'Waiting for Priya' in page.locator('#app').inner_text()
    page.get_by_role('button',name='Waiting for Priya').click()
    page.get_by_role('button',name='Cancel request').click()
    assert page.get_by_role('button',name='Hand over shift').is_visible()
    results['interactions'].append('Keyboard choose/review/send; pending remains; return and cancel request')
    # Offline and empty retry preserve honest state.
    page.goto(url+'?screen=offline&theme=dark');page.get_by_role('button',name='Try again').click()
    assert 'Still offline' in page.locator('#app').inner_text()
    assert page.get_by_role('button',name='Hand over shift').count()==0
    page.goto(url+'?screen=empty');page.get_by_role('button',name='Check again').click()
    assert 'No schedule is available' in page.locator('#app').inner_text()
    results['interactions'].append('Offline retry and empty retry remain honest')
    # Cancel and Escape preserve return path.
    page.goto(url+'?screen=compose');page.keyboard.press('Escape')
    assert page.get_by_role('button',name='Hand over shift').is_visible()
    results['interactions'].append('Escape returns from compose')
    # System preference and reduced-motion.
    page.emulate_media(color_scheme='dark',reduced_motion='reduce');page.goto(url+'?screen=main')
    assert page.locator('html').get_attribute('data-theme')=='dark'
    assert page.locator('button').evaluate('(e)=>getComputedStyle(e).transitionDuration')=='0s'
    results['interactions'].append('System dark preference; reduced-motion removes transitions')
    # Explicit acceptance only in separate review harness.
    page.goto((OUT/'review.html').as_uri())
    frame=page.frame_locator('#product')
    frame.get_by_role('button',name='Hand over shift').click()
    frame.locator('#recipient').select_option('Priya Raman')
    frame.get_by_role('button',name='Review handover').click()
    frame.get_by_role('button',name='Send handover request').click()
    page.get_by_role('button',name='Simulate Priya accepting').click()
    frame.get_by_role('heading',name='Priya has the shift').wait_for(state='visible')
    frame.get_by_role('button',name='Back to schedule').click()
    assert frame.get_by_role('heading',name='Priya is on call').is_visible()
    results['interactions'].append('Separate explicit simulated acceptance updates owner and return schedule')
    browser.close()
assert not results['errors'],results['errors']
(OUT/'verification'/'results.json').write_text(json.dumps(results,indent=2))
print(json.dumps({'state_cases':len(results['states']),'interactions':results['interactions'],'errors':results['errors']},indent=2))
