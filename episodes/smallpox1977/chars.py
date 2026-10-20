"""ตัวละครและพร็อพ: ผู้ป่วยไข้ทรพิษตามธรรมชาติคนสุดท้าย อาลี มาว มาอลิน (26 ต.ค. 1977)
ไม่แสดงอาการแบบน่ากลัว: ตุ่มเป็นจุดเล็ก ๆ แบบการ์ตูน, ไวรัสเป็นการ์ตูนหน้าบึ้ง; ไม่ใช้โลโก้ WHO จริง"""
import math

from gfx import GOLD, GOLD2, GREY, INK, NAVY, RED, WHITE, hexc
from people import Look, _rr, _shade, _smooth_path, _stroke

SKIN_SO = hexc("#6e4a30")
WHO_BLUE = hexc("#3d8fd1")
VIRUS = hexc("#8bbf4a")
SAND = hexc("#ecd9a8")

# อาลี มาว มาอลิน วัย 23: ผมสั้นหยิก ผิวคล้ำ หน้าผอม เสื้อขาวพ่อครัว
ALI = Look(hair="buzz", hair_col=hexc("#1b1714"), outfit="tee", suit=WHITE, pants=hexc("#3a4a6a"), skin=SKIN_SO,
           w=54, jaw=0.35, nose=1.05, brow=0.9, age=0.1, build=0.9)
ALI_OLD = Look(hair="buzz", hair_col=hexc("#3a3632"), outfit="tee", suit=WHO_BLUE, pants=hexc("#3a4a6a"),
               skin=SKIN_SO, w=55, jaw=0.4, nose=1.05, brow=0.9, age=0.55, facial="goatee", build=0.95)
DOCTOR = Look(hair="part", hair_col=hexc("#5a4a3a"), outfit="tee", suit=WHITE, pants=hexc("#5a6a7a"),
              glasses="thin", w=56, age=0.45)
WORKERS = [   # เจ้าหน้าที่ภาคสนาม
    Look(hair="short", hair_col=hexc("#1b1714"), outfit="tee", suit=WHO_BLUE, pants=hexc("#c9b38a"), skin=hexc("#5a3a26"),
         w=55, age=0.3),
    Look(hair="bun", hair_col=hexc("#1b1714"), outfit="dress", suit=hexc("#d76b5a"), skin=hexc("#7a4a2c"), w=54,
         age=0.3, height=0.93),
    Look(hair="part", hair_col=hexc("#8a6a42"), outfit="tee", suit=WHO_BLUE, pants=hexc("#c9b38a"), w=55, age=0.4,
         glasses="thin"),
]
KIDS = [
    Look(hair="buzz", hair_col=hexc("#1b1714"), outfit="tee", suit=hexc("#f2c25c"), pants=hexc("#3a4a6a"),
         skin=hexc("#6e4a30"), w=54, height=0.6, headsc=1.45),
    Look(hair="bun", hair_col=hexc("#1b1714"), outfit="dress", suit=hexc("#8ab4f0"), skin=hexc("#5a3a26"), w=54,
         height=0.58, headsc=1.45),
]


def spots(g, x, y, sc=1.0, k=1.0, n=10):
    """ตุ่มบนหน้า/ตัวแบบการ์ตูน (จุดสีชมพูเล็ก ๆ)"""
    for i in range(int(n * k)):
        a = i * 2.4
        r = 18 + (i * 37) % 26
        g.circle(x + r * math.cos(a) * sc, y + r * math.sin(a) * sc * 1.1, 6.5 * max(sc, 0.8), hexc("#f07a7a"), 2)


def virus(g, x, y, r, t=0.0, mood="angry", col=VIRUS):
    """ไวรัสการ์ตูนหนาม + หน้าบึ้ง"""
    with g.at(x, y, 1, t * 20):
        for i in range(10):
            a = i * math.pi / 5
            g.line([(r * 0.9 * math.cos(a), r * 0.9 * math.sin(a)), (r * 1.3 * math.cos(a), r * 1.3 * math.sin(a))],
                   max(4, r * 0.08), INK, amp=0)
            g.circle(r * 1.35 * math.cos(a), r * 1.35 * math.sin(a), r * 0.13, col, 3)
        g.circle(0, 0, r, col, 6)
    with g.at(x, y):
        for ex in (-1, 1):
            g.circle(ex * r * 0.32, -r * 0.1, r * 0.12, INK, 0)
            if mood == "angry":
                g.line([(ex * r * 0.5, -r * 0.38), (ex * r * 0.15, -r * 0.25)], max(3, r * 0.07), INK, amp=0)
        if mood == "angry":
            g.arc(0, r * 0.45, r * 0.3, 200, 340, max(3, r * 0.07), INK)
        else:
            g.arc(0, r * 0.1, r * 0.3, 20, 160, max(3, r * 0.07), INK)


