"""Apply all 40 staged decks only after full human review and structural validation."""
from pathlib import Path
import hashlib,json,csv,shutil
from helper import ROOT,BASE,read
from brainscape import cards_from_path

def apply():
 qa=json.loads((BASE/'qa_current'/'summary.json').read_text())
 assert qa['decks']==40 and qa['structural_errors']==0 and qa['candidate_cards']==0, 'Run and resolve final QA before integration'
 manifest=json.loads((BASE/'manifest.json').read_text());summary=[]
 approved=json.loads((BASE/'approved_headword_changes.json').read_text())
 approved={(x['deck'],x['row']):(x['before'],x['after']) for x in approved}
 for m in manifest:
  pack,deck=m['pack'],m['deck'];name=f'deck_{deck}.csv'
  src=ROOT/pack/name;stage=BASE/'staged'/pack/name;log=BASE/'logs'/pack/f'deck_{deck}.json'
  assert stage.exists() and log.exists(),f'Missing reviewed output: {pack}/{deck}'
  assert hashlib.sha256(src.read_bytes()).hexdigest()==m['sha256'],f'Source changed since backup: {src}'
  old=read(pack,deck);new=cards_from_path(stage);data=json.loads(log.read_text())
  assert data['reviewed']==500 and len(new)==len(old)==500
  if pack=='russian_english':assert [c['qMdBody'] for c in new]==[c['qMdBody'] for c in old]
  else:
   for row,(a,b) in enumerate(zip(old,new),1):
    if a['qMdBody']!=b['qMdBody']:assert approved.get((deck,row))==(a['qMdBody'],b['qMdBody']),f'Unreviewed English headword change {deck}/{row}'
  with stage.open(newline='') as f:
   rows=list(csv.reader(f));assert rows[0]==['Question','Answer'] and len(rows)==501 and all(len(r)==2 for r in rows)
  for row,c in enumerate(new,1):
   assert all(c.get(k,'').strip() for k in ['qMdBody','aMdBody','qMdFootnote','aMdFootnote']),f'{deck}/{row} blank'
   assert c['qMdPrompt']=='Translate:'
   assert '\n\n## Footnote\n\n' in c['question'] and '\n\n## Footnote\n\n' in c['answer']
  fields=['qMdBody','aMdBody','qMdFootnote','aMdFootnote']
  changed=sum(any(a[k]!=b[k] for k in fields) for a,b in zip(old,new))
  summary.append(dict(**m,reviewed=500,changed=changed,sha256_after=hashlib.sha256(stage.read_bytes()).hexdigest()))
 for s in summary:
  pack,deck=s['pack'],s['deck'];name=f'deck_{deck}.csv';dest=ROOT/pack/name;temporary=dest.with_suffix('.csv.repair_tmp')
  shutil.copyfile(BASE/'staged'/pack/name,temporary);temporary.replace(dest)
  assert hashlib.sha256(dest.read_bytes()).hexdigest()==s['sha256_after']
 (BASE/'applied_manifest.json').write_text(json.dumps(summary,indent=2)+'\n')
 for pack in ['russian_english','english_russian']:
  count=sum(s['changed'] for s in summary if s['pack']==pack)
  (ROOT/pack/'REPAIR_STATUS.md').write_text(f'''# Full-deck repair — 2026-09-07

All 20 top-level deck CSVs (10,000 cards) were reviewed for translations, examples, target use, and vocabulary sequencing. {count:,} cards were changed locally. Card counts and sequence were preserved.

The top-level `deck_*.csv` files are the current corrected decks. Original snapshots, complete change logs, patch scripts, and validation records are in `../repair_20260907/`.

`_chunks/`, `_chunks/fixed/`, old rewrite scripts, and `_vocab/` predate this repair. They are historical working artifacts; do not merge or run them over the corrected top-level decks. Regenerate working chunks from the current CSVs before another editing round.

The current vocabulary rule is **prior decks only**, except that the first 1→500 deck may use its own full vocabulary. The target itself and common function words are allowed. Older fixer-guide language allowing the current deck in later bands is superseded by this user instruction.

No Brainscape upload was performed by this repair.
''')
 print(json.dumps(dict(decks=len(summary),reviewed=sum(s['reviewed'] for s in summary),changed=sum(s['changed'] for s in summary),by_pack={p:sum(s['changed'] for s in summary if s['pack']==p) for p in ['russian_english','english_russian']}),indent=2))
if __name__=='__main__':apply()
