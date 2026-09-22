"""Summarize reviewed corrections and validate frozen local/live evidence."""
import json
from pathlib import Path
from brainscape import card_write_payload
from spanish_audio_20260912.review import read

R=Path(__file__).resolve().parent
packs=json.loads((R/'packs.json').read_text())
results=[]
detail=['# Spanish deck corrections — 12 September 2026','',
        'Each entry records the original card ID, its position, and the corrected fields. Full request payloads are preserved in the changes directory.','']
for p in packs:
    pid=p['packId'];label='English → Spanish' if p['spanishSide']=='a' else 'Spanish → English'
    count=0;decks=[]
    detail.extend([f'## {label}',''])
    manifest=R/f'manifest_{pid}.json'
    for d in p['decks']:
        did=d['deckId'];f=R/'changes'/f'{did}.json'
        changes=json.loads(f.read_text()) if f.exists() else []
        count+=len(changes)
        frozen=R/f'prepared_{did}.json'
        verified=False
        if frozen.exists():
            current=json.loads(frozen.read_text());expected=read(did)
            verified=(len(current)==500 and [c['cardId'] for c in current]==[c['cardId'] for c in expected] and
                      all(card_write_payload(a)==card_write_payload(b) for a,b in zip(current,expected)))
        decks.append({'deckId':did,'name':d['name'],'cards':500,'changedCards':len(changes),'textIdsOrderVerified':verified})
        if changes:detail.extend([f'### {d["name"]} — deck {did}',''])
        for c in changes:
            detail.extend([f'**Card {c["row"]} · ID {c["cardId"]}**',''])
            for field in ['qMdBody','qMdFootnote','aMdBody','aMdFootnote']:
                before,after=c['before'][field],c['after'][field]
                if before==after:continue
                name={'qMdBody':'Question term','qMdFootnote':'Question example','aMdBody':'Answer term','aMdFootnote':'Answer example'}[field]
                detail.extend([f'- {name}: {before} → **{after}**'])
            detail.extend(['',c['reason'],''])
    results.append({'packId':pid,'name':label,'spanishSide':p['spanishSide'],'cards':8000,'changedCards':count,'decks':decks,'allTextVerified':all(d['textIdsOrderVerified'] for d in decks)})
(R/'corrections.md').write_text('\n'.join(detail))
ready=all(p['allTextVerified'] for p in results)
status={'date':'2026-09-12','textStatus':'complete' if ready else 'verification_pending','packs':results,
        'audioStatus':'awaiting_explicit_Cartesia_approval','audioCards':16000,'audioLocale':'es-MX',
        'audioVoice':'Ximena','audioScope':'Spanish term and example only; answer for English→Spanish and question for Spanish→English',
        'bulkAudioGenerated':0,'bulkAudioUploaded':0,'localXlsxFilesUpdated':26,'localXlsxCellsChanged':558}
(R/'status.json').write_text(json.dumps(status,ensure_ascii=False,indent=2))
print(json.dumps({k:v for k,v in status.items() if k!='packs'},ensure_ascii=False))
