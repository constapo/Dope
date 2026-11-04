#!/usr/bin/env python3
"""90 s tile reel "old tiles vs new black marble-look tiles" from free photo-realistic stills.

Owner rules (2026-10-29): real-looking footage only (no drawings), camera always handheld at chest
height and level, free sources only, no prices or budgets. The stills come from the free AI Horde
network (anonymous), and each one gets a slow handheld-phone camera move with natural hand shake.
Voice: Kokoro am_michael (speed 0.90); Greek subtitles; silent bilingual end card.

Usage: python3 build_tiles_photo.py STILLS_DIR OUT_DIR
STILLS_DIR holds one image per still name used in LINES (.webp/.png/.jpg).
"""
import glob, os, subprocess, sys

import numpy as np
import soundfile
from PIL import Image, ImageDraw, ImageFont

from build_tiles_preview import (ACCENT, END_SECS, FONT_B, FPS, H, KOKORO_DIR, NAVY, W, end_card,
                                 text_center, wrap)

SHOTS_SECS = 84.0  # picture part; the end card adds END_SECS -> 90 s (owner, 2026-10-29)
OVERSIZE = 1.18    # room for the camera to move without showing edges

# (still, spoken English, Greek subtitle, on-screen label, camera move: zoom from, zoom to, slide x, slide y)
LINES = [
    ("old1", "Cracked, tired floor tiles?", "Σπασμένα, κουρασμένα πλακάκια δαπέδου;", "BEFORE · ΠΡΙΝ", 1.00, 1.10, 0.0, 0.0),
    ("old2", "Old floors trap dirt and look worn.", "Τα παλιά δάπεδα κρατούν βρωμιά και δείχνουν φθαρμένα.", "BEFORE · ΠΡΙΝ", 1.04, 1.04, -0.6, 0.0),
    ("old3", "Cracks let water and dirt get under the tiles.", "Οι ρωγμές αφήνουν νερό και βρωμιά να μπαίνουν κάτω από τα πλακάκια.", "BEFORE · ΠΡΙΝ", 1.00, 1.08, 0.3, 0.2),
    ("measure", "First, we check the room and measure everything.", "Πρώτα ελέγχουμε τον χώρο και μετράμε τα πάντα.", "", 1.06, 1.00, 0.0, 0.0),
    ("protect", "We protect doors and furniture from dust.", "Προστατεύουμε πόρτες και έπιπλα από τη σκόνη.", "", 1.03, 1.03, 0.6, 0.0),
    ("work1", "Then we remove the old tiles cleanly.", "Μετά αφαιρούμε τα παλιά πλακάκια καθαρά.", "", 1.00, 1.08, 0.0, 0.2),
    ("debris", "All the rubble is bagged and taken away.", "Όλα τα μπάζα μπαίνουν σε σάκους και απομακρύνονται.", "", 1.04, 1.04, -0.5, 0.0),
    ("screed", "We make sure the base is flat and level.", "Βεβαιωνόμαστε ότι η βάση είναι επίπεδη και αλφαδιασμένη.", "", 1.00, 1.07, 0.0, 0.3),
    ("water1", "Next, the whole floor gets a waterproofing membrane.", "Μετά όλο το δάπεδο παίρνει στεγανωτική μεμβράνη.", "", 1.00, 1.07, 0.4, 0.0),
    ("water2", "Corners and joints are sealed with reinforcing tape.", "Γωνίες και αρμοί σφραγίζονται με ενισχυτική ταινία.", "", 1.05, 1.00, 0.0, 0.2),
    ("adhesive", "Adhesive goes on evenly with a notched trowel.", "Η κόλλα απλώνεται ομοιόμορφα με οδοντωτή σπάτουλα.", "", 1.05, 1.00, 0.3, 0.0),
    ("water3", "The tiles go down right over the waterproofing.", "Τα πλακάκια μπαίνουν ακριβώς πάνω από τη στεγάνωση.", "", 1.00, 1.06, -0.4, 0.0),
    ("work2", "Then we lay the new tiles,", "Μετά στρώνουμε τα νέα πλακάκια,", "", 1.00, 1.07, 0.0, 0.0),
    ("spacers", "with spacers and a level on every row.", "με σφηνάκια και αλφάδι σε κάθε σειρά.", "", 1.03, 1.03, -0.6, 0.0),
    ("grout", "Fine grout fills every joint.", "Λεπτός αρμόστοκος γεμίζει κάθε αρμό.", "", 1.00, 1.08, 0.2, 0.2),
    ("clean", "Then everything is cleaned and polished.", "Μετά όλα καθαρίζονται και γυαλίζονται.", "", 1.05, 1.00, 0.0, 0.0),
    ("after", "A smooth, easy-to-clean finish.", "Λείο φινίρισμα που καθαρίζει εύκολα.", "AFTER · ΜΕΤΑ", 1.03, 1.03, 0.7, 0.0),
    ("after3", "Black marble look, made to last.", "Όψη μαύρου μαρμάρου, φτιαγμένη να διαρκεί.", "AFTER · ΜΕΤΑ", 1.00, 1.08, -0.4, 0.0),
    ("after", "Feel the difference.", "Νιώστε τη διαφορά.", "AFTER · ΜΕΤΑ", 1.03, 1.12, 0.5, 0.3),
]


