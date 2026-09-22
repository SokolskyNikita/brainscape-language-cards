#!/usr/bin/env python3
"""Analyze deck_15260188.csv against FIXUP_PLAYBOOK rules. Read-only."""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

from brainscape import cards_from_path, lemma_from_card

BASE = Path("russian_english")
PRIOR = [BASE / "deck_15260182.csv", BASE / "deck_15260185.csv"]
TARGET = BASE / "deck_15260188.csv"

BAD_GLOSS_PAIRS: dict[str, set[str]] = {
    "не": {"no"},
    "я": {"me"},
    "они": {"them"},
    "мы": {"us"},
    "он": {"it"},
    "она": {"it"},
    "этот": {"that"},
    "у": {"near"},
    "бы": {"if"},
    "время": {"hour"},
    "год": {"annum"},
    "ты": {"thou"},
}

ARCHAIC_LATIN = {
    "thou", "thee", "thy", "thine", "ye",
    "annum", "per", "via", "ibid", "cf", "viz",
    "hamlet",
}

DRILL_PATTERNS = [
    re.compile(r"^[А-ЯЁ][а-яё]+\s+и\s+[А-ЯЁа-яё]+\.\s*$"),
    re.compile(r"^[А-ЯЁ][а-яё]+\s+в\s+[А-ЯЁа-яё]+\.\s*$"),
]

PLACE_WORDS = {
    "москва", "москве", "москву", "москвой",
    "питер", "питере", "петербург", "петербурге",
    "кафе", "парк", "парке", "парку",
    "ресторан", "ресторане",
}

CYR_WORD = re.compile(r"[А-ЯЁа-яё]+")
LATIN_WORD = re.compile(r"[a-zA-Z]+")

# Common Russian inflection suffixes to strip for stem matching
INFLECTION_SUFFIXES = (
    "иями", "ями", "ами", "ях", "ах", "ов", "ев", "ей", "ём", "ем",
    "ом", "ой", "ей", "ью", "ию", "ия", "ие", "ии", "ий", "ым", "им",
    "ых", "их", "ую", "юю", "ая", "яя", "ое", "ее", "ые", "ие",
    "а", "я", "у", "ю", "е", "и", "ы", "о", "ь",
)

RUSSIAN_STOP = {
    "и", "в", "во", "не", "на", "с", "со", "к", "ко", "у", "о", "об", "обо",
    "от", "до", "за", "из", "по", "для", "при", "над", "под", "перед", "между",
    "а", "но", "или", "ли", "бы", "же", "то", "это", "что", "как", "так",
    "я", "ты", "он", "она", "оно", "мы", "вы", "они", "мне", "тебе", "ему",
    "ей", "нам", "вам", "им", "меня", "тебя", "его", "её", "ее", "нас", "вас", "их",
    "мой", "моя", "моё", "мое", "мои", "твой", "свой", "своя", "своё", "свое",
    "наш", "ваш", "этот", "эта", "это", "эти", "тот", "та", "те", "такой",
    "который", "которая", "которое", "которые", "котором", "которой",
    "кто", "где", "когда", "почему", "зачем", "куда", "откуда", "сколько",
    "очень", "уже", "ещё", "еще", "тоже", "также", "только", "даже", "если",
    "чтобы", "потому", "поэтому", "хотя", "пока", "был", "была", "было", "были",
    "есть", "будет", "буду", "будешь", "нет", "да", "ну", "вот", "тут", "там",
    "здесь", "сюда", "туда", "пожалуйста", "спасибо", "извините", "простите",
    "хорошо", "ладно", "конечно", "может", "надо", "нужно", "можно", "нельзя",
    "всё", "все", "всего", "всей", "всем", "один", "одна", "одно", "два",
    "больше", "меньше", "много", "мало", "немного", "чуть", "совсем",
    "сегодня", "вчера", "завтра", "сейчас", "потом", "раньше", "позже",
    "всегда", "никогда", "иногда", "часто", "редко", "опять", "снова",
    "просто", "прямо", "именно", "почти", "вдруг", "вроде", "ни", "либо",
    "чем", "какой", "какая", "какое", "какие", "сам", "сама", "само", "сами",
    "себя", "себе", "собой", "никто", "ничто", "ничего", "кого", "чего",
    "кому", "чему", "кем", "про", "без", "через", "мимо", "вокруг",
    "после", "вместо", "кроме", "среди", "против", "ради", "благодаря",
    "нему", "ней", "него", "неё", "нее", "них", "нем", "нём",
    "мной", "мною", "тобой", "тобою", "собою",
    "быть", "будем", "будете", "будут", "будешь",
    "так", "тут", "там", "здесь", "отсюда", "оттуда",
    "раз", "два", "три", "четыре", "пять",
    "этом", "этой", "этих", "том", "той", "тех",
    "мне", "тебе", "себе", "нам", "вам",
    "моего", "моей", "моих", "твоего", "твоей", "своего", "своей", "своих",
    "его", "её", "ее", "их", "нашего", "нашей", "вашего", "вашей",
    "как", "так", "вот", "ведь", "уж", "ли", "же", "бы",
    "где", "куда", "откуда", "когда", "как", "сколько", "почему", "зачем",
    "что", "чтобы", "чем", "чего", "чему", "чём", "чем",
    "кто", "кого", "кому", "кем", "ком",
    "чей", "чья", "чьё", "чьи", "чьего", "чьей",
    "сто", "тысяча", "миллион",
}

