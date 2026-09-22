"""Sync reviewed text corrections to production, preserving concurrent edits."""
import concurrent.futures
import datetime
import json
import time
from pathlib import Path
from brainscape import BrainscapeClient, card_write_payload
from spanish_audio_20260912.review import read

R = Path(__file__).resolve().parent
C = BrainscapeClient.discover(timeout=60)
packs = json.loads((R / 'packs.json').read_text())
jobs = [(p, d) for p in packs for d in p['decks']]
snapshot_dir = R / ('production_' + datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ'))
snapshot_dir.mkdir()

def fetch(job):
    p, d = job
    cards = C.list_cards(p['packId'], d['deckId'])
    (snapshot_dir / f'{d["deckId"]}.json').write_text(json.dumps(cards, ensure_ascii=False, indent=2))
    return job, cards

pending = []
conflicts = []
reports = []
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    for (p, d), live in pool.map(fetch, jobs):
        desired = read(d['deckId'])
        expected_ids = [c['cardId'] for c in desired]
        assert len(live) == len(desired) == 500
        assert [c['cardId'] for c in live] == expected_ids, f'Card IDs/order changed in {d["deckId"]}'
        changes_path = R / 'changes' / f'{d["deckId"]}.json'
        patches = {x['cardId']: x for x in json.loads(changes_path.read_text())} if changes_path.exists() else {}
        differing = 0
        for actual, expected in zip(live, desired):
            if card_write_payload(actual) == card_write_payload(expected):
                continue
            differing += 1
            patch = patches.get(actual['cardId'])
            if patch and card_write_payload(actual) == patch['before']:
                pending.append((p, d, patch, actual))
            else:
                conflicts.append({'packId': p['packId'], 'deckId': d['deckId'], 'cardId': actual['cardId']})
        reports.append({'packId': p['packId'], 'deckId': d['deckId'], 'cards': 500, 'initialDifferences': differing})
        print('Compared', len(reports), '/ 32 decks;', differing, 'differences in', d['deckId'], flush=True)

updated = []
for p, d, patch, initial in pending:
    for attempt in range(8):
        try:
            live = C.get_card(p['packId'], d['deckId'], patch['cardId'])
            current = card_write_payload(live)
            assert current in [patch['before'], patch['after']], f'Concurrent edit on {patch["cardId"]}'
            if current != patch['after']:
                C.update_card(p['packId'], d['deckId'], patch['cardId'], **patch['after'])
                updated.append(patch['cardId'])
            result = C.get_card(p['packId'], d['deckId'], patch['cardId'])
            assert card_write_payload(result) == patch['after']
            assert result.get('stats') == live.get('stats')
            for field in ['qSoundUrl', 'aSoundUrl']:
                assert result.get(field) == live.get(field)
            time.sleep(.5)
            break
        except Exception as exc:
            if getattr(exc, 'status', None) not in [429, 500, 502, 503, 504] or attempt == 7:
                raise
            time.sleep(min(60, 5 * 2 ** attempt))

result = {
    'checkedAt': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'productionBaseUrl': C.base_url,
    'status': 'conflicts' if conflicts else 'synced',
    'decks': reports,
    'cardsCompared': sum(r['cards'] for r in reports),
    'updatedCards': updated,
    'concurrentTextChanges': conflicts,
    'audioGeneratedOrUploaded': False,
}
(R / 'production_sync.json').write_text(json.dumps(result, ensure_ascii=False, indent=2))
print('PRODUCTION:', result['status'], ';', result['cardsCompared'], 'cards compared;', len(updated), 'updates;', len(conflicts), 'concurrent changes', flush=True)
if conflicts:
    raise SystemExit(2)
