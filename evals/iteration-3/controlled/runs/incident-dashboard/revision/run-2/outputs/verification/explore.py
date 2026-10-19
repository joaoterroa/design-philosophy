from playwright.sync_api import sync_playwright
from pathlib import Path
root=Path(__file__).resolve().parents[2]
with sync_playwright() as p:
 browser=p.chromium.launch()
 page=browser.new_page(viewport={'width':1920,'height':1080})
 page.goto((root/'dashboard/index.html').as_uri())
 page.screenshot(path=str(root/'outputs/verification/baseline-tv.png'))
 print('Baseline table:',page.locator('table').bounding_box())
 for mode in ['table','board']:
  page.goto((root/'outputs/exploration/compare.html').as_uri()+'?'+mode)
  page.screenshot(path=str(root/f'outputs/exploration/{mode}.png'))
 browser.close()
