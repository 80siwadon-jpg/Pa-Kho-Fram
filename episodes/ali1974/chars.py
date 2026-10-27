"""ตัวละครและพร็อพ: The Rumble in the Jungle (30 ต.ค. 1974) อาลี vs โฟร์แมน ที่กินชาซา
ชกมวยวาดแบบการ์ตูน ไม่มีเลือด/บาดแผล — หมัดเข้าเป้าใช้ดาววิ้ง เส้นความเร็ว"""
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


_bo = _load("boeing707_1958")
_cu = _load("cuba1962")
globe = _bo.globe
tv = _cu.tv

RED_C = hexc("#c8343a")
BLUE_C = hexc("#2b5fa8")
CANVAS = hexc("#e9e2cf")
SKIN_ALI = hexc("#9a6a48")
SKIN_GF = hexc("#5e3d28")

GLOVE = hexc("#4a2a26")   # นวมสีน้ำตาลเข้ม (ตามภาพจริง)
# มูฮัมหมัด อาลี วัย 32: ผมดำสั้นเรียบ หน้าหล่อเกลี้ยงเกลา ยิ้มมั่นใจ กางเกงมวยขาวขอบดำ นวมน้ำตาลเข้ม รองเท้าขาว
ALI = Look(hair="short", hair_col=hexc("#1b1714"), skin=SKIN_ALI, outfit="bare", shorts=True, pants=WHITE,
           shirt=INK, socks=WHITE, shoes=WHITE, gloves=GLOVE, w=60, jaw=0.5, nose=1.0, brow=1.0, age=0.15, build=1.12)
ALI_SUIT = Look(hair="short", hair_col=hexc("#1b1714"), skin=SKIN_ALI, suit=hexc("#2b2f3a"), tie=hexc("#1b1714"),
                w=60, jaw=0.5, age=0.15, build=1.1)
# จอร์จ โฟร์แมน วัย 25: ตัวใหญ่สูงกว่า ผมหยิกฟูสั้น หนวด หน้าดุ กางเกงแดงขอบน้ำเงิน นวมน้ำตาลเข้ม
FOREMAN = Look(hair="afro", hair_col=hexc("#1b1714"), skin=SKIN_GF, outfit="bare", shorts=True, pants=RED_C,
               shirt=BLUE_C, socks=WHITE, shoes=WHITE, gloves=GLOVE, w=64, jaw=0.85, nose=1.1, brow=1.3, age=0.1, build=1.28,
               height=1.04, facial="mustache")
REFEREE = Look(hair="bald", hair_col=hexc("#8a8a8a"), skin=hexc("#6a4530"), outfit="vest", suit=WHITE, shirt=WHITE,
               tie=INK, bowtie=True, pants=hexc("#2b2f3a"), w=58, age=0.6)
PUNDITS = [
    Look(hair="part", hair_col=hexc("#5a4632"), suit=hexc("#6a5a3a"), tie=hexc("#c8553d"), w=58, age=0.5,
         glasses="thick"),
    Look(hair="slick", hair_col=hexc("#2b2622"), suit=hexc("#3a4a6a"), tie=hexc("#e3a92b"), w=58, age=0.6,
         facial="mustache"),
]


def ring(g, y, t=0.0, sag=0.0, x0=60, x1=1020, night=False):
    """เวทีมวย (มองด้านหน้า): พื้นผ้าใบ เสามุม เชือก 3 เส้น — sag เชือกหย่อน (อาลีพิง) ที่ด้านซ้าย"""
    c = g.c
    _rr(c, x0 - 40, y, (x1 - x0) + 80, 70, 6)
    _shade(c, hexc("#2b2f3a"), 6, 0.2)
    _rr(c, x0 - 40, y - 24, (x1 - x0) + 80, 30, 4)
    _shade(c, CANVAS, 6, 0.1)
    for i, (x, col) in enumerate(((x0, RED_C), (x1, BLUE_C))):
        _rr(c, x - 16, y - 420, 32, 400, 8)
        _shade(c, hexc("#c9ced6"), 5, 0.3)
        _rr(c, x - 24, y - 420, 48, 140, 10)
        _shade(c, col, 5, 0.2)
    for k, yy in enumerate((y - 360, y - 270, y - 180)):
        pts = []
        for j in range(21):
            u = j / 20
            x = x0 + (x1 - x0) * u
            dy = sag * 60 * math.exp(-((u - 0.18) * 6) ** 2) * (1 - 0.2 * k)
            dx = -sag * 30 * math.exp(-((u - 0.18) * 6) ** 2)
            pts.append((x + dx, yy + dy * 0.4 + 3 * math.sin(t * 2 + j * 0.5 + k)))
        _stroke(c, pts, 12, (RED_C, WHITE, BLUE_C)[k], 1)
        _stroke(c, pts, 3, INK, 0.5)


