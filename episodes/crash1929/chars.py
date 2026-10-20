"""ตัวละครและพร็อพ: วันพฤหัสทมิฬ 24 ต.ค. 1929 (ไม่แสดงการทำร้ายตัวเอง/ความรุนแรง)"""
import math

from gfx import GOLD, GOLD2, GREY, INK, NAVY, RED, WHITE, hexc
from people import Look, _rr, _shade, _smooth_path, _stroke

GREEN = hexc("#3c8d4f")
STONE = hexc("#e9e4d6")
TAPE = hexc("#f4efe2")

BROKERS = [   # นายหน้าค้าหุ้นยุค 1920s
    Look(hair="slick", hair_col=hexc("#2b2622"), outfit="vest", suit=hexc("#3b3a3e"), shirt=WHITE, tie=hexc("#7a2e2e"),
         w=56, age=0.4, facial="mustache"),
    Look(hair="part", hair_col=hexc("#6b4a33"), outfit="vest", suit=hexc("#4a4038"), shirt=WHITE, tie=hexc("#2b3f63"),
         bowtie=True, w=56, age=0.3, glasses="round"),
    Look(hair="slick", hair_col=hexc("#9a948a"), suit=hexc("#2f3036"), tie=hexc("#2b2622"), w=58, age=0.6,
         hat="bowler", jowls=0.3),
]
COMMON = [   # คนธรรมดา: คนกวาดถนน คนขับแท็กซี่ แม่บ้าน
    Look(hair="short", hair_col=hexc("#5a4a3a"), outfit="tee", suit=hexc("#6a7f9a"), pants=hexc("#3a3a40"), w=56,
         hat="porkpie", hat_trim=hexc("#5a5a5a"), age=0.4, stubble=0.5),
    Look(hair="short", hair_col=hexc("#2b2622"), outfit="vest", suit=hexc("#d9a441"), shirt=WHITE, tie=INK, w=56,
         hat="porkpie", hat_trim=hexc("#2b2622"), age=0.3),
    Look(hair="bun", hair_col=hexc("#6b4a33"), outfit="dress", suit=hexc("#8a5a7a"), w=54, height=0.93, age=0.3),
]
BANKER = Look(hair="bald", hair_col=hexc("#9a948a"), suit=hexc("#1f1f24"), tie=hexc("#1f1f24"), bowtie=True, w=62,
              jaw=0.7, jowls=0.6, age=0.7, build=1.25, hat="tophat")


def exchange(g, x, y, sc=1.0, t=0.0, a=1.0):
    """อาคารตลาดหลักทรัพย์นิวยอร์ก: เสาโรมัน 6 ต้น หน้าจั่ว ธงชาติ"""
    c = g.c
    with g.at(x, y, sc), g.alpha(a):
        _rr(c, -380, -80, 760, 80, 4)
        _shade(c, STONE, 5, 0.2)
        for i in range(6):
            _rr(c, -320 + i * 128, -520, 60, 440, 6)
            _shade(c, WHITE, 4, 0.2)
        _rr(c, -380, -600, 760, 80, 4)
        _shade(c, STONE, 5, 0.2)
        c.new_path()
        for p in [(-400, -600), (0, -760), (400, -600)]:
            c.line_to(*p)
        c.close_path()
        _shade(c, STONE, 5, 0.25)
        g.text("NEW YORK STOCK EXCHANGE", 0, -560, 34, "kanit", INK, maxw=700)
        g.line([(0, -760), (0, -880)], 6, INK, amp=0)
        g.flag(0, -880, 110, 66, "us", t)


