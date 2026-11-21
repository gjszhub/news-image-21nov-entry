#!/usr/bin/env python3
"""Draw the 21 November 2026 world-news front page (1024x1024 PNG).

Stories (all 21 Nov 2026, from the build brief):
  1. Poland — Russian missile + jet drone land in Poland
  2. COP31 — UN climate talks in Antalya run into overtime
  3. Berlin — Coalition of the Willing; EU agrees EUR 90bn for Ukraine
  4. Sport — Alcaraz sweeps his ATP Finals group in Turin
Footer index: JPMorgan/Visa/Mastercard cyberattack, Hyundai 2027 Elantra,
Mongolian president resigns, France calls urgent UN Security Council meeting.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 231)
CARD = (255, 253, 246)
INK = (26, 26, 26)
MUTED = (90, 84, 70)
RULE = (60, 54, 44)
RED = (155, 27, 27)
BORDER = (207, 198, 174)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_TITLE = font("DejaVuSans-Bold.ttf", 62)
F_DATE = font("DejaVuSans-Bold.ttf", 27)
F_KICK = font("DejaVuSans-Bold.ttf", 15)
F_HEAD = font("DejaVuSans-Bold.ttf", 26)
F_BODY = font("DejaVuSans.ttf", 18)
F_FOOT_LBL = font("DejaVuSans-Bold.ttf", 18)
F_FOOT = font("DejaVuSans.ttf", 16)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def star(draw, cx, cy, r, fill):
    import math
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rad = r if i % 2 == 0 else r * 0.42
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    draw.polygon(pts, fill=fill)


def art_poland():
    img = Image.new("RGB", (476, 180), (22, 35, 63))
    d = ImageDraw.Draw(img)
    # stars
    for (x, y, r) in [(40, 30, 2), (120, 55, 2), (200, 25, 3), (300, 40, 2),
                      (380, 28, 2), (440, 60, 3), (90, 90, 2), (250, 70, 2)]:
        d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255))
    # missile trail arc
    d.arc([60, -120, 560, 220], start=200, end=330, fill=(255, 255, 255), width=6)
    d.arc([60, -120, 560, 220], start=235, end=330, fill=(255, 176, 66), width=10)
    # missile flame + body
    d.ellipse([392, 78, 416, 102], fill=(255, 140, 40))
    d.ellipse([398, 84, 410, 96], fill=(255, 220, 120))
    d.polygon([(416, 84), (446, 90), (416, 96)], fill=(200, 200, 200))
    # jets (small silhouettes)
    d.polygon([(150, 130), (176, 136), (150, 142), (158, 136)], fill=(120, 130, 150))
    d.polygon([(300, 118), (326, 124), (300, 130), (308, 124)], fill=(120, 130, 150))
    # Polish flag band at the bottom
    d.rectangle([0, 148, 476, 164], fill=(255, 255, 255))
    d.rectangle([0, 164, 476, 180], fill=(220, 20, 60))
    return img


def art_cop31():
    img = Image.new("RGB", (476, 180), (250, 214, 150))
    d = ImageDraw.Draw(img)
    # warm sky gradient
    for y in range(120):
        t = y / 120.0
        r = int(250 - 30 * t)
        g = int(214 - 60 * t)
        b = int(150 - 20 * t)
        d.line([(0, y), (476, y)], fill=(r, g, b))
    # sun
    d.ellipse([330, 18, 420, 108], fill=(255, 196, 0))
    d.ellipse([352, 40, 398, 86], fill=(255, 220, 90))
    # sea bands
    d.rectangle([0, 120, 476, 140], fill=(23, 120, 130))
    d.rectangle([0, 140, 476, 160], fill=(16, 96, 110))
    d.rectangle([0, 160, 476, 180], fill=(12, 78, 92))
    # wave arcs
    for y, x0 in [(128, 20), (148, 120), (168, 60)]:
        d.arc([x0, y - 8, x0 + 90, y + 8], start=200, end=340, fill=(255, 255, 255), width=3)
    # green leaf sprout (rotated ellipse leaf + stem)
    leaf = Image.new("RGBA", (90, 60), (0, 0, 0, 0))
    ld = ImageDraw.Draw(leaf)
    ld.ellipse([6, 8, 84, 52], fill=(46, 125, 50, 255))
    ld.line([(10, 52), (80, 10)], fill=(34, 90, 40, 255), width=3)
    leaf = leaf.rotate(38, resample=Image.BICUBIC, expand=False)
    img.paste(leaf, (58, 92), leaf)
    d.line([(104, 150), (104, 118)], fill=(34, 90, 40), width=4)
    return img


def art_berlin():
    img = Image.new("RGB", (476, 180), (0, 51, 153))
    d = ImageDraw.Draw(img)
    # circle of EU stars
    import math
    for i in range(12):
        ang = -math.pi / 2 + i * math.pi / 6
        x = 238 + 74 * math.cos(ang)
        y = 88 + 74 * math.sin(ang)
        star(d, x, y, 9, (255, 204, 0))
    # Brandenburg Gate silhouette (dark)
    gate = (16, 20, 34)
    d.rectangle([168, 150, 308, 164], fill=gate)          # platform
    for cx in (180, 204, 228, 252, 276, 300):
        d.rectangle([cx - 6, 96, cx + 6, 150], fill=gate)  # columns
    d.rectangle([168, 82, 308, 96], fill=gate)            # entablature
    d.rectangle([216, 66, 260, 82], fill=gate)            # quadriga base
    d.ellipse([228, 52, 248, 70], fill=gate)              # quadriga hint
    d.rectangle([0, 164, 476, 180], fill=(0, 40, 120))    # ground shadow
    return img


def art_tennis():
    img = Image.new("RGB", (476, 180), (32, 86, 140))
    d = ImageDraw.Draw(img)
    # court
    d.rectangle([48, 22, 428, 158], fill=(58, 125, 68))
    d.rectangle([48, 22, 428, 158], outline=(255, 255, 255), width=3)
    d.line([(48, 90), (428, 90)], fill=(255, 255, 255), width=3)   # net
    d.line([(238, 22), (238, 158)], fill=(255, 255, 255), width=2)  # centre line
    d.line([(120, 22), (120, 158)], fill=(255, 255, 255), width=2)  # service lines
    d.line([(356, 22), (356, 158)], fill=(255, 255, 255), width=2)
    d.rectangle([48, 86, 428, 94], fill=(240, 240, 240))             # net band
    # ball
    d.ellipse([330, 118, 366, 154], fill=(204, 255, 0))
    d.arc([332, 120, 364, 152], start=40, end=200, fill=(255, 255, 255), width=3)
    d.arc([332, 120, 364, 152], start=220, end=20, fill=(255, 255, 255), width=3)
    return img


STORIES = [
    ("POLAND", (155, 27, 27), art_poland,
     "Missiles land in Poland",
     "Kh-101 down at Nowy Lipowiec, a second near Rudnik nad Sanem, "
     "jet drone at Molodycz. No injuries. Tusk: \u201cintentional "
     "provocation\u201d."),
    ("CLIMATE", (23, 110, 90), art_cop31,
     "Climate talks run overtime",
     "UN talks in Antalya stretch past Friday; the draft deal drops "
     "all fossil-fuel mentions. Panama threatens a veto."),
    ("UKRAINE", (0, 51, 153), art_berlin,
     "\u20ac90bn agreed for Ukraine",
     "Zelensky joins the Coalition of the Willing in Berlin. The EU "
     "agrees \u20ac90bn for Kyiv to end-2027, plus \u20ac70bn NATO aid."),
    ("SPORT", (46, 125, 50), art_tennis,
     "Alcaraz sweeps ATP group",
     "Carlos Alcaraz wins all three group matches at the ATP Finals "
     "in Turin, reaching the semi-finals unbeaten."),
]

FOOTER = [
    "JPMorgan, Visa and Mastercard report a cyberattack on third-party vendors; core networks unaffected.",
    "Hyundai unveils the 2027 Elantra at the LA Auto Show.",
    "Mongolia\u2019s president resigns; a snap election is ahead.",
    "France calls an urgent UN Security Council meeting over the Kyiv strikes.",
]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # outer border
    d.rectangle([10, 10, W - 11, H - 11], outline=INK, width=3)
    # header
    title = "WORLD NEWS"
    d.text(((W - d.textlength(title, font=F_TITLE)) / 2, 30), title, font=F_TITLE, fill=INK)
    date = "SATURDAY 21 NOVEMBER 2026"
    d.text(((W - d.textlength(date, font=F_DATE)) / 2, 104), date, font=F_DATE, fill=RED)
    d.line([(24, 142), (W - 24, 142)], fill=RULE, width=3)
    d.line([(24, 148), (W - 24, 148)], fill=RULE, width=1)

    # 2x2 grid
    cell_w, cell_h, gap, ox, oy = 476, 348, 12, 24, 158
    for i, (kick, accent, art_fn, head, body) in enumerate(STORIES):
        x0 = ox + (i % 2) * (cell_w + gap)
        y0 = oy + (i // 2) * (cell_h + gap)
        d.rectangle([x0, y0, x0 + cell_w - 1, y0 + cell_h - 1], fill=CARD, outline=BORDER, width=1)
        img.paste(art_fn(), (x0 + 1, y0 + 1))
        d.text((x0 + 14, y0 + 192), kick, font=F_KICK, fill=accent)
        head_lines = wrap(d, head, F_HEAD, cell_w - 28)
        hy = y0 + 214
        for ln in head_lines[:2]:
            d.text((x0 + 14, hy), ln, font=F_HEAD, fill=INK)
            hy += 30
        by = hy + 6
        for ln in wrap(d, body, F_BODY, cell_w - 28)[:3]:
            d.text((x0 + 14, by), ln, font=F_BODY, fill=(40, 38, 34))
            by += 23

    # footer
    fy = 878
    d.text((24, fy), "ALSO TODAY", font=F_FOOT_LBL, fill=INK)
    d.line([(24, fy + 26), (W - 24, fy + 26)], fill=RULE, width=2)
    col_w = 476
    for i, item in enumerate(FOOTER):
        cx = 24 + (i % 2) * (col_w + 12)
        cy = fy + 38 + (i // 2) * 52
        lines = wrap(d, item, F_FOOT, col_w - 18)
        ly = cy
        for j, ln in enumerate(lines[:2]):
            prefix = "\u2022  " if j == 0 else "     "
            d.text((cx, ly), prefix + ln, font=F_FOOT, fill=MUTED)
            ly += 21

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
