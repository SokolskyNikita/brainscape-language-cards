import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from brainscape import answer_lemma_from_card, card_write_payload, cards_from_path, lemma_from_card
from russian_english._chunk_io import rewrite_chunk

FIXES = {
    "экология": ("ecology", "Я изучаю экологию.", "I study ecology."),
    "этический": ("ethical", "Это этический вопрос.", "This is an ethical question."),
    "отрицательно": ("negatively", "Он ответил отрицательно.", "He answered negatively."),
    "рельс": ("rail", "Поезд идёт по рельсам.", "The train goes on the rails."),
    "наедине": ("alone", "Мы остались наедине.", "We stayed alone."),
    "бюллетень": ("bulletin", "Прочитай бюллетень.", "Read the bulletin."),
    "пчела": ("bee", "Пчела на цветке.", "The bee is on the flower."),
    "сталь": ("steel", "Это сталь.", "This is steel."),
    "отвлекать": ("to distract", "Не отвлекай меня.", "Don't distract me."),
    "лошадиный": ("horse", "Это лошадиный хвост.", "This is a horse tail."),
    "раздумье": ("reflection", "Он сидел в раздумье.", "He sat in reflection."),
    "оптический": ("optical", "Это оптический обман.", "This is an optical illusion."),
    "указатель": ("sign", "Где указатель?", "Where is the sign?"),
    "гид": ("guide", "Гид ждёт нас.", "The guide is waiting for us."),
    "вырастать": ("to grow", "Он начал вырастать.", "He began to grow."),
    "неудобно": ("uncomfortable", "Мне неудобно.", "I feel uncomfortable."),
    "упорный": ("persistent", "Он очень упорный.", "He is very persistent."),
    "ускорение": ("acceleration", "Это ускорение.", "This is acceleration."),
    "побочный": ("side", "Это побочный эффект.", "This is a side effect."),
    "тотальный": ("total", "Это тотальный контроль.", "This is total control."),
    "классик": ("classic", "Он русский классик.", "He is a Russian classic."),
    "иль": ("or", "Иль ты, иль я.", "You or I."),
    "оглядеться": ("to look around", "Оглядись вокруг.", "Look around."),
    "хлопоты": ("fuss", "Сколько хлопот!", "So much fuss!"),
    "дополнить": ("to supplement", "Дополни список.", "Supplement the list."),
    "летопись": ("chronicle", "Это старая летопись.", "This is an old chronicle."),
    "помещаться": ("to fit", "Это помещается здесь.", "It fits here."),
    "червь": ("worm", "Вот червь.", "Here is a worm."),
    "возложить": ("to lay", "Возложи надежду на него.", "Lay hope on him."),
    "обидный": ("offensive", "Это обидные слова.", "These are offensive words."),
    "диктатура": ("dictatorship", "Это диктатура.", "This is a dictatorship."),
    "самец": ("male", "Это самец.", "This is a male."),
    "поликлиника": ("clinic", "Я иду в поликлинику.", "I am going to the clinic."),
    "негодяй": ("scoundrel", "Он негодяй.", "He is a scoundrel."),
    "оный": ("that", "В оный день.", "On that day."),
    "валить": ("to fell", "Валить дерево трудно.", "It is hard to fell a tree."),
    "указываться": ("to be indicated", "Адрес указывался там.", "The address was indicated there."),
    "собачка": ("little dog", "Вот собачка.", "Here is the little dog."),
    "налогообложение": ("taxation", "Налогообложение высокое.", "Taxation is high."),
    "отличить": ("to distinguish", "Я не могу отличить их.", "I cannot distinguish them."),
    "шикарный": ("luxurious", "Какой шикарный дом!", "What a luxurious house!"),
    "мрачно": ("gloomy", "Здесь мрачно.", "It is gloomy here."),
    "адресовать": ("to address", "Адресуй письмо ей.", "Address the letter to her."),
    "императорский": ("imperial", "Это императорский дворец.", "This is an imperial palace."),
    "фасад": ("facade", "Смотри на фасад.", "Look at the facade."),
    "счёт": ("bill", "Принеси счёт.", "Bring the bill."),
    "кайф": ("high", "Это кайф.", "This is a high."),
    "барышня": ("young lady", "Барышня ждёт.", "The young lady is waiting."),
    "завоевание": ("conquest", "Это было завоевание.", "This was a conquest."),
    "гадость": ("filth", "Какая гадость!", "What filth!"),
    "убедительно": ("convincingly", "Он говорит убедительно.", "He speaks convincingly."),
    "наплевать": ("to not care", "Мне наплевать.", "I do not care."),
    "закупка": ("purchase", "Закупка завтра.", "The purchase is tomorrow."),
    "буржуазия": ("bourgeoisie", "Это буржуазия.", "This is the bourgeoisie."),
    "лад": ("harmony", "Они в ладу.", "They are in harmony."),
    "жрать": ("to devour", "Он начал жрать.", "He began to devour."),
    "шрифт": ("font", "Смени шрифт.", "Change the font."),
    "контейнер": ("container", "Где контейнер?", "Where is the container?"),
    "отход": ("departure", "Отход поезда в пять.", "The train's departure is at five."),
    "оскорбить": ("to insult", "Не оскорби его.", "Don't insult him."),
    "шинель": ("overcoat", "Он надел шинель.", "He put on the overcoat."),
    "палач": ("executioner", "Палач здесь.", "The executioner is here."),
    "позабыть": ("to forget", "Я могу позабыть это.", "I can forget this."),
    "алкогольный": ("alcoholic", "Это алкогольный напиток.", "This is an alcoholic drink."),
    "качественно": ("properly", "Сделай это качественно.", "Do this properly."),
    "предчувствие": ("premonition", "У меня плохое предчувствие.", "I have a bad premonition."),
    "расширяться": ("to expand", "Город расширяется.", "The city is expanding."),
    "наставник": ("mentor", "Он мой наставник.", "He is my mentor."),
    "догонять": ("to catch up", "Я догоняю его.", "I am catching up with him."),
    "злиться": ("to get angry", "Не надо злиться.", "Don't get angry."),
    "сытый": ("full", "Я сытый.", "I am full."),
    "подвижный": ("mobile", "Мальчик очень подвижный.", "The boy is very mobile."),
    "разбиться": ("to shatter", "Чашка разбилась.", "The cup shattered."),
    "отреагировать": ("to react", "Она быстро отреагировала.", "She reacted quickly."),
    "пионер": ("pioneer", "Он был пионером.", "He was a pioneer."),
    "сторож": ("watchman", "Сторож спит.", "The watchman is sleeping."),
    "вестник": ("messenger", "Он вестник войны.", "He is a messenger of war."),
    "восхождение": ("ascent", "Восхождение было трудным.", "The ascent was hard."),
    "некто": ("someone", "Некто пришёл.", "Someone came."),
    "санкция": ("sanction", "Это санкция.", "This is a sanction."),
    "прочитывать": ("to read", "Я прочитываю письмо.", "I read the letter."),
    "праздновать": ("to celebrate", "Мы празднуем сегодня.", "We celebrate today."),
    "разложить": ("to lay out", "Разложи книги.", "Lay out the books."),
    "спастись": ("to escape", "Нам удалось спастись.", "We managed to escape."),
    "бутерброд": ("sandwich", "Хочу бутерброд.", "I want a sandwich."),
    "сборка": ("assembly", "Сборка готова.", "The assembly is ready."),
    "испуг": ("fright", "Это был испуг.", "That was a fright."),
    "соблазн": ("temptation", "Это соблазн.", "This is a temptation."),
    "джип": ("jeep", "Где джип?", "Where is the jeep?"),
    "питерский": ("Petersburg", "Это питерский друг.", "This is a Petersburg friend."),
    "слияние": ("merger", "Это слияние.", "This is a merger."),
    "значок": ("badge", "Где мой значок?", "Where is my badge?"),
    "ласкать": ("to caress", "Она ласкает кота.", "She is caressing the cat."),
    "уставать": ("to get tired", "Я быстро устаю.", "I get tired quickly."),
    "похвала": ("praise", "Мне нужна похвала.", "I need praise."),
    "арсенал": ("arsenal", "Это наш арсенал.", "This is our arsenal."),
    "ускорить": ("to speed up", "Ускорь шаг.", "Speed up your step."),
    "особняк": ("mansion", "Это особняк.", "This is a mansion."),
    "пожить": ("to stay", "Я хочу пожить здесь.", "I want to stay here."),
    "просидеть": ("to sit", "Он может просидеть час.", "He can sit for an hour."),
}

