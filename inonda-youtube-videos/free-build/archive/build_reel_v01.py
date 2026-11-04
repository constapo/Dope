#!/usr/bin/env python3
"""90-second vertical reel/ad from Video 01, free tools only.
Voice: lines cut from the existing Emma narration (word timings from faster-whisper, run locally).
Pictures: Pollinations.ai (free, no account), 9:16, slow camera moves, 30 fps, 1080x1920.
Captions burned in; last ~11 s is an Inonda Ltd contact card (details from inonda.site/.org/.homes).
Usage: python3 build_reel_v01.py WORK_DIR  (WORK_DIR must contain v01_words.json; LOGO optional)."""
import json, os, subprocess, sys, time, urllib.parse, urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
AUDIO = os.path.join(ROOT, "..", "audio", "Inonda_Video01_narration_Emma.mp3")
WORK = sys.argv[1]
FPS, W, H = 30, 1080, 1920
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
STYLE = ("photorealistic phone photo, vertical, 35mm lens, natural daylight, real camera, realistic "
         "textures, older Cyprus apartment, no people, no faces, no text, no logos")

# narration lines kept for the ad: (start, end) seconds in the full narration
LINES = [(0.00, 6.30), (18.10, 29.40), (30.00, 41.00), (55.70, 60.40), (103.10, 110.60),
         (112.55, 118.30), (192.45, 207.30), (237.80, 242.40), (276.10, 286.80), (296.30, 306.30)]
# pictures in order, with their share of the timeline: (shot id, prompt, seconds)
SHOTS = [
 ("t01", "close-up of a cracked chipped beige 1990s ceramic wall tile beside a shower, grout stained dark", 2.2),
 ("t02", "bathroom ceiling corner with brown damp stain, peeling paint and black mould spots", 2.1),
 ("t03", "overhead view of an old shower tray with murky water around a corroded drain grate", 2.1),
 ("t06", "street of white-rendered apartment blocks in Cyprus in morning sun, solar water heaters on flat roofs", 5.6),
 ("t04", "renovated bathroom, light-grey large porcelain tiles, walk-in glass shower, floating vanity, warm LED mirror", 5.6),
 ("t05", "doorway view into an old dated bathroom with beige tiles and worn fittings", 11.0),
 ("t07", "moisture meter pressed against a stained bathroom wall", 4.7),
 ("t09", "bathroom being stripped, old wall tiles removed, rubble and dust in the light", 7.5),
 ("t08", "old galvanised pipes inside an opened bathroom wall cavity", 5.8),
 ("t11", "grey waterproof membrane freshly rolled on a shower floor", 7.5),
 ("t11b", "reinforcing waterproof tape pressed into a shower wall corner", 7.4),
 ("t13", "smooth white silicone sealant bead along a tiled shower corner", 4.6),
 ("t14", "new chrome tap running clear water over a white basin", 5.3),
 ("t16", "finished renovated bathroom with floating vanity and warm LED mirror, clean and bright", 5.4),
 ("t15", "bright renovated bathroom seen from the doorway, light-grey tiles, glass shower", 9.0),
]
CARD_SECS = 11.0  # contact card; voice keeps running under its first seconds
TOTAL = 90.0
# speech-to-text mishearings of the company name, fixed word by word: (heard words, shown text)
FIXES = [(["an", "under", "limited."], "Inonda Ltd."), (["In", "Onder"], "Inonda"), (["Outcome"], "Out come")]


def fix_words(chunk):
    out, i = [], 0
    while i < len(chunk):
        for heard, shown in FIXES:
            n = len(heard)
            if [w for _, _, w in chunk[i:i + n]] == heard:
                out.append((chunk[i][0], chunk[i + n - 1][1], shown)); i += n; break
        else:
            out.append(chunk[i]); i += 1
    return out


def run(*a):
    subprocess.run(a, check=True)


def fetch(prompt, seed, path):
    if os.path.exists(path) and os.path.getsize(path) > 20000:
        return
    q = urllib.parse.quote(f"{prompt}, {STYLE}")
    url = f"https://image.pollinations.ai/prompt/{q}?width=1080&height=1920&nologo=true&seed={seed}"
    time.sleep(20)  # free tier rate-limits fast callers with HTTP 402
    for attempt in range(8):
        try:
            data = urllib.request.urlopen(url, timeout=180).read()
            if len(data) > 20000:
                open(path, "wb").write(data); return
        except Exception as e:
            print("retry", path, e, flush=True)
        time.sleep(30 * (attempt + 1))
    raise SystemExit(f"could not fetch {path}")


