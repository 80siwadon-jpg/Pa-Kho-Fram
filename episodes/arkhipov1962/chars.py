"""ตัวละครและพร็อพ: วันเสาร์ทมิฬ 27 ต.ค. 1962 — U-2 ถูกยิงตก + เรือดำน้ำ B-59 / วาซิลี อาร์คีปอฟ
ไม่แสดงภาพการยิงโดน/ระเบิดนิวเคลียร์: ใช้จอเรดาร์ ควัน นาฬิกาวันสิ้นโลก แสงไฟเตือนแทน
ใช้ตัวละคร/พร็อพบางส่วนจากตอน cuba1962"""
import importlib.util
import math
import os

import cairo

from gfx import GOLD, GOLD2, GREY, INK, NAVY, RED, WHITE, hexc
from people import Look, _rr, _shade, _smooth_path, _stroke

_spec = importlib.util.spec_from_file_location(
    "cuba_chars", os.path.join(os.path.dirname(__file__), "..", "cuba1962", "chars.py"))
cuba = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cuba)
JFK, KHRUSHCHEV = cuba.JFK, cuba.KHRUSHCHEV
warship, clock_face, dove, red_phone = cuba.warship, cuba.clock_face, cuba.dove, cuba.red_phone

SEA = hexc("#bcd8ec")
DEEP = hexc("#1f3550")
US_BLUE = hexc("#3f6496")
SOV_RED = hexc("#b8473a")
HULL = hexc("#3a4048")
NAVY_BLK = hexc("#1d2230")

# วาซิลี อาร์คีปอฟ (36): ผมดำหวีเสยเรียบ หน้าเหลี่ยม คิ้วเข้ม สงบนิ่ง เครื่องแบบทหารเรือโซเวียตสีดำ + หมวกนายทหารเรือ
ARKHIPOV = Look(hair="slick", hair_col=hexc("#2b2622"), suit=NAVY_BLK, tie=INK, w=58, jaw=0.75, nose=1.05, brow=1.15,
                age=0.3, hat="peaked", hat_trim=NAVY_BLK, epaulettes=True)
# วาเลนติน ซาวิตสกี กัปตันเรือ B-59: ร่างหนา หน้ากลม คิ้วดก (เสื้อกล้ามเพราะร้อนจัด)
SAVITSKY = Look(hair="crew", hair_col=hexc("#3a2f28"), outfit="tee", suit=hexc("#e9e4d8"), pants=NAVY_BLK, w=62,
                jaw=0.8, jowls=0.3, brow=1.35, age=0.5, build=1.2)
# นายทหารการเมือง (คนที่ 2)
POLIT = Look(hair="part", hair_col=hexc("#5a4632"), outfit="tee", suit=hexc("#e9e4d8"), pants=NAVY_BLK, w=57,
             jaw=0.5, brow=1.0, age=0.4, glasses="thin")
CREW = Look(hair="buzz", hair_col=hexc("#5a4632"), outfit="stripe", pants=NAVY_BLK, w=56, age=0.1)
# นายพลทำเนียบขาว (เครื่องแบบกองทัพอากาศสีฟ้าเทา)
GENERALS = [
    Look(hair="part", hair_col=hexc("#2b2622"), suit=hexc("#5a6f8a"), shirt=hexc("#c9d4e0"), tie=INK, w=62, jaw=0.9,
         jowls=0.4, age=0.6, hat="peaked", hat_trim=hexc("#3a4a63"), stars=3),
    Look(hair="crew", hair_col=hexc("#9a948a"), suit=hexc("#4f5a3a"), tie=INK, w=60, jaw=0.7, age=0.7, stars=2),
]


def underwater(g, y0, t, y1=1420):
    """ใต้ทะเล: ไล่จากฟ้าอ่อนลงน้ำเงินเข้ม + ฟองอากาศ"""
    c = g.c
    gr = cairo.LinearGradient(0, y0, 0, y1)
    gr.add_color_stop_rgba(0, *SEA[:3], 1)
    gr.add_color_stop_rgba(1, 0.32, 0.45, 0.6, 1)
    c.rectangle(-500, y0, 2100, y1 - y0)
    c.set_source(gr)
    c.fill()
    _stroke(c, [(-500, y0), (1600, y0)], 6, INK, smooth=False)
    for i in range(10):
        u = (t * 0.25 + i * 0.137) % 1
        x = 160 + (i * 97) % 760 + 12 * math.sin(t * 2 + i)
        g.circle(x, y1 - (y1 - y0) * u, 8 + (i % 3) * 4, (1, 1, 1, 0.5 * (1 - u)), 2,
                 stroke=(1, 1, 1, 0.7 * (1 - u)))


