#!/usr/bin/env python3
from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PACK = ROOT / "english_russian"
sys.path.insert(0, str(ROOT))

from brainscape.cards import card_write_payload, cards_from_path, cards_match

SRC = PACK / "_chunks" / "deck_15260283_01.csv"
OUT = PACK / "_chunks" / "fixed" / "deck_15260283_01.csv"
LOG = PACK / "_chunks" / "logs" / "deck_15260283_01.txt"

FUNCTION_EN = {
    "a", "an", "the", "is", "be", "i", "you", "he", "she", "it", "we", "they",
    "my", "and", "or", "in", "on", "at", "to", "of", "for", "with", "from",
    "not", "his", "him", "her", "their", "them", "our", "us", "me", "am",
    "are", "was", "were", "been", "being", "this", "that", "these", "those",
    "as", "by", "into", "about", "than", "then", "so", "if", "but", "its",
    "your", "do", "does", "did", "will", "would", "can", "could", "may",
    "there", "here", "has", "had", "have", "don't", "dont", "let's", "lets",
    "all", "off", "done", "myself", "yourself", "himself", "herself",
    "itself", "ourselves", "themselves", "one's", "ones",
}

FUNCTION_RU = {
    "и", "а", "или", "не", "ни", "но", "да", "же", "ли", "бы", "то", "это",
    "этот", "эта", "эти", "этой", "этом", "эту", "этих", "этим", "этими",
    "этого", "этому", "я", "ты", "он", "она", "оно", "мы", "вы", "они",
    "мой", "моя", "мое", "мои", "моего", "моей", "моем", "моим", "мою",
    "твой", "твоя", "твое", "твои", "твою", "твоей", "ваш", "наш", "наша",
    "наше", "наши", "его", "ее", "их", "ему", "ей", "им", "ими", "меня",
    "мне", "тебя", "тебе", "нас", "нам", "вас", "вам", "себя", "себе",
    "собой", "свой", "своя", "свое", "свои", "свою", "своей", "своего",
    "своим", "в", "во", "на", "с", "со", "к", "ко", "у", "о", "об", "от",
    "до", "из", "за", "по", "под", "над", "при", "для", "без", "между",
    "через", "был", "была", "было", "были", "будет", "будут", "буду",
    "есть", "быть", "уже", "еще", "также", "тоже", "только", "вот", "ведь",
    "ну", "все", "всех", "всего", "всем", "здесь", "тут", "там", "давай",
    "как", "что", "чтобы", "когда", "если", "где", "чем", "кто",
    "них", "него", "нее", "ней", "ним",
}

