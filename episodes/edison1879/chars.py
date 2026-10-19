"""ตัวละครและพร็อพ: หลอดไฟไส้คาร์บอนของเอดิสัน 21 ต.ค. 1879 — คนแบบกึ่งเสมือนจริงจาก src/people.py"""
import math

import cairo

from gfx import GOLD, GOLD2, INK, LGREY, RED, WHITE, hexc
from people import Look, _rr, _shade, _smooth_path, _stroke

AMBER = hexc("#ffb347")
GLOW = (1.0, 0.72, 0.28)
WOOD = hexc("#a8763e")
WOOD2 = hexc("#7a5230")
GLASS = (0.86, 0.93, 0.98, 0.45)
BRASS = hexc("#c9a24a")

# โทมัส อัลวา เอดิสัน (32 ปี): ผมดำน้ำตาลหนา ปอยตกหน้าผาก หน้าเกลี้ยง คิ้วหนา กรามเหลี่ยม
# เชิ้ตขาวพับแขน กั๊กเทาเข้ม หูกระต่ายดำ สายนาฬิกาพก
EDISON = Look(hair="edison", hair_col=hexc("#3a2c22"), suit=hexc("#3b3a3e"), shirt=hexc("#f7f4ec"), tie=hexc("#1b1916"),
              outfit="vest", pants=hexc("#3b3a3e"), shoes=hexc("#1b1916"), w=62, jaw=0.65, nose=1.15, brow=1.3,
              age=0.25, build=1.05)
# ชาลส์ แบตเชเลอร์: ผู้ช่วยมือขวา เคราดกเต็มหน้า
BATCHELOR = Look(hair="part", hair_col=hexc("#4a3424"), suit=hexc("#5a4a3a"), shirt=hexc("#f2ece0"), tie=hexc("#7a2e2e"),
                 outfit="vest", pants=hexc("#4a4038"), facial="beard", w=58, jaw=0.4, nose=1.2, age=0.35, height=1.04)
# ฟรานซิส อัพตัน: นักคณิตศาสตร์ประจำทีม แว่นกลม หนวด
UPTON = Look(hair="part", hair_col=hexc("#6b4a33"), suit=hexc("#2f3a4a"), shirt=WHITE, tie=hexc("#2b3f63"),
             outfit="vest", pants=hexc("#2f3a4a"), facial="mustache", glasses="thin", w=56, jaw=0.3, age=0.2, height=0.98)
# นักวิทยาศาสตร์/นักข่าวที่หัวเราะเยาะ (หมวกทรงสูง/ทรงกลม)
CRITICS = [
    Look(hair="slick", hair_col=hexc("#9a948a"), suit=hexc("#1f1f24"), tie=hexc("#1f1f24"), bowtie=True, hat="tophat",
         facial="mustache", w=60, jaw=0.5, jowls=0.5, nose=1.3, age=0.8),
    Look(hair="short", hair_col=hexc("#3a2f28"), suit=hexc("#5a4a3a"), tie=hexc("#7a2e2e"), hat="bowler",
         facial="beard", w=58, age=0.5),
    Look(hair="part", hair_col=hexc("#6b4a33"), suit=hexc("#2f3a4a"), tie=hexc("#2b3f63"), hat="bowler",
         glasses="thin", w=56, age=0.4),
]


