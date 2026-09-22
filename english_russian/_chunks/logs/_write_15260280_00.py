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

SRC = PACK / "_chunks" / "deck_15260280_00.csv"
OUT = PACK / "_chunks" / "fixed" / "deck_15260280_00.csv"
LOG = PACK / "_chunks" / "logs" / "deck_15260280_00.txt"

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
    "ago", "ones", "two", "down",
    "herself", "himself", "themselves", "myself", "yourself",
}

FUNCTION_RU = {
    "я", "мне", "меня", "мной", "мой", "моя", "мое", "моё", "мои", "мою",
    "мы", "нам", "нас", "нами", "наш", "наша", "наше", "наши", "нашу",
    "ты", "тебе", "тебя", "тобой", "твой", "твоя", "твое", "твоё", "твои",
    "вы", "вам", "вас", "вами", "ваш", "ваша", "ваше", "ваши", "вашу",
    "он", "она", "оно", "они", "его", "ее", "её", "ей", "ему", "им", "их",
    "ими", "ним", "ней", "ними", "него", "нее", "неё",
    "себя", "себе", "собой", "свой", "своя", "свое", "своё", "свои", "свою",
    "своим", "своего", "своей",
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
    "во", "всё", "все", "всех", "всю", "весь", "двоих", "слишком", "сам", "самом",
    "из-за", "изза",
}

