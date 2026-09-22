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

SRC = PACK / "_chunks" / "deck_15260283_03.csv"
OUT = PACK / "_chunks" / "fixed" / "deck_15260283_03.csv"
LOG = PACK / "_chunks" / "logs" / "deck_15260283_03.txt"

FUNCTION_EN = {
    "a", "an", "the", "is", "be", "i", "you", "he", "she", "it", "we", "they",
    "my", "and", "or", "in", "on", "at", "to", "of", "for", "with", "from",
    "not", "his", "him", "her", "their", "them", "our", "us", "me", "am",
    "are", "was", "were", "been", "being", "this", "that", "these", "those",
    "as", "by", "into", "about", "than", "then", "so", "if", "but", "its",
    "your", "do", "does", "did", "will", "would", "can", "could", "may",
    "there", "here", "has", "had", "have", "don't", "dont", "let's", "lets",
    "all", "off", "done", "myself", "yourself", "himself", "herself",
    "itself", "ourselves", "themselves", "one's", "ones", "up", "out",
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
allow_ru |= {"утешаться", "мимикрия"}

# (en_lemma, en_ex, ru_lemma, ru_ex)
FIXED = [
    ("to have sex", "They like to have sex at night.", "трахаться", "Они любят трахаться ночью."),
    ("genuinely", "He was genuinely happy.", "подлинно", "Он был подлинно счастлив."),
    ("TV show", "I love that TV show.", "телепередача", "Я люблю ту телепередачу."),
    ("grating", "I heard the grating of the door.", "скрежет", "Я слышал скрежет двери."),
    ("prosaic", "Her words were prosaic.", "прозаический", "Её слова были прозаическими."),
    ("sympathetically", "She looked at him sympathetically.", "сочувственно", "Она посмотрела на него сочувственно."),
    ("to be comforted", "She began to be comforted.", "утешаться", "Она начала утешаться."),
    ("old women's", "This is old women's talk.", "бабий", "Это бабий разговор."),
    ("skeptic", "He remained a skeptic.", "скептик", "Он остался скептиком."),
    ("intimidate", "He tried to intimidate me.", "запугать", "Он пытался запугать меня."),
    ("average", "He is an average American guy.", "среднестатистический", "Он среднестатистический американский парень."),
    ("bald spot", "He has a bald spot.", "лысина", "У него лысина."),
    ("distinguishable", "The stars were barely distinguishable.", "различимый", "Звёзды были едва различимы."),
    ("fall under", "This case will fall under the new law.", "подпадать", "Этот случай будет подпадать под новый закон."),
    ("incomparably", "She is incomparably better.", "несравненно", "Она несравненно лучше."),
    ("to test", "We need to test the program.", "тестировать", "Нам нужно тестировать программу."),
    ("confidentiality", "Keep confidentiality at all costs.", "секретность", "Сохраняйте секретность любой ценой."),
    ("to awaken", "I hope to awaken early tomorrow.", "пробудиться", "Я надеюсь пробудиться рано завтра."),
    ("pilgrim", "The pilgrim visited the sacred place.", "паломник", "Паломник посетил священное место."),
    ("coverage", "The coverage is expanding.", "охват", "Охват расширяется."),
    ("gracious", "Her smile was truly gracious.", "любезный", "Её улыбка была по-настоящему любезной."),
    ("to outrage", "His words began to outrage me.", "возмущать", "Его слова начали возмущать меня."),
    ("chassis", "The car's chassis needs repair.", "шасси", "Шасси автомобиля требует ремонта."),
    ("to be issued", "The papers are to be issued soon.", "оформляться", "Бумаги скоро будут оформляться."),
    ("blond", "He is a blond.", "блондин", "Он блондин."),
    ("sled", "We sat on our sled.", "санки", "Мы сидели на наших санках."),
    ("ballerina", "The ballerina danced well.", "балерина", "Балерина танцевала хорошо."),
    ("baptize", "They will baptize the baby tomorrow.", "окрестить", "Они окрестят малыша завтра."),
    ("chunk", "He threw a chunk of bread.", "кусок", "Он бросил кусок хлеба."),
    ("priestess", "The priestess led the sacred ritual.", "жрица", "Жрица провела священный ритуал."),
    ("screw up", "I will screw up the lid tightly.", "закрутить", "Я закручу крышку плотно."),
    ("gazebo", "We sat in the garden gazebo.", "беседка", "Мы сидели в садовой беседке."),
    ("paramedic", "The paramedic came quickly.", "фельдшер", "Фельдшер быстро пришёл."),
    ("aftertaste", "The soup had a bitter aftertaste.", "привкус", "У супа был горький привкус."),
    ("mimicry", "This insect uses mimicry.", "мимикрия", "Это насекомое использует мимикрию."),
    ("insignificance", "He felt his own insignificance.", "ничтожество", "Он чувствовал своё ничтожество."),
    ("to involve", "He tried to involve her in fraud.", "замешать", "Он пытался замешать её в мошенничество."),
    ("source code", "I read the source code yesterday.", "исходник", "Я читал исходник вчера."),
    ("chronological", "Arrange the events in chronological order.", "хронологический", "Поставьте события в хронологическом порядке."),
    ("rationality", "I value rationality.", "рациональность", "Я ценю рациональность."),
    ("at random", "I chose a book at random.", "наугад", "Я выбрал книгу наугад."),
    ("crawl out", "The baby will crawl out soon.", "выползти", "Малыш скоро выползет."),
    ("vigor", "He worked with vigor.", "бодрость", "Он работал с бодростью."),
    ("chewing gum", "I bought chewing gum.", "жвачка", "Я купил жвачку."),
    ("drinking", "Install a drinking water filter.", "питьевой", "Установите фильтр для питьевой воды."),
    ("plasma", "Blood plasma is important.", "плазма", "Плазма крови важна."),
    ("cement", "We need more cement.", "цемент", "Нам нужно больше цемента."),
    ("communal apartment", "I grew up in a communal apartment.", "коммуналка", "Я вырос в коммуналке."),
    ("to sway", "The wind began to sway the trees.", "покачивать", "Ветер начал покачивать деревья."),
    ("heretic", "They called him a heretic.", "еретик", "Они назвали его еретиком."),
    ("ninetieth", "This is his ninetieth day.", "девяностый", "Это его девяностый день."),
    ("virginity", "She kept her virginity.", "девственность", "Она сохранила свою девственность."),
    ("adrenaline", "I felt adrenaline.", "адреналин", "Я чувствовал адреналин."),
    ("furnish", "They decided to furnish the apartment.", "обставить", "Они решили обставить квартиру."),
    ("hardworking", "She is a hardworking student.", "трудолюбивый", "Она трудолюбивая студентка."),
    ("loyal", "He remained loyal to his friends.", "лояльный", "Он оставался лояльным к своим друзьям."),
    ("purposefully", "She worked purposefully.", "целенаправленно", "Она работала целенаправленно."),
    ("crucify", "They will crucify the traitor.", "распять", "Они распнут предателя."),
    ("to describe", "Don't describe every detail.", "расписывать", "Не расписывай каждую деталь."),
    ("hedge", "The garden has a hedge.", "изгородь", "У сада есть изгородь."),
    ("to feel deeply", "I want to feel deeply this pain.", "прочувствовать", "Я хочу прочувствовать эту боль."),
    ("parachutist", "The parachutist is in the sky.", "парашютист", "Парашютист в небе."),
    ("rye", "They grow rye in the field.", "рожь", "Они растят рожь в поле."),
    ("hem", "She held up her dress's hem.", "подол", "Она подняла подол своего платья."),
    ("audacity", "His audacity surprised us.", "дерзость", "Его дерзость удивила нас."),
    ("to shove", "Don't shove your hand in.", "засовывать", "Не засовывай руку."),
    ("to glue", "I need to glue this paper.", "приклеить", "Мне нужно приклеить эту бумагу."),
    ("satire", "This book is a satire.", "сатира", "Эта книга — сатира."),
    ("bro", "Listen, bro, I know.", "браток", "Слушай, браток, я знаю."),
    ("seethe", "The water began to seethe.", "бурлить", "Вода начала бурлить."),
    ("limousine", "We arrived in a limousine.", "лимузин", "Мы прибыли на лимузине."),
    ("round dance", "They began a round dance.", "хоровод", "Они начали хоровод."),
    ("nun", "The nun prayed silently.", "монахиня", "Монахиня молилась молча."),
    ("depot", "The train arrived at the depot.", "депо", "Поезд прибыл в депо."),
    ("snow-covered", "The mountains were snow-covered.", "заснеженный", "Горы были заснеженные."),
    ("untouched", "The forest remained untouched.", "нетронутый", "Лес оставался нетронутым."),
    ("bristle", "He has gray bristle.", "щетина", "У него седая щетина."),
    ("oil pipeline", "The oil pipeline burst yesterday.", "нефтепровод", "Нефтепровод лопнул вчера."),
    ("jump off", "He will jump off the train.", "соскочить", "Он соскочит с поезда."),
    ("irretrievably", "The letter was irretrievably lost.", "безвозвратно", "Письмо было безвозвратно потеряно."),
    ("symposium", "I went to a symposium.", "симпозиум", "Я ходил на симпозиум."),
    ("chocolate bar", "I want a chocolate bar now.", "шоколадка", "Я хочу шоколадку сейчас."),
    ("department store", "I bought it at the department store.", "универмаг", "Я купил это в универмаге."),
    ("Bolshevism", "He wrote about Bolshevism.", "большевизм", "Он писал о большевизме."),
    ("snowball", "The snowball hit the window softly.", "снежок", "Снежок мягко ударил в окно."),
    ("swimsuit", "She bought a new swimsuit yesterday.", "купальник", "Она купила новый купальник вчера."),
    ("mileage", "The car's mileage is high.", "пробег", "Пробег автомобиля высокий."),
    ("smolder", "The fire continued to smolder.", "тлеть", "Огонь продолжал тлеть."),
    ("blush", "A blush appeared on her face.", "румянец", "На её лице появился румянец."),
    ("caste", "He is from another caste.", "каста", "Он из другой касты."),
    ("golf", "He plays golf every day.", "гольф", "Он играет в гольф каждый день."),
    ("to be guessed", "The answer can be guessed.", "угадываться", "Ответ угадывается."),
    ("astrologer", "The astrologer came yesterday.", "астролог", "Астролог пришёл вчера."),
    ("to infuriate", "Loud noise tends to infuriate me.", "бесить", "Громкий шум обычно бесит меня."),
    ("talk over", "I need to talk over this with him.", "переговорить", "Мне нужно переговорить об этом с ним."),
    ("postman", "The postman brings letters every day.", "почтальон", "Почтальон носит письма каждый день."),
    ("hippie", "The hippie wore bright clothes.", "хиппи", "Хиппи носил яркую одежду."),
    ("self-serving", "He is a self-serving man.", "корыстный", "Он корыстный человек."),
    ("deformation", "The accident caused deformation.", "деформация", "Авария вызвала деформацию."),
    ("chasing", "He ran chasing the dog.", "вдогонку", "Он побежал вдогонку за собакой."),
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
    "threw": "throw",
    "held": "hold",
    "led": "lead",
    "grew": "grow",
    "hit": "hit",
    "lost": "lose",
    "chose": "choose",
    "ran": "run",
    "wore": "wear",
    "read": "read",
    "better": "good",
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
    "писал": "писать",
    "увидел": "видеть",
    "услышал": "слышать",
    "слышу": "слышать",
    "слышал": "слышать",
    "пришел": "прийти",
    "пришла": "прийти",
    "шел": "идти",
    "шла": "идти",
    "шли": "идти",
    "ходил": "ходить",
    "лучше": "хороший",
    "хорошо": "хороший",
    "дети": "детский",
    "растят": "растить",
    "бросил": "бросить",
    "сидели": "сидеть",
    "любит": "любить",
    "любят": "любить",
    "называли": "назвать",
    "сохранила": "сохранить",
    "чувствует": "чувствовать",
    "чувствовал": "чувствовать",
    "удивила": "удивить",
    "вызвала": "вызывать",
    "побежал": "бежать",
    "носит": "носить",
    "купил": "купить",
    "купила": "купить",
    "подняла": "поднять",
    "посмотрела": "смотреть",
    "пытался": "пытаться",
    "остался": "остаться",
    "оставался": "оставаться",
    "решили": "решить",
    "начали": "начать",
    "начал": "начать",
    "начала": "начать",
    "прибыли": "прибыть",
    "прибыл": "прибыть",
    "лопнул": "лопнуть",
    "ударил": "ударить",
    "вырос": "вырасти",
    "танцевала": "танцевать",
    "окрестят": "окрестить",
    "провела": "провести",
    "закручу": "закрутить",
    "использует": "использовать",
    "читал": "читать",
    "поставьте": "поставить",
    "ценю": "ценить",
    "выбрал": "выбрать",
    "установите": "установить",
    "сохраняйте": "сохранять",
    "надеюсь": "надеяться",
    "посетил": "посетить",
    "требует": "требовать",
    "распнут": "распять",
    "расписывай": "расписывать",
    "засовывай": "засовывать",
    "слушай": "слушать",
    "угадывается": "угадываться",
    "бесит": "бесить",
    "переговорить": "переговорить",
    "молилась": "молиться",
    "играл": "играть",
    "носит": "носить",
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
