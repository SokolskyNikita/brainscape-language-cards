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

SRC = PACK / "_chunks" / "deck_15260266_00.csv"
OUT = PACK / "_chunks" / "fixed" / "deck_15260266_00.csv"
LOG = PACK / "_chunks" / "logs" / "deck_15260266_00.txt"

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
    "who", "what", "when", "where", "why", "how", "which", "that",
}

FUNCTION_RU = {
    "я", "мне", "меня", "мной", "мой", "моя", "мое", "моё", "мои", "мою",
    "мы", "нам", "нас", "нами", "наш", "наша", "наше", "наши", "нашу",
    "ты", "тебе", "тебя", "тобой", "твой", "твоя", "твое", "твоё", "твои",
    "вы", "вам", "вас", "вами", "ваш", "ваша", "ваше", "ваши", "вашу",
    "он", "она", "оно", "они", "его", "ее", "её", "ей", "ему", "им", "их",
    "ими", "ним", "ней", "ними", "него", "нее", "неё",
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
    "мне", "тебе", "ему", "ей", "нам", "вам", "им",
}

allow_en = {
    line.strip().lower()
    for line in (PACK / "_vocab" / "allow_en_15260266.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_ru = {
    line.strip().replace("ё", "е").lower()
    for line in (PACK / "_vocab" / "allow_ru_15260266.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_en |= FUNCTION_EN
allow_ru |= FUNCTION_RU

# (en_lemma, en_ex, ru_lemma, ru_ex)
FIXED = [
    ("tiny", "I see a tiny house.", "крошечный", "Я вижу крошечный дом."),
    ("properly", "He cannot explain it properly.", "толком", "Он не может толком это объяснить."),
    ("niche", "He found his niche in art.", "ниша", "Он нашел свою нишу в искусстве."),
    ("condom", "He bought a condom.", "презерватив", "Он купил презерватив."),
    ("to proclaim", "He wants to proclaim the truth.", "заявить", "Он хочет заявить правду."),
    ("voluntary", "The work is voluntary.", "добровольный", "Работа добровольная."),
    ("removal", "They need the removal of the table.", "удаление", "Им нужно удаление стола."),
    ("few", "Only a few know this.", "немногий", "Только немногие это знают."),
    ("affect", "This will affect the result.", "сказаться", "Это скажется на результате."),
    ("to fling open", "She will fling open the door.", "распахнуть", "Она распахнет дверь."),
    ("bark", "The bark of the tree is dry.", "кора", "Кора дерева сухая."),
    ("untruth", "He told an untruth.", "неправда", "Он сказал неправду."),
    ("to settle", "We will settle near the river.", "расположиться", "Мы расположимся у реки."),
    ("voluntarily", "This was done voluntarily.", "добровольно", "Это сделано добровольно."),
    ("disaster", "The war was a disaster.", "бедствие", "Война была бедствием."),
    ("baron", "The baron lived in a large house.", "барон", "Барон жил в большом доме."),
    ("traction", "The engine has strong traction.", "тяга", "У двигателя сильная тяга."),
    ("slide", "I like to slide on the snow.", "скользить", "Мне нравится скользить по снегу."),
    ("surgeon", "The surgeon works in the hospital.", "хирург", "Хирург работает в больнице."),
    ("fisherman", "The fisherman caught a big fish.", "рыбак", "Рыбак поймал большую рыбу."),
    ("lever", "He pulls the lever.", "рычаг", "Он тянет рычаг."),
    ("inaccessible", "The house is inaccessible.", "недоступный", "Дом недоступен."),
    ("sheet", "I wash the sheet.", "простыня", "Я мою простыню."),
    ("formally", "He formally accepted the offer.", "формально", "Он формально принял предложение."),
    ("Israeli", "This is an Israeli city.", "израильский", "Это израильский город."),
    ("ninety", "She is ninety years old.", "девяносто", "Ей девяносто лет."),
    ("interested", "She is interested in the book.", "заинтересованный", "Она заинтересована в книге."),
    ("applied", "This is applied science.", "прикладной", "Это прикладная наука."),
    ("diameter", "The diameter of the circle is ten meters.", "диаметр", "Диаметр круга - десять метров."),
    ("dressed", "She was dressed in red.", "одетый", "Она была одета в красное."),
    ("auction", "The house was sold at auction.", "аукцион", "Дом продали на аукционе."),
    ("moan", "I heard a soft moan.", "стон", "Я слышал тихий стон."),
    ("prostitute", "She worked as a prostitute.", "проститутка", "Она работала проституткой."),
    ("invariably", "He is invariably ready.", "неизменно", "Он неизменно готов."),
    ("five hundred", "I have five hundred books.", "пятьсот", "У меня пятьсот книг."),
    ("to be keen on", "She is keen on music.", "увлекаться", "Она увлекается музыкой."),
    ("to glance", "He likes to glance at the door.", "поглядывать", "Он любит поглядывать на дверь."),
    ("boil", "Mother will boil the meat.", "варить", "Мама будет варить мясо."),
    ("Islamic", "Islamic art is old.", "исламский", "Исламское искусство старое."),
    ("deposit", "They found a gold deposit.", "месторождение", "Они нашли золотое месторождение."),
    ("to get lost", "I always get lost in this city.", "теряться", "Я всегда теряюсь в этом городе."),
    ("branded", "This is a branded bag.", "фирменный", "Это фирменная сумка."),
    ("hearth", "The family sat by the hearth.", "очаг", "Семья сидела у очага."),
    ("to sing", "I want to sing this song.", "спеть", "Я хочу спеть эту песню."),
    ("symbolic", "The gift was symbolic.", "символический", "Подарок был символическим."),
    ("to iron", "I need to iron my shirt.", "гладить", "Мне нужно гладить рубашку."),
    ("withdraw", "He wants to withdraw from the room.", "удалиться", "Он хочет удалиться из комнаты."),
    ("compromise", "We found a compromise.", "компромисс", "Мы нашли компромисс."),
    ("to exhibit", "They exhibit new pictures.", "выставлять", "Они выставляют новые картины."),
    ("tenant", "The tenant lives here.", "жилец", "Жилец живет здесь."),
    ("Georgian", "I love Georgian wine.", "грузинский", "Я люблю грузинское вино."),
    ("cabbage", "I have cabbage in my garden.", "капуста", "У меня в саду есть капуста."),
    ("decrease", "The number will decrease.", "уменьшаться", "Число будет уменьшаться."),
    ("nervously", "She waited nervously.", "нервно", "Она нервно ждала."),
    ("to have lunch", "We want to have lunch together.", "обедать", "Мы хотим обедать вместе."),
    ("innovative", "This is an innovative idea.", "инновационный", "Это инновационная идея."),
    ("imagine", "I imagine a world without war.", "воображать", "Я воображаю мир без войны."),
    ("immortal", "The hero is immortal.", "бессмертный", "Герой бессмертный."),
    ("vague", "His answer was vague.", "смутный", "Его ответ был смутным."),
    ("theme", "The theme of the book is war.", "тематика", "Тематика книги - война."),
    ("immerse", "I want to immerse in work.", "погрузиться", "Я хочу погрузиться в работу."),
    ("retail", "This is a retail store.", "розничный", "Это розничный магазин."),
    ("traveler", "The traveler is in the city.", "путешественник", "Путешественник в городе."),
    ("trio", "The trio is here.", "тройка", "Тройка здесь."),
    ("holder", "He is the holder of the prize.", "обладатель", "Он обладатель приза."),
    ("desperately", "He desperately wants to leave.", "отчаянно", "Он отчаянно хочет уйти."),
    ("designer", "The designer made a new dress.", "дизайнер", "Дизайнер сделал новое платье."),
    ("run", "The run helps me.", "бег", "Бег помогает мне."),
    ("beginner", "He is a beginner at this work.", "начинающий", "Он начинающий в этой работе."),
    ("accountant", "The accountant works here.", "бухгалтер", "Бухгалтер работает здесь."),
    ("to state", "They state the result.", "констатировать", "Они констатируют результат."),
    ("persecution", "Persecution of the people must stop.", "преследование", "Преследование народа должно остановиться."),
    ("special service", "The special service found the man.", "спецслужба", "Спецслужба нашла человека."),
    ("to clap", "I heard him clap.", "хлопнуть", "Я слышал, как он хлопнул."),
    ("intervene", "I will intervene in their talk.", "вмешаться", "Я вмешаюсь в их разговор."),
    ("clarity", "I need clarity.", "ясность", "Мне нужна ясность."),
    ("blonde", "She is a beautiful blonde.", "блондинка", "Она красивая блондинка."),
    ("butt", "He sits on his butt.", "жопа", "Он сидит на жопе."),
    ("defend", "I will defend my idea.", "отстаивать", "Я буду отстаивать свою идею."),
    ("prescribe", "The doctor will prescribe rest.", "прописать", "Врач пропишет отдых."),
    ("to inhabit", "They inhabit this land.", "обитать", "Они обитают на этой земле."),
    ("to end up", "He ended up in the city.", "оказаться", "Он оказался в городе."),
    ("dominance", "They want dominance in the region.", "господство", "Они хотят господства в области."),
    ("loading", "The loading of the file is slow.", "загрузка", "Загрузка файла медленная."),
    ("apostle", "The apostle spoke to the people.", "апостол", "Апостол говорил с народом."),
    ("infection", "The infection is dangerous.", "инфекция", "Инфекция опасна."),
    ("galaxy", "Our galaxy is large.", "галактика", "Наша галактика большая."),
    ("interior", "The interior of the house is beautiful.", "интерьер", "Интерьер дома красивый."),
    ("elimination", "Elimination of the problem is needed.", "устранение", "Устранение проблемы нужно."),
    ("torturous", "The pain was torturous.", "мучительный", "Боль была мучительной."),
    ("harp", "She played the harp.", "арфа", "Она играла на арфе."),
    ("relieve", "Music can relieve your pain.", "облегчить", "Музыка может облегчить вашу боль."),
    ("shaft", "The machine needs a new shaft.", "вал", "Машине нужен новый вал."),
    ("to take off", "The bird is ready to take off.", "взлететь", "Птица готова взлететь."),
    ("premise", "The premise is not true.", "предпосылка", "Предпосылка неверна."),
    ("to separate", "Please separate the paper.", "отделять", "Пожалуйста, отделите бумагу."),
    ("pretext", "He is here under the pretext of work.", "предлог", "Он здесь под предлогом работы."),
    ("Olympic", "He has an Olympic medal.", "олимпийский", "У него есть олимпийская медаль."),
    ("to move", "I cannot move.", "шевелиться", "Я не могу шевелиться."),
    ("to steal", "They steal from the store.", "воровать", "Они воруют из магазина."),
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


def en_ok(text: str) -> list[str]:
    bad = []
    for raw in re.findall(r"[A-Za-z']+", text):
        w = raw.lower().replace("'", "")
        if not w or w in allow_en:
            continue
        if IRREGULAR_EN.get(w, "") in allow_en:
            continue
        if any(form in allow_en for form in en_forms(w)):
            continue
        if w.endswith("ly") and w[:-2] in allow_en:
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


IRREGULAR_EN = {
    "made": "make", "went": "go", "gone": "go", "bought": "buy",
    "knew": "know", "known": "know", "sold": "sell", "grew": "grow",
    "grown": "grow", "took": "take", "taken": "take", "gave": "give",
    "given": "give", "saw": "see", "seen": "see", "came": "come",
    "did": "do", "done": "do", "had": "have", "said": "say",
    "told": "tell", "got": "get", "found": "find", "left": "leave",
    "kept": "keep", "felt": "feel", "thought": "think", "brought": "bring",
    "stood": "stand", "sat": "sit", "ran": "run", "won": "win",
    "lost": "lose", "met": "meet", "led": "lead", "paid": "pay",
    "spoke": "speak", "written": "write", "wrote": "write",
    "ate": "eat", "eaten": "eat", "drank": "drink", "drunk": "drink",
    "sits": "sit", "caught": "catch", "heard": "hear", "broke": "break",
}


def ru_ok(text: str) -> list[str]:
    bad = []
    for raw in re.findall(r"[А-Яа-яЁё-]+", text):
        if raw.replace("-", "") == "":
            continue
        w = raw.replace("ё", "е").replace("Ё", "е").lower()
        if w in allow_ru:
            continue
        stems = ru_stems(w)
        if any(stem in allow_ru for stem in stems if len(stem) >= 3):
            continue
        if any(w.startswith(lemma) or lemma.startswith(w) for lemma in allow_ru if len(lemma) >= 4 and len(w) >= 4):
            continue
        if any(
            w[: max(4, len(w) - 3)] == lemma[: max(4, len(w) - 3)]
            for lemma in allow_ru
            if abs(len(lemma) - len(w)) <= 4 and min(len(lemma), len(w)) >= 4
        ):
            continue
        if any(stem.startswith(lemma[:4]) or lemma.startswith(stem[:4]) for lemma in allow_ru for stem in stems if len(lemma) >= 4 and len(stem) >= 4):
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
        allow_en.add(en.lower())
        allow_ru.add(ru.replace("ё", "е").lower())
        for part in re.split(r"[\s,;]+", en.lower()):
            part = re.sub(r"^(to|the|a|an|be|on)$", "", part).strip()
            if part:
                allow_en.add(part)
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
        if ru_key[:4] not in ru_ex_n and ru_key[:3] not in ru_ex_n:
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
