import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from brainscape import answer_lemma_from_card, card_write_payload, cards_from_path, lemma_from_card
from russian_english._chunk_io import rewrite_chunk

PACK = REPO / "russian_english"
SRC = PACK / "_chunks" / "deck_15260198_03.csv"

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
    "знаю": "знать", "живу": "жить", "живет": "жить",
    "шла": "идти", "шел": "идти", "шли": "идти",
    "идет": "идти", "идем": "идти", "идёт": "идти",
    "стал": "стать", "стала": "стать", "стали": "стать",
    "взял": "взять", "взяла": "взять",
    "стоит": "стоять", "стоят": "стоять", "стою": "стоять",
    "сидим": "сидеть", "сидит": "сидеть",
    "горит": "гореть",
    "изучаю": "изучать",
    "мыслит": "мыслить",
    "смотрит": "смотреть",
    "растет": "расти", "растёт": "расти", "растут": "расти",
    "лет": "год",
    "сожгу": "сжечь", "сжег": "сжечь", "сжёг": "сжечь",
    "сожму": "сжать", "сжми": "сжать",
    "обойдусь": "обходиться", "обойтись": "обходиться",
    "застыл": "застыть",
    "предпочел": "предпочесть", "предпочёл": "предпочесть",
    "уселся": "усесться",
    "передается": "передаваться", "передаётся": "передаваться",
    "возвратится": "возвратиться",
    "решил": "решить",
    "нужен": "нужный", "нужна": "нужный",
    "сказал": "сказать", "сказала": "сказать",
    "пришло": "прийти", "пришла": "прийти", "пришел": "прийти",
    "годится": "годиться",
    "порядка": "порядок",
    "руку": "рука", "руки": "рука",
    "окна": "окно", "окно": "окно",
    "церкви": "церковь",
    "выдвинем": "выдвинуть",
    "обойтись": "обходиться",
    "кассы": "касса",
    "скамейке": "скамейка",
    "клинике": "клиника",
    "аренду": "аренда",
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
    Path("russian_english/_chunks/deck_15260198_03.csv"),
    {
        "сжечь": ("burn, incinerate", "Он хочет сжечь бумагу.", "He wants to burn the paper."),
        "посчитать": ("calculate, count", "Нам надо посчитать.", "We need to calculate."),
        "выдвинуть": ("nominate, put forward", "Надо выдвинуть его.", "We will nominate him."),
        "правитель": ("ruler, governor", "Это наш правитель.", "This is our ruler."),
        "передаваться": (
            "to be transmitted, to be passed on",
            "Болезнь может передаваться.",
            "Illness can be passed on.",
        ),
        "пацан": ("boy, lad", "Этот пацан мой брат.", "This boy is my brother."),
        "пожелание": ("wish, desire", "У меня есть пожелание.", "I have a wish."),
        "поддержание": (
            "maintenance, support",
            "Нужно поддержание порядка.",
            "We need maintenance of order.",
        ),
        "пенсионер": (
            "pensioner, retiree",
            "Мой отец уже пенсионер.",
            "My father is already a pensioner.",
        ),
        "бесконечно": ("infinitely, endless", "Это бесконечно долго.", "This is infinitely long."),
        "стук": ("knock, tapping", "Это стук в дверь.", "That is a knock at the door."),
        "сравнительно": (
            "comparatively, relatively",
            "Это сравнительно просто.",
            "This is comparatively simple.",
        ),
        "рожать": (
            "to give birth, to bear",
            "Она скоро будет рожать.",
            "She will give birth soon.",
        ),
        "обходиться": (
            "manage, do without",
            "Я могу обходиться без помощи.",
            "I can manage without help.",
        ),
        "крестьянский": ("peasant, rural", "Это крестьянский дом.", "This is a peasant house."),
        "поддаваться": (
            "yield, succumb",
            "Не надо поддаваться страху.",
            "Do not yield to fear.",
        ),
        "касса": ("cash desk, box office", "Где здесь касса?", "Where is the cash desk?"),
        "слабо": ("weakly, faintly", "Огонь горит слабо.", "The fire burns weakly."),
        "простор": ("space, expanse", "Мне нужен простор.", "I need space."),
        "наказать": ("punish, penalize", "Его надо наказать.", "He must be punished."),
        "мент": ("cop, policeman", "Мент стоит у дома.", "The cop stands near the house."),
        "здравый": ("sound, sensible", "У него здравый смысл.", "He has sound sense."),
        "программирование": (
            "programming, coding",
            "Я изучаю программирование.",
            "I study programming.",
        ),
        "сеанс": ("session, screening", "Сеанс в два часа.", "The session is at two."),
        "четверо": ("four, four people", "Нас было четверо.", "There were four of us."),
        "научно": ("scientifically, scholarly", "Он мыслит научно.", "He thinks scientifically."),
        "подружка": ("girlfriend, female friend", "Это моя подружка.", "This is my girlfriend."),
        "сжать": ("squeeze, compress", "Надо сжать руку.", "You need to squeeze the hand."),
        "поесть": ("to eat, to have a meal", "Мне надо поесть.", "I need to eat."),
        "столичный": ("capital, metropolitan", "Это столичный город.", "This is a capital city."),
        "возвратиться": (
            "return, come back",
            "Он хочет возвратиться домой.",
            "He wants to return home.",
        ),
        "скамейка": ("bench, seat", "Где наша скамейка?", "Where is the bench?"),
        "спортсмен": ("athlete, sportsman", "Он хороший спортсмен.", "He is a good athlete."),
        "телевизионный": (
            "television, TV",
            "Это телевизионный сигнал.",
            "This is a television signal.",
        ),
        "перечислить": (
            "list, enumerate",
            "Надо перечислить имена.",
            "We need to list the names.",
        ),
        "старт": ("start, launch", "Это хороший старт.", "This is a good start."),
        "скот": ("cattle, livestock", "Скот стоит в поле.", "The cattle stand in the field."),
        "изобретение": (
            "invention, discovery",
            "Это важное изобретение.",
            "This is an important invention.",
        ),
        "годиться": ("to be suitable, to fit", "Это должно годиться.", "This must be suitable."),
        "обучать": ("to teach, to train", "Он будет обучать нас.", "He will teach us."),
        "усесться": (
            "sit down, settle",
            "Он хочет усесться у окна.",
            "He wants to sit down by the window.",
        ),
        "алгоритм": ("algorithm", "Этот алгоритм простой.", "This algorithm is simple."),
        "освоение": (
            "development, mastering",
            "Освоение космоса идёт.",
            "The development of space goes on.",
        ),
        "кататься": ("to skate, to ride", "Я хочу кататься.", "I want to skate."),
        "перестройка": (
            "restructuring, perestroika",
            "Идёт большая перестройка.",
            "A big restructuring is going on.",
        ),
        "полевой": ("field, fieldwork", "Это полевой цветок.", "This is a field flower."),
        "относительный": (
            "relative, comparative",
            "Это относительный успех.",
            "This is a relative success.",
        ),
        "проделать": ("do, carry out", "Я хочу проделать работу.", "I want to do the work."),
        "медленный": ("slow, sluggish", "Это медленный поезд.", "This is a slow train."),
        "застыть": ("freeze, petrify", "Он может застыть тут.", "He can freeze here."),
        "работодатель": ("employer", "Это мой работодатель.", "This is my employer."),
        "кирпич": ("brick, block", "Это красный кирпич.", "This is a red brick."),
        "убеждать": (
            "to persuade, to convince",
            "Он хочет убеждать нас.",
            "He wants to persuade us.",
        ),
        "клиника": ("clinic, hospital", "Это местная клиника.", "This is a local clinic."),
        "невозможность": (
            "impossibility, inability",
            "Это полная невозможность.",
            "This is a complete impossibility.",
        ),
        "порождать": (
            "generate, produce",
            "Это может порождать страх.",
            "This can generate fear.",
        ),
        "аренда": ("rent, lease", "Аренда уже высокая.", "The rent is already high."),
        "пропускать": (
            "to miss, to skip",
            "Не надо пропускать урок.",
            "Do not miss the lesson.",
        ),
        "предпочесть": (
            "prefer, choose",
            "Он решил предпочесть чай.",
            "He decided to prefer tea.",
        ),
        "исполниться": (
            "to be fulfilled, to come true",
            "Мечта должна исполниться.",
            "The dream must be fulfilled.",
        ),
        "тропа": ("path, trail", "Тропа идёт через лес.", "The path goes through the forest."),
        "сосредоточить": (
            "concentrate, focus",
            "Надо сосредоточить внимание.",
            "We need to concentrate attention.",
        ),
        "матрос": ("sailor, seaman", "Этот матрос молодой.", "This sailor is young."),
        "механический": (
            "mechanical, mechanic",
            "У него механический голос.",
            "He has a mechanical voice.",
        ),
        "затылок": (
            "back of the head, nape",
            "Удар в затылок.",
            "A blow to the back of the head.",
        ),
        "раздражение": (
            "irritation, annoyance",
            "Я чувствую раздражение.",
            "I feel irritation.",
        ),
        "водный": ("water, aquatic", "Это водный путь.", "This is a water path."),
        "задумчиво": (
            "thoughtfully, pensively",
            "Он задумчиво смотрит в окно.",
            "He looks thoughtfully at the window.",
        ),
        "инфляция": (
            "inflation, price increase",
            "Инфляция растёт каждый год.",
            "Inflation grows every year.",
        ),
        "наметить": ("outline, mark", "Нам надо наметить план.", "We need to outline the plan."),
        "локальный": ("local, localized", "Это локальный рынок.", "This is a local market."),
        "потянуться": ("to stretch, to reach out", "Я хочу потянуться.", "I want to stretch."),
        "степь": ("steppe, prairie", "Степь очень широкая.", "The steppe is very wide."),
        "календарь": ("calendar, almanac", "Где мой календарь?", "Where is my calendar?"),
        "закат": ("sunset, decline", "Закат уже близко.", "Sunset is already near."),
        "грубо": ("roughly, coarsely", "Он грубо сказал это.", "He said that roughly."),
        "внезапный": ("sudden, unexpected", "Это внезапный дождь.", "This is a sudden rain."),
        "дожидаться": (
            "wait for, await",
            "Я буду дожидаться тебя.",
            "I will wait for you.",
        ),
        "ширина": ("width, breadth", "Какая ширина стола?", "What is the width of the table?"),
        "доноситься": (
            "to be heard, to carry",
            "Музыка может доноситься сюда.",
            "Music can be heard here.",
        ),
        "оранжевый": ("orange, orange-colored", "У меня оранжевый шар.", "I have an orange ball."),
        "повредить": (
            "damage, harm",
            "Не надо повредить стол.",
            "Do not damage the table.",
        ),
        "поспешить": ("to hurry, to hasten", "Нам надо поспешить.", "We need to hurry."),
        "всюду": ("everywhere, all over", "Вода всюду.", "There is water everywhere."),
        "написание": (
            "spelling, writing",
            "Проверь написание слова.",
            "Check the spelling of the word.",
        ),
        "шептать": ("whisper, murmur", "Не надо шептать.", "Do not whisper."),
        "субъективный": (
            "subjective, personal",
            "Это субъективный взгляд.",
            "This is a subjective view.",
        ),
        "демон": ("demon, fiend", "Это злой демон.", "This is an evil demon."),
        "десятый": ("tenth, 10th", "Это десятый день.", "This is the tenth day."),
        "поп": ("priest, pop", "Поп стоит у церкви.", "The priest stands by the church."),
        "гнездо": ("nest, roost", "Гнездо на дереве.", "The nest is on the tree."),
        "одиннадцать": ("eleven", "Нас одиннадцать человек.", "There are eleven of us."),
        "торжество": (
            "celebration, festivity",
            "Завтра будет торжество.",
            "Tomorrow there will be a celebration.",
        ),
        "модернизация": (
            "modernization, upgrade",
            "Нужна модернизация завода.",
            "The factory needs modernization.",
        ),
        "переписка": (
            "correspondence, exchange of letters",
            "Наша переписка долгая.",
            "Our correspondence is long.",
        ),
        "барьер": ("barrier, hurdle", "Барьер на дороге.", "There is a barrier on the road."),
        "питаться": ("to feed, to nourish", "Им надо питаться.", "They need to feed."),
        "возвращать": (
            "to return, to give back",
            "Я буду возвращать книгу.",
            "I will return the book.",
        ),
        "митинг": ("rally, meeting", "Завтра будет митинг.", "Tomorrow there will be a rally."),
        "представиться": (
            "introduce oneself, present oneself",
            "Мне надо представиться.",
            "I need to introduce myself.",
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
