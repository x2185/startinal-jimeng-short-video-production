from __future__ import annotations

import json
import os
import hashlib
import re
import sqlite3
import subprocess
import shutil
from contextlib import contextmanager
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Literal
from urllib import error as urllib_error
from urllib import request as urllib_request

import jwt
from fastapi import Depends, FastAPI, File, HTTPException, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import bcrypt
from pydantic import BaseModel, Field

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = Path(os.getenv("PRODUCTION_HUB_DATA_DIR", PROJECT_ROOT / "data"))
CATEGORY_UPLOAD_DIR = DATA_DIR / "catalog_uploads"
OUTPUT_DIR = DATA_DIR / "outputs"
DB_PATH = DATA_DIR / "production-hub.sqlite3"
JWT_SECRET = os.getenv("PRODUCTION_HUB_JWT_SECRET", "change-me-before-sharing")
TOKEN_TTL_HOURS = 12
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1").rstrip("/")
PRODUCTION_HUB_PROMPT_MODEL = os.getenv("PRODUCTION_HUB_PROMPT_MODEL", "gpt-5.6")
FFMPEG_BIN = os.getenv("PRODUCTION_HUB_FFMPEG_PATH", "ffmpeg")
ASSET_PREVIEW_DIR = DATA_DIR / "asset_previews"
MEDIA_TYPES = {
    ".jpg": "image", ".jpeg": "image", ".png": "image", ".webp": "image", ".gif": "image",
    ".mp4": "video", ".mov": "video", ".m4v": "video", ".webm": "video",
    ".mp3": "audio", ".wav": "audio", ".m4a": "audio",
    ".txt": "document", ".md": "document", ".pdf": "document", ".docx": "document", ".xlsx": "document", ".csv": "document",
}

bearer_scheme = HTTPBearer(auto_error=False)


def password_digest(password: str) -> bytes:
    # Pre-hash so bcrypt's 72-byte input limit cannot truncate a user's password.
    return hashlib.sha256(password.encode("utf-8")).digest()


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password_digest(password), bcrypt.gensalt()).decode("ascii")


def verify_password(password: str, stored_hash: str) -> bool:
    return bcrypt.checkpw(password_digest(password), stored_hash.encode("ascii"))

