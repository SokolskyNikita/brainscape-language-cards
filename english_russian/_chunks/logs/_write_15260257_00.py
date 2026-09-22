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

SRC = PACK / "_chunks" / "deck_15260257_00.csv"
OUT = PACK / "_chunks" / "fixed" / "deck_15260257_00.csv"
LOG = PACK / "_chunks" / "logs" / "deck_15260257_00.txt"

FUNCTION = {
    "a", "the", "is", "be", "i", "you", "he", "she", "it", "we", "they",
    "my", "and", "or", "in", "on", "at", "to", "of", "for", "with", "from",
    "not", "his", "him", "her", "their", "them", "our", "us", "me", "am",
    "are", "was", "were", "been", "being", "this", "that", "these", "those",
    "an", "as", "by", "into", "about", "than", "then", "so", "if", "but",
    "its", "your", "can", "will", "would", "could", "should", "may", "must",
    "do", "did", "does", "have", "has", "had", "here", "there", "now",
    "please", "let", "lets", "don't", "didn't", "i'm", "it's", "yes", "no",
}

IRREGULAR = {
    "took": "take", "taken": "take", "came": "come", "gone": "go", "went": "go",
    "won": "win", "stole": "steal", "stolen": "steal", "wore": "wear",
    "worn": "wear", "felt": "feel", "built": "build", "caught": "catch",
    "saw": "see", "seen": "see", "heard": "hear", "bought": "buy",
    "left": "leave", "gave": "give", "given": "give", "found": "find",
    "made": "make", "said": "say", "told": "tell", "knew": "know",
    "got": "get", "thought": "think", "taught": "teach", "stood": "stand",
    "lit": "light", "ran": "run", "sat": "sit", "began": "begin",
    "stopped": "stop", "stopping": "stop",
    "became": "become", "broke": "break", "chose": "choose", "drove": "drive",
    "ate": "eat", "fell": "fall", "flew": "fly", "forgot": "forget",
    "grew": "grow", "held": "hold", "kept": "keep", "led": "lead",
    "lost": "lose", "met": "meet", "paid": "pay", "put": "put",
    "read": "read", "rode": "ride", "rose": "rise", "sang": "sing",
    "slept": "sleep", "spoke": "speak", "swam": "swim", "took": "take",
    "wrote": "write", "written": "write", "done": "do", "been": "be",
}

RU_FUNCTION = {
    "я", "ты", "он", "она", "оно", "мы", "вы", "они", "мой", "моя", "моё",
    "мои", "твой", "его", "её", "ее", "их", "наш", "ваш", "мне", "меня",
    "тебе", "тебя", "ему", "ему", "ей", "нас", "вам", "вас", "им", "их",
    "себя", "себе", "свой", "своя", "своё", "свои", "свою", "своим", "своей",
    "в", "на", "с", "со", "из", "к", "ко", "у", "о", "об", "от", "по", "за",
    "для", "до", "при", "без", "над", "под", "про", "между", "через",
    "и", "или", "но", "а", "да", "не", "ни", "же", "ли", "бы", "то", "это",
    "этот", "эта", "эти", "тот", "та", "те", "быть", "был", "была", "было",
    "были", "есть", "будет", "будут", "уже", "ещё", "еще", "вот", "там",
    "тут", "здесь", "очень", "также", "только", "уже", "чем", "как", "что",
    "чтобы", "если", "когда", "где", "куда", "откуда", "потому", "поэтому",
    "давайте", "пожалуйста", "-", "—",
}

