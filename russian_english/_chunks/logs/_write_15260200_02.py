import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from russian_english._chunk_io import rewrite_chunk

print(
    rewrite_chunk(
        Path("russian_english/_chunks/deck_15260200_02.csv"),
        {
            "бык": (
                "bull, ox",
                "Бык стоит в поле.",
                "The bull stands in the field.",
            ),
            "заработок": (
                "earnings, income",
                "Его заработок хороший.",
                "His earnings are good.",
            ),
            "симпатия": (
                "attraction, liking",
                "У меня к ней симпатия.",
                "I have an attraction to her.",
            ),
            "примитивный": (
                "primitive, rudimentary",
                "Это примитивный план.",
                "This is a primitive plan.",
            ),
            "прорыв": (
                "breakthrough",
                "Это большой прорыв.",
                "This is a big breakthrough.",
            ),
            "коэффициент": (
                "coefficient, factor",
                "Коэффициент высокий.",
                "The coefficient is high.",
            ),
            "материнский": (
                "maternal, motherly",
                "Это материнская любовь.",
                "This is maternal love.",
            ),
            "напрасно": (
                "in vain, needlessly",
                "Он ждал напрасно.",
                "He waited in vain.",
            ),
            "мишка": (
                "bear, teddy bear",
                "Дай мне мишку.",
                "Give me the teddy bear.",
            ),
            "угадать": (
                "guess, predict",
                "Угадай ответ.",
                "Guess the answer.",
            ),
            "индивид": (
                "individual, person",
                "Каждый индивид важен.",
                "Every individual is important.",
            ),
            "поблагодарить": (
                "to thank, to express gratitude",
                "Я хочу поблагодарить тебя.",
                "I want to thank you.",
            ),
            "восстание": (
                "uprising, rebellion",
                "Восстание началось.",
                "The uprising started.",
            ),
            "республиканский": (
                "Republican",
                "Это республиканский план.",
                "This is a Republican plan.",
            ),
            "влажный": (
                "moist, damp",
                "Воздух влажный.",
                "The air is moist.",
            ),
            "опускаться": (
                "to descend, to go down",
                "Солнце опускается.",
                "The sun descends.",
            ),
            "отвратительный": (
                "disgusting, repulsive",
                "Запах отвратительный.",
                "The smell is disgusting.",
            ),
            "вылет": (
                "departure, takeoff",
                "Вылет завтра.",
                "The departure is tomorrow.",
            ),
            "пик": (
                "peak",
                "Мы на пике горы.",
                "We are at the mountain peak.",
            ),
            "пригодиться": (
                "to come in handy, to be useful",
                "Это пригодится.",
                "This will come in handy.",
            ),
            "похоронить": (
                "to bury, to inter",
                "Мы похоронили его.",
                "We buried him.",
            ),
            "верность": (
                "loyalty, fidelity",
                "Его верность сильная.",
                "His loyalty is strong.",
            ),
            "нормативный": (
                "regulatory, normative",
                "Это нормативный документ.",
                "This is a regulatory document.",
            ),
            "дверца": (
                "door, small door",
                "Открой дверцу.",
                "Open the small door.",
            ),
            "удобство": (
                "convenience, comfort",
                "Это большое удобство.",
                "This is a big convenience.",
            ),
            "импульс": (
                "impulse, pulse",
                "Это сильный импульс.",
                "This is a strong impulse.",
            ),
            "однозначно": (
                "definitely, unequivocally",
                "Это однозначно хорошо.",
                "This is definitely good.",
            ),
            "слышаться": (
                "to be heard, to sound",
                "Слышатся голоса.",
                "Voices are heard.",
            ),
            "сознательно": (
                "consciously, deliberately",
                "Она сознательно выбрала это.",
                "She consciously chose this.",
            ),
            "кивать": (
                "nod, bob",
                "Она кивает головой.",
                "She nods her head.",
            ),
            "приготовление": (
                "preparation, cooking",
                "Приготовление ужина долгое.",
                "Dinner preparation is long.",
            ),
            "невинный": (
                "innocent, guiltless",
                "Он невинный.",
                "He is innocent.",
            ),
            "повторение": (
                "repetition, iteration",
                "Повторение нужно.",
                "Repetition is needed.",
            ),
            "наследие": (
                "heritage, legacy",
                "Это наше наследие.",
                "This is our heritage.",
            ),
            "поляк": (
                "Pole, Polish person",
                "Поляк живёт здесь.",
                "The Pole lives here.",
            ),
            "сгореть": (
                "burn down, burn out",
                "Дом сгорел.",
                "The house burned down.",
            ),
            "ограничиваться": (
                "to be limited, to be restricted",
                "Он ограничивался этим.",
                "He was limited to this.",
            ),
            "пирамида": (
                "pyramid",
                "Пирамида высокая.",
                "The pyramid is tall.",
            ),
            "сволочь": (
                "scoundrel, bastard",
                "Он сволочь.",
                "He is a scoundrel.",
            ),
            "различать": (
                "to distinguish, to differentiate",
                "Я различаю цвета.",
                "I distinguish colors.",
            ),
            "татарин": (
                "Tatar, Tartar",
                "Татарин живёт здесь.",
                "The Tatar lives here.",
            ),
            "потихоньку": (
                "quietly, gradually",
                "Она потихоньку закрыла дверь.",
                "She quietly closed the door.",
            ),
            "ночевать": (
                "to spend the night, to stay overnight",
                "Я буду ночевать там.",
                "I will spend the night there.",
            ),
            "ставиться": (
                "to be placed, to be set",
                "Стол ставится здесь.",
                "The table is placed here.",
            ),
            "откровенный": (
                "frank, candid",
                "Он откровенный.",
                "He is frank.",
            ),
            "качать": (
                "swing, pump",
                "Он качает воду.",
                "He pumps water.",
            ),
            "тираж": (
                "circulation, print run",
                "Тираж книги большой.",
                "The book's circulation is big.",
            ),
            "убитый": (
                "killed, dead",
                "Он был убит.",
                "He was killed.",
            ),
            "череп": (
                "skull, cranium",
                "Это его череп.",
                "This is his skull.",
            ),
            "чайник": (
                "kettle, teapot",
                "Чайник на столе.",
                "The kettle is on the table.",
            ),
            "устанавливаться": (
                "to be installed, to settle",
                "Система устанавливается.",
                "The system is being installed.",
            ),
            "нетерпение": (
                "impatience, eagerness",
                "Я вижу её нетерпение.",
                "I see her impatience.",
            ),
            "убыток": (
                "loss, deficit",
                "Это большой убыток.",
                "This is a big loss.",
            ),
            "экономия": (
                "economy, saving",
                "Это хорошая экономия.",
                "This is a good saving.",
            ),
            "уложить": (
                "lay, put to bed",
                "Уложи малыша.",
                "Put the baby to bed.",
            ),
            "завидовать": (
                "to envy, to be jealous of",
                "Не завидуй ему.",
                "Don't envy him.",
            ),
            "обнимать": (
                "to hug, to embrace",
                "Я хочу обнимать тебя.",
                "I want to hug you.",
            ),
            "энтузиазм": (
                "enthusiasm, zeal",
                "Её энтузиазм сильный.",
                "Her enthusiasm is strong.",
            ),
            "допрос": (
                "interrogation, questioning",
                "Допрос был долгий.",
                "The interrogation was long.",
            ),
            "породить": (
                "to generate, to give birth",
                "Это породило страх.",
                "This generated fear.",
            ),
            "отклонение": (
                "deviation, deflection",
                "Это большое отклонение.",
                "This is a big deviation.",
            ),
            "урожай": (
                "harvest, crop",
                "Урожай хороший.",
                "The harvest is good.",
            ),
            "архитектор": (
                "architect, designer",
                "Архитектор здесь.",
                "The architect is here.",
            ),
            "авиационный": (
                "aviation, aeronautical",
                "Это авиационный завод.",
                "This is an aviation plant.",
            ),
            "отличать": (
                "distinguish, differentiate",
                "Я отличаю их.",
                "I distinguish them.",
            ),
            "епископ": (
                "bishop, prelate",
                "Епископ здесь.",
                "The bishop is here.",
            ),
            "освещать": (
                "illuminate, light up",
                "Солнце освещает дом.",
                "The sun illuminates the house.",
            ),
            "невысокий": (
                "short, not tall",
                "Он невысокий.",
                "He is short.",
            ),
            "выложить": (
                "lay out, post",
                "Она выложила карты.",
                "She laid out the cards.",
            ),
            "творец": (
                "creator, maker",
                "Творец создал мир.",
                "The creator made the world.",
            ),
            "турок": (
                "Turk, Turkish person",
                "Турок живёт здесь.",
                "The Turk lives here.",
            ),
            "спрятаться": (
                "to hide, to conceal",
                "Она спряталась за дверью.",
                "She hid behind the door.",
            ),
            "висок": (
                "temple",
                "У него болит висок.",
                "His temple hurts.",
            ),
            "подъехать": (
                "to drive up, to come up",
                "Я подъеду к дому.",
                "I'll drive up to the house.",
            ),
            "поручение": (
                "assignment, commission",
                "У меня есть поручение.",
                "I have an assignment.",
            ),
            "удовлетворять": (
                "satisfy, fulfill",
                "Это удовлетворяет меня.",
                "This satisfies me.",
            ),
            "пузырь": (
                "bubble, blister",
                "Пузырь на воде.",
                "The bubble is on the water.",
            ),
            "неожиданность": (
                "surprise, unexpectedness",
                "Подарок был неожиданностью.",
                "The gift was a surprise.",
            ),
            "недостаточный": (
                "insufficient, inadequate",
                "Свет недостаточный.",
                "The light is insufficient.",
            ),
            "ласковый": (
                "affectionate, tender",
                "У неё ласковый голос.",
                "She has an affectionate voice.",
            ),
            "приемлемый": (
                "acceptable, admissible",
                "Цена приемлемая.",
                "The price is acceptable.",
            ),
            "дружить": (
                "to be friends, to make friends",
                "Мы давно дружим.",
                "We are friends.",
            ),
            "смертельный": (
                "deadly, lethal",
                "Это смертельный удар.",
                "This is a deadly blow.",
            ),
            "чрезвычайный": (
                "extraordinary, emergency",
                "Это чрезвычайный случай.",
                "This is an emergency case.",
            ),
            "жилищный": (
                "housing, residential",
                "Это жилищный вопрос.",
                "This is a housing question.",
            ),
            "дерьмо": (
                "shit, crap",
                "Это дерьмо.",
                "This is shit.",
            ),
            "выработать": (
                "develop, produce",
                "Мы выработали план.",
                "We developed a plan.",
            ),
            "усталый": (
                "tired, weary",
                "Я усталый.",
                "I am tired.",
            ),
            "уволить": (
                "dismiss, fire",
                "Его уволили.",
                "They fired him.",
            ),
            "жилище": (
                "dwelling, habitation",
                "Это старое жилище.",
                "This is an old dwelling.",
            ),
            "кисть": (
                "brush, bunch",
                "Возьми кисть.",
                "Take the brush.",
            ),
            "огород": (
                "vegetable garden, kitchen garden",
                "Я в огороде.",
                "I am in the vegetable garden.",
            ),
            "секция": (
                "section, unit",
                "Это моя секция.",
                "This is my section.",
            ),
            "защитный": (
                "protective, defensive",
                "Это защитный слой.",
                "This is a protective layer.",
            ),
            "освоить": (
                "master, assimilate",
                "Она освоила язык.",
                "She mastered the language.",
            ),
            "абонент": (
                "subscriber, customer",
                "Абонент ждёт.",
                "The subscriber waits.",
            ),
            "гвоздь": (
                "nail, spike",
                "Гвоздь в стене.",
                "The nail is in the wall.",
            ),
            "пенсионный": (
                "pension, retirement",
                "Это пенсионный возраст.",
                "This is retirement age.",
            ),
            "запуск": (
                "launch, startup",
                "Запуск завтра.",
                "The launch is tomorrow.",
            ),
            "очерк": (
                "essay, sketch",
                "Она написала очерк.",
                "She wrote an essay.",
            ),
        },
    )
)