# ---------------------------------------------------------------- หลอดไฟ
def bulb(g, x, y, sc=1.0, glow=0.0, t=0.0, broken=0.0, filament="horse", rot=0.0, burn=0.0):
    """หลอดไฟแก้วยุคแรก (ทรงลูกแพร์ ปลายแหลม) — x,y = กลางกระเปาะ
    glow 0..1 แสงส้ม, burn 0..1 ไส้ละลายขาด (ล้มเหลว)"""
    c = g.c
    with g.at(x, y, sc, rot):
        if glow > 0:
            fl = 1 + 0.03 * math.sin(t * 9) + 0.02 * math.sin(t * 23)
            for r, a in ((520, 0.18), (330, 0.28), (190, 0.45)):
                rg = cairo.RadialGradient(0, 0, 0, 0, 0, r * fl)
                rg.add_color_stop_rgba(0, *GLOW, a * glow)
                rg.add_color_stop_rgba(1, *GLOW, 0)
                c.set_source(rg)
                c.arc(0, 0, r * fl, 0, 2 * math.pi)
                c.fill()
        # คอหลอด + ฐาน
        _rr(c, -44, 120, 88, 70, 10)
        _shade(c, BRASS, 5, 0.3)
        for k in range(3):
            _stroke(c, [(-44, 136 + k * 18), (44, 136 + k * 18)], 3, INK, 0.5, smooth=False)
        _rr(c, -22, 186, 44, 26, 8)
        _shade(c, hexc("#3a3330"), 4, 0)
        # สายไฟ/ขาไส้
        top = -40
        for sx in (-1, 1):
            _stroke(c, [(sx * 24, 120), (sx * 26, 40), (sx * 30, top + 30)], 4, hexc("#8a8580"), smooth=False)
        # ไส้หลอด
        fc = (0.15, 0.12, 0.1, 1) if glow < 0.2 else (1, 0.85 + 0.15 * glow, 0.55, 1)
        if filament == "horse" and burn < 1:
            pts = [(-30, top + 30), (-34, top - 20), (-14, top - 52), (14, top - 52), (34, top - 20), (30, top + 30)]
            if burn > 0:   # ขาดตรงกลาง
                _stroke(c, pts[:3], 6, fc)
                _stroke(c, pts[3:], 6, fc)
            else:
                if glow > 0.2:
                    _stroke(c, pts, 16, (1, 0.9, 0.6, 0.6 * glow))
                _stroke(c, pts, 6, fc)
        elif burn >= 1:
            _stroke(c, [(-30, top + 30), (-30, top - 4)], 5, fc)
            _stroke(c, [(30, top + 30), (28, top - 6)], 5, fc)
        # กระเปาะแก้ว
        _smooth_path(c, [(-44, 120), (-96, 40), (-112, -40), (-80, -130), (0, -168), (80, -130), (112, -40), (96, 40), (44, 120)])
        c.set_source_rgba(*GLASS[:3], 0.25 if glow < 0.3 else 0.12)
        c.fill_preserve()
        c.set_source_rgba(*INK)
        c.set_line_width(6)
        c.stroke()
        _stroke(c, [(0, -168), (6, -196), (2, -208)], 6, INK, smooth=False)   # จุกปลายแก้ว (ที่ปิดสุญญากาศ)
        _stroke(c, [(-74, -90), (-90, -30), (-82, 20)], 9, WHITE, 0.8)   # แสงสะท้อน
        if broken > 0:
            _stroke(c, [(20, -120), (40, -80), (28, -60), (60, -30)], 3, INK, broken)


def candle(g, x, y, sc=1.0, t=0.0, lit=True):
    c = g.c
    with g.at(x, y, sc):
        if lit:
            rg = cairo.RadialGradient(0, -230, 0, 0, -230, 140)
            rg.add_color_stop_rgba(0, *GLOW, 0.35)
            rg.add_color_stop_rgba(1, *GLOW, 0)
            c.set_source(rg)
            c.arc(0, -230, 140, 0, 2 * math.pi)
            c.fill()
        _smooth_path(c, [(-70, 0), (-60, -24), (60, -24), (70, 0)])
        _shade(c, BRASS, 5, 0.3)
        _rr(c, -26, -190, 52, 170, 6)
        _shade(c, hexc("#f4ecd8"), 5, 0.25)
        _stroke(c, [(-18, -190), (-14, -160), (-20, -140)], 7, hexc("#f4ecd8"))
        _stroke(c, [(0, -190), (0, -206)], 3, INK, smooth=False)
        if lit:
            fl = 1 + 0.12 * math.sin(t * 11 + x) + 0.06 * math.sin(t * 27)
            with g.at(0, -206, 1, 0.08 * math.sin(t * 7 + x), sx=1, sy=fl):
                _smooth_path(c, [(0, -60), (16, -20), (12, 4), (0, 10), (-12, 4), (-16, -20)])
                _shade(c, AMBER, 4, 0)
                _smooth_path(c, [(0, -30), (7, -6), (0, 4), (-7, -6)])
                _shade(c, hexc("#fff1c4"), 0, 0)


