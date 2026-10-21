"""ตัวละครและพร็อพ: ธีโอดอร์ โรสเวลต์ (เกิด 27 ต.ค. 1858) — ถูกยิงที่มิลวอกี 1912 แล้วปราศรัยต่อ
ไม่แสดงภาพการยิงโดน: ใช้เงามือปืน แสงวาบ และรอยเปื้อนเล็ก ๆ บนเสื้อแทน"""
import importlib.util
import math
import os

from gfx import GOLD, GOLD2, GREY, INK, NAVY, RED, WHITE, hexc
from people import Look, _rr, _shade, _smooth_path, _stroke


def _load(ep):
    spec = importlib.util.spec_from_file_location(f"{ep}_chars",
                                                  os.path.join(os.path.dirname(__file__), "..", ep, "chars.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


horse = _load("balaclava1854").horse
crowd_mass = _load("pentagon1967").crowd_mass

KHAKI = hexc("#b8a77a")
BROWN = hexc("#5a4632")
BLOOD = hexc("#a8323a")

# ธีโอดอร์ โรสเวลต์: ผมน้ำตาลเข้มแสกข้างหวีเรียบ หนวดหนาดกเต็มริมฝีปาก แว่นหนีบจมูกไร้กรอบ หน้ากว้าง กรามใหญ่ ล่ำ
TEDDY = Look(hair="part", hair_col=hexc("#4a3424"), suit=hexc("#2b2622"), shirt=WHITE, tie=hexc("#2b2f3a"), w=66,
             jaw=0.85, jowls=0.25, nose=1.0, brow=1.0, age=0.45, build=1.2, glasses="thin", facial="walrus")
TEDDY_RR = Look(hair="part", hair_col=hexc("#4a3424"), suit=KHAKI, shirt=hexc("#c9bd92"), tie=hexc("#2b4f8a"), w=64,
                jaw=0.8, age=0.3, build=1.15, glasses="thin", facial="walrus", hat="cowboy", hat_trim=BROWN)
TEDDY_KID = Look(hair="part", hair_col=hexc("#6b4a33"), outfit="vest", suit=hexc("#5a6a8a"), w=55, age=0.0,
                 height=0.6, headsc=1.45, build=0.75, glasses="thin")
TEDDY_FIT = Look(hair="part", hair_col=hexc("#4a3424"), outfit="tee", suit=WHITE, pants=hexc("#2b2f3a"), w=60,
                 age=0.05, build=1.15, glasses="thin")
FATHER = Look(hair="part", hair_col=hexc("#3a2a1e"), suit=hexc("#2b2622"), tie=INK, w=62, jaw=0.6, age=0.5,
              facial="beard", bowtie=True)
RIDERS = [
    Look(hair="short", hair_col=hexc("#3a2a1e"), suit=KHAKI, shirt=hexc("#c9bd92"), tie=hexc("#2b4f8a"), w=57,
         age=0.2, hat="cowboy", hat_trim=BROWN),
    Look(hair="crew", hair_col=hexc("#8a6a42"), suit=KHAKI, shirt=hexc("#c9bd92"), tie=hexc("#2b4f8a"), w=58,
         age=0.3, hat="cowboy", hat_trim=hexc("#7a6040"), facial="mustache"),
]
AIDE = Look(hair="part", hair_col=hexc("#2b2622"), suit=hexc("#3a3f48"), tie=hexc("#7a2e2e"), w=58, age=0.4,
            hat="bowler")


def bed(g, x, y, sc=1.0, t=0.0):
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -300, -120, 600, 90, 20)
        _shade(c, WHITE, 6, 0.15)
        _rr(c, -330, -260, 40, 260, 10)
        _shade(c, hexc("#8a5a3a"), 5, 0.2)
        _rr(c, 290, -180, 40, 180, 10)
        _shade(c, hexc("#8a5a3a"), 5, 0.2)
        _rr(c, -280, -170, 160, 60, 26)
        _shade(c, WHITE, 5, 0.1)
        b = 6 * math.sin(t * 5)
        _smooth_path(c, [(-150, -110), (-120, -150 - b), (280, -150 - b), (290, -110)])
        _shade(c, hexc("#9ac0e0"), 5, 0.15)


def wheeze(g, x, y, t, k=1.0):
    """เส้นหายใจหอบ"""
    for i in range(3):
        u = (t * 1.5 + i / 3) % 1
        g.arc(x + 40 * u, y - 20 * i, 30 + 20 * u, -60, 60, 5, (*GREY[:3], (1 - u) * k))


def brain(g, x, y, sc=1.0, t=0.0):
    with g.at(x, y, sc, 3 * math.sin(t * 2)):
        g.blob(0, 0, 130, 100, hexc("#f2b8c6"), 6, seed=4)
        for i in range(4):
            g.arc(-60 + i * 40, -10 + 20 * (i % 2), 30, 200, 340, 5, hexc("#c8788a"))
        g.line([(0, -90), (0, 90)], 5, hexc("#c8788a"), amp=0)


def dumbbell(g, x, y, sc=1.0, rot=0.0):
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -110, -10, 220, 20, 8)
        _shade(c, GREY, 4, 0.1)
        for sx in (-1, 1):
            _rr(c, sx * 110 - 30, -55, 60, 110, 14)
            _shade(c, hexc("#3a3f48"), 5, 0.2)


