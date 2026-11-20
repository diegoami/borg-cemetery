"""Sharded harvests (borg-zoo#184): seed blocks, and joining a class's shards in seed order."""
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from harvest_incidents import shard_range
from merge_incident_shards import merge
from synthetic_suite import write

SCHEMA = 'borg-cemetery/balanced-incident-harvest@1'


def shard_dir(root, shard, cases, stop='range_exhausted', cls=0):
    """A packed selection of one shard with the given (case id, save hash) pairs."""
    d = root / f'shard-{shard}'
    write(d / 'spec.json', {'source_commit': 'abc'})
    write(d / 'build.json', {'git_rev': 'abc'})
    selected = []
    for case_id, save in cases:
        attempt = f'a-{shard}-{case_id}'
        (d / 'cases' / case_id).mkdir(parents=True)
        (d / 'cases' / case_id / 'incident.json').write_text('{}')
        (d / 'attempts' / attempt).mkdir(parents=True)
        (d / 'attempts' / attempt / 'summary.json').write_text('{}')
        selected.append({'id': case_id, 'directory': case_id, 'save_sha256': save, 'source_attempt': attempt})
    write(d / 'harvest.json', {'schema': SCHEMA, 'spec_sha256': 's', 'class_idx': cls, 'shard': shard,
                               'attempts': [{'id': c['source_attempt']} for c in selected], 'selected': selected,
                               'rejected': [], 'stop_reason': stop})


class ShardRangeTest(unittest.TestCase):
    def test_blocks_cover_the_class_once_in_order(self):
        spec = {'max_attempts_per_class': 1000, 'shard_size': 250}
        self.assertEqual([shard_range(spec, k) for k in range(4)], [(0, 250), (250, 500), (500, 750), (750, 1000)])
        with self.assertRaises(ValueError):
            shard_range(spec, 4)
        with self.assertRaises(ValueError):
            shard_range(spec, None)

    def test_an_unsharded_spec_searches_everything(self):
        self.assertEqual(shard_range({'max_attempts_per_class': 1024}, None), (0, 1024))
        with self.assertRaises(ValueError):
            shard_range({'max_attempts_per_class': 1024}, 1)


class MergeTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.inputs = self.root / 'inputs'

    def tearDown(self):
        self.tmp.cleanup()

    def test_shards_join_in_block_order_up_to_the_target(self):
        shard_dir(self.inputs, 1, [('c3', 'h3'), ('c4', 'h4')])
        shard_dir(self.inputs, 0, [('c1', 'h1'), ('c2', 'h2')])
        doc = merge(self.inputs, self.root / 'out', 0, target=3)
        self.assertEqual([c['id'] for c in doc['selected']], ['c1', 'c2', 'c3'])
        self.assertEqual([c['source_shard'] for c in doc['selected']], [0, 0, 1])
        self.assertEqual(doc['shards_used'], [0, 1])
        self.assertTrue((self.root / 'out/cases/c3/incident.json').exists())
        self.assertIsNone(doc['gap'])

    def test_a_duplicate_save_across_shards_is_taken_once(self):
        shard_dir(self.inputs, 0, [('c1', 'h1')])
        shard_dir(self.inputs, 1, [('c2', 'h1'), ('c3', 'h3')])
        doc = merge(self.inputs, self.root / 'out', 0, target=2)
        self.assertEqual([c['id'] for c in doc['selected']], ['c1', 'c3'])

    def test_a_shard_stopped_early_ends_the_selection(self):
        shard_dir(self.inputs, 0, [('c1', 'h1')], stop='retained_evidence_budget')
        shard_dir(self.inputs, 1, [('c2', 'h2'), ('c3', 'h3')])
        doc = merge(self.inputs, self.root / 'out', 0, target=3)
        self.assertEqual([c['id'] for c in doc['selected']], ['c1'])
        self.assertIn('stopped early', doc['gap'])

    def test_a_missing_shard_ends_the_selection(self):
        shard_dir(self.inputs, 0, [('c1', 'h1')])
        shard_dir(self.inputs, 2, [('c3', 'h3')])
        doc = merge(self.inputs, self.root / 'out', 0, target=3)
        self.assertEqual([c['id'] for c in doc['selected']], ['c1'])
        self.assertEqual(doc['gap'], 'shard 1 missing')

    def test_other_classes_are_ignored(self):
        shard_dir(self.inputs, 0, [('c1', 'h1')])
        shard_dir(self.root / 'other', 0, [('x', 'hx')], cls=5)
        doc = merge(self.inputs, self.root / 'out', 0, target=1)
        self.assertEqual([c['id'] for c in doc['selected']], ['c1'])


if __name__ == '__main__':
    unittest.main()
