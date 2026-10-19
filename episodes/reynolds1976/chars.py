"""ตัวละครและพร็อพ: วันเกิดไรอัน เรย์โนลด์ส 23 ต.ค. 1976 (ฮีโร่ชุดแดงเป็นภาพการ์ตูนทั่วไป ไม่ใช้โลโก้จริง)"""
import math

from gfx import GOLD, GOLD2, GREY, INK, NAVY, RED, WHITE, hexc
from people import Look, _rr, _shade, _smooth_path, _stroke

DP_RED = hexc("#b8232e")
GL_GREEN = hexc("#2f9a4f")

# ไรอัน เรย์โนลด์ส: ผมสั้นเสยน้ำตาลเข้มแซมเทา หนวดเคราขึ้นบาง ๆ กรามคม สูทดำ เชิ้ตขาว เนกไทเทาลายจุด
RYAN = Look(hair="slick", hair_col=hexc("#3f342c"), suit=hexc("#1f1f24"), tie=hexc("#5a6270"), stubble=0.7, w=56,
            jaw=0.65, nose=1.05, brow=1.0, age=0.35)
RYAN_YOUNG = Look(hair="short", hair_col=hexc("#4a3a2c"), outfit="tee", suit=hexc("#3c8d9f"), pants=hexc("#3f5f8a"),
                  w=55, jaw=0.55, age=0.05, height=0.62, headsc=1.4)
# ฮีโร่ชุดแดงปากเก่ง (หน้ากากแดงคลุมทั้งหัว)
HERO = Look(hair="bald", hair_col=DP_RED, skin=DP_RED, outfit="tee", suit=DP_RED, pants=DP_RED, shoes=hexc("#2b2622"),
            w=56, jaw=0.5, brow=0.0, age=0.0)
EXECS = [
    Look(hair="part", hair_col=hexc("#9a948a"), suit=hexc("#2f3a4a"), tie=hexc("#2b3f63"), glasses="thin", w=58,
         age=0.7, jowls=0.4),
    Look(hair="bald", hair_col=hexc("#9a948a"), suit=hexc("#3b3f48"), tie=hexc("#7a2e2e"), w=60, age=0.75, jowls=0.5),
    Look(hair="bun", hair_col=hexc("#5a4a3a"), outfit="dress", suit=hexc("#4a3a5a"), w=54, age=0.5, height=0.93),
]
FANS = [
    Look(hair="short", hair_col=hexc("#2b2622"), outfit="hoodie", suit=hexc("#e8892e"), pants=hexc("#3f5f8a"), w=56),
    Look(hair="long", hair_col=hexc("#5a3a22"), outfit="tee", suit=DP_RED, pants=hexc("#2f3a4a"), w=54, height=0.92),
    Look(hair="afro", hair_col=hexc("#221e1c"), outfit="tee", suit=hexc("#3c8d9f"), pants=hexc("#3a3a40"), w=56,
         skin=hexc("#8a5a3c")),
]


def mask_eyes(g, x, y, sc=1.0):
    """ลายรอบตาสีดำ + ตาขาว ทับหน้ากากแดง (เรียกหลังวาด person HERO; x,y = กลางหน้า)"""
    c = g.c
    with g.at(x, y, sc):
        for sx in (-1, 1):
            _smooth_path(c, [(sx * 8, -20), (sx * 56, -34), (sx * 62, 4), (sx * 14, 10)])
            _shade(c, hexc("#1b1714"), 3, 0)
            _smooth_path(c, [(sx * 18, -12), (sx * 48, -20), (sx * 50, -2), (sx * 20, 2)])
            _shade(c, WHITE, 2, 0)


def hero(g, x, ground, sc=0.8, pose="down", turn=0.0, mood="smile", seed=3, k=0.0, pose2=None):
    from people import person
    person(g, x, ground, HERO, sc, mood=mood, pose=pose, pose2=pose2, k=k, turn=turn, seed=seed)
    hy = ground - 842 * sc * HERO.height
    mask_eyes(g, x + turn * 56 * sc * 0.28, hy - 8 * sc, sc)


def poison(g, x, y, sc=1.0, rot=0.0, label="BOX OFFICE"):
    """ขวดยาพิษ (ตรา 'ยาพิษบ็อกซ์ออฟฟิศ')"""
    c = g.c
    with g.at(x, y, sc, rot):
        _smooth_path(c, [(-40, -260), (40, -260), (40, -190), (110, -120), (110, 60), (-110, 60), (-110, -120),
                         (-40, -190)])
        _shade(c, hexc("#6a3f8a"), 6, 0.3)
        _rr(c, -50, -310, 100, 60, 10)
        _shade(c, hexc("#6e4528"), 5, 0.2)
        _rr(c, -90, -100, 180, 140, 10)
        _shade(c, hexc("#f4efe2"), 4, 0.1)
        g.circle(0, -60, 26, WHITE, 4)   # หัวกะโหลกการ์ตูน
        g.circle(-9, -62, 6, INK, 0)
        g.circle(9, -62, 6, INK, 0)
        g.line([(-30, -20), (30, 0)], 6, INK, amp=0)
        g.line([(-30, 0), (30, -20)], 6, INK, amp=0)
        g.text(label, 0, 25, 22, "kanit", RED, maxw=170)


