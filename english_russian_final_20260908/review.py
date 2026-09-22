from pathlib import Path
import sys,json,csv
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT))
from brainscape import cards_from_path,card_from_faces,card_write_payload
BASE=ROOT/'english_russian_final_20260908'
def patch(deck, changes):
 p=ROOT/'english_russian'/f'deck_{deck}.csv'; cards=cards_from_path(p); log=[]
 prior=BASE/f'{deck}.json'
 existing={c['row']:c for c in json.loads(prior.read_text())['changes']} if prior.exists() else {}
 for row,(a,qe,ae,reason) in changes.items():
  c=cards[row-1]; before=[c[k] for k in ['qMdBody','aMdBody','qMdFootnote','aMdFootnote']]
  after=[before[0],a or before[1],qe or before[2],ae or before[3]]
  cards[row-1]=card_from_faces(f'# Translate:\n\n{after[0]}\n\n## Footnote\n\n{after[2]}',f'{after[1]}\n\n## Footnote\n\n{after[3]}')
  entry=existing.get(row)
  if entry: before=entry['before']; reason=entry['reason']+' '+reason
  existing[row]=dict(row=row,before=before,after=after,reason=reason)
 with p.open('w',newline='') as f:
  w=csv.writer(f,lineterminator='\n');w.writerow(['Question','Answer'])
  for c in cards:
   v=card_write_payload(c);w.writerow([v['question'],v['answer']])
 (BASE/f'{deck}.json').write_text(json.dumps(dict(deck=deck,reviewed=500,changes=[existing[k] for k in sorted(existing)]),ensure_ascii=False,indent=2)+'\n')
 print(deck,'reviewed 500, changed',len(existing))
def dump(deck):
 for i,c in enumerate(cards_from_path(ROOT/'english_russian'/f'deck_{deck}.csv'),1):
  print(f"{i}|{c['qMdBody']}|{c['aMdBody']}|{c['qMdFootnote']}|{c['aMdFootnote']}")
if __name__=='__main__':dump(sys.argv[1])
