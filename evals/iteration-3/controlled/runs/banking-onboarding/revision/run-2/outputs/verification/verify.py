from pathlib import Path
import json
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
URL=(ROOT/'app/index.html').as_uri()
results={'screens':[], 'checks':[], 'errors':[]}
with sync_playwright() as p:
 b=p.chromium.launch()
 context=b.new_context()
 page=context.new_page()
 page.on('pageerror',lambda e:results['errors'].append(str(e)))
 page.on('request',lambda r:results['errors'].append('Network request: '+r.url) if r.url.startswith(('http:','https:')) else None)
 for w,h in [(390,844),(320,568)]:
  page.set_viewport_size({'width':w,'height':h})
  for theme in ['light','dark']:
   for state in ['welcome','details','details-error','code','code-error','help','done']:
    page.goto(f'{URL}?screen={state}&theme={theme}&display=laptop')
    page.evaluate('document.fonts.ready')
    assert page.locator('#app').count()==1
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'),(w,theme,state,'overflow')
    if state=='help':
     assert page.locator('dialog').evaluate('(d)=>d.open')
     page.keyboard.press('Escape')
     assert page.locator('#open-help').evaluate('(e)=>e===document.activeElement')
     page.locator('#open-help').click()
    if (w==390 and state in ['welcome','details-error','code','help','done'] and theme=='light') or (w==320 and state in ['code-error','help'] and theme=='dark'):
     page.screenshot(path=str(ROOT/f'verification/{state}-{w}-{theme}.png'),full_page=state!='help')
    results['screens'].append({'size':f'{w}x{h}','theme':theme,'state':state,'height':page.evaluate('document.documentElement.scrollHeight')})
 # Main path, invalid input, state retention and no false success.
 page.set_viewport_size({'width':390,'height':844})
 page.goto(URL+'?screen=welcome&theme=light')
 page.locator('#start').click()
 assert page.locator('h1').evaluate('(e)=>e===document.activeElement')
 page.locator('button[type=submit]').click()
 assert page.locator('#name').get_attribute('aria-invalid')=='true'
 assert page.locator('#name').evaluate('(e)=>e===document.activeElement')
 page.locator('#name').fill('Alex Morgan')
 page.locator('#mobile').fill('07123 456482')
 page.locator('button[type=submit]').click()
 assert '482' in page.locator('.intro').inner_text()
 page.locator('#back').click()
 assert page.locator('#name').input_value()=='Alex Morgan'
 assert page.locator('#mobile').input_value()=='07123 456482'
 page.locator('button[type=submit]').click()
 page.locator('#code').fill('000000')
 page.locator('button[type=submit]').click()
 assert 'code-error' in page.url
 assert page.locator('#code').get_attribute('aria-invalid')=='true'
 assert page.locator('#code').evaluate('(e)=>e===document.activeElement')
 page.locator('#no-code').click()
 assert page.locator('dialog').evaluate('(d)=>d.open')
 assert page.locator('#call-help').get_attribute('href')=='tel:08081570192'
 page.locator('#close-help').click()
 assert page.locator('#no-code').evaluate('(e)=>e===document.activeElement')
 assert page.locator('#code').input_value()=='000000'
 test_code=page.evaluate('EVAL_FIXTURES.bank.testCode')
 assert test_code not in page.locator('body').inner_text()
 page.locator('#code').fill(test_code)
 page.locator('button[type=submit]').click()
 assert 'done' in page.url
 assert 'Alex' in page.locator('h1').inner_text()
 page.locator('#finish').click()
 assert 'welcome' in page.url
 results['checks'].append('Full flow, validation, wrong/correct code, back preservation, Help button dismissal and focus restoration')
 # Keyboard-only path.
 page.goto(URL+'?screen=welcome&theme=dark')
 page.keyboard.press('Tab');assert page.locator('#open-help').evaluate('(e)=>e===document.activeElement')
 page.keyboard.press('Tab');assert page.locator('#start').evaluate('(e)=>e===document.activeElement')
 page.keyboard.press('Enter');page.keyboard.press('Tab')
 assert page.locator('#name').evaluate('(e)=>e===document.activeElement')
 page.keyboard.type('Alex Morgan');page.keyboard.press('Tab');page.keyboard.type('+44 7123 456482');page.keyboard.press('Tab');page.keyboard.press('Enter')
 page.keyboard.press('Tab');assert page.locator('#code').evaluate('(e)=>e===document.activeElement')
 page.keyboard.type(test_code);page.keyboard.press('Tab');page.keyboard.press('Enter')
 assert 'done' in page.url
 results['checks'].append('Keyboard-only welcome → details → code → completion, including +44 format')
 # Modal keyboard containment and Escape.
 page.goto(URL+'?screen=help&theme=dark')
 for i in range(8):
  page.keyboard.press('Tab')
  assert page.evaluate('document.querySelector("dialog").contains(document.activeElement)')
 page.keyboard.press('Escape')
 assert page.locator('#open-help').evaluate('(e)=>e===document.activeElement')
 results['checks'].append('Native modal Tab containment, Escape dismissal, direct Help opens over code')
 # System theme + reduced motion + text zoom + larger display queries.
 page.emulate_media(color_scheme='dark',reduced_motion='reduce')
 page.goto(URL+'?screen=code')
 assert page.locator('html').get_attribute('data-theme')=='dark'
 assert page.locator('#code').evaluate('(e)=>getComputedStyle(e).transitionDuration')=='0s'
 page.emulate_media(color_scheme='light')
 page.wait_for_function("document.documentElement.dataset.theme==='light'")
 for display in ['tv','laptop']:
  page.set_viewport_size({'width':1280,'height':900})
  page.goto(URL+f'?screen=help&theme=dark&display={display}')
  assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
 page.set_viewport_size({'width':320,'height':568})
 page.goto(URL+'?screen=details-error&theme=light')
 page.evaluate('document.documentElement.style.fontSize="200%"')
 assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
 page.screenshot(path=str(ROOT/'verification/text-200-percent.png'),full_page=True)
 results['checks'].append('System theme updates, URL theme override, reduced motion, 200% text, tv/laptop queries')
 # Control target audit across states.
 page.evaluate('document.documentElement.style.fontSize="100%"')
 for state in ['welcome','details-error','code-error','help','done']:
  page.goto(URL+f'?screen={state}&theme=light')
  targets=page.locator('button,input,a[href]').evaluate_all('(els)=>els.filter(e=>e.getBoundingClientRect().width>0 && !e.closest("dialog:not([open])")).map(e=>({id:e.id,w:e.getBoundingClientRect().width,h:e.getBoundingClientRect().height}))')
  assert all(t['w']>=44 and t['h']>=44 for t in targets),(state,targets)
 results['checks'].append('Visible controls at least 44×44 CSS px (buttons designed at 52–60 px)')
 b.close()
assert not results['errors'],results['errors']
(ROOT/'verification/results.json').write_text(json.dumps(results,indent=2))
print(json.dumps({'rendered_states':len(results['screens']),'checks':results['checks'],'errors':results['errors']},indent=2))
