import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from russian_english._chunk_io import rewrite_chunk

print(
    rewrite_chunk(
        Path("russian_english/_chunks/deck_15260213_02.csv"),
        {
            "нахождение": (
                "finding, discovery",
                "Это важное нахождение.",
                "This is an important finding.",
            ),
            "парадный": (
                "ceremonial, parade",
                "Парадный костюм готов.",
                "The ceremonial suit is ready.",
            ),
            "выдумать": (
                "invent, make up",
                "Она выдумала историю.",
                "She invented a story.",
            ),
            "провозгласить": (
                "proclaim, declare",
                "Они провозгласили мир.",
                "They proclaimed peace.",
            ),
            "коррекция": (
                "correction, adjustment",
                "Нужна коррекция текста.",
                "The text needs a correction.",
            ),
            "коготь": (
                "claw, talon",
                "У кошки острый коготь.",
                "The cat has a sharp claw.",
            ),
            "изъять": (
                "remove, extract",
                "Они изъяли документы.",
                "They removed the documents.",
            ),
            "порадовать": (
                "to please, to delight",
                "Надо порадовать их.",
                "We must please them.",
            ),
            "присоединяться": (
                "to join, to connect",
                "Я не буду присоединяться.",
                "I will not join.",
            ),
            "тоталитарный": (
                "totalitarian, authoritarian",
                "Это тоталитарный режим.",
                "This is a totalitarian regime.",
            ),
            "резолюция": (
                "resolution",
                "Вот новая резолюция.",
                "Here is a new resolution.",
            ),
            "экзотический": (
                "exotic",
                "Это экзотический фрукт.",
                "This is an exotic fruit.",
            ),
            "минеральный": (
                "mineral",
                "Минеральная вода холодная.",
                "The mineral water is cold.",
            ),
            "походка": (
                "gait, walk",
                "У него лёгкая походка.",
                "He has a light gait.",
            ),
            "уносить": (
                "carry away, take away",
                "Ветер уносит листья.",
                "The wind carries away the leaves.",
            ),
            "родственный": (
                "related, kindred",
                "Это родственный язык.",
                "This is a related language.",
            ),
            "бланк": (
                "form, blank",
                "Заполни этот бланк.",
                "Fill out this form.",
            ),
            "матка": (
                "uterus, womb",
                "Врач видит матку.",
                "The doctor sees the uterus.",
            ),
            "лебедь": (
                "swan",
                "Вот белый лебедь.",
                "Here is a white swan.",
            ),
            "пасха": (
                "Easter",
                "Пасха уже завтра.",
                "Easter is tomorrow.",
            ),
            "подбежать": (
                "to run up, to come running",
                "Он подбежал к дому.",
                "He ran up to the house.",
            ),
            "взаимодействовать": (
                "interact, cooperate",
                "Они должны взаимодействовать.",
                "They must interact.",
            ),
            "сундук": (
                "chest, trunk",
                "Старый сундук пуст.",
                "The old chest is empty.",
            ),
            "внучка": (
                "granddaughter",
                "Моя внучка дома.",
                "My granddaughter is home.",
            ),
            "консервативный": (
                "conservative, traditional",
                "У него консервативный взгляд.",
                "He has a conservative view.",
            ),
            "устраиваться": (
                "to settle in, to get a job",
                "Он устраивается на работу.",
                "He wants to get a job.",
            ),
            "живо": (
                "quickly, lively",
                "Он живо ответил.",
                "He answered quickly.",
            ),
            "кража": (
                "theft, stealing",
                "Это была кража.",
                "This was a theft.",
            ),
            "нулевой": (
                "zero, null",
                "У нас нулевой результат.",
                "We have a zero result.",
            ),
            "интеллигент": (
                "intellectual, cultured person",
                "Он настоящий интеллигент.",
                "He is a true intellectual.",
            ),
            "тонуть": (
                "sink, drown",
                "Лодка начинает тонуть.",
                "The boat starts to sink.",
            ),
            "небось": (
                "I bet, probably",
                "Небось, ты устал.",
                "Probably you are tired.",
            ),
            "осмыслить": (
                "comprehend, make sense of",
                "Надо осмыслить это.",
                "We must comprehend this.",
            ),
            "лечебный": (
                "therapeutic, medicinal",
                "Это лечебный чай.",
                "This is therapeutic tea.",
            ),
            "туманный": (
                "foggy, misty",
                "Сегодня туманный день.",
                "Today is a foggy day.",
            ),
            "голландский": (
                "Dutch",
                "Это голландский сыр.",
                "This is Dutch cheese.",
            ),
            "благодать": (
                "grace, blessing",
                "Вот настоящая благодать.",
                "This is true grace.",
            ),
            "парад": (
                "parade",
                "Парад на улице.",
                "The parade is on the street.",
            ),
            "реабилитация": (
                "rehabilitation",
                "Ему нужна реабилитация.",
                "He needs rehabilitation.",
            ),
            "доброволец": (
                "volunteer",
                "Он наш доброволец.",
                "He is our volunteer.",
            ),
            "уран": (
                "uranium, Uranus",
                "Уран есть металл.",
                "Uranium is a metal.",
            ),
            "разбивать": (
                "to break, to smash",
                "Не надо разбивать стекло.",
                "Do not break the glass.",
            ),
            "противодействие": (
                "counteraction, opposition",
                "Есть сильное противодействие.",
                "There is strong counteraction.",
            ),
            "весы": (
                "scales, Libra",
                "Поставь это на весы.",
                "Put this on the scales.",
            ),
            "разгар": (
                "height, midst",
                "Сейчас разгар лета.",
                "It is the height of summer.",
            ),
            "крах": (
                "collapse, crash",
                "Это полный крах.",
                "This is a total collapse.",
            ),
            "впредь": (
                "henceforth, from now on",
                "Впредь так не делай.",
                "Henceforth do not do that.",
            ),
            "выдаваться": (
                "stand out, be issued",
                "Документы выдаются здесь.",
                "Documents are issued here.",
            ),
            "уменьшиться": (
                "decrease, diminish",
                "Боль должна уменьшиться.",
                "The pain must decrease.",
            ),
            "земляк": (
                "countryman, fellow countryman",
                "Он мой земляк.",
                "He is my countryman.",
            ),
            "извиниться": (
                "to apologize, to excuse oneself",
                "Я хочу извиниться.",
                "I want to apologize.",
            ),
            "давность": (
                "limitation period, antiquity",
                "Срок давности важен.",
                "The limitation period is important.",
            ),
            "поощрять": (
                "encourage, promote",
                "Надо поощрять сына.",
                "We must encourage the son.",
            ),
            "загореться": (
                "to catch fire, to light up",
                "Дом загорелся ночью.",
                "The house catches fire at night.",
            ),
            "мыслитель": (
                "thinker, philosopher",
                "Он великий мыслитель.",
                "He is a great thinker.",
            ),
            "незадолго": (
                "shortly before, not long before",
                "Это было незадолго до нас.",
                "This was shortly before us.",
            ),
            "ректор": (
                "rector, president",
                "Ректор говорит со студентами.",
                "The rector talks with the students.",
            ),
            "учитываться": (
                "to be taken into account, to be considered",
                "Это должно учитываться.",
                "This must be considered.",
            ),
            "таможня": (
                "customs",
                "Таможня ещё закрыта.",
                "Customs is still closed.",
            ),
            "приоткрыть": (
                "to crack open, to half-open",
                "Приоткрой окно.",
                "Crack open the window.",
            ),
            "обучить": (
                "to teach, to train",
                "Он обучил сына.",
                "He teaches his son.",
            ),
            "руководящий": (
                "guiding, leading",
                "Он занял руководящий пост.",
                "He took a leading post.",
            ),
            "приговорить": (
                "sentence, condemn",
                "Суд приговорил его.",
                "The court sentenced him.",
            ),
            "модем": (
                "modem",
                "Модем не работает.",
                "The modem does not work.",
            ),
            "похитить": (
                "kidnap, abduct",
                "Они хотят похитить его.",
                "They want to kidnap him.",
            ),
            "коробочка": (
                "box, small box",
                "Коробочка на столе.",
                "The box is on the table.",
            ),
            "клятва": (
                "oath, vow",
                "Это моя клятва.",
                "This is my oath.",
            ),
            "телега": (
                "cart, wagon",
                "Телега стоит во дворе.",
                "The cart stands in the yard.",
            ),
            "плясать": (
                "dance",
                "Мы любим плясать.",
                "We love to dance.",
            ),
            "прихватить": (
                "grab, snatch",
                "Прихвати ключи.",
                "Grab the keys.",
            ),
            "заведомо": (
                "deliberately, knowingly",
                "Это заведомо плохой план.",
                "This is a deliberately bad plan.",
            ),
            "однозначный": (
                "unambiguous, unequivocal",
                "Ответ однозначный.",
                "The answer is unambiguous.",
            ),
            "нетрудно": (
                "not difficult, easy",
                "Это нетрудно понять.",
                "This is not difficult to understand.",
            ),
            "старшина": (
                "sergeant major, petty officer",
                "Старшина дал приказ.",
                "The sergeant major gives an order.",
            ),
            "немедленный": (
                "immediate, instant",
                "Нужен немедленный ответ.",
                "An immediate answer is needed.",
            ),
            "исправлять": (
                "correct, fix",
                "Надо исправлять ошибки.",
                "We must correct mistakes.",
            ),
            "жук": (
                "beetle, bug",
                "Жук на столе.",
                "A beetle is on the table.",
            ),
            "вооружить": (
                "arm, equip",
                "Они хотят вооружить отряд.",
                "They want to arm the squad.",
            ),
            "кличка": (
                "nickname",
                "Какая у него кличка?",
                "What is his nickname?",
            ),
            "чудный": (
                "wonderful, marvelous",
                "Какой чудный день!",
                "What a wonderful day!",
            ),
            "дружный": (
                "united, close",
                "У нас дружная семья.",
                "We have a united family.",
            ),
            "казахский": (
                "Kazakh",
                "Он учит казахский язык.",
                "He is learning Kazakh.",
            ),
            "груда": (
                "heap, pile",
                "На полу груда книг.",
                "There is a heap of books on the floor.",
            ),
            "сбрасывать": (
                "to drop, to discard",
                "Не надо сбрасывать снег.",
                "Do not drop the snow.",
            ),
            "врезаться": (
                "crash into, collide",
                "Машина врезалась в дерево.",
                "The car crashed into a tree.",
            ),
            "ля": (
                "la, A",
                "Это нота ля.",
                "This is the note la.",
            ),
            "амбиция": (
                "ambition, aspiration",
                "У неё большая амбиция.",
                "She has a great ambition.",
            ),
            "сидение": (
                "seat, seating",
                "Сидение мягкое.",
                "The seat is soft.",
            ),
            "лик": (
                "face, image",
                "Я вижу его лик.",
                "I see his face.",
            ),
            "вынимать": (
                "to remove, to extract",
                "Надо вынимать ключ.",
                "We must remove the key.",
            ),
            "растительный": (
                "vegetable, plant-based",
                "Это растительное масло.",
                "This is vegetable oil.",
            ),
            "осваивать": (
                "master, assimilate",
                "Он начал осваивать язык.",
                "He starts to master the language.",
            ),
            "императрица": (
                "empress",
                "Императрица в зале.",
                "The empress is in the hall.",
            ),
            "жать": (
                "press, squeeze",
                "Не надо жать меня.",
                "Do not squeeze me.",
            ),
            "бессмертие": (
                "immortality, eternal life",
                "Он верит в бессмертие.",
                "He believes in immortality.",
            ),
            "репетиция": (
                "rehearsal, practice",
                "Репетиция завтра.",
                "The rehearsal is tomorrow.",
            ),
            "исправление": (
                "correction, amendment",
                "Нужно исправление.",
                "A correction is needed.",
            ),
            "грузовой": (
                "cargo, freight",
                "Грузовой поезд уже здесь.",
                "The cargo train is already here.",
            ),
            "казарма": (
                "barracks",
                "Солдаты живут в казарме.",
                "Soldiers live in the barracks.",
            ),
            "рыбалка": (
                "fishing, angling",
                "Завтра идём на рыбалку.",
                "Tomorrow we go fishing.",
            ),
        },
    )
)
