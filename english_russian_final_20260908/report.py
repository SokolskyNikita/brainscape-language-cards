from pathlib import Path
from collections import Counter
import json,hashlib,sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from brainscape import cards_from_path
BASE=Path(__file__).resolve().parent; ROOT=BASE.parent
keys=['qMdBody','aMdBody','qMdFootnote','aMdFootnote']; labels=['English target','Russian translation','English example','Russian example']
changes=[];decks=[];counts=Counter()
for n,p in enumerate(sorted((ROOT/'english_russian').glob('deck_*.csv'))):
 deck=p.stem[5:];a=cards_from_path(BASE/'originals'/p.name);b=cards_from_path(p)
 log=json.loads((BASE/f'{deck}.json').read_text());reasons={c['row']:c['reason'] for c in log['changes']};dc=[]
 assert log['reviewed']==500 and len(a)==len(b)==500
 for row,(x,y) in enumerate(zip(a,b),1):
  assert x[keys[0]]==y[keys[0]]
  before=[x[k] for k in keys];after=[y[k] for k in keys]
  if before==after:continue
  assert row in reasons
  fields=[labels[i] for i in range(4) if before[i]!=after[i]];counts.update(fields)
  c=dict(deck=deck,row=row,card_number=n*500+row,before=before,after=after,fields=fields,reason=reasons[row]);changes.append(c);dc.append(c)
 (BASE/f'{deck}.json').write_text(json.dumps(dict(deck=deck,reviewed=500,changes=dc),ensure_ascii=False,indent=2)+'\n')
 decks.append(dict(deck=deck,cards=500,changed=len(dc),sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
assert len(decks)==20 and json.loads((BASE/'qa.json').read_text())==[]
sync=BASE/'cloud_sync/results.json';results=json.loads(sync.read_text()) if sync.exists() else []
complete=len(results)==20 and all(next((r for r in results if str(r['deck'])==d['deck']),{}).get('sha256')==d['sha256'] for d in decks)
summary=dict(reviewed_cards=10000,reviewed_decks=20,changed_cards=len(changes),changed_fields=dict(counts),qa_candidates=0,cloud_complete=complete,cloud_verified_cards=sum(r['verified_cards'] for r in results),decks=decks)
(BASE/'changes.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2)+'\n')
(BASE/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
lines=['# English → Russian: final review changes — 2026-09-08','',f'{len(changes)} cards corrected after rereading all 10,000. Each entry gives the state before this pass and the final correction.','']
for c in changes:
 lines.extend([f"## Card {c['card_number']} · {c['after'][0]}",'',f"Deck {c['deck']}, row {c['row']}.",'','| Field | Before | After |','|---|---|---|'])
 for i in range(4):
  if c['before'][i]!=c['after'][i]:
   esc=lambda s:s.replace('|','\\|').replace('\n','<br>')
   lines.append(f"| {labels[i]} | {esc(c['before'][i])} | {esc(c['after'][i])} |")
 lines.extend(['',c['reason'],''])
(BASE/'CHANGES.md').write_text('\n'.join(lines))
status='Saved in place to Brainscape pack 21917816. All 10,000 live cards were read back and matched the corrected files; existing card IDs and order were preserved.' if complete else 'Local corrections and validation are complete. Brainscape synchronization and full live verification are in progress.'
text=f'''# English → Russian: final review — 2026-09-08

All **10,000 cards across 20 decks** were reread for translation accuracy, natural and equivalent examples, use of the listed targets, and supporting vocabulary introduced in earlier decks. **{len(changes)} cards were corrected** in this pass. All corrected cards received a second reading.

{status}

The changes include false friends, overly narrow unlabelled meanings, gender and register distinctions, noun/adjective mismatches, inaccurate tense or meaning in example pairs, and unnecessarily advanced supporting vocabulary. Multiple legitimate senses are retained where useful; these cards are learning prompts, not exhaustive dictionary entries.

## Validation

- Exactly 500 cards per deck and 10,000 overall; original English targets and order preserved.
- All four fields present on every card.
- Morphology-based checks found no remaining target-use or vocabulary-sequencing candidates, followed by manual review of the changed examples. These checks are aids, not proof of linguistic perfection.
- Supporting content vocabulary uses prior decks only, with the user's exception allowing the entire first 500-card deck. Function words, natural inflections, and the card's own target are allowed.
- Changed Russian translations: {counts['Russian translation']}; English examples: {counts['English example']}; Russian examples: {counts['Russian example']}. These field counts overlap across cards.

## Changes by deck

| Cards | Deck ID | Corrected cards |
|---|---|---:|
'''
for i,d in enumerate(decks):text+=f"| {i*500+1}–{(i+1)*500} | {d['deck']} | {d['changed']} |\n"
text+='''
## Review records

- [20 selected examples](20_EXAMPLES.md)
- [Every correction, with before/after text](CHANGES.md)
- [Structured changes](changes.json)
- [Counts and final file fingerprints](summary.json)
- Original pre-pass snapshots: `originals/`.
- Live pre-update backups and verification records: `cloud_sync/`.

## Dictionary checks

Selected sense distinctions were checked against published reference entries:

- **Unlearn**: deliberately abandon a learned habit or method, rather than simply lose a skill. [Cambridge Dictionary](https://dictionary.cambridge.org/dictionary/english/unlearn).
- **Fir**: the main botanical sense is the genus *Abies*, Russian «пихта». [Merriam-Webster](https://www.merriam-webster.com/dictionary/fir) and [Большая российская энциклопедия](https://bigenc.ru/c/pikhta-fb77be).
- **Groat**: an old British coin; distinguish singular *groat* from grain *groats*. [Merriam-Webster](https://www.merriam-webster.com/dictionary/groat).
- **Ensign**: a flag or a junior military/naval officer; historical Russian «прапорщик» needs a sense label. [Cambridge Dictionary](https://dictionary.cambridge.org/dictionary/english/ensign).
- **Suite** can mean a retinue, although this use is uncommon. [Merriam-Webster: retinue](https://www.merriam-webster.com/dictionary/retinue).
'''
(BASE/'README.md').write_text(text)
print(json.dumps({k:v for k,v in summary.items() if k!='decks'},ensure_ascii=False))
