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

SRC = PACK / "_chunks" / "deck_15260248_04.csv"
OUT = PACK / "_chunks" / "fixed" / "deck_15260248_04.csv"
LOG = PACK / "_chunks" / "logs" / "deck_15260248_04.txt"

FUNCTION_EN = {
    "a", "an", "the", "is", "be", "i", "you", "he", "she", "it", "we", "they",
    "my", "and", "or", "in", "on", "at", "to", "of", "for", "with", "from",
    "not", "his", "him", "her", "their", "them", "our", "us", "me", "am",
    "are", "was", "were", "been", "being", "this", "that", "these", "those",
    "as", "by", "into", "about", "than", "then", "so", "if", "but", "its",
    "your", "do", "does", "did", "will", "would", "can", "could", "may",
    "there", "here", "has", "had", "have",
}

FUNCTION_RU = {
    "и", "а", "или", "не", "ни", "но", "да", "же", "ли", "бы", "то", "это",
    "этот", "эта", "эти", "этой", "этом", "эту", "этих", "этим", "этими",
    "я", "ты", "он", "она", "оно", "мы", "вы", "они", "мой", "моя", "моё",
    "мои", "моего", "моей", "моём", "моим", "мою", "твой", "ваш", "наш",
    "его", "её", "их", "ему", "ей", "им", "ими", "меня", "мне", "меня",
    "тебя", "тебе", "нас", "нам", "вас", "вам", "себя", "себе", "собой",
    "в", "во", "на", "с", "со", "к", "ко", "у", "о", "об", "от", "до",
    "из", "за", "по", "под", "над", "при", "для", "без", "между", "через",
    "был", "была", "было", "были", "будет", "будут", "буду", "есть", "быть",
    "уже", "ещё", "также", "тоже", "только", "уже", "вот", "ведь", "ну",
}

