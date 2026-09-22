from pathlib import Path
import re,sys
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT))
from brainscape import cards_from_path

def load_source():
    decks=[]
    for pack in ['russian_english','english_russian']:
        mapping=(ROOT/pack/'file_to_deck.md').read_text()
        for filename,band in re.findall(r'\| `(deck_\d+\.csv)` \| ([^|]+) \|',mapping):
            cards=cards_from_path(ROOT/pack/filename)
            decks.append(dict(pack=pack,file=filename,band=band.strip(),cards=[dict(row=i+1,q=c['qMdBody'],a=c['aMdBody'],qe=c.get('qMdFootnote',''),ae=c.get('aMdFootnote','')) for i,c in enumerate(cards)]))
    return decks