SCHEMA = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    display_name TEXT NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('admin', 'user')),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS product_records (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    owner_id INTEGER NOT NULL REFERENCES users(user_id),
    name TEXT NOT NULL,
    shop_url TEXT,
    target_market TEXT NOT NULL DEFAULT 'United States',
    language TEXT NOT NULL DEFAULT 'English (US)',
    selling_points TEXT NOT NULL DEFAULT '',
    restrictions TEXT NOT NULL DEFAULT '',
    asset_root TEXT NOT NULL DEFAULT '',
    status TEXT NOT NULL DEFAULT 'draft'
        CHECK(status IN ('draft', 'ready', 'archived')),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_product_records_owner_updated
ON product_records(owner_id, updated_at DESC);

CREATE TABLE IF NOT EXISTS assets (
    asset_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL REFERENCES product_records(product_id),
    source_path TEXT NOT NULL,
    sha256 TEXT NOT NULL,
    media_type TEXT NOT NULL,
    category TEXT NOT NULL,
    bytes INTEGER NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(product_id, sha256)
);

CREATE INDEX IF NOT EXISTS idx_assets_product_type
ON assets(product_id, media_type);

CREATE TABLE IF NOT EXISTS content_packages (
    package_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL REFERENCES product_records(product_id),
    requested_by INTEGER NOT NULL REFERENCES users(user_id),
    content_type TEXT NOT NULL CHECK(content_type IN ('ugc_mix', 'product_showcase')),
    creative_route TEXT NOT NULL,
    script TEXT NOT NULL,
    storyboard TEXT NOT NULL,
    prompt_notes TEXT NOT NULL,
    output_path TEXT NOT NULL DEFAULT '',
    status TEXT NOT NULL DEFAULT 'draft'
        CHECK(status IN ('draft', 'submitted', 'approved', 'changes_requested')),
    reviewer_note TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_content_packages_product_status
ON content_packages(product_id, status);
"""


@contextmanager
def database():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    ASSET_PREVIEW_DIR.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.executescript(SCHEMA)
    ensure_content_package_columns(connection)
    try:
        yield connection
        connection.commit()
    finally:
        connection.close()


def ensure_content_package_columns(connection: sqlite3.Connection) -> None:
    columns = {row["name"] for row in connection.execute("PRAGMA table_info(content_packages)").fetchall()}
    if "output_path" not in columns:
        connection.execute("ALTER TABLE content_packages ADD COLUMN output_path TEXT NOT NULL DEFAULT ''")


def utc_now() -> str:
    return datetime.now(UTC).isoformat()


def serialize_user(row: sqlite3.Row) -> dict:
    return {
        "id": row["user_id"],
        "email": row["email"],
        "display_name": row["display_name"],
        "role": row["role"],
    }


def serialize_product(row: sqlite3.Row) -> dict:
    return {
        "id": row["product_id"],
        "name": row["name"],
        "shop_url": row["shop_url"],
        "target_market": row["target_market"],
        "language": row["language"],
        "selling_points": row["selling_points"],
        "restrictions": row["restrictions"],
        "asset_root": row["asset_root"],
        "status": row["status"],
        "created_at": row["created_at"],
        "updated_at": row["updated_at"],
    }


class BootstrapPayload(BaseModel):
    email: str = "admin"
    display_name: str = Field(min_length=2, max_length=60)
    password: str = Field(min_length=4, max_length=120)


class LoginPayload(BaseModel):
    email: str
    password: str


class UserPayload(BaseModel):
    email: str
    display_name: str = Field(min_length=2, max_length=60)
    password: str = Field(min_length=8, max_length=120)
    role: Literal["admin", "user"] = "user"


class ProductPayload(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    shop_url: str | None = None
    target_market: str = "United States"
    language: str = "English (US)"
    selling_points: str = ""
    restrictions: str = ""
    asset_root: str = ""


class ProductUpdatePayload(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    shop_url: str | None = None
    target_market: str = "United States"
    language: str = "English (US)"
    selling_points: str = ""
    restrictions: str = ""
    asset_root: str = ""


class PackagePayload(BaseModel):
    product_id: int
    content_type: Literal["ugc_mix", "product_showcase"]
    creative_route: str = Field(min_length=2, max_length=120)


class ReviewPayload(BaseModel):
    status: Literal["approved", "changes_requested"]
    reviewer_note: str = Field(max_length=1000)


class ScanPayload(BaseModel):
    source_path: str = Field(min_length=1, max_length=1000)


class CatalogScanPayload(BaseModel):
    source_path: str = Field(min_length=1, max_length=1000)


def create_token(user: dict) -> str:
    payload = {
        "sub": str(user["id"]),
        "role": user["role"],
        "exp": datetime.now(UTC) + timedelta(hours=TOKEN_TTL_HOURS),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> dict:
    if not credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Please sign in.")
    try:
        payload = jwt.decode(credentials.credentials, JWT_SECRET, algorithms=["HS256"])
        user_id = int(payload["sub"])
    except (jwt.InvalidTokenError, KeyError, ValueError) as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid session.") from exc

    with database() as connection:
        row = connection.execute(
            "SELECT user_id, email, display_name, role FROM users WHERE user_id = ?",
            (user_id,),
        ).fetchone()
    if not row:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Account not found.")
    return serialize_user(row)


def require_admin(current_user: dict = Depends(get_current_user)) -> dict:
    if current_user["role"] != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Administrator access required.")
    return current_user


def split_lines(value: str | None, fallback: str) -> list[str]:
    if not value:
        return [fallback]
    items = [line.strip() for line in value.splitlines() if line.strip()]
    return items or [fallback]


def safe_asset_preview_root(product_id: int, asset_id: int) -> Path:
    root = ASSET_PREVIEW_DIR / f"product-{product_id}" / f"asset-{asset_id}"
    root.mkdir(parents=True, exist_ok=True)
    return root


def resolve_ffmpeg() -> str | None:
    try:
        import imageio_ffmpeg

        path = imageio_ffmpeg.get_ffmpeg_exe()
        if path:
            return path
    except Exception:
        pass
    return shutil.which(FFMPEG_BIN)


def inspect_image_asset(path: Path) -> str:
    try:
        from PIL import Image

        with Image.open(path) as image:
            return f"{path.name}: {image.width}x{image.height} {image.mode.lower()}"
    except Exception:
        return f"{path.name}: image file"


def inspect_text_asset(path: Path) -> str:
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return f"{path.name}: document file"
    snippet = " ".join(text.split())[:240]
    return f"{path.name}: {snippet}" if snippet else f"{path.name}: document file"


def extract_video_frames(path: Path, asset_id: int, product_id: int) -> list[Path]:
    ffmpeg = resolve_ffmpeg()
    if not ffmpeg:
        return []
    preview_root = safe_asset_preview_root(product_id, asset_id)
    frame_paths: list[Path] = []
    timestamps = [0.5, 2.0, 4.0]
    for index, timestamp in enumerate(timestamps, start=1):
        frame_path = preview_root / f"frame-{index:02d}.jpg"
        command = [
            ffmpeg,
            "-y",
            "-ss",
            str(timestamp),
            "-i",
            str(path),
            "-frames:v",
            "1",
            "-q:v",
            "2",
            str(frame_path),
        ]
        try:
            completed = subprocess.run(command, capture_output=True, check=False, timeout=30)
            if completed.returncode == 0 and frame_path.exists():
                frame_paths.append(frame_path)
        except Exception:
            break
    return frame_paths


def inspect_video_asset(path: Path, asset_id: int, product_id: int) -> str:
    frames = extract_video_frames(path, asset_id, product_id)
    if not frames:
        return f"{path.name}: video file (frame extraction unavailable)"
    frame_list = ", ".join(frame.name for frame in frames)
    return f"{path.name}: video key frames -> {frame_list}"


def summarize_assets(product_id: int, assets: list[sqlite3.Row]) -> tuple[list[str], list[str], list[str]]:
    if not assets:
        return ["no indexed assets yet"], ["no indexed assets yet"], ["no indexed assets yet"]
    categories: dict[str, int] = {}
    samples: list[str] = []
    notes: list[str] = []
    for asset in assets:
        category = asset["category"] or "未分类"
        categories[category] = categories.get(category, 0) + 1
        if len(samples) < 5:
            samples.append(Path(asset["source_path"]).name)
        path = Path(asset["source_path"])
        if asset["media_type"] == "image":
            notes.append(inspect_image_asset(path))
        elif asset["media_type"] == "video":
            notes.append(inspect_video_asset(path, int(asset["asset_id"]), product_id))
        elif asset["media_type"] == "document":
            notes.append(inspect_text_asset(path))
        else:
            notes.append(f"{path.name}: {asset['media_type']} file")
    category_summary = [f"{name} x{count}" for name, count in sorted(categories.items(), key=lambda item: (-item[1], item[0]))]
    return category_summary, samples, notes


def build_local_prompt_notes(
    product_name: str,
    selling_points: list[str],
    restrictions: list[str],
    asset_categories: list[str],
    asset_samples: list[str],
    asset_notes: list[str],
    content_type: str,
) -> str:
    product_signal = f"{product_name} · {content_type}"
    asset_note_1 = asset_notes[0] if asset_notes else "no asset notes"
    asset_note_2 = asset_notes[1] if len(asset_notes) > 1 else asset_note_1
    asset_note_3 = asset_notes[2] if len(asset_notes) > 2 else asset_note_1
    prompt_angles = [
        f"identity lock: use the indexed assets ({', '.join(asset_categories[:3])}) as the source of truth",
        f"opening beat: strongest first-frame reaction based on {asset_samples[0] if asset_samples else product_name}",
        f"hands-on proof: show the product being held, used, or tested naturally around {asset_samples[1] if len(asset_samples) > 1 else product_name}",
        f"detail macro: emphasize surface, texture, buttons, seams, or moving parts visible in {asset_samples[2] if len(asset_samples) > 2 else 'the indexed assets'}",
        f"real-home context: place the product in an ordinary room setting that matches {asset_note_1}",
        f"benefit demonstration: show the verified point '{selling_points[0]}' clearly and simply using the real product",
        f"comparison angle: show the claim '{selling_points[1 % len(selling_points)]}' with a practical before/after style proof",
        f"close-up motion: slow push-in or gentle handheld movement on the product and its details from {asset_note_2}",
        f"package reality: show the actual packaging or part names without distortion if present in {asset_categories[0]}",
        f"trust cue: keep logo, color, and shape faithful to the reference assets",
        f"human scale: include hands or table interaction for size clarity using the real product photos",
        f"soundless clarity: let the image explain '{selling_points[2 % len(selling_points)]}' without narration",
        f"clean cutaway: one subject, no unrelated props, no cluttered background, based on {product_signal}",
        f"retail-safe look: avoid '{restrictions[0]}', only visible verified facts from the assets",
        f"CTA frame: leave clean space for product-link text at the end while keeping {product_name} centered",
        f"alternate angle: show the product from a second useful viewpoint and keep '{product_signal}' in focus",
        f"texture proof: highlight material quality, finish, or surface detail related to '{selling_points[3 % len(selling_points)]}'",
        f"motion proof: show a real action cycle that proves '{selling_points[4 % len(selling_points)]}' using {asset_note_3}",
        f"social-native framing: make it feel like a creator shot for {product_name}, not a studio ad",
        f"assembly-ready: make each clip short, specific, and usable for {content_type}, with scene ideas derived from the indexed assets",
    ]
    return (
        "JiMeng execution rule: generate exactly 5 seconds per prompt; use the same product reference for every selected clip and keep a stable final frame for the next edit cut.\n\n"
        + "\n\n".join(
        [
            f"{index:02d}. Reference the supplied {product_name} images for product identity. "
            f"Vertical 9:16, realistic handheld product footage, natural home lighting, one product only, "
            f"preserve shape/color/logo/text, no warped packaging, no extra fingers, no unrelated brands. "
            f"{variant}. Generate 4–8 second clips for assembly."
            for index, variant in enumerate(prompt_angles, start=1)
        ]
        )
    )


def extract_responses_text(data: dict) -> str:
    output_text = data.get("output_text")
    if isinstance(output_text, str) and output_text.strip():
        return output_text.strip()
    for item in data.get("output", []):
        if item.get("type") != "message":
            continue
        for content in item.get("content", []):
            if content.get("type") in {"output_text", "text"} and content.get("text"):
                return content["text"].strip()
    raise RuntimeError("OpenAI response did not include text output.")


# A five-second unit is the safe common denominator for JiMeng video modes.
# The finished 30-second social video is assembled outside the generator.
JIMENG_CLIP_SECONDS = 5
JIMENG_TOTAL_SECONDS = 30


def build_jimeng_assembly_storyboard() -> str:
    """Return a duration-safe, cut-ready plan rather than one long generation."""
    shots = [
        ("0–5s", "Hook", "Strongest result or reaction; finish on a stable product reveal."),
        ("5–10s", "Reveal", "Unbox or hand-hold the real product; match the prior ending when possible."),
        ("10–15s", "Proof A", "Show one complete, simple use action; end with the product centered."),
        ("15–20s", "Proof B", "Show a second detail or outcome; preserve product identity and setting."),
        ("20–25s", "Detail", "Macro detail or scale cue; hold the final frame clean for a transition."),
        ("25–30s", "CTA", "Product hero with empty safe area for the TikTok Shop product link."),
    ]
    header = (
        f"JiMeng duration-safe assembly plan — {len(shots)} × {JIMENG_CLIP_SECONDS}s clips = {JIMENG_TOTAL_SECONDS}s final edit\n"
        "Generate each row separately. Reuse the same product reference image for every clip; when available, use the prior selected clip's last frame as the next clip's reference. "
        "Do not request one 30-second generation.\n"
    )
    return header + "\n".join(f"{time}  [{name}, {JIMENG_CLIP_SECONDS}s]  {direction}" for time, name, direction in shots)


def generate_prompt_notes(product: sqlite3.Row, assets: list[sqlite3.Row], content_type: str, route: str) -> str:
    product_name = product["name"]
    selling_points = split_lines(product["selling_points"], "verified product details")
    restrictions = split_lines(product["restrictions"], "avoid unsupported claims or visuals")
    asset_categories, asset_samples, asset_notes = summarize_assets(int(product["product_id"]), assets)
    local_fallback = build_local_prompt_notes(
        product_name,
        selling_points,
        restrictions,
        asset_categories,
        asset_samples,
        asset_notes,
        content_type,
    )
    if not OPENAI_API_KEY:
        return local_fallback

    system_prompt = (
        "You write short, practical product-video prompts. "
        "Return valid JSON only, with a top-level object that has a prompts array of exactly 20 strings. "
        "Each string should be distinct and tailored to the product assets, not just the product name. "
        "Every prompt must request exactly 5 seconds and a clean final composition that can be cut into another clip."
    )
    user_prompt = {
        "product_name": product_name,
        "creative_route": route,
        "content_type": content_type,
        "selling_points": selling_points,
        "restrictions": restrictions,
        "asset_categories": asset_categories,
        "asset_samples": asset_samples,
        "asset_notes": asset_notes[:12],
        "requirements": [
            "Exactly 20 prompts",
            "Use the product name, asset categories, file-name hints, selling points, restrictions, and asset notes",
            "Each prompt should differ meaningfully from the others",
            "Keep prompts suitable for JiMeng video generation",
            "Use concise English",
            "Specify exactly 5 seconds, never one long 30-second generation",
            "Preserve product identity across clips and leave a stable final frame for an edit cut",
        ],
    }
    request_body = {
        "model": PRODUCTION_HUB_PROMPT_MODEL,
        "input": [
            {
                "role": "system",
                "content": [{"type": "input_text", "text": system_prompt}],
            },
            {
                "role": "user",
                "content": [{"type": "input_text", "text": json.dumps(user_prompt, ensure_ascii=False)}],
            },
        ],
    }
    req = urllib_request.Request(
        f"{OPENAI_API_BASE}/responses",
        data=json.dumps(request_body).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {OPENAI_API_KEY}",
        },
        method="POST",
    )
    try:
        with urllib_request.urlopen(req, timeout=90) as response:
            data = json.loads(response.read().decode("utf-8"))
        raw_text = extract_responses_text(data)
        payload = json.loads(raw_text)
        prompts = payload.get("prompts")
        if not isinstance(prompts, list) or len(prompts) != 20:
            raise RuntimeError("OpenAI response did not return 20 prompts.")
        cleaned = [str(item).strip() for item in prompts if str(item).strip()]
        if len(cleaned) != 20:
            raise RuntimeError("OpenAI response contained empty prompts.")
        return "\n\n".join(f"{index:02d}. {prompt}" for index, prompt in enumerate(cleaned, start=1))
    except (urllib_error.HTTPError, urllib_error.URLError, TimeoutError, json.JSONDecodeError, RuntimeError):
        return local_fallback


def generated_package(product: sqlite3.Row, assets: list[sqlite3.Row], content_type: str, route: str) -> tuple[str, str, str]:
    product_name = product["name"]
    selling_points = split_lines(product["selling_points"], "verified product details")
    format_name = "UGC talking-head mix" if content_type == "ugc_mix" else "product showcase"
    script = (
        f"[{format_name} · {route}]\n\n"
        f"Hook: “I did not expect {product_name} to be this satisfying.”\n"
        "Reveal: “Here’s what you actually get.”\n"
        f"Proof: Show the product doing its real job; highlight only verified points: {selling_points[0]}.\n"
        "Close: “Tap the product link to see the full details.”"
    )
    storyboard = (
        "0–2s  Stop moment — strongest visual result or reaction\n"
        "2–7s  Real reveal — unbox or hand-hold the actual product\n"
        "7–17s Proof — show one function or play moment clearly\n"
        "17–25s Detail — close-up and a second piece of visual proof\n"
        "25–30s CTA — product hero and TikTok Shop product-link prompt"
    )
    # The legacy outline above describes the creative beats.  Replace it with
    # an executable plan that respects JiMeng's short-clip duration limit.
    storyboard = build_jimeng_assembly_storyboard()
    asset_rows = assets
    prompts = generate_prompt_notes(product, asset_rows, content_type, route)
    return script, storyboard, prompts


def safe_path_part(value: str) -> str:
    cleaned = re.sub(r"[^0-9A-Za-z\u4e00-\u9fff._ -]+", "_", value).strip(" ._-")
    return cleaned or "product"


def planned_output_path(product: sqlite3.Row, package_id: int, content_type: str) -> str:
    product_folder = safe_path_part(product["name"])
    output_file = f"{package_id:06d}_{content_type}.mp4"
    return str(OUTPUT_DIR / f"product-{product['product_id']}" / product_folder / output_file)


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        while chunk := file.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


app = FastAPI(title="Startinal Product Motion Forge", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health():
    return {"status": "ok", "storage_mode": "local-first"}


@app.get("/api/setup-status")
def setup_status():
    with database() as connection:
        count = connection.execute("SELECT COUNT(*) AS total FROM users").fetchone()["total"]
    return {"needs_bootstrap": count == 0}


@app.post("/api/bootstrap")
def bootstrap(payload: BootstrapPayload):
    with database() as connection:
        count = connection.execute("SELECT COUNT(*) AS total FROM users").fetchone()["total"]
        if count:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Setup is already complete.")
        cursor = connection.execute(
            "INSERT INTO users(email, display_name, password_hash, role) VALUES (?, ?, ?, 'admin')",
            (payload.email.lower().strip(), payload.display_name.strip(), hash_password(payload.password)),
        )
        row = connection.execute(
            "SELECT user_id, email, display_name, role FROM users WHERE user_id = ?",
            (cursor.lastrowid,),
        ).fetchone()
    user = serialize_user(row)
    return {"token": create_token(user), "user": user}


@app.post("/api/login")
def login(payload: LoginPayload):
    with database() as connection:
        row = connection.execute("SELECT * FROM users WHERE email = ?", (payload.email.lower().strip(),)).fetchone()
    if not row or not verify_password(payload.password, row["password_hash"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password.")
    user = serialize_user(row)
    return {"token": create_token(user), "user": user}


@app.get("/api/me")
def me(current_user: dict = Depends(get_current_user)):
    return current_user


@app.get("/api/products")
def list_products(current_user: dict = Depends(get_current_user)):
    with database() as connection:
        if current_user["role"] == "admin":
            rows = connection.execute("SELECT * FROM product_records ORDER BY updated_at DESC").fetchall()
        else:
            rows = connection.execute(
                "SELECT * FROM product_records WHERE owner_id = ? ORDER BY updated_at DESC",
                (current_user["id"],),
            ).fetchall()
    return [serialize_product(row) for row in rows]


@app.post("/api/products")
def create_product(payload: ProductPayload, current_user: dict = Depends(get_current_user)):
    with database() as connection:
        cursor = connection.execute(
            """
            INSERT INTO product_records(owner_id, name, shop_url, target_market, language, selling_points, restrictions, asset_root, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                current_user["id"], payload.name.strip(), payload.shop_url, payload.target_market,
                payload.language, payload.selling_points, payload.restrictions, payload.asset_root, utc_now(),
            ),
        )
        row = connection.execute("SELECT * FROM product_records WHERE product_id = ?", (cursor.lastrowid,)).fetchone()
    return serialize_product(row)


@app.patch("/api/products/{product_id}")
def update_product(product_id: int, payload: ProductUpdatePayload, current_user: dict = Depends(get_current_user)):
    with database() as connection:
        product = connection.execute("SELECT * FROM product_records WHERE product_id = ?", (product_id,)).fetchone()
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="商品不存在。")
        if current_user["role"] != "admin" and product["owner_id"] != current_user["id"]:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="你没有权限修改这个商品。")
        connection.execute(
            """
            UPDATE product_records
            SET name = ?, shop_url = ?, target_market = ?, language = ?, selling_points = ?, restrictions = ?, asset_root = ?, updated_at = ?
            WHERE product_id = ?
            """,
            (
                payload.name.strip(),
                payload.shop_url,
                payload.target_market,
                payload.language,
                payload.selling_points,
                payload.restrictions,
                payload.asset_root,
                utc_now(),
                product_id,
            ),
        )
        row = connection.execute("SELECT * FROM product_records WHERE product_id = ?", (product_id,)).fetchone()
    return serialize_product(row)


