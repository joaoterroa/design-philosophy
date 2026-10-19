"""Render every direct state from file://; retain selected screenshots and contact sheets."""
from playwright.sync_api import sync_playwright
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw
from io import BytesIO
import math
ROOT=Path(__file__).resolve().parents[1]
BASE=(ROOT/'app/index.html').as_uri()
OUT=ROOT/'screenshots';OUT.mkdir(exist_ok=True)
selected={('main','light',400),('compose','dark',400),('pending','light',400),('live','dark',1920),('surge','light',1440),('welcome','light',390),('code-error','dark',320),('help','light',320)}
groups=[('menu',['main','compose','pending','offline','empty','accepted'],400,680,'laptop',400),('bank-390',['welcome','details','details-error','code','code-error','help','done'],390,844,'laptop',390),('bank-320',['welcome','details','details-error','code','code-error','help','done'],320,568,'laptop',320),('dashboard-tv',['live','stale','surge'],1920,1080,'tv',720),('dashboard-laptop',['live','stale','surge'],1440,900,'laptop',720)]
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True)
 page=browser.new_page()
 for group,states,w,h,display,thumbwidth in groups:
  for theme in ['light','dark']:
   tiles=[]
   for state in states:
    page.set_viewport_size({'width':w,'height':h})
    page.goto(f'{BASE}?screen={state}&theme={theme}&display={display}')
    page.evaluate('document.fonts.ready')
    raw=page.screenshot(full_page=True)
    if (state,theme,w) in selected:(OUT/f'{state}-{theme}-{w}.png').write_bytes(raw)
    # Contact sheets retain the entire page so scrollable content can be inspected.
    img=Image.open(BytesIO(raw)).convert('RGB')
    img=img.resize((thumbwidth,round(img.height*thumbwidth/img.width)))
    tile=Image.new('RGB',(thumbwidth,img.height+28),'#e1e3e7')
    tile.paste(img,(0,28));ImageDraw.Draw(tile).text((8,8),f'{state} / {theme} / {w}x{h}',fill='black');tiles.append(tile)
   cols=3 if len(states)>3 else 1
   rows=math.ceil(len(tiles)/cols);cellh=max(t.height for t in tiles)
   sheet=Image.new('RGB',(cols*thumbwidth,rows*cellh),'#d3d6dc')
   for i,tile in enumerate(tiles):sheet.paste(tile,((i%cols)*thumbwidth,(i//cols)*cellh))
   sheet.save(OUT/f'contact-{group}-{theme}.jpg',quality=88)
 # Real review state, reached through the normal flow.
 page.set_viewport_size({'width':400,'height':680});page.goto(BASE+'?screen=main&theme=light')
 page.get_by_role('button',name='Hand over your shift').click();page.locator('#recipient').select_option('Priya Raman')
 page.get_by_role('button',name='Review handover').click();page.screenshot(path=str(OUT/'review-light-400.png'))
 browser.close()
print('Rendered 52 direct state/size/theme combinations plus handover review. Saved selected screens and full-page contact sheets.')
