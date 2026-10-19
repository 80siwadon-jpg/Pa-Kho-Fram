"""ตัวละครและพร็อพ: อัลเฟรด โนเบล (เกิด 21 ต.ค. 1833) — คนแบบกึ่งเสมือนจริงจาก src/people.py"""
import math

import cairo

from gfx import GOLD, GOLD2, GREY, INK, LGREY, NAVY, RED, WHITE, hexc, lerp
from gfx import hn as _hn
from people import Look, _rr, _shade, _smooth_path, _stroke

PAPERC = hexc("#f4efe2")
DYN = hexc("#c8553d")
NITRO = (0.95, 0.85, 0.45)


def hn(*a):
    return (_hn(*a) + 1) / 2


# อัลเฟรด โนเบล: ผมเข้มหวีเสยหน้าผากกว้าง เคราดกเต็มคาง คิ้วหนา ตาลึก จมูกโด่ง สูทดำ โบว์
NOBEL = Look(hair="nixon", hair_col=hexc("#3a2c22"), suit=hexc("#22252c"), tie=hexc("#1b1916"), bowtie=True,
             facial="beard", w=58, jaw=0.45, nose=1.3, brow=1.4, age=0.55, build=0.95)
NOBEL_YOUNG = Look(hair="part", hair_col=hexc("#3a2c22"), suit=hexc("#3b3a3e"), shirt=hexc("#f7f4ec"),
                   tie=hexc("#1b1916"), outfit="vest", facial="mustache", w=56, jaw=0.4, nose=1.25, brow=1.2, age=0.2)
NOBEL_OLD = Look(hair="nixon", hair_col=hexc("#b9b4aa"), suit=hexc("#22252c"), tie=hexc("#1b1916"), bowtie=True,
                 facial="beard", w=58, jaw=0.45, nose=1.3, brow=1.2, age=0.85, build=0.92)
# เอมิล น้องชายคนเล็ก (อายุ 20)
EMIL = Look(hair="part", hair_col=hexc("#6b4a33"), suit=hexc("#5a4a3a"), shirt=WHITE, tie=hexc("#7a2e2e"),
            outfit="vest", w=54, age=0.0, nose=1.1, height=0.96)
# ลุดวิก พี่ชาย (เคราดก ผมบาง)
LUDVIG = Look(hair="nixon", hair_col=hexc("#5a4a3a"), suit=hexc("#2f3a4a"), tie=hexc("#1b1916"), bowtie=True,
              facial="beard", w=60, jaw=0.5, jowls=0.3, nose=1.2, age=0.6)
WORKERS = [
    Look(hair="short", hair_col=hexc("#6b4a33"), suit=hexc("#8a6a4a"), outfit="flannel", pants=hexc("#4a4038"),
         hat="bowler", facial="mustache", w=58, age=0.4),
    Look(hair="buzz", hair_col=hexc("#2b2622"), suit=hexc("#5a6b85"), outfit="tee", pants=hexc("#3a3a42"),
         w=56, age=0.3),
]


# ---------------------------------------------------------------- พร็อพ
def flask(g, x, y, sc=1.0, t=0.0, fill=NITRO, shake=0.0, rot=0.0):
    """ขวดแก้วไนโตรกลีเซอรีน (ของเหลวเหลืองใส) — x,y = ก้นขวด"""
    c = g.c
    sx = shake * 6 * math.sin(t * 40)
    with g.at(x + sx, y, sc, rot + shake * 4 * math.sin(t * 33)):
        _smooth_path(c, [(-30, -260), (30, -260), (30, -170), (110, -40), (100, 0), (-100, 0), (-110, -40), (-30, -170)])
        c.save()
        c.clip_preserve()
        lvl = -90 + 6 * math.sin(t * 3)
        c.new_path()
        c.rectangle(-140, lvl, 280, 200)
        c.set_source_rgba(*fill, 0.85)
        c.fill()
        c.restore()
        _smooth_path(c, [(-30, -260), (30, -260), (30, -170), (110, -40), (100, 0), (-100, 0), (-110, -40), (-30, -170)])
        c.set_source_rgba(0.86, 0.93, 0.98, 0.3)
        c.fill_preserve()
        c.set_source_rgba(*INK)
        c.set_line_width(6)
        c.stroke()
        _rr(c, -36, -290, 72, 34, 8)
        _shade(c, hexc("#a8763e"), 5, 0.2)
        _stroke(c, [(-60, -40), (-30, -120)], 8, WHITE, 0.7)
        g.text("NG", 0, -50, 34, "kanit", INK)


