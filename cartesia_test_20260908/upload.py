import json,time,hashlib
from pathlib import Path
from urllib.request import urlopen
from brainscape import BrainscapeClient
ROOT=Path(__file__).resolve().parent
manifest=json.loads((ROOT/'manifest.json').read_text())
assert len(manifest['items'])==20
assert all((ROOT/i['file']).stat().st_size>1000 for i in manifest['items'])
c=BrainscapeClient.discover(retries=1)
statefile=ROOT/'state.json'
s=json.loads(statefile.read_text()) if statefile.exists() else {'cards':[]}
def save():statefile.write_text(json.dumps(s,indent=2,ensure_ascii=False))
if 'pack' not in s:
 s['pack']=c.create_pack('Russian to English — Cartesia TEST 2026-09-08',desc='20-card audio sample. English answer only: word, half-second pause, full example sentence. Skylar, General American. KEEP for manual validation.',private=True);save()
p=s['pack']['packId']
assert c.get_pack(p)['name']=='Russian to English — Cartesia TEST 2026-09-08'
if 'deck' not in s:
 s['deck']=c.create_deck(p,'20 English answers — Skylar — KEEP',desc='Cartesia Sonic 3.6, en-US. Word + 500 ms pause + example. Separate copies; original vocabulary decks unchanged.');save()
d=s['deck']['deckId']
assert c.get_deck(p,d)['name']=='20 English answers — Skylar — KEEP'
for item in manifest['items']:
 row=next((x for x in s['cards'] if x['number']==item['number']),None)
 if row is None:
  card=c.create_card(p,d,question=item['question'],answer=item['answer'])
  row={'number':item['number'],'cardId':card['cardId'],'word':item['word']};s['cards'].append(row);save()
 if 'job' not in row:
  row['job']=c.attach_audio(p,d,row['cardId'],answer_file=ROOT/item['file']);save()
 print(f'Uploaded {item["number"]}/20: {item["word"]}',flush=True)
for attempt in range(20):
 cards=c.list_cards(p,d)
 if len(cards)==20 and all(x.get('aSoundUrl') and not x.get('qSoundUrl') for x in cards):break
 time.sleep(3)
else:raise SystemExit('Audio jobs not all finished; keep state and check later.')
checks=[]
byid={x['cardId']:x for x in cards}
for item,row in zip(manifest['items'],s['cards']):
 card=byid[row['cardId']]
 assert card['question']==item['question'] and card['answer']==item['answer'],'Text changed'
 with urlopen(card['aSoundUrl'],timeout=30) as r:raw=r.read()
 assert raw==(ROOT/item['file']).read_bytes(),'Stored audio differs'
 checks.append({'cardId':card['cardId'],'number':item['number'],'answerAudioVerified':True,'sha256':hashlib.sha256(raw).hexdigest()})
s['verified']=checks;s['private']=c.get_pack(p).get('private');save()
(ROOT/'readback.json').write_text(json.dumps(cards,indent=2,ensure_ascii=False))
print('VERIFIED: 20 answer-only attachments; exact source text preserved.',flush=True)
print('Dashboard: https://www.brainscape.com'+s['pack']['paths']['dashboardPath'],flush=True)
print('Deck ID:',d,'Private:',s['private'],flush=True)
