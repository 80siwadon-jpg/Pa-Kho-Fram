"""ตัวละครและพร็อพ: อันโตนี ฟาน เลเวนฮุก (เกิด 24 ต.ค. 1632) — กล้องจุลทรรศน์เลนส์เดี่ยว + จุลินทรีย์ตัวจิ๋ว"""
import math

from gfx import GOLD, GOLD2, GREY, INK, NAVY, RED, WHITE, hexc
from people import Look, _rr, _shade, _smooth_path, _stroke

BRASS = hexc("#d2a640")
PARCH = hexc("#f1e3c0")
WAX = hexc("#b8232e")
CLOTH = [hexc("#b8463a"), hexc("#3d6fa8"), hexc("#d9a441"), hexc("#4f8a52"), hexc("#7a4a8a")]
BUG = [hexc("#6cc4a1"), hexc("#f08a8a"), hexc("#8ab4f0"), hexc("#f2c25c"), hexc("#b48af0")]

# เลเวนฮุก: วิกผมลอนยาวสีน้ำตาล หนวดบางเหนือปาก ผ้าผูกคอขาว เสื้อคลุมยาวสีน้ำตาลแดง (ตามภาพของ Verkolje)
LEEU = Look(hair="periwig", hair_col=hexc("#6b4228"), suit=hexc("#a4542f"), outfit="vest", shirt=hexc("#8a4428"),
            tie=hexc("#8a4428"), cravat=True, facial="mustache", w=56, nose=1.12, brow=0.7,
            jaw=0.45, age=0.45)
# นักปราชญ์ราชสมาคมแห่งลอนดอน: วิกผมยาว ผ้าผูกคอ เสื้อคลุมเข้ม
SCHOLARS = [
    Look(hair="periwig", hair_col=hexc("#d9d5cc"), suit=hexc("#2b2622"), outfit="vest", shirt=hexc("#2b2622"),
         tie=hexc("#2b2622"), cravat=True, w=57, age=0.75, jowls=0.3),
    Look(hair="periwig", hair_col=hexc("#3a2a1e"), suit=hexc("#2f3a4a"), outfit="vest", shirt=hexc("#2f3a4a"),
         tie=hexc("#2f3a4a"), cravat=True, w=56, age=0.5, glasses="roundthin"),
    Look(hair="periwig", hair_col=hexc("#9a7a52"), suit=hexc("#4a2a3a"), outfit="vest", shirt=hexc("#4a2a3a"),
         tie=hexc("#4a2a3a"), cravat=True, w=56, age=0.6, facial="mustache"),
]


def microscope(g, x, y, sc=1.0, rot=0.0, t=0.0, glint=1.0):
    """กล้องจุลทรรศน์ของเลเวนฮุก: แผ่นทองเหลืองเล็ก ๆ มีเลนส์เม็ดจิ๋ว + เกลียวปรับ + เข็มเสียบตัวอย่าง"""
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -8, -10, 16, 290, 6)   # สกรูยาวด้านหลัง
        _shade(c, hexc("#a8823a"), 4, 0.3)
        for i in range(10):
            _stroke(c, [(-8, 20 + i * 24), (8, 30 + i * 24)], 2.5, INK, 0.5, smooth=False)
        _smooth_path(c, [(-70, -150), (70, -150), (80, -120), (80, 120), (70, 150), (-70, 150), (-80, 120), (-80, -120)])
        _shade(c, BRASS, 5, 0.3)
        for sx, sy in ((-56, -126), (56, -126), (-56, 126), (56, 126)):
            g.circle(sx, sy, 7, hexc("#a8823a"), 3)
        g.circle(0, -60, 18, hexc("#a8823a"), 4)
        g.circle(0, -60, 9, hexc("#cfe8f5"), 3)   # เลนส์เม็ดจิ๋ว
        if glint > 0:
            g.sparkle(10 + 4 * math.sin(t * 3), -72, 20 * glint)
        g.line([(30, -60), (110, -60)], 6, INK, amp=0)   # เข็มเสียบตัวอย่าง
        g.circle(110, -60, 9, hexc("#c99320"), 3)


