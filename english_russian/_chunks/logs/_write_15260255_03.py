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

SRC = PACK / "_chunks" / "deck_15260255_03.csv"
OUT = PACK / "_chunks" / "fixed" / "deck_15260255_03.csv"
LOG = PACK / "_chunks" / "logs" / "deck_15260255_03.txt"

FUNCTION = {
    "a", "the", "is", "be", "i", "you", "he", "she", "it", "we", "they",
    "my", "and", "or", "in", "on", "at", "to", "of", "for", "with", "from",
    "not", "his", "him", "her", "their", "them", "our", "us", "me", "am",
    "are", "was", "were", "been", "being", "this", "that", "these", "those",
    "an", "as", "by", "into", "about", "than", "then", "so", "if", "but",
    "its", "your",
}

IRREGULAR = {
    "began": "begin", "begun": "begin",
    "lost": "lose",
    "grew": "grow", "grown": "grow",
    "came": "come",
    "went": "go", "gone": "go",
    "saw": "see", "seen": "see",
    "knew": "know", "known": "know",
    "said": "say",
    "took": "take", "taken": "take",
    "gave": "give", "given": "give",
    "found": "find",
    "made": "make",
    "looked": "look",
    "felt": "feel",
    "wanted": "want",
    "needed": "need",
    "helped": "help",
    "waited": "wait",
    "has": "have", "had": "have",
    "did": "do", "done": "do",
    "led": "lead",
    "caught": "catch",
    "fell": "fall",
    "got": "get",
    "wrote": "write", "written": "write",
    "forgot": "forget", "forgotten": "forget",
    "wore": "wear", "worn": "wear",
    "sold": "sell",
    "stopped": "stop",
    "started": "start",
    "opened": "open",
    "learned": "learn",
    "left": "leave",
    "thought": "think",
    "brought": "bring",
    "bought": "buy",
    "told": "tell",
    "heard": "hear",
    "held": "hold",
    "kept": "keep",
    "let": "let",
    "put": "put",
    "read": "read",
    "ran": "run",
    "sat": "sit",
    "stood": "stand",
    "spoke": "speak",
    "spent": "spend",
    "won": "win",
    "met": "meet",
    "became": "become",
    "built": "build",
    "chose": "choose",
    "drew": "draw",
    "drove": "drive",
    "ate": "eat",
    "flew": "fly",
    "hid": "hide",
    "hit": "hit",
    "hurt": "hurt",
    "lay": "lie",
    "lain": "lie",
    "paid": "pay",
    "sent": "send",
    "sang": "sing",
    "slept": "sleep",
    "swam": "swim",
    "taught": "teach",
    "threw": "throw",
    "woke": "wake",
    "understood": "understand",
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
    ("funny", "Your joke was really funny.", "смешной", "Твоя шутка была действительно смешной."),
    ("to demand", "He demanded an explanation.", "потребовать", "Он потребовал объяснение."),
    ("absolute", "His power is absolute.", "абсолютный", "Его сила абсолютная."),
    ("seminar", "I was at a seminar yesterday.", "семинар", "Я был на семинаре вчера."),
    ("metro", "I take the metro to work.", "метро", "Я езжу на метро на работу."),
    ("recommend", "I recommend this book.", "рекомендовать", "Я рекомендую эту книгу."),
    ("server", "The server does not work.", "сервер", "Сервер не работает."),
    ("audience", "The audience listened.", "публика", "Публика слушала."),
    ("prayer", "She said a prayer.", "молитва", "Она сказала молитву."),
    ("glasses", "He lost his glasses yesterday.", "очки", "Он потерял свои очки вчера."),
    ("hand in", "I need to hand in my work.", "сдать", "Мне нужно сдать работу."),
    ("hate", "I hate this work.", "ненавидеть", "Я ненавижу эту работу."),
    ("resistance", "The resistance was strong.", "сопротивление", "Сопротивление было сильным."),
    ("to cope", "I can cope with this work.", "справиться", "Я могу справиться с этой работой."),
    ("luck", "Good luck on your exam!", "удача", "Удачи на экзамене!"),
    ("policeman", "The policeman came yesterday.", "полицейский", "Полицейский пришёл вчера."),
    ("to recognize", "They recognize this fact.", "признавать", "Они признают этот факт."),
    ("collection", "The collection started yesterday.", "сбор", "Сбор начался вчера."),
    ("length", "I know the length of the table.", "длина", "Я знаю длину стола."),
    ("peaceful", "The village was peaceful.", "мирный", "Деревня была мирной."),
    ("wheel", "The car's wheel is new.", "колесо", "Колесо машины новое."),
    ("intention", "His intention was clear.", "намерение", "Его намерение было ясным."),
    ("friendship", "Friendship is important.", "дружба", "Дружба важна."),
    ("unexpected", "The gift was completely unexpected.", "неожиданный", "Подарок был совершенно неожиданным."),
    ("dinner", "I want dinner now.", "ужин", "Я хочу ужин сейчас."),
    ("engine", "The car's engine stopped.", "двигатель", "Двигатель машины остановился."),
    ("young man", "The young man came yesterday.", "юноша", "Юноша пришёл вчера."),
    ("talent", "She has talent.", "талант", "У неё есть талант."),
    ("automatic", "This door is automatic.", "автоматический", "Эта дверь автоматическая."),
    ("beast", "The beast was in the forest.", "зверь", "Зверь был в лесу."),
    ("naked", "The man was naked.", "голый", "Мужчина был голым."),
    ("worry", "She began to worry.", "переживать", "Она начала переживать."),
    ("corpse", "They found a corpse.", "труп", "Они нашли труп."),
    ("turn", "Take the next left turn.", "поворот", "Сделайте следующий левый поворот."),
    ("priest", "The priest led the service.", "священник", "Священник провёл службу."),
    ("exercise", "I do my exercise every day.", "упражнение", "Я делаю своё упражнение каждый день."),
    ("punishment", "He received his punishment quietly.", "наказание", "Он тихо получил своё наказание."),
    ("strategic", "This is a strategic plan.", "стратегический", "Это стратегический план."),
    ("moral", "This is a moral question.", "моральный", "Это моральный вопрос."),
    ("mention", "I mentioned your name.", "упомянуть", "Я упомянул твоё имя."),
    ("to give birth", "She is going to give birth soon.", "родить", "Она скоро собирается родить."),
    ("sword", "He took his sword.", "меч", "Он взял свой меч."),
    ("processing", "Processing of documents takes time.", "обработка", "Обработка документов занимает время."),
    ("mobile", "I lost my mobile yesterday.", "мобильный", "Я потерял свой мобильный вчера."),
    ("to be carried out", "The plan will be carried out soon.", "осуществляться", "План скоро осуществится."),
    ("incomprehensible", "His explanation was incomprehensible.", "непонятный", "Его объяснение было непонятным."),
    ("complexity", "I see the complexity of the problem.", "сложность", "Я вижу сложность проблемы."),
    ("conscience", "His conscience is clear.", "совесть", "Его совесть чистая."),
    ("sofa", "I sit on the sofa.", "диван", "Я сижу на диване."),
    ("hunting", "We are going hunting tomorrow.", "охота", "Мы идём на охоту завтра."),
    ("drug", "He was caught selling drugs.", "наркотик", "Он был пойман на продаже наркотиков."),
    ("community", "The community came yesterday.", "сообщество", "Сообщество пришло вчера."),
    ("passenger", "The passenger waited for the train.", "пассажир", "Пассажир ждал поезда."),
    ("poetry", "She writes beautiful poetry.", "поэзия", "Она пишет красивую поэзию."),
    ("to close", "Remember to close the window.", "закрывать", "Не забудь закрыть окно."),
    ("premium", "She received a premium.", "премия", "Она получила премию."),
    ("sufficient", "He has sufficient time.", "достаточный", "У него достаточное время."),
    ("script", "He wrote the script for a movie.", "сценарий", "Он написал сценарий для фильма."),
    ("psychology", "I study psychology at university.", "психология", "Я изучаю психологию в университете."),
    ("code", "I forgot the code.", "код", "Я забыл код."),
    ("alas", "Alas, I cannot come.", "увы", "Увы, я не могу прийти."),
    ("crew", "The crew is ready.", "экипаж", "Экипаж готов."),
    ("assistant", "The assistant solved the problem quickly.", "помощник", "Помощник быстро решил проблему."),
    ("to feed", "I need to feed the cat.", "кормить", "Мне нужно кормить кошку."),
    ("bone", "The dog found a bone.", "кость", "Собака нашла кость."),
    ("association", "He joined the local association.", "ассоциация", "Он вступил в местную ассоциацию."),
    ("entrepreneur", "The entrepreneur started a new project.", "предприниматель", "Предприниматель начал новый проект."),
    ("spread", "They spread the news quickly.", "распространить", "Они быстро распространили новость."),
    ("port", "The ship is in the port.", "порт", "Корабль в порту."),
    ("paint", "I need more red paint.", "краска", "Мне нужно больше красной краски."),
    ("to foresee", "He did not foresee the consequences.", "предусмотреть", "Он не предусмотрел последствия."),
    ("rocket", "The rocket is ready.", "ракета", "Ракета готова."),
    ("to marry", "He wants to marry next year.", "жениться", "Он хочет жениться в следующем году."),
    ("resolution", "The council passed a new resolution.", "постановление", "Совет принял новое постановление."),
    ("in vain", "He waited in vain.", "зря", "Он ждал зря."),
    ("mud", "The car is in the mud.", "грязь", "Машина в грязи."),
    ("certificate", "She received her birth certificate today.", "свидетельство", "Она получила своё свидетельство о рождении сегодня."),
    ("to think over", "I need to think over this.", "обдумать", "Мне нужно обдумать это."),
    ("to shout", "He shouted for help.", "крикнуть", "Он крикнул о помощи."),
    ("sand", "I see sand on the street.", "песок", "Я вижу песок на улице."),
    ("tempo", "The tempo of the music is fast.", "темп", "Темп музыки быстрый."),
    ("avoid", "I want to avoid this.", "избежать", "Я хочу избежать этого."),
    ("ceiling", "The ceiling is high.", "потолок", "Потолок высокий."),
    ("vacation", "I need a vacation soon.", "отпуск", "Мне скоро нужен отпуск."),
    ("thoroughly", "She thoroughly read the document.", "тщательно", "Она тщательно прочитала документ."),
    ("angel", "She looked like an angel.", "ангел", "Она выглядела как ангел."),
    ("monastery", "He saw the ancient monastery.", "монастырь", "Он видел древний монастырь."),
    ("below", "He lives below.", "внизу", "Он живёт внизу."),
    ("route", "We know our route.", "маршрут", "Мы знаем наш маршрут."),
    ("unusual", "She wore an unusual dress today.", "необычный", "Она носила необычное платье сегодня."),
    ("dust", "I see dust on the table.", "пыль", "Я вижу пыль на столе."),
    ("to invite", "I decided to invite my friends.", "приглашать", "Я решил пригласить моих друзей."),
    ("plant", "The plant is in the room.", "растение", "Растение в комнате."),
    ("democratic", "We live in a democratic society.", "демократический", "Мы живём в демократическом обществе."),
    ("ideal", "This is an ideal solution for us.", "идеальный", "Это идеальное решение для нас."),
    ("turnover", "The turnover is high.", "оборот", "Оборот высокий."),
    ("to put on", "She put on a dress.", "надеть", "Она надела платье."),
    ("nowhere", "He is going nowhere.", "никуда", "Он никуда не идёт."),
    ("fighter", "She is a true fighter.", "боец", "Она настоящий боец."),
    ("introduction", "The book's introduction is short.", "введение", "Введение книги короткое."),
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


def en_ok(text: str) -> list[str]:
    bad = []
    for raw in re.findall(r"[A-Za-z']+", text):
        w = raw.lower().replace("'", "")
        if not w or w in allow_en:
            continue
        if any(form in allow_en for form in en_forms(w)):
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
        if w in allow_ru or w in extra:
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
        extra = {ru.lower().replace("ё", "е")}
        for token in en_ok(en_ex):
            leftover.append(f"{i} EN leftover {token!r}: {en_ex}")
        for token in ru_ok(ru_ex, extra):
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
