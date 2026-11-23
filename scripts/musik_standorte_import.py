#!/usr/bin/env python3
"""Import verified production paths from the music copy CSV into SQLite.

Default is read-only dry-run. --write creates a verified SQLite backup and
inserts all rows atomically. Does not modify any audio file.
"""
import argparse
import csv
from datetime import datetime
import os
from pathlib import Path
import sqlite3
import sys

ROOT = Path("/mnt/datensichv/Musiksammlung")
FIELDS = ["sha256", "quelle_aktuell", "ziel", "quellsammlung"]


def prepare(db, plan):
    con = sqlite3.connect(f"file:{db.resolve()}?mode=ro", uri=True)
    try:
        collections = con.execute("SELECT id,root_path FROM collections WHERE role='production'").fetchall()
        if len(collections) != 1 or collections[0] != (5, str(ROOT)):
            raise ValueError(f"Produktionssammlung unerwartet: {collections}")
        hashes = dict(con.execute("SELECT sha256,id FROM audio_files"))
        existing = con.execute("SELECT COUNT(*) FROM file_locations").fetchone()[0]
        if existing:
            raise ValueError(f"file_locations ist nicht leer ({existing} Einträge); kein Import")
        rows = []
        seen_ids = set()
        seen_paths = set()
        with plan.open(encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            if reader.fieldnames != FIELDS:
                raise ValueError("Unerwartete CSV-Kopfzeile")
            for line, row in enumerate(reader, 2):
                if None in row or any(not row.get(field) for field in FIELDS):
                    raise ValueError(f"Ungültige CSV-Zeile {line}")
                sha = row["sha256"].lower()
                audio_id = hashes.get(sha)
                if audio_id is None or audio_id in seen_ids:
                    raise ValueError(f"Fehlende oder doppelte SHA-256-Zuordnung in Zeile {line}")
                dest = Path(row["ziel"])
                if not dest.is_absolute() or ".." in dest.parts or not dest.is_relative_to(ROOT) or dest == ROOT:
                    raise ValueError(f"Ungültiger Zielpfad in Zeile {line}")
                relative = dest.relative_to(ROOT).as_posix()
                if relative in seen_paths:
                    raise ValueError(f"Doppelter Zielpfad in Zeile {line}")
                if dest.is_symlink() or not dest.is_file():
                    raise ValueError(f"Zieldatei fehlt oder ist keine reguläre Datei: {dest}")
                seen_ids.add(audio_id)
                seen_paths.add(relative)
                rows.append((audio_id, 5, relative))
        if len(rows) != len(hashes):
            raise ValueError(f"Unvollständiger Plan: {len(rows)} von {len(hashes)} Dateien")
        return rows
    finally:
        con.close()


def write_database(db, rows):
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = db.with_name(f"{db.stem}-before-locations-{stamp}{db.suffix}")
    if backup.exists():
        raise ValueError(f"Sicherungsdatei existiert bereits: {backup}")
    source = sqlite3.connect(f"file:{db.resolve()}?mode=ro", uri=True)
    try:
        with sqlite3.connect(str(backup)) as target:
            source.backup(target)
    except Exception:
        backup.unlink(missing_ok=True)
        raise
    finally:
        source.close()
    check = sqlite3.connect(f"file:{backup.resolve()}?mode=ro", uri=True)
    try:
        if check.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
            raise ValueError("Sicherung hat Integritätsprüfung nicht bestanden")
        if check.execute("SELECT COUNT(*) FROM file_locations").fetchone()[0] != 0:
            raise ValueError("Sicherung enthält unerwartete Standorte")
    finally:
        check.close()
    print(f"Verifizierte Datenbanksicherung: {backup}", flush=True)
    con = sqlite3.connect(db)
    try:
        con.execute("PRAGMA foreign_keys=ON")
        con.execute("BEGIN IMMEDIATE")
        if con.execute("SELECT COUNT(*) FROM file_locations").fetchone()[0]:
            raise ValueError("Zwischenzeitlich eingetragene Standorte: Abbruch")
        con.executemany("""INSERT INTO file_locations
            (audio_file_id,collection_id,relative_path,status,last_verified_at)
            VALUES (?,?,?,'present',CURRENT_TIMESTAMP)""", rows)
        count = con.execute("SELECT COUNT(*) FROM file_locations WHERE collection_id=5 AND status='present'").fetchone()[0]
        if count != len(rows) or con.execute("PRAGMA foreign_key_check").fetchall():
            raise ValueError("Kontrollprüfung der Einträge fehlgeschlagen")
        con.commit()
        print(f"Import erfolgreich: {count} Produktionsstandorte eingetragen")
    except Exception:
        con.rollback()
        raise
    finally:
        con.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database", type=Path, default=Path.home() / "Musiksammlung_work/musiksammlung.sqlite")
    parser.add_argument("--plan", type=Path, default=Path.home() / "Musiksammlung_work/musik-kopierplan.csv")
    parser.add_argument("--write", action="store_true", help="Nach Sicherung in Datenbank schreiben")
    args = parser.parse_args()
    try:
        rows = prepare(args.database, args.plan)
        print(f"Prüfung erfolgreich: {len(rows)} vorhandene Zielpfade, eindeutige SHA-256-Zuordnung")
        print("Hinweis: Es werden keine neuen Datei-Prüfsummen berechnet.")
        if args.write:
            write_database(args.database, rows)
        else:
            print("DRY-RUN: Keine Datenbank- oder Musikdateien verändert")
    except (OSError, ValueError, sqlite3.Error) as e:
        print(f"ABBRUCH: {e}", file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
