# Brainscape audio experiment — September 8, 2026

**Cleanup:** User confirmed all audio works and requested removal. Deck 22994657
was deleted and its absence verified. The empty test class 24125111 remains.
The retained-deck statements below describe the original experiment.

[Open class dashboard](https://www.brainscape.com/l/dashboard/audio-api-test-2026-09-08-24125111)

[Open deck preview](https://www.brainscape.com/flashcards/audio-compatibility-tests-keep-22994657/packs/24125111)

Created one NEW class (24125111) and one NEW deck (22994657). No existing
class/deck/card was modified or deleted. All eight test cards remain.
The API ignored private=True on create and update, so this test class is public.

## Official options

- Web: upload MP3, max 5 MB, through the audio icon; Pro feature.
- Mobile: record in-app, up to 30 seconds; Pro feature.
- One audio attachment per side, so separate question and answer clips are supported.
- Audio may accompany text and images.
- No built-in text-to-speech feature was established from the docs or API inspection.
  Externally generated speech can be uploaded as MP3 (demonstrated here).

Sources:
- https://brainscape.zendesk.com/hc/en-us/articles/115002384072-How-do-I-add-images-sounds-to-flashcards
- https://brainscape.zendesk.com/hc/en-us/articles/8521066818829-How-do-I-record-audio-in-Brainscape
- https://brainscape.zendesk.com/hc/en-us/articles/360001037411-Why-can-t-I-hear-sound-on-my-flashcard

## Retained cards and results

| Card | Experiment | Result |
|---|---|---|
| 1 | MP3 on question | Stored successfully; fetched bytes match generated MP3 |
| 2 | MP3 on answer | Stored successfully; fetched bytes match generated MP3 |
| 3 | Distinct MP3s on both sides in one request | Both stored and byte-verified |
| 4 | Text-only control | No audio fields |
| 5 | Raw ordinary PATCH with data URL | Audio ignored; omitted text cleared; label/text restored |
| 6 | HTTPS MP3 URL through attachment endpoint | HTTP 500, Unknown Error code 363; no audio |
| 7 | Markdown link to generated MP3 | Ordinary clickable link in public preview; no native audio field |
| 8 | HTML audio element | Public preview displays markup as text; no native audio field |

Native attachment route: POST /api/v2/packs/{pack}/decks/{deck}/cards/{card}/atchs.
Payload fields: qSoundUrl / aSoundUrl, each a data:audio/mpeg;base64,... string.
Returns jobId; processing is asynchronous. Repeated uploads replaced prior clips.
Discovered from the official authenticated web application's bundled source.

The profile reported isPro=false, yet native upload jobs completed. Do not infer
that all free accounts officially support this or that this private API is stable.

The web UI enforces audio/mpeg and 5,242,880 bytes. Other formats/oversize files
were not uploaded to probe server limits. The new helper rejects unsupported
extensions, empty/oversize files and missing MP3 headers.

## Generated samples and verification

Fresh macOS synthetic speech (Samantha), converted to MP3 using ffmpeg:
- question.mp3: "Audio test. Question side. What is two plus two?" — 3.521 seconds, 14,541 bytes.
- answer.mp3: "Audio test. Answer side. Two plus two is four." — 3.452 seconds, 14,332 bytes.

No pre-existing personal audio files were used. Initial sandboxed speech generation
produced empty files; these were replaced with valid generated speech before final
verification. Earlier probe_results.json describes that preliminary pass; the final
source of truth is verified_audio.json and readback.json.

All four final stored audio files returned audio/mpeg and matched the corresponding
local generated MP3 byte-for-byte. ffprobe confirmed durations; the final API
readback confirmed the expected audio matrix across all eight cards. The public
website preview confirmed the deck and negative-control rendering. The browser
was not signed in, so authenticated study playback and mobile playback remain
for manual validation. The public preview does not expose native audio controls.

To validate: open the class while signed in, study/edit the KEEP deck, and inspect
cards 1–3 for native play controls on the appropriate sides. Card 4 is silent.
Compare card 7's ordinary link and card 8's non-playing markup with native audio.

Client changes: attach_audio() plus rejection of silent audio kwargs in text writes.
Mocked routing/two-side payload validation and local invalid-input checks passed.
Live create/upload/replacement/readback and content-byte verification passed.
