"""Build a read-only linguistic audit of the first 25 cards in each Russian pack deck."""
from pathlib import Path
import json,hashlib,re
from collections import Counter
ROOT=Path(__file__).resolve().parent.parent
from source_data import load_source
D=load_source()
# deck index 0..19 RU->EN, 20..39 EN->RU; card positions are 1-based.
RAW='''0|13|2|improve|“That's not that one” is an awkward, context-dependent rendering of “Это не то”. Use “That is not what I meant” or rebuild both faces around “то”, keeping an allowed English gloss.
0|23|1|fix|The gloss “have” describes the whole possession construction у + genitive + есть/zero, not the preposition alone. Label it “at; used in possession: у него … = he has …” so the card does not teach у as a verb.
1|16|2|fix|“Я чуть понял” is unnatural for “I understood a little”; чуть often suggests barely/almost in this environment. Use “Я чуть устал / I am a little tired”.
2|7|2|improve|Bare “Sister's already home” needs a family-name style context. “My sister is already home / Моя сестра уже дома” is a better standalone model.
2|22|2|fix|“Это одно целое” means “It is a single whole”, not simply “It's the whole”. Preserve одно in the translation: “It is one whole”.
3|11|1,2|improve|“Мне дали повышение” normally suggests a promotion; “a raise” specifically suggests increased pay. Teach “promotion” here, or explicitly say “повышение зарплаты” for a pay raise.
3|16|2|improve|“Give me the contact” is vague English without context. Specify “contact details” and the corresponding Russian, or use an example such as “Мы поддерживаем контакт / We keep in contact”.
5|1|2|fix|“У неё дар к музыке” is a poor collocation. Use “У неё музыкальный дар / She has a gift for music”, or “У неё дар / She has a gift” for simpler vocabulary.
6|9|2|improve|“A corporate holiday” suggests a company holiday rather than a company celebration. Use a clearer shared collocation such as “корпоративный сайт / corporate website”, subject to vocabulary checks.
6|18|2|fix|“He waited up to morning” is unnatural temporal English. Use gloss “right up until” and “He waited right up until morning / Он ждал вплоть до утра”.
7|6|1|fix|“Existence” is too broad as an unqualified gloss for быт. Keep “everyday life; domestic life”.
7|11|2|improve|“Планирование поездки трудно” sounds strained. “Планирование поездки — трудная работа” or a simpler shared sentence is more natural.
7|18|1,2|fix|“Fear encompassed him” is a forced literal translation. This sense of охватить is “to grip/overwhelm”: “Страх охватил его / Fear gripped him”. Update the gloss to match.
7|21|1|fix|“Meat” teaches the wrong everyday sense for плоть. Keep “flesh”; food meat is мясо.
8|1|2|fix|“The boot presses my foot” is unnatural English. Use “The boot presses against my foot”, or teach “pinch” for this sense and update the gloss.
8|2|2|improve|“We waited for the storm's intensification” is cumbersome. Use a simpler pairing such as “Усиление ветра / Intensification of the wind”, after confirming vocabulary.
8|8|1,2|fix|“Претендовать на звание” means to contend for/lay claim to a title, not necessarily win it. “She will claim the championship title” implies success. Use “She will contend for the title” and align the gloss.
8|13|2|fix|“He has a high qualification” is a Russian calque. Use “He has professional qualifications / У него профессиональная квалификация”, or “He is highly qualified” with a matching gloss/form.
8|15|1|fix|“Curd” is not a reliable standalone translation of сыр; keep “cheese”. Curd/curds require their own food sense and context.
8|24|1,2|fix|The example leaves ethnicity versus citizenship ambiguous. “Национальность” in this Russian sentence normally describes ethnicity; English “nationality” usually suggests citizenship. Use the existing “ethnicity” gloss and a matching example, or explain the distinction.
9|9|2|fix|“Residence here is expensive” is unnatural for “Проживание здесь дорого”. Use the existing “living” gloss: “Living here is expensive”.
9|22|2|improve|“Regulate the water” leaves the controlled quantity unspecified. Specify flow/temperature on both sides, or choose a simpler object.
9|23|1,2|fix|For a wheel's physical shaft, English uses “axle”, already in the gloss. If the abstract axis is intended, say “ось вращения / axis of rotation”.
10|22|2|improve|“It's quiet in this interval” is artificial without an established time interval. Use “Между ними промежуток / There is a gap between them”.
10|24|2|improve|“В окрестности тихо” is strained for “in the vicinity”; обычное “В окрестностях тихо” is the natural plural of the same lemma.
11|9|2|improve|“A long selection” can mean a long list rather than a lengthy selection process. “Подбор занял час / The selection took an hour” teaches the process clearly.
11|10|2|improve|“Церемония совершается” is an unusual general model; совершается naturally combines with обряд. Choose a concrete compatible subject and mirror it in English.
11|13|1,2|fix|“Я прослежу за этим” generally means “I will see to it/keep an eye on it”. “I'll track this” suggests tracking an object. Align both examples with the intended monitoring sense.
11|25|2|fix|“Long loading” is not idiomatic standalone English. Use “Загрузка идёт медленно / Loading is slow”.
12|25|2|improve|“Она прижимает книгу” leaves out what she presses it against. Add “к себе / to herself” or another clear complement.
13|19|2|fix|“He claimed his debt” sounds as though he is claiming a debt he owes. Use “He demanded repayment of the debt” and a matching claim/demand gloss for востребовать.
14|3|1|fix|Надлежать expresses obligation: “must; should; be required to”. “To be due” is too narrow and does not capture the verb generally. “Книгу надлежит вернуть завтра / The book must be returned tomorrow”.
14|10|2|fix|“Идеально, мы закончим завтра” is a calque of sentence-initial English “Ideally”. Use “Всё прошло идеально / Everything went perfectly”, changing the gloss to “perfectly”.
14|22|2|improve|A yacht is “moored” or simply “is” by the shore, not normally “stands”. Translate стоит idiomatically while retaining “yacht”.
15|7|2|fix|“Она рождает сына” is a poor ordinary childbirth example; рожать is usual for literal labor. Preserve рождать with a natural figurative subject, e.g. “Страх рождает ненависть / Fear gives birth to hatred”.
15|11|2|fix|“Чистка дома” is not the normal collocation for housecleaning (уборка дома). Keep чистка but choose shoes/teeth or another suitable object on both faces.
15|20|2|fix|“Чистая медь” normally means pure copper in this material-identification example. Use “This is pure copper”, not “clean copper”.
16|10|1|improve|“Tend to” loses the persistent trying/attempting nuance of норовить. “He keeps trying to argue” is a better gloss/example alignment.
16|13|2|improve|“We took a box at the theater” is less clear than “We booked a box at the theater”. Align the Russian with a booking or seating context.
16|15|2|improve|“The express goes at noon” is unnatural timetable English. Use “The express leaves at noon”.
17|6|1,2|fix|For fabric shrinking in water, Russian normally uses сесть, not сжаться. Preserve сжаться with “contract”: “Мышца сжалась / The muscle contracted”, and update the gloss.
17|19|1,2|fix|“Мнимый друг” usually means an apparent/false friend, whereas “imaginary friend” means an invented companion. Teach “supposed/false” here or choose a different context for imaginary.
18|6|2|improve|“He has a strong muscle” is an odd isolated statement. “У него сильные мускулы / He has strong muscles” uses an ordinary plural of the same target.
18|9|2|improve|“The dining table is already ready” is awkward. Use “Обеденный стол большой / The dining table is large”, or a properly set-table example.
19|2|2|improve|“Seeking repentance” is an unusual model; seeking forgiveness is more usual but would teach a different target. Use “Его покаяние искреннее / His repentance is sincere”, subject to vocabulary checks.
19|4|2|improve|“Possessed by a strange energy” is figurative and vague. A concrete “одержимый страхом / obsessed with fear” sense would teach the target more clearly, with matching gloss.
20|15|2|improve|“They come this evening” is an unnatural standalone planned-arrival sentence. Use “They are coming this evening / Они придут сегодня вечером”.
21|1|2|fix|“До поздна” is misspelled; write “допоздна”. Simpler: “Мне приходится работать / I have to work”.
21|21|2|improve|“Больший дом” is grammatical but marked in this request; ordinary Russian uses “дом побольше”. Prefer a context where больший naturally modifies a quantity, or explicitly teach the comparative construction.
22|21|2|improve|“Он казался согласным с планом” is strained. “He is agreeable to this / Он согласен на это” models the willing/agreement sense more naturally.
22|24|1,2|fix|“Particularity” usually means a distinctive feature/peculiarity; “частность” is a particular detail. The example fails to establish a matching sense. Use особенность for the distinctive-feature sense and rebuild the examples.
23|6|2|fix|“Every student came, including the teacher” incorrectly includes the teacher in the set of students. Use “Everyone came, including the teacher / Все пришли, включая учителя”.
23|8|2|fix|“Он чувствовал себя глубоко несчастным внутри” is an English calque with redundant внутри. Use “He felt unhappy / Он чувствовал себя несчастным”.
24|1|2|fix|“Hiding something” is not “скрывает это” (hiding this). Use “скрывает что-то” or make the English say “this”.
24|2|2|fix|“Я чувствую сильное обязательство помогать” is unnatural. Use “I have an obligation to help / У меня есть обязательство помогать”.
24|7|2|improve|“Мы хотим максимальную эффективность” is strained as a model sentence. “Нужна максимальная эффективность / We need maximum efficiency” is clearer.
25|2|2|fix|“Ярко улыбнулась” is a calque of “smiled brightly”. Remove the adverb on both sides: “The red-haired girl smiled / Рыжая девушка улыбнулась”.
25|4|2|fix|“Ваш ответ был совершенным” is a poor ordinary collocation for a perfect answer. Use a subject that naturally takes совершенный, such as “совершенная система / a perfect system”, or change the Russian gloss to идеальный.
25|7|2|improve|“A colored book / цветная книга” is unclear about what is colored. Use “colored paper / цветная бумага”.
25|13|2|improve|“Is to be built soon” suggests a planned construction/result; “будет строиться” emphasizes the process. “The house is being built / Дом строится” aligns the target more cleanly.
25|18|2|fix|“Выставят новое искусство” is an unnatural collocation. Use “They will exhibit pictures / Они выставят картины”.
26|1|2|fix|“Гладкая смесь” copies English smooth and is a bad food-texture model. Simplify to “This is a mixture / Это смесь”, or use однородная with a matching gloss/context.
26|2|2|improve|English “a potato” implies one tuber; Russian “есть картошка” often means potatoes growing there. Make number and intended garden context explicit on both sides.
26|3|2|improve|“The melody sounds in my head” is unnatural English. Use “I hear a melody / Я слышу мелодию”.
26|14|2|fix|“A fine for speed / штраф за скорость” omits the offense. Normally “a fine for speeding / штраф за превышение скорости”; for simpler vocabulary use “He paid a fine / Он заплатил штраф”.
26|15|2|fix|“I learn Spanish this year” needs the ongoing tense: “I am learning Spanish this year”.
26|19|2|fix|“Волга течёт через землю” sounds like flowing through soil rather than across a territory. Use “Волга — река / The Volga is a river”.
27|13|2|fix|“Pursued an academic career” describes engaging in that career; “стремилась к” only says she aspired to it. Align with “She wanted an academic career / Она хотела академическую карьеру”.
27|14|2|fix|“Колеблись” is a valid imperative, but “Не колеблись спросить” is an unnatural construction/calque in contemporary usage. A natural translation of this English idiom is “Не стесняйся спросить”, which would miss колебаться. Preserve the target with “He hesitated / Он колебался”.
27|18|2|improve|“Startle → вздрогнуть” is valid for the intransitive English sense. This example instead uses transitive “startled me”; its causative Russian translation is correct, but a matching intransitive example would teach the listed pair more directly. [Merriam-Webster](https://www.merriam-webster.com/dictionary/startle).
27|22|2|fix|“Отмечали своё этническое наследие” is a calque of celebrate heritage. Use “They are proud of their ethnic heritage / Они гордятся своим этническим наследием”, or simplify further for vocabulary.
28|5|2|fix|“Заявить правду” is a bad collocation for proclaim the truth. Choose a natural announcement context and corresponding Russian, e.g. proclaim victory / провозгласить победу.
28|7|2|improve|“Им нужно удаление стола” is bureaucratic and unnatural for moving furniture. Use a concrete context where удаление naturally means removal, or a simpler “Удаление необходимо / Removal is necessary”.
28|17|1,2|fix|Engine тяга is normally “thrust” or pulling force; English traction normally concerns grip. A vehicle/road traction example or a revised gloss is needed.
28|23|2|fix|Laundry is стирать: “Я стираю простыню / I wash the sheet”. “Мою простыню” teaches the wrong washing verb for ordinary laundry.
28|24|1,2|improve|The pair is valid in some contexts, but “формально принял” can suggest acceptance merely in form, whereas the English can mean officially. Specify the intended sense; официально is clearer for official acceptance. [Cambridge](https://dictionary.cambridge.org/dictionary/english-russian/formally).
29|15|2|improve|“The player intercepts the letter” is an odd scene without a game narrative. Use a ball or a non-player subject, keeping both faces aligned.
29|17|1,2|fix|Technical composite materials are “композитные материалы”, not simply составные. Also “Мост использует” personifies the bridge awkwardly. Choose a true component/composite sense and rebuild both sides.
30|18|2|fix|“Яркость солнца сильная” / “brightness … is strong” are poor collocations. Use “Яркость высокая / The brightness is high”, or a concrete brightness-control example.
30|20|1|improve|Бодрый emphasizes vigor/alertness; cheerful emphasizes a happy mood. “Cheerful” can overlap, but весёлый is a cleaner target for the current context; otherwise change the English sense explicitly.
31|14|1,2|fix|A dream “сбывается”, not “свершается”. Use “to come true → сбыться”; “My dream came true / Моя мечта сбылась”.
31|16|2|improve|“Issued a strict order” and “строго приказал” move strictness from the order to the manner of commanding. Simpler: “The commandant gave an order / Комендант отдал приказ”.
32|7|2|improve|“Her feline nature is clear / Её кошачья природа ясна” is vague and artificial. Use a concrete feline feature, such as eyes.
32|9|2|fix|“Сладость … была сильной” is a poor collocation. Use “I like the cake's sweetness / Мне нравится сладость торта”.
32|16|2|fix|“Его наглость была ясной” is unnatural. Use “His impudence surprised me / Его наглость меня удивила”.
32|19|2|improve|“His behavior was an oddity” is stilted and may characterize the behavior as an object. A concrete noticed oddity is clearer: “I noticed an oddity / Я заметил странность”.
33|7|1,2|fix|“Got hooked on the idea” suggests becoming fascinated; “зацепилась за идею” suggests seizing on it. Use a literal snagging context for зацепиться or change the Russian target for the fascination sense.
34|7|1,2|fix|The university subject “calculus” needs “математический анализ” or specified дифференциальное/интегральное исчисление. Bare исчисление is too broad in the example.
34|9|1|fix|Комбат is “battalion commander”, not generic “combat commander”. Correct the English headword and example. Dictionary confirmation: [Gramota](https://gramota.ru/poisk?mode=all&query=%D0%BA%D0%BE%D0%BC%D0%B1%D0%B0%D1%82).
34|15|2|fix|“A byte stores one character” is not generally true: characters can occupy multiple bytes. Use “A byte has eight bits / В байте восемь бит”.
34|18|2|fix|For butter, размягчить is more natural than смягчить. Preserve смягчить with a natural context such as “soften the blow / смягчить удар”.
35|19|2|improve|“The rate will be fixed tomorrow” implies a set result; “будет фиксироваться” emphasizes the process/repetition. Use a present repeated-recording example or explicitly align the aspect.
35|23|4|fix|The target noun канализация never appears: канализационная is a derived adjective, not an inflection. Use “В городе есть канализация / The city has sewerage”.
36|6|1,2|improve|“Concentratedly” is highly unnatural as an everyday vocabulary headword/example. Prefer “with concentration / сосредоточенно” and align the example; this requires a headword change.
36|7|1,2|fix|Standalone “Берегись!” usually means “Watch out!/Beware!”; polite “Please take care” usually means “Береги себя”. The current pairing confuses these speech acts.
36|22|2|improve|“His membership is over / Его членство кончилось” is clumsy. “His membership ended / Его членство закончилось” is a cleaner simple model.
36|23|2|improve|“Frenziedly” is awkward for an everyday example even though it is a real word. Prefer a more idiomatic adverb or phrase and explicitly align the gloss.
37|7|2|improve|“Her dress has elegance / В её платье есть изящество” is stilted. Use “I admire its elegance / Я восхищаюсь его изяществом”, or another short natural sentence after checking vocabulary.
37|20|1,2|fix|“My zodiac / свой зодиак” confuses the zodiac with a zodiac sign. Keep zodiac with “The zodiac has twelve signs / У зодиака двенадцать знаков”, or change the target to “zodiac sign / знак зодиака”.
37|24|1,2|fix|The English idiom is normally “get into the swing of things”, not bare “get into the swing”. Разыграться needs a playing/warming-up context. Complete and contextualize the phrase or change the gloss.
38|2|2|fix|“This work is to be paid soon” and “будет оплачиваться” are awkward for a one-off payment. Preserve оплачиваться using “This work is paid for / Эта работа оплачивается”.
38|8|2|fix|“I will rummage” states a future action; “Я хочу порыться” says I want to. Use “Я пороюсь на чердаке” or add “want to” on the English side.
38|10|2|fix|“Пресвятое место” is a poor generic collocation; пресвятой is predominantly an elevated religious epithet. Use a genuine religious expression and its established English equivalent.
38|18|1,2|fix|The song is normally called “The Internationale” in English, not “the International”. Correct the song headword/example, or choose an actual international-organization sense and matching Russian.
39|4|2|improve|“Possessed by a strange energy” is vague and figurative. A concrete obsession/possession example would teach the selected sense more clearly.
39|10|2|fix|“The mountain relief is high / Рельеф горы высокий” is a poor technical collocation. Use “The terrain is uneven / Рельеф неровный”, with the corresponding sense selected in the gloss.
39|15|2|improve|“Винт слишком тугой” is less clear than a tight lid/door/rope context. Choose a natural noun with тугой and mirror it in English.
39|17|1|fix|“Disperse” is not a reliable interchangeable gloss for растворяться; dissolution and dispersion differ. Keep “dissolve” for the sugar example.
39|23|1|fix|“Shawl” is normally шаль, not шарф. Keep “scarf” for this card.
'''
findings=[]
for line in RAW.strip().splitlines():
 di,row,cats,level,note=line.split('|',4);di=int(di);row=int(row);d=D[di];c=d['cards'][row-1]
 findings.append(dict(deck_index=di,row=row,categories=cats.split(','),level=level,note=note))
