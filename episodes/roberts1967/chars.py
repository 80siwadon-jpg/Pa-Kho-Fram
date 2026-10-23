"""ตัวละครและพร็อพ: วันเกิดจูเลีย โรเบิร์ตส์ (28 ต.ค. 1967)
ไม่ใช้โปสเตอร์/ภาพนิ่งภาพยนตร์จริง และไม่วาดรูปปั้นออสการ์จริง (ใช้ถ้วยทองทั่วไป)"""
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


_ph = _load("phoenix1974")
_kp = _load("katyperry1984")
_mf = _load("macfarlane1973")
golden_statue, film_strip, heart, clapper, paw = _ph.golden_statue, _ph.film_strip, _ph.heart, _ph.clapper, _ph.paw
spotlight, confetti, hollywood, suitcase = _kp.spotlight, _kp.confetti, _kp.hollywood, _kp.suitcase
money = _mf.money

AUBURN = hexc("#a8562a")
STRAW = hexc("#d9a45a")
PW_RED = hexc("#a8233a")

# จูเลีย โรเบิร์ตส์: ผมยาวลอนน้ำตาลทองอมแดง ยิ้มกว้างมาก ปากกว้าง ตาโต
JULIA = Look(hair="long", hair_col=STRAW, outfit="dress", suit=hexc("#1d1d21"), w=56, jaw=0.35, nose=1.0, brow=0.9,
             age=0.3, height=0.97)
JULIA_YOUNG = Look(hair="long", hair_col=AUBURN, outfit="tee", suit=hexc("#e8e0cc"), pants=hexc("#3a4a6a"), w=55,
                   jaw=0.3, age=0.0, height=0.97)
JULIA_KID = Look(hair="long", hair_col=AUBURN, outfit="dress", suit=hexc("#5a8ab8"), w=54, age=0.0, height=0.6,
                 headsc=1.45)
JULIA_RED = Look(hair="long", hair_col=AUBURN, outfit="dress", suit=PW_RED, w=55, jaw=0.3, age=0.05, height=0.97)
# ลุคแม่เลี้ยงเดี่ยวสู้คดี: ผมสีบลอนด์ยาว เสื้อเข้ารูปเสือดาว/สีสดแบบยุค 90
JULIA_ERIN = Look(hair="long", hair_col=hexc("#d9b070"), outfit="dress", suit=hexc("#3a3f48"), w=55, jaw=0.3,
                  age=0.2, height=0.97)
ERIC = Look(hair="part", hair_col=hexc("#6b4a33"), outfit="tee", suit=hexc("#3a3f48"), pants=hexc("#3a3a40"), w=58,
            age=0.1)
STARS = [
    Look(hair="bun", hair_col=hexc("#2b2622"), outfit="dress", suit=hexc("#5a3a5a"), w=54, age=0.2, height=0.95),
    Look(hair="long", hair_col=hexc("#8a5a2a"), outfit="dress", suit=hexc("#2b4f6a"), w=54, age=0.2, height=0.95),
]
ACTOR = Look(hair="slick", hair_col=hexc("#5a4632"), suit=hexc("#22252c"), tie=INK, w=60, age=0.4)
EXEC = Look(hair="bald", suit=hexc("#3a3f48"), tie=hexc("#7a2e2e"), w=62, age=0.6, jowls=0.3)
FAMILIES = [
    Look(hair="short", hair_col=hexc("#5a4632"), outfit="flannel", suit=hexc("#8a5a3a"), pants=hexc("#3a3a40"), w=57,
         age=0.3),
    Look(hair="bun", hair_col=hexc("#a8763e"), outfit="dress", suit=hexc("#3c8d4f"), w=54, age=0.3, height=0.93),
    Look(hair="short", hair_col=hexc("#8a6a42"), outfit="tee", suit=hexc("#e3a92b"), pants=hexc("#3a4a6a"), w=54,
         height=0.6, headsc=1.45),
]


def smile_icon(g, x, y, r, t=0.0, glow=1.0):
    """รอยยิ้มกว้างสดใส (ไอคอน)"""
    if glow > 0:
        g.sunburst(x, y, r * 1.15, r * 1.7, 16, t * 8, 8, (1, 0.85, 0.4, 0.6 * glow))
    g.circle(x, y, r, hexc("#f6e0c8"), 7)
    for sx in (-1, 1):
        g.arc(x + sx * r * 0.35, y - r * 0.15, r * 0.12, 200, 340, 6, INK)
    c = g.c
    c.new_path()
    c.arc(x, y + r * 0.05, r * 0.55, math.radians(15), math.radians(165))
    c.close_path()
    c.set_source_rgba(1, 1, 1, 1)
    c.fill_preserve()
    c.set_source_rgba(*INK)
    c.set_line_width(6)
    c.stroke()


def dog(g, x, y, sc=1.0, t=0.0):
    c = g.c
    with g.at(x, y, sc):
        g.blob(0, -60, 110, 60, hexc("#c99a62"), 6, seed=2)
        for lx in (-70, -30, 40, 80):
            _rr(c, lx - 12, -20, 24, 70, 8)
            _shade(c, hexc("#b8884a"), 4, 0.1)
        g.blob(110, -120, 55, 48, hexc("#c99a62"), 6, seed=3)
        g.blob(90, -150, 22, 40, hexc("#8a5a2a"), 4, seed=4)
        g.circle(125, -128, 7, INK, 0)
        g.circle(160, -112, 9, INK, 0)
        _stroke(c, [(-110, -80), (-160, -130 + 15 * math.sin(t * 10))], 10, hexc("#b8884a"))