def u2(g, x, y, sc=1.0, rot=0.0):
    """เครื่องบินสอดแนม U-2 มองด้านบน: ปีกยาวเรียวแบบเครื่องร่อน สีดำ"""
    c = g.c
    with g.at(x, y, sc, rot):
        _smooth_path(c, [(-20, -10), (-420, 0), (-420, 16), (-20, 30), (20, 30), (420, 16), (420, 0), (20, -10)])
        _shade(c, hexc("#2b2f3a"), 5, 0.2)
        _rr(c, -26, -190, 52, 400, 26)
        _shade(c, hexc("#3a3f48"), 5, 0.25)
        _smooth_path(c, [(-10, 170), (-110, 220), (-110, 236), (0, 222), (110, 236), (110, 220), (10, 170)])
        _shade(c, hexc("#2b2f3a"), 4, 0.2)
        _smooth_path(c, [(-12, -160), (12, -160), (8, -120), (-8, -120)])
        _shade(c, hexc("#9ad0f5"), 3, 0)


def smoke_trail(g, pts, t, k=1.0):
    """ควันเป็นทาง (แทนการระเบิด)"""
    n = len(pts)
    for i, (px, py) in enumerate(pts[:max(1, int(n * k))]):
        r = 18 + i * 3 + 4 * math.sin(t * 3 + i)
        g.circle(px, py, r, (0.55, 0.57, 0.6, 0.55), 0)


def radar(g, x, y, r, t=0.0, blip=1.0, lost=0.0):
    """จอเรดาร์: เส้นกวาด + จุดเครื่องบิน (lost = สัญญาณหาย)"""
    c = g.c
    c.new_path()
    c.arc(x, y, r, 0, 2 * math.pi)
    _shade(c, hexc("#0f2a1c"), 8, 0)
    for k in (0.33, 0.66):
        c.new_path()
        c.arc(x, y, r * k, 0, 2 * math.pi)
        c.set_source_rgba(0.3, 0.9, 0.5, 0.4)
        c.set_line_width(3)
        c.stroke()
    a = t * 2.2
    c.save()
    c.new_path()
    c.move_to(x, y)
    c.arc(x, y, r - 6, a - 0.6, a)
    c.close_path()
    c.set_source_rgba(0.3, 0.9, 0.5, 0.35)
    c.fill()
    c.restore()
    _stroke(c, [(x, y), (x + (r - 6) * math.cos(a), y + (r - 6) * math.sin(a))], 4, (0.4, 1, 0.6, 1), smooth=False)
    if blip > 0:
        bx, by = x + r * 0.4, y - r * 0.3
        if lost <= 0:
            g.circle(bx, by, 12, (0.5, 1, 0.6, 1), 0)
        else:
            g.circle(bx, by, 12 + 40 * lost, (1, 0.35, 0.3, max(0, 1 - lost)), 0)
            if lost > 0.6:
                g.label("?", bx, by, 70, color=RED)


def helmet(g, x, y, sc=1.0, rot=0.0):
    """หมวกนักบิน (สัญลักษณ์การสูญเสีย)"""
    c = g.c
    with g.at(x, y, sc, rot):
        _smooth_path(c, [(-110, 40), (-120, -40), (-60, -110), (60, -110), (120, -40), (110, 40)])
        _shade(c, hexc("#d9dde3"), 6, 0.3)
        _rr(c, -90, -40, 180, 70, 30)
        _shade(c, hexc("#3a3f48"), 5, 0.1)
        _rr(c, -120, 30, 240, 26, 10)
        _shade(c, hexc("#7b8794"), 4, 0)


def ribbon(g, x, y, sc=1.0):
    """โบว์ไว้ทุกข์สีดำ"""
    c = g.c
    with g.at(x, y, sc):
        for sx in (-1, 1):
            _smooth_path(c, [(0, 0), (sx * 40, 110), (sx * 18, 104), (sx * 6, 130), (sx * -10, 20)])
            _shade(c, INK, 3, 0)
            _smooth_path(c, [(0, 0), (sx * 70, -40), (sx * 80, 20)])
            _shade(c, INK, 3, 0)
        g.circle(0, 0, 18, INK, 0)


