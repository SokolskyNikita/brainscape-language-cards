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

SRC = PACK / "_chunks" / "deck_15260277_02.csv"
OUT = PACK / "_chunks" / "fixed" / "deck_15260277_02.csv"
LOG = PACK / "_chunks" / "logs" / "deck_15260277_02.txt"

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
    for line in (PACK / "_vocab" / "allow_en_15260277.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_ru = {
    line.strip().replace("ё", "е").lower()
    for line in (PACK / "_vocab" / "allow_ru_15260277.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_en |= FUNCTION_EN
allow_ru |= FUNCTION_RU

# New lemmas introduced by corrections (taught on this card).
allow_ru |= {"самара", "разместить", "самооценка", "отрывной", "цезарь"}

# (en_lemma, en_ex, ru_lemma, ru_ex)
FIXED = [
    ("dedication", "The book's dedication is short.", "посвящение", "Посвящение в книге короткое."),
    ("dynamo", "He plays for Dynamo.", "динамо", "Он играет за Динамо."),
    ("periphery", "Our house is on the periphery.", "периферия", "Наш дом на периферии."),
    ("islet", "There is an islet in the sea.", "островок", "В море есть островок."),
    ("disgraceful", "His behavior was disgraceful.", "позорный", "Его поведение было позорным."),
    ("clown", "The clown laughs.", "клоун", "Клоун смеётся."),
    ("to collapse", "The building can collapse.", "рушиться", "Здание может рушиться."),
    ("to slip through", "He will slip through.", "проскочить", "Он проскочит."),
    ("blink", "Stars blink at night.", "мигать", "Звезды мигают ночью."),
    ("shoulder blade", "My shoulder blade hurts.", "лопатка", "У меня болит лопатка."),
    ("clumsy", "He is a clumsy boy.", "неуклюжий", "Он неуклюжий мальчик."),
    ("suspend", "They decided to suspend the project.", "приостановить", "Они решили приостановить проект."),
    ("reorganization", "The company announced a reorganization.", "реорганизация", "Компания объявила о реорганизации."),
    ("unhealthy", "This is an unhealthy habit.", "нездоровый", "Это нездоровая привычка."),
    ("sanctuary", "This church is our sanctuary.", "святыня", "Эта церковь - наша святыня."),
    ("reluctantly", "He reluctantly agreed.", "неохотно", "Он неохотно согласился."),
    ("wash off", "I want to wash off the paint.", "смыть", "Я хочу смыть краску."),
    ("encouragement", "I need your encouragement.", "поощрение", "Мне нужно твоё поощрение."),
    ("hectare", "They have five hectares.", "гектар", "У них пять гектаров."),
    ("little flower", "I have a little flower.", "цветочек", "У меня есть цветочек."),
    ("whore", "Do not call her a whore.", "блядь", "Не называй её блядью."),
    ("to push", "He likes to push me.", "подталкивать", "Он любит меня подталкивать."),
    ("vacuum", "There is a vacuum in the room.", "вакуум", "В комнате вакуум."),
    ("nausea", "I feel nausea.", "тошнота", "Я чувствую тошноту."),
    ("emit", "Stars emit light and heat.", "излучать", "Звезды излучают свет и тепло."),
    ("psychiatric", "This is psychiatric help.", "психиатрический", "Это психиатрическая помощь."),
    ("inappropriate", "Your joke was inappropriate.", "неуместный", "Твоя шутка была неуместной."),
    ("harshly", "He speaks harshly.", "сурово", "Он говорит сурово."),
    ("sectoral", "This is a sectoral problem.", "отраслевой", "Это отраслевая проблема."),
    ("unilateral", "His answer was unilateral.", "односторонний", "Его ответ был односторонним."),
    ("Petrovsky", "The Petrovsky park is near.", "петровский", "Петровский парк рядом."),
    ("cooperative", "They have a cooperative.", "кооператив", "У них есть кооператив."),
    ("to hire", "They hire a man.", "нанимать", "Они нанимают человека."),
    ("pioneering", "This is pioneering work.", "пионерский", "Это пионерская работа."),
    ("concern", "This is a large concern.", "концерн", "Это большой концерн."),
    ("to have breakfast", "I like to have breakfast early.", "завтракать", "Мне нравится завтракать рано."),
    ("controller", "The controller does not work.", "контроллер", "Контроллер не работает."),
    ("barren", "The land is barren.", "бесплодный", "Земля бесплодная."),
    ("to repel", "She tried to repel him.", "оттолкнуть", "Она пыталась его оттолкнуть."),
    ("birth rate", "The birth rate is low.", "рождаемость", "Рождаемость низкая."),
    ("cottage", "We have a cottage near the lake.", "коттедж", "У нас коттедж у озера."),
    ("to flow down", "Water can flow down.", "стекать", "Вода может стекать."),
    ("celebrity", "I see a celebrity.", "знаменитость", "Я вижу знаменитость."),
    ("impregnate", "Impregnate the fabric with oil.", "пропитать", "Пропитайте ткань маслом."),
    ("heart attack", "He had a heart attack.", "инфаркт", "У него был инфаркт."),
    ("writer's", "This is a writer's book.", "писательский", "Это писательская книга."),
    ("physiology", "This is human physiology.", "физиология", "Это физиология человека."),
    ("fruitful", "The meeting was fruitful.", "плодотворный", "Встреча была плодотворной."),
    ("shashlik", "We have shashlik this evening.", "шашлык", "У нас шашлык этим вечером."),
    ("poor man", "The poor man has no bread.", "бедняк", "У бедняка нет хлеба."),
    ("human rights activist", "He is a human rights activist.", "правозащитник", "Он правозащитник."),
    ("richly", "This house is richly made.", "богато", "Этот дом богато сделан."),
    ("vicious", "This is a vicious habit.", "порочный", "Это порочная привычка."),
    ("filling", "The filling of the form takes time.", "заполнение", "Заполнение формы занимает время."),
    ("Samara", "Samara is a beautiful city.", "Самара", "Самара - красивый город."),
    ("to accommodate", "We will accommodate him.", "разместить", "Мы его разместим."),
    ("archaeologist", "He is an archaeologist.", "археолог", "Он археолог."),
    ("diagram", "I have a diagram.", "диаграмма", "У меня есть диаграмма."),
    ("cavalry", "The cavalry is near.", "конница", "Конница рядом."),
    ("excavation", "The excavation is near the river.", "раскопка", "Раскопка у реки."),
    ("emission", "The factory has a large emission.", "выброс", "У завода большой выброс."),
    ("winged", "A winged horse is near.", "крылатый", "Крылатая лошадь рядом."),
    ("dew", "There is dew on the grass.", "роса", "На траве есть роса."),
    ("geopolitical", "This is a geopolitical question.", "геополитический", "Это геополитический вопрос."),
    ("label", "I check the label.", "ярлык", "Я проверяю ярлык."),
    ("ruthless", "He is a ruthless man.", "беспощадный", "Он беспощадный человек."),
    ("to evacuate", "They evacuate him.", "вывозить", "Они его вывозят."),
    ("vaccination", "Vaccination protects against disease.", "прививка", "Прививка защищает от болезни."),
    ("abstain", "I will abstain from this.", "воздержаться", "Я воздержусь от этого."),
    ("Caesar", "I read about Caesar.", "Цезарь", "Я читал о Цезаре."),
    ("serial", "This is serial production.", "серийный", "Это серийное производство."),
    ("isolate", "We isolate him.", "изолировать", "Мы его изолируем."),
    ("contingent", "The contingent arrived on time.", "контингент", "Контингент прибыл вовремя."),
    ("drinking party", "The drinking party was at night.", "пьянка", "Пьянка была ночью."),
    ("wholly", "This is wholly his work.", "всецело", "Это всецело его работа."),
    ("to adjust", "I adjust the radio.", "настраивать", "Я настраиваю радио."),
    ("painfully", "He takes this painfully.", "болезненно", "Он принимает это болезненно."),
    ("self-esteem", "He has high self-esteem.", "самооценка", "У него высокая самооценка."),
    ("Hungarian", "She speaks Hungarian.", "венгерский", "Она говорит на венгерском."),
    ("cough", "I have a cough.", "кашель", "У меня кашель."),
    ("immunity", "He has immunity.", "иммунитет", "У него есть иммунитет."),
    ("lead around", "He tried to lead me around.", "обвести", "Он пытался меня обвести."),
    ("millionaire", "He is a millionaire.", "миллионер", "Он миллионер."),
    ("high-ranking", "He is a high-ranking man.", "высокопоставленный", "Он высокопоставленный человек."),
    ("regional committee", "The regional committee met today.", "обком", "Обком встретился сегодня."),
    ("to snack", "I want to snack.", "закусить", "Я хочу закусить."),
    ("realism", "I like realism.", "реализм", "Мне нравится реализм."),
    ("hereditary", "This is a hereditary disease.", "наследственный", "Это наследственная болезнь."),
    ("mat", "Put your shoes on the mat.", "коврик", "Поставь свою обувь на коврик."),
    ("autograph", "I have his autograph after the concert.", "автограф", "У меня его автограф после концерта."),
    ("resettlement", "Resettlement takes time.", "переселение", "Переселение занимает время."),
    ("tear-off", "I have a tear-off calendar.", "отрывной", "У меня отрывной календарь."),
    ("exchange glances", "They will exchange glances.", "переглянуться", "Они переглянутся."),
    ("archbishop", "The archbishop is near.", "архиепископ", "Архиепископ рядом."),
    ("theorem", "This theorem is short.", "теорема", "Эта теорема короткая."),
    ("to pardon", "The king will pardon him.", "помиловать", "Король его помилует."),
    ("bill of exchange", "He has a bill of exchange.", "вексель", "У него есть вексель."),
    ("competitiveness", "They have competitiveness.", "конкурентоспособность", "У них есть конкурентоспособность."),
    ("incompatible", "Their views are incompatible.", "несовместимый", "Их взгляды несовместимы."),
    ("indisputable", "Her talent is indisputable.", "бесспорный", "Её талант бесспорен."),
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
