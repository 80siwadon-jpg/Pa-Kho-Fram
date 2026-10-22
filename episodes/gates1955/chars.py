"""ตัวละครและพร็อพ: วันเกิดบิล เกตส์ (28 ต.ค. 1955)
ไม่ใช้โลโก้จริงของ Microsoft/Windows/IBM — เขียนเป็นตัวหนังสือธรรมดา"""
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


_xp = _load("winxp2001")
_sp = _load("smallpox1977")
_mf = _load("macfarlane1973")
_hv = _load("harvard1636")
crt, keyboard, tower = _xp.crt, _xp.keyboard, _xp.tower
syringe, virus, KIDS = _sp.syringe, _sp.virus, _sp.KIDS
money = _mf.money
hall, grad_cap = _hv.hall, _hv.grad_cap

BEIGE = hexc("#e6dfcc")
MS_BLUE = hexc("#2b6fd1")

# บิล เกตส์ วัยหนุ่ม (ยุค 70): ผมทรงกะลาสีน้ำตาลอ่อนปรกหน้าผาก แว่นกรอบใหญ่ หน้าเด็ก ผอม เสื้อกันหนาว
GATES_YOUNG = Look(hair="full", hair_col=hexc("#a87a4a"), outfit="hoodie", suit=hexc("#6b8aa8"), pants=hexc("#3a4a6a"),
                   w=56, jaw=0.3, nose=0.95, age=0.0, build=0.85, glasses="thick")
GATES_KID = Look(hair="full", hair_col=hexc("#b8885a"), outfit="tee", suit=hexc("#c8553d"), pants=hexc("#3a4a6a"),
                 w=55, age=0.0, height=0.62, headsc=1.45, glasses="thick")
# บิล เกตส์ ปัจจุบัน: ผมสีเทาขาวหวีข้าง แว่นสี่เหลี่ยมกรอบดำ ยิ้มกว้าง สูทกรมท่า เนกไทลายขวาง
GATES = Look(hair="part", hair_col=hexc("#c9c4ba"), suit=hexc("#1f2b4a"), tie=hexc("#5a2a3a"), w=60, jaw=0.5,
             nose=1.0, age=0.7, glasses="thick")
GATES_MID = Look(hair="part", hair_col=hexc("#8a6a4a"), suit=hexc("#2b2f3a"), tie=hexc("#2b4f8a"), w=58, jaw=0.4,
                 age=0.3, glasses="thick")
# พอล อัลเลน: เคราเต็ม แว่น ผมน้ำตาลเข้ม
ALLEN = Look(hair="short", hair_col=hexc("#4a3424"), outfit="flannel", suit=hexc("#8a5a3a"), pants=hexc("#3a3a40"),
             w=60, jaw=0.6, age=0.15, facial="beard", glasses="thin")
PARENTS = [
    Look(hair="part", hair_col=hexc("#5a4632"), suit=hexc("#2b2f3a"), tie=hexc("#2b3f63"), w=60, age=0.5,
         height=1.06, glasses="thin"),
    Look(hair="bun", hair_col=hexc("#a8763e"), outfit="dress", suit=hexc("#3f6a8a"), w=54, age=0.45, height=0.93),
]


def mainframe(g, x, y, sc=1.0, t=0.0):
    """คอมพิวเตอร์ยุค 60-70 ขนาดตู้เสื้อผ้า + ม้วนเทป + ไฟกะพริบ"""
    c = g.c
    with g.at(x, y, sc):
        for i in range(2):
            _rr(c, -300 + i * 310, -620, 290, 620, 10)
            _shade(c, hexc("#c9cdd2"), 6, 0.25)
        for i, cx in enumerate((-235, -85)):
            for r in range(2):
                g.circle(cx, -480 + r * 0, 0, WHITE, 0)
        for r in range(2):
            for i in range(2):
                cx, cy = -230 + i * 150, -500 + r * 180
                g.circle(cx, cy, 58, hexc("#3a3f48"), 5)
                g.circle(cx, cy, 20, WHITE, 3)
                a = t * 4 * (1 if i else -1)
                g.line([(cx, cy), (cx + 50 * math.cos(a), cy + 50 * math.sin(a))], 4, GREY, amp=0)
        for r in range(6):
            for i in range(6):
                on = math.sin(t * 6 + r * 1.7 + i * 2.3) > 0.2
                g.circle(60 + i * 36, -560 + r * 40, 9, (1, 0.3, 0.25, 1) if on else (0.5, 0.2, 0.2, 1), 2)
        _rr(c, 40, -280, 220, 160, 6)
        _shade(c, hexc("#3a3f48"), 4, 0.1)
        for k in range(5):
            _stroke(c, [(60, -260 + k * 28), (60 + 150 * ((k * 37 + int(t * 3)) % 10) / 10, -260 + k * 28)], 4,
                    (0.4, 1, 0.5, 1), smooth=False)


