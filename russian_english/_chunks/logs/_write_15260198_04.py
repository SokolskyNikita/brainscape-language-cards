import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from brainscape import answer_lemma_from_card, card_write_payload, cards_from_path, lemma_from_card
from russian_english._chunk_io import rewrite_chunk

PACK = REPO / "russian_english"

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
    "one", "onto", "dont", "doesnt", "lets", "ill", "dont",
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
    "во", "всё", "все", "всех", "всю", "весь", "двоих", "слишком", "сам", "самом",
    "из-за", "изза", "хорошо", "давай", "скоро", "часто", "один", "одна", "одно",
    "надо", "мне", "нас",
}

allow_en = {
    line.strip().lower()
    for line in (PACK / "_vocab" / "allow_en_15260198.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_ru = {
    line.strip().replace("ё", "е").lower()
    for line in (PACK / "_vocab" / "allow_ru_15260198.txt").read_text(encoding="utf-8").splitlines()
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
    "sat": "sit", "felt": "feel", "kept": "keep", "fell": "fall",
    "knew": "know", "ran": "run", "thought": "think", "chose": "choose",
    "drove": "drive", "won": "win", "caught": "catch", "taught": "teach",
    "froze": "freeze", "burns": "burn", "grows": "grow", "looks": "look",
    "thinks": "think", "speaks": "speak", "takes": "take",
}

IRREGULAR_RU = {
    "может": "мочь", "могу": "мочь", "можем": "мочь",
    "хочу": "хотеть", "хочет": "хотеть", "хотим": "хотеть",
    "вижу": "видеть", "видишь": "видеть", "видит": "видеть",
    "знаю": "знать", "знает": "знать", "живу": "жить", "живет": "жить",
    "шла": "идти", "шел": "идти", "шли": "идти",
    "идет": "идти", "идем": "идти", "идёт": "идти",
    "стал": "стать", "стала": "стать", "стали": "стать",
    "взял": "взять", "взяла": "взять",
    "стоит": "стоять", "стоят": "стоять", "стою": "стоять",
    "сидим": "сидеть", "сидит": "сидеть",
    "сказал": "сказать", "сказала": "сказать",
    "пришло": "прийти", "пришла": "прийти", "пришел": "прийти",
    "решил": "решить",
    "нужен": "нужный", "нужна": "нужный",
    "руку": "рука", "руки": "рука",
    "книг": "книга", "книги": "книга",
}

RU_ENDINGS = (
    "ами", "ями", "ого", "его", "ому", "ему", "ыми", "ими", "ой", "ей", "ом",
    "ем", "ах", "ях", "ам", "ям", "ов", "ев", "ую", "юю", "ая", "яя",
    "ое", "ее", "ые", "ие", "ый", "ий", "а", "я", "у", "ю", "е", "и",
    "ы", "о", "ь",
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
        if any(
            a.startswith(stem) or stem.startswith(a)
            for a in allow_ru
            if len(a) >= 4 and len(stem) >= 4
        ):
            return True
    return False


def _tokens(text: str) -> list[str]:
    return re.findall(r"[A-Za-zА-Яа-яЁё'-]+", text)


stats = rewrite_chunk(
    Path("russian_english/_chunks/deck_15260198_04.csv"),
    {
        "прижать": ("press, clamp", "Надо прижать кнопку.", "You need to press the button."),
        "опера": ("opera", "Это опера.", "This is an opera."),
        "сознательный": (
            "conscious, deliberate",
            "Он сознательный человек.",
            "He is a conscious person.",
        ),
        "госпожа": ("Madam, Mrs.", "Госпожа уже дома.", "Madam is already home."),
        "самоубийство": ("suicide", "Это было самоубийство.", "That was suicide."),
        "прибегать": (
            "resort to",
            "Надо прибегать к помощи.",
            "We need to resort to help.",
        ),
        "ранг": ("rank, grade", "У него высокий ранг.", "He has a high rank."),
        "мыло": ("soap", "Надо купить мыло.", "I need to buy soap."),
        "поэма": ("poem, epic", "Это длинная поэма.", "This is a long poem."),
        "коррупция": ("corruption", "Коррупция уже есть.", "Corruption is already here."),
        "оркестр": ("orchestra, band", "Это хороший оркестр.", "This is a good orchestra."),
        "запрещать": (
            "prohibit, ban",
            "Закон будет запрещать это.",
            "The law will prohibit this.",
        ),
        "шарик": ("ball, little ball", "Это красный шарик.", "This is a red ball."),
        "жир": ("fat, grease", "Много жира.", "There is much fat."),
        "газовый": ("gas", "Это газовый огонь.", "This is a gas fire."),
        "грохот": ("rumble, roar", "Это громкий грохот.", "This is a loud rumble."),
        "орбита": ("orbit, trajectory", "Это высокая орбита.", "This is a high orbit."),
        "освободиться": (
            "get free, be released",
            "Надо освободиться.",
            "I need to get free.",
        ),
        "финский": ("Finnish", "Это финский язык.", "This is the Finnish language."),
        "подразумевать": (
            "imply, presuppose",
            "Что это будет подразумевать?",
            "What will this imply?",
        ),
        "палочка": ("stick, rod", "Это длинная палочка.", "This is a long stick."),
        "вручить": (
            "hand over, present",
            "Надо вручить письмо.",
            "I need to hand over the letter.",
        ),
        "беременный": (
            "pregnant, expectant",
            "У неё беременный вид.",
            "She has a pregnant look.",
        ),
        "пожаловаться": ("complain", "Надо пожаловаться.", "I need to complain."),
        "превращать": (
            "transform, convert",
            "Он будет превращать золото.",
            "He will transform gold.",
        ),
        "направо": (
            "to the right, rightward",
            "Надо идти направо.",
            "You need to go to the right.",
        ),
        "упорно": (
            "stubbornly, persistently",
            "Надо упорно работать.",
            "You need to work stubbornly.",
        ),
        "аромат": (
            "aroma, fragrance",
            "Какой аромат на кухне!",
            "What an aroma in the kitchen!",
        ),
        "подбородок": ("chin", "У него большой подбородок.", "He has a big chin."),
        "триста": (
            "three hundred",
            "У меня триста книг.",
            "I have three hundred books.",
        ),
        "осудить": ("condemn", "Надо осудить это.", "We need to condemn this."),
        "надевать": (
            "put on, wear",
            "Надо надевать платье.",
            "You need to put on a dress.",
        ),
        "суп": ("soup, broth", "Это хороший суп.", "This is good soup."),
        "объятие": ("embrace, hug", "Это долгое объятие.", "This is a long embrace."),
        "полночь": ("midnight", "Это уже полночь.", "It is already midnight."),
        "вытянуть": (
            "pull out, stretch",
            "Надо вытянуть руку.",
            "You need to pull out the hand.",
        ),
        "буря": ("storm", "Это сильная буря.", "This is a strong storm."),
        "разочарование": (
            "disappointment",
            "Это большое разочарование.",
            "This is a big disappointment.",
        ),
        "око": ("eye", "Это моё око.", "This is my eye."),
        "совершенствование": (
            "improvement",
            "Это важное совершенствование.",
            "This is an important improvement.",
        ),
        "общежитие": (
            "dormitory, hostel",
            "Это наше общежитие.",
            "This is our dormitory.",
        ),
        "упустить": (
            "miss, let slip",
            "Не надо упустить шанс.",
            "Do not miss the chance.",
        ),
        "аналитик": ("analyst", "Это наш аналитик.", "This is our analyst."),
        "гражданство": (
            "citizenship, nationality",
            "Нам надо гражданство.",
            "We need citizenship.",
        ),
        "разрабатывать": (
            "develop, elaborate",
            "Они будут разрабатывать план.",
            "They will develop a plan.",
        ),
        "обитатель": (
            "inhabitant, dweller",
            "Это обитатель леса.",
            "This is an inhabitant of the forest.",
        ),
        "прочный": ("durable, strong", "Этот стол прочный.", "This table is durable."),
        "соседка": (
            "neighbor, female neighbor",
            "Моя соседка дома.",
            "My neighbor is at home.",
        ),
        "фильтр": ("filter, strainer", "Где мой фильтр?", "Where is my filter?"),
        "должный": ("due, proper", "Это должный порядок.", "This is the due order."),
        "тронуть": ("touch, move", "Можно тронуть стол?", "Can I touch the table?"),
        "ерунда": ("nonsense, rubbish", "Это полная ерунда.", "This is complete nonsense."),
        "резать": ("cut, slice", "Надо резать хлеб.", "You need to cut the bread."),
        "проникать": (
            "penetrate, infiltrate",
            "Свет будет проникать сюда.",
            "Light will penetrate here.",
        ),
        "мужество": ("courage, bravery", "У неё есть мужество.", "She has courage."),
        "шофер": ("driver, chauffeur", "Шофер уже дома.", "The driver is already home."),
        "параллельно": (
            "parallel, concurrently",
            "Надо идти параллельно.",
            "You need to go parallel.",
        ),
        "провал": ("failure, collapse", "Это полный провал.", "This is a complete failure."),
        "задержка": ("delay", "Это долгая задержка.", "This is a long delay."),
        "вправе": (
            "entitled, authorized",
            "Вы вправе знать.",
            "You are entitled to know.",
        ),
        "животный": ("animal, creature", "Это животный жир.", "This is animal fat."),
        "физически": (
            "physically",
            "Он физически сильный.",
            "He is physically strong.",
        ),
        "вопль": ("scream, howl", "Это её вопль.", "This is her scream."),
        "ура": ("hurray, hurrah", "Ура, мы дома!", "Hurray, we are home!"),
        "физик": ("physicist", "Это наш физик.", "This is our physicist."),
        "клясться": ("swear, vow", "Не надо клясться.", "Do not swear."),
        "стабильный": ("stable, steady", "Это стабильный план.", "This is a stable plan."),
        "жирный": ("fat", "Этот суп жирный.", "This soup is fat."),
        "товарный": (
            "goods, commodity",
            "Это товарный поезд.",
            "This is a goods train.",
        ),
        "недолго": ("not long, briefly", "Это недолго.", "This is not long."),
        "знакомиться": ("meet, get acquainted", "Надо знакомиться.", "We need to meet."),
        "сопротивляться": (
            "resist, oppose",
            "Надо сопротивляться.",
            "We need to resist.",
        ),
        "нежно": (
            "gently, tenderly",
            "Надо говорить нежно.",
            "You need to speak gently.",
        ),
        "гладкий": ("smooth, sleek", "Этот камень гладкий.", "This stone is smooth."),
        "призрак": (
            "ghost, phantom",
            "Призрак в старом доме.",
            "The ghost is in the old house.",
        ),
        "провожать": (
            "see off, escort",
            "Надо провожать друга.",
            "We need to see off a friend.",
        ),
        "условный": (
            "conditional, hypothetical",
            "Это условный знак.",
            "This is a conditional sign.",
        ),
        "регулярный": (
            "regular, periodic",
            "Это регулярный поезд.",
            "This is a regular train.",
        ),
        "мышка": ("mouse, little mouse", "Мышка в доме.", "The mouse is in the house."),
        "адекватный": (
            "adequate, appropriate",
            "Это адекватный ответ.",
            "This is an adequate answer.",
        ),
        "ай": ("ouch, ow", "Ай, моя рука!", "Ouch, my hand!"),
        "таможенный": (
            "customs",
            "Это таможенный контроль.",
            "This is customs control.",
        ),
        "захватывать": (
            "capture, captivate",
            "Они будут захватывать город.",
            "They will capture the city.",
        ),
        "внешне": (
            "externally, outwardly",
            "Она внешне спокойная.",
            "She is calm externally.",
        ),
        "экскурсия": (
            "excursion, tour",
            "Завтра будет экскурсия.",
            "Tomorrow there will be an excursion.",
        ),
        "семя": ("seed", "Это маленькое семя.", "This is a small seed."),
        "супер": ("super, superb", "Это супер!", "This is super!"),
        "продолжительность": (
            "duration, length",
            "Какая продолжительность фильма?",
            "What is the duration of the movie?",
        ),
        "украшение": (
            "decoration, ornament",
            "Это красивое украшение.",
            "This is a beautiful decoration.",
        ),
        "уменьшение": (
            "reduction, decrease",
            "Это уменьшение.",
            "This is a reduction.",
        ),
        "стройный": ("slim, slender", "Он стройный человек.", "He is a slim person."),
        "публиковать": (
            "publish, post",
            "Они будут публиковать статью.",
            "They will publish the article.",
        ),
        "депрессия": ("depression", "У неё депрессия.", "She has depression."),
        "энергетика": (
            "power industry, energy sector",
            "Нам нужна энергетика.",
            "We need the power industry.",
        ),
        "радикальный": (
            "radical, extreme",
            "Это радикальный план.",
            "This is a radical plan.",
        ),
        "справляться": ("cope, manage", "Надо справляться.", "You need to cope."),
        "уделять": (
            "devote, allocate",
            "Надо уделять время работе.",
            "You need to devote time to work.",
        ),
        "лишиться": (
            "lose, be deprived of",
            "Не надо лишиться этого.",
            "Do not lose this.",
        ),
        "сериал": (
            "TV series, serial",
            "Это хороший сериал.",
            "This is a good TV series.",
        ),
        "разорвать": (
            "tear, break",
            "Надо разорвать письмо.",
            "You need to tear the letter.",
        ),
    },
)
print(stats)

dest = Path(stats["path"])
cards = cards_from_path(dest)
leftover = []
for i, card in enumerate(cards, 1):
    lemma = lemma_from_card(card)
    gloss = answer_lemma_from_card(card)
    payload = card_write_payload(card)
    ru = payload["question"].split("## Footnote")[-1].strip()
    en = payload["answer"].split("## Footnote")[-1].strip()
    ru_l = ru.replace("ё", "е").lower()
    if lemma.replace("ё", "е").lower() not in ru_l:
        leftover.append(f"{i} LEMMA {lemma} :: {ru}")
    gloss_l = re.sub(r"^(to |the |a |an )", "", gloss.split(",")[0].strip().lower())
    gloss_toks = [g for g in re.split(r"\s+", gloss_l) if g]
    if gloss_toks and not any(g in en.lower() for g in gloss_toks):
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
