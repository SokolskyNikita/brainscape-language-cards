"""Offline regression checks for the portable maintenance audit."""

from __future__ import annotations

import csv
import json
import tempfile
import unittest
from pathlib import Path

from .audit import AuditError, ROOT, audit


def _face(body: str, footnote: str) -> str:
    return f"# Translate:\n\n{body}\n\n## Footnote\n\n{footnote}"


def _write_fixture(root: Path, *, review: dict | None = None) -> tuple[Path, Path]:
    """Create two tiny packs that exercise the band rule and CSV fallback."""

    courses = []
    for slug, q_values, a_values in (
        (
            "english_russian",
            [("alpha", "alpha"), ("beta", "beta"), ("gamma", "alpha"), ("delta", "beta")],
            [("альфа", "альфа"), ("бета", "бета"), ("гамма", "гамма"), ("дельта", "дельта")],
        ),
        (
            "russian_english",
            [("альфа", "alpha"), ("бета", "beta"), ("гамма", "gamma"), ("дельта", "delta")],
            [("alpha", "alpha"), ("beta", "beta"), ("gamma", "alpha"), ("delta", "beta")],
        ),
    ):
        deck_entries = []
        folder = root / slug
        folder.mkdir()
        for deck_number in range(2):
            deck_id = 1000 + len(courses) * 10 + deck_number
            records = []
            for row in range(2):
                qbody, qfoot = q_values[deck_number * 2 + row]
                abody, afoot = a_values[deck_number * 2 + row]
                records.append(
                    {
                        "cardId": deck_id * 10 + row,
                        "deckId": deck_id,
                        "number": row + 1,
                        "qMdBody": qbody,
                        "qMdFootnote": qfoot,
                        "aMdBody": abody,
                        "aMdFootnote": afoot,
                    }
                )
            json_name = f"deck_{deck_id}.json"
            csv_name = f"deck_{deck_id}.csv"
            (folder / json_name).write_text(json.dumps(records, ensure_ascii=False), encoding="utf-8")
            with (folder / csv_name).open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=["Question", "Answer"])
                writer.writeheader()
                for record in records:
                    writer.writerow(
                        {
                            "Question": _face(record["qMdBody"], record["qMdFootnote"]),
                            "Answer": _face(record["aMdBody"], record["aMdFootnote"]),
                        }
                    )
            deck_entries.append(
                {
                    "deckId": deck_id,
                    "name": f"{deck_number * 2}->{(deck_number + 1) * 2}",
                    "position": deck_number + 1,
                    "card_count": 2,
                    "csv": f"{slug}/{csv_name}",
                    "json": f"{slug}/{json_name}",
                }
            )
        courses.append({"slug": slug, "packId": 1, "name": slug, "decks": deck_entries})

    courses_path = root / "courses.json"
    courses_path.write_text(json.dumps({"courses": courses}), encoding="utf-8")
    policy_path = root / "policy.json"
    policy_path.write_text(
        json.dumps(
            {
                "policy_version": "test",
                "reference_pack": "english_russian",
                "audited_packs": ["english_russian", "russian_english"],
                "cards_per_band": 2,
                "exempt_forms": [],
                "sense_reviews": "sense_reviews.json",
                "reference_fingerprint": {},
            }
        ),
        encoding="utf-8",
    )
    reviews = [review] if review else []
    (root / "sense_reviews.json").write_text(json.dumps(reviews), encoding="utf-8")
    return courses_path, policy_path


class MaintenanceAuditTests(unittest.TestCase):
    def test_current_mirror_is_clean(self) -> None:
        courses_path = ROOT / "courses.json"
        if not courses_path.exists():
            self.skipTest("current mirror is not present")
        with tempfile.TemporaryDirectory() as output:
            summary = audit(
                courses_path=courses_path,
                output_dir=Path(output),
                policy_path=ROOT / "maintenance" / "policy.json",
            )
        self.assertEqual(
            {pack: values["flagged_cards"] for pack, values in summary.items()},
            {"english_russian": 0, "russian_english": 0},
        )

    def test_csv_source_audits_a_proposed_edit(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            courses, policy = _write_fixture(Path(directory))
            json_summary = audit(
                courses_path=courses,
                output_dir=Path(directory) / "json-output",
                policy_path=policy,
            )
            self.assertEqual(json_summary["english_russian"]["flagged_cards"], 0)

            csv_path = Path(directory) / "english_russian" / "deck_1001.csv"
            with csv_path.open(encoding="utf-8") as handle:
                rows = list(csv.DictReader(handle))
            rows[0]["Question"] = _face("gamma", "unintroduced_word")
            with csv_path.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=["Question", "Answer"])
                writer.writeheader()
                writer.writerows(rows)

            csv_summary = audit(
                courses_path=courses,
                output_dir=Path(directory) / "csv-output",
                policy_path=policy,
                source_mode="csv",
            )
            self.assertEqual(csv_summary["english_russian"]["flagged_cards"], 1)
            self.assertEqual(csv_summary["english_russian"]["word_card_pairs"], 2)

    def test_changed_context_invalidates_a_review(self) -> None:
        review = {
            "pack": "english_russian",
            "overall": 2,
            "head": "beta",
            "example": "saw",
            "ru": "бета",
            "word": "saw",
            "action": "resolve_sense",
            "sense": "see",
            "exact_reference_positions": [],
            "base_reference_positions": [1],
            "current_target_lemmas": ["alpha"],
            "reason": "A reviewed example.",
        }
        with tempfile.TemporaryDirectory() as directory:
            courses, policy = _write_fixture(Path(directory), review=review)
            json_path = Path(directory) / "english_russian" / "deck_1000.json"
            records = json.loads(json_path.read_text(encoding="utf-8"))
            # Review #2 is in the first deck's second row.
            records[1]["qMdFootnote"] = "saw changed"
            json_path.write_text(json.dumps(records), encoding="utf-8")
            with self.assertRaisesRegex(AuditError, "stale semantic review"):
                audit(
                    courses_path=courses,
                    output_dir=Path(directory) / "output",
                    policy_path=policy,
                )


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
