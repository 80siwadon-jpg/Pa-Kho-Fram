"""ตัวละครและพร็อพ: ระเบิดค่ายทหารกองกำลังรักษาสันติภาพ กรุงเบรุต 23 ต.ค. 1983
ไม่แสดงภาพความรุนแรง: ไม่มีคนบาดเจ็บ/ศพ — ใช้แสงวาบ ฝุ่นควัน ซากตึก ตัวเลขผู้เสียชีวิต และอนุสรณ์แทน; ไม่วาดคนร้าย"""
import math

import cairo

from gfx import GOLD, GOLD2, GREY, INK, LGREY, NAVY, RED, WHITE, hexc
from people import Look, _rr, _shade, _smooth_path, _stroke

CONCRETE = hexc("#d8d3c7")
CONCRETE2 = hexc("#bdb6a6")
SANDBAG = hexc("#cdb88a")
DUST = (0.72, 0.68, 0.62)
FIRE = hexc("#f2a93b")
OLIVE = hexc("#5f6b45")
OLIVE2 = hexc("#4a5538")
TRUCK = hexc("#e8c13a")
DAWN = hexc("#f6d9b0")

MARINES = [   # นาวิกโยธินสหรัฐฯ (ชุดสนามลายพราง ผมสั้นเกรียน)
    Look(hair="crew", hair_col=hexc("#6b4a33"), outfit="fatigue", suit=OLIVE, pants=OLIVE2, w=56, age=0.2, jaw=0.6),
    Look(hair="buzz", hair_col=hexc("#221e1c"), outfit="fatigue", suit=OLIVE, pants=OLIVE2, w=56, age=0.2,
         skin=hexc("#8a5a3c")),
    Look(hair="crew", hair_col=hexc("#c9a46a"), outfit="fatigue", suit=OLIVE, pants=OLIVE2, w=55, age=0.15),
]
PARAS = [   # พลร่มฝรั่งเศส (เบเรต์แดง)
    Look(hair="short", hair_col=hexc("#3a2f28"), outfit="fatigue", suit=hexc("#6f7450"), pants=OLIVE2, hat="beret",
         hat_trim=hexc("#a8323a"), w=56, age=0.25),
    Look(hair="short", hair_col=hexc("#5a4a3a"), outfit="fatigue", suit=hexc("#6f7450"), pants=OLIVE2, hat="beret",
         hat_trim=hexc("#a8323a"), w=55, age=0.2, facial="mustache"),
]
RESCUE = [   # ทีมกู้ภัย (หมวกนิรภัย เสื้อสะท้อนแสง)
    Look(hair="crew", outfit="tee", suit=hexc("#e8892e"), pants=hexc("#3a3a40"), hat="brodie",
         hat_trim=hexc("#f2c94c"), w=56),
    Look(hair="buzz", outfit="fatigue", suit=OLIVE, pants=OLIVE2, hat="brodie", hat_trim=OLIVE2, w=56,
         skin=hexc("#b07a52")),
]


def sky(g, k=1.0, col=DAWN):
    """ท้องฟ้ารุ่งเช้า (ไล่สีส้มอ่อนลงหาขอบฟ้า บนพื้นขาว)"""
    if k <= 0:
        return
    c = g.c
    lg = cairo.LinearGradient(0, 200, 0, 1270)
    lg.add_color_stop_rgba(0, 1, 1, 1, 0)
    lg.add_color_stop_rgba(1, *col[:3], 0.9 * k)
    c.set_source(lg)
    c.rectangle(-500, 140, 2100, 1130)
    c.fill()


def sun(g, x, y, r, t=0.0):
    g.sunburst(x, y, r * 1.2, r * 2.0, 14, t * 6, 8, (0.98, 0.78, 0.4, 0.6))
    g.circle(x, y, r, hexc("#f6b450"), 5)


