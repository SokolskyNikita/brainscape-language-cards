import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from russian_english._chunk_io import rewrite_chunk

print(
    rewrite_chunk(
        Path("russian_english/_chunks/deck_15260217_01.csv"),
        {
            "пробел": (
                "space, gap",
                "Тут есть пробел.",
                "There is a space here.",
            ),
            "себестоимость": (
                "cost price, prime cost",
                "Себестоимость слишком высокая.",
                "The cost price is too high.",
            ),
            "форт": (
                "fort, fortress",
                "Форт стоит на холме.",
                "The fort stands on the hill.",
            ),
            "эстетика": (
                "aesthetics, esthetics",
                "Мне нравится эта эстетика.",
                "I like the aesthetics.",
            ),
            "сворачивать": (
                "to fold, to roll up",
                "Я сворачиваю письмо.",
                "I fold the letter.",
            ),
            "духовенство": (
                "clergy, clergyman",
                "Духовенство собралось в церкви.",
                "The clergy gathered in the church.",
            ),
            "помещик": (
                "landowner, nobleman",
                "Помещик жил в деревне.",
                "The landowner lived in the village.",
            ),
            "приписать": (
                "attribute, ascribe",
                "Ему приписали победу.",
                "They attributed the victory to him.",
            ),
            "эгоизм": (
                "egoism, selfishness",
                "Это чистый эгоизм.",
                "This is pure selfishness.",
            ),
            "пахать": (
                "to plow, to work hard",
                "Он пашет поле.",
                "He plows the field.",
            ),
            "драйвер": (
                "driver, software driver",
                "Нужен новый драйвер.",
                "We need a new driver.",
            ),
            "терапевт": (
                "general practitioner",
                "Я был у терапевта.",
                "I saw the general practitioner.",
            ),
            "скачок": (
                "jump, leap",
                "Цены сделали скачок.",
                "Prices made a jump.",
            ),
            "гавань": (
                "harbor, haven",
                "Корабль вошёл в гавань.",
                "The ship entered the harbor.",
            ),
            "земский": (
                "provincial",
                "Земский врач приехал.",
                "The provincial doctor arrived.",
            ),
            "цельный": (
                "solid, whole",
                "Это цельный кусок.",
                "This is a whole piece.",
            ),
            "затихнуть": (
                "subside, quiet down",
                "Шум наконец затих.",
                "The noise finally quieted down.",
            ),
            "вселенский": (
                "universal, ecumenical",
                "Это вселенская правда.",
                "This is a universal truth.",
            ),
            "неприличный": (
                "indecent, improper",
                "Это неприличный вопрос.",
                "That's an indecent question.",
            ),
            "числиться": (
                "to be listed, to be registered",
                "Он числится на работе.",
                "He is listed at work.",
            ),
            "угощать": (
                "treat, regale",
                "Я угощу тебя чаем.",
                "I'll treat you to tea.",
            ),
            "идиотский": (
                "idiotic, stupid",
                "Это идиотский план.",
                "That's an idiotic plan.",
            ),
            "духовно": (
                "spiritually, spiritually-minded",
                "Она духовно сильна.",
                "She is spiritually strong.",
            ),
            "затмение": (
                "eclipse, occultation",
                "Сегодня будет затмение.",
                "There will be an eclipse today.",
            ),
            "первенство": (
                "championship, primacy",
                "Мы выиграли первенство.",
                "We won the championship.",
            ),
            "опередить": (
                "overtake, outstrip",
                "Я тебя опережу.",
                "I will overtake you.",
            ),
            "толковый": (
                "sensible, explanatory",
                "Он толковый парень.",
                "He is a sensible guy.",
            ),
            "ловкий": (
                "skillful, agile",
                "Он ловкий парень.",
                "He is a skillful guy.",
            ),
            "оппозиционный": (
                "oppositional, opposition",
                "Это оппозиционная газета.",
                "This is an opposition newspaper.",
            ),
            "оккупировать": (
                "occupy",
                "Враги оккупировали город.",
                "The enemy occupied the city.",
            ),
            "насильственный": (
                "violent, forcible",
                "Это насильственное преступление.",
                "This is a violent crime.",
            ),
            "нажатие": (
                "press, push",
                "Одно нажатие кнопки.",
                "One press of the button.",
            ),
            "дежурить": (
                "to be on duty, to stand watch",
                "Я дежурю сегодня.",
                "I am on duty today.",
            ),
            "сменяться": (
                "to change, to alternate",
                "Дни быстро сменяются.",
                "The days change quickly.",
            ),
            "скоростной": (
                "high-speed, rapid",
                "Это скоростной поезд.",
                "This is a high-speed train.",
            ),
            "опоздание": (
                "delay, lateness",
                "Прости за опоздание.",
                "Sorry for the delay.",
            ),
            "переодеться": (
                "change clothes, get changed",
                "Мне надо переодеться.",
                "I need to change clothes.",
            ),
            "скудный": (
                "meager, scanty",
                "У нас скудный ужин.",
                "We have a meager dinner.",
            ),
            "барин": (
                "master, lord",
                "Барин вышел во двор.",
                "The master went out to the yard.",
            ),
            "обеспечиваться": (
                "to be provided, to be ensured",
                "Питание обеспечивается.",
                "Food is provided.",
            ),
            "диабет": (
                "diabetes, diabetes mellitus",
                "У неё диабет.",
                "She has diabetes.",
            ),
            "воистину": (
                "truly, indeed",
                "Это воистину так.",
                "This is truly so.",
            ),
            "страж": (
                "guard, sentinel",
                "Страж стоял у ворот.",
                "The guard stood at the gate.",
            ),
            "ступня": (
                "foot, sole",
                "У меня болит ступня.",
                "My foot hurts.",
            ),
            "съедать": (
                "to eat up, to consume",
                "Он съедает всё.",
                "He eats up everything.",
            ),
            "си": (
                "B, si",
                "Сыграй си ещё раз.",
                "Play B again.",
            ),
            "раскол": (
                "schism, split",
                "В партии произошёл раскол.",
                "A split happened in the party.",
            ),
            "предсказывать": (
                "predict, forecast",
                "Он предсказывает дождь.",
                "He predicts rain.",
            ),
            "обхватить": (
                "embrace, encompass",
                "Она обхватила его шею.",
                "She embraced his neck.",
            ),
            "злоупотребление": (
                "abuse, misuse",
                "Это злоупотребление властью.",
                "This is an abuse of power.",
            ),
            "монарх": (
                "monarch, sovereign",
                "Монарх вышел к народу.",
                "The monarch went out to the people.",
            ),
            "магистраль": (
                "main line, trunk line",
                "Поезд идёт по магистрали.",
                "The train goes on the main line.",
            ),
            "сугроб": (
                "snowdrift, snow bank",
                "Возле дома лежит сугроб.",
                "There is a snowdrift near the house.",
            ),
            "корейский": (
                "Korean",
                "Это корейский фильм.",
                "This is a Korean movie.",
            ),
            "девиз": (
                "motto, slogan",
                "Наш девиз простой.",
                "Our motto is simple.",
            ),
            "прилив": (
                "tide, high tide",
                "Скоро будет прилив.",
                "The tide will come soon.",
            ),
            "стихнуть": (
                "subside, abate",
                "Ветер стих.",
                "The wind subsided.",
            ),
            "копирование": (
                "copying, duplication",
                "Копирование запрещено.",
                "Copying is forbidden.",
            ),
            "беззащитный": (
                "defenseless, vulnerable",
                "Ребёнок был беззащитен.",
                "The child was defenseless.",
            ),
            "побледнеть": (
                "to turn pale, to blanch",
                "Она побледнела от страха.",
                "She turned pale from fear.",
            ),
            "кавалер": (
                "gentleman, cavalier",
                "Он настоящий кавалер.",
                "He is a true gentleman.",
            ),
            "стопка": (
                "shot glass, stack",
                "Налей стопку.",
                "Pour a shot glass.",
            ),
            "распространиться": (
                "spread, disseminate",
                "Слух быстро распространился.",
                "The rumor spread quickly.",
            ),
            "адресат": (
                "addressee, recipient",
                "Кто адресат письма?",
                "Who is the addressee of the letter?",
            ),
            "прошлогодний": (
                "last year's, last-year's",
                "Это прошлогодний снег.",
                "This is last year's snow.",
            ),
            "соус": (
                "sauce, gravy",
                "Добавь соус к мясу.",
                "Add sauce to the meat.",
            ),
            "обыкновение": (
                "habit, custom",
                "У него такое обыкновение.",
                "He has such a habit.",
            ),
            "поморщиться": (
                "to wince, to grimace",
                "Он поморщился от боли.",
                "He winced from the pain.",
            ),
            "суверенитет": (
                "sovereignty, autonomy",
                "Страна защищает суверенитет.",
                "The country defends its sovereignty.",
            ),
            "неформальный": (
                "informal, casual",
                "Это неформальный ужин.",
                "This is an informal dinner.",
            ),
            "веранда": (
                "veranda, porch",
                "Мы сидели на веранде.",
                "We sat on the veranda.",
            ),
            "рифма": (
                "rhyme, rime",
                "В стихе нет рифмы.",
                "There is no rhyme in the verse.",
            ),
            "малость": (
                "a bit, a little",
                "Подожди малость.",
                "Wait a bit.",
            ),
            "пробраться": (
                "sneak in, infiltrate",
                "Мы пробрались в дом.",
                "We sneaked in.",
            ),
            "менталитет": (
                "mentality, mindset",
                "У них другой менталитет.",
                "They have another mentality.",
            ),
            "ноздря": (
                "nostril, naris",
                "У него болит ноздря.",
                "His nostril hurts.",
            ),
            "вонючий": (
                "smelly, stinky",
                "Какой вонючий сыр.",
                "What smelly cheese.",
            ),
            "лабораторный": (
                "laboratory, lab",
                "Это лабораторная работа.",
                "This is laboratory work.",
            ),
            "распределять": (
                "distribute, allocate",
                "Она распределяет работу.",
                "She distributes the work.",
            ),
            "ухватиться": (
                "grab, seize",
                "Он ухватился за край.",
                "He grabbed the edge.",
            ),
            "выпрямиться": (
                "straighten up, straighten",
                "Он сразу выпрямился.",
                "He straightened up at once.",
            ),
            "обрывок": (
                "fragment, snippet",
                "Я нашёл обрывок бумаги.",
                "I found a fragment of paper.",
            ),
            "призвание": (
                "calling, vocation",
                "Это моё призвание.",
                "This is my calling.",
            ),
            "необыкновенно": (
                "extraordinarily, exceptionally",
                "Она необыкновенно красива.",
                "She is extraordinarily beautiful.",
            ),
            "интегрировать": (
                "integrate, incorporate",
                "Нужно интегрировать эту систему.",
                "We need to integrate this system.",
            ),
            "пластмассовый": (
                "plastic, plastic-made",
                "Это пластмассовая ложка.",
                "This is a plastic spoon.",
            ),
            "казахстанский": (
                "Kazakhstani, Kazakh",
                "Это казахстанский фильм.",
                "This is a Kazakhstani movie.",
            ),
            "перевернуться": (
                "to overturn, to flip over",
                "Лодка перевернулась.",
                "The boat overturned.",
            ),
            "дивизион": (
                "division, divisional",
                "Дивизион стоит здесь.",
                "The division stands here.",
            ),
            "опереться": (
                "to lean on, to rely on",
                "Он опёрся на стол.",
                "He leaned on the table.",
            ),
            "возглас": (
                "exclamation, outcry",
                "Раздался громкий возглас.",
                "A loud exclamation sounded.",
            ),
            "па": (
                "dad, pa",
                "Па, посмотри сюда.",
                "Dad, look here.",
            ),
            "попугай": (
                "parrot, parakeet",
                "Попугай сидит в клетке.",
                "The parrot sits in the cage.",
            ),
            "останки": (
                "remains, relics",
                "Здесь нашли останки.",
                "They found remains here.",
            ),
            "трансляция": (
                "broadcast, transmission",
                "Трансляция уже началась.",
                "The broadcast already started.",
            ),
            "рейд": (
                "raid, raiding party",
                "Полиция провела рейд.",
                "The police made a raid.",
            ),
            "отличительный": (
                "distinctive, distinguishing",
                "Это его отличительный знак.",
                "This is his distinctive mark.",
            ),
            "притягивать": (
                "attract, pull",
                "Она притягивает внимание.",
                "She attracts attention.",
            ),
            "прозрачность": (
                "transparency, clarity",
                "Нам нужна прозрачность.",
                "We need transparency.",
            ),
            "исповедь": (
                "confession, confession of faith",
                "Он шёл на исповедь.",
                "He went to confession.",
            ),
        },
    )
)
