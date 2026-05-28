"""Generate favicon PNG/ICO assets from the brand mark (indigo->violet bolt).
One-off build script; safe to re-run. Uses 4x supersampling for clean edges.
"""
from pathlib import Path
from PIL import Image, ImageDraw

OUT = Path(__file__).parent / "public"
SS = 4  # supersample factor

# Brand gradient endpoints (diagonal top-left -> bottom-right)
C0 = (99, 102, 241)   # indigo-500  #6366F1
C1 = (124, 58, 237)   # violet-600  #7C3AED

# Lightning bolt polygon on a 64x64 grid (matches favicon.svg path)
BOLT = [(34.5, 27.5), (34.5, 11), (13, 38.5), (30, 38.5),
        (30, 55.5), (51.5, 27.5)]


def _gradient(size):
    """Diagonal gradient square."""
    img = Image.new("RGB", (size, size))
    px = img.load()
    for y in range(size):
        for x in range(size):
            t = (x + y) / (2 * (size - 1))
            px[x, y] = tuple(round(C0[i] + (C1[i] - C0[i]) * t) for i in range(3))
    return img


def _rounded_mask(size, radius):
    m = Image.new("L", (size, size), 0)
    d = ImageDraw.Draw(m)
    d.rounded_rectangle([0, 0, size - 1, size - 1], radius=radius, fill=255)
    return m


def render(px):
    """Render the icon at px pixels (rounded gradient tile + white bolt)."""
    s = px * SS
    grad = _gradient(s)
    radius = round(s * 15 / 64)  # match svg rx=15 on 64 grid

    tile = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    tile.paste(grad, (0, 0), _rounded_mask(s, radius))

    # bolt
    bolt = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    bd = ImageDraw.Draw(bolt)
    scale = s / 64.0
    pts = [(x * scale, y * scale) for (x, y) in BOLT]
    bd.polygon(pts, fill=(255, 255, 255, 255))
    tile = Image.alpha_composite(tile, bolt)

    return tile.resize((px, px), Image.LANCZOS)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    sizes = {
        "favicon-16.png": 16,
        "favicon-32.png": 32,
        "favicon-48.png": 48,
        "apple-touch-icon.png": 180,
        "icon-192.png": 192,
        "icon-512.png": 512,
        "og-fallback.png": 512,
    }
    imgs = {}
    for name, px in sizes.items():
        img = render(px)
        img.save(OUT / name)
        imgs[px] = img
        print("wrote", name, f"{px}x{px}")

    # Multi-resolution .ico (16/32/48)
    ico = render(256)
    ico.save(OUT / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48), (256, 256)])
    print("wrote favicon.ico (16/32/48/256)")


if __name__ == "__main__":
    main()
