import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from brainscape import card_write_payload, cards_from_path, lemma_from_card
from russian_english._chunk_io import rewrite_chunk

PACK = REPO / "russian_english"
SRC = PACK / "_chunks" / "deck_15260224_03.csv"

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
}

IRREGULAR_RU = {
    "может": "мочь", "могу": "мочь", "можем": "мочь",
    "хочу": "хотеть", "хочет": "хотеть", "хотим": "хотеть",
    "вижу": "видеть", "видишь": "видеть", "видит": "видеть",
    "знаю": "знать", "живу": "жить", "живет": "жить", "живёт": "жить",
    "шла": "идти", "шел": "идти", "шёл": "идти", "шли": "идти",
    "идет": "идти", "идёт": "идти", "идем": "идти", "идём": "идти",
    "стал": "стать", "стала": "стать", "стали": "стать",
    "поет": "петь", "поёт": "петь", "поют": "петь",
    "вышел": "выйти", "вышла": "выйти",
    "пришла": "прийти", "пришел": "прийти", "пришёл": "прийти",
    "взял": "взять", "взяла": "взять",
    "стоит": "стоять", "стоят": "стоять",
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
    "зевать": ("yawn, gape", "Он зевает на уроке.", "He yawns in class."),
    "ассистент": ("assistant, aide", "Мой ассистент здесь.", "My assistant is here."),
    "дошкольный": ("preschool, pre-school", "Это дошкольный класс.", "This is a preschool class."),
    "аргументация": ("argumentation, reasoning", "Его аргументация слабая.", "His argumentation is weak."),
    "трибунал": ("tribunal, court", "Это военный трибунал.", "This is a military tribunal."),
    "полумрак": ("twilight, semi-darkness", "В комнате полумрак.", "There is twilight in the room."),
    "целенаправленный": ("purposeful, goal-oriented", "Это целенаправленный шаг.", "This is a purposeful step."),
    "патологический": ("pathological, morbid", "Это патологический страх.", "This is a pathological fear."),
    "лицей": ("lyceum, lycee", "Она учится в лицее.", "She studies at the lyceum."),
    "осмотреться": ("look around, examine", "Я осмотрелся вокруг.", "I look around."),
    "поганый": ("foul, rotten", "Запах поганый.", "The smell is foul."),
    "копа": ("stack, sixty", "Там копа сена.", "There is a stack of hay."),
    "пренебрежение": ("neglect, disregard", "Это пренебрежение долгом.", "This is neglect of duty."),
    "сфотографировать": ("to photograph, to take a picture", "Я сфотографировал дом.", "I photographed the house."),
    "мыльный": ("soapy, soap", "Вода мыльная.", "The water is soapy."),
    "прилетать": ("to arrive, to fly in", "Птицы прилетают весной.", "Birds arrive in spring."),
    "эффектный": ("impressive, spectacular", "Это эффектное платье.", "This is an impressive dress."),
    "побеседовать": ("to chat, to talk", "Я хочу побеседовать с ним.", "I want to chat with him."),
    "усиленный": ("reinforced, strengthened", "Это усиленный мост.", "This is a reinforced bridge."),
    "смешаться": ("to mix, to blend", "Краски смешались.", "The paints mix."),
    "ярославский": ("Yaroslavl", "Это ярославский поезд.", "This is a Yaroslavl train."),
    "кошмарный": ("nightmarish, terrible", "Это кошмарный сон.", "This is a nightmarish dream."),
    "самооценка": ("self-esteem, self-assessment", "У неё низкая самооценка.", "She has low self-esteem."),
    "социалист": ("socialist", "Он социалист.", "He is a socialist."),
    "клад": ("treasure, stash", "Они нашли клад.", "They found a treasure."),
    "прибыльный": ("profitable, lucrative", "Это прибыльный бизнес.", "This is a profitable business."),
    "предосторожность": ("precaution, precautionary measure", "Нужна предосторожность.", "A precaution is needed."),
    "чех": ("Czech", "Мой друг чех.", "My friend is a Czech."),
    "хутор": ("farmstead", "Они живут на хуторе.", "They live on a farmstead."),
    "носилки": ("stretcher, litter", "Врачи несут носилки.", "The doctors carry the stretcher."),
    "стебель": ("stem, stalk", "Стебель цветка тонкий.", "The flower stem is thin."),
    "изрядный": ("considerable, decent", "У него изрядный опыт.", "He has considerable experience."),
    "гравитационный": ("gravitational, gravity", "Это гравитационное поле.", "This is a gravitational field."),
    "виток": ("turn, coil", "Это виток провода.", "This is a coil of wire."),
    "разговорный": ("conversational, colloquial", "Это разговорный язык.", "This is conversational language."),
    "растительность": ("vegetation, flora", "Там густая растительность.", "There is thick vegetation there."),
    "роспись": ("painting, decoration", "На стене роспись.", "There is a painting on the wall."),
    "пята": ("heel", "Пята болит.", "The heel hurts."),
    "запятая": ("comma", "Здесь нужна запятая.", "A comma is needed here."),
    "наивно": ("naively, naive", "Она наивно верит ему.", "She naively believes him."),
    "плацдарм": ("beachhead, bridgehead", "Это наш плацдарм.", "This is our beachhead."),
    "мужичок": ("little man, peasant", "Там стоит мужичок.", "A little man stands there."),
    "циничный": ("cynical", "Это циничный ответ.", "This is a cynical answer."),
    "воплощать": ("embody, incarnate", "Он воплощает силу.", "He embodies force."),
    "сменять": ("to change, to replace", "Они сменяют караул.", "They change the guard."),
    "вдохновлять": ("inspire, motivate", "Музыка вдохновляет меня.", "Music inspires me."),
    "вязать": ("knit, tie", "Она любит вязать шарф.", "She loves to knit a scarf."),
    "незамедлительно": ("immediately, without delay", "Приходи незамедлительно.", "Come immediately."),
    "резина": ("rubber, eraser", "Мяч из резины.", "The ball is of rubber."),
    "взыскание": ("recovery, collection", "Это взыскание долга.", "This is recovery of a debt."),
    "медлить": ("delay, procrastinate", "Не медли.", "Do not delay."),
    "передатчик": ("transmitter, sender", "Передатчик работает.", "The transmitter works."),
    "царапина": ("scratch, scrape", "У него царапина на руке.", "He has a scratch on his hand."),
    "паста": ("paste, pasta", "Это зубная паста.", "This is tooth paste."),
    "согнуть": ("bend, curve", "Согни палку.", "Bend the stick."),
    "настоятельно": ("urgently, insistently", "Я настоятельно прошу.", "I insistently ask."),
    "сжиматься": ("to contract, to shrink", "Ткань сжимается в воде.", "The cloth shrinks in water."),
    "потрудиться": ("to make an effort, to trouble oneself", "Он не потрудился ответить.", "He did not make an effort to answer."),
    "разорить": ("ruin, bankrupt", "Он разорил семью.", "He ruined the family."),
    "альпинист": ("mountaineer, climber", "Альпинист идёт в горы.", "The mountaineer goes to the mountains."),
    "напрягаться": ("to strain, to tense up", "Не напрягайся так.", "Do not strain so."),
    "распадаться": ("disintegrate, fall apart", "Союз распадается.", "The union disintegrates."),
    "гадкий": ("ugly, nasty", "Это гадкий поступок.", "This is a nasty act."),
    "новшество": ("innovation, novelty", "Это полезное новшество.", "This is a useful innovation."),
    "теневой": ("shadow, shadowy", "Это теневой рынок.", "This is a shadow market."),
    "аудио": ("audio, sound", "Это аудио, не видео.", "This is audio, not video."),
    "трап": ("gangway, ramp", "Мы идём по трапу.", "We walk on the gangway."),
    "тайком": ("secretly, covertly", "Она тайком вышла.", "She secretly went out."),
    "материться": ("to swear, to curse", "Не матерись.", "Do not swear."),
    "ржать": ("to neigh, to bray", "Лошадь может ржать.", "The horse can neigh."),
    "непохожий": ("dissimilar, unlike", "Он непохож на отца.", "He is dissimilar to his father."),
    "огорчение": ("disappointment, chagrin", "Это большое огорчение.", "This is a big disappointment."),
    "прут": ("rod, bar", "Он несёт прут.", "He carries a rod."),
    "измучить": ("to exhaust, to torment", "Работа измучила его.", "Work exhausted him."),
    "канцлер": ("chancellor", "Канцлер говорит в зале.", "The chancellor speaks in the hall."),
    "иудейский": ("Jewish, Judaic", "Это иудейский храм.", "This is a Jewish temple."),
    "куб": ("cube, block", "Это красный куб.", "This is a red cube."),
    "электорат": ("electorate, voters", "Весь электорат здесь.", "The whole electorate is here."),
    "бурый": ("brown, dark-brown", "Это бурый медведь.", "This is a brown bear."),
    "прояснить": ("clarify, elucidate", "Проясни этот вопрос.", "Clarify this question."),
    "геолог": ("geologist", "Геолог видит нефть.", "The geologist sees oil."),
    "сочный": ("juicy, succulent", "Этот плод сочный.", "This fruit is juicy."),
    "гастроль": ("tour, guest performance", "Это гастроль театра.", "This is a tour of the theater."),
    "романтик": ("romantic", "Он романтик.", "He is a romantic."),
    "неудачно": ("unsuccessfully", "Он неудачно открыл дверь.", "He unsuccessfully opened the door."),
    "рассудить": ("judge, reason out", "Судья рассудит спор.", "The judge will judge the dispute."),
    "очарование": ("charm, enchantment", "Её очарование сильно.", "Her charm is strong."),
    "моча": ("urine, pee", "Это моча.", "This is urine."),
    "отделиться": ("separate, detach", "Они хотят отделиться.", "They want to separate."),
    "смешивать": ("to mix, to blend", "Она смешивает краску.", "She mixes the paint."),
    "превосходно": ("excellent, superb", "Это превосходно.", "This is excellent."),
    "баржа": ("barge", "Баржа идёт по реке.", "The barge goes down the river."),
    "компас": ("compass", "Компас показывает север.", "The compass shows north."),
    "кнут": ("whip", "Он держит кнут.", "He holds a whip."),
    "обаятельный": ("charming, charismatic", "Он обаятельный человек.", "He is a charming person."),
    "телец": ("Taurus, bull", "Я телец по гороскопу.", "I am a Taurus."),
    "интуитивно": ("intuitively", "Она интуитивно поняла.", "She intuitively understood."),
    "воскреснуть": ("to resurrect, to rise again", "Он хочет воскреснуть.", "He wants to resurrect."),
    "разгадать": ("solve, decipher", "Разгадай загадку.", "Solve the riddle."),
    "зашагать": ("to stride, to step", "Он зашагал к двери.", "He strides to the door."),
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
