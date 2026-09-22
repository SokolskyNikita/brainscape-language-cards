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

SRC = PACK / "_chunks" / "deck_15260281_04.csv"
OUT = PACK / "_chunks" / "fixed" / "deck_15260281_04.csv"
LOG = PACK / "_chunks" / "logs" / "deck_15260281_04.txt"

FUNCTION_EN = {
    "a", "an", "the", "is", "be", "i", "you", "he", "she", "it", "we", "they",
    "my", "and", "or", "in", "on", "at", "to", "of", "for", "with", "from",
    "not", "his", "him", "her", "their", "them", "our", "us", "me", "am",
    "are", "was", "were", "been", "being", "this", "that", "these", "those",
    "as", "by", "into", "about", "than", "then", "so", "if", "but", "its",
    "your", "do", "does", "did", "will", "would", "can", "could", "may",
    "there", "here", "has", "had", "have", "don't", "dont", "let's", "lets",
    "all", "off", "done",
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
    for line in (PACK / "_vocab" / "allow_en_15260281.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_ru = {
    line.strip().replace("ё", "е").lower()
    for line in (PACK / "_vocab" / "allow_ru_15260281.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_en |= FUNCTION_EN
allow_ru |= FUNCTION_RU

# New lemmas introduced by corrections (taught on this card).
allow_ru |= {"орел", "омск", "впитать"}

# (en_lemma, en_ex, ru_lemma, ru_ex)
FIXED = [
    ("coupon", "I redeemed a coupon for bread.", "талон", "Я обменял талон на хлеб."),
    ("exhalation", "His exhalation is warm.", "выдох", "Его выдох тёплый."),
    ("to spare", "He does not spare his enemy.", "щадить", "Он не щадит своего врага."),
    ("bust", "She admired the marble bust in the museum.", "бюст", "Она восхищалась мраморным бюстом в музее."),
    ("resin", "There is sticky resin on the tree.", "смола", "На дереве есть липкая смола."),
    ("porthole", "I looked through the porthole.", "иллюминатор", "Я смотрел в иллюминатор."),
    ("inadequacy", "She has a deep inadequacy.", "неполноценность", "У неё глубокая неполноценность."),
    ("sheriff", "The sheriff arrested the fugitive yesterday.", "шериф", "Шериф арестовал беглеца вчера."),
    ("carrot", "I planted a carrot in the garden.", "морковь", "Я посадил морковь в саду."),
    ("confluence", "A confluence of events led to chaos.", "стечение", "Стечение событий привело к хаосу."),
    ("trial", "This is a trial version.", "пробный", "Это пробная версия."),
    ("summit", "Leaders discussed peace at the summit.", "саммит", "Лидеры обсудили мир на саммите."),
    ("demanding", "He is a demanding teacher.", "требовательный", "Он требовательный учитель."),
    ("to be traced", "This pattern can be traced in history.", "прослеживаться", "Этот узор прослеживается в истории."),
    ("arithmetic", "I love arithmetic.", "арифметика", "Я люблю арифметику."),
    ("ventilation", "This room has ventilation.", "вентиляция", "В этой комнате есть вентиляция."),
    ("borscht", "I made borscht for dinner.", "борщ", "Я приготовил борщ на ужин."),
    ("to be brought up", "She was brought up in this house.", "воспитываться", "Она воспитывалась в этом доме."),
    ("legally", "She's legally his wife now.", "юридически", "Она теперь юридически его жена."),
    ("little voice", "I hear her little voice.", "голосок", "Я слышу её голосок."),
    ("mournful", "Her eyes were deep and mournful.", "скорбный", "Её глаза были глубокими и скорбными."),
    ("rivalry", "The rivalry between them intensified.", "соперничество", "Соперничество между ними обострилось."),
    ("trusted", "He was a trusted advisor.", "доверенный", "Он был доверенным советником."),
    ("barber", "The barber cut his hair.", "парикмахер", "Парикмахер срезал ему волосы."),
    ("librarian", "The librarian recommended a novel.", "библиотекарь", "Библиотекарь порекомендовал роман."),
    ("boundless", "The sea is boundless.", "бескрайний", "Море бескрайнее."),
    ("one hundred percent", "This is a one hundred percent result.", "стопроцентный", "Это стопроцентный результат."),
    ("witchcraft", "She studied witchcraft for many years.", "колдовство", "Она изучала колдовство много лет."),
    ("inexperienced", "He is an inexperienced teacher.", "неопытный", "Он неопытный учитель."),
    ("weekly", "This is a weekly magazine.", "еженедельный", "Это еженедельный журнал."),
    ("sweaty", "He is sweaty after the run.", "потный", "Он потный после бега."),
    ("simplification", "This is a useful simplification.", "упрощение", "Это полезное упрощение."),
    ("everyday use", "This word is in everyday use.", "обиход", "Это слово в обиходе."),
    ("to climb in", "He struggled to climb in the window.", "влезать", "Он с трудом пытался влезть в окно."),
    ("caringly", "She caringly holds the baby.", "заботливо", "Она заботливо держит младенца."),
    ("blooming", "I see a blooming garden.", "цветущий", "Я вижу цветущий сад."),
    ("presiding", "He is presiding today.", "председательствующий", "Он председательствующий сегодня."),
    ("heterogeneous", "The team was quite heterogeneous.", "разнородный", "Команда была довольно разнородной."),
    ("military enlistment office", "He visited the military enlistment office.", "военкомат", "Он посетил военкомат."),
    ("to lubricate", "I need to lubricate the door.", "смазать", "Мне нужно смазать дверь."),
    ("unprofitable", "This work is unprofitable.", "невыгодный", "Эта работа невыгодная."),
    ("unsuitable", "This dress is unsuitable.", "неподходящий", "Это платье неподходящее."),
    ("to erect", "They plan to erect a new monument.", "воздвигнуть", "Они планируют воздвигнуть новый памятник."),
    ("to stuff", "She loves to stuff the pillows.", "набивать", "Она любит набивать подушки."),
    ("fence off", "They decided to fence off the garden.", "оградить", "Они решили оградить сад."),
    ("diocese", "He works in the Moscow diocese.", "епархия", "Он работает в Московской епархии."),
    ("expulsion", "His expulsion from university was unexpected.", "отчисление", "Его отчисление из университета было неожиданным."),
    ("chariot", "The chariot is on the field.", "колесница", "Колесница на поле."),
    ("suburban", "They live in a quiet suburban house.", "пригородный", "Они живут в тихом пригородном доме."),
    ("semester", "The semester ends in December.", "семестр", "Семестр заканчивается в декабре."),
    ("bunny", "The bunny is in the field.", "зайчик", "Зайчик в поле."),
    ("announcer", "The announcer introduced the next song.", "диктор", "Диктор представил следующую песню."),
    ("ethnicity", "Her ethnicity is important to her.", "народность", "Её народность важна для неё."),
    ("coursework", "I finished my coursework yesterday.", "курсовой", "Я закончил свою курсовую вчера."),
    ("calorie", "I am counting every calorie today.", "калория", "Я считаю каждую калорию сегодня."),
    ("trophy", "He displayed his trophy proudly.", "трофей", "Он гордо показывал свой трофей."),
    ("exposure", "His exposure shocked the community.", "разоблачение", "Его разоблачение потрясло общество."),
    ("smart aleck", "Don't be a smart aleck, please.", "умник", "Пожалуйста, не будь умником."),
    ("interethnic", "This is an interethnic conflict.", "межнациональный", "Это межнациональный конфликт."),
    ("demarcation", "The river served as a natural demarcation.", "разграничение", "Река служила естественным разграничением."),
    ("to absorb", "The sponge will absorb the water.", "впитать", "Губка впитает воду."),
    ("glare", "I see a glare on the water.", "блик", "Я вижу блик на воде."),
    ("heavily", "He sighed heavily.", "тяжко", "Он тяжко вздохнул."),
    ("flora", "The island's flora is truly unique.", "флора", "Флора острова действительно уникальна."),
    ("Romanian", "She speaks Romanian.", "румынский", "Она говорит на румынском."),
    ("screenwriter", "He is a screenwriter.", "сценарист", "Он сценарист."),
    ("Cossackdom", "Cossackdom has old traditions.", "казачество", "У казачества есть старые традиции."),
    ("cornice", "The cornice is on the building.", "карниз", "Карниз на здании."),
    ("continental", "They have a continental breakfast.", "континентальный", "У них континентальный завтрак."),
    ("desolate", "The town is desolate.", "безлюдный", "Город безлюдный."),
    ("steadily", "She works steadily.", "неуклонно", "Она работает неуклонно."),
    ("unfortunate", "This is an unfortunate day.", "злополучный", "Это злополучный день."),
    ("Eagle", "The eagle flies high.", "орёл", "Орёл летит высоко."),
    ("capitulation", "The army's capitulation was unexpected.", "капитуляция", "Капитуляция армии была неожиданной."),
    ("intuitive", "This method is intuitive.", "интуитивный", "Этот метод интуитивный."),
    ("fanatic", "He is a football fanatic.", "фанатик", "Он фанатик футбола."),
    ("cunningly", "He cunningly escaped.", "хитро", "Он хитро избежал этого."),
    ("advance", "He received an advance.", "аванс", "Он получил аванс."),
    ("navigation", "Navigation is important for sailors.", "навигация", "Навигация важна для моряков."),
    ("commune", "They lived together in a commune.", "коммуна", "Они жили вместе в коммуне."),
    ("to found", "He wants to found a new city.", "основать", "Он хочет основать новый город."),
    ("tattoo", "She got a new dragon tattoo.", "татуировка", "Она сделала новую татуировку с драконом."),
    ("epithet", 'He earned the epithet "the Brave."', "эпитет", 'Он заслужил эпитет "Храбрый".'),
    ("to stick", "Mud will stick to my shoe.", "прилипнуть", "Грязь прилипнет к моей обуви."),
    ("Omsk", "I visited Omsk last summer.", "Омск", "Я посетил Омск летом."),
    ("switch", "Let's switch to a different topic.", "переключиться", "Давайте переключимся на другую тему."),
    ("ho", "Ho! Let's go!", "хо", "Хо! Пошли!"),
    ("hospitality", "Their hospitality is warm.", "гостеприимство", "Их гостеприимство тёплое."),
    ("guru", "He's a guru in digital marketing.", "гуру", "Он гуру в цифровом маркетинге."),
    ("culinary", "This is a culinary school.", "кулинарный", "Это кулинарная школа."),
    ("extramural", "She enrolled in extramural studies.", "заочный", "Она поступила на заочное обучение."),
    ("communicator", "He's an excellent communicator at work.", "коммуникатор", "Он отличный коммуникатор на работе."),
    ("patronage", "He enjoyed the king's patronage.", "покровительство", "Он пользовался покровительством короля."),
    ("moonshine", "He makes his own moonshine secretly.", "самогон", "Он тайно делает свой самогон."),
    ("spacesuit", "He wears a spacesuit.", "скафандр", "Он носит скафандр."),
    ("to bask", "Cats love to bask in the sun.", "греться", "Кошки любят греться на солнце."),
    ("salute", "I see a salute in the sky.", "салют", "Я вижу салют в небе."),
    ("optics", "The optics store sells quality lenses.", "оптика", "Магазин оптики продает качественные линзы."),
    ("dialect", "She speaks a unique local dialect.", "диалект", "Она говорит на уникальном местном диалекте."),
    ("envelop", "Mist will envelop the town.", "окутать", "Туман окутает город."),
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
