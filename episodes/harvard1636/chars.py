"""ตัวละครและพร็อพ: ก่อตั้งวิทยาลัยที่กลายเป็นฮาร์วาร์ด (28 ต.ค. 1636)
ไม่ใช้ตราสัญลักษณ์จริงของมหาวิทยาลัย — วาดอาคารอิฐ/หนังสือ/หมวกบัณฑิตทั่วไป
จอห์น ฮาร์วาร์ดไม่มีภาพเหมือนจริงหลงเหลือ — วาดเป็นศาสนาจารย์หนุ่มชุดดำปกขาวตามยุค"""
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


_nob = _load("nobel1833")
_rr58 = _load("roosevelt1858")
medal, quill, candle = _nob.medal, _nob.quill, _nob.candle
tree = _rr58.tree

CRIMSON = hexc("#a51c30")
BRICK = hexc("#b5523b")
PARCH = hexc("#f1e3c0")
PURITAN = hexc("#26231f")

# ผู้ตั้งถิ่นฐานพิวริตัน: ชุดดำ ปกขาวแบน หมวกทรงสูงยอดตัด
PURITANS = [
    Look(hair="long", hair_col=hexc("#4a3a2c"), suit=PURITAN, outfit="vest", shirt=PURITAN, tie=PURITAN, band=True,
         facial="beard", w=58, age=0.6, hat="tophat", hat_trim=hexc("#8a6a3a")),
    Look(hair="long", hair_col=hexc("#8a6a42"), suit=hexc("#3a3632"), outfit="vest", shirt=hexc("#3a3632"),
         tie=hexc("#3a3632"), band=True, w=56, age=0.4, hat="tophat", hat_trim=hexc("#8a6a3a")),
    Look(hair="bun", hair_col=hexc("#5a3a22"), outfit="dress", suit=hexc("#4a4a52"), w=54, age=0.4, height=0.93,
         band=True),
]
# จอห์น ฮาร์วาร์ด (30): ศาสนาจารย์หนุ่ม ผมยาวประบ่า ชุดดำ ปกขาว
JOHN = Look(hair="long", hair_col=hexc("#6b4a33"), suit=PURITAN, outfit="vest", shirt=PURITAN, tie=PURITAN, band=True,
            w=56, jaw=0.4, age=0.2, facial="mustache")
TEACHER = Look(hair="long", hair_col=hexc("#2b2622"), suit=PURITAN, outfit="vest", shirt=PURITAN, tie=PURITAN,
               band=True, facial="beard", w=58, age=0.5)
STUDENT = Look(hair="short", hair_col=hexc("#6b4a33"), outfit="vest", suit=hexc("#3a3632"), shirt=WHITE, w=55,
               age=0.0, band=True)
MODERN = [
    Look(hair="short", hair_col=hexc("#2b2622"), outfit="hoodie", suit=CRIMSON, pants=hexc("#3a4a6a"), w=55, age=0.0),
    Look(hair="bun", hair_col=hexc("#8a5a2a"), outfit="tee", suit=WHITE, pants=hexc("#2b2f3a"), w=54, age=0.0,
         height=0.93, glasses="round"),
    Look(hair="buzz", hair_col=hexc("#1b1714"), outfit="flannel", suit=hexc("#5a6a8a"), pants=hexc("#3a3a40"),
         skin=hexc("#7a4a2c"), w=55, age=0.05),
]


def forest(g, y, t=0.0, x0=-300, x1=1400, n=12, sc=0.9):
    for i in range(n):
        x = x0 + (x1 - x0) * i / (n - 1) + 30 * math.sin(i * 2.7)
        tree(g, x, y + (i % 2) * 10, sc * (0.85 + 0.2 * ((i * 37) % 10) / 10), t)


