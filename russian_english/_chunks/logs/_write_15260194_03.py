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
SRC = PACK / "_chunks" / "deck_15260194_03.csv"

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
    "one", "onto", "doesnt",
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
    for line in (PACK / "_vocab" / "allow_en_15260194.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_ru = {
    line.strip().replace("ё", "е").lower()
    for line in (PACK / "_vocab" / "allow_ru_15260194.txt").read_text(encoding="utf-8").splitlines()
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
    "waits": "wait", "grows": "grow", "lives": "live", "opens": "open",
    "looks": "look", "reads": "read", "walks": "walk", "writes": "write",
    "sends": "send", "strives": "strive", "threatens": "threaten",
    "identified": "identify", "deserved": "deserve", "refused": "refuse",
    "descended": "descend",
}

IRREGULAR_RU = {
    "может": "мочь", "могу": "мочь", "можем": "мочь",
    "хочу": "хотеть", "хочет": "хотеть", "хотим": "хотеть",
    "вижу": "видеть", "видишь": "видеть", "видит": "видеть",
    "знаю": "знать", "живу": "жить", "живет": "жить", "живёт": "жить",
    "шла": "идти", "шел": "идти", "шёл": "идти", "шли": "идти",
    "идет": "идти", "идёт": "идти", "идем": "идти", "идём": "идти",
    "стал": "стать", "стала": "стать", "стали": "стать",
    "пришла": "прийти", "пришел": "прийти", "пришёл": "прийти",
    "взял": "взять", "взяла": "взять",
    "стоит": "стоять", "стоят": "стоять",
    "сплю": "спать", "спит": "спать",
    "смотри": "смотреть",
    "жди": "ждать", "ждёт": "ждать", "ждет": "ждать",
    "дай": "дать",
    "пишет": "писать", "пишу": "писать",
    "ушел": "уйти", "ушёл": "уйти", "ушла": "уйти",
    "дается": "даваться", "даётся": "даваться",
    "ври": "врать", "врите": "врать",
    "брожу": "бродить", "бродим": "бродить",
}


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
    return False


