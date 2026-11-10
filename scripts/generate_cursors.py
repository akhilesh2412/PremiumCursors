"""
Pro Premium Cursors — generator
Draws a full premium Windows cursor scheme (17 roles) at 256px master size
with a dark-navy glass fill, white border and cyan glow, then exports:
  .cur  (multi-size 32+48, PNG-compressed entries) for static cursors
  .ani  (12-frame rotating spinner) for Wait + AppStarting
Run:  pip install pillow && python scripts/generate_cursors.py
Out:  ../cursors/
"""
import io, os, struct
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "cursors")
os.makedirs(OUT, exist_ok=True)

S = 256  # master canvas
ACCENT = (56, 189, 248, 255)      # cyan
ACCENT2 = (99, 102, 241, 255)     # indigo
WHITE = (255, 255, 255, 255)

# Aurora premium gradient stops (diagonal): sky -> indigo -> violet
STOPS = [(0.0, (14, 165, 233)), (0.45, (99, 102, 241)), (0.75, (139, 92, 246)), (1.0, (217, 70, 239))]


def _lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def _stop_color(t):
    for i in range(len(STOPS) - 1):
        if STOPS[i][0] <= t <= STOPS[i + 1][0]:
            a, b = STOPS[i], STOPS[i + 1]
            return _lerp(a[1], b[1], (t - a[0]) / (b[0] - a[0]))
    return STOPS[-1][1]


def gradient():
    g = Image.new("RGBA", (S, S))
    px = g.load()
    for y in range(S):
        for x in range(S):
            px[x, y] = _stop_color((x + y) / (2 * (S - 1))) + (255,)
    return g


GRAD = gradient()


def _smooth(mask):
    """Round the corners of a silhouette: blur then re-threshold."""
    return mask.filter(ImageFilter.GaussianBlur(3)).point(lambda v: 255 if v > 110 else 0)


def compose(mask, glow=True):
    """mask: L silhouette -> PREMIUM v2 styled cursor:
    soft drop shadow + cyan glow + white border + cyan inner ring +
    aurora gradient fill + top gloss + bottom shade."""
    m = _smooth(mask)
    dil = m.filter(ImageFilter.MaxFilter(17))             # outer border silhouette
    ring = m.filter(ImageFilter.MaxFilter(7))              # inner ring silhouette
    out = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    # drop shadow (offset, blurred black silhouette)
    shadow = Image.new("RGBA", (S, S), (0, 0, 0, 255))
    out.paste(shadow, (9, 12), dil.filter(ImageFilter.GaussianBlur(7)))
    if glow:
        glow_img = Image.new("RGBA", (S, S), (56, 130, 246, 255))
        out.paste(glow_img, (0, 0), dil.filter(ImageFilter.GaussianBlur(12)))
    out.paste(Image.new("RGBA", (S, S), WHITE), (0, 0), dil)          # white border
    out.paste(Image.new("RGBA", (S, S), (34, 211, 238, 255)), (0, 0), ring)  # cyan inner ring
    out.paste(GRAD, (0, 0), m)                                        # aurora fill
    # bottom shade for depth
    shade = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    spx = shade.load()
    for y in range(S):
        a = int(70 * max(0.0, (y / S - 0.45) / 0.55))
        for x in range(S):
            spx[x, y] = (0, 0, 10, a)
    shade.putalpha(Image.composite(shade.split()[3], Image.new("L", (S, S), 0), m))
    out.alpha_composite(shade)
    # top gloss (soft diagonal light)
    gloss = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    gd = ImageDraw.Draw(gloss)
    gd.polygon([(0, 0), (S, 0), (0, int(S * 0.62))], fill=(255, 255, 255, 110))
    gloss = gloss.filter(ImageFilter.GaussianBlur(14))
    gloss.putalpha(Image.composite(gloss.split()[3], Image.new("L", (S, S), 0), m))
    out.alpha_composite(gloss)
    return out


def mask_of(draw_fn):
    m = Image.new("L", (S, S), 0)
    draw_fn(ImageDraw.Draw(m))
    return m


ARROW = [(55, 22), (55, 214), (103, 164), (134, 236), (166, 221), (135, 148), (198, 148)]


def d_arrow(d, pts=ARROW):
    d.polygon(pts, fill=255)


def scaled(pts, k, dx=0, dy=0):
    return [(x * k + dx, y * k + dy) for x, y in pts]


# ---------------- silhouettes ----------------
def m_arrow():
    return mask_of(d_arrow)


def m_help():
    def f(d):
        d.polygon(scaled(ARROW, 0.76, -6, -4), fill=255)
        d.ellipse([140, 140, 240, 240], fill=255)
    return mask_of(f)


def m_crosshair():
    def f(d):
        d.ellipse([66, 66, 190, 190], outline=255, width=16)
        d.rectangle([121, 14, 135, 74], fill=255)
        d.rectangle([121, 182, 135, 242], fill=255)
        d.rectangle([14, 121, 74, 135], fill=255)
        d.rectangle([182, 121, 242, 135], fill=255)
        d.ellipse([120, 120, 136, 136], fill=255)
    return mask_of(f)


