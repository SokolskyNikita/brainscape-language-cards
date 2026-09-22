import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from brainscape import (
    answer_lemma_from_card,
    card_write_payload,
    cards_from_path,
    lemma_from_card,
)
from russian_english._chunk_io import rewrite_chunk

print(
    rewrite_chunk(
        Path("russian_english/_chunks/deck_15260214_03.csv"),
        {
            "отвлечь": (
                "distract, divert",
                "Отвлеки его от работы.",
                "Distract him from work.",
            ),
            "ваза": (
                "vase, urn",
                "Ваза разбилась.",
                "The vase shattered.",
            ),
            "парадоксальный": (
                "paradoxical, contradictory",
                "Это парадоксальный ответ.",
                "This is a paradoxical answer.",
            ),
            "крещение": (
                "baptism, christening",
                "Крещение завтра.",
                "The baptism is tomorrow.",
            ),
            "жадный": (
                "greedy, avaricious",
                "Он слишком жадный.",
                "He is too greedy.",
            ),
            "милицейский": (
                "police, militia",
                "Милицейская машина тут.",
                "The police car is here.",
            ),
            "послевоенный": (
                "postwar, post-war",
                "Это послевоенный город.",
                "This is a postwar city.",
            ),
            "обморок": (
                "faint, swoon",
                "Это был обморок.",
                "That was a faint.",
            ),
            "хата": (
                "hut, cottage",
                "Это старая хата.",
                "This is an old hut.",
            ),
            "профессионализм": (
                "professionalism",
                "Его профессионализм виден.",
                "His professionalism is visible.",
            ),
            "испугать": (
                "to scare, to frighten",
                "Не испугай кота.",
                "Do not scare the cat.",
            ),
            "поддаться": (
                "yield, succumb",
                "Он не поддался.",
                "He did not yield.",
            ),
            "замирать": (
                "freeze, hold one's breath",
                "Он замирает тут.",
                "He freezes here.",
            ),
            "сбой": (
                "malfunction, failure",
                "Это снова сбой.",
                "This is a malfunction again.",
            ),
            "быстрота": (
                "speed, swiftness",
                "Его быстрота важна.",
                "His speed is important.",
            ),
            "прилагать": (
                "to apply, to exert",
                "Прилагай больше силы.",
                "Apply more force.",
            ),
            "недопустимый": (
                "inadmissible, unacceptable",
                "Это недопустимый шаг.",
                "This is an inadmissible step.",
            ),
            "выяснение": (
                "clarification, elucidation",
                "Нужно выяснение.",
                "Clarification is needed.",
            ),
            "купюра": (
                "banknote, bill",
                "Купюра на столе.",
                "The banknote is on the table.",
            ),
            "предписание": (
                "prescription, order",
                "Это строгое предписание.",
                "This is a strict prescription.",
            ),
            "полуостров": (
                "peninsula",
                "Полуостров далеко.",
                "The peninsula is far.",
            ),
            "крокодил": (
                "crocodile, alligator",
                "Крокодил в реке.",
                "The crocodile is in the river.",
            ),
            "ползать": (
                "crawl, creep",
                "Кот ползает тут.",
                "The cat crawls here.",
            ),
            "перец": (
                "pepper, bell pepper",
                "В супе есть перец.",
                "There is pepper in the soup.",
            ),
            "усилиться": (
                "intensify, strengthen",
                "Ветер усилится.",
                "The wind will intensify.",
            ),
            "будка": (
                "booth, kiosk",
                "Это старая будка.",
                "This is an old booth.",
            ),
            "подражать": (
                "imitate, emulate",
                "Не подражай ему.",
                "Do not imitate him.",
            ),
            "одновременный": (
                "simultaneous, concurrent",
                "Это одновременный удар.",
                "This is a simultaneous blow.",
            ),
            "печататься": (
                "to be printed, to be published",
                "Книга печатается.",
                "The book is being printed.",
            ),
            "хранилище": (
                "repository, storage",
                "Хранилище закрыто.",
                "The repository is closed.",
            ),
            "бедняга": (
                "poor thing, wretch",
                "Бедняга опять болеет.",
                "The poor thing is sick again.",
            ),
            "старание": (
                "diligence, effort",
                "Его старание видно.",
                "His diligence is visible.",
            ),
            "непривычный": (
                "unusual, unfamiliar",
                "Этот вкус непривычный.",
                "This taste is unusual.",
            ),
            "социолог": (
                "sociologist",
                "Она социолог.",
                "She is a sociologist.",
            ),
            "привлекательность": (
                "attractiveness, appeal",
                "Её привлекательность важна.",
                "Her attractiveness is important.",
            ),
            "надлежащий": (
                "proper, due",
                "Это надлежащий порядок.",
                "This is the proper order.",
            ),
            "произвольный": (
                "arbitrary, random",
                "Это произвольный выбор.",
                "This is an arbitrary choice.",
            ),
            "красавец": (
                "handsome man, beau",
                "Он настоящий красавец.",
                "He is a real handsome man.",
            ),
            "поспать": (
                "to sleep, to have a nap",
                "Мне надо поспать.",
                "I need to sleep.",
            ),
            "кормление": (
                "feeding, nourishment",
                "Кормление уже началось.",
                "The feeding already started.",
            ),
            "несправедливость": (
                "injustice, unfairness",
                "Какая несправедливость!",
                "What an injustice!",
            ),
            "контраст": (
                "contrast, stark difference",
                "Какой сильный контраст!",
                "What a strong contrast!",
            ),
            "нюанс": (
                "nuance, subtlety",
                "Я вижу нюанс.",
                "I see the nuance.",
            ),
            "трактовка": (
                "interpretation, rendition",
                "Это новая трактовка.",
                "This is a new interpretation.",
            ),
            "равнодушно": (
                "indifferently, apathetically",
                "Он равнодушно слушает.",
                "He listens indifferently.",
            ),
            "шахматный": (
                "chess, chess-related",
                "Это шахматный стол.",
                "This is a chess table.",
            ),
            "хищник": (
                "predator, carnivore",
                "Это опасный хищник.",
                "This is a dangerous predator.",
            ),
            "некрасивый": (
                "ugly, unattractive",
                "Этот дом некрасивый.",
                "This house is ugly.",
            ),
            "измерять": (
                "measure, gauge",
                "Измеряй стол.",
                "Measure the table.",
            ),
            "вылезть": (
                "to climb out, to emerge",
                "Вылезь отсюда.",
                "Climb out of here.",
            ),
            "пух": (
                "down, fluff",
                "В подушке пух.",
                "There is down in the pillow.",
            ),
            "шапочка": (
                "cap, bonnet",
                "Надень шапочку.",
                "Put on the cap.",
            ),
            "инсулин": (
                "insulin",
                "Ей нужен инсулин.",
                "She needs insulin.",
            ),
            "нечистый": (
                "unclean, impure",
                "Стол нечистый.",
                "The table is unclean.",
            ),
            "либерализм": (
                "liberalism",
                "Он говорит о либерализме.",
                "He talks about liberalism.",
            ),
            "подъезжать": (
                "to approach, to drive up",
                "Машина подъезжает.",
                "The car is approaching.",
            ),
            "очевидец": (
                "eyewitness, observer",
                "Он очевидец.",
                "He is an eyewitness.",
            ),
            "жареный": (
                "fried, roasted",
                "Жареная рыба вкусная.",
                "The fried fish is tasty.",
            ),
            "прерывать": (
                "interrupt, disrupt",
                "Не прерывай меня.",
                "Do not interrupt me.",
            ),
            "побуждать": (
                "encourage, prompt",
                "Это побуждает меня.",
                "This encourages me.",
            ),
            "удалять": (
                "remove, delete",
                "Удаляй этот файл.",
                "Remove this file.",
            ),
            "запеть": (
                "to sing, to start singing",
                "Она запела.",
                "She started to sing.",
            ),
            "коктейль": (
                "cocktail, mix",
                "Закажи коктейль.",
                "Order a cocktail.",
            ),
            "посметь": (
                "dare, venture",
                "Не посмей!",
                "Do not dare!",
            ),
            "парить": (
                "soar, steam",
                "Птица парит высоко.",
                "The bird soars high.",
            ),
            "вспыхивать": (
                "flare up, flash",
                "Огонь вспыхивает.",
                "The fire flares up.",
            ),
            "швырнуть": (
                "to throw, to fling",
                "Швырни мяч.",
                "Throw the ball.",
            ),
            "вовлечь": (
                "involve, engage",
                "Вовлеки его в работу.",
                "Involve him in the work.",
            ),
            "прикоснуться": (
                "to touch, to come into contact",
                "Прикоснись к столу.",
                "Touch the table.",
            ),
            "изобретатель": (
                "inventor",
                "Он известный изобретатель.",
                "He is a famous inventor.",
            ),
            "специализироваться": (
                "specialize, specialize in",
                "Он специализируется тут.",
                "He specializes here.",
            ),
            "скользкий": (
                "slippery, slick",
                "Дорога скользкая.",
                "The road is slippery.",
            ),
            "слюна": (
                "saliva, spit",
                "Слюна во рту.",
                "There is saliva in the mouth.",
            ),
            "вскрыть": (
                "open, reveal",
                "Вскрой коробку.",
                "Open the box.",
            ),
            "совпасть": (
                "coincide, match",
                "Время совпало.",
                "The time coincided.",
            ),
            "хорошенький": (
                "pretty, cute",
                "Какой хорошенький кот!",
                "What a pretty cat!",
            ),
            "лак": (
                "varnish, lacquer",
                "Нанеси лак.",
                "Apply the varnish.",
            ),
            "помчаться": (
                "to rush, to dash",
                "Он помчался домой.",
                "He rushed home.",
            ),
            "действо": (
                "action, act",
                "Действо уже началось.",
                "The action already started.",
            ),
            "эмигрант": (
                "emigrant",
                "Эмигрант скучает по дому.",
                "The emigrant misses home.",
            ),
            "напарник": (
                "partner, teammate",
                "Мой напарник уже тут.",
                "My partner is already here.",
            ),
            "демографический": (
                "demographic, demographical",
                "Это демографический рост.",
                "This is demographic growth.",
            ),
            "монтаж": (
                "installation, montage",
                "Монтаж уже готов.",
                "The installation is already ready.",
            ),
            "отодвинуть": (
                "to move back, to push away",
                "Отодвинь стул.",
                "Move back the chair.",
            ),
            "пешеход": (
                "pedestrian, walker",
                "Пешеход уже тут.",
                "The pedestrian is already here.",
            ),
            "единичный": (
                "single, individual",
                "Это единичный случай.",
                "This is a single case.",
            ),
            "подлый": (
                "mean, despicable",
                "Он подлый человек.",
                "He is a mean person.",
            ),
            "избыточный": (
                "excessive, surplus",
                "Это избыточный вес.",
                "This is excessive weight.",
            ),
            "напрягать": (
                "strain, tense",
                "Не напрягай руку.",
                "Do not strain your hand.",
            ),
            "уточнение": (
                "clarification, specification",
                "Мне нужно уточнение.",
                "I need a clarification.",
            ),
            "нелегко": (
                "not easy, difficult",
                "Ему нелегко.",
                "It is not easy for him.",
            ),
            "устоять": (
                "withstand, resist",
                "Он не устоял.",
                "He did not withstand.",
            ),
            "недоразумение": (
                "misunderstanding, mix-up",
                "Это простое недоразумение.",
                "This is a simple misunderstanding.",
            ),
            "судорожно": (
                "convulsively, spasmodically",
                "Он судорожно кивает.",
                "He nods convulsively.",
            ),
            "забивать": (
                "to score, to hammer",
                "Он забивает снова.",
                "He scores again.",
            ),
            "удариться": (
                "to hit, to strike",
                "Он ударился о стол.",
                "He hit the table.",
            ),
            "вспоминаться": (
                "to be remembered, to be recalled",
                "Это часто вспоминается.",
                "This is remembered often.",
            ),
            "робкий": (
                "timid, shy",
                "Он слишком робкий.",
                "He is too timid.",
            ),
            "зажигать": (
                "to light, to ignite",
                "Зажигай свечу.",
                "Light the candle.",
            ),
            "добавление": (
                "addition, adding",
                "Это полезное добавление.",
                "This is a useful addition.",
            ),
        },
    )
)

