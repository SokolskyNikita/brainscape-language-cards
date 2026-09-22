#!/usr/bin/env python3
"""Rewrite english_russian deck_15260256_03 (cards 301-400)."""

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

SRC = ROOT / "_chunks" / "deck_15260256_03.csv"
OUT = ROOT / "_chunks" / "fixed" / "deck_15260256_03.csv"
LOG = ROOT / "_chunks" / "logs" / "deck_15260256_03.txt"
ALLOW_EN = ROOT / "_vocab" / "allow_en_15260256.txt"
ALLOW_RU = ROOT / "_vocab" / "allow_ru_15260256.txt"

FUNC_EN = {
    "a", "an", "the", "is", "be", "i", "you", "he", "she", "it", "we", "they",
    "my", "and", "or", "in", "on", "at", "to", "of", "for", "with", "from", "not",
}
FUNC_EN_EXTRA = {
    "am", "are", "was", "were", "been", "being",
    "me", "him", "us", "them", "his",
}

# Keep original English glosses. Russian lemma kept unless noted.
# (ru_lemma, en_example, ru_example)
FIXED: list[tuple[str, str, str]] = [
    ("миссия", "This is an important mission.", "Это важная миссия."),
    ("тонна", "We need a ton of water.", "Нам нужна тонна воды."),
    ("горизонт", "The sun is on the horizon.", "Солнце на горизонте."),
    ("уверить", "I want to assure you.", "Я хочу уверить вас."),
    ("сахар", "I need more sugar.", "Мне нужно больше сахара."),
    ("эволюция", "This is about evolution.", "Это об эволюции."),
    ("мебель", "We have new furniture.", "У нас новая мебель."),
    ("типичный", "This is a typical day.", "Это типичный день."),
    ("пустыня", "The desert is large.", "Пустыня большая."),
    ("оригинальный", "This idea is original.", "Эта идея оригинальная."),
    ("обида", "She feels offense.", "Она чувствует обиду."),
    ("сочетание", "This is a good combination.", "Это хорошее сочетание."),
    ("вооружение", "The country needs new armament.", "Стране нужно новое вооружение."),
    ("чашка", "I need a cup.", "Мне нужна чашка."),
    ("прокуратура", "He works in the prosecutor's office.", "Он работает в прокуратуре."),
    ("съезд", "The congress is tomorrow.", "Съезд завтра."),
    ("приобретение", "This is a new acquisition.", "Это новое приобретение."),
    ("график", "Check the schedule.", "Проверьте график."),
    ("философ", "He is a philosopher.", "Он философ."),
    ("сдавать", "I hand in the work.", "Я сдаю работу."),
    ("племя", "The tribe is large.", "Племя большое."),
    ("ветка", "A bird sits on the branch.", "Птица сидит на ветке."),
    ("сталкиваться", "I do not want to encounter him.", "Я не хочу сталкиваться с ним."),
    ("гнев", "I see his anger.", "Я вижу его гнев."),
    ("почтовый", "Check your postal address.", "Проверьте ваш почтовый адрес."),
    ("слабость", "This is my weakness.", "Это моя слабость."),
    ("целиком", "He read the book entirely.", "Он прочитал книгу целиком."),
    ("консультант", "He is a consultant.", "Он консультант."),
    ("крепость", "The fortress is old.", "Крепость старая."),
    ("разделять", "We need to divide the work.", "Нам нужно разделять работу."),
    ("разбираться", "He wants to understand cars.", "Он хочет разбираться в машинах."),
    ("правление", "His governance was good.", "Его правление было хорошим."),
    ("сладкий", "The tea is sweet.", "Чай сладкий."),
    ("ствол", "The tree trunk is thick.", "Ствол дерева толстый."),
    ("завершить", "I need to complete the work.", "Мне нужно завершить работу."),
    ("дождаться", "I need to wait for him.", "Мне нужно дождаться его."),
    ("независимость", "They want independence.", "Они хотят независимости."),
    ("недавний", "I read a recent article.", "Я прочитал недавнюю статью."),
    ("долина", "The valley is large.", "Долина большая."),
    ("довести", "He can bring the work to an end.", "Он может довести работу до конца."),
    ("каталог", "I have a furniture catalog.", "У меня есть каталог мебели."),
    ("забор", "There is a fence around the house.", "Вокруг дома есть забор."),
    ("фото", "I have a new photo.", "У меня есть новое фото."),
    ("суровый", "The winter was severe.", "Зима была суровой."),
    ("невероятный", "The news is incredible.", "Новость невероятная."),
    ("благодарность", "I want to show my gratitude.", "Я хочу показать свою благодарность."),
    ("мгновенно", "He instantly knows this.", "Он мгновенно знает это."),
    ("преодолеть", "She will overcome this.", "Она преодолеет это."),
    ("пугать", "Do not scare me.", "Не пугай меня."),
    ("целовать", "She likes to kiss him.", "Она любит целовать его."),
    ("испугаться", "I do not want to get scared.", "Я не хочу испугаться."),
    ("отчаяние", "I see her despair.", "Я вижу её отчаяние."),
    ("некогда", "I have no time.", "Мне некогда."),
    ("награда", "This is her award.", "Это её награда."),
    ("обыкновенный", "It was an ordinary day.", "Это был обыкновенный день."),
    ("добыча", "The animal sees the prey.", "Животное видит добычу."),
    ("своеобразный", "His taste is peculiar.", "Его вкус своеобразный."),
    ("противный", "This smell is disgusting.", "Этот запах противный."),
    ("царство", "The kingdom is large.", "Царство большое."),
    ("ярко", "The fire burns brightly.", "Огонь горит ярко."),
    ("революционный", "His idea is revolutionary.", "Его идея революционная."),
    ("течь", "The river can flow.", "Река может течь."),
    ("молодец", "Well done, my friend.", "Молодец, мой друг."),
    ("изменять", "He can cheat on her.", "Он может изменять ей."),
    ("преследовать", "They want to pursue him.", "Они хотят преследовать его."),
    ("корпоративный", "This is corporate culture.", "Это корпоративная культура."),
    ("взаимный", "Our respect is mutual.", "Наше уважение взаимное."),
    ("государь", "The sovereign is in the city.", "Государь в городе."),
    ("легенда", "He is a legend.", "Он легенда."),
    ("оппозиция", "The opposition is strong.", "Оппозиция сильная."),
    ("установление", "The establishment of peace is important.", "Установление мира важно."),
    ("посредством", "He can speak by means of a letter.", "Он может говорить посредством письма."),
    ("вплоть", "He worked up to the end.", "Он работал вплоть до конца."),
    ("орать", "He wants to yell.", "Он хочет орать."),
    ("демонстрировать", "She can demonstrate her work.", "Она может демонстрировать свою работу."),
    ("цифровой", "This is a digital photo.", "Это цифровое фото."),
    ("предположение", "His assumption is bad.", "Его предположение плохое."),
    ("тарелка", "The plate is on the table.", "Тарелка на столе."),
    ("хранение", "We need a place for storage.", "Нам нужно место для хранения."),
    ("благородный", "He is a noble man.", "Он благородный человек."),
    ("грозить", "He wants to threaten me.", "Он хочет грозить мне."),
    ("торчать", "The key sticks out.", "Ключ торчит."),
    ("издательство", "The publishing house needs a new book.", "Издательству нужна новая книга."),
    ("неудача", "This is a failure.", "Это неудача."),
    ("пушка", "The cannon is old.", "Пушка старая."),
    ("муниципальный", "This is a municipal school.", "Это муниципальная школа."),
    ("снаряд", "The shell is nearby.", "Снаряд рядом."),
    ("сумасшедший", "He is crazy.", "Он сумасшедший."),
    ("мудрость", "I need wisdom.", "Мне нужна мудрость."),
    ("мрачный", "The sky is gloomy today.", "Небо сегодня мрачное."),
    ("исполнительный", "This is executive power.", "Это исполнительная власть."),
    ("ядро", "The nucleus is in the center.", "Ядро в центре."),
    ("историк", "The historian reads about the past.", "Историк читает о прошлом."),
    ("виртуальный", "This is a virtual world.", "Это виртуальный мир."),
    ("тянуться", "I like to stretch in the morning.", "Я люблю тянуться утром."),
    ("предок", "He is my ancestor.", "Он мой предок."),
    ("сок", "I drink juice every morning.", "Я пью сок каждое утро."),
    ("плыть", "I want to swim to the other side.", "Я хочу плыть на другую сторону."),
    ("громкий", "The music is loud.", "Музыка громкая."),
    ("рассуждение", "I hear his reasoning.", "Я слышу его рассуждение."),
]


