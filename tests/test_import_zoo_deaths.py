"""Importing borg-zoo death bundles (borg-zoo#176, #63)."""
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import import_zoo_deaths as importer

KEYS = b'10 a 0 0\n20 b 0 0\n'
KEYS_SHA = hashlib.sha256(KEYS).hexdigest()


def bundle(base, cell, seed, status='reproduced', keys=KEYS, trace_total=None):
    out = base / cell
    (out / 'user').mkdir(parents=True)
    (out / 'user/borg.txt').write_text('borg_cheat_death = FALSE\n')
    (out / 'keys.log').write_bytes(keys)
    (out / 'summary.json').write_text(json.dumps({
        'seed': seed, 'race': 'Human', 'race_idx': 0, 'class': 'Druid', 'class_idx': 2, 'dead': True,
        'stop_reason': 'death', 'death_cause': 'a crow', 'game_turns': 500, 'clevel': 2, 'depth': 1,
        'max_depth': 1, 'game_options': {}}))
    (out / 'config.txt').write_text(f'seed={seed}\nrace_idx=0\nclass_idx=2\nturns=1000\nexact_turns=1\n'
                                    'borg_txt_sha256=feed\nzoo_profile=p\nzoo_specimen=s\n')
    (out / 'BUILD_ID').write_text('git_rev=abc\ngit_dirty=no\nsource_sha256=src\nbinary_sha256=bin\n')
    if trace_total:
        (out / 'trace-core.jsonl').write_text(''.join(f'{{"n": {i}}}\n' for i in range(5)))
        (out / 'trace-core.lines').write_text(f'{trace_total}\n')
    entry = {'schema': 'borg-zoo/death-bundle@1', 'cell': cell, 'bundle': cell, 'seed': seed,
             'specimen': 's', 'profile': 'p', 'character': 'Human Druid', 'cause': 'a crow',
             'final': {'turn': 500, 'level': 2, 'depth': 1, 'max_depth': 1}, 'status': status,
             'error': None if status == 'reproduced' else 'replay keys differ',
             'play_sha256': KEYS_SHA, 'experiment': 'exp', 'build': {'impl': 'rust'}}
    with (base / 'index.jsonl').open('a') as f:
        f.write(json.dumps(entry) + '\n')


