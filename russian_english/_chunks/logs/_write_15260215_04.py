#!/usr/bin/env python3
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from brainscape import answer_lemma_from_card, card_write_payload, cards_from_path, lemma_from_card
from russian_english._chunk_io import rewrite_chunk

FIXES = {
    "корточки": ("squat", "Он сел на корточки.", "He sat in a squat."),
    "укрытие": ("shelter", "Мы нашли укрытие.", "We found shelter."),
    "российско": ("Russian", "Это российско-американский проект.", "This is a Russian American project."),
    "составитель": ("compiler", "Он составитель словаря.", "He is a compiler of the dictionary."),
    "машинный": ("machine", "Это машинный перевод.", "This is a machine translation."),
    "робко": ("timidly", "Она робко сказала это.", "She timidly said this."),
    "наподобие": ("similar to", "Это наподобие дома.", "This is similar to a house."),
    "насчитывать": ("number", "Город насчитывает десять домов.", "The city numbers ten houses."),
    "величественный": ("majestic", "Это величественный дом.", "This is a majestic house."),
    "графиня": ("countess", "Графиня вошла в зал.", "The countess entered the hall."),
    "истец": ("plaintiff", "Истец уже здесь.", "The plaintiff is already here."),
    "холдинг": ("holding", "Это большой холдинг.", "This is a large holding."),
    "навязать": ("impose", "Они навязали это нам.", "They imposed this on us."),
    "заподозрить": ("suspect", "Я заподозрил его.", "I suspected him."),
    "пастернак": ("parsnip", "Я купил пастернак.", "I bought a parsnip."),
    "душить": ("strangle", "Не души меня.", "Don't strangle me."),
    "продержаться": ("hold out", "Мы должны продержаться.", "We must hold out."),
    "раскалить": ("make red-hot", "Раскали это железо.", "Make this iron red-hot."),
    "притворяться": ("pretend", "Не притворяйся больным.", "Don't pretend to be sick."),
    "колея": ("rut", "Машина застряла в колее.", "The car got stuck in a rut."),
    "предназначаться": ("be intended", "Это предназначается тебе.", "This is intended for you."),
    "кустарник": ("shrub", "В саду растёт кустарник.", "A shrub grows in the garden."),
    "служитель": ("servant", "Он служитель церкви.", "He is a servant of the church."),
    "врата": ("gates", "Врата уже открыты.", "The gates are already open."),
    "подскочить": ("jump", "Кот подскочил на кровать.", "The cat jumped on the bed."),
    "кондиционер": ("air conditioner", "Включи кондиционер.", "Turn on the air conditioner."),
    "прожектор": ("searchlight", "Прожектор горит.", "The searchlight burns."),
    "теперешний": ("current", "Это теперешний план.", "This is the current plan."),
    "восторженный": ("ecstatic", "Она была восторженной.", "She was ecstatic."),
    "духовность": ("spirituality", "Ему важна духовность.", "Spirituality is important to him."),
    "дозор": ("watch", "Ночной дозор вышел.", "The night watch went out."),
    "опережать": ("outstrip", "Она опережает нас.", "She outstrips us."),
    "восстать": ("rise", "Народ хочет восстать.", "The people want to rise."),
    "шорох": ("rustle", "Я слышу шорох.", "I hear a rustle."),
    "клей": ("glue", "Мне нужен клей.", "I need glue."),
    "прокат": ("rental", "Это наш прокат.", "This is our rental."),
    "раздеться": ("undress", "Надо раздеться.", "I need to undress."),
    "угостить": ("treat", "Угости меня чаем.", "Treat me to tea."),
    "стыдиться": ("be ashamed", "Не стыдись этого.", "Don't be ashamed of this."),
    "дерзкий": ("bold", "Это дерзкий ответ.", "This is a bold answer."),
    "ненавистный": ("hateful", "Это ненавистный человек.", "This is a hateful man."),
    "сенат": ("senate", "Сенат принял закон.", "The senate passed a law."),
    "красить": ("paint", "Я буду красить стену.", "I will paint the wall."),
    "указательный": ("index", "Это указательный палец.", "This is the index finger."),
    "поправлять": ("correct", "Не поправляй меня.", "Don't correct me."),
    "мелко": ("shallow", "Здесь слишком мелко.", "It is too shallow here."),
    "проблемный": ("problematic", "Это проблемный вопрос.", "This is a problematic question."),
    "достопримечательность": ("attraction", "Это главная достопримечательность.", "This is the main attraction."),
    "самочувствие": ("well-being", "У меня плохое самочувствие.", "My well-being is bad."),
    "негде": ("nowhere", "Мне негде сесть.", "I have nowhere to sit."),
    "кланяться": ("bow", "Не кланяйся ему.", "Don't bow to him."),
    "процветание": ("prosperity", "Я вижу процветание.", "I see prosperity."),
    "мишень": ("target", "Попади в мишень.", "Hit the target."),
    "салфетка": ("napkin", "Дай мне салфетку.", "Give me a napkin."),
    "родня": ("relatives", "Моя родня здесь.", "My relatives are here."),
    "экспансия": ("expansion", "Это их экспансия.", "This is their expansion."),
    "послушный": ("obedient", "Он послушный сын.", "He is an obedient son."),
    "ледник": ("glacier", "Это большой ледник.", "This is a large glacier."),
    "маркиз": ("marquis", "Маркиз вошёл в зал.", "The marquis entered the hall."),
    "розыск": ("search", "Полиция начала розыск.", "The police started a search."),
    "государственность": ("statehood", "Они получили государственность.", "They got statehood."),
    "таз": ("basin, pelvis", "Налей воду в таз.", "Pour water into the basin."),
    "скверный": ("nasty", "Это скверный день.", "This is a nasty day."),
    "похвалить": ("praise", "Я хочу похвалить тебя.", "I want to praise you."),
    "хулиган": ("hooligan", "Этот хулиган опять здесь.", "This hooligan is here again."),
    "накладывать": ("apply", "Не накладывай это.", "Don't apply this."),
    "тачка": ("wheelbarrow", "Я толкаю тачку.", "I push the wheelbarrow."),
    "рация": ("walkie-talkie", "Возьми рацию.", "Take the walkie-talkie."),
    "законность": ("legality", "Я сомневаюсь в законности.", "I doubt the legality."),
    "поспорить": ("argue", "Давай поспорим.", "Let's argue."),
    "примерный": ("exemplary", "Он примерный сын.", "He is an exemplary son."),
    "разъяснить": ("clarify", "Разъясни это мне.", "Clarify this for me."),
    "взвесить": ("weigh", "Взвесь это мясо.", "Weigh this meat."),
    "зов": ("call", "Я слышу зов.", "I hear a call."),
    "восход": ("sunrise", "Восход уже близко.", "Sunrise is already near."),
    "выручить": ("rescue", "Выручи меня.", "Rescue me."),
    "продвинуться": ("advance", "Нам надо продвинуться.", "We need to advance."),
    "процитировать": ("quote", "Процитируй его слова.", "Quote his words."),
    "оборонный": ("defense", "Это оборонный завод.", "This is a defense factory."),
    "обитание": ("habitat", "Это место обитания.", "This is their habitat."),
    "опухоль": ("tumor", "У него опухоль.", "He has a tumor."),
    "оговорка": ("slip, reservation", "Это была оговорка.", "That was a slip."),
    "пересмотр": ("revision", "Нужен пересмотр плана.", "The plan needs revision."),
    "стержень": ("rod", "Это железный стержень.", "This is an iron rod."),
    "герб": ("coat of arms", "Это наш герб.", "This is our coat of arms."),
    "вписываться": ("fit in", "Он не вписывается.", "He does not fit in."),
    "бинокль": ("binoculars", "Дай мне бинокль.", "Give me the binoculars."),
    "прославить": ("glorify", "Они хотят прославить его.", "They want to glorify him."),
    "выскакивать": ("jump out", "Он любит выскакивать.", "He loves to jump out."),
    "груша": ("pear", "Я съел грушу.", "I ate a pear."),
    "упорство": ("perseverance", "Ему нужно упорство.", "He needs perseverance."),
    "вырываться": ("break free", "Она всё время вырывается.", "She breaks free all the time."),
    "обеспокоить": ("disturb", "Это обеспокоило её.", "This disturbed her."),
    "инициатор": ("initiator", "Он инициатор этого.", "He is the initiator of this."),
    "целостный": ("holistic", "Это целостный подход.", "This is a holistic approach."),
    "учредить": ("establish", "Они хотят учредить фонд.", "They want to establish a fund."),
    "сдохнуть": ("die", "Собака скоро сдохнет.", "The dog will soon die."),
    "поговорка": ("saying", "Это старая поговорка.", "This is an old saying."),
    "отправление": ("departure", "Отправление поезда близко.", "The departure of the train is near."),
    "выхватить": ("snatch", "Он выхватил письмо.", "He snatched the letter."),
}

