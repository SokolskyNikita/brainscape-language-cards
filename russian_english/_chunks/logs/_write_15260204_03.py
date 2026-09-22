import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from brainscape import answer_lemma_from_card, card_write_payload, cards_from_path, lemma_from_card
from russian_english._chunk_io import rewrite_chunk

PACK = REPO / "russian_english"
SRC = PACK / "_chunks" / "deck_15260204_03.csv"

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
    "one", "onto", "dont", "doesnt", "lets",
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
    for line in (PACK / "_vocab" / "allow_en_15260204.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_ru = {
    line.strip().replace("ё", "е").lower()
    for line in (PACK / "_vocab" / "allow_ru_15260204.txt").read_text(encoding="utf-8").splitlines()
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
    "sat": "sit", "ran": "run", "running": "run", "runs": "run",
    "hitting": "hit", "going": "go", "coming": "come",
}

IRREGULAR_RU = {
    "может": "мочь", "могу": "мочь", "можем": "мочь",
    "хочу": "хотеть", "хочет": "хотеть", "хотим": "хотеть", "хочешь": "хотеть",
    "вижу": "видеть", "видишь": "видеть", "видит": "видеть",
    "знаю": "знать", "живу": "жить", "живет": "жить", "живёт": "жить", "живём": "жить",
    "шла": "идти", "шел": "идти", "шёл": "идти", "шли": "идти",
    "идет": "идти", "идёт": "идти", "идем": "идти", "идём": "идти",
    "стал": "стать", "стала": "стать", "стали": "стать",
    "поет": "петь", "поёт": "петь", "поют": "петь",
    "вышел": "выйти", "вышла": "выйти",
    "пришла": "прийти", "пришел": "прийти", "пришёл": "прийти",
    "залез": "залезть", "залезла": "залезть",
    "взял": "взять", "взяла": "взять",
    "стоит": "стоять", "стоят": "стоять",
    "сел": "сесть", "села": "сесть",
    "бьет": "бить", "бьёт": "бить",
    "бежит": "бежать",
    "спит": "спать",
    "дай": "дать",
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
    "шлем": ("helmet", "Надень шлем.", "Put on the helmet."),
    "меньшинство": ("minority", "Меньшинство против.", "The minority is against."),
    "нарастать": ("grow", "Шум стал нарастать.", "The noise began to grow."),
    "сарай": ("shed", "В сарае темно.", "It's dark in the shed."),
    "чувствительный": ("sensitive", "Он слишком чувствительный.", "He is too sensitive."),
    "установленный": ("established", "Это установленный факт.", "This is an established fact."),
    "повторный": ("repeated", "Повторный звонок.", "A repeated call."),
    "изобрести": ("invent", "Он хочет изобрести машину.", "He wants to invent a machine."),
    "ван": ("van", "Ван стоит у дома.", "The van is by the house."),
    "добыть": ("obtain", "Надо добыть воду.", "We need to obtain water."),
    "престол": ("throne", "Он на престоле.", "He is on the throne."),
    "вздыхать": ("sigh", "Она стала вздыхать.", "She began to sigh."),
    "бешеный": ("mad", "Он просто бешеный.", "He is just mad."),
    "купаться": ("swim", "Я люблю купаться.", "I love to swim."),
    "пытка": ("torture", "Это пытка.", "This is torture."),
    "навести": ("aim", "Наведи на цель.", "Aim at the target."),
    "парочка": ("couple", "Там стоит парочка.", "A couple is standing there."),
    "проанализировать": ("analyze", "Надо проанализировать это.", "We need to analyze this."),
    "пристально": ("intently", "Он пристально смотрел.", "He looked intently."),
    "критиковать": ("criticize", "Не критикуй её.", "Do not criticize her."),
    "здешний": ("local", "Он здешний.", "He is local."),
    "мчаться": ("race", "Он стал мчаться.", "He began to race."),
    "горожанин": ("townsman", "Он горожанин.", "He is a townsman."),
    "кролик": ("rabbit", "Кролик бежит.", "The rabbit runs."),
    "фундамент": ("foundation", "Фундамент крепкий.", "The foundation is strong."),
    "бал": ("ball", "Она идёт на бал.", "She is going to the ball."),
    "спонсор": ("sponsor", "Кто наш спонсор?", "Who is our sponsor?"),
    "королевство": ("kingdom", "Это большое королевство.", "This is a big kingdom."),
    "герцог": ("duke", "Герцог уже здесь.", "The duke is already here."),
    "оборачиваться": ("turn around", "Не оборачивайся.", "Do not turn around."),
    "ссора": ("quarrel", "Это была ссора.", "That was a quarrel."),
    "останавливать": ("stop", "Не останавливай меня.", "Do not stop me."),
    "внушать": ("inspire", "Его слова внушают страх.", "His words inspire fear."),
    "оправдывать": ("justify", "Не оправдывай себя.", "Do not justify yourself."),
    "разводить": ("breed", "Он разводит собак.", "He breeds dogs."),
    "именовать": ("name", "Как его именуют?", "What do they name him?"),
    "подводить": ("let down", "Не подводи меня.", "Do not let me down."),
    "кран": ("faucet", "Закрой кран.", "Close the faucet."),
    "порядочный": ("decent", "Он порядочный человек.", "He is a decent man."),
    "роковой": ("fateful", "Это роковой час.", "This is a fateful hour."),
    "ступать": ("step", "Не ступай сюда.", "Do not step here."),
    "песенка": ("song", "Какая милая песенка.", "What a nice song."),
    "восемьдесят": ("eighty", "Ей исполнилось восемьдесят.", "She turned eighty."),
    "олень": ("deer", "Олень стоит там.", "A deer is standing there."),
    "настойчиво": ("persistently", "Он настойчиво просил.", "He persistently asked."),
    "барабан": ("drum", "Он бьёт в барабан.", "He is hitting the drum."),
    "катер": ("motorboat", "Катер уже здесь.", "The motorboat is already here."),
    "платный": ("paid", "Это платный вход.", "This is paid entry."),
    "парус": ("sail", "Парус белый.", "The sail is white."),
    "любоваться": ("admire", "Он любовался видом.", "He admired the view."),
    "отключить": ("turn off", "Отключи телефон.", "Turn off the phone."),
    "равнодушный": ("indifferent", "Он равнодушный.", "He is indifferent."),
    "зажечь": ("light", "Надо зажечь свечу.", "Light the candle."),
    "коль": ("if", "Коль хочешь, иди.", "If you want, go."),
    "удаляться": ("move away", "Он стал удаляться.", "He began to move away."),
    "ежегодный": ("annual", "Это ежегодный праздник.", "This is an annual holiday."),
    "расставаться": ("part", "Пора расставаться.", "Time to part."),
    "минувший": ("last", "Минувшим летом.", "Last summer."),
    "злость": ("anger", "Его злость ясна.", "His anger is clear."),
    "вторжение": ("invasion", "Это вторжение.", "This is an invasion."),
    "эра": ("era", "Новая эра.", "A new era."),
    "рожа": ("mug", "Какая у него рожа.", "What a mug he has."),
    "властный": ("authoritative", "У неё властный тон.", "She has an authoritative tone."),
    "жестокость": ("cruelty", "Какая жестокость.", "What cruelty."),
    "сосредоточиться": ("concentrate", "Сосредоточься на деле.", "Concentrate on the matter."),
    "тряпка": ("rag", "Дай тряпку.", "Give me the rag."),
    "показ": ("show", "Показ уже начался.", "The show already started."),
    "залог": ("pledge", "Это залог успеха.", "This is a pledge of success."),
    "ферма": ("farm", "Мы живём на ферме.", "We live on a farm."),
    "познать": ("know", "Он хочет познать мир.", "He wants to know the world."),
    "отделить": ("separate", "Отдели это.", "Separate this."),
    "искра": ("spark", "Видишь искру?", "Do you see the spark?"),
    "оргазм": ("orgasm", "Это был оргазм.", "That was an orgasm."),
    "монополия": ("monopoly", "Это монополия.", "This is a monopoly."),
    "запланировать": ("plan", "Запланируй встречу.", "Plan the meeting."),
    "койка": ("bunk", "Он на койке.", "He is on the bunk."),
    "выигрывать": ("win", "Он любит выигрывать.", "He loves to win."),
    "аптека": ("pharmacy", "Где аптека?", "Where is the pharmacy?"),
    "догнать": ("catch up", "Надо тебя догнать.", "I need to catch up with you."),
    "парадокс": ("paradox", "Это парадокс.", "This is a paradox."),
    "титул": ("title", "Он получил титул.", "He got the title."),
    "треугольник": ("triangle", "Это треугольник.", "This is a triangle."),
    "детектив": ("detective", "Детектив пришёл.", "The detective came."),
    "подозрительный": ("suspicious", "Он подозрительный.", "He is suspicious."),
    "кислород": ("oxygen", "Нам нужен кислород.", "We need oxygen."),
    "вращаться": ("rotate", "Колесо вращается.", "The wheel is rotating."),
    "прыгнуть": ("jump", "Прыгни сюда.", "Jump here."),
    "плавно": ("smoothly", "Дверь плавно открылась.", "The door opened smoothly."),
    "вампир": ("vampire", "Вампир спит днём.", "The vampire sleeps by day."),
    "атрибут": ("attribute", "Это его атрибут.", "This is his attribute."),
    "северо": ("north", "Поверни на северо-запад.", "Turn north-west."),
    "витамин": ("vitamin", "Пей витамины.", "Take the vitamins."),
    "аппетит": ("appetite", "У меня хороший аппетит.", "I have a good appetite."),
    "заверить": ("assure", "Я тебя заверяю.", "I assure you."),
    "инстанция": ("authority", "Спроси в инстанции.", "Ask the authority."),
    "отныне": ("from now on", "Отныне я здесь.", "From now on I am here."),
    "отмена": ("cancellation", "Отмена рейса.", "Cancellation of the flight."),
    "роскошь": ("luxury", "Это роскошь.", "This is luxury."),
    "крошечный": ("tiny", "Крошечный дом.", "A tiny house."),
    "напугать": ("scare", "Ты меня напугал.", "You scared me."),
}


