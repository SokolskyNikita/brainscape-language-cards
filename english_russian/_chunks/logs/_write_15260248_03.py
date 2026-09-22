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

SRC = PACK / "_chunks" / "deck_15260248_03.csv"
OUT = PACK / "_chunks" / "fixed" / "deck_15260248_03.csv"
LOG = PACK / "_chunks" / "logs" / "deck_15260248_03.txt"

FUNCTION_EN = {
    "a", "an", "the", "is", "be", "i", "you", "he", "she", "it", "we", "they",
    "my", "and", "or", "in", "on", "at", "to", "of", "for", "with", "from",
    "not", "his", "him", "her", "their", "them", "our", "us", "me", "am",
    "are", "was", "were", "been", "being", "this", "that", "these", "those",
    "as", "by", "into", "about", "than", "then", "so", "if", "but", "its",
    "your", "do", "does", "did", "will", "would", "can", "could", "may",
    "there", "here", "has", "had", "have",
}

FUNCTION_RU = {
    "и", "а", "или", "не", "ни", "но", "да", "же", "ли", "бы", "то", "это",
    "этот", "эта", "эти", "этой", "этом", "эту", "этих", "этим", "этими",
    "я", "ты", "он", "она", "оно", "мы", "вы", "они", "мой", "моя", "моё",
    "мои", "моего", "моей", "моём", "моим", "мою", "твой", "ваш", "наш",
    "его", "её", "их", "ему", "ей", "им", "ими", "меня", "мне", "меня",
    "тебя", "тебе", "нас", "нам", "вас", "вам", "себя", "себе", "собой",
    "в", "во", "на", "с", "со", "к", "ко", "у", "о", "об", "от", "до",
    "из", "за", "по", "под", "над", "при", "для", "без", "между", "через",
    "был", "была", "было", "были", "будет", "будут", "буду", "есть", "быть",
    "уже", "ещё", "также", "тоже", "только", "уже", "вот", "ведь", "ну",
}

