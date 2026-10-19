from playwright.sync_api import sync_playwright
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
BASE=(ROOT/'app/index.html').as_uri()
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True)
 page=browser.new_page()
 errors=[]
 page.on('pageerror',lambda error:errors.append(str(error)))
 for screen,theme,w,h,display in [('main','light',400,680,'laptop'),('compose','dark',400,680,'laptop'),('pending','light',400,680,'laptop'),('live','dark',1920,1080,'tv'),('surge','light',1440,900,'laptop'),('welcome','light',390,844,'laptop'),('code-error','dark',320,568,'laptop'),('help','light',320,568,'laptop')]:
  page.set_viewport_size({'width':w,'height':h})
  page.goto(f'{BASE}?screen={screen}&theme={theme}&display={display}')
  page.screenshot(path=str(ROOT/'screenshots'/f'{screen}-{theme}-{w}.png'),full_page=True)
  print(screen,theme,page.evaluate('({width:document.documentElement.scrollWidth,height:document.documentElement.scrollHeight,app:JSON.stringify(document.querySelector("#app").getBoundingClientRect())})'))
 print('ERRORS',errors)
 browser.close()
