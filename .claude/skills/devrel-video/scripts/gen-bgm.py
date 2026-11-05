#!/usr/bin/env python3
# Local synth music bed — license-clean, no model/auth. Warm engine: windowed-sinc lowpass + FFT reverb +
# FM/Rhodes keys + soft drums. Six styles; pick with a 3rd arg or BGM_STYLE env (default: corporate).
#   gen-bgm.py <out.wav> [duration_s] [style]   style: ambient|lofi|uplift|minimal|corporate|focus
# Swap for a produced track via a MusicGen/HeyGen render through the same <audio id="bgm"> seam.
import numpy as np, wave, sys, os

SR = 44100
DUR = float(sys.argv[2]) if len(sys.argv) > 2 else 25.7
STYLE = sys.argv[3] if len(sys.argv) > 3 else os.environ.get("BGM_STYLE", "corporate")

def hz(m): return 440.0 * 2 ** ((m - 69) / 12)

def fftconv(x, h):
    n = len(x) + len(h) - 1
    nf = 1 << (n - 1).bit_length()
    return np.fft.irfft(np.fft.rfft(x, nf) * np.fft.rfft(h, nf), nf)[:n]

def lowpass(x, fc, taps=161):
    fc = min(fc, SR / 2 * 0.95)
    m = (taps - 1) // 2
    k = np.arange(taps) - m
    h = np.sinc(2 * fc / SR * k) * np.hanning(taps); h /= h.sum()
    return fftconv(x, h)[m:m + len(x)]

def adsr(n, a, d, s, r):
    e = np.full(n, s, float)
    ai, di, ri = int(a * SR), int(d * SR), int(r * SR)
    if ai > 0: e[:ai] = np.linspace(0, 1, ai)
    if di > 0: e[ai:ai + di] = np.linspace(1, s, di)
    if 0 < ri < n: e[-ri:] = e[-ri:] * np.linspace(1, 0, ri)
    return e

def pad_osc(f, n):
    t = np.arange(n) / SR
    vib = 1 + 0.003 * np.sin(2 * np.pi * 5 * t)
    y = (np.sin(2 * np.pi * f * vib * t) + np.sin(2 * np.pi * f * 1.004 * t) + np.sin(2 * np.pi * f * 0.996 * t)) / 3
    return y + 0.10 * np.sin(2 * np.pi * 3 * f * t)

def fm(f, n, ratio=1.0, index=2.2, decay=0.9):
    t = np.arange(n) / SR
    env = np.exp(-t / decay)
    return np.sin(2 * np.pi * f * t + np.sin(2 * np.pi * f * ratio * t) * index * env) * env

def bass_osc(f, n, decay=0.5):
    t = np.arange(n) / SR
    return np.tanh((np.sin(2 * np.pi * f * t) + 0.3 * np.sin(2 * np.pi * 2 * f * t)) * np.exp(-t / decay) * 1.3)

def kick():
    n = int(0.22 * SR); t = np.arange(n) / SR
    fsw = 95 * np.exp(-t / 0.035) + 45
    return np.sin(2 * np.pi * np.cumsum(fsw) / SR) * np.exp(-t / 0.16) * 0.9

def hat():
    n = int(0.045 * SR)
    y = np.random.default_rng(3).standard_normal(n) * np.exp(-np.arange(n) / SR / 0.016)
    return lowpass(y - np.concatenate([[0], y[:-1]]), 9000) * 0.9

def reverb(x, decay=1.3, wet=0.26, seed=1):
    L = int(SR * decay); tt = np.arange(L) / SR
    ir = np.random.default_rng(seed).standard_normal(L) * np.exp(-tt / (decay * 0.35))
    ir = lowpass(ir, 4200); ir /= np.abs(ir).max() + 1e-9
    w = fftconv(x, ir)[:len(x)]; w /= np.abs(w).max() + 1e-9
    return x * (1 - wet) + w * wet * (np.abs(x).max() + 1e-9)

def place(buf, start, sig):
    i0 = int(start * SR); i1 = min(len(buf), i0 + len(sig))
    if i0 < len(buf): buf[i0:i1] += sig[:i1 - i0]

