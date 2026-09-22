from pathlib import Path
import sys,json,concurrent.futures,time
B=Path(__file__).resolve().parent;R=B.parent;sys.path.insert(0,str(R))
from brainscape import BrainscapeClient,cards_from_path
c=BrainscapeClient.discover(timeout=40,retries=2)
plan=json.loads((B/'plan.json').read_text());pairs=sorted({(x['pack'],x['packId'],x['deckId']) for x in plan})
def fetch(x):
 pack,pid,did=x;p=B/'before'/pack/f'{did}.json';p.parent.mkdir(parents=True,exist_ok=True)
 if p.exists():live=json.loads(p.read_text())
 else:
  live=c.list_cards(pid,did,per_page=500);p.write_text(json.dumps(live,ensure_ascii=False,indent=2))
 old=cards_from_path(B/'originals'/pack/f'deck_{did}.csv')
 assert len(live)==len(old)==500
 assert all(all(a.get(k,'')==b.get(k,'') for k in ['qMdBody','aMdBody','qMdFootnote','aMdFootnote']) for a,b in zip(live,old)),f'Live text conflict {pack}/{did}'
 byid={x['cardId']:x for x in live}
 for x in plan:
  if x['pack']==pack and x['deckId']==did:assert live[x['row']-1]['cardId']==x['cardId']
 print(pack,did,'500 cards; unchanged text and IDs',flush=True)
 return dict(pack=pack,packId=pid,deckId=did,cards=500)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:rows=list(pool.map(fetch,pairs))
(B/'preflight.json').write_text(json.dumps(dict(checked_at=time.time(),decks=rows),indent=2))
