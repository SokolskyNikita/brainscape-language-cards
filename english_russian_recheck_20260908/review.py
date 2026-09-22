import sys,json,csv
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT))
from brainscape import cards_from_path,card_from_faces,card_write_payload
BASE=Path(__file__).resolve().parent
FIELDS=['qMdBody','aMdBody','qMdFootnote','aMdFootnote']
def read(deck):return cards_from_path(BASE/'originals'/f'deck_{deck}.csv')
def save(deck,patches):
 p=BASE/'patches'/f'{deck}.json'
 old=json.loads(p.read_text()) if p.exists() else {}
 old.update({str(k):v for k,v in patches.items()})
 p.write_text(json.dumps(old,ensure_ascii=False,indent=2)+'\n')
def dump(deck,start,end):
 for i,c in enumerate(read(deck),1):
  if start<=i<=end: print(str(i)+' | '+' | '.join(c.get(k,'') for k in FIELDS))
if __name__=='__main__':dump(sys.argv[1],int(sys.argv[2]),int(sys.argv[3]))