def vet_kit(g, x, y, sc=1.0):
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -120, -90, 240, 160, 16)
        _shade(c, WHITE, 6, 0.1)
        _rr(c, -40, -130, 80, 44, 12)
        _shade(c, INK, 0, 0)
        _rr(c, -18, -60, 36, 100, 4)
        c.set_source_rgba(*RED)
        c.fill()
        _rr(c, -50, -28, 100, 36, 4)
        c.set_source_rgba(*RED)
        c.fill()


def nyc(g, y, t=0.0):
    """เส้นขอบฟ้านิวยอร์ก"""
    c = g.c
    hs = [220, 340, 280, 420, 300, 500, 260, 380]
    for i, h in enumerate(hs):
        x = 140 + i * 105
        _rr(c, x, y - h, 90, h, 3)
        _shade(c, hexc("#c9cdd2"), 4, 0.15)
        for r in range(int(h / 60)):
            for k in range(2):
                _rr(c, x + 15 + k * 40, y - h + 20 + r * 60, 20, 26, 2)
                c.set_source_rgba(1, 0.9, 0.55, 0.8 if (i + r + k) % 3 else 0.3)
                c.fill()


def price_card(g, x, y, sc=1.0, rot=0.0, txt="$3,000", col=INK):
    with g.at(x, y, sc, rot):
        g.rrect(-200, -80, 400, 160, 20, WHITE, 8, stroke=col)
        g.text(txt, 0, 0, 84, "kanit", col)


def boxoffice(g, x, y, sc=1.0, k=1.0, t=0.0):
    """กราฟรายได้พุ่ง"""
    with g.at(x, y, sc):
        g.rrect(-260, -220, 520, 440, 20, WHITE, 7)
        g.line([(-220, 180), (220, 180)], 6, INK, amp=0)
        for i in range(5):
            h = 60 + 60 * i
            kk = max(0.0, min(1.0, k * 5 - i))
            if kk > 0:
                g.rrect(-200 + i * 85, 180 - h * kk, 60, h * kk, 6, hexc("#3c8d4f"), 5)
        g.star(160, -160, 30, GOLD2, 4)


def gavel(g, x, y, sc=1.0, rot=0.0):
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -10, -20, 20, 220, 8)
        _shade(c, hexc("#8a5a3a"), 5, 0.2)
        _rr(c, -80, -70, 160, 70, 20)
        _shade(c, hexc("#6a3a22"), 6, 0.25)


def factory(g, x, y, sc=1.0, t=0.0):
    """โรงงานบริษัทยักษ์ + น้ำเสียซึมลงดิน"""
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -260, -260, 520, 260, 6)
        _shade(c, hexc("#8a9096"), 6, 0.25)
        for i in range(2):
            _rr(c, -200 + i * 140, -460, 70, 220, 4)
            _shade(c, hexc("#6a6f78"), 5, 0.2)
            for k in range(3):
                u = (t * 0.5 + k / 3 + i * 0.2) % 1
                g.circle(-165 + i * 140 - 40 * u, -480 - 120 * u, 26 + 26 * u, (0.6, 0.6, 0.62, 1 - u), 0)
        g.blob(160, 20, 140, 30, hexc("#8ab84a"), 4, seed=7)


def glass_ceiling(g, x, y, w, k=0.0, t=0.0):
    """เพดานกระจก แตกตาม k"""
    c = g.c
    if k < 0.5:
        _rr(c, x - w / 2, y - 20, w, 40, 6)
        c.set_source_rgba(0.75, 0.88, 0.98, 0.7)
        c.fill_preserve()
        c.set_source_rgba(*INK)
        c.set_line_width(5)
        c.stroke()
        if k > 0.1:
            for i in range(5):
                a = i * 1.25
                g.line([(x, y), (x + 120 * math.cos(a) * k * 2, y + 30 * math.sin(a))], 4, INK, amp=0)
    else:
        u = (k - 0.5) * 2
        for i in range(8):
            px = x - w / 2 + (i + 0.5) * w / 8 + (i - 3.5) * 30 * u
            py = y + 200 * u * u + 20 * math.sin(i * 2)
            with g.at(px, py, 1, (i - 3.5) * 25 * u):
                g.poly([(-40, -20), (40, -15), (30, 20), (-35, 18)], (0.75, 0.88, 0.98, 0.8), 4, amp=0)


def balance(g, x, y, sc=1.0, tilt=0.0, t=0.0):
    """ตาชั่งรายได้ ชาย-หญิง"""
    c = g.c
    with g.at(x, y, sc):
        g.line([(0, 0), (0, -420)], 12, INK, amp=0)
        _rr(c, -100, -10, 200, 30, 8)
        _shade(c, GOLD, 5, 0.2)
        a = math.radians(-12 * tilt)
        dx, dy = 300 * math.cos(a), 300 * math.sin(a)
        g.line([(-dx, -420 - dy), (dx, -420 + dy)], 10, GOLD2, amp=0)
        g.circle(0, -420, 16, GOLD, 4)
        for sx, txt in ((-1, "♂"), (1, "♀")):
            px, py = sx * dx, -420 + sx * dy
            g.line([(px, py), (px - 80, py + 150)], 3, INK, amp=0)
            g.line([(px, py), (px + 80, py + 150)], 3, INK, amp=0)
            c.new_path()
            c.arc(px, py + 150, 90, 0, math.pi)
            c.close_path()
            _shade(c, GOLD, 5, 0.2)
            g.text("$20M", px, py + 190, 34, "kanit", INK)