FIXES = {
    "сплошной": ("solid", "Стена сплошная.", "The wall is solid."),
    "невидимый": ("invisible", "Он почти невидимый.", "He's almost invisible."),
    "радостный": ("joyful", "Её смех радостный.", "Her laughter is joyful."),
    "академик": (
        "academician",
        "Академик читает лекцию.",
        "The academician reads a lecture.",
    ),
    "оттого": (
        "therefore",
        "Уже поздно, оттого я сплю.",
        "It's already late, therefore I sleep.",
    ),
    "роды": ("birth", "Роды прошли хорошо.", "The birth went well."),
    "эй": ("hey", "Эй, подожди меня!", "Hey, wait for me!"),
    "записывать": ("to write down", "Записывай это.", "Write this down."),
    "трасса": ("route", "Это длинная трасса.", "That's a long route."),
    "социалистический": (
        "socialist",
        "Это социалистическая партия.",
        "That's a socialist party.",
    ),
    "таки": ("after all", "Он таки пришёл.", "He came after all."),
    "нету": ("none", "Молока нету.", "There's none."),
    "даваться": (
        "to come",
        "Это будет даваться легко.",
        "This will come easily.",
    ),
    "угрожать": ("to threaten", "Он угрожает соседу.", "He threatens the neighbor."),
    "поместить": ("to place", "Помести книгу сюда.", "Place the book here."),
    "продвижение": (
        "promotion",
        "Она ждёт продвижение.",
        "She waits for a promotion.",
    ),
    "проиграть": ("to lose", "Я не хочу проиграть.", "I don't want to lose."),
    "кругом": ("around", "Смотри кругом.", "Look around."),
    "предоставление": (
        "provision",
        "Это предоставление помощи.",
        "That's the provision of help.",
    ),
    "первоначальный": (
        "initial",
        "Это первоначальный план.",
        "That's the initial plan.",
    ),
    "вложить": ("to invest", "Вложи капитал.", "Invest the capital."),
    "протест": ("protest", "Это большой протест.", "That's a big protest."),
    "ограниченный": ("limited", "Время ограничено.", "Time is limited."),
    "выносить": ("to endure", "Я не выношу боль.", "I can't endure the pain."),
    "сооружение": (
        "structure",
        "Это старое сооружение.",
        "That's an old structure.",
    ),
    "развитый": (
        "developed",
        "Это развитая страна.",
        "That's a developed country.",
    ),
    "сравнивать": ("to compare", "Не сравнивай нас.", "Don't compare us."),
    "разместить": ("to place", "Размести гостей здесь.", "Place the guests here."),
    "тяжесть": ("weight", "Я чувствую тяжесть.", "I feel the weight."),
    "бытовой": ("household", "Это бытовой вопрос.", "That's a household matter."),
    "лечить": ("to treat", "Врач лечит пациента.", "The doctor treats the patient."),
    "запрет": ("ban", "Это полный запрет.", "That's a full ban."),
    "бюджетный": ("budget", "Это бюджетный вариант.", "That's a budget option."),
    "выгода": ("benefit", "В этом есть выгода.", "There's a benefit in this."),
    "уголок": ("corner", "Это тихий уголок.", "That's a quiet corner."),
    "максимум": ("maximum", "Это мой максимум.", "That's my maximum."),
    "перерыв": ("break", "Сделаем перерыв.", "Take a break."),
    "тренер": ("coach", "Тренер ждёт команду.", "The coach waits for the team."),
    "москвич": ("Muscovite", "Я москвич.", "I'm a Muscovite."),
    "верх": ("top", "Смотри на верх.", "Look at the top."),
    "удовлетворить": (
        "to satisfy",
        "Это удовлетворит желание.",
        "This will satisfy the wish.",
    ),
    "опуститься": (
        "to descend",
        "Он опустился на землю.",
        "He descended to the ground.",
    ),
    "подавлять": (
        "to suppress",
        "Не подавляй чувство.",
        "Don't suppress the feeling.",
    ),
    "изобразить": ("to depict", "Изобрази эту картину.", "Depict this picture."),
    "шляпа": ("hat", "Где моя шляпа?", "Where's my hat?"),
    "репутация": (
        "reputation",
        "У него хорошая репутация.",
        "He has a good reputation.",
    ),
    "добиваться": (
        "to strive for",
        "Она добивается цели.",
        "She strives for the goal.",
    ),
    "гроб": ("coffin", "Гроб уже в земле.", "The coffin is already in the ground."),
    "ошибиться": (
        "to make a mistake",
        "Я не хочу ошибиться.",
        "I don't want to make a mistake.",
    ),
    "повышенный": (
        "increased",
        "Это повышенный риск.",
        "That's an increased risk.",
    ),
    "поздравлять": (
        "to congratulate",
        "Мы поздравляем тебя.",
        "We congratulate you.",
    ),
    "употребление": ("use", "Это употребление слова.", "That's the use of the word."),
    "напечатать": ("to print", "Напечатай этот текст.", "Print this text."),
    "выявить": (
        "to identify",
        "Мы выявили причину.",
        "We identified the reason.",
    ),
    "бассейн": ("pool", "Я в бассейне.", "I'm at the pool."),
    "радостно": ("joyfully", "Она радостно живёт.", "She lives joyfully."),
    "мэр": ("mayor", "Мэр открывает парк.", "The mayor opens the park."),
    "пояснить": ("to explain", "Поясни смысл.", "Explain the meaning."),
    "заявка": ("application", "Где моя заявка?", "Where's my application?"),
    "внедрение": (
        "implementation",
        "Это новое внедрение.",
        "That's a new implementation.",
    ),
    "валюта": ("currency", "Это сильная валюта.", "That's a strong currency."),
    "максимально": (
        "maximally",
        "Сделай это максимально быстро.",
        "Do this maximally quickly.",
    ),
    "врать": ("to lie", "Он хочет врать.", "He wants to lie."),
    "кабина": ("cabin", "Войди в кабину.", "Go into the cabin."),
    "системный": (
        "systemic",
        "Это системная проблема.",
        "That's a systemic problem.",
    ),
    "милиционер": (
        "policeman",
        "Милиционер идёт сюда.",
        "The policeman walks here.",
    ),
    "прокурор": ("prosecutor", "Прокурор в суде.", "The prosecutor is in court."),
    "критик": ("critic", "Критик пишет отзыв.", "The critic writes a review."),
    "служебный": (
        "official",
        "Это служебный вход.",
        "That's an official entrance.",
    ),
    "бродить": ("to wander", "Мы бродим по лесу.", "We wander through the forest."),
    "проговорить": ("to say", "Проговори эту фразу.", "Say this phrase."),
    "носитель": ("carrier", "Он носитель языка.", "He's a language carrier."),
    "неизбежный": (
        "inevitable",
        "Это неизбежный конец.",
        "That's an inevitable end.",
    ),
    "куртка": ("jacket", "Где моя куртка?", "Where's my jacket?"),
    "отчасти": ("partly", "Это отчасти правда.", "That's partly true."),
    "непонятно": ("unclear", "Мне это непонятно.", "This is unclear to me."),
    "отказать": (
        "to refuse",
        "Они отказали в просьбе.",
        "They refused the request.",
    ),
    "общественность": (
        "public",
        "Общественность хочет ответ.",
        "The public wants an answer.",
    ),
    "актив": ("asset", "Это актив банка.", "That's a bank asset."),
    "численность": (
        "number",
        "Численность армии растёт.",
        "The army's number grows.",
    ),
    "обойти": ("to bypass", "Обойди этот дом.", "Bypass this house."),
    "незаметно": ("unnoticed", "Он незаметно ушёл.", "He left unnoticed."),
    "заслужить": ("to deserve", "Он заслужил успех.", "He deserved success."),
    "отправлять": ("to send", "Я отправляю письмо.", "I send a letter."),
    "кладбище": ("cemetery", "Мы идём на кладбище.", "We go to the cemetery."),
    "эхо": ("echo", "Я слышу эхо.", "I hear the echo."),
    "утратить": ("to lose", "Не утрать силу.", "Don't lose strength."),
    "славный": ("nice", "Он славный парень.", "He's a nice guy."),
    "евро": ("euro", "У меня мало евро.", "I have little euro."),
    "посадка": ("landing", "Посадка была поздней.", "The landing was late."),
    "ровный": ("even", "Дорога ровная.", "The road is even."),
    "икона": ("icon", "Икона в церкви.", "The icon is in the church."),
    "последовательность": (
        "sequence",
        "Это важная последовательность.",
        "That's an important sequence.",
    ),
    "двести": (
        "two hundred",
        "Там двести человек.",
        "There are two hundred people.",
    ),
    "вчерашний": (
        "yesterday's",
        "Это вчерашний хлеб.",
        "That's yesterday's bread.",
    ),
    "добавлять": ("to add", "Добавляй сахар.", "Add sugar."),
    "ботинок": ("shoe", "Где мой ботинок?", "Where's my shoe?"),
    "шоу": ("show", "Это хорошее шоу.", "That's a good show."),
    "удобно": ("comfortably", "Мне удобно сидеть.", "I sit comfortably."),
    "штаны": ("trousers", "Где мои штаны?", "Where are my trousers?"),
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
