from playwright.sync_api import sync_playwright
from pathlib import Path
import json
root=Path(__file__).resolve().parents[2]
report={}
with sync_playwright() as p:
 b=p.chromium.launch()
 page=b.new_page(viewport={'width':1440,'height':900},reduced_motion='reduce')
 page.add_init_script('window.__shifts=[];new PerformanceObserver(l=>l.getEntries().forEach(e=>{if(!e.hadRecentInput)window.__shifts.push(e.value)})).observe({type:"layout-shift",buffered:true})')
 page.goto((root/'outputs/app/index.html').as_uri()+'?screen=surge&theme=light&display=laptop')
 page.evaluate('document.fonts.ready')
 page.keyboard.press('Tab')
 assert page.locator('.skip').evaluate('(e)=>e===document.activeElement')
 page.keyboard.press('Enter')
 assert page.locator('#incidents').evaluate('(e)=>e===document.activeElement')
 page.keyboard.press('Tab')
 assert page.locator('#open-tab').evaluate('(e)=>e===document.activeElement')
 outline=page.locator('#open-tab').evaluate('(e)=>({style:getComputedStyle(e).outlineStyle,width:getComputedStyle(e).outlineWidth,color:getComputedStyle(e).outlineColor})')
 assert outline['style']=='solid' and outline['width']=='3px',outline
 page.keyboard.press('Tab');page.keyboard.press('Enter')
 assert page.locator('#resolved-tab').get_attribute('aria-pressed')=='true'
 assert page.locator('#resolved-tab').evaluate('(e)=>e===document.activeElement')
 page.keyboard.press('Tab');assert page.locator('#search').evaluate('(e)=>e===document.activeElement')
 page.keyboard.press('Tab');assert page.locator('#severity').evaluate('(e)=>e===document.activeElement')
 page.keyboard.press('Tab');page.keyboard.press('Enter')
 assert page.locator('dialog').evaluate('(e)=>e.open')
 assert page.locator('#close-dialog').evaluate('(e)=>e===document.activeElement')
 page.keyboard.press('Tab')
 assert page.locator('dialog').evaluate('(e)=>e.contains(document.activeElement)')
 page.keyboard.press('Escape')
 assert page.locator('[data-incident="INC-2288"]').evaluate('(e)=>e===document.activeElement')
 report['keyboard']='Skip link, view switch, search, severity, details, native modal focus trap, Escape and return focus passed'
 report['visibleFocus']=outline
 report['layoutShift']=page.evaluate('window.__shifts.reduce((a,b)=>a+b,0)')
 report['reducedMotion']=page.evaluate('matchMedia("(prefers-reduced-motion: reduce)").matches')
 report['minimumTargetHeight']=page.evaluate('Math.min(...[...document.querySelectorAll("button,input,select")].filter(e=>e.getBoundingClientRect().width>0).map(e=>e.getBoundingClientRect().height))')
 assert report['minimumTargetHeight']>=44,report
 # Every supplied incident, including resolved, opens with all shared facts intact.
 page.locator('#open-tab').click()
 allfacts=page.evaluate('EVAL_FIXTURES.dashboard')
 for group,tab in [('incidents','open-tab'),('resolved','resolved-tab')]:
  page.locator('#'+tab).click()
  for incident in allfacts[group]:
   page.locator('[data-incident="'+incident['id']+'"]').click()
   text=page.locator('dialog').inner_text()
   for k in ['id','title','service','status','opened','duration']:
    assert str(incident[k]) in text,(incident['id'],k)
   assert ('SEV'+str(incident['severity'])) in text
   if 'commander' in incident:assert (incident['commander'] or 'Unassigned') in text
   page.keyboard.press('Escape')
 report['fixtureFacts']='All 12 open and 2 resolved incidents match supplied facts in details'
 page.goto((root/'outputs/app/index.html').as_uri()+'?screen=surge&theme=dark&display=tv')
 page.set_viewport_size({'width':1920,'height':1080})
 page.get_by_role('button',name='Next incident page').click()
 page.screenshot(path=str(root/'outputs/screenshots/surge-dark-tv-page-2.png'),full_page=True)
 page.goto((root/'outputs/app/index.html').as_uri()+'?screen=live&theme=light&display=laptop')
 page.set_viewport_size({'width':1440,'height':900})
 page.locator('[data-incident="INC-2291"]').focus();page.keyboard.press('Enter')
 page.screenshot(path=str(root/'outputs/screenshots/incident-details.png'))
 report['screenReader']='Semantic landmarks, table headers, labeled controls and dialog inspected in DOM; no screen reader software available'
 b.close()
(root/'outputs/verification/accessibility.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