def syringe(g, x, y, sc=1.0, rot=0.0, fill=1.0):
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -160, -30, 260, 60, 12)
        _shade(c, hexc("#eef6fb"), 6, 0.1)
        if fill > 0:
            _rr(c, -150 + 240 * (1 - fill), -20, 240 * fill, 40, 8)
            _shade(c, WHO_BLUE, 0, 0)
        _rr(c, -200, -12, 50, 24, 4)
        _shade(c, hexc("#c9ced6"), 4, 0)
        _rr(c, -230, -40, 30, 80, 6)
        _shade(c, hexc("#c9ced6"), 4, 0)
        g.line([(100, 0), (190, 0)], 5, INK, amp=0)


def drops(g, x, y, sc=1.0, t=0.0):
    """วัคซีนโปลิโอชนิดหยด"""
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -40, -160, 80, 150, 16)
        _shade(c, hexc("#f2c25c"), 6, 0.2)
        _smooth_path(c, [(-25, -160), (25, -160), (8, -220), (-8, -220)])
        _shade(c, WHITE, 5, 0.1)
        u = (t * 1.2) % 1
        g.poly([(0, -230 + 0), (12, -200), (0, -188), (-12, -200)], WHO_BLUE, 3, amp=0, smooth=True) if u > 2 else None
        with g.at(0, -230 + 160 * u):
            g.poly([(0, -14), (10, 4), (0, 12), (-10, 4)], (*WHO_BLUE[:3], 1 - u), 3, amp=0, smooth=True)


def emblem(g, x, y, r, t=0.0):
    """ตราองค์กรอนามัยแบบการ์ตูน: ลูกโลก + ไม้เท้างูพัน (ไม่ใช่โลโก้จริง)"""
    c = g.c
    c.new_path()
    c.arc(x, y, r, 0, 2 * math.pi)
    _shade(c, WHO_BLUE, 6, 0.2)
    for k in (0.4, 0.75):
        c.new_path()
        c.save()
        c.translate(x, y)
        c.scale(k, 1)
        c.arc(0, 0, r, 0, 2 * math.pi)
        c.restore()
        c.set_source_rgba(1, 1, 1, 0.7)
        c.set_line_width(3)
        c.stroke()
    _stroke(c, [(x - r, y), (x + r, y)], 3, WHITE, 0.7, smooth=False)
    g.line([(x, y - r * 1.1), (x, y + r * 1.1)], 8, INK, amp=0)
    pts = [(x + r * 0.28 * math.sin(i * 0.9 + t), y - r * 0.9 + i * r * 0.18) for i in range(11)]
    g.line(pts, 6, GOLD, amp=0, smooth=True)


def hospital(g, x, y, sc=1.0):
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -280, -360, 560, 360, 6)
        _shade(c, hexc("#f2ece0"), 6, 0.2)
        for r in range(2):
            for k in range(4):
                _rr(c, -230 + k * 125, -320 + r * 130, 80, 80, 6)
                _shade(c, hexc("#9ab8d0"), 4, 0.1)
        _rr(c, -60, -120, 120, 120, 8)
        _shade(c, hexc("#8a6a42"), 4, 0.1)
        _rr(c, -70, -440, 140, 70, 10)
        _shade(c, WHITE, 5, 0)
        _rr(c, -12, -432, 24, 54, 2)
        _shade(c, RED, 0, 0)
        _rr(c, -27, -417, 54, 24, 2)
        _shade(c, RED, 0, 0)


