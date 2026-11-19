from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import scenario_config


class ConfiguredExactTurnsTest(unittest.TestCase):
    """The configured adapter's argv: exact_turns is opt-in and the save is copied."""

    def launch(self, **kwargs):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            template = tmp / 'borg.txt'
            template.write_text('borg_respawn_race = 0\n')
            save = tmp / 'input.save'
            save.write_bytes(b'original save')
            binary = tmp / 'bin/angband'
            binary.parent.mkdir()
            binary.write_bytes(b'')
            raw = tmp / 'raw'
            calls = []
            def fake(argv, **kw):
                calls.append((argv, kw))
                (raw / 'save/input.save').write_bytes(b'autosaved')
                return 1  # a failed run skips receipt checks
            scenario = dict(birth_seed=7, race_idx=1, class_idx=2)
            inherited = dict(BORG_OBSERVATION_LOG='/x/obs.jsonl', BORG_CEMETERY_DIR='/x/cem', PATH='/bin')
            execute = scenario_config.configured_adapter(template, **kwargs)
            with mock.patch.object(scenario_config, 'command', fake):
                rc = execute(tmp, binary, raw, save, scenario, 300, inherited, 5)
            self.assertEqual(rc, 1)
            self.assertEqual(save.read_bytes(), b'original save')
            argv, kw = calls[0]
            config = (raw / 'config.txt').read_text()
            self.assertIn('save_sha256=' + scenario_config.sha(save), config)
            return [str(a) for a in argv], kw['env'], raw

    def test_default_has_no_exact_turns(self):
        argv, env, raw = self.launch()
        self.assertNotIn('-exact-turns', argv)
        self.assertIn('-turns', argv)
        self.assertEqual(argv[argv.index('-turns') + 1], '300')
        self.assertEqual(argv[argv.index('-load') + 1], str(raw / 'save/input.save'))

    def test_exact_turns_reaches_frontend(self):
        argv, env, raw = self.launch(exact_turns=True)
        self.assertEqual(argv.count('-exact-turns'), 1)

    def test_environment(self):
        argv, env, raw = self.launch()
        self.assertEqual(env['BORG_CORE'], 'borg-rs')
        self.assertEqual(env['BORG_CEMETERY_DIR'], '/x/cem')
        self.assertNotIn('BORG_OBSERVATION_LOG', env)


if __name__ == '__main__':
    unittest.main()
