# Russian ↔ English deck repair

Completed local review of all 20,000 cards in 40 sub-decks. **3,702 cards corrected.** Each deck still contains 500 cards in its original sequence.

The corrected files are the top-level `deck_*.csv` files in `russian_english/` and `english_russian/`. The subsequent [cloud synchronization](cloud_sync/README.md) is complete: all 40 sub-decks and 20,000 cards were verified against these files.

## What was checked

- Translation meaning, part of speech, and misleading extra senses.
- Grammar, naturalness, and agreement between the two example sentences.
- Presence of the taught word or a valid inflected form in its example.
- Supporting vocabulary from earlier decks; the first 1→500 deck may use its full vocabulary. The target and common grammatical function words are allowed.

All cards received a full first pass using parallel lower-cost reviewers and an independent full second pass. Additional checks covered changed meanings and accidental substitutions of unrelated headwords. Russian headwords were preserved; deliberate English headword corrections are recorded in `approved_headword_changes.json`.

## Validation

Final automated checks: 40 decks, 0 structural errors, 0 remaining target/vocabulary candidates. These checks use Russian and English morphology and supplement the language review; they do not prove every possible interpretation or stylistic choice.

CSV format, complete fields, card counts, sequence, proposal references, and final file hashes were verified. Original files were backed up before editing.

## Changes by deck

| Direction | Band | Deck | Cards changed |
|---|---|---|---:|
| Russian → English | 1->500 | [15260182](../russian_english/deck_15260182.csv) | 29 |
| Russian → English | 500->1000 | [15260185](../russian_english/deck_15260185.csv) | 75 |
| Russian → English | 1000->1500 | [15260188](../russian_english/deck_15260188.csv) | 65 |
| Russian → English | 1500->2000 | [15260190](../russian_english/deck_15260190.csv) | 46 |
| Russian → English | 2000->2500 | [15260191](../russian_english/deck_15260191.csv) | 38 |
| Russian → English | 2500->3000 | [15260192](../russian_english/deck_15260192.csv) | 37 |
| Russian → English | 3000->3500 | [15260194](../russian_english/deck_15260194.csv) | 54 |
| Russian → English | 3500->4000 | [15260196](../russian_english/deck_15260196.csv) | 49 |
| Russian → English | 4000->4500 | [15260198](../russian_english/deck_15260198.csv) | 95 |
| Russian → English | 4500->5000 | [15260200](../russian_english/deck_15260200.csv) | 96 |
| Russian → English | 5000->5500 | [15260204](../russian_english/deck_15260204.csv) | 74 |
| Russian → English | 5500->6000 | [15260207](../russian_english/deck_15260207.csv) | 81 |
| Russian → English | 6000->6500 | [15260210](../russian_english/deck_15260210.csv) | 38 |
| Russian → English | 6500->7000 | [15260213](../russian_english/deck_15260213.csv) | 75 |
| Russian → English | 7000->7500 | [15260214](../russian_english/deck_15260214.csv) | 107 |
| Russian → English | 7500->8000 | [15260215](../russian_english/deck_15260215.csv) | 82 |
| Russian → English | 8000->8500 | [15260217](../russian_english/deck_15260217.csv) | 71 |
| Russian → English | 8500->9000 | [15260218](../russian_english/deck_15260218.csv) | 80 |
| Russian → English | 9000->9500 | [15260221](../russian_english/deck_15260221.csv) | 98 |
| Russian → English | 9500->10000 | [15260224](../russian_english/deck_15260224.csv) | 95 |
| English → Russian | 1->500 | [15260246](../english_russian/deck_15260246.csv) | 26 |
| English → Russian | 500->1000 | [15260248](../english_russian/deck_15260248.csv) | 203 |
| English → Russian | 1000->1500 | [15260251](../english_russian/deck_15260251.csv) | 154 |
| English → Russian | 1500->2000 | [15260255](../english_russian/deck_15260255.csv) | 120 |
| English → Russian | 2000->2500 | [15260256](../english_russian/deck_15260256.csv) | 105 |
| English → Russian | 2500->3000 | [15260257](../english_russian/deck_15260257.csv) | 129 |
| English → Russian | 3000->3500 | [15260260](../english_russian/deck_15260260.csv) | 135 |
| English → Russian | 3500->4000 | [15260263](../english_russian/deck_15260263.csv) | 105 |
| English → Russian | 4000->4500 | [15260266](../english_russian/deck_15260266.csv) | 117 |
| English → Russian | 4500->5000 | [15260268](../english_russian/deck_15260268.csv) | 68 |
| English → Russian | 5000->5500 | [15260269](../english_russian/deck_15260269.csv) | 75 |
| English → Russian | 5500->6000 | [15260272](../english_russian/deck_15260272.csv) | 107 |
| English → Russian | 6000->6500 | [15260277](../english_russian/deck_15260277.csv) | 84 |
| English → Russian | 6500->7000 | [15260280](../english_russian/deck_15260280.csv) | 95 |
| English → Russian | 7000->7500 | [15260281](../english_russian/deck_15260281.csv) | 131 |
| English → Russian | 7500->8000 | [15260282](../english_russian/deck_15260282.csv) | 160 |
| English → Russian | 8000->8500 | [15260283](../english_russian/deck_15260283.csv) | 97 |
| English → Russian | 8500->9000 | [15260285](../english_russian/deck_15260285.csv) | 115 |
| English → Russian | 9000->9500 | [15260287](../english_russian/deck_15260287.csv) | 125 |
| English → Russian | 9500->10000 | [22976521](../english_russian/deck_22976521.csv) | 166 |

## Review and recovery records

- `originals/`: untouched source backups.
- `logs/`: complete original-to-final before/after records, indexed by one-based card row.
- `first_pass_snapshot/`: preserved intermediate results for review history.
- `second_pass_final_*.json`: second-pass corrections and full-deck review manifests.
- `qa_current/`: final structural and vocabulary checks.
- `applied_manifest.json`: original and final hashes plus exact change counts.

Old `_chunks/`, `_chunks/fixed/`, `_vocab/`, and earlier rewrite scripts are historical working files. Do not merge them over the corrected CSVs. The earlier `audit_first25/` report describes the pre-repair sample and is superseded by this full repair.
