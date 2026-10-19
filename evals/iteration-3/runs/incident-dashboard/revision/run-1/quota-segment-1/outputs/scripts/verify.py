from pathlib import Path
from playwright.sync_api import sync_playwright
import json
root=Path(__file__).resolve().parents[2]
url=(root/'outputs/app/index.html').as_uri()
results=[]
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless=True)
 for display,width,height in [('tv',1920,1080),('laptop',1440,900)]:
  for theme in ['light','dark']:
   for state in ['live','stale','surge']:
    page=browser.new_page(viewport={'width':width,'height':height},device_scale_factor=1)
    errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
    page.goto(f'{url}?screen={state}&theme={theme}&display={display}')
    page.evaluate('document.fonts.ready');page.wait_for_timeout(100)
    data=page.evaluate('''() => ({bodyWidth:document.documentElement.scrollWidth,bodyHeight:document.documentElement.scrollHeight,rows:document.querySelectorAll('#incident-rows tr').length,firstIncidentY:document.querySelector('#incident-rows').getBoundingClientRect().y,tableOverflow:document.querySelector('table').scrollWidth>document.querySelector('.table-wrap').clientWidth,footerBottom:document.querySelector('.footer').getBoundingClientRect().bottom,clipped:[...document.querySelectorAll('td,th,.panel-top,.metric')].filter(e=>e.scrollWidth>e.clientWidth+1).map(e=>e.textContent),theme:document.documentElement.dataset.theme})''')
    assert data['bodyWidth']==width,(display,theme,state,data)
    assert not errors,errors
    assert data['rows']==(7 if state!='surge' or display=='tv' else 12)
    page.screenshot(path=str(root/f'outputs/verification/{display}-{theme}-{state}.png'),full_page=True)
    results.append({'display':display,'theme':theme,'state':state,**data,'errors':errors})
    page.close()
 browser.close()
(root/'outputs/verification/layout-results.json').write_text(json.dumps(results,indent=2))
print(json.dumps(results,indent=2))