def oil_lamp(g, x, y, sc=1.0, t=0.0):
    c = g.c
    with g.at(x, y, sc):
        rg = cairo.RadialGradient(0, -170, 0, 0, -170, 170)
        rg.add_color_stop_rgba(0, *GLOW, 0.3)
        rg.add_color_stop_rgba(1, *GLOW, 0)
        c.set_source(rg)
        c.arc(0, -170, 170, 0, 2 * math.pi)
        c.fill()
        _smooth_path(c, [(-80, 0), (-90, -40), (-60, -100), (60, -100), (90, -40), (80, 0)])
        _shade(c, hexc("#b8473a"), 5, 0.3)
        _rr(c, -30, -122, 60, 24, 4)
        _shade(c, BRASS, 4, 0.2)
        fl = 1 + 0.1 * math.sin(t * 10 + x)
        with g.at(0, -150, 1, sx=1, sy=fl):
            _smooth_path(c, [(0, -40), (12, -12), (0, 6), (-12, -12)])
            _shade(c, AMBER, 3, 0)
        _smooth_path(c, [(-34, -118), (-46, -200), (-28, -270), (28, -270), (46, -200), (34, -118)])
        c.set_source_rgba(*GLASS)
        c.fill_preserve()
        c.set_source_rgba(*INK)
        c.set_line_width(5)
        c.stroke()


def flame(g, x, y, s=1.0, t=0.0, col=None):
    with g.at(x, y, s, 0.1 * math.sin(t * 8 + x), sx=s, sy=s * (1 + 0.12 * math.sin(t * 13 + x))):
        _smooth_path(g.c, [(0, -120), (40, -50), (46, 10), (0, 40), (-46, 10), (-40, -50)])
        _shade(g.c, col or hexc("#f08a3a"), 5, 0.2)
        _smooth_path(g.c, [(0, -50), (20, -10), (0, 22), (-20, -10)])
        _shade(g.c, hexc("#ffd166"), 0, 0)


def bench(g, x0, x1, y):
    """โต๊ะทดลองไม้ยาว — y = ระดับพื้นโต๊ะ"""
    c = g.c
    _rr(c, x0, y, x1 - x0, 40, 6)
    _shade(c, WOOD, 6, 0.25, horiz=False)
    for lx in (x0 + 40, x1 - 80):
        _rr(c, lx, y + 40, 40, 1270 - y - 40, 4)
        _shade(c, WOOD2, 6, 0.3)


def jar(g, x, y, sc=1.0, t=0.0, thread=True, glow=0.0):
    """โหลแก้วครอบ (bell jar) มีเส้นด้ายสีดำข้างใน — x,y = ฐาน"""
    c = g.c
    with g.at(x, y, sc):
        if glow > 0:
            rg = cairo.RadialGradient(0, -170, 0, 0, -170, 360)
            rg.add_color_stop_rgba(0, *GLOW, 0.5 * glow)
            rg.add_color_stop_rgba(1, *GLOW, 0)
            c.set_source(rg)
            c.arc(0, -170, 360, 0, 2 * math.pi)
            c.fill()
        _rr(c, -150, -20, 300, 40, 8)
        _shade(c, WOOD2, 6, 0.2)
        if thread:
            fc = (1, 0.88, 0.55, 1) if glow > 0.2 else (0.12, 0.1, 0.1, 1)
            _stroke(c, [(-30, -20), (-30, -130), (-36, -200), (-10, -240), (10, -240), (36, -200), (30, -130), (30, -20)], 5, fc)
        _smooth_path(c, [(-120, -20), (-126, -220), (-90, -320), (0, -346), (90, -320), (126, -220), (120, -20)])
        c.set_source_rgba(*GLASS)
        c.fill_preserve()
        c.set_source_rgba(*INK)
        c.set_line_width(6)
        c.stroke()
        c.new_path()
        c.arc(0, -360, 18, 0, 2 * math.pi)
        _shade(c, GLASS[:3] + (0.9,), 5, 0)
        _stroke(c, [(-96, -260), (-102, -120)], 10, WHITE, 0.8)


