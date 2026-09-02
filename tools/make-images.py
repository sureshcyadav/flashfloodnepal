# -*- coding: utf-8 -*-
"""Regenerate og.png and the favicons for flashfloodnepal.com.

    pip install pillow
    python tools/make-images.py

Downloads the Archivo TTFs from Google Fonts on first run (SIL Open Font
Licence) into tools/.fonts, which is gitignored. Palette and geometry mirror
the hero illustration in index.html."""
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
            url = "https://fonts.gstatic.com/s/archivo/v25/" + name
            print("fetching Archivo %d ..." % w)
            urllib.request.urlretrieve(url, p)

_ensure_fonts()

def f(weight, size):
    return ImageFont.truetype(os.path.join(FONT, "archivo-%d.ttf" % weight), size)

def hx(c):
    c = c.lstrip("#")
    return tuple(int(c[i:i+2], 16) for i in (0, 2, 4))

# ---------------------------------------------------------------- palette
DEEP  = hx("0C161C"); INK = hx("132029")
RED   = hx("A5241C"); RED2 = hx("CF5A4E"); RED3 = hx("F0A79E")
ICE   = hx("BFDCE6"); PALE = hx("E8F2F5")
DEK   = hx("CBDADE"); MUTE = hx("8FA6AF")

W, H = 1200, 630
SX = W / 1440.0          # hero viewBox is 1440 x 560
SY = 0.86
OY = 30                  # drop the range clear of the kicker line

def sc(x, y):
    return (x * SX, y * SY + OY)

def pts(seq, floor=H):
    """scale a hero polyline and close it to the bottom of the canvas"""
    return [sc(x, y) for x, y in seq] + [(W, floor), (0, floor)]

FAR = [(0,318),(92,252),(152,284),(232,186),(302,244),(384,152),(470,232),(542,196),
       (622,116),(704,206),(784,170),(862,238),(952,180),(1042,252),(1122,206),
       (1212,266),(1302,220),(1382,270),(1440,246)]
MID = [(0,392),(84,338),(172,370),(254,306),(344,352),(432,290),(524,338),(612,272),
       (702,328),(792,296),(882,346),(982,306),(1072,356),(1162,320),(1262,366),
       (1352,330),(1440,372)]
NEAR= [(0,466),(124,420),(246,452),(368,402),(492,446),(616,392),(742,436),(866,408),
       (990,450),(1112,414),(1238,456),(1352,424),(1440,462)]

def vgrad(img, stops, y0, y1):
    """paint a vertical gradient between (offset, colour) stops"""
    d = ImageDraw.Draw(img)
    span = max(1, y1 - y0)
    for y in range(y0, y1):
        t = (y - y0) / float(span)
        for i in range(len(stops) - 1):
            a, ca = stops[i]; b, cb = stops[i + 1]
            if a <= t <= b:
                k = (t - a) / max(1e-6, (b - a))
                c = tuple(int(ca[j] + (cb[j] - ca[j]) * k) for j in range(3))
                d.line([(0, y), (img.width, y)], fill=c)
                break

def blend(c, other, k):
    return tuple(int(c[i] + (other[i] - c[i]) * k) for i in range(3))

