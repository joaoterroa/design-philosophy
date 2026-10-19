from playwright.sync_api import sync_playwright
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
BASE=(ROOT/'app/index.html').as_uri()
GROUPS=[(['main','compose','pending','offline','empty','accepted'],[(400,680,'laptop')]),(['live','stale','surge'],[(1920,1080,'tv'),(1440,900,'laptop')]),(['welcome','details','details-error','code','code-error','help','done'],[(390,844,'laptop'),(320,568,'laptop')])]
results=[];errors=[];requests=[]
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True)
 page=browser.new_page()
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.on('request',lambda r:requests.append(r.url) if not r.url.startswith('file:') else None)
 for states,sizes in GROUPS:
  for state in states:
   for w,h,display in sizes:
    for theme in ['light','dark']:
     page.set_viewport_size({'width':w,'height':h})
     page.goto(f'{BASE}?screen={state}&theme={theme}&display={display}')
     page.evaluate('document.fonts.ready')
     m=page.evaluate('''() => {const app=document.querySelector('#app'),r=app.getBoundingClientRect();return {width:document.documentElement.scrollWidth,height:document.documentElement.scrollHeight,app:{x:r.x,y:r.y,width:r.width,height:r.height},incidents:document.querySelectorAll('.incident').length,dialog:!!document.querySelector('dialog[open]'),clipped:[...document.querySelectorAll('h1,h2,h3,p,span,button,label,input,select')].filter(e=>e.clientWidth>0&&e.scrollWidth>e.clientWidth+2).map(e=>e.outerHTML.slice(0,100))}}''')
     assert m['width']<=w,(state,theme,w,'horizontal overflow',m)
     assert not m['clipped'],(state,theme,w,'clipped text',m['clipped'])
     if state in GROUPS[0][0]:assert m['app']['width']==360 and m['app']['height']<=640 and m['app']['x']==20 and m['app']['y']==20
     if state in ['live','stale']:assert m['incidents']==7
     if state=='surge':assert m['incidents']==12
     if display=='tv':assert m['height']<=h,(state,theme,'TV vertical overflow',m['height'])
     if state=='help':assert m['dialog']
     assert not page.get_by_text(page.evaluate('EVAL_FIXTURES.bank.testCode'),exact=True).count()
     results.append({'state':state,'theme':theme,'viewport':[w,h],'display':display,**m})
 # Menu keyboard path, review editing, return, explicit acceptance and cancellation.
 page.set_viewport_size({'width':400,'height':680});page.goto(BASE+'?screen=main&theme=light')
 page.get_by_role('button',name='Hand over your shift').focus();page.keyboard.press('Enter')
 page.locator('#recipient').select_option('Priya Raman');page.locator('#handover-note').fill('Watch the EU routing queue.')
 page.get_by_role('button',name='Review handover').click();assert page.get_by_role('heading',name='Ready to hand over?').is_visible()
 page.get_by_role('button',name='Edit handover').click();assert page.locator('#recipient').input_value()=='Priya Raman'
 page.get_by_role('button',name='Review handover').click();page.get_by_role('button',name='Send request').click()
 assert page.get_by_text('You’re still on call.',exact=True).is_visible()
 page.wait_for_timeout(300);assert 'screen=pending' in page.url
 page.get_by_role('button',name='Back to schedule').click();page.get_by_role('button',name='View handover request').click()
 page.evaluate("window.postMessage('simulate-acceptance','*')");page.wait_for_function("location.search.includes('screen=accepted')")
 page.get_by_role('button',name='View current schedule').click();assert page.get_by_role('heading',name='Priya is on call').is_visible()
 page.goto(BASE+'?screen=pending');page.get_by_role('button',name='Cancel request').click();assert page.get_by_role('heading',name='You’re on call').is_visible()
 # Bank validation, retained input, Help button/Escape/focus, correct fixture code.
 page.set_viewport_size({'width':320,'height':568});page.goto(BASE+'?screen=welcome&theme=light')
 page.get_by_role('button',name='Get started').click();page.get_by_role('button',name='Send me a code').click()
 assert page.locator('[aria-invalid="true"]').count()==2
 page.locator('#full-name').fill('Alex Morgan');page.locator('#mobile').fill('07700 900482');page.get_by_role('button',name='Send me a code').click()
 assert 'screen=code' in page.url
 page.locator('#sms-code').fill('000000');page.get_by_role('button',name='Confirm code').click();assert 'screen=code-error' in page.url
 assert page.locator('#sms-code').input_value()=='000000'
 page.get_by_role('button',name='Help',exact=True).click();assert page.locator('dialog').is_visible()
 page.keyboard.press('Escape');assert not page.locator('dialog').is_visible();assert page.evaluate('document.activeElement.textContent')=='Help'
 page.get_by_role('button',name='Help',exact=True).click();page.get_by_role('button',name='Back to setup').click();assert page.evaluate('document.activeElement.textContent')=='Help'
 page.locator('#sms-code').fill(page.evaluate('EVAL_FIXTURES.bank.testCode'));page.get_by_role('button',name='Confirm code').click()
 assert 'screen=done' in page.url
 assert page.get_by_text('12345678',exact=True).is_visible()
 page.goto(BASE+'?screen=help&theme=dark');page.keyboard.press('Escape');page.wait_for_url('**screen=code**')
 assert page.evaluate('document.activeElement.textContent')=='Help'
 # System theme, explicit override and reduced motion.
 page.emulate_media(color_scheme='dark',reduced_motion='reduce');page.goto(BASE+'?screen=main')
 assert page.evaluate('document.documentElement.dataset.theme')=='dark'
 assert page.locator('button').first.evaluate('(e)=>getComputedStyle(e).transitionDuration')=='0s'
 page.goto(BASE+'?screen=main&theme=light');assert page.evaluate('document.documentElement.dataset.theme')=='light'
 # Separate harness must deliver explicit acceptance across file origins.
 page.goto((ROOT/'review.html').as_uri())
 frame=page.frame_locator('iframe')
 frame.get_by_role('button',name='Hand over your shift').click();frame.locator('#recipient').select_option('Priya Raman')
 frame.get_by_role('button',name='Review handover').click();frame.get_by_role('button',name='Send request').click()
 page.get_by_role('button',name='Simulate Priya accepting').click()
 frame.get_by_role('heading',name='Handover complete').wait_for(state='visible')
 browser.close()
assert not errors,errors
assert not requests,requests
report={'states_checked':len(results),'javascript_errors':errors,'external_requests':requests,'interactions':'passed','states':results}
(ROOT/'verification/results.json').write_text(json.dumps(report,indent=2))
print(json.dumps({'states_checked':len(results),'javascript_errors':errors,'external_requests':requests,'interactions':'passed','tv_heights':[{k:r[k] for k in ['state','theme','height']} for r in results if r['display']=='tv']},indent=2))
