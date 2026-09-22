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

SRC = PACK / "_chunks" / "deck_22976521_02.csv"
OUT = PACK / "_chunks" / "fixed" / "deck_22976521_02.csv"
LOG = PACK / "_chunks" / "logs" / "deck_22976521_02.txt"

FUNCTION_EN = {
    "a", "an", "the", "is", "be", "i", "you", "he", "she", "it", "we", "they",
    "my", "and", "or", "in", "on", "at", "to", "of", "for", "with", "from",
    "not", "his", "him", "her", "their", "them", "our", "us", "me", "am",
    "are", "was", "were", "been", "being", "this", "that", "these", "those",
    "as", "by", "into", "about", "than", "then", "so", "if", "but", "its",
    "your", "do", "does", "did", "will", "would", "can", "could", "may",
    "there", "here", "has", "had", "have", "don't", "dont", "let's", "lets",
    "all", "off", "done", "myself", "yourself", "himself", "herself",
    "itself", "ourselves", "themselves", "one's", "ones", "too", "very",
    "also", "still", "even", "only", "just", "i'll", "she's", "he's", "it's",
    "no", "yes", "over", "under", "up", "down", "out", "up", "again",
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
    "давайте", "как", "что", "чтобы", "когда", "если", "где", "чем", "кто",
    "них", "него", "нее", "ней", "ним", "очень", "слишком", "нет", "да",
}

