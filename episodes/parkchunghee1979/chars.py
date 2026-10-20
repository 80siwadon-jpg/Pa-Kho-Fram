"""ตัวละครและพร็อพ: การลอบสังหารประธานาธิบดีพัก จ็อง-ฮี (26 ต.ค. 1979)
ไม่แสดงการยิง/บาดแผล: ใช้แสงวาบในความมืด เงาคน เก้าอี้ล้ม แก้วหก แทน"""
import math

import cairo

from gfx import GOLD, GOLD2, GREY, INK, NAVY, RED, WHITE, hexc
from people import Look, _rr, _shade, _smooth_path, _stroke

KSKIN = hexc("#e6be98")
NIGHT = hexc("#1c2236")

# พัก จ็อง-ฮี (61): ผอม ผมดำหวีเรียบแสกข้าง โหนกแก้ม ตาเรียว สูทเทาลายทาง เนกไทลายขวาง
PARK = Look(hair="slick", hair_col=hexc("#1b1714"), suit=hexc("#4a4d55"), tie=hexc("#2b2f3a"), skin=KSKIN, w=53,
            jaw=0.3, nose=0.9, brow=0.9, age=0.6, build=0.88)
# คิม แจ-กยู ผอ. KCIA: ผมดำเรียบ หนวดบางเหนือปาก หน้ากว้าง สูทเข้ม
KIM = Look(hair="part", hair_col=hexc("#2b2622"), suit=hexc("#2b2f3a"), tie=hexc("#5a2e2e"), skin=KSKIN, w=58,
           jaw=0.65, jowls=0.2, nose=1.0, brow=1.0, age=0.55, facial="mustache")
KIM_GEN = Look(hair="part", hair_col=hexc("#2b2622"), suit=hexc("#b8a77a"), shirt=hexc("#d9cba3"),
               tie=hexc("#6b6448"), skin=KSKIN, w=58, jaw=0.65, jowls=0.2, age=0.4, facial="mustache",
               hat="peaked", hat_trim=hexc("#2b2f3a"))
# ชา จี-ชอล หัวหน้าหน่วยอารักขา: ร่างใหญ่ หน้ากลม ผมเกรียน สูทดำ
CHA = Look(hair="crew", hair_col=hexc("#1b1714"), suit=hexc("#1d1d21"), tie=hexc("#1d1d21"), skin=KSKIN, w=62,
           jaw=0.85, jowls=0.3, nose=1.0, brow=1.2, age=0.4, build=1.2)
# ชอน ดู-ฮวาน: ศีรษะล้าน เครื่องแบบทหาร
CHUN = Look(hair="bald", hair_col=hexc("#3a3632"), suit=hexc("#5f6a4a"), shirt=hexc("#c9bd92"), tie=hexc("#4a4630"),
            skin=KSKIN, w=58, jaw=0.6, age=0.45, hat="peaked", hat_trim=hexc("#4a5a3a"))
GUESTS = [
    Look(hair="part", hair_col=hexc("#2b2622"), suit=hexc("#3a3f48"), tie=hexc("#2b3f63"), skin=KSKIN, w=56, age=0.6,
         glasses="thin"),
]
PROTESTERS = [
    Look(hair="short", hair_col=hexc("#1b1714"), outfit="tee", suit=WHITE, pants=hexc("#3a4a6a"), skin=KSKIN, w=55,
         age=0.0, hat="headband", hat_trim=WHITE),
    Look(hair="bun", hair_col=hexc("#1b1714"), outfit="dress", suit=hexc("#5a6a8a"), skin=KSKIN, w=54, age=0.0,
         height=0.93),
    Look(hair="crew", hair_col=hexc("#1b1714"), outfit="tee", suit=hexc("#d9cba3"), pants=hexc("#2b2f3a"), skin=KSKIN,
         w=55, age=0.05, glasses="thick"),
]


