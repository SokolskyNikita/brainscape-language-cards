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

SRC = PACK / "_chunks" / "deck_15260255_01.csv"
OUT = PACK / "_chunks" / "fixed" / "deck_15260255_01.csv"
LOG = PACK / "_chunks" / "logs" / "deck_15260255_01.txt"

FUNCTION = {
    "a", "the", "is", "be", "i", "you", "he", "she", "it", "we", "they",
    "my", "and", "or", "in", "on", "at", "to", "of", "for", "with", "from",
    "not", "his", "him", "her", "their", "them", "our", "us", "me", "am",
    "are", "was", "were", "been", "being", "this", "that", "these", "those",
    "an", "as", "by", "into", "about", "than", "then", "so", "if", "but",
    "its", "your",
}

RU_FUNCTION = {
    "я", "ты", "он", "она", "оно", "мы", "вы", "они",
    "меня", "тебя", "его", "её", "ее", "нас", "вас", "их",
    "мне", "тебе", "ему", "ей", "нам", "вам", "им",
    "мной", "тобой", "ним", "ней", "нами", "вами", "ними",
    "него", "неё", "нее", "нему", "ней", "ним",
    "мой", "моя", "моё", "мое", "мои", "моего", "моей", "моём", "моем", "моих",
    "твой", "твоя", "твоё", "твое", "твои", "твоего", "твоей", "твоих",
    "свой", "своя", "своё", "свое", "свои", "своего", "своей", "своём", "своем",
        "своих", "своему", "своим", "своими", "своём", "своем", "свою", "своего",
    "наш", "наша", "наше", "наши", "нашего", "нашей", "наших",
    "ваш", "ваша", "ваше", "ваши", "вашего", "вашей", "ваших",
    "этот", "эта", "это", "эти", "этого", "этой", "этом", "этих", "этим", "этими", "эту",
    "тот", "та", "то", "те",
    "быть", "был", "была", "было", "были", "будет", "будут", "буду", "будем",
    "есть", "нет", "не", "да", "и", "а", "но", "или", "что", "как", "где",
    "когда", "кто", "чем", "в", "на", "с", "к", "у", "о", "об", "от", "до",
    "за", "из", "по", "для", "при", "про", "без", "над", "под", "между",
    "во", "со", "ко",
}

