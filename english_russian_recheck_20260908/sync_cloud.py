"""In-place sync of the freshly rechecked English→Russian pack only."""
import hashlib,json,sys,time
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT))
from brainscape import BrainscapeClient,cards_from_path
from brainscape.cards import cards_match,card_write_payload
from brainscape.sync import validate_deck
from brainscape.errors import BrainscapeError
BASE=Path(__file__).resolve().parent
OUT=BASE/'cloud_sync';OUT.mkdir(exist_ok=True)
def log(event,**kw):
 r=dict(time=datetime.now(timezone.utc).isoformat(),event=event,**kw)
 with (OUT/'events.jsonl').open('a') as f:f.write(json.dumps(r,ensure_ascii=False)+'\n')
 print(json.dumps(r),flush=True)
class PacedClient(BrainscapeClient):
 last_request=0.
 def request(self,method,path,**kw):
  for attempt in range(8):
   time.sleep(max(0,.5-(time.monotonic()-self.last_request)))
   self.last_request=time.monotonic()
   try:return super().request(method,path,**kw)
   except BrainscapeError as e:
    if e.status!=429 or attempt==7:raise
    delay=min(60,15*2**attempt);log('rate_limit_backoff',seconds=delay);time.sleep(delay)
def main():
 client=PacedClient.discover();client.ping();results=[]
 manifest=json.loads((BASE/'applied_manifest.json').read_text())
 for ordinal,m in enumerate(manifest,1):
  deck=m['deck'];did=int(deck);pid=21917816;name=f'deck_{deck}.csv';source=ROOT/'english_russian'/name
  assert hashlib.sha256(source.read_bytes()).hexdigest()==m['sha256_after']
  old=cards_from_path(BASE/'originals'/name);desired=cards_from_path(source)
  remote=client.list_cards(pid,did)
  assert len(remote)==len(old)==len(desired)==500
  assert len({c['cardId'] for c in remote})==500
  for row,(before,cur,want) in enumerate(zip(old,remote,desired),1):
   assert cards_match(cur,before) or cards_match(cur,want),f'Concurrent live change: {deck} row {row}'
  backup=OUT/f'{deck}_before.json'
  if not backup.exists():backup.write_text(json.dumps(remote,ensure_ascii=False,indent=2)+'\n')
  updates=[(row,cur,want) for row,(cur,want) in enumerate(zip(remote,desired),1) if not cards_match(cur,want)]
  log('deck_start',ordinal=ordinal,deck=deck,band=m['band'],updates=len(updates))
  for i,(row,cur,want) in enumerate(updates,1):
   client.update_card(pid,did,cur['cardId'],**card_write_payload(want))
  after=client.list_cards(pid,did)
  assert not validate_deck(after,desired),f'Readback mismatch: {deck}'
  assert [c['cardId'] for c in after]==[c['cardId'] for c in remote],f'Identity/order changed: {deck}'
  r=dict(deck=deck,band=m['band'],count=len(after),updated=len(updates),verified=True,identities_preserved=True,sha256=m['sha256_after'],verified_at=datetime.now(timezone.utc).isoformat())
  results.append(r);(OUT/'results.json').write_text(json.dumps(results,indent=2)+'\n');log('deck_verified',ordinal=ordinal,**r)
 log('sync_complete',decks=len(results),cards=sum(r['count'] for r in results),updated=sum(r['updated'] for r in results))
if __name__=='__main__':
 try:main()
 except Exception as e:
  log('stopped',error_type=type(e).__name__,message=str(e));raise SystemExit(1)
