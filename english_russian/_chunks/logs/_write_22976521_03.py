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

SRC = PACK / "_chunks" / "deck_22976521_03.csv"
OUT = PACK / "_chunks" / "fixed" / "deck_22976521_03.csv"
LOG = PACK / "_chunks" / "logs" / "deck_22976521_03.txt"

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
    "can't", "cannot", "won't", "must", "should", "please", "now", "today",
    "down", "up", "out", "over", "again", "once", "every", "each", "more",
    "most", "some", "any", "no", "yes", "let", "how", "when", "where",
    "why", "who", "what", "which",
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
    "есть", "быть", "уже", "еще", "ещё", "также", "тоже", "только", "вот",
    "ведь", "ну", "все", "всех", "всего", "всем", "всем", "всём", "здесь",
    "тут", "там", "давай", "давайте", "как", "что", "чтобы", "когда",
    "если", "где", "чем", "кто", "них", "него", "нее", "ней", "ним",
    "очень", "слишком", "пусть",
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
    ("yawn, gape", "I can't stop yawning today.", "зевать", "Я не могу перестать зевать сегодня."),
    ("assistant, aide", "The assistant is here.", "ассистент", "Ассистент здесь."),
    ("preschool, pre-school", "This is preschool education.", "дошкольный", "Это дошкольное образование."),
    ("argumentation, reasoning", "His argumentation was clear.", "аргументация", "Его аргументация была ясной."),
    ("tribunal, court", "The tribunal will decide.", "трибунал", "Трибунал решит."),
    ("twilight, semi-darkness", "Twilight filled the room.", "полумрак", "Полумрак наполнил комнату."),
    ("purposeful, goal-oriented", "Her steps were purposeful.", "целенаправленный", "Её шаги были целенаправленными."),
    ("pathological, morbid", "He showed pathological jealousy.", "патологический", "Он проявил патологическую ревность."),
    ("lyceum, lycee", "She finished the lyceum last year.", "лицей", "Она окончила лицей в прошлом году."),
    ("look around, examine", "I looked around the room.", "осмотреться", "Я осмотрелся в комнате."),
    ("foul, rotten", "The smell was truly foul.", "поганый", "Запах был по-настоящему поганый."),
    ("pit, dig", "The pit is deep.", "яма", "Яма глубокая."),
    ("neglect, disregard", "Neglect can lead to failure.", "пренебрежение", "Пренебрежение может привести к неудаче."),
    ("to photograph, to take a picture", "I want to photograph the sunset.", "сфотографировать", "Я хочу сфотографировать закат."),
    ("soapy, soap", "The water felt soapy.", "мыльный", "Вода была мыльной."),
    ("to arrive, to fly in", "The plane will arrive soon.", "прилетать", "Самолёт скоро прилетит."),
    ("impressive, spectacular", "Her performance was impressive.", "эффектный", "Её выступление было эффектным."),
    ("to chat, to talk", "They sat down to chat.", "побеседовать", "Они сели побеседовать."),
    ("reinforced, strengthened", "The bridge was reinforced with steel.", "усиленный", "Мост был усилен сталью."),
    ("to get mixed, to blend", "The paints got mixed.", "смешаться", "Краски смешались."),
    ("Yaroslavl, Yaroslavsky", "This is a Yaroslavl street.", "ярославский", "Это ярославская улица."),
    ("nightmarish, terrible", "It was a nightmarish night.", "кошмарный", "Это была кошмарная ночь."),
    ("self-esteem, self-assessment", "His self-esteem is low.", "самооценка", "Его самооценка низкая."),
    ("socialist", "He is a socialist.", "социалист", "Он социалист."),
    ("treasure, stash", "They found ancient treasure.", "клад", "Они нашли древний клад."),
    ("profitable, lucrative", "This business is profitable.", "прибыльный", "Этот бизнес прибыльный."),
    ("precaution, precautionary measure", "This precaution is important.", "предосторожность", "Эта предосторожность важна."),
    ("Czech, Czech person", "He is a Czech.", "чех", "Он чех."),
    ("hamlet, farmstead", "They live in a quiet hamlet.", "хутор", "Они живут в тихом хуторе."),
    ("stretcher, litter", "They carried him on a stretcher.", "носилки", "Они несли его на носилках."),
    ("stem, stalk", "The flower's stem is thin.", "стебель", "Стебель цветка тонкий."),
    ("considerable, decent", "She has considerable talent.", "изрядный", "У неё изрядный талант."),
    ("gravitational, gravity", "Gravitational force is strong.", "гравитационный", "Гравитационная сила сильная."),
    ("turn, coil", "The wire made another turn.", "виток", "Провод сделал ещё один виток."),
    ("conversational, colloquial", "She prefers conversational English.", "разговорный", "Она предпочитает разговорный английский."),
    ("vegetation, flora", "The vegetation is thick here.", "растительность", "Здесь густая растительность."),
    ("painting, decoration", "She admired the painting on the vase.", "роспись", "Она восхищалась росписью на вазе."),
    ("heel, fifth", "His heel hurts.", "пята", "Его пята болит."),
    ("comma", "Use a comma here.", "запятая", "Поставьте здесь запятую."),
    ("naively, naive", "She naively trusted the stranger.", "наивно", "Она наивно доверилась незнакомцу."),
    ("beachhead, bridgehead", "They took the beachhead.", "плацдарм", "Они заняли плацдарм."),
    ("little man, peasant", "The little man smiled.", "мужичок", "Мужичок улыбнулся."),
    ("cynical", "He is cynical about everything.", "циничный", "Он циничен во всём."),
    ("embody, incarnate", "She embodies strength.", "воплощать", "Она воплощает силу."),
    ("to change, to replace", "I need to change my clothes.", "сменять", "Мне нужно сменить одежду."),
    ("inspire, motivate", "Music can inspire me.", "вдохновлять", "Музыка может вдохновлять меня."),
    ("knit, tie", "She loves to knit a scarf.", "вязать", "Она любит вязать шарф."),
    ("immediately, without delay", "Call the doctor immediately!", "незамедлительно", "Позвоните врачу незамедлительно!"),
    ("rubber, eraser", "This is rubber.", "резина", "Это резина."),
    ("recovery, collection", "Debt recovery began.", "взыскание", "Взыскание долга началось."),
    ("delay, procrastinate", "Don't delay the answer.", "медлить", "Не медли с ответом."),
    ("transmitter, sender", "The transmitter is working.", "передатчик", "Передатчик работает."),
    ("scratch, scrape", "He got a scratch on his arm.", "царапина", "У него царапина на руке."),
    ("paste, pasta", "Apply the paste to the skin.", "паста", "Нанесите пасту на кожу."),
    ("bend, curve", "I can bend the wire.", "согнуть", "Я могу согнуть провод."),
    ("urgently, insistently", "He insistently asked for an answer.", "настоятельно", "Он настоятельно просил ответа."),
    ("to contract, to shrink", "Metals contract in the cold.", "сжиматься", "Металлы сжимаются на холоде."),
    ("to make an effort, to trouble oneself", "He decided to make an effort.", "потрудиться", "Он решил потрудиться."),
    ("bankrupt, ruin", "The war will ruin the country.", "разорить", "Война разорит страну."),
    ("mountaineer, climber", "The mountaineer reached the top.", "альпинист", "Альпинист достиг вершины."),
    ("to strain, to tense up", "I had to strain to hear her.", "напрягаться", "Мне пришлось напрягаться, чтобы услышать её."),
    ("disintegrate, fall apart", "The bread will disintegrate in water.", "распадаться", "Хлеб распадётся в воде."),
    ("ugly, nasty", "The pattern was truly ugly.", "гадкий", "Узор был по-настоящему гадкий."),
    ("innovation, novelty", "This innovation will help us.", "новшество", "Это новшество нам поможет."),
    ("shadow, shadowy", "He works in the shadow economy.", "теневой", "Он работает в теневой экономике."),
    ("audio, sound", "I listened to the audio.", "аудио", "Я слушал аудио."),
    ("gangway, ramp", "Clear the gangway for passengers.", "трап", "Освободите трап для пассажиров."),
    ("secretly, covertly", "She secretly admired him.", "тайком", "Она тайком восхищалась им."),
    ("to swear, to curse", "He began to swear loudly.", "материться", "Он начал громко материться."),
    ("to neigh, to bray", "The horse began to neigh.", "ржать", "Лошадь начала ржать."),
    ("dissimilar, unlike", "Their opinions are dissimilar.", "непохожий", "Их мнения непохожи."),
    ("disappointment, chagrin", "His failure was a deep disappointment.", "огорчение", "Его неудача была глубоким огорчением."),
    ("rod, bar", "I found a rod.", "прут", "Я нашёл прут."),
    ("to exhaust, to torment", "The long road exhausted him.", "измучить", "Долгая дорога измучила его."),
    ("chancellor, prime minister", "The chancellor spoke today.", "канцлер", "Канцлер говорил сегодня."),
    ("Jewish, Judaic", "He went to a Jewish service.", "иудейский", "Он пошёл на иудейскую службу."),
    ("cube, block", "I see a cube.", "куб", "Я вижу куб."),
    ("electorate, voters", "The electorate wants change.", "электорат", "Электорат хочет перемен."),
    ("brown, dark-brown", "This is a brown bear.", "бурый", "Это бурый медведь."),
    ("clarify, elucidate", "Please clarify your question.", "прояснить", "Пожалуйста, проясните ваш вопрос."),
    ("geologist", "The geologist studied the rocks.", "геолог", "Геолог изучал породы."),
    ("juicy, succulent", "This apple is juicy.", "сочный", "Это яблоко сочное."),
    ("tour, guest performance", "The theater announced a tour.", "гастроль", "Театр объявил гастроль."),
    ("romantic, novelist", "He is a romantic.", "романтик", "Он романтик."),
    ("unsuccessfully", "He tried unsuccessfully to open the door.", "неудачно", "Он неудачно попытался открыть дверь."),
    ("judge, reason out", "Let him judge this matter.", "рассудить", "Пусть он рассудит это дело."),
    ("charm, enchantment", "Her smile has charm.", "очарование", "В её улыбке есть очарование."),
    ("urine, pee", "This is urine.", "моча", "Это моча."),
    ("separate, detach", "The twins decided to separate.", "отделиться", "Близнецы решили отделиться."),
    ("to mix, to blend", "Mix the flour and water.", "смешивать", "Смешивайте муку и воду."),
    ("excellent, superb", "That was excellent.", "превосходно", "Это было превосходно."),
    ("barge, lighter", "The barge floated down the river.", "баржа", "Баржа плыла по реке."),
    ("compass, compasses", "He navigated using a compass.", "компас", "Он ориентировался с помощью компаса."),
    ("whip, knout", "The whip hit him.", "кнут", "Кнут ударил его."),
    ("charming, charismatic", "He is truly charming.", "обаятельный", "Он действительно обаятельный."),
    ("Taurus, bull", "My sign is Taurus.", "телец", "Мой знак — телец."),
    ("intuitively", "She intuitively understood him.", "интуитивно", "Она интуитивно поняла его."),
    ("to resurrect, to rise again", "He will resurrect on the third day.", "воскреснуть", "Он воскреснет на третий день."),
    ("solve, decipher", "Can you solve this puzzle?", "разгадать", "Разгадайте эту загадку?"),
    ("to stride, to step", "I saw him stride forward.", "зашагать", "Я видел, как он зашагал вперёд."),
]