@app.post("/api/products/{product_id}/scan")
def scan_product_assets(product_id: int, payload: ScanPayload, current_user: dict = Depends(get_current_user)):
    source_root = Path(payload.source_path).expanduser().resolve()
    if not source_root.is_dir():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="素材文件夹不存在或后端无法访问。")
    with database() as connection:
        product = connection.execute("SELECT * FROM product_records WHERE product_id = ?", (product_id,)).fetchone()
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="商品不存在。")
        if current_user["role"] != "admin" and product["owner_id"] != current_user["id"]:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="你没有权限扫描这个商品。")
        result = {"indexed": 0, "duplicates": 0, "ignored": 0, "by_type": {}}
        for path in source_root.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in MEDIA_TYPES:
                if path.is_file(): result["ignored"] += 1
                continue
            kind = MEDIA_TYPES[path.suffix.lower()]
            fingerprint = file_hash(path)
            relative_parts = path.relative_to(source_root).parts
            category = relative_parts[0] if len(relative_parts) > 1 else "未分类"
            cursor = connection.execute(
                "INSERT OR IGNORE INTO assets(product_id, source_path, sha256, media_type, category, bytes) VALUES (?, ?, ?, ?, ?, ?)",
                (product_id, str(path), fingerprint, kind, category, path.stat().st_size),
            )
            if cursor.rowcount:
                result["indexed"] += 1
                result["by_type"][kind] = result["by_type"].get(kind, 0) + 1
            else:
                result["duplicates"] += 1
        connection.execute("UPDATE product_records SET asset_root = ?, updated_at = ? WHERE product_id = ?", (str(source_root), utc_now(), product_id))
    return result