def m_ibeam():
    return mask_of(lambda d: d.polygon(
        [(70, 35), (186, 35), (186, 64), (142, 64), (142, 192), (186, 192),
         (186, 221), (70, 221), (70, 192), (114, 192), (114, 64), (70, 64)], fill=255))


def m_pen():
    def f(d):
        d.polygon([(78, 138), (168, 48), (196, 76), (106, 166)], fill=255)   # pencil body
        d.polygon([(78, 138), (106, 166), (60, 184)], fill=255)               # tip
        d.polygon([(168, 48), (188, 30), (206, 48), (196, 76)], fill=255)    # eraser end
    return mask_of(f)


def m_no():
    def f(d):
        d.ellipse([38, 38, 218, 218], outline=255, width=30)
        d.line([(66, 190), (190, 66)], fill=255, width=30)
    return mask_of(f)


def m_size_ns():
    return mask_of(lambda d: d.polygon(
        [(128, 18), (178, 80), (150, 80), (150, 176), (178, 176), (128, 238),
         (78, 176), (106, 176), (106, 80), (78, 80)], fill=255))


def m_size_we():
    return mask_of(lambda d: d.polygon(
        [(18, 128), (80, 78), (80, 106), (176, 106), (176, 78), (238, 128),
         (176, 178), (176, 150), (80, 150), (80, 178)], fill=255))


def m_size_nwse():
    def f(d):
        d.line([(62, 62), (194, 194)], fill=255, width=36)
        d.polygon([(22, 22), (102, 22), (22, 102)], fill=255)
        d.polygon([(234, 234), (154, 234), (234, 154)], fill=255)
    return mask_of(f)


def m_size_nesw():
    def f(d):
        d.line([(194, 62), (62, 194)], fill=255, width=36)
        d.polygon([(234, 22), (154, 22), (234, 102)], fill=255)
        d.polygon([(22, 234), (102, 234), (22, 154)], fill=255)
    return mask_of(f)


def m_size_all():
    # classic 4-way move arrow as ONE simple outline polygon (no self-intersections)
    pts = [(128, 15), (166, 62), (144, 62), (144, 112), (194, 112), (241, 128),
           (194, 144), (144, 144), (144, 194), (166, 194), (128, 241), (90, 194),
           (112, 194), (112, 144), (62, 144), (15, 128), (62, 112), (112, 112),
           (112, 62), (90, 62)]
    return mask_of(lambda d: d.polygon(pts, fill=255))


def m_up_arrow():
    return mask_of(lambda d: d.polygon(
        [(128, 22), (216, 130), (166, 130), (166, 234), (90, 234), (90, 130), (40, 130)], fill=255))


def m_hand():
    def f(d):
        d.rounded_rectangle([98, 26, 140, 152], radius=20, fill=255)      # index finger
        d.rounded_rectangle([142, 66, 178, 152], radius=17, fill=255)     # middle (curled top)
        d.rounded_rectangle([180, 92, 210, 152], radius=14, fill=255)     # ring (curled top)
        d.rounded_rectangle([90, 132, 216, 244], radius=30, fill=255)     # palm
        d.ellipse([52, 138, 122, 208], fill=255)                          # thumb
    return mask_of(f)


def m_pin():
    def f(d):
        d.ellipse([70, 22, 186, 178], fill=255)
        d.polygon([(84, 138), (172, 138), (128, 240)], fill=255)
    return mask_of(f)


def m_person():
    def f(d):
        d.ellipse([98, 26, 158, 86], fill=255)                            # head
        d.ellipse([60, 96, 196, 222], fill=255)                           # shoulders
    return mask_of(f)


# ---------------- export helpers ----------------
def png_bytes(img, size):
    buf = io.BytesIO()
    img.resize((size, size), Image.LANCZOS).save(buf, format="PNG")
    return buf.getvalue()


def write_cur(img, hotspot256, path, sizes=(48, 32)):
    entries, datas = [], []
    offset = 6 + 16 * len(sizes)
    for sz in sizes:
        data = png_bytes(img, sz)
        hx = max(0, min(sz - 1, round(hotspot256[0] * sz / S)))
        hy = max(0, min(sz - 1, round(hotspot256[1] * sz / S)))
        entries.append(struct.pack("<BBBBHHII", sz if sz < 256 else 0, sz if sz < 256 else 0,
                                   0, 0, hx, hy, len(data), offset))
        datas.append(data)
        offset += len(data)
    with open(path, "wb") as f:
        f.write(struct.pack("<HHH", 0, 2, len(sizes)))
        for e in entries:
            f.write(e)
        for d in datas:
            f.write(d)


def cur_bytes_single(img, hotspot256, size=32):
    data = png_bytes(img, size)
    hx = round(hotspot256[0] * size / S)
    hy = round(hotspot256[1] * size / S)
    head = struct.pack("<HHH", 0, 2, 1)
    entry = struct.pack("<BBBBHHII", size, size, 0, 0, hx, hy, len(data), 6 + 16)
    return head + entry + data


