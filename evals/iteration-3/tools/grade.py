#!/usr/bin/env python3
from study_paths import artifact_path
"""Record functional evidence separately from visual preference. Never repair outputs."""
import json,re,argparse
from pathlib import Path
from urllib.parse import urlencode
from playwright.sync_api import sync_playwright
from capture import FIXED_TIME, output_hash
STUDY=Path(__file__).resolve().parents[1]

def text(page):return page.locator('body').inner_text()
def settle(page):page.clock.run_for(500)
def click(page,pattern):
    locator=page.get_by_role('button',name=re.compile(pattern,re.I)).filter(visible=True)
    if locator.count()==0:
        locator=page.get_by_role('link',name=re.compile(pattern,re.I)).filter(visible=True)
    if locator.count()==0:return False
    locator.first.click();settle(page);return True

def fill_code(page,value):
    fields=page.locator('input:visible').all()
    # Prefer an explicitly identifiable one-time-code field; otherwise use the visible code inputs.
    otp=[f for f in fields if (f.get_attribute('autocomplete')=='one-time-code' or re.search(r'otp|code', (f.get_attribute('name') or '')+' '+(f.get_attribute('id') or ''),re.I))]
    candidates=otp or fields
    if not candidates:return False
    singles=[f for f in candidates if f.get_attribute('maxlength')=='1']
    if len(singles)>=6:
        for f,digit in zip(singles,value):f.fill(digit)
    else:candidates[0].fill(value)
    return True

