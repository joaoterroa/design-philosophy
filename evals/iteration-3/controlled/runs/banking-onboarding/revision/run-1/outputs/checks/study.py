from playwright.sync_api import sync_playwright
from pathlib import Path
root=Path(__file__).resolve().parents[2]
with sync_playwright() as p:
 browser=p.chromium.launch()
 page=browser.new_page(viewport={'width':390,'height':844},device_scale_factor=1)
 for v in ['a','b']:
  page.goto((root/'outputs/review/compositions.html').as_uri()+'?variant='+v)
  page.screenshot(path=str(root/('outputs/review/composition-'+v+'.png')),full_page=True)
  page.get_by_role('button',name='Get started').click()
  page.screenshot(path=str(root/('outputs/review/composition-'+v+'-details.png')),full_page=True)
 browser.close()
