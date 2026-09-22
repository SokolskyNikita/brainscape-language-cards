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

SRC = PACK / "_chunks" / "deck_15260269_00.csv"
OUT = PACK / "_chunks" / "fixed" / "deck_15260269_00.csv"
LOG = PACK / "_chunks" / "logs" / "deck_15260269_00.txt"

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
    "ago", "ones", "two", "down", "one",
}

FUNCTION_RU = {
    "я", "мне", "меня", "мной", "мой", "моя", "мое", "моё", "мои", "мою",
    "мы", "нам", "нас", "нами", "наш", "наша", "наше", "наши", "нашу",
    "ты", "тебе", "тебя", "тобой", "твой", "твоя", "твое", "твоё", "твои",
    "вы", "вам", "вас", "вами", "ваш", "ваша", "ваше", "ваши", "вашу",
    "он", "она", "оно", "они", "его", "ее", "её", "ей", "ему", "им", "их",
    "ими", "ним", "ней", "ними", "него", "нее", "неё",
    "себя", "себе", "собой", "свой", "своя", "свое", "своё", "свои", "свою",
    "своим", "своего", "своей",
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
    "во", "всё", "все", "всех", "всю", "весь", "двоих", "слишком", "сам", "самом",
    "нужен", "нужна", "нужны",
}

