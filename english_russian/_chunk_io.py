"""Split / merge english_russian CSVs into 100-card rewrite chunks."""

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
    card_write_payload,
    cards_from_path,
    lemma_from_card,
)

CHUNK = 100
DECKS = [
    ("deck_15260246.csv", "1->500"),
    ("deck_15260248.csv", "500->1000"),
    ("deck_15260251.csv", "1000->1500"),
    ("deck_15260255.csv", "1500->2000"),
    ("deck_15260256.csv", "2000->2500"),
    ("deck_15260257.csv", "2500->3000"),
    ("deck_15260260.csv", "3000->3500"),
    ("deck_15260263.csv", "3500->4000"),
    ("deck_15260266.csv", "4000->4500"),
    ("deck_15260268.csv", "4500->5000"),
    ("deck_15260269.csv", "5000->5500"),
    ("deck_15260272.csv", "5500->6000"),
    ("deck_15260277.csv", "6000->6500"),
    ("deck_15260280.csv", "6500->7000"),
    ("deck_15260281.csv", "7000->7500"),
    ("deck_15260282.csv", "7500->8000"),
    ("deck_15260283.csv", "8000->8500"),
    ("deck_15260285.csv", "8500->9000"),
    ("deck_15260287.csv", "9000->9500"),
    ("deck_22976521.csv", "9500->10000"),
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
            deck_en.update(_split_lemmas(lemma_from_card(card)))
            deck_ru.update(_split_lemmas(answer_lemma_from_card(card)))
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
