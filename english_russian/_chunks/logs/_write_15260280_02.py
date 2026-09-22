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

SRC = PACK / "_chunks" / "deck_15260280_02.csv"
OUT = PACK / "_chunks" / "fixed" / "deck_15260280_02.csv"
LOG = PACK / "_chunks" / "logs" / "deck_15260280_02.txt"

FUNCTION_EN = {
    "a", "an", "the", "is", "be", "i", "you", "he", "she", "it", "we", "they",
    "my", "and", "or", "in", "on", "at", "to", "of", "for", "with", "from",
    "not", "his", "him", "her", "their", "them", "our", "us", "me", "am",
    "are", "was", "were", "been", "being", "this", "that", "these", "those",
    "as", "by", "into", "about", "than", "then", "so", "if", "but", "its",
    "your", "do", "does", "did", "will", "would", "can", "could", "may",
    "there", "here", "has", "had", "have", "don't", "dont", "let's", "lets",
    "all", "off", "done", "no",
    "myself", "yourself", "himself", "herself", "itself", "ourselves",
    "yourselves", "themselves", "oneself",
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

# New lemmas introduced by POS / sense corrections (taught on this card).
allow_ru |= {"волгоград", "голливуд", "владимир", "вологда"}

# (en_lemma, en_ex, ru_lemma, ru_ex)
FIXED = [
    ("paratrooper", "The paratrooper landed behind enemy lines.", "десантник", "Десантник сел за вражескими линиями."),
    ("deliverance", "Prayer brought her deliverance.", "избавление", "Молитва принесла ей избавление."),
    ("auditor", "The auditor is in the company.", "аудитор", "Аудитор в компании."),
    ("to ask for it", "He is asking for it.", "напрашиваться", "Он напрашивается на это."),
    ("edge of a forest", "We stood at the edge of a forest.", "опушка", "Мы стояли на опушке леса."),
    ("commonwealth", "This country is part of the Commonwealth.", "содружество", "Эта страна - часть Содружества."),
    ("Communist Party", "He is in the Communist Party.", "компартия", "Он в компартии."),
    ("pebble", "I found a smooth pebble.", "камешек", "Я нашёл гладкий камешек."),
    ("Volgograd", "I was in Volgograd.", "Волгоград", "Я был в Волгограде."),
    ("to feel nauseous", "I feel nauseous in the car.", "тошнить", "Меня тошнит в машине."),
    ("ferocious", "The ferocious dog is here.", "свирепый", "Свирепая собака здесь."),
    ("blast furnace", "The blast furnace is old.", "доменная печь", "Доменная печь старая."),
    ("floral", "She has a floral dress.", "цветочный", "У неё цветочное платье."),
    ("pronunciation", "Her pronunciation is good.", "произношение", "Её произношение хорошее."),
    ("drown", "He tried to drown the rat.", "утопить", "Он пытался утопить крысу."),
    ("to distinguish oneself", "He wants to distinguish himself.", "отличиться", "Он хочет отличиться."),
    ("to calm down", "He is calming down.", "успокаиваться", "Он успокаивается."),
    ("to stumble", "He will stumble in the dark.", "споткнуться", "Он споткнётся в темноте."),
    ("projection", "The projection of the movie is clear.", "проекция", "Проекция фильма ясная."),
    ("little horse", "The little horse runs.", "лошадка", "Лошадка бежит."),
    ("wardrobe", "Her wardrobe is large.", "гардероб", "Её гардероб большой."),
    ("ashtray", "Put it in the ashtray.", "пепельница", "Поставь это в пепельницу."),
    ("to fail", "He fails at work.", "проваливаться", "Он проваливается на работе."),
    ("airline", "This airline is new.", "авиакомпания", "Эта авиакомпания новая."),
    ("wolf's", "This is a wolf's track.", "волчий", "Это волчий след."),
    ("hallucination", "He had a hallucination.", "галлюцинация", "У него была галлюцинация."),
    ("scratch", "I need to scratch my hand.", "почесать", "Мне нужно почесать руку."),
    ("wallet", "I lost my wallet.", "бумажник", "Я потерял бумажник."),
    ("to jerk", "He jerked to the door.", "рвануться", "Он рванулся к двери."),
    ("Hollywood", "I was in Hollywood.", "Голливуд", "Я был в Голливуде."),
    ("inevitability", "I see the inevitability of this.", "неизбежность", "Я вижу неизбежность этого."),
    ("disperse", "The wind will disperse the clouds.", "рассеять", "Ветер рассеет облака."),
    ("nostalgia", "I feel nostalgia.", "ностальгия", "Я чувствую ностальгию."),
    ("to plug", "He will plug the hole.", "заткнуть", "Он заткнёт дыру."),
    ("moss", "There is moss on the stone.", "мох", "На камне есть мох."),
    ("parting", "I do not want this parting.", "расставание", "Я не хочу этого расставания."),
    ("hieroglyph", "I see a hieroglyph.", "иероглиф", "Я вижу иероглиф."),
    ("to rape", "He tried to rape her.", "изнасиловать", "Он пытался её изнасиловать."),
    ("adjustment", "The machine needs an adjustment.", "корректировка", "Машине нужна корректировка."),
    ("caprice", "This is only a caprice.", "каприз", "Это только каприз."),
    ("objectivity", "I need objectivity here.", "объективность", "Мне нужна объективность здесь."),
    ("coziness", "I like the coziness of this house.", "уют", "Мне нравится уют этого дома."),
    ("audit", "We will prepare the audit.", "аудит", "Мы подготовим аудит."),
    ("excessively", "He drinks coffee excessively.", "чрезмерно", "Он чрезмерно пьёт кофе."),
    ("insurer", "The insurer pays.", "страховщик", "Страховщик платит."),
    ("revive", "The street will revive at night.", "оживиться", "Улица оживится ночью."),
    ("redistribution", "They want a redistribution of land.", "перераспределение", "Они хотят перераспределение земли."),
    ("Vladimir", "Vladimir lives here.", "Владимир", "Владимир живёт здесь."),
    ("aiming", "Aiming takes time.", "наведение", "Наведение занимает время."),
    ("Vologda", "I was in Vologda.", "Вологда", "Я был в Вологде."),
    ("bodyguard", "He has a bodyguard.", "телохранитель", "У него есть телохранитель."),
    ("relevance", "I see the relevance of this.", "актуальность", "Я вижу актуальность этого."),
    ("gossip", "She likes gossip.", "сплетня", "Ей нравятся сплетни."),
    ("Marxist", "This is a Marxist book.", "марксистский", "Это марксистская книга."),
    ("mound", "There is a mound near the house.", "бугор", "У дома есть бугор."),
    ("to be added", "Sugar is to be added now.", "добавляться", "Сахар добавляется сейчас."),
    ("cellar", "We store wine in the cellar.", "погреб", "Мы храним вино в погребе."),
    ("abstraction", "This is only an abstraction.", "абстракция", "Это только абстракция."),
    ("to fix", "I need to fix my bicycle.", "починить", "Мне нужно починить велосипед."),
    ("insomnia", "She has insomnia.", "бессонница", "У неё бессонница."),
    ("mastery", "Mastery of the language takes time.", "овладение", "Овладение языком занимает время."),
    ("to stick out", "He will stick out of the window.", "высунуться", "Он высунется из окна."),
    ("maliciously", "He smiled maliciously.", "злобно", "Он злобно улыбнулся."),
    ("hang over", "Clouds hang over the house.", "нависнуть", "Над домом нависли облака."),
    ("phoenix", "The phoenix is a bird.", "феникс", "Феникс - это птица."),
    ("mosaic", "I see a beautiful mosaic.", "мозаика", "Я вижу красивую мозаику."),
    ("to get wet", "I will get wet without a coat.", "промокнуть", "Я промокну без пальто."),
    ("elastic", "This material is elastic.", "упругий", "Этот материал упругий."),
    ("Far Eastern", "This is Far Eastern land.", "дальневосточный", "Это дальневосточная земля."),
    ("bloodstained", "This is a bloodstained knife.", "окровавленный", "Это окровавленный нож."),
    ("conception", "Conception was in the spring.", "зачатие", "Зачатие было весной."),
    ("decency", "He has no decency.", "приличие", "У него нет приличия."),
    ("invariable", "This law is invariable.", "неизменный", "Этот закон неизменен."),
    ("lad", "The lad is here.", "парнишка", "Парнишка здесь."),
    ("nightingale", "The nightingale sings at night.", "соловей", "Соловей поёт ночью."),
    ("dam", "The dam is on the river.", "плотина", "Плотина на реке."),
    ("reminder", "I have a reminder.", "напоминание", "У меня есть напоминание."),
    ("to last", "The meeting will last an hour.", "продлиться", "Встреча продлится час."),
    ("to exaggerate", "Do not exaggerate this.", "преувеличивать", "Не преувеличивай это."),
    ("scissors", "I need scissors to cut paper.", "ножницы", "Мне нужны ножницы, чтобы резать бумагу."),
    ("listen to", "Listen to this song.", "прослушать", "Прослушай эту песню."),
    ("homeless", "He is homeless.", "бездомный", "Он бездомный."),
    ("regardless", "Regardless of the weather, we will go.", "невзирая", "Невзирая на погоду, мы пойдём."),
    ("overseer", "The overseer is strict.", "надзиратель", "Надзиратель строгий."),
    ("inn", "We stayed at a cozy inn.", "трактир", "Мы остановились в уютном трактире."),
    ("pump", "The pump is old.", "насос", "Насос старый."),
    ("speaking", "This is a speaking parrot.", "говорящий", "Это говорящий попугай."),
    ("little shop", "I found a little shop.", "магазинчик", "Я нашёл магазинчик."),
    ("meanness", "I see his meanness.", "подлость", "Я вижу его подлость."),
    ("crib", "The baby sleeps in the crib.", "кроватка", "Младенец спит в кроватке."),
    ("puzzle", "His question will puzzle her.", "озадачить", "Его вопрос её озадачит."),
    ("mist", "The mist is over the river.", "дымка", "Дымка над рекой."),
    ("radically", "This is radically new.", "радикально", "Это радикально новое."),
    ("to send out", "We need to send out letters.", "высылать", "Нам нужно высылать письма."),
    ("to break off", "The call will break off.", "оборваться", "Звонок оборвётся."),
    ("preventive", "This is a preventive measure.", "профилактический", "Это профилактическая мера."),
    ("hoarse", "His voice is hoarse.", "хриплый", "Его голос хриплый."),
    ("to stick in", "He will stick in the key.", "воткнуть", "Он воткнёт ключ."),
    ("to master", "He is mastering the language.", "овладевать", "Он овладевает языком."),
    ("unreasonable", "His demands are unreasonable.", "неразумный", "Его требования неразумны."),
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
    "stood": "stand",
    "lost": "lose",
    "felt": "feel",
    "left": "leave",
    "paid": "pay",
    "landed": "land",
    "brought": "bring",
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
    "сел": "сесть",
    "стоит": "стоять",
    "стояли": "стоять",
    "пьет": "пить",
    "пьёт": "пить",
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
        else:
            print(f"UNCHANGED {i}: {en_lemma}")
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
