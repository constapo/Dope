#!/usr/bin/env python3
"""Reel v01 with a free older-male voiceover ("George") and Greek subtitles.
Voice: Microsoft Edge neural TTS via edge-tts (free, no account), one clip per sentence so
each Greek subtitle lines up exactly with its sentence. Pictures/contact card come from
build_reel_v01.py (the stills it downloaded are reused).
Usage: python3 build_reel_v01_george.py WORK_DIR   (needs: pip install edge-tts)"""
import asyncio, os, ssl, subprocess, sys
import edge_tts, edge_tts.communicate
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_reel_v01 as base

# Owner's chosen voice (2026-10-15 session): free local Kokoro "am_michael". Edge voice kept as fallback.
ENGINE = os.environ.get("REEL_VOICE_ENGINE", "kokoro")
KOKORO_VOICE, KOKORO_SPEED = "am_michael", 0.90
KOKORO_DIR = os.path.expanduser("~/.cache/kokoro")  # kokoro-v1.0.onnx + voices-v1.0.bin (thewh1teagle/kokoro-onnx)
VOICE, RATE, PITCH = "en-GB-ThomasNeural", "-3%", "-14Hz"  # Edge fallback: lower pitch, an older man
GAP = 0.35  # pause between sentences, seconds
CA = "/root/.ccr/ca-bundle.crt"  # sandbox proxy CA; ignored where it does not exist

# (spoken English, Greek subtitle)
LINES = [
 ("This bathroom in Cyprus had cracked tiles, a damp ceiling and a shower that never drained properly.",
  "Αυτό το μπάνιο στην Κύπρο είχε σπασμένα πλακάκια, υγρασία στο ταβάνι και ντους που δεν άδειαζε σωστά."),
 ("Sound familiar?", "Σας φαίνεται γνώριμο;"),
 ("We are Inonda Limited.", "Είμαστε η Inonda Ltd."),
 ("We repair, renovate and maintain homes across Cyprus.",
  "Επισκευάζουμε, ανακαινίζουμε και συντηρούμε σπίτια σε όλη την Κύπρο."),
 ("Every job is led by a technician with up to twenty-two years of experience.",
  "Κάθε δουλειά την αναλαμβάνει τεχνικός με έως και 22 χρόνια εμπειρίας."),
 ("Step one is the survey, before any demolition. We check the walls for damp.",
  "Πρώτο βήμα η αυτοψία, πριν από κάθε κατεδάφιση. Ελέγχουμε τους τοίχους για υγρασία."),
 ("This is where surprises appear: hidden leaks and old repairs. That is normal.",
  "Εδώ εμφανίζονται οι εκπλήξεις: κρυφές διαρροές και παλιές επισκευές. Είναι φυσιολογικό."),
 ("A good contractor shows you photos straight away, not a surprise bill later.",
  "Ένας σωστός εργολάβος σας δείχνει αμέσως φωτογραφίες, όχι έναν απρόσμενο λογαριασμό αργότερα."),
 ("You never see the waterproofing once the tiles are on, and that is exactly why people skip it.",
  "Τη στεγανοποίηση δεν τη βλέπετε όταν μπουν τα πλακάκια, και γι' αυτό ακριβώς πολλοί την παραλείπουν."),
 ("When it fails, the water goes into the wall, or through to the neighbour below.",
  "Όταν αποτύχει, το νερό πάει μέσα στον τοίχο ή στον γείτονα από κάτω."),
 ("The tiles still look fine. The damage does not.", "Τα πλακάκια φαίνονται μια χαρά. Η ζημιά όχι."),
 ("It is the most expensive shortcut in any bathroom.", "Είναι η πιο ακριβή παράλειψη σε κάθε μπάνιο."),
 ("In the corners we use flexible sealant, not grout, because rigid grout will crack.",
  "Στις γωνίες βάζουμε ελαστική σιλικόνη, όχι αρμόστοκο, γιατί ο άκαμπτος αρμός ραγίζει."),
 ("We visit, listen to what you want, and give you a clear written quote before we begin.",
  "Ερχόμαστε, ακούμε τι θέλετε και σας δίνουμε σαφή γραπτή προσφορά πριν ξεκινήσουμε."),
 ("Bathroom, kitchen, damp wall or leaking terrace? We would love to hear from you.",
  "Μπάνιο, κουζίνα, τοίχος με υγρασία ή ταράτσα που στάζει; Θα χαρούμε να σας ακούσουμε."),
]


