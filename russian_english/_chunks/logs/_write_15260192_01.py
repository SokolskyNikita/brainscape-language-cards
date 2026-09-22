import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from russian_english._chunk_io import rewrite_chunk

print(
    rewrite_chunk(
        Path("russian_english/_chunks/deck_15260192_01.csv"),
        {
            "доходить": (
                "to reach, to get through",
                "До меня не доходит.",
                "It's not getting through to me.",
            ),
            "образовать": ("to form", "Давай образуем группу.", "Let's form a group."),
            "разрушить": (
                "to destroy",
                "Ты всё разрушил.",
                "You destroyed everything.",
            ),
            "отражать": (
                "to reflect",
                "Зеркало плохо отражает.",
                "The mirror doesn't reflect well.",
            ),
            "лезть": ("to climb, to poke into", "Не лезь.", "Don't poke into it."),
            "голод": ("hunger", "Какой голод!", "What hunger!"),
            "выстрел": ("shot", "Это был выстрел?", "Was that a shot?"),
            "столетие": (
                "century",
                "Прошло уже столетие.",
                "A century has already passed.",
            ),
            "ключевой": (
                "key, crucial",
                "Это ключевой момент.",
                "This is the key moment.",
            ),
            "шкаф": (
                "wardrobe, cupboard",
                "Поставь в шкаф.",
                "Put it in the wardrobe.",
            ),
            "победитель": ("winner", "Кто победитель?", "Who's the winner?"),
            "доверять": ("to trust", "Я ему не доверяю.", "I don't trust him."),
            "независимо": (
                "independently, regardless",
                "Независимо от цены.",
                "Regardless of the price.",
            ),
            "жанр": ("genre", "Это не мой жанр.", "That's not my genre."),
            "зимний": ("winter", "Зимний вечер.", "A winter evening."),
            "вступать": (
                "to join, to enter",
                "Не вступай в спор.",
                "Don't enter the argument.",
            ),
            "философский": (
                "philosophical",
                "Слишком философский вопрос.",
                "That's too philosophical.",
            ),
            "решаться": (
                "to dare, to make up one's mind",
                "Я не решаюсь.",
                "I don't dare.",
            ),
            "объективный": (
                "objective, impartial",
                "Будь объективным.",
                "Be objective.",
            ),
            "трагедия": ("tragedy", "Это трагедия.", "It's a tragedy."),
            "уезжать": (
                "to leave, to depart",
                "Мне нужно уезжать завтра утром.",
                "I need to leave tomorrow morning.",
            ),
            "священный": (
                "sacred, holy",
                "Это священное место.",
                "This is a sacred place.",
            ),
            "жаловаться": ("to complain", "Хватит жаловаться.", "Stop complaining."),
            "четверг": ("Thursday", "До четверга.", "See you Thursday."),
            "фестиваль": (
                "festival",
                "Пойдём на фестиваль?",
                "Want to go to the festival?",
            ),
            "ненависть": (
                "hatred, hate",
                "Это уже ненависть.",
                "That's hatred at this point.",
            ),
            "холм": ("hill", "Дом на холме.", "The house is on the hill."),
            "частота": ("frequency", "Какая частота?", "What's the frequency?"),
            "вечерний": ("evening", "Вечерний поезд.", "The evening train."),
            "контекст": (
                "context",
                "Без контекста не ясно.",
                "Without context it's unclear.",
            ),
            "копия": ("copy", "Где копия?", "Where's the copy?"),
            "удовлетворение": (
                "satisfaction",
                "Никакого удовлетворения.",
                "No satisfaction at all.",
            ),
            "направиться": (
                "to head",
                "Мы направились к выходу.",
                "We headed for the exit.",
            ),
            "узел": ("knot", "Свяжи узел.", "Tie a knot."),
            "испытать": (
                "to experience, to undergo",
                "Я такое уже испытал.",
                "I've already experienced that.",
            ),
            "психолог": (
                "psychologist",
                "Психолог мне очень помог.",
                "The psychologist helped me a lot.",
            ),
            "вред": ("harm", "В этом нет вреда.", "There's no harm in that."),
            "жалко": (
                "pity, sorry",
                "Жалко, что она не смогла прийти.",
                "It's a pity she couldn't come.",
            ),
            "финансирование": (
                "funding",
                "Без финансирования никак.",
                "No way without funding.",
            ),
            "нигде": (
                "nowhere, anywhere",
                "Его нигде не найти.",
                "He is nowhere to be found.",
            ),
            "неплохо": ("not bad, pretty good", "Совсем неплохо.", "Not bad at all."),
            "побывать": ("to visit, to stop by", "Побывай у нас.", "Come visit us."),
            "идеология": (
                "ideology",
                "Это уже идеология.",
                "That's already ideology.",
            ),
            "зарегистрировать": (
                "to register",
                "Надо зарегистрировать машину.",
                "We need to register the car.",
            ),
            "командование": (
                "command",
                "Командование молчит.",
                "Command is silent.",
            ),
            "отрицательный": (
                "negative",
                "Результат отрицательный.",
                "The result is negative.",
            ),
            "создаваться": (
                "to be created, to take shape",
                "Команда ещё создаётся.",
                "The team is still taking shape.",
            ),
            "убеждение": (
                "conviction, belief",
                "Это моё убеждение.",
                "That's my conviction.",
            ),
            "звание": ("rank, title", "Какое у него звание?", "What's his rank?"),
            "высоко": ("high, highly", "Слишком высоко.", "Too high."),
            "жалеть": (
                "to regret, to pity",
                "Я жалею, что сказал.",
                "I regret saying that.",
            ),
            "скала": ("cliff, rock", "Там скала.", "There's a cliff there."),
            "вторник": ("Tuesday", "Давай во вторник.", "Let's do Tuesday."),
            "выше": ("higher, above", "Поставь выше.", "Put it higher."),
            "непременно": (
                "without fail, certainly",
                "Я непременно приду.",
                "I'll certainly come.",
            ),
            "обвинение": (
                "accusation, charge",
                "Какое обвинение?",
                "What's the charge?",
            ),
            "искусственный": (
                "artificial",
                "Это искусственный свет?",
                "Is this artificial light?",
            ),
            "вынести": (
                "to take out, to carry out",
                "Вынеси это отсюда.",
                "Take this out of here.",
            ),
            "исключить": ("to exclude", "Исключи его.", "Exclude him."),
            "литр": ("liter, litre", "Я купил литр молока.", "I bought a liter of milk."),
            "учебник": (
                "textbook",
                "Она забыла свой учебник дома.",
                "She forgot her textbook at home.",
            ),
            "тьма": ("darkness", "Какая тьма!", "What darkness!"),
            "превышать": (
                "to exceed",
                "Не превышай скорость.",
                "Don't exceed the speed limit.",
            ),
            "лента": ("ribbon, tape", "Свяжи ленту.", "Tie the ribbon."),
            "христианский": (
                "Christian",
                "Это христианский праздник.",
                "It's a Christian holiday.",
            ),
            "недостаточно": (
                "not enough",
                "Этого недостаточно.",
                "That's not enough.",
            ),
            "готовность": ("readiness", "Полная готовность.", "Full readiness."),
            "начальство": (
                "the bosses, management",
                "Начальство не в курсе.",
                "The bosses don't know.",
            ),
            "удивить": (
                "to surprise, to astonish",
                "Подарок удивит её.",
                "The gift will surprise her.",
            ),
            "проявляться": (
                "to show, to appear",
                "Это сразу проявляется.",
                "It shows right away.",
            ),
            "лесной": ("forest", "Лесная дорога.", "A forest road."),
            "исполнять": ("to perform", "Кто будет исполнять?", "Who's performing?"),
            "нагрузка": (
                "load, burden",
                "Большая нагрузка сегодня.",
                "A big load today.",
            ),
            "объединить": (
                "to unite, to combine",
                "Давай объединим.",
                "Let's combine them.",
            ),
            "зарубежный": (
                "foreign, overseas",
                "Она любит зарубежные фильмы.",
                "She loves foreign movies.",
            ),
            "душевный": ("warm, heartfelt", "Он очень душевный.", "He's really warm."),
            "раб": ("slave", "Я там как раб.", "I'm like a slave there."),
            "корреспондент": (
                "correspondent, reporter",
                "Он корреспондент.",
                "He's a correspondent.",
            ),
            "спутник": (
                "satellite",
                "Спутник не отвечает.",
                "The satellite isn't answering.",
            ),
            "цепь": ("chain", "Где цепь?", "Where's the chain?"),
            "пропустить": (
                "to miss, to skip",
                "Я снова пропущу поезд.",
                "I'll miss the train again.",
            ),
            "потенциальный": (
                "potential",
                "Это потенциальный клиент.",
                "That's a potential client.",
            ),
            "приниматься": (
                "to set about, to get down to",
                "Пора приниматься за работу.",
                "Time to get down to work.",
            ),
            "розовый": ("pink", "Розовый или красный?", "Pink or red?"),
            "почитать": (
                "to read (a bit)",
                "Я люблю почитать перед сном.",
                "I love to read before bed.",
            ),
            "идеал": ("ideal", "Он не мой идеал.", "He's not my ideal."),
            "благодарить": ("to thank", "Не надо благодарить.", "No need to thank me."),
            "эпизод": (
                "episode",
                "Я посмотрел последний эпизод вчера.",
                "I watched the last episode yesterday.",
            ),
            "вечно": ("forever, always", "Он вечно на работе.", "He's always at work."),
            "учесть": (
                "to take into account",
                "Надо это учесть.",
                "We need to take that into account.",
            ),
            "сетевой": ("network", "Нужен сетевой доступ.", "I need network access."),
            "визит": ("visit", "Визит к врачу.", "A visit to the doctor."),
            "орден": ("medal, order", "Ему дали орден.", "They gave him a medal."),
            "конкуренция": (
                "competition",
                "Большая конкуренция.",
                "There's a lot of competition.",
            ),
            "колонна": ("column", "За колонной.", "Behind the column."),
            "парламент": (
                "parliament",
                "Что там в парламенте?",
                "What's going on in parliament?",
            ),
            "собор": (
                "cathedral",
                "Встретимся у собора.",
                "Let's meet at the cathedral.",
            ),
            "танцевать": ("to dance", "Пойдём танцевать?", "Want to go dancing?"),
            "соревнование": (
                "competition, contest",
                "Кто выиграл соревнование?",
                "Who won the contest?",
            ),
            "произносить": (
                "to pronounce",
                "Как это произносить?",
                "How do you pronounce that?",
            ),
        },
    )
)
