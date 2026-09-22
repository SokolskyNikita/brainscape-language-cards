"""Split / merge russian_english CSVs into 100-card rewrite chunks.

Never changes the Russian question lemma, card order, or card count.
English gloss (answer body) may change. Writes Question/Answer faces
via card_write_payload so the files stay re-importable.

Do not import any other pack. This pack is rewritten on its own.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from brainscape import (  # noqa: E402
    answer_lemma_from_card,
    card_from_faces,
    card_write_payload,
    cards_from_path,
    lemma_from_card,
)

CHUNK = 100
PROMPT = "Translate:"
DECKS = [
    ("deck_15260182.csv", "1->500"),
    ("deck_15260185.csv", "500->1000"),
    ("deck_15260188.csv", "1000->1500"),
    ("deck_15260190.csv", "1500->2000"),
    ("deck_15260191.csv", "2000->2500"),
    ("deck_15260192.csv", "2500->3000"),
    ("deck_15260194.csv", "3000->3500"),
    ("deck_15260196.csv", "3500->4000"),
    ("deck_15260198.csv", "4000->4500"),
    ("deck_15260200.csv", "4500->5000"),
    ("deck_15260204.csv", "5000->5500"),
    ("deck_15260207.csv", "5500->6000"),
    ("deck_15260210.csv", "6000->6500"),
    ("deck_15260213.csv", "6500->7000"),
    ("deck_15260214.csv", "7000->7500"),
    ("deck_15260215.csv", "7500->8000"),
    ("deck_15260217.csv", "8000->8500"),
    ("deck_15260218.csv", "8500->9000"),
    ("deck_15260221.csv", "9000->9500"),
    ("deck_15260224.csv", "9500->10000"),
]


def _split_lemmas(text: str) -> list[str]:
    parts = re.split(r"[,;/]| or | and ", text)
    out = []
    for part in parts:
        part = re.sub(r"^(to |the |a |an )", "", part.strip().lower())
        if part:
            out.append(part)
    return out or [text.strip().lower()]


def write_csv(path: Path, cards: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh, lineterminator="\n")
        writer.writerow(["Question", "Answer"])
        for card in cards:
            payload = card_write_payload(card)
            writer.writerow([payload["question"], payload["answer"]])


def rewrite_chunk(path: str | Path, fixes: dict[str, tuple[str, str, str]]) -> dict[str, int]:
    """Rewrite a 100-card chunk. Writes to ``_chunks/fixed/<same name>``."""
    src = Path(path)
    if not src.is_absolute():
        src = REPO / src
    cards = cards_from_path(src)
    lemmas = [lemma_from_card(card) for card in cards]
    wanted = set(lemmas)
    extra = set(fixes) - wanted
    missing = wanted - set(fixes)
    if extra:
        raise ValueError(f"fixes for lemmas not in chunk: {sorted(extra)[:12]}")
    if missing:
        raise ValueError(f"chunk lemmas missing from fixes: {sorted(missing)[:12]}")
    if len(lemmas) != len(wanted):
        raise ValueError("duplicate lemmas in chunk; refusing to write")

    changed = 0
    out = []
    for lemma in lemmas:
        gloss, ru, en = fixes[lemma]
        new_card = card_from_faces(
            f"# {PROMPT}\n\n{lemma}\n\n## Footnote\n\n{ru.strip()}",
            f"{gloss.strip()}\n\n## Footnote\n\n{en.strip()}",
        )
        payload = card_write_payload(new_card)
        if lemma_from_card(payload) != lemma:
            raise ValueError(f"lemma changed: {lemma!r} -> {lemma_from_card(payload)!r}")
        old = card_write_payload(cards[len(out)])
        if payload != old:
            changed += 1
        out.append(payload)

    dest = ROOT / "_chunks" / "fixed" / src.name
    write_csv(dest, out)
    return {"changed": changed, "unchanged": len(out) - changed, "total": len(out), "path": str(dest)}


def extract() -> None:
    chunks_dir = ROOT / "_chunks"
    vocab_dir = ROOT / "_vocab"
    chunks_dir.mkdir(exist_ok=True)
    vocab_dir.mkdir(exist_ok=True)
    known_en: set[str] = set()
    known_ru: set[str] = set()
    manifest = []

    for file_name, band in DECKS:
        cards = cards_from_path(ROOT / file_name)
        if len(cards) != 500:
            raise SystemExit(f"{file_name} has {len(cards)} cards, expected 500")
        deck_en: set[str] = set()
        deck_ru: set[str] = set()
        for card in cards:
            deck_ru.update(_split_lemmas(lemma_from_card(card)))
            deck_en.update(_split_lemmas(answer_lemma_from_card(card)))
        allow_en = sorted(known_en | deck_en)
        allow_ru = sorted(known_ru | deck_ru)
        deck_id = file_name.removeprefix("deck_").removesuffix(".csv")
        (vocab_dir / f"allow_en_{deck_id}.txt").write_text(
            "\n".join(allow_en) + "\n", encoding="utf-8"
        )
        (vocab_dir / f"allow_ru_{deck_id}.txt").write_text(
            "\n".join(allow_ru) + "\n", encoding="utf-8"
        )
        for index in range(0, 500, CHUNK):
            chunk_cards = cards[index : index + CHUNK]
            suffix = f"{index // CHUNK:02d}"
            stem = f"deck_{deck_id}_{suffix}"
            write_csv(chunks_dir / f"{stem}.csv", chunk_cards)
            manifest.append(
                {
                    "stem": stem,
                    "file": file_name,
                    "deck_id": deck_id,
                    "band": band,
                    "start": index + 1,
                    "end": index + len(chunk_cards),
                    "count": len(chunk_cards),
                    "allow_en": f"_vocab/allow_en_{deck_id}.txt",
                    "allow_ru": f"_vocab/allow_ru_{deck_id}.txt",
                }
            )
        known_en |= deck_en
        known_ru |= deck_ru

    (ROOT / "_chunks" / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"extracted {len(manifest)} chunks")


def merge() -> None:
    fixed_dir = ROOT / "_chunks" / "fixed"
    missing = []
    for file_name, band in DECKS:
        deck_id = file_name.removeprefix("deck_").removesuffix(".csv")
        cards = []
        for index in range(5):
            path = fixed_dir / f"deck_{deck_id}_{index:02d}.csv"
            if not path.exists():
                missing.append(str(path.relative_to(ROOT)))
                continue
            cards.extend(cards_from_path(path))
        if missing:
            continue
        if len(cards) != 500:
            raise SystemExit(f"{file_name}: merged {len(cards)} cards, expected 500")
        lemmas = [lemma_from_card(card) for card in cards]
        original = [lemma_from_card(card) for card in cards_from_path(ROOT / file_name)]
        if lemmas != original:
            raise SystemExit(f"{file_name}: lemma order changed; refusing merge")
        write_csv(ROOT / file_name, cards)
        print(f"merged {file_name} ({band}) {len(cards)}")
    if missing:
        raise SystemExit("missing fixed chunks:\n" + "\n".join(missing))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("extract", "merge"))
    args = parser.parse_args()
    if args.command == "extract":
        extract()
    else:
        merge()


if __name__ == "__main__":
    main()
