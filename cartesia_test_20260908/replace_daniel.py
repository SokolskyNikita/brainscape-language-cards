import json,time,hashlib
from pathlib import Path
from urllib.request import urlopen
from brainscape import BrainscapeClient
R=Path(__file__).resolve().parent
m=json.loads((R/'manifest.json').read_text());s=json.loads((R/'state.json').read_text());c=BrainscapeClient.discover(retries=1)
p=24125405;d=22995414
assert s['pack']['packId']==p and s['deck']['deckId']==d
assert m['generation_config']=={'emotion':'neutral','speed':0.9}
assert m['voice']=='Daniel' and len(m['items'])==len(s['cards'])==20
assert all((R/i['file']).stat().st_size>1000 for i in m['items'])
rows={x['number']:x for x in s['cards']}
# Capture the existing card text/IDs before any mutation.
original=c.list_cards(p,d);assert {x['cardId'] for x in original}=={x['cardId'] for x in s['cards']}
for item in m['items']:
 row=rows[item['number']]
 if 'danielNeutralJob' not in row:
  row['danielNeutralJob']=c.attach_audio(p,d,row['cardId'],answer_file=R/item['file'])
  (R/'state.json').write_text(json.dumps(s,indent=2,ensure_ascii=False))
 print('Daniel uploaded',item['number'],'/20',flush=True)
for attempt in range(25):
 cards=c.list_cards(p,d);byid={x['cardId']:x for x in cards};checks=[]
 for item in m['items']:
  card=byid[rows[item['number']]['cardId']]
  assert card['question']==item['question'] and card['answer']==item['answer'] and not card.get('qSoundUrl')
  with urlopen(card['aSoundUrl'],timeout=30) as r:raw=r.read()
  checks.append(raw==(R/item['file']).read_bytes())
 if all(checks):break
 time.sleep(3)
else:raise SystemExit('Replacement still processing; rerun verification.')
c.update_deck(p,d,name='20 English answers — Daniel neutral — KEEP')
c.update_pack(p,desc='20-card audio sample. English answer only: word, half-second pause, full example sentence. Daniel, General American, neutral emotion, speed 0.9; no pronunciation overrides. KEEP for manual validation.')
s['deck']=c.get_deck(p,d);s['voice']='Daniel';s['danielNeutralVerified']=20
(R/'state.json').write_text(json.dumps(s,indent=2,ensure_ascii=False));(R/'readback.json').write_text(json.dumps(cards,indent=2,ensure_ascii=False))
print('VERIFIED: all 20 Daniel clips byte-match; text and IDs unchanged; answer audio only.',flush=True)
