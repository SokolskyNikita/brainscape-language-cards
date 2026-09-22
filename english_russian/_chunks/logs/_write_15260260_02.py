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

SRC = PACK / "_chunks" / "deck_15260260_02.csv"
OUT = PACK / "_chunks" / "fixed" / "deck_15260260_02.csv"
LOG = PACK / "_chunks" / "logs" / "deck_15260260_02.txt"

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
        "а", "но", "или", "мою", "твою", "свою", "нашу", "вашу",
        "моего", "твоего", "своего", "нашего", "вашего",
        "хочу", "хочешь", "хочет", "хотим", "хотите", "хотят",
        "пью", "пьёшь", "пьешь", "пьёт", "пьет", "пьём", "пьем", "пьёте", "пьете", "пьют",
    }
}

IRREGULAR = {
    "bought": "buy", "came": "come", "became": "become", "lost": "lose",
    "fought": "fight", "began": "begin", "ran": "run", "ate": "eat",
    "drank": "drink", "saw": "see", "went": "go", "got": "get",
    "gave": "give", "took": "take", "made": "make", "knew": "know",
    "thought": "think", "told": "tell", "left": "leave", "felt": "feel",
    "kept": "keep", "stood": "stand", "sat": "sit", "wrote": "write",
    "grew": "grow", "wore": "wear", "chose": "choose", "spoke": "speak",
    "heard": "hear", "held": "hold", "found": "find", "said": "say",
    "did": "do", "had": "have", "has": "have", "been": "be", "was": "be",
    "were": "be", "is": "be", "are": "be", "am": "be",
    "tore": "tear", "forgot": "forget", "sent": "send", "broke": "break",
    "won": "win", "paid": "pay", "sold": "sell", "built": "build",
    "taught": "teach", "caught": "catch", "led": "lead", "met": "meet",
    "preferred": "prefer", "covered": "cover",
}