FUNCTION_EN = {
    "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
    "i", "he", "she", "we", "they", "you", "it", "this", "that", "these", "those",
    "my", "his", "her", "our", "their", "me", "him", "us", "them",
    "not", "no", "do", "does", "did", "will", "would", "can", "could",
    "to", "of", "in", "on", "at", "for", "from", "with", "by", "and", "or", "but",
    "already", "here", "there", "too", "very", "again", "what", "how", "often",
    "out", "up", "off", "into", "about", "than", "as", "so", "if", "when",
}

FUNCTION_RU = {
    "я", "ты", "он", "она", "мы", "вы", "они", "меня", "тебя", "его", "её", "ее",
    "нас", "вас", "их", "мне", "тебе", "ему", "ей", "нам", "вам", "им",
    "мой", "моя", "мое", "моё", "мои", "твой", "свой", "своя", "свое", "свои", "свою",
    "своей", "своего", "этот", "эта", "это", "эти", "тот", "та", "то", "те",
    "в", "во", "на", "с", "со", "к", "ко", "у", "о", "об", "от", "до",
    "из", "за", "по", "под", "над", "при", "для", "без", "между", "через",
    "был", "была", "было", "были", "будет", "будут", "буду", "есть", "быть",
    "уже", "еще", "ещё", "также", "тоже", "только", "вот", "ведь", "ну", "все",
    "как", "что", "чтобы", "когда", "если", "где", "чем", "кто", "тут",
    "там", "здесь", "давай", "нем", "нём", "ней", "них", "не", "ни", "да",
    "и", "а", "но", "или", "же", "ли", "бы", "какая", "какой", "какое",
}

