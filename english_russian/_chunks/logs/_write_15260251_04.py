#!/usr/bin/env python3
from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from brainscape.cards import card_write_payload, cards_from_path, cards_match

SRC = ROOT / "english_russian/_chunks/deck_15260251_04.csv"
OUT = ROOT / "english_russian/_chunks/fixed/deck_15260251_04.csv"
LOG = ROOT / "english_russian/_chunks/logs/deck_15260251_04.txt"

# (en_lemma, ru_lemma, en_example, ru_example)
CARDS = [
    ("to step on", "наступить", "Do not step on the dog.", "Не наступите на собаку."),
    ("hello", "привет", "Hello, how are you today?", "Привет, как ты сегодня?"),
    ("package", "пакет", "I received a package today.", "Я получил пакет сегодня."),
    ("viewer", "зритель", "The viewer watched the movie.", "Зритель смотрел фильм."),
    ("to dream", "мечтать", "She loves to dream.", "Она любит мечтать."),
    ("turn into", "превратиться", "The boy will turn into a man.", "Мальчик превратится в мужчину."),
    ("restaurant", "ресторан", "We were at a restaurant.", "Мы были в ресторане."),
    ("fee", "плата", "The fee was high.", "Плата была высокой."),
    ("legislation", "законодательство", "New legislation was finally passed.", "Новое законодательство наконец было принято."),
    ("moon", "луна", "The moon is bright at night.", "Луна ночью яркая."),
    ("extremely", "крайне", "She was extremely happy.", "Она была крайне счастлива."),
    ("security", "охрана", "The museum has security.", "В музее есть охрана."),
    ("publication", "публикация", "I read this publication.", "Я прочитал эту публикацию."),
    ("nod", "кивнуть", "She nodded.", "Она кивнула."),
    ("discuss", "обсуждать", "Let's discuss this tomorrow.", "Давайте обсудим это завтра."),
    ("for sure", "наверняка", "He will come, for sure.", "Он наверняка придёт."),
    ("logic", "логика", "I see no logic.", "Я не вижу логики."),
    ("specially", "специально", "I did this specially for you.", "Я сделал это специально для тебя."),
    ("to be held", "проводиться", "The meeting will be held tomorrow.", "Встреча будет проводиться завтра."),
    ("blue", "синий", "The sky is blue today.", "Небо сегодня синее."),
    ("essence", "сущность", "I understand the essence of the question.", "Я понимаю сущность вопроса."),
    ("to give back", "отдавать", "I promised to give back his book.", "Я пообещал отдать его книгу."),
    ("mirror", "зеркало", "She looked into the mirror.", "Она посмотрела в зеркало."),
    ("along", "вдоль", "Walk along the river.", "Пройдите вдоль реки."),
    ("final", "конечный", "This is the final answer.", "Это конечный ответ."),
    ("reverse", "обратный", "This is the reverse side.", "Это обратная сторона."),
    ("palm", "ладонь", "She held the book in her palm.", "Она держала книгу в ладони."),
    ("distant", "дальний", "The distant mountains looked beautiful.", "Дальние горы выглядели красивыми."),
    ("gate", "ворота", "Open the gate for the guests.", "Откройте ворота для гостей."),
    ("to transmit", "передавать", "We need to transmit this message.", "Нам нужно передать это сообщение."),
    ("continue", "продолжить", "Let's continue our discussion tomorrow.", "Давайте продолжим наше обсуждение завтра."),
    ("dream", "мечта", "This is my dream.", "Это моя мечта."),
    ("nutrition", "питание", "Nutrition is important for health.", "Питание важно для здоровья."),
    ("profit", "прибыль", "The company reported a significant profit.", "Компания сообщила о значительной прибыли."),
    ("file", "файл", "I opened the file yesterday.", "Я открыл файл вчера."),
    ("fleet", "флот", "The fleet is at sea.", "Флот в море."),
    ("religion", "религия", "Religion is important in his life.", "Религия важна в его жизни."),
    ("God's", "божий", "This is God's house.", "Это божий дом."),
    ("plus", "плюс", "Two plus two equals four.", "Два плюс два равно четыре."),
    ("cat", "кошка", "The cat slept on the chair.", "Кошка спала на стуле."),
    ("characteristic", "характерный", "This is a characteristic feature.", "Это характерная особенность."),
    ("fat", "толстый", "The cat is fat.", "Кошка толстая."),
    ("communicate", "общаться", "We communicate every day.", "Мы общаемся каждый день."),
    ("fifth", "пятый", "This is the fifth day.", "Это пятый день."),
    ("hang", "висеть", "Pictures hang on the wall.", "Картины висят на стене."),
    ("contribute", "способствовать", "They contribute to our success.", "Они способствуют нашему успеху."),
    ("excellent", "отличный", "Your work was excellent.", "Ваша работа была отличной."),
    ("reserve", "запас", "We have a reserve of water.", "У нас есть запас воды."),
    ("wing", "крыло", "The bird has a wing.", "У птицы есть крыло."),
    ("editor", "редактор", "The editor read the article.", "Редактор прочитал статью."),
    ("tone", "тон", "Her voice had a quiet tone.", "Её голос имел тихий тон."),
    ("defense", "оборона", "The castle's defense was strong.", "Оборона замка была сильной."),
    ("colonel", "полковник", "The colonel spoke to the soldiers.", "Полковник говорил с солдатами."),
    ("neighboring", "соседний", "This is a neighboring house.", "Это соседний дом."),
    ("release", "выпустить", "They will release the book tomorrow.", "Они выпустят книгу завтра."),
    ("worthy", "достойный", "He is worthy of respect.", "Он достоин уважения."),
    ("crisis", "кризис", "This is a deep crisis.", "Это глубокий кризис."),
    ("to hurry", "спешить", "I need to hurry.", "Мне нужно спешить."),
    ("dispute", "спор", "They have a dispute.", "У них есть спор."),
    ("to be done", "делаться", "The work is being done.", "Работа делается."),
    ("lake", "озеро", "We were by the lake.", "Мы были у озера."),
    ("wild", "дикий", "The forest was wild.", "Лес был дикий."),
    ("round", "круглый", "The table is round.", "Стол круглый."),
    ("bottom", "дно", "I see the bottom.", "Я вижу дно."),
    ("to turn around", "повернуться", "She turned around slowly.", "Она медленно повернулась."),
    ("younger", "младший", "He is my younger brother.", "Он мой младший брат."),
    ("acceptance", "принятие", "This is acceptance of the offer.", "Это принятие предложения."),
    ("expert", "эксперт", "He is an expert.", "Он эксперт."),
    ("destroy", "уничтожить", "Fire can quickly destroy a forest.", "Огонь может быстро уничтожить лес."),
    ("to hit", "попадать", "He wants to hit the goal.", "Он хочет попасть в цель."),
    ("joint", "совместный", "This is our joint work.", "Это наша совместная работа."),
    ("warm", "тепло", "It is warm in the house.", "В доме тепло."),
    ("north", "север", "We are in the north.", "Мы на севере."),
    ("individual", "индивидуальный", "Every student has an individual plan.", "У каждого студента индивидуальный план."),
    ("darkness", "темнота", "I cannot see in the darkness.", "Я не вижу в темноте."),
    ("breath", "дыхание", "His breath is deep.", "Его дыхание глубокое."),
    ("concert", "концерт", "I was at a concert yesterday.", "Я был на концерте вчера."),
    ("minimum", "минимум", "This is the minimum.", "Это минимум."),
    ("experiment", "эксперимент", "Let's start the experiment now.", "Давайте начнем эксперимент сейчас."),
    ("regional", "региональный", "This is a regional center.", "Это региональный центр."),
    ("negotiations", "переговоры", "The negotiations were long.", "Переговоры были долгими."),
    ("interview", "интервью", "She prepared for the interview.", "Она подготовилась к интервью."),
    ("agency", "агентство", "She works for an agency.", "Она работает в агентстве."),
    ("purchase", "покупка", "I made a purchase on the internet yesterday.", "Вчера я сделал покупку в интернете."),
    ("weather", "погода", "The weather today is good.", "Погода сегодня хорошая."),
    ("limitation", "ограничение", "Every rule has its limitation.", "Каждое правило имеет своё ограничение."),
    ("upbringing", "воспитание", "Her upbringing was good.", "Её воспитание было хорошим."),
    ("Chinese", "китайский", "I love Chinese food.", "Я люблю китайскую еду."),
    ("trend", "тенденция", "The trend is clear.", "Тенденция ясная."),
    ("sin", "грех", "This is a sin.", "Это грех."),
    ("manufacturer", "производитель", "The manufacturer released a new model.", "Производитель выпустил новую модель."),
    ("joke", "шутка", "That was a good joke.", "Это была хорошая шутка."),
    ("wake up", "проснуться", "I woke up early.", "Я проснулся рано."),
    ("attack", "атака", "The army began the attack.", "Армия начала атаку."),
    ("registration", "регистрация", "Registration opens tomorrow.", "Регистрация открывается завтра."),
    ("report", "доклад", "She presented her report confidently.", "Она уверенно представила свой доклад."),
    ("cell", "клетка", "This is a cell of the body.", "Это клетка тела."),
    ("candidate", "кандидат", "The candidate prepared for the meeting.", "Кандидат подготовился к встрече."),
    ("symbol", "символ", "The star is a symbol.", "Звезда — это символ."),
    ("everywhere", "везде", "Cats are everywhere in the city.", "В городе везде кошки."),
]


