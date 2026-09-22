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

IRREGULAR_EN = {
    "came": "come", "gave": "give", "took": "take", "went": "go", "got": "get",
    "saw": "see", "was": "be", "were": "be", "been": "be", "had": "have",
    "did": "do", "said": "say", "made": "make", "left": "leave", "felt": "feel",
    "began": "begin", "became": "become", "bought": "buy", "caught": "catch",
    "kept": "keep", "lost": "lose", "fell": "fall", "grew": "grow", "held": "hold",
    "knew": "know", "ran": "run", "sat": "sit", "stood": "stand", "told": "tell",
    "thought": "think", "wrote": "write", "spoke": "speak", "broke": "break",
    "chose": "choose", "drove": "drive", "ate": "eat", "flew": "fly",
    "hurts": "hurt", "argues": "argue", "eats": "eat", "repeats": "repeat",
    "climbing": "climb", "stating": "state",
}

IRREGULAR_RU = {
    "идет": "идти", "иду": "идти", "шел": "идти", "шла": "идти", "шли": "идти",
    "нужна": "нужный", "нужен": "нужный", "нужно": "нужный",
    "болит": "болеть", "смотрит": "смотреть", "смотри": "смотреть",
    "люблю": "любить", "начал": "начать", "начала": "начать",
    "ест": "есть",
    "может": "мочь", "хочет": "хотеть", "хочу": "хотеть",
    "допускается": "допускаться",
    "обрушится": "обрушиться",
}

RU_ENDINGS = (
    "ами", "ями", "ого", "его", "ому", "ему", "ыми", "ими", "ой", "ей", "ом",
    "ем", "ах", "ях", "ам", "ям", "ов", "ев", "ую", "юю", "ая", "яя", "ое",
    "ее", "ые", "ие", "ый", "ий", "а", "я", "у", "ю", "е", "и", "ы", "о", "ь",
)

