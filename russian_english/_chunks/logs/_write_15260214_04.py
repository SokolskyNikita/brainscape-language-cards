import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from brainscape import (
    answer_lemma_from_card,
    card_write_payload,
    cards_from_path,
    lemma_from_card,
)
from russian_english._chunk_io import rewrite_chunk

print(
    rewrite_chunk(
        Path("russian_english/_chunks/deck_15260214_04.csv"),
        {
            "офицерский": (
                "officer's, commissioned officer's",
                "Офицерская форма чистая.",
                "The officer's uniform is clean.",
            ),
            "сирота": (
                "orphan, waif",
                "Он сирота.",
                "He is an orphan.",
            ),
            "тележка": (
                "cart, trolley",
                "Тележка полная.",
                "The cart is full.",
            ),
            "вырабатывать": (
                "produce, generate",
                "Завод вырабатывает сталь.",
                "The plant produces steel.",
            ),
            "следственный": (
                "investigative, inquisitorial",
                "Следственная группа здесь.",
                "The investigative team is here.",
            ),
            "подавление": (
                "suppression, repression",
                "Это подавление прав.",
                "This is suppression of rights.",
            ),
            "замешательство": (
                "confusion, perplexity",
                "Она в замешательстве.",
                "She is in confusion.",
            ),
            "красноярский": (
                "Krasnoyarsk, Krasnoyarsky",
                "Это Красноярский край.",
                "This is the Krasnoyarsk region.",
            ),
            "опровергнуть": (
                "refute, disprove",
                "Он опроверг слух.",
                "He refuted the rumor.",
            ),
            "эскадра": (
                "squadron, flotilla",
                "Эскадра вышла в море.",
                "The squadron went to sea.",
            ),
            "выплатить": (
                "to pay, to pay out",
                "Выплати долг завтра.",
                "Pay the debt tomorrow.",
            ),
            "опция": (
                "option, choice",
                "Это платная опция.",
                "This is a paid option.",
            ),
            "непредсказуемый": (
                "unpredictable, unforeseeable",
                "Погода непредсказуемая.",
                "The weather is unpredictable.",
            ),
            "стихийный": (
                "spontaneous, elemental",
                "Это стихийный митинг.",
                "This is a spontaneous rally.",
            ),
            "кинжал": (
                "dagger, dirk",
                "У него кинжал.",
                "He has a dagger.",
            ),
            "облегчать": (
                "to alleviate, to ease",
                "Это облегчает боль.",
                "This alleviates pain.",
            ),
            "обнажить": (
                "expose, bare",
                "Он обнажил рану.",
                "He exposed the wound.",
            ),
            "правонарушение": (
                "violation, infringement",
                "Это большое правонарушение.",
                "This is a large violation.",
            ),
            "активист": (
                "activist",
                "Активист вышел на площадь.",
                "The activist went to the square.",
            ),
            "настольный": (
                "tabletop, desktop",
                "Это настольная игра.",
                "This is a tabletop game.",
            ),
            "затея": (
                "idea, venture",
                "Это глупая затея.",
                "This is a stupid idea.",
            ),
            "предпринимательский": (
                "entrepreneurial, business-oriented",
                "Это предпринимательский риск.",
                "This is an entrepreneurial risk.",
            ),
            "калитка": (
                "small gate, wicket",
                "Калитка открыта.",
                "The small gate is open.",
            ),
            "водяной": (
                "water, aquatic",
                "Это водяной знак.",
                "This is a water mark.",
            ),
            "ветхий": (
                "old, decrepit",
                "Это ветхий дом.",
                "This is an old house.",
            ),
            "приказание": (
                "order, instruction",
                "Он дал приказание.",
                "He gave an order.",
            ),
            "скотина": (
                "cattle, beast",
                "Скотина в поле.",
                "The cattle are in the field.",
            ),
            "вручную": (
                "manually, by hand",
                "Он пишет вручную.",
                "He writes manually.",
            ),
            "здоровенный": (
                "huge, enormous",
                "Он здоровенный.",
                "He is huge.",
            ),
            "пропорция": (
                "proportion, ratio",
                "Смешай в этой пропорции.",
                "Mix it in this proportion.",
            ),
            "престиж": (
                "prestige",
                "Ему важен престиж.",
                "Prestige matters to him.",
            ),
            "иудей": (
                "Jew, Hebrew",
                "Он иудей.",
                "He is a Jew.",
            ),
            "обнаруживаться": (
                "to be found, to be detected",
                "Ошибка обнаруживается сразу.",
                "The error is found at once.",
            ),
            "податься": (
                "to go, to apply",
                "Он решил податься в город.",
                "He decided to go to the city.",
            ),
            "гонорар": (
                "fee, honorarium",
                "Гонорар большой.",
                "The fee is large.",
            ),
            "варвар": (
                "barbarian, savage",
                "Варвар сжёг деревню.",
                "The barbarian burned the village.",
            ),
            "исполняться": (
                "to be fulfilled, to come true",
                "Мечты исполняются.",
                "Dreams are fulfilled.",
            ),
            "рискованный": (
                "risky, hazardous",
                "Это рискованный шаг.",
                "This is a risky step.",
            ),
            "пословица": (
                "proverb, saying",
                "Это старая пословица.",
                "This is an old proverb.",
            ),
            "вовсю": (
                "at full tilt, in full swing",
                "Он бежал вовсю.",
                "He ran at full tilt.",
            ),
            "буфет": (
                "canteen, buffet",
                "Мы ели в буфете.",
                "We ate in the canteen.",
            ),
            "огневой": (
                "fire, gunfire",
                "Это огневая точка.",
                "This is a fire point.",
            ),
            "неотъемлемый": (
                "integral, inseparable",
                "Это неотъемлемое право.",
                "This is an integral right.",
            ),
            "водопад": (
                "waterfall, cascade",
                "Водопад шумит.",
                "The waterfall is loud.",
            ),
            "славянин": (
                "Slav, Slavic person",
                "Он славянин.",
                "He is a Slav.",
            ),
            "стипендия": (
                "scholarship, grant",
                "Она получила стипендию.",
                "She got a scholarship.",
            ),
            "радиус": (
                "radius",
                "Радиус круга мал.",
                "The circle's radius is small.",
            ),
            "грамматика": (
                "grammar, syntax",
                "Грамматика трудная.",
                "The grammar is hard.",
            ),
            "вычислить": (
                "calculate, compute",
                "Я вычислил сумму.",
                "I calculated the sum.",
            ),
            "информировать": (
                "inform, notify",
                "Информируй меня сразу.",
                "Inform me at once.",
            ),
            "пафос": (
                "pathos, pomposity",
                "В речи много пафоса.",
                "The speech has much pathos.",
            ),
            "запутаться": (
                "get confused, get entangled",
                "Я запутался.",
                "I got confused.",
            ),
            "безусловный": (
                "unconditional, absolute",
                "Это безусловная любовь.",
                "This is unconditional love.",
            ),
            "хижина": (
                "hut, cabin",
                "Хижина у реки.",
                "The hut is by the river.",
            ),
            "золотистый": (
                "golden, goldish",
                "У неё золотистые волосы.",
                "She has golden hair.",
            ),
            "ритуальный": (
                "ritual, ceremonial",
                "Это ритуальный танец.",
                "This is a ritual dance.",
            ),
            "участковый": (
                "beat officer, precinct officer",
                "Участковый пришёл к нам.",
                "The beat officer came to us.",
            ),
            "развал": (
                "collapse, breakdown",
                "Развал союза быстрый.",
                "The union collapse is fast.",
            ),
            "пастух": (
                "shepherd, herdsman",
                "Пастух гонит стадо.",
                "The shepherd drives the flock.",
            ),
            "информационно": (
                "informationally",
                "Он ответил информационно.",
                "He answered informationally.",
            ),
            "пробиваться": (
                "break through, make one's way",
                "Он пробивается сквозь толпу.",
                "He breaks through the crowd.",
            ),
            "пролетать": (
                "to fly by, to pass",
                "Время пролетает быстро.",
                "Time flies by fast.",
            ),
            "типография": (
                "printing house, print shop",
                "Типография печатает книги.",
                "The printing house prints books.",
            ),
            "сострадание": (
                "compassion, sympathy",
                "У неё есть сострадание.",
                "She has compassion.",
            ),
            "субстанция": (
                "substance, matter",
                "Это вредная субстанция.",
                "This is a harmful substance.",
            ),
            "копать": (
                "dig, excavate",
                "Копай яму здесь.",
                "Dig a hole here.",
            ),
            "банан": (
                "banana",
                "Я ем банан.",
                "I eat a banana.",
            ),
            "майский": (
                "May, May-time",
                "Это майский день.",
                "This is a May day.",
            ),
            "парта": (
                "desk, school desk",
                "Сядь за парту.",
                "Sit at the desk.",
            ),
            "широта": (
                "latitude, breadth",
                "Широта Москвы известна.",
                "Moscow's latitude is known.",
            ),
            "отопление": (
                "heating, central heating",
                "Отопление не работает.",
                "The heating does not work.",
            ),
            "шаман": (
                "shaman, shamanic healer",
                "Шаман живёт далеко.",
                "The shaman lives far away.",
            ),
            "копыто": (
                "hoof, cloven hoof",
                "У лошади болит копыто.",
                "The horse's hoof hurts.",
            ),
            "напоследок": (
                "finally, lastly",
                "Напоследок он сказал правду.",
                "Finally he told the truth.",
            ),
            "пониматься": (
                "to be understood, to be comprehensible",
                "Это понимается иначе.",
                "This is understood otherwise.",
            ),
            "радуга": (
                "rainbow, iris",
                "После дождя радуга.",
                "After the rain, a rainbow.",
            ),
            "увлекательный": (
                "fascinating, captivating",
                "Это увлекательный рассказ.",
                "This is a fascinating story.",
            ),
            "караул": (
                "guard, sentinel",
                "Караул стоит у двери.",
                "The guard stands at the door.",
            ),
            "раздумывать": (
                "ponder, reflect",
                "Я раздумываю над этим.",
                "I ponder this.",
            ),
            "утверждаться": (
                "to be affirmed, to be established",
                "Это мнение утверждается.",
                "This opinion is being affirmed.",
            ),
            "методология": (
                "methodology, methodological approach",
                "Его методология ясна.",
                "His methodology is clear.",
            ),
            "впечатлять": (
                "impress",
                "Ты меня впечатляешь.",
                "You impress me.",
            ),
            "дюжина": (
                "dozen, twelve",
                "Купи дюжину яиц.",
                "Buy a dozen eggs.",
            ),
            "терминал": (
                "terminal, kiosk",
                "Мы в терминале.",
                "We are in the terminal.",
            ),
            "полезность": (
                "utility, usefulness",
                "Я вижу полезность этого.",
                "I see the utility of this.",
            ),
            "гамма": (
                "range, gamma",
                "Гамма цветов широкая.",
                "The color range is wide.",
            ),
            "туннель": (
                "tunnel, underpass",
                "Поезд в туннеле.",
                "The train is in the tunnel.",
            ),
            "грабить": (
                "rob, loot",
                "Они грабят банк.",
                "They rob the bank.",
            ),
            "персидский": (
                "Persian, Farsi",
                "Это персидский кот.",
                "This is a Persian cat.",
            ),
            "спад": (
                "decline, downturn",
                "Это экономический спад.",
                "This is an economic decline.",
            ),
            "вздумать": (
                "to fancy, to conceive",
                "Не вздумай уехать.",
                "Do not fancy leaving.",
            ),
            "киоск": (
                "kiosk, booth",
                "Купи воду в киоске.",
                "Buy water at the kiosk.",
            ),
            "канцелярия": (
                "office, chancellery",
                "Она в канцелярии.",
                "She is in the office.",
            ),
            "ссориться": (
                "to quarrel, to argue",
                "Они снова ссорятся.",
                "They quarrel again.",
            ),
            "тыкать": (
                "poke, prod",
                "Не тыкай меня.",
                "Don't poke me.",
            ),
            "неограниченный": (
                "unlimited, unrestricted",
                "У него неограниченный доступ.",
                "He has unlimited access.",
            ),
            "яростный": (
                "furious, fierce",
                "Он яростный.",
                "He is furious.",
            ),
            "разыскивать": (
                "to search for, to look for",
                "Полиция разыскивает его.",
                "Police search for him.",
            ),
            "финальный": (
                "final, last",
                "Это финальный матч.",
                "This is the final match.",
            ),
            "сбыться": (
                "come true, be fulfilled",
                "Мечта может сбыться.",
                "The dream can come true.",
            ),
        },
    )
)

