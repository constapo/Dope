"""Instagram test post: tile-replacement offer (free tools only).

Background: your own job photo (--photo path.jpg) or, by default, a drawn tile-floor pattern
(CSS, no download). Icons: Iconify public API (free SVGs).
Layout: HTML/CSS rendered to PNG with headless Chromium (CHROME env var, default: Playwright's copy).
Usage: python3 build_post.py OUT_DIR [--photo PHOTO.jpg]
Outputs: post_1080x1080.png (feed) and story_1080x1920.png (story / reel cover).
"""
import base64, os, subprocess, sys, time, urllib.parse, urllib.request

CHROME = os.environ.get("CHROME", "/opt/pw-browsers/chromium-1243/chrome-linux64/chrome")

NAVY, ACCENT = "#16232b", "#4FC3F7"  # same colours as the approved reel end card
# Large light-grey porcelain tiles (60 cm look) with grout lines and soft window light, full frame.
TILE_PATTERN = ("background:"
                "radial-gradient(90% 60% at 80% 8%,rgba(255,255,255,.6),rgba(255,255,255,0) 70%),"
                "linear-gradient(90deg,#8e979e 0 4px,transparent 4px 100%) 0 0/360px 100%,"
                "linear-gradient(0deg,#8e979e 0 4px,transparent 4px 100%) 0 0/100% 360px,"
                "linear-gradient(160deg,#e6e9eb 0%,#d3d8db 50%,#c3c9cd 100%)")
ICONS = {"phone": "mdi/phone", "whatsapp": "mdi/whatsapp", "viber": "simple-icons/viber",
         "check": "mdi/check-circle", "facebook": "mdi/facebook", "instagram": "mdi/instagram"}


def fetch(url, path, timeout=180, tries=6, wait=20):
    if os.path.exists(path) and os.path.getsize(path) > 0:
        return path
    for attempt in range(tries):
        try:
            data = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}),
                                          timeout=timeout).read()
            open(path, "wb").write(data)
            return path
        except Exception as e:  # free services; retrying costs nothing
            print(f"retry {attempt + 1}: {e}")
            time.sleep(wait)
    sys.exit(f"could not download {url}")


def data_uri(path, mime):
    return f"data:{mime};base64," + base64.b64encode(open(path, "rb").read()).decode()


def icon(out, name, color="white"):
    path = os.path.join(out, f"icon_{name}.svg")
    fetch(f"https://api.iconify.design/{ICONS[name]}.svg?color={urllib.parse.quote(color)}", path, 30, 3, 3)
    return data_uri(path, "image/svg+xml")


def html(w, h, photo, ic):
    story = h > w
    head = 92 if story else 74
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:{w}px;height:{h}px;font-family:'DejaVu Sans',sans-serif;color:#fff;background:{NAVY};overflow:hidden}}
.photo{{position:absolute;inset:0;{photo}}}
.shade{{position:absolute;inset:0;background:linear-gradient(180deg,rgba(22,35,43,.15) 0%,
  rgba(22,35,43,.25) {38 if story else 30}%,rgba(22,35,43,.93) {62 if story else 58}%,{NAVY} 100%)}}
.brand{{position:absolute;top:{70 if story else 48}px;left:56px;font-weight:700;font-size:34px;letter-spacing:2px;
  background:{NAVY}cc;padding:10px 20px;border-radius:10px}}
.brand span{{color:{ACCENT}}}
.box{{position:absolute;left:56px;right:56px;bottom:{90 if story else 48}px}}
h1{{font-size:{head}px;line-height:1.02;font-weight:800}}
h2{{font-size:{head * .56:.0f}px;color:{ACCENT};margin:10px 0 {26 if story else 18}px;font-weight:700}}
.offer{{display:inline-flex;align-items:center;gap:14px;background:{ACCENT};color:{NAVY};font-weight:800;
  font-size:{34 if story else 30}px;padding:14px 24px;border-radius:14px}}
.offer img{{width:40px}}
.offer small{{display:block;font-size:.78em;font-weight:700}}
.contacts{{display:flex;gap:30px;margin-top:{34 if story else 22}px;font-size:{32 if story else 28}px;font-weight:700;
  flex-wrap:wrap}}
.contacts div{{display:flex;align-items:center;gap:10px}}
.contacts img{{width:{40 if story else 34}px}}
.apps{{display:flex;gap:14px;align-items:center;margin-top:14px;font-size:{26 if story else 23}px;opacity:.95}}
.apps img{{width:{34 if story else 30}px}}
</style></head><body>
<div class="photo"></div><div class="shade"></div>
<div class="brand">INONDA <span>LTD</span></div>
<div class="box">
  <h1>New floor tiles.<br>Old floor out.</h1>
  <h2>Νέα πλακάκια δαπέδου.</h2>
  <div class="offer"><img src="{ic['check_navy']}"><div>Free inspection &amp; written quote
    <small>Δωρεάν αυτοψία και γραπτή προσφορά</small></div></div>
  <div class="contacts">
    <div><img src="{ic['phone']}">+357 94 091 616</div>
    <div><img src="{ic['phone']}">+357 94 091 613</div>
  </div>
  <div class="apps"><img src="{ic['whatsapp']}"><img src="{ic['viber']}">WhatsApp · Viber · Call / Κλήση
    &nbsp;&nbsp;<img src="{ic['instagram']}">@inondaltd</div>
</div></body></html>"""


def main(out, photo_path=None):
    os.makedirs(out, exist_ok=True)
    bg = TILE_PATTERN
    if photo_path:
        bg = f"background:url('{data_uri(photo_path, 'image/jpeg')}') center/cover"
    ic = {n: icon(out, n) for n in ICONS}
    ic["check_navy"] = icon(out, "check", NAVY)
    for w, h, name in [(1080, 1080, "post_1080x1080.png"), (1080, 1920, "story_1080x1920.png")]:
        page = os.path.abspath(os.path.join(out, name.replace(".png", ".html")))
        open(page, "w", encoding="utf-8").write(html(w, h, bg, ic))
        subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                        f"--window-size={w},{h}", f"--screenshot={os.path.abspath(os.path.join(out, name))}",
                        "file://" + page], check=True, capture_output=True)
        print("wrote", os.path.join(out, name))

if __name__ == "__main__":
    args = sys.argv[1:]
    photo = args[args.index("--photo") + 1] if "--photo" in args else None
    main(args[0] if args and args[0] != "--photo" else "out", photo)
