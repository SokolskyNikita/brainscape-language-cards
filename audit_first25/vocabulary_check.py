from pathlib import Path
from source_data import load_source
import json,re
from functools import lru_cache
import pymorphy3
from nltk.stem import WordNetLemmatizer
m=pymorphy3.MorphAnalyzer(); w=WordNetLemmatizer()
@lru_cache(None)
def forms(t,lang):
 t=t.lower().replace('ё','е')
 if lang=='ru': return {p.normal_form.replace('ё','е') for p in m.parse(t)}|{t}
 return {t}|set().union(*(set(w._morphy(t,pos)) for pos in ['n','v','a','r']))
def tokens(t): return re.findall(r"[a-zA-Zа-яА-ЯёЁ]+",t.lower())
stop_en=set('a an the i me my mine you your yours he him his she her hers it its we us our ours they them their theirs this that these those is am are was were be been being do does did have has had will would shall should can could may might must not no yes and or but if of in on at to for from with by as than so there here all some any every which what who whom whose how when where why s t m re ve ll d don didn doesn won isn aren wasn weren couldn wouldn shouldn hasn haven hadn let please something anything nothing everything'.split())
stop_ru=set('и а но в на к с со у по из за о об от до во не ни да нет это то что как который этот тот свой мой твой наш ваш его ее их он она оно они мы вы я ты себя весь такой уже еще вот бы же ли надо можно нельзя какой здесь там слишком'.split())
ds=load_source(); first={}; results=[]
for d in ds:
 pack=d['pack']; b=int(d['band'].split('->')[0]); b=0 if b==1 else b
 for lang,key in [('ru','q' if pack=='russian_english' else 'a'),('en','a' if pack=='russian_english' else 'q')]:
  for c in d['cards']:
   for t in tokens(c[key]):
    for f in forms(t,lang): first.setdefault((pack,lang,f),b)
for d in ds:
 pack=d['pack']; b=int(d['band'].split('->')[0]); b=0 if b==1 else b
 for c in d['cards'][:25]:
  problems={}
  for lang,key,ex in [('ru','q','qe'),('en','a','ae')] if pack=='russian_english' else [('en','q','qe'),('ru','a','ae')]:
   target=set().union(*(forms(t,lang) for t in tokens(c[key])))
   missing=[]
   for t in tokens(c[ex]):
    fs=forms(t,lang)
    if fs & target or fs & (stop_ru if lang=='ru' else stop_en):continue
    if lang=='ru' and any(p.tag.POS in {'PREP','CONJ','PRCL','NPRO','INTJ'} for p in m.parse(t)):continue
    earliest=min((first.get((pack,lang,f),99999) for f in fs))
    if earliest>b or (b>0 and earliest==b): missing.append((t,'absent' if earliest==99999 else earliest))
   if missing:problems[lang]=missing
  if problems:results.append(dict(pack=pack,band=d['band'],row=c['row'],word=c['q'],missing=problems))
json.dump(results,open(Path(__file__).with_name('vocabulary_candidates.json'),'w'),ensure_ascii=False,indent=2)
print('Candidate cards',len(results))
