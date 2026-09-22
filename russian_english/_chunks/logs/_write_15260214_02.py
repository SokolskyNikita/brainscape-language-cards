import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from russian_english._chunk_io import rewrite_chunk

print(
    rewrite_chunk(
        Path("russian_english/_chunks/deck_15260214_02.csv"),
        {
            "любопытно": (
                "curiously, interestingly",
                "Любопытно, что он молчит.",
                "Curiously, he is silent.",
            ),
            "залп": (
                "volley, salvo",
                "Это был залп.",
                "That was a volley.",
            ),
            "приблизить": (
                "bring closer, move nearer",
                "Приблизь книгу.",
                "Bring the book closer.",
            ),
            "фара": (
                "headlight, lamp",
                "Фара снова сломана.",
                "The headlight is broken again.",
            ),
            "сравнительный": (
                "comparative, relative",
                "Это сравнительный метод.",
                "This is a comparative method.",
            ),
            "генератор": (
                "generator, alternator",
                "Генератор снова работает.",
                "The generator works again.",
            ),
            "манипуляция": (
                "manipulation",
                "Это чистая манипуляция.",
                "This is pure manipulation.",
            ),
            "лавочка": (
                "bench, small shop",
                "Сядь на лавочку.",
                "Sit on the bench.",
            ),
            "грузин": (
                "Georgian",
                "Мой друг — грузин.",
                "My friend is a Georgian.",
            ),
            "немногие": (
                "few, not many",
                "Немногие это знают.",
                "Few know this.",
            ),
            "исчерпать": (
                "exhaust, deplete",
                "Мы исчерпали время.",
                "We exhausted the time.",
            ),
            "дружок": (
                "buddy, pal",
                "Подожди меня, дружок.",
                "Wait for me, buddy.",
            ),
            "швейцарский": (
                "Swiss",
                "Это швейцарский сыр.",
                "This is Swiss cheese.",
            ),
            "пересмотреть": (
                "review, reconsider",
                "Пересмотри этот план.",
                "Review this plan.",
            ),
            "сало": (
                "lard, pork fat",
                "Я не ем сало.",
                "I do not eat lard.",
            ),
            "ядовитый": (
                "poisonous, toxic",
                "Этот гриб ядовитый.",
                "This mushroom is poisonous.",
            ),
            "татарский": (
                "Tatar, Tartar",
                "Это татарский язык.",
                "This is the Tatar language.",
            ),
            "литовский": (
                "Lithuanian",
                "Это литовский язык.",
                "This is Lithuanian.",
            ),
            "десант": (
                "landing, airborne",
                "Десант уже здесь.",
                "The landing is already here.",
            ),
            "казанский": (
                "Kazan, Kazansky",
                "Это казанский поезд.",
                "This is the Kazan train.",
            ),
            "засада": (
                "ambush, trap",
                "Это была засада.",
                "This was an ambush.",
            ),
            "повышаться": (
                "to increase, to rise",
                "Цены снова повышаются.",
                "Prices increase again.",
            ),
            "изгнать": (
                "expel, banish",
                "Его изгнали из дома.",
                "They expelled him from the house.",
            ),
            "отвлечься": (
                "get distracted, take a break",
                "Я отвлёкся от дела.",
                "I was distracted from the matter.",
            ),
            "координация": (
                "coordination",
                "Нам нужна координация.",
                "We need coordination.",
            ),
            "детальный": (
                "detailed, thorough",
                "Дай детальный план.",
                "Give a detailed plan.",
            ),
            "поползти": (
                "crawl, creep",
                "Он пополз туда.",
                "He crawled there.",
            ),
            "мерка": (
                "measure, size",
                "Сними мерку.",
                "Take a measure.",
            ),
            "чувственный": (
                "sensual",
                "Её голос был чувственным.",
                "Her voice was sensual.",
            ),
            "содействовать": (
                "assist, facilitate",
                "Мы содействуем им.",
                "We assist them.",
            ),
            "уезд": (
                "district, county",
                "Он жил в уезде.",
                "He lived in the district.",
            ),
            "обход": (
                "bypass, detour",
                "Иди в обход.",
                "Go on the bypass.",
            ),
            "вертеться": (
                "to spin, to revolve",
                "Не вертись на стуле.",
                "Do not spin on the chair.",
            ),
            "потреблять": (
                "consume, use",
                "Мы потребляем много воды.",
                "We consume a lot of water.",
            ),
            "вращение": (
                "rotation, spinning",
                "Это медленное вращение.",
                "This is a slow rotation.",
            ),
            "преграда": (
                "obstacle, barrier",
                "Перед нами стоит преграда.",
                "An obstacle stands before us.",
            ),
            "разъяснение": (
                "explanation, clarification",
                "Мне нужно разъяснение.",
                "I need an explanation.",
            ),
            "резервный": (
                "reserve, backup",
                "Это резервный выход.",
                "This is a reserve exit.",
            ),
            "могущественный": (
                "powerful, mighty",
                "Он могущественный враг.",
                "He is a powerful enemy.",
            ),
            "винить": (
                "blame, accuse",
                "Не вини меня.",
                "Do not blame me.",
            ),
            "казачий": (
                "Cossack, Cossack's",
                "Это казачья песня.",
                "This is a Cossack song.",
            ),
            "преемник": (
                "successor, heir",
                "Он мой преемник.",
                "He is my successor.",
            ),
            "эльф": (
                "elf",
                "Эльф жил в лесу.",
                "The elf lived in the forest.",
            ),
            "римлянин": (
                "Roman",
                "Римлянин шёл домой.",
                "The Roman went home.",
            ),
            "поднос": (
                "tray, platter",
                "Поставь поднос на стол.",
                "Put the tray on the table.",
            ),
            "основательно": (
                "thoroughly, in-depth",
                "Он основательно всё проверил.",
                "He thoroughly checked everything.",
            ),
            "бум": (
                "boom, craze",
                "Начался большой бум.",
                "A big boom began.",
            ),
            "развестись": (
                "to divorce, to get divorced",
                "Они хотят развестись.",
                "They want to divorce.",
            ),
            "осмелиться": (
                "dare, venture",
                "Я не осмелюсь спросить.",
                "I will not dare to ask.",
            ),
            "заведовать": (
                "to manage, to be in charge of",
                "Она заведует этим домом.",
                "She manages this house.",
            ),
            "прекращаться": (
                "to cease, to stop",
                "Дождь начал прекращаться.",
                "The rain began to cease.",
            ),
            "автомашина": (
                "car, automobile",
                "Автомашина стоит у дома.",
                "The car stands by the house.",
            ),
            "нацелить": (
                "aim, target",
                "Нацель удар на него.",
                "Aim the blow at him.",
            ),
            "совать": (
                "to poke, to thrust",
                "Не надо совать нос.",
                "Do not poke your nose.",
            ),
            "стан": (
                "camp, station",
                "Их стан был у реки.",
                "Their camp was by the river.",
            ),
            "соседство": (
                "neighborhood, vicinity",
                "Это тихое соседство.",
                "This is a quiet neighborhood.",
            ),
            "влага": (
                "moisture, humidity",
                "Земле нужна влага.",
                "The ground needs moisture.",
            ),
            "устало": (
                "tiredly, wearily",
                "Он устало сел.",
                "He sat down tiredly.",
            ),
            "ми": (
                "mi",
                "Спой ноту ми.",
                "Sing the note mi.",
            ),
            "неудобство": (
                "inconvenience, discomfort",
                "Прости за неудобство.",
                "Sorry for the inconvenience.",
            ),
            "решимость": (
                "determination, resolve",
                "Её решимость сильна.",
                "Her determination is strong.",
            ),
            "воротник": (
                "collar, neckband",
                "Подними воротник.",
                "Raise the collar.",
            ),
            "сближение": (
                "rapprochement, convergence",
                "Их сближение уже началось.",
                "Their rapprochement already began.",
            ),
            "безработный": (
                "unemployed, jobless",
                "Он давно безработный.",
                "He has been unemployed long.",
            ),
            "описываться": (
                "to be described, to be depicted",
                "Это описывается в книге.",
                "This is described in the book.",
            ),
            "храбрый": (
                "brave, courageous",
                "Будь храбрым.",
                "Be brave.",
            ),
            "троица": (
                "Trinity, triad",
                "Я верю в Троицу.",
                "I believe in the Trinity.",
            ),
            "ринуться": (
                "rush, dash",
                "Они ринулись туда.",
                "They rushed there.",
            ),
            "предсказание": (
                "prediction, prophecy",
                "Это странное предсказание.",
                "This is a strange prediction.",
            ),
            "ассоциироваться": (
                "to associate, to be associated",
                "Это ассоциируется с летом.",
                "This associates with summer.",
            ),
            "воробей": (
                "sparrow",
                "Воробей сидит на окне.",
                "A sparrow sits on the window.",
            ),
            "оперативно": (
                "promptly, quickly",
                "Он оперативно всё сделал.",
                "He promptly did everything.",
            ),
            "вилла": (
                "villa, country house",
                "Это большая вилла.",
                "This is a big villa.",
            ),
            "фиолетовый": (
                "purple, violet",
                "Это фиолетовое платье.",
                "This is a purple dress.",
            ),
            "вскрикнуть": (
                "to cry out, to exclaim",
                "Она вскрикнула.",
                "She cried out.",
            ),
            "садик": (
                "kindergarten, nursery",
                "Малыш идёт в садик.",
                "The child goes to kindergarten.",
            ),
            "шаблон": (
                "template, stencil",
                "Возьми этот шаблон.",
                "Take this template.",
            ),
            "упереться": (
                "to lean, to insist",
                "Он упёрся в дверь.",
                "He leaned against the door.",
            ),
            "сбивать": (
                "knock down, throw off",
                "Не сбивай стул.",
                "Do not knock down the chair.",
            ),
            "банкротство": (
                "bankruptcy, insolvency",
                "Это полное банкротство.",
                "This is complete bankruptcy.",
            ),
            "оперировать": (
                "operate, to perform surgery",
                "Врач будет оперировать.",
                "The doctor will operate.",
            ),
            "умело": (
                "skillfully, adeptly",
                "Она умело всё делает.",
                "She skillfully does everything.",
            ),
            "сосать": (
                "suck",
                "Не надо сосать палец.",
                "Do not suck your finger.",
            ),
            "наглядный": (
                "visual, illustrative",
                "Это наглядный пример.",
                "This is a visual example.",
            ),
            "сравнимый": (
                "comparable, commensurate",
                "Эти цены сравнимы.",
                "These prices are comparable.",
            ),
            "всевышний": (
                "the Almighty, the Most High",
                "Всевышний нас слышит.",
                "The Almighty hears us.",
            ),
            "альянс": (
                "alliance, coalition",
                "Это крепкий альянс.",
                "This is a strong alliance.",
            ),
            "сбоку": (
                "side, from the side",
                "Смотри сбоку.",
                "Look from the side.",
            ),
            "безобразие": (
                "outrage, monstrosity",
                "Какое безобразие!",
                "What an outrage!",
            ),
            "партизанский": (
                "partisan, guerrilla",
                "Это партизанская война.",
                "This is a partisan war.",
            ),
            "грунт": (
                "soil, ground",
                "Грунт здесь сухой.",
                "The soil is dry here.",
            ),
            "пристальный": (
                "intense, piercing",
                "Его взгляд был пристальным.",
                "His look was intense.",
            ),
            "вкусно": (
                "tasty, delicious",
                "Тут очень вкусно.",
                "It is very tasty here.",
            ),
            "жизненно": (
                "vital, life-related",
                "Это жизненно важно.",
                "This is vitally important.",
            ),
            "иллюстрировать": (
                "illustrate",
                "Он будет иллюстрировать книгу.",
                "He will illustrate the book.",
            ),
            "вырастить": (
                "to grow, to raise",
                "Я выращу цветы.",
                "I will grow flowers.",
            ),
            "добавка": (
                "additive, supplement",
                "Это вредная добавка.",
                "This is a harmful additive.",
            ),
            "светло": (
                "light, bright",
                "Тут очень светло.",
                "It is very light here.",
            ),
            "почтенный": (
                "honorable, respected",
                "Он почтенный гость.",
                "He is an honorable guest.",
            ),
            "смертельно": (
                "deadly, fatally",
                "Это смертельно опасно.",
                "This is fatally dangerous.",
            ),
        },
    )
)
