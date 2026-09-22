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

SRC = PACK / "_chunks" / "deck_15260266_01.csv"
OUT = PACK / "_chunks" / "fixed" / "deck_15260266_01.csv"
LOG = PACK / "_chunks" / "logs" / "deck_15260266_01.txt"

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
        "собой", "мой", "моя", "моё", "мое", "мои", "мою", "моего", "моей",
        "твой", "твоя", "твоё", "твое", "твои",
        "свой", "своя", "своё", "свое", "свои", "наш", "наша", "наше",
        "наши", "ваш", "ваша", "ваше", "ваши", "этот", "эта", "это", "эти", "эту",
        "тот", "та", "то", "те", "такой", "такая", "такое", "такие", "весь",
        "вся", "всё", "все", "сам", "сама", "само", "сами", "быть", "есть",
        "был", "была", "было", "были", "буду", "будет", "будем", "будете",
        "будут", "нет", "не", "ни", "да", "уже", "ещё", "еще", "только", "даже",
        "тоже", "также", "очень", "так", "как", "что", "кто", "где", "когда",
        "почему", "куда", "который", "какой", "чтобы", "если", "потому", "ведь",
        "ли", "же", "бы", "вот", "здесь", "тут", "там", "теперь", "сейчас",
        "потом", "всегда", "никогда", "иногда", "от", "до", "по", "со", "из",
        "без", "при", "про", "об", "за", "над", "под", "перед", "после",
        "между", "через", "около", "для", "к", "у", "о", "в", "во", "на", "с",
        "и", "а", "но", "или", "может", "могут", "могу", "можем",
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
    "flew": "fly", "led": "lead", "caught": "catch", "rode": "ride",
    "swore": "swear", "lay": "lie",
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
    ("conspiracy", "They found a dangerous conspiracy.", "заговор", "Они нашли опасный заговор."),
    ("spacious", "The apartment is very spacious.", "просторный", "Квартира очень просторная."),
    ("in every way", "She supported him in every way.", "всячески", "Она всячески его поддерживала."),
    ("all-Russian", "The all-Russian competition starts tomorrow.", "всероссийский", "Всероссийский конкурс начинается завтра."),
    ("vanity", "There is vanity in the city.", "суета", "В городе есть суета."),
    ("Gospel", "She reads the Gospel every morning.", "евангелие", "Она читает Евангелие каждое утро."),
    ("noisy", "The street was very noisy.", "шумный", "Улица была очень шумной."),
    ("wait a bit", "Just wait a bit, please.", "погодить", "Пожалуйста, погодите немного."),
    ("statistical", "This is a statistical question.", "статистический", "Это статистический вопрос."),
    ("subjugate", "They aimed to subjugate the country.", "подчинить", "Они стремились подчинить страну."),
    ("squadron", "The squadron flew over the city.", "эскадрилья", "Эскадрилья пролетела над городом."),
    ("medic", "The medic is in the house.", "медик", "Медик в доме."),
    ("jealousy", "I know his jealousy.", "ревность", "Я знаю его ревность."),
    ("intend", "I intend to visit the city next year.", "намереваться", "Я намереваюсь посетить город в следующем году."),
    ("bowels", "They found gold in the earth's bowels.", "недра", "Они нашли золото в недрах земли."),
    ("fireplace", "The fireplace is in the room.", "камин", "Камин в комнате."),
    ("to present", "He failed to present ID.", "предъявлять", "Он не предъявил удостоверение."),
    ("confrontation", "I do not want a confrontation.", "противостояние", "Я не хочу противостояния."),
    ("counter", "She stood at the counter.", "прилавок", "Она стояла у прилавка."),
    ("to progress", "We need to progress quickly.", "продвигаться", "Нам нужно быстро продвигаться."),
    ("reptile", "He called him a reptile.", "гад", "Он назвал его гадом."),
    ("franc", "I have one franc.", "франк", "У меня есть один франк."),
    ("linear", "The line shows linear growth.", "линейный", "Линия показывает линейный рост."),
    ("leak", "The roof began to leak.", "протекать", "Крыша начала протекать."),
    ("motorcycle", "He rides his motorcycle every day.", "мотоцикл", "Он ездит на своём мотоцикле каждый день."),
    ("kindness", "I see her kindness.", "доброта", "Я вижу её доброту."),
    ("Stalinist", "I see Stalinist architecture.", "сталинский", "Я вижу сталинскую архитектуру."),
    ("accumulation", "The accumulation of snow was significant.", "накопление", "Накопление снега было значительным."),
    ("prestigious", "She studies at a prestigious university.", "престижный", "Она учится в престижном университете."),
    ("boredom", "I feel boredom.", "скука", "Я чувствую скуку."),
    ("tire", "I need a new tire.", "шина", "Мне нужна новая шина."),
    ("lieutenant colonel", "The lieutenant colonel is in the city.", "подполковник", "Подполковник в городе."),
    ("infinity", "I think about infinity.", "бесконечность", "Я думаю о бесконечности."),
    ("to be nervous", "She started to be nervous.", "нервничать", "Она начала нервничать."),
    ("wise man", "The wise man said this.", "мудрец", "Мудрец сказал это."),
    ("closing", "I know about the closing.", "закрытие", "Я знаю о закрытии."),
    ("Komsomol", "He joined the Komsomol.", "комсомол", "Он вступил в комсомол."),
    ("prolonged", "It was a prolonged meeting.", "продолжительный", "Это была продолжительная встреча."),
    ("drug addict", "The drug addict wants help.", "наркоман", "Наркоман хочет помощи."),
    ("mess", "Look at this mess.", "беспорядок", "Посмотри на этот беспорядок."),
    ("spy", "I caught a spy nearby.", "шпион", "Я поймал шпиона рядом."),
    ("log", "He sat on a log.", "бревно", "Он сидел на бревне."),
    ("tourism", "Tourism is important for the city.", "туризм", "Туризм важен для города."),
    ("rubber", "She wore rubber boots today.", "резиновый", "Она надела резиновые сапоги сегодня."),
    ("caress", "His caress was gentle.", "ласка", "Его ласка была нежной."),
    ("masterpiece", "This is a true masterpiece.", "шедевр", "Это настоящий шедевр."),
    ("explode", "The bomb will explode soon.", "взорваться", "Бомба скоро взорвётся."),
    ("braid", "She has a braid.", "коса", "У неё есть коса."),
    ("ID", "Show me your ID, please.", "удостоверение", "Покажите мне ваше удостоверение, пожалуйста."),
    ("holidays", "School holidays start next week.", "каникулы", "Школьные каникулы начинаются на следующей неделе."),
    ("innumerable", "Stars in the sky are innumerable.", "бесчисленный", "Звезды в небе бесчисленны."),
    ("in exchange", "I received a book in exchange.", "взамен", "Я получил книгу взамен."),
    ("eyelid", "Her eyelid is red.", "веко", "Её веко красное."),
    ("permissible", "Is this action permissible here?", "допустимый", "Это действие допустимо здесь?"),
    ("all kinds of", "She has all kinds of books.", "всяческий", "У неё всяческие книги."),
    ("rid", "I want to rid him of fear.", "избавить", "Я хочу избавить его от страха."),
    ("fly by", "The years fly by quickly.", "пролететь", "Годы быстро пролетают."),
    ("classic", "I love this classic.", "классика", "Я люблю эту классику."),
    ("remote control", "He lost the remote control again.", "пульт", "Он снова потерял пульт."),
    ("worldview", "I know his worldview.", "мировоззрение", "Я знаю его мировоззрение."),
    ("machine", "The machine works well.", "станок", "Станок хорошо работает."),
    ("hastily", "She hastily left the room.", "поспешно", "Она поспешно вышла из комнаты."),
    ("stumble upon", "I stumbled upon an old book.", "наткнуться", "Я наткнулся на старую книгу."),
    ("fascism", "He spoke about fascism.", "фашизм", "Он говорил о фашизме."),
    ("mistress", "He has a mistress.", "любовница", "У него есть любовница."),
    ("scarlet", "This is a scarlet color.", "алый", "Это алый цвет."),
    ("neutral", "He was neutral in the war.", "нейтральный", "Он был нейтральным в войне."),
    ("secondary", "This is a secondary question.", "вторичный", "Это вторичный вопрос."),
    ("meadow", "I walk in the meadow.", "луг", "Я хожу по лугу."),
    ("military personnel", "Military personnel received a letter today.", "военнослужащий", "Военнослужащие получили письмо сегодня."),
    ("to put in", "He tried to put in the key.", "засунуть", "Он пытался засунуть ключ."),
    ("theoretically", "Theoretically, this will work.", "теоретически", "Теоретически это будет работать."),
    ("bring in", "Please bring in the books.", "занести", "Пожалуйста, занесите книги."),
    ("sadness", "Her eyes reflected deep sadness.", "грусть", "В её глазах отражалась глубокая грусть."),
    ("unconscious", "He was completely unconscious.", "бессознательный", "Он был совершенно бессознательный."),
    ("insect", "An insect landed on my hand.", "насекомое", "На мою руку село насекомое."),
    ("partisan", "The partisan was in the forest.", "партизан", "Партизан был в лесу."),
    ("silent", "He was silent at the meeting.", "молчаливый", "Он был молчаливый на встрече."),
    ("broken", "The cup is now broken.", "разбитый", "Чашка теперь разбита."),
    ("convincing", "His argument was very convincing.", "убедительный", "Его аргумент был очень убедительным."),
    ("array", "The array is large.", "массив", "Массив большой."),
    ("drag", "I had to drag the heavy suitcase.", "таскать", "Мне пришлось таскать тяжёлый чемодан."),
    ("to step", "He paused to step into the room.", "шагнуть", "Он остановился, чтобы шагнуть в комнату."),
    ("radiation", "I feel the radiation.", "излучение", "Я чувствую излучение."),
    ("find oneself", "I found myself in the city.", "очутиться", "Я очутился в городе."),
    ("fraction", "He joined the party's fraction.", "фракция", "Он вступил во фракцию партии."),
    ("multicolored", "She wore a multicolored dress.", "разноцветный", "Она носила разноцветное платье."),
    ("thunderstorm", "The thunderstorm was strong.", "гроза", "Гроза была сильной."),
    ("solemnly", "He solemnly said these words.", "торжественно", "Он торжественно сказал эти слова."),
    ("to send", "They send me letters.", "присылать", "Они присылают мне письма."),
    ("fragile", "This glass is fragile.", "хрупкий", "Это стекло хрупкое."),
    ("to get drunk", "He decided to get drunk.", "напиться", "Он решил напиться."),
    ("unbearable", "The heat was simply unbearable.", "невыносимый", "Жара была просто невыносимой."),
    ("fairy-tale", "She had a fairy-tale wedding.", "сказочный", "У неё была сказочная свадьба."),
    ("to be remembered", "This day will be remembered.", "запомниться", "Этот день запомнится."),
    ("adaptation", "Adaptation is important.", "адаптация", "Адаптация важна."),
    ("echelon", "He joined a high echelon.", "эшелон", "Он вступил в высокий эшелон."),
    ("diplomatic", "He chose a diplomatic answer.", "дипломатический", "Он выбрал дипломатический ответ."),
    ("fountain", "The fountain is in the park.", "фонтан", "Фонтан в парке."),
    ("to connect", "I need to connect these wires.", "соединять", "Мне нужно соединить эти провода."),
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
    "хотеть": ("хоч",),
    "видеть": ("виж", "вид"),
    "выйти": ("выш", "выйд"),
    "ходить": ("хож", "ход"),
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
