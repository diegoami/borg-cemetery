import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from register_deaths import register


class NativeRegistrationTest(unittest.TestCase):
    def test_registers_human_page_without_rewriting_historical_index_or_capture(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            case = root / 'deaths/D0001-rust-seed123'
            case.mkdir(parents=True)
            record = dict(schema='borg-reborn-rs/death-record@1', id=case.name, encounter_family='start-example',
                          identity=dict(seed=123, git_rev='a' * 40), raw_cause='a monster',
                          terminal=dict(turn=100, race_idx=0, class_idx=0, dead=True))
            (case / 'record.json').write_text(json.dumps(record))
            (case / 'report.md').write_text('Original native report.\n')
            (root / 'deaths/README.md').write_text('Curated historical index.\n')
            (root / 'deaths/index.json').write_text('{"historical": true}\n')
            originals = {p: p.read_bytes() for p in (case / 'record.json', case / 'report.md',
                         root / 'deaths/README.md', root / 'deaths/index.json')}
            self.assertEqual(register(root), 1)
            self.assertIn('123', (root / 'deaths/CATALOG.md').read_text())
            self.assertTrue((case / 'README.md').exists())
            for path, original in originals.items():
                self.assertEqual(path.read_bytes(), original)
            catalogue = (root / 'deaths/CATALOG.md').read_bytes()
            register(root)
            self.assertEqual((root / 'deaths/CATALOG.md').read_bytes(), catalogue)

    def test_native_export_defaults_to_cemetery_and_respects_temporary_override(self):
        root = Path(__file__).resolve().parents[1]
        path = root / 'scripts/native/export-death.py'
        spec = importlib.util.spec_from_file_location('cemetery_native_export_test', path)
        native = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(native)
        with patch.dict(os.environ, {'BORG_DEATH_RECORDS_DIR': ''}):
            self.assertEqual(native.registry_dir(), root / 'deaths')
        with tempfile.TemporaryDirectory() as tmp, patch.dict(os.environ, {'BORG_DEATH_RECORDS_DIR': tmp}):
            self.assertEqual(native.registry_dir(), Path(tmp))

    def test_moved_family_algorithm_still_identifies_the_existing_reborn_death(self):
        root = Path(__file__).resolve().parents[1]
        spec = importlib.util.spec_from_file_location('cemetery_family_compatibility', root / 'scripts/native/export-death.py')
        native = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(native)
        case = root / 'deaths/D0007'
        record = json.loads((case / 'record.json').read_text())
        summary = json.loads((case / 'summary.json').read_text())
        family = native.run_family(summary, native.read_kv(case / 'config.txt'), 'rust',
                                   record['identity']['source_sha256'], record['identity']['flags'])
        self.assertEqual(family, record['encounter_family'])


if __name__ == '__main__':
    unittest.main()
