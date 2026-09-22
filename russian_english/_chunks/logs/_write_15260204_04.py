import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from brainscape import answer_lemma_from_card, card_write_payload, cards_from_path, lemma_from_card
from russian_english._chunk_io import rewrite_chunk

PACK = REPO / "russian_english"
SRC = PACK / "_chunks" / "deck_15260204_04.csv"

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
    for line in (PACK / "_vocab" / "allow_en_15260204.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_ru = {
    line.strip().replace("ё", "е").lower()
    for line in (PACK / "_vocab" / "allow_ru_15260204.txt").read_text(encoding="utf-8").splitlines()
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
    "caught": "catch", "shone": "shine", "teeth": "tooth",
}

IRREGULAR_RU = {
    "может": "мочь", "могу": "мочь", "можем": "мочь",
    "хочу": "хотеть", "хочет": "хотеть", "хотим": "хотеть",
    "вижу": "видеть", "видишь": "видеть", "видит": "видеть",
    "знаю": "знать", "живу": "жить", "живет": "жить", "живёт": "жить",
    "шла": "идти", "шел": "идти", "шёл": "идти", "шли": "идти",
    "идет": "идти", "идёт": "идти", "идем": "идти", "идём": "идти",
    "стал": "стать", "стала": "стать", "стали": "стать",
    "поет": "петь", "поёт": "петь", "поют": "петь",
    "вышел": "выйти", "вышла": "выйти",
    "пришла": "прийти", "пришел": "прийти", "пришёл": "прийти", "пришли": "прийти",
    "взял": "взять", "взяла": "взять",
    "стоит": "стоять", "стоят": "стоять", "стоял": "стоять",
    "гласит": "гласить",
    "сдамся": "сдаться",
    "уловил": "уловить",
    "расположились": "расположиться",
    "надень": "надеть",
    "смени": "сменить",
    "нажми": "нажать",
    "купи": "купить",
    "лей": "лить",
    "посмотри": "посмотреть",
    "сядь": "сесть",
}


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
    "толком": ("properly", "Я не понял толком.", "I did not get it properly."),
    "ниша": ("niche", "Это его ниша.", "This is his niche."),
    "сдаться": ("give up", "Пора сдаться.", "Time to give up."),
    "презерватив": ("condom", "Возьми презерватив.", "Take a condom."),
    "чеченец": ("Chechen", "Он чеченец.", "He is Chechen."),
    "гласить": ("state", "Закон гласит так.", "The law states this."),
    "добровольный": ("voluntary", "Это добровольный шаг.", "This is a voluntary step."),
    "враждебный": ("hostile", "Он такой враждебный.", "He is so hostile."),
    "удаление": ("removal", "Удаление уже началось.", "The removal already began."),
    "немногий": ("few", "Немногие пришли.", "Few came."),
    "сказаться": ("affect", "Это может сказаться.", "This can affect us."),
    "восстанавливать": ("restore", "Мы восстанавливаем дом.", "We are restoring the house."),
    "восхищаться": ("admire", "Я восхищаюсь тобой.", "I admire you."),
    "относить": ("take", "Я отношу книги домой.", "I take the books home."),
    "распахнуть": ("throw open", "Распахни дверь.", "Throw open the door."),
    "кора": ("bark", "Кора дерева сухая.", "The tree bark is dry."),
    "круто": ("cool", "Это круто.", "That's cool."),
    "неправда": ("lie", "Это неправда.", "This is a lie."),
    "криминальный": ("criminal", "Это криминальный мир.", "This is a criminal world."),
    "уловить": ("catch", "Я уловил смысл.", "I can catch the meaning."),
    "расположиться": ("settle", "Мы расположились здесь.", "We settled here."),
    "добровольно": ("voluntarily", "Он пришёл добровольно.", "He came voluntarily."),
    "поверх": ("over", "Надень это поверх пальто.", "Put this over the coat."),
    "бедствие": ("disaster", "Это бедствие.", "This is a disaster."),
    "барон": ("baron", "Барон уже здесь.", "The baron is already here."),
    "тяга": ("craving", "У него тяга к этому.", "He has a craving for this."),
    "скользить": ("slide", "Не скользи.", "Do not slide."),
    "хирург": ("surgeon", "Хирург уже здесь.", "The surgeon is already here."),
    "рыбак": ("fisherman", "Рыбак на реке.", "The fisherman is on the river."),
    "фотоаппарат": ("camera", "Где мой фотоаппарат?", "Where is my camera?"),
    "рычаг": ("lever", "Нажми на рычаг.", "Press the lever."),
    "недоступный": ("inaccessible", "Это недоступный остров.", "This is an inaccessible island."),
    "простыня": ("sheet", "Смени простыню.", "Change the sheet."),
    "формально": ("formally", "Он формально прав.", "He is formally right."),
    "израильский": ("Israeli", "Это израильский город.", "This is an Israeli city."),
    "наименование": ("name", "Какое наименование?", "What is the name?"),
    "девяносто": ("ninety", "Ей девяносто лет.", "She is ninety."),
    "заинтересованный": ("interested", "Я заинтересован.", "I am interested."),
    "прикладной": ("applied", "Это прикладной курс.", "This is an applied course."),
    "диаметр": ("diameter", "Какой диаметр?", "What is the diameter?"),
    "смотреться": ("look", "Как я смотрюсь?", "How do I look?"),
    "колокол": ("bell", "Колокол звонит.", "The bell is ringing."),
    "побеждать": ("win", "Он любит побеждать.", "He loves to win."),
    "одетый": ("dressed", "Мальчик уже одетый.", "The boy is already dressed."),
    "аукцион": ("auction", "Картина на аукционе.", "The painting is at auction."),
    "стон": ("moan", "Я слышал стон.", "I heard a moan."),
    "проститутка": ("prostitute", "Она работала проституткой.", "She worked as a prostitute."),
    "неизменно": ("invariably", "Он неизменно прав.", "He is invariably right."),
    "противоположность": ("opposite", "Она моя противоположность.", "She is my opposite."),
    "пятьсот": ("five hundred", "Мне нужно пятьсот.", "I need five hundred."),
    "увлекаться": ("be into", "Она увлекается спортом.", "She is into sport."),
    "поглядывать": ("glance", "Он стал поглядывать на часы.", "He began to glance at the clock."),
    "варить": ("boil", "Я буду варить суп.", "I will boil soup."),
    "исламский": ("Islamic", "Это исламский праздник.", "This is an Islamic holiday."),
    "чистить": ("clean", "Я буду чистить зубы.", "I will clean my teeth."),
    "месторождение": ("deposit", "Это месторождение нефти.", "This is an oil deposit."),
    "маркетинговый": ("marketing", "Это маркетинговый план.", "This is a marketing plan."),
    "теряться": ("get lost", "Не теряйся здесь.", "Do not get lost here."),
    "отразиться": ("affect", "Это отразится на нас.", "This will affect us."),
    "фирменный": ("branded", "Это фирменный знак.", "This is a branded sign."),
    "пустяк": ("trifle", "Это пустяк.", "This is a trifle."),
    "очаг": ("hearth", "Сядь у очага.", "Sit by the hearth."),
    "спеть": ("sing", "Она хочет спеть.", "She wants to sing."),
    "символический": ("symbolic", "Это символический жест.", "This is a symbolic gesture."),
    "гладить": ("iron", "Нужно гладить рубашку.", "I need to iron the shirt."),
    "удалиться": ("withdraw", "Он решил удалиться.", "He decided to withdraw."),
    "компромисс": ("compromise", "Нам нужен компромисс.", "We need a compromise."),
    "выставлять": ("exhibit", "Они выставляют картины.", "They exhibit paintings."),
    "забраться": ("climb", "Он хочет забраться туда.", "He wants to climb there."),
    "жилец": ("tenant", "Новый жилец пришёл.", "A new tenant came."),
    "смелость": ("courage", "Ему нужна смелость.", "He needs courage."),
    "солнышко": ("sunshine", "Солнышко уже здесь.", "The sunshine is already here."),
    "грузинский": ("Georgian", "Я люблю грузинский чай.", "I love Georgian tea."),
    "капуста": ("cabbage", "Купи капусту.", "Buy cabbage."),
    "уменьшаться": ("decrease", "Боль стала уменьшаться.", "The pain began to decrease."),
    "нервно": ("nervously", "Она нервно ждала.", "She waited nervously."),
    "обедать": ("have lunch", "Мы будем обедать.", "We will have lunch."),
    "печально": ("sadly", "Он печально смотрел.", "He looked sadly."),
    "инновационный": ("innovative", "Это инновационный план.", "This is an innovative plan."),
    "дружно": ("together", "Они дружно работают.", "They work together."),
    "меж": ("between", "Меж нами тайна.", "A secret between us."),
    "воображать": ("imagine", "Он любит воображать.", "He loves to imagine."),
    "сказываться": ("affect", "Стресс сказывается на здоровье.", "Stress affects health."),
    "бессмертный": ("immortal", "Он хочет быть бессмертным.", "He wants to be immortal."),
    "смутный": ("vague", "У меня смутный план.", "I have a vague plan."),
    "погибший": ("deceased", "Погибший был молод.", "The deceased was young."),
    "газетный": ("newspaper", "Газетная статья.", "A newspaper article."),
    "выкинуть": ("throw out", "Выкинь это.", "Throw this out."),
    "тематика": ("theme", "Какая тематика?", "What is the theme?"),
    "погрузиться": ("immerse", "Он хочет погрузиться в работу.", "He wants to immerse himself in work."),
    "розничный": ("retail", "Это розничный магазин.", "This is a retail store."),
    "путешественник": ("traveler", "Путешественник уже здесь.", "The traveler is already here."),
    "сажать": ("plant", "Я буду сажать деревья.", "I will plant trees."),
    "тройка": ("trio", "Это наша тройка.", "This is our trio."),
    "ка": ("just", "Посмотри-ка сюда.", "Just look here."),
    "обладатель": ("holder", "Он обладатель приза.", "He is the prize holder."),
    "индеец": ("Indian", "Он индеец.", "He is Indian."),
    "отчаянно": ("desperately", "Она отчаянно ждала.", "She waited desperately."),
    "задержаться": ("stay", "Я решил задержаться.", "I decided to stay."),
    "лить": ("pour", "Я буду лить воду.", "I will pour water."),
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