def skyline(g, y, t=0.0, a=1.0):
    """เมืองเบรุตริมทะเล: ตึกแถว หออะซาน ต้นสน(ซีดาร์)"""
    c = g.c
    with g.alpha(a):
        xs = [(-300, 160, 300), (-120, 120, 420), (20, 150, 260), (190, 110, 520), (320, 140, 340), (480, 120, 450),
              (620, 160, 280), (800, 110, 380), (930, 150, 310), (1100, 130, 420), (1250, 150, 260)]
        for x, w, h in xs:
            _rr(c, x, y - h, w, h, 4)
            _shade(c, hexc("#e7e1d3"), 4, 0.2)
            for r in range(int(h / 70)):
                for k in range(int(w / 50)):
                    _rr(c, x + 16 + k * 46, y - h + 24 + r * 66, 22, 30, 3)
                    _shade(c, hexc("#bcd6e6"), 2, 0)
        mx = 700   # หออะซาน
        _rr(c, mx - 22, y - 560, 44, 560, 4)
        _shade(c, WHITE, 4, 0.2)
        _smooth_path(c, [(mx - 30, y - 560), (mx, y - 640), (mx + 30, y - 560)])
        _shade(c, hexc("#7fb08a"), 4, 0.2)
        _rr(c, mx - 34, y - 470, 68, 18, 4)
        _shade(c, WHITE, 3, 0.1)


def clock(g, x, y, r, hh=6, mm=22, k=1.0):
    with g.at(x, y, k):
        g.circle(0, 0, r, WHITE, 8)
        for i in range(12):
            a = i * math.pi / 6
            g.line([(0.82 * r * math.sin(a), -0.82 * r * math.cos(a)), (0.92 * r * math.sin(a), -0.92 * r * math.cos(a))],
                   5, INK, amp=0)
        am = mm / 60 * 2 * math.pi
        ah = (hh % 12 + mm / 60) / 12 * 2 * math.pi
        g.line([(0, 0), (0.5 * r * math.sin(ah), -0.5 * r * math.cos(ah))], 12, INK, amp=0)
        g.line([(0, 0), (0.75 * r * math.sin(am), -0.75 * r * math.cos(am))], 7, RED, amp=0)
        g.circle(0, 0, 10, INK, 0)


def barracks(g, x, y, sc=1.0, floors=4, squash=0.0, flag="us", t=0.0):
    """อาคารที่พักคอนกรีต 4 ชั้น — squash 0..1 = ยุบตัวลงเป็นกองซาก"""
    c = g.c
    fh = 130
    h = floors * fh * (1 - 0.88 * squash)
    with g.at(x, y, sc):
        if squash < 1:
            _rr(c, -300, -h, 600, h, 6)
            _shade(c, CONCRETE, 6, 0.25)
            for f in range(floors):
                fy = -h + f * h / floors
                _stroke(c, [(-300, fy), (300, fy)], 4, INK, 0.4, smooth=False)
                for k in range(5):
                    wy = fy + h / floors * 0.25
                    _rr(c, -260 + k * 110, wy, 70, h / floors * 0.5, 4)
                    _shade(c, hexc("#8fa6b5") if squash < 0.1 else hexc("#6a645a"), 3, 0.1)
        if squash > 0:   # กองซาก
            for i in range(9):
                rx = -260 + i * 65 + 10 * math.sin(i * 7)
                with g.at(rx, -40 * squash - 20 * (i % 3), 1, (i * 37) % 50 - 25):
                    _rr(c, -50, -24, 100, 48, 6)
                    _shade(c, CONCRETE2, 4, 0.3)
        if squash < 0.3:
            g.line([(250, -h), (250, -h - 160)], 6, INK, amp=0)
            if flag == "us":
                g.flag(250, -h - 160, 120, 76, "us", t)
            elif flag == "fr":
                flag_fr(g, 250, -h - 160, 120, 76, t)


def flag_fr(g, x, y, w, h, t=0.0):
    c = g.c
    for i, col in enumerate((hexc("#2b4c9a"), WHITE, RED)):
        c.new_path()
        x0, x1 = x + w * i / 3, x + w * (i + 1) / 3
        o0, o1 = 5 * math.sin(t * 6 - i), 5 * math.sin(t * 6 - i - 1)
        for p in [(x0, y + o0), (x1, y + o1), (x1, y + h + o1), (x0, y + h + o0)]:
            c.line_to(*p)
        c.close_path()
        _shade(c, col, 3, 0.1)


