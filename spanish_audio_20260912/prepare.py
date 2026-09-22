"""Apply reviewed text patches, verify live cards, then freeze an audio manifest."""
import concurrent.futures,json,sys,hashlib,re,time
from pathlib import Path
from brainscape import BrainscapeClient,card_write_payload
from spanish_audio_20260912.review import read
R=Path(__file__).resolve().parent
SETTINGS={'model_id':'sonic-3.6','voice':'3597a26f-80ef-4bd5-8101-9699bc764917','locale':'es-MX','generation_config':{'emotion':'neutral','speed':0.9}}
def main():
    pid=int(sys.argv[1]);assert pid in [21303832,21945419]
    p=next(x for x in json.loads((R/'packs.json').read_text()) if x['packId']==pid)
    C=BrainscapeClient.discover(timeout=60)
    changes=[]
    for d in p['decks']:
        f=R/'changes'/f'{d["deckId"]}.json'
        if f.exists():changes.extend((d,x) for x in json.loads(f.read_text()))
    def snapshot(d):return d['deckId'],C.list_cards(pid,d['deckId'])
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        current={did:{c['cardId']:c for c in cards} for did,cards in pool.map(snapshot,p['decks'])}
    pending=[]
    for d,x in changes:
        actual=card_write_payload(current[d['deckId']][x['cardId']])
        if actual==x['after']:continue
        assert actual==x['before'],f'Concurrent text edit on {x["cardId"]}'
        pending.append((d,x))
    print('Already corrected:',len(changes)-len(pending),'; remaining:',len(pending),flush=True)
    def update_once(item):
        d,x=item;live=C.get_card(pid,d['deckId'],x['cardId'])
        actual=card_write_payload(live)
        if actual!=x['after']:
            assert actual==x['before'],f'Concurrent text edit on {x["cardId"]}'
            C.update_card(pid,d['deckId'],x['cardId'],**x['after'])
        return x['cardId']
    def update(item):
        for attempt in range(8):
            try:
                result=update_once(item)
                time.sleep(.5)
                return result
            except Exception as exc:
                if getattr(exc,'status',None) not in (429,500,502,503,504) or attempt==7:raise
                delay=min(60,5*2**attempt)
                print('Retrying card',item[1]['cardId'],'after',delay,'seconds',flush=True)
                time.sleep(delay)
    for index,item in enumerate(pending,1):
        update(item)
        if index%25==0:print('Remaining text patches applied:',index,'/',len(pending),flush=True)
    print('Text patches applied:',len(changes),flush=True)
    def freeze(d):
        live=C.list_cards(pid,d['deckId']);desired=read(d['deckId'])
        assert len(live)==len(desired)==500
        assert [c['cardId'] for c in live]==[c['cardId'] for c in desired]
        for a,b in zip(live,desired):assert card_write_payload(a)==card_write_payload(b),(d['deckId'],a['cardId'])
        (R/f'prepared_{d["deckId"]}.json').write_text(json.dumps(live,ensure_ascii=False,indent=2))
        return d,live
    items=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        for d,cards in pool.map(freeze,p['decks']):
            for c in cards:
                s=p['spanishSide'];word=c.get(s+'MdBody') or '';sentence=c.get(s+'MdFootnote') or ''
                assert word and sentence
                # Silent editorial label and acronym expansion, Spanish speech only.
                word={'chat (internet)':'chat','AC':'aire acondicionado','mts':'metros','crio':'crío','elije':'elige'}.get(word,word)
                sentence=sentence.replace('Elije ','Elige ').replace('elije ','elige ').replace(' (AC)','')
                transcript=word.rstrip('.!?')+'. <break time="500ms"/>'+sentence
                assert not re.search(r'\b(the|and|your|you|she|they|this|that|with|from|for|yourself)\b',transcript,re.I),(d['deckId'],c['cardId'],transcript)
                key=hashlib.sha256(json.dumps([SETTINGS,transcript],ensure_ascii=False,sort_keys=True).encode()).hexdigest()
                items.append({'packId':pid,'deckId':d['deckId'],'cardId':c['cardId'],'side':s,'transcript':transcript,'key':key,'text':card_write_payload(c),'otherSoundUrl':c.get(('q' if s=='a' else 'a')+'SoundUrl')})
    m={**p,'settings':SETTINGS,'items':items}
    (R/f'manifest_{pid}.json').write_text(json.dumps(m,ensure_ascii=False,indent=2))
    print('Prepared',len(items),'cards;',len({i['key'] for i in items}),'unique recordings;',sum(len(i['transcript']) for i in items),'characters',flush=True)
if __name__=='__main__':main()
