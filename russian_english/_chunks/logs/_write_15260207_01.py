import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from russian_english._chunk_io import rewrite_chunk

print(
    rewrite_chunk(
        Path("russian_english/_chunks/deck_15260207_01.csv"),
        {
            "нервничать": (
                "to be nervous, to fret",
                "Не нервничай.",
                "Don't be nervous.",
            ),
            "мудрец": (
                "wise man, sage",
                "Старый мудрец сказал.",
                "The old wise man said this.",
            ),
            "закрытие": (
                "closing, closure",
                "Закрытие магазина.",
                "The store's closing.",
            ),
            "комсомольский": (
                "Komsomol, Young Communist League",
                "Комсомольская газета.",
                "A Komsomol newspaper.",
            ),
            "продолжительный": (
                "prolonged, extended",
                "Продолжительный день.",
                "A prolonged day.",
            ),
            "наркоман": (
                "drug addict, junkie",
                "Он наркоман.",
                "He is a drug addict.",
            ),
            "скакать": (
                "to jump, to hop",
                "Конь скачет.",
                "The horse jumps.",
            ),
            "беспорядок": (
                "mess, disorder",
                "Какой беспорядок.",
                "What a mess.",
            ),
            "шпион": ("spy, agent", "Он шпион.", "He is a spy."),
            "кипеть": (
                "boil, seethe",
                "Вода кипит.",
                "The water is boiling.",
            ),
            "предельно": (
                "extremely, maximally",
                "Я предельно устал.",
                "I am extremely tired.",
            ),
            "снижаться": (
                "decrease, decline",
                "Цены снижаются.",
                "Prices are decreasing.",
            ),
            "бревно": ("log, timber", "Большое бревно.", "A big log."),
            "туризм": (
                "tourism, travel industry",
                "Туризм растёт.",
                "Tourism is growing.",
            ),
            "го": ("go, let's go", "Го домой.", "Let's go home."),
            "закрыться": (
                "to close, to shut",
                "Магазин закрылся.",
                "The store closed.",
            ),
            "докладывать": (
                "report, inform",
                "Я буду докладывать.",
                "I will report.",
            ),
            "резиновый": (
                "rubber, rubbery",
                "Резиновый мяч.",
                "A rubber ball.",
            ),
            "ноль": ("zero, nil", "Там ноль.", "It's zero there."),
            "ласка": ("caress, affection", "Его ласка.", "His caress."),
            "шедевр": (
                "masterpiece, work of art",
                "Это шедевр.",
                "This is a masterpiece.",
            ),
            "взорваться": (
                "explode, blow up",
                "Бомба взорвалась.",
                "The bomb exploded.",
            ),
            "коса": ("braid, scythe", "У неё коса.", "She has a braid."),
            "удостоверение": (
                "ID, certificate",
                "Вот удостоверение.",
                "Here's my ID.",
            ),
            "каникулы": (
                "holidays, vacation",
                "Скоро каникулы.",
                "Holidays are soon.",
            ),
            "бесчисленный": (
                "innumerable, countless",
                "Бесчисленные звёзды.",
                "Innumerable stars.",
            ),
            "просмотреть": (
                "look through, review",
                "Просмотри письмо.",
                "Look through the letter.",
            ),
            "взамен": (
                "in exchange, in return",
                "Возьми это взамен.",
                "Take this in exchange.",
            ),
            "веко": ("eyelid", "Правое веко.", "The right eyelid."),
            "хлопать": (
                "to clap, to slap",
                "Они хлопают.",
                "They clap.",
            ),
            "допустимый": (
                "permissible, acceptable",
                "Это допустимо.",
                "This is permissible.",
            ),
            "всяческий": (
                "all kinds of, every possible",
                "Всяческая помощь.",
                "All kinds of help.",
            ),
            "избавить": (
                "rid, liberate",
                "Избавь меня от этого.",
                "Rid me of this.",
            ),
            "пролететь": (
                "fly by, pass",
                "День пролетел.",
                "The day flew by.",
            ),
            "классика": (
                "classic, classics",
                "Это классика.",
                "This is a classic.",
            ),
            "пульт": (
                "remote control, console",
                "Где пульт?",
                "Where's the remote control?",
            ),
            "мировоззрение": (
                "worldview, outlook",
                "Его мировоззрение.",
                "His worldview.",
            ),
            "станок": (
                "machine, lathe",
                "Станок работает.",
                "The machine is working.",
            ),
            "поспешно": (
                "hastily, hurriedly",
                "Она поспешно ушла.",
                "She hastily left.",
            ),
            "наткнуться": (
                "stumble upon, come across",
                "Я наткнулся на это.",
                "I stumbled upon this.",
            ),
            "шахта": (
                "mine, shaft",
                "Шахта закрыта.",
                "The mine is closed.",
            ),
            "фашизм": ("fascism", "Это фашизм.", "This is fascism."),
            "полюс": ("pole", "Северный полюс.", "The North Pole."),
            "любовница": (
                "mistress, lover",
                "У него любовница.",
                "He has a mistress.",
            ),
            "алый": (
                "scarlet, crimson",
                "Алый флаг.",
                "A scarlet flag.",
            ),
            "нейтральный": (
                "neutral, impartial",
                "Нейтральный тон.",
                "A neutral tone.",
            ),
            "вторичный": (
                "secondary, secondhand",
                "Вторичный рынок.",
                "The secondary market.",
            ),
            "нехороший": (
                "bad, unpleasant",
                "Нехороший день.",
                "A bad day.",
            ),
            "луг": ("meadow, field", "Большой луг.", "A big meadow."),
            "осматривать": (
                "inspect, examine",
                "Осматривай дом.",
                "Inspect the house.",
            ),
            "футбольный": (
                "football, soccer",
                "Футбольный мяч.",
                "A football.",
            ),
            "военнослужащий": (
                "military personnel, serviceman",
                "Он военнослужащий.",
                "He is a serviceman.",
            ),
            "засунуть": (
                "to put in, to insert",
                "Засунь это сюда.",
                "Put this in here.",
            ),
            "теоретически": (
                "theoretically, in theory",
                "Теоретически да.",
                "Theoretically, yes.",
            ),
            "занести": (
                "bring in, enter",
                "Занеси это.",
                "Bring this in.",
            ),
            "жидкий": (
                "liquid, fluid",
                "Вода жидкая.",
                "Water is liquid.",
            ),
            "грусть": (
                "sadness, melancholy",
                "Какая грусть.",
                "What sadness.",
            ),
            "бессознательный": (
                "unconscious, subconscious",
                "Он бессознательный.",
                "He is unconscious.",
            ),
            "вправо": (
                "to the right, rightward",
                "Иди вправо.",
                "Go to the right.",
            ),
            "насекомое": (
                "insect, bug",
                "Маленькое насекомое.",
                "A small insect.",
            ),
            "партизан": (
                "partisan, guerrilla",
                "Он партизан.",
                "He is a partisan.",
            ),
            "молчаливый": (
                "silent, taciturn",
                "Он молчаливый.",
                "He is silent.",
            ),
            "разбитый": (
                "broken, shattered",
                "Разбитый стакан.",
                "A broken glass.",
            ),
            "убедительный": (
                "convincing, persuasive",
                "Убедительный ответ.",
                "A convincing answer.",
            ),
            "массив": (
                "array, massif",
                "Горный массив.",
                "A mountain massif.",
            ),
            "этакий": ("such, kind of", "Этакий тип.", "Such a guy."),
            "таскать": (
                "drag, haul",
                "Не таскай это.",
                "Don't drag this.",
            ),
            "шагнуть": (
                "to step, to stride",
                "Он шагнул.",
                "He stepped.",
            ),
            "излучение": (
                "radiation, emission",
                "Сильное излучение.",
                "Strong radiation.",
            ),
            "очутиться": (
                "find oneself, end up",
                "Я очутился дома.",
                "I found myself at home.",
            ),
            "армянский": (
                "Armenian",
                "Армянский язык.",
                "The Armenian language.",
            ),
            "фракция": (
                "faction, fraction",
                "Левая фракция.",
                "The left faction.",
            ),
            "разноцветный": (
                "multicolored, variegated",
                "Разноцветный шар.",
                "A multicolored ball.",
            ),
            "гроза": (
                "thunderstorm, storm",
                "Сильная гроза.",
                "A strong thunderstorm.",
            ),
            "торжественно": (
                "solemnly, ceremoniously",
                "Он торжественно сказал.",
                "He solemnly said.",
            ),
            "присылать": (
                "to send, to forward",
                "Они присылают письма.",
                "They send letters.",
            ),
            "прибывать": (
                "to arrive, to come",
                "Поезда прибывают.",
                "The trains arrive.",
            ),
            "возглавить": (
                "to head, to lead",
                "Он возглавил группу.",
                "He headed the group.",
            ),
            "хрупкий": (
                "fragile, brittle",
                "Хрупкий стакан.",
                "A fragile glass.",
            ),
            "выпивать": (
                "to drink, to imbibe",
                "Он любит выпивать.",
                "He likes to drink.",
            ),
            "напиться": (
                "to get drunk, to drink one's fill",
                "Он напился.",
                "He got drunk.",
            ),
            "октябрьский": (
                "October, October's",
                "Октябрьский день.",
                "An October day.",
            ),
            "невыносимый": (
                "unbearable, intolerable",
                "Невыносимый шум.",
                "Unbearable noise.",
            ),
            "сертификат": (
                "certificate, certification",
                "Вот сертификат.",
                "Here's the certificate.",
            ),
            "сказочный": (
                "fairy-tale, fabulous",
                "Сказочный дом.",
                "A fairy-tale house.",
            ),
            "вытаскивать": (
                "to pull out, to extract",
                "Он вытаскивает это.",
                "He pulls this out.",
            ),
            "чайный": (
                "tea, tea-related",
                "Чайный стол.",
                "The tea table.",
            ),
            "мелькать": (
                "flash, flicker",
                "Огни мелькают.",
                "Lights flash.",
            ),
            "запомниться": (
                "to be remembered, to stick in the memory",
                "Это запомнится.",
                "This will be remembered.",
            ),
            "адаптация": (
                "adaptation, adjustment",
                "Быстрая адаптация.",
                "A quick adaptation.",
            ),
            "эшелон": (
                "echelon, train",
                "Первый эшелон.",
                "The first echelon.",
            ),
            "жутко": (
                "terribly, awfully",
                "Жутко холодно.",
                "It's terribly cold.",
            ),
            "дипломатический": (
                "diplomatic, diplomatical",
                "Дипломатический ответ.",
                "A diplomatic answer.",
            ),
            "шкала": (
                "scale, scale (measurement)",
                "Посмотри на шкалу.",
                "Look at the scale.",
            ),
            "фонтан": (
                "fountain, jet",
                "Большой фонтан.",
                "A big fountain.",
            ),
            "заорать": (
                "to yell, to scream",
                "Он заорал.",
                "He yelled.",
            ),
            "соединять": (
                "to connect, to join",
                "Соедини это.",
                "Connect this.",
            ),
            "страстный": (
                "passionate, ardent",
                "Он страстный.",
                "He is passionate.",
            ),
            "урод": (
                "monster, freak",
                "Какой урод.",
                "What a monster.",
            ),
            "включаться": (
                "to turn on, to engage",
                "Свет включается.",
                "The light turns on.",
            ),
        },
    )
)
