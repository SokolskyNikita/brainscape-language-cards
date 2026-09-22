import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from brainscape import answer_lemma_from_card, card_write_payload, cards_from_path, lemma_from_card
from russian_english._chunk_io import rewrite_chunk

PACK = REPO / "russian_english"
SRC = PACK / "_chunks" / "deck_15260185_04.csv"

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
    "one", "onto", "dont", "doesnt", "lets",
    "don't", "doesn't", "can't", "won't", "isn't", "i'm", "i've", "we're",
    "he's", "she's", "that's", "what's", "where's", "how's", "it's",
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
}

allow_en = {
    line.strip().lower()
    for line in (PACK / "_vocab" / "allow_en_15260185.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_ru = {
    line.strip().replace("ё", "е").lower()
    for line in (PACK / "_vocab" / "allow_ru_15260185.txt").read_text(encoding="utf-8").splitlines()
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
    "lit": "light", "slept": "sleep", "sang": "sing", "sings": "sing",
    "sat": "sit", "ran": "run", "running": "run", "runs": "run",
    "hitting": "hit", "going": "go", "coming": "come",
    "felt": "feel", "growing": "grow", "paying": "pay",
}

IRREGULAR_RU = {
    "может": "мочь", "могу": "мочь", "можем": "мочь",
    "хочу": "хотеть", "хочет": "хотеть", "хотим": "хотеть", "хочешь": "хотеть",
    "вижу": "видеть", "видишь": "видеть", "видит": "видеть",
    "знаю": "знать", "живу": "жить", "живет": "жить", "живёт": "жить",
    "шла": "идти", "шел": "идти", "шёл": "идти", "шли": "идти",
    "идет": "идти", "идёт": "идти", "идем": "идти", "идём": "идти",
    "стал": "стать", "стала": "стать", "стали": "стать",
    "взял": "взять", "взяла": "взять",
    "стоит": "стоять", "стоят": "стоять",
    "спит": "спать", "спал": "спать",
    "дай": "дать",
    "растёт": "расти", "растет": "расти",
    "зовут": "звать",
    "зови": "звать",
    "открой": "открыть",
    "ухе": "ухо",
    "левая": "левый",
}

RU_ENDINGS = (
    "ами", "ями", "ого", "его", "ому", "ему", "ыми", "ими", "ой", "ей", "ом",
    "ем", "ах", "ях", "ам", "ям", "ов", "ев", "ую", "юю", "ая", "яя",
    "ое", "ее", "ые", "ие", "ый", "ий", "ую", "а", "я", "у", "ю", "е", "и",
    "ы", "о", "ь",
)


def _en_ok(word: str) -> bool:
    w = word.lower()
    if w in allow_en:
        return True
    if IRREGULAR_EN.get(w) in allow_en:
        return True
    if "-" in w and all(_en_ok(p) for p in w.split("-") if p):
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
    if mapped and mapped.replace("ё", "е") in allow_ru:
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


def target_in_example(lemma: str, example: str) -> bool:
    text = example.replace("ё", "е").lower()
    parts = [p.strip() for p in re.split(r"[\s,;]+", lemma.replace("ё", "е").lower()) if p.strip()]
    keys = [p for p in parts if p not in {"to", "be", "the", "a", "an", "of", "it", "is"}] or parts
    compact = text.replace(" ", "")
    tokens = set(re.findall(r"[A-Za-z']+", text)) | set(re.findall(r"[А-Яа-яЁё]+", text))
    for key in keys:
        stem = key[:4] if len(key) >= 4 else key
        if stem and stem in compact:
            return True
        if key in text:
            return True
        if IRREGULAR_EN.get(key) and IRREGULAR_EN[key] in tokens:
            return True
        for tok in tokens:
            if IRREGULAR_EN.get(tok) == key:
                return True
            if IRREGULAR_RU.get(tok) == key:
                return True
    return False


FIXES = {
    "воля": ("will, willpower", "У неё сильная воля.", "She has a strong will."),
    "январь": ("January", "В январе.", "In January."),
    "боевой": ("combat, fighting", "Боевой дух.", "Fighting spirit."),
    "хватать": ("to be enough", "Мне не хватает времени.", "I don't have enough time."),
    "вчера": ("yesterday", "Я был там вчера.", "I was there yesterday."),
    "режим": ("regime, routine", "Какой режим?", "What's the routine?"),
    "очередной": ("another, next", "Очередной вопрос.", "Another question."),
    "отдать": ("to give, to hand over", "Отдай это.", "Hand that over."),
    "здоровье": ("health", "Как здоровье?", "How's your health?"),
    "расти": ("to grow", "Он быстро растёт.", "He's growing fast."),
    "стоимость": ("cost, price", "Какая стоимость?", "What's the cost?"),
    "правильный": ("correct, right", "Ваш ответ правильный.", "Your answer is correct."),
    "километр": ("kilometer", "Мы прошли пять километров.", "We walked five kilometers."),
    "звать": ("to call, to be called", "Не надо звать.", "No need to call."),
    "шесть": ("six", "Шесть часов.", "It's six."),
    "личность": ("person, personality", "Известная личность.", "A famous person."),
    "физический": ("physical", "Физический труд.", "Physical work."),
    "регион": ("region, area", "В нашем регионе.", "In our region."),
    "рот": ("mouth", "Открой рот.", "Open your mouth."),
    "больной": ("sick, ill", "Он совсем больной.", "He's really sick."),
    "итог": ("result, outcome", "Какой итог?", "What's the result?"),
    "предел": ("limit", "Это уже предел.", "That's the limit."),
    "занять": ("to borrow", "Можно занять?", "Can I borrow this?"),
    "читатель": ("reader", "Наш читатель.", "Our reader."),
    "медленно": ("slowly", "Говори медленно.", "Speak slowly."),
    "старик": ("old man", "Это старик.", "That's an old man."),
    "прочий": ("other, the rest", "И прочее.", "And the rest."),
    "победа": ("victory, win", "Это наша победа.", "That's our victory."),
    "элемент": ("element", "Важный элемент.", "An important element."),
    "естественно": ("naturally, of course", "Естественно.", "Of course."),
    "обратиться": ("to turn to, to address", "Обратись к врачу.", "Turn to a doctor."),
    "постоянный": ("permanent, constant", "Постоянная работа.", "A permanent job."),
    "встречаться": ("to meet, to date", "Мы встречаемся завтра.", "We're meeting tomorrow."),
    "женский": ("women's, female", "Женский голос.", "A female voice."),
    "командир": ("commander", "Где командир?", "Where's the commander?"),
    "август": ("August", "До августа.", "Until August."),
    "впервые": ("for the first time", "Я здесь впервые.", "It's my first time here."),
    "секунда": ("second", "Одну секунду.", "One second."),
    "счастливый": ("happy", "Счастливый человек.", "A happy person."),
    "житель": ("resident, inhabitant", "Местный житель.", "A local resident."),
    "видимо": ("apparently", "Видимо, нет.", "Apparently not."),
    "праздник": ("holiday, celebration", "Сегодня праздник.", "Today's a holiday."),
    "множество": ("a great many, multitude", "Множество проблем.", "A great many problems."),
    "сумма": ("sum, amount", "Какая сумма?", "What's the amount?"),
    "сцена": ("scene, stage", "Он на сцене.", "He's on stage."),
    "насколько": ("how much, to what extent", "Насколько это важно?", "How much does this matter?"),
    "есть": ("to eat", "Я хочу есть.", "I want to eat."),
    "едва": ("hardly, barely", "Он едва спал прошлой ночью.", "He hardly slept last night."),
    "техника": ("equipment, technology", "Новая техника.", "New equipment."),
    "малый": ("small, minor", "Малый размер.", "A small size."),
    "подготовка": ("preparation", "Нужна подготовка.", "We need preparation."),
    "сожаление": ("regret", "Без сожаления.", "Without regret."),
    "ухо": ("ear", "Боль в ухе.", "Pain in the ear."),
    "исторический": ("historical, historic", "Исторический момент.", "A historic moment."),
    "занятие": ("class, activity", "У меня занятие.", "I've got a class."),
    "почувствовать": ("to feel", "Я это почувствовал.", "I felt that."),
    "существование": ("existence", "Смысл существования.", "The meaning of existence."),
    "мужик": ("guy, man", "Нормальный мужик.", "A normal guy."),
    "городской": ("city, urban", "Городской район.", "A city district."),
    "октябрь": ("October", "С октября.", "Since October."),
    "недавно": ("recently", "Я недавно был там.", "I was there recently."),
    "нос": ("nose", "Большой нос.", "A big nose."),
    "существо": ("creature, being", "Живое существо.", "A living creature."),
    "абсолютно": ("absolutely, totally", "Абсолютно нет.", "Absolutely not."),
    "обладать": ("to possess, to have", "Он обладает силой.", "He possesses strength."),
    "рамка": ("frame", "Картина в рамке.", "The picture's in a frame."),
    "начинаться": ("to begin, to start", "Фильм начинается.", "The movie's starting."),
    "генерал": ("general", "Он генерал.", "He's a general."),
    "благодаря": ("thanks to, due to", "Благодаря тебе.", "Thanks to you."),
    "значить": ("to mean", "Что это значит?", "What does that mean?"),
    "многое": ("much, many things", "Многое зависит от тебя.", "Much depends on you."),
    "попробовать": ("to try", "Попробуй.", "Try it."),
    "французский": ("French", "Это французский?", "Is that French?"),
    "правильно": ("correctly, right", "Правильно.", "That's right."),
    "сентябрь": ("September", "До сентября.", "Until September."),
    "известно": ("it is known", "Мне это известно.", "That's known to me."),
    "левый": ("left", "Левая рука.", "The left hand."),
    "университет": ("university", "Я в университете.", "I'm at university."),
    "считаться": ("to be considered, to count", "Не считается.", "That doesn't count."),
    "частный": ("private", "Частный дом.", "A private house."),
    "глубокий": ("deep", "Глубокая река.", "A deep river."),
    "многие": ("many", "Многие так думают.", "Many think so."),
    "клуб": ("club", "В каком клубе?", "Which club?"),
    "принадлежать": ("to belong", "Эта книга принадлежит мне.", "This book belongs to me."),
    "подняться": ("to get up, to rise", "Я не могу подняться.", "I can't get up."),
    "лето": ("summer", "Люблю лето.", "I love summer."),
    "заставить": ("to make, to force", "Не заставляй меня.", "Don't make me."),
    "выражение": ("expression, phrase", "Странное выражение.", "A strange expression."),
    "платить": ("to pay", "Кто платит?", "Who's paying?"),
    "спокойно": ("calmly", "Говори спокойно.", "Speak calmly."),
    "приводить": ("to bring, to lead", "Приводи его сюда.", "Bring him here."),
    "одежда": ("clothes, clothing", "Где одежда?", "Where are the clothes?"),
    "ради": ("for the sake of", "Ради тебя.", "For your sake."),
    "автомобиль": ("car", "Вчера я купил новый автомобиль.", "I bought a new car yesterday."),
    "продажа": ("sale", "Дом на продажу.", "The house is for sale."),
    "закрыть": ("to close, to shut", "Пожалуйста, закройте дверь.", "Please close the door."),
    "святой": ("holy, saint", "Святой человек.", "A holy man."),
    "финансовый": ("financial", "Финансовый вопрос.", "A financial matter."),
    "декабрь": ("December", "После декабря.", "After December."),
    "театр": ("theater", "В театре.", "At the theater."),
}


def check_leftovers(dest: Path) -> tuple[list[str], list[str]]:
    leftover: list[str] = []
    missing: list[str] = []
    for i, card in enumerate(cards_from_path(dest), start=1):
        lemma = lemma_from_card(card)
        gloss = answer_lemma_from_card(card)
        payload = card_write_payload(card)
        ru_ex = payload["question"].split("## Footnote")[-1].strip()
        en_ex = payload["answer"].split("## Footnote")[-1].strip()
        lemma_bits = set(re.findall(r"[A-Za-z']+", gloss.lower()))
        for tok in re.findall(r"[A-Za-z']+", en_ex):
            if tok.lower() in lemma_bits:
                continue
            if not _en_ok(tok):
                leftover.append(f"{i} EN {tok} :: {en_ex}")
        ru_bits = set(re.findall(r"[А-Яа-яЁё]+", lemma.lower().replace("ё", "е")))
        for tok in re.findall(r"[А-Яа-яЁё]+", ru_ex):
            if tok.replace("ё", "е").lower() in ru_bits:
                continue
            if not _ru_ok(tok):
                leftover.append(f"{i} RU {tok} :: {ru_ex}")
        if not target_in_example(gloss, en_ex):
            missing.append(f"{i} EN {gloss} :: {en_ex}")
        if not target_in_example(lemma, ru_ex):
            missing.append(f"{i} RU {lemma} :: {ru_ex}")
    return leftover, missing


if __name__ == "__main__":
    stats = rewrite_chunk(SRC, FIXES)
    print(stats)
    leftover, missing = check_leftovers(Path(stats["path"]))
    if leftover:
        print("LEFTOVER:")
        print("\n".join(leftover))
    if missing:
        print("MISSING TARGET:")
        print("\n".join(missing))
    if not leftover and not missing:
        print("leftover=0 missing_target=0")
