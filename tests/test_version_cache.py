import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import case_replay as replay


class VersionCacheTest(unittest.TestCase):
    def test_checkout_cache_reuses_existing_user_cache_without_moving_it(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            legacy = root / 'user-cache/borg-cemetery'
            legacy.mkdir(parents=True)
            (legacy / 'version').write_text('existing recording bindings remain valid')
            checkout = root / 'checkout'
            checkout.mkdir()
            with patch.dict(os.environ, {'XDG_CACHE_HOME': str(root / 'user-cache'), 'BORG_CEMETERY_CACHE': ''}):
                cache = replay.default_cache(checkout)
                self.assertTrue(cache.is_symlink())
                self.assertEqual(cache.resolve(), legacy)
                self.assertTrue((cache / 'version').is_file())
                self.assertEqual(replay.default_cache(checkout), cache)

    def test_original_version_is_built_once_and_shared_between_cases(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / 'source'
            binary = source / 'build/rust/game/angband'
            selected = dict(program='borg-rs', source='a' * 40)
            def build(*args, **kwargs):
                binary.parent.mkdir(parents=True)
                binary.write_bytes(b'one pinned executable')
            with patch.object(replay, 'checkout', return_value=source) as checkout, patch.object(replay, 'run', side_effect=build) as compiler:
                first = replay.original_build(root, selected)
                second = replay.original_build(root, dict(selected, case='another-death'))
                self.assertEqual(first, second)
                self.assertEqual(compiler.call_count, 1)
                self.assertEqual(checkout.call_count, 1)
            binary.write_bytes(b'changed')
            with patch.object(replay, 'run') as compiler:
                with self.assertRaisesRegex(ValueError, 'Cached executable changed'):
                    replay.original_build(root, selected)
                compiler.assert_not_called()

    def test_interrupted_recorder_tool_build_does_not_rebuild_game(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / 'source'
            folder = root / 'recorder-runtime' / replay.RECORDER_SOURCE
            binary = folder / 'engine/game/angband'
            recorder = folder / 'tools/release/angband-recorder'
            calls = []
            def build(argv, **kwargs):
                calls.append([str(v) for v in argv])
                if argv[:2] == ['cmake', '--build']:
                    binary.parent.mkdir(parents=True)
                    binary.write_bytes(b'game phase')
                if argv[0] == 'cargo':
                    if sum(c[0] == 'cargo' for c in calls) == 1:
                        raise OSError('interrupted tool build')
                    recorder.parent.mkdir(parents=True)
                    recorder.write_bytes(b'recorder CLI')
            with patch.object(replay, 'checkout', return_value=source), patch.object(replay, 'run', side_effect=build):
                with self.assertRaisesRegex(OSError, 'interrupted'):
                    replay.recorder_build(root, 1)
                replay.recorder_build(root, 1)
            self.assertEqual(sum(c[:2] == ['cmake', '--build'] for c in calls), 1)
            with patch.object(replay, 'run') as compiler, patch.object(replay, 'checkout') as checkout:
                replay.recorder_build(root, 1)
                compiler.assert_not_called()
                checkout.assert_not_called()


if __name__ == '__main__':
    unittest.main()