def dynamite(g, x, y, sc=1.0, rot=0.0, n=3, fuse=0.0, t=0.0):
    """มัดไดนาไมต์ (แท่งแดง) — fuse 0..1 ชนวนไหม้ไป"""
    c = g.c
    with g.at(x, y, sc, rot):
        for i in range(n):
            ox = (i - (n - 1) / 2) * 46
            _rr(c, ox - 22, -150, 44, 220, 10)
            _shade(c, DYN, 5, 0.3)
        _rr(c, -(n * 46) / 2 - 4, -40, n * 46 + 8, 28, 4)
        _shade(c, hexc("#2b2622"), 4, 0.1)
        g.text("DYNAMITE", 0, -90, 22, "kanit", WHITE) if n >= 3 else None
        if fuse < 1:
            L = 140 * (1 - fuse)
            pts = [(0, -150), (20, -150 - L * 0.4), (-10, -150 - L * 0.75), (14, -150 - L)]
            _stroke(c, pts, 5, INK)
            if fuse > 0:
                g.sparkle(pts[-1][0], pts[-1][1], 26 + 6 * math.sin(t * 30), (1, 0.75, 0.3, 1), 0)


def mountain(g, x0, x1, y, h, t=0.0, tunnel=0.0, blast=0.0):
    """ภูเขาหิน + อุโมงค์ (tunnel 0..1) + ฝุ่นระเบิด (blast 0..1)"""
    c = g.c
    _smooth_path(c, [(x0, y), (x0 + (x1 - x0) * 0.25, y - h * 0.7), (x0 + (x1 - x0) * 0.45, y - h),
                     (x0 + (x1 - x0) * 0.7, y - h * 0.75), (x1, y)])
    _shade(c, hexc("#9a8a7a"), 7, 0.3)
    for i in range(5):
        px = x0 + (x1 - x0) * (0.2 + 0.15 * i)
        _stroke(c, [(px, y - h * 0.3 - i * 20), (px + 40, y - h * 0.45 - i * 18)], 4, INK, 0.3)
    if tunnel > 0:
        cx = (x0 + x1) / 2
        r = 110 * tunnel
        c.new_path()
        c.arc(cx, y, r, math.pi, 2 * math.pi)
        c.close_path()
        _shade(c, hexc("#2b2622"), 6, 0)
    if blast > 0:
        for i in range(8):
            a = math.pi + i * math.pi / 7
            rr = 160 * blast
            g.circle((x0 + x1) / 2 + math.cos(a) * rr, y - h * 0.4 + math.sin(a) * rr * 0.7,
                     50 + 50 * blast * hn(i, 3), (0.85, 0.82, 0.78, 0.8 * (1 - blast * 0.6)), 0)


def boom(g, x, y, r, k, t=0.0):
    """แสงวาบระเบิด (ไม่มีภาพความรุนแรง) — k 0..1"""
    if k <= 0:
        return
    c = g.c
    rr = r * (0.4 + 0.8 * k)
    rg = cairo.RadialGradient(x, y, 0, x, y, rr)
    rg.add_color_stop_rgba(0, 1, 0.97, 0.8, 1 - 0.6 * k)
    rg.add_color_stop_rgba(0.5, 1, 0.75, 0.35, 0.8 * (1 - k))
    rg.add_color_stop_rgba(1, 1, 0.6, 0.2, 0)
    c.set_source(rg)
    c.arc(x, y, rr, 0, 2 * math.pi)
    c.fill()
    for i in range(10):
        a = i * 2 * math.pi / 10 + hn(i, 4)
        g.line([(x + math.cos(a) * rr * 0.5, y + math.sin(a) * rr * 0.5), (x + math.cos(a) * rr, y + math.sin(a) * rr)],
               10, (1, 0.8, 0.3, 1 - k), amp=0)


