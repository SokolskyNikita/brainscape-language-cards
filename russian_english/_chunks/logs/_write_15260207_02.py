import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from russian_english._chunk_io import rewrite_chunk

print(
    rewrite_chunk(
        Path("russian_english/_chunks/deck_15260207_02.csv"),
        {
            "основатель": (
                "founder",
                "Он основатель.",
                "He is the founder.",
            ),
            "лауреат": (
                "laureate, awardee",
                "Он лауреат.",
                "He is a laureate.",
            ),
            "толкнуть": (
                "push, shove",
                "Толкни дверь.",
                "Push the door.",
            ),
            "конкурентный": (
                "competitive, rival",
                "Рынок конкурентный.",
                "The market is competitive.",
            ),
            "ворваться": (
                "burst in, break in",
                "Он ворвался.",
                "He burst in.",
            ),
            "выявление": (
                "detection, identification",
                "Раннее выявление.",
                "Early detection.",
            ),
            "проработать": (
                "work out, elaborate",
                "Проработай план.",
                "Work out the plan.",
            ),
            "тормоз": (
                "brake, retarder",
                "Где тормоз?",
                "Where is the brake?",
            ),
            "преодолевать": (
                "overcome, surmount",
                "Она преодолевает страх.",
                "She overcomes fear.",
            ),
            "патриарх": (
                "patriarch, primate",
                "Старый патриарх.",
                "The old patriarch.",
            ),
            "мониторинг": (
                "monitoring, surveillance",
                "Нужен мониторинг.",
                "We need monitoring.",
            ),
            "энциклопедия": (
                "encyclopedia, encyclopaedia",
                "Открой энциклопедию.",
                "Open the encyclopedia.",
            ),
            "натянуть": (
                "stretch, tighten",
                "Натяни ткань.",
                "Stretch the cloth.",
            ),
            "сообщаться": (
                "communicate, correspond",
                "Мы сообщаемся.",
                "We communicate.",
            ),
            "увезти": (
                "to take away, to carry off",
                "Они увезли стол.",
                "They took away the table.",
            ),
            "знаток": (
                "expert, connoisseur",
                "Он знаток.",
                "He is an expert.",
            ),
            "хан": (
                "khan, ruler",
                "Великий хан.",
                "The great khan.",
            ),
            "будить": (
                "wake, awaken",
                "Не буди меня.",
                "Don't wake me.",
            ),
            "трибуна": (
                "rostrum, tribune",
                "Он на трибуне.",
                "He is on the rostrum.",
            ),
            "разрешаться": (
                "to be resolved, to be allowed",
                "Проблема разрешается.",
                "The problem is being resolved.",
            ),
            "приводиться": (
                "to be cited, to be brought",
                "Пример приводится.",
                "The example is cited.",
            ),
            "виднеться": (
                "to be visible, to appear",
                "Гора виднеется.",
                "The mountain is visible.",
            ),
            "предпринимательство": (
                "entrepreneurship, businessmanship",
                "Это предпринимательство.",
                "This is entrepreneurship.",
            ),
            "хохотать": (
                "to laugh, to chuckle",
                "Они хохочут.",
                "They laugh.",
            ),
            "застрять": (
                "get stuck, be stuck",
                "Я застрял.",
                "I got stuck.",
            ),
            "благотворительный": (
                "charitable, philanthropic",
                "Благотворительный вечер.",
                "A charitable evening.",
            ),
            "организовывать": (
                "organize, arrange",
                "Мы организовываем вечер.",
                "We organize an evening.",
            ),
            "принтер": (
                "printer",
                "Принтер не работает.",
                "The printer does not work.",
            ),
            "недоверие": (
                "distrust, mistrust",
                "Его недоверие.",
                "His distrust.",
            ),
            "прикосновение": (
                "touch, contact",
                "Мягкое прикосновение.",
                "A soft touch.",
            ),
            "конкурировать": (
                "compete, compete with",
                "Они конкурируют.",
                "They compete.",
            ),
            "кислота": (
                "acid",
                "Это кислота.",
                "This is acid.",
            ),
            "ухаживать": (
                "to take care of, to court",
                "Она ухаживает за ним.",
                "She takes care of him.",
            ),
            "сходный": (
                "similar, akin",
                "Сходный случай.",
                "A similar case.",
            ),
            "голубь": (
                "pigeon, dove",
                "Голубь сел.",
                "The pigeon sat.",
            ),
            "добывать": (
                "to extract, to obtain",
                "Они добывают нефть.",
                "They extract oil.",
            ),
            "проволока": (
                "wire, cable",
                "Тонкая проволока.",
                "A thin wire.",
            ),
            "морально": (
                "morally, ethically",
                "Это морально плохо.",
                "This is morally bad.",
            ),
            "обрабатывать": (
                "process, treat",
                "Обрабатывай письмо.",
                "Process the letter.",
            ),
            "скончаться": (
                "to die, to pass away",
                "Он скончался.",
                "He died.",
            ),
            "смущать": (
                "embarrass, confuse",
                "Не смущай её.",
                "Don't embarrass her.",
            ),
            "мороженое": (
                "ice cream, ice-cream",
                "Хочу мороженое.",
                "I want ice cream.",
            ),
            "белок": (
                "protein",
                "Мне нужен белок.",
                "I need protein.",
            ),
            "легендарный": (
                "legendary",
                "Он легендарный.",
                "He is legendary.",
            ),
            "усиливать": (
                "to strengthen, to intensify",
                "Это усиливает звук.",
                "This strengthens the sound.",
            ),
            "табак": (
                "tobacco",
                "Он курит табак.",
                "He smokes tobacco.",
            ),
            "соображать": (
                "to reason, to figure out",
                "Я не соображаю.",
                "I can't figure it out.",
            ),
            "низко": (
                "low, down",
                "Птица летит низко.",
                "The bird flies low.",
            ),
            "нанять": (
                "hire, employ",
                "Мы наняли его.",
                "We hired him.",
            ),
            "преобладать": (
                "prevail, dominate",
                "Правда преобладает.",
                "Truth prevails.",
            ),
            "обозначение": (
                "designation, notation",
                "Ясное обозначение.",
                "A clear designation.",
            ),
            "моделирование": (
                "modeling, simulation",
                "Это моделирование.",
                "This is modeling.",
            ),
            "неясный": (
                "unclear, vague",
                "Ответ неясный.",
                "The answer is unclear.",
            ),
            "завет": (
                "testament, behest",
                "Это завет.",
                "This is a testament.",
            ),
            "обнаружиться": (
                "to be found, to turn up",
                "Ключи обнаружились.",
                "The keys were found.",
            ),
            "поставлять": (
                "supply, deliver",
                "Мы поставляем воду.",
                "We supply water.",
            ),
            "усиливаться": (
                "to intensify, to strengthen",
                "Ветер усиливается.",
                "The wind is intensifying.",
            ),
            "предотвратить": (
                "prevent, avert",
                "Это предотвратит беду.",
                "This will prevent trouble.",
            ),
            "пожаловать": (
                "welcome, to welcome",
                "Добро пожаловать.",
                "Welcome.",
            ),
            "увести": (
                "lead away, take away",
                "Они хотят увести его.",
                "They want to lead him away.",
            ),
            "неловко": (
                "awkward, uncomfortable",
                "Мне неловко.",
                "I feel awkward.",
            ),
            "математик": (
                "mathematician",
                "Он математик.",
                "He is a mathematician.",
            ),
            "просвещение": (
                "enlightenment, education",
                "Это просвещение.",
                "This is enlightenment.",
            ),
            "сверх": (
                "over, above",
                "Это сверх плана.",
                "This is over the plan.",
            ),
            "завернуть": (
                "wrap, turn",
                "Заверни это.",
                "Wrap this.",
            ),
            "муравей": (
                "ant",
                "Маленький муравей.",
                "A small ant.",
            ),
            "лопата": (
                "shovel, spade",
                "Возьми лопату.",
                "Take the shovel.",
            ),
            "заехать": (
                "to drop by, to swing by",
                "Он хочет заехать.",
                "He wants to drop by.",
            ),
            "питать": (
                "to feed, to nourish",
                "Еда питает тело.",
                "Food nourishes the body.",
            ),
            "характеризоваться": (
                "to be characterized, to be distinguished",
                "Город характеризуется этим.",
                "The city is characterized by this.",
            ),
            "даль": (
                "distance, range",
                "Смотри в даль.",
                "Look into the distance.",
            ),
            "провинциальный": (
                "provincial, rural",
                "Провинциальный город.",
                "A provincial town.",
            ),
            "ограничиться": (
                "to limit, to confine",
                "Ограничимся этим.",
                "We'll limit it to this.",
            ),
            "благополучный": (
                "prosperous, successful",
                "Благополучный год.",
                "A prosperous year.",
            ),
            "исток": (
                "source, origin",
                "Исток реки.",
                "The source of the river.",
            ),
            "откликнуться": (
                "respond, react",
                "Он откликнулся.",
                "He responded.",
            ),
            "завалить": (
                "overwhelm, bury",
                "Работа завалила меня.",
                "Work overwhelmed me.",
            ),
            "богиня": (
                "goddess, deity",
                "Она богиня.",
                "She is a goddess.",
            ),
            "коляска": (
                "stroller, carriage",
                "Детская коляска.",
                "A baby stroller.",
            ),
            "закрываться": (
                "to close, to shut",
                "Магазин закрывается.",
                "The store is closing.",
            ),
            "количественный": (
                "quantitative, numerical",
                "Количественный анализ.",
                "Quantitative analysis.",
            ),
            "физиономия": (
                "face, mug",
                "Его физиономия.",
                "His face.",
            ),
            "мелькнуть": (
                "flash, flicker",
                "Свет мелькнул.",
                "The light flashed.",
            ),
            "передвижение": (
                "movement, motion",
                "Медленное передвижение.",
                "Slow movement.",
            ),
            "отметка": (
                "mark, grade",
                "Высокая отметка.",
                "A high mark.",
            ),
            "кол": (
                "stake, pole",
                "Забей кол.",
                "Drive in the stake.",
            ),
            "прогрессивный": (
                "progressive, advanced",
                "Прогрессивный план.",
                "A progressive plan.",
            ),
            "связка": (
                "bundle, bunch",
                "Связка ключей.",
                "A bundle of keys.",
            ),
            "классовый": (
                "class",
                "Классовый конфликт.",
                "A class conflict.",
            ),
            "впадать": (
                "to fall into, to flow into",
                "Не впадай в страх.",
                "Don't fall into fear.",
            ),
            "привыкать": (
                "to get used to, to accustom",
                "Я привыкаю к этому.",
                "I get used to this.",
            ),
            "раствор": (
                "solution, solvent",
                "Водный раствор.",
                "A water solution.",
            ),
            "нажимать": (
                "press, push",
                "Нажимай кнопку.",
                "Press the button.",
            ),
            "немой": (
                "mute, dumb",
                "Он немой.",
                "He is mute.",
            ),
            "превосходный": (
                "excellent, superb",
                "Превосходный день.",
                "An excellent day.",
            ),
            "чрезмерный": (
                "excessive, undue",
                "Чрезмерный шум.",
                "Excessive noise.",
            ),
            "спустить": (
                "lower, release",
                "Спусти флаг.",
                "Lower the flag.",
            ),
            "вежливый": (
                "polite, courteous",
                "Он вежливый.",
                "He is polite.",
            ),
            "предоставляться": (
                "to be provided, to be granted",
                "Помощь предоставляется.",
                "Help is provided.",
            ),
            "возмущение": (
                "indignation, disturbance",
                "Его возмущение.",
                "His indignation.",
            ),
        },
    )
)
