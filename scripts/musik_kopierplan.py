#!/usr/bin/env python3
"""Read-only proposed copy plan; never creates directories, copies files or writes SQLite."""
import argparse
from collections import Counter
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
    parts = PurePosixPath(rel).parts
    if not parts or any(p in ("", ".", "..") for p in parts) or rel.startswith("/"):
        return None
    return PurePosixPath(*parts)

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--database", type=Path, default=Path.home() / "Musiksammlung_work/musiksammlung.sqlite")
    ap.add_argument("--examples", type=int, default=12)
    args = ap.parse_args()
    con = sqlite3.connect("file:" + str(args.database.resolve()) + "?mode=ro", uri=True)
    try:
        sources = con.execute("SELECT id,name,root_path FROM collections WHERE role='source'").fetchall()
        roots = {i: root for i, name, root in sources}
        names = {i: name for i, name, root in sources}
        target = con.execute("SELECT root_path FROM collections WHERE role='production'").fetchone()
        if target is None:
            raise SystemExit("Keine Produktions-Collection in der Datenbank")
        target_root = target[0]
        rows = con.execute("""SELECT a.id,a.sha256,o.collection_id,o.original_path
            FROM audio_files a JOIN file_origins o ON o.audio_file_id=a.id
            ORDER BY a.id,o.id""")
        grouped = {}
        for file_id, sha, cid, path in rows:
            rel = safe_relative(path, roots[cid])
            if rel is not None:
                grouped.setdefault(file_id, (sha, []))[1].append((cid, path, rel))
        used = {}
        counts = Counter()
        samples = []
        errors = []
        for file_id, (sha, origins) in sorted(grouped.items()):
            # Prefer DATENSICHV; preserve the source-relative original tree.
            origins.sort(key=lambda x: (names[x[0]] == "ds_musik", names[x[0]], str(x[2])))
            source = next(((cid, path, rel) for cid, path, rel in origins if Path(current_path(path)).is_file()), None)
            if source is None:
                errors.append((sha, "Keine erreichbare Quelldatei"))
                continue
            cid, path, rel = source
            candidate = rel
            key = str(candidate).casefold()
            if key in used and used[key] != sha:
                counts["name_conflicts"] += 1
                # Suffix before extension, deterministic and independent of traversal order.
                base = rel.stem
                ext = rel.suffix
                candidate = rel.with_name(f"{base}--{sha[:12]}{ext}")
                key = str(candidate).casefold()
                if key in used and used[key] != sha:
                    candidate = rel.with_name(f"{base}--{sha}{ext}")
                    key = str(candidate).casefold()
            if key in used and used[key] != sha:
                errors.append((sha, "Zielpfad weiterhin belegt"))
                continue
            used[key] = sha
            counts["planned"] += 1
            counts["tv_sources" if names[cid] == "ds_musik" else "datensichv_sources"] += 1
            if len(samples) < max(args.examples, 0):
                samples.append((current_path(path), target_root.rstrip("/") + "/" + str(candidate)))
        total = con.execute("SELECT COUNT(*) FROM audio_files").fetchone()[0]
        print("NUR DRY-RUN: keine Verzeichnisse, Dateien oder Datenbankeinträge verändert")
        print(f"Eindeutige Inhalte in SQLite: {total}")
        print(f"Geplante Kopien: {counts['planned']}")
        print(f"Quellen DATENSICHV: {counts['datensichv_sources']}")
        print(f"Quellen TV: {counts['tv_sources']}")
        print(f"Namenskonflikte mit SHA-Zusatz: {counts['name_conflicts']}")
        print(f"Nicht planbare Inhalte: {total-counts['planned']}")
        print(f"Zielwurzel: {target_root}")
        print("Beispiele (Quelle -> vorgeschlagenes Ziel):")
        for source, dest in samples:
            print(f"  {source}\n    -> {dest}")
        for sha, reason in errors[:10]:
            print(f"PROBLEM {sha}: {reason}")
        print("HINWEIS: Dies ist nur ein Plan, keine erneute SHA-256-Prüfung und kein Kopiervorgang.")
    finally:
        con.close()

if __name__ == "__main__":
    main()
