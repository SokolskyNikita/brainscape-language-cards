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
        Path("russian_english/_chunks/deck_15260207_03.csv"),
        {
            "вылезать": (
                "to climb out, to emerge",
                "Надо вылезать.",
                "I need to climb out.",
            ),
            "завтрашний": (
                "tomorrow's, next day's",
                "Завтрашний план.",
                "Tomorrow's plan.",
            ),
            "джентльмен": (
                "gentleman, gent",
                "Он джентльмен.",
                "He is a gentleman.",
            ),
            "скачать": (
                "to download",
                "Надо скачать файл.",
                "I need to download the file.",
            ),
            "влечь": (
                "to entail, to attract",
                "Это может влечь за собой риск.",
                "This may entail a risk.",
            ),
            "влево": (
                "to the left, left",
                "Смотри влево.",
                "Look to the left.",
            ),
            "ассортимент": (
                "assortment, range",
                "Большой ассортимент.",
                "A large assortment.",
            ),
            "повар": (
                "cook, chef",
                "Он повар.",
                "He is a cook.",
            ),
            "устный": (
                "oral, verbal",
                "Устный ответ.",
                "An oral answer.",
            ),
            "мусульманский": (
                "Muslim, Islamic",
                "Мусульманский праздник.",
                "A Muslim holiday.",
            ),
            "бегство": (
                "escape, flight",
                "Его бегство.",
                "His escape.",
            ),
            "опросить": (
                "to survey, to interrogate",
                "Надо опросить народ.",
                "We need to survey the people.",
            ),
            "огурец": (
                "cucumber, gherkin",
                "Свежий огурец.",
                "A fresh cucumber.",
            ),
            "доводить": (
                "to bring to, to drive to",
                "Не доводи меня.",
                "Do not drive me to it.",
            ),
            "пена": (
                "foam, lather",
                "Пена в ванне.",
                "Foam in the bath.",
            ),
            "ребро": (
                "rib, edge",
                "Болит ребро.",
                "The rib hurts.",
            ),
            "выстрелить": (
                "to shoot, to fire",
                "Он хочет выстрелить.",
                "He wants to shoot.",
            ),
            "рецензия": (
                "review, critique",
                "Плохая рецензия.",
                "A bad review.",
            ),
            "известность": (
                "fame, renown",
                "Его известность.",
                "His fame.",
            ),
            "прах": (
                "ash, dust",
                "Его прах.",
                "His ash.",
            ),
            "подоконник": (
                "windowsill",
                "Кот на подоконнике.",
                "The cat is on the windowsill.",
            ),
            "пробежать": (
                "to run through, to run past",
                "Надо пробежать двор.",
                "I need to run through the yard.",
            ),
            "излагать": (
                "to state, to set out",
                "Надо излагать план.",
                "I need to state the plan.",
            ),
            "толкование": (
                "interpretation, explanation",
                "Странное толкование.",
                "A strange interpretation.",
            ),
            "прикрытие": (
                "cover, covering",
                "Нужно прикрытие.",
                "We need cover.",
            ),
            "ежели": (
                "if",
                "Ежели так, хорошо.",
                "If so, good.",
            ),
            "телеканал": (
                "TV channel",
                "Новый телеканал.",
                "A new TV channel.",
            ),
            "участь": (
                "fate, lot",
                "Его участь.",
                "His fate.",
            ),
            "интервал": (
                "interval, gap",
                "Короткий интервал.",
                "A short interval.",
            ),
            "былой": (
                "former, bygone",
                "Былой успех.",
                "Former success.",
            ),
            "тщательный": (
                "thorough, meticulous",
                "Тщательный выбор.",
                "A thorough choice.",
            ),
            "логичный": (
                "logical, rational",
                "Логичный ответ.",
                "A logical answer.",
            ),
            "братец": (
                "little brother, bro",
                "Где братец?",
                "Where is my little brother?",
            ),
            "дополнительно": (
                "additionally, extra",
                "Нужно это дополнительно.",
                "We need this additionally.",
            ),
            "губерния": (
                "province, governorate",
                "Большая губерния.",
                "A large province.",
            ),
            "постучать": (
                "to knock, to tap",
                "Надо постучать в дверь.",
                "I need to knock on the door.",
            ),
            "торопливо": (
                "hurriedly, hastily",
                "Он торопливо ест.",
                "He eats hurriedly.",
            ),
            "винт": (
                "screw, propeller",
                "Где винт?",
                "Where is the screw?",
            ),
            "деяние": (
                "deed, action",
                "Доброе деяние.",
                "A good deed.",
            ),
            "фига": (
                "fig, nothing",
                "Сладкая фига.",
                "A sweet fig.",
            ),
            "вика": (
                "Vika",
                "Вика дома.",
                "Vika is home.",
            ),
            "православие": (
                "Orthodoxy",
                "Русское православие.",
                "Russian Orthodoxy.",
            ),
            "затруднение": (
                "difficulty, embarrassment",
                "Есть затруднение.",
                "There is a difficulty.",
            ),
            "брачный": (
                "marital, matrimonial",
                "Брачный договор.",
                "A marital contract.",
            ),
            "порвать": (
                "to tear, to rip",
                "Надо порвать письмо.",
                "I need to tear the letter.",
            ),
            "допускаться": (
                "to be allowed, to be admitted",
                "Это не допускается.",
                "This is not allowed.",
            ),
            "багаж": (
                "luggage, baggage",
                "Где багаж?",
                "Where is the luggage?",
            ),
            "толщина": (
                "thickness, gauge",
                "Какая толщина?",
                "What thickness?",
            ),
            "трижды": (
                "three times",
                "Трижды в день.",
                "Three times a day.",
            ),
            "нехватка": (
                "shortage, deficiency",
                "Есть нехватка.",
                "There is a shortage.",
            ),
            "устойчивость": (
                "stability, resilience",
                "Нужна устойчивость.",
                "We need stability.",
            ),
            "зажать": (
                "to clamp, to pinch",
                "Надо зажать это.",
                "I need to clamp this.",
            ),
            "мистический": (
                "mystical, mystic",
                "Мистический свет.",
                "A mystical light.",
            ),
            "чушь": (
                "nonsense, rubbish",
                "Это чушь.",
                "That is nonsense.",
            ),
            "возиться": (
                "to fiddle, to tinker",
                "Не надо возиться.",
                "Do not fiddle.",
            ),
            "синдром": (
                "syndrome",
                "Странный синдром.",
                "A strange syndrome.",
            ),
            "сияние": (
                "radiance, glow",
                "Яркое сияние.",
                "A bright radiance.",
            ),
            "доктрина": (
                "doctrine, dogma",
                "Его доктрина.",
                "His doctrine.",
            ),
            "трястись": (
                "to shake, to tremble",
                "Я начал трястись от страха.",
                "I began to shake from fear.",
            ),
            "истерика": (
                "tantrum, hysteria",
                "Страшная истерика.",
                "A terrible tantrum.",
            ),
            "штурман": (
                "navigator, pilot",
                "Он штурман.",
                "He is a navigator.",
            ),
            "утрата": (
                "loss, deprivation",
                "Большая утрата.",
                "A great loss.",
            ),
            "уцелеть": (
                "to survive",
                "Он хочет уцелеть.",
                "He wants to survive.",
            ),
            "фланг": (
                "flank, wing",
                "Левый фланг.",
                "The left flank.",
            ),
            "жевать": (
                "to chew",
                "Надо жевать медленно.",
                "I need to chew slowly.",
            ),
            "такт": (
                "tact, beat",
                "Чувство такта.",
                "A sense of tact.",
            ),
            "донести": (
                "to convey, to report",
                "Я хочу донести правду.",
                "I want to convey the truth.",
            ),
            "справедливо": (
                "fairly, justly",
                "Говори справедливо.",
                "Speak fairly.",
            ),
            "носиться": (
                "to rush, to zoom",
                "Он любит носиться.",
                "He loves to rush.",
            ),
            "глагол": (
                "verb",
                "Это глагол.",
                "This is a verb.",
            ),
            "одеться": (
                "to get dressed, to dress",
                "Надо одеться.",
                "I need to get dressed.",
            ),
            "обоснование": (
                "justification, foundation",
                "Нет обоснования.",
                "There is no justification.",
            ),
            "угодить": (
                "to please, to satisfy",
                "Трудно угодить.",
                "It is hard to please.",
            ),
            "горячо": (
                "hotly, warmly",
                "Он горячо спорит.",
                "He argues hotly.",
            ),
            "рекорд": (
                "record",
                "Новый рекорд.",
                "A new record.",
            ),
            "открытка": (
                "postcard, greeting card",
                "Красивая открытка.",
                "A beautiful postcard.",
            ),
            "итальянец": (
                "Italian",
                "Он итальянец.",
                "He is Italian.",
            ),
            "примета": (
                "omen, sign",
                "Плохая примета.",
                "A bad omen.",
            ),
            "электричка": (
                "electric train",
                "Где электричка?",
                "Where is the electric train?",
            ),
            "хм": (
                "hmm, uh",
                "Хм, это странно.",
                "Hmm, that is strange.",
            ),
            "сугубо": (
                "strictly, solely",
                "Это сугубо моё.",
                "This is strictly mine.",
            ),
            "прощание": (
                "farewell, goodbye",
                "Долгое прощание.",
                "A long farewell.",
            ),
            "лысый": (
                "bald",
                "Он лысый.",
                "He is bald.",
            ),
            "кружиться": (
                "to spin, to whirl",
                "Она любит кружиться.",
                "She loves to spin.",
            ),
            "пышный": (
                "lush, fluffy",
                "Пышный сад.",
                "A lush garden.",
            ),
            "предвыборный": (
                "pre-election, electoral",
                "Предвыборный план.",
                "A pre-election plan.",
            ),
            "цирк": (
                "circus",
                "Я люблю цирк.",
                "I love the circus.",
            ),
            "почка": (
                "kidney, bud",
                "Болит почка.",
                "The kidney hurts.",
            ),
            "колючий": (
                "prickly, thorny",
                "Колючий куст.",
                "A prickly bush.",
            ),
            "президиум": (
                "presidium",
                "Новый президиум.",
                "The new presidium.",
            ),
            "клинический": (
                "clinical",
                "Клинический случай.",
                "A clinical case.",
            ),
            "затронуть": (
                "to touch, to affect",
                "Это должно затронуть нас.",
                "This must touch us.",
            ),
            "новинка": (
                "novelty, new product",
                "Это новинка.",
                "This is a novelty.",
            ),
            "обрушиться": (
                "to collapse, to fall down",
                "Дом скоро обрушится.",
                "The house will collapse soon.",
            ),
            "твердить": (
                "to repeat, to harp on",
                "Он твердит это.",
                "He repeats this.",
            ),
            "сбегать": (
                "to run away, to dash off",
                "Не надо сбегать.",
                "Do not run away.",
            ),
            "вознаграждение": (
                "reward",
                "Большое вознаграждение.",
                "A large reward.",
            ),
            "старина": (
                "old times, old friend",
                "В старину было тихо.",
                "In the old times it was quiet.",
            ),
            "птичий": (
                "bird, avian",
                "Птичий крик.",
                "A bird cry.",
            ),
            "орех": (
                "nut, kernel",
                "Сладкий орех.",
                "A sweet nut.",
            ),
        },
    )
)

dest = PACK / "_chunks" / "fixed" / "deck_15260207_03.csv"
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
