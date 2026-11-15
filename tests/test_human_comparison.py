import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from human_comparison import compare, archive_comparison, markdown


class HumanComparisonTest(unittest.TestCase):
    def setUp(self):
        self.scenario = dict(start_turn=100, original_endpoint_turn=200, race_idx=2, class_idx=1)
        self.rows = [dict(turn=t, hp=15, max_hp=15, level=2, race_idx=2, class_idx=1,
                          cheat_live=0, noscore=32, dead=0) for t in (100, 190, 210, 400)]

    def test_survival_beyond_original_death_is_descriptive_and_readable(self):
        result = compare(self.rows, self.scenario, save_captured=True, verified=True)
        self.assertTrue(result['beyond_original_death'])
        self.assertEqual(result['engine_ticks_beyond_original'], 200)
        self.assertIn('Survived beyond the original death turn 200', markdown(result))
        self.assertIn('15/15', markdown(result))

    def test_incomplete_or_nonordinary_evidence_cannot_claim_qualified_survival(self):
        for saved, verified in ((False, True), (True, False)):
            self.assertFalse(compare(self.rows, self.scenario, save_captured=saved, verified=verified)['beyond_original_death'])
        altered = [dict(r) for r in self.rows]
        altered[1]['cheat_live'] = 1
        self.assertFalse(compare(altered, self.scenario, save_captured=True, verified=True)['beyond_original_death'])
        altered[1]['cheat_live'] = 0
        altered[1]['noscore'] |= 2
        self.assertFalse(compare(altered, self.scenario, save_captured=True, verified=True)['beyond_original_death'])
        self.assertFalse(compare(self.rows[:2], self.scenario, save_captured=True, verified=True)['beyond_original_death'])

    def test_death_and_new_birth_cannot_count_as_the_same_surviving_life(self):
        rows = [self.rows[0], dict(self.rows[1], dead=1, hp=-1), dict(self.rows[0], turn=1), self.rows[-1]]
        self.assertFalse(compare(rows, self.scenario, save_captured=True, verified=True)['beyond_original_death'])

    def test_published_human_example_is_bound_to_the_start_and_verified_archive(self):
        root = Path(__file__).resolve().parents[1]
        entry = root / 'deaths/D0007/alternatives/human/20261115T004527-7541a0'
        result = archive_comparison(entry, "Fang, Farmer Maggot's Dog")
        self.assertTrue(result['beyond_original_death'])
        self.assertEqual(result['last_turn'], 4873)
        self.assertEqual(result['engine_ticks_beyond_original'], 1233)
        self.assertEqual(result['hp'], 15)
        self.assertFalse(result['original_cause_visible'])
        self.assertEqual(json.loads((entry / 'comparison.json').read_text()), result)


if __name__ == '__main__':
    unittest.main()
