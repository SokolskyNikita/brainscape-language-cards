# Russian→English slice fixer

Work only in `russian_english/`. Do not open, copy, invert, or consult any other pack.

Question face: Russian lemma + Russian example.  
Answer face: English gloss + English example.  
`# Translate:` stays on the question.

## Hard rules

- Never change the Russian lemma (`qMdBody`), card order, or card count.
- The English gloss (`aMdBody`) may change if the translation is wrong.
- The Russian example must use **this** lemma (an inflected form is fine: `нести` → `Неси`).
- The English example must use **this** gloss (an inflected form is fine: `carry` → `carried`). Do not swap in a synonym (`carry` → `bring`, `и` → `or`).
- Every lemma in the slice must be in `fixes`. Extra keys are refused.
- Do not call Brainscape. Do not upload.
- Write only the assigned 100-card chunk under `_chunks/fixed/`.

## What to fix

1. Wrong gloss (ghost ≠ `приведение`; `ан` ≠ bathhouse; `сосна` ≠ fir).
2. Bad or ungrammatical examples (`Она исполнилось`, `проследю`, `странным энергией`, `You're well done`).
3. Example that teaches a different word (`ближний` + `возле`, `коли` + `если`, `грядущий` + `предстоящее`, `рыбный` + `рыбу`, `включиться` + `включите свет`).
4. Leftover vocab: content words in the examples must already be lemmas in prior decks, or in **this** deck. Function words (`и`, `в`, `не`, `the`, `is`) are fine. The allow lists are `_vocab/allow_ru_*.txt` and `_vocab/allow_en_*.txt`.

## Style

- Spoken, short, one clause. Prefer 3–8 words.
- One clear sense. If the lemma is a particle or function word, pick the everyday sense (`то` = that one, not `что`; `уж` = the particle; `б` = would).
- Government must be real Russian: `звонить` + dative, `о` + prepositional (`о истории`), no `спросить вопрос`, no `менее много`, no `иметь тебя`.
- No model-refusal text. No `thou` / `annum` / `hamlet`. No English calques.
- Aspect: `решил` + perfective (`выбросить`, not `выбрасывать`). Age: `Ей исполнилось`, never `Она исполнилось`.
- Gender and agreement: `начинающая`, `странной энергией`, `своей руке`.

## How to write

Dump the slice, then write a script that calls `rewrite_chunk` with every lemma:

```python
from pathlib import Path
from russian_english._chunk_io import rewrite_chunk

rewrite_chunk(
    Path("russian_english/_chunks/deck_15260182_00.csv"),
    {
        "и": ("and", "Книга и стол.", "The book and the table."),
        # ... every lemma in the slice
    },
)
```

Leave a card unchanged by passing its current gloss + examples. Still include the key.

Save the script under `_chunks/logs/_write_<deckId>_<slice>.py` and run it.

## Return

- Files touched
- `changed` / `unchanged` / `total==100`
- 8–12 before/after lines
- Any leftover problems you could not fix without changing the lemma