def render(cfg):
    N = int(SR * DUR)
    beat = 60.0 / cfg["bpm"]; bar = 4 * beat
    chords = cfg["chords"]; el = cfg["el"]
    pad = np.zeros(N); keys = np.zeros(N); arp = np.zeros(N); bass = np.zeros(N); drum = np.zeros(N)
    for b in range(int(np.ceil(DUR / bar)) + 1):
        bm, voicing, arpm = chords[b % len(chords)]
        tb = b * bar
        if "pad" in el:
            ln = int(bar * SR); e = adsr(ln, 0.35, 0.2, 0.85, 0.6)
            ch = sum(pad_osc(hz(m), ln) for m in voicing)
            place(pad, tb, lowpass(ch / len(voicing), cfg.get("pad_lp", 2600)) * e)
        if "keys" in el:
            for sub in (0, 2):
                ln = int(1.6 * beat * SR)
                ch = sum(fm(hz(m), ln, cfg.get("keys_ratio", 1.0), cfg.get("keys_idx", 1.6), 1.1) for m in voicing)
                place(keys, tb + sub * beat, ch / len(voicing) * 0.6)
        if "arp" in el and tb >= 0.8:
            for e8 in range(8):
                m = arpm[e8 % len(arpm)] + (12 if e8 % 4 >= 2 else 0)
                place(arp, tb + e8 * 0.5 * beat, fm(hz(m), int(0.5 * beat * SR), 2.0, 1.2, 0.22) * 0.4)
        if "bass" in el:
            per = cfg.get("bass_per", 1)
            for k in range(per):
                place(bass, tb + k * (bar / per), bass_osc(hz(bm), int((bar / per) * SR), cfg.get("bass_dec", 0.6)) * 0.8)
    if "kick" in el:
        kk = kick(); t0 = 1.5
        while t0 < DUR - 1.5: place(drum, t0, kk); t0 += beat
    if "hat" in el:
        hh = hat() * 0.25; t0 = 1.5 + beat / 2
        while t0 < DUR - 1.5: place(drum, t0, hh); t0 += beat

    mix = (pad * cfg.get("g_pad", 0.9) + keys * cfg.get("g_keys", 0.9) + arp * cfg.get("g_arp", 0.7)
           + bass * cfg.get("g_bass", 1.0) + drum * cfg.get("g_drum", 0.9))
    mix = lowpass(mix, cfg.get("bus_lp", 7000))
    mix = reverb(mix, cfg.get("rv_dec", 1.3), cfg.get("rv_wet", 0.26))
    mix = np.tanh(mix * 1.05)
    t = np.arange(N) / SR
    g = np.ones(N); g[t < 3.0] = 0.65                       # duck the intro (under the title card)
    fi, fo = int(0.5 * SR), int(2.0 * SR)
    g[:fi] *= np.linspace(0, 1, fi); g[-fo:] *= np.linspace(1, 0, fo) ** 1.4
    mix *= g; mix /= np.abs(mix).max() + 1e-9
    Lr = reverb(mix, cfg.get("rv_dec", 1.3), 0.10, 5); Rr = reverb(mix, cfg.get("rv_dec", 1.3), 0.10, 9)
    st = np.stack([mix * 0.9 + Lr * 0.1, mix * 0.9 + Rr * 0.1], axis=1)
    st *= 10 ** (-1.5 / 20) / (np.abs(st).max() + 1e-9)
    return (st * 32767).astype('<i2')

# chord = (bass midi, [voicing], [arp])
Dmaj = [(50, [66, 69, 74], [62, 66, 69, 74]), (54, [66, 69, 73], [61, 66, 69, 73]),
        (55, [67, 71, 74], [62, 67, 71, 74]), (57, [64, 69, 73], [64, 69, 73, 76])]
Fadd = [(41, [60, 65, 69], [60, 65, 69, 72]), (43, [60, 64, 67], [55, 60, 64, 67]),
        (45, [60, 64, 69], [57, 60, 64, 69]), (48, [60, 64, 67], [60, 64, 67, 72])]
Amin = [(45, [60, 64, 69], [57, 60, 64, 69]), (41, [60, 65, 69], [53, 60, 65, 69]),
        (48, [60, 64, 67], [55, 60, 64, 67]), (43, [62, 67, 71], [55, 62, 67, 71])]

STYLES = {
    "ambient":   dict(bpm=68,  chords=Fadd, el={"pad", "keys", "bass"}, bass_per=1, bass_dec=1.4,
                      pad_lp=2000, bus_lp=5200, rv_dec=2.0, rv_wet=0.4, keys_idx=1.2, g_keys=0.7),
    "lofi":      dict(bpm=82,  chords=Amin, el={"pad", "keys", "bass", "kick", "hat"}, bass_per=2, bass_dec=0.7,
                      pad_lp=1700, bus_lp=4200, rv_dec=1.2, rv_wet=0.3, keys_idx=1.8, g_keys=0.85, g_drum=0.7),
    "uplift":    dict(bpm=110, chords=Dmaj, el={"pad", "arp", "bass", "kick", "hat"}, bass_per=4, bass_dec=0.5,
                      pad_lp=2800, bus_lp=7500, rv_dec=1.1, rv_wet=0.22, g_arp=0.6),
    "minimal":   dict(bpm=92,  chords=Fadd, el={"pad", "keys"}, bass_per=1,
                      pad_lp=2200, bus_lp=6000, rv_dec=1.8, rv_wet=0.36, keys_ratio=1.0, keys_idx=1.4, g_keys=0.9, g_pad=0.6),
    "corporate": dict(bpm=116, chords=Dmaj, el={"pad", "keys", "arp", "bass", "kick", "hat"}, bass_per=4, bass_dec=0.45,
                      pad_lp=3000, bus_lp=8000, rv_dec=1.0, rv_wet=0.2, keys_idx=1.4, g_arp=0.5, g_keys=0.55),
    "focus":     dict(bpm=100, chords=Amin, el={"pad", "bass", "hat"}, bass_per=4, bass_dec=0.4,
                      pad_lp=1900, bus_lp=5000, rv_dec=1.6, rv_wet=0.3, g_pad=1.0, g_bass=1.0, g_drum=0.5),
}

cfg = STYLES.get(STYLE, STYLES["corporate"])
pcm = render(cfg)
out = sys.argv[1] if len(sys.argv) > 1 else "bgm.wav"
with wave.open(out, 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print(f"wrote {DUR:.1f}s stereo bed (style={STYLE}, {cfg['bpm']:.0f} BPM)")
