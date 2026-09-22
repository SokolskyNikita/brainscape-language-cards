# First 25 cards in each Russian-language deck: audit

Reviewed 2026-09-07. Scope: current top-level CSVs in `russian_english/` and `english_russian/`; 20 decks per direction, 25 cards per deck, **1,000 cards**. Source decks were not edited and no Brainscape calls were made.

## How to read this report

- **1 — Translation:** incorrect or misleading headword/gloss or sense.
- **2 — Example:** grammar, meaning mismatch, bad collocation, or unnatural example.
- **3 — Vocabulary sequencing:** supporting vocabulary not found in prior decks of the same pack. For the first 1→500 deck, its whole deck is allowed. The current target itself is always allowed.
- **4 — Target use:** the example replaces the listed target with another form/word. Ordinary inflections are accepted; aspect partners are marked separately as consistency concerns.

**Fix** means a concrete correction is recommended. **Improve** marks a naturalness/clarity judgment rather than a categorical grammatical error. **Sequence** flags the requested vocabulary rule; it does not imply the sentence is intrinsically complicated. **Consistency** marks an aspect partner rather than an unrelated synonym.

Vocabulary checks use the actual headwords on each language side of each pack, not the other direction and not all words occurring in examples. Russian morphology and English irregular-form normalization were used, followed by manual filtering. Common function words are exempt. Familiar verbal aspect variants were manually excluded from vocabulary flags; the feminine воспитанница for воспитанник is not counted as new supporting vocabulary. Derivations and different parts of speech are not automatically interchangeable. Vocabulary results are conservative flags, not proof that every unflagged token is taught in the intended sense. “Absent” means absent from this pack’s headwords, not absent from Russian or English.

Suggested repairs explain direction; they are not a fully rewritten, vocabulary-validated replacement deck. Card numbers below are **1-based positions within each deck**, not physical CSV line numbers.

**161 of 1,000 sampled cards have at least one finding.** Finding entries: 44 improve, 65 fix, 5 consistency, 58 sequence. A card can have multiple entries.

## Coverage by deck

| Direction | Band | Cards checked | Cards flagged |
|---|---|---:|---:|
| RU→EN | 1→500 | 25 | 2 |
| RU→EN | 500→1000 | 25 | 1 |
| RU→EN | 1000→1500 | 25 | 2 |
| RU→EN | 1500→2000 | 25 | 3 |
| RU→EN | 2000→2500 | 25 | 0 |
| RU→EN | 2500→3000 | 25 | 2 |
| RU→EN | 3000→3500 | 25 | 3 |
| RU→EN | 3500→4000 | 25 | 4 |
| RU→EN | 4000→4500 | 25 | 7 |
| RU→EN | 4500→5000 | 25 | 6 |
| RU→EN | 5000→5500 | 25 | 2 |
| RU→EN | 5500→6000 | 25 | 5 |
| RU→EN | 6000→6500 | 25 | 2 |
| RU→EN | 6500→7000 | 25 | 2 |
| RU→EN | 7000→7500 | 25 | 3 |
| RU→EN | 7500→8000 | 25 | 3 |
| RU→EN | 8000→8500 | 25 | 3 |
| RU→EN | 8500→9000 | 25 | 2 |
| RU→EN | 9000→9500 | 25 | 2 |
| RU→EN | 9500→10000 | 25 | 2 |
| EN→RU | 1→500 | 25 | 1 |
| EN→RU | 500→1000 | 25 | 9 |
| EN→RU | 1000→1500 | 25 | 8 |
| EN→RU | 1500→2000 | 25 | 5 |
| EN→RU | 2000→2500 | 25 | 5 |
| EN→RU | 2500→3000 | 25 | 7 |
| EN→RU | 3000→3500 | 25 | 10 |
| EN→RU | 3500→4000 | 25 | 8 |
| EN→RU | 4000→4500 | 25 | 5 |
| EN→RU | 4500→5000 | 25 | 5 |
| EN→RU | 5000→5500 | 25 | 2 |
| EN→RU | 5500→6000 | 25 | 3 |
| EN→RU | 6000→6500 | 25 | 4 |
| EN→RU | 6500→7000 | 25 | 6 |
| EN→RU | 7000→7500 | 25 | 4 |
| EN→RU | 7500→8000 | 25 | 3 |
| EN→RU | 8000→8500 | 25 | 5 |
| EN→RU | 8500→9000 | 25 | 4 |
| EN→RU | 9000→9500 | 25 | 5 |
| EN→RU | 9500→10000 | 25 | 6 |

## RU→EN · 1→500

Source: [deck_15260182.csv](../russian_english/deck_15260182.csv)

### Card 13: то → that, that one

- Question example: Это не то.
- Answer example: That's not that one.
- **Improve · 2:** “That's not that one” is an awkward, context-dependent rendering of “Это не то”. Use “That is not what I meant” or rebuild both faces around “то”, keeping an allowed English gloss.

### Card 23: у → have, at

- Question example: У него дом.
- Answer example: He has a house.
- **Fix · 1:** The gloss “have” describes the whole possession construction у + genitive + есть/zero, not the preposition alone. Label it “at; used in possession: у него … = he has …” so the card does not teach у as a verb.


## RU→EN · 500→1000

Source: [deck_15260185.csv](../russian_english/deck_15260185.csv)

### Card 16: чуть → a little, slightly

- Question example: Я чуть понял.
- Answer example: I understood a little.
- **Fix · 2:** “Я чуть понял” is unnatural for “I understood a little”; чуть often suggests barely/almost in this environment. Use “Я чуть устал / I am a little tired”.


## RU→EN · 1000→1500

Source: [deck_15260188.csv](../russian_english/deck_15260188.csv)

### Card 7: сестра → sister

- Question example: Сестра уже дома.
- Answer example: Sister's already home.
- **Improve · 2:** Bare “Sister's already home” needs a family-name style context. “My sister is already home / Моя сестра уже дома” is a better standalone model.

### Card 22: целое → the whole

- Question example: Это одно целое.
- Answer example: It's the whole.
- **Fix · 2:** “Это одно целое” means “It is a single whole”, not simply “It's the whole”. Preserve одно in the translation: “It is one whole”.


## RU→EN · 1500→2000

Source: [deck_15260190.csv](../russian_english/deck_15260190.csv)

### Card 11: повышение → raise, increase

- Question example: Мне дали повышение.
- Answer example: They gave me a raise.
- **Improve · 1, 2:** “Мне дали повышение” normally suggests a promotion; “a raise” specifically suggests increased pay. Teach “promotion” here, or explicitly say “повышение зарплаты” for a pay raise.

### Card 12: крыша → roof

- Question example: Кот на крыше.
- Answer example: The cat's on the roof.
- **Sequence · 3:** Vocabulary outside the allowed earlier-deck inventory: кот (RU; first headword band 1500→2000); cat (EN; first headword band 1500→2000). Simplify the example using previously introduced words. Same-band vocabulary fails the requested rule even when it is easy or appears earlier within this deck.

### Card 16: контакт → contact

- Question example: Дай контакт.
- Answer example: Give me the contact.
- **Improve · 2:** “Give me the contact” is vague English without context. Specify “contact details” and the corresponding Russian, or use an example such as “Мы поддерживаем контакт / We keep in contact”.


## RU→EN · 2000→2500

Source: [deck_15260191.csv](../russian_english/deck_15260191.csv)

No actionable issue identified in these 25 cards under the stated review criteria.

## RU→EN · 2500→3000

Source: [deck_15260192.csv](../russian_english/deck_15260192.csv)

### Card 1: дар → gift, talent

- Question example: У неё дар к музыке.
- Answer example: She has a gift for music.
- **Fix · 2:** “У неё дар к музыке” is a poor collocation. Use “У неё музыкальный дар / She has a gift for music”, or “У неё дар / She has a gift” for simpler vocabulary.

### Card 14: ловить → to catch

- Question example: Лови шар!
- Answer example: Catch the ball!
- **Sequence · 3:** Vocabulary outside the allowed earlier-deck inventory: шар (RU; first headword band 2500→3000); ball (EN; first headword band 2500→3000). Simplify the example using previously introduced words. Same-band vocabulary fails the requested rule even when it is easy or appears earlier within this deck.


