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

SRC = PACK / "_chunks" / "deck_15260266_02.csv"
OUT = PACK / "_chunks" / "fixed" / "deck_15260266_02.csv"
LOG = PACK / "_chunks" / "logs" / "deck_15260266_02.txt"

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
        "а", "но", "или", "во", "из-за", "больше",
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
    "led": "lead", "slept": "sleep", "dug": "dig",
}

allow_en = {
    line.strip().lower()
    for line in (PACK / "_vocab" / "allow_en_15260266.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
} | FUNCTION_EN
allow_ru = {
    line.strip().replace("ё", "е").lower()
    for line in (PACK / "_vocab" / "allow_ru_15260266.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
} | FUNCTION_RU

# (en_lemma, en_ex, ru_lemma, ru_ex)
FIXED = [
    ("passionate", "She is a passionate person.", "страстный", "Она страстный человек."),
    ("to turn on", "The light will turn on soon.", "включаться", "Свет скоро включится."),
    ("founder", "The founder launched the company in 1998.", "основатель", "Основатель запустил компанию в 1998 году."),
    ("laureate", "The laureate received a prize.", "лауреат", "Лауреат получил премию."),
    ("competitive", "The market is very competitive.", "конкурентный", "Рынок очень конкурентный."),
    ("burst in", "He burst in without a word.", "ворваться", "Он ворвался без слова."),
    ("detection", "Early detection saves lives.", "выявление", "Раннее выявление спасает жизни."),
    ("work out", "We will work out the details.", "проработать", "Мы проработаем детали."),
    ("brake", "The brake will stop the car.", "тормоз", "Тормоз остановит машину."),
    ("patriarch", "The patriarch spoke to the people.", "патриарх", "Патриарх говорил с народом."),
    ("monitoring", "Monitoring of the situation is important.", "мониторинг", "Мониторинг ситуации важен."),
    ("encyclopedia", "I read it in an encyclopedia.", "энциклопедия", "Я прочитал это в энциклопедии."),
    ("khan", "The khan lived in this city.", "хан", "Хан жил в этом городе."),
    ("wake", "Do not wake him.", "будить", "Не буди его."),
    ("rostrum", "He spoke from the rostrum.", "трибуна", "Он говорил с трибуны."),
    ("to be resolved", "The issue will be resolved soon.", "разрешаться", "Проблема скоро разрешится."),
    ("to be cited", "This source is often cited.", "приводиться", "Этот источник часто приводится."),
    ("to be visible", "The mountain is visible from here.", "виднеться", "Гора виднеется отсюда."),
    ("entrepreneurship", "Entrepreneurship is important for the country.", "предпринимательство", "Предпринимательство важно для страны."),
    ("get stuck", "I get stuck in the door.", "застрять", "Я застреваю в двери."),
    ("charitable", "She runs a charitable organization.", "благотворительный", "Она управляет благотворительной организацией."),
    ("printer", "The printer does not work.", "принтер", "Принтер не работает."),
    ("distrust", "She felt deep distrust towards him.", "недоверие", "Она испытывала глубокое недоверие к нему."),
    ("compete", "Companies compete in the market.", "конкурировать", "Компании конкурируют на рынке."),
    ("acid", "This acid is strong.", "кислота", "Эта кислота сильная."),
    ("to take care of", "She promised to take care of him.", "ухаживать", "Она пообещала ухаживать за ним."),
    ("pigeon", "A pigeon sat on the windowsill.", "голубь", "Голубь сидел на подоконнике."),
    ("to extract", "They learned to extract gold.", "добывать", "Они научились добывать золото."),
    ("morally", "This is morally important.", "морально", "Это морально важно."),
    ("embarrass", "His question began to embarrass her.", "смущать", "Его вопрос начал смущать её."),
    ("ice cream", "I love ice cream.", "мороженое", "Я люблю мороженое."),
    ("squirrel", "The squirrel climbed the tree.", "белка", "Белка забралась на дерево."),
    ("legendary", "His skills were legendary.", "легендарный", "Его навыки были легендарными."),
    ("tobacco", "He does not smoke tobacco.", "табак", "Он не курит табак."),
    ("to reason", "I cannot reason now.", "соображать", "Я не соображаю сейчас."),
    ("hire", "I need to hire a manager.", "нанять", "Мне нужно нанять менеджера."),
    ("prevail", "This opinion will prevail.", "преобладать", "Это мнение будет преобладать."),
    ("designation", "Each place has a clear designation.", "обозначение", "Каждое место имеет ясное обозначение."),
    ("modeling", "Modeling of this system is important.", "моделирование", "Моделирование этой системы важно."),
    ("testament", "This book is his testament.", "завет", "Эта книга — его завет."),
    ("to intensify", "The wind began to intensify.", "усиливаться", "Ветер начал усиливаться."),
    ("prevent", "Masks can prevent disease spread.", "предотвратить", "Маски могут предотвратить распространение болезней."),
    ("welcome", "Welcome to our home!", "добро пожаловать", "Добро пожаловать в наш дом!"),
    ("awkward", "The silence was awkward.", "неловкий", "Тишина была неловкой."),
    ("mathematician", "The mathematician solved the complex equation.", "математик", "Математик решил сложное уравнение."),
    ("enlightenment", "Enlightenment is important for the people.", "просвещение", "Просвещение важно для народа."),
    ("over", "This is over the plan.", "сверх", "Это сверх плана."),
    ("wrap", "Please wrap the gift.", "завернуть", "Пожалуйста, заверните подарок."),
    ("ant", "An ant sat on the table.", "муравей", "Муравей сидел на столе."),
    ("shovel", "I need a shovel.", "лопата", "Мне нужна лопата."),
    ("to drop by", "I want to drop by tomorrow.", "заехать", "Я хочу заехать завтра."),
    ("to be characterized", "This region is characterized by its climate.", "характеризоваться", "Этот регион характеризуется своим климатом."),
    ("provincial", "This is a provincial town.", "провинциальный", "Это провинциальный город."),
    ("prosperous", "The country became prosperous and stable.", "благополучный", "Страна стала благополучной и стабильной."),
    ("overwhelm", "Work can overwhelm him.", "завалить", "Работа завалит его."),
    ("goddess", "She is a Greek goddess.", "богиня", "Она греческая богиня."),
    ("stroller", "She pushed the stroller through the park.", "коляска", "Она толкала коляску через парк."),
    ("quantitative", "We need quantitative analysis.", "количественный", "Нам нужен количественный анализ."),
    ("physiognomy", "Her physiognomy revealed her true feelings.", "физиономия", "Её физиономия выдала её истинные чувства."),
    ("stake", "Put the stake in the earth.", "кол", "Поставьте кол в землю."),
    ("progressive", "She supports progressive educational reforms.", "прогрессивный", "Она поддерживает прогрессивные образовательные реформы."),
    ("bundle", "She carried a bundle of keys.", "связка", "Она несла связку ключей."),
    ("to fall into", "He began to fall into despair.", "впадать", "Он начал впадать в отчаяние."),
    ("mute", "He is mute.", "немой", "Он немой."),
    ("polite", "He was always polite to guests.", "вежливый", "Он всегда был вежлив с гостями."),
    ("to be provided", "Help is provided to all.", "предоставляться", "Помощь предоставляется всем."),
    ("indignation", "She felt indignation.", "возмущение", "Она почувствовала возмущение."),
    ("to climb out", "He managed to climb out.", "вылезать", "Он смог вылезти."),
    ("tomorrow's", "Tomorrow's weather is good.", "завтрашний", "Завтрашняя погода хорошая."),
    ("gentleman", "He is a true gentleman.", "джентльмен", "Он настоящий джентльмен."),
    ("download", "I'll download the file today.", "скачать", "Я скачаю файл сегодня."),
    ("to attract", "The sea attracts me.", "влечь", "Море влечёт меня."),
    ("cook", "The cook prepares soup.", "повар", "Повар готовит суп."),
    ("oral", "The exam includes an oral section.", "устный", "Экзамен включает устный раздел."),
    ("escape", "He planned his escape at night.", "бегство", "Он планировал своё бегство ночью."),
    ("to survey", "We need to survey them.", "опросить", "Нам нужно опросить их."),
    ("cucumber", "I bought a cucumber.", "огурец", "Я купил огурец."),
    ("to bring to", "Do not bring him to tears.", "доводить", "Не доводи его до слёз."),
    ("foam", "There is foam on the water.", "пена", "На воде есть пена."),
    ("rib", "He broke a rib.", "ребро", "Он сломал ребро."),
    ("fame", "He wants fame.", "известность", "Он хочет известности."),
    ("ash", "His ash is in the sea.", "прах", "Его прах в море."),
    ("windowsill", "The cat sat on the windowsill.", "подоконник", "Кошка сидела на подоконнике."),
    ("to run through", "He decided to run through the park.", "пробежать", "Он решил пробежать через парк."),
    ("TV channel", "I found a new TV channel.", "телеканал", "Я нашёл новый телеканал."),
    ("thorough", "He conducted a thorough investigation.", "тщательный", "Он провел тщательное расследование."),
    ("little brother", "My little brother is at home.", "братец", "Мой братец дома."),
    ("additionally", "Additionally, we need more time.", "дополнительно", "Дополнительно нам нужно время."),
    ("to knock", "I need to knock on the door.", "постучать", "Мне нужно постучать в дверь."),
    ("hurriedly", "She hurriedly packed her suitcase.", "торопливо", "Она торопливо собрала свой чемодан."),
    ("screw", "I need a screw.", "винт", "Мне нужен винт."),
    ("fig", "This is a fig.", "фига", "Это фига."),
    ("Vika", "Vika is my sister.", "Вика", "Вика — моя сестра."),
    ("Orthodoxy", "He embraced Orthodoxy.", "православие", "Он принял православие."),
    ("matrimonial", "They offer matrimonial services.", "брачный", "Они предлагают брачные услуги."),
    ("to be allowed", "This is not allowed here.", "допускаться", "Это здесь не допускается."),
    ("luggage", "I packed my luggage.", "багаж", "Я собрал свой багаж."),
    ("thickness", "Measure the thickness of the wall.", "толщина", "Измерьте толщину стены."),
    ("thrice", "He called her name thrice.", "трижды", "Он трижды позвал её по имени."),
    ("clamp", "I want to clamp the paper.", "зажать", "Я хочу зажать бумагу."),
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
    "хотеть": ("хоч", "хот"),
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
