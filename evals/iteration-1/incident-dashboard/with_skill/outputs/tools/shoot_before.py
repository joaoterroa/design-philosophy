import sys, json
from playwright.sync_api import sync_playwright
O=sys.argv[1]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/opt/pw-browsers/chromium', args=['--headless=new'])
    for w,h,name in [(1920,1080,'tv-1920x1080'),(1440,900,'laptop-1440x900'),(1280,720,'laptop-1280x720')]:
        pg=b.new_page(viewport={'width':w,'height':h})
        pg.goto('file://'+O+'/dashboard/index.html')
        pg.screenshot(path=f'{O}/screenshots/before/{name}.png')
        m=pg.evaluate("""()=>{const r=s=>{const e=document.querySelector(s);if(!e)return null;const b=e.getBoundingClientRect();return [Math.round(b.top),Math.round(b.bottom)]};
          const rows=[...document.querySelectorAll('tr')].map(t=>Math.round(t.getBoundingClientRect().top));
          return {docH:document.documentElement.scrollHeight, table:r('table'), sev1Row:rows[1], h1:r('h1'), big:getComputedStyle(document.querySelector('.big')).fontSize, td:getComputedStyle(document.querySelector('td')).fontSize, oncall:r('.wide:nth-of-type(6)')}}""")
        print(name, json.dumps(m))
    b.close()
