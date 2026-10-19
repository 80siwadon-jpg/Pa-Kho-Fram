"""ตัวละครและพร็อพ: วันเกิดไมเคิล ไครช์ตัน 23 ต.ค. 1942 (ไดโนเสาร์การ์ตูน ไม่มีภาพบาดเจ็บ)"""
import math

from gfx import GOLD, GOLD2, GREY, INK, NAVY, RED, WHITE, hexc
from people import Look, _rr, _shade, _smooth_path, _stroke

AMBER = hexc("#e8a33d")
DINO = hexc("#7aa05a")
DINO2 = hexc("#5f8a46")
GREEN = hexc("#3c8d4f")

# ไมเคิล ไครช์ตัน: สูงมาก (206 ซม.) ผมน้ำตาลเสยปรกหู แว่นกลมกรอบบาง สูทกรมท่า เชิ้ตขาว เนกไทแดง ยิ้มกว้าง
CRICHTON = Look(hair="part", hair_col=hexc("#5a3a26"), suit=hexc("#1f2a44"), tie=hexc("#b8323a"), glasses="roundthin",
                w=54, jaw=0.45, nose=1.15, brow=0.8, age=0.45, height=1.08, build=0.92)
STUDENT = Look(hair="full", hair_col=hexc("#5a3a26"), outfit="tee", suit=WHITE, pants=hexc("#3a3a40"),
               glasses="roundthin", w=54, jaw=0.4, nose=1.1, age=0.1, height=1.06, build=0.9)
SPIELBERG = Look(hair="short", hair_col=hexc("#5a4a3a"), outfit="flannel", suit=hexc("#6a7f9a"), pants=hexc("#3a4a6a"),
                 glasses="thin", facial="beard", w=56, age=0.4)
CROWD = [
    Look(hair="short", hair_col=hexc("#2b2622"), outfit="tee", suit=hexc("#e8892e"), pants=hexc("#3f5f8a"), w=56),
    Look(hair="long", hair_col=hexc("#5a3a22"), outfit="tee", suit=hexc("#3c8d9f"), pants=hexc("#2f3a4a"), w=54,
         height=0.92),
    Look(hair="afro", hair_col=hexc("#221e1c"), outfit="hoodie", suit=hexc("#c8553d"), pants=hexc("#3a3a40"), w=56,
         skin=hexc("#8a5a3c")),
]


def microscope(g, x, y, sc=1.0, t=0.0):
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -130, -30, 260, 30, 8)
        _shade(c, hexc("#3a3a40"), 5, 0.2)
        _smooth_path(c, [(60, -30), (90, -200), (60, -260), (20, -250), (40, -200), (20, -30)])
        _shade(c, hexc("#e8e6df"), 5, 0.25)
        _rr(c, -100, -110, 170, 20, 4)
        _shade(c, hexc("#bcd6e6"), 4, 0.1)   # แท่นวางสไลด์
        with g.at(0, -260, 1, -25):
            _rr(c, -26, -150, 52, 190, 10)
            _shade(c, hexc("#e8e6df"), 5, 0.25)
            _rr(c, -18, -190, 36, 46, 6)
            _shade(c, INK, 4, 0.1)
        g.circle(-30, -140, 10 + 2 * math.sin(t * 4), (0.6, 0.85, 0.6, 0.8), 0)


def mosquito(g, x, y, sc=1.0, t=0.0):
    c = g.c
    with g.at(x, y, sc):
        for sx in (-1, 1):
            _smooth_path(c, [(0, 0), (sx * 60, -30 - 10 * math.sin(t * 20)), (sx * 80, -10), (sx * 20, 10)])
            _shade(c, (0.85, 0.9, 0.95, 0.7), 3, 0.1)
        _rr(c, -10, -12, 70, 24, 12)
        _shade(c, hexc("#4a3a2a"), 3, 0.2)
        g.circle(-14, 0, 14, hexc("#4a3a2a"), 3)
        _stroke(c, [(-26, 4), (-70, 18)], 3, INK, smooth=False)
        for k in range(3):
            _stroke(c, [(10 + k * 16, 10), (k * 20 - 10, 50)], 3, INK)


