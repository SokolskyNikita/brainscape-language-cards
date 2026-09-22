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
    "don't", "can't", "let's", "didn't", "won't", "isn't", "i'm",
    "there", "here", "very", "too", "now", "today", "yesterday", "tomorrow",
    "some", "any", "all", "no", "yes", "do", "does", "did", "have", "has",
    "had", "will", "would", "can", "could", "should", "must", "may", "might",
    "please", "more", "most", "less", "much", "many", "few", "such", "also",
    "only", "even", "still", "already", "always", "never", "often", "once",
    "after", "before", "under", "over", "through", "between", "without",
    "who", "what", "when", "where", "why", "how", "which",
    "ago", "ones", "two", "down", "up", "out", "off", "back",
    "herself", "himself", "themselves", "myself", "yourself",
    "one", "onto", "away", "soon",
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
    "из-за", "хорошо", "давай", "скоро", "часто", "один", "одна",
}

allow_en = {
    line.strip().lower()
    for line in (PACK / "_vocab" / "allow_en_15260200.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_ru = {
    line.strip().replace("ё", "е").lower()
    for line in (PACK / "_vocab" / "allow_ru_15260200.txt").read_text(encoding="utf-8").splitlines()
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
    "fell": "fall", "felt": "feel", "ran": "run", "running": "run",
    "cried": "cry", "worked": "work", "says": "say",
}

IRREGULAR_RU = {
    "может": "мочь", "могу": "мочь", "можем": "мочь",
    "хочу": "хотеть", "хочет": "хотеть", "хотим": "хотеть",
    "вижу": "видеть", "видишь": "видеть", "видит": "видеть",
    "знаю": "знать", "знаешь": "знать", "знает": "знать",
    "живу": "жить", "живет": "жить", "живёт": "жить",
    "шла": "идти", "шел": "идти", "шёл": "идти", "шли": "идти",
    "идет": "идти", "идёт": "идти", "идем": "идти", "идём": "идти",
    "стал": "стать", "стала": "стать", "стали": "стать",
    "стоит": "стоять", "стоят": "стоять",
    "люблю": "любить", "любит": "любить",
    "говори": "говорить", "говорит": "говорить",
    "скажи": "сказать", "сказал": "сказать",
    "проверь": "проверить", "нажми": "нажать",
    "купи": "купить", "кинь": "кинуть",
    "упал": "упасть", "упала": "упасть",
    "свалилось": "свалиться", "свалится": "свалиться",
    "оторвался": "оторваться", "оторвалась": "оторваться",
    "сработал": "сработать", "заплакала": "заплакать",
    "пишется": "писаться", "наклонись": "наклониться",
    "убегает": "убегать", "сдавайся": "сдаваться",
    "руководствуюсь": "руководствоваться",
    "ссылается": "ссылаться", "украшает": "украшать",
    "стимулирует": "стимулировать",
    "причиняй": "причинить", "лишай": "лишать",
    "уменьши": "уменьшить", "опускай": "опускать",
    "переверни": "перевернуть",
}

RU_ENDINGS = (
    "ами", "ями", "ого", "его", "ому", "ему", "ыми", "ими", "ой", "ей", "ом",
    "ем", "ах", "ях", "ам", "ям", "ов", "ев", "ую", "юю", "ая", "яя",
    "ое", "ее", "ые", "ие", "ый", "ий", "ую", "а", "я", "у", "ю", "е", "и",
    "ы", "о", "ь",
)


def _en_ok(word: str) -> bool:
    w = word.lower().replace("'", "")
    if w in allow_en:
        return True
    if IRREGULAR_EN.get(word.lower()) in allow_en:
        return True
    if "-" in word and all(_en_ok(p) for p in word.split("-") if p):
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
        if any(
            a.startswith(stem) or stem.startswith(a)
            for a in allow_ru
            if len(a) >= 4 and len(stem) >= 4
        ):
            return True
    return False


def _tokens(text: str) -> list[str]:
    return re.findall(r"[A-Za-zА-Яа-яЁё'-]+", text)


print(
    rewrite_chunk(
        Path("russian_english/_chunks/deck_15260200_03.csv"),
        {
            "наклониться": (
                "to bend, to lean",
                "Наклонись ниже.",
                "Bend down lower.",
            ),
            "равенство": (
                "equality, equity",
                "Нам нужно равенство.",
                "We need equality.",
            ),
            "реконструкция": (
                "reconstruction, renovation",
                "Это реконструкция дома.",
                "This is a house reconstruction.",
            ),
            "яд": (
                "poison, venom",
                "Это сильный яд.",
                "This is strong poison.",
            ),
            "изба": (
                "hut, log cabin",
                "Изба стоит в лесу.",
                "The hut stands in the forest.",
            ),
            "культ": (
                "cult",
                "Это опасный культ.",
                "This is a dangerous cult.",
            ),
            "обезьяна": (
                "monkey, ape",
                "Обезьяна на дереве.",
                "The monkey is on the tree.",
            ),
            "акционер": (
                "shareholder, stockholder",
                "Акционер на собрании.",
                "The shareholder is at the meeting.",
            ),
            "схватка": (
                "clash, skirmish",
                "Это была схватка.",
                "This was a clash.",
            ),
            "писание": (
                "writing, scripture",
                "Это старое писание.",
                "This is old writing.",
            ),
            "составление": (
                "compilation, drafting",
                "Составление плана долгое.",
                "The compilation of the plan is long.",
            ),
            "спирт": (
                "alcohol, spirit",
                "Это чистый спирт.",
                "This is pure alcohol.",
            ),
            "медный": (
                "copper, coppery",
                "Это медный провод.",
                "This is a copper wire.",
            ),
            "континент": (
                "continent, mainland",
                "Это большой континент.",
                "This is a large continent.",
            ),
            "встречный": (
                "oncoming, counter",
                "Встречный ветер сильный.",
                "The oncoming wind is strong.",
            ),
            "убегать": (
                "to run away, to escape",
                "Он убегает.",
                "He runs away.",
            ),
            "бомбардировщик": (
                "bomber",
                "Бомбардировщик над городом.",
                "The bomber is over the city.",
            ),
            "фантастика": (
                "science fiction, fantasy",
                "Я люблю фантастику.",
                "I love science fiction.",
            ),
            "опоздать": (
                "to be late, to miss",
                "Я не хочу опоздать.",
                "I do not want to be late.",
            ),
            "сработать": (
                "to work, to go off",
                "План сработал.",
                "The plan worked.",
            ),
            "портфель": (
                "briefcase, portfolio",
                "Портфель на столе.",
                "The briefcase is on the table.",
            ),
            "единственно": (
                "only, solely",
                "Единственно ты знаешь.",
                "Only you know.",
            ),
            "сдерживать": (
                "to restrain, to hold back",
                "Надо сдерживать его.",
                "I need to restrain him.",
            ),
            "строитель": (
                "builder",
                "Строитель работает здесь.",
                "The builder works here.",
            ),
            "руководствоваться": (
                "to be guided, to follow",
                "Я руководствуюсь законом.",
                "I am guided by the law.",
            ),
            "представительство": (
                "agency, representation",
                "Это наше представительство.",
                "This is our agency.",
            ),
            "агрессивный": (
                "aggressive, hostile",
                "Он слишком агрессивный.",
                "He is too aggressive.",
            ),
            "проголосовать": (
                "to vote",
                "Надо проголосовать.",
                "I need to vote.",
            ),
            "серебро": (
                "silver",
                "Это чистое серебро.",
                "This is pure silver.",
            ),
            "наследство": (
                "inheritance, heritage",
                "Это большое наследство.",
                "This is a large inheritance.",
            ),
            "базар": (
                "market, bazaar",
                "Я на базаре.",
                "I am at the market.",
            ),
            "уличный": (
                "street, outdoor",
                "Это уличный кот.",
                "This is a street cat.",
            ),
            "премьер": (
                "premier, prime minister",
                "Премьер говорит нет.",
                "The premier says no.",
            ),
            "кружок": (
                "circle, club",
                "Это мой кружок.",
                "This is my circle.",
            ),
            "спуск": (
                "descent, slope",
                "Спуск опасный.",
                "The descent is dangerous.",
            ),
            "полнота": (
                "fullness, completeness",
                "Полнота жизни важна.",
                "The fullness of life is important.",
            ),
            "писаться": (
                "to be written",
                "Это должно писаться так.",
                "This should be written this way.",
            ),
            "презентация": (
                "presentation",
                "Презентация завтра.",
                "The presentation is tomorrow.",
            ),
            "звон": (
                "ringing, chime",
                "Я слышу звон.",
                "I hear the ringing.",
            ),
            "скидка": (
                "discount, rebate",
                "Большая скидка сегодня.",
                "A big discount today.",
            ),
            "подключение": (
                "connection, hookup",
                "Проверь подключение.",
                "Check the connection.",
            ),
            "сердечный": (
                "cardiac, heartfelt",
                "Это сердечный приступ.",
                "This is a cardiac attack.",
            ),
            "категорически": (
                "categorically, emphatically",
                "Я категорически против.",
                "I am categorically against.",
            ),
            "индийский": (
                "Indian",
                "Я люблю индийское кино.",
                "I love Indian movies.",
            ),
            "правоохранительный": (
                "law enforcement",
                "Правоохранительные органы здесь.",
                "Law enforcement is here.",
            ),
            "жалость": (
                "pity, compassion",
                "Я чувствую жалость.",
                "I feel pity.",
            ),
            "тварь": (
                "creature, beast",
                "Странная тварь.",
                "A strange creature.",
            ),
            "конструктор": (
                "constructor, designer",
                "Он хороший конструктор.",
                "He is a good constructor.",
            ),
            "сокровище": (
                "treasure, riches",
                "Это наше сокровище.",
                "This is our treasure.",
            ),
            "параллельный": (
                "parallel",
                "Это параллельный путь.",
                "This is a parallel path.",
            ),
            "колоссальный": (
                "colossal, enormous",
                "Это колоссальный успех.",
                "This is a colossal success.",
            ),
            "перчатка": (
                "glove, mitten",
                "Где моя перчатка?",
                "Where is my glove?",
            ),
            "бедность": (
                "poverty",
                "Бедность страшная.",
                "Poverty is terrible.",
            ),
            "украшать": (
                "decorate, adorn",
                "Она украшает стол.",
                "She decorates the table.",
            ),
            "причинить": (
                "to cause, to inflict",
                "Не причиняй боль.",
                "Do not cause pain.",
            ),
            "предельный": (
                "maximum, ultimate",
                "Предельная скорость.",
                "The maximum speed.",
            ),
            "лишать": (
                "to deprive",
                "Не лишай меня этого.",
                "Do not deprive me of this.",
            ),
            "микрофон": (
                "microphone",
                "Говори в микрофон.",
                "Speak in the microphone.",
            ),
            "уменьшить": (
                "to reduce, to decrease",
                "Уменьши скорость.",
                "Reduce the speed.",
            ),
            "командный": (
                "team, command",
                "Это командная игра.",
                "This is a team game.",
            ),
            "сдаваться": (
                "to surrender, to give up",
                "Не сдавайся.",
                "Do not surrender.",
            ),
            "дескать": (
                "they say",
                "Он, дескать, дома.",
                "He is home, they say.",
            ),
            "прибытие": (
                "arrival, coming",
                "Прибытие поезда в шесть.",
                "The arrival of the train is at six.",
            ),
            "формулировка": (
                "formulation, wording",
                "Плохая формулировка.",
                "Bad formulation.",
            ),
            "аналогия": (
                "analogy, parallel",
                "Это простая аналогия.",
                "This is a simple analogy.",
            ),
            "стимулировать": (
                "stimulate, encourage",
                "Это стимулирует рост.",
                "This stimulates growth.",
            ),
            "содействие": (
                "assistance, cooperation",
                "Нам нужно содействие.",
                "We need assistance.",
            ),
            "семьдесят": (
                "seventy",
                "Ему семьдесят.",
                "He is seventy.",
            ),
            "тогдашний": (
                "then, of that time",
                "Тогдашний президент.",
                "The then president.",
            ),
            "колбаса": (
                "sausage, salami",
                "Купи колбасу.",
                "Buy sausage.",
            ),
            "пластиковый": (
                "plastic",
                "Пластиковый стол.",
                "A plastic table.",
            ),
            "территориальный": (
                "territorial",
                "Это территориальный вопрос.",
                "This is a territorial question.",
            ),
            "корзина": (
                "basket, bin",
                "Корзина полная.",
                "The basket is full.",
            ),
            "оторваться": (
                "to break away, to detach",
                "Надо оторваться от работы.",
                "I need to break away from work.",
            ),
            "свалиться": (
                "to fall down, to collapse",
                "Дерево скоро свалится.",
                "The tree will fall down soon.",
            ),
            "кинуть": (
                "to throw, to toss",
                "Надо кинуть мяч.",
                "I need to throw the ball.",
            ),
            "инструктор": (
                "instructor, trainer",
                "Инструктор здесь.",
                "The instructor is here.",
            ),
            "традиционно": (
                "traditionally",
                "Мы традиционно так делаем.",
                "We traditionally do it this way.",
            ),
            "превращение": (
                "transformation, conversion",
                "Странное превращение.",
                "A strange transformation.",
            ),
            "непростой": (
                "difficult, complicated",
                "Вопрос непростой.",
                "The question is difficult.",
            ),
            "опускать": (
                "to lower, to let down",
                "Не опускай голову.",
                "Do not lower your head.",
            ),
            "задница": (
                "buttocks, bottom",
                "Он упал на задницу.",
                "He fell on his buttocks.",
            ),
            "фактический": (
                "actual, factual",
                "Фактическая цена другая.",
                "The actual price is different.",
            ),
            "имидж": (
                "image",
                "Её имидж очень важный.",
                "Her image is very important.",
            ),
            "иерархия": (
                "hierarchy",
                "Строгая иерархия.",
                "A strict hierarchy.",
            ),
            "ссылаться": (
                "to refer, to cite",
                "Он ссылается на закон.",
                "He refers to the law.",
            ),
            "стресс": (
                "stress, strain",
                "У меня стресс.",
                "I have stress.",
            ),
            "экспериментальный": (
                "experimental",
                "Это экспериментальный метод.",
                "This is an experimental method.",
            ),
            "заплакать": (
                "to cry",
                "Она хочет заплакать.",
                "She wants to cry.",
            ),
            "квадрат": (
                "square",
                "Это идеальный квадрат.",
                "This is a perfect square.",
            ),
            "полотенце": (
                "towel",
                "Где полотенце?",
                "Where is the towel?",
            ),
            "содержимое": (
                "content, contents",
                "Проверь содержимое.",
                "Check the content.",
            ),
            "клавиша": (
                "key, button",
                "Нажми клавишу.",
                "Press the key.",
            ),
            "изложение": (
                "exposition, statement",
                "Ясное изложение.",
                "A clear exposition.",
            ),
            "лишение": (
                "deprivation, loss",
                "Это лишение свободы.",
                "This is deprivation of freedom.",
            ),
            "опасение": (
                "apprehension, fear",
                "У меня есть опасение.",
                "I have an apprehension.",
            ),
            "лампочка": (
                "light bulb, bulb",
                "Лампочка не работает.",
                "The light bulb does not work.",
            ),
            "оплатить": (
                "to pay, to settle",
                "Надо оплатить это.",
                "I need to pay this.",
            ),
            "индустрия": (
                "industry, sector",
                "Эта индустрия большая.",
                "This industry is large.",
            ),
            "перевернуть": (
                "to overturn, to flip",
                "Не переверни стол.",
                "Do not overturn the table.",
            ),
        },
    )
)

dest = PACK / "_chunks" / "fixed" / "deck_15260200_03.csv"
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
