from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image,ImageOps,ImageDraw
import json
root=Path(__file__).resolve().parents[2];out=root/'outputs/verification'
metrics=[]
with sync_playwright() as p:
 b=p.chromium.launch()
 for display,w,h in [('tv',1920,1080),('laptop',1440,900)]:
  page=b.new_page(viewport={'width':w,'height':h})
  page.add_init_script("window.shifts=[];new PerformanceObserver(l=>l.getEntries().forEach(e=>{if(!e.hadRecentInput)shifts.push(e.value)})).observe({type:'layout-shift',buffered:true})")
  page.goto((root/'outputs/app/index.html').as_uri()+f'?screen=surge&display={display}&theme=dark')
  page.evaluate('document.fonts.ready');page.wait_for_timeout(150)
  if display=='tv':assert page.evaluate('document.documentElement.scrollHeight<=innerHeight')
  assert all(h>=44 for h in page.locator('button:visible,input:visible').evaluate_all('(els)=>els.map(e=>e.getBoundingClientRect().height)'))
  if display=='laptop':
   expected=page.evaluate('EVAL_FIXTURES.dashboard.incidents')
   for i in expected:
    row=page.locator('tr').filter(has=page.locator(f'[data-id="{i["id"]}"]'))
    text=row.inner_text()
    for k in ['title','service','status','opened','duration']:
     assert i[k] in text.replace('\n',' '),(k,i['id'])
   page.locator('[data-id="INC-2278"]').scroll_into_view_if_needed()
   page.screenshot(path=str(out/'surge-laptop-bottom.png'))
  for i in page.evaluate('EVAL_FIXTURES.dashboard.resolved'):
   page.locator(f'[data-id="{i["id"]}"]').click()
   text=page.locator('dialog').inner_text()
   for k in ['title','service','status','opened','duration']:assert i[k] in text
   page.keyboard.press('Tab');assert page.locator('dialog').evaluate('(e)=>e.contains(document.activeElement)')
   page.keyboard.press('Escape')
  metrics.append({'display':display,'measuredCLS':sum(page.evaluate('window.shifts')),'targetHeightMinimum':44,'resolvedDetails':'passed','tvDocumentOverflow':False if display=='tv' else 'intentional page scroll'})
  page.close()
 b.close()
(out/'extended-results.json').write_text(json.dumps(metrics,indent=2))
files=[out/f'{s}-{d}-{t}.png' for d in ['tv','laptop'] for t in ['light','dark'] for s in ['live','stale','surge']]
canvas=Image.new('RGB',(1200,4*250),'#dce2e8');draw=ImageDraw.Draw(canvas)
for n,f in enumerate(files):
 im=Image.open(f);im.thumbnail((390,220));x=(n%3)*400;y=(n//3)*250;canvas.paste(im,(x,y+24));draw.text((x+5,y+5),f.stem,fill='#12355b')
canvas.save(out/'contact-sheet.jpg')
print(json.dumps(metrics))
