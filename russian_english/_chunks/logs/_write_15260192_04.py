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
    "don't", "that's", "he's", "she's", "it's", "i'm", "we're", "they're",
    "there", "here", "very", "too", "now", "today", "yesterday", "tomorrow",
    "some", "any", "all", "no", "yes", "do", "does", "did", "have", "has",
    "had", "will", "would", "can", "could", "should", "must", "may", "might",
    "please", "more", "most", "less", "much", "many", "few", "such", "also",
    "only", "even", "still", "already", "always", "never", "often", "once",
    "after", "before", "under", "over", "through", "between", "without",
    "who", "what", "when", "where", "why", "how", "which",
    "ago", "ones", "two", "down", "up", "out", "off", "back",
    "herself", "himself", "themselves", "myself", "yourself",
    "one", "onto", "dont", "doesnt", "lets", "just", "again",
    "let's", "there's", "what's", "i've", "we've", "you'll", "he's",
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

IRREGULAR_EN = {
    "came": "come", "gave": "give", "took": "take", "went": "go", "got": "get",
    "saw": "see", "was": "be", "were": "be", "been": "be", "had": "have",
    "did": "do", "said": "say", "made": "make", "left": "leave", "felt": "feel",
    "began": "begin", "became": "become", "bought": "buy", "caught": "catch",
    "kept": "keep", "lost": "lose", "fell": "fall", "grew": "grow", "held": "hold",
    "knew": "know", "ran": "run", "sat": "sit", "stood": "stand", "told": "tell",
    "thought": "think", "wrote": "write", "spoke": "speak", "broke": "break",
    "chose": "choose", "drove": "drive", "ate": "eat", "flew": "fly",
    "understood": "understand", "shown": "show", "showed": "show",
}

IRREGULAR_RU = {
    "идет": "идти", "иду": "идти", "шел": "идти", "шла": "идти", "шли": "идти",
    "нужна": "нужный", "нужен": "нужный", "нужно": "нужный",
    "болит": "болеть", "смотрит": "смотреть", "смотри": "смотреть",
    "люблю": "любить", "начал": "начать", "начала": "начать",
    "ест": "есть", "съел": "съесть",
    "может": "мочь", "могу": "мочь", "хочет": "хотеть", "хочу": "хотеть",
    "звонил": "звонить", "звонили": "звонить",
    "купили": "купить", "пойдём": "пойти", "пошел": "пойти",
    "ушёл": "уйти", "ушел": "уйти", "понял": "понять",
    "получил": "получить", "вышел": "выйти",
    "сдаю": "сдавать", "целуй": "целовать",
}

RU_ENDINGS = (
    "ами", "ями", "ого", "его", "ому", "ему", "ыми", "ими", "ой", "ей", "ом",
    "ем", "ах", "ях", "ам", "ям", "ов", "ев", "ую", "юю", "ая", "яя", "ое",
    "ее", "ые", "ие", "ый", "ий", "а", "я", "у", "ю", "е", "и", "ы", "о", "ь",
)

