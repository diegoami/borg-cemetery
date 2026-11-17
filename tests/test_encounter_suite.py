"""Fast smoke limits, encounter-start identity and complete failure accounting."""
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import encounter_suite as e
from synthetic_suite import sha, write


class EncounterTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.bank = self.root / 'synthetic/fast-caster-encounters'
        shutil.copytree(ROOT / 'synthetic/fast-caster-encounters', self.bank)
        self.path = self.bank / 'suite.json'
        self.manifest = json.loads(self.path.read_text())

    def tearDown(self):
        self.tmp.cleanup()

    def test_bounded_manifest_and_duplicate_cases(self):
        self.assertEqual(len(e.prepare(self.path, self.root)[1]), 4)
        for change in [dict(horizon_engine_turns=100000), dict(wall_seconds=120),
                       dict(scenarios=self.manifest['scenarios'] + [self.manifest['scenarios'][0]])]:
            write(self.path, dict(self.manifest, **change))
            with self.assertRaises(ValueError):
                e.prepare(self.path, self.root)

    def test_borg_rs_manifest_is_valid_but_requires_configured_execution(self):
        write(self.path,dict(self.manifest,core='borg-rs'))
        self.assertEqual(len(e.prepare(self.path,self.root)[1]),4)
        with self.assertRaisesRegex(ValueError,'explicit configured execution'):
            e.run_suite(self.path,self.root/'source',self.root/'out',root=self.root)

    def test_start_after_contact_or_tampered_save_is_rejected(self):
        entry = self.manifest['scenarios'][0]
        scenario = self.root / entry['scenario']
        value = json.loads(scenario.read_text())
        value['start_turn'] = value['selection']['trigger_turn'] + 1
        write(scenario, value)
        entry['sha256'] = sha(scenario)
        write(self.path, self.manifest)
        with self.assertRaisesRegex(ValueError, 'encounter onset'):
            e.prepare(self.path, self.root)
        value['start_turn'] = value['selection']['trigger_turn']
        write(scenario, value)
        entry['sha256'] = sha(scenario)
        write(self.path, self.manifest)
        (scenario.parent / value['save']).write_bytes(b'corrupt')
        with self.assertRaisesRegex(ValueError, 'hash mismatch'):
            e.prepare(self.path, self.root)

    def test_each_case_retained_after_failure_and_inherited_tuning_cleared(self):
        source = self.root / 'source'
        (source / 'engine').mkdir(parents=True)
        (source / 'engine/UPSTREAM').write_text('commit=' + self.manifest['engine_commit'] + '\n')
        calls = []
        def fake(source, scenario, dest, **kwargs):
            self.assertEqual(os.environ.get('BORG_CORE'), 'reborn')
            self.assertNotIn('BORG_PARAM_TEST', os.environ)
            self.assertNotIn('ANGBAND_RECORD_DIR', os.environ)
            calls.append(scenario)
            if len(calls) == 1:
                raise ValueError('deliberate first-case failure')
            write(dest / 'trial.json', dict(status='survived_horizon', summary={}))
            (dest / 'run').mkdir()
            data = json.loads((scenario / 'scenario.json').read_text())
            initial = data['initial_observed']
            (dest / 'run/state.log').write_text(f"{data['start_turn']} 0,0 d1/1 hp{initial['hp']}/{initial['max_hp']} sp{initial['sp']}/{initial['max_sp']}\n")
            for name in ('keys.log', 'messages.log'):
                (dest / 'run' / name).write_text('test stream\n')
            return 0
        with patch.dict(os.environ, BORG_PARAM_TEST='changed', ANGBAND_RECORD_DIR='unwanted'), patch(
                'encounter_suite.subprocess.check_output', return_value=self.manifest['baseline_source_commit'] + '\n'):
            result = e.run_suite(self.path, source, self.root / 'out', adapter=fake, root=self.root)
            self.assertEqual(os.environ['BORG_PARAM_TEST'], 'changed')
            self.assertEqual(os.environ['ANGBAND_RECORD_DIR'], 'unwanted')
        self.assertEqual(len(calls), 4)
        self.assertEqual(len(result['results']), 4)
        self.assertEqual(result['invalid_count'], 1)
        self.assertEqual(result['results'][0]['status'], 'harness_failure')


if __name__ == '__main__':
    unittest.main()
