import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import build_statistics as stats


def dossier(root, name='D0001', binary='a' * 64, family='start-one'):
    path = root / 'deaths' / name
    path.mkdir(parents=True)
    record = dict(schema='borg-reborn-rs/death-record@1', id=name, encounter_family=family,
                  identity=dict(git_rev='f' * 40, binary_sha256=binary, source_sha256='b' * 64,
                                impl='rust', seed=123, git_dirty='no'),
                  terminal=dict(dead=True, turn=1000, depth=1, level=2), raw_cause='a monster',
                  attempts=[dict(role='original', outcome='death', source_commit='f' * 40,
                                 binary_sha256=binary, result_sha256='c' * 64)])
    (path / 'record.json').write_text(json.dumps(record))
    return path, record


class StatisticsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def test_repeats_families_and_nested_branches_do_not_become_independent_births(self):
        path, record = dossier(self.root)
        record['attempts'].append(dict(role='repeat', outcome='death', binary_sha256='d' * 64))
        (path / 'record.json').write_text(json.dumps(record))
        dossier(self.root, 'D0002')
        branch = path / 'alternatives/human/example'
        branch.mkdir(parents=True)
        (branch / 'record.json').write_text(json.dumps(record))
        rows = stats.local_source(self.root)['records']
        self.assertEqual(stats.counts(rows), [2, 1, 0, 3, 1])
        stats.generate(self.root)
        report = (self.root / 'statistics/README.md').read_text()
        self.assertIn('| 2 | 1 | 0 | 3 | 1 |', report)
        self.assertIn('No mortality or survival rate', report)
        self.assertIn('d' * 64, (self.root / 'statistics/attempts.md').read_text())
        page = next((self.root / 'statistics/builds').glob('*/README.md')).read_text()
        self.assertIn('Embedded repeats (all builds)', page)
        self.assertNotIn('d' * 64, page)

    def test_same_commit_different_binary_and_dirty_inputs_stay_separate(self):
        path, _ = dossier(self.root)
        first = stats.normalize(path, 'cemetery')
        other = copy.deepcopy(first)
        other['build']['binary_sha256'] = 'e' * 64
        self.assertNotEqual(stats.build_id(first), stats.build_id(other))
        other = copy.deepcopy(first)
        other['build']['inputs_dirty'] = 'yes'
        self.assertNotEqual(stats.build_id(first), stats.build_id(other))
        stats.generate(self.root)
        page = next((self.root / 'statistics/builds').glob('*/README.md')).read_text()
        self.assertIn('a' * 64, page)
        self.assertIn('f' * 40, page)
        self.assertIn('../../../deaths/D0001/README.md', page)

    def test_saved_rng_and_missing_seed_are_explicit(self):
        path, record = dossier(self.root)
        record['identity']['start_save'] = {'sha256': 'saved'}
        (path / 'record.json').write_text(json.dumps(record))
        row = stats.normalize(path, 'cemetery')
        self.assertIsNone(row['seed'])
        self.assertEqual(row['seed_basis'], 'saved RNG')
        record['identity'].pop('start_save')
        record['identity'].pop('seed')
        record['attempts'][0]['requested_seed'] = 999
        (path / 'record.json').write_text(json.dumps(record))
        row = stats.normalize(path, 'cemetery')
        self.assertIsNone(row['seed'])
        self.assertEqual(row['seed_basis'], 'not recorded')

    def test_missing_build_identity_does_not_merge_unknown_cases(self):
        first, _ = dossier(self.root)
        row = stats.normalize(first, 'cemetery')
        row['build']['binary_sha256'] = row['build']['source_sha256'] = None
        other = copy.deepcopy(row)
        other['case'] = 'D0002'
        self.assertNotEqual(stats.build_id(row), stats.build_id(other))

    def test_check_detects_changed_records_and_regeneration_is_deterministic(self):
        path, record = dossier(self.root)
        stats.generate(self.root)
        before = (self.root / 'statistics/README.md').read_bytes()
        stats.generate(self.root, check=True)
        stats.generate(self.root)
        self.assertEqual(before, (self.root / 'statistics/README.md').read_bytes())
        record['terminal']['turn'] = 2000
        (path / 'record.json').write_text(json.dumps(record))
        with self.assertRaisesRegex(ValueError, 'regeneration'):
            stats.generate(self.root, check=True)
        stats.generate(self.root)
        stats.generate(self.root, check=True)

    def test_external_snapshot_is_pinned_checks_metadata_and_survives_offline_regeneration(self):
        external = self.root / 'external'
        external.mkdir()
        path, record = dossier(external)
        # The external repository retains its historical path, not cemetery/deaths.
        (external / 'docs').mkdir()
        (external / 'deaths').rename(external / 'docs/deaths')
        path = external / 'docs/deaths/D0001'
        def git(*args):
            return subprocess.check_output(['git', '-C', str(external), *args], text=True).strip()
        git('init', '-q')
        git('config', 'user.name', 'Test')
        git('config', 'user.email', 'test@example.org')
        git('add', '.')
        git('commit', '-qm', 'fixture')
        pin = git('rev-parse', 'HEAD')
        stats.generate(self.root, external, pin)
        page = next((self.root / 'statistics/builds').glob('*/README.md')).read_text()
        self.assertIn(f'/blob/{pin}/docs/deaths/D0001/report.md', page)
        record['terminal']['turn'] = 12
        (path / 'record.json').write_text(json.dumps(record))
        stats.generate(self.root, check=True)  # reads the retained snapshot, never that dirty checkout
        with self.assertRaises(subprocess.CalledProcessError):
            stats.import_external(external, pin)
        git('checkout', '--', 'docs/deaths/D0001/record.json')
        (path / 'build.json').write_text('{}')
        with self.assertRaisesRegex(ValueError, 'Untracked metadata'):
            stats.import_external(external, pin)

    def test_living_terminal_is_not_counted_as_a_death(self):
        path, record = dossier(self.root)
        record['terminal']['dead'] = False
        (path / 'record.json').write_text(json.dumps(record))
        with self.assertRaisesRegex(ValueError, 'Living record'):
            stats.normalize(path, 'cemetery')


if __name__ == '__main__':
    unittest.main()
