"""ตัวละครและพร็อพ: วันเกิดโจนัส ซอล์ก (28 ต.ค. 1914) — วัคซีนโปลิโอที่ไม่จดสิทธิบัตร
โรคโปลิโอ: ไม่วาดความพิการแบบน่ากลัว ใช้ปอดเหล็ก/ไม้ค้ำ/สระที่ปิดแทน"""
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


_sp = _load("smallpox1977")
_cu = _load("cuba1962")
_lv = _load("leeuwenhoek1632")
_mf = _load("macfarlane1973")
_gt = _load("gates1955")
syringe, virus, KIDS = _sp.syringe, _sp.virus, _sp.KIDS
tv = _cu.tv
compound_scope = _lv.compound_scope
money = _mf.money
heart = _gt.heart

VIRUS_RED = hexc("#d9665a")
LAB = hexc("#f4f6f8")

# โจนัส ซอล์ก: ผมดำหวีเรียบ หน้าผากเถิกสูง แว่นกรอบบนดำ (browline) หน้าเรียวยาว จมูกโด่ง
SALK = Look(hair="slick", hair_col=hexc("#2b2622"), suit=hexc("#5a5d63"), tie=hexc("#2b2f3a"), w=56, jaw=0.35,
            nose=1.15, brow=0.95, age=0.4, glasses="thick")
SALK_LAB = Look(hair="slick", hair_col=hexc("#2b2622"), suit=LAB, shirt=WHITE, tie=hexc("#2b2f3a"), w=56, jaw=0.35,
                nose=1.15, brow=0.95, age=0.4, glasses="thick")
SALK_KID = Look(hair="short", hair_col=hexc("#2b2622"), outfit="vest", suit=hexc("#5a5d63"), w=54, age=0.0,
                height=0.6, headsc=1.45)
PARENTS = [
    Look(hair="short", hair_col=hexc("#3a2a1e"), outfit="vest", suit=hexc("#4a3a2c"), w=58, age=0.5,
         facial="mustache", hat="bowler"),
    Look(hair="bun", hair_col=hexc("#2b2622"), outfit="dress", suit=hexc("#6a5a6a"), w=54, age=0.45, height=0.93),
]
# เอ็ดเวิร์ด อาร์. เมอร์โรว์: ผมดำหวีเสยเรียบ คิ้วเข้ม หน้าเข้ม สูทเข้ม
MURROW = Look(hair="slick", hair_col=hexc("#1b1714"), suit=hexc("#2b2f3a"), tie=hexc("#1b1714"), w=58, jaw=0.6,
              brow=1.3, age=0.45)
WIFE = Look(hair="bun", hair_col=hexc("#5a3a22"), outfit="dress", suit=hexc("#8a5a6a"), w=54, age=0.3, height=0.93)
SONS = [Look(hair="short", hair_col=hexc("#3a2a1e"), outfit="tee", suit=c, pants=hexc("#3a4a6a"), w=54, age=0.0,
             height=h, headsc=1.45) for c, h in ((hexc("#3f6496"), 0.6), (hexc("#c8553d"), 0.52), (hexc("#3c8d4f"), 0.45))]
PUPILS = [
    Look(hair="short", hair_col=hexc("#8a6a42"), outfit="tee", suit=hexc("#e3a92b"), pants=hexc("#3a4a6a"), w=54,
         height=0.6, headsc=1.45),
    Look(hair="bun", hair_col=hexc("#3a2a1e"), outfit="dress", suit=hexc("#d76b5a"), w=54, height=0.58, headsc=1.45),
    Look(hair="buzz", hair_col=hexc("#1b1714"), outfit="tee", suit=hexc("#5a8ab8"), pants=hexc("#3a3a40"),
         skin=hexc("#7a4a2c"), w=54, height=0.6, headsc=1.45),
]


def iron_lung(g, x, y, sc=1.0, t=0.0, kid=True):
    """ปอดเหล็ก: ถังทรงกระบอกยาวบนขาตั้ง มีศีรษะเด็กโผล่ด้านหนึ่ง"""
    c = g.c
    from people import head
    with g.at(x, y, sc):
        for lx in (-220, 200):
            _rr(c, lx - 10, -120, 20, 120, 4)
            _shade(c, GREY, 4, 0)
        breathe = 4 * math.sin(t * 2)
        _rr(c, -300, -330 - breathe, 560, 230 + breathe, 110)
        _shade(c, hexc("#e6d8a0"), 7, 0.3, horiz=False)
        for i in range(4):
            g.circle(-160 + i * 110, -220, 24, hexc("#9ad0f5"), 4)
        _rr(c, 250, -300, 40, 170, 12)
        _shade(c, hexc("#c9ced6"), 5, 0.1)
        if kid:
            with g.at(330, -230, 0.55, 90):
                head(g, KIDS[0], "sad", 0, 0.2, (0, 0), 7, 4.5)


