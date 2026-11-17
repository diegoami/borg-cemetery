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
        # three keys per turn, 10 game turns apart, as in a borgh state log;
        # the last turn (2000) is the death's
        return [{'line': n, 'turn': 1000 + ((n - 1) // 3) * 10} for n in range(1, 304)]

    def test_every_one_of_the_last_turns_is_drawn(self):
        chosen = animate_death.select(self.rows(), 50)
        self.assertEqual(len(chosen), 49)  # the death is the fiftieth frame
        self.assertEqual([r['turn'] for r in chosen], list(range(1510, 2000, 10)))
        # each frame is the last key of its turn
        self.assertTrue(all(r['line'] % 3 == 0 for r in chosen))

    def test_every_k_keeps_the_turns_nearest_the_death(self):
        chosen = animate_death.select(self.rows(), 10, every=3)
        self.assertEqual([r['turn'] for r in chosen], [1930, 1960, 1990])  # 1990 is the turn just before the death

    def test_a_game_shorter_than_the_window_gives_all_its_turns(self):
        rows = self.rows()[:9]  # three turns, the last one the death
        self.assertEqual([r['turn'] for r in animate_death.select(rows, 50)], [1000, 1010])

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
            for name in ('last-200-turns', 'last-50-turns', 'last-200-turns-every-4'):
                (case / 'media' / f'{name}.gif').write_bytes(b'GIF89a')
            death_pages.dossier_page(case)
            page = (case / 'README.md').read_text()
        self.assertIn('## Last turns before the death', page)
        self.assertLess(page.index('Last 50 turns'), page.index('Last 200 turns**'))
        self.assertIn('[receipt](media/last-50-turns.json)', page)
        self.assertIn('**Last 200 turns, every 4**', page)


if __name__ == '__main__':
    unittest.main()