allow_en = {
    line.strip().lower()
    for line in (PACK / "_vocab" / "allow_en_15260255.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_ru = {
    line.strip().replace("ё", "е").lower()
    for line in (PACK / "_vocab" / "allow_ru_15260255.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_en |= FUNCTION

# (en_lemma, en_ex, ru_lemma, ru_ex)
FIXED = [
    ("Saturday", "I rest every Saturday.", "суббота", "Я отдыхаю каждую субботу."),
    ("lie down", "I want to lie down.", "лечь", "Я хочу лечь."),
    ("to count on", "I learned to count on him.", "рассчитывать", "Я научился рассчитывать на него."),
    ("obvious", "The answer was obvious.", "очевидный", "Ответ был очевиден."),
    ("fifty", "She is fifty.", "пятьдесят", "Ей пятьдесят."),
    ("substance", "Water is an important substance.", "вещество", "Вода — важное вещество."),
    ("academy", "She studies at the academy.", "академия", "Она учится в академии."),
    ("continuation", "The continuation of the story is short.", "продолжение", "Продолжение рассказа короткое."),
    ("centimeter", "The table is ten centimeters.", "сантиметр", "Стол — десять сантиметров."),
    ("forever", "I will remember you forever.", "навсегда", "Я буду помнить тебя навсегда."),
    ("belly", "His belly is very big.", "живот", "У него очень большой живот."),
    ("root", "The root of the tree is strong.", "корень", "Корень дерева сильный."),
    ("wooden", "There is a wooden table.", "деревянный", "Есть деревянный стол."),
    ("sample", "Please look at the sample.", "образец", "Пожалуйста, посмотрите на образец."),
    ("terrestrial", "Earth is a terrestrial planet.", "земной", "Земля — земная планета."),
    ("profession", "This is an important profession.", "профессия", "Это важная профессия."),
    ("out", "Get out of my room!", "вон", "Вон из моей комнаты!"),
    ("commercial", "This is a commercial bank.", "коммерческий", "Это коммерческий банк."),
    ("to play", "He will play this song.", "сыграть", "Он сыграет эту песню."),
    ("hotel", "We live in a hotel.", "гостиница", "Мы живём в гостинице."),
    ("campaign", "The campaign was successful.", "кампания", "Кампания была успешной."),
    ("assertion", "His assertion was true.", "утверждение", "Его утверждение было верным."),
    ("withstand", "The house can withstand this wind.", "выдержать", "Дом может выдержать этот ветер."),
    ("mail", "I received the mail today.", "почта", "Я получил почту сегодня."),
    ("to carry", "I will carry you home.", "повезти", "Я повезу тебя домой."),
    ("to listen", "I want to listen to the birds.", "послушать", "Я хочу послушать птиц."),
    ("oh", "Oh, I know!", "ой", "Ой, я знаю!"),
    ("listener", "He is a good listener.", "слушатель", "Он хороший слушатель."),
    ("pause", "Let's take a pause.", "пауза", "Давайте сделаем паузу."),
    ("chamber", "He is in the chamber.", "палата", "Он в палате."),
    ("efficiency", "This work needs more efficiency.", "эффективность", "Этой работе нужна большая эффективность."),
    ("credit", "The bank gives credit.", "кредит", "Банк даёт кредит."),
    ("drunk", "He was drunk at the party.", "пьяный", "Он был пьяный на вечеринке."),
    ("to win", "She wants to win.", "победить", "Она хочет победить."),
    ("confidence", "She speaks with great confidence.", "уверенность", "Она говорит с большой уверенностью."),
    ("to make sure", "I want to make sure.", "убедиться", "Я хочу убедиться."),
    ("sir", "Yes, sir.", "сэр", "Да, сэр."),
    ("teaching", "This teaching is old.", "учение", "Это учение старое."),
    ("celebrate", "We celebrate this day every year.", "отмечать", "Мы отмечаем этот день каждый год."),
    ("perception", "His perception of the world is interesting.", "восприятие", "Его восприятие мира интересно."),
    ("dirty", "His clothing was dirty.", "грязный", "Его одежда была грязной."),
    ("proof", "This is proof of his words.", "доказательство", "Это доказательство его слов."),
    ("Friday", "I love Friday.", "пятница", "Я люблю пятницу."),
    ("ring", "She wears a gold ring.", "кольцо", "Она носит золотое кольцо."),
    ("seller", "The seller is in the store.", "продавец", "Продавец в магазине."),
    ("capture", "They want to capture the city.", "захватить", "Они хотят захватить город."),
    ("magnitude", "The magnitude of the problem is great.", "величина", "Величина проблемы велика."),
    ("tension", "There is tension in the room.", "напряжение", "В комнате есть напряжение."),
    ("mandatory", "This meeting is mandatory.", "обязательный", "Эта встреча обязательна."),
    ("to be found", "The key will be found.", "найтись", "Ключ найдётся."),
    ("peasant", "The peasant works in the field.", "крестьянин", "Крестьянин работает в поле."),
    ("to undertake", "She decided to undertake the work.", "приняться", "Она решила приняться за работу."),
    ("to refuse", "He decided to refuse the offer.", "отказываться", "Он решил отказаться от предложения."),
    ("suggest", "I want to suggest this plan.", "предложить", "Я хочу предложить этот план."),
    ("catch", "I will catch you.", "поймать", "Я поймаю тебя."),
    ("rural", "She lives in a rural house.", "сельский", "Она живёт в сельском доме."),
    ("to wait", "I decided to wait at home.", "подождать", "Я решил подождать дома."),
    ("peak", "We reached the peak.", "вершина", "Мы достигли вершины."),
    ("board", "Write this on the board.", "доска", "Напишите это на доске."),
    ("Japanese", "I love Japanese food.", "японский", "Я люблю японскую еду."),
    ("secret", "I know her secret.", "секрет", "Я знаю её секрет."),
    ("to achieve", "I want to achieve success.", "достигать", "Я хочу достигать успеха."),
    ("to protect", "Soldiers protect their country.", "защищать", "Солдаты защищают свою страну."),
    ("perceive", "I perceive colors.", "воспринимать", "Я воспринимаю цвета."),
    ("to prefer", "I prefer coffee to tea.", "предпочитать", "Я предпочитаю кофе чаю."),
    ("pen", "This is my favorite pen.", "ручка", "Это моя любимая ручка."),
    ("identical", "Their answers were identical.", "одинаковый", "Их ответы были одинаковыми."),
    ("hit", "He hit the table hard.", "ударить", "Он сильно ударил по столу."),
    ("to smoke", "He wants to smoke outside.", "курить", "Он хочет курить на улице."),
    ("testify", "She will testify tomorrow.", "свидетельствовать", "Она будет свидетельствовать завтра."),
    ("confirm", "Please confirm this tomorrow.", "подтвердить", "Пожалуйста, подтвердите это завтра."),
    ("to rush", "He decided to rush into the fight.", "броситься", "Он решил броситься в бой."),
    ("Monday", "Monday is the start of the week.", "понедельник", "Понедельник — начало недели."),
    ("strict", "Her parents are very strict.", "строгий", "Её родители очень строгие."),
    ("breathe", "I want to breathe.", "дышать", "Я хочу дышать."),
    ("portrait", "This is his portrait.", "портрет", "Это его портрет."),
    ("grab", "Grab your bag.", "схватить", "Схвати свою сумку."),
    ("nuclear", "Nuclear energy is important.", "ядерный", "Ядерная энергия важна."),
    ("threshold", "He is on the threshold.", "порог", "Он на пороге."),
    ("sector", "The sector is important.", "сектор", "Сектор важный."),
    ("walk", "Let's walk in the park today.", "гулять", "Давайте гулять в парке сегодня."),
    ("to give as a gift", "I want to give this book as a gift.", "подарить", "Я хочу подарить эту книгу."),
    ("beam", "A beam of light is on the table.", "луч", "Луч света на столе."),
    ("conclude", "They will conclude the agreement tomorrow.", "заключить", "Они заключат соглашение завтра."),
    ("surrounding", "The surrounding nature is beautiful.", "окружающий", "Окружающая природа красивая."),
    ("to commit", "He decided to commit a crime.", "совершать", "Он решил совершить преступление."),
    ("cool", "That's a cool idea!", "крутой", "Это крутая идея!"),
    ("habit", "Reading is a good habit.", "привычка", "Чтение — хорошая привычка."),
    ("unique", "Her talent is unique.", "уникальный", "Её талант уникальный."),
    ("lieutenant", "The lieutenant is in the army.", "лейтенант", "Лейтенант в армии."),
    ("press", "The press writes about the government.", "пресса", "Пресса пишет о правительстве."),
    ("test", "Life is a test.", "испытание", "Жизнь — это испытание."),
    ("emotion", "This is a strong emotion.", "эмоция", "Это сильная эмоция."),
    ("apply", "Apply this theory.", "применять", "Примените эту теорию."),
    ("nine", "We have nine books.", "девять", "У нас девять книг."),
    ("join", "I will join the club today.", "вступить", "Я вступлю в клуб сегодня."),
    ("transport", "We need public transport.", "транспорт", "Нам нужен общественный транспорт."),
    ("offensive", "The army will begin an offensive.", "наступление", "Армия начнёт наступление."),
    ("manifestation", "This is a manifestation of his fear.", "проявление", "Это проявление его страха."),
    ("tail", "The dog's tail is big.", "хвост", "Хвост собаки большой."),
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
    return forms


def en_ok(text: str, extra: set[str] | None = None) -> list[str]:
    extra = extra or set()
    bad = []
    for raw in re.findall(r"[A-Za-z']+", text):
        w = raw.lower().replace("'", "")
        if not w or w in allow_en or w in extra or w == "tv":
            continue
        if any(form in allow_en or form in extra for form in en_forms(w)):
            continue
        if w.endswith("ly") and w[:-2] + "l" in allow_en:
            continue
        bad.append(raw)
    return bad


def ru_ok(text: str, extra: set[str] | None = None) -> list[str]:
    extra = extra or set()
    bad = []
    for raw in re.findall(r"[А-Яа-яЁё-]+", text):
        w = raw.replace("ё", "е").replace("Ё", "е").lower()
        if w in allow_ru or w in extra or w in RU_FUNCTION:
            continue
        pool = allow_ru | extra
        if any(w.startswith(lemma) or lemma.startswith(w) for lemma in pool if len(lemma) >= 4 and len(w) >= 4):
            continue
        if any(
            w[: max(4, len(w) - 3)] == lemma[: max(4, len(w) - 3)]
            for lemma in pool
            if abs(len(lemma) - len(w)) <= 4 and min(len(lemma), len(w)) >= 4
        ):
            continue
        bad.append(raw)
    return bad


def lemma_tokens_en(en: str) -> set[str]:
    parts = re.findall(r"[A-Za-z']+", en.lower())
    return {p.replace("'", "") for p in parts if p.replace("'", "")}


def lemma_tokens_ru(ru: str) -> set[str]:
    parts = re.findall(r"[А-Яа-яЁё-]+", ru.lower())
    return {p.replace("ё", "е") for p in parts}


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
        stem = ru_key[:4]
        if stem not in ru_ex_n and not any(
            ru_ex_n.startswith(p) or p in ru_ex_n
            for p in (ru_key, ru_key[:5], ru_key[:3])
            if len(p) >= 3
        ):
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
