#!/usr/bin/env python3
"""SHA-256-verified, resumable music copy from the exported CSV plan.

Default: dry run. --write explicitly enables copying. Never modifies sources.
"""
import argparse
import csv
import hashlib
import os
from pathlib import Path
import stat
import sys
import uuid

FIELDS = ["sha256", "quelle_aktuell", "ziel", "quellsammlung"]
TARGET_ROOT = Path("/mnt/datensichv/Musiksammlung")
CHUNK = 1024 * 1024


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(CHUNK), b""):
            h.update(block)
    return h.hexdigest()


def validate_plan(path):
    rows = []
    destinations = set()
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != FIELDS:
            raise ValueError("Unerwartete CSV-Spalten")
        for number, row in enumerate(reader, 2):
            if None in row or any(not row.get(k) for k in FIELDS):
                raise ValueError(f"Ungültige CSV-Zeile {number}")
            sha = row["sha256"].lower()
            if len(sha) != 64 or any(c not in "0123456789abcdef" for c in sha):
                raise ValueError(f"Ungültiger SHA-256 in Zeile {number}")
            src = Path(row["quelle_aktuell"])
            dst = Path(row["ziel"])
            if not src.is_absolute() or not dst.is_absolute() or ".." in dst.parts:
                raise ValueError(f"Ungültiger Pfad in Zeile {number}")
            if not dst.is_relative_to(TARGET_ROOT) or dst == TARGET_ROOT:
                raise ValueError(f"Ziel außerhalb der Musiksammlung in Zeile {number}")
            if dst in destinations:
                raise ValueError(f"Doppelter Zielpfad in Zeile {number}")
            destinations.add(dst)
            rows.append((sha, src, dst))
    if not rows:
        raise ValueError("Leerer Kopierplan")
    return rows


def ensure_safe_parents(dst, create):
    # No symlink may redirect a destination directory.
    for parent in reversed(dst.parents):
        if parent == Path("/"):
            continue
        try:
            mode = parent.lstat().st_mode
        except FileNotFoundError:
            if create:
                parent.mkdir(exist_ok=True)
                mode = parent.lstat().st_mode
            else:
                continue
        if not stat.S_ISDIR(mode):
            raise RuntimeError(f"Ziel-Pfadkomponente ist kein echtes Verzeichnis: {parent}")


def run(rows, write):
    copied = skipped = 0
    print(f"Modus: {'KOPIEREN' if write else 'DRY-RUN'}; Plan: {len(rows)} Dateien", flush=True)
    for index, (sha, src, dst) in enumerate(rows, 1):
        ensure_safe_parents(dst, False)
        if os.path.lexists(dst):
            if dst.is_symlink() or not dst.is_file():
                raise RuntimeError(f"Ziel existiert, ist aber keine reguläre Datei: {dst}")
            if digest(dst) != sha:
                raise RuntimeError(f"Ziel existiert mit abweichender Prüfsumme: {dst}")
            skipped += 1
            continue
        if not src.is_file():
            raise RuntimeError(f"Quelle fehlt: {src}")
        if not write:
            continue
        # Verify source fully before writing a destination.
        if digest(src) != sha:
            raise RuntimeError(f"Quell-Prüfsumme stimmt nicht: {src}")
        ensure_safe_parents(dst, True)
        temp = dst.with_name(dst.name + ".partial-" + uuid.uuid4().hex)
        try:
            with src.open("rb") as inp, temp.open("xb") as out:
                for block in iter(lambda: inp.read(CHUNK), b""):
                    out.write(block)
                out.flush()
                os.fsync(out.fileno())
            if digest(temp) != sha:
                raise RuntimeError(f"Zielkopie hat abweichende Prüfsumme: {dst}")
            # Hard link is atomic and refuses to replace an existing destination.
            os.link(temp, dst, follow_symlinks=False)
            copied += 1
        finally:
            temp.unlink(missing_ok=True)
        if index % 100 == 0:
            print(f"Fortschritt: {index}/{len(rows)}; neu {copied}; bereits geprüft {skipped}", flush=True)
    print(f"Fertig: neu kopiert {copied}; bereits vorhanden und geprüft {skipped}; Plan {len(rows)}", flush=True)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--plan", type=Path, default=Path.home() / "Musiksammlung_work/musik-kopierplan.csv")
    p.add_argument("--write", action="store_true", help="Kopieren ausdrücklich aktivieren")
    p.add_argument("--limit", type=int, help="Nur die ersten N Plan-Einträge bearbeiten (für kontrollierte Tests)")
    args = p.parse_args()
    try:
        rows = validate_plan(args.plan)
        if args.limit is not None:
            if args.limit < 1:
                raise ValueError("--limit muss mindestens 1 sein")
            rows = rows[:args.limit]
        run(rows, args.write)
    except (OSError, ValueError, RuntimeError) as exc:
        print(f"ABBRUCH: {exc}", file=sys.stderr, flush=True)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
