"""Preserve provenance and avoid promoting observations to executable state."""
import json
import subprocess
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import caster_candidates as c


class CandidatesTest(unittest.TestCase):
    def test_projection_excludes_hidden_gear_and_missing_stays_missing(self):
        row = c.observation(dict(turn=4, hp=2, max_hp=10, dead=0,
                                 details=dict(gear=[dict(actual_kind='Teleportation')]),
                                 inventory=dict(pack=[dict(description='an unknown scroll',
                                                           actual_kind='Teleportation')]),
                                 spells=None))
        self.assertTrue(row['low_hp_candidate'])
        self.assertNotIn('Teleportation', json.dumps(row))
        self.assertEqual(row['missing'], ['spells'])
        for hp, maximum in [(-1, 10), (2, 0), (True, 10), (None, 10)]:
            self.assertFalse(c.observation(dict(hp=hp, max_hp=maximum, dead=0))['low_hp_candidate'])
        self.assertTrue(c.observation(dict(hp=0, max_hp=10, dead=0))['low_hp_candidate'])
        self.assertFalse(c.observation(dict(hp=0, max_hp=10, dead=1))['low_hp_candidate'])
        self.assertFalse(c.observation(dict(hp=0, max_hp=10))['low_hp_candidate'])

    def test_spell_diagnostics_are_removed_at_both_levels(self):
        result = c.observation(dict(spells={'class': 'Mage', 'hidden_rng': 12,
            'learned': [{'name': 'Magic Missile', 'mana': 1, 'hidden_target_hp': 50}]}))
        self.assertEqual(result['spells'], {'class': 'Mage', 'learned': [
            {'name': 'Magic Missile', 'mana': 1}]})

    def test_normalization_separates_equipment_from_pack_resources(self):
        first = [dict(description='a Wooden Torch (663 turns)', weight=10)]
        second = [dict(description='10 Wooden Torches (5000 turns)', weight=100)]
        self.assertEqual(c.normalized_items(first), c.normalized_items(second))
        self.assertNotEqual(c.normalized_items([dict(description='a Shield [2,+0]')]),
                            c.normalized_items([dict(description='a Shield [2,+1]')]))
        observations = [dict(inventory=dict(equipment=first, pack=first)),
                        dict(inventory=dict(equipment=first, pack=second))]
        self.assertEqual(len(c.normalized_sets(observations, 'equipment')), 1)
        self.assertEqual(len(c.normalized_sets(observations, 'pack')), 1)
        observations[1]['inventory']['pack'] = [dict(description='a Potion of Speed')]
        self.assertEqual(len(c.normalized_sets(observations, 'pack')), 2)

    def test_hashes_loadout_deduplication_and_level_filter(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            case = root / 'deaths/caster'
            case.mkdir(parents=True)
            frames = []
            for turn, level in [(10, 1), (20, 1), (30, 11)]:
                frame = case / f'{turn}.json'
                frame.write_text(json.dumps(dict(turn=turn, level=level, hp=2, max_hp=10,
                                                 inventory=dict(pack=[]), spells={'class': 'Mage'})))
                frames.append(dict(json=frame.name, json_sha256=c.digest(frame)))
            record = case / 'record.json'
            record.write_text(json.dumps(dict(recording=dict(selected_original_frames=frames))))
            result = c.collect(root)
            self.assertEqual(len(result['cases']), 1)
            result = result['cases'][0]
            self.assertEqual(len(result['observations']), 2)
            self.assertEqual(len(result['observed_loadouts']), 1)
            self.assertFalse(result['original_continuation_verified'])
            self.assertEqual(result['execution_status'], 'requires_caster_build_adapter')
            (case / '10.json').write_text('{}')
            with self.assertRaisesRegex(ValueError, 'hash mismatch'):
                c.collect(root)

    def test_missing_digest_is_explicitly_excluded(self):
        with tempfile.TemporaryDirectory() as tmp:
            case = Path(tmp) / 'deaths/caster'
            case.mkdir(parents=True)
            (case / 'record.json').write_text(json.dumps(dict(recording=dict(
                selected_original_frames=[dict(json='missing.json')]))))
            result = c.collect(Path(tmp))
            self.assertEqual(result['cases'], [])
            self.assertEqual(result['excluded_frames'][0]['reason'], 'no_published_frame_digest')

    def test_save_integrity_and_unknown_level(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            scenario = root / 'scenarios/mage'
            scenario.mkdir(parents=True)
            save = scenario / 'start.save.gz'
            save.write_bytes(b'retained test bytes')
            (scenario / 'scenario.json').write_text(json.dumps(dict(class_idx=1,
                save=save.name, compressed_sha256=c.digest(save), event_kind='near_death_candidate')))
            row = c.collect(root)['saved_scenarios'][0]
            self.assertIsNone(row['level'])
            self.assertFalse(row['independent_life'])
            save.write_bytes(b'changed')
            with self.assertRaisesRegex(ValueError, 'hash mismatch'):
                c.collect(root)

    def test_missing_frames_and_missing_spells_are_visible(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            case = root / 'deaths/mage'
            case.mkdir(parents=True)
            record = dict(character='Hobbit Mage', terminal=dict(level=3, class_idx=1))
            path = case / 'record.json'
            path.write_text(json.dumps(record))
            row = c.collect(root)['unobserved_cases'][0]
            self.assertEqual(row['status'], 'no_recorded_frames')
            self.assertIsNone(row['inventory'])
            frame = case / 'frame.json'
            frame.write_text(json.dumps(dict(turn=10, level=3, dead=0, hp=0, max_hp=10)))
            record['recording'] = dict(selected_original_frames=[dict(
                json=frame.name, json_sha256=c.digest(frame))])
            path.write_text(json.dumps(record))
            row = c.collect(root)['cases'][0]['observations'][0]
            self.assertIn('spells', row['missing'])
            self.assertEqual(row['class_basis'], 'record_metadata')
            self.assertTrue(row['low_hp_candidate'])
            record.update(character='Unknown', terminal={})
            path.write_text(json.dumps(record))
            self.assertEqual(c.collect(root)['excluded_frames'][0]['reason'], 'class_unavailable')
            record.update(character='Hobbit Mage', terminal=dict(level=3, class_idx=1))
            frame.write_text(json.dumps(dict(turn=10, level=3, spells={'class': 'Priest'})))
            record['recording']['selected_original_frames'][0]['json_sha256'] = c.digest(frame)
            path.write_text(json.dumps(record))
            self.assertEqual(c.collect(root)['excluded_frames'][0]['reason'], 'class_metadata_conflict')

    def test_untracked_inputs_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            subprocess.run(['git', 'init', '-q', str(root)], check=True)
            (root / 'deaths').mkdir()
            (root / 'deaths/untracked.json').write_text('{}')
            with self.assertRaisesRegex(ValueError, 'untracked changes'):
                c.require_clean_inputs(root)


if __name__ == '__main__':
    unittest.main()
