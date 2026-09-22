import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from brainscape import answer_lemma_from_card, cards_from_path, lemma_from_card
from brainscape.cards import card_write_payload
from russian_english._chunk_io import rewrite_chunk

print(
    rewrite_chunk(
        Path("russian_english/_chunks/deck_15260217_04.csv"),
        {
            "охарактеризовать": ("characterize, describe", "Охарактеризуй это.", "Characterize this."),
            "фургон": ("van, wagon", "Вот фургон.", "Here is the van."),
            "возобновить": ("resume, renew", "Возобнови работу.", "Resume the work."),
            "воспроизвести": ("reproduce, playback", "Воспроизведи звук.", "Reproduce the sound."),
            "небывалый": ("unprecedented, unparalleled", "Небывалый холод.", "Unprecedented cold."),
            "помахать": ("to wave, to flutter", "Надо помахать.", "I need to wave."),
            "шнур": ("cord, lace", "Где шнур?", "Where is the cord?"),
            "поднести": ("bring, present", "Поднеси книгу.", "Bring the book."),
            "объединяться": ("to unite, to join", "Надо объединяться.", "We need to unite."),
            "караван": ("caravan, convoy", "Вот караван.", "Here is the caravan."),
            "грызть": ("to gnaw, to nibble", "Не грызи кость.", "Don't gnaw the bone."),
            "глотка": ("throat, gulp", "Боль в глотке.", "Pain in the throat."),
            "крыться": ("to hide, to lie", "Ему негде крыться.", "He has nowhere to hide."),
            "принудить": ("coerce, force", "Надо принудить его.", "We need to coerce him."),
            "комсомол": ("Komsomol", "Он в комсомоле.", "He is in the Komsomol."),
            "гороскоп": ("horoscope", "Читай гороскоп.", "Read the horoscope."),
            "удочка": ("fishing rod, rod", "Где удочка?", "Where is the fishing rod?"),
            "нестандартный": ("non-standard, unconventional", "Нестандартный подход.", "A non-standard approach."),
            "незачем": ("no need, no reason", "Незачем ждать.", "No need to wait."),
            "подружиться": ("to make friends, to befriend", "Надо подружиться.", "We need to make friends."),
            "новгородский": ("Novgorodian, of Novgorod", "Новгородский дом.", "A Novgorodian house."),
            "оккупация": ("occupation, annexation", "После оккупации.", "After the occupation."),
            "транспортировка": ("transportation", "Транспортировка товара.", "Transportation of goods."),
            "единомышленник": ("like-minded person, fellow thinker", "Он мой единомышленник.", "He is my like-minded person."),
            "шумно": ("noisily, loudly", "Он шумно спит.", "He sleeps noisily."),
            "послушно": ("obediently, dutifully", "Он послушно ждёт.", "He obediently waits."),
            "неуверенность": ("uncertainty, insecurity", "Это неуверенность.", "This is uncertainty."),
            "национал": ("nationalist", "Он национал.", "He is a nationalist."),
            "садовый": ("garden", "Садовый стол.", "A garden table."),
            "умелый": ("skilled, skillful", "Он умелый мастер.", "He is a skilled master."),
            "имущественный": ("property, proprietary", "Имущественный вопрос.", "A property question."),
            "запечатлеть": ("capture, immortalize", "Запечатлей это.", "Capture this."),
            "библиотечный": ("library", "Библиотечный зал.", "A library hall."),
            "заразить": ("infect, contaminate", "Не зарази меня.", "Don't infect me."),
            "пренебрегать": ("neglect, disregard", "Не пренебрегай мной.", "Don't neglect me."),
            "сулить": ("promise, hold out", "Это сулит беду.", "This promises trouble."),
            "распахнуться": ("to swing open, to fling open", "Дверь распахнётся.", "The door will swing open."),
            "сыщик": ("detective, investigator", "Сыщик здесь.", "The detective is here."),
            "вскакивать": ("to jump up, to leap up", "Он вскакивает.", "He jumps up."),
            "вывоз": ("export, removal", "Вывоз товара.", "The export of goods."),
            "откинуть": ("throw back, recline", "Откинь голову.", "Throw back your head."),
            "внушение": ("suggestion", "Это внушение.", "This is a suggestion."),
            "интеллектуал": ("intellectual", "Он интеллектуал.", "He is an intellectual."),
            "подтолкнуть": ("push, nudge", "Подтолкни дверь.", "Push the door."),
            "присвоение": ("appropriation, assignment", "Это присвоение.", "This is an appropriation."),
            "кончина": ("demise, death", "После кончины.", "After the demise."),
            "рапорт": ("report", "Вот рапорт.", "Here is the report."),
            "красоваться": ("show off, flaunt", "Не надо красоваться.", "No need to show off."),
            "непостижимый": ("incomprehensible, unfathomable", "Непостижимый мир.", "An incomprehensible world."),
            "половинка": ("half", "Вот половинка.", "Here is a half."),
            "береговой": ("coastal", "Береговой ветер.", "A coastal wind."),
            "срезать": ("cut off, slice", "Надо срезать край.", "Cut off the edge."),
            "чуткий": ("sensitive, perceptive", "Он чуткий.", "He is sensitive."),
            "насчёт": ("about, regarding", "Что насчёт ужина?", "What about dinner?"),
            "полушарие": ("hemisphere", "Это полушарие.", "This is a hemisphere."),
            "эмоционально": ("emotionally", "Он эмоционально слабый.", "He is emotionally weak."),
            "бодро": ("briskly, cheerfully", "Иди бодро.", "Go briskly."),
            "раскрытый": ("opened, disclosed", "Раскрытая книга.", "An opened book."),
            "задрать": ("lift up, pull up", "Надо задрать голову.", "Lift up your head."),
            "романтика": ("romance, romanticism", "Где романтика?", "Where is the romance?"),
            "берлинский": ("Berlin, Berliner", "Берлинский поезд.", "The Berlin train."),
            "пугаться": ("to be scared, to be frightened", "Не пугайся.", "Don't be scared."),
            "стареть": ("to age, to grow old", "Все будут стареть.", "All will age."),
            "лексика": ("vocabulary, lexicon", "Сложная лексика.", "Hard vocabulary."),
            "прототип": ("prototype, model", "Вот прототип.", "Here is the prototype."),
            "побудить": ("encourage, prompt", "Надо побудить его.", "Encourage him."),
            "итоговый": ("final, summary", "Итоговый день.", "The final day."),
            "отбрасывать": ("to throw back, to cast off", "Не отбрасывай свет.", "Don't throw back the light."),
            "всплыть": ("surface, emerge", "Правда всплыла.", "The truth did surface."),
            "брести": ("trudge, plod", "Надо брести домой.", "We need to trudge home."),
            "компактный": ("compact", "Компактный дом.", "A compact house."),
            "тосковать": ("to miss, to yearn", "Не тоскуй по мне.", "Don't miss me."),
            "пронизывать": ("pierce, permeate", "Холод будет пронизывать.", "The cold will pierce."),
            "вибрация": ("vibration", "Это вибрация.", "This is a vibration."),
            "сигара": ("cigar", "Вот сигара.", "Here is a cigar."),
            "влететь": ("to fly into, to crash into", "Птица влетела в дом.", "The bird did fly into the house."),
            "подействовать": ("to affect, to influence", "Это должно подействовать.", "This must affect him."),
            "недовольно": ("discontentedly", "Он недовольно ждёт.", "He waits discontentedly."),
            "венок": ("wreath, garland", "Вот венок.", "Here is a wreath."),
            "дружественный": ("friendly, amicable", "Дружественный тон.", "A friendly tone."),
            "своевременный": ("timely, prompt", "Своевременный ответ.", "A timely answer."),
            "покорно": ("humbly, submissively", "Я покорно жду.", "I humbly wait."),
            "двенадцатый": ("twelfth", "Двенадцатый день.", "The twelfth day."),
            "психологически": ("psychologically", "Он психологически слабый.", "He is psychologically weak."),
            "мило": ("cute, nice", "Это мило.", "This is cute."),
            "гимнастика": ("gymnastics", "Это гимнастика.", "This is gymnastics."),
            "миллиметр": ("millimeter", "Один миллиметр.", "One millimeter."),
            "подаваться": ("to be served, to apply", "Ужин будет подаваться.", "Dinner will be served."),
            "спровоцировать": ("provoke, instigate", "Его легко спровоцировать.", "It is easy to provoke him."),
            "драгоценность": ("jewel, treasure", "Это драгоценность.", "This is a jewel."),
            "пиратский": ("pirate", "Пиратский корабль.", "A pirate ship."),
            "пролетарский": ("proletarian", "Пролетарский район.", "A proletarian district."),
            "резиденция": ("residence", "Его резиденция далеко.", "His residence is far."),
            "почтение": ("respect, reverence", "С почтением.", "With respect."),
            "языческий": ("pagan, heathen", "Языческий храм.", "A pagan temple."),
            "сосновый": ("pine", "Сосновый лес.", "A pine forest."),
            "напрячься": ("to strain, to tense up", "Надо напрячься.", "I need to strain."),
            "швед": ("Swede, Swedish", "Он швед.", "He is a Swede."),
            "пучок": ("bundle, bunch", "Пучок волос.", "A bundle of hair."),
            "аллергия": ("allergy", "У меня аллергия.", "I have an allergy."),
        },
    )
)