def smoke(g, x, y, t, n=5, s=1.0, a=0.6):
    for i in range(n):
        u = (t * 0.35 + i / n) % 1
        g.circle(x + 40 * math.sin(t + i * 2) * s, y - u * 300 * s, (40 + 70 * u) * s, (0.55, 0.55, 0.58, a * (1 - u)), 0)


def newspaper(g, x, y, sc=1.0, rot=0.0, head="", sub="", fr=True, photo=True, k_head=1.0):
    """หนังสือพิมพ์ฝรั่งเศส 1888 พาดหัวข่าวมรณกรรม"""
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -300, -380, 600, 760, 6)
        _shade(c, PAPERC, 6, 0.2)
        g.text("LE JOURNAL" if fr else "NEWS", 0, -330, 52, "kanit", INK)
        _stroke(c, [(-270, -296), (270, -296)], 4, INK, smooth=False)
        g.text("1888", 0, -276, 22, "kanitm", GREY)
        if head and k_head > 0:
            g.text(head, 0, -200, 44, "kanit", INK, maxw=540, sc=k_head)
        if sub:
            g.text(sub, 0, -110, 30, "kanitsb", INK, maxw=540)
        if photo:   # กรอบรูปผู้ตาย (ขอบดำไว้ทุกข์)
            _rr(c, -110, -60, 220, 260, 4)
            _shade(c, hexc("#d9d2c2"), 8, 0.1)
        for k in range(7):
            _stroke(c, [(-270, 240 + k * 18), (270 - (k == 6) * 200, 240 + k * 18)], 6, LGREY, smooth=False)
            if k < 5:
                _stroke(c, [(130, -40 + k * 40), (270, -40 + k * 40)], 6, LGREY, smooth=False)
                _stroke(c, [(-270, -40 + k * 40), (-130, -40 + k * 40)], 6, LGREY, smooth=False)


def will_doc(g, x, y, sc=1.0, rot=0.0, write=1.0, seal=0.0, title="พินัยกรรม"):
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -240, -320, 480, 640, 8)
        _shade(c, PAPERC, 6, 0.15)
        g.text(title, 0, -250, 54, "kanit", INK)
        g.text("1895", 0, -190, 30, "kanitm", GREY)
        n = int(9 * write)
        for k in range(n):
            w = 380 if k % 3 else 300
            _stroke(c, [(-190, -130 + k * 40), (-190 + w, -130 + k * 40 + 2 * math.sin(k))], 4, NAVY, 0.8)
        if write >= 1:
            _stroke(c, [(60, 240), (90, 210), (110, 250), (140, 214), (170, 246), (200, 226)], 4, INK)
        if seal > 0:
            with g.at(-130, 230, seal):
                g.circle(0, 0, 60, RED, 5)
                g.star(0, 0, 30, hexc("#e08070"), 3)


def medal(g, x, y, r, sc=1.0, rot=0.0, label=""):
    c = g.c
    with g.at(x, y, sc, rot):
        c.new_path()
        c.arc(0, 0, r, 0, 2 * math.pi)
        _shade(c, GOLD, 7, 0.3)
        c.new_path()
        c.arc(0, 0, r * 0.8, 0, 2 * math.pi)
        _shade(c, GOLD2, 4, 0.15)
        # หน้าด้านข้างโนเบล (ภาพนูน)
        _smooth_path(c, [(-r * 0.35, -r * 0.45), (r * 0.1, -r * 0.55), (r * 0.3, -r * 0.3), (r * 0.4, -r * 0.05),
                         (r * 0.25, r * 0.1), (r * 0.3, r * 0.4), (-r * 0.1, r * 0.55), (-r * 0.4, r * 0.3)])
        _shade(c, hexc("#d9a441"), 3, 0.3)
        if label:
            g.label(label, 0, r + 50, 40)


