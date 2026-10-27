"""ตัวละครและพร็อพ: วันเกิดวิโนนา ไรเดอร์ (29 ต.ค. 1971)
ไม่ใช้หน้าตา/โปสเตอร์ตัวละครลิขสิทธิ์จริง (Beetlejuice/Stranger Things) — วาดเป็นวิโนนาในชุดสื่อถึงบทแทน"""
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
_jr = _load("roberts1967")
golden_statue, film_strip, heart, candle, siren = (_ph.golden_statue, _ph.film_strip, _ph.heart, _ph.candle,
                                                   _ph.siren)
spotlight, tear_drops = _kp.spotlight, _kp.tear_drops
hollywood = _kp.hollywood

GOTH = hexc("#2b2630")
RAVEN = hexc("#1b1714")

# วิโนนา ไรเดอร์: ผมดำสั้นหน้าม้า/ประบ่า ตาโตกลม หน้าเล็ก ผิวขาว ชุดดำสายกอธิก
WINONA = Look(hair="long", hair_col=RAVEN, outfit="dress", suit=GOTH, w=52, jaw=0.25, nose=0.85, brow=0.95, age=0.05,
              height=0.92)
WINONA_KID = Look(hair="long", hair_col=RAVEN, outfit="dress", suit=hexc("#8a6a4a"), w=52, age=0.0, height=0.6,
                  headsc=1.45)
# ช่วงคัมแบ็ก: แม่ยุค 80s ผมสั้นยุ่ง เสื้อเชิ้ตลายสก็อต
JOYCE = Look(hair="long", hair_col=hexc("#3a2a1e"), outfit="flannel", suit=hexc("#8a5a3a"), pants=hexc("#3a4a6a"),
             w=52, jaw=0.25, age=0.4, height=0.92)
WINONA_90S = Look(hair="long", hair_col=RAVEN, outfit="tee", suit=hexc("#3a3f48"), pants=hexc("#2b2f3a"), w=52,
                  jaw=0.25, age=0.05, height=0.92)
BURTON = Look(hair="afro", hair_col=RAVEN, suit=hexc("#1d1d21"), tie=hexc("#1d1d21"), w=56, age=0.3,
              glasses="shades")
DEPP = Look(hair="long", hair_col=hexc("#2b2622"), outfit="tee", suit=hexc("#1d1d21"), pants=hexc("#3a3a40"), w=55,
            jaw=0.5, age=0.1, facial="goatee")
PAPS = [
    Look(hair="part", hair_col=hexc("#3a2f28"), suit=hexc("#3a3f48"), tie=hexc("#7a2e2e"), w=58, age=0.4),
    Look(hair="crew", hair_col=hexc("#8a6a42"), outfit="hoodie", suit=hexc("#5a6a4a"), pants=hexc("#3a3a40"), w=57,
         age=0.3),
    Look(hair="bun", hair_col=hexc("#8a5a2a"), outfit="dress", suit=hexc("#5a3a5a"), w=54, age=0.3, height=0.93),
]
KIDS = [
    Look(hair="short", hair_col=hexc("#8a6a42"), outfit="tee", suit=hexc("#d76b5a"), pants=hexc("#3a4a6a"), w=54,
         height=0.6, headsc=1.45),
    Look(hair="bun", hair_col=hexc("#c99a52"), outfit="dress", suit=hexc("#e3a92b"), w=54, height=0.58, headsc=1.45),
]


def camera_flash(g, x, y, sc=1.0, t=0.0, phase=0.0):
    """กล้องถ่ายรูปแฟลชวาบ (นักข่าวแท็บลอยด์)"""
    c = g.c
    with g.at(x, y, sc, 6 * math.sin(t * 2 + phase)):
        _rr(c, -90, -55, 180, 110, 14)
        _shade(c, hexc("#2b2f3a"), 5, 0.2)
        g.circle(10, 0, 36, hexc("#c9ced6"), 5)
        g.circle(10, 0, 18, INK, 0)
        _rr(c, -80, -80, 50, 26, 6)
        _shade(c, hexc("#c9ced6"), 4, 0)
    if math.sin(t * 7 + phase * 3) > 0.7:
        g.star(x - 55 * sc, y - 95 * sc, 60 * sc, (1, 1, 0.85, 0.9), 0, pts=8, inner=0.35)


