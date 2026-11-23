#!/usr/bin/env python3
"""Read-only validation of two sha256sum -z inventories; never reads audio files."""
import argparse
from collections import Counter
from pathlib import Path
import sys

ROOTS = {
    'miniitx': '/mnt/datensichv/miniitx/Musik',
    'von_media': '/mnt/datensichv/von_media/Musik',
    'vonaspirev5': '/mnt/datensichv/vonaspirev5/Musik',
    'ds_musik': '/media/oscheil/TV/ds_musik',
}
HEX = frozenset(b'0123456789abcdef')


def parse_inventory(path, allowed):
    raw = path.read_bytes()
    if not raw.endswith(b'\0'):
        raise ValueError(f'{path}: missing final NUL terminator')
    counts = Counter()
    hashes = set()
    seen_paths = {}
    for index, record in enumerate(raw.split(b'\0')[:-1], 1):
        if len(record) < 67 or record[64:66] != b'  ' or any(b not in HEX for b in record[:64]):
            raise ValueError(f'{path}: invalid record {index}')
        digest = record[:64].decode('ascii')
        original_bytes = record[66:]
        if not original_bytes or b'\0' in original_bytes:
            raise ValueError(f'{path}: empty path at record {index}')
        # Preserve exact path bytes for a later import using surrogateescape.
        matches = [name for name in allowed if original_bytes.startswith(ROOTS[name].encode() + b'/')]
        if len(matches) != 1:
            display = original_bytes.decode('utf-8', 'backslashreplace')
            raise ValueError(f'{path}: unrecognized source path at record {index}: {display[:160]}')
        key = (matches[0], original_bytes)
        if key in seen_paths:
            if seen_paths[key] != digest:
                raise ValueError(f'{path}: conflicting hashes for one path at record {index}')
            raise ValueError(f'{path}: duplicate path at record {index}')
        seen_paths[key] = digest
        counts[matches[0]] += 1
        hashes.add(digest)
    return counts, hashes, len(seen_paths)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--datensichv', type=Path, default=Path.home() / 'musik-pruefsummen.sha256z')
    p.add_argument('--tv', type=Path, default=Path.home() / 'musik-terra11.sha256z')
    args = p.parse_args()
    a_counts, a_hashes, a_n = parse_inventory(args.datensichv, ('miniitx', 'von_media', 'vonaspirev5'))
    b_counts, b_hashes, b_n = parse_inventory(args.tv, ('ds_musik',))
    print('DRY-RUN – no database or music files written')
    for name in ROOTS:
        print(f'{name:14s} {a_counts[name] + b_counts[name]:>8,d} source paths')
    print(f'Total origin paths:        {a_n + b_n:,}')
    print(f'Unique SHA-256 contents:   {len(a_hashes | b_hashes):,}')
    print(f'Identical extra copies:    {a_n + b_n - len(a_hashes | b_hashes):,}')
    print(f'Only on TV (by hash):      {len(b_hashes - a_hashes):,}')
    print(f'Only on DATENSICHV:        {len(a_hashes - b_hashes):,}')
    print(f'In both inventories:       {len(a_hashes & b_hashes):,}')
    print('Original path bytes validated; no paths normalized or renamed.')

if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        sys.exit(1)
