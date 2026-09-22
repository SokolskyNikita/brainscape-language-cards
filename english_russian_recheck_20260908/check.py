import sys,json
from review import ROOT,BASE,read,FIELDS
sys.path.insert(0,str(ROOT/'repair_20260907'))
from qa import forms,toks,function,target_present
entries=[m for m in json.loads((ROOT/'repair_20260907/applied_manifest.json').read_text()) if m['pack']=='english_russian']
first={};data={}
for ix,m in enumerate(entries):
 deck=m['deck']; cards=read(deck)
 p=BASE/'patches'/f'{deck}.json';patch=json.loads(p.read_text()) if p.exists() else {}
 for row,fields in patch.items():cards[int(row)-1].update(dict(zip(FIELDS,fields)))
 data[deck]=cards
 for c in cards:
  for lang,key in [('en','qMdBody'),('ru','aMdBody')]:
   for t in toks(c[key]):
    for f in forms(t,lang):first.setdefault((lang,f),ix)
issues=[]
for ix,m in enumerate(entries):
 for row,c in enumerate(data[m['deck']],1):
  errors={}
  for lang,k,e in [('en','qMdBody','qMdFootnote'),('ru','aMdBody','aMdFootnote')]:
   if not target_present(c[k],c[e],lang):errors[lang+'_target']=c[e]
   target=set().union(*(forms(t,lang) for t in toks(c[k])))
   missing=[t for t in toks(c[e]) if not function(t,lang) and not forms(t,lang)&target and min(first.get((lang,f),99) for f in forms(t,lang))>max(0,ix-1)]
   if missing:errors[lang+'_vocab']=missing
  if errors:issues.append({'deck':m['deck'],'row':row,'word':c['qMdBody'],'issues':errors})
(BASE/'qa.json').write_text(json.dumps(issues,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(issues,ensure_ascii=False,indent=2))