def tabloid(g, x, y, sc=1.0, rot=0.0, head="SHOPLIFT!", sub="STAR SCANDAL"):
    with g.at(x, y, sc, rot):
        g.rrect(-260, -340, 520, 680, 6, hexc("#f4efe2"), 6)
        g.rrect(-260, -340, 520, 110, 6, RED, 0)
        g.text("TABLOID", 0, -285, 56, "kanit", WHITE)
        g.text(head, 0, -170, 66, "kanit", RED)
        g.text(sub, 0, -100, 34, "kanitsb", INK)
        g.rrect(-200, -50, 180, 220, 4, hexc("#c9c2b2"), 4)
        for i in range(6):
            g.line([(10, -40 + i * 40), (220, -40 + i * 40)], 4, GREY, amp=0)
        g.text("?!", -110, 60, 90, "kanit", RED)


def shopping_bag(g, x, y, sc=1.0, rot=0.0):
    c = g.c
    with g.at(x, y, sc, rot):
        _smooth_path(c, [(-110, 0), (-90, -230), (90, -230), (110, 0)])
        _shade(c, hexc("#e8dcc0"), 6, 0.2)
        g.arc(0, -230, 50, 180, 360, 8, INK)
        g.text("$", 0, -110, 70, "kanit", GOLD)


def cuffs(g, x, y, sc=1.0, rot=0.0):
    c = g.c
    with g.at(x, y, sc, rot):
        for sx in (-1, 1):
            c.new_path()
            c.arc(sx * 70, 0, 50, 0, 2 * math.pi)
            c.set_source_rgba(*GREY)
            c.set_line_width(16)
            c.stroke()
        for i in range(3):
            g.circle(-20 + i * 20, -40, 10, GREY, 3)


def bulbs_wall(g, x, y, w, t=0.0, letters="RIGHT HERE"):
    """ผนังบ้านไฟประดับ + ตัวอักษร (ภาพจำแม่ตามหาลูก — ไม่ใช่ฉากจริงของซีรีส์)"""
    c = g.c
    with g.at(x, y):
        _rr(c, -w / 2, -420, w, 420, 4)
        _shade(c, hexc("#e8d6b0"), 6, 0.15)
        for k in range(4):
            _stroke(c, [(-w / 2, -380 + k * 100), (w / 2, -380 + k * 100)], 3, hexc("#c9b083"), 0.6, smooth=False)
        cols = [(1, 0.3, 0.3), (0.3, 0.6, 1), (1, 0.85, 0.3), (0.4, 0.9, 0.5)]
        n = 12
        for i in range(n):
            px = -w / 2 + 40 + i * (w - 80) / (n - 1)
            py = -360 + 20 * math.sin(i * 0.9)
            on = math.sin(t * 5 + i * 1.7) > -0.2
            col = cols[i % 4]
            g.circle(px, py, 16, (*col, 1 if on else 0.3), 3)
            if on:
                g.circle(px, py, 30, (*col, 0.25), 0)
        _stroke(c, [(-w / 2 + 40, -360), (w / 2 - 40, -360)], 3, INK, 0.5)
        g.text(letters, 0, -200, 60, "kanit", INK)


def axe(g, x, y, sc=1.0, rot=0.0):
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -12, -300, 24, 320, 8)
        _shade(c, hexc("#8a5a3a"), 5, 0.2)
        _smooth_path(c, [(10, -300), (110, -330), (120, -220), (10, -240)])
        _shade(c, hexc("#c9ced6"), 5, 0.3)


def broken_wall(g, x, y, k=0.0):
    """รูกำแพงทลาย"""
    if k <= 0:
        return
    with g.at(x, y, k):
        g.blob(0, 0, 110, 90, hexc("#2b2630"), 6, seed=4)
        for i in range(6):
            a = i * 1.05
            g.poly([(80 * math.cos(a), 70 * math.sin(a)), (150 * math.cos(a + 0.2), 120 * math.sin(a + 0.2)),
                    (110 * math.cos(a + 0.4), 90 * math.sin(a + 0.4))], hexc("#e8d6b0"), 4, amp=0)


def tv_series(g, x, y, sc=1.0, t=0.0, label="SERIES"):
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -260, -170, 520, 330, 24)
        _shade(c, hexc("#2b2f3a"), 7, 0.2)
        _rr(c, -230, -140, 460, 270, 14)
        c.set_source_rgba(0.85, 0.15, 0.15, 0.9)
        c.fill()
        g.text(label, 0, -10, 56, "kanit", WHITE)
        _rr(c, -40, 160, 80, 40, 4)
        _shade(c, hexc("#3a3f48"), 4, 0)
    for i in range(3):
        u = (t * 1.2 + i / 3) % 1
        g.star(x + 300 * sc * math.cos(i * 2.1 + t), y - 200 * sc - 60 * u, 24, (*GOLD2[:3], 1 - u), 3)


def phoenix_rise(g, x, y, sc, t, k):
    return _ph.phoenix_bird(g, x, y, sc, t, k)
