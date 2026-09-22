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

SRC = PACK / "_chunks" / "deck_15260285_00.csv"
OUT = PACK / "_chunks" / "fixed" / "deck_15260285_00.csv"
LOG = PACK / "_chunks" / "logs" / "deck_15260285_00.txt"

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
allow_ru |= {"рига", "тула"}

# (en_lemma, en_ex, ru_lemma, ru_ex)
FIXED = [
    ("to bathe", "I want to bathe in the sea.", "искупаться", "Я хочу искупаться в море."),
    ("marathon", "I ran a marathon last year.", "марафон", "Я пробежал марафон в прошлом году."),
    ("wilderness", "They live in the wilderness.", "глушь", "Они живут в глуши."),
    ("to echo", "She began to echo his words.", "вторить", "Она начала вторить его словам."),
    ("Riga", "Riga is an old city.", "Рига", "Рига — старый город."),
    ("orphanage", "She grew up in an orphanage.", "детдом", "Она выросла в детдоме."),
    ("elegance", "Her dress has elegance.", "изящество", "В её платье есть изящество."),
    ("to flash", "The light will flash.", "вспыхнуть", "Свет вспыхнет."),
    ("adoption", "They waited for the adoption.", "усыновление", "Они ждали усыновления."),
    ("result from", "Problems result from this.", "проистекать", "Проблемы проистекают из этого."),
    ("holster", "The gun is in the holster.", "кобура", "Пистолет в кобуре."),
    ("unsolvable", "This question seems unsolvable.", "неразрешимый", "Этот вопрос кажется неразрешимым."),
    ("lower back", "My lower back hurts.", "поясница", "У меня болит поясница."),
    ("shudder", "I will shudder at this news.", "содрогнуться", "Я содрогнусь от этой новости."),
    ("to harm", "He does not want to harm her.", "навредить", "Он не хочет навредить ей."),
    ("anomaly", "This weather is an anomaly.", "аномалия", "Эта погода — аномалия."),
    ("document flow", "I know our document flow.", "документооборот", "Я знаю наш документооборот."),
    ("hissing", "I hear the hissing.", "шипение", "Я слышу шипение."),
    ("bore", "He is such a bore.", "зануда", "Он такой зануда."),
    ("zodiac", "I know my zodiac.", "зодиак", "Я знаю свой зодиак."),
    ("fiftieth", "This is his fiftieth year.", "пятидесятый", "Это его пятидесятый год."),
    ("accelerated", "This is an accelerated course.", "ускоренный", "Это ускоренный курс."),
    ("exhaustive", "The answer was exhaustive.", "исчерпывающий", "Ответ был исчерпывающим."),
    ("get into the swing", "She will get into the swing soon.", "разыграться", "Она скоро разыграется."),
    ("navel", "I see her navel.", "пупок", "Я вижу её пупок."),
    ("flea", "The dog has a flea.", "блоха", "У собаки есть блоха."),
    ("elaboration", "The work needs elaboration.", "проработка", "Работа требует проработки."),
    ("canyon", "We saw a canyon.", "каньон", "Мы видели каньон."),
    ("drive around", "Let's drive around the city.", "объехать", "Давай объедем город."),
    ("transnational", "This is a transnational bank.", "транснациональный", "Это транснациональный банк."),
    ("unscrupulous", "He is an unscrupulous man.", "недобросовестный", "Он недобросовестный человек."),
    ("to squeeze through", "He could squeeze through.", "пролезть", "Он смог пролезть."),
    ("psychosis", "He has a psychosis.", "психоз", "У него психоз."),
    ("scarecrow", "The scarecrow stands in the field.", "чучело", "Чучело стоит в поле."),
    ("enlighten", "Please enlighten me.", "просветить", "Пожалуйста, просветите меня."),
    ("stylistics", "He studies stylistics.", "стилистика", "Он изучает стилистику."),
    ("meteorite", "A meteorite fell in the field.", "метеорит", "Метеорит упал в поле."),
    ("canned", "The canned factory is old.", "консервный", "Консервный завод старый."),
    ("executive committee", "The executive committee is here.", "исполком", "Исполком здесь."),
    ("reproach", "She heard his reproach.", "укор", "Она слышала его укор."),
    ("to grasp", "He tries to grasp the idea.", "схватывать", "Он пытается схватывать идею."),
    ("psychoanalyst", "The psychoanalyst helped her.", "психоаналитик", "Психоаналитик помог ей."),
    ("inviolability", "The inviolability of the home is important.", "неприкосновенность", "Неприкосновенность дома важна."),
    ("meaningfully", "He looked at her meaningfully.", "многозначительно", "Он посмотрел на неё многозначительно."),
    ("calculator", "I need a calculator.", "калькулятор", "Мне нужен калькулятор."),
    ("unusually", "She smiled unusually.", "необычно", "Она необычно улыбнулась."),
    ("boarding house", "She stayed at a boarding house.", "пансион", "Она остановилась в пансионе."),
    ("pious", "She led a pious life.", "благочестивый", "Она вела благочестивую жизнь."),
    ("colonist", "The colonist built a house.", "колонист", "Колонист построил дом."),
    ("electrician", "The electrician came today.", "электрик", "Электрик пришёл сегодня."),
    ("slide down", "The snow will slide down.", "сползти", "Снег сползёт."),
    ("small flock", "A small flock of birds flew.", "стайка", "Стайка птиц летела."),
    ("madman", "The madman laughed.", "безумец", "Безумец смеялся."),
    ("unauthorized", "This is unauthorized work.", "несанкционированный", "Это несанкционированная работа."),
    ("battleship", "The battleship is at sea.", "линкор", "Линкор в море."),
    ("admission", "Admission was closed.", "допуск", "Допуск был закрыт."),
    ("two-year", "She started a two-year course.", "двухлетний", "Она начала двухлетний курс."),
    ("endurance", "He has great endurance.", "выносливость", "У него большая выносливость."),
    ("to be honored", "She will be honored.", "удостоиться", "Она удостоится чести."),
    ("consensus", "We reached a consensus.", "консенсус", "Мы достигли консенсуса."),
    ("Tula", "Tula is an old city.", "Тула", "Тула — старый город."),
    ("Atlantic", "Atlantic winds are cold.", "атлантический", "Атлантические ветры холодные."),
    ("gazelle", "I saw a gazelle.", "газель", "Я видел газель."),
    ("to be crowned", "The work will be crowned with success.", "увенчаться", "Работа увенчается успехом."),
    ("bad weather", "Bad weather ruined the day.", "непогода", "Непогода испортила день."),
    ("take root", "This idea will take root.", "прижиться", "Эта идея приживётся."),
    ("espionage", "Espionage is dangerous.", "шпионаж", "Шпионаж опасен."),
    ("Cuban", "She loves Cuban music.", "кубинский", "Она любит кубинскую музыку."),
    ("threateningly", "He looked at me threateningly.", "угрожающе", "Он посмотрел на меня угрожающе."),
    ("English-speaking", "This is an English-speaking city.", "англоязычный", "Это англоязычный город."),
    ("adopt", "They want to adopt this idea.", "перенять", "Они хотят перенять эту идею."),
    ("to interest", "Books interest her.", "заинтересовывать", "Книги заинтересовывают её."),
    ("flakes", "I like flakes.", "хлопья", "Я люблю хлопья."),
    ("tribal", "This is a tribal dance.", "племенной", "Это племенной танец."),
    ("sort out", "I need to sort out my papers.", "перебрать", "Мне нужно перебрать свои бумаги."),
    ("porter", "The porter carried our bags.", "носильщик", "Носильщик нёс наши сумки."),
    ("expend", "We will expend our time.", "израсходовать", "Мы израсходуем наше время."),
    ("Pacific", "I see the Pacific coast.", "тихоокеанский", "Я вижу тихоокеанское побережье."),
    ("self-improvement", "He wants self-improvement.", "самосовершенствование", "Он хочет самосовершенствования."),
    ("perch", "I caught a perch yesterday.", "окунь", "Вчера я поймал окуня."),
    ("Nord", "The Nord is cold.", "норд", "Норд холодный."),
    ("botanical", "She studies the botanical garden.", "ботанический", "Она изучает ботанический сад."),
    ("impermeable", "This wall is impermeable.", "непроницаемый", "Эта стена непроницаемая."),
    ("improvisation", "He loves improvisation.", "импровизация", "Он любит импровизацию."),
    ("civilizational", "This is a civilizational question.", "цивилизационный", "Это цивилизационный вопрос."),
    ("cosmonautics", "He studies cosmonautics.", "космонавтика", "Он изучает космонавтику."),
    ("headphone", "I lost my headphone yesterday.", "наушник", "Я потерял наушник вчера."),
    ("to draw in", "He began to draw in air.", "втягивать", "Он начал втягивать воздух."),
    ("loose", "The soil was loose.", "рыхлый", "Почва была рыхлой."),
    ("to prevent", "They try to prevent war.", "предотвращать", "Они пытаются предотвращать войну."),
    ("inventory", "We need new inventory.", "инвентарь", "Нам нужен новый инвентарь."),
    ("neutralize", "We must neutralize this.", "нейтрализовать", "Мы должны нейтрализовать это."),
    ("oval", "The table has an oval form.", "овальный", "Стол имеет овальную форму."),
    ("tailcoat", "He wore a tailcoat.", "фрак", "Он надел фрак."),
    ("bridesmaid", "She was a bridesmaid.", "дружка", "Она была дружкой."),
    ("schizophrenia", "He has schizophrenia.", "шизофрения", "У него шизофрения."),
    ("to cut in", "They want to cut in a lock.", "врезать", "Они хотят врезать замок."),
    ("dig up", "They will dig up the old tree.", "выкопать", "Они выкопают старое дерево."),
    ("field marshal", "The field marshal led the army.", "фельдмаршал", "Фельдмаршал вёл армию."),
    ("cobbler", "The cobbler made my shoes.", "сапожник", "Сапожник сделал мою обувь."),
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
    "led": "lead",
    "flew": "fly",
    "fell": "fall",
    "ran": "run",
    "grew": "grow",
    "wore": "wear",
    "lost": "lose",
    "stood": "stand",
    "hurt": "hurt",
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
    "видел": "видеть",
    "видели": "видеть",
    "пришел": "прийти",
    "помог": "помочь",
    "нес": "нести",
    "вел": "вести",
    "упал": "упасть",
    "поймал": "поймать",
    "потерял": "потерять",
    "надел": "надеть",
    "сделал": "сделать",
    "построил": "построить",
    "любит": "любить",
    "люблю": "любить",
    "изучает": "изучать",
    "болит": "болеть",
    "смог": "смочь",
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
