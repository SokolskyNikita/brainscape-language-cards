import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from russian_english._chunk_io import rewrite_chunk

print(
    rewrite_chunk(
        Path("russian_english/_chunks/deck_15260194_02.csv"),
        {
            "оформление": (
                "design",
                "Мне нравится это оформление.",
                "I like this design.",
            ),
            "подушка": ("pillow", "Где моя подушка?", "Where's my pillow?"),
            "соглашаться": ("to agree", "Я не соглашаюсь.", "I don't agree."),
            "полагаться": ("to rely", "Я полагаюсь на тебя.", "I rely on you."),
            "замысел": ("plan", "Его замысел ясен.", "His plan is clear."),
            "цветной": (
                "colored",
                "Это цветной рисунок.",
                "That's a colored drawing.",
            ),
            "манера": (
                "manner",
                "Мне не нравится его манера.",
                "I don't like his manner.",
            ),
            "возразить": ("to object", "Я хочу возразить.", "I want to object."),
            "призыв": ("call", "Я слышал его призыв.", "I heard his call."),
            "утвердить": (
                "to approve",
                "Они утвердили план.",
                "They approved the plan.",
            ),
            "греческий": (
                "Greek",
                "Это греческий язык.",
                "That's the Greek language.",
            ),
            "строиться": (
                "to be built",
                "Дом ещё строится.",
                "The house is still being built.",
            ),
            "талантливый": (
                "talented",
                "Он талантливый артист.",
                "He's a talented artist.",
            ),
            "ничего": ("nothing", "Я ничего не знаю.", "I know nothing."),
            "монитор": (
                "monitor",
                "Монитор на столе.",
                "The monitor is on the table.",
            ),
            "дракон": ("dragon", "Это большой дракон.", "That's a big dragon."),
            "регулярно": ("regularly", "Я регулярно читаю.", "I read regularly."),
            "выставить": (
                "to display",
                "Выставь картину.",
                "Display the picture.",
            ),
            "препятствие": (
                "obstacle",
                "Это большое препятствие.",
                "That's a big obstacle.",
            ),
            "волшебный": (
                "magical",
                "Это волшебный вечер.",
                "That's a magical evening.",
            ),
            "истребитель": (
                "fighter",
                "Истребитель летит высоко.",
                "The fighter flies high.",
            ),
            "матч": ("match", "Кто выиграл матч?", "Who won the match?"),
            "фонарь": ("lantern", "Фонарь горит.", "The lantern burns."),
            "официально": (
                "officially",
                "Он официально сказал нет.",
                "He officially said no.",
            ),
            "подтверждение": (
                "confirmation",
                "Где подтверждение?",
                "Where's the confirmation?",
            ),
            "седьмой": (
                "seventh",
                "Это седьмой день.",
                "That's the seventh day.",
            ),
            "лифт": (
                "elevator",
                "Лифт не работает.",
                "The elevator doesn't work.",
            ),
            "производиться": (
                "to be produced",
                "Хлеб производится здесь.",
                "Bread is produced here.",
            ),
            "указанный": (
                "specified",
                "Это указанный адрес.",
                "That's the specified address.",
            ),
            "длиться": (
                "to last",
                "Встреча будет длиться час.",
                "The meeting will last an hour.",
            ),
            "настроить": ("to adjust", "Настрой звук.", "Adjust the sound."),
            "департамент": (
                "department",
                "Он работает в департаменте.",
                "He works in the department.",
            ),
            "флаг": ("flag", "Где наш флаг?", "Where's our flag?"),
            "владение": (
                "possession",
                "Это его владение.",
                "That's his possession.",
            ),
            "элита": ("elite", "Элита собралась здесь.", "The elite gathered here."),
            "батарея": ("battery", "Батарея слабая.", "The battery is weak."),
            "приключение": (
                "adventure",
                "Это большое приключение.",
                "That's a big adventure.",
            ),
            "пособие": (
                "benefit",
                "Она получает пособие.",
                "She receives a benefit.",
            ),
            "сервис": ("service", "Сервис хороший.", "The service is good."),
            "любопытный": (
                "curious",
                "Он очень любопытный.",
                "He's very curious.",
            ),
            "покидать": (
                "to leave",
                "Я не хочу покидать дом.",
                "I don't want to leave the house.",
            ),
            "успевать": ("to manage", "Я едва успеваю.", "I barely manage."),
            "коммунистический": (
                "communist",
                "Это коммунистическая партия.",
                "That's the communist party.",
            ),
            "мудрый": ("wise", "Он мудрый человек.", "He's a wise person."),
            "нормально": ("okay", "Всё нормально.", "It's okay."),
            "пускать": ("to let", "Они не пускают нас.", "They don't let us in."),
            "бледный": ("pale", "Его лицо бледное.", "His face is pale."),
            "вор": ("thief", "Вор бежит.", "The thief is running."),
            "обрести": ("to gain", "Она обрела силу.", "She gained strength."),
            "дорожка": ("path", "Иди по дорожке.", "Go along the path."),
            "послание": (
                "message",
                "Я читал его послание.",
                "I read his message.",
            ),
            "внук": ("grandson", "Мой внук дома.", "My grandson is home."),
            "выражаться": (
                "to express",
                "Он плохо выражается.",
                "He expresses himself badly.",
            ),
            "неприятность": (
                "trouble",
                "Это большая неприятность.",
                "That's big trouble.",
            ),
            "окончить": (
                "to finish",
                "Он окончил школу.",
                "He finished school.",
            ),
            "рассвет": ("dawn", "Я встал на рассвете.", "I got up at dawn."),
            "склон": ("slope", "Дом на склоне.", "The house is on the slope."),
            "провинция": (
                "province",
                "Он живёт в провинции.",
                "He lives in the province.",
            ),
            "сформулировать": (
                "to formulate",
                "Сформулируй вопрос.",
                "Formulate the question.",
            ),
            "дабы": (
                "in order to",
                "Он ушёл, дабы отдохнуть.",
                "He left in order to rest.",
            ),
            "недалеко": ("not far", "Дом недалеко.", "The house is not far."),
            "подряд": ("in a row", "Три дня подряд.", "Three days in a row."),
            "пляж": ("beach", "Мы на пляже.", "We're at the beach."),
            "попасться": ("to get caught", "Вор попался.", "The thief got caught."),
            "выжить": ("to survive", "Как он выжил?", "How did he survive?"),
            "кончить": ("to finish", "Я кончил работу.", "I finished the work."),
            "благодарный": (
                "grateful",
                "Он благодарный сын.",
                "He's a grateful son.",
            ),
            "хозяйственный": (
                "household",
                "Это хозяйственный магазин.",
                "That's a household store.",
            ),
            "поинтересоваться": (
                "to inquire",
                "Я поинтересовался ценой.",
                "I inquired about the price.",
            ),
            "перо": (
                "feather",
                "Перо птицы на столе.",
                "The bird's feather is on the table.",
            ),
            "модный": (
                "fashionable",
                "Это модное платье.",
                "That's a fashionable dress.",
            ),
            "переставать": (
                "to stop",
                "Дождь не перестаёт.",
                "The rain doesn't stop.",
            ),
            "игровой": ("game", "Это игровая комната.", "That's a game room."),
            "толк": ("sense", "В этом нет толка.", "There's no sense in this."),
            "спасать": ("to save", "Спасай его.", "Save him."),
            "избегать": ("to avoid", "Я избегаю его.", "I avoid him."),
            "гордиться": (
                "to be proud of",
                "Я горжусь тобой.",
                "I'm proud of you.",
            ),
            "заполнить": ("to fill in", "Заполни форму.", "Fill in the form."),
            "маркетинг": (
                "marketing",
                "Он работает в маркетинге.",
                "He works in marketing.",
            ),
            "железнодорожный": (
                "railway",
                "Это железнодорожная станция.",
                "That's a railway station.",
            ),
            "браться": (
                "to undertake",
                "Я берусь за работу.",
                "I undertake the work.",
            ),
            "книжный": (
                "book",
                "Это книжный магазин.",
                "That's a book store.",
            ),
            "любопытство": (
                "curiosity",
                "Это просто любопытство.",
                "That's just curiosity.",
            ),
            "предполагаться": (
                "to be supposed",
                "Дождь предполагается.",
                "Rain is supposed.",
            ),
            "ритм": ("rhythm", "Мне нравится этот ритм.", "I like this rhythm."),
            "завершение": (
                "completion",
                "Это завершение работы.",
                "That's the completion of the work.",
            ),
            "подвиг": ("feat", "Это настоящий подвиг.", "That's a real feat."),
            "нерв": ("nerve", "У меня слабые нервы.", "I have weak nerves."),
            "водить": ("to drive", "Он водит машину.", "He drives a car."),
            "обмануть": ("to trick", "Он обманул меня.", "He tricked me."),
            "пилот": ("pilot", "Пилот готов.", "The pilot is ready."),
            "отзыв": ("review", "Напиши отзыв.", "Write a review."),
            "голосование": (
                "voting",
                "Голосование уже идёт.",
                "Voting is already going on.",
            ),
            "миссис": ("Mrs.", "Миссис ждёт.", "Mrs. is waiting."),
            "христианин": ("Christian", "Он христианин.", "He's a Christian."),
            "стыдно": ("ashamed", "Мне стыдно.", "I'm ashamed."),
            "иллюзия": (
                "illusion",
                "Это только иллюзия.",
                "That's only an illusion.",
            ),
            "гений": ("genius", "Он настоящий гений.", "He's a real genius."),
            "плавать": ("to swim", "Я люблю плавать.", "I love to swim."),
            "держава": (
                "power",
                "Это великая держава.",
                "That's a great power.",
            ),
        },
    )
)
