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

SRC = PACK / "_chunks" / "deck_15260285_03.csv"
OUT = PACK / "_chunks" / "fixed" / "deck_15260285_03.csv"
LOG = PACK / "_chunks" / "logs" / "deck_15260285_03.txt"

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
    for line in (PACK / "_vocab" / "allow_en_15260285.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_ru = {
    line.strip().replace("ё", "е").lower()
    for line in (PACK / "_vocab" / "allow_ru_15260285.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_en |= FUNCTION_EN
allow_ru |= FUNCTION_RU

# New lemmas introduced by corrections (taught on this card).
allow_ru |= {"россия"}

# (en_lemma, en_ex, ru_lemma, ru_ex)
FIXED = [
    ("overlapping", "The overlapping of work caused a problem.", "перекрытие", "Перекрытие работ вызвало проблему."),
    ("Brazilian", "She loves Brazilian coffee.", "бразильский", "Она любит бразильский кофе."),
    ("vinegar", "I added vinegar to the salad.", "уксус", "Я добавил уксус в салат."),
    ("pawn", "He moved his pawn forward.", "пешка", "Он передвинул свою пешку вперёд."),
    ("cosmodrome", "The cosmodrome launched a satellite.", "космодром", "Космодром запустил спутник."),
    ("saucer", "Place your cup on the saucer.", "блюдце", "Поставьте вашу чашку на блюдце."),
    ("radio listener", "The radio listener won a prize.", "радиослушатель", "Радиослушатель получил приз."),
    ("bra", "She bought a new bra yesterday.", "лифчик", "Она купила новый лифчик вчера."),
    ("to crawl out", "He began to crawl out.", "выползать", "Он начал выползать."),
    ("one-room", "I live in a one-room apartment.", "однокомнатный", "Я живу в однокомнатной квартире."),
    ("liner", "The liner leaves at dawn.", "лайнер", "Лайнер уходит на рассвете."),
    ("fuse", "Check the fuse first.", "предохранитель", "Сначала проверьте предохранитель."),
    ("gathering", "A sinister gathering stood in the shadows.", "сборище", "Зловещее сборище стояло в тенях."),
    ("anthill", "Ants live in the anthill.", "муравейник", "Муравьи живут в муравейнике."),
    ("democratization", "The democratization process is long.", "демократизация", "Процесс демократизации долгий."),
    ("extremist", "He has extremist views.", "экстремистский", "У него экстремистские взгляды."),
    ("to tuck in", "She helped tuck in the sheets.", "заправить", "Она помогла заправить простыни."),
    ("plaster", "We put plaster on the wall.", "штукатурка", "Мы покрыли стену штукатуркой."),
    ("to decline", "The water began to decline.", "спадать", "Вода начала спадать."),
    ("doorman", "The doorman greeted us.", "швейцар", "Швейцар нас встретил."),
    ("withdrawal", "The withdrawal of soldiers began.", "вывод", "Вывод солдат начался."),
    ("woodpecker", "A woodpecker sat on the tree.", "дятел", "Дятел сидел на дереве."),
    ("sew on", "I will sew on the button tomorrow.", "пришить", "Я пришью пуговицу завтра."),
    ("Pokrovsky", "Pokrovsky Cathedral is truly magnificent.", "покровский", "Покровский собор действительно великолепен."),
    ("approvingly", "She nodded approvingly at his idea.", "одобрительно", "Она одобрительно кивнула на его идею."),
    ("skit", "They showed a short skit.", "сценка", "Они показали короткую сценку."),
    ("in passing", "She mentioned it in passing.", "мимоходом", "Она упомянула это мимоходом."),
    ("to guard", "Dogs guard the house.", "сторожить", "Собаки сторожат дом."),
    ("pull off", "He tried to pull off the cloth.", "оттянуть", "Он пытался оттянуть ткань."),
    ("polytechnic", "She studies at the polytechnic institute.", "политехнический", "Она учится в политехническом институте."),
    ("overseas", "She bought overseas tea yesterday.", "заморский", "Она купила заморский чай вчера."),
    ("marijuana", "Marijuana is illegal here.", "марихуана", "Марихуана здесь незаконна."),
    ("unattainable", "This goal is unattainable.", "недостижимый", "Эта цель недостижима."),
    ("reproductive", "Reproductive health is very important.", "репродуктивный", "Репродуктивное здоровье очень важно."),
    ("pin", "She put a pin in the fabric.", "булавка", "Она воткнула булавку в ткань."),
    ("mysteriously", "She smiled mysteriously.", "загадочно", "Она загадочно улыбнулась."),
    ("to cut through", "The boat cut through the water.", "рассекать", "Лодка рассекала воду."),
    ("chest of drawers", "I bought a new chest of drawers.", "комод", "Я купил новый комод."),
    ("cosmopolitan", "He is a true cosmopolitan.", "космополит", "Он настоящий космополит."),
    ("douse", "He doused him with water.", "облить", "Он облил его водой."),
    ("wiring", "The old wiring burned.", "проводка", "Старая проводка сгорела."),
    ("to step over", "He had to step over the puddle.", "переступать", "Ему пришлось переступить через лужу."),
    ("at times", "At times life is hard.", "временами", "Временами жизнь трудна."),
    ("to instill", "She wanted to instill hope.", "вселять", "Она хотела вселить надежду."),
    ("to blacken", "The paper began to blacken.", "чернеть", "Бумага начала чернеть."),
    ("negotiation", "The negotiation was long.", "переговоры", "Переговоры были долгими."),
    ("pant", "He began to pant after running.", "пыхтеть", "Он начал пыхтеть после бега."),
    ("to refuel", "We stopped to refuel the car.", "заправлять", "Мы остановились, чтобы заправить машину."),
    ("sharpen", "I need to sharpen the knife.", "точить", "Мне нужно точить нож."),
    ("American woman", "The American woman loves to travel.", "американка", "Американка любит путешествовать."),
    ("linguist", "She is a linguist.", "лингвист", "Она лингвист."),
    ("to pale", "Her face began to pale with fear.", "бледнеть", "Её лицо начало бледнеть от страха."),
    ("culmination", "The project reached its culmination today.", "кульминация", "Проект достиг своей кульминации сегодня."),
    ("spasm", "He felt a spasm in his leg.", "спазм", "Он почувствовал спазм в ноге."),
    ("backwoods", "He is from the backwoods.", "глубинка", "Он из глубинки."),
    ("contemptuous", "His gaze was cold and contemptuous.", "презрительный", "Его взгляд был холодным и презрительным."),
    ("lull", "After the storm came a lull.", "затишье", "После бури наступило затишье."),
    ("headboard", "She leaned against the soft headboard.", "изголовье", "Она прислонилась к мягкому изголовью."),
    ("mummy", "They found a mummy.", "мумия", "Они нашли мумию."),
    ("to tickle", "He loves to tickle his sister.", "щекотать", "Он любит щекотать свою сестру."),
    ("phantom", "The phantom stood in the dark.", "фантом", "Фантом стоял в темноте."),
    ("moving", "Fear is the moving force.", "движущий", "Страх — движущая сила."),
    ("tulip", "She planted a tulip in her garden.", "тюльпан", "Она посадила тюльпан в своём саду."),
    ("kilowatt", "The house uses one kilowatt.", "киловатт", "Дом использует один киловатт."),
    ("ham", "I made a sandwich with ham.", "ветчина", "Я сделал бутерброд с ветчиной."),
    ("amber", "She wore an amber ring.", "янтарный", "Она носила янтарное кольцо."),
    ("awkwardly", "He danced awkwardly.", "неуклюже", "Он неуклюже танцевал."),
    ("radar", "The ship appeared on the radar.", "радар", "Корабль появился на радаре."),
    ("immobility", "His injury caused immobility.", "неподвижность", "Его травма вызвала неподвижность."),
    ("handshake", "He gave me a handshake.", "рукопожатие", "Он дал мне рукопожатие."),
    ("atheism", "He wrote about atheism.", "атеизм", "Он писал об атеизме."),
    ("viscous", "The oil is viscous.", "вязкий", "Масло вязкое."),
    ("disability", "He lives with a disability.", "инвалидность", "Он живёт с инвалидностью."),
    ("to shave", "He needs to shave daily.", "бриться", "Ему нужно бриться каждый день."),
    ("imperialistic", "This war is imperialistic.", "империалистический", "Эта война империалистическая."),
    ("spontaneously", "She spontaneously began to sing.", "спонтанно", "Она спонтанно начала петь."),
    ("mold", "The bread was covered in mold.", "плесень", "Хлеб был покрыт плесенью."),
    ("to award", "They will award the winner tomorrow.", "награждать", "Они наградят победителя завтра."),
    ("iceberg", "The ship hit an iceberg.", "айсберг", "Корабль столкнулся с айсбергом."),
    ("crucifixion", "The painting shows the crucifixion.", "распятие", "На картине видно распятие."),
    ("cluster", "This cluster is large.", "кластер", "Этот кластер большой."),
    ("dugout", "Soldiers rested in the dugout.", "блиндаж", "Солдаты отдыхали в блиндаже."),
    ("capitalization", "The company's capitalization grew.", "капитализация", "Капитализация компании выросла."),
    ("cretin", "He is acting like a cretin.", "кретин", "Он ведёт себя как кретин."),
    ("self-confident", "She is too self-confident.", "самоуверенный", "Она очень самоуверенная."),
    ("Babylonian", "The Babylonian empire was ancient.", "вавилонский", "Вавилонская империя была древней."),
    ("phobia", "He has a spider phobia.", "фобия", "У него фобия пауков."),
    ("haven", "This house is a haven.", "пристанище", "Этот дом — пристанище."),
    ("megaphone", "He shouted through the megaphone.", "мегафон", "Он кричал через мегафон."),
    ("blindness", "He was born with blindness.", "слепота", "Он родился со слепотой."),
    ("derivative", "This is a derivative form.", "производный", "Это производная форма."),
    ("Russia", "Russia is a large country.", "Россия", "Россия — большая страна."),
    ("venture", "They began a risky venture.", "предприятие", "Они начали рискованное предприятие."),
    ("plumb", "The wall is plumb.", "отвесный", "Стена отвесная."),
    ("sonny", "Come here, sonny.", "сыночек", "Иди сюда, сыночек."),
    ("little finger", "He hurt his little finger.", "мизинец", "Он ударил мизинец."),
    ("hard labor", "He got hard labor.", "каторга", "Он получил каторгу."),
    ("transaction", "The bank closed the transaction.", "транзакция", "Банк закрыл транзакцию."),
    ("to slide", "He began to slide down.", "скатываться", "Он начал скатываться вниз."),
    ("to run across", "I had to run across the street.", "перебегать", "Мне пришлось перебежать улицу."),
]


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


IRREGULAR_EN = {
    "was": "be",
    "were": "be",
    "been": "be",
    "is": "be",
    "are": "be",
    "am": "be",
    "has": "have",
    "had": "have",
    "did": "do",
    "does": "do",
    "made": "make",
    "came": "come",
    "got": "get",
    "went": "go",
    "saw": "see",
    "took": "take",
    "gave": "give",
    "left": "leave",
    "felt": "feel",
    "began": "begin",
    "won": "win",
    "bought": "buy",
    "stood": "stand",
    "sat": "sit",
    "showed": "show",
    "said": "say",
    "tried": "try",
    "smiled": "smile",
    "burned": "burn",
    "wanted": "want",
    "reached": "reach",
    "planted": "plant",
    "uses": "use",
    "wore": "wear",
    "danced": "dance",
    "appeared": "appear",
    "caused": "cause",
    "wrote": "write",
    "lives": "live",
    "decided": "decide",
    "covered": "cover",
    "shows": "show",
    "hung": "hang",
    "grew": "grow",
    "acting": "act",
    "spent": "spend",
    "born": "bear",
    "cut": "cut",
    "put": "put",
    "hurt": "hurt",
    "hit": "hit",
    "found": "find",
    "loved": "love",
    "moved": "move",
    "added": "add",
    "launched": "launch",
    "helped": "help",
    "greeted": "greet",
    "studies": "study",
    "nodded": "nod",
    "mentioned": "mention",
    "leaned": "lean",
    "shouted": "shout",
    "stopped": "stop",
    "leaves": "leave",
}


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
    "передвинул": "двигать",
    "встретил": "встреча",
    "помогла": "помогать",
    "достиг": "достигать",
    "почувствовал": "чувствовать",
    "посадила": "сад",
    "наградят": "награждать",
    "перебежал": "перебегать",
    "закрыл": "закрывать",
    "ударил": "удар",
    "получил": "получить",
    "вызвала": "вызывать",
    "долгий": "долго",
    "долгими": "долго",
    "трудна": "трудно",
    "видно": "видеть",
    "выросла": "расти",
    "ведет": "вести",
    "иди": "идти",
    "сюда": "здесь",
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
