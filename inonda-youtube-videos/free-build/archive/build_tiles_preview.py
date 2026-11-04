#!/usr/bin/env python3
"""PREVIEW of the 30 s tile reel "old tiles vs new smooth tiles" (owner request 2026-10-29).

Free and local only: drawn tile scenes (PIL), Kokoro am_michael voice (speed 0.90), Greek subtitles
burned in, silent bilingual end card. No prices, no budgets. This is an animatic for the owner to
approve the script, pacing and look; real job photos or approved footage replace the drawn scenes.
Usage: python3 build_tiles_preview.py OUT_DIR   (needs: pip install kokoro-onnx soundfile pillow;
model files kokoro-v1.0.onnx + voices-v1.0.bin in ~/.cache/kokoro)
"""
import math, os, random, subprocess, sys

import numpy as np
import soundfile
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS = 1080, 1920, 30
GAP, END_SECS = 0.35, 6.0
NAVY, ACCENT = (22, 35, 43), (79, 195, 247)
FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
KOKORO_DIR = os.path.expanduser("~/.cache/kokoro")

# (scene, spoken English, Greek subtitle, on-screen label)
LINES = [
    ("old", "Cracked, tired floor tiles?", "Σπασμένα, κουρασμένα πλακάκια δαπέδου;", "BEFORE · ΠΡΙΝ"),
    ("old", "Old floors trap dirt and look worn.", "Τα παλιά δάπεδα κρατούν βρωμιά και δείχνουν φθαρμένα.", "BEFORE · ΠΡΙΝ"),
    ("remove", "We remove them cleanly.", "Τα αφαιρούμε καθαρά.", ""),
    ("lay", "Then we lay new tiles, perfectly level,", "Μετά στρώνουμε νέα πλακάκια, απόλυτα αλφαδιασμένα,", ""),
    ("new", "with a smooth, easy-to-clean finish.", "με λείο φινίρισμα που καθαρίζει εύκολα.", "AFTER · ΜΕΤΑ"),
    ("new", "Feel the difference.", "Νιώστε τη διαφορά.", "AFTER · ΜΕΤΑ"),
]


def voice(out):
    from kokoro_onnx import Kokoro
    k = Kokoro(f"{KOKORO_DIR}/kokoro-v1.0.onnx", f"{KOKORO_DIR}/voices-v1.0.bin")
    clips, sr = [], 24000
    for _, en, _, _ in LINES:
        s, sr = k.create(en, voice="am_michael", speed=0.90, lang="en-us")
        clips.append(np.concatenate([s, np.zeros(int(GAP * sr), dtype=s.dtype)]))
    lead = np.zeros(int(0.4 * sr), dtype=clips[0].dtype)
    audio = np.concatenate([lead] + clips + [np.zeros(int(END_SECS * sr), dtype=clips[0].dtype)])
    soundfile.write(out, audio, sr)
    starts, t = [], 0.4
    for c in clips:
        starts.append((t, t + len(c) / sr - GAP)); t += len(c) / sr
    return starts, t, len(audio) / sr


# ---------- drawn floors (oversized so we can pan / zoom) ----------
def old_floor(rng):
    S, T = 1700, 260
    im = Image.new("RGB", (S, S), (120, 110, 95))
    d = ImageDraw.Draw(im)
    for y in range(0, S, T):
        for x in range(0, S, T):
            base = (198 + rng.randint(-14, 8), 182 + rng.randint(-14, 8), 150 + rng.randint(-16, 6))
            d.rectangle([x + 7, y + 7, x + T - 7, y + T - 7], fill=base)
            for _ in range(rng.randint(2, 6)):  # stains
                cx, cy, r = x + rng.randint(30, T - 30), y + rng.randint(30, T - 30), rng.randint(12, 45)
                d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(base[0] - 35, base[1] - 38, base[2] - 40))
            if rng.random() < 0.55:  # cracks
                px, py = x + rng.randint(10, T - 10), y + 8
                for _ in range(rng.randint(5, 9)):
                    nx, ny = px + rng.randint(-40, 40), py + rng.randint(20, 45)
                    d.line([px, py, nx, ny], fill=(70, 62, 52), width=rng.randint(2, 4)); px, py = nx, ny
            if rng.random() < 0.15:  # chipped corner
                d.polygon([(x + T - 7, y + 7), (x + T - 70, y + 7), (x + T - 7, y + 60)], fill=(110, 102, 88))
    return im.filter(ImageFilter.GaussianBlur(1.1))


