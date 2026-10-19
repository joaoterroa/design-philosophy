#!/usr/bin/env python3
"""Continue only service-quota-interrupted attempts, with retained work and remaining budget.

No design outcome is replaced. Prior segments, artifacts and logs remain inspectable.
Requires a confirmed service reset before invocation. Does not consume reset credits.
"""
import argparse,json,shutil,math
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
from types import SimpleNamespace
import runner
STUDY=Path(__file__).resolve().parents[1]

def prepare(record):
    a=Path(record['artifactDir']);status=json.loads((a/'status.json').read_text())
    assert status['state']=='failed' and status.get('agentErrors'),record['id']
    assert any('usage limit' in json.dumps(e).lower() for e in status['agentErrors']),record['id']
    assert not status.get('originalInputsModified'),record['id']
    assert status['elapsedSeconds']<1200
    segment=a/'quota-segment-1';assert not segment.exists()
    segment.mkdir()
    # Preserve every earlier record and partial output; leave workspace work untouched.
    for file in ('attempt.lock','status.json','command.json','command.txt','events.jsonl','stderr.log','final.md','prompt.md','outputs'):
        if (a/file).exists():shutil.move(a/file,segment/file)
    prior=status['elapsedSeconds']
    events=[]
    for line in (segment/'events.jsonl').read_text(errors='replace').splitlines():
        try:
            event=json.loads(line)
            if event.get('type')=='item.completed' and event.get('item',{}).get('type')!='error':events.append(event)
        except:pass
    r=dict(record,quotaRecovery=True,priorElapsedSeconds=prior)
    remaining=math.floor(1200-prior)
    if events:
        # Ephemeral prior sessions cannot restore hidden context; provide only their own visible trace.
        w=Path(record['workspace']);(w/'RECOVERY-LOG.jsonl').write_text('\n'.join(json.dumps(e) for e in events)+'\n')
        r['contextRecovery']='existing workspace plus own visible trace; hidden context unavailable'
        r['quotaRecoveryPrompt']=f'''The service interrupted your previous session because account usage was exhausted. The account now allows ordinary usage. Continue the same task from the existing files, not a new design. Your prior visible tool/message trace is in RECOVERY-LOG.jsonl. Read it as your own work history; no external design review or feedback has been provided. Hidden reasoning cannot be restored. The supplied skill, fixtures and original request are unchanged. You have {remaining} seconds remaining from the original1200second allowance. Finish implementation and verification, preserving the task requirements. Use normal approval review for any sandbox escalation; earlier review failed because of quota, not an unsafe-action finding. Do not change the supplied inputs. Record any unfinished checks honestly.'''
    else:r['contextRecovery']='fresh; prior segment failed before design work'
    return r,remaining

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--confirmed-reset',action='store_true',required=True);parser.add_argument('--jobs',type=int,default=3,choices=(1,2,3));args=parser.parse_args()
    protocol=STUDY/'protocol.json';spec=json.loads(protocol.read_text())
    planned=[prepare(r) for r in spec['runs']]
    (STUDY/'recovery.json').write_text(json.dumps(dict(reason='service quota interruption, reset confirmed by ordinaryUsageAllowed=true',preservedFrozenInputs=True,budget='1200seconds cumulative active process time, interrupted segments retained',limitations=['Three sessions restore visible trace and workspace but not hidden ephemeral context.','Nine sessions had no prior design work.','Offline reference and model settings remain fixed.'],runs=[dict(id=r['id'],remainingSeconds=seconds,contextRecovery=r['contextRecovery']) for r,seconds in planned]),indent=2)+'\n')
    good=True
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        jobs={pool.submit(runner.run_one,r,protocol,SimpleNamespace(codex=runner.CODEX,dry_run=False,timeout_seconds=seconds)):r['id'] for r,seconds in planned}
        for f in as_completed(jobs):
            try:good=f.result() and good
            except Exception as e:print('RECOVERY ERROR',jobs[f],str(e),flush=True);good=False
    return 0 if good else 1
if __name__=='__main__':raise SystemExit(main())
