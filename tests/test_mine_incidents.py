"""Near-death candidates require damage and observed recovery, not a ratio alone."""
from pathlib import Path
import json
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from mine_incidents import load_frames, onset


class IncidentTest(unittest.TestCase):
    def frames(self, states):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'frames.jsonl'
            rows=[]
            for t,hp,maxhp in states:
                rows.append(dict(turn=t,status=dict(hp=hp,max_hp=maxhp,sp=0,max_sp=2,level=1,depth=1),monsters=[]))
            p.write_text(''.join(json.dumps(r)+'\n' for r in rows))
            return load_frames(p)

    def test_actual_low_hp_and_recovery_are_required(self):
        _,_,recoveries=self.frames([(1,8,8),(10,2,8),(20,1,8),(30,4,8)])
        self.assertEqual(len(recoveries),1)
        self.assertEqual(recoveries[0]['minimum']['hp'],1)
        self.assertEqual(recoveries[0]['recovery']['hp'],4)

    def test_levelup_ratio_change_is_not_a_near_death(self):
        self.assertEqual(self.frames([(1,2,4),(10,2,10),(20,8,10)])[2],[])

    def test_unrecovered_fatal_episode_is_not_called_a_survival(self):
        self.assertEqual(self.frames([(1,8,8),(10,1,8),(20,-1,8)])[2],[])

    def test_living_zero_hp_is_retained(self):
        r=self.frames([(1,2,8),(10,0,8),(20,5,8)])[2]
        self.assertEqual(r[0]['minimum']['hp'],0)

    def test_visible_onset_is_not_the_final_low_hp_action(self):
        episodes=[dict(race=1,index=3,depth=1,first=10,last=100,line=1)]
        selected=onset(episodes,[],[dict(index=1,name='wild dog')],100,'a wild dog')
        self.assertEqual(selected['trigger_turn'],10)

    def test_balance_is_exactly_111_for_all_nine_classes(self):
        spec=json.loads((ROOT/'synthetic/balanced-999-incidents/harvest-spec.json').read_text())
        self.assertEqual(spec['classes'],list(range(9)))
        self.assertEqual(spec['target_per_class']*len(spec['classes']),999)


if __name__=='__main__':unittest.main()
