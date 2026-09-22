#!/usr/bin/env python3
from __future__ import annotations

import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from brainscape.cards import (  # noqa: E402
    card_from_faces,
    card_write_payload,
    cards_from_path,
    cards_match,
)

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "deck_15260251_01.csv"
OUT = ROOT / "fixed" / "deck_15260251_01.csv"
LOG = ROOT / "logs" / "deck_15260251_01.txt"

# (en_lemma, ru_lemma, en_example, ru_example)
FIXED: list[tuple[str, str, str, str]] = [
    ("screen", "экран", "Watch the movie on this screen.", "Смотрите фильм на этом экране."),
    ("cute", "милый", "That dog is so cute!", "Эта собака такая милая!"),
    ("to perish", "погибнуть", "They feared to perish at sea.", "Они боялись погибнуть в море."),
    ("traditional", "традиционный", "This is a traditional song.", "Это традиционная песня."),
    ("to be healthy", "здравствовать", "I want to be healthy.", "Я хочу здравствовать."),
    ("transition", "переход", "Life is a transition.", "Жизнь - это переход."),
    ("bed", "кровать", "I sleep in this bed.", "Я сплю в этой кровати."),
    ("dedicate", "посвятить", "I dedicated this song to you.", "Я посвятил эту песню тебе."),
    ("lesson", "урок", "This is a valuable lesson.", "Это ценный урок."),
    ("sex", "секс", "Sex is a natural human desire.", "Секс - это естественное человеческое желание."),
    ("motherland", "родина", "I love my motherland.", "Я люблю свою родину."),
    ("wine", "вино", "She drinks red wine.", "Она пьёт красное вино."),
    ("zone", "зона", "This is a safety zone.", "Это зона безопасности."),
    ("knee", "колено", "I feel pain in my knee.", "Я чувствую боль в колене."),
    ("to sound", "звучать", "The song began to sound loudly.", "Песня начала громко звучать."),
    ("colleague", "коллега", "I talked with my colleague today.", "Я сегодня говорил с коллегой."),
    ("poor", "бедный", "He was a poor man.", "Он был бедным человеком."),
    ("appearance", "появление", "They saw his appearance.", "Они видели его появление."),
    ("edition", "издание", "I bought the last edition.", "Я купил последнее издание."),
    ("sharply", "резко", "He turned around sharply.", "Он резко повернулся."),
    ("to talk", "поговорить", "I want to talk with her.", "Я хочу поговорить с ней."),
    ("Jew", "еврей", "My friend is a Jew.", "Мой друг - еврей."),
    ("budget", "бюджет", "We have no budget this month.", "У нас нет бюджета в этом месяце."),
    ("rarely", "редко", "She rarely goes home.", "Она редко идёт домой."),
    ("prince", "князь", "The prince was young.", "Князь был молодым."),
    ("floor", "этаж", "We live on the third floor.", "Мы живем на третьем этаже."),
    ("honor", "честь", "He received this with honor.", "Он получил это с честью."),
    ("to be required", "требоваться", "This will be required tomorrow.", "Это будет требоваться завтра."),
    ("remarkable", "замечательный", "This is a remarkable book.", "Это замечательная книга."),
    ("cry", "плакать", "The baby often cries.", "Малыш часто плачет."),
    ("need", "потребность", "People have a need for water.", "У людей есть потребность в воде."),
    ("invent", "придумать", "She will invent a new game.", "Она придумает новую игру."),
    ("debt", "долг", "He has a big debt.", "У него большой долг."),
    ("temple", "храм", "The temple stood on the mountain.", "Храм стоял на горе."),
    ("come in", "заходить", "Please, come in and sit down.", "Пожалуйста, заходите и сядьте."),
    ("danger", "опасность", "There is danger ahead.", "Впереди есть опасность."),
    ("deputy", "депутат", "The deputy offered a new law.", "Депутат предложил новый закон."),
    ("enroll", "поступить", "I will enroll in university soon.", "Я скоро поступлю в университет."),
    ("to choose", "выбирать", "I have to choose now.", "Мне нужно выбирать сейчас."),
    ("achieve", "достигнуть", "She wanted to achieve her dreams.", "Она хотела достигнуть своих мечт."),
    ("save", "сохранить", "Please save the document now.", "Пожалуйста, сохраните документ сейчас."),
    ("depth", "глубина", "The depth of the sea is great.", "Глубина моря велика."),
    ("category", "категория", "Choose the right category.", "Выберите правильную категорию."),
    ("hot", "горячий", "The tea is very hot.", "Чай очень горячий."),
    ("arrange", "устроить", "We will arrange a meeting.", "Мы устроим встречу."),
    ("administration", "администрация", "The administration has a plan.", "У администрации есть план."),
    ("organize", "организовать", "We will organize a meeting.", "Мы организуем встречу."),
    ("effect", "эффект", "This had a good effect.", "Это имело хороший эффект."),
    ("to fly", "лететь", "Birds love to fly in winter.", "Птицы любят лететь зимой."),
    ("trade", "торговля", "International trade is important.", "Международная торговля важна."),
    ("description", "описание", "The book's description was short.", "Описание книги было коротким."),
    ("risk", "риск", "This is a big risk.", "Это большой риск."),
    ("accommodate", "расположить", "We can accommodate five guests.", "Мы можем расположить пять гостей."),
    ("horse", "лошадь", "The horse is in the field.", "Лошадь на поле."),
    ("corridor", "коридор", "The corridor was empty.", "Коридор был пустым."),
    ("girlfriend", "подруга", "She is my girlfriend.", "Она моя подруга."),
    ("commit", "совершить", "He will commit a crime.", "Он совершит преступление."),
    ("capital", "капитал", "This capital is important.", "Этот капитал важен."),
    ("exception", "исключение", "She was the exception to the rule.", "Она была исключением из правил."),
    ("competition", "конкурс", "She was in the competition.", "Она была на конкурсе."),
    ("scheme", "схема", "This is a smart scheme.", "Это умная схема."),
    ("nocturnal", "ночной", "Cats are nocturnal animals.", "Кошки - ночные животные."),
    ("spring", "весна", "Spring brought beautiful flowers.", "Весна принесла красивые цветы."),
    ("check", "проверить", "Please check this document.", "Пожалуйста, проверьте этот документ."),
    ("beauty", "красота", "I see her beauty.", "Я вижу её красоту."),
    ("thirty", "тридцать", "She turned thirty.", "Ей исполнилось тридцать."),
    ("fish", "рыба", "This is a big fish.", "Это большая рыба."),
    ("get", "достать", "I'll get the book from the table.", "Я достану книгу со стола."),
    ("deeply", "глубоко", "She felt this deeply.", "Она глубоко это чувствовала."),
    ("publish", "опубликовать", "They will publish the article tomorrow.", "Они опубликуют статью завтра."),
    ("accurate", "точный", "His answer was accurate.", "Его ответ был точным."),
    ("pipe", "трубка", "This is his pipe.", "Это его трубка."),
    ("to be said", "говориться", "Much is said about this.", "Об этом много говорится."),
    ("eastern", "восточный", "The eastern wind is cold.", "Восточный ветер холодный."),
    ("key", "ключ", "I lost my key yesterday.", "Я потерял свой ключ вчера."),
    ("surname", "фамилия", "What's your surname?", "Какая у вас фамилия?"),
    ("to include", "включать", "The list will include this.", "Список будет включать это."),
    ("discovery", "открытие", "This discovery is important.", "Это открытие важно."),
    ("turn on", "включить", "Please turn on the light.", "Пожалуйста, включите свет."),
    ("miracle", "чудо", "This was a true miracle.", "Это было настоящим чудом."),
    ("regiment", "полк", "The regiment went through the city.", "Полк прошёл через город."),
    ("armchair", "кресло", "He read quietly in his armchair.", "Он тихо читал в своём кресле."),
    ("opposite", "напротив", "He sat opposite me.", "Он сидел напротив меня."),
    ("appeal", "обращение", "Their appeal reached many people.", "Их обращение дошло до многих людей."),
    ("describe", "описать", "Please describe your experience.", "Пожалуйста, опишите ваш опыт."),
    ("quiet", "тихий", "The forest was quiet.", "Лес был тихим."),
    ("whose", "чей", "Whose book is this?", "Чья это книга?"),
    ("eight", "восемь", "She bought eight books yesterday.", "Она купила восемь книг вчера."),
    ("gray", "серый", "The sky is gray today.", "Сегодня небо серое."),
    ("to be present", "присутствовать", "He needed to be present at the meeting.", "Ему нужно было присутствовать на встрече."),
    ("to learn", "научиться", "I want to learn Russian.", "Я хочу научиться русскому языку."),
    ("ministry", "министерство", "She works in this ministry.", "Она работает в этом министерстве."),
    ("unexpectedly", "неожиданно", "She unexpectedly came home.", "Она неожиданно пришла домой."),
    ("cinema", "кино", "We watched a movie at the cinema.", "Мы смотрели фильм в кино."),
    ("medical", "медицинский", "She wants medical help.", "Она хочет медицинскую помощь."),
    ("tax", "налог", "We pay this tax.", "Мы платим этот налог."),
    ("iron", "железный", "This is an iron door.", "Это железная дверь."),
    ("glad", "рад", "I'm glad you came today.", "Я рад, что ты пришел сегодня."),
    ("reduction", "снижение", "There was a reduction in errors.", "Произошло снижение ошибок."),
    ("cultural", "культурный", "This is a cultural event.", "Это культурное событие."),
]


