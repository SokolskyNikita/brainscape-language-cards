# File to deck map

Pack: **Spanish→English, 8000 Most Common Words** (`21303832`).

Yes: this folder has one spreadsheet per 500-word band from 1 through 8000 (16 files). It does not include the extra native-speaker decks (`1-500 [all decks now native-speaker refined]`, `501-1000`). `Types of changes made.docx` is notes, not a deck.

Local xlsx files were rewritten from the live decks after the cascade to 500 cards per band. Faces are the canonical markdown the API stores (blank line before `## Footnote`), so `cards_from_path` / `sync_deck_from_path` can write them back after edits.

Filename ids are the Brainscape `deckId`s.

| file | live deck | deck id | first 5 (file = live) | cards |
|---|---|---|---|---|
| `deck_15350594.xlsx` | 1→500 | 15350594 | que, de, no, a, el | 500 |
| `deck_15350614.xlsx` | 500→1000 | 15350614 | equivocado, público, cerveza, cocina, temprano | 500 |
| `deck_15350618.xlsx` | 1000→1500 | 15350618 | responder, construir, disco, oíste, entrenador | 500 |
| `deck_15350621.xlsx` | 1500→2000 | 15350621 | echado, bicicleta, utilizar, producto, mago | 500 |
| `deck_15350624.xlsx` | 2000→2500 | 15350624 | terminaste, presupuesto, exposición, quisiste, vencer | 500 |
| `deck_15350628.csv.xlsx` | 2500→3000 | 15350628 | gripe, pacto, mátame, sexto, enojar | 500 |
| `deck_15350630.xlsx` | 3000→3500 | 15350630 | suministro, cooperar, latín, establecido, viví | 500 |
| `deck_15350631.xlsx` | 3500→4000 | 15350631 | morder, cebo, matarás, querés, amablemente | 500 |
| `deck_15350634.xlsx` | 4000→4500 | 15350634 | eje, convencí, analista, labio, tendido | 500 |
| `deck_15350639.xlsx` | 4500→5000 | 15350639 | atacante, grité, dispararte, bah, poseído | 500 |
| `deck_15350644.xlsx` | 5000→5500 | 15350644 | desviar, despliegue, enfermar, modificar, provisional | 500 |
| `deck_15350645.xlsx` | 5500→6000 | 15350645 | enamoraste, avisarte, insegura, detenidamente, biografía | 500 |
| `deck_15350647.xlsx` | 6000→6500 | 15350647 | provee, turbulencia, arreglarte, respetuosamente, hechicera | 500 |
| `deck_15350649.xlsx` | 6500→7000 | 15350649 | definido, rotura, presagio, asistido, desviación | 500 |
| `deck_15350652.xlsx` | 7000→7500 | 15350652 | elaborar, hornear, autenticidad, convenio, avergonzar | 500 |
| `deck_15350654.xlsx` | 7500→8000 | 15350654 | arrugado, improvisado, imprevisto, latente, pasivo | 500 |

Totals: **8000** cards across **16** decks (16×500). First 15 bands were filled by cascading leftover cards forward. `7500→8000` was finished with 21 cards from `deck_bonus.xlsx` (imperial … institución) plus the first 32 of `deck_bonus_2.xlsx` (rescatar … establo). Do not add those files again.

`deck_bonus_2.xlsx` still has 18 unused lemmas after `establo` (`alrededores` … `bóveda`).
