#!/usr/bin/env python3
from study_paths import artifact_path
"""Collect each finished job once while the remaining generators continue."""
from pathlib import Path
import json,time,subprocess,sys,argparse
TOOLS=Path(__file__).resolve().parent
parser=argparse.ArgumentParser();parser.add_argument('--protocol',type=Path,default=TOOLS.parent/'protocol.json');args=parser.parse_args();p=args.protocol.resolve();STUDY=p.parent;protocol=json.loads(p.read_text())
while True:
    pending=[]
    for r in protocol['runs']:
        a=artifact_path(r, STUDY)
        if (a/'capture.json').exists():continue
        s=a/'status.json'
        status=json.loads(s.read_text()) if s.exists() else {}
        quota=any('usage limit' in json.dumps(e).lower() for e in status.get('agentErrors',[]))
        if not status or status['state']=='running' or quota:pending.append(r['id']);continue
        result=subprocess.run([sys.executable,str(TOOLS/'capture.py'),'--protocol',str(p),'--run',r['id']],check=False)
        if result.returncode:
            print('Capture incomplete; retained as evidence:',r['id'],flush=True)
            if not (a/'capture.json').exists():raise RuntimeError('Capture infrastructure failed before a record was written')
    if not pending:break
    time.sleep(10)
print('Collected all12 finished job records.',flush=True)
