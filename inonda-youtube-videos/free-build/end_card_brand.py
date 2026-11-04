#!/usr/bin/env python3
"""Standard Inonda end card (owner's request 2026-11-04), silent, bilingual EN/GR, 1080x1920.

- Company logo above "Inonda Ltd" on a light (white) panel.
- Both phone numbers, each with a modern smartphone icon (not the classic handset; the owner
  rejected that symbol).
- WhatsApp, Viber and every social account in their original brand colours, never monochrome.
Brand glyphs: Simple Icons (CC0), kept in ../brand/social-icons/. Needs: pip install cairosvg.

Usage: from end_card_brand import end_card   ->  PIL RGB image
       python3 end_card_brand.py OUT.png      ->  writes a still for checking
"""
import io, os, sys
import cairosvg
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
NAVY, ACCENT, SOFT = (22, 35, 43), (79, 195, 247), (205, 220, 228)
FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
HERE = os.path.dirname(os.path.abspath(__file__))
BRAND = os.path.join(HERE, "..", "brand")
ICONS = os.path.join(BRAND, "social-icons")

PHONES = [("+357 94 091 616", "Irina · Director  /  Ιρίνα · Διευθύντρια"),
          ("+357 94 091 613", "Constantin · Foreman  /  Κωνσταντίν · Εργοδηγός")]
SOCIAL = [("facebook", "Facebook", "inondalimited"), ("instagram", "Instagram", "@inondaltd"),
          ("tiktok", "TikTok", "@inonda26"), ("youtube", "YouTube", "@InondaLTD")]


def font(path, size):
    return ImageFont.truetype(path, size)


def glyph(name, size, colour):
    """Simple Icons glyph rendered in one colour, transparent background."""
    svg = open(os.path.join(ICONS, name + ".svg")).read().replace("<svg ", f'<svg fill="{colour}" ', 1)
    return Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg.encode(), output_width=size,
                                                  output_height=size))).convert("RGBA")


def rounded_mask(size, radius):
    m = Image.new("L", (size, size), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, size - 1, size - 1], radius, fill=255)
    return m


def gradient(size, stops):
    """Diagonal gradient (bottom-left to top-right), stops = [(pos, (r,g,b)), ...]."""
    im = Image.new("RGB", (size, size))
    px = im.load()
    for y in range(size):
        for x in range(size):
            t = (x + (size - 1 - y)) / (2 * (size - 1))
            for (p0, c0), (p1, c1) in zip(stops, stops[1:]):
                if p0 <= t <= p1:
                    k = (t - p0) / (p1 - p0)
                    px[x, y] = tuple(int(a + (b - a) * k) for a, b in zip(c0, c1))
                    break
    return im


