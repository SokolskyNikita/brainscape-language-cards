# English example repairs — 22 September 2026

Completed and verified in Brainscape and local CSV exports.

| Direction | Cards repaired | English audio replaced |
|---|---:|---:|
| English → Russian | 272 | 272 |
| Russian → English | 472 | 472 |
| Total | 744 | 744 |

650 Russian example translations were updated to match the revised English.
Every revised example retains its English and Russian target. Card IDs, target
headwords, deck membership, order, and the other audio side were preserved.
All 20,000 cards across 40 decks were checked against the expected text; all
744 replacement audio files were downloaded from Brainscape and matched by SHA-256.
The vocabulary audit on those verified cloud snapshots reports **zero remaining
violations under the agreed rules**.

## Rules applied

- English → Russian headword positions supply the English vocabulary timeline
  for both directions. Deck 1 permits the first 500 heads; subsequent decks
  permit prior 500-card groups plus the current English target.
- An inflected form explicitly taught in the same meaning must wait for its
  scheduled deck. Otherwise, an inflection of an allowed base is permitted.
- Context-specific sense reviews distinguish homonyms such as past-tense
  “saw” from the cutting tool. Two existing reviews were carried forward to
  their revised sentences after checking that their meaning remained the same.
- Approved exemptions: an, not, don't, their, can't, will, should, shall, may,
  let's, isn't, please, because, everyone, neither, during.
- Only English vocabulary is restricted; Russian translations may use any
  appropriate Russian words.

Your mom's example, Russian → English #2140, now reads:
“Follow the law strictly.” / “Следуйте закону строго.”
It no longer introduces “forbidden” ahead of its scheduled English headword.

## Audio

737 distinct recordings serve the 744 cards; seven exact transcript matches
share recordings. Cartesia Sonic 3.6, Daniel voice
`47c38ca4-5f35-497b-b1a3-415245fb35e1`, en-US, neutral emotion, speed 0.9.
Each recording contains the English target, a 500 ms pause, and the new example.
Russian parenthetical annotations are omitted from spoken heads. Output is
44.1 kHz, 128 kbps mono MP3. Every file passed decoding and duration checks.
Fresh caches are keyed by the complete transcript and synthesis settings.

## Evidence

- [All before/after sentence changes](changes.md)
- [Structured changes with card IDs](changes.json)
- [Cloud verification result](result.json)
- [Audit of verified cloud snapshots](qa_live/repair_validation.json)
- [Remaining vocabulary findings (empty)](qa_live/final_findings.json)
- [Source snapshot hashes](qa_live/final_source_manifest.json)
- [Audio manifest](audio_manifest.json)
- [Audio generation result](audio_result.json)

`replacements.json` is the reviewed replacement source. The `manual_*.tsv`,
`auto_drafts.json`, and draft/refinement scripts are intermediate drafting artifacts.

`originals/` and `before/` preserve the previous CSVs and live cards.
`staged/` contains the repaired CSVs; identical files were copied to the two
normal deck directories after cloud verification. `after/` contains verified
live cards. `receipts/` records attachment jobs; `verified/` records per-deck checks.
No credentials are stored in these artifacts.

## Reproduction

From `cards/` (with the environment activated):

```sh
python3 sentence_repair_20260922/validate.py --live
```

This is a read-only audit of the verified post-sync snapshots. The older
`vocabulary_audit_20260922` reports intentionally preserve the pre-repair audit.

The resumable workflow is `stage.py`, `validate.py`, `generate_audio.py`, then
`sync.py --apply`. Audio generation uses Cartesia; sync writes to Brainscape.
Generation and sync reject changed plans after the audio manifest is created.
The sync performs fresh conflict checks and preserves backups and receipts.
Do not run concurrent copies of the sync script.
