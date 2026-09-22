import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from brainscape import answer_lemma_from_card, card_write_payload, cards_from_path, lemma_from_card
from russian_english._chunk_io import rewrite_chunk

FIXES = {
    "затянуть": ("tighten", "Затяни ремень.", "Tighten the belt."),
    "занавес": ("curtain", "Занавес упал.", "The curtain fell."),
    "переть": ("to carry", "Тяжело переть мешок.", "It is hard to carry the sack."),
    "прочтение": ("reading", "Это новое прочтение.", "This is a new reading."),
    "эмиграция": ("emigration", "Эмиграция была трудной.", "Emigration was hard."),
    "сформироваться": ("to form", "Характер сформировался.", "The character has formed."),
    "таять": ("to melt", "Снег начал таять.", "The snow began to melt."),
    "гибнуть": ("to perish", "Они гибнут там.", "They perish there."),
    "психиатр": ("psychiatrist", "Я иду к психиатру.", "I am going to the psychiatrist."),
    "хит": ("hit", "Это хит.", "This is a hit."),
    "высказываться": ("to speak out", "Он высказывается.", "He is speaking out."),
    "передвигаться": ("to move", "Он плохо передвигается.", "He moves poorly."),
    "индивидуальность": ("individuality", "У неё есть индивидуальность.", "She has individuality."),
    "вцепиться": ("to cling", "Он вцепился в меня.", "He will cling to me."),
    "тюремный": ("prison", "Это тюремный двор.", "This is a prison yard."),
    "вылетать": ("to fly out", "Мы вылетаем утром.", "We fly out in the morning."),
    "укол": ("shot", "Мне сделали укол.", "They gave me a shot."),
    "стаж": ("experience", "У него большой стаж.", "He has a lot of experience."),
    "привилегия": ("privilege", "Это не привилегия.", "This is not a privilege."),
    "фондовый": ("stock", "Это фондовый рынок.", "This is the stock market."),
    "струна": ("string", "Вот струна.", "Here is the string."),
    "наливать": ("to pour", "Он наливает чай.", "He is pouring tea."),
    "нахмуриться": ("to frown", "Он нахмурился.", "He frowned."),
    "вешать": ("to hang", "Он вешает пальто.", "He is hanging the coat."),
    "коалиция": ("coalition", "Это коалиция.", "This is a coalition."),
    "раздавать": ("to give out", "Она раздаёт книги.", "She gives out books."),
    "колдун": ("wizard", "Колдун здесь.", "The wizard is here."),
    "погоня": ("chase", "Началась погоня.", "The chase started."),
    "проноситься": ("to rush by", "Поезд проносится мимо.", "The train rushes by."),
    "кубик": ("cube", "Дай мне кубик.", "Give me the cube."),
    "мех": ("fur", "Это мех.", "This is fur."),
    "физиологический": ("physiological", "Это физиологический процесс.", "This is a physiological process."),
    "тревожить": ("to disturb", "Не тревожь его.", "Don't disturb him."),
    "грипп": ("flu", "У меня грипп.", "I have the flu."),
    "уплата": ("payment", "Уплата завтра.", "The payment is tomorrow."),
    "профессионально": ("professionally", "Он работает профессионально.", "He works professionally."),
    "погладить": ("to stroke", "Она погладила кота.", "She stroked the cat."),
    "рассыпаться": ("to scatter", "Сахар рассыпался.", "The sugar scattered."),
    "перебирать": ("to go through", "Я перебираю книги.", "I am going through the books."),
    "лыжа": ("ski", "Где моя лыжа?", "Where is my ski?"),
    "автоматизация": ("automation", "Нужна автоматизация.", "Automation is needed."),
    "пополам": ("in half", "Дели хлеб пополам.", "Divide the bread in half."),
    "бетонный": ("concrete", "Это бетонный стол.", "This is a concrete table."),
    "прицел": ("sight", "Проверь прицел.", "Check the sight."),
    "лиса": ("fox", "Лиса в лесу.", "The fox is in the forest."),
    "маяк": ("lighthouse", "Я вижу маяк.", "I see the lighthouse."),
    "влиятельный": ("influential", "Он влиятельный человек.", "He is an influential person."),
    "избить": ("to beat", "Его избили.", "They beat him."),
    "правильность": ("correctness", "Проверь правильность.", "Check the correctness."),
    "механика": ("mechanics", "Я изучаю механику.", "I study mechanics."),
    "вихрь": ("whirlwind", "Вихрь здесь.", "The whirlwind is here."),
    "обучаться": ("to study", "Он обучается здесь.", "He is studying here."),
    "антенна": ("antenna", "Это антенна.", "This is an antenna."),
    "публично": ("publicly", "Он публично сказал это.", "He said this publicly."),
    "погибать": ("to perish", "Они погибают там.", "They perish there."),
    "курорт": ("resort", "Мы едем на курорт.", "We are going to the resort."),
    "разочаровать": ("to disappoint", "Ты меня разочаровал.", "You disappointed me."),
    "замкнутый": ("introverted", "Он очень замкнутый.", "He is very introverted."),
    "предшественник": ("predecessor", "Это мой предшественник.", "This is my predecessor."),
    "осторожность": ("caution", "Нужна осторожность.", "Caution is needed."),
    "плач": ("crying", "Я слышу плач.", "I hear crying."),
    "направленность": ("direction", "Какая направленность?", "What is the direction?"),
    "схожий": ("similar", "Они очень схожи.", "They are very similar."),
    "племянник": ("nephew", "Это мой племянник.", "This is my nephew."),
    "попрощаться": ("to say goodbye", "Пора попрощаться.", "Time to say goodbye."),
    "оборудовать": ("to equip", "Мы оборудовали комнату.", "We equipped the room."),
    "стенд": ("stand", "Где стенд?", "Where is the stand?"),
    "приспособить": ("to adapt", "Мы приспособили стол.", "We adapted the table."),
    "погубить": ("to destroy", "Это погубит его.", "This will destroy him."),
    "хитрость": ("cunning", "Это его хитрость.", "This is his cunning."),
    "отрываться": ("to break away", "Он отрывается от нас.", "He is breaking away from us."),
    "приветствие": ("greeting", "Это приветствие.", "This is a greeting."),
    "пропуск": ("pass", "Где твой пропуск?", "Where is your pass?"),
    "управляемый": ("controlled", "Это управляемый процесс.", "This is a controlled process."),
    "ощущаться": ("to be felt", "Холод может ощущаться.", "The cold can be felt."),
    "родовой": ("ancestral", "Это родовой дом.", "This is the ancestral home."),
    "воспитатель": ("caregiver", "Она воспитатель.", "She is a caregiver."),
    "осложнение": ("complication", "Есть осложнение.", "There is a complication."),
    "уронить": ("to drop", "Я уронил ключ.", "I dropped the key."),
    "рубить": ("to chop", "Он рубит дерево.", "He is chopping the tree."),
    "инцидент": ("incident", "Это был инцидент.", "This was an incident."),
    "издеваться": ("to mock", "Не издевайся.", "Don't mock."),
    "желанный": ("desired", "Это желанный подарок.", "This is the desired gift."),
    "презирать": ("to despise", "Я презираю ложь.", "I despise lies."),
    "частичный": ("partial", "Это частичный ответ.", "This is a partial answer."),
    "игла": ("needle", "Где игла?", "Where is the needle?"),
    "хронический": ("chronic", "У него хроническая боль.", "He has chronic pain."),
    "приготовиться": ("to get ready", "Пора приготовиться.", "Time to get ready."),
    "аллея": ("alley", "Мы идём по аллее.", "We are walking down the alley."),
    "сливаться": ("to merge", "Река сливается.", "The river merges."),
    "пылать": ("to blaze", "Огонь пылает.", "The fire blazes."),
    "вплотную": ("up close", "Подойди вплотную.", "Come up close."),
    "индикатор": ("indicator", "Смотри на индикатор.", "Look at the indicator."),
    "извинение": ("apology", "Это извинение.", "This is an apology."),
    "алмаз": ("diamond", "Это алмаз.", "This is a diamond."),
    "близ": ("near", "Дом близ парка.", "The house is near the park."),
    "побег": ("escape", "Это побег.", "This is an escape."),
    "молоток": ("hammer", "Где молоток?", "Where is the hammer?"),
    "поверхностный": ("superficial", "Это поверхностный взгляд.", "This is a superficial view."),
    "утонуть": ("to drown", "Он может утонуть.", "He can drown."),
}

