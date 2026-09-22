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

SRC = PACK / "_chunks" / "deck_15260285_04.csv"
OUT = PACK / "_chunks" / "fixed" / "deck_15260285_04.csv"
LOG = PACK / "_chunks" / "logs" / "deck_15260285_04.txt"

FUNCTION_EN = {
    "a", "an", "the", "is", "be", "i", "you", "he", "she", "it", "we", "they",
    "my", "and", "or", "in", "on", "at", "to", "of", "for", "with", "from",
    "not", "his", "him", "her", "their", "them", "our", "us", "me", "am",
    "are", "was", "were", "been", "being", "this", "that", "these", "those",
    "as", "by", "into", "about", "than", "then", "so", "if", "but", "its",
    "your", "do", "does", "did", "will", "would", "can", "could", "may",
    "there", "here", "has", "had", "have", "don't", "dont", "let's", "lets",
    "i'll", "we'll", "it's", "we're", "he's", "she's", "they're", "that's",
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

# (en_lemma, en_ex, ru_lemma, ru_ex)
FIXED = [
    ("discredit", "They want to discredit the politician.", "дискредитировать", "Они хотят дискредитировать политика."),
    ("dyed", "Her hair is dyed.", "крашеный", "Её волосы крашеные."),
    ("deceptive", "Appearances can be deceptive.", "обманчивый", "Внешность может быть обманчивой."),
    ("to feast one's eyes", "I feasted my eyes on the garden.", "насмотреться", "Я насмотрелся на сад."),
    ("clergyman", "The clergyman led the Sunday service.", "священнослужитель", "Священнослужитель провел воскресную службу."),
    ("bard", "The bard sang of ancient heroes.", "бард", "Бард пел о древних героях."),
    ("dishevel", "Wind can easily dishevel your hair.", "растрепать", "Ветер может легко растрепать твои волосы."),
    ("billiards", "We played billiards all evening long.", "бильярд", "Мы играли в бильярд весь вечер."),
    ("agony", "He screamed in agony from the wound.", "агония", "Он кричал в агонии от раны."),
    ("lifeless", "The doll's eyes were lifeless.", "безжизненный", "Глаза куклы были безжизненными."),
    ("leasing", "They chose leasing.", "лизинг", "Они выбрали лизинг."),
    ("foyer", "Meet me in the foyer.", "фойе", "Встреть меня в фойе."),
    ("yurt", "This is a yurt.", "юрта", "Это юрта."),
    ("tunic", "He wore a military tunic proudly.", "китель", "Он гордо носил военный китель."),
    ("linguistics", "She studies linguistics at the university.", "лингвистика", "Она изучает лингвистику в университете."),
    ("interviewer", "The interviewer asked insightful questions.", "интервьюер", "Интервьюер задал проницательные вопросы."),
    ("meridian", "This is the meridian.", "меридиан", "Это меридиан."),
    ("Highness", "Yes, Your Highness.", "высочество", "Да, Ваше Высочество."),
    ("tranquil", "The lake was perfectly tranquil at dawn.", "безмятежный", "Озеро было совершенно безмятежным на рассвете."),
    ("little task", "I finished the little task quickly.", "задачка", "Я быстро закончил эту маленькую задачку."),
    ("providence", "Providence saved us.", "провидение", "Провидение спасло нас."),
    ("to throw open", "She decided to throw open the windows.", "распахивать", "Она решила распахнуть окна."),
    ("modernize", "We must modernize our old factory.", "модернизировать", "Мы должны модернизировать наш старый завод."),
    ("consulting", "This is a consulting company.", "консалтинговый", "Это консалтинговая компания."),
    ("to recoil", "He recoiled in horror.", "отпрянуть", "Он отпрянул от ужаса."),
    ("instinctive", "Her reaction was instinctive.", "инстинктивный", "Её реакция была инстинктивной."),
    ("frozen", "His face was frozen.", "застывший", "Его лицо было застывшим."),
    ("devastating", "The news was absolutely devastating.", "сокрушительный", "Новость была абсолютно сокрушительной."),
    ("pantry", "The pantry is full now.", "кладовая", "Кладовая теперь полная."),
    ("Cinderella", "Cinderella lost her shoe.", "золушка", "Золушка потеряла свою обувь."),
    ("questioning", "I wait for the questioning.", "расспрос", "Я жду расспроса."),
    ("pilgrimage", "They started a spiritual pilgrimage.", "паломничество", "Они начали духовное паломничество."),
    ("astronaut", "The astronaut saw the earth.", "астронавт", "Астронавт видел землю."),
    ("indulgent", "She is an indulgent mother.", "снисходительный", "Она снисходительная мать."),
    ("subtext", "The dialogue's subtext revealed true intentions.", "подтекст", "Подтекст диалога раскрыл истинные намерения."),
    ("to be disappointed", "I tried not to be disappointed.", "разочароваться", "Я старался не разочароваться."),
    ("memorandum", "She signed the memorandum yesterday.", "меморандум", "Она подписала меморандум вчера."),
    ("Aeroflot", "Aeroflot is a big airline.", "аэрофлот", "Аэрофлот — большая авиакомпания."),
    ("sobriety", "He celebrated one year of sobriety.", "трезвость", "Он отметил год трезвости."),
    ("speculator", "The speculator bought a house.", "спекулянт", "Спекулянт купил дом."),
    ("chill", "A sudden chill filled the room.", "холодок", "Внезапный холодок наполнил комнату."),
    ("to be displayed", "The map is displayed here.", "отображаться", "Карта отображается здесь."),
    ("terrifying", "The movie was absolutely terrifying.", "ужасающий", "Фильм был абсолютно ужасающим."),
    ("to hoarse", "He began to hoarse.", "хрипеть", "Он начал хрипеть."),
    ("elegantly", "She danced elegantly.", "изящно", "Она изящно танцевала."),
    ("to amuse", "He tried hard to amuse her.", "смешить", "Он очень старался смешить её."),
    ("fortune-telling", "She believes in fortune-telling deeply.", "гадание", "Она глубоко верит в гадание."),
    ("evasion", "His evasion was clear.", "уклонение", "Его уклонение было ясным."),
    ("adept", "He is an adept of this idea.", "адепт", "Он адепт этой идеи."),
    ("telegraphic", "A telegraphic message came today.", "телеграфный", "Сегодня пришло телеграфное сообщение."),
    ("assurance", "He gave his assurance of loyalty.", "заверение", "Он дал заверение в верности."),
    ("mammoth", "The mammoth walked on the plain.", "мамонт", "Мамонт ходил по равнине."),
    ("inaccurate", "The map's directions were inaccurate.", "неточный", "Указания на карте были неточными."),
    ("matte", "This paper is matte.", "матовый", "Эта бумага матовая."),
    ("thorn", "There is a thorn on the bush.", "колючка", "На кусте есть колючка."),
    ("secluded", "They found a secluded spot for lunch.", "укромный", "Они нашли укромное местечко для обеда."),
    ("to organize", "We need to organize quickly.", "организоваться", "Нам нужно быстро организоваться."),
    ("hopelessness", "I felt hopelessness.", "безысходность", "Я чувствовал безысходность."),
    ("sane", "He seemed perfectly sane in the interview.", "вменяемый", "На интервью он казался абсолютно вменяемым."),
    ("squeaky", "The door is squeaky when opened.", "скрипучий", "Дверь скрипучая, когда её открывают."),
    ("multinational", "A multinational festival celebrates diverse cultures.", "многонациональный", "Многонациональный фестиваль празднует разнообразие культур."),
    ("drink away", "He will drink away his wealth.", "пропить", "Он пропьёт своё богатство."),
    ("little-known", "He knows a little-known artist.", "малоизвестный", "Он знает малоизвестного художника."),
    ("marinka", "I caught a marinka yesterday.", "маринка", "Вчера я поймал маринку."),
    ("reconstruct", "We must reconstruct the building.", "реконструировать", "Мы должны реконструировать здание."),
    ("videocassette", "I found an old videocassette yesterday.", "видеокассета", "Вчера я нашел старую видеокассету."),
    ("symmetrical", "The building's design is perfectly symmetrical.", "симметричный", "Дизайн здания абсолютно симметричный."),
    ("epilogue", "The book's epilogue revealed their fates.", "эпилог", "Эпилог книги раскрыл их судьбы."),
    ("into smithereens", "He smashed the vase into smithereens.", "вдребезги", "Он разбил вазу вдребезги."),
    ("leech", "The leech sucked blood from his leg.", "пиявка", "Пиявка высосала кровь из его ноги."),
    ("Ossetian", "He is an Ossetian.", "осетин", "Он осетин."),
    ("cocaine", "He was arrested for selling cocaine.", "кокаин", "Он был арестован за продажу кокаина."),
    ("nomad", "A nomad travels with the seasons.", "кочевник", "Кочевник путешествует вместе с сезонами."),
    ("moo", "The cow will moo at dawn.", "мычать", "Корова будет мычать на рассвете."),
    ("Uzbek", "My friend is an Uzbek.", "узбек", "Мой друг - узбек."),
    ("evaporate", "The puddle will soon evaporate.", "испариться", "Лужа скоро испарится."),
    ("diarrhea", "He suffered from severe diarrhea.", "понос", "Он страдал от сильного поноса."),
    ("flatter", "Do not flatter him.", "льстить", "Не льсти ему."),
    ("slyly", "He smiled slyly.", "лукаво", "Он лукаво улыбнулся."),
    ("plush", "She hugged her plush bear.", "плюшевый", "Она обняла своего плюшевого медведя."),
    ("affirmatively", "He nodded affirmatively to my question.", "утвердительно", "Он кивнул утвердительно на мой вопрос."),
    ("unfounded", "His fears were completely unfounded.", "необоснованный", "Его страхи были полностью необоснованны."),
    ("finish writing", "I will finish writing the report soon.", "дописать", "Я скоро допишу отчёт."),
    ("self-control", "He showed remarkable self-control.", "самообладание", "Он показал замечательное самообладание."),
    ("full-time", "He is a full-time student.", "очный", "Он очный студент."),
    ("deviate", "Do not deviate from the plan.", "отклоняться", "Не отклоняйтесь от плана."),
    ("to bloom", "Flowers begin to bloom in spring.", "расцветать", "Цветы начинают расцветать весной."),
    ("cloudy", "The day is cloudy.", "пасмурный", "День пасмурный."),
    ("to be demonstrated", "The work is demonstrated today.", "демонстрироваться", "Работа демонстрируется сегодня."),
    ("ethnographic", "The museum displayed ethnographic artifacts.", "этнографический", "Музей выставил этнографические артефакты."),
    ("maestro", "The maestro stood before the orchestra.", "маэстро", "Маэстро стоял перед оркестром."),
    ("pork", "I cooked pork for dinner.", "свинина", "Я приготовил свинину на ужин."),
    ("predictable", "His behavior was predictable.", "предсказуемый", "Его поведение было предсказуемым."),
    ("procedural", "The procedural rules are clear.", "процессуальный", "Процессуальные правила ясны."),
    ("distinction", "There is a clear distinction.", "различение", "Есть ясное различение."),
    ("sphinx", "The sphinx guards the ancient pyramids.", "сфинкс", "Сфинкс охраняет древние пирамиды."),
    ("cherish", "I cherish our moments together deeply.", "лелеять", "Я глубоко лелею наши моменты вместе."),
    ("triangular", "The table is triangular.", "треугольный", "Стол треугольный."),
    ("to smear", "I like to smear oil on bread.", "мазать", "Я люблю мазать масло на хлеб."),
    ("to row", "They learned to row together.", "грести", "Они научились грести вместе."),
]


IRREGULAR_EN = {
    "sang": "sing",
    "sung": "sing",
    "chose": "choose",
    "chosen": "choose",
    "slept": "sleep",
    "wore": "wear",
    "worn": "wear",
    "sat": "sit",
    "bought": "buy",
    "began": "begin",
    "begun": "begin",
    "came": "come",
    "gave": "give",
    "given": "give",
    "felt": "feel",
    "caught": "catch",
    "stood": "stand",
    "found": "find",
    "saw": "see",
    "seen": "see",
    "went": "go",
    "gone": "go",
    "took": "take",
    "taken": "take",
    "made": "make",
    "knew": "know",
    "known": "know",
    "led": "lead",
    "said": "say",
    "told": "tell",
    "got": "get",
    "had": "have",
    "did": "do",
    "was": "be",
    "were": "be",
    "been": "be",
}


def _en_ok(word: str) -> bool:
    w = word.lower()
    if w in allow_en:
        return True
    mapped = IRREGULAR_EN.get(w)
    if mapped and mapped in allow_en:
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
    # hugged / nodded
    if w.endswith("ed") and len(w) > 4 and w[-4] == w[-3] and w[:-3] in allow_en:
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
    "видел": "видеть",
    "видела": "видеть",
    "знаю": "знать",
    "живу": "жить",
    "живем": "жить",
    "живет": "жить",
    "шел": "идти",
    "шёл": "идти",
    "дай": "дать",
    "дали": "дать",
    "дал": "дать",
    "пришел": "прийти",
    "пришёл": "прийти",
    "пришла": "прийти",
    "ушел": "уйти",
    "ушёл": "уйти",
    "ждем": "ждать",
    "ждём": "ждать",
    "жду": "ждать",
    "ждёт": "ждать",
    "ждет": "ждать",
    "нравится": "нравиться",
    "встреть": "встретить",
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
