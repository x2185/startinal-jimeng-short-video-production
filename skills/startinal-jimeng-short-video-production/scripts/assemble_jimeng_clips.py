#!/usr/bin/env python3
"""Join approved JiMeng clips with FFmpeg without invoking an AI model."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
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


def concat_line(path: Path) -> str:
    """Produce a safe FFmpeg concat-demuxer file line."""
    return "file '" + path.resolve().as_posix().replace("'", r"'\\''") + "'\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Join approved JiMeng clips with FFmpeg.")
    parser.add_argument("--clips", nargs="+", required=True, type=Path, help="Approved clips in playback order.")
    parser.add_argument("--output", required=True, type=Path, help="Final MP4 output path.")
    parser.add_argument(
        "--ffmpeg",
        type=Path,
        help="Path to the FFmpeg executable; use when FFmpeg is not on PATH.",
    )
    parser.add_argument("--reencode", action="store_true", help="Re-encode incompatible source clips to H.264/AAC.")
    parser.add_argument("--overwrite", action="store_true", help="Allow replacing an existing output file.")
    parser.add_argument("--dry-run", action="store_true", help="Print the command without running FFmpeg.")
    args = parser.parse_args()

    if len(args.clips) < 2:
        parser.error("Provide at least two clips.")
    missing = [str(path) for path in args.clips if not path.is_file()]
    if missing:
        parser.error("Missing clip(s): " + ", ".join(missing))
    if args.output.exists() and not args.overwrite:
        parser.error(f"Output already exists: {args.output}. Use --overwrite to replace it.")
    if args.ffmpeg is not None:
        if not args.ffmpeg.is_file():
            parser.error(f"FFmpeg executable does not exist: {args.ffmpeg}")
        ffmpeg = str(args.ffmpeg)
    else:
        ffmpeg = find_ffmpeg()
        if not ffmpeg:
            parser.error("FFmpeg was not found on PATH or under tools/. Install it, add it to PATH, or pass --ffmpeg C:\\path\\ffmpeg.exe.")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".txt", delete=False) as handle:
        concat_file = Path(handle.name)
        handle.writelines(concat_line(path) for path in args.clips)

    command = [ffmpeg, "-y" if args.overwrite else "-n", "-f", "concat", "-safe", "0", "-i", str(concat_file)]
    if args.reencode:
        command += ["-c:v", "libx264", "-preset", "medium", "-crf", "18", "-c:a", "aac", "-b:a", "192k"]
    else:
        command += ["-c", "copy"]
    command += ["-movflags", "+faststart", str(args.output)]

    print("FFmpeg command:", subprocess.list2cmdline(command))
    try:
        if args.dry_run:
            return 0
        return subprocess.run(command, check=False).returncode
    finally:
        concat_file.unlink(missing_ok=True)


if __name__ == "__main__":
    sys.exit(main())
