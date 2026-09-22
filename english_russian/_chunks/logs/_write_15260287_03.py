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

SRC = PACK / "_chunks" / "deck_15260287_03.csv"
OUT = PACK / "_chunks" / "fixed" / "deck_15260287_03.csv"
LOG = PACK / "_chunks" / "logs" / "deck_15260287_03.txt"

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
    for line in (PACK / "_vocab" / "allow_en_15260287.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_ru = {
    line.strip().replace("ё", "е").lower()
    for line in (PACK / "_vocab" / "allow_ru_15260287.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_en |= FUNCTION_EN
allow_ru |= FUNCTION_RU

# New lemmas introduced by corrections (taught on this card).
allow_ru |= {"активировать"}

# (en_lemma, en_ex, ru_lemma, ru_ex)
FIXED = [
    ("sheikh", "The sheikh spoke to the people.", "шейх", "Шейх говорил с народом."),
    ("to swirl", "Smoke began to swirl in the air.", "клубиться", "Дым начал клубиться в воздухе."),
    ("federative", "Our country is a federative state.", "федеративный", "Наша страна федеративное государство."),
    ("smoker", "My father is a smoker.", "курильщик", "Мой отец курильщик."),
    ("midwife", "The midwife helped the woman.", "акушерка", "Акушерка помогла женщине."),
    ("slave girl", "The slave girl wanted freedom.", "рабыня", "Рабыня хотела свободы."),
    ("business card", "He gave me his business card.", "визитка", "Он дал мне свою визитку."),
    ("straightforward", "He is a straightforward man.", "прямолинейный", "Он прямолинейный человек."),
    ("saboteur", "The saboteur destroyed the bridge.", "диверсант", "Диверсант уничтожил мост."),
    ("to delirium", "He began to delirium at night.", "бредить", "Он начал бредить ночью."),
    ("to bring closer", "This book will bring closer two friends.", "сближать", "Эта книга сблизит двух друзей."),
    ("vowel", "A is a vowel.", "гласный", "А это гласный."),
    ("sludge", "There is sludge at the bottom.", "отстой", "На дне есть отстой."),
    ("correlation", "There is a correlation between these facts.", "корреляция", "Между этими фактами есть корреляция."),
    ("highly qualified", "She is a highly qualified doctor.", "высококвалифицированный", "Она высококвалифицированный врач."),
    ("weekday", "This is a weekday train.", "будничный", "Это будничный поезд."),
    ("abbreviation", "This is an abbreviation of the name.", "аббревиатура", "Это аббревиатура имени."),
    ("passageway", "The passageway led to the yard.", "проход", "Проход вел во двор."),
    ("associative", "This is an associative link.", "ассоциативный", "Это ассоциативная связь."),
    ("jellyfish", "A jellyfish is in the water.", "медуза", "Медуза в воде."),
    ("to thread", "She will thread the needle.", "просунуть", "Она просунет нить в иглу."),
    ("to look out for", "Look out for the boy.", "высматривать", "Высматривай мальчика."),
    ("relentlessly", "Time moves relentlessly.", "неумолимо", "Время идет неумолимо."),
    ("apron", "She put on an apron.", "фартук", "Она надела фартук."),
    ("Nazism", "Nazism brought great evil.", "нацизм", "Нацизм принес большое зло."),
    ("drummer", "The drummer played loudly.", "барабанщик", "Барабанщик играл громко."),
    ("theology", "He studies theology.", "богословие", "Он изучает богословие."),
    ("to call over", "I called over the boy.", "подозвать", "Я подозвал мальчика."),
    ("Talmud", "He reads the Talmud.", "талмуд", "Он читает Талмуд."),
    ("administratively", "The city is divided administratively.", "административно", "Город разделен административно."),
    ("primary source", "Read the primary source.", "первоисточник", "Прочитайте первоисточник."),
    ("anticipate", "I anticipate this meeting.", "предвкушать", "Я предвкушаю эту встречу."),
    ("immensely", "I am immensely glad.", "безмерно", "Я безмерно рад."),
    ("cybernetics", "He studies cybernetics.", "кибернетика", "Он изучает кибернетику."),
    ("closet", "He lives in a small closet.", "каморка", "Он живет в маленькой каморке."),
    ("Portuguese", "I study the Portuguese language.", "португальский", "Я изучаю португальский язык."),
    ("to merge", "He began to merge into the group.", "вливаться", "Он начал вливаться в группу."),
    ("sip", "She likes to sip tea.", "потягивать", "Она любит потягивать чай."),
    ("tireless", "She is a tireless worker.", "неутомимый", "Она неутомимая работница."),
    ("snowfall", "The snowfall was heavy.", "снегопад", "Снегопад был сильным."),
    ("to activate", "I want to activate this machine.", "активировать", "Я хочу активировать эту машину."),
    ("stocky", "He is a stocky man.", "коренастый", "Он коренастый мужчина."),
    ("to infiltrate", "They want to infiltrate the group.", "внедряться", "Они хотят внедриться в группу."),
    ("verification", "This machine needs verification.", "поверка", "Этой машине нужна поверка."),
    ("half-word", "He understood from a half-word.", "полуслово", "Он понял с полуслова."),
    ("glucose", "There is glucose in the blood.", "глюкоза", "В крови есть глюкоза."),
    ("demolition", "They began the demolition of the house.", "снос", "Они начали снос дома."),
    ("mountaineering", "He loves mountaineering.", "альпинизм", "Он любит альпинизм."),
    ("termination", "We demand termination of the contract.", "расторжение", "Мы требуем расторжения договора."),
    ("enterprising", "He is an enterprising man.", "предприимчивый", "Он предприимчивый человек."),
    ("to shell", "They will shell the town.", "обстрелять", "Они обстреляют город."),
    ("unrealized", "This was an unrealized plan.", "несостоявшийся", "Это был несостоявшийся план."),
    ("unlearn", "He will unlearn how to write.", "разучиться", "Он разучится писать."),
    ("faceless", "This is a faceless crowd.", "безликий", "Это безликая толпа."),
    ("revaluation", "We need a revaluation of this work.", "переоценка", "Нам нужна переоценка этой работы."),
    ("rhythmic", "This is a rhythmic movement.", "ритмический", "Это ритмическое движение."),
    ("to tune", "I need to tune the guitar.", "настроить", "Мне нужно настроить гитару."),
    ("hepatitis", "He is sick with hepatitis.", "гепатит", "Он болен гепатитом."),
    ("environmental conservation", "This is an environmental conservation law.", "природоохранный", "Это природоохранный закон."),
    ("coursemate", "I met my coursemate yesterday.", "однокурсник", "Вчера я встретил однокурсника."),
    ("rumor", "A rumor spread through the town.", "слух", "По городу прошел слух."),
    ("drainage", "We need drainage of the water.", "отвод", "Нам нужен отвод воды."),
    ("hundred square meters", "He bought a hundred square meters of land.", "сотка", "Он купил сотку земли."),
    ("buzz", "The bee will buzz near the window.", "жужжать", "Пчела будет жужжать у окна."),
    ("seem", "It seemed to me that he was here.", "почудиться", "Мне почудилось, что он здесь."),
    ("film adaptation", "I saw the film adaptation of the book.", "экранизация", "Я видел экранизацию книги."),
    ("satanic", "This is a satanic book.", "сатанинский", "Это сатанинская книга."),
    ("disobedient", "The disobedient boy did not listen.", "непослушный", "Непослушный мальчик не слушал."),
    ("vibrate", "The table began to vibrate.", "вибрировать", "Стол начал вибрировать."),
    ("to shoot oneself", "He decided to shoot himself.", "застрелиться", "Он решил застрелиться."),
    ("pediatrician", "The pediatrician examined the child.", "педиатр", "Педиатр осмотрел мальчика."),
    ("sonnet", "He wrote a sonnet.", "сонет", "Он написал сонет."),
    ("restorative", "He needs a restorative rest.", "восстановительный", "Ему нужен восстановительный отдых."),
    ("recruit", "The recruit joined the army.", "новобранец", "Новобранец вступил в армию."),
    ("to lock oneself in", "She decided to lock herself in.", "запереться", "Она решила запереться."),
    ("foresight", "His foresight saved us.", "предвидение", "Его предвидение спасло нас."),
    ("Frenchwoman", "The Frenchwoman spoke slowly.", "француженка", "Француженка говорила медленно."),
    ("summarize", "Please summarize the report.", "резюмировать", "Пожалуйста, резюмируйте доклад."),
    ("italic", "The title was in italic.", "курсив", "Название было курсивом."),
    ("astral", "He spoke of the astral world.", "астральный", "Он говорил об астральном мире."),
    ("texture", "I like the texture of this paper.", "фактура", "Мне нравится фактура этой бумаги."),
    ("tangibly", "The pain was tangibly strong.", "ощутимо", "Боль была ощутимо сильной."),
    ("masterfully", "He masterfully played this role.", "мастерски", "Он мастерски сыграл эту роль."),
    ("immoral", "This action is immoral.", "аморальный", "Это действие аморально."),
    ("religiously", "She was raised religiously.", "религиозно", "Ее воспитали религиозно."),
    ("Aquarius", "He was born under Aquarius.", "водолей", "Он родился под знаком Водолея."),
    ("get along", "We always get along.", "ладить", "Мы всегда ладим."),
    ("political officer", "The political officer spoke to the soldiers.", "замполит", "Замполит говорил с солдатами."),
    ("bachelor", "He is a happy bachelor.", "холостяк", "Он счастливый холостяк."),
    ("ooze", "Blood began to ooze from the wound.", "сочиться", "Кровь начала сочиться из раны."),
    ("rejoicing", "There was rejoicing in the city.", "ликование", "В городе было ликование."),
    ("to get closer", "They want to get closer.", "сблизиться", "Они хотят сблизиться."),
    ("provocatively", "She looked at him provocatively.", "вызывающе", "Она вызывающе посмотрела на него."),
    ("accreditation", "The school received accreditation.", "аккредитация", "Школа получила аккредитацию."),
    ("interpersonal", "This is an interpersonal conflict.", "межличностный", "Это межличностный конфликт."),
    ("machine-building", "He works at a machine-building plant.", "машиностроительный", "Он работает на машиностроительном заводе."),
    ("dandelion", "A dandelion grew by the road.", "одуванчик", "У дороги вырос одуванчик."),
    ("memorization", "Memorization takes time.", "запоминание", "Запоминание требует времени."),
    ("bestseller", "This book is a bestseller.", "бестселлер", "Эта книга бестселлер."),
    ("archer", "The archer hit the target.", "лучник", "Лучник попал в цель."),
]

IRREGULAR_EN = {
    "gave": "give",
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
    "led": "lead",
    "brought": "bring",
    "met": "meet",
    "saw": "see",
    "grew": "grow",
    "born": "bear",
    "understood": "understand",
    "took": "take",
    "came": "come",
    "went": "go",
    "made": "make",
    "knew": "know",
    "thought": "think",
    "found": "find",
    "told": "tell",
    "held": "hold",
    "read": "read",
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
    "дал": "дать",
    "вела": "вести",
    "вел": "вести",
    "идет": "идти",
    "шел": "идти",
    "шла": "идти",
    "шло": "идти",
    "шли": "идти",
    "прошел": "пройти",
    "видел": "видеть",
    "хорошо": "хороший",
    "лучше": "хороший",
    "нужна": "нужно",
    "нужен": "нужно",
    "нужны": "нужно",
    "помогла": "помогать",
    "принес": "принести",
    "спас": "спастись",
    "спасло": "спастись",
    "встретил": "встреча",
    "купил": "купить",
    "вырос": "вырасти",
    "родился": "родиться",
    "воспитали": "воспитать",
    "болен": "больной",
    "нравится": "нравиться",
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
