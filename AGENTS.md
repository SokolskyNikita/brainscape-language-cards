# Working on the cards

- Read README.md, sentence_repair_20260922/README.md, and
  vocabulary_audit_20260922/REPORT.md before continuing improvements.
- This directory is the standalone cards Git repository. The companion client
  remains outside it at ../api-client/ in the existing local workspace. Do not
  vendor or publish the client as part of card changes.
- Run scripts via python run.py WORKSPACE/SCRIPT.py. This preserves historical
  imports and working-directory assumptions. Install the separate client and
  requirements.txt dependencies as described in README.md on a fresh computer.
- english_russian/ and russian_english/ contain the latest verified CSVs. Dated
  workspaces contain historical plans and snapshots. Start a new dated workspace
  for new repairs; do not overwrite the evidence of completed runs.
- Preserve card IDs, deck membership, order, target headwords, and unaffected audio.
  Keep the agreed English vocabulary timeline, exact-form scheduling rules, sense
  reviews, and approved exemptions. Russian translations are unrestricted.
- Do not discard drafts, manifests, receipts, originals, or recordings as garbage.
  Audio is ignored by Git but retained locally; preserve backups separately.
- Secrets belong in .env or process environment. Never print or commit them.
- Offline checks: python run.py sentence_repair_20260922/validate.py --live
  and python run.py vocabulary_audit_20260922/meaning/test_regressions.py.
  Here --live reads saved snapshots, not the current server.
- Some historical scripts write to Brainscape at startup or import. Inspect them
  before running and do not import arbitrary scripts to discover tests.
