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

SRC = PACK / "_chunks" / "deck_15260256_02.csv"
OUT = PACK / "_chunks" / "fixed" / "deck_15260256_02.csv"
LOG = PACK / "_chunks" / "logs" / "deck_15260256_02.txt"

FUNCTION = {
    "a", "the", "is", "be", "i", "you", "he", "she", "it", "we", "they",
    "my", "and", "or", "in", "on", "at", "to", "of", "for", "with", "from",
    "not", "his", "him", "her", "their", "them", "our", "us", "me", "am",
    "are", "was", "were", "been", "being", "this", "that", "these", "those",
    "an", "as", "by", "into", "about", "than", "then", "so", "if", "but",
    "its", "your", "dont", "don't", "ill", "i'll", "im", "i'm", "lets",
    "let's", "did", "does", "do", "will", "would", "can", "could", "must",
    "should", "have", "has", "had", "here", "there", "now", "just", "only",
    "very", "too", "also", "no", "yes", "please", "every", "all", "some",
    "any", "each", "own", "who", "what", "when", "where", "why", "how",
    "which", "because", "before", "after", "again", "once", "more", "most",
    "much", "many", "few", "little", "other", "another", "same", "such",
    "up", "down", "out", "over", "under", "off", "back", "away",
}

allow_en = {
    line.strip().lower()
    for line in (PACK / "_vocab" / "allow_en_15260256.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_ru = {
    line.strip().replace("ё", "е").lower()
    for line in (PACK / "_vocab" / "allow_ru_15260256.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_en |= FUNCTION

# (en_lemma, en_ex, ru_lemma, ru_ex)
FIXED = [
    ("trifle", "Don't worry, it's only a trifle.", "мелочь", "Не волнуйся, это только мелочь."),
    ("discipline", "Discipline is important for success.", "дисциплина", "Дисциплина важна для успеха."),
    ("at first", "At first I did not know.", "вначале", "Вначале я не знал."),
    ("airport", "Meet me at the airport.", "аэропорт", "Встреть меня в аэропорту."),
    ("on time", "He arrived on time for the meeting.", "вовремя", "Он прибыл вовремя на встречу."),
    ("myth", "The legend was only a myth.", "миф", "Легенда была только мифом."),
    ("freely", "He speaks freely.", "свободно", "Он свободно говорит."),
    ("author's", "I love the author's unique style.", "авторский", "Мне нравится уникальный авторский стиль."),
    ("knock down", "The car will knock down the tree.", "сбить", "Машина собьёт дерево."),
    ("Polish", "She loves Polish books.", "польский", "Она любит польские книги."),
    ("competitor", "He is my competitor.", "конкурент", "Он мой конкурент."),
    ("mask", "Wear a mask in the store.", "маска", "Надень маску в магазине."),
    ("complaint", "She wrote a complaint yesterday.", "жалоба", "Она написала жалобу вчера."),
    ("consumption", "Energy consumption is increasing.", "потребление", "Потребление энергии растёт."),
    ("to rely on", "I learned to rely on myself.", "опираться", "Я научился опираться на себя."),
    ("signature", "Please, add your signature here.", "подпись", "Пожалуйста, поставьте вашу подпись здесь."),
    ("transparent", "The water was transparent.", "прозрачный", "Вода была прозрачной."),
    ("aviation", "Aviation connects parts of the world.", "авиация", "Авиация связывает части мира."),
    ("cow", "The cow is in the field.", "корова", "Корова на поле."),
    ("start", "I'll start the car now.", "завести", "Я сейчас заведу машину."),
    ("to be applied", "The rule is to be applied always.", "применяться", "Правило применяется всегда."),
    ("to lie down", "I lie down early.", "ложиться", "Я ложусь рано."),
    ("insist", "I insist on this answer.", "настаивать", "Я настаиваю на этом ответе."),
    ("beverage", "I want a cold beverage.", "напиток", "Я хочу холодный напиток."),
    ("elect", "They will elect a new president soon.", "избрать", "Они скоро изберут нового президента."),
    ("liberation", "The city celebrated its liberation.", "освобождение", "Город отметил своё освобождение."),
    ("double", "I want a double coffee.", "двойной", "Я хочу двойной кофе."),
    ("written", "This is a written document.", "письменный", "Это письменный документ."),
    ("count", "The count lives in the city.", "граф", "Граф живёт в городе."),
    ("thick", "The forest is thick.", "густой", "Лес густой."),
    ("Roman", "The Roman Empire was strong.", "римский", "Римская империя была сильной."),
    ("fold", "I will fold the paper.", "сложить", "Я сложу бумагу."),
    ("studio", "She has a studio for work.", "студия", "У неё есть студия для работы."),
    ("arrival", "His arrival was unexpected.", "приход", "Его приход был неожиданным."),
    ("Kremlin", "The Kremlin is in Moscow.", "кремль", "Кремль в Москве."),
    ("reflection", "The lake's reflection is clear.", "отражение", "Отражение озера ясное."),
    ("on the eve", "On the eve of the exam, she studied.", "накануне", "Накануне экзамена она училась."),
    ("measurement", "We need this measurement.", "измерение", "Нам нужно это измерение."),
    ("celestial", "He can see celestial bodies.", "небесный", "Он видит небесные тела."),
    ("genuine", "This is a genuine gold ring.", "подлинный", "Это подлинное золотое кольцо."),
    ("noticeably", "He was noticeably quiet.", "заметно", "Он был заметно тихим."),
    ("separately", "We live separately.", "отдельно", "Мы живём отдельно."),
    ("fulfill", "She will fulfill her promise.", "исполнить", "Она исполнит своё обещание."),
    ("restore", "We must restore the old building.", "восстановить", "Мы восстановим старое здание."),
    ("preliminary", "The preliminary results are good.", "предварительный", "Предварительные результаты хорошие."),
    ("sincerely", "I sincerely thank you.", "искренне", "Я искренне благодарю вас."),
    ("to care", "She learned to care for plants.", "заботиться", "Она научилась заботиться о растениях."),
    ("get rid of", "We must get rid of this problem.", "избавиться", "Мы должны избавиться от этой проблемы."),
    ("hide", "I must hide the gift.", "скрыть", "Я должен скрыть подарок."),
    ("ecological", "Ecological problems are important.", "экологический", "Экологические проблемы важны."),
    ("pray", "I pray every night.", "молиться", "Я молюсь каждую ночь."),
    ("novella", "She published her first novella.", "повесть", "Она опубликовала свою первую повесть."),
    ("component", "This component is important.", "компонент", "Этот компонент важен."),
    ("violate", "They did not violate the agreement.", "нарушить", "Они не нарушили соглашение."),
    ("pride", "Her pride was clear.", "гордость", "Её гордость была ясной."),
    ("bride", "The bride looked beautiful.", "невеста", "Невеста выглядела красивой."),
    ("lead away", "The officer will lead away the man.", "отвести", "Офицер отведёт человека."),
    ("contribution", "His contribution changed the project's course.", "вклад", "Его вклад изменил ход проекта."),
    ("to prove", "He worked hard to prove this.", "доказывать", "Он много работал, чтобы доказать это."),
    ("to be observed", "Such problems are observed often.", "наблюдаться", "Такие проблемы часто наблюдаются."),
    ("deaf", "He is deaf in one ear.", "глухой", "Он глухой на одно ухо."),
    ("metal", "Iron is a strong metal.", "металл", "Железо — сильный металл."),
    ("incorrect", "Your answer is incorrect.", "неправильный", "Ваш ответ неправильный."),
    ("brief", "Keep the explanation brief, please.", "краткий", "Пожалуйста, дайте краткое объяснение."),
    ("suitable", "This is a suitable dress.", "подходящий", "Это подходящее платье."),
    ("accompany", "She will accompany me to the store.", "сопровождать", "Она будет сопровождать меня в магазин."),
    ("theoretical", "Theoretical knowledge differs from practical.", "теоретический", "Теоретические знания отличаются от практических."),
    ("stay", "My stay at the hotel is good.", "пребывание", "Моё пребывание в гостинице хорошее."),
    ("lie", "He told a harmful lie.", "ложь", "Он сказал вредную ложь."),
    ("catastrophe", "The war was a major catastrophe.", "катастрофа", "Война была большой катастрофой."),
    ("environment", "He grew up in a good environment.", "окружение", "Он вырос в хорошем окружении."),
    ("processor", "The processor is new.", "процессор", "Процессор новый."),
    ("fair", "Life is not always fair.", "справедливый", "Жизнь не всегда справедлива."),
    ("profile", "He changed his profile picture.", "профиль", "Он изменил фотографию профиля."),
    ("quarter", "I live in a quiet quarter.", "квартал", "Я живу в тихом квартале."),
    ("legislative", "The legislative body passed a new law.", "законодательный", "Законодательный орган принял новый закон."),
    ("exploitation", "The book showed workers' exploitation.", "эксплуатация", "Книга показала эксплуатацию рабочих."),
    ("little house", "The little house is blue.", "домик", "Домик синий."),
    ("metallic", "The door has a metallic color.", "металлический", "У двери металлический цвет."),
    ("wonderful", "She had a wonderful smile.", "чудесный", "У неё была чудесная улыбка."),
    ("servant", "The king has a good servant.", "слуга", "У короля есть хороший слуга."),
    ("decisively", "She spoke decisively.", "решительно", "Она говорила решительно."),
    ("critical", "This is a critical moment.", "критический", "Это критический момент."),
    ("activist", "The activist fights for justice.", "активист", "Активист борется за справедливость."),
    ("to advise", "I want to advise you.", "посоветовать", "Я хочу посоветовать вам."),
    ("steering wheel", "He held the steering wheel.", "руль", "Он держал руль."),
    ("sixth", "He finished sixth.", "шестой", "Он закончил шестым."),
    ("pancake", "I made a pancake for breakfast.", "блин", "Я сделал блин на завтрак."),
    ("twice", "I called him twice today.", "дважды", "Я звонил ему дважды сегодня."),
    ("to descend", "We began to descend the mountain.", "спускаться", "Мы начали спускаться с горы."),
    ("candle", "The candle is on the table.", "свеча", "Свеча на столе."),
    ("bear", "The bear found a large fish.", "медведь", "Медведь нашёл большую рыбу."),
    ("operational", "We need operational measures.", "оперативный", "Нам нужны оперативные меры."),
    ("upstairs", "I go upstairs.", "наверх", "Я иду наверх."),
    ("forecast", "The weather forecast looks good.", "прогноз", "Прогноз погоды выглядит хорошим."),
    ("survey", "We conducted a survey yesterday.", "опрос", "Мы провели опрос вчера."),
    ("interlocutor", "My interlocutor nodded in agreement.", "собеседник", "Мой собеседник кивнул в знак согласия."),
    ("elderly", "The elderly man walked home.", "пожилой", "Пожилой человек шёл домой."),
    ("spouse", "My spouse is at home.", "супруг", "Мой супруг дома."),
    ("to install", "I need to install new software.", "устанавливать", "Мне нужно установить новую программу."),
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


def en_ok(text: str) -> list[str]:
    bad = []
    for raw in re.findall(r"[A-Za-z']+", text):
        w = raw.lower().replace("'", "")
        if not w or w in allow_en:
            continue
        if any(form in allow_en for form in en_forms(w)):
            continue
        if w.endswith("ly") and w[:-2] + "l" in allow_en:
            continue
        bad.append(raw)
    return bad


def ru_ok(text: str) -> list[str]:
    bad = []
    for raw in re.findall(r"[А-Яа-яЁё-]+", text):
        w = raw.replace("ё", "е").replace("Ё", "е").lower()
        if w in allow_ru:
            continue
        if any(w.startswith(lemma) or lemma.startswith(w) for lemma in allow_ru if len(lemma) >= 4 and len(w) >= 4):
            continue
        if any(w[: max(4, len(w) - 3)] == lemma[: max(4, len(w) - 3)] for lemma in allow_ru if abs(len(lemma) - len(w)) <= 4 and min(len(lemma), len(w)) >= 4):
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
        for token in en_ok(en_ex):
            leftover.append(f"{i} EN leftover {token!r}: {en_ex}")
        for token in ru_ok(ru_ex):
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
