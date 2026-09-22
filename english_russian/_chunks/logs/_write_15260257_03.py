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

SRC = PACK / "_chunks" / "deck_15260257_03.csv"
OUT = PACK / "_chunks" / "fixed" / "deck_15260257_03.csv"
LOG = PACK / "_chunks" / "logs" / "deck_15260257_03.txt"

FUNCTION = {
    "a", "the", "is", "be", "i", "you", "he", "she", "it", "we", "they",
    "my", "and", "or", "in", "on", "at", "to", "of", "for", "with", "from",
    "not", "his", "him", "her", "their", "them", "our", "us", "me", "am",
    "are", "was", "were", "been", "being", "this", "that", "these", "those",
    "an", "as", "by", "into", "about", "than", "then", "so", "if", "but",
    "its", "your", "im", "lets", "let", "do", "did", "does", "done",
    "have", "has", "had", "will", "would", "can", "could", "must", "should",
    "may", "might", "shall", "here", "there", "now", "just", "very", "too",
    "also", "only", "even", "still", "already", "yet", "again", "once",
    "some", "any", "no", "all", "each", "every", "both", "few", "more",
    "most", "other", "another", "such", "own", "same", "new", "old",
}

allow_en = {
    line.strip().lower()
    for line in (PACK / "_vocab" / "allow_en_15260257.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_ru = {
    line.strip().replace("ё", "е").lower()
    for line in (PACK / "_vocab" / "allow_ru_15260257.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_en |= FUNCTION

# (en_lemma, en_ex, ru_lemma, ru_ex)
FIXED = [
    ("riddle", "Life is a complex riddle.", "загадка", "Жизнь - это сложная загадка."),
    ("whisper", "She will whisper a secret this evening.", "прошептать", "Она прошепчет секрет сегодня вечером."),
    ("mad", "He was mad with power.", "безумный", "Он был безумен от власти."),
    ("minus", "Temperature dropped to minus five.", "минус", "Температура упала до минус пяти."),
    ("reduce", "We need to reduce the risk to a minimum.", "свести", "Нам нужно свести риск к минимуму."),
    ("to retreat", "The army decided to retreat quickly.", "отходить", "Армия решила быстро отходить."),
    ("dose", "Take your dose of medicine now.", "доза", "Прими сейчас свою дозу лекарства."),
    ("pathetic", "His words were simply pathetic.", "жалкий", "Его слова были просто жалкими."),
    ("penetrate", "Light can penetrate thin fabric.", "проникнуть", "Свет может проникнуть через тонкую ткань."),
    ("retain", "We must retain our employees.", "удержать", "Нам нужно удержать наших сотрудников."),
    ("performer", "The performer sang a song.", "исполнитель", "Исполнитель пел песню."),
    ("get a job", "He needs to get a job soon.", "устроиться", "Ему нужно скоро устроиться на работу."),
    ("popularity", "His popularity grew quickly.", "популярность", "Его популярность быстро выросла."),
    ("to drive past", "I decided to drive past her house.", "проехать", "Я решил проехать мимо её дома."),
    ("enjoy", "Enjoy your food!", "наслаждаться", "Наслаждайтесь едой!"),
    ("diploma", "She showed her diploma.", "диплом", "Она показала свой диплом."),
    ("to drag", "I had to drag the suitcase.", "тащить", "Мне пришлось тащить чемодан."),
    ("automotive", "I love automotive design.", "автомобильный", "Я люблю автомобильный дизайн."),
    ("morality", "Morality is important for people.", "мораль", "Мораль важна для людей."),
    ("trash", "Take out the trash this evening.", "мусор", "Вынеси мусор сегодня вечером."),
    ("propaganda", "I do not believe this propaganda.", "пропаганда", "Я не верю этой пропаганде."),
    ("beard", "He has a big beard.", "борода", "У него большая борода."),
    ("tariff", "The new tariff made prices high.", "тариф", "Новый тариф сделал цены высокими."),
    ("to chat", "We chat every evening.", "беседовать", "Мы беседуем каждый вечер."),
    ("detailed", "He gave a detailed explanation.", "подробный", "Он дал подробное объяснение."),
    ("patience", "I need patience now.", "терпение", "Мне сейчас нужно терпение."),
    ("robot", "The robot completed its task efficiently.", "робот", "Робот эффективно выполнил свою задачу."),
    ("to listen to", "I promised to listen to her story.", "выслушать", "Я пообещал выслушать её историю."),
    ("delete", "Please delete this file immediately.", "удалить", "Пожалуйста, удалите этот файл сейчас."),
    ("frankly", "Frankly, I do not like the results.", "откровенно", "Откровенно говоря, мне не нравятся результаты."),
    ("selection", "The team's selection was strict.", "отбор", "Отбор команды был строгим."),
    ("fatigue", "I feel extreme fatigue.", "усталость", "Я чувствую крайнюю усталость."),
    ("fall out", "My tooth will fall out soon.", "выпасть", "Мой зуб скоро выпадет."),
    ("to fall in love", "I want to fall in love.", "полюбить", "Я хочу полюбить."),
    ("sincere", "His words were sincere.", "искренний", "Его слова были искренними."),
    ("knight", "The knight protected the village.", "рыцарь", "Рыцарь защитил деревню."),
    ("on duty", "The doctor on duty came.", "дежурный", "Дежурный врач пришёл."),
    ("deny", "He cannot deny this fact.", "отрицать", "Он не может отрицать этот факт."),
    ("stand out", "Her dress made her stand out.", "выделяться", "Её платье заставило её выделяться."),
    ("particle", "A particle can be very small.", "частица", "Частица может быть очень маленькой."),
    ("dynamics", "The dynamics of the market are new.", "динамика", "Динамика рынка новая."),
    ("elbow", "He hit his elbow on the table.", "локоть", "Он ударил локоть о стол."),
    ("merit", "This is a great merit.", "заслуга", "Это большая заслуга."),
    ("transformation", "The city's transformation was fast.", "преобразование", "Преобразование города было быстрым."),
    ("regulation", "The new regulation is important.", "регулирование", "Новое регулирование важное."),
    ("formal", "This is only a formal requirement.", "формальный", "Это только формальное требование."),
    ("spoil", "The rain will spoil our day.", "испортить", "Дождь испортит наш день."),
    ("living room", "We sat in the living room.", "гостиная", "Мы сидели в гостиной."),
    ("shock", "The news gave her a shock.", "шок", "Новость дала ей шок."),
    ("tour", "We went on a tour.", "тур", "Мы пошли в тур."),
    ("bandit", "The bandit stole the gold.", "бандит", "Бандит украл золото."),
    ("yield", "I will yield to you.", "уступать", "Я уступлю тебе."),
    ("bill", "The government passed the bill.", "законопроект", "Правительство приняло законопроект."),
    ("closeness", "I feel closeness to my family.", "близость", "Я чувствую близость к своей семье."),
    ("guitar", "He played the guitar.", "гитара", "Он играл на гитаре."),
    ("balcony", "She stood on the balcony.", "балкон", "Она стояла на балконе."),
    ("to explain", "He came to explain himself.", "объясняться", "Он пришёл, чтобы объясниться."),
    ("shield", "The knight raised his shield.", "щит", "Рыцарь поднял свой щит."),
    ("all possible", "Look at all possible solutions.", "всевозможный", "Смотрите всевозможные решения."),
    ("to guess", "I tried to guess her age.", "догадываться", "Я пытался догадаться о её возрасте."),
    ("inspect", "Please inspect the car thoroughly.", "осмотреть", "Пожалуйста, тщательно осмотрите машину."),
    ("attraction", "They work on the attraction of students.", "привлечение", "Они работают над привлечением студентов."),
    ("graduate", "He is a school graduate.", "выпускник", "Он выпускник школы."),
    ("real estate", "He bought real estate.", "недвижимость", "Он купил недвижимость."),
    ("monk", "The monk prayed.", "монах", "Монах молился."),
    ("kiss", "Their first kiss was magical.", "поцелуй", "Их первый поцелуй был волшебным."),
    ("forgiveness", "I want forgiveness.", "прощение", "Я хочу прощения."),
    ("to accuse", "He began to accuse her.", "обвинять", "Он начал обвинять её."),
    ("championship", "This championship is important.", "чемпионат", "Этот чемпионат важный."),
    ("artillery", "The artillery started at dawn.", "артиллерия", "Артиллерия начала на рассвете."),
    ("involuntarily", "He involuntarily smiled at the joke.", "невольно", "Он невольно улыбнулся шутке."),
    ("delivery", "Your delivery has arrived.", "доставка", "Ваша доставка прибыла."),
    ("shade", "I love this shade of blue.", "оттенок", "Мне нравится этот оттенок синего."),
    ("prize", "She received a prize.", "приз", "Она получила приз."),
    ("receipt", "The receipt of funds was late.", "поступление", "Поступление средств было поздним."),
    ("hypothesis", "His hypothesis is interesting.", "гипотеза", "Его гипотеза интересная."),
    ("stand", "Let's stand here for a minute.", "постоять", "Давайте постоим здесь минуту."),
    ("to command", "He learned to command a ship.", "командовать", "Он научился командовать кораблём."),
    ("colony", "This country was a colony.", "колония", "Эта страна была колонией."),
    ("in view of", "In view of this, we will wait.", "ввиду", "Ввиду этого мы будем ждать."),
    ("magician", "The magician showed his power.", "маг", "Маг показал свою силу."),
    ("departure", "His departure was at noon.", "отъезд", "Его отъезд был в полдень."),
    ("score", "He wants to score now.", "забить", "Он хочет забить сейчас."),
    ("placement", "The placement of furniture is important.", "размещение", "Размещение мебели важное."),
    ("to pity", "I will pity him.", "пожалеть", "Я пожалею его."),
    ("to wound", "He wanted to wound, not kill.", "ранить", "Он хотел ранить, а не убить."),
    ("excite", "This idea will excite interest.", "возбудить", "Эта идея возбудит интерес."),
    ("theatrical", "Her gestures were theatrical.", "театральный", "Её жесты были театральными."),
    ("slogan", "Every party needs a slogan.", "лозунг", "Каждой партии нужно иметь лозунг."),
    ("get out", "We must get out of here.", "выбраться", "Нам нужно выбраться отсюда."),
    ("to examine", "She wanted to examine the picture.", "разглядывать", "Она хотела разглядывать картину."),
    ("sweat", "I feel sweat on my face.", "пот", "Я чувствую пот на лице."),
    ("for a long time", "He left for a long time.", "надолго", "Он ушел надолго."),
    ("entertainment", "Movies are my favorite entertainment.", "развлечение", "Фильмы - моё любимое развлечение."),
    ("folder", "I organized my documents in a folder.", "папка", "Я организовал свои документы в папке."),
    ("dishes", "I washed the dishes yesterday.", "посуда", "Я мыл посуду вчера."),
    ("arrow", "Follow the arrow to the exit.", "стрелка", "Следуйте за стрелкой к выходу."),
    ("denote", "These signs will denote danger.", "обозначить", "Эти знаки обозначат опасность."),
    ("principal", "This is the principal question.", "главный", "Это главный вопрос."),
    ("phase", "This is only a phase.", "фаза", "Это только фаза."),
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
        if not w or w in allow_en or w == "tv":
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
