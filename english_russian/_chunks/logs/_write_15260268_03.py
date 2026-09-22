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

SRC = PACK / "_chunks" / "deck_15260268_03.csv"
OUT = PACK / "_chunks" / "fixed" / "deck_15260268_03.csv"
LOG = PACK / "_chunks" / "logs" / "deck_15260268_03.txt"

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

# (en_lemma, en_ex, ru_lemma, ru_ex)
FIXED = [
    ("toast", "We raise a toast to friendship.", "тост", "Мы поднимаем тост за дружбу."),
    ("exceed", "Our costs exceed our income.", "превысить", "Наши расходы превысили наш доход."),
    ("silhouette", "A silhouette stands in the light.", "силуэт", "Силуэт стоит в свете."),
    ("competence", "She has high competence.", "компетенция", "У неё высокая компетенция."),
    ("reproduce", "Plants can reproduce.", "воспроизводить", "Растения могут воспроизводиться."),
    ("uniform", "He wears his military uniform.", "мундир", "Он носит свой военный мундир."),
    ("Archangel", "The archangel stood in the light.", "архангел", "Архангел стоял в свете."),
    ("ruins", "Ancient ruins stand here.", "развалины", "Древние развалины стоят здесь."),
    ("skeleton", "The museum has a skeleton.", "скелет", "В музее есть скелет."),
    ("Czech", "I like Czech beer.", "чешский", "Мне нравится чешское пиво."),
    ("whistle", "I hear a loud whistle.", "свист", "Я слышу громкий свист."),
    ("sinister", "The forest looked sinister at night.", "зловещий", "Лес ночью выглядел зловещим."),
    ("senator", "The senator spoke for a long time.", "сенатор", "Сенатор долго говорил."),
    ("to be indignant", "She will be indignant.", "возмутиться", "Она возмутится."),
    ("sympathize", "I sympathize with your loss.", "сочувствовать", "Я сочувствую вашей потере."),
    ("hay", "The field is full of hay.", "сено", "Поле полно сена."),
    ("doom", "They will doom him.", "обречь", "Они обрекут его."),
    ("brotherhood", "There is a strong brotherhood.", "братство", "Есть сильное братство."),
    ("nanny", "The nanny is in the house.", "няня", "Няня в доме."),
    ("moderate", "This is a moderate price.", "умеренный", "Это умеренная цена."),
    ("London", "London is a big city.", "Лондон", "Лондон - большой город."),
    ("bow", "She took a bow.", "поклон", "Она сделала поклон."),
    ("arc", "There is an arc in the sky.", "дуга", "В небе есть дуга."),
    ("subtlety", "I like her subtlety in art.", "тонкость", "Мне нравится её тонкость в искусстве."),
    ("denial", "This is a clear denial.", "отрицание", "Это ясное отрицание."),
    ("unfavorable", "The weather was unfavorable.", "неблагоприятный", "Погода была неблагоприятной."),
    ("internally", "She felt internally calm.", "внутренне", "Она чувствовала себя внутренне спокойной."),
    ("traitor", "He is a traitor.", "предатель", "Он предатель."),
    ("migration", "Birds prepare for migration south.", "миграция", "Птицы готовятся к миграции на юг."),
    ("erotic", "She read an erotic book.", "эротический", "Она читала эротическую книгу."),
    ("to wave", "He will wave his flag.", "размахивать", "Он будет размахивать флагом."),
    ("little heap", "She made a little heap.", "кучка", "Она сделала кучку."),
    ("Mercedes", "I have a red Mercedes.", "мерседес", "У меня есть красный мерседес."),
    ("thickly", "Snow will fall thickly at night.", "густо", "Ночью снег будет идти густо."),
    ("from afar", "I saw him from afar.", "издали", "Я видел его издали."),
    ("disco", "We danced at night at the disco.", "дискотека", "Мы танцевали ночью на дискотеке."),
    ("endow", "They will endow him with power.", "наделить", "Они наделят его властью."),
    ("veil", "The veil came down quietly.", "покров", "Покров тихо спустился."),
    ("unfair", "This law is unfair.", "несправедливый", "Этот закон несправедливый."),
    ("break down", "My car will break down soon.", "сломаться", "Моя машина скоро сломается."),
    ("construction site", "The construction site is very noisy.", "стройка", "Стройка очень шумная."),
    ("compartment", "I sat in the compartment.", "купе", "Я сидел в купе."),
    ("ordinary person", "An ordinary person is here.", "обыватель", "Обыватель здесь."),
    ("peer", "She will peer into the darkness.", "вглядываться", "Она будет вглядываться в темноту."),
    ("to run out", "He ran out of the house.", "выбежать", "Он выбежал из дома."),
    ("to linger", "She likes to linger here.", "задерживаться", "Она любит задерживаться здесь."),
    ("disagreement", "Their disagreement is strong.", "разногласие", "Их разногласие сильное."),
    ("modernity", "I do not like this modernity.", "современность", "Мне не нравится эта современность."),
    ("Sverdlovsk", "Sverdlovsk is a large city.", "Свердловск", "Свердловск - большой город."),
    ("farmer", "The farmer works in the field.", "фермер", "Фермер работает в поле."),
    ("to tower", "The castle towers above us.", "возвышаться", "Замок возвышается над нами."),
    ("compliment", "He gave her a sincere compliment.", "комплимент", "Он сделал ей искренний комплимент."),
    ("hail", "There was hail on the field today.", "град", "Сегодня на поле был град."),
    ("caviar", "She likes caviar.", "икра", "Ей нравится икра."),
    ("cruelly", "He was cruelly punished for his error.", "жестоко", "Он был жестоко наказан за свою ошибку."),
    ("jerk", "The car gave a sudden jerk.", "рывок", "Машина сделала внезапный рывок."),
    ("Nazi", "He was a Nazi.", "гитлеровец", "Он был гитлеровцем."),
    ("earthquake", "The earthquake was strong.", "землетрясение", "Землетрясение было сильным."),
    ("execute", "They will execute the traitor tomorrow.", "казнить", "Завтра они казнят предателя."),
    ("finding", "The finding of treasure is important.", "нахождение", "Нахождение сокровища важно."),
    ("ceremonial", "The ceremonial dress was truly magnificent.", "парадный", "Парадный наряд был поистине великолепен."),
    ("proclaim", "They will proclaim their love.", "провозгласить", "Они провозгласят свою любовь."),
    ("correction", "He made a correction to the document.", "коррекция", "Он сделал коррекцию в документе."),
    ("claw", "The cat has a sharp claw.", "коготь", "У кошки острый коготь."),
    ("to join", "I join their team.", "присоединяться", "Я присоединяюсь к их команде."),
    ("totalitarian", "The regime was totalitarian.", "тоталитарный", "Режим был тоталитарным."),
    ("exotic", "She wears an exotic dress.", "экзотический", "Она носит экзотическое платье."),
    ("mineral", "This water is mineral.", "минеральный", "Эта вода минеральная."),
    ("gait", "His gait is slow.", "походка", "Его походка медленная."),
    ("related", "This is a related question.", "родственный", "Это родственный вопрос."),
    ("uterus", "The uterus is in the body.", "матка", "Матка в теле."),
    ("swan", "A swan is on the lake.", "лебедь", "Лебедь на озере."),
    ("Easter", "Easter is in spring.", "пасха", "Пасха весной."),
    ("to run up", "He ran up to me.", "подбежать", "Он подбежал ко мне."),
    ("interact", "They interact with animals.", "взаимодействовать", "Они взаимодействуют с животными."),
    ("chest", "He found treasure in the old chest.", "сундук", "Он нашёл сокровище в старом сундуке."),
    ("granddaughter", "My granddaughter is here.", "внучка", "Моя внучка здесь."),
    ("conservative", "He is conservative.", "консервативный", "Он консервативный."),
    ("to settle in", "They can settle in quickly.", "устраиваться", "Они могут быстро устраиваться."),
    ("theft", "There was a theft at the store.", "кража", "В магазине была кража."),
    ("I bet", "I bet he is already here.", "небось", "Небось, он уже здесь."),
    ("comprehend", "I did not comprehend his explanation.", "осмыслить", "Я не осмыслил его объяснение."),
    ("therapeutic", "The therapeutic massage relieved my pain.", "лечебный", "Лечебный массаж облегчил мою боль."),
    ("foggy", "The morning was foggy and cold.", "туманный", "Утро было туманным и холодным."),
    ("Dutch", "I like Dutch cheese.", "голландский", "Мне нравится голландский сыр."),
    ("grace", "She felt the grace of God.", "благодать", "Она чувствовала благодать Бога."),
    ("parade", "We watched the parade.", "парад", "Мы смотрели парад."),
    ("rehabilitation", "He needs rehabilitation.", "реабилитация", "Ему нужна реабилитация."),
    ("volunteer", "He is a volunteer.", "доброволец", "Он доброволец."),
    ("uranium", "They found uranium.", "уран", "Они нашли уран."),
    ("to break", "He will break the glass with a hammer.", "разбивать", "Он будет разбивать стекло молотком."),
    ("counteraction", "The government has a counteraction plan.", "противодействие", "У правительства есть план противодействия."),
    ("scales", "The scales are on the table.", "весы", "Весы стоят на столе."),
    ("henceforth", "Henceforth, please lock the door.", "впредь", "Впредь, пожалуйста, заприте дверь."),
    ("countryman", "He is my countryman.", "земляк", "Он мой земляк."),
    ("limitation period", "The limitation period is over.", "давность", "Срок давности прошёл."),
    ("encourage", "They encourage me.", "поощрять", "Они поощряют меня."),
    ("to catch fire", "The dry leaf will catch fire.", "загореться", "Сухой лист загорится."),
    ("thinker", "He is a thinker.", "мыслитель", "Он мыслитель."),
    ("rector", "The rector announced a policy.", "ректор", "Ректор объявил политику."),
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
