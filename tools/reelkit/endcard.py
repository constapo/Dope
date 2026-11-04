"""Silent bilingual Inonda end card, ported from inonda-youtube-videos/free-build/build_tiles_preview.py.

No prices (constitution, Principle I): the card offers a free inspection and a written quote only.
"""
from __future__ import annotations

from PIL import Image, ImageDraw, ImageFont

NAVY, ACCENT = (22, 35, 43), (79, 195, 247)
FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

ROWS = [("Inonda Ltd", 84, "white", FONT_B), ("Repairs · Renovations · Maintenance · Cyprus", 32, "white", FONT_R),
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


def text_center(d, w, y, s, font, fill, stroke=4):
    tw = d.textlength(s, font=font)
    d.text(((w - tw) / 2, y), s, font=font, fill=fill, stroke_width=stroke, stroke_fill=(0, 0, 0))


def wrap(d, s, font, maxw):
    words, lines, cur = s.split(), [], ""
    for word in words:
        t = (cur + " " + word).strip()
        if d.textlength(t, font=font) > maxw and cur:
            lines.append(cur)
            cur = word
        else:
            cur = t
    return lines + [cur] if cur else lines


def end_card(w: int, h: int):
    """Card for a vertical reel (1080x1920) or, scaled to fit, a landscape video (1920x1080)."""
    natural_h = 230 + sum(int(sz * 1.45) for _, sz, _, _ in ROWS)
    scale = min(1.0, (h - 120) / natural_h, w / 1080)
    im = Image.new("RGB", (w, h), NAVY)
    d = ImageDraw.Draw(im)
    y = int(230 * scale) if h > w else int((h - natural_h * scale + 230 * scale) / 2)
    for s, sz, c, f in ROWS:
        size = max(12, int(sz * scale))
        if s:
            text_center(d, w, y, s, ImageFont.truetype(f, size), c, 0)
        y += int(size * 1.45)
    return im
