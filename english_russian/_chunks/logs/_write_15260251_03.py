#!/usr/bin/env python3
"""Rewrite english_russian deck_15260251_03 (cards 301-400)."""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REPO = ROOT.parent
sys.path.insert(0, str(REPO))

from brainscape.cards import (  # noqa: E402
    card_write_payload,
    cards_from_path,
    cards_match,
)

SRC = ROOT / "_chunks" / "deck_15260251_03.csv"
OUT = ROOT / "_chunks" / "fixed" / "deck_15260251_03.csv"
LOG = ROOT / "_chunks" / "logs" / "deck_15260251_03.txt"
ALLOW_EN = ROOT / "_vocab" / "allow_en_15260251.txt"
ALLOW_RU = ROOT / "_vocab" / "allow_ru_15260251.txt"

FUNC_EN = {
    "a", "an", "the", "is", "be", "i", "you", "he", "she", "it", "we", "they",
    "my", "and", "or", "in", "on", "at", "to", "of", "for", "with", "from", "not",
}

# Inflections of the tiny function-word set (be/I/he/she/we/they).
FUNC_EN_EXTRA = {
    "am", "are", "was", "were", "been", "being",
    "me", "him", "us", "them", "his",
}

# Overrides: 0-based index -> (ru_lemma or None, en_ex, ru_ex)
# None lemma means keep the original Russian lemma.
FIX: dict[int, tuple[str | None, str, str]] = {
    2: (None, "I bought domestic products.", "Я купил отечественные продукты."),
    3: (None, "The owner is in the house.", "Владелец в доме."),
    4: (None, "The equipment is new.", "Оборудование новое."),
    5: (None, "This is big trouble.", "Это большая беда."),
    6: (None, "I report the news.", "Я сообщаю новость."),
    7: (None, "The house is ahead.", "Дом впереди."),
    8: (None, "I heard a scream.", "Я услышал крик."),
    9: (None, "My uncle loves fish.", "Мой дядя любит рыбу."),
    10: (None, "This is an important economic indicator.", "Это важный экономический показатель."),
    11: (None, "He develops fast.", "Он развивается быстро."),
    12: (None, "The formation of the group is important.", "Формирование группы важно."),
    13: (None, "I see the signal.", "Я вижу сигнал."),
    14: (None, "They will appoint a new director soon.", "Они скоро назначат нового директора."),
    15: (None, "Light seemed to emanate from the house.", "Казалось, свет исходил от дома."),
    16: (None, "The dog is on the grass.", "Собака на траве."),
    17: (None, "The treatment was effective.", "Лечение было эффективным."),
    18: (None, "The tools are in the box.", "Инструменты в ящике."),
    19: (None, "The institution opens in the morning.", "Учреждение открывается утром."),
    20: (None, "The old castle stood on the mountain.", "Старый замок стоял на горе."),
    21: (None, "I feel the impact.", "Я чувствую воздействие."),
    23: (None, "He smiled slightly.", "Он слегка улыбнулся."),
    24: (None, "He looked into the abyss.", "Он смотрел в пропасть."),
    25: (None, "Act accordingly.", "Действуйте соответственно."),
    27: (None, "The distance is large.", "Расстояние большое."),
    28: (None, "I see evil in this.", "Я вижу зло в этом."),
    29: (None, "The noise on the street was strong.", "Шум на улице был сильным."),
    30: (None, "The fact will prove it.", "Факт докажет это."),
    31: (None, "She was calm.", "Она была спокойной."),
    32: (None, "Write the digit.", "Напишите цифру."),
    33: (None, "The opinion formed.", "Мнение сложилось."),
    34: (None, "We walked along the pier.", "Мы шли по молу."),
    35: (None, "The file is on the disk.", "Файл лежит на диске."),
    36: (None, "The place is very convenient.", "Место очень удобное."),
    37: (None, "Everything can change.", "Всё может меняться."),
    38: (None, "We want to evaluate the situation.", "Мы хотим оценить ситуацию."),
    40: (None, "I feel pain in my neck.", "Я чувствую боль в шее."),
    42: (None, "This is a good chance.", "Это хороший шанс."),
    43: (None, "She has a small booklet.", "У неё есть маленькая книжка."),
    44: (None, "The player is on the field.", "Игрок на поле."),
    45: (None, "I need to prepare for work.", "Мне нужно готовиться к работе."),
    46: (None, "Reading is important.", "Чтение важно."),
    47: (None, "The old house has a staircase.", "В старом доме есть лестница."),
    48: (None, "We are in the boat.", "Мы в лодке."),
    50: (None, "She loves to collect books.", "Она любит собирать книги."),
    51: (None, "The pressure is high.", "Давление высокое."),
    52: (None, "He literally said that.", "Он буквально сказал это."),
    53: (None, "The consumer wants a new product.", "Потребитель хочет новый продукт."),
    54: (None, "This murder is a crime.", "Это убийство — преступление."),
    56: (None, "The movie will end soon.", "Фильм скоро закончится."),
    57: (None, "I want a piece of bread.", "Я хочу кусок хлеба."),
    58: (None, "Our strategy led to victory.", "Наша стратегия привела к победе."),
    59: (None, "He has dignity.", "У него есть достоинство."),
    60: (None, "This is a series of events.", "Это серия событий."),
    61: (None, "She chose the upper floor.", "Она выбрала верхний этаж."),
    62: (None, "They want to found a new school.", "Они хотят основать новую школу."),
    63: (None, "Follow the procedure.", "Следуйте процедуре."),
    64: (None, "I work exclusively at home.", "Я работаю исключительно дома."),
    65: (None, "Please consider this question.", "Пожалуйста, рассмотрите этот вопрос."),
    66: (None, "The army headquarters is in the city.", "Штаб армии в городе."),
    68: ("извиниться", "I want to apologize.", "Я хочу извиниться."),
    70: (None, "The baby smiled.", "Малыш улыбнулся."),
    71: (None, "I love this food.", "Я люблю эту еду."),
    72: ("ополчение", "The militia is in the city.", "Ополчение в городе."),
    73: (None, "Her expectation was high.", "Её ожидание было высоким."),
    74: (None, "I believe in the Lord.", "Я верю в господа."),
    75: (None, "I like philosophy.", "Мне нравится философия."),
    76: (None, "I heard laughter.", "Я услышал смех."),
    78: (None, "Numerous stars are in the night sky.", "Многочисленные звёзды на ночном небе."),
    79: (None, "This is a vital question.", "Это жизненный вопрос."),
    80: (None, "This is a narrow street.", "Это узкая улица."),
    82: (None, "This is an old block.", "Это старый блок."),
    83: (None, "They will arrive tomorrow.", "Они прибудут завтра."),
    85: (None, "The driver is in the car.", "Водитель в машине."),
    86: (None, "He walked from there quickly.", "Он быстро ушёл оттуда."),
    87: (None, "The pain is very sharp.", "Боль очень острая."),
    88: (None, "The bridge is on the river.", "Мост на реке."),
    89: (None, "I want a trip in the summer.", "Я хочу поездку летом."),
    90: (None, "I love the silence.", "Я люблю тишину."),
    91: (None, "His hearing is good.", "Его слух хороший."),
    92: (None, "The buyer made an offer.", "Покупатель сделал предложение."),
    95: (None, "I will prepare a report.", "Я подготовлю доклад."),
    96: (None, "The tank is in the city.", "Танк в городе."),
    97: (None, "My salary is good.", "Моя зарплата хорошая."),
    98: ("обратиться", "We need to address this question.", "Нам нужно обратиться к этому вопросу."),
    99: (None, "She has a relative in the city.", "У неё есть родственник в городе."),
}


