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
    "вариация": ("variation", "Это моя вариация.", "This is my variation."),
    "футболка": ("T-shirt", "Купи новую футболку.", "Buy a new T-shirt."),
    "рубка": ("cutting, chopping", "Рубка уже началась.", "The cutting has already started."),
    "противно": ("disgusting", "Мне противно это слышать.", "This is disgusting to hear."),
    "девичий": ("maiden, girlish", "Это её девичья фамилия.", "This is her maiden name."),
    "мусорный": ("garbage, trash", "Это мусорное ведро.", "This is a garbage bucket."),
    "пророчество": ("prophecy", "Это старое пророчество.", "This is an old prophecy."),
    "разрушительный": ("destructive", "Это разрушительный удар.", "This is a destructive blow."),
    "усмотрение": ("discretion", "Это на ваше усмотрение.", "This is at your discretion."),
    "колокольчик": ("bell", "Я слышу колокольчик.", "I hear a bell."),
    "доставаться": ("to get, to fall to", "Мне всегда достаётся это.", "I always get this."),
    "пьяница": ("drunkard", "Пьяница уже дома.", "The drunkard is already home."),
    "гибкость": ("flexibility", "Ей нужна гибкость.", "She needs flexibility."),
    "упрекать": ("to reproach", "Не упрекай меня.", "Don't reproach me."),
    "оформлять": ("to formalize", "Надо оформлять бумаги.", "We need to formalize the papers."),
    "ступить": ("step, set foot", "Не ступи сюда.", "Don't step here."),
    "пивной": ("beer", "Это пивной бар.", "This is a beer bar."),
    "подтверждаться": ("to be confirmed", "Новость ещё подтверждается.", "The news is still being confirmed."),
    "грешный": ("sinful", "Я человек грешный.", "I am a sinful man."),
    "тусовка": ("party", "Тусовка уже началась.", "The party has already started."),
    "терзать": ("torment", "Это будет терзать его.", "This will torment him."),
    "завещание": ("will, testament", "Он написал завещание.", "He wrote a will."),
    "любезно": ("kindly", "Он любезно открыл дверь.", "He kindly opened the door."),
    "ухудшение": ("deterioration", "Я вижу ухудшение.", "I see a deterioration."),
    "увидать": ("to see", "Я увидал его там.", "I did see him there."),
    "аквариум": ("aquarium", "В аквариуме есть рыбы.", "There are fish in the aquarium."),
    "продовольственный": ("food, grocery", "Это продовольственный магазин.", "This is a food store."),
    "сустав": ("joint", "Этот сустав болит.", "This joint hurts."),
    "теоретик": ("theorist", "Он известный теоретик.", "He is a famous theorist."),
    "двухэтажный": ("two-story", "Это двухэтажный дом.", "This is a two-story house."),
    "траектория": ("trajectory", "Траектория была верной.", "The trajectory was right."),
    "двойка": ("two", "Он получил двойку.", "He got a two."),
    "посвящать": ("dedicate, devote", "Я посвящаю это тебе.", "I dedicate this to you."),
    "боярин": ("boyar", "Это старый боярин.", "This is an old boyar."),
    "героин": ("heroin", "Это опасный героин.", "This is dangerous heroin."),
    "пусто": ("empty", "В комнате пусто.", "The room is empty."),
    "наутро": ("in the morning", "Он ушёл наутро.", "He left in the morning."),
    "установиться": ("settle", "Погода уже установилась.", "The weather has already settled."),
    "именоваться": ("to be called", "Как это именуется?", "What is this called?"),
    "проповедовать": ("preach", "Он любит проповедовать.", "He loves to preach."),
    "скрипеть": ("to creak", "Дверь начала скрипеть.", "The door began to creak."),
    "тупо": ("stupid", "Это звучит тупо.", "This sounds stupid."),
    "виновник": ("culprit", "Виновник уже здесь.", "The culprit is already here."),
    "скатерть": ("tablecloth", "Скатерть лежит на столе.", "The tablecloth is on the table."),
    "испуганный": ("frightened, scared", "Он выглядит испуганным.", "He looks frightened."),
    "намеренно": ("intentionally", "Он сделал это намеренно.", "He did this intentionally."),
    "пожениться": ("to get married", "Они хотят пожениться.", "They want to get married."),
    "сахарный": ("sugar, sugary", "Чай слишком сахарный.", "The tea is too sugary."),
    "психотерапевт": ("psychotherapist", "Я иду к психотерапевту.", "I am going to the psychotherapist."),
    "декорация": ("decoration, set", "Декорация уже готова.", "The decoration is already ready."),
    "бриллиант": ("diamond", "Это настоящий бриллиант.", "This is a real diamond."),
    "вещание": ("broadcasting", "Вещание уже началось.", "The broadcasting has already started."),
    "открытость": ("openness", "Мне нравится её открытость.", "I like her openness."),
    "эвакуация": ("evacuation", "Эвакуация уже началась.", "The evacuation has already started."),
    "насущный": ("pressing, urgent", "Это насущный вопрос.", "This is a pressing question."),
    "запястье": ("wrist", "Часы на запястье.", "The watch is on the wrist."),
    "законодатель": ("legislator", "Законодатель принял закон.", "The legislator passed a law."),
    "бюрократический": ("bureaucratic", "Это бюрократический процесс.", "This is a bureaucratic process."),
    "обозрение": ("review, survey", "Я читаю обозрение.", "I am reading a review."),
    "неуверенно": ("uncertainly", "Она неуверенно улыбнулась.", "She smiled uncertainly."),
    "княгиня": ("princess", "Княгиня вошла в зал.", "The princess entered the hall."),
    "придурок": ("idiot, fool", "Он полный придурок.", "He is a complete idiot."),
    "отстоять": ("defend", "Мы должны отстоять это.", "We must defend this."),
    "джунгли": ("jungle", "Мы вошли в джунгли.", "We entered the jungle."),
    "выращивать": ("to grow", "Они выращивают овощи.", "They grow vegetables."),
    "скинуть": ("throw off, send", "Скинь это пальто.", "Throw off this coat."),
    "задерживать": ("to delay", "Не задерживай меня.", "Don't delay me."),
    "раскрываться": ("to open up", "Цветок начал раскрываться.", "The flower began to open up."),
    "грош": ("penny", "Это не стоит гроша.", "This is not worth a penny."),
    "мясной": ("meat, meaty", "Это мясной суп.", "This is a meat soup."),
    "покорить": ("conquer", "Они хотят покорить гору.", "They want to conquer the mountain."),
    "кинематограф": ("cinema", "Я люблю кинематограф.", "I love cinema."),
    "загрузить": ("upload, load", "Загрузи этот файл.", "Upload this file."),
    "превзойти": ("outdo, surpass", "Он смог превзойти их.", "He managed to outdo them."),
    "спираль": ("spiral", "Это старая спираль.", "This is an old spiral."),
    "выплачивать": ("to pay", "Он будет выплачивать долг.", "He will pay the debt."),
    "обитель": ("abode", "Это тихая обитель.", "This is a quiet abode."),
    "мгновенный": ("instant", "Ответ был мгновенным.", "The answer was instant."),
    "втянуть": ("to pull in, to involve", "Он втянул меня.", "He pulled me in."),
    "убираться": ("to clean up", "Мне нужно убираться.", "I need to clean up."),
    "наизусть": ("by heart", "Она знает это наизусть.", "She knows this by heart."),
    "выразительный": ("expressive", "У неё выразительные глаза.", "She has expressive eyes."),
    "смутиться": ("to be embarrassed", "Он сразу смутился.", "He was immediately embarrassed."),
    "учредитель": ("founder", "Он учредитель этой фирмы.", "He is the founder of this firm."),
    "неспособность": ("inability", "Это его неспособность.", "This is his inability."),
    "улечься": ("lie down", "Надо улечься.", "I need to lie down."),
    "нобелевский": ("Nobel", "Это Нобелевская премия.", "This is a Nobel prize."),
    "быстренько": ("quickly", "Сделай это быстренько.", "Do this quickly."),
    "скрип": ("creak, squeak", "Я слышал скрип.", "I heard a creak."),
    "выпивка": ("drink, alcohol", "Купи выпивку.", "Buy some drink."),
    "развиться": ("develop", "Это может развиться.", "This can develop."),
    "затеять": ("start", "Он затеял ссору.", "He started a fight."),
    "штык": ("bayonet", "Штык был острый.", "The bayonet was sharp."),
    "приезжий": ("newcomer, visitor", "Приезжий уже здесь.", "The newcomer is already here."),
    "як": ("yak", "Як стоит на горе.", "The yak is standing on the mountain."),
    "производительный": ("productive", "Это был производительный день.", "This was a productive day."),
    "записной": ("notebook", "Это записная книжка.", "This is a notebook."),
    "шторм": ("storm", "Шторм уже близко.", "The storm is already close."),
    "навязчивый": ("obtrusive, intrusive", "Он слишком навязчивый.", "He is too obtrusive."),
    "скопление": ("accumulation, cluster", "Тут большое скопление.", "There is a large accumulation here."),
}