def glove(g, x, y, sc=1.0, rot=0.0):
    c = g.c
    with g.at(x, y, sc, rot):
        g.blob(0, 0, 80, 70, RED, 6, seed=2)
        g.blob(-60, 10, 34, 46, RED, 5, seed=3)
        _rr(c, -60, 50, 120, 60, 14)
        _shade(c, WHITE, 5, 0.1)


def mountain(g, x, y, sc=1.0, t=0.0):
    c = g.c
    with g.at(x, y, sc):
        c.new_path()
        for p in [(-320, 0), (-60, -420), (40, -320), (140, -460), (360, 0)]:
            c.line_to(*p)
        c.close_path()
        _shade(c, hexc("#9aa48a"), 6, 0.25)
        c.new_path()
        for p in [(140, -460), (100, -400), (150, -380), (190, -400)]:
            c.line_to(*p)
        c.close_path()
        _shade(c, WHITE, 3, 0)


def flag_us(g, x, y, w, h, t=0.0):
    g.flag(x, y, w, h, "us", t)


def stick(g, x, y, sc=1.0, rot=0.0):
    """ไม้พลองกระบองยักษ์"""
    c = g.c
    with g.at(x, y, sc, rot):
        _smooth_path(c, [(-24, 0), (-40, -420), (0, -470), (40, -420), (24, 0)])
        _shade(c, hexc("#8a5a3a"), 6, 0.3)
        for i in range(3):
            g.circle(-10 + 14 * (i % 2), -380 + i * 80, 8, hexc("#5a3a22"), 0)


def monopoly(g, x, y, sc=1.0, k=0.0):
    """ตึกกลุ่มทุนผูกขาด (ร้าวแตกตาม k)"""
    c = g.c
    with g.at(x, y, sc):
        for side in (-1, 1):
            off = side * 60 * k
            with g.at(off, 0, 1, side * 10 * k):
                c.new_path()
                if side < 0:
                    pts = [(-180, 0), (-180, -420), (0, -420), (-20, -300), (20, -200), (-10, -100), (10, 0)]
                else:
                    pts = [(10, 0), (-10, -100), (20, -200), (-20, -300), (0, -420), (180, -420), (180, 0)]
                for p in pts:
                    c.line_to(*p)
                c.close_path()
                _shade(c, hexc("#6a6f78"), 6, 0.25)
        if k < 0.3:
            g.text("TRUST", 0, -470, 60, "kanit", INK)
        for i in range(3):
            for j in range(4):
                _rr(c, -150 + i * 110 - 60 * k * (1 if i == 0 else 0), -380 + j * 90, 60, 50, 4)
                _shade(c, hexc("#f2d68a"), 3, 0)


def tree(g, x, y, sc=1.0, t=0.0):
    c = g.c
    with g.at(x, y, sc, 2 * math.sin(t * 1.5 + x)):
        _rr(c, -18, -140, 36, 140, 6)
        _shade(c, hexc("#7a4a2a"), 5, 0.2)
        c.new_path()
        for p in [(0, -420), (110, -140), (-110, -140)]:
            c.line_to(*p)
        c.close_path()
        _shade(c, hexc("#3c8d4f"), 6, 0.2)


def canal(g, x, y, sc=1.0, t=0.0):
    """คลองปานามา: ประตูน้ำ + เรือแล่นผ่านระหว่างสองฝั่ง"""
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -380, -120, 760, 120, 4)
        _shade(c, hexc("#bcd8ec"), 5, 0.1)
        for sx in (-1, 1):
            c.new_path()
            for p in [(sx * 380, -120), (sx * 380, -330), (sx * 140, -300), (sx * 110, -120)]:
                c.line_to(*p)
            c.close_path()
            _shade(c, hexc("#6b8f3a"), 6, 0.2)
        _rr(c, -110, -150, 22, 150, 4)
        _shade(c, hexc("#7a4a2a"), 4, 0)
        bx = -60 + ((t * 40) % 160)
        with g.at(bx, -120, 0.5):
            _smooth_path(c, [(-120, -40), (120, -40), (90, 30), (-100, 30)])
            _shade(c, RED, 5, 0.2)
            _rr(c, -40, -100, 80, 60, 6)
            _shade(c, WHITE, 4, 0.1)


def gunman(g, x, y, sc=1.0, k=1.0):
    """มือปืน — เงาดำ ไม่เห็นหน้า"""
    from people import person
    look = Look(hair="part", suit=INK, hat="bowler", w=56)
    with g.silhouette(INK, 0.9 * k):
        with g.at(x, y, 1, 0, sx=-1, sy=1):   # หันซ้ายเข้าหาโรสเวลต์ (แขนไม่ล้นขอบขวา)
            person(g, 0, 0, look, sc, pose="point", turn=0.6, shadow=False)