print(
    rewrite_chunk(
        Path("russian_english/_chunks/deck_15260210_03.csv"),
        FIXES,
    )
)

FUNCTION_EN = {
    "a", "an", "the", "is", "be", "i", "you", "he", "she", "it", "we", "they",
    "my", "and", "or", "in", "on", "at", "to", "of", "for", "with", "from",
    "not", "his", "him", "her", "their", "them", "our", "us", "me", "am",
    "are", "was", "were", "been", "being", "this", "that", "these", "those",
    "as", "by", "into", "about", "than", "then", "so", "if", "but", "its",
    "your", "do", "does", "did", "will", "would", "can", "could", "may",
    "there", "here", "has", "had", "have", "don't", "dont", "let's", "lets",
    "all", "off", "done", "myself", "yourself", "himself", "herself",
    "itself", "ourselves", "themselves", "one's", "ones", "it's", "s",
    "down", "up", "out", "what", "where", "when", "who", "why", "how",
    "very", "too", "now", "yes", "no", "some", "any", "more", "most",
}

FUNCTION_RU = {
    "и", "а", "или", "не", "ни", "но", "да", "же", "ли", "бы", "то", "это",
    "этот", "эта", "эти", "этой", "этом", "эту", "этих", "этим", "этими",
    "этого", "этому", "я", "ты", "он", "она", "оно", "мы", "вы", "они",
    "мой", "моя", "мое", "мои", "его", "ее", "их", "ему", "ей", "им",
    "меня", "мне", "тебя", "тебе", "нас", "нам", "вас", "вам", "себя",
    "себе", "свой", "своя", "свое", "свои", "свою", "своей", "своего",
    "в", "во", "на", "с", "со", "к", "ко", "у", "о", "об", "от", "до",
    "из", "за", "по", "под", "над", "при", "для", "без", "между", "через",
    "был", "была", "было", "были", "будет", "будут", "буду", "есть", "быть",
    "уже", "еще", "также", "тоже", "только", "вот", "ведь", "ну", "все",
    "как", "что", "чтобы", "когда", "если", "где", "чем", "кто", "тут",
    "там", "здесь", "давай", "нем", "нём", "ней", "них", "ним", "какая", "какой",
    "нее", "неё", "ею",
}

