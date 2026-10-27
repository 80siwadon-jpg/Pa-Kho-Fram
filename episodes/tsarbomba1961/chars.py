"""ตัวละครและพร็อพ: ซาร์ บอมบา (30 ต.ค. 1961)
ไม่แสดงภาพคนบาดเจ็บ — ใช้แสงวาบ ลูกไฟ ควันดอกเห็ด วงคลื่นกระแทก บ้านร้างพังแทน"""
import importlib.util
import math
import os

import cairo

from gfx import GOLD, GOLD2, GREY, INK, NAVY, RED, WHITE, hexc
from people import Look, _rr, _shade, _smooth_path, _stroke


def _load(ep):
    spec = importlib.util.spec_from_file_location(f"{ep}_chars",
                                                  os.path.join(os.path.dirname(__file__), "..", ep, "chars.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


_cu = _load("cuba1962")
_ak = _load("arkhipov1962")
_bo = _load("boeing707_1958")
_wp = _load("westphalia1648")
JFK, KHRUSHCHEV = _cu.JFK, _cu.KHRUSHCHEV
time_bomb, dove, missile = _cu.time_bomb, _cu.dove, _cu.missile
globe, calendar = _ak.globe, _ak.calendar
house, cloud, crown = _bo.house, _bo.cloud, _bo.crown
treaty = _wp.treaty

SOV = hexc("#b8473a")
US = hexc("#3f6496")
ICE = hexc("#eef5fa")
ARCTIC = hexc("#bcd8ec")
BOMB = hexc("#5f6b5a")
FALLOUT = hexc("#9fbf5a")
SMOKE = (0.66, 0.62, 0.58)

SCIENTISTS = [
    Look(hair="part", hair_col=hexc("#3a2f28"), suit=hexc("#f4f6f8"), shirt=WHITE, tie=hexc("#2b2f3a"), w=57,
         age=0.35, glasses="thick"),
    Look(hair="short", hair_col=hexc("#8a8a8a"), suit=hexc("#f4f6f8"), shirt=WHITE, tie=hexc("#5a3a3a"), w=58,
         age=0.6, facial="mustache"),
]
PILOT = Look(hair="short", hair_col=hexc("#5a4632"), outfit="vest", suit=hexc("#6a5a3a"), shirt=hexc("#6a5a3a"),
             tie=hexc("#6a5a3a"), pants=hexc("#4a4a40"), w=58, jaw=0.6, age=0.3, hat="peaked",
             hat_trim=hexc("#3a3a30"))
GENERAL = Look(hair="short", hair_col=hexc("#8a8a8a"), suit=hexc("#5a6a4a"), tie=hexc("#3a3a30"), w=62, jaw=0.7,
               jowls=0.4, age=0.6, build=1.15, hat="peaked", hat_trim=SOV, stars=2)


def tsar(g, x, y, sc=1.0, rot=0.0):
    """ตัวระเบิด (มุมข้าง): อ้วนยาว หัวมน ครีบหาง — หัวไปทางขวา"""
    c = g.c
    with g.at(x, y, sc, rot):
        for sy in (-1, 1):   # ครีบหาง
            _smooth_path(c, [(-300, 0), (-380, sy * 120), (-420, sy * 120), (-380, 0)])
            _shade(c, hexc("#4a5446"), 5, 0.1)
        _rr(c, -420, -40, 60, 80, 10)
        _shade(c, hexc("#4a5446"), 5, 0.1)
        _smooth_path(c, [(-360, -80), (200, -100), (300, -80), (360, -30), (370, 0), (360, 30), (300, 80),
                         (200, 100), (-360, 80)])
        _shade(c, BOMB, 7, 0.35)
        for xx in (-200, 40):
            _stroke(c, [(xx, -96), (xx, 96)], 4, INK, 0.45, smooth=False)
        g.star(120, 0, 34, SOV, 4)


def bomber(g, x, y, sc=1.0, rot=0.0, t=0.0, bomb=1.0, flip=False):
    """ทูโพเลฟ ตู-95 สีขาวสะท้อนแสง (มุมข้าง หัวไปทางขวา) ใบพัดคู่ 4 เครื่อง ปีกลู่ — bomb 1 = ระเบิดโผล่ใต้ท้อง"""
    c = g.c
    with g.at(x, y, sc, rot, sx=-1 if flip else 1, sy=1):
        _smooth_path(c, [(-80, -20), (-260, 70), (-210, 80), (40, 10)])   # ปีกไกล
        _shade(c, hexc("#d9dee4"), 5, 0.2)
        _smooth_path(c, [(-430, -20), (-380, -150), (-330, -150), (-300, -30)])   # หางตั้ง
        _shade(c, hexc("#eef1f4"), 6, 0.2)
        _smooth_path(c, [(-440, -10), (-300, -40), (300, -40), (380, -20), (420, 10), (380, 30), (300, 40),
                         (-300, 30), (-440, 10)])
        _shade(c, hexc("#f4f6f8"), 7, 0.25)
        if bomb > 0:   # ระเบิดโผล่ใต้ท้อง (ปิดประตูไม่มิด)
            with g.at(-30, 40 + 30 * (1 - bomb), 0.42):
                tsar(g, 0, 0, 1)
        _smooth_path(c, [(-380, 0), (-470, -50), (-440, 10)])   # หางระดับ
        _shade(c, hexc("#e2e6ea"), 5, 0.1)
        for i in range(8):   # หน้าต่าง
            g.circle(-200 + i * 50, -10, 7, hexc("#8fb8de"), 2)
        _smooth_path(c, [(320, -34), (370, -26), (390, -6), (330, -10)])
        _shade(c, hexc("#8fb8de"), 4, 0)
        g.star(-370, -95, 22, SOV, 3)
        for ex, ey in ((-20, 50), (-150, 92)):   # เครื่องยนต์ + ใบพัดคู่
            _smooth_path(c, [(ex - 60, ey - 14), (ex + 60, ey - 18), (ex + 80, ey), (ex + 60, ey + 18),
                             (ex - 60, ey + 14)])
            _shade(c, hexc("#cfd5dc"), 5, 0.2)
            for k in range(2):
                s = math.sin(t * 40 + k * 1.3 + ex)
                c.save()
                c.translate(ex + 92 + k * 14, ey)
                c.scale(0.18, 1)
                c.new_path()
                c.arc(0, 0, 60, 0, 2 * math.pi)
                c.restore()
                c.set_source_rgba(0.3, 0.33, 0.38, 0.25 + 0.1 * s)
                c.fill()
        _smooth_path(c, [(60, 0), (-200, 120), (-150, 128), (130, 20)])   # ปีกใกล้ (ลู่หลัง)
        _shade(c, hexc("#e9ecf0"), 6, 0.2)


def parachute(g, x, y, sc=1.0, k=1.0, t=0.0):
    """ร่มชูชีพยักษ์ (โดมลายแถบ) แขวนที่ (x,y) จุดล่างสุดของสาย"""
    if k <= 0.02:
        return
    c = g.c
    sw = 0.08 * math.sin(t * 1.5)
    with g.at(x, y, 1, math.degrees(sw) * 0.5):
        with g.at(0, 0, sc * k):
            for i in range(7):
                _stroke(c, [(0, 0), (-260 + i * 87, -330)], 3, INK, 0.7, smooth=False)
            for i in range(6):
                x0 = -280 + i * 93.3
                _smooth_path(c, [(x0, -330), (x0 + 10, -420 + 30 * abs(i - 2.5) ** 1.2 * 0 - 20 * (1 - abs(i - 2.5) / 2.5)),
                                 (x0 + 47, -470 + 25 * abs(i - 2.5)), (x0 + 83, -420), (x0 + 93, -330),
                                 (x0 + 47, -350)])
                _shade(c, WHITE if i % 2 else hexc("#e8833a"), 5, 0.15)


def arctic(g, y, t=0.0, island=True, x0=-500, x1=1600):
    """ทะเลอาร์กติก + เกาะน้ำแข็ง/หิมะ (เกาะเซแวร์นี)"""
    c = g.c
    c.rectangle(x0, y, x1 - x0, 1500 - y)
    c.set_source_rgba(*ARCTIC)
    c.fill()
    for i in range(10):
        xx = x0 + ((i * 230 + t * 30) % (x1 - x0))
        _stroke(c, [(xx, y + 40 + (i % 3) * 50), (xx + 70, y + 40 + (i % 3) * 50)], 4, hexc("#8fb8de"), 0.8,
                smooth=False)
    if island:
        _smooth_path(c, [(x0, y + 10), (-100, y - 60), (150, y - 130), (380, y - 90), (560, y - 170),
                         (800, y - 80), (1000, y - 110), (x1, y - 40), (x1, y + 30), (x0, y + 30)])
        _shade(c, ICE, 6, 0.2)
        for xx, yy in ((150, y - 130), (560, y - 170), (1000, y - 110)):
            _stroke(c, [(xx - 60, yy + 40), (xx, yy + 10), (xx + 60, yy + 40)], 4, hexc("#a8c4d8"), 0.8)


def ice_floe(g, x, y, w, seed=0):
    g.poly([(x - w / 2, y), (x - w / 3, y - 18), (x + w / 3, y - 22), (x + w / 2, y - 4), (x + w / 3, y + 10),
            (x - w / 3, y + 10)], ICE, 4, seed=seed)


def fireball(g, x, y, r, t=0.0, k=1.0):
    """ลูกไฟ (ไล่สีขาว → เหลือง → ส้ม) ไม่มีเศษ"""
    if k <= 0 or r <= 1:
        return
    c = g.c
    rg = cairo.RadialGradient(x, y, 0, x, y, r * 1.5)
    rg.add_color_stop_rgba(0, 1, 1, 0.92, k)
    rg.add_color_stop_rgba(0.4, 1, 0.86, 0.4, k)
    rg.add_color_stop_rgba(0.66, 0.98, 0.55, 0.2, 0.9 * k)
    rg.add_color_stop_rgba(1, 0.98, 0.55, 0.2, 0)
    c.set_source(rg)
    c.arc(x, y, r * 1.5, 0, 2 * math.pi)
    c.fill()
    for i in range(14):
        a = i * 2 * math.pi / 14 + t * 0.3
        rr = r * (0.85 + 0.08 * math.sin(t * 3 + i * 1.7))
        g.circle(x + rr * math.cos(a), y + rr * math.sin(a), r * 0.22, (0.98, 0.62, 0.22, 0.55 * k), 0)


def mushroom(g, x, y, h, k=1.0, t=0.0, glow=1.0, w=1.0):
    """ควันดอกเห็ดยักษ์ฐานที่ (x,y) สูง h — k การก่อตัว 0..1"""
    if k <= 0.02:
        return
    hh = h * k
    cw = (0.32 + 0.12 * k) * h * w
    for i in range(10):   # ลำต้น
        u = i / 10
        yy = y - u * hh * 0.82
        rr = (0.11 * h + 0.03 * h * math.sin(t * 2 + i)) * w * (0.8 + 0.3 * (1 - u))
        g.circle(x + 6 * math.sin(i + t), yy, rr * (0.6 + 0.4 * k), (*SMOKE, 0.95), 0)
    for i in range(3):   # วงแหวนกลางลำต้น
        yy = y - hh * (0.45 + 0.08 * i)
        g.c.save()
        g.c.translate(x, yy)
        g.c.scale(1, 0.25)
        g.c.new_path()
        g.c.arc(0, 0, cw * (0.55 - 0.08 * i), 0, 2 * math.pi)
        g.c.restore()
        g.c.set_source_rgba(0.85, 0.85, 0.86, 0.7 * k)
        g.c.set_line_width(14)
        g.c.stroke()
    top = y - hh
    for i in range(14):   # หัวเห็ด
        a = i * 2 * math.pi / 14 + t * 0.15
        g.circle(x + cw * math.cos(a), top + 0.28 * cw * math.sin(a), cw * 0.42 + 8 * math.sin(t + i),
                 (0.6, 0.56, 0.52, 0.97), 0)
    g.circle(x, top - cw * 0.12, cw * 0.62, (0.68, 0.63, 0.58, 1), 0)
    if glow > 0:   # แสงไฟเรืองในหัวและฐาน
        rg = cairo.RadialGradient(x, top + cw * 0.1, 0, x, top + cw * 0.1, cw * 0.8)
        rg.add_color_stop_rgba(0, 1, 0.75, 0.35, 0.8 * glow)
        rg.add_color_stop_rgba(1, 1, 0.75, 0.35, 0)
        g.c.set_source(rg)
        g.c.arc(x, top + cw * 0.1, cw * 0.8, 0, 2 * math.pi)
        g.c.fill()
        for i in range(5):
            g.circle(x - 0.2 * h * w + i * 0.1 * h * w, y - 10, 0.06 * h + 6 * math.sin(t * 6 + i),
                     (0.98, 0.66, 0.23, 0.6 * glow), 0)


def everest(g, x, y, h, col=hexc("#9aa3ad")):
    c = g.c
    _smooth_path(c, [(x - h * 0.9, y), (x - h * 0.25, y - h * 0.7), (x, y - h), (x + h * 0.35, y - h * 0.6),
                     (x + h * 0.9, y)])
    _shade(c, col, 5, 0.25)
    _smooth_path(c, [(x - h * 0.25, y - h * 0.7), (x, y - h), (x + h * 0.2, y - h * 0.77), (x + h * 0.05, y - h * 0.72),
                     (x - h * 0.1, y - h * 0.78)])
    _shade(c, WHITE, 4, 0)


def shock_ring(g, x, y, r, k=1.0, col=(1, 0.75, 0.35), lw=10):
    if k <= 0 or r <= 1:
        return
    g.c.new_path()
    g.c.arc(x, y, r, 0, 2 * math.pi)
    g.c.set_source_rgba(*col[:3], k)
    g.c.set_line_width(lw)
    g.c.stroke()


def trefoil(g, x, y, r, col=hexc("#e3c13a"), rot=0.0):
    """สัญลักษณ์กัมมันตรังสี"""
    c = g.c
    with g.at(x, y, 1, rot):
        c.new_path()
        c.arc(0, 0, r, 0, 2 * math.pi)
        _shade(c, col, 5, 0)
        for i in range(3):
            a0 = math.radians(-90 + i * 120 - 30)
            a1 = math.radians(-90 + i * 120 + 30)
            c.new_path()
            c.arc(0, 0, r * 0.8, a0, a1)
            c.arc_negative(0, 0, r * 0.22, a1, a0)
            c.close_path()
            c.set_source_rgba(*INK)
            c.fill()
        c.new_path()
        c.arc(0, 0, r * 0.14, 0, 2 * math.pi)
        c.set_source_rgba(*INK)
        c.fill()


def fallout(g, x, y, s=1.0, t=0.0, k=1.0):
    """เมฆกัมมันตรังสีสีเขียวหม่น"""
    if k <= 0.02:
        return
    with g.at(x, y, s * k):
        for i in range(7):
            a = i * 0.9
            g.circle(160 * math.cos(a) * 0.9, 50 * math.sin(a) + 6 * math.sin(t * 2 + i), 90 + 10 * (i % 3),
                     (*FALLOUT[:3], 0.85), 0)
        trefoil(g, 0, 0, 60, rot=10 * math.sin(t))


def seismo(g, x, y, sc=1.0, t=0.0, amp=1.0):
    """เครื่องวัดแผ่นดินไหว: กระดาษ + เข็มเส้นกราฟ"""
    c = g.c
    with g.at(x, y, sc):
        g.rrect(-300, -170, 600, 340, 20, WHITE, 6)
        for i in range(5):
            _stroke(c, [(-280, -120 + i * 60), (280, -120 + i * 60)], 2, hexc("#c9d6e2"), 1, smooth=False)
        pts = []
        for i in range(120):
            xx = -280 + i * 4.7
            u = i / 120
            env = amp * math.exp(-((u - 0.55) * 6) ** 2) * 120
            pts.append((xx, env * math.sin(i * 1.3 + t * 8) + 3 * math.sin(i * 0.7)))
        _stroke(c, pts, 4, RED, 1, smooth=False)


def dial(g, x, y, sc=1.0, val=50, mx=100, label="เมกะตัน"):
    """มาตรวัดพลังระเบิด 0..mx"""
    c = g.c
    with g.at(x, y, sc):
        c.new_path()
        c.arc(0, 0, 240, math.pi, 2 * math.pi)
        c.close_path()
        _shade(c, WHITE, 7, 0.05)
        for i in range(5):
            a0 = math.pi + i * math.pi / 5
            c.new_path()
            c.arc(0, 0, 200, a0, a0 + math.pi / 5)
            c.set_source_rgba(*[(0.24, 0.55, 0.31), (0.54, 0.72, 0.29), (0.89, 0.76, 0.23), (0.89, 0.52, 0.23),
                                (0.75, 0.2, 0.2)][i], 1)
            c.set_line_width(40)
            c.stroke()
        a = math.pi + math.pi * min(1, val / mx)
        _stroke(c, [(0, 0), (170 * math.cos(a), 170 * math.sin(a))], 12, INK, 1, smooth=False)
        g.circle(0, 0, 20, INK, 0)
        g.text(f"{int(round(val))}", 0, -80, 80, "kanit", INK)
        g.text(label, 0, 40, 40, "kanitsb", GREY)


def flat_house(g, x, y, sc=1.0, crush=0.0, seed=0):
    """บ้านไม้ร้าง — crush 0..1 ถูกบดราบ (ไม่มีคน)"""
    if crush < 0.95:
        with g.at(x, y, sc, -6 * crush, sx=1, sy=1 - 0.85 * crush):
            house(g, 0, 0, 1, hexc("#d9c8a8"), hexc("#7a5a3a"))
    else:
        c = g.c
        with g.at(x, y, sc):
            for i in range(6):
                with g.at(-120 + i * 48, -14 - (i % 2) * 14, 1, (i * 37 + seed * 11) % 40 - 20):
                    _rr(c, -60, -10, 120, 20, 4)
                    _shade(c, hexc("#a8865a") if i % 2 else hexc("#7a5a3a"), 4, 0.2)


def atom(g, x, y, r, t=0.0, glow=1.0):
    """อะตอมเรืองแสง (พลังในมือมนุษย์)"""
    c = g.c
    if glow > 0:
        g.sunburst(x, y, r * 0.8, r * 1.6, 16, t * 10, 8, (1, 0.85, 0.4, 0.5 * glow))
    for i in range(3):
        c.save()
        c.translate(x, y)
        c.rotate(t * 0.6 + i * math.pi / 3)
        c.scale(1, 0.36)
        c.new_path()
        c.arc(0, 0, r, 0, 2 * math.pi)
        c.restore()
        c.set_source_rgba(*INK)
        c.set_line_width(6)
        c.stroke()
        a = t * 3 + i * 2.1
        ca, sa = math.cos(t * 0.6 + i * math.pi / 3), math.sin(t * 0.6 + i * math.pi / 3)
        ex, ey = r * math.cos(a), 0.36 * r * math.sin(a)
        g.circle(x + ex * ca - ey * sa, y + ex * sa + ey * ca, 14, hexc("#5aa0e0"), 4)
    g.circle(x, y, r * 0.22, GOLD2, 5)


def hands(g, x, y, sc=1.0, skin=hexc("#f0c8a0")):
    """สองมือประคองจากด้านล่าง"""
    c = g.c
    with g.at(x, y, sc):
        for sx in (-1, 1):
            _smooth_path(c, [(sx * 20, 40), (sx * 200, 20), (sx * 250, -40), (sx * 230, -70), (sx * 160, -40),
                             (sx * 60, -20), (sx * 20, 0)])
            _shade(c, skin, 6, 0.25)
            _smooth_path(c, [(sx * 120, 20), (sx * 200, 140), (sx * 60, 160)])
            _shade(c, skin, 6, 0.2)


def shield(g, x, y, sc=1.0, rot=0.0):
    c = g.c
    with g.at(x, y, sc, rot):
        _smooth_path(c, [(0, -160), (130, -110), (120, 30), (0, 160), (-120, 30), (-130, -110)])
        _shade(c, hexc("#5a8ab8"), 7, 0.3)
        _smooth_path(c, [(0, -110), (80, -80), (74, 20), (0, 110), (-74, 20), (-80, -80)])
        _shade(c, hexc("#8fb8de"), 4, 0.1)


def balance(g, x, y, sc=1.0, tilt=0.0):
    """ตาชั่ง: คืนตำแหน่งจานซ้าย/ขวา (พิกัดจอ)"""
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -14, -380, 28, 380, 6)
        _shade(c, hexc("#a8763e"), 5, 0.2)
        _rr(c, -120, -20, 240, 30, 8)
        _shade(c, hexc("#a8763e"), 5, 0.2)
        a = math.radians(tilt)
        for sx in (-1, 1):
            px, py = sx * 260 * math.cos(a), -380 + sx * 260 * math.sin(a)
            _stroke(c, [(0, -380), (px, py)], 10, INK, 1, smooth=False)
            _stroke(c, [(px, py), (px - 90, py + 180)], 3, INK, 1, smooth=False)
            _stroke(c, [(px, py), (px + 90, py + 180)], 3, INK, 1, smooth=False)
            _smooth_path(c, [(px - 120, py + 180), (px + 120, py + 180), (px + 80, py + 220), (px - 80, py + 220)])
            _shade(c, GOLD, 5, 0.2)
        g.circle(0, -380, 22, GOLD2, 5)
    a = math.radians(tilt)
    return [(x + sc * sx * 260 * math.cos(a), y + sc * (-380 + sx * 260 * math.sin(a) + 180)) for sx in (-1, 1)]