# Irregular / common inflected forms mapped to lemmas we'll encounter
IRREGULAR_FORMS: dict[str, str] = {
    "был": "быть", "была": "быть", "было": "быть", "были": "быть",
    "есть": "быть", "буду": "быть", "будет": "быть", "будем": "быть",
    "шёл": "идти", "шла": "идти", "шли": "идти", "шел": "идти",
    "пошёл": "пойти", "пошла": "пойти", "пошли": "пойти", "пошел": "пойти",
    "пришёл": "прийти", "пришла": "прийти", "пришли": "прийти", "пришел": "прийти",
    "ушёл": "уйти", "ушла": "уйти", "ушли": "уйти", "ушел": "уйти",
    "вышел": "выйти", "вышла": "выйти", "вышли": "выйти",
    "лучше": "хороший", "лучший": "хороший", "хуже": "плохой",
    "больше": "большой", "меньше": "маленький",
    "дети": "ребёнок", "детей": "ребёнок", "ребенок": "ребёнок", "ребёнка": "ребёнок",
    "люди": "человек", "людей": "человек", "человека": "человек",
    "время": "время", "времени": "время", "временем": "время",
    "дело": "дело", "дела": "дело", "делу": "дело",
    "день": "день", "дня": "день", "днём": "день", "днем": "день",
    "год": "год", "года": "год", "году": "год", "лет": "год",
    "дом": "дом", "дома": "дом", "доме": "дом", "домой": "дом",
    "рука": "рука", "руки": "рука", "руке": "рука", "рукой": "рука",
    "глаз": "глаз", "глаза": "глаз", "глазами": "глаз",
    "слово": "слово", "слова": "слово", "слову": "слово",
    "вода": "вода", "воды": "вода", "воде": "вода", "водой": "вода",
    "стол": "стол", "стола": "стол", "столе": "стол", "столом": "стол",
    "чай": "чай", "кофе": "кофе",
    "молоко": "молоко", "молоком": "молоко",
    "книга": "книга", "книги": "книга", "книге": "книга", "книгу": "книга",
    "город": "город", "города": "город", "городе": "город",
    "страна": "страна", "страны": "страна", "стране": "страна",
    "жизнь": "жизнь", "жизни": "жизнь",
    "работа": "работа", "работы": "работа", "работе": "работа",
    "школа": "школа", "школы": "школа", "школе": "школа",
    "мир": "мир", "мира": "мир", "мире": "мир",
    "история": "история", "истории": "история",
    "деньги": "деньги", "денег": "деньги",
    "ничего": "ничто", "никого": "никто", "никому": "никто",
    "котором": "который", "которой": "который", "которого": "который",
    "которую": "который", "которые": "который", "которым": "который",
    "своём": "свой", "своем": "свой", "своей": "свой", "своего": "свой",
    "своих": "свой", "свою": "свой", "свои": "свой",
    "нему": "он", "ней": "она", "него": "он", "неё": "она", "нее": "она",
    "них": "они", "нем": "он", "нём": "он",
    "меня": "я", "тебя": "ты", "нас": "мы", "вас": "вы",
    "мной": "я", "тобой": "ты",
    "этого": "этот", "этой": "этот", "эту": "этот", "эти": "этот", "этих": "этот",
    "того": "тот", "той": "тот", "ту": "тот", "те": "тот", "тех": "тот",
    "такое": "такой", "такая": "такой", "такие": "такой", "таких": "такой",
    "таком": "такой", "такую": "такой",
    "новый": "новый", "нового": "новый", "новой": "новый", "новые": "новый",
    "новую": "новый", "новым": "новый",
    "хороший": "хороший", "хорошая": "хороший", "хорошее": "хороший",
    "хорошие": "хороший", "хорошую": "хороший", "хорошем": "хороший",
    "большой": "большой", "большая": "большой", "большое": "большой",
    "большие": "большой", "большую": "большой",
    "маленький": "маленький", "маленькая": "маленький",
    "первый": "первый", "первого": "первый", "первой": "первый", "первые": "первый",
    "русский": "русский", "русская": "русский", "русское": "русский",
    "русские": "русский", "русском": "русский",
    "английский": "английский", "английская": "английский",
    "московский": "московский",
    "питер": "питер", "петербург": "петербург",
    "москва": "москва", "москве": "москва",
    "парке": "парк", "парку": "парк",
    "домой": "дом", "дома": "дом",
    "прав": "правый", "права": "правый",
    "знаю": "знать", "знает": "знать", "знают": "знать", "знал": "знать",
    "любит": "любить", "люблю": "любить", "любят": "любить",
    "хочу": "хотеть", "хочет": "хотеть", "хотят": "хотеть",
    "могу": "мочь", "может": "мочь", "могут": "мочь", "мог": "мочь",
    "делаю": "делать", "делает": "делать", "делают": "делать", "делал": "делать",
    "говорю": "говорить", "говорит": "говорить", "говорят": "говорить",
    "думаю": "думать", "думает": "думать", "думают": "думать",
    "вижу": "видеть", "видит": "видеть", "видят": "видеть",
    "слышу": "слышать", "слышит": "слышать",
    "читаю": "читать", "читает": "читать", "читал": "читать",
    "пишу": "писать", "пишет": "писать", "писал": "писать",
    "рисую": "рисовать", "рисовать": "рисовать", "рисует": "рисовать",
    "живу": "жить", "живёт": "жить", "живет": "жить", "живут": "жить",
    "работаю": "работать", "работает": "работать",
    "учусь": "учиться", "учится": "учиться",
    "иду": "идти", "идёт": "идти", "идет": "идти", "идут": "идти",
    "приду": "прийти", "придёт": "прийти", "придет": "прийти",
    "пойду": "пойти", "пойдёт": "пойти", "пойдет": "пойти",
    "нашёл": "найти", "нашла": "найти", "нашел": "найти", "нашли": "найти",
    "дал": "дать", "дала": "дать", "дали": "дать", "даёт": "дать", "дает": "дать",
    "взял": "взять", "взяла": "взять", "взяли": "взять",
    "стал": "стать", "стала": "стать", "стали": "стать",
    "сказал": "сказать", "сказала": "сказать", "сказали": "сказать",
    "спросил": "спросить", "спросила": "спросить",
    "ответил": "ответить", "ответила": "ответить",
    "помог": "помочь", "помогла": "помочь",
    "планируют": "планировать", "планирую": "планировать",
    "пожертвовали": "пожертвовать",
    "преодолевает": "преодолевать",
    "направьте": "направить",
    "составить": "составить",
    "построить": "построить",
    "мирной": "мирный", "тихой": "тихий",
    "благотворительный": "благотворительный",
    "шекспира": "шекспир",
}


