#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PACK = ROOT / "english_russian"
sys.path.insert(0, str(ROOT))

from brainscape.cards import card_write_payload, cards_from_path, cards_match
from english_russian._chunk_io import write_csv

SRC = PACK / "_chunks" / "deck_15260268_01.csv"
OUT = PACK / "_chunks" / "fixed" / "deck_15260268_01.csv"
LOG = PACK / "_chunks" / "logs" / "deck_15260268_01.txt"

FUNCTION_EN = {
    "a", "the", "is", "be", "i", "you", "he", "she", "it", "we", "they",
    "my", "and", "or", "in", "on", "at", "to", "of", "for", "with", "from",
    "not", "his", "him", "her", "their", "them", "our", "us", "me", "am",
    "are", "was", "were", "been", "being", "this", "that", "these", "those",
    "an", "as", "by", "into", "about", "than", "then", "so", "if", "but",
    "its", "your", "all", "no", "yes", "do", "does", "did", "done", "doing",
    "has", "have", "had", "having", "will", "would", "can", "could", "may",
    "might", "must", "shall", "should", "just", "also", "too", "very",
}

FUNCTION_RU = {
    w.replace("ё", "е")
    for w in {
        "я", "ты", "он", "она", "оно", "мы", "вы", "они", "меня", "тебя", "его",
        "её", "ее", "нас", "вас", "их", "мне", "тебе", "ему", "ей", "нам", "вам",
        "им", "мной", "мною", "тобой", "ним", "ней", "него", "нем", "нём", "ними",
        "неё", "нее",
        "собой", "мой", "моя", "моё", "мое", "мои", "твой", "твоя", "твоё", "твое",
        "твои", "свой", "своя", "своё", "свое", "свои", "наш", "наша", "наше",
        "наши", "ваш", "ваша", "ваше", "ваши", "этот", "эта", "это", "эти",
        "тот", "та", "то", "те", "такой", "такая", "такое", "такие", "весь",
        "вся", "всё", "все", "сам", "сама", "само", "сами", "быть", "есть",
        "был", "была", "было", "были", "буду", "будет", "будем", "будете",
        "будут", "нет", "не", "ни", "да", "уже", "ещё", "еще", "только", "даже",
        "тоже", "также", "очень", "так", "как", "что", "кто", "где", "когда",
        "почему", "куда", "который", "какой", "чтобы", "если", "потому", "ведь",
        "ли", "же", "бы", "вот", "здесь", "тут", "там", "теперь", "сейчас",
        "потом", "всегда", "никогда", "иногда", "от", "до", "по", "со", "из",
        "без", "при", "про", "об", "за", "над", "под", "перед", "после",
        "между", "через", "около", "для", "к", "у", "о", "в", "на", "с", "и",
        "а", "но", "или",
    }
}

IRREGULAR = {
    "bought": "buy", "came": "come", "became": "become", "lost": "lose",
    "fought": "fight", "began": "begin", "ran": "run", "ate": "eat",
    "drank": "drink", "saw": "see", "went": "go", "got": "get",
    "gave": "give", "took": "take", "made": "make", "knew": "know",
    "thought": "think", "told": "tell", "left": "leave", "felt": "feel",
    "kept": "keep", "stood": "stand", "sat": "sit", "wrote": "write",
    "grew": "grow", "wore": "wear", "chose": "choose", "spoke": "speak",
    "heard": "hear", "held": "hold", "found": "find", "said": "say",
    "did": "do", "had": "have", "has": "have", "been": "be", "was": "be",
    "were": "be", "is": "be", "are": "be", "am": "be",
    "tore": "tear", "forgot": "forget", "sent": "send", "broke": "break",
    "clung": "cling", "slept": "sleep", "caught": "catch",
}