allow_en = {
    line.strip().lower()
    for line in (PACK / "_vocab" / "allow_en_15260192.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_ru = {
    line.strip().replace("ё", "е").lower()
    for line in (PACK / "_vocab" / "allow_ru_15260192.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_en |= FUNCTION_EN
allow_ru |= FUNCTION_RU


def _en_ok(word: str, extra: set[str] | None = None) -> bool:
    w = word.lower()
    pool = allow_en | (extra or set())
    if w in pool:
        return True
    if IRREGULAR_EN.get(w) in pool:
        return True
    if w.endswith("'s") and w[:-2] in pool:
        return True
    for suf in ("'s", "s", "es", "ed", "ing", "ly", "er", "est"):
        if w.endswith(suf) and w[: -len(suf)] in pool:
            return True
        if w.endswith(suf) and w[: -len(suf)] + "e" in pool:
            return True
    if w.endswith("ies") and (w[:-3] + "y") in pool:
        return True
    if w.endswith("ied") and (w[:-3] + "y") in pool:
        return True
    return False


def _ru_ok(word: str, extra: set[str] | None = None) -> bool:
    w = word.replace("ё", "е").lower()
    pool = allow_ru | (extra or set())
    if w in pool:
        return True
    if IRREGULAR_RU.get(w) in pool:
        return True
    stems = {w}
    for suf in RU_ENDINGS:
        if w.endswith(suf) and len(w) - len(suf) >= 3:
            stems.add(w[: -len(suf)])
    for stem in stems:
        if stem in pool:
            return True
        if any(
            a.startswith(stem) or stem.startswith(a)
            for a in pool
            if len(a) >= 4 and len(stem) >= 4
        ):
            return True
    return False


def _tokens(text: str) -> list[str]:
    return re.findall(r"[A-Za-zА-Яа-яЁё'-]+", text)


def _gloss_parts(gloss: str) -> set[str]:
    cleaned = re.sub(r"\([^)]*\)", "", gloss.lower())
    parts = re.split(r"[,;/]| or | and ", cleaned)
    out = set()
    for part in parts:
        part = re.sub(r"^(to |the |a |an )", "", part.strip())
        if part:
            out.add(part)
            out.update(part.split())
    return out


fixes = {
    "шестой": ("sixth", "Я шестой.", "I'm sixth."),
    "блин": ("damn, crap", "Блин, опять!", "Damn, again!"),
    "дважды": ("twice", "Звонил дважды.", "I called twice."),
    "спускаться": (
        "to go down, to descend",
        "Мы спускаемся.",
        "We're going down.",
    ),
    "негативный": ("negative", "Негативный ответ.", "A negative answer."),
    "свеча": ("candle", "Где свеча?", "Where's the candle?"),
    "медведь": ("bear", "Там медведь!", "There's a bear!"),
    "оперативный": (
        "prompt, operational",
        "Нужна оперативная помощь.",
        "We need prompt help.",
    ),
    "помешать": (
        "to get in the way",
        "Только не помешай.",
        "Just don't get in the way.",
    ),
    "наверх": ("upstairs, up", "Пойдём наверх.", "Let's go upstairs."),
    "прогноз": ("forecast", "Какой прогноз?", "What's the forecast?"),
    "опрос": ("survey, poll", "Был опрос?", "Was there a survey?"),
    "собеседник": (
        "conversation partner",
        "Собеседник молчит.",
        "The conversation partner is quiet.",
    ),
    "публичный": ("public", "Это публичное место.", "This is a public place."),
    "пожилой": ("elderly", "Он уже пожилой.", "He's elderly now."),
    "подсказать": (
        "to prompt, to hint",
        "Подскажи мне.",
        "Give me a hint.",
    ),
    "супруг": ("husband", "Супруг ещё на работе.", "My husband's still at work."),
    "устанавливать": (
        "to install, to set",
        "Они устанавливают программу.",
        "They're installing the program.",
    ),
    "миссия": ("mission", "Это наша миссия.", "This is our mission."),
    "свидание": ("date", "У нас свидание.", "We've got a date."),
    "дедушка": ("grandfather, grandpa", "Дедушка дома?", "Is grandpa home?"),
    "платформа": ("platform", "На какой платформе?", "Which platform?"),
    "тонна": ("ton", "Там тонна работы.", "There's a ton of work."),
    "горизонт": (
        "horizon",
        "Солнце за горизонтом.",
        "The sun's below the horizon.",
    ),
    "уверить": ("to assure", "Могу вас уверить.", "I can assure you."),
    "сахар": ("sugar", "Без сахара.", "No sugar."),
    "эволюция": ("evolution", "Это эволюция.", "That's evolution."),
    "мебель": ("furniture", "Купили мебель.", "We bought furniture."),
    "типичный": ("typical", "Типичный случай.", "A typical case."),
    "пустыня": ("desert", "Мы в пустыне.", "We're in the desert."),
    "оригинальный": ("original", "Оригинальная идея.", "An original idea."),
    "внутрь": ("inside", "Положи внутрь.", "Put it inside."),
    "обида": ("offense, resentment", "Без обиды.", "No offense."),
    "призывать": (
        "to call for, to urge",
        "Они призывают к миру.",
        "They're calling for peace.",
    ),
    "сочетание": (
        "combination",
        "Странное сочетание.",
        "A strange combination.",
    ),
    "заканчиваться": (
        "to end, to run out",
        "Фильм заканчивается.",
        "The movie's ending.",
    ),
    "вооружение": ("weaponry, arms", "Новое вооружение.", "New weaponry."),
    "чашка": ("cup", "Мне нужна чашка кофе.", "I need a cup of coffee."),
    "справка": ("certificate", "Нужна справка.", "I need a certificate."),
    "прокуратура": (
        "prosecutor's office",
        "Звонили из прокуратуры.",
        "The prosecutor's office called.",
    ),
    "артист": ("performer, actor", "Артист вышел.", "The performer came out."),
    "пожелать": ("to wish", "Пожелай мне удачи.", "Wish me luck."),
    "съезд": (
        "congress, convention",
        "Съезд завтра.",
        "The congress is tomorrow.",
    ),
    "профессионал": (
        "professional",
        "Он настоящий профессионал.",
        "He's a true professional.",
    ),
    "позади": ("behind", "Он позади.", "He's behind."),
    "приобретение": (
        "purchase, acquisition",
        "Новое приобретение.",
        "A new purchase.",
    ),
    "принц": ("prince", "Где принц?", "Where's the prince?"),
    "график": ("schedule", "Какой у тебя график?", "What's your schedule?"),
    "отдохнуть": ("to rest", "Мне нужно отдохнуть.", "I need to rest."),
    "философ": ("philosopher", "Он философ.", "He's a philosopher."),
    "превратить": (
        "to turn into",
        "Не преврати это в игру.",
        "Don't turn this into a game.",
    ),
    "сдавать": (
        "to take (an exam), to hand in",
        "Я сдаю экзамен.",
        "I'm taking an exam.",
    ),
    "племя": ("tribe, clan", "Всё племя приехало.", "The whole clan showed up."),
    "ветка": ("branch", "Ветка упала.", "The branch fell."),
    "сталкиваться": (
        "to run into, to encounter",
        "Я часто с этим сталкиваюсь.",
        "I run into this a lot.",
    ),
    "гнев": ("anger", "Это гнев.", "That's anger."),
    "захотеться": (
        "to feel like",
        "Мне захотелось кофе.",
        "I felt like having coffee.",
    ),
    "почтовый": (
        "postal, mail",
        "Это почтовый адрес.",
        "This is a postal address.",
    ),
    "слабость": ("weakness", "Это моя слабость.", "That's my weakness."),
    "целиком": ("whole, entirely", "Съел целиком.", "Ate it whole."),
    "консультант": ("consultant", "Он консультант.", "He's a consultant."),
    "крепость": ("fortress", "Старая крепость.", "An old fortress."),
    "церковный": ("church (adj.)", "Церковный праздник.", "A church holiday."),
    "разделять": (
        "to share, to divide",
        "Я не разделяю это мнение.",
        "I don't share that view.",
    ),
    "разбираться": (
        "to know about, to figure out",
        "Я в этом не разбираюсь.",
        "I don't know about this.",
    ),
    "правление": ("board, rule", "Новое правление.", "A new board."),
    "сладкий": ("sweet", "Слишком сладкий.", "Too sweet."),
    "видать": (
        "apparently",
        "Видать, он уже ушёл.",
        "Apparently he already left.",
    ),
    "ствол": ("trunk", "Ствол дерева толстый.", "The tree trunk is thick."),
    "завершить": (
        "to complete, to finish",
        "Нужно завершить работу.",
        "Need to finish the work.",
    ),
    "дождаться": ("to wait for", "Дождись меня.", "Wait for me."),
    "независимость": (
        "independence",
        "Борются за независимость.",
        "They're fighting for independence.",
    ),
    "недавний": ("recent", "Недавний случай.", "A recent case."),
    "долина": ("valley", "Внизу долина.", "There's a valley below."),
    "довести": (
        "to bring to, to see through",
        "Доведи до конца.",
        "See it through.",
    ),
    "каталог": ("catalog", "Посмотри в каталоге.", "Look in the catalog."),
    "забор": ("fence", "Забор высокий.", "The fence is high."),
    "фото": ("photo", "Покажи фото.", "Show the photo."),
    "суровый": ("harsh, severe", "Зима суровая.", "The winter is harsh."),
    "невероятный": (
        "incredible",
        "Невероятная история.",
        "An incredible story.",
    ),
    "пресс": ("abs", "У него сильный пресс.", "He's got strong abs."),
    "законный": (
        "legal, lawful",
        "Это законное требование.",
        "That's a legal requirement.",
    ),
    "коллекция": (
        "collection",
        "У неё большая коллекция.",
        "She has a big collection.",
    ),
    "благодарность": ("gratitude", "Из благодарности.", "Out of gratitude."),
    "мгновенно": (
        "instantly",
        "Он мгновенно понял.",
        "He understood instantly.",
    ),
    "преодолеть": (
        "to overcome",
        "Ты это преодолеешь.",
        "You will overcome this.",
    ),
    "пугать": ("to scare", "Не пугай меня.", "Don't scare me."),
    "целовать": ("to kiss", "Не целуй меня.", "Don't kiss me."),
    "испугаться": ("to get scared", "Я испугался.", "I got scared."),
    "отчаяние": ("despair", "Это уже отчаяние.", "This is despair."),
    "спрятать": (
        "to hide",
        "Мне нужно спрятать подарок.",
        "I need to hide the gift.",
    ),
    "призвать": (
        "to draft, to call up",
        "Его призвали в армию.",
        "He was drafted.",
    ),
    "некогда": ("no time", "Мне некогда.", "I have no time."),
    "награда": ("award", "Он получил награду.", "He got an award."),
    "обыкновенный": ("ordinary", "Обыкновенный день.", "An ordinary day."),
    "поделиться": ("to share", "Поделись со мной.", "Share with me."),
    "добыча": ("haul, loot", "Это наша добыча.", "This is our haul."),
    "своеобразный": (
        "distinctive, peculiar",
        "Вкус своеобразный.",
        "The taste is distinctive.",
    ),
    "противный": (
        "nasty, disgusting",
        "Какой противный запах.",
        "What a nasty smell.",
    ),
    "царство": ("kingdom", "Это его царство.", "This is his kingdom."),
}

stats = rewrite_chunk(
    Path("russian_english/_chunks/deck_15260192_04.csv"),
    fixes,
)
print(stats)

leftover = []
cards = cards_from_path(Path(stats["path"]))
for i, card in enumerate(cards, 1):
    payload = card_write_payload(card)
    lemma = lemma_from_card(card)
    gloss = answer_lemma_from_card(card)
    ru = payload["question"].split("## Footnote")[-1].strip()
    en = payload["answer"].split("## Footnote")[-1].strip()
    extra_en = _gloss_parts(gloss)
    extra_ru = {lemma.lower().replace("ё", "е")}
    stem = lemma[:4].replace("ё", "е") if len(lemma) >= 4 else lemma.replace("ё", "е")
    if stem.lower() not in ru.lower().replace("ё", "е"):
        leftover.append(f"{i} LEMMA {lemma} :: {ru}")
    gloss_ok = False
    en_l = en.lower()
    for part in _gloss_parts(gloss):
        if part in en_l:
            gloss_ok = True
            break
        if any(
            tok.lower().startswith(part[:4])
            for tok in _tokens(en)
            if part[:4].isalpha() and len(part) >= 4
        ):
            gloss_ok = True
            break
    if not gloss_ok:
        leftover.append(f"{i} GLOSS {gloss} :: {en}")
    for tok in _tokens(en):
        if not _en_ok(tok, extra_en):
            leftover.append(f"{i} EN {tok} :: {en}")
    for tok in _tokens(ru):
        if not _ru_ok(tok, extra_ru):
            leftover.append(f"{i} RU {tok} :: {ru}")

print(f"leftovers={len(leftover)}")
if leftover:
    print("\n".join(leftover))