## RU→EN · 3000→3500

Source: [deck_15260194.csv](../russian_english/deck_15260194.csv)

### Card 6: преследовать → to pursue

- Question example: Полиция преследует вора.
- Answer example: The police pursue the thief.
- **Sequence · 3:** Vocabulary outside the allowed earlier-deck inventory: вора (RU; first headword band 3000→3500); thief (EN; first headword band 3000→3500). Simplify the example using previously introduced words. Same-band vocabulary fails the requested rule even when it is easy or appears earlier within this deck.

### Card 9: корпоративный → corporate

- Question example: У нас корпоративный праздник.
- Answer example: We have a corporate holiday.
- **Improve · 2:** “A corporate holiday” suggests a company holiday rather than a company celebration. Use a clearer shared collocation such as “корпоративный сайт / corporate website”, subject to vocabulary checks.

### Card 18: вплоть → up to

- Question example: Он ждал вплоть до утра.
- Answer example: He waited up to morning.
- **Fix · 2:** “He waited up to morning” is unnatural temporal English. Use gloss “right up until” and “He waited right up until morning / Он ждал вплоть до утра”.


## RU→EN · 3500→4000

Source: [deck_15260196.csv](../russian_english/deck_15260196.csv)

### Card 6: быт → everyday life, existence

- Question example: Это наш обычный быт.
- Answer example: This is our everyday life.
- **Fix · 1:** “Existence” is too broad as an unqualified gloss for быт. Keep “everyday life; domestic life”.

### Card 11: планирование → planning, scheduling

- Question example: Планирование поездки трудно.
- Answer example: Planning a trip is hard.
- **Improve · 2:** “Планирование поездки трудно” sounds strained. “Планирование поездки — трудная работа” or a simpler shared sentence is more natural.

### Card 18: охватить → to cover, to encompass

- Question example: Страх охватил его.
- Answer example: Fear encompassed him.
- **Fix · 1, 2:** “Fear encompassed him” is a forced literal translation. This sense of охватить is “to grip/overwhelm”: “Страх охватил его / Fear gripped him”. Update the gloss to match.

### Card 21: плоть → flesh, meat

- Question example: Это плоть и кровь.
- Answer example: This is flesh and blood.
- **Fix · 1:** “Meat” teaches the wrong everyday sense for плоть. Keep “flesh”; food meat is мясо.


## RU→EN · 4000→4500

Source: [deck_15260198.csv](../russian_english/deck_15260198.csv)

### Card 1: давить → to press, to crush

- Question example: Сапог давит мне ногу.
- Answer example: The boot presses my foot.
- **Fix · 2:** “The boot presses my foot” is unnatural English. Use “The boot presses against my foot”, or teach “pinch” for this sense and update the gloss.

### Card 2: усиление → intensification, reinforcement

- Question example: Мы ждали усиления бури.
- Answer example: We waited for the storm's intensification.
- **Improve · 2:** “We waited for the storm's intensification” is cumbersome. Use a simpler pairing such as “Усиление ветра / Intensification of the wind”, after confirming vocabulary.
- **Sequence · 3:** Vocabulary outside the allowed earlier-deck inventory: бури (RU; first headword band 4000→4500); storm (EN; first headword band 4000→4500). Simplify the example using previously introduced words. Same-band vocabulary fails the requested rule even when it is easy or appears earlier within this deck.

### Card 8: претендовать → claim, aspire

- Question example: Она будет претендовать на звание чемпиона.
- Answer example: She will claim the championship title.
- **Fix · 1, 2:** “Претендовать на звание” means to contend for/lay claim to a title, not necessarily win it. “She will claim the championship title” implies success. Use “She will contend for the title” and align the gloss.
- **Sequence · 3:** Vocabulary outside the allowed earlier-deck inventory: чемпиона (RU; first headword band 4000→4500). Simplify the example using previously introduced words. Same-band vocabulary fails the requested rule even when it is easy or appears earlier within this deck.

### Card 13: квалификация → qualification, credentials

- Question example: У него высокая квалификация.
- Answer example: He has a high qualification.
- **Fix · 2:** “He has a high qualification” is a Russian calque. Use “He has professional qualifications / У него профессиональная квалификация”, or “He is highly qualified” with a matching gloss/form.

### Card 15: сыр → cheese, curd

- Question example: Я ем сыр с хлебом.
- Answer example: I eat cheese with bread.
- **Fix · 1:** “Curd” is not a reliable standalone translation of сыр; keep “cheese”. Curd/curds require their own food sense and context.

### Card 21: исключительный → exceptional, exclusive

- Question example: У неё исключительный талант в живописи.
- Answer example: She has exceptional talent in painting.
- **Sequence · 3:** Vocabulary outside the allowed earlier-deck inventory: живописи (RU; first headword band 4000→4500). Simplify the example using previously introduced words. Same-band vocabulary fails the requested rule even when it is easy or appears earlier within this deck.

### Card 24: национальность → nationality, ethnicity

- Question example: Её национальность - русская.
- Answer example: Her nationality is Russian.
- **Fix · 1, 2:** The example leaves ethnicity versus citizenship ambiguous. “Национальность” in this Russian sentence normally describes ethnicity; English “nationality” usually suggests citizenship. Use the existing “ethnicity” gloss and a matching example, or explain the distinction.


## RU→EN · 4500→5000

Source: [deck_15260200.csv](../russian_english/deck_15260200.csv)

### Card 8: болтать → chat, babble

- Question example: Мы поболтаем за чашкой чая.
- Answer example: We'll chat over a cup of tea.
- **Consistency · 4:** The example uses an aspect partner: болтать → поболтаем (поболтать). Meaning is related, so this is not a messenger/bearer substitution. For strict practice of the exact listed lemma, rewrite the example with that lemma; ordinary tense/case inflections are accepted.

### Card 9: проживание → residence, living

- Question example: Проживание здесь дорого.
- Answer example: Residence here is expensive.
- **Fix · 2:** “Residence here is expensive” is unnatural for “Проживание здесь дорого”. Use the existing “living” gloss: “Living here is expensive”.

### Card 16: одеваться → to dress, to get dressed

- Question example: Мне нужно одеться сейчас.
- Answer example: I need to get dressed now.
- **Consistency · 4:** The example uses an aspect partner: одеваться → одеться. Meaning is related, so this is not a messenger/bearer substitution. For strict practice of the exact listed lemma, rewrite the example with that lemma; ordinary tense/case inflections are accepted.

### Card 17: поворачиваться → to turn, to rotate

- Question example: Он всегда поворачивается налево.
- Answer example: He always turns left.
- **Sequence · 3:** Vocabulary outside the allowed earlier-deck inventory: налево (RU; first headword band 4500→5000). Simplify the example using previously introduced words. Same-band vocabulary fails the requested rule even when it is easy or appears earlier within this deck.

### Card 22: регулировать → regulate, adjust

- Question example: Нужно регулировать воду.
- Answer example: We need to regulate the water.
- **Improve · 2:** “Regulate the water” leaves the controlled quantity unspecified. Specify flow/temperature on both sides, or choose a simpler object.

### Card 23: ось → axis, axle

- Question example: Это ось колеса.
- Answer example: This is the wheel's axis.
- **Fix · 1, 2:** For a wheel's physical shaft, English uses “axle”, already in the gloss. If the abstract axis is intended, say “ось вращения / axis of rotation”.


## RU→EN · 5000→5500

Source: [deck_15260204.csv](../russian_english/deck_15260204.csv)

### Card 22: промежуток → interval, gap

- Question example: В этом промежутке тихо.
- Answer example: It's quiet in this interval.
- **Improve · 2:** “It's quiet in this interval” is artificial without an established time interval. Use “Между ними промежуток / There is a gap between them”.

### Card 24: окрестность → vicinity

- Question example: В окрестности тихо.
- Answer example: It's quiet in the vicinity.
- **Improve · 2:** “В окрестности тихо” is strained for “in the vicinity”; обычное “В окрестностях тихо” is the natural plural of the same lemma.


## RU→EN · 5500→6000

Source: [deck_15260207.csv](../russian_english/deck_15260207.csv)

### Card 1: дизайнер → designer, stylist

