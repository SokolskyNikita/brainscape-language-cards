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

SRC = PACK / "_chunks" / "deck_15260257_04.csv"
OUT = PACK / "_chunks" / "fixed" / "deck_15260257_04.csv"
LOG = PACK / "_chunks" / "logs" / "deck_15260257_04.txt"

FUNCTION = {
    "a", "the", "is", "be", "i", "you", "he", "she", "it", "we", "they",
    "my", "and", "or", "in", "on", "at", "to", "of", "for", "with", "from",
    "not", "his", "him", "her", "their", "them", "our", "us", "me", "am",
    "are", "was", "were", "been", "being", "this", "that", "these", "those",
    "an", "as", "by", "into", "about", "than", "then", "so", "if", "but",
    "its", "your", "did", "does", "do", "can", "will", "would", "could",
    "should", "may", "might", "must", "have", "has", "had", "here", "there",
    "now", "soon", "today", "yesterday", "tomorrow", "yes", "no", "too",
    "very", "also", "only", "just", "even", "still", "already", "always",
    "never", "often", "every", "each", "some", "any", "all", "both", "more",
    "most", "much", "many", "how", "what", "when", "where", "who", "why",
    "which", "up", "down", "out", "off", "over", "under", "after", "before",
    "because", "while", "until", "through", "between", "among", "one", "two",
    "three", "first", "last", "new", "old",
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
    ("variety", "This is a new variety of apple.", "сорт", "Это новый сорт яблока."),
    ("bloody", "The battle was bloody.", "кровавый", "Битва была кровавой."),
    ("to offend", "He did not want to offend her.", "обидеть", "Он не хотел обидеть её."),
    ("fascist", "He called him a fascist.", "фашист", "Он назвал его фашистом."),
    ("tournament", "This is a big tournament.", "турнир", "Это большой турнир."),
    ("bathroom", "I cleaned the bathroom today.", "ванная", "Я мыл ванную сегодня."),
    ("contradict", "His actions often contradict his words.", "противоречить", "Его действия часто противоречат его словам."),
    ("to be perceived", "Beauty is perceived as good.", "восприниматься", "Красота воспринимается как хорошая."),
    ("avenue", "This avenue is big.", "проспект", "Этот проспект большой."),
    ("disassemble", "We need to disassemble the engine.", "разобрать", "Нам нужно разобрать двигатель."),
    ("dark", "It is dark outside.", "темно", "На улице темно."),
    ("rack", "Put the books on the rack.", "стойка", "Поставьте книги на стойку."),
    ("to be offered", "The work is offered today.", "предлагаться", "Работа предлагается сегодня."),
    ("truck", "The truck delivered the goods.", "грузовик", "Грузовик доставил товары."),
    ("noon", "Lunch is at noon.", "полдень", "Обед в полдень."),
    ("to stare", "She stared at him.", "уставиться", "Она уставилась на него."),
    ("shooting", "I heard the shooting.", "стрельба", "Я слышал стрельбу."),
    ("swamp", "There is a swamp near the river.", "болото", "Рядом с рекой есть болото."),
    ("accident", "There was an accident on the highway.", "авария", "На шоссе была авария."),
    ("intellect", "Her intellect is strong.", "интеллект", "Её интеллект сильный."),
    ("to be heard", "A voice was heard.", "послышаться", "Послышался голос."),
    ("to diverge", "Our paths began to diverge.", "расходиться", "Наши пути начали расходиться."),
    ("instinct", "Mother's instinct is powerful.", "инстинкт", "Инстинкт матери мощный."),
    ("to be discussed", "The topic will be discussed tomorrow.", "обсуждаться", "Тема будет обсуждаться завтра."),
    ("race", "This is one race.", "раса", "Это одна раса."),
    ("coast", "We walked along the coast.", "побережье", "Мы гуляли вдоль побережья."),
    ("respond", "He did not respond to my call.", "отозваться", "Он не отозвался на мой звонок."),
    ("lid", "The box needs a lid.", "крышка", "Ящику нужна крышка."),
    ("stomach", "I feel pain in my stomach after dinner.", "желудок", "Я чувствую боль в желудке после ужина."),
    ("bucket", "Fill the bucket with water.", "ведро", "Наполните ведро водой."),
    ("tactic", "This is a smart tactic.", "тактика", "Это умная тактика."),
    ("zero", "The temperature is zero.", "нуль", "Температура — нуль."),
    ("lightning", "Lightning struck the tree.", "молния", "Молния ударила в дерево."),
    ("Chechen", "He speaks Chechen.", "чеченский", "Он говорит на чеченском."),
    ("shop", "I visited the local shop yesterday.", "лавка", "Я посетил местную лавку вчера."),
    ("thesis", "Her thesis is new.", "тезис", "Её тезис новый."),
    ("make out", "I can make out the sign from here.", "разглядеть", "Я могу разглядеть знак отсюда."),
    ("to contribute", "I want to contribute ideas.", "вносить", "Я хочу вносить идеи."),
    ("raincoat", "She forgot her raincoat at home.", "плащ", "Она забыла свой плащ дома."),
    ("to look back", "She paused to look back.", "оглянуться", "Она остановилась, чтобы оглянуться."),
    ("accessory", "This is a car accessory.", "принадлежность", "Это принадлежность машины."),
    ("collapse", "The building will collapse soon.", "рухнуть", "Здание скоро рухнет."),
    ("importance", "Understand the importance of this.", "важность", "Поймите важность этого."),
    ("judgment", "Your judgment is good.", "суждение", "Ваше суждение хорошее."),
    ("to fall ill", "She fell ill yesterday.", "заболеть", "Она заболела вчера."),
    ("compensation", "He received fair compensation for his work.", "компенсация", "Он получил справедливую компенсацию за свою работу."),
    ("relief", "She sighed in relief.", "облегчение", "Она вздохнула с облегчением."),
    ("to lie around", "Books lie around my house.", "валяться", "Книги валяются у меня дома."),
    ("supplier", "We found a new supplier.", "поставщик", "Мы нашли нового поставщика."),
    ("Christianity", "Christianity is a religion.", "христианство", "Христианство — религия."),
    ("dissatisfied", "He is dissatisfied with the results.", "недовольный", "Он недоволен результатами."),
    ("Cossack", "The Cossack has a horse.", "казак", "У казака есть лошадь."),
    ("observer", "The observer noted every detail carefully.", "наблюдатель", "Наблюдатель внимательно отметил каждую деталь."),
    ("manuscript", "She found an old manuscript.", "рукопись", "Она нашла старую рукопись."),
    ("menu", "Check the menu.", "меню", "Проверьте меню."),
    ("brave", "She was brave.", "смелый", "Она была смелой."),
    ("pill", "Take this pill with water.", "таблетка", "Примите эту таблетку с водой."),
    ("principally", "He works principally at home.", "главным образом", "Он работает главным образом дома."),
    ("medal", "He has a gold medal today.", "медаль", "У него сегодня золотая медаль."),
    ("linguistic", "She studies linguistic texts.", "языковой", "Она учит языковые тексты."),
    ("anxiety", "Anxiety filled her before the exam.", "беспокойство", "Беспокойство охватило её перед экзаменом."),
    ("pedagogical", "This is a pedagogical text.", "педагогический", "Это педагогический текст."),
    ("sailor", "The sailor is on the sea.", "моряк", "Моряк на море."),
    ("justify", "He could not justify his actions.", "оправдать", "Он не смог оправдать свои действия."),
    ("gray-haired", "The gray-haired man smiled.", "седой", "Седой мужчина улыбнулся."),
    ("poetic", "This is a poetic text.", "поэтический", "Это поэтический текст."),
    ("equally", "They treat us equally.", "одинаково", "Они обращаются с нами одинаково."),
    ("to be planned", "The meeting is planned for tomorrow.", "планироваться", "Встреча планируется на завтра."),
    ("desirably", "Desirably, come tomorrow.", "желательно", "Желательно прийти завтра."),
    ("lend", "These words lend meaning to the text.", "придать", "Эти слова придают смысл тексту."),
    ("visibility", "Visibility was almost zero.", "видимость", "Видимость была почти нуль."),
    ("accent", "Her accent is strong.", "акцент", "Её акцент сильный."),
    ("fall silent", "He will fall silent soon.", "замолчать", "Он скоро замолчит."),
    ("governmental", "Governmental policy is important.", "правительственный", "Правительственная политика важна."),
    ("solemn", "This was a solemn day.", "торжественный", "Это был торжественный день."),
    ("to precede", "Night precedes morning.", "предшествовать", "Ночь предшествует утру."),
    ("devil", "The devil is bad.", "дьявол", "Дьявол плохой."),
    ("coat", "She wore a warm coat outside.", "пальто", "Она надела теплое пальто на улицу."),
    ("optimal", "This is the optimal result.", "оптимальный", "Это оптимальный результат."),
    ("insert", "Please insert your card.", "вставить", "Пожалуйста, вставьте карту."),
    ("robe", "She wore a robe at home.", "халат", "Она носила халат дома."),
    ("Arabic", "She studies Arabic.", "арабский", "Она учит арабский."),
    ("from below", "The sound came from below.", "снизу", "Звук шёл снизу."),
    ("rat", "The rat ran in the house.", "крыса", "Крыса бежала в доме."),
    ("divorce", "They got a divorce yesterday.", "развод", "Они получили развод вчера."),
    ("precious", "Time with family is precious.", "драгоценный", "Время с семьёй драгоценно."),
    ("fluctuation", "Price fluctuation is strong.", "колебание", "Колебание цены сильное."),
    ("safe", "The route is safe.", "безопасный", "Маршрут безопасный."),
    ("fly", "A fly sat on the table.", "муха", "Муха села на стол."),
    ("capitalism", "Capitalism is an economic system.", "капитализм", "Капитализм — экономическая система."),
    ("mighty", "The mighty river is near.", "могучий", "Могучая река рядом."),
    ("icy", "The road was icy and cold.", "ледяной", "Дорога была ледяной и холодной."),
    ("heat", "The summer heat was strong.", "жара", "Летняя жара была сильной."),
    ("to laugh", "She laughed.", "рассмеяться", "Она рассмеялась."),
    ("warning", "He did not see the warning.", "предупреждение", "Он не видел предупреждения."),
    ("nowadays", "Nowadays he lives well.", "нынче", "Нынче он живёт хорошо."),
    ("bicycle", "I ride my bicycle every morning.", "велосипед", "Я езжу на велосипеде каждое утро."),
    ("fantastic", "The view was simply fantastic.", "фантастический", "Вид был просто фантастический."),
    ("recipe", "I found a new recipe.", "рецепт", "Я нашёл новый рецепт."),
    ("sleigh", "I see a sleigh in the snow.", "сани", "Я вижу сани в снегу."),
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
        if any(
            w[: max(4, len(w) - 3)] == lemma[: max(4, len(w) - 3)]
            for lemma in allow_ru
            if abs(len(lemma) - len(w)) <= 4 and min(len(lemma), len(w)) >= 4
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
