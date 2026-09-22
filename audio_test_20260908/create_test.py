import json
from pathlib import Path
from brainscape import BrainscapeClient
ROOT=Path(__file__).resolve().parent
state=ROOT/'state.json'
if state.exists():
    raise SystemExit('State already exists; refusing to create a duplicate sandbox.')
c=BrainscapeClient.discover(retries=1)
p=c.create_pack('Audio API TEST — 2026-09-08',desc='Separate audio experiment. Fresh synthetic speech only. KEEP for manual validation.',private=True)
s={'pack':p,'cards':[]};state.write_text(json.dumps(s,indent=2))
pid=p['packId']
d=c.create_deck(pid,'Audio compatibility tests — KEEP',desc='Generated speech: question, answer, both sides, and negative controls.')
s['deck']=d;state.write_text(json.dumps(s,indent=2));did=d['deckId']
for label,kwargs in [('01 Question audio',{'question_file':ROOT/'question.mp3'}),('02 Answer audio',{'answer_file':ROOT/'answer.mp3'}),('03 Both sides',{'question_file':ROOT/'question.mp3','answer_file':ROOT/'answer.mp3'}),('04 Text-only control',{})]:
    card=c.create_card(pid,did,question=label+'\n\nWhat is two plus two?',answer='Two plus two is four.')
    row={'label':label,'cardId':card['cardId']};s['cards'].append(row);state.write_text(json.dumps(s,indent=2))
    if kwargs:
        try: row['upload']=c.attach_audio(pid,did,card['cardId'],**kwargs)
        except Exception as e: row['error']={'type':type(e).__name__,'message':str(e),'status':getattr(e,'status',None),'payload':getattr(e,'payload',None)}
    state.write_text(json.dumps(s,indent=2))
print(json.dumps(s,indent=2))
