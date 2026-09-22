import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from brainscape import answer_lemma_from_card, card_write_payload, cards_from_path, lemma_from_card
from russian_english._chunk_io import rewrite_chunk

PACK = REPO / "russian_english"
SRC = PACK / "_chunks" / "deck_15260213_03.csv"

FUNCTION_EN = {
    "a", "the", "is", "be", "i", "you", "he", "she", "it", "we", "they",
    "my", "and", "or", "in", "on", "at", "to", "of", "for", "with", "from",
    "not", "his", "him", "her", "their", "them", "our", "us", "me", "am",
    "are", "was", "were", "been", "being", "this", "that", "these", "those",
    "an", "as", "by", "into", "about", "than", "then", "so", "if", "but",
    "its", "your", "im", "dont", "cant", "lets", "didnt", "wont", "isnt",
    "there", "here", "very", "too", "now", "today", "yesterday", "tomorrow",
    "some", "any", "all", "no", "yes", "do", "does", "did", "have", "has",
    "had", "will", "would", "can", "could", "should", "must", "may", "might",
    "please", "more", "most", "less", "much", "many", "few", "such", "also",
    "only", "even", "still", "already", "always", "never", "often", "once",
    "after", "before", "under", "over", "through", "between", "without",
    "who", "what", "when", "where", "why", "how", "which",
    "ago", "ones", "two", "down", "up", "out", "off", "back",
    "herself", "himself", "themselves", "myself", "yourself", "oneself",
    "one", "onto", "dont", "doesnt", "lets", "don't",
}

FUNCTION_RU = {
    "я", "мне", "меня", "мной", "мой", "моя", "мое", "моё", "мои", "мою",
    "мы", "нам", "нас", "нами", "наш", "наша", "наше", "наши", "нашу",
    "ты", "тебе", "тебя", "тобой", "твой", "твоя", "твое", "твоё", "твои",
    "вы", "вам", "вас", "вами", "ваш", "ваша", "ваше", "ваши", "вашу",
    "он", "она", "оно", "они", "его", "ее", "её", "ей", "ему", "им", "их",
    "ими", "ним", "ней", "ними", "него", "нее", "неё",
    "себя", "себе", "собой", "свой", "своя", "свое", "своё", "свои", "свою",
    "своим", "своего", "своей",
    "это", "эта", "этот", "эти", "этого", "этой", "этому", "этим", "этих", "эту",
    "то", "та", "тот", "те", "того", "той", "тому", "тем", "тех", "ту",
    "такой", "такая", "такое", "такие", "так",
    "не", "ни", "нет", "да", "вот", "уж", "ли", "же", "бы",
    "в", "на", "с", "со", "у", "к", "ко", "по", "из", "за", "от", "до",
    "для", "без", "при", "о", "об", "про", "над", "под", "между", "через",
    "после", "перед", "и", "а", "но", "или", "что", "как", "когда", "где",
    "чтобы", "если", "потому", "уже", "еще", "ещё", "только", "даже", "тоже",
    "также", "очень", "сейчас", "теперь", "всегда", "сегодня", "вчера", "завтра",
    "был", "была", "было", "были", "будет", "будут", "есть", "быть",
    "здесь", "тут", "там", "можно", "нужно", "должен", "должна", "должно", "должны",
    "во", "всё", "все", "всех", "всю", "весь", "слишком", "сам", "самом",
    "из-за", "изза", "хорошо", "давай", "скоро", "часто", "один", "одна",
    "надо", "сюда", "туда", "отсюда",
}

