"""Resumable Spanish-only audio generation, attachment and full verification."""
import concurrent.futures,fcntl,hashlib,json,subprocess,sys,threading,time
from pathlib import Path
from urllib.request import Request,urlopen
from urllib.error import HTTPError,URLError
from brainscape import BrainscapeClient,card_write_payload
R=Path(__file__).resolve().parent
PID=int(sys.argv[1]);M=json.loads((R/f'manifest_{PID}.json').read_text())
assert len(M['items'])==8000 and PID in [21945419,21303832]
lockfile=(R/'run.lock').open('w');fcntl.flock(lockfile,fcntl.LOCK_EX|fcntl.LOCK_NB)
from brainscape.config import require_secret
KEY=require_secret("CARTESIA_API_KEY")
C=BrainscapeClient.discover(retries=3,timeout=60)
for n in ['audio','receipts','verified']:(R/n).mkdir(exist_ok=True)
LOCK=threading.Lock();STOP=threading.Event();START=time.time();COUNT={'generated':0,'cached':0,'uploaded':0,'verified':0}
UPLOAD_LOCK=threading.Lock();NEXT_UPLOAD=0.0
MANIFEST_HASH=hashlib.sha256((R/f'manifest_{PID}.json').read_bytes()).hexdigest()
def pace_upload(delay=0):
    global NEXT_UPLOAD
    with UPLOAD_LOCK:
        now=time.monotonic()
        if delay:NEXT_UPLOAD=max(NEXT_UPLOAD,now+delay);return
        wait=max(0,NEXT_UPLOAD-now)
        NEXT_UPLOAD=max(NEXT_UPLOAD,now)+.3
    if wait:time.sleep(wait)
    if STOP.is_set():raise RuntimeError('Stopped after a failure')
def atomic(p,x):
    tmp=p.with_suffix('.tmp');tmp.write_text(json.dumps(x,ensure_ascii=False));tmp.replace(p)
def event(kind,**kw):
    with LOCK:
        with (R/'events.jsonl').open('a') as f:f.write(json.dumps({'time':time.time(),'packId':PID,'kind':kind,**kw})+'\n')
def count(k):
    with LOCK:
        COUNT[k]+=1
        if sum(COUNT.values())%100==0:
            atomic(R/f'progress_{PID}.json',{'counts':COUNT,'elapsedSeconds':round(time.time()-START)})
            print(json.dumps(COUNT),flush=True)
def audiofile(i):return R/'audio'/f'{i["key"]}.mp3'
def receipt(i):return R/'receipts'/f'{i["cardId"]}.json'
def synth(i):
    if STOP.is_set():raise RuntimeError('Stopped after a failure')
    dest=audiofile(i)
    if dest.exists():count('cached');return i
    body={**M['settings'],'transcript':i['transcript'],'output_format':{'container':'wav','encoding':'pcm_s16le','sample_rate':44100}}
    for a in range(4):
        try:
            req=Request('https://api.cartesia.ai/tts/bytes',data=json.dumps(body).encode(),headers={'Authorization':'Bearer '+KEY,'Cartesia-Version':'2026-08-14','Content-Type':'application/json'})
            with urlopen(req,timeout=90) as r:raw=r.read()
            break
        except HTTPError as e:
            if e.code not in [429,500,502,503,504] or a==3:raise RuntimeError(f'Cartesia HTTP {e.code}: '+e.read().decode()[:250].replace(KEY,'[REDACTED]')) from None
            event('tts_retry',cardId=i['cardId'],status=e.code);time.sleep(3*(a+1))
        except (URLError,TimeoutError,OSError):
            if a==3:raise
            time.sleep(3*(a+1))
    assert raw[:4]==b'RIFF' and len(raw)>5000
    mp3=subprocess.run(['ffmpeg','-v','error','-i','pipe:0','-codec:a','libmp3lame','-b:a','128k','-f','mp3','pipe:1'],input=raw,capture_output=True,check=True).stdout
    assert 1000<len(mp3)<5242880
    tmp=dest.with_suffix('.tmp');tmp.write_bytes(mp3);tmp.replace(dest)
    event('generated',cardId=i['cardId'],characters=len(i['transcript']),bytes=len(mp3));count('generated');return i