print(
    rewrite_chunk(
        Path("russian_english/_chunks/deck_15260215_04.csv"),
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
    "we", "must", "up",
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
    "уже", "еще", "ещё", "также", "тоже", "только", "вот", "ведь", "ну", "все",
    "как", "что", "чтобы", "когда", "если", "где", "чем", "кто", "тут",
    "там", "здесь", "давай", "нем", "нём", "ней", "них", "надо",
    "нее", "неё", "моя", "мое", "моё", "мои",
}

allow_en = {
    line.strip().lower()
    for line in (REPO / "russian_english/_vocab/allow_en_15260215.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_ru = {
    line.strip().replace("ё", "е").lower()
    for line in (REPO / "russian_english/_vocab/allow_ru_15260215.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_en |= FUNCTION_EN
allow_ru |= FUNCTION_RU

IRREGULAR_EN = {
    "came": "come", "gave": "give", "took": "take", "went": "go", "got": "get",
    "saw": "see", "was": "be", "were": "be", "been": "be", "had": "have",
    "did": "do", "said": "say", "made": "make", "left": "leave", "felt": "feel",
    "began": "begin", "became": "become", "bought": "buy", "caught": "catch",
    "kept": "keep", "lost": "lose", "fell": "fall", "falls": "fall",
    "grew": "grow", "held": "hold",
    "knew": "know", "ran": "run", "sat": "sit", "stood": "stand", "told": "tell",
    "thought": "think", "wrote": "write", "spoke": "speak", "broke": "break",
    "chose": "choose", "drove": "drive", "ate": "eat", "flew": "fly",
    "heard": "hear", "lay": "lie", "pulled": "pull", "passed": "pass",
    "started": "start", "opened": "open", "smiled": "smile", "entered": "enter",
    "looks": "look", "hurts": "hurt", "knows": "know", "sounds": "sound",
    "needs": "need", "loves": "love", "likes": "like",
    "confirmed": "confirm", "settled": "settle", "called": "call",
    "married": "marry", "embarrassed": "embarrass",
    "sugary": "sugar", "papers": "paper", "vegetables": "vegetable",
    "eyes": "eye", "fishes": "fish",
    "stuck": "stick", "lit": "light", "grows": "grow",
    "imposed": "impose", "suspected": "suspect", "intended": "intend",
    "jumped": "jump", "outstrips": "outstrip", "numbers": "number",
    "houses": "house", "gates": "gate", "relatives": "relative",
    "applies": "apply", "breaks": "break", "disturbed": "disturb",
    "snatched": "snatch", "said": "say",
}
IRREGULAR_RU = {
    "идет": "идти", "иду": "идти", "шел": "идти", "шла": "идти", "шли": "идти",
    "нужна": "нужный", "нужен": "нужный", "нужно": "нужный",
    "болит": "болеть", "лежит": "лежать", "слышит": "слышать", "слышу": "слышать",
    "слышал": "слышать", "вижу": "видеть", "видит": "видеть",
    "купи": "купить", "купил": "купить", "сделай": "сделать", "сделал": "сделать",
    "открой": "открыть", "открыл": "открыть",
    "написал": "написать", "получил": "получить", "получили": "получить",
    "принял": "принять",
    "звучит": "звучать", "может": "мочь", "смог": "смочь",
    "ушел": "уйти", "ушёл": "уйти", "вошла": "войти", "вошли": "войти",
    "вошел": "войти", "вошёл": "войти",
    "любит": "любить", "люблю": "любить", "хотят": "хотеть", "хочет": "хотеть",
    "хочу": "хотеть",
    "знает": "знать", "начал": "начать", "начала": "начать",
    "началась": "начаться", "началось": "начаться",
    "выглядит": "выглядеть", "выглядел": "выглядеть",
    "улыбнулась": "улыбнуться", "нравится": "нравиться",
    "сел": "сесть", "села": "сесть", "нашли": "найти",
    "насчитывает": "насчитывать", "навязали": "навязать",
    "заподозрил": "заподозрить", "души": "душить",
    "должны": "должный", "больным": "больной",
    "застряла": "застрять", "застрял": "застрять",
    "предназначается": "предназначаться",
    "растёт": "расти", "растет": "расти",
    "церкви": "церковь", "открыты": "открытый",
    "подскочил": "подскочить", "включи": "включить",
    "горит": "гореть", "важна": "важный", "вышел": "выйти",
    "опережает": "опережать", "угощу": "угостить", "угости": "угостить", "чаем": "чай",
    "стыдись": "стыдиться", "стену": "стена",
    "поправляй": "поправлять", "главная": "главный",
    "попади": "попасть", "дай": "дать",
    "налей": "налить", "воду": "вода",
    "накладывает": "накладывать", "накладывай": "накладывать", "краску": "краска",
    "толкаю": "толкать", "возьми": "взять",
    "сомневаюсь": "сомневаться", "поспорим": "поспорить",
    "разъясни": "разъяснить", "взвесь": "взвесить",
    "выручи": "выручить", "процитируй": "процитировать",
    "обеспокоило": "обеспокоить", "съел": "съесть",
    "грушу": "груша", "вырывается": "вырываться",
    "сдохнет": "сдохнуть", "старая": "старый",
    "поезда": "поезд", "выхватил": "выхватить",
    "кланяйся": "кланяться", "притворяйся": "притворяться",
    "раскали": "раскалить", "вписывается": "вписываться",
    "сказала": "сказать", "восторженной": "восторженный",
    "большои": "большой", "большой": "большой",
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


dest = REPO / "russian_english/_chunks/fixed/deck_15260215_04.csv"
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
