import gzip
import hashlib
import json
from pathlib import Path
import unittest


class AnalysisResultsTest(unittest.TestCase):
    def test_frozen_profiles_results_and_logs_agree(self):
        case = Path(__file__).resolve().parents[1] / 'deaths/D0007'
        base = {p['name']: p['value'] for p in json.loads((case / 'params.json').read_text())['parameters']}
        plan = json.loads((case / 'analysis-profiles/plan.json').read_text())
        results = json.loads((case / 'analysis-results/results.json').read_text())
        expected = {arm['name']: arm['override'] for arm in plan['arms']}
        self.assertEqual(set(expected), {row['name'] for row in results})
        binaries = set()
        for row in results:
            folder = case / 'analysis-results' / row['name']
            trial = json.loads((folder / 'trial.json').read_text())
            params = json.loads((folder / 'params.json').read_text())['parameters']
            changed = {p['name']: p['value'] for p in params if p['value'] != base[p['name']]}
            self.assertEqual(changed, expected[row['name']])
            self.assertEqual(trial['source_commit'], plan['source_commit'])
            self.assertEqual(trial['start_turn'], 3402)
            self.assertEqual(trial['horizon_engine_turns'], 1000)
            binaries.add(trial['build']['binary_sha256'])
            self.assertEqual(row['status'], trial['status'])
            self.assertEqual(row['turn'], trial['summary']['game_turns'])
            self.assertFalse(row['independent_birth'])
            hashes = json.loads((folder / 'evidence-hashes.json').read_text())
            for name, expected_hash in hashes.items():
                data = gzip.decompress((folder / (name + '.gz')).read_bytes())
                self.assertEqual(hashlib.sha256(data).hexdigest(), expected_hash)
            with gzip.open(folder / 'trace.jsonl.gz', 'rt') as stream:
                violations = sum(len(json.loads(line).get('violations', [])) for line in stream)
            self.assertEqual(row['trace_violations'], violations)
        self.assertEqual(len(binaries), 1)
        rest = next(r for r in results if r['name'] == 'rest-1')
        self.assertEqual(rest['trace_violations'], 4)


if __name__ == '__main__':
    unittest.main()