FUNCTION_EN = {
    "the", "a", "an", "to", "of", "in", "on", "at", "for", "with", "by", "from",
    "and", "or", "but", "not", "no", "yes", "is", "are", "was", "were", "be",
    "been", "being", "am", "do", "does", "did", "done", "have", "has", "had",
    "this", "that", "these", "those", "it", "its", "he", "she", "we", "they",
    "him", "her", "us", "them", "his", "our", "their", "my", "your", "me", "you",
    "i", "there", "here", "so", "too", "very", "just", "as", "if", "than",
    "into", "out", "up", "down", "over", "under", "about", "after", "before",
    "again", "once", "away", "off", "then", "now", "still", "already", "yet",
    "don't", "doesn't", "didn't", "isn't", "aren't", "wasn't", "weren't",
}

FUNCTION_RU = {
    "в", "во", "на", "с", "со", "к", "ко", "у", "о", "об", "от", "до",
    "из", "за", "по", "под", "над", "при", "для", "без", "между", "через",
    "был", "была", "было", "были", "будет", "будут", "буду", "есть", "быть",
    "уже", "еще", "ещё", "также", "тоже", "только", "вот", "ведь", "ну", "все",
    "как", "что", "чтобы", "когда", "если", "где", "чем", "кто", "тут",
    "там", "здесь", "давай", "нем", "нём", "ней", "них", "не", "ни", "да",
    "и", "а", "но", "или", "же", "ли", "бы", "какая", "какой", "какое",
    "этот", "эта", "это", "эти", "этой", "этом", "этому", "этого", "этим",
    "этих", "этими", "тот", "та", "те", "той", "том", "тому", "того", "тем",
    "ему", "его", "ей", "им", "их", "нам", "нас", "вам", "вас", "мне",
    "тебя", "тебе", "нее", "неё", "мой", "моя", "мое", "моё", "мои",
    "твой", "твоя", "наш", "наша", "ваш", "ваша",
}

