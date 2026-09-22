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

SRC = PACK / "_chunks" / "deck_15260283_04.csv"
OUT = PACK / "_chunks" / "fixed" / "deck_15260283_04.csv"
LOG = PACK / "_chunks" / "logs" / "deck_15260283_04.txt"

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

# (en_lemma, en_ex, ru_lemma, ru_ex)
FIXED = [
    ("gingerbread", "I ate gingerbread today.", "пряник", "Я ел пряник сегодня."),
    ("one-time", "I bought a one-time ticket.", "разовый", "Я купил разовый билет."),
    ("slowing down", "The slowing down of traffic was sudden.", "замедление", "Замедление движения было внезапным."),
    ("Protestant", "He visited a Protestant church.", "протестантский", "Он посетил протестантскую церковь."),
    ("ardent", "She was an ardent supporter of justice.", "пылкий", "Она была пылким сторонником справедливости."),
    ("auditory", "This is an auditory signal.", "слуховой", "Это слуховой сигнал."),
    ("company-level", "He received a company-level promotion.", "ротный", "Он получил ротное повышение."),
    ("reliably", "He reliably predicted the outcome.", "достоверно", "Он достоверно предсказал исход."),
    ("to change clothes", "I need to change clothes quickly.", "переодеваться", "Мне нужно быстро переодеться."),
    ("nitrogen", "Plants need nitrogen to grow.", "азот", "Растениям нужен азот для роста."),
    ("louse", "A louse jumped on my arm.", "вошь", "Вошь прыгнула мне на руку."),
    ("to alarm", "His behavior began to alarm her.", "настораживать", "Его поведение начало настораживать её."),
    ("racer", "The racer won the championship easily.", "гонщик", "Гонщик легко победил в чемпионате."),
    ("draught", "The cold draught made me tremble.", "сквозняк", "Холодный сквозняк заставил меня дрожать."),
    ("airborne", "The airborne soldiers landed at dawn.", "десантный", "Десантные солдаты сели на рассвете."),
    ("to tan", "She loves to tan every summer.", "загорать", "Она любит загорать каждое лето."),
    ("anesthesia", "She woke up after the anesthesia.", "наркоз", "Она проснулась после наркоза."),
    ("hypostasis", "He has a divine hypostasis.", "ипостась", "Он имеет божественную ипостась."),
    ("autobiography", "I wrote my own autobiography.", "автобиография", "Я написал свою автобиографию."),
    ("luminescence", "The luminescence was bright.", "свечение", "Свечение было ярким."),
    ("straighten out", "I will straighten out the wrinkled shirt.", "расправить", "Я расправлю мятую рубашку."),
    ("cabinet", "She stored bread in the cabinet.", "шкафчик", "Она хранила хлеб в шкафчике."),
    ("toss and turn", "I toss and turn at night.", "ворочаться", "Я ворочаюсь ночью."),
    ("splinter", "A splinter flew from the tree.", "щепка", "Щепка улетела от дерева."),
    ("to be lazy", "I decided to be lazy today.", "полениться", "Я решил полениться сегодня."),
    ("emerge", "A new plan began to emerge.", "наметиться", "Наметился новый план."),
    ("deafen", "Loud explosions can deafen me.", "оглушить", "Громкие взрывы могут оглушить меня."),
    ("doze off", "I often doze off in the evening.", "задремать", "Я часто задремываю вечером."),
    ("dimly", "The room was dimly lit.", "тускло", "Комната была тускло освещена."),
    ("to smash", "The army will smash the enemy.", "громить", "Армия будет громить врага."),
    ("to toss", "He loves to toss the stone high.", "подбрасывать", "Он любит подбрасывать камень высоко."),
    ("frigate", "The frigate sailed into the sunset.", "фрегат", "Фрегат поплыл в закат."),
    ("plantation", "The tea plantation was vast.", "плантация", "Чайная плантация была обширной."),
    ("Renaissance", "This picture is from the Renaissance.", "ренессанс", "Эта картина эпохи ренессанса."),
    ("thriller", "I love watching a good thriller.", "триллер", "Мне нравится смотреть хороший триллер."),
    ("tan", "She has a deep tan.", "загар", "У неё глубокий загар."),
    ("vestibule", "Leave your shoes in the vestibule.", "тамбур", "Оставьте обувь в тамбуре."),
    ("Dzerzhinsky", "This is a Dzerzhinsky street.", "дзержинский", "Это дзержинская улица."),
    ("respectfully", "He spoke respectfully to the old man.", "почтительно", "Он почтительно говорил со старым человеком."),
    ("gangster", "This is a gangster movie.", "бандитский", "Это бандитский фильм."),
    ("self-sufficient", "He is self-sufficient now.", "самодостаточный", "Он сейчас самодостаточный."),
    ("to slam shut", "The door will slam shut.", "захлопнуться", "Дверь захлопнется."),
    ("accentuate", "Bright colors accentuate her eyes.", "акцентировать", "Яркие цвета акцентируют её глаза."),
    ("high-tech", "This is a high-tech device.", "высокотехнологичный", "Это высокотехнологичное устройство."),
    ("imperturbable", "He remained imperturbable.", "невозмутимый", "Он остался невозмутимым."),
    ("railroader", "My father was a railroader.", "железнодорожник", "Мой отец был железнодорожником."),
    ("amulet", "She wore her amulet.", "амулет", "Она носила свой амулет."),
    ("dilemma", "Faced with a dilemma, she hesitated.", "дилемма", "Столкнувшись с дилеммой, она колебалась."),
    ("capsule", "I swallowed the medicine capsule.", "капсула", "Я проглотил капсулу с лекарством."),
    ("liquidity", "The bank has high liquidity.", "ликвидность", "У банка высокая ликвидность."),
    ("radiator", "The radiator is hot.", "радиатор", "Радиатор горячий."),
    ("realistic", "Set realistic goals for yourself.", "реалистический", "Ставьте перед собой реалистические цели."),
    ("farther away", "He stood farther away.", "поодаль", "Он стоял поодаль."),
    ("extermination", "The extermination of the enemy is needed.", "истребление", "Истребление врага нужно."),
    ("to be paid out", "Bonuses are to be paid out each month.", "выплачиваться", "Бонусы выплачиваются каждый месяц."),
    ("princely", "This is a princely palace.", "княжеский", "Это княжеский дворец."),
    ("X-ray", "I need an X-ray photo of my arm.", "рентгеновский", "Мне нужна рентгеновская фотография руки."),
    ("trough", "Pigs were eating from the trough.", "корыто", "Свиньи ели из корыта."),
    ("Duma", "He is a Duma deputy.", "думский", "Он думский депутат."),
    ("classify", "They classify books into different groups.", "классифицировать", "Они классифицируют книги на разные группы."),
    ("to slow down", "I need to slow down my step.", "замедлять", "Мне нужно замедлять свой шаг."),
    ("dig out", "They had to dig out a hole.", "вырыть", "Им пришлось вырыть яму."),
    ("hypocrisy", "His actions revealed hypocrisy.", "лицемерие", "Его действия показали лицемерие."),
    ("beef", "I cooked beef for dinner.", "говядина", "Я приготовил говядину на ужин."),
    ("bull-calf", "The farmer has a new bull-calf.", "бычок", "У фермера есть бычок."),
    ("shameful", "His behavior was truly shameful.", "постыдный", "Его поведение было поистине постыдным."),
    ("inoculate", "We must inoculate the child.", "привить", "Нам нужно привить малыша."),
    ("Bryansk", "This is Bryansk bread.", "брянский", "Это брянский хлеб."),
    ("enrich", "Travel can enrich your life.", "обогатить", "Путешествия могут обогатить вашу жизнь."),
    ("relaxation", "I need relaxation after work.", "расслабление", "Мне нужно расслабление после работы."),
    ("lama", "The lama blessed the people.", "лама", "Лама благословил народ."),
    ("high-quality", "I bought a high-quality leather jacket.", "высококачественный", "Я купил высококачественную кожаную куртку."),
    ("playpen", "The baby slept in the playpen.", "манеж", "Малыш спал в манеже."),
    ("jargon", "Legal documents are full of jargon.", "жаргон", "Юридические документы полны жаргона."),
    ("cobblestone", "There is cobblestone on the street.", "булыжник", "На улице лежит булыжник."),
    ("excess", "This excess noise is unbearable.", "перебор", "Этот перебор с шумом невыносим."),
    ("crab", "The crab went on the sand.", "краб", "Краб полз по песку."),
    ("named", "She received a named scholarship.", "именной", "Она получила именную стипендию."),
    ("print", "Please print this document for me.", "отпечатать", "Пожалуйста, отпечатайте этот документ для меня."),
    ("to request", "I want to request more information.", "запрашивать", "Я хочу запросить ещё информацию."),
    ("pop", "She loves pop music.", "эстрадный", "Она любит эстрадную музыку."),
    ("turn to stone", "He will turn to stone forever.", "окаменеть", "Он навсегда окаменеет."),
    ("blues", "He loves playing the blues.", "блюз", "Он любит играть блюз."),
    ("halo", "She had a halo of golden hair.", "ореол", "У неё был ореол из золотых волос."),
    ("turn black", "The leaf will turn black soon.", "почернеть", "Лист скоро почернеет."),
    ("ozone", "The ozone layer protects us.", "озон", "Озоновый слой защищает нас."),
    ("dilettante", "He is a dilettante in classical music.", "дилетант", "Он дилетант в классической музыке."),
    ("transverse", "The bridge has a transverse line.", "поперечный", "Мост имеет поперечную линию."),
    ("printout", "Check the printout for errors.", "распечатка", "Проверьте распечатку на наличие ошибок."),
    ("unimaginable", "The pain was simply unimaginable.", "невообразимый", "Боль была просто невообразимая."),
    ("positioning", "This is the positioning of the product.", "позиционирование", "Это позиционирование товара."),
    ("rooms", "The palace had quiet rooms.", "покои", "Во дворце были тихие покои."),
    ("hundredth", "He finished his hundredth day.", "сотый", "Он закончил свой сотый день."),
    ("nobody's", "This is nobody's house.", "ничей", "Это ничей дом."),
    ("fasten", "Please fasten the papers together.", "скрепить", "Пожалуйста, скрепите бумаги вместе."),
    ("shawl", "She put on a warm shawl.", "шаль", "Она надела тёплую шаль."),
    ("antimonopoly", "The government passed antimonopoly legislation.", "антимонопольный", "Правительство приняло антимонопольное законодательство."),
    ("aging", "Aging is a natural process.", "старение", "Старение - это естественный процесс."),
    ("piercingly", "She stared piercingly into his eyes.", "пронзительно", "Она пронзительно уставилась ему в глаза."),
    ("plywood", "We need more plywood for the project.", "фанера", "Нам нужно ещё фанеры для проекта."),
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
    "woke": "wake",
    "won": "win",
    "lit": "light",
    "set": "set",
    "put": "put",
    "said": "say",
    "told": "tell",
    "knew": "know",
    "thought": "think",
    "found": "find",
    "stood": "stand",
    "ran": "run",
    "flew": "fly",
    "wore": "wear",
    "slept": "sleep",
    "had": "have",
}


def _en_ok(word: str) -> bool:
    w = word.lower()
    if w in allow_en:
        return True
    if IRREGULAR_EN.get(w) in allow_en:
        return True
    if w.endswith("'s") and w[:-2] in allow_en:
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
    "ел": "есть",
    "ела": "есть",
    "ели": "есть",
    "яму": "яма",
    "пришлось": "прийтись",
    "сели": "сесть",
    "сел": "сесть",
    "полз": "ползти",
    "надела": "надеть",
    "надеть": "надеть",
    "лежит": "лежать",
    "показали": "показать",
    "имеет": "иметь",
    "остался": "остаться",
    "осталась": "остаться",
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
