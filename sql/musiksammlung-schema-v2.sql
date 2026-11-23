-- Musiksammlung / SQLite / schema version 2
-- Only for a NEW database. Does not read, copy, modify or delete music files.
PRAGMA foreign_keys = ON;
BEGIN TRANSACTION;

CREATE TABLE schema_version (
  version INTEGER PRIMARY KEY,
  applied_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
INSERT INTO schema_version(version) VALUES (2);

-- Logical collections: historical source roots, productive collection and backup.
CREATE TABLE collections (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL UNIQUE,
  host TEXT NOT NULL,
  root_path TEXT NOT NULL,
  volume_label TEXT,
  role TEXT NOT NULL CHECK(role IN ('source','production','backup')),
  notes TEXT,
  active INTEGER NOT NULL DEFAULT 1 CHECK(active IN (0,1)),
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(host, root_path)
);

-- Identity of byte-identical audio content, not necessarily of a musical work.
CREATE TABLE audio_files (
  id INTEGER PRIMARY KEY,
  sha256 TEXT NOT NULL UNIQUE
    CHECK(length(sha256)=64 AND sha256 NOT GLOB '*[^0-9a-f]*'),
  file_size_bytes INTEGER CHECK(file_size_bytes IS NULL OR file_size_bytes >= 0),
  format TEXT,
  duration_seconds REAL CHECK(duration_seconds IS NULL OR duration_seconds >= 0),
  codec TEXT,
  bitrate_kbps INTEGER,
  sample_rate_hz INTEGER,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Historical provenance. Keep records even after original files are removed.
-- original_path is preserved exactly as supplied by the original inventory.
CREATE TABLE file_origins (
  id INTEGER PRIMARY KEY,
  audio_file_id INTEGER NOT NULL REFERENCES audio_files(id),
  collection_id INTEGER NOT NULL REFERENCES collections(id),
  original_path TEXT NOT NULL,
  source_status TEXT NOT NULL DEFAULT 'unverified'
    CHECK(source_status IN ('unverified','present','removed','missing')),
  imported_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  removed_at TEXT,
  notes TEXT,
  UNIQUE(collection_id, original_path)
);

-- Current or last observed location of productive and backup copies.
-- Paths may change without changing audio_files or tracks identities.
CREATE TABLE file_locations (
  id INTEGER PRIMARY KEY,
  audio_file_id INTEGER NOT NULL REFERENCES audio_files(id),
  collection_id INTEGER NOT NULL REFERENCES collections(id),
  relative_path TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'unverified'
    CHECK(status IN ('present','missing','moved','unverified')),
  first_seen_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  last_seen_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  last_verified_at TEXT,
  UNIQUE(collection_id, relative_path)
);

CREATE TABLE tracks (
  id INTEGER PRIMARY KEY,
  entry_type TEXT NOT NULL DEFAULT 'track'
    CHECK(entry_type IN ('track','radio_program','unknown')),
  title TEXT,
  artist TEXT,
  album TEXT,
  genre TEXT,
  release_year INTEGER,
  composer TEXT,
  radio_station TEXT,
  broadcast_date TEXT,
  description TEXT,
  notes TEXT,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE track_files (
  track_id INTEGER NOT NULL REFERENCES tracks(id) ON DELETE CASCADE,
  audio_file_id INTEGER NOT NULL REFERENCES audio_files(id) ON DELETE CASCADE,
  preferred INTEGER NOT NULL DEFAULT 0 CHECK(preferred IN (0,1)),
  link_reason TEXT,
  PRIMARY KEY(track_id, audio_file_id)
);

CREATE TABLE tags (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL UNIQUE
);
CREATE TABLE track_tags (
  track_id INTEGER NOT NULL REFERENCES tracks(id) ON DELETE CASCADE,
  tag_id INTEGER NOT NULL REFERENCES tags(id) ON DELETE CASCADE,
  PRIMARY KEY(track_id, tag_id)
);

CREATE TABLE scan_runs (
  id INTEGER PRIMARY KEY,
  collection_id INTEGER NOT NULL REFERENCES collections(id),
  started_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  finished_at TEXT,
  status TEXT NOT NULL DEFAULT 'running'
    CHECK(status IN ('running','completed','failed')),
  scanned_files INTEGER NOT NULL DEFAULT 0,
  notes TEXT
);

CREATE TABLE duplicate_candidates (
  id INTEGER PRIMARY KEY,
  track_id_a INTEGER NOT NULL REFERENCES tracks(id),
  track_id_b INTEGER NOT NULL REFERENCES tracks(id),
  detection_method TEXT NOT NULL,
  confidence REAL CHECK(confidence IS NULL OR confidence BETWEEN 0 AND 1),
  review_status TEXT NOT NULL DEFAULT 'pending'
    CHECK(review_status IN ('pending','same_recording','different_recording','ignored')),
  notes TEXT,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CHECK(track_id_a < track_id_b),
  UNIQUE(track_id_a, track_id_b, detection_method)
);

CREATE INDEX idx_origins_audio ON file_origins(audio_file_id);
CREATE INDEX idx_origins_collection_status ON file_origins(collection_id, source_status);
CREATE INDEX idx_locations_audio ON file_locations(audio_file_id);
CREATE INDEX idx_locations_collection_status ON file_locations(collection_id, status);
CREATE INDEX idx_track_files_audio ON track_files(audio_file_id);
CREATE INDEX idx_tracks_title_artist ON tracks(title, artist);
CREATE INDEX idx_scan_runs_collection ON scan_runs(collection_id, started_at);

-- Historical paths reflect the original machines, not today's temporary mounts.
-- The TV backup root is a PLANNED destination, not a mounted/created directory.
INSERT INTO collections(name,host,root_path,volume_label,role,notes) VALUES
 ('miniitx','terra-1240','/mnt/datensichv/miniitx/Musik','DATENSICHV','source','Historical source'),
 ('von_media','terra-1240','/mnt/datensichv/von_media/Musik','DATENSICHV','source','Historical source'),
 ('vonaspirev5','terra-1240','/mnt/datensichv/vonaspirev5/Musik','DATENSICHV','source','Historical source'),
 ('ds_musik','terra11','/media/oscheil/TV/ds_musik','TV','source','Historical source path on terra11'),
 ('production','terra-1240','/mnt/datensichv/Musiksammlung','DATENSICHV','production','Planned productive collection'),
 ('backup_tv','terra-1240','/mnt/tv-musik/Musiksammlung-Backup','TV','backup','Provisional backup path; confirm before backup');

COMMIT;