allow_en = {
    line.strip().lower()
    for line in (REPO / "russian_english/_vocab/allow_en_15260210.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_ru = {
    line.strip().replace("ё", "е").lower()
    for line in (REPO / "russian_english/_vocab/allow_ru_15260210.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_en |= FUNCTION_EN
allow_ru |= FUNCTION_RU

IRREGULAR_EN = {
    "came": "come", "gave": "give", "gives": "give", "took": "take", "went": "go",
    "got": "get", "saw": "see", "was": "be", "were": "be", "been": "be",
    "had": "have", "did": "do", "said": "say", "made": "make", "left": "leave",
    "felt": "feel", "began": "begin", "became": "become", "fell": "fall",
    "clung": "cling", "frowned": "frown", "stroked": "stroke", "scattered": "scatter",
    "started": "start", "needed": "need", "equipped": "equip", "adapted": "adapt",
    "dropped": "drop", "disappointed": "disappoint", "formed": "form",
    "melting": "melt", "speaking": "speak", "hanging": "hang", "pouring": "pour",
    "rushing": "rush", "rushes": "rush", "studying": "study", "chopping": "chop",
    "breaking": "break", "walking": "walk", "blazing": "blaze", "going": "go",
    "moves": "move", "works": "work", "gives": "give", "look": "look",
}

IRREGULAR_RU = {
    "идет": "идти", "иду": "идти", "идем": "идти", "идём": "идти",
    "шел": "идти", "шёл": "идти", "шла": "идти", "шли": "идти",
    "нужна": "нужный", "нужен": "нужный", "нужно": "нужный",
    "вижу": "видеть", "видишь": "видеть", "видит": "видеть",
    "дай": "дать", "дайте": "дать",
    "едем": "ехать", "едет": "ехать",
    "слышу": "слышать", "слышит": "слышать",
    "проверь": "проверить",
    "дели": "делить", "делим": "делить",
    "сказал": "сказать", "сказала": "сказать",
    "смотри": "смотреть",
    "работает": "работать",
    "упал": "упасть", "упала": "упасть",
    "начал": "начать", "начала": "начать", "началась": "начаться",
    "сделали": "сделать", "сделал": "сделать",
    "люблю": "любить",
    "может": "мочь", "могу": "мочь", "можем": "мочь",
    "подойди": "подойти",
    "сформировался": "сформироваться",
    "высказывается": "высказываться",
    "вцепился": "вцепиться",
    "наливает": "наливать",
    "нахмурился": "нахмуриться",
    "вешает": "вешать",
    "раздает": "раздавать", "раздаёт": "раздавать",
    "проносится": "проноситься",
    "погладила": "погладить",
    "рассыпался": "рассыпаться",
    "избили": "избить",
    "обучается": "обучаться",
    "погибают": "погибать",
    "разочаровал": "разочаровать",
    "оборудовали": "оборудовать",
    "приспособили": "приспособить",
    "отрывается": "отрываться",
    "уронил": "уронить",
    "издевайся": "издеваться",
    "сливается": "сливаться",
    "пылает": "пылать",
}

RU_ENDINGS = (
    "ами", "ями", "ого", "его", "ому", "ему", "ыми", "ими", "ой", "ей", "ом",
    "ем", "ах", "ях", "ам", "ям", "ов", "ев", "ую", "юю", "ая", "яя", "ое",
    "ее", "ые", "ие", "ый", "ий", "а", "я", "у", "ю", "е", "и", "ы", "о", "ь",
)


def _en_ok(word: str) -> bool:
    w = word.lower()
    if w in allow_en:
        return True
    if IRREGULAR_EN.get(w) in allow_en:
        return True
    if w.endswith("'s") and w[:-2] in allow_en:
        return True
    for suf in ("'s", "s", "es", "ed", "ing", "ly", "er", "est"):
        if w.endswith(suf) and w[: -len(suf)] in allow_en:
            return True
        if w.endswith(suf) and w[: -len(suf)] + "e" in allow_en:
            return True
    if w.endswith("ies") and (w[:-3] + "y") in allow_en:
        return True
    if w.endswith("ied") and (w[:-3] + "y") in allow_en:
        return True
    return False


def _ru_ok(word: str) -> bool:
    w = word.replace("ё", "е").lower()
    if w in allow_ru:
        return True
    if IRREGULAR_RU.get(w) in allow_ru:
        return True
    stems = {w}
    for suf in RU_ENDINGS:
        if w.endswith(suf) and len(w) - len(suf) >= 3:
            stems.add(w[: -len(suf)])
    for stem in stems:
        if stem in allow_ru:
            return True
        if any(a.startswith(stem) or stem.startswith(a) for a in allow_ru if len(a) >= 4 and len(stem) >= 4):
            return True
    return False


def _tokens(text: str) -> list[str]:
    return re.findall(r"[A-Za-zА-Яа-яЁё'-]+", text)


dest = REPO / "russian_english/_chunks/fixed/deck_15260210_03.csv"
cards = cards_from_path(dest)
leftover = []
for i, card in enumerate(cards, 1):
    lemma = lemma_from_card(card)
    gloss = answer_lemma_from_card(card)
    payload = card_write_payload(card)
    ru = payload["question"].split("## Footnote")[-1].strip()
    en = payload["answer"].split("## Footnote")[-1].strip()
    ru_l = ru.replace("ё", "е").lower()
    stem = lemma.replace("ё", "е").lower()[:4]
    if stem and stem not in ru_l and lemma.replace("ё", "е").lower() not in ru_l:
        leftover.append(f"{i} LEMMA {lemma} :: {ru}")
    gloss_l = re.sub(r"^(to |the |a |an )", "", gloss.split(",")[0].strip().lower())
    gloss_tok = gloss_l.split()[0] if gloss_l else ""
    if gloss_tok and gloss_tok not in en.lower() and not any(
        g in en.lower() for g in gloss_l.split()
    ):
        leftover.append(f"{i} GLOSS {gloss} :: {en}")
    extra_en = set()
    extra_ru = {lemma.replace("ё", "е").lower()}
    for part in re.split(r"[,;/]| or | and ", gloss):
        part = re.sub(r"^(to |the |a |an )", "", part.strip().lower())
        extra_en.update(part.split())
    allow_en.update(extra_en)
    allow_ru.update(extra_ru)
    for tok in _tokens(en):
        if not _en_ok(tok):
            leftover.append(f"{i} EN {tok} :: {en}")
    for tok in _tokens(ru):
        if not _ru_ok(tok):
            leftover.append(f"{i} RU {tok} :: {ru}")

print(f"leftovers={len(leftover)}")
if leftover:
    print("\n".join(leftover))
