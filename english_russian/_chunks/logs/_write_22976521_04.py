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

SRC = PACK / "_chunks" / "deck_22976521_04.csv"
OUT = PACK / "_chunks" / "fixed" / "deck_22976521_04.csv"
LOG = PACK / "_chunks" / "logs" / "deck_22976521_04.txt"

FUNCTION_EN = {
    "a", "an", "the", "is", "be", "i", "you", "he", "she", "it", "we", "they",
    "my", "and", "or", "in", "on", "at", "to", "of", "for", "with", "from",
    "not", "his", "him", "her", "their", "them", "our", "us", "me", "am",
    "are", "was", "were", "been", "being", "this", "that", "these", "those",
    "as", "by", "into", "about", "than", "then", "so", "if", "but", "its",
    "your", "do", "does", "did", "will", "would", "can", "could", "may",
    "there", "here", "has", "had", "have", "don't", "dont", "let's", "lets",
    "all", "off", "done", "myself", "yourself", "himself", "herself",
    "itself", "ourselves", "themselves", "one's", "ones", "too", "very",
    "also", "still", "even", "only", "just", "i'll", "she's", "he's", "it's",
    "now", "up", "down", "over", "after", "before", "out", "no", "yes",
    "couldn't", "couldnt",
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
    "них", "него", "нее", "ней", "ним", "очень", "слишком",
    "люди", "сюда",
}

