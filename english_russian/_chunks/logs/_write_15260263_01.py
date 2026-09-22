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

SRC = PACK / "_chunks" / "deck_15260263_01.csv"
OUT = PACK / "_chunks" / "fixed" / "deck_15260263_01.csv"
LOG = PACK / "_chunks" / "logs" / "deck_15260263_01.txt"

FUNCTION_EN = {
    "a", "the", "is", "be", "i", "you", "he", "she", "it", "we", "they",
    "my", "and", "or", "in", "on", "at", "to", "of", "for", "with", "from",
    "not", "his", "him", "her", "their", "them", "our", "us", "me", "am",
    "are", "was", "were", "been", "being", "this", "that", "these", "those",
    "an", "as", "by", "into", "about", "than", "then", "so", "if", "but",
    "its", "your", "all", "no", "yes", "do", "does", "did", "done", "doing",
    "has", "have", "had", "having", "will", "would", "can", "could", "may",
    "might", "must", "shall", "should", "just", "also", "too", "very",
}

FUNCTION_RU = {
    w.replace("ё", "е")
    for w in {
        "я", "ты", "он", "она", "оно", "мы", "вы", "они", "меня", "тебя", "его",
        "её", "ее", "нас", "вас", "их", "мне", "тебе", "ему", "ей", "нам", "вам",
        "им", "мной", "мною", "тобой", "ним", "ней", "него", "нем", "нём", "ними",
        "неё", "нее",
        "собой", "мой", "моя", "моё", "мое", "мои", "твой", "твоя", "твоё", "твое",
        "твои", "свой", "своя", "своё", "свое", "свои", "наш", "наша", "наше",
        "наши", "ваш", "ваша", "ваше", "ваши", "этот", "эта", "это", "эти",
        "тот", "та", "то", "те", "такой", "такая", "такое", "такие", "весь",
        "вся", "всё", "все", "сам", "сама", "само", "сами", "быть", "есть",
        "был", "была", "было", "были", "буду", "будет", "будем", "будете",
        "будут", "нет", "не", "ни", "да", "уже", "ещё", "еще", "только", "даже",
        "тоже", "также", "очень", "так", "как", "что", "кто", "где", "когда",
        "почему", "куда", "который", "какой", "чтобы", "если", "потому", "ведь",
        "ли", "же", "бы", "вот", "здесь", "тут", "там", "теперь", "сейчас",
        "потом", "всегда", "никогда", "иногда", "от", "до", "по", "со", "из",
        "без", "при", "про", "об", "за", "над", "под", "перед", "после",
        "между", "через", "около", "для", "к", "у", "о", "в", "на", "с", "и",
        "а", "но", "или",
    }
}

IRREGULAR = {
    "bought": "buy", "came": "come", "became": "become", "lost": "lose",
    "fought": "fight", "began": "begin", "ran": "run", "ate": "eat",
    "drank": "drink", "saw": "see", "went": "go", "got": "get",
    "gave": "give", "took": "take", "made": "make", "knew": "know",
    "thought": "think", "told": "tell", "left": "leave", "felt": "feel",
    "kept": "keep", "stood": "stand", "sat": "sit", "wrote": "write",
    "grew": "grow", "wore": "wear", "chose": "choose", "spoke": "speak",
    "heard": "hear", "held": "hold", "found": "find", "said": "say",
    "did": "do", "had": "have", "has": "have", "been": "be", "was": "be",
    "were": "be", "is": "be", "are": "be", "am": "be",
    "tore": "tear", "forgot": "forget", "sent": "send", "broke": "break",
    "flew": "fly", "led": "lead", "met": "meet", "won": "win", "sang": "sing",
    "fell": "fall",
}

