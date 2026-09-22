# File to deck map

Pack: **Russian->English, 10000 most common words** (`21919521`).

Live download as Brainscape Question/Answer CSVs. One file per 500-word band. Faces are the canonical markdown the API stores (blank line before `## Footnote`), so `cards_from_path` / `sync_deck_from_path` can write them back after edits.

Question face is the Russian lemma + Russian example. Answer face is the English gloss + English example (`# Translate:` stays on the question). Filename ids are the Brainscape `deckId`s.

Re-insert after edits:

```python
from brainscape import BrainscapeClient, sync_deck_from_path

client = BrainscapeClient.discover()
sync_deck_from_path(client, 21919521, DECK_ID, path)
```

Pair by the Russian question (`lemma_from_card`).

| file | live deck | deck id | first 5 (Russian lemma) | csv cards |
|---|---|---|---|---|
| `deck_15260182.csv` | 1->500 | 15260182 | и · в · не · на · я | 500 |
| `deck_15260185.csv` | 500->1000 | 15260185 | наверное · период · кстати · пара · квартира | 500 |
| `deck_15260188.csv` | 1000->1500 | 15260188 | произведение · построить · деревня · направить · составить | 500 |
| `deck_15260190.csv` | 1500->2000 | 15260190 | скажем · поступать · нижний · южный · газ | 500 |
| `deck_15260191.csv` | 2000->2500 | 15260191 | резкий · сверху · спрос · различие · учение | 500 |
| `deck_15260192.csv` | 2500->3000 | 15260192 | дар · рекомендация · лекарство · максимальный · объявление | 500 |
| `deck_15260194.csv` | 3000->3500 | 15260194 | ярко · революционный · течь · молодец · изменять | 500 |
| `deck_15260196.csv` | 3500->4000 | 15260196 | применить · бумажка · мисс · бабка · нить | 500 |
| `deck_15260198.csv` | 4000->4500 | 15260198 | давить · усиление · неверный · группировка · люк | 500 |
| `deck_15260200.csv` | 4500->5000 | 15260200 | овощ · противостоять · сновидение · виновный · фокус | 500 |
| `deck_15260204.csv` | 5000->5500 | 15260204 | заклинание · аллах · ловушка · взятка · оказание | 500 |
| `deck_15260207.csv` | 5500->6000 | 15260207 | дизайнер · бег · дырка · начинающий · причём | 500 |
| `deck_15260210.csv` | 6000->6500 | 15260210 | прижаться · ансамбль · крохотный · предательство · прохладный | 500 |
| `deck_15260213.csv` | 6500->7000 | 15260213 | литератор · поглощать · литься · пресловутый · неподвижно | 500 |
| `deck_15260214.csv` | 7000->7500 | 15260214 | марксизм · въезд · надлежать · аварийный · чек | 500 |
| `deck_15260215.csv` | 7500->8000 | 15260215 | знатный · реветь · шрам · изысканный · истечение | 500 |
| `deck_15260217.csv` | 8000->8500 | 15260217 | донесение · буквальный · инопланетянин · зрелость · унылый | 500 |
| `deck_15260218.csv` | 8500->9000 | 15260218 | непреодолимый · канадский · кошачий · наркомания · сладость | 500 |
| `deck_15260221.csv` | 9000->9500 | 15260221 | строфа · опека · углубление · трус · ронять | 500 |
| `deck_15260224.csv` | 9500->10000 | 15260224 | перерезать · покаяние · исцеление · одержимый · военнопленный | 500 |

Totals: **10000** cards across **20** decks. Each file round-tripped through `cards_from_path` + `validate_deck` with 0 problems.