allow_en = {
    line.strip().lower()
    for line in (PACK / "_vocab" / "allow_en_15260213.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_ru = {
    line.strip().replace("ё", "е").lower()
    for line in (PACK / "_vocab" / "allow_ru_15260213.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_en |= FUNCTION_EN
allow_ru |= FUNCTION_RU

IRREGULAR_EN = {
    "made": "make", "met": "meet", "saw": "see", "got": "get", "gave": "give",
    "took": "take", "came": "come", "went": "go", "goes": "go", "ate": "eat",
    "spoke": "speak", "broke": "break", "bought": "buy", "built": "build",
    "found": "find", "left": "leave", "held": "hold", "holds": "hold",
    "told": "tell", "said": "say", "heard": "hear", "paid": "pay",
    "sold": "sell", "lost": "lose", "spent": "spend", "stood": "stand",
    "stands": "stand", "wrote": "write", "flew": "fly", "grew": "grow",
    "began": "begin", "became": "become", "did": "do", "done": "do",
    "had": "have", "has": "have", "been": "be", "was": "be", "were": "be",
    "lit": "light", "slept": "sleep", "opened": "open", "hints": "hint",
    "howls": "howl", "hurts": "hurt", "loves": "love", "managed": "manage",
    "predicted": "predict", "rushed": "rush", "sneaks": "sneak",
    "started": "start", "answered": "answer", "needed": "need",
    "fascinated": "fascinate", "running": "run", "allowed": "allow",
    "letters": "letter", "children": "child", "studies": "study",
}

IRREGULAR_RU = {
    "может": "мочь", "могу": "мочь", "можем": "мочь",
    "хочу": "хотеть", "хочет": "хотеть", "хотим": "хотеть",
    "вижу": "видеть", "видишь": "видеть", "видит": "видеть",
    "знаю": "знать", "живу": "жить", "живет": "жить", "живёт": "жить",
    "шла": "идти", "шел": "идти", "шёл": "идти", "шли": "идти",
    "идет": "идти", "идёт": "идти", "идем": "идти", "идём": "идти",
    "стал": "стать", "стала": "стать", "стали": "стать",
    "воет": "выть", "выют": "выть",
    "задалсь": "задаваться", "задаюсь": "задаваться",
    "пригоден": "пригодный", "бессилен": "бессильный",
    "болит": "болеть", "начался": "начаться", "начал": "начать",
    "открыл": "открыть", "купила": "купить", "купил": "купить",
    "ответила": "ответить", "ответил": "ответить",
    "сказал": "сказать", "увлекла": "увлечь",
    "возвели": "возвести", "предсказал": "предсказать",
    "прибежал": "прибежать", "благословит": "благословить",
    "выгляни": "выглянуть", "сдвинь": "сдвинуть", "ткни": "ткнуть",
    "устремился": "устремиться", "тронулся": "тронуться",
    "потерял": "потерять", "делает": "делать",
}


def _en_ok(word: str) -> bool:
    w = word.lower()
    if w in allow_en:
        return True
    if IRREGULAR_EN.get(w) in allow_en:
        return True
    if "-" in w and all(_en_ok(p) for p in w.split("-") if p):
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


RU_ENDINGS = (
    "ами", "ями", "ого", "его", "ому", "ему", "ыми", "ими", "ой", "ей", "ом",
    "ем", "ах", "ях", "ам", "ям", "ов", "ев", "ую", "юю", "ая", "яя",
    "ое", "ее", "ые", "ие", "ый", "ий", "ую", "а", "я", "у", "ю", "е", "и",
    "ы", "о", "ь",
)


def _ru_stems(word: str) -> set[str]:
    w = word.replace("ё", "е").lower()
    out = {w}
    for n in range(3, min(6, len(w) + 1)):
        out.add(w[:n])
    for suf in RU_ENDINGS:
        if w.endswith(suf) and len(w) - len(suf) >= 3:
            out.add(w[: -len(suf)])
    return out


def _ru_ok(word: str) -> bool:
    w = word.replace("ё", "е").lower()
    if w in allow_ru:
        return True
    mapped = IRREGULAR_RU.get(w)
    if mapped and mapped in allow_ru:
        return True
    stems = _ru_stems(w)
    for lemma in allow_ru:
        if len(lemma) < 3:
            continue
        if stems & _ru_stems(lemma):
            return True
        stem = lemma[:4] if len(lemma) >= 4 else lemma
        if w.startswith(stem) or lemma.startswith(w[:4] if len(w) >= 4 else w):
            return True
    return False


def _tokens(text: str) -> list[str]:
    return re.findall(r"[A-Za-zА-Яа-яЁё'-]+", text)


FIXES = {
    "тесто": (
        "dough, batter",
        "Я вижу тесто.",
        "I see the dough.",
    ),
    "задаваться": (
        "ask oneself, wonder",
        "Он начал задаваться вопросом.",
        "He began to ask himself a question.",
    ),
    "уменьшать": (
        "reduce, decrease",
        "Надо уменьшать скорость.",
        "We must reduce the speed.",
    ),
    "полезно": (
        "useful, beneficial",
        "Это очень полезно.",
        "This is very useful.",
    ),
    "картофель": (
        "potato, potatoes",
        "Картофель уже готов.",
        "The potato is already ready.",
    ),
    "небрежно": (
        "carelessly, negligently",
        "Он небрежно открыл дверь.",
        "He carelessly opened the door.",
    ),
    "отсек": (
        "compartment, section",
        "Вот большой отсек.",
        "Here is a large compartment.",
    ),
    "желаемый": (
        "desired, wished",
        "Это желаемый результат.",
        "This is the desired result.",
    ),
    "вычисление": (
        "calculation, computation",
        "Вычисление верное.",
        "The calculation is correct.",
    ),
    "лезвие": (
        "blade, edge",
        "Лезвие очень острое.",
        "The blade is very sharp.",
    ),
    "вылезти": (
        "to climb out, to emerge",
        "Надо вылезти отсюда.",
        "We must climb out of here.",
    ),
    "мерзкий": (
        "disgusting, vile",
        "Он мерзкий человек.",
        "He is a disgusting person.",
    ),
    "косметика": (
        "cosmetics, makeup",
        "Она купила косметику.",
        "She bought cosmetics.",
    ),
    "проникновение": (
        "penetration, infiltration",
        "Это проникновение в дом.",
        "This is a penetration into the house.",
    ),
    "конечность": (
        "limb, extremity",
        "Конечность уже здесь.",
        "The limb is already here.",
    ),
    "русскоязычный": (
        "Russian-speaking, Russian-language",
        "Он русскоязычный учитель.",
        "He is a Russian-speaking teacher.",
    ),
    "тренироваться": (
        "to train, to practice",
        "Я хочу тренироваться.",
        "I want to train.",
    ),
    "зарегистрироваться": (
        "to register, to sign up",
        "Надо зарегистрироваться здесь.",
        "I need to register here.",
    ),
    "ил": (
        "silt, mud",
        "Вот ил.",
        "Here is silt.",
    ),
    "тронуться": (
        "to move, to start off",
        "Машина не хочет тронуться.",
        "The car does not want to move.",
    ),
    "крошка": (
        "crumb, baby",
        "Крошка на столе.",
        "A crumb is on the table.",
    ),
    "разгром": (
        "defeat, rout",
        "Это полный разгром.",
        "This is a complete defeat.",
    ),
    "подставить": (
        "to set up, to frame",
        "Не надо меня подставить.",
        "Do not set me up.",
    ),
    "тусклый": (
        "dim, dull",
        "Свет тусклый.",
        "The light is dim.",
    ),
    "намекать": (
        "hint, imply",
        "Не надо намекать.",
        "Do not hint.",
    ),
    "вставлять": (
        "insert, put in",
        "Надо вставлять карту.",
        "We must insert the card.",
    ),
    "нежелание": (
        "reluctance, unwillingness",
        "Его нежелание ясно.",
        "His reluctance is clear.",
    ),
    "приписывать": (
        "attribute, ascribe",
        "Они приписывают это мне.",
        "They attribute this to me.",
    ),
    "бунт": (
        "rebellion, mutiny",
        "Бунт уже здесь.",
        "The rebellion is already here.",
    ),
    "роща": (
        "grove, copse",
        "Вот роща.",
        "Here is a grove.",
    ),
    "терминология": (
        "terminology, nomenclature",
        "Эта терминология сложная.",
        "This terminology is complex.",
    ),
    "необычайно": (
        "extraordinarily, exceptionally",
        "Это необычайно важно.",
        "This is extraordinarily important.",
    ),
    "выглянуть": (
        "to look out, to peek",
        "Надо выглянуть в окно.",
        "We must look out the window.",
    ),
    "штурмовик": (
        "assault trooper, stormtrooper",
        "Штурмовик уже здесь.",
        "The assault trooper is already here.",
    ),
    "пригодный": (
        "suitable, fit",
        "Этот нож пригоден.",
        "This knife is suitable.",
    ),
    "выручка": (
        "revenue, proceeds",
        "Какая сегодня выручка?",
        "What is today's revenue?",
    ),
    "обилие": (
        "abundance, plenty",
        "Здесь обилие воды.",
        "Here is an abundance of water.",
    ),
    "распоряжаться": (
        "to manage, to dispose of",
        "Кто будет распоряжаться?",
        "Who will manage?",
    ),
    "снабжение": (
        "supply, provisioning",
        "Снабжение уже здесь.",
        "The supply is already here.",
    ),
    "гормон": (
        "hormone",
        "Это важный гормон.",
        "This is an important hormone.",
    ),
    "помещать": (
        "to place, to accommodate",
        "Не надо помещать это сюда.",
        "Do not place this here.",
    ),
    "слушание": (
        "hearing, listening",
        "Слушание завтра.",
        "The hearing is tomorrow.",
    ),
    "укреплять": (
        "to strengthen, to fortify",
        "Надо укреплять тело.",
        "We must strengthen the body.",
    ),
    "выть": (
        "howl, wail",
        "Собака начала выть.",
        "The dog began to howl.",
    ),
    "бремя": (
        "burden, load",
        "Это большое бремя.",
        "This is a big burden.",
    ),
    "угодный": (
        "pleasing, suitable",
        "Это угодный ответ.",
        "This is a pleasing answer.",
    ),
    "пробираться": (
        "sneak, thread one's way",
        "Он начал пробираться домой.",
        "He began to sneak home.",
    ),
    "плеер": (
        "player, MP3 player",
        "Где мой плеер?",
        "Where is my player?",
    ),
    "памятный": (
        "memorable, commemorative",
        "Это памятный день.",
        "This is a memorable day.",
    ),
    "графика": (
        "graphics, graphic art",
        "Графика хорошая.",
        "The graphics are good.",
    ),
    "возвести": (
        "build, erect",
        "Они хотят возвести дом.",
        "They want to build a house.",
    ),
    "сдвинуть": (
        "to shift, to move",
        "Надо сдвинуть стол.",
        "We must shift the table.",
    ),
    "перевал": (
        "mountain pass, pass",
        "Мы на перевале.",
        "We are on the mountain pass.",
    ),
    "курение": (
        "smoking, tobacco use",
        "Курение здесь нельзя.",
        "Smoking is not allowed here.",
    ),
    "паутина": (
        "web, cobweb",
        "Паутина на стене.",
        "A web is on the wall.",
    ),
    "семнадцать": (
        "seventeen",
        "Ей семнадцать.",
        "She is seventeen.",
    ),
    "снаряжение": (
        "equipment, gear",
        "Снаряжение уже готово.",
        "The equipment is already ready.",
    ),
    "доминировать": (
        "dominate, prevail",
        "Они хотят доминировать.",
        "They want to dominate.",
    ),
    "ткнуть": (
        "poke, jab",
        "Он хочет ткнуть меня.",
        "He wants to poke me.",
    ),
    "навязывать": (
        "impose, foist",
        "Не надо навязывать это.",
        "Do not impose this.",
    ),
    "бессильный": (
        "powerless, impotent",
        "Он бессильный человек.",
        "He is a powerless person.",
    ),
    "азиатский": (
        "Asian, Asiatic",
        "Это азиатский город.",
        "This is an Asian city.",
    ),
    "седло": (
        "saddle, seat",
        "Седло на столе.",
        "The saddle is on the table.",
    ),
    "гвардейский": (
        "Guards, guard",
        "Это гвардейский полк.",
        "This is a Guards regiment.",
    ),
    "правота": (
        "correctness, being right",
        "Я вижу его правоту.",
        "I see his correctness.",
    ),
    "умолчание": (
        "omission, silence",
        "Это важное умолчание.",
        "This is an important omission.",
    ),
    "полигон": (
        "test site, firing range",
        "Мы на полигоне.",
        "We are at the test site.",
    ),
    "журналистика": (
        "journalism, reporting",
        "Он любит журналистику.",
        "He loves journalism.",
    ),
    "больничный": (
        "sick leave, medical certificate",
        "Я на больничном.",
        "I am on sick leave.",
    ),
    "подчас": (
        "sometimes, occasionally",
        "Подчас это трудно.",
        "Sometimes this is hard.",
    ),
    "положительно": (
        "positively, affirmative",
        "Я положительно это знаю.",
        "I positively know this.",
    ),
    "претендент": (
        "contender, claimant",
        "Он главный претендент.",
        "He is the main contender.",
    ),
    "устремиться": (
        "to rush, to strive",
        "Он хочет устремиться туда.",
        "He wants to rush there.",
    ),
    "корона": (
        "crown, corona",
        "Корона на столе.",
        "The crown is on the table.",
    ),
    "прочность": (
        "strength, durability",
        "Прочность стены высокая.",
        "The strength of the wall is high.",
    ),
    "модификация": (
        "modification, alteration",
        "Нужна модификация.",
        "A modification is needed.",
    ),
    "поздороваться": (
        "to greet, to say hello",
        "Я хочу поздороваться.",
        "I want to greet him.",
    ),
    "предсказать": (
        "predict, forecast",
        "Кто может предсказать это?",
        "Who can predict this?",
    ),
    "повиноваться": (
        "to obey, to comply",
        "Надо повиноваться.",
        "We must obey.",
    ),
    "коза": (
        "goat, she-goat",
        "Коза в поле.",
        "The goat is in the field.",
    ),
    "несомненный": (
        "undoubted, unquestionable",
        "Это несомненный факт.",
        "This is an undoubted fact.",
    ),
    "многократно": (
        "repeatedly, many times",
        "Он многократно это делает.",
        "He does this repeatedly.",
    ),
    "выгодно": (
        "advantageous, profitable",
        "Это очень выгодно.",
        "This is very advantageous.",
    ),
    "украинец": (
        "Ukrainian, Ukrainian man",
        "Он украинец.",
        "He is Ukrainian.",
    ),
    "коварный": (
        "treacherous, cunning",
        "Это коварный план.",
        "This is a treacherous plan.",
    ),
    "аккумулятор": (
        "battery, accumulator",
        "Аккумулятор новый.",
        "The battery is new.",
    ),
    "револьвер": (
        "revolver, revolver gun",
        "Револьвер на столе.",
        "The revolver is on the table.",
    ),
    "благословить": (
        "bless, consecrate",
        "Она хочет благословить нас.",
        "She wants to bless us.",
    ),
    "переспросить": (
        "ask again, double-check",
        "Можно переспросить?",
        "Can I ask again?",
    ),
    "кривая": (
        "curve, bent",
        "Кривая на дороге.",
        "The curve is on the road.",
    ),
    "обмениваться": (
        "exchange, swap",
        "Мы хотим обмениваться.",
        "We want to exchange.",
    ),
    "сущий": (
        "utter, sheer",
        "Это сущий ад.",
        "This is utter hell.",
    ),
    "закуска": (
        "snack, appetizer",
        "Закуска уже готова.",
        "The snack is already ready.",
    ),
    "плановый": (
        "planned, scheduled",
        "Это плановая встреча.",
        "This is a planned meeting.",
    ),
    "блокнот": (
        "notebook, notepad",
        "Где мой блокнот?",
        "Where is my notebook?",
    ),
    "гусь": (
        "goose, gander",
        "Гусь в воде.",
        "The goose is in the water.",
    ),
    "увлечь": (
        "fascinate, captivate",
        "Книга может увлечь.",
        "The book can fascinate.",
    ),
    "почерк": (
        "handwriting, penmanship",
        "Её почерк плохой.",
        "Her handwriting is bad.",
    ),
    "прибежать": (
        "come running, run up",
        "Он хочет прибежать сюда.",
        "He wants to come running here.",
    ),
    "ценовой": (
        "price, pricing",
        "Это ценовой вопрос.",
        "This is a price question.",
    ),
}


def check_leftovers(dest: Path) -> list[str]:
    cards = cards_from_path(dest)
    leftover: list[str] = []
    local_en = set(allow_en)
    local_ru = set(allow_ru)
    for i, card in enumerate(cards, 1):
        lemma = lemma_from_card(card)
        gloss = answer_lemma_from_card(card)
        payload = card_write_payload(card)
        ru = payload["question"].split("## Footnote")[-1].strip()
        en = payload["answer"].split("## Footnote")[-1].strip()
        ru_l = ru.replace("ё", "е").lower()
        if lemma.replace("ё", "е").lower() not in ru_l and lemma[:4].replace("ё", "е").lower() not in ru_l:
            leftover.append(f"{i} LEMMA {lemma} :: {ru}")
        gloss_l = re.sub(r"^(to |the |a |an )", "", gloss.split(",")[0].strip().lower())
        if gloss_l and gloss_l.split()[0] not in en.lower() and not any(
            g in en.lower() for g in gloss_l.split()
        ):
            leftover.append(f"{i} GLOSS {gloss} :: {en}")
        extra_en = set()
        extra_ru = {lemma.replace("ё", "е").lower()}
        for part in re.split(r"[,;/]| or | and ", gloss):
            part = re.sub(r"^(to |the |a |an )", "", part.strip().lower())
            extra_en.update(part.split())
        local_en.update(extra_en)
        local_ru.update(extra_ru)
        for tok in _tokens(en):
            if tok.lower() not in local_en and not _en_ok(tok):
                leftover.append(f"{i} EN {tok} :: {en}")
        for tok in _tokens(ru):
            if tok.replace("ё", "е").lower() not in local_ru and not _ru_ok(tok):
                leftover.append(f"{i} RU {tok} :: {ru}")
    return leftover


stats = rewrite_chunk(SRC, FIXES)
print(stats)
leftover = check_leftovers(Path(stats["path"]))
print(f"leftovers={len(leftover)}")
if leftover:
    print("\n".join(leftover))