def amber(g, x, y, sc=1.0, t=0.0, glow=0.5):
    """ก้อนอำพันมียุงข้างใน"""
    c = g.c
    with g.at(x, y, sc, 6 * math.sin(t)):
        if glow > 0:
            g.sunburst(0, 0, 150, 260, 14, t * 10, 8, (1, 0.8, 0.4, 0.5 * glow))
        _smooth_path(c, [(-110, -40), (-60, -120), (40, -130), (120, -60), (110, 50), (40, 120), (-60, 110), (-120, 40)])
        _shade(c, AMBER, 6, 0.3)
        mosquito(g, 0, 0, 0.9, 0.0)
        _smooth_path(c, [(-110, -40), (-60, -120), (40, -130), (120, -60), (110, 50), (40, 120), (-60, 110), (-120, 40)])
        c.set_source_rgba(0.95, 0.65, 0.2, 0.35)
        c.fill()
        _stroke(c, [(-70, -80), (-20, -100)], 10, WHITE, 0.6)


def dna(g, x, y, h=500, t=0.0, sc=1.0, col1=RED, col2=NAVY):
    """เกลียวดีเอ็นเอตั้ง"""
    with g.at(x, y, sc):
        n = 14
        for i in range(n):
            yy = -h / 2 + i * h / (n - 1)
            ph = t * 2 + i * 0.55
            x1, x2 = 60 * math.sin(ph), -60 * math.sin(ph)
            g.line([(x1, yy), (x2, yy)], 4, GREY, amp=0)
            g.circle(x1, yy, 13, col1, 3)
            g.circle(x2, yy, 13, col2, 3)


def trex(g, x, y, sc=1.0, t=0.0, roar=0.0, flip=False, walk=True):
    """ทีเร็กซ์การ์ตูน — x,y = พื้น หันขวา (flip = หันซ้าย)"""
    c = g.c
    st = math.sin(t * 6) if walk else 0
    with g.at(x, y - 6 * abs(st), sc, 0, sx=-sc if flip else sc, sy=sc):
        for k, ph in ((-1, 0), (1, math.pi)):   # ขา
            a = 18 * math.sin(t * 6 + ph) if walk else 0
            with g.at(-30 + k * 50, -230, 1, a):
                _smooth_path(c, [(-50, -40), (50, -40), (40, 120), (60, 200), (70, 230), (-10, 230), (0, 200), (-40, 110)])
                _shade(c, DINO2 if k < 0 else DINO, 6, 0.3)
        _smooth_path(c, [(-420, -330 + 20 * st), (-200, -360), (40, -420), (160, -470), (200, -380), (120, -260),
                         (-60, -200), (-240, -260)])
        _shade(c, DINO, 6, 0.3)   # ลำตัว + หาง
        for i in range(6):
            _smooth_path(c, [(-260 + i * 60, -360 - (i > 2) * 30), (-240 + i * 60, -400 - (i > 2) * 30),
                             (-220 + i * 60, -360 - (i > 2) * 30)])
            _shade(c, DINO2, 3, 0.2)
        _stroke(c, [(130, -330), (180, -300), (190, -270)], 14, INK)   # แขนสั้น
        _stroke(c, [(130, -330), (180, -300), (190, -270)], 8, DINO2)
        jaw = 26 * roar
        with g.at(170, -470, 1, -8):   # หัว
            _smooth_path(c, [(-40, -60), (120, -80), (200, -40), (210, 0), (60, 10), (-20, 30)])
            _shade(c, DINO, 6, 0.25)
            with g.at(0, 10, 1, jaw):
                _smooth_path(c, [(-10, 0), (190, 4), (170, 40), (20, 50)])
                _shade(c, DINO2, 5, 0.25)
                for k in range(5):
                    g.poly([(50 + k * 28, 4), (62 + k * 28, 4), (56 + k * 28, -10)], WHITE, 2, amp=0)
            for k in range(5):
                g.poly([(50 + k * 28, 4), (62 + k * 28, 4), (56 + k * 28, 18)], WHITE, 2, amp=0)
            g.circle(70, -36, 14, WHITE, 4)
            g.circle(74, -36, 7, INK, 0)
            _stroke(c, [(50, -56), (96, -50)], 6, INK, smooth=False)


def book(g, x, y, sc=1.0, rot=0.0, title="JURASSIC PARK", col=hexc("#2b2622")):
    """ปกหนังสือนิยาย (โครงกระดูกไดโนเสาร์บนปก)"""
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -150, -210, 300, 420, 10)
        _shade(c, col, 6, 0.3)
        _rr(c, -150, -210, 26, 420, 6)
        _shade(c, hexc("#1b1714"), 3, 0)
        g.circle(10, -40, 90, hexc("#c8323a"), 5)
        _stroke(c, [(-50, -10), (0, -60), (50, -70), (70, -40), (40, -20)], 10, INK)   # โครงกระดูกหัว
        for k in range(4):
            _stroke(c, [(-40 + k * 20, -10), (-30 + k * 20, 20)], 5, INK, smooth=False)
        g.text("MICHAEL CRICHTON", 10, -160, 22, "kanit", GOLD2, maxw=260)
        g.text(title, 10, 110, 36, "kanit", hexc("#f2c94c"), maxw=260)


