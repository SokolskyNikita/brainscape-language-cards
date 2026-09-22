"""Generate content-addressed replacement English audio; no Brainscape writes."""
from pathlib import Path
import concurrent.futures,hashlib,json,os,re,subprocess,threading,time
from urllib.request import Request,urlopen
from urllib.error import HTTPError,URLError
B=Path(__file__).resolve().parent;R=B.parent
SETTINGS={'model_id':'sonic-3.6','voice':'47c38ca4-5f35-497b-b1a3-415245fb35e1','locale':'en-US','generation_config':{'emotion':'neutral','speed':0.9},'output_format':{'container':'wav','encoding':'pcm_s16le','sample_rate':44100}}
def digest(body):return hashlib.sha256(json.dumps(body,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def atomic(p,data):
 t=p.with_suffix('.tmp');t.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n');t.replace(p)
def load_manifest():
 """Resolve historical absolute paths without rewriting the hashed evidence."""
 m=json.loads((B/'audio_manifest.json').read_text())
 for i in m['items']:
  expected=Path('audio')/f'{i["content_hash"]}.mp3'
  old=Path(i['file'])
  assert old.parts[-2:]==expected.parts, 'Unexpected audio manifest path'
  i['file']=str(expected)
 return m
def audio_path(item):return B/item['file']
def manifest():
 items=[]
 for x in json.loads((B/'changes.json').read_text()):
  head=re.sub(r'\([^()]*[А-Яа-яЁё][^()]*\)','',x['english_target']).strip()
  transcript=head+'. <break time="500ms"/>'+x['after_english_example']
  assert not re.search(r'[А-Яа-яЁё]',transcript)
  body=dict(SETTINGS,transcript=transcript);h=digest(body)
  items.append({k:x[k] for k in ['pack','packId','deckId','cardId','overall','audio_side']}|{'transcript':transcript,'content_hash':h,'file':str(Path('audio')/f'{h}.mp3')})
 return {'settings':SETTINGS,'changes_sha256':hashlib.sha256((B/'changes.json').read_bytes()).hexdigest(),'items':items}
def main():
 m=manifest();path=B/'audio_manifest.json'
 if path.exists():assert load_manifest()==m,'Replacement plan changed after manifest creation'
 else:atomic(path,m)
 (B/'audio').mkdir(exist_ok=True)
 from brainscape.config import require_secret
 key=require_secret("CARTESIA_API_KEY")
 unique={i['content_hash']:i for i in m['items']};lock=threading.Lock();stop=threading.Event();count=0
 def synth(i):
  nonlocal count
  if stop.is_set():raise RuntimeError('Generation stopped after failure')
  dest=audio_path(i);meta=dest.with_suffix('.json')
  if dest.exists() and meta.exists():
   result=json.loads(meta.read_text());assert hashlib.sha256(dest.read_bytes()).hexdigest()==result['sha256']
   return result
  body=dict(SETTINGS,transcript=i['transcript'])
  for attempt in range(4):
   try:
    req=Request('https://api.cartesia.ai/tts/bytes',data=json.dumps(body).encode(),headers={'Authorization':'Bearer '+key,'Cartesia-Version':'2026-08-14','Content-Type':'application/json'},method='POST')
    with urlopen(req,timeout=90) as response:raw=response.read()
    break
   except HTTPError as e:
    if e.code not in (429,500,502,503,504) or attempt==3:raise RuntimeError(f'Cartesia HTTP {e.code}') from None
    time.sleep(3*(attempt+1))
   except (URLError,TimeoutError,OSError):
    if attempt==3:raise
    time.sleep(3*(attempt+1))
  assert raw[:4]==b'RIFF' and len(raw)>5000
  tmp=dest.with_suffix('.tmp.mp3')
  subprocess.run(['ffmpeg','-v','error','-y','-i','pipe:0','-ac','1','-codec:a','libmp3lame','-b:a','128k',str(tmp)],input=raw,capture_output=True,check=True)
  probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(tmp)]))
  duration=float(probe['format']['duration']);assert 1<duration<35,(i['cardId'],duration)
  assert probe['streams'][0]['codec_name']=='mp3' and probe['streams'][0]['channels']==1
  assert 1000<tmp.stat().st_size<5*1024*1024
  tmp.replace(dest)
  result={'content_hash':i['content_hash'],'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'bytes':dest.stat().st_size,'duration':duration,'transcript':i['transcript']}
  atomic(meta,result)
  with lock:
   count+=1
   if count%25==0:print(f'Generated {count}/{len(unique)} distinct recordings',flush=True)
  return result
 def failed(f):
  if f.exception():stop.set()
 print(f'{len(m["items"])} cards; {len(unique)} distinct recordings; {sum(len(i["transcript"]) for i in unique.values())} input characters',flush=True)
 with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
  jobs=[pool.submit(synth,i) for i in unique.values()]
  for f in jobs:f.add_done_callback(failed)
  result=[f.result() for f in concurrent.futures.as_completed(jobs)]
 atomic(B/'audio_result.json',{'status':'complete','cards':len(m['items']),'distinct_recordings':len(result),'total_seconds':sum(x['duration'] for x in result),'manifest_sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
 print('Audio generation complete; all files decoded and validated.',flush=True)
if __name__=='__main__':main()
