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

SRC = PACK / "_chunks" / "deck_15260281_01.csv"
OUT = PACK / "_chunks" / "fixed" / "deck_15260281_01.csv"
LOG = PACK / "_chunks" / "logs" / "deck_15260281_01.txt"

FUNCTION_EN = {
    "a", "an", "the", "is", "be", "i", "you", "he", "she", "it", "we", "they",
    "my", "and", "or", "in", "on", "at", "to", "of", "for", "with", "from",
    "not", "his", "him", "her", "their", "them", "our", "us", "me", "am",
    "are", "was", "were", "been", "being", "this", "that", "these", "those",
    "as", "by", "into", "about", "than", "then", "so", "if", "but", "its",
    "your", "do", "does", "did", "will", "would", "can", "could", "may",
    "there", "here", "has", "had", "have", "don't", "dont", "let's", "lets",
    "all", "off", "done",
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
    "давайте", "как", "что", "чтобы", "когда", "если", "где", "чем", "кто",
    "них", "него", "нее", "ней", "ним",
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

# New lemmas introduced by POS / translation corrections (taught on this card).
allow_ru |= {"амур", "сырье", "рязань"}

# (en_lemma, en_ex, ru_lemma, ru_ex)
FIXED = [
    ("chandelier", "The chandelier sparkled above the table.", "люстра", "Люстра сверкала над столом."),
    ("nomenclature", "The nomenclature was complex.", "номенклатура", "Номенклатура была сложной."),
    ("non-existent", "His patience was non-existent.", "несуществующий", "Его терпение было несуществующим."),
    ("the day before yesterday", "I arrived the day before yesterday.", "позавчера", "Я приехал позавчера."),
    ("glowing", "I see a glowing star.", "светящийся", "Я вижу светящуюся звезду."),
    ("regulator", "The regulator controls the pressure.", "регулятор", "Регулятор контролирует давление."),
    ("guild", "She joined the writer's guild.", "гильдия", "Она вступила в гильдию писателей."),
    ("shutdown", "There is a sudden shutdown.", "отключение", "Есть внезапное отключение."),
    ("scroll", "He opened the ancient scroll.", "свиток", "Он открыл древний свиток."),
    ("Gothic", "The cathedral is Gothic.", "готический", "Собор готический."),
    ("Serb", "He is a Serb.", "серб", "Он серб."),
    ("penalty", "He got a penalty.", "штрафной", "Он получил штрафной."),
    ("Amur", "The Amur is a great river.", "Амур", "Амур - большая река."),
    ("companion", "He found a faithful companion.", "компаньон", "Он нашел верного компаньона."),
    ("to evade", "He learned to evade difficult questions.", "уклоняться", "Он научился уклоняться от сложных вопросов."),
    ("intoxication", "Intoxication is in his head.", "опьянение", "Опьянение у него в голове."),
    ("confidential", "This was a confidential talk.", "доверительный", "Это был доверительный разговор."),
    ("rum", "He drinks the old rum slowly.", "ром", "Он медленно пьет старый ром."),
    ("absorption", "The sponge has fast absorption.", "поглощение", "У губки быстрое поглощение."),
    ("stagnation", "Economic stagnation is without progress.", "застой", "Экономический застой без прогресса."),
    ("organizing committee", "The organizing committee met today.", "оргкомитет", "Оргкомитет собрался сегодня."),
    ("physical culture", "Physical culture improves health.", "физкультура", "Физкультура улучшает здоровье."),
    ("friction", "Friction makes heat between surfaces.", "трение", "Трение делает тепло между поверхностями."),
    ("stuffy", "The room felt stuffy and hot.", "душный", "В комнате было душно и жарко."),
    ("discomfort", "He felt discomfort in this place.", "дискомфорт", "Он чувствовал дискомфорт в этом месте."),
    ("nationalwide", "The campaign gained nationalwide attention.", "общенациональный", "Кампания получила общенациональное внимание."),
    ("to stumble upon", "I happen to stumble upon an old friend.", "натыкаться", "Я случайно натыкаюсь на старого друга."),
    ("eve", "Christmas Eve is magical.", "канун", "Канун Рождества волшебный."),
    ("nominal", "The fee was only nominal.", "номинальный", "Плата была только номинальной."),
    ("inhuman", "Their treatment of prisoners was inhuman.", "нечеловеческий", "Их обращение с пленниками было нечеловеческим."),
    ("cartoon", "I watched a cartoon yesterday evening.", "мультфильм", "Вчера вечером я смотрел мультфильм."),
    ("burial mound", "They found an ancient burial mound.", "курган", "Они нашли древний курган."),
    ("to upset", "His words upset her deeply.", "огорчать", "Его слова глубоко её огорчают."),
    ("to ruin", "He will not ruin her life.", "губить", "Он не будет губить её жизнь."),
    ("upward", "The bird flew upward.", "кверху", "Птица полетела кверху."),
    ("cardinal", "The cardinal addressed the people.", "кардинал", "Кардинал обратился к народу."),
    ("backward", "His ideas are considered backward today.", "отсталый", "Его идеи сегодня считаются отсталыми."),
    ("to die out", "These animals died out.", "вымереть", "Эти животные вымерли."),
    ("fertilizer", "We need more fertilizer for tomatoes.", "удобрение", "Нам нужно больше удобрения для помидоров."),
    ("the Lord's", "The church celebrates the Lord's Day.", "господень", "Церковь празднует Господень день."),
    ("raw material", "Cotton is a key raw material.", "сырье", "Хлопок - главное сырье."),
    ("Hindu", "She married a Hindu man.", "индус", "Она вышла замуж за индуса."),
    ("Ryazan", "I visit Ryazan in summer.", "Рязань", "Я посещаю Рязань летом."),
    ("activate", "We must activate this work.", "активизировать", "Мы должны активизировать эту работу."),
    ("graduate school", "She wants graduate school abroad.", "аспирантура", "Она хочет аспирантуру за границей."),
    ("noun", "A noun names a person or thing.", "существительное", "Существительное называет лицо или предмет."),
    ("to spill out", "Water began to spill out.", "вылиться", "Вода начала выливаться."),
    ("tomb", "The pharaoh's tomb was rich.", "гробница", "Гробница фараона была богатой."),
    ("to reign", "A new king began to reign.", "воцариться", "Новый король воцарился."),
    ("settler", "The settler built a new home.", "переселенец", "Переселенец построил новый дом."),
    ("doctoral", "She is pursuing her doctoral studies.", "докторский", "Она занимается своими докторскими исследованиями."),
    ("writing", "I see a writing man.", "пишущий", "Я вижу пишущего человека."),
    ("daughter-in-law", "My daughter-in-law is very kind.", "невестка", "Моя невестка очень добрая."),
    ("lipstick", "She has red lipstick.", "помада", "У неё красная помада."),
    ("sash", "The window sash was closed.", "створка", "Створка окна была закрыта."),
    ("plead", "She will plead for him.", "хлопотать", "Она будет хлопотать за него."),
    ("mirage", "The desert mirage fooled us.", "мираж", "Мираж в пустыне обманул нас."),
    ("individually", "The teacher saw them individually.", "индивидуально", "Учитель видел их индивидуально."),
    ("rejoice", "Let's rejoice at our success.", "ликовать", "Давайте ликовать от нашего успеха."),
    ("overnight stay", "We found an overnight stay.", "ночлег", "Мы нашли ночлег."),
    ("unequal", "Their forces were unequal.", "неравный", "Их силы были неравны."),
    ("sexuality", "She studies her sexuality.", "сексуальность", "Она изучает свою сексуальность."),
    ("philological", "This is a philological text.", "филологический", "Это филологический текст."),
    ("to become famous", "He worked hard to become famous.", "прославиться", "Он много работал, чтобы прославиться."),
    ("meek", "She was meek but strong.", "кроткий", "Она была кроткой, но сильной."),
    ("heroism", "Heroism shines in war.", "героизм", "Героизм сияет на войне."),
    ("philologist", "The philologist read ancient texts.", "филолог", "Филолог читал древние тексты."),
    ("pinch", "She pinched her lips.", "поджать", "Она поджала губы."),
    ("to sweep", "The storm will sweep the city.", "пронестись", "Буря пронесется по городу."),
    ("burning", "I felt a burning pain.", "жгучий", "Я почувствовал жгучую боль."),
    ("aphorism", "This is a short aphorism.", "афоризм", "Это короткий афоризм."),
    ("refueling", "We need refueling.", "заправка", "Нам нужна заправка."),
    ("parishioner", "The parishioner came to church.", "прихожанин", "Прихожанин пришел в церковь."),
    ("urn", "The urn was filled with paper.", "урна", "Урна была наполнена бумагой."),
    ("broom", "She has a broom.", "веник", "У неё есть веник."),
    ("surf", "We listened to the surf at night.", "прибой", "Мы слушали прибой ночью."),
    ("editorial", "The editorial group has a meeting.", "редакционный", "У редакционной группы встреча."),
    ("ladies'", "This is a ladies' room.", "дамский", "Это дамская комната."),
    ("to befit", "This place befits a queen.", "подобать", "Это место подобает королеве."),
    ("evenly", "Spread the paint evenly.", "равномерно", "Распределите краску равномерно."),
    ("carry through", "He will carry through the box.", "пронести", "Он пронесет ящик."),
    ("psychoanalysis", "This is a study of psychoanalysis.", "психоанализ", "Это изучение психоанализа."),
    ("boar", "A wild boar is in the forest.", "кабан", "Дикий кабан в лесу."),
    ("breather", "I need a short breather.", "передышка", "Мне нужна короткая передышка."),
    ("suffocate", "I will suffocate here.", "задохнуться", "Я тут задохнусь."),
    ("embryo", "The embryo began to grow.", "зародыш", "Зародыш начал расти."),
    ("driving", "Driving needs care and skill.", "вождение", "Вождение требует внимания и умения."),
    ("Australian", "This is an Australian city.", "австралийский", "Это австралийский город."),
    ("imperfect", "This work is imperfect.", "несовершенный", "Эта работа несовершенна."),
    ("alloy", "This metal is an alloy of gold.", "сплав", "Этот металл - сплав золота."),
    ("lackey", "He treated me like a lackey.", "лакей", "Он относился ко мне как к лакею."),
    ("mermaid", "The mermaid sang in the sea.", "русалка", "Русалка пела в море."),
    ("abbot", "The abbot led the monastery.", "настоятель", "Настоятель руководил монастырем."),
    ("to boast", "He will boast about this.", "похвастаться", "Он похвастается этим."),
    ("lock", "The boat enters the lock slowly.", "шлюз", "Лодка медленно входит в шлюз."),
    ("bastard", "He is a real bastard.", "ублюдок", "Он настоящий ублюдок."),
    ("amplifier", "He bought a new guitar amplifier.", "усилитель", "Он купил новый усилитель для гитары."),
    ("invalid", "The ticket is invalid now.", "недействительный", "Билет сейчас недействительный."),
    ("to growl", "The dog began to growl.", "рычать", "Собака начала рычать."),
    ("bunker", "They sit in the bunker.", "бункер", "Они сидят в бункере."),
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
    "began": "begin",
    "felt": "feel",
    "found": "find",
    "left": "leave",
    "bought": "buy",
    "thought": "think",
    "knew": "know",
    "said": "say",
    "told": "tell",
    "kept": "keep",
    "heard": "hear",
    "became": "become",
    "built": "build",
    "wrote": "write",
    "read": "read",
    "led": "lead",
    "held": "hold",
    "lost": "lose",
    "paid": "pay",
    "sent": "send",
    "spent": "spend",
    "stood": "stand",
    "sat": "sit",
    "won": "win",
    "ran": "run",
    "hid": "hide",
    "sung": "sing",
    "sang": "sing",
    "flew": "fly",
    "died": "die",
    "swept": "sweep",
    "drank": "drink",
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
    "видим": "видеть",
    "видел": "видеть",
    "знаю": "знать",
    "живу": "жить",
    "живем": "жить",
    "живет": "жить",
    "пьет": "пить",
    "пела": "петь",
    "сидят": "сидеть",
    "нужна": "нужно",
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
