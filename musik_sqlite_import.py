#!/usr/bin/env python3
"""Import SHA-256 inventories into a NEW SQLite database; never opens audio files."""
import argparse
from collections import Counter
from pathlib import Path
import sqlite3
import sys

ROOTS = {
    'miniitx': b'/mnt/datensichv/miniitx/Musik/',
    'von_media': b'/mnt/datensichv/von_media/Musik/',
    'vonaspirev5': b'/mnt/datensichv/vonaspirev5/Musik/',
    'ds_musik': b'/media/oscheil/TV/ds_musik/',
}
HEX = frozenset(b'0123456789abcdef')


def parse(path, names):
    raw = path.read_bytes()
    if not raw.endswith(b'\0'):
        raise ValueError(f'{path}: abschliessendes NUL fehlt')
    seen = set()
    for number, record in enumerate(raw.split(b'\0')[:-1], 1):
        if len(record) < 67 or record[64:66] != b'  ' or any(x not in HEX for x in record[:64]):
            raise ValueError(f'{path}: ungueltiger Datensatz {number}')
        digest = record[:64].decode('ascii')
        path_bytes = record[66:]
        matches = [name for name in names if path_bytes.startswith(ROOTS[name]) and len(path_bytes) > len(ROOTS[name])]
        if len(matches) != 1:
            raise ValueError(f'{path}: unbekannter Herkunftspfad in Datensatz {number}')
        key = (matches[0], path_bytes)
        if key in seen:
            raise ValueError(f'{path}: doppelter Herkunftspfad in Datensatz {number}')
        seen.add(key)
        # SQLite TEXT requires valid UTF-8. Reject unusual raw bytes rather than corrupt paths.
        try:
            original_path = path_bytes.decode('utf-8', 'strict')
        except UnicodeDecodeError as exc:
            raise ValueError(f'{path}: Pfad in Datensatz {number} ist kein UTF-8') from exc
        yield matches[0], digest, original_path


def collect(datensichv, tv):
    rows = list(parse(datensichv, ('miniitx', 'von_media', 'vonaspirev5')))
    rows.extend(parse(tv, ('ds_musik',)))
    hashes = {digest for _, digest, _ in rows}
    counts = Counter(name for name, _, _ in rows)
    return rows, hashes, counts


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--datensichv', type=Path, default=Path.home() / 'musik-pruefsummen.sha256z')
    ap.add_argument('--tv', type=Path, default=Path.home() / 'musik-terra11.sha256z')
    ap.add_argument('--schema', type=Path, required=True)
    ap.add_argument('--database', type=Path, required=True, help='Neuer, noch nicht existierender Datenbankpfad')
    ap.add_argument('--write', action='store_true', help='Nur mit dieser Option eine neue Datenbank erzeugen')
    args = ap.parse_args()
    rows, hashes, counts = collect(args.datensichv, args.tv)
    print(f'Herkunftspfade: {len(rows)}; SHA-256-Inhalte: {len(hashes)}')
    for name in ROOTS:
        print(f'  {name}: {counts[name]}')
    if not args.write:
        print('DRY-RUN: Keine Datenbank erstellt. --write ist fuer den Import erforderlich.')
        return
    if args.database.exists():
        raise ValueError(f'Zieldatenbank existiert bereits: {args.database}')
    schema = args.schema.read_text(encoding='utf-8')
    # Atomic creation: SQLite uses a new exclusive file; never overwrite an existing database.
    import os
    fd = os.open(args.database, os.O_RDWR | os.O_CREAT | os.O_EXCL, 0o600)
    os.close(fd)
    try:
        con = sqlite3.connect(args.database)
        try:
            con.executescript(schema)
            if con.execute('SELECT version FROM schema_version').fetchone() != (2,):
                raise ValueError('Schema ist nicht Version 2')
            ids = dict(con.execute('SELECT name, id FROM collections'))
            if set(ROOTS) - set(ids):
                raise ValueError('Quellsammlungen fehlen im Schema')
            con.execute('BEGIN')
            con.executemany('INSERT INTO audio_files(sha256) VALUES (?)', ((h,) for h in sorted(hashes)))
            hash_ids = dict(con.execute('SELECT sha256, id FROM audio_files'))
            con.executemany('INSERT INTO file_origins(audio_file_id, collection_id, original_path) VALUES (?,?,?)',
                            ((hash_ids[digest], ids[name], path) for name, digest, path in rows))
            if con.execute('PRAGMA foreign_key_check').fetchall():
                raise ValueError('Fremdschluesselpruefung fehlgeschlagen')
            con.commit()
            actual = (con.execute('SELECT count(*) FROM audio_files').fetchone()[0],
                      con.execute('SELECT count(*) FROM file_origins').fetchone()[0])
            if actual != (len(hashes), len(rows)):
                raise ValueError(f'Zaehler stimmen nicht: {actual}')
            print(f'Import erfolgreich: {actual[0]} audio_files, {actual[1]} file_origins')
        finally:
            con.close()
    except Exception:
        # Never delete a possibly useful failed database silently.
        print(f'Import nicht abgeschlossen; Zieldatei bitte pruefen: {args.database}', file=sys.stderr)
        raise


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, sqlite3.Error) as error:
        print(f'FEHLER: {error}', file=sys.stderr)
        sys.exit(1)
