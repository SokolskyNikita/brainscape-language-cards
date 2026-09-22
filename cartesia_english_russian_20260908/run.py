"""Resumable question-only audio rollout. No card text writes or deletions."""
import concurrent.futures,hashlib,json,os,queue,subprocess,threading,time
from pathlib import Path
from urllib.request import Request,urlopen
from urllib.error import HTTPError,URLError
from brainscape import BrainscapeClient
R=Path(__file__).resolve().parent
M=json.loads((R/'manifest.json').read_text());P=M['packId']
assert P==21917816 and len(M['items'])==10000
assert sum(len(i['transcript']) for i in M['items'])<1000000
assert M['generation_config']=={'emotion':'neutral','speed':0.9}
from brainscape.config import require_secret
KEY=require_secret("CARTESIA_API_KEY")
C=BrainscapeClient.discover(retries=3,timeout=60)
for name in ['audio','receipts','verified']:(R/name).mkdir(exist_ok=True)
LOCK=threading.Lock();STOP=threading.Event();START=time.time()
COUNT={'generated':0,'uploaded':0,'verified':0,'errors':0}
def atomic(path,value):
 tmp=path.with_suffix('.tmp');tmp.write_text(json.dumps(value,ensure_ascii=False));tmp.replace(path)
def event(kind,**kw):
 with LOCK:
  with (R/'events.jsonl').open('a') as f:f.write(json.dumps({'time':time.time(),'kind':kind,**kw})+'\n')
def progress(kind):
 with LOCK:
  COUNT[kind]+=1
  if sum(COUNT.values())%50==0:
   atomic(R/'progress.json',{'counts':COUNT.copy(),'elapsedSeconds':round(time.time()-START)})
   print(json.dumps(COUNT),flush=True)
def stop_on_failure(f):
 if f.exception() is not None:STOP.set()
def audiofile(i):return R/'audio'/f'{i["cardId"]}.mp3'
def receipt(i):return R/'receipts'/f'{i["cardId"]}.json'
def synth(i):
 if STOP.is_set():raise RuntimeError('Stopped after another failure')
 dest=audiofile(i)
 if dest.exists():return i
 body={k:M[k] for k in ['model','voice','locale','generation_config']}
 body['model_id']=body.pop('model');body.update(transcript=i['transcript'],output_format={'container':'wav','encoding':'pcm_s16le','sample_rate':44100})
 for attempt in range(4):
  try:
   req=Request('https://api.cartesia.ai/tts/bytes',data=json.dumps(body).encode(),headers={'Authorization':'Bearer '+KEY,'Cartesia-Version':'2026-08-14','Content-Type':'application/json'},method='POST')
   with urlopen(req,timeout=90) as response:raw=response.read()
   break
  except HTTPError as e:
   if e.code not in (429,500,502,503,504) or attempt==3:raise RuntimeError(f'Cartesia HTTP {e.code}: {e.read().decode()[:200]}') from None
   event('tts_retry',cardId=i['cardId'],status=e.code);time.sleep(3*(attempt+1))
  except (URLError,TimeoutError,OSError):
   if attempt==3:raise
   event('tts_network_retry',cardId=i['cardId']);time.sleep(3*(attempt+1))
 assert raw[:4]==b'RIFF' and len(raw)>5000
 mp3=subprocess.run(['ffmpeg','-v','error','-i','pipe:0','-codec:a','libmp3lame','-b:a','128k','-f','mp3','pipe:1'],input=raw,capture_output=True,check=True).stdout
 assert 1000<len(mp3)<5242880
 tmp=dest.with_suffix('.tmp');tmp.write_bytes(mp3);tmp.replace(dest)
 event('generated',cardId=i['cardId'],characters=len(i['transcript']),bytes=len(mp3));progress('generated')
 return i
def upload(i):
 if STOP.is_set():raise RuntimeError('Stopped after another failure')
 path=receipt(i)
 if path.exists():return
 for attempt in range(4):
  try:
   result=C.attach_audio(P,i['deckId'],i['cardId'],question_file=audiofile(i));break
  except Exception as e:
   status=getattr(e,'status',None)
   if status in (400,401,403,404,422) or attempt==3:raise
   event('upload_retry',cardId=i['cardId'],error=str(e)[:150]);time.sleep(3*(attempt+1))
 atomic(path,{'cardId':i['cardId'],'deckId':i['deckId'],'job':result,'sha256':hashlib.sha256(audiofile(i).read_bytes()).hexdigest()})
 progress('uploaded')
