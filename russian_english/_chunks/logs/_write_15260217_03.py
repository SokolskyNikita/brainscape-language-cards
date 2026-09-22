import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from brainscape import answer_lemma_from_card, cards_from_path, lemma_from_card
from brainscape.cards import card_write_payload
from russian_english._chunk_io import rewrite_chunk

print(
    rewrite_chunk(
        Path("russian_english/_chunks/deck_15260217_03.csv"),
        {
            "журнальный": ("magazine, journal", "Журнальный стол.", "A magazine table."),
            "геометрия": ("geometry", "Геометрия сложная.", "Geometry is hard."),
            "малышка": ("little girl, baby girl", "Малышка спит.", "The little girl is sleeping."),
            "повлечь": ("lead to, entail", "Это повлечёт беду.", "This will lead to trouble."),
            "гнусный": ("disgusting, vile", "Гнусный запах.", "A disgusting smell."),
            "загородный": ("country, suburban", "Загородный дом.", "A country house."),
            "риторика": ("rhetoric, oratory", "Его риторика слабая.", "His rhetoric is weak."),
            "декоративный": ("decorative, ornamental", "Декоративный сад.", "A decorative garden."),
            "взаимопонимание": ("mutual understanding", "Нет взаимопонимания.", "There is no mutual understanding."),
            "поклясться": ("to swear, to vow", "Я поклянусь.", "I will swear."),
            "легальный": ("legal, legitimate", "Это легальный путь.", "This is a legal path."),
            "пограничник": ("border guard, frontier guard", "Пограничник нас остановил.", "The border guard stopped us."),
            "потечь": ("to leak, to flow", "Труба потекла.", "The pipe leaked."),
            "ломаться": ("to break down, to malfunction", "Машина ломается.", "The car is breaking down."),
            "обследовать": ("examine, inspect", "Врач обследовал меня.", "The doctor examined me."),
            "изначальный": ("initial, original", "Изначальный план.", "The initial plan."),
            "управляться": ("to cope, to be managed", "Как ты управляешься?", "How do you cope?"),
            "спасаться": ("to escape, to be saved", "Спасайся!", "Escape!"),
            "штора": ("curtain, drape", "Закрой штору.", "Close the curtain."),
            "выдумка": ("fiction, fabrication", "Это выдумка.", "This is fiction."),
            "цыган": ("Gypsy, Roma", "Цыган поёт.", "The Gypsy is singing."),
            "восклицать": ("exclaim, cry out", "Не восклицай.", "Don't exclaim."),
            "краевой": ("regional, territorial", "Краевой центр далеко.", "The regional center is far."),
            "подмигнуть": ("wink, blink", "Он мне подмигнул.", "He winked at me."),
            "монография": ("monograph", "Это его монография.", "This is his monograph."),
            "кусать": ("bite, nibble", "Не кусай меня.", "Don't bite me."),
            "абсурд": ("nonsense, absurd", "Это абсурд.", "This is nonsense."),
            "лихорадка": ("fever", "У неё лихорадка.", "She has a fever."),
            "пуститься": ("set off, embark", "Он пустился бежать.", "He set off running."),
            "вялый": ("listless, sluggish", "Он сегодня вялый.", "He is listless today."),
            "санитар": ("orderly", "Санитар пришёл.", "The orderly came."),
            "будни": ("weekdays, workdays", "В будни я работаю.", "I work on weekdays."),
            "ростовский": ("Rostov, Rostov-on-Don", "Ростовский поезд.", "The Rostov train."),
            "тамошний": ("local, there", "Тамошний народ другой.", "The local people are different."),
            "вежливость": ("politeness, courtesy", "Ему не хватает вежливости.", "He has no politeness."),
            "энергично": ("energetically, vigorously", "Он работает энергично.", "He works energetically."),
            "сопоставление": ("comparison, juxtaposition", "Это сопоставление.", "This is a comparison."),
            "задевать": ("to hurt, to offend", "Не задевай его.", "Don't hurt him."),
            "муза": ("muse, inspiration", "Где твоя муза?", "Where is your muse?"),
            "всплеск": ("splash, surge", "Всплеск воды.", "A splash of water."),
            "нарушитель": ("violator, infringer", "Нарушитель убежал.", "The violator ran away."),
            "лестничный": ("staircase, stairway", "Лестничный свет не горит.", "The staircase light is out."),
            "ходьба": ("walking, walk", "Люблю ходьбу.", "I love walking."),
            "прислониться": ("lean against, rest against", "Прислонись к стене.", "Lean against the wall."),
            "шерстяной": ("woolen, wooly", "Шерстяной свитер.", "A woolen sweater."),
            "таксист": ("taxi driver, cabbie", "Таксист ждёт.", "The taxi driver is waiting."),
            "осмысление": ("comprehension, understanding", "Нужно осмысление.", "Comprehension is needed."),
            "апельсин": ("orange", "Дай апельсин.", "Give me an orange."),
            "расклад": ("situation, layout", "Плохой расклад.", "A bad situation."),
            "спрыгнуть": ("to jump off, to leap off", "Спрыгни с крыши.", "Jump off the roof."),
            "присяжный": ("juror, sworn", "Присяжный молчит.", "The juror is silent."),
            "эксклюзивный": ("exclusive", "Это эксклюзивный клуб.", "This is an exclusive club."),
            "одиноко": ("lonely, alone", "Мне одиноко.", "I feel lonely."),
            "покачиваться": ("sway, rock", "Лодка покачивается.", "The boat is swaying."),
            "таить": ("conceal, hide", "Он таит это.", "He conceals this."),
            "применимый": ("applicable, relevant", "Это не применимо.", "This is not applicable."),
            "сжигать": ("burn, incinerate", "Не сжигай письма.", "Don't burn the letters."),
            "выдавить": ("squeeze out, extrude", "Выдави сок.", "Squeeze out the juice."),
            "раздать": ("to hand out, to distribute", "Раздай карты.", "Hand out the cards."),
            "беспроводный": ("wireless, cordless", "Беспроводный телефон.", "A wireless phone."),
            "ребятишки": ("kids, little children", "Ребятишки во дворе.", "The kids are in the yard."),
            "метрополитен": ("subway, metro", "Где метрополитен?", "Where is the subway?"),
            "вериться": ("to seem true, to be believed", "Не верится.", "It does not seem true."),
            "панорама": ("panorama, vista", "Какая панорама!", "What a panorama!"),
            "скромность": ("modesty, humility", "Ей не хватает скромности.", "She has no modesty."),
            "захлопнуть": ("to slam, to bang", "Захлопни дверь.", "Slam the door."),
            "венец": ("crown, wreath", "На ней венец.", "She has a crown on."),
            "ослабление": ("weakening, relaxation", "После ослабления.", "After the weakening."),
            "воспроизводство": ("reproduction", "Воспроизводство идёт.", "Reproduction is going on."),
            "задержание": ("arrest, detention", "После задержания.", "After the arrest."),
            "эссе": ("essay, composition", "Напиши эссе.", "Write an essay."),
            "концептуальный": ("conceptual", "Это концептуальный вопрос.", "This is a conceptual question."),
            "служанка": ("maid, servant", "Служанка ушла.", "The maid left."),
            "стимулирование": ("stimulation, encouragement", "Нужно стимулирование.", "Stimulation is needed."),
            "аспирант": ("graduate student, postgraduate", "Она аспирант.", "She is a graduate student."),
            "навеки": ("forever, for eternity", "Это навеки.", "This is forever."),
            "недолгий": ("short, brief", "Недолгий сон.", "A short sleep."),
            "правозащитный": ("human rights, rights-defending", "Правозащитный центр.", "A human rights center."),
            "парадигма": ("paradigm, model", "Новая парадигма.", "A new paradigm."),
            "регламент": ("regulation, rules", "Читай регламент.", "Read the regulation."),
            "соорудить": ("construct, build", "Мы соорудили стол.", "We constructed a table."),
            "приучить": ("to train, to accustom", "Приучи собаку.", "Train the dog."),
            "ведомый": ("led, guided", "Он ведомый.", "He is led."),
            "переполнить": ("overfill, overflow", "Не переполни чашку.", "Don't overfill the cup."),
            "внедрить": ("implement, introduce", "Внедри это.", "Implement this."),
            "свежесть": ("freshness, crispness", "Какая свежесть!", "What freshness!"),
            "будильник": ("alarm clock, alarm", "Будильник звонит.", "The alarm clock is ringing."),
            "липкий": ("sticky, tacky", "Стол липкий.", "The table is sticky."),
            "улучшиться": ("improve, get better", "Погода улучшится.", "The weather will improve."),
            "бухгалтерия": ("accounting, bookkeeping", "Она в бухгалтерии.", "She is in accounting."),
            "озвучить": ("to voice, to dub", "Озвучь это.", "Voice this."),
            "жизнедеятельность": ("vital activity, life activity", "Нормальная жизнедеятельность.", "Normal vital activity."),
            "пристать": ("to pester, to accost", "Он пристал ко мне.", "He pestered me."),
            "выписка": ("statement, extract", "Принеси выписку.", "Bring the statement."),
            "срыв": ("disruption, failure", "Это срыв.", "This is a disruption."),
            "иголка": ("needle, pin", "Где иголка?", "Where is the needle?"),
            "музейный": ("museum, museum-related", "Музейный зал.", "A museum hall."),
            "призрачный": ("ghostly, spectral", "Призрачный свет.", "A ghostly light."),
            "ребёнок": ("child, kid", "Ребёнок спит.", "The child is sleeping."),
            "ливень": ("downpour, heavy rain", "Начался ливень.", "A downpour started."),
        },
    )
)

