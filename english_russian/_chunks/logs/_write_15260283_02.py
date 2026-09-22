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

SRC = PACK / "_chunks" / "deck_15260283_02.csv"
OUT = PACK / "_chunks" / "fixed" / "deck_15260283_02.csv"
LOG = PACK / "_chunks" / "logs" / "deck_15260283_02.txt"

FUNCTION_EN = {
    "a", "an", "the", "is", "be", "i", "you", "he", "she", "it", "we", "they",
    "my", "and", "or", "in", "on", "at", "to", "of", "for", "with", "from",
    "not", "his", "him", "her", "their", "them", "our", "us", "me", "am",
    "are", "was", "were", "been", "being", "this", "that", "these", "those",
    "as", "by", "into", "about", "than", "then", "so", "if", "but", "its",
    "your", "do", "does", "did", "will", "would", "can", "could", "may",
    "there", "here", "has", "had", "have", "don't", "dont", "let's", "lets",
    "all", "off", "done", "myself", "yourself", "himself", "herself",
    "itself", "ourselves", "themselves", "one's", "ones",
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
    for line in (PACK / "_vocab" / "allow_en_15260283.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_ru = {
    line.strip().replace("ё", "е").lower()
    for line in (PACK / "_vocab" / "allow_ru_15260283.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_en |= FUNCTION_EN
allow_ru |= FUNCTION_RU

# New lemmas introduced by POS / translation corrections (taught on this card).
allow_ru |= {"беспрепятственный", "убаюкать", "лунный свет"}

# (en_lemma, en_ex, ru_lemma, ru_ex)
FIXED = [
    ("typo", "I found a typo in the letter.", "опечатка", "Я нашёл опечатку в письме."),
    ("stepfather", "My stepfather is very kind.", "отчим", "Мой отчим очень добрый."),
    ("analog", "I prefer analog watches to digital.", "аналоговый", "Я предпочитаю аналоговые часы цифровым."),
    ("remembrance", "I was at the remembrance.", "помин", "Я был на помине."),
    ("unmarried", "He is still unmarried.", "холостой", "Он всё ещё холостой."),
    ("scepter", "The king held a scepter.", "жезл", "Король держал жезл."),
    ("hawk", "I see a hawk in the sky.", "ястреб", "Я вижу ястреба в небе."),
    ("mediation", "They need mediation.", "посредничество", "Им надо посредничество."),
    ("moonlight", "The moonlight was bright.", "лунный свет", "Лунный свет был ярким."),
    ("mutilate", "They did not mutilate him.", "изуродовать", "Они не изуродовали его."),
    ("zeal", "She works with great zeal.", "рвение", "Она работает с большим рвением."),
    ("rehearse", "We must rehearse now.", "репетировать", "Мы должны репетировать сейчас."),
    ("counterintelligence", "He works in counterintelligence.", "контрразведка", "Он работает в контрразведке."),
    ("otherworldly", "Her voice was otherworldly.", "неземной", "Её голос был неземным."),
    ("exaggerate", "He likes to exaggerate.", "преувеличить", "Он любит преувеличивать."),
    ("cuckoo", "I hear a cuckoo.", "кукушка", "Я слышу кукушку."),
    ("son of a bitch", "He is a real son of a bitch.", "сукин сын", "Он настоящий сукин сын."),
    ("cowardly", "He is a cowardly man.", "трусливый", "Он трусливый человек."),
    ("boatswain", "The boatswain shouted loudly.", "боцман", "Боцман кричал громко."),
    ("cripple", "War made him a cripple.", "калека", "Война сделала его калекой."),
    ("megapolis", "This city is a megapolis.", "мегаполис", "Этот город — мегаполис."),
    ("unhindered", "The path was unhindered.", "беспрепятственный", "Путь был беспрепятственным."),
    ("boutique", "She opened a boutique.", "бутик", "Она открыла бутик."),
    ("lively", "The market was lively.", "бойкий", "Рынок был бойким."),
    ("accomplishment", "This was a great accomplishment.", "свершение", "Это было великое свершение."),
    ("reverence", "She felt reverence.", "благоговение", "Она чувствовала благоговение."),
    ("to program", "I need to program this machine.", "запрограммировать", "Мне нужно запрограммировать эту машину."),
    ("aristocracy", "The aristocracy had power.", "аристократия", "Аристократия имела власть."),
    ("underestimate", "Do not underestimate him.", "недооценивать", "Не недооценивай его."),
    ("hermit", "The hermit lived in the forest.", "отшельник", "Отшельник жил в лесу."),
    ("hijack", "They hijack the ship.", "угонять", "Они угоняют корабль."),
    ("picket", "Workers held a picket.", "пикет", "Рабочие держали пикет."),
    ("idler", "He is an idler.", "бездельник", "Он бездельник."),
    ("stupidity", "This is stupidity.", "тупость", "Это тупость."),
    ("denomination", "He chose another denomination.", "конфессия", "Он выбрал другую конфессию."),
    ("ironic", "This is an ironic story.", "иронический", "Это ироническая история."),
    ("vouch", "I can vouch for him.", "ручаться", "Я могу ручаться за него."),
    ("to bolt", "He decided to bolt.", "удрать", "Он решил удрать."),
    ("novelist", "He is a famous novelist.", "прозаик", "Он известный прозаик."),
    ("Five-Year Plan", "The Five-Year Plan was important.", "пятилетка", "Пятилетка была важной."),
    ("humpbacked", "The humpbacked bridge is old.", "горбатый", "Горбатый мост старый."),
    ("emigrate", "They want to emigrate.", "эмигрировать", "Они хотят эмигрировать."),
    ("sender", "The sender is unknown.", "отправитель", "Отправитель неизвестен."),
    ("resumption", "The resumption of work is soon.", "возобновление", "Возобновление работы скоро."),
    ("tale", "This is an old tale.", "сказание", "Это старое сказание."),
    ("brand", "This is a brand of shame.", "клеймо", "Это клеймо позора."),
    ("veterinarian", "The veterinarian treated my cat today.", "ветеринар", "Ветеринар лечил мою кошку сегодня."),
    ("liberalization", "They want liberalization.", "либерализация", "Они хотят либерализацию."),
    ("debut", "Her debut was a success.", "дебют", "Её дебют был успехом."),
    ("vow", "She made a vow.", "обет", "Она дала обет."),
    ("marketer", "He works as a marketer.", "маркетолог", "Он работает маркетологом."),
    ("to arrive in time", "He arrived in time.", "подоспеть", "Он подоспел."),
    ("microbe", "This microbe is dangerous.", "микроб", "Этот микроб опасен."),
    ("kerosene", "We use kerosene for the lamp.", "керосин", "Мы используем керосин для лампы."),
    ("blackmail", "This is blackmail.", "шантаж", "Это шантаж."),
    ("cubic meter", "We need three cubic meters of sand.", "кубометр", "Нам нужно три кубометра песка."),
    ("occupier", "The occupier is in the city.", "оккупант", "Оккупант в городе."),
    ("seventeenth", "This is the seventeenth day.", "семнадцатый", "Это семнадцатый день."),
    ("to turn up", "A chance turned up.", "подвернуться", "Возможность подвернулась."),
    ("to be elected", "He hopes to be elected.", "избираться", "Он надеется избираться."),
    ("to look closely", "She began to look closely.", "присматриваться", "Она начала присматриваться."),
    ("voice recorder", "I lost my voice recorder yesterday.", "диктофон", "Я потерял свой диктофон вчера."),
    ("oil and gas", "This is an oil and gas company.", "нефтегазовый", "Это нефтегазовая компания."),
    ("dimension", "Check the box's dimension.", "габарит", "Проверьте габарит ящика."),
    ("law and order", "We need law and order.", "правопорядок", "Мы хотим правопорядок."),
    ("impurity", "There is an impurity in the water.", "примесь", "В воде есть примесь."),
    ("to be undertaken", "This work is undertaken every year.", "предприниматься", "Эта работа предпринимается каждый год."),
    ("multiply", "Multiply five by two.", "умножить", "Умножьте пять на два."),
    ("orbital", "This is an orbital station.", "орбитальный", "Это орбитальная станция."),
    ("stare", "He likes to stare.", "пялиться", "Он любит пялиться."),
    ("fair-haired", "She is a fair-haired girl.", "белокурый", "Она белокурая девушка."),
    ("carefree", "He is a carefree boy.", "беззаботный", "Он беззаботный мальчик."),
    ("existential", "This is an existential question.", "экзистенциальный", "Это экзистенциальный вопрос."),
    ("sideways", "The vase fell sideways.", "набок", "Ваза упала набок."),
    ("Snow Maiden", "I see the Snow Maiden.", "Снегурочка", "Я вижу Снегурочку."),
    ("cowardice", "His cowardice is known.", "трусость", "Его трусость известна."),
    ("to sweat", "I began to sweat from the heat.", "вспотеть", "Я вспотел от жары."),
    ("dear", "Thank you, dear.", "голубчик", "Спасибо, голубчик."),
    ("Freemasonry", "He reads about Freemasonry.", "масонство", "Он читает о масонстве."),
    ("enviable", "She has an enviable career.", "завидный", "У неё завидная карьера."),
    ("tedious", "This work is tedious.", "нудный", "Эта работа нудная."),
    ("aristocratic", "She has an aristocratic face.", "аристократический", "У неё аристократическое лицо."),
    ("internship", "I started my internship in summer.", "стажировка", "Я начал стажировку летом."),
    ("resonant", "The hall is resonant.", "гулкий", "Зал гулкий."),
    ("carousel", "They love the carousel in the park.", "карусель", "Они любят карусель в парке."),
    ("to spill", "Do not spill the water.", "проливать", "Не проливай воду."),
    ("pernicious", "This is a pernicious habit.", "пагубный", "Это пагубная привычка."),
    ("crater", "The crater is deep.", "кратер", "Кратер глубокий."),
    ("Astrakhan", "This is an Astrakhan coat.", "астраханский", "Это астраханское пальто."),
    ("ringingly", "She laughed ringingly.", "звонко", "Она звонко рассмеялась."),
    ("tall", "He is a tall man.", "рослый", "Он рослый мужчина."),
    ("to lull", "The song will lull the child.", "убаюкать", "Песня убаюкает дитя."),
    ("clear up", "The sky will clear up soon.", "проясниться", "Небо скоро прояснится."),
    ("Western European", "This is a Western European country.", "западноевропейский", "Это западноевропейская страна."),
    ("amateur activity", "The club has amateur activity.", "самодеятельность", "В клубе есть самодеятельность."),
    ("obsolete", "This method is obsolete.", "устаревший", "Этот способ устаревший."),
    ("missionary", "The missionary went far.", "миссионер", "Миссионер ушёл далеко."),
    ("vomiting", "He had vomiting at night.", "рвота", "У него ночью была рвота."),
    ("lava", "Lava is hot.", "лава", "Лава горячая."),
    ("upholster", "We will upholster the old sofa.", "обить", "Надо обить старый диван."),
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
    "felt": "feel",
    "wrote": "write",
    "built": "build",
    "sat": "sit",
    "began": "begin",
    "became": "become",
    "bought": "buy",
    "caught": "catch",
    "kept": "keep",
    "left": "leave",
    "shown": "show",
    "showed": "show",
    "stopped": "stop",
    "heard": "hear",
    "found": "find",
    "held": "hold",
    "lost": "lose",
    "chose": "choose",
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
    "нашел": "найти",
    "нашла": "найти",
    "будь": "быть",
    "стал": "стать",
    "стала": "стать",
    "стали": "стать",
    "пишет": "писать",
    "увидел": "видеть",
    "услышал": "слышать",
    "слышу": "слышать",
    "ушел": "уйти",
    "ушла": "уйти",
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
