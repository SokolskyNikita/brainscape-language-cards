"""Apply three final wording refinements after the main sync completes."""
import json,csv,hashlib
from review import BASE,ROOT,FIELDS,save,read
from brainscape import cards_from_path,card_from_faces
from brainscape.cards import cards_match,card_write_payload
from brainscape.sync import validate_deck
from sync_cloud import PacedClient,log,OUT

def main():
 manifest=json.loads((BASE/'applied_manifest.json').read_text()); results=json.loads((OUT/'results.json').read_text())
 assert len(results)==20 and all(r['verified'] for r in results)
 pending=json.loads((BASE/'final_refinements_pending.json').read_text())
 client=PacedClient.discover()
 for deck,patch in pending.items():
  name=f'deck_{deck}.csv';source=ROOT/'english_russian'/name; m=next(m for m in manifest if m['deck']==deck)
  assert hashlib.sha256(source.read_bytes()).hexdigest()==m['sha256_after']
  before=cards_from_path(source);desired=list(before);remote=client.list_cards(21917816,int(deck))
  for row,v in patch.items():
   q,a,qe,ae=v;desired[int(row)-1]=card_from_faces(f'# Translate:\n\n{q}\n\n## Footnote\n\n{qe}',f'{a}\n\n## Footnote\n\n{ae}')
  assert len(remote)==500
  assert all(cards_match(cur,old) or cards_match(cur,new) for cur,old,new in zip(remote,before,desired))
  (OUT/f'{deck}_before_refinement.json').write_text(json.dumps(remote,ensure_ascii=False,indent=2)+'\n')
  for row in patch:
   ix=int(row)-1
   if not cards_match(remote[ix],desired[ix]):client.update_card(21917816,int(deck),remote[ix]['cardId'],**card_write_payload(desired[ix]))
  after=client.list_cards(21917816,int(deck));assert not validate_deck(after,desired)
  assert [c['cardId'] for c in after]==[c['cardId'] for c in remote]
  with source.open('w',newline='') as f:
   w=csv.writer(f);w.writerow(['Question','Answer']);w.writerows((c['question'],c['answer']) for c in desired)
  (BASE/'staged'/name).write_bytes(source.read_bytes());save(deck,patch)
  m['sha256_after']=hashlib.sha256(source.read_bytes()).hexdigest()
  r=next(r for r in results if r['deck']==deck);r['sha256']=m['sha256_after'];r['final_refinements_verified']=len(patch)
  log('refinements_verified',deck=deck,count=500,refinements=len(patch))
  (BASE/'applied_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
  (OUT/'results.json').write_text(json.dumps(results,indent=2)+'\n')
 changes=[]
 for m in manifest:
  for row,(before,after) in enumerate(zip(read(m['deck']),cards_from_path(ROOT/'english_russian'/f"deck_{m['deck']}.csv")),1):
   if not cards_match(before,after):changes.append(dict(deck=m['deck'],band=m['band'],row=row,before={k:before[k] for k in FIELDS},after={k:after[k] for k in FIELDS}))
  m['changed']=sum(c['deck']==m['deck'] for c in changes)
 (BASE/'changes.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2)+'\n')
 (BASE/'applied_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
 log('final_refinements_complete',changed_cards=len(changes))
if __name__=='__main__':main()
