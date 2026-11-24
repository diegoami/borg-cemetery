#!/usr/bin/env python3
"""Copy an Angband save with auto_more enabled for a headless restart."""
import argparse
import gzip
import struct
from pathlib import Path


def with_auto_more(raw):
    data = bytearray(raw)
    if not data.startswith(b"SaveVNLA"):
        raise ValueError("Unexpected Angband save signature")
    offset = 8
    while offset < len(data):
        name, version, size, checksum = struct.unpack_from("<16sIII", data, offset)
        start = offset + 28
        end = start + size
        if end > len(data):
            raise ValueError("Truncated Angband save block")
        if name.rstrip(b"\x00") == b"options":
            if version != 1 or sum(data[start:end]) != checksum:
                raise ValueError("Unexpected options block version or checksum")
            key = b"\x00auto_more\x00"
            value = data.index(key, start, end) + len(key)
            if value >= end or data[value] not in (0, 1):
                raise ValueError("Invalid auto_more value")
            if not data[value]:
                data[value] = 1
                struct.pack_into("<I", data, offset + 24, checksum + 1)
            return data
        offset = start + ((size + 3) & ~3)
    raise ValueError("Missing options block")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("original", type=Path, help="Native .save or .save.gz")
    parser.add_argument("private_save", type=Path, help="New .save path")
    args = parser.parse_args()
    raw = args.original.read_bytes()
    if args.original.suffix == ".gz":
        raw = gzip.decompress(raw)
    prepared = with_auto_more(raw)
    with args.private_save.open("xb") as target:
        target.write(prepared)


if __name__ == "__main__":
    main()
