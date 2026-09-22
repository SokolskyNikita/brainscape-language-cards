"""Validate review proposal references; never mutates decks."""
from pathlib import Path
from collections import defaultdict
import json
from helper import BASE
from brainscape import cards_from_path
FIELDS=['qMdBody','aMdBody','qMdFootnote','aMdFootnote']
def collect():
 grouped=defaultdict(list);errors=[];files=[]
 for p in sorted(BASE.glob('second_pass_final_*.json')):
  if p.stem.endswith('_reviewed'):continue
  data=json.loads(p.read_text());assert isinstance(data,list),p
  files.append(p.name)
  for f in data:
   try:
    pack,deck,row=f['pack'],str(f['deck']),int(f['row']);assert pack in ['russian_english','english_russian'] and 1<=row<=500
    assert len(f['before'])==len(f['after'])==4 and all(isinstance(s,str) and s.strip() for s in f['after'])
    cards=cards_from_path(BASE/'first_pass_snapshot'/pack/f'deck_{deck}.csv');current=[cards[row-1][k] for k in FIELDS]
    if current!=f['before']:errors.append(dict(file=p.name,deck=deck,row=row,problem='before differs from preserved first-pass card',current=current,before=f['before']))
    if pack=='russian_english' and f['after'][0]!=current[0]:errors.append(dict(file=p.name,deck=deck,row=row,problem='Russian source lemma changed'))
    grouped[(pack,deck,row)].append(dict(**f,source_file=p.name))
   except Exception as e:errors.append(dict(file=p.name,record=f,error=str(e)))
 conflicts=[dict(key=k,proposals=v) for k,v in grouped.items() if len({tuple(x['after']) for x in v})>1]
 report=dict(files=files,unique_cards=len(grouped),errors=errors,conflicts=conflicts)
 (BASE/'proposal_validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(dict(files=len(files),unique_cards=len(grouped),errors=len(errors),conflicts=len(conflicts))))
 return grouped,report
if __name__=='__main__':collect()
