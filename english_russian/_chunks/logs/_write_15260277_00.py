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

SRC = PACK / "_chunks" / "deck_15260277_00.csv"
OUT = PACK / "_chunks" / "fixed" / "deck_15260277_00.csv"
LOG = PACK / "_chunks" / "logs" / "deck_15260277_00.txt"

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

# New target lemmas taught on this slice, plus inflections the stemmer misses.
allow_en |= {
    "began", "chose", "built", "wore", "dug", "sang", "became", "fell", "sold",
    "shown",     "shrank", "sat", "heard", "forgot", "gave", "hung", "felt", "made",
    "spilled", "soared", "underwent", "withstood", "jealous",
}
allow_ru |= {
    "озорство", "басня", "басню", "воронеж", "тверь", "наличные",
    "пришлось", "может", "люблю", "любит", "живёт", "живет", "руки",
    "готов", "села", "умолкла", "листья", "свисают", "ревнует",
    "суетится", "прибавить", "нес", "нёс", "ясна", "ясен", "ясной",
    "канадскую", "воспитанницей", "посоветуемся", "прикрепите",
    "развяжите", "ждала", "отказался", "смешал", "решили", "очистить",
    "забыла", "наступил", "звучала", "гнилым", "прошёл", "прошел",
    "посетил", "посетили", "говорил", "унизить", "улучшает",
    "парил", "высоко", "жили", "чувствовал", "учила", "стал",
    "красным", "независима", "ясной", "перечисленные", "спела",
    "освободиться", "проверьте", "шёл", "шел", "искал", "читали",
    "подожду", "громким", "читаю", "пролил", "выдержал", "долгую",
    "белоснежным", "привёл", "привел", "растёт", "растет",
    "награды", "пятисот", "рублей", "долларов", "симптомов",
    "пользователя", "искусству", "энергии", "кредита", "пули",
    "ветки", "лодоки", "лодки", "глаза", "имени", "имена",
    "книги", "документы", "врачом", "врача", "молоко", "молоку",
    "зиму", "торта", "воде", "мире", "трагедии", "трапезу",
    "ключа", "браслет", "врагом", "заборе", "пролив", "пролива",
    "письму", "солдат", "рублям", "пригороде", "ветке", "табуретке",
    "удел", "демократии", "мелочей", "отсрочку", "фронте",
    "предложения", "коктейль", "сахар", "джаз", "ночь", "рынка",
    "темперамент", "список", "кран", "рану", "университете",
    "радостный", "принуждения", "зонтик", "дома", "подошвой",
    "полдень", "яблоко", "локомотив", "лечение", "билет",
    "летом", "соперника", "опыт", "сокол", "средневековье",
    "ночь", "вещество", "английский", "месяцев", "светофор",
    "субсидию", "честность", "припев", "природу", "калибр",
    "странник", "щелчок", "тумбочке", "мифологию", "погашение",
    "кофе", "осаду", "настроение", "платье", "обычай",
    "напрячься", "швед", "аллергия", "проблема", "природа",
    "наркомании", "сладость", "ткань", "вдохнуть", "смертности",
    "воспитанник", "кузнец", "наглость", "поведению", "поведение",
    "мобилизация", "ворон", "обострению", "жара", "шашку",
    "эквивалент", "толпа", "лист", "опасность", "лодку",
    "приверженец", "подкрепление", "бармен", "факел",
    "сводный", "награды", "патологию", "синоним", "подошва",
    "сирена", "хирургическое", "льготный", "делегат",
    "доступность", "беспокойным", "наркотическое",
    "интенсивно", "финансово", "журналистская", "фотоаппарат",
    "архивные", "покуда", "капризным", "непредсказуемым",
}