allow_en = {
    line.strip().lower()
    for line in (REPO / "russian_english/_vocab/allow_en_15260214.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_ru = {
    line.strip().replace("ё", "е").lower()
    for line in (REPO / "russian_english/_vocab/allow_ru_15260214.txt").read_text(encoding="utf-8").splitlines()
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
    "matters": "matter", "lives": "live", "hurts": "hurt", "breaks": "break",
    "flies": "fly", "prints": "print", "robs": "rob", "fancied": "fancy",
    "answered": "answer", "understood": "understand", "fulfilled": "fulfill",
    "alleviates": "alleviate", "exposed": "expose", "refuted": "refute",
    "calculated": "calculate", "known": "know",
}

IRREGULAR_RU = {
    "идет": "идти", "иду": "идти", "шел": "идти", "шла": "идти", "шли": "идти",
    "вышла": "выйти", "вышел": "выйти", "виден": "видный",
    "нужна": "нужный", "нужен": "нужный", "нужно": "нужный",
    "бежал": "бежать", "ели": "есть", "ем": "есть",
    "пишет": "писать", "говорит": "говорить",
    "любит": "любить", "болит": "болеть", "живет": "жить",
    "стоит": "стоять", "сказал": "сказать", "ответил": "ответить",
    "получила": "получить", "пришел": "прийти",
    "сжег": "сжечь", "гонит": "гнать",
    "печатает": "печатать", "грабят": "грабить",
    "ссорятся": "ссориться", "тыкай": "тыкать",
    "копай": "копать", "сядь": "сесть", "купи": "купить",
    "смешай": "смешать", "выплати": "выплатить",
    "информируй": "информировать", "опроверг": "опровергнуть",
    "обнажил": "обнажить", "подался": "податься",
    "вычислил": "вычислить", "запутался": "запутаться",
    "вздумал": "вздумать", "сбылась": "сбыться",
    "разыскивает": "разыскивать", "пробивается": "пробиваться",
    "пролетает": "пролетать", "обнаруживается": "обнаруживаться",
    "исполняются": "исполняться", "понимается": "пониматься",
    "утверждается": "утверждаться", "раздумываю": "раздумывать",
    "впечатляешь": "впечатлять", "облегчает": "облегчать",
    "вырабатывает": "вырабатывать",
    "рану": "рана", "дал": "дать", "важен": "важный",
    "шумит": "шуметь", "мал": "малый", "речи": "речь",
    "реки": "река", "яму": "яма", "ясна": "ясный",
    "яиц": "яйцо", "вижу": "видеть", "воду": "вода",
    "открыта": "открытый", "решил": "решить",
    "вздумай": "вздумать", "может": "мочь",
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


dest = REPO / "russian_english/_chunks/fixed/deck_15260214_04.csv"
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
