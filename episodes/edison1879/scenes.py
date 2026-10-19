"""ฉากตอน: หลอดไฟไส้คาร์บอนของเอดิสัน (21 ต.ค. 1879) — ตัวละครแบบกึ่งเสมือนจริง (src/people.py)"""
import math
import os
import sys

import cairo

sys.path.insert(0, os.path.dirname(__file__))
from chars import (BATCHELOR, CRITICS, EDISON, GLOW, UPTON, bench, bulb, candle, city, clock, flame,  # noqa: E402
                   furnace, heart, jar, knife_switch, material, moon, newspaper, oil_lamp, spool, stairs,
                   vacuum_pump, x_mark)
from fx import burst  # noqa: E402
from gfx import (GOLD, GOLD2, GREY, INK, LGREY, NAVY, RED, W, WHITE, e_io, e_out, hexc, hn, lerp,  # noqa: E402
                 pop, seg)
from people import _rr, _shade, head, person  # noqa: E402

CX = W / 2
GROUND = 1270
DESK = 900
GOLDTXT = hexc("#b37a12")
AMBERTXT = hexc("#d9731f")
NIGHT = hexc("#2a3150")

CAMERA = {"hook": "push_in", "dark": "pan_right", "failed": "tilt_up", "edison": "push_in", "trials": "pan_left",
          "mock": "dutch", "thread": "push_in", "glow": "pull_out", "clock": "tilt_up", "legacy": "pan_right",
          "lesson": "pull_out", "outro": "push_in"}
TRANSITIONS = {"edison": "iris", "mock": "whip", "glow": "zoom", "legacy": "fade"}


def glow_disc(g, x, y, r, a):
    if a <= 0:
        return
    rg = cairo.RadialGradient(x, y, 0, x, y, r)
    rg.add_color_stop_rgba(0, *GLOW, a)
    rg.add_color_stop_rgba(1, *GLOW, 0)
    g.c.set_source(rg)
    g.c.arc(x, y, r, 0, 2 * math.pi)
    g.c.fill()


def darkness(g, t, cx, cy, r, k=1.0, n=9, seed=4, hw=470):
    """ความมืดรอบจุดกลาง (แผงกรมท่า ไล่จางเข้าหาแสง) — k มาก = มืดบีบเข้ามาใกล้"""
    c = g.c
    hole = r * (1.0 - 0.45 * k) * (1 + 0.03 * math.sin(t * 2.3))
    c.save()
    _rr(c, cx - hw, cy - 440, 2 * hw, 880, 60)
    c.clip()
    rg = cairo.RadialGradient(cx, cy, hole * 0.55, cx, cy, hole * 1.25)
    rg.add_color_stop_rgba(0, *NIGHT[:3], 0.0)
    rg.add_color_stop_rgba(1, *NIGHT[:3], 0.92)
    c.set_source(rg)
    c.paint()
    for i in range(n):   # ดาว/ฝุ่นในความมืด
        a = 2 * math.pi * i / n + t * 0.15
        g.sparkle(cx + math.cos(a) * (hw - 70), cy + math.sin(a) * 370, 8 + 3 * math.sin(t * 3 + i), (1, 1, 1, 0.5), 0)
    c.restore()


def window(g, x, y, w, h, night=1.0, t=0.0, moon_k=0.0, dawn=0.0):
    c = g.c
    _rr(c, x - 16, y - 16, w + 32, h + 32, 8)
    _shade(c, hexc("#7a5230"), 6, 0.2)
    sky = tuple(lerp(a, b, night) for a, b in zip((0.75, 0.88, 0.98), (0.17, 0.2, 0.33)))
    sky = tuple(lerp(a, b, dawn) for a, b in zip(sky, (0.99, 0.82, 0.6)))
    _rr(c, x, y, w, h, 4)
    _shade(c, sky + (1,), 5, 0.0)
    c.save()
    _rr(c, x, y, w, h, 4)
    c.clip()
    if night > 0.3 and dawn < 0.5:
        for i in range(7):
            g.sparkle(x + 30 + (i * 97) % (w - 60), y + 30 + (i * 53) % (h * 0.6), 7 + 3 * math.sin(t * 3 + i), WHITE, 0)
    if moon_k > 0:
        moon(g, x + w * 0.7, y + h * (1.0 - 0.6 * moon_k), 46)
    if dawn > 0:
        g.circle(x + w * 0.4, y + h * (1.2 - 0.45 * dawn), 70, hexc("#f6b24a"), 5)
    c.restore()
    g.line([(x + w / 2, y), (x + w / 2, y + h)], 10, hexc("#7a5230"), amp=0)
    g.line([(x, y + h / 2), (x + w, y + h / 2)], 10, hexc("#7a5230"), amp=0)


def counter(g, x, y, txt, label, col, size=110, k=1.0):
    if k <= 0:
        return
    g.label(txt, x, y, size, color=col, sc=k)
    if label:
        g.label(label, x, y + size * 0.85, 46, sc=k)


def lab_bg(g, t):
    """ห้องทดลอง: ชั้นวางขวด + โต๊ะ"""
    c = g.c
    g.ground(GROUND, WHITE)
    _rr(c, 80, 420, 300, 18, 4)
    _shade(c, hexc("#7a5230"), 5, 0.2)
    for i, col in enumerate((hexc("#8fb8de"), hexc("#c8553d"), hexc("#6b8f3a"), hexc("#e3a92b"))):
        _rr(c, 100 + i * 68, 330, 46, 90, 10)
        _shade(c, col[:3] + (0.8,), 4, 0.25)


