"""ตัวละครและพร็อพ: รัชกาลที่ 5 เสด็จสวรรคต 23 ต.ค. 1910 — วาดอย่างสุภาพ สง่างาม (ไม่ใช้ท่าทาง/สีหน้าตลก)"""
import math

import cairo

from gfx import GOLD, GOLD2, GREY, INK, LGREY, NAVY, RED, WHITE, hexc
from people import Look, _rr, _shade, _smooth_path, _stroke

BRONZE = hexc("#6b5a3e")
MARBLE = hexc("#e9e6df")
GLOW = (1.0, 0.82, 0.45)
AMBER = hexc("#f2a93b")
MOURN = hexc("#2b2826")

# รัชกาลที่ 5 (พระชนมายุ 57): พระมัสสุงอนเรียว ผมสั้นแสกข้าง ฉลองพระองค์ปกตั้งสีขาว กระดุมทอง
# สายสะพาย ดาราเครื่องราชฯ ผ้าม่วง ถุงเท้าขาว
RAMA5 = Look(hair="part", hair_col=hexc("#2e2a28"), suit=hexc("#f4f2ec"), collar=hexc("#f4f2ec"), outfit="tunic",
              sash=hexc("#e6b54a"), stars=3, pants=hexc("#4a3a6a"), facial="mustache", w=58, jaw=0.5, jowls=0.15,
              nose=1.0, brow=0.6, age=0.5, build=1.0, height=1.0, skin=hexc("#e8b994"))
# ประชาชนในชุดไว้ทุกข์ (ดำ/ขาว)
TH_SKIN = [hexc("#e2b08a"), hexc("#d6a07a"), hexc("#e8bc98"), hexc("#cf9a72")]
MOURNERS = [
    Look(hair="crew", hair_col=hexc("#221e1c"), outfit="tee", suit=MOURN, pants=MOURN, skin=TH_SKIN[0], w=56, age=0.4),
    Look(hair="bun", hair_col=hexc("#221e1c"), outfit="dress", suit=MOURN, skin=TH_SKIN[1], w=54, age=0.3, height=0.93),
    Look(hair="short", hair_col=hexc("#2e2a28"), outfit="tee", suit=WHITE, pants=MOURN, skin=TH_SKIN[2], w=57, age=0.6),
    Look(hair="bun", hair_col=hexc("#5a5550"), outfit="dress", suit=WHITE, skin=TH_SKIN[3], w=54, age=0.8, height=0.9),
    Look(hair="buzz", hair_col=hexc("#221e1c"), outfit="tee", suit=MOURN, pants=hexc("#3a3a40"), skin=TH_SKIN[1], w=56,
         age=0.2, height=0.62, headsc=1.4),
]
# คนปัจจุบัน (มาวางพวงมาลา)
TODAY = [
    Look(hair="part", hair_col=hexc("#221e1c"), suit=hexc("#f4f2ec"), tie=hexc("#d9a441"), skin=TH_SKIN[0], w=57),
    Look(hair="long", hair_col=hexc("#221e1c"), outfit="dress", suit=hexc("#e8c45a"), skin=TH_SKIN[2], w=54,
         height=0.93),
    Look(hair="crew", hair_col=hexc("#221e1c"), outfit="tee", suit=hexc("#e8c45a"), pants=hexc("#3a3a40"),
         skin=TH_SKIN[3], w=56),
    Look(hair="buzz", hair_col=hexc("#221e1c"), outfit="tee", suit=hexc("#f4f2ec"), pants=hexc("#3f6496"),
         skin=TH_SKIN[1], w=56, height=0.62, headsc=1.4),
]
SLAVES = [
    Look(hair="buzz", hair_col=hexc("#221e1c"), outfit="tee", suit=hexc("#b9a88a"), pants=hexc("#7a6a52"),
         skin=TH_SKIN[3], w=56, age=0.5),
    Look(hair="bun", hair_col=hexc("#221e1c"), outfit="dress", suit=hexc("#a8977a"), skin=TH_SKIN[1], w=54, age=0.4,
         height=0.92),
    Look(hair="buzz", hair_col=hexc("#221e1c"), outfit="tee", suit=hexc("#b9a88a"), pants=hexc("#7a6a52"),
         skin=TH_SKIN[0], w=56, height=0.62, headsc=1.4),
]


