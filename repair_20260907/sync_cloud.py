"""Sequential, resumable in-place sync of the 40 repaired vocabulary decks."""
import hashlib
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from brainscape import BrainscapeClient, cards_from_path
from brainscape.cards import card_write_payload, cards_match
from brainscape.sync import validate_deck
from brainscape.errors import BrainscapeError

BASE = ROOT / 'repair_20260907'
OUT = BASE / 'cloud_sync'
PACKS = {'english_russian': 21917816, 'russian_english': 21919521}

def log(event, **fields):
    record = dict(time=datetime.now(timezone.utc).isoformat(), event=event, **fields)
    with (OUT / 'events.jsonl').open('a') as f:
        f.write(json.dumps(record, ensure_ascii=False) + '\n')
    print(json.dumps(record, ensure_ascii=False), flush=True)

class PacedClient(BrainscapeClient):
    last_request = 0.0

    def request(self, method, path, **kwargs):
        for attempt in range(8):
            time.sleep(max(0, 0.5 - (time.monotonic() - self.last_request)))
            self.last_request = time.monotonic()
            try:
                return super().request(method, path, **kwargs)
            except BrainscapeError as exc:
                if exc.status != 429 or attempt == 7:
                    raise
                delay = min(60, 15 * 2 ** attempt)
                log('rate_limit_backoff', seconds=delay, attempt=attempt + 1)
                time.sleep(delay)

def main():
    OUT.mkdir(exist_ok=True)
    client = PacedClient.discover()
    client.ping()
    manifest = json.loads((BASE / 'applied_manifest.json').read_text())
    manifest.sort(key=lambda m: (list(PACKS).index(m['pack']), int(m['band'].split('->')[0])))
    results = []
    for ordinal, m in enumerate(manifest, 1):
        pack, deck = m['pack'], m['deck']
        pid, did = PACKS[pack], int(deck)
        source = ROOT / pack / f'deck_{deck}.csv'
        assert hashlib.sha256(source.read_bytes()).hexdigest() == m['sha256_after'], 'Local file changed after repair'
        desired = cards_from_path(source)
        original = cards_from_path(BASE / 'originals' / pack / source.name)
        live_deck = client.get_deck(pid, did)
        assert live_deck['name'] == m['band'], (did, live_deck['name'], m['band'])
        remote = client.list_cards(pid, did)
        assert len(remote) == len(desired) == len(original) == 500
        assert len({c['cardId'] for c in remote}) == 500
        for row, (old, current, want) in enumerate(zip(original, remote, desired), 1):
            assert current.get('qMdBody') in {old['qMdBody'], want['qMdBody']}, f'Unexpected live word/order: {deck} row {row}'
        backup = OUT / f'{pack}_{deck}_before.json'
        if not backup.exists():
            backup.write_text(json.dumps(remote, ensure_ascii=False, indent=2) + '\n')
        updates = [(row, cur, want) for row, (cur, want) in enumerate(zip(remote, desired), 1) if not cards_match(cur, want)]
        log('deck_start', ordinal=ordinal, total=40, pack=pack, deck=deck, band=m['band'], updates=len(updates))
        for index, (row, current, want) in enumerate(updates, 1):
            client.update_card(pid, did, current['cardId'], **card_write_payload(want))
            if index % 25 == 0:
                log('card_progress', deck=deck, updated=index, total=len(updates))
        after = client.list_cards(pid, did)
        problems = validate_deck(after, desired)
        assert not problems, f'Verification failed for {deck}: {problems[:3]}'
        assert [c['cardId'] for c in after] == [c['cardId'] for c in remote], 'Card identities or ordering changed'
        result = dict(pack=pack, pack_id=pid, deck=deck, band=m['band'], updated=len(updates), count=len(after), verified=True, source_sha256=m['sha256_after'], verified_at=datetime.now(timezone.utc).isoformat())
        (OUT / f'{pack}_{deck}_verified.json').write_text(json.dumps(result, indent=2) + '\n')
        results.append(result)
        (OUT / 'results.json').write_text(json.dumps(results, indent=2) + '\n')
        log('deck_verified', ordinal=ordinal, **result)
        if ordinal < len(manifest):
            time.sleep(3)
    log('sync_complete', decks=len(results), cards=sum(r['count'] for r in results), updated=sum(r['updated'] for r in results))

if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        log('stopped', error_type=type(exc).__name__, message=str(exc))
        raise SystemExit(1)
