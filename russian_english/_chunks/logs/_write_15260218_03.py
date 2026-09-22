import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from brainscape import answer_lemma_from_card, card_write_payload, cards_from_path, lemma_from_card
from russian_english._chunk_io import rewrite_chunk

print(
    rewrite_chunk(
        Path("russian_english/_chunks/deck_15260218_03.csv"),
        {
            "позорный": (
                "disgraceful",
                "Это позорный случай.",
                "This is a disgraceful case.",
            ),
            "манер": (
                "manner",
                "У него нет манер.",
                "He has no manners.",
            ),
            "клоун": (
                "clown",
                "Где клоун?",
                "Where is the clown?",
            ),
            "рушиться": (
                "collapse",
                "Дом будет рушиться.",
                "The house will collapse.",
            ),
            "доходность": (
                "yield",
                "Какая доходность?",
                "What is the yield?",
            ),
            "проскочить": (
                "slip through",
                "Он проскочил.",
                "He slipped through.",
            ),
            "мигать": (
                "blink",
                "Свет мигает.",
                "The light blinks.",
            ),
            "бесполезно": (
                "useless",
                "Это бесполезно.",
                "This is useless.",
            ),
            "лопатка": (
                "spatula",
                "Где лопатка?",
                "Where is the spatula?",
            ),
            "неуклюжий": (
                "clumsy",
                "Он неуклюжий.",
                "He is clumsy.",
            ),
            "приостановить": (
                "suspend",
                "Они приостановили работу.",
                "They suspended the work.",
            ),
            "реорганизация": (
                "reorganization",
                "Нам нужна реорганизация.",
                "We need a reorganization.",
            ),
            "настоять": (
                "insist",
                "Я настою на этом.",
                "I will insist on this.",
            ),
            "нездоровый": (
                "unhealthy",
                "У него нездоровый вид.",
                "He has an unhealthy look.",
            ),
            "святыня": (
                "shrine",
                "Это старая святыня.",
                "This is an old shrine.",
            ),
            "неохотно": (
                "reluctantly",
                "Он неохотно говорит да.",
                "He reluctantly says yes.",
            ),
            "кризисный": (
                "crisis",
                "Это кризисный момент.",
                "This is a crisis moment.",
            ),
            "смыть": (
                "wash off",
                "Надо смыть это.",
                "Need to wash this off.",
            ),
            "интерпретировать": (
                "interpret",
                "Как это интерпретировать?",
                "How to interpret this?",
            ),
            "проститься": (
                "say goodbye",
                "Пора проститься.",
                "Time to say goodbye.",
            ),
            "детально": (
                "in detail",
                "Говори детально.",
                "Speak in detail.",
            ),
            "дымиться": (
                "smoke",
                "Дом дымится.",
                "The house smokes.",
            ),
            "крюк": (
                "hook",
                "Вот крюк.",
                "Here is the hook.",
            ),
            "блуждать": (
                "wander",
                "Не блуждай тут.",
                "Don't wander here.",
            ),
            "поощрение": (
                "encouragement",
                "Мне нужно поощрение.",
                "I need encouragement.",
            ),
            "туловище": (
                "torso",
                "У него сильное туловище.",
                "He has a strong torso.",
            ),
            "гектар": (
                "hectare",
                "Это один гектар.",
                "This is one hectare.",
            ),
            "одиночный": (
                "solitary",
                "Это одиночная камера.",
                "This is a solitary cell.",
            ),
            "вещать": (
                "broadcast",
                "Они вещают новости.",
                "They broadcast the news.",
            ),
            "магистр": (
                "master",
                "Он уже магистр.",
                "He is already a master.",
            ),
            "цветочек": (
                "little flower",
                "Вот цветочек.",
                "Here is a little flower.",
            ),
            "формулировать": (
                "formulate",
                "Надо формулировать это.",
                "You need to formulate this.",
            ),
            "папироса": (
                "cigarette",
                "Дай папиросу.",
                "Give me a cigarette.",
            ),
            "блядь": (
                "fuck",
                "Блядь, опять нет.",
                "Fuck, no again.",
            ),
            "подталкивать": (
                "push",
                "Не подталкивай меня.",
                "Don't push me.",
            ),
            "вакуум": (
                "vacuum",
                "Это полный вакуум.",
                "This is a complete vacuum.",
            ),
            "разыгрывать": (
                "play",
                "Не разыгрывай меня.",
                "Don't play me.",
            ),
            "записаться": (
                "sign up",
                "Я хочу записаться.",
                "I want to sign up.",
            ),
            "тошнота": (
                "nausea",
                "У меня тошнота.",
                "I have nausea.",
            ),
            "излучать": (
                "radiate",
                "Она излучает свет.",
                "She radiates light.",
            ),
            "психиатрический": (
                "psychiatric",
                "Это психиатрическая больница.",
                "This is a psychiatric hospital.",
            ),
            "неуместный": (
                "inappropriate",
                "Это неуместный вопрос.",
                "This is an inappropriate question.",
            ),
            "сурово": (
                "harshly",
                "Он сурово говорит нет.",
                "He harshly says no.",
            ),
            "нанесение": (
                "application",
                "Это нанесение краски.",
                "This is an application of paint.",
            ),
            "расплачиваться": (
                "pay",
                "Надо расплачиваться.",
                "We need to pay.",
            ),
            "отраслевой": (
                "industry",
                "Это отраслевой рынок.",
                "This is an industry market.",
            ),
            "односторонний": (
                "one-sided",
                "Это одностороннее решение.",
                "This is a one-sided decision.",
            ),
            "петровский": (
                "Petrovsky",
                "Это петровский дворец.",
                "This is a Petrovsky palace.",
            ),
            "кооператив": (
                "cooperative",
                "Это наш кооператив.",
                "This is our cooperative.",
            ),
            "нанимать": (
                "hire",
                "Нам надо нанимать.",
                "We need to hire.",
            ),
            "сокровенный": (
                "cherished",
                "Это сокровенный план.",
                "This is a cherished plan.",
            ),
            "привод": (
                "drive",
                "Привод не работает.",
                "The drive does not work.",
            ),
            "свистеть": (
                "whistle",
                "Он любит свистеть.",
                "He likes to whistle.",
            ),
            "пионерский": (
                "Pioneer",
                "Это пионерский лагерь.",
                "This is a Pioneer camp.",
            ),
            "холст": (
                "canvas",
                "Это чистый холст.",
                "This is a clean canvas.",
            ),
            "концерн": (
                "concern",
                "Это большой концерн.",
                "This is a big concern.",
            ),
            "завтракать": (
                "have breakfast",
                "Пора завтракать.",
                "Time to have breakfast.",
            ),
            "обогнать": (
                "overtake",
                "Надо обогнать их.",
                "We need to overtake them.",
            ),
            "контроллер": (
                "controller",
                "Где контроллер?",
                "Where is the controller?",
            ),
            "бесплодный": (
                "barren",
                "Это бесплодная земля.",
                "This is barren land.",
            ),
            "приморский": (
                "seaside",
                "Это приморский город.",
                "This is a seaside town.",
            ),
            "оттолкнуть": (
                "push away",
                "Он оттолкнул меня.",
                "He pushed me away.",
            ),
            "раскладывать": (
                "lay out",
                "Она раскладывает карты.",
                "She lays out the cards.",
            ),
            "рождаемость": (
                "birth rate",
                "Какая рождаемость?",
                "What is the birth rate?",
            ),
            "коттедж": (
                "cottage",
                "Наш коттедж там.",
                "Our cottage is there.",
            ),
            "стекать": (
                "drain",
                "Вода стекает.",
                "The water drains.",
            ),
            "лагерный": (
                "camp",
                "Это лагерная жизнь.",
                "This is camp life.",
            ),
            "знаменитость": (
                "celebrity",
                "Он теперь знаменитость.",
                "He is a celebrity now.",
            ),
            "образовывать": (
                "form",
                "Они образуют круг.",
                "They form a circle.",
            ),
            "шевелить": (
                "move",
                "Он не может шевелить.",
                "He cannot move.",
            ),
            "пропитать": (
                "soak",
                "Надо пропитать хлеб.",
                "Need to soak the bread.",
            ),
            "напрочь": (
                "completely",
                "Он напрочь отказался.",
                "He completely refused.",
            ),
            "сослаться": (
                "refer",
                "Могу сослаться на него.",
                "I can refer to him.",
            ),
            "фигня": (
                "nonsense",
                "Это фигня.",
                "This is nonsense.",
            ),
            "пехотный": (
                "infantry",
                "Это пехотный солдат.",
                "This is an infantry soldier.",
            ),
            "растянуться": (
                "stretch out",
                "Я растянусь на диване.",
                "I will stretch out on the sofa.",
            ),
            "инфаркт": (
                "heart attack",
                "У него инфаркт.",
                "He has a heart attack.",
            ),
            "писательский": (
                "writer's",
                "Это писательский стол.",
                "This is a writer's table.",
            ),
            "жид": (
                "yid",
                "Не говори жид.",
                "Don't say yid.",
            ),
            "физиология": (
                "physiology",
                "Я изучаю физиологию.",
                "I study physiology.",
            ),
            "плодотворный": (
                "fruitful",
                "Это плодотворный день.",
                "This is a fruitful day.",
            ),
            "шашлык": (
                "shashlik",
                "Мы едим шашлык.",
                "We eat shashlik.",
            ),
            "полис": (
                "policy",
                "Где мой полис?",
                "Where is my policy?",
            ),
            "прибрежный": (
                "coastal",
                "Это прибрежный дом.",
                "This is a coastal house.",
            ),
            "бедняк": (
                "poor man",
                "Он бедняк.",
                "He is a poor man.",
            ),
            "хмурый": (
                "gloomy",
                "Он сегодня хмурый.",
                "He is gloomy today.",
            ),
            "правозащитник": (
                "human rights activist",
                "Он правозащитник.",
                "He is a human rights activist.",
            ),
            "богато": (
                "richly",
                "Они богато живут.",
                "They live richly.",
            ),
            "вытянуться": (
                "stretch",
                "Пора вытянуться.",
                "Time to stretch.",
            ),
            "шататься": (
                "stagger",
                "Он шатается.",
                "He staggers.",
            ),
            "поместье": (
                "estate",
                "Это старое поместье.",
                "This is an old estate.",
            ),
            "расписать": (
                "paint",
                "Я расписал стену.",
                "I painted the wall.",
            ),
            "порочный": (
                "vicious",
                "Это порочный круг.",
                "This is a vicious circle.",
            ),
            "обаяние": (
                "charm",
                "У неё есть обаяние.",
                "She has charm.",
            ),
            "заполнение": (
                "filling",
                "Нужно заполнение.",
                "Filling is needed.",
            ),
            "трепетать": (
                "tremble",
                "Он трепещет.",
                "He trembles.",
            ),
            "бросок": (
                "throw",
                "Это сильный бросок.",
                "This is a strong throw.",
            ),
            "самарский": (
                "Samara",
                "Это самарский дом.",
                "This is a Samara house.",
            ),
            "чуять": (
                "smell",
                "Собака любит чуять.",
                "The dog loves to smell.",
            ),
            "нырять": (
                "dive",
                "Он любит нырять.",
                "He loves to dive.",
            ),
        },
    )
)

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
    "herself", "himself", "themselves", "myself", "yourself",
    "one", "onto", "dont", "doesnt", "lets", "don't", "again",
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
    "из-за", "изза", "хорошо", "давай", "скоро", "часто", "один", "одна",
    "надо", "пора", "какой", "какая", "какие", "кого",
}

