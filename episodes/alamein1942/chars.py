"""ตัวละครและพร็อพ: ยุทธการเอล-อาลาเมนครั้งที่สอง 23 ต.ค. 1942
ไม่แสดงภาพความรุนแรง: การรบ = แสงวาบ ควัน ฝุ่น รถถังจอดนิ่ง ไม่มีคนบาดเจ็บ; ไม่ใช้สัญลักษณ์นาซี (ใช้กากบาทรถถังแทน)"""
import math

import cairo

from gfx import GOLD, GOLD2, GREY, INK, LGREY, NAVY, RED, WHITE, hexc
from people import Look, _rr, _shade, _smooth_path, _stroke

SAND = hexc("#ecd9a8")
SAND2 = hexc("#d9bf80")
NIGHT = hexc("#1f2740")
KHAKI = hexc("#b8a576")
DAK = hexc("#a69a6a")        # สีเครื่องแบบกองทัพแอฟริกาเยอรมัน
GERM = hexc("#8f8668")       # รถถังเยอรมันสีทราย-เทา
BRIT = hexc("#c2b38a")       # รถถังอังกฤษสีทราย
FIRE = hexc("#f2a93b")

# เออร์วิน รอมเมล (50): หมวกนายทหารมีแว่นกันฝุ่นคาด, กรามเหลี่ยม, ยิ้มมั่นใจ, ผ้าพันคอ, เครื่องแบบสีกากีเขียว
ROMMEL = Look(hair="short", hair_col=hexc("#5a4a3a"), suit=DAK, shirt=hexc("#c9bd92"), tie=hexc("#6b6448"),
              hat="peaked", hat_trim=hexc("#6b6650"), goggles=True, w=60, jaw=0.75, jowls=0.2, nose=1.05, brow=0.9,
              age=0.5, stars=1)
# เบอร์นาร์ด มอนต์โกเมอรี (54): หมวกเบเรต์ดำติดตรา 2 อัน, หน้าเรียวคม จมูกโด่ง หนวดเล็ก, เสื้อสเวตเตอร์กากี
MONTY = Look(hair="short", hair_col=hexc("#9a8a72"), suit=KHAKI, shirt=hexc("#d8cba3"), tie=hexc("#8a7a52"),
             hat="beret", hat_trim=hexc("#232120"), w=52, jaw=0.15, jowls=0.0, nose=1.35, brow=0.8, age=0.65,
             facial="mustache")
# วินสตัน เชอร์ชิลล์ (67): หัวล้าน แก้มย้อย ร่างท้วม หูกระต่ายลายจุด
CHURCHILL = Look(hair="bald", hair_col=hexc("#e2d6c2"), suit=hexc("#2f3036"), tie=hexc("#1f3a6b"), bowtie=True,
                 w=68, jaw=0.85, jowls=0.9, nose=0.9, brow=0.5, age=0.75, build=1.3, height=0.92)
TOMMY = [   # ทหารอังกฤษ
    Look(hair="short", outfit="tee", suit=KHAKI, pants=KHAKI, hat="brodie", hat_trim=hexc("#7a7350"), w=56, age=0.3),
    Look(hair="short", outfit="tee", suit=hexc("#c4b282"), pants=hexc("#a8976a"), hat="brodie",
         hat_trim=hexc("#7a7350"), w=56, age=0.2, facial="mustache"),
]


def night_sky(g, k=1.0, flash=0.0):
    """ท้องฟ้ากลางคืนในทะเลทราย (แผงกรมท่าจางลงหาขอบฟ้า) + แสงวาบจากปืนใหญ่"""
    c = g.c
    if k <= 0:
        return
    c.save()
    lg = cairo.LinearGradient(0, 160, 0, 1270)
    a = 0.95 * k * (1 - 0.8 * flash)
    lg.add_color_stop_rgba(0, *NIGHT[:3], a)
    lg.add_color_stop_rgba(0.85, *NIGHT[:3], a * 0.75)
    lg.add_color_stop_rgba(1, *NIGHT[:3], a * 0.3)
    c.set_source(lg)
    c.rectangle(-500, 140, 2100, 1130)
    c.fill()
    if flash > 0:
        rg = cairo.RadialGradient(540, 1260, 50, 540, 1260, 900)
        rg.add_color_stop_rgba(0, 1, 0.85, 0.5, 0.9 * flash)
        rg.add_color_stop_rgba(1, 1, 0.85, 0.5, 0)
        c.set_source(rg)
        c.rectangle(-500, 140, 2100, 1130)
        c.fill()
    c.restore()


