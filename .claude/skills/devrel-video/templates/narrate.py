#!/usr/bin/env python3
# TEMPLATE — copy to projects/<slug>/ and adapt: FOOT_DUR (ffprobe capture.mp4), the beat caps
# (FILTER_CAP/INSPECT_CAP = capture-time of each transition, from your hero script's pacing), and the
# EN/ES line texts. Expects vo1..vo5.wav from scripts/tts.sh in the cwd.
# Build the narration voice track + re-timed captions from the measured TTS line durations.
# The VOICE drives the timeline: scene/chapter times come from real line lengths, not guesses.
# Prints the composition timing map (plug into index.html); writes voice.wav + captions.<lang>.srt.
import sys, wave, json
import numpy as np

SR = 48000
FOOT_DUR = 20.28          # measured capture length
FILTER_CAP, INSPECT_CAP = 7.7, 14.0   # capture-time of the filter click / item open (from your capture.js pacing)
LEAD, TAIL = 0.4, 0.4

# Spoken narration lines (the TTS source) — ONE per beat, clean text (no parens/version #s; em-dash -> comma).
# Keep in sync with the EN captions below. `python narrate.py --lines` prints them (scripts/variant.sh TTS's them).
SPOKEN = [
    "Acme. The fastest way to ship your product.",
    "Browse everything in one place. Clean, fast, and built for teams.",
    "Filter to find exactly what you need in seconds.",
    "Open any item to see the detail, the price, and how to get started.",
    "Start building at acme.com.",
]
if "--lines" in sys.argv:            # print the spoken lines (for the variant helper to TTS), then exit
    print("\n".join(SPOKEN)); raise SystemExit

def load(path):
    with wave.open(path, 'rb') as w:
        sr, ch, n = w.getframerate(), w.getnchannels(), w.getnframes()
        d = np.frombuffer(w.readframes(n), dtype='<i2').astype(np.float32) / 32768.0
    if ch == 2:
        d = d.reshape(-1, 2).mean(axis=1)
    if sr != SR:                      # linear resample to 48k
        d = np.interp(np.arange(int(len(d) * SR / sr)) / SR, np.arange(len(d)) / sr, d)
    return d

vos = [load(f"vo{i}.wav") for i in range(1, 6)]
dur = [len(v) / SR for v in vos]

title_dur = LEAD + dur[0] + TAIL
fs = title_dur                                   # footage start
p1 = LEAD
p2 = fs + 0.3
p3 = max(p2 + dur[1] + 0.2, fs + FILTER_CAP)
p4 = max(p3 + dur[2] + 0.2, fs + INSPECT_CAP)
foot_end = fs + FOOT_DUR
cta_start = foot_end
p5 = cta_start + 0.2
cta_dur = 0.2 + dur[4] + 0.5
total = cta_start + cta_dur
starts = [p1, p2, p3, p4, p5]

# voice track (stereo, silence with each line placed at its start)
N = int(total * SR)
voice = np.zeros(N)
for v, p in zip(vos, starts):
    i0 = int(p * SR); i1 = min(N, i0 + len(v)); voice[i0:i1] += v[:i1 - i0]
st = np.clip(np.stack([voice, voice], axis=1), -1, 1)
with wave.open('voice.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((st * 32767).astype('<i2').tobytes())

# captions re-timed to the narration (what the voice actually says)
def ts(x):
    ms = int(round(x * 1000))
    return f"{ms//3600000:02d}:{ms%3600000//60000:02d}:{ms%60000//1000:02d},{ms%1000:03d}"
EN = ["Acme — the fastest way\nto ship your product.",
      "Browse everything in one place —\nclean, fast, built for teams.",
      "Filter to find exactly\nwhat you need in seconds.",
      "Open any item for the detail,\nthe price, and how to start.",
      "Start building at acme.com."]
ES = ["Acme: la forma más rápida\nde lanzar tu producto.",
      "Explóralo todo en un solo lugar:\nrápido y hecho para equipos.",
      "Filtra para encontrar justo\nlo que necesitas en segundos.",
      "Abre cualquier elemento para ver el detalle,\nel precio y cómo empezar.",
      "Empieza a construir en acme.com."]
for lang, txt in (('en', EN), ('es', ES)):
    out = [f"{i}\n{ts(s)} --> {ts(s + d)}\n{t}\n" for i, (s, d, t) in enumerate(zip(starts, dur, txt), 1)]
    open(f"captions.{lang}.srt", 'w').write("\n".join(out))

timing = {
    "total": round(total, 2), "title_dur": round(title_dur, 2), "footage_start": round(fs, 2),
    "footage_dur": FOOT_DUR, "cta_start": round(cta_start, 2), "cta_dur": round(cta_dur, 2),
    "vo_starts": [round(x, 2) for x in starts],
    "line_durs": [round(d, 2) for d in dur],          # avatar bubble lengths = line_durs[0] (intro) / [4] (cta)
    "ch1": [round(p2, 2), round(fs + FILTER_CAP, 2)],
    "ch2": [round(fs + FILTER_CAP + 0.2, 2), round(fs + INSPECT_CAP, 2)],
    "ch3": [round(fs + INSPECT_CAP + 0.2, 2), round(foot_end, 2)],
}
json.dump(timing, open("timing.json", "w"), indent=2)   # scripts/retime.py applies this to index.html
print(json.dumps(timing, indent=2))
