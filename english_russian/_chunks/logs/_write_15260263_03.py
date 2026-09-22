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

SRC = PACK / "_chunks" / "deck_15260263_03.csv"
OUT = PACK / "_chunks" / "fixed" / "deck_15260263_03.csv"
LOG = PACK / "_chunks" / "logs" / "deck_15260263_03.txt"

FUNCTION_EN = {
    "a", "the", "is", "be", "i", "you", "he", "she", "it", "we", "they",
    "my", "and", "or", "in", "on", "at", "to", "of", "for", "with", "from",
    "not", "his", "him", "her", "their", "them", "our", "us", "me", "am",
    "are", "was", "were", "been", "being", "this", "that", "these", "those",
    "an", "as", "by", "into", "about", "than", "then", "so", "if", "but",
    "its", "your", "all", "no", "yes", "do", "does", "did", "done", "doing",
    "has", "have", "had", "having", "will", "would", "can", "could", "may",
    "might", "must", "shall", "should", "just", "also", "too", "very",
    "himself", "herself", "myself", "itself", "themselves", "ourselves",
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
    for line in (PACK / "_vocab" / "allow_en_15260263.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
} | FUNCTION_EN
allow_ru = {
    line.strip().replace("ё", "е").lower()
    for line in (PACK / "_vocab" / "allow_ru_15260263.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
} | FUNCTION_RU

# (en_lemma, en_ex, ru_lemma, ru_ex)
FIXED = [
    ("cooperate", "We must cooperate to solve this.", "сотрудничать", "Мы должны сотрудничать, чтобы решить это."),
    ("to cease", "The noise will cease.", "прекратиться", "Шум прекратится."),
    ("aggression", "His aggression is strong.", "агрессия", "Его агрессия сильная."),
    ("prevention", "Prevention is important.", "профилактика", "Профилактика важна."),
    ("spin", "The Earth continues to spin daily.", "крутиться", "Земля продолжает крутиться каждый день."),
    ("glade", "Deer stood in the glade.", "поляна", "Олени стояли на поляне."),
    ("brand new", "I bought a brand new car.", "новенький", "Я купил новенькую машину."),
    ("flock", "I see a flock of birds.", "стая", "Стая птиц здесь."),
    ("cozy", "This room is cozy.", "уютный", "Эта комната уютная."),
    ("employment", "Employment is growing.", "занятость", "Занятость растёт."),
    ("halfway", "We're halfway there already.", "наполовину", "Мы уже наполовину там."),
    ("blow", "The wind will blow strongly this evening.", "дуть", "Ветер будет сильно дуть сегодня вечером."),
    ("flexible", "She is very flexible.", "гибкий", "Она очень гибкая."),
    ("to beg", "She began to beg for help.", "умолять", "Она начала умолять о помощи."),
    ("integrate", "We must integrate this into the system.", "встроить", "Мы должны встроить это в систему."),
    ("crow", "The crow sat on the tree.", "ворона", "Ворона сидела на дереве."),
    ("truly", "She was truly a remarkable woman.", "поистине", "Она была поистине замечательной женщиной."),
    ("jeans", "I bought new jeans yesterday.", "джинсы", "Вчера я купил новые джинсы."),
    ("to come to", "I saw him come to slowly.", "очнуться", "Я видел, как он медленно очнулся."),
    ("stimulus", "Music is a powerful stimulus for memory.", "стимул", "Музыка — мощный стимул для памяти."),
    ("compatriot", "She found a compatriot in the city.", "соотечественник", "Она нашла соотечественника в городе."),
    ("hostage", "They took him hostage yesterday.", "заложник", "Они взяли его в заложники вчера."),
    ("to fall off", "He did not fall off the roof.", "сорваться", "Он не сорвался с крыши."),
    ("convention", "I read the convention.", "конвенция", "Я читал конвенцию."),
    ("continuously", "He works continuously.", "непрерывно", "Он работает непрерывно."),
    ("imprint", "I see an imprint on the table.", "отпечаток", "Я вижу отпечаток на столе."),
    ("elected", "She was elected president.", "избранный", "Она была избрана президентом."),
    ("coating", "The table has a new coating.", "покрытие", "У стола новое покрытие."),
    ("too much", "This is too much.", "чересчур", "Это чересчур."),
    ("graphic", "This is a graphic design.", "графический", "Это графический дизайн."),
    ("composer", "He is a famous composer.", "композитор", "Он известный композитор."),
    ("intimate", "They shared an intimate moment together.", "интимный", "Они разделили интимный момент вместе."),
    ("excerpt", "Read this excerpt from the novel.", "отрывок", "Прочитайте этот отрывок из романа."),
    ("bitch", "She called him a bitch.", "сука", "Она сказала, что он сука."),
    ("immobile", "He was immobile for a long time.", "неподвижный", "Он был неподвижным долгое время."),
    ("shot glass", "He filled the shot glass quickly.", "рюмка", "Он быстро наполнил рюмку."),
    ("moreover", "She refused, and moreover, she left early.", "притом", "Она отказалась, и притом она ушла рано."),
    ("personnel", "This is a personnel question.", "кадровый", "Это кадровый вопрос."),
    ("dome", "The church has a high dome.", "купол", "У церкви высокий купол."),
    ("tiger", "I saw a tiger.", "тигр", "Я видел тигра."),
    ("photographer", "The photographer took a photo.", "фотограф", "Фотограф сделал фотографию."),
    ("density", "The density of water is known.", "плотность", "Плотность воды известна."),
    ("tenderly", "He tenderly held her hand.", "ласково", "Он ласково держал её за руку."),
    ("cut out", "She cut out a heart from paper.", "вырезать", "Она вырезала сердце из бумаги."),
    ("input", "Check the input.", "ввод", "Проверьте ввод."),
    ("to crave", "I crave water.", "жаждать", "Я жажду воды."),
    ("grid", "The city has a grid of streets.", "сетка", "В городе есть сетка улиц."),
    ("aesthetic", "This is an aesthetic choice.", "эстетический", "Это эстетический выбор."),
    ("oligarch", "The oligarch is very rich.", "олигарх", "Олигарх очень богатый."),
    ("courteous", "He was always courteous to guests.", "любезный", "Он всегда был любезен с гостями."),
    ("confuse", "Bright colors often confuse me.", "путать", "Яркие цвета часто путают меня."),
    ("rider", "The rider sat on the horse.", "всадник", "Всадник сидел на лошади."),
    ("reciprocal", "This is a reciprocal step.", "ответный", "Это ответный шаг."),
    ("excessive", "The noise was excessive.", "излишний", "Шум был излишним."),
    ("anniversary", "Today is his anniversary.", "юбилей", "Сегодня его юбилей."),
    ("skillfully", "She skillfully opened the door.", "ловко", "Она ловко открыла дверь."),
    ("salad", "I made a salad.", "салат", "Я сделал салат."),
    ("matrix", "I see the matrix.", "матрица", "Я вижу матрицу."),
    ("canvas", "She painted on the canvas.", "полотно", "Она рисовала на полотне."),
    ("documentation", "Please read the documentation.", "документация", "Пожалуйста, прочитайте документацию."),
    ("atom", "An atom is very small.", "атом", "Атом очень маленький."),
    ("directory", "I opened the directory.", "справочник", "Я открыл справочник."),
    ("showcase", "I saw a dress in the showcase.", "витрина", "Я видел платье в витрине."),
    ("analogue", "Find an analogue in nature.", "аналог", "Найдите аналог в природе."),
    ("managerial", "He has managerial work.", "управленческий", "У него управленческая работа."),
    ("narrative", "The narrative is important.", "повествование", "Повествование важно."),
    ("Kyiv-style", "This is a Kyiv-style dish.", "киевский", "Это киевское блюдо."),
    ("deck", "He stood on the ship's deck.", "палуба", "Он стоял на палубе корабля."),
    ("capitalist", "He criticized the capitalist system.", "капиталистический", "Он критиковал капиталистическую систему."),
    ("privatization", "Privatization of the factory started.", "приватизация", "Приватизация завода началась."),
    ("intermediary", "She was an intermediary in the deal.", "посредник", "Она была посредником в сделке."),
    ("dissatisfaction", "His dissatisfaction grew daily.", "недовольство", "Его недовольство росло с каждым днем."),
    ("waiter", "The waiter gave us tea.", "официант", "Официант дал нам чай."),
    ("electricity", "We need electricity at home.", "электричество", "Нам нужно электричество дома."),
    ("knock out", "He knocked out a tooth.", "выбить", "Он выбил зуб."),
    ("swimming", "I love swimming in the ocean.", "плавание", "Я люблю плавание в океане."),
    ("puppy", "The puppy is small.", "щенок", "Щенок маленький."),
    ("greenery", "The garden was full of greenery.", "зелень", "Сад был полон зелени."),
    ("how many", "How many apples did you buy?", "сколько", "Сколько яблок ты купил?"),
    ("elder", "The elder spoke to the people.", "старец", "Старец говорил с народом."),
    ("diplomat", "The diplomat came to the city.", "дипломат", "Дипломат приехал в город."),
    ("hurt", "Your words really hurt me.", "задеть", "Твои слова действительно задели меня."),
    ("vertical", "The line is vertical.", "вертикальный", "Линия вертикальная."),
    ("segment", "This is a market segment.", "сегмент", "Это сегмент рынка."),
    ("pot", "The pot is on the table.", "горшок", "Горшок стоит на столе."),
    ("hurtful", "This is hurtful.", "обидно", "Это обидно."),
    ("no matter", "No matter what he says.", "неважно", "Неважно, что он говорит."),
    ("moderator", "The moderator closes the topic.", "модератор", "Модератор закрывает тему."),
    ("to realize", "She began to realize the truth.", "сознавать", "Она начала сознавать правду."),
    ("medieval", "This is a medieval city.", "средневековый", "Это средневековый город."),
    ("thoracic", "He has thoracic pain.", "грудной", "У него грудная боль."),
    ("pie", "I like this pie.", "пирог", "Мне нравится этот пирог."),
    ("revelation", "His words were a revelation.", "откровение", "Его слова были откровением."),
    ("initially", "Initially I did not know this.", "первоначально", "Первоначально я этого не знал."),
    ("intermediate", "This is an intermediate step.", "промежуточный", "Это промежуточный шаг."),
    ("irony", "The irony of life surprises us.", "ирония", "Ирония жизни удивляет нас."),
    ("to recommend oneself", "It is hard to recommend oneself.", "рекомендоваться", "Трудно рекомендоваться."),
    ("work off", "He needs to work off his debt.", "отработать", "Ему нужно отработать свой долг."),
    ("Slavic", "She studies Slavic languages at university.", "славянский", "Она учит славянские языки в университете."),
    ("madness", "This is madness.", "безумие", "Это безумие."),
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


RU_IRREG = {
    "пить": ("пь",),
    "есть": ("ед", "еш", "ем", "ел"),
    "идти": ("ид", "шл", "ше"),
    "пойти": ("пой", "пош"),
    "мочь": ("мож", "мог"),
    "учить": ("уч",),
    "взять": ("возьм", "взя"),
    "видеть": ("виж", "вид"),
    "уйти": ("ушл", "уйд"),
    "хотеть": ("хоч", "хот"),
    "дать": ("дад", "дал", "даст"),
    "сесть": ("сяд", "сел"),
    "ехать": ("ед", "еха"),
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
