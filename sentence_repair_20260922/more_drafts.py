from pathlib import Path
import json,re,sys
B=Path(__file__).resolve().parent;sys.path.insert(0,str(B.parent/'vocabulary_audit_20260922'))
from audit import W
p=json.loads((B/'plan.json').read_text());out=json.loads((B/'auto_drafts.json').read_text())
def third(v):
 if v=='have':return 'has'
 if re.search('[^aeiou]y$',v):return v[:-1]+'ies'
 return v+('es' if re.search('(s|sh|ch|x|z|o)$',v) else 's')
for x in p:
 key=f"{x['pack']}:{x['overall']}"
 if key in out:continue
 ws=[f['word'] for f in x['findings']];en=x['current_english_example'];ru=x['current_russian_example']
 if len(ws)!=1:continue
 w=ws[0];newen=None;newru=ru
 if w=='home':
  newen=re.sub(r'\bat home\b','here',en);newen=re.sub(r'\bhome\b','here',newen)
  if 'домой' in ru:continue
  newru=re.sub(r'\bдома\b','здесь',ru)
 elif w in {'just','pure','yet'}:
  newen=re.sub(r'\b'+w+r'\s*','',en,flags=re.I)
  rr={'just':r'\b(просто|только что|лишь)\s*','pure':r'\b(чистый|чистая|чистое|чистые)\s*','yet':r'\b(ещё|еще|пока)\s*'}[w]
  newru=re.sub(rr,'',ru,flags=re.I)
  if newru==ru:continue
 elif w.endswith('ing'):
  vs=W._morphy(w,'v')
  if not vs:continue
  base=vs[0]
  pat=r"\b(is|are|am)\s+(not\s+)?"+w+r'\b'
  def replacement(m):return (('does' if m[1]=='is' else 'do')+' not '+base) if m[2] else (third(base) if m[1]=='is' else base)
  newen,n=re.subn(pat,replacement,en)
  if not n:
   pat=r"(\b\w+)('s|'re|'m)\s+(not\s+)?"+w+r'\b'
   def repl(m):return m[1]+' '+((('does' if m[2]=="'s" else 'do')+' not '+base) if m[3] else third(base) if m[2]=="'s" else base)
   newen,n=re.subn(pat,repl,en)
  if not n:
   newen,n=re.subn(r'\b(love|loves|loved) '+w+r'\b',lambda m:m[1]+' to '+base,en)
  if not n:continue
 if not newen or newen==en:continue
 newen=newen[0].upper()+newen[1:];newru=newru[0].upper()+newru[1:]
 out[key]=dict(en=newen,ru=newru,method='simple_grammar_draft')
(B/'auto_drafts.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print('Total drafts:',len(out),'remaining:',len(p)-len(out))
