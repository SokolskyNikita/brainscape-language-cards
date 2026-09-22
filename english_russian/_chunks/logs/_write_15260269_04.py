#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PACK = ROOT / "english_russian"
sys.path.insert(0, str(ROOT))

from brainscape.cards import card_write_payload, cards_from_path, cards_match
from english_russian._chunk_io import write_csv

SRC = PACK / "_chunks" / "deck_15260269_04.csv"
OUT = PACK / "_chunks" / "fixed" / "deck_15260269_04.csv"
LOG = PACK / "_chunks" / "logs" / "deck_15260269_04.txt"

FUNCTION_EN = {
    "a", "the", "is", "be", "i", "you", "he", "she", "it", "we", "they",
    "my", "and", "or", "in", "on", "at", "to", "of", "for", "with", "from",
    "not", "his", "him", "her", "their", "them", "our", "us", "me", "am",
    "are", "was", "were", "been", "being", "this", "that", "these", "those",
    "an", "as", "by", "into", "about", "than", "then", "so", "if", "but",
    "its", "your", "im", "dont", "cant", "lets", "didnt", "wont", "isnt",
    "there", "here", "very", "too", "now", "today", "yesterday", "tomorrow",
    "some", "any", "all", "no", "yes", "do", "does", "did", "have", "has",
    "had", "will", "would", "can", "could", "should", "must", "may", "might",
    "please", "more", "most", "less", "much", "many", "few", "such", "also",
    "only", "even", "still", "already", "always", "never", "often", "once",
    "after", "before", "under", "over", "through", "between", "without",
    "who", "what", "when", "where", "why", "how", "which",
    "himself", "herself", "itself", "themselves", "myself", "yourself",
    "just", "out", "off", "up", "down", "again", "away", "back",
}

FUNCTION_RU = {
    "я", "мне", "меня", "мной", "мой", "моя", "мое", "моё", "мои", "мою",
    "мы", "нам", "нас", "нами", "наш", "наша", "наше", "наши", "нашу",
    "ты", "тебе", "тебя", "тобой", "твой", "твоя", "твое", "твоё", "твои",
    "вы", "вам", "вас", "вами", "ваш", "ваша", "ваше", "ваши", "вашу",
    "он", "она", "оно", "они", "его", "ее", "её", "ей", "ему", "им", "их",
    "ими", "ним", "ней", "ними", "него", "нее", "неё", "них",
    "себя", "себе", "собой", "свой", "своя", "свое", "своё", "свои", "свою",
    "своим", "своего", "своей",
    "это", "эта", "этот", "эти", "этого", "этой", "этому", "этим", "этих", "эту",
    "то", "та", "тот", "те", "того", "той", "тому", "тем", "тех", "ту",
    "такой", "такая", "такое", "такие", "так",
    "не", "ни", "нет", "да", "вот", "уж", "ли", "же", "бы",
    "в", "на", "с", "со", "у", "к", "ко", "по", "из", "за", "от", "до",
    "для", "без", "при", "о", "об", "про", "над", "под", "между", "через",
    "после", "перед", "и", "а", "но", "или", "что", "как", "когда", "где",
    "чтобы", "если", "потому", "уже", "еще", "ещё", "только", "даже", "тоже",
    "также", "очень", "сейчас", "теперь", "всегда", "сегодня", "вчера", "завтра",
    "был", "была", "было", "были", "будет", "будут", "есть", "быть",
    "здесь", "тут", "там", "можно", "нужно", "должен", "должна", "должно", "должны",
    "могу", "можешь", "может", "можем", "можете", "могут",
}

