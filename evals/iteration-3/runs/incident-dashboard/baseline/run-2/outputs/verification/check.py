from playwright.sync_api import sync_playwright
from pathlib import Path
import json, hashlib
ROOT=Path(__file__).resolve().parents[1]
URL=(ROOT/'app/index.html').as_uri()
OUT=ROOT/'verification'
results=[]
shots={'live-light-laptop','live-dark-tv','surge-dark-tv','stale-light-laptop','main-light-menu','compose-dark-menu','pending-light-menu','welcome-light-390','details-error-light-320','code-dark-390','help-light-320','done-light-390'}
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless=True)
 page=browser.new_page()
 errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 cases=[]
 for state in ['live','stale','surge']:
  for size,w,h in [('laptop',1440,900),('tv',1920,1080)]:
   for theme in ['light','dark']:cases.append((state,theme,size,w,h))
 for state in ['main','compose','pending','offline','empty','accepted']:
  for theme in ['light','dark']:cases.append((state,theme,'menu',400,680))
 for state in ['welcome','details','details-error','code','code-error','help','done']:
  for size,w,h in [('390',390,844),('320',320,568)]:
   for theme in ['light','dark']:cases.append((state,theme,size,w,h))
 for state,theme,size,w,h in cases:
  page.set_viewport_size({'width':w,'height':h})
  page.goto(f'{URL}?screen={state}&theme={theme}&display={size}')
  page.evaluate('document.fonts.ready');page.wait_for_timeout(40)
  key=f'{state}-{theme}-{size}'
  metrics=page.evaluate('''() => ({width:document.documentElement.scrollWidth,height:document.documentElement.scrollHeight,app:document.querySelector('#app').getBoundingClientRect().toJSON(),table:document.querySelector('.incident-table')?.getBoundingClientRect().toJSON(),rows:document.querySelectorAll('.incident-table tbody tr').length})''')
  assert metrics['width']<=w,f'Horizontal overflow {key}: {metrics}'
  if size=='menu':
   assert metrics['app']['width']==360 and metrics['app']['x']==20 and metrics['app']['y']==20
   assert metrics['app']['height']<=640
  if size=='tv':assert metrics['height']<=h,f'TV overflow {key}: {metrics}'
  if key in shots:page.screenshot(path=str(OUT/f'{key}.png'),full_page=True)
  results.append({'case':key,**metrics})
 # Primary handover path, keyboard operated.
 page.goto(f'{URL}?screen=main&theme=light');page.evaluate('sessionStorage.clear()');page.reload()
 page.get_by_role('button',name='Hand over your shift').focus();page.keyboard.press('Enter')
 assert 'Who’s taking over?' in page.locator('h1').inner_text()
 page.get_by_label('Handover note').fill('Keep an eye on Routing API.')
 page.get_by_role('button',name='Review handover').focus();page.keyboard.press('Enter')
 assert page.get_by_text('You stay responsible until Priya accepts.').is_visible()
 page.get_by_role('button',name='Send handover',exact=True).click()
 assert page.get_by_text('You’re still responsible.',exact=True).is_visible()
 page.wait_for_timeout(100);assert 'pending' in page.url
 page.get_by_role('button',name='Record Priya’s acceptance').click();assert 'Priya has the shift.' in page.locator('h1').inner_text()
 page.get_by_role('button',name='Back to schedule').click();assert 'Priya is on call.' in page.locator('h1').inner_text()
 # Cancel route.
 page.evaluate('sessionStorage.clear()');page.goto(f'{URL}?screen=compose');page.get_by_role('button',name='Cancel',exact=True).click();assert 'screen=main' in page.url
 # TV page retains every fixture incident across two pages.
 page.set_viewport_size({'width':1920,'height':1080});page.goto(f'{URL}?screen=surge&display=tv&theme=dark');assert page.locator('tbody tr').count()==7
 page.get_by_role('button',name='Next').click();assert page.locator('tbody tr').count()==5;assert page.get_by_text('INC-2278',exact=True).is_visible();page.get_by_role('button',name='Previous').click();assert page.get_by_text('INC-2291',exact=True).is_visible()
 # Banking validation, full completion, modal dismiss and focus.
 page.set_viewport_size({'width':320,'height':568});page.goto(f'{URL}?screen=welcome&theme=light');page.get_by_role('button',name='Get started').click()
 page.get_by_role('button',name='Send security code').click();assert page.locator('#name-error').is_visible();assert page.locator('#mobile-error').is_visible()
 page.get_by_label('Full name',exact=True).fill('Alex Morgan');page.get_by_label('Mobile number',exact=True).fill('07700 900482');page.get_by_role('button',name='Send security code').click()
 page.get_by_label('Security code',exact=True).fill('000000');page.get_by_role('button',name='Verify and finish').click();assert page.locator('#code-error').is_visible();assert 'screen=done' not in page.url
 page.get_by_role('button',name='Help',exact=True).click();assert page.locator('dialog').is_visible();page.keyboard.press('Escape');assert not page.locator('dialog').is_visible();assert page.locator('#help-button').evaluate('(el)=>el===document.activeElement')
 page.get_by_role('button',name='Help',exact=True).click();page.get_by_role('button',name='Back to setup').click();assert page.locator('#help-button').evaluate('(el)=>el===document.activeElement')
 page.get_by_role('button',name='Back to your details').click();assert page.get_by_label('Full name',exact=True).input_value()=='Alex Morgan';page.get_by_role('button',name='Send security code').click()
 code=page.evaluate('EVAL_FIXTURES.bank.testCode');page.get_by_label('Security code',exact=True).fill(code);page.get_by_role('button',name='Verify and finish').click();assert page.get_by_text('Setup complete',exact=True).is_visible()
 # System theme, reduced motion and fixture invariants.
 page.emulate_media(color_scheme='dark',reduced_motion='reduce');page.goto(f'{URL}?screen=live');assert page.locator('html').get_attribute('data-theme')=='dark'
 assert page.locator('tbody tr').count()==7
 page.goto(f'{URL}?screen=surge&display=laptop');assert page.locator('tbody tr').count()==12
 assert not errors,errors
 browser.close()
assert (ROOT/'app/fixtures.js').read_bytes()==(ROOT.parent/'fixtures.js').read_bytes()
(OUT/'results.json').write_text(json.dumps({'screens':results,'consoleErrors':errors,'interactions':'passed','fixtureUnchanged':True},indent=2))
print(f'PASS: {len(results)} state/theme/size combinations; handover, cancel, TV paging, validation, wrong and correct code, Back, Help/Escape/focus, system theme, reduced motion, fixture parity.')
