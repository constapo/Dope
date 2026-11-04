#!/usr/bin/env python3
"""Fetch the 18 free photo-realistic stills for build_tiles_photo.py from Pollinations (free, no account).

Every prompt follows the Realism standard in ../shot-list.md: handheld phone at chest height, level
horizon, real-looking, with the realism guard appended. Stills that show warped hands, melted tools or
anything drawn are rejected by eye before building; delete the file and run again with another seed.

Usage: python3 stills_tiles.py STILLS_DIR [name ...]          (Pollinations, one at a time)
       python3 stills_tiles.py --horde STILLS_DIR [name ...]  (AI Horde, anonymous, all at once)
Both are free and need no account. Pollinations stamps a mark in the bottom-right corner, so its
stills are cropped (bottom 6 %) before use.
"""
import json, os, sys, time, urllib.parse, urllib.request

# No "phone/smartphone" here: models then draw a phone into the picture (2026-11-04).
ANGLE = ("candid point-of-view photo taken at chest height by a person standing in the room, level horizon, "
         "looking slightly down at the work, vertical 9:16 photo")
GUARD = ("shot on a real camera, natural imperfect lighting, realistic physics and textures, real-world "
         "scale. Avoid: CGI, 3D render, cartoon, illustration, oversaturated colours, glowing light, "
         "warped hands, extra fingers, melting objects, text, logos, watermarks")
ROOM = "small living room of an older apartment in Cyprus, window daylight"

STILLS = {
    "old1": f"cracked and chipped beige 1990s ceramic floor tiles, dirty grey grout, one tile lifting, {ROOM}",
    "old2": f"view across a floor of worn beige ceramic tiles with stains and dull scratched glaze, {ROOM}",
    "old3": "close view of a long crack running through beige floor tiles with dark dirt inside the crack",
    "measure": f"tradesman's hands pulling a yellow tape measure across an old tiled floor, {ROOM}",
    "protect": "doorway and wooden furniture covered with clear plastic dust sheets and masking tape, room under renovation",
    "work1": "close view of two gloved hands holding a wide steel chisel under a broken beige floor tile, prying it up, dust, bare grey cement under it",
    "debris": "heavy rubble bags full of broken tile pieces standing by the door of a room under renovation",
    "screed": "bare smooth grey cement screed floor with a long aluminium spirit level lying on it, empty room",
    "water1": "grey liquid waterproofing membrane freshly rolled over a whole cement floor, paint roller on extension pole",
    "water2": "gloved hand pressing reinforcing waterproof tape into the wall-to-floor corner over grey membrane",
    "adhesive": "gloved hand holding a notched steel trowel, combing grey tile adhesive into even straight ridges on a grey floor",
    "water3": "first large glossy black marble-look tiles laid on grey waterproofing membrane, only black tiles, rest of floor bare",
    "work2": "gloved hands placing a large polished black marble-look floor tile next to other black tiles, bare screed beyond",
    "spacers": "small white plastic cross spacers in the narrow joints between large glossy BLACK marble-look floor tiles, a green spirit level lying across the black tiles, all tiles black",
    "grout": "kneeling tiler's gloved hand pressing dark grey grout into the joints of black marble-look floor tiles with a red rubber grout float, grout bucket beside",
    "clean": "gloved hand wiping a glossy black marble-look tiled floor with a big yellow sponge, bucket of water beside, empty room",
    "after": f"finished floor of large polished black marble-look tiles with fine white veins, mirror-smooth, window reflection on the glossy black floor, thin even grout lines, {ROOM}",
    "after3": "bright modern room with a large glossy black marble-look tiled floor with fine white and grey veins, sofa and plant, clean and new",
}


def fetch(name, out_dir, seed=4100):
    path = os.path.join(out_dir, name + ".jpg")
    if os.path.exists(path) and os.path.getsize(path) > 20000:
        return path
    prompt = f"{STILLS[name]}, {ANGLE}. {GUARD}"
    url = (f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt)}"
           f"?width=1080&height=1920&nologo=true&seed={seed + list(STILLS).index(name)}")
    for attempt in range(8):
        time.sleep(20)  # free tier rate-limits fast callers
        try:
            data = urllib.request.urlopen(url, timeout=240).read()
            if len(data) > 20000:
                open(path, "wb").write(data)
                print("ok", name, flush=True)
                return path
        except Exception as e:
            print("retry", name, e, flush=True)
        time.sleep(30 * attempt)
    raise SystemExit(f"could not fetch {name}")


HORDE = "https://aihorde.net/api/v2"
HORDE_MODELS = ["Juggernaut XL", "AlbedoBase XL (SDXL)"]  # photoreal SDXL models online 2026-11-04
NEG = "cartoon, illustration, drawing, painting, 3d render, cgi, anime, text, watermark, logo, deformed hands, extra fingers, top-down view, aerial view, blurry"


def horde_call(path, body=None):
    req = urllib.request.Request(HORDE + path, data=json.dumps(body).encode() if body else None,
                                 headers={"apikey": "0000000000", "Content-Type": "application/json",
                                          "Client-Agent": "inonda-video-builder:1:anonymous",
                                          "User-Agent": "inonda-video-builder/1.0"})
    return json.load(urllib.request.urlopen(req, timeout=120))


def horde(names, out_dir, seed=int(os.environ.get('SEED', '4100'))):
    jobs = {}
    for n in names:
        if os.path.exists(os.path.join(out_dir, n + ".webp")) or os.path.exists(os.path.join(out_dir, n + ".jpg")):
            continue
        prompt = f"{STILLS[n]}, {ANGLE}. shot on a real camera, natural imperfect lighting, realistic textures ### {NEG}"
        r = horde_call("/generate/async", {"prompt": prompt, "models": HORDE_MODELS,
                                           "params": {"width": 640, "height": 1152, "steps": 28,
                                                      "seed": str(seed + list(STILLS).index(n)), "n": 1}})
        jobs[n] = r["id"]; print("queued", n, flush=True)
    while jobs:
        time.sleep(20)
        for n, jid in list(jobs.items()):
            st = horde_call(f"/generate/check/{jid}")
            if st.get("faulted"):
                print("faulted", n, flush=True); del jobs[n]; continue
            if st.get("done"):
                g = horde_call(f"/generate/status/{jid}")["generations"][0]
                data = urllib.request.urlopen(urllib.request.Request(g["img"], headers={"User-Agent": "inonda-video-builder/1.0"}), timeout=120).read()
                open(os.path.join(out_dir, n + ".webp"), "wb").write(data)
                print("ok", n, g.get("model"), flush=True); del jobs[n]
        print("waiting", len(jobs), flush=True)


if __name__ == "__main__":
    use_horde = sys.argv[1] == "--horde"
    args = sys.argv[2:] if use_horde else sys.argv[1:]
    out = args[0]
    os.makedirs(out, exist_ok=True)
    names = args[1:] or list(STILLS)
    if use_horde:
        horde(names, out)
    else:
        for n in names:
            fetch(n, out)
