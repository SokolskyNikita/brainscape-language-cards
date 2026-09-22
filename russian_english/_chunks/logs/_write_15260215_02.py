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
    "коммерсант": ("businessman, merchant", "Коммерсант пришёл рано.", "The businessman came early."),
    "папаша": ("dad, daddy", "Папаша уже дома.", "Dad is already home."),
    "офисный": ("office", "Это офисный работник.", "This is an office worker."),
    "инерция": ("inertia", "Инерция ещё сильна.", "The inertia is still strong."),
    "очистка": ("cleaning", "Нужна очистка дома.", "The house needs cleaning."),
    "дежурство": ("duty, watch", "Сегодня моё дежурство.", "Today is my duty."),
    "солидарность": ("solidarity", "Я выражаю солидарность.", "I express solidarity."),
    "растерянно": ("confusedly", "Он растерянно смотрел на нас.", "He looked at us confusedly."),
    "равнодушие": ("indifference", "Его равнодушие меня ранит.", "His indifference hurts me."),
    "сухопутный": ("land, terrestrial", "Это сухопутная армия.", "This is a land army."),
    "экономически": ("economically", "Это экономически важно.", "This is economically important."),
    "дисплей": ("display, screen", "Дисплей не работает.", "The display does not work."),
    "кредитование": ("lending", "Это банковское кредитование.", "This is bank lending."),
    "созреть": ("to ripen, to mature", "Яблоки уже созрели.", "The apples have already ripened."),
    "пласт": ("layer", "Сними этот пласт.", "Take this layer off."),
    "упускать": ("miss, let slip", "Не упускай шанс.", "Don't miss the chance."),
    "лимон": ("lemon", "Лимон лежит на столе.", "The lemon is on the table."),
    "шишка": ("cone, bump", "Сосна уронила шишку.", "A cone fell from the pine."),
    "дико": ("wildly", "Он дико смеялся.", "He laughed wildly."),
    "краснеть": ("to blush, to turn red", "Она начала краснеть.", "She began to blush."),
    "порой": ("sometimes", "Порой он молчит.", "Sometimes he is silent."),
    "сословие": ("social class", "Это старое сословие.", "This is an old social class."),
    "смутно": ("vaguely", "Я смутно помню это.", "I vaguely remember this."),
    "изоляция": ("isolation", "Ему нужна изоляция.", "He needs isolation."),
    "раствориться": ("dissolve", "Сахар растворится быстро.", "The sugar will dissolve quickly."),
    "аппаратный": ("hardware", "Это аппаратный сбой.", "This is a hardware failure."),
    "влагалище": ("vagina", "Боль во влагалище.", "There is pain in the vagina."),
    "ржавый": ("rusty", "Этот нож ржавый.", "This knife is rusty."),
    "датчик": ("sensor", "Датчик не работает.", "The sensor does not work."),
    "иуда": ("Judas", "Он настоящий иуда.", "He is a real Judas."),
    "неторопливо": ("leisurely", "Он неторопливо шёл домой.", "He walked home leisurely."),
    "многообразие": ("diversity, variety", "Мне нравится это многообразие.", "I like this diversity."),
    "тополь": ("poplar", "Тополь растёт у дома.", "The poplar grows by the house."),
    "повязка": ("bandage", "Сними повязку.", "Take the bandage off."),
    "разбирательство": ("inquiry, investigation", "Разбирательство ещё идёт.", "The inquiry is still going."),
    "одобрять": ("approve", "Я одобряю решение.", "I approve the decision."),
    "первобытный": ("primitive", "Это первобытный страх.", "This is a primitive fear."),
    "вступительный": ("entrance, introductory", "Это вступительный экзамен.", "This is an entrance exam."),
    "карманный": ("pocket", "Это карманный словарь.", "This is a pocket dictionary."),
    "санаторий": ("sanatorium", "Она в санатории.", "She is in the sanatorium."),
    "переписать": ("rewrite", "Перепиши это письмо.", "Rewrite this letter."),
    "умудриться": ("manage", "Она умудрилась уйти.", "She managed to leave."),
    "свершиться": ("to come true", "Мечта свершилась.", "The dream came true."),
    "псевдоним": ("pseudonym", "Она пишет под псевдонимом.", "She writes under a pseudonym."),
    "комендант": ("commandant", "Комендант отдал приказ.", "The commandant gave an order."),
    "сувенир": ("souvenir", "Сувенир лежит на столе.", "The souvenir is on the table."),
    "внушительный": ("impressive", "Это внушительный дом.", "This is an impressive house."),
    "старенький": ("old", "Это старенький дом.", "This is an old house."),
    "поди": ("probably", "Поди, он уже дома.", "He is probably already home."),
    "мэрия": ("city hall", "Я иду в мэрию.", "I am going to city hall."),
    "фуражка": ("service cap", "Он носит фуражку.", "He wears a service cap."),
    "прикол": ("joke, prank", "Это глупый прикол.", "This is a stupid joke."),
    "минуть": ("pass by", "Лето быстро минуло.", "Summer passed by quickly."),
    "яростно": ("fiercely", "Он яростно спорит.", "He argues fiercely."),
    "месячный": ("monthly", "Это месячный план.", "This is a monthly plan."),
    "пожимать": ("to shake", "Я не люблю пожимать руки.", "I don't like to shake hands."),
    "туалетный": ("toilet", "Купи туалетную бумагу.", "Buy toilet paper."),
    "нырнуть": ("dive", "Он нырнул в озеро.", "He dived into the lake."),
    "искушение": ("temptation", "Это сильное искушение.", "This is a strong temptation."),
    "заросль": ("thicket", "Он вошёл в заросль.", "He went into the thicket."),
    "необычайный": ("extraordinary", "Это необычайный случай.", "This is an extraordinary case."),
    "забава": ("fun, amusement", "Это простая забава.", "This is simple fun."),
    "идентификация": ("identification", "Нужна идентификация.", "Identification is needed."),
    "содержательный": ("meaningful", "Это содержательный разговор.", "This is a meaningful conversation."),
    "дискриминация": ("discrimination", "Дискриминация незаконна.", "Discrimination is illegal."),
    "предназначение": ("purpose", "Это его предназначение.", "This is his purpose."),
    "фанат": ("fan", "Она фанат этой команды.", "She is a fan of this team."),
    "собеседование": ("interview", "Собеседование завтра утром.", "The interview is tomorrow morning."),
    "уводить": ("lead away", "Не уводи его.", "Don't lead him away."),
    "летучий": ("volatile", "Это летучий газ.", "This is a volatile gas."),
    "срывать": ("pluck", "Не срывай цветы.", "Don't pluck the flowers."),
    "босой": ("barefoot", "Он идёт босой.", "He is walking barefoot."),
    "перила": ("railing", "Перила холодные.", "The railing is cold."),
    "вопить": ("to yell", "Он начал вопить.", "He began to yell."),
    "клочок": ("scrap, tuft", "Клочок бумаги упал.", "A scrap of paper fell."),
    "снайпер": ("sniper", "Снайпер ждёт сигнала.", "The sniper waits for a signal."),
    "перебивать": ("interrupt", "Не перебивай меня.", "Don't interrupt me."),
    "пермский": ("Perm", "Это пермский город.", "This is a Perm city."),
    "хрустальный": ("crystal", "Это хрустальный стакан.", "This is a crystal glass."),
    "гитлеровский": ("Nazi", "Это гитлеровский режим.", "This is a Nazi regime."),
    "настойчивый": ("persistent", "Он очень настойчивый.", "He is very persistent."),
    "зенитный": ("anti-aircraft", "Зенитный огонь начался.", "The anti-aircraft fire started."),
    "рассердиться": ("to get angry", "Он легко рассердился.", "He got angry easily."),
    "выслушивать": ("to listen to", "Я выслушиваю их.", "I listen to them."),
    "координатор": ("coordinator", "Она наш координатор.", "She is our coordinator."),
    "идентичность": ("identity", "Это её идентичность.", "This is her identity."),
    "поливать": ("to water", "Я поливаю цветы.", "I am watering the flowers."),
    "прилично": ("decently", "Она прилично одета.", "She is decently dressed."),
    "болельщик": ("fan, supporter", "Он болельщик этой команды.", "He is a fan of this team."),
    "комфортный": ("comfortable", "Стул очень комфортный.", "The chair is very comfortable."),
    "целесообразный": ("expedient", "Это целесообразный план.", "This is an expedient plan."),
    "поменяться": ("to exchange", "Давай поменяемся местами.", "Let's exchange places."),
    "чулок": ("stocking", "Чулок лежит на стуле.", "The stocking is on the chair."),
    "неспособный": ("incapable", "Он неспособен врать.", "He is incapable of lying."),
    "коленка": ("knee", "У меня болит коленка.", "My knee hurts."),
    "сокращаться": ("to decrease", "Штат будет сокращаться.", "The staff will decrease."),
    "ух": ("whoa", "Ух, как холодно!", "Whoa, it's so cold!"),
    "подозрительно": ("suspiciously", "Тут подозрительно тихо.", "It is suspiciously quiet here."),
    "капиталист": ("capitalist", "Он богатый капиталист.", "He is a rich capitalist."),
    "ньютон": ("Newton", "Это один ньютон.", "This is one Newton."),
}