- Question example: Она наняла дизайнера.
- Answer example: She hired a designer.
- **Sequence · 3:** Vocabulary outside the allowed earlier-deck inventory: наняла (RU; first headword band 5500→6000); hired (EN; first headword band 5500→6000). Simplify the example using previously introduced words. Same-band vocabulary fails the requested rule even when it is easy or appears earlier within this deck.

### Card 9: подбор → selection, choice

- Question example: Долгий подбор.
- Answer example: A long selection.
- **Improve · 2:** “A long selection” can mean a long list rather than a lengthy selection process. “Подбор занял час / The selection took an hour” teaches the process clearly.

### Card 10: совершаться → to occur, to take place

- Question example: Церемония совершается.
- Answer example: The ceremony is taking place.
- **Improve · 2:** “Церемония совершается” is an unusual general model; совершается naturally combines with обряд. Choose a concrete compatible subject and mirror it in English.

### Card 13: проследить → track, monitor

- Question example: Я прослежу за этим.
- Answer example: I'll track this.
- **Fix · 1, 2:** “Я прослежу за этим” generally means “I will see to it/keep an eye on it”. “I'll track this” suggests tracking an object. Align both examples with the intended monitoring sense.

### Card 25: загрузка → loading, download

- Question example: Долгая загрузка.
- Answer example: Long loading.
- **Fix · 2:** “Long loading” is not idiomatic standalone English. Use “Загрузка идёт медленно / Loading is slow”.


## RU→EN · 6000→6500

Source: [deck_15260210.csv](../russian_english/deck_15260210.csv)

### Card 10: нора → burrow

- Question example: Лиса сидит в норе.
- Answer example: The fox sits in the burrow.
- **Sequence · 3:** Vocabulary outside the allowed earlier-deck inventory: лиса (RU; first headword band 6000→6500); fox (EN; first headword band 6000→6500). Simplify the example using previously introduced words. Same-band vocabulary fails the requested rule even when it is easy or appears earlier within this deck.

### Card 25: прижимать → to press

- Question example: Она прижимает книгу.
- Answer example: She presses the book.
- **Improve · 2:** “Она прижимает книгу” leaves out what she presses it against. Add “к себе / to herself” or another clear complement.


## RU→EN · 6500→7000

Source: [deck_15260213.csv](../russian_english/deck_15260213.csv)

### Card 17: пират → pirate, buccaneer

- Question example: Пират украл сундук с сокровищами.
- Answer example: The pirate stole the treasure chest.
- **Sequence · 3:** Vocabulary outside the allowed earlier-deck inventory: сундук (RU; first headword band 6500→7000). Simplify the example using previously introduced words. Same-band vocabulary fails the requested rule even when it is easy or appears earlier within this deck.

### Card 19: востребовать → to claim

- Question example: Он востребовал свой долг.
- Answer example: He claimed his debt.
- **Fix · 2:** “He claimed his debt” sounds as though he is claiming a debt he owes. Use “He demanded repayment of the debt” and a matching claim/demand gloss for востребовать.


## RU→EN · 7000→7500

Source: [deck_15260214.csv](../russian_english/deck_15260214.csv)

### Card 3: надлежать → to be due

- Question example: Книгу надлежит вернуть завтра.
- Answer example: The book is due tomorrow.
- **Fix · 1:** Надлежать expresses obligation: “must; should; be required to”. “To be due” is too narrow and does not capture the verb generally. “Книгу надлежит вернуть завтра / The book must be returned tomorrow”.

### Card 10: идеально → ideally

- Question example: Идеально, мы закончим завтра.
- Answer example: Ideally, we will finish tomorrow.
- **Fix · 2:** “Идеально, мы закончим завтра” is a calque of sentence-initial English “Ideally”. Use “Всё прошло идеально / Everything went perfectly”, changing the gloss to “perfectly”.

### Card 22: яхта → yacht

- Question example: Яхта стоит у берега.
- Answer example: The yacht stands by the shore.
- **Improve · 2:** A yacht is “moored” or simply “is” by the shore, not normally “stands”. Translate стоит idiomatically while retaining “yacht”.


## RU→EN · 7500→8000

Source: [deck_15260215.csv](../russian_english/deck_15260215.csv)

### Card 7: рождать → to give birth

- Question example: Она рождает сына.
- Answer example: She is giving birth to a son.
- **Fix · 2:** “Она рождает сына” is a poor ordinary childbirth example; рожать is usual for literal labor. Preserve рождать with a natural figurative subject, e.g. “Страх рождает ненависть / Fear gives birth to hatred”.

### Card 11: чистка → cleaning

- Question example: Завтра нужна чистка дома.
- Answer example: The house needs cleaning tomorrow.
- **Fix · 2:** “Чистка дома” is not the normal collocation for housecleaning (уборка дома). Keep чистка but choose shoes/teeth or another suitable object on both faces.

### Card 20: медь → copper

- Question example: Это чистая медь.
- Answer example: This is clean copper.
- **Fix · 2:** “Чистая медь” normally means pure copper in this material-identification example. Use “This is pure copper”, not “clean copper”.


## RU→EN · 8000→8500

Source: [deck_15260217.csv](../russian_english/deck_15260217.csv)

### Card 10: норовить → to tend, to be inclined

- Question example: Он норовит спорить.
- Answer example: He tends to argue.
- **Improve · 1:** “Tend to” loses the persistent trying/attempting nuance of норовить. “He keeps trying to argue” is a better gloss/example alignment.

### Card 13: ложа → box

- Question example: Мы взяли ложу в театре.
- Answer example: We took a box at the theater.
- **Improve · 2:** “We took a box at the theater” is less clear than “We booked a box at the theater”. Align the Russian with a booking or seating context.

### Card 15: экспресс → express, fast train

- Question example: Экспресс идёт в полдень.
- Answer example: The express goes at noon.
- **Improve · 2:** “The express goes at noon” is unnatural timetable English. Use “The express leaves at noon”.


## RU→EN · 8500→9000

Source: [deck_15260218.csv](../russian_english/deck_15260218.csv)

### Card 6: сжаться → to shrink

- Question example: Ткань сжалась в воде.
- Answer example: The fabric shrank in water.
- **Fix · 1, 2:** For fabric shrinking in water, Russian normally uses сесть, not сжаться. Preserve сжаться with “contract”: “Мышца сжалась / The muscle contracted”, and update the gloss.

### Card 19: мнимый → imaginary

- Question example: Это мнимый друг.
- Answer example: This is an imaginary friend.
- **Fix · 1, 2:** “Мнимый друг” usually means an apparent/false friend, whereas “imaginary friend” means an invented companion. Teach “supposed/false” here or choose a different context for imaginary.


## RU→EN · 9000→9500

Source: [deck_15260221.csv](../russian_english/deck_15260221.csv)

### Card 6: мускул → muscle

- Question example: У него сильный мускул.
- Answer example: He has a strong muscle.
- **Improve · 2:** “He has a strong muscle” is an odd isolated statement. “У него сильные мускулы / He has strong muscles” uses an ordinary plural of the same target.

### Card 9: обеденный → dining, lunchtime

- Question example: Обеденный стол уже готов.
- Answer example: The dining table is already ready.
- **Improve · 2:** “The dining table is already ready” is awkward. Use “Обеденный стол большой / The dining table is large”, or a properly set-table example.


## RU→EN · 9500→10000

Source: [deck_15260224.csv](../russian_english/deck_15260224.csv)

### Card 2: покаяние → repentance

- Question example: Он ищет покаяния.
- Answer example: He is seeking repentance.
- **Improve · 2:** “Seeking repentance” is an unusual model; seeking forgiveness is more usual but would teach a different target. Use “Его покаяние искреннее / His repentance is sincere”, subject to vocabulary checks.
- **Sequence · 3:** Vocabulary outside the allowed earlier-deck inventory: seeking (EN; absent as a headword in this pack). Simplify the example using previously introduced words. Same-band vocabulary fails the requested rule even when it is easy or appears earlier within this deck.

### Card 4: одержимый → possessed, obsessed

- Question example: Она казалась одержимой странной энергией.
- Answer example: She seemed possessed by a strange energy.
- **Improve · 2:** “Possessed by a strange energy” is figurative and vague. A concrete “одержимый страхом / obsessed with fear” sense would teach the target more clearly, with matching gloss.


