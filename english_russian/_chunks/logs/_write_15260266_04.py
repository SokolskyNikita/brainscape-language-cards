#!/usr/bin/env python3
"""Rewrite english_russian deck_15260266_04 (cards 401-500)."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PACK = ROOT / "english_russian"
sys.path.insert(0, str(ROOT))

from brainscape.cards import card_write_payload, cards_from_path, cards_match
from english_russian._chunk_io import write_csv

SRC = PACK / "_chunks" / "deck_15260266_04.csv"
OUT = PACK / "_chunks" / "fixed" / "deck_15260266_04.csv"
LOG = PACK / "_chunks" / "logs" / "deck_15260266_04.txt"

FUNCTION_EN = {
    "a", "the", "is", "be", "i", "you", "he", "she", "it", "we", "they",
    "my", "and", "or", "in", "on", "at", "to", "of", "for", "with", "from",
    "not", "his", "him", "her", "their", "them", "our", "us", "me", "am",
    "are", "was", "were", "been", "being", "this", "that", "these", "those",
    "an", "as", "by", "into", "about", "than", "then", "so", "if", "but",
    "its", "your", "all", "no", "yes", "do", "does", "did", "done", "doing",
    "has", "have", "had", "having", "will", "would", "can", "could", "may",
    "might", "must", "shall", "should", "just", "also", "too", "very",
}

FUNCTION_RU = {
    w.replace("ё", "е")
    for w in {
        "я", "ты", "он", "она", "оно", "мы", "вы", "они", "меня", "тебя", "его",
        "её", "ее", "нас", "вас", "их", "мне", "тебе", "ему", "ей", "нам", "вам",
        "им", "мной", "мною", "тобой", "ним", "ней", "него", "нем", "нём", "ними",
        "неё", "нее",
        "собой", "мой", "моя", "моё", "мое", "мои", "твой", "твоя", "твоё", "твое",
        "твои", "свой", "своя", "своё", "свое", "свои", "наш", "наша", "наше",
        "наши", "ваш", "ваша", "ваше", "ваши", "этот", "эта", "это", "эти",
        "тот", "та", "то", "те", "такой", "такая", "такое", "такие", "весь",
        "вся", "всё", "все", "сам", "сама", "само", "сами", "быть", "есть",
        "был", "была", "было", "были", "буду", "будет", "будем", "будете",
        "будут", "нет", "не", "ни", "да", "уже", "ещё", "еще", "только", "даже",
        "тоже", "также", "очень", "так", "как", "что", "кто", "где", "когда",
        "почему", "куда", "который", "какой", "чтобы", "если", "потому", "ведь",
        "ли", "же", "бы", "вот", "здесь", "тут", "там", "теперь", "сейчас",
        "потом", "всегда", "никогда", "иногда", "от", "до", "по", "со", "из",
        "без", "при", "про", "об", "за", "над", "под", "перед", "после",
        "между", "через", "около", "для", "к", "у", "о", "в", "на", "с", "и",
        "а", "но", "или",
    }
}

# Keep original English glosses. Russian lemma kept unless noted.
# (ru_lemma, en_example, ru_example)
FIXED: list[tuple[str, str, str]] = [
    ("пассивный", "He was passive.", "Он был пассивным."),
    ("лечиться", "I need to be treated.", "Мне нужно лечиться."),
    ("заинтересоваться", "She will become interested in art.", "Она заинтересуется искусством."),
    ("поклониться", "They will bow down to the king.", "Они поклонятся королю."),
    ("теракт", "The city remembers the terrorist act.", "Город помнит теракт."),
    ("древность", "She loves antiquity.", "Она любит древность."),
    ("прижаться", "She will snuggle up to him.", "Она прижмётся к нему."),
    ("ансамбль", "The ensemble played.", "Ансамбль играл."),
    ("метафора", "This is only a metaphor.", "Это только метафора."),
    ("резюме", "This is my resume.", "Это моё резюме."),
    ("фиксировать", "They fix the time.", "Они фиксируют время."),
    ("нора", "This is a burrow.", "Это нора."),
    ("печень", "The liver is an important organ.", "Печень есть важный орган."),
    ("интенсивность", "The work has high intensity.", "У работы высокая интенсивность."),
    ("таракан", "I found a cockroach in the soup.", "Я нашёл таракана в супе."),
    ("противоречивый", "His words were contradictory.", "Его слова были противоречивы."),
    ("сходиться", "The paths converge at the lake.", "Пути сходятся у озера."),
    ("близнец", "She has a twin brother.", "У неё есть брат-близнец."),
    ("старательно", "She diligently did her work.", "Она старательно сделала свою работу."),
    ("героический", "It was a heroic act.", "Это был героический акт."),
    ("выбрасывать", "I throw away old paper.", "Я выбрасываю старую бумагу."),
    ("переезд", "Our relocation is next week.", "Наш переезд на следующей неделе."),
    ("предвидеть", "I foresee the future.", "Я предвижу будущее."),
    ("глина", "This house is of clay.", "Этот дом из глины."),
    ("переработка", "Recycling is important.", "Переработка важна."),
    ("хвалить", "They praise her work.", "Они хвалят её работу."),
    ("ленинский", "This is a Leninist idea.", "Это ленинская идея."),
    ("алтарь", "They stand at the altar.", "Они стоят у алтаря."),
    ("очаровательный", "She looked charming.", "Она выглядела очаровательной."),
    ("рвануть", "He will pull the door.", "Он рванёт дверь."),
    ("референдум", "The referendum will decide the city's fate.", "Референдум решит судьбу города."),
    ("одобрение", "She needs their approval.", "Ей нужно их одобрение."),
    ("гул", "I hear the hum of the engine.", "Я слышу гул двигателя."),
    ("крючок", "The coat is on the hook.", "Пальто на крючке."),
    ("биология", "I like biology.", "Мне нравится биология."),
    ("балет", "She loves ballet.", "Она любит балет."),
    ("реализоваться", "The plan was realized.", "План реализовался."),
    ("рыдать", "She will sob.", "Она будет рыдать."),
    ("чайка", "I see a seagull.", "Я вижу чайку."),
    ("склониться", "He bowed before her.", "Он склонился перед ней."),
    ("стремительный", "The river has a rapid current.", "У реки стремительное течение."),
    ("божество", "They believe in this deity.", "Они верят в это божество."),
    ("метаться", "He will flounder without help.", "Он будет метаться без помощи."),
    ("порошок", "I will buy this powder.", "Я куплю этот порошок."),
    ("Пушкин", "I read Pushkin.", "Я читаю Пушкина."),
    ("документальный", "This is a documentary movie.", "Это документальное кино."),
    ("добродетель", "Patience is a great virtue.", "Терпение есть великая добродетель."),
    ("выписать", "Please write out the address.", "Пожалуйста, выпишите адрес."),
    ("узор", "The dress has a pattern.", "На платье есть узор."),
    ("выслать", "Please send out the letter.", "Нужно выслать письмо."),
    ("стадион", "The stadium is full.", "Стадион полный."),
    ("дрожь", "I have a tremor.", "У меня дрожь."),
    ("человечек", "I see a little man.", "Я вижу человечка."),
    ("подписывать", "I need to sign this document.", "Мне нужно подписывать этот документ."),
    ("согласование", "We need coordination.", "Нам нужно согласование."),
    ("роддом", "She will give birth at the maternity hospital.", "Она родит в роддоме."),
    ("подсознание", "This is in the subconscious.", "Это в подсознании."),
    ("подсказывать", "Please hint the answer.", "Пожалуйста, подскажи ответ."),
    ("проповедь", "He will give a sermon.", "Он скажет проповедь."),
    ("факс", "I have a fax.", "У меня есть факс."),
    ("комфорт", "I like the comfort of this house.", "Мне нравится комфорт этого дома."),
    ("парашют", "He jumped with a parachute.", "Он прыгнул с парашютом."),
    ("господствовать", "They dominate in this city.", "Они господствуют в этом городе."),
    ("процентный", "This is a percentage change.", "Это процентное изменение."),
    ("цензура", "There is censorship in the country.", "В стране есть цензура."),
    ("мутный", "The water looked murky.", "Вода выглядела мутной."),
    ("интрига", "I like this intrigue.", "Мне нравится эта интрига."),
    ("складывать", "She will fold the paper.", "Она будет складывать бумагу."),
    ("многолетний", "This is a perennial flower.", "Это многолетний цветок."),
    ("стирать", "I need to erase the mistake.", "Мне нужно стирать ошибку."),
    ("недаром", "Not for nothing did she study.", "Недаром она училась."),
    ("сумочка", "She lost her handbag.", "Она потеряла сумочку."),
    ("шуба", "She has a fur coat.", "У неё есть шуба."),
    ("загнать", "Drive the horse in.", "Нужно загнать лошадь."),
    ("бокс", "He loves boxing.", "Он любит бокс."),
    ("мамин", "This is mom's house.", "Это мамин дом."),
    ("смириться", "One must resign oneself to fate.", "Нужно смириться с судьбой."),
    ("ударный", "I hear a percussive sound.", "Я слышу ударный звук."),
    ("петух", "I see a rooster.", "Я вижу петуха."),
    ("компенсировать", "I will compensate the loss.", "Я компенсирую потерю."),
    ("немыслимый", "This idea is inconceivable.", "Эта идея немыслима."),
    ("заветный", "This is her cherished dream.", "Это её заветная мечта."),
    ("античный", "This is an antique temple.", "Это античный храм."),
    ("двадцатый", "She was twentieth.", "Она была двадцатой."),
    ("убежище", "They found shelter from the storm.", "Они нашли убежище от бури."),
    ("последовательно", "He works three years consecutively.", "Он работает три года последовательно."),
    ("визуальный", "This is a visual example.", "Это визуальный пример."),
    ("оцениваться", "The work is evaluated every year.", "Работа оценивается каждый год."),
    ("инженерный", "This is an engineering problem.", "Это инженерная задача."),
    ("ненадолго", "He will come for a short time.", "Он придёт ненадолго."),
    ("сонный", "I feel very sleepy today.", "Сегодня я чувствую себя очень сонным."),
    ("драматический", "This is a dramatic story.", "Это драматическая история."),
    ("ягода", "I love a fresh berry.", "Я люблю свежую ягоду."),
    ("неудобный", "This is an inconvenient time.", "Это неудобное время."),
    ("пыльный", "The room was dusty.", "Комната была пыльной."),
    ("благословение", "Health is a great blessing.", "Здоровье есть великое благословение."),
    ("уральский", "These are the Ural mountains.", "Это уральские горы."),
    ("крымский", "This is a Crimean city.", "Это крымский город."),
    ("массивный", "This is a massive stone.", "Это массивный камень."),
    ("отправка", "The dispatch will be today.", "Отправка будет сегодня."),
]


allow_en = {
    line.strip().lower()
    for line in (PACK / "_vocab" / "allow_en_15260266.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
} | FUNCTION_EN
allow_ru = {
    line.strip().replace("ё", "е").lower()
    for line in (PACK / "_vocab" / "allow_ru_15260266.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
} | FUNCTION_RU


EN_IRREG = {
    "became": "become",
    "begun": "begin",
    "began": "begin",
    "bought": "buy",
    "came": "come",
    "did": "do",
    "done": "do",
    "felt": "feel",
    "found": "find",
    "gave": "give",
    "given": "give",
    "gone": "go",
    "got": "get",
    "had": "have",
    "heard": "hear",
    "held": "hold",
    "kept": "keep",
    "knew": "know",
    "known": "know",
    "left": "leave",
    "lost": "lose",
    "made": "make",
    "said": "say",
    "saw": "see",
    "seen": "see",
    "sent": "send",
    "stood": "stand",
    "taken": "take",
    "took": "take",
    "went": "go",
    "written": "write",
    "wrote": "write",
}


def en_forms(word: str) -> list[str]:
    out = {word}
    if word in EN_IRREG:
        out.add(EN_IRREG[word])
    for suf in ("'s", "s'", "ies", "es", "ed", "ing", "ly", "er", "est", "s"):
        if word.endswith(suf) and len(word) > len(suf) + 2:
            out.add(word[: -len(suf)])
            if suf == "ies":
                out.add(word[:-3] + "y")
            if suf == "ed" and word.endswith("ied"):
                out.add(word[:-3] + "y")
    if word.endswith("ied") and len(word) > 4:
        out.add(word[:-3] + "y")
    return list(out)


def en_ok(text: str, extra: set[str]) -> list[str]:
    bad = []
    for raw in re.findall(r"[A-Za-z']+", text):
        w = raw.lower().replace("'", "")
        if not w or w in allow_en or w in extra:
            continue
        if any(form in allow_en or form in extra for form in en_forms(w)):
            continue
        if w.endswith("ly") and w[:-2] + "l" in allow_en:
            continue
        for lemma in allow_en | extra:
            parts = lemma.replace("-", " ").split()
            if w in parts:
                break
        else:
            bad.append(raw)
    return bad


RU_IRREG = {
    "пить": ("пь",),
    "есть": ("ед", "еш", "ем", "ел"),
    "идти": ("ид", "шл", "ше"),
    "пойти": ("пой", "пош"),
    "мочь": ("мож", "мог"),
    "учить": ("уч",),
    "взять": ("возьм", "взя"),
    "хотеть": ("хоч", "хот"),
    "жить": ("жив",),
    "видеть": ("виж", "вид"),
    "говорить": ("говор",),
}


def ru_ok(text: str, extra: set[str]) -> list[str]:
    bad = []
    pool = allow_ru | extra
    for raw in re.findall(r"[А-Яа-яЁё-]+", text):
        w = raw.replace("ё", "е").replace("Ё", "е").lower()
        if w in pool:
            continue
        if any(
            w.startswith(lemma) or lemma.startswith(w)
            for lemma in pool
            if len(lemma) >= 3 and len(w) >= 3
        ):
            continue
        if any(
            w[:3] == lemma[:3]
            for lemma in pool
            if len(lemma) >= 3 and len(w) >= 3
        ):
            continue
        if any(
            lemma in pool and any(w.startswith(stem) for stem in stems)
            for lemma, stems in RU_IRREG.items()
        ):
            continue
        bad.append(raw)
    return bad


def make_card(en: str, en_ex: str, ru: str, ru_ex: str) -> dict:
    return card_write_payload(
        {
            "qMdPrompt": "Translate:",
            "qMdBody": en,
            "qMdClarifier": "",
            "qMdFootnote": en_ex,
            "aMdPrompt": "",
            "aMdBody": ru,
            "aMdClarifier": "",
            "aMdFootnote": ru_ex,
        }
    )


def lemma_in_en(gloss: str, example: str) -> bool:
    g = gloss.lower()
    ex = example.lower()
    if g in ex:
        return True
    key = re.sub(r"^(to |the |a |an )", "", g)
    if key in ex:
        return True
    parts = [p for p in key.replace("-", " ").split() if p not in {"to", "the", "a", "an", "be"}]
    return all(p in ex for p in parts) if parts else False


def lemma_in_ru(lemma: str, example: str) -> bool:
    key = lemma.lower().replace("ё", "е")
    ex = example.lower().replace("ё", "е")
    if key in ex:
        return True
    if len(key) >= 4 and key[:4] in ex:
        return True
    if len(key) >= 5 and key[:5] in ex:
        return True
    return False


def main() -> None:
    originals = cards_from_path(SRC)
    if len(originals) != 100 or len(FIXED) != 100:
        raise SystemExit(f"expected 100, got {len(originals)} / {len(FIXED)}")

    cards = []
    leftover = []
    for i, (ru, en_ex, ru_ex) in enumerate(FIXED, 1):
        orig = originals[i - 1]
        en = orig["qMdBody"]
        extra_en = set(re.findall(r"[a-z']+", en.lower()))
        extra_en |= set(en.lower().replace("-", " ").split())
        extra_ru = {w.replace("ё", "е").lower() for w in re.findall(r"[А-Яа-яЁё-]+", ru)}
        for token in en_ok(en_ex, extra_en):
            leftover.append(f"{i} EN leftover {token!r}: {en_ex}")
        for token in ru_ok(ru_ex, extra_ru):
            leftover.append(f"{i} RU leftover {token!r}: {ru_ex}")
        if not lemma_in_en(en, en_ex):
            leftover.append(f"{i}: EN example missing {en!r}")
        if not lemma_in_ru(ru, ru_ex):
            leftover.append(f"{i}: RU example missing {ru!r}")
        cards.append(make_card(en, en_ex, ru, ru_ex))

    write_csv(OUT, cards)
    loaded = cards_from_path(OUT)
    if len(loaded) != 100:
        raise SystemExit(f"cards_from_path returned {len(loaded)}")

    changed = sum(1 for a, b in zip(originals, loaded) if not cards_match(a, b))
    LOG.parent.mkdir(parents=True, exist_ok=True)
    LOG.write_text(f"{changed}\n", encoding="utf-8")
    print(f"wrote {OUT}")
    print(f"cards_from_path={len(loaded)}")
    print(f"changed={changed}")
    if leftover:
        print("LEFTOVER / CHECKS:")
        print("\n".join(leftover))
    else:
        print("vocab check clean")


if __name__ == "__main__":
    main()