@app.post("/api/catalog/scan")
def scan_product_catalog(payload: CatalogScanPayload, current_user: dict = Depends(get_current_user)):
    catalog_root = Path(payload.source_path).expanduser().resolve()
    if not catalog_root.is_dir():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="产品总文件夹不存在或后端无法访问。")
    folders = sorted([entry for entry in catalog_root.iterdir() if entry.is_dir()], key=lambda entry: entry.name.lower())
    if not folders:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="总文件夹下没有产品子文件夹。")
    summary = {"products_created": 0, "products_existing": 0, "assets_indexed": 0, "duplicates": 0, "ignored": 0, "products": []}
    with database() as connection:
        for folder in folders:
            product = connection.execute(
                "SELECT * FROM product_records WHERE owner_id = ? AND name = ? ORDER BY product_id LIMIT 1",
                (current_user["id"], folder.name),
            ).fetchone()
            if product:
                summary["products_existing"] += 1
                product_id = product["product_id"]
            else:
                cursor = connection.execute(
                    "INSERT INTO product_records(owner_id, name, asset_root, updated_at) VALUES (?, ?, ?, ?)",
                    (current_user["id"], folder.name, str(folder), utc_now()),
                )
                product_id = cursor.lastrowid
                summary["products_created"] += 1
            result = {"indexed": 0, "duplicates": 0, "ignored": 0}
            for path in folder.rglob("*"):
                if not path.is_file() or path.suffix.lower() not in MEDIA_TYPES:
                    if path.is_file(): result["ignored"] += 1
                    continue
                kind = MEDIA_TYPES[path.suffix.lower()]
                fingerprint = file_hash(path)
                relative_parts = path.relative_to(folder).parts
                category = relative_parts[0] if len(relative_parts) > 1 else "未分类"
                cursor = connection.execute(
                    "INSERT OR IGNORE INTO assets(product_id, source_path, sha256, media_type, category, bytes) VALUES (?, ?, ?, ?, ?, ?)",
                    (product_id, str(path), fingerprint, kind, category, path.stat().st_size),
                )
                if cursor.rowcount: result["indexed"] += 1
                else: result["duplicates"] += 1
            summary["assets_indexed"] += result["indexed"]
            summary["duplicates"] += result["duplicates"]
            summary["ignored"] += result["ignored"]
            summary["products"].append({"name": folder.name, **result})
    return summary