## EN→RU · 1→500

Source: [deck_15260246.csv](../english_russian/deck_15260246.csv)

### Card 15: they → они

- Question example: They come this evening.
- Answer example: Они придут сегодня вечером.
- **Improve · 2:** “They come this evening” is an unnatural standalone planned-arrival sentence. Use “They are coming this evening / Они придут сегодня вечером”.


## EN→RU · 500→1000

Source: [deck_15260248.csv](../english_russian/deck_15260248.csv)

### Card 1: to have to → приходиться

- Question example: I have to work late today.
- Answer example: Мне приходится работать до поздна сегодня.
- **Fix · 2:** “До поздна” is misspelled; write “допоздна”. Simpler: “Мне приходится работать / I have to work”.
- **Sequence · 3:** Vocabulary outside the allowed earlier-deck inventory: late (EN; first headword band 500→1000). Simplify the example using previously introduced words. Same-band vocabulary fails the requested rule even when it is easy or appears earlier within this deck.

### Card 3: enter → войти

- Question example: Please enter the room quietly.
- Answer example: Пожалуйста, войдите в комнату тихо.
- **Sequence · 3:** Vocabulary outside the allowed earlier-deck inventory: quietly (EN; first headword band 500→1000); тихо (RU; first headword band 500→1000). Simplify the example using previously introduced words. Same-band vocabulary fails the requested rule even when it is easy or appears earlier within this deck.

### Card 8: usual → обычный

- Question example: He wants his usual tea.
- Answer example: Он хочет свой обычный чай.
- **Sequence · 3:** Vocabulary outside the allowed earlier-deck inventory: tea (EN; first headword band 500→1000); чай (RU; first headword band 500→1000). Simplify the example using previously introduced words. Same-band vocabulary fails the requested rule even when it is easy or appears earlier within this deck.

### Card 10: dollar → доллар

- Question example: I found a dollar yesterday.
- Answer example: Я нашёл доллар вчера.
- **Sequence · 3:** Vocabulary outside the allowed earlier-deck inventory: yesterday (EN; first headword band 500→1000); вчера (RU; first headword band 500→1000). Simplify the example using previously introduced words. Same-band vocabulary fails the requested rule even when it is easy or appears earlier within this deck.

### Card 14: to arrive → приехать

- Question example: They hope to arrive today.
- Answer example: Они надеются приехать сегодня.
- **Sequence · 3:** Vocabulary outside the allowed earlier-deck inventory: hope (EN; first headword band 500→1000); надеются (RU; first headword band 500→1000). Simplify the example using previously introduced words. Same-band vocabulary fails the requested rule even when it is easy or appears earlier within this deck.

### Card 17: nature → природа

- Question example: Nature is beautiful.
- Answer example: Природа красивая.
- **Sequence · 3:** Vocabulary outside the allowed earlier-deck inventory: beautiful (EN; first headword band 500→1000); красивая (RU; first headword band 500→1000). Simplify the example using previously introduced words. Same-band vocabulary fails the requested rule even when it is easy or appears earlier within this deck.

### Card 19: like → вроде

- Question example: I need something like this.
- Answer example: Мне нужно что-то вроде этого.
- **Sequence · 3:** Vocabulary outside the allowed earlier-deck inventory: need (EN; first headword band 1000→1500). Simplify the example using previously introduced words. Same-band vocabulary fails the requested rule even when it is easy or appears earlier within this deck.

### Card 21: larger → больший

- Question example: Choose the larger house, please.
- Answer example: Выберите, пожалуйста, больший дом.
- **Improve · 2:** “Больший дом” is grammatical but marked in this request; ordinary Russian uses “дом побольше”. Prefer a context where больший naturally modifies a quantity, or explicitly teach the comparative construction.
- **Sequence · 3:** Vocabulary outside the allowed earlier-deck inventory: choose (EN; first headword band 500→1000); выберите (RU; first headword band 500→1000). Simplify the example using previously introduced words. Same-band vocabulary fails the requested rule even when it is easy or appears earlier within this deck.

### Card 23: object → объект

- Question example: The object was clearly visible.
- Answer example: Объект был явно виден.
- **Sequence · 3:** Vocabulary outside the allowed earlier-deck inventory: clearly (EN; first headword band 500→1000); visible (EN; first headword band 500→1000); явно (RU; first headword band 500→1000). Simplify the example using previously introduced words. Same-band vocabulary fails the requested rule even when it is easy or appears earlier within this deck.


## EN→RU · 1000→1500

Source: [deck_15260251.csv](../english_russian/deck_15260251.csv)

### Card 2: kitchen → кухня

- Question example: I love cooking in the kitchen.
- Answer example: Я люблю готовить на кухне.
- **Sequence · 3:** Vocabulary outside the allowed earlier-deck inventory: cooking (EN; first headword band 1000→1500); готовить (RU; first headword band 1000→1500). Simplify the example using previously introduced words. Same-band vocabulary fails the requested rule even when it is easy or appears earlier within this deck.

### Card 3: pocket → карман

- Question example: He found a key in his pocket.
- Answer example: Он нашёл ключ в своём кармане.
- **Sequence · 3:** Vocabulary outside the allowed earlier-deck inventory: key (EN; first headword band 1000→1500); ключ (RU; first headword band 1000→1500). Simplify the example using previously introduced words. Same-band vocabulary fails the requested rule even when it is easy or appears earlier within this deck.

### Card 9: according to → согласно

- Question example: According to the law, this is true.
- Answer example: Согласно закону, это правда.
- **Sequence · 3:** Vocabulary outside the allowed earlier-deck inventory: true (EN; first headword band 1000→1500). Simplify the example using previously introduced words. Same-band vocabulary fails the requested rule even when it is easy or appears earlier within this deck.

### Card 12: disappear → исчезнуть

- Question example: The man disappeared in the darkness.
- Answer example: Человек исчез в темноте.
- **Sequence · 3:** Vocabulary outside the allowed earlier-deck inventory: darkness (EN; first headword band 1000→1500); темноте (RU; first headword band 1000→1500). Simplify the example using previously introduced words. Same-band vocabulary fails the requested rule even when it is easy or appears earlier within this deck.

### Card 16: laugh → смеяться

- Question example: We laughed loudly.
- Answer example: Мы громко смеялись.
- **Sequence · 3:** Vocabulary outside the allowed earlier-deck inventory: loudly (EN; first headword band 1000→1500); громко (RU; first headword band 1000→1500). Simplify the example using previously introduced words. Same-band vocabulary fails the requested rule even when it is easy or appears earlier within this deck.

### Card 21: agreeable → согласный

- Question example: He seemed agreeable to the plan.
- Answer example: Он казался согласным с планом.
- **Improve · 2:** “Он казался согласным с планом” is strained. “He is agreeable to this / Он согласен на это” models the willing/agreement sense more naturally.

### Card 24: particularity → частность

- Question example: I see this particularity in his work.
- Answer example: Я вижу эту частность в его работе.
- **Fix · 1, 2:** “Particularity” usually means a distinctive feature/peculiarity; “частность” is a particular detail. The example fails to establish a matching sense. Use особенность for the distinctive-feature sense and rebuild the examples.

### Card 25: to fulfill → выполнить

- Question example: He promised to fulfill her wish.
- Answer example: Он обещал выполнить её желание.
- **Sequence · 3:** Vocabulary outside the allowed earlier-deck inventory: promised (EN; first headword band 1000→1500); обещал (RU; first headword band 1000→1500). Simplify the example using previously introduced words. Same-band vocabulary fails the requested rule even when it is easy or appears earlier within this deck.


## EN→RU · 1500→2000

Source: [deck_15260255.csv](../english_russian/deck_15260255.csv)

### Card 1: practical → практический

- Question example: She prefers practical solutions.
- Answer example: Она предпочитает практические решения.
- **Sequence · 3:** Vocabulary outside the allowed earlier-deck inventory: prefers (EN; first headword band 1500→2000); предпочитает (RU; first headword band 1500→2000). Simplify the example using previously introduced words. Same-band vocabulary fails the requested rule even when it is easy or appears earlier within this deck.

### Card 6: including → включая