_kokoro = None


def say_kokoro(text, out):
    global _kokoro
    import soundfile
    from kokoro_onnx import Kokoro
    if _kokoro is None:
        _kokoro = Kokoro(f"{KOKORO_DIR}/kokoro-v1.0.onnx", f"{KOKORO_DIR}/voices-v1.0.bin")
    samples, sr = _kokoro.create(text, voice=KOKORO_VOICE, speed=KOKORO_SPEED, lang="en-us")
    soundfile.write(out, samples, sr)


async def say(text, out):
    if os.path.exists(CA):
        edge_tts.communicate._SSL_CTX = ssl.create_default_context(cafile=CA)
    await edge_tts.Communicate(text, VOICE, rate=RATE, pitch=PITCH).save(out)


def duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                         capture_output=True, text=True, check=True).stdout
    return float(out.strip())


def voice_track(work):
    """One mp3 per sentence -> one wav with GAP between; returns [(start, end, greek)]."""
    folder = f"{work}/voice_{ENGINE}"
    os.makedirs(folder, exist_ok=True)
    parts, cues, t = [], [], 0.4
    for i, (en, gr) in enumerate(LINES):
        mp3 = f"{folder}/{i:02d}." + ("wav" if ENGINE == "kokoro" else "mp3")
        if not os.path.exists(mp3):
            say_kokoro(en, mp3) if ENGINE == "kokoro" else asyncio.run(say(en, mp3))
        d = duration(mp3)
        cues.append((t, t + d, gr))
        parts.append((mp3, d))
        t += d + GAP
    inputs, chain = [], ""
    for i, (mp3, d) in enumerate(parts):
        inputs += ["-i", mp3]
        chain += f"[{i}:a]aresample=48000,apad=pad_dur={GAP}[a{i}];"
    chain += f"anullsrc=r=48000:cl=mono,atrim=0:0.4[lead];[lead]" + "".join(
        f"[a{i}]" for i in range(len(parts))) + f"concat=n={len(parts) + 1}:v=0:a=1,apad[o]"
    base.run("ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", chain, "-map", "[o]",
             "-t", str(base.TOTAL), "-c:a", "aac", "-b:a", "192k", f"{work}/reel_george.m4a")
    return cues, t


def greek_ass(cues, out):
    head = (f"[Script Info]\nScriptType: v4.00+\nPlayResX: {base.W}\nPlayResY: {base.H}\nWrapStyle: 0\n\n"
            "[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, "
            "BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, "
            "Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
            "Style: Gr,DejaVu Sans,60,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,1,0,0,0,100,100,0,0,1,5,2,2,70,70,460,161\n\n"
            "[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")
    card_start = base.TOTAL - base.CARD_SECS
    rows = [f"Dialogue: 0,{base.ts(s)},{base.ts(min(e + 0.25, card_start))},Gr,,0,0,0,,{g}"
            for s, e, g in cues if s < card_start]
    open(out, "w").write(head + "\n".join(rows) + "\n")


