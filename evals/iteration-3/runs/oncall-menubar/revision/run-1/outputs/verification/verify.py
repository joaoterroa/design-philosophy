from pathlib import Path
import json
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1]
base=(root/'app/index.html').as_uri()
results=[]
errors=[]
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True)
    context=browser.new_context(viewport={"width":400,"height":680},device_scale_factor=1)
    page=context.new_page()
    page.on('pageerror', lambda e: errors.append(str(e)))
    for theme in ['light','dark']:
        for state in ['main','compose','review','pending','offline','empty','accepted']:
            page.goto(f'{base}?screen={state}&theme={theme}')
            page.wait_for_timeout(70)
            box=page.locator('#app').bounding_box()
            metrics=page.locator('#app').evaluate('(e)=>({scrollHeight:e.scrollHeight,clientHeight:e.clientHeight,scrollWidth:e.scrollWidth,clientWidth:e.clientWidth})')
            assert box['x']==20 and box['y']==20 and box['width']==360, (state,box)
            assert box['height']<=640, (state,box)
            assert metrics['scrollWidth']==metrics['clientWidth'],(state,metrics)
            assert metrics['scrollHeight']==metrics['clientHeight'],(state,metrics)
            assert page.locator('h1').count()==1
            page.screenshot(path=str(root/f'verification/screenshots/{state}-{theme}.png'))
            results.append({'state':state,'theme':theme,'bounds':box,'overflow':metrics})
    # Complete keyboard-led main flow with review, notes, and cancellation route.
    page.goto(f'{base}?screen=main&theme=light')
    page.keyboard.press('Tab')
    assert page.locator('[data-action="compose"]').evaluate('(e)=>e===document.activeElement')
    page.keyboard.press('Enter')
    assert 'compose' in page.url
    assert page.locator('#review-button').is_disabled()
    page.keyboard.press('Tab') # heading -> first sequential control can be Cancel or recipient
    page.get_by_role('radio',name='Priya Raman').check()
    page.locator('#note').fill('Routing is stable. Keep an eye on the deploy.')
    page.get_by_role('button',name='Review handover').click()
    assert 'review' in page.url
    assert page.get_by_text('Routing is stable. Keep an eye on the deploy.').count()==1
    page.get_by_role('button',name='Back',exact=False).click()
    assert page.locator('#note').input_value()=='Routing is stable. Keep an eye on the deploy.'
    assert page.get_by_role('radio',name='Priya Raman').is_checked()
    page.get_by_role('button',name='Review handover').click()
    page.get_by_role('button',name='Send handover request').click()
    assert 'pending' in page.url
    assert page.get_by_text('You’re still on call',exact=True).count()==1
    page.wait_for_timeout(400)
    assert 'pending' in page.url, 'Acceptance must not be automatic'
    page.get_by_role('button',name='Back to schedule').click()
    assert page.get_by_role('button',name='View pending handover').count()==1
    page.get_by_role('button',name='View pending handover').click()
    page.get_by_role('button',name='Cancel request').click()
    assert page.get_by_role('button',name='Hand over shift').count()==1
    assert page.get_by_text('Request cancelled. You’re still on call.').count()==1
    # Escape returns from review to compose, then schedule.
    page.get_by_role('button',name='Hand over shift').click()
    page.keyboard.press('Escape')
    assert 'screen=main' in page.url
    # Honest offline and empty retries.
    page.goto(f'{base}?screen=offline')
    assert page.get_by_role('button',name='Hand over shift').is_disabled()
    page.get_by_role('button',name='Try again').click()
    assert 'Still offline' in page.locator('#retry-status').inner_text()
    page.goto(f'{base}?screen=empty')
    page.get_by_role('button',name='Check again').click()
    assert 'No schedule is available' in page.locator('#empty-status').inner_text()
    # Separate explicit acceptance simulation; completed schedule must agree.
    page.goto((root/'review.html').as_uri())
    page.locator('#state').select_option('pending')
    page.get_by_role('button',name='Open selected state').click()
    frame=page.frame_locator('#prototype')
    frame.get_by_role('heading',name='Waiting for Priya').wait_for()
    page.get_by_role('button',name='Simulate Priya accepting').click()
    frame.get_by_role('heading',name='Priya is now on call').wait_for()
    frame.get_by_role('button',name='Back to schedule').click()
    assert frame.get_by_text('Priya is on call',exact=True).count()==1
    assert frame.get_by_role('button',name='Hand over shift').count()==0
    # URL theme beats system; otherwise system theme is followed.
    page.emulate_media(color_scheme='dark',reduced_motion='reduce')
    page.goto(f'{base}?screen=main')
    assert page.locator('html').get_attribute('data-theme')=='dark'
    page.goto(f'{base}?screen=main&theme=light')
    assert page.locator('html').get_attribute('data-theme')=='light'
    assert not errors,errors
    browser.close()
(root/'verification/results.json').write_text(json.dumps({'screens':results,'page_errors':errors,'interaction_checks':'passed'},indent=2))
print(f'PASS: {len(results)} state/theme screenshots; flow, cancel, Escape, retries, explicit acceptance, and system theme checks.')
