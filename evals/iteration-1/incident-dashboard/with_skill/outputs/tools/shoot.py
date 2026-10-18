import sys, json
from playwright.sync_api import sync_playwright
O=sys.argv[1]; only=sys.argv[2:] 
base='file://'+O+'/app/index.html'
shots=[
 ('wall-live-dark',1920,1080,'?display=wall&state=live&frozen'),
 ('wall-live-light',1920,1080,'?display=wall&state=live&frozen&theme=light'),
 ('wall-allclear-dark',1920,1080,'?display=wall&state=allclear&frozen'),
 ('wall-stale-dark',1920,1080,'?display=wall&state=stale&frozen'),
 ('wall-partial-dark',1920,1080,'?display=wall&state=partial&frozen'),
 ('wall-surge-dark',1920,1080,'?display=wall&state=surge&frozen'),
 ('wall-loading-dark',1920,1080,'?display=wall&state=loading&frozen'),
 ('wall-live-4k',3840,2160,'?display=wall&state=live&frozen'),
 ('wall-live-1366x768',1366,768,'?display=wall&state=live&frozen'),
 ('desk-live-light-1440',1440,900,'?state=live&frozen&theme=light'),
 ('desk-live-dark-1440',1440,900,'?state=live&frozen&theme=dark'),
 ('desk-live-light-1280x720',1280,720,'?state=live&frozen&theme=light'),
 ('desk-surge-light-1440',1440,900,'?state=surge&frozen&theme=light'),
 ('desk-partial-light-1440',1440,900,'?state=partial&frozen&theme=light'),
 ('desk-stale-light-1440',1440,900,'?state=stale&frozen&theme=light'),
 ('desk-allclear-light-1440',1440,900,'?state=allclear&frozen&theme=light'),
 ('desk-loading-light-1440',1440,900,'?state=loading&frozen&theme=light'),
 ('narrow-live-light-390',390,844,'?state=live&frozen&theme=light'),
 ('narrow-live-dark-390',390,844,'?state=live&frozen&theme=dark'),
]
M="""()=>{
 const d=document.documentElement; const out={hscroll:d.scrollWidth>d.clientWidth, docH:d.scrollHeight, vh:innerHeight};
 const r=(s)=>{const e=document.querySelector(s); if(!e) return null; const b=e.getBoundingClientRect(); return [Math.round(b.top),Math.round(b.bottom)]};
 out.firstRow=r('#open-list li:not([hidden]) .row'); out.oncall=r('.oncall');
 out.visibleOpen=document.querySelectorAll('#open-list li:not([hidden])').length;
 out.font=document.fonts.check('16px "IBM Plex Sans"');
 out.rootPx=getComputedStyle(d).fontSize;
 // elements whose text overflows their box horizontally (excluding intentionally clamped)
 const bad=[]; document.querySelectorAll('body *').forEach(e=>{ if(e.closest('[hidden]')||e.closest('svg')) return; const cs=getComputedStyle(e); if(cs.display==='none') return;
   const b=e.getBoundingClientRect(); if(b.width>0 && b.right>innerWidth+1) bad.push(e.className||e.tagName)});
 out.offscreen=[...new Set(bad)].slice(0,8);
 const sec=document.querySelector('#open-section'); out.sectionOverflow= sec.scrollHeight>sec.clientHeight+1 && d.dataset.display==='wall';
 const side=document.querySelector('.side'); out.sideOverflow= side.scrollHeight>side.clientHeight+1 && d.dataset.display==='wall';
 return out}"""
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/opt/pw-browsers/chromium', args=['--headless=new'])
    for name,w,h,qs in shots:
        if only and not any(o in name for o in only): continue
        pg=b.new_page(viewport={'width':w,'height':h})
        errs=[]; pg.on('console', lambda m: errs.append(m.text) if m.type=='error' else None); pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.goto(base+qs); pg.wait_for_timeout(400)
        full = name.startswith('desk') or name.startswith('narrow')
        pg.screenshot(path=f'{O}/screenshots/{name}.png', full_page=full)
        print(name, json.dumps(pg.evaluate(M)), errs)
        pg.close()
    b.close()