def lens_bead(g, x, y, r=40, t=0.0):
    """เม็ดเลนส์แก้วใส"""
    c = g.c
    c.new_path()
    c.arc(x, y, r, 0, 2 * math.pi)
    _shade(c, hexc("#dcefff"), 4, 0.25)
    c.new_path()
    c.arc(x - r * 0.3, y - r * 0.3, r * 0.3, 0, 2 * math.pi)
    c.set_source_rgba(1, 1, 1, 0.9)
    c.fill()
    g.sparkle(x + r * 0.5, y - r * 0.6, r * 0.5 * (0.7 + 0.3 * math.sin(t * 4)))


def compound_scope(g, x, y, sc=1.0):
    """กล้องจุลทรรศน์แบบลำกล้องของยุคนั้น (เลนส์หลายชิ้น ภาพมัว)"""
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -110, -20, 220, 40, 10)
        _shade(c, hexc("#5a3a22"), 5, 0.2)
        _rr(c, -18, -260, 36, 240, 6)
        _shade(c, hexc("#8a6a3a"), 4, 0.2)
        _smooth_path(c, [(-50, -480), (50, -480), (40, -260), (-40, -260)])
        _shade(c, hexc("#2f4a6a"), 5, 0.25)
        for yy in (-440, -380, -320):
            _rr(c, -52, yy, 104, 16, 4)
            _shade(c, GOLD, 3, 0.1)
        _rr(c, -30, -520, 60, 44, 8)
        _shade(c, hexc("#2b2622"), 4, 0.1)


def cloth_bolts(g, x, y, sc=1.0, t=0.0):
    """ม้วนผ้าหลากสีวางซ้อนบนชั้นร้าน"""
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -260, -20, 520, 30, 6)
        _shade(c, hexc("#8a6a42"), 5, 0.2)
        for row in range(2):
            for i in range(4 - row):
                cx = -195 + i * 130 + row * 65
                cy = -80 - row * 110
                col = CLOTH[(i + row * 2) % 5]
                c.new_path()
                c.arc(cx, cy, 58, 0, 2 * math.pi)
                _shade(c, col, 5, 0.3)
                c.new_path()
                c.arc(cx, cy, 30, 0, 2 * math.pi)
                c.set_source_rgba(*INK[:3], 0.25)
                c.set_line_width(3)
                c.stroke()
                g.circle(cx, cy, 10, hexc("#e8dcc0"), 3)


def weave(g, x, y, r=220, dense=1.0):
    """ลายเส้นด้ายถักทอในวงเลนส์ (dense ต่ำ = ทอห่าง ๆ แบบผ้าโกง)"""
    c = g.c
    c.save()
    c.new_path()
    c.arc(x, y, r, 0, 2 * math.pi)
    c.clip()
    c.set_source_rgb(0.98, 0.95, 0.9)
    c.paint()
    gap = 34 / max(dense, 0.3)
    n = int(r * 2 / gap) + 2
    for i in range(n):
        o = -r + i * gap
        _stroke(c, [(x - r, y + o), (x + r, y + o)], 14, hexc("#c86a4a"), 0.9, smooth=False)
        _stroke(c, [(x + o, y - r), (x + o, y + r)], 14, hexc("#e8a060"), 0.9, smooth=False)
    c.restore()
    c.new_path()
    c.arc(x, y, r, 0, 2 * math.pi)
    c.set_source_rgba(*INK[:3], 1)
    c.set_line_width(10)
    c.stroke()


