from pathlib import Path
import json
from playwright.sync_api import sync_playwright
from PIL import Image, ImageOps, ImageDraw
ROOT=Path(__file__).resolve().parents[1]
BASE=(ROOT/'app/index.html').as_uri()
OUT=ROOT/'verification'
reports=[]
with sync_playwright() as p:
 browser=p.chromium.launch()
 page=browser.new_page(viewport={"width":390,"height":844},device_scale_factor=1)
 errors=[]
 external=[]
 page.on('request',lambda req:external.append(req.url) if req.url.startswith(('https:','http:')) else None)
 page.on('pageerror',lambda e:errors.append(str(e)))
 thumbs=[]
 for width,height in [(390,844),(320,568)]:
  page.set_viewport_size({'width':width,'height':height})
  for theme in ['light','dark']:
   for state in ['welcome','details','details-error','code','code-error','help','done']:
    page.goto(f'{BASE}?screen={state}&theme={theme}')
    page.evaluate('document.fonts.ready')
    info=page.evaluate('''() => ({overflow:document.documentElement.scrollWidth>innerWidth, title:document.title, heading:document.querySelector('h1').getBoundingClientRect().top, dialog:document.querySelector('dialog').open, targets:[...document.querySelectorAll('button,input,a,summary')].filter(e=>e.checkVisibility() && e.getBoundingClientRect().height>0 && (!document.querySelector('dialog').open||e.closest('dialog'))).map(e=>({label:e.textContent.trim()||e.id,h:e.getBoundingClientRect().height,w:e.getBoundingClientRect().width}))})''')
    assert not info['overflow'],(width,theme,state,'horizontal overflow')
    assert state!='help' or info['dialog']
    for t in info['targets']:
     assert t['h']>=48,(width,theme,state,'small target',t)
    # Visible viewport screenshots of every required state, preserved as one contact sheet.
    shot=page.screenshot(full_page=False)
    import io
    im=Image.open(io.BytesIO(shot)).convert('RGB');im.thumbnail((195,422))
    tile=Image.new('RGB',(215,452),'#dddddd');tile.paste(im,((215-im.width)//2,23));ImageDraw.Draw(tile).text((6,5),f'{state} {width} {theme}',fill='black');thumbs.append(tile)
    if (width,theme,state) in [(390,'light','welcome'),(390,'light','details-error'),(390,'light','code'),(390,'dark','code-error'),(390,'light','help'),(390,'dark','done'),(320,'light','welcome'),(320,'dark','help')]:
     page.screenshot(path=str(OUT/f'{state}-{width}-{theme}.png'),full_page=False)
    reports.append({'width':width,'height':height,'theme':theme,'state':state,**info})
 # Main flow, validation, keyboard and Help focus return.
 page.set_viewport_size({'width':390,'height':844})
 page.goto(BASE+'?theme=light')
 page.get_by_role('button',name='Let’s get started').click()
 assert page.locator('h1').evaluate('(e)=>e===document.activeElement')
 page.get_by_role('button',name='Continue',exact=True).click()
 assert page.locator('#full-name').get_attribute('aria-invalid')=='true'
 assert page.locator('#full-name').evaluate('(e)=>e===document.activeElement')
 page.get_by_label('Full name',exact=True).fill('Alex Morgan')
 page.get_by_label('Mobile number',exact=True).fill('07700 900482')
 page.get_by_role('button',name='Continue',exact=True).click()
 assert 'screen=code' in page.url
 assert '482' in page.locator('.intro').inner_text()
 page.get_by_label('Text message code',exact=True).fill('111111')
 page.get_by_role('button',name='Confirm code').click()
 assert 'screen=done' not in page.url
 assert page.locator('#code').get_attribute('aria-invalid')=='true'
 page.get_by_role('button',name='Help',exact=True).click()
 assert page.locator('dialog').evaluate('(d)=>d.open')
 page.keyboard.press('Escape')
 assert not page.locator('dialog').evaluate('(d)=>d.open')
 assert page.locator('#help-open').evaluate('(e)=>e===document.activeElement')
 assert page.locator('#code').input_value()=='111111'
 page.get_by_role('button',name='Help',exact=True).click()
 page.get_by_role('button',name='Back to setup').click()
 assert page.locator('#help-open').evaluate('(e)=>e===document.activeElement')
 page.locator('#code').fill(page.evaluate('EVAL_FIXTURES.bank.testCode'))
 page.get_by_role('button',name='Confirm code').click()
 assert 'screen=done' in page.url
 assert page.locator('.balance').inner_text()==page.evaluate('EVAL_FIXTURES.bank.balance')
 page.get_by_text('Keep your banking safe',exact=True).click()
 assert page.evaluate('EVAL_FIXTURES.bank.warning') in page.locator('details').inner_text()
 page.get_by_role('button',name='Back',exact=True).click()
 assert 'screen=code' in page.url
 page.get_by_role('button',name='Change mobile number').click()
 assert page.get_by_label('Full name',exact=True).input_value()=='Alex Morgan'
 assert page.get_by_label('Mobile number',exact=True).input_value()=='07700 900482'
 # Entire main flow using keyboard only.
 page.goto(BASE+'?theme=dark')
 page.keyboard.press('Tab');assert page.locator('#help-open').evaluate('(e)=>e===document.activeElement')
 page.keyboard.press('Tab');page.keyboard.press('Enter')
 page.keyboard.press('Tab');page.keyboard.type('Alex Morgan')
 page.keyboard.press('Tab');page.keyboard.type('07700900482')
 page.keyboard.press('Tab');page.keyboard.press('Enter')
 page.keyboard.press('Tab');page.keyboard.type(page.evaluate('EVAL_FIXTURES.bank.testCode'))
 page.keyboard.press('Tab');page.keyboard.press('Enter')
 assert 'screen=done' in page.url
 # System preference + manual override and reduced motion.
 page.emulate_media(color_scheme='dark',reduced_motion='reduce')
 page.goto(BASE+'?screen=code')
 assert page.locator('html').get_attribute('data-theme')=='dark'
 assert page.locator('.primary').first.evaluate('(e)=>getComputedStyle(e).transitionDuration')=='0s'
 page.goto(BASE+'?screen=code&theme=light')
 assert page.locator('html').get_attribute('data-theme')=='light'
 # Text enlargement: essential content remains reachable with no horizontal scrolling.
 page.set_viewport_size({'width':320,'height':568})
 for state in ['welcome','details-error','code-error','help','done']:
  page.goto(BASE+f'?screen={state}&theme=dark')
  page.evaluate("document.documentElement.style.fontSize='200%'")
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),('200% overflow',state)
  if state=='help':
   page.locator('#help-close').scroll_into_view_if_needed()
   page.get_by_role('button',name='Back to setup').click()
   assert not page.locator('dialog').evaluate('(d)=>d.open')
  elif state.startswith('code'):
   page.locator('.safety').scroll_into_view_if_needed()
   assert page.locator('.safety').is_visible()
 assert not external,external
 assert not errors,errors
 browser.close()
 sheet=Image.new('RGB',(7*215,4*452),'#dddddd')
 for i,t in enumerate(thumbs):sheet.paste(t,((i%7)*215,(i//7)*452))
 sheet.save(OUT/'all-states-contact-sheet.jpg',quality=90)
 (OUT/'results.json').write_text(json.dumps({'states':reports,'javascriptErrors':errors,'interactionChecks':'passed','keyboardFlow':'passed','systemThemeAndReducedMotion':'passed','textEnlargement200Percent':'passed','externalNetworkRequests':external},indent=2))
 print('PASS: 28 state/size/theme combinations; main flow, invalid details, wrong and correct code, Back, Help button/Escape/focus return, keyboard-only flow, system theme and reduced motion. No JS errors or horizontal overflow.')
