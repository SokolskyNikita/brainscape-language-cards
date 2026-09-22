import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from russian_english._chunk_io import rewrite_chunk

print(
    rewrite_chunk(
        Path("russian_english/_chunks/deck_15260192_02.csv"),
        {
            "глупость": (
                "foolishness, stupidity",
                "Какая глупость!",
                "What foolishness!",
            ),
            "эмоциональный": (
                "emotional",
                "Он такой эмоциональный.",
                "He's so emotional.",
            ),
            "перенести": (
                "to postpone, to reschedule",
                "Давай перенесём на завтра.",
                "Let's postpone it until tomorrow.",
            ),
            "городок": (
                "small town",
                "Милый городок.",
                "Nice small town.",
            ),
            "подтверждать": (
                "to confirm",
                "Подтверждаешь?",
                "Can you confirm?",
            ),
            "распределение": (
                "distribution, allocation",
                "Странное распределение.",
                "Strange allocation.",
            ),
            "отправляться": (
                "to set off, to depart",
                "Когда отправляемся?",
                "When do we set off?",
            ),
            "любитель": (
                "amateur, enthusiast",
                "Он любитель музыки.",
                "He's a music enthusiast.",
            ),
            "бар": ("bar", "Давай в бар.", "Let's go to the bar."),
            "неизвестно": (
                "unknown",
                "Неизвестно, где он.",
                "It's unknown where he is.",
            ),
            "приличный": (
                "decent, respectable",
                "Он приличный человек.",
                "He's a decent person.",
            ),
            "содержаться": (
                "to be contained",
                "Что там содержится?",
                "What's contained there?",
            ),
            "обзор": (
                "review, overview",
                "Читал обзор?",
                "Did you read the review?",
            ),
            "претензия": (
                "complaint, claim",
                "У меня претензия.",
                "I have a complaint.",
            ),
            "позвать": (
                "to call over, to invite",
                "Позови его.",
                "Call him over.",
            ),
            "нападение": (
                "attack, assault",
                "Это было нападение.",
                "That was an attack.",
            ),
            "рассматриваться": (
                "to be considered",
                "Это ещё рассматривается.",
                "That's still being considered.",
            ),
            "рубашка": ("shirt", "Где моя рубашка?", "Where's my shirt?"),
            "итальянский": ("Italian", "Это итальянский?", "Is this Italian?"),
            "тоска": (
                "melancholy, boredom",
                "Какая тоска.",
                "What boredom.",
            ),
            "завтрак": (
                "breakfast",
                "Что на завтрак?",
                "What's for breakfast?",
            ),
            "ниже": ("below, lower", "Поставь ниже.", "Put it lower."),
            "пенсия": ("pension", "Когда пенсия?", "When's the pension?"),
            "восстановление": (
                "recovery, restoration",
                "Восстановление идёт.",
                "Recovery is going on.",
            ),
            "турист": ("tourist", "Он турист?", "Is he a tourist?"),
            "инвестор": ("investor", "Нужен инвестор.", "We need an investor."),
            "переживание": (
                "worry, feeling",
                "Хватит переживаний.",
                "Enough of the worry.",
            ),
            "сравнить": ("to compare", "Давай сравним.", "Let's compare."),
            "мода": (
                "fashion",
                "Это уже не мода.",
                "That's out of fashion.",
            ),
            "заложить": (
                "to pawn, to mortgage",
                "Пришлось заложить часы.",
                "Had to pawn the watch.",
            ),
            "разработчик": ("developer", "Он разработчик.", "He's a developer."),
            "везти": (
                "to take (by vehicle)",
                "Куда это везти?",
                "Where should I take this?",
            ),
            "рисовать": (
                "to draw",
                "Не рисуй на столе.",
                "Don't draw on the table.",
            ),
            "возникновение": (
                "emergence, onset",
                "С момента возникновения.",
                "Since the emergence.",
            ),
            "вестись": (
                "to fall for",
                "Не ведись на это.",
                "Don't fall for that.",
            ),
            "заказать": ("to order, to book", "Закажи чай.", "Order tea."),
            "стенка": (
                "wall, wall unit",
                "Поставь у стенки.",
                "Put it by the wall.",
            ),
            "узнавать": (
                "to recognize, to find out",
                "Узнаёшь его?",
                "Do you recognize him?",
            ),
            "ведение": (
                "management, keeping",
                "Ведение дел за ним.",
                "The management is his.",
            ),
            "единство": ("unity", "Нам нужно единство.", "We need unity."),
            "мощность": (
                "power, capacity",
                "Не хватает мощности.",
                "There isn't enough power.",
            ),
            "здорово": (
                "great, cool",
                "Здорово придумал!",
                "That's great!",
            ),
            "иностранец": (
                "foreigner",
                "Он иностранец?",
                "Is he a foreigner?",
            ),
            "статистика": (
                "statistics",
                "По статистике — да.",
                "According to the statistics, yes.",
            ),
            "предупредить": (
                "to warn",
                "Надо было предупредить.",
                "You should have warned me.",
            ),
            "волноваться": ("to worry", "Не волнуйся.", "Don't worry."),
            "музыкант": ("musician", "Он музыкант.", "He's a musician."),
            "пьеса": ("play", "Идёшь на пьесу?", "Going to the play?"),
            "десятилетие": (
                "decade",
                "Прошло уже десятилетие.",
                "A decade has already passed.",
            ),
            "пожать": (
                "to shake, to squeeze",
                "Давай пожмём руки.",
                "Let's shake on it.",
            ),
            "осознать": ("to realize", "Я это осознал.", "I realized that."),
            "блестящий": ("brilliant", "Блестящая идея!", "Brilliant idea!"),
            "убийца": (
                "killer, murderer",
                "Убийцу поймали.",
                "They caught the killer.",
            ),
            "известие": ("news", "Слышал известие?", "Did you hear the news?"),
            "печальный": ("sad", "Какой печальный день.", "What a sad day."),
            "улучшение": (
                "improvement",
                "Есть улучшение?",
                "Any improvement?",
            ),
            "яблоко": ("apple", "Хочешь яблоко?", "Want an apple?"),
            "слева": ("on the left", "Он слева.", "He's on the left."),
            "заявлять": (
                "to declare, to claim",
                "Он заявляет, что не виноват.",
                "He claims he's not guilty.",
            ),
            "местность": (
                "area, terrain",
                "Знакомая местность.",
                "Familiar area.",
            ),
            "экспедиция": (
                "expedition",
                "Они ушли в экспедицию.",
                "They left on an expedition.",
            ),
            "зарабатывать": (
                "to earn",
                "Сколько ты зарабатываешь?",
                "How much do you earn?",
            ),
            "прогресс": ("progress", "Есть прогресс?", "Any progress?"),
            "цитировать": (
                "to quote, to cite",
                "Не цитируй меня.",
                "Don't quote me.",
            ),
            "пояс": ("belt", "Где мой пояс?", "Where's my belt?"),
            "королева": (
                "queen",
                "Она как королева.",
                "She's like a queen.",
            ),
            "квадратный": ("square", "Квадратный стол?", "A square table?"),
            "заинтересовать": (
                "to interest",
                "Чем тебя заинтересовать?",
                "What would interest you?",
            ),
            "выгодный": (
                "profitable, worthwhile",
                "Выгодное предложение.",
                "A profitable offer.",
            ),
            "начальный": (
                "initial, beginner",
                "Это начальный уровень.",
                "That's beginner level.",
            ),
            "старуха": (
                "old woman",
                "Там живёт старуха.",
                "An old woman lives there.",
            ),
            "ограничить": (
                "to limit, to restrict",
                "Надо ограничить расход.",
                "We need to limit the expense.",
            ),
            "нежели": (
                "than",
                "Сейчас, нежели потом.",
                "Now rather than later.",
            ),
            "аэродром": (
                "airfield",
                "Мы уже на аэродроме.",
                "We're already at the airfield.",
            ),
            "делиться": (
                "to share",
                "Не люблю делиться.",
                "I don't like to share.",
            ),
            "допускать": (
                "to allow, to admit",
                "Не допускай этого.",
                "Don't allow that.",
            ),
            "торопиться": ("to hurry", "Я тороплюсь.", "I'm in a hurry."),
            "реагировать": (
                "to react",
                "Он не реагирует.",
                "He's not reacting.",
            ),
            "союзник": ("ally", "Он наш союзник.", "He's our ally."),
            "раскрыть": (
                "to reveal",
                "Не раскрывай секрет.",
                "Don't reveal the secret.",
            ),
            "корпорация": (
                "corporation",
                "Большая корпорация.",
                "A big corporation.",
            ),
            "временной": (
                "time-related, temporal",
                "Это временной ряд.",
                "That's a time series.",
            ),
            "надоесть": (
                "to get tired of",
                "Мне это надоело.",
                "I'm tired of this.",
            ),
            "задержать": (
                "to delay, to detain",
                "Не задерживай меня.",
                "Don't delay me.",
            ),
            "сапог": ("boot", "Где второй сапог?", "Where's the other boot?"),
            "мелочь": (
                "small change, trifle",
                "Есть мелочь?",
                "Got any change?",
            ),
            "складываться": (
                "to work out, to take shape",
                "Всё складывается.",
                "It's all working out.",
            ),
            "дисциплина": (
                "discipline",
                "Нет дисциплины.",
                "There's no discipline.",
            ),
            "справа": ("on the right", "Он справа.", "He's on the right."),
            "транспортный": (
                "transport (adj.)",
                "Транспортная карта?",
                "A transport card?",
            ),
            "вначале": (
                "at first",
                "Вначале я не понял.",
                "At first I didn't understand.",
            ),
            "аэропорт": (
                "airport",
                "Встреть меня в аэропорту.",
                "Meet me at the airport.",
            ),
            "сокращение": (
                "layoff, reduction",
                "Идут сокращения.",
                "There are layoffs.",
            ),
            "вовремя": (
                "on time",
                "Ты как раз вовремя.",
                "You're right on time.",
            ),
            "миф": ("myth", "Это миф.", "That's a myth."),
            "свободно": (
                "free, vacant",
                "Здесь свободно?",
                "Is this vacant?",
            ),
            "авторский": (
                "author's, original",
                "Авторский проект.",
                "An original project.",
            ),
            "сбить": (
                "to knock down, to throw off",
                "Его сбили.",
                "They knocked him down.",
            ),
            "кусочек": (
                "little piece",
                "Хочешь кусочек?",
                "Want a little piece?",
            ),
            "неплохой": (
                "not bad, decent",
                "Фильм совсем неплохой.",
                "The movie's not bad at all.",
            ),
        },
    )
)