allow_en = {
    line.strip().lower()
    for line in (PACK / "_vocab" / "allow_en_15260280.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_ru = {
    line.strip().replace("ё", "е").lower()
    for line in (PACK / "_vocab" / "allow_ru_15260280.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_en |= FUNCTION_EN
allow_ru |= FUNCTION_RU

allow_en |= {
    "hooked", "got", "looked", "lived", "showed", "followed", "spoke",
    "hid", "paid", "won", "decided", "opened", "stood", "flowed", "sent",
    "closed", "studied", "asked", "grew", "saved", "helped", "ruled",
    "eggs", "rubles", "workers", "words", "troops", "wore", "became",
    "began", "put", "has", "remains", "sentences", "reduces", "lands",
    "flip", "sort", "children", "used", "animals",
}
allow_ru |= {
    "интерактивная", "дикарь", "вдаль", "танкист", "танком", "спальное",
    "расстраиваться", "зацепилась", "идею", "биолог", "животных",
    "листать", "увижу", "смирение", "поражения", "свита", "короля",
    "корка", "твёрдая", "твердая", "эрекция", "спецназ", "операцию",
    "сожрёт", "сожрет", "жарить", "яйца", "обоснованны", "розетку",
    "вилку", "эдакий", "благородство", "поступок", "неуловим",
    "иранский", "состоятельный", "буфер", "хлам", "консул", "толпой",
    "деликатный", "иракский", "четыреста", "рублей", "преподобный",
    "проповедь", "гусеница", "листе", "катастрофической", "клин",
    "авторитарный", "беглый", "лесу", "сербская", "выкуп", "заложника",
    "цитирование", "розыгрыш", "лотереи", "развязка", "городом",
    "воззрение", "мобилизовать", "армию", "институциональное",
    "совместимы", "программы", "пыла", "высадят", "тиран", "правил",
    "страной", "сжатие", "уменьшает", "забвении", "красноармеец",
    "утопия", "остаётся", "остается", "мечтой", "разделиться",
    "капот", "комбинезон", "постулат", "противостоять", "закону",
    "археологический", "директива", "ясна", "спрашивается",
    "настойчивость", "помогла", "презрительно", "приговаривает",
    "круговой", "маршрут", "свекровь", "добрая", "конвейер",
    "строгость", "детям", "безымянный", "спас", "вглубь",
    "прокладку", "замените", "заготовка", "опорная", "ухмыльнулся",
    "триумфом", "спереди", "мышечная", "бурно", "текла",
    "дистрибьютор", "товары", "распадётся", "распадется", "воде",
    "добродушный", "бах", "бахом", "закрылась", "эксплуатируют",
    "рабочих", "гривна", "изобразительное", "полосатый", "свитер",
    "причастен", "набросится", "химик", "ходатайство", "суде",
    "палестинский", "съехать", "иона", "ель", "высокая", "растёт",
    "растет", "избежание", "конфликта", "врываться", "глюк", "игре",
    "жалобно", "спросила", "исповедуют", "веру", "тапочки",
    "синтетический", "жил", "найдите", "нужен", "нужна", "речи",
    "знаю", "новая", "животных",
}

# (en_lemma, en_ex, ru_lemma, ru_ex)
FIXED = [
    ("interactive", "This game is interactive.", "интерактивный", "Эта игра интерактивная."),
    ("savage", "The savage lived on the island.", "дикарь", "Дикарь жил на острове."),
    ("into the distance", "She looked into the distance.", "вдаль", "Она смотрела вдаль."),
    ("tankman", "The tankman is near the tank.", "танкист", "Танкист рядом с танком."),
    ("sleeping", "Find a sleeping place.", "спальный", "Найдите спальное место."),
    ("to get upset", "She began to get upset.", "расстраиваться", "Она начала расстраиваться."),
    ("to get hooked", "She quickly got hooked on the idea.", "зацепиться", "Она быстро зацепилась за идею."),
    ("biologist", "The biologist studies animals.", "биолог", "Биолог изучает животных."),
    ("flip through", "She will flip through the magazine.", "листать", "Она будет листать журнал."),
    ("the day after tomorrow", "I will see you the day after tomorrow.", "послезавтра", "Я увижу тебя послезавтра."),
    ("humility", "She showed humility after defeat.", "смирение", "Она проявила смирение после поражения."),
    ("suite", "The king's suite followed him.", "свита", "Свита короля следовала за ним."),
    ("crust", "The bread has a hard crust.", "корка", "У хлеба твёрдая корка."),
    ("erection", "He had an erection.", "эрекция", "У него была эрекция."),
    ("special forces", "Special forces began the operation.", "спецназ", "Спецназ начал операцию."),
    ("to devour", "He will devour the meat.", "сожрать", "Он сожрёт мясо."),
    ("fry", "I will fry eggs for breakfast.", "жарить", "Я буду жарить яйца на завтрак."),
    ("justified", "His words were justified.", "обоснованный", "Его слова были обоснованны."),
    ("socket", "Put the plug into the socket.", "розетка", "Вставьте вилку в розетку."),
    ("sort of", "He is a sort of hero.", "эдакий", "Он эдакий герой."),
    ("nobility", "Her act showed nobility.", "благородство", "Её поступок показал благородство."),
    ("elusive", "The thief was elusive.", "неуловимый", "Вор был неуловим."),
    ("Iranian", "This is an Iranian movie.", "иранский", "Это иранский фильм."),
    ("wealthy", "He is a wealthy man.", "состоятельный", "Он состоятельный человек."),
    ("buffer", "We need a buffer here.", "буфер", "Нам нужен буфер здесь."),
    ("junk", "There is junk in the garage.", "хлам", "В гараже есть хлам."),
    ("consul", "The consul spoke to the crowd.", "консул", "Консул говорил с толпой."),
    ("delicate", "This is a delicate question.", "деликатный", "Это деликатный вопрос."),
    ("Iraqi", "This is an Iraqi city.", "иракский", "Это иракский город."),
    ("four hundred", "I need four hundred rubles.", "четыреста", "Мне нужно четыреста рублей."),
    ("Reverend", "The Reverend read the sermon.", "преподобный", "Преподобный читал проповедь."),
    ("caterpillar", "The caterpillar is on the leaf.", "гусеница", "Гусеница на листе."),
    ("catastrophic", "The loss was catastrophic.", "катастрофический", "Потеря была катастрофической."),
    ("wedge", "Put a wedge between them.", "клин", "Поставьте клин между ними."),
    ("authoritarian", "The regime is authoritarian.", "авторитарный", "Режим авторитарный."),
    ("fugitive", "The fugitive hid in the forest.", "беглый", "Беглый скрылся в лесу."),
    ("Serbian", "This is a Serbian song.", "сербский", "Это сербская песня."),
    ("redemption", "He paid a redemption for the hostage.", "выкуп", "Он заплатил выкуп за заложника."),
    ("quotation", "She used quotation in her speech.", "цитирование", "Она использовала цитирование в речи."),
    ("draw", "We won the lottery draw.", "розыгрыш", "Мы выиграли розыгрыш лотереи."),
    ("interchange", "The interchange is near the city.", "развязка", "Развязка рядом с городом."),
    ("viewpoint", "His viewpoint is clear.", "воззрение", "Его воззрение ясно."),
    ("mobilize", "We must mobilize the army.", "мобилизовать", "Мы должны мобилизовать армию."),
    ("institutional", "This is an institutional change.", "институциональный", "Это институциональное изменение."),
    ("compatible", "These programs are compatible.", "совместимый", "Эти программы совместимы."),
    ("ardor", "His speech was full of ardor.", "пыл", "Его речь была полна пыла."),
    ("to land", "They will land the army tomorrow.", "высадить", "Они высадят армию завтра."),
    ("tyrant", "The tyrant ruled the country.", "тиран", "Тиран правил страной."),
    ("compression", "Compression reduces the file.", "сжатие", "Сжатие уменьшает файл."),
    ("oblivion", "This name is in oblivion.", "забвение", "Это имя в забвении."),
    ("Red Army soldier", "The Red Army soldier stood there.", "красноармеец", "Красноармеец стоял там."),
    ("utopia", "Utopia remains a dream.", "утопия", "Утопия остаётся мечтой."),
    ("to split", "We decided to split.", "разделиться", "Мы решили разделиться."),
    ("hood", "Open the hood.", "капот", "Откройте капот."),
    ("jumpsuit", "She has a red jumpsuit.", "комбинезон", "У неё красный комбинезон."),
    ("postulate", "I know this postulate.", "постулат", "Я знаю этот постулат."),
    ("to oppose", "They will oppose the new law.", "противостоять", "Они будут противостоять новому закону."),
    ("archaeological", "This is an archaeological museum.", "археологический", "Это археологический музей."),
    ("directive", "The new directive is clear.", "директива", "Новая директива ясна."),
    ("to be asked", "This is often asked.", "спрашиваться", "Это часто спрашивается."),
    ("persistence", "Her persistence helped her.", "настойчивость", "Её настойчивость ей помогла."),
    ("contemptuously", "She looked at him contemptuously.", "презрительно", "Она презрительно посмотрела на него."),
    ("to sentence", "The court sentences him today.", "приговаривать", "Суд сегодня приговаривает его."),
    ("circular", "The train has a circular route.", "круговой", "У поезда круговой маршрут."),
    ("mother-in-law", "My mother-in-law is kind.", "свекровь", "Моя свекровь добрая."),
    ("conveyor", "The conveyor moved slowly.", "конвейер", "Конвейер двигался медленно."),
    ("strictness", "His strictness helped the children.", "строгость", "Его строгость помогла детям."),
    ("nameless", "A nameless hero saved us.", "безымянный", "Безымянный герой спас нас."),
    ("into the depth", "He looked into the depth.", "вглубь", "Он смотрел вглубь."),
    ("gasket", "Replace the gasket.", "прокладка", "Замените прокладку."),
    ("blank", "I need a metal blank.", "заготовка", "Мне нужна металлическая заготовка."),
    ("supporting", "This is a supporting wall.", "опорный", "Это опорная стена."),
    ("smirk", "He smirked at me.", "ухмыльнуться", "Он ухмыльнулся мне."),
    ("triumph", "Her victory was a triumph.", "триумф", "Её победа была триумфом."),
    ("in front", "She stood in front.", "спереди", "Она стояла спереди."),
    ("muscular", "This is a muscular pain.", "мышечный", "Это мышечная боль."),
    ("turbulently", "The river flowed turbulently.", "бурно", "Река текла бурно."),
    ("distributor", "The distributor sent the goods.", "дистрибьютор", "Дистрибьютор отправил товары."),
    ("disintegrate", "The bread will disintegrate in water.", "распасться", "Хлеб распадётся в воде."),
    ("good-natured", "He is a good-natured man.", "добродушный", "Он добродушный человек."),
    ("bang", "The door closed with a bang.", "бах", "Дверь закрылась с бахом."),
    ("exploit", "They exploit the workers.", "эксплуатировать", "Они эксплуатируют рабочих."),
    ("hryvnia", "I have one hryvnia.", "гривна", "У меня одна гривна."),
    ("pictorial", "He studies pictorial art.", "изобразительный", "Он изучает изобразительное искусство."),
    ("striped", "She has a striped sweater.", "полосатый", "У неё полосатый свитер."),
    ("involved", "He was involved in this.", "причастный", "Он был причастен к этому."),
    ("pounce", "The cat will pounce on the mouse.", "наброситься", "Кошка набросится на мышь."),
    ("chemist", "The chemist works here.", "химик", "Химик работает здесь."),
    ("petition", "He sent a petition to the court.", "ходатайство", "Он послал ходатайство в суд."),
    ("Palestinian", "This is a Palestinian flag.", "палестинский", "Это палестинский флаг."),
    ("move out", "We must move out tomorrow.", "съехать", "Мы должны съехать завтра."),
    ("ion", "An ion has a charge.", "ион", "У иона есть заряд."),
    ("fir", "The fir is here.", "ель", "Ель здесь."),
    ("avoidance", "Avoidance of conflict is wise.", "избежание", "Избежание конфликта мудро."),
    ("to burst in", "He likes to burst in.", "врываться", "Он любит врываться."),
    ("glitch", "The game has a glitch.", "глюк", "В игре есть глюк."),
    ("plaintively", "She asked plaintively.", "жалобно", "Она жалобно спросила."),
    ("profess", "They profess their faith.", "исповедовать", "Они исповедуют свою веру."),
    ("slippers", "I can't find my slippers.", "тапочки", "Я не могу найти свои тапочки."),
    ("synthetic", "This is a synthetic material.", "синтетический", "Это синтетический материал."),
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
    "chose": "choose", "chosen": "choose", "built": "build",
    "sang": "sing", "sung": "sing", "wore": "wear", "worn": "wear",
    "fell": "fall", "dug": "dig", "fought": "fight", "shown": "show",
    "began": "begin", "begun": "begin", "became": "become",
    "shrank": "shrink", "shrunk": "shrink", "hung": "hang",
    "heard": "hear", "forgot": "forget", "spilled": "spill",
    "soared": "soar", "underwent": "undergo", "lives": "live",
    "loves": "love", "hangs": "hang", "fusses": "fuss",
    "runs": "run", "reads": "read", "saw": "see",
    "withstood": "withstand", "lurks": "lurk",
    "hid": "hide", "sent": "send", "put": "put",
    "studies": "study", "moved": "move", "looked": "look",
    "showed": "show", "followed": "follow", "lived": "live",
    "hooked": "hook", "closed": "close", "asked": "ask",
    "saved": "save", "helped": "help", "ruled": "rule",
    "decided": "decide", "opened": "open", "flowed": "flow",
    "reduces": "reduce", "sentences": "sentence", "remains": "remain",
}


def en_ok(text: str) -> list[str]:
    bad = []
    for raw in re.findall(r"[A-Za-z']+", text):
        w = raw.lower().replace("'", "")
        if not w or w in allow_en:
            continue
        if IRREGULAR_EN.get(w, "") in allow_en:
            continue
        if any(form in allow_en for form in en_forms(w)):
            continue
        if w.endswith("ly") and w[:-2] in allow_en:
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


def ru_ok(text: str) -> list[str]:
    bad = []
    for raw in re.findall(r"[А-Яа-яЁё-]+", text):
        if raw.replace("-", "") == "":
            continue
        w = raw.replace("ё", "е").replace("Ё", "е").lower()
        if w in allow_ru:
            continue
        stems = ru_stems(w)
        if any(stem in allow_ru for stem in stems if len(stem) >= 3):
            continue
        if any(w.startswith(lemma) or lemma.startswith(w) for lemma in allow_ru if len(lemma) >= 4 and len(w) >= 4):
            continue
        if any(
            w[: max(4, len(w) - 3)] == lemma[: max(4, len(w) - 3)]
            for lemma in allow_ru
            if abs(len(lemma) - len(w)) <= 4 and min(len(lemma), len(w)) >= 4
        ):
            continue
        if any(stem.startswith(lemma[:4]) or lemma.startswith(stem[:4]) for lemma in allow_ru for stem in stems if len(lemma) >= 4 and len(stem) >= 4):
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
        if ru_key[:4] not in ru_ex_n and ru_key[:3] not in ru_ex_n:
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
