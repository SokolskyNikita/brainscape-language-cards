import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from russian_english._chunk_io import rewrite_chunk

print(
    rewrite_chunk(
        Path("russian_english/_chunks/deck_15260198_01.csv"),
        {
            "биография": (
                "biography",
                "Я читал его биографию.",
                "I read his biography.",
            ),
            "отверстие": (
                "hole",
                "В стене есть отверстие.",
                "There is a hole in the wall.",
            ),
            "экспертиза": (
                "examination",
                "Нужна экспертиза дома.",
                "The house needs an examination.",
            ),
            "гордый": ("proud", "Он гордый отец.", "He is a proud father."),
            "рюкзак": ("backpack", "Где мой рюкзак?", "Where is my backpack?"),
            "строение": (
                "building, structure",
                "Это старое строение.",
                "This is an old building.",
            ),
            "кружка": ("mug, cup", "Дай мне кружку.", "Give me a mug."),
            "ноутбук": ("laptop", "Я купил новый ноутбук.", "I bought a new laptop."),
            "поклонник": (
                "admirer, fan",
                "У неё есть поклонник.",
                "She has an admirer.",
            ),
            "покончить": (
                "put an end to, finish",
                "Покончи с этим.",
                "Put an end to this.",
            ),
            "травма": (
                "injury, trauma",
                "У него травма руки.",
                "He has an injury of the hand.",
            ),
            "скучный": (
                "boring, dull",
                "Этот фильм скучный.",
                "This movie is boring.",
            ),
            "крутить": ("twist, spin", "Не крути это.", "Don't twist this."),
            "стремительно": (
                "rapidly, swiftly",
                "Он стремительно растёт.",
                "He grows rapidly.",
            ),
            "сорвать": (
                "pluck, tear off",
                "Он сорвал цветок.",
                "He plucked a flower.",
            ),
            "ежедневный": (
                "daily, everyday",
                "Это моя ежедневная работа.",
                "This is my daily work.",
            ),
            "адмирал": (
                "admiral",
                "Адмирал ждёт нас.",
                "The admiral waits for us.",
            ),
            "походить": (
                "resemble, look like",
                "Ты походишь на отца.",
                "You resemble your father.",
            ),
            "прислушиваться": (
                "listen, heed",
                "Я прислушиваюсь к нему.",
                "I listen to him.",
            ),
            "аж": ("even, as much as", "Он ждал аж час.", "He even waited an hour."),
            "дура": ("fool, idiot", "Она полная дура.", "She is a complete fool."),
            "обязать": (
                "obligate, compel",
                "Его обязали ждать.",
                "They obligated him to wait.",
            ),
            "бедро": ("thigh, hip", "У меня болит бедро.", "My thigh hurts."),
            "потомок": (
                "descendant, offspring",
                "Он потомок царя.",
                "He is a descendant of the tsar.",
            ),
            "операционный": (
                "surgical, operational",
                "Это операционный стол.",
                "This is a surgical table.",
            ),
            "отнять": (
                "take away, subtract",
                "Он отнял у меня книгу.",
                "He took away my book.",
            ),
            "осветить": (
                "illuminate, light up",
                "Солнце осветило комнату.",
                "The sun illuminated the room.",
            ),
            "слон": ("elephant", "Слон очень большой.", "The elephant is very big."),
            "полезть": (
                "climb, crawl",
                "Он полез на дерево.",
                "He climbed the tree.",
            ),
            "предусматривать": (
                "provide for, stipulate",
                "Закон предусматривает это.",
                "The law provides for this.",
            ),
            "печатный": (
                "printed",
                "Это печатный текст.",
                "This is printed text.",
            ),
            "любовный": (
                "love, amorous",
                "Это любовное письмо.",
                "This is a love letter.",
            ),
            "непрерывный": (
                "continuous, uninterrupted",
                "Это непрерывный шум.",
                "This is continuous noise.",
            ),
            "панель": ("panel", "Сними эту панель.", "Take off this panel."),
            "сдача": ("change, surrender", "Сдачи не надо.", "Keep the change."),
            "патрон": (
                "cartridge",
                "У него нет патронов.",
                "He has no cartridges.",
            ),
            "интеллигенция": (
                "intelligentsia",
                "Интеллигенция была против.",
                "The intelligentsia was against it.",
            ),
            "магический": (
                "magical, magic",
                "Это магический момент.",
                "This is a magical moment.",
            ),
            "приступ": (
                "attack, bout",
                "У него приступ боли.",
                "He has an attack of pain.",
            ),
            "феномен": (
                "phenomenon",
                "Это странный феномен.",
                "This is a strange phenomenon.",
            ),
            "пароль": ("password", "Я забыл пароль.", "I forgot the password."),
            "отечество": (
                "fatherland, motherland",
                "Он любит отечество.",
                "He loves the fatherland.",
            ),
            "гениальный": (
                "brilliant, genius",
                "Это гениальная идея.",
                "This is a brilliant idea.",
            ),
            "забирать": (
                "take away, collect",
                "Он забирает мои вещи.",
                "He takes away my things.",
            ),
            "рассылка": (
                "mailing, newsletter",
                "Рассылка уже готова.",
                "The mailing is already ready.",
            ),
            "полноценный": (
                "full, complete",
                "Это полноценный обед.",
                "This is a full meal.",
            ),
            "печаль": (
                "sorrow, sadness",
                "Её печаль глубока.",
                "Her sorrow is deep.",
            ),
            "опора": ("support, prop", "Ты моя опора.", "You are my support."),
            "освещение": (
                "lighting, illumination",
                "Освещение здесь плохое.",
                "The lighting here is bad.",
            ),
            "пейзаж": (
                "landscape, scenery",
                "Какой красивый пейзаж.",
                "What a beautiful landscape.",
            ),
            "печатать": ("type, print", "Я печатаю письмо.", "I type a letter."),
            "совершенство": (
                "perfection, excellence",
                "Это почти совершенство.",
                "This is almost perfection.",
            ),
            "кончаться": (
                "end, finish",
                "Фильм уже кончается.",
                "The movie is already ending.",
            ),
            "боевик": (
                "action movie, thriller",
                "Давай посмотрим боевик.",
                "Let's watch an action movie.",
            ),
            "овладеть": (
                "master, take control of",
                "Она овладеет языком.",
                "She will master the language.",
            ),
            "снаружи": ("outside", "Подожди снаружи.", "Wait outside."),
            "заглядывать": (
                "look in, peek",
                "Он заглядывает к нам.",
                "He looks in on us.",
            ),
            "речка": (
                "stream, small river",
                "Речка совсем рядом.",
                "The stream is right nearby.",
            ),
            "совокупность": (
                "totality, aggregate",
                "В совокупности это много.",
                "In totality this is a lot.",
            ),
            "торговец": (
                "merchant, trader",
                "Торговец продаёт хлеб.",
                "The merchant sells bread.",
            ),
            "пиджак": ("jacket, blazer", "Надень пиджак.", "Put on the jacket."),
            "величество": (
                "majesty",
                "Её величество здесь.",
                "Her majesty is here.",
            ),
            "каша": (
                "porridge, cereal",
                "Каша ещё горячая.",
                "The porridge is still hot.",
            ),
            "жажда": (
                "thirst, craving",
                "У меня сильная жажда.",
                "I have a strong thirst.",
            ),
            "космонавт": (
                "cosmonaut, astronaut",
                "Космонавт уже дома.",
                "The cosmonaut is already home.",
            ),
            "пехота": (
                "infantry",
                "Пехота идёт в город.",
                "The infantry goes to the city.",
            ),
            "драка": ("fight, brawl", "Там была драка.", "There was a fight there."),
            "фашистский": (
                "fascist",
                "Это фашистский режим.",
                "This is a fascist regime.",
            ),
            "диагноз": (
                "diagnosis",
                "Диагноз ещё не ясен.",
                "The diagnosis is not clear yet.",
            ),
            "стесняться": (
                "be shy, be embarrassed",
                "Не стесняйся меня.",
                "Don't be shy with me.",
            ),
            "земельный": (
                "land",
                "Это земельный вопрос.",
                "This is a land question.",
            ),
            "вытекать": (
                "flow out, leak out",
                "Вода вытекает отсюда.",
                "Water flows out from here.",
            ),
            "сводиться": (
                "come down to, boil down to",
                "Всё сводится к этому.",
                "It all comes down to this.",
            ),
            "иллюстрация": (
                "illustration, picture",
                "Смотри эту иллюстрацию.",
                "Look at this illustration.",
            ),
            "сводить": (
                "bring together, reduce",
                "Мы сводим их вместе.",
                "We bring them together.",
            ),
            "мысленно": (
                "mentally",
                "Я мысленно согласился.",
                "I mentally agreed.",
            ),
            "возрождение": (
                "revival, renaissance",
                "Это возрождение города.",
                "This is a revival of the city.",
            ),
            "частый": (
                "frequent, common",
                "Он частый гость.",
                "He is a frequent guest.",
            ),
            "завоевать": (
                "conquer, win",
                "Они завоевали город.",
                "They conquered the city.",
            ),
            "ежегодно": (
                "annually, yearly",
                "Мы ездим туда ежегодно.",
                "We go there annually.",
            ),
            "следом": ("after, behind", "Иди следом за мной.", "Go after me."),
            "раздаваться": (
                "be heard, sound",
                "Звук раздаётся снова.",
                "The sound is heard again.",
            ),
            "сибирский": (
                "Siberian",
                "Это сибирский холод.",
                "This is Siberian cold.",
            ),
            "солидный": (
                "respectable, solid",
                "Он солидный человек.",
                "He is a respectable man.",
            ),
            "порыв": (
                "gust, impulse",
                "Сильный порыв ветра.",
                "A strong gust of wind.",
            ),
            "обновление": (
                "update, renewal",
                "Нужно обновление системы.",
                "We need a system update.",
            ),
            "кошмар": (
                "nightmare, horror",
                "Какой ужасный кошмар.",
                "What a terrible nightmare.",
            ),
            "композиция": (
                "composition, arrangement",
                "Его композиция хорошая.",
                "His composition is good.",
            ),
            "сотовый": (
                "mobile, cellular",
                "Где мой сотовый?",
                "Where is my mobile?",
            ),
            "интеграция": (
                "integration",
                "Интеграция ещё идёт.",
                "The integration is still going.",
            ),
            "исключать": (
                "exclude, eliminate",
                "Не исключай меня.",
                "Don't exclude me.",
            ),
            "преимущественно": (
                "primarily, predominantly",
                "Он преимущественно дома.",
                "He is primarily at home.",
            ),
            "гуманитарный": (
                "humanitarian",
                "Это гуманитарная помощь.",
                "This is humanitarian aid.",
            ),
            "натуральный": (
                "natural, organic",
                "Это натуральный цвет.",
                "This is a natural color.",
            ),
            "хитрый": ("cunning, sly", "Он очень хитрый.", "He is very cunning."),
            "застать": (
                "find, catch",
                "Я застал его дома.",
                "I found him at home.",
            ),
            "проезд": (
                "fare, passage",
                "Проезд стоит дорого.",
                "The fare is expensive.",
            ),
            "решающий": (
                "decisive, determining",
                "Это решающий момент.",
                "This is a decisive moment.",
            ),
            "диапазон": (
                "range, spectrum",
                "Какой широкий диапазон.",
                "What a wide range.",
            ),
            "предпочтение": (
                "preference",
                "Моё предпочтение — чай.",
                "My preference is tea.",
            ),
        },
    )
)