def flag_lb(g, x, y, w, h, t=0.0):
    """ธงเลบานอน: แดง-ขาว-แดง + ต้นซีดาร์เขียว"""
    c = g.c
    with g.at(x, y + 4 * math.sin(t * 5)):
        _rr(c, 0, 0, w, h, 2)
        _shade(c, RED, 4, 0)
        _rr(c, 0, h * 0.25, w, h * 0.5, 0)
        _shade(c, WHITE, 0, 0)
        c.new_path()
        for p in [(w / 2, h * 0.28), (w / 2 + w * 0.14, h * 0.68), (w / 2 - w * 0.14, h * 0.68)]:
            c.line_to(*p)
        c.close_path()
        _shade(c, hexc("#3c8d4f"), 2, 0)


def bunk(g, x, y, sc=1.0, t=0.0, look=None):
    """เตียงสองชั้น ทหารนอนหลับ (หัวบนหมอน + ผ้าห่ม) + Zzz"""
    from people import head
    c = g.c
    with g.at(x, y, sc):
        for yy in (-140, -360):
            _rr(c, -220, yy - 20, 440, 40, 6)
            _shade(c, hexc("#8a8f94"), 5, 0.2)
            _rr(c, -200, yy - 50, 90, 34, 14)
            _shade(c, WHITE, 4, 0.1)   # หมอน
            _smooth_path(c, [(-110, yy - 20), (-100, yy - 70), (190, yy - 64), (200, yy - 20)])
            _shade(c, hexc("#6b7a52"), 5, 0.25)   # ผ้าห่ม
            if look is not None:
                with g.at(-150, yy - 80, 0.42, -80):
                    head(g, look, "neutral", 0, 0, (0, 0), 1, 4.5)
                for i in range(3):
                    u = (t * 0.5 + i / 3 + yy * 0.001) % 1
                    g.text("z", -120 + 40 * u + 20 * i, yy - 140 - 120 * u, 30 + 16 * i, "kanit", (0.3, 0.35, 0.5, 1 - u))
        for sx in (-1, 1):
            g.line([(sx * 220, 0), (sx * 220, -420)], 10, hexc("#6a7076"), amp=0)


def truck(g, x, y, sc=1.0, t=0.0, speed=1.0):
    """รถบรรทุกสีเหลือง (ภาพเงาเรียบ ไม่มีคนขับให้เห็น) — x,y = พื้น หันขวา"""
    c = g.c
    by = 3 * math.sin(t * 30) * speed
    with g.at(x, y + by, sc):
        _rr(c, -300, -230, 380, 170, 10)   # กระบะ
        _shade(c, TRUCK, 6, 0.3)
        for k in range(4):
            _stroke(c, [(-280 + k * 95, -220), (-280 + k * 95, -70)], 4, INK, 0.3, smooth=False)
        _smooth_path(c, [(90, -60), (90, -250), (210, -250), (270, -150), (280, -60)])
        _shade(c, TRUCK, 6, 0.25)
        _smooth_path(c, [(120, -230), (195, -230), (240, -150), (120, -150)])
        _shade(c, hexc("#4a5a66"), 4, 0.1)   # กระจกมืด
        for wx in (-200, 190):
            with g.at(wx, -50, 1, -t * 400 * speed):
                c.new_path()
                c.arc(0, 0, 50, 0, 2 * math.pi)
                _shade(c, hexc("#2b2826"), 5, 0.1)
                c.new_path()
                c.arc(0, 0, 20, 0, 2 * math.pi)
                _shade(c, hexc("#9a9a9a"), 3, 0)
        if speed > 0.3:
            for i in range(4):
                u = (t * 1.5 + i / 4) % 1
                g.circle(-320 - 160 * u, -40 - 30 * u, 20 + 30 * u, DUST + (0.6 * (1 - u),), 0)
            for i in range(3):
                g.line([(-360 - i * 50, -180 + i * 50), (-460 - i * 50, -180 + i * 50)], 6, GREY, amp=0)