def write_ani(frames, hotspot256, path, jif=4):
    """frames: list of RGBA master images. ANI with anih + LIST fram of .cur icons."""
    icons = [cur_bytes_single(fr, hotspot256) for fr in frames]
    anih = struct.pack("<IIIIIIIII", 36, len(frames), len(frames), 32, 32, 32, 1, jif, 1)
    chunks = b"anih" + struct.pack("<I", 36) + anih
    fram = b""
    for ic in icons:
        fram += b"icon" + struct.pack("<I", len(ic)) + ic + (b"\0" if len(ic) % 2 else b"")
    chunks += b"LIST" + struct.pack("<I", 4 + len(fram)) + b"fram" + fram
    with open(path, "wb") as f:
        f.write(b"RIFF" + struct.pack("<I", 4 + len(chunks)) + b"ACON" + chunks)


def spinner_frame(step, total=12, center=(128, 128), radius=74, arrow_img=None):
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    if arrow_img is not None:
        img.alpha_composite(arrow_img)
    cx, cy = center
    box = [cx - radius, cy - radius, cx + radius, cy + radius]
    # glow layer (blurred arcs) + sharp gradient arcs on top
    for layer, blur, width in [("glow", 8, 26), ("sharp", 0, 20)]:
        seg = Image.new("RGBA", (S, S), (0, 0, 0, 0))
        d = ImageDraw.Draw(seg)
        for k in range(8):
            a0 = step * (360 / total) + k * 42 - 90
            fade = 1 - k / 9
            base = _stop_color(((a0 % 360) / 360 + step / total) % 1.0)
            col = base + (int(255 * fade),)
            d.arc(box, start=a0, end=a0 + 27, fill=col, width=width)
        d.ellipse([cx - 11, cy - 11, cx + 11, cy + 11], fill=(255, 255, 255, 255))
        if blur:
            seg = seg.filter(ImageFilter.GaussianBlur(blur))
        img.alpha_composite(seg)
    return img


def font(sz):
    for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
              r"C:\Windows\Fonts\arialbd.ttf"]:
        if os.path.exists(p):
            return ImageFont.truetype(p, sz)
    return ImageFont.load_default()


# ---------------- build the set ----------------
def build():
    static = [
        ("Arrow.cur",    m_arrow(),    (55, 22)),
        ("Crosshair.cur", m_crosshair(), (128, 128)),
        ("IBeam.cur",    m_ibeam(),    (128, 128)),
        ("NWPen.cur",    m_pen(),      (60, 184)),
        ("No.cur",       m_no(),       (128, 128)),
        ("SizeNS.cur",   m_size_ns(),  (128, 128)),
        ("SizeWE.cur",   m_size_we(),  (128, 128)),
        ("SizeNWSE.cur", m_size_nwse(), (128, 128)),
        ("SizeNESW.cur", m_size_nesw(), (128, 128)),
        ("SizeAll.cur",  m_size_all(), (128, 128)),
        ("UpArrow.cur",  m_up_arrow(), (128, 22)),
        ("Hand.cur",     m_hand(),     (119, 26)),
        ("Pin.cur",      m_pin(),      (128, 240)),
        ("Person.cur",   m_person(),   (128, 56)),
    ]
    masters = {}
    for name, mask, hot in static:
        img = compose(mask)
        masters[name] = (img, hot)
        write_cur(img, hot, os.path.join(OUT, name))
        print("cur:", name)

    # Help = arrow + accent ? badge (badge drawn on top of styled arrow)
    help_img = compose(mask_of(lambda d: d.polygon(scaled(ARROW, 0.76, -6, -4), fill=255)))
    hd = ImageDraw.Draw(help_img)
    hd.ellipse([138, 138, 242, 242], fill=ACCENT2, outline=WHITE, width=6)
    hd.text((172, 152), "?", font=font(74), fill=WHITE)
    write_cur(help_img, (48, 18), os.path.join(OUT, "Help.cur"))
    masters["Help.cur"] = (help_img, (48, 18))
    print("cur: Help.cur")

    # Pin hole detail
    pin_img, pin_hot = masters["Pin.cur"]
    pd = ImageDraw.Draw(pin_img)
    pd.ellipse([104, 62, 152, 110], fill=(11, 18, 32, 255), outline=ACCENT, width=6)
    write_cur(pin_img, pin_hot, os.path.join(OUT, "Pin.cur"))

    # Wait.ani — pure spinner
    frames = [spinner_frame(i) for i in range(12)]
    write_ani(frames, (128, 128), os.path.join(OUT, "Wait.ani"))
    print("ani: Wait.ani")

    # AppStarting.ani — small arrow + mini spinner bottom-right
    small_arrow = compose(mask_of(lambda d: d.polygon(scaled(ARROW, 0.72, -8, -6), fill=255)))
    frames = [spinner_frame(i, center=(178, 182), radius=46, arrow_img=small_arrow) for i in range(12)]
    write_ani(frames, (44, 18), os.path.join(OUT, "AppStarting.ani"))
    print("ani: AppStarting.ani")
    return masters


if __name__ == "__main__":
    build()
    print("done ->", OUT)
