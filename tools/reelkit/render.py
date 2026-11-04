"""Timeline maths and rendering: pictures with handheld moves, labels, Greek subtitles, end card.

Each line is rendered to its own video segment, cached by everything that affects its pixels
(picture, move, label, subtitle, frame count). A one-line edit re-renders only that line; the
segments are then joined without re-encoding and the voice track is added (FR-011, SC-002).
Timings are whole frames, so changing one line's length never shifts another line's frames.
"""
from __future__ import annotations

import math
import multiprocessing
import os
import subprocess

import numpy as np
import soundfile
from PIL import ImageDraw, ImageFont

from . import cache, motion
from .endcard import ACCENT, FONT_B, NAVY, end_card, text_center, wrap

FPS = 30
LEAD = 0.4       # silence before the first line, seconds
GAP = 0.35       # pause after each line, seconds
SUB_TAIL = 0.3   # subtitle stays this long after the words end
MAX_SUB_LINES = 2
RENDER_VERSION = "2"  # bump to invalidate cached segments after a rendering change
X264 = ["-c:v", "libx264", "-preset", "fast", "-crf", "19", "-pix_fmt", "yuv420p", "-r", str(FPS)]


def _frames(seconds: float) -> int:
    return int(math.ceil(round(seconds * FPS, 6)))


def timeline(plan, clip_lengths: list[float]) -> dict:
    """Start/end of every line, when its subtitle shows, and the total length, in whole frames.

    Each line lasts its speech plus GAP, or min_seconds if longer (plan timings are minimums).
    The lead-in belongs to the first line's picture. Times are frame counts / FPS."""
    spans, f = [], _frames(LEAD)
    for line, length in zip(plan.lines, clip_lengths):
        n = _frames(max(length + GAP, line.min_seconds))
        sub = min(n, _frames(length + SUB_TAIL))
        spans.append({"line": line.number, "start": f / FPS, "speech_end": f / FPS + length,
                      "sub_end": (f + sub) / FPS, "end": (f + n) / FPS,
                      "start_f": f, "frames": n, "sub_frames": sub})
        f += n
    card = _frames(plan.end_card_seconds)
    return {"spans": spans, "shots_end": f / FPS, "total": (f + card) / FPS,
            "lead_f": _frames(LEAD), "card_frames": card}


def assemble_audio(plan, clip_paths: list[str], tl: dict, out: str) -> float:
    clips = [soundfile.read(p, dtype="float32") for p in clip_paths]
    sr = clips[0][1]
    audio = np.zeros(int(round(tl["total"] * sr)), dtype=np.float32)
    for (samples, csr), span in zip(clips, tl["spans"]):
        if csr != sr:
            raise ValueError("voice clips have different sample rates")
        if samples.ndim > 1:
            samples = samples.mean(axis=1)
        i = int(round(span["start"] * sr))
        audio[i:i + len(samples)] = samples[: max(0, len(audio) - i)]
    soundfile.write(out, audio, sr)
    return len(audio) / sr


def _subtitles(plan, w, scale, probe, warnings):
    subs, base = {}, max(20, int(50 * scale))
    for line in plan.lines:
        size = base
        while True:  # shrink the subtitle (down to 75 %) before giving up on two lines
            font = ImageFont.truetype(FONT_B, size)
            rows = wrap(probe, line.greek, font, w - int(140 * scale))
            if len(rows) <= MAX_SUB_LINES or size <= int(base * 0.75):
                break
            size -= 2
        if len(rows) > MAX_SUB_LINES:
            warnings.append(f"line {line.number}: Greek subtitle needs {len(rows)} lines on screen; shorten it")
        subs[line.number] = (rows, size)
    return subs


def _file_id(path: str) -> str:
    st = os.stat(path)
    return f"{os.path.abspath(path)}:{st.st_size}:{int(st.st_mtime)}"


