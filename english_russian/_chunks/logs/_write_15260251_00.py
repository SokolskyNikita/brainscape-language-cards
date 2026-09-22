#!/usr/bin/env python3
"""Rewrite deck_15260251_00 (band 1000->1500, cards 1-100)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REPO = ROOT.parent
sys.path.insert(0, str(REPO))

import csv  # noqa: E402

from brainscape.cards import card_write_payload, cards_from_path  # noqa: E402


def write_csv(path: Path, cards: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh, lineterminator="\n")
        writer.writerow(["Question", "Answer"])
        for card in cards:
            payload = card_write_payload(card)
            writer.writerow([payload["question"], payload["answer"]])

# (english gloss, russian lemma, english example, russian example)
# None example = keep the original footnote for that face.
FIXES: list[tuple[str, str, str | None, str | None]] = [
    ("garden", "сад", "I love my garden.", "Я люблю свой сад."),
    ("kitchen", "кухня", None, None),
    ("pocket", "карман", "He found a key in his pocket.", "Он нашёл ключ в своём кармане."),
    ("childhood", "детство", "I remember my childhood.", "Я помню своё детство."),
    ("doubt", "сомнение", "I have no doubt.", "У меня нет сомнения."),
    ("hundred", "сотня", "I have a hundred dollars.", "У меня есть сотня долларов."),
    ("plot", "участок", "They bought a plot near the house.", "Они купили участок рядом с домом."),
    ("promise", "обещать", "I promise to come.", "Я обещаю прийти."),
    ("according to", "согласно", "According to the law, this is true.", "Согласно закону, это правда."),
    (
        "construction",
        "строительство",
        "Construction of the house began today.",
        "Строительство дома началось сегодня.",
    ),
    ("beer", "пиво", "I drink cold beer every day.", "Я пью холодное пиво каждый день."),
    (
        "disappear",
        "исчезнуть",
        "The man disappeared in the darkness.",
        "Человек исчез в темноте.",
    ),
    ("thin", "тонкий", "The paper is thin.", "Бумага тонкая."),
    (
        "forgive",
        "простить",
        "Please forgive my late answer.",
        "Пожалуйста, простите мой поздний ответ.",
    ),
    ("device", "устройство", "The device does not work.", "Устройство не работает."),
    ("laugh", "смеяться", "We laughed loudly.", "Мы громко смеялись."),
    ("rich", "богатый", "He became a rich man.", "Он стал богатым человеком."),
    ("bright", "яркий", "The stars were bright at night.", "Звёзды были яркими ночью."),
    (
        "to correspond",
        "соответствовать",
        "This does not correspond to the fact.",
        "Это не соответствует факту.",
    ),
    ("tear", "слеза", "A tear fell from her eye.", "Слеза упала из её глаза."),
    ("agreeable", "согласный", None, None),
    ("library", "библиотека", None, None),
    ("communication", "общение", "Communication is important.", "Общение важно."),
    (
        "particularity",
        "частность",
        "I see this particularity in his work.",
        "Я вижу эту частность в его работе.",
    ),
    (
        "to fulfill",
        "выполнить",
        "He promised to fulfill her wish.",
        "Он обещал выполнить её желание.",
    ),
    ("faithful", "верный", None, None),
    ("difference", "отличие", "I see the difference.", "Я вижу отличие."),
    ("train", "поезд", "The train came in the morning.", "Поезд пришёл утром."),
    ("official", "официальный", "This is official news.", "Это официальная новость."),
    ("products", "продукция", "Their products are good.", "Их продукция хорошая."),
    (
        "application",
        "применение",
        "The application of knowledge is important.",
        "Применение знаний важно.",
    ),
    ("tsar", "царь", "The tsar had great power.", "У царя была большая власть."),
    (
        "take place",
        "состояться",
        "The concert will take place today.",
        "Концерт состоится сегодня.",
    ),
    ("stream", "поток", None, None),
    ("benefit", "польза", "There is benefit in this work.", "В этой работе есть польза."),
    (
        "to interfere",
        "мешать",
        "Do not interfere with my work.",
        "Не мешай моей работе.",
    ),
    ("cross", "перейти", "We must cross the street.", "Мы должны перейти улицу."),
    ("mood", "настроение", "Her mood is good.", "У неё хорошее настроение."),
    (
        "gradually",
        "постепенно",
        "He gradually understood this.",
        "Он постепенно понял это.",
    ),
    (
        "editorial office",
        "редакция",
        "I work in the editorial office.",
        "Я работаю в редакции.",
    ),
    (
        "something",
        "нечто",
        "I felt something in the darkness.",
        "Я чувствовал нечто в темноте.",
    ),
    ("crowd", "толпа", "The crowd was in the street.", "Толпа была на улице."),
    ("healthy", "здоровый", "He has a healthy body.", "У него здоровое тело."),
    ("planet", "планета", "Earth is a planet.", "Земля — планета."),
    ("generation", "поколение", "This is a new generation.", "Это новое поколение."),
    ("reaction", "реакция", "His reaction was calm.", "Его реакция была спокойной."),
    ("smart", "умный", None, None),
    ("mechanism", "механизм", "This mechanism is complex.", "Этот механизм сложный."),
    ("actually", "собственно", "Actually, I want tea.", "Собственно, я хочу чай."),
    ("bird", "птица", None, None),
    (
        "relatively",
        "относительно",
        "The price is relatively high.",
        "Цена относительно высокая.",
    ),
    ("household", "хозяйство", "This is my household.", "Это моё хозяйство."),
    (
        "victim",
        "жертва",
        "He became a victim of the crime.",
        "Он стал жертвой преступления.",
    ),
    ("to open", "открывать", None, None),
    ("pronounce", "произнести", None, None),
    (
        "organism",
        "организм",
        "Every organism plays a vital role.",
        "Каждый организм играет жизненную роль.",
    ),
    (
        "achievement",
        "достижение",
        "This was a great achievement.",
        "Это было великое достижение.",
    ),
    ("up", "вверх", None, None),
    ("bottle", "бутылка", None, None),
    ("recognize", "признать", "I recognize this fact.", "Я признаю этот факт."),
    (
        "to define",
        "определять",
        "How do you define this word?",
        "Как вы определяете это слово?",
    ),
    ("brain", "мозг", None, None),
    (
        "drawing",
        "рисунок",
        "She saw a beautiful drawing.",
        "Она видела красивый рисунок.",
    ),
    ("museum", "музей", "We were at the museum yesterday.", "Мы были в музее вчера."),
    (
        "dependence",
        "зависимость",
        "This is a strong dependence.",
        "Это сильная зависимость.",
    ),
    ("rain", "дождь", "Rain is falling today.", "Сегодня идёт дождь."),
    ("implementation", "реализация", None, None),
    ("smile", "улыбка", "She has a beautiful smile.", "У неё красивая улыбка."),
    ("east", "восток", "The sun is in the east.", "Солнце на востоке."),
    ("to smile", "улыбнуться", "She wanted to smile.", "Она хотела улыбнуться."),
    ("bread", "хлеб", "I bought fresh bread today.", "Я купил свежий хлеб сегодня."),
    (
        "grandmother",
        "бабушка",
        "My grandmother lives here.",
        "Моя бабушка живёт здесь.",
    ),
    ("shadow", "тень", "I see the shadow of the tree.", "Я вижу тень дерева."),
    ("to experience", "испытывать", "I experience fear.", "Я испытываю страх."),
    (
        "to assume",
        "полагать",
        "I assume that this is true.",
        "Я полагаю, что это правда.",
    ),
    (
        "today's",
        "сегодняшний",
        "Today's weather is warm.",
        "Сегодняшняя погода тёплая.",
    ),
    ("active", "активный", "She is an active woman.", "Она активная женщина."),
    (
        "receiving",
        "получение",
        "Receiving the letter was important.",
        "Получение письма было важным.",
    ),
    ("dangerous", "опасный", "This is a dangerous place.", "Это опасное место."),
    (
        "announce",
        "объявить",
        "They will announce the news soon.",
        "Они скоро объявят новость.",
    ),
    ("skin", "кожа", "Her skin is white.", "Её кожа белая."),
    ("electronic", "электронный", None, None),
    ("marine", "морской", "This is a marine animal.", "Это морское животное."),
    (
        "violation",
        "нарушение",
        "This is a violation of the law.",
        "Это нарушение закона.",
    ),
    ("ensure", "обеспечить", "We must ensure safety.", "Мы должны обеспечить безопасность."),
    ("horror", "ужас", "She screamed in horror.", "Она кричала от ужаса."),
    ("act", "акт", "Please read the act.", "Пожалуйста, прочитайте акт."),
    (
        "contain",
        "содержать",
        "The book contains old photographs.",
        "Книга содержит старые фотографии.",
    ),
    ("learn", "учить", None, None),
    ("tool", "инструмент", "He took a tool from the box.", "Он взял инструмент из ящика."),
    (
        "committee",
        "комитет",
        "The committee accepted the offer.",
        "Комитет принял предложение.",
    ),
    (
        "figure",
        "фигура",
        "She saw her figure in the mirror.",
        "Она видела свою фигуру в зеркале.",
    ),
    ("from here", "отсюда", "You can see the sea from here.", "Отсюда видно море."),
    ("camp", "лагерь", None, None),
    ("track", "след", "I see a track on the snow.", "Я вижу след на снегу."),
    ("property", "собственность", None, None),
    (
        "section",
        "раздел",
        "Check this section of the book.",
        "Проверьте этот раздел книги.",
    ),
    (
        "reality",
        "реальность",
        "This is reality, not a dream.",
        "Это реальность, а не мечта.",
    ),
    ("loss", "потеря", "She felt a deep loss.", "Она чувствовала глубокую потерю."),
    ("winter", "зима", "Winter is my favorite time.", "Зима — моё любимое время."),
]


def main() -> None:
    src = ROOT / "_chunks" / "deck_15260251_00.csv"
    dst = ROOT / "_chunks" / "fixed" / "deck_15260251_00.csv"
    log = ROOT / "_chunks" / "logs" / "deck_15260251_00.txt"

    originals = cards_from_path(src)
    if len(originals) != 100:
        raise SystemExit(f"expected 100 input cards, got {len(originals)}")
    if len(FIXES) != 100:
        raise SystemExit(f"expected 100 fixes, got {len(FIXES)}")

    out: list[dict] = []
    for orig, (gloss, lemma, en_ex, ru_ex) in zip(originals, FIXES, strict=True):
        if orig["qMdBody"] != gloss:
            raise SystemExit(f"gloss mismatch: {orig['qMdBody']!r} != {gloss!r}")
        if orig["aMdBody"] != lemma:
            raise SystemExit(f"lemma mismatch for {gloss}: {orig['aMdBody']!r} != {lemma!r}")
        card = {
            "qMdPrompt": "Translate:",
            "qMdBody": gloss,
            "qMdClarifier": "",
            "qMdFootnote": en_ex if en_ex is not None else orig["qMdFootnote"],
            "aMdPrompt": "",
            "aMdBody": lemma,
            "aMdClarifier": "",
            "aMdFootnote": ru_ex if ru_ex is not None else orig["aMdFootnote"],
        }
        out.append(card_write_payload(card))

    write_csv(dst, out)
    written = cards_from_path(dst)
    if len(written) != 100:
        raise SystemExit(f"cards_from_path returned {len(written)}, expected 100")

    changed = 0
    for old, new in zip(originals, written, strict=True):
        if (
            old["qMdBody"] != new["qMdBody"]
            or old["aMdBody"] != new["aMdBody"]
            or old["qMdFootnote"] != new["qMdFootnote"]
            or old["aMdFootnote"] != new["aMdFootnote"]
        ):
            changed += 1

    log.write_text(f"{changed}\n", encoding="utf-8")
    print(f"wrote {dst}")
    print(f"cards_from_path={len(written)}")
    print(f"changed={changed}")


if __name__ == "__main__":
    main()