def globe(g, x, y, r, t=0.0):
    c = g.c
    c.new_path()
    c.arc(x, y, r, 0, 2 * math.pi)
    _shade(c, hexc("#8fb8de"), 6, 0.3)
    c.save()
    c.arc(x, y, r, 0, 2 * math.pi)
    c.clip()
    for i in range(5):
        cx = x + ((i * 0.37 + t * 0.08) % 1 * 2.4 - 1.2) * r
        g.blob(cx, y + (hn(i, 7) - 0.5) * r * 1.2, r * 0.3, r * 0.2, hexc("#c9b083"), 0, 3 + i)
    c.restore()
    c.new_path()
    c.arc(x, y, r, 0, 2 * math.pi)
    c.set_source_rgba(*INK)
    c.set_line_width(6)
    c.stroke()


def coin_stack(g, x, y, n, sc=1.0):
    with g.at(x, y, sc):
        for i in range(n):
            _rr(g.c, -60, -i * 22 - 22, 120, 22, 10)
            _shade(g.c, GOLD, 4, 0.2)


def icon(g, kind, x, y, s=1.0, k=1.0):
    """ไอคอนสาขารางวัล: physics/chem/med/lit/peace"""
    c = g.c
    with g.at(x, y, s * k):
        c.new_path()
        c.arc(0, 0, 90, 0, 2 * math.pi)
        _shade(c, WHITE, 6, 0.05)
        if kind == "physics":
            for i in range(3):
                with g.at(0, 0, 1, i * 60):
                    c.new_path()
                    c.save()
                    c.scale(1, 0.38)
                    c.arc(0, 0, 60, 0, 2 * math.pi)
                    c.restore()
                    c.set_source_rgba(*INK)
                    c.set_line_width(4)
                    c.stroke()
            g.circle(0, 0, 12, NAVY, 3)
        elif kind == "chem":
            flask(g, 0, 50, 0.38, fill=(0.4, 0.75, 0.5))
        elif kind == "med":
            _rr(c, -18, -55, 36, 110, 4)
            _shade(c, RED, 4, 0)
            _rr(c, -55, -18, 110, 36, 4)
            _shade(c, RED, 4, 0)
        elif kind == "lit":
            for sx in (-1, 1):
                _smooth_path(c, [(0, -30), (sx * 60, -40), (sx * 60, 40), (0, 50)])
                _shade(c, PAPERC, 4, 0.1)
            _stroke(c, [(0, -30), (0, 50)], 4, INK, smooth=False)
        elif kind == "peace":
            _smooth_path(c, [(-50, 10), (-10, -30), (40, -40), (60, -20), (20, 0), (40, 30), (-20, 30)])
            _shade(c, WHITE, 4, 0.15)
            _stroke(c, [(30, -10), (70, 10)], 5, hexc("#4f8a3a"))


def candle(g, x, y, sc=1.0, t=0.0):
    c = g.c
    with g.at(x, y, sc):
        rg = cairo.RadialGradient(0, -230, 0, 0, -230, 160)
        rg.add_color_stop_rgba(0, 1, 0.75, 0.3, 0.35)
        rg.add_color_stop_rgba(1, 1, 0.75, 0.3, 0)
        c.set_source(rg)
        c.arc(0, -230, 160, 0, 2 * math.pi)
        c.fill()
        _rr(c, -26, -190, 52, 190, 6)
        _shade(c, hexc("#f4ecd8"), 5, 0.25)
        fl = 1 + 0.12 * math.sin(t * 11 + x)
        with g.at(0, -206, 1, 0.08 * math.sin(t * 7), sx=1, sy=fl):
            _smooth_path(c, [(0, -60), (16, -20), (12, 4), (0, 10), (-12, 4), (-16, -20)])
            _shade(c, hexc("#ffb347"), 4, 0)


def desk(g, x0, x1, y):
    c = g.c
    _rr(c, x0, y, x1 - x0, 40, 6)
    _shade(c, hexc("#7a5230"), 6, 0.25, horiz=False)
    for lx in (x0 + 40, x1 - 80):
        _rr(c, lx, y + 40, 40, 1270 - y - 40, 4)
        _shade(c, hexc("#5a3a22"), 6, 0.3)


def quill(g, x, y, sc=1.0, rot=0.0):
    c = g.c
    with g.at(x, y, sc, rot):
        _smooth_path(c, [(0, 0), (30, -80), (70, -200), (40, -210), (10, -120)])
        _shade(c, WHITE, 4, 0.2)
        _stroke(c, [(0, 0), (50, -200)], 3, INK)