allow_en = {
    line.strip().lower()
    for line in (PACK / "_vocab" / "allow_en_15260260.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
} | FUNCTION_EN
allow_ru = {
    line.strip().replace("ё", "е").lower()
    for line in (PACK / "_vocab" / "allow_ru_15260260.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
} | FUNCTION_RU

# (en_lemma, en_ex, ru_lemma, ru_ex)
FIXED = [
    ("axe", "The axe is on the table.", "топор", "Топор на столе."),
    ("incarnation", "She is the incarnation of love.", "воплощение", "Она воплощение любви."),
    ("to navigate", "Learn to navigate the city streets.", "ориентироваться", "Научитесь ориентироваться на улицах города."),
    ("diet", "She started a new diet yesterday.", "диета", "Она начала новую диету вчера."),
    ("hourly", "The hourly pay is high.", "часовой", "Часовая плата высокая."),
    ("sit down", "Please, sit down here.", "присесть", "Пожалуйста, присядьте здесь."),
    ("earned", "He received earned pay.", "заработный", "Он получил заработную плату."),
    ("contemporary", "He is my contemporary.", "современник", "Он мой современник."),
    ("envelope", "The letter is in the envelope.", "конверт", "Письмо в конверте."),
    ("orient", "Let's orient the map.", "ориентировать", "Давайте ориентировать карту."),
    ("be noted", "The error is noted in the text.", "отмечаться", "Ошибка отмечается в тексте."),
    ("to release", "She learned to release her fears.", "отпускать", "Она научилась отпускать свои страхи."),
    ("communism", "He reads about communism.", "коммунизм", "Он читает о коммунизме."),
    ("mm", '"Mm, that tastes good."', "мм", "Мм, это вкусно."),
    ("underground", "The underground station is cold.", "подземный", "Подземная станция холодная."),
    ("whisker", "The cat has a whisker.", "ус", "У кошки есть ус."),
    ("pencil", "I lost my pencil again.", "карандаш", "Я снова потерял свой карандаш."),
    ("to fly out", "I need to fly out tomorrow.", "вылететь", "Мне нужно вылететь завтра."),
    ("to swear", "He began to swear loudly.", "ругаться", "Он начал громко ругаться."),
    ("hare", "The hare ran through the field.", "заяц", "Заяц бежал через поле."),
    ("to invest", "They invest in the company.", "вкладывать", "Они вкладывают в компанию."),
    ("lover", "Her husband has a lover.", "любовник", "У её мужа есть любовник."),
    ("extract", "They extract oil from the earth.", "извлечь", "Они извлекают масло из земли."),
    ("ridiculous", "That idea is ridiculous.", "нелепый", "Эта идея нелепая."),
    ("to please", "I try to please my mother.", "радовать", "Я пытаюсь радовать свою мать."),
    ("incorrectly", "He answered the question incorrectly.", "неправильно", "Он ответил на вопрос неправильно."),
    ("index", "Check the book's index.", "индекс", "Проверьте индекс книги."),
    ("princess", "The princess wore a red dress.", "принцесса", "Принцесса носила красное платье."),
    ("puddle", "There is a puddle on the road.", "лужа", "На дороге есть лужа."),
    ("chaos", "The room was in chaos.", "хаос", "Комната была в хаосе."),
    ("self-government", "The city has self-government.", "самоуправление", "У города есть самоуправление."),
    ("raw", "The meat is raw.", "сырой", "Мясо сырое."),
    ("tragic", "His death was tragic.", "трагический", "Его смерть была трагической."),
    ("psyche", "He has a strong psyche.", "психика", "У него сильная психика."),
    ("asphalt", "The road is covered with asphalt.", "асфальт", "Дорога покрыта асфальтом."),
    ("to be felt", "Tension is felt in the room.", "чувствоваться", "Напряжение чувствуется в комнате."),
    ("portal", "The portal transported us instantly.", "портал", "Портал мгновенно перенёс нас."),
    ("tightly", "The lid sits tightly.", "плотно", "Крышка сидит плотно."),
    ("to announce", "They announce the winner.", "объявлять", "Они объявляют победителя."),
    ("closely", "They worked closely together on the project.", "тесно", "Они тесно работали вместе над проектом."),
    ("infrastructure", "The city's infrastructure needs improvement.", "инфраструктура", "Инфраструктура города нуждается в улучшении."),
    ("session", "The exam session starts tomorrow.", "сессия", "Сессия экзаменов начинается завтра."),
    ("telegram", "I received a telegram yesterday.", "телеграмма", "Я получил телеграмму вчера."),
    ("ritual", "Coffee is my daily ritual.", "ритуал", "Кофе - мой ритуал ежедневно."),
    ("bravely", "She bravely looked at her fear.", "смело", "Она смело смотрела на свой страх."),
    ("eternity", "Love felt like an eternity.", "вечность", "Любовь казалась вечностью."),
    ("organizational", "Organizational work is important for success.", "организационный", "Организационная работа важна для успеха."),
    ("to glow", "The stars began to glow softly.", "светиться", "Звезды начали мягко светиться."),
    ("naive", "She was naive to trust him.", "наивный", "Она была наивна, доверяя ему."),
    ("to get acquainted", "I need to get acquainted with the document.", "ознакомиться", "Мне нужно ознакомиться с документом."),
    ("cognac", "He drinks cognac slowly.", "коньяк", "Он медленно пьёт коньяк."),
    ("deficit", "The budget deficit keeps growing.", "дефицит", "Дефицит бюджета продолжает расти."),
    ("bay", "The bay was calm at dawn.", "залив", "Залив был спокойным на рассвете."),
    ("to tear", "The paper began to tear.", "рваться", "Бумага начала рваться."),
    ("burn", "I must burn the old letters.", "сжечь", "Надо сжечь старые письма."),
    ("nominate", "I will nominate you tomorrow.", "выдвинуть", "Я выдвину тебя завтра."),
    ("ruler", "The ruler made a new law.", "правитель", "Правитель сделал новый закон."),
    ("to be transmitted", "The message is transmitted now.", "передаваться", "Сообщение передаётся сейчас."),
    ("wish", "This is my wish.", "пожелание", "Это моё пожелание."),
    ("pensioner", "The pensioner walks in the park.", "пенсионер", "Пенсионер гуляет в парке."),
    ("infinitely", "He is infinitely kind.", "бесконечно", "Он бесконечно добрый."),
    ("comparatively", "Prices are comparatively low here.", "сравнительно", "Цены здесь сравнительно низкие."),
    ("cash desk", "Please, queue at the cash desk.", "касса", "Пожалуйста, станьте в очередь у кассы."),
    ("weakly", "He smiled weakly at the joke.", "слабо", "Он слабо улыбнулся на шутку."),
    ("punish", "They will punish the guilty party.", "наказать", "Они накажут виновную сторону."),
    ("cop", "The cop arrested the thief.", "мент", "Мент арестовал вора."),
    ("programming", "I love learning programming languages.", "программирование", "Я люблю учить языки программирования."),
    ("scientifically", "They work scientifically.", "научно", "Они работают научно."),
    ("squeeze", "I must squeeze her hand.", "сжать", "Надо сжать её руку."),
    ("bench", "Sit down on the bench, please.", "скамейка", "Пожалуйста, садитесь на скамейку."),
    ("athlete", "The athlete has a gold medal.", "спортсмен", "У спортсмена есть золотая медаль."),
    ("cattle", "The cattle are in the field.", "скот", "Скот на поле."),
    ("invention", "This was an important invention.", "изобретение", "Это было важное изобретение."),
    ("to be suitable", "This fabric is suitable for a dress.", "годиться", "Эта ткань годится для платья."),
    ("algorithm", "The algorithm solved the problem efficiently.", "алгоритм", "Алгоритм эффективно решил проблему."),
    ("to skate", "I love to skate in winter.", "кататься", "Я люблю кататься зимой."),
    ("restructuring", "The company announced a major restructuring.", "перестройка", "Компания объявила о крупной перестройке."),
    ("slow", "This train is slow.", "медленный", "Этот поезд медленный."),
    ("employer", "My employer increased my salary.", "работодатель", "Мой работодатель поднял мою зарплату."),
    ("brick", "I bought a red brick yesterday.", "кирпич", "Вчера я купил красный кирпич."),
    ("to persuade", "He tried to persuade his friend.", "убеждать", "Он пытался убеждать своего друга."),
    ("clinic", "She works at the local clinic.", "клиника", "Она работает в местной клинике."),
    ("impossibility", "Achieving perfection is an impossibility.", "невозможность", "Достижение совершенства - невозможность."),
    ("generate", "Ideas generate new questions.", "порождать", "Идеи порождают новые вопросы."),
    ("rent", "We must pay the rent.", "аренда", "Нам надо платить аренду."),
    ("to miss", "I often miss the train.", "пропускать", "Я часто пропускаю поезд."),
    ("prefer", "I preferred tea today.", "предпочесть", "Я предпочёл чай сегодня."),
    ("to be fulfilled", "Her dream will be fulfilled soon.", "исполниться", "Её мечта скоро исполнится."),
    ("concentrate", "Please concentrate your attention.", "сосредоточить", "Пожалуйста, сосредоточьте своё внимание."),
    ("mechanical", "This is a mechanical system.", "механический", "Это механическая система."),
    ("back of the head", "He felt a pain in the back of the head.", "затылок", "Он почувствовал боль в затылке."),
    ("irritation", "His comment created irritation.", "раздражение", "Его комментарий создал раздражение."),
    ("thoughtfully", "She gazed thoughtfully at him.", "задумчиво", "Она задумчиво смотрела на него."),
    ("inflation", "Inflation is a problem this year.", "инфляция", "Инфляция - проблема в этом году."),
    ("outline", "Let's outline our plan today.", "наметить", "Давайте наметим наш план на сегодня."),
    ("to stretch", "I like to stretch in the morning.", "потянуться", "Мне нравится потянуться утром."),
    ("steppe", "Horses ran on the steppe.", "степь", "Лошади бежали по степи."),
    ("calendar", "Check the calendar for today's date.", "календарь", "Проверьте календарь на сегодняшнюю дату."),
    ("sunset", "The sunset was orange.", "закат", "Закат был оранжевым."),
    ("roughly", "This costs roughly ten.", "грубо", "Это стоит грубо десять."),
]


def en_forms(word: str) -> set[str]:
    forms = {word}
    if word in IRREGULAR:
        forms.add(IRREGULAR[word])
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
    return forms


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


def ru_ok(text: str, extra: set[str]) -> list[str]:
    bad = []
    pool = allow_ru | extra
    for raw in re.findall(r"[А-Яа-яЁё-]+", text):
        w = raw.replace("ё", "е").replace("Ё", "е").lower()
        if not w or w in {"-"} or w in pool:
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
    for i, (en, en_ex, ru, ru_ex) in enumerate(FIXED, 1):
        orig = originals[i - 1]
        if orig["qMdBody"] != en:
            leftover.append(f"{i}: gloss changed {orig['qMdBody']!r} -> {en!r}")
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