def stems(word: str) -> set[str]:
    """Return stem variants for matching inflected forms."""
    w = word.lower().replace("ё", "е")
    result = {w}
    if w in IRREGULAR_FORMS:
        result.add(IRREGULAR_FORMS[w])
    # Generate stems by stripping suffixes
    for suf in INFLECTION_SUFFIXES:
        if len(w) > len(suf) + 2 and w.endswith(suf):
            result.add(w[: -len(suf)])
    # Also add progressively shorter prefixes (min 3 chars)
    for length in range(len(w), max(2, len(w) - 4), -1):
        result.add(w[:length])
    return result


def build_form_index(lemmas: list[str]) -> dict[str, set[str]]:
    """Map each token stem -> set of known lemmas it could belong to."""
    index: dict[str, set[str]] = defaultdict(set)
    for lemma in lemmas:
        for s in stems(lemma):
            index[s].add(lemma)
    return index


from collections import defaultdict  # noqa: E402 — used above


def token_matches_lemma(token: str, lemma: str) -> bool:
    tok = token.lower().replace("ё", "е")
    lem = lemma.lower().replace("ё", "е")
    if tok == lem:
        return True
    if lem in tok or tok in lem:
        return True
    tok_stems = stems(tok)
    lem_stems = stems(lem)
    if tok_stems & lem_stems:
        return True
    if tok in IRREGULAR_FORMS and IRREGULAR_FORMS[tok].replace("ё", "е") == lem:
        return True
    if lem in IRREGULAR_FORMS.values():
        for form, base in IRREGULAR_FORMS.items():
            if base.replace("ё", "е") == lem and form.replace("ё", "е") == tok:
                return True
    # Verb reflexive
    if lem.endswith("ся") or lem.endswith("сь"):
        base = lem.rstrip("ся").rstrip("ь")
        if tok.startswith(base[: max(3, len(base) - 2)]):
            return True
    # Prefix match for long lemmas
    min_len = min(4, len(lem))
    if len(lem) >= 4 and tok.startswith(lem[:min_len]):
        return True
    if len(tok) >= 4 and lem.startswith(tok[:min_len]):
        return True
    return False