def candle(g, x, y, sc=1.0, t=0.0):
    c = g.c
    with g.at(x, y, sc):
        rg = cairo.RadialGradient(0, -230, 0, 0, -230, 140)
        rg.add_color_stop_rgba(0, *GLOW, 0.35)
        rg.add_color_stop_rgba(1, *GLOW, 0)
        c.set_source(rg)
        c.arc(0, -230, 140, 0, 2 * math.pi)
        c.fill()
        _smooth_path(c, [(-60, 0), (-50, -22), (50, -22), (60, 0)])
        _shade(c, GOLD, 5, 0.3)
        _rr(c, -24, -190, 48, 170, 6)
        _shade(c, hexc("#f4ecd8"), 5, 0.25)
        _stroke(c, [(0, -190), (0, -206)], 3, INK, smooth=False)
        fl = 1 + 0.12 * math.sin(t * 11 + x) + 0.06 * math.sin(t * 27)
        with g.at(0, -206, 1, 0.08 * math.sin(t * 7 + x), sx=1, sy=fl):
            _smooth_path(c, [(0, -60), (16, -20), (12, 4), (0, 10), (-12, 4), (-16, -20)])
            _shade(c, AMBER, 4, 0)
            _smooth_path(c, [(0, -30), (7, -6), (0, 4), (-7, -6)])
            _shade(c, hexc("#fff1c4"), 0, 0)


def ribbon(g, x, y, sc=1.0, rot=0.0):
    """โบดำไว้ทุกข์"""
    c = g.c
    with g.at(x, y, sc, rot):
        for sx in (-1, 1):
            _smooth_path(c, [(0, 0), (sx * 40, 120), (sx * 18, 130), (sx * 4, 110)])
            _shade(c, MOURN, 5, 0.2)
        for sx in (-1, 1):
            _smooth_path(c, [(0, 0), (sx * 90, -60), (sx * 100, 10), (sx * 80, 40)])
            _shade(c, MOURN, 5, 0.25)
        c.new_path()
        c.arc(0, 0, 22, 0, 2 * math.pi)
        _shade(c, MOURN, 5, 0.1)


def portrait_frame(g, x, y, w, h, t=0.0, mourn=0.0):
    """พระบรมฉายาลักษณ์ (วาด) ในกรอบทอง + ผ้าระบายขาวดำไว้ทุกข์"""
    from people import person
    c = g.c
    with g.at(x, y):
        _rr(c, -w / 2 - 34, -h / 2 - 34, w + 68, h + 68, 14)
        _shade(c, GOLD, 6, 0.3)
        _rr(c, -w / 2, -h / 2, w, h, 6)
        _shade(c, hexc("#f6f1e4"), 5, 0.05)
        c.save()
        _rr(c, -w / 2, -h / 2, w, h, 6)
        c.clip()
        sc = h / 440
        person(g, 0, -h / 2 + 30 + 950 * sc, RAMA5, sc, mood="neutral", pose="down", shadow=False)
        c.restore()
        if mourn > 0:   # ผ้าระบายดำ-ขาวคล้องมุมบน
            k = mourn
            for sx in (-1, 1):
                _smooth_path(c, [(sx * (w / 2 + 34), -h / 2 - 34), (sx * (w / 2 + 34 - 90 * k), -h / 2 - 34),
                                 (sx * (w / 2 + 34), -h / 2 - 34 + 110 * k)])
                _shade(c, MOURN, 5, 0.2)
            with g.alpha(k):
                _smooth_path(c, [(-w / 2 - 34, -h / 2 - 34), (0, -h / 2 - 4), (w / 2 + 34, -h / 2 - 34), (0, -h / 2 - 22)])
                _shade(c, WHITE, 5, 0.15)
                ribbon(g, 0, -h / 2 - 44, 0.45)