def clapper(g, x, y, sc=1.0, k=0.0, t=0.0):
    """สเลตกองถ่าย (k = เปิดฝา)"""
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -150, -40, 300, 200, 8)
        _shade(c, hexc("#2b2622"), 6, 0.2)
        g.text("1993", 0, 60, 60, "kanit", WHITE)
        with g.at(-150, -40, 1, -25 * k):
            _rr(c, 0, -50, 300, 50, 6)
            _shade(c, WHITE, 5, 0.1)
            for i in range(5):
                g.poly([(10 + i * 60, -50), (40 + i * 60, -50), (20 + i * 60, 0), (-10 + i * 60, 0)], INK, 0, amp=0)


def cross_sign(g, x, y, sc=1.0, text="ER"):
    """ป้ายห้องฉุกเฉิน"""
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -170, -120, 340, 240, 20)
        _shade(c, WHITE, 6, 0.1)
        g.poly([(-30, -90), (30, -90), (30, -30), (90, -30), (90, 30), (30, 30), (30, 90), (-30, 90), (-30, 30),
                (-90, 30), (-90, -30), (-30, -30)], RED, 4, amp=0)
        g.text(text, 0, 150, 70, "kanit", RED)


def robot_cowboy(g, x, y, sc=1.0, t=0.0, reveal=0.0):
    """หุ่นยนต์คาวบอย (Westworld): หน้าเปิดเห็นวงจร"""
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -90, -360, 180, 280, 30)
        _shade(c, hexc("#2b2622"), 6, 0.2)   # เสื้อดำ
        _rr(c, -60, -80, 50, 80, 8)
        _shade(c, hexc("#4a3a2a"), 4, 0.2)
        _rr(c, 10, -80, 50, 80, 8)
        _shade(c, hexc("#4a3a2a"), 4, 0.2)
        c.new_path()
        c.arc(0, -440, 80, 0, 2 * math.pi)
        _shade(c, hexc("#efc4a1"), 6, 0.2)
        if reveal > 0:
            with g.alpha(reveal):
                _rr(c, -60, -490, 120, 100, 10)
                _shade(c, hexc("#3a4a5a"), 4, 0.1)
                for k in range(4):
                    _stroke(c, [(-50, -470 + k * 22), (50, -470 + k * 22)], 3, hexc("#5ad0f0"), smooth=False)
                g.circle(-24, -450, 10, RED, 2)
                g.circle(24, -450, 10, RED, 2)
        else:
            g.circle(-26, -450, 8, INK, 0)
            g.circle(26, -450, 8, INK, 0)
        _smooth_path(c, [(-160, -500), (-60, -520), (-50, -600), (50, -600), (60, -520), (160, -500), (60, -490),
                         (-60, -490)])
        _shade(c, hexc("#2b2622"), 6, 0.1)   # หมวกคาวบอย


def chip(g, x, y, sc=1.0, t=0.0, label="AI"):
    c = g.c
    with g.at(x, y, sc):
        for i in range(5):
            for s in (-1, 1):
                _stroke(c, [(-80 + i * 40, s * 100), (-80 + i * 40, s * 140)], 8, GREY, smooth=False)
                _stroke(c, [(s * 100, -80 + i * 40), (s * 140, -80 + i * 40)], 8, GREY, smooth=False)
        _rr(c, -100, -100, 200, 200, 20)
        _shade(c, hexc("#2b3440"), 6, 0.2)
        g.text(label, 0, 0, 80, "kanit", hexc("#5ad0f0"))


def money_rain(g, t, n=8, x0=100, x1=1000, y0=300, y1=1200):
    for i in range(n):
        u = (t * 0.35 + i / n) % 1
        x = x0 + (x1 - x0) * ((i * 0.37) % 1) + 30 * math.sin(t * 2 + i)
        with g.at(x, y0 + (y1 - y0) * u, 1, 30 * math.sin(t * 3 + i)):
            g.rrect(-50, -26, 100, 52, 6, hexc("#9fd08a"), 4)
            g.text("$", 0, 0, 34, "kanit", hexc("#2f7a3f"))