# Aspect partners are meaningful consistency concerns, not synonym-substitution errors.
for di,row,note in [(9,8,'болтать → поболтаем (поболтать)'),(9,16,'одеваться → одеться'),(29,15,'перехватить → перехватывает (перехватывать)'),(39,8,'натягивать → натяну (натянуть)'),(39,17,'растворяться → растворится (раствориться)')]:
 findings.append(dict(deck_index=di,row=row,categories=['4'],level='consistency',note=f'The example uses an aspect partner: {note}. Meaning is related, so this is not a messenger/bearer substitution. For strict practice of the exact listed lemma, rewrite the example with that lemma; ordinary tense/case inflections are accepted.'))
# Remove morphology artifacts and familiar aspect partners from the vocabulary-only findings.
skip={('russian_english','4500->5000',8),('russian_english','4500->5000',16),('english_russian','1500->2000',14),('english_russian','1500->2000',18),('english_russian','2000->2500',17),('english_russian','2000->2500',21),('english_russian','4500->5000',7),('english_russian','4500->5000',12),('english_russian','4500->5000',15),('english_russian','4500->5000',23),('english_russian','4500->5000',25),('english_russian','5000->5500',9),('english_russian','5500->6000',1),('english_russian','5500->6000',24),('english_russian','6000->6500',13),('english_russian','6500->7000',10),('english_russian','8000->8500',2),('english_russian','8000->8500',13),('english_russian','8000->8500',22),('english_russian','9500->10000',8)}
for r in json.load(open(Path(__file__).with_name('vocabulary_candidates.json'))):
 if (r['pack'],r['band'],r['row']) in skip:continue
 di=next(i for i,d in enumerate(D) if d['pack']==r['pack'] and d['band']==r['band'])
 parts=[]
 for lang,ts in r['missing'].items():
  for word,b in ts:
   if word=='поздна':continue # misspelling, already reported
   location='absent as a headword in this pack' if b=='absent' else f'first headword band {b}→{b+500}'
   parts.append(f'{word} ({lang.upper()}; {location})')
 if not parts:continue
 note='Vocabulary outside the allowed earlier-deck inventory: '+ '; '.join(parts)+'. Simplify the example using previously introduced words. Same-band vocabulary fails the requested rule even when it is easy or appears earlier within this deck.'
 if r['pack']=='english_russian' and r['word']=='socket':note+=' The existing same-band “to plug → заткнуть” is also a different sense from the electrical noun plug.'
 findings.append(dict(deck_index=di,row=r['row'],categories=['3'],level='sequence',note=note))
