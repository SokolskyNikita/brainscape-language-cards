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

SRC = PACK / "_chunks" / "deck_22976521_01.csv"
OUT = PACK / "_chunks" / "fixed" / "deck_22976521_01.csv"
LOG = PACK / "_chunks" / "logs" / "deck_22976521_01.txt"

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
    "no", "yes", "up", "down", "out", "over", "under", "again", "once",
    "who", "what", "when", "where", "why", "how", "which", "whom",
    "don't", "didn't", "doesn't", "can't", "won't", "i'm", "we're", "they're",
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

# (en_lemma, en_ex, ru_lemma, ru_ex)
FIXED = [
    ("identify, recognize", "I could not identify him.", "опознать", "Я не смог его опознать."),
    ("performance, protrusion", "There is a protrusion on the wall.", "выступ", "На стене есть выступ."),
    ("training, practice", "This is a training camp.", "тренировочный", "Это тренировочный лагерь."),
    ("Sagittarius, archer", "She is a Sagittarius.", "стрелец", "Она Стрелец."),
    ("Smolensk, Smolensky", "This is a Smolensk street.", "смоленский", "Это смоленская улица."),
    ("five-year, five-year-old", "She has a five-year-old son.", "пятилетний", "У неё пятилетний сын."),
    ("educational, instructive", "The movie was educational.", "поучительный", "Фильм был поучительным."),
    ("cylinder, tank", "The cylinder is empty.", "баллон", "Баллон пустой."),
    ("fellow traveler, companion", "He found a fellow traveler.", "попутчик", "Он нашёл попутчика."),
    ("turn inside out, wring out", "She will turn the jacket inside out.", "вывернуть", "Она вывернет куртку."),
    ("brazenly, insolently", "He brazenly took the book.", "нагло", "Он нагло взял книгу."),
    ("to hear, to overhear", "I heard his words.", "услыхать", "Я услыхал его слова."),
    ("refinement, improvement", "The plan needs further refinement.", "доработка", "Плану нужна доработка."),
    ("fan, ventilator", "The fan is in the room.", "вентилятор", "Вентилятор в комнате."),
    ("enthusiast, zealot", "He is a true enthusiast.", "энтузиаст", "Он настоящий энтузиаст."),
    ("devilishly, damnably", "This work is devilishly hard.", "чертовски", "Эта работа чертовски трудная."),
    ("paratrooper, airborne trooper", "The paratrooper is ready.", "десантник", "Десантник готов."),
    ("solid, substantial", "This is a solid argument.", "веский", "Это веский аргумент."),
    ("deliverance, liberation", "We wait for deliverance.", "избавление", "Мы ждём избавления."),
    ("to fall, to collapse", "The house began to collapse.", "валиться", "Дом начал валиться."),
    ("aspiration, ambition", "Her aspiration is clear.", "устремление", "Её устремление ясно."),
    ("auditor, listener", "The auditor came yesterday.", "аудитор", "Аудитор пришёл вчера."),
    ("inheritance, heritage", "Inheritance of land is hard.", "наследование", "Наследование земли трудное."),
    ("layout, arrangement", "This old layout of life is simple.", "уклад", "Этот старый уклад жизни простой."),
    ("to ask for it, to invite", "He is asking for it.", "напрашиваться", "Он напрашивается на это."),
    ("route, tract", "This tract is old.", "тракт", "Этот тракт старый."),
    ("identical", "The twins wore identical dresses.", "идентичный", "Близнецы носили идентичные платья."),
    ("shoe, boot", "I lost my shoe yesterday.", "башмак", "Я потерял свой башмак вчера."),
    ("riding, skating", "I love riding.", "катание", "Я люблю катание."),
    ("recognize, identify", "I can recognize this word.", "распознать", "Я могу распознать это слово."),
    ("move, relocate", "Let's move to the next room.", "переместиться", "Давайте переместимся в следующую комнату."),
    ("edge of a forest, fringe", "We stood at the edge of a forest.", "опушка", "Мы стояли на опушке леса."),
    ("attach, find a place for", "Attach the shed to the house.", "пристроить", "Пристройте сарай к дому."),
    ("ward, dependent", "She is my ward.", "подопечный", "Она моя подопечная."),
    ("guest, visitor", "The guest arrived early.", "гостья", "Гостья прибыла рано."),
    ("improve, perfect", "We must improve our work.", "совершенствовать", "Мы должны совершенствовать нашу работу."),
    ("accompany", "Danger can accompany this work.", "сопутствовать", "Опасность может сопутствовать этой работе."),
    ("commonwealth, alliance", "They formed a commonwealth.", "содружество", "Они создали содружество."),
    ("Communist Party", "The Communist Party is old.", "компартия", "Компартия старая."),
    ("pebble, small stone", "I found a pebble.", "камешек", "Я нашёл камешек."),
    ("Volgograd, Volgogradsky", "This is a Volgograd street.", "волгоградский", "Это волгоградская улица."),
    ("coffee, coffee-related", "This is coffee color.", "кофейный", "Это кофейный цвет."),
    ("mockery, bullying", "This is mockery.", "издевательство", "Это издевательство."),
    ("to feel nauseous, to feel sick", "I began to feel nauseous.", "тошнить", "Меня начало тошнить."),
    ("to bark, to snap", "He snapped at me.", "рявкнуть", "Он рявкнул на меня."),
    ("ferocious, fierce", "The dog is ferocious.", "свирепый", "Эта собака свирепая."),
    ("blast furnace, domain", "This is a blast furnace plant.", "доменный", "Это доменный завод."),
    ("standard, benchmark", "Gold is a standard of beauty.", "эталон", "Золото — эталон красоты."),
    ("floral, flowery", "She wore a floral dress.", "цветочный", "Она носила цветочное платье."),
    ("pronunciation, enunciation", "Her pronunciation is good.", "произношение", "Её произношение хорошее."),
    ("humiliate, degrade", "They want to humiliate him.", "унизить", "Они хотят унизить его."),
    ("drown, sink", "He tried to sink the boat.", "утопить", "Он пытался утопить лодку."),
    ("rustle, swish", "Leaves rustle in the wind.", "шуршать", "Листья шуршат на ветру."),
    ("increase, rise", "Prices will increase soon.", "повыситься", "Цены скоро повысятся."),
    ("to distinguish oneself, to excel", "He wants to distinguish himself.", "отличиться", "Он хочет отличиться."),
    ("to calm down, to settle down", "Please calm down.", "успокаиваться", "Пожалуйста, успокаивайтесь."),
    ("to stumble, to trip", "He did not stumble in the dark.", "споткнуться", "Он не споткнулся в темноте."),
    ("projection, mapping", "I see the projection on the wall.", "проекция", "Я вижу проекцию на стене."),
    ("little horse, pony", "The little horse is fast.", "лошадка", "Лошадка быстрая."),
    ("wardrobe, closet", "She opened her wardrobe.", "гардероб", "Она открыла свой гардероб."),
    ("miss, slip", "That was a miss.", "промах", "Это был промах."),
    ("ashtray, ashpan", "The ashtray is on the table.", "пепельница", "Пепельница на столе."),
    ("to fail, to sink", "The plan began to fail.", "проваливаться", "План начал проваливаться."),
    ("goal, naked", "He scored a goal.", "гол", "Он забил гол."),
    ("monthly, monthly basis", "This is a monthly plan.", "ежемесячный", "Это ежемесячный план."),
    ("bring in, enter", "Please bring in the box.", "заносить", "Пожалуйста, заносите ящик."),
    ("airline, carrier", "This airline is new.", "авиакомпания", "Эта авиакомпания новая."),
    ("wolf's, lupine", "This is a wolf's fur.", "волчий", "Это волчий мех."),
    ("hallucination, illusion", "It was a hallucination.", "галлюцинация", "Это была галлюцинация."),
    ("to cherish, to value", "I cherish this book.", "дорожить", "Я дорожу этой книгой."),
    ("train, coach", "I train my dog daily.", "тренировать", "Я тренирую свою собаку каждый день."),
    ("scratch, itch", "I need to scratch my hand.", "почесать", "Мне нужно почесать руку."),
    ("lawn, meadow", "The lawn is near the house.", "лужайка", "Лужайка у дома."),
    ("wallet, billfold", "I lost my wallet yesterday.", "бумажник", "Я потерял свой бумажник вчера."),
    ("to jerk, to dash", "He jerked forward.", "рвануться", "Он рванулся вперёд."),
    ("Hollywood, Hollywood-style", "This is a Hollywood movie.", "голливудский", "Это голливудский фильм."),
    ("mental, psychological", "This is a mental problem.", "ментальный", "Это ментальная проблема."),
    ("inevitability, unavoidability", "I know the inevitability of death.", "неизбежность", "Я знаю неизбежность смерти."),
    ("disperse, scatter", "They will disperse the crowd.", "рассеять", "Они рассеют толпу."),
    ("nostalgia, homesickness", "I feel nostalgia.", "ностальгия", "Я чувствую ностальгию."),
    ("to plug, to shut up", "Please plug the hole.", "заткнуть", "Пожалуйста, заткните дыру."),
    ("moss, lichen", "Moss is on the stone.", "мох", "Мох на камне."),
    ("parting, separation", "Parting is hard.", "расставание", "Расставание трудное."),
    ("hieroglyph, ideogram", "I see a hieroglyph.", "иероглиф", "Я вижу иероглиф."),
    ("to rape, to violate", "He tried to rape her.", "изнасиловать", "Он пытался изнасиловать её."),
    ("adjustment, correction", "The plan needs an adjustment.", "корректировка", "Плану нужна корректировка."),
    ("caprice, whim", "This is only a caprice.", "каприз", "Это только каприз."),
    ("objectivity, impartiality", "Objectivity is important.", "объективность", "Объективность важна."),
    ("subconscious, subliminal", "This is a subconscious fear.", "подсознательный", "Это подсознательный страх."),
    ("master, ruler", "He is the master of this land.", "повелитель", "Он повелитель этой земли."),
    ("child, offspring", "Look at this child.", "чадо", "Смотри на это чадо."),
    ("conceal, harbor", "He will conceal his anger.", "затаить", "Он затаит свой гнев."),
    ("courage, valor", "Her courage is great.", "отвага", "Её отвага велика."),
    ("coziness, comfort", "I love this coziness.", "уют", "Я люблю этот уют."),
    ("to have dinner, to dine", "We will have dinner together.", "поужинать", "Мы поужинаем вместе."),
    ("confuse, mix up", "Do not confuse the names.", "спутать", "Не спутайте имена."),
    ("audit, inspection", "We must prepare for the audit.", "аудит", "Мы должны подготовиться к аудиту."),
    ("excessively, overly", "He drinks coffee excessively.", "чрезмерно", "Он чрезмерно пьёт кофе."),
    ("insurer, underwriter", "The insurer paid quickly.", "страховщик", "Страховщик быстро заплатил."),
    ("to grow, to raise", "They raise their son.", "растить", "Они растят своего сына."),
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
    "lost": "lose",
    "wore": "wear",
    "worn": "wear",
    "stood": "stand",
    "held": "hold",
    "brought": "bring",
    "thought": "think",
    "taught": "teach",
    "paid": "pay",
    "said": "say",
    "told": "tell",
    "seen": "see",
    "taken": "take",
    "given": "give",
    "put": "put",
    "scored": "score",
    "tried": "try",
    "snapped": "snap",
    "formed": "form",
    "followed": "follow",
    "arrived": "arrive",
    "opened": "open",
    "jerked": "jerk",
    "needs": "need",
    "drinks": "drink",
    "leaves": "leaf",
    "prices": "price",
    "twins": "twin",
    "words": "word",
    "names": "name",
    "dresses": "dress",
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
    "ждём": "ждать",
    "ждем": "ждать",
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
    "смотри": "смотреть",
    "нужна": "нужно",
    "нужен": "нужно",
    "готов": "готовый",
    "заплатил": "платить",
    "пьёт": "пить",
    "пьет": "пить",
    "растят": "растить",
    "взял": "взять",
    "пришёл": "прийти",
    "пришел": "прийти",
    "шёл": "идти",
    "шли": "идти",
    "потерял": "потерять",
    "люблю": "любить",
    "пытался": "пытаться",
    "забил": "забить",
    "открыла": "открыть",
    "носили": "носить",
    "стояли": "стоять",
    "создали": "создать",
    "поужинаем": "поужинать",
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
