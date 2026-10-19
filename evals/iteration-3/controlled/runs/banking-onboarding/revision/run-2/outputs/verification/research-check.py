from playwright.sync_api import sync_playwright
from pathlib import Path
import json
root=Path(__file__).resolve().parents[1]
report=[]
with sync_playwright() as p:
 b=p.chromium.launch();page=b.new_page(viewport={'width':390,'height':844})
 for v in ['a','b']:
  page.goto((root/'research/compositions.html').as_uri()+'?v='+v);page.evaluate('document.fonts.ready')
  page.screenshot(path=str(root/f'research/composition-{v}.png'),full_page=True)
  initial=page.locator('h1:visible').inner_text()
  page.locator('.primary:visible').click();page.evaluate('document.fonts.ready')
  report.append({'variant':v,'initialHeading':initial,'nextHeading':page.locator('h1').inner_text(),'nextURL':page.url.split('?')[-1]})
  page.screenshot(path=str(root/f'research/composition-{v}-next.png'))
 b.close()
(root/'research/comparison.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