def check(g, x, y, s, col=hexc("#3c8d4f"), k=1.0):
    if k <= 0:
        return
    g.line([(x - 50 * s, y), (x - 50 * s + 40 * s * min(1, k * 2), y + 40 * s * min(1, k * 2))], 18 * s, col, amp=0)
    if k > 0.5:
        kk = (k - 0.5) * 2
        g.line([(x - 10 * s, y + 40 * s), (x - 10 * s + 90 * s * kk, y + 40 * s - 100 * s * kk)], 18 * s, col, amp=0)


# ------------------------------------------------------------------ 1. hook
def s_hook(g, t, L, d):
    if t < L[1] - 0.2:   # วันที่ + หลอดไฟริบหรี่
        g.ground(GROUND, WHITE)
        fl = 0.55 + 0.45 * abs(math.sin(t * 3.1) * math.sin(t * 1.7 + 1))
        bulb(g, CX, 900, 1.5, glow=fl, t=t)
        g.label("วันนี้ในอดีต", CX, 400, 104, sc=lerp(2.0, 1, e_out(seg(t, 0.1, 0.4))) if t > 0.1 else 0, rot=-4)
        g.label("21 ตุลาคม 1879", CX, 540, 84, color=RED, sc=pop(t, 0.8))
        return
    if t < L[2] - 0.2:   # ห้องทดลองเล็ก ๆ นิวเจอร์ซีย์
        g.ground(GROUND, WHITE)
        c = g.c
        with g.at(CX, GROUND, 1.0):
            _rr(c, -360, -620, 720, 620, 6)
            _shade(c, hexc("#f4efe2"), 7, 0.15)
            g.poly([(-400, -620), (0, -800), (400, -620)], hexc("#8a5a36"), 7)
            for r in range(2):
                for q in range(4):
                    on = (q + r + int((t - L[1]) * 2)) % 3 == 0
                    _rr(c, -290 + q * 160, -540 + r * 230, 100, 140, 4)
                    _shade(c, hexc("#ffd27a") if on else hexc("#cfe3f3"), 5, 0.1)
            _rr(c, -60, -170, 120, 170, 4)
            _shade(c, hexc("#7a5230"), 6, 0.2)
            _rr(c, -400, -330, 800, 26, 4)
            _shade(c, hexc("#8a5a36"), 5, 0.2)
        g.label("ห้องทดลองเล็ก ๆ", CX, 330, 84, sc=pop(t, L[1] + 0.1), rot=-3)
        g.label("รัฐนิวเจอร์ซีย์ สหรัฐฯ", CX, 1140, 56, color=NAVY, sc=pop(t, L[1] + 0.7))
        return
    if t < L[3] - 0.2:   # ชายคนหนึ่งและทีมงาน (เงา)
        g.ground(GROUND, WHITE)
        for i, (lk, x, sc) in enumerate(((BATCHELOR, 230, 0.72), (UPTON, 850, 0.7), (EDISON, CX, 0.82))):
            k = e_out(seg(t, L[2] + i * 0.3, L[2] + i * 0.3 + 0.6))
            with g.alpha(k), g.silhouette(INK, 0.92):
                person(g, x + (1 - k) * (60 if x > CX else -60), GROUND, lk, sc, seed=i + 1, turn=0.3 if x < CX else -0.3)
        g.label("ใครกัน?", CX, 330, 90, color=RED, sc=pop(t, L[2] + 1.0), rot=-4)
        return
    if t < L[5] - 0.2:   # จ้องเส้นด้ายในโหลแก้ว + หัวใจเต้นระรัว
        lab_bg(g, t)
        bench(g, -200, 1280, DESK)
        jar(g, CX, DESK, 1.5, t)
        for i, (lk, x) in enumerate(((BATCHELOR, 170), (EDISON, 900))):
            with g.at(x, 680 + 6 * math.sin(t * 2 + i), 1.25):
                head(g, lk, "worry" if i == 0 else "firm", turn=0.4 if x < CX else -0.4, look_at=(1 if x < CX else -1, 0.3))
        g.label("เส้นด้ายสีดำ", CX, 1150, 72, sc=pop(t, L[3] + 0.4))
        if t > L[4] - 0.2:
            beat = 1 + 0.18 * max(0, math.sin(t * 9)) ** 4
            heart(g, CX, 1120, 1.1 * beat * pop(t, L[4]))
            pts = []
            for i in range(40):
                xx = 120 + i * 22
                ph = (xx / 220 - t * 2.2) % 1
                yy = 1120 - (80 if 0.45 < ph < 0.5 else -50 if 0.5 < ph < 0.55 else 0)
                pts.append((xx, yy))
            with g.alpha(0.35 * pop(t, L[4])):
                g.line(pts[:14], 6, RED, amp=0)
                g.line(pts[26:], 6, RED, amp=0)
        return
    if t < L[6] - 0.2:   # ถ้าขาดเหมือนทุกครั้ง
        g.ground(GROUND, WHITE)
        bulb(g, CX, 760, 2.0, t=t, burn=seg(t, L[5] + 1.0, L[5] + 1.5))
        for i in range(5):
            x_mark(g, 170 + i * 185, 1130, 0.8, pop(t, L[5] + 0.3 + i * 0.25))
        g.label("ทุกครั้งที่ผ่านมา", CX, 330, 72, color=RED, sc=pop(t, L[5] + 0.2))
        burst(g, CX, 640, t, L[5] + 1.1, 8, 160, 18)
        return
    # ความฝันจะเอาชนะความมืด ... อาจดับลง
    g.ground(GROUND, WHITE)
    dim = 1 - 0.85 * e_io(seg(t, L[7] + 0.6, L[7] + 1.6))
    fl = dim * (0.8 + 0.2 * math.sin(t * 7)) if t > L[7] else 0.9 + 0.1 * math.sin(t * 7)
    darkness(g, t, CX, 760, 420, seg(t, L[6], L[7] + 1.6))
    bulb(g, CX, 760, 1.4, glow=fl, t=t)
    if t < L[7] - 0.2:
        g.label("เอาชนะความมืด", CX, 330, 84, color=AMBERTXT, sc=pop(t, L[6] + 0.3), rot=-3)
    else:
        g.label("หรือจะดับลง...?", CX, 330, 84, color=NAVY, sc=pop(t, L[7] + 0.2), rot=-3)


