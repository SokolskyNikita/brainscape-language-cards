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

SRC = PACK / "_chunks" / "deck_15260255_04.csv"
OUT = PACK / "_chunks" / "fixed" / "deck_15260255_04.csv"
LOG = PACK / "_chunks" / "logs" / "deck_15260255_04.txt"

FUNCTION = {
    "a", "the", "is", "be", "i", "you", "he", "she", "it", "we", "they",
    "my", "and", "or", "in", "on", "at", "to", "of", "for", "with", "from",
    "not", "his", "him", "her", "their", "them", "our", "us", "me", "am",
    "are", "was", "were", "been", "being", "this", "that", "these", "those",
    "an", "as", "by", "into", "about", "than", "then", "so", "if", "but",
    "its", "your", "has", "had", "did", "does", "will", "can", "could",
    "should", "would", "must", "do", "have", "no", "yes", "there", "here",
    "up", "down", "out", "over", "after", "before", "now", "all", "some",
    "any", "more", "most", "other", "such", "also", "only", "just", "very",
    "too", "when", "where", "who", "what", "which", "how", "why",
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
    ("argument", "This is a strong argument.", "аргумент", "Это сильный аргумент."),
    ("fabric", "This fabric is soft.", "ткань", "Эта ткань мягкая."),
    ("to be preserved", "The old house was preserved.", "сохраниться", "Старый дом сохранился."),
    ("survive", "We will survive this war together.", "пережить", "Мы вместе переживём эту войну."),
    ("warehouse", "The warehouse stores many goods.", "склад", "На складе много товаров."),
    ("egg", "I need an egg.", "яйцо", "Мне нужно яйцо."),
    ("trust", "Trust is important.", "доверие", "Доверие важно."),
    ("gentle", "Her voice is gentle.", "нежный", "Её голос нежный."),
    ("throat", "His throat is dry.", "горло", "У него сухое горло."),
    ("to teach", "I want to teach him.", "научить", "Я хочу научить его."),
    ("to designate", "They designated this house for guests.", "предназначить", "Они предназначили этот дом для гостей."),
    ("format", "Choose the right format.", "формат", "Выберите правильный формат."),
    ("British", "He is a British writer.", "британский", "Он британский писатель."),
    ("cover", "Snow will cover the city.", "покрыть", "Снег покроет город."),
    ("spend", "I will spend time at home.", "тратить", "Я буду тратить время дома."),
    ("existing", "This is the existing plan.", "существующий", "Это существующий план."),
    ("lawyer", "I see my lawyer today.", "адвокат", "Я вижу своего адвоката сегодня."),
    ("experienced", "She is an experienced teacher.", "опытный", "Она опытный учитель."),
    ("gun", "He has a gun.", "пистолет", "У него есть пистолет."),
    ("industrial", "This is an industrial city.", "промышленный", "Это промышленный город."),
    ("teenager", "The teenager is at home.", "подросток", "Подросток дома."),
    ("bomb", "They found a bomb.", "бомба", "Они нашли бомбу."),
    ("tower", "The tower is high.", "башня", "Башня высокая."),
    ("towards", "She walked towards him.", "навстречу", "Она шла ему навстречу."),
    ("socially", "She is socially active.", "социально", "Она социально активна."),
    ("hostess", "The hostess opened the door.", "хозяйка", "Хозяйка открыла дверь."),
    ("deliver", "Please deliver this letter tomorrow.", "доставить", "Пожалуйста, доставьте это письмо завтра."),
    ("pull out", "I will pull out the book.", "вытащить", "Я вытащу книгу."),
    ("wealth", "He has great wealth.", "богатство", "У него большое богатство."),
    ("to be needed", "This book will be needed tomorrow.", "понадобиться", "Эта книга понадобится завтра."),
    ("supreme", "The supreme court is important.", "верховный", "Верховный суд важен."),
    ("motive", "His motive is clear.", "мотив", "Его мотив ясный."),
    ("defeat", "They faced defeat with dignity.", "поражение", "Они приняли поражение с достоинством."),
    ("toilet", "The toilet is near the door.", "туалет", "Туалет рядом с дверью."),
    ("preserve", "We want to preserve this house.", "сохранять", "Мы хотим сохранять этот дом."),
    ("alarm", "I hear the alarm.", "тревога", "Я слышу тревогу."),
    ("to dial", "I need to dial her number.", "набрать", "Мне нужно набрать её номер."),
    ("protect", "They will protect the guests.", "защитить", "Они защитят гостей."),
    ("expensive", "This car is very expensive.", "дорогой", "Эта машина очень дорогая."),
    ("cruel", "Life is cruel sometimes.", "жестокий", "Жизнь иногда жестокая."),
    ("firmly", "He closed the door firmly.", "крепко", "Он крепко закрыл дверь."),
    ("to decide", "She decided to go.", "решиться", "Она решилась пойти."),
    ("deprive", "They want to deprive him of his house.", "лишить", "Они хотят лишить его дома."),
    ("administrative", "This is an administrative task.", "административный", "Это административная задача."),
    ("tremble", "He trembles from the cold.", "дрожать", "Он дрожит от холода."),
    ("fruit", "This fruit is good.", "плод", "Этот плод хороший."),
    ("vessel", "The vessel is large.", "судно", "Судно большое."),
    ("to live", "They live in this city.", "проживать", "Они проживают в этом городе."),
    ("independently", "She works independently.", "самостоятельно", "Она работает самостоятельно."),
    ("subsequently", "He subsequently left home.", "впоследствии", "Он впоследствии ушёл из дома."),
    ("dialogue", "The movie's dialogue was long.", "диалог", "Диалог в фильме был длинным."),
    ("to smell", "These flowers smell good.", "пахнуть", "Эти цветы хорошо пахнут."),
    ("start talking", "He started talking suddenly.", "заговорить", "Он вдруг заговорил."),
    ("wedding", "Their wedding was beautiful.", "свадьба", "Их свадьба была красивой."),
    ("fog", "The fog hides the sun.", "туман", "Туман скрывает солнце."),
    ("delight", "I feel delight.", "восторг", "Я чувствую восторг."),
    ("emphasize", "I want to emphasize this.", "подчеркнуть", "Я хочу подчеркнуть это."),
    ("lord", "The lord is in the house.", "лорд", "Лорд в доме."),
    ("accuracy", "Accuracy is important.", "точность", "Точность важна."),
    ("to transform", "Water transforms into snow.", "превращаться", "Вода превращается в снег."),
    ("staff", "The staff is at work.", "персонал", "Персонал на работе."),
    ("exclaim", "She will exclaim in surprise.", "воскликнуть", "Она воскликнет от удивления."),
    ("major", "The major is in the army.", "майор", "Майор в армии."),
    ("to evaluate", "They evaluate the work.", "оценивать", "Они оценивают работу."),
    ("turn around", "Please turn around slowly.", "обернуться", "Пожалуйста, обернитесь медленно."),
    ("to ring out", "A voice will ring out.", "раздаться", "Голос раздастся."),
    ("operator", "The operator answered the call.", "оператор", "Оператор ответил на звонок."),
    ("constitution", "The constitution defines the law.", "конституция", "Конституция определяет закон."),
    ("card", "This is my bank card.", "карточка", "Это моя банковская карточка."),
    ("analogous", "Their situations are analogous.", "аналогичный", "Их ситуации аналогичны."),
    ("pregnancy", "This is her first pregnancy.", "беременность", "Это её первая беременность."),
    ("to keep", "I keep his letters.", "хранить", "Я храню его письма."),
    ("researcher", "The researcher published her book.", "исследователь", "Исследователь опубликовала свою книгу."),
    ("to disappear", "They disappear at night.", "исчезать", "Они исчезают ночью."),
    ("Frenchman", "The Frenchman loves tea.", "француз", "Француз любит чай."),
    ("married", "She wants to get married.", "замуж", "Она хочет выйти замуж."),
    ("toy", "The boy has a toy.", "игрушка", "У мальчика есть игрушка."),
    ("merrily", "They talked merrily.", "весело", "Они весело говорили."),
    ("season", "Winter is my favorite season.", "сезон", "Зима — мой любимый сезон."),
    ("formula", "The formula solved the complex problem.", "формула", "Формула решила сложную проблему."),
    ("consideration", "The plan is under consideration.", "рассмотрение", "План на рассмотрении."),
    ("to look in", "I will look in tomorrow morning.", "заглянуть", "Я загляну завтра утром."),
    ("Don", "The Don is a long river.", "дон", "Дон — длинная река."),
    ("fist", "He raised his fist.", "кулак", "Он поднял кулак."),
    ("physics", "He studies physics.", "физика", "Он учит физику."),
    ("universal", "This is a universal law.", "всеобщий", "Это всеобщий закон."),
    ("violence", "Violence solves nothing.", "насилие", "Насилие ничего не решает."),
    ("gesture", "He will make a gesture.", "жест", "Он сделает жест."),
    ("initial", "Return to the initial plan.", "исходный", "Вернитесь к исходному плану."),
    ("to force", "They will force him to leave.", "вынудить", "Они вынудят его уйти."),
    ("Englishman", "The Englishman loves tea.", "англичанин", "Англичанин любит чай."),
    ("brigade", "The brigade did their task.", "бригада", "Бригада сделала свою задачу."),
    ("challenge", "This is a real challenge.", "вызов", "Это настоящий вызов."),
    ("drop", "This is a drop of water.", "капля", "Это капля воды."),
    ("laboratory", "She works in a laboratory.", "лаборатория", "Она работает в лаборатории."),
    ("salvation", "Hope is their only salvation.", "спасение", "Надежда — их спасение."),
    ("immediate", "He is my immediate director.", "непосредственный", "Он мой непосредственный директор."),
    ("half an hour", "I will be ready in half an hour.", "полчаса", "Я буду готов через полчаса."),
    ("shelf", "Put the book on the shelf.", "полка", "Поставь книгу на полку."),
    ("passport", "This is my passport.", "паспорт", "Это мой паспорт."),
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
        if any(
            w[: max(4, len(w) - 3)] == lemma[: max(4, len(w) - 3)]
            for lemma in allow_ru
            if abs(len(lemma) - len(w)) <= 4 and min(len(lemma), len(w)) >= 4
        ):
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
