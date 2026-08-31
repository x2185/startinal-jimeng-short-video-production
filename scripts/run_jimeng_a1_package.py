#!/usr/bin/env python3
"""Generate a linked JiMeng A1 3.0 720P package and archive every artifact.

The runner uses Volcengine AK/SK Signature V4 directly and only reads credentials
from an ignored .env file or the process environment. It never prints secrets.

This is a legacy *single-first-frame* API runner. It must not be used for
mechanical or state-changing demonstrations that need multiple product views.
Prepare those jobs for JiMeng's All-reference UI instead, where the operator
can attach verified start, detail, and end-state evidence for the clip.
"""

from __future__ import annotations

import argparse
import base64
import datetime as dt
import hashlib
import hmac
import json
import os
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


HOST = "visual.volcengineapi.com"
REGION = "cn-north-1"
SERVICE = "cv"
API_VERSION = "2022-08-31"
REQ_KEY = "jimeng_i2v_first_v30"
SUBMIT_ACTION = "CVSync2AsyncSubmitTask"
RESULT_ACTION = "CVSync2AsyncGetResult"


def find_ffmpeg(explicit: str | None = None) -> str | None:
    """Resolve FFmpeg without requiring teammates to edit their system PATH.

    A project can carry ``tools/ffmpeg/.../ffmpeg.exe`` with it.  The runner may
    be launched either from that project or from an installed Skill folder, so
    check the working project first and the bundled-project layout second.
    """
    if explicit:
        candidate = Path(explicit).expanduser()
        return str(candidate) if candidate.is_file() else None
    on_path = shutil.which("ffmpeg")
    if on_path:
        return on_path
    roots = [Path.cwd(), Path(__file__).resolve().parents[3]]
    for root in roots:
        tools_dir = root / "tools"
        if not tools_dir.is_dir():
            continue
        candidates = sorted(tools_dir.glob("**/ffmpeg.exe"))
        if candidates:
            return str(candidates[0])
    return None


def load_dotenv(path: Path) -> None:
    """Load only unset variables from a simple ``KEY=VALUE`` or ``KEY:VALUE`` file."""
    if not path.is_file():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        separators = [index for index in (line.find("="), line.find(":")) if index >= 0]
        if not separators:
            continue
        separator_index = min(separators)
        key, value = line[:separator_index], line[separator_index + 1 :]
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def env_value(*names: str) -> str | None:
    for name in names:
        value = os.environ.get(name)
        if value:
            return value
    return None


def hmac_sha256(key: bytes, message: str) -> bytes:
    return hmac.new(key, message.encode("utf-8"), hashlib.sha256).digest()


def signing_key(secret: str, date_stamp: str) -> bytes:
    key_date = hmac_sha256(secret.encode("utf-8"), date_stamp)
    key_region = hmac_sha256(key_date, REGION)
    key_service = hmac_sha256(key_region, SERVICE)
    return hmac_sha256(key_service, "request")