# ------------------------------------------------------------------ 2. dark
def s_dark(g, t, L, d):
    if t < L[1] - 0.2:   # พระอาทิตย์ตก
        k = seg(t, 0.2, L[1])
        g.circle(CX, lerp(700, 1150, e_io(k)), 150, hexc("#f2994a"), 7)
        c = g.c
        _rr(c, -400, 1100, W + 800, 400, 0)
        _shade(c, WHITE, 0, 0)
        g.line([(-400, 1100), (W + 400, 1100)], 7, amp=0)
        for i, x in enumerate((120, 330, 700, 900)):
            h = 140 + 50 * (i % 2)
            g.poly([(x - 90, 1100), (x - 90, 1100 - h), (x, 1100 - h - 90), (x + 90, 1100 - h), (x + 90, 1100)],
                   hexc("#5a5f75"), 6)
            _rr(c, x - 25, 1100 - h + 30, 50, 60, 4)
            _shade(c, hexc("#ffd27a") if k > 0.5 + i * 0.1 else hexc("#cfe3f3"), 4, 0)
        g.label("พระอาทิตย์ตกดิน", CX, 360, 84, sc=pop(t, 0.4), rot=-3)
        return
    if t < L[2] - 0.2:   # เทียนไข + ตะเกียงน้ำมัน
        g.ground(GROUND, WHITE)
        bench(g, 60, 1020, DESK)
        candle(g, 300, DESK, 1.5, t)
        oil_lamp(g, 760, DESK, 1.6, t)
        g.label("เทียนไข", 300, 420, 64, sc=pop(t, L[1] + 0.3))
        g.label("ตะเกียงน้ำมัน", 760, 420, 64, sc=pop(t, L[1] + 1.2))
        g.label("โลกทั้งใบพึ่งแค่นี้", CX, 1140, 60, color=NAVY, sc=pop(t, L[1] + 2.0))
        return
    g.ground(GROUND, WHITE)   # มืดสลัว + ไฟไหม้
    darkness(g, t, 330, 760, 300, 0.7, 7, hw=290)
    oil_lamp(g, 330, 980, 1.3, t)
    g.label("มืดสลัว", 330, 400, 76, color=NAVY, sc=pop(t, L[2] + 0.1))
    k = seg(t, L[2] + 1.0, L[2] + 2.0)
    with g.at(800, 1050, 1, -20 * k):
        oil_lamp(g, 0, 0, 1.0, t)
    for i in range(3):
        flame(g, 760 + i * 70, 1150, (0.7 + 0.2 * i) * pop(t, L[2] + 1.6 + i * 0.2), t)
    with g.at(800, 470, pop(t, L[2] + 1.4)):
        g.poly([(0, -110), (110, 80), (-110, 80)], GOLD, 7)
        g.label("!", 0, 10, 100)
    g.label("เสี่ยงไฟไหม้!", 760, 680, 64, color=RED, sc=pop(t, L[2] + 1.8))


