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

SRC = PACK / "_chunks" / "deck_15260268_02.csv"
OUT = PACK / "_chunks" / "fixed" / "deck_15260268_02.csv"
LOG = PACK / "_chunks" / "logs" / "deck_15260268_02.txt"

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
    ("executioner", "The executioner holds an axe.", "палач", "Палач держит топор."),
    ("alcoholic", "This drink is alcoholic.", "алкогольный", "Этот напиток алкогольный."),
    ("qualitatively", "They improved the product qualitatively.", "качественно", "Они качественно улучшили продукт."),
    ("premonition", "She had a premonition of danger.", "предчувствие", "У неё было предчувствие опасности."),
    ("mentor", "She has a mentor at school.", "наставник", "У неё есть наставник в школе."),
    ("to get angry", "He can get angry quickly.", "злиться", "Он может быстро злиться."),
    ("to crash", "The car was about to crash.", "разбиться", "Машина собиралась разбиться."),
    ("to react", "She was slow to react to danger.", "отреагировать", "Она медленно отреагировала на опасность."),
    ("pioneer", "He was a pioneer in this field.", "пионер", "Он был пионером в этой области."),
    ("watchman", "The watchman walks around the building at night.", "сторож", "Сторож ходит вокруг здания ночью."),
    ("herald", "The herald has the news.", "вестник", "У вестника есть новость."),
    ("ascent", "The ascent is hard.", "восхождение", "Восхождение сложное."),
    ("someone", "Someone waits at the door.", "некто", "Некто ждёт у двери."),
    ("sanction", "The state imposed a sanction.", "санкция", "Государство наложило санкцию."),
    ("decompose", "Fire will decompose the leaf.", "разложить", "Огонь разложит лист."),
    ("to be saved", "They pray to be saved from danger.", "спастись", "Они молятся, чтобы спастись от опасности."),
    ("sandwich", "I have a cheese sandwich today.", "бутерброд", "Сегодня у меня бутерброд с сыром."),
    ("assembly", "The assembly of the model will start now.", "сборка", "Сборка модели начнётся сейчас."),
    ("fright", "She screamed in sudden fright.", "испуг", "Она закричала от внезапного испуга."),
    ("temptation", "This temptation is strong.", "соблазн", "Этот соблазн сильный."),
    ("jeep", "The jeep is in the mud.", "джип", "Джип стоит в грязи."),
    ("Petersburg", "I love Petersburg at night.", "Петербург", "Я люблю Петербург ночью."),
    ("merger", "The merger created a strong company.", "слияние", "Слияние создало сильную компанию."),
    ("badge", "He has a new badge.", "значок", "У него есть новый значок."),
    ("arsenal", "The team has a new arsenal.", "арсенал", "У команды есть новый арсенал."),
    ("accelerate", "They want to accelerate the work.", "ускорить", "Они хотят ускорить работу."),
    ("mansion", "They live in a large mansion.", "особняк", "Они живут в большом особняке."),
    ("to sit out", "He had to sit out the whole night.", "просидеть", "Он просидел всю ночь."),
    ("absorb", "Plants absorb water and light.", "поглощать", "Растения поглощают воду и свет."),
    ("to flow", "Tears can flow from her eyes.", "литься", "Слёзы могут литься из её глаз."),
    ("notorious", "He is a notorious man.", "пресловутый", "Он пресловутый человек."),
    ("motionless", "The cat is motionless.", "неподвижный", "Кошка неподвижная."),
    ("bass", "He plays the bass.", "бас", "Он играет на басе."),
    ("to fall out", "My hair started to fall out.", "выпадать", "Мои волосы начали выпадать."),
    ("dismissal", "His dismissal is a shock.", "увольнение", "Его увольнение - удар."),
    ("to view", "I view the documents every day.", "просматривать", "Я просматриваю документы каждый день."),
    ("to be achieved", "Success is to be achieved through work.", "достигаться", "Успех должен достигаться через труд."),
    ("sociology", "I read sociology at university.", "социология", "Я читаю социологию в университете."),
    ("pirate", "The pirate has a gold box.", "пират", "У пирата есть ящик с золотом."),
    ("frog", "The frog jumped into the pond.", "лягушка", "Лягушка прыгнула в пруд."),
    ("nickname", "He has a new nickname.", "прозвище", "У него есть новое прозвище."),
    ("to reduce", "The list will reduce this year.", "сократиться", "Список сократится в этом году."),
    ("fourteen", "She is fourteen this year.", "четырнадцать", "Ей четырнадцать в этом году."),
    ("to dive", "He learned to dive in the sea.", "погружаться", "Он научился погружаться в море."),
    ("mosquito", "A mosquito is on my arm.", "комар", "Комар сидит на руке."),
    ("extremity", "Pain reached an extremity.", "крайность", "Боль дошла до крайности."),
    ("arena", "The arena is full of people.", "арена", "Арена полна народа."),
    ("defensive", "They have a defensive plan.", "оборонительный", "У них оборонительный план."),
    ("worthily", "He lived his life worthily.", "достойно", "Он прожил свою жизнь достойно."),
    ("heel", "Her heel is old.", "каблук", "Её каблук старый."),
    ("to question", "He will question the witness.", "расспрашивать", "Он будет расспрашивать свидетеля."),
    ("dictate", "Leaders dictate the team's plan.", "диктовать", "Руководители диктуют план команды."),
    ("student (female)", "The student passed her exam.", "студентка", "Студентка сдала экзамен."),
    ("reproduction", "Art reproduction needs attention.", "воспроизведение", "Воспроизведению искусства нужно внимание."),
    ("footbridge", "Cross the river on the footbridge.", "мостик", "Перейдите реку по мостику."),
    ("abortion", "She thought about an abortion.", "аборт", "Она думала об аборте."),
    ("frightened", "She was frightened.", "испуганный", "Она была испуганной."),
    ("annoyance", "His error was a great annoyance.", "досада", "Его ошибка была большой досадой."),
    ("to be published", "His articles are published every month.", "публиковаться", "Его статьи публикуются каждый месяц."),
    ("long before", "He came long before us.", "задолго", "Он пришёл задолго до нас."),
    ("repression", "Repression killed many voices.", "репрессия", "Репрессия убила многие голоса."),
    ("inflow", "The inflow of water is strong.", "приток", "Приток воды сильный."),
    ("steam locomotive", "The steam locomotive is loud.", "паровоз", "Паровоз громкий."),
    ("serf", "The serf worked the master's land.", "крепостной", "Крепостной работал на земле хозяина."),
    ("promote", "We want to promote our plan.", "продвинуть", "Мы хотим продвинуть наш план."),
    ("to look over", "I need to look over the room.", "оглядеть", "Мне нужно оглядеть комнату."),
    ("bronze", "She has a bronze medal.", "бронзовый", "У неё есть бронзовая медаль."),
    ("generalization", "This generalization is simple.", "обобщение", "Это обобщение простое."),
    ("villain", "The villain laughed loudly.", "злодей", "Злодей громко смеялся."),
    ("fade", "The stars will fade in the sky.", "погаснуть", "Звёзды погаснут в небе."),
    ("precipice", "He stands on the precipice in fear.", "обрыв", "Он стоит на обрыве в страхе."),
    ("picturesque", "The village looks picturesque.", "живописный", "Деревня выглядит живописной."),
    ("to match", "The colors match.", "сочетаться", "Цвета сочетаются."),
    ("undesirable", "This habit is undesirable.", "нежелательный", "Эта привычка нежелательная."),
    ("to fit in", "The work must fit in an hour.", "укладываться", "Работа должна укладываться в час."),
    ("impudent", "He is an impudent man.", "наглый", "Он наглый человек."),
    ("defect", "The product has a defect.", "дефект", "У продукта есть дефект."),
    ("blessed", "She is blessed in his love.", "блаженный", "Она блаженная в его любви."),
    ("Nizhny Novgorod", "I visited Nizhny Novgorod in summer.", "Нижний Новгород", "Я посетил Нижний Новгород летом."),
    ("missile", "The missile is in the sky.", "ракета", "Ракета в небе."),
    ("Murmansk", "Murmansk is a cold city.", "Мурманск", "Мурманск - холодный город."),
    ("considerably", "He has improved considerably.", "изрядно", "Он изрядно улучшился."),
    ("deign", "She did not deign to answer.", "изволить", "Она не изволила ответить."),
    ("beat off", "They beat off the attack.", "отбить", "Они отбили атаку."),
    ("miserable", "He lived in a miserable old house.", "убогий", "Он жил в убогом старом доме."),
    ("duel", "They have a duel at dawn.", "поединок", "У них поединок на рассвете."),
    ("to lock", "Please lock the door.", "запирать", "Пожалуйста, заприте дверь."),
    ("burst", "The glass burst.", "лопнуть", "Стекло лопнуло."),
    ("violin", "She played the violin.", "скрипка", "Она играла на скрипке."),
    ("lyrical", "Her voice is lyrical.", "лирический", "Её голос лирический."),
    ("casino", "She is at the casino.", "казино", "Она в казино."),
    ("garrison", "The garrison is ready for war.", "гарнизон", "Гарнизон готов к войне."),
    ("wrestler", "The wrestler has a match today.", "борец", "У борца сегодня матч."),
    ("fall apart", "The old house will fall apart.", "развалиться", "Старый дом развалится."),
    ("flax", "Flax is in the field.", "лён", "Лён лежит в поле."),
    ("paragraph", "Start a new paragraph here.", "абзац", "Начните новый абзац здесь."),
    ("to punish", "They punish the thief.", "наказывать", "Они наказывают вора."),
    ("interrelation", "The interrelation between events is clear.", "взаимосвязь", "Взаимосвязь между событиями ясна."),
    ("little by little", "Little by little, he improved his work.", "понемногу", "Понемногу он улучшал свою работу."),
    ("briefly", "He briefly explained the plan.", "кратко", "Он кратко объяснил план."),
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
