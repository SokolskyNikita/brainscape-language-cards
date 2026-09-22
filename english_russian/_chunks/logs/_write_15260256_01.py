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

SRC = PACK / "_chunks" / "deck_15260256_01.csv"
OUT = PACK / "_chunks" / "fixed" / "deck_15260256_01.csv"
LOG = PACK / "_chunks" / "logs" / "deck_15260256_01.txt"

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
    for line in (PACK / "_vocab" / "allow_en_15260256.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_ru = {
    line.strip().replace("ё", "е").lower()
    for line in (PACK / "_vocab" / "allow_ru_15260256.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_en |= FUNCTION

# (en_lemma, en_ex, ru_lemma, ru_ex)
FIXED = [
    ("financing", "We need financing for this project.", "финансирование", "Нам нужно финансирование для этого проекта."),
    ("not bad", "This is not bad.", "неплохо", "Это неплохо."),
    ("to visit", "I want to visit this city soon.", "побывать", "Я хочу скоро побывать в этом городе."),
    ("ideology", "His ideology is clear.", "идеология", "Его идеология ясна."),
    ("register", "Please register this document.", "зарегистрировать", "Пожалуйста, зарегистрируйте этот документ."),
    ("command", "He received command of the army.", "командование", "Он получил командование армией."),
    ("negative", "The result was negative.", "отрицательный", "Результат был отрицательным."),
    ("to be created", "New companies continue to be created.", "создаваться", "Новые компании продолжают создаваться."),
    ("conviction", "His conviction is strong.", "убеждение", "Его убеждение сильно."),
    ("to regret", "He began to regret his words.", "жалеть", "Он начал жалеть о своих словах."),
    ("rock", "The rock is high.", "скала", "Скала высокая."),
    ("Tuesday", "I have a meeting on Tuesday.", "вторник", "У меня встреча во вторник."),
    ("certainly", "I will certainly come.", "непременно", "Я непременно приду."),
    ("accusation", "He refused the accusation.", "обвинение", "Он отказался от обвинения."),
    ("artificial", "These flowers look artificial.", "искусственный", "Эти цветы выглядят искусственными."),
    ("carry out", "They will carry out the old table.", "вынести", "Они вынесут старый стол."),
    ("exclude", "Please exclude this name from the list.", "исключить", "Пожалуйста, исключите это имя из списка."),
    ("liter", "I need a liter of milk.", "литр", "Мне нужен литр молока."),
    ("textbook", "Her textbook is at home.", "учебник", "Её учебник дома."),
    ("to exceed", "This number can exceed ten.", "превышать", "Это число может превышать десять."),
    ("ribbon", "She has a red ribbon in her hair.", "лента", "У неё красная лента в волосах."),
    ("Christian", "This is a Christian book.", "христианский", "Это христианская книга."),
    ("insufficient", "His answer was insufficient.", "недостаточный", "Его ответ был недостаточным."),
    ("readiness", "His readiness is important.", "готовность", "Его готовность важна."),
    ("authority", "He spoke to the authority.", "начальство", "Он говорил с начальством."),
    ("to manifest", "Dreams began to manifest in reality.", "проявляться", "Мечты начали проявляться в реальности."),
    ("load", "The computer has a big load.", "нагрузка", "У компьютера большая нагрузка."),
    ("unite", "Let's unite our groups.", "объединить", "Давайте объединим наши группы."),
    ("soulful", "Her voice was deep and soulful.", "душевный", "Её голос был глубоким и душевным."),
    ("slave", "He lived like a slave.", "раб", "Он жил как раб."),
    ("correspondent", "The correspondent wrote this letter.", "корреспондент", "Корреспондент написал это письмо."),
    ("satellite", "The satellite is near Earth.", "спутник", "Спутник рядом с Землёй."),
    ("chain", "This chain is strong.", "цепь", "Эта цепь сильная."),
    ("miss", "I will miss the train again.", "пропустить", "Я снова пропущу поезд."),
    ("pink", "She has a bright pink dress.", "розовый", "У неё яркое розовое платье."),
    ("to thank", "We thank the teacher.", "благодарить", "Мы благодарим учителя."),
    ("episode", "I watched this episode yesterday.", "эпизод", "Я смотрел этот эпизод вчера."),
    ("take into account", "We need to take this fact into account.", "учесть", "Нужно учесть этот факт."),
    ("column", "The column is high.", "колонна", "Колонна высокая."),
    ("parliament", "The parliament accepted a new law.", "парламент", "Парламент принял новый закон."),
    ("cathedral", "The cathedral is old and big.", "собор", "Собор старый и большой."),
    ("to dance", "She loves to dance.", "танцевать", "Она любит танцевать."),
    ("foolishness", "This is foolishness.", "глупость", "Это глупость."),
    ("emotional", "This was an emotional day.", "эмоциональный", "Это был эмоциональный день."),
    ("transfer", "Please transfer the meeting to Friday.", "перенести", "Пожалуйста, перенесите встречу на пятницу."),
    ("town", "We visited a small town.", "городок", "Мы посетили маленький городок."),
    ("amateur", "He is an amateur.", "любитель", "Он любитель."),
    ("bar", "Let's meet at the bar.", "бар", "Давайте встретимся в баре."),
    ("decent", "He has a decent suit.", "приличный", "У него приличный костюм."),
    ("to be contained", "This information is contained in the letter.", "содержаться", "Эта информация содержится в письме."),
    ("review", "I read an interesting movie review.", "обзор", "Я прочитал интересный обзор фильма."),
    ("claim", "He has a claim to this house.", "претензия", "У него есть претензия на этот дом."),
    ("shirt", "I have a new shirt.", "рубашка", "У меня новая рубашка."),
    ("Italian", "I love Italian music.", "итальянский", "Я люблю итальянскую музыку."),
    ("yearning", "She felt a deep yearning for home.", "тоска", "Она чувствовала глубокую тоску по дому."),
    ("breakfast", "I eat bread for breakfast.", "завтрак", "Я ем хлеб на завтрак."),
    ("pension", "She has a small pension.", "пенсия", "У неё маленькая пенсия."),
    ("recovery", "His recovery took a month.", "восстановление", "Его восстановление заняло месяц."),
    ("tourist", "The tourist has a map.", "турист", "У туриста есть карта."),
    ("investor", "The investor looks at the market.", "инвестор", "Инвестор смотрит на рынок."),
    ("compare", "Let's compare the two books.", "сравнить", "Давайте сравним две книги."),
    ("fashion", "Fashion changes every year.", "мода", "Мода меняется каждый год."),
    ("mortgage", "They want to mortgage their house.", "заложить", "Они хотят заложить свой дом."),
    ("developer", "The developer wrote this program.", "разработчик", "Разработчик написал эту программу."),
    ("to draw", "I love to draw.", "рисовать", "Я люблю рисовать."),
    ("emergence", "The emergence of this idea is clear.", "возникновение", "Возникновение этой идеи ясно."),
    ("to be fooled", "I will not be fooled.", "вестись", "Я не буду вестись."),
    ("unity", "Unity is important.", "единство", "Единство важно."),
    ("foreigner", "The foreigner asked a question.", "иностранец", "Иностранец задал вопрос."),
    ("statistics", "Statistics show this fact.", "статистика", "Статистика показывает этот факт."),
    ("to warn", "I want to warn you.", "предупредить", "Я хочу предупредить вас."),
    ("to worry", "No need to worry about tomorrow.", "волноваться", "Не нужно волноваться о завтра."),
    ("musician", "The musician plays music.", "музыкант", "Музыкант играет музыку."),
    ("decade", "She lived in this city for a decade.", "десятилетие", "Она жила в этом городе десятилетие."),
    ("to shake", "I want to shake his hand.", "пожать", "Я хочу пожать ему руку."),
    ("realize", "She will realize the truth.", "осознать", "Она осознает правду."),
    ("brilliant", "This is a brilliant idea.", "блестящий", "Это блестящая идея."),
    ("killer", "The police will find the killer.", "убийца", "Полиция найдёт убийцу."),
    ("sad", "He felt sad today.", "печальный", "Он был печален сегодня."),
    ("improvement", "This is a significant improvement.", "улучшение", "Это значительное улучшение."),
    ("apple", "I eat an apple every morning.", "яблоко", "Я ем яблоко каждое утро."),
    ("to declare", "They declare this every year.", "заявлять", "Они заявляют это каждый год."),
    ("locality", "This locality is beautiful.", "местность", "Эта местность красива."),
    ("expedition", "The expedition is in the mountains.", "экспедиция", "Экспедиция в горах."),
    ("to earn", "She works to earn a salary.", "зарабатывать", "Она работает, чтобы зарабатывать зарплату."),
    ("progress", "We see progress today.", "прогресс", "Мы видим прогресс сегодня."),
    ("belt", "His belt is new.", "пояс", "Его пояс новый."),
    ("queen", "The queen is in the palace.", "королева", "Королева во дворце."),
    ("profitable", "This business can be profitable.", "выгодный", "Этот бизнес может быть выгодным."),
    ("old woman", "The old woman is in the room.", "старуха", "Старуха в комнате."),
    ("aerodrome", "We are at the aerodrome.", "аэродром", "Мы на аэродроме."),
    ("to share", "I love to share my stories.", "делиться", "Я люблю делиться своими историями."),
    ("react", "She will not react to the news.", "реагировать", "Она не будет реагировать на новости."),
    ("ally", "He became our ally.", "союзник", "Он стал нашим союзником."),
    ("reveal", "She will reveal the secret.", "раскрыть", "Она раскроет секрет."),
    ("corporation", "The corporation has a new name.", "корпорация", "У корпорации новое имя."),
    ("temporary", "This is a temporary solution.", "временный", "Это временное решение."),
    ("to tire of", "She began to tire of this work.", "надоесть", "Ей надоела эта работа."),
    ("detain", "The police will detain this man soon.", "задержать", "Полиция скоро задержит этого человека."),
    ("boot", "Her boot is new.", "сапог", "Её сапог новый."),
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


def en_ok(text: str) -> list[str]:
    bad = []
    for raw in re.findall(r"[A-Za-z']+", text):
        w = raw.lower().replace("'", "")
        if not w or w in allow_en or w == "tv":
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