allow_en = {
    line.strip().lower()
    for line in (PACK / "_vocab" / "allow_en_15260283.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_ru = {
    line.strip().replace("ё", "е").lower()
    for line in (PACK / "_vocab" / "allow_ru_15260283.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_en |= FUNCTION_EN
allow_ru |= FUNCTION_RU

# Lemma corrections taught on this card.
allow_ru |= {"незаметный", "каменистый", "бродяга"}

# (en_lemma, en_ex, ru_lemma, ru_ex)
FIXED = [
    ("rapist", "The rapist is in prison.", "насильник", "Насильник в тюрьме."),
    ("vulgarity", "I hate this vulgarity.", "пошлость", "Я ненавижу эту пошлость."),
    ("gym", "I go to the gym.", "спортзал", "Я хожу в спортзал."),
    ("destroyer", "The destroyer is at sea.", "эсминец", "Эсминец в море."),
    ("arterial", "Arterial blood is red.", "артериальный", "Артериальная кровь красная."),
    ("to be bought", "These books are to be bought.", "покупаться", "Эти книги покупаются."),
    ("to be lucky", "I was lucky yesterday.", "посчастливиться", "Мне посчастливилось вчера."),
    ("handcuff", "Put the handcuff on him.", "наручник", "Наденьте на него наручник."),
    ("horned", "The horned animal is large.", "рогатый", "Рогатое животное большое."),
    ("boiler room", "The boiler room is hot.", "котельная", "Котельная горячая."),
    ("sewing", "This is sewing work.", "швейный", "Это швейная работа."),
    ("bequeath", "He will bequeath the house to his son.", "завещать", "Он завещает дом сыну."),
    ("urinary", "This is a urinary pain.", "мочевой", "Это мочевая боль."),
    ("pea", "I eat pea soup.", "горох", "Я ем суп с горохом."),
    ("unshaven", "He looks unshaven.", "небритый", "Он выглядит небритым."),
    ("gendarme", "The gendarme is here.", "жандарм", "Жандарм здесь."),
    ("donor", "He is a blood donor.", "донор", "Он донор крови."),
    ("Irishman", "The Irishman lives here.", "ирландец", "Ирландец живет здесь."),
    ("optimize", "We must optimize the work.", "оптимизировать", "Мы должны оптимизировать работу."),
    ("twig", "A bird sat on the twig.", "веточка", "Птица сидела на веточке."),
    ("climatic", "Climatic change is slow.", "климатический", "Климатическое изменение медленное."),
    ("perish", "Many soldiers will perish.", "сгинуть", "Многие солдаты сгинут."),
    ("gardener", "The gardener works in the garden.", "садовник", "Садовник работает в саду."),
    ("designing", "Designing takes time.", "конструирование", "Конструирование занимает время."),
    ("convex", "The glass is convex.", "выпуклый", "Стекло выпуклое."),
    ("caustic", "The caustic smoke is bad.", "едкий", "Едкий дым плохой."),
    ("flaw", "I see a flaw here.", "изъян", "Я вижу изъян здесь."),
    ("hertz", "The sound is one hundred hertz.", "герц", "Звук — сто герц."),
    ("solitude", "I need solitude.", "уединение", "Мне нужно уединение."),
    ("to camouflage", "They will camouflage the car.", "замаскировать", "Они замаскируют машину."),
    ("whiteness", "I like the whiteness of the snow.", "белизна", "Мне нравится белизна снега."),
    ("stationery", "I need stationery paper.", "канцелярский", "Мне нужна канцелярская бумага."),
    ("self-determination", "I want self-determination.", "самоопределение", "Я хочу самоопределение."),
    ("soak", "Don't soak the bread.", "мочить", "Не мочи хлеб."),
    ("to fasten", "Please fasten your coat.", "застегнуть", "Пожалуйста, застегните пальто."),
    ("small in number", "Our group is small in number.", "малочисленный", "Наша группа малочисленна."),
    ("bounce off", "The stone will bounce off the wall.", "отскочить", "Камень отскочит от стены."),
    ("pre-death", "This is his pre-death letter.", "предсмертный", "Это его предсмертное письмо."),
    ("mandate", "He received a mandate.", "мандат", "Он получил мандат."),
    ("in a flash", "He left in a flash.", "мигом", "Он мигом ушел."),
    ("slender", "He is a slender man.", "худощавый", "Он худощавый человек."),
    ("to burst out laughing", "She burst out laughing.", "захохотать", "Она захохотала."),
    ("metallurgical", "He works at a metallurgical plant.", "металлургический", "Он работает на металлургическом заводе."),
    ("recreate", "They will recreate the old house.", "воссоздать", "Они воссоздадут старый дом."),
    ("lilac", "She has a lilac dress.", "лиловый", "У неё лиловое платье."),
    ("epic", "This book is an epic.", "эпопея", "Эта книга — эпопея."),
    ("mourning", "She wore a mourning dress.", "траурный", "Она надела траурное платье."),
    ("stamping", "I heard the stamping.", "топот", "Я слышал топот."),
    ("to tire", "This work will tire me.", "утомить", "Эта работа утомит меня."),
    ("toolkit", "I need a new toolkit.", "инструментарий", "Мне нужен новый инструментарий."),
    ("to slide down", "The snow will slide down the roof.", "сползать", "Снег будет сползать с крыши."),
    ("chivalrous", "He is a chivalrous man.", "рыцарский", "Он рыцарский человек."),
    ("mane", "The horse has a big mane.", "грива", "У лошади большая грива."),
    ("biographical", "This is a biographical book.", "биографический", "Это биографическая книга."),
    ("expire", "The time will expire tomorrow.", "истечь", "Время истечет завтра."),
    ("unremarkable", "His work is unremarkable.", "незаметный", "Его работа незаметна."),
    ("small suitcase", "She took a small suitcase.", "чемоданчик", "Она взяла чемоданчик."),
    ("tape measure", "I lost my tape measure.", "рулетка", "Я потерял свою рулетку."),
    ("nineteenth", "This is the nineteenth day.", "девятнадцатый", "Это девятнадцатый день."),
    ("rink", "The rink is large.", "каток", "Каток большой."),
    ("shootout", "The shootout was short.", "перестрелка", "Перестрелка была короткой."),
    ("adverb", '"Quickly" is an adverb.', "наречие", "«Быстро» — это наречие."),
    ("crumpled", "This paper is crumpled.", "мятый", "Этот лист мятый."),
    ("to serve (time)", "He must serve time.", "отбывать", "Он должен отбывать срок."),
    ("relentless", "He is a relentless man.", "неумолимый", "Он неумолимый человек."),
    ("coachman", "The coachman waited.", "кучер", "Кучер ждал."),
    ("cloth", "She bought red cloth.", "сукно", "Она купила красное сукно."),
    ("irreversible", "This change is irreversible.", "необратимый", "Это изменение необратимо."),
    ("above-mentioned", "Read the above-mentioned letter.", "вышеуказанный", "Читайте вышеуказанное письмо."),
    ("cane", "He walks with a cane.", "трость", "Он ходит с тростью."),
    ("seminary", "He is at the seminary.", "семинария", "Он в семинарии."),
    ("intangible", "This is an intangible thing.", "нематериальный", "Это нематериальная вещь."),
    ("little book", "I read this little book.", "книжечка", "Я читал эту книжечку."),
    ("to set out", "They set out in the morning.", "пускаться", "Они пускаются в путь утром."),
    ("forester", "The forester lives in the forest.", "лесник", "Лесник живет в лесу."),
    ("basketball", "I play basketball.", "баскетбол", "Я играю в баскетбол."),
    ("curly", "She has curly hair.", "кудрявый", "У неё кудрявые волосы."),
    ("insulator", "Glass is an insulator.", "изолятор", "Стекло — изолятор."),
    ("to throw out", "I throw out old paper.", "выкидывать", "Я выкидываю старую бумагу."),
    ("lion's", "He has a lion's heart.", "львиный", "У него львиное сердце."),
    ("rocky", "The road is rocky.", "каменистый", "Дорога каменистая."),
    ("to be dedicated", "This book is dedicated to her.", "посвящаться", "Эта книга посвящается ей."),
    ("vagrant", "A vagrant sat by the house.", "бродяга", "Бродяга сидел у дома."),
    ("velvet", "Her dress is of velvet.", "бархат", "Её платье из бархата."),
    ("alms", "She gave alms to the poor.", "милостыня", "Она дала милостыню бедным."),
    ("amen", "We said amen.", "аминь", "Мы сказали аминь."),
    ("knowing", "He had a knowing smile.", "знающий", "У него была знающая улыбка."),
    ("pester", "Don't pester me.", "теребить", "Не тереби меня."),
    ("milestone", "This year is a milestone.", "веха", "Этот год — веха."),
    ("substitution", "I saw the substitution.", "подмена", "Я видел подмену."),
    ("lightly", "She opened the door lightly.", "легонько", "Она легонько открыла дверь."),
    ("masonry", "The masonry is old.", "кладка", "Кладка старая."),
    ("to flutter", "The flag will flutter in the wind.", "развеваться", "Флаг будет развеваться на ветру."),
    ("evoke", "This song will evoke the night.", "навеять", "Эта песня навеет ночь."),
    ("secondarily", "Art is secondarily important.", "вторично", "Искусство вторично важно."),
    ("investigate", "They will investigate the case.", "расследовать", "Они будут расследовать дело."),
    ("picnic", "We will go to a picnic.", "пикник", "Мы пойдем на пикник."),
    ("Caspian", "The Caspian Sea is large.", "каспийский", "Каспийское море большое."),
    ("mercury", "Mercury is a metal.", "ртуть", "Ртуть — металл."),
    ("to endow", "They endow him with power.", "наделять", "Они наделяют его силой."),
]


IRREGULAR_EN = {
    "made": "make",
    "met": "meet",
    "saw": "see",
    "got": "get",
    "gave": "give",
    "took": "take",
    "came": "come",
    "went": "go",
    "ate": "eat",
    "spoke": "speak",
    "broke": "break",
    "felt": "feel",
    "wrote": "write",
    "built": "build",
    "sat": "sit",
    "began": "begin",
    "became": "become",
    "bought": "buy",
    "caught": "catch",
    "kept": "keep",
    "left": "leave",
    "shown": "show",
    "showed": "show",
    "stopped": "stop",
    "heard": "hear",
    "wore": "wear",
    "lost": "lose",
    "gave": "give",
    "said": "say",
    "read": "read",
    "put": "put",
}


def _en_ok(word: str) -> bool:
    w = word.lower()
    if w in allow_en:
        return True
    if IRREGULAR_EN.get(w) in allow_en:
        return True
    if "-" in w and all(_en_ok(p) for p in w.split("-") if p):
        return True
    for suf in ("'s", "s", "es", "ed", "ing", "ly", "er", "est"):
        if w.endswith(suf) and w[: -len(suf)] in allow_en:
            return True
        if w.endswith(suf) and w[: -len(suf)] + "e" in allow_en:
            return True
    if w.endswith("ies") and (w[:-3] + "y") in allow_en:
        return True
    if w.endswith("ied") and (w[:-3] + "y") in allow_en:
        return True
    return False


RU_ENDINGS = (
    "ами", "ями", "ого", "его", "ому", "ему", "ыми", "ими", "ой", "ей", "ом",
    "ем", "ах", "ях", "ам", "ям", "ов", "ев", "ей", "ую", "юю", "ая", "яя",
    "ое", "ее", "ые", "ие", "ый", "ий", "ой", "а", "я", "у", "ю", "е", "и",
    "ы", "о", "ь",
)


def _ru_stems(word: str) -> set[str]:
    w = word.replace("ё", "е").lower()
    out = {w}
    for n in range(3, min(6, len(w) + 1)):
        out.add(w[:n])
    for suf in RU_ENDINGS:
        if w.endswith(suf) and len(w) - len(suf) >= 3:
            out.add(w[: -len(suf)])
    return out


IRREGULAR_RU = {
    "может": "мочь",
    "могу": "мочь",
    "можем": "мочь",
    "хочу": "хотеть",
    "хочет": "хотеть",
    "хотим": "хотеть",
    "вижу": "видеть",
    "видишь": "видеть",
    "видит": "видеть",
    "знаю": "знать",
    "живу": "жить",
    "живем": "жить",
    "живет": "жить",
    "нашел": "найти",
    "нашла": "найти",
    "будь": "быть",
    "стал": "стать",
    "стала": "стать",
    "стали": "стать",
    "пишет": "писать",
    "увидел": "видеть",
    "услышал": "слышать",
    "слышу": "слышать",
    "ем": "есть",
    "ест": "есть",
    "идет": "идти",
    "пойдем": "пойти",
    "ушел": "уйти",
    "дал": "дать",
    "дала": "дать",
    "взял": "взять",
    "взяла": "взять",
    "ждал": "ждать",
    "купила": "купить",
    "надела": "надеть",
    "слышал": "слышать",
    "видел": "видеть",
    "сказал": "сказать",
    "сказали": "сказать",
    "читал": "читать",
    "читайте": "читать",
    "открой": "открыть",
    "открыла": "открыть",
    "работает": "работать",
    "хожу": "ходить",
    "ходит": "ходить",
    "играю": "играть",
    "нужно": "нужно",
    "нужен": "нужный",
    "нужна": "нужный",
    "должен": "должен",
}


def _ru_ok(word: str) -> bool:
    w = word.replace("ё", "е").lower()
    if w in allow_ru:
        return True
    mapped = IRREGULAR_RU.get(w)
    if mapped and mapped in allow_ru:
        return True
    stems = _ru_stems(w)
    for lemma in allow_ru:
        if len(lemma) < 3:
            continue
        if stems & _ru_stems(lemma):
            return True
        stem = lemma[:4] if len(lemma) >= 4 else lemma
        if w.startswith(stem) or lemma.startswith(w[:4] if len(w) >= 4 else w):
            return True
    return False


def make_card(en_lemma: str, en_ex: str, ru_lemma: str, ru_ex: str) -> dict:
    return card_write_payload(
        {
            "qMdPrompt": "Translate:",
            "qMdBody": en_lemma,
            "qMdClarifier": "",
            "qMdFootnote": en_ex,
            "aMdPrompt": "",
            "aMdBody": ru_lemma,
            "aMdClarifier": "",
            "aMdFootnote": ru_ex,
        }
    )


def target_in_example(lemma: str, example: str) -> bool:
    text = example.replace("ё", "е").lower()
    parts = [p.strip() for p in re.split(r"\s+", lemma.replace("ё", "е").lower()) if p.strip()]
    keys = [p for p in parts if p not in {"to", "be", "the", "a", "an"}] or parts
    for key in keys:
        key = key.strip("()")
        stem = key[:4] if len(key) >= 4 else key
        if stem and stem in text.replace(" ", ""):
            return True
        if key in text:
            return True
    return False


def write_csv(path: Path, cards: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh, lineterminator="\n")
        writer.writerow(["Question", "Answer"])
        for card in cards:
            payload = card_write_payload(card)
            writer.writerow([payload["question"], payload["answer"]])


def main() -> None:
    orig = cards_from_path(SRC)
    if len(orig) != 100:
        raise SystemExit(f"expected 100 source cards, got {len(orig)}")
    if len(FIXED) != 100:
        raise SystemExit(f"expected 100 fixed rows, got {len(FIXED)}")

    cards = []
    changed = 0
    leftover: list[str] = []
    missing_target: list[str] = []
    for i, ((en_lemma, en_ex, ru_lemma, ru_ex), old) in enumerate(zip(FIXED, orig), start=1):
        if old.get("qMdBody") != en_lemma:
            raise SystemExit(f"order mismatch at {i}: {old.get('qMdBody')!r} vs {en_lemma!r}")
        card = make_card(en_lemma, en_ex, ru_lemma, ru_ex)
        cards.append(card)
        if not cards_match(old, card):
            changed += 1
        lemma_bits = set(re.findall(r"[A-Za-z']+", en_lemma.lower()))
        for tok in re.findall(r"[A-Za-z']+", en_ex):
            if tok.lower() in lemma_bits:
                continue
            if not _en_ok(tok):
                leftover.append(f"{i} EN {tok} :: {en_ex}")
        ru_bits = set(re.findall(r"[А-Яа-яЁё]+", ru_lemma.lower().replace("ё", "е")))
        for tok in re.findall(r"[А-Яа-яЁё]+", ru_ex):
            if tok.replace("ё", "е").lower() in ru_bits:
                continue
            if not _ru_ok(tok):
                leftover.append(f"{i} RU {tok} :: {ru_ex}")
        if not target_in_example(en_lemma, en_ex):
            missing_target.append(f"{i} EN {en_lemma} :: {en_ex}")
        if not target_in_example(ru_lemma, ru_ex):
            missing_target.append(f"{i} RU {ru_lemma} :: {ru_ex}")

    write_csv(OUT, cards)
    got = cards_from_path(OUT)
    if len(got) != 100:
        raise SystemExit(f"cards_from_path returned {len(got)}")
    LOG.parent.mkdir(parents=True, exist_ok=True)
    LOG.write_text(f"{changed}\n", encoding="utf-8")
    print(f"wrote {OUT}")
    print(f"cards_from_path={len(got)} changed={changed}")
    if leftover:
        print("LEFTOVER:")
        print("\n".join(leftover))
    if missing_target:
        print("MISSING TARGET:")
        print("\n".join(missing_target))


if __name__ == "__main__":
    main()
