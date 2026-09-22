import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from brainscape import answer_lemma_from_card, card_write_payload, cards_from_path, lemma_from_card
from russian_english._chunk_io import rewrite_chunk

PACK = REPO / "russian_english"
SRC = PACK / "_chunks" / "deck_15260213_04.csv"

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
    "eats": "eat", "reads": "read", "works": "work",
}

IRREGULAR_RU = {
    "может": "мочь", "могу": "мочь", "можем": "мочь",
    "хочу": "хотеть", "хочет": "хотеть", "хотим": "хотеть",
    "вижу": "видеть", "видишь": "видеть", "видит": "видеть",
    "знаю": "знать", "живу": "жить", "живет": "жить", "живёт": "жить",
    "шла": "идти", "шел": "идти", "шёл": "идти", "шли": "идти",
    "идет": "идти", "идёт": "идти", "идем": "идти", "идём": "идти",
    "иду": "идти",
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
    "упал": "упасть", "пришло": "прийти", "стоит": "стоять",
    "работает": "работать", "читаю": "читать", "ест": "есть",
    "весит": "весить", "устарело": "устареть", "мерцают": "мерцать",
    "выясняется": "выясняться", "нужна": "нужный",
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
    "побрать": (
        "to gather, to take",
        "Надо побрать всё.",
        "We must gather everything.",
    ),
    "перелом": (
        "fracture, break",
        "У него перелом ноги.",
        "He has a leg fracture.",
    ),
    "поддерживаться": (
        "to be supported, to be maintained",
        "Это должно поддерживаться.",
        "This must be supported.",
    ),
    "досуг": (
        "leisure, free time",
        "У меня есть досуг.",
        "I have leisure.",
    ),
    "световой": (
        "light, luminous",
        "Это световой сигнал.",
        "This is a light signal.",
    ),
    "супермаркет": (
        "supermarket, hypermarket",
        "Я в супермаркете.",
        "I am at the supermarket.",
    ),
    "весить": (
        "to weigh",
        "Сколько это весит?",
        "How much does this weigh?",
    ),
    "реактор": (
        "reactor, nuclear reactor",
        "Реактор работает.",
        "The reactor works.",
    ),
    "отрывать": (
        "to tear off, to detach",
        "Не надо отрывать это.",
        "Do not tear this off.",
    ),
    "посему": (
        "therefore, thus",
        "Посему я здесь.",
        "Therefore I am here.",
    ),
    "царица": (
        "queen, tsarina",
        "Царица уже здесь.",
        "The queen is already here.",
    ),
    "отбирать": (
        "to select, to take away",
        "Они хотят отбирать это.",
        "They want to select this.",
    ),
    "окраска": (
        "coloring, paintwork",
        "Окраска хорошая.",
        "The coloring is good.",
    ),
    "скорбь": (
        "sorrow, grief",
        "Это большая скорбь.",
        "This is great sorrow.",
    ),
    "облигация": (
        "bond, debenture",
        "Это государственная облигация.",
        "This is a government bond.",
    ),
    "постепенный": (
        "gradual, progressive",
        "Это постепенный процесс.",
        "This is a gradual process.",
    ),
    "вспомогательный": (
        "auxiliary, supplementary",
        "Это вспомогательный вопрос.",
        "This is an auxiliary question.",
    ),
    "бюрократия": (
        "bureaucracy, red tape",
        "Это большая бюрократия.",
        "This is a big bureaucracy.",
    ),
    "неинтересный": (
        "uninteresting, boring",
        "Книга неинтересная.",
        "The book is uninteresting.",
    ),
    "имение": (
        "estate, manor",
        "Это большое имение.",
        "This is a large estate.",
    ),
    "конный": (
        "equestrian, horse",
        "Это конный спорт.",
        "This is equestrian sport.",
    ),
    "неповторимый": (
        "unique, unparalleled",
        "Её стиль неповторимый.",
        "Her style is unique.",
    ),
    "оп": (
        "oops, whoa",
        "Оп, я упал.",
        "Oops, I fell.",
    ),
    "устареть": (
        "become obsolete, become outdated",
        "Это уже устарело.",
        "This has become obsolete.",
    ),
    "утка": (
        "duck, hoax",
        "Утка в воде.",
        "The duck is in the water.",
    ),
    "санитарный": (
        "sanitary, hygienic",
        "Это санитарный контроль.",
        "This is sanitary control.",
    ),
    "вектор": (
        "vector, carrier",
        "Вектор идёт сюда.",
        "The vector goes here.",
    ),
    "унитаз": (
        "toilet, commode",
        "Где унитаз?",
        "Where is the toilet?",
    ),
    "мемуары": (
        "memoirs",
        "Я читаю мемуары.",
        "I read memoirs.",
    ),
    "реестр": (
        "register, registry",
        "Это национальный реестр.",
        "This is the national register.",
    ),
    "мерцать": (
        "twinkle, flicker",
        "Звёзды мерцают.",
        "Stars twinkle.",
    ),
    "острота": (
        "sharpness, pungency",
        "Острота ножа высокая.",
        "The knife's sharpness is high.",
    ),
    "стереть": (
        "erase, delete",
        "Надо стереть это.",
        "We must erase this.",
    ),
    "оправдываться": (
        "to make excuses, to justify oneself",
        "Не надо оправдываться.",
        "Do not make excuses.",
    ),
    "кандидатура": (
        "candidacy, nomination",
        "Его кандидатура хорошая.",
        "His candidacy is good.",
    ),
    "ресница": (
        "eyelash, eyelashes",
        "У неё длинная ресница.",
        "She has a long eyelash.",
    ),
    "авторитетный": (
        "authoritative, reputable",
        "Это авторитетный человек.",
        "This is an authoritative person.",
    ),
    "чердак": (
        "attic, loft",
        "Я на чердаке.",
        "I am in the attic.",
    ),
    "сверстник": (
        "peer, contemporary",
        "Он мой сверстник.",
        "He is my peer.",
    ),
    "яркость": (
        "brightness, vividness",
        "Яркость очень высокая.",
        "The brightness is very high.",
    ),
    "финн": (
        "Finn, Finnish",
        "Он финн.",
        "He is a Finn.",
    ),
    "бодрый": (
        "cheerful, lively",
        "Она сегодня бодрая.",
        "She is cheerful today.",
    ),
    "слог": (
        "syllable, sound",
        "Это один слог.",
        "This is one syllable.",
    ),
    "несовершеннолетний": (
        "minor, underage",
        "Он ещё несовершеннолетний.",
        "He is still a minor.",
    ),
    "торт": (
        "cake, torte",
        "Это большой торт.",
        "This is a big cake.",
    ),
    "магнитофон": (
        "tape recorder, cassette recorder",
        "Где мой магнитофон?",
        "Where is my tape recorder?",
    ),
    "гадать": (
        "guess, predict",
        "Не надо гадать.",
        "Do not guess.",
    ),
    "методический": (
        "methodical, methodological",
        "Это методический подход.",
        "This is a methodical approach.",
    ),
    "неважный": (
        "unimportant, insignificant",
        "Это неважный вопрос.",
        "This is an unimportant question.",
    ),
    "оптимизация": (
        "optimization",
        "Нужна оптимизация.",
        "Optimization is needed.",
    ),
    "смешанный": (
        "mixed, blended",
        "Это смешанный тип.",
        "This is a mixed type.",
    ),
    "озаботить": (
        "to concern, to trouble",
        "Это может озаботить меня.",
        "This can concern me.",
    ),
    "пробыть": (
        "to stay, to remain",
        "Я хочу пробыть неделю.",
        "I want to stay a week.",
    ),
    "экс": (
        "ex, ex-boyfriend/girlfriend",
        "Это мой экс.",
        "This is my ex.",
    ),
    "пальма": (
        "palm, palm tree",
        "Пальма высокая.",
        "The palm is tall.",
    ),
    "оскорблять": (
        "to insult, to offend",
        "Не надо оскорблять его.",
        "Do not insult him.",
    ),
    "башка": (
        "head, noggin",
        "У него большая башка.",
        "He has a big head.",
    ),
    "пушистый": (
        "fluffy, furry",
        "Кот очень пушистый.",
        "The cat is very fluffy.",
    ),
    "жадно": (
        "greedily, eagerly",
        "Он жадно это ест.",
        "He eats this greedily.",
    ),
    "молоденький": (
        "young, youthful",
        "Она ещё молоденькая.",
        "She is still young.",
    ),
    "листва": (
        "foliage, leaves",
        "Листва уже здесь.",
        "The foliage is already here.",
    ),
    "выясняться": (
        "to be clarified, to turn out",
        "Всё выясняется сейчас.",
        "Everything is being clarified now.",
    ),
    "провокация": (
        "provocation, incitement",
        "Это явная провокация.",
        "This is a clear provocation.",
    ),
    "оснастить": (
        "equip, outfit",
        "Надо оснастить дом.",
        "We must equip the house.",
    ),
    "реалия": (
        "reality, realities",
        "Это важная реалия.",
        "This is an important reality.",
    ),
    "речной": (
        "river, fluvial",
        "Это речной порт.",
        "This is a river port.",
    ),
    "культурно": (
        "culturally",
        "Мы культурно разные.",
        "We are culturally different.",
    ),
    "ориентир": (
        "landmark, reference point",
        "Это важный ориентир.",
        "This is an important landmark.",
    ),
    "приоритетный": (
        "priority, preferential",
        "Это приоритетный вопрос.",
        "This is a priority question.",
    ),
    "веселиться": (
        "have fun, enjoy oneself",
        "Они хотят веселиться.",
        "They want to have fun.",
    ),
    "пятка": (
        "heel",
        "У меня болит пятка.",
        "My heel hurts.",
    ),
    "извне": (
        "from outside, externally",
        "Это пришло извне.",
        "This came from outside.",
    ),
    "комсомолец": (
        "Komsomol member, Young Communist",
        "Он был комсомольцем.",
        "He was a Komsomol member.",
    ),
    "самостоятельность": (
        "independence, self-reliance",
        "Мне нужна самостоятельность.",
        "I need independence.",
    ),
    "сочинить": (
        "compose, create",
        "Я хочу сочинить песню.",
        "I want to compose a song.",
    ),
    "слиться": (
        "merge, blend",
        "Они хотят слиться.",
        "They want to merge.",
    ),
    "национализм": (
        "nationalism, chauvinism",
        "Это опасный национализм.",
        "This is dangerous nationalism.",
    ),
    "развитой": (
        "developed, advanced",
        "Это развитой город.",
        "This is a developed city.",
    ),
    "подписание": (
        "signing, signature",
        "Подписание завтра.",
        "The signing is tomorrow.",
    ),
    "раскрытие": (
        "disclosure, revelation",
        "Это полное раскрытие.",
        "This is a full disclosure.",
    ),
    "эпидемия": (
        "epidemic, outbreak",
        "Эпидемия уже здесь.",
        "The epidemic is already here.",
    ),
    "провайдер": (
        "provider, carrier",
        "Это наш провайдер.",
        "This is our provider.",
    ),
    "линейка": (
        "ruler, line",
        "Линейка на столе.",
        "The ruler is on the table.",
    ),
    "заблудиться": (
        "to get lost, to lose one's way",
        "Здесь легко заблудиться.",
        "It is easy to get lost here.",
    ),
    "дремать": (
        "doze, nap",
        "Я хочу дремать.",
        "I want to doze.",
    ),
    "дверной": (
        "door, door-related",
        "Это дверной ключ.",
        "This is a door key.",
    ),
    "впасть": (
        "fall into, sink",
        "Он может впасть в сон.",
        "He can fall into sleep.",
    ),
    "великолепно": (
        "magnificent, splendid",
        "Это великолепно.",
        "This is magnificent.",
    ),
    "укрыться": (
        "to take shelter, to hide",
        "Надо укрыться здесь.",
        "We must take shelter here.",
    ),
    "талия": (
        "waist, waistline",
        "У неё тонкая талия.",
        "She has a thin waist.",
    ),
    "показательный": (
        "demonstrative, indicative",
        "Это показательный пример.",
        "This is a demonstrative example.",
    ),
    "электроника": (
        "electronics, electronic equipment",
        "Я люблю электронику.",
        "I love electronics.",
    ),
    "усадьба": (
        "estate, manor",
        "Это старая усадьба.",
        "This is an old estate.",
    ),
    "лекарственный": (
        "medicinal, pharmaceutical",
        "Это лекарственное растение.",
        "This is a medicinal plant.",
    ),
    "бомж": (
        "homeless person, bum",
        "Там стоит бомж.",
        "A homeless person stands there.",
    ),
    "ненормальный": (
        "abnormal, not normal",
        "Это ненормальный человек.",
        "This is an abnormal person.",
    ),
    "воплотить": (
        "embody, incarnate",
        "Надо воплотить идею.",
        "We must embody the idea.",
    ),
    "нравственность": (
        "morality, ethics",
        "Это важная нравственность.",
        "This is important morality.",
    ),
    "австрийский": (
        "Austrian",
        "Это австрийский город.",
        "This is an Austrian city.",
    ),
    "хребет": (
        "ridge, spine",
        "Хребет высокий.",
        "The ridge is high.",
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
