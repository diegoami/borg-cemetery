"""Replay must restore policy provenance and fail closed on incomplete evidence."""
import copy
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest import mock

from test_rerun_death import rd, dossier


class ReplayConfigurationTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.source = self.root / 'source'
        binary = self.source / 'build/rust/game/angband'
        binary.parent.mkdir(parents=True)
        binary.write_bytes(b'original executable')
        (binary.parent.parent / 'BUILD_ID').write_text('source_sha256=abc\n')
        self.case = dossier(self.root, config_extra='borg_core=borg-rs\n')
        self.borg = b'borg_param_file_setting = 17\n'
        self.streams = {name: (name + '\n').encode()
                        for name in ('keys.log', 'state.log', 'messages.log')}
        self.params = [
            dict(name='environment_setting', value=23, origin='environment'),
            dict(name='file_setting', value=17, origin='borg.txt'),
            dict(name='default_setting', value=11, origin='default', class_values={
                'mage': dict(value=31, origin='environment'),
                'warrior': dict(value=37, origin='borg.txt')}),
        ]
        self.summary = dict(seed=102, race_idx=2, class_idx=1, dead=True, loaded=False,
                            stop_reason='death', game_turns=743, death_cause='orc',
                            clevel=3, depth=1, max_depth=2)
        self.record = json.loads((self.case / 'record.json').read_text())
        self.record['identity']['binary_sha256'] = rd.sha(binary)
        self.record['terminal'].update(cause='orc', level=3, depth=1, max_depth=2, dead=True)
        self.record['attempts'] = [dict(role='original', result_sha256=self.digest(self.streams['keys.log']),
                                      raw_sha256={n: self.digest(b) for n, b in self.streams.items()})]
        self.config = rd.read_kv(self.case / 'config.txt')
        self.config['borg_txt_sha256'] = self.digest(self.borg)
        self.save_params()
        self.env = None

    @staticmethod
    def digest(data):
        return rd.hashlib.sha256(data).hexdigest()

    def save_params(self):
        (self.case / 'params-core.json').write_text(json.dumps(self.params) + '\n')
        self.config['params_core_sha256'] = rd.sha(self.case / 'params-core.json')
        self.record['identity']['params_core_sha256'] = self.config['params_core_sha256']
        self.save_record()

    def save_record(self):
        (self.case / 'config.txt').write_text(''.join(f'{k}={v}\n' for k, v in self.config.items()))
        self.record['files_sha256'] = {name: rd.sha(self.case / name)
                                       for name in ('config.txt', 'summary.json', 'params-core.json')
                                       if (self.case / name).exists()}
        (self.case / 'record.json').write_text(json.dumps(self.record))

    def output(self, cmd, **kwargs):
        self.env = kwargs['env']
        run = Path(cmd[1])
        (run / 'user').mkdir(parents=True)
        (run / 'user/borg.txt').write_bytes(self.borg)
        (run / 'config.txt').write_bytes((self.case / 'config.txt').read_bytes())
        for name, data in self.streams.items():
            (run / name).write_bytes(data)
        (run / 'summary.json').write_text(json.dumps(self.summary))
        # The core the plan resolves, not the config's own borg_core: a
        # record that names no controller still plays one core or the other.
        if rd.plan(self.case)['core'] == 'borg-rs':
            (run / 'params-core.json').write_bytes((self.case / 'params-core.json').read_bytes())
            (run / 'trace-core.jsonl').write_text('{"check":"attack"}\n')
        else:
            for name in ('observations.jsonl', 'worlds.txt', 'knowledge.json'):
                (run.parent / name).write_text('reborn log\n')
        return subprocess.CompletedProcess(cmd, 0, '', '')

    def execute(self, mutate=None, extra=()):
        out = self.root / 'out'
        def launch(cmd, **kwargs):
            result = self.output(cmd, **kwargs)
            if mutate:
                mutate(out)
            return result
        with mock.patch.object(rd, 'ROOT', self.source), mock.patch.object(rd.subprocess, 'run', launch):
            rc = rd.main([str(self.case), str(out), *extra])
        return rc, json.loads((out / 'reproduction.json').read_text())

    def test_zoo_pborg_config_must_match_recorded_yaml_before_staging(self):
        run = self.root / 'run'
        (run / 'user').mkdir(parents=True)
        yaml = b'borg_param_file_setting: 17\n'
        with mock.patch.object(rd.subprocess, 'check_output', return_value=yaml) as convert:
            with self.assertRaisesRegex(SystemExit, 'pborg.yaml differs'):
                rd.stage_zoo_config(run, self.borg.decode(), 'wrong-hash')
            self.assertEqual(list((run / 'user').iterdir()), [])
            rd.stage_zoo_config(run, self.borg.decode(), self.digest(yaml))
        self.assertEqual(convert.call_args.kwargs['input'], self.borg)
        self.assertEqual((run / 'user/pborg.yaml').read_bytes(), yaml)
        self.assertEqual((run / 'pborg-legacy.txt').read_bytes(), self.borg)
        self.assertFalse((run / 'user/borg.txt').exists())

    def test_native_replay_restores_environment_and_class_origins_only(self):
        with mock.patch.dict(os.environ, BORG_PARAM_AMBIENT='99', BORG_CORE='reborn',
                             BORG_TXT_SET='bad=1', BORG_SCARY_LIST='/unrelated',
                             BORG_PROFILE='/unrelated', BORG_CORE_TRACE='off',
                             ANGBAND_BIN='/other/game', ANGBAND_RECORD_DIR='/unrelated'):
            rc, receipt = self.execute()
        self.assertEqual(rc, 0)
        self.assertTrue(receipt['reproduction_verified'])
        self.assertEqual(receipt['status'], 'reproduced')
        self.assertEqual(self.env['BORG_CORE'], 'borg-rs')
        self.assertEqual(self.env['BORG_PARAM_ENVIRONMENT_SETTING'], '23')
        self.assertEqual(self.env['BORG_PARAM_DEFAULT_SETTING__MAGE'], '31')
        self.assertNotIn('BORG_PARAM_FILE_SETTING', self.env)
        self.assertNotIn('BORG_PARAM_DEFAULT_SETTING', self.env)
        self.assertNotIn('BORG_PARAM_DEFAULT_SETTING__WARRIOR', self.env)
        for key in ('BORG_PARAM_AMBIENT', 'BORG_TXT_SET', 'BORG_SCARY_LIST',
                    'BORG_CORE_TRACE', 'ANGBAND_BIN', 'ANGBAND_RECORD_DIR', 'BORG_WORLD_LOG'):
            self.assertNotIn(key, self.env)
        self.assertNotEqual(self.env['BORG_PROFILE'], '/unrelated')

    def test_historical_missing_controller_is_reborn_even_with_native_ambient_default(self):
        del self.config['borg_core']
        del self.config['params_core_sha256']
        del self.record['identity']['params_core_sha256']
        (self.case / 'params-core.json').unlink()
        self.save_record()
        with mock.patch.dict(os.environ, BORG_CORE='borg-rs', BORG_PARAM_AMBIENT='99'):
            rc, receipt = self.execute()
        self.assertEqual(rc, 0)
        self.assertEqual(receipt['core'], 'reborn')
        self.assertEqual(self.env['BORG_CORE'], 'reborn')
        self.assertIn('BORG_OBSERVATION_LOG', self.env)
        self.assertNotIn('BORG_PARAM_AMBIENT', self.env)

    def test_a_native_receipt_without_a_controller_selects_the_native_core(self):
        # A record from before the harness always recorded borg_core (#607):
        # it names no controller, but only the native core writes
        # params-core.json, so the receipt settles which core played.
        del self.config['borg_core']
        self.save_record()
        with mock.patch.dict(os.environ, BORG_CORE='reborn', BORG_PARAM_AMBIENT='99'):
            rc, receipt = self.execute()
        self.assertEqual(rc, 0)
        self.assertEqual(receipt['core'], 'borg-rs')
        self.assertEqual(self.env['BORG_CORE'], 'borg-rs')
        self.assertNotIn('BORG_OBSERVATION_LOG', self.env)
        self.assertNotIn('BORG_PARAM_AMBIENT', self.env)

    def test_an_explicit_reborn_core_with_a_native_receipt_is_refused(self):
        self.config['borg_core'] = 'reborn'
        self.save_record()
        with self.assertRaisesRegex(SystemExit, 'contradicts the recorded reborn core'):
            rd.plan(self.case)

    def test_matching_keys_do_not_hide_a_changed_stream_endpoint_or_policy(self):
        mutations = {
            'state': lambda out: (out / 'run/state.log').write_text('changed'),
            'messages': lambda out: (out / 'run/messages.log').write_text('changed'),
            'endpoint': lambda out: (out / 'run/summary.json').write_text(json.dumps(
                dict(self.summary, game_turns=744))),
            'borg.txt': lambda out: (out / 'run/user/borg.txt').write_text('different'),
            'native origins': lambda out: (out / 'run/params-core.json').write_text(json.dumps(
                [dict(row, origin='environment') for row in self.params])),
            'trace': lambda out: (out / 'run/trace-core.jsonl').unlink(),
        }
        for name, mutate in mutations.items():
            with self.subTest(name=name):
                # Preserve each failed attempt in a separate output directory.
                rc, receipt = self.execute(mutate)
                self.assertEqual(rc, 1)
                self.assertFalse(receipt['reproduction_verified'])
                self.assertTrue(receipt['errors'])
                (self.root / 'out').rename(self.root / name)

    def test_missing_original_stream_hash_is_not_verified(self):
        del self.record['attempts'][0]['raw_sha256']['state.log']
        self.save_record()
        rc, receipt = self.execute()
        self.assertEqual(rc, 1)
        self.assertIn('no original state.log hash', '\n'.join(receipt['errors']))

    def test_any_build_is_always_labelled_diagnostic(self):
        rc, receipt = self.execute(extra=('--any-build',))
        self.assertEqual(rc, 0)
        self.assertEqual(receipt['status'], 'diagnostic')
        self.assertFalse(receipt['reproduction_verified'])

    def test_changed_binary_is_refused_before_execution(self):
        (self.source / 'build/rust/game/angband').write_text('changed binary')
        with mock.patch.object(rd, 'ROOT', self.source), self.assertRaisesRegex(SystemExit, 'executable differs'):
            rd.main([str(self.case), str(self.root / 'out')])
        self.assertFalse((self.root / 'out').exists())

    def test_parameter_payload_tampering_and_missing_receipts_are_refused(self):
        for name in ('params-core.json', 'config.txt', 'summary.json'):
            with self.subTest(name=name):
                path = self.case / name
                original = path.read_bytes()
                path.write_bytes(original + b' ')
                with self.assertRaisesRegex(SystemExit, 'recorded hash'):
                    rd.plan(self.case)
                path.write_bytes(original)
        (self.case / 'params-core.json').unlink()
        with self.assertRaisesRegex(SystemExit, 'missing'):
            rd.plan(self.case)

    def test_malformed_parameter_origins_names_and_classes_are_refused(self):
        originals = copy.deepcopy(self.params)
        for field, value in [('origin', 'unknown'), ('value', True), ('name', 'UPPERCASE'),
                             ('class_values', {'unknown': dict(value=1, origin='environment')})]:
            with self.subTest(field=field):
                self.params = [dict(originals[0], **{field: value})]
                self.save_params()
                with self.assertRaisesRegex(SystemExit, 'invalid params-core'):
                    rd.plan(self.case)

    def test_explicit_invalid_controller_is_not_replaced_by_a_default(self):
        for value in ('', 'unknown'):
            self.config['borg_core'] = value
            self.save_record()
            with self.assertRaisesRegex(SystemExit, 'unsupported recorded core'):
                rd.plan(self.case)

    def test_zoo_replay_keeps_recorded_parameter_environment_and_native_logs(self):
        self.config.update(zoo_profile='test', turns='1000', exact_turns='1', borg_reborn_core='borg-rs')
        del self.config['borg_core']
        self.save_record()
        (self.source / 'harness').mkdir()
        (self.source / 'harness/borg.txt').write_text('[BEGIN FORMULA SECTION]\n')
        with mock.patch.object(rd, 'ROOT', self.source):
            text = ('borg_respawn_race = 2\n\nborg_respawn_class = 1\n\n'
                    'borg_cheat_death = FALSE\n\nborg_respawn_winners = FALSE\n\n'
                    'borg_reborn_core = borg-rs\n\n[BEGIN FORMULA SECTION]\n')
            self.config['borg_txt_sha256'] = self.digest(text.encode())
            self.save_record()
            p = rd.plan(self.case)
            out = self.root / 'zoo-out'
            with mock.patch.dict(os.environ, BORG_PARAM_AMBIENT='99'), \
                    mock.patch.object(rd.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0)) as launch:
                rd.run_zoo(p, out, {}, 0)
        env = launch.call_args.kwargs['env']
        self.assertEqual(env['BORG_PARAM_ENVIRONMENT_SETTING'], '23')
        self.assertEqual(env['BORG_PARAM_DEFAULT_SETTING__MAGE'], '31')
        self.assertEqual(env['BORG_RUN_DIR'], str(out / 'run'))
        self.assertNotIn('BORG_PARAM_AMBIENT', env)


if __name__ == '__main__':
    unittest.main()