allow_en = {
    line.strip().lower()
    for line in (PACK / "_vocab" / "allow_en_15260268.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
} | FUNCTION_EN
allow_ru = {
    line.strip().replace("ё", "е").lower()
    for line in (PACK / "_vocab" / "allow_ru_15260268.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
} | FUNCTION_RU

# (en_lemma, en_ex, ru_lemma, ru_ex)
FIXED = [
    ("melt", "The snow will melt.", "таять", "Снег будет таять."),
    ("psychiatrist", "The psychiatrist helped her.", "психиатр", "Психиатр помогает ей."),
    ("individuality", "Celebrate your individuality every day.", "индивидуальность", "Отмечайте свою индивидуальность каждый день."),
    ("cling", "The boy will cling to the chair.", "вцепиться", "Мальчик вцепится в стул."),
    ("injection", "He received an injection yesterday.", "укол", "Он получил укол вчера."),
    ("privilege", "Education is a significant privilege.", "привилегия", "Образование — это значительная привилегия."),
    ("stock", "This is a stock market.", "фондовый", "Это фондовый рынок."),
    ("string", "She touched the guitar string.", "струна", "Она тронула струну гитары."),
    ("to frown", "She will frown.", "нахмуриться", "Она нахмурится."),
    ("coalition", "The coalition is in the government.", "коалиция", "Коалиция в правительстве."),
    ("to distribute", "They will distribute food.", "раздавать", "Они будут раздавать еду."),
    ("chase", "I saw a police chase.", "погоня", "Я видел погоню полиции."),
    ("to rush by", "The train will rush by.", "проноситься", "Поезд пронесётся мимо."),
    ("cube", "The cube is on the table.", "кубик", "Кубик на столе."),
    ("fur", "Her coat is of fur.", "мех", "Её пальто из меха."),
    ("physiological", "This is a physiological change.", "физиологический", "Это физиологическое изменение."),
    ("disturb", "Please do not disturb me.", "тревожить", "Пожалуйста, не тревожьте меня."),
    ("influenza", "She had influenza in winter.", "грипп", "У неё был грипп зимой."),
    ("professionally", "She sings professionally.", "профессионально", "Она поёт профессионально."),
    ("to stroke", "She will stroke the cat.", "погладить", "Она погладит кошку."),
    ("crumble", "The bread will crumble easily.", "рассыпаться", "Хлеб легко рассыплется."),
    ("sort through", "I will sort through these old books.", "перебирать", "Я буду перебирать эти старые книги."),
    ("ski", "I have a new ski.", "лыжа", "У меня новая лыжа."),
    ("automation", "Automation helps the factory.", "автоматизация", "Автоматизация помогает заводу."),
    ("concrete", "This is a concrete wall.", "бетонный", "Это бетонная стена."),
    ("sight", "He checked the sight.", "прицел", "Он проверил прицел."),
    ("fox", "The fox ran through the forest.", "лиса", "Лиса бежала через лес."),
    ("lighthouse", "The lighthouse is on the rock.", "маяк", "Маяк стоит на скале."),
    ("influential", "He is an influential man.", "влиятельный", "Он влиятельный человек."),
    ("to beat", "He beat this man.", "избить", "Он избил этого человека."),
    ("correctness", "He had a doubt about the correctness of the answer.", "правильность", "У него было сомнение в правильности ответа."),
    ("mechanics", "He studies mechanics.", "механика", "Он учится механике."),
    ("whirlwind", "The whirlwind was strong.", "вихрь", "Вихрь был сильным."),
    ("antenna", "The car's antenna broke.", "антенна", "Антенна машины сломалась."),
    ("publicly", "He spoke publicly.", "публично", "Он говорил публично."),
    ("resort", "We stayed at a resort.", "курорт", "Мы жили на курорте."),
    ("disappoint", "The movie disappointed me.", "разочаровать", "Фильм меня разочаровал."),
    ("predecessor", "His predecessor left yesterday.", "предшественник", "Его предшественник ушёл вчера."),
    ("caution", "You need caution on the street.", "осторожность", "На улице нужна осторожность."),
    ("crying", "I heard her crying.", "плач", "Я слышал её плач."),
    ("nephew", "My nephew lives in the city.", "племянник", "Мой племянник живёт в городе."),
    ("equip", "We need to equip the laboratory.", "оборудовать", "Нам нужно оборудовать лабораторию."),
    ("adapt", "We will adapt the room.", "приспособить", "Мы приспособим комнату."),
    ("to break away", "She will break away from the crowd.", "отрываться", "Она отрывается от толпы."),
    ("greeting", "I heard a greeting.", "приветствие", "Я слышал приветствие."),
    ("controlled", "This process is controlled.", "управляемый", "Этот процесс управляемый."),
    ("ancestral", "They visited their ancestral home.", "родовой", "Они посетили свой родовой дом."),
    ("educator", "The educator helps the boy.", "воспитатель", "Воспитатель помогает мальчику."),
    ("complication", "There is a risk of a complication.", "осложнение", "Есть риск осложнения."),
    ("chop", "I will chop the tree.", "рубить", "Я буду рубить дерево."),
    ("mock", "They often mock him.", "издеваться", "Они часто издеваются над ним."),
    ("desired", "She received the desired gift.", "желанный", "Она получила желанный подарок."),
    ("despise", "I despise this man.", "презирать", "Я презираю этого человека."),
    ("partial", "He offered only a partial answer.", "частичный", "Он предложил только частичный ответ."),
    ("needle", "The needle is on the table.", "игла", "Игла лежит на столе."),
    ("chronic", "He has chronic pain.", "хронический", "У него хроническая боль."),
    ("merge", "Two rivers merge.", "сливаться", "Две реки сливаются."),
    ("to blaze", "The house began to blaze.", "пылать", "Дом начал пылать."),
    ("apology", "Please accept my apology.", "извинение", "Примите моё извинение."),
    ("diamond", "The diamond is in the box.", "алмаз", "Алмаз лежит в ящике."),
    ("hammer", "I need a hammer.", "молоток", "Мне нужен молоток."),
    ("superficial", "His knowledge is superficial.", "поверхностный", "Его знание поверхностное."),
    ("to drown", "He will not drown.", "утонуть", "Он не утонет."),
    ("ecology", "He studies ecology.", "экология", "Он учится экологии."),
    ("ethical", "Is this question ethical?", "этический", "Этот вопрос этический?"),
    ("negatively", "He responded negatively.", "отрицательно", "Он ответил отрицательно."),
    ("rail", "The train is on the rail.", "рельс", "Поезд стоит на рельсе."),
    ("alone", "She wanted to be alone with him.", "наедине", "Она хотела быть наедине с ним."),
    ("bulletin", "Read this bulletin.", "бюллетень", "Прочитайте этот бюллетень."),
    ("bee", "The bee is on the flower.", "пчела", "Пчела на цветке."),
    ("distract", "Loud sounds often distract me.", "отвлекать", "Громкие звуки часто отвлекают меня."),
    ("optical", "He bought optical glasses.", "оптический", "Он купил оптические очки."),
    ("guide", "Our guide was good.", "гид", "Наш гид был хорошим."),
    ("to grow up", "The boy will grow up.", "вырастать", "Мальчик вырастет."),
    ("uncomfortable", "The chair is uncomfortable.", "неудобный", "Стул неудобный."),
    ("stubborn", "He is a stubborn man.", "упрямый", "Он упрямый человек."),
    ("acceleration", "The car's acceleration is good.", "ускорение", "Ускорение машины хорошее."),
    ("total", "This is total control.", "тотальный", "Это тотальный контроль."),
    ("floodplain", "The village is on the floodplain.", "пойма", "Деревня стоит на пойме."),
    ("look around", "Look around the room.", "оглядеться", "Оглядитесь в комнате."),
    ("troubles", "Life is full of troubles.", "хлопоты", "Жизнь полна хлопот."),
    ("supplement", "I will supplement the list.", "дополнить", "Я дополню список."),
    ("to fit", "The books do not fit on the shelf.", "помещаться", "Книги не помещаются на полке."),
    ("worm", "The bird took a worm.", "червь", "Птица взяла червя."),
    ("dictatorship", "This is a dictatorship.", "диктатура", "Это диктатура."),
    ("polyclinic", "I visited the polyclinic yesterday.", "поликлиника", "Я посетил поликлинику вчера."),
    ("to fell", "They will fell the trees.", "валить", "Они будут валить деревья."),
    ("to be indicated", "This is indicated in the text.", "указываться", "Это указывается в тексте."),
    ("taxation", "Taxation is high in this country.", "налогообложение", "Налогообложение в этой стране высокое."),
    ("facade", "The facade of the house is white.", "фасад", "Фасад дома белый."),
    ("young lady", "The young lady is in the room.", "барышня", "Барышня в комнате."),
    ("conquest", "This was an important conquest.", "завоевание", "Это было важное завоевание."),
    ("nastiness", "I will not eat this nastiness.", "гадость", "Я не буду есть такую гадость."),
    ("convincingly", "He spoke convincingly.", "убедительно", "Он говорил убедительно."),
    ("bourgeoisie", "The bourgeoisie has gold.", "буржуазия", "У буржуазии есть золото."),
    ("eat", "Dogs like to eat meat.", "жрать", "Собаки любят жрать мясо."),
    ("font", "Choose another font.", "шрифт", "Выберите другой шрифт."),
    ("container", "The container is already full.", "контейнер", "Контейнер уже полный."),
    ("waste", "This is industrial waste.", "отход", "Это промышленный отход."),
    ("greatcoat", "He wore a greatcoat.", "шинель", "Он надел шинель."),
]


def en_forms(word: str) -> set[str]:
    forms = {word}
    if word in IRREGULAR:
        forms.add(IRREGULAR[word])
    for suffix in ("'s", "s", "es", "ed", "ing", "ly", "er", "est"):
        if word.endswith(suffix) and len(word) > len(suffix) + 2:
            forms.add(word[: -len(suffix)])
    if word.endswith("ies") and len(word) > 4:
        forms.add(word[:-3] + "y")
    if word.endswith("ied") and len(word) > 4:
        forms.add(word[:-3] + "y")
    if word.endswith("ing") and len(word) > 5:
        forms.add(word[:-3] + "e")
    if word.endswith("ed") and len(word) > 4:
        forms.add(word[:-1])
    return forms


def en_ok(text: str, extra: set[str]) -> list[str]:
    bad = []
    for raw in re.findall(r"[A-Za-z']+", text):
        w = raw.lower().replace("'", "")
        if not w or w in allow_en or w in extra:
            continue
        if any(form in allow_en or form in extra for form in en_forms(w)):
            continue
        if w.endswith("ly") and w[:-2] + "l" in allow_en:
            continue
        for lemma in allow_en | extra:
            parts = lemma.replace("-", " ").split()
            if w in parts:
                break
        else:
            bad.append(raw)
    return bad


RU_IRREG = {
    "пить": ("пь",),
    "есть": ("ед", "еш", "ем", "ел"),
    "идти": ("ид", "шл", "ше"),
    "пойти": ("пой", "пош"),
    "мочь": ("мож", "мог"),
    "учить": ("уч",),
    "взять": ("возьм", "взя"),
    "уйти": ("уш", "уйд"),
    "жрать": ("жр",),
}


def ru_ok(text: str, extra: set[str]) -> list[str]:
    bad = []
    pool = allow_ru | extra
    for raw in re.findall(r"[А-Яа-яЁё-]+", text):
        w = raw.replace("ё", "е").replace("Ё", "е").lower()
        if w in pool:
            continue
        if any(
            w.startswith(lemma) or lemma.startswith(w)
            for lemma in pool
            if len(lemma) >= 3 and len(w) >= 3
        ):
            continue
        if any(
            w[:3] == lemma[:3]
            for lemma in pool
            if len(lemma) >= 3 and len(w) >= 3
        ):
            continue
        if any(
            lemma in pool and any(w.startswith(stem) for stem in stems)
            for lemma, stems in RU_IRREG.items()
        ):
            continue
        bad.append(raw)
    return bad


def make_card(en: str, en_ex: str, ru: str, ru_ex: str) -> dict:
    return card_write_payload(
        {
            "qMdPrompt": "Translate:",
            "qMdBody": en,
            "qMdClarifier": "",
            "qMdFootnote": en_ex,
            "aMdPrompt": "",
            "aMdBody": ru,
            "aMdClarifier": "",
            "aMdFootnote": ru_ex,
        }
    )


def lemma_in_en(gloss: str, example: str) -> bool:
    g = gloss.lower()
    ex = example.lower()
    if g in ex:
        return True
    key = re.sub(r"^(to |the |a |an )", "", g)
    if key in ex:
        return True
    parts = [p for p in key.replace("-", " ").split() if p not in {"to", "the", "a", "an", "be"}]
    return all(p in ex for p in parts) if parts else False


def lemma_in_ru(lemma: str, example: str) -> bool:
    key = lemma.lower().replace("ё", "е")
    ex = example.lower().replace("ё", "е")
    if key in ex:
        return True
    if len(key) >= 4 and key[:4] in ex:
        return True
    if len(key) >= 5 and key[:5] in ex:
        return True
    return False


def main() -> None:
    originals = cards_from_path(SRC)
    if len(originals) != 100 or len(FIXED) != 100:
        raise SystemExit(f"expected 100, got {len(originals)} / {len(FIXED)}")

    cards = []
    leftover = []
    for i, (en, en_ex, ru, ru_ex) in enumerate(FIXED, 1):
        orig = originals[i - 1]
        if orig["qMdBody"] != en:
            leftover.append(f"{i}: gloss changed {orig['qMdBody']!r} -> {en!r}")
        extra_en = set(re.findall(r"[a-z']+", en.lower()))
        extra_en |= set(en.lower().replace("-", " ").split())
        extra_ru = {w.replace("ё", "е").lower() for w in re.findall(r"[А-Яа-яЁё-]+", ru)}
        for token in en_ok(en_ex, extra_en):
            leftover.append(f"{i} EN leftover {token!r}: {en_ex}")
        for token in ru_ok(ru_ex, extra_ru):
            leftover.append(f"{i} RU leftover {token!r}: {ru_ex}")
        if not lemma_in_en(en, en_ex):
            leftover.append(f"{i}: EN example missing {en!r}")
        if not lemma_in_ru(ru, ru_ex):
            leftover.append(f"{i}: RU example missing {ru!r}")
        cards.append(make_card(en, en_ex, ru, ru_ex))

    write_csv(OUT, cards)
    loaded = cards_from_path(OUT)
    if len(loaded) != 100:
        raise SystemExit(f"cards_from_path returned {len(loaded)}")

    changed = sum(1 for a, b in zip(originals, loaded) if not cards_match(a, b))
    LOG.write_text(f"{changed}\n", encoding="utf-8")
    print(f"wrote {OUT}")
    print(f"cards_from_path={len(loaded)}")
    print(f"changed={changed}")
    if leftover:
        print("LEFTOVER / CHECKS:")
        print("\n".join(leftover))
    else:
        print("vocab check clean")


if __name__ == "__main__":
    main()
