# Cartesia Russian → English test — 2026-09-08

Created at the user's request. **KEEP this separate deck for manual validation.**

- Class: Russian to English — Cartesia TEST 2026-09-08 (24125405)
- Deck: 20 English answers — Daniel neutral — KEEP (22995414)
- Dashboard: https://www.brainscape.com/l/dashboard/24125405
- 20 copied cards selected from Russian→English source deck 15260182, class 21919521.
- Original source decks/cards are read-only throughout this workflow.
- Model: Cartesia Sonic 3.6; API version 2026-08-14.
- Voice: Daniel, native General American; locale en-US.
- Transcript: English word/phrase, period, <break time="500ms"/>, original full English example sentence.
- No Russian audio. No spoken formatting labels. Each entire clip is attached to the answer only.
- The natural punctuation pause can make the total audible gap longer than 500 ms.
- Cartesia output: 44.1 kHz mono PCM WAV, converted to 128 kbps MP3.
- Credentials: CARTESIA_API_KEY in repository-root `.env`, mode 600, ignored by Git. No key in these scripts/manifests.

20 generated MP3s all passed ffprobe and each had a detectable silence interval
of at least 250 ms. Clips are roughly 2–3 seconds long. manifest.json preserves
source card IDs, question/answer text, transcripts, model and voice settings.

upload.py resumes using state.json and creates only this isolated class/deck.
It polls attachment completion, checks there is no question-side audio, compares
all remote text with source text, and fetches each uploaded file to verify its
bytes match the local MP3. Completion is recorded in state.json under verified.
The initial source.json is a read-only 100-card snapshot; only the 20 entries
in manifest.json are copied into the new test deck.

Scripts never delete cards, decks, or classes. Brainscape may ignore private=True
for this account; actual privacy is recorded in state.json after verification.

Speech text totals 444 characters before punctuation/break markup. Exactly
20 successful Cartesia generations were made; no rerolls were needed.

## Daniel replacement

At the user's request, the same 20 test cards are being updated to Daniel
(47c38ca4-5f35-497b-b1a3-415245fb35e1), General American. Current manifest and
audio files contain Daniel; the previous Skylar files are archived in skylar/.
replace_daniel.py replaces only answer attachments and verifies remote bytes
against the new MP3s before recording danielVerified=20 in state.json.
All 20 new clips passed duration and detectable-pause checks.

## Neutral delivery revision

Requested neutral Daniel at speed 0.9 on all 20 cards. No custom IPA, phonetic
respellings, or pronunciation dictionaries. Original word and sentence transcripts
are unchanged. Default Daniel files are archived in daniel_default/. Current
manifest/audio use generation_config={emotion: neutral, speed: 0.9}. Completion
is recorded as danielNeutralVerified=20 in state.json after remote byte checks.
