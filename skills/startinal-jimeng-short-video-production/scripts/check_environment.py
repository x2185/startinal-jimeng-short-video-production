#!/usr/bin/env python3
"""Check the local prerequisites for the JiMeng short-video production skill."""

from __future__ import annotations

import argparse
import platform
import shutil
import subprocess
import sys
from pathlib import Path


def find_ffmpeg() -> str | None:
    """Find FFmpeg on PATH or in the current project's conventional tools folder."""
    on_path = shutil.which("ffmpeg")
    if on_path:
        return on_path
    tools_dir = Path.cwd() / "tools"
    if tools_dir.is_dir():
        candidates = sorted(tools_dir.glob("**/ffmpeg.exe"))
        if candidates:
            return str(candidates[0])
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description="Check local prerequisites for this skill.")
    parser.add_argument("--assembly", action="store_true", help="Fail if FFmpeg is unavailable.")
    parser.add_argument("--ffmpeg", type=Path, help="Explicit FFmpeg executable path.")
    parser.add_argument(
        "--install-missing",
        action="store_true",
        help="Install missing FFmpeg through Windows winget after explicit user approval.",
    )
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
        ffmpeg = find_ffmpeg()

    if ffmpeg:
        print(f"OK   FFmpeg: {ffmpeg}")
    elif args.install_missing:
        winget = shutil.which("winget")
        if platform.system() != "Windows":
            print("FAIL Automatic FFmpeg installation is currently supported only on Windows.")
            failed = True
        elif not winget:
            print("FAIL Windows winget was not found. Install FFmpeg manually, then rerun this check.")
            failed = True
        else:
            command = [
                winget,
                "install",
                "--id",
                "Gyan.FFmpeg.Shared",
                "--exact",
                "--accept-package-agreements",
                "--accept-source-agreements",
            ]
            print("INFO Installing missing FFmpeg with winget after user approval.")
            result = subprocess.run(command, check=False).returncode
            if result:
                print(f"FAIL FFmpeg installation failed with exit code {result}.")
                failed = True
            else:
                print("OK   FFmpeg installation completed. Open a new terminal, then rerun this check.")
    elif args.assembly:
        print("FAIL FFmpeg not found. Install it, add it to PATH, or pass --ffmpeg C:\\path\\ffmpeg.exe.")
        failed = True
    else:
        print("WARN FFmpeg not found. It is needed only for local video assembly.")

    try:
        import rembg  # type: ignore[import-not-found,unused-ignore]
    except ImportError:
        print("WARN Optional rembg not found. Product-reference packs will preserve source assets but cannot create automatic transparent cutouts.")
    else:
        print("OK   Optional rembg: automatic product-cutout candidates available (edge review still required).")

    print("INFO This skill can plan, audit, and write prompts without an API key.")
    print("INFO JiMeng API automation needs a provider-specific integration and local credentials; never store keys in this skill.")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
