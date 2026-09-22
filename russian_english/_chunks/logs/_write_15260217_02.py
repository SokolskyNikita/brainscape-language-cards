import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from russian_english._chunk_io import rewrite_chunk

print(
    rewrite_chunk(
        Path("russian_english/_chunks/deck_15260217_02.csv"),
        {
            "травка": (
                "grass, weed",
                "Травка уже выросла.",
                "The grass already grew.",
            ),
            "разразиться": (
                "burst out, erupt",
                "Он разразился смехом.",
                "He burst out laughing.",
            ),
            "конвой": (
                "convoy, escort",
                "Конвой шёл медленно.",
                "The convoy went slowly.",
            ),
            "кумир": (
                "idol, icon",
                "Он мой кумир.",
                "He is my idol.",
            ),
            "футболист": (
                "footballer, soccer player",
                "Он хороший футболист.",
                "He is a good footballer.",
            ),
            "древесина": (
                "wood, timber",
                "Стол из древесины.",
                "The table is wood.",
            ),
            "мостовая": (
                "pavement, cobblestone",
                "Мостовая мокрая.",
                "The pavement is wet.",
            ),
            "выходец": (
                "native, someone from",
                "Он выходец из деревни.",
                "He is a native of the village.",
            ),
            "невиданный": (
                "unprecedented, unseen",
                "Это невиданный случай.",
                "This is an unprecedented case.",
            ),
            "должник": (
                "debtor, borrower",
                "Должник не платит.",
                "The debtor does not pay.",
            ),
            "искусственно": (
                "artificially, synthetically",
                "Это сделано искусственно.",
                "This is done artificially.",
            ),
            "бешенство": (
                "rabies, fury",
                "Он был в бешенстве.",
                "He was in a fury.",
            ),
            "обрадовать": (
                "to gladden, to delight",
                "Это обрадует маму.",
                "This will delight mom.",
            ),
            "бархатный": (
                "velvety, velvet",
                "У неё бархатный голос.",
                "She has a velvety voice.",
            ),
            "подверженный": (
                "susceptible, prone",
                "Он подвержен болезням.",
                "He is prone to illness.",
            ),
            "всматриваться": (
                "peer, scrutinize",
                "Я всматриваюсь в темноту.",
                "I peer into the dark.",
            ),
            "бесшумно": (
                "noiselessly, silently",
                "Он бесшумно вошёл.",
                "He entered noiselessly.",
            ),
            "совокупный": (
                "aggregate, total",
                "Совокупный доход вырос.",
                "The total income grew.",
            ),
            "увлекать": (
                "to fascinate, to captivate",
                "Книга увлекает меня.",
                "The book fascinates me.",
            ),
            "инвестировать": (
                "invest, invest in",
                "Я хочу инвестировать.",
                "I want to invest.",
            ),
            "педаль": (
                "pedal, treadle",
                "Нажми на педаль.",
                "Press the pedal.",
            ),
            "раскрыться": (
                "to open up, to unfold",
                "Цветок раскрылся.",
                "The flower opened up.",
            ),
            "здороваться": (
                "to greet, to say hello",
                "Мы всегда здороваемся.",
                "We always greet each other.",
            ),
            "правдивый": (
                "truthful, honest",
                "Он правдивый человек.",
                "He is a truthful person.",
            ),
            "подсчитать": (
                "calculate, count",
                "Я подсчитаю сумму.",
                "I will calculate the sum.",
            ),
            "внушить": (
                "inspire, instill",
                "Его слова внушили страх.",
                "His words instilled fear.",
            ),
            "выборка": (
                "sample, selection",
                "Это большая выборка.",
                "This is a large sample.",
            ),
            "зрачок": (
                "pupil",
                "Зрачок большой.",
                "The pupil is large.",
            ),
            "деваться": (
                "to go, to disappear",
                "Куда он девался?",
                "Where did he disappear to?",
            ),
            "бродяга": (
                "vagabond, tramp",
                "Он жил как бродяга.",
                "He lived as a vagabond.",
            ),
            "бесценный": (
                "priceless, invaluable",
                "Этот дар бесценный.",
                "This gift is priceless.",
            ),
            "наставление": (
                "instruction",
                "Следуй моему наставлению.",
                "Follow my instruction.",
            ),
            "новосибирский": (
                "Novosibirsk",
                "Это новосибирский поезд.",
                "This is a Novosibirsk train.",
            ),
            "расстроиться": (
                "get upset, be disappointed",
                "Она расстроилась.",
                "She got upset.",
            ),
            "атеист": (
                "atheist, nonbeliever",
                "Он атеист.",
                "He is an atheist.",
            ),
            "доводиться": (
                "happen to, be related as",
                "Он мне доводится дядей.",
                "He happens to be my uncle.",
            ),
            "хмыкнуть": (
                "snort, chuckle",
                "Он только хмыкнул.",
                "He only snorted.",
            ),
            "повозка": (
                "cart, wagon",
                "Повозка стоит у дома.",
                "The cart stands by the house.",
            ),
            "бонус": (
                "bonus, reward",
                "Он получил бонус.",
                "He received a bonus.",
            ),
            "шут": (
                "jester, fool",
                "Шут смеялся.",
                "The jester laughed.",
            ),
            "неверно": (
                "incorrectly, wrong",
                "Ты ответил неверно.",
                "You answered incorrectly.",
            ),
            "рыть": (
                "dig, burrow",
                "Он роет яму.",
                "He is digging a hole.",
            ),
            "сбиться": (
                "get lost, stray",
                "Мы сбились с пути.",
                "We got lost.",
            ),
            "попутно": (
                "incidentally, en route",
                "Попутно купи хлеб.",
                "Incidentally, buy bread.",
            ),
            "примечательный": (
                "notable, remarkable",
                "Это примечательный случай.",
                "This is a notable case.",
            ),
            "карета": (
                "carriage, coach",
                "Карета ждала у дома.",
                "The carriage waited by the house.",
            ),
            "гаишник": (
                "traffic policeman, road cop",
                "Гаишник остановил машину.",
                "The traffic policeman stopped the car.",
            ),
            "подразумеваться": (
                "to be implied, to be understood",
                "Это подразумевается.",
                "This is implied.",
            ),
            "переправа": (
                "ferry, crossing",
                "Переправа через реку закрыта.",
                "The crossing over the river is closed.",
            ),
            "возвышенный": (
                "exalted, sublime",
                "У него возвышенный стиль.",
                "He has an exalted style.",
            ),
            "состязание": (
                "competition, contest",
                "Состязание начнётся завтра.",
                "The competition starts tomorrow.",
            ),
            "спец": (
                "specialist, spec",
                "Нам нужен спец.",
                "We need a specialist.",
            ),
            "подчиниться": (
                "to obey, to submit",
                "Он подчинился приказу.",
                "He obeyed the order.",
            ),
            "возмутить": (
                "disturb, outrage",
                "Это меня возмутило.",
                "This outraged me.",
            ),
            "сторонний": (
                "external, third-party",
                "Это сторонний человек.",
                "This is an external person.",
            ),
            "уродливый": (
                "ugly, hideous",
                "Этот дом уродливый.",
                "This house is ugly.",
            ),
            "спутниковый": (
                "satellite",
                "У нас спутниковое телевидение.",
                "We have satellite television.",
            ),
            "вылечить": (
                "to cure, to heal",
                "Врач хочет вылечить его.",
                "The doctor wants to cure him.",
            ),
            "прогнозировать": (
                "to forecast, to predict",
                "Трудно прогнозировать погоду.",
                "It is hard to forecast the weather.",
            ),
            "присоединение": (
                "accession, annexation",
                "Присоединение прошло быстро.",
                "The accession went quickly.",
            ),
            "унаследовать": (
                "inherit",
                "Она унаследует дом.",
                "She will inherit the house.",
            ),
            "стаканчик": (
                "cup, glass",
                "Дай мне стаканчик.",
                "Give me a cup.",
            ),
            "смуглый": (
                "swarthy, dark-skinned",
                "У него смуглое лицо.",
                "He has a swarthy face.",
            ),
            "ураган": (
                "hurricane, typhoon",
                "Идёт сильный ураган.",
                "A strong hurricane is coming.",
            ),
            "зараза": (
                "infection, pest",
                "Эта зараза везде.",
                "This infection is everywhere.",
            ),
            "фишка": (
                "chip, token",
                "Поставь фишку сюда.",
                "Put the chip here.",
            ),
            "целесообразность": (
                "expediency, advisability",
                "В этом есть целесообразность.",
                "There is expediency in this.",
            ),
            "преобразовать": (
                "transform, convert",
                "Он хочет преобразовать город.",
                "He wants to transform the city.",
            ),
            "стойкий": (
                "resilient, steadfast",
                "Он стойкий человек.",
                "He is a resilient person.",
            ),
            "отслеживать": (
                "to track, to monitor",
                "Мы отслеживаем заказ.",
                "We track the order.",
            ),
            "эфирный": (
                "ethereal, etheric",
                "У неё эфирный голос.",
                "She has an ethereal voice.",
            ),
            "изгнание": (
                "exile, banishment",
                "Он жил в изгнании.",
                "He lived in exile.",
            ),
            "черепаха": (
                "turtle, tortoise",
                "Черепаха ползёт медленно.",
                "The turtle crawls slowly.",
            ),
            "челябинский": (
                "Chelyabinsk",
                "Это челябинский завод.",
                "This is a Chelyabinsk plant.",
            ),
            "обменяться": (
                "exchange, swap",
                "Мы обменяемся местами.",
                "We will swap places.",
            ),
            "уткнуться": (
                "to bury, to stick",
                "Он уткнулся в книгу.",
                "He buried himself in the book.",
            ),
            "копировать": (
                "copy, duplicate",
                "Не копируй мою работу.",
                "Don't copy my work.",
            ),
            "неприязнь": (
                "antipathy, aversion",
                "У неё неприязнь к нему.",
                "She has an aversion to him.",
            ),
            "праведный": (
                "righteous, just",
                "Он праведный человек.",
                "He is a righteous man.",
            ),
            "мафия": (
                "mafia, mob",
                "Мафия правит городом.",
                "The mafia rules the city.",
            ),
            "катушка": (
                "reel, bobbin",
                "Катушка упала.",
                "The reel fell.",
            ),
            "крестный": (
                "godfather",
                "Он мой крестный.",
                "He is my godfather.",
            ),
            "сшить": (
                "to sew, to stitch",
                "Она сшила платье.",
                "She sewed a dress.",
            ),
            "док": (
                "dock",
                "Корабль стоит в доке.",
                "The ship is in the dock.",
            ),
            "буркнуть": (
                "mutter, grumble",
                "Он буркнул что-то.",
                "He muttered something.",
            ),
            "застрелить": (
                "to shoot, to shoot dead",
                "Его застрелили.",
                "They shot him dead.",
            ),
            "кувшин": (
                "jug, pitcher",
                "Налей воду в кувшин.",
                "Pour water into the jug.",
            ),
            "вручать": (
                "to hand over, to present",
                "Ему вручают ключ.",
                "They hand over the key to him.",
            ),
            "телекомпания": (
                "television company, broadcaster",
                "Телекомпания показала кино.",
                "The television company showed a movie.",
            ),
            "тонко": (
                "thinly, finely",
                "Она тонко режет сыр.",
                "She slices the cheese thinly.",
            ),
            "греть": (
                "to warm, to heat",
                "Солнце греет землю.",
                "The sun warms the land.",
            ),
            "безобидный": (
                "harmless, innocuous",
                "Это безобидный вопрос.",
                "This is a harmless question.",
            ),
            "реактивный": (
                "jet, reactive",
                "Это реактивный двигатель.",
                "This is a jet engine.",
            ),
            "погружение": (
                "immersion, diving",
                "Погружение было глубоким.",
                "The immersion was deep.",
            ),
            "сводка": (
                "summary, report",
                "Я читаю сводку.",
                "I am reading the summary.",
            ),
            "подсудимый": (
                "defendant, accused",
                "Подсудимый молчал.",
                "The defendant was silent.",
            ),
            "незнание": (
                "ignorance, lack of knowledge",
                "Это просто незнание.",
                "This is simply ignorance.",
            ),
            "щедро": (
                "generously, liberally",
                "Он щедро дал нам хлеб.",
                "He generously gave us bread.",
            ),
            "рекламировать": (
                "advertise, promote",
                "Они рекламируют товар.",
                "They advertise the goods.",
            ),
            "шокировать": (
                "shock",
                "Это шокировало меня.",
                "This shocked me.",
            ),
        },
    )
)