def flower(g, x, y, r, col, rot=0.0):
    c = g.c
    with g.at(x, y, 1, rot):
        for i in range(5):
            a = i * 2 * math.pi / 5
            c.new_path()
            c.arc(r * 0.55 * math.cos(a), r * 0.55 * math.sin(a), r * 0.55, 0, 2 * math.pi)
            _shade(c, col, 3, 0.15)
        c.new_path()
        c.arc(0, 0, r * 0.35, 0, 2 * math.pi)
        _shade(c, GOLD2, 2.5, 0)


def wreath(g, x, y, sc=1.0, rot=0.0, text="น้อมรำลึก"):
    """พวงมาลาดอกไม้กลม + ริบบิ้น"""
    c = g.c
    cols = [hexc("#f2c94c"), WHITE, hexc("#e8a33d"), hexc("#f6e3a1")]
    with g.at(x, y, sc, rot):
        g.line([(-60, 140), (-110, 330)], 10, INK, amp=0)
        g.line([(60, 140), (110, 330)], 10, INK, amp=0)
        c.new_path()
        c.arc(0, 0, 150, 0, 2 * math.pi)
        _shade(c, hexc("#4f8a4a"), 6, 0.3)
        for i in range(18):
            a = i * 2 * math.pi / 18
            flower(g, 125 * math.cos(a), 125 * math.sin(a), 30, cols[i % 4], i * 20)
        c.new_path()
        c.arc(0, 0, 90, 0, 2 * math.pi)
        _shade(c, WHITE, 5, 0.05)
        _smooth_path(c, [(-70, 60), (70, 60), (80, 210), (40, 190), (0, 220), (-40, 190), (-80, 210)])
        _shade(c, hexc("#e6b54a"), 4, 0.2)
        if text:
            g.text(text, 0, 2, 30, "kanit", INK, maxw=170)


def statue(g, x, y, sc=1.0, t=0.0):
    """พระบรมรูปทรงม้า: แท่นหินอ่อนสูง + ม้าสำริด + พระบรมรูปทรงเครื่องแบบ — x,y = กลางฐาน"""
    c = g.c
    with g.at(x, y, sc):
        # ฐานขั้นบันได + แท่นสูง
        _rr(c, -330, -60, 660, 60, 4)
        _shade(c, MARBLE, 5, 0.25)
        _rr(c, -280, -110, 560, 50, 4)
        _shade(c, MARBLE, 5, 0.25)
        _rr(c, -200, -560, 400, 450, 6)
        _shade(c, MARBLE, 5, 0.3)
        _rr(c, -230, -600, 460, 44, 4)
        _shade(c, MARBLE, 5, 0.2)
        _rr(c, -110, -420, 220, 160, 4)
        _shade(c, BRONZE, 4, 0.2)
        g.text("๕", 0, -340, 70, "kanit", GOLD2)
        # ม้า (ยืนก้าวขาหน้า หันขวา)
        bc = BRONZE
        for lx, ld in ((-110, 0), (-70, 10), (90, -40), (130, 0)):
            if lx == 90:
                _stroke(c, [(lx, -760), (lx + 30, -700), (lx + 10, -640)], 26, INK, smooth=True)
                _stroke(c, [(lx, -760), (lx + 30, -700), (lx + 10, -640)], 18, bc, smooth=True)
            else:
                _stroke(c, [(lx, -760), (lx + 4, -680), (lx, -604)], 26, INK, smooth=False)
                _stroke(c, [(lx, -760), (lx + 4, -680), (lx, -604)], 18, bc, smooth=False)
        _smooth_path(c, [(-150, -790), (-120, -850), (60, -860), (150, -830), (170, -770), (120, -730), (-120, -730),
                         (-160, -760)])
        _shade(c, bc, 5, 0.35)
        _smooth_path(c, [(90, -850), (140, -930), (180, -965), (215, -950), (185, -860), (170, -780)])
        _shade(c, bc, 5, 0.3)   # คอ
        _smooth_path(c, [(172, -968), (205, -990), (272, -905), (262, -880), (225, -885), (182, -925)])
        _shade(c, bc, 5, 0.3)   # หัวม้า
        for ex in (190, 204):
            _smooth_path(c, [(ex - 6, -975), (ex, -1010), (ex + 8, -978)])
            _shade(c, bc, 3, 0.2)
        _stroke(c, [(100, -860), (140, -935), (178, -972)], 12, hexc("#3a3024"))   # แผงคอ
        _stroke(c, [(-150, -790), (-200, -720), (-190, -660)], 14, hexc("#3a3024"))   # หาง
        g.circle(214, -948, 5, INK, 0)
        # ผู้ทรงม้า
        _smooth_path(c, [(-50, -840), (40, -840), (30, -990), (-30, -990)])
        _shade(c, bc, 5, 0.3)
        _stroke(c, [(20, -960), (80, -900), (140, -910)], 18, INK)
        _stroke(c, [(20, -960), (80, -900), (140, -910)], 11, bc)
        _smooth_path(c, [(-10, -840), (20, -760), (0, -740), (-30, -820)])
        _shade(c, bc, 4, 0.3)
        c.new_path()
        c.arc(0, -1030, 40, 0, 2 * math.pi)
        _shade(c, bc, 5, 0.3)
        _smooth_path(c, [(-46, -1060), (0, -1110), (46, -1060), (60, -1050), (-60, -1050)])
        _shade(c, hexc("#4a3e2c"), 4, 0.2)   # หมวกยอดขนนก
        _stroke(c, [(0, -1100), (10, -1150), (-6, -1180)], 8, hexc("#4a3e2c"))
        # เงาแสงบนสำริด
        _stroke(c, [(-100, -835), (40, -845)], 5, (1, 1, 1), 0.25)