def brand_tile(name, size=96):
    """App-style rounded tile in the platform's own colours."""
    r = int(size * 0.24)
    g = int(size * 0.62)
    off = ((size - g) // 2, (size - g) // 2)
    if name == "instagram":
        bg = gradient(size, [(0, (254, 218, 117)), (0.25, (250, 126, 30)), (0.5, (214, 41, 118)),
                             (0.75, (150, 47, 191)), (1, (79, 91, 213))]).convert("RGBA")
        bg.alpha_composite(glyph(name, g, "#FFFFFF"), off)
    elif name == "tiktok":  # black tile, cyan and red echoes under the white note
        bg = Image.new("RGBA", (size, size), (0, 0, 0, 255))
        s = max(2, size // 32)
        bg.alpha_composite(glyph(name, g, "#25F4EE"), (off[0] - s, off[1] - s))
        bg.alpha_composite(glyph(name, g, "#FE2C55"), (off[0] + s, off[1] + s))
        bg.alpha_composite(glyph(name, g, "#FFFFFF"), off)
    elif name == "youtube":  # white tile, red play button with white triangle
        bg = Image.new("RGBA", (size, size), (255, 255, 255, 255))
        g = int(size * 0.74)
        bg.alpha_composite(glyph(name, g, "#FF0000"), ((size - g) // 2, (size - g) // 2))
    else:
        colour = {"facebook": (24, 119, 242), "whatsapp": (37, 211, 102), "viber": (115, 96, 242)}[name]
        bg = Image.new("RGBA", (size, size), colour + (255,))
        bg.alpha_composite(glyph(name, g, "#FFFFFF"), off)
    tile = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    tile.paste(bg, (0, 0), rounded_mask(size, r))
    return tile


def phone_icon(size=96):
    """Modern smartphone: rounded accent tile with a slim white handset outline and screen."""
    t = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(t)
    d.rounded_rectangle([0, 0, size - 1, size - 1], int(size * 0.24), fill=ACCENT + (255,))
    pw, ph = int(size * 0.40), int(size * 0.68)
    x0, y0 = (size - pw) // 2, (size - ph) // 2
    d.rounded_rectangle([x0, y0, x0 + pw, y0 + ph], int(pw * 0.22), fill=(255, 255, 255, 255))
    m = max(3, size // 24)
    d.rounded_rectangle([x0 + m, y0 + m * 2, x0 + pw - m, y0 + ph - m * 2], int(pw * 0.12), fill=NAVY + (255,))
    d.rounded_rectangle([x0 + pw * 0.36, y0 + m * 0.6, x0 + pw * 0.64, y0 + m * 1.4], m, fill=NAVY + (255,))
    return t


def mail_icon(size=96):
    t = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(t)
    d.rounded_rectangle([0, 0, size - 1, size - 1], int(size * 0.24), fill=(0, 120, 212, 255))  # Outlook blue
    x0, y0, x1, y1 = size * 0.2, size * 0.3, size * 0.8, size * 0.7
    d.rounded_rectangle([x0, y0, x1, y1], int(size * 0.05), fill=(255, 255, 255, 255))
    w = max(3, size // 20)
    d.line([(x0 + w, y0 + w), (size / 2, size * 0.52), (x1 - w, y0 + w)], fill=(0, 120, 212, 255), width=w)
    return t


def centre(d, y, text, f, fill):
    d.text(((W - d.textlength(text, font=f)) / 2, y), text, font=f, fill=fill)


def end_card():
    im = Image.new("RGBA", (W, H), NAVY + (255,))
    d = ImageDraw.Draw(im)

    # Logo on a light panel, above the company name.
    logo = Image.open(os.path.join(BRAND, "inonda-logo-overlay.png")).convert("RGBA")
    lw = 420
    logo = logo.resize((lw, int(logo.height * lw / logo.width)), Image.LANCZOS)
    pw, ph = lw + 80, logo.height + 50
    px, py = (W - pw) // 2, 70
    d.rounded_rectangle([px, py, px + pw, py + ph], 36, fill=(255, 255, 255, 255))
    im.alpha_composite(logo, ((W - lw) // 2, py + 25))
    y = py + ph + 30

    centre(d, y, "Inonda Ltd", font(FONT_B, 78), "white"); y += 100
    centre(d, y, "Repairs · Renovations · Maintenance · Cyprus", font(FONT_R, 30), SOFT); y += 44
    centre(d, y, "Επισκευές · Ανακαινίσεις · Συντήρηση · Κύπρος", font(FONT_R, 30), SOFT); y += 70

    centre(d, y, "CONTACT US  ·  ΕΠΙΚΟΙΝΩΝΗΣΤΕ", font(FONT_B, 50), ACCENT); y += 66
    centre(d, y, "Free inspection & written quote  /  Δωρεάν αυτοψία & γραπτή προσφορά",
           font(FONT_R, 25), "white"); y += 56

    # Phone rows: modern phone tile + number + who answers.
    icon, fn, fl = phone_icon(96), font(FONT_B, 58), font(FONT_R, 25)
    x_ic = 150
    for num, who in PHONES:
        im.alpha_composite(icon, (x_ic, y))
        d.text((x_ic + 126, y - 2), num, font=fn, fill="white")
        d.text((x_ic + 128, y + 64), who, font=fl, fill=SOFT)
        y += 128

    # WhatsApp / Viber / call, in brand colours.
    y += 6
    s = 72
    label = "WhatsApp  ·  Viber  ·  Call / Κλήση"
    f = font(FONT_R, 32)
    total = s * 2 + 16 + 24 + d.textlength(label, font=f)
    x = int((W - total) / 2)
    im.alpha_composite(brand_tile("whatsapp", s), (x, y)); x += s + 16
    im.alpha_composite(brand_tile("viber", s), (x, y)); x += s + 24
    d.text((x, y + 17), label, font=f, fill="white"); y += s + 26

    f = font(FONT_R, 36)
    mail = "inonda2026@outlook.com"
    total = s + 24 + d.textlength(mail, font=f)
    x = int((W - total) / 2)
    im.alpha_composite(mail_icon(s), (x, y)); d.text((x + s + 24, y + 14), mail, font=f, fill="white")
    y += s + 60

    centre(d, y, "FOLLOW US  ·  ΑΚΟΛΟΥΘΗΣΤΕ ΜΑΣ", font(FONT_B, 50), ACCENT); y += 82

    # Social accounts: two columns of brand tiles.
    s, fb, fr = 84, font(FONT_B, 30), font(FONT_R, 32)
    cols = [110, 590]
    for i, (key, name, handle) in enumerate(SOCIAL):
        cx, cy = cols[i % 2], y + (i // 2) * (s + 34)
        im.alpha_composite(brand_tile(key, s), (cx, cy))
        d.text((cx + s + 22, cy + 4), name, font=fb, fill=SOFT)
        d.text((cx + s + 22, cy + 42), handle, font=fr, fill="white")
    y += 2 * (s + 34) + 30

    centre(d, y, "inonda.site  |  inonda.org  |  inonda.homes", font(FONT_R, 34), "white")
    return im.convert("RGB")


def _glass(im, box, radius=40, tint=(255, 255, 255, 38), edge=(255, 255, 255, 70)):
    """Frosted-glass panel: blur what is behind it, lay a light tint and a thin bright edge."""
    from PIL import ImageFilter
    x0, y0, x1, y1 = [int(v) for v in box]
    region = im.crop((x0, y0, x1, y1)).filter(ImageFilter.GaussianBlur(18))
    over = Image.new("RGBA", region.size, tint)
    region = Image.alpha_composite(region.convert("RGBA"), over)
    mask = Image.new("L", region.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, region.width - 1, region.height - 1], radius, fill=255)
    im.paste(region, (x0, y0), mask)
    ImageDraw.Draw(im).rounded_rectangle([x0, y0, x1 - 1, y1 - 1], radius, outline=edge, width=2)


def _background(bg):
    from PIL import ImageFilter, ImageEnhance
    if bg is None:  # navy to teal gradient
        g = Image.new("RGB", (W, H))
        px = g.load()
        for y in range(H):
            t = y / (H - 1)
            c = tuple(int(a + (b - a) * t) for a, b in zip((14, 30, 48), (10, 78, 96)))
            for x in range(W):
                px[x, y] = c
        return g.convert("RGBA")
    bg = bg.convert("RGB")
    s = max(W / bg.width, H / bg.height)
    bg = bg.resize((round(bg.width * s), round(bg.height * s)), Image.LANCZOS)
    bg = bg.crop(((bg.width - W) // 2, (bg.height - H) // 2, (bg.width - W) // 2 + W, (bg.height - H) // 2 + H))
    bg = ImageEnhance.Brightness(bg.filter(ImageFilter.GaussianBlur(26))).enhance(0.45)
    shade = Image.new("RGBA", (W, H), (8, 20, 30, 110))
    return Image.alpha_composite(bg.convert("RGBA"), shade)


def end_card_glass(bg=None):
    """2026 'link-in-bio' style: blurred photo of the finished job behind frosted-glass panels,
    pill buttons for the phones, a row of brand-coloured app icons. bg: PIL image or None."""
    im = _background(bg)
    d = ImageDraw.Draw(im)

    logo = Image.open(os.path.join(BRAND, "inonda-logo-overlay.png")).convert("RGBA")
    lw = 360
    logo = logo.resize((lw, int(logo.height * lw / logo.width)), Image.LANCZOS)
    pw, ph = lw + 70, logo.height + 40
    px, py = (W - pw) // 2, 80
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))  # soft shadow under the light logo panel
    ImageDraw.Draw(sh).rounded_rectangle([px + 6, py + 14, px + pw + 6, py + ph + 14], 44, fill=(0, 0, 0, 120))
    from PIL import ImageFilter
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14)))
    d.rounded_rectangle([px, py, px + pw, py + ph], 44, fill=(255, 255, 255, 255))
    im.alpha_composite(logo, ((W - lw) // 2, py + 20))
    y = py + ph + 26
    centre(d, y, "Inonda Ltd", font(FONT_B, 72), "white"); y += 92
    centre(d, y, "Repairs · Renovations · Maintenance · Cyprus", font(FONT_R, 28), SOFT); y += 40
    centre(d, y, "Επισκευές · Ανακαινίσεις · Συντήρηση · Κύπρος", font(FONT_R, 28), SOFT); y += 66

    centre(d, y, "FREE INSPECTION & QUOTE", font(FONT_B, 54), ACCENT); y += 66
    centre(d, y, "ΔΩΡΕΑΝ ΑΥΤΟΨΙΑ & ΠΡΟΣΦΟΡΑ", font(FONT_B, 44), ACCENT); y += 78

    # Phone pills.
    icon, fn, fl = phone_icon(92), font(FONT_B, 56), font(FONT_R, 25)
    for num, who in PHONES:
        _glass(im, (90, y, W - 90, y + 124), radius=62)
        d = ImageDraw.Draw(im)
        im.alpha_composite(icon, (106, y + 16))
        d.text((228, y + 10), num, font=fn, fill="white")
        d.text((230, y + 78), who, font=fl, fill=SOFT)
        y += 144

    # Message row: WhatsApp, Viber, email.
    s = 78
    _glass(im, (90, y, W - 90, y + s + 36), radius=50)
    d = ImageDraw.Draw(im)
    im.alpha_composite(brand_tile("whatsapp", s), (110, y + 18))
    im.alpha_composite(brand_tile("viber", s), (110 + s + 14, y + 18))
    d.text((110 + 2 * s + 40, y + 20), "WhatsApp · Viber · Call", font=font(FONT_B, 32), fill="white")
    d.text((110 + 2 * s + 40, y + 62), "Γράψτε μας ή καλέστε μας", font=font(FONT_R, 26), fill=SOFT)
    y += s + 56
    f = font(FONT_R, 34)
    mail = "inonda2026@outlook.com"
    total = 60 + 20 + d.textlength(mail, font=f)
    x = int((W - total) / 2)
    im.alpha_composite(mail_icon(60), (x, y)); d.text((x + 80, y + 10), mail, font=f, fill="white")
    y += 98

    # Follow us: four brand icons in a row on one glass panel.
    _glass(im, (60, y, W - 60, y + 280), radius=44)
    d = ImageDraw.Draw(im)
    centre(d, y + 22, "FOLLOW US  ·  ΑΚΟΛΟΥΘΗΣΤΕ ΜΑΣ", font(FONT_B, 40), "white")
    s, fh = 100, font(FONT_R, 24)
    colw = (W - 120) / 4
    for i, (key, name, handle) in enumerate(SOCIAL):
        cx = 60 + colw * i + colw / 2
        im.alpha_composite(brand_tile(key, s), (int(cx - s / 2), y + 88))
        d.text((cx - d.textlength(handle, font=fh) / 2, y + 88 + s + 16), handle, font=fh, fill="white")
    y += 310
    centre(d, y, "inonda.site  ·  inonda.org  ·  inonda.homes", font(FONT_B, 32), "white")
    return im.convert("RGB")


if __name__ == "__main__":
    # python3 end_card_brand.py OUT.png [glass [BACKGROUND_IMAGE]]
    out = sys.argv[1] if len(sys.argv) > 1 else "end_card.png"
    if len(sys.argv) > 2 and sys.argv[2] == "glass":
        end_card_glass(Image.open(sys.argv[3]) if len(sys.argv) > 3 else None).save(out)
    else:
        end_card().save(out)