def check(i,card):
 if card['question']!=i['question'] or card['answer']!=i['answer'] or card.get('aSoundUrl')!=i['aSoundUrl']:
  raise RuntimeError(f'Text or answer audio mismatch on {i["cardId"]}')
 url=card.get('qSoundUrl')
 if not url:return False
 for attempt in range(3):
  try:
   with urlopen(url,timeout=40) as response:raw=response.read()
   break
  except (HTTPError,URLError,TimeoutError,OSError):
   if attempt==2:return False
   time.sleep(2)
 return hashlib.sha256(raw).digest()==hashlib.sha256(audiofile(i).read_bytes()).digest()
# Reuse recordings only when transcript and every voice setting match exactly.
T=R.parent/'cartesia_russian_english_20260908';source=json.loads((T/'manifest.json').read_text())
assert all(source[k]==M[k] for k in ['model','voice','locale','generation_config'])
by_transcript={x['transcript']:x for x in source['items']}
reused=[]
for i in M['items']:
 s=by_transcript.get(i['transcript'])
 if s:
  src=T/'audio'/f'{s["cardId"]}.mp3'
  if not audiofile(i).exists():audiofile(i).write_bytes(src.read_bytes())
  reused.append({'cardId':i['cardId'],'sourceCardId':s['cardId']})
atomic(R/'reuse.json',reused)
print('Reused',len(reused),'matching recordings; new recordings needed:',len(M['items'])-len(reused),flush=True)
def live_cards(did):
 for attempt in range(4):
  try:return C.list_cards(P,did)
  except Exception as e:
   if getattr(e,'status',None) in (400,401,403,404,422) or attempt==3:raise
   event('read_retry',deckId=did,error=str(e)[:150]);time.sleep(3*(attempt+1))
def verify_deck(deck,items):
 did=deck["deckId"];done=R/"verified"/f"{did}.json"
 print("VERIFYING DECK",did,flush=True)
 for attempt in range(8):
  live=live_cards(did);byid={c['cardId']:c for c in live}
  assert set(byid)=={i['cardId'] for i in items}
  with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:ok=list(pool.map(lambda i:check(i,byid[i['cardId']]),items))
  if all(ok):break
  print('Waiting for attachments:',sum(ok),'/500',flush=True);time.sleep(10)
 else:raise RuntimeError(f'Verification incomplete for {did}: {sum(ok)}/500')
 atomic(done,{'deckId':did,'name':deck['name'],'cards':500,'verifiedAt':time.time(),'textPreserved':True,'answerAudioPreserved':True,'questionBytesMatched':500})
 for i in items:progress('verified')
 print('VERIFIED DECK',did,'500/500',flush=True);event('deck_verified',deckId=did,cards=500)

with concurrent.futures.ThreadPoolExecutor(max_workers=1) as verifier:
 verification_jobs=[]
 # Generate/upload decks serially while one verifier checks the preceding deck.
 for deck in M['decks']:
  did=deck['deckId'];items=[i for i in M['items'] if i['deckId']==did]
  done=R/'verified'/f'{did}.json'
  if done.exists():print('Already verified deck',did,flush=True);continue
  live=live_cards(did);live_byid={c['cardId']:c for c in live}
  assert len(live)==len(items)==500 and set(live_byid)=={i['cardId'] for i in items}
  assert all(live_byid[i['cardId']]['question']==i['question'] and live_byid[i['cardId']]['answer']==i['answer'] for i in items)
  print('START DECK',deck['name'],did,flush=True);event('deck_start',deckId=did)
  try:
   with concurrent.futures.ThreadPoolExecutor(max_workers=5) as gen,concurrent.futures.ThreadPoolExecutor(max_workers=24) as up:
    futures=[gen.submit(synth,i) for i in items];uploads=[]
    for f in futures:f.add_done_callback(stop_on_failure)
    for f in concurrent.futures.as_completed(futures):
     uf=up.submit(upload,f.result());uf.add_done_callback(stop_on_failure);uploads.append(uf)
    for f in concurrent.futures.as_completed(uploads):f.result()
  except Exception as e:
   STOP.set();event('error',deckId=did,error=str(e)[:300]);raise
  verification_jobs.append(verifier.submit(verify_deck,deck,items))
  verification_jobs[-1].add_done_callback(stop_on_failure)
 for job in verification_jobs:job.result()
reports=[json.loads(p.read_text()) for p in (R/'verified').glob('*.json')]
assert len(reports)==20 and sum(x['cards'] for x in reports)==10000
atomic(R/'result.json',{'status':'complete','packId':P,'cards':10000,'decks':reports,'settings':{k:M[k] for k in ['model','voice','locale','generation_config']}})
print('COMPLETE: 10,000 question audio files verified; 20 decks; all text and answer audio preserved.',flush=True)