def somalia_map(g, x, y, sc=1.0, t=0.0, pin=1.0):
    """แผนที่จะงอยแอฟริกา (โซมาเลีย) แบบเรียบง่าย + หมุดเมอร์กา"""
    c = g.c
    with g.at(x, y, sc):
        _smooth_path(c, [(-260, -260), (40, -300), (300, -320), (230, -180), (60, 80), (-120, 300), (-200, 260),
                         (-180, 60), (-300, -80)])
        _shade(c, SAND, 6, 0.15)
        _smooth_path(c, [(-60, -250), (280, -305), (215, -185), (50, 70), (-110, 280), (-140, 150), (-20, -80)])
        _shade(c, hexc("#e8c68a"), 4, 0.1)
        if pin > 0.02:
            with g.at(-60, 160, pin):
                g.poly([(0, 0), (-28, -60), (0, -90), (28, -60)], RED, 5, amp=0, smooth=True)
                g.circle(0, -62, 12, WHITE, 0)
            g.label("เมอร์กา", 60, 170, 46, color=RED, sc=pin)


def contact_web(g, x, y, t=0.0, k=1.0, n=161, r=360):
    """เครือข่ายผู้สัมผัสโรค: จุดเล็ก ๆ ขยายออกจากอาลีตรงกลาง"""
    m = int(n * k)
    for i in range(m):
        a = i * 2.39996
        rr = r * math.sqrt((i + 1) / n)
        px, py = x + rr * math.cos(a), y + rr * math.sin(a) * 0.85
        if i < 24:
            g.line([(x, y), (px, py)], 2, (0.6, 0.6, 0.65, 0.6), amp=0)
        g.circle(px, py, 9, hexc("#f2c25c") if i % 4 else hexc("#8ab4f0"), 2)
    g.circle(x, y, 28, RED, 5)


def ring(g, x, y, r, t=0.0, k=1.0, col=WHO_BLUE):
    """วงล้อมฉีดวัคซีน (ล้อมรั้ว) — วงแหวนหมุนเป็นเส้นประ"""
    n = 36
    for i in range(n):
        if i / n > k:
            break
        a0 = i * 360 / n + t * 20
        g.arc(x, y, r, a0, a0 + 360 / n * 0.6, 12, col)


def certificate(g, x, y, sc=1.0, rot=0.0, t=0.0):
    with g.at(x, y, sc, rot):
        g.rrect(-220, -280, 440, 560, 12, hexc("#f4eedf"), 7)
        emblem(g, 0, -170, 60, t)
        g.text("SMALLPOX", 0, -60, 46, "kanit", INK)
        g.text("ERADICATED", 0, 0, 46, "kanit", hexc("#3c8d4f"))
        g.text("1980", 0, 80, 70, "kanit", RED)
        g.circle(130, 200, 50, GOLD, 6)
        g.star(130, 200, 26, WHITE, 0)


def thermometer(g, x, y, sc=1.0, rot=0.0, level=1.0):
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -22, -260, 44, 260, 22)
        _shade(c, WHITE, 6, 0.1)
        _rr(c, -10, -240 + 220 * (1 - level), 20, 220 * level + 10, 10)
        _shade(c, RED, 0, 0)
        c.new_path()
        c.arc(0, 20, 40, 0, 2 * math.pi)
        _shade(c, RED, 6, 0.2)


def skull_scale(g, x, y, sc=1.0, k=1.0):
    """ตัวเลขผู้เสียชีวิตแบบไอคอนคน (ไม่ใช้หัวกะโหลก)"""
    with g.at(x, y, sc):
        for i in range(int(30 * k)):
            px, py = -270 + (i % 10) * 60, -100 + (i // 10) * 90
            g.circle(px, py - 24, 16, GREY, 3)
            g.rrect(px - 20, py - 6, 40, 44, 14, GREY, 3)


def stopwatch_globe(g, x, y, r, t=0.0, green=0.0):
    """ลูกโลก (เขียวขึ้นเรื่อย ๆ = ปลอดโรค)"""
    c = g.c
    c.new_path()
    c.arc(x, y, r, 0, 2 * math.pi)
    base = (0.45, 0.7, 0.93)
    c.set_source_rgb(*base)
    c.fill_preserve()
    c.set_source_rgba(*INK[:3], 1)
    c.set_line_width(7)
    c.stroke()
    for i, (dx, dy, rx, ry) in enumerate(((-0.3, -0.2, 0.35, 0.25), (0.3, 0.1, 0.25, 0.4), (-0.1, 0.45, 0.2, 0.15))):
        g.blob(x + dx * r, y + dy * r, rx * r, ry * r, hexc("#6fae5a"), 4, seed=i)
