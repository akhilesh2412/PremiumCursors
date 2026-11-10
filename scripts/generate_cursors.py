"""
Pro Premium Cursors — generator (v3 macOS style)
Draws a full Windows cursor scheme (17 roles) in the sleek macOS look:
small slim shapes, glossy charcoal-black fill, THIN white outline, soft
shadow; the Link hand is the classic white glove; Busy is the iconic
spinning beach ball. Exports .cur (32+48 PNG entries) and .ani (12-frame).
Run:  pip install pillow && python scripts/generate_cursors.py
Out:  ../cursors/
"""
import io, os, struct
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "cursors")
os.makedirs(OUT, exist_ok=True)
S = 256
WHITE = (255, 255, 255, 255)
BLACK = (10, 10, 12, 255)


def _lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def _diag_gradient(top, bottom):
    g = Image.new("RGBA", (S, S))
    px = g.load()
    for y in range(S):
        for x in range(S):
            px[x, y] = _lerp(top, bottom, (x + y) / (2 * (S - 1))) + (255,)
    return g


MAC_FILL = _diag_gradient((86, 86, 96), (8, 8, 11))       # glossy charcoal, NOT flat black
GLOVE_FILL = _diag_gradient((255, 255, 255), (203, 203, 214))


def _smooth(mask, fatten=7, blur=6):
    """HEAVY rounding: slightly fatten, strong blur, re-threshold —
    every corner (even the arrow tip) comes out round and smooth."""
    m = mask.filter(ImageFilter.MaxFilter(fatten)) if fatten > 1 else mask
    m = m.filter(ImageFilter.GaussianBlur(blur))
    return m.point(lambda v: 255 if v > 100 else 0)


def compose(mask, fill=None, border=WHITE, fatten=7, blur=6):
    """Sleek mac-style body: tiny soft shadow, THIN outline, glossy fill."""
    fill = fill or MAC_FILL
    m = _smooth(mask, fatten, blur)
    dil = m.filter(ImageFilter.MaxFilter(9))               # thin outline
    out = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    sh = Image.new("RGBA", (S, S), (0, 0, 0, 140))
    out.paste(sh, (4, 6), dil.filter(ImageFilter.GaussianBlur(5)))
    out.paste(Image.new("RGBA", (S, S), border), (0, 0), dil)
    out.paste(fill, (0, 0), m)
    gloss = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    gd = ImageDraw.Draw(gloss)
    gd.polygon([(0, 0), (S, 0), (0, int(S * 0.6))], fill=(255, 255, 255, 64))
    gloss = gloss.filter(ImageFilter.GaussianBlur(16))
    gloss.putalpha(Image.composite(gloss.split()[3], Image.new("L", (S, S), 0), m))
    out.alpha_composite(gloss)
    return out


def new_mask():
    img = Image.new("L", (S, S), 0)
    return img, ImageDraw.Draw(img)


def save_cur(img, name, hotspot):
    entries = b""
    blobs = b""
    for size in (48, 32):
        r = img.resize((size, size), Image.LANCZOS)
        bio = io.BytesIO(); r.save(bio, "PNG"); data = bio.getvalue()
        hx = max(0, min(size - 1, round(hotspot[0] * size / S)))
        hy = max(0, min(size - 1, round(hotspot[1] * size / S)))
        entries += struct.pack("<BBBBHHII", size if size < 256 else 0, size if size < 256 else 0,
                               0, 0, hx, hy, len(data), 6 + 2 * 16 + len(blobs))
        blobs += data
    cur = struct.pack("<HHH", 0, 2, 2) + entries + blobs
    open(os.path.join(OUT, name), "wb").write(cur)
    print("cur", name)


def save_ani(frames, name, hotspot, jif=1):
    datas = []
    for f in frames:
        bio = io.BytesIO(); f.save(bio, "PNG"); datas.append(bio.getvalue())
    n = len(datas)
    anih = struct.pack("<IIIIIIIII", 36, n, n, 0, 0, 32, 1, jif, 1)
    seq = b"".join(struct.pack("<i", i) for i in range(n))
    rate = b"".join(struct.pack("<I", jif) for _ in range(n))

    def chunk(tag, payload):
        pad = b"\x00" if len(payload) % 2 else b""
        return tag + struct.pack("<I", len(payload)) + payload + pad

    ico_chunks = b""
    for i, data in enumerate(datas):
        one = struct.pack("<HHH", 0, 2, 1) + struct.pack(
            "<BBBBHHII", 0, 0, 0, 0, hotspot[0], hotspot[1], len(data), 22) + data
        ico_chunks += chunk(b"icon", one)
    fram = chunk(b"LIST", b"fram" + ico_chunks)
    body = b"ACON" + chunk(b"anih", anih) + chunk(b"rate", rate) + chunk(b"seq ", seq) + fram
    open(os.path.join(OUT, name), "wb").write(b"RIFF" + struct.pack("<I", len(body)) + body)
    print("ani", name, n, "frames")


