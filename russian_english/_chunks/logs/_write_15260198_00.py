import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from russian_english._chunk_io import rewrite_chunk

print(
    rewrite_chunk(
        Path("russian_english/_chunks/deck_15260198_00.csv"),
        {
            "давить": (
                "to press, to crush",
                "Сапог давит мне ногу.",
                "The boot presses my foot.",
            ),
            "усиление": (
                "intensification, reinforcement",
                "Мы ждали усиления бури.",
                "We waited for the storm's intensification.",
            ),
            "неверный": (
                "unfaithful, incorrect",
                "Он был неверен ей.",
                "He was unfaithful to her.",
            ),
            "группировка": (
                "faction, gang",
                "Эта группировка опасна.",
                "This faction is dangerous.",
            ),
            "люк": ("hatch, manhole", "Открой люк.", "Open the hatch."),
            "восьмой": (
                "eighth, 8th",
                "Она закончила гонку на восьмом месте.",
                "She finished the race in eighth place.",
            ),
            "турецкий": (
                "Turkish, Ottoman",
                "Я люблю турецкий кофе.",
                "I love Turkish coffee.",
            ),
            "претендовать": (
                "claim, aspire",
                "Она будет претендовать на звание чемпиона.",
                "She will claim the championship title.",
            ),
            "отобрать": (
                "take away, confiscate",
                "Они отберут у тебя твои права.",
                "They will take away your rights.",
            ),
            "праздничный": (
                "festive, holiday",
                "Комната выглядела праздничной и яркой.",
                "The room looked festive and bright.",
            ),
            "уста": (
                "lips, mouth",
                "Её уста прошептали тайное обещание.",
                "Her lips whispered a secret promise.",
            ),
            "переехать": (
                "move, relocate",
                "Мы переедем в следующем месяце.",
                "We will move next month.",
            ),
            "квалификация": (
                "qualification, credentials",
                "У него высокая квалификация.",
                "He has a high qualification.",
            ),
            "незначительный": (
                "insignificant, minor",
                "Изменение было незначительным.",
                "The change was insignificant.",
            ),
            "сыр": (
                "cheese, curd",
                "Я ем сыр с хлебом.",
                "I eat cheese with bread.",
            ),
            "незаконный": (
                "illegal, unlawful",
                "Продажа наркотиков незаконна.",
                "Selling drugs is illegal.",
            ),
            "ха": (
                "ha, haha",
                '"Ха, я знал, что ты придешь!"',
                '"Ha, I knew you\'d come!"',
            ),
            "снежный": (
                "snowy, snow",
                "Снежный день был тихим.",
                "The snowy day was quiet.",
            ),
            "президентский": (
                "presidential, president's",
                "Он объявил о своей президентской кампании сегодня.",
                "He announced his presidential campaign today.",
            ),
            "скучно": (
                "boring, dull",
                "Мне здесь скучно.",
                "It is so boring here.",
            ),
            "исключительный": (
                "exceptional, exclusive",
                "У неё исключительный талант в живописи.",
                "She has exceptional talent in painting.",
            ),
            "обман": (
                "deception, fraud",
                "Обман разрушил их доверие.",
                "Deception destroyed their trust.",
            ),
            "зрелище": (
                "spectacle, show",
                "Бой был страшным зрелищем.",
                "The fight was a terrible spectacle.",
            ),
            "национальность": (
                "nationality, ethnicity",
                "Её национальность - русская.",
                "Her nationality is Russian.",
            ),
            "купец": (
                "merchant, trader",
                "Купец продал хлеб.",
                "The merchant sold bread.",
            ),
            "провод": (
                "wire, cable",
                "Провод слишком длинный.",
                "The wire is too long.",
            ),
            "гриб": (
                "mushroom, fungus",
                "Я нашел гриб в лесу.",
                "I found a mushroom in the forest.",
            ),
            "фрукт": (
                "fruit, produce",
                "Я люблю есть свежие фрукты каждый день.",
                "I love eating fresh fruit daily.",
            ),
            "ненужный": (
                "unnecessary, unneeded",
                "Эта встреча абсолютно ненужная.",
                "This meeting is completely unnecessary.",
            ),
            "глянуть": ("look, glance", "Глянь сюда!", "Look here!"),
            "немалый": (
                "significant, considerable",
                "Она внесла немалый вклад.",
                "She made a significant contribution.",
            ),
            "баня": (
                "bathhouse, sauna",
                "Мы отдыхали в местной бане.",
                "We relaxed at the local bathhouse.",
            ),
            "открыто": (
                "openly, open",
                "Он открыто выразил свои мнения.",
                "He openly expressed his opinions.",
            ),
            "миновать": (
                "to pass, to bypass",
                "Опасность скоро минует.",
                "The danger will pass soon.",
            ),
            "передовой": (
                "advanced, cutting-edge",
                "Это передовой метод.",
                "This is an advanced method.",
            ),
            "дарить": (
                "to give, to present",
                "Я люблю дарить подарки.",
                "I love to give gifts.",
            ),
            "потрясать": (
                "shake, amaze",
                "Его слова потрясают нас.",
                "His words shake us.",
            ),
            "тупой": (
                "dull, blunt",
                "Нож слишком тупой, чтобы резать.",
                "The knife is too dull to cut.",
            ),
            "плоский": (
                "flat, plane",
                "Стол совсем плоский.",
                "The table is flat.",
            ),
            "церемония": (
                "ceremony, ritual",
                "Церемония свадьбы была красивой.",
                "The wedding ceremony was beautiful.",
            ),
            "ступенька": (
                "step, rung",
                "Осторожно, ступенька!",
                "Watch your step!",
            ),
            "переносить": (
                "to transfer, to postpone",
                "Мы переносим встречу.",
                "We postpone the meeting.",
            ),
            "большевик": (
                "Bolshevik, Communist",
                "Большевик взял власть.",
                "The Bolshevik took power.",
            ),
            "возбуждение": (
                "excitation, arousal",
                "Его возбуждение росло.",
                "His arousal grew.",
            ),
            "живопись": (
                "painting, fine art",
                "Я люблю живопись.",
                "I love painting.",
            ),
            "советник": (
                "advisor, counselor",
                "Он мой советник.",
                "He is my advisor.",
            ),
            "оригинал": (
                "original, original copy",
                "Я нашел оригинал картины.",
                "I found the original painting.",
            ),
            "предстоящий": (
                "upcoming, forthcoming",
                "Предстоящий бой будет трудным.",
                "The upcoming fight will be hard.",
            ),
            "соперник": (
                "rival, competitor",
                "Он победил своего соперника.",
                "He defeated his rival.",
            ),
            "поручить": (
                "entrust, assign",
                "Я поручу тебе это задание.",
                "I will entrust you with this task.",
            ),
            "балл": (
                "point, score",
                "Он получил высокий балл.",
                "He got a high score.",
            ),
            "бокал": (
                "goblet, wine glass",
                "Он поднял бокал с вином.",
                "He raised the goblet of wine.",
            ),
            "юбка": (
                "skirt, kilt",
                "Она купила новую красную юбку.",
                "She bought a new red skirt.",
            ),
            "экспорт": (
                "export, exports",
                "Экспорт нефти растёт.",
                "Oil export is growing.",
            ),
            "драться": (
                "to fight, to scuffle",
                "Мальчики дрались во дворе.",
                "The boys fought in the yard.",
            ),
            "конституционный": (
                "constitutional, charter",
                "Это конституционный закон.",
                "This is a constitutional law.",
            ),
            "вспышка": (
                "flash, flare",
                "Яркая вспышка осветила небо.",
                "A bright flash lit the sky.",
            ),
            "стабильность": (
                "stability, steadiness",
                "Нам сейчас нужна большая стабильность.",
                "We need more stability now.",
            ),
            "прохожий": (
                "passerby, pedestrian",
                "Прохожий спросил дорогу.",
                "A passerby asked the way.",
            ),
            "разведчик": (
                "scout, intelligence agent",
                "Разведчик видел врага.",
                "The scout saw the enemy.",
            ),
            "нищий": (
                "beggar, pauper",
                "Нищий попросил немного еды.",
                "The beggar asked for some food.",
            ),
            "разрешать": (
                "to allow, to permit",
                "Мать не разрешает мне идти.",
                "Mother does not allow me to go.",
            ),
            "обнаруживать": (
                "to detect, to discover",
                "Собака обнаруживает след.",
                "The dog detects the trail.",
            ),
            "альтернативный": (
                "alternative, alternate",
                "Рассмотрите альтернативное решение.",
                "Consider an alternative solution.",
            ),
            "функциональный": (
                "functional, operational",
                "Приложение теперь полностью функционально.",
                "The app is fully functional now.",
            ),
            "инспектор": (
                "inspector, inspectorate",
                "Инспектор тщательно изучил документы.",
                "The inspector examined the documents carefully.",
            ),
            "налить": (
                "pour, fill",
                "Пожалуйста, налейте мне немного воды.",
                "Please pour me some water.",
            ),
            "понести": (
                "to carry, to bear",
                "Он понёс сумку домой.",
                "He carried the bag home.",
            ),
            "возрасти": (
                "grow, increase",
                "Цены быстро возросли.",
                "Prices grew fast.",
            ),
            "интерпретация": (
                "interpretation, rendition",
                "Это моя интерпретация.",
                "This is my interpretation.",
            ),
            "отвернуться": (
                "turn away, turn around",
                "Она отвернулась от окна.",
                "She turned away from the window.",
            ),
            "свинья": (
                "pig, swine",
                "Свинья лежит в грязи.",
                "The pig lies in the mud.",
            ),
            "потрясти": (
                "shake, impress",
                "Новость потрясет общество.",
                "The news will shake the community.",
            ),
            "рациональный": (
                "rational, reasonable",
                "Выберите рациональное решение.",
                "Choose a rational solution.",
            ),
            "попадаться": (
                "to be caught, to come across",
                "Он старался не попадаться.",
                "He tried not to be caught.",
            ),
            "предъявить": (
                "present, produce",
                "Пожалуйста, предъявите ваш билет.",
                "Please present your ticket.",
            ),
            "скорее": (
                "rather, more likely",
                "Я бы скорее остался дома сегодня.",
                "I'd rather stay home today.",
            ),
            "латинский": (
                "Latin, Latin language",
                "Я изучаю латинский в университете.",
                "I study Latin at university.",
            ),
            "прибавить": (
                "add, increase",
                "Прибавьте сахар к рецепту.",
                "Add sugar to the recipe.",
            ),
            "охотно": (
                "willingly, gladly",
                "Она охотно поделилась своим обедом.",
                "She willingly shared her lunch.",
            ),
            "воспитывать": (
                "to educate, to bring up",
                "Она воспитывает сына.",
                "She brings up her son.",
            ),
            "железо": (
                "iron, metal",
                "Железо - прочный металл.",
                "Iron is a strong metal.",
            ),
            "госпиталь": (
                "hospital, infirmary",
                "Он лежит в госпитале.",
                "He lies in the hospital.",
            ),
            "поменять": (
                "change, exchange",
                "Мне нужно поменять одежду.",
                "I need to change my clothes.",
            ),
            "ванна": (
                "bath, bathtub",
                "Я принимаю ванну.",
                "I take a bath.",
            ),
            "хрен": (
                "horseradish, (slang) damn/darn",
                "Я добавил хрен в суп.",
                "I added horseradish to the soup.",
            ),
            "оторвать": (
                "to tear off, to detach",
                "Она оторвала лист.",
                "She tore off the page.",
            ),
            "климат": (
                "climate, weather",
                "Климат здесь холодный.",
                "The climate here is cold.",
            ),
            "лук": (
                "onion, bow",
                "Я режу лук для супа.",
                "I cut an onion for soup.",
            ),
            "целевой": (
                "target, goal-oriented",
                "Это целевая группа.",
                "This is the target group.",
            ),
            "постройка": (
                "construction, building",
                "Постройка заняла два года.",
                "The construction took two years.",
            ),
            "сопровождаться": (
                "to be accompanied, to be accompanied by",
                "Дождь сопровождался ветром.",
                "The rain was accompanied by wind.",
            ),
            "старость": (
                "old age, senility",
                "Старость приносит мудрость.",
                "Old age brings wisdom.",
            ),
            "разнообразие": (
                "diversity, variety",
                "Я люблю разнообразие.",
                "I love diversity.",
            ),
            "первичный": (
                "primary, initial",
                "Это первичный этап.",
                "This is the primary stage.",
            ),
            "администратор": (
                "administrator, manager",
                "Администратор открыл зал.",
                "The administrator opened the hall.",
            ),
            "сопровождение": (
                "accompaniment, escort",
                "Музыка была её сопровождением.",
                "Music was her accompaniment.",
            ),
            "кожаный": (
                "leather, leather-made",
                "Это кожаная куртка.",
                "This is a leather jacket.",
            ),
            "змея": (
                "snake, serpent",
                "Змея лежит в траве.",
                "The snake lies in the grass.",
            ),
            "грустно": (
                "sadly, sorrowfully",
                "Он грустно сказал это.",
                "He said this sadly.",
            ),
        },
    )
)
