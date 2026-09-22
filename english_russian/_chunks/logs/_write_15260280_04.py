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

SRC = PACK / "_chunks" / "deck_15260280_04.csv"
OUT = PACK / "_chunks" / "fixed" / "deck_15260280_04.csv"
LOG = PACK / "_chunks" / "logs" / "deck_15260280_04.txt"

FUNCTION_EN = {
    "a", "an", "the", "is", "be", "i", "you", "he", "she", "it", "we", "they",
    "my", "and", "or", "in", "on", "at", "to", "of", "for", "with", "from",
    "not", "his", "him", "her", "their", "them", "our", "us", "me", "am",
    "are", "was", "were", "been", "being", "this", "that", "these", "those",
    "as", "by", "into", "about", "than", "then", "so", "if", "but", "its",
    "your", "do", "does", "did", "will", "would", "can", "could", "may",
    "there", "here", "has", "had", "have", "don't", "dont", "let's", "lets",
    "all", "off", "done", "up", "out", "no", "yes", "very", "too", "now",
    "some", "any", "only", "even", "still", "already", "always", "never",
    "after", "before", "who", "what", "when", "where", "why", "how",
    "himself", "herself", "themselves", "myself", "yourself",
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
    for line in (PACK / "_vocab" / "allow_en_15260280.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_ru = {
    line.strip().replace("ё", "е").lower()
    for line in (PACK / "_vocab" / "allow_ru_15260280.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_en |= FUNCTION_EN
allow_ru |= FUNCTION_RU

# Lemma taught by the reversible correction, already in prior-deck allow list.
allow_ru |= {"двусторонний"}

# (en_lemma, en_ex, ru_lemma, ru_ex)
FIXED = [
    ("scandalous", "His behavior was scandalous.", "скандальный", "Его поведение было скандальным."),
    ("pile on", "Critics pile on him.", "навалиться", "Критики навалились на него."),
    ("patient (female)", "The patient is in the hospital.", "пациентка", "Пациентка в больнице."),
    ("cast iron", "This pot is cast iron.", "чугунный", "Этот горшок чугунный."),
    ("drive away", "They drive away the dog.", "прогонять", "Они прогоняют собаку."),
    ("cynicism", "I do not like his cynicism.", "цинизм", "Мне не нравится его цинизм."),
    ("instrumental", "This music is instrumental.", "инструментальный", "Эта музыка инструментальная."),
    ("to stream", "Water streams from the hill.", "струиться", "Вода струится с холма."),
    ("indispensable", "This book is indispensable.", "незаменимый", "Эта книга незаменима."),
    ("pastor", "The pastor is in the church.", "пастор", "Пастор в церкви."),
    ("Chekist", "The Chekist is in the house.", "чекист", "Чекист в доме."),
    ("to be interrupted", "He is interrupted often.", "прерываться", "Он часто прерывается."),
    ("to wriggle", "The snake can wriggle.", "извиваться", "Змея может извиваться."),
    ("ideologist", "He is an ideologist.", "идеолог", "Он идеолог."),
    ("to comprehend", "I cannot comprehend this.", "постигать", "Я не могу постичь это."),
    ("shorts", "He put on shorts.", "шорты", "Он надел шорты."),
    ("adjutant", "The adjutant has a letter.", "адъютант", "У адъютанта есть письмо."),
    ("unstable", "The table is unstable.", "неустойчивый", "Стол неустойчивый."),
    ("brilliantly", "She played brilliantly.", "блестяще", "Она блестяще играла."),
    ("bait", "This is bait for the fish.", "приманка", "Это приманка для рыбы."),
    ("lazybones", "Get up, you lazybones!", "лентяй", "Вставай, лентяй!"),
    ("vial", "There is water in the vial.", "флакон", "Во флаконе есть вода."),
    ("logo", "I like this logo.", "логотип", "Мне нравится этот логотип."),
    ("werewolf", "The story is about a werewolf.", "оборотень", "Эта история про оборотня."),
    ("handful", "Give me a handful of earth.", "горсть", "Дай мне горсть земли."),
    ("almanac", "I read this almanac.", "альманах", "Я читал этот альманах."),
    ("coolness", "I like the coolness of the evening.", "прохлада", "Мне нравится прохлада вечера."),
    ("backwards", "He walked backwards.", "взад", "Он шёл взад."),
    ("parasite", "This animal is a parasite.", "паразит", "Это животное — паразит."),
    ("dad's", "This is dad's book.", "папин", "Это папина книга."),
    ("algae", "There is algae in the water.", "водоросль", "В воде есть водоросль."),
    ("rescuer", "The rescuer is here.", "спасатель", "Спасатель здесь."),
    ("tights", "She put on tights.", "колготки", "Она надела колготки."),
    ("conjuncture", "The market conjuncture is good.", "конъюнктура", "Конъюнктура рынка хорошая."),
    ("get dark", "It will get dark soon.", "стемнеть", "Скоро стемнеет."),
    ("grope", "I have to grope in the dark.", "шарить", "Мне нужно шарить в темноте."),
    ("reversible", "This jacket is reversible.", "двусторонний", "Эта куртка двусторонняя."),
    ("consolidation", "We need consolidation of the lesson.", "закрепление", "Нам нужно закрепление урока."),
    ("resonance", "His words found resonance.", "резонанс", "Его слова нашли резонанс."),
    ("symphony", "I hear a symphony.", "симфония", "Я слышу симфонию."),
    ("anti-tank", "This is an anti-tank gun.", "противотанковый", "Это противотанковая пушка."),
    ("chosen one", "He is the chosen one.", "избранник", "Он избранник."),
    ("clue", "This is an important clue.", "улика", "Это важная улика."),
    ("genetics", "He reads about genetics.", "генетика", "Он читает о генетике."),
    ("burial", "The burial was yesterday.", "захоронение", "Захоронение было вчера."),
    ("power of attorney", "I have a power of attorney.", "доверенность", "У меня есть доверенность."),
    ("rapier", "He has a rapier.", "шпага", "У него есть шпага."),
    ("hunger strike", "He is on a hunger strike.", "голодовка", "Он на голодовке."),
    ("carbohydrate", "There is carbohydrate in bread.", "углевод", "В хлебе есть углевод."),
    ("guarantor", "He is my guarantor.", "гарант", "Он мой гарант."),
    ("Sberbank", "I work at Sberbank.", "сбербанк", "Я работаю в Сбербанке."),
    ("sowing", "The sowing began in spring.", "посев", "Посев начался весной."),
    ("to shout out", "He can shout out a word.", "прокричать", "Он может прокричать слово."),
    ("to dry up", "The river can dry up.", "высохнуть", "Река может высохнуть."),
    ("editing", "Editing takes time.", "редактирование", "Редактирование занимает время."),
    ("to scoop", "I scoop water with my hand.", "черпать", "Я черпаю воду рукой."),
    ("valve", "The valve is closed.", "клапан", "Клапан закрыт."),
    ("little face", "I see her little face.", "личико", "Я вижу её личико."),
    ("hose", "Give me the hose.", "шланг", "Дай мне шланг."),
    ("milliliter", "I need one milliliter of water.", "миллилитр", "Мне нужен один миллилитр воды."),
    ("to set on fire", "He wants to set the house on fire.", "поджечь", "Он хочет поджечь дом."),
    ("symbolism", "I see the symbolism in this book.", "символика", "Я вижу символику в этой книге."),
    ("to shimmer", "The water can shimmer.", "переливаться", "Вода может переливаться."),
    ("ball of yarn", "The cat plays with a ball of yarn.", "клубок", "Кошка играет с клубком."),
    ("lottery", "She plays the lottery.", "лотерея", "Она играет в лотерею."),
    ("sanctity", "He spoke of the sanctity of life.", "святость", "Он говорил о святости жизни."),
    ("volost", "This village is in the volost.", "волость", "Эта деревня в волости."),
    ("presumably", "Presumably, he is at home.", "предположительно", "Предположительно, он дома."),
    ("mercilessly", "He spoke mercilessly.", "безжалостно", "Он говорил безжалостно."),
    ("awaken", "This news can awaken hope.", "пробудить", "Эта новость может пробудить надежду."),
    ("Briton", "This man is a Briton.", "британец", "Этот человек — британец."),
    ("to be valued", "This work is valued.", "цениться", "Эта работа ценится."),
    ("lobby", "We wait in the lobby.", "вестибюль", "Мы ждём в вестибюле."),
    ("counterweight", "This is a counterweight.", "противовес", "Это противовес."),
    ("to ask (for permission)", "The boy wants to ask to go out.", "проситься", "Мальчик хочет проситься на улицу."),
    ("in reality", "I see this in reality.", "наяву", "Я вижу это наяву."),
    ("resist", "He does not want to resist.", "противиться", "Он не хочет противиться."),
    ("hierarchical", "This is a hierarchical system.", "иерархический", "Это иерархическая система."),
    ("palatial", "This is a palatial hall.", "дворцовый", "Это дворцовый зал."),
    ("to fill up", "The hall can fill up.", "наполниться", "Зал может наполниться."),
    ("homemade", "This is a homemade radio.", "самодельный", "Это самодельное радио."),
    ("raft", "We made a raft.", "плот", "Мы сделали плот."),
    ("avalanche", "The avalanche came from the mountain.", "лавина", "Лавина пришла с горы."),
    ("to rearrange", "I need to rearrange the books.", "переложить", "Мне нужно переложить книги."),
    ("tanned", "He is very tanned.", "загорелый", "Он очень загорелый."),
    ("amnesty", "They gave him amnesty.", "амнистия", "Ему дали амнистию."),
    ("to establish oneself", "He wants to establish himself here.", "утвердиться", "Он хочет утвердиться здесь."),
    ("ode", "This is an ode.", "ода", "Это ода."),
    ("vast", "The field is vast.", "необъятный", "Поле необъятное."),
    ("truthfulness", "I know the truthfulness of his words.", "истинность", "Я знаю истинность его слов."),
    ("miraculously", "He miraculously came home.", "чудом", "Он чудом пришёл домой."),
    ("reinforce", "I can reinforce my words.", "подкрепить", "Я могу подкрепить свои слова."),
    ("hairy", "His hands are hairy.", "волосатый", "Его руки волосатые."),
    ("enrichment", "This is enrichment of the language.", "обогащение", "Это обогащение языка."),
    ("Mongol", "This man is a Mongol.", "монгол", "Этот человек — монгол."),
    ("play out", "They want to play out a scene.", "разыграть", "Они хотят разыграть сцену."),
    ("assimilation", "Assimilation of the lesson takes time.", "усвоение", "Усвоение урока занимает время."),
    ("karma", "He believes in karma.", "карма", "Он верит в карму."),
    ("degradation", "This is degradation of the language.", "деградация", "Это деградация языка."),
    ("lucky", "He is a lucky man.", "удачливый", "Он удачливый человек."),
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
    "found": "find",
    "read": "read",
    "put": "put",
    "played": "play",
    "walked": "walk",
    "began": "begin",
    "takes": "take",
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
    "шел": "идти",
    "шёл": "идти",
    "дай": "дать",
    "дали": "дать",
    "пришел": "прийти",
    "пришёл": "прийти",
    "пришла": "прийти",
    "ждем": "ждать",
    "ждём": "ждать",
    "нравится": "нравиться",
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
    parts = [p.strip() for p in re.split(r"[\s()]+", lemma.replace("ё", "е").lower()) if p.strip()]
    keys = [p for p in parts if p not in {"to", "be", "the", "a", "an", "for", "of", "one"}] or parts
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
