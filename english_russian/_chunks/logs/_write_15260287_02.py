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

SRC = PACK / "_chunks" / "deck_15260287_02.csv"
OUT = PACK / "_chunks" / "fixed" / "deck_15260287_02.csv"
LOG = PACK / "_chunks" / "logs" / "deck_15260287_02.txt"

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
    for line in (PACK / "_vocab" / "allow_en_15260287.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_ru = {
    line.strip().replace("ё", "е").lower()
    for line in (PACK / "_vocab" / "allow_ru_15260287.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_en |= FUNCTION_EN
allow_ru |= FUNCTION_RU

# New lemmas introduced by corrections (taught on this card).
allow_ru |= {
    "лед",
    "краеведение",
    "приоткрытый",
    "износить",
    "преосвященство",
    "хам",
    "сверлить",
}

# (en_lemma, en_ex, ru_lemma, ru_ex)
FIXED = [
    ("fly into", "Birds often fly into open windows.", "залетать", "Птицы часто залетают в открытые окна."),
    ("mitten", "She lost her mitten in the snow.", "рукавица", "Она потеряла свою рукавицу в снегу."),
    ("to be depicted", "The scene is to be depicted here.", "изображаться", "Сцена должна изображаться здесь."),
    ("supervise", "I will supervise the project closely.", "курировать", "Я буду тщательно курировать проект."),
    ("capital investment", "He made a capital investment.", "капиталовложение", "Он сделал капиталовложение."),
    ("connoisseur", "He is a connoisseur of books.", "ценитель", "Он ценитель книг."),
    ("to mutter", "He muttered under his breath.", "пробурчать", "Он пробурчал под нос."),
    ("pitfall", "There is a hidden pitfall here.", "подвох", "Здесь есть скрытый подвох."),
    ("uncontrollable", "The car was uncontrollable.", "неуправляемый", "Машина была неуправляемой."),
    ("choke", "He began to choke on water.", "захлебнуться", "Он начал захлёбываться водой."),
    ("inseparably", "They are inseparably linked.", "неразрывно", "Они неразрывно связаны."),
    ("ice", "I see ice on the lake.", "лёд", "Я вижу лёд на озере."),
    ("unnaturally", "She smiled unnaturally.", "неестественно", "Она улыбалась неестественно."),
    ("to be attracted", "She is attracted to him.", "привлекаться", "Она привлекается к нему."),
    ("self-publishing", "He chose self-publishing.", "самиздат", "Он выбрал самиздат."),
    ("to incite", "Do not incite a war.", "разжигать", "Не разжигай войну."),
    ("crossbar", "He hit the crossbar twice.", "перекладина", "Он дважды попал в перекладину."),
    ("aggressively", "He aggressively defended his opinion.", "агрессивно", "Он агрессивно защищал своё мнение."),
    ("categorical", "He gave a categorical denial.", "категорический", "Он дал категорическое отрицание."),
    ("sorting", "Sorting mail takes time.", "сортировка", "Сортировка почты занимает время."),
    ("ubiquitous", "This word is ubiquitous.", "повсеместный", "Это слово повсеместное."),
    ("prologue", "I read the book's prologue.", "пролог", "Я прочитал пролог книги."),
    ("smoke out", "They will smoke out the rats.", "выкурить", "Они выкурят крыс."),
    ("angelic", "Her smile was simply angelic.", "ангельский", "Её улыбка была просто ангельской."),
    ("self-expression", "Art is a form of self-expression.", "самовыражение", "Искусство — это форма самовыражения."),
    ("deduction", "I got a tax deduction.", "вычет", "Я получил налоговый вычет."),
    ("local history", "I read local history.", "краеведение", "Я читаю краеведение."),
    ("impostor", "He was an impostor.", "самозванец", "Он был самозванцем."),
    ("ajar", "The door was ajar.", "приоткрытый", "Дверь была приоткрыта."),
    ("to be canceled", "The meeting is to be canceled.", "отменяться", "Встреча отменяется."),
    ("front-line soldier", "He is a front-line soldier.", "фронтовик", "Он фронтовик."),
    ("bear cub", "The bear cub followed its mother.", "медвежонок", "Медвежонок следовал за своей матерью."),
    ("arbitrator", "The arbitrator heard the dispute.", "арбитр", "Арбитр выслушал спор."),
    ("hold", "The cargo is in the hold.", "трюм", "Груз в трюме."),
    ("denigrate", "Do not denigrate this man.", "порочить", "Не порочь этого человека."),
    ("butcher", "The butcher prepared the meat.", "мясник", "Мясник приготовил мясо."),
    ("enzyme", "This enzyme works.", "фермент", "Этот фермент работает."),
    ("fresco", "I saw a fresco.", "фреска", "Я увидел фреску."),
    ("compote", "I made cherry compote yesterday.", "компот", "Вчера я сделал вишнёвый компот."),
    ("to wear out", "He will wear out these shoes.", "износить", "Он износит эту обувь."),
    ("barbell", "He lifted the barbell.", "штанга", "Он поднял штангу."),
    ("troop", "The troop went through the forest.", "отряд", "Отряд шёл через лес."),
    ("protracted", "The negotiations were protracted.", "затяжной", "Переговоры были затяжными."),
    ("abstinence", "Abstinence is hard.", "воздержание", "Воздержание трудно."),
    ("to be welcomed", "Guests are always welcomed.", "приветствоваться", "Гости всегда приветствуются."),
    ("advisory", "This is an advisory body.", "консультативный", "Это консультативный орган."),
    ("departmental", "This is a departmental question.", "ведомственный", "Это ведомственный вопрос."),
    ("printing", "He works in printing.", "полиграфия", "Он работает в полиграфии."),
    ("ingenuity", "His ingenuity helped us.", "изобретательность", "Его изобретательность помогла нам."),
    ("reactionary", "His ideas were reactionary.", "реакционный", "Его идеи были реакционными."),
    ("to be played out", "The scene is being played out.", "разыгрываться", "Сцена разыгрывается."),
    ("Yugoslav", "This is a Yugoslav city.", "югославский", "Это югославский город."),
    ("to get out of breath", "I got out of breath.", "запыхаться", "Я запыхался."),
    ("uncertain", "He felt uncertain.", "неуверенный", "Он чувствовал себя неуверенным."),
    ("eau de cologne", "He bought eau de cologne.", "одеколон", "Он купил одеколон."),
    ("Tajik", "He is Tajik.", "таджик", "Он таджик."),
    ("murkiness", "There is murkiness in the water.", "муть", "В воде есть муть."),
    ("injure", "Do not injure your hand.", "травмировать", "Не травмируй руку."),
    ("summing up", "The summing up took time.", "подведение", "Подведение заняло время."),
    ("systematize", "We must systematize our work.", "систематизировать", "Мы должны систематизировать нашу работу."),
    ("repay", "I will repay you soon.", "воздать", "Я скоро воздам тебе."),
    ("flatly", "He flatly refused their offer.", "наотрез", "Он наотрез отказался от их предложения."),
    ("eminence", "I saw His Eminence.", "преосвященство", "Я видел Его Преосвященство."),
    ("inside out", "He wore his shirt inside out.", "наизнанку", "Он носил свою рубашку наизнанку."),
    ("boor", "He is a boor.", "хам", "Он хам."),
    ("gas mask", "He wore a gas mask.", "противогаз", "Он надел противогаз."),
    ("to bite off", "He tried to bite off more bread.", "откусить", "Он попытался откусить больше хлеба."),
    ("ghetto", "They lived in the ghetto.", "гетто", "Они жили в гетто."),
    ("to get off", "He is getting off the horse.", "слезать", "Он слезает с лошади."),
    ("to hate", "She began to hate him.", "возненавидеть", "Она возненавидела его."),
    ("nourishment", "We need nourishment.", "пропитание", "Нам нужно пропитание."),
    ("vineyard", "We visited the vineyard yesterday.", "виноградник", "Мы посетили виноградник вчера."),
    ("to seduce", "He tried to seduce her with gifts.", "соблазнять", "Он пытался соблазнить её подарками."),
    ("hummock", "There is a hummock here.", "кочка", "Здесь есть кочка."),
    ("lexicon", "His lexicon is large.", "лексикон", "Его лексикон большой."),
    ("laconic", "His answer was laconic.", "лаконичный", "Его ответ был лаконичным."),
    ("palette", "Her palette has many colors.", "палитра", "На её палитре много цветов."),
    ("ignition", "Turn the key for ignition.", "зажигание", "Поверните ключ для зажигания."),
    ("sail away", "They will sail away together.", "уплыть", "Они уплывут вместе."),
    ("feeder", "There is a feeder in the garden.", "кормушка", "В саду есть кормушка."),
    ("chromosome", "This is a chromosome.", "хромосома", "Это хромосома."),
    ("Eurasian", "This is a Eurasian country.", "евразийский", "Это евразийская страна."),
    ("squeak", "I heard a squeak.", "писк", "Я услышал писк."),
    ("to fan", "She began to fan the fire.", "раздувать", "Она начала раздувать огонь."),
    ("gallop", "The horse went at a gallop.", "галоп", "Лошадь шла галопом."),
    ("easy", "The task was easy.", "нетрудный", "Задача была нетрудной."),
    ("speculative", "This idea seems speculative.", "спекулятивный", "Эта идея кажется спекулятивной."),
    ("to drill", "He began to drill into the wall.", "сверлить", "Он начал сверлить стену."),
    ("vocals", "I like her vocals.", "вокал", "Мне нравится её вокал."),
    ("enclosure", "The dogs are in the enclosure.", "загон", "Собаки в загоне."),
    ("city committee", "The city committee met yesterday.", "горком", "Горком собрался вчера."),
    ("impassive", "His face was impassive.", "бесстрастный", "Его лицо было бесстрастным."),
    ("health-improving", "This is health-improving rest.", "оздоровительный", "Это оздоровительный отдых."),
    ("potency", "The medication's potency is high.", "потенция", "Потенция лекарства высокая."),
    ("restlessly", "She walked restlessly.", "беспокойно", "Она беспокойно ходила."),
    ("fishing line", "He bought a fishing line.", "леска", "Он купил леску."),
    ("chestnut", "I see a chestnut.", "каштан", "Я вижу каштан."),
    ("interception", "He made an interception.", "перехват", "Он сделал перехват."),
    ("truce", "They finally agreed to a truce.", "перемирие", "Они наконец согласились на перемирие."),
    ("dentist", "I visited the dentist yesterday.", "стоматолог", "Я посетил стоматолога вчера."),
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
    "chose": "choose",
    "lost": "lose",
    "hit": "hit",
    "read": "read",
    "gave": "give",
    "wore": "wear",
    "lived": "live",
    "tried": "try",
    "liked": "like",
    "walked": "walk",
    "helped": "help",
    "visited": "visit",
    "followed": "follow",
    "covered": "cover",
    "linked": "link",
    "muttered": "mutter",
    "smiled": "smile",
    "defended": "defend",
    "lifted": "lift",
    "prepared": "prepare",
    "refused": "refuse",
    "agreed": "agree",
    "takes": "take",
    "works": "work",
    "gives": "give",
    "requires": "require",
    "getting": "get",
    "being": "be",
    "played": "play",
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
    "шел": "идти",
    "шла": "идти",
    "шли": "идти",
    "иду": "идти",
    "идет": "идти",
    "дал": "давать",
    "дала": "давать",
    "получил": "получить",
    "помогла": "помочь",
    "собрался": "собрать",
    "нравится": "нравиться",
    "запыхался": "запыхаться",
    "возненавидела": "возненавидеть",
    "пробурчал": "пробурчать",
    "приоткрыта": "приоткрытый",
    "льдом": "лед",
    "износит": "износить",
    "сверлить": "сверлить",
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