# (en_lemma, en_ex, ru_lemma, ru_ex)
FIXED = [
    ("pagan", "This is a pagan custom.", "языческий", "Это языческий обычай."),
    ("to strain", "He had to strain to hear her.", "напрячься", "Ему пришлось напрячься, чтобы слышать её."),
    ("Swede", "The Swede lives in this city.", "швед", "Швед живёт в этом городе."),
    ("allergy", "She has an allergy to milk.", "аллергия", "У неё аллергия на молоко."),
    ("insurmountable", "The problem seemed insurmountable.", "непреодолимый", "Проблема казалась непреодолимой."),
    ("Canadian", "He loves Canadian winter.", "канадский", "Он любит канадскую зиму."),
    ("feline", "Her feline nature is clear.", "кошачий", "Её кошачья природа ясна."),
    ("drug addiction", "His drug addiction is a problem.", "наркомания", "Его наркомания — проблема."),
    ("sweetness", "The cake's sweetness was strong.", "сладость", "Сладость торта была сильной."),
    ("to shrink", "The fabric can shrink in water.", "сесть", "Ткань может сесть в воде."),
    ("to inhale", "I need to inhale deeply and slowly.", "вдохнуть", "Мне нужно глубоко и медленно вдохнуть."),
    ("mortality", "Mortality rates are increasing in the world.", "смертность", "Уровень смертности растёт в мире."),
    ("ward", "She became his ward after the tragedy.", "воспитанник", "Она стала его воспитанницей после трагедии."),
    ("meal", "The family sat down to the meal.", "трапеза", "Семья села за трапезу."),
    ("blacksmith", "The blacksmith made a new key.", "кузнец", "Кузнец сделал новый ключ."),
    ("impudence", "His impudence was clear.", "наглость", "Его наглость была ясной."),
    ("bracelet", "She received a gold bracelet as a gift.", "браслет", "Она получила в подарок золотой браслет."),
    ("consult", "We will consult a doctor tomorrow.", "посоветоваться", "Мы завтра посоветуемся с врачом."),
    ("oddity", "His behavior was an oddity.", "странность", "Его поведение было странностью."),
    ("imaginary", "He saw an imaginary enemy.", "мнимый", "Он видел мнимого врага."),
    ("mobilization", "The mobilization began today.", "мобилизация", "Мобилизация началась сегодня."),
    ("raven", "A raven sat on the fence.", "ворон", "Ворон сидел на заборе."),
    ("exacerbation", "Stress led to the exacerbation of symptoms.", "обострение", "Стресс привёл к обострению симптомов."),
    ("mischief", "The boy loves mischief.", "озорство", "Мальчик любит озорство."),
    ("strait", "The ship navigated the narrow strait.", "пролив", "Корабль прошёл узкий пролив."),
    ("hellish", "The heat was hellish today.", "адский", "Жара сегодня была адская."),
    ("attach", "Attach the document to the letter.", "прикрепить", "Прикрепите документ к письму."),
    ("to throw up", "He is ready to throw up his hands.", "вскинуть", "Он готов вскинуть руки."),
    ("checker", "I lost my last checker.", "шашка", "Я потерял свою последнюю шашку."),
    ("front-line", "This is a front-line soldier.", "фронтовой", "Это фронтовой солдат."),
    ("equivalent", "Five dollars is the equivalent of five hundred rubles.", "эквивалент", "Пять долларов — это эквивалент пятисот рублей."),
    ("to fall silent", "The crowd fell silent.", "умолкнуть", "Толпа умолкла."),
    ("suburb", "We live in a quiet suburb.", "пригород", "Мы живём в тихом пригороде."),
    ("hang down", "A leaf hangs down from the branch.", "свисать", "Лист свисает с ветки."),
    ("to lurk", "Danger lurks around here.", "таиться", "Опасность таится здесь."),
    ("stool", "She sat on the stool quietly.", "табуретка", "Она тихо сидела на табуретке."),
    ("untie", "Please untie the boat.", "развязать", "Пожалуйста, развяжите лодку."),
    ("impatiently", "She waited impatiently.", "нетерпеливо", "Она нетерпеливо ждала."),
    ("to be jealous", "He is jealous of her.", "ревновать", "Он ревнует её."),
    ("lot", "This is my lot.", "удел", "Это мой удел."),
    ("adherent", "He is an adherent of democracy.", "приверженец", "Он приверженец демократии."),
    ("fuss", "She always fusses over small details.", "суетиться", "Она всегда суетится из-за мелочей."),
    ("to rub", "I need to rub my eyes.", "потереть", "Мне нужно потереть глаза."),
    ("deferment", "He received a deferment.", "отсрочка", "Он получил отсрочку."),
    ("reinforcement", "We need reinforcement at the front.", "подкрепление", "Нам нужно подкрепление на фронте."),
    ("similarly", "Similarly, he refused the offer.", "аналогично", "Аналогично, он отказался от предложения."),
    ("bartender", "The bartender mixed a perfect cocktail.", "бармен", "Бармен смешал идеальный коктейль."),
    ("displace", "They want to displace him.", "вытеснить", "Они хотят вытеснить его."),
    ("to add", "I need to add sugar.", "прибавлять", "Мне нужно прибавить сахар."),
    ("jazz", "I love listening to jazz.", "джаз", "Я люблю слушать джаз."),
    ("torch", "He carried the torch through the night.", "факел", "Он нёс факел всю ночь."),
    ("cash", "I need cash for the market.", "наличные", "Мне нужны наличные для рынка."),
    ("temperament", "Her fiery temperament was clear.", "темперамент", "Её огненный темперамент был ясен."),
    ("fable", "I read this fable yesterday.", "басня", "Я читал эту басню вчера."),
    ("consolidated", "The consolidated list is ready.", "сводный", "Сводный список готов."),
    ("drip", "The faucet started to drip slowly.", "капать", "Кран начал медленно капать."),
    ("to honor", "They decided to honor him with a prize.", "удостоить", "Они решили удостоить его награды."),
    ("to cleanse", "We need to cleanse the wound.", "очищать", "Нам нужно очистить рану."),
    ("pathology", "He reads pathology at university.", "патология", "Он читает патологию в университете."),
    ("synonym", "Happy is a synonym for joyful.", "синоним", "Счастливый — это синоним слова радостный."),
    ("coercion", "He refused the coercion.", "принуждение", "Он отказался от принуждения."),
    ("umbrella", "She forgot her umbrella at home.", "зонтик", "Она забыла свой зонтик дома."),
    ("sole", "I stepped on a stone with my sole.", "подошва", "Я наступил на камень подошвой."),
    ("siren", "The siren sounded loudly at noon.", "сирена", "Сирена громко звучала в полдень."),
    ("rotten", "The apple was rotten.", "гнилой", "Яблоко было гнилым."),
    ("locomotive", "The old locomotive still runs smoothly.", "локомотив", "Старый локомотив всё ещё работает плавно."),
    ("surgical", "He underwent surgical treatment yesterday.", "хирургический", "Он прошёл хирургическое лечение вчера."),
    ("privileged", "He received a privileged ticket.", "льготный", "Он получил льготный билет."),
    ("Voronezh", "I visited Voronezh in summer.", "Воронеж", "Я посетил Воронеж летом."),
    ("delegate", "The delegate spoke confidently.", "делегат", "Делегат говорил уверенно."),
    ("humiliate", "They wanted to humiliate their rival.", "унижать", "Они хотели унизить своего соперника."),
    ("accessibility", "Accessibility improves user experience significantly.", "доступность", "Доступность значительно улучшает опыт пользователя."),
    ("to devote oneself", "She decided to devote herself to art.", "посвятить себя", "Она решила посвятить себя искусству."),
    ("falcon", "The falcon soared high above.", "сокол", "Сокол парил высоко."),
    ("Middle Ages", "Knights lived in the Middle Ages.", "средневековье", "Рыцари жили в средневековье."),
    ("restless", "He felt restless all night.", "беспокойный", "Он чувствовал себя беспокойным всю ночь."),
    ("narcotic", "This is a narcotic substance.", "наркотический", "Это наркотическое вещество."),
    ("intensively", "She studied English intensively for months.", "интенсивно", "Она интенсивно учила английский несколько месяцев."),
    ("traffic light", "The traffic light turned red.", "светофор", "Светофор стал красным."),
    ("subsidy", "The government has an energy subsidy.", "субсидия", "У правительства есть субсидия на энергию."),
    ("financially", "She is financially independent now.", "финансово", "Она теперь финансово независима."),
    ("journalistic", "Her journalistic integrity was clear.", "журналистский", "Её журналистская честность была ясной."),
    ("listed", "The listed names are here.", "перечисленный", "Перечисленные имена здесь."),
    ("chorus", "She sang the chorus.", "припев", "Она спела припев."),
    ("to photograph", "I love to photograph nature.", "фотографировать", "Я люблю фотографировать природу."),
    ("to be freed", "They hoped to be freed soon.", "освобождаться", "Они надеялись скоро освободиться."),
    ("caliber", "Check the bullet's caliber.", "калибр", "Проверьте калибр пули."),
    ("wanderer", "The wanderer walked alone.", "странник", "Странник шёл один."),
    ("archival", "We read archival documents yesterday.", "архивный", "Мы читали архивные документы вчера."),
    ("as long as", "I will wait as long as necessary.", "покуда", "Я подожду, покуда это будет нужно."),
    ("click", "This click was loud.", "щелчок", "Этот щелчок был громким."),
    ("nightstand", "My favorite books are on the nightstand.", "тумбочка", "Мои любимые книги на тумбочке."),
    ("mythology", "I read Greek mythology at university.", "мифология", "Я читаю греческую мифологию в университете."),
    ("repayment", "Credit repayment is due tomorrow.", "погашение", "Погашение кредита завтра."),
    ("uh", "Uh, what was your question again?", "гм", "Гм, какой был твой вопрос?"),
    ("spill", "I accidentally spilled my coffee.", "пролить", "Я случайно пролил свой кофе."),
    ("siege", "The castle withstood a long siege.", "осада", "Замок выдержал долгую осаду."),
    ("capricious", "Her mood was capricious and unpredictable.", "капризный", "Её настроение было капризным и непредсказуемым."),
    ("Tver", "We visited Tver in summer.", "Тверь", "Мы посетили Тверь летом."),
    ("snow-white", "Her dress was snow-white.", "белоснежный", "Её платье было белоснежным."),
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
