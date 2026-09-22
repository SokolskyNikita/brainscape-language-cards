import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from brainscape import answer_lemma_from_card, card_write_payload, cards_from_path, lemma_from_card
from russian_english._chunk_io import rewrite_chunk

PACK = REPO / "russian_english"
SRC = PACK / "_chunks" / "deck_15260196_03.csv"

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
    "planned": "plan", "offered": "offer",
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
    "стал": "стать", "стала": "стать", "стали": "стать",
    "взял": "взять", "взяла": "взять",
    "стоит": "стоять", "стоят": "стоять",
    "болит": "болеть",
    "принес": "принести", "принеси": "принести",
    "прочти": "прочитать",
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
    "предлагаться": ("to be offered, to be proposed", "Это предлагается нам.", "This is offered to us."),
    "мыслить": ("think, reason", "Он мыслит быстро.", "He thinks fast."),
    "грузовик": ("truck, lorry", "Грузовик уже здесь.", "The truck is already here."),
    "полдень": ("noon, midday", "Приходи в полдень.", "Come at noon."),
    "свыше": ("above, over", "Свыше пяти человек.", "Over five people."),
    "уставиться": ("to stare, to gaze", "Он уставился на меня.", "He stared at me."),
    "стрельба": ("shooting, gunfire", "Слышишь стрельбу?", "Do you hear the shooting?"),
    "править": ("rule, govern", "Он правит страной.", "He rules the country."),
    "оформить": ("process, formalize", "Оформи заказ.", "Process the order."),
    "болото": ("swamp, marsh", "Мы у болота.", "We are by the swamp."),
    "контрольный": ("control, check", "Это контрольный вопрос.", "This is a control question."),
    "авария": ("accident, crash", "Там была авария.", "There was an accident."),
    "интеллект": ("intellect, intelligence", "У него сильный интеллект.", "He has a strong intellect."),
    "леди": ("lady, dame", "Эта леди здесь.", "This lady is here."),
    "захват": ("capture, seizure", "Это захват города.", "This is the capture of the city."),
    "послышаться": ("to be heard", "Послышался голос.", "A voice was heard."),
    "перечень": ("list, inventory", "Вот перечень.", "Here is the list."),
    "развернуться": ("unfold, deploy", "План развернулся.", "The plan unfolded."),
    "сохраняться": ("to be preserved, to remain", "Традиция сохраняется.", "The tradition is preserved."),
    "расходиться": ("to diverge, to differ", "Наши пути расходятся.", "Our paths diverge."),
    "инстинкт": ("instinct, intuition", "Это мой инстинкт.", "This is my instinct."),
    "обсуждаться": ("to be discussed, to be debated", "Тема обсуждается.", "The topic is discussed."),
    "дорожный": ("road, travel", "Это дорожный знак.", "This is a road sign."),
    "строчка": ("line, row", "Прочти эту строчку.", "Read this line."),
    "возглавлять": ("to lead, to head", "Он возглавляет команду.", "He leads the team."),
    "раса": ("race", "Это одна раса.", "This is one race."),
    "успокоить": ("calm, soothe", "Успокой её.", "Calm her."),
    "классный": ("cool, awesome", "Это классный фильм.", "This is a cool movie."),
    "побережье": ("coast, shoreline", "Мы на побережье.", "We are on the coast."),
    "отозваться": ("respond, echo", "Он не отозвался.", "He did not respond."),
    "крышка": ("lid, cover", "Где крышка?", "Where is the lid?"),
    "желудок": ("stomach, belly", "У меня болит желудок.", "My stomach hurts."),
    "ведро": ("bucket, pail", "Принеси ведро.", "Bring the bucket."),
    "тактика": ("tactic, strategy", "Это наша тактика.", "This is our tactic."),
    "нуль": ("zero, null", "Это нуль.", "This is zero."),
    "молния": ("lightning, zipper", "Я видел молнию.", "I saw lightning."),
    "стеклянный": ("glass, glassy", "Это стеклянный стол.", "This is a glass table."),
    "чеченский": ("Chechen", "Это чеченский язык.", "This is the Chechen language."),
    "японец": ("Japanese, Japanese person", "Он японец.", "He is Japanese."),
    "лавка": ("shop, bench", "Это старая лавка.", "This is an old shop."),
    "тезис": ("thesis, proposition", "Это главный тезис.", "This is the main thesis."),
    "разглядеть": ("make out, discern", "Я не разглядел знак.", "I did not make out the sign."),
    "вносить": ("to contribute, to introduce", "Вноси свои идеи.", "Contribute your ideas."),
    "плащ": ("raincoat, cloak", "Где мой плащ?", "Where is my raincoat?"),
    "оглянуться": ("to look back, to glance back", "Оглянись назад.", "Look back."),
    "значимый": ("significant, meaningful", "Это значимый день.", "This is a significant day."),
    "принадлежность": ("belonging, affiliation", "Это его принадлежность.", "This is his belonging."),
    "рухнуть": ("collapse, fall", "Дом рухнул.", "The house collapsed."),
    "возрастать": ("to increase, to grow", "Цены возрастают.", "Prices increase."),
    "важность": ("importance, significance", "Я знаю важность этого.", "I know the importance of this."),
    "суждение": ("judgment, opinion", "Это моё суждение.", "This is my judgment."),
    "заболеть": ("to fall ill, to get sick", "Она заболела вчера.", "She fell ill yesterday."),
    "компенсация": ("compensation, indemnity", "Где компенсация?", "Where is the compensation?"),
    "командующий": ("commander", "Командующий здесь.", "The commander is here."),
    "облегчение": ("relief, alleviation", "Какое облегчение!", "What a relief!"),
    "валяться": ("to lie around, to loaf", "Книги валяются тут.", "Books lie around here."),
    "поставщик": ("supplier, provider", "Это наш поставщик.", "This is our supplier."),
    "христианство": ("Christianity", "Это христианство.", "This is Christianity."),
    "уточнить": ("clarify, specify", "Уточни вопрос.", "Clarify the question."),
    "недовольный": ("dissatisfied, unhappy", "Он недовольный.", "He is dissatisfied."),
    "казак": ("Cossack", "Он казак.", "He is a Cossack."),
    "наблюдатель": ("observer, watcher", "Наблюдатель здесь.", "The observer is here."),
    "рукопись": ("manuscript", "Где рукопись?", "Where is the manuscript?"),
    "поглядеть": ("look, watch", "Погляди сюда.", "Look here."),
    "пользование": ("use, utilization", "Это для пользования.", "This is for use."),
    "меню": ("menu, card", "Где меню?", "Where is the menu?"),
    "смелый": ("brave, bold", "Он смелый.", "He is brave."),
    "удерживать": ("to hold, to retain", "Не удерживай меня.", "Do not hold me."),
    "таблетка": ("pill, tablet", "Прими таблетку.", "Take the pill."),
    "изготовление": ("manufacturing, production", "Нужно изготовление.", "We need manufacturing."),
    "принципиально": ("fundamentally", "Я принципиально против.", "I am fundamentally against."),
    "медаль": ("medal, medallion", "Вот медаль.", "Here is the medal."),
    "языковой": ("linguistic, language", "Это языковой вопрос.", "This is a language question."),
    "ведомство": ("department, agency", "Это наше ведомство.", "This is our department."),
    "беспокойство": ("anxiety, unrest", "У меня беспокойство.", "I have anxiety."),
    "педагогический": ("pedagogical, educational", "Это педагогический вопрос.", "This is a pedagogical question."),
    "моряк": ("sailor, seaman", "Он моряк.", "He is a sailor."),
    "оправдать": ("justify, vindicate", "Я не могу оправдать это.", "I cannot justify this."),
    "седой": ("gray-haired, hoary", "Он уже седой.", "He is already gray-haired."),
    "поэтический": ("poetic, poetical", "Это поэтический текст.", "This is a poetic text."),
    "одинаково": ("equally, the same", "Они одинаково важны.", "They are equally important."),
    "формировать": ("to form, to shape", "Мы формируем план.", "We form a plan."),
    "планироваться": ("to be planned, to be scheduled", "Встреча планируется.", "The meeting is planned."),
    "мощь": ("power, might", "Какая мощь!", "What power!"),
    "желательно": ("preferably", "Желательно завтра.", "Preferably tomorrow."),
    "приблизиться": ("approach, come closer", "Он приблизился ко мне.", "He approached me."),
    "придать": ("lend, impart", "Это придаст вес.", "This will lend weight."),
    "видимость": ("visibility, appearance", "Видимость плохая.", "Visibility is bad."),
    "акцент": ("accent, emphasis", "У неё акцент.", "She has an accent."),
    "замолчать": ("hush, fall silent", "Все замолчали.", "They all hushed."),
    "приблизительно": ("approximately, roughly", "Приблизительно десять.", "Approximately ten."),
    "ломать": ("break, damage", "Не ломай это.", "Do not break this."),
    "правительственный": ("governmental, government", "Это правительственный план.", "This is a governmental plan."),
    "торжественный": ("solemn, ceremonial", "Это торжественный день.", "This is a solemn day."),
    "предшествовать": ("to precede", "Он предшествует нам.", "He precedes us."),
    "дьявол": ("devil, demon", "Это не дьявол.", "This is not the devil."),
    "примечание": ("note, remark", "Читай примечание.", "Read the note."),
    "блеск": ("shine, gloss", "Какой блеск!", "What a shine!"),
    "пальто": ("coat, overcoat", "Где моё пальто?", "Where is my coat?"),
    "оптимальный": ("optimal, optimum", "Это оптимальный путь.", "This is the optimal way."),
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
