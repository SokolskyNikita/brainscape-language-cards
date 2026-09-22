import sys,json,time,hashlib
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from brainscape import BrainscapeClient,cards_from_path
from brainscape.cards import cards_match,card_write_payload
from brainscape.sync import validate_deck
from brainscape.errors import BrainscapeError
BASE=ROOT/'english_russian_final_20260908';OUT=BASE/'cloud_sync';OUT.mkdir(exist_ok=True)
class PacedClient(BrainscapeClient):
 last_request=0
 def request(self,method,path,**kwargs):
  for attempt in range(8):
   time.sleep(max(0,.5-(time.monotonic()-self.last_request)));self.last_request=time.monotonic()
   try:return super().request(method,path,**kwargs)
   except BrainscapeError as e:
    if e.status!=429 or attempt==7:raise
    time.sleep(min(60,15*2**attempt))
def main():
 client=PacedClient.discover();client.ping();results=[]
 for p in sorted((ROOT/'english_russian').glob('deck_*.csv')):
  deck=int(p.stem[5:]);want=cards_from_path(p);old=cards_from_path(BASE/'originals'/p.name);remote=client.list_cards(21917816,deck)
  assert len(remote)==len(want)==len(old)==500
  for row,(a,b,c) in enumerate(zip(old,remote,want),1):
   assert cards_match(b,a) or cards_match(b,c),f'Live conflict: {deck} row {row}'
  backup=OUT/f'{deck}_before.json'
  if not backup.exists():backup.write_text(json.dumps(remote,ensure_ascii=False,indent=2))
  changes=[(b,c) for b,c in zip(remote,want) if not cards_match(b,c)]
  print('Updating',deck,len(changes),'cards',flush=True)
  for b,c in changes:client.update_card(21917816,deck,b['cardId'],**card_write_payload(c))
  after=client.list_cards(21917816,deck)
  assert not validate_deck(after,want)
  assert [c['cardId'] for c in after]==[c['cardId'] for c in remote]
  result=dict(deck=deck,updated=len(changes),verified_cards=500,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),verified_at=datetime.now(timezone.utc).isoformat())
  results.append(result);(OUT/'results.json').write_text(json.dumps(results,indent=2))
  print('Verified',deck,flush=True)
 print('COMPLETE',sum(r['updated'] for r in results),'updated;',len(results)*500,'verified',flush=True)
if __name__=='__main__':main()
