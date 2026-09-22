import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from brainscape import answer_lemma_from_card, card_write_payload, cards_from_path, lemma_from_card
from russian_english._chunk_io import rewrite_chunk

PACK = REPO / "russian_english"

FUNCTION_EN = {
    "a", "the", "is", "be", "i", "you", "he", "she", "it", "we", "they",
    "my", "and", "or", "in", "on", "at", "to", "of", "for", "with", "from",
    "not", "his", "him", "her", "their", "them", "our", "us", "me", "am",
    "are", "was", "were", "been", "being", "this", "that", "these", "those",
    "an", "as", "by", "into", "about", "than", "then", "so", "if", "but",
    "its", "your", "im", "dont", "cant", "lets", "didnt", "wont", "isnt",
    "don't", "can't", "let's", "didn't", "won't", "isn't", "i'm",
    "there", "here", "very", "too", "now", "today", "yesterday", "tomorrow",
    "some", "any", "all", "no", "yes", "do", "does", "did", "have", "has",
    "had", "will", "would", "can", "could", "should", "must", "may", "might",
    "please", "more", "most", "less", "much", "many", "few", "such", "also",
    "only", "even", "still", "already", "always", "never", "often", "once",
    "after", "before", "under", "over", "through", "between", "without",
    "who", "what", "when", "where", "why", "how", "which",
    "ago", "ones", "two", "down", "up", "out", "off", "back",
    "herself", "himself", "themselves", "myself", "yourself",
    "one", "onto", "away", "soon",
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
    "во", "всё", "все", "всех", "всю", "весь", "слишком", "сам", "самом",
    "из-за", "хорошо", "давай", "скоро", "часто", "один", "одна",
}