allow_en = {
    line.strip().lower()
    for line in (PACK / "_vocab" / "allow_en_15260263.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
} | FUNCTION_EN
allow_ru = {
    line.strip().replace("ё", "е").lower()
    for line in (PACK / "_vocab" / "allow_ru_15260263.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
} | FUNCTION_RU

# (en_lemma, en_ex, ru_lemma, ru_ex)
FIXED = [
    ("hut", "The old hut stands in the forest.", "изба", "Старая изба стоит в лесу."),
    ("cult", "This cult is new.", "культ", "Этот культ новый."),
    ("monkey", "The monkey sits in the tree.", "обезьяна", "Обезьяна сидит на дереве."),
    ("shareholder", "The shareholder is at the meeting.", "акционер", "Акционер на встрече."),
    ("clash", "There was a clash in the street.", "схватка", "На улице была схватка."),
    ("compilation", "The compilation of the list is important.", "составление", "Составление списка важно."),
    ("copper", "The copper kettle is on the table.", "медный", "Медный чайник на столе."),
    ("continent", "This continent is large.", "континент", "Этот континент большой."),
    ("oncoming", "Watch the oncoming car.", "встречный", "Смотри на встречную машину."),
    ("to run away", "They run away from the house.", "убегать", "Они убегают из дома."),
    ("bomber", "The bomber is over the city.", "бомбардировщик", "Бомбардировщик над городом."),
    ("science fiction", "I love science fiction.", "фантастика", "Я люблю фантастику."),
    ("to be late", "He tried not to be late.", "опоздать", "Он пытался не опоздать."),
    ("briefcase", "He has documents in a briefcase.", "портфель", "У него документы в портфеле."),
    ("restrain", "Please restrain your emotions.", "сдерживать", "Пожалуйста, сдерживайте свои эмоции."),
    ("builder", "The builder finished the house today.", "строитель", "Строитель закончил дом сегодня."),
    ("to be guided", "Learn to be guided by the rule.", "руководствоваться", "Научитесь руководствоваться правилом."),
    ("representation", "The company opened a representation in the city.", "представительство", "Компания открыла представительство в городе."),
    ("aggressive", "His aggressive behavior scared her.", "агрессивный", "Его агрессивное поведение напугало её."),
    ("to vote", "I will vote today.", "проголосовать", "Я проголосую сегодня."),
    ("inheritance", "She has a large inheritance.", "наследство", "У неё большое наследство."),
    ("premier", "He saw the premier yesterday.", "премьер", "Он видел премьера вчера."),
    ("descent", "The descent is long.", "спуск", "Спуск длинный."),
    ("fullness", "I feel the fullness of life.", "полнота", "Я чувствую полноту жизни."),
    ("presentation", "The presentation is at ten.", "презентация", "Презентация в десять."),
    ("ringing", "I hear a ringing.", "звон", "Я слышу звон."),
    ("discount", "There is a discount today.", "скидка", "Сегодня есть скидка."),
    ("cardiac", "He has a cardiac problem.", "сердечный", "У него сердечная проблема."),
    ("categorically", "He categorically denied it.", "категорически", "Он категорически отрицал это."),
    ("Indian", "I love Indian food.", "индийский", "Я люблю индийскую еду."),
    ("law enforcement", "This is a law enforcement organ.", "правоохранительный", "Это правоохранительный орган."),
    ("constructor", "I have a constructor at home.", "конструктор", "У меня дома есть конструктор."),
    ("treasure", "We found treasure in the house.", "сокровище", "Мы нашли сокровище в доме."),
    ("colossal", "The statue is colossal.", "колоссальный", "Статуя колоссальная."),
    ("glove", "She lost her left glove yesterday.", "перчатка", "Она потеряла свою левую перчатку вчера."),
    ("poverty", "Poverty is a big problem.", "бедность", "Бедность — большая проблема."),
    ("decorate", "Let's decorate the room together.", "украшать", "Давайте вместе украсим комнату."),
    ("to cause", "He will cause no harm.", "причинить", "Он не причинит вреда."),
    ("limiting", "This is the limiting speed.", "предельный", "Это предельная скорость."),
    ("microphone", "She speaks into the microphone.", "микрофон", "Она говорит в микрофон."),
    ("to surrender", "He will not surrender.", "сдаваться", "Он не будет сдаваться."),
    ("they say", "They say he is home.", "дескать", "Он, дескать, дома."),
    ("formulation", "The formulation of the idea is clear.", "формулировка", "Формулировка идеи ясна."),
    ("analogy", "He explained it with an analogy.", "аналогия", "Он объяснил это аналогией."),
    ("stimulate", "Coffee will stimulate work.", "стимулировать", "Кофе будет стимулировать работу."),
    ("assistance", "They offered assistance.", "содействие", "Они предложили содействие."),
    ("seventy", "He is seventy.", "семьдесят", "Ему семьдесят."),
    ("sausage", "I bought sausage for breakfast.", "колбаса", "Я купил колбасу на завтрак."),
    ("plastic", "She bought a plastic bottle.", "пластиковый", "Она купила пластиковую бутылку."),
    ("territorial", "This is a territorial question.", "территориальный", "Это территориальный вопрос."),
    ("basket", "She has a basket of apples.", "корзина", "У неё корзина яблок."),
    ("break away", "He will break away from the crowd.", "оторваться", "Он оторвётся от толпы."),
    ("fall down", "The old tree will fall down soon.", "свалиться", "Старое дерево скоро свалится."),
    ("instructor", "The instructor explained the exercise.", "инструктор", "Инструктор объяснил упражнение."),
    ("traditionally", "Traditionally we eat at home.", "традиционно", "Традиционно мы едим дома."),
    ("buttocks", "He sat on his buttocks.", "задница", "Он сел на задницу."),
    ("hierarchy", "The company has a hierarchy.", "иерархия", "В компании есть иерархия."),
    ("refer", "Please refer to the book.", "ссылаться", "Пожалуйста, ссылайтесь на книгу."),
    ("stress", "Stress is bad for health.", "стресс", "Стресс плох для здоровья."),
    ("experimental", "This is experimental work.", "экспериментальный", "Это экспериментальная работа."),
    ("to cry", "She will cry.", "заплакать", "Она заплачет."),
    ("towel", "Bring your towel to the beach.", "полотенце", "Возьми своё полотенце на пляж."),
    ("exposition", "The exposition of the idea is clear.", "изложение", "Изложение идеи ясно."),
    ("deprivation", "This deprivation is a problem.", "лишение", "Это лишение — проблема."),
    ("apprehension", "She felt apprehension.", "опасение", "Она чувствовала опасение."),
    ("light bulb", "I need a new light bulb.", "лампочка", "Мне нужна новая лампочка."),
    ("overturn", "The wind will overturn the boat.", "перевернуть", "Ветер перевернёт лодку."),
    ("agricultural", "This is agricultural land.", "сельскохозяйственный", "Это сельскохозяйственная земля."),
    ("to travel", "I love to travel.", "путешествовать", "Я люблю путешествовать."),
    ("milky", "She loves milky coffee.", "молочный", "Она любит молочный кофе."),
    ("jet", "There is a jet of water.", "струя", "Есть струя воды."),
    ("consecutive", "These are consecutive numbers.", "последовательный", "Это последовательные числа."),
    ("betrayal", "His betrayal is a problem.", "измена", "Его измена — проблема."),
    ("in the distance", "There is a house in the distance.", "вдали", "Вдали есть дом."),
    ("to attack", "The dog will attack him.", "нападать", "Собака будет нападать на него."),
    ("cable", "The cable is on the table.", "кабель", "Кабель на столе."),
    ("to squeeze", "She tried to squeeze his hand.", "сжимать", "Она пыталась сжимать его руку."),
    ("elegant", "She wore an elegant dress.", "изящный", "Она носила изящное платье."),
    ("accumulate", "He will accumulate gold.", "накопить", "Он накопит золото."),
    ("to surpass", "She will surpass him.", "превосходить", "Она будет превосходить его."),
    ("singing", "I hear singing.", "пение", "Я слышу пение."),
    ("statue", "The statue stands in the park.", "статуя", "Статуя стоит в парке."),
    ("accuse", "They will accuse him.", "обвинить", "Они обвинят его."),
    ("sober", "He was sober yesterday.", "трезвый", "Он был трезвым вчера."),
    ("monster", "The monster is in the house.", "монстр", "Монстр в доме."),
    ("to stretch out", "He will stretch out his hand.", "протягивать", "Он будет протягивать руку."),
    ("decay", "The decay of the system is a problem.", "распад", "Распад системы — проблема."),
    ("objection", "He has an objection.", "возражение", "У него есть возражение."),
    ("to cherish", "Learn to cherish your health.", "беречь", "Научитесь беречь своё здоровье."),
    ("conductor", "The conductor knows the road.", "проводник", "Проводник знает дорогу."),
    ("march", "Soldiers march in the street.", "шагать", "Солдаты шагают по улице."),
    ("carry away", "The waves will carry away the boat.", "унести", "Волны унесут лодку."),
    ("cessation", "The cessation of work is important.", "прекращение", "Прекращение работы важно."),
    ("eliminate", "We must eliminate the danger.", "устранить", "Мы должны устранить опасность."),
    ("tenderness", "Her voice was full of tenderness.", "нежность", "Её голос был полон нежности."),
    ("chemistry", "I love chemistry.", "химия", "Я люблю химию."),
    ("millennium", "This is a new millennium.", "тысячелетие", "Это новое тысячелетие."),
    ("anxious", "She had an anxious look.", "тревожный", "У неё был тревожный вид."),
    ("commandment", "This is an old commandment.", "заповедь", "Это старая заповедь."),
    ("pond", "The pond is near the house.", "пруд", "Пруд рядом с домом."),
]


def en_forms(word: str) -> set[str]:
    forms = {word}
    if word in IRREGULAR:
        forms.add(IRREGULAR[word])
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
    return forms


def en_ok(text: str, extra: set[str]) -> list[str]:
    bad = []
    for raw in re.findall(r"[A-Za-z']+", text):
        w = raw.lower().replace("'", "")
        if not w or w in allow_en or w in extra:
            continue
        if any(form in allow_en or form in extra for form in en_forms(w)):
            continue
        if w.endswith("ly") and w[:-2] + "l" in allow_en:
            continue
        for lemma in allow_en | extra:
            parts = lemma.replace("-", " ").split()
            if w in parts:
                break
        else:
            bad.append(raw)
    return bad


RU_IRREG = {
    "пить": ("пь",),
    "есть": ("ед", "еш", "ем", "ел"),
    "идти": ("ид", "шл", "ше"),
    "пойти": ("пой", "пош"),
    "мочь": ("мож", "мог"),
    "учить": ("уч",),
    "взять": ("возьм", "взя"),
}


def ru_ok(text: str, extra: set[str]) -> list[str]:
    bad = []
    pool = allow_ru | extra
    for raw in re.findall(r"[А-Яа-яЁё-]+", text):
        w = raw.replace("ё", "е").replace("Ё", "е").lower()
        if w in pool:
            continue
        if any(
            w.startswith(lemma) or lemma.startswith(w)
            for lemma in pool
            if len(lemma) >= 3 and len(w) >= 3
        ):
            continue
        if any(
            w[:3] == lemma[:3]
            for lemma in pool
            if len(lemma) >= 3 and len(w) >= 3
        ):
            continue
        if any(
            lemma in pool and any(w.startswith(stem) for stem in stems)
            for lemma, stems in RU_IRREG.items()
        ):
            continue
        bad.append(raw)
    return bad


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


def lemma_in_en(gloss: str, example: str) -> bool:
    g = gloss.lower()
    ex = example.lower()
    if g in ex:
        return True
    key = re.sub(r"^(to |the |a |an )", "", g)
    if key in ex:
        return True
    parts = [p for p in key.replace("-", " ").split() if p not in {"to", "the", "a", "an", "be"}]
    return all(p in ex for p in parts) if parts else False


def lemma_in_ru(lemma: str, example: str) -> bool:
    key = lemma.lower().replace("ё", "е")
    ex = example.lower().replace("ё", "е")
    if key in ex:
        return True
    if len(key) >= 4 and key[:4] in ex:
        return True
    if len(key) >= 5 and key[:5] in ex:
        return True
    return False


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
        extra_en = set(re.findall(r"[a-z']+", en.lower()))
        extra_en |= set(en.lower().replace("-", " ").split())
        extra_ru = {w.replace("ё", "е").lower() for w in re.findall(r"[А-Яа-яЁё-]+", ru)}
        for token in en_ok(en_ex, extra_en):
            leftover.append(f"{i} EN leftover {token!r}: {en_ex}")
        for token in ru_ok(ru_ex, extra_ru):
            leftover.append(f"{i} RU leftover {token!r}: {ru_ex}")
        if not lemma_in_en(en, en_ex):
            leftover.append(f"{i}: EN example missing {en!r}")
        if not lemma_in_ru(ru, ru_ex):
            leftover.append(f"{i}: RU example missing {ru!r}")
        cards.append(make_card(en, en_ex, ru, ru_ex))

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
    else:
        print("vocab check clean")


if __name__ == "__main__":
    main()