def throne_hall(g, x, y, sc=1.0):
    """พระที่นั่งอนันตสมาคม (โดมหินอ่อน) เป็นฉากหลังจาง ๆ"""
    c = g.c
    with g.at(x, y, sc), g.alpha(0.45):
        _rr(c, -520, -260, 1040, 260, 4)
        _shade(c, MARBLE, 4, 0.15)
        for i in range(9):
            _rr(c, -480 + i * 112, -230, 30, 200, 4)
            _shade(c, WHITE, 3, 0.1)
        _rr(c, -200, -420, 400, 160, 4)
        _shade(c, MARBLE, 4, 0.15)
        c.new_path()
        c.arc(0, -420, 170, math.pi, 2 * math.pi)
        c.close_path()
        _shade(c, hexc("#b9c7c2"), 4, 0.2)
        _rr(c, -18, -640, 36, 60, 4)
        _shade(c, MARBLE, 3, 0.1)
        for sx in (-1, 1):
            c.new_path()
            c.arc(sx * 420, -260, 70, math.pi, 2 * math.pi)
            c.close_path()
            _shade(c, hexc("#b9c7c2"), 4, 0.2)


def siam_disc(g, x, y, r, lost=0.0, t=0.0):
    """สยามเป็นวงกลม: ส่วนขอบ 'เสียสละ' หลุดออกไป แกนกลาง (เอกราช) ยังอยู่ — ภาพเชิงสัญลักษณ์ ไม่ใช่แผนที่จริง"""
    c = g.c
    with g.at(x, y):
        c.new_path()
        c.arc(0, 0, r, 0, 2 * math.pi)
        _shade(c, hexc("#f6e3a1"), 6, 0.2)
        for i, (a0, a1) in enumerate(((-2.6, -2.0), (0.3, 0.9), (1.9, 2.4), (-0.9, -0.4))):
            k = max(0.0, min(1.0, lost * 4 - i))
            if k <= 0:
                continue
            am = (a0 + a1) / 2
            d = 120 * k
            with g.at(d * math.cos(am), d * math.sin(am), 1, k * 18 * (1 if i % 2 else -1)):
                c.new_path()
                c.arc(0, 0, r, a0, a1)
                c.arc_negative(0, 0, r * 0.72, a1, a0)
                c.close_path()
                _shade(c, hexc("#d9d3c5"), 5, 0.2)
            c.new_path()
            c.arc(0, 0, r + 4, a0, a1)
            c.arc_negative(0, 0, r * 0.72, a1, a0)
            c.close_path()
            c.set_source_rgba(1, 1, 1, 1)
            c.fill()
        c.new_path()
        c.arc(0, 0, r * 0.72, 0, 2 * math.pi)
        c.set_source_rgba(*hexc("#b37a12")[:3], 0.8)
        c.set_line_width(5)
        c.stroke()