def crowd(g, y, t=0.0, n=14, a=1.0, cheer=1.0, col=(0.16, 0.18, 0.26)):
    """ฝูงชนเงามืดโบกมือ"""
    for i in range(n):
        x = -40 + i * 1160 / n + 20 * math.sin(i * 2.3)
        hy = y - 40 - 20 * ((i * 37) % 3) - 12 * abs(math.sin(t * 4 + i)) * cheer
        g.circle(x, hy, 34, (*col, a), 0)
        g.c.new_path()
        g.c.arc(x, hy + 110, 70, math.pi, 2 * math.pi)
        g.c.set_source_rgba(*col, a)
        g.c.fill()
        if i % 2 and cheer > 0:
            arm = 0.4 * math.sin(t * 6 + i)
            g.line([(x + 40, hy + 60), (x + 70 + 30 * arm, hy - 50)], 18, (*col, a), amp=0)


def stars(g, x, y, t, r=80, n=5, k=1.0):
    """ดาววิ้งเวียนหัว (แทนบาดแผล)"""
    for i in range(n):
        a = t * 4 + i * 2 * math.pi / n
        g.star(x + r * math.cos(a), y + 0.35 * r * math.sin(a), 22 * k, GOLD2, 4)


def impact(g, x, y, s=1.0, t=0.0, k=1.0, col=(1, 0.85, 0.3)):
    """ประกายหมัดเข้าเป้า"""
    if k <= 0:
        return
    g.star(x, y, 70 * s * k, (*col[:3], 1), 5, pts=10, inner=0.5, rot=t * 50)
    for i in range(6):
        a = i * 1.05 + 0.3
        g.line([(x + 80 * s * math.cos(a), y + 80 * s * math.sin(a)),
                (x + 130 * s * math.cos(a), y + 130 * s * math.sin(a))], 6, (*INK[:3], k), amp=0)


def belt(g, x, y, sc=1.0, rot=0.0, shine=0.0, t=0.0):
    """เข็มขัดแชมป์ (ทั่วไป)"""
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -300, -45, 600, 90, 40)
        _shade(c, hexc("#2b2622"), 6, 0.2)
        c.new_path()
        c.arc(0, 0, 120, 0, 2 * math.pi)
        _shade(c, GOLD, 7, 0.35)
        c.new_path()
        c.arc(0, 0, 80, 0, 2 * math.pi)
        _shade(c, GOLD2, 5, 0.1)
        g.star(0, 0, 44, RED_C, 4)
        for sx in (-1, 1):
            _rr(c, sx * 190 - 40, -36, 80, 72, 14)
            _shade(c, GOLD, 5, 0.3)
    if shine > 0:
        g.sparkle(x + 90 * sc, y - 80 * sc, 30 * sc * (0.6 + 0.4 * math.sin(t * 6)), GOLD2)


def bell(g, x, y, sc=1.0, t=0.0, ring_k=1.0):
    c = g.c
    with g.at(x, y, sc, 14 * math.sin(t * 30) * ring_k):
        _smooth_path(c, [(-110, 40), (-90, -40), (-50, -100), (50, -100), (90, -40), (110, 40)])
        _shade(c, GOLD, 7, 0.35)
        _rr(c, -130, 30, 260, 30, 10)
        _shade(c, hexc("#c99320"), 5, 0.2)
        g.circle(0, 70, 22, hexc("#8a6a20"), 5)
    if ring_k > 0:
        for i in range(3):
            u = (t * 2 + i / 3) % 1
            g.arc(x, y, (150 + 160 * u) * sc, -50, 50, 7, (*GOLD[:3], (1 - u) * ring_k))
            g.arc(x, y, (150 + 160 * u) * sc, 130, 230, 7, (*GOLD[:3], (1 - u) * ring_k))


