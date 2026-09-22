# Full Russian → English answer audio rollout

User approved the neutral Daniel 20-card sample and requested the same for all
Russian→English cards. Authorized target: class 21919521, 20 decks, 10,000 cards.
The separate 20-card test deck remains untouched.

Settings: Cartesia Sonic 3.6, Daniel (47c38ca4-5f35-497b-b1a3-415245fb35e1),
en-US, neutral emotion, speed 0.9. No IPA or pronunciation dictionaries.
Transcript: original English answer body + period + <break time="500ms"/> +
original English answer footnote/example. Total input: 582,254 characters
including pause markup. English text is spoken; formatting headings are not.

The 20 approved neutral Daniel clips are reused when source IDs and transcripts
match. Other clips are generated once and cached as 128 kbps mono MP3 files.
All original live cards are snapshotted as before_DECKID.json before any upload.
No card text updates, deletions, reorder operations or question attachments occur.

Run from `cards/` with the environment activated: PYTHONPATH=. python3 cartesia_russian_english_20260908/run.py
The runner resumes using audio/, receipts/, and verified/. Do not run duplicate
instances. It generates and uploads one deck at a time with bounded concurrency (5 Cartesia,
24 Brainscape attachment uploads), while one verifier checks the preceding deck
with up to 8 concurrent downloads. It retries only bounded transient failures.

Each deck is verified after upload: exact IDs/counts, original question/answer
text, preserved question audio, and byte equality for every answer MP3 retrieved
from its Brainscape URL. Per-deck reports are in verified/. result.json exists
only when all 20 decks and all 10,000 cards pass. events.jsonl and run.log record
progress; progress.json contains counters for this invocation.

Both the Cartesia key and Brainscape cookie are loaded from repository-root
`.env`; no credentials are copied into the output directory.

English-only speech: 40 answer bodies contain parenthetical Russian usage notes.
Those parenthetical notes are omitted from the spoken headword only; written
card text is unchanged. english_only_changes.json records every spoken variant.
No IPA or custom pronunciation replacements are used.

Completed: all 10,000 answer recordings across all 20 decks uploaded and verified.
Every remote MP3 matched its generated file; all question/answer text and question
audio were preserved. 9,980 clips generated (581,350 input characters), 20 approved
clips reused. Provider billing may differ for retries. The separate test deck was
not changed or deleted.