def clip(img, out, secs, k):
    n = int(round(secs * FPS))
    zoom = f"1+0.10*on/{n}" if k % 2 == 0 else f"1.10-0.10*on/{n}"
    vf = (f"crop=iw:ih*0.95:0:0,scale={W*2}:{H*2}:force_original_aspect_ratio=increase,crop={W*2}:{H*2},"
          f"zoompan=z='{zoom}':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2':d={n}:s={W}x{H}:fps={FPS},"
          f"eq=saturation=0.92,noise=alls=4:allf=t,format=yuv420p")
    run("ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-i", img, "-vf", vf, "-frames:v", str(n),
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", out)


def ts(t):
    return f"{int(t//3600)}:{int(t%3600//60):02d}:{t%60:05.2f}"


def captions(words_json, out_ass):
    segs = json.load(open(words_json))
    words = [(s, e, w) for seg in segs for (s, e, w) in seg["w"]]
    lines, offset = [], 0.0
    for a, b in LINES:
        chunk = []
        for s, e, w in words:
            if s >= a - 0.05 and e <= b + 0.05:
                chunk.append((s - a + offset, e - a + offset, w.strip()))
        chunk = fix_words(chunk)
        for i in range(0, len(chunk), 4):  # 4 words per caption
            g = chunk[i:i + 4]
            if g[0][0] >= TOTAL - CARD_SECS:  # contact card shows the details itself
                continue
            txt = " ".join(x[2] for x in g)
            nxt = chunk[i + 4][0] if i + 4 < len(chunk) else g[-1][1] + 0.05
            lines.append(f"Dialogue: 0,{ts(g[0][0])},{ts(min(g[-1][1] + 0.05, nxt - 0.01))},Cap,,0,0,0,,{txt}")
        offset += b - a
    head = (f"[Script Info]\nScriptType: v4.00+\nPlayResX: {W}\nPlayResY: {H}\n\n[V4+ Styles]\n"
            "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, "
            "Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, "
            "Alignment, MarginL, MarginR, MarginV, Encoding\n"
            "Style: Cap,DejaVu Sans,74,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,1,0,0,0,100,100,0,0,1,6,2,2,80,80,520,1\n\n"
            "[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")
    open(out_ass, "w").write(head + "\n".join(lines) + "\n")
    return offset  # voice length


def contact_card(out, logo):
    lines = [
        ("Inonda Ltd", 86, 360), ("Repairs - Renovations - Maintenance", 44, 470), ("Cyprus", 44, 530),
        ("Book a free inspection", 56, 680),
        ("Irina, Director", 50, 800), ("+357 94 091 616", 64, 870),
        ("Constantin, Foreman", 50, 990), ("+357 94 091 613", 64, 1060),
        ("WhatsApp  -  Viber  -  Call", 42, 1150),
        ("inonda2026@outlook.com", 46, 1250),
        ("inonda.site  |  inonda.org  |  inonda.homes", 40, 1340),
        ("Facebook: inondalimited    Instagram: @inondaltd", 36, 1440),
        ("TikTok: @inonda26    YouTube: @InondaLTD", 36, 1500),
        ("29 Charalampou Mouskou, 2014 Strovolos, Nicosia", 32, 1600),
    ]
    dt = ",".join(
        f"drawtext=fontfile={FONT}:text='{t.replace(':', chr(92) + ':')}':fontsize={s}:fontcolor=white:x=(w-tw)/2:y={y}"
        f":alpha='min(1,max(0,(t-{0.15*i:.2f})/0.4))'" for i, (t, s, y) in enumerate(lines))
    inputs = ["-f", "lavfi", "-i", f"color=c=0x16232b:s={W}x{H}:r={FPS}:d={CARD_SECS}"]
    if logo and os.path.exists(logo):
        inputs += ["-loop", "1", "-i", logo]
        fc = f"[1:v]scale=300:-1[l];[0:v][l]overlay=(W-w)/2:70,{dt},format=yuv420p"
    else:
        fc = f"[0:v]{dt},format=yuv420p"
    run("ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", fc, "-t", str(CARD_SECS),
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", out)


def main():
    os.makedirs(f"{WORK}/rimg", exist_ok=True); os.makedirs(f"{WORK}/rclips", exist_ok=True)
    voice_len = captions(f"{WORK}/v01_words.json", f"{WORK}/reel.ass")
    # voice: the kept lines joined with 0.1 s gaps would add drift, so join them directly
    parts = "".join(f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.03,afade=t=out:st={b-a-0.05}:d=0.05[a{i}];"
                    for i, (a, b) in enumerate(LINES))
    run("ffmpeg", "-y", "-loglevel", "error", "-i", AUDIO, "-filter_complex",
        parts + "".join(f"[a{i}]" for i in range(len(LINES))) + f"concat=n={len(LINES)}:v=0:a=1,apad[o]",
        "-map", "[o]", "-t", str(TOTAL), "-c:a", "aac", "-b:a", "192k", f"{WORK}/reel_voice.m4a")
    pics = TOTAL - CARD_SECS
    scale = pics / sum(s for _, _, s in SHOTS)
    vids = []
    for k, (sid, prompt, secs) in enumerate(SHOTS):
        img = f"{WORK}/rimg/{sid}.jpg"
        fetch(prompt, 500 + k, img)
        out = f"{WORK}/rclips/{sid}.mp4"
        clip(img, out, secs * scale, k)
        vids.append(out); print("ok", sid, flush=True)
    card = f"{WORK}/rclips/card.mp4"
    contact_card(card, os.environ.get("LOGO"))
    vids.append(card)
    with open(f"{WORK}/reel_list.txt", "w") as f:
        f.writelines(f"file '{v}'\n" for v in vids)
    final = f"{WORK}/Inonda_Reel_bathroom_90s_9x16_30fps.mp4"
    ass = f"{WORK}/reel.ass".replace(":", r"\:")
    run("ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", f"{WORK}/reel_list.txt",
        "-i", f"{WORK}/reel_voice.m4a", "-vf", f"subtitles={ass},fps={FPS}", "-map", "0:v", "-map", "1:a",
        "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-c:a", "copy", "-t", str(TOTAL),
        "-movflags", "+faststart", final)
    print("DONE", final, "voice", round(voice_len, 1))


if __name__ == "__main__":
    main()
