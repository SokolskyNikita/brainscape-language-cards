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

SRC = PACK / "_chunks" / "deck_15260263_02.csv"
OUT = PACK / "_chunks" / "fixed" / "deck_15260263_02.csv"
LOG = PACK / "_chunks" / "logs" / "deck_15260263_02.txt"

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
        "а", "но", "или",
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
    "led": "lead", "sold": "sell", "paid": "pay", "built": "build",
    "caught": "catch", "taught": "teach", "fell": "fall", "met": "meet",
    "slept": "sleep", "spent": "spend", "won": "win", "drove": "drive",
    "flew": "fly", "drew": "draw", "threw": "throw", "sang": "sing",
    "feet": "foot", "children": "child", "men": "man", "women": "woman",
    "dispersed": "disperse", "studies": "study", "costs": "cost",
}

allow_en = {
    line.strip().lower()
    for line in (PACK / "_vocab" / "allow_en_15260263.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
} | FUNCTION_EN
allow_ru = {
    line.strip().replace("ё", "е").lower()
    for line in (PACK / "_vocab" / "allow_ru_15260263.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
} | FUNCTION_RU

# (en_lemma, en_ex, ru_lemma, ru_ex)
FIXED = [
    ("entry", "The entry ticket costs ten dollars.", "входной", "Входной билет стоит десять долларов."),
    ("survival", "Survival in the wild is hard.", "выживание", "Выживание в дикой природе трудно."),
    ("shame", "She felt deep shame.", "стыд", "Она чувствовала глубокий стыд."),
    ("butterfly", "A butterfly landed on her hand.", "бабочка", "Бабочка села ей на руку."),
    ("autonomous", "This robot is autonomous.", "автономный", "Этот робот автономный."),
    ("ignore", "Just ignore the comments.", "игнорировать", "Просто игнорируйте комментарии."),
    ("to disperse", "The crowd dispersed slowly.", "разойтись", "Толпа медленно разошлась."),
    ("cork", "I bought a bottle without a cork.", "пробка", "Я купил бутылку без пробки."),
    ("laziness", "Laziness often leads to problems.", "лень", "Лень часто приводит к проблемам."),
    ("likeness", "There is a likeness between them.", "подобие", "Между ними есть подобие."),
    ("admiration", "Her work earned admiration.", "восхищение", "Её работа заслужила восхищение."),
    ("to hinder", "The injury began to hinder his progress.", "препятствовать", "Травма начала препятствовать его прогрессу."),
    ("desperate", "He was in a desperate situation.", "отчаянный", "Он был в отчаянном положении."),
    ("coincidence", "This is a coincidence.", "совпадение", "Это совпадение."),
    ("to abandon", "He decided to abandon the project.", "забросить", "Он решил забросить проект."),
    ("bowl", "The bowl is on the table.", "чаша", "Чаша на столе."),
    ("temporarily", "The school is temporarily closed.", "временно", "Школа временно закрыта."),
    ("settlement", "The ancient settlement is near the river.", "поселение", "Древнее поселение у реки."),
    ("motivation", "Her motivation is important.", "мотивация", "Её мотивация важна."),
    ("structural", "The building has a structural problem.", "структурный", "У здания есть структурная проблема."),
    ("child", "Every child deserves love.", "дитя", "Каждое дитя заслуживает любви."),
    ("bourgeois", "He has a bourgeois family.", "буржуазный", "У него буржуазная семья."),
    ("intuition", "I trust her intuition.", "интуиция", "Я верю её интуиции."),
    ("backrest", "The chair has a high backrest.", "спинка", "У стула высокая спинка."),
    ("not a bit", "He was not a bit surprised.", "ничуть", "Он ничуть не удивился."),
    ("Arab", "The Arab man smiled.", "араб", "Араб улыбнулся."),
    ("disgust", "His behavior filled her with disgust.", "отвращение", "Его поведение наполнило её отвращением."),
    ("witch", "The witch lives in the forest.", "ведьма", "Ведьма живёт в лесу."),
    ("expel", "The school decided to expel him.", "выгнать", "Школа решила его выгнать."),
    ("geographical", "This is a geographical map.", "географический", "Это географическая карта."),
    ("lag behind", "He began to lag behind the group.", "отстать", "Он начал отставать от группы."),
    ("questionnaire", "Please fill out the questionnaire.", "анкета", "Пожалуйста, заполните анкету."),
    ("conditionally", "He is conditionally free.", "условно", "Он условно свободен."),
    ("spell", "She said a powerful spell.", "заклинание", "Она произнесла мощное заклинание."),
    ("Allah", "They believe in Allah.", "аллах", "Они верят в Аллаха."),
    ("trap", "He fell into the trap easily.", "ловушка", "Он легко попал в ловушку."),
    ("bribe", "He refused the bribe.", "взятка", "Он отказался от взятки."),
    ("college", "She studies English at the college.", "колледж", "Она учит английский в колледже."),
    ("parental", "Parental love is important.", "родительский", "Родительская любовь важна."),
    ("steamer", "I saw the steamer at dawn.", "пароход", "Я видел пароход на рассвете."),
    ("New Year's", "This is a New Year's gift.", "новогодний", "Это новогодний подарок."),
    ("grandiose", "His plans were grandiose.", "грандиозный", "Его планы были грандиозны."),
    ("disorder", "He suffers from a psychological disorder.", "расстройство", "Он страдает от психического расстройства."),
    ("clan", "The clan is at the meeting.", "клан", "Клан на встрече."),
    ("stranger", "A stranger is at the door.", "незнакомец", "Незнакомец у двери."),
    ("sheep", "The sheep is on the hill.", "овца", "Овца на холме."),
    ("pine", "The pine stands near the house.", "сосна", "Сосна стоит у дома."),
    ("to drive", "I offered to drive her home.", "отвезти", "Я предложил отвезти её домой."),
    ("interval", "There was a short interval.", "промежуток", "Был короткий промежуток."),
    ("vicinity", "We live in the vicinity of the forest.", "окрестность", "Мы живём в окрестности леса."),
    ("foot", "The table is one foot wide.", "фут", "Стол шириной один фут."),
    ("friendly", "He gave me a friendly smile.", "дружеский", "Он подарил мне дружескую улыбку."),
    ("classification", "This classification is new.", "классификация", "Эта классификация новая."),
    ("declaration", "This is a tax declaration.", "декларация", "Это налоговая декларация."),
    ("to function", "The system began to function.", "функционировать", "Система начала функционировать."),
    ("to say goodbye", "They came to say goodbye.", "прощаться", "Они пришли попрощаться."),
    ("to be removed", "This picture will be removed.", "сниматься", "Эта картина снимется."),
    ("thunder", "I heard thunder at night.", "гром", "Я слышал гром ночью."),
    ("dead end", "We reached a dead end.", "тупик", "Мы попали в тупик."),
    ("intensive", "The course was very intensive.", "интенсивный", "Курс был очень интенсивным."),
    ("captive", "The captive waited for help.", "пленный", "Пленный ждал помощи."),
    ("loner", "He has always been a loner.", "одиночка", "Он всегда был одиночкой."),
    ("superiority", "His superiority was clear.", "превосходство", "Его превосходство было ясным."),
    ("candy", "I love candy.", "конфета", "Я люблю конфеты."),
    ("teach", "I will teach you English.", "преподавать", "Я буду преподавать тебе английский."),
    ("literate", "She is highly literate in English.", "грамотный", "Она очень грамотна в английском."),
    ("ethics", "Ethics is important.", "этика", "Этика важна."),
    ("jaw", "He felt pain in his jaw.", "челюсть", "Он чувствовал боль в челюсти."),
    ("impose", "They will impose a new fine.", "наложить", "Они наложат новый штраф."),
    ("romantic", "Their dinner was deeply romantic.", "романтический", "Их ужин был глубоко романтическим."),
    ("urgent", "This matter is urgent.", "срочный", "Это дело срочное."),
    ("approximation", "This is only an approximation.", "приближение", "Это только приближение."),
    ("coup", "The coup was against the government.", "переворот", "Переворот был против правительства."),
    ("accounting", "She works in the accounting department.", "бухгалтерский", "Она работает в бухгалтерском отделе."),
    ("to pass by", "We pass by the park every day.", "проезжать", "Мы каждый день проезжаем мимо парка."),
    ("crawl", "The baby will crawl.", "ползти", "Младенец будет ползти."),
    ("intonation", "Her intonation was strange.", "интонация", "Её интонация была странной."),
    ("Swedish", "This is a Swedish book.", "шведский", "Это шведская книга."),
    ("stereotype", "Stereotypes often hinder understanding.", "стереотип", "Стереотипы часто мешают пониманию."),
    ("regularity", "The experiment confirmed the regularity.", "закономерность", "Эксперимент подтвердил закономерность."),
    ("twilight", "I like twilight in the city.", "сумерки", "Мне нравятся сумерки в городе."),
    ("well-being", "Your well-being is important.", "благополучие", "Ваше благополучие важно."),
    ("refugee", "The refugee is in the city.", "беженец", "Беженец в городе."),
    ("fly away", "The birds will fly away in winter.", "улететь", "Птицы улетят зимой."),
    ("to bring up", "They want to bring up their son well.", "воспитать", "Они хотят хорошо воспитать своего сына."),
    ("dissertation", "She wrote her dissertation.", "диссертация", "Она написала свою диссертацию."),
    ("justification", "He offered no justification for his actions.", "оправдание", "Он не предложил оправдания своим действиям."),
    ("roller", "The door has a roller.", "ролик", "У двери есть ролик."),
    ("charge", "The battery has no charge.", "заряд", "У батареи нет заряда."),
    ("platoon", "The platoon went through the forest.", "взвод", "Взвод прошёл через лес."),
    ("to spit", "He began to spit.", "плевать", "Он начал плевать."),
    ("overcoming", "Overcoming fear is hard.", "преодоление", "Преодоление страха трудно."),
    ("sigh", "She let out a deep sigh.", "вздох", "Она издала глубокий вздох."),
    ("to calm", "She will calm the baby.", "успокаивать", "Она будет успокаивать младенца."),
    ("marshal", "The marshal gave a command.", "маршал", "Маршал дал команду."),
    ("fail", "He will fail the exam tomorrow.", "провалиться", "Он провалится на экзамене завтра."),
    ("reject", "She decided to reject his help.", "отвергнуть", "Она решила отвергнуть его помощь."),
    ("manufacture", "They want to manufacture cars.", "изготовить", "Они хотят изготовить машины."),
    ("rarity", "This book is a rarity.", "редкость", "Эта книга — редкость."),
    ("to invent", "He loves to invent new games.", "придумывать", "Он любит придумывать новые игры."),
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


def ru_ok(text: str, extra: set[str]) -> list[str]:
    bad = []
    pool = allow_ru | extra
    for raw in re.findall(r"[А-Яа-яЁё]+", text):
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
