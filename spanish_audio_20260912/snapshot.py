import concurrent.futures, json
from pathlib import Path
from brainscape import BrainscapeClient

R=Path(__file__).resolve().parent
C=BrainscapeClient.discover(timeout=60)
packs=[]
for pid,side in [(21945419,'a'),(21303832,'q')]:
    decks=C.list_decks(pid)
    assert len(decks)==16
    packs.append({'packId':pid,'spanishSide':side,'decks':decks})
(R/'packs.json').write_text(json.dumps(packs,ensure_ascii=False,indent=2))
def get(item):
    p,d=item
    dest=R/f'before_{d["deckId"]}.json'
    if dest.exists(): cards=json.loads(dest.read_text())
    else:
        cards=C.list_cards(p['packId'],d['deckId'])
        dest.write_text(json.dumps(cards,ensure_ascii=False,indent=2))
    assert len(cards)==500
    print(p['packId'],d['deckId'],d['name'],len(cards),flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    list(pool.map(get,[(p,d) for p in packs for d in p['decks']]))