allow_en = {
    line.strip().lower()
    for line in (PACK / "_vocab" / "allow_en_15260257.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_ru = {
    line.strip().replace("ё", "е").lower()
    for line in (PACK / "_vocab" / "allow_ru_15260257.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_en |= FUNCTION

# (en_lemma, en_ex, ru_lemma, ru_ex)
FIXED = [
    ("cave", "The cave is dark.", "пещера", "В пещере темно."),
    ("red-haired", "The red-haired girl smiled brightly.", "рыжий", "Рыжая девушка ярко улыбнулась."),
    ("worldwide", "This is a worldwide problem.", "всемирный", "Это всемирная проблема."),
    ("perfect", "Your answer was perfect.", "совершенный", "Ваш ответ был совершенным."),
    ("pillow", "I need a new pillow.", "подушка", "Мне нужна новая подушка."),
    ("to rely", "I learned to rely on myself.", "полагаться", "Я научился полагаться на себя."),
    ("colored", "I bought a colored book.", "цветной", "Я купил цветную книгу."),
    ("manner", "I like his manner.", "манера", "Мне нравится его манера."),
    ("to object", "I want to object.", "возразить", "Я хочу возразить."),
    ("call", "I heard the call.", "призыв", "Я слышал призыв."),
    ("approve", "They will approve this plan.", "утвердить", "Они утвердят этот план."),
    ("Greek", "I love Greek music.", "греческий", "Я люблю греческую музыку."),
    ("to be built", "The house is to be built soon.", "строиться", "Дом скоро будет строиться."),
    ("talented", "She is a talented artist.", "талантливый", "Она талантливый художник."),
    ("monitor", "I bought a new computer monitor.", "монитор", "Я купил новый монитор для компьютера."),
    ("dragon", "I saw a dragon.", "дракон", "Я видел дракона."),
    ("regularly", "I read regularly.", "регулярно", "Я регулярно читаю."),
    ("exhibit", "They will exhibit new art.", "выставить", "Они выставят новое искусство."),
    ("obstacle", "This is a big obstacle.", "препятствие", "Это большое препятствие."),
    ("magical", "The night sky looked magical.", "волшебный", "Ночное небо выглядело волшебным."),
    ("match", "They won the football match.", "матч", "Они победили в футбольном матче."),
    ("lantern", "He took the lantern.", "фонарь", "Он взял фонарь."),
    ("officially", "He officially announced the news.", "официально", "Он официально объявил новость."),
    ("confirmation", "I need confirmation.", "подтверждение", "Мне нужно подтверждение."),
    ("seventh", "He finished seventh.", "седьмой", "Он закончил седьмым."),
    ("elevator", "The elevator stopped.", "лифт", "Лифт остановился."),
    ("be produced", "Cars can be produced in a factory.", "производиться", "Машины могут производиться на заводе."),
    ("indicated", "This is the indicated path.", "указанный", "Это указанный путь."),
    ("adjust", "Please adjust the radio.", "настроить", "Пожалуйста, настройте радио."),
    ("flag", "I see the flag.", "флаг", "Я вижу флаг."),
    ("possession", "The house is in my possession.", "владение", "Дом в моём владении."),
    ("elite", "The elite came.", "элита", "Элита пришла."),
    ("battery", "I need a new battery.", "батарея", "Мне нужна новая батарея."),
    ("adventure", "This is a great adventure.", "приключение", "Это великое приключение."),
    ("curious", "The girl was curious.", "любопытный", "Девушка была любопытна."),
    ("wise", "A wise person thinks.", "мудрый", "Мудрый человек думает."),
    ("normally", "He works normally.", "нормально", "Он работает нормально."),
    ("pale", "Her face turned pale.", "бледный", "Её лицо стало бледным."),
    ("thief", "The thief stole my bag.", "вор", "Вор украл мою сумку."),
    ("gain", "She hoped to gain his trust.", "обрести", "Она надеялась обрести его доверие."),
    ("grandson", "My grandson plays football.", "внук", "Мой внук играет в футбол."),
    ("dawn", "Dawn came early.", "рассвет", "Рассвет наступил рано."),
    ("slope", "The slope is covered in snow.", "склон", "Склон покрыт снегом."),
    ("province", "He lives in the province.", "провинция", "Он живёт в провинции."),
    ("formulate", "Let's formulate a clear plan.", "сформулировать", "Давайте сформулируем ясный план."),
    ("so as to", "He left so as to sleep.", "дабы", "Он ушёл, дабы спать дома."),
    ("not far", "The store is not far from here.", "недалеко", "Магазин недалеко отсюда."),
    ("in a row", "He won three games in a row.", "подряд", "Он победил в трёх играх подряд."),
    ("beach", "We are on the beach.", "пляж", "Мы на пляже."),
    ("to get caught", "He tried to cheat and got caught.", "попасться", "Он пытался обмануть и попался."),
    ("finish", "I must finish this task today.", "закончить", "Мне надо закончить эту задачу сегодня."),
    ("grateful", "I am grateful for your help today.", "благодарный", "Я благодарен за вашу помощь сегодня."),
    ("to inquire", "I want to inquire about the price.", "поинтересоваться", "Я хочу поинтересоваться о цене."),
    ("feather", "She found a bird's feather outside.", "перо", "Она нашла перо птицы на улице."),
    ("fashionable", "She wore a fashionable dress today.", "модный", "Она надела модное платье сегодня."),
    ("gaming", "This is a gaming computer.", "игровой", "Это игровой компьютер."),
    ("push", "Give the door a push.", "толк", "Дай двери толк."),
    ("to save", "I want to save her life.", "спасать", "Я хочу спасать её жизнь."),
    ("to avoid", "She learned to avoid him.", "избегать", "Она научилась избегать его."),
    ("to be proud of", "I am proud of you.", "гордиться", "Я горжусь тобой."),
    ("fill in", "Please fill in the form.", "заполнить", "Пожалуйста, заполните форму."),
    ("marketing", "I work in marketing.", "маркетинг", "Я работаю в маркетинге."),
    ("railway", "This is a railway station.", "железнодорожный", "Это железнодорожная станция."),
    ("curiosity", "Curiosity is natural.", "любопытство", "Любопытство естественно."),
    ("to be supposed", "He is supposed to come tomorrow.", "предполагаться", "Предполагается, что он придёт завтра."),
    ("rhythm", "I like this rhythm.", "ритм", "Мне нравится этот ритм."),
    ("completion", "The work is near completion.", "завершение", "Работа близка к завершению."),
    ("feat", "This was a great feat.", "подвиг", "Это был великий подвиг."),
    ("nerve", "The doctor found the nerve.", "нерв", "Врач нашёл нерв."),
    ("deceive", "Do not deceive me.", "обмануть", "Не обмани меня."),
    ("pilot", "The pilot came.", "пилот", "Пилот пришёл."),
    ("voting", "Voting is important.", "голосование", "Голосование важно."),
    ("Mrs.", "Mrs. came today.", "миссис", "Миссис пришла сегодня."),
    ("ashamed", "He felt ashamed of his actions.", "стыдно", "Ему было стыдно за свои действия."),
    ("illusion", "Love was an illusion.", "иллюзия", "Любовь была иллюзией."),
    ("genius", "He is a true genius.", "гений", "Он настоящий гений."),
    ("swim", "I love to swim in the ocean.", "плавать", "Я люблю плавать в океане."),
    ("solid", "This is a solid wall.", "сплошной", "Это сплошная стена."),
    ("invisible", "He is invisible.", "невидимый", "Он невидимый."),
    ("joyful", "She is joyful today.", "радостный", "Она радостная сегодня."),
    ("academician", "The academician published a book.", "академик", "Академик опубликовала книгу."),
    ("hey", "Hey, wait for me!", "эй", "Эй, подожди меня!"),
    ("socialist", "This is a socialist idea.", "социалистический", "Это социалистическая идея."),
    ("indeed", "She did indeed finish the project.", "таки", "Она таки закончила проект."),
    ("to be given", "Language is given easily to her.", "даваться", "Язык давался ей легко."),
    ("promotion", "She received a promotion yesterday.", "продвижение", "Она получила продвижение вчера."),
    ("to lose", "He did not want to lose the game.", "проиграть", "Он не хотел проиграть в игре."),
    ("invest", "I will invest time.", "вложить", "Я вложу время."),
    ("protest", "They organized a protest.", "протест", "Они организовали протест."),
    ("limited", "Time is limited.", "ограниченный", "Время ограничено."),
    ("developed", "This is a developed country.", "развитый", "Это развитая страна."),
    ("to compare", "I want to compare these books.", "сравнивать", "Я хочу сравнивать эти книги."),
    ("treat", "Doctors treat patients every day.", "лечить", "Врач лечит пациентов каждый день."),
    ("coach", "The coach came to the team.", "тренер", "Тренер пришёл к команде."),
    ("Muscovite", "The Muscovite lives in the city.", "москвич", "Москвич живёт в городе."),
    ("top", "I see the top of the mountain.", "верх", "Я вижу верх горы."),
    ("satisfy", "This food will satisfy your hunger.", "удовлетворить", "Эта еда удовлетворит ваш голод."),
    ("suppress", "They suppress the voice.", "подавлять", "Они подавляют голос."),
    ("depict", "The artist will depict your dreams.", "изобразить", "Художник изобразит ваши мечты."),
    ("hat", "She wore a beautiful red hat.", "шляпа", "Она надела красивую красную шляпу."),
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


def extra_en(card_en: str) -> set[str]:
    key = card_en.lower().replace("to ", "")
    extra = {key}
    extra.update(key.replace(".", "").split())
    extra.update(en_forms(key))
    for part in key.split():
        extra.update(en_forms(part))
    return extra


def extra_ru(card_ru: str) -> set[str]:
    key = card_ru.lower().replace("ё", "е")
    extra = {key}
    extra.update(key.replace("-", " ").split())
    return extra


def en_ok(text: str, card_en: str) -> list[str]:
    extra = extra_en(card_en)
    bad = []
    for raw in re.findall(r"[A-Za-z']+", text):
        w = raw.lower().replace("'", "")
        if not w or w in allow_en or w in extra:
            continue
        if any(form in allow_en or form in extra for form in en_forms(w)):
            continue
        if w.endswith("ly") and w[:-2] + "l" in allow_en:
            continue
        bad.append(raw)
    return bad


def ru_ok(text: str, card_ru: str) -> list[str]:
    extra = extra_ru(card_ru)
    bad = []
    for raw in re.findall(r"[А-Яа-яЁё-]+", text):
        w = raw.replace("ё", "е").replace("Ё", "е").lower()
        if w in allow_ru or w in extra or w in RU_FUNCTION:
            continue
        pool = allow_ru | extra
        if any(w.startswith(lemma) or lemma.startswith(w) for lemma in pool if len(lemma) >= 3 and len(w) >= 3):
            continue
        if any(
            w[: max(3, len(w) - 3)] == lemma[: max(3, len(w) - 3)]
            for lemma in pool
            if abs(len(lemma) - len(w)) <= 5 and min(len(lemma), len(w)) >= 3
        ):
            continue
        if any(w[:3] == lemma[:3] for lemma in extra if len(lemma) >= 3 and len(w) >= 3):
            continue
        bad.append(raw)
    return bad


def has_en_lemma(en: str, example: str) -> bool:
    ex = example.lower()
    key = en.lower().replace("to ", "")
    if key in ex or en.lower() in ex:
        return True
    parts = [p for p in re.split(r"[\s.]+", key) if p and p not in {"to", "be", "a", "the", "of"}]
    return any(p in ex for p in parts)


def has_ru_lemma(ru: str, example: str) -> bool:
    t = example.lower().replace("ё", "е")
    l = ru.lower().replace("ё", "е")
    if l in t:
        return True
    for n in range(min(len(l), 6), 2, -1):
        if l[:n] in t:
            return True
    return False


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
        for token in en_ok(en_ex, en):
            leftover.append(f"{i} EN leftover {token!r}: {en_ex}")
        for token in ru_ok(ru_ex, ru):
            leftover.append(f"{i} RU leftover {token!r}: {ru_ex}")
        if not has_en_lemma(en, en_ex):
            leftover.append(f"{i}: EN example missing {en!r}")
        if not has_ru_lemma(ru, ru_ex):
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


if __name__ == "__main__":
    main()