def render(plan, build_dir: str, picture_files: dict, clip_paths: list[str], warnings: list, log=None):
    log = log if log is not None else []
    w, h = plan.size
    clip_lengths = [soundfile.info(p).duration for p in clip_paths]
    tl = timeline(plan, clip_lengths)
    wav = os.path.join(build_dir, "voice.wav")
    assemble_audio(plan, clip_paths, tl, wav)
    seg_dir = os.path.join(build_dir, "segments")
    os.makedirs(seg_dir, exist_ok=True)

    scale = w / 1080 if h > w else h / 1080
    card = end_card(w, h)
    subs = _subtitles(plan, w, scale, ImageDraw.Draw(card.copy()), warnings)

    # one segment per line (the first also covers the lead-in), then the end card
    segments = []
    for k, (line, span) in enumerate(zip(plan.lines, tl["spans"])):
        lead = tl["lead_f"] if k == 0 else 0
        mv = line.move
        key = cache.key("segment", RENDER_VERSION, w, h, _file_id(picture_files[line.number]),
                        [mv.zoom_from, mv.zoom_to, mv.slide_x, mv.slide_y, mv.shake], line.label,
                        subs[line.number], lead, span["frames"], span["sub_frames"], line.number)
        segments.append({"kind": "line", "k": k, "lead": lead, "frames": lead + span["frames"],
                         "path": os.path.join(seg_dir, f"{key}.mp4")})
    card_key = cache.key("card", RENDER_VERSION, w, h, plan.end_card_variant, tl["card_frames"])
    segments.append({"kind": "card", "frames": tl["card_frames"], "path": os.path.join(seg_dir, f"{card_key}.mp4")})

    todo = [s for s in segments if not os.path.exists(s["path"])]
    for s in segments:
        what = f"line {plan.lines[s['k']].number}" if s["kind"] == "line" else "end card"
        log.append(f"segment {what}: {'rendered' if s in todo else 'cache hit'}")

    stills, cropped_warned = {}, set()
    for s in todo:
        if s["kind"] != "line":
            continue
        line = plan.lines[s["k"]]
        path = picture_files[line.number]
        if path not in stills:
            stills[path], cropped = motion.load_still(path, w, h)
            if cropped and line.number not in cropped_warned:
                cropped_warned.add(line.number)
    for line in plan.lines:  # report crops for every line, cached or not
        path = picture_files[line.number]
        if path not in stills:
            from PIL import Image
            with Image.open(path) as im:
                iw, ih = im.size
            s_ = max(w * motion.OVERSIZE / iw, h * motion.OVERSIZE / ih)
            if (w * motion.OVERSIZE * h * motion.OVERSIZE) / (iw * s_ * ih * s_) < 0.9:
                cropped_warned.add(line.number)
    for n in sorted(cropped_warned):
        warnings.append(f"line {n}: picture shape differs from the frame; centre-cropped")

    global _STATE
    _STATE = {"plan": plan, "w": w, "h": h, "tl": tl, "stills": stills, "files": picture_files, "subs": subs,
              "scale": scale, "f_lab": ImageFont.truetype(FONT_B, max(20, int(54 * scale))),
              "card": card.tobytes(), "segments": segments, "jitter": {}}
    for s in todo:
        if s["kind"] == "line":
            n = s["frames"]
            num = plan.lines[s["k"]].number
            _STATE["jitter"][s["k"]] = [motion.shake(n, 1000 * num + j, 1.0) for j in (1, 2, 3)]

    workers = max(1, min(8, (os.cpu_count() or 2) - 1))
    pool = None
    try:
        if todo and workers > 1 and "fork" in multiprocessing.get_all_start_methods():
            pool = multiprocessing.get_context("fork").Pool(workers)
        for s in todo:
            tmp = s["path"] + ".part.mp4"
            ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                                   "-s", f"{w}x{h}", "-r", str(FPS), "-i", "-", *X264, "-an", tmp],
                                  stdin=subprocess.PIPE)
            idx = segments.index(s)
            jobs = [(idx, i) for i in range(s["frames"])]
            frames = pool.imap(_frame_bytes, jobs, chunksize=6) if pool else map(_frame_bytes, jobs)
            try:
                for fr in frames:
                    ff.stdin.write(fr)
            finally:
                ff.stdin.close()
                if ff.wait() != 0:
                    raise RuntimeError("ffmpeg failed while writing a segment")
            os.replace(tmp, s["path"])
    finally:
        if pool:
            pool.close()
            pool.join()
        _STATE = None

    out = os.path.join(build_dir, f"{plan.slug}.mp4")
    lst = os.path.join(build_dir, "segments.txt")
    with open(lst, "w", encoding="utf-8") as f:
        f.writelines(f"file '{s['path']}'\n" for s in segments)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-i", wav,
                    "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "160k",
                    "-t", f"{tl['total']:.3f}", "-movflags", "+faststart", out], check=True)
    return out, tl


_STATE = None  # shared with forked frame workers


def _frame_bytes(job) -> bytes:
    seg_idx, i = job
    st = _STATE
    seg = st["segments"][seg_idx]
    if seg["kind"] == "card":
        return st["card"]
    plan, w, h, scale = st["plan"], st["w"], st["h"], st["scale"]
    k = seg["k"]
    line, span = plan.lines[k], st["tl"]["spans"][k]
    p = i / max(1, seg["frames"] - 1)
    ax, ay, ar = motion.SHAKE[line.move.shake]
    jx, jy, jr = st["jitter"][k]
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
    local = i - seg["lead"]
    if 0 <= local < span["sub_frames"]:  # Greek subtitle above the bottom 20 % safe area
        rows, size = st["subs"][line.number]
        font = ImageFont.truetype(FONT_B, size)
        step = int(size * 1.28)
        y = int(h * 0.74) - len(rows) * int(size * 1.24)
        for row in rows:
            text_center(d, w, y, row, font, "white")
            y += step
    return fr.tobytes()
