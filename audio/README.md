# Downloadable card audio

The actual MP3 files are public GitHub Release assets:

**[Download the September 22, 2026 audio release](https://github.com/SokolskyNikita/brainscape-language-cards/releases/tag/audio-2026-09-22)**

| Archive | Recordings | Download size | Contents |
| --- | ---: | ---: | --- |
| [English → Russian originals](https://github.com/SokolskyNikita/brainscape-language-cards/releases/download/audio-2026-09-22/english-russian-original-audio.zip) | 10,000 | 498 MiB | English question-side recordings from the September 8 rollout |
| [Russian → English originals](https://github.com/SokolskyNikita/brainscape-language-cards/releases/download/audio-2026-09-22/russian-english-original-audio.zip) | 10,000 | 532 MiB | English answer-side recordings from the September 8 rollout |
| [Repaired English examples](https://github.com/SokolskyNikita/brainscape-language-cards/releases/download/audio-2026-09-22/english-example-replacement-audio.zip) | 737 | 39 MiB | Replacement recordings used by 744 cards in the September 22 repair |

The three archives contain **20,737 production MP3 files** (about 1.04 GiB).
Seven revised transcripts share recordings. The originals remain available as
historical evidence; use the index below to select the current recording.

## Which recording belongs to a card?

[`current.json`](current.json) maps all **20,000 current English/Russian cards**
to their correct English recording as of the September 22 verified snapshot.
Each entry includes the class, deck, card ID, overall position, audio side,
headword, example, transcript, archive name, relative file path, and SHA-256.
For the 744 repaired cards it points to the replacement audio, not the old clip.

These are English recordings for both learning directions. There are no retained
production Russian-language recordings or Spanish bulk recordings to publish.
The Spanish bulk generation has not run. Small compatibility/voice experiments
remain local and are not included in this production release.

## Download and restore

Download all three ZIP files and `SHA256SUMS` from the release page, then verify
and extract them **at the root of this cards repository**. Archive paths reproduce
the exact workspace layout used by the existing generation and sync scripts.

With GitHub CLI, from the cards repository root:

```sh
gh release download audio-2026-09-22 \
  --repo SokolskyNikita/brainscape-language-cards \
  --pattern '*.zip' --pattern SHA256SUMS --dir audio/downloads
(cd audio/downloads && shasum -a 256 -c SHA256SUMS)
for archive in audio/downloads/*.zip; do unzip -n "$archive" -d .; done
shasum -a 256 -c audio/files.sha256
```

`unzip -n` preserves existing files; a checksum mismatch should be investigated
before replacing any local recording. On Linux, `sha256sum -c` can be used instead
of `shasum -a 256 -c`. No API client, Cartesia account, or Brainscape login is
needed to download or play these recordings.

A normal `git clone` or GitHub source-code ZIP does not download release assets.
Audio stays outside Git history, but the actual bytes are hosted publicly on
GitHub and can be restored without regenerating speech.

## Verification and reproduction

[`archives.json`](archives.json) records each archive's download URL, exact byte
size, file count, and SHA-256. [`files.sha256`](files.sha256) records the individual
MP3 checksums. Every recording was checked against its existing production
receipt or generation metadata before packaging; every archived payload was
checked again after packaging. The current index's transcripts match the saved
post-repair card examples.

To rebuild these archives from a checkout with the audio restored (Python 3.10+):

```sh
python audio/package.py --output /tmp/brainscape-audio-release
```

This is an offline packager for the September 22 snapshot. It never generates
speech or writes to Brainscape. For future repair batches, publish a new release
and update the catalog to the newly verified state, preserving older releases.