def token_known(token: str, known_lemmas: set[str]) -> bool:
    tok = token.lower()
    if tok in RUSSIAN_STOP:
        return True
    if tok in IRREGULAR_FORMS and IRREGULAR_FORMS[tok] in known_lemmas:
        return True
    for lemma in known_lemmas:
        if token_matches_lemma(tok, lemma):
            return True
    return False


def normalize_gloss_part(part: str) -> str:
    return part.strip().lower().rstrip(".")


def parse_gloss_parts(gloss: str) -> list[str]:
    parts: list[str] = []
    for chunk in re.split(r"[,;]", gloss):
        chunk = chunk.strip()
        if chunk:
            parts.append(chunk)
    return parts


def gloss_issues(lemma: str, gloss: str) -> list[str]:
    issues: list[str] = []
    if not gloss or not gloss.strip():
        issues.append("gloss:empty")
        return issues

    parts = [normalize_gloss_part(p) for p in parse_gloss_parts(gloss)]
    bare_parts = [re.sub(r"\([^)]*\)", "", p).strip() for p in parts]

    if len(bare_parts) >= 2:
        seen: set[str] = set()
        for bp in bare_parts:
            if bp in seen:
                issues.append("gloss:duplicate")
                break
            seen.add(bp)

    for p in parts:
        for w in LATIN_WORD.findall(p):
            if w.lower() in ARCHAIC_LATIN:
                issues.append(f"gloss:archaic_latin:{w.lower()}")

    bad = BAD_GLOSS_PAIRS.get(lemma.lower(), set())
    if bad and len(bare_parts) >= 2:
        for bp in bare_parts[1:]:
            for bw in bad:
                if bw in bp.split():
                    issues.append(f"gloss:wrong_second_sense:{bp}")

    return issues


