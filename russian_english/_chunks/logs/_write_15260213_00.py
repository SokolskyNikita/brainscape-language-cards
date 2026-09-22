import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from russian_english._chunk_io import rewrite_chunk

print(
    rewrite_chunk(
        Path("russian_english/_chunks/deck_15260213_00.csv"),
        {
            "литератор": (
                "writer, man of letters",
                "Литератор опубликовал свой роман.",
                "The writer published his novel.",
            ),
            "поглощать": (
                "absorb, consume",
                "Растения поглощают свет.",
                "Plants absorb light.",
            ),
            "литься": (
                "to flow, to pour",
                "Слёзы льются из глаз.",
                "Tears flow from the eyes.",
            ),
            "пресловутый": (
                "notorious, infamous",
                "Его пресловутый план провалился.",
                "His notorious plan failed.",
            ),
            "неподвижно": (
                "motionless, immobile",
                "Кот сидел неподвижно.",
                "The cat sat motionless.",
            ),
            "приспособление": (
                "device, adapter",
                "Это простое приспособление.",
                "This is a simple device.",
            ),
            "различаться": (
                "to differ, to vary",
                "Их мнения различаются.",
                "Their opinions differ.",
            ),
            "цепляться": (
                "cling, hold on",
                "Листья цепляются за мокрое окно.",
                "Leaves cling to the wet window.",
            ),
            "бас": (
                "bass, contrabass",
                "Он прекрасно играл на басе.",
                "He played the bass beautifully.",
            ),
            "выпадать": (
                "to fall out, to drop out",
                "Мои волосы начали выпадать.",
                "My hair started to fall out.",
            ),
            "увольнение": (
                "dismissal, termination",
                "Его увольнение потрясло весь офис.",
                "His dismissal shocked the entire office.",
            ),
            "просматривать": (
                "to browse, to look through",
                "Я просматриваю почту.",
                "I browse the mail.",
            ),
            "достигаться": (
                "to be achieved, to be attained",
                "Успех достигается трудом.",
                "Success is achieved by work.",
            ),
            "снабдить": (
                "supply, equip",
                "Мы должны снабдить войска едой.",
                "We must supply the troops with food.",
            ),
            "социология": (
                "sociology",
                "Я изучаю социологию в университете.",
                "I study sociology at university.",
            ),
            "пересекать": (
                "to cross, to intersect",
                "Мы пересекаем реку.",
                "We cross the river.",
            ),
            "пират": (
                "pirate, buccaneer",
                "Пират украл сундук с сокровищами.",
                "The pirate stole the treasure chest.",
            ),
            "лягушка": (
                "frog",
                "Лягушка прыгнула в пруд.",
                "The frog jumped into the pond.",
            ),
            "востребовать": (
                "to claim",
                "Он востребовал свой долг.",
                "He claimed his debt.",
            ),
            "прозвище": (
                "nickname",
                "Ему дали смешное прозвище.",
                "They gave him a funny nickname.",
            ),
            "глубинный": (
                "deep, profound",
                "У него глубинный страх.",
                "He has a deep fear.",
            ),
            "хохот": (
                "laughter",
                "Её хохот заполнил комнату.",
                "Her laughter filled the room.",
            ),
            "коли": (
                "if, when",
                "Останься, коли устал.",
                "Stay if you are tired.",
            ),
            "сократиться": (
                "to decrease",
                "Расходы сильно сократились.",
                "Expenses decreased a lot.",
            ),
            "четырнадцать": (
                "fourteen",
                "Ей исполнилось четырнадцать в прошлом месяце.",
                "She turned fourteen last month.",
            ),
            "погружаться": (
                "to dive, to immerse",
                "Он погружается в воду.",
                "He dives into the water.",
            ),
            "комар": (
                "mosquito",
                "Комар сел мне на руку.",
                "A mosquito sat on my hand.",
            ),
            "крайность": (
                "extreme, extremity",
                "Это уже крайность.",
                "This is already an extreme.",
            ),
            "арена": (
                "arena, venue",
                "На арене было много народа.",
                "There were many people in the arena.",
            ),
            "оборонительный": (
                "defensive, protective",
                "Это оборонительный ход.",
                "This is a defensive move.",
            ),
            "достойно": (
                "worthily, deservedly",
                "Он прожил свою жизнь достойно.",
                "He lived his life worthily.",
            ),
            "потрясение": (
                "shock, amazement",
                "Новость была полным потрясением.",
                "The news was a complete shock.",
            ),
            "каблук": (
                "heel, stiletto",
                "Она сломала каблук на вечеринке.",
                "She broke her heel at the party.",
            ),
            "прелестный": (
                "charming, lovely",
                "Она носила прелестное летнее платье.",
                "She wore a charming summer dress.",
            ),
            "впрямь": (
                "indeed, really",
                "Она впрямь очень талантлива.",
                "She is indeed very talented.",
            ),
            "расспрашивать": (
                "to question, to interrogate",
                "Он начал расспрашивать свидетеля.",
                "He began to question the witness.",
            ),
            "общность": (
                "commonality",
                "Между ними есть общность взглядов.",
                "There is a commonality of views.",
            ),
            "кузов": (
                "body, car body",
                "Кузов машины в грязи.",
                "The car body is dirty.",
            ),
            "обновить": (
                "update, refresh",
                "Обнови страницу.",
                "Update the page.",
            ),
            "уделить": (
                "devote, allocate",
                "Удели мне минуту.",
                "Devote a minute to me.",
            ),
            "наземный": (
                "terrestrial, ground-based",
                "Это наземный транспорт.",
                "This is terrestrial transport.",
            ),
            "диктовать": (
                "dictate",
                "Он диктует письмо.",
                "He dictates a letter.",
            ),
            "студентка": (
                "female student",
                "Студентка сдала экзамен.",
                "The female student passed the exam.",
            ),
            "кухонный": (
                "kitchen, culinary",
                "Кухонный нож очень острый.",
                "The kitchen knife is very sharp.",
            ),
            "свадебный": (
                "wedding, bridal",
                "Она надела свадебное платье.",
                "She put on the wedding dress.",
            ),
            "воспроизведение": (
                "playback, reproduction",
                "Воспроизведение звука плохое.",
                "The sound playback is bad.",
            ),
            "пообщаться": (
                "to chat, to communicate",
                "Давай пообщаемся вечером.",
                "Let's chat in the evening.",
            ),
            "текстовый": (
                "text, textual",
                "Это текстовый файл.",
                "This is a text file.",
            ),
            "мостик": (
                "footbridge, gangway",
                "Мы прошли по мостику.",
                "We walked on the footbridge.",
            ),
            "накормить": (
                "to feed, to nourish",
                "Мне нужно накормить кота.",
                "I need to feed the cat.",
            ),
            "аборт": (
                "abortion",
                "Врач говорил об аборте.",
                "The doctor spoke about abortion.",
            ),
            "испуганно": (
                "frightened, scared",
                "Она испуганно оглянулась.",
                "She looked back frightened.",
            ),
            "досада": (
                "annoyance, vexation",
                "Его ошибка была большой досадой.",
                "His mistake was a great annoyance.",
            ),
            "публиковаться": (
                "to be published, to appear",
                "Он публикуется каждый год.",
                "He is published every year.",
            ),
            "коллегия": (
                "board, college",
                "Коллегия одобрила предложение.",
                "The board approved the proposal.",
            ),
            "задолго": (
                "long before, well in advance",
                "Он прибыл задолго до нас.",
                "He arrived long before us.",
            ),
            "перебраться": (
                "move, relocate",
                "Мы переберёмся в новый город.",
                "We will move to a new city.",
            ),
            "ограда": (
                "fence, enclosure",
                "Ограда вокруг сада высокая.",
                "The fence around the garden is high.",
            ),
            "репрессия": (
                "repression, crackdown",
                "Народ помнит те репрессии.",
                "The people remember that repression.",
            ),
            "приток": (
                "inflow, tributary",
                "Приток воды вырос.",
                "The inflow of water grew.",
            ),
            "охотничий": (
                "hunting, hunter's",
                "Он носил свой охотничий пиджак.",
                "He wore his hunting jacket.",
            ),
            "имперский": (
                "imperial",
                "Это имперский дворец.",
                "This is an imperial palace.",
            ),
            "гонять": (
                "chase, drive",
                "Собака гоняет кошку.",
                "The dog chases the cat.",
            ),
            "паровоз": (
                "steam locomotive, locomotive",
                "Паровоз остановился у станции.",
                "The steam locomotive stopped at the station.",
            ),
            "крепостной": (
                "serf, bonded",
                "Крепостной работал на земле лорда.",
                "The serf worked the lord's land.",
            ),
            "продовольствие": (
                "food, provisions",
                "Нам нужно больше продовольствия.",
                "We need more food.",
            ),
            "топ": (
                "top",
                "Он в топе списка.",
                "He is at the top of the list.",
            ),
            "продвинуть": (
                "promote, advance",
                "Они хотят продвинуть его.",
                "They want to promote him.",
            ),
            "оглядеть": (
                "to look over, to examine",
                "Он оглядел комнату.",
                "He looked over the room.",
            ),
            "бронзовый": (
                "bronze, bronzy",
                "Она выиграла бронзовую медаль.",
                "She won the bronze medal.",
            ),
            "обобщение": (
                "generalization, abstraction",
                "Его обобщение неверно.",
                "His generalization is wrong.",
            ),
            "супружеский": (
                "matrimonial, conjugal",
                "У них спокойная супружеская жизнь.",
                "They have a quiet matrimonial life.",
            ),
            "злодей": (
                "villain, evildoer",
                "Злодей убежал в лес.",
                "The villain ran into the forest.",
            ),
            "погаснуть": (
                "go out, fade",
                "Свет внезапно погас.",
                "The light went out suddenly.",
            ),
            "обрыв": (
                "precipice, cliff",
                "Он стоял на обрыве.",
                "He stood on the cliff.",
            ),
            "звенеть": (
                "ring, jingle",
                "В кармане звенит монета.",
                "A coin rings in the pocket.",
            ),
            "живописный": (
                "picturesque, scenic",
                "Какой живописный вид.",
                "What a picturesque view.",
            ),
            "сочетаться": (
                "to match, to combine",
                "Эти цвета хорошо сочетаются.",
                "These colors match well.",
            ),
            "нежелательный": (
                "undesirable, unwanted",
                "Курение - нежелательная привычка.",
                "Smoking is an undesirable habit.",
            ),
            "укладываться": (
                "to go to bed, to fit",
                "Она укладывается спать.",
                "She goes to bed.",
            ),
            "наглый": (
                "impudent, cheeky",
                "Какой наглый ответ.",
                "What an impudent answer.",
            ),
            "дефект": (
                "defect, flaw",
                "Продукт имеет производственный дефект.",
                "The product has a manufacturing defect.",
            ),
            "блаженный": (
                "blessed, blissful",
                "Какое блаженное утро.",
                "What a blissful morning.",
            ),
            "нижегородский": (
                "Nizhny Novgorod, Nizhegorodsky",
                "Он живёт в нижегородском крае.",
                "He lives in the Nizhny Novgorod region.",
            ),
            "ракетный": (
                "rocket, missile",
                "Это ракетный двигатель.",
                "This is a rocket engine.",
            ),
            "мурманский": (
                "Murmansk, Murmansk-related",
                "Мы едем в мурманский порт.",
                "We are going to the Murmansk port.",
            ),
            "изрядно": (
                "considerably, quite",
                "Он изрядно устал.",
                "He is considerably tired.",
            ),
            "изволить": (
                "deign, please",
                "Она не изволила ответить.",
                "She didn't deign to answer.",
            ),
            "отбить": (
                "repel, beat off",
                "Солдаты отбили атаку.",
                "The soldiers repelled the attack.",
            ),
            "элитный": (
                "elite, premium",
                "Это элитный клуб.",
                "This is an elite club.",
            ),
            "убогий": (
                "miserable, wretched",
                "Это убогий дом.",
                "This is a miserable house.",
            ),
            "поединок": (
                "duel, fight",
                "Они договорились о поединке на рассвете.",
                "They arranged a duel at dawn.",
            ),
            "запирать": (
                "to lock, to bolt",
                "Он каждый вечер запирает дверь.",
                "He locks the door every evening.",
            ),
            "очертание": (
                "outline, contour",
                "Я вижу очертания гор.",
                "I see the outline of the mountains.",
            ),
            "лопнуть": (
                "burst, pop",
                "Шарик внезапно лопнул.",
                "The balloon burst suddenly.",
            ),
            "скрипка": (
                "violin, fiddle",
                "Она прекрасно играла на скрипке.",
                "She played the violin beautifully.",
            ),
            "лирический": (
                "lyrical, lyric",
                "Это лирическое стихотворение.",
                "This is a lyrical poem.",
            ),
            "отрезок": (
                "segment, section",
                "Это короткий отрезок.",
                "This is a short segment.",
            ),
            "казино": (
                "casino, gambling house",
                "Он проиграл в казино.",
                "He lost at the casino.",
            ),
            "перемещаться": (
                "move around, move",
                "Нам трудно перемещаться по городу.",
                "It is hard to move around the city.",
            ),
        },
    )
)
