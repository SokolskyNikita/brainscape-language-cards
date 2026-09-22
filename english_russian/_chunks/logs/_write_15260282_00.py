#!/usr/bin/env python3
from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PACK = ROOT / "english_russian"
sys.path.insert(0, str(ROOT))

from brainscape.cards import card_write_payload, cards_from_path, cards_match

SRC = PACK / "_chunks" / "deck_15260282_00.csv"
OUT = PACK / "_chunks" / "fixed" / "deck_15260282_00.csv"
LOG = PACK / "_chunks" / "logs" / "deck_15260282_00.txt"

FUNCTION_EN = {
    "a", "an", "the", "is", "be", "i", "you", "he", "she", "it", "we", "they",
    "my", "and", "or", "in", "on", "at", "to", "of", "for", "with", "from",
    "not", "his", "him", "her", "their", "them", "our", "us", "me", "am",
    "are", "was", "were", "been", "being", "this", "that", "these", "those",
    "as", "by", "into", "about", "than", "then", "so", "if", "but", "its",
    "your", "do", "does", "did", "will", "would", "can", "could", "may",
    "there", "here", "has", "had", "have", "don't", "dont", "let's", "lets",
    "all", "off", "done",
}

FUNCTION_RU = {
    "и", "а", "или", "не", "ни", "но", "да", "же", "ли", "бы", "то", "это",
    "этот", "эта", "эти", "этой", "этом", "эту", "этих", "этим", "этими",
    "этого", "этому", "я", "ты", "он", "она", "оно", "мы", "вы", "они",
    "мой", "моя", "мое", "мои", "моего", "моей", "моем", "моим", "мою",
    "твой", "твоя", "твое", "твои", "твою", "твоей", "ваш", "наш", "наша",
    "наше", "наши", "его", "ее", "их", "ему", "ей", "им", "ими", "меня",
    "мне", "тебя", "тебе", "нас", "нам", "вас", "вам", "себя", "себе",
    "собой", "свой", "своя", "свое", "свои", "свою", "своей", "своего",
    "своим", "в", "во", "на", "с", "со", "к", "ко", "у", "о", "об", "от",
    "до", "из", "за", "по", "под", "над", "при", "для", "без", "между",
    "через", "был", "была", "было", "были", "будет", "будут", "буду",
    "есть", "быть", "уже", "еще", "также", "тоже", "только", "вот", "ведь",
    "ну", "все", "всех", "всего", "всем", "здесь", "тут", "там", "давай",
    "как", "что", "чтобы", "когда", "если", "где", "чем", "кто",
    "них", "него", "нее", "ней", "ним",
}

