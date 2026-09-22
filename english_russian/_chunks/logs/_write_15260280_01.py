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

SRC = PACK / "_chunks" / "deck_15260280_01.csv"
OUT = PACK / "_chunks" / "fixed" / "deck_15260280_01.csv"
LOG = PACK / "_chunks" / "logs" / "deck_15260280_01.txt"

FUNCTION_EN = {
    "a", "an", "the", "is", "be", "i", "you", "he", "she", "it", "we", "they",
    "my", "and", "or", "in", "on", "at", "to", "of", "for", "with", "from",
    "not", "his", "him", "her", "their", "them", "our", "us", "me", "am",
    "are", "was", "were", "been", "being", "this", "that", "these", "those",
    "as", "by", "into", "about", "than", "then", "so", "if", "but", "its",
    "your", "do", "does", "did", "will", "would", "can", "could", "may",
    "there", "here", "has", "had", "have", "don't", "dont", "let's", "lets",
    "all", "off", "done", "himself", "herself", "myself", "itself", "themselves",
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
    for line in (PACK / "_vocab" / "allow_en_15260280.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_ru = {
    line.strip().replace("ё", "е").lower()
    for line in (PACK / "_vocab" / "allow_ru_15260280.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_en |= FUNCTION_EN
allow_ru |= FUNCTION_RU

# New lemmas introduced by corrections (taught on this card).
allow_ru |= {"краснодар", "тюмень", "смоленск"}

# (en_lemma, en_ex, ru_lemma, ru_ex)
FIXED = [
    ("clip", "I watched a new clip.", "клип", "Я посмотрел новый клип."),
    ("to death", "He was scared to death.", "насмерть", "Он был напуган насмерть."),
    ("astronomer", "The astronomer looks at a star.", "астроном", "Астроном смотрит на звезду."),
    ("to pat", "She likes to pat the dog.", "похлопать", "Она любит похлопать собаку."),
    ("blizzard", "The blizzard covered the road.", "метель", "Метель покрыла дорогу."),
    ("axiom", "This is an axiom.", "аксиома", "Это аксиома."),
    ("get enough sleep", "I must get enough sleep.", "выспаться", "Мне нужно выспаться."),
    ("Buddhism", "Buddhism is an old religion.", "буддизм", "Буддизм — старая религия."),
    ("salvific", "This is a salvific force.", "спасительный", "Это спасительная сила."),
    ("technical school", "He graduated from a technical school.", "техникум", "Он окончил техникум."),
    ("Danish", "This is a Danish city.", "датский", "Это датский город."),
    ("to turn away", "She began to turn away.", "отворачиваться", "Она начала отворачиваться."),
    ("spout", "The kettle's spout is hot.", "носик", "Носик чайника горячий."),
    ("Norwegian", "This is a Norwegian city.", "норвежский", "Это норвежский город."),
    ("to glance at", "He glanced at the room.", "окинуть", "Он окинул взглядом комнату."),
    ("colorful", "The picture is colorful.", "красочный", "Картина красочная."),
    ("feudal", "It was a feudal system.", "феодальный", "Это была феодальная система."),
    ("municipality", "The municipality has a park.", "муниципалитет", "У муниципалитета есть парк."),
    ("forgery", "This is a forgery.", "подделка", "Это подделка."),
    ("fat man", "The fat man laughed.", "толстяк", "Толстяк смеялся."),
    ("manipulate", "They manipulate him.", "манипулировать", "Они манипулируют им."),
    ("predatory", "It is a predatory animal.", "хищный", "Это хищное животное."),
    ("unintentionally", "He unintentionally broke the vase.", "нечаянно", "Он нечаянно разбил вазу."),
    ("multiple", "He has multiple wounds.", "множественный", "У него множественные раны."),
    ("Krasnodar", "I live in Krasnodar.", "Краснодар", "Я живу в Краснодаре."),
    ("procession", "I see a procession.", "шествие", "Я вижу шествие."),
    ("conventionality", "This is only a conventionality.", "условность", "Это только условность."),
    ("dying", "The dying man whispered his wish.", "умирающий", "Умирающий человек прошептал своё желание."),
    ("astronomical", "The price is astronomical.", "астрономический", "Цена астрономическая."),
    ("to be provided for", "This is provided for in the law.", "предусматриваться", "Это предусматривается в законе."),
    ("shoot down", "They shot down the bird.", "подбить", "Они подбили птицу."),
    ("repentance", "He came to repentance.", "покаяние", "Он пришёл к покаянию."),
    ("healing", "He needs healing.", "исцеление", "Ему нужно исцеление."),
    ("possessed", "She seemed possessed by a strange energy.", "одержимый", "Она казалась одержимой странной энергией."),
    ("prisoner of war", "He became a prisoner of war.", "военнопленный", "Он стал военнопленным."),
    ("evacuate", "We must evacuate the building now.", "эвакуировать", "Мы должны сейчас эвакуировать здание."),
    ("daring", "He is a daring driver.", "лихой", "Он лихой водитель."),
    ("commerce", "He works in commerce.", "коммерция", "Он работает в коммерции."),
    ("alcoholism", "Alcoholism is a problem.", "алкоголизм", "Алкоголизм — это проблема."),
    ("tight", "The knot is tight.", "тугой", "Узел тугой."),
    ("crowbar", "He opened the box with a crowbar.", "лом", "Он открыл ящик ломом."),
    ("peasantry", "The peasantry was poor.", "крестьянство", "Крестьянство было бедным."),
    ("bunks", "The soldiers have bunks.", "нары", "У солдат есть нары."),
    ("scarf", "She has a new scarf.", "шарф", "У неё новый шарф."),
    ("dean", "The dean welcomed new students.", "декан", "Декан приветствовал новых студентов."),
    ("to wave off", "He waved off my question.", "отмахнуться", "Он отмахнулся от моего вопроса."),
    ("daddy", "Daddy bought me a new bicycle.", "папочка", "Папочка купил мне новый велосипед."),
    ("small room", "She rented a small room.", "комнатка", "Она сняла комнатку."),
    ("diplomacy", "We need diplomacy.", "дипломатия", "Нам нужна дипломатия."),
    ("hinder", "Heavy rain can hinder your plan.", "затруднять", "Сильный дождь может затруднить ваш план."),
    ("washing", "The washing machine does not work.", "стиральный", "Стиральная машина не работает."),
    ("extraction", "The extraction of the tooth was successful.", "извлечение", "Извлечение зуба было успешным."),
    ("fiber", "Cotton fiber is strong.", "волокно", "Хлопковое волокно сильное."),
    ("political scientist", "The political scientist analyzed the election.", "политолог", "Политолог анализировал выборы."),
    ("cardboard", "I bought a cardboard box.", "картонный", "Я купил картонный ящик."),
    ("Byzantine", "The Byzantine Empire was great.", "византийский", "Византийская империя была великой."),
    ("playwright", "The playwright wrote a book.", "драматург", "Драматург написал книгу."),
    ("vent", "Open the vent for fresh air.", "форточка", "Открой форточку для свежего воздуха."),
    ("insufficiency", "There is an insufficiency of water.", "недостаточность", "Есть недостаточность воды."),
    ("flood", "The river will flood the town soon.", "затопить", "Река скоро затопит город."),
    ("migrant", "The migrant found work.", "мигрант", "Мигрант нашёл работу."),
    ("leash", "Keep the dog on a leash.", "поводок", "Держите собаку на поводке."),
    ("buttock", "His buttock hurts.", "ягодица", "У него болит ягодица."),
    ("subsystem", "The engine is a subsystem.", "подсистема", "Двигатель — это подсистема."),
    ("jar", "I put water in a jar.", "баночка", "Я налил воду в баночку."),
    ("Tyumen", "I live in Tyumen.", "Тюмень", "Я живу в Тюмени."),
    ("Politburo", "The Politburo decided the policy.", "политбюро", "Политбюро приняло решение о политике."),
    ("certification", "I received my certification yesterday.", "сертификация", "Я получил свою сертификацию вчера."),
    ("informatics", "I study informatics at the university.", "информатика", "Я изучаю информатику в университете."),
    ("patron", "He became a patron of the arts.", "покровитель", "Он стал покровителем искусств."),
    ("preacher", "The preacher spoke to the people.", "проповедник", "Проповедник говорил с народом."),
    ("principality", "This is a small principality.", "княжество", "Это маленькое княжество."),
    ("baton", "The officer raised his baton.", "дубинка", "Офицер поднял свою дубинку."),
    ("finishing", "The finishing on the table is good.", "отделка", "Отделка стола хорошая."),
    ("lace", "I want a new lace.", "шнурок", "Я хочу новый шнурок."),
    ("roll", "Let's roll the stone.", "катить", "Давайте катить камень."),
    ("streamlet", "A streamlet ran from the hill.", "струйка", "Струйка бежала с холма."),
    ("to drag on", "They drag on the meeting.", "затягивать", "Они затягивают встречу."),
    ("to pull oneself together", "He pulled himself together.", "взять себя в руки", "Он взял себя в руки."),
    ("pi", "I know the number pi.", "пи", "Я знаю число пи."),
    ("shut up", "Shut up and listen!", "заткнуться", "Заткнись и слушай!"),
    ("manifesto", "He published his manifesto.", "манифест", "Он опубликовал свой манифест."),
    ("intercourse", "They had intercourse.", "сношение", "У них было сношение."),
    ("merciful", "The king was merciful.", "милостивый", "Царь был милостив."),
    ("to loom", "A war began to loom.", "намечаться", "Начала намечаться война."),
    ("hiss", "The snake began to hiss loudly.", "шипеть", "Змея начала громко шипеть."),
    ("underage", "The boy is underage.", "малолетний", "Мальчик малолетний."),
    ("deputy's", "This is the deputy's plan.", "депутатский", "Это депутатский план."),
    ("petal", "A flower petal fell.", "лепесток", "Лепесток цветка упал."),
    ("communicative", "She is very communicative.", "коммуникативный", "Она очень коммуникативная."),
    ("illegally", "He lived there illegally.", "незаконно", "Он жил там незаконно."),
    ("Sagittarius", "She is a Sagittarius.", "стрелец", "Она Стрелец."),
    ("Smolensk", "We live in Smolensk.", "Смоленск", "Мы живём в Смоленске."),
    ("five-year", "This is a five-year plan.", "пятилетний", "Это пятилетний план."),
    ("fellow traveler", "He found a fellow traveler.", "попутчик", "Он нашёл попутчика."),
    ("turn inside out", "She turned the jacket inside out.", "вывернуть", "Она вывернула куртку."),
    ("brazenly", "He brazenly took the book.", "нагло", "Он нагло взял книгу."),
    ("refinement", "The text needs refinement.", "доработка", "Текст требует доработки."),
    ("enthusiast", "He is a true enthusiast.", "энтузиаст", "Он настоящий энтузиаст."),
    ("devilishly", "It is devilishly cold.", "чертовски", "Это чертовски холодно."),
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
    "shot": "shoot",
    "slept": "sleep",
    "bought": "buy",
    "found": "find",
    "put": "put",
    "ran": "run",
    "fell": "fall",
    "hurt": "hurt",
    "kept": "keep",
    "wrote": "write",
    "knew": "know",
    "began": "begin",
    "became": "become",
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
    "живём": "жить",
    "живёт": "жить",
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