def dunes(g, y, t=0.0, col=SAND):
    c = g.c
    c.new_path()
    c.move_to(-500, y + 60)
    for i in range(53):
        x = -500 + i * 40
        c.line_to(x, y + 40 * math.sin(x * 0.004 + 1) + 20 * math.sin(x * 0.011))
    c.line_to(1600, y + 160)
    c.line_to(-500, y + 160)
    c.close_path()
    _shade(c, col, 5, 0.15)


def tank(g, x, y, sc=1.0, side="de", t=0.0, flip=False, turret=0.0, fire=0.0, dead=0.0, move=True):
    """รถถังมองด้านข้าง หันขวา — x,y = พื้น; side de (กากบาทเยอรมัน) / uk; dead = ควันดำ ขยับไม่ได้"""
    c = g.c
    by = (2 * math.sin(t * 20)) if move and not dead else 0
    body = GERM if side == "de" else BRIT
    with g.at(x, y + by, sc, 0, sx=-sc if flip else sc, sy=sc):
        _rr(c, -230, -90, 460, 90, 44)   # สายพาน
        _shade(c, hexc("#3a3632"), 6, 0.2)
        for i in range(6):
            wx = -180 + i * 72
            with g.at(wx, -45, 1, -t * 300 * (0 if dead or not move else 1)):
                c.new_path()
                c.arc(0, 0, 28, 0, 2 * math.pi)
                _shade(c, hexc("#6a645a"), 4, 0.2)
                _stroke(c, [(-20, 0), (20, 0)], 3, INK, smooth=False)
        _smooth_path(c, [(-250, -90), (-240, -170), (220, -170), (260, -110), (240, -90)])
        _shade(c, body, 6, 0.3)
        with g.at(-10, -170, 1, turret):
            _rr(c, -110, -90, 200, 92, 20)
            _shade(c, body, 6, 0.25)
            _rr(c, 80, -60, 230, 26, 8)   # ปืน
            _shade(c, hexc("#5a5448"), 5, 0.2)
            if fire > 0:
                g.star(330, -47, 70 * fire, FIRE, 4, pts=8, inner=0.45)
        if side == "de":   # กากบาททหารเยอรมัน (Balkenkreuz)
            with g.at(-40, -130):
                _rr(c, -30, -10, 60, 20, 2)
                _shade(c, INK, 3, 0)
                _rr(c, -10, -30, 20, 60, 2)
                _shade(c, INK, 3, 0)
                _stroke(c, [(-26, -6), (26, -6)], 3, WHITE, 0.7, smooth=False)
        else:   # ลายพรางแถบแดง-ขาว-แดง ประจำกองทัพที่ 8
            for i, col in enumerate((RED, WHITE, RED)):
                _rr(c, -90 + i * 26, -150, 26, 40, 2)
                _shade(c, col, 3, 0)
        if dead > 0:
            for i in range(4):
                u = (t * 0.35 + i / 4) % 1
                g.circle(-40 + 30 * math.sin(i + t) - 60 * u, -290 - 260 * u, (30 + 60 * u), (0.25, 0.24, 0.24, 0.6 * dead * (1 - u)), 0)


def artillery(g, x, y, sc=1.0, t=0.0, fire=0.0):
    """ปืนใหญ่สนามยิงยามค่ำคืน — x,y = พื้น หันขวา"""
    c = g.c
    with g.at(x, y, sc):
        rec = -14 * fire
        with g.at(rec, -110, 1, -24):
            _rr(c, -60, -18, 260, 36, 10)
            _shade(c, hexc("#4f5a3a"), 5, 0.25)
            if fire > 0:
                g.star(220, 0, 90 * fire, FIRE, 4, pts=9, inner=0.4)
                g.star(220, 0, 45 * fire, hexc("#fff1c4"), 0, pts=9, inner=0.5)
        _smooth_path(c, [(-80, -150), (40, -150), (60, -70), (-90, -70)])
        _shade(c, hexc("#5d6a44"), 5, 0.25)
        _stroke(c, [(-60, -80), (-200, 0)], 14, INK, smooth=False)
        _stroke(c, [(-60, -80), (-200, 0)], 8, hexc("#5d6a44"), smooth=False)
        c.new_path()
        c.arc(0, -50, 52, 0, 2 * math.pi)
        _shade(c, hexc("#3a3632"), 5, 0.2)
        c.new_path()
        c.arc(0, -50, 18, 0, 2 * math.pi)
        _shade(c, hexc("#6a645a"), 3, 0)


