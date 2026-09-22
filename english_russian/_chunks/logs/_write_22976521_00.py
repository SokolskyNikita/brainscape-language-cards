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

SRC = PACK / "_chunks" / "deck_22976521_00.csv"
OUT = PACK / "_chunks" / "fixed" / "deck_22976521_00.csv"
LOG = PACK / "_chunks" / "logs" / "deck_22976521_00.txt"

FUNCTION_EN = {
    "a", "an", "the", "is", "be", "i", "you", "he", "she", "it", "we", "they",
    "my", "and", "or", "in", "on", "at", "to", "of", "for", "with", "from",
    "not", "his", "him", "her", "their", "them", "our", "us", "me", "am",
    "are", "was", "were", "been", "being", "this", "that", "these", "those",
    "as", "by", "into", "about", "than", "then", "so", "if", "but", "its",
    "your", "do", "does", "did", "will", "would", "can", "could", "may",
    "there", "here", "has", "had", "have", "don't", "dont", "let's", "lets",
    "all", "off", "done", "myself", "yourself", "himself", "herself",
    "itself", "ourselves", "themselves", "one's", "ones", "too", "very",
    "also", "still", "even", "only", "just", "i'll", "she's", "he's", "it's",
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
    "давайте", "как", "что", "чтобы", "когда", "если", "где", "чем", "кто",
    "них", "него", "нее", "ней", "ним", "очень", "слишком",
}

