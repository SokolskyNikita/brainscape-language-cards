"""Patch the reviewed card IDs, replace English audio, then verify every deck."""
from pathlib import Path
import argparse,concurrent.futures,hashlib,json,shutil,sys,threading,time
from urllib.request import urlopen
B=Path(__file__).resolve().parent;R=B.parent;sys.path.insert(0,str(R))
from brainscape import BrainscapeClient,cards_from_path
from brainscape.cards import card_write_payload
from generate_audio import manifest,atomic,load_manifest,audio_path

def main(apply=False):
 changes=json.loads((B/'changes.json').read_text());m=load_manifest()
 assert m==manifest(),'Plan changed after audio generation'
 assert json.loads((B/'audio_result.json').read_text())['status']=='complete'
 assert not json.loads((B/'qa/final_findings.json').read_text())
 assert not json.loads((B/'stale_sense_reviews.json').read_text())
 client=BrainscapeClient.discover(retries=3,timeout=60)
 byid={x['cardId']:x for x in changes};audio={i['cardId']:i for i in m['items']};assert len(byid)==len(audio)==744
 pairs=sorted({(x['pack'],x['packId'],x['deckId']) for x in changes});assert len(pairs)==40
 for folder in ['receipts','after','verified']:(B/folder).mkdir(exist_ok=True)
 hashes={}
 for i in m['items']:
  p=audio_path(i);h=hashlib.sha256(p.read_bytes()).hexdigest()
  assert h==json.loads(p.with_suffix('.json').read_text())['sha256'];hashes[i['cardId']]=h
 def baseline(pack,did):return json.loads((B/'before'/pack/f'{did}.json').read_text())
 def assert_deck(pair,live,final=False):
  pack,pid,did=pair;old=baseline(pack,did)
  assert len(live)==len(old)==500 and [c['cardId'] for c in live]==[c['cardId'] for c in old],f'IDs/order changed: {did}'
  for a,b in zip(old,live):
   x=byid.get(a['cardId']);before=card_write_payload(a);actual=card_write_payload(b)
   if x:
    desired=card_write_payload(x['after_card'])
    assert before==card_write_payload(x['before_card']),f'Baseline changed on {a["cardId"]}'
    assert actual==desired or (not final and actual==before),f'Text conflict on {a["cardId"]}'
    other='aSoundUrl' if pack=='english_russian' else 'qSoundUrl'
    assert a.get(other)==b.get(other),f'Other audio changed on {a["cardId"]}'
   else:
    assert actual==before,f'Unrelated card text changed on {a["cardId"]}'
    assert all(a.get(k)==b.get(k) for k in ['qSoundUrl','aSoundUrl']),f'Unrelated audio changed on {a["cardId"]}'
 def fetch(pair):
  pack,pid,did=pair;live=client.list_cards(pid,did,per_page=500);assert_deck(pair,live)
  return pair,live
 print('Checking all 40 live decks for conflicts...',flush=True)
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:live_decks=dict(pool.map(fetch,pairs))
 print('20,000 live cards match the expected baseline or resumable desired state.',flush=True)
 if not apply:print('Preflight only; no writes.',flush=True);return
 live_byid={c['cardId']:c for live in live_decks.values() for c in live}
 stop=threading.Event();lock=threading.Lock();count=0
 def upload(x):
  nonlocal count
  if stop.is_set():raise RuntimeError('Stopped after another failure')
  cid=x['cardId'];i=audio[cid];receipt=B/'receipts'/f'{cid}.json';desired=card_write_payload(x['after_card'])
  if card_write_payload(live_byid[cid])!=desired:
   client.update_card(x['packId'],x['deckId'],cid,**desired)
  old_receipt=json.loads(receipt.read_text()) if receipt.exists() else None
  if not old_receipt or old_receipt['sha256']!=hashes[cid]:
   side='question_file' if x['pack']=='english_russian' else 'answer_file'
   job=client.attach_audio(x['packId'],x['deckId'],cid,**{side:audio_path(i)})
   atomic(receipt,{'cardId':cid,'packId':x['packId'],'deckId':x['deckId'],'sha256':hashes[cid],'content_hash':i['content_hash'],'job':job,'uploadedAt':time.time()})
  with lock:
   count+=1
   if count%25==0:print(f'Text and English audio submitted: {count}/744',flush=True)
 def failed(f):
  if f.exception():stop.set()
 with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
  jobs=[pool.submit(upload,x) for x in changes]
  for f in jobs:f.add_done_callback(failed)
  for f in concurrent.futures.as_completed(jobs):f.result()
 print('All 744 updates submitted. Verifying live text and downloading replacement recordings...',flush=True)
 def audio_matches(args):
  card,pack=args;cid=card['cardId'];url=card.get('qSoundUrl' if pack=='english_russian' else 'aSoundUrl')
  if not url:return False
  for attempt in range(3):
   try:
    with urlopen(url,timeout=45) as response:raw=response.read()
    return hashlib.sha256(raw).hexdigest()==hashes[cid]
   except Exception:
    if attempt==2:return False
    time.sleep(2*(attempt+1))
 def verify(pair):
  pack,pid,did=pair;expected=sum(x['deckId']==did for x in changes)
  for attempt in range(8):
   live=client.list_cards(pid,did,per_page=500);assert_deck(pair,live,final=True)
   selected=[(c,pack) for c in live if c['cardId'] in byid]
   with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:ok=list(pool.map(audio_matches,selected))
   if all(ok):break
   print(f'Deck {did}: {sum(ok)}/{expected} recordings ready; waiting for attachment processing.',flush=True);time.sleep(10)
  else:raise RuntimeError(f'Audio verification incomplete for deck {did}')
  out=B/'after'/pack;out.mkdir(exist_ok=True);atomic(out/f'{did}.json',live)
  report={'pack':pack,'packId':pid,'deckId':did,'cards':500,'changed_cards':expected,'audio_bytes_matched':sum(ok),'ids_order_preserved':True,'all_text_matches':True,'other_audio_preserved':True,'verifiedAt':time.time()}
  atomic(B/'verified'/f'{did}.json',report);print(f'Verified {pack}/{did}: 500 cards, {expected} replacement recordings',flush=True)
  return report
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:reports=list(pool.map(verify,pairs))
 assert len(reports)==40 and sum(x['audio_bytes_matched'] for x in reports)==744
 # Keep local exports in sync, refusing to overwrite any concurrent local edits.
 for pack,_,did in pairs:
  name=f'deck_{did}.csv';dest=R/pack/name;src=B/'staged'/pack/name;old=B/'originals'/pack/name
  assert dest.read_bytes() in [old.read_bytes(),src.read_bytes()],f'Local file changed concurrently: {dest}'
 for pack,_,did in pairs:
  name=f'deck_{did}.csv';dest=R/pack/name;src=B/'staged'/pack/name
  shutil.copyfile(src,dest)
  live=json.loads((B/'after'/pack/f'{did}.json').read_text());local=cards_from_path(dest)
  assert [card_write_payload(c) for c in local]==[card_write_payload(c) for c in live]
 atomic(B/'result.json',{'status':'complete','verifiedAt':time.time(),'cards_checked':20000,'decks':40,'changed_cards':744,'changed_by_pack':{p:sum(x['pack']==p for x in changes) for p in ['english_russian','russian_english']},'recordings_attached_and_bytes_verified':744,'distinct_recordings':737,'vocabulary_flags':0,'local_exports_match_cloud':True,'manifest_sha256':hashlib.sha256((B/'audio_manifest.json').read_bytes()).hexdigest(),'deck_reports':reports})
 print('COMPLETE: 744 cards and recordings updated and verified; all 20,000 cards checked; local CSVs match cloud.',flush=True)
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--apply',action='store_true');args=parser.parse_args();main(args.apply)