- Question example: Every student came, including the teacher.
- Answer example: Каждый студент пришёл, включая учителя.
- **Fix · 2:** “Every student came, including the teacher” incorrectly includes the teacher in the set of students. Use “Everyone came, including the teacher / Все пришли, включая учителя”.

### Card 8: unhappy → несчастный

- Question example: He felt deeply unhappy inside.
- Answer example: Он чувствовал себя глубоко несчастным внутри.
- **Fix · 2:** “Он чувствовал себя глубоко несчастным внутри” is an English calque with redundant внутри. Use “He felt unhappy / Он чувствовал себя несчастным”.

### Card 9: layer → слой

- Question example: Add another layer of paint.
- Answer example: Добавьте еще один слой краски.
- **Sequence · 3:** Vocabulary outside the allowed earlier-deck inventory: paint (EN; first headword band 1500→2000); краски (RU; first headword band 1500→2000). Simplify the example using previously introduced words. Same-band vocabulary fails the requested rule even when it is easy or appears earlier within this deck.

### Card 16: meat → мясо

- Question example: I bought meat for dinner.
- Answer example: Я купил мясо на ужин.
- **Sequence · 3:** Vocabulary outside the allowed earlier-deck inventory: dinner (EN; first headword band 1500→2000); ужин (RU; first headword band 1500→2000). Simplify the example using previously introduced words. Same-band vocabulary fails the requested rule even when it is easy or appears earlier within this deck.


## EN→RU · 2000→2500

Source: [deck_15260256.csv](../english_russian/deck_15260256.csv)

### Card 1: suspect → подозревать

- Question example: I suspect he is hiding something.
- Answer example: Я подозреваю, что он скрывает это.
- **Fix · 2:** “Hiding something” is not “скрывает это” (hiding this). Use “скрывает что-то” or make the English say “this”.

### Card 2: obligation → обязательство

- Question example: I feel a strong obligation to help.
- Answer example: Я чувствую сильное обязательство помогать.
- **Fix · 2:** “Я чувствую сильное обязательство помогать” is unnatural. Use “I have an obligation to help / У меня есть обязательство помогать”.

### Card 7: maximum → максимальный

- Question example: We want maximum efficiency today.
- Answer example: Мы хотим максимальную эффективность сегодня.
- **Improve · 2:** “Мы хотим максимальную эффективность” is strained as a model sentence. “Нужна максимальная эффективность / We need maximum efficiency” is clearer.

### Card 9: minimal → минимальный

- Question example: The damage was minimal.
- Answer example: Ущерб был минимальным.
- **Sequence · 3:** Vocabulary outside the allowed earlier-deck inventory: damage (EN; first headword band 2000→2500); ущерб (RU; first headword band 2000→2500). Simplify the example using previously introduced words. Same-band vocabulary fails the requested rule even when it is easy or appears earlier within this deck.

### Card 12: remark → замечание

- Question example: He made a critical remark.
- Answer example: Он сделал критическое замечание.
- **Sequence · 3:** Vocabulary outside the allowed earlier-deck inventory: critical (EN; first headword band 2000→2500); критическое (RU; first headword band 2000→2500). Simplify the example using previously introduced words. Same-band vocabulary fails the requested rule even when it is easy or appears earlier within this deck.


## EN→RU · 2500→3000

Source: [deck_15260257.csv](../english_russian/deck_15260257.csv)

### Card 1: cave → пещера

- Question example: The cave is dark.
- Answer example: В пещере темно.
- **Sequence · 3:** Vocabulary outside the allowed earlier-deck inventory: dark (EN; first headword band 2500→3000); темно (RU; first headword band 2500→3000). Simplify the example using previously introduced words. Same-band vocabulary fails the requested rule even when it is easy or appears earlier within this deck.

### Card 2: red-haired → рыжий

- Question example: The red-haired girl smiled brightly.
- Answer example: Рыжая девушка ярко улыбнулась.
- **Fix · 2:** “Ярко улыбнулась” is a calque of “smiled brightly”. Remove the adverb on both sides: “The red-haired girl smiled / Рыжая девушка улыбнулась”.

### Card 4: perfect → совершенный

- Question example: Your answer was perfect.
- Answer example: Ваш ответ был совершенным.
- **Fix · 2:** “Ваш ответ был совершенным” is a poor ordinary collocation for a perfect answer. Use a subject that naturally takes совершенный, such as “совершенная система / a perfect system”, or change the Russian gloss to идеальный.

### Card 7: colored → цветной

- Question example: I bought a colored book.
- Answer example: Я купил цветную книгу.
- **Improve · 2:** “A colored book / цветная книга” is unclear about what is colored. Use “colored paper / цветная бумага”.

### Card 13: to be built → строиться

- Question example: The house is to be built soon.
- Answer example: Дом скоро будет строиться.
- **Improve · 2:** “Is to be built soon” suggests a planned construction/result; “будет строиться” emphasizes the process. “The house is being built / Дом строится” aligns the target more cleanly.

### Card 18: exhibit → выставить

- Question example: They will exhibit new art.
- Answer example: Они выставят новое искусство.
- **Fix · 2:** “Выставят новое искусство” is an unnatural collocation. Use “They will exhibit pictures / Они выставят картины”.

### Card 21: match → матч

- Question example: They won the football match.
- Answer example: Они победили в футбольном матче.
- **Sequence · 3:** Vocabulary outside the allowed earlier-deck inventory: football (EN; first headword band 2500→3000); футбольном (RU; absent as a headword in this pack). Simplify the example using previously introduced words. Same-band vocabulary fails the requested rule even when it is easy or appears earlier within this deck.


## EN→RU · 3000→3500

Source: [deck_15260260.csv](../english_russian/deck_15260260.csv)

### Card 1: mixture → смесь

- Question example: The soup is a smooth mixture.
- Answer example: Суп - это гладкая смесь.
- **Fix · 2:** “Гладкая смесь” copies English smooth and is a bad food-texture model. Simplify to “This is a mixture / Это смесь”, or use однородная with a matching gloss/context.
- **Sequence · 3:** Vocabulary outside the allowed earlier-deck inventory: soup (EN; first headword band 3000→3500); smooth (EN; first headword band 3000→3500); суп (RU; first headword band 3000→3500); гладкая (RU; first headword band 3000→3500). Simplify the example using previously introduced words. Same-band vocabulary fails the requested rule even when it is easy or appears earlier within this deck.

### Card 2: potato → картошка

- Question example: I have a potato in my garden.
- Answer example: У меня в саду есть картошка.
- **Improve · 2:** English “a potato” implies one tuber; Russian “есть картошка” often means potatoes growing there. Make number and intended garden context explicit on both sides.

### Card 3: melody → мелодия

- Question example: The melody sounds in my head.
- Answer example: Мелодия звучит в моей голове.
- **Improve · 2:** “The melody sounds in my head” is unnatural English. Use “I hear a melody / Я слышу мелодию”.

### Card 4: tasty → вкусный

- Question example: The soup looks very tasty.
- Answer example: Суп выглядит очень вкусным.
- **Sequence · 3:** Vocabulary outside the allowed earlier-deck inventory: soup (EN; first headword band 3000→3500); суп (RU; first headword band 3000→3500). Simplify the example using previously introduced words. Same-band vocabulary fails the requested rule even when it is easy or appears earlier within this deck.

### Card 5: sixty → шестьдесят

- Question example: She turned sixty today.
- Answer example: Ей исполнилось шестьдесят сегодня.
- **Sequence · 3:** Vocabulary outside the allowed earlier-deck inventory: исполнилось (RU; first headword band 3000→3500). Simplify the example using previously introduced words. Same-band vocabulary fails the requested rule even when it is easy or appears earlier within this deck.

### Card 9: bureau → бюро

- Question example: I contacted the bureau.
- Answer example: Я связался с бюро.
- **Sequence · 3:** Vocabulary outside the allowed earlier-deck inventory: связался (RU; first headword band 3000→3500). Simplify the example using previously introduced words. Same-band vocabulary fails the requested rule even when it is easy or appears earlier within this deck.

### Card 14: fine → штраф