def teletype(g, x, y, sc=1.0, t=0.0):
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -200, -220, 400, 220, 16)
        _shade(c, BEIGE, 6, 0.25)
        _rr(c, -150, -330, 300, 120, 10)
        _shade(c, WHITE, 5, 0.05)
        for k in range(4):
            _stroke(c, [(-120, -310 + k * 24), (-120 + 200 * ((k * 3 + int(t * 4)) % 7) / 7, -310 + k * 24)], 3,
                    INK, 0.7, smooth=False)
        for r in range(3):
            for i in range(8):
                g.circle(-140 + i * 40 + 6 * r, -150 + r * 40, 13, hexc("#3a3f48"), 2)


def altair(g, x, y, sc=1.0, t=0.0):
    """ไมโครคอมพิวเตอร์รุ่นแรก (กล่องฟ้า แถวสวิตช์ ไฟแดง) — ไม่มีจอ"""
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -320, -200, 640, 200, 12)
        _shade(c, hexc("#3f6ea8"), 6, 0.25)
        _rr(c, -300, -140, 600, 120, 6)
        _shade(c, hexc("#2b2f3a"), 4, 0.05)
        for i in range(16):
            on = math.sin(t * 5 + i * 1.3) > 0
            g.circle(-270 + i * 36, -115, 8, (1, 0.3, 0.25, 1) if on else (0.45, 0.2, 0.2, 1), 2)
            _rr(c, -276 + i * 36, -75, 12, 34, 4)
            _shade(c, WHITE, 2, 0)
        g.text("8800", -230, -170, 30, "kanit", WHITE)


def magazine(g, x, y, sc=1.0, rot=0.0, t=0.0):
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -220, -300, 440, 600, 8)
        _shade(c, hexc("#f2d68a"), 6, 0.15)
        _rr(c, -220, -300, 440, 110, 8)
        _shade(c, RED, 0, 0)
        g.text("POPULAR", 0, -265, 40, "kanit", WHITE)
        g.text("ELECTRONICS", 0, -220, 34, "kanit", WHITE)
        g.text("JAN 1975", 0, -150, 28, "kanitsb", INK)
        altair(g, 0, 120, 0.6, t)
        g.text("WORLD'S FIRST", 0, 190, 30, "kanit", INK)
        g.text("MINICOMPUTER KIT", 0, 235, 26, "kanitsb", INK)


def garage(g, x, y, sc=1.0, label=""):
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -300, -380, 600, 380, 4)
        _shade(c, hexc("#e8dcc0"), 6, 0.2)
        c.new_path()
        for p in [(-340, -370), (0, -500), (340, -370)]:
            c.line_to(*p)
        c.close_path()
        _shade(c, hexc("#7a4a2a"), 6, 0.2)
        _rr(c, -220, -290, 440, 290, 6)
        _shade(c, hexc("#c9b083"), 5, 0.1)
        for k in range(5):
            _stroke(c, [(-220, -240 + k * 55), (220, -240 + k * 55)], 3, INK, 0.4, smooth=False)
        if label:
            g.rrect(-200, -470, 400, 70, 12, WHITE, 5)
            g.text(label, 0, -435, 44, "kanit", MS_BLUE)


def ibm_pc(g, x, y, sc=1.0, t=0.0, screen="dos"):
    """พีซียุค 80: กล่องเบจ + จอเขียว"""
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -280, -140, 560, 140, 10)
        _shade(c, BEIGE, 6, 0.2)
        for i in range(2):
            _rr(c, 40 + i * 110, -100, 90, 30, 4)
            _shade(c, hexc("#3a3f48"), 3, 0)
        _rr(c, -220, -520, 440, 360, 20)
        _shade(c, BEIGE, 6, 0.2)
        _rr(c, -180, -480, 360, 270, 14)
        _shade(c, hexc("#0e1a10"), 4, 0)
        if screen == "dos":
            g.text("MS-DOS", -100, -440, 34, "kanit", (0.4, 1, 0.5, 1))
            g.text("C:\\>", -120, -390, 32, "kanit", (0.4, 1, 0.5, 1))
            if math.sin(t * 6) > 0:
                _rr(c, -60, -405, 22, 30, 2)
                c.set_source_rgba(0.4, 1, 0.5, 1)
                c.fill()


def floppy(g, x, y, sc=1.0, rot=0.0, label="MS-DOS"):
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -140, -140, 280, 280, 10)
        _shade(c, hexc("#2b2f3a"), 6, 0.2)
        _rr(c, -100, -140, 200, 90, 4)
        _shade(c, hexc("#c9cdd2"), 4, 0.1)
        _rr(c, -110, 10, 220, 110, 6)
        _shade(c, WHITE, 4, 0)
        g.text(label, 0, 65, 36, "kanit", INK)


