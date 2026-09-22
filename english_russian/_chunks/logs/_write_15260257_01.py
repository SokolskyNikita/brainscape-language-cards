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

SRC = PACK / "_chunks" / "deck_15260257_01.csv"
OUT = PACK / "_chunks" / "fixed" / "deck_15260257_01.csv"
LOG = PACK / "_chunks" / "logs" / "deck_15260257_01.txt"

FUNCTION = {
    "a", "the", "is", "be", "i", "you", "he", "she", "it", "we", "they",
    "my", "and", "or", "in", "on", "at", "to", "of", "for", "with", "from",
    "not", "his", "him", "her", "their", "them", "our", "us", "me", "am",
    "are", "was", "were", "been", "being", "this", "that", "these", "those",
    "an", "as", "by", "into", "about", "than", "then", "so", "if", "but",
    "its", "your",
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
    ("reputation", "He has a good reputation.", "репутация", "У него хорошая репутация."),
    ("coffin", "They carry the coffin.", "гроб", "Они несут гроб."),
    ("to make a mistake", "I tried not to make a mistake.", "ошибиться", "Я пытался не ошибиться."),
    ("increased", "He has increased interest.", "повышенный", "У него повышенный интерес."),
    ("congratulate", "We congratulate the team every year.", "поздравлять", "Мы поздравляем команду каждый год."),
    ("to print", "I need to print the document.", "напечатать", "Мне нужно напечатать документ."),
    ("pool", "We swim in the pool today.", "бассейн", "Мы сегодня плаваем в бассейне."),
    ("joyfully", "She joyfully accepted the gift.", "радостно", "Она радостно приняла подарок."),
    ("mayor", "The mayor opened the new park.", "мэр", "Мэр открыл новый парк."),
    ("currency", "The dollar is a strong currency.", "валюта", "Доллар - сильная валюта."),
    ("maximally", "Use this process maximally.", "максимально", "Используйте процесс максимально."),
    ("cabin", "The driver sat in the cabin.", "кабина", "Водитель сидел в кабине."),
    ("prosecutor", "The prosecutor spoke in court.", "прокурор", "Прокурор говорил в суде."),
    ("critic", "The critic wrote about the book.", "критик", "Критик написал о книге."),
    ("wander", "I love to wander through the forest.", "бродить", "Я люблю бродить по лесу."),
    ("carrier", "He is a carrier of this disease.", "носитель", "Он носитель этой болезни."),
    ("inevitable", "Change is inevitable in life.", "неизбежный", "Изменения в жизни неизбежны."),
    ("jacket", "I have a new winter jacket.", "куртка", "У меня новая зимняя куртка."),
    ("partly", "He was partly responsible for the error.", "отчасти", "Он был отчасти ответствен за ошибку."),
    ("unclear", "The text is unclear.", "непонятный", "Текст непонятный."),
    ("asset", "Knowledge is an important asset.", "актив", "Знание — важный актив."),
    ("bypass", "We'll bypass the main road.", "обойти", "Мы обойдем главную дорогу."),
    ("inconspicuously", "He inconspicuously left the room.", "незаметно", "Он незаметно вышел из комнаты."),
    ("to deserve", "He worked hard to deserve success.", "заслужить", "Он много работал, чтобы заслужить успех."),
    ("cemetery", "We visited the cemetery.", "кладбище", "Мы посетили кладбище."),
    ("echo", "I heard an echo.", "эхо", "Я слышал эхо."),
    ("glorious", "The victory was glorious.", "славный", "Победа была славной."),
    ("euro", "I have fifty euro.", "евро", "У меня пятьдесят евро."),
    ("landing", "The landing was good.", "посадка", "Посадка была хорошей."),
    ("icon", "There is a sacred icon on the wall.", "икона", "На стене есть священная икона."),
    ("sequence", "Follow the correct sequence.", "последовательность", "Следуйте правильной последовательности."),
    ("two hundred", "I have two hundred dollars.", "двести", "У меня двести долларов."),
    ("yesterday's", "Yesterday's news was important.", "вчерашний", "Вчерашние новости были важными."),
    ("shoe", "I lost my shoe yesterday.", "ботинок", "Вчера я потерял свой ботинок."),
    ("conveniently", "The store is conveniently near.", "удобно", "Магазин удобно рядом."),
    ("trousers", "He has new trousers.", "штаны", "У него новые штаны."),
    ("to be stored", "The documents are to be stored there.", "храниться", "Документы хранятся там."),
    ("battalion", "The battalion stood at dawn.", "батальон", "Батальон стоял на рассвете."),
    ("testimony", "His testimony was important in court.", "показание", "Его показание было важным в суде."),
    ("specialty", "This is her specialty.", "специальность", "Это её специальность."),
    ("calculate", "I will calculate the cost.", "рассчитать", "Я рассчитаю цену."),
    ("refrigerator", "There is milk in the refrigerator.", "холодильник", "В холодильнике есть молоко."),
    ("verse", "She read a beautiful verse aloud.", "стих", "Она вслух прочитала красивый стих."),
    ("arrest", "Police will arrest him soon.", "арестовать", "Полиция скоро арестует его."),
    ("kopeck", "I found a kopeck on the street.", "копейка", "Я нашёл копейку на улице."),
    ("wounded", "He is a wounded soldier.", "раненый", "Он раненый солдат."),
    ("gaze", "His gaze was cold.", "взор", "Его взор был холодным."),
    ("throw out", "Please throw out the trash.", "выбросить", "Пожалуйста, выбросьте мусор."),
    ("fill", "Fill the cup with water, please.", "наполнить", "Наполните чашку водой, пожалуйста."),
    ("jump out", "The cat will jump out soon.", "выскочить", "Кошка скоро выскочит."),
    ("outcome", "The outcome was unexpected.", "исход", "Исход был неожиданным."),
    ("terrorist", "The terrorist was finally captured.", "террорист", "Террориста наконец-то захватили."),
    ("suitcase", "I took my suitcase for the trip.", "чемодан", "Я взял свой чемодан для поездки."),
    ("let down", "He promised but let me down.", "подвести", "Он обещал, но подвёл меня."),
    ("disabled person", "The disabled person needs help.", "инвалид", "Инвалиду нужна помощь."),
    ("shake", "I will shake my head.", "покачать", "Я покачаю головой."),
    ("to spread", "The news began to spread quickly.", "распространяться", "Новости начали быстро распространяться."),
    ("invitation", "I received an invitation yesterday.", "приглашение", "Вчера я получил приглашение."),
    ("commissar", "The commissar gave a strict command.", "комиссар", "Комиссар дал строгую команду."),
    ("to jump up", "He jumped up from the chair.", "вскочить", "Он вскочил со стула."),
    ("aloud", "She read the poem aloud.", "вслух", "Она прочитала стихотворение вслух."),
    ("infant", "The infant slept in the bed.", "младенец", "Младенец спал в кровати."),
    ("unfold", "Please unfold the map.", "развернуть", "Пожалуйста, разверните карту."),
    ("balance", "Keep balance in your life.", "баланс", "Держите баланс в жизни."),
    ("suspicion", "His look was full of suspicion.", "подозрение", "Его взгляд был полон подозрения."),
    ("visa", "I need a visa.", "виза", "Мне нужна виза."),
    ("to serve", "He wanted to serve his country.", "послужить", "Он хотел послужить своей стране."),
    ("muzzle", "The dog's muzzle was soft and wet.", "морда", "Морда собаки была мягкой и мокрой."),
    ("attentive", "She was attentive to his needs.", "внимательный", "Она была внимательна к его потребностям."),
    ("fragment", "I found a fragment of the letter.", "фрагмент", "Я нашёл фрагмент письма."),
    ("hole", "I fell into a deep hole.", "дыра", "Я упал в глубокую дыру."),
    ("specifically", "He asked specifically about the work.", "конкретно", "Он спросил конкретно о работе."),
    ("to value", "Learn to value simple pleasures.", "ценить", "Научитесь ценить простые радости."),
    ("confidently", "She confidently answered the question.", "уверенно", "Она уверенно ответила на вопрос."),
    ("basement", "We store wine in the basement.", "подвал", "Мы храним вино в подвале."),
    ("busy", "He's too busy today.", "занятый", "Он очень занят сегодня."),
    ("false", "This is a false name.", "ложный", "Это ложное имя."),
    ("attractive", "She found him very attractive.", "привлекательный", "Она нашла его очень привлекательным."),
    ("stove", "I cooked dinner on the stove.", "плита", "Я готовил ужин на плите."),
    ("atomic", "This is an atomic station.", "атомный", "Это атомная станция."),
    ("interrupt", "Please don't interrupt me.", "прервать", "Пожалуйста, не прерывай меня."),
    ("passage", "The narrow passage was strange.", "проход", "Узкий проход был странным."),
    ("choir", "The choir sang in the church.", "хор", "Хор пел в церкви."),
    ("maiden", "The maiden stood by the window.", "девица", "Девица стояла у окна."),
    ("sleeve", "She carefully pulled up her sleeve.", "рукав", "Она осторожно подняла рукав."),
    ("steal", "He tried to steal the picture.", "украсть", "Он пытался украсть картину."),
    ("socialism", "Socialism supports collective property.", "социализм", "Социализм выступает за коллективную собственность."),
    ("dining room", "We eat in the dining room.", "столовая", "Мы едим в столовой."),
    ("to be sold", "The house is to be sold soon.", "продаваться", "Дом скоро будет продаваться."),
    ("to head", "We decided to head north.", "направляться", "Мы направляемся на север."),
    ("favorable", "Weather conditions were favorable.", "благоприятный", "Погодные условия были благоприятными."),
    ("stick", "He found a big stick outside.", "палка", "Он нашел большую палку на улице."),
    ("outstanding", "He is an outstanding writer.", "выдающийся", "Он выдающийся писатель."),
    ("paradise", "This island is a true paradise.", "рай", "Остров — настоящий рай."),
    ("eyebrow", "She raised an eyebrow in surprise.", "бровь", "Она удивлённо подняла бровь."),
    ("to fall asleep", "I struggled to fall asleep last night.", "заснуть", "Мне было трудно заснуть прошлой ночью."),
    ("translator", "She works as a professional translator.", "переводчик", "Она работает профессиональным переводчиком."),
    ("break free", "She wanted to break free.", "вырваться", "Она хотела вырваться."),
    ("jointly", "They work jointly.", "совместно", "Они работают совместно."),
    ("equilibrium", "He lost his equilibrium.", "равновесие", "Он потерял равновесие."),
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


IRREGULAR = {
    "wrote": "write", "bought": "buy", "lost": "lose", "fell": "fall",
    "sang": "sing", "spent": "spend", "held": "hold", "slept": "sleep",
    "began": "begin", "stood": "stand", "found": "find", "took": "take",
    "gave": "give", "came": "come", "went": "go", "saw": "see",
    "heard": "hear", "left": "leave", "kept": "keep", "sat": "sit",
    "told": "tell", "said": "say", "made": "make", "did": "do",
    "had": "have", "been": "be", "was": "be", "were": "be",
    "ate": "eat", "ran": "run", "won": "win", "got": "get",
    "knew": "know", "thought": "think", "felt": "feel", "brought": "bring",
    "caught": "catch", "taught": "teach", "built": "build", "sent": "send",
    "paid": "pay", "sold": "sell", "met": "meet", "led": "lead",
    "grew": "grow", "became": "become", "spoke": "speak",
}


def en_ok(text: str) -> list[str]:
    bad = []
    for raw in re.findall(r"[A-Za-z']+", text):
        w = raw.lower().replace("'", "")
        if not w or w in allow_en or w == "tv":
            continue
        if IRREGULAR.get(w) in allow_en:
            continue
        if any(form in allow_en for form in en_forms(w)):
            continue
        if w.endswith("ly") and w[:-2] + "l" in allow_en:
            continue
        bad.append(raw)
    return bad


def ru_ok(text: str) -> list[str]:
    bad = []
    for raw in re.findall(r"[А-Яа-яЁё-]+", text):
        w = raw.replace("ё", "е").replace("Ё", "е").lower()
        if w in allow_ru:
            continue
        if len(w) <= 3:
            continue
        if any(w.startswith(lemma) or lemma.startswith(w) for lemma in allow_ru if len(lemma) >= 4 and len(w) >= 4):
            continue
        if any(w[: max(4, len(w) - 3)] == lemma[: max(4, len(w) - 3)] for lemma in allow_ru if abs(len(lemma) - len(w)) <= 4 and min(len(lemma), len(w)) >= 4):
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
        for token in en_ok(en_ex):
            leftover.append(f"{i} EN leftover {token!r}: {en_ex}")
        for token in ru_ok(ru_ex):
            leftover.append(f"{i} RU leftover {token!r}: {ru_ex}")
        if en.split()[0].lower() not in en_ex.lower() and en.lower() not in en_ex.lower():
            key = en.lower().replace("to ", "")
            if key not in en_ex.lower() and not any(p in en_ex.lower() for p in key.split()):
                leftover.append(f"{i}: EN example missing {en!r}")
        ru_key = ru.lower().replace("ё", "е")
        ru_ex_n = ru_ex.lower().replace("ё", "е")
        if ru_key[:4] not in ru_ex_n:
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
