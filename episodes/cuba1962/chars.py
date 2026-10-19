"""ตัวละครและพร็อพ: วิกฤตขีปนาวุธคิวบา 22 ต.ค. 1962 — คนแบบกึ่งเสมือนจริงจาก src/people.py
ไม่แสดงภาพระเบิดนิวเคลียร์ทำลายล้าง ใช้นาฬิกา/ชนวน/แสงเตือนแทน"""
import math

import cairo

from gfx import GOLD, GOLD2, GREY, INK, LGREY, NAVY, RED, WHITE, hexc, lerp
from gfx import hn as _hn
from people import Look, _rr, _shade, _smooth_path, _stroke

SEA = hexc("#bcd8ec")
LAND = hexc("#e9dfc8")
US_BLUE = hexc("#3f6496")
SOV_RED = hexc("#b8473a")


def hn(*a):
    return (_hn(*a) + 1) / 2


# จอห์น เอฟ. เคนเนดี (45): ผมหนาน้ำตาลแดงปัดลอนสูง หน้าตายิ้มเก่ง สูทเทาเข้ม เนกไทแคบสีกรมท่า
JFK = Look(hair="jfk", hair_col=hexc("#7a4a2a"), suit=hexc("#3a3f4a"), tie=hexc("#1f2b4a"), w=60, jaw=0.6,
           nose=1.05, brow=1.0, age=0.3, build=1.0, height=1.02, pin=False)
# นิกิตา ครุสชอฟ (68): ศีรษะล้าน ใบหน้ากลม ร่างท้วม สูทหลวม เหรียญดาวที่อก
KHRUSHCHEV = Look(hair="bald", hair_col=hexc("#b9b4aa"), suit=hexc("#4a4d55"), tie=hexc("#5a3a3a"), w=68, jaw=0.8,
                  jowls=0.8, nose=1.15, brow=0.7, age=0.75, build=1.25, height=0.9, stars=2)
ADVISORS = [
    Look(hair="part", hair_col=hexc("#3a2f28"), suit=hexc("#2f3a4a"), tie=hexc("#7a2e2e"), glasses="thin", w=58,
         age=0.4),
    Look(hair="crew", hair_col=hexc("#9a948a"), suit=hexc("#4f5a3a"), tie=hexc("#2b2622"), w=60, jaw=0.7, age=0.7),
]
FAMILY = [
    Look(hair="slick", hair_col=hexc("#3a2f28"), suit=hexc("#8a6a4a"), outfit="flannel", pants=hexc("#3a3a42"), w=58,
         age=0.4),
    Look(hair="bun", hair_col=hexc("#a8763e"), suit=hexc("#3f8a8a"), outfit="dress", w=54, age=0.3, height=0.93),
    Look(hair="buzz", hair_col=hexc("#6b4a33"), suit=hexc("#e3a92b"), outfit="tee", pants=hexc("#3f6496"), w=56,
         age=0.0, height=0.62, headsc=1.4),
]


# ---------------------------------------------------------------- พร็อพ
def tv(g, x, y, sc=1.0, t=0.0, on=True, face=None):
    """ทีวีจอตู้ยุค 60 (ภาพขาวดำ) — face: Look ของคนบนจอ"""
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -260, -210, 520, 400, 34)
        _shade(c, hexc("#7a5230"), 7, 0.3)
        _rr(c, -220, -170, 360, 290, 50)
        _shade(c, hexc("#c9cdd3") if on else hexc("#55585e"), 6, 0.15)
        if on and face is not None:
            from people import head
            c.save()
            _rr(c, -220, -170, 360, 290, 50)
            c.clip()
            with g.at(-40, 10, 1.05):
                head(g, face, "firm", talk=0.5 + 0.5 * math.sin(t * 9), turn=0.0)
            for k in range(0, 290, 8):   # เส้นสแกน
                c.rectangle(-220, -170 + k, 360, 2)
            c.set_source_rgba(0, 0, 0, 0.08)
            c.fill()
            c.restore()
        for k in (-90, 90):
            g.line([(k * 0.3, -210), (k, -320)], 6, amp=0)
        for i in range(2):
            g.circle(200, -90 + i * 80, 18, GOLD, 4)