def lemma_in_example(lemma: str, example: str) -> bool:
    if not example:
        return False
    tokens = tokenize_russian(example)
    for tok in tokens:
        if token_matches_lemma(tok, lemma):
            return True
    ex_lower = example.lower().replace("ё", "е")
    lem_lower = lemma.lower().replace("ё", "е")
    if lem_lower in ex_lower:
        return True
    stem = lem_lower[: max(4, len(lem_lower) - 2)]
    if len(stem) >= 3 and stem in ex_lower:
        return True
    return False


def is_grammar_drill(example: str) -> bool:
    ex = example.strip()
    for pat in DRILL_PATTERNS:
        if pat.match(ex):
            return True
    return False


def tokenize_russian(text: str) -> list[str]:
    return CYR_WORD.findall(text)


def content_word_issues(
    lemma: str,
    example: str,
    known_lemmas: set[str],
    leftover_tokens: set[str],
) -> list[str]:
    issues: list[str] = []
    for tok in tokenize_russian(example):
        tl = tok.lower()
        if tl in RUSSIAN_STOP:
            continue
        if token_matches_lemma(tok, lemma):
            continue
        if token_known(tok, known_lemmas):
            continue
        if tl in leftover_tokens:
            continue
        if tl.replace("ё", "е") in leftover_tokens:
            continue
        # Allow proper names (capitalized in source)
        if tok[0].isupper() and len(tok) > 1:
            continue
        issues.append(f"vocab:unknown:{tl}")
    return issues


def grammar_issues(lemma: str, example: str) -> list[str]:
    issues: list[str] = []
    if is_grammar_drill(example):
        issues.append("grammar:drill")
    if re.search(r"\bо\s+истори", example, re.I):
        issues.append("grammar:о_истории")
    if re.search(r"ждать\s+на\b", example, re.I):
        issues.append("grammar:ждать_на")
    # Missing ё in common words
    yo_checks = [
        (r"\bшел\b", "grammar:missing_yo:шел"),
        (r"\bпошел\b", "grammar:missing_yo:пошел"),
        (r"\bпришел\b", "grammar:missing_yo:пришел"),
        (r"\bушел\b", "grammar:missing_yo:ушел"),
        (r"\bждет\b", "grammar:missing_yo:ждет"),
        (r"\bидет\b", "grammar:missing_yo:идет"),
        (r"\bсвоем\b", "grammar:missing_yo:своем"),
        (r"\bчерный\b", "grammar:missing_yo:черный"),
        (r"\bчерная\b", "grammar:missing_yo:черная"),
        (r"\bее\b", "grammar:missing_yo:ее"),
        (r"\bвсе\b", "grammar:missing_yo:все"),  # only when meaning "everything"
    ]
    for pattern, tag in yo_checks:
        if re.search(pattern, example, re.I):
            issues.append(tag)
    return issues


def place_mentions(example: str) -> list[str]:
    return [t.lower() for t in tokenize_russian(example) if t.lower() in PLACE_WORDS]