def night(g, k=1.0, glow=0.0, x=540, y=760):
    """ห้องมืด (แผงกรมท่า) + แสงไฟโต๊ะ"""
    c = g.c
    if k <= 0:
        return
    c.save()
    c.rectangle(-500, 140, 2100, 1130)
    c.set_source_rgba(*NIGHT[:3], 0.82 * k)
    c.fill()
    if glow > 0:
        rg = cairo.RadialGradient(x, y, 40, x, y, 620)
        rg.add_color_stop_rgba(0, 1, 0.92, 0.7, 0.75 * glow)
        rg.add_color_stop_rgba(1, 1, 0.92, 0.7, 0)
        c.set_source(rg)
        c.rectangle(-500, 140, 2100, 1130)
        c.fill()
    c.restore()


def flash(g, x, y, r, k):
    """แสงวาบเสียงปืน (ไม่มีภาพการยิงโดน)"""
    if k <= 0 or k >= 1:
        return
    a = 1 - k
    g.star(x, y, r * (0.4 + 0.9 * k), (1, 0.85, 0.4, a), 0, pts=12, inner=0.45)
    g.star(x, y, r * 0.5 * (0.4 + 0.9 * k), (1, 1, 0.9, a), 0, pts=12, inner=0.5)


def table(g, x, y, w=820, t=0.0, bottles=True, spill=0.0):
    """โต๊ะอาหารเตี้ยแบบเกาหลี + ขวดเหล้า แก้ว จาน"""
    c = g.c
    with g.at(x, y):
        _rr(c, -w / 2, -40, w, 40, 10)
        _shade(c, hexc("#7a4a2a"), 6, 0.25)
        for sx in (-1, 1):
            _rr(c, sx * (w / 2 - 50) - 15, 0, 30, 90, 4)
            _shade(c, hexc("#5a3a22"), 5, 0.1)
        for i, px in enumerate((-260, -40, 180)):
            c.save()
            c.translate(px, -50)
            c.scale(1, 0.3)
            c.new_path()
            c.arc(0, 0, 60, 0, 2 * math.pi)
            c.restore()
            _shade(c, WHITE, 4, 0.1)
        if bottles:
            for i, bx in enumerate((-150, 70)):
                rot = 75 * spill if i == 1 else 0
                with g.at(bx, -40, 1, rot):
                    _smooth_path(c, [(-24, 0), (-24, -110), (-10, -140), (-10, -190), (10, -190), (10, -140), (24, -110),
                                     (24, 0)])
                    _shade(c, hexc("#4a6a3a") if i else hexc("#8a5a2a"), 5, 0.3)
                    _rr(c, -20, -90, 40, 50, 4)
                    _shade(c, hexc("#f4eedf"), 3, 0)
            for gx in (-300, 280):
                with g.at(gx, -40, 1, 80 * spill if gx > 0 else 0):
                    _smooth_path(c, [(-20, 0), (-26, -60), (26, -60), (20, 0)])
                    _shade(c, hexc("#e6eef4"), 4, 0.1)
                    _rr(c, -22, -40, 44, 30, 4)
                    _shade(c, hexc("#e8c45a"), 0, 0)


def chair(g, x, y, sc=1.0, rot=0.0):
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -60, -260, 30, 260, 6)
        _shade(c, hexc("#5a3a22"), 5, 0.2)
        _rr(c, -60, -110, 140, 26, 6)
        _shade(c, hexc("#7a4a2a"), 5, 0.2)
        _rr(c, 54, -100, 22, 100, 4)
        _shade(c, hexc("#5a3a22"), 4, 0.1)


def pistol(g, x, y, sc=1.0, rot=0.0, jam=0.0):
    """ปืนพก (ไอคอนเรียบ) + เครื่องหมาย ! ตอนขัดลำกล้อง"""
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -60, -40, 200, 50, 8)
        _shade(c, hexc("#4a4d55"), 5, 0.3)
        _smooth_path(c, [(-50, 0), (20, 0), (0, 120), (-60, 120)])
        _shade(c, hexc("#2b2f3a"), 5, 0.2)
        _stroke(c, [(20, 10), (40, 50), (10, 50)], 5, INK)
    if jam > 0:
        g.label("!", x + 160 * sc, y - 100 * sc, 110, color=RED, sc=jam, rot=10)


