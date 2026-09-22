from pathlib import Path
import sys,json,csv,copy,contextlib,io
B=Path(__file__).resolve().parent;R=B.parent
sys.path[:0]=[str(R),str(R/'vocabulary_audit_20260922')]
from brainscape import cards_from_path,card_from_faces
from brainscape.cards import card_write_payload
import conditional_audit as audit
from exact_audit import load,tokens

def main():
 plan=json.loads((B/'plan.json').read_text());repl=json.loads((B/'replacements.json').read_text())
 decks,manifest=load();changes=[]
 for x in plan:
  key=f"{x['pack']}:{x['overall']}";r=repl[key];di,row=divmod(x['overall']-1,500)
  d=decks[x['pack']][di];c=d['cards'][row];en,ru=('qMdFootnote','aMdFootnote') if x['pack']=='english_russian' else ('aMdFootnote','qMdFootnote')
  assert c[en]==x['current_english_example'] and c[ru]==x['current_russian_example']
  assert r['en']!=c[en],key
  original=copy.deepcopy(c)
  c[en]=r['en'];c[ru]=r['ru']
  changed=card_from_faces(f"# Translate:\n\n{c['qMdBody']}\n\n## Footnote\n\n{c['qMdFootnote']}",f"{c['aMdBody']}\n\n## Footnote\n\n{c['aMdFootnote']}")
  c.update(changed)
  changes.append(dict(**x,after_english_example=r['en'],after_russian_example=r['ru'],before_card=original,after_card=c))
 for pack,ds in decks.items():
  out=B/'staged'/pack;out.mkdir(parents=True,exist_ok=True)
  for d in ds:
   with (out/d['file']).open('w',newline='') as f:
    w=csv.writer(f,lineterminator='\n');w.writerow(['Question','Answer'])
    for c in d['cards']:w.writerow([c['question'],c['answer']])
   check=cards_from_path(out/d['file']);assert len(check)==500
   original=cards_from_path(B/'originals'/pack/d['file'])
   assert [(c['qMdBody'],c['aMdBody']) for c in check]==[(c['qMdBody'],c['aMdBody']) for c in original]
 (B/'changes.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2)+'\n')
 reviews=json.loads((R/'vocabulary_audit_20260922/meaning/sense_reviews.json').read_text())
 extra=B/'new_sense_reviews.json'
 if extra.exists():reviews+=json.loads(extra.read_text())
 lookup={(x['pack'],x['overall'],x['word']):x for x in reviews}
 stale=[]
 for key,v in list(lookup.items()):
  pack,n,word=key;di,row=divmod(n-1,500);c=decks[pack][di]['cards'][row];ex=c['qMdFootnote' if pack=='english_russian' else 'aMdFootnote']
  if word in tokens(ex) and v['action']=='resolve_sense' and v['example']!=ex:stale.append(dict(old=v,new_example=ex));del lookup[key]
 (B/'stale_sense_reviews.json').write_text(json.dumps(stale,ensure_ascii=False,indent=2))
 audit.load=lambda:(decks,manifest)
 qa=B/'qa';qa.mkdir(exist_ok=True)
 with contextlib.redirect_stdout(io.StringIO()):result=audit.main(sense_reviews=lookup,output_base=qa)
 flags=result[2]
 print('Staged:',len(changes),'Vocabulary flags:',len(flags),'stale semantic contexts:',len(stale))
 for x in flags:print(x['pack'][:2],x['overall'],x['head'],'|',x['example'],'|',x['word'],x['reason'])
if __name__=='__main__':main()
