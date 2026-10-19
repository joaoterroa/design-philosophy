from pathlib import Path
from playwright.sync_api import sync_playwright
import json
root=Path(__file__).resolve().parents[2]
out=root/'outputs/verification'
results=[]
with sync_playwright() as p:
 browser=p.chromium.launch()
 for display,w,h in [('laptop',1440,900),('tv',1920,1080)]:
  for theme in ['light','dark']:
   for state in ['live','stale','surge']:
    page=browser.new_page(viewport={'width':w,'height':h},reduced_motion='reduce')
    errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
    requests=[];page.on('request',lambda r:requests.append(r.url))
    page.goto((root/'outputs/app/index.html').as_uri()+f'?screen={state}&theme={theme}&display={display}')
    page.evaluate('document.fonts.ready')
    count=page.locator('tbody tr').count()
    assert count==(7 if state!='surge' or display=='tv' else 12),(state,display,count)
    assert page.locator('.metric-number').first.inner_text()==('12' if state=='surge' else '7')
    assert page.locator('.notice').count()==(1 if state=='stale' else 0)
    assert page.locator('td.missing').inner_text()=='!Unassigned' or 'Unassigned' in page.locator('td.missing').inner_text()
    assert page.locator('.service').count()==5
    assert page.locator('.resolved-button').count()==2
    overflow=page.evaluate('document.documentElement.scrollWidth>innerWidth')
    assert not overflow
    panel=page.locator('.incident-panel').bounding_box()
    footer=page.locator('.page-footer').bounding_box()
    if display=='tv': assert footer['y']+footer['height']<=h,footer
    page.locator('.incident-button').first.click()
    assert page.locator('dialog').is_visible()
    assert 'Unassigned' in page.locator('dialog').inner_text()
    page.keyboard.press('Escape')
    assert page.locator('.incident-button').first.evaluate('(e)=>e===document.activeElement')
    if display=='tv' and state=='surge':
     page.locator('#next').focus();page.keyboard.press('Enter')
     assert page.locator('tbody tr').count()==5
     assert 'INC-2278' in page.locator('table').inner_text()
     assert page.locator('#previous').evaluate('(e)=>e===document.activeElement')
     page.screenshot(path=str(out/'surge-tv-page2.png')) if theme=='dark' else None
     page.locator('#previous').click()
    if display=='laptop':
     search=page.locator('#search');search.fill('Routing API')
     assert page.locator('tbody tr').count()==(3 if state=='surge' else 2)
     assert search.evaluate('(e)=>e===document.activeElement')
     search.fill('no such incident');assert page.locator('.empty').is_visible()
     search.fill('')
    assert not errors,errors
    assert all(u.startswith('file:') or u.startswith('data:') for u in requests)
    page.screenshot(path=str(out/f'{state}-{display}-{theme}.png'))
    results.append({'screen':state,'display':display,'theme':theme,'rows':count,'panelY':panel['y'],'footerBottom':footer['y']+footer['height'],'horizontalOverflow':overflow,'pageErrors':errors,'networkRequests':0})
    page.close()
 page=browser.new_page(color_scheme='dark')
 page.goto((root/'outputs/app/index.html').as_uri())
 assert page.locator('html').get_attribute('data-theme')=='dark'
 page.emulate_media(color_scheme='light')
 page.wait_for_function("document.documentElement.dataset.theme==='light'")
 browser.close()
(out/'results.json').write_text(json.dumps(results,indent=2))
print('PASS: 12 direct routes, row counts, stale state, pagination, search, modal/Escape/focus, overflow, offline requests, system themes.')