# ------------------------------------------------------------------ 3. failed
def s_failed(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:
        bench(g, 0, 1080, 1000)
        years = ("1840", "1860", "1874", "1878")
        for i, y in enumerate(years):
            x = 165 + i * 250
            bulb(g, x, 790, 0.75 * pop(t, 0.3 + i * 0.3), t=t, glow=0.0, burn=1.0 if t > L[1] + 0.2 + i * 0.25 else 0)
            g.label(y, x, 1080, 46, color=GREY, sc=pop(t, 0.5 + i * 0.3))
            if t > L[1]:
                x_mark(g, x, 780, 1.0, pop(t, L[1] + 0.2 + i * 0.25))
        g.label("นักประดิษฐ์หลายคน", CX, 360, 80, sc=pop(t, 0.2), rot=-3)
        if t > L[1] - 0.2:
            g.label("ล้มเหลวไม่เป็นท่า!", CX, 500, 76, color=RED, sc=pop(t, L[1] + 1.0))
        return
    # สว่างวาบไม่กี่นาที แล้วไหม้ละลาย
    on = seg(t, L[2] + 0.2, L[2] + 0.5) * (1 - seg(t, L[3] + 0.6, L[3] + 1.0))
    burn = seg(t, L[3] + 0.6, L[3] + 1.2)
    bulb(g, 440, 820, 1.7, glow=on * (0.9 + 0.1 * math.sin(t * 20)), t=t, burn=burn)
    mins = min(3.0, (t - L[2]) * 0.9)
    clock(g, 860, 640, 120, mins / 60 * 10, pop(t, L[2] + 0.4))
    g.label("ไม่กี่นาที", 860, 860, 60, sc=pop(t, L[2] + 0.8))
    if burn > 0:
        for i in range(3):
            u = (t * 0.7 + i / 3) % 1
            g.circle(440 + 20 * math.sin(t * 2 + i), 560 - u * 240, 30 + 30 * u, (0.8, 0.8, 0.8, 0.6 * (1 - u) * burn), 0)
        g.label("ไหม้ละลาย!", 440, 1150, 76, color=RED, sc=pop(t, L[3] + 1.0), rot=-3)
    g.label("ไส้หลอด", 440, 360, 70, sc=pop(t, L[2] + 0.1))


# ------------------------------------------------------------------ 4. edison
def s_edison(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:
        g.sunburst(CX, 720, 260, 640, 22, t * 10, 12, (0.95, 0.85, 0.55, 0.8))
        person(g, CX, GROUND, EDISON, 0.92, mood="firm" if t < 2.0 else "shout", pose="down" if t < 1.6 else "point",
               turn=0.15, seed=1, talk=t > 1.6)
        g.label('"โทมัส อัลวา เอดิสัน"', CX, 330, 88, color=GOLDTXT, sc=pop(t, 0.3), rot=-3)
        g.name_tag(t, 0.8, 800, 1120, "โทมัส อัลวา เอดิสัน", "นักประดิษฐ์ วัย 32 ปี", side=-1)
        if t > 3.0:
            g.label("ท้าทายโลก!", 260, 560, 70, color=RED, sc=pop(t, 3.0), rot=-6)
        return
    person(g, 330, GROUND, EDISON, 0.85, mood="smile", pose="hold", turn=0.3, seed=1, talk=True)
    bulb(g, 760, 640, 1.1, glow=0.8 + 0.2 * math.sin(t * 3), t=t)
    g.label("ทนทาน", 760, 380, 70, color=AMBERTXT, sc=pop(t, L[1] + 0.3))
    for i in range(4):   # บ้านทุกหลังเข้าถึงได้
        x = 620 + i * 110
        k = pop(t, L[1] + 1.2 + i * 0.25)
        with g.at(x, 1150, k):
            g.poly([(-45, 0), (-45, -70), (0, -110), (45, -70), (45, 0)], hexc("#f4efe2"), 5)
            _rr(g.c, -16, -64, 32, 32, 3)
            _shade(g.c, hexc("#ffd27a"), 3, 0)
    g.label("ทุกคนเข้าถึงได้", 780, 1000, 56, sc=pop(t, L[1] + 1.0))


# ------------------------------------------------------------------ 5. trials
def s_trials(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # เบื้องหลัง: ล้มเหลวนับพันครั้ง
        n = int(min(1000, 1000 * e_io(seg(t, L[1], L[2] - 0.4)) ** 1.6)) if t > L[1] else 0
        for i in range(min(24, 6 + n // 40)):
            x = 170 + (i * 137) % 740
            y = 1180 - (i // 6) * 90 + 10 * math.sin(i)
            bulb(g, x, y, 0.5, t=t, burn=1.0, rot=(hn(i, 3) - 0.5) * 120)
        g.label("เบื้องหลัง...", CX, 360, 84, sc=pop(t, 0.2), rot=-3)
        if t > L[1] - 0.2:
            counter(g, CX, 640, f"{n:,} ครั้ง" if n < 1000 else "นับพันครั้ง", "ล้มเหลว", RED, 110, pop(t, L[1]))
        return
    if t < L[3] - 0.2:   # อดหลับอดนอน
        window(g, 640, 360, 300, 260, 1.0, t, moon_k=seg(t, L[2], L[3]))
        bench(g, -200, 1280, DESK)
        clock(g, 230, 470, 90, 2 + (t - L[2]) * 0.6)
        person(g, 420, GROUND, EDISON, 0.82, mood="sad", pose="think", turn=0.3, seed=1)
        bulb(g, 760, DESK - 110, 0.55, t=t, burn=1.0)
        for i in range(3):
            u = (t * 0.6 + i / 3) % 1
            g.label("z", 560 + 60 * u + i * 10, 520 - 160 * u, 40 + 30 * u, color=GREY, a=1 - u)
        g.label("อดหลับอดนอน", CX, 1150, 66, color=NAVY, sc=pop(t, L[2] + 0.5))
        return
    if t < L[4] - 0.2:   # ทดลองวัสดุแทบทุกอย่าง
        kinds = ["platinum", "fiber", "hair", "platinum", "fiber", "hair", "fiber", "platinum", "hair"]
        for i, kd in enumerate(kinds):
            x, y = 220 + (i % 3) * 320, 560 + (i // 3) * 260
            material(g, kd, x, y, 0.9 * pop(t, L[3] + i * 0.18), t)
        g.label("แทบทุกอย่างบนโลก", CX, 330, 80, sc=pop(t, L[3] + 0.1), rot=-3)
        return
    if t < L[5] - 0.2:   # แพลทินัม
        material(g, "platinum", CX, 740, 2.2 * pop(t, L[4] + 0.1), t)
        for i in range(3):
            g.sparkle(CX + 260 * math.cos(t * 1.4 + i * 2.1), 740 + 220 * math.sin(t * 1.4 + i * 2.1), 22, GOLD2)
        g.label("แพลทินัม", CX, 330, 90, color=GREY, sc=pop(t, L[4] + 0.2))
        g.label("โลหะล้ำค่า!", CX, 1120, 70, color=GOLDTXT, sc=pop(t, L[4] + 0.8))
        return
    if t < L[6] - 0.2:   # เส้นใยพืช -> เส้นผม
        material(g, "fiber", 300, 720, 1.6 * pop(t, L[5] + 0.1), t)
        material(g, "hair", 780, 720, 1.6 * pop(t, L[5] + 1.0), t)
        g.label("เส้นใยพืช", 300, 1000, 62, sc=pop(t, L[5] + 0.3))
        g.label("เส้นผม", 780, 1000, 62, sc=pop(t, L[5] + 1.2))
        g.line([(450, 720), (600, 720)], 10, GREY, amp=0)
        g.poly([(600, 695), (640, 720), (600, 745)], GREY, 0)
        return
    # หนวดเคราของเพื่อนร่วมงาน!
    pull = e_io(seg(t, L[6] + 0.6, L[6] + 1.2))
    person(g, 300, GROUND, BATCHELOR, 0.85, mood="shock" if pull > 0.5 else "neutral", turn=0.3, seed=2)
    person(g, 820, GROUND, EDISON, 0.82, mood="smile", pose="hold", turn=-0.3, seed=1)
    if pull > 0:
        g.line([(330, 580), (lerp(330, 640, pull), lerp(580, 640, pull))], 4, hexc("#4a3424"), amp=0)
    g.label("หนวดเคราเพื่อน!", CX, 330, 84, color=RED, sc=pop(t, L[6] + 0.2), rot=-4)
    if pull > 0.5:
        g.label("โอ๊ย!", 160, 470, 60, color=RED, sc=pop(t, L[6] + 1.1), rot=-10)


# ------------------------------------------------------------------ 6. mock
def s_mock(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:   # เดือนแล้วเดือนเล่า
        months = ["มี.ค.", "เม.ย.", "พ.ค.", "มิ.ย.", "ก.ค.", "ส.ค.", "ก.ย.", "ต.ค."]
        p = seg(t, 0.2, L[1] - 0.2) * (len(months) - 1)
        i = int(p)
        g.calendar(CX, 760, 1.5, "", months[min(i, len(months) - 1)], "1879",
                   flip=(p - i, "") if i < len(months) - 1 else None)
        g.label("เดือนแล้วเดือนเล่า", CX, 330, 80, sc=pop(t, 0.2), rot=-3)
        return
    if t < L[2] - 0.2:   # เงินทุนร่อยหรอ
        sc = lerp(1.6, 0.7, e_io(seg(t, L[1] + 0.2, L[2] - 0.3)))
        g.money_bag(CX, 820, sc)
        for i in range(5):
            u = seg(t, L[1] + 0.2 + i * 0.25, L[1] + 1.0 + i * 0.25)
            if 0 < u < 1:
                g.coin(CX + (i - 2) * 140 * u * 2, 820 - 300 * u + 400 * u * u, 36, "$", t * 300)
        g.label("เงินทุนร่อยหรอ", CX, 360, 80, color=RED, sc=pop(t, L[1] + 0.1))
        return
    if t < L[3] - 0.2:   # หัวเราะเยาะ
        for i, (lk, x) in enumerate(zip(CRITICS, (190, CX, 890))):
            person(g, x, GROUND + 10 * abs(math.sin(t * 9 + i)), lk, 0.72, mood="smile", pose="down",
                   turn=0.2 * (1 - i), seed=5 + i, talk=True)
        for i in range(4):
            u = (t * 0.8 + i / 4) % 1
            g.label("ฮ่า ๆ", 150 + i * 260, 560 - 120 * u, 50, color=GREY, a=1 - u, rot=(i - 1.5) * 10)
        g.label("หัวเราะเยาะ!", CX, 330, 84, color=RED, sc=pop(t, L[2] + 0.2), rot=-3)
        return
    person(g, 230, GROUND, EDISON, 0.78, mood="worry", turn=0.3, seed=1)   # ตราหน้า: คนเพ้อฝัน
    newspaper(g, 710, 620, 1.05 * pop(t, L[3] + 0.1), -6 + 2 * math.sin(t), "คนเพ้อฝัน!", "เอดิสันเสียสติไปแล้ว?")
    g.label("ถูกตราหน้า", 710, 1000, 66, color=NAVY, sc=pop(t, L[3] + 1.2))


# ------------------------------------------------------------------ 7. thread
def s_thread(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:   # มืดแปดด้าน
        darkness(g, t, CX, 760, 380, seg(t, 0, L[1]), 8)
        person(g, CX, GROUND, EDISON, 0.8, mood="sad", turn=0.0, seed=1)
        g.label("มืดแปดด้าน", CX, 330, 90, color=NAVY, sc=pop(t, 0.3), rot=-3)
        return
    if t < L[2] - 0.2:   # หันมามองของใกล้ตัว
        bench(g, 520, 1280, DESK)
        person(g, 300, GROUND, EDISON, 0.82, mood="think" if t < L[1] + 1.0 else "smile", pose="think", turn=0.4,
               look_at=(1, 0.4), seed=1)
        spool(g, 800, DESK - 130, 0.9)
        for i in range(4):
            g.sparkle(800 + 140 * math.cos(t * 2 + i * 1.57), 770 + 140 * math.sin(t * 2 + i * 1.57), 16 * pop(t, L[1] + 0.8))
        g.label("ของใกล้ตัวที่สุด", CX, 360, 76, sc=pop(t, L[1] + 0.2), rot=-3)
        return
    if t < L[3] - 0.2:   # เส้นด้ายฝ้ายเย็บผ้า
        spool(g, 330, 760, 2.0, rot=4 * math.sin(t), unwind=e_out(seg(t, L[2] + 0.3, L[2] + 1.5)))
        g.label('"เส้นด้ายฝ้าย', CX, 330, 80, sc=pop(t, L[2] + 0.2), rot=-3)
        g.label('เย็บผ้า"', CX, 440, 80, color=AMBERTXT, sc=pop(t, L[2] + 0.5), rot=-3)
        g.label("ธรรมดา ๆ", 760, 1050, 66, color=GREY, sc=pop(t, L[2] + 1.4))
        return
    if t < L[4] - 0.2:   # เผาอบเป็นคาร์บอน
        furnace(g, 360, 1180, 1.3, t, 1.0)
        k = seg(t, L[3] + 0.6, L[3] + 2.2)
        col = tuple(lerp(a, b, k) for a, b in zip((0.95, 0.93, 0.88), (0.1, 0.09, 0.09))) + (1,)
        with g.at(820, 760, 1.5):
            g.line([(-30, 60), (-34, 0), (-14, -40), (14, -40), (34, 0), (30, 60)], 9, INK, amp=0, smooth=True)
            g.line([(-30, 60), (-34, 0), (-14, -40), (14, -40), (34, 0), (30, 60)], 5, col, amp=0, smooth=True)
        g.label("เผาอบ", 360, 360, 72, sc=pop(t, L[3] + 0.2))
        g.label("คาร์บอนสีดำ", 820, 960, 60, sc=pop(t, L[3] + 1.6))
        g.label("เปราะบาง", 820, 1050, 50, color=RED, sc=pop(t, L[3] + 2.2))
        return
    if t < L[5] - 0.2:   # บรรจุในหลอดแก้วสุญญากาศ
        vacuum_pump(g, 250, 1220, 1.1, t)
        bulb(g, 720, 740, 1.6, t=t)
        g.line([(300, 560), (520, 560), (640, 600)], 8, GREY, amp=0)
        g.label("หลอดแก้ว", 720, 360, 72, sc=pop(t, L[4] + 0.2))
        g.label("สุญญากาศ", 720, 1130, 66, color=NAVY, sc=pop(t, L[4] + 0.8))
        return
    shake = 6 * math.sin(t * 31) * math.sin(t * 7)   # มือสั่นเทา
    with g.at(shake, shake * 0.5):
        bulb(g, 720, 700, 1.7, t=t)
    with g.at(shake * 0.6, 0):
        person(g, 230, GROUND, EDISON, 0.8, mood="worry", pose="hold", turn=0.4, look_at=(1, -0.3), seed=1)
    for i in range(3):   # เส้นสั่น
        g.line([(560 + i * 18, 1000 - i * 30), (575 + i * 18, 1030 - i * 30)], 5, GREY, amp=0)
    g.label("มือที่สั่นเทา", 720, 1150, 76, sc=pop(t, L[5] + 0.2), rot=-3)


# ------------------------------------------------------------------ 8. glow
def s_glow(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:   # สับสวิตช์
        k = e_out(seg(t, 1.0, 1.4))
        knife_switch(g, 300, 1000, 1.6, k)
        bulb(g, 800, 640, 1.2, t=t, glow=0.0)
        g.line([(420, 960), (600, 960), (800, 860)], 7, amp=0)
        if k > 0.9:
            for i in range(4):
                p = ((t - 1.4) * 2 + i / 4) % 1
                g.sparkle(lerp(420, 800, p), lerp(960, 860, max(0, p - 0.5) * 2), 18, GOLD2)
        g.label("สับสวิตช์!", CX, 330, 90, color=RED, sc=pop(t, 1.0), rot=-4)
        return
    if t < L[2] - 0.2:   # สว่างวาบ!
        k = e_out(seg(t, L[1] - 0.2, L[1] + 0.5))
        g.sunburst(CX, 760, 300, 700, 24, t * 12, 12, (1.0, 0.8, 0.45, 0.7 * k))
        bulb(g, CX, 760, 1.9, t=t, glow=k)
        g.label("แสงสีส้มนวลตา!", CX, 330, 86, color=AMBERTXT, sc=pop(t, L[1] + 0.3), rot=-3)
        return
    # ทุกคนหยุดหายใจ / ไม่ละสายตา
    glow_disc(g, CX, 640, 700, 0.35)
    bench(g, -200, 1280, DESK)
    bulb(g, CX, DESK - 230, 0.9, t=t, glow=1.0)
    trio = ((BATCHELOR, 150, "shock"), (EDISON, 920, "shock" if t < L[3] else "smile"))
    for i, (lk, x, m) in enumerate(trio):
        with g.at(x, 600, 1.3):
            head(g, lk, m, turn=0.4 if x < CX else -0.4, look_at=(1 if x < CX else -1, 0.2))
    if t < L[3] - 0.2:
        g.label("แทบหยุดหายใจ", CX, 330, 80, sc=pop(t, L[2] + 0.2), rot=-3)
    else:
        g.label("ไม่มีใครละสายตา", CX, 330, 80, color=NAVY, sc=pop(t, L[3] + 0.2), rot=-3)


# ------------------------------------------------------------------ 9. clock
def hours_at(t, L):
    """เวลาที่หลอดสว่างมาแล้ว (ชั่วโมง) ตามบรรทัดพากย์"""
    if t < L[1]:
        return lerp(0, 5 / 60, seg(t, 0, L[1]))
    if t < L[2]:
        return lerp(5 / 60, 1.0, e_io(seg(t, L[1], L[2])))
    if t < L[5]:
        return lerp(1.0, 12.0, seg(t, L[2], L[5]))
    return lerp(12.0, 13.5, e_out(seg(t, L[5], L[5] + 1.5)))


def s_clock(g, t, L, d):
    g.ground(GROUND, WHITE)
    h = hours_at(t, L)
    if t < L[2] - 0.2:
        clock(g, 330, 720, 210, h)
        bulb(g, 820, 720, 1.1, t=t, glow=1.0)
        txt = "5 นาที" if t < L[1] + 1.5 else "1 ชั่วโมง"
        counter(g, 330, 1100, txt, "", RED, 80, pop(t, 0.3 if t < L[1] + 1.5 else L[1] + 1.5))
        g.label("ติ๊ก... ต็อก...", CX, 330, 76, color=GREY, sc=pop(t, 0.2), rot=-3)
        return
    if t < L[3] - 0.2:   # ค่ำคืนอันเหน็บหนาว
        window(g, 560, 340, 400, 340, 1.0, t, moon_k=seg(t, L[2], L[3]))
        bench(g, -200, 1280, DESK)
        bulb(g, 420, DESK - 230, 0.9, t=t, glow=1.0)
        clock(g, 200, 470, 100, h)
        person(g, 760, GROUND, EDISON, 0.75, mood="neutral", pose="cross", turn=-0.3, look_at=(-1, 0.3), seed=1)
        for i in range(3):   # ลมหายใจเป็นไอ (หนาว)
            u = (t * 0.7 + i / 3) % 1
            g.circle(700 - 60 * u, 640 - 30 * u, 14 + 16 * u, (0.85, 0.9, 0.95, 0.7 * (1 - u)), 0)
        g.label(f"{int(h)} ชั่วโมง", 200, 640, 56, color=RED, sc=pop(t, L[2] + 0.4))
        g.label("ค่ำคืนเหน็บหนาว", CX, 1170, 62, color=NAVY, sc=pop(t, L[2] + 2.0))
        return
    if t < L[4] - 0.2:   # ไส้หลอดไม่ยอมขาด
        bulb(g, CX, 740, 1.9, t=t, glow=0.9 + 0.1 * math.sin(t * 5))
        g.label("ไม่ยอมขาด!", CX, 360, 90, color=RED, sc=pop(t, L[3] + 1.0), rot=-4)
        g.label(f"{int(h)} ชั่วโมง", CX, 1200, 60, color=GREY)
        return
    if t < L[5] - 0.2:   # สู้ความมืดอย่างมั่นคง
        darkness(g, t, CX, 760, 460, 0.4 - 0.4 * seg(t, L[4], L[5]), 10)
        bulb(g, CX, 760, 1.5, t=t, glow=1.0)
        g.label("สู้ความมืด", CX, 330, 86, color=AMBERTXT, sc=pop(t, L[4] + 0.2), rot=-3)
        return
    window(g, 560, 340, 400, 340, 1.0 - seg(t, L[5], L[5] + 1.5), t, dawn=seg(t, L[5], L[5] + 1.5))
    clock(g, 300, 600, 170, h)
    counter(g, CX, 960, "13½ ชั่วโมง!", "", RED, 110, pop(t, L[5] + 0.6))
    for i in range(5):
        g.sparkle(160 + i * 190, 1150 + 20 * math.sin(t * 3 + i), 16 * pop(t, L[5] + 0.9 + i * 0.15))


# ------------------------------------------------------------------ 10. legacy
def s_legacy(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:
        bulb(g, 300, 760, 1.3, t=t, glow=1.0)
        counter(g, 760, 640, "13½", "ชั่วโมง", RED, 140, pop(t, 0.2))
        if t > L[1] - 0.2:   # จุดเปลี่ยน: มาถูกทาง
            check(g, 760, 940, 1.6, k=seg(t, L[1] + 0.8, L[1] + 1.4))
            g.label("จุดเปลี่ยนประวัติศาสตร์", CX, 330, 76, sc=pop(t, L[1] + 0.1), rot=-3)
            g.label("มาถูกทาง!", 760, 1150, 66, color=hexc("#3c8d4f"), sc=pop(t, L[1] + 1.4))
        return
    if t < L[3] - 0.2:   # นับพันชั่วโมง
        k = e_io(seg(t, L[2] + 0.3, L[2] + 2.6))
        n = int(lerp(13.5, 1200, k))
        bulb(g, CX, 780, 1.5, t=t, glow=1.0)
        counter(g, CX, 360, f"{n:,} ชั่วโมง" if k < 1 else "นับพันชั่วโมง", "", RED, 96, pop(t, L[2] + 0.2))
        g.label("พัฒนาต่อยอด", CX, 1140, 66, color=NAVY, sc=pop(t, L[2] + 0.6))
        return
    # เมืองยามค่ำคืนสว่างไสว
    lit = e_io(seg(t, L[3] + 0.3, L[4] + 1.5))
    moon(g, 860, 540, 56)
    city(g, -300, 1380, 1160, t, lit)
    g.label("ค่ำคืนที่เปลี่ยนไป", CX, 340, 80, sc=pop(t, L[3] + 0.2), rot=-3)
    if t > L[4] - 0.2:
        g.label("ไม่เหมือนเดิมอีกต่อไป", CX, 1220, 60, color=AMBERTXT, sc=pop(t, L[4] + 0.4))


# ------------------------------------------------------------------ 11. lesson
def s_lesson(g, t, L, d):
    g.ground(GROUND, WHITE)
    g.label("บทเรียน", CX, 340, 100, sc=pop(t, 0.1), rot=-3)
    if t < L[3] - 0.2:
        if t > L[1] - 0.2:
            for i in range(9):   # เส้นแบ่ง
                g.line([(CX, 520 + i * 80), (CX, 560 + i * 80)], 8, GREY, amp=0)
            gave_up = seg(t, L[2] + 0.6, L[2] + 1.8)
            with g.alpha(1 - 0.75 * gave_up):
                person(g, 270 - 120 * gave_up, GROUND, EDISON, 0.62, mood="sad" if gave_up > 0 else "worry",
                       turn=0.3 - 0.6 * gave_up, seed=3)
            person(g, 790, GROUND, EDISON, 0.62, mood="firm", pose="hold", turn=-0.3, seed=1)
            bulb(g, 900, 640, 0.45, t=t, glow=pop(t, L[2] + 1.8))
            g.label("คนเพ้อฝัน", 270, 470, 56, color=GREY, sc=pop(t, L[1] + 0.3))
            g.label("ผู้เปลี่ยนโลก", 790, 470, 56, color=GOLDTXT, sc=pop(t, L[1] + 0.9))
            if t > L[2] - 0.2:
                g.label("ยอมแพ้ก่อน?", 270, 1140, 56, color=RED, sc=pop(t, L[2] + 0.4))
        return
    k = seg(t, L[3] - 0.2, L[3] + 2.2)
    stairs(g, 100, 1240, 7, k, step_w=105, step_h=80)
    if t > L[4] - 0.2:
        kk = e_io(seg(t, L[4] + 0.3, L[4] + 2.0))
        person(g, lerp(150, 780, kk), 1240 - lerp(80, 560, kk), EDISON, 0.36, mood="smile", seed=1, turn=-0.2,
               shadow=False)
        bulb(g, 880, 470, 0.45, t=t, glow=pop(t, L[4] + 1.8))
        g.label("บันไดสู่ความสำเร็จ", 380, 560, 60, color=GOLDTXT, sc=pop(t, L[4] + 0.3))
    else:
        person(g, 150, 1240 - 80 * min(1, k * 7), EDISON, 0.36, mood="firm", seed=1, turn=-0.2, shadow=False)
        g.label("ล้มเหลว ไม่ใช่ พ่ายแพ้", CX, 500, 64, color=RED, sc=pop(t, L[3] + 0.3))


# ------------------------------------------------------------------ 12. outro
def s_outro(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # ทุ่มเทซ้ำ ๆ ท่ามกลางคำดูถูก
        bench(g, 420, 1280, DESK)
        n = int((t - 0.2) * 1.4)
        person(g, 280, GROUND, EDISON, 0.8, mood="firm", pose="hold" if n % 2 else "think", turn=0.3, seed=1)
        for i in range(min(n, 6)):
            x_mark(g, 600 + (i % 3) * 140, 760 + (i // 3) * 110, 0.6, pop(t, 0.2 + (i + 1) / 1.4))
        g.label("ทุ่มเทซ้ำ ๆ", CX, 330, 84, sc=pop(t, 0.2), rot=-3)
        if t > L[1] - 0.2:
            for i, s in enumerate(("ไม่มีทาง!", "เพ้อฝัน!")):
                with g.at(700 + i * 120, 470 + i * 130, pop(t, L[1] + 0.2 + i * 0.5)):
                    g.bubble(0, 0, 300, 110, WHITE, tail=(1, 1))
                    g.label(s, 0, 0, 44, color=GREY)
        return
    if t < L[3] - 0.2:   # แรงผลักดัน
        beat = 1 + 0.12 * max(0, math.sin(t * 7)) ** 4
        heart(g, 360, 760, 2.2 * beat * pop(t, L[2]))
        bulb(g, 760, 760, 1.1, t=t, glow=1.0)
        g.label("+", 560, 760, 100, sc=pop(t, L[2] + 0.4))
        g.label("แรงผลักดันของคุณ?", CX, 340, 80, color=RED, sc=pop(t, L[2] + 0.2), rot=-3)
        return
    with g.at(CX + 120, 650, pop(t, L[3] - 0.1)):
        g.bubble(0, 0, 520, 240, WHITE, tail=(-1, 1))
        for i in range(3):
            g.circle(-110 + i * 110, 0, 24 + 6 * math.sin(t * 6 - i), INK, 0)
    person(g, 270, GROUND, EDISON, 0.75, mood="smile", pose="wave", turn=0.3, seed=1, talk=True)
    for i in range(5):
        g.sparkle(160 + i * 190, 1180 + 20 * math.sin(t * 3 + i), 14 * pop(t, L[3] + 0.5 + i * 0.3))
    g.label("คอมเมนต์คุยกันได้เลย!", 660, 960, 62, color=RED, sc=pop(t, L[3] + 0.4))


SCENES = {
    "hook": s_hook, "dark": s_dark, "failed": s_failed, "edison": s_edison, "trials": s_trials, "mock": s_mock,
    "thread": s_thread, "glow": s_glow, "clock": s_clock, "legacy": s_legacy, "lesson": s_lesson, "outro": s_outro,
}
NO_IRIS = set()
