#!/usr/bin/env python3
"""Check retained attempt bytes; receipts hash uncompressed originals."""
import gzip
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parent
receipt = json.loads((root / 'receipts.json').read_text())
for attempt in receipt['attempts']:
    for metadata in attempt['files'].values():
        path = root / metadata['stored']
        raw = path.read_bytes()
        if path.suffix == '.gz':
            raw = gzip.decompress(raw)
        assert len(raw) == metadata['bytes'], path
        assert hashlib.sha256(raw).hexdigest() == metadata['sha256'], path
    process = json.loads((root / attempt['files']['process.json']['stored']).read_text())
    assert process['status'] == attempt['process_status'] == 'success'
    assert process['executable_sha256_before'] == process['executable_sha256_after'] == attempt['binary_sha256']
print(f"Verified {len(receipt['attempts'])} attempts; repeats are not independent lives")
