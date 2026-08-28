#!/usr/bin/env python3
"""Create an auditable real-product reference pack from verified source images.

The optional rembg dependency is deliberately not installed by this script.  A
missing dependency leaves source assets intact and records that cutouts are
pending review, instead of silently producing a misleading substitute.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path


SUPPORTED = {".jpg", ".jpeg", ".png"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a reviewable real-product source and optional-cutout pack.")
    parser.add_argument("--input", type=Path, action="append", required=True, help="Verified finished-product image; repeat for multiple views.")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--label", default="product")
    parser.add_argument("--remove-background", choices=("auto", "required", "off"), default="auto")
    args = parser.parse_args()

    inputs = [path.expanduser().resolve() for path in args.input]
    for path in inputs:
        if not path.is_file():
            parser.error(f"Input image does not exist: {path}")
        if path.suffix.lower() not in SUPPORTED:
            parser.error(f"Unsupported image type: {path.name}")

    remover = None
    if args.remove_background != "off":
        try:
            from rembg import remove  # type: ignore[import-not-found]
            remover = remove
        except ImportError:
            if args.remove_background == "required":
                parser.error("Background removal requires optional dependency rembg. Install it explicitly, then retry.")

    source_dir = args.output_dir / "source"
    cutout_dir = args.output_dir / "cutouts"
    source_dir.mkdir(parents=True, exist_ok=True)
    if remover:
        cutout_dir.mkdir(parents=True, exist_ok=True)

    assets: list[dict[str, str | int]] = []
    for index, source in enumerate(inputs, start=1):
        suffix = source.suffix.lower()
        copied = source_dir / f"identity-{index:02d}{suffix}"
        shutil.copy2(source, copied)
        entry: dict[str, str | int] = {
            "source": str(source),
            "copied_source": str(copied.resolve()),
            "sha256": sha256(source),
            "bytes": source.stat().st_size,
            "role": "verified_finished_product_identity",
        }
        if remover:
            target = cutout_dir / f"identity-{index:02d}.png"
            try:
                target.write_bytes(remover(source.read_bytes()))
            except Exception as exc:  # rembg providers can fail independently per image.
                entry["cutout_status"] = f"failed: {exc}"
            else:
                entry["cutout_candidate"] = str(target.resolve())
                entry["cutout_status"] = "pending_edge_review"
        else:
            entry["cutout_status"] = "pending_optional_rembg_install"
        assets.append(entry)

    manifest = {
        "schema_version": 1,
        "label": args.label,
        "background_removal": "available" if remover else "not_installed_or_disabled",
        "review_required": True,
        "review_note": "Confirm silhouette, translucent edges, tips, logos and included parts before compositing or prompting.",
        "assets": assets,
    }
    manifest_path = args.output_dir / "reference-pack.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Created reference pack: {manifest_path}")
    if remover:
        print("Cutout candidates created; complete edge review before use.")
    else:
        print("Source assets preserved. Optional rembg is unavailable, so no cutout is claimed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
