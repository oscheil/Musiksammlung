#!/usr/bin/env python3
"""Read-only size and accessibility inventory for music consolidation."""
import argparse
from collections import Counter
import os
from pathlib import Path
import sqlite3
import stat

OLD_TV = '/media/oscheil/TV/ds_musik/'
CURRENT_TV = '/mnt/tv-musik/ds_musik/'

def actual_path(origin):
    if origin.startswith(OLD_TV):
        return CURRENT_TV + origin[len(OLD_TV):]
    return origin

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--database', type=Path, default=Path.home() / 'Musiksammlung_work/musiksammlung.sqlite')
    parser.add_argument('--destination-parent', type=Path, default=Path('/mnt/datensichv'))
    args = parser.parse_args()
    con = sqlite3.connect('file:' + str(args.database.resolve()) + '?mode=ro', uri=True)
    try:
        rows = con.execute("""SELECT a.sha256, c.name, o.original_path
            FROM file_origins AS o
            JOIN audio_files AS a ON a.id=o.audio_file_id
            JOIN collections AS c ON c.id=o.collection_id
            ORDER BY a.sha256, CASE WHEN c.name='ds_musik' THEN 1 ELSE 0 END, o.id""")
        origins = reachable = distinct = sourced = size_bytes = allocated_bytes = inconsistent = 0
        missing, inaccessible = Counter(), Counter()
        last_digest = None
        sizes = set()
        chosen_size = chosen_blocks = None

        def finish():
            nonlocal sourced, size_bytes, allocated_bytes, inconsistent
            if chosen_size is not None:
                sourced += 1
                size_bytes += chosen_size
                allocated_bytes += chosen_blocks
            if len(sizes) > 1:
                inconsistent += 1

        for digest, collection, origin in rows:
            if digest != last_digest:
                if last_digest is not None:
                    finish()
                distinct += 1
                last_digest = digest
                sizes = set()
                chosen_size = chosen_blocks = None
            origins += 1
            try:
                st = os.stat(actual_path(origin), follow_symlinks=False)
                if not stat.S_ISREG(st.st_mode):
                    inaccessible[collection] += 1
                    continue
            except FileNotFoundError:
                missing[collection] += 1
                continue
            except OSError:
                inaccessible[collection] += 1
                continue
            reachable += 1
            sizes.add(st.st_size)
            if chosen_size is None:
                chosen_size = st.st_size
                chosen_blocks = st.st_blocks * 512
        if last_digest is not None:
            finish()
        vfs = os.statvfs(args.destination_parent)
        free_bytes = vfs.f_bavail * vfs.f_frsize
        print('NUR LESEND – keine Audiodateien geöffnet, kopiert oder verändert')
        print(f'Herkunftspfade in Datenbank:          {origins:,}')
        print(f'Davon aktuell erreichbar:            {reachable:,}')
        print(f'Eindeutige SHA-256-Inhalte:          {distinct:,}')
        print(f'Davon mit erreichbarer Quelldatei:   {sourced:,}')
        print(f'Ohne erreichbare Quelldatei:         {distinct-sourced:,}')
        print(f'Summe logischer Dateigrößen:         {size_bytes / 1024**3:.2f} GiB')
        print(f'Quell-Belegung (nur Näherung):       {allocated_bytes / 1024**3:.2f} GiB')
        print(f'Freier Platz auf Ziel-Dateisystem:  {free_bytes / 1024**3:.2f} GiB')
        print(f'Hashes mit abweichenden Größen:     {inconsistent:,}')
        for label, counts in [('Fehlende Herkunftspfade', missing), ('Nicht regulär/kein Zugriff', inaccessible)]:
            print(label + ': ' + (', '.join(f'{k}={v}' for k, v in sorted(counts.items())) if counts else 'keine'))
        print('Hinweis: Größen beruhen auf stat, nicht auf erneuter SHA-256-Prüfung.')
        print('Hinweis: Der tatsächliche Platzbedarf beim Kopieren hängt von Dateisystem und Zielstruktur ab.')
    finally:
        con.close()

if __name__ == '__main__':
    main()
