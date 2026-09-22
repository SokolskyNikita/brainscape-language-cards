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

SRC = PACK / "_chunks" / "deck_15260263_04.csv"
OUT = PACK / "_chunks" / "fixed" / "deck_15260263_04.csv"
LOG = PACK / "_chunks" / "logs" / "deck_15260263_04.txt"

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
        "а", "но", "или", "них",
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
    "sang": "sing", "shown": "show", "showed": "show", "won": "win",
    "brought": "bring",
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
    ("lift", "He helped lift the table.", "приподнять", "Он помог приподнять стол."),
    ("take care of", "Please take care of my plants.", "позаботиться", "Пожалуйста, позаботьтесь о моих растениях."),
    ("greatness", "I know his true greatness.", "величие", "Я знаю его настоящее величие."),
    ("to be expected", "Delays are to be expected.", "ожидаться", "Задержки ожидаются."),
    ("amazement", "She looked at him in amazement.", "изумление", "Она смотрела на него с изумлением."),
    ("assault", "The army prepared for the assault.", "штурм", "Армия готовилась к штурму."),
    ("output", "The factory's output grew this year.", "выработка", "Выработка завода выросла в этом году."),
    ("banal", "His jokes are banal.", "банальный", "Его шутки банальны."),
    ("notebook", "She filled her notebook.", "тетрадь", "Она заполнила свою тетрадь."),
    ("to be angry", "He tried not to be angry.", "сердиться", "Он старался не сердиться."),
    ("singer", "The singer sings a new song.", "певец", "Певец поёт новую песню."),
    ("to rustle", "The leaf will rustle in the wind.", "шелестеть", "Лист будет шелестеть на ветру."),
    ("to reach", "We plan to reach Moscow by night.", "доехать", "Мы планируем доехать до Москвы к ночи."),
    ("disappearance", "His disappearance surprised me.", "исчезновение", "Его исчезновение меня удивило."),
    ("inclination", "He showed an inclination towards music.", "склонность", "Он проявил склонность к музыке."),
    ("league", "This is a football league.", "лига", "Это футбольная лига."),
    ("embankment", "We walked along the river embankment.", "набережная", "Мы гуляли вдоль набережной реки."),
    ("proudly", "She proudly showed her work.", "гордо", "Она гордо показала свою работу."),
    ("energetic", "He is always so energetic in the mornings.", "энергичный", "Он всегда такой энергичный по утрам."),
    ("magnetic", "This stone is magnetic.", "магнитный", "Этот камень магнитный."),
    ("manifest", "His fear will manifest today.", "проявиться", "Его страх проявится сегодня."),
    ("persuade", "I managed to persuade my friend.", "уговорить", "Мне удалось уговорить моего друга."),
    ("keyboard", "There is coffee on my keyboard.", "клавиатура", "На моей клавиатуре есть кофе."),
    ("Olympiad", "She will go to the Olympiad.", "олимпиада", "Она пойдёт на олимпиаду."),
    ("climb", "He will climb the tree.", "залезть", "Он залезет на дерево."),
    ("to surprise", "I planned to surprise my friend.", "удивлять", "Я планировал удивить моего друга."),
    ("Armenian", "He is Armenian by origin.", "армянин", "Он армянин по происхождению."),
    ("malice", "She spoke with malice.", "злоба", "Она говорила со злобой."),
    ("insult", "He took her words as an insult.", "оскорбление", "Он принял её слова как оскорбление."),
    ("tip", "This is the tip of the nose.", "кончик", "Это кончик носа."),
    ("bouquet", "She received a beautiful bouquet today.", "букет", "Она получила красивый букет сегодня."),
    ("cassette", "I found an old music cassette.", "кассета", "Я нашёл старую музыкальную кассету."),
    ("trade union", "He joined the trade union.", "профсоюз", "Он вступил в профсоюз."),
    ("settle", "They decided to settle in the city.", "поселиться", "Они решили поселиться в городе."),
    ("nurse", "The nurse helped the woman.", "медсестра", "Медсестра помогла женщине."),
    ("disgrace", "His actions are a disgrace to the family.", "позор", "Его действия — позор для семьи."),
    ("widow", "The widow loved her husband.", "вдова", "Вдова любила своего мужа."),
    ("Parisian", "She bought a Parisian dress.", "парижский", "Она купила парижское платье."),
    ("helmet", "He always wears his helmet.", "шлем", "Он всегда носит свой шлем."),
    ("minority", "He is in the minority.", "меньшинство", "Он в меньшинстве."),
    ("shed", "The car is in the shed.", "сарай", "Машина в сарае."),
    ("sensitive", "He is sensitive to cold.", "чувствительный", "Он чувствителен к холоду."),
    ("established", "This is an established rule.", "установленный", "Это установленное правило."),
    ("repeated", "He has a repeated question.", "повторный", "У него повторный вопрос."),
    ("obtain", "They managed to obtain water.", "добыть", "Они смогли добыть воду."),
    ("throne", "The king sat on the throne.", "престол", "Царь сидел на престоле."),
    ("aim", "Aim the camera at the bird.", "навести", "Наведите камеру на птицу."),
    ("couple", "A couple walked by, holding hands.", "парочка", "Мимо прошла парочка, держась за руки."),
    ("intently", "She listened intently.", "пристально", "Она пристально слушала."),
    ("criticize", "They often criticize his work.", "критиковать", "Они часто критикуют его работу."),
    ("townsman", "The townsman lives in the city.", "горожанин", "Горожанин живёт в городе."),
    ("rabbit", "The rabbit ran in the field.", "кролик", "Кролик бежал в поле."),
    ("sponsor", "He is my team's sponsor.", "спонсор", "Он спонсор моей команды."),
    ("duke", "The duke has much land.", "герцог", "У герцога много земли."),
    ("quarrel", "They had a quarrel yesterday evening.", "ссора", "У них вчера вечером была ссора."),
    ("to inspire", "His words began to inspire hope.", "внушать", "Его слова начали внушать надежду."),
    ("to let down", "I promised not to let you down.", "подводить", "Я пообещал тебя не подводить."),
    ("faucet", "Water comes from the faucet.", "кран", "Из крана идёт вода."),
    ("fatal", "The error was fatal to their plan.", "роковой", "Ошибка была роковой для их плана."),
    ("eighty", "She turned eighty yesterday.", "восемьдесят", "Ей вчера исполнилось восемьдесят."),
    ("deer", "I saw a deer on the road.", "олень", "Я видел оленя на дороге."),
    ("persistently", "He persistently asked the question.", "настойчиво", "Он настойчиво задавал вопрос."),
    ("drum", "He played the drum.", "барабан", "Он играл на барабане."),
    ("motorboat", "We took a motorboat for the day.", "катер", "Мы взяли катер на день."),
    ("paid", "The museum has paid lessons.", "платный", "В музее есть платные уроки."),
    ("sail", "I see a white sail.", "парус", "Я вижу белый парус."),
    ("admire", "I want to admire the sunset.", "любоваться", "Я хочу любоваться закатом."),
    ("indifferent", "He seemed indifferent to her tears.", "равнодушный", "Он казался равнодушным к её слезам."),
    ("to light", "He wants to light the candle.", "зажечь", "Он хочет зажечь свечу."),
    ("to move away", "He began to move away slowly.", "удаляться", "Он начал медленно удаляться."),
    ("invasion", "The army began the invasion.", "вторжение", "Армия начала вторжение."),
    ("authoritative", "He spoke in an authoritative tone.", "властный", "Он говорил властным тоном."),
    ("cruelty", "War often brings cruelty.", "жестокость", "Война часто приносит жестокость."),
    ("rag", "I cleaned the table with a rag.", "тряпка", "Я мыл стол тряпкой."),
    ("pledge", "He offered his watch as a pledge.", "залог", "Он предложил свои часы в качестве залога."),
    ("farm", "We visited the farm yesterday.", "ферма", "Мы посетили ферму вчера."),
    ("to know", "I want to know the truth.", "познать", "Я хочу познать правду."),
    ("spark", "A spark will start a fire.", "искра", "Искра начнёт огонь."),
    ("orgasm", "She had an orgasm.", "оргазм", "У неё был оргазм."),
    ("monopoly", "The company has a monopoly.", "монополия", "У компании есть монополия."),
    ("to plan", "We need to plan our trip.", "запланировать", "Нам нужно запланировать нашу поездку."),
    ("pharmacy", "I went to the pharmacy today.", "аптека", "Я сегодня ходил в аптеку."),
    ("catch up", "I need to catch up with you.", "догнать", "Мне нужно тебя догнать."),
    ("paradox", "This is a paradox.", "парадокс", "Это парадокс."),
    ("triangle", "I see a triangle.", "треугольник", "Я вижу треугольник."),
    ("detective", "The detective found the answer quickly.", "детектив", "Детектив быстро нашёл ответ."),
    ("suspicious", "His behavior was very suspicious.", "подозрительный", "Его поведение было очень подозрительным."),
    ("oxygen", "Plants produce oxygen.", "кислород", "Растения производят кислород."),
    ("rotate", "The earth rotates around the sun.", "вращаться", "Земля вращается вокруг солнца."),
    ("to jump", "He asked me to jump first.", "прыгнуть", "Он сказал мне прыгнуть первым."),
    ("smoothly", "The boat moved smoothly on the lake.", "плавно", "Лодка плавно шла по озеру."),
    ("vampire", "The vampire comes at night.", "вампир", "Вампир приходит ночью."),
    ("attribute", "This is her royal attribute.", "атрибут", "Это её королевский атрибут."),
    ("vitamin", "I need more vitamin daily.", "витамин", "Мне нужно больше витамина каждый день."),
    ("appetite", "He has no appetite today.", "аппетит", "У него сегодня нет аппетита."),
    ("certify", "I will certify your documents tomorrow.", "заверить", "Я заверю ваши документы завтра."),
    ("instance", "I sent the letter to another instance.", "инстанция", "Я отправил письмо в другую инстанцию."),
    ("from now on", "From now on I will work every day.", "отныне", "Отныне я буду работать каждый день."),
    ("cancellation", "The flight cancellation surprised us.", "отмена", "Отмена рейса удивила нас."),
    ("luxury", "She lives in luxury.", "роскошь", "Она живёт в роскоши."),
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
    "идти": ("ид", "шл", "ше", "йд"),
    "пойти": ("пой", "пош"),
    "мочь": ("мож", "мог"),
    "учить": ("уч",),
    "взять": ("возьм", "взя"),
    "хотеть": ("хоч", "хот"),
    "петь": ("пою", "пое", "поё", "пел"),
    "видеть": ("виж", "вид"),
    "прийти": ("прид", "приш", "прих"),
    "мыть": ("мою", "мое", "мыл"),
    "любить": ("любл", "люби"),
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
