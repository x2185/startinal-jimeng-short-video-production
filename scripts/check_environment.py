#!/usr/bin/env python3
"""Check the local prerequisites for the JiMeng short-video production skill."""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Check local prerequisites for this skill.")
    parser.add_argument("--assembly", action="store_true", help="Fail if FFmpeg is unavailable.")
    parser.add_argument("--ffmpeg", type=Path, help="Explicit FFmpeg executable path.")
    args = parser.parse_args()

    failed = False
    if sys.version_info < (3, 9):
        print(f"FAIL Python {sys.version.split()[0]} found; Python 3.9 or newer is required.")
        failed = True
    else:
        print(f"OK   Python {sys.version.split()[0]}")

    if args.ffmpeg is not None:
        ffmpeg = str(args.ffmpeg) if args.ffmpeg.is_file() else None
    else:
        ffmpeg = shutil.which("ffmpeg")

    if ffmpeg:
        print(f"OK   FFmpeg: {ffmpeg}")
    elif args.assembly:
        print("FAIL FFmpeg not found. Install it, add it to PATH, or pass --ffmpeg C:\\path\\ffmpeg.exe.")
        failed = True
    else:
        print("WARN FFmpeg not found. It is needed only for local video assembly.")

    print("INFO This skill can plan, audit, and write prompts without an API key.")
    print("INFO JiMeng API automation needs a provider-specific integration and local credentials; never store keys in this skill.")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