FUNCTION_EN = {
    "a", "an", "the", "to", "of", "in", "on", "at", "for", "from", "with", "by",
    "and", "or", "but", "not", "no", "yes", "is", "are", "was", "were", "be",
    "am", "been", "being", "do", "does", "did", "will", "would", "can", "could",
    "has", "have", "had", "i", "you", "he", "she", "it", "we", "they", "me",
    "him", "her", "us", "them", "my", "your", "his", "its", "our", "their",
    "this", "that", "these", "those", "there", "here", "what", "where", "when",
    "how", "who", "why", "don't", "doesn't", "isn't", "aren't", "wasn't",
    "weren't", "won't", "can't", "i'm", "he's", "she's", "it's", "we're",
    "they're", "that's", "there's", "where's", "out", "up", "down", "off",
    "into", "about", "after", "before", "again", "already", "also", "just",
    "only", "very", "so", "too", "then", "than", "as", "if", "because",
}
FUNCTION_RU = {
    "я", "ты", "он", "она", "оно", "мы", "вы", "они", "меня", "тебя", "его",
    "её", "ее", "нас", "вас", "их", "мне", "тебе", "ему", "ей", "нам", "вам",
    "им", "мной", "тобой", "им", "ею", "нами", "вами", "ими", "мой", "моя",
    "мое", "моё", "мои", "твой", "твоя", "твое", "твоё", "твои", "наш", "наш",
    "это", "этот", "эта", "эти", "тот", "та", "те", "не", "ни", "да", "нет",
    "и", "а", "но", "или", "ли", "же", "бы", "б", "уж", "ка", "то", "себе",
    "свой", "своя", "свое", "своё", "свои", "свою", "своей", "своего",
    "в", "во", "на", "с", "со", "к", "ко", "у", "о", "об", "от", "до",
    "из", "за", "по", "под", "над", "при", "для", "без", "между", "через",
    "был", "была", "было", "были", "будет", "будут", "буду", "есть", "быть",
    "уже", "еще", "ещё", "также", "тоже", "только", "вот", "ведь", "ну", "все",
    "как", "что", "чтобы", "когда", "если", "где", "чем", "кто", "тут",
    "там", "здесь", "давай", "нем", "нём", "ней", "них", "нее", "неё",
}

