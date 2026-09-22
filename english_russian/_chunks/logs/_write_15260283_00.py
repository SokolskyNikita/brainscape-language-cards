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

SRC = PACK / "_chunks" / "deck_15260283_00.csv"
OUT = PACK / "_chunks" / "fixed" / "deck_15260283_00.csv"
LOG = PACK / "_chunks" / "logs" / "deck_15260283_00.txt"

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

# New lemmas introduced by corrections (taught on this card).
allow_ru |= {"сдержанный"}

# (en_lemma, en_ex, ru_lemma, ru_ex)
FIXED = [
    ("to overcome", "I try to overcome fear.", "одолевать", "Я стараюсь одолевать страх."),
    ("unperturbed", "He remained unperturbed.", "невозмутимый", "Он оставался невозмутимым."),
    ("cataclysm", "The cataclysm destroyed the city.", "катаклизм", "Катаклизм уничтожил город."),
    ("talk into", "She talked him into going.", "уговорить", "Она уговорила его пойти."),
    ("non-living", "A stone is a non-living thing.", "неживой", "Камень — неживая вещь."),
    ("concentratedly", "She worked concentratedly.", "сосредоточенно", "Она работала сосредоточенно."),
    ("to take care", "Please take care.", "беречься", "Пожалуйста, берегись."),
    ("to smirk", "He began to smirk.", "ухмыляться", "Он начал ухмыляться."),
    ("barricade", "They built a barricade.", "баррикада", "Они построили баррикаду."),
    ("retell", "She likes to retell the story.", "пересказывать", "Она любит пересказывать историю."),
    ("rot", "The apples will rot.", "гнить", "Яблоки будут гнить."),
    ("neurosis", "She has a neurosis.", "невроз", "У неё невроз."),
    ("diagonal", "I drew a diagonal.", "диагональ", "Я нарисовал диагональ."),
    ("Kirovsky", "I live on Kirovsky street.", "кировский", "Я живу на Кировской улице."),
    ("six hundred", "I have six hundred books.", "шестьсот", "У меня шестьсот книг."),
    ("ballad", "She sang a ballad.", "баллада", "Она спела балладу."),
    ("steering", "The steering wheel is new.", "рулевой", "Рулевое колесо новое."),
    ("armored train", "The armored train is coming.", "бронепоезд", "Бронепоезд идёт."),
    ("reconcile", "They want to reconcile.", "примириться", "Они хотят примириться."),
    ("masturbation", "Masturbation is normal.", "мастурбация", "Мастурбация нормальна."),
    ("privatize", "They want to privatize the company.", "приватизировать", "Они хотят приватизировать компанию."),
    ("membership", "His membership is over.", "членство", "Его членство кончилось."),
    ("frenziedly", "She danced frenziedly.", "бешено", "Она бешено танцевала."),
    ("stallion", "The stallion ran in the field.", "жеребец", "Жеребец бежал по полю."),
    ("blackness", "I saw only blackness.", "чернота", "Я видел только черноту."),
    ("amiss", "Something is amiss here.", "неладный", "Здесь что-то неладное."),
    ("dizziness", "She felt dizziness.", "головокружение", "Она чувствовала головокружение."),
    ("snowflake", "A snowflake fell on her nose.", "снежинка", "Снежинка упала ей на нос."),
    ("buttstock", "He held the buttstock.", "приклад", "Он держал приклад."),
    ("comfortably", "She slept comfortably.", "комфортно", "Она спала комфортно."),
    ("portable", "This computer is portable.", "портативный", "Этот компьютер портативный."),
    ("trillion", "He has a trillion dollars.", "триллион", "У него триллион долларов."),
    ("epigraph", "The book has an epigraph.", "эпиграф", "В книге есть эпиграф."),
    ("abundantly", "Flowers grew abundantly.", "обильно", "Цветы обильно росли."),
    ("cottage cheese", "I love cottage cheese.", "творог", "Я люблю творог."),
    ("stylistic", "This is a stylistic question.", "стилистический", "Это стилистический вопрос."),
    ("cut down", "They cut down the tree.", "вырубить", "Они вырубили дерево."),
    ("tin", "The box is tin.", "жестяной", "Коробка жестяная."),
    ("sour cream", "I added sour cream to the soup.", "сметана", "Я добавил сметану в суп."),
    ("palms", "She pressed her palms together.", "ладонь", "Она сжала свои ладони."),
    ("sensory", "This is a sensory test.", "сенсорный", "Это сенсорный тест."),
    ("fauna", "The fauna here is rich.", "фауна", "Фауна здесь богатая."),
    ("irreconcilable", "He is an irreconcilable enemy.", "непримиримый", "Он непримиримый враг."),
    ("to warm up", "I want to warm up.", "согреться", "Я хочу согреться."),
    ("General Staff", "He works at the General Staff.", "генштаб", "Он работает в генштабе."),
    ("to applaud", "They began to applaud.", "аплодировать", "Они начали аплодировать."),
    ("to put under", "He put a book under the pillow.", "подложить", "Он подложил книгу под подушку."),
    ("seductive", "Her voice was seductive.", "соблазнительный", "Её голос был соблазнительным."),
    ("saturate", "Rain will saturate the earth.", "насытить", "Дождь насытит землю."),
    ("wax", "She used wax for the candles.", "воск", "Она использовала воск для свечей."),
    ("unheard-of", "This is an unheard-of success.", "неслыханный", "Это неслыханный успех."),
    ("restrained", "Her answer was restrained.", "сдержанный", "Её ответ был сдержанным."),
    ("sauna", "I was in the sauna yesterday.", "сауна", "Я был в сауне вчера."),
    ("high-rise", "I live in a high-rise building.", "высотный", "Я живу в высотном доме."),
    ("authenticity", "They checked the authenticity.", "подлинность", "Они проверили подлинность."),
    ("regarding", "I wrote regarding this question.", "касательно", "Я писал касательно этого вопроса."),
    ("pasture", "Cows are in the pasture.", "пастбище", "Коровы на пастбище."),
    ("explainable", "This is explainable.", "объяснимый", "Это объяснимо."),
    ("comic book", "I love reading comic books.", "комикс", "Я люблю читать комиксы."),
    ("seduce", "She wanted to seduce him.", "соблазнить", "Она хотела соблазнить его."),
    ("to fall down", "He fell down on the floor.", "повалиться", "Он повалился на пол."),
    ("lotus", "The lotus blooms in the water.", "лотос", "Лотос цветёт в воде."),
    ("localization", "The localization of the text is ready.", "локализация", "Локализация текста готова."),
    ("pre-war", "This is a pre-war house.", "довоенный", "Это довоенный дом."),
    ("encoding", "The encoding of the text is ready.", "кодирование", "Кодирование текста готово."),
    ("consecrate", "They will consecrate the church.", "освятить", "Они освятят церковь."),
    ("taboo", "Talking about this is a taboo.", "табу", "Говорить об этом — это табу."),
    ("futile", "His attempt was futile.", "тщетный", "Его попытка была тщетной."),
    ("debauchery", "He lives in debauchery.", "разврат", "Он живёт в разврате."),
    ("voivode", "The voivode led the army.", "воевода", "Воевода вёл армию."),
    ("selfless", "She is a selfless woman.", "бескорыстный", "Она бескорыстная женщина."),
    ("offender", "He is the offender.", "обидчик", "Он обидчик."),
    ("gravitate", "They gravitate to him.", "тяготеть", "Они тяготеют к нему."),
    ("to call names", "He called him names.", "обозвать", "Он обозвал его."),
    ("pornography", "He writes about pornography.", "порнография", "Он пишет о порнографии."),
    ("gray hair", "He has gray hair.", "седина", "У него седина."),
    ("anticipation", "I felt anticipation.", "предвкушение", "Я чувствовал предвкушение."),
    ("to graze", "Cows love to graze in the field.", "пастись", "Коровы любят пастись на поле."),
    ("trigger", "He held the trigger.", "курок", "Он держал курок."),
    ("discord", "There is discord among them.", "рознь", "Среди них есть рознь."),
    ("comic", "The story is comic.", "комический", "История комическая."),
    ("plenarium", "The plenarium met today.", "пленум", "Пленум собрался сегодня."),
    ("to fuck", "He wants to fuck her.", "трахнуть", "Он хочет её трахнуть."),
    ("perversion", "This is a perversion.", "извращение", "Это извращение."),
    ("stony", "The path was stony.", "каменистый", "Путь был каменистый."),
    ("fragrant", "The flowers are fragrant.", "душистый", "Цветы душистые."),
    ("atmospheric", "This movie is atmospheric.", "атмосферный", "Этот фильм атмосферный."),
    ("broth", "I made chicken broth.", "бульон", "Я приготовил куриный бульон."),
    ("theological", "He studies theological books.", "богословский", "Он изучает богословские книги."),
    ("bureaucrat", "He is a bureaucrat.", "бюрократ", "Он бюрократ."),
    ("building up", "The building up of the army continues.", "наращивание", "Наращивание армии продолжается."),
    ("to design", "He wants to design a new machine.", "сконструировать", "Он хочет сконструировать новую машину."),
    ("subsistence", "The subsistence minimum grew.", "прожиточный", "Прожиточный минимум вырос."),
    ("verdict", "The verdict was clear.", "вердикт", "Вердикт был ясный."),
    ("whirlpool", "The boat is near the whirlpool.", "водоворот", "Лодка рядом с водоворотом."),
    ("greenish", "The walls were greenish.", "зеленоватый", "Стены были зеленоватыми."),
    ("semantics", "He studies semantics.", "семантика", "Он изучает семантику."),
    ("to color", "She will color the picture.", "раскрасить", "Она раскрасит картину."),
    ("submission", "He showed submission.", "покорность", "Он показал покорность."),
    ("port wine", "She likes port wine.", "портвейн", "Она любит портвейн."),
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
    "held": "hold",
    "told": "tell",
    "said": "say",
    "paid": "pay",
    "sold": "sell",
    "lost": "lose",
    "spent": "spend",
    "stood": "stand",
    "slept": "sleep",
    "drew": "draw",
    "grew": "grow",
    "ran": "run",
    "sang": "sing",
    "fell": "fall",
    "led": "lead",
    "pressed": "press",
    "checked": "check",
    "added": "add",
    "used": "use",
    "tried": "try",
    "talked": "talk",
    "worked": "work",
    "danced": "dance",
    "likes": "like",
    "lives": "live",
    "lived": "live",
    "wants": "want",
    "wanted": "want",
    "studies": "study",
    "writes": "write",
    "comes": "come",
    "coming": "come",
    "going": "go",
    "reading": "read",
    "talking": "talk",
    "blooms": "bloom",
    "continues": "continue",
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
    "видел": "видеть",
    "знаю": "знать",
    "живу": "жить",
    "живем": "жить",
    "живет": "жить",
    "живет": "жить",
    "нашел": "найти",
    "нашла": "найти",
    "будь": "быть",
    "стал": "стать",
    "стала": "стать",
    "стали": "стать",
    "пишет": "писать",
    "писал": "писать",
    "увидел": "видеть",
    "услышал": "слышать",
    "слышу": "слышать",
    "шел": "идти",
    "шёл": "идти",
    "шла": "идти",
    "шли": "идти",
    "идет": "идти",
    "идёт": "идти",
    "вырос": "расти",
    "росли": "расти",
    "спела": "петь",
    "держал": "держать",
    "сжала": "сжать",
    "упала": "упасть",
    "нажал": "нажать",
    "вел": "вести",
    "вёл": "вести",
    "бежал": "бежать",
    "танцевала": "танцевать",
    "стараюсь": "стараться",
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
