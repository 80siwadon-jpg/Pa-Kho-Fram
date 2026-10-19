"""ตัวละครและพร็อพ: แครี ฟิชเชอร์ (เกิด 21 ต.ค. 1956) — คนแบบกึ่งเสมือนจริงจาก src/people.py
ไม่ใช้โลโก้/ตัวอักษรของภาพยนตร์ — วาดเครื่องแต่งกายและปืนแบบทั่วไป"""
import math

from gfx import GOLD, GOLD2, GREY, INK, LGREY, NAVY, RED, WHITE, hexc, lerp
from gfx import hn as _hn
from people import Look, _rr, _shade, _smooth_path, _stroke

SPACE = hexc("#232a45")
PINK = hexc("#e88aa8")


def hn(*a):
    return (_hn(*a) + 1) / 2


# เจ้าหญิงในชุดขาว มวยผมสองข้าง (วัย 20)
LEIA = Look(hair="leia", hair_col=hexc("#5a3a26"), suit=hexc("#f6f3ec"), outfit="gown", shoes=hexc("#e9e2d4"),
            w=54, jaw=0.25, nose=0.95, brow=0.9, age=0.0, height=0.9)
# แครีวัยผู้ใหญ่นอกจอ: ผมสั้นยุ่งสีเข้ม เสื้อดำ (นักเขียน-นักพูด)
CARRIE = Look(hair="full", hair_col=hexc("#3a2c22"), suit=hexc("#1f1f24"), outfit="tee", pants=hexc("#1f1f24"),
              glasses="thin", w=56, jaw=0.35, nose=1.0, age=0.5, height=0.9)
CARRIE_TEEN = Look(hair="long", hair_col=hexc("#5a3a26"), suit=hexc("#8a6a9a"), outfit="tee", pants=hexc("#3f6496"),
                   w=54, age=0.0, height=0.88)
EXECS = [
    Look(hair="slick", hair_col=hexc("#3a2f28"), suit=hexc("#3b4250"), tie=hexc("#7a2e2e"), glasses="thick",
         w=60, jaw=0.6, jowls=0.5, nose=1.2, age=0.6),
    Look(hair="crew", hair_col=hexc("#9a948a"), suit=hexc("#2f3a4a"), tie=hexc("#8a6a2a"), facial="mustache",
         w=58, age=0.7),
]
FANS = [
    Look(hair="leia", hair_col=hexc("#2b2622"), suit=hexc("#f6f3ec"), outfit="gown", w=52, age=0.0, height=0.82),
    Look(hair="buzz", hair_col=hexc("#2b2622"), suit=hexc("#3f6496"), outfit="tee", pants=hexc("#3a3a42"), w=56,
         age=0.1, skin=hexc("#8a5a3c")),
    Look(hair="long", hair_col=hexc("#a8763e"), suit=hexc("#c8553d"), outfit="tee", pants=hexc("#3f6496"), w=54,
         age=0.1, height=0.9),
    Look(hair="part", hair_col=hexc("#6b4a33"), suit=hexc("#3c8d4f"), outfit="hoodie", pants=hexc("#3a3a42"),
         glasses="thick", w=56, age=0.2),
]


# ---------------------------------------------------------------- พร็อพ
def blaster(g, x, y, sc=1.0, rot=0.0, shot=0.0):
    """ปืนเลเซอร์แบบทั่วไป — shot 0..1 ลำแสงเลเซอร์ (ยิงขึ้นฟ้า ไม่โดนใคร)"""
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -20, -10, 80, 110, 14)   # ด้าม
        _shade(c, hexc("#2b2b30"), 5, 0.2)
        _rr(c, -60, -60, 220, 60, 14)   # ตัวปืน
        _shade(c, hexc("#4a4a52"), 5, 0.25)
        _rr(c, 150, -46, 90, 30, 8)    # ลำกล้อง
        _shade(c, hexc("#2b2b30"), 4, 0.1)
        _rr(c, 20, -84, 100, 26, 6)    # ศูนย์เล็ง
        _shade(c, hexc("#2b2b30"), 4, 0.1)
        if shot > 0:
            L = 600 * shot
            g.line([(240, -31), (240 + L, -31)], 26, (1, 0.3, 0.3, 0.35), amp=0)
            g.line([(240, -31), (240 + L, -31)], 10, (1, 0.85, 0.85, 1), amp=0)


def stars(g, t, n=26, area=(-200, 300, 1280, 1250), seed=5):
    for i in range(n):
        x = area[0] + hn(i, seed) * (area[2] - area[0])
        y = area[1] + hn(i, seed + 1) * (area[3] - area[1])
        g.sparkle(x, y, 6 + 5 * hn(i, seed + 2) + 2 * math.sin(t * 3 + i), (1, 1, 1, 0.9), 0)


def space_panel(g, x0=60, y0=300, x1=1020, y1=1240):
    _rr(g.c, x0, y0, x1 - x0, y1 - y0, 40)
    _shade(g.c, SPACE, 6, 0.0)