def submarine(g, x, y, sc=1.0, t=0.0, flip=False, label="B-59", tilt=0.0):
    """เรือดำน้ำดีเซลโซเวียตชั้น Foxtrot มองด้านข้าง"""
    c = g.c
    with g.at(x, y + 6 * math.sin(t * 1.2), sc, tilt + 1.2 * math.sin(t * 0.9), sx=-sc if flip else sc, sy=sc):
        c.new_path()
        c.move_to(-380, 0)
        c.curve_to(-380, -40, -300, -60, -200, -60)
        c.line_to(260, -60)
        c.curve_to(360, -60, 400, -20, 400, 0)
        c.curve_to(400, 30, 340, 50, 260, 50)
        c.line_to(-200, 50)
        c.curve_to(-300, 50, -380, 30, -380, 0)
        c.close_path()
        _shade(c, HULL, 6, 0.3, horiz=False)
        _smooth_path(c, [(-20, -60), (0, -150), (130, -150), (160, -60)])   # หอบังคับการ
        _shade(c, hexc("#4a5058"), 6, 0.25)
        g.line([(60, -150), (60, -200)], 6, INK, amp=0)
        g.text(label, 75, -100, 34, "kanit", WHITE)
        _smooth_path(c, [(-380, 0), (-430, -50), (-440, 50)])   # หาง
        _shade(c, hexc("#4a5058"), 5, 0.2)
        a = t * 8
        for k in range(3):
            _stroke(c, [(-450, 0), (-450 + 6 * math.cos(a + k * 2.1), 40 * math.sin(a + k * 2.1))], 5, INK,
                    smooth=False)
        for i in range(6):
            g.circle(-250 + i * 80, 10, 6, hexc("#5a6068"), 2)


def depth_charge(g, x, y, sc=1.0, rot=0.0):
    """ระเบิดน้ำลึก (ถังทรงกระบอก)"""
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -40, -60, 80, 120, 14)
        _shade(c, hexc("#4f5a3a"), 5, 0.3)
        for yy in (-30, 30):
            _stroke(c, [(-40, yy), (40, yy)], 4, INK, smooth=False)


def shock_ring(g, x, y, k):
    """คลื่นสั่นสะเทือนใต้น้ำ (ไม่มีไฟระเบิด)"""
    if 0 < k < 1:
        for j in range(2):
            kk = min(1, k + j * 0.2)
            c = g.c
            c.new_path()
            c.arc(x, y, 40 + 220 * kk, 0, 2 * math.pi)
            c.set_source_rgba(1, 1, 1, 0.8 * (1 - kk))
            c.set_line_width(10)
            c.stroke()


def sub_room(g, t, heat=0.0, alarm=0.0):
    """ห้องในเรือดำน้ำ: ผนังเหล็ก ท่อ หลอดไฟ มาตรวัด — heat ทำให้แสงแดงอมส้ม"""
    c = g.c
    c.rectangle(-500, 140, 2100, 1130)
    c.set_source_rgba(*hexc("#c9cdd2")[:3], 1)
    c.fill()
    for i in range(4):
        _stroke(c, [(-500, 300 + i * 34), (1600, 300 + i * 34)], 14, hexc("#8a9096"), smooth=False)
    for xx in (120, 960):
        _stroke(c, [(xx, 140), (xx, 1270)], 22, hexc("#7b8794"), smooth=False)
        for yy in range(200, 1270, 160):
            g.circle(xx, yy, 9, hexc("#5a6068"), 3)
    if heat > 0:
        rg = cairo.RadialGradient(540, 700, 80, 540, 700, 900)
        rg.add_color_stop_rgba(0, 1, 0.45, 0.2, 0.0)
        rg.add_color_stop_rgba(1, 1, 0.35, 0.15, 0.35 * heat)
        c.set_source(rg)
        c.rectangle(-500, 140, 2100, 1130)
        c.fill()
    if alarm > 0:
        a = 0.5 + 0.5 * math.sin(t * 9)
        g.circle(540, 470, 34, (1, 0.2 * a, 0.2 * a, 1), 5)
        c.rectangle(-500, 140, 2100, 1130)
        c.set_source_rgba(1, 0.1, 0.1, 0.12 * a * alarm)
        c.fill()