def interaction(browser,record):
    app=artifact_path(record, STUDY)/'outputs/app/index.html';task=record['task'];results=[]
    if not app.exists():return [dict(check='live flow',status='unavailable',evidence='App missing')]
    context=browser.new_context(viewport=dict(width=400 if task=='oncall-menubar' else 390,height=844),reduced_motion='reduce',locale='en-GB',timezone_id='Europe/London')
    context.route('**/*',lambda r:r.abort() if r.request.url.startswith(('http:','https:')) else r.continue_())
    page=context.new_page();page.clock.install(time=FIXED_TIME);page.clock.pause_at(FIXED_TIME)
    def open(screen):page.goto(app.as_uri()+'?'+urlencode(dict(screen=screen,theme='light',display='menu' if task=='oncall-menubar' else 'phone')));settle(page)
    def add(check,status,evidence):results.append(dict(check=check,status=status,evidence=evidence))
    try:
        if task=='oncall-menubar':
            open('main');launched=click(page,r'hand.?over|transfer.*shift')
            add('open handover','pass' if launched else 'needs manual review',text(page)[:900])
            chosen=False
            if launched:
                radio=page.get_by_role('radio',name=re.compile('Priya',re.I))
                if radio.count():radio.first.check();chosen=True
                else:
                    label=page.get_by_label(re.compile('Priya',re.I))
                    if label.count() and label.first.get_attribute('type') in ('radio','checkbox'):label.first.check();chosen=True
                    if not chosen:
                        for select in page.locator('select:visible').all():
                            options=select.locator('option').all()
                            for option in options:
                                if 'Priya' in (option.text_content() or ''):
                                    select.select_option(value=option.get_attribute('value'));chosen=True;break
                            if chosen:break
                    if not chosen:chosen=click(page,r'Priya')
                settle(page)
                click(page,r'^review|review hand|continue')
                sent=click(page,r'send|request.*handover|ask.*Priya|confirm.*handover|^hand.?over$')
                settle(page);current=text(page);honest=bool(re.search(r'still.*(you|Jamie)|(you|Jamie).*still|until.*accept|remain.*(you|on.call)',current,re.I))
                add('send and retain responsibility while pending','pass' if sent and honest else 'needs manual review',dict(chosen=chosen,sent=sent,text=current[:1500]))
                page.clock.run_for(5000)
                add('no automatic acceptance','pass' if re.search(r'pending|waiting|until.*accept|request.*sent',text(page),re.I) else 'needs manual review',text(page)[:1000])
        elif task=='banking-onboarding':
            open('welcome');started=click(page,r'get started|^start|begin|set up|open.*account|^continue|^next')
            add('welcome advances','pass' if started and page.locator('input:visible').count()>0 else 'needs manual review',text(page)[:700])
            for field in page.locator('input:visible').all():
                info=field.evaluate('(e)=>({id:e.id,type:e.type,name:e.name,label:[...(e.labels||[])].map(l=>l.textContent).join(" ")})')
                desc=' '.join(str(v) for v in info.values()).lower()
                if 'mobile' in desc or 'phone' in desc or info['type']=='tel':field.fill('07123456482')
                elif 'first' in desc:field.fill('Alex')
                elif 'last' in desc or 'surname' in desc:field.fill('Morgan')
                elif 'name' in desc:field.fill('Alex Morgan')
            advanced=click(page,r'^continue|^next|send.*code|check.*details')
            add('valid details advance','pass' if advanced and re.search(r'code|texted|text message',text(page),re.I) else 'needs manual review',text(page)[:1000])
            # Direct code route ensures an upstream selector mismatch does not block this test.
            open('code');fill_code(page,'000000');pressed=click(page,r'^continue|verify|confirm|check.*code|^finish|^next')
            bad=text(page)
            add('wrong code rejected','pass' if pressed and re.search(r'incorrect|wrong|not.*match|try again|check.*code|invalid',bad,re.I) and page.locator('input:visible').count()>0 else 'needs manual review',bad[:1200])
            filled=fill_code(page,'482913');pressed=click(page,r'^continue|verify|confirm|check.*code|^finish|^next');good=text(page)
            add('correct code advances','pass' if filled and pressed and re.search(r'ready|complete|all set|set up|account.*open|welcome|success',good,re.I) else 'needs manual review',good[:1400])
            open('code');helped=click(page,r'^help$|get help|help with|need help')
            helptext=text(page);has_human=bool(re.search(r'0808|call|phone|branch|speak|person',helptext,re.I))
            add('help provides human route','pass' if helped and has_human else 'needs manual review',helptext[:1300])
            page.keyboard.press('Escape');settle(page)
            active=page.evaluate('({tag:document.activeElement.tagName,text:document.activeElement.textContent?.trim().slice(0,100),outline:getComputedStyle(document.activeElement).outlineStyle})')
            add('Escape restores Help focus','pass' if helped and re.search(r'help',active['text'] or '',re.I) else 'needs manual review',active)
            page.locator('input:visible').first.focus();page.keyboard.press('Tab')
            focus=page.evaluate('({tag:document.activeElement.tagName,text:document.activeElement.textContent?.trim().slice(0,100),outline:getComputedStyle(document.activeElement).outlineStyle,shadow:getComputedStyle(document.activeElement).boxShadow})')
            add('keyboard focus indicator','pass' if focus['outline'] not in ('none','') or focus['shadow']!='none' else 'needs manual review',focus)
        else:
            add('dashboard interaction scope','not applicable','Read-only display; inspect data, freshness, overflow and laptop access separately.')
    except Exception as error:add('script path','needs manual review',str(error))
    finally:context.close()
    return results

