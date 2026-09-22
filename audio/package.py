"""Package retained production MP3s and index the current English card recordings.

Offline only. Does not synthesize audio or modify cards/old manifests.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import zipfile

ROOT = Path(__file__).resolve().parents[1]
REPAIR = ROOT / 'sentence_repair_20260922'
SOURCES = {
    'english-russian-original-audio.zip': 'cartesia_english_russian_20260908',
    'russian-english-original-audio.zip': 'cartesia_russian_english_20260908',
    'english-example-replacement-audio.zip': 'sentence_repair_20260922',
}


def sha256(path):
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True, help='Archive output directory outside this repository')
    parser.add_argument('--tag', default='audio-2026-09-22')
    args = parser.parse_args()
    output = args.output.resolve()
    if output.is_relative_to(ROOT):
        parser.error('Use an output directory outside the repository')
    output.mkdir(parents=True, exist_ok=True)

    hashes = {}
    groups = {}
    for name, source in SOURCES.items():
        paths = sorted((ROOT / source / 'audio').glob('*.mp3'))
        expected_count = 737 if source == REPAIR.name else 10000
        assert len(paths) == expected_count, (source, len(paths), expected_count)
        groups[name] = paths
        for path in paths:
            assert not path.is_symlink(), path
            digest = sha256(path)
            if source == REPAIR.name:
                expected = json.loads(path.with_suffix('.json').read_text())['sha256']
            else:
                expected = json.loads((ROOT / source / 'receipts' / f'{path.stem}.json').read_text())['sha256']
            assert digest == expected, f'Recording differs from its verified hash: {path}'
            hashes[path.relative_to(ROOT).as_posix()] = digest

    replacements = json.loads((REPAIR / 'audio_manifest.json').read_text())
    changed = {i['cardId']: i for i in replacements['items']}
    assert len(changed) == 744
    current = []
    for pack in ['english_russian', 'russian_english']:
        side = 'q' if pack == 'english_russian' else 'a'
        source = f'cartesia_{pack}_20260908'
        original = json.loads((ROOT / source / 'manifest.json').read_text())
        by_id = {i['cardId']: i for i in original['items']}
        mappings = re.findall(r'\| `(deck_\d+\.csv)` \| ([^|]+) \|', (ROOT / pack / 'file_to_deck.md').read_text())
        assert len(mappings) == 20
        for deck_index, (filename, _) in enumerate(mappings):
            deck_id = int(Path(filename).stem.split('_')[1])
            cards = json.loads((REPAIR / 'after' / pack / f'{deck_id}.json').read_text())
            assert len(cards) == 500
            for row, card in enumerate(cards, 1):
                cid = card['cardId']
                item = changed.get(cid)
                if item:
                    assert item['pack'] == pack and item['deckId'] == deck_id
                    path = f'{REPAIR.name}/audio/{item["content_hash"]}.mp3'
                    archive = 'english-example-replacement-audio.zip'
                    transcript = item['transcript']
                else:
                    assert by_id[cid]['deckId'] == deck_id
                    path = f'{source}/audio/{cid}.mp3'
                    archive = 'english-russian-original-audio.zip' if side == 'q' else 'russian-english-original-audio.zip'
                    transcript = by_id[cid]['transcript']
                assert path in hashes
                spoken_head = re.sub(r'\([^()]*[А-Яа-яЁё][^()]*\)', '', card[side + 'MdBody']).strip()
                assert transcript == spoken_head + '. <break time="500ms"/>' + card[side + 'MdFootnote'], cid
                current.append({
                    'pack': pack, 'packId': original['packId'], 'deckId': deck_id,
                    'cardId': cid, 'overall': deck_index * 500 + row,
                    'audio_side': 'question' if side == 'q' else 'answer',
                    'headword': card[side + 'MdBody'], 'example': card[side + 'MdFootnote'],
                    'transcript': transcript, 'archive': archive, 'file': path,
                    'sha256': hashes[path],
                })
    assert len(current) == 20000 and len({i['cardId'] for i in current}) == 20000
    assert sum(i['archive'] == 'english-example-replacement-audio.zip' for i in current) == 744

    assets = []
    for name, paths in groups.items():
        destination = output / name
        with zipfile.ZipFile(destination, 'w', compression=zipfile.ZIP_STORED) as archive:
            for path in paths:
                relative = path.relative_to(ROOT).as_posix()
                info = zipfile.ZipInfo(relative, date_time=(2026, 9, 22, 0, 0, 0))
                info.external_attr = 0o100644 << 16
                archive.writestr(info, path.read_bytes())
        # Verify each archived payload against the saved production receipt.
        with zipfile.ZipFile(destination) as archive:
            assert len(archive.infolist()) == len(paths)
            for entry in archive.infolist():
                assert hashlib.sha256(archive.read(entry)).hexdigest() == hashes[entry.filename]
        assets.append({
            'name': name, 'files': len(paths), 'bytes': destination.stat().st_size,
            'sha256': sha256(destination),
            'url': f'https://github.com/SokolskyNikita/brainscape-language-cards/releases/download/{args.tag}/{name}',
        })
        print(f'Verified {name}: {len(paths)} MP3s, {destination.stat().st_size / 1024**2:.1f} MiB', flush=True)

    catalog = ROOT / 'audio'
    write_json(catalog / 'archives.json', {'release': args.tag, 'assets': assets})
    write_json(catalog / 'current.json', {'snapshot': '2026-09-22', 'cards': current})
    (catalog / 'files.sha256').write_text(''.join(f'{digest}  {path}\n' for path, digest in sorted(hashes.items())))
    (output / 'SHA256SUMS').write_text(''.join(f'{a["sha256"]}  {a["name"]}\n' for a in assets))
    print(f'Indexed {len(current)} current cards; preserved {len(hashes)} production recordings.')


if __name__ == '__main__':
    main()
