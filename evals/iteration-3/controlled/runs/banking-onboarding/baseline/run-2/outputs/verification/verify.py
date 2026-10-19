from pathlib import Path
import json
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
APP=(ROOT/'app/index.html').as_uri()
SHOTS=ROOT/'verification/screenshots'
SHOTS.mkdir(exist_ok=True)
results=[]
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless=True)
 page=browser.new_page(viewport={'width':390,'height':844},device_scale_factor=1)
 errors=[]
 page.on('pageerror',lambda e:errors.append(str(e)))
 for width,height in [(390,844),(320,568)]:
  page.set_viewport_size({'width':width,'height':height})
  for theme in ['light','dark']:
   for state in ['welcome','details','details-error','code','code-error','help','done']:
    page.goto(f'{APP}?screen={state}&theme={theme}&display=laptop')
    page.evaluate('document.fonts.ready')
    assert page.locator('#app').count()==1
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'),f'Overflow {state} {width} {theme}'
    assert page.locator('h1').inner_text()
    if state=='help':
     assert page.locator('dialog').evaluate('(d)=>d.open')
     page.keyboard.press('Escape')
     assert not page.locator('dialog').evaluate('(d)=>d.open')
     page.wait_for_function("document.activeElement.id === 'help-trigger'")
    if (width,theme,state) in [(390,'light','welcome'),(320,'light','details-error'),(390,'dark','code-error'),(390,'light','done')]:
     page.screenshot(path=str(SHOTS/f'{state}-{width}-{theme}.png'),full_page=True)
    results.append({'width':width,'height':height,'theme':theme,'state':state,'overflow':False})
 page.set_viewport_size({'width':390,'height':844})
 page.goto(f'{APP}?screen=welcome&theme=light')
 page.get_by_role('button',name='Let’s get started').click()
 page.get_by_role('button',name='Continue').click()
 assert page.locator('#full-name').get_attribute('aria-invalid')=='true'
 assert page.locator('#mobile').get_attribute('aria-invalid')=='true'
 assert page.locator('#full-name').evaluate('(e)=>e===document.activeElement')
 bank=page.evaluate('EVAL_FIXTURES.bank')
 page.get_by_label('Full name').fill(bank['customer'])
 page.get_by_label('Mobile number').fill('07700 900482')
 page.get_by_role('button',name='Continue').click()
 assert 'code' in page.url
 page.get_by_label('6-digit code').fill('000000')
 page.get_by_role('button',name='Confirm code').click()
 assert page.locator('#code').get_attribute('aria-invalid')=='true'
 assert page.locator('h1').inner_text()=='Check your mobile'
 page.get_by_role('button',name='Help',exact=True).click()
 assert page.locator('dialog').evaluate('(d)=>d.open')
 assert page.locator('dialog a').get_attribute('href')=='tel:'+bank['helpPhone'].replace(' ','')
 page.get_by_role('button',name='Back to setup').click()
 page.wait_for_function("document.activeElement.id === 'help-trigger'")
 page.get_by_role('button',name='Help',exact=True).click()
 page.keyboard.press('Tab')
 assert page.locator('dialog a').evaluate('(e)=>e===document.activeElement')
 page.keyboard.press('Tab');page.keyboard.press('Tab')
 assert page.locator('dialog a').evaluate('(e)=>e===document.activeElement')
 page.keyboard.press('Escape')
 page.get_by_role('button',name='Request a new code').click()
 assert 'no text is sent' in page.locator('#resend-status').inner_text()
 page.get_by_role('button',name='Back',exact=True).click()
 assert page.get_by_label('Full name').input_value()==bank['customer']
 page.get_by_role('button',name='Continue').click()
 page.get_by_label('6-digit code').fill(bank['testCode'])
 page.get_by_role('button',name='Confirm code').click()
 assert 'ready' in page.locator('h1').inner_text()
 assert bank['accountNumber'] in page.locator('main').inner_text()
 page.get_by_role('button',name='Finish',exact=True).click()
 assert 'where you are' in page.locator('h1').inner_text()
 # Keyboard-only happy path, no mouse.
 page.goto(f'{APP}?screen=welcome&theme=dark')
 page.keyboard.press('Tab');page.keyboard.press('Tab');page.keyboard.press('Enter')
 assert page.locator('h1').inner_text()=='First, your details'
 page.keyboard.press('Tab');page.keyboard.type(bank['customer']);page.keyboard.press('Tab');page.keyboard.type('07700900482');page.keyboard.press('Tab');page.keyboard.press('Enter')
 assert page.locator('h1').inner_text()=='Check your mobile'
 page.keyboard.press('Tab');page.keyboard.type(bank['testCode']);page.keyboard.press('Tab');page.keyboard.press('Enter')
 assert 'ready' in page.locator('h1').inner_text()
 # System theme and URL override, reduced motion, display variant, zoom/reflow.
 page.emulate_media(color_scheme='dark',reduced_motion='reduce')
 page.goto(f'{APP}?screen=code&display=tv')
 assert page.locator('html').get_attribute('data-theme')=='dark'
 assert page.locator('html').get_attribute('data-display')=='tv'
 assert page.locator('#code').evaluate('(e)=>getComputedStyle(e).transitionDuration')=='0s'
 page.goto(f'{APP}?screen=welcome&theme=light&display=tv')
 assert page.locator('html').get_attribute('data-theme')=='light'
 page.set_viewport_size({'width':320,'height':568})
 page.evaluate("document.documentElement.style.fontSize='200%'")
 assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'),'200% text overflow'
 assert not errors,errors
 browser.close()
(ROOT/'verification/results.json').write_text(json.dumps({'screens':results,'interaction_checks':'Passed: validation, wrong and fixture code, Back retention, Help button/Escape/focus trap/return, resend status, finish, keyboard-only happy path, system theme, URL override, reduced motion, display flag, 200% welcome reflow','page_errors':errors},indent=2))
print(f'PASS: {len(results)} screen/size/theme checks and interaction suite')