@app.post("/api/catalog/upload")
async def upload_product_catalog(files: list[UploadFile] = File(...), current_user: dict = Depends(get_current_user)):
    """Browser-compatible folder import. Files are copied into the local data directory, then indexed."""
    if not files:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="没有选择素材文件。")
    import_root = CATEGORY_UPLOAD_DIR / f"user-{current_user['id']}-{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
    imported = 0
    for upload in files:
        raw_name = (upload.filename or "").replace("\\", "/")
        relative = Path(raw_name)
        if not raw_name or relative.is_absolute() or ".." in relative.parts:
            continue
        target = (import_root / relative).resolve()
        if import_root.resolve() not in target.parents:
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("wb") as output:
            while chunk := await upload.read(1024 * 1024):
                output.write(chunk)
        imported += 1
    if not imported:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="未找到可导入的文件。")
    scan_root = import_root
    top_level = [entry for entry in import_root.iterdir() if entry.is_dir()]
    if len(top_level) == 1 and any(entry.is_dir() for entry in top_level[0].iterdir()):
        scan_root = top_level[0]
    return scan_product_catalog(CatalogScanPayload(source_path=str(scan_root)), current_user)


@app.get("/api/products/{product_id}/assets")
def list_product_assets(product_id: int, current_user: dict = Depends(get_current_user)):
    with database() as connection:
        product = connection.execute("SELECT * FROM product_records WHERE product_id = ?", (product_id,)).fetchone()
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="商品不存在。")
        if current_user["role"] != "admin" and product["owner_id"] != current_user["id"]:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="你没有权限查看这个商品。")
        rows = connection.execute("SELECT asset_id, source_path, media_type, category, bytes, created_at FROM assets WHERE product_id = ? ORDER BY asset_id", (product_id,)).fetchall()
    return [dict(row) for row in rows]