def run():
    proto=json.loads((STUDY/'protocol.json').read_text());all_results=[]
    fixture_path=STUDY/'inputs/incident-dashboard/fixtures.json'
    if not fixture_path.exists():fixture_path=STUDY/'inputs/common/fixtures.json'
    fixtures=json.loads(fixture_path.read_text());open_ids={x['id'] for x in fixtures['dashboard']['incidents']};resolved_ids={x['id'] for x in fixtures['dashboard']['resolved']}
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True)
        for record in proto['runs']:
            if SELECTED and record['id'] not in SELECTED:continue
            a=artifact_path(record, STUDY);cap_path=a/'capture.json'
            if not cap_path.exists():continue
            cap=json.loads(cap_path.read_text());status=json.loads((a/'status.json').read_text());checks=[];flags=[]
            def check(name,passed,evidence,severity='functional'):
                checks.append(dict(check=name,status='pass' if passed else 'fail',evidence=evidence,severity=severity))
            check('complete run',status.get('completeArtifact',False),status['state'],'critical')
            check('all final states captured',cap.get('complete',False),f"{cap.get('capturedShots',0)}/{cap['expectedShots']}",'critical')
            check('supplied inputs unchanged',not status.get('originalInputsModified',False),status.get('changedOriginalInputs',[]),'integrity')
            for field,name in [('consoleErrorShots','console errors'),('pageErrorShots','runtime errors'),('networkDependentShots','network dependence'),('horizontalOverflowShots','horizontal overflow'),('menuClippedShots','menu clipping')]:
                check('no '+name,cap.get('issues',{}).get(field,0)==0,cap.get('issues',{}).get(field,0))
            shots=cap.get('shots',[])
            for screen in sorted({x['screen'] for x in shots}):
                variants=[s for s in shots if s['screen']==screen];light=next((s for s in variants if s['theme']=='light'),{});dark=next((s for s in variants if s['theme']=='dark' and s['display']==light.get('display')), {})
                check('theme changes '+screen,light.get('sha256')!=dark.get('sha256'),dict(light=light.get('sha256'),dark=dark.get('sha256')))
            if record['task']=='banking-onboarding':
                normal=next(s for s in shots if s['screen']=='code' and s['display']=='phone' and s['theme']=='light');m=normal.get('metrics',{})
                check('code preview has no usable test code','482913' not in re.sub(r'\s','',m.get('bodyText','')),'Visible body text excludes482913','critical')
                fields=[];small=[]
                for s in shots:
                    fields.extend(s.get('metrics',{}).get('unlabeledFields',[]))
                    small.extend([dict(shot=s['id'],label=c['label'],rect=c['rect']) for c in s.get('metrics',{}).get('controls',[]) if c['inViewport'] and not c['disabled'] and (c['rect']['width']<43.9 or c['rect']['height']<43.9)])
                check('programmatic field labels',not fields,fields,'accessibility')
                check('visible interactive targets at least44px',not small,small,'accessibility')
                smalltext=[dict(text=t['text'],size=t['fontSize']) for t in m.get('textRuns',[]) if t['inViewport'] and t['fontSize']<16 and t['tag'] not in ('SVG','PATH')]
                check('code screen visible text at least16px',not smalltext,smalltext,'accessibility')
            elif record['task']=='incident-dashboard':
                for s in shots:
                    if s['theme']!='light' or s['display']!='tv':continue
                    m=s.get('metrics',{});runs=m.get('textRuns',[]);ids=set()
                    for t in runs:
                        if t['inViewport'] and t['rect']['bottom']<=1080.1:ids.update(re.findall(r'INC-\d+',t['text']))
                    s['visibleIncidentIds']=sorted(ids)
                    flags.append(dict(check='TV visible incident identifiers',screen=s['screen'],count=len(ids),openCount=len(ids & open_ids),resolvedCount=len(ids & resolved_ids),ids=sorted(ids),expectedOpen=12 if s['screen']=='surge' else 7,note='Identifier visibility is a coverage aid; inspect title legibility, overflow summary and paging behavior too.'))
                    if s['screen']=='live':check('SEV1 incident retained','INC-2291' in m.get('bodyText',''),'INC-2291 in rendered text','critical')
                    if s['screen']=='stale':check('stale status explicit',bool(re.search(r'stale|last.*update|offline|connection|out.of.date|last.*sync',m.get('bodyText',''),re.I)),m.get('bodyText','')[:800],'critical')
            source_hash=output_hash(a/'outputs') if (a/'outputs').exists() else None
            live=interaction(browser,record)
            assert not source_hash or output_hash(a/'outputs')==source_hash,'Grading changed source'
            result=dict(runId=record['id'],checks=checks,observations=flags,interaction=live,failures=sum(c['status']=='fail' for c in checks),limitations=['Target and text checks are scoped measurements, not full accessibility or usability conformance.','Unrecognized generic action selectors require manual review; do not count as an agent defect without checking.'])
            (a/'functional.json').write_text(json.dumps(result,indent=2)+'\n');all_results.append(result)
            print(record['id'],result['failures'],'automatic flags',flush=True)
        browser.close()
    all_results=[json.loads((artifact_path(r, STUDY)/'functional.json').read_text()) for r in proto['runs'] if (artifact_path(r, STUDY)/'functional.json').exists()]
    (STUDY/'functional.json').write_text(json.dumps(all_results,indent=2)+'\n')
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--study',type=Path,default=STUDY);parser.add_argument('--run',action='append');args=parser.parse_args();STUDY=args.study.resolve();SELECTED=set(args.run or []);run()
