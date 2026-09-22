import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from brainscape import card_write_payload, cards_from_path, lemma_from_card
from russian_english._chunk_io import rewrite_chunk

PACK = REPO / "russian_english"
SRC = PACK / "_chunks" / "deck_15260224_04.csv"

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
    "ago", "ones", "two", "down", "up", "out", "off", "back",
    "herself", "himself", "themselves", "myself", "yourself",
    "one", "onto", "dont", "doesnt", "lets", "let", "us",
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
    "из-за", "изза", "хорошо", "давай", "скоро", "часто", "один", "одна",
}

allow_en = {
    line.strip().lower()
    for line in (PACK / "_vocab" / "allow_en_15260224.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_ru = {
    line.strip().replace("ё", "е").lower()
    for line in (PACK / "_vocab" / "allow_ru_15260224.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_en |= FUNCTION_EN
allow_ru |= FUNCTION_RU

IRREGULAR_EN = {
    "made": "make", "met": "meet", "saw": "see", "got": "get", "gave": "give",
    "took": "take", "came": "come", "went": "go", "goes": "go", "ate": "eat",
    "spoke": "speak", "broke": "break", "bought": "buy", "built": "build",
    "found": "find", "left": "leave", "held": "hold", "holds": "hold",
    "told": "tell", "said": "say", "heard": "hear", "paid": "pay",
    "sold": "sell", "lost": "lose", "spent": "spend", "stood": "stand",
    "stands": "stand", "wrote": "write", "flew": "fly", "grew": "grow",
    "began": "begin", "became": "become", "did": "do", "done": "do",
    "had": "have", "has": "have", "been": "be", "was": "be", "were": "be",
    "lit": "light", "slept": "sleep", "sang": "sing", "sings": "sing",
    "works": "work", "working": "work", "sleeping": "sleep",
    "understood": "understand", "chose": "choose", "opened": "open",
    "lives": "live", "carries": "carry", "studies": "study",
    "plays": "play", "played": "play", "waits": "wait", "waited": "wait",
    "slips": "slip", "gasped": "gasp", "climbed": "climb", "piled": "pile",
    "felled": "fell", "confessed": "confess", "shouts": "shout",
    "wriggles": "wriggle", "streams": "stream", "drove": "drive",
    "construct": "construct", "constructs": "construct",
    "tilted": "tilt", "molds": "mold", "learned": "learn",
    "dragged": "drag", "hovers": "hover", "pierces": "pierce",
    "disputes": "dispute", "overflows": "overflow", "revives": "revive",
    "estimates": "estimate", "needed": "need",
}

IRREGULAR_RU = {
    "может": "мочь", "могу": "мочь", "можем": "мочь",
    "хочу": "хотеть", "хочет": "хотеть", "хотим": "хотеть",
    "вижу": "видеть", "видишь": "видеть", "видит": "видеть",
    "знаю": "знать", "живу": "жить", "живет": "жить", "живёт": "жить",
    "живут": "жить",
    "шла": "идти", "шел": "идти", "шёл": "идти", "шли": "идти",
    "идет": "идти", "идёт": "идти", "идем": "идти", "идём": "идти",
    "иду": "идти",
    "стал": "стать", "стала": "стать", "стали": "стать",
    "поет": "петь", "поёт": "петь", "поют": "петь",
    "вышел": "выйти", "вышла": "выйти",
    "пришла": "прийти", "пришел": "прийти", "пришёл": "прийти",
    "взял": "взять", "взяла": "взять", "возьми": "взять",
    "стоит": "стоять", "стоят": "стоять",
    "нужна": "нужный", "нужен": "нужный", "нужно": "нужный",
    "купи": "купить", "скажи": "сказать", "сказал": "сказать",
    "играет": "играть", "ждет": "ждать", "ждёт": "ждать",
    "держи": "держать", "надень": "надеть",
    "прошло": "пройти", "прошел": "пройти", "прошёл": "пройти",
    "познаем": "познавать", "познаём": "познавать",
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
    "ем", "ах", "ях", "ам", "ям", "ов", "ев", "ую", "юю", "ая", "яя",
    "ое", "ее", "ые", "ие", "ый", "ий", "ую", "а", "я", "у", "ю", "е", "и",
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


def target_in_example(lemma: str, example: str) -> bool:
    text = example.replace("ё", "е").lower()
    parts = [p.strip() for p in re.split(r"[\s,;]+", lemma.replace("ё", "е").lower()) if p.strip()]
    keys = [p for p in parts if p not in {"to", "be", "the", "a", "an", "of", "it"}] or parts
    compact = text.replace(" ", "")
    for key in keys:
        stem = key[:4] if len(key) >= 4 else key
        if stem and stem in compact:
            return True
        if key in text:
            return True
    return False


FIXES = {
    "экстаз": ("ecstasy, rapture", "Он в экстазе.", "He is in ecstasy."),
    "ощупь": ("by touch, to the touch", "Я иду на ощупь.", "I go by touch."),
    "панк": ("punk, punk rock", "Он любит панк.", "He loves punk."),
    "браво": ("bravo, well done", "Браво!", "Bravo!"),
    "награждение": ("award ceremony, presentation", "Награждение завтра.", "The award ceremony is tomorrow."),
    "ускользать": ("to slip away, to elude", "Он ускользает.", "He slips away."),
    "двусторонний": ("bilateral, two-sided", "Это двусторонний разговор.", "This is a bilateral talk."),
    "переключение": ("switching, switching over", "Нужно переключение.", "Switching is needed."),
    "степной": ("steppe, grassland", "Это степной край.", "This is steppe country."),
    "реставрация": ("restoration, renovation", "Реставрация дома идёт.", "The house needs restoration."),
    "бдительность": ("vigilance, alertness", "Нужна бдительность.", "Vigilance is needed."),
    "ахнуть": ("gasp, sigh", "Она ахнула.", "She gasped."),
    "выстраиваться": ("to line up, to arrange", "Они выстраиваются.", "They line up."),
    "развивающийся": ("developing, evolving", "Это развивающийся мир.", "This is a developing world."),
    "дозвониться": ("get through, reach by phone", "Я не могу дозвониться.", "I cannot get through."),
    "ишь": ("look, well", "Ишь ты!", "Look at you!"),
    "тетрадка": ("notebook, exercise book", "Где тетрадка?", "Where is the notebook?"),
    "морозный": ("frosty, freezing", "День морозный.", "The day is frosty."),
    "перечисление": ("enumeration, listing", "Это перечисление имён.", "This is an enumeration of names."),
    "наравне": ("on a par, equally", "Они живут наравне.", "They live equally."),
    "оживить": ("revive, animate", "Это оживит его.", "This will revive him."),
    "разозлиться": ("to get angry, to become enraged", "Он разозлился.", "He got angry."),
    "водород": ("hydrogen", "Это водород.", "This is hydrogen."),
    "фараон": ("pharaoh", "Это фараон.", "This is a pharaoh."),
    "скупой": ("miserly, stingy", "Он скупой.", "He is miserly."),
    "материализм": ("materialism, materiality", "Это материализм.", "This is materialism."),
    "созвездие": ("constellation, star cluster", "Это созвездие.", "This is a constellation."),
    "маловероятный": ("unlikely, improbable", "Это маловероятный случай.", "This is an unlikely case."),
    "соседский": ("neighborly, neighboring", "Это соседский дом.", "This is a neighboring house."),
    "пламенный": ("fiery, ardent", "Это пламенная речь.", "This is a fiery speech."),
    "фея": ("fairy, faerie", "Это фея.", "This is a fairy."),
    "погром": ("pogrom, riot", "Это погром.", "This is a pogrom."),
    "преждевременный": ("premature, untimely", "Это преждевременный шаг.", "This is a premature step."),
    "победный": ("victorious, triumphant", "Это победный день.", "This is a victorious day."),
    "возводить": ("to construct, to erect", "Они возводят дом.", "They construct a house."),
    "взобраться": ("climb, scramble", "Он взобрался на гору.", "He climbed the mountain."),
    "наклонить": ("tilt, incline", "Наклони голову.", "Tilt the head."),
    "консервы": ("canned food, preserves", "Купи консервы.", "Buy canned food."),
    "мор": ("plague, pestilence", "Это мор.", "This is a plague."),
    "мультимедийный": ("multimedia, multimedia-based", "Это мультимедийный урок.", "This is a multimedia lesson."),
    "лепить": ("to mold, to sculpt", "Она лепит снег.", "She molds snow."),
    "миллиграмм": ("milligram", "Это миллиграмм.", "This is a milligram."),
    "прикидывать": ("estimate, approximate", "Я прикидываю цену.", "I estimate the price."),
    "гладко": ("smoothly, slickly", "Всё прошло гладко.", "All went smoothly."),
    "мятеж": ("rebellion, mutiny", "Это мятеж.", "This is a rebellion."),
    "сквер": ("square, park", "Мы в сквере.", "We are in the park."),
    "витать": ("to hover, to float", "Он витает в облаках.", "He hovers in the clouds."),
    "пробивать": ("pierce, break through", "Он пробивает стену.", "He pierces the wall."),
    "оглядывать": ("to look around, to examine", "Я оглядываю комнату.", "I look around the room."),
    "декрет": ("maternity leave, decree", "Она в декрете.", "She is on maternity leave."),
    "выдернуть": ("pull out, extract", "Выдерни зуб.", "Pull out the tooth."),
    "переполнять": ("to overflow, to overwhelm", "Вода переполняет чашку.", "Water overflows the cup."),
    "калининградский": ("Kaliningrad", "Это калининградский поезд.", "This is a Kaliningrad train."),
    "оспаривать": ("dispute, contest", "Они оспаривают это.", "They dispute this."),
    "предводитель": ("leader, chieftain", "Он предводитель.", "He is a leader."),
    "лояльность": ("loyalty, allegiance", "Это лояльность.", "This is loyalty."),
    "косметический": ("cosmetic, cosmetics", "Это косметический ремонт.", "This is a cosmetic repair."),
    "скандальный": ("scandalous, sensational", "Это скандальный факт.", "This is a scandalous fact."),
    "навалиться": ("pile on, crowd", "Работа навалилась на него.", "Work piled on him."),
    "пациентка": ("patient, female patient", "Пациентка ждёт врача.", "The patient waits for the doctor."),
    "чугунный": ("cast iron, iron", "Это чугунный мост.", "This is a cast iron bridge."),
    "расслабляться": ("relax, unwind", "Я хочу расслабиться.", "I want to relax."),
    "прогонять": ("drive away, chase away", "Прогони кота.", "Drive away the cat."),
    "отгонять": ("drive away, repel", "Он отгоняет собак.", "He drives away the dogs."),
    "цинизм": ("cynicism", "Это цинизм.", "This is cynicism."),
    "инструментальный": ("instrumental, tool-based", "Это инструментальная музыка.", "This is instrumental music."),
    "вкратце": ("briefly, in brief", "Он сказал вкратце.", "He said it briefly."),
    "струиться": ("to stream, to flow", "Вода струится.", "Water streams."),
    "уклон": ("slope, bias", "Здесь уклон.", "There is a slope here."),
    "незаменимый": ("indispensable, irreplaceable", "Он незаменимый друг.", "He is an indispensable friend."),
    "пастор": ("pastor, minister", "Это пастор.", "This is a pastor."),
    "чекист": ("Chekist, security officer", "Это чекист.", "This is a Chekist."),
    "кепка": ("cap, baseball cap", "У него кепка.", "He has a cap."),
    "сервисный": ("service, servicing", "Это сервисный ключ.", "This is a service key."),
    "познавать": ("to learn, to get to know", "Мы познаём мир.", "We learn the world."),
    "сознаться": ("to confess, to admit", "Он сознался.", "He confessed."),
    "трос": ("cable, rope", "Это трос.", "This is a cable."),
    "выкрикивать": ("shout, cry out", "Он выкрикивает имя.", "He shouts the name."),
    "притащить": ("drag, bring", "Притащи стул.", "Drag the chair."),
    "прерываться": ("to be interrupted, to break off", "Разговор прерывается.", "The talk is interrupted."),
    "уплатить": ("to pay, to settle", "Уплати долг.", "Pay the debt."),
    "извиваться": ("to wriggle, to squirm", "Рыба извивается.", "The fish wriggles."),
    "идеолог": ("ideologist, ideologue", "Он идеолог.", "He is an ideologist."),
    "винный": ("wine, vinous", "Это винный магазин.", "This is a wine shop."),
    "дворянство": ("nobility, gentry", "Это дворянство.", "This is the nobility."),
    "постигать": ("to comprehend, to grasp", "Он постигает смысл.", "He comprehends the meaning."),
    "шорты": ("shorts, Bermuda shorts", "Где шорты?", "Where are the shorts?"),
    "подонок": ("scoundrel, lowlife", "Он подонок.", "He is a scoundrel."),
    "адъютант": ("adjutant, aide-de-camp", "Это адъютант.", "This is an adjutant."),
    "столовый": ("dining, canteen", "Это столовый зал.", "This is a dining hall."),
    "неустойчивый": ("unstable, unsteady", "Стол неустойчивый.", "The table is unstable."),
    "рать": ("army, host", "Рать идёт.", "The army is coming."),
    "блестяще": ("brilliantly, splendidly", "Он блестяще играет.", "He plays brilliantly."),
    "обозреватель": ("observer, reviewer", "Он обозреватель.", "He is an observer."),
    "повалить": ("to fell, to knock down", "Ветер повалил дерево.", "The wind felled the tree."),
    "соприкосновение": ("touch, contact", "Это соприкосновение.", "This is contact."),
    "приманка": ("bait, lure", "Это приманка.", "This is bait."),
    "терпеливый": ("patient, enduring", "Он терпеливый.", "He is patient."),
    "лентяй": ("lazybones, slacker", "Он лентяй.", "He is a lazybones."),
    "белорус": ("Belarusian, Byelorussian", "Он белорус.", "He is a Belarusian."),
}


def check_leftovers(dest: Path) -> tuple[list[str], list[str]]:
    leftover: list[str] = []
    missing: list[str] = []
    cards = cards_from_path(dest)
    extra_en = set()
    extra_ru = set()
    for card in cards:
        lemma = lemma_from_card(card)
        extra_ru.update(re.findall(r"[а-яё]+", lemma.lower()))
        gloss = card_write_payload(card)["answer"].split("\n\n", 1)[0]
        extra_en.update(re.findall(r"[a-z']+", gloss.lower()))
    allow_en.update(extra_en)
    allow_ru.update(extra_ru)
    for i, card in enumerate(cards, 1):
        lemma = lemma_from_card(card)
        payload = card_write_payload(card)
        q = payload["question"]
        a = payload["answer"]
        ru_ex = q.split("## Footnote", 1)[-1].strip()
        en_ex = a.split("## Footnote", 1)[-1].strip()
        gloss = a.split("\n\n", 1)[0].strip()
        if not target_in_example(lemma, ru_ex):
            missing.append(f"{i} LEMMA {lemma} :: {ru_ex}")
        if not target_in_example(gloss, en_ex):
            missing.append(f"{i} GLOSS {gloss} :: {en_ex}")
        for tok in re.findall(r"[a-z']+", en_ex.lower()):
            if not _en_ok(tok):
                leftover.append(f"{i} EN {tok} :: {en_ex}")
        for tok in re.findall(r"[а-яё]+", ru_ex.lower()):
            if not _ru_ok(tok):
                leftover.append(f"{i} RU {tok} :: {ru_ex}")
    return leftover, missing


if __name__ == "__main__":
    stats = rewrite_chunk(SRC, FIXES)
    print(stats)
    leftover, missing = check_leftovers(Path(stats["path"]))
    if leftover:
        print("leftovers:")
        print("\n".join(leftover))
    if missing:
        print("missing_target:")
        print("\n".join(missing))
    if not leftover and not missing:
        print("leftover=0 missing_target=0")
