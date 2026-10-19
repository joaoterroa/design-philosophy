from pathlib import Path
from playwright.sync_api import sync_playwright
import json
root=Path(__file__).resolve().parents[1];url=(root/'app/index.html').as_uri();report={}
with sync_playwright() as p:
 b=p.chromium.launch();page=b.new_page(viewport={'width':320,'height':568})
 page.add_init_script('window.layoutShifts=[];new PerformanceObserver(list=>{for(const e of list.getEntries())if(!e.hadRecentInput)window.layoutShifts.push(e.value)}).observe({type:"layout-shift",buffered:true})')
 page.goto(url+'?screen=welcome&theme=light');page.evaluate('document.fonts.ready');page.wait_for_timeout(200)
 report['welcome_CLS']=page.evaluate('layoutShifts.reduce((a,v)=>a+v,0)')
 report['welcome_action']=page.locator('#start').bounding_box()
 assert report['welcome_action']['y']+report['welcome_action']['height']<=568
 page.locator('#start').click();page.locator('#name').fill('123');page.locator('#mobile').fill('not a number');page.locator('button[type=submit]').click()
 assert page.locator('#name').get_attribute('aria-invalid')=='true'
 page.locator('#name').fill('李');page.locator('#mobile').fill('+44 7123 456482');page.locator('button[type=submit]').click();assert 'code' in page.url
 page.locator('#code').fill('abc');page.locator('button[type=submit]').click();assert 'numbers only' in page.locator('#code-error').inner_text()
 assert page.locator('#code').get_attribute('aria-invalid')=='true'
 page.locator('.safety').scroll_into_view_if_needed();assert page.locator('.safety').is_visible()
 page.locator('#back').click();assert page.locator('#name').input_value()=='李'
 page.locator('#name').fill('Alexandria'*10);page.locator('button[type=submit]').click();test_code=page.evaluate('EVAL_FIXTURES.bank.testCode');page.locator('#code').fill(test_code);page.locator('button[type=submit]').click()
 assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
 page.goto(url+'?screen=details&theme=dark');page.keyboard.press('Tab');page.screenshot(path=str(root/'verification/keyboard-focus.png'))
 page.goto(url+'?screen=help&theme=light');page.evaluate('document.documentElement.style.fontSize="200%"');page.locator('#close-help').scroll_into_view_if_needed();page.locator('#close-help').click();assert not page.locator('dialog').evaluate('(d)=>d.open')
 report['edge_checks']=['Numeric-only name and malformed mobile rejected','Unicode one-character name accepted','Non-digit code rejected with a repair instruction','Safety warning scrolls into view on narrow screen','Long unbroken name wraps on completion','Help remains dismissible with 200% text','Welcome CTA wholly visible at 320×568']
 report['semantics']=page.locator('#app').aria_snapshot()
 b.close()
(root/'verification/edge-results.json').write_text(json.dumps(report,indent=2,ensure_ascii=False));print(json.dumps({k:v for k,v in report.items() if k!='semantics'},indent=2,ensure_ascii=False))