allow_en = {
    line.strip().lower()
    for line in (PACK / "_vocab" / "allow_en_22976521.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_ru = {
    line.strip().replace("ё", "е").lower()
    for line in (PACK / "_vocab" / "allow_ru_22976521.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_en |= FUNCTION_EN
allow_ru |= FUNCTION_RU

# New lemmas introduced by corrections (taught on this card).
allow_ru |= {"степь"}

# (en_lemma, en_ex, ru_lemma, ru_ex)
FIXED = [
    ("ecstasy, rapture", "She danced in ecstasy.", "экстаз", "Она танцевала в экстазе."),
    ("by touch, to the touch", "He navigated the room by touch.", "ощупь", "Он ориентировался в комнате на ощупь."),
    ("punk, punk rock", "He loves punk music.", "панк", "Он любит панк-музыку."),
    ("bravo, well done", '"Bravo!" she said.', "браво", '"Браво!" — сказала она.'),
    ("award ceremony, presentation", "The award ceremony starts at eight.", "награждение", "Церемония награждения начинается в восемь."),
    ("to slip away, to elude", "He managed to slip away unnoticed.", "ускользать", "Ему удалось ускользнуть незамеченным."),
    ("bilateral, two-sided", "They signed a bilateral agreement.", "двусторонний", "Они подписали двустороннее соглашение."),
    ("switching, switching over", "Switching channels became annoying.", "переключение", "Переключение каналов стало раздражать."),
    ("steppe, grassland", "The horses ran on the steppe.", "степь", "Лошади бежали по степи."),
    ("restoration, renovation", "The castle's restoration took years.", "реставрация", "Реставрация замка заняла годы."),
    ("vigilance, alertness", "Eternal vigilance is the price of freedom.", "бдительность", "Вечная бдительность - это цена свободы."),
    ("gasp, sigh", "She gasped in surprise.", "ахнуть", "Она ахнула от удивления."),
    ("to line up, to arrange", "People began to line up early.", "выстраиваться", "Люди начали выстраиваться в очередь рано."),
    ("developing, evolving", "A developing country wants progress.", "развивающийся", "Развивающаяся страна хочет прогресса."),
    ("get through, reach by phone", "I couldn't get through to you.", "дозвониться", "Я не смог дозвониться до тебя."),
    ("look, well", "Look, it is raining!", "ишь", "Ишь, дождь идёт!"),
    ("notebook, exercise book", "She filled her notebook with poems.", "тетрадка", "Она заполнила свою тетрадку стихами."),
    ("frosty, freezing", "The morning air felt frosty.", "морозный", "Утренний воздух был морозным."),
    ("enumeration, listing", "The report included an enumeration of facts.", "перечисление", "Отчёт включал перечисление фактов."),
    ("on a par, equally", "She works on a par with us.", "наравне", "Она работает наравне с нами."),
    ("revive, animate", "Music can revive the soul deeply.", "оживить", "Музыка может глубоко оживить душу."),
    ("to get angry, to become enraged", "He got angry quickly.", "разозлиться", "Он быстро разозлился."),
    ("hydrogen", "Hydrogen is the lightest element.", "водород", "Водород — самый лёгкий элемент."),
    ("pharaoh", "The pharaoh was a king.", "фараон", "Фараон был царём."),
    ("miserly, stingy", "He is a miserly man.", "скупой", "Он скупой человек."),
    ("materialism, materiality", "He writes about materialism.", "материализм", "Он пишет о материализме."),
    ("constellation, star cluster", "This is a famous constellation.", "созвездие", "Это известное созвездие."),
    ("unlikely, improbable", "Victory seems unlikely now.", "маловероятный", "Победа сейчас кажется маловероятной."),
    ("neighborly, neighboring", "She offered neighborly help with groceries.", "соседский", "Она предложила соседскую помощь с продуктами."),
    ("fiery, ardent", "He gave a fiery speech.", "пламенный", "Он произнёс пламенную речь."),
    ("fairy, faerie", "The fairy granted her three wishes.", "фея", "Фея исполнила её три желания."),
    ("pogrom, riot", "The pogrom devastated the community.", "погром", "Погром опустошил сообщество."),
    ("premature, untimely", "His answer is premature.", "преждевременный", "Его ответ преждевременный."),
    ("victorious, triumphant", "They sing a victorious song.", "победный", "Они поют победную песню."),
    ("to construct, to erect", "They plan to construct a new bridge.", "возводить", "Они планируют возвести новый мост."),
    ("climb, scramble", "They will climb the mountain tomorrow.", "взобраться", "Они взоберутся на гору завтра."),
    ("tilt, incline", "She will tilt her head curiously.", "наклонить", "Она любопытно наклонит голову."),
    ("canned food, preserves", "I stocked up on canned food.", "консервы", "Я запасся консервами."),
    ("plague, pestilence", "The plague killed many people.", "мор", "Мор убил много людей."),
    ("multimedia, multimedia-based", "This is a multimedia program.", "мультимедийный", "Это мультимедийная программа."),
    ("to mold, to sculpt", "She learned to mold clay beautifully.", "лепить", "Она научилась красиво лепить из глины."),
    ("milligram, mg", "Only a milligram was needed.", "миллиграмм", "Был нужен только миллиграмм."),
    ("estimate, approximate", "I can only estimate the cost.", "прикидывать", "Я могу только прикидывать стоимость."),
    ("smoothly, slickly", "The work went smoothly.", "гладко", "Работа шла гладко."),
    ("rebellion, mutiny", "The rebellion shook the nation.", "мятеж", "Мятеж потряс нацию."),
    ("square, park", "Let's meet in the square.", "сквер", "Давайте встретимся в сквере."),
    ("to hover, to float", "Fog began to hover over the river.", "витать", "Туман начал витать над рекой."),
    ("pierce, break through", "The needle will pierce the fabric easily.", "пробивать", "Игла легко пробьёт ткань."),
    ("to look around, to examine", "I paused to look around the room.", "оглядывать", "Я остановился, чтобы оглядеть комнату."),
    ("maternity leave, decree", "She's on maternity leave now.", "декрет", "Она сейчас в декрете."),
    ("pull out, extract", "Carefully pull out the splinter.", "выдернуть", "Аккуратно выдерните занозу."),
    ("to overflow, to overwhelm", "Water began to overflow the cup.", "переполнять", "Вода начала переполнять чашку."),
    ("Kaliningrad, Kaliningradsky", "This is a Kaliningrad street.", "калининградский", "Это калининградская улица."),
    ("dispute, contest", "They will dispute the unfair charges.", "оспаривать", "Они будут оспаривать несправедливые обвинения."),
    ("leader, chieftain", "The leader inspired his followers greatly.", "предводитель", "Предводитель сильно вдохновил своих последователей."),
    ("loyalty, allegiance", "His loyalty to the company is strong.", "лояльность", "Его лояльность к компании сильная."),
    ("cosmetic, cosmetics", "She bought a new cosmetic set.", "косметический", "Она купила новый косметический набор."),
    ("scandalous, sensational", "Her behavior was absolutely scandalous.", "скандальный", "Её поведение было абсолютно скандальным."),
    ("pile on, crowd", "Critics pile on after the loss.", "навалиться", "Критики навалились после поражения."),
    ("patient (female), female patient", "The patient is in the room now.", "пациентка", "Пациентка сейчас в комнате."),
    ("cast iron, iron", "She cooked in a cast iron pot.", "чугунный", "Она готовила в чугунном горшке."),
    ("relax, unwind", "Just relax and enjoy the moment.", "расслабляться", "Просто расслабьтесь и наслаждайтесь моментом."),
    ("drive away, chase away", "The scarecrow will drive away birds.", "прогонять", "Чучело будет прогонять птиц."),
    ("drive away, repel", "The dog will drive away the cats.", "отгонять", "Собака будет отгонять кошек."),
    ("cynicism", "His cynicism is strong.", "цинизм", "Его цинизм сильный."),
    ("instrumental, tool-based", "He likes instrumental music.", "инструментальный", "Он любит инструментальную музыку."),
    ("briefly, in brief", "He explained the concept briefly.", "вкратце", "Он вкратце объяснил концепцию."),
    ("to stream, to flow", "Water began to stream down the hill.", "струиться", "Вода начала струиться с холма."),
    ("slope, bias", "The road has a slope.", "уклон", "У дороги есть уклон."),
    ("indispensable, irreplaceable", "Water is indispensable for human survival.", "незаменимый", "Вода незаменима для выживания человека."),
    ("pastor, minister", "The pastor delivered a moving sermon.", "пастор", "Пастор произнёс трогательную проповедь."),
    ("Chekist, security officer", "The Chekist monitored the dissidents closely.", "чекист", "Чекист тщательно следил за диссидентами."),
    ("cap, baseball cap", "He always wears his favorite cap.", "кепка", "Он всегда носит свою любимую кепку."),
    ("service, servicing", "This is a service center.", "сервисный", "Это сервисный центр."),
    ("to learn, to get to know", "We want to learn the world.", "познавать", "Мы хотим познавать мир."),
    ("to confess, to admit", "He decided to confess his feelings.", "сознаться", "Он решил сознаться в своих чувствах."),
    ("cable, rope", "The bridge is supported by steel cables.", "трос", "Мост поддерживается стальными тросами."),
    ("shout, cry out", "He will shout your name loudly.", "выкрикивать", "Он будет громко выкрикивать ваше имя."),
    ("drag, bring", "I'll drag the sofa over here.", "притащить", "Я притащу диван сюда."),
    ("to be interrupted, to break off", "His speech began to break off.", "прерываться", "Его речь начала прерываться."),
    ("to pay, to settle", "I need to pay the tax.", "уплатить", "Мне нужно уплатить налог."),
    ("to wriggle, to squirm", "The worm began to wriggle free.", "извиваться", "Червь начал извиваться, чтобы освободиться."),
    ("ideologist, ideologue", "He is a prominent Marxist ideologist.", "идеолог", "Он выдающийся идеолог марксизма."),
    ("wine, vinous", "This is a wine shop.", "винный", "Это винный магазин."),
    ("nobility, gentry", "The nobility lived in this house.", "дворянство", "Дворянство жило в этом доме."),
    ("to comprehend, to grasp", "He cannot comprehend the theory.", "постигать", "Он не может постичь теорию."),
    ("shorts, Bermuda shorts", "He packed shorts for the beach.", "шорты", "Он упаковал шорты для пляжа."),
    ("scoundrel, lowlife", "He is a scoundrel.", "подонок", "Он подонок."),
    ("adjutant, aide-de-camp", "The adjutant brought the letter.", "адъютант", "Адъютант принёс письмо."),
    ("dining, canteen", "This is a dining knife.", "столовый", "Это столовый нож."),
    ("unstable, unsteady", "The chair is unstable.", "неустойчивый", "Стул неустойчивый."),
    ("battle, war", "The prince led the battle.", "рать", "Князь вёл рать."),
    ("brilliantly, splendidly", "She danced brilliantly at the competition.", "блестяще", "Она блестяще танцевала на соревновании."),
    ("observer, reviewer", "The observer noted every detail.", "обозреватель", "Обозреватель отметил каждую деталь."),
    ("to fell, to knock down", "They aimed to fell the old tree.", "повалить", "Они стремились повалить старое дерево."),
    ("touch, contact", "A gentle touch can convey love.", "соприкосновение", "Нежное соприкосновение может передать любовь."),
    ("bait, lure", "He used cheese as mouse bait.", "приманка", "Он использовал сыр в качестве приманки для мышей."),
    ("patient, enduring", "She is very patient with a child.", "терпеливый", "Она очень терпеливая с ребёнком."),
    ("lazybones, slacker", "Get up, you lazybones!", "лентяй", "Вставай, лентяй!"),
    ("Belarusian, Byelorussian", "She married a Belarusian man.", "белорус", "Она вышла замуж за белоруса."),
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
    "felt": "feel",
    "wrote": "write",
    "built": "build",
    "sat": "sit",
    "began": "begin",
    "became": "become",
    "bought": "buy",
    "caught": "catch",
    "kept": "keep",
    "left": "leave",
    "shown": "show",
    "showed": "show",
    "stopped": "stop",
    "heard": "hear",
    "slept": "sleep",
    "dug": "dig",
    "flew": "fly",
    "found": "find",
    "ran": "run",
    "knew": "know",
    "cut": "cut",
    "said": "say",
    "killed": "kill",
    "led": "lead",
    "sang": "sing",
    "shook": "shake",
    "grew": "grow",
    "children": "child",
    "brought": "bring",
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
    "смог": "мочь",
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
    "живёт": "жить",
    "нашел": "найти",
    "нашла": "найти",
    "нашёл": "найти",
    "будь": "быть",
    "стал": "стать",
    "стала": "стать",
    "стали": "стать",
    "пишет": "писать",
    "напиши": "писать",
    "увидел": "видеть",
    "услышал": "слышать",
    "слышу": "слышать",
    "должен": "должный",
    "должны": "должный",
    "жди": "ждать",
    "жду": "ждать",
    "открой": "открыть",
    "храните": "хранить",
    "держите": "держать",
    "сказала": "сказать",
    "идёт": "идти",
    "идет": "идти",
    "хочет": "хотеть",
    "поют": "петь",
    "убил": "убить",
    "людей": "человек",
    "шла": "идти",
    "вёл": "вести",
    "вел": "вести",
    "принёс": "принести",
    "принес": "принести",
    "царем": "царь",
    "царём": "царь",
    "ребенком": "ребенок",
    "ребёнком": "ребенок",
}


def _ru_ok(word: str) -> bool:
    w = word.replace("ё", "е").lower()
    if w in allow_ru:
        return True
    mapped = IRREGULAR_RU.get(w) or IRREGULAR_RU.get(word.lower())
    if mapped and mapped.replace("ё", "е").lower() in allow_ru:
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
    parts = [
        re.sub(r"[^\w'-]+", "", p).strip()
        for p in re.split(r"[,;/]|\s+", lemma.replace("ё", "е").lower())
        if p.strip()
    ]
    keys = [p for p in parts if p not in {"to", "be", "the", "a", "an"}] or parts
    for key in keys:
        stem = key[:4] if len(key) >= 4 else key
        if stem and stem in text.replace(" ", ""):
            return True
        if key in text:
            return True
    return False


def first_gloss(text: str) -> str:
    return re.split(r"[,/]", text)[0].strip().lower()


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
        if first_gloss(old.get("qMdBody") or "") != first_gloss(en_lemma):
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
