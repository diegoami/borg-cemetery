import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from case_launchers import launchers
from case_replay import alternative_summary, attach_human, plan, sha, write


class CaseLauncherTest(unittest.TestCase):
    def test_launchers_locate_tools_from_another_working_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'scripts').mkdir()
            (root / 'scripts/case_replay.py').write_text('import sys\nprint(repr(sys.argv[1:]))\n')
            case = root / 'deaths/case with spaces'
            case.mkdir(parents=True)
            launchers(case)
            for name, action in [('build.sh', 'build'), ('watch.sh', 'watch'), ('play.sh', 'human')]:
                self.assertTrue(os.access(case / name, os.X_OK))
                output = subprocess.check_output([str(case / name), '--label', 'My test'], cwd='/tmp', text=True)
                self.assertIn(repr(action), output)
                self.assertIn(str(case), output)
                self.assertIn('My test', output)

    def test_every_existing_death_and_scenario_gets_the_process(self):
        root = Path(__file__).resolve().parents[1]
        for case in [p.parent for p in (root / 'deaths').glob('D*/record.json')] + list((root / 'scenarios').glob('S*')):
            for name in ('build.sh', 'watch.sh', 'play.sh'):
                self.assertTrue(os.access(case / name, os.X_OK), str(case / name))
                subprocess.run(['bash', '-n', str(case / name)], check=True)
        self.assertEqual(plan(root / 'deaths/D0007')['scenario'], root / 'scenarios/S0003')
        self.assertEqual(plan(root / 'deaths/D0005-recorded')['kind'], 'legacy')
        self.assertEqual(plan(root / 'deaths/D0001-seed8400-warrior')['kind'], 'seed')

    def test_human_recording_is_attached_and_mixed_play_is_labelled(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            case, scenario, session = root / 'death', root / 'scenario', root / 'session-1'
            case.mkdir()
            scenario.mkdir()
            (session / 'record').mkdir(parents=True)
            (case / 'report.md').write_text('Original death account.\n')
            write(case / 'record.json', dict(id='D-test', identity=dict(seed=102)))
            write(scenario / 'scenario.json', dict(start_turn=3402, save_sha256='original-save', race_idx=2, class_idx=1))
            rows = [dict(turn=3402, race_idx=2, class_idx=1, hp=9, dead=0),
                    dict(turn=3700, race_idx=2, class_idx=1, hp=5, dead=0)]
            (session / 'record/frames.jsonl').write_text(''.join(json.dumps(r) + '\n' for r in rows))
            (session / 'record/inputs.jsonl').write_text(json.dumps(dict(kind='poll', input=dict(event_type=1))) + '\n')
            write(session / 'verification.json', dict(verified=True))
            write(session / 'session.json', dict(runtime=dict(binary='pinned-game', recorder='pinned-recorder')))
            entry = attach_human(case, scenario, session, 'Retreated earlier', 'Tried returning to stairs.')
            self.assertTrue((case / 'report.md').read_text().startswith('Original death account.\n'))
            self.assertIn('Alternative human play', (case / 'report.md').read_text())
            self.assertIn('Retreated earlier', (case / 'report.md').read_text())
            self.assertTrue((entry / 'recording.tar.xz').is_file())
            meta = json.loads((entry / 'alternative.json').read_text())
            self.assertEqual(meta['save_sha256'], 'original-save')
            self.assertFalse(meta['independent_birth'])
            self.assertEqual(meta['actor'], 'human play')
            self.assertNotIn('survived_horizon', meta['outcome'])
            with (session / 'record/inputs.jsonl').open('a') as stream:
                stream.write(json.dumps(dict(kind='bot')) + '\n')
            self.assertEqual(alternative_summary(session / 'record', json.loads((scenario / 'scenario.json').read_text()))['actor'], 'mixed human/Borg play')
            with (case / 'report.md').open('a') as stream:
                stream.write('\nLater independent analysis must survive.\n')
            import shutil
            another = root / 'session-2'
            shutil.copytree(session, another)
            attach_human(case, scenario, another, 'Second attempt', '')
            updated = (case / 'report.md').read_text()
            self.assertIn('Later independent analysis must survive.', updated)
            self.assertIn('Retreated earlier', updated)
            self.assertIn('Second attempt', updated)
            self.assertEqual(updated.count('<!-- alternative-human-play:start -->'), 1)

    def test_wrong_start_is_not_attached_to_a_death(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write(root / 'unused.json', {})
            (root / 'frames.jsonl').write_text(json.dumps(dict(turn=1, race_idx=2, class_idx=1, hp=9)) + '\n')
            (root / 'inputs.jsonl').write_text('')
            with self.assertRaisesRegex(ValueError, 'expected starting turn'):
                alternative_summary(root, dict(start_turn=3402, race_idx=2, class_idx=1))


if __name__ == '__main__':
    unittest.main()
