#!/usr/bin/env python3
"""Read-only copy plan with detailed name conflicts and destination checks."""
import argparse
import csv
from collections import Counter, defaultdict
import os
from pathlib import Path, PurePosixPath
import sqlite3

TV_OLD = "/media/oscheil/TV/ds_musik/"
TV_NOW = "/mnt/tv-musik/ds_musik/"

def current_path(path):
    return TV_NOW + path[len(TV_OLD):] if path.startswith(TV_OLD) else path

def safe_relative(original, root):
    prefix = root.rstrip("/") + "/"
    if not original.startswith(prefix):
        return None
    rel = original[len(prefix):]
    if not rel or rel.startswith("/") or any(p in ("", ".", "..") for p in rel.split("/")):
        return None
    return PurePosixPath(rel)

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--database", type=Path, default=Path.home() / "Musiksammlung_work/musiksammlung.sqlite")
    ap.add_argument("--examples", type=int, default=5)
    ap.add_argument("--export", type=Path, help="CSV-Kopierplan schreiben (nur wenn konfliktfrei planbar; bestehende Datei wird nicht überschrieben)")
    args = ap.parse_args()
    con = sqlite3.connect("file:" + str(args.database.resolve()) + "?mode=ro", uri=True)
    try:
        sources = con.execute("SELECT id,name,root_path FROM collections WHERE role='source'").fetchall()
        roots = {i: root for i, name, root in sources}
        names = {i: name for i, name, root in sources}
        target = con.execute("SELECT root_path FROM collections WHERE role='production'").fetchone()
        if target is None:
            raise SystemExit("Keine Produktions-Collection in der Datenbank")
        target_root = Path(target[0])
        grouped = defaultdict(list)
        hashes = {}
        invalid = []
        for file_id, sha, cid, path in con.execute("""SELECT a.id,a.sha256,o.collection_id,o.original_path
                FROM audio_files a JOIN file_origins o ON o.audio_file_id=a.id ORDER BY a.id,o.id"""):
            hashes[file_id] = sha
            rel = safe_relative(path, roots[cid])
            if rel is None:
                invalid.append((sha, path))
            else:
                grouped[file_id].append((cid, path, rel))
        selected = []
        problems = []
        for file_id, origins in sorted(grouped.items()):
            origins.sort(key=lambda x: (names[x[0]] == "ds_musik", names[x[0]], str(x[2])))
            source = next(((cid, path, rel) for cid, path, rel in origins if Path(current_path(path)).is_file()), None)
            if source is None:
                problems.append((hashes[file_id], "Keine erreichbare Quelle"))
            else:
                selected.append((hashes[file_id], *source))
        reserved = {str(rel).casefold() for sha, cid, path, rel in selected}
        used = {}
        planned = []
        conflicts = []
        existing = []
        for sha, cid, source, rel in selected:
            key = str(rel).casefold()
            candidate = rel
            if key in used:
                first = used[key]
                for suffix in (sha[:12], sha):
                    alt = rel.with_name(f"{rel.stem}--{suffix}{rel.suffix}")
                    alt_key = str(alt).casefold()
                    if alt_key not in used and alt_key not in reserved:
                        candidate = alt
                        key = alt_key
                        break
                else:
                    problems.append((sha, "Kein freier eindeutiger Zielname"))
                    continue
                conflicts.append((str(rel), first, source, str(candidate)))
            used[key] = source
            destination = target_root / str(candidate)
            if os.path.lexists(destination):
                existing.append(str(destination))
            planned.append((sha, cid, current_path(source), destination))
        # Check planned file-vs-directory collisions, including case-folded names.
        file_keys = {str(dest.relative_to(target_root)).casefold() for _, _, _, dest in planned}
        hierarchy = []
        for _, _, _, dest in planned:
            rel = dest.relative_to(target_root)
            for parent in list(rel.parents)[:-1]:
                if str(parent).casefold() in file_keys:
                    hierarchy.append(str(rel))
                    break
            # Existing path components must be directories, never files or symlinks.
            for parent in [target_root, *reversed(list(dest.parents)[:-1])]:
                if parent == Path("/"):
                    continue
                if os.path.lexists(parent) and (parent.is_symlink() or not parent.is_dir()):
                    hierarchy.append(f"{dest} (vorhandene Pfadkomponente: {parent})")
                    break
        counts = Counter("TV" if names[cid] == "ds_musik" else "DATENSICHV" for _, cid, _, _ in planned)
        total = con.execute("SELECT COUNT(*) FROM audio_files").fetchone()[0]
        print("NUR DRY-RUN: keine Dateien, Verzeichnisse oder Datenbankeinträge verändert")
        print(f"Eindeutige Inhalte: {total}; geplante Kopien: {len(planned)}")
        print(f"Quellen DATENSICHV: {counts['DATENSICHV']}; TV: {counts['TV']}")
        print(f"Namenskonflikte: {len(conflicts)}; bestehende Zielpfade: {len(existing)}")
        print(f"Datei/Verzeichnis-Konflikte: {len(hierarchy)}; Planungsfehler: {len(problems)}")
        print(f"Ungültige Herkunftspfade: {len(invalid)}; Zielwurzel: {target_root}")
        print("\nNAMENSKONFLIKTE:")
        for original, first, second, resolved in conflicts:
            print(f"  Gewünschter relativer Pfad: {original}")
            print(f"    Erste Quelle: {first}")
            print(f"    Weitere Quelle: {second}")
            print(f"    Alternativer Zielpfad: {resolved}")
        print("\nBEREITS VORHANDENE ZIELPFADE:")
        for path in existing[:30]:
            print(f"  {path}")
        if len(existing) > 30:
            print(f"  ... weitere {len(existing)-30}")
        print("\nDATEI/VERZEICHNIS-KONFLIKTE:")
        for path in hierarchy[:30]:
            print(f"  {path}")
        if len(hierarchy) > 30:
            print(f"  ... weitere {len(hierarchy)-30}")
        print("\nPLANUNGSFEHLER:")
        for item in problems[:30]:
            print(f"  {item}")
        print("\nBEISPIELE:")
        for sha, cid, src, dst in planned[:max(args.examples, 0)]:
            print(f"  {src}\n    -> {dst}")
        if args.export:
            if problems or invalid or existing or hierarchy or len(planned) != total:
                print("EXPORT ABGEBROCHEN: Planungsfehler oder vorhandene Zielkonflikte.")
                raise SystemExit(2)
            # Exclusive creation: never overwrite an existing plan.
            try:
                with args.export.open("x", encoding="utf-8", newline="") as output:
                    writer = csv.writer(output)
                    writer.writerow(["sha256", "quelle_aktuell", "ziel", "quellsammlung"])
                    for sha, cid, src, dst in planned:
                        writer.writerow([sha, str(src), str(dst), names[cid]])
            except FileExistsError:
                print(f"EXPORT ABGEBROCHEN: Datei existiert bereits: {args.export}")
                raise SystemExit(2)
            print(f"CSV-Kopierplan exportiert: {args.export} ({len(planned)} Einträge)")
        print("HINWEIS: Keine erneute SHA-256-Prüfung; keine Kopieraktion.")
    finally:
        con.close()

if __name__ == "__main__":
    main()
