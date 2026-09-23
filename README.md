# Brainscape language cards

A mirror of the numbered vocabulary decks actually uploaded to these four courses.

| Direction | Cards | Decks | Study on Brainscape | Local files |
| --- | ---: | ---: | --- | --- |
| English → Russian | 10,000 | 20 | [Open course](https://www.brainscape.com/packs/english-russian-10000-most-common-words-21917816) | [english_russian/](english_russian/) |
| Russian → English | 10,000 | 20 | [Open course](https://www.brainscape.com/packs/russian-english-10000-most-common-words-21919521) | [russian_english/](russian_english/) |
| English → Spanish | 8,000 | 16 | [Open course](https://www.brainscape.com/packs/english-spanish-8000-most-common-words-21945419) | [english_spanish/](english_spanish/) |
| Spanish → English | 8,000 | 16 | [Open course](https://www.brainscape.com/packs/spanish-english-8000-most-common-words-21303832) | [spanish_english/](spanish_english/) |

Each `deck_ID.csv` contains the uploaded question/answer text. Its matching JSON
retains card IDs, order, structured fields, and live audio URLs for future edits.
[`courses.json`](courses.json) records the exact deck list and verification time.
Temporary/test decks and unapplied work are excluded.

## Audio

[Download the audio currently attached to the mirrored cards](audio/README.md).
The public release contains actual recordings, with a card-to-file index and
checksums. Only the current recording for each attached card side is included.
Audio binaries are release assets, so a normal Git clone does not download them.

## Improving the cards

[`maintenance/`](maintenance/README.md) contains the shared vocabulary rules,
reviewed word senses, audit, and live-mirror checker. Work from the current course
files; preserve card IDs, deck order, and audio on any unchanged side. Draft work
belongs outside the published mirror until it has been uploaded and verified.

The companion `brainscape` API client is separate and remains unpublished. In the
existing local workspace it is at `../api-client/`. Python 3.10+ setup:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m nltk.downloader wordnet
```

Run the offline vocabulary audit:

```sh
python maintenance/audit.py --output /tmp/brainscape-card-audit
```

To compare this mirror with Brainscape, install the separate API client
(`python -m pip install -e ../api-client`) and run the checker (GET requests only):

```sh
python run.py maintenance/mirror.py
```

After a verified upload, `python run.py maintenance/mirror.py --refresh` replaces
local exports with fresh live data. Review local edits before refreshing. Never
run a historical batch against newer cards.

Credentials belong in `.env` or the process environment. Use `BRAINSCAPE_ENV_FILE`
to select a file explicitly; the existing workspace already uses its parent
`.env`. They are never committed.
