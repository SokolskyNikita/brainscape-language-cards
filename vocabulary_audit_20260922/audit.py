"""Read-only English-example sequencing audit; never changes cards or contacts API."""
from pathlib import Path
from functools import lru_cache
from collections import defaultdict,Counter
import sys,json,re,hashlib,unicodedata
from nltk.stem import WordNetLemmatizer
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from brainscape import cards_from_path
BASE=Path(__file__).resolve().parent
W=WordNetLemmatizer()
# Explicit grammar exemption, reported separately from the literal rule.
GRAMMAR=set('a an the i me my mine you your yours he him his she her hers it its we us our ours they them their theirs this that these those is am are was were be been being do does did have has had will would shall should can could may might must not no yes and or but if of in on at to for from with by as than so there here all some any every which what who whom whose how when where why let please something anything nothing everything another other during everyone everybody someone somebody anyone anybody nobody across beyond within onto toward towards about between without against through throughout into neither'.split())
PRONOUNS=dict(zip('me my mine him his her hers us our ours them their theirs your yours'.split(),'i i i he he she she we we we they they they you you'.split()))
REFLEXIVES={t:'self' for t in 'myself yourself himself herself itself ourselves yourselves themselves oneself'.split()}
INFLECTIONS={**PRONOUNS,**REFLEXIVES,'an':'a','these':'this','those':'that','could':'can','would':'will','should':'shall','might':'may','towards':'toward','disc':'disk'}
@lru_cache(None)
def forms(t):
 t=t.lower(); n=INFLECTIONS.get(t,t)
 return frozenset({t,n}|{f for p in ['n','v','a','r'] for f in W._morphy(n,p)})
def tokens(s):
 s=s.lower().replace('’',"'")
 s=''.join(c for c in unicodedata.normalize('NFKD',s) if not unicodedata.combining(c))
 # Expand contractions; possessive 's contributes no new lexical word.
 s=re.sub(r"\bwon't\b",'will not',s);s=re.sub(r"\bcan't\b",'can not',s)
 s=re.sub(r'\bcannot\b','can not',s);s=re.sub(r"\bshan't\b",'shall not',s)
 s=re.sub(r"n't\b",' not',s)
 for suffix,full in [("'m",' am'),("'re",' are'),("'ve",' have'),("'ll",' will'),("'d",' would')]:s=re.sub(re.escape(suffix)+r'\b',full,s)
 s=re.sub(r"\b(it|he|she|that|there|here|what|who)'s\b",r'\1 is',s)
 s=re.sub(r"\blet's\b",'let us',s);s=re.sub(r"'s\b",'',s)
 return re.findall(r'[a-z]+',s)
def clean(s):return re.sub(r'\([^)]*\)','',s)
def main():
 summary={};all_findings=[];deck_results=[];evidence=[];shared_index=None;shared_solo=None
 for pack in ['english_russian','russian_english']:
  key,ex=('qMdBody','qMdFootnote') if pack=='english_russian' else ('aMdBody','aMdFootnote')
  mappings=re.findall(r'\| `(deck_\d+\.csv)` \| ([^|]+) \|',(ROOT/pack/'file_to_deck.md').read_text())
  decks=[];index=defaultdict(list);solo=defaultdict(list)
  for di,(filename,band) in enumerate(mappings):
   local=ROOT/pack/filename;live=BASE/'live'/pack/(local.stem[5:]+'.json')
   cards=json.loads(live.read_text()) if live.exists() else cards_from_path(local)
   assert len(cards)==500
   decks.append((filename,band.strip(),cards,'live' if live.exists() else 'local'))
   for row,c in enumerate(cards,1):
    head=clean(c[key]);ref=dict(deck_index=di,deck=local.stem[5:],row=row,overall=di*500+row,head=c[key])
    for t in set(tokens(head)):
     for f in forms(t):index[f].append(dict(ref,head_token=t))
    for alt in re.split(r'[,;/]|\s+or\s+',head):
     ts=tokens(re.sub(r'^\s*to\s+','',alt))
     if len(ts)==1:
      for f in forms(ts[0]):solo[f].append(ref)
  if pack=='english_russian':shared_index=index;shared_solo=solo
  else:index=shared_index;solo=shared_solo
  findings=[];matches=0
  for di,(filename,band,cards,source) in enumerate(decks):
   before=len(findings)
   for row,c in enumerate(cards,1):
    target=set().union(*(forms(t) for t in tokens(clean(c[key]))))
    for t in sorted(set(tokens(c.get(ex,'')))):
     fs=forms(t)
     if fs&target:continue
     refs=[r for f in fs for r in index[f]]
     earliest=min(refs,key=lambda r:r['overall']) if refs else None
     allowed=[r for r in refs if r['deck_index']<=max(0,di-1)]
     base=dict(pack=pack,deck=filename[5:-4],band=band,row=row,overall=di*500+row,head=c[key],example=c.get(ex,''),word=t)
     if allowed:
      matches+=1
      if not fs&GRAMMAR:
       r=min(allowed,key=lambda r:r['overall']);single=any(r['deck_index']<=max(0,di-1) for f in fs for r in solo[f])
       if not single:evidence.append(dict(base,earliest=r))
     else:
      findings.append(dict(base,grammar_exemption=bool(fs&GRAMMAR),reason='absent' if not earliest else ('same_deck' if earliest['deck_index']==di else 'later_deck'),earliest=earliest))
   subset=findings[before:]
   deck_results.append(dict(pack=pack,band=band,deck=filename[5:-4],cards=len(cards),source=source,content_violation_cards=len({x['row'] for x in subset if not x['grammar_exemption']}),literal_violation_cards=len({x['row'] for x in subset})))
  content=[x for x in findings if not x['grammar_exemption']]
  summary[pack]=dict(cards=sum(len(d[2]) for d in decks),decks=len(decks),content_violation_cards=len({x['overall'] for x in content}),content_word_card_pairs=len(content),literal_violation_cards=len({x['overall'] for x in findings}),literal_word_card_pairs=len(findings),literal_words=dict(Counter(x['word'] for x in findings)),supported_word_card_pairs=matches)
  all_findings.extend(findings)
 for name,obj in [('summary',summary),('findings',all_findings),('decks',deck_results),('phrase_evidence',evidence)]:
  (BASE/f'{name}.json').write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
