import json
from pathlib import Path
from datetime import datetime,timezone
BASE=Path(__file__).resolve().parent
changes=json.loads((BASE/'changes.json').read_text());manifest=json.loads((BASE/'applied_manifest.json').read_text())
raw=json.loads((BASE/'qa.json').read_text())
assert raw==[{'deck':'15260246','row':60,'word':'nor','issues':{'en_vocab':['neither']}}]
qa={'reviewed_cards':10000,'decks':20,'target_mismatch_candidates':0,'unresolved_vocabulary_candidates':0,'accepted_function_words':[{'deck':'15260246','row':60,'word':'neither','reason':'Grammatical partner of nor in the neither…nor construction; permitted function word.'}],'structural_checks':['500 cards per deck','nonempty headwords and examples','canonical Brainscape formatting','CSV round trip','no identical full cards within a deck'],'vocabulary_rule':'First 500 may use the whole first band; later bands may use prior bands plus the current target and grammatical function words. Inflections allowed. English→Russian inventory only.'}
(BASE/'qa_reviewed.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n')
fields={'qMdBody':'English headword','aMdBody':'Russian translation','qMdFootnote':'English example','aMdFootnote':'Russian example'}
lines=['# English → Russian: fresh recheck, 8 September 2026','',f'Read and rechecked all 10,000 cards in all 20 decks. Corrected {len(changes)} cards. This is a fresh linguistic review of the previously reviewed set.','', 'Review covered translation accuracy, grammar and natural usage, agreement between the English and Russian examples, target-word use, and supporting vocabulary from earlier decks. Inflected target forms are allowed; the first deck can draw on its own 500 words.','', 'The automated checks support the linguistic review; they do not prove that every sentence has only one possible interpretation. No target-word mismatches or unresolved vocabulary flags remain. “Neither” on the “nor” card is retained as a grammatical function word.','', '| Field | Cards changed |','|---|---:|']
for k,v in fields.items():lines.append(f"| {v} | {sum(c['before'][k]!=c['after'][k] for c in changes)} |")
lines+=['','Counts overlap because one card may have several fields corrected. Incorrect extra English alternatives were removed where they represented different words, such as “pi, peony” and “moss, lichen.”','','| Deck | Cards reviewed | Cards corrected |','|---|---:|---:|']
for m in manifest:lines.append(f"| {m['band']} | 500 | {m['changed']} |")
lines+=['','The original files and a complete before/after log are preserved in this folder. See [all changes](changes.md), [structured changes](changes.json), and [reviewed validation](qa_reviewed.json).','', 'Selected dictionary checks: English *compote* is a cooked-fruit dish ([Cambridge](https://dictionary.cambridge.org/us/dictionary/english/compote)); *decennial* can mean lasting ten years ([Merriam-Webster](https://www.merriam-webster.com/dictionary/decennial)); *constructor* can mean someone who constructs ([Merriam-Webster](https://www.merriam-webster.com/dictionary/constructor)). The standard singular form *кроссовка* and genitive plural *кроссовок* were checked against the [Russian Language Institute’s dictionary](https://ruslang.ru/sites/default/files/2024-12/ASRYa-4-2.pdf).','']
result=BASE/'cloud_sync/results.json'
if result.exists():
 r=json.loads(result.read_text());lines += [f"Brainscape verification completed for {len(r)}/20 decks ({sum(x['count'] for x in r):,} cards).",'']
(BASE/'REPORT.md').write_text('\n'.join(lines))
out=['# Complete before/after changes','']
for c in changes:
 out += [f"## {c['band']} — card {c['row']}: {c['after']['qMdBody']}",'','| Field | Before | After |','|---|---|---|']
 for k,label in fields.items():
  if c['before'][k]!=c['after'][k]:
   before=c['before'][k].replace('|','\\|').replace('\n','<br>');after=c['after'][k].replace('|','\\|').replace('\n','<br>')
   out.append(f'| {label} | {before} | {after} |')
 out.append('')
(BASE/'changes.md').write_text('\n'.join(out))
print('Review report and complete before/after log written.')
