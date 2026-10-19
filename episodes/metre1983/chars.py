"""ตัวละครและพร็อพ: นิยาม 1 เมตรด้วยความเร็วแสง 21 ต.ค. 1983 — คนแบบกึ่งเสมือนจริงจาก src/people.py"""
import math

from gfx import GOLD, GOLD2, GREY, INK, LGREY, NAVY, RED, WHITE, hexc, hn as _hn, lerp


def hn(*a):   # 0..1
    return (_hn(*a) + 1) / 2
from people import Look, _rr, _shade, _smooth_path, _stroke

PT = hexc("#c9ced6")       # แพลทินัม-อิริเดียม
PT2 = hexc("#9aa1ab")
BEAM = (1.0, 0.86, 0.3)
SPACE = hexc("#232a45")
YELLOW = hexc("#f2c230")

# นักวิทยาศาสตร์ในที่ประชุม CGPM ปี 1983 (สูทยุค 80s แว่นกรอบใหญ่)
SCIENTISTS = [
    Look(hair="part", hair_col=hexc("#9a948a"), suit=hexc("#3b4250"), tie=hexc("#7a2e2e"), glasses="thick", w=58,
         jaw=0.5, nose=1.2, age=0.7),
    Look(hair="bun", hair_col=hexc("#6b4a33"), suit=hexc("#8a4a5a"), outfit="dress", glasses="thin", w=54, age=0.5,
         height=0.94),
    Look(hair="slick", hair_col=hexc("#2b2622"), suit=hexc("#5a4a3a"), tie=hexc("#2b3f63"), facial="mustache",
         w=58, age=0.55, skin=hexc("#d9a37e")),
    Look(hair="crew", hair_col=hexc("#d9d5cc"), suit=hexc("#2f3a4a"), tie=hexc("#8a6a2a"), bowtie=True,
         glasses="thin", w=58, age=0.85, jowls=0.4),
]
KID = Look(hair="buzz", hair_col=hexc("#2b2622"), suit=hexc("#e3a92b"), outfit="tee", pants=hexc("#3f6496"),
           w=56, age=0.0, height=0.62, headsc=1.4, skin=hexc("#e8b48f"))


# ---------------------------------------------------------------- พร็อพ
def metre_bar(g, x, y, length=820, sc=1.0, rot=0.0, scratch=0.0, glow=0.0, t=0.0, shrink=0.0):
    """แท่งเมตรต้นแบบ (แพลทินัม-อิริเดียม หน้าตัดรูปตัว X) — x,y = กึ่งกลาง
    scratch 0..1 รอยขีดข่วน, shrink หดสั้นลง (เกินจริงเพื่อสื่อ)"""
    c = g.c
    L = length * (1 - 0.08 * shrink)
    with g.at(x, y, sc, rot):
        if glow > 0:
            g.sunburst(0, 0, L * 0.3, L * 0.62, 18, t * 8, 10, (0.95, 0.88, 0.6, 0.6 * glow))
        _rr(c, -L / 2, -26, L, 52, 8)
        _shade(c, PT, 6, 0.3, horiz=False)
        _rr(c, -L / 2 + 10, -8, L - 20, 16, 4)   # ร่องกลาง (หน้าตัด X)
        _shade(c, PT2, 3, 0.2)
        for sx in (-1, 1):   # ขีดบอกระยะ 1 เมตรใกล้ปลายทั้งสอง
            for k in range(3):
                _stroke(c, [(sx * (L / 2 - 30) - k * 6 * sx, -6), (sx * (L / 2 - 30) - k * 6 * sx, 6)], 2, INK, smooth=False)
        g.text("1 m", 0, -52, 30, "kanit", INK)
        for i in range(int(scratch * 8)):
            px = -L / 2 + 60 + hn(i, 3) * (L - 120)
            _stroke(c, [(px, -20 + hn(i, 4) * 10), (px + 30 + 20 * hn(i, 5), 4 + hn(i, 6) * 14)], 2.5, INK, 0.6, smooth=False)
        # หน้าตัด X ที่ปลายขวา
        with g.at(L / 2 + 50, 0, 0.55):
            c.new_path()
            for px, py in [(-40, -50), (-14, -50), (0, -14), (14, -50), (40, -50), (16, 0), (40, 50), (14, 50), (0, 14),
                           (-14, 50), (-40, 50), (-16, 0)]:
                c.line_to(px, py)
            c.close_path()
            _shade(c, PT, 5, 0.25)


