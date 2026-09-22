import base64,hashlib,json
from pathlib import Path
from urllib.request import urlopen
from brainscape import BrainscapeClient
root=Path(__file__).resolve().parent
s=json.loads((root/'state.json').read_text());c=BrainscapeClient.discover(retries=1);p=s['pack']['packId'];d=s['deck']['deckId']
assert p==24125111 and d==22994657
out=[]
cards=c.list_cards(p,d)
for card in cards:
 for field,filename in [('qSoundUrl','question.mp3'),('aSoundUrl','answer.mp3')]:
  if card.get(field):
   with urlopen(card[field]) as r: raw=r.read();mime=r.headers.get('Content-Type');status=r.status
   out.append({'test':'stored audio bytes','cardId':card['cardId'],'field':field,'status':status,'mime':mime,'bytes':len(raw),'matches_original':hashlib.sha256(raw).digest()==hashlib.sha256((root/filename).read_bytes()).digest()})
url=cards[0]['qSoundUrl'];data='data:audio/mpeg;base64,'+base64.b64encode((root/'question.mp3').read_bytes()).decode()
for name,method,body in [('05 Direct PATCH data URL','patch',{'qSoundUrl':data}),('06 Attachment HTTPS URL','attach',{'qSoundUrl':url}),('07 Markdown audio link','text',{}),('08 HTML audio element','html',{})]:
 q=name
 if method=='text':q+='\n\n[Play sample audio]('+url+')'
 if method=='html':q+='\n\n<audio controls src="'+url+'"></audio>'
 card=c.create_card(p,d,question=q,answer='Test control. Compare with the native play button on cards 1–3.')
 row={'label':name,'cardId':card['cardId']};s['cards'].append(row);(root/'state.json').write_text(json.dumps(s,indent=2))
 try:
  if method in ['patch','attach']:row['response']=c.request('PATCH' if method=='patch' else 'POST',f'packs/{p}/decks/{d}/cards/{card["cardId"]}'+('/atchs' if method=='attach' else ''),body=body)
 except Exception as e:row['error']={'status':getattr(e,'status',None),'message':str(e)}
 if 'response' in row:row['response']={k:v for k,v in row['response'].items() if k in ['jobId','cardId','qSoundUrl']}
 (root/'state.json').write_text(json.dumps(s,indent=2));out.append(row)
(root/'probe_results.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
