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

SRC = PACK / "_chunks" / "deck_15260272_03.csv"
OUT = PACK / "_chunks" / "fixed" / "deck_15260272_03.csv"
LOG = PACK / "_chunks" / "logs" / "deck_15260272_03.txt"

FUNCTION_EN = {
    "a", "the", "is", "be", "i", "you", "he", "she", "it", "we", "they",
    "my", "and", "or", "in", "on", "at", "to", "of", "for", "with", "from",
    "not", "his", "him", "her", "their", "them", "our", "us", "me", "am",
    "are", "was", "were", "been", "being", "this", "that", "these", "those",
    "an", "as", "by", "into", "about", "than", "then", "so", "if", "but",
    "its", "your", "im", "dont", "cant", "lets", "didnt", "wont", "isnt",
    "there", "here", "very", "too", "now", "today", "yesterday", "tomorrow",
    "some", "any", "all", "no", "yes", "do", "does", "did", "have", "has",
    "had", "will", "would", "can", "could", "should", "must", "may", "might",
    "please", "more", "most", "less", "much", "many", "few", "such", "also",
    "only", "even", "still", "already", "always", "never", "often", "once",
    "after", "before", "under", "over", "through", "between", "without",
    "who", "what", "when", "where", "why", "how", "which",
}

FUNCTION_RU = {
    "я", "мне", "меня", "мной", "мой", "моя", "мое", "моё", "мои", "мою",
    "моего", "моей", "моему", "моим", "моими", "моих",
    "мы", "нам", "нас", "нами", "наш", "наша", "наше", "наши", "нашу",
    "ты", "тебе", "тебя", "тобой", "твой", "твоя", "твое", "твоё", "твои",
    "вы", "вам", "вас", "вами", "ваш", "ваша", "ваше", "ваши", "вашу",
    "он", "она", "оно", "они", "его", "ее", "её", "ей", "ему", "им", "их",
    "ими", "ним", "ней", "ними", "него", "нее", "неё", "нему", "них",
    "себя", "себе", "собой", "свой", "своя", "свое", "своё", "свои", "свою", "своим", "своего", "своей",
    "это", "эта", "этот", "эти", "этого", "этой", "этому", "этим", "этих", "эту",
    "то", "та", "тот", "те", "того", "той", "тому", "тем", "тех", "ту",
    "такой", "такая", "такое", "такие", "так",
    "не", "ни", "нет", "да", "вот", "уж", "ли", "же", "бы",
    "в", "на", "с", "со", "у", "к", "ко", "по", "из", "за", "от", "до",
    "для", "без", "при", "о", "об", "про", "над", "под", "между", "через",
    "после", "перед", "и", "а", "но", "или", "что", "как", "когда", "где",
    "чтобы", "если", "потому", "уже", "еще", "ещё", "только", "даже", "тоже",
    "также", "очень", "сейчас", "теперь", "всегда", "сегодня", "вчера", "завтра",
    "был", "была", "было", "были", "будет", "будут", "есть", "быть",
    "здесь", "тут", "там", "можно", "нужно", "должен", "должна", "должно", "должны",
}

