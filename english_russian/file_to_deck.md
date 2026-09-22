# File to deck map

Pack: **English->Russian, 10000 most common words** (`21917816`).

Live download as Brainscape Question/Answer CSVs. One file per 500-word band. Faces are the canonical markdown the API stores (blank line before `## Footnote`), so `cards_from_path` / `sync_deck_from_path` can write them back after edits.

Question face is the English gloss + English example. Answer face is the Russian lemma + Russian example (`# Translate:` stays on the question). Filename ids are the Brainscape `deckId`s.

Re-insert after edits:

```python
from brainscape import BrainscapeClient, answer_lemma_from_card, sync_deck_from_path

client = BrainscapeClient.discover()
sync_deck_from_path(client, 21917816, DECK_ID, path, key=answer_lemma_from_card)
```

Pair by the Russian answer, not the English gloss.

| file | live deck | deck id | first 5 (English gloss) | csv cards |
|---|---|---|---|---|
| `deck_15260246.csv` | 1->500 | 15260246 | and · in · no · on · I | 500 |
| `deck_15260248.csv` | 500->1000 | 15260248 | to have to · knowledge · enter · to offer · to begin | 500 |
| `deck_15260251.csv` | 1000->1500 | 15260251 | garden · kitchen · pocket · childhood · doubt | 500 |
| `deck_15260255.csv` | 1500->2000 | 15260255 | practical · translate · to need · directly · sexual | 500 |
| `deck_15260256.csv` | 2000->2500 | 15260256 | suspect · obligation · mountainous · protocol · recommendation | 500 |
| `deck_15260257.csv` | 2500->3000 | 15260257 | cave · red-haired · worldwide · perfect · pillow | 500 |
| `deck_15260260.csv` | 3000->3500 | 15260260 | mixture · potato · melody · tasty · sixty | 500 |
| `deck_15260263.csv` | 3500->4000 | 15260263 | safely · herd · to be mentioned · portion · sidewalk | 500 |
| `deck_15260266.csv` | 4000->4500 | 15260266 | tiny · properly · niche · condom · to proclaim | 500 |
| `deck_15260268.csv` | 4500->5000 | 15260268 | anthem · patriot · sixteen · addiction · giant | 500 |
| `deck_15260269.csv` | 5000->5500 | 15260269 | bureaucracy · uninteresting · estate · equestrian · oops | 500 |
| `deck_15260272.csv` | 5500->6000 | 15260272 | isolation · dissolve · hardware · vagina · rusty | 500 |
| `deck_15260277.csv` | 6000->6500 | 15260277 | pagan · to strain · Swede · allergy · insurmountable | 500 |
| `deck_15260280.csv` | 6500->7000 | 15260280 | interactive · savage · into the distance · tankman · sleeping | 500 |
| `deck_15260281.csv` | 7000->7500 | 15260281 | desirable · Moldovan · colonial · Mongolian · Reich | 500 |
| `deck_15260282.csv` | 7500->8000 | 15260282 | hanger · dogma · rely · circumference · hoarsely | 500 |
| `deck_15260283.csv` | 8000->8500 | 15260283 | to overcome · unperturbed · cataclysm · talk into · non-living | 500 |
| `deck_15260285.csv` | 8500->9000 | 15260285 | to bathe · marathon · wilderness · to echo · Riga | 500 |
| `deck_15260287.csv` | 9000->9500 | 15260287 | half a century · to be paid · interrogate · round-the-clock · millionth | 500 |
| `deck_22976521.csv` | 9500->10000 | 22976521 | cut, sever · repentance, penitence · healing, cure · possessed, obsessed · prisoner of war, POW | 500 |

Totals: **10000** cards across **20** decks. Each file round-tripped through `cards_from_path` + `validate_deck` (`key=answer_lemma_from_card`) with 0 problems.
