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
    "there's", "where's", "when's", "what's", "who's", "how's", "isn't",
    "there", "here", "very", "too", "now", "today", "yesterday", "tomorrow",
    "some", "any", "all", "no", "yes", "do", "does", "did", "have", "has",
    "had", "will", "would", "can", "could", "should", "must", "may", "might",
    "please", "more", "most", "less", "much", "many", "few", "such", "also",
    "only", "even", "still", "already", "always", "never", "often", "once",
    "after", "before", "under", "over", "through", "between", "without",
    "who", "what", "when", "where", "why", "how", "which",
    "ago", "ones", "two", "down", "up", "out", "off", "back",
    "herself", "himself", "themselves", "myself", "yourself",
    "one", "onto", "dont", "doesnt", "lets", "got",
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
    "такой", "такая", "такое", "такие", "так", "какой",
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
    "forgot": "forget", "rang": "ring",
}

IRREGULAR_RU = {
    "идет": "идти", "иду": "идти", "шел": "идти", "шла": "идти", "шли": "идти",
    "нужна": "нужный", "нужен": "нужный", "нужно": "нужный",
    "болит": "болеть", "смотрит": "смотреть", "смотри": "смотреть",
    "люблю": "любить", "начал": "начать", "начала": "начать",
    "ест": "есть",
    "может": "мочь", "хочет": "хотеть", "хочу": "хотеть",
    "превращается": "превращаться",
    "обернись": "обернуться",
    "подай": "подавать",
    "знаю": "знать",
}

RU_ENDINGS = (
    "ами", "ями", "ого", "его", "ому", "ему", "ыми", "ими", "ой", "ей", "ом",
    "ем", "ах", "ях", "ам", "ям", "ов", "ев", "ую", "юю", "ая", "яя", "ое",
    "ее", "ые", "ие", "ый", "ий", "лся", "лась", "лось", "лись", "ться", "тся",
    "ешь", "ишь", "ете", "ите", "ут", "ют", "ат", "ят", "ет", "ит",
    "ла", "ло", "ли", "ть", "ти", "ся", "сь",
    "а", "я", "у", "ю", "е", "и", "ы", "о", "ь", "л",
)

