from pathlib import Path
import json,io
from PIL import Image,ImageDraw
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'outputs/verification'
BASE=(ROOT/'outputs/app/index.html').as_uri()
results=[]
contact=Image.new("RGB",(1440,1360),"#e8edf1");draw=ImageDraw.Draw(contact)
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True)
 for display,w,h in [('tv',1920,1080),('laptop',1440,900)]:
  for theme in ['light','dark']:
   for state in ['live','stale','surge']:
    page=browser.new_page(viewport={'width':w,'height':h},device_scale_factor=1,color_scheme=theme,reduced_motion='reduce')
    errors=[];network=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.on('request',lambda r:network.append(r.url) if not r.url.startswith('file:') else None)
    page.add_init_script('window.__cls=0;new PerformanceObserver(list=>{for(const e of list.getEntries())if(!e.hadRecentInput)window.__cls+=e.value}).observe({type:"layout-shift",buffered:true})')
    page.goto(f'{BASE}?screen={state}&theme={theme}&display={display}')
    page.evaluate('document.fonts.ready')
    page.evaluate('()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))')
    initial_layout_shift=page.evaluate('window.__cls')
    expected=12 if state=='surge' else 7
    assert page.locator('#open').inner_text()==str(expected)
    assert page.locator('#incident-rows tr').count()==(min(expected,7) if display=='tv' else expected)
    source=page.evaluate('EVAL_FIXTURES.dashboard.incidents')[:expected]
    for i,incident in enumerate(source[:7] if display=='tv' else source):
     text=page.locator('#incident-rows tr').nth(i).inner_text()
     for key in ['id','title','service','status','opened','duration']:
      assert incident[key] in text,(key,incident['id'])
     assert (incident['commander'] or 'Unassigned') in text
    for button in page.locator('.incident-button:visible').all():
     assert button.bounding_box()['height']>=44
    initial_table_y=page.locator('table').bounding_box()['y']
    assert page.locator('.commander-missing').first.inner_text()=='Unassigned'
    assert page.locator('.resolved-item').count()==2
    assert page.locator('.service').count()==5
    if state=='stale':
     assert 'Updates interrupted' in page.locator('.statusbar').inner_text()
     assert '09:42' in page.locator('.statusbar').inner_text()
    if display=='tv' and state=='surge':
     before_resolved_y=page.locator('.resolved').bounding_box()['y']
     page.locator('#next').focus();page.keyboard.press('Enter');assert page.locator('#incident-rows tr').count()==5
     assert abs(page.locator('.resolved').bounding_box()['y']-before_resolved_y)<1
     if theme=='dark':page.screenshot(path=str(OUT/'tv-surge-page-two-dark.png'))
     assert page.locator('#incident-rows').inner_text().find('INC-2278')>=0
     page.locator('#previous').click()
    if display=='laptop':
     page.locator('#search').fill('scanner');assert page.locator('#incident-rows tr').count()==(2 if state=='surge' else 1)
     assert page.locator('#search').evaluate('(e)=>e===document.activeElement')
     page.locator('#search').fill('no match at all');assert page.locator('#empty').is_visible()
     page.locator('#clear').click();assert page.locator('#search').evaluate('(e)=>e===document.activeElement')
     page.locator('#severity').select_option('1');assert page.locator('#incident-rows tr').count()==1
     page.locator('#severity').select_option('all')
    page.locator('[data-incident="INC-2291"]').click()
    assert page.locator('dialog').is_visible()
    assert 'Unassigned' in page.locator('dialog').inner_text()
    page.keyboard.press('Escape');assert not page.locator('dialog').is_visible()
    assert page.locator('[data-incident="INC-2291"]').evaluate('(e)=>e===document.activeElement')
    page.locator('[data-incident="INC-2288"]').click();assert 'Yesterday 15:30' in page.locator('dialog').inner_text();page.keyboard.press('Escape')
    page.evaluate('()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))')
    page.evaluate('document.activeElement.blur();window.scrollTo(0,0)')
    page.wait_for_function('window.scrollY===0')
    dims=page.evaluate('''()=>({width:innerWidth,scrollWidth:document.documentElement.scrollWidth,height:innerHeight,scrollHeight:document.documentElement.scrollHeight,tableY:document.querySelector('table').getBoundingClientRect().top,footerBottom:document.querySelector('footer').getBoundingClientRect().bottom})''')
    assert dims['scrollWidth']<=w
    if display=='tv':assert dims['scrollHeight']<=h, dims
    assert not errors,errors
    assert not network,network
    if (display,state,theme) in [('tv','live','dark'),('laptop','surge','light'),('tv','stale','light'),('tv','surge','dark')]:
     page.screenshot(path=str(OUT/f'{display}-{state}-{theme}.png'),full_page=True)
    shot=Image.open(io.BytesIO(page.screenshot()));shot.thumbnail((470,300))
    x=(len(results)%3)*480;y=(len(results)//3)*340
    draw.text((x+8,y+6),f'{display} {state} {theme}',fill='#12355b');contact.paste(shot,(x+5,y+30))
    results.append(dict(initialLayoutShift=initial_layout_shift,layoutShiftDuringScript=page.evaluate('window.__cls'),initialTableY=initial_table_y,display=display,theme=theme,state=state,errors=errors,network=network,**dims))
    page.close()
 page=browser.new_page(viewport={'width':1440,'height':900},color_scheme='dark');page.goto(BASE);assert page.locator('html').get_attribute('data-theme')=='dark';page.emulate_media(color_scheme='light');page.wait_for_function("document.documentElement.dataset.theme==='light'")
 page.keyboard.press('Tab');assert page.locator('.skip').evaluate('(e)=>e===document.activeElement');page.keyboard.press('Enter');page.keyboard.press('Tab');assert page.locator('#search').evaluate('(e)=>e===document.activeElement')
 page.keyboard.press('Tab');page.keyboard.press('Tab');page.keyboard.press('Enter');assert page.locator('dialog').is_visible();page.keyboard.press('Escape')
 page.goto(f'{BASE}?screen=stale&theme=dark&display=laptop');page.locator('[data-incident="INC-2291"]').click();page.screenshot(path=str(OUT/'laptop-stale-dialog-dark.png'))
 browser.close()
contact.save(OUT/'state-contact-sheet.jpg')
(OUT/'results.json').write_text(json.dumps(results,indent=2))
print(f'PASS: {len(results)} state/theme/display combinations; fixture counts, search, filters, TV pagination, incident dialogs, Escape and focus restoration, system theme, keyboard skip, offline requests, overflow.');print(json.dumps(results,indent=2))