FUNCTION_EN = {
    "a", "an", "the", "to", "of", "in", "on", "at", "for", "from", "with", "by",
    "and", "or", "but", "not", "no", "yes", "is", "are", "was", "were", "be",
    "am", "been", "being", "do", "does", "did", "will", "would", "can", "could",
    "has", "have", "had", "i", "you", "he", "she", "it", "we", "they", "me",
    "him", "her", "us", "them", "my", "your", "his", "its", "our", "their",
    "this", "that", "these", "those", "there", "here", "what", "where", "when",
    "how", "who", "why", "don't", "doesn't", "isn't", "aren't", "wasn't",
    "weren't", "won't", "can't", "i'm", "he's", "she's", "it's", "we're",
    "they're", "that's", "there's", "where's", "out", "up", "down", "off",
    "into", "about", "after", "before", "again", "already", "also", "just",
    "only", "very", "so", "too", "then", "than", "as", "if", "because",
}
FUNCTION_RU = {
    "я", "ты", "он", "она", "оно", "мы", "вы", "они", "меня", "тебя", "его",
    "её", "ее", "нас", "вас", "их", "мне", "тебе", "ему", "ей", "нам", "вам",
    "им", "мной", "тобой", "им", "ею", "нами", "вами", "ими", "мой", "моя",
    "мое", "моё", "мои", "твой", "твоя", "твое", "твоё", "твои", "наш", "наш",
    "это", "этот", "эта", "эти", "тот", "та", "те", "не", "ни", "да", "нет",
    "и", "а", "но", "или", "ли", "же", "бы", "б", "уж", "ка", "то", "себе",
    "свой", "своя", "свое", "своё", "свои", "свою", "своей", "своего",
    "в", "во", "на", "с", "со", "к", "ко", "у", "о", "об", "от", "до",
    "из", "за", "по", "под", "над", "при", "для", "без", "между", "через",
    "был", "была", "было", "были", "будет", "будут", "буду", "есть", "быть",
    "уже", "еще", "ещё", "также", "тоже", "только", "вот", "ведь", "ну", "все",
    "как", "что", "чтобы", "когда", "если", "где", "чем", "кто", "тут",
    "там", "здесь", "давай", "нем", "нём", "ней", "них", "нее", "неё",
}

