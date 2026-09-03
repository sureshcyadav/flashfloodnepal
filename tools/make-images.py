# -*- coding: utf-8 -*-
"""Regenerate the social images and favicons for flashfloodnepal.com.

    pip install pillow
    python tools/make-images.py

Downloads the Archivo TTFs from Google Fonts on first run (SIL Open Font
Licence) into tools/.fonts, which is gitignored. Palette and geometry mirror
the hero illustration in index.html.

Outputs
    og.png              1200x630   Facebook / LinkedIn / X / Slack link card
    og-instagram.png    1080x1350  Instagram feed, 4:5 portrait
    og-story.png        1080x1920  Instagram / Facebook story, 9:16
    favicon.svg, favicon.ico, favicon-32.png, apple-touch-icon.png

The Instagram images carry the domain as printed text because Instagram does
not make links in captions clickable - readers have to be able to read the
address off the picture.
"""
import io, os, urllib.request
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.dirname(HERE)
FONT = os.path.join(HERE, ".fonts")

_TTF = {
    700: "k3k6o8UDI-1M0wlSV9XAw6lQkqWY8Q82sJaRE-NWIDdgffTT0zRp8A.ttf",
    800: "k3k6o8UDI-1M0wlSV9XAw6lQkqWY8Q82sJaRE-NWIDdgffTTtDRp8A.ttf",
    900: "k3k6o8UDI-1M0wlSV9XAw6lQkqWY8Q82sJaRE-NWIDdgffTTnTRp8A.ttf",
}

def _ensure_fonts():
    if not os.path.isdir(FONT):
        os.makedirs(FONT)
    for w, name in _TTF.items():
        p = os.path.join(FONT, "archivo-%d.ttf" % w)
        if not os.path.exists(p):
            print("fetching Archivo %d ..." % w)
            urllib.request.urlretrieve(
                "https://fonts.gstatic.com/s/archivo/v25/" + name, p)

_ensure_fonts()

def f(weight, size):
    return ImageFont.truetype(os.path.join(FONT, "archivo-%d.ttf" % weight), size)

def hx(c):
    c = c.lstrip("#")
    return tuple(int(c[i:i+2], 16) for i in (0, 2, 4))

# ---------------------------------------------------------------- palette
DEEP = hx("0C161C"); RED2 = hx("CF5A4E"); RED3 = hx("F0A79E")
ICE  = hx("BFDCE6"); PALE = hx("E8F2F5")
DEK  = hx("CBDADE"); MUTE = hx("8FA6AF"); RULE = hx("2A3E47")
WHITE = hx("F4F8F8")

FAR = [(0,318),(92,252),(152,284),(232,186),(302,244),(384,152),(470,232),(542,196),
       (622,116),(704,206),(784,170),(862,238),(952,180),(1042,252),(1122,206),
       (1212,266),(1302,220),(1382,270),(1440,246)]
MID = [(0,392),(84,338),(172,370),(254,306),(344,352),(432,290),(524,338),(612,272),
       (702,328),(792,296),(882,346),(982,306),(1072,356),(1162,320),(1262,366),
       (1352,330),(1440,372)]
NEAR= [(0,466),(124,420),(246,452),(368,402),(492,446),(616,392),(742,436),(866,408),
       (990,450),(1112,414),(1238,456),(1352,424),(1440,462)]

STATS = [("1,114", "DEAD"), ("3,916", "MISSING"),
         ("0.04%", "OF GLOBAL CO₂"), ("$5 BN", "TO REBUILD")]
DOMAIN = "flashfloodnepal.com"

def blend(c, o, k):
    return tuple(int(c[i] + (o[i] - c[i]) * k) for i in range(3))

def vgrad(img, stops, y0, y1):
    d = ImageDraw.Draw(img)
    span = max(1, y1 - y0)
    for y in range(y0, y1):
        t = (y - y0) / float(span)
        for i in range(len(stops) - 1):
            a, ca = stops[i]; b, cb = stops[i + 1]
            if a <= t <= b:
                k = (t - a) / max(1e-6, (b - a))
                d.line([(0, y), (img.width, y)],
                       fill=tuple(int(ca[j] + (cb[j] - ca[j]) * k) for j in range(3)))
                break

