"""Structural checks plus morphology-based review candidates. Candidates require human judgment."""
from pathlib import Path
from functools import lru_cache
from collections import Counter
import json,re,sys,argparse
import pymorphy3
from nltk.stem import WordNetLemmatizer
from helper import ROOT,BASE,read
from brainscape import cards_from_path,card_from_faces
M=pymorphy3.MorphAnalyzer();W=WordNetLemmatizer()
STOP_EN=set('a an the i me my mine you your yours he him his she her hers it its we us our ours they them their theirs this that these those is am are was were be been being do does did have has had will would shall should can could may might must not no yes and or but if of in on at to for from with by as than so there here all some any every which what who whom whose how when where why s t m re ve ll d don didn doesn won isn aren wasn weren couldn wouldn shouldn hasn haven hadn let please something anything nothing everything another other during everyone everybody someone somebody anyone anybody nobody across beyond within onto toward towards about between without against through throughout'.split())
STOP_RU=set('и а но в на к с со у по из за о об от до во не ни да нет это то что как который этот тот свой мой твой наш ваш его ее их он она оно они мы вы я ты себя весь такой уже еще вот бы же ли надо можно нельзя какой здесь там слишком пожалуйста другой должный'.split())
EN_FORMS={'cannot':'can','us':'we','them':'they','him':'he','her':'she','me':'i','my':'i','our':'we','their':'they','his':'he','your':'you','mine':'i','ours':'we','theirs':'they','hers':'she','yours':'you','myself':'self','yourself':'self','himself':'self','herself':'self','itself':'self','ourselves':'self','yourselves':'self','themselves':'self','oneself':'self'}
@lru_cache(None)
def forms(t,lang):
 t=t.lower().replace('ё','е')
 if lang=='ru':return frozenset({t}|{p.normal_form.replace('ё','е') for p in M.parse(t)})
 return frozenset({t,EN_FORMS.get(t,t)}|set().union(*(set(W._morphy(t,p)) for p in ['n','v','a','r'])))
def toks(t):return re.findall(r'[a-zа-яё]+',t.lower())
def function(t,lang):
 fs=forms(t,lang)
 if lang=='en':return bool(fs&STOP_EN)
 return bool(fs&STOP_RU) or any((p.tag.POS in {'PREP','CONJ','PRCL','NPRO','INTJ'} or 'Apro' in p.tag) for p in M.parse(t))
def parts(t):
 t=re.sub(r'\([^)]*\)','',t)
 t=re.sub(r"\bone['’]s\s+",'',t)
 return [p.strip() for p in re.split(r'[,;/]|\s+or\s+',t) if p.strip()]
def target_present(lemma,example,lang):
 es=set().union(*(forms(t,lang) for t in toks(example))) if toks(example) else set()
 for alt in parts(lemma):
  tokens=toks(alt)
  if lang=='en' and len(tokens)>1 and tokens[0]=='to':tokens=tokens[1:]
  core=[t for t in tokens if not function(t,lang)] or tokens
  if core and all(forms(t,lang)&es for t in core):return True
 return False
