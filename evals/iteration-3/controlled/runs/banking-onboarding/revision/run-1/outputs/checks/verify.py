from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image,ImageOps,ImageDraw
import json
root=Path(__file__).resolve().parents[2]
app=(root/'outputs/app/index.html').as_uri()
shots=root/'outputs/screenshots'
results={'states':[], 'interactions':[], 'console_errors':[], 'network_requests':[]}
thumbs=[]
with sync_playwright() as p:
 browser=p.chromium.launch()
 page=browser.new_page()
 page.add_init_script("window.__cls=0;new PerformanceObserver(list=>{for(const e of list.getEntries())if(!e.hadRecentInput)window.__cls+=e.value}).observe({type:'layout-shift',buffered:true});")
 page.on('pageerror',lambda e:results['console_errors'].append(str(e)))
 page.on('request',lambda r:results['network_requests'].append(r.url) if r.url.startswith(('http:','https:')) else None)
 for w,h in [(390,844),(320,568)]:
  for theme in ['light','dark']:
   for screen in ['welcome','details','details-error','code','code-error','help','done']:
    page.set_viewport_size({'width':w,'height':h})
    page.goto(f'{app}?screen={screen}&theme={theme}&display=laptop')
    page.evaluate('document.fonts.ready')
    page.wait_for_timeout(50)
    metrics=page.evaluate('''() => ({cls:window.__cls,overflow:document.documentElement.scrollWidth>innerWidth,heading:document.querySelector('h1').getBoundingClientRect().top,dialogOpen:document.querySelector('dialog').open,smallTargets:[...document.querySelectorAll('button,input,a')].filter(x=>x.getBoundingClientRect().height>0&&x.getBoundingClientRect().height<48).map(x=>x.textContent)})''')
    assert metrics['cls']<0.1,(screen,w,theme,metrics)
    assert not metrics['overflow'],(screen,w,theme,metrics)
    assert not metrics['smallTargets'],(screen,w,theme,metrics)
    assert metrics['dialogOpen']==(screen=='help')
    if screen=='help':
     assert page.locator('#close-help').evaluate('(e)=>{const r=e.getBoundingClientRect();return r.top>=0&&r.bottom<=innerHeight}')
    results['states'].append({'screen':screen,'width':w,'height':h,'theme':theme,**metrics})
    path=shots/f'{screen}-{w}-{theme}.png'
    page.screenshot(path=str(path),full_page=(screen!='help'))
    im=Image.open(path).convert('RGB');im.thumbnail((195,600))
    tile=Image.new('RGB',(215,im.height+35),'#e0e0e0');tile.paste(im,(10,30));ImageDraw.Draw(tile).text((8,8),f'{screen} {w} {theme}',fill='black');thumbs.append(tile)
 # Interaction: main path, invalid data, correct code, backwards preservation.
 page.set_viewport_size({'width':390,'height':844})
 page.goto(app+'?screen=welcome&theme=light')
 page.get_by_role('button',name='Get started').click()
 assert 'screen=details' in page.url
 page.get_by_role('button',name='Continue',exact=False).click()
 assert page.locator('#full-name').get_attribute('aria-invalid')=='true'
 assert page.locator('#mobile').get_attribute('aria-invalid')=='true'
 assert page.locator('#full-name').evaluate('(e)=>e===document.activeElement')
 bank=page.evaluate('EVAL_FIXTURES.bank')
 page.get_by_label('Full name').fill(bank['customer'])
 page.get_by_label('Mobile number',exact=True).fill('07700 900482')
 page.get_by_role('button',name='Continue',exact=False).click()
 assert 'screen=code' in page.url
 page.get_by_role('button',name='Back',exact=True).click()
 assert page.get_by_label('Full name').input_value()==bank['customer']
 assert page.get_by_label('Mobile number',exact=True).input_value()=='07700 900482'
 page.get_by_role('button',name='Continue',exact=False).click()
 page.get_by_label('Security code',exact=True).fill('111111')
 page.get_by_role('button',name='Confirm code').click()
 assert 'screen=code-error' in page.url
 assert page.get_by_label('Security code',exact=True).get_attribute('aria-invalid')=='true'
 assert page.locator('#security-code').evaluate('(e)=>e===document.activeElement')
 # Modal: Escape, explicit dismiss, focus return, tab containment.
 for dismiss in ['escape','button']:
  page.get_by_role('button',name='Help',exact=True).click()
  assert page.locator('dialog').evaluate('(d)=>d.open')
  for _ in range(5):
   page.keyboard.press('Tab')
   assert page.evaluate("document.querySelector('dialog').contains(document.activeElement)")
  if dismiss=='escape': page.keyboard.press('Escape')
  else: page.get_by_role('button',name='Back to setup').click()
  page.wait_for_function("new URLSearchParams(location.search).get('screen')==='code-error'")
  assert not page.locator('dialog').evaluate('(d)=>d.open')
  assert page.locator('#help-button').evaluate('(e)=>e===document.activeElement')
 page.get_by_label('Security code',exact=True).fill(bank['testCode'])
 page.get_by_role('button',name='Confirm code').click()
 assert 'screen=done' in page.url
 assert page.locator('h1').evaluate('(e)=>e===document.activeElement')
 page.get_by_role('button',name='Finish',exact=False).click()
 assert 'screen=welcome' in page.url
 results['interactions']+=['Welcome → details → validation errors → valid details → code → wrong code rejected → fixture code → done → finish','Back preserves details','Help Escape and button dismiss; focus returns; Tab remains in dialog','Focus goes to first invalid input or new screen heading']
 # Direct help and trigger-specific focus return.
 page.goto(app+'?screen=help&theme=dark&display=tv')
 page.keyboard.press('Escape')
 page.wait_for_function("new URLSearchParams(location.search).get('screen')==='code'")
 assert 'screen=code' in page.url
 assert page.locator('#help-button').evaluate('(e)=>e===document.activeElement')
 page.get_by_role('button',name='Haven’t received a code?').click()
 page.get_by_role('button',name='Back to setup').click()
 page.wait_for_function("new URLSearchParams(location.search).get('screen')==='code'")
 assert page.locator('#code-help').evaluate('(e)=>e===document.activeElement')
 assert page.locator('a[href^="tel:"]').get_attribute('href')=='tel:'+bank['helpPhone'].replace(' ','')
 results['interactions'].append('Direct help opens over code; phone link uses fixture; alternate trigger regains focus')
 # Keyboard-only successful journey.
 page.goto(app+'?screen=welcome&theme=light')
 page.keyboard.press('Tab');page.keyboard.press('Tab');page.keyboard.press('Enter')
 assert 'screen=details' in page.url
 page.keyboard.press('Tab');page.keyboard.type(bank['customer']);page.keyboard.press('Tab');page.keyboard.type('07700900482');page.keyboard.press('Tab');page.keyboard.press('Enter')
 assert 'screen=code' in page.url
 page.keyboard.press('Tab');page.keyboard.type(bank['testCode']);page.keyboard.press('Tab');page.keyboard.press('Enter')
 assert 'screen=done' in page.url
 results['interactions'].append('Entire successful setup completed by keyboard')
 # Visible keyboard focus, nonempty invalid input, details Help continuity.
 page.goto(app+'?screen=details&theme=light')
 page.get_by_label('Full name').fill('123')
 page.get_by_label('Mobile number',exact=True).fill('not a number')
 page.get_by_role('button',name='Continue',exact=False).click()
 assert 'screen=details-error' in page.url
 assert page.locator('#name-error').is_visible() and page.locator('#mobile-error').is_visible()
 page.keyboard.press('Tab')
 focus=page.evaluate('({width:getComputedStyle(document.activeElement).outlineWidth,style:getComputedStyle(document.activeElement).outlineStyle})')
 assert focus['width']=='3px' and focus['style']=='solid'
 page.get_by_role('button',name='Help',exact=True).click()
 page.get_by_role('button',name='Back to setup').click()
 page.wait_for_function("new URLSearchParams(location.search).get('screen')==='details-error'")
 assert page.get_by_label('Mobile number',exact=True).input_value()=='not a number'
 assert 'screen=details-error' in page.url
 results['interactions'].append('Nonempty invalid details rejected; visible 3px keyboard focus; details preserved through Help')
 # System theme + reduced motion, display URL supported, wide layouts.
 page.emulate_media(color_scheme='dark',reduced_motion='reduce')
 page.goto(app+'?screen=code&display=tv')
 assert page.locator('html').get_attribute('data-theme')=='dark'
 assert page.locator('.primary').first.evaluate('(e)=>getComputedStyle(e).transitionDuration')=='0s'
 for display in ['tv','laptop']:
  page.set_viewport_size({'width':1280,'height':800})
  page.goto(app+f'?screen=details-error&theme=light&display={display}')
  assert not page.evaluate('document.documentElement.scrollWidth>innerWidth')
 results['interactions']+=['System dark preference and reduced motion verified','Both display parameters accepted; centered readable form at 1280×800']
 # 200% text scaling with mobile reflow; no hidden or horizontally clipped page.
 page.set_viewport_size({'width':320,'height':568})
 for screen in ['welcome','details-error','code-error','help','done']:
  page.goto(app+f'?screen={screen}&theme=light')
  page.evaluate("document.documentElement.style.fontSize='200%'")
  assert not page.evaluate('document.documentElement.scrollWidth>innerWidth'),('200% text',screen)
  if screen=='help':assert page.locator('#close-help').evaluate('(e)=>e.getBoundingClientRect().bottom<=innerHeight')
 results['interactions'].append('200% text scaling at 320×568: no page overflow; help dismiss remains visible')
 assert not results['console_errors'],results['console_errors']
 assert not results['network_requests'],results['network_requests']
 browser.close()
# Contact sheet preserves every direct state at both mobile sizes in both themes.
cols=7;rows=4;cellw=215;cellh=max(i.height for i in thumbs)
canvas=Image.new('RGB',(cols*cellw,rows*cellh),'#d0d0d0')
for i,im in enumerate(thumbs):canvas.paste(im,((i%cols)*cellw,(i//cols)*cellh))
canvas.save(shots/'all-states.png')
# Keep a small representative set alongside the contact sheet.
keep={'welcome-390-light.png','details-error-320-light.png','code-error-390-dark.png','help-320-dark.png','done-390-light.png','all-states.png'}
for path in shots.glob('*.png'):
 if path.name not in keep:path.unlink()
(root/'outputs/checks/results.json').write_text(json.dumps(results,indent=2))
print(f"PASS: {len(results['states'])} direct state renders; {len(results['interactions'])} interaction groups; zero network or JavaScript errors.")
