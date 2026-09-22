from pathlib import Path
import sys,json,re,hashlib,time
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from brainscape import BrainscapeClient,cards_from_path
BASE=Path(__file__).resolve().parent
client=BrainscapeClient.discover(timeout=20,retries=1)
manifest=[]
for pack,pid in [('english_russian',21917816),('russian_english',21919521)]:
 for filename,band in re.findall(r'\| `(deck_\d+\.csv)` \| ([^|]+) \|',(ROOT/pack/'file_to_deck.md').read_text()):
  did=int(filename[5:-4]);out=BASE/'live'/pack/f'{did}.json';out.parent.mkdir(parents=True,exist_ok=True)
  if out.exists():cards=json.loads(out.read_text())
  else:
   cards=client.list_cards(pid,did,per_page=500);out.write_text(json.dumps(cards,ensure_ascii=False,indent=2));time.sleep(.6)
  local=cards_from_path(ROOT/pack/filename)
  fields=['qMdBody','aMdBody','qMdFootnote','aMdFootnote']
  differences=sum(any(a.get(k,'')!=b.get(k,'') for k in fields) for a,b in zip(cards,local))
  assert len(cards)==len(local)==500
  manifest.append(dict(pack=pack,deck=did,band=band.strip(),count=len(cards),local_differences=differences,local_sha256=hashlib.sha256((ROOT/pack/filename).read_bytes()).hexdigest()))
  print(pack,band.strip(),len(cards),'local differences',differences,flush=True)
(BASE/'manifest.json').write_text(json.dumps(dict(checked_at=datetime.now(timezone.utc).isoformat(),decks=manifest),indent=2))