def load_lemmas(path: Path) -> set[str]:
    return {line.strip().lower() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()}


def en_tokens(text: str) -> list[str]:
    return [t for t in re.findall(r"[a-zA-Z']+", text.lower()) if t]


def ru_tokens(text: str) -> list[str]:
    return [t for t in re.findall(r"[а-яёА-ЯЁ]+", text.lower()) if t]


def stem_en(word: str) -> list[str]:
    out = {word}
    for suf in ("'s", "s'", "ies", "es", "ed", "ing", "ly", "er", "est", "s"):
        if word.endswith(suf) and len(word) > len(suf) + 2:
            out.add(word[: -len(suf)])
            if suf == "ies":
                out.add(word[:-3] + "y")
            if suf == "ed" and word.endswith("ied"):
                out.add(word[:-3] + "y")
            if suf == "ing" and word.endswith("ying"):
                out.add(word[:-3])
    if word.endswith("ied") and len(word) > 4:
        out.add(word[:-3] + "y")
    return list(out)


def en_ok(word: str, allow: set[str], extra: set[str]) -> bool:
    if word in FUNC_EN or word in FUNC_EN_EXTRA or word in allow or word in extra:
        return True
    for form in stem_en(word):
        if form in allow or form in extra or form in FUNC_EN:
            return True
        if f"to {form}" in allow:
            return True
    # multiword lemmas containing this token
    for lemma in allow:
        parts = lemma.replace("-", " ").split()
        if word in parts or any(word == p or word in stem_en(p) for p in parts if p not in {"to", "the", "a", "an"}):
            return True
    return False


