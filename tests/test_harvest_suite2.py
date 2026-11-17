"""Harvest identities and cross-bank deduplication fail before gameplay."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import json
import tempfile
import unittest
from unittest.mock import patch
import harvest_incidents as h

class Suite2HarvestTests(unittest.TestCase):
    def test_changed_exclusion_rejected_before_any_game(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);spec=root/'spec.json';excluded=root/'exclude.json'
            excluded.write_text('{}')
            spec.write_text(json.dumps({'exclusion':{'path':'exclude.json','sha256':'0'*64}}))
            with patch.object(h,'one') as one:
                with self.assertRaisesRegex(ValueError,'exclusion inventory changed'):
                    h.run(spec,root/'source',root/'out',0,root/'tools')
                one.assert_not_called()

    def test_overlapping_source_seeds_rejected_before_any_game(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);spec=root/'spec.json';excluded=root/'exclude.json'
            excluded.write_text(json.dumps({'save_sha256':[],'source_seeds':[2000000]}))
            spec.write_text(json.dumps({'exclusion':{'path':'exclude.json','sha256':h.sha(excluded)},
                                       'seed_base':2000000,'max_attempts_per_class':1}))
            with patch.object(h,'one') as one:
                with self.assertRaisesRegex(ValueError,'source seeds overlap'):
                    h.run(spec,root/'source',root/'out',0,root/'tools')
                one.assert_not_called()

    def test_missing_capture_interface_rejected_before_gameplay(self):
        with tempfile.TemporaryDirectory() as temp:
            source=Path(temp)
            with self.assertRaisesRegex(ValueError,'lacks BORG_ENCOUNTER_LOG'):
                h.require_capture_support(source,{'suite_id':'suite2-v1','core':'borg-rs'})
            # Legacy definitions retain their historical execution path.
            h.require_capture_support(source,{})

    def test_storage_bound_preserves_shortage_journal_without_starting_game(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);source=root/'source';tools=root/'tools';out=root/'out'
            binary=source/'build/rust/game/angband';binary.parent.mkdir(parents=True);binary.write_bytes(b'fake')
            build=source/'build/rust/BUILD_ID';build.write_text('git_rev='+('a'*40)+'\nsource_sha256='+('b'*64)+'\nbinary_sha256='+h.sha(binary)+'\n')
            spec=root/'spec.json';spec.write_text(json.dumps(dict(source_commit='a'*40,native_tools_commit='c'*40,
                target_per_class=111,workers=1,seed_base=2000000,max_attempts_per_class=1024,max_retained_bytes_per_class=1)))
            with patch.object(h.subprocess,'check_output',side_effect=['c'*40+'\n','a'*40+'\n','b'*64+'\n']),patch.object(h,'one') as game:
                result=h.run(spec,source,out,0,tools)
            game.assert_not_called()
            self.assertEqual(result['selected'],[])
            self.assertEqual(result['stop_reason'],'retained_evidence_budget')
            self.assertEqual(json.loads((out/'harvest.json').read_text())['target'],111)