def house(g, x, y, sc=1.0, t=0.0, lit=1.0):
    """เซฟเฮาส์ทรงเกาหลี หลังคาโค้ง หน้าต่างมีไฟ"""
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -300, -280, 600, 280, 6)
        _shade(c, hexc("#e8dcc0"), 6, 0.2)
        _smooth_path(c, [(-400, -260), (-300, -330), (0, -380), (300, -330), (400, -260), (300, -290), (0, -320),
                         (-300, -290)])
        _shade(c, hexc("#3a3f48"), 6, 0.2)
        for k in range(3):
            _rr(c, -230 + k * 170, -220, 120, 120, 6)
            col = (1, 0.85, 0.45, 1) if lit > 0 else (0.3, 0.32, 0.4, 1)
            _shade(c, col, 4, 0)
            _stroke(c, [(-230 + k * 170 + 60, -220), (-230 + k * 170 + 60, -100)], 3, INK, smooth=False)


def placard(g, x, y, sc=1.0, rot=0.0, txt="ประชาธิปไตย"):
    with g.at(x, y, sc, rot):
        g.line([(0, 0), (0, -260)], 10, hexc("#8a6a42"), amp=0)
        g.rrect(-120, -380, 240, 140, 8, WHITE, 6)
        g.text(txt, 0, -310, 40, "kanit", RED)


def tank(g, x, y, sc=1.0, flip=False, t=0.0):
    c = g.c
    with g.at(x, y, sc, 0, sx=-sc if flip else sc, sy=sc):
        _rr(c, -260, -110, 520, 110, 50)
        _shade(c, hexc("#4a4d3a"), 6, 0.2)
        for k in range(6):
            g.circle(-200 + k * 80, -55, 30, hexc("#2b2b28"), 4)
        _rr(c, -200, -200, 380, 100, 16)
        _shade(c, hexc("#5f6a4a"), 6, 0.25)
        _rr(c, -60, -280, 200, 90, 30)
        _shade(c, hexc("#6a7552"), 6, 0.25)
        _rr(c, 130, -250, 260, 26, 6)
        _shade(c, hexc("#4a4d3a"), 5, 0.1)


def gavel(g, x, y, sc=1.0, rot=0.0):
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -10, -20, 20, 220, 8)
        _shade(c, hexc("#8a5a3a"), 5, 0.2)
        _rr(c, -80, -70, 160, 70, 20)
        _shade(c, hexc("#6a3a22"), 6, 0.25)


def candle(g, x, y, sc=1.0, t=0.0):
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -26, -200, 52, 200, 8)
        _shade(c, WHITE, 5, 0.15)
        g.poly([(0, -280 + 6 * math.sin(t * 7)), (20, -220), (0, -200), (-20, -220)], GOLD2, 3, amp=0, smooth=True)


def taegeuk(g, x, y, r, t=0.0):
    """ตราไทกึก (หยิน-หยางแดง/น้ำเงิน) — สัญลักษณ์เกาหลีใต้แบบเรียบง่าย"""
    c = g.c
    with g.at(x, y, 1, -20 + 4 * math.sin(t)):
        red, blue = (0.8, 0.12, 0.2), (0.0, 0.2, 0.55)
        for (a0, a1, col) in ((math.pi, 2 * math.pi, red), (0, math.pi, blue)):
            c.new_path()
            c.arc(0, 0, r, a0, a1)
            c.close_path()
            c.set_source_rgb(*col)
            c.fill()
        for (cx, col) in ((-r / 2, red), (r / 2, blue)):
            c.new_path()
            c.arc(cx, 0, r / 2, 0, 2 * math.pi)
            c.set_source_rgb(*col)
            c.fill()
        c.new_path()
        c.arc(0, 0, r, 0, 2 * math.pi)
        c.set_source_rgba(*INK[:3], 1)
        c.set_line_width(6)
        c.stroke()


def silhouette(g, x, y, sc=1.0, pose="down", a=1.0):
    """เงาคนดำทึบ (ใช้ในฉากความมืด)"""
    from people import person
    with g.silhouette(INK, a):
        person(g, x, y, KIM, sc, pose=pose, turn=-0.5, shadow=False)