def pool_closed(g, x, y, sc=1.0, t=0.0):
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -360, -60, 720, 60, 6)
        _shade(c, hexc("#9ad0f5"), 6, 0.1)
        for i in range(6):
            g.arc(-300 + i * 120, -30, 20, 200, 340, 4, WHITE)
        for sx in (-1, 1):
            _stroke(c, [(sx * 300, -60), (sx * 300, -280)], 10, GREY, smooth=False)
        _stroke(c, [(-300, -240), (300, -240)], 6, hexc("#7a4a2a"), smooth=False)
        with g.at(0, -240, 1, 4 * math.sin(t * 2)):
            g.rrect(-150, 0, 300, 110, 10, RED, 6)
            g.text("CLOSED", 0, 55, 54, "kanit", WHITE)


def house_closed(g, x, y, sc=1.0):
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -180, -260, 360, 260, 6)
        _shade(c, hexc("#e8dcc0"), 6, 0.2)
        c.new_path()
        for p in [(-210, -250), (0, -380), (210, -250)]:
            c.line_to(*p)
        c.close_path()
        _shade(c, hexc("#7a4a2a"), 6, 0.2)
        for wx in (-110, 110):
            _rr(c, wx - 50, -200, 100, 90, 4)
            _shade(c, hexc("#4a5068"), 4, 0)
            for k in range(4):
                _stroke(c, [(wx - 50, -190 + k * 22), (wx + 50, -190 + k * 22)], 4, hexc("#8a6a42"), smooth=False)
        _rr(c, -40, -130, 80, 130, 6)
        _shade(c, hexc("#6e4528"), 4, 0.1)


def crutches(g, x, y, sc=1.0, rot=0.0):
    c = g.c
    with g.at(x, y, sc, rot):
        for sx in (-1, 1):
            with g.at(sx * 40, 0, 1, sx * 5):
                _stroke(c, [(0, 0), (0, -380)], 12, hexc("#8a6a42"), smooth=False)
                _rr(c, -40, -400, 80, 22, 8)
                _shade(c, hexc("#5a3a22"), 4, 0)


def vial(g, x, y, sc=1.0, rot=0.0, label="VACCINE", glow=0.0):
    c = g.c
    with g.at(x, y, sc, rot):
        if glow > 0:
            g.circle(0, -80, 150, (1, 0.9, 0.5, 0.3 * glow), 0)
        _rr(c, -60, -200, 120, 200, 18)
        _shade(c, hexc("#e6f2fa"), 6, 0.1)
        _rr(c, -52, -110, 104, 100, 12)
        _shade(c, hexc("#f2c25c"), 0, 0)
        _rr(c, -40, -250, 80, 56, 8)
        _shade(c, hexc("#3a3f48"), 5, 0)
        _rr(c, -56, -170, 112, 50, 4)
        _shade(c, WHITE, 3, 0)
        g.text(label, 0, -145, 22, "kanit", INK)


def dead_virus(g, x, y, r, t=0.0, dead=1.0):
    """ไวรัส → ตายแล้ว (ตา X, สีซีด)"""
    col = tuple(VIRUS_RED[i] * (1 - dead) + 0.75 * dead for i in range(3)) + (1,)
    virus(g, x, y, r, t * (1 - dead), "angry" if dead < 0.5 else "sad", col)
    if dead > 0.5:
        for sx in (-1, 1):
            g.line([(x + sx * r * 0.35 - 12, y - r * 0.2 - 12), (x + sx * r * 0.35 + 12, y - r * 0.2 + 12)], 6, INK,
                   amp=0)
            g.line([(x + sx * r * 0.35 + 12, y - r * 0.2 - 12), (x + sx * r * 0.35 - 12, y - r * 0.2 + 12)], 6, INK,
                   amp=0)


