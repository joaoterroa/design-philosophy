#!/usr/bin/env python3
"""Build a self-contained visual shape study from primary evidence and offline captures."""
import base64
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path
from PIL import Image
from capture import STUDY, REPO, VARIANTS, FACTOR

PRIOR=STUDY.parent/'browser-company-study'
# Manual observation records. Crops are source pixels, not fits to a curve formula.
OBSERVATIONS=[
 ('dia-profile-home','Composer and browser frame','The broad composer, selected tab, small profile control and pill attachment action form different shape roles.',[558,403,678,523],'demo'),
 ('dia-profile-form','Profile creation','The modal, input and buttons use modest corners. The larger composer behind them stays much softer.',[731,345,851,465],'demo'),
 ('dia-icon-picker','Icon picker','A rounded popover has an anchoring pointer. The tab, circular window controls and picker are different constructions.',[681,265,801,385],'demo'),
 ('dia-strategy-08','Full browser and code answer','A small window radius, rounder message/composer and compact toolbar control coexist. The sample code is page content, not implementation evidence.',[445,706,565,826],'published UI'),
 ('dia-signup','Signup form','Plain fields and a compact rounded button. The brand does not require large-radius surfaces everywhere.',[51,332,171,432],'published UI crop'),
 ('dia-group-chat-demo-4s','Group becomes chat context','The context tile repeats inside the composer. Contrast, inset and type hierarchy make it legible as an object.',[331,486,451,606],'demo'),
 ('arc-recovery','Arc Recovery Card','The black object has a rounded outer edge and inset border. Its silhouette works with strong contrast and a distinct information layout.',[123,348,243,468],'help screenshot'),
 ('arc-sync','Arc sync settings','A small-radius settings group sits next to a pill switch and circular thumb. Ordinary platform geometry remains visible.',[20,16,140,136],'help screenshot'),
 ('arc-routing','Arc routing sheet','Compact fields and dropdowns use modest radii. The large sheet and window retain a separate scale.',[217,193,337,313],'help screenshot'),
 ('dia-strategy-05','Composer closeup','A soft outer shell encloses a smaller context tile and icon mount. The Chat action is a capsule, not proof of a squircle formula.',[201,303,321,423],'isolated component'),
 ('dia-strategy-02','Tab closeup','Concave lower joins connect the selected tab to the content field. This is not a four-corner squircle.',[480,261,600,381],'isolated component'),
]

def uri(path):
    ext=path.suffix.lower(); mime='image/png' if ext=='.png' else 'image/jpeg'
    return f'data:{mime};base64,'+base64.b64encode(path.read_bytes()).decode()

def main():
    catalog={x['id']:x for x in json.loads((PRIOR/'evidence/catalog.json').read_text())}
    images={}; evidence=[]
    for id,title,note,crop,kind in OBSERVATIONS:
        item=catalog[id]; path=PRIOR/'evidence'/item['file']
        assert sha256(path.read_bytes()).hexdigest()==item['sha256']
        key='ref-'+id; images[key]=uri(path)
        with Image.open(path) as im:
            out=STUDY/f'evidence/{id}__corner.png'; im.crop(tuple(crop)).save(out)
        images[key+'-corner']=uri(out)
        evidence.append({**item, 'title':title,'observation':note,'crop':crop,'viewKind':kind,'image':key,
          'localSource':str(path.relative_to(REPO)),'cornerSha256':sha256(out.read_bytes()).hexdigest()})
    (STUDY/'evidence/catalog.json').write_text(json.dumps(evidence,indent=2)+'\n')
    results=json.loads((STUDY/'experiments/results.json').read_text())
    for case in results['records']:
        for record in case['records']:
            file=record['file'];images[file]=uri(STUDY/file)
            # Identical source-pixel crops across variants, derived from unchanged geometry.
            metrics=record['metrics']
            if case['evaluation']=='oncall-menubar':
                crop=[0,0,72,72]
            else:
                target=next(x for x in metrics['corners'] if (
                  ('sheet' in x['cls']) if 'help' in case['id'] else
                  ('btn-primary' in x['cls']) if case['evaluation']=='banking-onboarding' else
                  x['cls']=='sev'))
                x,y,w,h=target['rect']; crop=[max(0,int(x)-6),max(0,int(y)-6),min(case['viewport'][0],int(x)+84),min(case['viewport'][1],int(y)+min(int(h)+6,84))]
            with Image.open(STUDY/file) as im:
                out=STUDY/(file.replace('.png','__corner.png')); im.crop(tuple(crop)).save(out)
            record['crop']=crop; record['cornerFile']=str(out.relative_to(STUDY));images[record['cornerFile']]=uri(out)
            # Keep report payload compact; full measurements remain in results.json.
            del record['metrics']
    data=dict(evidence=evidence,results=results,images=images,factor=FACTOR,variants=list(VARIANTS))
    template=(STUDY/'tools/report-template.html').read_text()
    payload=json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')
    (STUDY/'index.html').write_text(template.replace('__DATA__',payload))
    print('Built offline report: 11 references, 80 full screenshots, 80 corner details.')
if __name__=='__main__': main()
