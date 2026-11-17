"""Selection preserves early/town deaths and uses observable encounter onsets."""
import gzip
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from curate_encounters import select, coverage
from harvest_encounters import archive, validate
from synthetic_suite import read, sha


def observed(turn, monsters=(), depth=1, hp=10, max_hp=10):
    return dict(line=turn, turn=turn, s=dict(depth=depth, level=1, hp=hp, max_hp=max_hp, x=1, y=1), monsters=list(monsters))


class CurationTest(unittest.TestCase):
    races = [dict(index=1, name='wild dog'), dict(index=2, name='white worm mass'), dict(index=3, name='battle-scarred veteran')]

    def test_town_death_is_eligible_before_level_two(self):
        mon = dict(index=4, race=3, x=2, y=1)
        result = select([observed(1, depth=0), observed(10, [mon], depth=0), observed(20, [mon], depth=0, hp=1)], [], self.races,
                        dict(dead=True, death_cause='a battle-scarred veteran', game_turns=25))
        self.assertEqual(result['trigger_turn'], 10)
        self.assertIn('unavailable', result['terminal_individual_identity'])

    def test_latest_visible_episode_and_earlier_incoming_message(self):
        mon = dict(index=5, race=1, x=2, y=1)
        result = select([observed(1, [mon]), observed(100), observed(200, [mon]), observed(220, [mon], hp=0)],
                        [dict(turn=195, text='The wild dog bites you.')], self.races,
                        dict(dead=True, death_cause='a wild dog', game_turns=230))
        self.assertEqual(result['trigger_turn'], 195)
        self.assertEqual(result['first_visible_turn'], 200)

    def test_poison_death_selects_contact_before_poison_onset(self):
        mon = dict(index=6, race=2, x=2, y=1)
        result = select([observed(1), observed(10, [mon]), observed(20, [mon], hp=1)],
                        [dict(turn=18, text='The white worm mass crawls on you.'), dict(turn=18, text='You are poisoned!')], self.races,
                        dict(dead=True, death_cause='poison', game_turns=25))
        self.assertEqual(result['trigger_turn'], 10)
        self.assertIn('terminal cause poison', result['selection_basis'])

    def test_invisible_survivor_contact_does_not_invent_a_monster_identity(self):
        result = select([observed(10), observed(20, hp=1)], [dict(turn=15, text='Something touches you.')], self.races, dict(dead=False))
        self.assertEqual(result['trigger_turn'], 15)
        self.assertIn('identity unavailable', result['monster_kind'])

    def test_hp_fraction_change_without_contact_uses_labeled_control(self):
        mon = dict(index=7, race=1, x=2, y=1)
        result = select([observed(1, hp=8), observed(10, hp=8, max_hp=12), observed(1000, [mon])],
                        [dict(turn=1000, text='The wild dog misses you.')], self.races, dict(dead=False))
        self.assertEqual(result['trigger_turn'], 1000)
        self.assertIn('HP-minimum association unavailable', result['selection_basis'])

    def test_compression_preserves_literal_stream_and_hash(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'messages.log'
            raw = b'blank message  \n\x00 literal bytes\n'
            path.write_bytes(raw)
            digest = sha(path)
            receipt = archive(path)
            self.assertFalse(path.exists())
            self.assertEqual(receipt['sha256'], digest)
            self.assertEqual(gzip.open(Path(tmp) / receipt['archive'], 'rb').read(), raw)

    def test_prespecified_harvest_budget_and_duplicate_ids(self):
        spec = read(ROOT / 'synthetic/caster-encounters-v2/harvest-spec.json')
        validate(spec)
        spec['cells'].append(spec['cells'][0])
        with self.assertRaises(ValueError):
            validate(spec)


if __name__ == '__main__':
    unittest.main()
