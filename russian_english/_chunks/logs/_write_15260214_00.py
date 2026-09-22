import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from russian_english._chunk_io import rewrite_chunk

print(
    rewrite_chunk(
        Path("russian_english/_chunks/deck_15260214_00.csv"),
        {
            "марксизм": (
                "Marxism",
                "Он читает о марксизме.",
                "He reads about Marxism.",
            ),
            "въезд": (
                "entry, entrance",
                "Въезд сюда закрыт.",
                "Entry here is closed.",
            ),
            "надлежать": (
                "to be due",
                "Книгу надлежит вернуть завтра.",
                "The book is due tomorrow.",
            ),
            "аварийный": (
                "emergency",
                "Нажми аварийную кнопку.",
                "Press the emergency button.",
            ),
            "чек": (
                "check, receipt",
                "Принесите чек, пожалуйста.",
                "Please bring the check.",
            ),
            "мраморный": (
                "marble",
                "Мраморный стол холодный.",
                "The marble table is cold.",
            ),
            "цент": (
                "cent, penny",
                "Я нашёл цент на земле.",
                "I found a cent on the ground.",
            ),
            "пятеро": (
                "five, five people",
                "Пятеро друзей уже здесь.",
                "Five friends are already here.",
            ),
            "патриотизм": (
                "patriotism",
                "Патриотизм ему важен.",
                "Patriotism is important to him.",
            ),
            "идеально": (
                "ideally",
                "Идеально, мы закончим завтра.",
                "Ideally, we will finish tomorrow.",
            ),
            "доверить": (
                "entrust, confide",
                "Я доверю тебе ключ.",
                "I will entrust the key to you.",
            ),
            "хранитель": (
                "keeper, guardian",
                "Он хранитель этого ключа.",
                "He is the keeper of this key.",
            ),
            "вывеска": (
                "signboard, sign",
                "Вывеска висит над дверью.",
                "The sign hangs above the door.",
            ),
            "дань": (
                "tribute, levy",
                "Они платили дань царю.",
                "They paid tribute to the tsar.",
            ),
            "рыбный": (
                "fish",
                "Я люблю рыбный суп.",
                "I love fish soup.",
            ),
            "импортный": (
                "imported",
                "Это импортное вино.",
                "This is imported wine.",
            ),
            "ныть": (
                "whine, moan",
                "Перестань ныть.",
                "Stop whining.",
            ),
            "дворянин": (
                "nobleman",
                "Дворянин жил в большом доме.",
                "The nobleman lived in a big house.",
            ),
            "вдобавок": (
                "in addition, moreover",
                "Вдобавок возьми хлеб.",
                "In addition, take some bread.",
            ),
            "тринадцать": (
                "thirteen",
                "Ей исполнилось тринадцать.",
                "She turned thirteen.",
            ),
            "прекращать": (
                "to stop, to cease",
                "Прекращай кричать.",
                "Stop shouting.",
            ),
            "яхта": (
                "yacht",
                "Яхта стоит у берега.",
                "The yacht stands by the shore.",
            ),
            "номинация": (
                "nomination",
                "Он получил номинацию.",
                "He received a nomination.",
            ),
            "дрогнуть": (
                "tremble, flinch",
                "Он не дрогнул.",
                "He did not flinch.",
            ),
            "песчаный": (
                "sandy, sand",
                "Пляж был очень песчаным.",
                "The beach was very sandy.",
            ),
            "стартовать": (
                "to start, to launch",
                "Мы стартуем на рассвете.",
                "We start at dawn.",
            ),
            "финансировать": (
                "finance, fund",
                "Они будут финансировать проект.",
                "They will finance the project.",
            ),
            "объектив": (
                "lens",
                "Объектив камеры грязный.",
                "The camera lens is dirty.",
            ),
            "забегать": (
                "to drop by, to run in",
                "Он часто забегает к нам.",
                "He often drops by.",
            ),
            "казна": (
                "treasury",
                "Казна почти пуста.",
                "The treasury is almost empty.",
            ),
            "загрязнение": (
                "pollution",
                "Это сильное загрязнение.",
                "This is strong pollution.",
            ),
            "гном": (
                "gnome",
                "Гном стоит в саду.",
                "The gnome stands in the garden.",
            ),
            "альфа": (
                "alpha",
                "Он здесь альфа.",
                "He is the alpha here.",
            ),
            "лениво": (
                "lazily",
                "Он лениво встал с кровати.",
                "He lazily got up from the bed.",
            ),
            "рассудок": (
                "reason, sanity",
                "Он потерял рассудок.",
                "He lost his reason.",
            ),
            "долгожданный": (
                "long-awaited",
                "Долгожданный день настал.",
                "The long-awaited day is here.",
            ),
            "поделить": (
                "divide, share",
                "Давайте поделим торт.",
                "Let's divide the cake.",
            ),
            "заход": (
                "sunset, approach",
                "Мы ждали заход солнца.",
                "We waited for the sunset.",
            ),
            "прокомментировать": (
                "to comment on",
                "Прокомментируй этот текст.",
                "Comment on this text.",
            ),
            "дополнять": (
                "to complement",
                "Эти цвета дополняют друг друга.",
                "These colors complement each other.",
            ),
            "сейф": (
                "safe, vault",
                "Ключ лежит в сейфе.",
                "The key is in the safe.",
            ),
            "отцовский": (
                "paternal, fatherly",
                "Это его отцовский дом.",
                "This is his paternal home.",
            ),
            "истинно": (
                "truly, genuinely",
                "Она истинно любила его.",
                "She truly loved him.",
            ),
            "схватиться": (
                "to clutch, to grasp",
                "Он схватился за руку.",
                "He clutched her hand.",
            ),
            "майя": (
                "Maya, Mayan",
                "Майя строили города.",
                "The Maya built cities.",
            ),
            "качаться": (
                "swing, sway",
                "Он любит качаться.",
                "He loves to swing.",
            ),
            "минутка": (
                "minute, moment",
                "Просто дай мне минутку, пожалуйста.",
                "Just give me a minute, please.",
            ),
            "корм": (
                "feed, fodder",
                "Купи корм для кота.",
                "Buy feed for the cat.",
            ),
            "обработать": (
                "process, treat",
                "Мы обработаем этот текст.",
                "We will process this text.",
            ),
            "достоверность": (
                "reliability",
                "Достоверность этого низка.",
                "The reliability of this is low.",
            ),
            "троллейбус": (
                "trolleybus",
                "Троллейбус едет по улице.",
                "The trolleybus goes down the street.",
            ),
            "специализация": (
                "specialization",
                "Его специализация — история.",
                "His specialization is history.",
            ),
            "одержать": (
                "to win",
                "Он одержал победу в игре.",
                "He won the game.",
            ),
            "постсоветский": (
                "post-Soviet",
                "Это постсоветский город.",
                "This is a post-Soviet city.",
            ),
            "фонарик": (
                "flashlight",
                "Возьми фонарик с собой.",
                "Take the flashlight with you.",
            ),
            "паук": (
                "spider",
                "Я вижу паука.",
                "I see a spider.",
            ),
            "подписка": (
                "subscription",
                "Я оплатил подписку.",
                "I paid for the subscription.",
            ),
            "баран": (
                "ram",
                "Баран стоит в поле.",
                "The ram stands in the field.",
            ),
            "сэкономить": (
                "save, economize",
                "Мы сэкономили воду.",
                "We saved water.",
            ),
            "могущество": (
                "power, might",
                "Его могущество растёт.",
                "His power is growing.",
            ),
            "перепись": (
                "census",
                "Перепись началась в январе.",
                "The census started in January.",
            ),
            "расцвет": (
                "blossoming, flowering",
                "Это расцвет её карьеры.",
                "This is the blossoming of her career.",
            ),
            "утешение": (
                "consolation, comfort",
                "Её слова — слабое утешение.",
                "Her words are weak consolation.",
            ),
            "кишка": (
                "intestine, gut",
                "Кишка болит.",
                "The intestine hurts.",
            ),
            "зять": (
                "son-in-law, son in law",
                "Мой зять очень добрый.",
                "My son-in-law is very kind.",
            ),
            "тоннель": (
                "tunnel",
                "Поезд вошёл в тоннель.",
                "The train went into the tunnel.",
            ),
            "пошутить": (
                "to joke",
                "Он любит пошутить.",
                "He loves to joke.",
            ),
            "навестить": (
                "visit, call on",
                "Я навещу маму завтра.",
                "I will visit mom tomorrow.",
            ),
            "молекула": (
                "molecule",
                "Это молекула воды.",
                "This is a water molecule.",
            ),
            "посередине": (
                "in the middle",
                "Стол стоит посередине.",
                "The table stands in the middle.",
            ),
            "непонимание": (
                "misunderstanding",
                "Это простое непонимание.",
                "This is a simple misunderstanding.",
            ),
            "отравить": (
                "to poison",
                "Он хотел отравить врага.",
                "He wanted to poison the enemy.",
            ),
            "склонить": (
                "to bend, to incline",
                "Она склонила голову.",
                "She bent her head.",
            ),
            "потомство": (
                "offspring",
                "Она защищает своё потомство.",
                "She protects her offspring.",
            ),
            "взойти": (
                "rise, ascend",
                "Солнце взошло рано.",
                "The sun rose early.",
            ),
            "верблюд": (
                "camel",
                "Верблюд идёт по песку.",
                "The camel goes on the sand.",
            ),
            "причинять": (
                "to cause",
                "Это причиняет боль.",
                "This causes pain.",
            ),
            "замедлить": (
                "slow down",
                "Замедли шаг.",
                "Slow down your step.",
            ),
            "комбинат": (
                "combine, complex",
                "Он работает на комбинате.",
                "He works at the combine.",
            ),
            "длительность": (
                "duration, length",
                "Длительность фильма — два часа.",
                "The movie's duration is two hours.",
            ),
            "зоопарк": (
                "zoo, zoological garden",
                "Мы посетили зоопарк вчера.",
                "We visited the zoo yesterday.",
            ),
            "детишки": (
                "little children, kiddies",
                "Детишки играют во дворе.",
                "The little children play in the yard.",
            ),
            "прирост": (
                "growth, increase",
                "Прирост был маленьким.",
                "The growth was small.",
            ),
            "беспомощный": (
                "helpless",
                "Он выглядел беспомощным.",
                "He looked helpless.",
            ),
            "листовка": (
                "leaflet, flyer",
                "Я прочитал листовку.",
                "I read the leaflet.",
            ),
            "стонать": (
                "moan, groan",
                "Он начал стонать от боли.",
                "He began to moan from pain.",
            ),
            "экстремальный": (
                "extreme",
                "Это экстремальный случай.",
                "This is an extreme case.",
            ),
            "заливать": (
                "pour, fill",
                "Заливай воду медленно.",
                "Pour the water slowly.",
            ),
            "канон": (
                "canon",
                "Эта книга — канон.",
                "This book is canon.",
            ),
            "предотвращение": (
                "prevention",
                "Предотвращение пожара важно.",
                "Fire prevention is important.",
            ),
            "складка": (
                "fold, pleat",
                "На юбке есть складка.",
                "There is a fold on the skirt.",
            ),
            "рубаха": (
                "shirt",
                "Это старая рубаха.",
                "This is an old shirt.",
            ),
            "насмешка": (
                "mockery, ridicule",
                "Его улыбка была насмешкой.",
                "His smile was mockery.",
            ),
            "обои": (
                "wallpaper",
                "Новые обои мне нравятся.",
                "I like the new wallpaper.",
            ),
            "достояние": (
                "heritage, property",
                "Это наше общее достояние.",
                "This is our common heritage.",
            ),
            "задействовать": (
                "involve, engage",
                "Нужно задействовать всю команду.",
                "We need to involve the whole team.",
            ),
            "скромно": (
                "modestly, humbly",
                "Она скромно сказала спасибо.",
                "She modestly said thanks.",
            ),
            "материально": (
                "materially, financially",
                "Они живут материально хорошо.",
                "They live well materially.",
            ),
            "придворный": (
                "court, courtier",
                "Он был придворным поэтом.",
                "He was a court poet.",
            ),
            "певица": (
                "singer, vocalist",
                "Певица вышла на сцену.",
                "The singer walked onto the stage.",
            ),
        },
    )
)