- Question example: He received a fine for speed.
- Answer example: Он получил штраф за скорость.
- **Fix · 2:** “A fine for speed / штраф за скорость” omits the offense. Normally “a fine for speeding / штраф за превышение скорости”; for simpler vocabulary use “He paid a fine / Он заплатил штраф”.

### Card 15: Spanish → испанский

- Question example: I learn Spanish this year.
- Answer example: Я учу испанский в этом году.
- **Fix · 2:** “I learn Spanish this year” needs the ongoing tense: “I am learning Spanish this year”.

### Card 19: Volga → Волга

- Question example: The Volga flows through the land.
- Answer example: Волга течёт через землю.
- **Fix · 2:** “Волга течёт через землю” sounds like flowing through soil rather than across a territory. Use “Волга — река / The Volga is a river”.

### Card 23: lunar → лунный

- Question example: The lunar landscape is beautiful.
- Answer example: Лунный пейзаж красивый.
- **Sequence · 3:** Vocabulary outside the allowed earlier-deck inventory: landscape (EN; first headword band 3000→3500); пейзаж (RU; first headword band 3000→3500). Simplify the example using previously introduced words. Same-band vocabulary fails the requested rule even when it is easy or appears earlier within this deck.


## EN→RU · 3500→4000

Source: [deck_15260263.csv](../english_russian/deck_15260263.csv)

### Card 4: portion → порция

- Question example: She has a small portion.
- Answer example: У неё небольшая порция.
- **Sequence · 3:** Vocabulary outside the allowed earlier-deck inventory: небольшая (RU; absent as a headword in this pack). Simplify the example using previously introduced words. Same-band vocabulary fails the requested rule even when it is easy or appears earlier within this deck.

### Card 13: academic → академический

- Question example: She pursued an academic career.
- Answer example: Она стремилась к академической карьере.
- **Fix · 2:** “Pursued an academic career” describes engaging in that career; “стремилась к” only says she aspired to it. Align with “She wanted an academic career / Она хотела академическую карьеру”.

### Card 14: hesitate → колебаться

- Question example: Don't hesitate to ask.
- Answer example: Не колеблись спросить.
- **Fix · 2:** “Колеблись” is a valid imperative, but “Не колеблись спросить” is an unnatural construction/calque in contemporary usage. A natural translation of this English idiom is “Не стесняйся спросить”, which would miss колебаться. Preserve the target with “He hesitated / Он колебался”.

### Card 16: pierce → пробить

- Question example: The arrow will pierce the door.
- Answer example: Стрела пробьёт дверь.
- **Sequence · 3:** Vocabulary outside the allowed earlier-deck inventory: стрела (RU; absent as a headword in this pack). Simplify the example using previously introduced words. Same-band vocabulary fails the requested rule even when it is easy or appears earlier within this deck.

### Card 18: startle → вздрогнуть