allow_en = {
    line.strip().lower()
    for line in (REPO / "russian_english/_vocab/allow_en_15260217.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_ru = {
    line.strip().replace("ё", "е").lower()
    for line in (REPO / "russian_english/_vocab/allow_ru_15260217.txt").read_text(encoding="utf-8").splitlines()
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
    "swore": "swear", "sung": "sing", "sang": "sing", "stopped": "stop",
    "sleeping": "sleep", "singing": "sing", "running": "run", "waiting": "wait",
    "breaking": "break", "ringing": "ring", "swaying": "sway", "winked": "wink",
    "leaked": "leak", "examined": "examine", "pestered": "pester",
    "started": "start", "constructed": "construct", "needed": "need",
    "children": "child", "letters": "letter", "cards": "card",
}
IRREGULAR_RU = {
    "идет": "идти", "иду": "идти", "шел": "идти", "шла": "идти", "шли": "идти",
    "поет": "петь", "поёт": "петь", "ждет": "ждать", "ждёт": "ждать",
    "пришел": "прийти", "пришёл": "прийти", "ушла": "уйти",
    "закрый": "закрыть", "дай": "дать", "люблю": "любить",
    "работает": "работать", "работаю": "работать",
    "спит": "спать", "молчит": "молчать", "горит": "гореть",
    "звони": "звонить", "звонит": "звонить", "читай": "читать",
    "напиши": "написать", "принеси": "принести",
    "начался": "начаться", "началась": "начаться",
    "хватит": "хватать", "хватает": "хватать",
    "убежал": "убежать", "остановил": "остановить",
    "повлечет": "повлечь", "поклянусь": "поклясться",
    "потекла": "потечь", "ломается": "ломаться",
    "обследовал": "обследовать", "управляешься": "управляться",
    "спасайся": "спасаться", "восклицай": "восклицать",
    "подмигнул": "подмигнуть", "кусай": "кусать",
    "пустился": "пуститься", "задевай": "задевать",
    "прислонись": "прислониться", "таит": "таить",
    "сжигай": "сжигать", "раздай": "раздать",
    "верится": "вериться", "соорудили": "соорудить",
    "улучшится": "улучшиться", "беду": "беда",
    "воды": "вода", "новая": "новый",
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
    for suf in ("'s", "s", "es", "ed", "ing", "ly", "er", "est"):
        if w.endswith(suf) and w[: -len(suf)] in allow_en:
            return True
        if w.endswith(suf) and w[: -len(suf)] + "e" in allow_en:
            return True
    if w.endswith("ies") and (w[:-3] + "y") in allow_en:
        return True
    if w.endswith("ied") and (w[:-3] + "y") in allow_en:
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


dest = REPO / "russian_english/_chunks/fixed/deck_15260217_03.csv"
cards = cards_from_path(dest)
leftover = []
for i, card in enumerate(cards, 1):
    lemma = lemma_from_card(card)
    gloss = answer_lemma_from_card(card)
    payload = card_write_payload(card)
    ru = payload["question"].split("## Footnote")[-1].strip()
    en = payload["answer"].split("## Footnote")[-1].strip()
    ru_l = ru.replace("ё", "е").lower()
    if lemma.replace("ё", "е").lower() not in ru_l and lemma.replace("ё", "е").lower()[:4] not in ru_l:
        leftover.append(f"{i} LEMMA {lemma} :: {ru}")
    gloss_l = re.sub(r"^(to |the |a |an )", "", gloss.split(",")[0].strip().lower())
    if gloss_l and gloss_l.split()[0] not in en.lower() and not any(g in en.lower() for g in gloss_l.split()):
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
