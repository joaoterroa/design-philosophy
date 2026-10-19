from playwright.sync_api import sync_playwright
from pathlib import Path
import json
from PIL import Image, ImageDraw
from io import BytesIO
root=Path(__file__).resolve().parents[2]
results=[]
contact=Image.new("RGB",(1600,1320),"#e6eaee")
contact_draw=ImageDraw.Draw(contact)
shot_index=0
keep={"live-light-tv","stale-dark-tv","surge-light-laptop"}
with sync_playwright() as p:
 b=p.chromium.launch()
 for display,size in [('tv',(1920,1080)),('laptop',(1440,900))]:
  for theme in ['light','dark']:
   for state in ['live','stale','surge']:
    page=b.new_page(viewport={'width':size[0],'height':size[1]},device_scale_factor=1,reduced_motion='reduce')
    errors=[];requests=[]
    page.on('pageerror',lambda err:errors.append(str(err)))
    page.on('request',lambda req:requests.append(req.url))
    page.goto((root/'outputs/app/index.html').as_uri()+f'?screen={state}&theme={theme}&display={display}')
    page.evaluate('document.fonts.ready')
    shot_name=f'{state}-{theme}-{display}'
    shot=page.screenshot(full_page=True)
    if shot_name in keep:(root/f'outputs/screenshots/{shot_name}.png').write_bytes(shot)
    thumb=Image.open(BytesIO(shot)).convert('RGB');thumb.thumbnail((386,400))
    col=shot_index%4;row=shot_index//4
    contact.paste(thumb,(col*400+7,row*440+28));contact_draw.text((col*400+7,row*440+7),shot_name,fill='#12355b')
    shot_index+=1
    info=page.evaluate('''()=>({width:innerWidth,height:innerHeight,scrollWidth:document.documentElement.scrollWidth,scrollHeight:document.documentElement.scrollHeight,firstIncident:document.querySelector('tbody tr')?.getBoundingClientRect().top,lastIncident:document.querySelector('tbody tr:last-child')?.getBoundingClientRect().bottom,rows:document.querySelectorAll('tbody tr').length,open:document.querySelector('#open').textContent,theme:document.documentElement.dataset.theme,font:getComputedStyle(document.body).fontFamily})''')
    assert info['scrollWidth']<=size[0],info
    assert info['open']==('12' if state=='surge' else '7'),info
    assert not errors,errors
    assert all(x.startswith('file:') for x in requests),requests
    assert info['theme']==theme
    if display=='tv':
     assert info['rows']==7,info
     assert info['scrollHeight']<=size[1],info
    else:
     assert info['rows']==(12 if state=='surge' else 7),info
    if state=='stale':
     assert page.get_by_role('status').filter(has_text='Data is stale').count()==1
     assert page.locator('.dot').count()==0
    if state=='surge' and display=='tv':
     page.get_by_role('button',name='Next incident page').click()
     assert page.locator('tbody tr').count()==5
     assert page.locator('tbody').inner_text().find('INC-2278')>=0
     assert page.locator('#prev').evaluate('(e)=>e===document.activeElement')
     page.get_by_role('button',name='Previous incident page').click()
     assert page.locator('tbody tr').count()==7
    page.get_by_role('button',name='Resolved 2').click()
    assert page.locator('tbody tr').count()==2
    assert 'INC-2288' in page.locator('tbody').inner_text()
    page.locator('[data-incident="INC-2288"]').click()
    assert page.locator('dialog').evaluate('(e)=>e.open')
    assert 'Yesterday 15:30' in page.locator('dialog').inner_text()
    page.keyboard.press('Escape')
    assert not page.locator('dialog').evaluate('(e)=>e.open')
    assert page.locator('[data-incident="INC-2288"]').evaluate('(e)=>e===document.activeElement')
    page.get_by_role('button',name=f'Open incidents {info["open"]}').click()
    page.locator('[data-incident="INC-2291"]').click()
    assert 'Unassigned' in page.locator('dialog').inner_text()
    page.get_by_role('button',name='Close incident details').click()
    if display=='laptop':
     page.get_by_role('searchbox',name='Search incidents').fill('Rotterdam')
     assert page.locator('tbody tr').count()==1
     assert page.get_by_role('searchbox').evaluate('(e)=>e===document.activeElement')
     page.get_by_role('searchbox').fill('zzzz')
     assert page.get_by_text('No matching incidents').count()==1
     page.get_by_role('button',name='Clear filters').click()
     assert page.get_by_role('searchbox').evaluate('(e)=>e===document.activeElement')
     page.get_by_label('Filter by severity').focus()
     page.get_by_label('Filter by severity').select_option('1')
     assert page.locator('tbody tr').count()==1
     assert page.get_by_label('Filter by severity').evaluate('(e)=>e===document.activeElement')
    results.append({'state':state,'theme':theme,'display':display,**info,'errors':errors,'externalRequests':len([x for x in requests if not x.startswith('file:')]),'interactions':'passed'})
    page.close()
 page=b.new_page(color_scheme='dark')
 page.goto((root/'outputs/app/index.html').as_uri())
 assert page.evaluate('document.documentElement.dataset.theme')=='dark'
 page.emulate_media(color_scheme='light')
 page.wait_for_function("document.documentElement.dataset.theme === 'light'")
 b.close()
(root/'outputs/verification/results.json').write_text(json.dumps(results,indent=2))
contact.save(root/'outputs/screenshots/state-matrix.jpg')
print(json.dumps(results,indent=2))
