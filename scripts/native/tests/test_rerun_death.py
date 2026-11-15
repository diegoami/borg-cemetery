"""tools/rerun-death.py (task TE.6, #76). Run: python3 -m unittest discover -s tools/tests"""

import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('rerun_death', HERE.parent / 'rerun-death.py')
rd = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rd)


def dossier(root, schema='borg-reborn-rs/death-record@1', impl='rust', flags='menu,exact', seed=102,
            summary_extra=None, config_extra='', keys_sha256='k' * 64):
    d = Path(root) / 'D0001-rust-seed102'
    d.mkdir()
    (d / 'record.json').write_text(json.dumps({
        'schema': schema, 'identity': {'impl': impl, 'seed': seed, 'flags': flags, 'source_sha256': 'abc', 'git_rev': 'f00'},
        'terminal': {'turn': 743, 'race_idx': 2, 'class_idx': 1},
        'attempts': [{'outcome': 'death', 'result_sha256': keys_sha256}]}))
    (d / 'summary.json').write_text(json.dumps({'seed': seed, 'race_idx': 2, 'class_idx': 1, 'game_turns': 743,
                                                **(summary_extra or {})}))
    (d / 'config.txt').write_text(f'flags={flags}\nborg_txt_sha256=x\nprofile=harness/profiles/reborn-default.txt\n'
                                  + config_extra)
    return d


