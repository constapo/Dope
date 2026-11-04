"""Content-hash keys and build folders, so unchanged voice clips and pictures are reused."""
from __future__ import annotations

import hashlib
import json
import os

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
VOICE_VERSION = "kokoro-v1.0"  # bump when the voice model changes so old clips are not reused


def key(*parts) -> str:
    blob = json.dumps(parts, sort_keys=True, ensure_ascii=False, default=str)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()[:16]


def voice_key(text: str, engine: str, name: str, speed: float) -> str:
    return key("voice", VOICE_VERSION, text, engine, name, round(float(speed), 3))


def picture_key(spec: dict) -> str:
    return key("picture", spec)


def build_dir(slug: str, out: str | None = None) -> str:
    d = os.path.abspath(out) if out else os.path.join(REPO_ROOT, "media", "reels", slug)
    for sub in ("", "voice", "pictures"):
        os.makedirs(os.path.join(d, sub), exist_ok=True)
    return d
