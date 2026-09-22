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

SRC = PACK / "_chunks" / "deck_15260287_00.csv"
OUT = PACK / "_chunks" / "fixed" / "deck_15260287_00.csv"
LOG = PACK / "_chunks" / "logs" / "deck_15260287_00.txt"

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
    "ago", "ones", "two", "down", "up", "out", "off", "back",
    "herself", "himself", "themselves", "myself", "yourself",
}

FUNCTION_RU = {
    "я", "мне", "меня", "мной", "мой", "моя", "мое", "моё", "мои", "мою",
    "мы", "нам", "нас", "нами", "наш", "наша", "наше", "наши", "нашу",
    "ты", "тебе", "тебя", "тобой", "твой", "твоя", "твое", "твоё", "твои",
    "вы", "вам", "вас", "вами", "ваш", "ваша", "ваше", "ваши", "вашу",
    "он", "она", "оно", "они", "его", "ее", "её", "ей", "ему", "им", "их",
    "ими", "ним", "ней", "ними", "него", "нее", "неё",
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
    "во", "всё", "все", "всех", "всю", "весь", "двоих", "слишком", "сам", "самом",
    "из-за", "изза", "хорошо", "давай", "скоро", "часто",
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
allow_ru |= {"привыкнуть", "костистый", "дисбаланс", "чернобыль"}

# (en_lemma, en_ex, ru_lemma, ru_ex)
FIXED = [
    ("half a century", "She lived there for half a century.", "полвека", "Она жила там полвека."),
    ("to be paid", "This work is to be paid soon.", "оплачиваться", "Эта работа скоро будет оплачиваться."),
    ("interrogate", "Police will interrogate the suspect this evening.", "допросить", "Полиция допросит подозреваемого вечером."),
    ("round-the-clock", "We need round-the-clock help.", "круглосуточный", "Нам нужна круглосуточная помощь."),
    ("millionth", "This is the millionth day.", "миллионный", "Это миллионный день."),
    ("tremulous", "Her voice was tremulous.", "трепетный", "Её голос был трепетным."),
    ("forwarding", "The forwarding of the letter took a week.", "пересылка", "Пересылка письма заняла неделю."),
    ("rummage", "I will rummage through the attic.", "порыться", "Я хочу порыться на чердаке."),
    ("get used to", "You will get used to the cold.", "привыкнуть", "Ты привыкнешь к холоду."),
    ("most holy", "This is a most holy place.", "пресвятой", "Это пресвятое место."),
    ("kidnapper", "The kidnapper took him.", "похититель", "Похититель взял его."),
    ("vine", "Grapes grow on the vine.", "лоза", "Лоза даёт виноград."),
    ("lie low", "He decided to lie low for a time.", "залечь", "Он решил на время залечь на дно."),
    ("retired", "He is a retired officer.", "отставной", "Он отставной офицер."),
    ("draft", "I wrote a new draft.", "черновик", "Я написал новый черновик."),
    ("to be replaced", "The filter is replaced often.", "заменяться", "Фильтр часто заменяется."),
    ("plausible", "His story seemed plausible.", "правдоподобный", "Его история казалась правдоподобной."),
    ("International", "They sing the International.", "интернационал", "Они поют Интернационал."),
    ("meticulous", "She did meticulous work.", "кропотливый", "Она сделала кропотливую работу."),
    ("routine", "This is routine work.", "рутинный", "Это рутинная работа."),
    ("glossy", "I bought a glossy magazine.", "глянцевый", "Я купил глянцевый журнал."),
    ("penultimate", "This is the penultimate page.", "предпоследний", "Это предпоследняя страница."),
    ("den", "The bear is in its den.", "берлога", "Медведь в своей берлоге."),
    ("planetary", "This is a planetary system.", "планетарный", "Это планетарная система."),
    ("zigzag", "The path is a zigzag.", "зигзаг", "Путь - это зигзаг."),
    ("humanistic", "He has humanistic views.", "гуманистический", "У него гуманистические взгляды."),
    ("prism", "Light goes through the prism.", "призма", "Свет идёт через призму."),
    ("cloudiness", "The cloudiness increased today.", "облачность", "Облачность сегодня увеличилась."),
    ("atrocity", "War leads to atrocity.", "зверство", "Война приводит к зверству."),
    ("proportionally", "Prices grow proportionally to demand.", "пропорционально", "Цены растут пропорционально спросу."),
    ("chop down", "They will chop down the old oak.", "срубить", "Они срубят старый дуб."),
    ("to hum", "The engine hummed softly.", "загудеть", "Двигатель тихо загудел."),
    ("benefactor", "The benefactor helped the school.", "благодетель", "Благодетель помог школе."),
    ("anarchy", "Anarchy began after the war.", "анархия", "После войны началась анархия."),
    ("to be guarded", "The house is guarded at night.", "охраняться", "Дом охраняется ночью."),
    ("conscript", "He became a conscript at eighteen.", "призывник", "Он стал призывником в восемнадцать лет."),
    ("sensational", "The news was absolutely sensational.", "сенсационный", "Новость была абсолютно сенсационной."),
    ("fanaticism", "Fanaticism blinds a person.", "фанатизм", "Фанатизм ослепляет человека."),
    ("entropy", "Entropy always increases.", "энтропия", "Энтропия всегда увеличивается."),
    ("goosebumps", "The story gave me goosebumps.", "мурашки", "От истории у меня мурашки."),
    ("fortieth", "This is the fortieth day.", "сороковой", "Это сороковой день."),
    ("illusory", "This hope is illusory.", "иллюзорный", "Эта надежда иллюзорна."),
    ("occult", "She reads occult books.", "оккультный", "Она читает оккультные книги."),
    ("provocative", "Her dress was provocative.", "провокационный", "Её платье было провокационным."),
    ("motorist", "The motorist stopped the car.", "автомобилист", "Автомобилист остановил машину."),
    ("cutaneous", "This is a cutaneous disease.", "кожный", "Это кожная болезнь."),
    ("youngster", "The youngster has talent.", "юнец", "Юнец имеет талант."),
    ("residual", "The residual effect is small.", "остаточный", "Остаточный эффект мал."),
    ("clitoris", "The clitoris is very sensitive.", "клитор", "Клитор очень чувствителен."),
    ("crane", "A crane flew over the field.", "журавль", "Журавль летел над полем."),
    ("reprocess", "We must reprocess the waste.", "переработать", "Мы должны переработать отходы."),
    ("barn", "The old barn holds all the grain.", "амбар", "Старый амбар хранит всё зерно."),
    ("expressively", "She spoke expressively.", "выразительно", "Она говорила выразительно."),
    ("twenty-year-old", "The twenty-year-old student lives here.", "двадцатилетний", "Двадцатилетний студент живёт здесь."),
    ("fearless", "She is fearless.", "бесстрашный", "Она бесстрашная."),
    ("fourteenth", "This is the fourteenth page.", "четырнадцатый", "Это четырнадцатая страница."),
    ("evaluative", "This is an evaluative report.", "оценочный", "Это оценочный доклад."),
    ("legionary", "The legionary marched with the army.", "легионер", "Легионер шёл с армией."),
    ("to settle up", "We need to settle up.", "рассчитаться", "Нам нужно рассчитаться."),
    ("cousin (female)", "My cousin loves painting.", "кузина", "Моя кузина любит рисовать."),
    ("responsive", "She is a responsive friend.", "отзывчивый", "Она отзывчивая подруга."),
    ("dowry", "Her dowry included land.", "приданое", "В её приданое входила земля."),
    ("run into", "He will run into trouble.", "нарваться", "Он нарвётся на беду."),
    ("acquaint", "I will acquaint you with the rules.", "ознакомить", "Я ознакомлю вас с правилами."),
    ("goalkeeper", "The goalkeeper saved the game.", "вратарь", "Вратарь спас игру."),
    ("racism", "Racism has no place here.", "расизм", "Расизму здесь не место."),
    ("hesitantly", "She hesitantly accepted the invitation.", "нерешительно", "Она нерешительно приняла приглашение."),
    ("icebreaker", "The icebreaker crossed the frozen sea.", "ледокол", "Ледокол прошёл по замерзшему морю."),
    ("transcript", "I read the meeting's transcript carefully.", "стенограмма", "Я внимательно прочитал стенограмму встречи."),
    ("dial", "He looks at the dial.", "циферблат", "Он смотрит на циферблат."),
    ("junction", "The train stopped at the junction.", "разъезд", "Поезд остановился на разъезде."),
    ("nimble", "The nimble cat ran away.", "шустрый", "Шустрая кошка убежала."),
    ("lure", "They used candy to lure the boy.", "заманить", "Они заманили мальчика конфетой."),
    ("to contain", "The jar cannot contain all the water.", "вмещать", "Банка не вмещает всю воду."),
    ("observatory", "The observatory sees the stars.", "обсерватория", "Обсерватория видит звёзды."),
    ("hang out", "They hang out here.", "тусоваться", "Они любят тусоваться здесь."),
    ("parry", "He will parry the attack.", "парировать", "Он парирует атаку."),
    ("hooliganism", "The city has a problem with hooliganism.", "хулиганство", "В городе есть проблема хулиганства."),
    ("high school student", "The high school student studies well.", "старшеклассник", "Старшеклассник хорошо учится."),
    ("Romanticism", "Romanticism loved nature and emotion.", "романтизм", "Романтизм любил природу и эмоции."),
    ("accusatory", "His tone was sharp and accusatory.", "обвинительный", "Его тон был резким и обвинительным."),
    ("sarcasm", "I hear your sarcasm.", "сарказм", "Я слышу ваш сарказм."),
    ("water supply", "The water supply was finally fixed.", "водопровод", "Водопровод наконец был починен."),
    ("creamy", "I love creamy mushroom soup.", "сливочный", "Я люблю сливочный грибной суп."),
    ("Chernobyl", "I read about Chernobyl.", "Чернобыль", "Я читал о Чернобыле."),
    ("simple-minded", "He is kind and simple-minded.", "простодушный", "Он добрый и простодушный."),
    ("garland", "The garland is above the door.", "гирлянда", "Гирлянда над дверью."),
    ("collectivization", "Collectivization changed village life.", "коллективизация", "Коллективизация изменила жизнь деревни."),
    ("diagnostic", "This is a diagnostic test.", "диагностический", "Это диагностический тест."),
    ("bony", "The fish was too bony to eat.", "костистый", "Рыба была слишком костистой."),
    ("unsatisfactory", "The results were unsatisfactory.", "неудовлетворительный", "Результаты были неудовлетворительными."),
    ("artistically", "She painted the wall artistically.", "художественно", "Она художественно писала на стене."),
    ("archangel", "He is an archangel.", "архангел", "Он архангел."),
    ("power engineer", "The power engineer fixed the problem.", "энергетик", "Энергетик решил проблему."),
    ("wit", "His wit always helps.", "остроумие", "Его остроумие всегда помогает."),
    ("womb", "Life begins in the womb.", "утроба", "Жизнь начинается в утробе."),
    ("Albanian", "He is Albanian.", "албанец", "Он албанец."),
    ("imbalance", "The imbalance is a problem.", "дисбаланс", "Дисбаланс - это проблема."),
    ("delicacy", "This cake is a delicacy.", "лакомство", "Этот торт - лакомство."),
    ("olive", "She wore an olive dress.", "оливковый", "Она носила оливковое платье."),
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
    "goes": "go",
    "ate": "eat",
    "spoke": "speak",
    "broke": "break",
    "bought": "buy",
    "built": "build",
    "found": "find",
    "left": "leave",
    "held": "hold",
    "holds": "hold",
    "told": "tell",
    "said": "say",
    "heard": "hear",
    "paid": "pay",
    "sold": "sell",
    "lost": "lose",
    "spent": "spend",
    "stood": "stand",
    "wrote": "write",
    "flew": "fly",
    "grew": "grow",
    "began": "begin",
    "became": "become",
    "saved": "save",
    "stopped": "stop",
    "lived": "live",
    "lives": "live",
    "helped": "help",
    "seemed": "seem",
    "did": "do",
    "done": "do",
    "had": "have",
    "has": "have",
    "been": "be",
    "was": "be",
    "were": "be",
    "read": "read",
    "ran": "run",
    "sang": "sing",
    "seen": "see",
    "known": "know",
    "thought": "think",
    "felt": "feel",
    "kept": "keep",
    "put": "put",
    "let": "let",
    "cut": "cut",
    "hit": "hit",
    "set": "set",
    "won": "win",
    "led": "lead",
    "sat": "sit",
    "wore": "wear",
    "included": "include",
    "accepted": "accept",
    "increased": "increase",
    "demanded": "demand",
    "decided": "decide",
    "replaced": "replace",
    "guarded": "guard",
    "used": "use",
    "loved": "love",
    "studies": "study",
    "changed": "change",
    "painted": "paint",
    "fixed": "fix",
    "crossed": "cross",
    "marched": "march",
    "hummed": "hum",
    "blinds": "blind",
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
    "живёт": "жить",
    "еду": "еда",
    "еды": "еда",
    "шла": "идти",
    "шел": "идти",
    "шёл": "идти",
    "шли": "идти",
    "стал": "стать",
    "стала": "стать",
    "стали": "стать",
    "пишет": "писать",
    "увидел": "видеть",
    "услышал": "слышать",
    "слышу": "слышать",
    "идет": "идти",
    "идёт": "идти",
    "поют": "петь",
    "поет": "петь",
    "поёт": "петь",
    "дает": "давать",
    "даёт": "давать",
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