def spotlight(g, x, y, ang, k=1.0, col=(1, 0.95, 0.75)):
    c = g.c
    with g.at(x, y, 1, ang):
        c.new_path()
        c.move_to(-20, 0)
        c.line_to(20, 0)
        c.line_to(260, 1100)
        c.line_to(-260, 1100)
        c.close_path()
        c.set_source_rgba(*col, 0.25 * k)
        c.fill()
        _rr(c, -50, -40, 100, 60, 10)
        _shade(c, hexc("#2b2b30"), 4, 0.1)


def camera(g, x, y, sc=1.0, flash=0.0):
    c = g.c
    with g.at(x, y, sc):
        if flash > 0:
            g.sunburst(60, -110, 60, 200, 14, 0, 8, (1, 1, 0.85, flash))
        _rr(c, -110, -70, 220, 140, 16)
        _shade(c, hexc("#2b2b30"), 6, 0.2)
        c.new_path()
        c.arc(0, 0, 48, 0, 2 * math.pi)
        _shade(c, hexc("#8fb8de"), 5, 0.1)
        _rr(c, 40, -120, 50, 40, 6)
        _shade(c, WHITE if flash > 0 else LGREY, 4, 0)


def scale_weigh(g, x, y, sc=1.0, needle=0.0):
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -160, -60, 320, 60, 14)
        _shade(c, WHITE, 6, 0.2)
        c.new_path()
        c.arc(0, -30, 46, math.pi, 2 * math.pi)
        _shade(c, LGREY, 4, 0.1)
        a = math.pi + needle * math.pi
        _stroke(c, [(0, -30), (math.cos(a) * 40, -30 + math.sin(a) * 40)], 5, RED, smooth=False)


def tape(g, x, y, w, rot, text, col=hexc("#f2c230")):
    """เทปติดกล่าวหา (ป้ายตราหน้า)"""
    with g.at(x, y, 1, rot):
        _rr(g.c, -w / 2, -36, w, 72, 4)
        _shade(g.c, col, 4, 0.1)
        g.text(text, 0, 0, 40, "kanit", INK, maxw=w - 20)


def microphone(g, x, y, sc=1.0):
    c = g.c
    with g.at(x, y, sc):
        g.line([(0, 0), (0, 520)], 10, hexc("#3a3a40"), amp=0)
        g.line([(-80, 520), (80, 520)], 12, hexc("#3a3a40"), amp=0)
        _rr(c, -34, -110, 68, 120, 34)
        _shade(c, hexc("#4a4a52"), 5, 0.2)
        for k in range(4):
            _stroke(c, [(-30, -90 + k * 22), (30, -90 + k * 22)], 2, WHITE, 0.3, smooth=False)


def book(g, x, y, sc=1.0, rot=0.0, title="บันทึกชีวิต"):
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -130, -180, 260, 360, 10)
        _shade(c, hexc("#3f6496"), 6, 0.25)
        _rr(c, -100, -140, 200, 120, 6)
        _shade(c, WHITE, 3, 0)
        g.text(title, 0, -80, 34, "kanit", INK, maxw=180)


def frame_box(g, x, y, w, h, brk=0.0, col=GREY):
    """กรอบที่โลกกำหนด — brk 0..1 แตกออก"""
    c = g.c
    segs = [((-1, -1), (1, -1)), ((1, -1), (1, 1)), ((1, 1), (-1, 1)), ((-1, 1), (-1, -1))]
    for i, ((ax, ay), (bx, by)) in enumerate(segs):
        dx, dy = (ax + bx) / 2, (ay + by) / 2
        with g.at(x + dx * 110 * brk, y + dy * 90 * brk, 1, (i % 2 * 2 - 1) * 15 * brk):
            g.line([(ax * w / 2 - dx * 220 * 0, ay * h / 2), (bx * w / 2, by * h / 2)], 14, col, amp=0)


def heart(g, x, y, s=1.0, col=RED):
    with g.at(x, y, s):
        c = g.c
        c.new_path()
        c.move_to(0, 30)
        c.curve_to(-70, -20, -40, -70, 0, -36)
        c.curve_to(40, -70, 70, -20, 0, 30)
        _shade(c, col, 5, 0.2)


def storm_cloud(g, x, y, s=1.0, t=0.0, bolt=0.0):
    with g.at(x + 10 * math.sin(t), y, s):
        for i, (dx, r) in enumerate(((-90, 70), (0, 95), (90, 70), (-40, 60), (50, 60))):
            g.circle(dx, (i > 2) * 40, r, hexc("#7b8794"), 5)
        if bolt > 0:
            g.poly([(10, 60), (-30, 160), (5, 160), (-20, 260), (50, 130), (15, 130), (40, 60)], GOLD2, 5)


def pill(g, x, y, rot=0.0, s=1.0):
    with g.at(x, y, s, rot):
        _rr(g.c, -40, -18, 80, 36, 18)
        _shade(g.c, WHITE, 4, 0.1)
        _rr(g.c, 0, -18, 40, 36, 18)
        _shade(g.c, RED, 4, 0.1)
