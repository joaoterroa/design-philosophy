from playwright.sync_api import sync_playwright
from pathlib import Path
root=Path(__file__).resolve().parents[2]
with sync_playwright() as p:
 browser=p.chromium.launch()
 page=browser.new_page(viewport={"width":860,"height":910},device_scale_factor=1)
 page.goto((root/'outputs/review/compositions.html').as_uri())
 page.screenshot(path=str(root/'outputs/screenshots/compositions.png'),full_page=True)
 browser.close()