def payload_for(en: str, ru: str, en_ex: str, ru_ex: str) -> dict[str, str]:
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
    original = cards_from_path(SRC)
    if len(original) != 100:
        raise SystemExit(f"expected 100 source cards, got {len(original)}")
    if len(CARDS) != 100:
        raise SystemExit(f"expected 100 rewritten cards, got {len(CARDS)}")

    rows = []
    changed = 0
    for i, (en, ru, en_ex, ru_ex) in enumerate(CARDS):
        src = original[i]
        if src.get("qMdBody") != en:
            raise SystemExit(f"order mismatch at {i+1}: {src.get('qMdBody')!r} vs {en!r}")
        new = payload_for(en, ru, en_ex, ru_ex)
        if not cards_match(src, new):
            changed += 1
        rows.append(new)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8", newline="\n") as fh:
        writer = csv.writer(fh, lineterminator="\n")
        writer.writerow(["Question", "Answer"])
        for card in rows:
            writer.writerow([card["question"], card["answer"]])

    written = cards_from_path(OUT)
    if len(written) != 100:
        raise SystemExit(f"cards_from_path returned {len(written)}")
    for i, card in enumerate(written):
        expect = rows[i]
        if not cards_match(card, expect):
            raise SystemExit(f"round-trip mismatch at card {i+1}")

    LOG.write_text(f"{changed}\n", encoding="utf-8")
    print(f"wrote {OUT}")
    print(f"cards_from_path: {len(written)}")
    print(f"changed: {changed}")


if __name__ == "__main__":
    main()
