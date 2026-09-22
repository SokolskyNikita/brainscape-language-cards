#!/usr/bin/env python3
"""Rewrite english_russian deck_15260281_03 (cards 301-400, band 7000->7500)."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PACK = ROOT / "english_russian"
sys.path.insert(0, str(ROOT))

from brainscape.cards import card_write_payload, cards_from_path, cards_match
from english_russian._chunk_io import write_csv

SRC = PACK / "_chunks" / "deck_15260281_03.csv"
OUT = PACK / "_chunks" / "fixed" / "deck_15260281_03.csv"
LOG = PACK / "_chunks" / "logs" / "deck_15260281_03.txt"

FUNCTION_EN = {
    "a", "an", "the", "is", "be", "i", "you", "he", "she", "it", "we", "they",
    "my", "and", "or", "in", "on", "at", "to", "of", "for", "with", "from",
    "not", "his", "him", "her", "their", "them", "our", "us", "me", "am",
    "are", "was", "were", "been", "being", "this", "that", "these", "those",
    "as", "by", "into", "about", "than", "then", "so", "if", "but", "its",
    "your", "do", "does", "did", "will", "would", "can", "could", "may",
    "might", "should", "must", "there", "here", "has", "had", "have",
    "don't", "dont", "let's", "lets", "all", "off", "done", "very", "too",
    "now", "today", "yesterday", "tomorrow", "some", "any", "no", "yes",
    "please", "more", "most", "less", "much", "many", "few", "such", "also",
    "only", "even", "still", "already", "always", "never", "often", "once",
    "after", "before", "under", "over", "through", "between", "without",
    "who", "what", "when", "where", "why", "how", "which", "just", "best",
    "better", "indeed", "himself", "herself", "itself", "myself", "yourself",
    "im", "dont", "cant", "didnt", "wont", "isnt",
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
    "них", "него", "нее", "ней", "ним", "можно", "нужно", "нужна", "нужен",
    "должен", "должна", "должно", "должны", "хорошо", "плохо", "очень",
    "сейчас", "теперь", "сегодня", "вчера", "завтра", "один", "одна",
    "одно", "сам", "сама", "само", "сами",
}

allow_en = {
    line.strip().lower()
    for line in (PACK / "_vocab" / "allow_en_15260281.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_ru = {
    line.strip().replace("ё", "е").lower()
    for line in (PACK / "_vocab" / "allow_ru_15260281.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_en |= FUNCTION_EN
allow_ru |= FUNCTION_RU

# New lemmas introduced by corrections (taught on this card).
allow_ru |= {"подло", "ставрополь", "персик"}

# (en_lemma, en_ex, ru_lemma, ru_ex)
FIXED = [
    ("agility", "Her agility impressed the coach.", "ловкость", "Её ловкость произвела впечатление на тренера."),
    ("all-union", "The all-union conference starts tomorrow.", "всесоюзный", "Всесоюзная конференция начинается завтра."),
    ("transplant", "She needs a heart transplant soon.", "пересадка", "Ей скоро нужна пересадка сердца."),
    ("inflate", "They used a pump to inflate it.", "надуть", "Они использовали насос, чтобы надуть это."),
    ("restrain oneself", "He could not restrain himself.", "сдержаться", "Он не смог сдержаться."),
    ("prostitution", "Prostitution is illegal in many countries.", "проституция", "Проституция незаконна во многих странах."),
    ("to be imbued with", "She seemed to be imbued with optimism.", "проникнуться", "Она казалась проникшейся оптимизмом."),
    ("steam", "This is a steam engine.", "паровой", "Это паровой двигатель."),
    ("flotilla", "A flotilla sailed into the harbor.", "флотилия", "Флотилия идёт в гавань."),
    ("hard drive", "My hard drive is full.", "винчестер", "Мой винчестер заполнен."),
    ("to be pronounced", "This word is to be pronounced slowly.", "произноситься", "Это слово должно произноситься медленно."),
    ("cubic", "The room is ten cubic meters.", "кубический", "Комната - десять кубических метров."),
    ("giggle", "They giggle quietly.", "хихикать", "Они тихо хихикают."),
    ("bathing", "She enjoys bathing in the lake.", "купание", "Она любит купание в озере."),
    ("microdistrict", "We live in a cozy microdistrict.", "микрорайон", "Мы живем в уютном микрорайоне."),
    ("gynecologist", "She visited her gynecologist annually.", "гинеколог", "Она посетила своего гинеколога."),
    ("reprimand", "He received a reprimand at work.", "выговор", "Он получил выговор на работе."),
    ("little restaurant", "We found a cozy little restaurant.", "ресторанчик", "Мы нашли уютный ресторанчик."),
    ("stylish", "She wore a stylish dress.", "стильный", "На ней было стильное платье."),
    ("underhandedly", "He underhandedly took her work.", "подло", "Он подло взял её работу."),
    ("pipeline", "The pipeline transports gas.", "трубопровод", "По трубопроводу идёт газ."),
    ("Stavropol", "I visited Stavropol last summer.", "Ставрополь", "Я посетил Ставрополь прошлым летом."),
    ("caricature", "I see a caricature.", "карикатура", "Я вижу карикатуру."),
    ("troupe", "The troupe performed well.", "труппа", "Труппа хорошо выступила."),
    ("sullenly", "He stared sullenly into the distance.", "угрюмо", "Он угрюмо смотрел вдаль."),
    ("earthen", "The earthen pot held fresh water.", "земляной", "Земляной горшок содержал свежую воду."),
    ("call back", "Please call back tomorrow morning.", "перезвонить", "Пожалуйста, перезвоните завтра утром."),
    ("bargain", "We will bargain for a good price.", "торговаться", "Мы будем торговаться за хорошую цену."),
    ("bun", "She has a sweet bun.", "булочка", "У неё сладкая булочка."),
    ("chapel", "They married in a chapel.", "часовня", "Они поженились в часовне."),
    ("conservatory", "She studies piano at the conservatory.", "консерватория", "Она учит пианино в консерватории."),
    ("tier", "The cake had three tiers.", "ярус", "Торт состоял из трех ярусов."),
    ("predestine", "Fate seemed to predestine their meeting.", "предопределить", "Судьба, казалось, предопределила их встречу."),
    ("dampness", "The dampness filled the old basement.", "сырость", "Сырость заполнила старый подвал."),
    ("aria", "This aria is beautiful.", "ария", "Эта ария прекрасна."),
    ("monsieur", "Monsieur, your table is ready.", "месье", "Месье, ваш стол готов."),
    ("hangar", "This is a large hangar.", "ангар", "Это большой ангар."),
    ("loader", "The loader lifted the heavy box.", "грузчик", "Грузчик поднял большой ящик."),
    ("Mediterranean", "I love the Mediterranean Sea.", "средиземный", "Я люблю Средиземное море."),
    ("to interrogate", "Police will interrogate him.", "допрашивать", "Полиция будет его допрашивать."),
    ("cache", "They found a hidden cache underground.", "тайник", "Они нашли тайник под землей."),
    ("pact", "They signed a peace pact yesterday.", "пакт", "Они подписали мирный пакт вчера."),
    ("to foreshadow", "Dark clouds foreshadow a storm.", "предвещать", "Тёмные облака предвещают бурю."),
    ("to languish", "He began to languish alone.", "томиться", "Он начал томиться один."),
    ("frankness", "Her frankness won my trust.", "откровенность", "Её откровенность завоевала моё доверие."),
    ("peach", "She has a sweet peach.", "персик", "У неё сладкий персик."),
    ("to revive", "Plants began to revive after rain.", "оживать", "Растения начали оживать после дождя."),
    ("to be derived", "This word is derived from that.", "выводиться", "Это слово выводится из этого."),
    ("to tear out", "He will tear out the page.", "вырывать", "Он вырывает страницу."),
    ("to swim by", "I watched the fish swim by.", "проплывать", "Я смотрел, как рыба проплывает мимо."),
    ("figurative", "She spoke in figurative language.", "образный", "Она говорила образным языком."),
    ("pardon", "Pardon, could you repeat that?", "пардон", "Пардон, не могли бы вы повторить это?"),
    ("differentiation", "Differentiation is important in marketing.", "дифференциация", "Дифференциация важна в маркетинге."),
    ("informatization", "Informatization is important.", "информатизация", "Информатизация важна."),
    ("a few", "I have a few books.", "несколько", "У меня есть несколько книг."),
    ("Karelian", "She cooked Karelian pies.", "карельский", "Она приготовила карельские пироги."),
    ("spread out", "The blanket was spread out.", "раскинуть", "Одеяло было раскинуто."),
    ("genocide", "Genocide is a crime against humanity.", "геноцид", "Геноцид - преступление против человечества."),
    ("infantryman", "The infantryman advanced cautiously.", "пехотинец", "Пехотинец осторожно продвигался вперёд."),
    ("resilience", "I see her resilience.", "стойкость", "Я вижу её стойкость."),
    ("titan", "He is a titan.", "титан", "Он титан."),
    ("centennial", "This oak is centennial.", "вековой", "Этот дуб вековой."),
    ("falsification", "The investigation found falsification.", "фальсификация", "Расследование нашло фальсификацию."),
    ("endless", "The desert seemed endless.", "нескончаемый", "Пустыня казалась нескончаемой."),
    ("Fritz", "Fritz was a German soldier.", "фриц", "Фриц был немецким солдатом."),
    ("carbine", "He took his carbine carefully.", "карабин", "Он осторожно взял свой карабин."),
    ("pileup", "There is a large pileup.", "завал", "Есть большой завал."),
    ("pour out", "She will pour out the sugar.", "высыпать", "Она высыпет сахар."),
    ("vulnerability", "I know his vulnerability.", "уязвимость", "Я знаю его уязвимость."),
    ("scatterbrained", "He is scatterbrained.", "рассеянный", "Он рассеянный."),
    ("smooth surface", "I see a smooth surface.", "гладь", "Я вижу гладь."),
    ("antibiotic", "She took an antibiotic for her infection.", "антибиотик", "Она приняла антибиотик от своей инфекции."),
    ("bosom", "This is nature's bosom.", "лоно", "Это лоно природы."),
    ("tundra", "The tundra is vast.", "тундра", "Тундра обширная."),
    ("pasta", "I am cooking pasta for dinner.", "макароны", "Я готовлю макароны на ужин."),
    ("canopy", "The canopy provided shade.", "навес", "Навес обеспечивал тень."),
    ("mythological", "He is a mythological Greek god.", "мифологический", "Он мифологический греческий бог."),
    ("to snicker", "They began to snicker quietly.", "посмеиваться", "Они начали тихо посмеиваться."),
    ("to stabilize", "Prices will stabilize.", "устояться", "Цены устоятся."),
    ("involvement", "I know his involvement.", "причастность", "Я знаю его причастность."),
    ("little bag", "She found coins in the little bag.", "мешочек", "Она нашла монеты в мешочке."),
    ("not necessarily", "It's not necessarily a good option.", "необязательно", "Это необязательно хороший вариант."),
    ("radio operator", "The radio operator sent a signal.", "радист", "Радист отправил сигнал."),
    ("in a low voice", "She spoke in a low voice.", "вполголоса", "Она говорила вполголоса."),
    ("facial", "He has a facial wound.", "лицевой", "У него лицевая рана."),
    ("to observe", "Remember to observe the rules.", "соблюсти", "Не забудьте соблюсти правила."),
    ("console", "I bought a new gaming console.", "приставка", "Я купил новую игровую приставку."),
    ("prosthesis", "He received his leg prosthesis yesterday.", "протез", "Он получил свой протез ноги вчера."),
    ("sentimental", "She kept the letter for sentimental reasons.", "сентиментальный", "Она сохранила письмо по сентиментальным причинам."),
    ("to be sad", "I don't want to be sad.", "грустить", "Я не хочу грустить."),
    ("despondency", "Her eyes reflected deep despondency.", "уныние", "В её глазах отражалось глубокое уныние."),
    ("telegraph", "They used the telegraph.", "телеграф", "Они использовали телеграф."),
    ("interrelated", "All systems are deeply interrelated.", "взаимосвязанный", "Все системы глубоко взаимосвязаны."),
    ("tiresome", "This task is tiresome indeed.", "утомительный", "Эта задача действительно утомительная."),
    ("guiltily", "She looked at me guiltily.", "виновато", "Она виновато посмотрела на меня."),
    ("hygiene", "Personal hygiene is very important.", "гигиена", "Личная гигиена очень важна."),
    ("frontal", "This is a frontal attack.", "лобовой", "Это лобовая атака."),
    ("insolvency", "The company declared insolvency.", "несостоятельность", "Компания объявила о несостоятельности."),
    ("formality", "It's just a formality now.", "формальность", "Это просто формальность."),
    ("chick", "The chick is small.", "птенец", "Птенец маленький."),
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
    "wore": "wear",
    "won": "win",
    "held": "hold",
    "sang": "sing",
    "began": "begin",
    "sent": "send",
    "bought": "buy",
    "kept": "keep",
    "found": "find",
    "grew": "grow",
    "said": "say",
    "told": "tell",
    "left": "leave",
    "knew": "know",
    "thought": "think",
    "felt": "feel",
    "heard": "hear",
    "stood": "stand",
    "sat": "sit",
    "ran": "run",
    "wrote": "write",
    "read": "read",
    "led": "lead",
    "paid": "pay",
    "built": "build",
    "caught": "catch",
    "taught": "teach",
    "fought": "fight",
    "chosen": "choose",
    "driven": "drive",
    "given": "give",
    "seen": "see",
    "taken": "take",
    "done": "do",
    "been": "be",
    "had": "have",
    "did": "do",
    "was": "be",
    "were": "be",
    "has": "have",
    "does": "do",
    "lives": "live",
    "needs": "need",
    "used": "use",
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
    "идет": "идти",
    "идёт": "идти",
    "идут": "идти",
    "шел": "идти",
    "шёл": "идти",
    "шла": "идти",
    "шли": "идти",
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
