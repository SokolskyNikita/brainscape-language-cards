import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from russian_english._chunk_io import rewrite_chunk

print(
    rewrite_chunk(
        Path("russian_english/_chunks/deck_15260217_00.csv"),
        {
            "донесение": (
                "report, dispatch",
                "Командир читает донесение.",
                "The commander reads the report.",
            ),
            "буквальный": (
                "literal",
                "Это буквальный перевод.",
                "This is a literal translation.",
            ),
            "инопланетянин": (
                "alien, extraterrestrial",
                "Мы видели инопланетянина.",
                "We saw an alien.",
            ),
            "зрелость": (
                "maturity, ripeness",
                "Зрелость приходит с опытом.",
                "Maturity comes with experience.",
            ),
            "унылый": (
                "dismal, dreary",
                "Сегодня унылая погода.",
                "The weather today is dismal.",
            ),
            "помойка": (
                "dump, garbage dump",
                "Он живёт рядом с помойкой.",
                "He lives near a dump.",
            ),
            "акула": (
                "shark",
                "Акула плыла возле пляжа.",
                "The shark swam near the beach.",
            ),
            "эмпирический": (
                "empirical",
                "Это эмпирический метод.",
                "This is an empirical method.",
            ),
            "действенный": (
                "effective",
                "Лекарство было действенным.",
                "The medicine was effective.",
            ),
            "норовить": (
                "to tend, to be inclined",
                "Он норовит спорить.",
                "He tends to argue.",
            ),
            "безупречный": (
                "flawless, impeccable",
                "Её работа безупречна.",
                "Her work is flawless.",
            ),
            "несоответствие": (
                "discrepancy, mismatch",
                "Вот несоответствие в цифрах.",
                "Here is a discrepancy in the numbers.",
            ),
            "ложа": (
                "box",
                "Мы взяли ложу в театре.",
                "We took a box at the theater.",
            ),
            "самосознание": (
                "self-awareness, self-consciousness",
                "Самосознание приходит с возрастом.",
                "Self-awareness comes with age.",
            ),
            "экспресс": (
                "express, fast train",
                "Экспресс идёт в полдень.",
                "The express goes at noon.",
            ),
            "измерить": (
                "measure, gauge",
                "Измерь длину стола.",
                "Measure the length of the table.",
            ),
            "синяк": (
                "bruise, contusion",
                "Она нашла синяк на своей руке.",
                "She found a bruise on her arm.",
            ),
            "братский": (
                "fraternal, brotherly",
                "Это братская помощь.",
                "This is fraternal help.",
            ),
            "вяло": (
                "listlessly, languidly",
                "Он вяло ответил.",
                "He answered listlessly.",
            ),
            "оптовый": (
                "wholesale, bulk",
                "Это оптовый рынок.",
                "This is a wholesale market.",
            ),
            "включиться": (
                "join, get involved",
                "Он хочет включиться в игру.",
                "He wants to join the game.",
            ),
            "дивный": (
                "wonderful, marvelous",
                "Какой дивный вечер!",
                "What a wonderful evening!",
            ),
            "позвоночник": (
                "spine, backbone",
                "У неё болит позвоночник.",
                "Her spine hurts.",
            ),
            "различить": (
                "distinguish, discern",
                "Я не могу различить лица.",
                "I cannot distinguish the faces.",
            ),
            "разгромить": (
                "defeat, rout",
                "Мы разгромили врага.",
                "We defeated the enemy.",
            ),
            "раздавить": (
                "crush, squash",
                "Не раздави паука.",
                "Do not crush the spider.",
            ),
            "представать": (
                "appear, stand before",
                "Он скоро предстанет перед судом.",
                "He will soon appear before the court.",
            ),
            "обязывать": (
                "to obligate, to bind",
                "Закон обязывает нас платить.",
                "The law binds us to pay.",
            ),
            "тематический": (
                "thematic, topical",
                "Это тематический вечер.",
                "This is a thematic evening.",
            ),
            "двоюродный": (
                "cousin",
                "Мой двоюродный брат здесь.",
                "My cousin is here.",
            ),
            "забытый": (
                "forgotten, overlooked",
                "Этот дом давно забыт.",
                "This house was long forgotten.",
            ),
            "бессмысленно": (
                "senselessly, meaninglessly",
                "Он бессмысленно смотрел в окно.",
                "He looked out the window senselessly.",
            ),
            "вражда": (
                "enmity, hostility",
                "Между ними вражда.",
                "There is enmity between them.",
            ),
            "лирика": (
                "lyric poetry, lyrics",
                "Она пишет красивую лирику.",
                "She writes beautiful lyric poetry.",
            ),
            "иномарка": (
                "foreign car, import car",
                "Он купил новую иномарку.",
                "He bought a new foreign car.",
            ),
            "звонкий": (
                "ringing, clear",
                "У неё звонкий голос.",
                "She has a ringing voice.",
            ),
            "усадить": (
                "to seat, to plant",
                "Усади гостей за стол.",
                "Seat the guests at the table.",
            ),
            "расстегнуть": (
                "unfasten, unzip",
                "Расстегни пальто.",
                "Unfasten your coat.",
            ),
            "терраса": (
                "terrace, patio",
                "Мы сидим на террасе.",
                "We sit on the terrace.",
            ),
            "конюшня": (
                "stable, stud farm",
                "Лошадь стоит в конюшне.",
                "The horse stands in the stable.",
            ),
            "заграничный": (
                "foreign, overseas",
                "У неё заграничный паспорт.",
                "She has a foreign passport.",
            ),
            "псковский": (
                "Pskov, Pskovian",
                "Я люблю псковский край.",
                "I love the Pskov region.",
            ),
            "вздрагивать": (
                "to shudder, to flinch",
                "Он вздрагивает от шума.",
                "He shudders at the noise.",
            ),
            "инновация": (
                "innovation, novelty",
                "Это важная инновация.",
                "This is an important innovation.",
            ),
            "улочка": (
                "lane, alley",
                "Мы идём по узкой улочке.",
                "We walk along a narrow lane.",
            ),
            "косяк": (
                "mistake, joint",
                "Это мой большой косяк.",
                "This is my big mistake.",
            ),
            "погон": (
                "epaulet",
                "У офицера новый погон.",
                "The officer has a new epaulet.",
            ),
            "парализовать": (
                "paralyze, immobilize",
                "Страх может парализовать вас.",
                "Fear can paralyze you.",
            ),
            "покоиться": (
                "to rest, to lie",
                "Он покоится с миром.",
                "He rests in peace.",
            ),
            "наглядно": (
                "visually, clearly",
                "Он наглядно показал ошибку.",
                "He clearly showed the error.",
            ),
            "ворчать": (
                "grumble, mutter",
                "Он ворчит с утра.",
                "He grumbles in the morning.",
            ),
            "обдумать": (
                "think over, consider",
                "Я обдумаю твоё предложение.",
                "I will think over your proposal.",
            ),
            "смущение": (
                "embarrassment, confusion",
                "Он скрыл своё смущение.",
                "He hid his embarrassment.",
            ),
            "пленник": (
                "prisoner, captive",
                "Пленник хочет свободы.",
                "The prisoner wants freedom.",
            ),
            "следование": (
                "following, compliance",
                "Следование правилам важно.",
                "Following the rules is important.",
            ),
            "дядька": (
                "uncle, guy",
                "Мой дядька живёт во дворе.",
                "My uncle lives in the yard.",
            ),
            "эль": (
                "ale, beer",
                "Он пьёт эль в баре.",
                "He drinks ale at the bar.",
            ),
            "пробегать": (
                "to run through, to skim",
                "Он любит пробегать через парк.",
                "He likes to run through the park.",
            ),
            "колоть": (
                "to prick, to sting",
                "Игла колет палец.",
                "The needle pricks the finger.",
            ),
            "весло": (
                "oar, paddle",
                "Весло упало в воду.",
                "The oar fell into the water.",
            ),
            "рис": (
                "rice",
                "Я люблю рис на ужин.",
                "I like rice for dinner.",
            ),
            "проклинать": (
                "to curse, to damn",
                "Не проклинай свою судьбу.",
                "Do not curse your fate.",
            ),
            "редактировать": (
                "edit, modify",
                "Мне нужно редактировать текст.",
                "I need to edit the text.",
            ),
            "причудливый": (
                "whimsical, fanciful",
                "Какой причудливый узор!",
                "What a whimsical pattern!",
            ),
            "подготовительный": (
                "preparatory, preparative",
                "Это подготовительный курс.",
                "This is a preparatory course.",
            ),
            "отвлекаться": (
                "to get distracted, to be distracted",
                "Не отвлекайся на уроке.",
                "Do not get distracted in class.",
            ),
            "надвигаться": (
                "approach, loom",
                "Зима надвигается тихо.",
                "Winter approaches silently.",
            ),
            "трафик": (
                "traffic, web traffic",
                "В городе большой трафик.",
                "There is heavy traffic in the city.",
            ),
            "опрокинуть": (
                "overturn, knock over",
                "Он опрокинул стул.",
                "He overturned the chair.",
            ),
            "поджидать": (
                "to wait for, to ambush",
                "Она поджидает его у двери.",
                "She waits for him at the door.",
            ),
            "соединиться": (
                "to connect, to unite",
                "Мы хотим соединиться с ними.",
                "We want to connect with them.",
            ),
            "соединяться": (
                "to connect, to unite",
                "Они соединяются в группу.",
                "They connect into a group.",
            ),
            "предрассудок": (
                "prejudice, bias",
                "Это старый предрассудок.",
                "This is an old prejudice.",
            ),
            "бомбить": (
                "bomb, raid",
                "Враг бомбит город.",
                "The enemy bombs the city.",
            ),
            "правящий": (
                "ruling, governing",
                "Правящая партия сильна.",
                "The ruling party is strong.",
            ),
            "мотивировать": (
                "motivate, encourage",
                "Учитель умеет мотивировать класс.",
                "The teacher can motivate the class.",
            ),
            "вертеть": (
                "twirl, spin",
                "Не верти кольцо на пальце.",
                "Do not twirl the ring on your finger.",
            ),
            "юношеский": (
                "youthful, juvenile",
                "У него юношеский вид.",
                "He has a youthful look.",
            ),
            "жадность": (
                "greed, avarice",
                "Его жадность всем видна.",
                "His greed is visible to all.",
            ),
            "виски": (
                "whiskey, whisky",
                "Налей виски в стакан.",
                "Pour the whiskey into the glass.",
            ),
            "диалектика": (
                "dialectics, dialectic",
                "Диалектика — часть философии.",
                "Dialectics is part of philosophy.",
            ),
            "взятие": (
                "capture, taking",
                "Взятие города заняло день.",
                "The capture of the city took a day.",
            ),
            "развлекаться": (
                "to have fun, to entertain oneself",
                "Ребёнок любит развлекаться.",
                "The child likes to have fun.",
            ),
            "забавно": (
                "funny, amusing",
                "Это было забавно.",
                "That was funny.",
            ),
            "провоцировать": (
                "provoke, incite",
                "Не провоцируй его гнев.",
                "Do not provoke his anger.",
            ),
            "автономия": (
                "autonomy, self-government",
                "Им нужна автономия.",
                "They need autonomy.",
            ),
            "блеснуть": (
                "shine, dazzle",
                "Звезда блеснула в небе.",
                "The star shone in the sky.",
            ),
            "штучка": (
                "thing, gadget",
                "Мне нравится эта штучка.",
                "I like this thing.",
            ),
            "размещать": (
                "to place, to accommodate",
                "Где размещать мебель?",
                "Where do we place the furniture?",
            ),
            "машинист": (
                "engineer, machinist",
                "Машинист ведёт поезд.",
                "The engineer drives the train.",
            ),
            "элегантный": (
                "elegant, stylish",
                "Она в элегантном платье.",
                "She is in an elegant dress.",
            ),
            "рассказчик": (
                "storyteller, narrator",
                "Он хороший рассказчик.",
                "He is a good storyteller.",
            ),
            "собрат": (
                "brother, comrade",
                "Он мой собрат.",
                "He is my comrade.",
            ),
            "скобка": (
                "bracket, brace",
                "Поставь число в скобки.",
                "Put the number in brackets.",
            ),
            "распустить": (
                "dissolve, disband",
                "Сахар распустится в воде.",
                "The sugar will dissolve in water.",
            ),
            "педагогика": (
                "pedagogy, education",
                "Педагогика — трудная наука.",
                "Pedagogy is a hard science.",
            ),
            "рефлекс": (
                "reflex, reflex action",
                "Врач проверил рефлекс.",
                "The doctor checked the reflex.",
            ),
            "глухо": (
                "faintly, dull",
                "Он глухо ответил.",
                "He answered faintly.",
            ),
            "дилер": (
                "dealer, distributor",
                "Дилер дал хорошую скидку.",
                "The dealer gave a good discount.",
            ),
            "напрасный": (
                "vain, futile",
                "Это напрасная попытка.",
                "This is a vain attempt.",
            ),
        },
    )
)
