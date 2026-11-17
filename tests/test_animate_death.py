"""Last-turns animations of zoo deaths (scripts/animate_death.py)."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import animate_death
import death_pages


class AnimateDeathTest(unittest.TestCase):
    def rows(self):
        # several keys per game turn, as in a borgh state log
        return [{'line': n, 'turn': 1000 + (n // 3) * 10} for n in range(1, 301)]

    def test_frames_come_from_the_last_turns_only_one_per_turn(self):
        chosen = animate_death.select(self.rows(), 2000, 500, 12)
        self.assertEqual(len(chosen), 11)  # the death is the twelfth frame
        self.assertTrue(all(r['turn'] >= 1500 for r in chosen))
        self.assertEqual(len({r['turn'] for r in chosen}), len(chosen))
        self.assertEqual(chosen, sorted(chosen, key=lambda r: r['line']))

    def test_a_short_window_gives_fewer_frames(self):
        chosen = animate_death.select(self.rows(), 2000, 30, 24)
        self.assertEqual([r['turn'] for r in chosen], [1970, 1980, 1990, 2000])

    def test_messages_keep_notes_apart_and_their_key_index(self):
        with tempfile.TemporaryDirectory() as tmp:
            log = Path(tmp) / 'messages.log'
            log.write_text('2171 57480 0 # Scary guy on level.\n2172 57485 0 The giant white mouse misses you.\n'
                           'garbage line\n')
            notes = animate_death.messages(log)
        self.assertEqual(notes, [(2171, '57480', 'Scary guy on level.', True),
                                 (2172, '57485', 'The giant white mouse misses you.', False)])
        # A frame stopped after 2172 keys has not yet played key 2173, which wrote line 2172.
        self.assertEqual([m[0] for m in notes if m[0] < 2172], [2171])

    def test_the_death_page_shows_its_animations(self):
        with tempfile.TemporaryDirectory() as tmp:
            case = Path(tmp) / 'deaths' / ('D-' + 'a' * 64)
            (case / 'media').mkdir(parents=True)
            (case / 'record.json').write_text(json.dumps({
                'schema': 'borg-reborn-rs/death-record@1', 'id': case.name, 'character': 'Human Druid',
                'raw_cause': 'a crow', 'identity': {'seed': 1, 'git_rev': 'abc'}, 'terminal': {'turn': 500}}))
            (case / 'summary.json').write_text('{}')
            death_pages.dossier_page(case)
            self.assertNotIn('Last turns before the death', (case / 'README.md').read_text())
            for turns in (2000, 500):
                (case / 'media' / f'last-{turns}-turns.gif').write_bytes(b'GIF89a')
            death_pages.dossier_page(case)
            page = (case / 'README.md').read_text()
        self.assertIn('## Last turns before the death', page)
        self.assertLess(page.index('Last 500 game turns'), page.index('Last 2000 game turns'))
        self.assertIn('[receipt](media/last-500-turns.json)', page)


if __name__ == '__main__':
    unittest.main()
