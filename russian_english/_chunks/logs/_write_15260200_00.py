from pathlib import Path

from russian_english._chunk_io import rewrite_chunk

print(
    rewrite_chunk(
        Path("russian_english/_chunks/deck_15260200_00.csv"),
    {
        "овощ": ("vegetable, veggie", "Купи свежие овощи.", "Buy fresh vegetables."),
        "противостоять": (
            "to resist, to withstand",
            "Мы должны противостоять врагу.",
            "We must resist the enemy.",
        ),
        "сновидение": (
            "dream, vision",
            "У меня было странное сновидение.",
            "I had a strange dream.",
        ),
        "виновный": (
            "guilty, culpable",
            "Он чувствовал себя виновным за ложь.",
            "He felt guilty for the lie.",
        ),
        "фокус": ("trick", "Он показал новый фокус.", "He showed a new trick."),
        "обозначать": (
            "denote, indicate",
            "Этот знак обозначает выход.",
            "This sign indicates the exit.",
        ),
        "пожарный": (
            "firefighter, fireman",
            "Пожарный бежит к дому.",
            "The firefighter runs to the house.",
        ),
        "болтать": (
            "chat, babble",
            "Мы поболтаем за чашкой чая.",
            "We'll chat over a cup of tea.",
        ),
        "проживание": (
            "residence, living",
            "Проживание здесь дорого.",
            "Residence here is expensive.",
        ),
        "связаться": (
            "to contact, to get in touch",
            "Мне нужно связаться с другом.",
            "I need to contact my friend.",
        ),
        "отражаться": (
            "to reflect, to be reflected",
            "Луна отражается в воде.",
            "The moon is reflected in the water.",
        ),
        "одевать": ("to dress", "Она одевает сына.", "She is dressing her son."),
        "симптом": (
            "symptom, sign",
            "Это симптом болезни.",
            "This is a symptom of disease.",
        ),
        "переулок": ("alley, lane", "Кот идёт по переулку.", "A cat walks down the alley."),
        "бочка": ("barrel, drum", "Бочка полна вина.", "The barrel is full of wine."),
        "одеваться": (
            "to dress, to get dressed",
            "Мне нужно одеться сейчас.",
            "I need to get dressed now.",
        ),
        "поворачиваться": (
            "to turn, to rotate",
            "Он всегда поворачивается налево.",
            "He always turns left.",
        ),
        "сомнительный": (
            "doubtful, questionable",
            "Его ответ сомнительный.",
            "His answer is doubtful.",
        ),
        "развести": (
            "divorce, dilute",
            "Разведи сок водой.",
            "Dilute the juice with water.",
        ),
        "болезненный": (
            "painful, morbid",
            "Это болезненный удар.",
            "This is a painful blow.",
        ),
        "осколок": (
            "shard, fragment",
            "Он наступил на острый осколок.",
            "He stepped on a sharp shard.",
        ),
        "регулировать": (
            "regulate, adjust",
            "Нужно регулировать воду.",
            "We need to regulate the water.",
        ),
        "ось": ("axis, axle", "Это ось колеса.", "This is the wheel's axis."),
        "тяжкий": ("heavy, hard", "У него тяжкий день.", "He has a hard day."),
        "плоскость": (
            "plane, surface",
            "Нарисуй линию на плоскости.",
            "Draw a line on the plane.",
        ),
        "раскрывать": (
            "to reveal, to disclose",
            "Не раскрывай секрет.",
            "Don't reveal the secret.",
        ),
        "закрепить": (
            "secure, fasten",
            "Закрепи картину на стене.",
            "Fasten the painting on the wall.",
        ),
        "дистанция": (
            "distance, range",
            "Держи дистанцию от огня.",
            "Keep your distance from the fire.",
        ),
        "прилететь": (
            "to arrive by air, to fly in",
            "Они прилетят завтра.",
            "They will fly in tomorrow.",
        ),
        "годовой": (
            "annual, yearly",
            "Годовой доклад уже готов.",
            "The annual report is already ready.",
        ),
        "увлечение": (
            "hobby, passion",
            "Сад — моё увлечение.",
            "The garden is my hobby.",
        ),
        "обследование": (
            "examination, survey",
            "Врач начал обследование.",
            "The doctor started the examination.",
        ),
        "дрова": (
            "firewood, logs",
            "Нам нужны дрова для печи.",
            "We need firewood for the stove.",
        ),
        "мадам": ("madam, ma'am", "Добрый вечер, мадам.", "Good evening, madam."),
        "отступить": (
            "retreat, withdraw",
            "Армия решила отступить.",
            "The army decided to retreat.",
        ),
        "терроризм": (
            "terrorism",
            "Терроризм угрожает миру.",
            "Terrorism threatens peace.",
        ),
        "респондент": (
            "respondent, survey participant",
            "Респондент заполнил опрос.",
            "The respondent filled the survey.",
        ),
        "обряд": ("rite, ceremony", "Это старый обряд.", "This is an old rite."),
        "нестись": (
            "to rush, to race",
            "Он несётся к выходу.",
            "He is rushing to the exit.",
        ),
        "видимый": (
            "visible, apparent",
            "Звёзды видимы сегодня.",
            "The stars are visible today.",
        ),
        "заря": ("dawn, twilight", "Заря уже на небе.", "Dawn is already in the sky."),
        "привязать": (
            "tie, attach",
            "Привяжи лодку к берегу.",
            "Tie the boat to the shore.",
        ),
        "издатель": (
            "publisher, editor",
            "Издатель выпустил новую книгу.",
            "The publisher released a new book.",
        ),
        "предать": ("betray", "Он предал своего друга.", "He betrayed his friend."),
        "отставка": (
            "resignation, dismissal",
            "Он объявил о своей отставке.",
            "He announced his resignation.",
        ),
        "заголовок": (
            "headline, title",
            "Заголовок в газете короткий.",
            "The headline in the newspaper is short.",
        ),
        "отступать": (
            "retreat, withdraw",
            "Армия медленно отступает.",
            "The army is slowly retreating.",
        ),
        "улучшить": (
            "improve, enhance",
            "Мы должны улучшить работу.",
            "We must improve the work.",
        ),
        "изредка": (
            "occasionally, rarely",
            "Я изредка ем яблоки.",
            "I occasionally eat apples.",
        ),
        "делегация": (
            "delegation, mission",
            "Делегация прибыла утром.",
            "The delegation arrived in the morning.",
        ),
        "трамвай": (
            "tram, streetcar",
            "Трамвай идёт в центр.",
            "The tram goes to the center.",
        ),
        "комбинация": (
            "combination, combo",
            "Это опасная комбинация.",
            "This is a dangerous combination.",
        ),
        "попросту": (
            "simply, plainly",
            "Она попросту не поняла.",
            "She simply did not understand.",
        ),
        "зависть": ("envy, jealousy", "Она чувствовала зависть.", "She felt envy."),
        "роскошный": (
            "luxurious, sumptuous",
            "Она жила в роскошном отеле.",
            "She lived in a luxurious hotel.",
        ),
        "высказаться": (
            "to express oneself, to speak out",
            "Она хотела ясно высказаться.",
            "She wanted to express herself clearly.",
        ),
        "окраина": (
            "outskirts, periphery",
            "Они живут на окраине города.",
            "They live on the outskirts of town.",
        ),
        "скучать": ("to miss, to be bored", "Я скучаю по тебе.", "I miss you."),
        "потребительский": (
            "consumer, consumerist",
            "Потребительский спрос растёт.",
            "Consumer demand grows.",
        ),
        "прохождение": (
            "passage, walkthrough",
            "Прохождение через лес заняло час.",
            "The passage through the forest took an hour.",
        ),
        "подача": (
            "supply, serve",
            "Подача воды снова работает.",
            "The water supply works again.",
        ),
        "комедия": (
            "comedy, farce",
            "Я смотрю хорошую комедию.",
            "I am watching a good comedy.",
        ),
        "экономист": (
            "economist",
            "Экономист знает рынок.",
            "The economist knows the market.",
        ),
        "парламентский": (
            "parliamentary, legislative",
            "Это парламентский вопрос.",
            "This is a parliamentary question.",
        ),
        "деревенский": (
            "rural, village",
            "Это деревенский дом.",
            "This is a rural house.",
        ),
        "специфика": (
            "specificity, peculiarity",
            "Я понял специфику дела.",
            "I understood the specificity of the matter.",
        ),
        "функционирование": (
            "functioning, operation",
            "Функционирование системы нормальное.",
            "The system's functioning is normal.",
        ),
        "выключить": (
            "turn off, switch off",
            "Пожалуйста, выключи свет.",
            "Please turn off the light.",
        ),
        "вольный": ("free, voluntary", "Он вольный человек.", "He is a free person."),
        "нота": (
            "note, musical note",
            "Она сыграла неверную ноту.",
            "She played a wrong note.",
        ),
        "ругать": ("scold, berate", "Она ругает сына.", "She scolds her son."),
        "альтернатива": (
            "alternative, option",
            "У нас нет альтернативы.",
            "We have no alternative.",
        ),
        "слышный": (
            "audible, hearable",
            "Звук едва слышен.",
            "The sound is barely audible.",
        ),
        "расстрелять": (
            "to shoot, to execute",
            "Солдаты расстреляли врага.",
            "The soldiers shot the enemy.",
        ),
        "значимость": (
            "significance, importance",
            "Значимость этого велика.",
            "The significance of this is great.",
        ),
        "женатый": (
            "married, wedded",
            "Он женат уже пять лет.",
            "He has been married for five years.",
        ),
        "обидеться": (
            "to be offended, to take offense",
            "Она обиделась на шутку.",
            "She was offended by the joke.",
        ),
        "пропадать": (
            "to disappear, to vanish",
            "Ключи вечно пропадают.",
            "The keys disappear forever.",
        ),
        "усилить": (
            "to strengthen, to intensify",
            "Мы усилили защиту.",
            "We strengthened our protection.",
        ),
        "дурацкий": ("silly, foolish", "Это дурацкая идея.", "That's a silly idea."),
        "выполняться": (
            "to be executed, to be carried out",
            "План выполняется по графику.",
            "The plan is being carried out on schedule.",
        ),
        "героиня": (
            "heroine, female hero",
            "Она героиня книги.",
            "She is the heroine of the book.",
        ),
        "девятый": ("ninth", "Он живёт на девятом этаже.", "He lives on the ninth floor."),
        "перебить": (
            "interrupt, break",
            "Не перебивай меня.",
            "Don't interrupt me.",
        ),
        "ручей": (
            "brook, stream",
            "Ручей течёт к реке.",
            "The brook flows to the river.",
        ),
        "расслабиться": ("relax, unwind", "Просто расслабься.", "Just relax."),
        "перспективный": (
            "promising, prospective",
            "Он перспективный молодой врач.",
            "He is a promising young doctor.",
        ),
        "вспыхнуть": (
            "flare up, ignite",
            "Огонь вспыхнул сразу.",
            "The fire flared up at once.",
        ),
        "гараж": ("garage, carport", "Машина в гараже.", "The car is in the garage."),
        "уступить": (
            "yield, concede",
            "Я уступил ему место.",
            "I yielded my place to him.",
        ),
        "кончать": (
            "to finish, to end",
            "Он кончает работу в шесть.",
            "He finishes work at six.",
        ),
        "тестирование": (
            "testing, test",
            "Тестирование уже началось.",
            "Testing has already started.",
        ),
        "изменяться": (
            "change, vary",
            "Погода часто изменяется.",
            "The weather often changes.",
        ),
        "ген": ("gene", "Этот ген вызывает болезнь.", "This gene causes disease."),
        "задумать": (
            "to conceive, to plan",
            "Она задумала всё заранее.",
            "She planned everything in advance.",
        ),
        "чин": ("rank, order", "Он получил высокий чин.", "He got a high rank."),
        "заполнять": (
            "to fill, to fill in",
            "Я заполняю форму.",
            "I am filling in the form.",
        ),
        "отбросить": (
            "discard, reject",
            "Отбрось эту мысль.",
            "Discard this thought.",
        ),
        "включение": (
            "inclusion, switching on",
            "Включение света всё изменило.",
            "Switching on the light changed everything.",
        ),
        "новичок": (
            "newcomer, beginner",
            "Новичок уже знает правила.",
            "The beginner already knows the rules.",
        ),
    },
    )
)