def mine(g, x, y, sc=1.0, buried=0.4):
    """กับระเบิดรถถัง (จานแบน) ฝังครึ่งหนึ่งในทราย"""
    c = g.c
    with g.at(x, y, sc):
        c.save()
        c.rectangle(-80, -80, 160, 80 + 30 * (1 - buried))
        c.clip()
        c.save()
        c.scale(1, 0.42)
        c.new_path()
        c.arc(0, 0, 70, 0, 2 * math.pi)
        c.restore()
        _shade(c, hexc("#59604a"), 5, 0.3)
        _rr(c, -18, -46, 36, 22, 6)
        _shade(c, hexc("#3a3e32"), 4, 0.1)
        c.restore()
        _smooth_path(c, [(-90, 0), (-40, -14), (40, -14), (90, 0), (40, 10), (-40, 10)])
        _shade(c, SAND2, 3, 0.1)


def warn_sign(g, x, y, sc=1.0, rot=0.0, text="MINEN"):
    c = g.c
    with g.at(x, y, sc, rot):
        g.line([(0, 0), (0, -260)], 12, hexc("#6e4528"), amp=0)
        c.new_path()
        for p in [(0, -400), (100, -230), (-100, -230)]:
            c.line_to(*p)
        c.close_path()
        _shade(c, hexc("#f2c94c"), 6, 0.2)
        g.text("!", 0, -290, 80, "kanit", INK)
        _rr(c, -90, -220, 180, 50, 6)
        _shade(c, WHITE, 4, 0.1)
        g.text(text, 0, -195, 32, "kanit", RED)


def smoke(g, x, y, r, t, n=5, col=(0.55, 0.53, 0.5), a=0.7, seed=0):
    for i in range(n):
        u = (t * 0.3 + i / n + seed) % 1
        g.circle(x + r * 0.9 * math.sin(i * 2.3 + seed) + 40 * math.sin(t + i), y - r * 1.4 * u, r * (0.5 + 0.7 * u),
                 col + (a * (1 - u),), 0)


def blast(g, x, y, r, k):
    """แสงวาบระเบิด (ไม่มีเศษ/คน)"""
    if k <= 0 or k >= 1:
        return
    a = 1 - k
    g.star(x, y, r * (0.4 + 0.8 * k), (0.98, 0.66, 0.23, a), 0, pts=10, inner=0.5)
    g.star(x, y, r * 0.5 * (0.4 + 0.8 * k), (1, 0.95, 0.75, a), 0, pts=10, inner=0.55)


def jerrycan(g, x, y, sc=1.0, rot=0.0, level=1.0, col=None):
    """ถังน้ำมัน (เจอร์รีแคน) + ขีดน้ำมัน"""
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -90, -260, 180, 260, 14)
        _shade(c, col or hexc("#6b6a4a"), 6, 0.25)
        _stroke(c, [(-60, -240), (60, -20)], 6, INK, 0.25, smooth=False)
        _stroke(c, [(60, -240), (-60, -20)], 6, INK, 0.25, smooth=False)
        _rr(c, -50, -300, 60, 44, 8)
        _shade(c, hexc("#4a4a38"), 5, 0.1)
        _rr(c, 20, -300, 40, 30, 6)
        _shade(c, hexc("#3a3a30"), 4, 0.1)
        if level < 1:   # มาตรวัดน้ำมัน
            g.circle(0, -130, 66, WHITE, 5)
            g.arc(0, -130, 52, math.radians(200), math.radians(340), 5, GREY)
            a = math.radians(200 + 140 * level)
            g.line([(0, -130), (46 * math.cos(a), -130 + 46 * math.sin(a))], 7, RED if level < 0.2 else INK, amp=0)
            g.text("E", -40, -100, 26, "kanit", RED)
            g.text("F", 40, -100, 26, "kanit", INK)


def derrick(g, x, y, sc=1.0, t=0.0):
    """บ่อน้ำมัน (หอเจาะ) + ถังน้ำมัน"""
    c = g.c
    with g.at(x, y, sc):
        for sx in (-1, 1):
            g.line([(sx * 110, 0), (sx * 20, -460)], 10, INK, amp=0)
        for k in range(1, 5):
            yy = -k * 92
            ww = 110 - k * 18
            g.line([(-ww, yy), (ww, yy)], 6, INK, amp=0)
            g.line([(-ww - 18, yy + 92), (ww, yy)], 4, GREY, amp=0)
        _rr(c, -30, -490, 60, 40, 4)
        _shade(c, RED, 4, 0.1)
        for i in range(2):
            _rr(c, 150 + i * 90, -150, 80, 150, 10)
            _shade(c, hexc("#2b2826"), 5, 0.25)
            _stroke(c, [(150 + i * 90, -110), (230 + i * 90, -110)], 4, GOLD2, smooth=False)


