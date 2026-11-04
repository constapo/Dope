"""Timeline maths and rendering: pictures with handheld moves, labels, Greek subtitles, end card."""
from __future__ import annotations

import multiprocessing
import os
import subprocess

import numpy as np
import soundfile
from PIL import ImageDraw, ImageFont

from . import motion
from .endcard import ACCENT, FONT_B, NAVY, end_card, text_center, wrap

FPS = 30
LEAD = 0.4       # silence before the first line, seconds
GAP = 0.35       # pause after each line, seconds
SUB_TAIL = 0.3   # subtitle stays this long after the words end
MAX_SUB_LINES = 2


def timeline(plan, clip_lengths: list[float]) -> dict:
    """Start/end of every line, when its subtitle shows, and the total length.

    Each line lasts its speech plus GAP, or min_seconds if longer (plan timings are minimums)."""
    spans, t = [], LEAD
    for line, length in zip(plan.lines, clip_lengths):
        end = t + max(length + GAP, line.min_seconds)
        spans.append({"line": line.number, "start": t, "speech_end": t + length,
                      "sub_end": min(end, t + length + SUB_TAIL), "end": end})
        t = end
    return {"spans": spans, "shots_end": t, "total": t + plan.end_card_seconds}


def assemble_audio(plan, clip_paths: list[str], tl: dict, out: str) -> float:
    clips = [soundfile.read(p, dtype="float32") for p in clip_paths]
    sr = clips[0][1]
    audio = np.zeros(int(round(tl["total"] * sr)) + 1, dtype=np.float32)
    for (samples, csr), span in zip(clips, tl["spans"]):
        if csr != sr:
            raise ValueError("voice clips have different sample rates")
        if samples.ndim > 1:
            samples = samples.mean(axis=1)
        i = int(round(span["start"] * sr))
        audio[i:i + len(samples)] = samples[: len(audio) - i]
    soundfile.write(out, audio, sr)
    return len(audio) / sr


def render(plan, build_dir: str, picture_files: dict, clip_paths: list[str], warnings: list):
    w, h = plan.size
    clip_lengths = [soundfile.info(p).duration for p in clip_paths]
    tl = timeline(plan, clip_lengths)
    wav = os.path.join(build_dir, "voice.wav")
    assemble_audio(plan, clip_paths, tl, wav)

    stills = {}
    for line in plan.lines:
        path = picture_files[line.number]
        if path not in stills:
            stills[path], cropped = motion.load_still(path, w, h)
            if cropped:
                warnings.append(f"line {line.number}: picture shape differs from the frame; centre-cropped")
    card = end_card(w, h)
    scale = w / 1080 if h > w else h / 1080
    f_sub = ImageFont.truetype(FONT_B, max(20, int(50 * scale)))
    f_lab = ImageFont.truetype(FONT_B, max(20, int(54 * scale)))

    probe = ImageDraw.Draw(card.copy())
    subs = {}
    base = max(20, int(50 * scale))
    for line in plan.lines:
        size = base
        while True:  # shrink the subtitle (down to 75 %) before giving up on two lines
            font = ImageFont.truetype(FONT_B, size)
            lines = wrap(probe, line.greek, font, w - int(140 * scale))
            if len(lines) <= MAX_SUB_LINES or size <= int(base * 0.75):
                break
            size -= 2
        if len(lines) > MAX_SUB_LINES:
            warnings.append(f"line {line.number}: Greek subtitle needs {len(lines)} lines on screen; shorten it")
        subs[line.number] = (lines, font)

    n = int(round(tl["total"] * FPS))
    out = os.path.join(build_dir, f"{plan.slug}.mp4")
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                           "-s", f"{w}x{h}", "-r", str(FPS), "-i", "-", "-i", wav, "-c:v", "libx264",
                           "-preset", "fast", "-crf", "19", "-pix_fmt", "yuv420p", "-c:a", "aac",
                           "-b:a", "160k", "-t", f"{tl['total']:.3f}", "-movflags", "+faststart", out],
                          stdin=subprocess.PIPE)
    global _STATE
    _STATE = {"plan": plan, "w": w, "h": h, "tl": tl, "stills": stills, "files": picture_files,
              "subs": subs, "scale": scale, "f_sub": f_sub, "f_lab": f_lab, "card": card.tobytes(),
              "jitter": [motion.shake(n, s, 1.0) for s in (1, 2, 3)]}
    workers = max(1, min(8, (os.cpu_count() or 2) - 1))
    try:
        if workers > 1 and "fork" in multiprocessing.get_all_start_methods():
            with multiprocessing.get_context("fork").Pool(workers) as pool:
                for fr in pool.imap(_frame_bytes, range(n), chunksize=6):
                    ff.stdin.write(fr)
        else:
            for i in range(n):
                ff.stdin.write(_frame_bytes(i))
    finally:
        _STATE = None
        ff.stdin.close()
        if ff.wait() != 0:
            raise RuntimeError("ffmpeg failed while writing the video")
    return out, tl


_STATE = None  # shared with forked frame workers


def _frame_bytes(i: int) -> bytes:
    st = _STATE
    plan, w, h, tl, scale = st["plan"], st["w"], st["h"], st["tl"], st["scale"]
    t = i / FPS
    if t >= tl["shots_end"]:
        return st["card"]
    spans = tl["spans"]
    k = max([j for j, s in enumerate(spans) if t >= s["start"]] or [0])
    span, line = spans[k], plan.lines[k]
    start = span["start"] if k else 0.0
    p = min(1.0, max(0.0, (t - start) / (span["end"] - start)))
    ax, ay, ar = motion.SHAKE[line.move.shake]
    jx, jy, jr = st["jitter"]
    mv = line.move
    fr = motion.frame(st["stills"][st["files"][line.number]], w, h, p, mv.zoom_from, mv.zoom_to,
                      mv.slide_x, mv.slide_y, jx[i] * ax, jy[i] * ay, jr[i] * ar)
    d = ImageDraw.Draw(fr)
    if line.label:
        f_lab = st["f_lab"]
        x0, y0 = int(60 * scale), int(150 * scale)
        pad = int(25 * scale)
        d.rounded_rectangle([x0, y0, x0 + d.textlength(line.label, font=f_lab) + 2 * pad,
                             y0 + int(90 * scale)], int(18 * scale), fill=NAVY)
        d.text((x0 + pad, y0 + int(10 * scale)), line.label, font=f_lab,
               fill=ACCENT if "AFTER" in line.label.upper() else "white")
    if span["start"] <= t <= span["sub_end"]:  # Greek subtitle above the bottom 20 % safe area
        rows, font = st["subs"][line.number]
        step = int(font.size * 1.28)
        y = int(h * 0.74) - len(rows) * int(font.size * 1.24)
        for row in rows:
            text_center(d, w, y, row, font, "white")
            y += step
    return fr.tobytes()
