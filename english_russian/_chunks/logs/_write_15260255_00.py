#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PACK = ROOT / "english_russian"
sys.path.insert(0, str(ROOT))

from brainscape.cards import card_write_payload, cards_from_path, cards_match
from english_russian._chunk_io import write_csv

SRC = PACK / "_chunks" / "deck_15260255_00.csv"
OUT = PACK / "_chunks" / "fixed" / "deck_15260255_00.csv"
LOG = PACK / "_chunks" / "logs" / "deck_15260255_00.txt"

FUNCTION = {
    "a", "the", "is", "be", "i", "you", "he", "she", "it", "we", "they",
    "my", "and", "or", "in", "on", "at", "to", "of", "for", "with", "from",
    "not", "his", "him", "her", "their", "them", "our", "us", "me", "am",
    "are", "was", "were", "been", "being", "this", "that", "these", "those",
    "an", "as", "by", "into", "about", "than", "then", "so", "if", "but",
    "its", "your",
}

allow_en = {
    line.strip().lower()
    for line in (PACK / "_vocab" / "allow_en_15260255.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_ru = {
    line.strip().replace("ё", "е").lower()
    for line in (PACK / "_vocab" / "allow_ru_15260255.txt").read_text(encoding="utf-8").splitlines()
    if line.strip()
}
allow_en |= FUNCTION

# (en_lemma, en_ex, ru_lemma, ru_ex)
FIXED = [
    ("practical", "She prefers practical solutions.", "практический", "Она предпочитает практические решения."),
    ("translate", "Please translate this document.", "перевести", "Пожалуйста, переведите этот документ."),
    ("to need", "I need help.", "нуждаться", "Я нуждаюсь в помощи."),
    ("directly", "He reported this directly to the director.", "непосредственно", "Он сообщил это непосредственно директору."),
    ("sexual", "Sexual health is important.", "сексуальный", "Сексуальное здоровье важно."),
    ("including", "Every student came, including the teacher.", "включая", "Каждый студент пришёл, включая учителя."),
    ("unknown", "His name is unknown.", "неизвестный", "Его имя неизвестно."),
    ("unhappy", "He felt deeply unhappy inside.", "несчастный", "Он чувствовал себя глубоко несчастным внутри."),
    ("layer", "Add another layer of paint.", "слой", "Добавьте еще один слой краски."),
    ("musical", "She loves musical evenings.", "музыкальный", "Она любит музыкальные вечера."),
    ("besides", "Besides work, she studies art.", "помимо", "Помимо работы, она занимается искусством."),
    ("appointment", "He received an important appointment yesterday.", "назначение", "Он получил важное назначение вчера."),
    ("guilty", "He felt guilty.", "виноватый", "Он чувствовал себя виноватым."),
    ("shift", "I start my night shift soon.", "смена", "Я скоро начинаю свою ночную смену."),
    ("positive", "He received a positive answer.", "положительный", "Он получил положительный ответ."),
    ("meat", "I bought meat for dinner.", "мясо", "Я купил мясо на ужин."),
    ("allocate", "Please allocate time for education.", "выделить", "Пожалуйста, выделите время на образование."),
    ("park", "Let's meet at the park.", "парк", "Давайте встретимся в парке."),
    ("prominent", "He is a prominent writer.", "видный", "Он видный писатель."),
    ("status", "Check your status.", "статус", "Проверьте ваш статус."),
    ("prison", "He was in prison yesterday.", "тюрьма", "Он был в тюрьме вчера."),
    ("one and a half", "I waited one and a half hours.", "полтора", "Я ждал полтора часа."),
    ("observation", "His observation was accurate.", "наблюдение", "Его наблюдение было точным."),
    ("figure out", "I need to figure out this problem.", "разобраться", "Мне нужно разобраться с этой проблемой."),
    ("psychological", "He has psychological problems.", "психологический", "У него психологические проблемы."),
    ("to engage in", "I decided to engage in sport.", "заняться", "Я решил заняться спортом."),
    ("to raise", "They raise their hands.", "поднимать", "Они поднимают руки."),
    ("to be ill", "She is ill today.", "болеть", "Она болеет сегодня."),
    ("stupid", "That was a stupid error.", "глупый", "Это была глупая ошибка."),
    ("to introduce oneself", "I want to introduce myself.", "представляться", "Я хочу представиться."),
    ("advantage", "Knowledge is a significant advantage.", "преимущество", "Знание - это значительное преимущество."),
    ("stretch out", "He stretched out his hand.", "протянуть", "Он протянул руку."),
    ("agreement", "We made an agreement yesterday.", "соглашение", "Мы заключили соглашение вчера."),
    ("rear", "Check the car's rear mirror.", "задний", "Проверь заднее зеркало машины."),
    ("accessible", "The museum is easily accessible by train.", "доступный", "Музей легко доступен на поезде."),
    ("to lie ahead", "Much work lies ahead.", "предстоять", "Предстоит много работы."),
    ("heap", "A heap of clothing is on the floor.", "куча", "Куча одежды лежит на полу."),
    ("to set", "He sets the task.", "задавать", "Он задаёт задачу."),
    ("carefully", "Open the door carefully.", "осторожно", "Откройте дверь осторожно."),
    ("peace", "She found peace in nature.", "покой", "Она нашла покой на природе."),
    ("independent", "She is a strong, independent woman.", "независимый", "Она сильная, независимая женщина."),
    ("explanation", "He offered an explanation.", "объяснение", "Он предложил объяснение."),
    ("solar", "We use solar energy.", "солнечный", "Мы используем солнечную энергию."),
    ("express", "I want to express my opinion.", "выразить", "Я хочу выразить своё мнение."),
    ("difficulty", "He had difficulty with this problem.", "трудность", "У него была трудность с этой проблемой."),
    ("fool", "Don't be a fool.", "дурак", "Не будь дураком."),
    ("cooperation", "Successful projects need cooperation.", "сотрудничество", "Успешным проектам нужно сотрудничество."),
    ("platform", "Choose the right platform for your project.", "площадка", "Выберите правильную площадку для проекта."),
    ("to get tired", "I got tired quickly.", "устать", "Я быстро устал."),
    ("unit", "This is an important unit.", "единица", "Это важная единица."),
    ("journey", "I love this journey.", "путешествие", "Я люблю это путешествие."),
    ("classical", "I love classical music.", "классический", "Я люблю классическую музыку."),
    ("honest", "He is an honest man.", "честный", "Он честный человек."),
    ("to order", "He ordered them to wait.", "приказать", "Он приказал им ждать."),
    ("interaction", "Human interaction is important.", "взаимодействие", "Взаимодействие людей важно."),
    ("empire", "This empire was strong.", "империя", "Эта империя была сильной."),
    ("Orthodox", "He is Orthodox.", "православный", "Он православный."),
    ("to sigh", "She paused to sigh deeply.", "вздохнуть", "Она остановилась, чтобы глубоко вздохнуть."),
    ("temperature", "The temperature is high.", "температура", "Температура высокая."),
    ("industry", "This industry is important.", "отрасль", "Эта отрасль важна."),
    ("dress", "She wore a beautiful red dress.", "платье", "Она носила красивое красное платье."),
    ("standard", "Gold is a standard of wealth.", "стандарт", "Золото — стандарт богатства."),
    ("rest", "I need some rest now.", "отдых", "Мне сейчас нужен отдых."),
    ("to succeed", "He will succeed.", "удаваться", "Ему это удастся."),
    ("passion", "Her passion for music was obvious.", "страсть", "Её страсть к музыке была очевидна."),
    ("civilization", "This civilization is ancient.", "цивилизация", "Эта цивилизация древняя."),
    ("division", "The division went into the fight.", "дивизия", "Дивизия пошла в бой."),
    ("oil", "I need oil for dinner.", "масло", "Мне нужно масло на ужин."),
    ("patient", "The patient received excellent help.", "пациент", "Пациент получил отличную помощь."),
    ("monetary", "He needs monetary help.", "денежный", "Ему нужна денежная помощь."),
    ("police", "The police came yesterday.", "полиция", "Полиция пришла вчера."),
    ("south", "We went south for the winter.", "юг", "Мы отправились на юг на зиму."),
    ("rare", "This bird is rare.", "редкий", "Эта птица редкая."),
    ("rate", "The bank rate increased.", "ставка", "Ставка банка выросла."),
    ("connect", "Let's connect these two rooms.", "соединить", "Давайте соединим эти две комнаты."),
    ("legal", "She needs legal help.", "юридический", "Ей нужна юридическая помощь."),
    ("milk", "I drink milk every morning.", "молоко", "Я пью молоко каждое утро."),
    ("suit", "He wore a suit to the interview.", "костюм", "Он надел костюм на интервью."),
    ("forehead", "His forehead is high.", "лоб", "У него высокий лоб."),
    ("dry", "The clothing is dry.", "сухой", "Одежда сухая."),
    ("palace", "We saw the palace.", "дворец", "Мы видели дворец."),
    ("sport", "I love watching sport on TV.", "спорт", "Я люблю смотреть спорт по телевизору."),
    ("exchange", "We agreed to an exchange.", "обмен", "Мы договорились об обмене."),
    ("ban", "They decided to ban this book.", "запретить", "Они решили запретить эту книгу."),
    ("pity", "It's a pity you can't come.", "жаль", "Жаль, что ты не можешь прийти."),
    ("democracy", "Democracy needs free speech.", "демократия", "Демократии нужна свобода слова."),
    ("explosion", "The explosion was near the house.", "взрыв", "Взрыв был рядом с домом."),
    ("broadly", "He smiled broadly.", "широко", "Он широко улыбнулся."),
    ("shoot", "Soldiers will shoot in the morning.", "стрелять", "Солдаты будут стрелять утром."),
    ("silently", "She silently nodded.", "молча", "Она молча кивнула."),
    ("aspiration", "Her aspiration was to become a doctor.", "стремление", "Её стремление было стать врачом."),
    ("refusal", "His refusal was unexpected.", "отказ", "Его отказ был неожиданным."),
    ("care", "Her care for the plants is important.", "забота", "Её забота о растениях важна."),
    ("judicial", "The judicial system needs reform.", "судебный", "Судебная система нуждается в реформе."),
    ("knife", "He took the knife carefully.", "нож", "Он осторожно взял нож."),
    ("unconditionally", "He agreed unconditionally.", "безусловно", "Он согласился безусловно."),
    ("satisfied", "He looked satisfied with the results.", "довольный", "Он выглядел довольным результатами."),
    ("popular", "This song is popular.", "популярный", "Эта песня популярна."),
    ("subsequent", "Subsequent events proved this.", "последующий", "Последующие события доказали это."),
    ("thinking", "Thinking is necessary for success.", "мышление", "Мышление необходимо для успеха."),
]


def en_forms(word: str) -> set[str]:
    forms = {word}
    for suffix in ("'s", "s", "es", "ed", "ing", "ly", "er", "est"):
        if word.endswith(suffix) and len(word) > len(suffix) + 2:
            forms.add(word[: -len(suffix)])
    if word.endswith("ies") and len(word) > 4:
        forms.add(word[:-3] + "y")
    if word.endswith("ied") and len(word) > 4:
        forms.add(word[:-3] + "y")
    if word.endswith("ing") and len(word) > 5:
        forms.add(word[:-3] + "e")
    if word.endswith("ed") and len(word) > 4:
        forms.add(word[:-1])
    return forms


def en_ok(text: str) -> list[str]:
    bad = []
    for raw in re.findall(r"[A-Za-z']+", text):
        w = raw.lower().replace("'", "")
        if not w or w in allow_en or w == "tv":
            continue
        if any(form in allow_en for form in en_forms(w)):
            continue
        if w.endswith("ly") and w[:-2] + "l" in allow_en:
            continue
        bad.append(raw)
    return bad


def ru_ok(text: str) -> list[str]:
    bad = []
    for raw in re.findall(r"[А-Яа-яЁё-]+", text):
        w = raw.replace("ё", "е").replace("Ё", "е").lower()
        if w in allow_ru:
            continue
        if any(w.startswith(lemma) or lemma.startswith(w) for lemma in allow_ru if len(lemma) >= 4 and len(w) >= 4):
            continue
        if any(w[: max(4, len(w) - 3)] == lemma[: max(4, len(w) - 3)] for lemma in allow_ru if abs(len(lemma) - len(w)) <= 4 and min(len(lemma), len(w)) >= 4):
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


def main() -> None:
    originals = cards_from_path(SRC)
    if len(originals) != 100 or len(FIXED) != 100:
        raise SystemExit(f"expected 100, got {len(originals)} / {len(FIXED)}")

    cards = []
    leftover = []
    for i, (en, en_ex, ru, ru_ex) in enumerate(FIXED, 1):
        orig = originals[i - 1]
        if orig["qMdBody"] != en:
            leftover.append(f"{i}: gloss changed {orig['qMdBody']!r} -> {en!r}")
        for token in en_ok(en_ex):
            leftover.append(f"{i} EN leftover {token!r}: {en_ex}")
        for token in ru_ok(ru_ex):
            leftover.append(f"{i} RU leftover {token!r}: {ru_ex}")
        if en.split()[0].lower() not in en_ex.lower() and en.lower() not in en_ex.lower():
            # multiword: require last content word
            key = en.lower().replace("to ", "")
            if key not in en_ex.lower() and not any(p in en_ex.lower() for p in key.split()):
                leftover.append(f"{i}: EN example missing {en!r}")
        ru_key = ru.lower().replace("ё", "е")
        ru_ex_n = ru_ex.lower().replace("ё", "е")
        if ru_key[:4] not in ru_ex_n:
            leftover.append(f"{i}: RU example missing {ru!r}")
        cards.append(make_card(en, en_ex, ru, ru_ex))

    write_csv(OUT, cards)
    loaded = cards_from_path(OUT)
    if len(loaded) != 100:
        raise SystemExit(f"cards_from_path returned {len(loaded)}")

    changed = sum(1 for a, b in zip(originals, loaded) if not cards_match(a, b))
    LOG.write_text(f"{changed}\n", encoding="utf-8")
    print(f"wrote {OUT}")
    print(f"cards_from_path={len(loaded)}")
    print(f"changed={changed}")
    if leftover:
        print("LEFTOVER / CHECKS:")
        print("\n".join(leftover))


if __name__ == "__main__":
    main()
