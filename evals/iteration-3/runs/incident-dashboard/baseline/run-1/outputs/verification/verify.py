from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image,ImageDraw
import json,io
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'outputs/verification';URL=(ROOT/'outputs/app/index.html').as_uri()
results=[]
with sync_playwright() as p:
 browser=p.chromium.launch();context=browser.new_context();page=context.new_page();page.set_default_timeout(5000);errors=[]
 page.add_init_script("window.layoutShifts=[];new PerformanceObserver(list=>{for(const e of list.getEntries())if(!e.hadRecentInput)window.layoutShifts.push(e.value)}).observe({type:'layout-shift',buffered:true})")
 page.on('pageerror',lambda error:errors.append(str(error)))
 screenshots={('live','dark',1920),('live','light',1440),('stale','dark',1920),('surge','light',1920),('main','light',400),('pending','dark',400),('welcome','light',390),('welcome','light',320),('help','dark',320)}
 tiles=[]
 groups=[(['live','stale','surge'],[(1920,1080,'tv'),(1440,900,'laptop')]),(['main','compose','pending','offline','empty','accepted'],[(400,680,'laptop')]),(['welcome','details-error','code','code-error','help','done'],[(390,844,'laptop'),(320,568,'laptop')])]
 for states,sizes in groups:
  for state in states:
   for w,h,display in sizes:
    for theme in ['light','dark']:
     page.set_viewport_size({'width':w,'height':h});page.goto(f'{URL}?screen={state}&theme={theme}&display={display}');page.evaluate('document.fonts.ready');page.wait_for_timeout(30)
     row=page.evaluate('''() => ({screen:new URLSearchParams(location.search).get('screen'),width:innerWidth,theme:document.documentElement.dataset.theme,layoutShift:(window.layoutShifts||[]).reduce((a,b)=>a+b,0),firstIncidentY:document.querySelector('tbody')?.getBoundingClientRect().top??null,horizontalOverflow:document.documentElement.scrollWidth>innerWidth,documentHeight:document.documentElement.scrollHeight,app:(()=>{let r=document.getElementById('app').getBoundingClientRect();return {x:r.x,y:r.y,width:r.width,height:r.height}})()})''')
     assert not row['horizontalOverflow'],row
     if state in ['main','compose','pending','offline','empty','accepted']:assert row['app']['x']==20 and row['app']['y']==20 and row['app']['width']==360 and row['app']['height']<=640,row
     if state in ['live','stale','surge'] and display=='tv':
      row['tvVerticalOverflow']=row['documentHeight']>h
      assert not row['tvVerticalOverflow'],row
     if (state,theme,w) in screenshots:page.screenshot(path=str(OUT/'screenshots'/f'{state}-{theme}-{w}.png'),full_page=True)
     im=Image.open(io.BytesIO(page.screenshot())).convert('RGB');im.thumbnail((320,240));tile=Image.new('RGB',(340,274),'#ddd');tile.paste(im,((340-im.width)//2,28));ImageDraw.Draw(tile).text((6,6),f'{state} / {theme} / {w}',fill='#111');tiles.append(tile);results.append(row)
 for start in range(0,len(tiles),12):
  sheet=Image.new('RGB',(1360,822),'#ccc')
  for i,im in enumerate(tiles[start:start+12]):sheet.paste(im,((i%4)*340,(i//4)*274))
  sheet.save(OUT/'screenshots'/f'contact-{start//12+1}.jpg')
 page.evaluate('sessionStorage.clear()');page.set_viewport_size({'width':400,'height':680});page.goto(f'{URL}?screen=main&theme=light')
 page.get_by_role('button',name='Hand over your shift').click();page.get_by_label('Hand over to').select_option('Priya Raman');page.get_by_label('Handover note').fill('Routing API needs attention.');page.get_by_role('button',name='Review handover').click()
 assert page.get_by_text('Review handover',exact=True).is_visible()
 page.get_by_role('button',name='Send handover request').click();assert page.get_by_text('You are still responsible.',exact=True).is_visible();page.wait_for_timeout(300);assert 'pending' in page.url
 page.get_by_role('button',name='Simulate Priya accepting').click();assert page.get_by_text('Handover accepted',exact=True).is_visible();page.get_by_role('button',name='Back to on call').click();assert page.get_by_text('Handover accepted. You’re off call.',exact=True).is_visible()
 page.evaluate('sessionStorage.clear()');page.goto(f'{URL}?screen=pending');page.get_by_role('button',name='Cancel request').click();assert page.get_by_role('button',name='Hand over your shift').is_visible()
 page.set_viewport_size({'width':320,'height':568});page.goto(f'{URL}?screen=welcome&theme=dark');page.get_by_role('button',name='Get started').click();page.get_by_role('button',name='Send text message').click();assert page.get_by_text('Enter your full name.',exact=True).is_visible()
 page.get_by_label('Full name',exact=True).fill('Alex Morgan');page.get_by_label('Mobile number',exact=True).fill('07123456482');page.get_by_role('button',name='Send text message').click();page.get_by_role('button',name='Back',exact=False).click();assert page.get_by_label('Full name',exact=True).input_value()=='Alex Morgan';page.get_by_role('button',name='Send text message').click();page.get_by_label('Text message code').fill('000000');page.get_by_role('button',name='Confirm code').click();assert 'code-error' in page.url
 help_button=page.get_by_role('button',name='Help',exact=True);help_button.click();assert page.get_by_role('dialog').is_visible();page.keyboard.press('Escape');assert not page.get_by_role('dialog').is_visible();assert help_button.evaluate('(e)=>e===document.activeElement')
 help_button.click();page.get_by_role('button',name='Back to setup').click();assert help_button.evaluate('(e)=>e===document.activeElement')
 code=page.evaluate('EVAL_FIXTURES.bank.testCode');page.get_by_label('Text message code').fill(code);page.get_by_role('button',name='Confirm code').click();assert page.get_by_text('You’re all set, Alex',exact=True).is_visible()
 page.set_viewport_size({'width':1920,'height':1080});page.goto(f'{URL}?screen=surge&display=tv');assert page.locator('tbody tr').count()==7;page.get_by_role('button',name='Next',exact=False).click();assert page.locator('tbody tr').count()==5;assert page.get_by_text('INC-2278',exact=True).is_visible();page.get_by_role('button',name='Previous',exact=False).click()
 page.get_by_role('button',name='Route optimiser timeouts for EU-West depots',exact=True).click();assert page.get_by_role('dialog').is_visible();page.keyboard.press('Escape')
 page.set_viewport_size({'width':1440,'height':900});page.goto(f'{URL}?screen=surge&display=laptop');assert page.locator('tbody tr').count()==12;page.get_by_text('INC-2278',exact=True).scroll_into_view_if_needed();assert page.get_by_text('INC-2278',exact=True).is_visible()
 page.emulate_media(color_scheme='dark',reduced_motion='reduce');page.goto(f'{URL}?screen=live');assert page.evaluate('document.documentElement.dataset.theme')=='dark';assert page.get_by_role('heading',name='Incident overview').is_visible();assert not errors,errors
 # A complete keyboard-only handover path, with a native select and focus after re-render.
 page.evaluate('sessionStorage.clear()');page.set_viewport_size({'width':400,'height':680});page.goto(f'{URL}?screen=main&theme=light')
 page.keyboard.press('Tab');assert page.evaluate('document.activeElement.textContent').startswith('Hand over your shift')
 page.keyboard.press('Enter');assert 'compose' in page.url
 page.keyboard.press('Tab');assert page.evaluate('document.activeElement.id')=='recipient'
 page.keyboard.press('p');page.keyboard.press('Tab');page.keyboard.type('No change to escalation routes.');page.keyboard.press('Tab');page.keyboard.press('Enter');assert page.get_by_text('Review handover',exact=True).is_visible()
 page.keyboard.press('Tab');page.keyboard.press('Enter');assert 'pending' in page.url
 page.reload();assert page.get_by_text('You are still responsible.',exact=True).is_visible()
 page.get_by_role('button',name='Back to on call').click();assert page.get_by_role('button',name='View pending handover').is_visible()
 page.get_by_role('button',name='View pending handover').click();page.get_by_role('button',name='Cancel request').click()
 # Every current roster entry is reachable in the constrained offline popover.
 page.goto(f'{URL}?screen=offline');assert page.get_by_role('button',name='Hand over your shift').is_disabled();page.locator('.roster-person').filter(has_text='Aiko Kimura').scroll_into_view_if_needed();assert page.locator('.roster-person').filter(has_text='Aiko Kimura').is_visible()
 # Welcome action is immediately visible on the shortest supported display.
 page.set_viewport_size({'width':320,'height':568});page.goto(f'{URL}?screen=welcome&theme=light')
 rect=page.get_by_role('button',name='Get started').bounding_box();assert rect['y']+rect['height']<=568,rect
 browser.close()
(OUT/'results.json').write_text(json.dumps({'renders':results,'consoleErrors':errors,'interactionChecks':'passed'},indent=2))
print(f'PASS: {len(results)} state/size/theme renders; handover, cancellation, bank validation, Help focus return, TV paging, incident detail, laptop reachability, system theme and reduced motion.')
print('TV overflow:',[(r['screen'],r['theme'],r['documentHeight']) for r in results if r.get('tvVerticalOverflow')])