allow_en = {
    line.strip().lower()
    for line in (REPO / "russian_english/_vocab/allow_en_15260214.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_ru = {
    line.strip().replace("ё", "е").lower()
    for line in (REPO / "russian_english/_vocab/allow_ru_15260214.txt").read_text(encoding="utf-8").splitlines()
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
    "intensified": "intensify", "shattered": "shatter", "started": "start",
    "listens": "listen", "nods": "nod", "misses": "miss", "crawls": "crawl",
    "soars": "soar", "flares": "flare", "scores": "score", "hit": "hit",
    "needed": "need", "closed": "close",
}

IRREGULAR_RU = {
    "идет": "идти", "иду": "идти", "шел": "идти", "шла": "идти", "шли": "идти",
    "нужна": "нужный", "нужен": "нужный", "нужно": "нужный",
    "надень": "надеть", "нанеси": "нанести", "закажи": "заказать",
    "швырни": "швырнуть", "вскрой": "вскрыть", "вылезь": "вылезть",
    "отодвинь": "отодвинуть", "прикоснись": "прикоснуться",
    "вовлеки": "вовлечь", "отвлеки": "отвлечь", "испугай": "испугать",
    "поддался": "поддаться", "устоял": "устоять", "совпало": "совпасть",
    "помчался": "помчаться", "ударился": "удариться", "запела": "запеть",
    "усилится": "усилиться", "разбилась": "разбиться",
    "смотрит": "смотреть", "молчит": "молчать", "болит": "болеть",
    "болеет": "болеть", "любит": "любить", "пишет": "писать",
    "говорит": "говорить", "слушает": "слушать", "кивает": "кивать",
    "скучает": "скучать", "лежит": "лежать", "вижу": "видеть",
    "видит": "видеть", "виден": "видный", "видно": "видно",
    "замирает": "замирать", "прилагай": "прилагать", "силы": "сила",
    "силу": "сила", "реке": "река", "реки": "река", "ползает": "ползать",
    "подражай": "подражать", "печатается": "печататься", "новая": "новый",
    "измеряй": "измерять", "подъезжает": "подъезжать",
    "прерывай": "прерывать", "побуждает": "побуждать", "удаляй": "удалять",
    "вспыхивает": "вспыхивать", "специализируется": "специализироваться",
    "рту": "рот", "напрягай": "напрягать", "руку": "рука",
    "забивает": "забивать", "вспоминается": "вспоминаться",
    "зажигай": "зажигать", "может": "мочь",
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


dest = REPO / "russian_english/_chunks/fixed/deck_15260214_03.csv"
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