print(
    rewrite_chunk(
        Path("russian_english/_chunks/deck_15260210_04.csv"),
        FIXES,
    )
)

FUNCTION_EN = {
    "a", "an", "the", "is", "be", "i", "you", "he", "she", "it", "we", "they",
    "my", "and", "or", "in", "on", "at", "to", "of", "for", "with", "from",
    "not", "his", "him", "her", "their", "them", "our", "us", "me", "am",
    "are", "was", "were", "been", "being", "this", "that", "these", "those",
    "as", "by", "into", "about", "than", "then", "so", "if", "but", "its",
    "your", "do", "does", "did", "will", "would", "can", "could", "may",
    "there", "here", "has", "had", "have", "don't", "dont", "let's", "lets",
    "all", "off", "done", "myself", "yourself", "himself", "herself",
    "itself", "ourselves", "themselves", "one's", "ones", "it's", "s",
    "down", "up", "out", "what", "where", "when", "who", "why", "how",
    "very", "too", "now", "yes", "no", "some", "any", "more", "most",
    "these",
}

FUNCTION_RU = {
    "и", "а", "или", "не", "ни", "но", "да", "же", "ли", "бы", "то", "это",
    "этот", "эта", "эти", "этой", "этом", "эту", "этих", "этим", "этими",
    "этого", "этому", "я", "ты", "он", "она", "оно", "мы", "вы", "они",
    "мой", "моя", "мое", "мои", "его", "ее", "их", "ему", "ей", "им",
    "меня", "мне", "тебя", "тебе", "нас", "нам", "вас", "вам", "себя",
    "себе", "свой", "своя", "свое", "свои", "свою", "своей", "своего",
    "в", "во", "на", "с", "со", "к", "ко", "у", "о", "об", "от", "до",
    "из", "за", "по", "под", "над", "при", "для", "без", "между", "через",
    "был", "была", "было", "были", "будет", "будут", "буду", "есть", "быть",
    "уже", "еще", "также", "тоже", "только", "вот", "ведь", "ну", "все",
    "как", "что", "чтобы", "когда", "если", "где", "чем", "кто", "тут",
    "там", "здесь", "давай", "нем", "нём", "ней", "них", "ним", "какая", "какой",
    "нее", "неё", "ею",
}

