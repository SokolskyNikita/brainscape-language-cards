# Card improvement maintenance

This directory contains the small, reusable part of the September 22 card
improvement workflow. It is deliberately independent of dated workspaces and
the Brainscape API. The current mirror is described by `../courses.json`; the
audit reads the saved per-deck JSON snapshots first and falls back to the CSV
exports in the same deck folder.

The durable rule is the English → Russian vocabulary timeline for both English
example packs. The first 500 reference headwords are allowed in both the first
and second 500-card bands; each later band may use the reference headwords from
the preceding bands, never its own band or a later band. An inflection may
inherit an allowed base only when that exact form is not taught in the same
sense. The current target and explicit alternatives are allowed. The approved
grammar forms and reviewed sense contexts are kept in `policy.json` and
`sense_reviews.json`.

Run the read-only audit from the cards repository root:

```sh
python maintenance/audit.py --output /tmp/brainscape-card-audit
```

The output directory receives `summary.json`, `findings.json`, `decks.json`,
`english_inventory.json`, `source_manifest.json`, and `semantic_decisions.json`.
It is safe to delete the output after review. The audit never contacts
Brainscape and never edits a deck. It fails if the reference headwords no
longer match the reviewed sense decisions, so a future card batch must refresh
the affected reviews instead of silently reusing them. The command exits with
status 1 when it finds vocabulary flags, which makes it usable in a local check
or CI job.

The default JSON-first mode audits the saved live snapshots. When a proposed
CSV has been edited while its baseline JSON remains unchanged, use
`python maintenance/audit.py --source csv --output /tmp/brainscape-card-audit`.
This makes the draft visible to the audit while retaining JSON as the verified
baseline for normal checks.

Run the small business-rule test suite with:

```sh
python -m unittest maintenance.test_audit
```

`courses.json` supplies each course `slug`, `packId`, and ordered `decks`. Each
deck entry contains `deckId`, its live `position`, `card_count`, and relative
`csv` and `json` paths. Live positions may have gaps when an unrelated live
deck is excluded from this mirror; the mirror order supplies the 500-card band
sequence. The JSON snapshot is the preferred source because it retains card
IDs and the `qMd*`/`aMd*` fields needed for exact future edits. The audit only
uses `english_russian` and `russian_english`; the mirror validator handles
structural checks for the Spanish packs.

When starting a new improvement batch:

1. Refresh the four live snapshots and verify `courses.json` before editing.
2. Preserve `cardId`, deck membership, row order, target headwords, and the
   unaffected audio side.
3. Re-run this audit against the proposed exports and review findings by
   meaning, sentence naturalness, and translation quality.
4. Record replacements and audio manifests in the batch workspace, then run a
   fresh conflict check before any cloud write.

The policy intentionally does not contain a generic English stop-word list or
blanket grammar exemption. Russian translations are unrestricted. Context
changes invalidate a sense review and must be reviewed again.