def upload(i):
    if STOP.is_set():raise RuntimeError('Stopped after a failure')
    dest=receipt(i)
    if dest.exists() and json.loads(dest.read_text())['key']==i['key']:return
    args={('question_file' if i['side']=='q' else 'answer_file'):audiofile(i)}
    for a in range(8):
        try:
            pace_upload()
            r=C.attach_audio(PID,i['deckId'],i['cardId'],**args);break
        except Exception as e:
            if getattr(e,'status',None) in [400,401,403,404,422] or a==7:raise
            delay=min(60,5*2**a)
            if getattr(e,'status',None)==429:pace_upload(delay)
            event('upload_retry',cardId=i['cardId'],status=getattr(e,'status',None),delay=delay)
            time.sleep(delay)
    atomic(dest,{'cardId':i['cardId'],'key':i['key'],'side':i['side'],'job':r});count('uploaded')
def check(i,c):
    other='a' if i['side']=='q' else 'q'
    assert card_write_payload(c)==i['text'],f'Text changed on {i["cardId"]}'
    assert c.get(other+'SoundUrl')==i['otherSoundUrl'],f'Other-side audio changed on {i["cardId"]}'
    url=c.get(i['side']+'SoundUrl')
    if not url:return False
    for a in range(3):
        try:
            with urlopen(url,timeout=40) as r:raw=r.read()
            return hashlib.sha256(raw).digest()==hashlib.sha256(audiofile(i).read_bytes()).digest()
        except (HTTPError,URLError,TimeoutError,OSError):
            if a==2:return False
            time.sleep(2)
def verify(d,items):
    print('VERIFY',d['deckId'],flush=True)
    for a in range(8):
        cards=C.list_cards(PID,d['deckId']);byid={c['cardId']:c for c in cards}
        assert [c['cardId'] for c in cards]==[i['cardId'] for i in items]
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:ok=list(pool.map(lambda i:check(i,byid[i['cardId']]),items))
        if all(ok):break
        print('Attachments ready',sum(ok),'/500',flush=True);time.sleep(10)
    else:raise RuntimeError(f'Audio verification incomplete for {d["deckId"]}')
    atomic(R/'verified'/f'{d["deckId"]}.json',{'packId':PID,'deckId':d['deckId'],'cards':len(items),'spanishSide':M['spanishSide'],'manifestHash':MANIFEST_HASH,'audioBytesMatched':len(items),'textPreserved':True,'otherAudioPreserved':True,'verifiedAt':time.time()})
    for _ in items:count('verified')
    print('VERIFIED',d['deckId'],flush=True)
def stop_failure(f):
    if f.exception():STOP.set()
with concurrent.futures.ThreadPoolExecutor(max_workers=1) as verifier:
    jobs=[]
    for d in M['decks']:
        items=[i for i in M['items'] if i['deckId']==d['deckId']]
        verified=R/'verified'/f'{d["deckId"]}.json'
        if verified.exists():
            assert json.loads(verified.read_text()).get('manifestHash')==MANIFEST_HASH,'Manifest changed after verification; review before resuming.'
            continue
        live=C.list_cards(PID,d['deckId']);assert len(live)==500
        assert [c['cardId'] for c in live]==[i['cardId'] for i in items]
        assert all(card_write_payload(c)==i['text'] for c,i in zip(live,items))
        print('START',PID,d['deckId'],d['name'],flush=True)
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as gen,concurrent.futures.ThreadPoolExecutor(max_workers=6) as up:
            # Unique transcript keys prevent duplicate cache writes within a deck.
            groups={}
            for i in items:groups.setdefault(i['key'],[]).append(i)
            fs=[gen.submit(synth,g[0]) for g in groups.values()];us=[]
            for f in fs:f.add_done_callback(stop_failure)
            for f in concurrent.futures.as_completed(fs):
                i=f.result()
                for target in groups[i['key']]:
                    u=up.submit(upload,target);u.add_done_callback(stop_failure);us.append(u)
            for u in concurrent.futures.as_completed(us):u.result()
        f=verifier.submit(verify,d,items);f.add_done_callback(stop_failure);jobs.append(f)
    for f in jobs:f.result()
reports=[json.loads((R/'verified'/f'{d["deckId"]}.json').read_text()) for d in M['decks']]
assert sum(r['cards'] for r in reports)==8000
atomic(R/f'result_{PID}.json',{'status':'complete','packId':PID,'cards':8000,'settings':M['settings'],'decks':reports})
print('COMPLETE',PID,'8000 Spanish recordings verified',flush=True)
