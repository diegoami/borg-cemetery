"""Distinct observable episodes require actual combat/targeting evidence."""
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from expand_encounters import discover
from synthetic_suite import write


class DiscoveryTest(unittest.TestCase):
    def test_no_repeated_frame_padding_and_all_failed_lives_visible(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            run = root / 'life'
            (run / 'checkpoints').mkdir(parents=True)
            write(root / 'harvest.json', dict(attempts=[dict(id='life', status='survived_cap', summary=dict(game_turns=100)),
                                                       dict(id='failed-life', status='harness_failure')]))
            write(run / 'knowledge.json', dict(races=[dict(index=1, name='wild dog')]))
            observations = []
            for turn, indices in [(10, [1]), (20, [1]), (30, []), (40, [1, 2]), (50, [2]), (60, [3])]:
                observations.append(dict(turn=turn, status=dict(depth=1, level=1, hp=10),
                                         monsters=[dict(index=i, race=1) for i in indices]))
            import json
            (run / 'observations.jsonl').write_text(''.join(json.dumps(o) + '\n' for o in observations))
            (run / 'messages.log').write_text('1 20 0 The wild dog is targeted.\n2 45 0 The wild dog bites you.\n')
            (run / 'checkpoints/index.jsonl').write_text(''.join(json.dumps(dict(file=f'{turn}.save', game_turn=turn, clevel=1)) + '\n' for turn in (9, 39, 59)))
            results = discover(root, root / 'discovery.json')
            self.assertEqual(len(results[0]['selected']), 2)
            self.assertEqual([e['trigger'] for e in results[0]['selected']], [10, 40])
            self.assertEqual(results[1]['status'], 'failed')


if __name__ == '__main__':
    unittest.main()