print(
    rewrite_chunk(
        Path("russian_english/_chunks/deck_15260215_03.csv"),
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
    "we", "must",
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
}
IRREGULAR_RU = {
    "идет": "идти", "иду": "идти", "шел": "идти", "шла": "идти", "шли": "идти",
    "нужна": "нужный", "нужен": "нужный", "нужно": "нужный",
    "болит": "болеть", "лежит": "лежать", "слышит": "слышать", "слышу": "слышать",
    "слышал": "слышать", "вижу": "видеть", "видит": "видеть",
    "купи": "купить", "сделай": "сделать", "сделал": "сделать",
    "открой": "открыть", "открыл": "открыть",
    "написал": "написать", "получил": "получить", "принял": "принять",
    "звучит": "звучать", "может": "мочь", "смог": "смочь",
    "подтверждается": "подтверждаться",
    "ушел": "уйти", "ушёл": "уйти", "вошла": "войти", "вошли": "войти",
    "вошел": "войти", "вошёл": "войти",
    "любит": "любить", "люблю": "любить", "хотят": "хотеть",
    "знает": "знать", "начал": "начать", "начала": "начать",
    "началась": "начаться", "началось": "начаться",
    "выглядит": "выглядеть", "выглядел": "выглядеть",
    "улыбнулась": "улыбнуться", "нравится": "нравиться",
    "достается": "доставаться", "достаётся": "доставаться",
    "упрекай": "упрекать", "ступи": "ступить",
    "увидал": "увидать", "посвящаю": "посвящать",
    "установилась": "установиться", "именуется": "именоваться",
    "задерживай": "задерживать", "скинь": "скинуть",
    "загрузи": "загрузить", "втянул": "втянуть",
    "улегся": "улечься", "улёгся": "улечься",
    "смутился": "смутиться", "затеял": "затеять",
    "выращивают": "выращивать",
    "готова": "готовый", "верной": "верный",
    "девичья": "девичий", "мусорное": "мусорный",
    "сахарный": "сахарный", "мясной": "мясной",
    "записная": "записной", "нобелевская": "нобелевский",
    "двухэтажный": "двухэтажный", "мгновенным": "мгновенный",
    "испуганным": "испуганный", "выразительные": "выразительный",
    "футболку": "футболка", "двойку": "двойка",
    "выпивку": "выпивка", "гроша": "грош",
    "психотерапевту": "психотерапевт",
    "бумаги": "бумага", "рыбы": "рыба",
    "овощи": "овощ", "гору": "гора",
    "глаза": "глаз", "фирмы": "фирма",
    "этой": "этот", "этого": "этот",
    "новые": "новый", "новую": "новый",
    "старое": "старый", "старая": "старый",
    "большое": "большой", "тихая": "тихий",
    "известный": "известный", "опасный": "опасный",
    "настоящий": "настоящий", "полный": "полный",
    "острый": "острый",
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


dest = REPO / "russian_english/_chunks/fixed/deck_15260215_03.csv"
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
