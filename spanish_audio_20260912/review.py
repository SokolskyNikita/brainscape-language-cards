import json,sys,copy
from pathlib import Path
from brainscape import card_write_payload
R=Path(__file__).resolve().parent
KEYS=['qMdBody','aMdBody','qMdFootnote','aMdFootnote']
def read(did):
    cards=json.loads((R/f'before_{did}.json').read_text())
    p=R/'changes'/f'{did}.json'
    if p.exists():
        for x in json.loads(p.read_text()):cards[x['row']-1].update(x['after'])
    return cards
def patch(did,changes):
    original=json.loads((R/f'before_{did}.json').read_text())
    cards=read(did);dest=R/'changes'/f'{did}.json';dest.parent.mkdir(exist_ok=True)
    prior={x['row']:x for x in json.loads(dest.read_text())} if dest.exists() else {}
    for row,(values,reason) in changes.items():
        cards[row-1].update(values)
        payload=card_write_payload(cards[row-1])
        prior[row]={'row':row,'cardId':cards[row-1]['cardId'],'before':card_write_payload(original[row-1]),'after':payload,'reason':reason}
    dest.write_text(json.dumps([prior[k] for k in sorted(prior)],ensure_ascii=False,indent=2))
    print(did,'changed',len(prior))
if __name__=='__main__':
    did=int(sys.argv[1]);start=int(sys.argv[2]) if len(sys.argv)>2 else 1;end=int(sys.argv[3]) if len(sys.argv)>3 else 500
    mode=sys.argv[4] if len(sys.argv)>4 else 'full'
    for i,c in enumerate(read(did),1):
        if start<=i<=end:
            ks=KEYS[:2] if mode=='pairs' else KEYS
            print(str(i)+'|'+'|'.join(c.get(k) or '' for k in ks))