def voice(out):
    from kokoro_onnx import Kokoro
    k = Kokoro(f"{KOKORO_DIR}/kokoro-v1.0.onnx", f"{KOKORO_DIR}/voices-v1.0.bin")
    sr, speech = 24000, []
    for line in LINES:
        s, sr = k.create(line[1], voice="am_michael", speed=0.90, lang="en-us")
        speech.append(s)
    lead = 0.4
    spare = max(0.35 * len(speech), SHOTS_SECS - lead - sum(len(s) for s in speech) / sr)
    gap = spare / len(speech)
    parts, spans, t = [np.zeros(int(lead * sr), dtype=speech[0].dtype)], [], lead
    for s in speech:
        parts += [s, np.zeros(int(gap * sr), dtype=s.dtype)]
        spans.append((t, t + len(s) / sr, t + len(s) / sr + gap)); t += len(s) / sr + gap
    parts.append(np.zeros(int(END_SECS * sr), dtype=speech[0].dtype))
    audio = np.concatenate(parts)
    soundfile.write(out, audio, sr)
    return spans, t, len(audio) / sr


def load_still(d, name):
    path = sorted(glob.glob(os.path.join(d, name + ".*")))[0]
    im = Image.open(path).convert("RGB")
    s = max(W * OVERSIZE / im.width, H * OVERSIZE / im.height)
    return im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)


def shake(n, seed, amp):
    """Smooth random hand movement: low-pass filtered noise, in pixels."""
    rng = np.random.default_rng(seed)
    x = np.cumsum(rng.normal(0, 1, n + 60))
    x = np.convolve(x, np.ones(25) / 25, mode="same")[30:30 + n]
    x -= np.linspace(x[0], x[-1], n)  # no long drift: the camera move handles direction
    return x / (np.abs(x).max() + 1e-6) * amp


def frame(src, p, z0, z1, sx, sy, jx, jy, rot):
    z = z0 + (z1 - z0) * p
    cw, ch = W / z, H / z  # source is scaled so z=1 shows the frame 1:1 with OVERSIZE spare
    room_x, room_y = (src.width - cw) / 2, (src.height - ch) / 2
    cx = src.width / 2 + sx * (p - 0.5) * room_x * 0.9 + jx
    cy = src.height / 2 + sy * (p - 0.5) * room_y * 0.9 + jy
    cx = min(max(cx, cw / 2), src.width - cw / 2)
    cy = min(max(cy, ch / 2), src.height - ch / 2)
    box = (cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2)
    im = src.crop(tuple(round(v) for v in box)).resize((W, H), Image.BICUBIC)
    if abs(rot) > 0.01:  # tiny roll, cropped so no corners show
        im = im.rotate(rot, Image.BICUBIC).crop((14, 25, W - 14, H - 25)).resize((W, H), Image.BICUBIC)
    return im


def main(stills_dir, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    wav = os.path.join(out_dir, "voice.wav")
    spans, shots_end, total = voice(wav)
    stills = {n: load_still(stills_dir, n) for n in {line[0] for line in LINES}}
    card = end_card()
    f_sub, f_lab = ImageFont.truetype(FONT_B, 50), ImageFont.truetype(FONT_B, 54)
    n = int(round(total * FPS))
    jx, jy, jr = shake(n, 1, 9), shake(n, 2, 7), shake(n, 3, 0.35)
    out = os.path.join(out_dir, "Inonda_Tiles_BlackMarble_90s_PREVIEW.mp4")
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                           "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", wav, "-c:v", "libx264",
                           "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p", "-c:a", "aac",
                           "-b:a", "160k", "-shortest", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    for i in range(n):
        t = i / FPS
        if t >= shots_end:
            ff.stdin.write(card.tobytes()); continue
        k = max(j for j, s in enumerate(spans) if t >= s[0] or j == 0)
        start = spans[k][0] if k else 0.0
        p = min(1.0, max(0.0, (t - start) / (spans[k][2] - start)))
        name, en, gr, label, z0, z1, sx, sy = LINES[k]
        fr = frame(stills[name], p, z0, z1, sx, sy, jx[i], jy[i], jr[i])
        d = ImageDraw.Draw(fr)
        if label:
            d.rounded_rectangle([60, 150, 60 + d.textlength(label, font=f_lab) + 50, 240], 18, fill=NAVY)
            d.text((85, 160), label, font=f_lab, fill=ACCENT if "AFTER" in label else "white")
        if spans[k][0] <= t <= spans[k][1] + 0.3:  # Greek subtitle above the bottom 20 % safe area
            lines = wrap(d, gr, f_sub, W - 140)
            y = int(H * 0.74) - len(lines) * 62
            for ln in lines:
                text_center(d, y, ln, f_sub, "white"); y += 64
        ff.stdin.write(fr.tobytes())
    ff.stdin.close(); ff.wait()
    print("wrote", out, f"{total:.1f}s")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
