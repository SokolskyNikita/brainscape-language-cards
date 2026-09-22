"""Correct one Russian future tense after the main sync; English audio is unchanged."""
from pathlib import Path
import copy,csv,hashlib,json,sys,time
B=Path(__file__).resolve().parent;R=B.parent;sys.path.insert(0,str(R))
from brainscape import BrainscapeClient,cards_from_path
from brainscape.cards import canonicalize_card,card_write_payload
from generate_audio import atomic,manifest

def main():
 result=json.loads((B/'result.json').read_text());assert result['status']=='complete'
 changes=json.loads((B/'changes.json').read_text());x=next(x for x in changes if x['pack']=='english_russian' and x['overall']==6645)
 assert x['after_english_example']=='The dean will welcome new students.'
 old=copy.deepcopy(x['after_card']);new=copy.deepcopy(old);new['aMdFootnote']='Декан будет приветствовать новых студентов.';new=canonicalize_card(new)
 assert all(old[k]==new[k] for k in ['qMdBody','aMdBody','qMdFootnote'])
 client=BrainscapeClient.discover(timeout=45,retries=3);live=client.get_card(x['packId'],x['deckId'],x['cardId'])
 assert card_write_payload(live) in [card_write_payload(old),card_write_payload(new)]
 audit_path=B/'translation_correction_before.json'
 if not audit_path.exists():atomic(audit_path,live)
 if card_write_payload(live)!=card_write_payload(new):client.update_card(x['packId'],x['deckId'],x['cardId'],**card_write_payload(new))
 verified=client.get_card(x['packId'],x['deckId'],x['cardId'])
 assert card_write_payload(verified)==card_write_payload(new)
 assert all(live.get(k)==verified.get(k) for k in ['qSoundUrl','aSoundUrl'])
 x['after_card']=new;x['after_russian_example']=new['aMdFootnote']
 atomic(B/'changes.json',changes)
 replacements=json.loads((B/'replacements.json').read_text());replacements['english_russian:6645']['ru']=new['aMdFootnote'];atomic(B/'replacements.json',replacements)
 snapshot=B/'after'/x['pack']/f'{x["deckId"]}.json';cards=json.loads(snapshot.read_text());assert cards[x['row']-1]['cardId']==x['cardId'];cards[x['row']-1]=verified;atomic(snapshot,cards)
 for folder in [B/'staged',R]:
  path=folder/x['pack']/f'deck_{x["deckId"]}.csv';local=cards_from_path(path)
  assert card_write_payload(local[x['row']-1]) in [card_write_payload(old),card_write_payload(new)]
  local[x['row']-1]=new
  with path.open('w',newline='') as f:
   w=csv.writer(f,lineterminator='\n');w.writerow(['Question','Answer']);w.writerows((c['question'],c['answer']) for c in local)
  assert [card_write_payload(c) for c in cards_from_path(path)]==[card_write_payload(c) for c in cards]
 previous=json.loads((B/'audio_manifest.json').read_text());current=manifest()
 assert previous['items']==current['items'] and previous['settings']==current['settings'],'English audio must remain identical'
 atomic(B/'audio_manifest.json',current);mh=hashlib.sha256((B/'audio_manifest.json').read_bytes()).hexdigest()
 aresult=json.loads((B/'audio_result.json').read_text());aresult['manifest_sha256']=mh;atomic(B/'audio_result.json',aresult)
 detail=B/'changes.md';detail.write_text(detail.read_text().replace('Декан приветствует новых студентов.',new['aMdFootnote']))
 result['verifiedAt']=time.time()
 result['manifest_sha256']=mh;result['translation_correction']={'cardId':x['cardId'],'overall':6645,'verifiedAt':time.time(),'audio_preserved':True};atomic(B/'result.json',result)
 print('Corrected and verified Russian future tense on English → Russian #6645; English audio preserved.')
if __name__=='__main__':main()
