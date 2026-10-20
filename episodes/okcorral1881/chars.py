"""ตัวละครและพร็อพ: ดวลปืนที่โอเค คอร์รัล ทูมสโตน 26 ต.ค. 1881
ไม่แสดงความรุนแรงตรง ๆ: ใช้ควันดินปืน แสงวาบ หมวกตกพื้น เงาคน แทนการยิง/การบาดเจ็บ"""
import math

from gfx import GOLD, GOLD2, GREY, INK, NAVY, RED, WHITE, hexc
from people import Look, _rr, _shade, _smooth_path, _stroke

SAND = hexc("#e8d6aa")
WOOD = hexc("#a8784a")
WOOD2 = hexc("#8a5a36")
COAT = hexc("#1f1d22")
SMOKE = (0.68, 0.66, 0.63)

# ไวแอตต์ เอิร์ป: ผมน้ำตาลอ่อน หนวดใหญ่ห้อยปลาย โค้ตยาวดำ หมวกปีกกว้างดำ
WYATT = Look(hair="part", hair_col=hexc("#8a6a42"), suit=COAT, shirt=WHITE, tie=COAT, bowtie=True,
             facial="mustache", w=56, jaw=0.55, nose=1.1, brow=1.0, age=0.4, cape=COAT, hat="cowboy",
             hat_trim=hexc("#1b1916"))
VIRGIL = Look(hair="part", hair_col=hexc("#6b4a33"), suit=COAT, shirt=WHITE, tie=COAT, facial="mustache", w=57,
              jaw=0.6, age=0.55, cape=COAT, hat="cowboy", hat_trim=hexc("#2b2622"))
MORGAN = Look(hair="part", hair_col=hexc("#a8844f"), suit=COAT, shirt=WHITE, tie=COAT, facial="mustache", w=55,
              jaw=0.45, age=0.2, cape=COAT, hat="cowboy", hat_trim=hexc("#2b2622"))
# ด็อก ฮอลลิเดย์: ผอม ซีด ผมบลอนด์อ่อน หนวด โค้ตเทา หูกระต่าย
DOC = Look(hair="slick", hair_col=hexc("#d2b07a"), suit=hexc("#7a7a80"), shirt=WHITE, tie=hexc("#2b2622"),
           bowtie=True, facial="mustache", skin=hexc("#f2d8c2"), w=52, jaw=0.25, nose=1.1, age=0.35, build=0.85,
           cape=hexc("#6a6a70"), hat="bowler")
# เดอะ คาวบอยส์
COWBOYS = [
    Look(hair="full", hair_col=hexc("#5a3a22"), outfit="vest", suit=hexc("#6b4a33"), shirt=hexc("#d9c49a"),
         tie=hexc("#8a2e2e"), facial="beard", w=57, age=0.45, hat="cowboy", hat_trim=hexc("#8a6a42")),   # ไอก์ แคลนตัน
    Look(hair="short", hair_col=hexc("#3a2a1e"), outfit="vest", suit=hexc("#4a5a6a"), shirt=hexc("#c9b38a"),
         tie=hexc("#2b2622"), w=54, age=0.0, hat="cowboy", hat_trim=hexc("#a8844f")),                    # บิลลี แคลนตัน
    Look(hair="short", hair_col=hexc("#2b2622"), outfit="vest", suit=hexc("#5a3a2a"), shirt=hexc("#e8dcc0"),
         tie=hexc("#2b2622"), facial="mustache", w=56, age=0.35, hat="cowboy", hat_trim=hexc("#6b5a3a")),  # แมคลอรี
    Look(hair="short", hair_col=hexc("#4a3424"), outfit="vest", suit=hexc("#3a4a3a"), shirt=hexc("#e8dcc0"),
         tie=hexc("#8a2e2e"), facial="mustache", w=56, age=0.3, hat="cowboy", hat_trim=hexc("#5a4632")),
]
TOWNS = [
    Look(hair="bun", hair_col=hexc("#5a3a22"), outfit="dress", suit=hexc("#8a5a6a"), w=54, height=0.93),
    Look(hair="short", hair_col=hexc("#6b4a33"), outfit="vest", suit=hexc("#5a4a3a"), shirt=WHITE, tie=hexc("#2b2622"),
         w=56, hat="bowler"),
]


