"""Regression checks for rejecting unverified audio without overwriting evidence."""
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location('package_current', Path(__file__).with_name('package_current.py'))
pack = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(pack)


class CacheVerificationTests(unittest.TestCase):
    def test_bad_cache_or_changed_url_never_replaces_verified_catalog(self):
        for mode in ('corrupt', 'changed_url'):
            with self.subTest(mode=mode), TemporaryDirectory() as temp:
                root = Path(temp) / 'cards'
                audio = root / 'audio'
                current = audio / 'current'
                clip = current / 'english_russian/audio/489015453-question.mp3'
                clip.parent.mkdir(parents=True)
                good = b'verified recording'
                clip.write_bytes(b'corrupt recording' if mode == 'corrupt' else good)
                old_url = 'https://s3.amazonaws.com/brainscape-prod/system/cm/489/015/453/q_sound.?old'
                card = {'cardId': 489015453, 'deckId': 1, 'qSoundUrl': old_url + ('new' if mode == 'changed_url' else '')}
                deck = root / 'deck.json'
                deck.write_text(json.dumps([card]))
                courses = {'courses': [{'slug': slug, 'packId': n, 'decks':
                           [{'deckId': 1, 'card_count': 1, 'json': 'deck.json'}] if n == 0 else []}
                           for n, slug in enumerate(pack.COURSE_SLUGS)]}
                (root / 'courses.json').write_text(json.dumps(courses))
                saved = json.dumps({'schema': 'brainscape-current-audio-v1', 'audio': [{
                    'course': 'english_russian', 'cardId': 489015453, 'side': 'question',
                    'url': old_url, 'sha256': hashlib.sha256(good).hexdigest()}]})
                (audio / 'current.json').write_text(saved)
                out = Path(temp) / 'archives'
                with patch.object(pack, 'CARDS_ROOT', root), patch.object(pack, 'AUDIO_ROOT', audio), patch.object(pack, 'CURRENT_ROOT', current), patch.object(sys, 'argv', ['package', '--courses', str(root/'courses.json'), '--output', str(out)]):
                    for _ in range(2):
                        with self.assertRaises(SystemExit):
                            pack.main()
                        self.assertEqual((audio / 'current.json').read_text(), saved)
                        self.assertFalse(out.exists())


if __name__ == '__main__':
    unittest.main()