def gunboat(g, x, y, sc=1.0, t=0.0, flag="fr", flip=False):
    """เรือปืนกลไฟของมหาอำนาจ — x,y = แนวน้ำ"""
    c = g.c
    by = 6 * math.sin(t * 1.8 + x * 0.01)
    with g.at(x, y + by, sc, 1.2 * math.sin(t * 1.3 + x * 0.02), sx=-sc if flip else sc, sy=sc):
        _smooth_path(c, [(-260, -70), (240, -70), (300, -110), (230, 10), (-230, 10)])
        _shade(c, hexc("#4a4d55"), 6, 0.35)
        _rr(c, -120, -150, 220, 80, 6)
        _shade(c, hexc("#e9e6df"), 5, 0.2)
        _rr(c, -40, -250, 60, 110, 6)
        _shade(c, hexc("#2b2826"), 5, 0.2)
        for i in range(3):
            u = (t * 0.6 + i / 3) % 1
            g.circle(-10 - 80 * u, -270 - 120 * u, 20 + 30 * u, (0.7, 0.7, 0.72, 0.7 * (1 - u)), 0)
        _stroke(c, [(130, -90), (220, -120)], 14, INK, smooth=False)   # ปืนหัวเรือ
        g.line([(-200, -70), (-200, -300)], 6, INK, amp=0)
        cols = {"fr": (hexc("#2b4c9a"), WHITE, RED), "uk": (hexc("#2b3f7a"), RED, hexc("#2b3f7a"))}[flag]
        wv = 5 * math.sin(t * 6)
        for i, col in enumerate(cols):
            c.new_path()
            for p in [(-200 + i * 40, -300 + wv * i * 0.3), (-160 + i * 40, -300 + wv * (i + 1) * 0.3),
                      (-160 + i * 40, -230 + wv * (i + 1) * 0.3), (-200 + i * 40, -230 + wv * i * 0.3)]:
                c.line_to(*p)
            c.close_path()
            _shade(c, col, 3, 0.1)


def sea(g, y, t, x0=-500, x1=1600, h=600):
    c = g.c
    c.new_path()
    c.move_to(x0, y)
    for i in range(int((x1 - x0) / 20) + 1):
        xx = x0 + i * 20
        c.line_to(xx, y + 10 * math.sin(xx * 0.02 + t * 2))
    c.line_to(x1, y + h)
    c.line_to(x0, y + h)
    c.close_path()
    _shade(c, hexc("#bcd6e6"), 5, 0.15)


def ministry(g, x, y, sc=1.0, label="กระทรวง"):
    """อาคารกระทรวงทรงยุโรป-ไทย"""
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -220, -300, 440, 300, 4)
        _shade(c, hexc("#f2ead6"), 5, 0.2)
        c.new_path()
        for p in [(-250, -300), (0, -420), (250, -300)]:
            c.line_to(*p)
        c.close_path()
        _shade(c, hexc("#c45a3c"), 5, 0.25)
        for i in range(5):
            _rr(c, -190 + i * 84, -260, 40, 220, 4)
            _shade(c, WHITE, 3, 0.15)
        _rr(c, -30, -120, 60, 120, 20)
        _shade(c, hexc("#6e4528"), 4, 0.2)
        if label:
            g.label(label, 0, -340, 40)


