"""A large bank keeps small shard limits, unique starts and complete accounting."""
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import encounter_bank as bank
from synthetic_suite import read, sha, write


class BankTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.base = self.root / 'synthetic/fast-caster-encounters'
        shutil.copytree(ROOT / 'synthetic/fast-caster-encounters', self.base)
        self.path = self.root / 'bank.json'
        self.value = dict(schema='borg-cemetery/encounter-bank@1', id='test', expected_cases=4,
                          shards=[dict(manifest=str((self.base / name).relative_to(self.root)), sha256=sha(self.base / name))
                                  for name in ('mage-suite.json', 'priest-suite.json')])
        write(self.path, self.value)

    def tearDown(self):
        self.tmp.cleanup()

    def test_small_shards_and_duplicate_or_wrong_denominator_rejected(self):
        self.assertEqual(len(bank.prepare_bank(self.path, self.root)[1]), 2)
        for change in (dict(expected_cases=5), dict(shards=self.value['shards'] * 2)):
            write(self.path, dict(self.value, **change))
            with self.assertRaises(ValueError):
                bank.prepare_bank(self.path, self.root)

    def test_failure_in_one_shard_does_not_skip_later_shards(self):
        success = dict(results=[dict(status='survived_horizon'), dict(status='death')], invalid_count=0, elapsed_seconds=0.2)
        with patch('encounter_bank.run_suite', side_effect=[ValueError('failure'), success]) as runner:
            result = bank.run_bank(self.path, self.root / 'source', self.root / 'out', self.root)
        self.assertEqual(runner.call_count, 2)
        self.assertEqual(result['expected_cases'], 4)
        self.assertEqual(result['invalid_count'], 2)
        self.assertEqual(result['completed_cases'], 2)

    def test_published_bank_has_hundreds_of_unique_qualified_starts(self):
        value, shards = bank.prepare_bank(ROOT / 'synthetic/caster-encounters-v2/bank.json', ROOT)
        self.assertGreaterEqual(value['expected_cases'], 200)
        self.assertEqual(sum(count for _, count in shards), value['expected_cases'])
        self.assertTrue(all(count <= 8 for _, count in shards))

    def test_indexing_references_does_not_require_game_execution(self):
        from index_encounters import index
        with tempfile.TemporaryDirectory(dir=ROOT) as tmp:
            output = Path(tmp) / 'fresh-index'
            index(ROOT / 'synthetic/caster-encounters-v2/all-cases.json',
                  ROOT / 'synthetic/fast-caster-encounters/suite.json', output, ROOT)
            value, _ = bank.prepare_bank(output / 'bank.json', ROOT)
            self.assertGreaterEqual(value['expected_cases'], 200)
            self.assertTrue((output / 'smoke-suite.json').exists())
            with self.assertRaises(ValueError):
                index(ROOT / 'synthetic/caster-encounters-v2/all-cases.json',
                      ROOT / 'synthetic/fast-caster-encounters/suite.json', output, ROOT)

    def test_mutated_shard_refused_before_execution(self):
        p = self.base / 'mage-suite.json'
        p.write_text(p.read_text() + ' ')
        with self.assertRaises(ValueError):
            bank.prepare_bank(self.path, self.root)


if __name__ == '__main__':
    unittest.main()