allow_en = {
    line.strip().lower()
    for line in (PACK / "_vocab" / "allow_en_15260207.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_ru = {
    line.strip().replace("ё", "е").lower()
    for line in (PACK / "_vocab" / "allow_ru_15260207.txt").read_text(encoding="utf-8").splitlines()
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
        Path("russian_english/_chunks/deck_15260207_04.csv"),
        {
            "продумать": (
                "think through, plan out",
                "Надо продумать план.",
                "We need to think through the plan.",
            ),
            "презрение": (
                "contempt, disdain",
                "Его презрение.",
                "His contempt.",
            ),
            "речевой": (
                "speech, verbal",
                "Речевой сигнал.",
                "A speech signal.",
            ),
            "возбуждать": (
                "excite, arouse",
                "Это может возбуждать.",
                "This can excite.",
            ),
            "спаситель": (
                "savior, redeemer",
                "Он спаситель.",
                "He is a savior.",
            ),
            "равнина": (
                "plain",
                "Широкая равнина.",
                "A wide plain.",
            ),
            "подвергнуться": (
                "to undergo, to be subjected",
                "Надо подвергнуться этому.",
                "We need to undergo this.",
            ),
            "секта": (
                "sect, cult",
                "Странная секта.",
                "A strange sect.",
            ),
            "присвоить": (
                "assign, appropriate",
                "Надо присвоить номер.",
                "We need to assign a number.",
            ),
            "отвергать": (
                "reject, repudiate",
                "Не надо отвергать это.",
                "Do not reject this.",
            ),
            "предание": (
                "tradition, legend",
                "Старое предание.",
                "An old tradition.",
            ),
            "сбыт": (
                "sales",
                "Сбыт товара.",
                "Sales of the goods.",
            ),
            "вой": (
                "howl, wail",
                "Вой волка.",
                "The howl of a wolf.",
            ),
            "массаж": (
                "massage",
                "Нужен массаж.",
                "I need a massage.",
            ),
            "злобный": (
                "malicious, spiteful",
                "Злобный взгляд.",
                "A malicious look.",
            ),
            "горизонтальный": (
                "horizontal, level",
                "Горизонтальная линия.",
                "A horizontal line.",
            ),
            "затянуться": (
                "drag on, linger",
                "Встреча может затянуться.",
                "The meeting may drag on.",
            ),
            "обижать": (
                "to offend, to hurt",
                "Не надо обижать её.",
                "Do not offend her.",
            ),
            "целостность": (
                "integrity, wholeness",
                "Целостность дела.",
                "The integrity of the case.",
            ),
            "посылка": (
                "parcel, package",
                "Где посылка?",
                "Where is the parcel?",
            ),
            "пустынный": (
                "deserted, desolate",
                "Пустынный дом.",
                "A deserted house.",
            ),
            "балтийский": (
                "Baltic",
                "Балтийское море.",
                "The Baltic Sea.",
            ),
            "повестка": (
                "agenda, summons",
                "Его повестка.",
                "His agenda.",
            ),
            "бездна": (
                "abyss, chasm",
                "Глубокая бездна.",
                "A deep abyss.",
            ),
            "хакер": (
                "hacker",
                "Он хакер.",
                "He is a hacker.",
            ),
            "катиться": (
                "to roll",
                "Мяч может катиться.",
                "The ball may roll.",
            ),
            "дожить": (
                "live out, survive",
                "Надо дожить до весны.",
                "I need to live to spring.",
            ),
            "вообразить": (
                "imagine, envision",
                "Надо вообразить это.",
                "We need to imagine this.",
            ),
            "полярный": (
                "polar",
                "Полярный круг.",
                "A polar circle.",
            ),
            "террор": (
                "terror",
                "Это террор.",
                "This is terror.",
            ),
            "якорь": (
                "anchor",
                "Брось якорь.",
                "Drop the anchor.",
            ),
            "прочно": (
                "firmly, solidly",
                "Держи прочно.",
                "Hold firmly.",
            ),
            "вправду": (
                "really, indeed",
                "Это вправду так?",
                "Is this really so?",
            ),
            "уравнение": (
                "equation",
                "Реши уравнение.",
                "Solve the equation.",
            ),
            "бакс": (
                "buck, dollar",
                "Нужен бакс.",
                "I need a buck.",
            ),
            "разбор": (
                "analysis, disassembly",
                "Разбор дела.",
                "An analysis of the case.",
            ),
            "согласовать": (
                "coordinate, agree",
                "Надо согласовать план.",
                "We need to coordinate the plan.",
            ),
            "персона": (
                "person, individual",
                "Важная персона.",
                "An important person.",
            ),
            "горечь": (
                "bitterness, gall",
                "Его горечь.",
                "His bitterness.",
            ),
            "телесный": (
                "bodily, corporeal",
                "Телесная боль.",
                "Bodily pain.",
            ),
            "продюсер": (
                "producer",
                "Он продюсер.",
                "He is a producer.",
            ),
            "месть": (
                "revenge, vengeance",
                "Это месть.",
                "This is revenge.",
            ),
            "католический": (
                "Catholic",
                "Католическая церковь.",
                "A Catholic church.",
            ),
            "счастливо": (
                "happily",
                "Счастливо жить.",
                "To live happily.",
            ),
            "покраснеть": (
                "to blush, to turn red",
                "Она может покраснеть.",
                "She may blush.",
            ),
            "пролетариат": (
                "proletariat",
                "Весь пролетариат.",
                "The whole proletariat.",
            ),
            "география": (
                "geography",
                "Урок географии.",
                "A geography lesson.",
            ),
            "архитектурный": (
                "architectural",
                "Архитектурный стиль.",
                "An architectural style.",
            ),
            "гимназия": (
                "gymnasium, grammar school",
                "Старая гимназия.",
                "An old gymnasium.",
            ),
            "усвоить": (
                "assimilate, absorb",
                "Надо усвоить урок.",
                "We need to assimilate the lesson.",
            ),
            "алло": (
                "hello",
                "Алло, это ты?",
                "Hello, is that you?",
            ),
            "сборная": (
                "national team",
                "Наша сборная.",
                "Our national team.",
            ),
            "банда": (
                "gang, band",
                "Местная банда.",
                "A local gang.",
            ),
            "даром": (
                "free, in vain",
                "Книга даром.",
                "The book is free.",
            ),
            "демократ": (
                "democrat",
                "Он демократ.",
                "He is a democrat.",
            ),
            "помеха": (
                "interference, obstacle",
                "Это помеха.",
                "This is interference.",
            ),
            "растеряться": (
                "get confused",
                "Он может растеряться.",
                "He may get confused.",
            ),
            "крейсер": (
                "cruiser",
                "Старый крейсер.",
                "An old cruiser.",
            ),
            "египетский": (
                "Egyptian",
                "Египетский храм.",
                "An Egyptian temple.",
            ),
            "аплодисменты": (
                "applause, clapping",
                "Громкие аплодисменты.",
                "Loud applause.",
            ),
            "вероятный": (
                "probable, likely",
                "Это вероятный случай.",
                "This is a probable case.",
            ),
            "завязать": (
                "tie",
                "Надо завязать узел.",
                "We need to tie a knot.",
            ),
            "генетический": (
                "genetic",
                "Генетический код.",
                "A genetic code.",
            ),
            "сдержать": (
                "restrain, hold back",
                "Надо сдержать гнев.",
                "We need to restrain the anger.",
            ),
            "безработица": (
                "unemployment",
                "Высокая безработица.",
                "High unemployment.",
            ),
            "объективно": (
                "objectively, impartially",
                "Смотри объективно.",
                "Look objectively.",
            ),
            "вычислительный": (
                "computational",
                "Вычислительный центр.",
                "A computational center.",
            ),
            "горько": (
                "bitterly",
                "Горько плакать.",
                "To cry bitterly.",
            ),
            "мирно": (
                "peacefully, calmly",
                "Мирно жить.",
                "To live peacefully.",
            ),
            "поздравление": (
                "congratulation, greeting",
                "Моё поздравление.",
                "My congratulation.",
            ),
            "разом": (
                "at once, together",
                "Все разом.",
                "All at once.",
            ),
            "социологический": (
                "sociological",
                "Социологический взгляд.",
                "A sociological look.",
            ),
            "конструктивный": (
                "constructive",
                "Конструктивный совет.",
                "Constructive advice.",
            ),
            "митрополит": (
                "metropolitan",
                "Наш митрополит.",
                "Our metropolitan.",
            ),
            "сочинять": (
                "compose, create",
                "Надо сочинять песни.",
                "We need to compose songs.",
            ),
            "пошлина": (
                "duty, tariff",
                "Высокая пошлина.",
                "A high duty.",
            ),
            "солдатский": (
                "soldier's, military",
                "Солдатский долг.",
                "A soldier's duty.",
            ),
            "благосостояние": (
                "welfare, well-being",
                "Наше благосостояние.",
                "Our welfare.",
            ),
            "снятие": (
                "removal, withdrawal",
                "Снятие маски.",
                "Removal of the mask.",
            ),
            "кавказский": (
                "Caucasian",
                "Кавказский край.",
                "The Caucasian region.",
            ),
            "фальшивый": (
                "fake, counterfeit",
                "Фальшивая улыбка.",
                "A fake smile.",
            ),
            "снизиться": (
                "decrease",
                "Цена может снизиться.",
                "The price may decrease.",
            ),
            "подвергать": (
                "subject, expose",
                "Не надо подвергать нас риску.",
                "Do not subject us to risk.",
            ),
            "грант": (
                "grant",
                "Новый грант.",
                "A new grant.",
            ),
            "выраженный": (
                "pronounced, marked",
                "Выраженный акцент.",
                "A pronounced accent.",
            ),
            "слушаться": (
                "to obey",
                "Надо слушаться матери.",
                "You need to obey your mother.",
            ),
            "расстроить": (
                "upset, disappoint",
                "Это может расстроить.",
                "This may upset me.",
            ),
            "жюри": (
                "jury",
                "Строгое жюри.",
                "A strict jury.",
            ),
            "крем": (
                "cream",
                "Этот крем.",
                "This cream.",
            ),
            "достоверный": (
                "reliable, authentic",
                "Достоверный источник.",
                "A reliable source.",
            ),
            "обосновать": (
                "justify, substantiate",
                "Надо обосновать это.",
                "We need to justify this.",
            ),
            "свод": (
                "compilation, summary",
                "Свод законов.",
                "A compilation of laws.",
            ),
            "пассивный": (
                "passive",
                "Он пассивный.",
                "He is passive.",
            ),
            "лечиться": (
                "to be treated",
                "Надо лечиться.",
                "I need to be treated.",
            ),
            "заинтересоваться": (
                "to become interested",
                "Она может заинтересоваться.",
                "She may become interested.",
            ),
            "поклониться": (
                "bow down",
                "Надо поклониться королю.",
                "We need to bow down to the king.",
            ),
            "плюнуть": (
                "to spit",
                "Не плюнь.",
                "Do not spit.",
            ),
            "звучание": (
                "sound",
                "Странное звучание.",
                "A strange sound.",
            ),
            "теракт": (
                "terrorist act",
                "Это теракт.",
                "This is a terrorist act.",
            ),
            "древность": (
                "antiquity",
                "Это древность.",
                "This is antiquity.",
            ),
        },
    )
)

dest = PACK / "_chunks" / "fixed" / "deck_15260207_04.csv"
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