def egypt_map(g, x, y, sc=1.0, t=0.0, arrow=1.0, suez=True):
    """แผนที่เชิงสัญลักษณ์ชายฝั่งแอฟริกาเหนือ: ลิเบีย -> อียิปต์ (เอล-อาลาเมน, อเล็กซานเดรีย, ไคโร, คลองสุเอซ)"""
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -480, -330, 960, 660, 30)
        _shade(c, hexc("#bcd6e6"), 6, 0.1)   # ทะเลเมดิเตอร์เรเนียน
        c.save()
        _rr(c, -480, -330, 960, 660, 30)
        c.clip()
        _smooth_path(c, [(-480, -150), (-300, -120), (-140, -60), (40, -80), (150, -60), (250, -90), (330, -80),
                         (480, -150), (600, -150), (600, 420), (-600, 420), (-600, -150)])
        _shade(c, SAND, 6, 0.15)
        c.restore()
        _rr(c, -480, -330, 960, 660, 30)
        c.set_source_rgba(*INK[:3], 1)
        c.set_line_width(6)
        c.stroke()
        _stroke(c, [(220, -70), (230, 60), (210, 330)], 12, hexc("#5aa0c8"))   # แม่น้ำไนล์
        if suez:
            _stroke(c, [(370, -110), (380, 120)], 9, hexc("#5aa0c8"), smooth=False)
            g.text("คลองสุเอซ", 380, 160, 30, "kanit", NAVY)
        g.text("ทะเลเมดิเตอร์เรเนียน", -160, -260, 32, "kanitm", NAVY)
        g.text("ลิเบีย", -330, 140, 40, "kanit", GREY)
        g.text("อียิปต์", 120, 220, 44, "kanit", GREY)
        for name, px, py, col in (("เอล-อาลาเมน", 20, -70, RED), ("อเล็กซานเดรีย", 190, -50, INK),
                                  ("ไคโร", 235, 70, INK)):
            g.circle(px, py, 13, col, 4)
            g.text(name, px, py + 34, 28, "kanit", col)
        if arrow > 0:   # ลูกศรรุกของรอมเมล
            pts = [(-420, -60), (-260, -40), (-100, -30), (-20, -50)]
            n = max(2, int(len(pts) * arrow + 0.99))
            _stroke(c, pts[:n], 22, INK)
            _stroke(c, pts[:n], 14, GERM)


def chess_piece(g, x, y, sc=1.0, col=WHITE):
    """ม้าหมากรุก (สัญลักษณ์การวางแผน)"""
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -90, -40, 180, 40, 10)
        _shade(c, col, 5, 0.25)
        _smooth_path(c, [(-60, -40), (-50, -130), (-70, -200), (-40, -270), (20, -290), (80, -240), (90, -200),
                         (30, -200), (50, -130), (60, -40)])
        _shade(c, col, 5, 0.3)
        g.circle(10, -250, 8, INK, 0)


def bolt(g, x, y, sc=1.0, col=GOLD2):
    with g.at(x, y, sc):
        g.poly([(20, -150), (-60, 10), (0, 10), (-30, 150), (70, -30), (10, -30), (50, -150)], col, 6, amp=0)


def storm(g, x, y, sc=1.0, t=0.0, calm=0.0):
    """พายุทราย (วงหมุน) -> calm=1 กลายเป็นดวงอาทิตย์สดใส"""
    c = g.c
    with g.at(x, y, sc):
        if calm < 1:
            for i in range(5):
                r = 60 + i * 50
                a0 = math.degrees(t * (2 - i * 0.2) + i)
                with g.alpha(1 - calm):
                    g.arc(0, 0, r, a0, a0 + 240, 14 - i, (0.75, 0.62, 0.38, 0.9))
        if calm > 0:
            with g.alpha(calm):
                g.sunburst(0, 0, 140, 280, 14, t * 10, 10, (0.98, 0.8, 0.35, 0.8))
                c.new_path()
                c.arc(0, 0, 120, 0, 2 * math.pi)
                _shade(c, hexc("#f6c445"), 6, 0.2)