print(
    rewrite_chunk(
        Path("russian_english/_chunks/deck_15260215_02.csv"),
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
    "там", "здесь", "давай", "нем", "нём", "ней", "них",
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
    "kept": "keep", "lost": "lose", "fell": "fall", "grew": "grow", "held": "hold",
    "knew": "know", "ran": "run", "sat": "sit", "stood": "stand", "told": "tell",
    "thought": "think", "wrote": "write", "spoke": "speak", "broke": "break",
    "chose": "choose", "drove": "drive", "ate": "eat", "flew": "fly",
    "dived": "dive", "dove": "dive", "laughed": "laugh", "walked": "walk",
    "looked": "look", "ripened": "ripen", "managed": "manage", "passed": "pass",
    "started": "start", "waited": "wait", "wait": "wait", "waits": "wait",
    "hurts": "hurt", "argues": "argue", "grows": "grow", "needs": "need",
    "works": "work", "writes": "write", "likes": "like", "express": "express",
    "lying": "lie", "dressed": "dress", "watering": "water", "shaking": "shake",
    "walking": "walk", "going": "go", "coming": "come", "taking": "take",
}

IRREGULAR_RU = {
    "идет": "идти", "иду": "идти", "шел": "идти", "шла": "идти", "шли": "идти",
    "нужна": "нужный", "нужен": "нужный", "нужно": "нужный",
    "созрели": "созреть", "минуло": "минуть", "нырнул": "нырнуть",
    "умудрилась": "умудриться", "свершилась": "свершиться",
    "рассердился": "рассердиться", "поменяемся": "поменяться",
    "перепиши": "переписать", "упускай": "упускать", "перебивай": "перебивать",
    "срывай": "срывать", "уводи": "уводить", "поливаю": "поливать",
    "пожимает": "пожимать", "выслушиваю": "выслушивать",
    "растворится": "раствориться", "вошел": "войти", "ждёт": "ждать",
    "ждет": "ждать", "болит": "болеть", "смотрит": "смотреть",
    "смотрел": "смотреть", "смеялся": "смеяться", "молчит": "молчать",
    "ранит": "ранить", "выражаю": "выражать", "нравится": "нравиться",
    "растёт": "расти", "растет": "расти",     "уронила": "уронить",
    "упал": "упасть",
    "чае": "чай",
    "руку": "рука",
    "руки": "рука",
    "неспособен": "неспособный",
    "пожимай": "пожимать",
    "люблю": "любить",
    "носит": "носить", "купи": "купить", "сними": "снять",
    "одобряю": "одобрять", "пишет": "писать", "отдал": "отдать",
    "началась": "начаться", "начался": "начаться", "начал": "начать",
    "начала": "начать", "спорит": "спорить", "лежит": "лежать",
    "пришел": "прийти", "пришёл": "прийти", "незаконна": "незаконный",
    "холодные": "холодный", "сильное": "сильный", "сильна": "сильный",
    "глупый": "глупый", "банковское": "банковский",
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


dest = REPO / "russian_english/_chunks/fixed/deck_15260215_02.csv"
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