def train(g, x, y, sc=1.0, t=0.0):
    """รถจักรไอน้ำ + ตู้โดยสาร — x,y = ระดับราง (หันขวา)"""
    c = g.c
    with g.at(x, y, sc):
        g.line([(-900, 0), (500, 0)], 8, INK, amp=0)
        for i in range(-900, 500, 60):
            _rr(c, i, 2, 30, 14, 2)
            _shade(c, hexc("#8a5a36"), 2, 0)
        for cx0 in (-760, -460):   # ตู้โดยสาร
            _rr(c, cx0 - 130, -200, 260, 150, 10)
            _shade(c, hexc("#3c8d4f"), 5, 0.3)
            for k in range(3):
                _rr(c, cx0 - 100 + k * 75, -175, 50, 50, 6)
                _shade(c, hexc("#fdf4dc"), 3, 0.1)
            for wx in (-80, 80):
                c.new_path()
                c.arc(cx0 + wx, -40, 34, 0, 2 * math.pi)
                _shade(c, INK, 4, 0)
        _rr(c, -280, -170, 330, 120, 50)   # หม้อน้ำ
        _shade(c, hexc("#2b2826"), 5, 0.3)
        _rr(c, -330, -260, 130, 210, 8)   # ห้องคนขับ
        _shade(c, RED, 5, 0.3)
        _rr(c, -310, -235, 90, 60, 6)
        _shade(c, hexc("#fdf4dc"), 3, 0.1)
        _rr(c, -10, -270, 50, 110, 6)   # ปล่องควัน
        _shade(c, hexc("#2b2826"), 5, 0.2)
        for i in range(4):
            u = (t * 0.8 + i / 4) % 1
            g.circle(15 - 160 * u, -300 - 140 * u, 22 + 40 * u, (0.82, 0.82, 0.84, 0.8 * (1 - u)), 3)
        _smooth_path(c, [(50, -50), (110, -20), (50, -10)])
        _shade(c, RED, 4, 0.2)
        for wx, wr in ((-260, 48), (-130, 48), (-10, 34)):
            with g.at(wx, -40, 1, -t * 200):
                c.new_path()
                c.arc(0, 0, wr, 0, 2 * math.pi)
                _shade(c, hexc("#c45a3c"), 5, 0.2)
                _stroke(c, [(-wr, 0), (wr, 0)], 4, INK, smooth=False)
                _stroke(c, [(0, -wr), (0, wr)], 4, INK, smooth=False)


def telegraph(g, x0, x1, y, t=0.0, n=3):
    """เสาโทรเลข + สายไฟ + สัญญาณวิ่ง"""
    c = g.c
    xs = [x0 + (x1 - x0) * i / (n - 1) for i in range(n)]
    for xx in xs:
        g.line([(xx, y), (xx, y - 420)], 12, hexc("#6e4528"), amp=0)
        g.line([(xx - 60, y - 380), (xx + 60, y - 380)], 9, hexc("#6e4528"), amp=0)
        g.circle(xx - 50, y - 392, 8, WHITE, 3)
        g.circle(xx + 50, y - 392, 8, WHITE, 3)
    for i in range(n - 1):
        pts = [(xs[i] + (xs[i + 1] - xs[i]) * u / 10, y - 392 + 40 * math.sin(math.pi * u / 10)) for u in range(11)]
        _stroke(c, pts, 3, INK)
    u = (t * 0.7) % 1
    seg_i = min(int(u * (n - 1)), n - 2)
    v = u * (n - 1) - seg_i
    px = xs[seg_i] + (xs[seg_i + 1] - xs[seg_i]) * v
    g.circle(px, y - 392 + 40 * math.sin(math.pi * v), 14, GOLD2, 4)
    g.label("· — ·", px, y - 450, 40, color=NAVY)


def school(g, x, y, sc=1.0):
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -240, -260, 480, 260, 4)
        _shade(c, hexc("#f6e3a1"), 5, 0.2)
        c.new_path()
        for p in [(-280, -260), (-180, -400), (180, -400), (280, -260)]:
            c.line_to(*p)
        c.close_path()
        _shade(c, hexc("#c45a3c"), 5, 0.25)
        for i in range(4):
            _rr(c, -200 + i * 110, -210, 70, 70, 4)
            _shade(c, WHITE, 3, 0.1)
        _rr(c, -40, -120, 80, 120, 4)
        _shade(c, hexc("#6e4528"), 4, 0.2)
        g.label("โรงเรียน", 0, -330, 38)


