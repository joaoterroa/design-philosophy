from playwright.sync_api import sync_playwright
from pathlib import Path
import json
from PIL import Image, ImageDraw
ROOT=Path(__file__).resolve().parents[1]
URL=(ROOT/'app/index.html').as_uri()
results=[]
with sync_playwright() as p:
 b=p.chromium.launch()
 for display,w,h in [('laptop',1440,900),('tv',1920,1080)]:
  for screen in ['live','stale','surge']:
   for theme in ['light','dark']:
    page=b.new_page(viewport={'width':w,'height':h},reduced_motion='reduce')
    errors=[]
    external=[]
    page.on('request',lambda r:external.append(r.url) if r.url.startswith(('http:','https:')) else None)
    page.add_init_script("window.layoutShift=0;new PerformanceObserver(list=>{for(const e of list.getEntries())if(!e.hadRecentInput)window.layoutShift+=e.value}).observe({type:'layout-shift',buffered:true})")
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.goto(f'{URL}?screen={screen}&theme={theme}&display={display}')
    page.evaluate('document.fonts.ready')
    page.screenshot(path=str(ROOT/f'verification/{screen}-{theme}-{display}.png'))
    metrics=page.evaluate('''() => ({width:document.documentElement.scrollWidth,height:document.documentElement.scrollHeight,tableY:document.querySelector('table').getBoundingClientRect().top,tableBottom:document.querySelector('table').getBoundingClientRect().bottom,asideBottom:document.querySelector('aside').getBoundingClientRect().bottom,rows:document.querySelectorAll('#rows tr').length,theme:document.documentElement.dataset.theme, fonts:document.fonts.check('16px Plex'),layoutShift:window.layoutShift})''')
    assert metrics['width']==w,metrics
    assert metrics['rows']==(7 if display=='tv' or screen!='surge' else 12),metrics
    assert not errors,errors
    assert not external,external
    facts=page.evaluate('window.EVAL_FIXTURES.dashboard')
    expected=facts['incidents'][:12 if screen=='surge' else 7]
    initial=expected[:7] if display=='tv' else expected
    for row,fact in zip(page.locator('#rows tr').all(),initial):
     text=row.inner_text()
     for key in ['id','title','service','status','duration','opened']:
      assert fact[key] in text,(key,fact,text)
     assert (fact['commander'] or 'Unassigned') in text
    assert page.locator('.metric-value').all_text_contents()==[str(len(expected)),facts['mttr'],str(facts['pages']),facts['slo']]
    assert page.locator('.resolved-item').count()==2
    for item,fact in zip(page.locator('.resolved-item').all(),facts['resolved']):
     for key in ['title','id','service','duration','status']:
      assert fact[key] in item.inner_text()
    for service in facts['services']:
     assert any(service['name'] in t and str(service['value']) in t for t in page.locator('.service-row').all_text_contents())
    assert page.locator('#search').bounding_box()['height']>=44
    assert page.locator('#severity').bounding_box()['height']>=44
    if display=='tv':assert metrics['height']<=h,metrics
    page.locator('[data-incident="INC-2291"]').click()
    assert page.locator('dialog').is_visible()
    assert page.locator('dialog').inner_text().find('09:42')>=0
    assert page.locator('dialog .missing').inner_text()=='Unassigned'
    page.keyboard.press('Escape')
    assert not page.locator('dialog').is_visible()
    assert page.evaluate('document.activeElement.dataset.incident')=='INC-2291'
    page.locator('#search').fill('NO MATCH')
    assert page.locator('#empty').is_visible()
    assert page.evaluate('document.activeElement.id')=='search'
    page.locator('#search').fill('')
    page.locator('#severity').select_option('2')
    assert page.locator('#rows tr').count()==2
    page.locator('#severity').focus()
    assert page.evaluate('document.activeElement.id')=='severity'
    page.locator('#severity').select_option('all')
    if display=='tv' and screen=='surge':
     page.locator('#next').click()
     assert page.locator('#rows tr').count()==5
     assert page.locator('[data-incident="INC-2278"]').is_visible()
     if theme=='light':page.screenshot(path=str(ROOT/'verification/surge-light-tv-page2.png'))
     assert page.evaluate('document.activeElement.id')=='prev'
     page.locator('#prev').click()
     assert page.locator('#rows tr').count()==7
    if screen=='stale':
     assert page.locator('.stale-banner').is_visible()
     assert 'Live' not in page.locator('.freshness').inner_text()
    page.locator('#theme').click()
    assert page.evaluate('document.documentElement.dataset.theme')!=theme
    assert 'theme=' in page.url
    results.append(dict(screen=screen,display=display,errors=errors,**metrics))
    page.close()
 # system theme fallback
 for theme in ['light','dark']:
  page=b.new_page(color_scheme=theme)
  page.goto(URL)
  assert page.evaluate('document.documentElement.dataset.theme')==theme
  page.emulate_media(color_scheme='light' if theme=='dark' else 'dark')
  page.wait_for_function("document.documentElement.dataset.theme !== '"+theme+"'")
  page.close()
 # Keyboard-only path from skip link through filters and incident details.
 page=b.new_page(viewport={'width':1440,'height':900})
 page.goto(f'{URL}?screen=surge&theme=dark&display=laptop')
 page.keyboard.press('Tab')
 assert page.locator('.skip').evaluate('(e)=>e===document.activeElement')
 page.keyboard.press('Enter')
 assert page.evaluate('document.activeElement.id')=='incidents'
 page.keyboard.press('Tab')
 assert page.evaluate('document.activeElement.id')=='search'
 page.keyboard.type('Routing')
 assert page.locator('#rows tr').count()==3
 page.keyboard.press('Tab')
 assert page.evaluate('document.activeElement.id')=='severity'
 page.keyboard.press('Tab')
 assert page.evaluate('document.activeElement.dataset.incident')=='INC-2291'
 page.keyboard.press('Enter')
 assert page.locator('dialog').is_visible()
 page.keyboard.press('Escape')
 assert page.evaluate('document.activeElement.dataset.incident')=='INC-2291'
 page.locator('#search').fill('')
 last=page.locator('[data-incident="INC-2278"]')
 last.focus()
 assert last.is_visible()
 page.keyboard.press('Enter')
 assert 'Invoice export queue growing' in page.locator('dialog').inner_text()
 page.keyboard.press('Escape')
 page.locator('[data-incident="INC-2287"]').focus()
 page.keyboard.press('Enter')
 assert 'Yesterday 11:02' in page.locator('dialog').inner_text()
 page.keyboard.press('Escape')
 page.locator('#display').focus()
 page.keyboard.press('Enter')
 page.wait_for_url(lambda url:'display=tv' in url)
 assert 'screen=surge' in page.url and 'theme=dark' in page.url
 page.close()
 b.close()
(ROOT/'verification/results.json').write_text(json.dumps(results,indent=2))
print(json.dumps(results,indent=2))

# Keep a small set of full-size screenshots plus a contact sheet of the complete matrix.
canvas=Image.new('RGB',(1920,1560),'#102235')
draw=ImageDraw.Draw(canvas)
for row,(display,theme) in enumerate([('laptop','light'),('laptop','dark'),('tv','light'),('tv','dark')]):
 for col,screen in enumerate(['live','stale','surge']):
  path=ROOT/f'verification/{screen}-{theme}-{display}.png'
  im=Image.open(path).convert('RGB')
  im.thumbnail((640,360))
  x,y=col*640,row*390
  draw.text((x+8,y+5),f'{screen} / {theme} / {display}',fill='white')
  canvas.paste(im,(x,y+25))
canvas.save(ROOT/'verification/state-matrix.png')
keep={'live-light-tv.png','stale-dark-tv.png','surge-dark-laptop.png'}
for path in (ROOT/'verification').glob('*-*-*.png'):
 if path.name not in keep and path.name!='surge-light-tv-page2.png':path.unlink()