def cabin(g, x, y, sc=1.0, label=""):
    """บ้านไม้ซุงหลังเล็ก (โรงเรียนแห่งแรก)"""
    c = g.c
    with g.at(x, y, sc):
        for i in range(6):
            _rr(c, -220, -40 - i * 40, 440, 40, 20)
            _shade(c, hexc("#9a6a3a"), 5, 0.25)
        c.new_path()
        for p in [(-260, -230), (0, -380), (260, -230)]:
            c.line_to(*p)
        c.close_path()
        _shade(c, hexc("#6e4528"), 6, 0.2)
        _rr(c, -40, -150, 80, 150, 6)
        _shade(c, hexc("#4a2e1a"), 4, 0.1)
        _rr(c, 90, -170, 80, 70, 4)
        _shade(c, hexc("#f2d68a"), 4, 0)
        if label:
            g.text(label, 0, -270, 34, "kanit", WHITE)


def hall(g, x, y, sc=1.0, t=0.0):
    """อาคารอิฐแดงยอดหอนาฬิกา (มหาวิทยาลัยยุคใหม่ ทั่วไป)"""
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -330, -300, 660, 300, 4)
        _shade(c, BRICK, 6, 0.25)
        for r in range(2):
            for i in range(7):
                _rr(c, -290 + i * 85, -270 + r * 130, 50, 90, 6)
                _shade(c, WHITE, 4, 0.05)
        c.new_path()
        for p in [(-360, -300), (0, -400), (360, -300)]:
            c.line_to(*p)
        c.close_path()
        _shade(c, hexc("#3a3f48"), 6, 0.2)
        _rr(c, -60, -560, 120, 180, 4)
        _shade(c, BRICK, 5, 0.2)
        g.circle(0, -480, 40, WHITE, 4)
        a = t * 0.5
        g.line([(0, -480), (28 * math.sin(a), -480 - 28 * math.cos(a))], 4, INK, amp=0)
        c.new_path()
        for p in [(-70, -560), (0, -660), (70, -560)]:
            c.line_to(*p)
        c.close_path()
        _shade(c, WHITE, 5, 0.1)


def book(g, x, y, sc=1.0, rot=0.0, col=CRIMSON, open_=False):
    c = g.c
    with g.at(x, y, sc, rot):
        if open_:
            for sx in (-1, 1):
                _smooth_path(c, [(0, 0), (sx * 120, -20), (sx * 130, -150), (0, -130)])
                _shade(c, PARCH, 5, 0.1)
                for k in range(4):
                    _stroke(c, [(sx * 20, -110 + k * 24), (sx * 105, -120 + k * 24)], 3, GREY, 0.6, smooth=False)
        else:
            _rr(c, -60, -170, 120, 170, 6)
            _shade(c, col, 5, 0.3)
            _rr(c, -45, -150, 90, 24, 4)
            _shade(c, GOLD, 3, 0)


def shelf(g, x, y, sc=1.0, n=1.0, t=0.0):
    """ชั้นหนังสือ (ห้องสมุดของจอห์น ฮาร์วาร์ด) n = สัดส่วนหนังสือที่วาง"""
    c = g.c
    cols = [CRIMSON, hexc("#3f6496"), hexc("#3c8d4f"), hexc("#8a5a2a"), hexc("#5a3a5a")]
    with g.at(x, y, sc):
        _rr(c, -280, -560, 560, 560, 8)
        _shade(c, hexc("#7a4a2a"), 7, 0.25)
        k = 0
        for r in range(3):
            _rr(c, -260, -180 - r * 180, 520, 16, 4)
            _shade(c, hexc("#5a3a22"), 3, 0)
            for i in range(11):
                k += 1
                if k > int(33 * n):
                    continue
                h = 120 + (i * 37 % 40)
                _rr(c, -250 + i * 46, -180 - r * 180 - h, 40, h, 4)
                _shade(c, cols[(i + r) % 5], 3, 0.2)


