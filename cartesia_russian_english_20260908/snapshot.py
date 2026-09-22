import json,concurrent.futures
from pathlib import Path
from brainscape import BrainscapeClient
R=Path(__file__).resolve().parent;c=BrainscapeClient.discover(retries=1);P=21919521
pack=c.get_pack(P);decks=c.list_decks(P)
ids={int(p.stem.split('_')[1]) for p in (R.parent/'russian_english').glob('deck_*.csv')}
selected=[d for d in decks if d['deckId'] in ids]
assert len(selected)==20
print('Class:',pack['name'],'selected decks:',len(selected),'other decks:',[(d['deckId'],d['name']) for d in decks if d['deckId'] not in ids],flush=True)
def get(d):
 p=R/f'before_{d["deckId"]}.json'
 if p.exists():cards=json.loads(p.read_text())
 else:
  cards=c.list_cards(P,d['deckId']);p.write_text(json.dumps(cards,ensure_ascii=False,indent=2))
 assert len(cards)==500
 return d,cards
items=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 for d,cards in pool.map(get,selected):
  for card in cards:
   word=card.get('aMdBody','').strip();sentence=card.get('aMdFootnote','').strip()
   assert word and sentence,(d['deckId'],card['cardId'])
   items.append({'deckId':d['deckId'],'cardId':card['cardId'],'word':word,'sentence':sentence,'question':card['question'],'answer':card['answer'],'qSoundUrl':card.get('qSoundUrl'),'aSoundUrl':card.get('aSoundUrl'),'transcript':word+'. <break time="500ms"/>'+sentence})
  print('Snapshot',d['name'],len(cards),flush=True)
assert len(items)==10000 and len({i['cardId'] for i in items})==10000
m={'packId':P,'packName':pack['name'],'decks':selected,'model':'sonic-3.6','voice':'47c38ca4-5f35-497b-b1a3-415245fb35e1','locale':'en-US','generation_config':{'emotion':'neutral','speed':0.9},'items':items}
(R/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2))
print('Total',len(items),'transcript characters',sum(len(i['transcript']) for i in items),'existing answer audio',sum(bool(i['aSoundUrl']) for i in items),flush=True)