allow_en = {
    line.strip().lower()
    for line in (PACK / "_vocab" / "allow_en_15260272.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_ru = {
    line.strip().replace("ё", "е").lower()
    for line in (PACK / "_vocab" / "allow_ru_15260272.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_en |= FUNCTION_EN
allow_ru |= FUNCTION_RU

# (en_lemma, en_ex, ru_lemma, ru_ex)
FIXED = [
    ("to lean on", "She needed a shoulder to lean on.", "опереться", "Ей нужно было плечо, чтобы опереться."),
    ("exclamation", "I heard her exclamation.", "возглас", "Я слышал её возглас."),
    ("parrot", "The parrot is in the room.", "попугай", "Попугай в комнате."),
    ("remains", "The remains were underground.", "останки", "Останки были под землёй."),
    ("broadcast", "I watched the broadcast.", "трансляция", "Я смотрел трансляцию."),
    ("raid", "Police conducted a raid at night.", "рейд", "Полиция провела рейд ночью."),
    ("distinctive", "Her voice is distinctive.", "отличительный", "Её голос отличительный."),
    ("transparency", "We value transparency in our team.", "прозрачность", "Мы ценим прозрачность в нашей команде."),
    ("confession", "Her confession was quiet.", "исповедь", "Её исповедь была тихой."),
    ("burst out", "She burst out laughing.", "разразиться", "Она разразилась смехом."),
    ("convoy", "The convoy is on the road.", "конвой", "Конвой на дороге."),
    ("idol", "He is my idol.", "кумир", "Он мой кумир."),
    ("footballer", "He is a famous footballer.", "футболист", "Он известный футболист."),
    ("wood", "The table is made of wood.", "древесина", "Стол сделан из древесины."),
    ("pavement", "The pavement is wet.", "мостовая", "Мостовая мокрая."),
    ("unprecedented", "This is an unprecedented event.", "невиданный", "Это невиданное событие."),
    ("debtor", "The debtor did not pay.", "должник", "Должник не платил."),
    ("artificially", "He smiled artificially.", "искусственно", "Он улыбнулся искусственно."),
    ("rabies", "The dog has rabies.", "бешенство", "У собаки бешенство."),
    ("to gladden", "This news will gladden him.", "обрадовать", "Эта новость его обрадует."),
    ("velvety", "Her voice is velvety.", "бархатный", "Её голос бархатный."),
    ("susceptible", "He is susceptible to this.", "подверженный", "Он подвержен этому."),
    ("noiselessly", "She noiselessly entered the room.", "бесшумно", "Она бесшумно входит в комнату."),
    ("to fascinate", "His stories fascinate me.", "увлекать", "Его рассказы увлекают меня."),
    ("pedal", "The car has a pedal.", "педаль", "У машины есть педаль."),
    ("truthful", "She was always truthful with me.", "правдивый", "Она всегда была правдивой со мной."),
    ("inspire", "His words inspire confidence.", "внушить", "Его слова внушают доверие."),
    ("pupil", "Her pupil is large.", "зрачок", "Её зрачок большой."),
    ("vagabond", "He is a vagabond.", "бродяга", "Он бродяга."),
    ("priceless", "Her smile is priceless.", "бесценный", "Её улыбка бесценная."),
    ("Novosibirsk", "I visited Novosibirsk in summer.", "Новосибирск", "Я посетил Новосибирск летом."),
    ("get upset", "She will get upset if you are late.", "расстроиться", "Она расстроится, если вы опоздаете."),
    ("atheist", "He is an atheist.", "атеист", "Он атеист."),
    ("snort", "He will snort at this.", "хмыкнуть", "Он хмыкнет на это."),
    ("bonus", "The employee received a bonus.", "бонус", "Сотрудник получил бонус."),
    ("jester", "The jester is at court.", "шут", "Шут при дворе."),
    ("incidentally", "I found this incidentally.", "попутно", "Я нашёл это попутно."),
    ("carriage", "They arrived in a carriage.", "карета", "Они прибыли в карете."),
    ("traffic policeman", "The traffic policeman issued a fine.", "гаишник", "Гаишник выписал штраф."),
    ("to be implied", "This is to be implied from his words.", "подразумеваться", "Это подразумевается из его слов."),
    ("ferry", "The ferry is on the river.", "паром", "Паром на реке."),
    ("exalted", "This is exalted language.", "возвышенный", "Это возвышенный язык."),
    ("to cure", "The doctor will cure him.", "вылечить", "Врач вылечит его."),
    ("to forecast", "They forecast rain.", "прогнозировать", "Они прогнозируют дождь."),
    ("accession", "This is accession to the union.", "присоединение", "Это присоединение к союзу."),
    ("inherit", "She will inherit the house.", "унаследовать", "Она унаследует дом."),
    ("swarthy", "He has a swarthy face.", "смуглый", "У него смуглое лицо."),
    ("hurricane", "The hurricane was strong.", "ураган", "Ураган был сильный."),
    ("chip", "He placed a chip on red.", "фишка", "Он поставил фишку на красное."),
    ("expediency", "He chose this for expediency.", "целесообразность", "Он выбрал это для целесообразности."),
    ("transform", "They want to transform the city.", "преобразовать", "Они хотят преобразовать город."),
    ("resilient", "He is a resilient man.", "стойкий", "Он стойкий человек."),
    ("to track", "We track this car.", "отслеживать", "Мы отслеживаем эту машину."),
    ("ethereal", "Her voice is ethereal.", "эфирный", "Её голос эфирный."),
    ("exile", "He was in exile.", "изгнание", "Он был в изгнании."),
    ("turtle", "The turtle slowly crossed the road.", "черепаха", "Черепаха медленно перешла дорогу."),
    ("Chelyabinsk", "I visited Chelyabinsk in summer.", "Челябинск", "Я посетил Челябинск летом."),
    ("antipathy", "She felt antipathy towards him.", "неприязнь", "Она чувствовала неприязнь к нему."),
    ("righteous", "His life was righteous.", "праведный", "Его жизнь была праведной."),
    ("mafia", "The mafia is in the city.", "мафия", "Мафия в городе."),
    ("reel", "The reel is on the table.", "катушка", "Катушка на столе."),
    ("godfather", "He is my son's godfather.", "крестный", "Он крестный моего сына."),
    ("to sew", "I need to sew a dress.", "сшить", "Мне нужно сшить платье."),
    ("dock", "The ship is at the dock.", "док", "Корабль в доке."),
    ("jug", "Fill the jug with water, please.", "кувшин", "Наполните, пожалуйста, кувшин водой."),
    ("television company", "This television company is large.", "телекомпания", "Эта телекомпания большая."),
    ("thinly", "She cut the cheese thinly.", "тонко", "Она тонко резала сыр."),
    ("to warm", "The sun will warm the house.", "греть", "Солнце будет греть дом."),
    ("harmless", "The spider is harmless.", "безобидный", "Паук безобидный."),
    ("immersion", "This is immersion in water.", "погружение", "Это погружение в воду."),
    ("summary", "The news summary was short.", "сводка", "Сводка новостей была короткой."),
    ("defendant", "The defendant is in court.", "подсудимый", "Подсудимый в суде."),
    ("ignorance", "This is ignorance of the law.", "незнание", "Это незнание закона."),
    ("generously", "He helps generously.", "щедро", "Он щедро помогает."),
    ("advertise", "They advertise this book.", "рекламировать", "Они рекламируют эту книгу."),
    ("geometry", "I study geometry at school.", "геометрия", "Я учу геометрию в школе."),
    ("little girl", "The little girl is at home.", "малышка", "Малышка дома."),
    ("entail", "Success will entail work.", "повлечь", "Успех повлечёт работу."),
    ("rhetoric", "His rhetoric was strong.", "риторика", "Его риторика была сильной."),
    ("decorative", "The vase is decorative.", "декоративный", "Ваза декоративная."),
    ("mutual understanding", "Mutual understanding is good.", "взаимопонимание", "Взаимопонимание хорошее."),
    ("border guard", "The border guard checked our passports.", "пограничник", "Пограничник проверил наши паспорта."),
    ("to leak", "Water began to leak.", "потечь", "Вода потекла."),
    ("to break down", "The car began to break down.", "ломаться", "Машина начала ломаться."),
    ("examine", "The doctor will examine the patient.", "обследовать", "Врач обследует пациента."),
    ("to be managed", "This work is to be managed carefully.", "управляться", "Эта работа должна управляться осторожно."),
    ("fiction", "This story is fiction.", "выдумка", "Этот рассказ — выдумка."),
    ("Gypsy", "The Gypsy played the violin.", "цыган", "Цыган играл на скрипке."),
    ("wink", "He will wink at me.", "подмигнуть", "Он подмигнёт мне."),
    ("monograph", "This is a monograph about the war.", "монография", "Это монография о войне."),
    ("bite", "The dog can bite.", "кусать", "Собака будет кусать."),
    ("absurd", "This is absurd.", "абсурд", "Это абсурд."),
    ("fever", "She has a high fever.", "лихорадка", "У неё высокая лихорадка."),
    ("set off", "They set off in the morning.", "пуститься", "Они пустились утром."),
    ("feeble", "His voice is feeble.", "вялый", "Его голос вялый."),
    ("sanitary worker", "The sanitary worker is in the hospital.", "санитар", "Санитар в больнице."),
    ("weekdays", "I work on weekdays.", "будни", "Я работаю по будням."),
    ("Rostov", "We visited Rostov.", "Ростов", "Мы посетили Ростов."),
    ("politeness", "Politeness is important.", "вежливость", "Вежливость важна."),
    ("energetically", "She worked energetically.", "энергично", "Она работала энергично."),
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
        forms.add(word[:-2])
    if word.endswith("d") and len(word) > 4:
        forms.add(word[:-1])
    return forms


IRREGULAR_EN = {
    "made": "make", "went": "go", "gone": "go", "bought": "buy",
    "knew": "know", "known": "know", "sold": "sell", "grew": "grow",
    "grown": "grow", "took": "take", "taken": "take", "gave": "give",
    "given": "give", "saw": "see", "seen": "see", "came": "come",
    "did": "do", "done": "do", "had": "have", "said": "say",
    "told": "tell", "got": "get", "gotten": "get", "found": "find",
    "left": "leave", "kept": "keep", "felt": "feel", "thought": "think",
    "brought": "bring", "stood": "stand", "sat": "sit", "ran": "run",
    "won": "win", "lost": "lose", "met": "meet", "led": "lead",
    "paid": "pay", "spoke": "speak", "written": "write", "wrote": "write",
    "ate": "eat", "eaten": "eat", "drank": "drink", "drunk": "drink",
    "taught": "teach", "caught": "catch", "began": "begin", "begun": "begin",
    "shown": "show", "showed": "show", "built": "build", "held": "hold",
    "heard": "hear", "sent": "send", "spent": "spend", "meant": "mean",
    "needed": "need", "received": "receive", "watched": "watch",
    "placed": "place", "chose": "choose", "lived": "live",
    "crossed": "cross", "checked": "check", "played": "play",
    "worked": "work", "visited": "visit", "cut": "cut",
}


def en_ok(text: str, extra: set[str]) -> list[str]:
    allowed = allow_en | extra
    bad = []
    for raw in re.findall(r"[A-Za-z']+", text):
        w = raw.lower().replace("'", "")
        if not w or w in allowed:
            continue
        if IRREGULAR_EN.get(w, "") in allowed:
            continue
        if any(form in allowed for form in en_forms(w)):
            continue
        if w.endswith("ly") and w[:-2] in allowed:
            continue
        bad.append(raw)
    return bad


RU_ENDINGS = (
    "ями", "ами", "ого", "его", "ому", "ему", "ыми", "ими",
    "ая", "яя", "ое", "ее", "ие", "ые", "ой", "ей", "ий", "ый",
    "ую", "юю", "ов", "ев", "ей", "ам", "ям", "ом", "ем",
    "ах", "ях", "ию", "ью", "ия", "ья", "ие", "ье",
    "ть", "ти", "ла", "ло", "ли", "ет", "ют", "ут", "ит", "ат", "ят",
    "ешь", "ишь", "ете", "ите", "ём", "ем", "им",
    "а", "я", "о", "е", "у", "ю", "ы", "и",
)


def ru_stems(word: str) -> set[str]:
    stems = {word}
    for end in RU_ENDINGS:
        if word.endswith(end) and len(word) - len(end) >= 3:
            stems.add(word[: -len(end)])
    if len(word) >= 5:
        stems.add(word[:5])
        stems.add(word[:4])
    return stems


def ru_ok(text: str, extra: set[str]) -> list[str]:
    allowed = allow_ru | extra
    bad = []
    for raw in re.findall(r"[А-Яа-яЁё-]+", text):
        if raw.replace("-", "") == "":
            continue
        w = raw.replace("ё", "е").replace("Ё", "е").lower()
        if w in allowed:
            continue
        stems = ru_stems(w)
        if any(stem in allowed for stem in stems if len(stem) >= 3):
            continue
        if any(w.startswith(lemma) or lemma.startswith(w) for lemma in allowed if len(lemma) >= 4 and len(w) >= 4):
            continue
        if any(
            w[: max(4, len(w) - 3)] == lemma[: max(4, len(w) - 3)]
            for lemma in allowed
            if abs(len(lemma) - len(w)) <= 4 and min(len(lemma), len(w)) >= 4
        ):
            continue
        if any(stem.startswith(lemma[:4]) or lemma.startswith(stem[:4]) for lemma in allowed for stem in stems if len(lemma) >= 4 and len(stem) >= 4):
            continue
        bad.append(raw)
    return bad


def lemma_tokens_en(en: str) -> set[str]:
    parts = re.findall(r"[A-Za-z']+", en.lower().replace("(", " ").replace(")", " "))
    extra = set(parts)
    extra.discard("to")
    extra.discard("the")
    extra.discard("a")
    extra.discard("an")
    return extra


def lemma_tokens_ru(ru: str) -> set[str]:
    parts = re.findall(r"[А-Яа-яЁё-]+", ru)
    return {p.replace("ё", "е").replace("Ё", "е").lower() for p in parts}


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
        extra_en = lemma_tokens_en(en)
        extra_ru = lemma_tokens_ru(ru)
        for token in en_ok(en_ex, extra_en):
            leftover.append(f"{i} EN leftover {token!r}: {en_ex}")
        for token in ru_ok(ru_ex, extra_ru):
            leftover.append(f"{i} RU leftover {token!r}: {ru_ex}")
        if en.split()[0].lower() not in en_ex.lower() and en.lower() not in en_ex.lower():
            key = en.lower().replace("to ", "")
            if key not in en_ex.lower() and not any(p in en_ex.lower() for p in key.split()):
                leftover.append(f"{i}: EN example missing {en!r}")
        ru_key = ru.lower().replace("ё", "е")
        ru_ex_n = ru_ex.lower().replace("ё", "е")
        first = ru_key.split()[0]
        if first[:4] not in ru_ex_n and first[:3] not in ru_ex_n:
            leftover.append(f"{i}: RU example missing {ru!r}")
        cards.append(make_card(en, en_ex, ru, ru_ex))

    OUT.parent.mkdir(parents=True, exist_ok=True)
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
