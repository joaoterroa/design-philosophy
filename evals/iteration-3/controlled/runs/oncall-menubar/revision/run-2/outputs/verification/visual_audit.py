from pathlib import Path
import json
from PIL import Image, ImageOps, ImageDraw
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[2];O=R/'outputs/verification';URL=(R/'outputs/app/index.html').as_uri()
report=[]
with sync_playwright() as p:
 b=p.chromium.launch();page=b.new_page(viewport={'width':400,'height':680},device_scale_factor=1)
 page.add_init_script("window.__cls=0;new PerformanceObserver(l=>{for(const e of l.getEntries())if(!e.hadRecentInput)window.__cls+=e.value}).observe({type:'layout-shift',buffered:true});")
 for theme in ['light','dark']:
  sheet=Image.new('RGB',(1200,1408),'#cdd0d7');d=ImageDraw.Draw(sheet)
  for i,state in enumerate(['main','compose','pending','offline','empty','accepted']):
   page.goto(URL+f'?screen={state}&theme={theme}')
   page.wait_for_selector('h1')
   shot=page.screenshot()
   import io
   im=Image.open(io.BytesIO(shot)).convert('RGB')
   x=(i%3)*400;y=(i//3)*704
   d.text((x+20,y+4),f'{state} / {theme}',fill='#24272d')
   sheet.paste(im,(x,y+24))
   before=page.locator('#app').bounding_box();page.wait_for_timeout(100);after=page.locator('#app').bounding_box()
   assert before==after
   report.append({'state':state,'theme':theme,'stable_after_render':True,'observed_cls':page.evaluate('window.__cls'),'h1_y':page.locator('h1').bounding_box()['y']})
  sheet.save(O/f'states-{theme}.png')
 # Inspect the non-empty review step and long-note case.
 page.goto(URL+'?screen=compose&theme=light')
 page.get_by_label('Hand over to').select_option(label='Priya Raman')
 page.get_by_label('Handover note').fill('Watch the routing queue. '*10)
 page.get_by_role('button',name='Review handover').click()
 report.append({'review_with_240_characters':page.locator('#app').evaluate('(e)=>({height:e.clientHeight,scroll:e.scrollHeight,width:e.clientWidth,scrollWidth:e.scrollWidth})')})
 page.get_by_role('button',name='Send request',exact=True).focus()
 assert page.get_by_role('button',name='Send request',exact=True).is_visible()
 page.screenshot(path=str(O/'review-note.png'))
 page.goto(URL+'?screen=offline&theme=light');page.get_by_role('button',name='Try again').click()
 report.append({'offline_after_retry':page.locator('#app').evaluate('(e)=>({height:e.clientHeight,scroll:e.scrollHeight})')})
 page.goto(URL+'?screen=accepted&theme=dark')
 page.get_by_role('button',name='Back to schedule').click();page.reload()
 assert page.get_by_role('heading',name='Priya is on call').is_visible()
 assert page.get_by_text('10:00–18:00').is_visible()
 report.append({'accepted_main_reload_preserves_owner_and_cover':True})
 b.close()
(O/'visual-audit.json').write_text(json.dumps(report,indent=2));print(json.dumps(report[-3:],indent=2))
