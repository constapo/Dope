"""Handheld phone camera move, ported from inonda-youtube-videos/free-build/archive/build_tiles_photo.py.

The camera is always level at chest height (constitution, Principle III): the only motion is a slow
zoom/slide across the still, a smooth hand shake and a tiny roll. There is no angle parameter.
"""
from __future__ import annotations

import numpy as np
from PIL import Image

OVERSIZE = 1.18  # room for the camera to move without showing edges
SHAKE = {"still": (0.0, 0.0, 0.0), "normal": (9.0, 7.0, 0.35), "strong": (14.0, 11.0, 0.5)}


def load_still(path: str, w: int, h: int):
    """Open a picture scaled so the frame fits with OVERSIZE spare. Returns (image, cropped?).

    A picture whose shape differs from the frame is centre-cropped by the frame window;
    'cropped' is True when more than 10 % of the picture is cut away, so it can be reported."""
    im = Image.open(path).convert("RGB")
    s = max(w * OVERSIZE / im.width, h * OVERSIZE / im.height)
    out = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    shown = (w * OVERSIZE * h * OVERSIZE) / (out.width * out.height)
    return out, shown < 0.9


def shake(n: int, seed: int, amp: float) -> np.ndarray:
    """Smooth random hand movement: low-pass filtered noise, in pixels (or degrees)."""
    if amp == 0 or n == 0:
        return np.zeros(n)
    rng = np.random.default_rng(seed)
    x = np.cumsum(rng.normal(0, 1, n + 60))
    x = np.convolve(x, np.ones(25) / 25, mode="same")[30:30 + n]
    x -= np.linspace(x[0], x[-1], n)  # no long drift: the camera move handles direction
    return x / (np.abs(x).max() + 1e-6) * amp


ROLL_MARGIN = 1.03  # extra zoom while rolling so no corner of the still ever shows


def frame(src, w, h, p, z0, z1, sx, sy, jx, jy, rot):
    """One frame of the move at progress p (0..1) with jitter jx, jy (px) and roll rot (deg).

    Zoom, slide, shake and roll are one affine transform (one resample per frame), which is
    about 6x faster than crop + rotate + resize and gives the same picture."""
    z = (z0 + (z1 - z0) * p) * (ROLL_MARGIN if abs(rot) > 0.01 else 1.0)
    cw, ch = w / z, h / z
    room_x, room_y = (src.width - cw) / 2, (src.height - ch) / 2
    cx = src.width / 2 + sx * (p - 0.5) * room_x * 0.9 + jx
    cy = src.height / 2 + sy * (p - 0.5) * room_y * 0.9 + jy
    cx = min(max(cx, cw / 2), src.width - cw / 2)
    cy = min(max(cy, ch / 2), src.height - ch / 2)
    t = np.radians(rot)
    a, b = np.cos(t) / z, np.sin(t) / z
    c, d = -np.sin(t) / z, np.cos(t) / z
    data = (a, b, cx - a * w / 2 - b * h / 2, c, d, cy - c * w / 2 - d * h / 2)
    return src.transform((w, h), Image.AFFINE, data, resample=Image.BILINEAR)
