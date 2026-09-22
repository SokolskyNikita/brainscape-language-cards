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

SRC = PACK / "_chunks" / "deck_15260260_03.csv"
OUT = PACK / "_chunks" / "fixed" / "deck_15260260_03.csv"
LOG = PACK / "_chunks" / "logs" / "deck_15260260_03.txt"

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
    ("sudden", "A sudden noise scared me.", "внезапный", "Внезапный шум испугал меня."),
    ("wait for", "We'll wait for the rain to stop.", "дожидаться", "Мы будем дожидаться, пока дождь прекратится."),
    ("width", "Measure the table's width, please.", "ширина", "Измерьте, пожалуйста, ширину стола."),
    ("orange", "The sunset sky turned bright orange.", "оранжевый", "Небо на закате стало ярко-оранжевым."),
    ("spelling", "Check the spelling carefully.", "написание", "Внимательно проверьте написание."),
    ("subjective", "Beauty is highly subjective.", "субъективный", "Красота в высшей степени субъективна."),
    ("demon", "He fought a demon.", "демон", "Он боролся с демоном."),
    ("tenth", "He was in tenth place.", "десятый", "Он был на десятом месте."),
    ("nest", "Birds build a nest in spring.", "гнездо", "Птицы строят гнездо весной."),
    ("eleven", "We have eleven books.", "одиннадцать", "У нас есть одиннадцать книг."),
    ("celebration", "The city had a celebration.", "торжество", "В городе было торжество."),
    ("modernization", "Modernization is important for the city.", "модернизация", "Модернизация важна для города."),
    ("correspondence", "We continued our correspondence for years.", "переписка", "Мы продолжали нашу переписку на протяжении многих лет."),
    ("barrier", "This barrier is high.", "барьер", "Этот барьер высокий."),
    ("rally", "This is a political rally.", "митинг", "Это политический митинг."),
    ("introduce oneself", "I need to introduce myself.", "представиться", "Мне нужно представиться."),
    ("opera", "She loves the opera.", "опера", "Она любит оперу."),
    ("conscious", "He made a conscious effort to improve.", "сознательный", "Он приложил сознательные усилия, чтобы улучшиться."),
    ("suicide", "I read about his suicide.", "самоубийство", "Я читал о его самоубийстве."),
    ("resort to", "They will resort to this.", "прибегать", "Они прибегнут к этому."),
    ("rank", "He achieved a high military rank.", "ранг", "Он достиг высокого военного ранга."),
    ("soap", "I bought new soap today.", "мыло", "Я купил новое мыло сегодня."),
    ("corruption", "Corruption is a big problem.", "коррупция", "Коррупция - большая проблема."),
    ("orchestra", "The orchestra played music.", "оркестр", "Оркестр играл музыку."),
    ("to prohibit", "Laws exist to prohibit this.", "запрещать", "Законы существуют, чтобы запрещать это."),
    ("rumble", "I heard a rumble.", "грохот", "Я слышал грохот."),
    ("orbit", "The moon has an orbit.", "орбита", "У луны есть орбита."),
    ("get free", "He managed to get free.", "освободиться", "Он смог освободиться."),
    ("Finnish", "I am learning Finnish.", "финский", "Я учу финский."),
    ("imply", "His words imply a secret.", "подразумевать", "Его слова подразумевают секрет."),
    ("to hand over", "I need to hand over the documents.", "вручить", "Мне нужно вручить документы."),
    ("pregnant", "She is pregnant.", "беременный", "Она беременна."),
    ("to complain", "She called to complain about noise.", "пожаловаться", "Она позвонила, чтобы пожаловаться на шум."),
    ("to the right", "Turn to the right here.", "направо", "Поверните здесь направо."),
    ("stubbornly", "He stubbornly refused to give up.", "упорно", "Он упорно отказывался сдаваться."),
    ("aroma", "I like the aroma in the kitchen.", "аромат", "Мне нравится аромат на кухне."),
    ("chin", "His chin is on his hand.", "подбородок", "Его подбородок на руке."),
    ("three hundred", "I have three hundred dollars.", "триста", "У меня триста долларов."),
    ("condemn", "They will condemn his actions.", "осудить", "Они осудят его действия."),
    ("soup", "I made chicken soup for dinner.", "суп", "Я сделал куриный суп на ужин."),
    ("embrace", "He gave her a warm embrace.", "объятие", "Он дал ей тёплое объятие."),
    ("midnight", "It was midnight.", "полночь", "Была полночь."),
    ("storm", "The storm was strong.", "буря", "Буря была сильной."),
    ("disappointment", "His gift was a huge disappointment.", "разочарование", "Его подарок был огромным разочарованием."),
    ("dormitory", "I live in a dormitory.", "общежитие", "Я живу в общежитии."),
    ("analyst", "The analyst reviewed the financial report.", "аналитик", "Аналитик изучил финансовый отчет."),
    ("citizenship", "She received citizenship.", "гражданство", "Она получила гражданство."),
    ("to develop", "We plan to develop a program.", "разрабатывать", "Мы планируем разрабатывать программу."),
    ("inhabitant", "The cave's inhabitant was a bear.", "обитатель", "Обитателем пещеры был медведь."),
    ("durable", "This backpack is very durable.", "прочный", "Этот рюкзак очень прочный."),
    ("neighbor (female)", "This is my neighbor (female).", "соседка", "Это моя соседка."),
    ("filter", "Change the coffee filter, please.", "фильтр", "Пожалуйста, замените фильтр для кофе."),
    ("due", "This is due respect.", "должный", "Это должное уважение."),
    ("touch", "Your story touched my heart.", "тронуть", "Ваша история тронула мое сердце."),
    ("cut", "I need to cut the bread.", "резать", "Мне нужно резать хлеб."),
    ("courage", "She showed great courage under fire.", "мужество", "Она проявила большое мужество под огнем."),
    ("parallel", "We walked parallel to the river.", "параллельно", "Мы шли параллельно реке."),
    ("delay", "The delay was long.", "задержка", "Задержка была долгой."),
    ("entitled", "You are entitled to your opinion.", "вправе", "Вы вправе иметь своё мнение."),
    ("physically", "He is physically strong.", "физически", "Он физически сильный."),
    ("hurray", '"Hurray, we did it!"', "ура", '"Ура, мы сделали это!"'),
    ("physicist", "The physicist solved the complex problem.", "физик", "Физик решил сложную задачу."),
    ("swear", "I swear to always tell the truth.", "клясться", "Я клянусь всегда говорить правду."),
    ("stable", "The economy is finally stable.", "стабильный", "Экономика наконец стабильна."),
    ("commodity", "Gold is a valuable commodity.", "товар", "Золото - ценный товар."),
    ("not long", "She was here not long.", "недолго", "Она была здесь недолго."),
    ("to resist", "He tried to resist.", "сопротивляться", "Он пытался сопротивляться."),
    ("gently", "He gently held her hand.", "нежно", "Он нежно держал её за руку."),
    ("smooth", "The stone's surface felt smooth.", "гладкий", "Поверхность камня была гладкой."),
    ("ghost", "I saw a ghost.", "призрак", "Я видел призрак."),
    ("to see off", "They came to see off their friend.", "провожать", "Они пришли провожать своего друга."),
    ("conditional", "The offer is conditional.", "условный", "Предложение условное."),
    ("regular", "This is a regular meeting.", "регулярный", "Это регулярная встреча."),
    ("adequate", "His response was perfectly adequate.", "адекватный", "Его ответ был абсолютно адекватным."),
    ("ouch", '"Ouch, that is hot!"', "ай", '"Ай, это горячо!"'),
    ("customs", "This is a customs rule.", "таможенный", "Это таможенное правило."),
    ("externally", "She looks calm externally.", "внешне", "Она внешне выглядит спокойной."),
    ("excursion", "We planned a river excursion tomorrow.", "экскурсия", "Мы запланировали речную экскурсию на завтра."),
    ("seed", "Plant the seed and watch it grow.", "семя", "Посади семя и наблюдай, как оно растет."),
    ("super", "Your idea is super!", "супер", "Твоя идея супер!"),
    ("duration", "The movie's duration was three hours.", "продолжительность", "Продолжительность фильма составила три часа."),
    ("decoration", "The room needs more decoration.", "украшение", "Комнате нужно больше украшения."),
    ("slim", "She has a slim figure.", "стройный", "У неё стройная фигура."),
    ("depression", "She has depression.", "депрессия", "У неё депрессия."),
    ("radical", "He offered a radical solution.", "радикальный", "Он предложил радикальное решение."),
    ("to devote", "She decided to devote more time to studying.", "уделять", "Она решила уделять больше времени учёбе."),
    ("TV series", "I love watching that TV series.", "сериал", "Мне нравится смотреть этот сериал."),
    ("vegetable", "A potato is a vegetable.", "овощ", "Картошка - это овощ."),
    ("focus", "The photo is in focus.", "фокус", "Фото в фокусе."),
    ("firefighter", "The firefighter is here.", "пожарный", "Пожарный здесь."),
    ("chat", "Let's chat over coffee tomorrow.", "болтать", "Давай завтра поболтаем за чашкой кофе."),
    ("residence", "His residence is in this city.", "проживание", "Его проживание в этом городе."),
    ("to contact", "I need to contact my friend.", "связаться", "Мне нужно связаться с моим другом."),
    ("to reflect", "The moon reflects in the water.", "отражаться", "Луна отражается в воде."),
    ("symptom", "This is a symptom of the disease.", "симптом", "Это симптом болезни."),
    ("alley", "The alley is dark.", "переулок", "В переулке темно."),
    ("barrel", "The barrel was filled with wine.", "бочка", "Бочка была наполнена вином."),
    ("to turn", "I turn around.", "поворачиваться", "Я поворачиваюсь."),
    ("doubtful", "His words seem doubtful to me.", "сомнительный", "Его слова сомнительные."),
    ("shard", "He stepped on a sharp shard.", "осколок", "Он наступил на острый осколок."),
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
    "fought": "fight", "heard": "hear", "held": "hold", "began": "begin",
    "became": "become", "built": "build", "shown": "show", "showed": "show",
}


