#!/usr/bin/env python3
"""Rewrite english_russian deck_15260277_03 (cards 301-400, band 6000->6500)."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PACK = ROOT / "english_russian"
sys.path.insert(0, str(ROOT))

from brainscape.cards import card_write_payload, cards_from_path, cards_match
from english_russian._chunk_io import write_csv

SRC = PACK / "_chunks" / "deck_15260277_03.csv"
OUT = PACK / "_chunks" / "fixed" / "deck_15260277_03.csv"
LOG = PACK / "_chunks" / "logs" / "deck_15260277_03.txt"

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
    for line in (PACK / "_vocab" / "allow_en_15260277.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_ru = {
    line.strip().replace("ё", "е").lower()
    for line in (PACK / "_vocab" / "allow_ru_15260277.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_en |= FUNCTION_EN
allow_ru |= FUNCTION_RU

# (en_lemma, en_ex, ru_lemma, ru_ex)
FIXED = [
    ("synagogue", "We visited the synagogue on Saturday.", "синагога", "Мы посетили синагогу в субботу."),
    ("to bark", "Dogs tend to bark at strangers.", "лаять", "Собаки склонны лаять на незнакомцев."),
    ("unacceptable", "This behavior is completely unacceptable.", "неприемлемый", "Это поведение абсолютно неприемлемо."),
    ("bombing", "The city endured bombing.", "бомбардировка", "Город выдержал бомбардировку."),
    ("aluminum", "They use aluminum.", "алюминий", "Они используют алюминий."),
    ("identify", "Police could not identify the suspect.", "идентифицировать", "Полиция не смогла идентифицировать подозреваемого."),
    ("let in", "They decided to let in the cat.", "впустить", "Они решили впустить кошку."),
    ("patronymic", "What is his patronymic?", "отчество", "Какое у него отчество?"),
    ("debates", "The candidates prepared for the debates.", "дебаты", "Кандидаты готовились к дебатам."),
    ("to gift", "He decided to gift her flowers.", "одарить", "Он решил одарить её цветами."),
    ("distort", "Mirrors can distort your reflection.", "исказить", "Зеркала могут исказить ваше отражение."),
    ("indulge", "I indulge in rest.", "предаваться", "Я предаюсь отдыху."),
    ("near Moscow", "A house near Moscow is ideal.", "подмосковный", "Подмосковный дом идеален."),
    ("exaggeration", "His story was an exaggeration.", "преувеличение", "Его история была преувеличением."),
    ("nutritious", "This food is nutritious.", "питательный", "Эта еда питательная."),
    ("lump", "He swallowed the lump in his throat.", "комок", "Он проглотил комок в горле."),
    ("cotton", "She wore a soft cotton dress.", "хлопок", "Она носила мягкое платье из хлопка."),
    ("speaker", "The speaker presented the research.", "докладчик", "Докладчик представил исследование."),
    ("straw", "The cow slept on the straw.", "солома", "Корова спала на соломе."),
    ("parable", "He told a parable.", "притча", "Он рассказал притчу."),
    ("thoughtful", "He looked thoughtful.", "задумчивый", "Он выглядел задумчивым."),
    ("stanza", "I read the first stanza.", "строфа", "Я прочитал первую строфу."),
    ("guardianship", "She assumed guardianship of her niece.", "опека", "Она взяла на себя опеку над своей племянницей."),
    ("recess", "The sculpture had a small recess.", "углубление", "Скульптура имела небольшое углубление."),
    ("coward", "They called him a coward.", "трус", "Они назвали его трусом."),
    ("refutation", "His refutation silenced the critics.", "опровержение", "Его опровержение заставило критиков замолчать."),
    ("dining", "The dining table is large.", "обеденный", "Обеденный стол большой."),
    ("consulate", "I visited the consulate yesterday.", "консульство", "Я посетил консульство вчера."),
    ("sour", "The lemon is extremely sour.", "кислый", "Лимон очень кислый."),
    ("psychotherapy", "She started psychotherapy last month.", "психотерапия", "Она начала психотерапию в прошлом месяце."),
    ("dividend", "The company announced its annual dividend.", "дивиденд", "Компания объявила о своем ежегодном дивиденде."),
    ("loving", "She is a loving mother.", "любящий", "Она любящая мать."),
    ("throw in", "I will throw in the bag.", "закинуть", "Я закину сумку."),
    ("partition", "We installed a partition in the room.", "перегородка", "Мы установили перегородку в комнате."),
    ("delightful", "The performance was absolutely delightful.", "восхитительный", "Спектакль был абсолютно восхитительным."),
    ("sponge", "I cleaned the table with a sponge.", "губка", "Я вытер стол губкой."),
    ("initiate", "We must initiate the project soon.", "инициировать", "Мы должны скоро инициировать проект."),
    ("miniature", "She collects miniature dolls.", "миниатюрный", "Она коллекционирует миниатюрные куклы."),
    ("inefficient", "The process was slow and inefficient.", "неэффективный", "Процесс был медленным и неэффективным."),
    ("clever girl", "You are a clever girl!", "умница", "Ты умница!"),
    ("overload", "The system faces an overload daily.", "перегрузка", "Система ежедневно сталкивается с перегрузкой."),
    ("mow", "I need to mow the lawn today.", "косить", "Мне нужно сегодня покосить газон."),
    ("loser", "He felt like a complete loser.", "неудачник", "Он чувствовал себя полным неудачником."),
    ("to number", "The stars number millions.", "насчитываться", "Звёзды насчитываются миллионами."),
    ("reasonably", "She priced the goods reasonably.", "разумно", "Она разумно оценила товары."),
    ("to lure", "Bright light lures the birds.", "манить", "Яркий свет манит птиц."),
    ("to nickname", "They decided to nickname him Bear.", "прозвать", "Они решили прозвать его Медведем."),
    ("to acquire", "They wanted to acquire a house.", "обзавестись", "Они хотели обзавестись домом."),
    ("to seize", "They wanted to seize the city.", "завладеть", "Они хотели завладеть городом."),
    ("to be transferred", "The meeting is to be transferred to Monday.", "переноситься", "Встреча переносится на понедельник."),
    ("non-existence", "Philosophers ponder the concept of non-existence.", "небытие", "Философы размышляют о концепции небытия."),
    ("folklore", "This is old folklore.", "фольклор", "Это старый фольклор."),
    ("wealthy person", "A wealthy person bought the mansion.", "богач", "Богач купил особняк."),
    ("Irish", "She loves Irish folk music.", "ирландский", "Она любит ирландскую народную музыку."),
    ("what kind of", "What kind of law is this?", "каковой", "Каковой это закон?"),
    ("to lack", "He seems to lack confidence.", "недоставать", "Ему, кажется, недостаёт уверенности."),
    ("Hebrew", "I am learning Hebrew.", "иврит", "Я учу иврит."),
    ("boulder", "The boulder blocked the path.", "глыба", "Глыба перекрыла тропу."),
    ("aborigine", "The aborigine shared his stories.", "абориген", "Абориген поделился своими историями."),
    ("to sow", "Farmers prepare to sow seeds in spring.", "сеять", "Фермеры готовятся сеять семена весной."),
    ("funnel", "Pour the liquid through the funnel.", "воронка", "Налейте жидкость через воронку."),
    ("decomposition", "Leaves undergo decomposition in autumn.", "разложение", "Листья подвергаются разложению осенью."),
    ("patrol", "The patrol walks at night.", "патруль", "Патруль ходит ночью."),
    ("banquet", "There was a banquet.", "банкет", "Был банкет."),
    ("supernatural", "She believes in a supernatural phenomenon.", "сверхъестественный", "Она верит в сверхъестественное явление."),
    ("to be violated", "Rules are not to be violated.", "нарушаться", "Правила не должны нарушаться."),
    ("to crumble", "The bread will crumble.", "посыпаться", "Хлеб посыплется."),
    ("recipient", "The recipient received the package today.", "получатель", "Получатель получил посылку сегодня."),
    ("inhale", "Inhale deeply to relax.", "вдыхать", "Вдыхайте глубоко, чтобы расслабиться."),
    ("horde", "A horde of warriors approached.", "орда", "Орда воинов приближалась."),
    ("saturated", "The market is saturated with goods.", "насыщенный", "Рынок насыщен товарами."),
    ("Mother of God", "Pray to the Mother of God.", "богородица", "Молись Богородице."),
    ("cavity", "The tree had a large cavity.", "полость", "У дерева была большая полость."),
    ("to ruffle", "The wind will ruffle his hair.", "потрепать", "Ветер потреплет его волосы."),
    ("to starve", "They starve in the siege.", "голодать", "Они голодают в осаде."),
    ("commentator", "The commentator analyzed the game live.", "комментатор", "Комментатор анализировал игру в прямом эфире."),
    ("notary", "The contract was signed by a notary.", "нотариус", "Контракт был подписан нотариусом."),
    ("become empty", "The room will become empty soon.", "опустеть", "Комната скоро опустеет."),
    ("stabilization", "Economic stabilization is important now.", "стабилизация", "Экономическая стабилизация сейчас важна."),
    ("seizure", "This is the seizure of goods.", "изъятие", "Это изъятие товаров."),
    ("preferably", "Preferably, serve it hot.", "предпочтительно", "Предпочтительно подавать его горячим."),
    ("mattress", "I bought a new mattress today.", "матрас", "Я купил новый матрас сегодня."),
    ("observant", "She is very observant.", "наблюдательный", "Она очень наблюдательная."),
    ("election", "His election was surprising.", "избрание", "Его избрание было удивительным."),
    ("undermine", "Criticism can undermine their confidence.", "подорвать", "Критика может подорвать их уверенность."),
    ("to call out", "He turned around to call out her name.", "окликнуть", "Он обернулся, чтобы окликнуть её по имени."),
    ("proportional", "Rewards are proportional to effort.", "пропорциональный", "Награды пропорциональны усилиям."),
    ("crown (of the head)", "He has a mark on the crown of his head.", "макушка", "У него пятно на макушке."),
    ("foreman", "The foreman leads the work.", "бригадир", "Бригадир руководит работой."),
    ("to appeal", "He will appeal for mercy.", "взывать", "Он будет взывать о милости."),
    ("artifact", "They found an ancient artifact underground.", "артефакт", "Они нашли древний артефакт под землёй."),
    ("psycho", "He is acting like a total psycho.", "псих", "Он ведёт себя как настоящий псих."),
    ("compressed", "The air was compressed.", "сжатый", "Воздух был сжатый."),
    ("partnership", "They created a partnership for business.", "товарищество", "Они создали товарищество для бизнеса."),
    ("charity", "She donated generously to charity.", "благотворительность", "Она щедро пожертвовала на благотворительность."),
    ("ditch", "The car went into the ditch.", "канава", "Машина попала в канаву."),
    ("adequately", "He responded adequately to the criticism.", "адекватно", "Он адекватно ответил на критику."),
    ("splashes", "There are splashes of water.", "брызги", "Есть брызги воды."),
    ("lighter", "He lost his lighter yesterday.", "зажигалка", "Он потерял свою зажигалку вчера."),
    ("mysticism", "Mysticism fascinated her deeply.", "мистика", "Мистика глубоко её очаровывала."),
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
    "wore": "wear", "worn": "wear", "slept": "sleep", "taught": "teach",
    "began": "begin", "begun": "begin",
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