allow_en = {
    line.strip().lower()
    for line in (PACK / "_vocab" / "allow_en_15260200.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_ru = {
    line.strip().replace("ё", "е").lower()
    for line in (PACK / "_vocab" / "allow_ru_15260200.txt").read_text(encoding="utf-8").splitlines()
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
    "fell": "fall", "felt": "feel", "ran": "run", "running": "run",
    "cried": "cry", "worked": "work", "says": "say",
    "lagged": "lag", "expelled": "expel", "drinks": "drink",
}

IRREGULAR_RU = {
    "может": "мочь", "могу": "мочь", "можем": "мочь",
    "хочу": "хотеть", "хочет": "хотеть", "хотим": "хотеть",
    "вижу": "видеть", "видишь": "видеть", "видит": "видеть",
    "знаю": "знать", "знаешь": "знать", "знает": "знать",
    "живу": "жить", "живет": "жить", "живёт": "жить",
    "шла": "идти", "шел": "идти", "шёл": "идти", "шли": "идти",
    "идет": "идти", "идёт": "идти", "идем": "идти", "идём": "идти",
    "стал": "стать", "стала": "стать", "стали": "стать",
    "стоит": "стоять", "стоят": "стоять",
    "люблю": "любить", "любит": "любить",
    "говори": "говорить", "говорит": "говорить",
    "скажи": "сказать", "сказал": "сказать",
    "купи": "купить", "кинь": "кинуть",
    "пьет": "пить", "пьёт": "пить",
    "слышит": "слышать", "слышу": "слышать",
    "ведет": "вести", "ведёт": "вести",
    "вожу": "возить", "возит": "возить",
    "кинулся": "кинуться", "кинулась": "кинуться",
    "отнесся": "отнестись", "отнёсся": "отнестись",
    "унес": "унести", "унёс": "унести",
    "разошлась": "разойтись", "разошлись": "разойтись",
    "влюбился": "влюбиться", "влюбилась": "влюбиться",
    "выразился": "выразиться", "выразилась": "выразиться",
    "забросил": "забросить", "забросила": "забросить",
    "отстал": "отстать", "отстала": "отстать",
    "рви": "рвать", "рвет": "рвать", "рвёт": "рвать",
    "береги": "беречь", "бережет": "беречь", "бережёт": "беречь",
    "надень": "надеть",
    "обманывай": "обманывать",
    "обижайся": "обижаться",
    "нападай": "нападать",
    "сжимай": "сжимать",
    "толкай": "толкать",
    "игнорируй": "игнорировать",
    "препятствуй": "препятствовать",
    "обвинили": "обвинить",
    "накопил": "накопить",
    "отразило": "отразить",
    "выгнали": "выгнать",
    "завершится": "завершиться",
    "украсим": "украсить",
    "наградят": "наградить",
    "протягивает": "протягивать",
    "превосходит": "превосходить",
    "высказывает": "высказывать",
    "шагают": "шагать",
    "заменяем": "заменять",
    "снижаем": "снижать",
    "оплачиваю": "оплачивать",
    "обслуживают": "обслуживать",
    "изучаю": "изучать",
    "получил": "получить",
    "работает": "работать",
    "закрыт": "закрыть",
}

RU_ENDINGS = (
    "ами", "ями", "ого", "его", "ому", "ему", "ыми", "ими", "ой", "ей", "ом",
    "ем", "ах", "ях", "ам", "ям", "ов", "ев", "ую", "юю", "ая", "яя",
    "ое", "ее", "ые", "ие", "ый", "ий", "ую", "а", "я", "у", "ю", "е", "и",
    "ы", "о", "ь",
)


def _en_ok(word: str) -> bool:
    w = word.lower().replace("'", "")
    if w in allow_en:
        return True
    if IRREGULAR_EN.get(word.lower()) in allow_en:
        return True
    if "-" in word and all(_en_ok(p) for p in word.split("-") if p):
        return True
    if word.lower().endswith("'s") and word.lower()[:-2] in allow_en:
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


def _ru_ok(word: str) -> bool:
    w = word.replace("ё", "е").lower()
    if w in allow_ru:
        return True
    if IRREGULAR_RU.get(w) in allow_ru:
        return True
    stems = {w}
    for suf in RU_ENDINGS:
        if w.endswith(suf) and len(w) - len(suf) >= 3:
            stems.add(w[: -len(suf)])
    for stem in stems:
        if stem in allow_ru:
            return True
        if any(
            a.startswith(stem) or stem.startswith(a)
            for a in allow_ru
            if len(a) >= 4 and len(stem) >= 4
        ):
            return True
    return False


def _tokens(text: str) -> list[str]:
    return re.findall(r"[A-Za-zА-Яа-яЁё'-]+", text)


print(
    rewrite_chunk(
        Path("russian_english/_chunks/deck_15260200_04.csv"),
        {
            "сельскохозяйственный": (
                "agricultural, agrarian",
                "Это сельскохозяйственный труд.",
                "This is agricultural work.",
            ),
            "путешествовать": (
                "to travel, to journey",
                "Я люблю путешествовать.",
                "I love to travel.",
            ),
            "молочный": (
                "milky, dairy",
                "Она пьёт молочный чай.",
                "She drinks milky tea.",
            ),
            "струя": (
                "jet, stream",
                "Это сильная струя.",
                "This is a strong jet.",
            ),
            "галстук": (
                "tie, necktie",
                "Это красный галстук.",
                "This is a red tie.",
            ),
            "обманывать": (
                "deceive, cheat",
                "Не обманывай меня.",
                "Do not deceive me.",
            ),
            "последовательный": (
                "consecutive, sequential",
                "Это последовательный день.",
                "This is a consecutive day.",
            ),
            "развить": (
                "develop, evolve",
                "Надо развить навык.",
                "We must develop the skill.",
            ),
            "нрав": (
                "character, temperament",
                "У него хороший нрав.",
                "He has a good character.",
            ),
            "измена": (
                "betrayal, treachery",
                "Это была измена.",
                "This was a betrayal.",
            ),
            "наградить": (
                "award, honor",
                "Её наградят завтра.",
                "They will award her tomorrow.",
            ),
            "обижаться": (
                "to be offended, to take offense",
                "Не обижайся.",
                "Do not be offended.",
            ),
            "кинуться": (
                "to rush, to throw oneself",
                "Он кинулся к двери.",
                "He rushed to the door.",
            ),
            "вдали": (
                "in the distance, afar",
                "Дом стоит вдали.",
                "The house stands in the distance.",
            ),
            "нападать": (
                "to attack, to assault",
                "Не нападай на него.",
                "Do not attack him.",
            ),
            "кабель": (
                "cable, wire",
                "Кабель на столе.",
                "The cable is on the table.",
            ),
            "туфля": (
                "shoe, pump",
                "Это красная туфля.",
                "This is a red shoe.",
            ),
            "сжимать": (
                "to squeeze, to compress",
                "Не сжимай меня.",
                "Do not squeeze me.",
            ),
            "отнестись": (
                "treat, relate",
                "Он хорошо отнёсся ко мне.",
                "He treated me well.",
            ),
            "изящный": (
                "elegant, graceful",
                "Это изящное платье.",
                "This is an elegant dress.",
            ),
            "накопить": (
                "accumulate, save",
                "Он накопил навык.",
                "He accumulated a skill.",
            ),
            "превосходить": (
                "to surpass, to exceed",
                "Он превосходит нас.",
                "He surpasses us.",
            ),
            "пение": (
                "singing, chant",
                "Я слышу пение.",
                "I hear singing.",
            ),
            "статуя": (
                "statue, sculpture",
                "Статуя стоит в парке.",
                "The statue stands in the park.",
            ),
            "обвинить": (
                "accuse, charge",
                "Его обвинили.",
                "They accused him.",
            ),
            "трезвый": (
                "sober, abstinent",
                "Он сегодня трезвый.",
                "He is sober today.",
            ),
            "монстр": (
                "monster, beast",
                "Это страшный монстр.",
                "This is a scary monster.",
            ),
            "протягивать": (
                "to stretch out, to extend",
                "Он протягивает письмо.",
                "He stretches out the letter.",
            ),
            "распад": (
                "decay, disintegration",
                "Это полный распад.",
                "This is full decay.",
            ),
            "возражение": (
                "objection, protest",
                "У меня есть возражение.",
                "I have an objection.",
            ),
            "украсить": (
                "decorate, adorn",
                "Давай украсим комнату.",
                "Let's decorate the room.",
            ),
            "беречь": (
                "to cherish, to conserve",
                "Береги здоровье.",
                "Cherish your health.",
            ),
            "проводник": (
                "conductor, guide",
                "Проводник ведёт нас.",
                "The conductor leads us.",
            ),
            "шагать": (
                "march, walk",
                "Солдаты шагают вместе.",
                "The soldiers march together.",
            ),
            "высказывать": (
                "to express, to voice",
                "Она высказывает правду.",
                "She expresses the truth.",
            ),
            "возить": (
                "carry, transport",
                "Надо возить его.",
                "I need to carry him.",
            ),
            "неведомый": (
                "unknown, mysterious",
                "Это неведомый путь.",
                "This is an unknown path.",
            ),
            "проектирование": (
                "design, planning",
                "Это проектирование дома.",
                "This is house design.",
            ),
            "унести": (
                "carry away, take away",
                "Ветер унёс шляпу.",
                "The wind carried away the hat.",
            ),
            "прекращение": (
                "cessation, termination",
                "Это прекращение работы.",
                "This is a cessation of work.",
            ),
            "устранить": (
                "eliminate, remove",
                "Надо устранить ошибку.",
                "We must eliminate the error.",
            ),
            "нежность": (
                "tenderness, gentleness",
                "В её голосе нежность.",
                "There is tenderness in her voice.",
            ),
            "сынок": (
                "son, little son",
                "Мой сынок дома.",
                "My son is at home.",
            ),
            "грамота": (
                "certificate, diploma",
                "Он получил грамоту.",
                "He received a certificate.",
            ),
            "химия": (
                "chemistry, alchemy",
                "Я изучаю химию.",
                "I study chemistry.",
            ),
            "тысячелетие": (
                "millennium, millenary",
                "Это новое тысячелетие.",
                "This is a new millennium.",
            ),
            "тревожный": (
                "anxious, alarming",
                "Он очень тревожный.",
                "He is very anxious.",
            ),
            "заповедь": (
                "commandment, precept",
                "Это старая заповедь.",
                "This is an old commandment.",
            ),
            "пруд": (
                "pond, pool",
                "Пруд рядом с домом.",
                "The pond is near the house.",
            ),
            "входной": (
                "entry, entrance",
                "Это входной билет.",
                "This is an entry ticket.",
            ),
            "выживание": (
                "survival, endurance",
                "Выживание здесь трудное.",
                "Survival here is hard.",
            ),
            "стыд": (
                "shame, embarrassment",
                "Это большой стыд.",
                "This is a big shame.",
            ),
            "заменять": (
                "replace, substitute",
                "Мы заменяем окно.",
                "We replace the window.",
            ),
            "толкать": (
                "push, shove",
                "Не толкай меня.",
                "Do not push me.",
            ),
            "бабочка": (
                "butterfly, bow tie",
                "Я вижу бабочку.",
                "I see a butterfly.",
            ),
            "автономный": (
                "autonomous, self-contained",
                "Это автономный район.",
                "This is an autonomous region.",
            ),
            "игнорировать": (
                "ignore, disregard",
                "Не игнорируй меня.",
                "Do not ignore me.",
            ),
            "разойтись": (
                "to disperse, to part ways",
                "Толпа разошлась.",
                "The crowd dispersed.",
            ),
            "пробка": (
                "traffic jam, cork",
                "Сегодня большая пробка.",
                "There is a big traffic jam today.",
            ),
            "влюбиться": (
                "to fall in love, to become enamored",
                "Я влюбился в неё.",
                "I fell in love with her.",
            ),
            "лень": (
                "laziness, indolence",
                "Это чистая лень.",
                "This is pure laziness.",
            ),
            "мрак": (
                "darkness, gloom",
                "В комнате мрак.",
                "There is darkness in the room.",
            ),
            "артиллерийский": (
                "artillery, gunnery",
                "Это артиллерийский огонь.",
                "This is artillery fire.",
            ),
            "подобие": (
                "likeness, resemblance",
                "Это только подобие.",
                "This is only a likeness.",
            ),
            "восхищение": (
                "admiration, delight",
                "Я смотрю с восхищением.",
                "I look with admiration.",
            ),
            "препятствовать": (
                "to hinder, to obstruct",
                "Не препятствуй мне.",
                "Do not hinder me.",
            ),
            "отчаянный": (
                "desperate, hopeless",
                "Это отчаянный шаг.",
                "This is a desperate step.",
            ),
            "совпадение": (
                "coincidence, match",
                "Это чистое совпадение.",
                "This is a pure coincidence.",
            ),
            "забросить": (
                "to abandon, to throw",
                "Он забросил спорт.",
                "He abandoned sports.",
            ),
            "выразиться": (
                "to express, to phrase",
                "Он плохо выразился.",
                "He expressed himself poorly.",
            ),
            "чаша": (
                "bowl, cup",
                "Чаша на столе.",
                "The bowl is on the table.",
            ),
            "рама": (
                "frame, chassis",
                "Это старая рама.",
                "This is an old frame.",
            ),
            "биржа": (
                "exchange, stock market",
                "Он работает на бирже.",
                "He works at the exchange.",
            ),
            "временно": (
                "temporarily, for the time being",
                "Магазин временно закрыт.",
                "The store is temporarily closed.",
            ),
            "поселение": (
                "settlement, community",
                "Это старое поселение.",
                "This is an old settlement.",
            ),
            "мотивация": (
                "motivation, incentive",
                "У него нет мотивации.",
                "He has no motivation.",
            ),
            "структурный": (
                "structural, configurational",
                "Это структурный вопрос.",
                "This is a structural question.",
            ),
            "дитя": (
                "child, infant",
                "Это маленькое дитя.",
                "This is a small child.",
            ),
            "оплачивать": (
                "to pay, to compensate",
                "Я оплачиваю это.",
                "I pay this.",
            ),
            "буржуазный": (
                "bourgeois",
                "Это буржуазный дом.",
                "This is a bourgeois house.",
            ),
            "интуиция": (
                "intuition, instinct",
                "У неё сильная интуиция.",
                "She has strong intuition.",
            ),
            "спинка": (
                "backrest, back",
                "Спинка стула высокая.",
                "The chair backrest is high.",
            ),
            "ничуть": (
                "not a bit, not at all",
                "Это ничуть не важно.",
                "This is not a bit important.",
            ),
            "снижать": (
                "reduce, lower",
                "Мы снижаем это.",
                "We reduce this.",
            ),
            "отразить": (
                "reflect, repel",
                "Зеркало отразило свет.",
                "The mirror reflected the light.",
            ),
            "араб": (
                "Arab, Arabian",
                "Он араб.",
                "He is an Arab.",
            ),
            "стихия": (
                "element, natural force",
                "Это сильная стихия.",
                "This is a strong element.",
            ),
            "отвращение": (
                "disgust, revulsion",
                "У меня отвращение к этому.",
                "I have disgust for this.",
            ),
            "исследовательский": (
                "research, investigative",
                "Это исследовательский центр.",
                "This is a research center.",
            ),
            "ведьма": (
                "witch, sorceress",
                "Это старая ведьма.",
                "This is an old witch.",
            ),
            "колодец": (
                "well, pit",
                "Колодец во дворе.",
                "The well is in the yard.",
            ),
            "выгнать": (
                "expel, drive out",
                "Его выгнали из школы.",
                "They expelled him from school.",
            ),
            "географический": (
                "geographical, geographic",
                "Это географический вопрос.",
                "This is a geographical question.",
            ),
            "отстать": (
                "lag behind, fall behind",
                "Он отстал от группы.",
                "He lagged behind the group.",
            ),
            "анкета": (
                "questionnaire, form",
                "Это короткая анкета.",
                "This is a short questionnaire.",
            ),
            "условно": (
                "conditionally, hypothetically",
                "Это условно верно.",
                "This is conditionally true.",
            ),
            "марш": (
                "march",
                "Солдаты на марше.",
                "The soldiers are on a march.",
            ),
            "завершиться": (
                "to end, to conclude",
                "Встреча скоро завершится.",
                "The meeting will end soon.",
            ),
            "рвать": (
                "to tear, to rip",
                "Не надо рвать письмо.",
                "Do not tear the letter.",
            ),
            "обслуживать": (
                "to serve, to maintain",
                "Они обслуживают гостей.",
                "They serve the guests.",
            ),
        },
    )
)

dest = PACK / "_chunks" / "fixed" / "deck_15260200_04.csv"
cards = cards_from_path(dest)
leftover = []
for i, card in enumerate(cards, 1):
    lemma = lemma_from_card(card)
    gloss = answer_lemma_from_card(card)
    payload = card_write_payload(card)
    ru = payload["question"].split("## Footnote")[-1].strip()
    en = payload["answer"].split("## Footnote")[-1].strip()
    ru_l = ru.replace("ё", "е").lower()
    stem = lemma.replace("ё", "е").lower()[:4]
    if stem and stem not in ru_l and lemma.replace("ё", "е").lower() not in ru_l:
        leftover.append(f"{i} LEMMA {lemma} :: {ru}")
    gloss_l = re.sub(r"^(to |the |a |an )", "", gloss.split(",")[0].strip().lower())
    gloss_tok = gloss_l.split()[0] if gloss_l else ""
    if gloss_tok and gloss_tok not in en.lower() and not any(
        g in en.lower() for g in gloss_l.split()
    ):
        leftover.append(f"{i} GLOSS {gloss} :: {en}")
    extra_en = set()
    extra_ru = {lemma.replace("ё", "е").lower()}
    for part in re.split(r"[,;/]| or | and ", gloss):
        part = re.sub(r"^(to |the |a |an )", "", part.strip().lower())
        extra_en.update(part.split())
    allow_en.update(extra_en)
    allow_ru.update(extra_ru)
    for tok in _tokens(en):
        if not _en_ok(tok):
            leftover.append(f"{i} EN {tok} :: {en}")
    for tok in _tokens(ru):
        if not _ru_ok(tok):
            leftover.append(f"{i} RU {tok} :: {ru}")

print(f"leftovers={len(leftover)}")
if leftover:
    print("\n".join(leftover))
