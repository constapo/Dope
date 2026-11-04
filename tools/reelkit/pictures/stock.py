"""Free licensed stock (Mixkit, Pexels, Pixabay, Coverr, CC0, CC-BY), downloaded once.

The content maker picks the clip and gives its direct file link and licence; searching stock sites
is out of scope for v1 (research.md §4). Video clips are reduced to their middle frame.
"""
from __future__ import annotations

import os
import shutil
import ssl
import subprocess
import urllib.parse
import urllib.request

from .. import cache
from .net import PaymentRequired, http_get

MEDIA_EXT = {".jpg", ".jpeg", ".png", ".webp", ".mp4", ".mov", ".webm"}


class StockError(Exception):
    pass


def _host(url: str) -> str:
    host = urllib.parse.urlparse(url).hostname or "stock"
    parts = host.split(".")
    return parts[-2] if len(parts) >= 2 else host


def obtain(line, build_dir: str, get=http_get):
    spec = line.picture.spec
    url = spec["stock"]
    ext = os.path.splitext(urllib.parse.urlparse(url).path)[1].lower()
    if ext not in MEDIA_EXT:
        raise StockError(f"{url} looks like a web page, not a media file; give the direct file link "
                         "(ends in .jpg, .png, .webp or .mp4)")
    k = cache.picture_key(spec)
    raw = os.path.join(build_dir, "pictures", f"{k}{ext}")
    if not os.path.exists(raw):
        try:
            data = get(url)
        except PaymentRequired as e:
            raise StockError(f"{url} asked for payment ({e}); only free sources are allowed") from e
        with open(raw + ".part", "wb") as f:
            f.write(data)
        shutil.move(raw + ".part", raw)
    still = raw
    if ext in {".mp4", ".mov", ".webm"}:
        still = os.path.join(build_dir, "pictures", f"{k}.jpg")
        if not os.path.exists(still):
            dur = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of",
                                  "default=nw=1:nk=1", raw], capture_output=True, text=True).stdout.strip()
            mid = float(dur or 0) / 2
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{mid:.2f}", "-i", raw,
                            "-frames:v", "1", "-q:v", "2", still], check=True)
    return {"line": line.number, "key": k, "file": still, "source": _host(url), "licence": spec["licence"],
            "credit": spec.get("credit", ""), "ai_generated": False, "accepted": True, "attempts": 0,
            "note": "still taken from the middle of a stock video clip" if still != raw else ""}


__all__ = ["obtain", "StockError", "ssl", "urllib"]