@app.get("/api/packages")
def list_packages(current_user: dict = Depends(get_current_user)):
    with database() as connection:
        query = """
            SELECT p.*, pr.name AS product_name, u.display_name AS requester_name
            FROM content_packages p
            JOIN product_records pr ON pr.product_id = p.product_id
            JOIN users u ON u.user_id = p.requested_by
        """
        if current_user["role"] == "admin":
            rows = connection.execute(query + " ORDER BY p.updated_at DESC").fetchall()
        else:
            rows = connection.execute(query + " WHERE p.requested_by = ? ORDER BY p.updated_at DESC", (current_user["id"],)).fetchall()
    return [dict(row) for row in rows]


@app.post("/api/packages")
def create_package(payload: PackagePayload, current_user: dict = Depends(get_current_user)):
    with database() as connection:
        product = connection.execute("SELECT * FROM product_records WHERE product_id = ?", (payload.product_id,)).fetchone()
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found.")
        if current_user["role"] != "admin" and product["owner_id"] != current_user["id"]:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not own this product.")
        assets = connection.execute(
            "SELECT asset_id, source_path, media_type, category, bytes, created_at FROM assets WHERE product_id = ? ORDER BY asset_id",
            (payload.product_id,),
        ).fetchall()
        script, storyboard, prompts = generated_package(product, list(assets), payload.content_type, payload.creative_route)
        cursor = connection.execute(
            """
            INSERT INTO content_packages(product_id, requested_by, content_type, creative_route, script, storyboard, prompt_notes, output_path, status, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'draft', ?)
            """,
            (
                payload.product_id,
                current_user["id"],
                payload.content_type,
                payload.creative_route,
                script,
                storyboard,
                prompts,
                "",
                utc_now(),
            ),
        )
        output_path = planned_output_path(product, cursor.lastrowid, payload.content_type)
        connection.execute(
            "UPDATE content_packages SET output_path = ?, updated_at = ? WHERE package_id = ?",
            (output_path, utc_now(), cursor.lastrowid),
        )
        row = connection.execute("SELECT * FROM content_packages WHERE package_id = ?", (cursor.lastrowid,)).fetchone()
    return dict(row)


