from pathlib import Path
from playwright.sync_api import sync_playwright
import json
root=Path(__file__).resolve().parents[2]
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless=True)
 page=browser.new_page(viewport={'width':1920,'height':1080},device_scale_factor=1)
 page.goto((root/'dashboard/index.html').as_uri());page.screenshot(path=str(root/'outputs/research/baseline-tv.png'))
 print(json.dumps(page.evaluate("({firstIncidentY:document.querySelector('table').getBoundingClientRect().y, fontSize:getComputedStyle(document.querySelector('td')).fontSize,bodyHeight:document.body.scrollHeight})")))
 for layout in ['incident','metrics']:
  page.goto((root/'outputs/research/compositions.html').as_uri()+'?layout='+layout);page.screenshot(path=str(root/f'outputs/research/{layout}-tv.png'))
 browser.close()
