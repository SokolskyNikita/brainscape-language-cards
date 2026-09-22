import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from russian_english._chunk_io import rewrite_chunk

print(
    rewrite_chunk(
        Path("russian_english/_chunks/deck_15260210_02.csv"),
        {
            "динамический": (
                "dynamic",
                "Это динамическая система.",
                "This is a dynamic system.",
            ),
            "контур": (
                "contour",
                "Вот контур горы.",
                "Here is the mountain's contour.",
            ),
            "гудеть": (
                "to hum",
                "Холодильник гудит.",
                "The fridge hums.",
            ),
            "раковина": (
                "sink",
                "Он моет руки в раковине.",
                "He washes his hands in the sink.",
            ),
            "выдержка": (
                "restraint",
                "Ему нужна выдержка.",
                "He needs restraint.",
            ),
            "ячейка": (
                "cell",
                "Это пустая ячейка.",
                "This is an empty cell.",
            ),
            "моментально": (
                "instantly",
                "Он моментально понял.",
                "He understood instantly.",
            ),
            "зрелый": (
                "ripe",
                "Яблоко уже зрелое.",
                "The apple is already ripe.",
            ),
            "проигрывать": (
                "to lose",
                "Он не хочет проигрывать.",
                "He does not want to lose.",
            ),
            "аккуратный": (
                "neat",
                "Стол очень аккуратный.",
                "The table is very neat.",
            ),
            "смениться": (
                "to change",
                "Погода быстро сменилась.",
                "The weather changed quickly.",
            ),
            "страховка": (
                "insurance",
                "Я купил страховку.",
                "I bought insurance.",
            ),
            "тактический": (
                "tactical",
                "Это тактический шаг.",
                "This is a tactical step.",
            ),
            "фигурка": (
                "figurine",
                "Вот маленькая фигурка.",
                "Here is a small figurine.",
            ),
            "набраться": (
                "to gather",
                "Мне нужно набраться сил.",
                "I need to gather strength.",
            ),
            "базироваться": (
                "to be based",
                "История базируется на фактах.",
                "The story is based on facts.",
            ),
            "лабиринт": (
                "maze",
                "Это сложный лабиринт.",
                "This is a complex maze.",
            ),
            "побить": (
                "to beat",
                "Он побил рекорд.",
                "He beat the record.",
            ),
            "прислушаться": (
                "to listen",
                "Прислушайся к сердцу.",
                "Listen to your heart.",
            ),
            "разбросать": (
                "to scatter",
                "Он разбросал книги.",
                "He scattered the books.",
            ),
            "ремесло": (
                "craft",
                "Это старое ремесло.",
                "This is an old craft.",
            ),
            "затрагивать": (
                "to affect",
                "Это затрагивает нас.",
                "This affects us.",
            ),
            "ослабить": (
                "to weaken",
                "Болезнь ослабила его.",
                "The illness weakened him.",
            ),
            "целоваться": (
                "to kiss",
                "Они хотят целоваться.",
                "They want to kiss.",
            ),
            "обыск": (
                "search",
                "Это обыск.",
                "This is a search.",
            ),
            "терпеливо": (
                "patiently",
                "Она терпеливо ждёт.",
                "She waits patiently.",
            ),
            "попить": (
                "to drink",
                "Мне нужно попить воды.",
                "I need to drink some water.",
            ),
            "выигрыш": (
                "win",
                "Это большой выигрыш.",
                "This is a big win.",
            ),
            "выбираться": (
                "to get out",
                "Нам надо выбираться.",
                "We need to get out.",
            ),
            "обретать": (
                "to gain",
                "Он обретает силу.",
                "He is gaining strength.",
            ),
            "акционерный": (
                "joint-stock",
                "Это акционерная компания.",
                "This is a joint-stock company.",
            ),
            "взорвать": (
                "to blow up",
                "Они хотят взорвать мост.",
                "They want to blow up the bridge.",
            ),
            "рабство": (
                "slavery",
                "Рабства уже нет.",
                "There is no slavery now.",
            ),
            "вытереть": (
                "to wipe",
                "Вытри стол.",
                "Wipe the table.",
            ),
            "подвергнуть": (
                "to subject",
                "Его подвергли допросу.",
                "They subjected him to questioning.",
            ),
            "каюта": (
                "cabin",
                "Наша каюта маленькая.",
                "Our cabin is small.",
            ),
            "попадание": (
                "hit",
                "Это прямое попадание.",
                "This is a direct hit.",
            ),
            "чувствительность": (
                "sensitivity",
                "Чувствительность кожи высокая.",
                "Skin sensitivity is high.",
            ),
            "окоп": (
                "trench",
                "Солдаты сидят в окопе.",
                "The soldiers sit in the trench.",
            ),
            "практиковать": (
                "to practice",
                "Она практикует каждый день.",
                "She practices every day.",
            ),
            "конфигурация": (
                "configuration",
                "Это новая конфигурация.",
                "This is a new configuration.",
            ),
            "надзор": (
                "supervision",
                "Он под надзором.",
                "He is under supervision.",
            ),
            "приказывать": (
                "to order",
                "Не приказывай мне.",
                "Do not order me.",
            ),
            "ярмарка": (
                "fair",
                "Мы на ярмарке.",
                "We are at the fair.",
            ),
            "экспозиция": (
                "exhibition",
                "Я видел эту экспозицию.",
                "I saw this exhibition.",
            ),
            "заключительный": (
                "final",
                "Это заключительный день.",
                "This is the final day.",
            ),
            "хроника": (
                "chronicle",
                "Я читал древнюю хронику.",
                "I read an ancient chronicle.",
            ),
            "скульптура": (
                "sculpture",
                "В парке новая скульптура.",
                "There is a new sculpture in the park.",
            ),
            "распорядиться": (
                "to manage",
                "Он распорядится этим.",
                "He will manage this.",
            ),
            "неприятно": (
                "unpleasant",
                "Мне это неприятно.",
                "This is unpleasant to me.",
            ),
            "библейский": (
                "biblical",
                "Это библейская история.",
                "This is a biblical story.",
            ),
            "косвенный": (
                "indirect",
                "Это косвенный вопрос.",
                "This is an indirect question.",
            ),
            "инспекция": (
                "inspection",
                "Машина прошла инспекцию.",
                "The car passed inspection.",
            ),
            "откладывать": (
                "to postpone",
                "Мы откладываем встречу.",
                "We are postponing the meeting.",
            ),
            "органический": (
                "organic",
                "Я люблю органические фрукты.",
                "I like organic fruit.",
            ),
            "отказывать": (
                "to refuse",
                "Он мне отказывает.",
                "He refuses me.",
            ),
            "прорваться": (
                "to break through",
                "Они прорвались.",
                "They broke through.",
            ),
            "лгать": (
                "to lie",
                "Не надо лгать.",
                "Do not lie.",
            ),
            "читаться": (
                "to read",
                "Книга хорошо читается.",
                "The book reads well.",
            ),
            "разбойник": (
                "bandit",
                "Разбойник в лесу.",
                "The bandit is in the forest.",
            ),
            "переходный": (
                "transitional",
                "Это переходный период.",
                "This is a transitional period.",
            ),
            "скамья": (
                "bench",
                "Садись на скамью.",
                "Sit on the bench.",
            ),
            "погулять": (
                "to walk",
                "Я хочу погулять.",
                "I want to walk.",
            ),
            "обыденный": (
                "ordinary",
                "Это обыденная жизнь.",
                "This is ordinary life.",
            ),
            "свалить": (
                "to dump",
                "Он свалил мусор.",
                "He dumped the trash.",
            ),
            "террористический": (
                "terrorist",
                "Это террористический акт.",
                "This is a terrorist act.",
            ),
            "шоколад": (
                "chocolate",
                "Я люблю шоколад.",
                "I love chocolate.",
            ),
            "броня": (
                "armor",
                "Рыцарь носит броню.",
                "The knight wears armor.",
            ),
            "зрительный": (
                "visual",
                "Это зрительная память.",
                "This is visual memory.",
            ),
            "предисловие": (
                "preface",
                "Прочитай предисловие.",
                "Read the preface.",
            ),
            "пуговица": (
                "button",
                "Дай мне пуговицу.",
                "Give me the button.",
            ),
            "треск": (
                "crack",
                "Это громкий треск.",
                "This is a loud crack.",
            ),
            "произвол": (
                "arbitrariness",
                "Это полный произвол.",
                "This is complete arbitrariness.",
            ),
            "проклятие": (
                "curse",
                "На нём проклятие.",
                "There is a curse on him.",
            ),
            "вдохновение": (
                "inspiration",
                "Мне нужно вдохновение.",
                "I need inspiration.",
            ),
            "ленивый": (
                "lazy",
                "Он очень ленивый.",
                "He is very lazy.",
            ),
            "волшебник": (
                "wizard",
                "Волшебник здесь.",
                "The wizard is here.",
            ),
            "оптимизм": (
                "optimism",
                "У неё есть оптимизм.",
                "She has optimism.",
            ),
            "ошибочный": (
                "mistaken",
                "Это ошибочное решение.",
                "This is a mistaken decision.",
            ),
            "приют": (
                "shelter",
                "Кот в приюте.",
                "The cat is at the shelter.",
            ),
            "особа": (
                "person",
                "Это важная особа.",
                "This is an important person.",
            ),
            "периодический": (
                "periodic",
                "Нужен периодический контроль.",
                "Periodic control is needed.",
            ),
            "привязанность": (
                "attachment",
                "У неё привязанность к коту.",
                "She has an attachment to the cat.",
            ),
            "верста": (
                "verst",
                "До дома десять вёрст.",
                "It is ten versts to the house.",
            ),
            "африканский": (
                "African",
                "Это африканское искусство.",
                "This is African art.",
            ),
            "премьера": (
                "premiere",
                "Премьера завтра.",
                "The premiere is tomorrow.",
            ),
            "унижение": (
                "humiliation",
                "Это унижение.",
                "This is humiliation.",
            ),
            "медитация": (
                "meditation",
                "Мне нужна медитация.",
                "I need meditation.",
            ),
            "расширять": (
                "to expand",
                "Мы расширяем бизнес.",
                "We are expanding the business.",
            ),
            "отводить": (
                "to lead away",
                "Офицер отводит его.",
                "The officer is leading him away.",
            ),
            "банкир": (
                "banker",
                "Банкир здесь.",
                "The banker is here.",
            ),
            "неполный": (
                "incomplete",
                "Работа еще неполная.",
                "The work is still incomplete.",
            ),
            "трактор": (
                "tractor",
                "Я вижу трактор.",
                "I see a tractor.",
            ),
            "думаться": (
                "to seem",
                "Мне так думается.",
                "It seems so to me.",
            ),
            "задолженность": (
                "debt",
                "У него большая задолженность.",
                "He has a large debt.",
            ),
            "обнаружение": (
                "detection",
                "Нужно быстрое обнаружение.",
                "Quick detection is needed.",
            ),
            "общественно": (
                "socially",
                "Это общественно важно.",
                "This is socially important.",
            ),
            "интеллигентный": (
                "cultured",
                "Он интеллигентный человек.",
                "He is a cultured person.",
            ),
            "последователь": (
                "follower",
                "Он мой последователь.",
                "He is my follower.",
            ),
            "восемнадцать": (
                "eighteen",
                "Ей исполнилось восемнадцать.",
                "She turned eighteen.",
            ),
        },
    )
)
