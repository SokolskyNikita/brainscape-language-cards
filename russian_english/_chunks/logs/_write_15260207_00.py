import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from russian_english._chunk_io import rewrite_chunk

print(
    rewrite_chunk(
        Path("russian_english/_chunks/deck_15260207_00.csv"),
        {
            "дизайнер": (
                "designer, stylist",
                "Она наняла дизайнера.",
                "She hired a designer.",
            ),
            "бег": ("run, running", "Я люблю бег.", "I love running."),
            "дырка": ("hole, gap", "В стене дырка.", "There's a hole in the wall."),
            "начинающий": (
                "beginner, novice",
                "Она начинающая.",
                "She is a beginner.",
            ),
            "причём": (
                "moreover, what's more",
                "Он опоздал, причём не позвонил.",
                "He was late; moreover, he didn't call.",
            ),
            "бухгалтер": (
                "accountant, bookkeeper",
                "Спроси бухгалтера.",
                "Ask the accountant.",
            ),
            "констатировать": (
                "to state, to note",
                "Он констатировал факт.",
                "He stated the fact.",
            ),
            "преследование": (
                "persecution, pursuit",
                "Это преследование.",
                "This is persecution.",
            ),
            "подбор": ("selection, choice", "Долгий подбор.", "A long selection."),
            "совершаться": (
                "to occur, to take place",
                "Церемония совершается.",
                "The ceremony is taking place.",
            ),
            "спецслужба": (
                "intelligence agency",
                "Спецслужба нашла его.",
                "The intelligence agency found him.",
            ),
            "хлопнуть": (
                "to clap, to bang",
                "Он хлопнул дверью.",
                "He banged the door.",
            ),
            "проследить": (
                "track, monitor",
                "Я прослежу за этим.",
                "I'll track this.",
            ),
            "вмешаться": (
                "intervene, interfere",
                "Он вмешался в спор.",
                "He intervened in the argument.",
            ),
            "туристический": (
                "tourist, touristic",
                "Туристический сезон.",
                "Tourist season.",
            ),
            "ясность": ("clarity, clearness", "Нужна ясность.", "We need clarity."),
            "блондинка": ("blonde, blond", "Она блондинка.", "She is a blonde."),
            "жопа": ("butt, ass", "Он упал на жопу.", "He fell on his butt."),
            "отстаивать": (
                "defend, insist on",
                "Они отстаивают права.",
                "They defend their rights.",
            ),
            "поразительный": (
                "amazing, astonishing",
                "Вид поразительный.",
                "The view is amazing.",
            ),
            "прописать": (
                "prescribe, register",
                "Врач прописал это.",
                "The doctor prescribed this.",
            ),
            "обитать": (
                "to inhabit, to dwell",
                "Медведи обитают в лесу.",
                "Bears inhabit the forest.",
            ),
            "довестись": (
                "to happen to",
                "Мне довелось жить там.",
                "I happened to live there.",
            ),
            "господство": (
                "dominance, supremacy",
                "Его господство кончилось.",
                "His dominance ended.",
            ),
            "загрузка": ("loading, download", "Долгая загрузка.", "Long loading."),
            "апостол": ("apostle", "Он был апостолом.", "He was an apostle."),
            "внесение": (
                "introduction, contribution",
                "Внесение изменений.",
                "The introduction of changes.",
            ),
            "инфекция": (
                "infection, contagion",
                "У него инфекция.",
                "He has an infection.",
            ),
            "галактика": ("galaxy", "Галактика далеко.", "The galaxy is far."),
            "спичка": ("match, matchstick", "Дай спичку.", "Give me a match."),
            "электроэнергия": (
                "electricity, electric power",
                "Нет электроэнергии.",
                "There's no electricity.",
            ),
            "интерьер": (
                "interior, decor",
                "Интерьер простой.",
                "The interior is simple.",
            ),
            "портить": ("spoil, ruin", "Не порти день.", "Don't spoil the day."),
            "устранение": (
                "elimination, removal",
                "Устранение ошибки.",
                "Elimination of the error.",
            ),
            "мучительный": (
                "torturous, agonizing",
                "Мучительный день.",
                "A torturous day.",
            ),
            "аль": ("or", "Аль ты устал?", "Or are you tired?"),
            "договариваться": (
                "to agree, to arrange",
                "Давай договариваться.",
                "Let's agree.",
            ),
            "облегчить": (
                "relieve, alleviate",
                "Это облегчит боль.",
                "This will relieve the pain.",
            ),
            "полоска": ("stripe, strip", "Синяя полоска.", "A blue stripe."),
            "русло": ("channel, bed", "Русло реки.", "The river bed."),
            "вал": ("shaft, embankment", "Высокий вал.", "A high embankment."),
            "взлететь": (
                "to take off, to soar",
                "Птица взлетела.",
                "The bird took off.",
            ),
            "предпосылка": (
                "premise, precondition",
                "Плохая предпосылка.",
                "A bad premise.",
            ),
            "отделять": (
                "to separate, to detach",
                "Отделяй это.",
                "Separate this.",
            ),
            "холл": ("hall, lobby", "Жди в холле.", "Wait in the hall."),
            "босс": ("boss, chief", "Где босс?", "Where's the boss?"),
            "предлог": (
                "pretext, preposition",
                "Это только предлог.",
                "That's only a pretext.",
            ),
            "олимпийский": (
                "Olympic, Olympian",
                "Олимпийские игры.",
                "The Olympic Games.",
            ),
            "шевелиться": ("to move, to stir", "Не шевелись.", "Don't move."),
            "водиться": (
                "to be found, to live",
                "В лесу водятся волки.",
                "Wolves live in the forest.",
            ),
            "воровать": ("to steal, to thieve", "Не воруй.", "Don't steal."),
            "извиняться": (
                "to apologize, to excuse oneself",
                "Я извиняюсь.",
                "I apologize.",
            ),
            "заговор": (
                "conspiracy, plot",
                "Это заговор.",
                "That's a conspiracy.",
            ),
            "предпринимать": (
                "to undertake, to embark on",
                "Что предпринимать?",
                "What to undertake?",
            ),
            "служение": ("ministry, service", "Её служение.", "Her ministry."),
            "пройтись": ("walk, stroll", "Пройдёмся?", "Shall we walk?"),
            "просторный": (
                "spacious, roomy",
                "Дом просторный.",
                "The house is spacious.",
            ),
            "распространять": (
                "spread, disseminate",
                "Не распространяй слухи.",
                "Don't spread rumors.",
            ),
            "всячески": (
                "in every way, in every possible way",
                "Он всячески помогает.",
                "He helps in every way.",
            ),
            "сочувствие": (
                "sympathy, compassion",
                "Моё сочувствие.",
                "My sympathy.",
            ),
            "всероссийский": (
                "all-Russian, nationwide",
                "Всероссийский конкурс.",
                "An all-Russian competition.",
            ),
            "поворачивать": (
                "to turn, to rotate",
                "Поворачивай сюда.",
                "Turn this way.",
            ),
            "суета": ("vanity, fuss", "Какая суета.", "What a fuss."),
            "евангелие": ("Gospel", "Читай евангелие.", "Read the Gospel."),
            "шумный": ("noisy, loud", "Шумный дом.", "A noisy house."),
            "погодить": ("wait a bit, hold on", "Погоди.", "Wait a bit."),
            "предстать": (
                "to appear, to stand before",
                "Он предстанет перед судом.",
                "He will appear in court.",
            ),
            "статистический": (
                "statistical",
                "Статистический факт.",
                "A statistical fact.",
            ),
            "остро": ("sharply, keenly", "Он остро сказал.", "He said it sharply."),
            "уговаривать": (
                "to persuade, to coax",
                "Не уговаривай меня.",
                "Don't persuade me.",
            ),
            "ничтожный": (
                "insignificant, negligible",
                "Ничтожный шанс.",
                "An insignificant chance.",
            ),
            "подчинить": (
                "subjugate, subordinate",
                "Они хотят подчинить нас.",
                "They want to subjugate us.",
            ),
            "эскадрилья": (
                "squadron, air squadron",
                "Эскадрилья в небе.",
                "The squadron is in the sky.",
            ),
            "медик": ("medic, medical worker", "Медик здесь.", "The medic is here."),
            "ревность": ("jealousy, envy", "Это ревность.", "That's jealousy."),
            "трещина": ("crack, fissure", "Трещина в стене.", "A crack in the wall."),
            "намереваться": (
                "intend, plan",
                "Я намереваюсь уйти.",
                "I intend to leave.",
            ),
            "недра": ("depths, bowels", "Недра богаты.", "The depths are rich."),
            "зам": ("deputy", "Где зам?", "Where's the deputy?"),
            "камин": (
                "fireplace, hearth",
                "У камина тепло.",
                "It's warm by the fireplace.",
            ),
            "предъявлять": (
                "to present, to produce",
                "Он предъявляет паспорт.",
                "He presents his passport.",
            ),
            "противостояние": (
                "confrontation, standoff",
                "Долгое противостояние.",
                "A long confrontation.",
            ),
            "экспертный": (
                "expert, expert-level",
                "Экспертный совет.",
                "Expert advice.",
            ),
            "прилавок": (
                "counter, showcase",
                "Она у прилавка.",
                "She is at the counter.",
            ),
            "продвигаться": (
                "to progress, to advance",
                "Мы продвигаемся.",
                "We are progressing.",
            ),
            "гад": ("villain, scoundrel", "Он гад.", "He's a villain."),
            "франк": ("franc", "Один франк.", "One franc."),
            "линейный": ("linear, line", "Линейный рост.", "Linear growth."),
            "протекать": ("leak, flow", "Труба протекает.", "The pipe leaks."),
            "мотоцикл": (
                "motorcycle, motorbike",
                "Его мотоцикл.",
                "His motorcycle.",
            ),
            "доброта": ("kindness, goodness", "Его доброта.", "His kindness."),
            "сталинский": (
                "Stalinist, Stalin's",
                "Сталинский дом.",
                "A Stalinist house.",
            ),
            "накопление": (
                "accumulation, buildup",
                "Накопление снега.",
                "Accumulation of snow.",
            ),
            "престижный": (
                "prestigious",
                "Престижный дом.",
                "A prestigious house.",
            ),
            "скука": ("boredom, tedium", "Какая скука.", "What boredom."),
            "тропинка": ("path, trail", "Узкая тропинка.", "A narrow path."),
            "шина": ("tire, busbar", "Нужна новая шина.", "I need a new tire."),
            "подполковник": (
                "lieutenant colonel, lieutenant-colonel",
                "Он подполковник.",
                "He's a lieutenant colonel.",
            ),
            "батюшка": ("father, priest", "Батюшка дома.", "Father is home."),
            "бесконечность": (
                "infinity, infinitude",
                "До бесконечности.",
                "To infinity.",
            ),
        },
    )
)