allow_en = {
    line.strip().lower()
    for line in (PACK / "_vocab" / "allow_en_22976521.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_ru = {
    line.strip().replace("ё", "е").lower()
    for line in (PACK / "_vocab" / "allow_ru_22976521.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_en |= FUNCTION_EN
allow_ru |= FUNCTION_RU

# (en_lemma, en_ex, ru_lemma, ru_ex)
FIXED = [
    ("revive, come to life", "The garden will revive in spring.", "оживиться", "Сад оживится весной."),
    ("redistribution, reallocation", "This is a redistribution of wealth.", "перераспределение", "Это перераспределение богатства."),
    ("Vladimir, Vladimirsky", "Vladimir apples are juicy.", "владимирский", "Владимирские яблоки сочные."),
    ("aiming, guidance", "The aiming of the gun was slow.", "наведение", "Наведение пушки было медленным."),
    ("edge, border", "The edge of the table is sharp.", "кромка", "Кромка стола острая."),
    ("Vologda, Vologodsky", "This is Vologda milk.", "вологодский", "Это вологодское молоко."),
    ("bodyguard, personal security officer", "He has a bodyguard.", "телохранитель", "У него есть телохранитель."),
    ("relevance, topicality", "I see the relevance of this question.", "актуальность", "Я вижу актуальность этого вопроса."),
    ("gossip, rumor", "I heard this gossip.", "сплетня", "Я слышал эту сплетню."),
    ("Marxist, Marxian", "He wrote a Marxist analysis.", "марксистский", "Он написал марксистский анализ."),
    ("correct, accurate", "Your answer is correct.", "корректный", "Ваш ответ корректен."),
    ("anonymous, anonym", "This letter is from an anonym.", "аноним", "Это письмо от анонима."),
    ("mound, hillock", "There is a mound near the house.", "бугор", "У дома есть бугор."),
    ("case, cover", "I bought a new case.", "чехол", "Я купил новый чехол."),
    ("damage, harm", "The fire caused great damage.", "урон", "Огонь причинил большой урон."),
    ("blade, edge", "The blade is sharp.", "клинок", "Клинок острый."),
    ("poster, playbill", "I saw a poster on the wall.", "афиша", "Я видел афишу на стене."),
    ("to be added, to join", "Sugar will be added last.", "добавляться", "Сахар будет добавляться последним."),
    ("cellar, basement", "We store wine in the cellar.", "погреб", "Мы храним вино в погребе."),
    ("abstraction, abstract", "This is only an abstraction.", "абстракция", "Это только абстракция."),
    ("daughter, subsidiary", "This is a daughter company.", "дочерний", "Это дочерняя компания."),
    ("universal, common to all mankind", "Love is a universal feeling.", "общечеловеческий", "Любовь — общечеловеческое чувство."),
    ("to fix, to repair", "I need to fix the chair.", "починить", "Мне нужно починить стул."),
    ("insomnia, sleeplessness", "I have insomnia.", "бессонница", "У меня бессонница."),
    ("mastery, acquisition", "He needs mastery of the language.", "овладение", "Ему нужно овладение языком."),
    ("work out, practice", "They will work out this movement.", "отрабатывать", "Они отработают это движение."),
    ("to stick out, to protrude", "He will stick out of the window.", "высунуться", "Он высунется из окна."),
    ("total, in total", "There were ten people in total.", "итого", "Итого было десять человек."),
    ("substantial, significant", "This is a substantial reason.", "весомый", "Это весомая причина."),
    ("maliciously, spitefully", "He looked at me maliciously.", "злобно", "Он злобно посмотрел на меня."),
    ("hang over, loom", "Dark clouds hang over the city.", "нависнуть", "Тёмные облака нависли над городом."),
    ("phoenix, fenix", "I know the phoenix.", "феникс", "Я знаю феникса."),
    ("fly, fly down", "I will fly to the sea.", "слетать", "Я слетаю к морю."),
    ("mosaic, tessellation", "There is a mosaic on the wall.", "мозаика", "На стене есть мозаика."),
    ("to get wet, to soak through", "I got wet in the rain.", "промокнуть", "Я промок под дождём."),
    ("elastic, resilient", "The rubber is elastic.", "упругий", "Резина упругая."),
    ("Far Eastern, Far East", "This is a Far Eastern city.", "дальневосточный", "Это дальневосточный город."),
    ("bloodstained, bloody", "The knife was bloodstained.", "окровавленный", "Нож был окровавлен."),
    ("elder, headman", "He is the elder of the village.", "староста", "Он староста деревни."),
    ("break, snap", "He will break their will.", "сломить", "Он сломит их волю."),
    ("conception, inception", "The conception was unexpected.", "зачатие", "Зачатие было неожиданным."),
    ("decency, propriety", "He has no decency.", "приличие", "У него нет приличия."),
    ("invariable, inevitable", "This is an invariable condition.", "непременный", "Это непременное условие."),
    ("leak, leakage", "There was a leak of water.", "утечка", "Была утечка воды."),
    ("lad, young man", "The lad smiled.", "парнишка", "Парнишка улыбнулся."),
    ("diligence, zeal", "I work with diligence.", "усердие", "Я работаю с усердием."),
    ("nightingale, thrush", "The nightingale sings in the garden.", "соловей", "Соловей поёт в саду."),
    ("dam, dike", "The dam is on the river.", "плотина", "Плотина на реке."),
    ("resort to, recourse to", "He will resort to force.", "прибегнуть", "Он прибегнет к силе."),
    ("reminder, notification", "Set a reminder for the meeting.", "напоминание", "Поставь напоминание о встрече."),
    ("burn, scald", "I have a burn on my hand.", "ожог", "У меня ожог на руке."),
    ("acceleration, dispersal", "The car's acceleration was fast.", "разгон", "Разгон машины был быстрым."),
    ("obtain, procure", "I will obtain this book.", "раздобыть", "Я раздобуду эту книгу."),
    ("to lay, to put", "They lay the foundation.", "закладывать", "Они закладывают фундамент."),
    ("registration, registrational", "This is a registration form.", "регистрационный", "Это регистрационная форма."),
    ("to avenge, to revenge", "He will avenge his father.", "мстить", "Он будет мстить за отца."),
    ("to last, to extend", "The meeting will last two hours.", "продлиться", "Встреча продлится два часа."),
    ("to stand, to withstand", "The church will stand for many years.", "простоять", "Церковь простоит много лет."),
    ("to exaggerate, to overstate", "He will exaggerate the story.", "преувеличивать", "Он преувеличит эту историю."),
    ("scissors, shears", "I cut paper with scissors.", "ножницы", "Я режу бумагу ножницами."),
    ("listen to, overhear", "Listen to this song.", "прослушать", "Прослушай эту песню."),
    ("homeless, vagrant", "He is homeless.", "бездомный", "Он бездомный."),
    ("regardless, irrespective", "Regardless of the weather, we will go.", "невзирая", "Невзирая на погоду, мы пойдём."),
    ("overseer, supervisor", "The overseer is in the prison.", "надзиратель", "Надзиратель в тюрьме."),
    ("inn, tavern", "We went to an inn.", "трактир", "Мы пошли в трактир."),
    ("carry out, spread", "They will spread the news.", "разнести", "Они разнесут новость."),
    ("pump, compressor", "The pump does not work.", "насос", "Насос не работает."),
    ("speaking, talking", "This is a speaking doll.", "говорящий", "Это говорящая кукла."),
    ("little shop, small store", "I saw a little shop.", "магазинчик", "Я видел магазинчик."),
    ("meanness, baseness", "This is meanness.", "подлость", "Это подлость."),
    ("crib, cot", "The baby sleeps in the crib.", "кроватка", "Малыш спит в кроватке."),
    ("puzzle, perplex", "His words will puzzle me.", "озадачить", "Его слова озадачат меня."),
    ("presentation, awarding", "The presentation of the prize was short.", "вручение", "Вручение премии было коротким."),
    ("mist, haze", "I see a mist over the river.", "дымка", "Я вижу дымку над рекой."),
    ("radically", "He changed his plan radically.", "радикально", "Он радикально изменил свой план."),
    ("to send out, to expel", "They send out the letter.", "высылать", "Они высылают письмо."),
    ("to break off, to snap", "The call broke off.", "оборваться", "Звонок оборвался."),
    ("ruthless, merciless", "He is a ruthless man.", "безжалостный", "Он безжалостный человек."),
    ("preventive, prophylactic", "This is a preventive measure.", "профилактический", "Это профилактическая мера."),
    ("hoarse, husky", "His voice is hoarse.", "хриплый", "У него хриплый голос."),
    ("blessed, hallowed", "This is a blessed day.", "благословенный", "Это благословенный день."),
    ("to stick in, to plug in", "He will stick the key in.", "воткнуть", "Он воткнёт ключ."),
    ("to master, to possess", "He will master the language.", "овладевать", "Он овладеет языком."),
    ("unreasonable, foolish", "This is an unreasonable request.", "неразумный", "Это неразумная просьба."),
    ("earth hut, dugout", "They lived in an earth hut.", "землянка", "Они жили в землянке."),
    ("Altai, Altay", "I was in the Altai mountains.", "алтайский", "Я был в Алтайских горах."),
    ("through, via", "He went through the field.", "чрез", "Он шёл чрез поле."),
    ("angry, cross", "He looked very angry yesterday.", "сердитый", "Он выглядел очень сердитым вчера."),
    ("sinner, transgressor", "Every sinner has a future.", "грешник", "У каждого грешника есть будущее."),
    ("speaker, dynamic", "The speaker is loud.", "динамик", "Динамик громкий."),
    ("transport, move", "We will transport the boxes.", "перевезти", "Мы перевезём ящики."),
    ("filling, stuffing", "I like the filling.", "начинка", "Мне нравится начинка."),
    ("redeem, buy out", "He will redeem the house.", "выкупить", "Он выкупит дом."),
    ("cutlet, patty", "I ordered a chicken cutlet for dinner.", "котлета", "Я заказал куриную котлету на ужин."),
    ("student, pupil", "The student solved the problem.", "ученица", "Ученица решила задачу."),
    ("to get pregnant, to conceive", "She hopes to get pregnant soon.", "забеременеть", "Она надеется скоро забеременеть."),
    ("awkward, clumsy", "The silence was awkward.", "неловкий", "Молчание было неловким."),
    ("Prussian", "This is a Prussian city.", "прусский", "Это прусский город."),
    ("to line up, to form up", "The soldiers will line up.", "выстроиться", "Солдаты выстроятся."),
    ("plump, chubby", "Her cheeks are plump.", "пухлый", "У неё пухлые щёки."),
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
    "slept": "sleep",
    "dug": "dig",
    "flew": "fly",
    "found": "find",
    "ran": "run",
    "knew": "know",
    "cut": "cut",
    "sings": "sing",
    "sang": "sing",
    "lived": "live",
    "looked": "look",
    "smiled": "smile",
    "changed": "change",
    "ordered": "order",
    "solved": "solve",
    "hopes": "hope",
    "caused": "cause",
    "stored": "store",
    "needs": "need",
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
    "смог": "мочь",
    "хочу": "хотеть",
    "хочет": "хотеть",
    "хотим": "хотеть",
    "вижу": "видеть",
    "видишь": "видеть",
    "видит": "видеть",
    "видел": "видеть",
    "знаю": "знать",
    "живу": "жить",
    "живем": "жить",
    "живет": "жить",
    "живёт": "жить",
    "нашел": "найти",
    "нашла": "найти",
    "нашёл": "найти",
    "будь": "быть",
    "стал": "стать",
    "стала": "стать",
    "стали": "стать",
    "пишет": "писать",
    "напиши": "писать",
    "увидел": "видеть",
    "услышал": "слышать",
    "слышу": "слышать",
    "слышал": "слышать",
    "должен": "должный",
    "должны": "должный",
    "жди": "ждать",
    "жду": "ждать",
    "открой": "открыть",
    "храните": "хранить",
    "держите": "держать",
    "шел": "идти",
    "шёл": "идти",
    "идет": "идти",
    "идёт": "идти",
    "пойдем": "пойти",
    "пойдем": "пойти",
    "поет": "петь",
    "поёт": "петь",
    "поставь": "поставить",
    "прослушай": "прослушать",
    "заказал": "заказ",
    "нравится": "нравиться",
    "изменил": "изменять",
    "промок": "промокнуть",
    "режу": "резать",
    "купил": "купить",
    "написал": "писать",
    "видел": "видеть",
}


def _ru_ok(word: str) -> bool:
    w = word.replace("ё", "е").lower()
    if w in allow_ru:
        return True
    mapped = IRREGULAR_RU.get(w) or IRREGULAR_RU.get(word.lower())
    if mapped and mapped.replace("ё", "е").lower() in allow_ru:
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
    parts = [
        re.sub(r"[^\w'-]+", "", p).strip()
        for p in re.split(r"[,;/]|\s+", lemma.replace("ё", "е").lower())
        if p.strip()
    ]
    keys = [p for p in parts if p not in {"to", "be", "the", "a", "an"}] or parts
    for key in keys:
        stem = key[:4] if len(key) >= 4 else key
        if stem and stem in text.replace(" ", ""):
            return True
        if key in text:
            return True
    return False


def first_gloss(text: str) -> str:
    return re.split(r"[,/]", text)[0].strip().lower()


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
        if first_gloss(old.get("qMdBody") or "") != first_gloss(en_lemma):
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
