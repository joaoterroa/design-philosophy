from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image,ImageOps,ImageDraw
import io,json
root=Path(__file__).resolve().parents[1]
url=(root/'app/index.html').as_uri()
with sync_playwright() as p:
 b=p.chromium.launch()
 page=b.new_page(viewport={'width':320,'height':568})
 page.goto(url+'?screen=welcome&theme=light')
 print(page.locator('#start').bounding_box())
 page.screenshot(path=str(root/'verification/welcome-320-light.png'),full_page=True)
 # Contact sheets retain every state and both themes at actual viewport dimensions before downscaling for review.
 for width,height in [(320,568),(390,844)]:
  page.set_viewport_size({'width':width,'height':height})
  sheet=Image.new('RGB',(7*220,2*(int(height*220/width)+28)),'#ddd')
  draw=ImageDraw.Draw(sheet)
  for row,theme in enumerate(['light','dark']):
   for col,state in enumerate(['welcome','details','details-error','code','code-error','help','done']):
    page.goto(url+f'?screen={state}&theme={theme}')
    page.evaluate('document.fonts.ready')
    page.evaluate('window.scrollTo(0,0)')
    im=Image.open(io.BytesIO(page.screenshot(full_page=False))).convert('RGB')
    im.thumbnail((220,1000))
    y=row*(int(height*220/width)+28)
    sheet.paste(im,(col*220,y+28));draw.text((col*220+4,y+6),state+' / '+theme,fill='#111')
  sheet.save(root/f'verification/states-{width}-contact.png')
 page.goto(url+'?screen=help&theme=dark');page.set_viewport_size({'width':320,'height':568});page.screenshot(path=str(root/'verification/help-320-dark.png'))
 page.goto(url+'?screen=details-error&theme=light');page.set_viewport_size({'width':390,'height':844});page.evaluate('window.scrollTo(0,0)');page.screenshot(path=str(root/'verification/details-error-390-light.png'),full_page=True)
 b.close()
