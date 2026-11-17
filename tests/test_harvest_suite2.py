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
