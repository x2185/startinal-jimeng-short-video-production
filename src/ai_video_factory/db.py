from __future__ import annotations

import sqlite3
from pathlib import Path


SCHEMA = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS products (
    product_id TEXT PRIMARY KEY,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS assets (
    asset_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id TEXT NOT NULL REFERENCES products(product_id),
    source_path TEXT NOT NULL,
    sha256 TEXT NOT NULL,
    media_type TEXT NOT NULL,
    category TEXT NOT NULL,
    bytes INTEGER NOT NULL,
    status TEXT NOT NULL DEFAULT 'indexed',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(product_id, sha256)
);

CREATE TABLE IF NOT EXISTS creative_memory (
    memory_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id TEXT REFERENCES products(product_id),
    kind TEXT NOT NULL,
    content TEXT NOT NULL,
    evidence TEXT NOT NULL,
    status TEXT NOT NULL CHECK(status IN ('candidate', 'approved', 'retired')),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE VIRTUAL TABLE IF NOT EXISTS memory_search USING fts5(
    content,
    evidence,
    content='creative_memory',
    content_rowid='memory_id'
);

CREATE TRIGGER IF NOT EXISTS creative_memory_ai AFTER INSERT ON creative_memory BEGIN
    INSERT INTO memory_search(rowid, content, evidence)
    VALUES (new.memory_id, new.content, new.evidence);
END;
CREATE TRIGGER IF NOT EXISTS creative_memory_ad AFTER DELETE ON creative_memory BEGIN
    INSERT INTO memory_search(memory_search, rowid, content, evidence)
    VALUES ('delete', old.memory_id, old.content, old.evidence);
END;
CREATE TRIGGER IF NOT EXISTS creative_memory_au AFTER UPDATE ON creative_memory BEGIN
    INSERT INTO memory_search(memory_search, rowid, content, evidence)
    VALUES ('delete', old.memory_id, old.content, old.evidence);
    INSERT INTO memory_search(rowid, content, evidence)
    VALUES (new.memory_id, new.content, new.evidence);
END;

CREATE TABLE IF NOT EXISTS video_runs (
    run_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id TEXT NOT NULL REFERENCES products(product_id),
    creative_id TEXT NOT NULL,
    output_uri TEXT,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(product_id, creative_id)
);
"""


def connect(db_path: Path) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    connection.executescript(SCHEMA)
    return connection


def ensure_product(connection: sqlite3.Connection, product_id: str) -> None:
    connection.execute(
        "INSERT OR IGNORE INTO products(product_id) VALUES (?)", (product_id,)
    )
    connection.commit()