def scene(W, H, sx, sy, oy, scrim_at, scrim_span, sky_to=0.78):
    """sky, three ranges, snow and the collapse marker; shared by all formats"""
    def sc(x, y):
        return (x * sx, y * sy + oy)
    def poly(seq):
        return [sc(x, y) for x, y in seq] + [(W, H), (0, H)]

    img = Image.new("RGB", (W, H), DEEP)
    vgrad(img, [(0.0, hx("0A1319")), (0.45, hx("16303C")),
                (0.78, hx("2C5567")), (1.0, hx("4A7789"))], 0, int(H * sky_to))
    d = ImageDraw.Draw(img, "RGBA")
    d.polygon(poly(FAR), fill=blend(hx("9FC0CE"), hx("6E97A8"), .5) + (170,))
    d.polygon([sc(622,116),sc(660,158),sc(640,152),
               sc(622,164),sc(604,150),sc(586,157)], fill=PALE + (205,))
    d.polygon([sc(384,152),sc(414,186),sc(398,180),
               sc(384,190),sc(368,178),sc(352,184)], fill=PALE + (140,))
    d.polygon(poly(MID), fill=blend(hx("5B8496"), hx("3A6272"), .5) + (230,))
    d.polygon([sc(612,276),sc(648,340),sc(672,410),sc(648,412),
               sc(620,344),sc(596,404),sc(574,402),sc(594,336)], fill=ICE + (128,))
    d.polygon(poly(NEAR), fill=blend(hx("243F4B"), hx("101E26"), .5) + (255,))

    mx, my = sc(622, 116)
    r = max(9, int(W * 0.0225))
    d.ellipse([mx-r, my-r, mx+r, my+r], outline=RED2 + (110,), width=2)
    d.ellipse([mx-r*.48, my-r*.48, mx+r*.48, my+r*.48], outline=RED2 + (255,), width=2)
    d.ellipse([mx-r*.13, my-r*.13, mx+r*.13, my+r*.13], fill=RED2)

    scrim = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(scrim)
    for y in range(scrim_at, H):
        a = int(250 * min(1.0, (y - scrim_at) / float(scrim_span)) ** 1.25)
        sd.line([(0, y), (W, y)], fill=DEEP + (a,))
    img = Image.alpha_composite(img.convert("RGBA"), scrim).convert("RGB")
    return img, (mx, my)

def kicker(d, x, y, size):
    d.text((x, y), "SPECIAL REPORT", font=f(800, size), fill=RED3)
    w = d.textlength("SPECIAL REPORT", font=f(800, size))
    d.text((x + w + size * .8, y), "CLIMATE AND RESPONSIBILITY",
           font=f(700, size), fill=MUTE)

def fit(d, text, weight, start, maxw, floor=40):
    s = start
    while d.textlength(text, font=f(weight, s)) > maxw and s > floor:
        s -= 2
    return s

# ================================================================ 1200x630
def og():
    W, H = 1200, 630
    img, (mx, my) = scene(W, H, W / 1440.0, 0.86, 30, 210, 240)
    d = ImageDraw.Draw(img)
    PAD = 72
    kicker(d, PAD, 54, 22)
    d.line([(mx + 27, my), (mx + 86, my)], fill=RED2, width=2)
    d.text((mx + 96, my - 19), "08:37, 26 AUGUST 2026", font=f(800, 20), fill=RED3)
    d.text((mx + 96, my + 3), "ice and rock leave the mountain", font=f(700, 17), fill=MUTE)

    t = "The mountain that fell"
    d.text((PAD, 322), t, font=f(900, fit(d, t, 900, 92, W - PAD * 2)), fill=WHITE)
    for i, line in enumerate([
        "Nepal produces four hundredths of one percent of the world's carbon",
        "dioxide. In August, a Himalayan glacier collapsed and killed a thousand",
        "of its people. This is the arithmetic of that sentence."]):
        d.text((PAD, 440 + i * 38), line, font=f(700, 27), fill=DEK)
    d.line([(PAD, 562), (W - PAD, 562)], fill=RULE, width=1)
    x = PAD
    for val, lab in STATS:
        d.text((x, 583), val, font=f(900, 23), fill=RED3)
        vw = d.textlength(val, font=f(900, 23))
        d.text((x + vw + 9, 586), lab, font=f(700, 19), fill=MUTE)
        x += vw + d.textlength(lab, font=f(700, 19)) + 46
    return img

