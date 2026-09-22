import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from russian_english._chunk_io import rewrite_chunk

print(
    rewrite_chunk(
        Path("russian_english/_chunks/deck_15260198_02.csv"),
        {
            "подхватить": (
                "to pick up, to catch",
                "Он подхватил мяч.",
                "He caught the ball.",
            ),
            "кукла": ("doll, puppet", "Где моя кукла?", "Where is my doll?"),
            "прыжок": (
                "jump, leap",
                "Это высокий прыжок.",
                "This is a high jump.",
            ),
            "уголь": ("coal, charcoal", "Нам нужен уголь.", "We need coal."),
            "выделение": (
                "allocation, secretion",
                "Нужно выделение времени.",
                "We need an allocation of time.",
            ),
            "головка": ("head, knob", "Поверни головку.", "Turn the knob."),
            "чемпион": (
                "champion, winner",
                "Он стал чемпионом.",
                "He became a champion.",
            ),
            "наносить": (
                "apply, inflict",
                "Он наносит удар.",
                "He inflicts a blow.",
            ),
            "листок": (
                "leaf, sheet",
                "С дерева упал листок.",
                "A leaf fell from the tree.",
            ),
            "периодически": (
                "periodically, occasionally",
                "Я периодически звоню.",
                "I call periodically.",
            ),
            "ноготь": (
                "nail, claw",
                "У неё длинный ноготь.",
                "She has a long nail.",
            ),
            "фунт": (
                "pound, lb",
                "Это стоит пять фунтов.",
                "This costs five pounds.",
            ),
            "ярость": (
                "rage, fury",
                "Он кричал от ярости.",
                "He shouted from rage.",
            ),
            "колхоз": (
                "collective farm, kolkhoz",
                "Они живут в колхозе.",
                "They live in a kolkhoz.",
            ),
            "машинка": ("toy car", "Купи ему машинку.", "Buy him a toy car."),
            "сверкать": (
                "sparkle, flash",
                "Её глаза сверкают.",
                "Her eyes sparkle.",
            ),
            "пред": (
                "before, in front of",
                "Он встал пред нами.",
                "He stood before us.",
            ),
            "мяч": ("ball", "Он ударил мяч.", "He hit the ball."),
            "повреждение": (
                "damage, injury",
                "Тут есть повреждение.",
                "There is damage here.",
            ),
            "топор": ("axe, hatchet", "Дай мне топор.", "Give me the axe."),
            "воплощение": (
                "incarnation, embodiment",
                "Он воплощение зла.",
                "He is the incarnation of evil.",
            ),
            "ориентироваться": (
                "to navigate, to orientate",
                "Я плохо ориентируюсь здесь.",
                "I cannot navigate here.",
            ),
            "изнутри": (
                "inside, from within",
                "Открой дверь изнутри.",
                "Open the door from inside.",
            ),
            "жаркий": (
                "hot, scorching",
                "Сегодня жаркий день.",
                "Today is a hot day.",
            ),
            "диета": ("diet, regimen", "Она на диете.", "She is on a diet."),
            "часовой": (
                "hourly, sentinel",
                "Часовой стоит у двери.",
                "The sentinel stands at the door.",
            ),
            "поправить": (
                "correct, adjust",
                "Дай я поправлю это.",
                "Let me correct this.",
            ),
            "присесть": (
                "sit down, squat",
                "Присядь сюда.",
                "Sit down here.",
            ),
            "заработный": (
                "wage",
                "Это его заработная плата.",
                "This is his wage.",
            ),
            "современник": (
                "contemporary, peer",
                "Он мой современник.",
                "He is my contemporary.",
            ),
            "конверт": (
                "envelope, cover",
                "Положи это в конверт.",
                "Put this in the envelope.",
            ),
            "ориентировать": (
                "orient, guide",
                "Ориентируй нас по карте.",
                "Orient us by the map.",
            ),
            "отмечаться": (
                "be noted, be celebrated",
                "Праздник отмечается завтра.",
                "The holiday is celebrated tomorrow.",
            ),
            "ремень": ("belt, strap", "Где мой ремень?", "Where is my belt?"),
            "отпускать": (
                "to release, to let go",
                "Не отпускай мою руку.",
                "Don't release my hand.",
            ),
            "коммунизм": (
                "communism",
                "Он верит в коммунизм.",
                "He believes in communism.",
            ),
            "снизить": (
                "reduce, lower",
                "Нужно снизить цену.",
                "We must reduce the price.",
            ),
            "мм": ("mm, millimeters", "Это пять мм.", "This is five mm."),
            "тем": (
                "the more, by that",
                "Тем больше он хочет.",
                "The more he wants.",
            ),
            "подземный": (
                "underground, subterranean",
                "Это подземный ход.",
                "This is an underground passage.",
            ),
            "ус": (
                "whisker, mustache",
                "У кота длинный ус.",
                "The cat has a long whisker.",
            ),
            "карандаш": (
                "pencil, crayon",
                "Где мой карандаш?",
                "Where is my pencil?",
            ),
            "вылететь": (
                "to fly out, to be eliminated",
                "Мы вылетим утром.",
                "We will fly out in the morning.",
            ),
            "разряд": (
                "category, discharge",
                "Это сильный разряд.",
                "This is a strong discharge.",
            ),
            "ругаться": (
                "to swear, to quarrel",
                "Они снова ругаются.",
                "They quarrel again.",
            ),
            "заяц": ("hare, rabbit", "Я видел зайца.", "I saw a hare."),
            "вкладывать": (
                "to invest, to put in",
                "Он вкладывает время.",
                "He invests time.",
            ),
            "любовник": (
                "lover, paramour",
                "У неё есть любовник.",
                "She has a lover.",
            ),
            "зафиксировать": (
                "record, fix",
                "Зафиксируй это.",
                "Record this.",
            ),
            "извлечь": (
                "extract, retrieve",
                "Извлеки это оттуда.",
                "Extract this from there.",
            ),
            "нелепый": (
                "ridiculous, absurd",
                "Это нелепый ответ.",
                "This is a ridiculous answer.",
            ),
            "радовать": (
                "to please, to delight",
                "Это радует меня.",
                "This pleases me.",
            ),
            "неправильно": (
                "incorrectly, wrong",
                "Он ответил неправильно.",
                "He answered incorrectly.",
            ),
            "индекс": (
                "index, indicator",
                "Найди это в индексе.",
                "Find this in the index.",
            ),
            "прятать": (
                "hide, conceal",
                "Она прячет письмо.",
                "She hides the letter.",
            ),
            "принцесса": (
                "princess",
                "Принцесса ждёт нас.",
                "The princess waits for us.",
            ),
            "лужа": (
                "puddle, pool",
                "Не наступи в лужу.",
                "Don't step in the puddle.",
            ),
            "сосуд": (
                "vessel, container",
                "Это старый сосуд.",
                "This is an old vessel.",
            ),
            "хаос": (
                "chaos, disorder",
                "В доме хаос.",
                "There is chaos in the house.",
            ),
            "самоуправление": (
                "self-government, self-management",
                "У нас самоуправление.",
                "We have self-government.",
            ),
            "сырой": (
                "raw, damp",
                "Не ешь сырое мясо.",
                "Don't eat raw meat.",
            ),
            "давний": (
                "old, long-standing",
                "Это мой давний друг.",
                "This is my old friend.",
            ),
            "трагический": (
                "tragic",
                "Это трагический случай.",
                "This is a tragic case.",
            ),
            "психика": (
                "psyche, mind",
                "Это бьёт по психике.",
                "This hits the psyche.",
            ),
            "асфальт": (
                "asphalt, tarmac",
                "Не сиди на асфальте.",
                "Don't sit on the asphalt.",
            ),
            "светить": (
                "shine, illuminate",
                "Солнце светит.",
                "The sun shines.",
            ),
            "воинский": (
                "military, martial",
                "Это воинский долг.",
                "This is a military duty.",
            ),
            "чувствоваться": (
                "to be felt, to feel",
                "Холод чувствуется здесь.",
                "The cold is felt here.",
            ),
            "поделать": (
                "to do, to make",
                "Ничего не поделаешь.",
                "You can do nothing.",
            ),
            "портал": (
                "portal, gateway",
                "Открой этот портал.",
                "Open this portal.",
            ),
            "уничтожать": (
                "destroy, annihilate",
                "Огонь уничтожает лес.",
                "Fire destroys the forest.",
            ),
            "плотно": (
                "tightly, densely",
                "Закрой дверь плотно.",
                "Close the door tightly.",
            ),
            "некуда": (
                "nowhere, no place",
                "Мне некуда идти.",
                "I have nowhere to go.",
            ),
            "объявлять": (
                "to announce, to declare",
                "Они объявляют победу.",
                "They announce the victory.",
            ),
            "удержаться": (
                "to hold on, to refrain",
                "Я не смог удержаться.",
                "I could not hold on.",
            ),
            "тесно": (
                "closely, tightly",
                "Мы сидим тесно.",
                "We sit tightly.",
            ),
            "инфраструктура": (
                "infrastructure, facilities",
                "Инфраструктура слабая.",
                "The infrastructure is weak.",
            ),
            "сессия": (
                "session, academic term",
                "Сессия начинается завтра.",
                "The session starts tomorrow.",
            ),
            "телеграмма": (
                "telegram, cablegram",
                "Я получил телеграмму.",
                "I received a telegram.",
            ),
            "умственный": (
                "intellectual, mental",
                "Это умственный труд.",
                "This is mental work.",
            ),
            "кинотеатр": (
                "cinema, movie theater",
                "Мы идём в кинотеатр.",
                "We are going to the cinema.",
            ),
            "ритуал": (
                "ritual, ceremony",
                "Это старый ритуал.",
                "This is an old ritual.",
            ),
            "комплект": (
                "set, kit",
                "Вот полный комплект.",
                "Here is the full set.",
            ),
            "смело": (
                "bravely, boldly",
                "Он смело сказал нет.",
                "He bravely said no.",
            ),
            "филиал": (
                "branch, subsidiary",
                "Это наш новый филиал.",
                "This is our new branch.",
            ),
            "учительница": (
                "teacher, female teacher",
                "Учительница вошла в класс.",
                "The teacher came into the class.",
            ),
            "вечность": (
                "eternity, infinity",
                "Это длилось вечность.",
                "It lasted an eternity.",
            ),
            "танковый": (
                "tank, armored",
                "Это был танковый бой.",
                "This was a tank battle.",
            ),
            "организационный": (
                "organizational",
                "Это организационный вопрос.",
                "This is an organizational question.",
            ),
            "тренинг": (
                "training, workshop",
                "Я иду на тренинг.",
                "I am going to a training.",
            ),
            "сообразить": (
                "figure out, realize",
                "Я не могу это сообразить.",
                "I cannot figure this out.",
            ),
            "светиться": (
                "to glow, to shine",
                "Её лицо светится.",
                "Her face glows.",
            ),
            "наивный": (
                "naive, gullible",
                "Он слишком наивный.",
                "He is too naive.",
            ),
            "ознакомиться": (
                "to get acquainted, to familiarize",
                "Ознакомься с этим.",
                "Familiarize yourself with this.",
            ),
            "коньяк": (
                "cognac, brandy",
                "Налей мне коньяк.",
                "Pour me some cognac.",
            ),
            "дефицит": (
                "deficit, shortage",
                "У нас дефицит воды.",
                "We have a deficit of water.",
            ),
            "оглядываться": (
                "to look back, to glance back",
                "Не оглядывайся.",
                "Don't look back.",
            ),
            "осенний": (
                "autumn, fall",
                "Это осенний день.",
                "This is an autumn day.",
            ),
            "залив": (
                "bay, gulf",
                "Мы живём у залива.",
                "We live by the bay.",
            ),
            "рваться": (
                "to tear, to strive",
                "Платье рвётся.",
                "The dress is tearing.",
            ),
        },
    )
)