def ring(g, x, y, sc=1.0, t=0.0, glow=1.0, dim=0.0):
    """แหวนพลังสีเขียว (ภาพทั่วไป)"""
    c = g.c
    with g.at(x, y, sc):
        if glow > 0:
            g.sunburst(0, -60, 90, 200, 12, t * 10, 8, (0.4, 0.9, 0.5, 0.5 * glow * (1 - dim)))
        c.new_path()
        c.arc(0, 30, 70, 0, 2 * math.pi)
        c.set_source_rgba(*INK[:3], 1)
        c.set_line_width(34)
        c.stroke_preserve()
        c.set_source_rgba(*hexc("#8a9096")[:3], 1)
        c.set_line_width(24)
        c.stroke()
        _rr(c, -60, -120, 120, 90, 24)
        _shade(c, GL_GREEN if dim < 0.5 else hexc("#7a8a7a"), 5, 0.3)
        g.circle(0, -75, 26, WHITE, 4)


def zipper_mouth(g, x, y, sc=1.0):
    """ปากถูกรูดซิปปิด (ไม่มีภาพรุนแรง)"""
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -120, -30, 240, 60, 30)
        _shade(c, hexc("#e8b0a0"), 5, 0.2)
        g.line([(-100, 0), (100, 0)], 6, INK, amp=0)
        for i in range(9):
            g.line([(-90 + i * 22, -10), (-90 + i * 22, 10)], 4, GREY, amp=0)
        _rr(c, 96, -18, 40, 36, 6)
        _shade(c, GOLD, 4, 0.2)


def flop_chart(g, x, y, w, h, k=1.0):
    c = g.c
    g.line([(x, y), (x + w, y)], 6, INK, amp=0)
    g.line([(x, y), (x, y - h)], 6, INK, amp=0)
    pts = [(0, 0.8), (0.3, 0.55), (0.55, 0.6), (0.8, 0.2), (1, 0.05)]
    n = max(2, int(len(pts) * k + 0.99))
    path = [(x + u * w, y - v * h) for u, v in pts[:n]]
    _stroke(c, path, 18, INK, smooth=False)
    _stroke(c, path, 12, RED, smooth=False)


def camera(g, x, y, sc=1.0, t=0.0, rec=True):
    """กล้องถ่ายหนังเล็ก ๆ + ไฟ REC"""
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -150, -90, 240, 180, 20)
        _shade(c, hexc("#2b2b30"), 6, 0.2)
        _smooth_path(c, [(90, -50), (190, -90), (190, 90), (90, 50)])
        _shade(c, hexc("#3a3a40"), 5, 0.2)
        for k in (-1, 1):
            g.circle(-90 + k * 0 + (k + 1) * 60, -150, 60, hexc("#2b2b30"), 5)
        if rec and int(t * 2) % 2 == 0:
            g.circle(-110, -50, 14, RED, 0)
            g.text("REC", -60, -50, 26, "kanit", RED)


def laptop(g, x, y, sc=1.0, t=0.0, leaked=0.0):
    """โน้ตบุ๊กเปิดคลิป + ป้าย LEAKED"""
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -230, -320, 460, 300, 16)
        _shade(c, hexc("#2b2b30"), 6, 0.2)
        _rr(c, -205, -295, 410, 250, 6)
        _shade(c, hexc("#3a4a5a"), 3, 0.1)
        g.poly([(-30, -210), (40, -170), (-30, -130)], WHITE, 4, amp=0)   # ปุ่มเล่น
        _smooth_path(c, [(-280, -20), (280, -20), (300, 20), (-300, 20)])
        _shade(c, hexc("#9aa1ab"), 5, 0.2)
        if leaked > 0:
            with g.at(110, -280, leaked * (1 + 0.6 * (1 - min(1, leaked))), -12):
                g.rrect(-130, -40, 260, 80, 10, (1, 1, 1, 0.9), 7, stroke=RED)
                g.text("LEAKED!", 0, 0, 46, "kanit", RED)


def rated_r(g, x, y, sc=1.0, rot=0.0):
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -110, -130, 220, 260, 16)
        _shade(c, WHITE, 6, 0.1)
        g.text("R", 0, -10, 170, "kanit", INK)
        g.text("RATED", 0, 95, 36, "kanit", INK)


def money_rain(g, t, n=9, x0=80, x1=1000, y0=320, y1=1200):
    for i in range(n):
        u = (t * 0.35 + i / n) % 1
        x = x0 + (x1 - x0) * ((i * 0.37) % 1) + 30 * math.sin(t * 2 + i)
        with g.at(x, y0 + (y1 - y0) * u, 1, 30 * math.sin(t * 3 + i)):
            g.rrect(-50, -26, 100, 52, 6, hexc("#9fd08a"), 4)
            g.text("$", 0, 0, 34, "kanit", hexc("#2f7a3f"))


def maple(g, x, y, sc=1.0, rot=0.0):
    """ใบเมเปิลแคนาดา"""
    with g.at(x, y, sc, rot):
        pts = []
        for i in range(11):
            a = -math.pi / 2 + i * 2 * math.pi / 11
            r = 100 if i % 2 == 0 else 50
            pts.append((r * math.cos(a), r * math.sin(a)))
        g.poly(pts, hexc("#d8323a"), 5, amp=0)
        g.line([(0, 40), (0, 130)], 10, hexc("#d8323a"), amp=0)


def star_walk(g, x, y, sc=1.0, name=""):
    """ดาวทองบนพื้น (ดาวดัง)"""
    with g.at(x, y, sc):
        g.rrect(-150, -150, 300, 300, 10, hexc("#d26a8a"), 6)
        g.star(0, -20, 100, GOLD, 5)
        if name:
            g.text(name, 0, 110, 30, "kanit", GOLD2, maxw=260)