def storefront(g, x, y, w, h, col, sign="", sc=1.0):
    """อาคารหน้าจั่วปลอมแบบเมืองตะวันตก + ระเบียงไม้"""
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -w / 2, -h, w, h, 4)
        _shade(c, col, 6, 0.2)
        _rr(c, -w / 2 - 10, -h - 40, w + 20, 50, 4)
        _shade(c, col, 6, 0.1)
        if sign:
            _rr(c, -w * 0.38, -h + 30, w * 0.76, 70, 6)
            _shade(c, hexc("#f4eedf"), 4, 0)
            g.text(sign, 0, -h + 65, 40, "kanit", INK)
        for k in (-1, 1):
            _rr(c, k * w * 0.26 - 40, -h + 130, 80, 110, 6)
            _shade(c, hexc("#9ab8d0"), 4, 0.1)
        _rr(c, -45, -170, 90, 170, 6)
        _shade(c, WOOD2, 4, 0.1)
        _rr(c, -w / 2 - 20, -200, w + 40, 20, 4)
        _shade(c, WOOD, 4, 0.1)
        for k in (-1, 1):
            g.line([(k * (w / 2 + 10), -190), (k * (w / 2 + 10), 0)], 10, INK, amp=0)


def town(g, y, x0=230):
    """ถนนเมืองตะวันตก 3 อาคาร (อยู่ในจอทั้งหมด)"""
    for i, (w, h, col, s) in enumerate(((260, 400, hexc("#c9915a"), "SALOON"), (240, 340, hexc("#b8644a"), "BANK"),
                                        (260, 440, hexc("#9a7a52"), "HOTEL"))):
        storefront(g, x0 + i * 310, y, w, h, col, s)


def corral(g, x, y, w=600, sc=1.0, sign=True):
    """รั้วคอกม้าไม้ + ป้าย O.K. CORRAL"""
    c = g.c
    with g.at(x, y, sc):
        for i in range(int(w / 120) + 1):
            _rr(c, -w / 2 + i * 120 - 10, -200, 20, 200, 4)
            _shade(c, WOOD2, 4, 0.1)
        for yy in (-170, -100):
            _rr(c, -w / 2, yy, w, 22, 4)
            _shade(c, WOOD, 4, 0.1)
        if sign:
            _rr(c, -180, -330, 360, 90, 8)
            _shade(c, hexc("#f4eedf"), 6, 0.1)
            g.text("O.K. CORRAL", 0, -285, 50, "kanit", INK)
            for k in (-1, 1):
                g.line([(k * 150, -240), (k * 150, -200)], 8, INK, amp=0)


def revolver(g, x, y, sc=1.0, rot=0.0, flash=0.0):
    """ปืนลูกโม่ (วาดแบบไอคอน)"""
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -20, -24, 220, 26, 6)
        _shade(c, hexc("#8a8f98"), 5, 0.3)
        c.new_path()
        c.arc(0, -10, 38, 0, 2 * math.pi)
        _shade(c, hexc("#6a6f78"), 5, 0.2)
        for k in range(6):
            a = k * math.pi / 3
            g.circle(20 * math.cos(a), -10 + 20 * math.sin(a), 6, INK, 0)
        _smooth_path(c, [(-30, 10), (10, 10), (-10, 120), (-60, 130), (-70, 100)])
        _shade(c, WOOD2, 5, 0.2)
        if flash > 0:
            g.star(240, -12, 70 * flash, hexc("#f2a93b"), 4, pts=9, inner=0.4)
            g.star(240, -12, 34 * flash, hexc("#fff1c4"), 0, pts=9, inner=0.5)


def badge(g, x, y, sc=1.0, rot=0.0, t=0.0, txt="MARSHAL"):
    with g.at(x, y, sc, rot):
        g.star(0, 0, 110, GOLD, 7, pts=6, inner=0.6)
        g.circle(0, 0, 54, GOLD2, 5)
        g.text(txt, 0, 0, 22, "kanit", INK)
        g.sparkle(70, -70, 20 * (0.7 + 0.3 * math.sin(t * 4)))