def bell(g, x, y, sc=1.0, t=0.0, ring=0.0):
    c = g.c
    with g.at(x, y, sc, 20 * math.sin(t * 10) * ring):
        _smooth_path(c, [(-90, 80), (-70, -40), (-30, -90), (30, -90), (70, -40), (90, 80)])
        _shade(c, GOLD, 6, 0.3)
        _rr(c, -100, 70, 200, 26, 10)
        _shade(c, GOLD2, 5, 0.2)
        g.circle(0, 110, 20, hexc("#8a6a3a"), 4)
    if ring > 0:
        for i in range(3):
            u = (t * 0.9 + i / 3) % 1
            g.arc(x, y, 150 + 200 * u, -50, 50, 7, (0.7, 0.55, 0.2, ring * (1 - u)))
            g.arc(x, y, 150 + 200 * u, 130, 230, 7, (0.7, 0.55, 0.2, ring * (1 - u)))


def clock(g, x, y, r, hh=10, mm=0, k=1.0):
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


def chart(g, x, y, w, h, pts, k=1.0, col=GREEN, lw=12):
    c = g.c
    g.line([(x, y), (x + w, y)], 6, INK, amp=0)
    g.line([(x, y), (x, y - h)], 6, INK, amp=0)
    n = max(2, int(len(pts) * k + 0.99))
    path = [(x + u * w, y - v * h) for u, v in pts[:n]]
    _stroke(c, path, lw + 6, INK, smooth=False)
    _stroke(c, path, lw, col, smooth=False)
    ex, ey = path[-1]
    g.circle(ex, ey, 14, col, 4)


def ticker(g, x, y, sc=1.0, t=0.0, fast=1.0, tape_len=600):
    """เครื่องพิมพ์ราคาหุ้น (ticker) ใต้โดมแก้ว + เทปกระดาษไหลออก"""
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -110, -40, 220, 40, 6)
        _shade(c, hexc("#6e4528"), 5, 0.2)
        _smooth_path(c, [(-90, -40), (-90, -200), (0, -260), (90, -200), (90, -40)])
        c.set_source_rgba(0.85, 0.92, 0.97, 0.35)
        c.fill_preserve()
        c.set_source_rgba(*INK[:3], 1)
        c.set_line_width(5)
        c.stroke()
        _rr(c, -50, -150, 100, 100, 10)
        _shade(c, hexc("#c9a24a"), 4, 0.25)
        with g.at(0, -100, 1, t * 300 * fast):
            c.new_path()
            c.arc(0, 0, 26, 0, 2 * math.pi)
            _shade(c, hexc("#8a8a8a"), 3, 0.1)
            _stroke(c, [(-26, 0), (26, 0)], 3, INK, smooth=False)
        pts = []
        for i in range(16):
            u = i / 15
            pts.append((60 + u * tape_len, -60 + 40 * math.sin(u * 6 + t * 3 * fast) + 140 * u * u))
        _stroke(c, pts, 34, INK)
        _stroke(c, pts, 28, TAPE)
        for i in range(5):
            u = ((t * 0.3 * fast + i / 5) % 1)
            px, py = pts[int(u * 14)]
            g.text("-", px, py, 22, "kanit", RED)


def money_stack(g, x, y, n=5, sc=1.0, melt=0.0):
    """กองธนบัตร (melt = ละลายหายเป็นไอ)"""
    c = g.c
    with g.at(x, y, sc):
        for i in range(n):
            a = max(0.0, 1 - melt * 1.5 + i * 0.1)
            if a <= 0.02:
                continue
            with g.alpha(min(1.0, a)):
                _rr(c, -110, -30 - i * 34, 220, 34, 6)
                _shade(c, hexc("#9fd08a"), 4, 0.2)
                g.circle(0, -13 - i * 34, 12, hexc("#2f7a3f"), 2)
        if melt > 0:
            for i in range(5):
                u = (melt * 2 + i / 5) % 1
                g.circle(-80 + i * 40, -n * 34 - 60 * u * 3, 10 + 20 * u, (0.8, 0.9, 0.8, 0.6 * (1 - u)), 0)