def caribbean_map(g, x, y, sc=1.0, t=0.0, missiles=0.0, ring=0.0, ships=0.0, range_k=0.0):
    """แผนที่ฟลอริดา-คิวบา: ฐานขีปนาวุธ, วงพิสัยยิง, เส้นปิดล้อม"""
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -460, -460, 920, 920, 30)
        _shade(c, SEA, 6, 0.05)
        c.save()
        _rr(c, -460, -460, 920, 920, 30)
        c.clip()
        # ฟลอริดา + ชายฝั่งสหรัฐ
        _smooth_path(c, [(-460, -460), (300, -460), (300, -330), (120, -300), (80, -200), (60, -90), (20, -60),
                         (-10, -120), (-40, -260), (-200, -300), (-460, -260)])
        _shade(c, LAND, 5, 0.1)
        g.text("สหรัฐอเมริกา", -180, -380, 40, "kanit", NAVY)
        # คิวบา
        _smooth_path(c, [(-330, 110), (-200, 60), (-40, 70), (120, 110), (300, 170), (360, 220), (240, 220), (60, 170),
                         (-120, 140), (-280, 150)])
        _shade(c, hexc("#d9e8b8"), 5, 0.15)
        g.text("คิวบา", 30, 150, 40, "kanit", INK)
        # ระยะ ~145 กม.
        g.line([(30, -70), (-60, 70)], 5, RED, amp=0)
        g.text("~145 กม.", 90, 0, 32, "kanit", RED)
        if missiles > 0:
            for i, (mx, my) in enumerate(((-210, 100), (-130, 95), (20, 100))):
                with g.at(mx, my, missiles * (1 + 0.1 * math.sin(t * 5 + i))):
                    g.poly([(0, -40), (12, -10), (12, 20), (-12, 20), (-12, -10)], RED, 3)
        if range_k > 0:
            for i in range(3):
                r = (i + 1) * 260 * range_k
                c.new_path()
                c.arc(-120, 100, r, 0, 2 * math.pi)
                c.set_source_rgba(0.85, 0.2, 0.2, 0.5 - 0.12 * i)
                c.set_line_width(5)
                c.set_dash([18, 12])
                c.stroke()
                c.set_dash([])
        if ring > 0:   # เส้นปิดล้อม (quarantine line)
            c.new_path()
            c.arc(0, 140, 330, math.pi * 0.05, math.pi * 0.05 + 2 * math.pi * ring)
            c.set_source_rgba(*US_BLUE[:3], 1)
            c.set_line_width(10)
            c.set_dash([30, 16])
            c.stroke()
            c.set_dash([])
        if ships > 0:
            for i in range(8):
                a = i * 2 * math.pi / 8 + 0.3
                ship_icon(g, math.cos(a) * 330, 140 + math.sin(a) * 330, 0.5 * ships, US_BLUE, math.degrees(a) + 90)
        c.restore()
        c.new_path()
        _rr(c, -460, -460, 920, 920, 30)
        c.set_source_rgba(*INK)
        c.set_line_width(6)
        c.stroke()


def ship_icon(g, x, y, s, col, rot=0.0):
    with g.at(x, y, s, rot):
        _smooth_path(g.c, [(0, -60), (22, -20), (22, 50), (-22, 50), (-22, -20)])
        _shade(g.c, col, 4, 0.2)
        _rr(g.c, -10, -6, 20, 24, 4)
        _shade(g.c, WHITE, 2, 0)


def warship(g, x, y, sc=1.0, t=0.0, flip=False, col=hexc("#7b8794")):
    c = g.c
    with g.at(x, y + 5 * math.sin(t * 1.8 + x), sc, 1.0 * math.sin(t * 1.3), sx=-sc if flip else sc, sy=sc):
        _smooth_path(c, [(-300, -40), (300, -40), (260, 40), (-260, 40)])
        _shade(c, col, 6, 0.3, horiz=False)
        _rr(c, -120, -120, 200, 80, 8)
        _shade(c, col, 5, 0.2)
        _rr(c, -60, -200, 80, 80, 6)
        _shade(c, col, 5, 0.2)
        g.line([(-20, -200), (-20, -300)], 6, INK, amp=0)
        _rr(c, 140, -80, 80, 40, 6)
        _shade(c, col, 4, 0.2)
        g.line([(220, -60), (300, -70)], 10, INK, amp=0)