allow_en = {
    line.strip().lower()
    for line in (REPO / "russian_english/_vocab/allow_en_15260217.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_ru = {
    line.strip().replace("ё", "е").lower()
    for line in (REPO / "russian_english/_vocab/allow_ru_15260217.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_en |= FUNCTION_EN
allow_ru |= FUNCTION_RU

IRREGULAR_EN = {
    "came": "come", "gave": "give", "took": "take", "went": "go", "got": "get",
    "saw": "see", "was": "be", "were": "be", "been": "be", "had": "have",
    "did": "do", "said": "say", "made": "make", "left": "leave", "felt": "feel",
    "began": "begin", "became": "become", "bought": "buy", "caught": "catch",
    "kept": "keep", "lost": "lose", "fell": "fall", "grew": "grow", "held": "hold",
    "knew": "know", "ran": "run", "sat": "sit", "stood": "stand", "told": "tell",
    "thought": "think", "wrote": "write", "spoke": "speak", "broke": "break",
    "chose": "choose", "drove": "drive", "ate": "eat", "flew": "fly",
    "sleeps": "sleep", "waits": "wait", "jumps": "jump", "promises": "promise",
}
IRREGULAR_RU = {
    "идет": "идти", "иду": "идти", "шел": "идти", "шла": "идти", "шли": "идти",
    "иди": "идти", "читай": "читать", "спит": "спать",
    "ждет": "ждать", "ждёт": "ждать", "жду": "ждать",
    "охарактеризуй": "охарактеризовать",
    "возобнови": "возобновить",
    "воспроизведи": "воспроизвести",
    "поднеси": "поднести",
    "грызи": "грызть",
    "запечатлей": "запечатлеть",
    "зарази": "заразить",
    "пренебрегай": "пренебрегать",
    "сулит": "сулить",
    "распахнется": "распахнуться",
    "распахнётся": "распахнуться",
    "вскакивает": "вскакивать",
    "откинь": "откинуть",
    "подтолкни": "подтолкнуть",
    "отбрасывай": "отбрасывать",
    "всплыла": "всплыть",
    "тоскуй": "тосковать",
    "влетела": "влететь",
    "пугайся": "пугаться",
    "беду": "беда",
    "голову": "голова",
    "должно": "должен",
    "негде": "негде",
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
    if IRREGULAR_RU.get(word) in allow_ru:
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


dest = REPO / "russian_english/_chunks/fixed/deck_15260217_04.csv"
cards = cards_from_path(dest)
leftover = []
for i, card in enumerate(cards, 1):
    lemma = lemma_from_card(card)
    gloss = answer_lemma_from_card(card)
    payload = card_write_payload(card)
    ru = payload["question"].split("## Footnote")[-1].strip()
    en = payload["answer"].split("## Footnote")[-1].strip()
    ru_l = ru.replace("ё", "е").lower()
    if lemma.replace("ё", "е").lower() not in ru_l and lemma.replace("ё", "е").lower()[:4] not in ru_l:
        leftover.append(f"{i} LEMMA {lemma} :: {ru}")
    gloss_l = re.sub(r"^(to |the |a |an )", "", gloss.split(",")[0].strip().lower())
    if gloss_l and gloss_l.split()[0] not in en.lower() and not any(g in en.lower() for g in gloss_l.split()):
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