def gauge(g, x, y, r, val, col=RED, label=""):
    """มาตรวัดเข็ม val 0..1"""
    c = g.c
    with g.at(x, y):
        g.circle(0, 0, r, WHITE, 6)
        c.new_path()
        c.arc(0, 0, r - 14, math.radians(135 + 270 * 0.75), math.radians(405))
        c.set_source_rgba(*RED[:3], 0.6)
        c.set_line_width(10)
        c.stroke()
        a = math.radians(135 + 270 * val)
        g.line([(0, 0), ((r - 18) * math.cos(a), (r - 18) * math.sin(a))], 7, col, amp=0)
        g.circle(0, 0, 10, INK, 0)
        if label:
            g.label(label, 0, r + 44, 40, color=INK)


def thermometer(g, x, y, sc=1.0, val=0.5):
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -36, -320, 72, 330, 36)
        _shade(c, WHITE, 6, 0.1)
        g.circle(0, 40, 60, RED, 6)
        h = 300 * val
        _rr(c, -16, 20 - h, 32, h + 10, 16)
        c.set_source_rgba(*RED)
        c.fill()
        for i in range(6):
            _stroke(c, [(36, -280 + i * 50), (56, -280 + i * 50)], 4, INK, smooth=False)


def battery(g, x, y, sc=1.0, level=1.0, t=0.0):
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -110, -60, 220, 120, 16)
        _shade(c, WHITE, 6, 0)
        _rr(c, 110, -24, 20, 48, 6)
        _shade(c, INK, 0, 0)
        col = RED if level < 0.3 else GOLD
        a = 1.0 if level > 0.3 else 0.5 + 0.5 * math.sin(t * 8)
        _rr(c, -96, -46, 192 * level, 92, 10)
        c.set_source_rgba(*col[:3], a)
        c.fill()


def radio(g, x, y, sc=1.0, t=0.0):
    """วิทยุสื่อสาร — ไม่มีสัญญาณ"""
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -170, -110, 340, 220, 18)
        _shade(c, hexc("#5a6048"), 6, 0.25)
        _rr(c, -140, -80, 180, 90, 8)
        _shade(c, hexc("#1b2a1c"), 4, 0)
        for i in range(18):
            xx = -132 + i * 10
            yy = -35 + 18 * math.sin(i * 1.7 + t * 23) * (0.5 + 0.5 * math.sin(t * 7 + i))
            g.line([(xx, -35), (xx, yy)], 3, (0.4, 1, 0.5, 0.8), amp=0)
        for i in range(2):
            g.circle(100, -50 + i * 80, 26, hexc("#2b2f3a"), 4)
        g.line([(120, -110), (170, -230)], 6, INK, amp=0)


def torpedo(g, x, y, sc=1.0, rot=0.0, glow=0.0):
    """ตอร์ปิโดหัวรบนิวเคลียร์ (สัญลักษณ์รังสี)"""
    c = g.c
    with g.at(x, y, sc, rot):
        _smooth_path(c, [(-300, -40), (220, -40), (300, 0), (220, 40), (-300, 40)])
        _shade(c, hexc("#7b8794"), 6, 0.3, horiz=False)
        _rr(c, 60, -40, 120, 80, 4)
        _shade(c, hexc("#f2c230"), 4, 0.1)
        with g.at(120, 0, 0.3):
            trefoil(g, 0, 0, 100)
        for sy in (-1, 1):
            _smooth_path(c, [(-280, 0), (-330, sy * 70), (-300, sy * 70), (-250, 0)])
            _shade(c, hexc("#5a6068"), 4, 0.1)
        if glow > 0:
            g.circle(120, 0, 70 + 10 * glow, (1, 0.85, 0.2, 0.25 * glow), 0)


def trefoil(g, x, y, r, col=INK):
    c = g.c
    for i in range(3):
        a0 = math.radians(-90 + i * 120 - 30)
        a1 = math.radians(-90 + i * 120 + 30)
        c.new_path()
        c.arc(x, y, r * 0.95, a0, a1)
        c.arc_negative(x, y, r * 0.28, a1, a0)
        c.close_path()
        c.set_source_rgba(*col)
        c.fill()
    g.circle(x, y, r * 0.18, col, 0)