IRREGULAR_EN = {
    "found": "find",
    "ran": "run",
    "knew": "know",
    "cut": "cut",
    "felt": "feel",
    "sat": "sit",
    "got": "get",
    "made": "make",
    "took": "take",
    "shown": "show",
    "showed": "show",
    "dug": "dig",
    "hit": "hit",
    "began": "begin",
    "spoke": "speak",
    "saw": "see",
    "seen": "see",
    "strode": "stride",
    "understood": "understand",
    "tried": "try",
    "went": "go",
    "stopped": "stop",
    "begun": "begin",
}

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
    "видели": "видеть",
    "знаю": "знать",
    "живу": "жить",
    "нашел": "найти",
    "нашла": "найти",
    "нашёл": "найти",
    "нашли": "найти",
    "стал": "стать",
    "стала": "стать",
    "стали": "стать",
    "должен": "должный",
    "должны": "должный",
    "сели": "сесть",
    "сел": "сесть",
    "поможет": "помочь",
    "просите": "просить",
    "просил": "просить",
    "проясните": "прояснить",
    "позвоните": "позвонить",
    "поставьте": "поставить",
    "нанесите": "нанести",
    "освободите": "освободить",
    "смешивайте": "смешивать",
    "распадётся": "распадаться",
    "распадется": "распадаться",
    "воскреснет": "воскреснуть",
    "зашагал": "зашагать",
    "прилетит": "прилетать",
    "решит": "решить",
    "заняли": "занять",
    "начал": "начать",
    "начала": "начать",
    "началось": "начаться",
    "окончила": "окончить",
    "осмотрелся": "осмотреться",
    "проявил": "проявить",
    "наполнил": "наполнить",
    "выкопали": "выкопать",
    "смешались": "смешаться",
    "попал": "попасть",
    "восхищалась": "восхищаться",
    "доверилась": "довериться",
    "улыбнулся": "улыбнуться",
    "воплощает": "воплощать",
    "сменить": "сменять",
    "работает": "работать",
    "просил": "просить",
    "сжимаются": "сжиматься",
    "разорит": "разорить",
    "достиг": "достичь",
    "измучила": "измучить",
    "изучал": "изучать",
    "объявил": "объявить",
    "рассудит": "рассудить",
    "исследовал": "исследовать",
    "ориентировался": "ориентироваться",
    "почувствовал": "почувствовать",
    "поняла": "понять",
    "пошёл": "пойти",
    "пошел": "пойти",
    "разгадайте": "разгадать",
    "болит": "болеть",
    "глубокая": "глубокий",
    "ударил": "ударить",
    "хочу": "хотеть",
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
