"""Create the small solid-colour test stills used by the offline tests."""
import os

from PIL import Image, ImageDraw

HERE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "stills")
STILLS = {"landscape": ((1600, 1200), (140, 120, 100)), "portrait": ((1200, 1600), (60, 60, 64)),
          "wide": ((2000, 1000), (180, 170, 150))}


def make(out=HERE):
    os.makedirs(out, exist_ok=True)
    for name, (size, colour) in STILLS.items():
        im = Image.new("RGB", size, colour)
        d = ImageDraw.Draw(im)
        for x in range(0, size[0], 100):  # grid so camera moves are visible
            d.line([x, 0, x, size[1]], fill=(255, 255, 255), width=2)
        for y in range(0, size[1], 100):
            d.line([0, y, size[0], y], fill=(255, 255, 255), width=2)
        im.save(os.path.join(out, f"{name}.jpg"), quality=85)


if __name__ == "__main__":
    make()