def vacuum_pump(g, x, y, sc=1.0, t=0.0):
    """ปั๊มสุญญากาศปรอท (Sprengel) — ท่อแก้วยาวบนขาตั้งไม้"""
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -110, -40, 220, 40, 6)
        _shade(c, WOOD2, 5, 0.2)
        _rr(c, -16, -620, 32, 580, 6)
        _shade(c, WOOD, 5, 0.25)
        for tx in (-50, 50):
            _stroke(c, [(tx, -60), (tx, -560)], 12, INK, smooth=False)
            _stroke(c, [(tx, -60), (tx, -560)], 6, (0.88, 0.94, 0.98, 1), smooth=False)
            for k in range(5):   # หยดปรอทไหลลง
                yy = -560 + ((t * 160 + k * 100 + tx) % 500)
                g.circle(tx, yy, 5, hexc("#9aa3ad"), 2)
        c.new_path()
        c.arc(0, -600, 56, 0, 2 * math.pi)
        c.set_source_rgba(*GLASS)
        c.fill_preserve()
        c.set_source_rgba(*INK)
        c.set_line_width(5)
        c.stroke()


def clock(g, x, y, r, t_hours, sc=1.0):
    """นาฬิกาแขวน — t_hours = เวลาที่ผ่านไป (เข็มยาวหมุน 1 รอบ/ชม.)"""
    c = g.c
    with g.at(x, y, sc):
        c.new_path()
        c.arc(0, 0, r + 22, 0, 2 * math.pi)
        _shade(c, WOOD, 7, 0.3)
        c.new_path()
        c.arc(0, 0, r, 0, 2 * math.pi)
        _shade(c, hexc("#fbf6ea"), 5, 0.1)
        for i in range(12):
            a = i * math.pi / 6
            l = 0.82 if i % 3 else 0.74
            _stroke(c, [(math.sin(a) * r * l, -math.cos(a) * r * l), (math.sin(a) * r * 0.92, -math.cos(a) * r * 0.92)],
                    6 if i % 3 == 0 else 3, INK, smooth=False)
        am = t_hours * 2 * math.pi
        ah = (t_hours + 10) / 12 * 2 * math.pi
        _stroke(c, [(0, 0), (math.sin(ah) * r * 0.5, -math.cos(ah) * r * 0.5)], 12, INK, smooth=False)
        _stroke(c, [(0, 0), (math.sin(am) * r * 0.78, -math.cos(am) * r * 0.78)], 7, INK, smooth=False)
        c.new_path()
        c.arc(0, 0, 12, 0, 2 * math.pi)
        _shade(c, RED, 3, 0)


def spool(g, x, y, sc=1.0, rot=0.0, unwind=0.0):
    """หลอดด้ายฝ้ายเย็บผ้า"""
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -60, -110, 120, 220, 10)
        _shade(c, WOOD, 5, 0.2)
        _rr(c, -46, -90, 92, 180, 4)
        _shade(c, hexc("#f4f0e6"), 4, 0.25)
        for k in range(9):
            _stroke(c, [(-46, -80 + k * 20), (46, -72 + k * 20)], 2, INK, 0.25, smooth=False)
        _rr(c, -80, -126, 160, 26, 8)
        _shade(c, WOOD2, 5, 0.1)
        _rr(c, -80, 100, 160, 26, 8)
        _shade(c, WOOD2, 5, 0.1)
        if unwind > 0:
            _stroke(c, [(46, 0), (120, 30 * unwind), (200 * unwind + 60, 80)], 4, INK)


