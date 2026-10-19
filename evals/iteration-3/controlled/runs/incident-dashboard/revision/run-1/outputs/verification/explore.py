from playwright.sync_api import sync_playwright
from pathlib import Path
root=Path(__file__).resolve().parents[2]
with sync_playwright() as p:
 b=p.chromium.launch()
 page=b.new_page(viewport={'width':1920,'height':1080},device_scale_factor=1)
 for name,path in [('baseline','dashboard/index.html'),('incident-first','outputs/review/alternatives.html'),('metrics-first','outputs/review/alternatives.html?metrics')]:
  page.goto('file://'+str(root/path));page.screenshot(path=str(root/'outputs/review'/f'{name}.png'),full_page=True)
  print(name,page.evaluate('({height:document.documentElement.scrollHeight,firstRow:document.querySelector("tr, .row")?.getBoundingClientRect().top})'))
 b.close()