def bell(g, x, y, sc=1.0, t=0.0, ring=1.0):
    c = g.c
    a = 18 * math.sin(t * 6) * ring
    with g.at(x, y, sc, a):
        _smooth_path(c, [(-20, -150), (20, -150), (60, -100), (70, 0), (110, 40), (-110, 40), (-70, 0), (-60, -100)])
        _shade(c, GOLD, 7, 0.3)
        g.circle(0, 60 + 0, 22, hexc("#8a6a3a"), 4)
    if ring > 0:
        for i in range(3):
            u = (t * 1.5 + i / 3) % 1
            g.arc(x, y - 40 * sc, (130 + 120 * u) * sc, -50, 50, 6, (*GOLD2[:3], (1 - u) * ring))
            g.arc(x, y - 40 * sc, (130 + 120 * u) * sc, 130, 230, 6, (*GOLD2[:3], (1 - u) * ring))


def headline(g, x, y, sc=1.0, rot=0.0, head="IT WORKS!", sub="SALK VACCINE SAFE"):
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -280, -340, 560, 680, 6)
        _shade(c, hexc("#f4efe2"), 6, 0.15)
        g.text("THE DAILY NEWS", 0, -290, 40, "kanit", INK)
        _stroke(c, [(-250, -258), (250, -258)], 4, INK, smooth=False)
        g.text("APRIL 12, 1955", 0, -232, 22, "kanitm", GREY)
        g.text(head, 0, -150, 76, "kanit", RED)
        g.text(sub, 0, -80, 32, "kanitsb", INK)
        vial(g, -120, 180, 0.8, -6)
        for k in range(6):
            _stroke(c, [(20, -20 + k * 40), (250, -20 + k * 40)], 5, GREY, 0.5, smooth=False)


def sun(g, x, y, r, t=0.0, face=True):
    g.sunburst(x, y, r * 1.15, r * 1.8, 18, t * 10, 10, GOLD2)
    g.circle(x, y, r, GOLD2, 7)
    if face:
        for sx in (-1, 1):
            g.arc(x + sx * r * 0.35, y - r * 0.1, r * 0.12, 200, 340, 6, INK)
        g.arc(x, y + r * 0.15, r * 0.35, 20, 160, 7, INK)


def patent(g, x, y, sc=1.0, rot=0.0, cross=0.0):
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -220, -290, 440, 580, 8)
        _shade(c, hexc("#f1e3c0"), 6, 0.15)
        g.text("PATENT", 0, -220, 64, "kanit", NAVY)
        g.text("No. ———", 0, -150, 30, "kanitm", GREY)
        for k in range(6):
            _stroke(c, [(-170, -80 + k * 40), (170 - (k % 2) * 60, -80 + k * 40)], 4, GREY, 0.5, smooth=False)
        g.circle(120, 210, 46, RED, 5)
    if cross > 0:
        k1 = min(1, cross * 2)
        g.line([(x - 240 * sc, y - 260 * sc), (x - 240 * sc + 480 * sc * k1, y - 260 * sc + 520 * sc * k1)], 18, RED,
               amp=0)
        if cross > 0.5:
            k2 = (cross - 0.5) * 2
            g.line([(x + 240 * sc, y - 260 * sc), (x + 240 * sc - 480 * sc * k2, y - 260 * sc + 520 * sc * k2)], 18,
                   RED, amp=0)


def price_tag(g, x, y, sc=1.0, rot=0.0, txt="ราคาทุน"):
    c = g.c
    with g.at(x, y, sc, rot):
        c.new_path()
        for p in [(-160, -70), (120, -70), (180, 0), (120, 70), (-160, 70)]:
            c.line_to(*p)
        c.close_path()
        _shade(c, hexc("#3c8d4f"), 6, 0.2)
        g.circle(120, 0, 14, WHITE, 4)
        g.text(txt, -20, 0, 50, "kanit", WHITE)


def globe(g, x, y, r, t=0.0):
    c = g.c
    c.new_path()
    c.arc(x, y, r, 0, 2 * math.pi)
    _shade(c, hexc("#8fb8de"), 6, 0.3)
    c.save()
    c.arc(x, y, r, 0, 2 * math.pi)
    c.clip()
    for i in range(5):
        cx = x + ((i * 0.37 + t * 0.06) % 1 * 2.4 - 1.2) * r
        g.blob(cx, y + (((i * 7919) % 100) / 100 - 0.5) * r * 1.2, r * 0.3, r * 0.2, hexc("#c9b083"), 0, 3 + i)
    c.restore()
    c.new_path()
    c.arc(x, y, r, 0, 2 * math.pi)
    c.set_source_rgba(*INK)
    c.set_line_width(6)
    c.stroke()