def furnace(g, x, y, sc=1.0, t=0.0, heat=1.0):
    """เตาอบคาร์บอน (กล่องเหล็กหล่อ) — x,y = ฐาน"""
    c = g.c
    with g.at(x, y, sc):
        if heat > 0:
            rg = cairo.RadialGradient(0, -170, 0, 0, -170, 300)
            rg.add_color_stop_rgba(0, 1, 0.5, 0.2, 0.35 * heat)
            rg.add_color_stop_rgba(1, 1, 0.5, 0.2, 0)
            c.set_source(rg)
            c.arc(0, -170, 300, 0, 2 * math.pi)
            c.fill()
        _rr(c, -170, -340, 340, 340, 18)
        _shade(c, hexc("#4a4a50"), 7, 0.35)
        _rr(c, -100, -230, 200, 130, 10)
        _shade(c, (1, 0.45 + 0.1 * math.sin(t * 6), 0.15, 1) if heat > 0 else hexc("#2a2a2e"), 6, 0.2)
        _rr(c, -40, -420, 80, 90, 4)
        _shade(c, hexc("#3a3a40"), 6, 0.2)
        for k in range(3):
            if heat > 0:
                u = (t * 0.6 + k / 3) % 1
                g.circle(10 * math.sin(t + k), -440 - u * 220, 26 + 30 * u, (0.85, 0.85, 0.85, 0.6 * (1 - u)), 0)


def knife_switch(g, x, y, sc=1.0, k=0.0):
    """สวิตช์คันโยก (knife switch) — k 0 = เปิด (คันตั้ง), 1 = สับลงแล้ว"""
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -160, -40, 320, 80, 10)
        _shade(c, hexc("#2a2622"), 6, 0.2)
        for sx in (-1, 1):
            _rr(c, sx * 60 - 14, -70, 28, 40, 4)
            _shade(c, BRASS, 4, 0.2)
        a = -80 * (1 - k)
        with g.at(-60, -50, 1, a):
            _rr(c, -10, -10, 150, 20, 6)
            _shade(c, BRASS, 4, 0.2)
            _rr(c, 120, -22, 70, 44, 14)
            _shade(c, hexc("#1b1916"), 5, 0.1)


def newspaper(g, x, y, sc=1.0, rot=0.0, head1="", head2=""):
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -230, -160, 460, 320, 6)
        _shade(c, hexc("#f4efe2"), 6, 0.2)
        g.text("THE DAILY NEWS", 0, -122, 34, "kanit", INK)
        _stroke(c, [(-210, -98), (210, -98)], 3, INK, smooth=False)
        if head1:
            g.text(head1, 0, -50, 56, "kanit", INK, maxw=420)
        if head2:
            g.text(head2, 0, 14, 34, "kanitsb", INK, maxw=420)
        for k in range(4):
            _stroke(c, [(-210, 60 + k * 22), (-20, 60 + k * 22)], 6, LGREY, smooth=False)
            _stroke(c, [(20, 60 + k * 22), (210, 60 + k * 22)], 6, LGREY, smooth=False)


