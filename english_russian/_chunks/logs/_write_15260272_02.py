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

SRC = PACK / "_chunks" / "deck_15260272_02.csv"
OUT = PACK / "_chunks" / "fixed" / "deck_15260272_02.csv"
LOG = PACK / "_chunks" / "logs" / "deck_15260272_02.txt"

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
    "just", "quite", "soon", "quickly", "easily", "slowly", "tonight",
    "last", "year", "up", "down", "out", "off", "onto", "upon", "around",
    "against", "during", "while", "because", "until", "since", "though",
    "each", "every", "both", "own", "same", "other", "another", "new",
    "old", "good", "bad", "big", "small", "long", "short", "high", "low",
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
    ("lyrics", "She writes new lyrics.", "лирика", "Она пишет новую лирику."),
    ("foreign car", "He bought a new foreign car.", "иномарка", "Он купил новую иномарку."),
    ("to seat", "Please seat the guests.", "усадить", "Пожалуйста, усадите гостей."),
    ("unfasten", "Please unfasten your jacket.", "расстегнуть", "Пожалуйста, расстегните куртку."),
    ("terrace", "We sat on the terrace.", "терраса", "Мы сидели на террасе."),
    ("Pskov", "Pskov is an old city.", "Псков", "Псков — старый город."),
    ("to shudder", "I began to shudder in fear.", "вздрагивать", "Я начал вздрагивать от страха."),
    ("innovation", "They have this innovation.", "инновация", "У них есть эта инновация."),
    ("lane", "This is a narrow lane.", "улочка", "Это узкая улочка."),
    ("mistake", "He made a big mistake yesterday.", "косяк", "Он сделал большой косяк вчера."),
    ("epaulet", "His epaulet is on the jacket.", "погон", "Его погон на куртке."),
    ("paralyze", "Fear can paralyze him.", "парализовать", "Страх может его парализовать."),
    ("visually", "He showed it visually.", "наглядно", "Он наглядно это показал."),
    ("grumble", "He began to grumble about the cold.", "ворчать", "Он начал ворчать на холод."),
    ("think over", "I will think over your plan tonight.", "обдумать", "Я обдумаю ваш план сегодня вечером."),
    ("embarrassment", "I felt embarrassment.", "смущение", "Я чувствовал смущение."),
    ("prisoner", "The prisoner wants freedom.", "пленник", "Пленник хочет свободы."),
    ("following", "Following the law is important.", "следование", "Следование закону важно."),
    ("ale", "He drinks ale at home.", "эль", "Он пьёт эль дома."),
    ("to prick", "Do not prick your finger.", "колоть", "Не коли палец."),
    ("oar", "He has an oar in the boat.", "весло", "У него в лодке есть весло."),
    ("rice", "I cooked rice for dinner.", "рис", "Я готовил рис на ужин."),
    ("to curse", "She began to curse her fate.", "проклинать", "Она начала проклинать свою судьбу."),
    ("edit", "I need to edit this text.", "редактировать", "Мне нужно редактировать этот текст."),
    ("whimsical", "She has a whimsical dress.", "причудливый", "У неё причудливое платье."),
    ("preparatory", "She went to a preparatory school.", "подготовительный", "Она ходила в подготовительную школу."),
    ("to get distracted", "I get distracted easily.", "отвлекаться", "Я легко отвлекаюсь."),
    ("traffic", "The traffic is heavy.", "трафик", "Трафик большой."),
    ("prejudice", "He has an old prejudice.", "предрассудок", "У него старый предрассудок."),
    ("ruling", "This is the ruling party.", "правящий", "Это правящая партия."),
    ("motivate", "Teachers motivate students to learn.", "мотивировать", "Учителя мотивируют студентов учиться."),
    ("twirl", "She loves to twirl her hair.", "вертеть", "Она любит вертеть волосами."),
    ("youthful", "He has a youthful face.", "юношеский", "У него юношеское лицо."),
    ("greed", "His greed is strong.", "жадность", "Его жадность сильна."),
    ("whiskey", "He drinks whiskey slowly.", "виски", "Он медленно пьёт виски."),
    ("dialectics", "He studies dialectics.", "диалектика", "Он учит диалектику."),
    ("to have fun", "We went to the park to have fun.", "развлекаться", "Мы пошли в парк развлекаться."),
    ("provoke", "His words provoke anger.", "провоцировать", "Его слова провоцируют гнев."),
    ("autonomy", "They wanted more autonomy at work.", "автономия", "Они хотели большей автономии на работе."),
    ("storyteller", "The storyteller told a story.", "рассказчик", "Рассказчик рассказал историю."),
    ("bracket", "Put the number in brackets.", "скобка", "Поставьте число в скобки."),
    ("pedagogy", "She studies pedagogy.", "педагогика", "Она учит педагогику."),
    ("reflex", "This is a natural reflex.", "рефлекс", "Это естественный рефлекс."),
    ("dealer", "The dealer sold the car.", "дилер", "Дилер продал машину."),
    ("vain", "It was a vain attempt.", "напрасный", "Это была напрасная попытка."),
    ("cost price", "The cost price is high.", "себестоимость", "Себестоимость высокая."),
    ("fort", "The old fort is large.", "форт", "Старый форт большой."),
    ("aesthetics", "He studies aesthetics.", "эстетика", "Он учит эстетику."),
    ("clergy", "The clergy is in the church.", "духовенство", "Духовенство в церкви."),
    ("landowner", "The landowner has a large house.", "помещик", "У помещика большой дом."),
    ("egoism", "Egoism is a bad thing.", "эгоизм", "Эгоизм — плохая вещь."),
    ("to plow", "Farmers need to plow their fields.", "пахать", "Фермерам нужно пахать свои поля."),
    ("therapist", "I visited the therapist yesterday.", "терапевт", "Я посетил терапевта вчера."),
    ("harbor", "The ship is in the harbor.", "гавань", "Корабль в гавани."),
    ("zemsky", "The zemsky doctor visited the village.", "земский", "Земский врач посетил деревню."),
    ("subside", "The storm will soon subside.", "затихнуть", "Скоро буря затихнет."),
    ("indecent", "That joke was quite indecent.", "неприличный", "Эта шутка была довольно неприличной."),
    ("idiotic", "That was an idiotic mistake.", "идиотский", "Это была идиотская ошибка."),
    ("spiritually", "She is spiritually strong.", "духовно", "Она духовно сильна."),
    ("eclipse", "We saw the eclipse yesterday.", "затмение", "Мы видели затмение вчера."),
    ("overtake", "I will overtake you soon.", "опередить", "Я скоро тебя опережу."),
    ("explanatory", "This is an explanatory dictionary.", "толковый", "Это толковый словарь."),
    ("skillful", "He is a skillful man.", "ловкий", "Он ловкий человек."),
    ("oppositional", "He joined an oppositional party.", "оппозиционный", "Он вступил в оппозиционную партию."),
    ("violent", "It was a violent death.", "насильственный", "Это была насильственная смерть."),
    ("to be on duty", "She had to be on duty tonight.", "дежурить", "Она должна была дежурить сегодня ночью."),
    ("high-speed", "The high-speed train leaves at noon.", "скоростной", "Скоростной поезд уходит в полдень."),
    ("change clothes", "I need to change clothes quickly.", "переодеться", "Мне нужно быстро переодеться."),
    ("meager", "Their food was meager.", "скудный", "Их еда была скудной."),
    ("diabetes", "She has diabetes.", "диабет", "У неё диабет."),
    ("to eat up", "She loves to eat up her vegetables.", "съедать", "Она любит съедать свои овощи."),
    ("schism", "The schism divided the church.", "раскол", "Раскол разделил церковь."),
    ("abuse", "This is abuse of power.", "злоупотребление", "Это злоупотребление властью."),
    ("monarch", "The monarch is in the city.", "монарх", "Монарх в городе."),
    ("main line", "The main line is closed.", "магистраль", "Магистраль закрыта."),
    ("snowdrift", "The car is in a snowdrift.", "сугроб", "Машина в сугробе."),
    ("Korean", "I love Korean food.", "корейский", "Я люблю корейскую еду."),
    ("motto", "This is my motto.", "девиз", "Это мой девиз."),
    ("tide", "The tide is coming in now.", "прилив", "Прилив сейчас наступает."),
    ("copying", "Copying the document takes time.", "копирование", "Копирование документа занимает время."),
    ("defenseless", "She looked defenseless.", "беззащитный", "Она выглядела беззащитной."),
    ("to turn pale", "She turned pale with fear.", "побледнеть", "Она побледнела от страха."),
    ("addressee", "The addressee received the letter.", "адресат", "Адресат получил письмо."),
    ("last year's", "I remember last year's summer.", "прошлогодний", "Я помню прошлогоднее лето."),
    ("sauce", "I added sauce to the meat.", "соус", "Я добавил соус к мясу."),
    ("to wince", "He winced in pain.", "поморщиться", "Он поморщился от боли."),
    ("sovereignty", "The country wants sovereignty.", "суверенитет", "Страна хочет суверенитета."),
    ("informal", "We had an informal meeting today.", "неформальный", "Сегодня у нас была неформальная встреча."),
    ("veranda", "We sat on the veranda all evening.", "веранда", "Мы сидели на веранде весь вечер."),
    ("rhyme", "This poem has a rhyme.", "рифма", "В этих стихах есть рифма."),
    ("a bit", "I am tired, just a bit.", "малость", "Я устал, малость."),
    ("sneak in", "They could sneak in at night.", "пробраться", "Они могли пробраться ночью."),
    ("mentality", "He has a different mentality.", "менталитет", "У него другой менталитет."),
    ("nostril", "His left nostril is closed.", "ноздря", "Его левая ноздря закрыта."),
    ("smelly", "This shirt is smelly.", "вонючий", "Эта рубашка вонючая."),
    ("distribute", "Please distribute the books.", "распределять", "Пожалуйста, распределите книги."),
    ("straighten up", "Please straighten up.", "выпрямиться", "Пожалуйста, выпрямитесь."),
    ("calling", "This work is her calling.", "призвание", "Эта работа — её призвание."),
    ("Kazakhstani", "He is a Kazakhstani writer.", "казахстанский", "Он казахстанский писатель."),
    ("to overturn", "The boat overturned quickly.", "перевернуться", "Лодка быстро перевернулась."),
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
    "winced": "wince", "overturned": "overturn",
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
