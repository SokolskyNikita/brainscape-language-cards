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

SRC = PACK / "_chunks" / "deck_15260263_00.csv"
OUT = PACK / "_chunks" / "fixed" / "deck_15260263_00.csv"
LOG = PACK / "_chunks" / "logs" / "deck_15260263_00.txt"

FUNCTION_EN = {
    "a", "the", "is", "be", "i", "you", "he", "she", "it", "we", "they",
    "my", "and", "or", "in", "on", "at", "to", "of", "for", "with", "from",
    "not", "his", "him", "her", "their", "them", "our", "us", "me", "am",
    "are", "was", "were", "been", "being", "this", "that", "these", "those",
    "an", "as", "by", "into", "about", "than", "then", "so", "if", "but",
    "its", "your", "all", "no", "yes", "do", "does", "did", "done", "doing",
    "has", "have", "had", "having", "will", "would", "can", "could", "may",
    "might", "must", "shall", "should", "just", "also", "too", "very",
    "there", "here", "now", "today", "yesterday", "tomorrow", "some", "any",
    "more", "most", "less", "much", "many", "few", "such", "only", "even",
    "still", "already", "always", "never", "often", "once", "after", "before",
    "under", "over", "through", "between", "without", "who", "what", "when",
    "where", "why", "how", "which", "please", "im", "dont", "cant", "lets",
    "didnt", "wont", "isnt",
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
        "а", "но", "или", "эту", "этого", "этой", "этому", "этих", "этими",
        "этим", "этом", "того", "той", "тому", "тех", "теми", "тем",
        "свою", "своего", "своей", "своему", "своим", "своих", "своими",
        "мою", "твою", "нашу", "вашу", "будь", "будьте",
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
    "flew": "fly", "led": "lead", "met": "meet", "won": "win", "sang": "sing",
    "fell": "fall", "laid": "lay", "hit": "hit", "put": "put", "set": "set",
    "let": "let", "cut": "cut", "built": "build", "ill": "i",
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
    ("safely", "They arrived safely home.", "благополучно", "Они благополучно прибыли домой."),
    ("herd", "The herd is large.", "стадо", "Стадо большое."),
    ("to be mentioned", "His name is mentioned in the report.", "упоминаться", "Его имя упоминается в докладе."),
    ("portion", "She has a small portion.", "порция", "У неё небольшая порция."),
    ("sidewalk", "I am on the sidewalk.", "тротуар", "Я на тротуаре."),
    ("panic", "There was panic in the city.", "паника", "В городе была паника."),
    ("flight", "The flight is at noon.", "рейс", "Рейс в полдень."),
    ("Christmas", "Christmas brings families together.", "рождество", "Рождество собирает вместе семьи."),
    ("secular", "This school is secular.", "светский", "Эта школа светская."),
    ("to insist", "She continued to insist.", "настаивать", "Она продолжала настаивать."),
    ("characterize", "Critics characterize the movie as good.", "характеризовать", "Критики характеризуют фильм как хороший."),
    ("checkmate", "He declared checkmate.", "мат", "Он объявил мат."),
    ("academic", "She pursued an academic career.", "академический", "Она стремилась к академической карьере."),
    ("hesitate", "Don't hesitate to ask.", "колебаться", "Не колеблись спросить."),
    ("lock up", "Please lock up the house this evening.", "запереть", "Пожалуйста, заприте дом сегодня вечером."),
    ("pierce", "The arrow will pierce the door.", "пробить", "Стрела пробьёт дверь."),
    ("similarity", "There is a similarity between them.", "сходство", "Между ними есть сходство."),
    ("startle", "The loud noise startled me.", "вздрогнуть", "Громкий шум заставил меня вздрогнуть."),
    ("inspection", "The car passed the inspection successfully.", "осмотр", "Автомобиль успешно прошёл осмотр."),
    ("cautious", "He is cautious crossing the street.", "осторожный", "Он осторожен, переходя улицу."),
    ("therapy", "She started therapy last month.", "терапия", "Она начала терапию в прошлом месяце."),
    ("ethnic", "They celebrated their ethnic heritage proudly.", "этнический", "Они гордо отмечали своё этническое наследие."),
    ("peephole", "She looked through the peephole.", "глазок", "Она посмотрела в глазок."),
    ("poster", "I bought a movie poster yesterday.", "плакат", "Я купил плакат к фильму вчера."),
    ("to be based", "The theory is based on facts.", "основываться", "Теория основывается на фактах."),
    ("outfit", "She admired her new outfit in the mirror.", "наряд", "Она любовалась своим новым нарядом в зеркале."),
    ("deceased", "The deceased was a respected individual.", "покойный", "Покойный был уважаемым человеком."),
    ("adore", "I absolutely adore this book.", "обожать", "Я абсолютно обожаю эту книгу."),
    ("bull", "The bull charged at me.", "бык", "Бык бросился на меня."),
    ("earnings", "His earnings were high last year.", "заработок", "Его заработок был высоким в прошлом году."),
    ("sympathy", "She felt sympathy for the newcomer.", "сочувствие", "Она чувствовала сочувствие к новичку."),
    ("primitive", "Their tools were quite primitive.", "примитивный", "Их инструменты были довольно примитивны."),
    ("breakthrough", "A scientific breakthrough changed everything.", "прорыв", "Научный прорыв изменил всё."),
    ("coefficient", "Calculate the coefficient.", "коэффициент", "Рассчитайте коэффициент."),
    ("maternal", "Her maternal instinct is strong.", "материнский", "Её материнский инстинкт сильный."),
    ("uprising", "The uprising was long.", "восстание", "Восстание было долгим."),
    ("Republican", "He supports the Republican party.", "республиканский", "Он поддерживает республиканскую партию."),
    ("moist", "The soil was moist.", "влажный", "Почва была влажной."),
    ("to come in handy", "This book will come in handy.", "пригодиться", "Эта книга пригодится."),
    ("to bury", "They want to bury him.", "похоронить", "Они хотят похоронить его."),
    ("loyalty", "His loyalty is strong.", "верность", "Его верность сильная."),
    ("regulatory", "The regulatory requirements are strict.", "нормативный", "Нормативные требования строгие."),
    ("convenience", "I like the store's convenience.", "удобство", "Мне нравится удобство магазина."),
    ("impulse", "He acted on impulse.", "импульс", "Он действовал по импульсу."),
    ("definitely", "She definitely won today.", "однозначно", "Она однозначно победила сегодня."),
    ("consciously", "She consciously chose this.", "сознательно", "Она сознательно выбрала это."),
    ("innocent", "The boy looks innocent.", "невинный", "Мальчик выглядит невинным."),
    ("repetition", "Repetition helps me.", "повторение", "Повторение мне помогает."),
    ("heritage", "We love our cultural heritage.", "наследие", "Мы любим наше культурное наследие."),
    ("Pole", "The Pole loves traditional food.", "поляк", "Поляк любит традиционную кухню."),
    ("burn down", "The house will burn down at night.", "сгореть", "Дом сгорит ночью."),
    ("to be limited", "His options are limited to this.", "ограничиваться", "Его варианты ограничиваются этим."),
    ("pyramid", "The pyramid is old and high.", "пирамида", "Пирамида старая и высокая."),
    ("scoundrel", "He is a scoundrel.", "сволочь", "Он сволочь."),
    ("to distinguish", "Learn to distinguish these facts.", "различать", "Научитесь различать эти факты."),
    ("Tatar", "The Tatar cooked traditional dishes.", "татарин", "Татарин готовил традиционные блюда."),
    ("to spend the night", "I decided to spend the night there.", "ночевать", "Я решил там ночевать."),
    ("to be placed", "The book is placed here.", "ставиться", "Книга ставится здесь."),
    ("frank", "He was frank about his feelings.", "откровенный", "Он был откровенен в своих чувствах."),
    ("swing", "I swing my son in the park.", "качать", "Я качаю сына в парке."),
    ("circulation", "The book's circulation is large.", "тираж", "Тираж книги большой."),
    ("killed", "He was killed in the accident.", "убитый", "Он был убит в аварии."),
    ("skull", "The skull protects the brain.", "череп", "Череп защищает мозг."),
    ("kettle", "There is water in the kettle.", "чайник", "В чайнике есть вода."),
    ("to be installed", "The software is installed today.", "устанавливаться", "Программа устанавливается сегодня."),
    ("impatience", "Her impatience was clearly visible.", "нетерпение", "Её нетерпение было явно видно."),
    ("lay", "She will lay the baby on the bed.", "уложить", "Она уложит младенца на кровать."),
    ("to envy", "She began to envy her friend's success.", "завидовать", "Она начала завидовать успеху своей подруги."),
    ("enthusiasm", "Her enthusiasm was truly strong.", "энтузиазм", "Её энтузиазм действительно был сильным."),
    ("interrogation", "The interrogation was long.", "допрос", "Допрос был долгим."),
    ("to generate", "The scandal generated new problems.", "породить", "Скандал породил новые проблемы."),
    ("deviation", "The deviation is large.", "отклонение", "Отклонение большое."),
    ("harvest", "The harvest was rich this year.", "урожай", "Урожай в этом году был богатым."),
    ("architect", "The architect built a new building.", "архитектор", "Архитектор построил новое здание."),
    ("distinguish", "Experts can distinguish these words easily.", "отличать", "Эксперты могут легко отличать эти слова."),
    ("bishop", "The bishop led the service.", "епископ", "Епископ провёл службу."),
    ("lay out", "She will lay out the cards.", "выложить", "Она выложит карты."),
    ("Turk", "The Turk visited Moscow last summer.", "турок", "Турок посетил Москву прошлым летом."),
    ("to drive up", "I will drive up to your house.", "подъехать", "Я подъеду к твоему дому."),
    ("assignment", "He received a new assignment today.", "поручение", "Он получил новое поручение сегодня."),
    ("bubble", "The soap made a bubble.", "пузырь", "Мыло сделало пузырь."),
    ("affectionate", "Her hug was affectionate.", "ласковый", "Её объятие было ласковым."),
    ("acceptable", "This price is perfectly acceptable.", "приемлемый", "Эта цена вполне приемлема."),
    ("to be friends", "They decided to be friends forever.", "дружить", "Они решили дружить навсегда."),
    ("deadly", "This snake is deadly.", "смертельный", "Эта змея смертельная."),
    ("extraordinary", "This is an extraordinary situation.", "чрезвычайный", "Это чрезвычайная ситуация."),
    ("housing", "This is a housing question.", "жилищный", "Это жилищный вопрос."),
    ("shit", "I stepped in dog shit.", "дерьмо", "Я наступил в собачье дерьмо."),
    ("tired", "I am really tired today.", "усталый", "Я сегодня действительно усталый."),
    ("dismiss", "They decided to dismiss the employee.", "уволить", "Они решили уволить сотрудника."),
    ("dwelling", "They found an ancient dwelling underground.", "жилище", "Они нашли древнее жилище под землей."),
    ("brush", "She held the brush.", "кисть", "Она держала кисть."),
    ("vegetable garden", "I work in the vegetable garden.", "огород", "Я работаю в огороде."),
    ("protective", "Wear protective gloves.", "защитный", "Наденьте защитные перчатки."),
    ("subscriber", "The subscriber missed the call.", "абонент", "Абонент пропустил звонок."),
    ("essay", "She published an essay.", "очерк", "Она опубликовала очерк."),
    ("to bend", "She will bend to take her shoe.", "наклониться", "Она наклонится, чтобы взять обувь."),
    ("equality", "We need equality.", "равенство", "Нам нужно равенство."),
    ("reconstruction", "The museum is under reconstruction.", "реконструкция", "Музей на реконструкции."),
    ("poison", "This is deadly poison.", "яд", "Это смертельный яд."),
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
    if word.endswith("d") and len(word) > 4:
        forms.add(word[:-1])
    return forms


def en_ok(text: str, extra: set[str] | None = None) -> list[str]:
    allowed = allow_en | (extra or set())
    bad = []
    for raw in re.findall(r"[A-Za-z']+", text):
        w = raw.lower().replace("'", "")
        if not w or w in allowed:
            continue
        if IRREGULAR.get(w, "") in allowed:
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


def ru_ok(text: str, extra: set[str] | None = None) -> list[str]:
    allowed = allow_ru | (extra or set())
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
        extra_en = {p.strip().lower() for p in re.split(r"[,;/]| to | ", en) if p.strip()}
        extra_ru = {ru.lower().replace("ё", "е")}
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
