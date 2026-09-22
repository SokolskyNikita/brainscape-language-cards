import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from russian_english._chunk_io import rewrite_chunk

print(
    rewrite_chunk(
        Path("russian_english/_chunks/deck_15260213_01.csv"),
        {
            "гарнизон": (
                "garrison",
                "Гарнизон стоит в городе.",
                "The garrison stands in the city.",
            ),
            "стукнуть": (
                "to knock, to hit",
                "Он стукнул в дверь.",
                "He knocked on the door.",
            ),
            "борец": (
                "wrestler, fighter",
                "Борец упал на землю.",
                "The wrestler fell on the ground.",
            ),
            "догадка": (
                "guess, conjecture",
                "Это только догадка.",
                "This is only a guess.",
            ),
            "зубной": (
                "dental",
                "Мне нужен зубной врач.",
                "I need a dental doctor.",
            ),
            "развалиться": (
                "fall apart, collapse",
                "Стул развалился.",
                "The chair fell apart.",
            ),
            "экономить": (
                "save, economize",
                "Надо экономить воду.",
                "We must save water.",
            ),
            "ль": (
                "whether",
                "Не знаю, дома ль он.",
                "I don't know whether he is home.",
            ),
            "абзац": (
                "paragraph",
                "Прочитай первый абзац.",
                "Read the first paragraph.",
            ),
            "наказывать": (
                "to punish, to penalize",
                "Не надо наказывать сына.",
                "Do not punish the son.",
            ),
            "взаимосвязь": (
                "interrelation, interconnection",
                "Тут явная взаимосвязь.",
                "Here is a clear interrelation.",
            ),
            "понемногу": (
                "little by little, gradually",
                "Он понемногу учит язык.",
                "He learns the language little by little.",
            ),
            "диагностика": (
                "diagnosis, diagnostics",
                "Диагностика ещё идёт.",
                "The diagnosis is still going.",
            ),
            "кратко": (
                "briefly, in brief",
                "Скажи кратко, что случилось.",
                "Say briefly what happened.",
            ),
            "тост": (
                "toast",
                "Он поднял тост.",
                "He raised a toast.",
            ),
            "превысить": (
                "exceed, surpass",
                "Он превысил скорость.",
                "He exceeded the speed.",
            ),
            "хорошенько": (
                "well, thoroughly",
                "Хорошенько подумай.",
                "Think thoroughly.",
            ),
            "силуэт": (
                "silhouette, outline",
                "Я вижу силуэт в окне.",
                "I see a silhouette in the window.",
            ),
            "милосердие": (
                "mercy, compassion",
                "Он просил милосердия.",
                "He asked for mercy.",
            ),
            "въехать": (
                "to drive in, to enter",
                "Машина въехала во двор.",
                "The car drove in.",
            ),
            "компетенция": (
                "competence, competency",
                "Это не моя компетенция.",
                "This is not my competence.",
            ),
            "благой": (
                "good, kind",
                "У него благие намерения.",
                "He has good intentions.",
            ),
            "воспроизводить": (
                "reproduce",
                "Машина воспроизводит звук.",
                "The machine reproduces the sound.",
            ),
            "мундир": (
                "uniform, tunic",
                "Офицер надел мундир.",
                "The officer put on his uniform.",
            ),
            "болтаться": (
                "dangle, swing",
                "Ключ болтается на поясе.",
                "The key dangles on the belt.",
            ),
            "архангельский": (
                "Archangelsk, Archangel",
                "Архангельский порт открыт.",
                "The Archangelsk port is open.",
            ),
            "развалины": (
                "ruins, rubble",
                "Мы стоим у развалин.",
                "We stand by the ruins.",
            ),
            "скелет": (
                "skeleton",
                "Скелет лежит в земле.",
                "The skeleton lies in the ground.",
            ),
            "чешский": (
                "Czech, Bohemian",
                "Я люблю чешское пиво.",
                "I love Czech beer.",
            ),
            "свист": (
                "whistle, whistling",
                "Я слышал свист.",
                "I heard a whistle.",
            ),
            "зловещий": (
                "sinister, ominous",
                "Это зловещий знак.",
                "This is a sinister sign.",
            ),
            "сенатор": (
                "senator",
                "Сенатор вышел к народу.",
                "The senator came out to the people.",
            ),
            "возмутиться": (
                "to be indignant, to be outraged",
                "Она возмутилась его словам.",
                "She was indignant at his words.",
            ),
            "сочувствовать": (
                "sympathize, empathize",
                "Я сочувствую тебе.",
                "I sympathize with you.",
            ),
            "привязывать": (
                "to tie, to attach",
                "Он привязывает собаку.",
                "He ties the dog.",
            ),
            "сено": (
                "hay",
                "Лошадь ест сено.",
                "The horse eats hay.",
            ),
            "обречь": (
                "doom, condemn",
                "Это обречёт нас на смерть.",
                "This will doom us to death.",
            ),
            "братство": (
                "brotherhood, fraternity",
                "Наше братство крепкое.",
                "Our brotherhood is strong.",
            ),
            "няня": (
                "nanny, babysitter",
                "Няня гуляет с сыном.",
                "The nanny walks with the son.",
            ),
            "отзываться": (
                "respond, react",
                "Почему ты не отзываешься?",
                "Why do you not respond?",
            ),
            "умеренный": (
                "moderate, temperate",
                "У нас умеренный климат.",
                "We have a moderate climate.",
            ),
            "лондонский": (
                "London, London's",
                "Лондонский поезд уже тут.",
                "The London train is already here.",
            ),
            "поклон": (
                "bow",
                "Он сделал поклон.",
                "He made a bow.",
            ),
            "дуга": (
                "arc, bow",
                "Мост имеет форму дуги.",
                "The bridge has the form of an arc.",
            ),
            "тонкость": (
                "subtlety, finesse",
                "В этом есть тонкость.",
                "There is a subtlety in this.",
            ),
            "возвратить": (
                "return",
                "Возвратите книгу завтра.",
                "Return the book tomorrow.",
            ),
            "исторически": (
                "historically",
                "Это исторически важно.",
                "This is historically important.",
            ),
            "приступать": (
                "to start",
                "Пора приступать к работе.",
                "Time to start work.",
            ),
            "отрицание": (
                "denial, negation",
                "Это полное отрицание.",
                "This is a complete denial.",
            ),
            "неблагоприятный": (
                "unfavorable, adverse",
                "Прогноз неблагоприятный.",
                "The forecast is unfavorable.",
            ),
            "внутренне": (
                "internally",
                "Он внутренне спокоен.",
                "He is internally calm.",
            ),
            "предатель": (
                "traitor, betrayer",
                "Его назвали предателем.",
                "They called him a traitor.",
            ),
            "миграция": (
                "migration",
                "Миграция птиц началась.",
                "The migration of birds began.",
            ),
            "эротический": (
                "erotic",
                "Это эротический роман.",
                "This is an erotic novel.",
            ),
            "размахивать": (
                "to wave, to brandish",
                "Он размахивает руками.",
                "He waves his arms.",
            ),
            "бывало": (
                "used to",
                "Он, бывало, сидел тут.",
                "He used to sit here.",
            ),
            "покойник": (
                "deceased, dead person",
                "Покойника похоронили вчера.",
                "They buried the deceased yesterday.",
            ),
            "авто": (
                "car, auto",
                "Вчера я купил новое авто.",
                "I bought a new car yesterday.",
            ),
            "кучка": (
                "little heap, small bunch",
                "На столе кучка бумаг.",
                "There is a little heap of paper on the table.",
            ),
            "мерседес": (
                "Mercedes, Mercedes-Benz",
                "Это мой мерседес.",
                "This is my Mercedes.",
            ),
            "густо": (
                "thickly, densely",
                "Снег идёт густо.",
                "The snow falls thickly.",
            ),
            "жечь": (
                "burn",
                "Нельзя жечь письма.",
                "You must not burn letters.",
            ),
            "издали": (
                "from afar",
                "Я узнал его издали.",
                "I recognized him from afar.",
            ),
            "селение": (
                "village, settlement",
                "Селение стоит у реки.",
                "The village stands by the river.",
            ),
            "дискотека": (
                "disco",
                "Мы идём на дискотеку.",
                "We are going to the disco.",
            ),
            "наделить": (
                "endow, bestow",
                "Его наделили властью.",
                "They endowed him with power.",
            ),
            "капитальный": (
                "major, capital",
                "Нужен капитальный ремонт.",
                "We need a major renovation.",
            ),
            "покров": (
                "cover, veil",
                "Покров снега толстый.",
                "The cover of snow is thick.",
            ),
            "несправедливый": (
                "unfair, unjust",
                "Это несправедливый суд.",
                "This is an unfair court.",
            ),
            "влечение": (
                "attraction, desire",
                "У него влечение к ней.",
                "He has an attraction to her.",
            ),
            "сломаться": (
                "break down",
                "Машина сломалась.",
                "The car broke down.",
            ),
            "стройка": (
                "construction site",
                "Стройка очень шумная.",
                "The construction site is very noisy.",
            ),
            "купе": (
                "compartment",
                "Наше купе занято.",
                "Our compartment is taken.",
            ),
            "обыватель": (
                "ordinary person",
                "Обыватель этого не поймёт.",
                "An ordinary person will not understand this.",
            ),
            "вглядываться": (
                "peer",
                "Он вглядывается в темноту.",
                "He peers into the darkness.",
            ),
            "выбежать": (
                "to run out",
                "Сын выбежал во двор.",
                "The son ran out into the yard.",
            ),
            "сожалеть": (
                "regret",
                "Я сожалею о словах.",
                "I regret the words.",
            ),
            "мертвец": (
                "corpse, dead man",
                "Мертвец лежал на земле.",
                "The corpse lay on the ground.",
            ),
            "безразличный": (
                "indifferent",
                "У него безразличный вид.",
                "He has an indifferent look.",
            ),
            "задерживаться": (
                "to linger, to be delayed",
                "Не задерживайся там.",
                "Do not linger there.",
            ),
            "разногласие": (
                "disagreement",
                "Между нами разногласие.",
                "There is a disagreement between us.",
            ),
            "выдвигать": (
                "nominate, put forward",
                "Они выдвигают его.",
                "They nominate him.",
            ),
            "современность": (
                "modernity",
                "Он не любит современность.",
                "He does not like modernity.",
            ),
            "свердловский": (
                "Sverdlovsk",
                "Это свердловский поезд.",
                "This is a Sverdlovsk train.",
            ),
            "пришелец": (
                "alien, newcomer",
                "Пришелец стоит у двери.",
                "The alien stands at the door.",
            ),
            "возрастной": (
                "age-related",
                "Это возрастной предел.",
                "This is an age-related limit.",
            ),
            "вытирать": (
                "to wipe",
                "Она вытирает стол.",
                "She wipes the table.",
            ),
            "фермер": (
                "farmer",
                "Фермер работает в поле.",
                "The farmer works in the field.",
            ),
            "разворачиваться": (
                "unfold",
                "События разворачиваются быстро.",
                "The events unfold quickly.",
            ),
            "возвышаться": (
                "to tower",
                "Гора возвышается над лесом.",
                "The mountain towers above the forest.",
            ),
            "комплимент": (
                "compliment",
                "Его комплимент был приятен.",
                "His compliment was pleasant.",
            ),
            "репортаж": (
                "report",
                "Я смотрел репортаж.",
                "I watched the report.",
            ),
            "град": (
                "hail",
                "Вчера шёл град.",
                "Hail fell yesterday.",
            ),
            "икра": (
                "caviar, roe",
                "Он ест икру.",
                "He eats caviar.",
            ),
            "жестоко": (
                "cruelly",
                "Он жестоко поступил.",
                "He acted cruelly.",
            ),
            "рывок": (
                "jerk",
                "Он сделал рывок.",
                "He made a jerk.",
            ),
            "гитлеровец": (
                "Nazi, Hitlerite",
                "Гитлеровец сдался.",
                "The Nazi surrendered.",
            ),
            "землетрясение": (
                "earthquake",
                "Землетрясение разрушило дом.",
                "The earthquake destroyed the house.",
            ),
            "вывезти": (
                "take out",
                "Мы вывезли вещи.",
                "We took out the things.",
            ),
            "казнить": (
                "execute",
                "Его казнят на рассвете.",
                "They will execute him at dawn.",
            ),
        },
    )
)
