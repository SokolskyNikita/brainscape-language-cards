from pathlib import Path
import sys,json,re
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'repair_20260907'))
from qa import forms,toks,function,target_present,STOP_EN
STOP_EN.update({"into", "neither"})  # Basic preposition; not supporting content vocabulary.
from review import ROOT,BASE,cards_from_path
paths=sorted((ROOT/'english_russian').glob('deck_*.csv')); decks=[cards_from_path(p) for p in paths];first={};issues=[];errors=[];changed=0
for band,cards in enumerate(decks):
 for c in cards:
  for lang,key in [('en','qMdBody'),('ru','aMdBody')]:
   for t in toks(re.sub(r'\([^)]*\)','',c[key])):
    for f in forms(t,lang):first.setdefault((lang,f),band)
for band,(p,cards) in enumerate(zip(paths,decks)):
 old=cards_from_path(BASE/'originals'/p.name)
 assert len(cards)==len(old)==500
 assert [c['qMdBody'] for c in cards]==[c['qMdBody'] for c in old]
 for row,c in enumerate(cards,1):
  keys=['qMdBody','aMdBody','qMdFootnote','aMdFootnote'];assert all(c[k].strip() for k in keys)
  changed+=any(c[k]!=old[row-1][k] for k in keys)
  flags={}
  for lang,key,ex in [('en','qMdBody','qMdFootnote'),('ru','aMdBody','aMdFootnote')]:
   if not target_present(c[key],c[ex],lang):flags[lang+'_target']=True
   target=set().union(*(forms(t,lang) for t in toks(c[key])))
   missing=[]
   for t in toks(c[ex]):
    if function(t,lang) or forms(t,lang)&target:continue
    earliest=min(first.get((lang,f),999) for f in forms(t,lang))
    if earliest>band or (band>0 and earliest==band):missing.append(t)
   if missing:flags[lang+'_vocab']=missing
  if flags:issues.append(dict(deck=p.stem[5:],row=row,card=[c[k] for k in keys],flags=flags))
(BASE/'qa.json').write_text(json.dumps(issues,ensure_ascii=False,indent=2))
print('10,000 cards; preserved heads/order; nonempty fields; changed:',changed,'candidates:',len(issues))
for i in issues:print(i['deck'],i['row'],'|'.join(i['card']),i['flags'])
