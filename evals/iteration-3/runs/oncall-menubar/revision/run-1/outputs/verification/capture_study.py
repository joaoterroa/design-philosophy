from pathlib import Path
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1]
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True)
    page=browser.new_page(viewport={"width":820,"height":830},device_scale_factor=1)
    page.goto((root/'research/compositions.html').as_uri())
    page.screenshot(path=str(root/'verification/screenshots/compositions.png'),full_page=True)
    browser.close()