def en_ok(text: str, extra: set[str]) -> list[str]:
    bad = []
    pool = allow_en | extra
    for raw in re.findall(r"[A-Za-z']+", text):
        w = raw.lower().replace("'", "")
        if not w or w in pool:
            continue
        if IRREGULAR_EN.get(w, "") in pool:
            continue
        if any(form in pool for form in en_forms(w)):
            continue
        if w.endswith("ly") and w[:-2] in pool:
            continue
        for lemma in pool:
            parts = lemma.replace("-", " ").split()
            if w in parts:
                break
        else:
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
    bad = []
    pool = allow_ru | extra
    for raw in re.findall(r"[А-Яа-яЁё-]+", text):
        if raw.replace("-", "") == "":
            continue
        w = raw.replace("ё", "е").replace("Ё", "е").lower()
        if w in pool:
            continue
        stems = ru_stems(w)
        if any(stem in pool for stem in stems if len(stem) >= 3):
            continue
        if any(w.startswith(lemma) or lemma.startswith(w) for lemma in pool if len(lemma) >= 4 and len(w) >= 4):
            continue
        if any(
            w[: max(4, len(w) - 3)] == lemma[: max(4, len(w) - 3)]
            for lemma in pool
            if abs(len(lemma) - len(w)) <= 4 and min(len(lemma), len(w)) >= 4
        ):
            continue
        if any(stem.startswith(lemma[:4]) or lemma.startswith(stem[:4]) for lemma in pool for stem in stems if len(lemma) >= 4 and len(stem) >= 4):
            continue
        if any(
            lemma in pool and any(w.startswith(stem) or stem.startswith(w[:3]) for stem in stems_list)
            for lemma, stems_list in {
                "дать": ("да", "дад", "дал"),
                "жить": ("жив",),
                "идти": ("ид", "шл", "ше"),
                "пойти": ("пой", "пош"),
                "прийти": ("прид", "приш"),
                "мочь": ("мож", "мог"),
                "смочь": ("смог", "смож"),
                "учить": ("уч",),
                "знать": ("зна",),
                "рука": ("рук",),
                "луна": ("лун",),
                "река": ("рек",),
                "вода": ("вод",),
                "год": ("лет",),
                "новый": ("нов",),
                "камень": ("камн",),
                "клясться": ("клян", "кляс"),
                "резать": ("реж",),
                "казаться": ("каж", "каз"),
                "приходить": ("приш", "приход"),
                "приходиться": ("пришл",),
                "сила": ("сил",),
                "высокий": ("высш", "высок"),
                "отчёт": ("отчет",),
                "отчет": ("отчет",),
                "план": ("планир",),
                "болтать": ("болт",),
            }.items()
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
    parts = [p for p in key.replace("-", " ").replace("(", " ").replace(")", " ").split() if p not in {"to", "the", "a", "an", "be"}]
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
        extra_en |= set(en.lower().replace("-", " ").replace("(", " ").replace(")", " ").split())
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
    else:
        print("vocab check clean")


if __name__ == "__main__":
    main()