def smoke(g, x, y, r, t, n=6, a=0.75, seed=0):
    for i in range(n):
        u = (t * 0.35 + i / n + seed) % 1
        g.circle(x + r * math.sin(i * 2.3 + seed) + 40 * math.sin(t + i), y - r * 1.2 * u, r * (0.5 + 0.8 * u),
                 SMOKE + (a * (1 - u),), 0)


def snow(g, t, n=40, seed=3):
    for i in range(n):
        x = (i * 137 + seed * 41) % 1300 - 100 + 30 * math.sin(t * 0.7 + i)
        y = 160 + ((i * 89 + t * 70 * (0.6 + 0.4 * (i % 3) / 2)) % 1100)
        g.circle(x, y, 5 + (i % 3) * 2, (1, 1, 1, 0.95), 1.5, stroke=(0.6, 0.65, 0.75, 0.8))


def hat_on_ground(g, x, y, sc=1.0, rot=0.0, col=hexc("#8a6a42")):
    c = g.c
    with g.at(x, y, sc, rot):
        _smooth_path(c, [(-50, -10), (-55, -80), (-25, -95), (0, -82), (25, -95), (55, -80), (50, -10)])
        _shade(c, col, 5, 0.25)
        _smooth_path(c, [(-110, -16), (-80, 4), (80, 4), (110, -16), (80, 10), (-80, 10)])
        _shade(c, col, 5, 0.1)


def gold_pile(g, x, y, sc=1.0, t=0.0):
    with g.at(x, y, sc):
        for i, (px, py, r) in enumerate(((-60, 0, 40), (10, -10, 46), (70, 4, 36), (-20, -50, 34), (40, -60, 30))):
            g.blob(px, py, r, r * 0.8, GOLD, 5, seed=i)
        g.sparkle(50, -90, 22 * (0.7 + 0.3 * math.sin(t * 5)))


def wanted(g, x, y, sc=1.0, rot=0.0, title="WANTED"):
    with g.at(x, y, sc, rot):
        g.rrect(-150, -200, 300, 400, 8, hexc("#f1e3c0"), 6)
        g.text(title, 0, -150, 52, "kanit", INK)
        g.rrect(-90, -100, 180, 170, 6, hexc("#e0cfa4"), 4)
        g.circle(0, -40, 40, hexc("#c9a46a"), 4)
        g.text("$500", 0, 130, 56, "kanit", RED)


def clock(g, x, y, r, t, k=1.0):
    if k < 0.02:
        return
    with g.at(x, y, k):
        g.circle(0, 0, r, WHITE, 8)
        for i in range(12):
            a = i * math.pi / 6
            g.line([(r * 0.8 * math.cos(a), r * 0.8 * math.sin(a)), (r * 0.92 * math.cos(a), r * 0.92 * math.sin(a))],
                   5, INK, amp=0)
        a = t * 2 * math.pi / 30 * 6
        g.line([(0, 0), (r * 0.75 * math.sin(a), -r * 0.75 * math.cos(a))], 8, RED, amp=0)
        g.circle(0, 0, 10, INK, 0)


def film(g, x, y, sc=1.0, t=0.0):
    """ม้วนฟิล์มภาพยนตร์"""
    c = g.c
    with g.at(x, y, sc, t * 40):
        c.new_path()
        c.arc(0, 0, 130, 0, 2 * math.pi)
        _shade(c, hexc("#3a3a40"), 6, 0.2)
        for k in range(6):
            a = k * math.pi / 3
            g.circle(70 * math.cos(a), 70 * math.sin(a), 26, WHITE, 4)
        g.circle(0, 0, 20, hexc("#8a8f98"), 4)


def tumbleweed(g, x, y, r, t):
    with g.at(x, y, 1, t * 200):
        for k in range(6):
            g.arc(0, 0, r * (0.4 + 0.1 * k), k * 50, k * 50 + 260, 4, hexc("#a8844f"))
