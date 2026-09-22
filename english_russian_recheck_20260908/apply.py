import json,csv,hashlib
from datetime import datetime,timezone
from review import ROOT,BASE,FIELDS,read
from brainscape import cards_from_path,card_from_faces
from brainscape.cards import cards_match
entries=[m for m in json.loads((ROOT/'repair_20260907/applied_manifest.json').read_text()) if m['pack']=='english_russian']
manifest=[];log=[]
for m in entries:
 deck=m['deck']; source=ROOT/'english_russian'/f'deck_{deck}.csv'; original=BASE/'originals'/source.name
 assert source.read_bytes()==original.read_bytes(),f'Concurrent source change: {source}'
 old=read(deck); new=list(old)
 patch=json.loads((BASE/'patches'/f'{deck}.json').read_text())
 for row,values in patch.items():
  assert len(values)==4 and all(v.strip() for v in values)
  ix=int(row)-1; q,a,qe,ae=values
  new[ix]=card_from_faces(f'# Translate:\n\n{q}\n\n## Footnote\n\n{qe}',f'{a}\n\n## Footnote\n\n{ae}')
  if not cards_match(old[ix],new[ix]):log.append(dict(deck=deck,band=m['band'],row=int(row),before={k:old[ix][k] for k in FIELDS},after={k:new[ix][k] for k in FIELDS}))
 assert len(old)==len(new)==500
 keys=[tuple(c[k] for k in FIELDS) for c in new]
 assert len(keys)==len(set(keys)),f'Duplicate full card: {deck}'
 staged=BASE/'staged'/source.name;staged.parent.mkdir(exist_ok=True)
 with staged.open('w',newline='') as f:
  w=csv.writer(f);w.writerow(['Question','Answer']);w.writerows((c['question'],c['answer']) for c in new)
 assert all(cards_match(a,b) for a,b in zip(cards_from_path(staged),new))
 manifest.append(dict(deck=deck,pack='english_russian',pack_id=21917816,band=m['band'],reviewed=500,changed=sum(x['deck']==deck for x in log),sha256_before=hashlib.sha256(original.read_bytes()).hexdigest(),sha256_after=hashlib.sha256(staged.read_bytes()).hexdigest()))
# Validate the complete batch before writing any source file.
for m in manifest:
 path=ROOT/'english_russian'/f"deck_{m['deck']}.csv"
 path.write_bytes((BASE/'staged'/path.name).read_bytes())
(BASE/'applied_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
(BASE/'changes.json').write_text(json.dumps(log,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(reviewed=sum(m['reviewed'] for m in manifest),changed=len(log),decks=len(manifest))))
