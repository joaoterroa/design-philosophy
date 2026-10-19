from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw
import io,json
R=Path(__file__).resolve().parents[1]
audit=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless=True)
 page=b.new_page()
 for width,height in [(390,844),(320,568)]:
  for theme in ['light','dark']:
   images=[]
   for state in ['welcome','details','details-error','code','code-error','help','done']:
    page.set_viewport_size({'width':width,'height':height})
    page.goto((R/'app/index.html').as_uri()+f'?screen={state}&theme={theme}')
    page.evaluate('document.fonts.ready')
    metrics=page.evaluate('''()=>({h1Y:document.querySelector('h1').getBoundingClientRect().top,scrollHeight:document.documentElement.scrollHeight,targets:[...document.querySelectorAll('button,input,a')].filter(e=>e.checkVisibility()).map(e=>({name:e.textContent||e.id,width:e.getBoundingClientRect().width,height:e.getBoundingClientRect().height}))})''')
    assert all(t['height']>=44 and t['width']>=44 for t in metrics['targets']),metrics
    if state=='welcome':
     assert page.locator('main .primary').evaluate('(e)=>e.getBoundingClientRect().bottom<=innerHeight'),'Welcome action below fold'
    audit.append({'state':state,'width':width,'theme':theme,**metrics})
    im=Image.open(io.BytesIO(page.screenshot(full_page=True))).convert('RGB')
    im.thumbnail((195,750))
    images.append((state,im))
    if (width,theme,state) in [(320,'dark','help'),(320,'light','welcome')]:
     page.screenshot(path=str(R/f'verification/screenshots/{state}-{width}-{theme}.png'),full_page=True)
   sheet=Image.new('RGB',(7*211,max(i.height for _,i in images)+38),'#dededb')
   d=ImageDraw.Draw(sheet)
   for i,(state,im) in enumerate(images):
    d.text((i*211+8,8),state,fill='#182631')
    sheet.paste(im,(i*211+8,30))
   sheet.save(R/f'verification/screenshots/audit-{width}-{theme}.jpg',quality=88)
 # Focus visibility and render evidence on actual focus, at required mobile size.
 page.set_viewport_size({'width':320,'height':568})
 page.goto((R/'app/index.html').as_uri()+'?screen=welcome&theme=light')
 page.keyboard.press('Tab')
 assert page.locator('#help-trigger').evaluate("e=>getComputedStyle(e).outlineStyle")=='solid'
 # enlarged text across each state, both themes
 for theme in ['light','dark']:
  for state in ['welcome','details','details-error','code','code-error','help','done']:
   page.goto((R/'app/index.html').as_uri()+f'?screen={state}&theme={theme}')
   page.evaluate("document.documentElement.style.fontSize='200%'")
   assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),f'200% overflow {state} {theme}'
 b.close()
(R/'verification/layout.json').write_text(json.dumps(audit,indent=2))
print('PASS: targets >=44px, visible focus, 200% reflow all states/themes; four visual contact sheets saved')