allow_en = {
    line.strip().lower()
    for line in (REPO / "russian_english/_vocab/allow_en_15260218.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_ru = {
    line.strip().replace("ё", "е").lower()
    for line in (REPO / "russian_english/_vocab/allow_ru_15260218.txt").read_text(encoding="utf-8").splitlines()
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
    "forgot": "forget", "refused": "refuse", "likes": "like", "loves": "love",
    "says": "say", "works": "work", "slipped": "slip", "pushed": "push",
    "stretched": "stretch", "painted": "paint", "overtook": "overtake",
    "lives": "live", "drains": "drain", "staggers": "stagger",
    "trembles": "tremble", "blinks": "blink", "smokes": "smoke",
    "radiates": "radiate", "lays": "lay", "smells": "smell",
    "hires": "hire", "forms": "form",
}

IRREGULAR_RU = {
    "идет": "идти", "иду": "идти", "шел": "идти", "шла": "идти", "шли": "идти",
    "нужна": "нужный", "нужен": "нужный", "нужно": "нужный",
    "хочу": "хотеть", "хочет": "хотеть", "хотим": "хотеть",
    "могу": "мочь", "может": "мочь", "можем": "мочь",
    "дай": "дать", "дали": "дать",
    "любит": "любить", "люблю": "любить",
    "говорит": "говорить", "сказал": "сказать",
    "забыл": "забыть", "отказался": "отказаться",
    "живут": "жить", "живет": "жить",
    "едим": "есть",
    "начал": "начать",
    "работает": "работать",
    "чует": "чуять",
    "трепещет": "трепетать",
    "мигает": "мигать",
    "дымится": "дымиться",
    "стекает": "стекать",
    "шатается": "шататься",
    "вещают": "вещать",
    "излучает": "излучать",
    "раскладывает": "раскладывать",
    "образуют": "образовывать",
    "обгонит": "обогнать",
    "проскочил": "проскочить",
    "приостановили": "приостановить",
    "настою": "настоять",
    "оттолкнул": "оттолкнуть",
    "растянусь": "растянуться",
    "расписал": "расписать",
    "смой": "смыть",
    "пропитай": "пропитать",
    "шевели": "шевелить",
    "блуждай": "блуждать",
    "подталкивай": "подталкивать",
    "разыгрывай": "разыгрывать",
}

RU_ENDINGS = (
    "ами", "ями", "ого", "его", "ому", "ему", "ыми", "ими", "ой", "ей", "ом",
    "ем", "ах", "ях", "ам", "ям", "ов", "ев", "ую", "юю", "ая", "яя", "ое",
    "ее", "ые", "ие", "ый", "ий", "а", "я", "у", "ю", "е", "и", "ы", "о", "ь",
)


def _en_ok(word: str) -> bool:
    w = word.lower().replace("'", "")
    if w in allow_en:
        return True
    if IRREGULAR_EN.get(w) in allow_en:
        return True
    if word.lower().endswith("'s") and word.lower()[:-2] in allow_en:
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


dest = REPO / "russian_english/_chunks/fixed/deck_15260218_03.csv"
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
    if gloss_l and gloss_l not in en.lower() and not any(
        g in en.lower() for g in gloss_l.split() if len(g) > 2
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
