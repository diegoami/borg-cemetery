"""Frozen inputs and native receipts must agree before comparing outcomes."""
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import compare_encounters as c
from scenario_config import settings
from synthetic_suite import read, write


class ComparisonTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        for name in ('synthetic/fast-caster-encounters', 'studies/fast-caster-config'):
            shutil.copytree(ROOT / name, self.root / name)
        self.study = self.root / 'studies/fast-caster-config'
        self.definition = self.study / 'evidence/definition.json'
        self.output = self.study / 'evidence/attempt-2'
        self.cell = self.output / 'cells/earlier-heal/town-departure-priest-human-203'

    def tearDown(self):
        self.tmp.cleanup()

    def collect(self):
        return c.collect(self.definition, self.output, self.root)

    def test_real_native_receipts_qualify_and_freeze_roundtrips(self):
        result = self.collect()
        self.assertEqual([p['outcome'] for p in result['pairs']], ['both_survived'] * 4)
        self.assertEqual(c.freeze(self.study / 'study.json', self.root / 'frozen.json', self.root), read(self.definition))

    def test_changed_inputs_refused(self):
        (self.study / 'base-borg.txt').write_text('borg_param_caution_clw_min_loss = 5\n')
        with self.assertRaises(ValueError):
            self.collect()

    def test_copied_arm_is_invalid(self):
        path = self.cell / 'cell.json'
        row = read(path)
        row['arm'] = 'base'
        write(path, row)
        result = self.collect()
        self.assertEqual(result['pairs'][0]['outcome'], 'invalid')

    def test_changed_trial_or_raw_receipt_is_invalid(self):
        for name in ('trial.json', 'run/params-core.json', 'run/user/borg.txt', 'run/errands_plan.txt', 'run/state.log'):
            with self.subTest(name=name):
                path = self.cell / name
                original = path.read_bytes()
                path.write_text('{}\n' if name.endswith('.json') else 'changed\n')
                self.assertEqual(self.collect()['pairs'][0]['outcome'], 'invalid')
                path.write_bytes(original)

    def test_stale_definition_and_missing_cells_never_become_survivals(self):
        row = read(self.definition)
        row['id'] += '-new'
        write(self.definition, row)
        self.assertEqual(self.collect()['pairs'][0]['outcome'], 'invalid')
        (self.cell / 'cell.json').unlink()
        self.assertEqual(self.collect()['pairs'][0]['outcome'], 'missing')

    def test_survival_classification_is_bounded_and_unverified_flags_are_explicit(self):
        death, alive = dict(status='death'), dict(status='survived_horizon')
        self.assertEqual(c.classify_pair(death, alive), 'rescued')
        self.assertEqual(c.classify_pair(alive, death), 'newly_killed')
        self.assertEqual(c.classify_pair(death, alive, ['borg_worships_damage']), 'unverified_configuration')
        self.assertEqual(c.classify_pair(death, dict(status='timeout')), 'invalid')
        self.assertEqual(c.classify_pair(death, dict(status='stopped')), 'inconclusive')

    def test_duplicate_settings_refused(self):
        with self.assertRaises(ValueError):
            settings('borg_param_x = 1\nborg_param_x = 2\n')


if __name__ == '__main__':
    unittest.main()
