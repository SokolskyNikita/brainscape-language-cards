# Spanish deck repair and audio — 12 September 2026

The live classes contain 16,000 cards in 32 decks:

| Class | Pack ID | Cards | Spanish audio side |
| --- | --- | --- | --- |
| English → Spanish | 21945419 | 8,000 | Answer |
| Spanish → English | 21303832 | 8,000 | Question |

## Corrections

The review produced corrections on 360 English → Spanish cards: 308 content corrections plus 52 additional cards needing punctuation only. It also repaired 15 malformed or misspelled Spanish → English cards before preparing their Spanish audio.

The English → Spanish review checked all headword pairs, manually reviewed the first 1,500 complete cards, and used structural checks and targeted review of suspicious examples across the remaining 6,500 cards. It does not establish that every original example is free of possible stylistic improvements.

`corrections.md` lists every changed field. `changes/` preserves complete before/after request payloads and existing card IDs. `before_*.json` contains the original live backups. `prepared_*.json` contains verified live cards after correction. `status.json` records whether every card's text, ID, and order has passed comparison.

Final verification passed for all 16,000 cards across both classes. The corrected text matches the reviewed payloads, and original card IDs, order, learning statistics, and existing audio are preserved.

The 26 affected local XLSX files have also been updated. All 26,052 cells were checked against the originals and the 558 intended cell changes; visible formatting and the two-column import structure were preserved. `xlsx_backups/` holds the originals.

## Audio status

The initial Cartesia voice-generation test succeeded. Bulk audio generation and upload have not started.

Automatic approval review rejected the bulk run because it requires explicit approval to send the Spanish card text to Cartesia. Approval was requested to send the Spanish terms and examples for all 16,000 cards, use the account's Cartesia API credits, and upload the resulting recordings to Brainscape. This approval is still pending.

The selected voice is Ximena with Mexican Spanish locale (`es-MX`), using Sonic 3.6 at speed 0.9. Each transcript contains the Spanish headword, a short pause, and its Spanish example. English translations, prompts, and headings are excluded. Recordings for identical transcripts are reused across the two directions.

## Resume after explicit approval

From the project directory, first confirm both packs show `allTextVerified: true` in `status.json`. The frozen manifests must not be changed after audio verification starts.

```sh
PYTHONPATH=. python3 spanish_audio_20260912/run.py 21303832
PYTHONPATH=. python3 spanish_audio_20260912/run.py 21945419
```

The runner uses the existing Cartesia key and Brainscape session without printing them. It saves recordings, upload receipts, and per-deck progress for resumption. It attaches MP3s only to the Spanish face and verifies the downloaded attachment bytes, original card text, card IDs/order, and unchanged audio on the other face. `result_PACKID.json` is written only after all 8,000 cards in that class pass verification.

No bulk generation or upload should be claimed complete until both result files exist and report completion.