def fence(g, x0, x1, y, broken=None):
    """รั้วลวดหนาม + เสา (broken = x ช่วงที่ถูกพังเปิด)"""
    c = g.c
    for xx in range(int(x0), int(x1), 140):
        if broken and broken[0] < xx < broken[1]:
            continue
        g.line([(xx, y), (xx, y - 220)], 8, hexc("#6e6a62"), amp=0)
    for row in (-190, -110):
        segs = [(x0, x1)] if not broken else [(x0, broken[0]), (broken[1], x1)]
        for a, b in segs:
            pts = []
            n = int((b - a) / 24)
            for i in range(n + 1):
                pts.append((a + (b - a) * i / max(1, n), y + row + 10 * math.sin(i * 1.9)))
            _stroke(c, pts, 3, INK, 0.8)
            for i in range(0, n, 3):
                px, py = pts[i]
                _stroke(c, [(px - 8, py - 8), (px + 8, py + 8)], 3, INK, 0.8, smooth=False)


def sandbags(g, x, y, n=5, rows=3, sc=1.0, scatter=0.0):
    c = g.c
    with g.at(x, y, sc):
        for r in range(rows):
            for i in range(n - r):
                bx = -n * 50 + i * 100 + r * 50 + scatter * (i - n / 2) * 60
                by = -30 - r * 50 - scatter * 40 * (1 - r)
                with g.at(bx, by, 1, scatter * (i * 13 % 30 - 15)):
                    _rr(c, -50, -26, 100, 52, 22)
                    _shade(c, SANDBAG, 4, 0.25)


def mushroom(g, x, y, k, t=0.0, sc=1.0):
    """ควันรูปดอกเห็ด (ไม่มีเศษ/คน) — k 0..1 การก่อตัว"""
    if k <= 0:
        return
    with g.at(x, y, sc):
        hgt = 650 * k
        for i in range(7):   # ลำต้น
            yy = -i * hgt / 7
            g.circle(8 * math.sin(i + t), yy, 70 + 10 * math.sin(t * 2 + i), DUST + (0.9,), 0)
        for i in range(10):   # หัวเห็ด
            a = i * 2 * math.pi / 10 + t * 0.2
            rr = 170 * k
            g.circle(rr * math.cos(a), -hgt + 0.45 * rr * math.sin(a), 110 * k + 10 * math.sin(t + i),
                     (0.62, 0.58, 0.54, 0.95), 0)
        g.circle(0, -hgt, 140 * k, (0.68, 0.63, 0.58, 1), 0)
        for i in range(5):   # แสงไฟเรื่อ ๆ ที่ฐาน
            g.circle(-120 + i * 60, -20, 50 + 10 * math.sin(t * 6 + i), (0.98, 0.66, 0.23, 0.7), 0)


def dust(g, x, y, r, t, n=7, a=0.75, seed=0.0):
    for i in range(n):
        u = (t * 0.25 + i / n + seed) % 1
        g.circle(x + r * 1.2 * math.sin(i * 2.1 + seed) + 30 * math.sin(t + i), y - r * u, r * (0.5 + 0.6 * u),
                 DUST + (a * (1 - 0.7 * u),), 0)


def flash(g, x, y, r, k):
    """แสงวาบสว่าง (ไม่มีเศษ) k 0..1"""
    if k <= 0 or k >= 1:
        return
    a = 1 - k
    g.star(x, y, r * (0.4 + 0.9 * k), (0.98, 0.66, 0.23, a), 0, pts=12, inner=0.5)
    g.star(x, y, r * 0.55 * (0.4 + 0.9 * k), (1, 0.96, 0.8, a), 0, pts=12, inner=0.55)


