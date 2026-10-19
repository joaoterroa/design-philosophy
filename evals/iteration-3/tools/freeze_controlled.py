#!/usr/bin/env python3
"""Freeze the valid task-only cohort; keep the excluded pilot and skill versions intact."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime,timezone
import json,shutil
ROOT=Path(__file__).resolve().parents[3];PILOT=ROOT/'evals/iteration-3';STUDY=PILOT/'controlled';WORK=Path('/private/tmp/design-eval-iteration-3-controlled')
def hashes(folder):return {p.relative_to(folder).as_posix():sha256(p.read_bytes()).hexdigest() for p in sorted(folder.rglob('*')) if p.is_file()}
def main():
 assert not (STUDY/'protocol.json').exists()
 old=json.loads((PILOT/'protocol.json').read_text());STUDY.mkdir(exist_ok=True)
 shutil.copytree(PILOT/'skills',STUDY/'skills');shutil.copyfile(PILOT/'revision.diff',STUDY/'revision.diff')
 for c in ('baseline','revision'):assert hashes(STUDY/'skills'/c)==old['skillHashes'][c]
 common=STUDY/'inputs/common';common.mkdir(parents=True)
 for folder in ('reference-pack','fonts'):shutil.copytree(PILOT/'inputs/common'/folder,common/folder)
 fixtures=json.loads((PILOT/'inputs/common/fixtures.json').read_text())
 original=(PILOT/'inputs/common/CONTRACT.md').read_text()
 generic_before=original.split('- Menu:')[0]
 generic_after=original[original.index('Implement light and dark themes'):]
 generic_after=generic_after.replace('same20minute wall-clock allowance','same12minute wall-clock allowance')
 tasks={'oncall-menubar':('menu','Menu','Dashboard'),'incident-dashboard':('dashboard','Dashboard','Banking'),'banking-onboarding':('bank','Banking',None)}
 prompts={e['name']:e['prompt'] for e in json.loads((ROOT/'evals/evals.json').read_text())['evals']}
 runs=[]
 for i,prior in enumerate(old['runs']):
  task=prior['task'];key,label,nextlabel=tasks[task];work=WORK/f'job-{i+1:02d}';assert not work.exists();work.mkdir(parents=True)
  shutil.copytree(STUDY/'skills'/prior['condition'],work/'skill');shutil.copytree(common/'reference-pack',work/'reference-pack');shutil.copytree(common/'fonts',work/'fonts')
  fixed={'now':fixtures['now'],key:fixtures[key]}
  js='/* Fixed offline fixture for the assigned product. */\nwindow.EVAL_FIXTURES = '+json.dumps(fixed,ensure_ascii=False,indent=2)+';\n'
  (work/'fixtures.js').write_text(js)
  if task=='incident-dashboard':
   for folder in ('dashboard','brand'):shutil.copytree(ROOT/'evals/fixtures/incident-dashboard'/folder,work/folder)
  specific=original.split('- '+label+':',1)[1]
  specific=specific.split('- '+nextlabel+':',1)[0] if nextlabel else specific.split('Implement light and dark themes',1)[0]
  contract=generic_before+'## Assigned product requirements\n\n'+label+':'+specific+'\n'+generic_after
  # No other app contract or data is visible to a generator.
  prompt=prompts[task]+'\n\n'+contract
  (work/'PROMPT.md').write_text(prompt)
  a=STUDY/f"runs/{task}/{prior['condition']}/run-{prior['repeat']}";a.mkdir(parents=True)
  (a/'PROMPT.md').write_text(prompt)
  taskinput=STUDY/'inputs'/task;taskinput.mkdir(exist_ok=True);(taskinput/'CONTRACT.md').write_text(contract);(taskinput/'fixtures.js').write_text(js);(taskinput/'fixtures.json').write_text(json.dumps(fixed,indent=2)+'\n')
  runs.append(dict(id=prior['id'],task=task,condition=prior['condition'],repeat=prior['repeat'],workspace=str(work),artifactDir=str(a),promptSha256=sha256(prompt.encode()).hexdigest(),initialFiles=hashes(work)))
 protocol={**old,'frozenAt':datetime.now(timezone.utc).isoformat(),'cohort':'controlled task-only; primary comparison','excludedPilot':'../PILOT-EXCLUSION.json','executor':{**old['executor'],'timeoutSeconds':720},'runs':runs,'commonHashes':hashes(STUDY/'inputs'),'amendmentsBeforeFirstRun':['Each workspace contains only its own task contract and data, fixing the excluded pilot’s cross-task workload ambiguity.','Equal12minute ceiling for all12fresh jobs; skill snapshots exactly match the frozen pilot versions.'],'design':{**old['design'],'independentFreshSessions':True,'quotaRecovery':False,'maxGenerationActiveSeconds':8640,'noPriorGeneratedInterfaces':True}}
 (STUDY/'protocol.json').write_text(json.dumps(protocol,indent=2,ensure_ascii=False)+'\n')
 (STUDY/'reviews').mkdir();shutil.copyfile(PILOT/'reviews/RUBRIC.md',STUDY/'reviews/RUBRIC.md')
 print('Frozen12fresh task-only jobs; baseline/revision hashes identical to excludedpilot;720second equalbudget.')
if __name__=='__main__':main()