allow_en = {
    line.strip().lower()
    for line in (PACK / "_vocab" / "allow_en_15260269.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
} | FUNCTION_EN
allow_ru = {
    line.strip().replace("ё", "е").lower()
    for line in (PACK / "_vocab" / "allow_ru_15260269.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
} | FUNCTION_RU

# (en_lemma, en_ex, ru_lemma, ru_ex)
FIXED = [
    ("ford", "We cross the river at the ford.", "форд", "Мы переходим реку у форда."),
    ("arch", "The arch stands in the park.", "арка", "Арка стоит в парке."),
    ("dump", "He works at the dump.", "свалка", "Он работает на свалке."),
    ("creditor", "The bank is my creditor.", "кредитор", "Банк — мой кредитор."),
    ("abundant", "The harvest is abundant.", "обильный", "Урожай обильный."),
    ("nature reserve", "We visited the nature reserve yesterday.", "заповедник", "Мы посетили заповедник вчера."),
    ("separation", "Their separation is a problem.", "разлука", "Их разлука — проблема."),
    ("mill", "The old mill is near the river.", "мельница", "Старая мельница стоит у реки."),
    ("to harass", "Do not harass her.", "приставать", "Не приставай к ней."),
    ("estimate", "Estimate the time.", "прикинуть", "Прикинь время."),
    ("lose weight", "I need to lose weight soon.", "похудеть", "Мне нужно скоро похудеть."),
    ("touching", "This is a touching story.", "трогательный", "Это трогательная история."),
    ("applicant", "The applicant has his documents.", "заявитель", "У заявителя есть документы."),
    ("volcano", "The volcano is high.", "вулкан", "Вулкан высокий."),
    ("extend", "We want to extend our vacation.", "продлить", "Мы хотим продлить наш отпуск."),
    ("systematic", "She has a systematic plan.", "систематический", "У неё систематический план."),
    ("to lay out", "She likes to lay out her things.", "выкладывать", "Она любит выкладывать свои вещи."),
    ("avant-garde", "He loves the avant-garde.", "авангард", "Он любит авангард."),
    ("variable", "Weather is always variable.", "переменный", "Погода всегда переменная."),
    ("Irkutsk", "I visited Irkutsk last summer.", "Иркутск", "Я посетил Иркутск прошлым летом."),
    ("to boil", "I need to boil an egg.", "сварить", "Мне нужно сварить яйцо."),
    ("cadet", "The cadet is young.", "курсант", "Курсант молодой."),
    ("domain", "Check the domain.", "домен", "Проверьте домен."),
    ("to pray", "She likes to pray at night.", "молиться", "Она любит молиться ночью."),
    ("hypnosis", "They use hypnosis.", "гипноз", "Они используют гипноз."),
    ("cheap", "This telephone is cheap.", "недорогой", "Этот телефон недорогой."),
    ("come to one's senses", "He finally came to his senses.", "опомниться", "Он наконец опомнился."),
    ("ink", "The pen is out of ink.", "чернила", "В ручке закончились чернила."),
    ("to defend oneself", "He needs to defend himself.", "защищаться", "Ему нужно защищаться."),
    ("to confuse", "I tried not to confuse the names.", "перепутать", "Я старался не перепутать имена."),
    ("Spaniard", "The Spaniard lives in this city.", "испанец", "Испанец живёт в этом городе."),
    ("execution by shooting", "This is an execution by shooting.", "расстрел", "Это расстрел."),
    ("generous", "He is a generous man.", "щедрый", "Он щедрый человек."),
    ("to wash", "I need to wash the dishes.", "вымыть", "Мне нужно вымыть посуду."),
    ("passionately", "She kissed him passionately.", "страстно", "Она страстно целовала его."),
    ("replenishment", "We need a replenishment of water.", "пополнение", "Нам нужно пополнение воды."),
    ("to slip", "It will slip from my hand.", "скользнуть", "Оно скользнёт с руки."),
    ("sperm", "The doctor talks about sperm.", "сперма", "Врач говорит о сперме."),
    ("squeal", "I heard a squeal.", "визг", "Я слышал визг."),
    ("anonymous", "The letter is anonymous.", "анонимный", "Письмо анонимное."),
    ("maniac", "The maniac was here yesterday.", "маньяк", "Маньяк был тут вчера."),
    ("to have dinner", "We want to have dinner at seven.", "ужинать", "Мы хотим ужинать в семь."),
    ("laser", "The laser is strong.", "лазер", "Лазер сильный."),
    ("to be prohibited", "Smoking is to be prohibited here.", "запрещаться", "Курение тут запрещается."),
    ("remake", "They want to remake the old movie.", "переделать", "Они хотят переделать старый фильм."),
    ("seam", "The seam on the dress is bad.", "шов", "Шов на платье плохой."),
    ("taxpayer", "Every taxpayer pays tax.", "налогоплательщик", "Каждый налогоплательщик платит налог."),
    ("swindler", "The swindler stole a thousand from them.", "мошенник", "Мошенник украл у них тысячу."),
    ("kinship", "They feel a deep kinship.", "родство", "Они чувствуют глубокое родство."),
    ("concession", "He made a concession for peace.", "уступка", "Он сделал уступку ради мира."),
    ("imitation", "Art is often an imitation of life.", "подражание", "Искусство часто — подражание жизни."),
    ("ensign", "The ensign is young.", "прапорщик", "Прапорщик молодой."),
    ("to lay", "She likes to lay the books.", "укладывать", "Она любит укладывать книги."),
    ("drunkenness", "His drunkenness is a problem.", "пьянство", "Его пьянство — проблема."),
    ("exhale", "Please exhale slowly.", "выдохнуть", "Пожалуйста, выдохните медленно."),
    ("thermal", "This is thermal energy.", "тепловой", "Это тепловая энергия."),
    ("get lost", "I can get lost in the forest.", "потеряться", "Я могу потеряться в лесу."),
    ("to write out", "She will write out the recipe.", "выписывать", "Она выписывает рецепт."),
    ("running", "Go home running.", "бегом", "Иди домой бегом."),
    ("forward", "Move forward.", "вперёд", "Идите вперёд."),
    ("piercing", "Her piercing look is cold.", "пронзительный", "Её пронзительный взгляд холодный."),
    ("pager", "He checked his pager.", "пейджер", "Он проверил свой пейджер."),
    ("change one's mind", "She will change her mind.", "передумать", "Она передумает."),
    ("unworthy", "He felt unworthy of her love.", "недостойный", "Он чувствовал себя недостойным её любви."),
    ("nasal", "He has a nasal voice.", "носовой", "У него носовой голос."),
    ("to undress", "She began to undress by the bed.", "раздеваться", "Она начала раздеваться у кровати."),
    ("legion", "The legion is large.", "легион", "Легион большой."),
    ("arbitration", "They want arbitration for the dispute.", "арбитраж", "Они хотят арбитраж по спору."),
    ("ravine", "There is a deep ravine.", "овраг", "Там глубокий овраг."),
    ("quantum", "This is a quantum effect.", "квантовый", "Это квантовый эффект."),
    ("to cut", "Use a knife to cut the cake.", "разрезать", "Используйте нож, чтобы разрезать торт."),
    ("awakening", "I felt an awakening.", "пробуждение", "Я почувствовал пробуждение."),
    ("pavilion", "He is at the pavilion.", "павильон", "Он у павильона."),
    ("mechanically", "She answered mechanically.", "машинально", "Она ответила машинально."),
    ("patty", "I ate a meat patty.", "пирожок", "Я съел пирожок с мясом."),
    ("condemnation", "Public condemnation was severe.", "осуждение", "Общественное осуждение было суровым."),
    ("saving", "I have a saving in the bank.", "сбережение", "У меня есть сбережение в банке."),
    ("monarchy", "The monarchy is old.", "монархия", "Монархия старая."),
    ("grape", "I love eating a grape.", "виноград", "Я люблю есть виноград."),
    ("publishing", "This is publishing work.", "издательский", "Это издательская работа."),
    ("starting", "This is the starting place.", "стартовый", "Это стартовое место."),
    ("short-term", "We need a short-term solution now.", "краткосрочный", "Нам сейчас нужно краткосрочное решение."),
    ("to be listed", "His name is listed in the book.", "значиться", "Его имя значится в книге."),
    ("vulnerable", "The city was vulnerable to attack.", "уязвимый", "Город был уязвим для атаки."),
    ("courier", "The courier delivered the package today.", "курьер", "Курьер доставил посылку сегодня."),
    ("to peer out", "She likes to peer out the window.", "выглядывать", "Она любит выглядывать в окно."),
    ("dependent", "He is dependent on her.", "зависимый", "Он зависим от неё."),
    ("break off", "He will break off the talk.", "оборвать", "Он оборвёт разговор."),
    ("inertia", "Inertia is strong.", "инерция", "Инерция сильная."),
    ("solidarity", "We stand in solidarity with you.", "солидарность", "Мы выражаем солидарность с вами."),
    ("bewilderedly", "She bewilderedly searched for her keys.", "растерянно", "Она растерянно искала свои ключи."),
    ("indifference", "His indifference hurt her.", "равнодушие", "Его равнодушие ранило её."),
    ("economically", "We must think economically.", "экономически", "Мы должны думать экономически."),
    ("display", "Check the telephone display.", "дисплей", "Проверьте дисплей телефона."),
    ("lending", "The bank specializes in lending.", "кредитование", "Банк специализируется на кредитовании."),
    ("to ripen", "The apple will ripen soon.", "созреть", "Яблоко скоро созреет."),
    ("lemon", "The lemon is in the water.", "лимон", "Лимон в воде."),
    ("cone", "The pine tree has a cone.", "шишка", "У сосны есть шишка."),
    ("wildly", "They laughed wildly.", "дико", "Они дико смеялись."),
    ("vaguely", "I vaguely remember his face.", "смутно", "Я смутно помню его лицо."),
]


def en_forms(word: str) -> set[str]:
    forms = {word}
    for suffix in ("'s", "s", "es", "ed", "ing", "ly", "er", "est"):
        if word.endswith(suffix) and len(word) > len(suffix) + 2:
            forms.add(word[: -len(suffix)])
    if word.endswith("ies") and len(word) > 4:
        forms.add(word[:-3] + "y")
    if word.endswith("ied") and len(word) > 4:
        forms.add(word[:-3] + "y")
    if word.endswith("ing") and len(word) > 5:
        forms.add(word[:-3] + "e")
    if word.endswith("ed") and len(word) > 4:
        forms.add(word[:-1])
        forms.add(word[:-2])
    if word.endswith("d") and len(word) > 4:
        forms.add(word[:-1])
    return forms


IRREGULAR_EN = {
    "made": "make", "went": "go", "gone": "go", "bought": "buy",
    "knew": "know", "known": "know", "sold": "sell", "grew": "grow",
    "grown": "grow", "took": "take", "taken": "take", "gave": "give",
    "given": "give", "saw": "see", "seen": "see", "came": "come",
    "did": "do", "done": "do", "had": "have", "said": "say",
    "told": "tell", "got": "get", "found": "find", "left": "leave",
    "kept": "keep", "felt": "feel", "thought": "think", "brought": "bring",
    "stood": "stand", "sat": "sit", "ran": "run", "won": "win",
    "lost": "lose", "met": "meet", "led": "lead", "paid": "pay",
    "spoke": "speak", "written": "write", "wrote": "write",
    "ate": "eat", "eaten": "eat", "drank": "drink", "drunk": "drink",
    "stole": "steal", "stolen": "steal", "broke": "break", "broken": "break",
    "began": "begin", "begun": "begin", "heard": "hear", "held": "hold",
    "fell": "fall", "fallen": "fall", "checked": "check",
}


def en_ok(text: str, extra: set[str]) -> list[str]:
    allowed = allow_en | extra
    bad = []
    for raw in re.findall(r"[A-Za-z']+", text):
        w = raw.lower().replace("'", "")
        if not w or w in allowed:
            continue
        if IRREGULAR_EN.get(w, "") in allowed:
            continue
        if any(form in allowed for form in en_forms(w)):
            continue
        if w.endswith("ly") and w[:-2] in allowed:
            continue
        bad.append(raw)
    return bad


RU_ENDINGS = (
    "ями", "ами", "ого", "его", "ому", "ему", "ыми", "ими",
    "ая", "яя", "ое", "ее", "ие", "ые", "ой", "ей", "ий", "ый",
    "ую", "юю", "ов", "ев", "ей", "ам", "ям", "ом", "ем",
    "ах", "ях", "ию", "ью", "ия", "ья", "ие", "ье",
    "ть", "ти", "ла", "ло", "ли", "ет", "ют", "ут", "ит", "ат", "ят",
    "ешь", "ишь", "ете", "ите", "ём", "ем", "им",
    "ёт", "ёшь",
    "а", "я", "о", "е", "у", "ю", "ы", "и",
)


def ru_stems(word: str) -> set[str]:
    stems = {word}
    for end in RU_ENDINGS:
        if word.endswith(end) and len(word) - len(end) >= 3:
            stems.add(word[: -len(end)])
    if len(word) >= 4:
        stems.add(word[:3])
        stems.add(word[:4])
    if len(word) >= 5:
        stems.add(word[:5])
    return stems


def ru_ok(text: str, extra: set[str]) -> list[str]:
    allowed = allow_ru | extra
    bad = []
    for raw in re.findall(r"[А-Яа-яЁё-]+", text):
        if raw.replace("-", "") == "":
            continue
        w = raw.replace("ё", "е").replace("Ё", "е").lower()
        if w in allowed:
            continue
        stems = ru_stems(w)
        if any(stem in allowed for stem in stems if len(stem) >= 3):
            continue
        if any(w.startswith(lemma) or lemma.startswith(w) for lemma in allowed if len(lemma) >= 3 and len(w) >= 3):
            continue
        if any(
            w[:3] == lemma[:3]
            for lemma in allowed
            if abs(len(lemma) - len(w)) <= 4 and min(len(lemma), len(w)) >= 3
        ):
            continue
        if any(stem.startswith(lemma[:4]) or lemma.startswith(stem[:4]) for lemma in allowed for stem in stems if len(lemma) >= 4 and len(stem) >= 4):
            continue
        bad.append(raw)
    return bad


def lemma_tokens_en(en: str) -> set[str]:
    parts = re.findall(r"[A-Za-z']+", en.lower().replace("(", " ").replace(")", " "))
    extra = set(parts)
    extra.discard("to")
    extra.discard("the")
    extra.discard("a")
    extra.discard("an")
    return extra


def lemma_tokens_ru(ru: str) -> set[str]:
    parts = re.findall(r"[А-Яа-яЁё-]+", ru)
    return {p.replace("ё", "е").replace("Ё", "е").lower() for p in parts}


def make_card(en: str, en_ex: str, ru: str, ru_ex: str) -> dict:
    return card_write_payload(
        {
            "qMdPrompt": "Translate:",
            "qMdBody": en,
            "qMdClarifier": "",
            "qMdFootnote": en_ex,
            "aMdPrompt": "",
            "aMdBody": ru,
            "aMdClarifier": "",
            "aMdFootnote": ru_ex,
        }
    )


def main() -> None:
    originals = cards_from_path(SRC)
    if len(originals) != 100 or len(FIXED) != 100:
        raise SystemExit(f"expected 100, got {len(originals)} / {len(FIXED)}")

    cards = []
    leftover = []
    for i, (en, en_ex, ru, ru_ex) in enumerate(FIXED, 1):
        orig = originals[i - 1]
        if orig["qMdBody"] != en:
            leftover.append(f"{i}: gloss changed {orig['qMdBody']!r} -> {en!r}")
        extra_en = lemma_tokens_en(en)
        extra_ru = lemma_tokens_ru(ru)
        for token in en_ok(en_ex, extra_en):
            leftover.append(f"{i} EN leftover {token!r}: {en_ex}")
        for token in ru_ok(ru_ex, extra_ru):
            leftover.append(f"{i} RU leftover {token!r}: {ru_ex}")
        if en.split()[0].lower() not in en_ex.lower() and en.lower() not in en_ex.lower():
            key = en.lower().replace("to ", "")
            if key not in en_ex.lower() and not any(p in en_ex.lower() for p in key.split()):
                leftover.append(f"{i}: EN example missing {en!r}")
        ru_key = ru.lower().replace("ё", "е")
        ru_ex_n = ru_ex.lower().replace("ё", "е")
        first = ru_key.split()[0]
        if first[:4] not in ru_ex_n and first[:3] not in ru_ex_n:
            leftover.append(f"{i}: RU example missing {ru!r}")
        cards.append(make_card(en, en_ex, ru, ru_ex))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    write_csv(OUT, cards)
    loaded = cards_from_path(OUT)
    if len(loaded) != 100:
        raise SystemExit(f"cards_from_path returned {len(loaded)}")

    changed = sum(1 for a, b in zip(originals, loaded) if not cards_match(a, b))
    LOG.write_text(f"{changed}\n", encoding="utf-8")
    print(f"wrote {OUT}")
    print(f"cards_from_path={len(loaded)}")
    print(f"changed={changed}")
    if leftover:
        print("LEFTOVER / CHECKS:")
        print("\n".join(leftover))


if __name__ == "__main__":
    main()
