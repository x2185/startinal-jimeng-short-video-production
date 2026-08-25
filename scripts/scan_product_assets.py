#!/usr/bin/env python3
"""Fingerprint product assets and flag changes that require identity re-review."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SUPPORTED = {".mp4", ".mov", ".m4v", ".avi", ".webm", ".jpg", ".jpeg", ".png", ".webp"}
CHUNK_SIZE = 1024 * 1024


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(CHUNK_SIZE):
            hasher.update(chunk)
    return hasher.hexdigest()


def fingerprint(root: Path) -> dict[str, dict[str, Any]]:
    items: dict[str, dict[str, Any]] = {}
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in SUPPORTED:
            continue
        stat = path.stat()
        relative = path.relative_to(root).as_posix()
        items[relative] = {
            "path": relative,
            "kind": "video" if path.suffix.lower() in {".mp4", ".mov", ".m4v", ".avi", ".webm"} else "image",
            "bytes": stat.st_size,
            "modified_utc": datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat(),
            "sha256": digest(path),
        }
    return items


def compare(previous: dict[str, Any], current: dict[str, dict[str, Any]]) -> dict[str, list[str]]:
    before = previous.get("assets", {}) if previous else {}
    added = sorted(set(current) - set(before))
    deleted = sorted(set(before) - set(current))
    changed = sorted(key for key in set(current) & set(before) if current[key]["sha256"] != before[key].get("sha256"))
    unchanged = sorted(key for key in set(current) & set(before) if key not in changed)
    return {"added": added, "changed": changed, "deleted": deleted, "unchanged": unchanged}


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan product assets and compare them with an earlier manifest.")
    parser.add_argument("--root", required=True, type=Path, help="Product-specific asset folder.")
    parser.add_argument("--manifest", required=True, type=Path, help="Manifest JSON to create or update.")
    args = parser.parse_args()
    root = args.root.resolve()
    if not root.is_dir():
        parser.error(f"Asset folder does not exist: {root}")
    prior: dict[str, Any] = {}
    if args.manifest.is_file():
        prior = json.loads(args.manifest.read_text(encoding="utf-8"))
        if prior.get("root") and prior["root"] != str(root):
            parser.error("Manifest belongs to another asset folder; choose a different manifest path.")
    assets = fingerprint(root)
    changes = compare(prior, assets)
    requires_identity_review = bool(changes["added"] or changes["changed"] or changes["deleted"])
    manifest = {
        "schema_version": 1,
        "root": str(root),
        "scanned_utc": datetime.now(timezone.utc).isoformat(),
        "assets": assets,
        "changes": changes,
        "requires_identity_review": requires_identity_review,
        "identity_review_reason": (
            "First scan or asset changes detected. Rebuild/reconfirm the product identity passport before paid generation."
            if requires_identity_review
            else "No asset-content changes detected; reuse is allowed only after checking the existing identity passport."
        ),
    }
    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    args.manifest.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Scanned {len(assets)} supported asset(s).")
    print(f"Added: {len(changes['added'])}; changed: {len(changes['changed'])}; deleted: {len(changes['deleted'])}; unchanged: {len(changes['unchanged'])}.")
    print("IDENTITY_REVIEW_REQUIRED" if requires_identity_review else "NO_ASSET_CONTENT_CHANGE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
