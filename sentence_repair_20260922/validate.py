"""Re-run vocabulary and bilingual target checks against staged or verified live decks."""
from pathlib import Path
import argparse,contextlib,hashlib,io,json,sys
B=Path(__file__).resolve().parent;R=B.parent
sys.path[:0]=[str(R),str(R/'vocabulary_audit_20260922'),str(R/'repair_20260907')]
import conditional_audit as audit
from exact_audit import load
from qa import target_present
from brainscape.cards import card_write_payload

def main(live=False):
 decks,manifest=load();changes=json.loads((B/'changes.json').read_text());flags=[]
 for x in changes:
  c=x['after_card'];ek,rk=('q','a') if x['pack']=='english_russian' else ('a','q')
  for lang,k in [('en',ek),('ru',rk)]:
   if not target_present(c[k+'MdBody'],c[k+'MdFootnote'],lang):flags.append({'pack':x['pack'],'overall':x['overall'],'language':lang})
 assert not flags,flags
 if live:
  for pack,ds in decks.items():
   for d in ds:
    did=int(Path(d['file']).stem.split('_')[1]);cards=json.loads((B/'after'/pack/f'{did}.json').read_text())
    assert [c['cardId'] for c in cards]==[c['cardId'] for c in d['cards']]
    d['cards']=cards
  for x in changes:
   di,row=divmod(x['overall']-1,500)
   assert card_write_payload(decks[x['pack']][di]['cards'][row])==card_write_payload(x['after_card'])
 else:
  for x in changes:
   di,row=divmod(x['overall']-1,500);decks[x['pack']][di]['cards'][row]=x['after_card']
 manifest=[]
 for pack,ds in decks.items():
  for d in ds:
   did=d['file'][5:-4]
   source=B/'after'/pack/f'{did}.json' if live else B/'staged'/pack/d['file']
   d['source']=str(source.relative_to(R))
   manifest.append(dict(pack=pack,deck=did,cards=len(d['cards']),source=d['source'],sha256=hashlib.sha256(source.read_bytes()).hexdigest()))
 reviews=json.loads((R/'vocabulary_audit_20260922/meaning/sense_reviews.json').read_text())+json.loads((B/'new_sense_reviews.json').read_text())
 lookup={(v['pack'],v['overall'],v['word']):v for v in reviews}
 audit.load=lambda:(decks,manifest)
 output=B/('qa_live' if live else 'qa');output.mkdir(exist_ok=True)
 with contextlib.redirect_stdout(io.StringIO()):result=audit.main(sense_reviews=lookup,output_base=output)
 assert not result[2],result[2]
 result={'source':'verified cloud snapshots' if live else 'staged replacements','cards_audited':sum(len(d['cards']) for ds in decks.values() for d in ds),'vocabulary_flags':0,'changed_cards_checked_for_bilingual_targets':len(changes),'target_presence_flags':0,'english_examples_changed':len(changes),'russian_translations_changed':sum(x['after_russian_example']!=x['current_russian_example'] for x in changes)}
 (output/'repair_validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--live',action='store_true');main(p.parse_args().live)
