import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from russian_english._chunk_io import rewrite_chunk

print(
    rewrite_chunk(
        Path("russian_english/_chunks/deck_15260218_02.csv"),
        {
            "костыль": (
                "crutch",
                "Мне нужен костыль.",
                "I need a crutch.",
            ),
            "равно": (
                "equal",
                "Два плюс два равно четыре.",
                "Two plus two equals four.",
            ),
            "очищение": (
                "cleansing",
                "Мне нужно очищение.",
                "I need a cleansing.",
            ),
            "официантка": (
                "waitress",
                "Где официантка?",
                "Where is the waitress?",
            ),
            "подростковый": (
                "teenage",
                "Это подростковый возраст.",
                "This is the teenage age.",
            ),
            "косвенно": (
                "indirectly",
                "Он косвенно сказал да.",
                "He indirectly said yes.",
            ),
            "привычно": (
                "habitually",
                "Она привычно говорит нет.",
                "She habitually says no.",
            ),
            "нехитрый": (
                "simple",
                "План нехитрый.",
                "The plan is simple.",
            ),
            "мерзавец": (
                "scoundrel",
                "Он полный мерзавец.",
                "He is a complete scoundrel.",
            ),
            "дистанционный": (
                "remote",
                "Это дистанционный урок.",
                "This is a remote lesson.",
            ),
            "окрасить": (
                "paint",
                "Я окрашу стену.",
                "I will paint the wall.",
            ),
            "словосочетание": (
                "word combination",
                "Это простое словосочетание.",
                "This is a simple word combination.",
            ),
            "шприц": (
                "syringe",
                "Где шприц?",
                "Where is the syringe?",
            ),
            "аграрный": (
                "agrarian",
                "Это аграрный район.",
                "This is an agrarian region.",
            ),
            "посланник": (
                "messenger",
                "Посланник уже здесь.",
                "The messenger is already here.",
            ),
            "уполномочить": (
                "authorize",
                "Я уполномочил его.",
                "I authorized him.",
            ),
            "патент": (
                "patent",
                "У него есть патент.",
                "He has a patent.",
            ),
            "репертуар": (
                "repertoire",
                "Какой у неё репертуар?",
                "What is her repertoire?",
            ),
            "отчуждение": (
                "alienation",
                "Я чувствую отчуждение.",
                "I feel alienation.",
            ),
            "нащупать": (
                "feel",
                "Нащупай ключ.",
                "Feel the key.",
            ),
            "привидение": (
                "ghost",
                "Я видел привидение.",
                "I saw a ghost.",
            ),
            "морщина": (
                "wrinkle",
                "У неё есть морщина.",
                "She has a wrinkle.",
            ),
            "недоумевать": (
                "be puzzled",
                "Я недоумеваю.",
                "I am puzzled.",
            ),
            "теннис": (
                "tennis",
                "Я играю в теннис.",
                "I play tennis.",
            ),
            "копаться": (
                "rummage",
                "Он копается в сумке.",
                "He is rummaging in the bag.",
            ),
            "пояснение": (
                "explanation",
                "Мне нужно пояснение.",
                "I need an explanation.",
            ),
            "покорный": (
                "submissive",
                "Он слишком покорный.",
                "He is too submissive.",
            ),
            "перечитывать": (
                "reread",
                "Я перечитываю письмо.",
                "I am rereading the letter.",
            ),
            "сюжетный": (
                "plot",
                "Это сюжетная линия.",
                "This is a plot line.",
            ),
            "ого": (
                "wow",
                "Ого, как красиво!",
                "Wow, how beautiful!",
            ),
            "дискурс": (
                "discourse",
                "Это научный дискурс.",
                "This is scientific discourse.",
            ),
            "подземелье": (
                "dungeon",
                "Это старое подземелье.",
                "This is an old dungeon.",
            ),
            "болтовня": (
                "chatter",
                "Это пустая болтовня.",
                "This is empty chatter.",
            ),
            "равняться": (
                "emulate",
                "Он равняется на отца.",
                "He emulates his father.",
            ),
            "бактерия": (
                "bacterium",
                "Это опасная бактерия.",
                "This is a dangerous bacterium.",
            ),
            "простираться": (
                "stretch",
                "Лес простирается до реки.",
                "The forest stretches to the river.",
            ),
            "раунд": (
                "round",
                "Это первый раунд.",
                "This is the first round.",
            ),
            "сборный": (
                "national team",
                "Это сборная команда.",
                "This is the national team.",
            ),
            "фу": (
                "yuck",
                "Фу, это плохо пахнет.",
                "Yuck, this smells bad.",
            ),
            "иммигрант": (
                "immigrant",
                "Он иммигрант.",
                "He is an immigrant.",
            ),
            "доцент": (
                "associate professor",
                "Она доцент.",
                "She is an associate professor.",
            ),
            "эстрада": (
                "stage",
                "Она на эстраде.",
                "She is on stage.",
            ),
            "геометрический": (
                "geometric",
                "Это геометрический узор.",
                "This is a geometric pattern.",
            ),
            "трещать": (
                "crack",
                "Дерево трещит.",
                "The tree is cracking.",
            ),
            "совхоз": (
                "state farm",
                "Он работает в совхозе.",
                "He works on a state farm.",
            ),
            "запретный": (
                "forbidden",
                "Это запретный плод.",
                "This is forbidden fruit.",
            ),
            "прогуляться": (
                "walk",
                "Давай прогуляемся.",
                "Let's walk.",
            ),
            "парик": (
                "wig",
                "Это новый парик.",
                "This is a new wig.",
            ),
            "справочный": (
                "reference",
                "Это справочная книга.",
                "This is a reference book.",
            ),
            "воскресение": (
                "resurrection",
                "Это воскресение.",
                "This is the resurrection.",
            ),
            "взирать": (
                "gaze",
                "Он взирает на море.",
                "He gazes at the sea.",
            ),
            "общепринятый": (
                "generally accepted",
                "Это общепринятое мнение.",
                "This is a generally accepted opinion.",
            ),
            "минский": (
                "Minsk",
                "Это минский поезд.",
                "This is a Minsk train.",
            ),
            "необъяснимый": (
                "inexplicable",
                "Страх был необъяснимым.",
                "The fear was inexplicable.",
            ),
            "сова": (
                "owl",
                "Сова на дереве.",
                "The owl is on the tree.",
            ),
            "удельный": (
                "specific",
                "Измерь удельный вес.",
                "Measure the specific weight.",
            ),
            "вышка": (
                "tower",
                "Там высокая вышка.",
                "There is a tall tower there.",
            ),
            "технически": (
                "technically",
                "Технически это верно.",
                "Technically this is true.",
            ),
            "тропический": (
                "tropical",
                "Это тропический остров.",
                "This is a tropical island.",
            ),
            "геологический": (
                "geological",
                "Это геологический музей.",
                "This is a geological museum.",
            ),
            "ассамблея": (
                "assembly",
                "Это большая ассамблея.",
                "This is a large assembly.",
            ),
            "двойник": (
                "double",
                "У него есть двойник.",
                "He has a double.",
            ),
            "политически": (
                "politically",
                "Это политически важно.",
                "This is politically important.",
            ),
            "функциональность": (
                "functionality",
                "Мне нравится функциональность.",
                "I like the functionality.",
            ),
            "агитация": (
                "campaigning",
                "Это политическая агитация.",
                "This is political campaigning.",
            ),
            "диктатор": (
                "dictator",
                "Он диктатор.",
                "He is a dictator.",
            ),
            "гласность": (
                "openness",
                "Нам нужна гласность.",
                "We need openness.",
            ),
            "отклонить": (
                "reject",
                "Они отклонили план.",
                "They rejected the plan.",
            ),
            "сани": (
                "sleigh",
                "Это сани.",
                "This is a sleigh.",
            ),
            "мозговой": (
                "brain",
                "Это мозговой центр.",
                "This is a brain center.",
            ),
            "представительный": (
                "impressive",
                "Он представительный мужчина.",
                "He is an impressive man.",
            ),
            "чума": (
                "plague",
                "Это страшная чума.",
                "This is a terrible plague.",
            ),
            "пенис": (
                "penis",
                "Это мужской пенис.",
                "This is a male penis.",
            ),
            "лицензионный": (
                "licensed",
                "Это лицензионный диск.",
                "This is a licensed disc.",
            ),
            "созерцание": (
                "contemplation",
                "Она любит созерцание.",
                "She loves contemplation.",
            ),
            "райский": (
                "heavenly",
                "Это райский остров.",
                "This is a heavenly island.",
            ),
            "валенок": (
                "felt boot",
                "Где мой валенок?",
                "Where is my felt boot?",
            ),
            "экспонат": (
                "exhibit",
                "Это новый экспонат.",
                "This is a new exhibit.",
            ),
            "кипяток": (
                "boiling water",
                "Осторожно, кипяток.",
                "Careful, boiling water.",
            ),
            "купля": (
                "purchase",
                "Это договор купли.",
                "This is a purchase contract.",
            ),
            "танцевальный": (
                "dance",
                "Это танцевальный клуб.",
                "This is a dance club.",
            ),
            "неофициальный": (
                "unofficial",
                "Это неофициальная встреча.",
                "This is an unofficial meeting.",
            ),
            "мечеть": (
                "mosque",
                "Это старая мечеть.",
                "This is an old mosque.",
            ),
            "электромагнитный": (
                "electromagnetic",
                "Это электромагнитное поле.",
                "This is an electromagnetic field.",
            ),
            "клюв": (
                "beak",
                "У птицы острый клюв.",
                "The bird has a sharp beak.",
            ),
            "встревожить": (
                "alarm",
                "Не встревожь её.",
                "Don't alarm her.",
            ),
            "клевета": (
                "slander",
                "Это чистая клевета.",
                "This is pure slander.",
            ),
            "храбрость": (
                "courage",
                "Ему нужна храбрость.",
                "He needs courage.",
            ),
            "поклоняться": (
                "worship",
                "Они поклоняются богу.",
                "They worship God.",
            ),
            "выявлять": (
                "reveal",
                "Тесты выявляют ошибки.",
                "Tests reveal mistakes.",
            ),
            "угу": (
                "uh-huh",
                "Угу, хорошо.",
                "Uh-huh, good.",
            ),
            "уполномоченный": (
                "authorized",
                "Он уполномоченный.",
                "He is authorized.",
            ),
            "отталкивать": (
                "repel",
                "Этот запах отталкивает.",
                "This smell repels.",
            ),
            "имитировать": (
                "imitate",
                "Дети имитируют взрослых.",
                "Children imitate adults.",
            ),
            "посвящение": (
                "dedication",
                "Это посвящение.",
                "This is a dedication.",
            ),
            "ловля": (
                "fishing",
                "Ему нравится ловля рыбы.",
                "He likes fishing.",
            ),
            "динамо": (
                "dynamo",
                "Это старое динамо.",
                "This is an old dynamo.",
            ),
            "несложный": (
                "simple",
                "Задача несложная.",
                "The task is simple.",
            ),
            "периферия": (
                "periphery",
                "Дома на периферии.",
                "The houses are on the periphery.",
            ),
            "островок": (
                "islet",
                "Там маленький островок.",
                "There is a small islet there.",
            ),
        },
    )
)
