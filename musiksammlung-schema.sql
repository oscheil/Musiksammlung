-- Musiksammlung: SQLite schema, version 1
-- Run against a NEW SQLite database only. No audio files are changed.
PRAGMA foreign_keys = ON;
BEGIN TRANSACTION;

CREATE TABLE schema_version (
  version INTEGER PRIMARY KEY,
  applied_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
INSERT INTO schema_version(version) VALUES (1);

-- A source collection is a logical import root on a particular host/volume.
CREATE TABLE collections (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL UNIQUE,
  host TEXT NOT NULL,
  root_path TEXT NOT NULL,
  volume_label TEXT,
  notes TEXT,
  active INTEGER NOT NULL DEFAULT 1 CHECK (active IN (0,1)),
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(host, root_path)
);

-- One row per distinct byte sequence, irrespective of filename/location.
CREATE TABLE audio_files (
  id INTEGER PRIMARY KEY,
  sha256 TEXT NOT NULL UNIQUE CHECK (length(sha256) = 64 AND sha256 NOT GLOB '*[^0-9a-f]*'),
  file_size_bytes INTEGER CHECK (file_size_bytes >= 0),
  format TEXT,
  duration_seconds REAL CHECK (duration_seconds IS NULL OR duration_seconds >= 0),
  codec TEXT,
  bitrate_kbps INTEGER,
  sample_rate_hz INTEGER,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- A stable catalog entry, independent of file hash or path.
-- A title can be unknown; radio extracts are ordinary tracks.
CREATE TABLE tracks (
  id INTEGER PRIMARY KEY,
  entry_type TEXT NOT NULL DEFAULT 'track' CHECK (entry_type IN ('track','radio_program','unknown')),
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

-- A track may have several encodings; a file is not automatically a track.
CREATE TABLE track_files (
  track_id INTEGER NOT NULL REFERENCES tracks(id) ON DELETE CASCADE,
  audio_file_id INTEGER NOT NULL REFERENCES audio_files(id) ON DELETE CASCADE,
  preferred INTEGER NOT NULL DEFAULT 0 CHECK (preferred IN (0,1)),
  link_reason TEXT,
  PRIMARY KEY(track_id, audio_file_id)
);

-- Path is a mutable observation, not a stable identity.
-- Retain missing/old paths for audit and move reconciliation.
CREATE TABLE file_locations (
  id INTEGER PRIMARY KEY,
  audio_file_id INTEGER NOT NULL REFERENCES audio_files(id),
  collection_id INTEGER NOT NULL REFERENCES collections(id),
  relative_path TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'present' CHECK (status IN ('present','missing','moved','unverified')),
  first_seen_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  last_seen_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  last_verified_at TEXT,
  UNIQUE(collection_id, relative_path)
);

-- Track-level labels are not dependent on embedded tags.
CREATE TABLE tags (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL UNIQUE
);
CREATE TABLE track_tags (
  track_id INTEGER NOT NULL REFERENCES tracks(id) ON DELETE CASCADE,
  tag_id INTEGER NOT NULL REFERENCES tags(id) ON DELETE CASCADE,
  PRIMARY KEY(track_id, tag_id)
);

-- Log future read-only inventories and controlled imports.
CREATE TABLE scan_runs (
  id INTEGER PRIMARY KEY,
  collection_id INTEGER NOT NULL REFERENCES collections(id),
  started_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  finished_at TEXT,
  status TEXT NOT NULL DEFAULT 'running' CHECK (status IN ('running','completed','failed')),
  scanned_files INTEGER NOT NULL DEFAULT 0,
  notes TEXT
);

-- Records candidate duplicates without automatically merging tracks.
CREATE TABLE duplicate_candidates (
  id INTEGER PRIMARY KEY,
  track_id_a INTEGER NOT NULL REFERENCES tracks(id),
  track_id_b INTEGER NOT NULL REFERENCES tracks(id),
  detection_method TEXT NOT NULL,
  confidence REAL CHECK (confidence IS NULL OR confidence BETWEEN 0 AND 1),
  review_status TEXT NOT NULL DEFAULT 'pending' CHECK (review_status IN ('pending','same_recording','different_recording','ignored')),
  notes TEXT,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CHECK (track_id_a < track_id_b),
  UNIQUE(track_id_a, track_id_b, detection_method)
);

CREATE INDEX idx_file_locations_hash_ref ON file_locations(audio_file_id);
CREATE INDEX idx_file_locations_collection_status ON file_locations(collection_id, status);
CREATE INDEX idx_track_files_audio ON track_files(audio_file_id);
CREATE INDEX idx_tracks_title_artist ON tracks(title, artist);
CREATE INDEX idx_scan_runs_collection ON scan_runs(collection_id, started_at);

-- Known roots only; no filesystem access or file imports happen here.
INSERT INTO collections(name, host, root_path, volume_label, notes) VALUES
 ('miniitx', 'terra-1240', '/mnt/datensichv/miniitx/Musik', NULL, 'Initial inventory'),
 ('von_media', 'terra-1240', '/mnt/datensichv/von_media/Musik', NULL, 'Initial inventory'),
 ('vonaspirev5', 'terra-1240', '/mnt/datensichv/vonaspirev5/Musik', NULL, 'Initial inventory'),
 ('ds_musik', 'terra11', '/media/oscheil/TV/ds_musik', 'TV', 'Initial inventory');

COMMIT;