def book(g, x, y, sc=1.0, rot=0.0, col=None):
    c = g.c
    with g.at(x, y, sc, rot):
        for sx in (-1, 1):
            _smooth_path(c, [(0, 10), (sx * 110, -10), (sx * 110, -150), (0, -130)])
            _shade(c, WHITE, 5, 0.1 if sx < 0 else 0.25)
            for k in range(3):
                _stroke(c, [(sx * 20, -100 + k * 30), (sx * 90, -114 + k * 30)], 3, GREY, smooth=False)
        _stroke(c, [(0, 10), (0, -130)], 5, col or RED, smooth=False)


def chain(g, x0, y0, x1, y1, broken=0.0, n=9):
    """โซ่: broken>0 = ข้อกลางหลุดแยกออก"""
    c = g.c
    for i in range(n):
        u = (i + 0.5) / n
        x, y = x0 + (x1 - x0) * u, y0 + (y1 - y0) * u
        side = -1 if i < n / 2 else 1
        x += side * 160 * broken
        y += 60 * broken * abs(u - 0.5)
        with g.at(x, y, 1, (90 if i % 2 else 0) + side * 25 * broken):
            _rr(c, -38, -22, 76, 44, 22)
            c.set_source_rgba(*INK[:3], 1)
            c.set_line_width(14)
            c.stroke_preserve()
            c.set_source_rgba(*hexc("#8a8a90")[:3], 1)
            c.set_line_width(8)
            c.stroke()


def dove(g, x, y, sc=1.0, t=0.0):
    c = g.c
    fl = math.sin(t * 8)
    with g.at(x, y, sc):
        _smooth_path(c, [(-70, 0), (-20, -30), (50, -24), (90, -40), (80, -10), (40, 20), (-40, 20)])
        _shade(c, WHITE, 5, 0.15)
        _smooth_path(c, [(-10, -20), (-40, -90 * (0.4 + 0.6 * abs(fl))), (30, -70 * (0.4 + 0.6 * abs(fl))), (30, -20)])
        _shade(c, WHITE, 5, 0.2)
        g.circle(70, -30, 5, INK, 0)
        _smooth_path(c, [(88, -36), (106, -30), (88, -26)])
        _shade(c, GOLD, 3, 0)


def crown(g, x, y, sc=1.0, rot=0.0):
    """พระมหาพิชัยมงกุฎ (ทรงชฎายอดแหลม) — สัญลักษณ์อำนาจ"""
    c = g.c
    with g.at(x, y, sc, rot):
        _smooth_path(c, [(-90, 0), (90, 0), (70, -80), (40, -160), (14, -260), (0, -330), (-14, -260), (-40, -160),
                         (-70, -80)])
        _shade(c, GOLD, 6, 0.35)
        for yy, ww in ((-60, 74), (-130, 52), (-200, 32)):
            _stroke(c, [(-ww, yy), (ww, yy)], 5, hexc("#b37a12"), smooth=False)
        _rr(c, -100, -20, 200, 34, 8)
        _shade(c, GOLD2, 5, 0.2)
        for i in range(5):
            g.circle(-72 + i * 36, -3, 8, RED if i % 2 else hexc("#3c8d4f"), 2)


def heart(g, x, y, sc=1.0, col=RED, a=1.0):
    c = g.c
    if a <= 0 or sc <= 0:
        return
    with g.at(x, y, sc), g.alpha(a):
        c.new_path()
        c.move_to(0, 30)
        c.curve_to(-60, -10, -40, -60, 0, -30)
        c.curve_to(40, -60, 60, -10, 0, 30)
        c.close_path()
        _shade(c, col, 4, 0.2)


def arrow(g, x, y, sx, col, sc=1.0):
    """ลูกศรหนา ชี้ไปทาง sx (+1 ขวา / -1 ซ้าย)"""
    with g.at(x, y, sc):
        g.poly([(-sx * 70, -22), (sx * 10, -22), (sx * 10, -50), (sx * 70, 0), (sx * 10, 50), (sx * 10, 22),
                (-sx * 70, 22)], col, 5, amp=0)
