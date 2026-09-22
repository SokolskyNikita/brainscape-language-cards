#!/usr/bin/env python3
from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PACK = ROOT / "english_russian"
sys.path.insert(0, str(ROOT))

from brainscape.cards import card_write_payload, cards_from_path, cards_match

SRC = PACK / "_chunks" / "deck_15260281_02.csv"
OUT = PACK / "_chunks" / "fixed" / "deck_15260281_02.csv"
LOG = PACK / "_chunks" / "logs" / "deck_15260281_02.txt"

FUNCTION_EN = {
    "a", "an", "the", "is", "be", "i", "you", "he", "she", "it", "we", "they",
    "my", "and", "or", "in", "on", "at", "to", "of", "for", "with", "from",
    "not", "his", "him", "her", "their", "them", "our", "us", "me", "am",
    "are", "was", "were", "been", "being", "this", "that", "these", "those",
    "as", "by", "into", "about", "than", "then", "so", "if", "but", "its",
    "your", "do", "does", "did", "will", "would", "can", "could", "may",
    "there", "here", "has", "had", "have", "don't", "dont", "let's", "lets",
    "all", "off", "done", "must", "such", "one", "only", "please", "often",
    "well", "early", "today", "near", "large", "high", "old", "long", "hard",
}

FUNCTION_RU = {
    "и", "а", "или", "не", "ни", "но", "да", "же", "ли", "бы", "то", "это",
    "этот", "эта", "эти", "этой", "этом", "эту", "этих", "этим", "этими",
    "этого", "этому", "я", "ты", "он", "она", "оно", "мы", "вы", "они",
    "мой", "моя", "мое", "мои", "моего", "моей", "моем", "моим", "мою",
    "твой", "твоя", "твое", "твои", "твою", "твоей", "ваш", "наш", "наша",
    "наше", "наши", "его", "ее", "их", "ему", "ей", "им", "ими", "меня",
    "мне", "тебя", "тебе", "нас", "нам", "вас", "вам", "себя", "себе",
    "собой", "свой", "своя", "свое", "свои", "свою", "своей", "своего",
    "своим", "в", "во", "на", "с", "со", "к", "ко", "у", "о", "об", "от",
    "до", "из", "за", "по", "под", "над", "при", "для", "без", "между",
    "через", "был", "была", "было", "были", "будет", "будут", "буду",
    "есть", "быть", "уже", "еще", "также", "тоже", "только", "вот", "ведь",
    "ну", "все", "всех", "всего", "всем", "здесь", "тут", "там", "давай",
    "как", "что", "чтобы", "когда", "если", "где", "чем", "кто",
    "них", "него", "нее", "ней", "ним", "около", "друг", "друга",
}

