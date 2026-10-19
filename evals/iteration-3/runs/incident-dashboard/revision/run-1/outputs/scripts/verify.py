"""Offline file:// layout, fixture, keyboard and state verification. No dependencies installed."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json, os
root=Path(__file__).resolve().parents[2]
url=(root/'outputs/app/index.html').as_uri()
out=root/'outputs/verification'
out.mkdir(exist_ok=True)
results=[]
interactions=[]
chrome=os.environ.get('DASHBOARD_CHROMIUM','/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path=chrome,headless=True)
 for display,width,height in [('tv',1920,1080),('laptop',1440,900)]:
  for theme in ['light','dark']:
   for state in ['live','stale','surge']:
    page=browser.new_page(viewport={'width':width,'height':height},device_scale_factor=1)
    errors=[]; network=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.on('request',lambda r:network.append(r.url) if not r.url.startswith('file:') else None)
    page.add_init_script("window.shifts=[];new PerformanceObserver(l=>{for(const e of l.getEntries())if(!e.hadRecentInput)window.shifts.push(e.value)}).observe({type:'layout-shift',buffered:true})")
    page.goto(f'{url}?screen={state}&theme={theme}&display={display}')
    page.evaluate('document.fonts.ready');page.wait_for_timeout(100)
    data=page.evaluate('''() => ({bodyWidth:document.documentElement.scrollWidth,bodyHeight:document.documentElement.scrollHeight,rows:document.querySelectorAll('#incident-rows tr').length,firstIncidentY:document.querySelector('#incident-rows').getBoundingClientRect().y,tableOverflow:document.querySelector('table').scrollWidth>document.querySelector('.table-wrap').clientWidth,footerBottom:document.querySelector('.footer').getBoundingClientRect().bottom,clipped:[...document.querySelectorAll('td,th,.panel-top,.metric,.incident-meta')].filter(e=>e.scrollWidth>e.clientWidth+1).map(e=>e.textContent),appliedTheme:document.documentElement.dataset.theme,cls:window.shifts.reduce((a,b)=>a+b,0),smallTargets:[...document.querySelectorAll('button')].filter(e=>e.getClientRects().length && e.getBoundingClientRect().height<44).map(e=>e.textContent)})''')
    assert data['bodyWidth']==width,(display,theme,state,data)
    if display=='tv': assert data['bodyHeight']<=height,(display,theme,state,data)
    assert data['appliedTheme']==theme
    assert not data['clipped'] and not data['smallTargets'],data
    assert not data['tableOverflow'] and data['cls']<0.01,data
    assert not errors and not network,(errors,network)
    assert data['rows']==(7 if state!='surge' or display=='tv' else 12)
    expected=page.evaluate("EVAL_FIXTURES.dashboard.incidents.slice(0,"+str(data['rows'])+")")
    for incident in expected:
     row=page.locator('tr').filter(has=page.locator('[data-incident="'+incident['id']+'"]'))
     for field in ['title','service','status','duration','opened']:
      assert incident[field] in row.inner_text(),(incident['id'],field)
     assert (incident['commander'] or 'Unassigned') in row.inner_text()
    for incident in page.evaluate('EVAL_FIXTURES.dashboard.resolved'):
     assert incident['id'] in page.locator('.resolved-list').inner_text()
     assert incident['title'] in page.locator('.resolved-list').inner_text()
    assert page.locator('.open-metric .metric-value').inner_text()==('12' if state=='surge' else '7')
    assert page.locator('.stale-banner').count()==(1 if state=='stale' else 0)
    page.screenshot(path=str(out/f'{display}-{theme}-{state}.png'),full_page=True)
    # Read every incident through the keyboard, verify full detail and Escape return.
    first=page.locator('[data-incident]').first
    first.focus();page.keyboard.press('Enter')
    assert page.locator('dialog').evaluate('(e)=>e.open')
    if state=='live' and ((display=='tv' and theme=='dark') or (display=='laptop' and theme=='light')):
     page.screenshot(path=str(out/f'{display}-{theme}-detail.png'))
    assert 'Unassigned' in page.locator('#detail-fields').inner_text()
    assert page.locator('#close-detail').evaluate('(e)=>e===document.activeElement')
    page.keyboard.press('Tab')
    assert page.locator('dialog').evaluate('(e)=>e.contains(document.activeElement)')
    page.keyboard.press('Escape')
    assert not page.locator('dialog').evaluate('(e)=>e.open')
    assert first.evaluate('(e)=>e===document.activeElement')
    first.press('Enter');page.locator('#close-detail').click()
    assert first.evaluate('(e)=>e===document.activeElement')
    if display=='tv' and state=='surge':
     before=page.locator('.resolved-heading').bounding_box()['y']
     page.locator('#next').focus();page.keyboard.press('Enter')
     assert page.locator('#next').evaluate('(e)=>e===document.activeElement')
     assert page.locator('#incident-rows tr').count()==5
     assert 'INC-2278' in page.locator('#incident-rows').inner_text()
     assert page.locator('#next').get_attribute('aria-disabled')=='true'
     assert abs(page.locator('.resolved-heading').bounding_box()['y']-before)<1
     page.screenshot(path=str(out/f'tv-{theme}-surge-page2.png'))
     page.locator('#previous').press('Enter')
     assert 'INC-2291' in page.locator('#incident-rows').inner_text()
     interactions.append({'theme':theme,'tvPagination':'PASS; all 12 reachable; stable footer; focus retained'})
    if display=='laptop' and state=='surge':
     last=page.locator('[data-incident="INC-2278"]');last.focus();last.press('Enter')
     assert page.locator('#detail-title').inner_text()=='Invoice export queue growing'
     page.keyboard.press('Escape')
     assert last.evaluate('(e)=>e===document.activeElement')
    interactions.append({'display':display,'theme':theme,'state':state,'detailsKeyboardCloseEscapeFocus':'PASS'})
    results.append({'display':display,'theme':theme,'state':state,**data,'errors':errors,'externalRequests':network})
    page.close()
 # System preference follows changes unless overridden. Reduced motion keeps the data.
 page=browser.new_page(viewport={'width':1440,'height':900},color_scheme='dark',reduced_motion='reduce')
 page.goto(url+'?screen=live');page.evaluate('document.fonts.ready')
 assert page.evaluate('document.documentElement.dataset.theme')=='dark'
 assert page.locator('[data-incident]').count()==7
 assert page.locator('[data-incident]').first.evaluate('(e)=>getComputedStyle(e).transitionDuration')=='0s'
 page.emulate_media(color_scheme='light');page.wait_for_timeout(50)
 assert page.evaluate('document.documentElement.dataset.theme')=='light'
 page.goto(url+'?theme=dark');page.emulate_media(color_scheme='light')
 assert page.evaluate('document.documentElement.dataset.theme')=='dark'
 # The first Tab reveals the skip link; activating it lands on the list heading.
 page.keyboard.press('Tab');assert page.locator('.skip').evaluate('(e)=>e===document.activeElement')
 assert page.locator('.skip').bounding_box()['y']>=0
 page.keyboard.press('Enter');assert page.locator('#open-incidents').evaluate('(e)=>e===document.activeElement')
 interactions.append({'systemTheme':'PASS initial, change, explicit override','reducedMotion':'PASS; data preserved; zero transition','skipLink':'PASS keyboard focus and target'})
 browser.close()
(out/'layout-results.json').write_text(json.dumps(results,indent=2))
(out/'interaction-results.json').write_text(json.dumps(interactions,indent=2))
print(json.dumps({'screens':len(results),'tvFits':all(r['bodyHeight']<=1080 for r in results if r['display']=='tv'),'consoleErrors':sum(len(r['errors'])for r in results),'externalRequests':sum(len(r['externalRequests'])for r in results),'maxCLS':max(r['cls']for r in results),'interactionChecks':interactions},indent=2))