# =============================================================== 1080x1350
def feed():
    W, H = 1080, 1350
    img, (mx, my) = scene(W, H, W / 1440.0, 0.92, 46, 400, 300, sky_to=0.55)
    d = ImageDraw.Draw(img)
    PAD = 76
    kicker(d, PAD, 66, 26)
    d.line([(mx + 26, my), (mx + 70, my)], fill=RED2, width=2)
    d.text((mx + 80, my - 11), "08:37, 26 AUG 2026", font=f(800, 21), fill=RED3)

    for i, line in enumerate(["The mountain", "that fell"]):
        d.text((PAD, 612 + i * 116), line, font=f(900, 108), fill=WHITE)
    for i, line in enumerate([
        "Nepal produces four hundredths of one percent",
        "of the world's carbon dioxide. In August, a",
        "Himalayan glacier collapsed and killed a",
        "thousand of its people."]):
        d.text((PAD, 878 + i * 42), line, font=f(700, 30), fill=DEK)

    d.line([(PAD, 1058), (W - PAD, 1058)], fill=RULE, width=1)
    for i, (val, lab) in enumerate(STATS):
        cx = PAD + (i % 2) * 486
        cy = 1090 + (i // 2) * 62
        d.text((cx, cy), val, font=f(900, 30), fill=RED3)
        vw = d.textlength(val, font=f(900, 30))
        d.text((cx + vw + 11, cy + 6), lab, font=f(700, 21), fill=MUTE)

    d.text((PAD, 1240), DOMAIN, font=f(900, 46), fill=WHITE)
    dw = d.textlength(DOMAIN, font=f(900, 46))
    d.text((PAD + dw + 18, 1256), "FULL REPORT", font=f(800, 22), fill=RED3)
    return img

# =============================================================== 1080x1920
def story():
    W, H = 1080, 1920
    # top ~250px and bottom ~320px are covered by Instagram's own chrome
    img, (mx, my) = scene(W, H, W / 1440.0, 1.02, 250, 700, 340, sky_to=0.42)
    d = ImageDraw.Draw(img)
    PAD = 80
    kicker(d, PAD, 300, 26)
    d.line([(mx + 26, my), (mx + 70, my)], fill=RED2, width=2)
    d.text((mx + 80, my - 11), "08:37, 26 AUG 2026", font=f(800, 21), fill=RED3)

    for i, line in enumerate(["The mountain", "that fell"]):
        d.text((PAD, 940 + i * 118), line, font=f(900, 110), fill=WHITE)
    for i, line in enumerate([
        "Nepal produces four hundredths of one percent",
        "of the world's carbon dioxide. In August, a",
        "Himalayan glacier collapsed and killed a",
        "thousand of its people."]):
        d.text((PAD, 1216 + i * 44), line, font=f(700, 31), fill=DEK)

    d.line([(PAD, 1414), (W - PAD, 1414)], fill=RULE, width=1)
    for i, (val, lab) in enumerate(STATS):
        cx = PAD + (i % 2) * 470
        cy = 1446 + (i // 2) * 60
        d.text((cx, cy), val, font=f(900, 29), fill=RED3)
        vw = d.textlength(val, font=f(900, 29))
        d.text((cx + vw + 10, cy + 6), lab, font=f(700, 20), fill=MUTE)

    d.text((PAD, 1592), DOMAIN, font=f(900, 44), fill=WHITE)
    # 1660-1810 deliberately left empty for the link sticker
    return img

# ================================================================ FAVICON
def icon(px):
    S = px * 8
    img = Image.new("RGB", (S, S), DEEP)
    d = ImageDraw.Draw(img)
    u = S / 64.0
    d.polygon([(4*u, 54*u), (24*u, 20*u), (40*u, 54*u)], fill=hx("6E97A8"))
    d.polygon([(26*u, 52*u), (46*u, 14*u), (62*u, 52*u)], fill=ICE)
    d.polygon([(40*u, 32*u), (46*u, 14*u), (52*u, 32*u)], fill=PALE)
    d.rectangle([0, 54*u, S, S], fill=hx("101E26"))
    d.ellipse([41*u, 9*u, 51*u, 19*u], fill=DEEP)
    d.ellipse([43*u, 11*u, 49*u, 17*u], fill=RED2)
    return img.resize((px, px), Image.LANCZOS)

FAVICON_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
  <rect width="64" height="64" fill="#0C161C"/>
  <path d="M4 54 L24 20 L40 54 Z" fill="#6E97A8"/>
  <path d="M26 52 L46 14 L62 52 Z" fill="#BFDCE6"/>
  <path d="M40 32 L46 14 L52 32 Z" fill="#E8F2F5"/>
  <rect y="54" width="64" height="10" fill="#101E26"/>
  <circle cx="46" cy="14" r="5" fill="#0C161C"/>
  <circle cx="46" cy="14" r="3" fill="#CF5A4E"/>
</svg>
"""

if __name__ == "__main__":
    for name, fn in (("og.png", og), ("og-instagram.png", feed), ("og-story.png", story)):
        im = fn()
        im.save(os.path.join(OUT, name), "PNG", optimize=True)
        print("%-20s %dx%-10s %d bytes" % (
            name, im.width, im.height, os.path.getsize(os.path.join(OUT, name))))

    icon(180).save(os.path.join(OUT, "apple-touch-icon.png"), "PNG", optimize=True)
    icon(32).save(os.path.join(OUT, "favicon-32.png"), "PNG", optimize=True)
    icon(64).save(os.path.join(OUT, "favicon.ico"), sizes=[(16,16),(32,32),(48,48)])
    with io.open(os.path.join(OUT, "favicon.svg"), "w", encoding="utf-8") as fh:
        fh.write(FAVICON_SVG)
    for n in ("apple-touch-icon.png", "favicon-32.png", "favicon.ico", "favicon.svg"):
        print("%-20s %d bytes" % (n, os.path.getsize(os.path.join(OUT, n))))
