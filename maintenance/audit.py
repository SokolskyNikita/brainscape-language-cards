#!/usr/bin/env python3
"""Read-only, meaning-aware vocabulary audit for the current card mirror.

The script intentionally knows nothing about dated workspaces or the
Brainscape API.  It consumes the stable ``courses.json`` manifest and the
per-deck JSON/CSV exports in the four-course mirror.  Only the two English
example packs are subject to the vocabulary sequencing rule; Spanish packs
remain available to the mirror validator and future editing tools.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterable

try:
    from nltk.stem import WordNetLemmatizer
except ImportError as exc:  # pragma: no cover - exercised on a bare checkout
    WordNetLemmatizer = None  # type: ignore[assignment,misc]
    _NLTK_IMPORT_ERROR = exc
else:
    _NLTK_IMPORT_ERROR = None


ROOT = Path(__file__).resolve().parents[1]
MAINTENANCE = Path(__file__).resolve().parent
DEFAULT_POLICY = MAINTENANCE / "policy.json"
PACKS = ("english_russian", "russian_english")
FIELDS = (
    "cardId",
    "deckId",
    "number",
    "qMdBody",
    "qMdFootnote",
    "aMdBody",
    "aMdFootnote",
)


class AuditError(RuntimeError):
    """An invalid mirror or stale review that should stop the audit."""


def _require_wordnet() -> None:
    if WordNetLemmatizer is None:
        raise AuditError(
            "nltk is required for inflection matching; install cards/requirements.txt"
        ) from _NLTK_IMPORT_ERROR
    try:
        # Accessing _morphy is enough to detect a missing WordNet corpus.
        WordNetLemmatizer()._morphy("work", "v")
    except LookupError as exc:
        raise AuditError(
            "NLTK WordNet data is missing; run `python -m nltk.downloader wordnet`"
        ) from exc


def _text(value: Any) -> str:
    return "" if value is None else str(value)


def parse_face(markdown: str) -> tuple[str | None, str, str]:
    """Return ``(prompt, body, footnote)`` from a Brainscape markdown face."""

    value = _text(markdown).replace("\r\n", "\n").replace("\r", "\n")
    before, marker, footnote = value.partition("## Footnote")
    if not marker:
        footnote = ""
    before = before.strip("\n ")
    prompt: str | None = None
    lines = before.splitlines()
    if lines and lines[0].strip().lower() == "# translate:":
        prompt = "# Translate:"
        before = "\n".join(lines[1:]).strip("\n ")
    return prompt, before, footnote.strip("\n ")


def _normalise_card(raw: dict[str, Any]) -> dict[str, Any]:
    """Normalise a saved API record or a minimal CSV-derived record."""

    if all(key in raw for key in ("qMdBody", "aMdBody")):
        card = dict(raw)
    else:
        question = raw.get("Question", raw.get("question", ""))
        answer = raw.get("Answer", raw.get("answer", ""))
        qprompt, qbody, qfoot = parse_face(question)
        aprompt, abody, afoot = parse_face(answer)
        card = dict(raw)
        card.update(
            qMdPrompt=qprompt,
            qMdBody=qbody,
            qMdFootnote=qfoot,
            aMdPrompt=aprompt,
            aMdBody=abody,
            aMdFootnote=afoot,
        )
    for key in FIELDS:
        card.setdefault(key, None)
    return card


def _json_cards(path: Path) -> list[dict[str, Any]]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(value, dict):
        value = value.get("cards")
    if not isinstance(value, list) or not all(isinstance(x, dict) for x in value):
        raise AuditError(f"{path}: expected a JSON array of card records")
    cards = [_normalise_card(x) for x in value]
    if not all(card.get("qMdBody") is not None for card in cards):
        raise AuditError(f"{path}: JSON cards do not contain qMdBody/aMdBody fields")
    return cards


def _csv_cards(path: Path) -> list[dict[str, Any]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    if not rows or not {"Question", "Answer"}.issubset(rows[0]):
        raise AuditError(f"{path}: expected Question,Answer CSV columns")
    return [_normalise_card(row) for row in rows]


def _relative(path: Path, root: Path) -> str:
    try:
        return str(path.resolve().relative_to(root.resolve()))
    except ValueError:
        return str(path)


def _source_for_deck(
    deck: dict[str, Any], root: Path, source_mode: str = "json"
) -> tuple[Path, list[dict[str, Any]]]:
    """Read JSON snapshots by default, or CSV proposals when requested."""

    candidates: list[Path] = []
    keys = ("csv", "json") if source_mode == "csv" else ("json", "csv")
    for key in keys:
        name = deck.get(key)
        if name:
            path = Path(name)
            candidates.append(path if path.is_absolute() else root / path)
    errors: list[str] = []
    for path in candidates:
        if not path.exists():
            errors.append(f"missing {path}")
            continue
        try:
            return path, _json_cards(path) if path.suffix == ".json" else _csv_cards(path)
        except (OSError, ValueError, json.JSONDecodeError, AuditError) as exc:
            errors.append(f"{path}: {exc}")
    raise AuditError(f"{deck.get('deckId', '<unknown>')}: no readable deck source ({'; '.join(errors)})")


def load_manifest(
    courses_path: Path,
    policy: dict[str, Any],
    source_mode: str = "json",
) -> tuple[dict[str, list[dict[str, Any]]], list[dict[str, Any]]]:
    """Load the configured English/Russian decks and source fingerprints."""

    data = json.loads(courses_path.read_text(encoding="utf-8"))
    courses = data.get("courses") if isinstance(data, dict) else data
    if not isinstance(courses, list):
        raise AuditError(f"{courses_path}: expected a courses array")
    by_slug = {item.get("slug"): item for item in courses if isinstance(item, dict)}
    missing = [slug for slug in PACKS if slug not in by_slug]
    if missing:
        raise AuditError(f"{courses_path}: missing courses {', '.join(missing)}")

    root = courses_path.parent
    packs: dict[str, list[dict[str, Any]]] = {}
    source_manifest: list[dict[str, Any]] = []
    for slug in PACKS:
        course = by_slug[slug]
        entries = course.get("decks")
        if not isinstance(entries, list) or not entries:
            raise AuditError(f"{slug}: course has no ordered decks")
        ordered = sorted(entries, key=lambda item: int(item.get("position", 0)))
        positions = [int(item.get("position", 0)) for item in ordered]
        # ``position`` is the live course position.  A filtered mirror may
        # intentionally have a gap where an unrelated live deck was omitted
        # (the final English → Russian deck is live position 21 after removing
        # an unrelated Spanish test deck at position 20).  The sorted mirror
        # order, rather than the live position number, drives card bands.
        if not positions or positions != sorted(set(positions)):
            raise AuditError(f"{slug}: deck positions must be strictly increasing")
        loaded: list[dict[str, Any]] = []
        for order, entry in enumerate(ordered, 1):
            source, cards = _source_for_deck(entry, root, source_mode)
            expected = int(entry.get("card_count", len(cards)))
            if len(cards) != expected:
                raise AuditError(
                    f"{slug} deck {entry.get('deckId')}: expected {expected} cards, found {len(cards)}"
                )
            if not cards:
                raise AuditError(f"{slug} deck {entry.get('deckId')}: empty deck")
            deck = dict(
                entry,
                position=order,
                live_position=int(entry.get("position", order)),
                file=source.name,
                cards=cards,
                source=source,
            )
            loaded.append(deck)
            source_manifest.append(
                {
                    "pack": slug,
                    "deck": str(entry.get("deckId", source.stem)),
                    "position": order,
                    "live_position": int(entry.get("position", order)),
                    "cards": len(cards),
                    "source": _relative(source, root),
                    "sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
                }
            )
        packs[slug] = loaded

    expected_total = int(policy.get("reference_fingerprint", {}).get("cards", 0))
    if expected_total and sum(len(d["cards"]) for d in packs["english_russian"]) != expected_total:
        raise AuditError("reference English → Russian card count changed; refresh policy reviews")
    return packs, source_manifest


def surface_tokens(value: str) -> list[str]:
    """Tokenise the exact surface spelling used by the reference audit."""

    value = _text(value).lower().replace("’", "'").replace("‘", "'")
    value = value.replace("‐", "-").replace("‑", "-")
    return re.findall(r"[a-zà-öø-ÿ]+(?:['-][a-zà-öø-ÿ]+)*", value)


def expanded_tokens(value: str) -> list[str]:
    """Expand grammar contractions for the inflection fallback."""

    value = _text(value).lower().replace("’", "'")
    value = "".join(
        char
        for char in unicodedata.normalize("NFKD", value)
        if not unicodedata.combining(char)
    )
    value = re.sub(r"\bwon't\b", "will not", value)
    value = re.sub(r"\bcan't\b", "can not", value)
    value = re.sub(r"\bcannot\b", "can not", value)
    value = re.sub(r"\bshan't\b", "shall not", value)
    value = re.sub(r"n't\b", " not", value)
    for suffix, full in (("'m", " am"), ("'re", " are"), ("'ve", " have"), ("'ll", " will"), ("'d", " would")):
        value = re.sub(re.escape(suffix) + r"\b", full, value)
    value = re.sub(r"\b(it|he|she|that|there|here|what|who)'s\b", r"\1 is", value)
    value = re.sub(r"\blet's\b", "let us", value)
    value = re.sub(r"'s\b", "", value)
    return re.findall(r"[a-z]+", value)


def head_tokens(value: str) -> list[str]:
    # Parenthetical explanatory labels do not teach a target word.
    return surface_tokens(re.sub(r"\([^)]*\)", "", _text(value)))


PRONOUNS = dict(
    zip(
        "me my mine him his her hers us our ours them their theirs your yours".split(),
        "i i i he he she she we we we they they they you you".split(),
    )
)
REFLEXIVES = {token: "self" for token in "myself yourself himself herself itself ourselves yourselves themselves oneself".split()}
INFLECTIONS = {
    **PRONOUNS,
    **REFLEXIVES,
    "an": "a",
    "these": "this",
    "those": "that",
    "could": "can",
    "would": "will",
    "should": "shall",
    "might": "may",
    "towards": "toward",
    "disc": "disk",
}


@lru_cache(maxsize=None)
def forms(token: str) -> frozenset[str]:
    _require_wordnet()
    token = token.lower()
    base = INFLECTIONS.get(token, token)
    lemmatizer = WordNetLemmatizer()
    return frozenset(
        {token, base}
        | {
            form
            for pos in ("n", "v", "a", "r")
            for form in lemmatizer._morphy(base, pos)
        }
    )


def _reference_fingerprint(decks: Iterable[dict[str, Any]]) -> str:
    pairs = [
        [card.get("qMdBody", ""), card.get("aMdBody", "")]
        for deck in decks
        for card in deck["cards"]
    ]
    payload = json.dumps(pairs, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _validate_reference_fingerprint(packs: dict[str, list[dict[str, Any]]], policy: dict[str, Any]) -> None:
    expected = policy.get("reference_fingerprint", {}).get("headword_pairs_sha256")
    if not expected:
        return
    actual = _reference_fingerprint(packs["english_russian"])
    if actual != expected:
        raise AuditError(
            "English → Russian headwords changed; refresh sense_reviews.json and "
            "policy.reference_fingerprint before auditing the new mirror"
        )


def _load_reviews(path: Path) -> dict[tuple[str, int, str], dict[str, Any]]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, list):
        raise AuditError(f"{path}: expected a JSON array")
    lookup: dict[tuple[str, int, str], dict[str, Any]] = {}
    for item in value:
        if not isinstance(item, dict):
            raise AuditError(f"{path}: each review must be an object")
        key = (str(item["pack"]), int(item["overall"]), str(item["word"]))
        if key in lookup:
            raise AuditError(f"{path}: duplicate review {key}")
        lookup[key] = item
    return lookup


def audit(
    *,
    courses_path: Path,
    output_dir: Path,
    policy_path: Path = DEFAULT_POLICY,
    source_mode: str = "json",
) -> dict[str, Any]:
    """Run the audit and write machine-readable results to ``output_dir``."""

    policy = json.loads(policy_path.read_text(encoding="utf-8"))
    if not isinstance(policy, dict):
        raise AuditError(f"{policy_path}: expected a policy object")
    if source_mode not in {"json", "csv"}:
        raise AuditError(f"unsupported source mode: {source_mode}")
    packs, manifest = load_manifest(courses_path, policy, source_mode)
    _validate_reference_fingerprint(packs, policy)
    review_file = policy_path.parent / str(policy.get("sense_reviews", "sense_reviews.json"))
    reviews = _load_reviews(review_file)
    exempt = set(policy.get("exempt_forms", []))
    _require_wordnet()

    exact: dict[str, dict[str, Any]] = {}
    morph: defaultdict[str, list[dict[str, Any]]] = defaultdict(list)
    reference_by_position: dict[int, dict[str, Any]] = {}
    for deck_index, deck in enumerate(packs["english_russian"]):
        for row, card in enumerate(deck["cards"], 1):
            overall = deck_index * int(policy["cards_per_band"]) + row
            reference = {
                "deck": str(deck.get("deckId", deck["file"])),
                "deck_index": deck_index,
                "band": deck.get("name", f"{row}"),
                "row": row,
                "overall": overall,
                "head": card.get("qMdBody", ""),
            }
            reference_by_position[overall] = dict(
                reference,
                russian=card.get("aMdBody", ""),
                example=card.get("qMdFootnote", ""),
            )
            for token in sorted(set(head_tokens(card.get("qMdBody", "")))):
                exact.setdefault(token, reference)
                for inflection in forms(token):
                    morph[inflection].append(dict(reference, head_token=token))

    findings: list[dict[str, Any]] = []
    deck_results: list[dict[str, Any]] = []
    decisions: Counter[tuple[str, str]] = Counter()
    semantic_decisions: list[dict[str, Any]] = []
    band_size = int(policy["cards_per_band"])

    for pack in PACKS:
        key, example_key = (
            ("qMdBody", "qMdFootnote")
            if pack == "english_russian"
            else ("aMdBody", "aMdFootnote")
        )
        for deck_index, deck in enumerate(packs[pack]):
            subset: list[dict[str, Any]] = []
            prior_limit = max(0, deck_index - 1)
            for row, card in enumerate(deck["cards"], 1):
                overall = deck_index * band_size + row
                target = set(head_tokens(card.get(key, "")))
                target_forms = set().union(*(forms(token) for token in target)) if target else set()
                active_reviews: set[tuple[str, int, str]] = set()

                def check(token: str, stack: tuple[str, ...] = ()) -> tuple[dict[str, Any] | None, str]:
                    if token in stack:
                        return None, "recursive_component"
                    if token in exempt:
                        return None, "explicit_exemption"
                    if token in target:
                        return None, "current_target"

                    review = reviews.get((pack, overall, token))
                    if review and review.get("action") == "resolve_sense":
                        active_reviews.add((pack, overall, token))
                        if review.get("head") != card.get(key) or review.get("example") != card.get(example_key):
                            raise AuditError(
                                f"stale semantic review: {pack} #{overall} {token}; "
                                "the target or example changed"
                            )
                        matching = [
                            reference_by_position[position]
                            for position in review.get("exact_reference_positions", [])
                            if position in reference_by_position
                        ]
                        if len(matching) != len(review.get("exact_reference_positions", [])):
                            raise AuditError(f"semantic review references a missing lesson: {pack} #{overall} {token}")
                        if not all(token in head_tokens(item["head"]) for item in matching):
                            raise AuditError(f"semantic review exact reference does not contain {token}: {pack} #{overall}")
                        if matching:
                            earliest = min(matching, key=lambda item: item["overall"])
                            allowed = earliest["deck_index"] <= prior_limit
                            outcome = (
                                None
                                if allowed
                                else {
                                    "word": token,
                                    "reason": "same_deck" if earliest["deck_index"] == deck_index else "later_deck",
                                    "earliest": earliest,
                                    "matched_forms": [],
                                    "sense": review.get("sense"),
                                    "semantic_reason": review.get("reason"),
                                }
                            )
                        elif target.intersection(review.get("current_target_lemmas", [])):
                            earliest = None
                            allowed = True
                            outcome = None
                        else:
                            bases = [
                                reference_by_position[position]
                                for position in review.get("base_reference_positions", [])
                                if position in reference_by_position
                            ]
                            earliest = min(bases, key=lambda item: item["overall"]) if bases else None
                            allowed = bool(earliest and earliest["deck_index"] <= prior_limit)
                            outcome = (
                                None
                                if allowed
                                else {
                                    "word": token,
                                    "reason": "base_not_yet_allowed" if earliest else "sense_not_taught",
                                    "earliest": earliest,
                                    "matched_forms": review.get("current_target_lemmas", []),
                                    "sense": review.get("sense"),
                                    "semantic_reason": review.get("reason"),
                                }
                            )
                        semantic_decisions.append(
                            {
                                "pack": pack,
                                "overall": overall,
                                "word": token,
                                "sense": review.get("sense"),
                                "allowed": allowed,
                                "earliest": earliest,
                                "reason": review.get("reason"),
                            }
                        )
                        return outcome, "sense_allowed" if allowed else "sense_blocked"

                    scheduled = exact.get(token)
                    if scheduled:
                        if scheduled["deck_index"] <= prior_limit:
                            return None, "exact_prior"
                        return {
                            "word": token,
                            "reason": "same_deck" if scheduled["deck_index"] == deck_index else "later_deck",
                            "earliest": scheduled,
                            "matched_forms": [],
                        }, "blocked_scheduled_form"

                    # A contraction or possessive is decomposed only if that
                    # spelling is not itself an explicitly taught target. The
                    # tokenizer expands the approved contractions already.
                    components = expanded_tokens(token)
                    if len(components) > 1:
                        component_findings = []
                        for component in components:
                            result, _ = check(component, stack + (token,))
                            if result:
                                component_findings.append(result)
                        return (
                            {
                                "word": token,
                                "reason": "component_not_allowed",
                                "earliest": None,
                                "matched_forms": [],
                                "components": component_findings,
                            }
                            if component_findings
                            else None,
                            "expanded_expression",
                        )
                    if len(components) == 1 and components[0] != token:
                        result, _ = check(components[0], stack + (token,))
                        return (
                            {
                                "word": token,
                                "reason": "component_not_allowed",
                                "earliest": None,
                                "matched_forms": [],
                                "components": [result],
                            }
                            if result
                            else None,
                            "expanded_expression",
                        )

                    related = forms(token)
                    if related.intersection(target_forms):
                        return None, "never_taught_target_inflection"
                    references = [reference for form in related for reference in morph.get(form, [])]
                    allowed = [reference for reference in references if reference["deck_index"] <= prior_limit]
                    if allowed:
                        return None, "never_taught_prior_inflection"
                    earliest = min(references, key=lambda item: item["overall"]) if references else None
                    return {
                        "word": token,
                        "reason": "base_not_yet_allowed" if earliest else "absent",
                        "earliest": earliest,
                        "matched_forms": sorted(related),
                    }, "blocked_unintroduced_base"

                for token, occurrences in sorted(Counter(surface_tokens(card.get(example_key, ""))).items()):
                    bad, decision = check(token)
                    decisions[(pack, decision)] += 1
                    if not bad:
                        continue
                    finding = {
                        "pack": pack,
                        "deck": str(deck.get("deckId", deck["file"])),
                        "band": deck.get("name", ""),
                        "row": row,
                        "overall": overall,
                        "head": card.get(key, ""),
                        "example": card.get(example_key, ""),
                        "occurrences": occurrences,
                        **bad,
                    }
                    subset.append(finding)
                    findings.append(finding)
            deck_results.append(
                {
                    "pack": pack,
                    "deck": str(deck.get("deckId", deck["file"])),
                    "position": deck_index + 1,
                    "band": deck.get("name", ""),
                    "total_cards": len(deck["cards"]),
                    "flagged_cards": len({item["overall"] for item in subset}),
                    "word_card_pairs": len(subset),
                }
            )

    summary: dict[str, Any] = {}
    for pack in PACKS:
        pack_findings = [item for item in findings if item["pack"] == pack]
        summary[pack] = {
            "total_cards": sum(len(deck["cards"]) for deck in packs[pack]),
            "flagged_cards": len({item["overall"] for item in pack_findings}),
            "word_card_pairs": len(pack_findings),
            "word_occurrences": sum(item["occurrences"] for item in pack_findings),
            "unique_word_forms": len({item["word"] for item in pack_findings}),
            "reasons": dict(Counter(item["reason"] for item in pack_findings)),
            "most_common": Counter(item["word"] for item in pack_findings).most_common(30),
            "decisions": {
                decision: count
                for (decision_pack, decision), count in decisions.items()
                if decision_pack == pack
            },
        }

    output_dir.mkdir(parents=True, exist_ok=True)
    outputs = {
        "summary.json": summary,
        "findings.json": findings,
        "decks.json": deck_results,
        "english_inventory.json": exact,
        "source_manifest.json": manifest,
        "semantic_decisions.json": semantic_decisions,
    }
    for name, value in outputs.items():
        (output_dir / name).write_text(
            json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    return summary


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--courses", type=Path, default=ROOT / "courses.json")
    parser.add_argument("--policy", type=Path, default=DEFAULT_POLICY)
    parser.add_argument(
        "--source",
        choices=("json", "csv"),
        default="json",
        help="prefer saved JSON snapshots (default) or proposed CSV exports",
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        summary = audit(
            courses_path=args.courses,
            output_dir=args.output,
            policy_path=args.policy,
            source_mode=args.source,
        )
    except (AuditError, OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 1 if any(item["flagged_cards"] for item in summary.values()) else 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
