from pathlib import Path
import json
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1]
base=(root/'app/index.html').as_uri()
checks=[]
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True)
    context=browser.new_context(viewport={'width':400,'height':680},reduced_motion='reduce')
    page=context.new_page()
    remote=[]
    page.on('request',lambda r: remote.append(r.url) if r.url.startswith(('http:','https:')) else None)
    page.goto(base+'?screen=main&theme=dark')
    page.keyboard.press('Tab')
    focus=page.evaluate('({tag:document.activeElement.tagName,outline:getComputedStyle(document.activeElement).outlineStyle,width:getComputedStyle(document.activeElement).outlineWidth})')
    assert focus['outline']=='solid' and focus['width']=='2px',focus
    page.keyboard.press('Enter')
    page.keyboard.press('Tab')
    assert page.get_by_role('radio',name='Priya Raman').evaluate('(e)=>e===document.activeElement')
    page.keyboard.press('Space')
    page.keyboard.press('Tab')
    assert page.locator('#note').evaluate('(e)=>e===document.activeElement')
    page.keyboard.type('Please watch the next deployment.')
    page.keyboard.press('Tab')
    assert page.locator('#review-button').evaluate('(e)=>e===document.activeElement')
    page.keyboard.press('Enter')
    assert page.get_by_role('heading',name='Review handover').evaluate('(e)=>e===document.activeElement')
    page.keyboard.press('Tab')
    assert page.get_by_role('button',name='Send handover request').evaluate('(e)=>e===document.activeElement')
    page.keyboard.press('Enter')
    assert page.get_by_role('heading',name='Waiting for Priya').evaluate('(e)=>e===document.activeElement')
    page.keyboard.press('Tab')
    page.keyboard.press('Tab')
    assert page.get_by_role('button',name='Cancel request').evaluate('(e)=>e===document.activeElement')
    page.keyboard.press('Enter')
    assert 'screen=main' in page.url
    page.go_back()
    page.wait_for_timeout(80)
    assert 'screen=main' in page.url, 'Back must not resurrect a cancelled request'
    checks.append('Keyboard-only handover and cancellation, with visible focus and focus after navigation')
    checks.append('Browser Back does not resurrect a cancelled request')
    # Escape from review preserves the selected recipient and note.
    page.goto(base+'?screen=compose&theme=light')
    page.get_by_role('radio',name='Priya Raman').check()
    long_note='Review the deployment. '+('x'*475)
    page.locator('#note').fill(long_note)
    page.get_by_role('button',name='Review handover').click()
    m=page.locator('#app').evaluate('(e)=>({w:e.clientWidth,sw:e.scrollWidth,h:e.clientHeight,sh:e.scrollHeight})')
    assert m['w']==m['sw'] and m['sh']>m['h'] and m['h']<=638,m
    page.get_by_role('button',name='Send handover request').focus()
    b=page.get_by_role('button',name='Send handover request').bounding_box()
    assert b['y']>=20 and b['y']+b['height']<=660,b
    page.keyboard.press('Escape')
    assert page.locator('#note').input_value()==long_note[:500]
    checks.append('500-character unbroken note wraps; vertical scrolling keeps actions reachable; Escape retains draft')
    # Re-rendering user text cannot inject markup.
    page.locator('#note').fill('<img src=x onerror=alert(1)>')
    page.get_by_role('button',name='Review handover').click()
    assert page.locator('.note-preview img').count()==0
    checks.append('Notes are rendered as text, not HTML')
    # Fixed fixtures have no asynchronous arrival; still check actual layout shift.
    page.goto(base+'?screen=main&theme=light')
    page.evaluate("window.shifts=[];new PerformanceObserver(l=>window.shifts.push(...l.getEntries().map(e=>e.value))).observe({type:'layout-shift',buffered:true})")
    page.wait_for_timeout(250)
    assert sum(page.evaluate('window.shifts'))==0
    checks.append('Measured layout shift on loaded main screen: 0')
    assert remote==[],remote
    checks.append('No HTTP or HTTPS requests across checks; all assets load from disk')
    browser.close()
(root/'verification/edge-results.json').write_text(json.dumps({'checks':checks,'remote_requests':remote},indent=2))
print('PASS: '+str(len(checks))+' keyboard, long-content, history, layout, and offline checks.')
