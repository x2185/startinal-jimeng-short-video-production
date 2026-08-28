#!/usr/bin/env python3
"""Create a non-destructive catalog of generated-video assets and run records."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


MEDIA_EXTENSIONS = {".mp4", ".mov", ".m4v", ".webm", ".avi", ".jpg", ".jpeg", ".png", ".webp"}
VIDEO_EXTENSIONS = {".mp4", ".mov", ".m4v", ".webm", ".avi"}
METADATA_EXTENSIONS = {".json", ".md"}


def classify(relative: Path) -> tuple[str, str, str]:
    """Return category, origin, and safe reuse recommendation."""
    parts = [part.lower() for part in relative.parts]
    name = relative.name.lower()
    stem = relative.stem.lower()
    suffix = relative.suffix.lower()
    location = "/".join(parts)

    if suffix in METADATA_EXTENSIONS:
        return "job_record", "derived_metadata", "not_media"
    if suffix not in MEDIA_EXTENSIONS:
        return "other", "unknown", "not_media"
    if "handoff" in parts:
        return "continuity_reference", "generated_derivative", "use_only_after_continuity_review"
    if "review" in parts or "contact-sheet" in name or "sheet" in stem:
        return "review_asset", "derived_review", "not_reusable_output"
    if "frames" in parts or "/input/" in f"/{location}/" or "reference" in stem:
        return "source_product_reference", "source_material", "evidence_only_not_generated_fact"
    if suffix in VIDEO_EXTENSIONS:
        if "finals" in parts or "final" in stem:
            return "assembled_final", "generated_or_assembled", "reusable_after_human_acceptance"
        if "clips" in parts or "clip-" in stem:
            return "generated_clip", "generated", "reusable_after_human_acceptance"
        return "video_candidate", "unknown_video_origin", "review_before_reuse"
    return "image_candidate", "unknown_image_origin", "review_before_reuse"


def job_key(relative: Path) -> str:
    parts = list(relative.parts)
    for index, part in enumerate(parts):
        lower = part.lower()
        if lower == "run" or lower.startswith("run-") or lower.endswith("-run"):
            return "/".join(parts[: index + 1])
    return parts[0] if parts else "root"


def build_catalog(root: Path, excluded: set[Path]) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.resolve() in excluded:
            continue
        relative = path.relative_to(root)
        category, origin, reuse = classify(relative)
        stat = path.stat()
        records.append(
            {
                "path": relative.as_posix(),
                "job_key": job_key(relative),
                "category": category,
                "origin": origin,
                "review_status": "unreviewed",
                "reuse_recommendation": reuse,
                "bytes": stat.st_size,
                "modified_utc": datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat(),
                "classification_note": "Classification is path-based and does not establish product facts or human acceptance.",
            }
        )
    return records


def write_report(records: list[dict[str, object]], target: Path) -> None:
    counts = Counter(str(record["category"]) for record in records)
    reusable = [record for record in records if str(record["reuse_recommendation"]).startswith("reusable")]
    lines = [
        "# Generated asset catalog",
        "",
        "**Status:** path-based classification only. Every generated item is `unreviewed`; this catalog does not certify product identity, mechanics, or quality.",
        "",
        "## Counts",
        "",
        "| Category | Files |",
        "| --- | ---: |",
    ]
    lines.extend(f"| {category} | {counts[category]} |" for category in sorted(counts))
    lines.extend(["", "## Reuse review queue", ""])
    if reusable:
        lines.append("Review these before marking them reusable in their job manifest:")
        lines.append("")
        lines.extend(f"- `{record['path']}` — {record['category']}" for record in reusable)
    else:
        lines.append("No generated final/clip candidates were found.")
    lines.extend(
        [
            "",
            "## Safety note",
            "",
            "Original product references remain the evidence authority. A generated clip can become a continuity or B-roll reference only after human acceptance; it never proves a product feature or physical mechanism.",
        ]
    )
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Classify generated-video outputs without moving source files.")
    parser.add_argument("--root", required=True, type=Path, help="Output folder to scan.")
    parser.add_argument("--catalog", required=True, type=Path, help="JSON catalog to create or replace.")
    parser.add_argument("--report", required=True, type=Path, help="Markdown review report to create or replace.")
    args = parser.parse_args()
    root = args.root.resolve()
    if not root.is_dir():
        parser.error(f"Scan root does not exist: {root}")
    catalog = args.catalog.resolve()
    report = args.report.resolve()
    records = build_catalog(root, {catalog, report})
    payload = {
        "schema_version": 1,
        "root": str(root),
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "review_status_default": "unreviewed",
        "records": records,
    }
    catalog.parent.mkdir(parents=True, exist_ok=True)
    catalog.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    write_report(records, report)
    counts = Counter(str(record["category"]) for record in records)
    print(f"Cataloged {len(records)} file(s): " + ", ".join(f"{name}={counts[name]}" for name in sorted(counts)))
    print(f"JSON: {catalog}")
    print(f"Report: {report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