allow_en = {
    line.strip().lower()
    for line in (PACK / "_vocab" / "allow_en_15260282.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_ru = {
    line.strip().replace("ё", "е").lower()
    for line in (PACK / "_vocab" / "allow_ru_15260282.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_en |= FUNCTION_EN
allow_ru |= FUNCTION_RU

# New lemmas introduced by corrections (taught on this card).
allow_ru |= {"азартный игрок", "свергнуть", "хабаровск", "привязать"}

# (en_lemma, en_ex, ru_lemma, ru_ex)
FIXED = [
    ("hanger", "The coat is on the hanger.", "вешалка", "Пальто на вешалке."),
    ("dogma", "His belief was dogma.", "догма", "Его убеждение было догмой."),
    ("rely", "I can rely on you.", "положиться", "Я могу положиться на вас."),
    ("circumference", "The circumference is large.", "окружность", "Окружность большая."),
    ("hoarsely", "He spoke hoarsely in the dark.", "хрипло", "Он хрипло говорил в темноте."),
    ("Bulgarian", "I love Bulgarian food.", "болгарский", "Я люблю болгарскую кухню."),
    ("collective farm worker", "The collective farm worker works in the field.", "колхозник", "Колхозник работает в поле."),
    ("carving", "I like this wood carving.", "резьба", "Мне нравится эта резьба по дереву."),
    ("concentration camp", "They visited a former concentration camp.", "концлагерь", "Они посетили бывший концлагерь."),
    ("to cough", "He tried not to cough loudly.", "кашлять", "Он старался не кашлять громко."),
    ("bottomless", "Her eyes are bottomless.", "бездонный", "Её глаза бездонные."),
    ("willow", "The willow stands by the river.", "ива", "Ива стоит у реки."),
    ("mistakenly", "He mistakenly took my book.", "ошибочно", "Он ошибочно взял мою книгу."),
    ("ark", "They will build an ark.", "ковчег", "Они построят ковчег."),
    ("soundlessly", "She walked soundlessly.", "беззвучно", "Она беззвучно шла."),
    ("sixtieth", "Today is the sixtieth day.", "шестидесятый", "Сегодня шестидесятый день."),
    ("blouse", "She will buy a blouse tomorrow.", "блузка", "Она купит блузку завтра."),
    ("to be amazed", "You will be amazed.", "обалдеть", "Ты обалдеешь."),
    ("to be fixed", "The rate will be fixed tomorrow.", "фиксироваться", "Ставка будет фиксироваться завтра."),
    ("shepherd dog", "The shepherd dog guards the sheep.", "овчарка", "Овчарка охраняет овцу."),
    ("continuity", "We need continuity of power.", "преемственность", "Нам нужна преемственность власти."),
    ("behavioral", "This is a behavioral problem.", "поведенческий", "Это поведенческая проблема."),
    ("sewerage", "The city has a sewerage system.", "канализация", "В городе есть канализационная система."),
    ("ethnos", "Each ethnos has a history.", "этнос", "У каждого этноса есть история."),
    ("gambler", "The gambler lost everything.", "азартный игрок", "Азартный игрок потерял всё."),
    ("alteration", "The dress needed an alteration.", "переделка", "Платью нужна была переделка."),
    ("mythical", "Dragons are mythical creatures.", "мифический", "Драконы - мифические существа."),
    ("oppressive", "The heat is oppressive today.", "тягостный", "Жара сегодня тягостная."),
    ("pastry", "I want a chocolate pastry.", "пирожное", "Я хочу шоколадное пирожное."),
    ("repent", "He will repent for his sins.", "каяться", "Он будет каяться в своих грехах."),
    ("vaccine", "The vaccine prevents many diseases.", "вакцина", "Вакцина предотвращает множество болезней."),
    ("pass-through", "This is a pass-through window.", "пропускной", "Это пропускное окно."),
    ("depart", "The train will soon depart.", "отбыть", "Поезд должен отбыть."),
    ("skeptically", "She looked at him skeptically.", "скептически", "Она скептически посмотрела на него."),
    ("manure", "There is manure on the field.", "навоз", "На поле есть навоз."),
    ("general education", "This is a general education school.", "общеобразовательный", "Это общеобразовательная школа."),
    ("unharmed", "The child is unharmed.", "невредимый", "Ребёнок невредим."),
    ("almighty", "God is almighty.", "всемогущий", "Бог всемогущий."),
    ("astrology", "She believes in astrology deeply.", "астрология", "Она глубоко верит в астрологию."),
    ("incoherent", "His explanation was completely incoherent.", "невнятный", "Его объяснение было полностью невнятным."),
    ("squint", "He will squint at the bright light.", "прищуриться", "Он прищурится от яркого света."),
    ("Mexican", "I love Mexican food.", "мексиканский", "Я люблю мексиканскую кухню."),
    ("renounce", "He will renounce his faith.", "отречься", "Он отречётся от своей веры."),
    ("trusting", "She was too trusting of strangers.", "доверчивый", "Она была слишком доверчивой к незнакомцам."),
    ("motherhood", "Motherhood changed her life.", "материнство", "Материнство изменило её жизнь."),
    ("tailor", "The tailor made my suit.", "портной", "Портной сшил мой костюм."),
    ("magnet", "The magnet holds the note.", "магнит", "Магнит держит записку."),
    ("to purchase", "They purchase water.", "закупать", "Они закупают воду."),
    ("dishonest", "He is a dishonest man.", "нечестный", "Он нечестный человек."),
    ("to pronounce", "He cannot pronounce her name.", "выговорить", "Он не может выговорить её имя."),
    ("originate", "Ideas often originate in unexpected places.", "зародиться", "Идеи часто зарождаются в неожиданных местах."),
    ("pearl", "She found a pearl.", "жемчужина", "Она нашла жемчужину."),
    ("forecasting", "Weather forecasting saves lives.", "прогнозирование", "Прогнозирование погоды спасает жизни."),
    ("saw", "He has a new saw.", "пила", "У него новая пила."),
    ("painter", "The painter has a masterpiece.", "живописец", "У живописца есть шедевр."),
    ("plum", "I want a fresh plum.", "слива", "Я хочу свежую сливу."),
    ("to have difficulty", "She will have difficulty with this.", "затрудняться", "Она затрудняется с этим."),
    ("Mason", "The Mason came to a secret meeting.", "масон", "Масон пришёл на секретную встречу."),
    ("decennial", "The town celebrates its decennial festival.", "десятилетний", "Город празднует свой десятилетний фестиваль."),
    ("hormonal", "She has hormonal changes now.", "гормональный", "У неё сейчас гормональные изменения."),
    ("telecommunication", "This is a telecommunication company.", "телекоммуникационный", "Это телекоммуникационная компания."),
    ("porcelain", "She has porcelain dolls.", "фарфоровый", "У неё фарфоровые куклы."),
    ("to delve", "She will delve into history.", "углубляться", "Она будет углубляться в историю."),
    ("overthrow", "They want to overthrow the government.", "свергнуть", "Они хотят свергнуть правительство."),
    ("vacuum cleaner", "I will buy a new vacuum cleaner.", "пылесос", "Я куплю новый пылесос."),
    ("scanner", "I will buy a new scanner.", "сканер", "Я куплю новый сканер."),
    ("willy-nilly", "He went into the army willy-nilly.", "поневоле", "Он поневоле пошёл в армию."),
    ("to consist of", "The team will consist of experts.", "состоять из", "Команда будет состоять из экспертов."),
    ("profitability", "The company's profitability is high this year.", "рентабельность", "Рентабельность компании в этом году высокая."),
    ("vulture", "A vulture is above the desert.", "гриф", "Гриф над пустыней."),
    ("secretariat", "The secretariat received all applications.", "секретариат", "Секретариат получил все заявления."),
    ("sprinkle", "They sprinkle the earth with snow.", "осыпать", "Они осыпают землю снегом."),
    ("anatomy", "She studies human anatomy at university.", "анатомия", "Она изучает анатомию человека в университете."),
    ("sleepless", "He spent a sleepless night.", "бессонный", "Он провёл бессонную ночь."),
    ("cherry", "I love cherry pie.", "вишня", "Я люблю пирог с вишней."),
    ("microchip", "This device has a microchip.", "микросхема", "В этом устройстве есть микросхема."),
    ("Tibetan", "She has a beautiful Tibetan dress.", "тибетский", "У неё красивое тибетское платье."),
    ("to be empty", "The house will be empty.", "пустовать", "Дом будет пустовать."),
    ("carved", "The door has carved patterns.", "резной", "На двери резные узоры."),
    ("sinus", "My sinus hurts.", "пазуха", "У меня болит пазуха."),
    ("prop", "This is a stage prop.", "реквизит", "Это реквизит для сцены."),
    ("warm up", "The fire will warm up the room.", "согреть", "Огонь согреет комнату."),
    ("asthma", "She has severe asthma.", "астма", "У неё тяжёлая астма."),
    ("indecision", "Indecision is his problem.", "нерешительность", "Нерешительность - его проблема."),
    ("boarding school", "She studies at a boarding school.", "интернат", "Она учится в интернате."),
    ("floppy disk", "I found an old floppy disk.", "дискета", "Я нашёл старую дискету."),
    ("autopsy", "The autopsy showed the cause of death.", "вскрытие", "Вскрытие показало причину смерти."),
    ("impatient", "He is impatient.", "нетерпеливый", "Он нетерпеливый."),
    ("heredity", "Heredity influences health.", "наследственность", "Наследственность влияет на здоровье."),
    ("Khabarovsk", "I visited Khabarovsk last summer.", "Хабаровск", "Я посетил Хабаровск прошлым летом."),
    ("wild game", "They hunted wild game for food.", "дичь", "Они охотились на дичь ради еды."),
    ("whim", "She bought the dress on a whim.", "прихоть", "Она купила платье по прихоти."),
    ("reader's", "This is a reader's book.", "читательский", "Это читательская книга."),
    ("correlate", "Prices correlate with demand levels.", "соотноситься", "Цены соотносятся с уровнем спроса."),
    ("dash", "He will dash to the door.", "метнуться", "Он метнётся к двери."),
    ("unnatural", "His smile seemed unnatural.", "неестественный", "Его улыбка казалась неестественной."),
    ("rusk", "The rusk is on the table.", "сухарь", "Сухарь на столе."),
    ("recognition", "This is face recognition.", "распознавание", "Это распознавание лиц."),
    ("dodge", "He managed to dodge the question.", "уклониться", "Он сумел уклониться от вопроса."),
    ("tie up", "Let's tie up the boat.", "привязать", "Давайте привяжем лодку."),
]


IRREGULAR_EN = {
    "made": "make",
    "met": "meet",
    "saw": "see",
    "got": "get",
    "gave": "give",
    "took": "take",
    "came": "come",
    "went": "go",
    "ate": "eat",
    "spoke": "speak",
    "broke": "break",
    "bought": "buy",
    "built": "build",
    "found": "find",
    "left": "leave",
    "held": "hold",
    "told": "tell",
    "said": "say",
    "heard": "hear",
    "paid": "pay",
    "sold": "sell",
    "lost": "lose",
    "spent": "spend",
    "stood": "stand",
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
    "ем", "ах", "ях", "ам", "ям", "ов", "ев", "ей", "ую", "юю", "ая", "яя",
    "ое", "ее", "ые", "ие", "ый", "ий", "ой", "а", "я", "у", "ю", "е", "и",
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


IRREGULAR_RU = {
    "может": "мочь",
    "могу": "мочь",
    "можем": "мочь",
    "хочу": "хотеть",
    "хочет": "хотеть",
    "хотим": "хотеть",
    "вижу": "видеть",
    "видишь": "видеть",
    "видит": "видеть",
    "знаю": "знать",
    "живу": "жить",
    "живем": "жить",
    "живет": "жить",
    "еду": "еда",
    "еды": "еда",
    "овец": "овца",
    "овцу": "овца",
    "шла": "идти",
    "шел": "идти",
    "шёл": "идти",
    "шли": "идти",
}


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


def make_card(en_lemma: str, en_ex: str, ru_lemma: str, ru_ex: str) -> dict:
    return card_write_payload(
        {
            "qMdPrompt": "Translate:",
            "qMdBody": en_lemma,
            "qMdClarifier": "",
            "qMdFootnote": en_ex,
            "aMdPrompt": "",
            "aMdBody": ru_lemma,
            "aMdClarifier": "",
            "aMdFootnote": ru_ex,
        }
    )


def target_in_example(lemma: str, example: str) -> bool:
    text = example.replace("ё", "е").lower()
    parts = [p.strip() for p in re.split(r"\s+", lemma.replace("ё", "е").lower()) if p.strip()]
    keys = [p for p in parts if p not in {"to", "be", "the", "a", "an"}] or parts
    for key in keys:
        stem = key[:4] if len(key) >= 4 else key
        if stem and stem in text.replace(" ", ""):
            return True
        if key in text:
            return True
    return False


def write_csv(path: Path, cards: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh, lineterminator="\n")
        writer.writerow(["Question", "Answer"])
        for card in cards:
            payload = card_write_payload(card)
            writer.writerow([payload["question"], payload["answer"]])


def main() -> None:
    orig = cards_from_path(SRC)
    if len(orig) != 100:
        raise SystemExit(f"expected 100 source cards, got {len(orig)}")
    if len(FIXED) != 100:
        raise SystemExit(f"expected 100 fixed rows, got {len(FIXED)}")

    cards = []
    changed = 0
    leftover: list[str] = []
    missing_target: list[str] = []
    for i, ((en_lemma, en_ex, ru_lemma, ru_ex), old) in enumerate(zip(FIXED, orig), start=1):
        if old.get("qMdBody") != en_lemma:
            raise SystemExit(f"order mismatch at {i}: {old.get('qMdBody')!r} vs {en_lemma!r}")
        card = make_card(en_lemma, en_ex, ru_lemma, ru_ex)
        cards.append(card)
        if not cards_match(old, card):
            changed += 1
        lemma_bits = set(re.findall(r"[A-Za-z']+", en_lemma.lower()))
        for tok in re.findall(r"[A-Za-z']+", en_ex):
            if tok.lower() in lemma_bits:
                continue
            if not _en_ok(tok):
                leftover.append(f"{i} EN {tok} :: {en_ex}")
        ru_bits = set(re.findall(r"[А-Яа-яЁё]+", ru_lemma.lower().replace("ё", "е")))
        for tok in re.findall(r"[А-Яа-яЁё]+", ru_ex):
            if tok.replace("ё", "е").lower() in ru_bits:
                continue
            if not _ru_ok(tok):
                leftover.append(f"{i} RU {tok} :: {ru_ex}")
        if not target_in_example(en_lemma, en_ex):
            missing_target.append(f"{i} EN {en_lemma} :: {en_ex}")
        if not target_in_example(ru_lemma, ru_ex):
            missing_target.append(f"{i} RU {ru_lemma} :: {ru_ex}")

    write_csv(OUT, cards)
    got = cards_from_path(OUT)
    if len(got) != 100:
        raise SystemExit(f"cards_from_path returned {len(got)}")
    LOG.parent.mkdir(parents=True, exist_ok=True)
    LOG.write_text(f"{changed}\n", encoding="utf-8")
    print(f"wrote {OUT}")
    print(f"cards_from_path={len(got)} changed={changed}")
    if leftover:
        print("LEFTOVER:")
        print("\n".join(leftover))
    if missing_target:
        print("MISSING TARGET:")
        print("\n".join(missing_target))


if __name__ == "__main__":
    main()
