from pathlib import Path
from playwright.sync_api import sync_playwright
import json
from PIL import Image, ImageDraw
ROOT=Path(__file__).resolve().parents[1]
URL=(ROOT/'app/index.html').as_uri()
SHOTS=ROOT/'screenshots'
SHOTS.mkdir(exist_ok=True)
results={'matrix':[], 'interactions':[], 'console_errors':[], 'external_requests':[]}
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True)
 page=browser.new_page()
 page.on('pageerror',lambda e:results['console_errors'].append(str(e)))
 page.on('request',lambda r:results['external_requests'].append(r.url) if r.url.startswith(('http:','https:')) else None)
 for width,height in [(390,844),(320,568)]:
  for theme in ['light','dark']:
   sheet=Image.new('RGB',(width*3,height*2+64), '#777777')
   for i,state in enumerate(['welcome','details-error','code','code-error','help','done']):
    page.set_viewport_size({'width':width,'height':height})
    page.goto(f'{URL}?screen={state}&theme={theme}&display=laptop')
    page.wait_for_function('document.fonts.status === "loaded"')
    page.evaluate('document.activeElement.blur()')
    size=page.evaluate('({width:document.documentElement.scrollWidth,viewport:innerWidth,height:document.documentElement.scrollHeight})')
    assert size['width']<=width, (state,theme,size)
    assert page.locator('#app').count()==1
    assert page.locator('h1').is_visible()
    if state=='help':assert page.locator('dialog').evaluate('(e)=>e.open')
    for inp in page.locator('input').all():
     assert inp.evaluate('(e)=>!!document.querySelector(`label[for="${e.id}"]`)')
    for el in page.locator('button, input, summary, dialog[open] a').all():
     if el.is_visible():assert el.bounding_box()['height']>=44,(state,el.inner_text())
    tmp=SHOTS/f'.{state}-{theme}-{width}.png'
    page.screenshot(path=str(tmp))
    im=Image.open(tmp).convert('RGB');sheet.paste(im,((i%3)*width,(i//3)*(height+32)+32))
    draw=ImageDraw.Draw(sheet);draw.text(((i%3)*width+8,(i//3)*(height+32)+8),f'{state} / {theme} / {width}',fill='white')
    if (state,theme,width) in [('details-error','light',320),('welcome','light',390),('code-error','light',390),('help','dark',320),('done','dark',390)]:
     page.screenshot(path=str(SHOTS/f'{state}-{theme}-{width}.png'),full_page=state!='help')
    tmp.unlink()
    results['matrix'].append({'state':state,'theme':theme,'width':width,'height':height,'document_height':size['height'],'horizontal_overflow':False})
   sheet.save(SHOTS/f'states-{theme}-{width}.png')
 page.set_viewport_size({'width':390,'height':844})
 page.goto(f'{URL}?screen=welcome&theme=light')
 page.get_by_role('button',name='Get started').click()
 assert page.locator('h1').inner_text()=='Your account details'
 page.get_by_role('button',name='Continue').click()
 assert page.locator('[aria-invalid=true]').count()==2
 assert page.evaluate('document.activeElement.id')=='name'
 page.locator('#name').fill('Alex Morgan')
 page.locator('#mobile').fill('07123456482')
 page.get_by_role('button',name='Continue').click()
 assert '482' in page.locator('main .intro').inner_text()
 page.get_by_role('button',name='Back',exact=True).click()
 assert page.locator('#name').input_value()=='Alex Morgan'
 assert page.locator('#mobile').input_value()=='07123456482'
 page.get_by_role('button',name='Continue').click()
 page.locator('#code').fill('000000')
 page.get_by_role('button',name='Confirm code').click()
 assert 'code-error' in page.url
 assert page.locator('#code-error').is_visible()
 assert page.evaluate('document.activeElement.id')=='code'
 page.get_by_role('button',name='Help',exact=True).click()
 assert page.locator('dialog').evaluate('(e)=>e.open')
 page.keyboard.press('Escape')
 assert not page.locator('dialog').evaluate('(e)=>e.open')
 assert page.evaluate('document.activeElement.id')=='help'
 page.get_by_role('button',name='I haven’t received a code').click()
 page.get_by_role('button',name='Back to setup').click()
 assert page.evaluate('document.activeElement.id')=='code-help'
 code=page.evaluate('EVAL_FIXTURES.bank.testCode')
 assert code not in page.locator('#app').inner_text()
 page.locator('#code').fill(code)
 page.get_by_role('button',name='Confirm code').click()
 assert 'done' in page.url
 page.get_by_role('button',name='Finish',exact=True).click()
 assert 'welcome' in page.url
 results['interactions'].append('Welcome → invalid details → corrected details → code → Back retains details → wrong code blocked → Help Escape and button restore focus → fixture code completes → Finish resets')
 page.goto(f'{URL}?screen=help&theme=dark')
 page.keyboard.press('Tab');assert page.locator('dialog').evaluate('(d)=>d.contains(document.activeElement)')
 page.keyboard.press('Shift+Tab');assert page.locator('dialog').evaluate('(d)=>d.contains(document.activeElement)')
 page.keyboard.press('Escape');assert page.evaluate('document.activeElement.id')=='help'
 assert 'screen=code' in page.url
 assert page.locator('.safety').is_visible()
 page.emulate_media(color_scheme='dark',reduced_motion='reduce')
 page.goto(f'{URL}?screen=welcome')
 assert page.locator('html').get_attribute('data-theme')=='dark'
 page.emulate_media(color_scheme='light')
 page.wait_for_function('document.documentElement.dataset.theme === "light"')
 page.locator('#start').focus();page.keyboard.press('Enter')
 page.keyboard.press('Tab');page.keyboard.type('Alex Morgan')
 page.keyboard.press('Tab');page.keyboard.type('07123456482')
 page.keyboard.press('Tab');page.keyboard.press('Enter')
 assert 'screen=code' in page.url
 assert page.evaluate('getComputedStyle(document.querySelector(".primary")).transitionDuration')=='0s'
 results['interactions'].append('Direct Help overlays code; focus trapped and restored; safety visible; live system-theme response; keyboard-only form flow; reduced motion')
 for state in ['welcome','details-error','code-error','help','done']:
  page.goto(f'{URL}?screen={state}&theme=light')
  page.evaluate('document.documentElement.style.fontSize="200%"')
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),('200% text',state)
 results['interactions'].append('200% text-size reflow without horizontal overflow at 390px')
 browser.close()
assert not results['console_errors'],results['console_errors']
assert not results['external_requests'],results['external_requests']
(ROOT/'verification/results.json').write_text(json.dumps(results,indent=2))
print(json.dumps({'matrix_states':len(results['matrix']),'interactions':results['interactions'],'console_errors':results['console_errors'],'external_requests':results['external_requests']},indent=2))