def font(sz):
    for p in ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
              "C:\\Windows\\Fonts\\arialbd.ttf"):
        if os.path.exists(p):
            return ImageFont.truetype(p, sz)
    return ImageFont.load_default()


# ---------------- shapes (slim + smaller, mac proportions) ----------------
def arrow_mask():
    m, d = new_mask()
    d.polygon([(64, 24), (64, 176), (102, 140), (120, 186), (146, 174), (128, 126), (178, 126)],
              fill=255)
    return m


def hand_mask():
    m, d = new_mask()
    # 4 distinct fingers (WIDE gaps so they survive the heavy rounding)
    for fx, fh in [(90, 104), (124, 116), (158, 106), (192, 86)]:
        d.rounded_rectangle([fx, 148 - fh, fx + 20, 152], 10, fill=255)
    # thumb sticking out on the left
    d.polygon([(92, 158), (56, 176), (62, 208), (94, 198)], fill=255)
    # palm
    d.rounded_rectangle([84, 138, 218, 234], 28, fill=255)
    return m


BALL_COLORS = [(255, 59, 48), (255, 149, 0), (255, 204, 0),
               (52, 199, 89), (10, 132, 255), (191, 90, 242)]


def beachball(step, center=(128, 128), radius=88):
    """Iconic macOS spinning beach ball."""
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    cx, cy = center
    # soft shadow
    sh = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    ImageDraw.Draw(sh).ellipse([cx - radius, cy - radius + 10, cx + radius, cy + radius + 10],
                               fill=(0, 0, 0, 110))
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(7)))
    d = ImageDraw.Draw(img)
    box = [cx - radius, cy - radius, cx + radius, cy + radius]
    rot = step * 30
    for i, col in enumerate(BALL_COLORS):
        d.pieslice(box, start=rot + i * 60 - 90, end=rot + (i + 1) * 60 - 90,
                   fill=col + (255,), outline=(255, 255, 255, 255), width=3)
    d.ellipse(box, outline=(30, 30, 34, 255), width=4)
    # glossy highlight top
    gl = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    ImageDraw.Draw(gl).ellipse([cx - radius * 0.62, cy - radius * 0.88,
                                cx + radius * 0.45, cy - radius * 0.18],
                               fill=(255, 255, 255, 105))
    img.alpha_composite(gl.filter(ImageFilter.GaussianBlur(10)))
    return img


