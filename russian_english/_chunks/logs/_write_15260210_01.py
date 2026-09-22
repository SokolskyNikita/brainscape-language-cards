import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from russian_english._chunk_io import rewrite_chunk

print(
    rewrite_chunk(
        Path("russian_english/_chunks/deck_15260210_01.csv"),
        {
            "мамин": (
                "mom's",
                "Это мамина книга.",
                "This is mom's book.",
            ),
            "смириться": (
                "to resign oneself",
                "Я смирился с этим.",
                "I resigned myself to this.",
            ),
            "рискнуть": (
                "to risk",
                "Я решил рискнуть.",
                "I decided to risk it.",
            ),
            "поблизости": (
                "nearby",
                "Магазин поблизости.",
                "The store is nearby.",
            ),
            "ударный": (
                "percussive",
                "Это ударный инструмент.",
                "This is a percussive instrument.",
            ),
            "петух": (
                "rooster",
                "Петух кричит утром.",
                "The rooster crows in the morning.",
            ),
            "упираться": (
                "to resist",
                "Он упирается.",
                "He is resisting.",
            ),
            "компенсировать": (
                "to compensate",
                "Это компенсирует потери.",
                "This compensates for the losses.",
            ),
            "немыслимый": (
                "unthinkable",
                "Это немыслимая идея.",
                "This is an unthinkable idea.",
            ),
            "заветный": (
                "cherished",
                "Это моя заветная мечта.",
                "This is my cherished dream.",
            ),
            "античный": (
                "ancient",
                "Это античный храм.",
                "This is an ancient temple.",
            ),
            "двадцатый": (
                "twentieth",
                "Это двадцатый век.",
                "This is the twentieth century.",
            ),
            "убежище": (
                "shelter",
                "Мы нашли убежище.",
                "We found shelter.",
            ),
            "последовательно": (
                "sequentially",
                "Делай это последовательно.",
                "Do this sequentially.",
            ),
            "проба": (
                "sample",
                "Это только проба.",
                "This is only a sample.",
            ),
            "ведать": (
                "to know",
                "Я не ведаю.",
                "I do not know.",
            ),
            "визуальный": (
                "visual",
                "Это визуальный знак.",
                "This is a visual sign.",
            ),
            "оцениваться": (
                "to be evaluated",
                "Работа оценивается.",
                "The work is being evaluated.",
            ),
            "инженерный": (
                "engineering",
                "Это инженерный проект.",
                "This is an engineering project.",
            ),
            "кидать": (
                "to throw",
                "Он кидает мяч.",
                "He throws the ball.",
            ),
            "умерший": (
                "deceased",
                "Умерший отец.",
                "The deceased father.",
            ),
            "бес": (
                "demon",
                "Это злой бес.",
                "This is an evil demon.",
            ),
            "ненадолго": (
                "for a short time",
                "Останься ненадолго.",
                "Stay for a short time.",
            ),
            "сонный": (
                "sleepy",
                "Я очень сонный.",
                "I am very sleepy.",
            ),
            "отнимать": (
                "to take away",
                "Это отнимает время.",
                "This takes away time.",
            ),
            "погрузить": (
                "to immerse",
                "Погрузи камень в воду.",
                "Immerse the stone in the water.",
            ),
            "драматический": (
                "dramatic",
                "Это драматический театр.",
                "This is a dramatic theater.",
            ),
            "ягода": (
                "berry",
                "Это сладкая ягода.",
                "This is a sweet berry.",
            ),
            "неприятель": (
                "enemy",
                "Это наш неприятель.",
                "This is our enemy.",
            ),
            "личностный": (
                "personal",
                "Это личностный рост.",
                "This is personal growth.",
            ),
            "нитка": (
                "thread",
                "Дай мне нитку.",
                "Give me the thread.",
            ),
            "сдвиг": (
                "shift",
                "Это большой сдвиг.",
                "This is a big shift.",
            ),
            "неудобный": (
                "uncomfortable",
                "Это неудобный стул.",
                "This is an uncomfortable chair.",
            ),
            "стоп": (
                "stop",
                "Скажи стоп.",
                "Say stop.",
            ),
            "пыльный": (
                "dusty",
                "Стол пыльный.",
                "The table is dusty.",
            ),
            "благословение": (
                "blessing",
                "Это большое благословение.",
                "This is a great blessing.",
            ),
            "уральский": (
                "Ural",
                "Это уральский город.",
                "This is a Ural city.",
            ),
            "крымский": (
                "Crimean",
                "Это крымский берег.",
                "This is the Crimean coast.",
            ),
            "массивный": (
                "massive",
                "Это массивный стол.",
                "This is a massive table.",
            ),
            "отправка": (
                "shipment",
                "Отправка завтра.",
                "The shipment is tomorrow.",
            ),
            "нищета": (
                "poverty",
                "Там страшная нищета.",
                "There is terrible poverty there.",
            ),
            "гимн": (
                "anthem",
                "Они поют гимн.",
                "They sing the anthem.",
            ),
            "патриот": (
                "patriot",
                "Он настоящий патриот.",
                "He is a true patriot.",
            ),
            "жрец": (
                "priest",
                "Древний жрец.",
                "An ancient priest.",
            ),
            "шестнадцать": (
                "sixteen",
                "Ей исполнилось шестнадцать.",
                "She turned sixteen.",
            ),
            "пристрастие": (
                "addiction",
                "У него пристрастие к игре.",
                "He has an addiction to the game.",
            ),
            "гигант": (
                "giant",
                "Это гигант.",
                "This is a giant.",
            ),
            "бульвар": (
                "boulevard",
                "Мы идём по бульвару.",
                "We walk along the boulevard.",
            ),
            "нарочно": (
                "on purpose",
                "Он сделал это нарочно.",
                "He did this on purpose.",
            ),
            "дуб": (
                "oak",
                "Это старый дуб.",
                "This is an old oak.",
            ),
            "присниться": (
                "to appear in a dream",
                "Ты мне приснился.",
                "You appeared in a dream.",
            ),
            "воздействовать": (
                "to influence",
                "Это воздействует на нас.",
                "This influences us.",
            ),
            "словесный": (
                "verbal",
                "Это словесный портрет.",
                "This is a verbal portrait.",
            ),
            "синтез": (
                "synthesis",
                "Это синтез.",
                "This is synthesis.",
            ),
            "уборка": (
                "cleaning",
                "Нужна уборка.",
                "Cleaning is needed.",
            ),
            "суждено": (
                "destined",
                "Ему суждено.",
                "He is destined.",
            ),
            "шить": (
                "to sew",
                "Она шьёт платье.",
                "She is sewing a dress.",
            ),
            "привозить": (
                "to bring",
                "Отец привозит хлеб.",
                "Father brings bread.",
            ),
            "страничка": (
                "page",
                "Открой эту страничку.",
                "Open this page.",
            ),
            "проглотить": (
                "to swallow",
                "Он проглотил воду.",
                "He swallowed the water.",
            ),
            "перехватить": (
                "to intercept",
                "Он перехватил мяч.",
                "He intercepted the ball.",
            ),
            "опасно": (
                "dangerous",
                "Здесь опасно.",
                "It is dangerous here.",
            ),
            "местечко": (
                "small town",
                "Тихое местечко.",
                "A quiet small town.",
            ),
            "припомнить": (
                "to recall",
                "Я не могу припомнить.",
                "I cannot recall.",
            ),
            "составной": (
                "compound",
                "Это составное слово.",
                "This is a compound word.",
            ),
            "шахматы": (
                "chess",
                "Мы играем в шахматы.",
                "We play chess.",
            ),
            "задыхаться": (
                "to gasp",
                "Я задыхаюсь.",
                "I am gasping.",
            ),
            "кристалл": (
                "crystal",
                "Это красивый кристалл.",
                "This is a beautiful crystal.",
            ),
            "цвести": (
                "to bloom",
                "Деревья цветут.",
                "The trees are blooming.",
            ),
            "промолчать": (
                "to keep silent, to say nothing",
                "Он решил промолчать.",
                "He chose to keep silent.",
            ),
            "университетский": (
                "university",
                "Это университетский двор.",
                "This is a university courtyard.",
            ),
            "познакомить": (
                "to introduce",
                "Познакомь меня с ним.",
                "Introduce me to him.",
            ),
            "наружный": (
                "outer",
                "Это наружная стена.",
                "This is an outer wall.",
            ),
            "вилка": (
                "fork",
                "Дай мне вилку.",
                "Give me a fork.",
            ),
            "старичок": (
                "old man",
                "Вот старичок.",
                "Here is an old man.",
            ),
            "пепел": (
                "ash",
                "Везде пепел.",
                "There is ash everywhere.",
            ),
            "частенько": (
                "quite often",
                "Я частенько хожу туда.",
                "I go there quite often.",
            ),
            "слыхать": (
                "to hear",
                "Я не слыхал.",
                "I did not hear.",
            ),
            "прихожая": (
                "hallway",
                "Оставь обувь в прихожей.",
                "Leave the shoes in the hallway.",
            ),
            "сплошь": (
                "entirely",
                "Поле сплошь в снегу.",
                "The field is entirely in snow.",
            ),
            "ведомость": (
                "list",
                "Проверь ведомость.",
                "Check the list.",
            ),
            "добираться": (
                "to get to",
                "Я добираюсь до работы.",
                "I get to work.",
            ),
            "полководец": (
                "commander",
                "Он великий полководец.",
                "He is a great commander.",
            ),
            "мамочка": (
                "mommy",
                "Мамочка дома.",
                "Mommy is at home.",
            ),
            "езда": (
                "riding",
                "Мне нравится езда.",
                "I like riding.",
            ),
            "тормозить": (
                "to brake",
                "Машина тормозит.",
                "The car is braking.",
            ),
            "завершать": (
                "to complete",
                "Я завершаю работу.",
                "I am completing the work.",
            ),
            "охотиться": (
                "to hunt",
                "Они охотятся в лесу.",
                "They hunt in the forest.",
            ),
            "снести": (
                "to demolish",
                "Они снесут дом.",
                "They will demolish the house.",
            ),
            "избыток": (
                "surplus, excess",
                "У нас избыток яблок.",
                "We have a surplus of apples.",
            ),
            "подчинение": (
                "subordination",
                "Это полное подчинение.",
                "This is complete subordination.",
            ),
            "импорт": (
                "import",
                "Импорт растёт.",
                "Import is growing.",
            ),
            "повиснуть": (
                "to hang",
                "Он повис на ветке.",
                "He hung on the branch.",
            ),
            "безумно": (
                "madly",
                "Она безумно любит его.",
                "She loves him madly.",
            ),
            "механик": (
                "mechanic",
                "Механик здесь.",
                "The mechanic is here.",
            ),
            "возмещение": (
                "compensation",
                "Я жду возмещения.",
                "I am waiting for compensation.",
            ),
            "спорный": (
                "controversial",
                "Это спорный вопрос.",
                "This is a controversial question.",
            ),
            "влезть": (
                "to climb in",
                "Он влез в окно.",
                "He climbed in the window.",
            ),
            "взволновать": (
                "to excite",
                "Это взволновало меня.",
                "This excited me.",
            ),
            "освобождать": (
                "to liberate",
                "Они освобождают город.",
                "They are liberating the city.",
            ),
        },
    )
)
