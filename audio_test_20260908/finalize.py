import base64,hashlib,json,time
from pathlib import Path
from urllib.request import urlopen
from brainscape import BrainscapeClient
root=Path(__file__).resolve().parent;s=json.loads((root/'state.json').read_text());c=BrainscapeClient.discover(retries=1);p=24125111;d=22994657
assert s['pack']['packId']==p and s['deck']['deckId']==d
for row,kwargs in zip(s['cards'][:3],[{'question_file':root/'question.mp3'},{'answer_file':root/'answer.mp3'},{'question_file':root/'question.mp3','answer_file':root/'answer.mp3'}]):
 row['finalUpload']=c.attach_audio(p,d,row['cardId'],**kwargs)
# Repeat raw PATCH with the nonempty speech sample.
c.patch(f'packs/{p}/decks/{d}/cards/{s["cards"][4]["cardId"]}',{'qSoundUrl':'data:audio/mpeg;base64,'+base64.b64encode((root/'question.mp3').read_bytes()).decode()})
(root/'state.json').write_text(json.dumps(s,indent=2))
for attempt in range(15):
 cards=c.list_cards(p,d);checks=[]
 for card in cards[:3]:
  for field,filename in [('qSoundUrl','question.mp3'),('aSoundUrl','answer.mp3')]:
   if card.get(field):
    with urlopen(card[field]) as r:raw=r.read();mime=r.headers.get('Content-Type')
    checks.append({'cardId':card['cardId'],'field':field,'bytes':len(raw),'mime':mime,'matches_generated':raw==(root/filename).read_bytes()})
 if len(checks)==4 and all(x['matches_generated'] for x in checks):break
 time.sleep(2)
(root/'readback.json').write_text(json.dumps(cards,indent=2));(root/'verified_audio.json').write_text(json.dumps(checks,indent=2))
print(json.dumps(checks,indent=2))
for card in cards: print(card['cardId'],card.get('qSoundUrl'),card.get('aSoundUrl'),card.get('question'))
# Link control now points at the final generated clip.
c.update_card(p,d,s['cards'][6]['cardId'],question='07 Markdown audio link\n\n[Play sample audio]('+cards[0]['qSoundUrl']+')',answer='Ordinary hyperlink, not a native flashcard audio attachment.')
print('retained deck',c.get_deck(p,d))
