#!/usr/bin/env python3
"""Rewrite english_russian deck_15260266_03 (cards 301-400)."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PACK = ROOT / "english_russian"
sys.path.insert(0, str(ROOT))

from brainscape.cards import card_write_payload, cards_from_path, cards_match
from english_russian._chunk_io import write_csv

SRC = PACK / "_chunks" / "deck_15260266_03.csv"
OUT = PACK / "_chunks" / "fixed" / "deck_15260266_03.csv"
LOG = PACK / "_chunks" / "logs" / "deck_15260266_03.txt"

FUNCTION_EN = {
    "a", "the", "is", "be", "i", "you", "he", "she", "it", "we", "they",
    "my", "and", "or", "in", "on", "at", "to", "of", "for", "with", "from",
    "not", "his", "him", "her", "their", "them", "our", "us", "me", "am",
    "are", "was", "were", "been", "being", "this", "that", "these", "those",
    "an", "as", "by", "into", "about", "than", "then", "so", "if", "but",
    "its", "your", "all", "no", "yes", "do", "does", "did", "done", "doing",
    "has", "have", "had", "having", "will", "would", "can", "could", "may",
    "might", "must", "shall", "should", "just", "also", "too", "very",
}

FUNCTION_RU = {
    w.replace("ё", "е")
    for w in {
        "я", "ты", "он", "она", "оно", "мы", "вы", "они", "меня", "тебя", "его",
        "её", "ее", "нас", "вас", "их", "мне", "тебе", "ему", "ей", "нам", "вам",
        "им", "мной", "мною", "тобой", "ним", "ней", "него", "нем", "нём", "ними",
        "неё", "нее",
        "собой", "мой", "моя", "моё", "мое", "мои", "твой", "твоя", "твоё", "твое",
        "твои", "свой", "своя", "своё", "свое", "свои", "наш", "наша", "наше",
        "наши", "ваш", "ваша", "ваше", "ваши", "этот", "эта", "это", "эти",
        "тот", "та", "то", "те", "такой", "такая", "такое", "такие", "весь",
        "вся", "всё", "все", "сам", "сама", "само", "сами", "быть", "есть",
        "был", "была", "было", "были", "буду", "будет", "будем", "будете",
        "будут", "нет", "не", "ни", "да", "уже", "ещё", "еще", "только", "даже",
        "тоже", "также", "очень", "так", "как", "что", "кто", "где", "когда",
        "почему", "куда", "который", "какой", "чтобы", "если", "потому", "ведь",
        "ли", "же", "бы", "вот", "здесь", "тут", "там", "теперь", "сейчас",
        "потом", "всегда", "никогда", "иногда", "от", "до", "по", "со", "из",
        "без", "при", "про", "об", "за", "над", "под", "перед", "после",
        "между", "через", "около", "для", "к", "у", "о", "в", "на", "с", "и",
        "а", "но", "или",
    }
}

# Keep original English glosses. Russian lemma kept unless noted.
# (ru_lemma, en_example, ru_example)
FIXED: list[tuple[str, str, str]] = [
    ("мистический", "The forest is mystical.", "Лес мистический."),
    ("возиться", "Do not fiddle with the pen.", "Не возись с ручкой."),
    ("синдром", "This is a new syndrome.", "Это новый синдром."),
    ("сияние", "I see a warm radiance.", "Я вижу тёплое сияние."),
    ("доктрина", "This is an old doctrine.", "Это старая доктрина."),
    ("истерика", "I see the crowd's hysteria.", "Я вижу истерику толпы."),
    ("штурман", "He is a navigator.", "Он штурман."),
    ("фланг", "The attack is from the flank.", "Атака с фланга."),
    ("жевать", "I like to chew.", "Я люблю жевать."),
    ("справедливо", "He speaks fairly.", "Он говорит справедливо."),
    ("глагол", "This word is a verb.", "Это слово — глагол."),
    ("горячо", "They hotly discuss the issue.", "Они горячо обсуждают вопрос."),
    ("открытка", "I have a beautiful postcard.", "У меня есть красивая открытка."),
    ("примета", "This is a bad omen.", "Это плохая примета."),
    ("электричка", "The electric train is here.", "Электричка здесь."),
    ("хм", "Hmm, that is an interesting idea.", "Хм, это интересная идея."),
    ("прощание", "This is our farewell.", "Это наше прощание."),
    ("лысый", "He is bald.", "Он лысый."),
    ("кружиться", "She likes to spin.", "Она любит кружиться."),
    ("пышный", "The garden is lush.", "Сад пышный."),
    ("предвыборный", "This is a pre-election day.", "Это предвыборный день."),
    ("цирк", "The circus is in the city.", "Цирк в городе."),
    ("почка", "He has one kidney.", "У него одна почка."),
    ("колючий", "The bush is very prickly.", "Куст очень колючий."),
    ("президиум", "The presidium is here.", "Президиум здесь."),
    ("клинический", "This is clinical work.", "Это клиническая работа."),
    ("новинка", "This is a novelty.", "Это новинка."),
    ("вознаграждение", "This is his reward.", "Это его вознаграждение."),
    ("старина", "I remember the old times.", "Я помню старину."),
    ("орех", "I like this nut.", "Мне нравится этот орех."),
    ("продумать", "We need to think through the plan.", "Нам нужно продумать план."),
    ("презрение", "I feel contempt.", "Я чувствую презрение."),
    ("спаситель", "He is their savior.", "Он их спаситель."),
    ("равнина", "The plain is large.", "Равнина большая."),
    ("подвергнуться", "He must undergo this.", "Ему нужно подвергнуться этому."),
    ("секта", "He joined a sect.", "Он вступил в секту."),
    ("присвоить", "He will assign a name.", "Он присвоит имя."),
    ("сбыт", "Sales are good this year.", "Сбыт в этом году хороший."),
    ("вой", "I hear a howl.", "Я слышу вой."),
    ("массаж", "I need a massage today.", "Мне нужен массаж сегодня."),
    ("злобный", "He is malicious.", "Он злобный."),
    ("горизонтальный", "This line is horizontal.", "Эта линия горизонтальная."),
    ("затянуться", "The year can drag on.", "Год может затянуться."),
    ("целостность", "The work has integrity.", "У работы есть целостность."),
    ("посылка", "I have a parcel today.", "У меня есть посылка сегодня."),
    ("пустынный", "The town is deserted.", "Город пустынный."),
    ("балтийский", "The Baltic Sea is very cold.", "Балтийское море очень холодное."),
    ("повестка", "The meeting agenda is full.", "Повестка встречи полная."),
    ("хакер", "The hacker is in the city.", "Хакер в городе."),
    ("катиться", "The stone will roll.", "Камень будет катиться."),
    ("дожить", "He will live out the year.", "Он доживёт этот год."),
    ("полярный", "This is a polar night.", "Это полярная ночь."),
    ("террор", "Terror is in the city.", "Террор в городе."),
    ("якорь", "The ship has an anchor.", "У корабля есть якорь."),
    ("уравнение", "Solve this equation.", "Решите это уравнение."),
    ("бакс", "I need fifty bucks.", "Мне нужно пятьдесят баксов."),
    ("согласовать", "We need to coordinate our plans.", "Нам нужно согласовать наши планы."),
    ("горечь", "I feel bitterness.", "Я чувствую горечь."),
    ("телесный", "This is bodily pain.", "Это телесная боль."),
    ("продюсер", "He is a producer.", "Он продюсер."),
    ("месть", "She needs revenge.", "Ей нужна месть."),
    ("католический", "This is a Catholic church.", "Это католическая церковь."),
    ("счастливо", "They live happily.", "Они живут счастливо."),
    ("покраснеть", "She will blush.", "Она покраснеет."),
    ("пролетариат", "The proletariat is large.", "Пролетариат большой."),
    ("география", "I like geography.", "Я люблю географию."),
    ("архитектурный", "This is an architectural style.", "Это архитектурный стиль."),
    ("гимназия", "She is in the gymnasium.", "Она в гимназии."),
    ("усвоить", "He will assimilate this.", "Он усвоит это."),
    ("сборная", "The national team is here.", "Сборная здесь."),
    ("банда", "The gang is in the city.", "Банда в городе."),
    ("демократ", "He is a proud democrat.", "Он гордый демократ."),
    ("помеха", "This is a new interference.", "Это новая помеха."),
    ("растеряться", "I do not want to get confused.", "Я не хочу растеряться."),
    ("крейсер", "The cruiser is at sea.", "Крейсер в море."),
    ("египетский", "I see an Egyptian pyramid.", "Я вижу египетскую пирамиду."),
    ("аплодисменты", "I hear applause.", "Я слышу аплодисменты."),
    ("вероятный", "Rain tomorrow is probable.", "Дождь завтра вероятен."),
    ("генетический", "This is a genetic problem.", "Это генетическая проблема."),
    ("безработица", "Unemployment is high.", "Безработица высокая."),
    ("объективно", "I want to speak objectively.", "Я хочу говорить объективно."),
    ("вычислительный", "This is computational work.", "Это вычислительная работа."),
    ("горький", "The coffee is bitter.", "Кофе горький."),
    ("мирно", "She lives peacefully.", "Она живёт мирно."),
    ("поздравление", "This is a congratulation.", "Это поздравление."),
    ("разом", "They did this at once.", "Они сделали это разом."),
    ("социологический", "This is a sociological study.", "Это социологическое исследование."),
    ("конструктивный", "This is a constructive idea.", "Это конструктивная идея."),
    ("митрополит", "The metropolitan is here today.", "Митрополит сегодня здесь."),
    ("сочинять", "She likes to compose.", "Она любит сочинять."),
    ("солдатский", "This is a soldier's house.", "Это солдатский дом."),
    ("благосостояние", "They want welfare.", "Они хотят благосостояния."),
    ("кавказский", "These are Caucasian mountains.", "Это кавказские горы."),
    ("фальшивый", "This is a fake smile.", "Это фальшивая улыбка."),
    ("грант", "She has a grant.", "У неё есть грант."),
    ("выраженный", "The idea is clearly expressed.", "Идея ясно выражена."),
    ("расстроить", "The news upset me.", "Новость меня расстроила."),
    ("жюри", "The jury will evaluate the work.", "Жюри оценит работу."),
    ("крем", "I need cream for my face.", "Мне нужен крем для лица."),
    ("достоверный", "The source is reliable.", "Источник достоверный."),
]


allow_en = {
    line.strip().lower()
    for line in (PACK / "_vocab" / "allow_en_15260266.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
} | FUNCTION_EN
allow_ru = {
    line.strip().replace("ё", "е").lower()
    for line in (PACK / "_vocab" / "allow_ru_15260266.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
} | FUNCTION_RU


def en_forms(word: str) -> list[str]:
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


def en_ok(text: str, extra: set[str]) -> list[str]:
    bad = []
    for raw in re.findall(r"[A-Za-z']+", text):
        w = raw.lower().replace("'", "")
        if not w or w in allow_en or w in extra:
            continue
        if any(form in allow_en or form in extra for form in en_forms(w)):
            continue
        if w.endswith("ly") and w[:-2] + "l" in allow_en:
            continue
        for lemma in allow_en | extra:
            parts = lemma.replace("-", " ").split()
            if w in parts:
                break
        else:
            bad.append(raw)
    return bad


RU_IRREG = {
    "пить": ("пь",),
    "есть": ("ед", "еш", "ем", "ел"),
    "идти": ("ид", "шл", "ше"),
    "пойти": ("пой", "пош"),
    "мочь": ("мож", "мог"),
    "учить": ("уч",),
    "взять": ("возьм", "взя"),
    "хотеть": ("хоч", "хот"),
    "жить": ("жив",),
    "видеть": ("виж", "вид"),
    "говорить": ("говор",),
}


def ru_ok(text: str, extra: set[str]) -> list[str]:
    bad = []
    pool = allow_ru | extra
    for raw in re.findall(r"[А-Яа-яЁё-]+", text):
        w = raw.replace("ё", "е").replace("Ё", "е").lower()
        if w in pool:
            continue
        if any(
            w.startswith(lemma) or lemma.startswith(w)
            for lemma in pool
            if len(lemma) >= 3 and len(w) >= 3
        ):
            continue
        if any(
            w[:3] == lemma[:3]
            for lemma in pool
            if len(lemma) >= 3 and len(w) >= 3
        ):
            continue
        if any(
            lemma in pool and any(w.startswith(stem) for stem in stems)
            for lemma, stems in RU_IRREG.items()
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


def lemma_in_en(gloss: str, example: str) -> bool:
    g = gloss.lower()
    ex = example.lower()
    if g in ex:
        return True
    key = re.sub(r"^(to |the |a |an )", "", g)
    if key in ex:
        return True
    parts = [p for p in key.replace("-", " ").split() if p not in {"to", "the", "a", "an", "be"}]
    return all(p in ex for p in parts) if parts else False


def lemma_in_ru(lemma: str, example: str) -> bool:
    key = lemma.lower().replace("ё", "е")
    ex = example.lower().replace("ё", "е")
    if key in ex:
        return True
    if len(key) >= 4 and key[:4] in ex:
        return True
    if len(key) >= 5 and key[:5] in ex:
        return True
    return False


def main() -> None:
    originals = cards_from_path(SRC)
    if len(originals) != 100 or len(FIXED) != 100:
        raise SystemExit(f"expected 100, got {len(originals)} / {len(FIXED)}")

    cards = []
    leftover = []
    for i, (ru, en_ex, ru_ex) in enumerate(FIXED, 1):
        orig = originals[i - 1]
        en = orig["qMdBody"]
        extra_en = set(re.findall(r"[a-z']+", en.lower()))
        extra_en |= set(en.lower().replace("-", " ").split())
        extra_ru = {w.replace("ё", "е").lower() for w in re.findall(r"[А-Яа-яЁё-]+", ru)}
        for token in en_ok(en_ex, extra_en):
            leftover.append(f"{i} EN leftover {token!r}: {en_ex}")
        for token in ru_ok(ru_ex, extra_ru):
            leftover.append(f"{i} RU leftover {token!r}: {ru_ex}")
        if not lemma_in_en(en, en_ex):
            leftover.append(f"{i}: EN example missing {en!r}")
        if not lemma_in_ru(ru, ru_ex):
            leftover.append(f"{i}: RU example missing {ru!r}")
        cards.append(make_card(en, en_ex, ru, ru_ex))

    write_csv(OUT, cards)
    loaded = cards_from_path(OUT)
    if len(loaded) != 100:
        raise SystemExit(f"cards_from_path returned {len(loaded)}")

    changed = sum(1 for a, b in zip(originals, loaded) if not cards_match(a, b))
    LOG.parent.mkdir(parents=True, exist_ok=True)
    LOG.write_text(f"{changed}\n", encoding="utf-8")
    print(f"wrote {OUT}")
    print(f"cards_from_path={len(loaded)}")
    print(f"changed={changed}")
    if leftover:
        print("LEFTOVER / CHECKS:")
        print("\n".join(leftover))
    else:
        print("vocab check clean")


if __name__ == "__main__":
    main()
