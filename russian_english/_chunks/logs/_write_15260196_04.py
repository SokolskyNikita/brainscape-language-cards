import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from brainscape import answer_lemma_from_card, card_write_payload, cards_from_path, lemma_from_card
from russian_english._chunk_io import rewrite_chunk

PACK = REPO / "russian_english"
SRC = PACK / "_chunks" / "deck_15260196_04.csv"

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
    "одной", "одним", "ко",
}

allow_en = {
    line.strip().lower()
    for line in (PACK / "_vocab" / "allow_en_15260196.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_ru = {
    line.strip().replace("ё", "е").lower()
    for line in (PACK / "_vocab" / "allow_ru_15260196.txt").read_text(encoding="utf-8").splitlines()
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
    "fell": "fall", "felt": "feel", "hurt": "hurt", "hurts": "hurt",
    "planned": "plan", "offered": "offer", "sat": "sit", "ran": "run",
}

IRREGULAR_RU = {
    "может": "мочь", "могу": "мочь", "можем": "мочь",
    "хочу": "хотеть", "хочет": "хотеть", "хотим": "хотеть",
    "вижу": "видеть", "видишь": "видеть", "видит": "видеть",
    "видел": "видеть", "видела": "видеть",
    "знаю": "знать", "знает": "знать",
    "живу": "жить", "живет": "жить", "живёт": "жить",
    "шла": "идти", "шел": "идти", "шёл": "идти", "шли": "идти",
    "идет": "идти", "идёт": "идти", "идем": "идти", "идём": "идти",
    "иду": "идти",
    "стал": "стать", "стала": "стать", "стали": "стать",
    "взял": "взять", "взяла": "взять",
    "стоит": "стоять", "стоят": "стоять",
    "болит": "болеть",
    "принес": "принести", "принеси": "принести",
    "прочти": "прочитать",
    "люди": "человек", "людей": "человек",
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
    "вставить": ("insert, put in", "Вставь карту сюда.", "Insert the card here."),
    "вопреки": ("despite, in spite of", "Вопреки дождю мы вышли.", "Despite the rain we left."),
    "халат": ("robe", "Она надела халат.", "She put on a robe."),
    "арабский": ("Arabic", "Она учит арабский.", "She studies Arabic."),
    "снизу": ("from below, from the bottom", "Голос шёл снизу.", "The voice came from below."),
    "крыса": ("rat", "Крыса бежит по земле.", "The rat runs on the ground."),
    "казнь": ("execution", "Казнь была публичной.", "The execution was public."),
    "служащий": ("clerk, employee", "Служащий открыл дверь.", "The clerk opened the door."),
    "развод": ("divorce", "Они хотят развод.", "They want a divorce."),
    "драгоценный": ("precious, valuable", "Это драгоценный камень.", "This is a precious stone."),
    "колебание": ("hesitation, fluctuation", "После колебания он согласился.", "After some hesitation he agreed."),
    "безопасный": ("safe, secure", "Этот путь безопасный.", "This path is safe."),
    "муха": ("fly", "Муха села на стол.", "A fly sat on the table."),
    "заодно": ("at the same time", "Купи хлеб заодно.", "Buy bread at the same time."),
    "капитализм": ("capitalism", "Он говорит о капитализме.", "He talks about capitalism."),
    "весенний": ("spring", "Весенний день ясный.", "The spring day is clear."),
    "могучий": ("mighty, powerful", "Он могучий человек.", "He is a mighty man."),
    "делить": ("share, divide", "Надо делить хлеб.", "We must share the bread."),
    "ледяной": ("icy", "Вода ледяная.", "The water is icy."),
    "жара": ("heat", "Сегодня страшная жара.", "The heat is terrible today."),
    "разбудить": ("wake, awaken", "Разбуди меня рано.", "Wake me early."),
    "рассмеяться": ("laugh, burst out laughing", "Она вдруг рассмеялась.", "She suddenly laughed."),
    "предупреждение": ("warning, notice", "Это важное предупреждение.", "This is an important warning."),
    "нынче": ("nowadays, today", "Нынче очень холодно.", "It is very cold nowadays."),
    "велосипед": ("bicycle, bike", "Где мой велосипед?", "Where is my bicycle?"),
    "фантастический": ("fantastic", "Вид был фантастический.", "The view was fantastic."),
    "рецепт": ("recipe, prescription", "Покажи мне рецепт.", "Show me the recipe."),
    "сан": ("rank, dignity", "Это высокий сан.", "This is a high rank."),
    "махнуть": ("wave", "Она махнула рукой.", "She waved her hand."),
    "смесь": ("mixture, blend", "Это странная смесь.", "This is a strange mixture."),
    "творение": ("creation", "Это его творение.", "This is his creation."),
    "кредитный": ("credit", "У меня кредитная карта.", "I have a credit card."),
    "картошка": ("potato", "Купи картошку.", "Buy potatoes."),
    "мелодия": ("melody, tune", "Какая красивая мелодия.", "What a beautiful melody."),
    "загадочный": ("mysterious", "У него загадочный взгляд.", "He has a mysterious look."),
    "студенческий": ("student", "Это студенческий билет.", "This is a student ticket."),
    "отыскать": ("find, locate", "Я отыскал ключ.", "I will find the key."),
    "вкусный": ("tasty, delicious", "Чай очень вкусный.", "The tea is very tasty."),
    "шестьдесят": ("sixty", "Ему уже шестьдесят.", "He is already sixty."),
    "пробормотать": ("mutter, mumble", "Он пробормотал слово.", "He muttered a word."),
    "полно": ("full of, plenty", "В комнате полно книг.", "The room is full of books."),
    "потерпеть": ("endure, suffer", "Надо потерпеть.", "We must endure it."),
    "мастерство": ("skill", "У него большое мастерство.", "He has great skill."),
    "радиостанция": ("radio station", "Я слушаю радиостанцию.", "I listen to the radio station."),
    "конгресс": ("congress", "Конгресс начал работу.", "Congress started work."),
    "повсюду": ("everywhere, all over", "Снег лежит повсюду.", "Snow lies everywhere."),
    "внешность": ("appearance, looks", "Не суди по внешности.", "Do not judge by appearance."),
    "пешком": ("on foot", "Я иду пешком.", "I go on foot."),
    "персональный": ("personal", "Это мой персональный ключ.", "This is my personal key."),
    "бюро": ("bureau, office", "Он работает в бюро.", "He works in an office."),
    "раздражать": ("irritate, annoy", "Этот шум раздражает.", "This noise irritates me."),
    "столкновение": ("collision, clash", "Произошло столкновение.", "A collision happened."),
    "идеологический": ("ideological", "Это идеологический спор.", "This is an ideological dispute."),
    "отложить": ("postpone", "Надо отложить встречу.", "We must postpone the meeting."),
    "штраф": ("fine, penalty", "Он заплатил штраф.", "He paid a fine."),
    "испанский": ("Spanish", "Она учит испанский.", "She studies Spanish."),
    "воспринять": ("perceive", "Она восприняла новость спокойно.", "She perceived the news calmly."),
    "сниться": ("dream, appear in a dream", "Мне снится море.", "I dream of the sea."),
    "мучить": ("torment, torture", "Он мучит меня.", "He torments me."),
    "дополнение": ("addition, supplement", "Это полезное дополнение.", "This is a useful addition."),
    "цех": ("workshop, department", "Он работает в цехе.", "He works in the workshop."),
    "подчиняться": ("obey, submit", "Надо подчиняться правилам.", "We must obey the rules."),
    "волга": ("Volga", "Волга большая река.", "The Volga is a big river."),
    "здравоохранение": ("healthcare, health care", "Ему нужно здравоохранение.", "He needs healthcare."),
    "решительный": ("decisive, resolute", "Он очень решительный.", "He is very decisive."),
    "наружу": ("outside, outward", "Выйди наружу.", "Go outside."),
    "сократить": ("reduce, cut down", "Надо сократить текст.", "We must reduce the text."),
    "лунный": ("lunar, moon", "Лунная ночь тихая.", "The lunar night is quiet."),
    "упоминать": ("mention", "Не упоминай его имя.", "Do not mention his name."),
    "прошедший": ("past, last", "Это прошедший день.", "This is a past day."),
    "приоритет": ("priority", "Это мой приоритет.", "This is my priority."),
    "бензин": ("gasoline, petrol", "Купи бензин.", "Buy gasoline."),
    "ленинградский": ("Leningrad, Leningradsky", "Это ленинградский вокзал.", "This is the Leningradsky station."),
    "обрадоваться": ("to be glad, to rejoice", "Она обрадовалась подарку.", "She was glad about the gift."),
    "повышать": ("raise, increase", "Они повышают цены.", "They raise prices."),
    "вмешательство": ("intervention, interference", "Его вмешательство помогло.", "His intervention helped."),
    "зерно": ("grain", "Зерно уже сухое.", "The grain is already dry."),
    "ток": ("current", "В доме нет тока.", "There is no current in the house."),
    "стоянка": ("parking, parking lot", "Где стоянка?", "Where is the parking?"),
    "гонка": ("race", "Гонка уже началась.", "The race already started."),
    "обувь": ("shoes", "Купи новую обувь.", "Buy new shoes."),
    "заново": ("again, anew", "Начни заново.", "Start again."),
    "льгота": ("benefit, privilege", "У него есть льгота.", "He has a benefit."),
    "неизбежно": ("inevitably", "Это неизбежно случится.", "This will inevitably happen."),
    "объединять": ("unite", "Они хотят объединять страны.", "They want to unite the countries."),
    "коренной": ("native, indigenous", "Он коренной житель.", "He is a native resident."),
    "демонстрация": ("demonstration", "Демонстрация началась утром.", "The demonstration started in the morning."),
    "временный": ("temporary", "Это временный дом.", "This is a temporary home."),
    "гармония": ("harmony", "Между ними гармония.", "There is harmony between them."),
    "ориентация": ("orientation", "Мне нужна ориентация.", "I need orientation."),
    "модуль": ("module, unit", "Открой этот модуль.", "Open this module."),
    "подвергаться": ("undergo, be subjected", "Он подвергается проверке.", "He undergoes a check."),
    "пообещать": ("promise", "Я пообещал прийти.", "I promised to come."),
    "повседневный": ("everyday, daily", "Это повседневная жизнь.", "This is everyday life."),
    "милость": ("mercy", "Покажи милость.", "Show mercy."),
    "элементарный": ("elementary, basic", "Это элементарный вопрос.", "This is an elementary question."),
    "анализировать": ("analyze", "Надо анализировать факты.", "We must analyze the facts."),
    "интерфейс": ("interface", "Интерфейс простой.", "The interface is simple."),
    "стрела": ("arrow", "Стрела попала в дерево.", "The arrow hit the tree."),
    "охватывать": ("cover, encompass", "Огонь охватывает дом.", "The fire covers the house."),
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
