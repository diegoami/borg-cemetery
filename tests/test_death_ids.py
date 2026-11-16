import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from death_ids import refresh, resolve
from native.death_identity import death_id, metadata, ensure


def record():
    return dict(schema='borg-reborn-rs/death-record@1', id='D0001',
                encounter_family='start-one', attempts=[
                    dict(role='original', outcome='death', result_sha256='a' * 64)])


class DeathIdentityTest(unittest.TestCase):
    def test_annotations_and_later_attempts_do_not_change_identity(self):
        first = record()
        raw = json.dumps(first).encode()
        original = metadata(first, raw, 'D0001')['id']
        changed = copy.deepcopy(first)
        changed['investigation'] = 'https://example.org/issue'
        changed['id'] = 'D0099'
        changed['attempts'].append(dict(role='repeat', result_sha256='b' * 64))
        self.assertEqual(metadata(changed, json.dumps(changed).encode(), 'D0099')['id'], original)
        self.assertNotEqual(death_id('start-two', 'a' * 64), original)
        self.assertNotEqual(death_id('start-one', 'b' * 64), original)

    def test_migration_is_additive_idempotent_and_aliases_are_scoped(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = [root / 'deaths/D0001', root / 'validation/controls/D0001']
            for i, path in enumerate(paths):
                path.mkdir(parents=True)
                rec = record()
                rec['encounter_family'] += str(i)
                (path / 'record.json').write_text(json.dumps(rec))
                (path / 'report.md').write_text('Original report\n')
            before = {p: p.read_bytes() for path in paths for p in path.iterdir()}
            rows = refresh(root)['records']
            self.assertEqual(len(rows), 2)
            self.assertNotEqual(rows[0]['id'], rows[1]['id'])
            self.assertEqual(refresh(root, check=True)['records'], rows)
            for p, raw in before.items():
                self.assertEqual(p.read_bytes(), raw)
            self.assertEqual(resolve(root, rows[0]['id']), paths[0])
            with self.assertRaisesRegex(ValueError, 'found 2'):
                resolve(root, 'D0001')
            (paths[0] / 'record.json').write_text('{}')
            with self.assertRaises(ValueError):
                refresh(root, check=True)

    def test_bad_sidecar_or_incomplete_original_cannot_be_accepted(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)
            (path / 'record.json').write_text(json.dumps(record()))
            value = ensure(path)
            value['id'] = 'D-' + '0' * 64
            (path / 'death-id.json').write_text(json.dumps(value))
            with self.assertRaisesRegex(ValueError, 'differs'):
                ensure(path, check=True)
        for attempts in ([], [dict(role='original')], record()['attempts'] * 2):
            broken = dict(record(), attempts=attempts)
            with self.assertRaises(ValueError):
                metadata(broken, json.dumps(broken).encode(), 'D0001')

    def test_guided_incident_does_not_invent_a_measured_run(self):
        rec = dict(schema='borg-reborn-rs/guided-death-analysis@1', id='watched')
        value = metadata(rec, json.dumps(rec).encode(), 'watched')
        self.assertEqual(value['basis']['kind'], 'historical-guided-record')
        self.assertNotIn('encounter_family', value['basis'])

    def test_all_retained_dossiers_have_verified_canonical_ids(self):
        root = Path(__file__).resolve().parents[1]
        self.assertGreater(len(refresh(root, check=True)['records']), 200)
