import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from russian_english._chunk_io import rewrite_chunk

print(
    rewrite_chunk(
        Path("russian_english/_chunks/deck_15260218_01.csv"),
        {
            "концертный": (
                "concert",
                "Это концертный зал.",
                "This is a concert hall.",
            ),
            "средневековье": (
                "Middle Ages",
                "Это было в средневековье.",
                "That was in the Middle Ages.",
            ),
            "беспокойный": (
                "restless",
                "Он сегодня беспокойный.",
                "He is restless today.",
            ),
            "единение": (
                "unity",
                "Нам нужно единение.",
                "We need unity.",
            ),
            "наркотический": (
                "narcotic",
                "Это наркотическое средство.",
                "This is a narcotic.",
            ),
            "интенсивно": (
                "intensively",
                "Мы работали интенсивно.",
                "We worked intensively.",
            ),
            "забыться": (
                "lose oneself",
                "Он забылся в работе.",
                "He lost himself in the work.",
            ),
            "подержать": (
                "hold",
                "Подержи сумку.",
                "Hold the bag.",
            ),
            "светофор": (
                "traffic light",
                "Светофор красный.",
                "The traffic light is red.",
            ),
            "путаница": (
                "confusion",
                "Тут полная путаница.",
                "There is complete confusion here.",
            ),
            "субсидия": (
                "subsidy",
                "Нам дали субсидию.",
                "They gave us a subsidy.",
            ),
            "материк": (
                "continent",
                "Это большой материк.",
                "This is a large continent.",
            ),
            "финансово": (
                "financially",
                "Она финансово независима.",
                "She is financially independent.",
            ),
            "журналистский": (
                "journalistic",
                "Это журналистский вопрос.",
                "This is a journalistic question.",
            ),
            "перечисленный": (
                "listed",
                "Имена уже перечислены.",
                "The names are already listed.",
            ),
            "припев": (
                "chorus",
                "Спой припев ещё раз.",
                "Sing the chorus again.",
            ),
            "прокатиться": (
                "go for a ride",
                "Давай прокатимся.",
                "Let's go for a ride.",
            ),
            "фотографировать": (
                "photograph",
                "Я люблю фотографировать.",
                "I love to photograph.",
            ),
            "отменять": (
                "cancel",
                "Не отменяй урок.",
                "Don't cancel the lesson.",
            ),
            "освобождаться": (
                "get free",
                "Я освобождаюсь вечером.",
                "I get free in the evening.",
            ),
            "калибр": (
                "caliber",
                "Какой калибр у пистолета?",
                "What caliber is the pistol?",
            ),
            "странник": (
                "wanderer",
                "Странник шёл по дороге.",
                "The wanderer walked along the road.",
            ),
            "архивный": (
                "archival",
                "Это архивный документ.",
                "This is an archival document.",
            ),
            "покуда": (
                "as long as",
                "Читай, покуда он спит.",
                "Read as long as he sleeps.",
            ),
            "пообедать": (
                "have lunch",
                "Давай пообедаем.",
                "Let's have lunch.",
            ),
            "щелчок": (
                "click",
                "Я слышал щелчок.",
                "I heard a click.",
            ),
            "тумбочка": (
                "nightstand",
                "Книга лежит на тумбочке.",
                "The book is on the nightstand.",
            ),
            "католик": (
                "Catholic",
                "Он католик.",
                "He is a Catholic.",
            ),
            "мифология": (
                "mythology",
                "Я читаю мифологию.",
                "I read mythology.",
            ),
            "погашение": (
                "repayment",
                "Это погашение долга.",
                "This is the repayment of the debt.",
            ),
            "гм": (
                "uh",
                "Гм, не знаю.",
                "Uh, I don't know.",
            ),
            "кара": (
                "punishment",
                "Его ждала кара.",
                "Punishment awaited him.",
            ),
            "смутить": (
                "embarrass",
                "Ты меня смутил.",
                "You embarrassed me.",
            ),
            "пролить": (
                "spill",
                "Я пролил чай.",
                "I spilled the tea.",
            ),
            "осада": (
                "siege",
                "Это долгая осада.",
                "This is a long siege.",
            ),
            "капризный": (
                "capricious",
                "Ребёнок сегодня капризный.",
                "The child is capricious today.",
            ),
            "тверской": (
                "Tver",
                "Это тверской поезд.",
                "This is a Tver train.",
            ),
            "сортир": (
                "toilet",
                "Где тут сортир?",
                "Where is the toilet here?",
            ),
            "обдумывать": (
                "ponder",
                "Я обдумываю ответ.",
                "I am pondering the answer.",
            ),
            "белоснежный": (
                "snow-white",
                "Платье белоснежное.",
                "The dress is snow-white.",
            ),
            "расплатиться": (
                "pay",
                "Я расплатился в кафе.",
                "I paid at the café.",
            ),
            "хлынуть": (
                "gush",
                "Вода хлынула из трубы.",
                "Water gushed from the pipe.",
            ),
            "заботливый": (
                "caring",
                "Она заботливая мама.",
                "She is a caring mother.",
            ),
            "усомниться": (
                "doubt",
                "Я усомнился в нём.",
                "I doubted him.",
            ),
            "трепет": (
                "reverence",
                "Я ждал с трепетом.",
                "I waited with reverence.",
            ),
            "познавательный": (
                "informative",
                "Это познавательный фильм.",
                "This is an informative movie.",
            ),
            "параллель": (
                "parallel",
                "Он провёл параллель.",
                "He drew a parallel.",
            ),
            "напор": (
                "pressure",
                "Напор воды слабый.",
                "The water pressure is weak.",
            ),
            "разворот": (
                "turnaround",
                "Сделай разворот.",
                "Make a turnaround.",
            ),
            "курский": (
                "Kursk",
                "Это курский поезд.",
                "This is a Kursk train.",
            ),
            "топить": (
                "heat",
                "Мы топим печь.",
                "We heat the stove.",
            ),
            "кишечник": (
                "intestine",
                "У меня болит кишечник.",
                "My intestine hurts.",
            ),
            "чип": (
                "chip",
                "В телефоне новый чип.",
                "There is a new chip in the phone.",
            ),
            "предметный": (
                "concrete",
                "Нужен предметный разговор.",
                "We need a concrete talk.",
            ),
            "смежный": (
                "adjacent",
                "Это смежная комната.",
                "This is an adjacent room.",
            ),
            "плитка": (
                "tile",
                "В ванной лежит плитка.",
                "There is tile in the bathroom.",
            ),
            "накрывать": (
                "set",
                "Я накрываю на стол.",
                "I set the table.",
            ),
            "рваный": (
                "torn",
                "Это рваная рубашка.",
                "This is a torn shirt.",
            ),
            "радиоактивный": (
                "radioactive",
                "Это радиоактивный мусор.",
                "This is radioactive waste.",
            ),
            "наступательный": (
                "offensive",
                "Это наступательный план.",
                "This is an offensive plan.",
            ),
            "квота": (
                "quota",
                "Мы выполнили квоту.",
                "We met the quota.",
            ),
            "оратор": (
                "orator",
                "Он хороший оратор.",
                "He is a good orator.",
            ),
            "нарезать": (
                "slice",
                "Я нарезал сыр.",
                "I sliced the cheese.",
            ),
            "окурок": (
                "cigarette butt",
                "Он бросил окурок.",
                "He threw the cigarette butt.",
            ),
            "горничная": (
                "maid",
                "Позови горничную.",
                "Call the maid.",
            ),
            "нагнуться": (
                "bend down",
                "Он нагнулся за ключом.",
                "He bent down for the key.",
            ),
            "крупно": (
                "big",
                "Он крупно выиграл.",
                "He won big.",
            ),
            "проделывать": (
                "perform",
                "Он проделывает этот фокус.",
                "He performs this trick.",
            ),
            "просматриваться": (
                "visible",
                "Дом просматривается из окна.",
                "The house is visible from the window.",
            ),
            "повсеместно": (
                "everywhere",
                "Снег лежит повсеместно.",
                "Snow lies everywhere.",
            ),
            "наделать": (
                "make a lot of",
                "Он наделал много шума.",
                "He made a lot of noise.",
            ),
            "рукоятка": (
                "handle",
                "Рукоятка сломалась.",
                "The handle broke.",
            ),
            "гей": (
                "gay",
                "Он открыто гей.",
                "He is openly gay.",
            ),
            "потенциально": (
                "potentially",
                "Это потенциально опасно.",
                "This is potentially dangerous.",
            ),
            "покоситься": (
                "look askance",
                "Он покосился на нас.",
                "He looked askance at us.",
            ),
            "верхом": (
                "on horseback",
                "Она едет верхом.",
                "She rides on horseback.",
            ),
            "бородатый": (
                "bearded",
                "Это бородатый мужчина.",
                "This is a bearded man.",
            ),
            "однородный": (
                "homogeneous",
                "Это однородная смесь.",
                "This is a homogeneous mixture.",
            ),
            "немаловажный": (
                "significant",
                "Это немаловажный факт.",
                "This is a significant fact.",
            ),
            "арбуз": (
                "watermelon",
                "Я ем арбуз.",
                "I eat watermelon.",
            ),
            "язва": (
                "ulcer",
                "У него язва.",
                "He has an ulcer.",
            ),
            "стражник": (
                "guard",
                "Стражник стоит у двери.",
                "The guard stands at the door.",
            ),
            "волевой": (
                "strong-willed",
                "Он волевой человек.",
                "He is a strong-willed person.",
            ),
            "типовой": (
                "standard",
                "Это типовой договор.",
                "This is a standard contract.",
            ),
            "буйный": (
                "boisterous",
                "Море сегодня буйное.",
                "The sea is boisterous today.",
            ),
            "гаснуть": (
                "go out",
                "Свет гаснет.",
                "The light is going out.",
            ),
            "довольствоваться": (
                "be satisfied",
                "Он довольствуется малым.",
                "He is satisfied with little.",
            ),
            "гармоничный": (
                "harmonious",
                "У них гармоничный брак.",
                "They have a harmonious marriage.",
            ),
            "вскричать": (
                "cry out",
                "Она вскричала от боли.",
                "She cried out in pain.",
            ),
            "воспаление": (
                "inflammation",
                "У меня воспаление горла.",
                "I have inflammation of the throat.",
            ),
            "жертвовать": (
                "donate",
                "Мы жертвуем на храм.",
                "We donate to the church.",
            ),
            "зенит": (
                "zenith",
                "Солнце в зените.",
                "The sun is at its zenith.",
            ),
            "закономерный": (
                "logical",
                "Это закономерный итог.",
                "This is a logical result.",
            ),
            "видеокамера": (
                "video camera",
                "У него есть видеокамера.",
                "He has a video camera.",
            ),
            "логически": (
                "logically",
                "Это логически верно.",
                "This is logically true.",
            ),
            "всплывать": (
                "surface",
                "Правда всплывает.",
                "The truth surfaces.",
            ),
            "крушение": (
                "crash",
                "Это крушение поезда.",
                "This is a train crash.",
            ),
            "юбилейный": (
                "anniversary",
                "Это юбилейный год.",
                "This is an anniversary year.",
            ),
            "прикасаться": (
                "touch",
                "Не прикасайся к печи.",
                "Don't touch the stove.",
            ),
            "богатырь": (
                "hero",
                "Это сильный богатырь.",
                "This is a strong hero.",
            ),
        },
    )
)
