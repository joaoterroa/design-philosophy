from playwright.sync_api import sync_playwright
from pathlib import Path
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True)
 page=browser.new_page(viewport={'width':820,'height':950},device_scale_factor=1)
 page.goto(Path('outputs/explorations/compositions.html').resolve().as_uri())
 page.screenshot(path='outputs/verification/compositions.png',full_page=True)
 browser.close()
