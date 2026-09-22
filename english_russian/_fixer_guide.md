# English→Russian local rewrite

Work only in `english_russian/`. Do not open, copy, invert, or consult any other pack.

This is an English→Russian frequency pack. The learner sees an English gloss and must produce the Russian.

## Card shape

Question (English):

```
# Translate:

{english gloss}

## Footnote

{english example}
```

Answer (Russian):

```
{russian lemma}

## Footnote

{russian example}
```

Rules:

- `# Translate:` stays on the question only. The answer has no heading.
- Blank line before `## Footnote` (Brainscape canonical form).
- One short example sentence per face. Same meaning on both sides.
- The example must use the target word (inflection is fine: переведите counts as перевести).
- Do not invent a second sense, a clarifier paragraph, or extra footnotes.

## What to fix

Review every card. Leave a card unchanged only if the pairing and both examples are already good.

### 1. Bad translations

The English gloss is the frequency-list headword. The Russian lemma must be a real translation of that English word in the sense the examples teach.

- If the pair is a valid sense, keep both lemmas and fix the examples to teach that sense.
- If the pair is wrong, change the Russian lemma to the correct translation of the English. Do not invent a new English headword.
- Typos in the Russian lemma must be corrected (`приведение` for ghost → `привидение`).
- False friends: shortly ≠ коротко (soon vs briefly); musical (show) ≠ музыкальный; formally dressed ≠ формально одет; methodical ≠ методический; oops ≠ оп.
- Wrong verbs: insist ≠ обстоять (настаивать); proclaim ≠ гласить (заявить / провозгласить); talk into ≠ наговорить (уговорить); get used to ≠ освоиться (привыкнуть); shrink (fabric) ≠ сжаться (сесть); flash (a light) ≠ засветиться (мигать / вспыхнуть); justify ≠ оправдываться (оправдать).
- Part-of-speech must match the gloss: if English is a noun (Riga, Black Sea, gambler, steering-as-verb), the Russian lemma and the examples must be the same part of speech. Prefer fixing examples to match a valid lemma; change the lemma when the lemma itself is the wrong word.
- `no` as a card is нет, not не. `not` would be не. If the gloss is `no`, use нет.
- Conjunction `that` is что. Demonstrative `that` is то / тот. Match the lemma you keep.
- `like` as “looks like” is похож на, not вроде.
- Generator / refusal text (`I'm sorry, but I can't fulfill this request.`) is not a card. Write a real pair.

### 2. Bad or incorrect sample sentences

- English and Russian examples must mean the same thing (dusk ≠ dawn).
- Correct Russian grammar: gender, case, agreement (`поздний ответ`, `свою обувь`, `Ей исполнилось шестьдесят`, `странной энергией`).
- Imperative after “please”: заприте / сотрите, not the bare infinitive.
- Aspect: не начинай + perfective (`начала пробормотать`, `начал сожрать`). Use начал + imperfective, or drop начал.
- No tautology (`добровольно добровольно`, `прощальное прощание`, `справедливо выполнена`).
- No empty sentences (“the key corresponds perfectly” — to what?).
- No English left on the Russian face.
- Keep examples short and concrete. One clause is enough.

### 3. Leftover vocabulary (graded)

Every content word in both examples must already have been taught:

- Deck `1->500`: only lemmas from this same deck (plus tiny function words: a, the, is, be, I, you, he, she, it, we, they, my, and, or, in, on, at, to, of, for, with, from, not).
- Later decks: lemmas from prior decks plus the current deck.

Inflection is allowed (`книгу` if `книга` is known). Proper names that are the card itself (Volga, Riga) are allowed. Do not use later-band words (photosynthesis on a “synthesis” card, magician/rabbit on an early “disappear” card, aspire/writer on “to be”).

If you cannot make a grammatical sentence from allowed words, use the simplest sentence that still uses the target word. Prefer “I know that” over “fascinating distant lands”.

### 4. Example must use the target word

If the lemma is вестник, the Russian sentence must use вестник (or an inflection), not почтальон. If the English gloss is messenger, the English sentence must use messenger, not bearer.

Same for compounds: a `synthesis` card may not switch to photosynthesis; a `construction` card may not switch to строительная площадка unless строительство itself appears.

## What not to do

- Do not reorder cards.
- Do not drop or add cards. Output exactly the same number, same sequence.
- Do not change an English gloss unless it is garbage (refusal text, duplicate word `evacuate, evacuate` — then keep one copy).
- Do not write essays, notes, or extra columns.
- Do not look at `russian_english/` or any other folder.

## Output

Write a CSV with header `Question,Answer` and the same canonical markdown faces. UTF-8, `\n` line endings, standard csv quoting.
