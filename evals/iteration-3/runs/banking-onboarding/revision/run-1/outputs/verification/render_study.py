from playwright.sync_api import sync_playwright
from pathlib import Path
with sync_playwright() as p:
 browser=p.chromium.launch()
 page=browser.new_page(viewport={"width":840,"height":900},device_scale_factor=1)
 page.goto(Path('outputs/research/compositions.html').resolve().as_uri())
 page.screenshot(path='outputs/research/compositions.png',full_page=True)
 browser.close()