class PlanTest(unittest.TestCase):
    def test_a_dossier_gives_the_same_run(self):
        with tempfile.TemporaryDirectory() as t:
            p = rd.plan(dossier(t))
        self.assertEqual((p['seed'], p['race'], p['class']), (102, 2, 1))
        self.assertEqual(p['cap'], 744, 'the death comes before the cap')
        self.assertEqual(p['flags'], 'menu', 'no exact stop: the game ends at the death')
        self.assertEqual(p['profile'], 'harness/profiles/reborn-default.txt')
        self.assertEqual(p['keys_sha256'], 'k' * 64)

    def test_the_runs_settings_come_back(self):
        # Review #227, finding 8: an errand run reruns as itself.
        with tempfile.TemporaryDirectory() as t:
            p = rd.plan(dossier(t, config_extra='borg_core=borg-rs\nborg_errand=/dive 3; /walk-back\n'
                                                 'borg_stopscared=50\n'))
        self.assertEqual(p['env'], {'BORG_CORE': 'borg-rs', 'BORG_ERRAND': '/dive 3; /walk-back',
                                    'BORG_STOPSCARED': '50'})
        with tempfile.TemporaryDirectory() as t:
            self.assertEqual(rd.plan(dossier(t))['env'], {}, 'a run without settings has none')
        with tempfile.TemporaryDirectory() as t:
            p = rd.plan(dossier(t, config_extra='borg_errand=\n'))
        self.assertEqual(p['env'], {'BORG_ERRAND': ''}, 'set but empty stays set')

    def test_a_changed_ladders_file_is_refused(self):
        with tempfile.TemporaryDirectory() as t:
            ladders = Path(t) / 'ladders.txt'
            ladders.write_text('warrior = trips:1*\n')
            good = rd.hashlib.sha256(ladders.read_bytes()).hexdigest()
            p = rd.plan(dossier(t, config_extra=f'borg_ladders={ladders}\nborg_ladders_sha256={good}\n'))
            self.assertEqual(p['env']['BORG_LADDERS'], str(ladders))
            ladders.write_text('warrior = trips:1,2*\n')
            (Path(t) / 'D0001-rust-seed102').rename(Path(t) / 'old')
            with self.assertRaises(SystemExit):
                rd.plan(dossier(t, config_extra=f'borg_ladders={ladders}\nborg_ladders_sha256={good}\n'))

    def test_a_plan_is_restored_from_the_source_checkout(self):
        # Issue #3: a plan run reruns with the plan config.txt names, resolved
        # like run.sh recorded it: relative to the source checkout.
        with tempfile.TemporaryDirectory() as t:
            src = Path(t) / 'src'
            plan_file = src / 'harness/plans/errands_plan_ambitious.txt'
            plan_file.parent.mkdir(parents=True)
            plan_file.write_text('/dive 3\n')
            good = rd.hashlib.sha256(plan_file.read_bytes()).hexdigest()
            d = dossier(t, config_extra='borg_errands_plan=harness/plans/errands_plan_ambitious.txt\n'
                                        f'borg_errands_plan_sha256={good}\n')
            with mock.patch.object(rd, 'ROOT', src):
                p = rd.plan(d)
        self.assertEqual(p['env']['BORG_ERRANDS_PLAN'], str(plan_file))

    def test_an_absolute_plan_path_is_used_as_recorded(self):
        with tempfile.TemporaryDirectory() as t:
            plan_file = Path(t) / 'plan.txt'
            plan_file.write_text('/dive 3\n')
            good = rd.hashlib.sha256(plan_file.read_bytes()).hexdigest()
            p = rd.plan(dossier(t, config_extra=f'borg_errands_plan={plan_file}\n'
                                                f'borg_errands_plan_sha256={good}\n'))
        self.assertEqual(p['env']['BORG_ERRANDS_PLAN'], str(plan_file))

    def test_a_dossier_copy_of_the_plan_is_used(self):
        # export-death.py keeps the plan, so its bytes win over the source
        # checkout's copy (which need not exist any more).
        with tempfile.TemporaryDirectory() as t:
            plan = '/dive 3\n'
            good = rd.hashlib.sha256(plan.encode()).hexdigest()
            d = dossier(t, config_extra='borg_errands_plan=harness/plans/gone.txt\n'
                                        f'borg_errands_plan_sha256={good}\n')
            (d / 'errands_plan.txt').write_text(plan)
            p = rd.plan(d)
        self.assertEqual(p['env']['BORG_ERRANDS_PLAN'], str(d / 'errands_plan.txt'))

    def test_a_changed_plan_is_refused(self):
        with tempfile.TemporaryDirectory() as t:
            plan_file = Path(t) / 'plan.txt'
            plan_file.write_text('/dive 3\n')
            good = rd.hashlib.sha256(plan_file.read_bytes()).hexdigest()
            config = f'borg_errands_plan={plan_file}\nborg_errands_plan_sha256={good}\n'
            self.assertEqual(rd.plan(dossier(t, config_extra=config))['env']['BORG_ERRANDS_PLAN'], str(plan_file))
            plan_file.write_text('/dive 4\n')
            (Path(t) / 'D0001-rust-seed102').rename(Path(t) / 'old')
            with self.assertRaises(SystemExit) as e:
                rd.plan(dossier(t, config_extra=config))
        self.assertIn('the run read errands plan', str(e.exception))

    def test_a_missing_plan_is_refused(self):
        with tempfile.TemporaryDirectory() as t:
            config = f'borg_errands_plan={Path(t) / "gone.txt"}\nborg_errands_plan_sha256={"a" * 64}\n'
            with self.assertRaises(SystemExit) as e:
                rd.plan(dossier(t, config_extra=config))
        self.assertIn('missing', str(e.exception))

    def test_the_rerun_sets_the_plan(self):
        with tempfile.TemporaryDirectory() as t:
            base = Path(t)
            src = base / 'src'
            (src / 'build/rust').mkdir(parents=True)
            (src / 'build/rust/BUILD_ID').write_text('source_sha256=abc\n')
            plan_file = src / 'harness/plans/p.txt'
            plan_file.parent.mkdir(parents=True)
            plan_file.write_text('/dive 3\n')
            good = rd.hashlib.sha256(plan_file.read_bytes()).hexdigest()
            keys = b'keys\n'
            d = dossier(base, keys_sha256=rd.hashlib.sha256(keys).hexdigest(),
                        config_extra=f'borg_errands_plan=harness/plans/p.txt\n'
                                     f'borg_errands_plan_sha256={good}\n')
            calls = {}

            def fake_run(cmd, **kwargs):
                calls['env'] = kwargs['env']
                run = Path(cmd[1])
                run.mkdir()
                (run / 'keys.log').write_bytes(keys)
                (run / 'summary.json').write_text('{}')
                for name in ('observations.jsonl', 'worlds.txt', 'knowledge.json'):
                    (run.parent / name).write_text('x')
                return subprocess.CompletedProcess(cmd, 0, '', '')

            # run.sh hashes the regenerated borg.txt, so the plan must be set
            # on the call, not only known to the dossier.
            with mock.patch.object(rd, 'ROOT', src), mock.patch.object(rd.subprocess, 'run', fake_run):
                self.assertEqual(rd.main([str(d), str(base / 'out')]), 0)
        self.assertEqual(calls['env']['BORG_ERRANDS_PLAN'], str(plan_file))

    def test_only_rust_harness_dossiers(self):
        with tempfile.TemporaryDirectory() as t:
            with self.assertRaises(SystemExit):
                rd.plan(dossier(t, schema='borg-rs/death-record@1'))
        with tempfile.TemporaryDirectory() as t:
            with self.assertRaises(SystemExit):
                rd.plan(dossier(t, impl='c-pristine'))
        with tempfile.TemporaryDirectory() as t:
            with self.assertRaises(SystemExit):
                rd.plan(dossier(t, flags='save=x.save,keep-load-rng'))

    def test_a_load_through_the_extra_options_is_refused(self):
        # E review, finding 4: run.sh -- -load FILE has flags=-.
        with tempfile.TemporaryDirectory() as t:
            with self.assertRaises(SystemExit):
                rd.plan(dossier(t, flags='-', config_extra='save_sha256=ab\n'))
        with tempfile.TemporaryDirectory() as t:
            with self.assertRaises(SystemExit):
                rd.plan(dossier(t, flags='-', summary_extra={'loaded': True}))

    def test_another_build_is_refused(self):
        with tempfile.TemporaryDirectory() as t:
            d = dossier(t)
            with self.assertRaises(SystemExit) as e:
                rd.main([str(d), str(Path(t) / 'out')])
            self.assertIn('check out f00', str(e.exception))


if __name__ == '__main__':
    unittest.main()