def candle(g, x, y, sc=1.0, t=0.0):
    c = g.c
    with g.at(x, y, sc):
        rg = cairo.RadialGradient(0, -190, 0, 0, -190, 120)
        rg.add_color_stop_rgba(0, 1.0, 0.82, 0.45, 0.35)
        rg.add_color_stop_rgba(1, 1.0, 0.82, 0.45, 0)
        c.set_source(rg)
        c.arc(0, -190, 120, 0, 2 * math.pi)
        c.fill()
        _rr(c, -22, -160, 44, 160, 6)
        _shade(c, hexc("#f4ecd8"), 5, 0.25)
        fl = 1 + 0.12 * math.sin(t * 11 + x)
        with g.at(0, -170, 1, 0.08 * math.sin(t * 7 + x), sx=1, sy=fl):
            _smooth_path(c, [(0, -50), (14, -16), (10, 4), (0, 8), (-10, 4), (-14, -16)])
            _shade(c, FIRE, 3, 0)


def memorial(g, x, y, sc=1.0, n=7, k=1.0):
    """แถวป้ายอนุสรณ์สีขาว (หลุมศพทหารแบบเรียบ ๆ)"""
    c = g.c
    with g.at(x, y, sc):
        for i in range(n):
            kk = max(0.0, min(1.0, k * n - i))
            if kk <= 0.02:
                continue
            with g.at(-n * 70 + i * 140 + 70, 0, kk):
                _smooth_path(c, [(-36, 0), (-36, -120), (0, -150), (36, -120), (36, 0)])
                _shade(c, WHITE, 5, 0.2)
                _stroke(c, [(-18, -90), (18, -90)], 4, GREY, smooth=False)
                _stroke(c, [(-18, -70), (18, -70)], 4, GREY, smooth=False)


def barrier(g, x, y, sc=1.0):
    """แท่งแบริเออร์คอนกรีตกันรถพุ่งชน (เกิดขึ้นทั่วโลกหลังเหตุการณ์นี้)"""
    c = g.c
    with g.at(x, y, sc):
        _smooth_path(c, [(-90, 0), (-70, -40), (-30, -60), (-26, -170), (26, -170), (30, -60), (70, -40), (90, 0)])
        _shade(c, CONCRETE, 5, 0.3)
        for k in range(2):
            _stroke(c, [(-26, -150 + k * 40), (26, -130 + k * 40)], 8, hexc("#e8c13a"), smooth=False)


def ship(g, x, y, sc=1.0, t=0.0):
    """เรือรบสหรัฐฯ (สีเทา) — ถอนทหารกลับ"""
    c = g.c
    with g.at(x, y + 5 * math.sin(t * 1.6), sc, 1.0 * math.sin(t * 1.2)):
        _smooth_path(c, [(-330, -60), (300, -60), (360, -120), (260, 20), (-300, 20)])
        _shade(c, hexc("#8a9096"), 6, 0.3)
        _rr(c, -140, -170, 260, 110, 6)
        _shade(c, hexc("#a2a8ae"), 5, 0.25)
        _rr(c, -60, -260, 80, 90, 6)
        _shade(c, hexc("#a2a8ae"), 5, 0.2)
        g.line([(-20, -260), (-20, -360)], 6, INK, amp=0)
        g.flag(-20, -360, 80, 50, "us", t)


def scale(g, x, y, sc=1.0, tilt=0.0, left="", right="", t=0.0):
    """ตาชั่งสองแขน (เปรียบเทียบสองทางเลือก) — tilt + = ซ้ายต่ำ"""
    c = g.c
    with g.at(x, y, sc):
        g.line([(0, 0), (0, -420)], 12, INK, amp=0)
        _rr(c, -100, -10, 200, 30, 8)
        _shade(c, GOLD, 5, 0.2)
        a = math.radians(-12 * tilt)
        dx, dy = 300 * math.cos(a), 300 * math.sin(a)
        g.line([(-dx, -420 - dy), (dx, -420 + dy)], 10, GOLD2, amp=0)
        g.circle(0, -420, 16, GOLD, 4)
        for sx, txt in ((-1, left), (1, right)):
            px, py = sx * dx, -420 + sx * dy
            g.line([(px, py), (px - 90, py + 160)], 3, INK, amp=0)
            g.line([(px, py), (px + 90, py + 160)], 3, INK, amp=0)
            c.new_path()
            c.arc(px, py + 160, 110, 0, math.pi)
            c.close_path()
            _shade(c, GOLD2, 5, 0.2)
            if txt:
                g.label(txt, px, py + 250, 40)
