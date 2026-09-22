#!/usr/bin/env python3
"""Rewrite english_russian deck_15260277_04 (cards 401-500, band 6000->6500)."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PACK = ROOT / "english_russian"
sys.path.insert(0, str(ROOT))

from brainscape.cards import card_write_payload, cards_from_path, cards_match
from english_russian._chunk_io import write_csv

SRC = PACK / "_chunks" / "deck_15260277_04.csv"
OUT = PACK / "_chunks" / "fixed" / "deck_15260277_04.csv"
LOG = PACK / "_chunks" / "logs" / "deck_15260277_04.txt"

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
}

FUNCTION_RU = {
    "я", "мне", "меня", "мной", "мой", "моя", "мое", "моё", "мои", "мою",
    "мы", "нам", "нас", "нами", "наш", "наша", "наше", "наши", "нашу",
    "ты", "тебе", "тебя", "тобой", "твой", "твоя", "твое", "твоё", "твои",
    "вы", "вам", "вас", "вами", "ваш", "ваша", "ваше", "ваши", "вашу",
    "он", "она", "оно", "они", "его", "ее", "её", "ей", "ему", "им", "их",
    "ими", "ним", "ней", "ними", "него", "нее", "неё",
    "себя", "себе", "собой", "свой", "своя", "свое", "своё", "свои", "свою", "своим", "своего", "своей",
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
}

allow_en = {
    line.strip().lower()
    for line in (PACK / "_vocab" / "allow_en_15260277.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_ru = {
    line.strip().replace("ё", "е").lower()
    for line in (PACK / "_vocab" / "allow_ru_15260277.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_en |= FUNCTION_EN
allow_ru |= FUNCTION_RU

# (en_lemma, en_ex, ru_lemma, ru_ex)
FIXED = [
    ("grammatical", "This sentence has a grammatical error.", "грамматический", "В этом предложении есть грамматическая ошибка."),
    ("to be released", "New books are to be released every month.", "выпускаться", "Новые книги должны выпускаться каждый месяц."),
    ("elastic band", "I lost my elastic band.", "резинка", "Я потерял свою резинку."),
    ("adjoin", "The garden adjoins the house.", "прилегать", "Сад прилегает к дому."),
    ("bookmark", "I lost my bookmark.", "закладка", "Я потерял свою закладку."),
    ("unforgettable", "It was an unforgettable day.", "незабываемый", "Это был незабываемый день."),
    ("tease", "She loves to tease her brother.", "дразнить", "Она любит дразнить своего брата."),
    ("to intersect", "The roads intersect here.", "пересекаться", "Дороги пересекаются здесь."),
    ("power station", "The power station is large.", "электростанция", "Электростанция большая."),
    ("parody", "This book is a parody.", "пародия", "Эта книга — пародия."),
    ("quay", "The boat is at the quay.", "причал", "Лодка у причала."),
    ("inquire", "May I inquire about your health?", "осведомиться", "Могу ли я осведомиться о вашем здоровье?"),
    ("to take a closer look", "I wanted to take a closer look.", "присмотреться", "Я хотел присмотреться."),
    ("grimace", "He made a grimace.", "гримаса", "Он сделал гримасу."),
    ("Azerbaijani", "She speaks Azerbaijani.", "азербайджанский", "Она говорит на азербайджанском."),
    ("working capacity", "His working capacity is high.", "работоспособность", "Его работоспособность высокая."),
    ("rabbi", "The rabbi spoke to the people.", "раввин", "Раввин говорил с народом."),
    ("gunpowder", "Gunpowder is dangerous.", "порох", "Порох опасен."),
    ("impotence", "He felt impotence.", "бессилие", "Он чувствовал бессилие."),
    ("to be translated", "This text is to be translated.", "переводиться", "Этот текст должен переводиться."),
    ("poisoning", "He had food poisoning.", "отравление", "У него было отравление."),
    ("belief", "This is an old belief.", "верование", "Это старое верование."),
    ("witty", "He is a witty man.", "остроумный", "Он остроумный человек."),
    ("ailment", "This ailment is not dangerous.", "недуг", "Этот недуг не опасен."),
    ("to build", "They want to build a plan.", "выстраивать", "Они хотят выстраивать план."),
    ("nationalist", "He is a nationalist.", "националист", "Он националист."),
    ("unsuccessfully", "He tried unsuccessfully to open the door.", "безуспешно", "Он безуспешно пытался открыть дверь."),
    ("to be appointed", "She is to be appointed soon.", "назначаться", "Она скоро должна назначаться."),
    ("robber", "The robber ran away.", "грабитель", "Грабитель убежал."),
    ("monotonous", "The work is monotonous.", "однообразный", "Работа однообразная."),
    ("chord", "He played a beautiful chord.", "аккорд", "Он сыграл красивый аккорд."),
    ("eccentric", "He is an eccentric.", "чудак", "Он чудак."),
    ("oversleep", "I may oversleep today.", "проспать", "Я могу проспать сегодня."),
    ("throw on", "Throw on a jacket.", "накинуть", "Накинь куртку."),
    ("feverishly", "She worked feverishly.", "лихорадочно", "Она лихорадочно работала."),
    ("uneven", "The road is uneven.", "неровный", "Дорога неровная."),
    ("tavern", "They met at the old tavern.", "кабак", "Они встретились в старом кабаке."),
    ("rudeness", "His rudeness surprised me.", "грубость", "Его грубость меня удивила."),
    ("exceeding", "Exceeding the speed is dangerous.", "превышение", "Превышение скорости опасно."),
    ("to crowd", "We began to crowd at the door.", "толпиться", "Мы начали толпиться у двери."),
    ("to slaughter", "They must slaughter the sick animal.", "зарезать", "Они должны зарезать больное животное."),
    ("precedent", "This case sets a precedent.", "прецедент", "Это дело создает прецедент."),
    ("insure", "We must insure our new house.", "застраховать", "Мы должны застраховать наш новый дом."),
    ("to bite", "The dog tried to bite me.", "укусить", "Собака пыталась укусить меня."),
    ("fraud", "He was accused of fraud.", "мошенничество", "Его обвинили в мошенничестве."),
    ("revival", "The city experienced a revival.", "оживление", "Город пережил оживление."),
    ("stroke", "He added one stroke.", "штрих", "Он добавил один штрих."),
    ("scorpion", "I saw a scorpion.", "скорпион", "Я видел скорпиона."),
    ("rape", "Rape is a crime.", "изнасилование", "Изнасилование — преступление."),
    ("convulsion", "He had a convulsion.", "судорога", "У него была судорога."),
    ("to swoop", "They will swoop on the city.", "налететь", "Они налетят на город."),
    ("mapping", "This mapping is useful.", "отображение", "Это отображение полезно."),
    ("crafty", "He is a crafty man.", "лукавый", "Он лукавый человек."),
    ("worship service", "They were at the worship service together.", "богослужение", "Они вместе были на богослужении."),
    ("cooling", "We need cooling.", "охлаждение", "Нам нужно охлаждение."),
    ("to spite", "He did this to spite her.", "назло", "Он сделал это назло ей."),
    ("literacy", "Literacy opens the door to knowledge.", "грамотность", "Грамотность открывает дверь к знаниям."),
    ("forcibly", "They forcibly closed the door.", "насильно", "Они насильно закрыли дверь."),
    ("sculptor", "The sculptor made a statue.", "скульптор", "Скульптор сделал статую."),
    ("table of contents", "Check the table of contents.", "оглавление", "Проверьте оглавление."),
    ("Dutchman", "He is a Dutchman.", "голландец", "Он голландец."),
    ("jewelry", "She bought jewelry.", "ювелирные изделия", "Она купила ювелирные изделия."),
    ("into one", "They gathered into one.", "воедино", "Они собрались воедино."),
    ("fraught", "The plan is fraught with danger.", "чреватый", "План чреват опасностью."),
    ("issues", "We discussed these issues.", "проблематика", "Мы обсудили эту проблематику."),
    ("toss", "He will toss the coin now.", "подбросить", "Он сейчас подбросит монету."),
    ("to pack", "I need to pack the books.", "упаковать", "Мне нужно упаковать книги."),
    ("reconciliation", "They wanted reconciliation after the argument.", "примирение", "Они хотели примирения после спора."),
    ("rub", "I need to rub the table.", "тереть", "Мне нужно тереть стол."),
    ("to ring", "I forgot to ring you yesterday.", "зазвонить", "Я забыл зазвонить тебе вчера."),
    ("lawn", "The lawn is large.", "газон", "Газон большой."),
    ("astonishingly", "Astonishingly, this is true.", "поразительно", "Поразительно, это правда."),
    ("polemic", "There was a polemic.", "полемика", "Была полемика."),
    ("warmth", "I felt the warmth of the sun.", "теплота", "Я чувствовал теплоту солнца."),
    ("acoustic", "This is acoustic music.", "акустический", "Это акустическая музыка."),
    ("dazzling", "She has a dazzling smile.", "ослепительный", "У неё ослепительная улыбка."),
    ("ataman", "The ataman will lead the people.", "атаман", "Атаман будет вести народ."),
    ("graduation", "Her graduation was yesterday.", "выпускной", "Её выпускной был вчера."),
    ("methodological", "This is a methodological question.", "методологический", "Это методологический вопрос."),
    ("rope", "He held the rope.", "канат", "Он держал канат."),
    ("niece", "I have a niece.", "племянница", "У меня есть племянница."),
    ("to elect", "They elect a president every year.", "избирать", "Они избирают президента каждый год."),
    ("lost", "He felt lost without her.", "потерянный", "Он чувствовал себя потерянным без неё."),
    ("mast", "The ship's mast is high.", "мачта", "Мачта корабля высокая."),
    ("hurry", "There is no hurry.", "спешка", "Спешки нет."),
    ("step over", "He must step over the bag.", "переступить", "Он должен переступить через сумку."),
    ("bell tower", "The bell tower is high.", "колокольня", "Колокольня высокая."),
    ("factory director", "The factory director is here today.", "директор завода", "Директор завода сегодня здесь."),
    ("send off", "I must send off the letter tomorrow.", "отослать", "Я должен отослать письмо завтра."),
    ("to survive", "They learned to survive.", "выживать", "Они научились выживать."),
    ("moose", "A moose stood on the road.", "лось", "Лось стоял на дороге."),
    ("to reconcile", "They want to reconcile.", "мириться", "Они хотят мириться."),
    ("inequality", "Inequality is a problem.", "неравенство", "Неравенство — проблема."),
    ("specification", "Check the specification.", "спецификация", "Проверьте спецификацию."),
    ("dwarf", "The dwarf stood among us.", "карлик", "Карлик стоял среди нас."),
    ("eleventh", "He is in eleventh place.", "одиннадцатый", "Он на одиннадцатом месте."),
    ("recover", "She will recover soon.", "поправиться", "Она скоро поправится."),
    ("darken", "The sky will darken soon.", "потемнеть", "Небо скоро потемнеет."),
    ("be famous for", "This city is famous for its park.", "славиться", "Этот город славится своим парком."),
    ("razor", "He bought a razor.", "бритва", "Он купил бритву."),
]


def en_forms(word: str) -> set[str]:
    forms = {word}
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
        forms.add(word[:-2])
    if word.endswith("d") and len(word) > 4:
        forms.add(word[:-1])
    return forms


IRREGULAR_EN = {
    "made": "make", "went": "go", "gone": "go", "bought": "buy",
    "knew": "know", "known": "know", "sold": "sell", "grew": "grow",
    "grown": "grow", "took": "take", "taken": "take", "gave": "give",
    "given": "give", "saw": "see", "seen": "see", "came": "come",
    "did": "do", "done": "do", "had": "have", "said": "say",
    "told": "tell", "got": "get", "found": "find", "left": "leave",
    "kept": "keep", "felt": "feel", "thought": "think", "brought": "bring",
    "stood": "stand", "sat": "sit", "ran": "run", "won": "win",
    "lost": "lose", "met": "meet", "led": "lead", "paid": "pay",
    "spoke": "speak", "written": "write", "wrote": "write",
    "ate": "eat", "eaten": "eat", "drank": "drink", "drunk": "drink",
    "wore": "wear", "worn": "wear", "slept": "sleep", "taught": "teach",
    "began": "begin", "begun": "begin", "held": "hold", "lit": "light",
    "forgot": "forget", "forgotten": "forget",
}


def en_ok(text: str, extra: set[str]) -> list[str]:
    allowed = allow_en | extra
    bad = []
    for raw in re.findall(r"[A-Za-z']+", text):
        w = raw.lower().replace("'", "")
        if not w or w in allowed:
            continue
        if IRREGULAR_EN.get(w, "") in allowed:
            continue
        if any(form in allowed for form in en_forms(w)):
            continue
        if w.endswith("ly") and w[:-2] in allowed:
            continue
        bad.append(raw)
    return bad


RU_ENDINGS = (
    "ями", "ами", "ого", "его", "ому", "ему", "ыми", "ими",
    "ая", "яя", "ое", "ее", "ие", "ые", "ой", "ей", "ий", "ый",
    "ую", "юю", "ов", "ев", "ей", "ам", "ям", "ом", "ем",
    "ах", "ях", "ию", "ью", "ия", "ья", "ие", "ье",
    "ть", "ти", "ла", "ло", "ли", "ет", "ют", "ут", "ит", "ат", "ят",
    "ешь", "ишь", "ете", "ите", "ём", "ем", "им",
    "а", "я", "о", "е", "у", "ю", "ы", "и",
)


def ru_stems(word: str) -> set[str]:
    stems = {word}
    for end in RU_ENDINGS:
        if word.endswith(end) and len(word) - len(end) >= 3:
            stems.add(word[: -len(end)])
    if len(word) >= 5:
        stems.add(word[:5])
        stems.add(word[:4])
    return stems


def ru_ok(text: str, extra: set[str]) -> list[str]:
    allowed = allow_ru | extra
    bad = []
    for raw in re.findall(r"[А-Яа-яЁё-]+", text):
        if raw.replace("-", "") == "":
            continue
        w = raw.replace("ё", "е").replace("Ё", "е").lower()
        if w in allowed:
            continue
        stems = ru_stems(w)
        if any(stem in allowed for stem in stems if len(stem) >= 3):
            continue
        if any(w.startswith(lemma) or lemma.startswith(w) for lemma in allowed if len(lemma) >= 4 and len(w) >= 4):
            continue
        if any(
            w[: max(4, len(w) - 3)] == lemma[: max(4, len(w) - 3)]
            for lemma in allowed
            if abs(len(lemma) - len(w)) <= 4 and min(len(lemma), len(w)) >= 4
        ):
            continue
        if any(stem.startswith(lemma[:4]) or lemma.startswith(stem[:4]) for lemma in allowed for stem in stems if len(lemma) >= 4 and len(stem) >= 4):
            continue
        bad.append(raw)
    return bad


def lemma_tokens_en(en: str) -> set[str]:
    parts = re.findall(r"[A-Za-z']+", en.lower().replace("(", " ").replace(")", " "))
    extra = set(parts)
    extra.discard("to")
    extra.discard("the")
    extra.discard("a")
    extra.discard("an")
    return extra


def lemma_tokens_ru(ru: str) -> set[str]:
    parts = re.findall(r"[А-Яа-яЁё-]+", ru)
    return {p.replace("ё", "е").replace("Ё", "е").lower() for p in parts}


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
        extra_en = lemma_tokens_en(en)
        extra_ru = lemma_tokens_ru(ru)
        for token in en_ok(en_ex, extra_en):
            leftover.append(f"{i} EN leftover {token!r}: {en_ex}")
        for token in ru_ok(ru_ex, extra_ru):
            leftover.append(f"{i} RU leftover {token!r}: {ru_ex}")
        if en.split()[0].lower() not in en_ex.lower() and en.lower() not in en_ex.lower():
            key = en.lower().replace("to ", "")
            if key not in en_ex.lower() and not any(p in en_ex.lower() for p in key.split()):
                leftover.append(f"{i}: EN example missing {en!r}")
        ru_key = ru.lower().replace("ё", "е")
        ru_ex_n = ru_ex.lower().replace("ё", "е")
        first = ru_key.split()[0]
        if first[:4] not in ru_ex_n and first[:3] not in ru_ex_n:
            leftover.append(f"{i}: RU example missing {ru!r}")
        cards.append(make_card(en, en_ex, ru, ru_ex))

    OUT.parent.mkdir(parents=True, exist_ok=True)
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