def load_lemmas(path: Path) -> set[str]:
    return {line.strip().lower() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()}


def en_tokens(text: str) -> list[str]:
    return [t for t in re.findall(r"[a-zA-Z']+", text.lower()) if t]


def ru_tokens(text: str) -> list[str]:
    return [t.replace("ё", "е") for t in re.findall(r"[а-яёА-ЯЁ]+", text.lower()) if t]


def stem_en(word: str) -> list[str]:
    out = {word}
    for suf in ("'s", "s'", "ies", "es", "ed", "ing", "ly", "er", "est", "s"):
        if word.endswith(suf) and len(word) > len(suf) + 2:
            out.add(word[: -len(suf)])
            if suf == "ies":
                out.add(word[:-3] + "y")
            if suf == "ed" and word.endswith("ied"):
                out.add(word[:-3] + "y")
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
    for lemma in allow | extra:
        parts = lemma.replace("-", " ").split()
        if word in parts:
            return True
    return False


def ru_ok(word: str, allow: set[str], extra: set[str]) -> bool:
    if word in allow or word in extra:
        return True
    for lemma in allow | extra:
        lemma = lemma.replace("ё", "е")
        if len(lemma) < 3:
            continue
        stem = lemma[: max(3, len(lemma) - 2)]
        if word.startswith(stem) or lemma.startswith(word[: max(3, len(word) - 2)]):
            return True
    return False


