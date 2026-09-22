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

SRC = PACK / "_chunks" / "deck_15260257_02.csv"
OUT = PACK / "_chunks" / "fixed" / "deck_15260257_02.csv"
LOG = PACK / "_chunks" / "logs" / "deck_15260257_02.txt"

FUNCTION = {
    "a", "the", "is", "be", "i", "you", "he", "she", "it", "we", "they",
    "my", "and", "or", "in", "on", "at", "to", "of", "for", "with", "from",
    "not", "his", "him", "her", "their", "them", "our", "us", "me", "am",
    "are", "was", "were", "been", "being", "this", "that", "these", "those",
    "an", "as", "by", "into", "about", "than", "then", "so", "if", "but",
    "its", "your", "did", "does", "has", "have", "had", "will", "can",
    "could", "would", "should", "may", "might", "must", "do", "who", "what",
    "when", "where", "why", "how", "which", "while", "now", "here", "there",
    "very", "too", "also", "just", "only", "please", "yes", "no", "up",
    "down", "out", "off", "over", "after", "before", "again", "once",
    "every", "any", "some", "all", "each", "one", "two", "three", "four",
    "five", "six", "seven", "eight", "nine", "ten",
}

allow_en = {
    line.strip().lower()
    for line in (PACK / "_vocab" / "allow_en_15260257.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_ru = {
    line.strip().replace("ё", "е").lower()
    for line in (PACK / "_vocab" / "allow_ru_15260257.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_en |= FUNCTION

# (en_lemma, en_ex, ru_lemma, ru_ex)
FIXED = [
    ("investigator", "The investigator examined the crime scene.", "следователь", "Следователь осмотрел место преступления."),
    ("freeze", "Suddenly, I heard a noise and froze.", "замереть", "Вдруг я услышал шум и замер."),
    ("embassy", "The embassy issued new recommendations.", "посольство", "Посольство выпустило новые рекомендации."),
    ("useless", "This tool is completely useless.", "бесполезный", "Этот инструмент совершенно бесполезен."),
    ("piece of paper", "I found a piece of paper.", "бумажка", "Я нашёл бумажку."),
    ("thread", "She lost the thread of conversation.", "нить", "Она потеряла нить разговора."),
    ("everyday life", "Technology is part of everyday life.", "быт", "Технология — часть быта."),
    ("workshop", "He spends hours in his workshop.", "мастерская", "Он сидит в своей мастерской часами."),
    ("underwater", "I see an underwater cave.", "подводный", "Я вижу подводную пещеру."),
    ("planning", "Planning a trip needs time.", "планирование", "Планирование поездки требует времени."),
    ("prophet", "The prophet saw the war.", "пророк", "Пророк видел войну."),
    ("pack", "I bought a pack of cigarettes.", "пачка", "Я купил пачку сигарет."),
    ("businessman", "The businessman closed a major deal.", "бизнесмен", "Бизнесмен заключил крупную сделку."),
    ("banner", "The soldiers raised the banner.", "знамя", "Солдаты подняли знамя."),
    ("to cover", "The fire will cover the forest.", "охватить", "Огонь охватит лес."),
    ("to disturb", "I didn't mean to disturb you.", "беспокоить", "Я не хотел вас беспокоить."),
    ("partially", "The door was partially open.", "частично", "Дверь была частично открыта."),
    ("flesh", "The wound shows his flesh.", "плоть", "Рана показывает его плоть."),
    ("Bible", "She reads the Bible every morning.", "библия", "Она читает Библию каждое утро."),
    ("productivity", "Productivity is high now.", "производительность", "Производительность сейчас высокая."),
    ("setting", "This setting is important.", "настройка", "Эта настройка важна."),
    ("expand", "We plan to expand our business.", "расширить", "Мы планируем расширить наш бизнес."),
    ("inclined", "He is inclined to wait.", "склонный", "Он склонен ждать."),
    ("to part", "They part at the airport.", "расстаться", "Они расстаются в аэропорту."),
    ("repeatedly", "He said this repeatedly.", "неоднократно", "Он неоднократно говорил это."),
    ("gram", "Add one gram of salt.", "грамм", "Добавьте один грамм соли."),
    ("oven", "The oven is hot now.", "печь", "Печь сейчас горячая."),
    ("originally", "Originally, it was a small village.", "изначально", "Изначально это была маленькая деревня."),
    ("hidden", "The letter is hidden.", "скрытый", "Письмо скрыто."),
    ("taxi", "I need a taxi.", "такси", "Мне нужно такси."),
    ("shine", "The stars shine brightly at night.", "сиять", "Звезды сияют ярко ночью."),
    ("salt", "Pass the salt, please.", "соль", "Передай, пожалуйста, соль."),
    ("away", "Go away immediately!", "прочь", "Уходи прочь сразу!"),
    ("dare", "Who dares to challenge me?", "сметь", "Кто смеет бросить мне вызов?"),
    ("consultation", "I scheduled a doctor's consultation today.", "консультация", "Я назначил консультацию у врача на сегодня."),
    ("to throw", "He will throw the stone.", "бросить", "Он бросит камень."),
    ("to adhere", "We strive to adhere to the rules.", "придерживаться", "Мы стремимся придерживаться правил."),
    ("to greet", "She wants to greet the guests.", "приветствовать", "Она хочет приветствовать гостей."),
    ("to increase", "Prices increase every year.", "увеличиваться", "Цены увеличиваются каждый год."),
    ("hostile", "They encountered hostile forces unexpectedly.", "вражеский", "Они неожиданно столкнулись с вражескими силами."),
    ("handkerchief", "She offered him a clean handkerchief.", "платок", "Она предложила ему чистый платок."),
    ("fall asleep", "I often fall asleep when I read.", "засыпать", "Я часто засыпаю, когда читаю."),
    ("cancer", "She has cancer.", "рак", "У неё рак."),
    ("to wake up", "I need to wake up early.", "просыпаться", "Мне нужно рано просыпаться."),
    ("mysterious", "The forest looked mysterious at night.", "таинственный", "Лес выглядел таинственным ночью."),
    ("programmer", "The programmer found an error quickly.", "программист", "Программист быстро нашёл ошибку."),
    ("security guard", "The security guard nodded.", "охранник", "Охранник кивнул."),
    ("alongside", "She worked alongside experts.", "наряду", "Она работала наряду с экспертами."),
    ("collective", "Their collective effort was strong.", "коллективный", "Их коллективное усилие было сильным."),
    ("video", "I watched the video on the internet.", "видео", "Я смотрел видео в интернете."),
    ("biological", "Biological processes are important.", "биологический", "Биологические процессы важны."),
    ("football", "I love watching football.", "футбол", "Я люблю смотреть футбол."),
    ("efficiently", "She works efficiently.", "эффективно", "Она работает эффективно."),
    ("nonsense", "This idea is complete nonsense.", "бред", "Эта идея - полный бред."),
    ("mile", "I ran a mile yesterday.", "миля", "Вчера я бежал милю."),
    ("cursed", "The cursed book brought them death.", "проклятый", "Проклятая книга принесла им смерть."),
    ("breed", "She loves her new dog breed.", "порода", "Она любит свою новую породу собак."),
    ("outsider", "He felt like an outsider at work.", "посторонний", "Он чувствовал себя посторонним на работе."),
    ("chicken", "I cooked chicken for dinner.", "курица", "Я готовил курицу на ужин."),
    ("cleanliness", "Cleanliness is important.", "чистота", "Чистота важна."),
    ("liberal", "She holds liberal views on education.", "либеральный", "Она придерживается либеральных взглядов на образование."),
    ("to escape", "He managed to escape.", "убежать", "Ему удалось убежать."),
    ("to cut off", "Please cut off this line.", "отрезать", "Пожалуйста, отрежьте эту линию."),
    ("extensive", "They conducted extensive research on the topic.", "обширный", "Они провели обширное исследование по теме."),
    ("incident", "The incident was a shock to the town.", "происшествие", "Происшествие было шоком для города."),
    ("highway", "The car is on the highway.", "шоссе", "Машина на шоссе."),
    ("knock", "Please knock before entering.", "стучать", "Пожалуйста, стучите перед входом."),
    ("cancel", "They decided to cancel the meeting.", "отменить", "Они решили отменить встречу."),
    ("pit", "He fell into a deep pit.", "яма", "Он упал в глубокую яму."),
    ("to be subject to", "Prices are subject to change.", "подлежать", "Цены подлежат изменению."),
    ("idiot", "He acted like a complete idiot.", "идиот", "Он вёл себя как полный идиот."),
    ("creator", "The creator wrote this book.", "создатель", "Создатель написал эту книгу."),
    ("observance", "Strict observance of rules is important.", "соблюдение", "Строгое соблюдение правил важно."),
    ("captivity", "He escaped captivity after five years.", "плен", "Он убежал из плена после пяти лет."),
    ("spoon", "I drink tea with a spoon.", "ложка", "Я пью чай ложкой."),
    ("fuel", "The car needs fuel.", "топливо", "Машине нужно топливо."),
    ("come", "Winter will come soon.", "настать", "Зима скоро настанет."),
    ("barely", "He barely said a word.", "еле", "Он еле сказал слово."),
    ("magic", "Her magic was strong.", "магия", "Её магия была сильной."),
    ("to hug", "I want to hug you.", "обнять", "Я хочу обнять тебя."),
    ("voter", "Every voter has an important choice.", "избиратель", "У каждого избирателя есть важный выбор."),
    ("meaningless", "This argument is completely meaningless.", "бессмысленный", "Этот аргумент совершенно бессмысленен."),
    ("gallery", "I see art in the gallery.", "галерея", "Я вижу искусство в галерее."),
    ("coin", "I found a coin under the sofa.", "монета", "Я нашёл монету под диваном."),
    ("finance", "I study finance at university.", "финансы", "Я учу финансы в университете."),
    ("liquid", "Water is a clear liquid.", "жидкость", "Вода - это прозрачная жидкость."),
    ("half a year", "I studied there for half a year.", "полгода", "Я учился там полгода."),
    ("vote", "I will vote tomorrow morning.", "голосовать", "Я буду голосовать завтра утром."),
    ("fundamental", "Respect is fundamental in a relationship.", "фундаментальный", "Уважение фундаментально в отношениях."),
    ("pole", "The bird sat on the pole.", "столб", "Птица села на столб."),
    ("bridegroom", "The bridegroom looked happy.", "жених", "Жених выглядел счастливым."),
    ("defender", "He became the city's brave defender.", "защитник", "Он стал смелым защитником города."),
    ("drive", "Dogs drive the horses.", "гнать", "Собаки гонят лошадей."),
    ("inherent", "Fear is inherent in war.", "присущий", "Страх присущ войне."),
    ("virus", "They spread the virus worldwide.", "вирус", "Они распространили вирус по всему миру."),
    ("stormy", "Their relationship was stormy.", "бурный", "Их отношения были бурными."),
    ("to condition", "This will condition our success.", "обусловить", "Это обусловит наш успех."),
    ("guard", "Dogs guard the house at night.", "охранять", "Собаки охраняют дом ночью."),
    ("dense", "The forest was dense.", "плотный", "Лес был плотным."),
    ("wash", "I need to wash my car.", "мыть", "Мне нужно мыть машину."),
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
    irregular = {
        "heard": "hear",
        "froze": "freeze",
        "lost": "lose",
        "bought": "buy",
        "found": "find",
        "saw": "see",
        "said": "say",
        "ran": "run",
        "felt": "feel",
        "held": "hold",
        "wrote": "write",
        "sat": "sit",
        "became": "become",
        "fell": "fall",
        "took": "take",
        "made": "make",
        "got": "get",
        "came": "come",
        "went": "go",
        "did": "do",
        "had": "have",
        "was": "be",
        "were": "be",
        "been": "be",
        "has": "have",
        "does": "do",
        "asleep": "sleep",
        "issued": "issue",
        "watched": "watch",
        "worked": "work",
        "looked": "look",
        "cooked": "cook",
        "studied": "study",
        "escaped": "escape",
        "decided": "decide",
        "completed": "complete",
        "acted": "act",
        "scheduled": "schedule",
        "encountered": "encounter",
        "conducted": "conduct",
        "offered": "offer",
        "raised": "raise",
        "closed": "close",
        "planned": "plan",
        "needed": "need",
        "managed": "manage",
        "spread": "spread",
        "read": "read",
    }
    if word in irregular:
        forms.add(irregular[word])
    return forms


def en_ok(text: str) -> list[str]:
    bad = []
    for raw in re.findall(r"[A-Za-z']+", text):
        w = raw.lower().replace("'", "")
        if not w or w in allow_en:
            continue
        if any(form in allow_en for form in en_forms(w)):
            continue
        if w.endswith("ly") and w[:-2] + "l" in allow_en:
            continue
        bad.append(raw)
    return bad


def ru_ok(text: str) -> list[str]:
    bad = []
    ru_function = {
        "я", "ты", "он", "она", "мы", "вы", "они", "мне", "меня", "тебя", "тебе",
        "его", "ему", "ее", "ей", "её", "нас", "нам", "вас", "вам", "их", "им",
        "мой", "моя", "мое", "моё", "мои", "твой", "свой", "своя", "свое", "своё",
        "свои", "свою", "своей", "наш", "нашa", "нашe", "этот", "эта", "это",
        "эти", "этот", "той", "том", "тем", "той", "был", "была", "было", "были",
        "нет", "не", "ни", "да", "ли", "бы", "же", "ведь", "вот", "и", "а", "но",
        "или", "да", "если", "чтобы", "как", "что", "в", "на", "из", "к", "у",
        "о", "об", "от", "до", "за", "при", "про", "со", "с", "по", "для", "без",
        "над", "под", "при", "через", "между", "перед", "после", "около",
    }
    for raw in re.findall(r"[А-Яа-яЁё-]+", text):
        w = raw.replace("ё", "е").replace("Ё", "е").lower()
        if w in allow_ru or w in ru_function:
            continue
        if any(w.startswith(lemma) or lemma.startswith(w) for lemma in allow_ru if len(lemma) >= 4 and len(w) >= 4):
            continue
        if any(w[: max(4, len(w) - 3)] == lemma[: max(4, len(w) - 3)] for lemma in allow_ru if abs(len(lemma) - len(w)) <= 4 and min(len(lemma), len(w)) >= 4):
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