def new_floor():
    S, T = 1700, 420
    im = Image.new("RGB", (S, S), (168, 172, 176))
    d = ImageDraw.Draw(im)
    for y in range(0, S, T):
        for x in range(0, S, T):
            g = 222 + ((x // T + y // T) % 2) * 4
            d.rectangle([x + 2, y + 2, x + T - 2, y + T - 2], fill=(g, g + 2, g + 4))
    return im.filter(ImageFilter.GaussianBlur(0.6))


def screed():
    rng = np.random.default_rng(3)
    a = rng.normal(150, 9, (1700, 1700, 1)).clip(0, 255)
    return Image.fromarray(np.concatenate([a, a * 0.97, a * 0.92], axis=2).astype("uint8")).filter(ImageFilter.GaussianBlur(1.5))


def view(src, p, zoom0=1.0, zoom1=1.12, dx=0.0):
    """Slow handheld-style push-in / slide across an oversized image."""
    z = zoom0 + (zoom1 - zoom0) * p
    cw, ch = int(W / z / 1.0 * 1.4), int(H / z / 1.0 * 1.4)
    cw, ch = min(cw, src.width), min(ch, src.height)
    cx = src.width / 2 + dx * p * 300 + math.sin(p * 9) * 6
    cy = src.height / 2 + math.cos(p * 7) * 5
    box = (int(cx - cw / 2), int(cy - ch / 2), int(cx + cw / 2), int(cy + ch / 2))
    return src.crop(box).resize((W, H), Image.BILINEAR)


def sheen(im, p):
    """Moving window reflection over a polished floor."""
    a = np.asarray(im).astype("float32")
    xs = np.linspace(0, 1, W)[None, :]
    ys = np.linspace(0, 1, H)[:, None]
    band = np.exp(-((xs * 0.9 + ys * 0.45 - (p * 1.6 - 0.2)) ** 2) / 0.006)
    glow = np.exp(-((xs - 0.75) ** 2 + (ys - 0.15) ** 2) / 0.08) * 0.25
    a = a + (band * 70 + glow * 60)[..., None]
    return Image.fromarray(a.clip(0, 255).astype("uint8"))


def text_center(d, y, s, font, fill, stroke=4):
    w = d.textlength(s, font=font)
    d.text(((W - w) / 2, y), s, font=font, fill=fill, stroke_width=stroke, stroke_fill=(0, 0, 0))


def wrap(d, s, font, maxw):
    words, lines, cur = s.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) > maxw and cur:
            lines.append(cur); cur = w
        else:
            cur = t
    return lines + [cur]


def end_card():
    im = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(im)
    rows = [("Inonda Ltd", 84, "white", FONT_B), ("Repairs · Renovations · Maintenance · Cyprus", 32, "white", FONT_R),
            ("Επισκευές · Ανακαινίσεις · Συντήρηση · Κύπρος", 32, "white", FONT_R), ("", 30, "white", FONT_R),
            ("CONTACT US TODAY", 62, ACCENT, FONT_B), ("ΕΠΙΚΟΙΝΩΝΗΣΤΕ ΜΑΖΙ ΜΑΣ", 48, ACCENT, FONT_B),
            ("Free inspection and written quote", 34, "white", FONT_R),
            ("Δωρεάν αυτοψία και γραπτή προσφορά", 34, "white", FONT_R), ("", 20, "white", FONT_R),
            ("+357 94 091 616", 60, "white", FONT_B), ("+357 94 091 613", 60, "white", FONT_B),
            ("WhatsApp · Viber · Call / Κλήση", 36, "white", FONT_R), ("inonda2026@outlook.com", 40, "white", FONT_R),
            ("", 30, "white", FONT_R), ("FOLLOW US", 62, ACCENT, FONT_B), ("ΑΚΟΛΟΥΘΗΣΤΕ ΜΑΣ", 48, ACCENT, FONT_B),
            ("Facebook: inondalimited   Instagram: @inondaltd", 32, "white", FONT_R),
            ("TikTok: @inonda26   YouTube: @InondaLTD", 32, "white", FONT_R),
            ("inonda.site  |  inonda.org  |  inonda.homes", 32, "white", FONT_R)]
    y = 230
    for s, sz, c, f in rows:
        if s:
            text_center(d, y, s, ImageFont.truetype(f, sz), c, 0)
        y += int(sz * 1.45)
    return im


def main(out_dir):
    os.makedirs(out_dir, exist_ok=True)
    wav = os.path.join(out_dir, "voice.wav")
    times, voice_end, total = voice(wav)
    rng = random.Random(7)
    OLD, NEW, BARE = old_floor(rng), new_floor(), screed()
    card = end_card()
    f_sub = ImageFont.truetype(FONT_B, 50)
    f_lab = ImageFont.truetype(FONT_B, 54)
    f_pre = ImageFont.truetype(FONT_B, 26)
    n = int(round(total * FPS))
    out = os.path.join(out_dir, "Inonda_Tiles_OldVsNew_PREVIEW.mp4")
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                           "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", wav, "-c:v", "libx264",
                           "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac",
                           "-b:a", "160k", "-shortest", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    for i in range(n):
        t = i / FPS
        if t >= voice_end:
            fr = card.copy()
        else:
            k = 0
            for j, (a, b) in enumerate(times):
                if t >= a - GAP:
                    k = j
            scene, en, gr, label = LINES[k]
            a = times[k][0]
            b = times[k + 1][0] if k + 1 < len(times) else voice_end
            p = min(1, max(0, (t - a) / max(0.1, b - a)))
            if scene == "old":
                fr = view(OLD, p if k == 0 else 0.5 + p / 2, 1.0, 1.15, 0.6 if k == 1 else 0)
            elif scene == "remove":  # old tiles disappear one row at a time, bare screed shows
                fr = view(OLD, 1.0, 1.15, 1.15).copy()
                bare = view(BARE, 1.0, 1.15, 1.15)
                cut = int(H * min(1, p * 1.2))
                fr.paste(bare.crop((0, H - cut, W, H)), (0, H - cut))
            elif scene == "lay":  # new tiles appear row by row over the screed
                fr = view(BARE, 0.0, 1.15, 1.15).copy()
                tiles = view(NEW, 0.0, 1.05, 1.05)
                cut = int(H * min(1, p * 1.15))
                fr.paste(tiles.crop((0, H - cut, W, H)), (0, H - cut))
            else:
                fr = sheen(view(NEW, (p + (k - 4)) / 2, 1.05, 1.12, 0.8), (p + (k - 4)) / 2)
            d = ImageDraw.Draw(fr)
            if label:
                d.rounded_rectangle([60, 150, 60 + d.textlength(label, font=f_lab) + 50, 240], 18, fill=NAVY + (0,))
                d.text((85, 160), label, font=f_lab, fill=ACCENT if "AFTER" in label else "white")
            if times[k][0] <= t <= times[k][1] + 0.25:  # Greek subtitle (safe area: above bottom 20 %)
                lines = wrap(d, gr, f_sub, W - 140)
                y = int(H * 0.74) - len(lines) * 62
                for ln in lines:
                    text_center(d, y, ln, f_sub, "white"); y += 64
            d.text((W - 190, 60), "PREVIEW", font=f_pre, fill=(255, 255, 255))
        ff.stdin.write(fr.tobytes())
    ff.stdin.close(); ff.wait()
    print("wrote", out, f"{total:.1f}s")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "out")
