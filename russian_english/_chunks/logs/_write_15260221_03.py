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
    "there", "here", "very", "too", "now", "today", "yesterday", "tomorrow",
    "some", "any", "all", "no", "yes", "do", "does", "did", "have", "has",
    "had", "will", "would", "can", "could", "should", "must", "may", "might",
    "please", "more", "most", "less", "much", "many", "few", "such", "also",
    "only", "even", "still", "already", "always", "never", "often", "once",
    "after", "before", "under", "over", "through", "between", "without",
    "who", "what", "when", "where", "why", "how", "which",
    "ago", "ones", "two", "down", "up", "out", "off", "back",
    "herself", "himself", "themselves", "myself", "yourself",
    "one", "onto", "dont", "doesnt", "lets", "own", "well", "yet",
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
    "своё", "свое",
}

allow_en = {
    line.strip().lower()
    for line in (PACK / "_vocab" / "allow_en_15260221.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_ru = {
    line.strip().replace("ё", "е").lower()
    for line in (PACK / "_vocab" / "allow_ru_15260221.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_en |= FUNCTION_EN
allow_ru |= FUNCTION_RU

IRREGULAR_EN = {
    "came": "come", "gave": "give", "took": "take", "went": "go", "got": "get",
    "saw": "see", "was": "be", "were": "be", "been": "be", "had": "have",
    "did": "do", "said": "say", "made": "make", "left": "leave", "felt": "feel",
    "began": "begin", "became": "become", "bought": "buy", "caught": "catch",
    "kept": "keep", "lost": "lose", "fell": "fall", "grew": "grow", "held": "hold",
    "knew": "know", "ran": "run", "sat": "sit", "stood": "stand", "told": "tell",
    "thought": "think", "wrote": "write", "spoke": "speak", "broke": "break",
    "chose": "choose", "drove": "drive", "ate": "eat", "flew": "fly",
    "works": "work", "worked": "work", "working": "work",
    "shows": "show", "showed": "show",
    "waits": "wait", "waited": "wait",
    "stands": "stand", "sits": "sit",
    "looks": "look", "looked": "look",
    "wants": "want", "wanted": "want",
    "needs": "need", "needed": "need",
    "opens": "open", "opened": "open",
    "puts": "put", "planted": "plant",
    "passed": "pass", "known": "know",
    "helped": "help", "laughed": "laugh",
    "hooked": "hook", "shifted": "shift",
    "scattered": "scatter", "smirked": "smirk",
    "devoured": "devour", "justified": "justify",
    "combined": "combine", "fried": "fry",
    "washed": "wash", "enjoyed": "enjoy",
    "landed": "land", "split": "split",
    "shot": "shoot", "asked": "ask",
    "wondered": "wonder", "sentenced": "sentence",
    "touched": "touch", "moved": "move",
    "does": "do", "has": "have",
}

IRREGULAR_RU = {
    "идет": "идти", "иду": "идти", "шел": "идти", "шла": "идти", "шли": "идти",
    "нужна": "нужный", "нужен": "нужный", "нужно": "нужный",
    "ждёт": "ждать", "ждет": "ждать", "ждут": "ждать",
    "смотрит": "смотреть", "молчит": "молчать",
    "любит": "любить", "хочет": "хотеть", "хочу": "хотеть",
    "вижу": "видеть", "видит": "видеть", "видишь": "видеть",
    "знаю": "знать", "живу": "жить", "живет": "жить", "живёт": "жить",
    "живётся": "житься", "живется": "житься", "жится": "житься",
    "стал": "стать", "стала": "стать", "стали": "стать",
    "взял": "взять", "взяла": "взять", "возьми": "взять",
    "стоит": "стоять", "стоят": "стоять",
    "сидит": "сидеть", "сидят": "сидеть",
    "говорит": "говорить", "сказал": "сказать",
    "дал": "дать", "дайте": "дать",
    "открыл": "открыть", "открой": "открыть",
    "надень": "надеть", "надел": "надеть",
    "выбрось": "выбросить", "выбросил": "выбросить",
    "принял": "принять", "приняла": "принять",
    "пошли": "пойти", "пошёл": "пойти", "пошел": "пойти",
    "смог": "смочь", "смогла": "смочь",
    "помогла": "помочь", "помог": "помочь",
    "решили": "решить", "решил": "решить",
    "ушло": "уйти", "ушёл": "уйти", "ушел": "уйти",
    "сожрал": "сожрать", "сожрала": "сожрать",
    "сработал": "сработать", "срабатывает": "срабатывать",
    "жарю": "жарить", "жарит": "жарить",
    "совмести": "совместить",
    "помой": "помыть",
    "насладись": "насладиться",
    "преподнеси": "преподнести",
    "противопоставь": "противопоставить",
    "разделимся": "разделиться", "разделилась": "разделиться",
    "влюбляется": "влюбляться",
    "совершенствоваться": "совершенствоваться",
    "сдвинулся": "сдвинуться", "сдвинулась": "сдвинуться",
    "разбежалась": "разбежаться",
    "ухмыльнулся": "ухмыльнуться",
    "зацепил": "зацепить", "зацепило": "зацепить",
    "высадили": "высадить",
    "расстреливают": "расстреливать",
    "приговаривать": "приговаривать",
    "спрашивается": "спрашиваться",
    "оправдаться": "оправдаться",
}

RU_ENDINGS = (
    "ами", "ями", "ого", "его", "ому", "ему", "ыми", "ими", "ой", "ей", "ом",
    "ем", "ах", "ях", "ам", "ям", "ов", "ев", "ую", "юю", "ая", "яя", "ое",
    "ее", "ые", "ие", "ый", "ий", "а", "я", "у", "ю", "е", "и", "ы", "о", "ь",
)


def _en_ok(word: str) -> bool:
    w = word.lower()
    if w in allow_en:
        return True
    if IRREGULAR_EN.get(w) in allow_en:
        return True
    if w.endswith("'s") and w[:-2] in allow_en:
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
        if any(a.startswith(stem) or stem.startswith(a) for a in allow_ru if len(a) >= 4 and len(stem) >= 4):
            return True
    return False


def _tokens(text: str) -> list[str]:
    return re.findall(r"[A-Za-zА-Яа-яЁё'-]+", text)


FIXES = {
    "смирение": ("humility, submission", "У неё есть смирение.", "She has humility."),
    "свита": ("suite, retinue", "Свита короля уже здесь.", "The king's suite is already here."),
    "корка": ("crust, rind", "Это корка хлеба.", "This is a bread crust."),
    "эрекция": ("erection", "У него эрекция.", "He has an erection."),
    "спецназ": ("special forces, Spetsnaz", "Спецназ уже здесь.", "The special forces are here."),
    "совместить": ("combine, align", "Совмести работу и отдых.", "Combine work and rest."),
    "сожрать": ("to devour, to gobble up", "Он всё сожрал.", "He devoured everything."),
    "жарить": ("fry, roast", "Я буду жарить мясо.", "I will fry the meat."),
    "обоснованный": ("justified, well-founded", "Это обоснованный ответ.", "This is a justified answer."),
    "спасательный": ("rescue, lifesaving", "Это спасательный круг.", "This is a rescue ring."),
    "розетка": ("socket, outlet", "Где розетка?", "Where is the socket?"),
    "эдакий": ("sort of, kind of", "Он эдакий странный тип.", "He is a sort of strange type."),
    "благородство": ("nobility, nobleness", "Это настоящее благородство.", "This is true nobility."),
    "неуловимый": ("elusive, evasive", "Он неуловимый.", "He is elusive."),
    "иранский": ("Iranian, Persian", "Это иранский город.", "This is an Iranian city."),
    "состоятельный": ("wealthy, affluent", "Он состоятельный человек.", "He is a wealthy man."),
    "буфер": ("buffer, bumper", "Нам нужен буфер.", "We need a buffer."),
    "хлам": ("junk, clutter", "Выбрось этот хлам.", "Throw out this junk."),
    "срабатывать": ("to work, to trigger", "Это не срабатывает.", "This does not work."),
    "трата": ("waste, expenditure", "Это пустая трата.", "This is a waste."),
    "совершенствоваться": ("improve, perfect oneself", "Он хочет совершенствоваться.", "He wants to improve."),
    "консул": ("consul", "Консул ждёт нас.", "The consul waits for us."),
    "упрямо": ("stubbornly, obstinately", "Он упрямо стоит.", "He stubbornly stands."),
    "деликатный": ("delicate, sensitive", "Это деликатный вопрос.", "This is a delicate question."),
    "иракский": ("Iraqi", "Это иракский город.", "This is an Iraqi city."),
    "четыреста": ("four hundred", "Здесь четыреста человек.", "There are four hundred people here."),
    "преподобный": ("Reverend, Venerable", "Преподобный говорит с нами.", "The Reverend speaks with us."),
    "гусеница": ("caterpillar, track", "Видишь гусеницу?", "Do you see the caterpillar?"),
    "усовершенствование": ("improvement, enhancement", "Это усовершенствование системы.", "This is an improvement of the system."),
    "узник": ("prisoner, captive", "Узник сидит здесь.", "The prisoner sits here."),
    "катастрофический": ("catastrophic, disastrous", "Это катастрофический удар.", "This is a catastrophic blow."),
    "клин": ("wedge, blade", "Держи клин.", "Hold the wedge."),
    "авторитарный": ("authoritarian, autocratic", "Это авторитарный режим.", "This is an authoritarian regime."),
    "беглый": ("fugitive, fleeting", "Он беглый.", "He is a fugitive."),
    "сослуживец": ("colleague, coworker", "Мой сослуживец здесь.", "My colleague is here."),
    "сербский": ("Serbian", "Это сербский язык.", "This is the Serbian language."),
    "выкуп": ("ransom, redemption", "Они ждут выкуп.", "They wait for the ransom."),
    "цитирование": ("quotation, citation", "Это точное цитирование.", "This is an exact quotation."),
    "норматив": ("standard, regulation", "Это наш норматив.", "This is our standard."),
    "розыгрыш": ("prank, draw", "Это был розыгрыш.", "It was a prank."),
    "преподнести": ("present, offer", "Преподнеси ей цветок.", "Present a flower to her."),
    "развязка": ("denouement, interchange", "Это развязка истории.", "This is the denouement of the story."),
    "воззрение": ("viewpoint, outlook", "У него своё воззрение.", "He has his own viewpoint."),
    "помыть": ("to wash, to clean", "Нужно помыть стол.", "I need to wash the table."),
    "мобилизовать": ("mobilize, call up", "Нужно мобилизовать народ.", "We need to mobilize the people."),
    "нацистский": ("Nazi, fascist", "Это нацистский знак.", "This is a Nazi sign."),
    "житься": ("to get along, to live", "Мне здесь хорошо живётся.", "I get along well here."),
    "пластик": ("plastic", "Это пластик.", "This is plastic."),
    "колода": ("deck, pack", "Колода на столе.", "The deck is on the table."),
    "хлебный": ("bread", "Это хлебный магазин.", "This is a bread shop."),
    "влюбляться": ("to fall in love", "Он быстро влюбляется.", "He falls in love quickly."),
    "институциональный": ("institutional", "Это институциональный вопрос.", "This is an institutional question."),
    "выставочный": ("exhibition, exhibit", "Это выставочный зал.", "This is an exhibition hall."),
    "насладиться": ("enjoy, savor", "Насладись вечером.", "Enjoy the evening."),
    "совместимый": ("compatible", "Они совместимы.", "They are compatible."),
    "деятельный": ("active, energetic", "Он очень деятельный.", "He is very active."),
    "пыл": ("ardor, zeal", "У него есть пыл.", "He has ardor."),
    "высадить": ("to plant, to land", "Мы высадили дерево.", "We planted a tree."),
    "нарядный": ("dressy, smart", "Она сегодня нарядная.", "She is dressy today."),
    "тиран": ("tyrant, despot", "Он настоящий тиран.", "He is a real tyrant."),
    "сжатие": ("compression, squeezing", "Это сжатие файла.", "This is compression of the file."),
    "забвение": ("oblivion, forgetfulness", "Имя ушло в забвение.", "The name went into oblivion."),
    "развлекательный": ("entertainment, entertaining", "Это развлекательная игра.", "This is an entertainment game."),
    "красноармеец": ("Red Army soldier", "Красноармеец стоит у двери.", "A Red Army soldier stands at the door."),
    "утопия": ("utopia", "Это пустая утопия.", "This is an empty utopia."),
    "разделиться": ("to split, to divide", "Группа разделилась.", "The group split."),
    "женитьба": ("marriage", "Женитьба уже близко.", "The marriage is already near."),
    "мироздание": ("universe, creation", "Мироздание велико.", "The universe is great."),
    "капот": ("hood, bonnet", "Открой капот.", "Open the hood."),
    "комбинезон": ("jumpsuit, overall", "Надень комбинезон.", "Put on the jumpsuit."),
    "постулат": ("postulate, axiom", "Это основной постулат.", "This is the main postulate."),
    "противопоставить": ("to contrast, to set against", "Противопоставь одно другому.", "Contrast one with the other."),
    "археологический": ("archaeological", "Это археологический музей.", "This is an archaeological museum."),
    "директива": ("directive", "Вот директива.", "Here is the directive."),
    "спрашиваться": ("to wonder, to be asked", "Спрашивается, кто это.", "One wonders who this is."),
    "динамичный": ("dynamic, energetic", "Это динамичный танец.", "This is a dynamic dance."),
    "настойчивость": ("persistence, perseverance", "Его настойчивость помогла.", "His persistence helped."),
    "презрительно": ("contemptuously, scornfully", "Он презрительно смотрит.", "He looks contemptuously."),
    "приговаривать": ("to sentence", "Суд будет приговаривать его.", "The court will sentence him."),
    "расправа": ("reprisal, massacre", "Это была расправа.", "This was a reprisal."),
    "поручик": ("lieutenant", "Поручик ждёт приказа.", "The lieutenant waits for the order."),
    "круговой": ("circular, round", "Это круговой путь.", "This is a circular path."),
    "начинание": ("initiative, undertaking", "Это новое начинание.", "This is a new initiative."),
    "свекровь": ("mother-in-law", "Моя свекровь дома.", "My mother-in-law is at home."),
    "потрогать": ("to touch, to feel", "Можно потрогать это?", "Can I touch this?"),
    "конвейер": ("conveyor, assembly line", "Конвейер не работает.", "The conveyor does not work."),
    "строгость": ("strictness, severity", "Его строгость известна.", "His strictness is known."),
    "настрой": ("mood, spirit", "У неё хороший настрой.", "She has a good mood."),
    "безымянный": ("nameless, anonymous", "Это безымянный герой.", "This is a nameless hero."),
    "вглубь": ("into the depth, inward", "Мы пошли вглубь леса.", "We went into the depth of the forest."),
    "оправдаться": ("justify, vindicate", "Он не смог оправдаться.", "He could not justify himself."),
    "прокладка": ("gasket, pad", "Вот старая прокладка.", "Here is the old gasket."),
    "сдвинуться": ("to shift, to move", "Он не сдвинулся.", "He did not shift."),
    "заготовка": ("stock, blank", "Это зимняя заготовка.", "This is winter stock."),
    "расстреливать": ("to shoot, to execute by shooting", "Их будут расстреливать.", "They will shoot them."),
    "опорный": ("supporting, bearing", "Это опорная стена.", "This is a supporting wall."),
    "разбежаться": ("scatter, disperse", "Толпа разбежалась.", "The crowd scattered."),
    "светильник": ("lamp", "Светильник на столе.", "The lamp is on the table."),
    "зацепить": ("hook, catch", "Он зацепил меня.", "He hooked me."),
    "ухмыльнуться": ("smirk, grin", "Он ухмыльнулся.", "He smirked."),
}

print(
    rewrite_chunk(
        Path("russian_english/_chunks/deck_15260221_03.csv"),
        FIXES,
    )
)

dest = PACK / "_chunks" / "fixed" / "deck_15260221_03.csv"
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
    lemma_ok = bool(stem and stem in ru_l) or lemma.replace("ё", "е").lower() in ru_l
    if not lemma_ok:
        for tok in _tokens(ru):
            mapped = IRREGULAR_RU.get(tok.replace("ё", "е").lower())
            if mapped == lemma.replace("ё", "е").lower():
                lemma_ok = True
                break
    if not lemma_ok:
        leftover.append(f"{i} LEMMA {lemma} :: {ru}")
    gloss_l = re.sub(r"^(to |the |a |an )", "", gloss.split(",")[0].strip().lower())
    gloss_tok = gloss_l.split()[0] if gloss_l else ""
    if gloss_tok and gloss_tok not in en.lower() and not any(g in en.lower() for g in gloss_l.split()):
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
