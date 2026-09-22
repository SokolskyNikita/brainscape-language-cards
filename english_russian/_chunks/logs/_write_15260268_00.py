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

SRC = PACK / "_chunks" / "deck_15260268_00.csv"
OUT = PACK / "_chunks" / "fixed" / "deck_15260268_00.csv"
LOG = PACK / "_chunks" / "logs" / "deck_15260268_00.txt"

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
    "ago", "ones", "two", "down",
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
}

allow_en = {
    line.strip().lower()
    for line in (PACK / "_vocab" / "allow_en_15260268.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_ru = {
    line.strip().replace("ё", "е").lower()
    for line in (PACK / "_vocab" / "allow_ru_15260268.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_en |= FUNCTION_EN
allow_ru |= FUNCTION_RU

# Inflections of allowed lemmas that the stemmer misses.
allow_en |= {"began", "chose", "built", "wore", "dug", "sang", "became", "fell", "sold", "shown"}
allow_ru |= {
    "пели", "хочу", "горы", "ждала", "ума", "упал", "люблю", "любит",
    "руки", "может", "смог", "смогла", "умеет", "съесть", "является",
    "шли", "нужен", "мойте", "кожи", "новая", "еду", "выросла", "идеи",
    "знает", "хотим",
}

# (en_lemma, en_ex, ru_lemma, ru_ex)
FIXED = [
    ("anthem", "They sang the national anthem proudly.", "гимн", "Они гордо пели гимн."),
    ("patriot", "He is a true patriot.", "патриот", "Он настоящий патриот."),
    ("sixteen", "She turned sixteen today.", "шестнадцать", "Ей исполнилось шестнадцать сегодня."),
    ("addiction", "His addiction to coffee is strong.", "пристрастие", "Его пристрастие к кофе сильное."),
    ("giant", "The giant towered over the trees.", "гигант", "Гигант возвышался над деревьями."),
    ("boulevard", "We walked along the boulevard.", "бульвар", "Мы шли по бульвару."),
    ("intentionally", "He intentionally ignored my message.", "нарочно", "Он нарочно проигнорировал мое сообщение."),
    ("oak", "The oak stood in the garden.", "дуб", "Дуб стоял в саду."),
    ("verbal", "He prefers verbal instructions.", "словесный", "Он предпочитает словесные инструкции."),
    ("synthesis", "This is a simple synthesis.", "синтез", "Это простой синтез."),
    ("cleaning", "We started the cleaning today.", "уборка", "Мы начали уборку сегодня."),
    ("destined", "They were destined to meet again.", "суждено", "Им было суждено встретиться снова."),
    ("sew", "She likes to sew dresses.", "шить", "Она любит шить платья."),
    ("swallow", "I cannot swallow this.", "проглотить", "Я не могу проглотить это."),
    ("intercept", "The player intercepts the letter.", "перехватить", "Игрок перехватывает письмо."),
    ("small town", "She misses her small town.", "местечко", "Ей не хватает её местечка."),
    ("composite", "The bridge uses composite materials.", "составной", "Мост использует составные материалы."),
    ("chess", "I love playing chess.", "шахматы", "Я люблю играть в шахматы."),
    ("to suffocate", "He began to suffocate in the smoke.", "задыхаться", "Он начал задыхаться от дыма."),
    ("crystal", "The crystal sparkled in the sun.", "кристалл", "Кристалл искрился на солнце."),
    ("bloom", "The flowers begin to bloom in spring.", "цвести", "Цветы начинают цвести весной."),
    ("to keep silent", "He chose to keep silent.", "промолчать", "Он решил промолчать."),
    ("to introduce", "I want to introduce you two.", "познакомить", "Я хочу познакомить вас двоих."),
    ("fork", "I need a fork to eat this.", "вилка", "Мне нужна вилка, чтобы это есть."),
    ("hallway", "Leave your shoes in the hallway.", "прихожая", "Оставьте свою обувь в прихожей."),
    ("solidly", "The wall was solidly built.", "прочно", "Стена была прочно построена."),
    ("get to", "I will get to work by bus.", "добираться", "Я буду добираться на работу на автобусе."),
    ("mommy", "Mommy is home today.", "мамочка", "Мамочка сегодня дома."),
    ("riding", "She likes riding a bicycle.", "езда", "Ей нравится езда на велосипеде."),
    ("to brake", "I must brake now.", "тормозить", "Мне нужно тормозить сейчас."),
    ("to hunt", "He loves to hunt in autumn.", "охотиться", "Он любит охотиться осенью."),
    ("demolish", "They plan to demolish the old building.", "снести", "Они планируют снести старое здание."),
    ("surplus", "We have a surplus of apples.", "избыток", "У нас избыток яблок."),
    ("subordination", "Subordination ensures organizational efficiency.", "подчинение", "Подчинение обеспечивает организационную эффективность."),
    ("import", "We need this import.", "импорт", "Нам нужен этот импорт."),
    ("madly", "She madly loved him.", "безумно", "Она безумно любила его."),
    ("mechanic", "The mechanic works here.", "механик", "Механик работает здесь."),
    ("disputable", "This claim is disputable.", "спорный", "Это утверждение спорное."),
    ("climb in", "He helped the cat climb in.", "влезть", "Он помог кошке влезть."),
    ("to liberate", "They want to liberate the city.", "освобождать", "Они хотят освободить город."),
    ("dynamic", "The system is highly dynamic.", "динамический", "Система очень динамическая."),
    ("contour", "The map showed the mountain's contour.", "контур", "Карта показывала контур горы."),
    ("sink", "Wash your hands in the sink.", "раковина", "Мойте руки в раковине."),
    ("restraint", "She showed remarkable restraint.", "выдержка", "Она показала замечательную выдержку."),
    ("mature", "The cheese is perfectly mature.", "зрелый", "Сыр идеально зрелый."),
    ("neat", "Your handwriting is very neat.", "аккуратный", "Твой почерк очень аккуратный."),
    ("tactical", "He made a tactical plan.", "тактический", "Он сделал тактический план."),
    ("figurine", "She collects small figurines.", "фигурка", "Она собирает маленькие фигурки."),
    ("labyrinth", "He was lost in the labyrinth.", "лабиринт", "Он заблудился в лабиринте."),
    ("scatter", "He scattered the books on the table.", "разбросать", "Он разбросал книги по столу."),
    ("craft", "She knows this craft.", "ремесло", "Она знает это ремесло."),
    ("to affect", "This news will affect her.", "затрагивать", "Эта новость затронет её."),
    ("weaken", "This will weaken him.", "ослабить", "Это ослабит его."),
    ("patiently", "She waited patiently for her turn.", "терпеливо", "Она терпеливо ждала своей очереди."),
    ("win", "She celebrated her big win.", "выигрыш", "Она отметила свой большой выигрыш."),
    ("joint-stock", "This is a joint-stock company.", "акционерный", "Это акционерная компания."),
    ("to blow up", "They planned to blow up the bridge.", "взорвать", "Они планировали взорвать мост."),
    ("slavery", "Slavery ended long ago.", "рабство", "Рабство закончилось давно."),
    ("to wipe", "I need to wipe the table.", "вытереть", "Мне нужно вытереть стол."),
    ("sensitivity", "Skin sensitivity can be high.", "чувствительность", "Чувствительность кожи может быть высокой."),
    ("trench", "Soldiers made a trench for protection.", "окоп", "Солдаты сделали окоп для защиты."),
    ("configuration", "Check the computer's configuration.", "конфигурация", "Проверьте конфигурацию компьютера."),
    ("supervision", "Under his supervision, quality improved significantly.", "надзор", "Под его надзором качество значительно улучшилось."),
    ("chronicle", "I read an ancient chronicle yesterday.", "хроника", "Вчера я прочитал древнюю хронику."),
    ("sculpture", "There is a new sculpture in the park.", "скульптура", "В парке есть новая скульптура."),
    ("to dispose", "He plans to dispose of his assets.", "распорядиться", "Он планирует распорядиться своими активами."),
    ("Biblical", "He studied biblical history at university.", "библейский", "Он изучал библейскую историю в университете."),
    ("indirect", "His answer was indirect.", "косвенный", "Его ответ был косвенным."),
    ("to postpone", "We do not want to postpone the meeting.", "откладывать", "Мы не хотим откладывать встречу."),
    ("organic", "I prefer organic food.", "органический", "Я предпочитаю органическую еду."),
    ("break through", "She managed to break through the wall.", "прорваться", "Она смогла прорваться через стену."),
    ("to be read", "This book is read often.", "читаться", "Эта книга часто читается."),
    ("transitional", "We are in a transitional period now.", "переходный", "Мы сейчас в переходном периоде."),
    ("to dump", "He decided to dump the trash.", "свалить", "Он решил свалить мусор."),
    ("chocolate", "I love this chocolate.", "шоколад", "Я люблю этот шоколад."),
    ("armor", "Knights wore armor for protection.", "броня", "Рыцари носили броню для защиты."),
    ("preface", "She wrote the preface for his book.", "предисловие", "Она написала предисловие к его книге."),
    ("arbitrariness", "This is not law, this is arbitrariness.", "произвол", "Это не закон, это произвол."),
    ("curse", "The ancient curse followed the family.", "проклятие", "Древнее проклятие преследовало семью."),
    ("inspiration", "Music was his greatest inspiration.", "вдохновение", "Музыка была его величайшим вдохновением."),
    ("lazy", "He is very lazy.", "ленивый", "Он очень ленивый."),
    ("wizard", "The wizard said a powerful spell.", "волшебник", "Волшебник произнёс мощное заклинание."),
    ("optimism", "I like her optimism.", "оптимизм", "Мне нравится её оптимизм."),
    ("erroneous", "His conclusions were entirely erroneous.", "ошибочный", "Его выводы были полностью ошибочными."),
    ("periodic", "This is a periodic report.", "периодический", "Это периодический доклад."),
    ("attachment", "Her attachment to the cat grew.", "привязанность", "Её привязанность к кошке выросла."),
    ("verst", "We traveled ten versts today.", "верста", "Мы проехали сегодня десять верст."),
    ("African", "She loves African art collections.", "африканский", "Она любит коллекции африканского искусства."),
    ("premiere", "The movie's premiere was sold out.", "премьера", "Билеты на премьеру фильма были распроданы."),
    ("humiliation", "He felt deep humiliation.", "унижение", "Он испытал глубокое унижение."),
    ("meditation", "Meditation improves mental clarity.", "медитация", "Медитация улучшает ясность ума."),
    ("banker", "The banker approved the credit.", "банкир", "Банкир одобрил кредит."),
    ("incomplete", "The report is still incomplete.", "неполный", "Доклад всё ещё неполный."),
    ("tractor", "The farmer has a tractor.", "трактор", "У фермера есть трактор."),
    ("intelligent", "He is an intelligent man.", "интеллектуальный", "Он интеллектуальный человек."),
    ("follower", "He became a follower of this idea.", "последователь", "Он стал последователем этой идеи."),
    ("eighteen", "She turned eighteen today.", "восемнадцать", "Ей исполнилось восемнадцать сегодня."),
    ("tighten", "Please tighten the screws.", "затянуть", "Пожалуйста, затяните винты."),
    ("curtain", "The curtain fell after the performance.", "занавес", "Занавес упал после представления."),
    ("emigration", "Emigration changed this country.", "эмиграция", "Эмиграция изменила эту страну."),
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
    "sews": "sew", "turned": "turn",
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
