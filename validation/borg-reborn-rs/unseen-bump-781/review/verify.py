#!/usr/bin/env python3
import gzip
import hashlib
import json
from pathlib import Path
root = Path(__file__).resolve().parent
receipt = json.loads((root / 'receipts.json').read_text())
for attempt in receipt['attempts']:
    for meta in attempt['files'].values():
        path = root / meta['stored']
        raw = path.read_bytes()
        if path.suffix == '.gz':
            raw = gzip.decompress(raw)
        assert len(raw) == meta['bytes'], path
        assert hashlib.sha256(raw).hexdigest() == meta['sha256'], path
    process = json.loads((root / attempt['files']['process.json']['stored']).read_text())
    assert process['status'] == attempt['process_status']
    assert process['executable_sha256_before'] == process['executable_sha256_after'] == attempt['binary_sha256']
    if attempt['harness_status'] == 'success':
        assert process['status'] == 'success'
    elif attempt['harness_status'] == 'missing_game_data':
        assert process['status'] == 'exit_failure'
print(f"Verified {len(receipt['attempts'])} attempts, including operational failures")
