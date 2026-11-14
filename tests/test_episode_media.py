import gzip
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from episode_inventory import extract_inventory, observations, description
from capture_episode_media import render_gif, sample, screen


class EpisodeMediaTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def test_inventory_at_start_changes_and_last_observation(self):
        rows = [dict(turn=t, inventory=[dict(desc='Scrolls of Phase Door', number=n,
                                            kind=999, aware=True)], equipment=[], quiver=[], spells=[])
                for t, n in [(1, 3), (10, 2), (15, 2), (20, 1), (30, 1), (40, 1)]]
        with gzip.open(self.root / 'observations.jsonl.gz', 'wt') as stream:
            for row in rows:
                stream.write(json.dumps(row) + '\n')
        result = extract_inventory(self.root, self.root / 'out', 12, 35)
        self.assertEqual([r['turn'] for r in result['snapshots']], [10, 20, 30])
        self.assertEqual([r['pack'][0]['number'] for r in result['snapshots']], [2, 1, 1])
        self.assertNotIn('kind', result['snapshots'][0]['pack'][0])
        self.assertEqual(description(result['snapshots'][0]['pack'][0]), '2 × Scrolls of Phase Door')

    def test_native_inventory_and_spell_deltas_are_carried_forward(self):
        rows = [dict(turn=1, inventory=dict(pack=[dict(description='a potion')]), spells={'known': ['heal']}),
                dict(turn=2, inventory=None, spells=None)]
        (self.root / 'frames.jsonl').write_text(''.join(json.dumps(r) + '\n' for r in rows))
        snapshots = list(observations(self.root))
        self.assertEqual(snapshots[1]['pack'][0]['description'], 'a potion')
        self.assertEqual(snapshots[1]['spells'], {'known': ['heal']})

    def test_missing_inventory_remains_explicitly_missing(self):
        result = extract_inventory(self.root, self.root / 'out', 10, 50)
        self.assertEqual(result['status'], 'not_recorded')
        self.assertEqual(result['snapshots'], [])

    def test_terminal_parser_and_sampling(self):
        path = self.root / 'stderr.log'
        path.write_text('diagnostic\n---- screen ----\n@..D\n....\n----------------\nafter\n')
        self.assertEqual(screen(path), '@..D\n....')
        rows = [dict(turn=i, line=i) for i in range(100)]
        selected = sample(rows, 10)
        self.assertEqual(len(selected), 10)
        self.assertEqual([selected[0]['turn'], selected[-1]['turn']], [0, 99])

    def test_gif_contains_real_supplied_screens_and_multiple_frames(self):
        from PIL import Image
        frames = [dict(turn=10, phase='verified replay', screen='@..D\n....'),
                  dict(turn=20, phase='original death', screen='You die.\n...D')]
        target = self.root / 'episode.gif'
        render_gif(frames, target, [], [], 102)
        with Image.open(target) as movie:
            self.assertEqual(movie.format, 'GIF')
            self.assertEqual(movie.n_frames, 2)
            movie.seek(1)
            self.assertEqual(movie.info['duration'], 1800)


if __name__ == '__main__':
    unittest.main()
