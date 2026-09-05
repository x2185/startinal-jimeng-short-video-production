#!/usr/bin/env python3
"""Copy reviewed generated assets into a stable, renamed material library."""

from __future__ import annotations

import argparse
import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path


VALID_STATUSES = {"accepted", "candidate", "rejected", "needs_origin_review", "unreviewed"}


def clean(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-") or "asset"


def destination_status(status: str) -> str:
    return {
        "accepted": "approved-reuse",
        "candidate": "reuse-candidates",
        "rejected": "rejected-do-not-reuse",
        "needs_origin_review": "needs-origin-review",
        "unreviewed": "needs-review",
    }[status]


def bucket(category: str) -> str:
    return {
        "source_product_reference": "source-evidence",
        "continuity_reference": "continuity-refs",
        "review_asset": "review-assets",
        "assembled_final": "final-videos",
        "generated_clip": "clips",
        "job_record": "job-records",
        "video_candidate": "video-candidates",
        "image_candidate": "image-candidates",
    }.get(category, "other")


def read_decisions(path: Path) -> dict[str, dict[str, str]]:
    if not path.is_file():
        return {}
    payload = json.loads(path.read_text(encoding="utf-8"))
    decisions = payload.get("job_decisions", {})
    if not isinstance(decisions, dict):
        raise ValueError("job_decisions must be an object keyed by catalog job_key")
    for key, decision in decisions.items():
        status = str(decision.get("review_status", "unreviewed"))
        if status not in VALID_STATUSES:
            raise ValueError(f"Unsupported review_status for {key}: {status}")
    return decisions


def main() -> int:
    parser = argparse.ArgumentParser(description="Copy and rename cataloged output media without touching originals.")
    parser.add_argument("--catalog", required=True, type=Path, help="JSON created by catalog_generated_assets.py")
    parser.add_argument("--decisions", type=Path, help="Optional visual-review decisions JSON")
    parser.add_argument("--library-root", required=True, type=Path, help="Destination generated-material library")
    args = parser.parse_args()
    catalog_path = args.catalog.resolve()
    payload = json.loads(catalog_path.read_text(encoding="utf-8"))
    source_root = Path(payload["root"])
    if not source_root.is_dir():
        raise FileNotFoundError(f"Catalog source root no longer exists: {source_root}")
    decisions = read_decisions(args.decisions.resolve()) if args.decisions else {}
    library_root = args.library_root.resolve()
    manifest_path = library_root / "library-manifest.json"
    copied: list[dict[str, str]] = []
    skipped = 0
    for sequence, record in enumerate(payload.get("records", []), start=1):
        relative = Path(str(record["path"]))
        source = source_root / relative
        if not source.is_file():
            continue
        job = str(record.get("job_key", "unassigned"))
        decision = decisions.get(job, {})
        status = str(decision.get("review_status", "unreviewed"))
        reason = str(decision.get("reason", "No visual decision recorded."))
        if status not in VALID_STATUSES:
            raise ValueError(f"Unsupported review_status for {job}: {status}")
        category = str(record.get("category", "other"))
        role = bucket(category)
        status_folder = "source-evidence" if category == "source_product_reference" else destination_status(status)
        target_dir = library_root / clean(job) / status_folder / role
        renamed = f"{sequence:03d}__{clean(job)}__{clean(relative.stem)}__{clean(str(record.get('category', 'other')))}{source.suffix.lower()}"
        target = target_dir / renamed
        target_dir.mkdir(parents=True, exist_ok=True)
        if target.exists() and target.stat().st_size == source.stat().st_size:
            skipped += 1
        else:
            shutil.copy2(source, target)
        copied.append(
            {
                "source": relative.as_posix(),
                "library_path": target.relative_to(library_root).as_posix(),
                "job_key": job,
                "category": category,
                "review_status": status,
                "review_reason": reason,
            }
        )
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "created_utc": datetime.now(timezone.utc).isoformat(),
                "mode": "copy-only; original output files remain unchanged",
                "source_catalog": str(catalog_path),
                "assets": copied,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"Catalog records copied: {len(copied)}; existing copies skipped: {skipped}")
    print(f"Library: {library_root}")
    print(f"Manifest: {manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
