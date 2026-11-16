"""Synthetic suite contracts with a fake execution adapter, never game saves."""
import copy
import json
import os
import signal
import subprocess
from pathlib import Path
import sys
import tempfile
import time
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import synthetic_suite as s


class FakeAdapter:
    def __init__(self, mode='survived_to_cap'):
        self.mode = mode
        self.calls = []

    def describe(self, commit, contracts, cores=()):
        if self.mode == 'unsupported':
            raise s.ExecutionError('unsupported', 'capability absent')
        return dict(repository='diegoami/borg-reborn-rs', commit=commit, contracts=sorted(contracts),
                    capabilities_sha256='d' * 64,
                    build=dict(impl='rust', git_rev=commit, git_dirty='no', inputs_dirty='no',
                               binary_sha256='b' * 64, source_sha256='c' * 64))

    def run(self, case, root, output):
        self.calls.append(case)
        self_assert = not any('save' in key or 'load' in key for key in case)
        if not self_assert:
            raise AssertionError('suite acquired a save dependency')
        output.mkdir()
        build = case['character_build']
        summary = dict(synthetic=True, loaded=False, seed=case['seed'], race_idx=build['race_idx'], class_idx=build['class_idx'],
                       start_depth=case['depth'], initial_depth=case['depth'], initial_clevel=1,
                       initial_cave_depth=case['depth'], initial_generation_pending=False,
                       synthetic_contract=case['harness_contract'], start_build=build['start'], dungeon_mode='one_way',
                       game_options=dict(birth_force_descend=True, birth_no_recall=True),
                       dead=self.mode == 'death', stop_reason='death' if self.mode == 'death' else 'turns',
                       death_cause='a test monster' if self.mode == 'death' else '', game_turns=case['turn_cap'], keys=2)
        process = dict(status='success', exit_code=0, timed_out=False,
                       executable_sha256_before='b' * 64, executable_sha256_after='b' * 64)
        if self.mode == 'identity_mismatch':
            summary['start_depth'] += 1
        if self.mode == 'timeout':
            process.update(status='timeout', timed_out=True)
        if self.mode == 'harness_failure':
            summary.update(dead=True, stop_reason='death')
            process.update(status='failed', exit_code=1)
        if self.mode == 'stopped':
            summary.update(stop_reason='borg_stopped', game_turns=20)
        if self.mode == 'short':
            summary.update(game_turns=20)
        if self.mode == 'contradictory':
            summary.update(dead=True, stop_reason='turns')
        s.write(output / 'summary.json', [] if self.mode == 'malformed' else summary)
        s.write(output / 'process.json', process)
        config = dict(synthetic='1', start_depth=str(case['depth']), start_build=build['start'],
                      borg_core=build['core'],
                      synthetic_contract=case['harness_contract'], dungeon_mode='one_way', profile_sha256=build['profile_sha256'])
        (output / 'config.txt').write_text(''.join(f'{k}={v}\n' for k, v in config.items()))
        (output / 'messages.log').write_text('0 1 0 Nothing happens.\n1 2 0 Nothing happens!\n2 3 0 Borg note: Nothing happens.\n')
        (output / 'keys.log').write_text('1 1 6b 0\n2 2 6c 0\n')
        if self.mode != 'missing':
            (output / 'state.log').write_text(f"1 1,1 d{case['depth']}/{case['depth']} hp1/20 sp0/0 f100\n"
                                             f"2 1,1 d{case['depth']}/{case['depth']} hp10/20 sp0/0 f100\n")
        if self.mode == 'bad_state':
            (output / 'state.log').write_text('truncated\n')
        if self.mode == 'pollution':
            (output.parent / 'natural-registry-guard').mkdir()
        return 124 if self.mode == 'timeout' else 1 if self.mode == 'harness_failure' else 0


class SuiteTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.profile = self.root / 'profile.txt'
        self.profile.write_text('# effective defaults pinned by source\n')
        self.manifest = dict(schema=s.SCHEMA, suite_id='test-suite', revision=1,
                             seeds=[102, 101], depths=[10, 5], turn_cap=100, wall_seconds=5,
                             candidate_screen=dict(kind='low_hp_candidate', hp_threshold=2),
                             character_builds=[dict(id='birth', race_idx=0, class_idx=0, core='reborn', start='birth',
                                                    profile='profile.txt', profile_sha256=s.sha(self.profile))],
                             runtime=dict(repository='diegoami/borg-reborn-rs', commit='a' * 40))
        self.path = self.root / 'suite.json'
        self.save()

    def tearDown(self):
        self.tmp.cleanup()

    def save(self):
        s.write(self.path, self.manifest)

    def test_canonical_identity_ignores_executable_selection_and_grid_order(self):
        original = s.generate(self.path)
        self.manifest['runtime']['commit'] = 'b' * 40
        self.manifest['seeds'].reverse()
        self.manifest['depths'].reverse()
        self.save()
        changed = s.generate(self.path)
        self.assertEqual(original['cases'], changed['cases'])
        self.assertEqual(original['suite_spec_sha256'], changed['suite_spec_sha256'])
        self.assertNotEqual(original['manifest_sha256'], changed['manifest_sha256'])
        self.assertEqual(len({row['id'] for row in original['cases']}), 4)
        self.assertFalse(any('save' in key for row in original['cases'] for key in row))
        self.assertEqual(s.canonical(original['cases']), s.canonical(s.generate(self.path)['cases']))

    def test_invalid_or_ambiguous_definitions_fail_before_execution(self):
        edits = [lambda m: m.update(seeds=[1, 1]), lambda m: m.update(depths=[True]),
                 lambda m: m.update(turn_cap=0), lambda m: m.update(wall_seconds=0),
                 lambda m: m.update(character_builds=[]),
                 lambda m: m['character_builds'].append(copy.deepcopy(m['character_builds'][0])),
                 lambda m: m['character_builds'][0].update(start='record'),
                 lambda m: m['character_builds'][0].update(profile='../elsewhere'),
                 lambda m: m['candidate_screen'].update(kind='near_death'),
                 lambda m: m['runtime'].update(commit='main'),
                 lambda m: m.update(suite_id=42),
                 lambda m: m.update(seeds=list(range(32)), depths=list(range(1, 33)))]
        original = copy.deepcopy(self.manifest)
        for edit in edits:
            with self.subTest(edit=edit):
                self.manifest = copy.deepcopy(original)
                edit(self.manifest)
                self.save()
                with self.assertRaises(ValueError):
                    s.generate(self.path)
        self.manifest = original
        self.save()
        self.profile.write_text('changed input\n')
        with self.assertRaisesRegex(ValueError, 'hash mismatch'):
            s.generate(self.path)

    def test_duplicate_json_keys_are_rejected(self):
        self.path.write_text('{"schema":"a","schema":"b"}')
        with self.assertRaisesRegex(ValueError, 'duplicate'):
            s.generate(self.path)

    def test_core_profiles_cannot_silently_ignore_named_overrides(self):
        self.manifest['character_builds'][0]['core'] = 'borg-rs'
        self.save()
        self.assertEqual(len(s.generate(self.path)['cases']), 4)
        self.profile.write_text('max_tries_per_turn = 4\n')
        self.manifest['character_builds'][0]['profile_sha256'] = s.sha(self.profile)
        self.save()
        with self.assertRaisesRegex(ValueError, 'explicit defaults only'):
            s.generate(self.path)

    def test_retained_comparison_detects_changed_streams_and_incomplete_cases(self):
        actual = s.run_suite(self.path, self.root, self.root / 'comparison', adapter=FakeAdapter())
        expected = copy.deepcopy(actual)
        self.assertEqual(s.verify_results(actual, expected), 4)
        for mutation in ('keys', 'state', 'messages', 'missing_digest', 'missing_case',
                         'duplicate_case', 'status', 'runtime', 'near_death', 'source',
                         'manifest', 'death_cause', 'minimum_hp'):
            changed = copy.deepcopy(actual)
            row = changed['results'][0]
            if mutation in ('keys', 'state', 'messages'):
                row['evidence'][mutation + '.log']['sha256'] = '0' * 64
            elif mutation == 'missing_digest':
                del row['evidence']['keys.log']
            elif mutation == 'missing_case':
                changed['results'].pop()
            elif mutation == 'duplicate_case':
                changed['results'][1] = copy.deepcopy(row)
            elif mutation == 'status':
                row['status'] = 'death'
            elif mutation == 'near_death':
                row['qualified_near_death'] = dict(count=0)
            elif mutation == 'source':
                changed['build_identity']['build']['source_sha256'] = 'e' * 64
            elif mutation == 'manifest':
                changed['manifest_sha256'] = 'e' * 64
            elif mutation == 'death_cause':
                row['death_cause'] = 'changed'
            elif mutation == 'minimum_hp':
                row['minimum_observed_living_hp'] = 123
            else:
                changed['requested_runtime']['commit'] = '0' * 40
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                s.verify_results(changed, expected)
        changed = copy.deepcopy(actual)
        for row in changed['results']:
            row['qualified_near_death'] = dict(coverage='unavailable', count=0)
        with self.assertRaisesRegex(ValueError, 'unavailable/null'):
            s.verify_results(changed, changed)

    def test_identity_and_key_log_receipts_cannot_be_bypassed(self):
        case = s.generate(self.path)['cases'][0]
        output = self.root / 'receipts'
        FakeAdapter().run(case, self.root, output)
        self.assertEqual(s.classify(case, output, 0, 'b' * 64)['status'], 'survived_to_cap')
        for digest in (None, '', False, 'a' * 64):
            with self.subTest(digest=digest):
                self.assertEqual(s.classify(case, output, 0, digest)['status'], 'identity_mismatch')
        process = s.read(output / 'process.json')
        for key in ('executable_sha256_before', 'executable_sha256_after'):
            s.write(output / 'process.json', dict(process, **{key: 'e' * 64}))
            self.assertEqual(s.classify(case, output, 0, 'b' * 64)['status'], 'identity_mismatch')
        s.write(output / 'process.json', dict(process, timed_out='false'))
        self.assertEqual(s.classify(case, output, 0, 'b' * 64)['status'], 'harness_failure')
        s.write(output / 'process.json', process)
        summary = s.read(output / 'summary.json')
        s.write(output / 'summary.json', dict(summary, game_turns=10**30))
        self.assertEqual(s.classify(case, output, 0, 'b' * 64)['status'], 'identity_mismatch')
        s.write(output / 'summary.json', summary)
        (output / 'keys.log').unlink()
        self.assertEqual(s.classify(case, output, 0, 'b' * 64)['status'], 'harness_failure')
        (output / 'keys.log').write_text('1 1 6b 0\n')
        self.assertEqual(s.classify(case, output, 0, 'b' * 64)['status'], 'identity_mismatch')

    def test_outer_timeout_kills_engine_grandchildren(self):
        pidfile = self.root / 'grandchild.pid'
        # A real launcher + child process exercises cleanup, rather than
        # mocking TimeoutExpired while leaving process ownership untested.
        code = ('import pathlib, subprocess, sys; '
                'child=subprocess.Popen([sys.executable,"-c","import time; time.sleep(60)"]); '
                'pathlib.Path(sys.argv[1]).write_text(str(child.pid)); child.wait()')
        with (self.root / 'timeout.log').open('wb') as log:
            self.assertEqual(s.run_bounded([sys.executable, '-c', code, str(pidfile)],
                                          self.root, os.environ.copy(), log, 1), 124)
        pid = int(pidfile.read_text())
        status = Path(f'/proc/{pid}/stat')
        # A killed child can briefly await its init reaper as a zombie.
        deadline = time.monotonic() + 2
        while True:
            try:
                state = status.read_text().split(') ', 1)[1][0]
            except FileNotFoundError:
                break
            if state in ('Z', 'X'):
                break
            if time.monotonic() >= deadline:
                self.fail(f'grandchild {pid} is still running after group timeout')
            time.sleep(0.01)

    def test_interrupted_runner_cleans_its_separate_process_group(self):
        pidfile = self.root / 'cancelled.pid'
        child_code = ('import pathlib, subprocess, sys; '
                      'child=subprocess.Popen([sys.executable,"-c","import time;time.sleep(60)"]); '
                      'pathlib.Path(sys.argv[1]).write_text(str(child.pid)); child.wait()')
        code = ('import os, signal, sys; '
                'sys.path.insert(0,sys.argv[1]); import synthetic_suite as s; '
                'signal.signal(signal.SIGTERM,s.terminate); '
                's.run_bounded([sys.executable,"-c",sys.argv[2],sys.argv[3]],'
                'os.getcwd(),os.environ.copy(),sys.stdout,60)')
        worker = subprocess.Popen([sys.executable, '-c', code, str(Path(s.__file__).parent),
                                   child_code, str(pidfile)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        try:
            deadline = time.monotonic() + 5
            while not pidfile.exists() and time.monotonic() < deadline:
                time.sleep(0.01)
            self.assertTrue(pidfile.exists(), 'worker failed to start the grandchild')
            worker.send_signal(signal.SIGTERM)
            self.assertEqual(worker.wait(timeout=5), 128 + signal.SIGTERM)
            status = Path(f'/proc/{int(pidfile.read_text())}/stat')
            deadline = time.monotonic() + 2
            while True:
                try:
                    state = status.read_text().split(') ', 1)[1][0]
                except FileNotFoundError:
                    break
                if state in ('Z', 'X'):
                    break
                if time.monotonic() >= deadline:
                    self.fail('cancelled runner left its grandchild running')
                time.sleep(0.01)
        finally:
            if worker.poll() is None:
                worker.kill()
            worker.wait()

    def test_outcomes_failures_and_unknown_qualification_are_independent(self):
        for mode, expected in [('death', 'death'), ('survived_to_cap', 'survived_to_cap'),
                               ('stopped', 'stopped'), ('short', 'stopped'), ('timeout', 'timeout'),
                               ('harness_failure', 'harness_failure'), ('identity_mismatch', 'identity_mismatch'),
                               ('missing', 'harness_failure'), ('malformed', 'harness_failure'),
                               ('bad_state', 'identity_mismatch'), ('pollution', 'harness_failure'),
                               ('contradictory', 'harness_failure')]:
            with self.subTest(mode=mode):
                adapter = FakeAdapter(mode)
                result = s.run_suite(self.path, self.root, self.root / mode, adapter=adapter)
                self.assertEqual({row['status'] for row in result['results']}, {expected})
                self.assertEqual(result['attempted_count'], 4)
                self.assertEqual(sum(row['denominator'] for row in result['aggregates']), 4)
                self.assertEqual(len(adapter.calls), 4)
                for row in result['results']:
                    self.assertEqual(row['qualified_near_death'], dict(coverage='unavailable', count=None, reason='P1 has no null-move evaluator'))
                    if mode in ('death', 'survived_to_cap'):
                        self.assertEqual(row['candidate_screen']['count'], 1)
                        self.assertEqual(row['refusal_messages']['nothing_happens_dot'], 1)
                        self.assertEqual(row['refusal_messages']['nothing_happens_bang'], 1)
                    if expected in s.FAILURES:
                        self.assertIsNone(row['terminal'])
                if mode == 'death':
                    self.assertEqual(result['death_causes'], {'a test monster': 4})
                if mode == 'missing':
                    self.assertEqual(len(result['missing_evidence']), 4)

    def test_unsupported_preflight_preserves_denominators_without_fake_attempts(self):
        adapter = FakeAdapter('unsupported')
        result = s.run_suite(self.path, self.root, self.root / 'unsupported', adapter=adapter)
        self.assertEqual(result['counts'], {'unsupported': 4})
        self.assertEqual(result['attempted_count'], 0)
        self.assertEqual(adapter.calls, [])
        self.assertIsNone(result['build_identity'])
        self.assertIn('Attempted 0 / 4', (self.root / 'unsupported/report.md').read_text())

    def test_existing_results_are_not_overwritten(self):
        out = self.root / 'results'
        s.run_suite(self.path, self.root, out, adapter=FakeAdapter())
        before = (out / 'results.json').read_bytes()
        with self.assertRaises(FileExistsError):
            s.run_suite(self.path, self.root, out, adapter=FakeAdapter())
        self.assertEqual(before, (out / 'results.json').read_bytes())


if __name__ == '__main__':
    unittest.main()

class CatalogTest(unittest.TestCase):
    def test_catalog_requires_the_ordinary_capture_and_binary_receipts(self):
        from unittest.mock import patch
        fixture = Path(__file__).resolve().parents[1] / 'synthetic/p1-warrior/warrior-level5.build'
        projection = s.build_record(fixture)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source, run = root / 'source', root / 'run'
            (source / 'build/rust').mkdir(parents=True)
            run.mkdir()
            build = source / 'build/rust/BUILD_ID'
            build.write_text('impl=rust\ngit_rev=' + 'a'*40 + '\ninputs_dirty=no\ngit_dirty=no\nsource_sha256=' + 'c'*64 + '\nbinary_sha256=' + 'b'*64 + '\n')
            summary = dict(seed=101, race_idx=0, class_idx=0, game_turns=20000, synthetic=False, loaded=False, build_capture_sha256=s.sha(fixture),
                           build_capture_level=projection['identity'][2], build_capture_turn=projection['observed'][0])
            s.write(run / 'summary.json', summary)
            s.write(run / 'process.json', dict(status='success', exit_code=0, executable_sha256_before='b'*64, executable_sha256_after='b'*64))
            for name in ('keys.log', 'state.log', 'config.txt'):
                (run / name).write_text('test observation receipt\n')
            with patch.object(s.RebornAdapter, 'describe', return_value=dict(commit='a'*40)):
                value = s.catalog(fixture, run, source, root / 'catalog.json')
                self.assertEqual(value['sample_count'], 1)
                self.assertEqual(value['record_sha256'], s.sha(fixture))
                self.assertIn('not a population average', value['limitations'][0])
                self.assertEqual(value['projection'], projection)
                for change in ({'synthetic': True}, {'loaded': True}, {'build_capture_sha256': 'c'*64}, {'build_capture_level': 6}):
                    s.write(run / 'summary.json', dict(summary, **change))
                    with self.assertRaisesRegex(ValueError, 'capture receipt'):
                        s.catalog(fixture, run, source, root / 'bad.json')
                s.write(run / 'summary.json', summary)
                s.write(run / 'process.json', dict(status='success', exit_code=0, executable_sha256_before='c'*64, executable_sha256_after='b'*64))
                with self.assertRaisesRegex(ValueError, 'binary/process'):
                    s.catalog(fixture, run, source, root / 'bad.json')
                build.write_text('inputs_dirty=yes\ngit_dirty=no\n')
                with self.assertRaisesRegex(ValueError, 'clean measured build'):
                    s.catalog(fixture, run, source, root / 'bad.json')