# ================================================================ OG CARD
def og():
    img = Image.new("RGB", (W, H), DEEP)
    vgrad(img, [(0.0, hx("0A1319")), (0.45, hx("16303C")),
                (0.78, hx("2C5567")), (1.0, hx("4A7789"))], 0, int(H * 0.78))
    d = ImageDraw.Draw(img, "RGBA")

    d.polygon(pts(FAR),  fill=blend(hx("9FC0CE"), hx("6E97A8"), .5) + (170,))
    # snow on the two highest far peaks
    d.polygon([sc(622,116),sc(660,158),sc(640,152),
               sc(622,164),sc(604,150),sc(586,157)], fill=PALE + (205,))
    d.polygon([sc(384,152),sc(414,186),sc(398,180),
               sc(384,190),sc(368,178),sc(352,184)], fill=PALE + (140,))
    d.polygon(pts(MID),  fill=blend(hx("5B8496"), hx("3A6272"), .5) + (230,))
    d.polygon([sc(612,276),sc(648,340),sc(672,410),sc(648,412),
               sc(620,344),sc(596,404),sc(574,402),sc(594,336)], fill=ICE + (128,))
    d.polygon(pts(NEAR), fill=blend(hx("243F4B"), hx("101E26"), .5) + (255,))

    # collapse marker: a thin reticle above the apex, with a leader line to a
    # timestamp, echoing the annotation on the report's hero
    mx, my = sc(622, 116)
    d.ellipse([mx-27, my-27, mx+27, my+27], outline=RED2 + (110,), width=2)
    d.ellipse([mx-13, my-13, mx+13, my+13], outline=RED2 + (255,), width=2)
    d.ellipse([mx-3.5, my-3.5, mx+3.5, my+3.5], fill=RED2)
    d.line([(mx+27, my), (mx+86, my)], fill=RED2, width=2)
    d.text((mx+96, my-19), "08:37, 26 AUGUST 2026", font=f(800, 20), fill=RED3)
    d.text((mx+96, my+3),  "ice and rock leave the mountain", font=f(700, 17), fill=MUTE)

    # legibility scrim behind the type
    scrim = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(scrim)
    for y in range(210, H):
        a = int(250 * min(1.0, (y - 210) / 240.0) ** 1.25)
        sd.line([(0, y), (W, y)], fill=DEEP + (a,))
    img = Image.alpha_composite(img.convert("RGBA"), scrim).convert("RGB")
    d = ImageDraw.Draw(img)

    PAD = 72
    # kicker
    d.text((PAD, 54), "SPECIAL REPORT", font=f(800, 22), fill=RED3)
    kw = d.textlength("SPECIAL REPORT", font=f(800, 22))
    d.text((PAD + kw + 18, 54), "CLIMATE AND RESPONSIBILITY", font=f(700, 22), fill=MUTE)

    # title, shrunk to fit if it ever needs to
    title, size = "The mountain that fell", 92
    while d.textlength(title, font=f(900, size)) > W - PAD * 2 and size > 48:
        size -= 2
    d.text((PAD, 322), title, font=f(900, size), fill=hx("F4F8F8"))

    # standfirst
    for i, line in enumerate([
        "Nepal produces four hundredths of one percent of the world's carbon",
        "dioxide. In August, a Himalayan glacier collapsed and killed a thousand",
        "of its people. This is the arithmetic of that sentence."]):
        d.text((PAD, 440 + i * 38), line, font=f(700, 27), fill=DEK)

    # rule + stat strip, kept clear of the bottom edge
    d.line([(PAD, 562), (W - PAD, 562)], fill=hx("2A3E47"), width=1)
    x = PAD
    for val, lab in [("1,114", "DEAD"), ("3,916", "MISSING"),
                     ("0.04%", "OF GLOBAL CO\u2082"), ("$5 BN", "TO REBUILD")]:
        d.text((x, 583), val, font=f(900, 23), fill=RED3)
        vw = d.textlength(val, font=f(900, 23))
        d.text((x + vw + 9, 586), lab, font=f(700, 19), fill=MUTE)
        x += vw + d.textlength(lab, font=f(700, 19)) + 46
    img.save(os.path.join(OUT, "og.png"), "PNG", optimize=True)
    return img

# ================================================================ FAVICON
def icon(px):
    """mountain + collapse point; readable down to 16px"""
    S = px * 8                                   # supersample
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
    o = og()
    print("og.png           %dx%d  %d bytes" % (o.width, o.height,
          os.path.getsize(os.path.join(OUT, "og.png"))))

    icon(180).save(os.path.join(OUT, "apple-touch-icon.png"), "PNG", optimize=True)
    icon(32).save(os.path.join(OUT, "favicon-32.png"), "PNG", optimize=True)
    icon(64).save(os.path.join(OUT, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)])
    with io.open(os.path.join(OUT, "favicon.svg"), "w", encoding="utf-8") as fh:
        fh.write(FAVICON_SVG)
    for n in ("apple-touch-icon.png", "favicon-32.png", "favicon.ico", "favicon.svg"):
        print("%-22s %d bytes" % (n, os.path.getsize(os.path.join(OUT, n))))