def key(g, x, y, sc=1.0, rot=0.0):
    """กุญแจ = กรรมสิทธิ์ซอฟต์แวร์"""
    c = g.c
    with g.at(x, y, sc, rot):
        c.new_path()
        c.arc(-110, 0, 60, 0, 2 * math.pi)
        _shade(c, GOLD, 7, 0.25)
        g.circle(-110, 0, 22, WHITE, 5)
        _rr(c, -60, -16, 220, 32, 6)
        _shade(c, GOLD, 6, 0.25)
        for i in range(2):
            _rr(c, 100 + i * 40, 10, 22, 40, 4)
            _shade(c, GOLD, 5, 0.2)


def window_screen(g, x, y, sc=1.0, t=0.0):
    """จอคอมพิวเตอร์มีหน้าต่าง (ทั่วไป ไม่ใช่โลโก้)"""
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -260, -200, 520, 380, 20)
        _shade(c, hexc("#3a3f48"), 6, 0.1)
        _rr(c, -230, -170, 460, 320, 8)
        _shade(c, hexc("#5aa0e0"), 3, 0)
        for i, (wx, wy) in enumerate(((-180, -130), (-40, -60))):
            with g.at(wx + 10 * math.sin(t + i), wy, 1):
                _rr(c, 0, 0, 220, 150, 8)
                _shade(c, WHITE, 4, 0.05)
                _rr(c, 0, 0, 220, 30, 8)
                _shade(c, MS_BLUE, 3, 0)
        _rr(c, -230, 120, 460, 30, 0)
        _shade(c, hexc("#2b4f9a"), 0, 0)


def pie(g, x, y, r, frac, col=MS_BLUE, label=""):
    c = g.c
    c.new_path()
    c.arc(x, y, r, 0, 2 * math.pi)
    _shade(c, hexc("#e9ecf0"), 6, 0.1)
    if frac > 0:
        c.new_path()
        c.move_to(x, y)
        c.arc(x, y, r - 3, -math.pi / 2, -math.pi / 2 + 2 * math.pi * frac)
        c.close_path()
        _shade(c, col, 5, 0.2)
    if label:
        g.label(label, x, y + r + 60, 70, color=col)


def crown(g, x, y, sc=1.0, rot=0.0):
    with g.at(x, y, sc, rot):
        g.poly([(-120, 60), (-140, -60), (-70, 0), (0, -90), (70, 0), (140, -60), (120, 60)], GOLD, 7)
        for px in (-140, 0, 140):
            g.circle(px, -60 if px else -90, 16, RED, 4)


def mosquito(g, x, y, sc=1.0, t=0.0, rot=0.0):
    c = g.c
    with g.at(x, y, sc, rot):
        for sx in (-1, 1):
            with g.at(0, -10, 1, sx * (20 + 25 * math.sin(t * 30))):
                g.blob(sx * 40, -30, 40, 18, (0.85, 0.92, 0.98, 0.8), 3, seed=4 + sx)
        g.blob(0, 0, 50, 16, hexc("#5a4a3a"), 4, seed=2)
        g.circle(55, -4, 14, hexc("#5a4a3a"), 3)
        _stroke(c, [(66, -4), (110, 6)], 3, INK, smooth=False)
        for i in range(3):
            _stroke(c, [(-20 + i * 20, 10), (-30 + i * 25, 50)], 3, INK)


def heart(g, x, y, r, col=RED, a=1.0):
    c = g.c
    c.new_path()
    c.move_to(x, y + r * 0.9)
    c.curve_to(x - r * 1.4, y - r * 0.2, x - r * 0.6, y - r * 1.2, x, y - r * 0.45)
    c.curve_to(x + r * 0.6, y - r * 1.2, x + r * 1.4, y - r * 0.2, x, y + r * 0.9)
    c.close_path()
    c.set_source_rgba(*col[:3], a)
    c.fill_preserve()
    c.set_source_rgba(*INK[:3], a)
    c.set_line_width(5)
    c.stroke()


def diploma(g, x, y, sc=1.0, rot=0.0, torn=0.0):
    c = g.c
    with g.at(x, y, sc, rot):
        for side in (-1, 1):
            with g.at(side * 40 * torn, 0, 1, side * 12 * torn):
                c.save()
                c.rectangle(-300 if side < 0 else 0, -200, 300, 400)
                c.clip()
                _rr(c, -220, -150, 440, 300, 10)
                _shade(c, hexc("#f4eedf"), 6, 0.1)
                g.text("DIPLOMA", 0, -90, 48, "kanit", hexc("#a51c30"))
                for k in range(3):
                    _stroke(c, [(-150, -20 + k * 40), (150, -20 + k * 40)], 4, GREY, 0.6, smooth=False)
                g.circle(130, 100, 34, RED, 4)
                c.restore()
