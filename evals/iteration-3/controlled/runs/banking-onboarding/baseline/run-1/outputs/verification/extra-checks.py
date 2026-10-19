from pathlib import Path
from playwright.sync_api import sync_playwright
import json
ROOT=Path(__file__).resolve().parents[1]
URL=(ROOT/'app/index.html').as_uri()
r={}
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True)
 page=browser.new_page(viewport={'width':320,'height':568})
 page.goto(URL+'?screen=welcome&theme=light&display=tv')
 page.wait_for_function('document.fonts.status === "loaded"')
 r['welcome_start_bounds_320']=page.locator('#start').bounding_box()
 assert r['welcome_start_bounds_320']['y']+r['welcome_start_bounds_320']['height']<=568
 page.get_by_role('button',name='Get started').click()
 page.locator('#name').fill('João D’Ávila')
 page.locator('#mobile').fill('+44 7123 456482')
 page.get_by_role('button',name='Continue').click()
 assert 'screen=code' in page.url
 page.locator('#code').fill('12')
 page.get_by_role('button',name='Confirm code').click()
 assert 'all 6 numbers' in page.locator('#code-error').inner_text()
 page.get_by_role('button',name='Help',exact=True).click()
 assert page.locator('.phone').get_attribute('href')=='tel:'+page.evaluate('EVAL_FIXTURES.bank.helpPhone').replace(' ','')
 page.get_by_role('button',name='Back to setup').click()
 assert page.evaluate('document.activeElement.id')=='help'
 page.locator('#code').fill(page.evaluate('EVAL_FIXTURES.bank.testCode'))
 page.get_by_role('button',name='Confirm code').click()
 assert 'João' in page.locator('h1').inner_text()
 r['small_phone_full_flow']='PASS: Unicode name, +44 mobile, incomplete-code rejection, Help, completion'
 for width in [320,390]:
  page.set_viewport_size({'width':width,'height':568 if width==320 else 844})
  for state in ['welcome','details-error','code-error','help','done']:
   page.goto(URL+f'?screen={state}&theme=dark&display=tv')
   page.evaluate('document.documentElement.style.fontSize="200%"')
   assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),(state,width)
   if state=='help':
    page.get_by_role('button',name='Back to setup').click()
    assert not page.locator('dialog').evaluate('(d)=>d.open')
 r['enlarged_text']='PASS: 200% text, five states at both 320px and 390px; enlarged Help dismissal reachable'
 page.set_viewport_size({'width':320,'height':568})
 page.goto(URL+'?screen=code&theme=light')
 page.keyboard.press('Tab')
 focus=page.evaluate('({id:document.activeElement.id,outline:getComputedStyle(document.activeElement).outlineStyle,width:getComputedStyle(document.activeElement).outlineWidth})')
 assert focus['outline']=='solid' and focus['width']=='3px',focus
 page.screenshot(path=str(ROOT/'screenshots/keyboard-focus-320.png'))
 r['visible_keyboard_focus']=focus
 # Safety disclosure works by keyboard.
 page.goto(URL+'?screen=welcome&theme=dark')
 page.locator('summary').focus();page.keyboard.press('Enter')
 assert page.locator('details').get_attribute('open') is not None
 assert page.evaluate('EVAL_FIXTURES.bank.warning') in page.locator('details').inner_text()
 r['safety_disclosure_keyboard']='PASS'
 # A long name must not force the completion page wider than its viewport.
 page.goto(URL+'?screen=welcome&theme=light')
 page.get_by_role('button',name='Get started').click()
 page.locator('#name').fill('Alexandriamargueriteelisabethavery')
 page.locator('#mobile').fill('07123456482')
 page.get_by_role('button',name='Continue').click()
 page.locator('#code').fill(page.evaluate('EVAL_FIXTURES.bank.testCode'))
 page.get_by_role('button',name='Confirm code').click()
 assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),'Long first name overflows'
 r['long_name']='PASS: unbroken 34-character name reflows'
 # Cold file loads: observe rendering shifts, without simulated requests.
 page.add_init_script("window.renderShifts=[];new PerformanceObserver(list=>{for(const e of list.getEntries())if(!e.hadRecentInput)window.renderShifts.push(e.value)}).observe({type:'layout-shift',buffered:true});")
 r['initial_layout_shift']={}
 for state in ['welcome','code','help']:
  page.goto(URL+f'?screen={state}&theme=light')
  page.wait_for_function('document.fonts.status === \"loaded\"')
  page.wait_for_timeout(250)
  r['initial_layout_shift'][state]=page.evaluate('window.renderShifts.reduce((a,b)=>a+b,0)')
 browser.close()
(ROOT/'verification/extra-results.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps(r,indent=2))