def check_leftovers(dest: Path) -> tuple[list[str], list[str]]:
    leftover: list[str] = []
    missing: list[str] = []
    for i, card in enumerate(cards_from_path(dest), start=1):
        lemma = lemma_from_card(card)
        gloss = answer_lemma_from_card(card)
        payload = card_write_payload(card)
        ru_ex = payload["question"].split("## Footnote")[-1].strip()
        en_ex = payload["answer"].split("## Footnote")[-1].strip()
        lemma_bits = set(re.findall(r"[A-Za-z']+", gloss.lower()))
        for tok in re.findall(r"[A-Za-z']+", en_ex):
            if tok.lower() in lemma_bits:
                continue
            if not _en_ok(tok):
                leftover.append(f"{i} EN {tok} :: {en_ex}")
        ru_bits = set(re.findall(r"[А-Яа-яЁё]+", lemma.lower().replace("ё", "е")))
        for tok in re.findall(r"[А-Яа-яЁё]+", ru_ex):
            if tok.replace("ё", "е").lower() in ru_bits:
                continue
            if not _ru_ok(tok):
                leftover.append(f"{i} RU {tok} :: {ru_ex}")
        if not target_in_example(gloss, en_ex):
            missing.append(f"{i} EN {gloss} :: {en_ex}")
        if not target_in_example(lemma, ru_ex):
            missing.append(f"{i} RU {lemma} :: {ru_ex}")
    return leftover, missing


if __name__ == "__main__":
    stats = rewrite_chunk(SRC, FIXES)
    print(stats)
    leftover, missing = check_leftovers(Path(stats["path"]))
    if leftover:
        print("LEFTOVER:")
        print("\n".join(leftover))
    if missing:
        print("MISSING TARGET:")
        print("\n".join(missing))
    if not leftover and not missing:
        print("leftover=0 missing_target=0")