def main() -> None:
    known_lemmas: list[str] = []
    leftover_tokens: set[str] = set()

    for path in PRIOR:
        for card in cards_from_path(path):
            known_lemmas.append(lemma_from_card(card))
            qfn = (card.get("qMdFootnote") or "").strip()
            for tok in tokenize_russian(qfn):
                leftover_tokens.add(tok.lower())
                leftover_tokens.add(tok.lower().replace("ё", "е"))

    known_set = set(known_lemmas)
    target_cards = cards_from_path(TARGET)
    assert len(target_cards) == 500

    results: list[dict] = []
    place_counter: Counter[str] = Counter()
    running_lemmas = list(known_lemmas)
    running_set = set(running_lemmas)
    running_leftover = set(leftover_tokens)

    for idx, card in enumerate(target_cards, 1):
        lemma = lemma_from_card(card)
        gloss = (card.get("aMdBody") or "").strip()
        q_fn = (card.get("qMdFootnote") or "").strip()
        a_fn = (card.get("aMdFootnote") or "").strip()

        card_issues: list[str] = []
        card_issues.extend(gloss_issues(lemma, gloss))

        if not lemma_in_example(lemma, q_fn):
            card_issues.append("example:missing_lemma")

        card_issues.extend(grammar_issues(lemma, q_fn))
        card_issues.extend(
            content_word_issues(lemma, q_fn, running_set, running_leftover)
        )

        for p in place_mentions(q_fn):
            place_counter[p] += 1

        running_lemmas.append(lemma)
        running_set.add(lemma)
        for tok in tokenize_russian(q_fn):
            running_leftover.add(tok.lower())
            running_leftover.add(tok.lower().replace("ё", "е"))

        card_issues = list(dict.fromkeys(card_issues))
        results.append({
            "index": idx,
            "lemma": lemma,
            "gloss": gloss,
            "q_footnote": q_fn,
            "a_footnote": a_fn,
            "issues": card_issues,
        })

    # Variety: flag repetitive places (3+ uses in this deck)
    repetitive = {p for p, c in place_counter.items() if c >= 3}
    for r in results:
        for p in place_mentions(r["q_footnote"]):
            if p in repetitive:
                tag = f"variety:repetitive_place:{p}"
                if tag not in r["issues"]:
                    r["issues"].append(tag)

    fix_lemmas = {r["lemma"]: r["issues"] for r in results if r["issues"]}
    ok_lemmas = [r["lemma"] for r in results if not r["issues"]]

    # Issue breakdown
    issue_counts: Counter[str] = Counter()
    for issues in fix_lemmas.values():
        for iss in issues:
            if iss.startswith("vocab:"):
                issue_counts["vocab:unknown"] += 1
            elif iss.startswith("gloss:"):
                issue_counts[":".join(iss.split(":")[:2])] += 1
            else:
                issue_counts[iss.split(":")[0] + (":" + iss.split(":")[1] if ":" in iss else "")] += 1

    print("=" * 60)
    print("DECK 15260188 FIXUP ANALYSIS")
    print("=" * 60)
    print(f"Total cards: {len(target_cards)}")
    print(f"Prior vocabulary: {len(known_lemmas)} lemmas")
    print(f"Cards needing changes: {len(fix_lemmas)}")
    print(f"Cards OK: {len(ok_lemmas)}")
    print()
    print("Issue breakdown:")
    for k, v in issue_counts.most_common():
        print(f"  {k}: {v}")
    print()
    print("Place repetition in this deck (>=2):")
    for p, c in place_counter.most_common():
        if c >= 2:
            print(f"  {p}: {c}")
    print()

    print("=" * 60)
    print("ALL LEMMAS NEEDING FIXES")
    print("=" * 60)
    for r in results:
        if not r["issues"]:
            continue
        issue_str = "; ".join(r["issues"])
        print(f"[{r['index']:3d}] {r['lemma']}")
        print(f"  issues: {issue_str}")
        print(f"  gloss: {r['gloss']}")
        print(f"  RU: {r['q_footnote']}")
        if r.get("a_footnote"):
            print(f"  EN: {r['a_footnote']}")
        print()

    print("=" * 60)
    print(f"OK CARDS ({len(ok_lemmas)})")
    print("=" * 60)
    ok_results = [r for r in results if not r["issues"]]
    for i in range(0, len(ok_results), 20):
        chunk = ok_results[i : i + 20]
        line = ", ".join(f"{r['index']}:{r['lemma']}" for r in chunk)
        print(f"  {line}")

    out = {
        "total": len(target_cards),
        "needs_fix": len(fix_lemmas),
        "ok": len(ok_lemmas),
        "fix_lemmas": fix_lemmas,
        "ok_lemmas": ok_lemmas,
        "place_counter": dict(place_counter),
        "issue_counts": dict(issue_counts),
        "results": results,
    }
    Path("_analyze_deck_15260188_output.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print()
    print("(JSON: _analyze_deck_15260188_output.json)")


if __name__ == "__main__":
    main()
