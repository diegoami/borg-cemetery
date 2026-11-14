import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from human_readable import action, threat, spells


class HumanReportsTest(unittest.TestCase):
    def test_actions_threats_and_spells_are_written_for_people(self):
        self.assertEqual(action('Walk(4)'), 'Move west')
        self.assertIn('Cast spell a from book 1', action('Cast { book: 0, letter: 97, aim: true }'))
        self.assertIn('56%', threat(dict(expected=5.46, worst=9.2, p_death=0.564)))
        readable = '\n'.join(spells([dict(book=0, flags=3, mana=1, fail=14),
                                    dict(book=0, flags=0, mana=2, fail=18)]))
        self.assertIn('Book 1, spell a', readable)
        self.assertIn('14%', readable)
        self.assertNotIn('spell b', readable)
        self.assertNotIn('{', readable)

    def test_canonical_deaths_and_scenarios_have_readable_playback_instructions(self):
        root = Path(__file__).resolve().parents[1]
        self.assertFalse((root / 'runs/local-validation-2026-11-14-reborn-seed102').exists())
        self.assertTrue((root / 'deaths/D0007/README.md').exists())
        for folder in (root / 'scenarios').glob('S*'):
            replay = (folder / 'REPLAY.md').read_text()
            self.assertIn('scripts/run_scenario.py', replay)
            self.assertIn(str(folder.relative_to(root)), replay)
            self.assertIn('No complete angband-recorder recording', replay)
            for name in ('README.md', 'report.md', 'inventory.md'):
                content = (folder / name).read_text()
                self.assertNotIn('"base_fail":', content)
                self.assertNotIn("'p_death':", content)
                self.assertNotIn('](scenario.json)', content)
        for name in ('D0005-recorded', 'D0006-recorded'):
            instructions = (root / 'deaths' / name / 'REPLAY.md').read_text()
            self.assertIn('replay-borg.py', instructions)
            self.assertIn('--verify-only', instructions)
            self.assertIn('tar -xJf', instructions)

    def test_saved_position_comparison_remains_bound_to_the_moved_save(self):
        import hashlib
        root = Path(__file__).resolve().parents[1] / 'scenarios/S0003'
        source = hashlib.sha256((root / 'scenario.json').read_bytes()).hexdigest()
        for role in ('baseline', 'candidate'):
            trial = json.loads((root / 'trials' / f'{role}-trial.json').read_text())
            self.assertEqual(trial['scenario_sha256'], source)
            self.assertEqual(trial['save_sha256'], json.loads((root / 'scenario.json').read_text())['save_sha256'])
