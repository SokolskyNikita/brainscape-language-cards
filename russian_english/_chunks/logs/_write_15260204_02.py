import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from brainscape import answer_lemma_from_card, card_write_payload, cards_from_path, lemma_from_card
from russian_english._chunk_io import rewrite_chunk

PACK = REPO / "russian_english"
SRC = PACK / "_chunks" / "deck_15260204_02.csv"

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
    "works": "work", "working": "work", "sleeping": "sleep",
    "filling": "fill", "starting": "start", "taking": "take",
    "knocked": "knock", "climbed": "climb", "settled": "settle",
    "persuaded": "persuade", "liquidated": "liquidate", "appointed": "appoint",
    "showed": "show", "refused": "refuse", "expected": "expect",
    "recommended": "recommend", "hurt": "hurt",
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
    "залез": "залезть", "залезла": "залезть",
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
    "приватизация": ("privatization", "Это приватизация завода.", "This is privatization of the factory."),
    "союзный": ("allied", "Это союзный договор.", "This is an allied treaty."),
    "оппонент": ("opponent", "Мой оппонент сильный.", "My opponent is strong."),
    "посредник": ("intermediary", "Он наш посредник.", "He is our intermediary."),
    "недовольство": ("discontent", "Его недовольство понятно.", "His discontent is clear."),
    "официант": ("waiter", "Позови официанта.", "Call the waiter."),
    "электричество": ("electricity", "Нет электричества.", "There is no electricity."),
    "наладить": ("set up", "Мы наладили связь.", "We set up the connection."),
    "выбить": ("knock out", "Он выбил зуб.", "He knocked out a tooth."),
    "плавание": ("swimming", "Я люблю плавание.", "I love swimming."),
    "щенок": ("puppy", "Щенок спит.", "The puppy is sleeping."),
    "зелень": ("greenery", "Сад полон зелени.", "The garden is full of greenery."),
    "разбирать": ("take apart", "Он разбирает часы.", "He is taking the watch apart."),
    "сколь": ("how", "Сколь это важно?", "How important is this?"),
    "заводить": ("start", "Он заводит машину.", "He is starting the car."),
    "невероятно": ("incredibly", "Это невероятно сложно.", "This is incredibly hard."),
    "старец": ("elder", "Старец здесь.", "The elder is here."),
    "наполнять": ("fill", "Она наполняет стакан.", "She is filling the glass."),
    "расписание": ("schedule", "Где расписание?", "Where is the schedule?"),
    "дипломат": ("diplomat", "Он дипломат.", "He is a diplomat."),
    "задеть": ("hurt", "Ты задел меня.", "You hurt me."),
    "подавить": ("suppress", "Подави страх.", "Suppress the fear."),
    "кубок": ("cup", "Он взял кубок.", "He took the cup."),
    "вертикальный": ("vertical", "Вертикальная линия.", "A vertical line."),
    "сегмент": ("segment", "Это один сегмент.", "This is one segment."),
    "горшок": ("pot", "Пустой горшок.", "An empty pot."),
    "обидно": ("it's a shame", "Обидно это слышать.", "It's a shame to hear this."),
    "мамаша": ("mama", "Мамаша здесь.", "Mama is here."),
    "неважно": ("it doesn't matter", "Это неважно.", "It doesn't matter."),
    "наводить": ("put in order", "Он наводит порядок.", "Put it in order."),
    "модератор": ("moderator", "Модератор здесь.", "The moderator is here."),
    "кушать": ("eat", "Кушай суп.", "Eat the soup."),
    "подключить": ("connect", "Подключи телефон.", "Connect the phone."),
    "сознавать": ("realize", "Я сознаю ошибку.", "I realize the mistake."),
    "средневековый": ("medieval", "Средневековый город.", "A medieval city."),
    "грудной": ("chest", "Грудная боль.", "Chest pain."),
    "пан": ("sir", "Добрый день, пан.", "Good day, sir."),
    "пирог": ("pie", "Свежий пирог.", "A fresh pie."),
    "откровение": ("revelation", "Это откровение.", "This is a revelation."),
    "первоначально": ("initially", "Первоначально я отказался.", "Initially I refused."),
    "промежуточный": ("intermediate", "Промежуточный этап.", "An intermediate stage."),
    "ирония": ("irony", "Какая ирония.", "What irony."),
    "пускай": ("let", "Пускай идёт.", "Let him go."),
    "рекомендоваться": ("be recommended", "Это рекомендуется.", "This is recommended."),
    "отработать": ("work off", "Он отработал долг.", "He worked off the debt."),
    "осуждать": ("condemn", "Не осуждай её.", "Do not condemn her."),
    "славянский": ("Slavic", "Славянский язык.", "A Slavic language."),
    "безумие": ("madness", "Это безумие.", "This is madness."),
    "закурить": ("light up", "Он вышел закурить.", "He went out to light up."),
    "приподнять": ("lift", "Приподними край.", "Lift the edge."),
    "позаботиться": ("take care of", "Позаботься о ней.", "Take care of her."),
    "величие": ("greatness", "Его величие ясно.", "His greatness is clear."),
    "ожидаться": ("be expected", "Дождь ожидается.", "Rain is expected."),
    "изумление": ("amazement", "Какое изумление.", "What amazement."),
    "штурм": ("assault", "Начался штурм.", "The assault began."),
    "поисковый": ("search", "Это поисковый сайт.", "This is a search site."),
    "выработка": ("output", "Выработка выросла.", "Output grew."),
    "банальный": ("banal", "Банальный вопрос.", "A banal question."),
    "тетрадь": ("notebook", "Открой тетрадь.", "Open the notebook."),
    "сердиться": ("be angry", "Не сердись.", "Do not be angry."),
    "певец": ("singer", "Певец поёт.", "The singer is singing."),
    "вложение": ("investment", "Это плохое вложение.", "This is a bad investment."),
    "шуметь": ("make noise", "Не надо шуметь.", "Do not make noise."),
    "поискать": ("look for", "Надо поискать ключи.", "Look for the keys."),
    "доехать": ("get to", "Надо доехать до дома.", "Get to the house."),
    "исчезновение": ("disappearance", "Его исчезновение странно.", "His disappearance is strange."),
    "склонность": ("inclination", "Склонность к спорту.", "An inclination for sport."),
    "лига": ("league", "Это его лига.", "This is his league."),
    "набережная": ("embankment", "Идём на набережную.", "Let's go to the embankment."),
    "гордо": ("proudly", "Он гордо стоит.", "He stands proudly."),
    "энергичный": ("energetic", "Энергичный парень.", "An energetic guy."),
    "назначать": ("appoint", "Они назначают директора.", "They are appointing a director."),
    "магнитный": ("magnetic", "Магнитное поле.", "A magnetic field."),
    "проявиться": ("show", "Талант проявился.", "The talent showed."),
    "коммунальный": ("communal", "Коммунальная квартира.", "A communal apartment."),
    "уговорить": ("persuade", "Я уговорил маму.", "I persuaded mom."),
    "клавиатура": ("keyboard", "Клавиатура не работает.", "The keyboard does not work."),
    "олимпиада": ("Olympiad", "Школьная олимпиада.", "A school Olympiad."),
    "залезть": ("climb", "Он залез на крышу.", "He climbed onto the roof."),
    "аппаратура": ("equipment", "Аппаратура работает.", "The equipment works."),
    "ликвидировать": ("liquidate", "Они ликвидировали фирму.", "They liquidated the firm."),
    "удивлять": ("surprise", "Ты меня удивляешь.", "You surprise me."),
    "поведать": ("tell", "Поведай правду.", "Tell the truth."),
    "армянин": ("Armenian", "Он армянин.", "He is Armenian."),
    "пограничный": ("border", "Пограничный пост.", "A border post."),
    "злоба": ("spite", "Его злоба ясна.", "His spite is clear."),
    "оскорбление": ("insult", "Это оскорбление.", "This is an insult."),
    "кончик": ("tip", "Кончик носа.", "The tip of the nose."),
    "букет": ("bouquet", "Красивый букет.", "A beautiful bouquet."),
    "кассета": ("cassette", "Старая кассета.", "An old cassette."),
    "профсоюз": ("trade union", "Профсоюз помогает.", "The trade union helps."),
    "поселиться": ("settle", "Они поселились здесь.", "They settled here."),
    "медсестра": ("nurse", "Медсестра пришла.", "The nurse came."),
    "обложка": ("cover", "Обложка книги.", "The book's cover."),
    "позор": ("disgrace", "Какой позор.", "What a disgrace."),
    "вдова": ("widow", "Она вдова.", "She is a widow."),
    "парижский": ("Parisian", "Парижский стиль.", "A Parisian style."),
    "тихонько": ("quietly", "Тихонько иди.", "Go quietly."),
    "европеец": ("European", "Он европеец.", "He is a European."),
    "находка": ("find", "Редкая находка.", "A rare find."),
}


def check_leftovers(dest: Path) -> list[str]:
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
