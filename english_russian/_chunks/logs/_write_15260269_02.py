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

SRC = PACK / "_chunks" / "deck_15260269_02.csv"
OUT = PACK / "_chunks" / "fixed" / "deck_15260269_02.csv"
LOG = PACK / "_chunks" / "logs" / "deck_15260269_02.txt"

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
}

FUNCTION_RU = {
    "я", "мне", "меня", "мной", "мой", "моя", "мое", "моё", "мои", "мою",
    "мы", "нам", "нас", "нами", "наш", "наша", "наше", "наши", "нашу",
    "ты", "тебе", "тебя", "тобой", "твой", "твоя", "твое", "твоё", "твои",
    "вы", "вам", "вас", "вами", "ваш", "ваша", "ваше", "ваши", "вашу",
    "он", "она", "оно", "они", "его", "ее", "её", "ей", "ему", "им", "их",
    "ими", "ним", "ней", "ними", "него", "нее", "неё",
    "себя", "себе", "собой", "свой", "своя", "свое", "своё", "свои", "свою", "своим", "своего", "своей",
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
    for line in (PACK / "_vocab" / "allow_en_15260269.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_ru = {
    line.strip().replace("ё", "е").lower()
    for line in (PACK / "_vocab" / "allow_ru_15260269.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_en |= FUNCTION_EN
allow_ru |= FUNCTION_RU

# (en_lemma, en_ex, ru_lemma, ru_ex)
FIXED = [
    ("tray", "She carried drinks on a tray.", "поднос", "Она несла напитки на подносе."),
    ("boom", "The boom started this year.", "бум", "Бум начался в этом году."),
    ("to divorce", "They decided to divorce.", "развестись", "Они решили развестись."),
    ("to poke", "He will poke his finger.", "совать", "Он будет совать палец."),
    ("neighborhood", "I love our peaceful neighborhood.", "соседство", "Я люблю наше мирное соседство."),
    ("moisture", "Plants grow with moisture.", "влага", "Растения растут с влагой."),
    ("tiredly", "She tiredly closed her eyes.", "устало", "Она устало закрыла глаза."),
    ("inconvenience", "I caused an inconvenience.", "неудобство", "Я причинил неудобство."),
    ("determination", "Her determination led to success.", "решимость", "Её решимость привела к успеху."),
    ("collar", "He touched his shirt collar.", "воротник", "Он тронул воротник рубашки."),
    ("rapprochement", "The countries want a rapprochement.", "сближение", "Страны хотят сближения."),
    ("unemployed", "He has been unemployed for months.", "безработный", "Он безработный уже несколько месяцев."),
    ("to be described", "The scene is described in the book.", "описываться", "Сцена описывается в книге."),
    ("Trinity", "The Trinity is a Christian doctrine.", "троица", "Троица - это христианское учение."),
    ("rush", "They will rush to the door.", "ринуться", "Они ринутся к двери."),
    ("prediction", "His prediction came true yesterday.", "предсказание", "Его предсказание сбылось вчера."),
    ("to associate", "This smell is associated with home.", "ассоциироваться", "Этот запах ассоциируется с домом."),
    ("sparrow", "A sparrow sat on the window.", "воробей", "Воробей сидел на окне."),
    ("promptly", "He promptly answered the letter.", "оперативно", "Он оперативно ответил на письмо."),
    ("villa", "They rented a villa for summer.", "вилла", "Они сняли виллу на лето."),
    ("purple", "The sky turned a deep purple.", "фиолетовый", "Небо стало глубокого фиолетового цвета."),
    ("to cry out", "She will cry out in fear.", "вскрикнуть", "Она вскрикнет от страха."),
    ("kindergarten", "She teaches music in a kindergarten.", "садик", "Она преподает музыку в садике."),
    ("template", "Choose a template for your project.", "шаблон", "Выберите шаблон для вашего проекта."),
    ("to lean", "She had to lean against the wall.", "упереться", "Ей нужно упереться в стену."),
    ("bankruptcy", "The company declared bankruptcy yesterday.", "банкротство", "Компания объявила о банкротстве вчера."),
    ("operate", "Doctors will operate tomorrow morning.", "оперировать", "Врачи будут оперировать завтра утром."),
    ("suck", "Babies often suck milk.", "сосать", "Младенцы часто сосут молоко."),
    ("comparable", "The prices are comparable.", "сравнимый", "Цены сравнимы."),
    ("the Almighty", "Pray to the Almighty for help.", "всевышний", "Молись Всевышнему о помощи."),
    ("alliance", "They formed an alliance for peace.", "альянс", "Они создали альянс для мира."),
    ("outrage", "I cannot accept this outrage.", "безобразие", "Я не могу принять это безобразие."),
    ("intense", "His intense gaze was on me.", "пристальный", "Его пристальный взгляд был на мне."),
    ("illustrate", "The book will illustrate the idea.", "иллюстрировать", "Книга будет иллюстрировать идею."),
    ("to grow", "I want to grow tomatoes.", "вырастить", "Я хочу вырастить помидоры."),
    ("additive", "Sugar is an additive in food.", "добавка", "Сахар есть добавка в еде."),
    ("honorable", "He is an honorable man.", "почтенный", "Он почтенный человек."),
    ("vase", "The vase fell on the table.", "ваза", "Ваза упала на стол."),
    ("paradoxical", "His words were paradoxical but true.", "парадоксальный", "Его слова были парадоксальными, но верными."),
    ("Baptism", "Her son's baptism is today.", "крещение", "Крещение её сына сегодня."),
    ("greedy", "He was greedy for power.", "жадный", "Он был жадным до власти."),
    ("postwar", "The postwar economy was weak.", "послевоенный", "Послевоенная экономика была слабой."),
    ("faint", "She fell in a faint.", "обморок", "Она упала в обморок."),
    ("professionalism", "She admired his professionalism.", "профессионализм", "Она ценила его профессионализм."),
    ("malfunction", "The system had a sudden malfunction.", "сбой", "У системы был внезапный сбой."),
    ("to apply", "Remember to apply gentle pressure.", "прилагать", "Не забудьте прилагать слабое давление."),
    ("inadmissible", "This behavior is completely inadmissible.", "недопустимый", "Это поведение совсем недопустимо."),
    ("clarification", "I need clarification of the rule.", "выяснение", "Мне нужно выяснение правила."),
    ("banknote", "I found a banknote on the street.", "купюра", "Я нашел купюру на улице."),
    ("prescription", "The court issued a prescription.", "предписание", "Суд вынес предписание."),
    ("peninsula", "The city is on a peninsula.", "полуостров", "Город стоит на полуострове."),
    ("crocodile", "A crocodile swims in the river.", "крокодил", "Крокодил плавает в реке."),
    ("pepper", "I added pepper to the soup.", "перец", "Я добавил перец в суп."),
    ("intensify", "The rain will intensify at night.", "усилиться", "Дождь усилится ночью."),
    ("booth", "He sat in the booth.", "будка", "Он сидел в будке."),
    ("imitate", "The boy often imitates his father.", "подражать", "Мальчик часто подражает отцу."),
    ("simultaneous", "The two events were simultaneous.", "одновременный", "Два события были одновременными."),
    ("to be printed", "The book is printed every year.", "печататься", "Книга печатается каждый год."),
    ("repository", "This is a document repository.", "хранилище", "Это хранилище документов."),
    ("poor thing", "The poor thing looked so lost.", "бедняга", "Бедняга выглядел таким потерянным."),
    ("diligence", "Her diligence earned her the promotion.", "старание", "Её старание принесло ей повышение."),
    ("sociologist", "The sociologist published her findings today.", "социолог", "Социолог опубликовала свои результаты сегодня."),
    ("attractiveness", "Her attractiveness is clear.", "привлекательность", "Её привлекательность ясна."),
    ("proper", "We need proper papers.", "надлежащий", "Нам нужны надлежащие бумаги."),
    ("arbitrary", "The choice seemed completely arbitrary.", "произвольный", "Выбор казался совершенно произвольным."),
    ("handsome", "He is a handsome man.", "красивый", "Он красивый мужчина."),
    ("to sleep", "I need to sleep now.", "поспать", "Мне нужно сейчас поспать."),
    ("feeding", "Feeding the boy is important.", "кормление", "Кормление мальчика - важное дело."),
    ("injustice", "The world knows this injustice.", "несправедливость", "Мир знает эту несправедливость."),
    ("contrast", "The contrast between them is clear.", "контраст", "Контраст между ними ясен."),
    ("nuance", "I see every nuance.", "нюанс", "Я вижу каждый нюанс."),
    ("indifferently", "He looked at the news indifferently.", "равнодушно", "Он равнодушно смотрел на новости."),
    ("predator", "The wolf is a powerful predator.", "хищник", "Волк - мощный хищник."),
    ("ugly", "That building is really ugly.", "некрасивый", "Это здание действительно некрасивое."),
    ("cap", "She put on a cap outside.", "шапочка", "Она надела шапочку на улице."),
    ("insulin", "The doctor gave him insulin.", "инсулин", "Врач дал ему инсулин."),
    ("unclean", "The room felt unclean.", "нечистый", "Комната казалась нечистой."),
    ("liberalism", "Liberalism values individual freedom.", "либерализм", "Либерализм ценит индивидуальную свободу."),
    ("eyewitness", "The eyewitness saw the man.", "очевидец", "Очевидец видел этого человека."),
    ("fried", "I love fried chicken.", "жареный", "Я люблю жареную курицу."),
    ("cocktail", "She took a cocktail.", "коктейль", "Она взяла коктейль."),
    ("soar", "Birds soar high above the mountains.", "парить", "Птицы парят высоко над горами."),
    ("inventor", "The inventor made a new machine.", "изобретатель", "Изобретатель сделал новую машину."),
    ("specialize", "Doctors often specialize in specific fields.", "специализироваться", "Врачи часто специализируются в конкретных областях."),
    ("slippery", "The road is very slippery today.", "скользкий", "Сегодня дорога очень скользкая."),
    ("saliva", "There is saliva in the mouth.", "слюна", "В рту есть слюна."),
    ("coincide", "Our vacations will coincide this year.", "совпасть", "Наши отпуска совпадут в этом году."),
    ("pretty", "She looks pretty in that dress.", "хорошенький", "Она выглядит хорошенькой в этом платье."),
    ("varnish", "I will use varnish on the table.", "лак", "Я буду использовать лак на столе."),
    ("emigrant", "The emigrant left his country.", "эмигрант", "Эмигрант ушёл из своей страны."),
    ("partner", "My partner did the work.", "напарник", "Мой напарник сделал работу."),
    ("demographic", "This is a demographic change.", "демографический", "Это демографическое изменение."),
    ("to move back", "I need to move back the chair.", "отодвинуть", "Мне нужно отодвинуть стул."),
    ("pedestrian", "The pedestrian crossed the street.", "пешеход", "Пешеход перешёл улицу."),
    ("single", "This is a single error.", "единичный", "Это единичная ошибка."),
    ("strain", "Don't strain your eyes reading.", "напрягать", "Не напрягай глаза, читая."),
    ("not easy", "It's not easy to learn Russian.", "нелегко", "Учить русский нелегко."),
    ("convulsively", "He spoke convulsively.", "судорожно", "Он судорожно говорил."),
    ("to score", "He aimed to score today.", "забивать", "Он стремился забивать сегодня."),
    ("timid", "The boy was timid.", "робкий", "Мальчик был робким."),
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
    "told": "tell", "got": "get", "found": "find", "left": "leave",
    "kept": "keep", "felt": "feel", "thought": "think", "brought": "bring",
    "stood": "stand", "sat": "sit", "ran": "run", "won": "win",
    "lost": "lose", "met": "meet", "led": "lead", "paid": "pay",
    "spoke": "speak", "written": "write", "wrote": "write",
    "ate": "eat", "eaten": "eat", "drank": "drink", "drunk": "drink",
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
