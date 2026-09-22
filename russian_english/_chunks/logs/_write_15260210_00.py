import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from russian_english._chunk_io import rewrite_chunk

print(
    rewrite_chunk(
        Path("russian_english/_chunks/deck_15260210_00.csv"),
        {
            "прижаться": (
                "to press close",
                "Она прижалась к отцу.",
                "She pressed close to her father.",
            ),
            "ансамбль": (
                "ensemble",
                "Ансамбль хорошо выступил.",
                "The ensemble performed well.",
            ),
            "крохотный": (
                "tiny",
                "Крохотный кот спит.",
                "The tiny cat sleeps.",
            ),
            "предательство": (
                "betrayal",
                "Это настоящее предательство.",
                "This is a real betrayal.",
            ),
            "прохладный": (
                "cool",
                "Ветер сегодня прохладный.",
                "The wind is cool today.",
            ),
            "метафора": (
                "metaphor",
                "Это только метафора.",
                "This is only a metaphor.",
            ),
            "резюме": (
                "resume",
                "Вот моё резюме.",
                "Here is my resume.",
            ),
            "фиксировать": (
                "to record",
                "Нужно фиксировать факты.",
                "We need to record the facts.",
            ),
            "грядущий": (
                "upcoming",
                "Грядущий год будет трудным.",
                "The upcoming year will be hard.",
            ),
            "нора": (
                "burrow",
                "Лиса сидит в норе.",
                "The fox sits in the burrow.",
            ),
            "печень": (
                "liver",
                "У папы болит печень.",
                "Dad's liver hurts.",
            ),
            "интенсивность": (
                "intensity",
                "Интенсивность света выросла.",
                "The intensity of the light grew.",
            ),
            "таракан": (
                "cockroach",
                "Я вижу таракана.",
                "I see a cockroach.",
            ),
            "обочина": (
                "shoulder",
                "Машина стоит на обочине.",
                "The car stands on the shoulder.",
            ),
            "противоречивый": (
                "contradictory",
                "Его слова противоречивы.",
                "His words are contradictory.",
            ),
            "сходиться": (
                "to converge",
                "Дороги сходятся у реки.",
                "The roads converge at the river.",
            ),
            "близнец": (
                "twin",
                "Он мой близнец.",
                "He is my twin.",
            ),
            "старательно": (
                "diligently",
                "Она старательно работает.",
                "She works diligently.",
            ),
            "преподавание": (
                "teaching",
                "Она любит преподавание.",
                "She loves teaching.",
            ),
            "героический": (
                "heroic",
                "Это героический поступок.",
                "This is a heroic act.",
            ),
            "выбрасывать": (
                "to throw away",
                "Я выбрасываю старые письма.",
                "I throw away old letters.",
            ),
            "переезд": (
                "move",
                "Переезд будет завтра.",
                "The move will be tomorrow.",
            ),
            "размах": (
                "scale",
                "Размах работ огромный.",
                "The scale of the work is huge.",
            ),
            "предвидеть": (
                "to foresee",
                "Я предвижу проблемы.",
                "I foresee problems.",
            ),
            "прижимать": (
                "to press",
                "Она прижимает книгу.",
                "She presses the book.",
            ),
            "глина": (
                "clay",
                "Она работает с глиной.",
                "She works with clay.",
            ),
            "переработка": (
                "recycling",
                "Переработка бумаги важна.",
                "Recycling paper is important.",
            ),
            "трон": (
                "throne",
                "Король сел на трон.",
                "The king sat on the throne.",
            ),
            "взнос": (
                "payment",
                "Я сделал взнос.",
                "I made a payment.",
            ),
            "хвалить": (
                "to praise",
                "Учитель хвалит ученика.",
                "The teacher praises the student.",
            ),
            "стрелковый": (
                "shooting",
                "Это стрелковый клуб.",
                "This is a shooting club.",
            ),
            "пищевой": (
                "food",
                "Пищевые продукты свежие.",
                "The food products are fresh.",
            ),
            "ленинский": (
                "Leninist",
                "Это ленинский план.",
                "This is a Leninist plan.",
            ),
            "алтарь": (
                "altar",
                "Они стоят у алтаря.",
                "They stand at the altar.",
            ),
            "очаровательный": (
                "charming",
                "Она очень очаровательная.",
                "She is very charming.",
            ),
            "рвануть": (
                "to dash",
                "Он рванул домой.",
                "He dashed home.",
            ),
            "референдум": (
                "referendum",
                "Завтра будет референдум.",
                "There will be a referendum tomorrow.",
            ),
            "одобрение": (
                "approval",
                "Я жду твоего одобрения.",
                "I wait for your approval.",
            ),
            "гул": (
                "hum",
                "Я слышу гул.",
                "I hear a hum.",
            ),
            "крючок": (
                "hook",
                "Я повесил пальто на крючок.",
                "I hung the coat on the hook.",
            ),
            "биология": (
                "biology",
                "Я изучаю биологию в университете.",
                "I study biology at university.",
            ),
            "балет": (
                "ballet",
                "Она любит балет.",
                "She loves ballet.",
            ),
            "реализоваться": (
                "to be realized",
                "План реализовался.",
                "The plan was realized.",
            ),
            "рыдать": (
                "to sob",
                "Она начала рыдать.",
                "She began to sob.",
            ),
            "чайка": (
                "seagull",
                "Чайка летит над морем.",
                "A seagull flies over the sea.",
            ),
            "склониться": (
                "to bow",
                "Он склонился перед отцом.",
                "He bowed before his father.",
            ),
            "запросто": (
                "easily",
                "Он запросто это сделал.",
                "He easily did this.",
            ),
            "стремительный": (
                "rapid",
                "Это стремительное решение.",
                "This is a rapid decision.",
            ),
            "божество": (
                "deity",
                "Они верят в божество.",
                "They believe in a deity.",
            ),
            "метаться": (
                "to rush about",
                "Он метался по комнате.",
                "He rushed about the room.",
            ),
            "порошок": (
                "powder",
                "Я купил порошок.",
                "I bought powder.",
            ),
            "выяснять": (
                "to find out",
                "Мы выясняем правду.",
                "We are finding out the truth.",
            ),
            "пушкинский": (
                "Pushkin's",
                "Это пушкинский музей.",
                "This is Pushkin's museum.",
            ),
            "документальный": (
                "documentary",
                "Я смотрю документальный фильм.",
                "I watch a documentary.",
            ),
            "добродетель": (
                "virtue",
                "Терпение - это добродетель.",
                "Patience is a virtue.",
            ),
            "выписать": (
                "to write out",
                "Врач выписал лекарство.",
                "The doctor wrote out the medicine.",
            ),
            "узор": (
                "pattern",
                "На платье красивый узор.",
                "The dress has a beautiful pattern.",
            ),
            "выслать": (
                "to send out",
                "Вышлите письмо сегодня.",
                "Send out the letter today.",
            ),
            "стадион": (
                "stadium",
                "Мы идём на стадион.",
                "We go to the stadium.",
            ),
            "дрожь": (
                "shiver",
                "Меня взяла дрожь.",
                "A shiver took me.",
            ),
            "человечек": (
                "little man",
                "Я вижу человечка.",
                "I see a little man.",
            ),
            "трясти": (
                "to shake",
                "Не тряси стол.",
                "Don't shake the table.",
            ),
            "подписывать": (
                "to sign",
                "Я подписываю письмо.",
                "I sign the letter.",
            ),
            "согласование": (
                "agreement",
                "Нужно согласование плана.",
                "We need agreement on the plan.",
            ),
            "роддом": (
                "maternity hospital, maternity ward",
                "Она родила в роддоме.",
                "She gave birth at the maternity hospital.",
            ),
            "трудящийся": (
                "worker",
                "Трудящийся идёт на работу.",
                "The worker goes to work.",
            ),
            "либерал": (
                "liberal",
                "Он политический либерал.",
                "He is a political liberal.",
            ),
            "секретарша": (
                "secretary",
                "Секретарша отвечает на звонок.",
                "The secretary answers the call.",
            ),
            "подсознание": (
                "subconscious",
                "Это из подсознания.",
                "This is from the subconscious.",
            ),
            "подсказывать": (
                "to hint",
                "Она подсказывает ответ.",
                "She hints at the answer.",
            ),
            "проповедь": (
                "sermon",
                "Он читает проповедь.",
                "He reads a sermon.",
            ),
            "запускать": (
                "to launch",
                "Они запускают программу.",
                "They launch the program.",
            ),
            "факс": (
                "fax, facsimile",
                "Я получил факс вчера.",
                "I received the fax yesterday.",
            ),
            "комфорт": (
                "comfort",
                "В доме есть комфорт.",
                "There is comfort in the house.",
            ),
            "трансформация": (
                "transformation",
                "Его трансформация удивила нас.",
                "His transformation surprised us.",
            ),
            "преступность": (
                "crime",
                "Преступность в городе растёт.",
                "Crime in the city grows.",
            ),
            "парашют": (
                "parachute",
                "У него есть парашют.",
                "He has a parachute.",
            ),
            "господствовать": (
                "to dominate",
                "Эта идея господствует.",
                "This idea dominates.",
            ),
            "перенос": (
                "transfer",
                "Перенос встречи на пятницу.",
                "The transfer is to Friday.",
            ),
            "верхушка": (
                "top",
                "Верхушка дерева сухая.",
                "The top of the tree is dry.",
            ),
            "горка": (
                "slide",
                "Он играет на горке.",
                "He plays on the slide.",
            ),
            "процентный": (
                "interest",
                "Процентная ставка высокая.",
                "The interest rate is high.",
            ),
            "связываться": (
                "to contact",
                "Я связываюсь с другом.",
                "I contact a friend.",
            ),
            "цензура": (
                "censorship",
                "Цензура убивает правду.",
                "Censorship kills the truth.",
            ),
            "птичка": (
                "little bird",
                "Птичка сидит на окне.",
                "A little bird sits on the window.",
            ),
            "мутный": (
                "murky",
                "Вода сегодня мутная.",
                "The water is murky today.",
            ),
            "интрига": (
                "intrigue",
                "В доме есть интрига.",
                "There is intrigue in the house.",
            ),
            "складывать": (
                "to fold",
                "Она складывает одежду.",
                "She folds the clothes.",
            ),
            "многолетний": (
                "long-term",
                "Это многолетний труд.",
                "This is long-term work.",
            ),
            "ранение": (
                "wound",
                "Ранение было глубоким.",
                "The wound was deep.",
            ),
            "стирать": (
                "to wash",
                "Я стираю рубашку.",
                "I wash the shirt.",
            ),
            "сойтись": (
                "to come together",
                "Мы сошлись у дома.",
                "We came together at the house.",
            ),
            "недаром": (
                "not for nothing",
                "Недаром его хвалят.",
                "They praise him not for nothing.",
            ),
            "насквозь": (
                "through",
                "Я мокрый насквозь.",
                "I am wet through.",
            ),
            "сумочка": (
                "handbag",
                "Она забыла сумочку.",
                "She forgot the handbag.",
            ),
            "обломок": (
                "fragment",
                "Обломок стекла на стуле.",
                "A fragment of glass is on the chair.",
            ),
            "пересечь": (
                "to cross, to intersect",
                "Мы планируем пересечь реку.",
                "We plan to cross the river.",
            ),
            "шуба": (
                "fur coat",
                "На ней новая шуба.",
                "She has a new fur coat.",
            ),
            "загнать": (
                "to drive in",
                "Он загнал гвоздь.",
                "He drove in the nail.",
            ),
            "бокс": (
                "boxing",
                "Он смотрит бокс.",
                "He watches boxing.",
            ),
        },
    )
)
