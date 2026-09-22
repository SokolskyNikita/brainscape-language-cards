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

SRC = PACK / "_chunks" / "deck_15260255_02.csv"
OUT = PACK / "_chunks" / "fixed" / "deck_15260255_02.csv"
LOG = PACK / "_chunks" / "logs" / "deck_15260255_02.txt"

FUNCTION = {
    "a", "the", "is", "be", "i", "you", "he", "she", "it", "we", "they",
    "my", "and", "or", "in", "on", "at", "to", "of", "for", "with", "from",
    "not", "his", "him", "her", "their", "them", "our", "us", "me", "am",
    "are", "was", "were", "been", "being", "this", "that", "these", "those",
    "an", "as", "by", "into", "about", "than", "then", "so", "if", "but",
    "its", "your", "has", "had", "did", "does", "will", "can", "could",
    "should", "would", "must", "do", "have",
}

allow_en = {
    line.strip().lower()
    for line in (PACK / "_vocab" / "allow_en_15260255.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_ru = {
    line.strip().replace("ё", "е").lower()
    for line in (PACK / "_vocab" / "allow_ru_15260255.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_en |= FUNCTION

# (en_lemma, en_ex, ru_lemma, ru_ex)
FIXED = [
    ("advertising", "This is an advertising campaign.", "рекламный", "Это рекламная кампания."),
    ("criminal", "This is a criminal case.", "уголовный", "Это уголовное дело."),
    ("to be determined", "The price is determined here.", "определяться", "Цена определяется здесь."),
    ("witness", "He was a witness to the crime.", "свидетель", "Он был свидетелем преступления."),
    ("kilogram", "I need a kilogram of bread.", "килограмм", "Мне нужен килограмм хлеба."),
    ("exam", "I passed the exam successfully.", "экзамен", "Я успешно сдал экзамен."),
    ("derive", "We can derive the formula easily.", "вывести", "Мы можем легко вывести формулу."),
    ("pull", "Pull the door to open it.", "тянуть", "Надо тянуть дверь, чтобы открыть её."),
    ("manager", "The manager opened the meeting.", "менеджер", "Менеджер открыл встречу."),
    ("cycle", "This cycle is important.", "цикл", "Этот цикл важен."),
    ("surprise", "Her gift was a pleasant surprise.", "удивление", "Её подарок был приятным удивлением."),
    ("Jewish", "This is a Jewish holiday.", "еврейский", "Это еврейский праздник."),
    ("reasonable", "His demands were quite reasonable.", "разумный", "Его требования были вполне разумны."),
    ("investment", "This is a good investment.", "инвестиция", "Это хорошая инвестиция."),
    ("inscription", "There was an inscription on the wall.", "надпись", "На стене была надпись."),
    ("to happen", "This can happen.", "случаться", "Это может случаться."),
    ("bag", "Her bag is everywhere.", "сумка", "Её сумка везде."),
    ("gold", "I have gold.", "золото", "У меня есть золото."),
    ("cigarette", "He wants a cigarette.", "сигарета", "Он хочет сигарету."),
    ("successful", "He is a successful entrepreneur.", "успешный", "Он успешный предприниматель."),
    ("to take away", "I want to take away your keys.", "забрать", "Я хочу забрать твои ключи."),
    ("quite a bit", "He reads quite a bit every day.", "немало", "Он каждый день читает немало."),
    ("cloud", "The sky is full of clouds.", "облако", "Небо полно облаков."),
    ("quote", "This is a famous quote.", "цитата", "Это известная цитата."),
    ("stripe", "The wall has a red stripe.", "полоса", "На стене есть красная полоса."),
    ("rating", "The movie's rating was low.", "рейтинг", "Рейтинг фильма был низким."),
    ("implement", "We will implement the plan tomorrow.", "реализовать", "Мы реализуем план завтра."),
    ("instruction", "Follow the instruction carefully.", "указание", "Следуйте указанию внимательно."),
    ("forced", "He was forced to apologize.", "вынужденный", "Он был вынужден извиниться."),
    ("warrior", "The warrior was ready for war.", "воин", "Воин был готов к войне."),
    ("atmosphere", "The atmosphere protects the Earth.", "атмосфера", "Атмосфера защищает Землю."),
    ("manage", "We'll manage without help.", "обойтись", "Мы можем обойтись без помощи."),
    ("monument", "The city has a new monument.", "памятник", "В городе есть новый памятник."),
    ("argue", "They often argue about policy.", "спорить", "Они часто спорят о политике."),
    ("accidental", "It was an accidental discovery.", "случайный", "Это было случайное открытие."),
    ("archive", "I searched the archive for hours.", "архив", "Я искал в архиве часами."),
    ("to implement", "We want to implement this strategy.", "осуществлять", "Мы хотим осуществлять эту стратегию."),
    ("actively", "She actively participated in the discussion.", "активно", "Она активно участвовала в обсуждении."),
    ("engineer", "The engineer solved the complex problem.", "инженер", "Инженер решил сложную проблему."),
    ("to be surprised", "I was surprised yesterday.", "удивиться", "Я удивился вчера."),
    ("nation", "The nation is strong.", "нация", "Нация сильная."),
    ("strictly", "Follow the law strictly.", "строго", "Следуйте закону строго."),
    ("successfully", "She successfully finished the project.", "успешно", "Она успешно закончила проект."),
    ("acquaintance", "This acquaintance is important.", "знакомство", "Это знакомство важно."),
    ("diary", "She writes in her diary every night.", "дневник", "Она пишет в свой дневник каждую ночь."),
    ("to influence", "Music has the power to influence emotions.", "влиять", "Музыка имеет силу влиять на эмоции."),
    ("convince", "I managed to convince my friend.", "убедить", "Мне удалось убедить моего друга."),
    ("button", "This button is red.", "кнопка", "Эта кнопка красная."),
    ("deal", "We signed a great deal yesterday.", "сделка", "Мы заключили отличную сделку вчера."),
    ("unpleasant", "The smell was quite unpleasant.", "неприятный", "Запах был довольно неприятный."),
    ("remainder", "The remainder is on the table.", "остаток", "Остаток на столе."),
    ("aspect", "Consider every aspect carefully.", "аспект", "Тщательно рассмотрите каждый аспект."),
    ("sports", "This is a sports club.", "спортивный", "Это спортивный клуб."),
    ("software", "This is a software system.", "программный", "Это программная система."),
    ("secretary", "The secretary organized the meeting.", "секретарь", "Секретарь организовал встречу."),
    ("clarify", "Please clarify this question.", "выяснить", "Пожалуйста, выясните этот вопрос."),
    ("distribution", "The distribution of resources is important.", "распространение", "Распространение ресурсов важно."),
    ("to confess", "He decided to confess his love.", "признаться", "Он решил признаться в своей любви."),
    ("ocean", "The ocean is huge and deep.", "океан", "Океан огромный и глубокий."),
    ("infinite", "The universe seems infinite in size.", "бесконечный", "Вселенная кажется бесконечной в размерах."),
    ("to hide", "She learned to hide her feelings.", "скрывать", "Она научилась скрывать свои чувства."),
    ("visitor", "A new visitor is in the museum.", "посетитель", "Новый посетитель в музее."),
    ("to be absent", "He was absent yesterday.", "отсутствовать", "Он отсутствовал вчера."),
    ("preservation", "The preservation of nature is important.", "сохранение", "Сохранение природы важно."),
    ("painful", "It was painful.", "больно", "Было больно."),
    ("skill", "He has skill and practice.", "умение", "У него есть умение и практика."),
    ("emperor", "The emperor had absolute power.", "император", "У императора была абсолютная власть."),
    ("universe", "The universe is infinitely huge.", "вселенная", "Вселенная бесконечно огромна."),
    ("to live through", "She hoped to live through the war.", "прожить", "Она надеялась прожить войну."),
    ("acknowledgment", "His acknowledgment of the error was important.", "признание", "Его признание ошибки было важным."),
    ("governor", "The governor announced a new policy today.", "губернатор", "Губернатор объявил о новой политике сегодня."),
    ("to stop", "We need to stop.", "останавливаться", "Нам надо останавливаться."),
    ("initiative", "This is her initiative.", "инициатива", "Это её инициатива."),
    ("repair", "The car needs repair.", "ремонт", "Машине нужен ремонт."),
    ("scale", "The project's scale is huge.", "масштаб", "Масштаб проекта огромен."),
    ("to endure", "She learned to endure the pain.", "терпеть", "Она научилась терпеть боль."),
    ("fifteen", "She turned fifteen.", "пятнадцать", "Ей исполнилось пятнадцать."),
    ("to agree", "We managed to agree on a time.", "договориться", "Мы смогли договориться о времени."),
    ("to advance", "The army will advance in the morning.", "наступать", "Армия будет наступать утром."),
    ("attract", "Bright colors will attract attention.", "привлечь", "Яркие цвета привлекут внимание."),
    ("smoke", "I see smoke in the room.", "дым", "Я вижу дым в комнате."),
    ("criticism", "She received this criticism.", "критика", "Она получила эту критику."),
    ("to express", "She struggled to express her feelings.", "выражать", "Она с трудом пыталась выражать свои чувства."),
    ("payment", "The payment is tomorrow.", "оплата", "Оплата будет завтра."),
    ("extension", "The extension of the road is two kilometers.", "протяжение", "Протяжение дороги — два километра."),
    ("parameter", "This parameter is important.", "параметр", "Этот параметр важен."),
    ("lecture", "This lecture was interesting.", "лекция", "Эта лекция была интересной."),
    ("dance", "This dance is beautiful.", "танец", "Этот танец красивый."),
    ("to rejoice", "We gathered to rejoice in victory.", "радоваться", "Мы собрались, чтобы радоваться победе."),
    ("cheek", "Her cheek is cold.", "щека", "Её щека холодная."),
    ("probability", "The probability of rain is high.", "вероятность", "Вероятность дождя высока."),
    ("earn", "She worked hard to earn respect.", "заработать", "Она много работала, чтобы заработать уважение."),
    ("boundary", "We crossed the boundary.", "рубеж", "Мы перешли рубеж."),
    ("intellectual", "This is an intellectual question.", "интеллектуальный", "Это интеллектуальный вопрос."),
    ("agent", "The agent finished the deal successfully.", "агент", "Агент успешно закончил сделку."),
    ("replace", "Please replace the empty bottle.", "заменить", "Пожалуйста, замените пустую бутылку."),
    ("consent", "I need her consent.", "согласие", "Мне нужно её согласие."),
    ("criterion", "Quality is our main criterion.", "критерий", "Качество — наш главный критерий."),
    ("origin", "The origin of the universe is unknown.", "происхождение", "Происхождение вселенной неизвестно."),
    ("ether", "The message disappeared into the ether.", "эфир", "Сообщение исчезло в эфире."),
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
    return forms


RU_FUNCTION = {
    "я", "ты", "он", "она", "оно", "мы", "вы", "они", "меня", "мне", "мной",
    "тебя", "тебе", "его", "ему", "ей", "её", "ее", "нас", "нам", "вас", "вам",
    "их", "им", "мой", "моя", "мое", "моё", "мои", "твой", "твоя", "твое",
    "твоё", "твои", "наш", "нашe", "нашa", "этот", "эта", "это", "эти", "этого",
    "этой", "этому", "этим", "этих", "тот", "та", "то", "те", "свой", "своя",
    "свое", "своё", "свои", "своего", "своей", "своему", "своим", "своих",
    "свою", "был", "была", "было", "были", "будет", "будут", "есть", "нет",
    "не", "ни", "да", "на", "в", "во", "с", "со", "к", "ко", "у", "о", "об",
    "обо", "от", "до", "за", "из", "по", "про", "при", "для", "без", "над",
    "под", "перед", "через", "и", "а", "но", "или", "что", "как", "так",
    "уже", "еще", "ещё", "же", "ли", "бы", "вот", "тут", "там", "здесь",
    "очень", "уже", "только", "уже", "все", "всё", "всех", "всем", "него",
    "неё", "нее", "них", "нее", "ей", "эту", "этом", "моего", "моему",
    "моим", "моих", "мою", "моей", "нами", "вами", "тобой", "него",
}


def en_ok(text: str, extra: set[str] | None = None) -> list[str]:
    allowed = allow_en | (extra or set())
    bad = []
    for raw in re.findall(r"[A-Za-z']+", text):
        w = raw.lower().replace("'", "")
        if not w or w in allowed or w == "tv":
            continue
        if any(form in allowed for form in en_forms(w)):
            continue
        if w.endswith("ly") and w[:-2] + "l" in allowed:
            continue
        bad.append(raw)
    return bad


def ru_ok(text: str, extra: set[str] | None = None) -> list[str]:
    allowed = allow_ru | RU_FUNCTION | (extra or set())
    bad = []
    for raw in re.findall(r"[А-Яа-яЁё-]+", text):
        w = raw.replace("ё", "е").replace("Ё", "е").lower()
        if w in allowed:
            continue
        if extra and any(len(e) >= 4 and (w.startswith(e[:4]) or e.startswith(w[:4])) for e in extra):
            continue
        if any(w.startswith(lemma) or lemma.startswith(w) for lemma in allowed if len(lemma) >= 4 and len(w) >= 4):
            continue
        if any(w[: max(4, len(w) - 3)] == lemma[: max(4, len(w) - 3)] for lemma in allowed if abs(len(lemma) - len(w)) <= 4 and min(len(lemma), len(w)) >= 4):
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
        en_extra = {p for p in re.findall(r"[a-z']+", en.lower()) if p not in {"to", "be", "a", "the", "an"}}
        ru_extra = {ru.lower().replace("ё", "е")}
        for token in en_ok(en_ex, en_extra):
            leftover.append(f"{i} EN leftover {token!r}: {en_ex}")
        for token in ru_ok(ru_ex, ru_extra):
            leftover.append(f"{i} RU leftover {token!r}: {ru_ex}")
        if en.split()[0].lower() not in en_ex.lower() and en.lower() not in en_ex.lower():
            key = en.lower().replace("to ", "")
            if key not in en_ex.lower() and not any(p in en_ex.lower() for p in key.split()):
                leftover.append(f"{i}: EN example missing {en!r}")
        ru_key = ru.lower().replace("ё", "е")
        ru_ex_n = ru_ex.lower().replace("ё", "е")
        if ru_key[:4] not in ru_ex_n:
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


if __name__ == "__main__":
    main()
