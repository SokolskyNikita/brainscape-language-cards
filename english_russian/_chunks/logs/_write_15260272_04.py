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

SRC = PACK / "_chunks" / "deck_15260272_04.csv"
OUT = PACK / "_chunks" / "fixed" / "deck_15260272_04.csv"
LOG = PACK / "_chunks" / "logs" / "deck_15260272_04.txt"

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
    "just", "quite", "soon", "quickly", "easily", "slowly", "tonight",
    "last", "year", "up", "down", "out", "off", "onto", "upon", "around",
    "against", "during", "while", "because", "until", "since", "though",
    "each", "every", "both", "own", "same", "other", "another", "new",
    "old", "good", "bad", "big", "small", "long", "short", "high", "low",
    "himself", "herself", "itself", "themselves", "myself", "yourself",
    "everyone", "someone", "anyone", "everything", "something", "anything",
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
}

allow_en = {
    line.strip().lower()
    for line in (PACK / "_vocab" / "allow_en_15260272.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_ru = {
    line.strip().replace("ё", "е").lower()
    for line in (PACK / "_vocab" / "allow_ru_15260272.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_en |= FUNCTION_EN
allow_ru |= FUNCTION_RU

# (en_lemma, en_ex, ru_lemma, ru_ex)
FIXED = [
    ("to hurt", "His words hurt me.", "задевать", "Его слова задевают меня."),
    ("muse", "She became his artistic muse.", "муза", "Она стала его художественной музой."),
    ("surge", "There was a surge of excitement.", "всплеск", "Был всплеск возбуждения."),
    ("violator", "He is a law violator.", "нарушитель", "Он нарушитель закона."),
    ("walking", "Walking is good exercise.", "ходьба", "Ходьба — это хорошая тренировка."),
    ("lean against", "She leaned against the old oak tree.", "прислониться", "Она прислонилась к старому дубу."),
    ("woolen", "She wore a woolen coat.", "шерстяной", "Она носила шерстяное пальто."),
    ("taxi driver", "The taxi driver arrived quickly.", "таксист", "Таксист приехал быстро."),
    ("comprehension", "His comprehension of the text is good.", "осмысление", "Его осмысление текста хорошее."),
    ("layout", "Check the game's layout.", "расклад", "Проверьте расклад игры."),
    ("to jump off", "He will jump off the table.", "спрыгнуть", "Он спрыгнет со стола."),
    ("juror", "The juror listened intently.", "присяжный", "Присяжный внимательно слушал."),
    ("exclusive", "This is an exclusive interview.", "эксклюзивный", "Это эксклюзивное интервью."),
    ("sway", "The trees sway gently in the wind.", "покачиваться", "Деревья покачиваются на ветру."),
    ("conceal", "She tried to conceal her feelings.", "таить", "Она пыталась таить свои чувства."),
    ("squeeze out", "I managed to squeeze out the paint.", "выдавить", "Мне удалось выдавить краску."),
    ("wireless", "I prefer a wireless telephone.", "беспроводной", "Я предпочитаю беспроводной телефон."),
    ("kids", "The kids played joyfully outside.", "ребятишки", "Ребятишки радостно играли на улице."),
    ("subway", "I go by subway daily.", "метрополитен", "Я ежедневно добираюсь на метрополитене."),
    ("to be believed", "This is not to be believed.", "вериться", "В это не верится."),
    ("panorama", "The panorama from the hill is beautiful.", "панорама", "Панорама с холма красивая."),
    ("modesty", "Her modesty is truly strong.", "скромность", "Её скромность действительно сильная."),
    ("to slam", "He will slam the door.", "захлопнуть", "Он захлопнет дверь."),
    ("weakening", "I see a weakening of his power.", "ослабление", "Я вижу ослабление его силы."),
    ("detention", "He faced detention at the border.", "задержание", "Он столкнулся с задержанием на границе."),
    ("conceptual", "This is a conceptual design phase.", "концептуальный", "Это концептуальная фаза."),
    ("maid", "The maid cleaned the room quietly.", "служанка", "Служанка тихо мыла комнату."),
    ("stimulation", "Exercise provides stimulation.", "стимулирование", "Упражнения обеспечивают стимулирование."),
    ("graduate student", "The graduate student defended the thesis.", "аспирант", "Аспирант защитил диссертацию."),
    ("human rights", "He defends human rights.", "права человека", "Он защищает права человека."),
    ("paradigm", "This is a new paradigm.", "парадигма", "Это новая парадигма."),
    ("construct", "They will construct a new bridge soon.", "соорудить", "Они скоро соорудят новый мост."),
    ("to accustom", "She will accustom him to work.", "приучить", "Она приучит его к работе."),
    ("led", "The led group is here.", "ведомый", "Ведомая группа здесь."),
    ("overflow", "Do not overflow the cup.", "переполнить", "Не переполните чашку."),
    ("freshness", "The morning air has freshness.", "свежесть", "В утреннем воздухе есть свежесть."),
    ("alarm clock", "The alarm clock is loud.", "будильник", "Будильник громкий."),
    ("sticky", "The table felt sticky and dirty.", "липкий", "Стол был липким и грязным."),
    ("to voice", "She decided to voice her concerns.", "озвучить", "Она решила озвучить свои опасения."),
    ("vital activity", "This is vital activity.", "жизнедеятельность", "Это жизнедеятельность."),
    ("to accost", "He will accost her.", "пристать", "Он пристанет к ней."),
    ("disruption", "The disruption spoiled our plans.", "срыв", "Срыв испортил наши планы."),
    ("ghostly", "The castle had a ghostly appearance.", "призрачный", "Замок имел призрачный вид."),
    ("downpour", "The sudden downpour started.", "ливень", "Внезапный ливень начался."),
    ("van", "We loaded the van with boxes.", "фургон", "Мы загрузили фургон ящиками."),
    ("cord", "I need a new cord.", "шнур", "Мне нужно взять новый шнур."),
    ("to unite", "They decided to unite.", "объединяться", "Они решили объединиться."),
    ("caravan", "The caravan went through the desert.", "караван", "Караван шёл через пустыню."),
    ("to gnaw", "The dog loves to gnaw bones.", "грызть", "Собака любит грызть кости."),
    ("to be covered", "The roof is to be covered with snow.", "покрываться", "Крыша покрывается снегом."),
    ("coerce", "They used threats to coerce him.", "принудить", "Они использовали угрозы, чтобы принудить его."),
    ("horoscope", "I read my horoscope daily.", "гороскоп", "Я читаю свой гороскоп каждый день."),
    ("fishing rod", "He bought a new fishing rod.", "удочка", "Он купил новую удочку."),
    ("non-standard", "He prefers non-standard solutions.", "нестандартный", "Он предпочитает нестандартные решения."),
    ("no need", "No need to do this.", "незачем", "Незачем делать это."),
    ("to make friends", "She wants to make friends.", "подружиться", "Она хочет подружиться."),
    ("Novgorodian", "The Novgorodian icon is priceless.", "новгородский", "Новгородская икона бесценна."),
    ("occupation", "The occupation went on for years.", "оккупация", "Оккупация шла годы."),
    ("like-minded person", "I found a like-minded person.", "единомышленник", "Я нашёл единомышленника."),
    ("noisily", "They played noisily outside.", "шумно", "Они шумно играли на улице."),
    ("obediently", "The dog obediently followed its owner.", "послушно", "Собака послушно следовала за своим хозяином."),
    ("uncertainty", "I feel uncertainty.", "неуверенность", "Я чувствую неуверенность."),
    ("skilled", "She is a skilled worker.", "умелый", "Она умелый сотрудник."),
    ("infect", "Mosquitoes can infect a human with disease.", "заразить", "Комары могут заразить человека."),
    ("neglect", "Don't neglect your health.", "пренебрегать", "Не пренебрегайте своим здоровьем."),
    ("to swing open", "The door began to swing open slowly.", "распахнуться", "Дверь начала медленно распахиваться."),
    ("throw back", "He will throw back his head.", "откинуть", "Он откинет голову."),
    ("suggestion", "His suggestion was strong.", "внушение", "Его внушение было сильным."),
    ("appropriation", "He faced criticism for cultural appropriation.", "присвоение", "Он столкнулся с критикой за культурное присвоение."),
    ("demise", "His demise was sudden.", "кончина", "Его кончина была внезапной."),
    ("show off", "He loves to show off his new car.", "красоваться", "Он любит красоваться своей новой машиной."),
    ("coastal", "This is a coastal city.", "береговой", "Это береговой город."),
    ("cut off", "Don't cut off the branch.", "срезать", "Не срезайте ветку."),
    ("hemisphere", "The Earth is divided into two hemispheres.", "полушарие", "Земля разделена на два полушария."),
    ("emotionally", "She spoke emotionally.", "эмоционально", "Она говорила эмоционально."),
    ("briskly", "She briskly started her morning work.", "бодро", "Она бодро начала утреннюю работу."),
    ("opened", "The book was finally opened.", "раскрытый", "Книга была наконец раскрыта."),
    ("lift up", "He likes to lift up his shirt.", "задрать", "Он любит задрать рубашку."),
    ("romance", "I love romance.", "романтика", "Я люблю романтику."),
    ("Berlin", "Berlin is a large city.", "Берлин", "Берлин большой город."),
    ("to be scared", "I tried not to be scared.", "пугаться", "Я пытался не пугаться."),
    ("to age", "We all begin to age from birth.", "стареть", "Мы все начинаем стареть с рождения."),
    ("vocabulary", "Expand your vocabulary daily.", "лексика", "Учите свою лексику каждый день."),
    ("prototype", "They test the prototype.", "прототип", "Они проверяют прототип."),
    ("to throw back", "The mirror tends to throw back light.", "отбрасывать", "Зеркало склонно отбрасывать свет."),
    ("trudge", "We trudge through the deep snow.", "брести", "Мы бредем через глубокий снег."),
    ("compact", "A compact car saves space.", "компактный", "Компактный автомобиль занимает мало места."),
    ("vibration", "The telephone's vibration will startle me.", "вибрация", "Вибрация телефона пугает меня."),
    ("cigar", "He has a fine cigar.", "сигара", "У него изысканная сигара."),
    ("to fly into", "The bird will fly into the room.", "влететь", "Птица влетит в комнату."),
    ("discontentedly", "She sighed discontentedly at the news.", "недовольно", "Она недовольно вздохнула от новостей."),
    ("wreath", "She placed a wreath on the grave.", "венок", "Она поставила венок на могилу."),
    ("timely", "Your timely answer was important.", "своевременный", "Ваш своевременный ответ был важен."),
    ("humbly", "I humbly accept your answer.", "покорно", "Я покорно принимаю ваш ответ."),
    ("twelfth", "He finished in twelfth place.", "двенадцатый", "Он закончил на двенадцатом месте."),
    ("gymnastics", "She likes gymnastics.", "гимнастика", "Она любит гимнастику."),
    ("millimeter", "This is one millimeter.", "миллиметр", "Это один миллиметр."),
    ("to be served", "Dinner is to be served soon.", "подаваться", "Ужин скоро будет подаваться."),
    ("jewel", "She wore a jewel.", "драгоценность", "Она носила драгоценность."),
    ("proletarian", "This is a proletarian newspaper.", "пролетарский", "Это пролетарская газета."),
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
    "told": "tell", "got": "get", "gotten": "get", "found": "find",
    "left": "leave", "kept": "keep", "felt": "feel", "thought": "think",
    "brought": "bring", "stood": "stand", "sat": "sit", "ran": "run",
    "won": "win", "lost": "lose", "met": "meet", "led": "lead",
    "paid": "pay", "spoke": "speak", "written": "write", "wrote": "write",
    "ate": "eat", "eaten": "eat", "drank": "drink", "drunk": "drink",
    "taught": "teach", "caught": "catch", "began": "begin", "begun": "begin",
    "shown": "show", "showed": "show", "built": "build", "held": "hold",
    "heard": "hear", "sent": "send", "spent": "spend", "meant": "mean",
    "wore": "wear", "worn": "wear", "rang": "ring", "rung": "ring",
    "became": "become", "become": "become",
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
    "а", "я", "о", "е", "у", "ю", "ы", "и",
)


def ru_stems(word: str) -> set[str]:
    stems = {word}
    for end in RU_ENDINGS:
        if word.endswith(end) and len(word) - len(end) >= 3:
            stems.add(word[: -len(end)])
    if len(word) >= 5:
        stems.add(word[:5])
        stems.add(word[:4])
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
        if any(w.startswith(lemma) or lemma.startswith(w) for lemma in allowed if len(lemma) >= 4 and len(w) >= 4):
            continue
        if any(
            w[: max(4, len(w) - 3)] == lemma[: max(4, len(w) - 3)]
            for lemma in allowed
            if abs(len(lemma) - len(w)) <= 4 and min(len(lemma), len(w)) >= 4
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
