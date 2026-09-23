"""Package the audio attached to the current live course snapshots.

The card repository is deliberately a mirror of the courses currently on
Brainscape.  This script therefore starts with ``courses.json`` and the
per-deck JSON snapshots, rather than with a historical generation directory.
It resolves every attached qSoundUrl/aSoundUrl to a retained local recording,
copies the bytes into ``audio/current/<course>/audio/``, and writes release
archives containing only the current course files.

The script is offline.  It does not call Brainscape, download audio, generate
speech, or modify card snapshots.  A URL that changed since the last catalog
is reported and withheld from the archive so a caller can refresh and verify
that recording before publishing it.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import shutil
import zipfile
from pathlib import Path
from urllib.parse import urlparse


CARDS_ROOT = Path(__file__).resolve().parents[1]
AUDIO_ROOT = CARDS_ROOT / "audio"
CURRENT_ROOT = AUDIO_ROOT / "current"
COURSE_SLUGS = (
    "english_russian",
    "russian_english",
    "english_spanish",
    "spanish_english",
)

# Brainscape's production URLs use paths such as
# /system/cm/489/015/453/q_sound.?<content digest>.  The final extension is
# intentionally absent, so parse the path instead of relying on a filename.
URL_RE = re.compile(
    r"/cm/(?P<a>\d{3})/(?P<b>\d{3})/(?P<c>\d{3})/(?P<side>[qa])_sound(?:\.|/|$)",
    re.IGNORECASE,
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def load_json(path: Path) -> object:
    with path.open() as stream:
        return json.load(stream)


def normalize_url(value: object) -> str | None:
    if value is None:
        return None
    value = str(value).strip()
    return value or None


def url_identity(url: str) -> tuple[int, str] | None:
    match = URL_RE.search(urlparse(url).path)
    if not match:
        return None
    card_id = int(match.group("a") + match.group("b") + match.group("c"))
    side = "question" if match.group("side").lower() == "q" else "answer"
    return card_id, side


def verified_catalog() -> dict[tuple[str, int, str], dict]:
    """Read the URL and hash that were verified for each cached recording."""
    catalog = load_json(AUDIO_ROOT / "current.json")
    if catalog.get("schema") != "brainscape-current-audio-v1":
        raise ValueError("A verified current audio catalog is required")
    return {(item["course"], int(item["cardId"]), item["side"]): item
            for item in catalog["audio"]}


def expected_source(
    slug: str,
    card_id: int,
    side: str,
) -> dict | None:
    # Once a clean package has been prepared, the cache is the durable local
    # source.  This lets the dated generation directories be removed without
    # breaking a later verification or release rebuild.
    cached = CURRENT_ROOT / slug / "audio" / f"{card_id}-{'question' if side == 'question' else 'answer'}.mp3"
    if cached.exists():
        return {"path": cached, "origin": "current-cache", "sha256": sha256(cached)}
    return None


def copy_current(source: Path, slug: str, card_id: int, side: str) -> tuple[Path, str]:
    destination = CURRENT_ROOT / slug / "audio" / f"{card_id}-{'question' if side == 'question' else 'answer'}.mp3"
    destination.parent.mkdir(parents=True, exist_ok=True)
    # copy2 retains useful local timestamps while the checksum remains the
    # authoritative identity used by the catalog and release archives.
    if not destination.exists() or sha256(destination) != sha256(source):
        shutil.copy2(source, destination)
    return destination, sha256(destination)


def archive_course(output: Path, slug: str, entries: list[dict]) -> dict | None:
    files = sorted({entry["file"] for entry in entries if entry.get("file")})
    if not files:
        return None
    name = f"{slug.replace('_', '-')}-audio.zip"
    destination = output / name
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_STORED) as archive:
        for relative in files:
            source = CURRENT_ROOT / relative
            if not source.exists():
                raise FileNotFoundError(source)
            info = zipfile.ZipInfo(relative, date_time=(2026, 9, 23, 0, 0, 0))
            info.external_attr = 0o100644 << 16
            archive.writestr(info, source.read_bytes())
    with zipfile.ZipFile(destination) as archive:
        for entry in archive.infolist():
            source = CURRENT_ROOT / entry.filename
            if sha256(source) != hashlib.sha256(archive.read(entry)).hexdigest():
                raise AssertionError(f"archive payload differs from source: {entry.filename}")
    return {
        "name": name,
        "files": len(files),
        "bytes": destination.stat().st_size,
        "sha256": sha256(destination),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--courses",
        type=Path,
        default=CARDS_ROOT / "courses.json",
        help="current course metadata (default: cards/courses.json)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="release staging directory; keep it outside cards/",
    )
    parser.add_argument(
        "--verified-at",
        help="UTC ISO timestamp for reproducible catalogs (default: now)",
    )
    args = parser.parse_args()
    courses_path = args.courses.resolve()
    output = args.output.resolve()
    if output.is_relative_to(CARDS_ROOT):
        parser.error("--output must be outside cards/ so release archives are never committed")
    metadata = load_json(courses_path)
    verified_at = args.verified_at or dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()
    courses = metadata.get("courses", [])
    by_slug = {str(course["slug"]): course for course in courses}
    missing_courses = [slug for slug in COURSE_SLUGS if slug not in by_slug]
    if missing_courses:
        parser.error(f"courses.json is missing required courses: {', '.join(missing_courses)}")

    previous = verified_catalog()
    missing: list[dict] = []
    changed_urls: list[dict] = []
    by_course: dict[str, list[dict]] = {slug: [] for slug in COURSE_SLUGS}
    card_counts: dict[str, int] = {slug: 0 for slug in COURSE_SLUGS}

    for slug in COURSE_SLUGS:
        course = by_slug[slug]
        for deck in course.get("decks", []):
            deck_id = int(deck["deckId"])
            json_name = deck.get("json") or f"{slug}/deck_{deck_id}.json"
            snapshot_path = CARDS_ROOT / str(json_name)
            if not snapshot_path.exists():
                raise FileNotFoundError(f"current deck snapshot is missing: {snapshot_path}")
            cards = load_json(snapshot_path)
            expected_count = int(deck.get("card_count", len(cards)))
            if len(cards) != expected_count:
                raise AssertionError(f"{snapshot_path}: expected {expected_count} cards, found {len(cards)}")
            for position, card in enumerate(cards, 1):
                card_id = int(card["cardId"])
                if int(card.get("deckId", deck_id)) != deck_id:
                    raise AssertionError(f"{snapshot_path}: card {card_id} has the wrong deckId")
                card_counts[slug] += 1
                for side, field in (("question", "qSoundUrl"), ("answer", "aSoundUrl")):
                    url = normalize_url(card.get(field))
                    if not url:
                        continue
                    identity = url_identity(url)
                    if identity != (card_id, side):
                        missing.append({
                            "course": slug,
                            "deckId": deck_id,
                            "cardId": card_id,
                            "side": side,
                            "url": url,
                            "reason": "audio URL does not identify this card and side",
                        })
                        continue
                    prior = previous.get((slug, card_id, side))
                    old_url = prior["url"] if prior else None
                    url_changed = bool(old_url and old_url != url)
                    if url_changed:
                        changed_urls.append({
                            "course": slug,
                            "deckId": deck_id,
                            "cardId": card_id,
                            "side": side,
                            "previous_url": old_url,
                            "url": url,
                        })
                    source = expected_source(slug, card_id, side)
                    if source and (not prior or source["sha256"] != prior.get("sha256")):
                        missing.append({"course": slug, "cardId": card_id, "side": side,
                                        "reason": "cache has no verified catalog hash or bytes differ"})
                        source = None
                    # A changed URL identifies a new attachment. A cached
                    # file with the old URL must not silently be published as
                    # if it had been verified for the new attachment.
                    changed_cache_blocked = bool(
                        url_changed and source and source.get("origin") == "current-cache"
                    )
                    if changed_cache_blocked:
                        missing.append({
                            "course": slug,
                            "deckId": deck_id,
                            "cardId": card_id,
                            "side": side,
                            "url": url,
                            "reason": "audio URL changed; refresh the current cache before packaging",
                        })
                        source = None
                    detail = {
                        "url": url,
                        "file": None,
                        "sha256": None,
                        "bytes": None,
                    }
                    if source is None:
                        if not changed_cache_blocked:
                            missing.append({
                                "course": slug,
                                "deckId": deck_id,
                                "cardId": card_id,
                                "side": side,
                                "url": url,
                                "reason": "no retained local MP3 matches this card",
                            })
                    else:
                        destination, digest = copy_current(source["path"], slug, card_id, side)
                        detail["file"] = destination.relative_to(CURRENT_ROOT).as_posix()
                        detail["sha256"] = digest
                        detail["bytes"] = destination.stat().st_size
                    by_course[slug].append({
                        "course": slug,
                        "deckId": deck_id,
                        "cardId": card_id,
                        "side": side,
                        "url": url,
                        "file": detail["file"],
                        "sha256": detail["sha256"],
                        "bytes": detail["bytes"],
                    })
    if missing or changed_urls:
        raise SystemExit("Audio cache requires verification; catalogs/archives were not changed: "
                         + json.dumps({"missing": missing, "changed_urls": changed_urls}))
    output.mkdir(parents=True, exist_ok=True)
    assets = []
    for slug in COURSE_SLUGS:
        asset = archive_course(output, slug, by_course[slug])
        if asset:
            assets.append(asset)
    for asset in assets:
        asset["url"] = (
            "https://github.com/SokolskyNikita/brainscape-language-cards/releases/download/"
            f"live-audio-2026-09-23/{asset['name']}"
        )
    sha_lines = []
    for slug in COURSE_SLUGS:
        for entry in sorted(by_course[slug], key=lambda item: item["file"] or ""):
            if entry["file"] and entry["sha256"]:
                sha_lines.append(f"{entry['sha256']}  {entry['file']}\n")
    (AUDIO_ROOT / "files.sha256").write_text("".join(sha_lines))
    audio_entries = [
        entry
        for slug in COURSE_SLUGS
        for entry in sorted(by_course[slug], key=lambda item: (item["course"], item["deckId"], item["cardId"], item["side"]))
    ]
    write_json(AUDIO_ROOT / "current.json", {
        "schema": "brainscape-current-audio-v1",
        "verified_at": verified_at,
        "release_tag": "live-audio-2026-09-23",
        "courses": [
            {
                "slug": slug,
                "packId": int(by_slug[slug]["packId"]),
                "name": by_slug[slug].get("name"),
                "card_count": card_counts[slug],
                "audio_sides": len(by_course[slug]),
                "packaged_files": sum(1 for item in by_course[slug] if item["file"]),
                "missing_audio": sum(1 for item in missing if item["course"] == slug),
            }
            for slug in COURSE_SLUGS
        ],
        "audio": audio_entries,
        "missing": missing,
        "changed_urls": changed_urls,
    })
    write_json(AUDIO_ROOT / "archives.json", {
        "schema": "brainscape-current-audio-assets-v1",
        "release": "live-audio-2026-09-23",
        "verified_at": verified_at,
        "assets": assets,
    })
    (output / "SHA256SUMS").write_text("".join(f"{a['sha256']}  {a['name']}\n" for a in assets))

    print(f"Indexed {sum(card_counts.values())} current cards across {len(COURSE_SLUGS)} courses.")
    print(f"Attached audio sides: {sum(len(v) for v in by_course.values())}; packaged: {sum(len([i for i in v if i['file']]) for v in by_course.values())}.")
    print(f"Missing mappings: {len(missing)}; changed URLs: {len(changed_urls)}.")
    for asset in assets:
        print(f"Verified {asset['name']}: {asset['files']} MP3s, {asset['bytes']} bytes")


if __name__ == "__main__":
    main()
