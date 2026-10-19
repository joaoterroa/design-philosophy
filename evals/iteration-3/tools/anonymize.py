#!/usr/bin/env python3
from study_paths import artifact_path
"""Prepare condition-free rendered pairs before visual review; keep identity key separate."""
from pathlib import Path
import json,shutil,secrets,argparse
from PIL import Image,ImageDraw,ImageFont
STUDY=Path(__file__).resolve().parents[1]
ROOT=STUDY.parents[1]
PREFERRED={
 'oncall-menubar':['main__menu__light','pending__menu__light','compose__menu__dark','offline__menu__dark'],
 'incident-dashboard':['live__tv__dark','surge__tv__dark','stale__tv__light','live__laptop__light'],
 'banking-onboarding':['welcome__phone__light','code__phone__light','code-error__phone__dark','help__small__light'],
}

def run():
    proto=json.loads((STUDY/'protocol.json').read_text());dest=STUDY/'blind-review';dest.mkdir(exist_ok=True)
    key_path=STUDY/'review-key.json';mapping=json.loads(key_path.read_text()) if key_path.exists() else {}
    tasks=[]
    fonts=['/System/Library/Fonts/Helvetica.ttc','/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    font=next((ImageFont.truetype(f,18) for f in fonts if Path(f).exists()),ImageFont.load_default())
    for task in PREFERRED:
        (dest/task).mkdir(exist_ok=True)
        taskpairs=[]
        for repeat in (1,2):
            id=f'{task}-pair-{repeat}';runs=[r for r in proto['runs'] if r['task']==task and r['repeat']==repeat]
            if not all((artifact_path(r, STUDY)/'capture.json').exists() for r in runs):continue
            if not all(json.loads((artifact_path(r, STUDY)/'capture.json').read_text()).get('complete') for r in runs):continue
            if id not in mapping:
                order=['baseline','revision'];
                if secrets.randbits(1):order.reverse()
                mapping[id]=dict(zip(('L','R'),order))
            pairdir=dest/task/f'pair-{repeat}';pairdir.mkdir(parents=True,exist_ok=True)
            sides={}
            for side,condition in mapping[id].items():
                record=next(r for r in runs if r['condition']==condition);artifact=artifact_path(record, STUDY);out=pairdir/side
                out.mkdir(exist_ok=True)
                if (artifact/'outputs/app').exists() and not (out/'app').exists():shutil.copytree(artifact/'outputs/app',out/'app')
                cap=json.loads((artifact/'capture.json').read_text());shots=[]
                for shot in cap['shots']:
                    if not shot.get('captureSucceeded'):continue
                    target=out/'shots'/Path(shot['path']).name;target.parent.mkdir(exist_ok=True)
                    shutil.copyfile(artifact/shot['path'],target)
                    shots.append(dict(id=shot['id'],file=target.relative_to(ROOT).as_posix(),pixels=shot['dimensions'],viewport=shot['viewport']))
                sides[side]=dict(shots=shots,app=(out/'app/index.html').relative_to(ROOT).as_posix(),metadata='Deliberately omitted condition, DESIGN.md, process artifacts and scores.')
            preferred=[shot for shot in PREFERRED[task] if all(any(s['id']==shot for s in sides[side]['shots']) for side in ('L','R'))]
            sheets=[]
            for n,shotid in enumerate(preferred):
                originals=[Image.open(ROOT/next(s['file'] for s in sides[side]['shots'] if s['id']==shotid)).convert('RGB') for side in ('L','R')]
                # Equal shared scale; no independent fit-to-height that could distort proportions.
                scale=min(1,690/max(im.width for im in originals),850/max(im.height for im in originals))
                resized=[im.resize((round(im.width*scale),round(im.height*scale))) for im in originals]
                canvas=Image.new('RGB',(1440,max(im.height for im in resized)+70),'#ecece8');draw=ImageDraw.Draw(canvas)
                for col,im in enumerate(resized):
                    draw.text((col*720+16,12),('Left' if col==0 else 'Right')+' · '+shotid,font=font,fill='#202020')
                    canvas.paste(im,(col*720+(720-im.width)//2,55))
                target=pairdir/f'comparison-{n+1}.png';canvas.save(target);sheets.append(target.relative_to(ROOT).as_posix())
            taskpairs.append(dict(id=id,repeat=repeat,sides=sides,primaryComparisons=sheets,primaryStates=preferred))
        manifest=dict(task=task,pairs=taskpairs,rubric=['composition','hierarchy','task fit and usability','product-specific personality','craftsmanship','overall design quality'],scoreAnchors={'1':'weak','2':'material weaknesses','3':'competent','4':'strong','5':'exceptional'},instructions='Judge full screens at their actual scale before enlarged details. Consider state changes, labels, density, priority and character together. No credit for following an unseen process or resembling a brand. State uncertainty. Do not inspect any other task, the identity key, skill files, DESIGN.md or other study material.')
        (dest/task/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');tasks.append(task)
    key_path.write_text(json.dumps(mapping,indent=2)+'\n')
    print('Prepared anonymous tasks:',', '.join(tasks))
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--study',type=Path,default=STUDY);args=parser.parse_args();STUDY=args.study.resolve();run()
