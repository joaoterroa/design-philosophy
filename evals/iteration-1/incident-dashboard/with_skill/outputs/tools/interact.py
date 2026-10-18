from playwright.sync_api import sync_playwright
import sys; O=sys.argv[1]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/opt/pw-browsers/chromium', args=['--headless=new'])
    pg=b.new_page(viewport={'width':1440,'height':900})
    errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto('file://'+O+'/app/index.html?state=live&theme=light')
    pg.wait_for_timeout(2500)
    print('freshness after 2.5s:', pg.inner_text('#freshness'))
    seq=[]
    for i in range(10):
        pg.keyboard.press('Tab')
        seq.append(pg.evaluate("()=>{const a=document.activeElement;return (a.dataset&&a.dataset.key)||a.getAttribute('aria-label')||a.id||a.tagName}"))
    print('tab order:', seq)
    # focus a row, then re-render via state change programmatically, check focus kept
    pg.focus('[data-key="INC-2290"]')
    pg.evaluate("NW_load('live')")
    print('focus after re-render:', pg.evaluate("document.activeElement.dataset.key"))
    o=pg.evaluate("()=>{const a=document.querySelector('[data-key=\"INC-2290\"]');const cs=getComputedStyle(a);return cs.outlineStyle+' '+cs.outlineWidth+' '+cs.outlineColor}")
    print('focus ring:', o)
    pg.keyboard.press('Tab'); 
    # tooltip on a column via focus
    pg.focus('.col-hit'); print('tooltip on focus:', pg.is_visible('#tip'), pg.inner_text('#tip'))
    pg.screenshot(path=O+'/screenshots/desk-keyboard-tooltip-light-1440.png')
    pg.select_option('#state-select','stale'); print('url after state switch:', pg.url.split('?')[1], '| freshness:', pg.inner_text('#freshness'))
    pg.emulate_media(reduced_motion='reduce')
    print('reduced motion bar transition:', pg.evaluate("getComputedStyle(document.querySelector('.bar')).transitionDuration"))
    print('errors:', errs)
    b.close()
