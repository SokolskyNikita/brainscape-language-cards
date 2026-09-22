import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from russian_english._chunk_io import rewrite_chunk

print(
    rewrite_chunk(
        Path("russian_english/_chunks/deck_15260214_01.csv"),
        {
            "блокада": (
                "blockade, siege",
                "Блокада длилась долго.",
                "The blockade lasted long.",
            ),
            "увлечься": (
                "to get carried away, to become engrossed",
                "Он легко увлёкся игрой.",
                "He easily got carried away.",
            ),
            "греметь": (
                "to thunder, to roar",
                "Гром начал греметь.",
                "It began to thunder.",
            ),
            "дрянь": (
                "trash, rubbish",
                "Этот фильм — дрянь.",
                "This movie is trash.",
            ),
            "занавеска": (
                "curtain, drape",
                "Закрой занавеску.",
                "Close the curtain.",
            ),
            "масштабный": (
                "large-scale, massive",
                "Это масштабный план.",
                "This is a large-scale plan.",
            ),
            "воспитательный": (
                "educational, upbringing",
                "Это воспитательный момент.",
                "This is an educational moment.",
            ),
            "объединиться": (
                "unite, merge",
                "Давайте объединимся сейчас.",
                "Let's unite now.",
            ),
            "уместный": (
                "appropriate, relevant",
                "Это уместный вопрос.",
                "This is an appropriate question.",
            ),
            "отдельность": (
                "separateness, isolation",
                "Отдельность тут важна.",
                "Separateness is important here.",
            ),
            "алкоголик": (
                "alcoholic, drunkard",
                "Он бывший алкоголик.",
                "He is a former alcoholic.",
            ),
            "процветать": (
                "thrive, prosper",
                "Город начал процветать.",
                "The city began to thrive.",
            ),
            "возмущаться": (
                "to protest, to be indignant",
                "Он начал возмущаться.",
                "He began to protest.",
            ),
            "перечислять": (
                "enumerate, list",
                "Перечисли имена.",
                "Enumerate the names.",
            ),
            "честность": (
                "honesty, integrity",
                "Честность ему важна.",
                "Honesty is important to him.",
            ),
            "тьфу": (
                "yuck, phooey",
                "Тьфу, это плохо!",
                "Yuck, this is bad!",
            ),
            "побыть": (
                "to stay, to spend time",
                "Я хочу побыть тут.",
                "I want to stay here.",
            ),
            "дюйм": (
                "inch, inches",
                "Это один дюйм.",
                "This is one inch.",
            ),
            "кастрюля": (
                "pot, saucepan",
                "Суп в кастрюле.",
                "The soup is in the pot.",
            ),
            "разыскать": (
                "find, locate",
                "Полиция разыскала его.",
                "The police found him.",
            ),
            "эволюционный": (
                "evolutionary",
                "Это эволюционный процесс.",
                "This is an evolutionary process.",
            ),
            "отдача": (
                "recoil, return",
                "Отдача была сильной.",
                "The recoil was strong.",
            ),
            "смысловой": (
                "semantic, meaningful",
                "Это смысловая ошибка.",
                "This is a semantic error.",
            ),
            "преданность": (
                "loyalty, devotion",
                "Его преданность сильна.",
                "His loyalty is strong.",
            ),
            "разборка": (
                "disassembly, dismantling",
                "Начни разборку.",
                "Start the disassembly.",
            ),
            "пояснять": (
                "explain, clarify",
                "Поясни свою мысль.",
                "Explain your thought.",
            ),
            "вспомниться": (
                "come to mind, be remembered",
                "Ей вспомнилась песня.",
                "The song came to mind.",
            ),
            "гребень": (
                "comb, crest",
                "Возьми гребень.",
                "Take the comb.",
            ),
            "самка": (
                "female, female animal",
                "Смотри, это самка.",
                "Look, this is a female.",
            ),
            "отомстить": (
                "to avenge, to revenge",
                "Он отомстил за брата.",
                "He avenged his brother.",
            ),
            "тайга": (
                "taiga, boreal forest",
                "Мы едем в тайгу.",
                "We go to the taiga.",
            ),
            "протестовать": (
                "protest, demonstrate",
                "Они протестуют завтра.",
                "They protest tomorrow.",
            ),
            "пульс": (
                "pulse, heartbeat",
                "Проверь пульс.",
                "Check the pulse.",
            ),
            "ощутимый": (
                "tangible, perceptible",
                "Это ощутимый результат.",
                "This is a tangible result.",
            ),
            "грамотно": (
                "competently",
                "Она пишет грамотно.",
                "She writes competently.",
            ),
            "приземлиться": (
                "land, touch down",
                "Мы скоро приземлимся.",
                "We will land soon.",
            ),
            "искажение": (
                "distortion, warping",
                "Это искажение звука.",
                "This is a distortion of sound.",
            ),
            "помидор": (
                "tomato",
                "Я купил помидор.",
                "I bought a tomato.",
            ),
            "кирпичный": (
                "brick, brickwork",
                "Это кирпичный дом.",
                "This is a brick house.",
            ),
            "покушение": (
                "assassination attempt",
                "Это было покушение.",
                "This was an assassination attempt.",
            ),
            "свитер": (
                "sweater, jumper",
                "Я купил свитер.",
                "I bought a sweater.",
            ),
            "проектный": (
                "project, design",
                "Это проектный отдел.",
                "This is the design department.",
            ),
            "размещаться": (
                "to be located, to be situated",
                "Офис размещается тут.",
                "The office is located here.",
            ),
            "конкурсный": (
                "competitive, contest-based",
                "Это конкурсный экзамен.",
                "This is a competitive exam.",
            ),
            "восходить": (
                "rise, ascend",
                "Солнце начинает восходить.",
                "The sun begins to rise.",
            ),
            "извлекать": (
                "extract, derive",
                "Они извлекают масло.",
                "They extract oil.",
            ),
            "блаженство": (
                "bliss, beatitude",
                "Это чистое блаженство.",
                "This is pure bliss.",
            ),
            "христов": (
                "Christ's, of Christ",
                "Это Христов храм.",
                "This is Christ's temple.",
            ),
            "ожить": (
                "come to life, revive",
                "Город начал ожить.",
                "The city began to come to life.",
            ),
            "вводиться": (
                "to be introduced, to be implemented",
                "Правило вводится завтра.",
                "The rule is introduced tomorrow.",
            ),
            "замужем": (
                "married",
                "Она уже замужем.",
                "She is already married.",
            ),
            "блокировать": (
                "block",
                "Не блокируй дверь.",
                "Do not block the door.",
            ),
            "налицо": (
                "evident, apparent",
                "Проблема уже налицо.",
                "The problem is already evident.",
            ),
            "спиртное": (
                "alcohol, spirits",
                "Он не пьёт спиртное.",
                "He does not drink alcohol.",
            ),
            "смешать": (
                "mix, blend",
                "Смешай воду и соль.",
                "Mix the water and salt.",
            ),
            "изобилие": (
                "abundance, plenty",
                "Тут изобилие еды.",
                "There is an abundance of food here.",
            ),
            "поплыть": (
                "to swim, to float",
                "Он решил поплыть.",
                "He decided to swim.",
            ),
            "пир": (
                "feast, banquet",
                "Мы устроили пир.",
                "We held a feast.",
            ),
            "упадок": (
                "decline, decay",
                "Это полный упадок.",
                "This is a complete decline.",
            ),
            "негодование": (
                "indignation, outrage",
                "Её негодование понятно.",
                "Her indignation is clear.",
            ),
            "донестись": (
                "reach, carry",
                "Голос донёсся сюда.",
                "The voice reached here.",
            ),
            "пересечение": (
                "intersection, crossing",
                "Стой на пересечении.",
                "Stop at the intersection.",
            ),
            "сатана": (
                "Satan, devil",
                "Он боится сатаны.",
                "He fears Satan.",
            ),
            "тайно": (
                "secretly, covertly",
                "Она тайно ушла.",
                "She secretly left.",
            ),
            "помереть": (
                "to die, to pass away",
                "Он не хотел помереть.",
                "He did not want to die.",
            ),
            "спускать": (
                "to lower, to let down",
                "Они спускают лодку.",
                "They lower the boat.",
            ),
            "улетать": (
                "to fly away, to depart",
                "Птицы улетают на юг.",
                "The birds fly away south.",
            ),
            "темнеть": (
                "to darken, to grow dark",
                "Небо начало темнеть.",
                "The sky began to darken.",
            ),
            "пшеница": (
                "wheat, wheat grain",
                "Они продают пшеницу.",
                "They sell wheat.",
            ),
            "пространственный": (
                "spatial, three-dimensional",
                "Это пространственный план.",
                "This is a spatial plan.",
            ),
            "веровать": (
                "to believe, to have faith",
                "Они веруют в Бога.",
                "They believe in God.",
            ),
            "употребить": (
                "use, consume",
                "Он употребил это слово.",
                "He used this word.",
            ),
            "являть": (
                "show, reveal",
                "Он явил силу.",
                "He showed strength.",
            ),
            "празднование": (
                "celebration, festivity",
                "Празднование уже началось.",
                "The celebration already started.",
            ),
            "посмеяться": (
                "laugh, have a laugh",
                "Мы хотели посмеяться.",
                "We wanted to laugh.",
            ),
            "сухо": (
                "dry, arid",
                "Полотенце уже сухо.",
                "The towel is already dry.",
            ),
            "некоммерческий": (
                "non-commercial, nonprofit",
                "Это некоммерческий проект.",
                "This is a non-commercial project.",
            ),
            "погасить": (
                "extinguish, repay",
                "Погаси свечу.",
                "Extinguish the candle.",
            ),
            "обыкновенно": (
                "usually, ordinarily",
                "Она обыкновенно пьёт чай.",
                "She usually drinks tea.",
            ),
            "склоняться": (
                "to incline, to tend",
                "Я склоняюсь к этому плану.",
                "I incline to this plan.",
            ),
            "откинуться": (
                "recline, lean back",
                "Он откинулся на стул.",
                "He reclined on the chair.",
            ),
            "бухта": (
                "bay, cove",
                "Мы вошли в бухту.",
                "We entered the bay.",
            ),
            "главнокомандующий": (
                "commander-in-chief, supreme commander",
                "Он наш главнокомандующий.",
                "He is our commander-in-chief.",
            ),
            "отдаваться": (
                "devote oneself, give oneself up",
                "Она отдаётся работе.",
                "She devotes herself to work.",
            ),
            "символизировать": (
                "symbolize, represent",
                "Это символизирует мир.",
                "This symbolizes peace.",
            ),
            "индустриальный": (
                "industrial, industrialized",
                "Это индустриальный город.",
                "This is an industrial city.",
            ),
            "глобализация": (
                "globalization, globalisation",
                "Глобализация меняет мир.",
                "Globalization changes the world.",
            ),
            "незаметный": (
                "inconspicuous, unnoticeable",
                "Он остался незаметным.",
                "He remained inconspicuous.",
            ),
            "пожертвовать": (
                "donate, sacrifice",
                "Пожертвуй книгу.",
                "Donate the book.",
            ),
            "мучение": (
                "torture, agony",
                "Это было мучение.",
                "This was torture.",
            ),
            "ветерок": (
                "breeze, zephyr",
                "Ветерок был тихий.",
                "The breeze was quiet.",
            ),
            "применительно": (
                "in relation to",
                "Применительно к делу — да.",
                "In relation to the matter, yes.",
            ),
            "особь": (
                "individual, specimen",
                "Это редкая особь.",
                "This is a rare individual.",
            ),
            "цветовой": (
                "color, chromatic",
                "Это цветовой круг.",
                "This is a color circle.",
            ),
            "крона": (
                "crown, canopy",
                "Крона дерева большая.",
                "The tree's crown is big.",
            ),
            "увидеться": (
                "to meet, to see each other",
                "Мы хотим увидеться.",
                "We want to meet.",
            ),
            "низ": (
                "bottom",
                "Низ коробки мокрый.",
                "The bottom of the box is wet.",
            ),
            "монолог": (
                "monologue, soliloquy",
                "Он начал монолог.",
                "He began a monologue.",
            ),
            "сердито": (
                "angrily, crossly",
                "Он сердито посмотрел.",
                "He looked angrily.",
            ),
            "вертикаль": (
                "vertical, vertical line",
                "Проведи вертикаль.",
                "Draw a vertical line.",
            ),
        },
    )
)