@app.post("/api/packages/{package_id}/regenerate")
def regenerate_package(package_id: int, current_user: dict = Depends(get_current_user)):
    with database() as connection:
        row = connection.execute("SELECT * FROM content_packages WHERE package_id = ?", (package_id,)).fetchone()
        if not row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Production package not found.")
        product = connection.execute("SELECT * FROM product_records WHERE product_id = ?", (row["product_id"],)).fetchone()
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="商品不存在。")
        if current_user["role"] != "admin" and row["requested_by"] != current_user["id"]:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not own this production package.")
        assets = connection.execute(
            "SELECT asset_id, source_path, media_type, category, bytes, created_at FROM assets WHERE product_id = ? ORDER BY asset_id",
            (row["product_id"],),
        ).fetchall()
        script, storyboard, prompts = generated_package(product, list(assets), row["content_type"], row["creative_route"])
        connection.execute(
            """
            UPDATE content_packages
            SET script = ?, storyboard = ?, prompt_notes = ?, updated_at = ?
            WHERE package_id = ?
            """,
            (script, storyboard, prompts, utc_now(), package_id),
        )
        updated = connection.execute("SELECT * FROM content_packages WHERE package_id = ?", (package_id,)).fetchone()
    return dict(updated)


@app.post("/api/packages/{package_id}/submit")
def submit_package(package_id: int, current_user: dict = Depends(get_current_user)):
    with database() as connection:
        row = connection.execute("SELECT * FROM content_packages WHERE package_id = ?", (package_id,)).fetchone()
        if not row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Production package not found.")
        if current_user["role"] != "admin" and row["requested_by"] != current_user["id"]:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not own this production package.")
        connection.execute(
            "UPDATE content_packages SET status = 'submitted', updated_at = ? WHERE package_id = ?",
            (utc_now(), package_id),
        )
    return {"ok": True}


