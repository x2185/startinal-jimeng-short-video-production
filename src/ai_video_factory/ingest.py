from __future__ import annotations

import hashlib
import sqlite3
from pathlib import Path

from .db import ensure_product


IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
VIDEO_EXTENSIONS = {".mp4", ".mov", ".m4v", ".webm"}
AUDIO_EXTENSIONS = {".mp3", ".wav", ".m4a"}
DOCUMENT_EXTENSIONS = {".txt", ".md", ".pdf", ".docx", ".xlsx", ".csv"}


def media_type(path: Path) -> str | None:
    suffix = path.suffix.lower()
    if suffix in IMAGE_EXTENSIONS:
        return "image"
    if suffix in VIDEO_EXTENSIONS:
        return "video"
    if suffix in AUDIO_EXTENSIONS:
        return "audio"
    if suffix in DOCUMENT_EXTENSIONS:
        return "document"
    return None


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        while chunk := file.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def category(source_root: Path, path: Path) -> str:
    relative_parts = path.relative_to(source_root).parts
    return relative_parts[0] if len(relative_parts) > 1 else "uncategorized"


def ingest_folder(
    connection: sqlite3.Connection, product_id: str, source_root: Path
) -> dict[str, int]:
    source_root = source_root.resolve()
    if not source_root.is_dir():
        raise ValueError(f"素材目录不存在: {source_root}")
    ensure_product(connection, product_id)
    result = {"indexed": 0, "duplicates": 0, "ignored": 0}
    for path in source_root.rglob("*"):
        if not path.is_file():
            continue
        kind = media_type(path)
        if kind is None:
            result["ignored"] += 1
            continue
        fingerprint = sha256(path)
        cursor = connection.execute(
            """
            INSERT OR IGNORE INTO assets
                (product_id, source_path, sha256, media_type, category, bytes)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                product_id,
                str(path),
                fingerprint,
                kind,
                category(source_root, path),
                path.stat().st_size,
            ),
        )
        result["indexed" if cursor.rowcount else "duplicates"] += 1
    connection.commit()
    return result