def lemma_in_en(gloss: str, example: str) -> bool:
    g = re.sub(r"^(to |the |a |an )", "", gloss.strip().lower())
    ex = example.lower()
    if g in ex:
        return True
    parts = [p for p in re.split(r"[\s/-]+", g) if p and p not in {"to", "the", "a", "an"}]
    return all(p in ex or any(p in stem_en(t) or t in stem_en(p) for t in en_tokens(ex)) for p in parts)


def lemma_in_ru(lemma: str, example: str) -> bool:
    lemma = lemma.replace("ё", "е").lower()
    tokens = ru_tokens(example)
    if lemma in tokens:
        return True
    stem = lemma[: max(3, len(lemma) - 2)]
    return any(t.startswith(stem) or lemma.startswith(t[: max(3, len(t) - 2)]) for t in tokens)


def main() -> None:
    allow_en = load_lemmas(ALLOW_EN)
    allow_ru = {x.replace("ё", "е") for x in load_lemmas(ALLOW_RU)}
    originals = cards_from_path(SRC)
    if len(originals) != 100:
        raise SystemExit(f"expected 100 source cards, got {len(originals)}")
    if len(FIXED) != 100:
        raise SystemExit(f"expected 100 fixes, got {len(FIXED)}")

    out_cards = []
    leftover: list[str] = []
    lemma_miss: list[str] = []
    for i, card in enumerate(originals):
        ru_lemma, en_ex, ru_ex = FIXED[i]
        new = {
            "qMdPrompt": "Translate:",
            "qMdBody": card["qMdBody"],
            "qMdClarifier": "",
            "qMdFootnote": en_ex,
            "aMdPrompt": "",
            "aMdBody": ru_lemma,
            "aMdClarifier": "",
            "aMdFootnote": ru_ex,
        }
        extra_en = set(en_tokens(new["qMdBody"] or ""))
        extra_en.update(p for p in (new["qMdBody"] or "").replace("-", " ").lower().split() if p)
        extra_ru = set(ru_tokens(new["aMdBody"] or ""))
        payload = card_write_payload(new)
        out_cards.append(payload)

        if not lemma_in_en(new["qMdBody"] or "", en_ex):
            lemma_miss.append(f"EN {i+1} {new['qMdBody']!r} missing in {en_ex!r}")
        if not lemma_in_ru(ru_lemma, ru_ex):
            lemma_miss.append(f"RU {i+1} {ru_lemma!r} missing in {ru_ex!r}")

        for tok in en_tokens(en_ex):
            if not en_ok(tok, allow_en, extra_en):
                leftover.append(f"EN {i+1} {new['qMdBody']!r}: {tok}")
        for tok in ru_tokens(ru_ex):
            if not ru_ok(tok, allow_ru, extra_ru):
                leftover.append(f"RU {i+1} {ru_lemma!r}: {tok}")

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
    if lemma_miss:
        print("LEMMA MISS:")
        for line in lemma_miss:
            print(" ", line)
    if leftover:
        print("LEFTOVER:")
        for line in leftover:
            print(" ", line)
    else:
        print("vocab check clean")


if __name__ == "__main__":
    main()
