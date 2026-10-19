from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image, ImageOps, ImageDraw
import json

ROOT = Path(__file__).resolve().parents[1]
APP = (ROOT / 'app/index.html').as_uri()
OUT = ROOT / 'verification'
SCREENS = ['welcome', 'details', 'details-error', 'code', 'code-error', 'help', 'done']
results = []
with sync_playwright() as p:
    browser = p.chromium.launch()
    for width, height in [(390,844),(320,568)]:
        thumbs = []
        for theme in ['light','dark']:
            for screen in SCREENS:
                page = browser.new_page(viewport={'width':width,'height':height}, device_scale_factor=1)
                errors=[]
                page.on('pageerror', lambda error: errors.append(str(error)))
                page.goto(f'{APP}?screen={screen}&theme={theme}')
                page.evaluate('document.fonts.ready')
                metrics = page.evaluate('''() => ({width:innerWidth, documentWidth:document.documentElement.scrollWidth, height:document.documentElement.scrollHeight, targets:[...document.querySelectorAll('button,a,input')].filter(e=>e.getClientRects().length && !e.closest('dialog:not([open])')).map(e=>({label:e.getAttribute('aria-label')||e.textContent||e.id,width:e.getBoundingClientRect().width,height:e.getBoundingClientRect().height})), heading:document.querySelector('h1').getBoundingClientRect().top})''')
                assert metrics['documentWidth'] == width, (screen,theme,metrics)
                assert not errors, errors
                assert all(t['height']>=48 for t in metrics['targets']), (screen,metrics['targets'])
                shot = OUT / 'screenshots' / f'{screen}-{theme}-{width}.png'
                page.screenshot(path=str(shot), full_page=True)
                img=Image.open(shot).convert('RGB')
                # Full-page contact sheet retains scroll content at small viewport.
                thumb=ImageOps.contain(img,(195,600))
                canvas=Image.new('RGB',(215,650),'#e0e0e0')
                canvas.paste(thumb,((215-thumb.width)//2,30))
                ImageDraw.Draw(canvas).text((8,8),f'{screen} / {theme}',fill='#000000')
                thumbs.append(canvas)
                results.append({'screen':screen,'theme':theme,'viewport':[width,height],**metrics,'errors':errors})
                page.close()
        sheet=Image.new('RGB',(215*7,650*2),'#e0e0e0')
        for i,img in enumerate(thumbs): sheet.paste(img,((i%7)*215,(i//7)*650))
        sheet.save(OUT / f'contact-sheet-{width}.png')
    browser.close()
(OUT/'render-results.json').write_text(json.dumps(results,indent=2))
print(f'{len(results)} state/theme/size render checks passed.')
