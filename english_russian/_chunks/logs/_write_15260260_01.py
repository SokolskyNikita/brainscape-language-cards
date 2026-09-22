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

SRC = PACK / "_chunks" / "deck_15260260_01.csv"
OUT = PACK / "_chunks" / "fixed" / "deck_15260260_01.csv"
LOG = PACK / "_chunks" / "logs" / "deck_15260260_01.txt"

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
        "а", "но", "или",
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
    ("interpretation", "Art allows for personal interpretation.", "интерпретация", "Искусство позволяет личную интерпретацию."),
    ("turn away", "She will turn away from him.", "отвернуться", "Она отвернётся от него."),
    ("pig", "The pig was in the mud.", "свинья", "Свинья была в грязи."),
    ("rational", "Choose a rational solution.", "рациональный", "Выберите рациональное решение."),
    ("to be caught", "He tried not to be caught.", "попадаться", "Он пытался не попадаться."),
    ("present", "Please present your ticket.", "предъявить", "Пожалуйста, предъявите ваш билет."),
    ("rather", "I would rather stay home today.", "скорее", "Я бы скорее остался дома сегодня."),
    ("Latin", "I study Latin at university.", "латинский", "Я учу латинский в университете."),
    ("willingly", "She willingly shared her lunch.", "охотно", "Она охотно поделилась своим обедом."),
    ("to educate", "Parents educate their son.", "воспитывать", "Родители воспитывают своего сына."),
    ("bath", "I need a bath this evening.", "ванна", "Мне нужна ванна сегодня вечером."),
    ("horseradish", "I added horseradish to the soup.", "хрен", "Я добавил хрен в суп."),
    ("to tear off", "She will tear off a piece of paper.", "оторвать", "Она оторвала кусок бумаги."),
    ("climate", "The climate of this country is cold.", "климат", "Климат этой страны холодный."),
    ("onion", "I cut an onion for soup.", "лук", "Я режу лук для супа."),
    ("target", "This is the target group.", "целевой", "Это целевая группа."),
    ("to be accompanied", "The movie is accompanied by music.", "сопровождаться", "Фильм сопровождается музыкой."),
    ("old age", "Old age brings wisdom.", "старость", "Старость приносит мудрость."),
    ("diversity", "Diversity is important for our community.", "разнообразие", "Разнообразие важно для нашего сообщества."),
    ("primary", "Primary sources are important.", "первичный", "Первичные источники важны."),
    ("administrator", "The administrator opened the conference room.", "администратор", "Администратор открыл комнату для конференции."),
    ("accompaniment", "Music was the accompaniment to her voice.", "сопровождение", "Музыка была сопровождением её голоса."),
    ("leather", "She bought a leather jacket.", "кожаный", "Она купила кожаную куртку."),
    ("snake", "The snake went through the grass.", "змея", "Змея прошла через траву."),
    ("sadly", "She looked at him sadly.", "грустно", "Она грустно посмотрела на него."),
    ("biography", "I read his biography yesterday.", "биография", "Я прочитал его биографию вчера."),
    ("expertise", "His expertise is important.", "опыт", "Его опыт важен."),
    ("proud", "She was proud of her son.", "гордый", "Она была горда своим сыном."),
    ("backpack", "I took my backpack for the trip.", "рюкзак", "Я взял свой рюкзак в поездку."),
    ("mug", "I filled my mug with coffee.", "кружка", "Я наполнил свою кружку кофе."),
    ("laptop", "I bought a new laptop yesterday.", "ноутбук", "Я купил новый ноутбук вчера."),
    ("admirer", "She has a secret admirer.", "поклонник", "У неё есть тайный поклонник."),
    ("injury", "He received an injury playing football.", "травма", "Он получил травму, играя в футбол."),
    ("twist", "She will twist the key.", "крутить", "Она будет крутить ключ."),
    ("rapidly", "He ran rapidly to the house.", "стремительно", "Он стремительно бежал к дому."),
    ("pluck", "She plucked an apple from the tree.", "сорвать", "Она сорвала яблоко с дерева."),
    ("admiral", "The admiral commands the fleet.", "адмирал", "Адмирал командует флотом."),
    ("resemble", "You resemble your mother.", "походить", "Ты походишь на свою мать."),
    ("to obligate", "The law will obligate him to pay.", "обязать", "Этот закон обязывает его платить."),
    ("thigh", "He has pain in his thigh.", "бедро", "У него боль в бедре."),
    ("descendant", "He is a descendant of the king.", "потомок", "Он потомок короля."),
    ("subtract", "Subtract five from ten.", "отнять", "Нужно отнять пять от десяти."),
    ("illuminate", "The sun will illuminate the room.", "осветить", "Солнце осветит комнату."),
    ("elephant", "The elephant drank water.", "слон", "Слон пил воду."),
    ("printed", "I read the printed book yesterday.", "печатный", "Я читал печатную книгу вчера."),
    ("continuous", "The rain was continuous all day.", "непрерывный", "Дождь был непрерывным весь день."),
    ("panel", "The wall was covered with a panel.", "панель", "Стена была покрыта панелью."),
    ("cartridge", "He loaded a cartridge into the rifle.", "патрон", "Он вставил патрон в винтовку."),
    ("intelligentsia", "The intelligentsia discussed the book.", "интеллигенция", "Интеллигенция обсуждала книгу."),
    ("password", "I forgot my password.", "пароль", "Я забыл свой пароль."),
    ("fatherland", "He loves his fatherland.", "отечество", "Он любит своё отечество."),
    ("mailing", "I sent a mailing yesterday.", "рассылка", "Я отправил рассылку вчера."),
    ("full-fledged", "He became a full-fledged member yesterday.", "полноценный", "Он стал полноценным членом вчера."),
    ("sorrow", "Her eyes were filled with sorrow.", "печаль", "Её глаза были наполнены печалью."),
    ("lighting", "The room's lighting was perfect.", "освещение", "Освещение в комнате было идеальным."),
    ("landscape", "The landscape looked beautiful.", "пейзаж", "Пейзаж выглядел красиво."),
    ("perfection", "Striving for perfection is important.", "совершенство", "Стремление к совершенству важно."),
    ("action movie", "I love watching a good action movie.", "боевик", "Я люблю смотреть хороший боевик."),
    ("aggregate", "The aggregate of information was important.", "совокупность", "Совокупность информации была важна."),
    ("majesty", "Her majesty greeted the guests.", "величество", "Её величество приветствовала гостей."),
    ("porridge", "I like porridge for breakfast.", "каша", "Мне нравится каша на завтрак."),
    ("thirst", "His thirst for knowledge is strong.", "жажда", "Его жажда знаний сильна."),
    ("cosmonaut", "The cosmonaut saw a star.", "космонавт", "Космонавт видел звезду."),
    ("infantry", "The infantry will go to the city.", "пехота", "Пехота пойдёт в город."),
    ("Fascist", "He was a Fascist.", "фашист", "Он был фашистом."),
    ("diagnosis", "The doctor shared the diagnosis today.", "диагноз", "Врач сообщил диагноз сегодня."),
    ("to be shy", "She learned not to be shy.", "стесняться", "Она научилась не стесняться."),
    ("land", "They bought land near the river.", "земля", "Они купили землю у реки."),
    ("leak out", "Oil began to leak out slowly.", "вытекать", "Масло начало медленно вытекать."),
    ("boil down to", "The question boils down to patience.", "сводиться", "Вопрос сводится к терпению."),
    ("illustration", "I like the illustration in this book.", "иллюстрация", "Мне нравится иллюстрация в этой книге."),
    ("bring together", "He brings friends together.", "сводить", "Он сводит друзей."),
    ("mentally", "She mentally prepared her speech.", "мысленно", "Она мысленно подготовила свою речь."),
    ("renaissance", "Art experienced a renaissance.", "возрождение", "Искусство пережило возрождение."),
    ("frequent", "Rain is frequent in the city.", "частый", "В городе часты дожди."),
    ("conquer", "They wanted to conquer new territory.", "завоевать", "Они хотели завоевать новую территорию."),
    ("annually", "We meet annually in the spring.", "ежегодно", "Мы встречаемся ежегодно весной."),
    ("Siberian", "The Siberian winter is cold.", "сибирский", "Сибирская зима холодная."),
    ("gust", "I felt a gust of wind.", "порыв", "Я чувствовал порыв ветра."),
    ("update", "We need an update for this software.", "обновление", "Нам нужно обновление для этой программы."),
    ("nightmare", "She had a nightmare at night.", "кошмар", "У неё был кошмар ночью."),
    ("cellular", "I need a new cellular telephone.", "сотовый", "Мне нужен новый сотовый телефон."),
    ("integration", "Integration of the system is important.", "интеграция", "Интеграция системы важна."),
    ("primarily", "He primarily drinks tea, not coffee.", "преимущественно", "Он преимущественно пьёт чай, а не кофе."),
    ("humanitarian", "She received humanitarian help.", "гуманитарный", "Она получила гуманитарную помощь."),
    ("cunning", "The man is cunning.", "хитрый", "Этот человек хитрый."),
    ("to catch", "I managed to catch him at home.", "застать", "Мне удалось застать его дома."),
    ("range", "This is a wide range of prices.", "диапазон", "Это широкий диапазон цен."),
    ("preference", "She has a strong preference for tea.", "предпочтение", "У неё есть сильное предпочтение: чай."),
    ("to pick up", "He picked up the disease.", "подхватить", "Он подхватил болезнь."),
    ("doll", "She received a beautiful doll as a gift.", "кукла", "Она получила в подарок красивую куклу."),
    ("coal", "We need more coal for the fire.", "уголь", "Нам нужен уголь для огня."),
    ("allocation", "Allocation of time is important for success.", "выделение", "Выделение времени важно для успеха."),
    ("champion", "He became a sport champion.", "чемпион", "Он стал чемпионом спорта."),
    ("periodically", "I check my mail periodically.", "периодически", "Я периодически проверяю свою почту."),
    ("nail", "She showed her red nail.", "ноготь", "Она показала свой красный ноготь."),
    ("pound", "I lost ten pounds in a month.", "фунт", "Я потерял десять фунтов за месяц."),
    ("rage", "His eyes burned with rage.", "ярость", "Его глаза горели яростью."),
    ("collective farm", "They worked at the collective farm.", "колхоз", "Они работали в колхозе."),
    ("sparkle", "Her eyes sparkle with joy.", "сверкать", "Её глаза сверкают радостью."),
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


RU_IRREG = {
    "пить": ("пь",),
    "есть": ("ед", "еш", "ем", "ел"),
    "идти": ("ид", "шл", "ше"),
    "пойти": ("пой", "пош"),
    "мочь": ("мож", "мог"),
    "учить": ("уч",),
    "взять": ("возьм", "взя"),
}

def ru_ok(text: str, extra: set[str]) -> list[str]:
    bad = []
    pool = allow_ru | extra
    for raw in re.findall(r"[А-Яа-яЁё-]+", text):
        w = raw.replace("ё", "е").replace("Ё", "е").lower()
        if w in pool:
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
        if any(
            lemma in pool and any(w.startswith(stem) for stem in stems)
            for lemma, stems in RU_IRREG.items()
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