def lens_view(g, x, y, r, t, kind="bugs", n=1.0, seed=0):
    """วงกลมภาพผ่านเลนส์ + ของข้างใน"""
    c = g.c
    c.save()
    c.new_path()
    c.arc(x, y, r, 0, 2 * math.pi)
    c.clip()
    c.set_source_rgb(0.93, 0.97, 0.99)
    c.paint()
    if kind == "bugs":
        microbes(g, x, y, r, t, n, seed)
    elif kind == "blood":
        for i in range(14):
            a = i * 2.4 + seed
            bx, by = x + r * 0.7 * math.cos(a) * ((i * 37 % 10) / 10), y + r * 0.7 * math.sin(a) * ((i * 53 % 10) / 10)
            bx += 8 * math.sin(t + i)
            c.save()
            c.translate(bx, by)
            c.scale(1, 0.75)
            c.new_path()
            c.arc(0, 0, r * 0.12, 0, 2 * math.pi)
            c.restore()
            _shade(c, hexc("#e0555a"), 3, 0.3)
            c.save()
            c.translate(bx, by)
            c.scale(1, 0.75)
            c.new_path()
            c.arc(0, 0, r * 0.05, 0, 2 * math.pi)
            c.restore()
            c.set_source_rgba(0.7, 0.2, 0.25, 0.5)
            c.fill()
    c.restore()
    c.new_path()
    c.arc(x, y, r, 0, 2 * math.pi)
    c.set_source_rgba(*INK[:3], 1)
    c.set_line_width(12)
    c.stroke()
    c.new_path()
    c.arc(x, y, r - 16, 3.6, 4.4)
    c.set_source_rgba(1, 1, 1, 0.8)
    c.set_line_width(8)
    c.stroke()


def microbes(g, x, y, r, t, n=1.0, seed=0):
    """แอนิมอลคูลส์: แท่ง เกลียว กลม มีหาง ว่ายวน กระดิกหาง"""
    c = g.c
    cnt = int(22 * n)
    for i in range(cnt):
        ph = i * 1.7 + seed
        rr = r * (0.15 + 0.75 * ((i * 61 + seed * 7) % 100) / 100)
        a = ph + t * (0.4 + 0.25 * (i % 3)) * (1 if i % 2 else -1)
        bx, by = x + rr * math.cos(a), y + rr * math.sin(a) * 0.9
        col = BUG[i % 5]
        kind = i % 4
        dirn = a + math.pi / 2 * (1 if i % 2 else -1)
        c.save()
        c.translate(bx, by)
        c.rotate(dirn)
        s = r / 300
        if kind == 0:   # แท่ง
            _rr(c, -34 * s, -12 * s, 68 * s, 24 * s, 12 * s)
            _shade(c, col, 3, 0.25)
        elif kind == 1:   # เกลียว
            pts = [(-40 * s + k * 10 * s, 10 * s * math.sin(k * 1.4 + t * 8)) for k in range(9)]
            _stroke(c, pts, 9 * s + 4, INK)
            _stroke(c, pts, 9 * s, col)
        else:   # กลมมีหาง
            tail = [(-18 * s - k * 9 * s, 7 * s * math.sin(k * 1.2 + t * 12 + i)) for k in range(6)]
            _stroke(c, tail, 4, INK, smooth=True)
            c.new_path()
            c.arc(0, 0, 18 * s, 0, 2 * math.pi)
            _shade(c, col, 3, 0.25)
            for ex in (-1, 1):
                c.new_path()
                c.arc(6 * s, ex * 6 * s, 3 * s, 0, 2 * math.pi)
                c.set_source_rgba(*INK[:3], 1)
                c.fill()
        c.restore()


def tooth(g, x, y, sc=1.0, plaque=1.0):
    """ฟันการ์ตูน + คราบพลัคสีขาวขุ่นตามซอก"""
    c = g.c
    with g.at(x, y, sc):
        _smooth_path(c, [(-90, -120), (-40, -140), (0, -120), (40, -140), (90, -120), (100, 0), (70, 140), (40, 150),
                         (20, 40), (-20, 40), (-40, 150), (-70, 140), (-100, 0)])
        _shade(c, WHITE, 6, 0.15)
        if plaque > 0:
            for px, py in ((-80, 10), (85, -10), (-60, -100), (70, -100)):
                c.new_path()
                c.arc(px, py, 24 * plaque, 0, 2 * math.pi)
                c.set_source_rgba(0.93, 0.88, 0.6, 0.85)
                c.fill()


def letter(g, x, y, sc=1.0, rot=0.0, seal=True):
    """จดหมายรายงานพร้อมภาพสเก็ตช์ + ตราครั่ง"""
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -130, -170, 260, 340, 8)
        _shade(c, PARCH, 6, 0.15)
        for i in range(5):
            _stroke(c, [(-100, -130 + i * 30), (100 - 30 * (i % 2), -130 + i * 30)], 4, INK, 0.45, smooth=False)
        c.new_path()
        c.arc(0, 60, 56, 0, 2 * math.pi)
        c.set_source_rgba(*INK[:3], 0.7)
        c.set_line_width(4)
        c.stroke()
        for k in range(4):
            a = k * 1.6
            _stroke(c, [(20 * math.cos(a) - 10, 60 + 20 * math.sin(a)), (20 * math.cos(a) + 10, 60 + 20 * math.sin(a) + 6)],
                    5, INK, 0.7, smooth=False)
        if seal:
            g.circle(80, 140, 26, WAX, 4)


