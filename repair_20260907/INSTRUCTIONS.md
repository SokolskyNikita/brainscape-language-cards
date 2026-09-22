# Full-deck language repair

User authorizes fixing ALL cards, all translation and example problems, in both directions, with cheaper parallel sub-agents. You own only the decks assigned in your task. Do not spawn more agents. Work independently; no live Brainscape calls. Do not edit source CSVs or other agents' files; stage through helper.save.

Review all 500 cards in EACH assigned deck, not just the first 25. Read them in 100-card batches with `python3 repair_20260907/helper.py PACK DECK START END`. Read the pack's `_fixer_guide.md` for linguistic details, but this task supersedes its old chunk-only scope and current-deck vocabulary allowance. User's current rule: supporting content words must be from PRIOR decks; only first 1->500 may use its whole deck. Target word itself is always allowed. Common function words are fine. Prior inventories: `repair_20260907/vocab/PACK/DECK.txt`. Use rg to confirm supporting words. Do not consult or invert the opposite pack.

Fix incorrect or misleading translations, nonmatching senses, false friends, grammar, awkward collocations/calques, semantic mismatch between examples, overly complicated/untaught vocabulary, and examples omitting the target on either side. Both examples must naturally mean the same thing and use their own target (ordinary inflection allowed). Use the actual verb aspect listed rather than a partner wherever practical. Choose short, concrete, natural examples (usually 3–8 words). Natural brief phrases are acceptable but do not replace everything with vacuous “This is X” or “I know X”. Preserve good existing cards. One clear sense is enough: remove wrong extra glosses; ensure examples use at least the selected valid gloss.

RU->EN: preserve Russian question lemma exactly, including genuine words that may look like typos (приведение is bringing/reduction, NOT ghost). Correct English gloss and both examples as needed.
EN->RU: preserve valid English headwords; correct the Russian translation. English headword corrections are permitted for real errors (e.g. combat commander -> battalion commander; International song -> Internationale), malformed or highly unnatural headwords, or faulty extra synonyms. Don't gratuitously replace English with a different concept.

Read `audit_first25/review.json` filtered only to your pack and assigned deck for known findings. These are suggestions, not unquestionable truth: use your judgment. For example колеблись is a valid imperative but “Не колеблись спросить” is unnatural; suite->свита is a valid sense.

Use `repair_20260907/helper.py`:
```
import sys
sys.path.insert(0,'repair_20260907')
from helper import read,save
save('russian_english','15260182', {
  16: ('к','to, towards','Я иду к дому.','I am walking towards the house.'),
},reviewed=500,notes='Reviewed all rows; ...')
```
Patch tuple is (question lemma, answer lemma, question example, answer example), regardless of direction. Unlisted rows remain unchanged. Store your patch script under `repair_20260907/scripts/NAME.py` (create directory). `save` always starts from originals, so rerunning a script must include ALL your patches. Stage one complete CSV and change log per assigned deck. Avoid a giant generic script that changes without linguistic review. Check your staged output and do not introduce duplicate complete Q/A pairs or new malformed markup.

Before finishing, ensure you have actually read/reviewed all 500 rows of every assigned deck, executed your patches, and addressed known first-25 findings where warranted. Return deck IDs, reviewed/changed counts, and any unresolved semantic problem. Do not declare unresolved problems merely because writing fixes takes effort.
