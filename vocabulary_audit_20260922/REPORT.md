# English-example sequencing audit — 22 September 2026

**Final rule: use the English → Russian vocabulary timeline for both packs. Inflections may inherit an allowed base only if that exact form is never explicitly taught in the same sense.**

| Pack | Cards audited | Cards with violations | Percentage | Offending word/card pairs |
|---|---:|---:|---:|---:|
| English → Russian | 10,000 | 272 | 2.72% | 276 |
| Russian → English | 10,000 | 472 | 4.72% | 476 |

**Total: 744 cards out of 20,000 (3.72%).**

A card is counted once regardless of how many words violate the rule. Word/card pairs count distinct offending surface words once per card. Repeated occurrences are separately recorded in JSON.

## Method

- Only English examples are checked. Russian examples are excluded.
- Reference vocabulary comes only from English → Russian English targets/glosses. Both packs use this same reference. Example sentences do not add vocabulary to the allow-list.
- Deck 1 may use all English → Russian cards 1–500. Deck 2 may also use only cards 1–500; deck 3 may use 1–1000; and so on. Same-deck supporting vocabulary is forbidden after deck 1, even if its card occurs earlier within that deck.
- The current card’s exact English target and its explicitly listed alternatives are allowed.
- If an exact supporting form is taught in the same sense, its scheduled deck takes precedence: a previously learned base does not unlock it early. This also applies to inflected forms of the current target. Different homonyms do not reserve each other’s schedule.
- If an exact form is never taught in the relevant sense, it is allowed when an inflectionally related English target has been introduced in an allowed deck, or is the current card’s target. Example: `worked` is never taught, so it can follow `work`. `forbidden` is explicitly taught at #6,169 and must wait.
- Inflection matching uses NLTK WordNet forms, English pronoun/reflexive paradigms, common modal pairs, and the `an/a`, `disc/disk`, `towards/toward` variants. Derivational relatives and synonyms are not generally equated.
- Case and apostrophe/hyphen typography are normalized. A contraction or possessive never explicitly taught is checked through its expanded/base words. A scheduled contraction must wait for its own deck. Hyphenated expressions never taught are checked through their components.
- Explicit alternatives and constituent words of multiword glosses count as introduced; parenthetical explanatory labels do not. This is a lexical sequencing audit, not a full assessment of word senses or whether an idiom teaches its constituents.
- Explicit exempt forms, allowed in every deck: `an`, `because`, `can't`, `don't`, `during`, `everyone`, `isn't`, `let's`, `may`, `neither`, `not`, `please`, `shall`, `should`, `their`, `will`. Exemptions also apply to expanded contraction components, so exempting `not` removes a `didn’t` flag caused solely by `not`. No other blanket grammar exemption is applied.
- Meaning corrections use 421 reviewed example contexts across 19 ambiguous forms, with explicit compatible reference lessons and base-word evidence. See [sense review decisions](meaning/sense_reviews.json). Context changes invalidate the reviewed correction instead of silently reusing it. This is a reviewed disambiguation layer, not general automatic word-sense understanding; other ambiguous cases remain conservatively flagged.
- Same lexical meaning in active/passive forms still counts as taught: bought in to be bought remains reserved. Reading as an activity and reading a book are not treated as unrelated homonyms. No blanket inflection exemption was added.
- See [changes from the previous audit](meaning/COMPARISON.md), [regression checks](meaning/test_regressions.py), and the [proposed update inventory](meaning/update_plan.json). No card text or audio has been changed.

## Your mom’s example

Russian → English **#2,140**, deck 2000→2500, card 140: **strictly** — “It’s strictly forbidden.”

**forbidden** is introduced at English → Russian **#6,169**, deck 6000→6500. Only English → Russian cards 1–2000 are available as supporting vocabulary on this card. **This is a violation.** The exact form becomes available for supporting examples from the 6500→7000 deck onward.

## Most frequent offending forms

| Form | English → Russian cards | Russian → English cards |
|---|---:|---:|
| bought | 72 | 19 |
| home | 0 | 29 |
| eyes | 15 | 6 |
| need | 0 | 21 |
| felt | 17 | 3 |
| opened | 12 | 6 |
| lost | 12 | 5 |
| ground | 0 | 17 |
| just | 0 | 17 |
| pure | 0 | 15 |
| found | 10 | 2 |
| things | 4 | 8 |
| working | 2 | 9 |
| decision | 0 | 11 |
| asked | 5 | 5 |
| lot | 0 | 10 |
| coming | 2 | 7 |
| accepted | 7 | 1 |
| checked | 5 | 2 |
| sleeping | 0 | 7 |

## Per-deck counts

| Card band | English → Russian | Russian → English |
|---|---:|---:|
| 1–500 | 18 | 52 |
| 501–1,000 | 18 | 42 |
| 1,001–1,500 | 22 | 44 |
| 1,501–2,000 | 18 | 37 |
| 2,001–2,500 | 19 | 22 |
| 2,501–3,000 | 25 | 32 |
| 3,001–3,500 | 25 | 23 |
| 3,501–4,000 | 19 | 12 |
| 4,001–4,500 | 11 | 22 |
| 4,501–5,000 | 8 | 25 |
| 5,001–5,500 | 13 | 28 |
| 5,501–6,000 | 21 | 15 |
| 6,001–6,500 | 15 | 18 |
| 6,501–7,000 | 11 | 21 |
| 7,001–7,500 | 9 | 14 |
| 7,501–8,000 | 5 | 15 |
| 8,001–8,500 | 8 | 10 |
| 8,501–9,000 | 4 | 18 |
| 9,001–9,500 | 2 | 11 |
| 9,501–10,000 | 1 | 11 |

## Files and verification

40/40 decks were audited from saved live snapshots. See [live/local comparison](manifest.json) and [source fingerprints](final_source_manifest.json). No card was changed.

- [All English → Russian flagged cards](english_russian_findings.md)
- [All Russian → English flagged cards](russian_english_findings.md)
- [Full structured findings](final_findings.json)
- [Summary counts](final_summary.json)
- [English reference inventory](final_english_inventory.json)

Reproduce with `python3 vocabulary_audit_20260922/conditional_audit.py` from the project directory. Files prefixed `exact_` and earlier exploratory outputs reflect superseded rules; the final result is this report and `final_*.json`.
