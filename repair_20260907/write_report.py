"""Summarize the applied local repair from its validation records."""
import json
from pathlib import Path
from helper import BASE

data = json.loads((BASE / 'applied_manifest.json').read_text())
qa = json.loads((BASE / 'qa_current' / 'summary.json').read_text())
changed = sum(d['changed'] for d in data)
lines = [
    '# Russian ↔ English deck repair',
    '',
    f'Completed local review of all 20,000 cards in 40 sub-decks. **{changed:,} cards corrected.** Each deck still contains 500 cards in its original sequence.',
    '',
    'The corrected files are the top-level `deck_*.csv` files in `russian_english/` and `english_russian/`. No Brainscape upload was performed.',
    '',
    '## What was checked',
    '',
    '- Translation meaning, part of speech, and misleading extra senses.',
    '- Grammar, naturalness, and agreement between the two example sentences.',
    '- Presence of the taught word or a valid inflected form in its example.',
    '- Supporting vocabulary from earlier decks; the first 1→500 deck may use its full vocabulary. The target and common grammatical function words are allowed.',
    '',
    'All cards received a full first pass using parallel lower-cost reviewers and an independent full second pass. Additional checks covered changed meanings and accidental substitutions of unrelated headwords. Russian headwords were preserved; deliberate English headword corrections are recorded in `approved_headword_changes.json`.',
    '',
    '## Validation',
    '',
    f"Final automated checks: {qa['decks']} decks, {qa['structural_errors']} structural errors, {qa['candidate_cards']} remaining target/vocabulary candidates. These checks use Russian and English morphology and supplement the language review; they do not prove every possible interpretation or stylistic choice.",
    '',
    'CSV format, complete fields, card counts, sequence, proposal references, and final file hashes were verified. Original files were backed up before editing.',
    '',
    '## Changes by deck',
    '',
    '| Direction | Band | Deck | Cards changed |',
    '|---|---|---|---:|',
]
for d in data:
    direction = 'Russian → English' if d['pack'] == 'russian_english' else 'English → Russian'
    lines.append(f"| {direction} | {d['band']} | [{d['deck']}](../{d['pack']}/deck_{d['deck']}.csv) | {d['changed']} |")
lines += [
    '',
    '## Review and recovery records',
    '',
    '- `originals/`: untouched source backups.',
    '- `logs/`: complete original-to-final before/after records, indexed by one-based card row.',
    '- `first_pass_snapshot/`: preserved intermediate results for review history.',
    '- `second_pass_final_*.json`: second-pass corrections and full-deck review manifests.',
    '- `qa_current/`: final structural and vocabulary checks.',
    '- `applied_manifest.json`: original and final hashes plus exact change counts.',
    '',
    'Old `_chunks/`, `_chunks/fixed/`, `_vocab/`, and earlier rewrite scripts are historical working files. Do not merge them over the corrected CSVs. The earlier `audit_first25/` report describes the pre-repair sample and is superseded by this full repair.',
    '',
]
(BASE / 'README.md').write_text('\n'.join(lines))
print(BASE / 'README.md')