class ImportZooDeathsTest(unittest.TestCase):
    def run_import(self, build):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            artifact = tmp / 'bundles' / 'deaths-s-0'
            artifact.mkdir(parents=True)
            build(artifact)
            registry = tmp / 'registry' / 'deaths'
            with patch.dict(os.environ, {'BORG_DEATH_RECORDS_DIR': str(registry)}):
                code = importer.main(['--bundles', str(tmp / 'bundles'), '--run-id', '777'])
            page = tmp / 'registry' / 'runs' / 'zoo-exp-777'
            cases = sorted(d.name for d in registry.iterdir() if d.name.startswith('D-')) if registry.exists() else []
            records = {c: json.loads((registry / c / 'record.json').read_text()) for c in cases}
            return code, json.loads((page / 'deaths.json').read_text()), (page / 'README.md').read_text(), records

    def test_reproduced_bundles_become_dossiers_and_others_are_listed(self):
        def build(base):
            bundle(base, 'suite/s/p/1', 1, trace_total=4000)
            bundle(base, 'suite/s/p/2', 2, status='not_reproduced')
            bundle(base, 'suite/s/p/3', 3, keys=b'other\n')  # keys are not the cell's
        code, deaths, readme, records = self.run_import(build)
        self.assertEqual(code, 0)
        rows = {r['seed']: r for r in deaths['deaths']}
        self.assertEqual(rows[1]['imported'], 'exported')
        self.assertEqual(rows[2]['imported'], 'skipped')
        self.assertEqual(rows[2]['reason'], 'replay keys differ')
        self.assertEqual(rows[3]['imported'], 'skipped')
        self.assertEqual(len(records), 1)
        record = records[rows[1]['case']]
        self.assertEqual(record['attempts'][0]['result_sha256'], KEYS_SHA)
        self.assertTrue(record['attempts'][0]['raw_directory'].startswith('borg-zoo run 777, artifact deaths-s-0'))
        self.assertEqual(record['core_decision_trace'], {'file': 'trace-core-tail.jsonl', 'lines': 5, 'of': 4000})
        self.assertIn(rows[1]['case'][:14], readme)
        self.assertIn('1 of 3 deaths have a dossier', readme)

    def test_bundles_without_an_index_line_are_listed_not_imported(self):
        def build(base):
            bundle(base, 'suite/s/p/1', 1)
            bundle(base, 'suite/s/p/2', 2)
            lines = (base / 'index.jsonl').read_text().splitlines()
            (base / 'index.jsonl').write_text(lines[0] + '\n')  # the shard stopped before indexing seed 2
            (base / 'suite/s/p/3/user').mkdir(parents=True)  # a replay cut short at its start
            (base / 'suite/s/p/3/user/borg.txt').write_text('x\n')
        code, deaths, readme, records = self.run_import(build)
        self.assertEqual(code, 0)
        rows = {r['seed']: r for r in deaths['deaths']}
        self.assertEqual(rows[1]['imported'], 'exported')
        self.assertEqual(rows[2]['imported'], 'skipped')
        self.assertIn('no index entry', rows[2]['reason'])
        self.assertEqual(rows[3]['imported'], 'skipped')
        self.assertEqual(len(records), 1)
        self.assertIn('1 of 3 deaths have a dossier', readme)

    def test_one_bad_index_line_does_not_stop_the_run(self):
        def build(base):
            bundle(base, 'suite/s/p/1', 1)
            bundle(base, 'suite/s/p/2', 2)
            lines = [json.loads(line) for line in (base / 'index.jsonl').read_text().splitlines()]
            del lines[1]['build']
            (base / 'index.jsonl').write_text(''.join(json.dumps(line) + '\n' for line in lines))
        _, deaths, _, records = self.run_import(build)
        rows = {r['seed']: r for r in deaths['deaths']}
        self.assertEqual(rows[1]['imported'], 'exported')
        self.assertIn('no bundle or build identity', rows[2]['reason'])

    def test_an_unreadable_trace_count_falls_back_to_the_kept_lines(self):
        def build(base):
            bundle(base, 'suite/s/p/1', 1, trace_total=4000)
            (base / 'suite/s/p/1/trace-core.lines').write_text('lots\n')
        _, _, _, records = self.run_import(build)
        (record,) = records.values()
        self.assertEqual(record['core_decision_trace']['of'], 5)

    def test_artifact_names_agree_for_indexed_and_unindexed_bundles(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            # gh run download: <dest>/<artifact>/<specimen>-<shard>/index.jsonl
            shard = tmp / 'dl' / 'deaths-s-0' / 's-0'
            shard.mkdir(parents=True)
            bundle(shard, 'suite/s/p/1', 1)
            (shard / 'suite/s/p/2/user').mkdir(parents=True)
            (shard / 'suite/s/p/2/user/borg.txt').write_text('x\n')
            found = list(importer.entries(tmp / 'dl'))
            self.assertEqual(found[0][0], 'deaths-s-0')
            self.assertEqual(importer.unindexed(tmp / 'dl', found)[0]['artifact'], 'deaths-s-0')
            # one shard directory given alone is its own artifact
            found = list(importer.entries(shard))
            self.assertEqual(found[0][0], 's-0')
            self.assertEqual(importer.unindexed(shard, found)[0]['artifact'], 's-0')

    def test_run_and_run_id_together_are_refused(self):
        with self.assertRaises(SystemExit):
            importer.main(['--run', '1', '--run-id', '2'])

    def test_a_scary_list_stays_with_the_dossier(self):
        # borg-zoo#228: the list the cell read is kept, so the death reruns with the same bytes.
        def build(base):
            bundle(base, 'suite/s/p/1', 1)
            out = base / 'suite/s/p/1'
            (out / 'user/scary_monsters.txt').write_bytes(b'Grip | 5 | - | -\n')
            with (out / 'config.txt').open('a') as f:
                f.write('borg_scary_list=scary_monsters.txt\nscary_list_sha256=x\n')
        _, deaths, _, records = self.run_import(build)
        (record,) = records.values()
        self.assertIn('scary_list.txt', record['files_sha256'])

    def test_the_same_death_twice_is_a_repeat(self):
        def build(base):
            bundle(base, 'suite/s/p/1', 1)
            bundle(base, 'suite/s/p/1-again', 1)
        _, deaths, _, records = self.run_import(build)
        self.assertEqual([r['imported'] for r in deaths['deaths']], ['exported', 'repeat'])
        self.assertEqual(len(records), 1)


if __name__ == '__main__':
    unittest.main()
