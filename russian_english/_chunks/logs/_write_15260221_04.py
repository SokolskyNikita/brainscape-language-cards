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
    "puts": "put",
    "shot": "shoot", "asked": "ask",
    "does": "do", "has": "have",
    "flowed": "flow", "sleeps": "sleep",
    "carries": "carry", "hears": "hear",
    "reads": "read", "turns": "turn",
    "protects": "protect", "leans": "lean",
    "refutes": "refute", "explodes": "explode",
    "studies": "study", "growing": "grow",
    "changing": "change", "provided": "provide",
    "scared": "scare", "pounced": "pounce",
    "spent": "spend",
}

IRREGULAR_RU = {
    "идет": "идти", "иду": "идти", "шел": "идти", "шла": "идти", "шли": "идти",
    "идёт": "идти",
    "нужна": "нужный", "нужен": "нужный", "нужно": "нужный",
    "смотрит": "смотреть", "смотри": "смотреть",
    "любит": "любить", "хочет": "хотеть", "хочу": "хотеть",
    "вижу": "видеть", "видит": "видеть", "видишь": "видеть", "видел": "видеть",
    "знаю": "знать", "живу": "жить", "живет": "жить", "живёт": "жить",
    "стал": "стать", "стала": "стать", "стали": "стать",
    "взял": "взять", "взяла": "взять", "возьми": "взять",
    "стоит": "стоять", "стоят": "стоять",
    "сидит": "сидеть", "сидят": "сидеть",
    "говорит": "говорить", "сказал": "сказать",
    "дал": "дать", "дайте": "дать",
    "надень": "надеть", "надел": "надеть",
    "решили": "решить", "решил": "решить",
    "спит": "спать",
    "слышит": "слышать", "слышишь": "слышать",
    "просит": "просить",
    "растет": "расти", "растёт": "расти",
    "меняется": "меняться",
    "изучает": "изучать",
    "учится": "учиться",
    "проверяем": "проверять",
    "зажги": "зажечь",
    "окинь": "окинуть", "окинула": "окинуть",
    "зовут": "звать",
    "упал": "упасть", "упала": "упасть",
    "испугался": "испугаться", "испугалась": "испугаться",
    "читает": "читать",
    "текла": "течь", "тек": "течь",
    "несет": "нести", "несёт": "нести",
    "покрылся": "покрыться", "покрылась": "покрыться", "покрылось": "покрыться",
    "распался": "распасться", "распалась": "распасться",
    "набросился": "наброситься", "набросилась": "наброситься",
    "съедем": "съехать", "съеду": "съехать",
    "врываются": "врываться", "врывается": "врываться",
    "взрываются": "взрываться", "взрывается": "взрываться",
    "отворачивается": "отворачиваться",
    "подставляй": "подставлять", "подставляет": "подставлять",
    "продвигают": "продвигать", "продвигает": "продвигать",
    "исповедуют": "исповедовать", "исповедует": "исповедовать",
    "трактуешь": "трактовать", "трактует": "трактовать",
    "наклоняется": "наклоняться",
    "предусматривается": "предусматриваться",
    "опровергает": "опровергать",
    "устраняем": "устранять", "устраняют": "устранять",
    "подбили": "подбить", "подбил": "подбить",
    "загоняют": "загонять", "загоняй": "загонять",
    "оберегает": "оберегать",
    "промелькнула": "промелькнуть", "промелькнул": "промелькнуть",
    "причастен": "причастный",
    "похлопай": "похлопать", "похлопаем": "похлопать",
    "эксплуатируют": "эксплуатировать",
    "затратили": "затратить", "затратил": "затратить",
    "понизь": "понизить",
    "порекомендую": "порекомендовать",
    "поболтаем": "поболтать",
    "хватит": "хватать",
    "может": "мочь",
    "распадется": "распасться", "распадётся": "распасться",
    "иди": "идти",
    "игре": "игра", "игры": "игра",
    "цену": "цена", "цены": "цена",
    "веру": "вера",
    "силы": "сила", "силу": "сила",
    "раны": "рана", "рану": "рана",
    "воды": "вода", "воду": "вода",
    "манипулируют": "манипулировать", "манипулирует": "манипулировать",
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
    "триумф": ("triumph, victory", "Это был настоящий триумф.", "It was a true triumph."),
    "рента": ("rent, annuity", "Он живёт на ренту.", "He lives on rent."),
    "спереди": ("in front, ahead", "Она стоит спереди.", "She stands in front."),
    "покрыться": ("to get covered, to be covered", "Стол покрылся пылью.", "The table will get covered in dust."),
    "обладание": ("possession, ownership", "Это обладание властью.", "This is possession of power."),
    "мышечный": ("muscular, muscle", "У него мышечная боль.", "He has a muscular pain."),
    "бурно": ("turbulently, stormily", "Река текла бурно.", "The river flowed turbulently."),
    "идол": ("idol, icon", "Она стала идолом.", "She became an idol."),
    "дистрибьютор": ("distributor, dealer", "Дистрибьютор уже здесь.", "The distributor is already here."),
    "распасться": ("fall apart, disintegrate", "Союз скоро распадётся.", "The union will fall apart."),
    "добродушный": ("good-natured, kind-hearted", "Он добродушный человек.", "He is a good-natured man."),
    "вверху": ("upstairs, at the top", "Кот спит вверху.", "The cat sleeps upstairs."),
    "сенсация": ("sensation", "Книга стала сенсацией.", "The book became a sensation."),
    "бах": ("bang, boom", "Слышишь этот бах?", "Do you hear that bang?"),
    "эксплуатировать": ("exploit, operate", "Они эксплуатируют народ.", "They exploit the people."),
    "гривна": ("hryvnia", "Это одна гривна.", "This is one hryvnia."),
    "брань": ("abuse, swearing", "Хватит этой брани.", "Enough of this abuse."),
    "размножение": ("reproduction, propagation", "Это размножение клетки.", "This is reproduction of a cell."),
    "затратить": ("spend, expend", "Мы затратили день.", "We had to spend a day."),
    "изобразительный": ("pictorial, visual", "Это изобразительное искусство.", "This is pictorial art."),
    "полосатый": ("striped, stripy", "Это полосатый кот.", "This is a striped cat."),
    "причастный": ("involved, participant", "Он причастен к этому.", "He is involved in this."),
    "наброситься": ("pounce, attack", "Кот набросился на мышь.", "The cat pounced on the mouse."),
    "химик": ("chemist", "Химик работает здесь.", "The chemist works here."),
    "ходатайство": ("petition, application", "Вот ходатайство.", "Here is the petition."),
    "палестинский": ("Palestinian", "Это палестинский флаг.", "This is a Palestinian flag."),
    "съехать": ("move out, slide off", "Мы съедем завтра.", "We will move out tomorrow."),
    "вхождение": ("entry, entrance", "Это вхождение в союз.", "This is entry into the union."),
    "ион": ("ion", "У иона есть заряд.", "An ion has a charge."),
    "трактовать": ("interpret, construe", "Как ты трактуешь это?", "How do you interpret this?"),
    "ель": ("spruce", "Ель стоит у дома.", "The spruce stands by the house."),
    "избежание": ("avoidance, evasion", "Это избежание войны.", "This is avoidance of war."),
    "врываться": ("to burst in, to break in", "Они врываются без стука.", "They burst in without a knock."),
    "колпак": ("cap, hood", "Надень колпак.", "Put on the cap."),
    "глюк": ("glitch, bug", "В игре есть глюк.", "There is a glitch in the game."),
    "жалобно": ("plaintively, mournfully", "Она жалобно смотрит.", "She looks plaintively."),
    "понизить": ("reduce, lower", "Нужно понизить цену.", "We need to reduce the price."),
    "исповедовать": ("profess, confess", "Они исповедуют эту веру.", "They profess this faith."),
    "наклоняться": ("to lean, to bend", "Она наклоняется вперёд.", "She leans forward."),
    "тапочки": ("slippers", "Где мои тапочки?", "Where are my slippers?"),
    "синтетический": ("synthetic, artificial", "Это синтетический материал.", "This is a synthetic material."),
    "продвигать": ("promote, advance", "Они продвигают этот товар.", "They promote this product."),
    "популяция": ("population", "Популяция растёт.", "The population is growing."),
    "клип": ("clip, music video", "Я видел новый клип.", "I saw a new clip."),
    "насмерть": ("to death, fatally", "Он испугался насмерть.", "He was scared to death."),
    "социум": ("society", "Социум меняется.", "Society is changing."),
    "астроном": ("astronomer", "Астроном смотрит на небо.", "The astronomer looks at the sky."),
    "оберегать": ("to protect, to guard", "Она оберегает дитя.", "She protects the child."),
    "загонять": ("drive in, herd", "Они загоняют скот в сарай.", "They drive the cattle into the barn."),
    "порекомендовать": ("recommend, suggest", "Я порекомендую эту книгу.", "I will recommend this book."),
    "промелькнуть": ("flash, flit", "Тень промелькнула.", "A shadow flashed."),
    "похлопать": ("to pat, to clap", "Похлопай собаку.", "Pat the dog."),
    "хождение": ("walking", "Это хождение по кругу.", "This is walking in a circle."),
    "безразличие": ("indifference, apathy", "Это полное безразличие.", "This is complete indifference."),
    "метель": ("blizzard, snowstorm", "На улице метель.", "There is a blizzard outside."),
    "аксиома": ("axiom, postulate", "Это просто аксиома.", "This is simply an axiom."),
    "выспаться": ("get enough sleep, sleep well", "Мне нужно выспаться.", "I need to get enough sleep."),
    "буддизм": ("Buddhism", "Он изучает буддизм.", "He studies Buddhism."),
    "спасительный": ("saving, rescuing", "Это спасительный шаг.", "This is a saving step."),
    "техникум": ("technical school, college", "Он учится в техникуме.", "He studies at a technical school."),
    "ввоз": ("import, entry", "Мы проверяем ввоз товара.", "We check the import of goods."),
    "продуктивный": ("productive, efficient", "Это был продуктивный день.", "It was a productive day."),
    "взрываться": ("explode, blow up", "Они часто взрываются.", "They often explode."),
    "дубовый": ("oak, oaken", "Это дубовый стол.", "This is an oak table."),
    "гостевой": ("guest", "Это гостевая комната.", "This is a guest room."),
    "подставлять": ("to set up, to frame", "Не подставляй меня.", "Do not set me up."),
    "датский": ("Danish", "Это датский язык.", "This is the Danish language."),
    "свечка": ("candle", "Зажги свечку.", "Light the candle."),
    "отворачиваться": ("to turn away, to avert", "Она отворачивается от меня.", "She turns away from me."),
    "носик": ("spout, little nose", "Носик чайника горячий.", "The kettle's spout is hot."),
    "норвежский": ("Norwegian", "Это норвежский язык.", "This is the Norwegian language."),
    "вахта": ("watch, duty shift", "Он стоит на вахте.", "He stands on watch."),
    "окинуть": ("to glance at, to sweep over", "Окинь взглядом комнату.", "Glance at the room."),
    "красочный": ("colorful, vivid", "Это красочный праздник.", "This is a colorful holiday."),
    "стишок": ("verse, little poem", "Она читает стишок.", "She reads a verse."),
    "феодальный": ("feudal", "Это феодальный строй.", "This is a feudal system."),
    "муниципалитет": ("municipality", "Муниципалитет дал ответ.", "The municipality gave an answer."),
    "колхозный": ("collective farm, kolkhoz", "Это колхозное поле.", "This is a collective farm field."),
    "прям": ("straight, directly", "Иди прям сюда.", "Come straight here."),
    "устранять": ("eliminate, remove", "Мы устраняем ошибки.", "We eliminate mistakes."),
    "подделка": ("forgery, counterfeit", "Это подделка.", "This is a forgery."),
    "нарком": ("People's Commissar, commissar", "Нарком дал приказ.", "The People's Commissar gave an order."),
    "толстяк": ("fat man, fatty", "Толстяк сидит там.", "The fat man sits there."),
    "манипулировать": ("manipulate", "Они манипулируют народом.", "They manipulate the people."),
    "хищный": ("predatory, carnivorous", "Это хищный зверь.", "This is a predatory beast."),
    "нечаянно": ("accidentally, unintentionally", "Он нечаянно упал.", "He accidentally fell."),
    "множественный": ("multiple, plural", "У него множественные раны.", "He has multiple wounds."),
    "краснодарский": ("Krasnodar", "Это краснодарский край.", "This is the Krasnodar region."),
    "кураж": ("high spirits, swagger", "У него сегодня кураж.", "He is in high spirits today."),
    "опровергать": ("refute, disprove", "Она опровергает слухи.", "She refutes the rumors."),
    "поклонение": ("worship, adoration", "Это поклонение идолу.", "This is worship of an idol."),
    "шествие": ("procession, march", "Шествие идёт по улице.", "The procession goes along the street."),
    "бишь": ("namely, that is", "Как бишь его зовут?", "What is his name, namely?"),
    "условность": ("convention, conventionality", "Это пустая условность.", "This is an empty convention."),
    "оскорбительный": ("offensive, insulting", "Это оскорбительный тон.", "This is an offensive tone."),
    "умирающий": ("dying", "Умирающий просит воды.", "The dying man asks for water."),
    "поболтать": ("chat, talk", "Давай поболтаем.", "Let's chat."),
    "астрономический": ("astronomical", "Цена астрономическая.", "The price is astronomical."),
    "предусматриваться": ("to be provided for, to be envisaged", "Это предусматривается законом.", "This is to be provided for by law."),
    "подбить": ("shoot down, sum up", "Мы подбили цель.", "We shot down the target."),
}

print(
    rewrite_chunk(
        Path("russian_english/_chunks/deck_15260221_04.csv"),
        FIXES,
    )
)

dest = PACK / "_chunks" / "fixed" / "deck_15260221_04.csv"
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