def will_scroll(g, x, y, sc=1.0, rot=0.0, write=1.0):
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -200, -260, 400, 520, 8)
        _shade(c, PARCH, 6, 0.15)
        g.text("พินัยกรรม", 0, -200, 50, "kanit", INK)
        g.text("1638", 0, -145, 30, "kanitm", GREY)
        for k in range(int(7 * write)):
            _stroke(c, [(-150, -90 + k * 40), (150 - (k % 3) * 40, -90 + k * 40)], 4, NAVY, 0.8)
        g.text("½", -90, 200, 60, "kanit", RED)
        g.text("400 เล่ม", 70, 200, 40, "kanit", INK)


def pounds(g, x, y, sc=1.0, t=0.0, label="£400"):
    with g.at(x, y, sc):
        for i in range(5):
            with g.at(-80 + i * 40, -i * 22, 1):
                g.circle(0, 0, 50, GOLD, 5)
                g.text("£", 0, 0, 50, "kanit", INK)
        g.label(label, 0, 120, 80, color=GOLD2 if False else hexc("#b37a12"))


def grad_cap(g, x, y, sc=1.0, rot=0.0, t=0.0):
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -90, -10, 180, 80, 20)
        _shade(c, INK, 4, 0)
        c.new_path()
        for p in [(-200, -20), (0, -100), (200, -20), (0, 60)]:
            c.line_to(*p)
        c.close_path()
        _shade(c, hexc("#2b2622"), 5, 0.1)
        sw = 10 * math.sin(t * 3)
        _stroke(c, [(0, -20), (150, 10), (150 + sw, 110)], 6, GOLD, smooth=False)
        g.circle(150 + sw, 120, 16, GOLD, 3)


def seedling(g, x, y, k=0.0, t=0.0, sc=1.0):
    """เมล็ด → ต้นกล้า → ต้นไม้ใหญ่ (k 0..1)"""
    c = g.c
    with g.at(x, y, sc):
        g.blob(0, 10, 260, 40, hexc("#8a6a42"), 5, seed=2)   # ดินแห้ง
        if k < 0.15:
            g.blob(0, -10, 24, 16, hexc("#6e4528"), 4, seed=3)
            return
        h = 60 + 520 * k
        _stroke(c, [(0, 0), (6 * math.sin(t), -h)], 10 + 30 * k, hexc("#7a4a2a"))
        r = 40 + 260 * k
        for i, (dx, dy) in enumerate(((0, -h), (-r * 0.6, -h + r * 0.3), (r * 0.6, -h + r * 0.3))):
            g.blob(dx, dy, r * 0.7, r * 0.55, hexc("#3c8d4f"), 6, seed=5 + i)


def watering_can(g, x, y, sc=1.0, rot=0.0, t=0.0, pour=1.0):
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -80, -70, 160, 120, 20)
        _shade(c, hexc("#5a8ab8"), 5, 0.2)
        _stroke(c, [(70, -40), (170, -110)], 16, hexc("#4a7aa8"), smooth=False)
        g.arc(-100, -10, 50, 100, 260, 10, hexc("#4a7aa8"))
    if pour > 0:
        for i in range(6):
            u = (t * 2 + i / 6) % 1
            g.circle(x + 170 * sc + 30 * u, y - 100 * sc + 160 * u, 8, (0.5, 0.7, 0.95, 1 - u), 0)


def nine_students(g, x, y, t=0.0, k=1.0, sc=0.42):
    from people import person
    for i in range(int(9 * k + 0.999)):
        px = x + (i % 5 - 2) * 130 + (i // 5) * 65
        py = y - (i // 5) * 0
        person(g, px, py, STUDENT, sc * (1 - 0.15 * (i // 5)), mood="smile", pose="down", turn=0.1 * (i - 4),
               seed=60 + i, shadow=i < 5)


def president_icon(g, x, y, sc=1.0, k=1.0):
    if k < 0.02:
        return
    with g.at(x, y, sc * k):
        g.circle(0, -70, 36, hexc("#f0c8a8"), 4)
        g.poly([(-50, 60), (-42, -20), (42, -20), (50, 60)], NAVY, 4, amp=0)
        g.star(0, 10, 14, GOLD, 2)