def faces(en_lemma: str, ru_lemma: str, en_ex: str, ru_ex: str) -> tuple[str, str]:
    q = f"# Translate:\n\n{en_lemma}\n\n## Footnote\n\n{en_ex}"
    a = f"{ru_lemma}\n\n## Footnote\n\n{ru_ex}"
    return q, a


def main() -> None:
    original = cards_from_path(SRC)
    if len(original) != 100:
        raise SystemExit(f"expected 100 source cards, got {len(original)}")
    if len(FIXED) != 100:
        raise SystemExit(f"expected 100 fixed rows, got {len(FIXED)}")

    out_cards = []
    rows = []
    for i, (en, ru, en_ex, ru_ex) in enumerate(FIXED):
        if original[i]["qMdBody"] != en:
            raise SystemExit(f"order mismatch at {i+1}: {original[i]['qMdBody']!r} vs {en!r}")
        payload = card_write_payload(card_from_faces(*faces(en, ru, en_ex, ru_ex)))
        out_cards.append(payload)
        rows.append({"Question": payload["question"], "Answer": payload["answer"]})

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=["Question", "Answer"], lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    written = cards_from_path(OUT)
    if len(written) != 100:
        raise SystemExit(f"cards_from_path returned {len(written)}")

    changed = sum(1 for a, b in zip(original, written) if not cards_match(a, b))
    LOG.write_text(f"{changed}\n", encoding="utf-8")
    print(f"wrote {OUT}")
    print(f"cards_from_path={len(written)}")
    print(f"changed={changed}")


if __name__ == "__main__":
    main()
