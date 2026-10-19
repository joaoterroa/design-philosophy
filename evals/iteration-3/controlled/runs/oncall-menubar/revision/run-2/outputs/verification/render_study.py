from pathlib import Path
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[2]
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True)
 page=browser.new_page(viewport={"width":800,"height":760},device_scale_factor=1)
 page.goto((root/'outputs/exploration/compositions.html').as_uri())
 page.screenshot(path=str(root/'outputs/verification/compositions.png'))
 browser.close()