allow_en = {
    line.strip().lower()
    for line in (PACK / "_vocab" / "allow_en_15260281.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_ru = {
    line.strip().replace("ё", "е").lower()
    for line in (PACK / "_vocab" / "allow_ru_15260281.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_en |= FUNCTION_EN
allow_ru |= FUNCTION_RU

# New lemmas introduced by corrections (taught on this card).
allow_ru |= {"заигрывать", "ослышаться", "клерк"}

# (en_lemma, en_ex, ru_lemma, ru_ex)
FIXED = [
    ("sobbing", "I hear her sobbing.", "рыдание", "Я слышу её рыдание."),
    ("iconic", "This movie is iconic.", "знаковый", "Этот фильм знаковый."),
    ("cordially", "She cordially invited us.", "приветливо", "Она приветливо пригласила нас."),
    ("value-based", "This is value-based education.", "ценностный", "Это ценностное образование."),
    ("beating", "This was a cruel beating.", "избиение", "Это было жестокое избиение."),
    ("diaspora", "The Russian diaspora is large.", "диаспора", "Русская диаспора большая."),
    ("frying pan", "I have a frying pan.", "сковородка", "У меня есть сковородка."),
    ("to be regulated", "Prices must be regulated.", "регулироваться", "Цены должны регулироваться."),
    ("to be measured", "The distance is to be measured.", "измеряться", "Расстояние должно измеряться."),
    ("to crunch", "I like to crunch apples.", "хрустеть", "Я люблю хрустеть яблоками."),
    ("gloriously", "She danced gloriously.", "славно", "Она славно танцевала."),
    ("unkind", "His words were unkind.", "недобрый", "Его слова были недобрыми."),
    ("compatibility", "Check the compatibility of these things.", "совместимость", "Проверьте совместимость этих вещей."),
    ("strand", "She has one strand.", "прядь", "У неё одна прядь."),
    ("to flirt", "She likes to flirt.", "заигрывать", "Она любит заигрывать."),
    ("cleaner", "The cleaner came early.", "уборщица", "Уборщица пришла рано."),
    ("wasteland", "There is a wasteland near the house.", "пустырь", "Около дома есть пустырь."),
    ("morgue", "The body is in the morgue.", "морг", "Тело в морге."),
    ("ore", "This is iron ore.", "руда", "Это железная руда."),
    ("Afghan", "This is an Afghan city.", "афганский", "Это афганский город."),
    ("pike", "There is a pike here.", "щука", "Здесь есть щука."),
    ("look back", "He did not look back.", "оглянуться", "Он не оглянулся."),
    ("absently", "She looked at me absently.", "рассеянно", "Она рассеянно посмотрела на меня."),
    ("conscientiously", "She works conscientiously.", "добросовестно", "Она работает добросовестно."),
    ("overlay", "This overlay is on the map.", "наложение", "Это наложение на карте."),
    ("projector", "We need a projector.", "проектор", "Нам нужен проектор."),
    ("mockingly", "He smiled mockingly.", "насмешливо", "Он насмешливо улыбнулся."),
    ("retention", "The retention of water is high.", "удержание", "Удержание воды высокое."),
    ("think up", "She will think up a plan.", "додуматься", "Она додумается до плана."),
    ("imperialism", "He wrote about imperialism.", "империализм", "Он писал об империализме."),
    ("inaction", "I was surprised by his inaction.", "бездействие", "Я удивился его бездействию."),
    ("rejection", "I felt her rejection.", "неприятие", "Я чувствовал её неприятие."),
    ("pood", "He lifted one pood.", "пуд", "Он поднял один пуд."),
    ("thinkable", "Is such a war thinkable?", "мыслимый", "Мыслима ли такая война?"),
    ("condescendingly", "He spoke to us condescendingly.", "снисходительно", "Он говорил с нами снисходительно."),
    ("licensing", "This licensing takes time.", "лицензирование", "Это лицензирование занимает время."),
    ("stun", "This news will stun you.", "ошеломить", "Эта новость вас ошеломит."),
    ("to chase", "The dog likes to chase the cat.", "гнаться", "Собака любит гнаться за кошкой."),
    ("muffle", "Please muffle the sound.", "приглушить", "Пожалуйста, приглушите звук."),
    ("humane", "This is a humane law.", "гуманный", "Это гуманный закон."),
    ("rhetorical", "Was that a rhetorical question?", "риторический", "Это был риторический вопрос?"),
    ("drill", "This is drill training.", "строевой", "Это строевая подготовка."),
    ("relativity", "I read about relativity.", "относительность", "Я читал об относительности."),
    ("fang", "The dog has a sharp fang.", "клык", "У собаки острый клык."),
    ("dispatcher", "The dispatcher answered me.", "диспетчер", "Диспетчер мне ответил."),
    ("gain experience", "I want to gain experience.", "набираться", "Я хочу набираться опыта."),
    ("to chop off", "He will chop off the branch.", "отрубить", "Он отрубит ветку."),
    ("non-governmental", "This is a non-governmental group.", "неправительственный", "Это неправительственная группа."),
    ("to torture", "They will torture him.", "замучить", "Они его замучат."),
    ("heal", "The wound will heal.", "зажить", "Рана заживёт."),
    ("fasting", "I do not like fasting.", "голодание", "Мне не нравится голодание."),
    ("narrate", "She will narrate the story.", "повествовать", "Она будет повествовать об этой истории."),
    ("to brush off", "She likes to brush off the dust.", "смахивать", "Она любит смахивать пыль."),
    ("guitarist", "The guitarist played well.", "гитарист", "Гитарист хорошо играл."),
    ("apple tree", "The apple tree is old.", "яблоня", "Яблоня старая."),
    ("non-traditional", "She likes non-traditional music.", "нетрадиционный", "Ей нравится нетрадиционная музыка."),
    ("devilish", "He has a devilish smile.", "дьявольский", "У него дьявольская улыбка."),
    ("ascending", "This is an ascending line.", "восходящий", "Это восходящая линия."),
    ("pendulum", "I see the pendulum.", "маятник", "Я вижу маятник."),
    ("naivety", "I was surprised by her naivety.", "наивность", "Я удивился её наивности."),
    ("constipation", "He has constipation.", "запор", "У него запор."),
    ("awkwardness", "I felt the awkwardness.", "неловкость", "Я почувствовал неловкость."),
    ("interrogatively", "She looked at him interrogatively.", "вопросительно", "Она посмотрела на него вопросительно."),
    ("to overlap", "These hours overlap.", "перекрывать", "Эти часы перекрывают друг друга."),
    ("martyr", "He died a martyr.", "мученик", "Он умер мучеником."),
    ("garment", "She wore a new garment.", "одеяние", "На ней было новое одеяние."),
    ("abroad", "News from abroad came today.", "зарубежье", "Новости из зарубежья пришли сегодня."),
    ("housewife", "The housewife prepared dinner.", "домохозяйка", "Домохозяйка приготовила ужин."),
    ("cheekbone", "She has a high cheekbone.", "скула", "У неё высокая скула."),
    ("memorial", "This memorial is old.", "мемориал", "Этот мемориал старый."),
    ("sketch", "He draws a sketch of the house.", "эскиз", "Он рисует эскиз дома."),
    ("invader", "The invader entered the city.", "захватчик", "Захватчик вошёл в город."),
    ("aggressiveness", "I was surprised by his aggressiveness.", "агрессивность", "Я удивился его агрессивности."),
    ("perimeter", "Look at the perimeter of the garden.", "периметр", "Смотри на периметр сада."),
    ("seriously", "Are you speaking seriously?", "серьёзно", "Вы говорите серьёзно?"),
    ("district committee", "The district committee works today.", "райком", "Райком работает сегодня."),
    ("drag oneself", "I had to drag myself to work.", "тащиться", "Мне пришлось тащиться на работу."),
    ("vulgar", "His words are vulgar.", "пошлый", "Его слова пошлые."),
    ("to sin", "I do not want to sin.", "грешить", "Я не хочу грешить."),
    ("hockey", "I watch hockey.", "хоккей", "Я смотрю хоккей."),
    ("to show through", "Blood will show through.", "проступать", "Кровь будет проступать."),
    ("outgrow", "The boy will outgrow this coat.", "перерасти", "Мальчик перерастёт это пальто."),
    ("demonstratively", "She demonstratively left.", "демонстративно", "Она демонстративно ушла."),
    ("lime", "The old lime is in the park.", "липа", "Старая липа в парке."),
    ("heresy", "This is heresy.", "ересь", "Это ересь."),
    ("Buddhist", "He visited a Buddhist temple.", "буддийский", "Он посетил буддийский храм."),
    ("splendor", "I saw the splendor of the palace.", "великолепие", "Я видел великолепие дворца."),
    ("mishear", "I often mishear words.", "ослышаться", "Я часто ослышаюсь."),
    ("speculation", "This is only speculation.", "спекуляция", "Это только спекуляция."),
    ("shroud", "They keep the shroud in the church.", "плащаница", "Плащаницу хранят в церкви."),
    ("clerk", "The clerk gave me the papers.", "клерк", "Клерк дал мне бумаги."),
    ("entertaining", "This book is entertaining.", "занимательный", "Эта книга занимательная."),
    ("agriculture", "He works in agriculture.", "земледелие", "Он работает в земледелии."),
    ("Hermitage", "We were at the Hermitage.", "эрмитаж", "Мы были в Эрмитаже."),
    ("broker", "He works as a broker.", "брокер", "Он работает брокером."),
    ("trim", "Please trim the tree.", "обрезать", "Пожалуйста, обрежьте дерево."),
    ("convene", "They want to convene the group.", "созвать", "Они хотят созвать группу."),
    ("dossier", "I read his dossier.", "досье", "Я читал его досье."),
    ("to fly to", "We will fly to the city.", "долететь", "Мы долетим до города."),
    ("waltz", "They danced a waltz.", "вальс", "Они танцевали вальс."),
]


IRREGULAR_EN = {
    "made": "make",
    "met": "meet",
    "saw": "see",
    "got": "get",
    "gave": "give",
    "took": "take",
    "came": "come",
    "went": "go",
    "ate": "eat",
    "spoke": "speak",
    "broke": "break",
    "heard": "hear",
    "caught": "catch",
    "felt": "feel",
    "wrote": "write",
    "left": "leave",
    "drew": "draw",
    "died": "die",
    "kept": "keep",
    "wore": "wear",
}


def _en_ok(word: str) -> bool:
    w = word.lower()
    if w in allow_en:
        return True
    if IRREGULAR_EN.get(w) in allow_en:
        return True
    if "-" in w and all(_en_ok(p) for p in w.split("-") if p):
        return True
    for suf in ("'s", "s", "es", "ed", "ing", "ly", "er", "est"):
        if w.endswith(suf) and w[: -len(suf)] in allow_en:
            return True
        if w.endswith(suf) and w[: -len(suf)] + "e" in allow_en:
            return True
    if w.endswith("ies") and (w[:-3] + "y") in allow_en:
        return True
    if w.endswith("ied") and (w[:-3] + "y") in allow_en:
        return True
    return False


RU_ENDINGS = (
    "ами", "ями", "ого", "его", "ому", "ему", "ыми", "ими", "ой", "ей", "ом",
    "ем", "ах", "ях", "ам", "ям", "ов", "ев", "ей", "ую", "юю", "ая", "яя",
    "ое", "ее", "ые", "ие", "ый", "ий", "ой", "а", "я", "у", "ю", "е", "и",
    "ы", "о", "ь",
)


def _ru_stems(word: str) -> set[str]:
    w = word.replace("ё", "е").lower()
    out = {w}
    for n in range(3, min(6, len(w) + 1)):
        out.add(w[:n])
    for suf in RU_ENDINGS:
        if w.endswith(suf) and len(w) - len(suf) >= 3:
            out.add(w[: -len(suf)])
    return out


IRREGULAR_RU = {
    "может": "мочь",
    "могу": "мочь",
    "можем": "мочь",
    "хочу": "хотеть",
    "хочет": "хотеть",
    "хотим": "хотеть",
    "вижу": "видеть",
    "видишь": "видеть",
    "видит": "видеть",
    "видел": "видеть",
    "знаю": "знать",
    "живу": "жить",
    "живем": "жить",
    "живет": "жить",
    "пришла": "прийти",
    "пришли": "прийти",
    "пришлось": "прийтись",
    "вошел": "войти",
    "дал": "дать",
    "умер": "умереть",
    "ушла": "уйти",
    "смотрю": "смотреть",
}


def _ru_ok(word: str) -> bool:
    w = word.replace("ё", "е").lower()
    if w in allow_ru:
        return True
    mapped = IRREGULAR_RU.get(w)
    if mapped and mapped in allow_ru:
        return True
    stems = _ru_stems(w)
    for lemma in allow_ru:
        if len(lemma) < 3:
            continue
        if stems & _ru_stems(lemma):
            return True
        stem = lemma[:4] if len(lemma) >= 4 else lemma
        if w.startswith(stem) or lemma.startswith(w[:4] if len(w) >= 4 else w):
            return True
    return False


def make_card(en_lemma: str, en_ex: str, ru_lemma: str, ru_ex: str) -> dict:
    return card_write_payload(
        {
            "qMdPrompt": "Translate:",
            "qMdBody": en_lemma,
            "qMdClarifier": "",
            "qMdFootnote": en_ex,
            "aMdPrompt": "",
            "aMdBody": ru_lemma,
            "aMdClarifier": "",
            "aMdFootnote": ru_ex,
        }
    )


def target_in_example(lemma: str, example: str) -> bool:
    text = example.replace("ё", "е").lower()
    parts = [p.strip() for p in re.split(r"\s+", lemma.replace("ё", "е").lower()) if p.strip()]
    keys = [p for p in parts if p not in {"to", "be", "the", "a", "an"}] or parts
    for key in keys:
        stem = key[:4] if len(key) >= 4 else key
        if stem and stem in text.replace(" ", ""):
            return True
        if key in text:
            return True
    return False


def write_csv(path: Path, cards: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh, lineterminator="\n")
        writer.writerow(["Question", "Answer"])
        for card in cards:
            payload = card_write_payload(card)
            writer.writerow([payload["question"], payload["answer"]])


def main() -> None:
    orig = cards_from_path(SRC)
    if len(orig) != 100:
        raise SystemExit(f"expected 100 source cards, got {len(orig)}")
    if len(FIXED) != 100:
        raise SystemExit(f"expected 100 fixed rows, got {len(FIXED)}")

    cards = []
    changed = 0
    leftover: list[str] = []
    missing_target: list[str] = []
    for i, ((en_lemma, en_ex, ru_lemma, ru_ex), old) in enumerate(zip(FIXED, orig), start=1):
        if old.get("qMdBody") != en_lemma:
            raise SystemExit(f"order mismatch at {i}: {old.get('qMdBody')!r} vs {en_lemma!r}")
        card = make_card(en_lemma, en_ex, ru_lemma, ru_ex)
        cards.append(card)
        if not cards_match(old, card):
            changed += 1
        lemma_bits = set(re.findall(r"[A-Za-z']+", en_lemma.lower()))
        for tok in re.findall(r"[A-Za-z']+", en_ex):
            if tok.lower() in lemma_bits:
                continue
            if not _en_ok(tok):
                leftover.append(f"{i} EN {tok} :: {en_ex}")
        ru_bits = set(re.findall(r"[А-Яа-яЁё]+", ru_lemma.lower().replace("ё", "е")))
        for tok in re.findall(r"[А-Яа-яЁё]+", ru_ex):
            if tok.replace("ё", "е").lower() in ru_bits:
                continue
            if not _ru_ok(tok):
                leftover.append(f"{i} RU {tok} :: {ru_ex}")
        if not target_in_example(en_lemma, en_ex):
            missing_target.append(f"{i} EN {en_lemma} :: {en_ex}")
        if not target_in_example(ru_lemma, ru_ex):
            missing_target.append(f"{i} RU {ru_lemma} :: {ru_ex}")

    write_csv(OUT, cards)
    got = cards_from_path(OUT)
    if len(got) != 100:
        raise SystemExit(f"cards_from_path returned {len(got)}")
    LOG.parent.mkdir(parents=True, exist_ok=True)
    LOG.write_text(f"{changed}\n", encoding="utf-8")
    print(f"wrote {OUT}")
    print(f"cards_from_path={len(got)} changed={changed}")
    if leftover:
        print("LEFTOVER:")
        print("\n".join(leftover))
    if missing_target:
        print("MISSING TARGET:")
        print("\n".join(missing_target))


if __name__ == "__main__":
    main()
