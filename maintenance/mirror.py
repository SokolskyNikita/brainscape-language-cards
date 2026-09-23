"""Read-only Brainscape export/check for the four published vocabulary courses."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import csv
from datetime import datetime, timezone
import io
import json
from pathlib import Path
import re

from brainscape import BrainscapeClient

ROOT = Path(__file__).resolve().parents[1]
COURSES = [('english_russian', 21917816, 10000), ('russian_english', 21919521, 10000),
           ('english_spanish', 21945419, 8000), ('spanish_english', 21303832, 8000)]


def public_card(card):
    keys = {'cardId', 'deckId', 'question', 'answer', 'number', 'qSoundUrl', 'aSoundUrl'}
    return {k: v for k, v in card.items() if k in keys or k.startswith(('qMd', 'aMd'))}


def csv_text(cards):
    output = io.StringIO(newline='')
    writer = csv.writer(output, lineterminator='\n')
    writer.writerow(['Question', 'Answer'])
    writer.writerows((card['question'], card['answer']) for card in cards)
    return output.getvalue()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--refresh', action='store_true', help='Replace local mirror from the live courses (GET requests only)')
    args = parser.parse_args()
    client = BrainscapeClient.discover(timeout=60)
    catalog = {'verified_at': datetime.now(timezone.utc).isoformat(), 'courses': []}
    jobs = []
    for slug, pid, expected_count in COURSES:
        pack = client.get_pack(pid)
        course = {'slug': slug, 'packId': pid, 'name': pack['name'],
                  'url': pack['paths']['sharePreviewLink'], 'card_count': 0, 'decks': []}
        decks = []
        for deck in client.list_decks(pid):
            match = re.fullmatch(r'(\d+)\s*->\s*(\d+)', deck['name'])
            if match:
                decks.append((int(match[1]), int(match[2]), deck))
        decks.sort(key=lambda d: d[2]['position'])
        assert len(decks) == expected_count // 500, f'Unexpected numbered deck count in {slug}'
        assert [end for _, end, _ in decks] == list(range(500, expected_count + 1, 500)), f'Deck order changed in {slug}'
        for start, end, deck in decks:
            did = deck['deckId']
            entry = {'deckId': did, 'name': deck['name'], 'position': deck['position'],
                     'card_count': len(deck['cardIds']), 'csv': f'{slug}/deck_{did}.csv',
                     'json': f'{slug}/deck_{did}.json'}
            assert entry['card_count'] == 500, f'Card count changed in deck {did}'
            course['decks'].append(entry)
            course['card_count'] += entry['card_count']
            jobs.append((course, entry, deck['cardIds']))
        catalog['courses'].append(course)

    def fetch(job):
        course, deck, expected_ids = job
        cards = client.list_cards(course['packId'], deck['deckId'], per_page=500)
        assert [c['cardId'] for c in cards] == expected_ids, f'Live card IDs/order mismatch: {deck["deckId"]}'
        return course, deck, [public_card(c) for c in cards]

    files = {}
    with ThreadPoolExecutor(max_workers=4) as pool:
        for n, (course, deck, cards) in enumerate(pool.map(fetch, jobs), 1):
            files[deck['json']] = json.dumps(cards, ensure_ascii=False, indent=2) + '\n'
            files[deck['csv']] = csv_text(cards)
            if n % 12 == 0:
                print(f'Fetched {n}/{len(jobs)} numbered decks', flush=True)
    if args.refresh:
        for name, content in files.items():
            path = ROOT / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
        (ROOT / 'courses.json').write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + '\n')
        print(f'Refreshed {len(jobs)} decks / {sum(c["card_count"] for c in catalog["courses"])} cards from Brainscape. No cloud writes.')
    else:
        differences = [name for name, content in files.items() if not (ROOT / name).exists() or (ROOT / name).read_text() != content]
        if differences:
            raise SystemExit('Live/local differences: ' + ', '.join(differences))
        print(f'All {len(jobs)} local decks match current Brainscape cards, IDs, order, and audio URLs.')


if __name__ == '__main__':
    main()