allow_en = {
    line.strip().lower()
    for line in (PACK / "_vocab" / "allow_en_22976521.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_ru = {
    line.strip().replace("ё", "е").lower()
    for line in (PACK / "_vocab" / "allow_ru_22976521.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_en |= FUNCTION_EN
allow_ru |= FUNCTION_RU

# New lemmas introduced by corrections (taught on this card).
allow_ru |= {"привидение"}

# (en_lemma, en_ex, ru_lemma, ru_ex)
FIXED = [
    ("cut, sever", "He cut the rope with scissors.", "перерезать", "Он перерезал канат ножницами."),
    ("repentance, penitence", "His repentance is real.", "покаяние", "Его покаяние настоящее."),
    ("healing, cure", "I wait for healing.", "исцеление", "Я жду исцеления."),
    ("possessed, obsessed", "She seemed possessed by a strange energy.", "одержимый", "Она казалась одержимой странной энергией."),
    ("prisoner of war, POW", "He became a prisoner of war.", "военнопленный", "Он стал военнопленным."),
    ("innovation, new development", "This innovation is important.", "нововведение", "Это нововведение важно."),
    ("evacuate", "We must evacuate the building now.", "эвакуировать", "Мы должны сейчас эвакуировать здание."),
    ("to stretch, to tighten", "I will stretch the cloth.", "натягивать", "Я натяну ткань."),
    ("daring, reckless", "He is a daring man.", "лихой", "Он лихой человек."),
    ("relief, terrain", "The mountain relief is high.", "рельеф", "Рельеф горы высокий."),
    ("farewell, parting", "This is our farewell.", "прощание", "Это наше прощание."),
    ("commerce, trade", "Commerce is important.", "коммерция", "Коммерция важна."),
    ("alcoholism, alcohol addiction", "Alcoholism is a disease.", "алкоголизм", "Алкоголизм — это болезнь."),
    ("ugly, monstrous", "This house is ugly.", "безобразный", "Этот дом безобразный."),
    ("tight, stiff", "The screw is too tight.", "тугой", "Винт слишком тугой."),
    ("sort of, kind of", "It's sort of interesting.", "вроде", "Это вроде интересно."),
    ("dissolve, disperse", "Sugar will dissolve in water quickly.", "растворяться", "Сахар быстро растворится в воде."),
    ("alien, stranger", "He felt like an alien among them.", "чужак", "Он чувствовал себя чужаком среди них."),
    ("ghost, apparition", "The ghost is in the old house.", "привидение", "Привидение в старом доме."),
    ("crowbar, scrap metal", "He opened the box with a crowbar.", "лом", "Он открыл ящик ломом."),
    ("peasantry", "The peasantry lives on the land.", "крестьянство", "Крестьянство живёт на земле."),
    ("bunks, berths", "The soldiers have bunks.", "нары", "У солдат есть нары."),
    ("scarf, shawl", "She put on a warm scarf.", "шарф", "Она надела тёплый шарф."),
    ("tighten, pull up", "Please tighten the screws.", "подтянуть", "Пожалуйста, подтяните винты."),
    ("to climb, to clamber", "He climbs the fence.", "забираться", "Он забирается на забор."),
    ("dean, dean's office", "The dean greeted the students.", "декан", "Декан приветствовал студентов."),
    ("to wave off, to brush off", "He will wave off my words.", "отмахнуться", "Он отмахнётся от моих слов."),
    ("daddy, dad", "Daddy bought me a book.", "папочка", "Папочка купил мне книгу."),
    ("small room, little room", "She rented a cozy small room.", "комнатка", "Она сняла уютную комнатку."),
    ("diplomacy", "Diplomacy is important.", "дипломатия", "Дипломатия важна."),
    ("emergency, urgent", "This is an emergency call.", "экстренный", "Это экстренный вызов."),
    ("hinder, impede", "Heavy rain can hinder the work.", "затруднять", "Сильный дождь может затруднить работу."),
    ("washing, laundry", "The washing machine is broken.", "стиральный", "Стиральная машина сломана."),
    ("extraction, retrieval", "The extraction was hard.", "извлечение", "Извлечение было трудным."),
    ("receipt, voucher", "Keep your receipt.", "квитанция", "Храните квитанцию."),
    ("trench, dugout", "Soldiers dug a trench.", "траншея", "Солдаты вырыли траншею."),
    ("fiber, filament", "Cotton fiber is strong.", "волокно", "Волокно хлопка прочное."),
    ("trade union, union", "The trade union is strong.", "профсоюз", "Профсоюз сильный."),
    ("political scientist, political analyst", "The political scientist wrote a book.", "политолог", "Политолог написал книгу."),
    ("citizen, female citizen", "She is a proud citizen.", "гражданка", "Она гордая гражданка."),
    ("swallow, martin", "A swallow flew over the lake.", "ласточка", "Ласточка пролетела над озером."),
    ("cardboard, carton", "I bought a cardboard box.", "картонный", "Я купил картонный ящик."),
    ("Byzantine", "The Byzantine city was rich.", "византийский", "Византийский город был богатым."),
    ("register, registry", "Write your name in the register.", "регистр", "Напиши своё имя в регистр."),
    ("but, however", "I tried, however I failed.", "однако", "Я пытался, однако не смог."),
    ("playwright, dramatist", "The playwright wrote a book.", "драматург", "Драматург написал книгу."),
    ("succeed, prosper", "She wants to succeed.", "преуспеть", "Она хочет преуспеть."),
    ("vent, small window", "Open the vent for fresh air.", "форточка", "Открой форточку для свежего воздуха."),
    ("series, succession", "A series of events began.", "череда", "Череда событий началась."),
    ("insufficiency, deficiency", "The insufficiency of water is clear.", "недостаточность", "Недостаточность воды ясна."),
    ("close, lock", "Please close the chain.", "замкнуть", "Пожалуйста, замкните цепь."),
    ("flood, inundate", "The river will flood the town soon.", "затопить", "Река скоро затопит город."),
    ("migrant, immigrant", "The migrant found work.", "мигрант", "Мигрант нашёл работу."),
    ("leash, lead", "Keep the dog on a leash.", "поводок", "Держите собаку на поводке."),
    ("buttock, glute", "He felt pain in his buttock.", "ягодица", "Он чувствовал боль в ягодице."),
    ("subsystem, sub-system", "The engine has a subsystem.", "подсистема", "У двигателя есть подсистема."),
    ("jar, little jar", "I opened the jar.", "баночка", "Я открыл баночку."),
    ("Tyumen, Tyumensky", "This is a Tyumen street.", "тюменский", "Это тюменская улица."),
    ("to water, to give a drink", "I need to water the horses.", "напоить", "Мне нужно напоить лошадей."),
    ("supply, provide", "We must supply the army with water.", "снабжать", "Мы должны снабжать армию водой."),
    ("underground, clandestine", "He works in the underground.", "подполье", "Он работает в подполье."),
    ("Politburo, Political Bureau", "The Politburo decided this.", "политбюро", "Политбюро это решило."),
    ("certification, certification process", "I got my certification yesterday.", "сертификация", "Я получил сертификацию вчера."),
    ("informatics, computer science", "I study informatics at the university.", "информатика", "Я изучаю информатику в университете."),
    ("patron, protector", "He is a patron of art.", "покровитель", "Он покровитель искусства."),
    ("preacher, sermonizer", "The preacher began the sermon.", "проповедник", "Проповедник начал проповедь."),
    ("principality, duchy", "This principality is old.", "княжество", "Это княжество старое."),
    ("chase, pursue", "Cats often chase their tails.", "гоняться", "Кошки часто гоняются за своими хвостами."),
    ("badly, poorly", "He sings badly.", "худо", "Он поёт худо."),
    ("baton, club", "The officer raised his baton.", "дубинка", "Офицер поднял дубинку."),
    ("finishing, trim", "The finishing on the table is good.", "отделка", "Отделка стола хорошая."),
    ("lace, cord", "The lace is on the shoe.", "шнурок", "Шнурок на ботинке."),
    ("roll, push", "Let's roll the stone.", "катить", "Давайте катить камень."),
    ("streamlet, trickle", "A streamlet ran from the roof.", "струйка", "Струйка бежала с крыши."),
    ("to drag on, to tighten", "The meeting began to drag on.", "затягивать", "Встреча начала затягиваться."),
    ("to pull oneself together, to realize", "He realized it too late.", "спохватиться", "Он спохватился слишком поздно."),
    ("pi, peony", "I know the number pi.", "пи", "Я знаю число пи."),
    ("distance, range", "The shot has a long range.", "дальность", "У выстрела большая дальность."),
    ("discuss, agree upon", "Let's agree upon the price.", "оговорить", "Давайте оговорим цену."),
    ("shut up, be quiet", "Shut up and listen!", "заткнуться", "Заткнись и слушай!"),
    ("manifesto, manifest", "He published his manifesto.", "манифест", "Он опубликовал свой манифест."),
    ("pressure, assault", "The pressure was strong.", "натиск", "Натиск был сильным."),
    ("beat off, repel", "They beat off the enemy.", "отбивать", "Они отбили врага."),
    ("in the distance, far away", "I saw a house in the distance.", "вдалеке", "Я видел дом вдалеке."),
    ("request, inquire", "I'll request the document tomorrow.", "запросить", "Я запрошу документ завтра."),
    ("intercourse, relations", "They had intercourse.", "сношение", "У них было сношение."),
    ("to beat, to batter", "They beat the man.", "избивать", "Они избивали человека."),
    ("merciful, gracious", "He is a merciful man.", "милостивый", "Он милостивый человек."),
    ("to loom, to be in the offing", "A new plan began to loom.", "намечаться", "Начал намечаться новый план."),
    ("hiss, sizzle", "The snake began to hiss loudly.", "шипеть", "Змея начала громко шипеть."),
    ("hint, suggest", "She will hint at the truth.", "намекнуть", "Она намекнёт на правду."),
    ("recovery, convalescence", "His recovery was slow.", "выздоровление", "Его выздоровление было медленным."),
    ("mystery, sacrament", "Marriage is a sacrament.", "таинство", "Брак — это таинство."),
    ("underage, juvenile", "He is still underage.", "малолетний", "Он ещё малолетний."),
    ("deputy's, parliamentary", "This is a deputy's question.", "депутатский", "Это депутатский вопрос."),
    ("Nazi, fascist", "He was a Nazi.", "нацист", "Он был нацистом."),
    ("employment, job placement", "She found employment.", "трудоустройство", "Она нашла трудоустройство."),
    ("petal, leaflet", "A petal fell down.", "лепесток", "Лепесток упал вниз."),
    ("communicative, communicational", "She's very communicative.", "коммуникативный", "Она очень коммуникативная."),
    ("illegally, unlawfully", "He lived there illegally.", "незаконно", "Он жил там незаконно."),
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
    "slept": "sleep",
    "dug": "dig",
    "flew": "fly",
    "found": "find",
    "ran": "run",
    "knew": "know",
    "cut": "cut",
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
    "смог": "мочь",
    "хочу": "хотеть",
    "хочет": "хотеть",
    "хотим": "хотеть",
    "вижу": "видеть",
    "видишь": "видеть",
    "видит": "видеть",
    "видел": "видеть",
    "знаю": "знать",
    "живу": "жить",
    "живем": "жить",
    "живет": "жить",
    "живет": "жить",
    "живёт": "жить",
    "нашел": "найти",
    "нашла": "найти",
    "нашёл": "найти",
    "будь": "быть",
    "стал": "стать",
    "стала": "стать",
    "стали": "стать",
    "пишет": "писать",
    "напиши": "писать",
    "увидел": "видеть",
    "услышал": "слышать",
    "слышу": "слышать",
    "должен": "должный",
    "должны": "должный",
    "жди": "ждать",
    "жду": "ждать",
    "открой": "открыть",
    "храните": "хранить",
    "держите": "держать",
    "заткнись": "заткнуться",
    "слушай": "слушать",
    "шею": "шея",
    "шее": "шея",
    "еды": "еда",
    "едой": "еда",
    "воды": "вода",
    "водой": "вода",
    "теплый": "тепло",
    "тёплый": "тепло",
}


def _ru_ok(word: str) -> bool:
    w = word.replace("ё", "е").lower()
    if w in allow_ru:
        return True
    mapped = IRREGULAR_RU.get(w) or IRREGULAR_RU.get(word.lower())
    if mapped and mapped.replace("ё", "е").lower() in allow_ru:
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
    parts = [
        re.sub(r"[^\w'-]+", "", p).strip()
        for p in re.split(r"[,;/]|\s+", lemma.replace("ё", "е").lower())
        if p.strip()
    ]
    keys = [p for p in parts if p not in {"to", "be", "the", "a", "an"}] or parts
    for key in keys:
        stem = key[:4] if len(key) >= 4 else key
        if stem and stem in text.replace(" ", ""):
            return True
        if key in text:
            return True
    return False


def first_gloss(text: str) -> str:
    return re.split(r"[,/]", text)[0].strip().lower()


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
        if first_gloss(old.get("qMdBody") or "") != first_gloss(en_lemma):
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