def signed_post(action: str, body: dict[str, Any], ak: str, sk: str, timeout: int) -> dict[str, Any]:
    payload = json.dumps(body, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    payload_hash = hashlib.sha256(payload).hexdigest()
    now = dt.datetime.now(dt.timezone.utc)
    amz_date = now.strftime("%Y%m%dT%H%M%SZ")
    date_stamp = now.strftime("%Y%m%d")
    query_items = [("Action", action), ("Version", API_VERSION)]
    canonical_query = urllib.parse.urlencode(query_items, quote_via=urllib.parse.quote, safe="~-._")
    headers = {
        "content-type": "application/json",
        "host": HOST,
        "x-content-sha256": payload_hash,
        "x-date": amz_date,
    }
    signed_header_names = ";".join(sorted(headers))
    canonical_headers = "".join(f"{key}:{headers[key]}\n" for key in sorted(headers))
    canonical_request = "\n".join([
        "POST", "/", canonical_query, canonical_headers, signed_header_names, payload_hash
    ])
    credential_scope = f"{date_stamp}/{REGION}/{SERVICE}/request"
    string_to_sign = "\n".join([
        "HMAC-SHA256", amz_date, credential_scope,
        hashlib.sha256(canonical_request.encode("utf-8")).hexdigest(),
    ])
    signature = hmac.new(signing_key(sk, date_stamp), string_to_sign.encode("utf-8"), hashlib.sha256).hexdigest()
    authorization = (
        f"HMAC-SHA256 Credential={ak}/{credential_scope}, "
        f"SignedHeaders={signed_header_names}, Signature={signature}"
    )
    url = f"https://{HOST}/?{canonical_query}"
    request = urllib.request.Request(
        url,
        data=payload,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Host": HOST,
            "X-Content-Sha256": payload_hash,
            "X-Date": amz_date,
            "Authorization": authorization,
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = response.read()
    except urllib.error.HTTPError as exc:
        raw = exc.read()
        try:
            detail = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            detail = {"message": raw.decode("utf-8", errors="replace")}
        raise RuntimeError(f"API HTTP {exc.code}: {detail.get('message', detail)}") from exc
    try:
        return json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RuntimeError("API response was not valid JSON.") from exc


def require_success(response: dict[str, Any], stage: str) -> dict[str, Any]:
    if response.get("code") != 10000:
        request_id = response.get("request_id", "unknown")
        raise RuntimeError(f"{stage} failed: {response.get('message', 'unknown error')} (request_id={request_id})")
    data = response.get("data")
    if not isinstance(data, dict):
        raise RuntimeError(f"{stage} succeeded without an expected data object.")
    return data


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def submit_clip(reference: Path, prompt: str, frames: int, ak: str, sk: str, timeout: int) -> tuple[str, dict[str, Any]]:
    encoded = base64.b64encode(reference.read_bytes()).decode("ascii")
    response = signed_post(
        SUBMIT_ACTION,
        {"req_key": REQ_KEY, "binary_data_base64": [encoded], "prompt": prompt, "seed": -1, "frames": frames},
        ak,
        sk,
        timeout,
    )
    task_id = require_success(response, "Task submission").get("task_id")
    if not task_id:
        raise RuntimeError("Task submission succeeded without task_id.")
    return str(task_id), response


def wait_for_video(task_id: str, ak: str, sk: str, timeout: int, interval: int, max_wait: int) -> tuple[str, dict[str, Any]]:
    deadline = time.monotonic() + max_wait
    last_response: dict[str, Any] = {}
    while time.monotonic() < deadline:
        try:
            last_response = signed_post(RESULT_ACTION, {"req_key": REQ_KEY, "task_id": task_id}, ak, sk, timeout)
        except RuntimeError as exc:
            message = str(exc)
            if "<urlopen error" in message or "handshake operation timed out" in message:
                print(f"WARN Task {task_id} polling transport error; retrying after {interval}s.")
                time.sleep(interval)
                continue
            raise
        data = require_success(last_response, "Task polling")
        status = data.get("status")
        if status == "done":
            video_url = data.get("video_url")
            if not video_url:
                raise RuntimeError(f"Task {task_id} finished without video_url.")
            return str(video_url), last_response
        if status in {"expired", "not_found"}:
            raise RuntimeError(f"Task {task_id} ended with status={status}.")
        time.sleep(interval)
    raise RuntimeError(f"Task {task_id} did not finish within {max_wait} seconds.")


class DownloadError(RuntimeError):
    """Raised only after all automatic CDN download routes have been tried."""


def has_video_file(path: Path) -> bool:
    """Treat a non-trivial local MP4 as resumable; FFmpeg validates it next."""
    return path.is_file() and path.stat().st_size >= 1_024


def download(url: str, destination: Path, timeout: int, attempts: int, route: str) -> None:
    """Download with proxy-aware fallbacks and never leave a partial final file.

    `direct` bypasses Python's HTTP(S)_PROXY environment settings. It cannot turn
    off a VPN that tunnels all system traffic, but makes split-tunnel/proxy setups
    recover without operator intervention.
    """
    destination.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(url, headers={"User-Agent": "Startinal-JiMeng-Runner/1.0"})
    routes = [("system", False), ("direct", True)] if route == "auto" else [(route, route == "direct")]
    failures: list[str] = []
    for attempt in range(1, attempts + 1):
        route_name, direct = routes[(attempt - 1) % len(routes)]
        # Use a distinct temporary name per attempt.  On Windows, antivirus or
        # file-indexing can briefly hold a previous .part file after a failed
        # download; reusing it prevents a safe resume of an already-paid task.
        temporary = destination.with_suffix(destination.suffix + f".part-{attempt}")
        temporary.unlink(missing_ok=True)
        try:
            opener = urllib.request.build_opener(urllib.request.ProxyHandler({})) if direct else urllib.request.build_opener()
            with opener.open(request, timeout=timeout) as response, temporary.open("wb") as handle:
                shutil.copyfileobj(response, handle)
            if not has_video_file(temporary):
                raise RuntimeError("empty or too-small response")
            temporary.replace(destination)
            print(f"Downloaded video via {route_name} route.")
            return
        except (urllib.error.URLError, OSError, RuntimeError) as exc:
            temporary.unlink(missing_ok=True)
            failures.append(f"{route_name}: {exc}")
            if attempt < attempts:
                wait = min(attempt * 5, 30)
                print(f"WARN CDN download failed via {route_name}; retrying in {wait}s.")
                time.sleep(wait)
    raise DownloadError(f"Video download failed after {attempts} automatic attempts ({'; '.join(failures[-2:])}).")


def extract_handoff(ffmpeg: str, video: Path, handoff_dir: Path, clip_seconds: int) -> Path:
    """Archive candidate frames from a clip's stable final second."""
    handoff_dir.mkdir(parents=True, exist_ok=True)
    candidates = [8.0, 8.5, 9.0, 9.4] if clip_seconds == 10 else [3.0, 3.5, 4.0, 4.4]
    for second in candidates:
        target = handoff_dir / f"candidate-{second:.1f}s.jpg"
        subprocess.run(
            [ffmpeg, "-hide_banner", "-loglevel", "error", "-y", "-ss", str(second), "-i", str(video), "-frames:v", "1", "-q:v", "2", str(target)],
            check=True,
        )
    selected = handoff_dir / ("candidate-9.0s.jpg" if clip_seconds == 10 else "candidate-4.0s.jpg")
    if not selected.is_file():
        raise RuntimeError("Failed to extract selected handoff frame.")
    return selected


def assemble(ffmpeg: str, clips: list[Path], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    concat = output.with_suffix(".concat.txt")
    concat.write_text("".join(f"file '{clip.resolve().as_posix()}'\n" for clip in clips), encoding="utf-8")
    try:
        result = subprocess.run(
            [ffmpeg, "-hide_banner", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(concat), "-c", "copy", "-movflags", "+faststart", str(output)],
            check=False,
        )
        if result.returncode:
            raise RuntimeError("FFmpeg assembly failed.")
    finally:
        concat.unlink(missing_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate one linked 30-second JiMeng A1 package (3 x 10s or 6 x 5s).")
    parser.add_argument("--package", required=True, type=Path, help="JSON file with one reference_image and one prompt per clip (single-frame API only).")
    parser.add_argument("--output-dir", required=True, type=Path, help="Directory for prompts, task records, clips, handoffs, and final.")
    parser.add_argument("--env-file", type=Path, default=Path(".env"), help="Ignored local credential file.")
    parser.add_argument("--ffmpeg", help="FFmpeg executable path; otherwise resolve from PATH.")
    parser.add_argument("--poll-interval", type=int, default=10)
    parser.add_argument("--max-wait", type=int, default=1800)
    parser.add_argument("--http-timeout", type=int, default=60)
    parser.add_argument("--download-attempts", type=int, default=8, help="Automatic CDN download attempts per URL.")
    parser.add_argument("--download-route", choices=("auto", "system", "direct"), default="auto", help="CDN route: system proxy/VPN, proxy-bypassing direct, or both.")
    parser.add_argument("--max-clips", type=int, help="Generate only the first N linked clips for an explicit low-cost test; skips final assembly when N is smaller than the package total.")
    parser.add_argument("--dry-run", action="store_true", help="Validate package and credentials without API submission.")
    parser.add_argument("--resume", action="store_true", help="Resume from saved manifest without resubmitting completed/submitted clips.")
    args = parser.parse_args()

    load_dotenv(args.env_file)
    ak = env_value("VOLCENGINE_ACCESS_KEY_ID", "VOLC_ACCESSKEY", "AccessKeyID")
    sk = env_value("VOLCENGINE_SECRET_ACCESS_KEY", "VOLC_SECRETKEY", "SecretAccessKey")
    if not ak or not sk:
        parser.error("Missing Volcengine credentials. Set AccessKeyID/SecretAccessKey or VOLCENGINE_ACCESS_KEY_ID/VOLCENGINE_SECRET_ACCESS_KEY in the local .env.")
    package = json.loads(args.package.read_text(encoding="utf-8"))
    extra_references = package.get("reference_images")
    if isinstance(extra_references, list) and len(extra_references) > 1:
        parser.error(
            "This legacy first-frame API accepts one image only. For a multi-state "
            "action, use the All-reference UI submission plan instead of this runner."
        )
    reference = Path(package["reference_image"])
    prompts = package.get("prompts")
    clip_seconds = package.get("clip_seconds", 10)
    if clip_seconds not in {5, 10}:
        parser.error("Package clip_seconds must be 5 or 10.")
    expected_clips = 30 // clip_seconds
    clip_limit = args.max_clips if args.max_clips is not None else expected_clips
    if not 1 <= clip_limit <= expected_clips:
        parser.error(f"--max-clips must be between 1 and {expected_clips} for this package.")
    if package.get("test_only") and clip_limit != package.get("max_clips_required", 1):
        parser.error("This test-only package must be run with its declared --max-clips value; it cannot submit a full package by accident.")
    frames = 24 * clip_seconds + 1
    if not reference.is_file():
        parser.error(f"Reference image does not exist: {reference}")
    if not isinstance(prompts, list) or len(prompts) != expected_clips or not all(isinstance(item, str) and item.strip() for item in prompts):
        parser.error(f"Package JSON must contain exactly {expected_clips} non-empty prompts for {clip_seconds}s clips.")
    if reference.suffix.lower() not in {".jpg", ".jpeg", ".png"}:
        parser.error("Reference image must be JPEG or PNG.")
    if reference.stat().st_size > 4_700_000:
        parser.error("Reference image exceeds the API's 4.7 MB limit.")
    ffmpeg = find_ffmpeg(args.ffmpeg)
    if not ffmpeg and not args.dry_run:
        parser.error("FFmpeg is required for handoff extraction and assembly. Pass --ffmpeg, add it to PATH, or keep it under tools/.")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_json(args.output_dir / "prompts.json", package)
    manifest_path = args.output_dir / "manifest.json"
    if args.resume and manifest_path.is_file():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest.get("model") != REQ_KEY or manifest.get("reference_image") != str(reference.resolve()):
            parser.error("Existing manifest is not compatible with this package; use a new output directory.")
        manifest["status"] = "resuming"
        manifest.pop("error", None)
    else:
        manifest = {"status": "prepared", "model": REQ_KEY, "reference_image": str(reference.resolve()), "clips": []}
    write_json(manifest_path, manifest)
    print("OK credentials present (values hidden).")
    print(f"OK package validated: {clip_limit}/{expected_clips} clips x {clip_seconds}s, output={args.output_dir}")
    if args.dry_run:
        return 0

    current_reference = reference
    clips: list[Path] = []
    try:
        for index, prompt in enumerate(prompts[:clip_limit], start=1):
            clip_dir = args.output_dir / "clips" / f"clip-{index:02d}"
            existing = next((item for item in manifest["clips"] if item.get("clip") == index), None)
            if existing and existing.get("status") == "downloaded" and Path(existing.get("video", "")).is_file() and Path(existing.get("handoff", "")).is_file():
                clips.append(Path(existing["video"]))
                current_reference = Path(existing["handoff"])
                print(f"Reused downloaded clip {index}/{expected_clips}.")
                continue
            video = clip_dir / f"clip-{index:02d}.mp4"
            if existing and has_video_file(video):
                handoff = extract_handoff(str(ffmpeg), video, clip_dir / "handoff", clip_seconds)
                existing.update({"status": "downloaded", "video": str(video.resolve()), "handoff": str(handoff.resolve())})
                write_json(manifest_path, manifest)
                clips.append(video)
                current_reference = handoff
                print(f"Recovered existing local clip {index}/{expected_clips} without resubmitting or downloading.")
                continue
            if existing and existing.get("status") == "submitted" and existing.get("task_id"):
                task_id = str(existing["task_id"])
                print(f"Resuming submitted clip {index}/{expected_clips}: task_id={task_id}")
            else:
                task_id, submitted = submit_clip(current_reference, prompt, frames, ak, sk, args.http_timeout)
                write_json(clip_dir / "submit-response.json", submitted)
                entry = {"clip": index, "task_id": task_id, "reference": str(current_reference.resolve()), "status": "submitted"}
                if existing:
                    manifest["clips"][manifest["clips"].index(existing)] = entry
                else:
                    manifest["clips"].append(entry)
                write_json(manifest_path, manifest)
                print(f"Submitted clip {index}/{expected_clips}: task_id={task_id}")
            cached_result = clip_dir / "result-response.json"
            if cached_result.is_file():
                polled = json.loads(cached_result.read_text(encoding="utf-8"))
                cached_data = require_success(polled, "Cached task result")
                video_url = cached_data.get("video_url")
                if not video_url:
                    video_url, polled = wait_for_video(task_id, ak, sk, args.http_timeout, args.poll_interval, args.max_wait)
                else:
                    print(f"Reusing cached result URL for clip {index}/{expected_clips}.")
            else:
                video_url, polled = wait_for_video(task_id, ak, sk, args.http_timeout, args.poll_interval, args.max_wait)
            write_json(clip_dir / "result-response.json", polled)
            try:
                download(video_url, video, args.http_timeout, args.download_attempts, args.download_route)
            except DownloadError:
                # Signed CDN URLs are short-lived. Refresh once from the completed task,
                # then repeat the same automatic route fallback before declaring failure.
                print(f"WARN Refreshing completed task result for clip {index}/{clip_limit} and retrying CDN download.")
                video_url, polled = wait_for_video(task_id, ak, sk, args.http_timeout, args.poll_interval, args.max_wait)
                write_json(clip_dir / "result-response.json", polled)
                download(video_url, video, args.http_timeout, args.download_attempts, args.download_route)
            handoff = extract_handoff(str(ffmpeg), video, clip_dir / "handoff", clip_seconds)
            entry = next(item for item in manifest["clips"] if item.get("clip") == index)
            entry.update({"status": "downloaded", "video": str(video.resolve()), "handoff": str(handoff.resolve())})
            write_json(manifest_path, manifest)
            clips.append(video)
            current_reference = handoff
            print(f"Downloaded clip {index}/{expected_clips} and extracted handoff frame.")
        if clip_limit != expected_clips:
            manifest["status"] = "partial_completed"
            manifest["completed_clips"] = clip_limit
            write_json(manifest_path, manifest)
            print(f"Partial test completed: {clip_limit}/{expected_clips} clips. No final assembly was performed.")
            return 0
        final = args.output_dir / "finals" / "package-01-30s.mp4"
        assemble(str(ffmpeg), clips, final)
        manifest["status"] = "completed"
        manifest["final_video"] = str(final.resolve())
        write_json(manifest_path, manifest)
        print(f"Completed: {final}")
        return 0
    except Exception as exc:
        manifest["status"] = "failed"
        manifest["error"] = str(exc)
        write_json(manifest_path, manifest)
        print(f"FAILED: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