def vault(g, x, y, r, k=0.0, t=0.0):
    """ประตูห้องนิรภัยกลม — k 0 = ปิด, 1 = เปิด (หมุนล้อ)"""
    c = g.c
    with g.at(x, y):
        c.new_path()
        c.arc(0, 0, r + 30, 0, 2 * math.pi)
        _shade(c, hexc("#6e747d"), 7, 0.3)
        c.new_path()
        c.arc(0, 0, r, 0, 2 * math.pi)
        _shade(c, hexc("#a4abb5"), 6, 0.25)
        for i in range(12):
            a = i * math.pi / 6
            g.circle(math.cos(a) * (r - 24), math.sin(a) * (r - 24), 10, hexc("#6e747d"), 3)
        with g.at(0, 0, 1, k * 200 + t * 2):
            for i in range(3):
                a = i * math.pi / 3
                g.line([(-math.cos(a) * r * 0.55, -math.sin(a) * r * 0.55), (math.cos(a) * r * 0.55, math.sin(a) * r * 0.55)],
                       16, hexc("#3a3a40"), amp=0)
            g.circle(0, 0, 34, hexc("#3a3a40"), 5)


def ruler(g, x, y, length=600, sc=1.0, rot=0.0, col=YELLOW, label=None):
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -length / 2, -40, length, 80, 6)
        _shade(c, col, 6, 0.2, horiz=False)
        n = int(length / 20)
        for i in range(n + 1):
            xx = -length / 2 + i * length / n
            hh = 30 if i % 10 == 0 else 18 if i % 5 == 0 else 10
            _stroke(c, [(xx, -40), (xx, -40 + hh)], 2.5 if hh > 20 else 1.8, INK, smooth=False)
        if label:
            g.text(label, 0, 14, 30, "kanit", INK)


def tape_measure(g, x, y, sc=1.0, ext=0.6, t=0.0):
    """ตลับเมตร — ext สายวัดยืดออก (0..1)"""
    c = g.c
    with g.at(x, y, sc):
        if ext > 0:
            L = 520 * ext
            _rr(c, 60, 30, L, 46, 3)
            _shade(c, YELLOW, 4, 0.15, horiz=False)
            for i in range(int(L / 26)):
                _stroke(c, [(70 + i * 26, 30), (70 + i * 26, 30 + (22 if i % 5 == 0 else 12))], 2, INK, smooth=False)
            _rr(c, 60 + L - 6, 22, 14, 62, 3)
            _shade(c, hexc("#c9cdd3"), 3, 0)
        _rr(c, -110, -110, 220, 220, 50)
        _shade(c, RED, 7, 0.25)
        c.new_path()
        c.arc(0, 0, 50, 0, 2 * math.pi)
        _shade(c, hexc("#c9cdd3"), 5, 0.1)


def eiffel(g, x, y, sc=1.0):
    c = g.c
    with g.at(x, y, sc):
        col = hexc("#7a5a3a")
        for sx in (-1, 1):
            _stroke(c, [(sx * 170, 0), (sx * 110, -200), (sx * 60, -420), (sx * 22, -640), (sx * 6, -820)], 14, col)
        for yy, w in ((-200, 110), (-420, 60), (-640, 22)):
            _rr(c, -w - 20, yy - 14, 2 * w + 40, 24, 4)
            _shade(c, col, 4, 0.1)
        g.arc(0, 0, 90, math.pi, 2 * math.pi, 12, col)
        g.line([(0, -820), (0, -900)], 8, col, amp=0)


def light_beam(g, x0, y, x1, k=1.0, t=0.0, lw=26):
    """ลำแสงวิ่งจาก x0 ไป x1 (k 0..1) + ประกายที่หัว"""
    if k <= 0:
        return
    xe = lerp(x0, x1, k)
    g.line([(x0, y), (xe, y)], lw + 24, (*BEAM, 0.25), amp=0)
    g.line([(x0, y), (xe, y)], lw, (*BEAM, 1), amp=0)
    g.line([(x0, y), (xe, y)], lw * 0.35, (1, 1, 1, 1), amp=0)
    g.sparkle(xe, y, 34 + 6 * math.sin(t * 20), (1, 0.95, 0.6, 1), 0)


def stopwatch(g, x, y, r, frac, sc=1.0):
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -22, -r - 44, 44, 30, 6)
        _shade(c, hexc("#c9cdd3"), 4, 0.1)
        c.new_path()
        c.arc(0, 0, r + 16, 0, 2 * math.pi)
        _shade(c, hexc("#c9cdd3"), 6, 0.2)
        c.new_path()
        c.arc(0, 0, r, 0, 2 * math.pi)
        _shade(c, WHITE, 5, 0.05)
        for i in range(12):
            a = i * math.pi / 6
            _stroke(c, [(math.sin(a) * r * 0.82, -math.cos(a) * r * 0.82), (math.sin(a) * r * 0.94, -math.cos(a) * r * 0.94)],
                    4, INK, smooth=False)
        a = frac * 2 * math.pi
        _stroke(c, [(0, 0), (math.sin(a) * r * 0.8, -math.cos(a) * r * 0.8)], 7, RED, smooth=False)
        g.circle(0, 0, 9, INK, 0)


