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
        Path("russian_english/_chunks/deck_15260218_04.csv"),
        {
            "разместиться": (
                "settle in",
                "Нам нужно разместиться здесь.",
                "We need to settle in here.",
            ),
            "археолог": (
                "archaeologist",
                "Где археолог?",
                "Where is the archaeologist?",
            ),
            "осесть": (
                "settle",
                "Пыль должна осесть.",
                "The dust must settle.",
            ),
            "диаграмма": (
                "diagram",
                "Где диаграмма?",
                "Where is the diagram?",
            ),
            "распределить": (
                "distribute",
                "Надо распределить хлеб.",
                "We need to distribute the bread.",
            ),
            "приподняться": (
                "rise",
                "Ему надо приподняться.",
                "He needs to rise.",
            ),
            "конница": (
                "cavalry",
                "Конница уже в поле.",
                "The cavalry is already in the field.",
            ),
            "раскопка": (
                "excavation",
                "Где раскопка?",
                "Where is the excavation?",
            ),
            "своевременно": (
                "timely",
                "Он дал ответ своевременно.",
                "He gave a timely answer.",
            ),
            "выброс": (
                "emission",
                "Выброс с завода большой.",
                "The emission from the factory is big.",
            ),
            "крылатый": (
                "winged",
                "Это крылатый конь.",
                "This is a winged horse.",
            ),
            "роса": (
                "dew",
                "Роса на траве.",
                "There is dew on the grass.",
            ),
            "геополитический": (
                "geopolitical",
                "Это геополитический вопрос.",
                "This is a geopolitical question.",
            ),
            "пакетик": (
                "packet",
                "Пакетик на столе.",
                "The packet is on the table.",
            ),
            "ярлык": (
                "label",
                "Где ярлык?",
                "Where is the label?",
            ),
            "беспощадный": (
                "ruthless",
                "Он беспощадный враг.",
                "He is a ruthless enemy.",
            ),
            "вывозить": (
                "export",
                "Они будут вывозить товар.",
                "They will export the goods.",
            ),
            "прививка": (
                "vaccination",
                "Мне нужна прививка.",
                "I need a vaccination.",
            ),
            "воздержаться": (
                "abstain",
                "Я хочу воздержаться.",
                "I want to abstain.",
            ),
            "разведывательный": (
                "reconnaissance",
                "Это разведывательная миссия.",
                "This is a reconnaissance mission.",
            ),
            "ответчик": (
                "defendant",
                "Ответчик уже в суде.",
                "The defendant is already in court.",
            ),
            "цезарь": (
                "Caesar",
                "Цезарь был генералом.",
                "Caesar was a general.",
            ),
            "бушевать": (
                "rage",
                "Буря будет бушевать.",
                "The storm will rage.",
            ),
            "серийный": (
                "serial",
                "Это серийное производство.",
                "This is serial production.",
            ),
            "чинить": (
                "repair",
                "Надо чинить часы.",
                "I need to repair the clock.",
            ),
            "изолировать": (
                "isolate",
                "Надо изолировать район.",
                "We need to isolate the area.",
            ),
            "убеждаться": (
                "make sure",
                "Надо убеждаться в этом.",
                "You need to make sure of this.",
            ),
            "контингент": (
                "contingent",
                "Контингент уже здесь.",
                "The contingent is already here.",
            ),
            "рацион": (
                "ration",
                "Какой у тебя рацион?",
                "What is your ration?",
            ),
            "подпольный": (
                "underground",
                "Это подпольная газета.",
                "This is an underground newspaper.",
            ),
            "пьянка": (
                "binge",
                "У нас была пьянка.",
                "We had a binge.",
            ),
            "всецело": (
                "wholly",
                "Она всецело за нас.",
                "She is wholly for us.",
            ),
            "настраивать": (
                "adjust",
                "Надо настраивать радио.",
                "I need to adjust the radio.",
            ),
            "экспортный": (
                "export",
                "Это экспортная машина.",
                "This is an export car.",
            ),
            "азарт": (
                "excitement",
                "Его азарт большой.",
                "His excitement is big.",
            ),
            "болезненно": (
                "painfully",
                "Это было болезненно.",
                "This was painfully hard.",
            ),
            "мах": (
                "swing",
                "Он сделал мах.",
                "He made a swing.",
            ),
            "самолюбие": (
                "vanity",
                "У него большое самолюбие.",
                "He has great vanity.",
            ),
            "венгерский": (
                "Hungarian",
                "Это венгерский язык.",
                "This is the Hungarian language.",
            ),
            "кашель": (
                "cough",
                "У него кашель.",
                "He has a cough.",
            ),
            "вписать": (
                "write in",
                "Надо вписать имя.",
                "You need to write in the name.",
            ),
            "ограбить": (
                "rob",
                "Они хотят ограбить банк.",
                "They want to rob the bank.",
            ),
            "иммунитет": (
                "immunity",
                "У меня есть иммунитет.",
                "I have immunity.",
            ),
            "фигурировать": (
                "figure",
                "Он будет фигурировать в деле.",
                "He will figure in the case.",
            ),
            "обвести": (
                "circle",
                "Надо обвести слово.",
                "You need to circle the word.",
            ),
            "миллионер": (
                "millionaire",
                "Он миллионер.",
                "He is a millionaire.",
            ),
            "ипотечный": (
                "mortgage",
                "Это ипотечный кредит.",
                "This is a mortgage loan.",
            ),
            "высокопоставленный": (
                "high-ranking",
                "Это высокопоставленный чиновник.",
                "This is a high-ranking official.",
            ),
            "обком": (
                "regional committee",
                "Обком уже здесь.",
                "The regional committee is already here.",
            ),
            "закусить": (
                "snack",
                "Надо закусить.",
                "I need to snack.",
            ),
            "реализм": (
                "realism",
                "Это чистый реализм.",
                "This is pure realism.",
            ),
            "напевать": (
                "hum",
                "Она будет напевать.",
                "She will hum.",
            ),
            "вдох": (
                "breath",
                "Сделай вдох.",
                "Take a breath.",
            ),
            "наследственный": (
                "hereditary",
                "Это наследственная болезнь.",
                "This is a hereditary disease.",
            ),
            "коврик": (
                "mat",
                "Обувь на коврике.",
                "The shoes are on the mat.",
            ),
            "автограф": (
                "autograph",
                "Мне нужен автограф.",
                "I need an autograph.",
            ),
            "переселение": (
                "resettlement",
                "Переселение уже идет.",
                "The resettlement already started.",
            ),
            "отрыв": (
                "gap",
                "У нас большой отрыв.",
                "We have a big gap.",
            ),
            "переглянуться": (
                "exchange glances",
                "Они хотят переглянуться.",
                "They want to exchange glances.",
            ),
            "архиепископ": (
                "archbishop",
                "Архиепископ в храме.",
                "The archbishop is in the temple.",
            ),
            "искусный": (
                "skilled",
                "Он искусный мастер.",
                "He is a skilled master.",
            ),
            "теорема": (
                "theorem",
                "Это большая теорема.",
                "This is a big theorem.",
            ),
            "помиловать": (
                "pardon",
                "Царь хочет помиловать его.",
                "The king wants to pardon him.",
            ),
            "вексель": (
                "promissory note",
                "Где вексель?",
                "Where is the promissory note?",
            ),
            "покурить": (
                "smoke",
                "Я хочу покурить.",
                "I want to smoke.",
            ),
            "конкурентоспособность": (
                "competitiveness",
                "Нам нужна конкурентоспособность.",
                "We need competitiveness.",
            ),
            "несовместимый": (
                "incompatible",
                "Эти виды несовместимы.",
                "These kinds are incompatible.",
            ),
            "разуметься": (
                "of course",
                "Это, разумеется, правда.",
                "This is, of course, true.",
            ),
            "бесспорный": (
                "indisputable",
                "Это бесспорный факт.",
                "This is an indisputable fact.",
            ),
            "синагога": (
                "synagogue",
                "Мы в синагоге.",
                "We are in the synagogue.",
            ),
            "лаять": (
                "bark",
                "Собака будет лаять.",
                "The dog will bark.",
            ),
            "стиснуть": (
                "clench",
                "Надо стиснуть рот.",
                "You need to clench your mouth.",
            ),
            "мгла": (
                "gloom",
                "Мгла над лесом.",
                "There is gloom over the forest.",
            ),
            "неприемлемый": (
                "unacceptable",
                "Это неприемлемо.",
                "This is unacceptable.",
            ),
            "бомбардировка": (
                "bombing",
                "Бомбардировка уже идет.",
                "The bombing already started.",
            ),
            "отдаться": (
                "devote oneself",
                "Она хочет отдаться работе.",
                "She wants to devote herself to work.",
            ),
            "алюминиевый": (
                "aluminum",
                "Это алюминиевый стол.",
                "This is an aluminum table.",
            ),
            "окрестный": (
                "surrounding",
                "Окрестный лес тих.",
                "The surrounding forest is quiet.",
            ),
            "сыпаться": (
                "pour",
                "Песок будет сыпаться.",
                "The sand will pour.",
            ),
            "идентифицировать": (
                "identify",
                "Надо идентифицировать его.",
                "We need to identify him.",
            ),
            "впустить": (
                "let in",
                "Надо впустить кота.",
                "We need to let the cat in.",
            ),
            "отчество": (
                "patronymic",
                "Какое у него отчество?",
                "What is his patronymic?",
            ),
            "навещать": (
                "visit",
                "Я буду навещать мать.",
                "I will visit my mother.",
            ),
            "дебаты": (
                "debate",
                "Дебаты уже идут.",
                "The debate already started.",
            ),
            "одарить": (
                "gift",
                "Он хочет одарить её.",
                "He wants to gift her.",
            ),
            "задушить": (
                "strangle",
                "Он хочет задушить врага.",
                "He wants to strangle the enemy.",
            ),
            "исказить": (
                "distort",
                "Нельзя исказить слово.",
                "You cannot distort the word.",
            ),
            "лидировать": (
                "lead",
                "Она будет лидировать.",
                "She will lead.",
            ),
            "предаваться": (
                "indulge",
                "Не надо предаваться страху.",
                "Do not indulge in fear.",
            ),
            "подмосковный": (
                "near Moscow",
                "Это подмосковный дом.",
                "This is a house near Moscow.",
            ),
            "преувеличение": (
                "exaggeration",
                "Это преувеличение.",
                "This is an exaggeration.",
            ),
            "местонахождение": (
                "location",
                "Местонахождение неизвестно.",
                "The location is unknown.",
            ),
            "питательный": (
                "nutritious",
                "Это питательная еда.",
                "This is nutritious food.",
            ),
            "торжествовать": (
                "triumph",
                "Мы хотим торжествовать.",
                "We want to triumph.",
            ),
            "комок": (
                "lump",
                "Комок в горле.",
                "There is a lump in the throat.",
            ),
            "хлопок": (
                "cotton",
                "Это хлопок.",
                "This is cotton.",
            ),
            "докладчик": (
                "speaker",
                "Докладчик уже здесь.",
                "The speaker is already here.",
            ),
            "солома": (
                "straw",
                "Корова на соломе.",
                "The cow is on the straw.",
            ),
            "притча": (
                "parable",
                "Это старая притча.",
                "This is an old parable.",
            ),
            "задумчивый": (
                "thoughtful",
                "Он задумчивый.",
                "He is thoughtful.",
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
    "one", "onto", "dont", "doesnt", "lets", "don't", "again", "cannot",
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
    "надо", "пора", "какой", "какая", "какие", "кого", "нельзя",
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
    "says": "say", "works": "work", "needs": "need", "wants": "want",
    "kinds": "kind", "shoes": "shoe",
}

IRREGULAR_RU = {
    "идет": "идти", "иду": "идти", "шел": "идти", "шла": "идти", "шли": "идти",
    "идут": "идти",
    "нужна": "нужный", "нужен": "нужный", "нужно": "нужный",
    "хочу": "хотеть", "хочет": "хотеть", "хотим": "хотеть", "хотят": "хотеть",
    "могу": "мочь", "может": "мочь", "можем": "мочь",
    "дай": "дать", "дали": "дать", "дал": "дать",
    "любит": "любить", "люблю": "любить",
    "говорит": "говорить", "сказал": "сказать",
    "сделал": "сделать", "сделай": "сделать",
    "тих": "тихий",
    "них": "они", "будем": "быть",
    "воду": "вода", "чая": "чай", "зону": "зона",
    "игры": "игра", "рукой": "рука", "руку": "рука",
    "новая": "новый", "хлопка": "хлопок",
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


dest = REPO / "russian_english/_chunks/fixed/deck_15260218_04.csv"
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