def cargo_ship(g, x, y, sc=1.0, t=0.0, flip=False):
    c = g.c
    with g.at(x, y + 5 * math.sin(t * 1.6 + x), sc, 1.0 * math.sin(t * 1.2), sx=-sc if flip else sc, sy=sc):
        _smooth_path(c, [(-280, -40), (300, -40), (260, 40), (-240, 40)])
        _shade(c, hexc("#5a3a3a"), 6, 0.3, horiz=False)
        for i in range(3):
            _rr(c, -200 + i * 120, -110, 100, 70, 4)
            _shade(c, [hexc("#c8553d"), hexc("#3f6496"), hexc("#6b8f3a")][i], 4, 0.2)
        _rr(c, 180, -150, 80, 110, 6)
        _shade(c, WHITE, 5, 0.2)
        _rr(c, 200, -220, 30, 70, 4)
        _shade(c, SOV_RED, 4, 0.1)


def sea(g, y0, t, y1=1300):
    c = g.c
    _rr(c, -400, y0, 1880, y1 - y0, 0)
    _shade(c, SEA, 0, 0)
    for i in range(14):
        x = -300 + (i * 173) % 1600
        yy = y0 + 40 + (i * 61) % max(60, y1 - y0 - 80)
        g.line([(x, yy + 5 * math.sin(t * 2 + i)), (x + 40, yy - 6), (x + 80, yy + 5 * math.sin(t * 2 + i))], 4,
               (1, 1, 1, 1), amp=0)


def jet(g, x, y, sc=1.0, rot=0.0):
    c = g.c
    with g.at(x, y, sc, rot):
        _smooth_path(c, [(-160, -10), (140, -14), (200, 0), (140, 14), (-160, 10)])
        _shade(c, hexc("#9aa1ab"), 5, 0.2, horiz=False)
        for sy in (-1, 1):
            c.new_path()
            for px, py in [(20, sy * 12), (-60, sy * 110), (-20, sy * 110), (70, sy * 14)]:
                c.line_to(px, py)
            c.close_path()
            _shade(c, hexc("#7b8794"), 4, 0.2)
        c.new_path()
        for px, py in [(-150, -8), (-190, -60), (-160, -60), (-110, -10)]:
            c.line_to(px, py)
        c.close_path()
        _shade(c, hexc("#7b8794"), 4, 0.2)


def missile(g, x, y, sc=1.0, rot=0.0):
    """ขีปนาวุธบนแท่นยิง (ไม่ยิง)"""
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -160, -30, 320, 40, 6)
        _shade(c, hexc("#4f5a3a"), 5, 0.2)
        with g.at(0, -40, 1, -30):
            _smooth_path(c, [(-200, -18), (150, -18), (230, 0), (150, 18), (-200, 18)])
            _shade(c, hexc("#e9e2d4"), 5, 0.2, horiz=False)
            _rr(c, -210, -30, 40, 60, 4)
            _shade(c, hexc("#4f5a3a"), 4, 0.1)
            g.circle(20, 0, 8, SOV_RED, 0)


def time_bomb(g, x, y, sc=1.0, t=0.0, fuse=1.0):
    """ระเบิดเวลา (สัญลักษณ์) — fuse 1..0 ชนวนเหลือ"""
    c = g.c
    with g.at(x, y, sc):
        c.new_path()
        c.arc(0, 0, 140, 0, 2 * math.pi)
        _shade(c, hexc("#2b2b30"), 7, 0.3)
        _rr(c, -40, -170, 80, 40, 8)
        _shade(c, hexc("#4a4a52"), 5, 0.1)
        L = 160 * fuse
        pts = [(0, -170), (30, -170 - L * 0.4), (-10, -170 - L * 0.75), (20, -170 - L)]
        if fuse > 0:
            _stroke(c, pts, 6, hexc("#a8763e"))
            g.sparkle(pts[-1][0], pts[-1][1], 30 + 8 * math.sin(t * 25), (1, 0.75, 0.3, 1), 0)
        _rr(c, -80, -30, 160, 60, 10)
        _shade(c, hexc("#1b1916"), 4, 0)
        g.text(f"00:{int(59 * fuse):02d}", 0, 0, 40, "kanit", RED)


