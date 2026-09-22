from pathlib import Path
import sys,json,csv,re,hashlib
ROOT=Path(__file__).resolve().parent.parent
BASE=ROOT/'repair_20260907'
sys.path.insert(0,str(ROOT))
from brainscape import cards_from_path,card_from_faces,card_write_payload

def read(pack,deck):
 p=BASE/'originals'/pack/f'deck_{deck}.csv'
 return cards_from_path(p)

def dump(pack,deck,start=1,end=500):
 for n,c in enumerate(read(pack,deck),1):
  if start<=n<=end: print(f"{n}: {c['qMdBody']} → {c['aMdBody']} | {c.get('qMdFootnote','')} / {c.get('aMdFootnote','')}")

def save(pack,deck,patches,reviewed=500,notes=''):
 """patches: row -> (question lemma, answer lemma, question example, answer example). All strings. Omit unchanged rows."""
 cards=read(pack,deck); before=[dict(c) for c in cards]
 assert len(cards)==reviewed==500
 for row,fields in patches.items():
  assert isinstance(row,int) and 1<=row<=500
  assert len(fields)==4 and all(isinstance(x,str) and x.strip() for x in fields)
  q,a,qe,ae=(x.strip() for x in fields)
  if pack=='russian_english': assert q==before[row-1]['qMdBody'],f'Preserve Russian lemma at {row}'
  cards[row-1]=card_from_faces(f'# Translate:\n\n{q}\n\n## Footnote\n\n{qe}',f'{a}\n\n## Footnote\n\n{ae}')
 out=BASE/'staged'/pack/f'deck_{deck}.csv';out.parent.mkdir(parents=True,exist_ok=True)
 temporary=out.with_suffix('.csv.tmp')
 with temporary.open('w',newline='',encoding='utf-8') as fh:
  w=csv.writer(fh,lineterminator='\n');w.writerow(['Question','Answer'])
  for c in cards:
   p=card_write_payload(c);w.writerow([p['question'],p['answer']])
 temporary.replace(out)
 changes=[dict(row=i+1,before={k:c.get(k,'') for k in ['qMdBody','aMdBody','qMdFootnote','aMdFootnote']},after={k:cards[i].get(k,'') for k in ['qMdBody','aMdBody','qMdFootnote','aMdFootnote']}) for i,c in enumerate(before) if any(c.get(k,'')!=cards[i].get(k,'') for k in ['qMdBody','aMdBody','qMdFootnote','aMdFootnote'])]
 log=BASE/'logs'/pack/f'deck_{deck}.json';log.parent.mkdir(parents=True,exist_ok=True)
 log.write_text(json.dumps(dict(deck=str(deck),pack=pack,reviewed=reviewed,changed=len(changes),notes=notes,changes=changes),ensure_ascii=False,indent=2)+'\n')
 print(f'{pack}/{deck}: reviewed {reviewed}, changed {len(changes)}, staged {out}')
 return cards
if __name__=='__main__':dump(sys.argv[1],sys.argv[2],int(sys.argv[3]) if len(sys.argv)>3 else 1,int(sys.argv[4]) if len(sys.argv)>4 else 500)
