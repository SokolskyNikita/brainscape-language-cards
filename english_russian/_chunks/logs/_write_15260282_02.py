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

SRC = PACK / "_chunks" / "deck_15260282_02.csv"
OUT = PACK / "_chunks" / "fixed" / "deck_15260282_02.csv"
LOG = PACK / "_chunks" / "logs" / "deck_15260282_02.txt"

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
    for line in (PACK / "_vocab" / "allow_en_15260282.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_ru = {
    line.strip().replace("ё", "е").lower()
    for line in (PACK / "_vocab" / "allow_ru_15260282.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_en |= FUNCTION_EN
allow_ru |= FUNCTION_RU

# New lemmas introduced by corrections (taught on this card).
allow_ru |= {"саратов", "оппортунист"}

# (en_lemma, en_ex, ru_lemma, ru_ex)
FIXED = [
    ("generalize", "Don't generalize from one example.", "обобщать", "Не обобщай по одному примеру."),
    ("to listen intently", "She stopped to listen intently.", "вслушиваться", "Она остановилась, чтобы вслушаться."),
    ("to populate", "Birds populate this island.", "населять", "Птицы населяют этот остров."),
    ("numbness", "He felt numbness after the news.", "оцепенение", "Он чувствовал оцепенение после новости."),
    ("disposable", "Disposable plates are convenient.", "одноразовый", "Одноразовые тарелки удобны."),
    ("fierce", "This man is fierce.", "лютый", "Этот человек лютый."),
    ("set oneself", "She set herself a new goal.", "задаться", "Она задалась новой целью."),
    ("talentless", "He is a talentless writer.", "бездарный", "Он бездарный писатель."),
    ("hitherto", "Hitherto I did not know this.", "доселе", "Доселе я этого не знал."),
    ("graze", "The boy will graze the cows.", "пасти", "Мальчик будет пасти коров."),
    ("garlic", "I added garlic to the soup.", "чеснок", "Я добавил чеснок в суп."),
    ("check mark", "Put a check mark next to the answer.", "галочка", "Поставьте галочку рядом с ответом."),
    ("makeup", "She put on makeup.", "макияж", "Она наложила макияж."),
    ("cumbersome", "This box is too cumbersome.", "громоздкий", "Этот ящик слишком громоздкий."),
    ("to subordinate", "They want to subordinate this land.", "подчинять", "Они хотят подчинить эту землю."),
    ("cultivation", "The cultivation of wheat is hard.", "выращивание", "Выращивание пшеницы трудно."),
    ("grandma", "I love my grandma.", "бабуля", "Я люблю свою бабулю."),
    ("collector", "He is a book collector.", "коллекционер", "Он коллекционер книг."),
    ("peck", "The chicken pecked the land.", "клевать", "Курица клевала землю."),
    ("chronology", "I know the chronology of events.", "хронология", "Я знаю хронологию событий."),
    ("least", "She is the least ready.", "наименее", "Она наименее готова."),
    ("preferable", "Silence is preferable to noise.", "предпочтительный", "Тишина предпочтительнее шума."),
    ("cradle", "The baby is in the cradle.", "колыбель", "Малыш в колыбели."),
    ("systematically", "She systematically checks her work.", "систематически", "Она систематически проверяет свою работу."),
    ("powerfully", "He lifted the box powerfully.", "мощно", "Он мощно поднял ящик."),
    ("parquet", "The room has parquet.", "паркет", "В комнате лежит паркет."),
    ("seasonal", "Seasonal food is good.", "сезонный", "Сезонная еда хорошая."),
    ("outpost", "There is an outpost on the border.", "застава", "На границе стоит застава."),
    ("Saratov", "I live in Saratov.", "Саратов", "Я живу в Саратове."),
    ("theologian", "The theologian writes a book.", "богослов", "Богослов пишет книгу."),
    ("tumble out", "The coins tumble out of the bag.", "вывалиться", "Монеты вывалились из сумки."),
    ("retribution", "He waited for retribution.", "возмездие", "Он ждал возмездия."),
    ("passing", "I caught a passing car.", "попутный", "Я поймал попутную машину."),
    ("casket", "She kept rings in a casket.", "шкатулка", "Она хранила кольца в шкатулке."),
    ("prevalence", "The prevalence of this idea is clear.", "преобладание", "Преобладание этой идеи ясно."),
    ("barbershop", "I went to the barbershop yesterday.", "парикмахерская", "Я ходил в парикмахерскую вчера."),
    ("exhaustion", "She felt complete exhaustion.", "истощение", "Она чувствовала полное истощение."),
    ("co-author", "She became my co-author.", "соавтор", "Она стала моим соавтором."),
    ("lifelong", "He received a lifelong sentence.", "пожизненный", "Он получил пожизненный срок."),
    ("waft", "The wind will waft from the sea.", "веять", "Ветер будет веять с моря."),
    ("mylord", "Yes, mylord, I hear you.", "милорд", "Да, милорд, я слышу вас."),
    ("clone", "They made a clone of the dog.", "клон", "Они сделали клон собаки."),
    ("Saudi", "Saudi banks are rich.", "саудовский", "Саудовские банки богатые."),
    ("shy", "She is too shy to speak.", "застенчивый", "Она слишком застенчивая, чтобы говорить."),
    ("cardinally", "He cardinally changes his life.", "кардинально", "Он кардинально изменяет свою жизнь."),
    ("to entrust", "I will entrust this work to him.", "поручать", "Я поручу ему эту работу."),
    ("Messiah", "They waited for the Messiah.", "мессия", "Они ждали мессию."),
    ("blurt out", "He will blurt out the secret.", "выпалить", "Он выпалит секрет."),
    ("colorless", "The water is colorless.", "бесцветный", "Вода бесцветная."),
    ("tender", "They got the tender.", "тендер", "Они получили тендер."),
    ("small patch", "There is a small patch of grass here.", "пятачок", "Здесь есть маленький пятачок травы."),
    ("to be studied", "This question is still being studied.", "изучаться", "Этот вопрос ещё изучается."),
    ("chronicler", "The chronicler wrote about the war.", "летописец", "Летописец писал о войне."),
    ("to be deposited", "Salt began to be deposited on the walls.", "откладываться", "Соль начала откладываться на стенах."),
    ("opportunist", "He is a real opportunist.", "оппортунист", "Он настоящий оппортунист."),
    ("angle", "I like this angle.", "ракурс", "Мне нравится этот ракурс."),
    ("immovable", "The stone was immovable.", "недвижимый", "Камень был недвижим."),
    ("populate", "They populated the new land.", "населить", "Они населили новую землю."),
    ("honey", "I like honey cake.", "медовый", "Я люблю медовый торт."),
    ("to baptize", "They will baptize him.", "крестить", "Они будут крестить его."),
    ("martial", "His speech was martial.", "воинственный", "Его речь была воинственной."),
    ("sing through", "She will sing through the song.", "пропеть", "Она пропоёт песню."),
    ("surgery", "He studies surgery.", "хирургия", "Он изучает хирургию."),
    ("tempting", "The offer was tempting.", "заманчивый", "Предложение было заманчивым."),
    ("borrowing", "Borrowing words is normal.", "заимствование", "Заимствование слов нормально."),
    ("dinosaur", "The boy saw a dinosaur.", "динозавр", "Мальчик увидел динозавра."),
    ("firearm", "He has a firearm.", "огнестрельный", "У него есть огнестрельное оружие."),
    ("lifting", "Lifting the box was hard.", "поднятие", "Поднятие ящика было трудным."),
    ("Old Russian", "He reads Old Russian texts.", "древнерусский", "Он читает древнерусские тексты."),
    ("helplessness", "She felt helplessness.", "беспомощность", "Она чувствовала беспомощность."),
    ("couch", "She sat on the couch.", "кушетка", "Она сидела на кушетке."),
    ("foreign policy", "This is a foreign policy question.", "внешнеполитический", "Это внешнеполитический вопрос."),
    ("to be attached", "The papers are to be attached.", "прилагаться", "Бумаги должны прилагаться."),
    ("sense", "I sense trouble.", "предчувствовать", "Я предчувствую беду."),
    ("ornament", "The vase has an ornament.", "орнамент", "На вазе есть орнамент."),
    ("lessee", "The lessee pays every month.", "арендатор", "Арендатор платит каждый месяц."),
    ("to pamper", "She likes to pamper her dog.", "баловать", "Она любит баловать свою собаку."),
    ("middle-aged", "He is a middle-aged man.", "немолодой", "Он немолодой мужчина."),
    ("standing", "A standing man waited at the door.", "стоящий", "У двери ждал стоящий мужчина."),
    ("rosy", "Her cheeks were rosy.", "румяный", "Её щёки были румяными."),
    ("liturgy", "The priest began the liturgy.", "литургия", "Священник начал литургию."),
    ("cabman", "The cabman waited by the house.", "извозчик", "Извозчик ждал у дома."),
    ("lick", "The dog will lick its paws.", "лизать", "Собака будет лизать свои лапы."),
    ("Judaism", "Judaism is an old religion.", "иудаизм", "Иудаизм — старая религия."),
    ("convocation", "The convocation is on Monday.", "созыв", "Созыв в понедельник."),
    ("valor", "He showed valor in the war.", "доблесть", "Он показал доблесть на войне."),
    ("to get attached", "I got attached to this dog.", "привязаться", "Я привязался к этой собаке."),
    ("authorship", "She proved her authorship.", "авторство", "Она доказала своё авторство."),
    ("dancer", "He is a good dancer.", "танцор", "Он хороший танцор."),
    ("toad", "A toad sat by the water.", "жаба", "Жаба сидела у воды."),
    ("operative", "The operative found the man.", "оперативник", "Оперативник нашёл этого человека."),
    ("dummy", "Do not be a dummy.", "болван", "Не будь болваном."),
    ("loom", "Clouds loom in the sky.", "маячить", "В небе маячат облака."),
    ("warily", "She warily opened the door.", "настороженно", "Она настороженно открыла дверь."),
    ("wash one's face", "I want to wash my face.", "умыться", "Я хочу умыться."),
    ("aura", "Her aura is here.", "аура", "Её аура здесь."),
    ("lubricant", "There is lubricant on the door.", "смазка", "На двери есть смазка."),
    ("industrialist", "The industrialist built a factory.", "промышленник", "Промышленник построил завод."),
    ("press down", "Press down on the lid.", "придавить", "Придавите крышку."),
    ("potion", "She made a potion.", "зелье", "Она сделала зелье."),
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