allow_en = {
    line.strip().lower()
    for line in (PACK / "_vocab" / "allow_en_15260248.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_ru = {
    line.strip().replace("ё", "е").lower()
    for line in (PACK / "_vocab" / "allow_ru_15260248.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_en |= FUNCTION_EN
allow_ru |= FUNCTION_RU


# (en_lemma, en_ex, ru_lemma, ru_ex)
FIXED = [
    ("borrow", "I want to borrow this book.", "занять", "Я хочу занять эту книгу."),
    ("reader", "This reader likes the book.", "читатель", "Этот читатель любит книгу."),
    ("slowly", "He slowly opened the door.", "медленно", "Он медленно открыл дверь."),
    ("old man", "The old man is at the table.", "старик", "Старик за столом."),
    ("victory", "This is a great victory.", "победа", "Это великая победа."),
    ("element", "Water is an important element.", "элемент", "Вода — важный элемент."),
    ("naturally", "Naturally, he refused the offer.", "естественно", "Естественно, он отказался от предложения."),
    ("turn to", "I will turn to you for help.", "обратиться", "Я обращусь к вам за помощью."),
    ("permanent", "This change is permanent.", "постоянный", "Это изменение постоянное."),
    ("to meet", "We meet every day.", "встречаться", "Мы встречаемся каждый день."),
    ("female", "This is a female voice.", "женский", "Это женский голос."),
    ("commander", "The commander is at home.", "командир", "Командир дома."),
    ("August", "I was at home in August.", "август", "Я был дома в августе."),
    ("for the first time", "She was at home for the first time.", "впервые", "Она была дома впервые."),
    ("happy", "She is happy today.", "счастливый", "Она счастливая сегодня."),
    ("resident", "The resident loves this small city.", "житель", "Житель любит этот маленький город."),
    ("apparently", "Apparently, he is at home.", "видимо", "Видимо, он дома."),
    ("holiday", "Today is a national holiday.", "праздник", "Сегодня национальный праздник."),
    ("set", "This is a large set.", "множество", "Это большое множество."),
    ("sum", "I know this sum.", "сумма", "Я знаю эту сумму."),
    ("scene", "The last scene was good.", "сцена", "Последняя сцена была хорошей."),
    ("to eat", "I want to eat now.", "есть", "Я хочу есть сейчас."),
    ("hardly", "This is hardly possible.", "едва", "Это едва возможно."),
    ("preparation", "This preparation is important.", "подготовка", "Эта подготовка важна."),
    ("regret", "I feel deep regret.", "сожаление", "Я чувствую глубокое сожаление."),
    ("ear", "I hear with my ear.", "ухо", "Я слышу ухом."),
    ("historical", "This is a historical fact.", "исторический", "Это исторический факт."),
    ("existence", "I know about the existence of this.", "существование", "Я знаю о существовании этого."),
    ("urban", "This is an urban district.", "городской", "Это городской район."),
    ("October", "I was at home in October.", "октябрь", "Я был дома в октябре."),
    ("recently", "I was at home recently.", "недавно", "Я был дома недавно."),
    ("nose", "Her nose is red.", "нос", "Её нос красный."),
    ("creature", "This creature is alive.", "существо", "Это существо живое."),
    ("to possess", "She wants to possess knowledge.", "обладать", "Она хочет обладать знаниями."),
    ("frame", "The picture is in the frame.", "рамка", "Картина в рамке."),
    ("thanks to", "Thanks to you I am at home.", "благодаря", "Благодаря вам я дома."),
    ("French", "She loves French music.", "французский", "Она любит французскую музыку."),
    ("correctly", "He answered the question correctly.", "правильно", "Он правильно ответил на вопрос."),
    ("September", "School starts again in September.", "сентябрь", "Школа снова начинается в сентябре."),
    ("known", "This is known to me.", "известно", "Это известно мне."),
    ("left", "This is the left hand.", "левый", "Это левая рука."),
    ("university", "She studies at the university.", "университет", "Она учится в университете."),
    ("to be considered", "This work is considered important.", "считаться", "Эта работа считается важной."),
    ("private", "He owns a private island.", "частный", "У него есть частный остров."),
    ("deep", "The sea is very deep.", "глубокий", "Море очень глубокое."),
    ("club", "This is a new club.", "клуб", "Это новый клуб."),
    ("belong", "This book belongs to me.", "принадлежать", "Эта книга принадлежит мне."),
    ("rise", "The sun will rise tomorrow.", "подняться", "Солнце поднимется завтра."),
    ("summer", "I love summer.", "лето", "Я люблю лето."),
    ("to make", "He wanted to make her stay.", "заставить", "Он хотел заставить её остаться."),
    ("expression", "Her expression showed her feelings.", "выражение", "Её выражение показало её чувства."),
    ("to pay", "I want to pay for this.", "платить", "Я хочу платить за это."),
    ("calmly", "She calmly explained the situation.", "спокойно", "Она спокойно объяснила ситуацию."),
    ("clothing", "This is old clothing.", "одежда", "Это старая одежда."),
    ("sale", "The car is on sale today.", "продажа", "Машина сегодня в продаже."),
    ("saint", "This is her favorite saint.", "святой", "Это её любимый святой."),
    ("financial", "This is a financial problem.", "финансовый", "Это финансовая проблема."),
    ("December", "Snow always falls in December.", "декабрь", "Снег всегда идет в декабре."),
    ("theater", "We were at the theater.", "театр", "Мы были в театре."),
    ("build", "They want to build a new house.", "построить", "Они хотят построить новый дом."),
    ("village", "This village is small.", "деревня", "Эта деревня маленькая."),
    ("direct", "Please direct your attention to this.", "направить", "Пожалуйста, направьте ваше внимание на это."),
    ("to make up", "I want to make up a list.", "составить", "Я хочу составить список."),
    ("fund", "This is a large fund.", "фонд", "Это большой фонд."),
    ("sister", "My sister loves music.", "сестра", "Моя сестра любит музыку."),
    ("to differ", "Our opinions differ.", "отличаться", "Наши мнения отличаются."),
    ("carry", "I will carry the book.", "нести", "Я буду нести книгу."),
    ("shout", "He will shout for help.", "кричать", "Он будет кричать о помощи."),
    ("observe", "We will observe the stars this evening.", "наблюдать", "Мы будем наблюдать за звёздами сегодня вечером."),
    ("west", "The city is in the west.", "запад", "Город на западе."),
    ("refuse", "I refuse to answer that question.", "отказаться", "Я отказываюсь отвечать на этот вопрос."),
    ("circumstance", "This is an important circumstance.", "обстоятельство", "Это важное обстоятельство."),
    ("golden", "This is a golden color.", "золотой", "Это золотой цвет."),
    ("June", "School ends in June.", "июнь", "Школа заканчивается в июне."),
    ("to treat", "I treat her well.", "обращаться", "Я хорошо обращаюсь с ней."),
    ("version", "This is a new version.", "версия", "Это новая версия."),
    ("minister", "The minister wants a new policy.", "министр", "Министр хочет новую политику."),
    ("share", "I bought a share today.", "акция", "Я купил акцию сегодня."),
    ("lip", "This is her lip.", "губа", "Это её губа."),
    ("additional", "This is additional information.", "дополнительный", "Это дополнительная информация."),
    ("judge", "Do not judge her.", "судить", "Не судите её."),
    ("empty", "The room was completely empty.", "пустой", "Комната была совершенно пустой."),
    ("cold", "The water is very cold today.", "холодный", "Вода сегодня очень холодная."),
    ("February", "February is the shortest month.", "февраль", "Февраль - самый короткий месяц."),
    ("flower", "She received a beautiful flower.", "цветок", "Она получила красивый цветок."),
    ("central", "This is the central station.", "центральный", "Это центральная станция."),
    ("professional", "This is professional work.", "профессиональный", "Это профессиональная работа."),
    ("factory", "This factory is large.", "завод", "Этот завод большой."),
    ("federal", "This is the federal government.", "федеральный", "Это федеральное правительство."),
    ("federation", "This country is a large federation.", "федерация", "Эта страна — большая федерация."),
    ("technical", "This is a technical manual.", "технический", "Это техническое руководство."),
    ("feature", "The main feature is quality.", "особенность", "Главная особенность — качество."),
    ("understanding", "This understanding is important.", "понимание", "Это понимание важно."),
    ("wear", "I want to wear new clothing.", "носить", "Я хочу носить новую одежду."),
    ("birth", "I know about her birth.", "рождение", "Я знаю о её рождении."),
    ("disease", "This is a bad disease.", "болезнь", "Это плохая болезнь."),
    ("perform", "She will perform on stage this evening.", "выступать", "Она будет выступать на сцене сегодня вечером."),
    ("send", "Please send this letter today.", "отправить", "Пожалуйста, отправьте это письмо сегодня."),
    ("square", "I am at the square.", "площадь", "Я на площади."),
    ("occupy", "Books occupy this room.", "занимать", "Книги занимают эту комнату."),
]


def _en_ok(word: str) -> bool:
    w = word.lower()
    if w in allow_en:
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


def _ru_ok(word: str) -> bool:
    w = word.replace("ё", "е").lower()
    if w in allow_ru:
        return True
    for lemma in allow_ru:
        if len(lemma) < 3:
            continue
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
        for tok in re.findall(r"[A-Za-z']+", en_ex):
            if not _en_ok(tok):
                leftover.append(f"{i} EN {tok} :: {en_ex}")
        for tok in re.findall(r"[А-Яа-яЁё]+", ru_ex):
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