def bubble_burst(g, x, y, r, k=0.0, t=0.0):
    """ฟองสบู่ลูกยักษ์ k: 0 = ฟองเต็ม, >0 แตกกระจาย"""
    c = g.c
    if k <= 0:
        g.circle(x, y, r * (1 + 0.03 * math.sin(t * 3)), (0.75, 0.88, 0.98, 0.45), 6)
        _stroke(c, [(x - r * 0.5, y - r * 0.4), (x - r * 0.2, y - r * 0.6)], 14, WHITE, 0.8)
        g.label("$", x, y, int(r * 0.9), color=GREEN)
        return
    for i in range(14):
        a = i * 2 * math.pi / 14
        d = r * (0.6 + 1.2 * k)
        with g.alpha(max(0.0, 1 - k)):
            g.circle(x + d * math.cos(a), y + d * math.sin(a), 12 + 10 * (i % 3), (0.75, 0.88, 0.98, 0.9), 4)
    if k < 0.6:
        g.star(x, y, r * (0.6 + k), (1, 1, 1, 0.9 - k), 6, pts=12, inner=0.4)


def headline(g, x, y, sc=1.0, rot=0.0, h1="STOCKS CRASH!", h2="WALL ST. PANIC"):
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -300, -380, 600, 760, 6)
        _shade(c, hexc("#f4efe2"), 6, 0.2)
        g.text("THE DAILY NEWS", 0, -320, 36, "kanit", INK)
        g.line([(-260, -290), (260, -290)], 4, INK, amp=0)
        g.text(h1, 0, -210, 64, "kanit", RED, maxw=540)
        g.text(h2, 0, -130, 40, "kanit", INK, maxw=540)
        for i in range(8):
            g.line([(-260, -60 + i * 40), (260 - 80 * (i % 3), -60 + i * 40)], 5, GREY, amp=0)
        g.text("OCT. 24, 1929", 0, 320, 30, "kanit", GREY)


def bank(g, x, y, sc=1.0, closed=0.0):
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -200, -320, 400, 320, 4)
        _shade(c, STONE, 5, 0.2)
        c.new_path()
        for p in [(-220, -320), (0, -420), (220, -320)]:
            c.line_to(*p)
        c.close_path()
        _shade(c, STONE, 5, 0.25)
        g.text("BANK", 0, -350, 40, "kanit", INK)
        for i in range(4):
            _rr(c, -160 + i * 95, -290, 30, 240, 4)
            _shade(c, WHITE, 3, 0.15)
        if closed > 0:
            with g.at(0, -170, closed, -10):
                g.rrect(-170, -50, 340, 100, 10, (1, 1, 1, 0.95), 7, stroke=RED)
                g.text("CLOSED", 0, 0, 56, "kanit", RED)


def factory(g, x, y, sc=1.0, t=0.0, off=0.0):
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -220, -220, 440, 220, 4)
        _shade(c, hexc("#c45a3c"), 5, 0.25)
        for i in range(3):
            c.new_path()
            for p in [(-220 + i * 147, -220), (-220 + i * 147, -300), (-73 + i * 147, -220)]:
                c.line_to(*p)
            c.close_path()
            _shade(c, hexc("#a8473a"), 4, 0.2)
        _rr(c, 140, -420, 50, 200, 4)
        _shade(c, hexc("#5a4a42"), 4, 0.2)
        if off < 0.5:
            for i in range(3):
                u = (t * 0.4 + i / 3) % 1
                g.circle(165 + 20 * math.sin(t + i), -440 - 160 * u, 20 + 30 * u, (0.6, 0.6, 0.6, 0.6 * (1 - u)), 0)
        else:
            g.line([(-200, -120), (200, -60)], 12, hexc("#8a6a42"), amp=0)
            g.line([(-200, -60), (200, -120)], 12, hexc("#8a6a42"), amp=0)


def soup_line(g, x0, y, n=6, sc=0.5, t=0.0):
    """แถวรอรับอาหาร (ภาพสัญลักษณ์ยุคเศรษฐกิจตกต่ำ)"""
    from people import person
    looks = COMMON + BROKERS
    for i in range(n):
        person(g, x0 + i * 120, y, looks[i % len(looks)], sc, mood="sad", pose="down", turn=0.6, seed=70 + i,
               shadow=False)