def flash(g, x, y, r, k):
    if 0 < k < 1:
        a = 1 - k
        g.star(x, y, r * (0.4 + 0.9 * k), (1, 0.85, 0.4, a), 0, pts=12, inner=0.45)


def glasses_case(g, x, y, sc=1.0, rot=0.0, hole=True):
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -150, -55, 300, 110, 50)
        _shade(c, hexc("#a8adb5"), 6, 0.35)
        _stroke(c, [(-150, -5), (150, -5)], 3, INK, 0.5, smooth=False)
        if hole:
            g.circle(30, 10, 16, INK, 0)


def speech(g, x, y, sc=1.0, rot=0.0, hole=True, n=50):
    """ปึกกระดาษสุนทรพจน์พับครึ่ง"""
    c = g.c
    with g.at(x, y, sc, rot):
        for i in range(5):
            _rr(c, -170 + i * 4, -120 - i * 6, 340, 240, 6)
            _shade(c, hexc("#f4eedf"), 4, 0.05)
        for i in range(6):
            _stroke(c, [(-130, -100 + i * 34), (130, -100 + i * 34)], 3, GREY, 0.5, smooth=False)
        if hole:
            g.circle(40, 0, 16, INK, 0)
        g.text(f"{n} แผ่น", 0, 150, 40, "kanit", GREY)


def lungs(g, x, y, sc=1.0, ok=True):
    with g.at(x, y, sc):
        for sx in (-1, 1):
            g.blob(sx * 70, 0, 60, 110, hexc("#f2b8c6"), 6, seed=5 + sx)
        g.line([(0, -140), (0, -40)], 10, hexc("#c8788a"), amp=0)
        if ok:
            g.line([(-40, 160), (0, 200), (70, 120)], 16, hexc("#3c8d4f"), amp=0)


def ambulance(g, x, y, sc=1.0, t=0.0):
    """รถพยาบาลยุค 1912 (รถม้า/รถยนต์โบราณ)"""
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -220, -260, 340, 200, 14)
        _shade(c, WHITE, 6, 0.2)
        _rr(c, 120, -190, 130, 130, 14)
        _shade(c, WHITE, 6, 0.2)
        _rr(c, -70, -200, 30, 90, 4)
        c.set_source_rgba(*RED)
        c.fill()
        _rr(c, -100, -170, 90, 30, 4)
        c.set_source_rgba(*RED)
        c.fill()
        for wx in (-130, 170):
            with g.at(wx, -50, 1, t * 200):
                g.circle(0, 0, 50, hexc("#3a3f48"), 6)
                g.line([(-40, 0), (40, 0)], 4, GREY, amp=0)


def podium(g, x, y, sc=1.0):
    c = g.c
    with g.at(x, y, sc):
        _smooth_path(c, [(-110, 0), (-90, -260), (90, -260), (110, 0)])
        _shade(c, hexc("#8a5a3a"), 6, 0.25)
        _rr(c, -130, -290, 260, 40, 8)
        _shade(c, hexc("#6e4528"), 5, 0.2)
        g.circle(0, -150, 40, GOLD, 4)


def moose(g, x, y, sc=1.0, t=0.0):
    """กวางมูส (ไอคอน Bull Moose)"""
    c = g.c
    with g.at(x, y, sc, 3 * math.sin(t * 2)):
        g.blob(0, 0, 150, 90, hexc("#7a4a2a"), 6, seed=3)
        for lx in (-90, -40, 60, 110):
            _rr(c, lx - 14, 60, 28, 140, 8)
            _shade(c, hexc("#5a3a22"), 4, 0.1)
        g.blob(170, -80, 70, 55, hexc("#7a4a2a"), 6, seed=4)
        g.blob(220, -60, 40, 30, hexc("#8a5a3a"), 5, seed=5)
        g.circle(170, -100, 7, INK, 0)
        for sx in (-1, 1):
            with g.at(150 + sx * 40, -140, 1, sx * 20):
                _smooth_path(c, [(0, 0), (sx * 40, -80), (sx * 90, -100), (sx * 70, -60), (sx * 110, -50), (sx * 60, -20)])
                _shade(c, hexc("#d9c48f"), 5, 0.1)


def dna(g, x, y, sc=1.0, t=0.0):
    with g.at(x, y, sc, 20):
        for i in range(12):
            yy = -260 + i * 46
            a = t * 2 + i * 0.6
            x1, x2 = 90 * math.sin(a), -90 * math.sin(a)
            g.line([(x1, yy), (x2, yy)], 5, GREY, amp=0)
            g.circle(x1, yy, 14, RED, 3)
            g.circle(x2, yy, 14, NAVY, 3)


def stain(g, x, y, r):
    """รอยเปื้อนเลือดเล็ก ๆ บนเสื้อ (ไม่รุนแรง)"""
    if r > 0:
        g.blob(x, y, r, r * 1.2, BLOOD, 0, seed=9)
