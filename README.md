# Brainscape language cards

English, Russian, and Spanish flashcard decks for Brainscape, with reviewed
examples, vocabulary-sequencing audits, and reproducible audio workflows.

This repository preserves the working decks and the evidence behind their changes.
Dated workspaces are deliberate history: they contain reviewed proposals,
originals, card IDs, sense decisions, audio settings, conflict checks, receipts,
and verification snapshots. Do not treat them as disposable build output.

## Current decks

| Folder | Role |
| --- | --- |
| `english_russian/` | Current 10,000-card English → Russian CSVs |
| `russian_english/` | Current 10,000-card Russian → English CSVs |
| `spanish_english_fixed/` | Corrected Spanish → English XLSX exports |
| `english_spanish_fixed/` | Corrected inverse English → Spanish XLSX exports |
| `spanish_english/` | Original Spanish exports, retained as source material |

Use each collection's `file_to_deck.md` where present for deck order and IDs.
Card positions are one-based; CSV row 1 is the header, not a card. Do not reorder
cards or use alphabetical filenames as a substitute for the deck mapping.

## Where the previous work ended

- **Latest English/Russian changes:** [sentence repair, September 22](sentence_repair_20260922/README.md).
  All 744 repaired cards and replacement English recordings were verified;
  current CSVs match the saved post-sync snapshots. Start here for continuation.
- **Vocabulary policy and sense decisions:** [September 22 audit](vocabulary_audit_20260922/REPORT.md),
  `vocabulary_audit_20260922/meaning/sense_reviews.json`, and the repair's
  `new_sense_reviews.json`. The older audit describes the **pre-repair** state;
  the final clean audit is in `sentence_repair_20260922/qa_live/`.
- **Spanish text and audio:** [September 12 workspace](spanish_audio_20260912/README.md).
- **Earlier bilingual reviews:** `repair_20260907/`, `recheck_20260908/`,
  `english_russian_recheck_20260908/`, `english_russian_final_20260908/`,
  and `russian_english_pass3_20260908/`.
- **Original audio generation and experiments:** `cartesia_*`, `audio_test_20260908/`.
  Test scripts may refer to deleted test decks; they are historical evidence,
  not a recommendation to recreate those decks.

The original task **Find strict and forbidden positions** led into the September
22 work. Its durable continuation context is recorded in the files above.
“strict” is English → Russian #1,674; “forbidden” is #6,169. The repaired Russian →
English #2,140 example is “Follow the law strictly.”

## Running scripts

Use Python 3.10 or newer. The companion `brainscape` API client is maintained
separately and is **not included in this repository**. Reading and editing the
deck files needs no client; the Python audit and synchronization scripts need it.
In the existing local workspace it is available at `../api-client/`.

From this repository's root:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
# Requires the separately maintained client to be present at this path:
python -m pip install -e '../api-client[xlsx]'
python -m nltk.downloader wordnet

python run.py sentence_repair_20260922/validate.py --live
python run.py vocabulary_audit_20260922/meaning/test_regressions.py
```

`--live` here validates saved post-sync snapshots; it makes no network requests.
On a new computer, copy the companion client alongside this checkout, or install
it into the same environment. `run.py` supports both a sibling `api-client/`
directory and an installed `brainscape` package.

For network operations, copy `.env.example` to `.env`, fill in the credentials,
and set `BRAINSCAPE_ENV_FILE` to its absolute path. Explicit environment variables
take precedence. The existing local workspace already uses its parent `.env`;
there is no need to copy or replace it. Offline audits need no credentials.
Speech generation also requires `ffmpeg` and `ffprobe` on `PATH`.

For historical commands that assume the old project root, use this repository
as the working directory (`cards/` in the existing local workspace). `run.py` handles that automatically and forwards arguments.
It does not turn a writing script into a dry run.

The September 22 workflow is `stage.py` → `validate.py` → `generate_audio.py` →
`sync.py` (preflight) → `sync.py --apply`. These are the **completed run's** scripts
and frozen plan. For a new improvement batch, create a new dated workspace and
capture fresh baselines; adapt the scripts and their batch-specific counts.
Do not overwrite the completed run or regenerate its plan casually. Never replay
older syncs against newer cards without fresh conflict checks.

Preserve headwords, card IDs, deck membership, ordering, and the unaffected audio
side. Review vocabulary by meaning and by the English → Russian learning timeline
for both directions. Russian translations are unrestricted. Keep the approved
exemptions and exact-form scheduling rules in the audit; do not replace them with
a generic list of common English words. Review naturalness and translation quality
in addition to passing the automated checks.

## Audio and backups

All existing recordings remain in their original workspace-relative locations.
Git ignores audio binaries to avoid putting the generated cache in ordinary Git
history; JSON manifests, content hashes, receipts, and verified cloud URLs remain
versionable. The latest repair resolves historical absolute audio paths at runtime
without rewriting its hashed manifest or verification record.

A Git clone includes the decks and review evidence. Running offline vocabulary
checks also requires the separate client and dependencies described above.
The clone **does not include recordings or credentials**. For full continuity,
back up the audio separately before moving or deleting this checkout. From the
repository root, this creates a portable archive of every retained recording:

```sh
python - <<'PY'
from pathlib import Path
import tarfile
with tarfile.open('cards-audio.tar.gz', 'w:gz') as archive:
    for path in Path('.').rglob('*'):
        if path.suffix.lower() in {'.mp3', '.wav', '.aiff', '.m4a'}:
            archive.add(path, arcname=str(path))
PY
```

Store that ignored archive securely outside the checkout, then extract it at the
root of a fresh clone. Transfer `.env` separately through a secure channel. Audio
can often be downloaded from the snapshot URLs or regenerated from manifests,
but URLs can expire and regeneration costs money and may produce different bytes.
The archive is the reliable way to preserve exact recordings and resume without
regenerating them.

`spanish_audio_20260912/sync_xlsx.mjs` is a historical spreadsheet-rendering helper
that uses the Codex `@oai/artifact-tool` runtime. Normal Python CSV/XLSX reading,
audits, and API synchronization do not require that runtime.

## Migration notes

Everything formerly under the project root, except the API package and local
configuration, now lives here with the same relative layout. This directory is
the root of the standalone `SokolskyNikita/brainscape-language-cards` repository. Use `cards/` in place
of the old root in previous task commands. Import `brainscape` from the installed
`api-client/` package or use the runner; there is no duplicate client inside cards.
Only OS metadata, bytecode caches, and disposable console logs were deleted.
Drafts, review logs, reports, test recordings, and rollback data were retained.
Historical JSON evidence may contain the old local absolute paths; these are
provenance, not credentials. Runtime consumers that need those paths resolve them
against this checkout.

## Repository scope

Decks, review scripts, snapshots, manifests, and receipts are versioned. Generated
audio, local dependencies, and credentials are excluded. The API client remains
separate and unpublished. No license has been assigned to the card content.
