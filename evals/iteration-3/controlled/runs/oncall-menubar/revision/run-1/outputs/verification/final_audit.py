from pathlib import Path
from playwright.sync_api import sync_playwright
import json
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'outputs'
url=(OUT/'app/index.html').as_uri()
report={'views':[], 'console_errors':[], 'focus_checks':[], 'layout_shift':[]}
with sync_playwright() as p:
 b=p.chromium.launch(headless=True)
 page=b.new_page(viewport={'width':400,'height':680},device_scale_factor=2)
 page.context.set_offline(True)
 page.on('console',lambda m:report['console_errors'].append(m.text) if m.type=='error' else None)
 page.add_init_script("window.shiftScore=0;new PerformanceObserver(es=>es.getEntries().forEach(e=>{if(!e.hadRecentInput)window.shiftScore+=e.value})).observe({type:'layout-shift',buffered:true})")
 for theme in ['light','dark']:
  for state in ['main','compose','pending','offline','empty','accepted']:
   page.goto(url+f'?screen={state}&theme={theme}')
   page.wait_for_selector('h1')
   data=page.evaluate('''()=>({screen:document.title,heading:document.querySelector('h1').getBoundingClientRect().y,buttons:[...document.querySelectorAll('button,select')].map(e=>({name:e.getAttribute('aria-label')||e.innerText,height:e.getBoundingClientRect().height,width:e.getBoundingClientRect().width})),shift:window.shiftScore})''')
   assert all(x['height']>=36 for x in data['buttons']),data
   report['views'].append({'theme':theme,'state':state,**data})
   page.screenshot(path=str(OUT/'screenshots'/f'{state}-{theme}.png'))
  page.goto(url+f'?screen=compose&theme={theme}')
  page.locator('#recipient').select_option('Priya Raman')
  page.get_by_role('button',name='Review handover').click()
  assert page.locator(':focus').inner_text()=='Ready to hand over?'
  report['focus_checks'].append(theme+': review heading focused')
  page.keyboard.press('Tab')
  assert page.locator(':focus').inner_text()=='Back'
  page.keyboard.press('Tab')
  assert page.locator(':focus').inner_text()=='Send handover request'
  page.screenshot(path=str(OUT/'screenshots'/f'review-{theme}.png'))
  page.get_by_role('button',name='Back',exact=True).click()
  assert page.locator('#recipient').input_value()=='Priya Raman'
  assert page.locator(':focus').get_attribute('id')=='recipient'
  report['focus_checks'].append(theme+': selected recipient and focus retained on Back')
  page.get_by_role('button',name='Cancel',exact=True).click()
  assert page.locator('h1').inner_text()=='You’re on call'
  page.reload();assert page.locator('h1').inner_text()=='You’re on call'
 # Capture a single final contact sheet externally with Pillow.
 b.close()
assert not report['console_errors'],report
(OUT/'verification'/'audit.json').write_text(json.dumps(report,indent=2))
from PIL import Image,ImageOps,ImageDraw
names=['main-light','compose-light','review-light','pending-light','offline-light','empty-light','accepted-light','main-dark','compose-dark','review-dark','pending-dark','offline-dark','empty-dark','accepted-dark']
thumbs=[]
for name in names:
 im=Image.open(OUT/'screenshots'/f'{name}.png').convert('RGB');im.thumbnail((240,408))
 thumb=Image.new('RGB',(240,432),'#e7e9e6');thumb.paste(im,(0,24));ImageDraw.Draw(thumb).text((10,5),name,fill='#242d29');thumbs.append(thumb)
sheet=Image.new('RGB',(240*7,432*2),'white')
for i,im in enumerate(thumbs):sheet.paste(im,((i%7)*240,(i//7)*432))
sheet.save(OUT/'screenshots'/'contact-sheet.png')
print(json.dumps({'views':len(report['views']),'focus_checks':report['focus_checks'],'console_errors':report['console_errors'],'max_layout_shift':max(x['shift'] for x in report['views'])},indent=2))
