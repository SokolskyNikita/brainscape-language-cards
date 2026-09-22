import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from russian_english._chunk_io import rewrite_chunk

print(
    rewrite_chunk(
        Path("russian_english/_chunks/deck_15260192_03.csv"),
        {
            "польский": (
                "Polish",
                "Это польский фильм?",
                "Is this a Polish movie?",
            ),
            "конкурент": (
                "competitor, rival",
                "Это наш конкурент.",
                "That's our competitor.",
            ),
            "существенно": (
                "significantly, substantially",
                "Это существенно.",
                "This matters significantly.",
            ),
            "маска": ("mask", "Надень маску.", "Put a mask on."),
            "жалоба": (
                "complaint",
                "Куда жалобу писать?",
                "Where do I file a complaint?",
            ),
            "потребление": (
                "consumption",
                "Потребление выросло.",
                "Consumption is up.",
            ),
            "опираться": (
                "to lean on, to rely on",
                "Не опирайся на дверь.",
                "Don't lean on the door.",
            ),
            "подпись": (
                "signature",
                "Нужна твоя подпись.",
                "I need your signature.",
            ),
            "прозрачный": (
                "transparent, clear",
                "Вода прозрачная.",
                "The water's clear.",
            ),
            "авиация": ("aviation", "Он в авиации.", "He's in aviation."),
            "корова": ("cow", "Смотри, корова!", "Look, a cow!"),
            "завести": (
                "to start, to get",
                "Заведи машину.",
                "Start the car.",
            ),
            "применяться": (
                "to be used, to be applied",
                "Это ещё применяется?",
                "Is that still used?",
            ),
            "ложиться": (
                "to lie down, to go to bed",
                "Я ложусь спать.",
                "I'm going to bed.",
            ),
            "настаивать": ("to insist", "Я настаиваю.", "I insist."),
            "изучить": (
                "to study, to examine",
                "Изучи это.",
                "Study this.",
            ),
            "напиток": (
                "drink",
                "Какой напиток?",
                "What drink do you want?",
            ),
            "избрать": ("to elect", "Его избрали.", "He got elected."),
            "освобождение": (
                "release, liberation",
                "До освобождения ещё год.",
                "A year until release.",
            ),
            "двойной": ("double", "Мне двойной.", "I'll take a double."),
            "письменный": (
                "written",
                "Нужен письменный ответ.",
                "I need a written answer.",
            ),
            "приготовить": (
                "to cook, to prepare",
                "Я приготовлю ужин.",
                "I'll cook dinner.",
            ),
            "сойти": (
                "to get off, to come off",
                "Сойди на следующей.",
                "Get off at the next one.",
            ),
            "инвестиционный": (
                "investment (adj.)",
                "Инвестиционный фонд?",
                "An investment fund?",
            ),
            "граф": ("count", "Он граф.", "He's a count."),
            "зачастую": (
                "often, frequently",
                "Зачастую так и бывает.",
                "That's often how it goes.",
            ),
            "густой": (
                "thick, dense",
                "Лес густой.",
                "The forest is dense.",
            ),
            "потребоваться": (
                "to be needed, to be required",
                "Потребуется время.",
                "Time will be needed.",
            ),
            "римский": (
                "Roman",
                "Это римский храм.",
                "That's a Roman temple.",
            ),
            "сложить": (
                "to fold, to put together",
                "Сложи это.",
                "Fold this.",
            ),
            "студия": (
                "studio",
                "Он работает в студии.",
                "He works in a studio.",
            ),
            "приход": (
                "arrival",
                "Жду твоего прихода.",
                "I'm waiting for your arrival.",
            ),
            "кремль": (
                "Kremlin",
                "Идём в Кремль?",
                "Shall we go to the Kremlin?",
            ),
            "авторитет": (
                "authority",
                "У него авторитет.",
                "He's got authority.",
            ),
            "отражение": (
                "reflection",
                "Смотри, отражение.",
                "Look, the reflection.",
            ),
            "накануне": (
                "the day before, on the eve",
                "Накануне праздника.",
                "The day before the holiday.",
            ),
            "мотор": (
                "engine, motor",
                "Мотор не завести.",
                "Can't start the engine.",
            ),
            "измерение": (
                "measurement",
                "Проверь измерение.",
                "Check the measurement.",
            ),
            "небесный": (
                "heavenly, sky-blue",
                "Небесный цвет.",
                "A sky-blue color.",
            ),
            "подлинный": (
                "genuine, authentic",
                "Это подлинное?",
                "Is this genuine?",
            ),
            "заметно": (
                "noticeably",
                "Это заметно.",
                "That's noticeably so.",
            ),
            "отдельно": (
                "separately",
                "Плати отдельно.",
                "Pay separately.",
            ),
            "исполнить": (
                "to fulfill, to perform",
                "Исполни план.",
                "Fulfill the plan.",
            ),
            "восстановить": (
                "to restore, to recover",
                "Восстанови файл.",
                "Restore the file.",
            ),
            "предварительный": (
                "preliminary",
                "Это предварительный план.",
                "That's a preliminary plan.",
            ),
            "искренне": (
                "sincerely, genuinely",
                "Я искренне рад.",
                "I'm genuinely glad.",
            ),
            "заботиться": (
                "to take care of",
                "Заботься о семье.",
                "Take care of the family.",
            ),
            "избавиться": (
                "to get rid of",
                "Надо избавиться от этого.",
                "We need to get rid of this.",
            ),
            "скрыть": (
                "to hide, to conceal",
                "Скрой это.",
                "Hide that.",
            ),
            "экологический": (
                "environmental, ecological",
                "Это экологический проект.",
                "It's an environmental project.",
            ),
            "молиться": ("to pray", "Она молится.", "She's praying."),
            "повесть": (
                "novella, tale",
                "Читал его повесть?",
                "Have you read his novella?",
            ),
            "вождь": (
                "chief, leader",
                "Кто у них вождь?",
                "Who's their chief?",
            ),
            "компонент": (
                "component",
                "Не хватает компонента.",
                "A component is missing.",
            ),
            "нарушить": (
                "to break, to violate",
                "Ты нарушил правило.",
                "You broke the rule.",
            ),
            "гордость": (
                "pride",
                "Это моя гордость.",
                "That's my pride and joy.",
            ),
            "невеста": (
                "bride, fiancée",
                "Где невеста?",
                "Where's the bride?",
            ),
            "передний": (
                "front",
                "Передняя дверь открыта.",
                "The front door's open.",
            ),
            "отвести": (
                "to take, to lead aside",
                "Отведи его домой.",
                "Take him home.",
            ),
            "вклад": (
                "contribution, deposit",
                "Это твой вклад.",
                "That's your contribution.",
            ),
            "доказывать": (
                "to prove",
                "Тебе не надо доказывать.",
                "You don't have to prove it.",
            ),
            "отнести": (
                "to take, to drop off",
                "Отнеси это туда.",
                "Take this over there.",
            ),
            "соображение": (
                "consideration, reason",
                "По соображениям безопасности.",
                "For security reasons.",
            ),
            "наблюдаться": (
                "to be observed, to occur",
                "Это часто наблюдается.",
                "That's often observed.",
            ),
            "глухой": (
                "deaf",
                "Он глухой на одно ухо.",
                "He's deaf in one ear.",
            ),
            "металл": ("metal", "Это металл?", "Is this metal?"),
            "неправильный": (
                "wrong, incorrect",
                "Неправильный номер.",
                "Wrong number.",
            ),
            "совещание": (
                "meeting",
                "Опять совещание.",
                "Another meeting.",
            ),
            "краткий": (
                "brief, short",
                "Мне нужен краткий ответ.",
                "I need a short answer.",
            ),
            "подходящий": (
                "suitable, right",
                "Это не подходящий момент.",
                "This isn't the right moment.",
            ),
            "сопровождать": (
                "to accompany",
                "Кто тебя сопровождает?",
                "Who's accompanying you?",
            ),
            "теоретический": (
                "theoretical",
                "Это теоретический вопрос.",
                "That's a theoretical question.",
            ),
            "пребывание": (
                "stay",
                "Долгое пребывание.",
                "A long stay.",
            ),
            "ложь": ("lie", "Это ложь.", "That's a lie."),
            "катастрофа": (
                "disaster, catastrophe",
                "Это катастрофа.",
                "This is a disaster.",
            ),
            "окружение": (
                "surroundings, circle",
                "Хорошее окружение.",
                "A good circle of people.",
            ),
            "процессор": (
                "processor",
                "Процессор слабый.",
                "The processor's weak.",
            ),
            "справедливый": (
                "fair, just",
                "Жизнь не всегда справедлива.",
                "Life is not always fair.",
            ),
            "профиль": (
                "profile",
                "Открой профиль.",
                "Open the profile.",
            ),
            "образоваться": (
                "to form",
                "Образовалась очередь.",
                "A line formed.",
            ),
            "квартал": (
                "block, quarter",
                "Через квартал.",
                "A block away.",
            ),
            "законодательный": (
                "legislative",
                "Законодательная власть.",
                "The legislative branch.",
            ),
            "эксплуатация": (
                "exploitation, operation",
                "Это чистая эксплуатация.",
                "That's pure exploitation.",
            ),
            "домик": (
                "little house, cottage",
                "Там домик.",
                "There's a little house there.",
            ),
            "окончательный": (
                "final, definitive",
                "Это моё окончательное решение.",
                "This is my final decision.",
            ),
            "пожар": ("fire", "Там пожар!", "There's a fire!"),
            "головной": (
                "head (adj.)",
                "Головной офис.",
                "The head office.",
            ),
            "металлический": (
                "metal, metallic",
                "Металлическая дверь.",
                "A metal door.",
            ),
            "чудесный": (
                "wonderful",
                "Чудесный день.",
                "A wonderful day.",
            ),
            "слуга": ("servant", "Позови слугу.", "Call the servant."),
            "осуществить": (
                "to carry out, to implement",
                "Это трудно осуществить.",
                "That's hard to carry out.",
            ),
            "удачный": (
                "successful, lucky",
                "Удачная покупка.",
                "A lucky buy.",
            ),
            "решительно": (
                "resolutely, firmly",
                "Он решительно отказался.",
                "He resolutely refused.",
            ),
            "переводить": (
                "to translate, to transfer",
                "Ты переводишь?",
                "Are you translating?",
            ),
            "критический": (
                "critical",
                "Критический момент.",
                "A critical moment.",
            ),
            "деятель": (
                "public figure",
                "Он известный деятель.",
                "He's a well-known public figure.",
            ),
            "нажать": ("to press", "Нажми сюда.", "Press here."),
            "посоветовать": (
                "to advise, to recommend",
                "Посоветуй, что делать.",
                "Advise me what to do.",
            ),
            "руль": (
                "steering wheel",
                "Держи руль.",
                "Hold the steering wheel.",
            ),
            "потратить": (
                "to spend",
                "Я всё потратил.",
                "I spent it all.",
            ),
        },
    )
)
