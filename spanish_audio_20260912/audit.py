import json,re,unicodedata,difflib
from pathlib import Path
from spanish_audio_20260912.review import read
R=Path(__file__).resolve().parent
packs=json.loads((R/'packs.json').read_text())
def norm(t):return ''.join(c for c in unicodedata.normalize('NFD',t.lower()) if not unicodedata.combining(c))
def present_es(w,s):
 w=norm(w);s=norm(s);tokens=re.findall(r'[a-z]+',s)
 if w in s:return True
 if len(w)>3 and any(t.startswith(w[:-2]) for t in tokens):return True
 return False
stop={'to','a','an','the','i','you','we','he','she','it','they','of','for','on','in','at','my','your','his','her','our','their','be','me','us','him','them','oneself','ones','all','have','will','would','am','is','are','was','were','has','had'}
def present_en(w,s):
 w=re.sub(r'\([^)]*\)','',w.lower());s=s.lower()
 for sense in w.split(','):
  ts=[x for x in re.findall('[a-z]+',sense) if x not in stop]
  if not ts:return True
  if all(t in s or (len(t)>4 and t[:-2] in s) for t in ts):return True
 return False
rows=[]
for d in packs[0]['decks'][3:]:
 cs=read(d['deckId']);flags=[]
 for i,c in enumerate(cs,1):
  q,a,qe,ae=[c.get(k) or '' for k in ['qMdBody','aMdBody','qMdFootnote','aMdFootnote']]
  why=[]
  if not present_es(a,ae):why.append('ES target')
  if not present_en(q,qe):why.append('EN target')
  if not all([q,a,qe,ae]):why.append('empty')
  if '(imperative' in q and re.search(r'\bno\b',ae,re.I):why.append('negative imperative')
  if 'subjunctive' in q:why.append('subjunctive')
  if why:flags.append({'deck':d['deckId'],'row':i,'why':why,'fields':[q,a,qe,ae]})
 rows.extend(flags);print(d['deckId'],len(flags))
(R/'candidates.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
print('Total',len(rows))