def cta_card(out, logo):
    """Silent bilingual (English/Greek) end card: on-screen call to contact us and follow us (no narration over it)."""
    accent = "0x4FC3F7"
    lines = [  # English line, then its Greek version
        ("Inonda Ltd", 80, 325, "white"),
        ("Repairs - Renovations - Maintenance - Cyprus", 34, 425, "white"),
        ("Επισκευές - Ανακαινίσεις - Συντήρηση - Κύπρος", 34, 470, "white"),
        ("CONTACT US TODAY", 60, 555, accent), ("ΕΠΙΚΟΙΝΩΝΗΣΤΕ ΜΑΖΙ ΜΑΣ", 48, 625, accent),
        ("Free inspection and written quote", 34, 695, "white"),
        ("Δωρεάν αυτοψία και γραπτή προσφορά", 34, 740, "white"),
        ("Irina, Director  ·  Ιρίνα, Διευθύντρια", 36, 815, "white"), ("+357 94 091 616", 60, 865, "white"),
        ("Constantin, Foreman  ·  Κωνσταντίν, Εργοδηγός", 34, 955, "white"), ("+357 94 091 613", 60, 1003, "white"),
        ("WhatsApp  -  Viber  -  Call / Κλήση", 36, 1090, "white"), ("inonda2026@outlook.com", 42, 1150, "white"),
        ("FOLLOW US", 60, 1245, accent), ("ΑΚΟΛΟΥΘΗΣΤΕ ΜΑΣ", 48, 1315, accent),
        ("Facebook: inondalimited", 42, 1390, "white"), ("Instagram: @inondaltd", 42, 1450, "white"),
        ("TikTok: @inonda26", 42, 1510, "white"), ("YouTube: @InondaLTD", 42, 1570, "white"),
        ("inonda.site  |  inonda.org  |  inonda.homes", 36, 1660, "white"),
        ("29 Charalampou Mouskou, 2014 Strovolos, Nicosia", 28, 1730, "white"),
        ("Χαραλάμπου Μούσκου 29, 2014 Στρόβολος, Λευκωσία", 28, 1770, "white"),
    ]
    dt = ",".join(
        f"drawtext=fontfile={base.FONT}:text='{t.replace(':', chr(92) + ':')}':fontsize={sz}:fontcolor={c}"
        f":x=(w-tw)/2:y={y}:alpha='min(1,max(0,(t-{0.10*i:.2f})/0.4))'" for i, (t, sz, y, c) in enumerate(lines))
    inputs = ["-f", "lavfi", "-i", f"color=c=0x16232b:s={base.W}x{base.H}:r={base.FPS}:d={base.CARD_SECS}"]
    if logo and os.path.exists(logo):
        inputs += ["-loop", "1", "-i", logo]
        fc = f"[1:v]scale=280:-1[l];[0:v][l]overlay=(W-w)/2:60,{dt},format=yuv420p"
    else:
        fc = f"[0:v]{dt},format=yuv420p"
    base.run("ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", fc, "-t", str(base.CARD_SECS),
             "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", out)


def main():
    work = sys.argv[1]
    cues, voice_end = voice_track(work)
    print("voice ends at", round(voice_end, 1), "s")
    greek_ass(cues, f"{work}/reel_gr.ass")
    card_start = base.TOTAL - base.CARD_SECS
    if voice_end > card_start:
        raise SystemExit(f"voice runs into the silent end card ({voice_end:.1f} s > {card_start:.1f} s)")
    # reuse the picture clips rendered by build_reel_v01.py; swap in the silent call-to-action card
    card = f"{work}/rclips/card_cta.mp4"
    cta_card(card, f"{work}/logo.png")
    clips = [l.strip()[6:-1] for l in open(f"{work}/reel_list.txt") if not l.strip().endswith("card.mp4'")]
    with open(f"{work}/reel_list_cta.txt", "w") as f:
        f.writelines(f"file '{c}'\n" for c in clips + [card])
    final = f"{work}/Inonda_Reel_bathroom_90s_Michael_GR.mp4"
    ass = f"{work}/reel_gr.ass".replace(":", r"\:")
    base.run("ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", f"{work}/reel_list_cta.txt",
             "-i", f"{work}/reel_george.m4a", "-vf", f"subtitles={ass},fps={base.FPS}", "-map", "0:v", "-map",
             "1:a", "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-c:a", "copy", "-t", str(base.TOTAL),
             "-movflags", "+faststart", final)
    print("DONE", final)


if __name__ == "__main__":
    main()