def fire_button(g, x, y, sc=1.0, cover=0.0, press=0.0, t=0.0):
    """ปุ่มยิงสีแดง + ฝาครอบ (cover 0 = ปิด, 1 = เปิด)"""
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -170, -40, 340, 120, 20)
        _shade(c, hexc("#4a4d55"), 6, 0.25)
        for i in range(5):
            _stroke(c, [(-160 + i * 70, -40), (-130 + i * 70, 80)], 12, hexc("#f2c230"), smooth=False)
        _rr(c, -170, -40, 340, 120, 20)
        c.set_source_rgba(*INK)
        c.set_line_width(6)
        c.stroke()
        c.save()
        c.translate(0, -40 + 12 * press)
        c.scale(1, 0.5)
        c.new_path()
        c.arc(0, 0, 110, math.pi, 2 * math.pi)
        c.close_path()
        c.restore()
        _shade(c, RED, 6, 0.3)
        with g.at(-120, -60, 1, -110 * cover):
            _rr(c, 0, -14, 240, 28, 10)
            c.set_source_rgba(0.75, 0.85, 0.95, 0.55)
            c.fill_preserve()
            c.set_source_rgba(*INK)
            c.set_line_width(4)
            c.stroke()


def vote_card(g, x, y, sc=1.0, rot=0.0, ok=True, name="", k=1.0):
    """การ์ดลงความเห็น: ✓ อนุมัติ / ✗ ไม่อนุมัติ"""
    if k < 0.02:
        return
    c = g.c
    col = hexc("#3c8d4f") if ok else RED
    with g.at(x, y, sc * k, rot):
        _rr(c, -130, -170, 260, 340, 18)
        _shade(c, hexc("#f4eedf"), 6, 0.1)
        for i in range(3):
            _stroke(c, [(-90, -120 + i * 30), (90, -120 + i * 30)], 3, GREY, 0.5, smooth=False)
        if ok:
            g.line([(-60, 20), (-15, 70), (70, -40)], 18, col, amp=0)
        else:
            g.line([(-60, -30), (60, 90)], 18, col, amp=0)
            g.line([(60, -30), (-60, 90)], 18, col, amp=0)
        if name:
            g.text(name, 0, 135, 30, "kanitsb", INK)


def sweat(g, x, y, t, n=3, sc=1.0):
    for i in range(n):
        u = (t * 0.8 + i / n) % 1
        with g.at(x + (i - 1) * 40 * sc, y + 60 * u * sc, sc):
            g.poly([(0, -24), (14, 4), (0, 16), (-14, 4)], (0.55, 0.8, 1, 1 - u), 3, amp=0, smooth=True)


def no_sign(g, x, y, sc=1.0, rot=0.0, t=0.0):
    """ป้าย "ไม่!" ในวงกลมห้าม"""
    with g.at(x, y, sc, rot):
        g.circle(0, 0, 150, WHITE, 0)
        g.c.new_path()
        g.c.arc(0, 0, 150, 0, 2 * math.pi)
        g.c.set_source_rgba(*RED)
        g.c.set_line_width(26)
        g.c.stroke()
        g.text("ไม่!", 0, 0, 110, "kanit", RED)


def globe(g, x, y, r, t=0.0, dim=0.0):
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
    if dim > 0:
        c.rectangle(x - r, y - r, 2 * r, 2 * r)
        c.set_source_rgba(0.1, 0.1, 0.15, 0.5 * dim)
        c.fill()
    c.restore()
    c.new_path()
    c.arc(x, y, r, 0, 2 * math.pi)
    c.set_source_rgba(*INK)
    c.set_line_width(6)
    c.stroke()


def calendar(g, x, y, sc=1.0, day="27", month="ต.ค. 1962", wd="เสาร์", rot=0.0, col=INK):
    with g.at(x, y, sc, rot):
        g.rrect(-200, -190, 400, 380, 30, WHITE, 8)
        g.rrect(-200, -190, 400, 100, 30, col, 8)
        g.text(month, 0, -140, 48, "kanit", WHITE)
        g.text(day, 0, 20, 170, "kanit", INK)
        g.text(wd, 0, 140, 46, "kanitsb", GREY)