def windmill(g, x, y, sc=1.0, t=0.0):
    c = g.c
    with g.at(x, y, sc):
        _smooth_path(c, [(-70, 0), (-50, -300), (50, -300), (70, 0)])
        _shade(c, hexc("#9a6a4a"), 6, 0.25)
        _smooth_path(c, [(-60, -300), (0, -360), (60, -300)])
        _shade(c, hexc("#4a3a3a"), 6, 0.2)
        _rr(c, -20, -70, 40, 70, 18)
        _shade(c, hexc("#4a3a3a"), 4, 0)
        with g.at(0, -300, 1, math.degrees(t * 0.8)):
            for k in range(4):
                with g.at(0, 0, 1, k * 90):
                    _rr(c, -14, -250, 28, 250, 4)
                    _shade(c, hexc("#e8dcc0"), 4, 0.1)
                    for j in range(4):
                        _stroke(c, [(-14, -60 - j * 50), (14, -60 - j * 50)], 2.5, INK, 0.5, smooth=False)
            g.circle(0, 0, 16, hexc("#4a3a3a"), 4)


def dutch_houses(g, y, x0=-300, n=9, sc=1.0):
    """บ้านหน้าจั่วขั้นบันไดแบบเดลฟท์"""
    c = g.c
    cols = [hexc("#b8644a"), hexc("#8a4a3a"), hexc("#c9915a"), hexc("#7a5a4a")]
    for i in range(n):
        x = x0 + i * 200 * sc
        h = (300 + 60 * (i % 3)) * sc
        wd = 180 * sc
        pts = [(x, y), (x, y - h), (x + wd * 0.2, y - h), (x + wd * 0.2, y - h - 40 * sc), (x + wd * 0.4, y - h - 40 * sc),
               (x + wd * 0.4, y - h - 80 * sc), (x + wd * 0.6, y - h - 80 * sc), (x + wd * 0.6, y - h - 40 * sc),
               (x + wd * 0.8, y - h - 40 * sc), (x + wd * 0.8, y - h), (x + wd, y - h), (x + wd, y)]
        c.new_path()
        for p in pts:
            c.line_to(*p)
        c.close_path()
        _shade(c, cols[i % 4], 5, 0.2)
        for r in range(2):
            for k in range(2):
                _rr(c, x + wd * (0.18 + 0.4 * k), y - h + 50 * sc + r * 110 * sc, wd * 0.24, 70 * sc, 4)
                _shade(c, hexc("#f4f0e0"), 3, 0)


def cradle(g, x, y, sc=1.0, t=0.0):
    """เปลไม้ + ทารกห่อผ้า"""
    c = g.c
    with g.at(x, y, sc, 5 * math.sin(t * 2)):
        _smooth_path(c, [(-180, -120), (180, -120), (150, 0), (-150, 0)])
        _shade(c, hexc("#a8784a"), 6, 0.25)
        for sx in (-1, 1):
            c.new_path()
            c.arc(sx * 130, 20, 50, 0, math.pi)
            c.set_source_rgba(*INK[:3], 1)
            c.set_line_width(8)
            c.stroke()
        _smooth_path(c, [(-120, -120), (-110, -190), (60, -200), (110, -150), (100, -120)])
        _shade(c, hexc("#cfe0f0"), 5, 0.15)
        c.new_path()
        c.arc(-70, -190, 52, 0, 2 * math.pi)
        _shade(c, hexc("#f2c9a8"), 5, 0.15)
        _smooth_path(c, [(-122, -196), (-110, -240), (-70, -250), (-30, -240), (-18, -196), (-70, -226)])
        _shade(c, WHITE, 4, 0.1)
        for ex in (-88, -52):
            _stroke(c, [(ex - 7, -186), (ex, -182), (ex + 7, -186)], 3.5, INK)
        _stroke(c, [(-78, -165), (-70, -160), (-62, -165)], 3, INK)