# Store exact evidence once per flagged card; keep all 1,000 cards for audit traceability.
by={}
for f in findings:by.setdefault((f['deck_index'],f['row']),[]).append(f)
records=[]
for di,d in enumerate(D):
 for c in d['cards'][:25]:
  records.append(dict(pack=d['pack'],band=d['band'],file=d['file'],**c,findings=by.get((di,c['row']),[])))
Path(__file__).with_name('review.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
md=['# First 25 cards in each Russian-language deck: audit','', 'Reviewed 2026-09-07. Scope: current top-level CSVs in `russian_english/` and `english_russian/`; 20 decks per direction, 25 cards per deck, **1,000 cards**. Source decks were not edited and no Brainscape calls were made.','', '## How to read this report','', '- **1 — Translation:** incorrect or misleading headword/gloss or sense.','- **2 — Example:** grammar, meaning mismatch, bad collocation, or unnatural example.','- **3 — Vocabulary sequencing:** supporting vocabulary not found in prior decks of the same pack. For the first 1→500 deck, its whole deck is allowed. The current target itself is always allowed.','- **4 — Target use:** the example replaces the listed target with another form/word. Ordinary inflections are accepted; aspect partners are marked separately as consistency concerns.','', '**Fix** means a concrete correction is recommended. **Improve** marks a naturalness/clarity judgment rather than a categorical grammatical error. **Sequence** flags the requested vocabulary rule; it does not imply the sentence is intrinsically complicated. **Consistency** marks an aspect partner rather than an unrelated synonym.','', 'Vocabulary checks use the actual headwords on each language side of each pack, not the other direction and not all words occurring in examples. Russian morphology and English irregular-form normalization were used, followed by manual filtering. Common function words are exempt. Familiar verbal aspect variants were manually excluded from vocabulary flags; the feminine воспитанница for воспитанник is not counted as new supporting vocabulary. Derivations and different parts of speech are not automatically interchangeable. Vocabulary results are conservative flags, not proof that every unflagged token is taught in the intended sense. “Absent” means absent from this pack’s headwords, not absent from Russian or English.','', 'Suggested repairs explain direction; they are not a fully rewritten, vocabulary-validated replacement deck. Card numbers below are **1-based positions within each deck**, not physical CSV line numbers.','']
counts=Counter(f['level'] for f in findings)
md += [f'**{len(by)} of 1,000 sampled cards have at least one finding.** Finding entries: '+', '.join(f'{v} {k}' for k,v in counts.items())+'. A card can have multiple entries.','', '## Coverage by deck','', '| Direction | Band | Cards checked | Cards flagged |','|---|---|---:|---:|']
for di,d in enumerate(D):
 md.append(f"| {'RU→EN' if di<20 else 'EN→RU'} | {d['band'].replace('->','→')} | 25 | {sum((di,r) in by for r in range(1,26))} |")
for di,d in enumerate(D):
 md+=['',f"## {'RU→EN' if di<20 else 'EN→RU'} · {d['band'].replace('->','→')}",'',f"Source: [{d['file']}]({'../'+d['pack']+'/'+d['file']})",'']
 items=[(r,by[(di,r)]) for r in range(1,26) if (di,r) in by]
 if not items:md+=['No actionable issue identified in these 25 cards under the stated review criteria.'];continue
 for row,fs in items:
  c=d['cards'][row-1]
  md += [f"### Card {row}: {c['q']} → {c['a']}",'',f"- Question example: {c['qe']}",f"- Answer example: {c['ae']}"]
  for f in fs:md += [f"- **{f['level'].capitalize()} · {', '.join(f['categories'])}:** {f['note']}"]
  md+=['']
md += ['## Accepted cases and limits','', '- Inflections such as пойду/идёт where appropriate, plural nouns, and case forms do not automatically fail target use. Feminine воспитанницей for воспитанник is accepted as a gender counterpart; use a male example if literal lemma identity is required.','- “suite → свита” is a valid dictionary sense, so it was not labeled a mistranslation. [Merriam-Webster, suite](https://www.merriam-webster.com/dictionary/suite).','- “комбат” was checked against the definition “commander of a battalion”. [Gramota, комбат](https://gramota.ru/poisk?mode=all&query=%D0%BA%D0%BE%D0%BC%D0%B1%D0%B0%D1%82).','- RU→EN приведение → reduction/bringing and EN→RU ghost → привидение are different valid targets in the files reviewed; the former was not treated as a ghost-translation typo.','- A valid selected sense is acceptable even when other senses exist. Short natural fragments are not automatically errors.','- This is a sample audit, not a review of the remaining 19,000 cards, and it establishes nothing about the live Brainscape state.','']
Path(__file__).with_name('report.md').write_text('\n'.join(md))
manifest=[dict(pack=d['pack'],file=d['file'],sha256=hashlib.sha256((ROOT/d['pack']/d['file']).read_bytes()).hexdigest(),cards=len(d['cards']),checked=25) for d in D]
Path(__file__).with_name('source_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps(dict(cards=1000,flagged=len(by),entries=counts,by_pack={p:len({(f['deck_index'],f['row']) for f in findings if D[f['deck_index']]['pack']==p}) for p in ['russian_english','english_russian']},categories={str(n):len({(f['deck_index'],f['row']) for f in findings if str(n) in f['categories']}) for n in range(1,5)}),indent=2))