def satellite(g, x, y, sc=1.0, rot=0.0, t=0.0):
    c = g.c
    with g.at(x, y, sc, rot):
        for sx in (-1, 1):
            _rr(c, sx * 70 + (0 if sx > 0 else -180), -40, 180, 80, 4)
            _shade(c, hexc("#3f6496"), 5, 0.2)
            for k in range(1, 4):
                _stroke(c, [(sx * 70 + (0 if sx > 0 else -180) + k * 45, -40), (sx * 70 + (0 if sx > 0 else -180) + k * 45, 40)],
                        2, WHITE, 0.5, smooth=False)
        _rr(c, -70, -60, 140, 120, 10)
        _shade(c, GOLD, 6, 0.25)
        g.line([(0, 60), (0, 110)], 6, GREY, amp=0)
        for i in range(3):   # คลื่นสัญญาณ
            u = (t * 0.8 + i / 3) % 1
            g.arc(0, 110, 30 + 80 * u, math.radians(50), math.radians(130), 5, (*BEAM, 1 - u))


def rocket(g, x, y, sc=1.0, rot=0.0, flame=1.0, t=0.0):
    c = g.c
    with g.at(x, y, sc, rot):
        if flame > 0:
            fl = 1 + 0.15 * math.sin(t * 25)
            _smooth_path(c, [(-30, 120), (0, 120 + 140 * flame * fl), (30, 120)])
            _shade(c, hexc("#f08a3a"), 4, 0)
        _smooth_path(c, [(0, -200), (50, -90), (50, 120), (-50, 120), (-50, -90)])
        _shade(c, WHITE, 6, 0.25)
        for sx in (-1, 1):
            _smooth_path(c, [(sx * 50, 40), (sx * 100, 140), (sx * 50, 120)])
            _shade(c, RED, 5, 0.2)
        g.circle(0, -60, 24, hexc("#8fb8de"), 5)


def planet(g, x, y, r, col=hexc("#c8553d")):
    c = g.c
    c.new_path()
    c.arc(x, y, r, 0, 2 * math.pi)
    _shade(c, col, 6, 0.35)
    for i in range(4):
        g.circle(x - r * 0.4 + hn(i, 2) * r * 0.8, y - r * 0.4 + hn(i, 3) * r * 0.8, r * 0.12, (0, 0, 0, 0.15), 0)


def airplane(g, x, y, sc=1.0, rot=0.0):
    c = g.c
    with g.at(x, y, sc, rot):
        _smooth_path(c, [(-200, -10), (160, -24), (220, 0), (160, 24), (-200, 10)])
        _shade(c, WHITE, 6, 0.2, horiz=False)
        for sy in (-1, 1):
            c.new_path()
            for px, py in [(-10, sy * 16), (-90, sy * 160), (-40, sy * 160), (70, sy * 18)]:
                c.line_to(px, py)
            c.close_path()
            _shade(c, hexc("#c9cdd3"), 5, 0.2)
        c.new_path()
        for px, py in [(-180, -8), (-230, -80), (-200, -80), (-140, -10)]:
            c.line_to(px, py)
        c.close_path()
        _shade(c, RED, 5, 0.2)


def atom(g, x, y, r, t=0.0, col=hexc("#e3a92b")):
    """อะตอมก๊าซคริปทอน-86 + คลื่นแสงที่ปล่อยออกมา"""
    for i in range(3):
        with g.at(x, y, 1, i * 60 + t * 20):
            g.c.new_path()
            g.c.save()
            g.c.scale(1, 0.38)
            g.c.arc(0, 0, r, 0, 2 * math.pi)
            g.c.restore()
            g.c.set_source_rgba(*INK)
            g.c.set_line_width(4)
            g.c.stroke()
            a = t * 3 + i * 2
            g.circle(math.cos(a) * r, math.sin(a) * r * 0.38, 12, hexc("#3f6496"), 3)
    g.circle(x, y, r * 0.22, col, 5)
    g.text("Kr", x, y, 34, "kanit", INK)


def wave(g, x0, x1, y, amp, wl, t, col=hexc("#d9608c"), lw=7):
    pts = [(x, y + amp * math.sin((x - x0) / wl * 2 * math.pi - t * 6)) for x in range(int(x0), int(x1), 8)]
    g.line(pts, lw, col, amp=0)


def stars(g, t, n=26, area=(-200, 300, 1280, 1250), seed=5):
    for i in range(n):
        x = area[0] + hn(i, seed) * (area[2] - area[0])
        y = area[1] + hn(i, seed + 1) * (area[3] - area[1])
        g.sparkle(x, y, 6 + 5 * hn(i, seed + 2) + 2 * math.sin(t * 3 + i), (1, 1, 1, 0.9), 0)


def space_panel(g, x0=60, y0=300, x1=1020, y1=1240):
    _rr(g.c, x0, y0, x1 - x0, y1 - y0, 40)
    _shade(g.c, SPACE, 6, 0.0)
