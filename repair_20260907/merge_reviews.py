"""Merge validated second-pass proposals onto the preserved first-pass snapshot."""
import json
from collections import Counter
from helper import BASE, read, save
from brainscape import cards_from_path

FIELDS = ['qMdBody', 'aMdBody', 'qMdFootnote', 'aMdFootnote']

def merge():
    manifest = json.loads((BASE / 'manifest.json').read_text())
    proposals = {}
    covered = Counter()
    expected_counts = {}
    for path in sorted(BASE.glob('second_pass_final_*_reviewed.json')):
        report = json.loads(path.read_text())
        entries = report if isinstance(report, list) else [dict(d, pack=report['pack']) for d in report['decks']]
        for deck in entries:
            assert deck['reviewed'] == 500
            covered[deck['pack'], str(deck['deck'])] += 1
            expected_counts[deck['pack'], str(deck['deck'])] = deck['proposed_changes']
    assert covered == Counter({(m['pack'], m['deck']): 1 for m in manifest})
    for path in sorted(BASE.glob('second_pass_final_*.json')):
        if '_reviewed' in path.stem:
            continue
        for p in json.loads(path.read_text()):
            key = (p['pack'], str(p['deck']), p['row'])
            assert key not in proposals, key
            proposals[key] = p
    actual_counts = Counter((pack, deck) for pack, deck, row in proposals)
    assert actual_counts == Counter(expected_counts), 'Review manifest counts must match proposals'
    approved = json.loads((BASE / 'approved_headword_changes.json').read_text())
    approved = {(p['deck'], p['row']): (p['before'], p['after']) for p in approved}
    merged = []
    for m in manifest:
        pack, deck = m['pack'], m['deck']
        original = read(pack, deck)
        first = cards_from_path(BASE / 'first_pass_snapshot' / pack / f'deck_{deck}.csv')
        patches = {}
        for row, (old, card) in enumerate(zip(original, first), 1):
            values = [card[k] for k in FIELDS]
            p = proposals.get((pack, deck, row))
            if p:
                assert p['before'] == values, (pack, deck, row)
                values = p['after']
            if pack == 'russian_english':
                assert values[0] == old['qMdBody']
            elif values[0] != old['qMdBody']:
                assert approved.get((deck, row)) == (old['qMdBody'], values[0])
            if values != [old[k] for k in FIELDS]:
                patches[row] = values
        merged.append((pack, deck, patches))
    for pack, deck, patches in merged:
        save(pack, deck, patches, notes='Full first pass plus independent full second pass; complete original-to-final change log.')

if __name__ == '__main__':
    merge()
