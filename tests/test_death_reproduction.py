"""Birth reproduction must match provenance, configuration and all three streams."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import reproduce_native_death as r


class ReproductionTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        for name in ('borg.txt', 'profile.txt'):
            (self.root / name).write_text(name + '\n')
        self.identity = dict(git_rev='a' * 40, source_sha256='b' * 64,
                             binary_sha256='c' * 64, seed=202,
                             borg_txt_sha256=r.sha(self.root / 'borg.txt'),
                             profile_sha256=r.sha(self.root / 'profile.txt'))
        self.summary = dict(seed=202, race_idx=8, class_idx=2, loaded=False, dead=True,
                            stop_reason='death', game_turns=100, death_cause='a test enemy',
                            clevel=1, depth=1)
        r.write(self.root / 'summary.json', self.summary)
        self.original = dict(schema='borg-reborn-rs/death-record@1', run_kind='harness',
            identity=self.identity, terminal=dict(dead=True, turn=100, cause='a test enemy',
                race_idx=8, class_idx=2, level=1, depth=1),
            files_sha256={'summary.json': r.sha(self.root / 'summary.json')},
            attempts=[dict(raw_sha256={})])
        for name in ('keys.log', 'state.log', 'messages.log'):
            (self.root / name).write_text('expected ' + name + '\n')
            self.original['attempts'][0]['raw_sha256'][name] = r.sha(self.root / name)
        r.write(self.root / 'record.json', self.original)
        r.write(self.root / 'runtime.json', dict(binary_sha256='c' * 64, game_data_files={}))
        self.recipe = dict(schema='borg-cemetery/native-death-recipe@1', start='birth',
            repository='diegoami/borg-reborn-rs', source_commit='a' * 40,
            source_sha256='b' * 64, binary_sha256='c' * 64, seed=202, race_idx=8,
            class_idx=2, turn_cap=200, flags='menu', environment={})
        for key, name in [('record', 'record.json'), ('runtime', 'runtime.json'),
                          ('borg_txt', 'borg.txt'), ('profile', 'profile.txt')]:
            self.recipe[key] = dict(path=name, sha256=r.sha(self.root / name))
        (self.root / 'config.txt').write_text(''.join(k + '=' + self.identity[k] + '\n'
            for k in ('borg_txt_sha256', 'profile_sha256')))

    def tearDown(self):
        self.tmp.cleanup()

    def test_recipe_identity_cannot_change_or_silently_ignore_configuration(self):
        self.assertTrue(r.inputs(self.recipe, self.root))
        for change in [dict(seed=203), dict(class_idx=1), dict(flags='menu,random'),
                       dict(environment={'BORG_PARAM_UNKNOWN': '1'})]:
            with self.assertRaises(ValueError):
                r.inputs(dict(self.recipe, **change), self.root)

    def test_loaded_origin_is_not_misrepresented_as_birth(self):
        r.write(self.root / 'summary.json', dict(self.summary, loaded=True))
        self.original['files_sha256']['summary.json'] = r.sha(self.root / 'summary.json')
        r.write(self.root / 'record.json', self.original)
        self.recipe['record']['sha256'] = r.sha(self.root / 'record.json')
        with self.assertRaisesRegex(ValueError, 'ordinary birth'):
            r.inputs(self.recipe, self.root)

    def test_endpoint_and_all_three_streams_are_required(self):
        self.assertEqual(len(r.verify_run(self.recipe, self.original, self.root)), 3)
        for name in ('keys.log', 'state.log', 'messages.log'):
            text = (self.root / name).read_text()
            (self.root / name).write_text('changed')
            with self.assertRaisesRegex(ValueError, 'stream differs'):
                r.verify_run(self.recipe, self.original, self.root)
            (self.root / name).write_text(text)
        r.write(self.root / 'summary.json', dict(self.summary, dead=False))
        with self.assertRaisesRegex(ValueError, 'endpoint differs'):
            r.verify_run(self.recipe, self.original, self.root)


if __name__ == '__main__':
    unittest.main()