- Question example: The loud noise startled me.
- Answer example: Громкий шум заставил меня вздрогнуть.
- **Improve · 2:** “Startle → вздрогнуть” is valid for the intransitive English sense. This example instead uses transitive “startled me”; its causative Russian translation is correct, but a matching intransitive example would teach the listed pair more directly. [Merriam-Webster](https://www.merriam-webster.com/dictionary/startle).

### Card 19: inspection → осмотр

- Question example: The car passed the inspection successfully.
- Answer example: Автомобиль успешно прошёл осмотр.
- **Sequence · 3:** Vocabulary outside the allowed earlier-deck inventory: автомобиль (RU; absent as a headword in this pack). Simplify the example using previously introduced words. Same-band vocabulary fails the requested rule even when it is easy or appears earlier within this deck.

### Card 21: therapy → терапия

- Question example: She started therapy last month.
- Answer example: Она начала терапию в прошлом месяце.
- **Sequence · 3:** Vocabulary outside the allowed earlier-deck inventory: прошлом (RU; absent as a headword in this pack). Simplify the example using previously introduced words. Same-band vocabulary fails the requested rule even when it is easy or appears earlier within this deck.

### Card 22: ethnic → этнический

- Question example: They celebrated their ethnic heritage proudly.
- Answer example: Они гордо отмечали своё этническое наследие.
- **Fix · 2:** “Отмечали своё этническое наследие” is a calque of celebrate heritage. Use “They are proud of their ethnic heritage / Они гордятся своим этническим наследием”, or simplify further for vocabulary.
- **Sequence · 3:** Vocabulary outside the allowed earlier-deck inventory: heritage (EN; first headword band 3500→4000); proudly (EN; first headword band 3500→4000); наследие (RU; first headword band 3500→4000). Simplify the example using previously introduced words. Same-band vocabulary fails the requested rule even when it is easy or appears earlier within this deck.


## EN→RU · 4000→4500

Source: [deck_15260266.csv](../english_russian/deck_15260266.csv)

### Card 5: to proclaim → заявить

- Question example: He wants to proclaim the truth.
- Answer example: Он хочет заявить правду.
- **Fix · 2:** “Заявить правду” is a bad collocation for proclaim the truth. Choose a natural announcement context and corresponding Russian, e.g. proclaim victory / провозгласить победу.

### Card 7: removal → удаление

- Question example: They need the removal of the table.
- Answer example: Им нужно удаление стола.
- **Improve · 2:** “Им нужно удаление стола” is bureaucratic and unnatural for moving furniture. Use a concrete context where удаление naturally means removal, or a simpler “Удаление необходимо / Removal is necessary”.

### Card 17: traction → тяга

- Question example: The engine has strong traction.
- Answer example: У двигателя сильная тяга.
- **Fix · 1, 2:** Engine тяга is normally “thrust” or pulling force; English traction normally concerns grip. A vehicle/road traction example or a revised gloss is needed.

### Card 23: sheet → простыня

- Question example: I wash the sheet.
- Answer example: Я мою простыню.
- **Fix · 2:** Laundry is стирать: “Я стираю простыню / I wash the sheet”. “Мою простыню” teaches the wrong washing verb for ordinary laundry.

### Card 24: formally → формально

- Question example: He formally accepted the offer.
- Answer example: Он формально принял предложение.
- **Improve · 1, 2:** The pair is valid in some contexts, but “формально принял” can suggest acceptance merely in form, whereas the English can mean officially. Specify the intended sense; официально is clearer for official acceptance. [Cambridge](https://dictionary.cambridge.org/dictionary/english-russian/formally).


## EN→RU · 4500→5000

Source: [deck_15260268.csv](../english_russian/deck_15260268.csv)

### Card 5: giant → гигант

- Question example: The giant towered over the trees.
- Answer example: Гигант возвышался над деревьями.
- **Sequence · 3:** Vocabulary outside the allowed earlier-deck inventory: возвышался (RU; first headword band 4500→5000). Simplify the example using previously introduced words. Same-band vocabulary fails the requested rule even when it is easy or appears earlier within this deck.

### Card 9: verbal → словесный

- Question example: He prefers verbal instructions.
- Answer example: Он предпочитает словесные инструкции.
- **Sequence · 3:** Vocabulary outside the allowed earlier-deck inventory: инструкции (RU; absent as a headword in this pack). Simplify the example using previously introduced words. Same-band vocabulary fails the requested rule even when it is easy or appears earlier within this deck.

### Card 15: intercept → перехватить

- Question example: The player intercepts the letter.
- Answer example: Игрок перехватывает письмо.
- **Improve · 2:** “The player intercepts the letter” is an odd scene without a game narrative. Use a ball or a non-player subject, keeping both faces aligned.
- **Consistency · 4:** The example uses an aspect partner: перехватить → перехватывает (перехватывать). Meaning is related, so this is not a messenger/bearer substitution. For strict practice of the exact listed lemma, rewrite the example with that lemma; ordinary tense/case inflections are accepted.

### Card 17: composite → составной

- Question example: The bridge uses composite materials.
- Answer example: Мост использует составные материалы.
- **Fix · 1, 2:** Technical composite materials are “композитные материалы”, not simply составные. Also “Мост использует” personifies the bridge awkwardly. Choose a true component/composite sense and rebuild both sides.

### Card 20: crystal → кристалл

- Question example: The crystal sparkled in the sun.
- Answer example: Кристалл искрился на солнце.
- **Sequence · 3:** Vocabulary outside the allowed earlier-deck inventory: искрился (RU; absent as a headword in this pack). Simplify the example using previously introduced words. Same-band vocabulary fails the requested rule even when it is easy or appears earlier within this deck.


## EN→RU · 5000→5500

Source: [deck_15260269.csv](../english_russian/deck_15260269.csv)

### Card 18: brightness → яркость

- Question example: The brightness of the sun is strong.
- Answer example: Яркость солнца сильная.
- **Fix · 2:** “Яркость солнца сильная” / “brightness … is strong” are poor collocations. Use “Яркость высокая / The brightness is high”, or a concrete brightness-control example.

### Card 20: cheerful → бодрый

- Question example: She looks cheerful today.
- Answer example: Она выглядит бодрой сегодня.
- **Improve · 1:** Бодрый emphasizes vigor/alertness; cheerful emphasizes a happy mood. “Cheerful” can overlap, but весёлый is a cleaner target for the current context; otherwise change the English sense explicitly.


## EN→RU · 5500→6000

Source: [deck_15260272.csv](../english_russian/deck_15260272.csv)

### Card 6: sensor → датчик

- Question example: The sensor detected motion.
- Answer example: Датчик обнаружил движение.
- **Sequence · 3:** Vocabulary outside the allowed earlier-deck inventory: motion (EN; absent as a headword in this pack). Simplify the example using previously introduced words. Same-band vocabulary fails the requested rule even when it is easy or appears earlier within this deck.

### Card 14: to come true → свершиться

- Question example: My dream came true.
- Answer example: Моя мечта свершилась.
- **Fix · 1, 2:** A dream “сбывается”, not “свершается”. Use “to come true → сбыться”; “My dream came true / Моя мечта сбылась”.

### Card 16: commandant → комендант

- Question example: The commandant issued a strict order.
- Answer example: Комендант строго приказал.
- **Improve · 2:** “Issued a strict order” and “строго приказал” move strictness from the order to the manner of commanding. Simpler: “The commandant gave an order / Комендант отдал приказ”.


## EN→RU · 6000→6500

Source: [deck_15260277.csv](../english_russian/deck_15260277.csv)

### Card 7: feline → кошачий

- Question example: Her feline nature is clear.
- Answer example: Её кошачья природа ясна.
- **Improve · 2:** “Her feline nature is clear / Её кошачья природа ясна” is vague and artificial. Use a concrete feline feature, such as eyes.

### Card 9: sweetness → сладость

- Question example: The cake's sweetness was strong.
- Answer example: Сладость торта была сильной.
- **Fix · 2:** “Сладость … была сильной” is a poor collocation. Use “I like the cake's sweetness / Мне нравится сладость торта”.

### Card 16: impudence → наглость

- Question example: His impudence was clear.
- Answer example: Его наглость была ясной.
- **Fix · 2:** “Его наглость была ясной” is unnatural. Use “His impudence surprised me / Его наглость меня удивила”.

### Card 19: oddity → странность

- Question example: His behavior was an oddity.
- Answer example: Его поведение было странностью.
- **Improve · 2:** “His behavior was an oddity” is stilted and may characterize the behavior as an object. A concrete noticed oddity is clearer: “I noticed an oddity / Я заметил странность”.


## EN→RU · 6500→7000

Source: [deck_15260280.csv](../english_russian/deck_15260280.csv)

### Card 7: to get hooked → зацепиться

- Question example: She quickly got hooked on the idea.
- Answer example: Она быстро зацепилась за идею.
- **Fix · 1, 2:** “Got hooked on the idea” suggests becoming fascinated; “зацепилась за идею” suggests seizing on it. Use a literal snagging context for зацепиться or change the Russian target for the fascination sense.

### Card 8: biologist → биолог

- Question example: The biologist studies animals.
- Answer example: Биолог изучает животных.
- **Sequence · 3:** Vocabulary outside the allowed earlier-deck inventory: изучает (RU; absent as a headword in this pack). Simplify the example using previously introduced words. Same-band vocabulary fails the requested rule even when it is easy or appears earlier within this deck.

### Card 11: humility → смирение

- Question example: She showed humility after defeat.
- Answer example: Она проявила смирение после поражения.
- **Sequence · 3:** Vocabulary outside the allowed earlier-deck inventory: проявила (RU; absent as a headword in this pack). Simplify the example using previously introduced words. Same-band vocabulary fails the requested rule even when it is easy or appears earlier within this deck.

### Card 13: crust → корка

- Question example: The bread has a hard crust.
- Answer example: У хлеба твёрдая корка.
- **Sequence · 3:** Vocabulary outside the allowed earlier-deck inventory: твёрдая (RU; absent as a headword in this pack). Simplify the example using previously introduced words. Same-band vocabulary fails the requested rule even when it is easy or appears earlier within this deck.

### Card 19: socket → розетка

- Question example: Put the plug into the socket.
- Answer example: Вставьте вилку в розетку.
- **Sequence · 3:** Vocabulary outside the allowed earlier-deck inventory: plug (EN; first headword band 6500→7000). Simplify the example using previously introduced words. Same-band vocabulary fails the requested rule even when it is easy or appears earlier within this deck. The existing same-band “to plug → заткнуть” is also a different sense from the electrical noun plug.

### Card 21: nobility → благородство

- Question example: Her act showed nobility.
- Answer example: Её поступок показал благородство.
- **Sequence · 3:** Vocabulary outside the allowed earlier-deck inventory: поступок (RU; absent as a headword in this pack). Simplify the example using previously introduced words. Same-band vocabulary fails the requested rule even when it is easy or appears earlier within this deck.


## EN→RU · 7000→7500

Source: [deck_15260281.csv](../english_russian/deck_15260281.csv)

### Card 7: calculus → исчисление

- Question example: I need calculus at university.
- Answer example: Мне нужно исчисление в университете.
- **Fix · 1, 2:** The university subject “calculus” needs “математический анализ” or specified дифференциальное/интегральное исчисление. Bare исчисление is too broad in the example.

### Card 9: combat commander → комбат

- Question example: The combat commander led the attack.
- Answer example: Комбат вёл атаку.
- **Fix · 1:** Комбат is “battalion commander”, not generic “combat commander”. Correct the English headword and example. Dictionary confirmation: [Gramota](https://gramota.ru/poisk?mode=all&query=%D0%BA%D0%BE%D0%BC%D0%B1%D0%B0%D1%82).

### Card 15: byte → байт

- Question example: A byte stores one character.
- Answer example: Байт хранит один символ.
- **Fix · 2:** “A byte stores one character” is not generally true: characters can occupy multiple bytes. Use “A byte has eight bits / В байте восемь бит”.

### Card 18: soften → смягчить

- Question example: Heat can often soften butter.
- Answer example: Тепло часто может смягчить масло.
- **Fix · 2:** For butter, размягчить is more natural than смягчить. Preserve смягчить with a natural context such as “soften the blow / смягчить удар”.
- **Sequence · 3:** Vocabulary outside the allowed earlier-deck inventory: butter (EN; absent as a headword in this pack). Simplify the example using previously introduced words. Same-band vocabulary fails the requested rule even when it is easy or appears earlier within this deck.


## EN→RU · 7500→8000

Source: [deck_15260282.csv](../english_russian/deck_15260282.csv)

### Card 10: to cough → кашлять

- Question example: He tried not to cough loudly.
- Answer example: Он старался не кашлять громко.
- **Sequence · 3:** Vocabulary outside the allowed earlier-deck inventory: старался (RU; absent as a headword in this pack). Simplify the example using previously introduced words. Same-band vocabulary fails the requested rule even when it is easy or appears earlier within this deck.

### Card 19: to be fixed → фиксироваться

- Question example: The rate will be fixed tomorrow.
- Answer example: Ставка будет фиксироваться завтра.
- **Improve · 2:** “The rate will be fixed tomorrow” implies a set result; “будет фиксироваться” emphasizes the process/repetition. Use a present repeated-recording example or explicitly align the aspect.

### Card 23: sewerage → канализация

- Question example: The city has a sewerage system.
- Answer example: В городе есть канализационная система.
- **Fix · 4:** The target noun канализация never appears: канализационная is a derived adjective, not an inflection. Use “В городе есть канализация / The city has sewerage”.
- **Sequence · 3:** Vocabulary outside the allowed earlier-deck inventory: канализационная (RU; absent as a headword in this pack). Simplify the example using previously introduced words. Same-band vocabulary fails the requested rule even when it is easy or appears earlier within this deck.


## EN→RU · 8000→8500

Source: [deck_15260283.csv](../english_russian/deck_15260283.csv)

### Card 1: to overcome → одолевать

- Question example: I try to overcome fear.
- Answer example: Я стараюсь одолевать страх.
- **Sequence · 3:** Vocabulary outside the allowed earlier-deck inventory: стараюсь (RU; absent as a headword in this pack). Simplify the example using previously introduced words. Same-band vocabulary fails the requested rule even when it is easy or appears earlier within this deck.

### Card 6: concentratedly → сосредоточенно

- Question example: She worked concentratedly.
- Answer example: Она работала сосредоточенно.
- **Improve · 1, 2:** “Concentratedly” is highly unnatural as an everyday vocabulary headword/example. Prefer “with concentration / сосредоточенно” and align the example; this requires a headword change.

### Card 7: to take care → беречься

- Question example: Please take care.
- Answer example: Пожалуйста, берегись.
- **Fix · 1, 2:** Standalone “Берегись!” usually means “Watch out!/Beware!”; polite “Please take care” usually means “Береги себя”. The current pairing confuses these speech acts.

### Card 22: membership → членство

- Question example: His membership is over.
- Answer example: Его членство кончилось.
- **Improve · 2:** “His membership is over / Его членство кончилось” is clumsy. “His membership ended / Его членство закончилось” is a cleaner simple model.

### Card 23: frenziedly → бешено

- Question example: She danced frenziedly.
- Answer example: Она бешено танцевала.
- **Improve · 2:** “Frenziedly” is awkward for an everyday example even though it is a real word. Prefer a more idiomatic adverb or phrase and explicitly align the gloss.


## EN→RU · 8500→9000

Source: [deck_15260285.csv](../english_russian/deck_15260285.csv)

### Card 2: marathon → марафон

- Question example: I ran a marathon last year.
- Answer example: Я пробежал марафон в прошлом году.
- **Sequence · 3:** Vocabulary outside the allowed earlier-deck inventory: прошлом (RU; absent as a headword in this pack). Simplify the example using previously introduced words. Same-band vocabulary fails the requested rule even when it is easy or appears earlier within this deck.

### Card 7: elegance → изящество

- Question example: Her dress has elegance.
- Answer example: В её платье есть изящество.
- **Improve · 2:** “Her dress has elegance / В её платье есть изящество” is stilted. Use “I admire its elegance / Я восхищаюсь его изяществом”, or another short natural sentence after checking vocabulary.

### Card 20: zodiac → зодиак

- Question example: I know my zodiac.
- Answer example: Я знаю свой зодиак.
- **Fix · 1, 2:** “My zodiac / свой зодиак” confuses the zodiac with a zodiac sign. Keep zodiac with “The zodiac has twelve signs / У зодиака двенадцать знаков”, or change the target to “zodiac sign / знак зодиака”.

### Card 24: get into the swing → разыграться

- Question example: She will get into the swing soon.
- Answer example: Она скоро разыграется.
- **Fix · 1, 2:** The English idiom is normally “get into the swing of things”, not bare “get into the swing”. Разыграться needs a playing/warming-up context. Complete and contextualize the phrase or change the gloss.


## EN→RU · 9000→9500

Source: [deck_15260287.csv](../english_russian/deck_15260287.csv)

### Card 2: to be paid → оплачиваться

- Question example: This work is to be paid soon.
- Answer example: Эта работа скоро будет оплачиваться.
- **Fix · 2:** “This work is to be paid soon” and “будет оплачиваться” are awkward for a one-off payment. Preserve оплачиваться using “This work is paid for / Эта работа оплачивается”.

### Card 8: rummage → порыться

- Question example: I will rummage through the attic.
- Answer example: Я хочу порыться на чердаке.
- **Fix · 2:** “I will rummage” states a future action; “Я хочу порыться” says I want to. Use “Я пороюсь на чердаке” or add “want to” on the English side.

### Card 9: get used to → привыкнуть

- Question example: You will get used to the cold.
- Answer example: Ты привыкнешь к холоду.
- **Sequence · 3:** Vocabulary outside the allowed earlier-deck inventory: холоду (RU; absent as a headword in this pack). Simplify the example using previously introduced words. Same-band vocabulary fails the requested rule even when it is easy or appears earlier within this deck.

### Card 10: most holy → пресвятой

- Question example: This is a most holy place.
- Answer example: Это пресвятое место.
- **Fix · 2:** “Пресвятое место” is a poor generic collocation; пресвятой is predominantly an elevated religious epithet. Use a genuine religious expression and its established English equivalent.

### Card 18: International → интернационал

- Question example: They sing the International.
- Answer example: Они поют Интернационал.
- **Fix · 1, 2:** The song is normally called “The Internationale” in English, not “the International”. Correct the song headword/example, or choose an actual international-organization sense and matching Russian.


## EN→RU · 9500→10000

Source: [deck_22976521.csv](../english_russian/deck_22976521.csv)

### Card 4: possessed, obsessed → одержимый

- Question example: She seemed possessed by a strange energy.
- Answer example: Она казалась одержимой странной энергией.
- **Improve · 2:** “Possessed by a strange energy” is vague and figurative. A concrete obsession/possession example would teach the selected sense more clearly.

### Card 8: to stretch, to tighten → натягивать

- Question example: I will stretch the cloth.
- Answer example: Я натяну ткань.
- **Consistency · 4:** The example uses an aspect partner: натягивать → натяну (натянуть). Meaning is related, so this is not a messenger/bearer substitution. For strict practice of the exact listed lemma, rewrite the example with that lemma; ordinary tense/case inflections are accepted.

### Card 10: relief, terrain → рельеф

- Question example: The mountain relief is high.
- Answer example: Рельеф горы высокий.
- **Fix · 2:** “The mountain relief is high / Рельеф горы высокий” is a poor technical collocation. Use “The terrain is uneven / Рельеф неровный”, with the corresponding sense selected in the gloss.

### Card 15: tight, stiff → тугой

- Question example: The screw is too tight.
- Answer example: Винт слишком тугой.
- **Improve · 2:** “Винт слишком тугой” is less clear than a tight lid/door/rope context. Choose a natural noun with тугой and mirror it in English.

### Card 17: dissolve, disperse → растворяться

- Question example: Sugar will dissolve in water quickly.
- Answer example: Сахар быстро растворится в воде.
- **Fix · 1:** “Disperse” is not a reliable interchangeable gloss for растворяться; dissolution and dispersion differ. Keep “dissolve” for the sugar example.
- **Consistency · 4:** The example uses an aspect partner: растворяться → растворится (раствориться). Meaning is related, so this is not a messenger/bearer substitution. For strict practice of the exact listed lemma, rewrite the example with that lemma; ordinary tense/case inflections are accepted.

### Card 23: scarf, shawl → шарф

- Question example: She put on a warm scarf.
- Answer example: Она надела тёплый шарф.
- **Fix · 1:** “Shawl” is normally шаль, not шарф. Keep “scarf” for this card.

## Accepted cases and limits

- Inflections such as пойду/идёт where appropriate, plural nouns, and case forms do not automatically fail target use. Feminine воспитанницей for воспитанник is accepted as a gender counterpart; use a male example if literal lemma identity is required.
- “suite → свита” is a valid dictionary sense, so it was not labeled a mistranslation. [Merriam-Webster, suite](https://www.merriam-webster.com/dictionary/suite).
- “комбат” was checked against the definition “commander of a battalion”. [Gramota, комбат](https://gramota.ru/poisk?mode=all&query=%D0%BA%D0%BE%D0%BC%D0%B1%D0%B0%D1%82).
- RU→EN приведение → reduction/bringing and EN→RU ghost → привидение are different valid targets in the files reviewed; the former was not treated as a ghost-translation typo.
- A valid selected sense is acceptable even when other senses exist. Short natural fragments are not automatically errors.
- This is a sample audit, not a review of the remaining 19,000 cards, and it establishes nothing about the live Brainscape state.
