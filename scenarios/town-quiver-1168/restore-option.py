from pathlib import Path
import gzip
import struct
import sys

original, town, target = map(Path, sys.argv[1:])

def read(path):
    return bytearray(gzip.decompress(path.read_bytes()) if path.suffix == '.gz' else path.read_bytes())

def option(data, key):
    assert data[:8] == b'SaveVNLA'
    offset = 8
    while offset < len(data):
        name, version, size, checksum = struct.unpack_from('<16sIII', data, offset)
        payload = offset + 28
        if name.rstrip(b'\0') == b'options':
            end = payload + size
            assert version == 1 and sum(data[payload:end]) == checksum
            index = data.index(b'\0' + key + b'\0', payload, end) + len(key) + 2
            return index, offset + 24, checksum
        offset = payload + ((size + 3) & ~3)
    raise ValueError("options block missing")

original_data = read(original)
native = original_data[option(original_data, b'auto_more')[0]]
assert native == 0
data = read(town)
index, checksum_at, checksum = option(data, b'auto_more')
assert data[index] == 1
data[index] = native
struct.pack_into('<I', data, checksum_at, checksum - 1)
with target.open('xb') as out:
    out.write(data)