def ru_ok(word: str, allow: set[str], extra: set[str]) -> bool:
    if word in allow or word in extra:
        return True
    for lemma in allow | extra:
        if len(lemma) < 3:
            continue
        stem = lemma[: max(3, len(lemma) - 2)]
        if word.startswith(stem) or lemma.startswith(word[: max(3, len(word) - 2)]):
            return True
    return False


def main() -> None:
    allow_en = load_lemmas(ALLOW_EN)
    allow_ru = load_lemmas(ALLOW_RU)
    originals = cards_from_path(SRC)
    if len(originals) != 100:
        raise SystemExit(f"expected 100 source cards, got {len(originals)}")

    out_cards = []
    leftover: list[str] = []
    for i, card in enumerate(originals):
        new = {
            "qMdPrompt": "Translate:",
            "qMdBody": card["qMdBody"],
            "qMdClarifier": "",
            "qMdFootnote": card["qMdFootnote"],
            "aMdPrompt": "",
            "aMdBody": card["aMdBody"],
            "aMdClarifier": "",
            "aMdFootnote": card["aMdFootnote"],
        }
        extra_en: set[str] = set()
        extra_ru: set[str] = set()
        if i in FIX:
            ru_lemma, en_ex, ru_ex = FIX[i]
            if ru_lemma:
                new["aMdBody"] = ru_lemma
            new["qMdFootnote"] = en_ex
            new["aMdFootnote"] = ru_ex
        gloss = (new["qMdBody"] or "").lower()
        extra_en.update(en_tokens(gloss))
        extra_en.update(p for p in gloss.replace("-", " ").split() if p)
        extra_ru.update(ru_tokens(new["aMdBody"] or ""))
        payload = card_write_payload(new)
        out_cards.append(payload)

        for tok in en_tokens(new["qMdFootnote"] or ""):
            if not en_ok(tok, allow_en, extra_en):
                leftover.append(f"EN {i+1} {new['qMdBody']!r}: {tok}")
        for tok in ru_tokens(new["aMdFootnote"] or ""):
            if not ru_ok(tok, allow_ru, extra_ru):
                leftover.append(f"RU {i+1} {new['aMdBody']!r}: {tok}")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh, lineterminator="\n")
        writer.writerow(["Question", "Answer"])
        for payload in out_cards:
            writer.writerow([payload["question"], payload["answer"]])

    written = cards_from_path(OUT)
    if len(written) != 100:
        raise SystemExit(f"cards_from_path returned {len(written)}")

    changed = sum(1 for a, b in zip(originals, written) if not cards_match(a, b))
    LOG.parent.mkdir(parents=True, exist_ok=True)
    LOG.write_text(f"{changed}\n", encoding="utf-8")

    print(f"wrote {len(written)} cards, changed {changed}")
    print(f"out {OUT}")
    if leftover:
        print("LEFTOVER:")
        for line in leftover:
            print(" ", line)
    else:
        print("vocab check clean")


if __name__ == "__main__":
    main()