def hammer(g, x, y, sc=1.0, rot=0.0):
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -14, -20, 28, 260, 8)
        _shade(c, hexc("#8a5a3a"), 5, 0.2)
        _rr(c, -110, -90, 220, 90, 14)
        _shade(c, hexc("#6a6e78"), 6, 0.35)


def africa(g, x, y, sc=1.0, pin=1.0, t=0.0):
    """แผนที่แอฟริกาอย่างง่าย + หมุดกินชาซา (ซาอีร์)"""
    c = g.c
    with g.at(x, y, sc):
        _smooth_path(c, [(-150, -300), (-40, -330), (60, -310), (120, -240), (180, -180), (250, -170), (210, -60),
                         (150, 20), (140, 130), (80, 230), (20, 320), (-40, 300), (-60, 180), (-80, 60), (-120, -40),
                         (-220, -90), (-260, -180), (-220, -260)])
        _shade(c, hexc("#c9b083"), 7, 0.2)
        _smooth_path(c, [(-20, -40), (60, -60), (110, 0), (90, 80), (20, 100), (-30, 60)])
        _shade(c, hexc("#7fb069"), 4, 0.15)
        if pin > 0:
            with g.at(-20, 40 - 20 * abs(math.sin(t * 3)), pin):
                _smooth_path(c, [(0, 0), (-30, -50), (0, -80), (30, -50)])
                _shade(c, RED_C, 5, 0.2)
                g.circle(0, -52, 12, WHITE, 0)


def jungle(g, y, t=0.0, a=1.0):
    """ใบไม้ป่าดงดิบด้านข้าง (กรอบภาพ)"""
    c = g.c
    for i, (x, s, rot) in enumerate(((60, 1.0, 30), (140, 0.8, 60), (980, 1.0, -30), (900, 0.8, -60),
                                     (40, 0.9, 10), (1040, 0.9, -10))):
        with g.at(x, y - (i % 2) * 180, s, rot + 5 * math.sin(t * 1.5 + i)):
            _smooth_path(c, [(0, 0), (-70, -150), (0, -320), (70, -150)])
            _shade(c, (0.30, 0.55, 0.32, a), 5, 0.3)
            _stroke(c, [(0, 0), (0, -300)], 4, INK, 0.4, smooth=False)


def heat(g, x, y, t, n=3, k=1.0):
    for i in range(n):
        u = (t * 0.7 + i / n) % 1
        pts = [(x - 120 + i * 120 + 14 * math.sin(t * 4 + j + i), y - j * 30 - 140 * u) for j in range(5)]
        g.line(pts, 6, (1, 0.55, 0.2, (1 - u) * k), amp=0, smooth=True)


def battery(g, x, y, sc=1.0, level=1.0):
    c = g.c
    col = (0.24, 0.55, 0.31) if level > 0.6 else ((0.89, 0.76, 0.23) if level > 0.3 else (0.75, 0.2, 0.2))
    with g.at(x, y, sc):
        _rr(c, -150, -70, 300, 140, 20)
        _shade(c, WHITE, 7, 0.05)
        _rr(c, 150, -30, 30, 60, 8)
        _shade(c, INK, 4, 0)
        if level > 0.01:
            _rr(c, -132, -52, 264 * level, 104, 12)
            c.set_source_rgba(*col, 1)
            c.fill()


def punch_bag(g, x, y, sc=1.0, t=0.0, hit=0.0):
    c = g.c
    with g.at(x, y, sc, 8 * math.sin(t * 6) * hit):
        _stroke(c, [(0, -360), (0, -300)], 6, INK, 1, smooth=False)
        _rr(c, -90, -300, 180, 360, 70)
        _shade(c, hexc("#a8865a"), 7, 0.3)
        for k in (-200, -60):
            _stroke(c, [(-90, k), (90, k)], 4, INK, 0.4, smooth=False)


def count_card(g, x, y, n, sc=1.0):
    with g.at(x, y, sc):
        g.circle(0, 0, 110, WHITE, 7)
        g.text(str(n), 0, 0, 120, "kanit", RED_C)