allow_en = {
    line.strip().lower()
    for line in (PACK / "_vocab" / "allow_en_15260191.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_ru = {
    line.strip().replace("ё", "е").lower()
    for line in (PACK / "_vocab" / "allow_ru_15260191.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_en |= FUNCTION_EN
allow_ru |= FUNCTION_RU


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


print(
    rewrite_chunk(
        Path("russian_english/_chunks/deck_15260191_04.csv"),
        {
            "защитить": ("to protect, to defend", "Защити меня.", "Protect me."),
            "остановка": ("stop, bus stop", "Это моя остановка.", "This is my stop."),
            "дорого": ("expensive", "Это слишком дорого.", "That's too expensive."),
            "жестокий": ("cruel, brutal", "Он жестокий.", "He's cruel."),
            "крепко": ("tightly, firmly", "Держи крепко.", "Hold tightly."),
            "решиться": ("to make up one's mind, to dare", "Она наконец решилась.", "She finally made up her mind."),
            "реально": ("really, for real", "Это реально?", "Is that really so?"),
            "лишить": ("to deprive, to strip", "Его лишили работы.", "They deprived him of work."),
            "выходной": ("day off", "Завтра у нас выходной.", "We have the day off tomorrow."),
            "административный": ("administrative", "Это административный вопрос.", "That's an administrative question."),
            "дрожать": ("to tremble, to shiver", "Я дрожу от страха.", "I tremble from fear."),
            "близко": ("close, near", "Дом очень близко.", "The house is very close."),
            "плод": ("fruit", "Это плод её труда.", "That's the fruit of her labor."),
            "судно": ("ship, vessel", "Судно уже в порту.", "The ship's already in port."),
            "борт": ("board, side", "Все на борт!", "All on board!"),
            "проживать": ("to reside, to live", "Он проживает здесь.", "He resides here."),
            "самостоятельно": ("independently, on one's own", "Это надо сделать самостоятельно.", "Do it independently."),
            "соединение": ("connection, compound", "Плохое соединение.", "Bad connection."),
            "впоследствии": ("afterwards, subsequently", "Впоследствии всё ясно.", "Afterwards it was clear."),
            "контракт": ("contract", "Вот контракт.", "Here's the contract."),
            "диалог": ("dialogue", "Это диалог.", "This is a dialogue."),
            "пахнуть": ("to smell", "Хлеб пахнет.", "The bread smells."),
            "заговорить": ("to start talking", "Он вдруг заговорил.", "He suddenly started to talk."),
            "свадьба": ("wedding", "Когда свадьба?", "When's the wedding?"),
            "туман": ("fog, mist", "На улице туман.", "There's fog outside."),
            "прибор": ("device, appliance", "Этот прибор новый.", "This device is new."),
            "восторг": ("delight", "Какой восторг!", "What a delight!"),
            "подчеркнуть": ("to emphasize, to underline", "Надо это подчеркнуть.", "I want to emphasize that."),
            "лорд": ("lord", "Где лорд?", "Where's the lord?"),
            "качественный": ("high-quality", "Это качественная вещь.", "This is a high-quality thing."),
            "точность": ("accuracy, precision", "Здесь важна точность.", "Accuracy is important here."),
            "превращаться": ("to turn into", "День превращается в ночь.", "Day turns into night."),
            "выпускать": ("to release, to issue", "Они выпускают новый фильм.", "They release a new movie."),
            "высказать": ("to express, to voice", "Надо высказать мнение.", "I want to express my opinion."),
            "девчонка": ("girl", "Где девчонка?", "Where's the girl?"),
            "персонал": ("staff, personnel", "Там хороший персонал.", "The staff there is good."),
            "тайный": ("secret", "Это тайный план.", "That's a secret plan."),
            "воскликнуть": ("to exclaim", "Она воскликнула громко.", "She exclaimed loudly."),
            "майор": ("major", "Он майор, не капитан.", "He's a major, not a captain."),
            "оценивать": ("to evaluate, to assess", "Как ты это оцениваешь?", "How do you evaluate this?"),
            "обернуться": ("to turn around, to turn out", "Обернись!", "Turn around!"),
            "молчание": ("silence", "Мне нужно молчание.", "I need silence."),
            "побежать": ("to run, to dash", "Он побежал в магазин.", "He will run to the store."),
            "мальчишка": ("boy, lad", "Мальчишка опять здесь.", "The boy is here again."),
            "особенный": ("special, particular", "У неё есть особенный талант.", "She has a special talent."),
            "предоставлять": ("to provide, to grant", "Они предоставляют помощь.", "They provide help."),
            "раздаться": ("to ring out", "Раздался звонок.", "The call will ring out."),
            "оператор": ("operator", "Где оператор?", "Where's the operator?"),
            "конституция": ("constitution", "Это против конституции.", "That's against the constitution."),
            "развивать": ("to develop", "Надо развивать бизнес.", "We need to develop the business."),
            "пустить": ("to let, to release", "Пусти меня!", "Let me in!"),
            "карточка": ("card", "У меня нет карточки.", "I don't have my card."),
            "подавать": ("to pass, to serve", "Подай чай.", "Pass the tea."),
            "поразить": ("to amaze, to strike", "Это меня поразило.", "That amazed me."),
            "кодекс": ("code", "Это кодекс.", "This is the code."),
            "аналогичный": ("similar, analogous", "У нас аналогичная проблема.", "We have a similar problem."),
            "беременность": ("pregnancy", "Это её первая беременность.", "This is her first pregnancy."),
            "хранить": ("to keep, to store", "Где это хранить?", "Where should I keep this?"),
            "исследователь": ("researcher", "Она исследователь.", "She's a researcher."),
            "исчезать": ("to disappear, to vanish", "Деньги исчезают слишком быстро.", "The money disappears too fast."),
            "француз": ("Frenchman", "Он француз.", "He's a Frenchman."),
            "замуж": ("married, to marry", "Она уже замуж.", "She is married now."),
            "препарат": ("medication, drug", "Где препарат?", "Where's the medication?"),
            "игрушка": ("toy", "Где моя игрушка?", "Where's my toy?"),
            "весело": ("fun, cheerfully", "Нам было весело.", "We had fun."),
            "конструкция": ("construction, structure", "Странная конструкция.", "A strange construction."),
            "сезон": ("season", "Зима мой любимый сезон.", "Winter is my favorite season."),
            "самостоятельный": ("independent", "Он уже самостоятельный.", "He's independent now."),
            "формула": ("formula", "Я не знаю формулу.", "I don't know the formula."),
            "рассмотрение": ("consideration, review", "Это на рассмотрении.", "It's under consideration."),
            "заглянуть": ("to drop by, to look in", "Я загляну завтра.", "I will drop by tomorrow."),
            "пробовать": ("to try, to taste", "Давай пробовать.", "Let's try."),
            "посадить": ("to seat, to plant", "Посади его сюда.", "Seat him here."),
            "дон": ("the Don", "Это Дон.", "This is the Don."),
            "кулак": ("fist", "Его кулак большой.", "His fist is big."),
            "физика": ("physics", "У нас физика в два.", "We have physics at two."),
            "всеобщий": ("universal, general", "Это всеобщее мнение.", "That's the universal opinion."),
            "насилие": ("violence, abuse", "Насилие не работает.", "Violence does not work."),
            "жест": ("gesture", "Странный жест.", "A strange gesture."),
            "нанести": ("to apply, to inflict", "Нанеси краску.", "Apply the paint."),
            "исходный": ("original, initial", "Это исходный план.", "That's the original plan."),
            "вынудить": ("to force, to compel", "Его вынудили уйти.", "They forced him to leave."),
            "обслуживание": ("service, maintenance", "Обслуживание здесь хорошее.", "The service here is good."),
            "освободить": ("to free, to release", "Его уже освободили.", "They already freed him."),
            "англичанин": ("Englishman", "Он англичанин.", "He's an Englishman."),
            "бригада": ("crew, brigade", "Наша бригада уже здесь.", "Our crew is already here."),
            "вызов": ("challenge, call", "Это для меня вызов.", "That's a challenge for me."),
            "капля": ("drop", "Ни капли нет.", "There's not a drop."),
            "лаборатория": ("laboratory, lab", "Я в лаборатории.", "I'm in the laboratory."),
            "спасение": ("rescue, salvation", "Это было наше спасение.", "That was our rescue."),
            "непосредственный": ("direct, immediate", "Он мой непосредственный начальник.", "He's my direct boss."),
            "гибель": ("death, ruin", "После его гибели.", "After his death."),
            "полчаса": ("half an hour, thirty minutes", "Через полчаса.", "In half an hour."),
            "полка": ("shelf", "Книга на полке.", "The book is on the shelf."),
            "паспорт": ("passport", "Где паспорт?", "Where's the passport?"),
            "подозревать": ("to suspect", "Я его подозреваю.", "I suspect him."),
            "обязательство": ("obligation, commitment", "У меня есть обязательства.", "I have obligations."),
            "активность": ("activity", "Сегодня активность низкая.", "Activity is low today."),
            "горный": ("mountain, mountainous", "Это горный район.", "That's a mountain district."),
            "протокол": ("protocol", "Это против протокола.", "That's against protocol."),
        },
    )
)

dest = PACK / "_chunks" / "fixed" / "deck_15260191_04.csv"
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