def red_phone(g, x, y, sc=1.0, ring=0.0, t=0.0):
    c = g.c
    with g.at(x + ring * 4 * math.sin(t * 50), y, sc):
        _smooth_path(c, [(-110, 0), (-90, -90), (90, -90), (110, 0)])
        _shade(c, SOV_RED, 6, 0.25)
        c.new_path()
        c.arc(0, -40, 34, 0, 2 * math.pi)
        _shade(c, WHITE, 4, 0.1)
        with g.at(0, -110 - ring * 10 * abs(math.sin(t * 30)), 1, ring * 6 * math.sin(t * 40)):
            _smooth_path(c, [(-130, 0), (-110, -40), (110, -40), (130, 0), (90, 10), (60, -14), (-60, -14), (-90, 10)])
            _shade(c, SOV_RED, 6, 0.25)


def shelter_sign(g, x, y, sc=1.0):
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -150, -110, 300, 220, 10)
        _shade(c, hexc("#f2c230"), 6, 0.1)
        c.new_path()
        c.arc(0, -10, 70, 0, 2 * math.pi)
        _shade(c, INK, 0, 0)
        for i in range(3):
            a = math.radians(-90 + i * 120)
            with g.at(0, -10, 1, math.degrees(a)):
                c.new_path()
                c.move_to(0, 0)
                c.arc(0, 0, 62, math.radians(-30), math.radians(30))
                c.close_path()
                _shade(c, hexc("#f2c230"), 0, 0)
        g.circle(0, -10, 14, hexc("#f2c230"), 0)
        g.text("FALLOUT SHELTER", 0, 80, 26, "kanit", INK)


def cans(g, x, y, n=6, sc=1.0):
    with g.at(x, y, sc):
        for i in range(n):
            cx, cy = (i % 3) * 70 - 70, -(i // 3) * 90
            _rr(g.c, cx - 30, cy - 80, 60, 80, 6)
            _shade(g.c, [hexc("#c8553d"), hexc("#e3a92b"), hexc("#3f6496")][i % 3], 4, 0.2)
            _rr(g.c, cx - 30, cy - 60, 60, 30, 2)
            _shade(g.c, WHITE, 2, 0)


def thread(g, x0, x1, y, tension=1.0, t=0.0, snap=0.0):
    """เส้นด้ายตึง สั่น + ฟั่นจะขาดตรงกลาง"""
    mid = (x0 + x1) / 2
    jit = 3 * math.sin(t * 40) * tension
    g.line([(x0, y), (mid - 6, y + jit)], 6, INK, amp=0)
    g.line([(mid + 6, y - jit), (x1, y)], 6, INK, amp=0)
    for k in (-1, 1):
        g.line([(mid - 6, y + jit), (mid + 6, y - jit + k * 4)], 2, INK, amp=0)
    for sx in (-1, 1):
        g.circle(x0 if sx < 0 else x1, y, 22, GREY, 5)


def clock_face(g, x, y, r, minutes_to=3.0):
    """นาฬิกาวันสิ้นโลก: เข็มใกล้เที่ยงคืน"""
    c = g.c
    c.new_path()
    c.arc(x, y, r, 0, 2 * math.pi)
    _shade(c, WHITE, 7, 0.1)
    for i in range(12):
        a = i * math.pi / 6
        _stroke(c, [(x + math.sin(a) * r * 0.82, y - math.cos(a) * r * 0.82), (x + math.sin(a) * r * 0.94, y - math.cos(a) * r * 0.94)],
                5 if i % 3 == 0 else 3, INK, smooth=False)
    am = -minutes_to / 60 * 2 * math.pi
    _stroke(c, [(x, y), (x + math.sin(am) * r * 0.8, y - math.cos(am) * r * 0.8)], 8, RED, smooth=False)
    _stroke(c, [(x, y), (x + math.sin(am / 12) * r * 0.5, y - math.cos(am / 12) * r * 0.5)], 12, INK, smooth=False)
    g.circle(x, y, 12, INK, 0)


def dove(g, x, y, s=1.0, t=0.0):
    flap = math.sin(t * 8)
    with g.at(x, y, s):
        _smooth_path(g.c, [(-80, 10), (-20, -20), (60, -10), (90, -30), (100, -10), (60, 20), (-40, 30)])
        _shade(g.c, WHITE, 5, 0.15)
        _smooth_path(g.c, [(-10, -10), (10, -90 - 30 * flap), (40, -80 - 20 * flap), (30, -10)])
        _shade(g.c, WHITE, 5, 0.15)
        _stroke(g.c, [(100, -20), (140, -10)], 5, hexc("#4f8a3a"))
        g.circle(80, -22, 4, INK, 0)
