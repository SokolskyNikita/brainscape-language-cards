import json,subprocess
from pathlib import Path
from urllib.request import Request,urlopen
from urllib.error import HTTPError
ROOT=Path(__file__).resolve().parent
from brainscape.config import require_secret
key=require_secret("CARTESIA_API_KEY")
cards=json.loads((ROOT/'source.json').read_text())
indices=[0,2,4,7,8,16,17,18,19,35,48,55,62,64,65,75,80,83,89,94]
items=[]
for number,index in enumerate(indices,1):
 card=cards[index]
 word=card['aMdBody'].strip();sentence=card['aMdFootnote'].strip()
 transcript=word+'. <break time="500ms"/>'+sentence
 item={'number':number,'sourceCardId':card['cardId'],'question':card['question'],'answer':card['answer'],'word':word,'sentence':sentence,'transcript':transcript,'file':f'{number:02}.mp3'}
 items.append(item)
(ROOT/'manifest.json').write_text(json.dumps({'model':'sonic-3.6','voice':'Daniel','voiceId':'47c38ca4-5f35-497b-b1a3-415245fb35e1','locale':'en-US','pauseMs':500,'generation_config':{'emotion':'neutral','speed':0.9},'items':items},indent=2,ensure_ascii=False))
for item in items:
 wav=ROOT/f'{item["number"]:02}.wav';mp3=ROOT/item['file']
 if not wav.exists():
  body={'model_id':'sonic-3.6','transcript':item['transcript'],'voice':'47c38ca4-5f35-497b-b1a3-415245fb35e1','locale':'en-US','generation_config':{'emotion':'neutral','speed':0.9},'output_format':{'container':'wav','encoding':'pcm_s16le','sample_rate':44100}}
  req=Request('https://api.cartesia.ai/tts/bytes',data=json.dumps(body).encode(),headers={'Authorization':'Bearer '+key,'Cartesia-Version':'2026-08-14','Content-Type':'application/json'},method='POST')
  try:
   with urlopen(req,timeout=60) as r:raw=r.read()
  except HTTPError as e:raise SystemExit(f'Cartesia HTTP {e.code}: '+e.read().decode()[:300])
  assert raw[:4]==b'RIFF' and len(raw)>5000,'Invalid or empty WAV'
  wav.write_bytes(raw)
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(wav),'-codec:a','libmp3lame','-b:a','128k',str(mp3)],check=True)
 info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration,size','-of','json',str(mp3)]))['format']
 assert float(info['duration'])>0.5
 print(f'{item["number"]:02} {item["word"]}: {float(info["duration"]):.2f}s',flush=True)
print('Generated 20 clips. Speech characters:',sum(len(i['word'])+len(i['sentence']) for i in items),flush=True)