def build():
    # Arrow + derivatives
    arrow = compose(arrow_mask())
    save_cur(arrow, "Arrow.cur", (64, 24))

    help_img = arrow.copy()
    hd = ImageDraw.Draw(help_img)
    hd.ellipse([150, 148, 226, 224], fill=(255, 255, 255, 255), outline=(15, 15, 18, 255), width=5)
    hd.text((172, 158), "?", fill=(15, 15, 18, 255), font=font(52))
    save_cur(help_img, "Help.cur", (64, 24))

    small_arrow = arrow.resize((176, 176), Image.LANCZOS)
    frames = []
    for i in range(12):
        f = Image.new("RGBA", (S, S), (0, 0, 0, 0))
        f.alpha_composite(small_arrow, (2, 2))
        ball = beachball(i, center=(182, 182), radius=58)
        f.alpha_composite(ball)
        frames.append(f)
    save_ani(frames, "AppStarting.ani", (6, 6))
    save_ani([beachball(i) for i in range(12)], "Wait.ani", (128, 128))

    # Crosshair (thin, mac-like)
    m, d = new_mask()
    d.ellipse([86, 86, 170, 170], outline=255, width=11)
    for box in ([118, 28, 138, 84], [118, 172, 138, 228], [28, 118, 84, 138], [172, 118, 228, 138]):
        d.rounded_rectangle(box, 5, fill=255)
    d.ellipse([120, 120, 136, 136], fill=255)
    save_cur(compose(m), "Crosshair.cur", (128, 128))

    # IBeam (slim)
    m, d = new_mask()
    d.rounded_rectangle([118, 52, 138, 204], 8, fill=255)
    d.rounded_rectangle([84, 44, 172, 66], 9, fill=255)
    d.rounded_rectangle([84, 190, 172, 212], 9, fill=255)
    save_cur(compose(m), "IBeam.cur", (128, 128))

    # NWPen (slim pen)
    m, d = new_mask()
    d.polygon([(66, 196), (84, 138), (168, 54), (202, 88), (118, 172)], fill=255)
    d.polygon([(66, 196), (78, 160), (96, 178)], fill=255)
    save_cur(compose(m), "NWPen.cur", (66, 196))

    # No (prohibited)
    m, d = new_mask()
    d.ellipse([52, 52, 204, 204], outline=255, width=24)
    d.polygon([(80, 158), (158, 80), (180, 102), (102, 180)], fill=255)
    save_cur(compose(m, fatten=3, blur=4.5), "No.cur", (128, 128))

    # Resize arrows (slim shafts)
    def dbl(p1, p2, vertical=True):
        m, d = new_mask()
        if vertical:
            d.polygon([(128, 36), (170, 92), (143, 92), (143, 164), (170, 164), (128, 220),
                       (86, 164), (113, 164), (113, 92), (86, 92)], fill=255)
        else:
            d.polygon([(36, 128), (92, 86), (92, 113), (164, 113), (164, 86), (220, 128),
                       (164, 170), (164, 143), (92, 143), (92, 170)], fill=255)
        return compose(m)

    save_cur(dbl(None, None, True), "SizeNS.cur", (128, 128))
    save_cur(dbl(None, None, False), "SizeWE.cur", (128, 128))

    # Diagonals: rotate the (correct) horizontal double-arrow mask by 45 deg
    hm, hd2 = new_mask()
    hd2.polygon([(36, 128), (92, 86), (92, 113), (164, 113), (164, 86), (220, 128),
                 (164, 170), (164, 143), (92, 143), (92, 170)], fill=255)
    save_cur(compose(hm.rotate(45, resample=Image.BICUBIC)), "SizeNWSE.cur", (128, 128))
    save_cur(compose(hm.rotate(-45, resample=Image.BICUBIC)), "SizeNESW.cur", (128, 128))

    # SizeAll: slim 4-way
    m, d = new_mask()
    d.polygon([(128, 30), (160, 66), (141, 66), (141, 115), (190, 115), (226, 128), (190, 141),
               (141, 141), (141, 190), (160, 190), (128, 226), (96, 190), (115, 190), (115, 141),
               (66, 141), (30, 128), (66, 115), (115, 115), (115, 66), (96, 66)], fill=255)
    save_cur(compose(m), "SizeAll.cur", (128, 128))

    # UpArrow (slim)
    m, d = new_mask()
    d.polygon([(128, 36), (190, 118), (152, 118), (152, 218), (104, 218), (104, 118), (66, 118)],
              fill=255)
    save_cur(compose(m), "UpArrow.cur", (128, 118))

    # Hand = white mac glove (white fill, thin black outline) + finger separators
    glove = compose(hand_mask(), fill=GLOVE_FILL, border=BLACK)
    gd2 = ImageDraw.Draw(glove)
    for gx, gy0, gy1 in [(117, 54, 106), (151, 46, 102), (185, 60, 100)]:
        gd2.line([(gx, gy0), (gx, gy1)], fill=(20, 20, 22, 255), width=5)
    save_cur(glove, "Hand.cur", (104, 60))

    # Pin
    m, d = new_mask()
    d.ellipse([76, 36, 180, 140], fill=255)
    d.polygon([(82, 92), (174, 92), (128, 224)], fill=255)
    pin = compose(m)
    pd = ImageDraw.Draw(pin)
    pd.ellipse([106, 66, 150, 110], fill=(245, 245, 250, 255))
    save_cur(pin, "Pin.cur", (128, 224))

    # Person
    m, d = new_mask()
    d.ellipse([98, 36, 158, 96], fill=255)
    d.pieslice([64, 92, 192, 220], 180, 360, fill=255)
    d.rectangle([64, 156, 192, 158], fill=255)
    save_cur(compose(m), "Person.cur", (128, 128))

    print("done ->", OUT)


if __name__ == "__main__":
    build()