def city(g, x0, x1, y, t, lit=1.0, seed=3):
    """เมืองยามค่ำคืน: ตึกเรียงตัว หน้าต่างติดไฟตามลำดับตาม lit (0..1)"""
    c = g.c
    import random
    rnd = random.Random(seed)
    x = x0
    i = 0
    while x < x1:
        w = rnd.randint(110, 190)
        h = rnd.randint(240, 560)
        _rr(c, x, y - h, w, h, 4)
        _shade(c, hexc("#3a3f55"), 6, 0.3)
        cols = max(1, (w - 30) // 40)
        rows = max(1, (h - 40) // 60)
        for r in range(rows):
            for q in range(cols):
                wx, wy = x + 22 + q * 40, y - h + 26 + r * 60
                on = rnd.random() < lit * 1.15 and (q + r + i) % 7 != 3
                if on:
                    rg = cairo.RadialGradient(wx + 10, wy + 14, 0, wx + 10, wy + 14, 34)
                    rg.add_color_stop_rgba(0, *GLOW, 0.45)
                    rg.add_color_stop_rgba(1, *GLOW, 0)
                    c.set_source(rg)
                    c.arc(wx + 10, wy + 14, 34, 0, 2 * math.pi)
                    c.fill()
                _rr(c, wx, wy, 20, 28, 2)
                _shade(c, hexc("#ffd27a") if on else hexc("#232838"), 2, 0)
        x += w + rnd.randint(6, 22)
        i += 1


def moon(g, x, y, r=60):
    c = g.c
    c.new_path()
    c.arc(x, y, r, 0, 2 * math.pi)
    _shade(c, hexc("#f6e7a8"), 5, 0.15)
    for dx, dy, rr in ((-18, -10, 12), (16, 18, 9), (10, -24, 6)):
        g.circle(x + dx, y + dy, rr, hexc("#e8d48a"), 0)


def x_mark(g, x, y, s=1.0, a=1.0):
    with g.alpha(a):
        g.line([(x - 40 * s, y - 40 * s), (x + 40 * s, y + 40 * s)], 16 * s, RED, amp=0)
        g.line([(x + 40 * s, y - 40 * s), (x - 40 * s, y + 40 * s)], 16 * s, RED, amp=0)


def material(g, kind, x, y, sc=1.0, t=0.0):
    """วัสดุที่ทดลองทำไส้หลอด: platinum / fiber / hair / beard / thread"""
    c = g.c
    with g.at(x, y, sc):
        c.new_path()
        c.arc(0, 0, 110, 0, 2 * math.pi)
        _shade(c, WHITE, 6, 0.08)
        if kind == "platinum":
            for k in range(5):
                _stroke(c, [(-60, -40 + k * 20), (-20, -50 + k * 20), (20, -30 + k * 20), (60, -40 + k * 20)], 7, hexc("#b9bec6"))
            _rr(c, -36, 40, 72, 36, 6)
            _shade(c, hexc("#d9dde3"), 4, 0.3)
            g.text("Pt", 0, 58, 28, "kanit", INK)
        elif kind == "fiber":
            for k in range(-3, 4):
                _stroke(c, [(k * 14, 70), (k * 18 + 6, 0), (k * 22 - 4, -70)], 5, hexc("#6b8f3a"))
            _smooth_path(c, [(0, -80), (30, -40), (0, -20), (-30, -40)])
            _shade(c, hexc("#8fbf4a"), 4, 0.2)
        elif kind == "hair":
            for k in range(-2, 3):
                _stroke(c, [(k * 16 - 10, 70), (k * 10 + 14, 20), (k * 18 - 6, -30), (k * 8 + 12, -70)], 3.5, hexc("#3a2c22"))
        elif kind == "thread":
            spool(g, 0, 0, 0.6)


def stairs(g, x, y, n, k, step_w=120, step_h=90):
    """บันไดที่แต่ละขั้นเป็น 'ล้มเหลว' — k 0..1 จำนวนขั้นที่โผล่"""
    c = g.c
    shown = k * n
    for i in range(n):
        a = max(0.0, min(1.0, shown - i))
        if a <= 0:
            continue
        sx, sy = x + i * step_w, y - i * step_h
        with g.alpha(a):
            _rr(c, sx, sy - step_h, step_w, step_h * (i + 1), 4)
            _shade(c, hexc("#e8e2d4") if i < n - 1 else GOLD2, 5, 0.2)
            if i < n - 1:
                x_mark(g, sx + step_w / 2, sy - step_h / 2, 0.42, 0.85)


def heart(g, x, y, s=1.0, col=RED):
    with g.at(x, y, s):
        c = g.c
        c.new_path()
        c.move_to(0, 30)
        c.curve_to(-70, -20, -40, -70, 0, -36)
        c.curve_to(40, -70, 70, -20, 0, 30)
        _shade(c, col, 5, 0.2)
