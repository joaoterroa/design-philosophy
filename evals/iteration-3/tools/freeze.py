#!/usr/bin/env python3
"""Pre-register the comparison and create clean, task-scoped workspaces."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
import json,shutil,random,subprocess
ROOT=Path(__file__).resolve().parents[3];STUDY=ROOT/'evals/iteration-3';WORK=Path('/private/tmp/design-eval-iteration-3')
def hashes(folder):return {p.relative_to(folder).as_posix():sha256(p.read_bytes()).hexdigest() for p in sorted(folder.rglob('*')) if p.is_file()}
def run():
    assert not (STUDY/'protocol.json').exists(),'Protocol is immutable once frozen.'
    raw=json.loads((ROOT/'evals/evals.json').read_text())['evals']
    common=STUDY/'inputs/common';common.mkdir(parents=True,exist_ok=True)
    prior=ROOT/'evals/iteration-2/browser-company-study/evidence'
    refs=json.loads((prior/'catalog.json').read_text());wanted=['dia-strategy-05','dia-profile-form','dia-icon-picker','dia-signup','arc-routing','arc-recovery']
    rp=common/'reference-pack';rp.mkdir(exist_ok=True)
    lines=['# Frozen first-party visual references','\nAvailable equally to all runs. Product images, not a style requirement. No prior generated interfaces or investigation conclusions are included. Use local images and record the limits of crops. Network is disabled.\n']
    for id in wanted:
        item=next(x for x in refs if x['id']==id);target=rp/f'{id}.png';shutil.copyfile(prior/item['file'],target)
        lines.append(f"- `{target.name}`: {item['title']}. {item['kind']}. {item['published']}. Source: {item['source']}. SHA256: {item['sha256']}\n")
    (rp/'SOURCES.md').write_text('\n'.join(lines))
    fonts=common/'fonts';fonts.mkdir(exist_ok=True)
    source=ROOT/'evals/iteration-1/incident-dashboard/with_skill/outputs/app/fonts'
    for name in ['plex-sans-latin.woff2','plex-mono-400-latin.woff2','plex-mono-500-latin.woff2']:shutil.copyfile(source/name,fonts/name)
    incidents=[
      dict(id='INC-2291',title='Route optimiser timeouts for EU-West depots',service='Routing API',severity=1,status='Investigating',opened='09:42',duration='1h 18m',commander=None),
      dict(id='INC-2290',title='Delayed tracking events from scanner fleet B',service='Tracking Ingest',severity=2,status='Mitigated',opened='08:05',duration='2h 55m',commander='Priya N.'),
      dict(id='INC-2289',title='Invoice PDF generation failing for 3% of accounts',service='Billing',severity=2,status='Monitoring',opened='Yesterday 22:10',duration='12h 50m',commander='Sam Okafor'),
    ]
    for i,(title,service) in enumerate([('Proof-of-delivery photos delayed','Driver App Backend'),('ETA recalculation lagging on EU routes','Routing API'),('Stock counts stale for Rotterdam depot','Warehouse Sync'),('Fuel surcharge rounding discrepancy','Billing'),('Pickup requests delayed for partner fleet','Routing API'),('Scanner retry queue above normal','Tracking Ingest'),('Export manifest refresh delayed','Warehouse Sync'),('Driver session refresh retries','Driver App Backend'),('Invoice export queue growing','Billing')]):
        incidents.append(dict(id=f'INC-{2286-i}',title=title,service=service,severity=3,status='Monitoring',opened='08:30',duration='2h 30m',commander='Aiko Kimura'))
    fixtures=dict(now='2026-10-18T10:00:00Z',menu=dict(product='Rota',teamSize=40,user='Jamie Ellis',rotation='Platform Primary',shiftStart='06:00',shiftEnd='18:00',handoverTo='Priya Raman',roster=[dict(name=n,role=r,until='18:00') for n,r in [('Jamie Ellis','Platform Primary'),('Sam Okafor','Observability'),('Tomás Ortega','Routing'),('Aiko Kimura','Data')]],pendingStillResponsible=True),bank=dict(name='Harbour',customer='Alex Morgan',mobileEnding='482',testCode='482913',codeLength=6,accountName='Everyday account',sortCode='04-00-26',accountNumber='12345678',balance='£0.00',helpPhone='0808 157 0192',warning='We will never call you to ask for this code. Do not share it.'),dashboard=dict(product='Northwind Incidents',openCount=7,surgeCount=12,incidents=incidents,resolved=[dict(id='INC-2288',title='Driver app login slow on Android 14',service='Driver App Backend',severity=3,status='Resolved',opened='Yesterday 15:30',duration='2h 05m'),dict(id='INC-2287',title='Warehouse sync duplicate SKUs',service='Warehouse Sync',severity=3,status='Resolved',opened='Yesterday 11:02',duration='45m')],services=[dict(name=n,value=v) for n,v in [('Routing API',14),('Tracking Ingest',9),('Billing',6),('Driver App Backend',4),('Warehouse Sync',2)]],primary='Priya N. (Platform)',secondary='Tomás R. (Routing)',until='18:00',pages=23,pagesDelta=5,mttr='48m',mttrChange='12% lower',slo='61%',sloChange='4 points lower',staleAsOf='09:42',displayTime='11:00',displayDate='18 October 2026'))
    (common/'fixtures.js').write_text('/* Fixed benchmark fixture. Test code is fixture-only, not an example to display to users. */\nwindow.EVAL_FIXTURES = '+json.dumps(fixtures,ensure_ascii=False,indent=2)+';\n')
    (common/'fixtures.json').write_text(json.dumps(fixtures,ensure_ascii=False,indent=2)+'\n')
    contract='''# Production contract for this evaluation

This workspace is one task: implement only the task in the opening user request. Task-specific clauses below apply only to that task.

Work only in this workspace. Read `skill/SKILL.md` and follow that supplied skill. It is the only design skill for this run. Other agents work elsewhere; edit only this workspace. Use `reference-pack/` for available offline visual research. Do not search other projects, home directories, earlier evaluations or other runs. Do not use installed skills, subagents, connectors or external services. All assets and code must work offline from disk. State any evidence limits instead of requesting clarification.

Deliver `outputs/app/index.html`, supporting static files, `outputs/DESIGN.md` and your verification scripts/screenshots. The prototype must run from file:// without a build or network. Copy the provided fixtures.js into the app and use EVAL_FIXTURES for shared facts. You may choose your copy and composition. Do not display test codes or pretend to use a real backend.

Provide a document root container `#app`. URL `?screen=<state>&theme=light|dark&display=tv|laptop` must directly open the states below. Normal interactions must work too. Record implemented and omitted behavior in DESIGN.md; no demo controls inside the product canvas. You may put a review harness in a separate HTML file.

- Menu: `main`, `compose`, `pending`, `offline`, `empty`, `accepted`. #app is a 360px-wide popover with maximum height640px, at x20/y20 in a 400×680 scene. The main flow lets Jamie choose Priya, review and send a handover. Sending enters pending, with Jamie responsible until acceptance. A simulated acceptance is a separate explicit action, not automatic. Offline shows last-known status honestly. Empty has no schedule. Preserve a return/cancel route. The supplied roster is the current roster, not all40staff.
- Dashboard: `live`, `stale`, `surge`. TV1920×1080 (`display=tv`) and laptop1440×900 (`display=laptop`). Live has the first7fixture incidents; surge all12. All statuses except the separate resolved list count as open in this fixture. Keep the original fixture facts, metrics, services and resolved history. Show missing commander as missing. Stale data must not look live. Explain any TV overflow and keep incidents reachable on laptop. Read dashboard/index.html and brand/guide.md first. Bundled fonts contain IBM Plex Sans and Mono. brand/guide.md is unchanged.
- Banking: `welcome`, `details-error`, `code`, `code-error`, `help`, `done`. Test390×844 and320×568. A plausible short accessible setup flow must lead from welcome to account details to SMS code to completion, with working validation, Back and Help. Details accepts name and mobile; invalid input shows helpful text. A wrong code must not advance; fixture testCode advances. Help gives a route to a person and dismisses by button and Escape with focus return. `help` directly opens Help over the code step. A code preview, if used, must not contain a usable example code. Keep the safety warning reachable. Use large text, clear labels and targets appropriate for older users.

Implement light and dark themes via the URL and system preference. Provide semantic, labeled controls, keyboard operation and visible focus. Preserve information in reduced motion. Target sizes and contrast must suit the task. Every state must be accessible through its direct URL.

You have the same20minute wall-clock allowance as every run, including research, exploration, implementation and verification. Use this whole allowance wisely, but finish when the implementation and checks are ready. Prioritize a runnable complete result. Do not install dependencies. Available tools: Node, Python `/private/tmp/design-compare-venv/bin/python` with Playwright and Pillow, and installed Chromium. Headless launch can require sandbox escalation; request that through the approval tool if needed. Inspect rendered screens yourself, fix issues, and record what you actually tested. Save a small set of your own screenshots; a separate evaluator will capture the full standardized set.

Do not commit, push, modify the supplied skill or fixtures, or edit global configuration. Record a preference for a visual treatment only if it fits this task. These are prototype exercises, not deployments.
'''
    (common/'CONTRACT.md').write_text(contract)
    runs=[]
    # Repeats split over sessions and counterbalanced conditions; order fixed before results.
    sequence=[('oncall-menubar','baseline',1),('incident-dashboard','revision',1),('banking-onboarding','baseline',1),('oncall-menubar','revision',1),('incident-dashboard','baseline',1),('banking-onboarding','revision',1),('oncall-menubar','revision',2),('incident-dashboard','baseline',2),('banking-onboarding','revision',2),('oncall-menubar','baseline',2),('incident-dashboard','revision',2),('banking-onboarding','baseline',2)]
    for idx,(task,condition,repeat) in enumerate(sequence):
        id=f'{task}__{condition}__{repeat}';workspace=WORK/f'job-{idx+1:02d}'
        assert not workspace.exists(),workspace
        workspace.mkdir(parents=True)
        shutil.copytree(STUDY/'skills'/condition,workspace/'skill')
        shutil.copytree(rp,workspace/'reference-pack')
        shutil.copytree(fonts,workspace/'fonts')
        shutil.copyfile(common/'fixtures.js',workspace/'fixtures.js')
        if task=='incident-dashboard':
            for folder in ('dashboard','brand'):shutil.copytree(ROOT/'evals/fixtures/incident-dashboard'/folder,workspace/folder)
        prompt=next(x['prompt'] for x in raw if x['name']==task)+'\n\n'+contract
        (workspace/'PROMPT.md').write_text(prompt)
        artifact=STUDY/f'runs/{task}/{condition}/run-{repeat}';artifact.mkdir(parents=True)
        (artifact/'PROMPT.md').write_text(prompt)
        runs.append(dict(id=id,task=task,condition=condition,repeat=repeat,workspace=str(workspace),artifactDir=str(artifact),promptSha256=sha256(prompt.encode()).hexdigest(),initialFiles=hashes(workspace)))
    protocol=dict(version=1,frozenAt=datetime.now(timezone.utc).isoformat(),baselineCommit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),executor=dict(cli='codex-cli 0.163.0',model='gpt-6.1-sol',reasoningEffort='high',maxConcurrent=3,timeoutSeconds=1200,network=False,hostSkills=False,independentFreshSessions=True),design=dict(tasks=3,conditions=2,repeats=2,runs=12,finalScreenshotsExpected=192,totalBudgetEqual=True,conditionBlindToGenerator=True,comparisonUnit='same task and repeat; task-level stability across repeats',bundledIntervention=True,noClaimOfStatisticalSignificance=True),skillHashes={c:hashes(STUDY/'skills'/c) for c in ('baseline','revision')},commonHashes=hashes(common),runs=runs,
    evaluation=dict(functional=['state routes render','no network or console errors','no horizontal overflow','task-critical facts retained','menu pending responsibility honest','bank incorrect/correct code and help/back/focus','older-user text and target dimensions','dashboard severity/commander/freshness and TV coverage','keyboard main paths and reduced motion'],visual=['composition','hierarchy','task fit and usability','product-specific personality','craftsmanship','overall design quality'],scale='1 weak,2 material weaknesses,3 competent,4 strong,5 exceptional; evidence per score',review='First review anonymous equal-scale rendered pairs without DESIGN.md or condition key; record preference and concrete reasons. Then inspect live interactions and reveal condition. Main-agent review is informed and not independent; seek human votes separately.',adoptionGate='Recommend adoption only if revised overall preference is stable on at least2of3tasks across both repeats, with no new critical functional/accessibility/coverage regression. Mixed result supports narrower revision, not automatic promotion.',accessibilityCaveat='Automated checks and scripted paths do not establish usability for older people or full screen-reader conformance.',externalValidity='Offline references, static prototypes, two repeats, one model; bundle cannot isolate each instruction; no independent human panel during this run.'))
    (STUDY/'protocol.json').write_text(json.dumps(protocol,indent=2,ensure_ascii=False)+'\n')
    (STUDY/'inputs/common/CONTRACT.md').write_text(contract)
    print('Frozen12 independent run workspaces and protocol. Expected192 final screenshots.')
if __name__=='__main__':run()