def crossed(g, x, y, sc=1.0, k=1.0):
    """กากบาทแดง"""
    if k <= 0:
        return
    with g.at(x, y, sc * k):
        g.line([(-70, -70), (70, 70)], 16, RED, amp=0)
        g.line([(70, -70), (-70, 70)], 16, RED, amp=0)


def book(g, x, y, sc=1.0, rot=0.0, title="", col=hexc("#5a3a6a")):
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -110, -150, 220, 300, 10)
        _shade(c, col, 6, 0.25)
        _rr(c, -80, -90, 160, 60, 6)
        _shade(c, PARCH, 3, 0)
        if title:
            g.text(title, 0, -60, 34, fnt="kanit", color=INK)


def university(g, x, y, sc=1.0):
    """อาคารมหาวิทยาลัยเสาโรมัน"""
    c = g.c
    with g.at(x, y, sc):
        c.new_path()
        for p in [(-220, -260), (0, -360), (220, -260)]:
            c.line_to(*p)
        c.close_path()
        _shade(c, hexc("#e8e0cc"), 6, 0.2)
        _rr(c, -230, -260, 460, 30, 4)
        _shade(c, hexc("#d8d0bc"), 5, 0)
        for i in range(5):
            _rr(c, -190 + i * 90, -230, 30, 220, 4)
            _shade(c, WHITE, 4, 0.2)
        _rr(c, -240, -10, 480, 20, 4)
        _shade(c, hexc("#d8d0bc"), 5, 0)
        g.circle(0, -300, 24, GOLD, 4)


def key(g, x, y, sc=1.0, rot=0.0):
    c = g.c
    with g.at(x, y, sc, rot):
        c.new_path()
        c.arc(-120, 0, 60, 0, 2 * math.pi)
        c.new_sub_path()
        c.arc(-120, 0, 26, 0, 2 * math.pi)
        c.set_fill_rule(1)
        _shade(c, GOLD, 6, 0.25)
        c.set_fill_rule(0)
        _rr(c, -64, -16, 200, 32, 8)
        _shade(c, GOLD, 6, 0.25)
        for kx in (90, 120):
            _rr(c, kx - 10, 10, 20, 44, 4)
            _shade(c, GOLD, 5, 0.25)


def medicine(g, x, y, sc=1.0, t=0.0):
    """ขวดยา + ไม้กางเขนแดง (การแพทย์)"""
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -70, -200, 140, 200, 24)
        _shade(c, hexc("#dcefff"), 6, 0.2)
        _rr(c, -40, -250, 80, 56, 8)
        _shade(c, hexc("#3d6fa8"), 5, 0.2)
        _rr(c, -50, -140, 100, 90, 10)
        _shade(c, WHITE, 4, 0)
        _rr(c, -10, -130, 20, 70, 2)
        _shade(c, RED, 0, 0)
        _rr(c, -35, -105, 70, 20, 2)
        _shade(c, RED, 0, 0)


def drop(g, x, y, r, col):
    c = g.c
    _smooth_path(c, [(x, y - r * 1.6), (x + r * 0.9, y - r * 0.2), (x + r, y + r * 0.3), (x, y + r), (x - r, y + r * 0.3),
                     (x - r * 0.9, y - r * 0.2)])
    _shade(c, col, 5, 0.25)


def beetle(g, x, y, sc=1.0, t=0.0):
    c = g.c
    with g.at(x, y, sc):
        for sx in (-1, 1):
            for k in range(3):
                _stroke(c, [(sx * 30, -20 + k * 26), (sx * 70, -30 + k * 30 + 6 * math.sin(t * 9 + k))], 6, INK)
        c.new_path()
        c.save()
        c.scale(1, 1.3)
        c.arc(0, 0, 44, 0, 2 * math.pi)
        c.restore()
        _shade(c, hexc("#3c8d4f"), 6, 0.3)
        c.new_path()
        c.arc(0, -64, 24, 0, 2 * math.pi)
        _shade(c, hexc("#2b2622"), 5, 0.1)
        _stroke(c, [(0, -40), (0, 56)], 4, INK)
