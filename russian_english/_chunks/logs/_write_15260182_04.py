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
    "herself", "himself", "themselves", "myself", "yourself",
    "one", "onto", "doesnt", "shall", "got", "ive", "youre", "hes", "shes",
    "theyre", "thats", "theres", "heres", "whats", "wheres", "whos",
    "havent", "hasnt", "arent", "wasnt", "werent", "id", "ill",
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
    "не", "ни", "нет", "да", "вот", "уж", "ли", "же", "бы", "б",
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
    for line in (PACK / "_vocab" / "allow_en_15260182.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_ru = {
    line.strip().replace("ё", "е").lower()
    for line in (PACK / "_vocab" / "allow_ru_15260182.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_en |= FUNCTION_EN
allow_ru |= FUNCTION_RU

IRREGULAR_EN = {
    "made": "make", "met": "meet", "saw": "see", "seen": "see", "got": "get", "gave": "give",
    "took": "take", "came": "come", "went": "go", "goes": "go", "ate": "eat",
    "spoke": "speak", "broke": "break", "bought": "buy", "built": "build",
    "found": "find", "left": "leave", "held": "hold", "holds": "hold",
    "told": "tell", "said": "say", "heard": "hear", "paid": "pay",
    "sold": "sell", "lost": "lose", "spent": "spend", "stood": "stand",
    "stands": "stand", "wrote": "write", "flew": "fly", "grew": "grow",
    "began": "begin", "became": "become", "did": "do", "done": "do",
    "known": "know", "knew": "know", "coming": "come", "going": "go",
    "mean": "means",
    "had": "have", "has": "have", "been": "be", "was": "be", "were": "be",
    "waits": "wait", "grows": "grow", "lives": "live", "opens": "open",
    "looks": "look", "reads": "read", "walks": "walk", "writes": "write",
}

IRREGULAR_RU = {
    "может": "мочь", "могу": "мочь", "можем": "мочь",
    "хочу": "хотеть", "хочет": "хотеть", "хотим": "хотеть",
    "вижу": "видеть", "видишь": "видеть", "видит": "видеть", "видел": "видеть",
    "знаю": "знать", "знал": "знать", "живу": "жить", "живет": "жить", "живёт": "жить",
    "шла": "идти", "шел": "идти", "шёл": "идти", "шли": "идти",
    "идет": "идти", "идёт": "идти", "идем": "идти", "идём": "идти", "иди": "идти",
    "стал": "стать", "стала": "стать", "стали": "стать",
    "пришла": "прийти", "пришел": "прийти", "пришёл": "прийти",
    "взял": "взять", "взяла": "взять",
    "стоит": "стоять", "стоят": "стоять",
    "сплю": "спать", "спит": "спать",
    "смотри": "смотреть", "посмотри": "посмотреть",
    "жди": "ждать", "ждёт": "ждать", "ждет": "ждать", "ждал": "ждать",
    "дай": "дать",
    "пишет": "писать", "пишу": "писать",
    "ушел": "уйти", "ушёл": "уйти", "ушла": "уйти",
    "хожу": "ходить", "ходит": "ходить", "ходишь": "ходить",
    "дня": "день", "дней": "день", "днем": "день", "днём": "день",
    "боюс": "бояться", "боюсь": "бояться", "боится": "бояться",
    "ищу": "искать", "ищем": "искать",
    "беру": "брать", "берёт": "брать", "берет": "брать",
    "купи": "купить",
    "отвечает": "отвечать",
    "покажи": "показать",
    "проси": "просить",
    "открой": "открыть",
    "расскажи": "рассказать",
    "выхожу": "выходить",
    "оставь": "оставить",
    "получаешь": "получать",
    "бойся": "бояться",
    "приведи": "привести",
    "ищешь": "искать",
    "принимаю": "принимать",
    "приходит": "приходить",
    "беру": "брать",
    "произошло": "произойти",
    "куплю": "купить",
    "позволяю": "позволять",
    "слышишь": "слышать",
    "представляю": "представлять",
    "поставь": "поставить", "поставить": "поставить",
}

PHRASES_EN = sorted(
    (p for p in allow_en if " " in p),
    key=len,
    reverse=True,
)


def _en_ok(word: str) -> bool:
    w = word.lower().replace("'", "")
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


def target_in_example(lemma: str, example: str) -> bool:
    text = example.replace("ё", "е").lower()
    parts = [p.strip() for p in re.split(r"[\s,;]+", lemma.replace("ё", "е").lower()) if p.strip()]
    keys = [p for p in parts if p not in {"to", "be", "the", "a", "an", "of", "it"}] or parts
    compact = text.replace(" ", "")
    for key in keys:
        stem = key[:4] if len(key) >= 4 else key
        if stem and stem in compact:
            return True
        if key in text:
            return True
    for tok in re.findall(r"[A-Za-zА-Яа-яЁё']+", example):
        w = tok.replace("ё", "е").replace("'", "").lower()
        mapped = IRREGULAR_EN.get(w) or IRREGULAR_RU.get(w)
        if mapped and mapped.replace("ё", "е").lower() in {k.replace("ё", "е") for k in keys}:
            return True
    return False


def tokens_en(text: str) -> list[str]:
    lowered = text.lower()
    for phrase in PHRASES_EN:
        lowered = lowered.replace(phrase, " ")
    return re.findall(r"[a-zA-Z']+", lowered)


def tokens_ru(text: str) -> list[str]:
    return re.findall(r"[А-Яа-яЁё]+", text)


FIXES = {
    "стена": ("wall", "Это стена.", "That's the wall."),
    "представлять": ("to imagine", "Не представляю.", "I can't imagine."),
    "слышать": ("to hear", "Ты слышишь?", "Can you hear?"),
    "ходить": ("to go, to walk", "Куда ты ходишь?", "Where do you go?"),
    "окно": ("window", "Где окно?", "Where's the window?"),
    "рядом": ("nearby, next to", "Я рядом.", "I'm nearby."),
    "прежде": ("before, previously", "Я никогда не видел этого прежде.", "I've never seen this before."),
    "показать": ("to show", "Покажи.", "Show me."),
    "опыт": ("experience", "У него есть опыт.", "He's got experience."),
    "тип": ("type, kind", "Он совсем не мой тип.", "He's not my type at all."),
    "оба": ("both", "Они оба.", "Both of them."),
    "около": ("near, about", "Около дома.", "Near the house."),
    "отвечать": ("to answer", "Он не отвечает.", "He's not answering."),
    "интерес": ("interest", "Есть интерес?", "Any interest?"),
    "современный": ("modern", "Это современный дом?", "Is this a modern house?"),
    "плохой": ("bad", "Плохая идея.", "Bad idea."),
    "сердце": ("heart", "От всего сердца.", "From the heart."),
    "управление": ("management", "Он в управлении.", "He's in management."),
    "наука": ("science", "Это наука?", "Is that science?"),
    "сообщение": ("message", "Есть сообщение.", "There's a message."),
    "значит": ("so, means", "Что это значит?", "What does that mean?"),
    "просить": ("to ask", "Не проси.", "Don't ask."),
    "немного": ("a little, a bit", "Немного воды.", "A little water."),
    "газета": ("newspaper", "Дай газету.", "Give me the newspaper."),
    "интересный": ("interesting, intriguing", "Это интересная идея.", "That's an interesting idea."),
    "живой": ("alive", "Он живой?", "Is he alive?"),
    "поставить": ("to put", "Куда поставить?", "Where should I put it?"),
    "необходимый": ("necessary", "Это необходимо.", "That's necessary."),
    "материал": ("material", "Какой материал?", "What material?"),
    "роль": ("role", "Это его роль.", "That's his role."),
    "открыть": ("to open", "Открой дверь.", "Open the door."),
    "представить": ("to imagine", "Не могу представить.", "I can't imagine."),
    "вполне": ("quite", "Вполне.", "Quite."),
    "будто": ("as if, as though", "Будто он дома.", "As if he's home."),
    "рассказать": ("to tell", "Расскажи.", "Tell me."),
    "выходить": ("to go out", "Я выхожу.", "I'm going out."),
    "рано": ("early", "Слишком рано.", "Too early."),
    "оставить": ("to leave", "Оставь тут.", "Leave it here."),
    "получать": ("to get", "Когда получаешь?", "When do you get it?"),
    "давно": ("long ago", "Это было давно.", "That was long ago."),
    "армия": ("army", "Он в армии.", "He's in the army."),
    "рабочий": ("worker", "Он рабочий.", "He's a worker."),
    "четыре": ("four", "Четыре дня.", "Four days."),
    "бояться": ("to be afraid", "Не бойся.", "Don't be afraid."),
    "различный": ("different, various", "У нас различные мнения.", "We have different opinions."),
    "долго": ("for a long time", "Долго ждал.", "I waited for a long time."),
    "привести": ("to bring", "Приведи его.", "Bring him."),
    "президент": ("president", "Кто президент?", "Who's the president?"),
    "либо": ("either, or", "Либо он, либо я.", "Either him or me."),
    "событие": ("event", "Важное событие.", "An important event."),
    "менее": ("less", "Это менее важно.", "That's less important."),
    "красный": ("red", "Не красный.", "Not the red one."),
    "социальный": ("social", "Это социальная проблема.", "That's a social problem."),
    "искать": ("to look for", "Что ищешь?", "What are you looking for?"),
    "большинство": ("most", "Большинство из нас.", "Most of us."),
    "бизнес": ("business", "Это бизнес.", "That's business."),
    "пусть": ("let, may", "Пусть будет так.", "Let it be so."),
    "легко": ("easily", "Это легко сделать.", "That's easily done."),
    "правительство": ("government", "Наше правительство.", "Our government."),
    "прямо": ("straight", "Иди прямо.", "Go straight."),
    "глава": ("head", "Глава семьи.", "Head of the family."),
    "член": ("member", "Он член группы.", "He's a group member."),
    "суд": ("court", "Дело в суде.", "The case is in court."),
    "возможно": ("maybe", "Возможно.", "Maybe."),
    "принимать": ("to accept", "Я принимаю.", "I accept."),
    "рубль": ("ruble", "Пять рублей.", "Five rubles."),
    "б": ("would", "Если б я знал.", "I would have known."),
    "миллион": ("million", "Миллион раз.", "A million times."),
    "целый": ("whole, entire", "Целый день.", "The whole day."),
    "приходить": ("to come", "Он не приходит.", "He's not coming."),
    "фильм": ("movie", "Какой фильм?", "What movie?"),
    "обычно": ("usually", "Я обычно дома.", "I'm usually home."),
    "спать": ("to sleep", "Хочу спать.", "I want to sleep."),
    "небольшой": ("small", "Небольшой дом.", "A small house."),
    "культура": ("culture", "Наша культура.", "Our culture."),
    "текст": ("text", "Вот текст.", "Here's the text."),
    "брать": ("to take", "Я беру.", "I'll take it."),
    "документ": ("document", "Вот документ.", "Here's the document."),
    "принцип": ("principle", "Это принцип.", "That's a principle."),
    "разговор": ("conversation", "О чём разговор?", "What's the conversation about?"),
    "телефон": ("phone", "Где телефон?", "Where's the phone?"),
    "произойти": ("to happen", "Что произошло?", "What happened?"),
    "правый": ("right", "Правая рука.", "The right hand."),
    "способ": ("way", "Есть способ.", "There's a way."),
    "течение": ("course", "В течение дня.", "In the course of the day."),
    "провести": ("to spend", "Как провести день?", "How do we spend the day?"),
    "вокруг": ("around", "Посмотри вокруг.", "Look around."),
    "проходить": ("to pass, to go by", "Время проходит.", "Time is passing."),
    "купить": ("buy, purchase", "Я куплю новую машину.", "I will buy a new car."),
    "родитель": ("parent", "Где родители?", "Where are the parents?"),
    "сей": ("this", "На сей раз.", "This time."),
    "ряд": ("row", "В первый ряд.", "In the first row."),
    "ещё": ("still, yet", "Ещё нет.", "Not yet."),
    "единственный": ("only", "Ты единственный.", "You're the only one."),
    "метр": ("meter", "Два метра.", "Two meters."),
    "сайт": ("website", "На нашем сайте.", "On our website."),
    "партия": ("party", "Какая партия?", "Which party?"),
    "позволять": ("to allow", "Я не позволяю.", "I don't allow it."),
    "образование": ("education", "У него образование.", "He's got an education."),
    "зачем": ("why", "Зачем это?", "Why is that?"),
}


def check_leftovers(dest: Path) -> list[str]:
    leftover: list[str] = []
    cards = cards_from_path(dest)
    extra_ru = {lemma_from_card(card).replace("ё", "е").lower() for card in cards}
    local_ru = set(allow_ru) | extra_ru
    for i, card in enumerate(cards, 1):
        lemma = lemma_from_card(card)
        gloss = answer_lemma_from_card(card)
        payload = card_write_payload(card)
        q = payload["question"]
        a = payload["answer"]
        ru = q.split("## Footnote")[-1].strip()
        en = a.split("## Footnote")[-1].strip() if "## Footnote" in a else a.strip()
        if not target_in_example(lemma, ru):
            leftover.append(f"{i} LEMMA {lemma} :: {ru}")
        if not target_in_example(gloss, en):
            leftover.append(f"{i} GLOSS {gloss} :: {en}")
        for tok in tokens_en(en):
            if not _en_ok(tok):
                leftover.append(f"{i} EN {tok} :: {en}")
        for tok in tokens_ru(ru):
            w = tok.replace("ё", "е").lower()
            if w in local_ru or _ru_ok(tok):
                continue
            leftover.append(f"{i} RU {tok} :: {ru}")
    return leftover


stats = rewrite_chunk(
    Path("russian_english/_chunks/deck_15260182_04.csv"),
    FIXES,
)
print(stats)

leftover = check_leftovers(Path(stats["path"]))
print(f"leftovers={len(leftover)}")
if leftover:
    print("\n".join(leftover))
