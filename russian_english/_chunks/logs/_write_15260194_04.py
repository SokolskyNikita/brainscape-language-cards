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
SRC = PACK / "_chunks" / "deck_15260194_04.csv"

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
    "descended": "descend", "stole": "steal", "froze": "freeze",
    "sings": "sing", "studies": "study",
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
    "шутить": ("joke", "Он любит шутить.", "He loves to joke."),
    "храниться": (
        "to be stored",
        "Документ хранится здесь.",
        "The document is stored here.",
    ),
    "батальон": ("battalion", "Батальон стоит здесь.", "The battalion stands here."),
    "показание": ("testimony", "Его показание важно.", "His testimony is important."),
    "специальность": (
        "specialty",
        "Это моя специальность.",
        "That's my specialty.",
    ),
    "повесить": ("to hang", "Повесь картину.", "Hang the picture."),
    "трогать": ("to touch", "Не трогай это.", "Don't touch this."),
    "рассчитать": (
        "to calculate",
        "Я рассчитаю сумму.",
        "I will calculate the sum.",
    ),
    "холодильник": (
        "refrigerator",
        "Молоко в холодильнике.",
        "The milk is in the refrigerator.",
    ),
    "стих": ("verse", "Это красивый стих.", "That's a beautiful verse."),
    "арестовать": (
        "to arrest",
        "Полиция арестует его.",
        "The police will arrest him.",
    ),
    "училище": ("school", "Я в училище.", "I'm at the school."),
    "копейка": ("kopeck", "У меня есть копейка.", "I have a kopeck."),
    "раненый": ("wounded", "Солдат раненый.", "The soldier is wounded."),
    "взор": ("gaze", "Её взор спокойный.", "Her gaze is calm."),
    "выбросить": ("to throw out", "Выбрось это.", "Throw this out."),
    "усмехнуться": ("to smirk", "Он усмехнулся.", "He smirked."),
    "наполнить": ("to fill", "Наполни стакан.", "Fill the glass."),
    "выскочить": ("to jump out", "Он выскочил из дома.", "He jumped out of the house."),
    "контора": ("office", "Он работает в конторе.", "He works in the office."),
    "исход": ("outcome", "Исход хороший.", "The outcome is good."),
    "террорист": ("terrorist", "Террорист здесь.", "The terrorist is here."),
    "чемодан": ("suitcase", "Где мой чемодан?", "Where's my suitcase?"),
    "коммуникация": (
        "communication",
        "Это важная коммуникация.",
        "That's important communication.",
    ),
    "подвести": ("to let down", "Он меня подвёл.", "He let me down."),
    "инвалид": (
        "disabled person",
        "Инвалид ждёт помощи.",
        "The disabled person waits for help.",
    ),
    "соблюдать": ("to observe", "Соблюдай правила.", "Observe the rules."),
    "натура": ("nature", "У неё спокойная натура.", "She has a calm nature."),
    "покачать": ("to shake", "Покачай головой.", "Shake your head."),
    "распространяться": (
        "to spread",
        "Новости распространяются быстро.",
        "The news spreads quickly.",
    ),
    "приглашение": (
        "invitation",
        "Я получил приглашение.",
        "I got an invitation.",
    ),
    "комиссар": ("commissar", "Комиссар дал приказ.", "The commissar gave an order."),
    "вскочить": ("to jump up", "Он вскочил с кровати.", "He jumped up from the bed."),
    "вслух": ("aloud", "Читай вслух.", "Read aloud."),
    "младенец": ("infant", "Младенец спит.", "The infant sleeps."),
    "развернуть": ("to unfold", "Разверни карту.", "Unfold the map."),
    "употреблять": ("to use", "Не употребляй это слово.", "Don't use this word."),
    "баланс": ("balance", "Это важный баланс.", "That's an important balance."),
    "подозрение": ("suspicion", "У меня есть подозрение.", "I have a suspicion."),
    "виза": ("visa", "Мне нужна виза.", "I need a visa."),
    "универсальный": (
        "universal",
        "Это универсальный метод.",
        "That's a universal method.",
    ),
    "послужить": ("to serve", "Это послужит уроком.", "This will serve as a lesson."),
    "размышлять": ("to reflect", "Я размышляю о жизни.", "I reflect on life."),
    "морда": ("muzzle", "У собаки большая морда.", "The dog has a big muzzle."),
    "постановка": (
        "production",
        "Это хорошая постановка.",
        "That's a good production.",
    ),
    "внимательный": (
        "attentive",
        "Он внимательный ученик.",
        "He's an attentive student.",
    ),
    "сражение": ("battle", "Сражение было долгим.", "The battle was long."),
    "фрагмент": ("fragment", "Это маленький фрагмент.", "That's a small fragment."),
    "дыра": ("hole", "В стене дыра.", "There's a hole in the wall."),
    "конкретно": ("specifically", "Говори конкретно.", "Speak specifically."),
    "ценить": ("to value", "Цени мою помощь.", "Value my help."),
    "уверенно": ("confidently", "Она уверенно говорит.", "She speaks confidently."),
    "торговать": ("to trade", "Он торгует на рынке.", "He trades at the market."),
    "подвал": ("basement", "Мы в подвале.", "We're in the basement."),
    "занятый": ("busy", "Он очень занятый.", "He's very busy."),
    "коснуться": ("to touch", "Не коснись стола.", "Don't touch the table."),
    "казать": ("to show", "Он хочет казать дорогу.", "He wants to show the road."),
    "ложный": ("false", "Это ложный ответ.", "That's a false answer."),
    "семейство": ("family", "Это большое семейство.", "That's a large family."),
    "привлекательный": (
        "attractive",
        "Он очень привлекательный.",
        "He's very attractive.",
    ),
    "плита": ("stove", "Еда на плите.", "The food is on the stove."),
    "атомный": ("atomic", "Это атомная энергия.", "That's atomic energy."),
    "прервать": ("to interrupt", "Не прерви меня.", "Don't interrupt me."),
    "заслуживать": (
        "to deserve",
        "Он заслуживает успеха.",
        "He deserves success.",
    ),
    "проход": ("passage", "Это длинный проход.", "That's a long passage."),
    "разрушение": (
        "destruction",
        "Это полное разрушение.",
        "That's complete destruction.",
    ),
    "хор": ("choir", "Хор поёт хорошо.", "The choir sings well."),
    "девица": ("maiden", "Девица ждёт ответа.", "The maiden waits for an answer."),
    "рукав": ("sleeve", "Рукав слишком длинный.", "The sleeve is too long."),
    "украсть": ("to steal", "Он хочет украсть книгу.", "He wants to steal the book."),
    "социализм": ("socialism", "Он изучает социализм.", "He studies socialism."),
    "шеф": ("boss", "Мой шеф ждёт.", "My boss waits."),
    "располагать": ("to have", "Мы располагаем временем.", "We have time."),
    "атаковать": ("to attack", "Они атакуют город.", "They attack the city."),
    "секретный": ("secret", "Это секретный план.", "That's a secret plan."),
    "столовая": ("dining room", "Мы в столовой.", "We're in the dining room."),
    "посещение": ("visit", "Это короткое посещение.", "That's a short visit."),
    "выводить": ("to take out", "Выводи собаку.", "Take the dog out."),
    "симпатичный": (
        "attractive",
        "Он симпатичный парень.",
        "He's an attractive guy.",
    ),
    "сделаться": ("to become", "Он хочет сделаться врачом.", "He wants to become a doctor."),
    "продаваться": (
        "to be sold",
        "Дом продаётся.",
        "The house is being sold.",
    ),
    "направляться": ("to head", "Мы направляемся домой.", "We're heading home."),
    "предупреждать": ("to warn", "Я предупреждаю тебя.", "I warn you."),
    "благоприятный": (
        "favorable",
        "Это благоприятный момент.",
        "That's a favorable moment.",
    ),
    "палка": ("stick", "Вот палка.", "Here's the stick."),
    "выдающийся": (
        "outstanding",
        "Это выдающийся результат.",
        "That's an outstanding result.",
    ),
    "рай": ("paradise", "Это настоящий рай.", "That's a true paradise."),
    "бровь": ("eyebrow", "Подними бровь.", "Raise your eyebrow."),
    "заснуть": ("to fall asleep", "Я хочу заснуть.", "I want to fall asleep."),
    "переводчик": (
        "translator",
        "Она хороший переводчик.",
        "She's a good translator.",
    ),
    "посреди": (
        "in the middle of",
        "Стол посреди комнаты.",
        "The table is in the middle of the room.",
    ),
    "вырваться": (
        "to break free",
        "Он вырвался из дома.",
        "He broke free from the house.",
    ),
    "эх": ("ah", "Эх, как жаль!", "Ah, what a pity!"),
    "обещание": ("promise", "Это моё обещание.", "That's my promise."),
    "совместно": ("jointly", "Мы работаем совместно.", "We work jointly."),
    "равновесие": (
        "equilibrium",
        "Он потерял равновесие.",
        "He lost his equilibrium.",
    ),
    "следователь": (
        "investigator",
        "Следователь задаёт вопрос.",
        "The investigator asks a question.",
    ),
    "замереть": ("to freeze", "Он хочет замереть.", "He wants to freeze."),
    "посольство": ("embassy", "Мы в посольстве.", "We're at the embassy."),
    "бесполезный": ("useless", "Это бесполезный совет.", "That's useless advice."),
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