@app.post("/api/packages/{package_id}/complete")
def complete_package(package_id: int, current_user: dict = Depends(get_current_user)):
    with database() as connection:
        row = connection.execute("SELECT * FROM content_packages WHERE package_id = ?", (package_id,)).fetchone()
        if not row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Production package not found.")
        if current_user["role"] != "admin" and row["requested_by"] != current_user["id"]:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not own this production package.")
        connection.execute(
            "UPDATE content_packages SET status = 'approved', updated_at = ? WHERE package_id = ?",
            (utc_now(), package_id),
        )
    return {"ok": True}


@app.delete("/api/packages/{package_id}")
def delete_package(package_id: int, current_user: dict = Depends(get_current_user)):
    with database() as connection:
        row = connection.execute("SELECT * FROM content_packages WHERE package_id = ?", (package_id,)).fetchone()
        if not row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Production package not found.")
        if current_user["role"] != "admin" and row["requested_by"] != current_user["id"]:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not own this production package.")
        connection.execute("DELETE FROM content_packages WHERE package_id = ?", (package_id,))
    return {"ok": True}


@app.post("/api/packages/{package_id}/review")
def review_package(package_id: int, payload: ReviewPayload, _: dict = Depends(require_admin)):
    with database() as connection:
        updated = connection.execute(
            "UPDATE content_packages SET status = ?, reviewer_note = ?, updated_at = ? WHERE package_id = ?",
            (payload.status, payload.reviewer_note, utc_now(), package_id),
        ).rowcount
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Production package not found.")
    return {"ok": True}


@app.get("/api/users")
def list_users(_: dict = Depends(require_admin)):
    with database() as connection:
        rows = connection.execute("SELECT user_id, email, display_name, role FROM users ORDER BY created_at").fetchall()
    return [serialize_user(row) for row in rows]


@app.post("/api/users")
def create_user(payload: UserPayload, _: dict = Depends(require_admin)):
    try:
        with database() as connection:
            cursor = connection.execute(
                "INSERT INTO users(email, display_name, password_hash, role) VALUES (?, ?, ?, ?)",
                (payload.email.lower().strip(), payload.display_name.strip(), hash_password(payload.password), payload.role),
            )
            row = connection.execute(
                "SELECT user_id, email, display_name, role FROM users WHERE user_id = ?", (cursor.lastrowid,)
            ).fetchone()
    except sqlite3.IntegrityError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="This email is already in use.") from exc
    return serialize_user(row)
