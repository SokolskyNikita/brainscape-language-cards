# Current course audio

This directory describes and packages the audio that is attached to the
current Brainscape courses represented by [`../courses.json`](../courses.json).
It is deliberately a current mirror: temporary decks, experiments, and
recordings that are not attached to one of those cards are outside its scope.

As of the verified snapshot in `courses.json`, the four courses contain 36,000
cards. The two English/Russian courses have 20,000 attached English recordings
in total:

| Course | Attached sides | Published archive |
| --- | ---: | --- |
| English → Russian | 10,000 question sides | [`english-russian-audio.zip`](https://github.com/SokolskyNikita/brainscape-language-cards/releases/download/live-audio-2026-09-23/english-russian-audio.zip) |
| Russian → English | 10,000 answer sides | [`russian-english-audio.zip`](https://github.com/SokolskyNikita/brainscape-language-cards/releases/download/live-audio-2026-09-23/russian-english-audio.zip) |
| English → Spanish | 0 | No attached audio found |
| Spanish → English | 0 | No attached audio found |

The Spanish courses are still represented by their live card snapshots. No
Spanish production MP3s were present locally to publish.

## Catalog and checksums

[`current.json`](current.json) is the compact audio catalog. Each entry records
the course, deck and card IDs, side, attached live URL, side-specific archive
path, SHA-256, and byte count. Its `missing` and `changed_urls` arrays record
any attached URL that could not be matched or changed since the previous
catalog; both must be empty before publishing. [`files.sha256`](files.sha256) repeats the per-file hashes
using the paths inside the release archives.

Archive metadata and release URLs are in [`archives.json`](archives.json).
`SHA256SUMS` is included with the release assets and verifies each archive.

The local cache is ignored by Git because it contains the actual MP3 bytes:

```text
audio/current/english_russian/audio/CARD_ID-question.mp3
audio/current/russian_english/audio/CARD_ID-answer.mp3
```

The suffix keeps both sides unambiguous if a future course receives audio on
both sides. The cache is the durable local source for future packaging, so the
card repository can remove old generation directories without losing the
published recordings.

## Download and restore

From the cards repository root:

```sh
gh release download live-audio-2026-09-23 \
  --repo SokolskyNikita/brainscape-language-cards \
  --pattern '*.zip' --pattern SHA256SUMS --dir /tmp/brainscape-audio-download
(cd /tmp/brainscape-audio-download && shasum -a 256 -c SHA256SUMS)
mkdir -p audio/current
for archive in /tmp/brainscape-audio-download/*.zip; do
  unzip -n "$archive" -d audio/current
done
(cd audio/current && shasum -a 256 -c ../files.sha256)
```

You can also download the ZIP files from the links above and extract both into
`audio/current/`. No Brainscape login or API client is needed to download or play
the recordings. `unzip -n` preserves existing local files.

## Rebuild the current package

From the standalone cards repository, after restoring the ignored `audio/current`
cache:

```sh
python audio/package_current.py \
  --courses courses.json \
  --output /tmp/brainscape-current-audio-release
```

The output directory must stay outside the repository. The script reads only
the current course metadata, the four course snapshot directories, and the
local current audio cache. It makes no network requests, does not synthesize
speech, and never writes to Brainscape. It checks that every attached URL names
the expected card and side, and it withholds changed URLs or missing local
files from the archives for review.

The packager checks each cached recording against the previously verified URL
and SHA-256. Missing, changed, or corrupted audio stops the run before catalog
or archive files are overwritten. For a new attachment, download and verify its
bytes before updating the cache/catalog and publishing a new release.

On Linux, `sha256sum -c` can replace `shasum -a 256 -c`.