def inspect(originals=False,deck=None,preview=False):
 proposal_map={}
 if preview:
  for p in BASE.glob("second_pass_final_*.json"):
   if p.stem.endswith("_reviewed"):continue
   for f in json.loads(p.read_text()):proposal_map[(f["pack"],str(f["deck"]),int(f["row"]))]=f["after"]
 manifest=json.loads((BASE/'manifest.json').read_text());allcards={};first={}
 for item in manifest:
  pack,id=item['pack'],item['deck'];path=BASE/('originals' if originals else 'staged')/pack/f'deck_{id}.csv'
  if not path.exists():path=BASE/'originals'/pack/f'deck_{id}.csv'
  cards=cards_from_path(path)
  if preview:
   for row in range(1,len(cards)+1):
    if (pack,id,row) in proposal_map:
     q,a,qe,ae=proposal_map[(pack,id,row)]
     cards[row-1]=card_from_faces(f'# Translate:\n\n{q}\n\n## Footnote\n\n{qe}',f'{a}\n\n## Footnote\n\n{ae}')
  allcards[(pack,id)]=cards
  band=int(item['band'].split('->')[0]);band=0 if band==1 else band
  for c in cards:
   for lang,key in [('ru','qMdBody'),('en','aMdBody')] if pack=='russian_english' else [('en','qMdBody'),('ru','aMdBody')]:
    for t in toks(re.sub(r'\([^)]*\)','',c[key])):
     for f in forms(t,lang):first.setdefault((pack,lang,f),band)
 reports=[]
 for item in manifest:
  pack,id=item['pack'],item['deck']
  if deck and id!=deck:continue
  band=int(item['band'].split('->')[0]);band=0 if band==1 else band
  cards=allcards[(pack,id)];original=read(pack,id);errs=[];candidates=[]
  if len(cards)!=500:errs.append(f'Expected 500 cards, got {len(cards)}')
  if pack=='russian_english' and [c['qMdBody'] for c in cards]!=[c['qMdBody'] for c in original]:errs.append('Russian question lemmas changed or reordered')
  seen={}
  for row,c in enumerate(cards,1):
   for k in ['qMdBody','aMdBody','qMdFootnote','aMdFootnote']:
    if not c.get(k,'').strip():errs.append(f'{row}: empty {k}')
   if c.get('qMdPrompt')!='Translate:':errs.append(f'{row}: bad prompt')
   key=(c['qMdBody'],c['aMdBody'],c.get('qMdFootnote'),c.get('aMdFootnote'))
   if key in seen:errs.append(f'{row}: exact duplicate of row {seen[key]}')
   seen[key]=row
   issues={}
   for lang,key,ex in [('ru','qMdBody','qMdFootnote'),('en','aMdBody','aMdFootnote')] if pack=='russian_english' else [('en','qMdBody','qMdFootnote'),('ru','aMdBody','aMdFootnote')]:
    if not target_present(c[key],c.get(ex,''),lang):issues[f'{lang}_target']=f"{c[key]} | {c.get(ex,'')}"
    target=set().union(*(forms(t,lang) for t in toks(c[key])))
    missing=[]
    for t in toks(c.get(ex,'')):
     if function(t,lang) or forms(t,lang)&target:continue
     earliest=min(first.get((pack,lang,f),99999) for f in forms(t,lang))
     if earliest>band or (band>0 and earliest==band):missing.append(dict(word=t,band='absent' if earliest==99999 else f'{earliest}->{earliest+500}'))
    if missing:issues[f'{lang}_vocab']=missing
    if lang=='ru' and re.search(r'[A-Za-z]{3,}',c.get(ex,'')):issues['latin_in_russian']=c.get(ex,'')
    if len(toks(c.get(ex,'')))>12:issues[f'{lang}_long']=c.get(ex,'')
   if re.search(r"I.m sorry|cannot fulfill|can't fulfill|as an AI|language model",c['question']+' '+c['answer'],re.I):errs.append(f'{row}: refusal text')
   if issues:candidates.append(dict(row=row,q=c['qMdBody'],a=c['aMdBody'],qe=c.get('qMdFootnote',''),ae=c.get('aMdFootnote',''),issues=issues))
  reports.append(dict(**item,errors=errs,candidates=candidates))
 folder=BASE/('qa_preview' if preview else ('qa_baseline' if originals else 'qa_current'));folder.mkdir(exist_ok=True)
 for r in reports:(folder/f"{r['pack']}_{r['deck']}.json").write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
 summary=dict(decks=len(reports),structural_errors=sum(len(r['errors']) for r in reports),candidate_cards=sum(len(r['candidates']) for r in reports),candidate_types=dict(Counter(k for r in reports for c in r['candidates'] for k in c['issues'])))
 (folder/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary))
 return reports
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--originals',action='store_true');p.add_argument('--deck');p.add_argument('--preview',action='store_true');a=p.parse_args();inspect(a.originals,a.deck,a.preview)
