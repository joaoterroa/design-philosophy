"""Exercise primary flows without mouse clicks or programmatic focus changes."""
from pathlib import Path
from playwright.sync_api import sync_playwright, expect
import json
ROOT=Path(__file__).resolve().parents[1];BASE=(ROOT/'app/index.html').as_uri()
def tab_to(page, selector):
 for _ in range(20):
  if page.evaluate('(s)=>document.activeElement.matches(s)',selector):return
  page.keyboard.press('Tab')
 raise AssertionError('Keyboard could not reach '+selector)
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True);page=browser.new_page(viewport={'width':400,'height':680})
 page.goto(BASE+'?screen=main&theme=dark')
 tab_to(page,'[data-action="compose"]')
 assert page.evaluate('getComputedStyle(document.activeElement).outlineStyle')=='solid'
 page.keyboard.press('Enter');tab_to(page,'#recipient');page.keyboard.press('p')
 assert page.locator('#recipient').input_value()=='Priya Raman'
 page.keyboard.press('Tab');page.keyboard.type('Check routing queue.');page.keyboard.press('Tab');page.keyboard.press('Enter')
 expect(page.get_by_role('heading',name='Ready to hand over?')).to_be_visible()
 tab_to(page,'[data-action="send"]');page.keyboard.press('Enter')
 expect(page.get_by_role('heading',name='Waiting for Priya')).to_be_visible()
 tab_to(page,'[data-action="cancel-request"]');page.keyboard.press('Enter')
 expect(page.get_by_role('heading',name='You’re on call')).to_be_visible()
 page.set_viewport_size({'width':320,'height':568});page.goto(BASE+'?screen=welcome&theme=light')
 tab_to(page,'[data-action="details"]');page.keyboard.press('Enter')
 tab_to(page,'#full-name');page.keyboard.type('Alex Morgan');page.keyboard.press('Tab');page.keyboard.type('07700 900482')
 page.keyboard.press('Tab');page.keyboard.press('Enter')
 tab_to(page,'#sms-code');page.keyboard.type('000000');page.keyboard.press('Enter')
 expect(page.locator('#sms-code')).to_be_focused()
 page.keyboard.press('Shift+Tab');expect(page.get_by_role('button',name='Help',exact=True)).to_be_focused()
 page.keyboard.press('Enter');expect(page.locator('dialog')).to_be_visible()
 for _ in range(5):
  page.keyboard.press('Tab');assert page.evaluate("!!document.activeElement.closest('dialog')")
 page.keyboard.press('Escape');expect(page.get_by_role('button',name='Help',exact=True)).to_be_focused()
 tab_to(page,'#sms-code');page.keyboard.press('Meta+A');page.keyboard.type(page.evaluate('EVAL_FIXTURES.bank.testCode'));page.keyboard.press('Enter')
 expect(page.get_by_role('heading',name='You’re all set, Alex')).to_be_visible()
 page.set_viewport_size({'width':1440,'height':900});page.goto(BASE+'?screen=surge&display=laptop');page.keyboard.press('End');page.wait_for_function('scrollY+innerHeight>=document.documentElement.scrollHeight-1')
 assert page.locator('.incident').last.evaluate('(e)=>{const r=e.getBoundingClientRect();return r.top>=0&&r.bottom<=innerHeight}')
 browser.close()
report={'passed':True,'flows':['keyboard-only handover choose/review/send/cancel','visible focus','keyboard-only banking details/wrong code/correct code','modal Tab containment and Escape focus return','laptop last incident reachable by keyboard scroll']}
(ROOT/'verification/keyboard-results.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
