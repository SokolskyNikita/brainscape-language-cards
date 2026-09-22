# Third full review — 2026-09-08

All 10,000 Russian–English cards were reread again. A further 417 cards were corrected: 289 translation glosses, 121 Russian examples, and 249 English examples (overlapping counts). Every changed card received another reading. Target-word and prior-deck vocabulary checks have zero remaining candidates; all headwords, counts and order are unchanged.

All 417 corrections are saved in Brainscape. All 10,000 cards were read back and verified, including card IDs and order. The final local file checksums match the readback verification records.

Full before/after records and original snapshots: [third-pass report](../russian_english_pass3_20260908/README.md), [all changes](../russian_english_pass3_20260908/CHANGES.md), [cloud verification](../russian_english_pass3_20260908/cloud_sync/results.json).

“Корточки” now describes a squat/squatting position. “Он сел на корточки.” → “He squatted down.”

Earlier reports below are historical. The current top-level CSVs include all completed passes.

---

# Fresh recheck — 2026-09-08

All 10,000 Russian–English cards were reread in a fresh semantic pass. A further 337 cards were corrected: 181 translation glosses, 148 Russian examples, and 239 English examples (overlapping counts). Headwords, card counts, and order are unchanged.

The current files pass the fresh target-word and vocabulary-order checks. Full before/after records and backups are in `../recheck_20260908/`. Cloud synchronization of this fresh pass is complete: 337 cards updated in place and all 10,000 cards read back and verified. Card IDs and ordering were preserved. See `../recheck_20260908/cloud_sync/results.json`.

The earlier review below is historical; the current top-level CSVs include both reviews.

---

# Full-deck repair — 2026-09-07

All 20 top-level deck CSVs (10,000 cards) were reviewed for translations, examples, target use, and vocabulary sequencing. 1,385 cards were changed locally. Card counts and sequence were preserved.

The top-level `deck_*.csv` files are the current corrected decks. Original snapshots, complete change logs, patch scripts, and validation records are in `../repair_20260907/`.

`_chunks/`, `_chunks/fixed/`, old rewrite scripts, and `_vocab/` predate this repair. They are historical working artifacts; do not merge or run them over the corrected top-level decks. Regenerate working chunks from the current CSVs before another editing round.

The current vocabulary rule is **prior decks only**, except that the first 1→500 deck may use its own full vocabulary. The target itself and common function words are allowed. Older fixer-guide language allowing the current deck in later bands is superseded by this user instruction.

Cloud synchronization is now complete. All 20 sub-decks were uploaded sequentially and all 10,000 cards verified against these files. See `../repair_20260907/cloud_sync/README.md` for the completion report.