allow_en = {
    line.strip().lower()
    for line in (PACK / "_vocab" / "allow_en_15260269.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_ru = {
    line.strip().replace("ё", "е").lower()
    for line in (PACK / "_vocab" / "allow_ru_15260269.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_en |= FUNCTION_EN
allow_ru |= FUNCTION_RU

# Tokens from multi-word allow lemmas (have fun, become obsolete, …).
for lemma in list(allow_en):
    for part in re.split(r"[\s-]+", lemma):
        if part:
            allow_en.add(part)

# New / corrected current-card lemmas and missed inflections.
allow_en |= {
    "became", "fell", "swims", "points", "looks", "looked", "ate", "came",
    "paid", "lived", "got", "bought", "lost", "sits", "stands", "stopped",
    "works",
}
allow_ru |= {
    "методичный", "методичная", "сотрите", "упал", "упала", "устарела",
    "плавает", "указывает", "опубликовала", "мерцают", "звезды", "чувствую",
    "объявила", "ресницу", "нашел", "нашёл", "чердаке", "бодрой",
    "неинтересная", "неважная", "озаботит", "написал", "пушистая",
    "выясняется", "отличаемся", "выберите", "дремлю", "впадет", "впадёт",
    "сидел", "воплотить", "видели", "надлежит", "работает", "вывеску",
    "платили", "жил", "возьми", "получил", "пуста", "пришел", "пришёл",
    "дополняют", "купил", "высокая", "остановился", "станции", "потерял",
    "сидит", "стоит", "году", "листву", "осеннюю", "одну", "тонкая",
    "песчаная", "импортное", "аварийный", "мраморный", "отцовский",
    "постсоветская", "лекарственное", "показательный", "смешанные",
    "санитарные", "конный", "огромное", "вкусный", "новый", "хорошего",
    "интернета", "кресле", "саду", "поле", "стене", "доме", "слова",
    "новости", "идею", "руку", "кошки", "журнала", "искусства",
    "ной", "давайте", "веселиться", "повеселимся",
    "реке", "хочет", "вижу", "ел", "люблю", "учу", "знаю", "яхте", "воды",
}

# (en_lemma, en_ex, ru_lemma, ru_ex)
FIXED = [
    ("bureaucracy", "Bureaucracy often slows progress.", "бюрократия", "Бюрократия часто мешает прогрессу."),
    ("uninteresting", "This book is uninteresting.", "неинтересный", "Эта книга неинтересная."),
    ("estate", "He has a huge estate.", "имение", "У него огромное имение."),
    ("equestrian", "She likes equestrian sport.", "конный", "Она любит конный спорт."),
    ("oops", "Oops, the cup fell.", "ой", "Ой, чашка упала."),
    ("become obsolete", "This machine has become obsolete.", "устареть", "Эта машина устарела."),
    ("duck", "The duck swims in the river.", "утка", "Утка плавает в реке."),
    ("sanitary", "We need sanitary conditions.", "санитарный", "Нам нужны санитарные условия."),
    ("vector", "The vector points north.", "вектор", "Вектор указывает на север."),
    ("memoirs", "She published her memoirs yesterday.", "мемуары", "Она опубликовала свои мемуары вчера."),
    ("twinkle", "Stars twinkle in the night sky.", "мерцать", "Звёзды мерцают в ночном небе."),
    ("sharpness", "I feel the sharpness of the knife.", "острота", "Я чувствую остроту ножа."),
    ("erase", "Please erase this error.", "стереть", "Пожалуйста, сотрите эту ошибку."),
    ("to justify", "He wants to justify this.", "оправдать", "Он хочет оправдать это."),
    ("candidacy", "She announced her candidacy yesterday.", "кандидатура", "Она объявила о своей кандидатуре вчера."),
    ("eyelash", "I see one eyelash.", "ресница", "Я вижу одну ресницу."),
    ("attic", "I found old books in the attic.", "чердак", "Я нашёл старые книги на чердаке."),
    ("brightness", "The brightness of the sun is strong.", "яркость", "Яркость солнца сильная."),
    ("Finn", "He is a Finn.", "финн", "Он финн."),
    ("cheerful", "She looks cheerful today.", "бодрый", "Она выглядит бодрой сегодня."),
    ("syllable", "This word has one syllable.", "слог", "В этом слове один слог."),
    ("minor", "He is still a minor.", "несовершеннолетний", "Он всё ещё несовершеннолетний."),
    ("cake", "This cake is tasty.", "торт", "Этот торт вкусный."),
    ("tape recorder", "I found my old tape recorder.", "магнитофон", "Я нашёл свой старый магнитофон."),
    ("methodical", "She is very methodical.", "методичный", "Она очень методичная."),
    ("unimportant", "This detail is unimportant.", "неважный", "Эта деталь неважная."),
    ("optimization", "We need this optimization.", "оптимизация", "Нам нужна эта оптимизация."),
    ("mixed", "The salad had mixed vegetables.", "смешанный", "В салате были смешанные овощи."),
    ("to concern", "This news will concern him.", "озаботить", "Эта новость его озаботит."),
    ("ex", "My ex wrote to me.", "экс", "Мой экс написал мне."),
    ("to insult", "He did not want to insult you.", "оскорблять", "Он не хотел оскорблять тебя."),
    ("fluffy", "The cat is so fluffy.", "пушистый", "Кошка такая пушистая."),
    ("greedily", "He greedily ate the cake.", "жадно", "Он жадно ел торт."),
    ("foliage", "I love autumn foliage.", "листва", "Я люблю осеннюю листву."),
    ("to be clarified", "The truth is being clarified.", "выясняться", "Правда выясняется."),
    ("provocation", "This is a provocation.", "провокация", "Это провокация."),
    ("culturally", "Culturally we differ.", "культурно", "Культурно мы отличаемся."),
    ("landmark", "The tower is a city landmark.", "ориентир", "Башня — ориентир города."),
    ("have fun", "Let's have fun today.", "веселиться", "Давайте веселиться сегодня."),
    ("from outside", "The danger came from outside.", "извне", "Опасность пришла извне."),
    ("Komsomol member", "The Komsomol member is at the meeting.", "комсомолец", "Комсомолец на встрече."),
    ("nationalism", "Nationalism is a strong idea.", "национализм", "Национализм — сильная идея."),
    ("signing", "The signing of the paper is today.", "подписание", "Подписание бумаги сегодня."),
    ("disclosure", "This disclosure is important.", "раскрытие", "Это раскрытие важное."),
    ("epidemic", "The epidemic is dangerous.", "эпидемия", "Эпидемия опасна."),
    ("provider", "Choose a good internet provider.", "провайдер", "Выберите хорошего провайдера интернета."),
    ("doze", "I often doze in the chair.", "дремать", "Я часто дремлю в кресле."),
    ("fall into", "He will fall into anger.", "впасть", "Он впадёт в гнев."),
    ("to take shelter", "We had to take shelter from the rain.", "укрыться", "Мы должны были укрыться от дождя."),
    ("waist", "She has a thin waist.", "талия", "У неё тонкая талия."),
    ("demonstrative", "This is a demonstrative example.", "показательный", "Это показательный пример."),
    ("electronics", "I study electronics at university.", "электроника", "Я учу электронику в университете."),
    ("medicinal", "This is a medicinal plant.", "лекарственный", "Это лекарственное растение."),
    ("homeless person", "The homeless person sat on the street.", "бомж", "Бомж сидел на улице."),
    ("abnormal", "His behavior was clearly abnormal.", "ненормальный", "Его поведение было явно ненормальным."),
    ("embody", "He wants to embody this idea.", "воплотить", "Он хочет воплотить эту идею."),
    ("Austrian", "This is an Austrian city.", "австрийский", "Это австрийский город."),
    ("ridge", "We saw the mountain ridge.", "хребет", "Мы видели горный хребет."),
    ("Marxism", "He studies Marxism.", "марксизм", "Он учит марксизм."),
    ("to be due", "It is due to us to wait.", "надлежать", "Нам надлежит ждать."),
    ("emergency", "This is an emergency exit.", "аварийный", "Это аварийный выход."),
    ("marble", "This is a marble table.", "мраморный", "Это мраморный стол."),
    ("cent", "I found a cent on the earth.", "цент", "Я нашёл цент на земле."),
    ("patriotism", "I know his patriotism.", "патриотизм", "Я знаю его патриотизм."),
    ("ideally", "This works ideally.", "идеально", "Это работает идеально."),
    ("keeper", "He is the keeper of this house.", "хранитель", "Он хранитель этого дома."),
    ("signboard", "I see the signboard.", "вывеска", "Я вижу вывеску."),
    ("tribute", "They paid tribute to the king.", "дань", "Они платили дань королю."),
    ("imported", "This is imported wine.", "импортный", "Это импортное вино."),
    ("whine", "He likes to whine.", "ныть", "Он любит ныть."),
    ("nobleman", "The nobleman lived in this house.", "дворянин", "Дворянин жил в этом доме."),
    ("in addition", "In addition, take this book.", "вдобавок", "Вдобавок возьми эту книгу."),
    ("thirteen", "She is thirteen.", "тринадцать", "Ей тринадцать."),
    ("yacht", "We were on a yacht today.", "яхта", "Мы были на яхте сегодня."),
    ("nomination", "He got a nomination.", "номинация", "Он получил номинацию."),
    ("sandy", "The road is sandy.", "песчаный", "Дорога песчаная."),
    ("lens", "I need a new lens.", "объектив", "Мне нужен новый объектив."),
    ("to run in", "He likes to run in to us.", "забегать", "Он любит забегать к нам."),
    ("treasury", "The treasury is empty.", "казна", "Казна пуста."),
    ("pollution", "Pollution of water is a problem.", "загрязнение", "Загрязнение воды — проблема."),
    ("gnome", "The gnome sat in the garden.", "гном", "Гном сидел в саду."),
    ("alpha", "He is the alpha here.", "альфа", "Он здесь альфа."),
    ("lazily", "He lazily sat in the chair.", "лениво", "Он лениво сидел в кресле."),
    ("long-awaited", "The long-awaited vacation finally came.", "долгожданный", "Долгожданный отпуск наконец пришёл."),
    ("to comment on", "He did not want to comment on this.", "прокомментировать", "Он не хотел прокомментировать это."),
    ("to complement", "These words complement each other.", "дополнять", "Эти слова дополняют друг друга."),
    ("paternal", "This is his paternal house.", "отцовский", "Это его отцовский дом."),
    ("to clutch", "He wants to clutch her hand.", "схватиться", "Он хочет схватиться за её руку."),
    ("Maya", "This is a Maya city.", "майя", "Это город майя."),
    ("feed", "I bought feed for the cat.", "корм", "Я купил корм для кошки."),
    ("reliability", "The reliability of this news is high.", "достоверность", "Достоверность этой новости высокая."),
    ("trolleybus", "The trolleybus stopped at the station.", "троллейбус", "Троллейбус остановился на станции."),
    ("specialization", "His specialization is history.", "специализация", "Его специализация — история."),
    ("post-Soviet", "This is a post-Soviet country.", "постсоветский", "Это постсоветская страна."),
    ("flashlight", "I lost my flashlight.", "фонарик", "Я потерял свой фонарик."),
    ("spider", "A spider sits on the wall.", "паук", "Паук сидит на стене."),
    ("subscription", "I have a subscription to a magazine.", "подписка", "У меня есть подписка на журнал."),
    ("ram", "The ram stands in the field.", "баран", "Баран стоит в поле."),
    ("census", "The census is this year.", "перепись", "Перепись в этом году."),
    ("blossoming", "This is the blossoming of art.", "расцвет", "Это расцвет искусства."),
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
    "told": "tell", "got": "get", "found": "find", "left": "leave",
    "kept": "keep", "felt": "feel", "thought": "think", "brought": "bring",
    "stood": "stand", "sat": "sit", "ran": "run", "won": "win",
    "lost": "lose", "met": "meet", "led": "lead", "paid": "pay",
    "spoke": "speak", "written": "write", "wrote": "write",
    "ate": "eat", "eaten": "eat", "drank": "drink", "drunk": "drink",
    "chose": "choose", "chosen": "choose", "built": "build",
    "sang": "sing", "sung": "sing", "wore": "wear", "worn": "wear",
    "fell": "fall", "dug": "dig", "fought": "fight", "shown": "show",
    "began": "begin", "begun": "begin", "became": "become",
    "swims": "swim", "points": "point", "looks": "look", "looked": "look",
    "works": "work", "sits": "sit", "stands": "stand", "stopped": "stop",
    "lived": "live", "announced": "announce", "published": "publish",
    "studies": "study",
}


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