allow_en = {
    line.strip().lower()
    for line in (REPO / "russian_english/_vocab/allow_en_15260210.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_ru = {
    line.strip().replace("ё", "е").lower()
    for line in (REPO / "russian_english/_vocab/allow_ru_15260210.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_en |= FUNCTION_EN
allow_ru |= FUNCTION_RU

IRREGULAR_EN = {
    "came": "come", "gave": "give", "gives": "give", "took": "take", "went": "go",
    "got": "get", "saw": "see", "was": "be", "were": "be", "been": "be",
    "had": "have", "did": "do", "said": "say", "made": "make", "left": "leave",
    "felt": "feel", "began": "begin", "became": "become", "fell": "fall",
    "laid": "lay", "sat": "sit", "forgot": "forget", "slept": "sleep",
    "spoke": "speak", "speaks": "speak", "goes": "go", "going": "go",
    "waiting": "wait", "sleeping": "sleep", "expanding": "expand",
    "devouring": "devour", "catching": "catch", "celebrating": "celebrate",
    "caressing": "caress", "shattered": "shatter", "reacted": "react",
    "indicated": "indicate", "managed": "manage", "stayed": "stay",
    "answered": "answer",
}

IRREGULAR_RU = {
    "идет": "идти", "иду": "идти", "идем": "идти", "идём": "идти",
    "шел": "идти", "шёл": "идти", "шла": "идти", "шли": "идти",
    "нужна": "нужный", "нужен": "нужный", "нужно": "нужный",
    "вижу": "видеть", "видишь": "видеть", "видит": "видеть",
    "дай": "дать", "дайте": "дать",
    "едем": "ехать", "едет": "ехать",
    "слышу": "слышать", "слышит": "слышать",
    "сказал": "сказать", "сказала": "сказать",
    "смотри": "смотреть", "смотрел": "смотреть",
    "работает": "работать",
    "начал": "начать", "начала": "начать",
    "сделали": "сделать", "сделал": "сделать", "сделай": "сделать",
    "люблю": "любить",
    "может": "мочь", "могу": "мочь", "можем": "мочь",
    "изучаю": "изучать",
    "качает": "качать",
    "остались": "остаться",
    "прочитай": "прочитать",
    "вырастают": "вырастать",
    "сидел": "сидеть",
    "ждет": "ждать", "ждёт": "ждать",
    "дополни": "дополнить",
    "помещается": "помещаться",
    "возложили": "возложить",
    "валят": "валить",
    "указывался": "указываться",
    "адресуй": "адресовать",
    "принеси": "принести",
    "говорит": "говорить",
    "жрет": "жрать", "жрёт": "жрать",
    "смени": "сменить",
    "оскорби": "оскорбить",
    "надел": "надеть",
    "позабыл": "позабыть",
    "расширяется": "расширяться",
    "догоняю": "догонять",
    "злись": "злиться",
    "разбилась": "разбиться",
    "отреагировала": "отреагировать",
    "спит": "спать",
    "пришел": "прийти", "пришёл": "прийти",
    "прочитываю": "прочитывать",
    "празднуем": "праздновать",
    "разложи": "разложить",
    "удалось": "удаться",
    "хочу": "хотеть",
    "ласкает": "ласкать",
    "устаю": "уставать",
    "ускорь": "ускорить",
    "просидел": "просидеть",
    "оглядись": "оглядеться",
    "отвлекай": "отвлекать",
    "ответил": "ответить",
    "высокое": "высокий",
    "обидные": "обидный",
    "готова": "готовый",
}

RU_ENDINGS = (
    "ами", "ями", "ого", "его", "ому", "ему", "ыми", "ими", "ой", "ей", "ом",
    "ем", "ах", "ях", "ам", "ям", "ов", "ев", "ую", "юю", "ая", "яя", "ое",
    "ее", "ые", "ие", "ый", "ий", "а", "я", "у", "ю", "е", "и", "ы", "о", "ь",
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
        if any(a.startswith(stem) or stem.startswith(a) for a in allow_ru if len(a) >= 4 and len(stem) >= 4):
            return True
    return False


def _tokens(text: str) -> list[str]:
    return re.findall(r"[A-Za-zА-Яа-яЁё'-]+", text)


dest = REPO / "russian_english/_chunks/fixed/deck_15260210_04.csv"
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
