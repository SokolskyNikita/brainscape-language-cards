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

SRC = PACK / "_chunks" / "deck_15260260_00.csv"
OUT = PACK / "_chunks" / "fixed" / "deck_15260260_00.csv"
LOG = PACK / "_chunks" / "logs" / "deck_15260260_00.txt"

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
    for line in (PACK / "_vocab" / "allow_en_15260260.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_ru = {
    line.strip().replace("ё", "е").lower()
    for line in (PACK / "_vocab" / "allow_ru_15260260.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_en |= FUNCTION_EN
allow_ru |= FUNCTION_RU

# (en_lemma, en_ex, ru_lemma, ru_ex)
FIXED = [
    ("mixture", "The soup is a smooth mixture.", "смесь", "Суп - это гладкая смесь."),
    ("potato", "I have a potato in my garden.", "картошка", "У меня в саду есть картошка."),
    ("melody", "The melody sounds in my head.", "мелодия", "Мелодия звучит в моей голове."),
    ("tasty", "The soup looks very tasty.", "вкусный", "Суп выглядит очень вкусным."),
    ("sixty", "She turned sixty today.", "шестьдесят", "Ей исполнилось шестьдесят сегодня."),
    ("mutter", "She muttered a word.", "пробормотать", "Она пробормотала слово."),
    ("radio station", "I listen to that radio station every day.", "радиостанция", "Я слушаю эту радиостанцию каждый день."),
    ("on foot", "I go to the city on foot.", "пешком", "Я иду в город пешком."),
    ("bureau", "I contacted the bureau.", "бюро", "Я связался с бюро."),
    ("irritate", "Loud noises irritate me.", "раздражать", "Громкие звуки раздражают меня."),
    ("collision", "The collision was on the road.", "столкновение", "Столкновение было на дороге."),
    ("ideological", "Their question was ideological.", "идеологический", "Их вопрос был идеологическим."),
    ("postpone", "We postponed the meeting.", "отложить", "Мы отложили встречу."),
    ("fine", "He received a fine for speed.", "штраф", "Он получил штраф за скорость."),
    ("Spanish", "I learn Spanish this year.", "испанский", "Я учу испанский в этом году."),
    ("torture", "They torture him.", "мучить", "Они мучают его."),
    ("addition", "This text needs an addition.", "дополнение", "Этому тексту нужно дополнение."),
    ("to obey", "Soldiers obey the command.", "подчиняться", "Солдаты подчиняются команде."),
    ("Volga", "The Volga flows through the land.", "Волга", "Волга течёт через землю."),
    ("healthcare", "Healthcare is an important right.", "здравоохранение", "Здравоохранение - важное право."),
    ("decisive", "He takes a decisive step.", "решительный", "Он делает решительный шаг."),
    ("outward", "He looked outward at the horizon.", "наружу", "Он смотрел наружу на горизонт."),
    ("lunar", "The lunar landscape is beautiful.", "лунный", "Лунный пейзаж красивый."),
    ("priority", "Health is my top priority.", "приоритет", "Здоровье - мой главный приоритет."),
    ("gasoline", "The car needs more gasoline.", "бензин", "Машине нужно больше бензина."),
    ("Leningrad", "I visited Leningrad recently.", "Ленинград", "Я недавно посетил Ленинград."),
    ("intervention", "They want intervention now.", "вмешательство", "Они хотят вмешательства сейчас."),
    ("grain", "A grain is on the table.", "зерно", "Зерно лежит на столе."),
    ("parking", "Parking is always full.", "стоянка", "Стоянка всегда полная."),
    ("shoes", "I bought new shoes yesterday.", "обувь", "Вчера я купил новую обувь."),
    ("anew", "Let's start anew tomorrow.", "заново", "Давайте начнём заново завтра."),
    ("inevitably", "Winter inevitably follows autumn.", "неизбежно", "Зима неизбежно следует за осенью."),
    ("indigenous", "Indigenous people live on this land.", "коренной", "Коренной народ живёт на этой земле."),
    ("demonstration", "The demonstration goes through the city.", "демонстрация", "Демонстрация идёт через город."),
    ("harmony", "They lived in perfect harmony.", "гармония", "Они жили в идеальной гармонии."),
    ("orientation", "Orientation helps in work.", "ориентация", "Ориентация помогает в работе."),
    ("module", "The course includes five modules.", "модуль", "Курс включает пять модулей."),
    ("to be subjected", "They are subjected to the law.", "подвергаться", "Они подвергаются закону."),
    ("to promise", "I promised to come.", "пообещать", "Я пообещал прийти."),
    ("everyday", "Everyday work is complex.", "повседневный", "Повседневная работа сложная."),
    ("mercy", "She wants mercy.", "милость", "Она хочет милости."),
    ("elementary", "This question is elementary.", "элементарный", "Этот вопрос элементарный."),
    ("analyze", "We analyze the text thoroughly.", "анализировать", "Мы тщательно анализируем текст."),
    ("interface", "The software interface is simple.", "интерфейс", "Интерфейс программы простой."),
    ("to encompass", "The plan will encompass the whole region.", "охватывать", "План будет охватывать всю область."),
    ("to press", "Don't press the door.", "давить", "Не давите на дверь."),
    ("intensification", "We see intensification of the storm.", "усиление", "Мы видим усиление бури."),
    ("unfaithful", "He was unfaithful to her.", "неверный", "Он был неверен ей."),
    ("grouping", "The grouping of stars was large.", "группировка", "Группировка звёзд была большой."),
    ("hatch", "Open the hatch to the roof.", "люк", "Откройте люк на крышу."),
    ("eighth", "She finished in eighth place.", "восьмой", "Она закончила на восьмом месте."),
    ("Turkish", "I love Turkish coffee.", "турецкий", "Я люблю турецкий кофе."),
    ("take away", "They want to take away the book.", "отобрать", "Они хотят отобрать книгу."),
    ("festive", "The room looked festive and bright.", "праздничный", "Комната выглядела праздничной и яркой."),
    ("lips", "Her lips whispered a secret.", "уста", "Её уста прошептали секрет."),
    ("qualification", "His qualification is high.", "квалификация", "Его квалификация высокая."),
    ("insignificant", "The change was insignificant.", "незначительный", "Изменение было незначительным."),
    ("cheese", "I love eating cheese with bread.", "сыр", "Я люблю есть сыр с хлебом."),
    ("illegal", "Selling drugs is illegal.", "незаконный", "Продажа наркотиков незаконна."),
    ("ha", '"Ha, I know it!"', "ха", '"Ха, я знаю это!"'),
    ("snowy", "The snowy landscape was beautiful.", "снежный", "Снежный пейзаж был красивым."),
    ("presidential", "He announced his presidential campaign today.", "президентский", "Он объявил о президентской кампании сегодня."),
    ("boring", "This lecture is so boring.", "скучный", "Эта лекция такая скучная."),
    ("exceptional", "She has exceptional talent in painting.", "исключительный", "У неё исключительный талант в живописи."),
    ("deception", "Deception killed their trust.", "обман", "Обман убил их доверие."),
    ("spectacle", "It was a beautiful spectacle.", "зрелище", "Это было красивое зрелище."),
    ("nationality", "Her nationality is Russian.", "национальность", "Её национальность - русская."),
    ("merchant", "The merchant sold bread.", "купец", "Купец продал хлеб."),
    ("wire", "The lamp has a wire.", "провод", "У лампы есть провод."),
    ("mushroom", "I found a mushroom in the forest.", "гриб", "Я нашёл гриб в лесу."),
    ("unnecessary", "This meeting is unnecessary.", "ненужный", "Эта встреча ненужная."),
    ("bathhouse", "We rest at the local bathhouse.", "баня", "Мы отдыхаем в местной бане."),
    ("openly", "He openly expressed his opinion.", "открыто", "Он открыто выразил своё мнение."),
    ("to pass", "Winter will pass slowly.", "миновать", "Зима медленно минует."),
    ("advanced", "They have an advanced system.", "передовой", "У них передовая система."),
    ("dull", "The knife is dull.", "тупой", "Нож тупой."),
    ("flat", "The earth is not flat.", "плоский", "Земля не плоская."),
    ("ceremony", "The wedding ceremony was beautiful.", "церемония", "Церемония свадьбы была красивой."),
    ("to transfer", "They transfer the box.", "переносить", "Они переносят ящик."),
    ("Bolshevik", "The Bolshevik was a worker.", "большевик", "Большевик был рабочим."),
    ("excitation", "There was excitation after the news.", "возбуждение", "После новости было возбуждение."),
    ("painting", "She loves landscape painting.", "живопись", "Она любит пейзажную живопись."),
    ("advisor", "He has a financial advisor.", "советник", "У него есть финансовый советник."),
    ("upcoming", "The upcoming meeting is today.", "предстоящий", "Предстоящая встреча сегодня."),
    ("rival", "He finally defeated his rival.", "соперник", "Он наконец победил своего соперника."),
    ("entrust", "I will entrust you with this task.", "поручить", "Я поручу вам эту задачу."),
    ("goblet", "He raised the goblet of wine.", "бокал", "Он поднял бокал вина."),
    ("skirt", "She bought a new red skirt.", "юбка", "Она купила новую красную юбку."),
    ("export", "Bread export is important this year.", "экспорт", "Экспорт хлеба важен в этом году."),
    ("constitutional", "A constitutional amendment was needed.", "конституционный", "Нужна была конституционная поправка."),
    ("flash", "A bright flash was in the sky.", "вспышка", "Яркая вспышка была в небе."),
    ("stability", "We need more stability now.", "стабильность", "Нам сейчас нужна большая стабильность."),
    ("passerby", "A passerby helps the boy.", "прохожий", "Прохожий помогает мальчику."),
    ("scout", "The scout reported the enemy.", "разведчик", "Разведчик сообщил о враге."),
    ("beggar", "The beggar wants bread.", "нищий", "Нищий хочет хлеб."),
    ("to detect", "They detect an error.", "обнаруживать", "Они обнаруживают ошибку."),
    ("alternative", "Consider an alternative solution.", "альтернативный", "Рассмотрите альтернативное решение."),
    ("functional", "The system is functional now.", "функциональный", "Система сейчас функциональна."),
    ("inspector", "The inspector examined the documents carefully.", "инспектор", "Инспектор тщательно рассмотрел документы."),
    ("pour", "Please pour me some water.", "налить", "Пожалуйста, налейте мне немного воды."),
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