allow_en = {
    line.strip().lower()
    for line in (PACK / "_vocab" / "allow_en_15260248.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_ru = {
    line.strip().replace("ё", "е").lower()
    for line in (PACK / "_vocab" / "allow_ru_15260248.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_en |= FUNCTION_EN
allow_ru |= FUNCTION_RU


# (en_lemma, en_ex, ru_lemma, ru_ex)
FIXED = [
    ("to strive", "We strive to help.", "стремиться", "Мы стремимся помочь."),
    ("station", "I am at the station.", "станция", "Я на станции."),
    ("record", "I made a record of the meeting.", "запись", "Я сделал запись встречи."),
    ("fall", "He will fall soon.", "упасть", "Он скоро упадёт."),
    ("to support", "I want to support my friend.", "поддерживать", "Я хочу поддерживать моего друга."),
    ("down", "He looked down.", "вниз", "Он посмотрел вниз."),
    ("significant", "The change was significant.", "значительный", "Изменение было значительным."),
    ("remind", "Please remind me tomorrow.", "напоминать", "Пожалуйста, напомни мне завтра."),
    ("responsibility", "He accepted the responsibility.", "ответственность", "Он принял ответственность."),
    ("folk", "This is folk music.", "народный", "Это народная музыка."),
    ("European", "This is a European city.", "европейский", "Это европейский город."),
    ("poet", "The poet wrote a book.", "поэт", "Поэт написал книгу."),
    ("compliance", "There is compliance with the law.", "соответствие", "Есть соответствие закону."),
    ("officer", "The officer is in the army.", "офицер", "Офицер в армии."),
    ("July", "We came in July.", "июль", "Мы приехали в июле."),
    ("convey", "I will convey your message.", "передать", "Я передам ваше сообщение."),
    ("elections", "Elections are important.", "выборы", "Выборы важны."),
    ("king", "The king has power.", "король", "У короля есть власть."),
    ("assert", "He will assert the truth.", "утверждать", "Он будет утверждать правду."),
    ("advertisement", "I saw your advertisement on the internet.", "реклама", "Я видел вашу рекламу в интернете."),
    ("revolution", "The revolution is history.", "революция", "Революция — это история."),
    ("phenomenon", "This is a known phenomenon.", "явление", "Это известное явление."),
    ("department", "He works in the financial department.", "отдел", "Он работает в финансовом отделе."),
    ("front", "Soldiers are on the front.", "фронт", "Солдаты на фронте."),
    ("artist", "The artist made a picture.", "художник", "Художник сделал картину."),
    ("informational", "I was at an informational meeting yesterday.", "информационный", "Я был на информационной встрече вчера."),
    ("animal", "The dog is an animal.", "животное", "Собака — это животное."),
    ("user", "The user is in the system.", "пользователь", "Пользователь в системе."),
    ("stage", "This is the last stage.", "этап", "Это последний этап."),
    ("style", "Her style is new.", "стиль", "Её стиль новый."),
    ("norm", "This is the norm now.", "норма", "Это норма сейчас."),
    ("transmission", "I see the transmission.", "передача", "Я вижу передачу."),
    ("value", "Family has great value.", "ценность", "Семья имеет большую ценность."),
    ("phrase", "I know a new phrase.", "фраза", "Я знаю новую фразу."),
    ("definition", "The definition is in the book.", "определение", "Определение в книге."),
    ("sing", "They sing in the morning.", "петь", "Они поют утром."),
    ("past", "He walked past the old house.", "мимо", "Он прошёл мимо старого дома."),
    ("date", "The date is in April.", "дата", "Дата в апреле."),
    ("to find", "She loves to find books.", "находить", "Она любит находить книги."),
    ("seven", "I came at seven today.", "семь", "Я пришёл в семь сегодня."),
    ("captain", "The captain is on the ship.", "капитан", "Капитан на корабле."),
    ("income", "My income is high this year.", "доход", "Мой доход высокий в этом году."),
    ("photograph", "I have this old photograph of the family.", "фотография", "У меня есть эта старая фотография семьи."),
    ("wave", "The wave is on the shore.", "волна", "Волна на берегу."),
    ("gather", "We will gather the team.", "собрать", "Мы соберём команду."),
    ("effort", "His effort was great.", "усилие", "Его усилие было большим."),
    ("clear", "The sky is clear.", "ясный", "Небо ясное."),
    ("professor", "The professor explained the theory clearly.", "профессор", "Профессор ясно объяснил теорию."),
    ("November", "Snow often starts in November.", "ноябрь", "Снег часто начинается в ноябре."),
    ("tea", "I drink tea every morning.", "чай", "Я пью чай каждое утро."),
    ("indicate", "The sign will indicate the path.", "указать", "Знак укажет путь."),
    ("participate", "I will participate in the meeting.", "участвовать", "Я буду участвовать во встрече."),
    ("translation", "I want a translation of this text.", "перевод", "Я хочу перевод этого текста."),
    ("factor", "This is an important factor.", "фактор", "Это важный фактор."),
    ("quietly", "She spoke quietly.", "тихо", "Она говорила тихо."),
    ("channel", "I watch this channel.", "канал", "Я смотрю этот канал."),
    ("useful", "This book is very useful.", "полезный", "Эта книга очень полезная."),
    ("comparison", "Comparison is important.", "сравнение", "Сравнение важно."),
    ("northern", "The northern wind is cold.", "северный", "Северный ветер холодный."),
    ("adult", "She is an adult now.", "взрослый", "Она сейчас взрослая."),
    ("to be born", "He was born in May.", "родиться", "Он родился в мае."),
    ("office", "She works in a small office.", "кабинет", "Она работает в маленьком кабинете."),
    ("recall", "I cannot recall the name.", "вспоминать", "Я не могу вспомнить имя."),
    ("forum", "I found answers on the forum.", "форум", "Я нашёл ответы на форуме."),
    ("personally", "I personally know him.", "лично", "Я лично знаю его."),
    ("spiritual", "This is a spiritual book.", "духовный", "Это духовная книга."),
    ("weak", "He felt weak after the disease.", "слабый", "Он чувствовал себя слабым после болезни."),
    ("in detail", "Explain the process in detail, please.", "подробно", "Пожалуйста, объясните процесс подробно."),
    ("vice versa", "She likes him and vice versa.", "наоборот", "Ей нравится он и наоборот."),
    ("civil", "This is civil law.", "гражданский", "Это гражданский закон."),
    ("journalist", "The journalist wrote an article.", "журналист", "Журналист написал статью."),
    ("conducting", "Conducting research is important.", "проведение", "Проведение исследования важно."),
    ("to perform", "She can perform the work.", "выполнять", "Она может выполнять работу."),
    ("leaf", "The last leaf is on the tree.", "лист", "Последний лист на дереве."),
    ("snow", "The snow is beautiful.", "снег", "Снег красивый."),
    ("to be used", "This can be used.", "использоваться", "Это может использоваться."),
    ("provision", "The provision of water is important.", "обеспечение", "Обеспечение водой важно."),
    ("commission", "She served on the commission.", "комиссия", "Она служила в комиссии."),
    ("to finish", "I have to finish my work.", "закончить", "Мне надо закончить мою работу."),
    ("glory", "They want glory for the country.", "слава", "Они хотят славы для страны."),
    ("convert", "He wants to convert him.", "обратить", "Он хочет обратить его."),
    ("ancient", "This is an ancient city.", "древний", "Это древний город."),
    ("clearly", "This is clearly important.", "явно", "Это явно важно."),
    ("beat", "Do not beat the dog.", "бить", "Не бей собаку."),
    ("tooth", "This tooth is bad.", "зуб", "Этот зуб плохой."),
    ("tradition", "This is a tradition of the family.", "традиция", "Это традиция семьи."),
    ("impossible", "This is often impossible.", "невозможный", "Это часто невозможно."),
    ("height", "The mountain's height is great.", "высота", "Высота горы большая."),
    ("foreign", "She speaks three foreign languages.", "иностранный", "Она говорит на трёх иностранных языках."),
    ("natural", "This is a natural process.", "естественный", "Это естественный процесс."),
    ("chairman", "The chairman opened the meeting.", "председатель", "Председатель открыл встречу."),
    ("neighbor", "My neighbor is very good.", "сосед", "Мой сосед очень хороший."),
    ("to be silent", "He wants to be silent.", "молчать", "Он хочет молчать."),
    ("to drink", "I want to drink some water.", "выпить", "Я хочу выпить немного воды."),
    ("to read", "I want to read the novel.", "прочитать", "Я хочу прочитать роман."),
    ("island", "The island was empty.", "остров", "Остров был пустой."),
    ("pleasant", "This day is very pleasant.", "приятный", "Этот день очень приятный."),
    ("presence", "The presence of water is important.", "наличие", "Наличие воды важно."),
    ("understandable", "Your question is understandable.", "понятный", "Ваш вопрос понятный."),
    ("to set off", "We will set off tomorrow.", "отправиться", "Мы отправимся завтра."),
]


def _en_ok(word: str) -> bool:
    w = word.lower()
    if w in allow_en:
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


def _ru_ok(word: str) -> bool:
    w = word.replace("ё", "е").lower()
    if w in allow_ru:
        return True
    for lemma in allow_ru:
        if len(lemma) < 3:
            continue
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
    # last content token of multiword lemmas like "to strive", "vice versa"
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
        for tok in re.findall(r"[A-Za-z']+", en_ex):
            if not _en_ok(tok):
                leftover.append(f"{i} EN {tok} :: {en_ex}")
        for tok in re.findall(r"[А-Яа-яЁё]+", ru_ex):
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
