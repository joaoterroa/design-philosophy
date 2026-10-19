from playwright.sync_api import sync_playwright
from pathlib import Path
import json
import io
from PIL import Image, ImageDraw
shots={"menu":[],"dashboard":[],"bank":[]}
ROOT=Path(__file__).resolve().parents[1]
URL=(ROOT/'app/index.html').as_uri()
results=[]
errors=[]
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True)
 page=browser.new_page(device_scale_factor=1)
 page.on('pageerror',lambda e:errors.append(str(e)))
 def open_state(state,theme,w,h,display='laptop'):
  page.set_viewport_size({'width':w,'height':h})
  page.goto(f'{URL}?screen={state}&theme={theme}&display={display}')
  page.wait_for_timeout(60)
  page.evaluate('document.fonts.ready')
 def measure(state,theme,w,h,display):
  data=page.evaluate('''() => {const a=document.querySelector('#app'),r=a.getBoundingClientRect();return {app:{x:r.x,y:r.y,width:r.width,height:r.height},horizontalOverflow:document.documentElement.scrollWidth>innerWidth,bodyHeight:document.documentElement.scrollHeight,dialogOpen:!!document.querySelector('dialog[open]'),table:document.querySelector('.table-wrap')?{client:document.querySelector('.table-wrap').clientHeight,scroll:document.querySelector('.table-wrap').scrollHeight}:null,incidents:document.querySelectorAll('.incident-table tbody tr').length}}''')
  if data['horizontalOverflow']:raise AssertionError(f'Horizontal overflow: {state} {theme} {w}')
  if state in ['main','compose','pending','offline','empty','accepted']:
   assert data['app']['width']==360 and data['app']['height']<=640 and data['app']['x']==20 and data['app']['y']==20,data
  if state in ['live','stale','surge']:assert data['incidents']==(12 if state=='surge' else 7)
  if state in ['live','stale'] and display=='tv':assert data['table']['client']==data['table']['scroll'],'TV live/stale list must fit'
  if state in ['live','stale','surge'] and display=='tv':assert data['bodyHeight']==h,'TV document must fit scene'
  assert page.evaluate('EVAL_FIXTURES.bank.testCode') not in page.inner_text('#app'),'Test code exposed'
  group='menu' if state in ['main','compose','pending','offline','empty','accepted'] else 'dashboard' if state in ['live','stale','surge'] else 'bank'
  shot=Image.open(io.BytesIO(page.screenshot())).convert('RGB')
  target=240 if group=='menu' else 480 if group=='dashboard' else 195
  shot.resize((target,round(shot.height*target/shot.width))).save(io.BytesIO(),format='PNG')
  shot.thumbnail((target,600))
  shots[group].append((f'{state} / {theme} / {w}×{h} / {display}',shot.copy()))
  results.append({'state':state,'theme':theme,'width':w,'height':h,'display':display,**data})
 for state in ['main','compose','pending','offline','empty','accepted']:
  for theme in ['light','dark']:
   open_state(state,theme,400,680);measure(state,theme,400,680,'laptop')
   if (state,theme) in [('main','light'),('main','dark'),('pending','light'),('offline','dark')]:page.screenshot(path=str(ROOT/f'verification/{state}-{theme}.png'))
 for state in ['live','stale','surge']:
  for theme in ['light','dark']:
   for display,w,h in [('tv',1920,1080),('laptop',1440,900)]:
    open_state(state,theme,w,h,display);measure(state,theme,w,h,display)
    if (state,theme,display) in [('live','dark','tv'),('stale','light','laptop'),('surge','dark','laptop')]:page.screenshot(path=str(ROOT/f'verification/{state}-{theme}-{display}.png'))
 for state in ['welcome','details-error','code','code-error','help','done']:
  for theme in ['light','dark']:
   for w,h in [(390,844),(320,568)]:
    open_state(state,theme,w,h);measure(state,theme,w,h,'laptop')
    if (state,theme,w) in [('welcome','light',390),('code-error','dark',320),('help','light',390),('done','light',390)]:page.screenshot(path=str(ROOT/f'verification/{state}-{theme}-{w}.png'),full_page=True)
 # Rota choose -> review -> pending -> return -> cancel. Keyboard activates review and send.
 open_state('main','light',400,680)
 page.get_by_role('button',name='Hand over shift…').click()
 page.get_by_label('Hand over to').select_option('Priya Raman')
 page.get_by_label('Handover note').fill('Routing is stable; keep an eye on the retry queue.')
 page.get_by_role('button',name='Review handover').focus();page.keyboard.press('Enter')
 assert page.get_by_role('heading',name='Review handover').count()==1
 page.get_by_role('button',name='Send request',exact=True).focus();page.keyboard.press('Enter')
 assert page.get_by_role('heading',name='Waiting for Priya').count()==1
 assert 'You’re still on call' in page.inner_text('#app')
 page.get_by_role('button',name='Back to schedule').click()
 page.get_by_role('button',name='View request').click()
 page.get_by_role('button',name='Cancel request').click()
 assert page.get_by_role('button',name='Hand over shift…').count()==1
 results.append({'interaction':'Rota choose, note, review, send, pending responsibility, return, cancel','passed':True})
 # Review harness acceptance happens only when explicitly clicked.
 page.set_viewport_size({'width':900,'height':900});page.goto((ROOT/'review.html').as_uri())
 frame=page.frame_locator('#preview')
 frame.get_by_role('button',name='Hand over shift…').click();frame.get_by_label('Hand over to').select_option('Priya Raman');frame.get_by_role('button',name='Review handover').click();frame.get_by_role('button',name='Send request',exact=True).click()
 assert frame.get_by_role('heading',name='Waiting for Priya').count()==1
 page.get_by_role('button',name='Simulate Priya accepting').click()
 frame.get_by_role('heading',name='Handover accepted').wait_for()
 results.append({'interaction':'Separate harness explicit acceptance','passed':True})
 # Banking validation, wrong-code rejection, help trap, Escape + button focus return, success.
 open_state('welcome','light',390,844)
 page.get_by_role('button',name='Get started').click()
 page.get_by_role('button',name='Send my code').click()
 assert page.locator('#full-name').get_attribute('aria-invalid')=='true'
 page.get_by_label('Full name',exact=True).fill('Alex Morgan');page.get_by_label('Mobile number',exact=True).fill('07700 900482')
 page.get_by_role('button',name='Send my code').click()
 page.get_by_label('Text message code',exact=True).fill('000000');page.get_by_role('button',name='Confirm code').click()
 assert page.locator('#sms-code').get_attribute('aria-invalid')=='true'
 page.get_by_role('button',name='Help',exact=True).click();assert page.locator('dialog').evaluate('(e)=>e.open')
 page.keyboard.press('Escape');assert page.evaluate('document.activeElement.id')=='help-trigger'
 page.get_by_role('button',name='Help',exact=True).click();page.get_by_role('button',name='Back to setup').click();assert page.evaluate('document.activeElement.id')=='help-trigger'
 code=page.evaluate('EVAL_FIXTURES.bank.testCode');page.get_by_label('Text message code',exact=True).fill(code);page.get_by_role('button',name='Confirm code').click()
 assert 'setup complete' in page.inner_text('#app').lower()
 assert code not in page.inner_text('#app')
 results.append({'interaction':'Bank validation, wrong code, Help, Escape/button focus return, correct code, completion','passed':True})
 # Reduced motion and system preference.
 page.emulate_media(color_scheme='dark',reduced_motion='reduce');page.goto(URL+'?screen=main')
 assert page.evaluate('document.documentElement.dataset.theme')=='dark'
 assert page.locator('.btn').first.evaluate('(e)=>getComputedStyle(e).transitionDuration')=='0s'
 results.append({'interaction':'System dark preference and reduced motion','passed':True})
 # Reach final surge row with the keyboard scroll container.
 open_state('surge','dark',1440,900)
 page.locator('.table-wrap').focus();page.keyboard.press('End')
 page.wait_for_timeout(80)
 assert page.locator('.table-wrap').evaluate('(e)=>e.scrollTop>0')
 results.append({'interaction':'Laptop surge keyboard scrolling','passed':True})
 browser.close()
for group,items in shots.items():
 cols=3 if group!='bank' else 4
 cw=max(im.width for _,im in items)+16;ch=max(im.height for _,im in items)+40
 sheet=Image.new('RGB',(cols*cw,((len(items)+cols-1)//cols)*ch),'#e3e5e8');draw=ImageDraw.Draw(sheet)
 for n,(label,im) in enumerate(items):
  x=(n%cols)*cw;y=(n//cols)*ch
  draw.text((x+8,y+8),label,fill='#202127');sheet.paste(im,(x+8,y+30))
 sheet.save(ROOT/f'verification/{group}-state-sheet.jpg',quality=90)
assert not errors,errors
(ROOT/'verification/results.json').write_text(json.dumps({'checks':results,'consoleErrors':errors},indent=2))
print(f'PASS: {len(results)} state and interaction checks; no page errors.')
