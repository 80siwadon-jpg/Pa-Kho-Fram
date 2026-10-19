"""ฉากตอน: นิยาม 1 เมตรด้วยความเร็วแสง (21 ต.ค. 1983) — ภาพจริงผ่าน src/photos.py (ไม่มีไฟล์ = วาดการ์ตูนแทน)"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from chars import (BEAM, KID, PT, SCIENTISTS, SPACE, YELLOW, airplane, atom, eiffel, hn, light_beam,  # noqa: E402
                   metre_bar, planet, rocket, ruler, satellite, space_panel, stars, stopwatch, tape_measure, vault,
                   wave)
from gfx import (GOLD, GOLD2, GREY, INK, LGREY, NAVY, RED, W, WHITE, e_io, e_out, hexc, lerp, pop,  # noqa: E402
                 seg)
from people import _rr, _shade, head, person  # noqa: E402
from photos import photo  # noqa: E402

CX = W / 2
GROUND = 1270
GOLDTXT = hexc("#b37a12")
GREEN = hexc("#3c8d4f")
BLUE = hexc("#3f6496")

CAMERA = {"hook": "push_in", "bar": "pan_right", "risk": "dutch", "paris": "tilt_up", "define": "push_in",
          "impact": "pan_left", "lesson": "pull_out", "outro": "push_in"}
TRANSITIONS = {"bar": "zoom", "risk": "whip", "paris": "fade", "define": "zoom", "impact": "iris"}


def ap(t, a, dur=0.38):
    return pop(t, a - 0.2, dur)


def earth(g, x, y, r, t=0.0):
    c = g.c
    c.new_path()
    c.arc(x, y, r, 0, 2 * math.pi)
    _shade(c, hexc("#5a8fd0"), 6, 0.3)
    c.save()
    c.arc(x, y, r, 0, 2 * math.pi)
    c.clip()
    for i in range(5):
        cx = x + ((i * 0.37 + t * 0.03) % 1 * 2.4 - 1.2) * r
        g.blob(cx, y + (hn(i, 7) - 0.5) * r * 1.2, r * 0.32, r * 0.22, GREEN, 0, 3 + i)
    c.restore()
    c.new_path()
    c.arc(x, y, r, 0, 2 * math.pi)
    c.set_source_rgba(*INK)
    c.set_line_width(6)
    c.stroke()


def skyscraper(g, x, y, w, h, tilt=0.0, crack=0.0):
    c = g.c
    with g.at(x, y, 1, tilt):
        _rr(c, -w / 2, -h, w, h, 4)
        _shade(c, hexc("#9aa0ab"), 6, 0.3)
        for r in range(int(h / 60)):
            for q in range(3):
                _rr(c, -w / 2 + 16 + q * (w - 32) / 3, -h + 20 + r * 60, (w - 32) / 3 - 10, 34, 2)
                _shade(c, hexc("#cfe3f3"), 2, 0)
        if crack > 0:
            g.line([(-w * 0.1, -h * 0.5), (w * 0.12, -h * 0.42), (-w * 0.05, -h * 0.33), (w * 0.2, -h * 0.25)][:2 + int(crack * 2)],
                   6, INK, amp=0)


def chain_link(g, x, y, rot, s=1.0, broken=0.0):
    with g.at(x + broken * 30 * math.cos(math.radians(rot)), y + broken * 30, s, rot + 40 * broken):
        g.c.new_path()
        g.c.save()
        g.c.scale(1, 0.55)
        g.c.arc(0, 0, 50, 0, 2 * math.pi)
        g.c.restore()
        g.c.set_source_rgba(*GREY[:3], 1)
        g.c.set_line_width(14)
        g.c.stroke()


def flags_row(g, t, y, k=1.0):
    cols = [(hexc("#2b3f8a"), WHITE, hexc("#c8553d")), (hexc("#c8553d"), WHITE, hexc("#2b3f63")),
            (hexc("#2f5a3a"), WHITE, hexc("#c8553d")), (hexc("#e3a92b"), hexc("#c8553d"), hexc("#2b2622"))]
    for i, cs in enumerate(cols):
        x = 180 + i * 240
        with g.at(x, y, k * pop(t, 0.2 + i * 0.15)):
            for j, col in enumerate(cs):
                _rr(g.c, -70 + j * 46.6, -50, 46.6, 100, 0)
                _shade(g.c, col, 0, 0)
            g.c.rectangle(-70, -50, 140, 100)
            g.c.set_source_rgba(*INK)
            g.c.set_line_width(4)
            g.c.stroke()
            ruler(g, 0, 150, 200, 0.9, label="1 m")


# ------------------------------------------------------------------ 1. hook
def s_hook(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:
        metre_bar(g, CX - 40, 860, 760, 1.0, 0, glow=1.0, t=t)
        g.label("วันนี้ในอดีต", CX, 380, 104, sc=lerp(2.0, 1, e_out(seg(t, 0.1, 0.4))) if t > 0.1 else 0, rot=-4)
        g.label("21 ตุลาคม 1983", CX, 520, 84, color=RED, sc=pop(t, 0.8))
        return
    if t < L[2] - 0.2:   # 1 เมตรของคนทั้งโลก
        earth(g, CX, 800, 260, t)
        ruler(g, CX, 1140, 640, ap(t, L[1] + 0.4), label="1 เมตร")
        g.label("1 เมตรของคนทั้งโลก", CX, 380, 80, sc=ap(t, L[1]), rot=-3)
        return
    if t < L[3] - 0.2:   # เพี้ยนแค่เสี้ยวมิลลิเมตร
        off = 18 * e_io(seg(t, L[2] + 0.6, L[2] + 1.6))
        ruler(g, CX, 720, 900, 1.0, label="ของจริง")
        ruler(g, CX + off, 900, 900, 1.0, col=hexc("#f2a0a0"), label="เพี้ยน?")
        with g.at(CX + 300, 810):
            g.circle(0, 0, 120, (0.9, 0.95, 1, 0.5), 8)
            g.line([(80, 80), (170, 170)], 22, hexc("#7a5230"), amp=0)
        g.label("แค่เสี้ยวมิลลิเมตร...", CX, 380, 80, color=RED, sc=ap(t, L[2]), rot=-3)
        g.label("หายนะ?", CX, 1130, 80, color=RED, sc=ap(t, L[2] + 1.6))
        return
    if t < L[4] - 0.2:   # ตึกระฟ้าพังทลาย
        k = e_io(seg(t, L[3], L[4]))
        skyscraper(g, CX, GROUND, 260, 760, -8 * k, k)
        g.label("ตึกระฟ้าพัง?", CX, 380, 84, color=RED, sc=ap(t, L[3]), rot=-3)
        return
    if t < L[5] - 0.2:   # ระบบนำทางเครื่องบิน
        k = seg(t, L[4], L[5])
        pts = [(lerp(100, 980, u), 800 - 120 * u + 160 * u * u * k) for u in [i / 20 for i in range(21)]]
        for i in range(0, 20, 2):
            g.line(pts[i:i + 2], 6, GREY, amp=0)
        u = 0.2 + 0.6 * k
        airplane(g, lerp(100, 980, u), 800 - 120 * u + 160 * u * u * k, 0.9, 12 * k)
        g.label("ระบบนำทางล่ม?", CX, 380, 84, color=RED, sc=ap(t, L[4]), rot=-3)
        return
    if t < L[6] - 0.2:   # ยานอวกาศหลงทาง
        space_panel(g)
        stars(g, t)
        rocket(g, lerp(300, 760, seg(t, L[5], L[6])), 800, 0.9, t * 80, 0.5, t)
        g.label("หลงทางกลางจักรวาล!", CX, 380, 76, color=RED, sc=ap(t, L[5]), rot=-3)
        return
    if t < L[7] - 0.2:   # โยนไม้บรรทัดทิ้ง
        k = e_io(seg(t, L[6] + 0.8, L[6] + 2.4))
        ruler(g, lerp(CX, 1300, k), lerp(820, 300, k) + 300 * k * k, 640, 1.0, k * 400, label="1 เมตร")
        g.label("โยนไม้บรรทัดทิ้ง!", CX, 380, 84, sc=ap(t, L[6]), rot=-3)
        return
    k = e_out(seg(t, L[7] - 0.2, L[7] + 1.0))   # ความเร็วแสง!
    g.sunburst(CX, 820, 200, 620, 22, t * 12, 12, (0.98, 0.88, 0.5, 0.7 * k))
    light_beam(g, -300, 820, 1400, k, t, 40)
    g.label('"ความเร็วแสง"!', CX, 380, 100, color=GOLDTXT, sc=ap(t, L[7]), rot=-4)


# ------------------------------------------------------------------ 2. bar
def s_bar(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:   # 1 เมตรที่ทั้งโลกใช้ตรงกัน
        flags_row(g, t, 700)
        g.label("ใช้ตรงกันทั้งโลก", CX, 380, 80, sc=ap(t, 0.2), rot=-3)
        return
    if t < L[2] - 0.2:   # แท่งแพลทินัม-อิริเดียม
        if not photo(g, "bar", CX, 780, 860, 560, -2, ap(t, L[1]), 1.0 + 0.06 * seg(t, L[1], L[2]),
                     label="แท่งเมตรต้นแบบ (แพลทินัม-อิริเดียม)"):
            metre_bar(g, CX - 40, 820, 820, 1.0, 0, glow=1.0, t=t)
            g.label("แพลทินัม 90% · อิริเดียม 10%", CX, 1060, 54, color=GREY, sc=ap(t, L[1] + 0.8))
        g.label("แท่งเดียวในโลก!", CX, 380, 84, color=GOLDTXT, sc=ap(t, L[1]), rot=-3)
        return
    if t < L[3] - 0.2:   # ห้องนิรภัยใต้ดินที่ฝรั่งเศส
        if t > L[2] + 1.6 and photo(g, "bipm", CX, 780, 860, 560, 2, ap(t, L[2] + 1.8), 1.04,
                                    label="สำนักงานชั่งตวงวัดระหว่างประเทศ (BIPM) เมืองแซฟวร์"):
            g.label("ฝรั่งเศส", CX, 380, 84, sc=ap(t, L[2]), rot=-3)
            return
        vault(g, 380, 800, 230, seg(t, L[2], L[3]), t)
        eiffel(g, 850, 1180, 0.7)
        g.label("ห้องนิรภัยใต้ดิน", CX, 380, 80, sc=ap(t, L[2]), rot=-3)
        g.label("ฝรั่งเศส", 850, 1130, 60, color=BLUE, sc=ap(t, L[2] + 0.8))
        return
    if t < L[4] - 0.2:   # 1 เมตรที่แท้จริงยาวแค่ไหน?
        flags_row(g, t + L[3], 640)
        for i in range(4):
            g.label("?", 180 + i * 240, 1000 + 15 * math.sin(t * 3 + i), 90, color=RED, sc=ap(t, L[3] + 0.3 + i * 0.15))
        g.label("ยาวแค่ไหนกันแน่?", CX, 380, 80, sc=ap(t, L[3]), rot=-3)
        return
    k = e_io(seg(t, L[4] + 0.2, L[4] + 1.4))   # เอามาเทียบกับแท่งต้นแบบ
    metre_bar(g, CX - 40, 720, 820, 1.0, 0, t=t)
    ruler(g, CX - 40, lerp(1150, 860, k), 820, 1.0, label="ไม้บรรทัดต้นแบบของแต่ละประเทศ")
    for sx in (-1, 1):
        g.line([(CX - 40 + sx * 380, 680), (CX - 40 + sx * 380, 920)], 4, RED, amp=0)
    if k > 0.95:
        g.label("ตรงกัน ✓".replace(" ✓", ""), CX, 1130, 70, color=GREEN, sc=ap(t, L[4] + 1.5))
    g.label("ต้องเอามาเทียบ!", CX, 380, 84, sc=ap(t, L[4]), rot=-3)


# ------------------------------------------------------------------ 3. risk
def s_risk(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:   # นักวิทยาศาสตร์กุมขมับ
        for i, lk in enumerate(SCIENTISTS[:3]):
            person(g, 190 + i * 340, GROUND, lk, 0.68, mood="worry", pose="think", turn=0.2 * (1 - i), seed=10 + i)
        g.label("กุมขมับ...", CX, 380, 90, color=NAVY, sc=ap(t, 0.2), rot=-3)
        return
    if t < L[3] - 0.2:   # ไม่มีวัตถุใดเป็นอมตะ / เสื่อม หด ขีดข่วน
        sc_ = seg(t, L[2], L[3] - 0.6)
        metre_bar(g, CX - 40, 800, 820, 1.0, 0, scratch=sc_, shrink=sc_, t=t)
        if t < L[2] - 0.2:
            g.label("ไม่มีวัตถุใดเป็นอมตะ", CX, 380, 76, sc=ap(t, L[1]), rot=-3)
            stopwatch(g, CX, 1060, 90, (t * 0.5) % 1)
        else:
            for i, s in enumerate(("เสื่อมสภาพ", "หดตัว", "รอยขีดข่วน")):
                g.label(s, 200 + i * 340, 1060, 58, color=RED, sc=ap(t, L[2] + 0.5 + i * 1.2))
            g.label("ตามกาลเวลา", CX, 380, 80, color=NAVY, sc=ap(t, L[2]), rot=-3)
        return
    if t < L[5] - 0.2:   # สงคราม/ภัยพิบัติ -> สูญสลาย
        shake = 6 * math.sin(t * 30) * seg(t, L[3] + 0.5, L[4])
        fade = seg(t, L[4] - 0.2, L[4] + 1.2)
        with g.alpha(1 - fade):
            vault(g, CX + shake, 780, 260, 0, t)
        for i in range(4):
            u = (t * 0.5 + i / 4) % 1
            g.circle(CX - 260 + i * 170, 520 - u * 160, 50 + 40 * u, (0.6, 0.6, 0.62, 0.5 * (1 - u)), 0)
        if fade > 0:
            for i in range(14):
                a = i * 2 * math.pi / 14
                g.circle(CX + math.cos(a) * 300 * fade, 780 + math.sin(a) * 300 * fade, 14, (*PT[:3], 1 - fade), 3)
        if t < L[4] - 0.2:
            g.label("สงคราม · ภัยพิบัติ", CX, 380, 80, color=RED, sc=ap(t, L[3]), rot=-3)
        else:
            g.label("สูญสลายในพริบตา!", CX, 380, 84, color=RED, sc=ap(t, L[4]), rot=-4)
        return
    if t < L[6] - 0.2:   # คลื่นแสงจากอะตอมก๊าซ (คริปทอน-86, 1960)
        atom(g, 280, 780, 160, t)
        wave(g, 480, 1000, 780, 60, 110, t)
        g.label("ปี 1960", CX, 380, 84, color=BLUE, sc=ap(t, L[5]), rot=-3)
        g.label("คลื่นแสงจากอะตอมคริปทอน-86", CX, 1120, 52, sc=ap(t, L[5] + 0.5))
        return
    if t < L[7] - 0.2:   # ยุคอวกาศ + เลเซอร์
        space_panel(g)
        stars(g, t)
        rocket(g, 300, 900 - 120 * seg(t, L[6], L[7]), 0.8, 0, 1.0, t)
        light_beam(g, 420, 640, 1000, e_out(seg(t, L[6] + 0.4, L[6] + 1.2)), t, 16)
        g.label("ยุคอวกาศ + เลเซอร์", CX, 380, 80, color=GOLDTXT, sc=ap(t, L[6]), rot=-3)
        return
    a = lerp(-50, 60, e_io(seg(t, L[7], L[7] + 1.2)))   # ความแม่นยำไม่พอ
    with g.at(CX, 980):
        for a0, lw, col in ((math.pi, 14, INK), (math.radians(330), 26, RED)):
            g.c.new_path()
            g.c.arc(0, 0, 300, a0, 2 * math.pi)
            g.c.set_source_rgba(*col)
            g.c.set_line_width(lw)
            g.c.stroke()
        g.line([(0, 0), (math.sin(math.radians(a)) * 260, -math.cos(math.radians(a)) * 260)], 12, INK, amp=0)
        g.circle(0, 0, 20, INK, 0)
    g.label("ความแม่นยำไม่พอแล้ว!", CX, 380, 76, color=RED, sc=ap(t, L[7]), rot=-3)


# ------------------------------------------------------------------ 4. paris
def s_paris(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:   # ปารีส ที่ประชุมนานาชาติ
        eiffel(g, 300, GROUND, 1.0)
        with g.at(720, 820, ap(t, 0.4)):
            g.rrect(-220, -150, 440, 300, 20, WHITE, 6)
            g.label("CGPM", 0, -60, 70, color=BLUE)
            g.label("ครั้งที่ 17 · 1983", 0, 30, 48)
        g.label("ที่ประชุมนานาชาติ · ปารีส", CX, 380, 70, sc=ap(t, 0.2), rot=-3)
        return
    if t < L[3] - 0.2:   # หัวกะทิของโลก ตัดสินใจปฏิวัติ
        vote = t > L[2] - 0.2
        for i, lk in enumerate(SCIENTISTS):
            person(g, 150 + i * 260, GROUND, lk, 0.62, mood="smile" if vote else "firm",
                   pose="wave" if vote and (i % 2 == 0 or t > L[2] + 0.6) else "down", turn=0.2 * (1.5 - i), seed=20 + i)
        if vote:
            g.label("ปฏิวัติวงการ!", CX, 380, 90, color=RED, sc=ap(t, L[2]), rot=-4)
        else:
            g.label("นักวิทยาศาสตร์หัวกะทิ", CX, 380, 76, sc=ap(t, L[1]), rot=-3)
        return
    if t < L[4] - 0.2:   # เลิกพึ่งวัตถุบนโลก
        metre_bar(g, CX - 40, 800, 820, 1.0, 0, t=t)
        k = ap(t, L[3] + 0.5)
        if k > 0:
            g.line([(CX - 380, 640), (CX + 300, 960)], 22 * k, RED, amp=0)
            g.line([(CX + 300, 640), (CX - 380, 960)], 22 * k, RED, amp=0)
        g.label("เลิกพึ่งวัตถุ", CX, 380, 84, sc=ap(t, L[3]), rot=-3)
        return
    if t < L[5] - 0.2:   # ผูก 1 เมตรเข้ากับกฎของเอกภพ
        space_panel(g)
        stars(g, t)
        ruler(g, 300, 800, 360, 0.9, label="1 m")
        n = int(5 * e_out(seg(t, L[4] + 0.2, L[4] + 1.6)))
        for i in range(n):
            chain_link(g, 500 + i * 80, 800, 90 * (i % 2), 0.7)
        g.sparkle(940, 800, 60 + 8 * math.sin(t * 6), (1, 0.9, 0.5, 1), 0)
        g.label("กฎเหล็กของเอกภพ", CX, 380, 80, color=GOLDTXT, sc=ap(t, L[4]), rot=-3)
        return
    k = e_out(seg(t, L[5] - 0.2, L[5] + 0.8))   # ความเร็วแสง!
    g.sunburst(CX, 800, 200, 640, 24, t * 12, 12, (0.98, 0.88, 0.5, 0.7 * k))
    light_beam(g, -300, 800, 1400, k, t, 44)
    g.label('"ความเร็วแสง"!', CX, 380, 100, color=GOLDTXT, sc=ap(t, L[5]), rot=-4)
    g.label("299,792,458 เมตร/วินาที", CX, 1100, 58, sc=ap(t, L[5] + 0.6))


# ------------------------------------------------------------------ 5. define
def s_define(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:   # นิยามใหม่
        with g.at(CX, 800, ap(t, 0.2), -3):
            g.rrect(-320, -260, 640, 520, 16, hexc("#f6f1e4"), 6)
            g.label("นิยามใหม่", 0, -170, 70, color=RED)
            for k in range(5):
                g.line([(-240, -60 + k * 50), (240 - (k == 4) * 160, -60 + k * 50)], 8, LGREY, amp=0)
            with g.at(170, 170, 1, -12):
                g.circle(0, 0, 70, (1, 1, 1, 0), 7, stroke=RED)
                g.text("1983", 0, 0, 40, "kanit", RED)
        g.label("นับจากนี้ไป...", CX, 380, 84, sc=ap(t, 0.2), rot=-3)
        return
    space_panel(g)
    stars(g, t)
    k = e_io(seg(t, L[1] + 0.2, L[1] + 1.8)) if t < L[2] else (((t - L[2]) * 0.8) % 1)
    for x in (200, 880):
        g.line([(x, 700), (x, 940)], 8, WHITE, amp=0)
    light_beam(g, 200, 820, 880, k, t, 22)
    g.label("1 เมตร", CX, 1000, 66, color=GOLDTXT, sc=ap(t, L[1]))
    if t < L[2] - 0.2:
        g.label("แสงเดินทางในสุญญากาศ", CX, 380, 70, color=GOLDTXT, sc=ap(t, L[1]), rot=-3)
    else:
        stopwatch(g, CX, 560, 80, k)
        g.label("1 / 299,792,458 วินาที", CX, 1150, 64, color=RED, sc=ap(t, L[2]))


# ------------------------------------------------------------------ 6. impact
def s_impact(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:   # น่าปวดหัว
        person(g, CX, GROUND, SCIENTISTS[0], 0.8, mood="worry", pose="think", turn=0.1, seed=30)
        for i, s in enumerate(("299,792,458", "1/c", "3×10⁸".replace("⁸", "8"), "c")):
            a = t * 1.5 + i * 1.57
            g.label(s, CX + 300 * math.cos(a), 540 + 80 * math.sin(a), 44, color=GREY)
        g.label("ปวดหัว?", CX, 380, 90, color=NAVY, sc=ap(t, 0.2), rot=-3)
        return
    if t < L[2] - 0.2:   # มติประกาศใช้
        with g.at(CX, 820, ap(t, L[1]), -6):
            g.rrect(-300, -110, 600, 220, 20, (1, 1, 1, 0), 12, stroke=RED)
            g.label("ประกาศใช้!", 0, 0, 96, color=RED)
        return
    if t < L[3] - 0.2:   # ปลดแอกจากวัตถุบนโลก
        brk = e_out(seg(t, L[2] + 1.0, L[2] + 2.0))
        earth(g, CX, 800, 220, t)
        for i in range(8):
            a = i * math.pi / 4
            chain_link(g, CX + math.cos(a) * 300, 800 + math.sin(a) * 300, math.degrees(a) + 90, 0.8, brk)
        for i in range(6):
            g.sparkle(CX + 380 * math.cos(t + i), 800 + 380 * math.sin(t + i), 16 * brk)
        g.label("ปลดแอก!", CX, 380, 96, color=GREEN, sc=ap(t, L[2]), rot=-4)
        return
    if t < L[5] - 0.2:   # แสงวิ่งผ่านจักรวาล / ไม่เพี้ยนแม้ระดับอะตอม
        space_panel(g)
        stars(g, t)
        for i in range(3):
            light_beam(g, 100, 560 + i * 220, 980, ((t * 0.4 + i / 3) % 1), t, 12)
        if t < L[4] - 0.2:
            g.label("ตราบใดที่แสงยังวิ่ง", CX, 380, 76, color=GOLDTXT, sc=ap(t, L[3]), rot=-3)
        else:
            with g.at(CX, 780, ap(t, L[4])):
                g.circle(0, 0, 200, WHITE, 6)
                atom(g, 0, 0, 140, t)
            g.label("ไม่เพี้ยนแม้ระดับอะตอม", CX, 380, 70, color=GOLDTXT, sc=ap(t, L[4]), rot=-3)
        return
    if t < L[6] - 0.2:   # รากฐานความแม่นยำ
        earth(g, CX, 820, 230, t)
        stopwatch(g, CX + 300, 560, 80, (t * 2) % 1)
        g.label("รากฐานของโลกยุคใหม่", CX, 380, 74, sc=ap(t, L[5]), rot=-3)
        return
    if t < L[7] - 0.2:   # GPS + อินเทอร์เน็ต
        if not photo(g, "gps", CX, 780, 860, 560, -2, ap(t, L[6]), 1.04, label="ดาวเทียม GPS"):
            space_panel(g)
            stars(g, t, 16)
            earth(g, CX, 1030, 190, t)
            satellite(g, CX, 560, 0.8, 8 * math.sin(t), t)
            with g.at(860, 1120, ap(t, L[6] + 0.6)):
                g.c.new_path()
                g.c.move_to(0, 60)
                g.c.curve_to(-70, -10, -40, -80, 0, -80)
                g.c.curve_to(40, -80, 70, -10, 0, 60)
                _shade(g.c, RED, 5, 0.2)
                g.circle(0, -30, 18, WHITE, 0)
        g.label("GPS · อินเทอร์เน็ต", CX, 380, 84, color=BLUE, sc=ap(t, L[6]), rot=-3)
        return
    space_panel(g)   # ยานลงจอดบนดาวดวงอื่น
    stars(g, t)
    g.c.save()
    _rr(g.c, 60, 300, 960, 940, 40)
    g.c.clip()
    planet(g, CX, 1350, 420)
    g.c.restore()
    k = e_out(seg(t, L[7], L[7] + 2.4))
    rocket(g, CX, lerp(420, 860, k), 0.7, 180, 1.0 - 0.5 * k, t)
    g.label("ลงจอดได้แม่นยำ!", CX, 380, 84, color=GOLDTXT, sc=ap(t, L[7]), rot=-3)


# ------------------------------------------------------------------ 7. lesson
def s_lesson(g, t, L, d):
    g.ground(GROUND, WHITE)
    g.label("บทเรียน", CX, 340, 100, sc=ap(t, 0.2), rot=-3)
    if t < L[2] - 0.2:   # เรื่องธรรมดาในชีวิตประจำวัน
        ruler(g, CX, 800, 700, ap(t, 0.4), label="1 เมตร")
        if t > L[1] - 0.2:
            g.label("เรื่องธรรมดาที่สุด", CX, 1000, 62, color=GREY, sc=ap(t, L[1]))
        return
    steps = [("1790s", "เมตรแรก"), ("1889", "แท่งโลหะ"), ("1960", "คลื่นแสง"), ("1983", "ความเร็วแสง")]
    for i, (yr, txt) in enumerate(steps):   # ความพยายามนับร้อยปี
        x = 150 + i * 260
        k = ap(t, L[2] + i * 0.6)
        if i:
            g.line([(x - 200, 820), (x - 60, 820)], 8, GREY, amp=0)
        with g.at(x, 820, k):
            g.circle(0, 0, 70, GOLD if i == 3 else WHITE, 6)
            g.text(yr, 0, 0, 34, "kanit", INK)
        g.label(txt, x, 940, 40, sc=k)
    if t > L[3] - 0.2:
        g.sparkle(930, 820, 60 + 8 * math.sin(t * 5), GOLD2)
        g.label("ความจริงที่ไม่เปลี่ยนแปลง", CX, 1120, 62, color=GOLDTXT, sc=ap(t, L[3]))
    else:
        g.label("ความพยายามนับร้อยปี", CX, 1120, 62, color=NAVY, sc=ap(t, L[2]))


# ------------------------------------------------------------------ 8. outro
def s_outro(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[3] - 0.2:   # มองตลับเมตรที่บ้าน ทึ่งขึ้นไหม
        person(g, 260, GROUND, KID, 0.9, mood="shock" if t > L[2] + 1 else "smile", pose="hold", turn=0.4, seed=40)
        tape_measure(g, 470, 1000, 0.6, e_io(seg(t, L[2], L[2] + 2.0)), t)
        if t > L[2] + 1:
            for i in range(4):
                g.sparkle(560 + i * 120, 760 + 30 * math.sin(t * 4 + i), 18, GOLD2)
        g.label("ทึ่งขึ้นไหม?", CX, 380, 90, color=RED, sc=ap(t, L[2]), rot=-3)
        return
    if t < L[5] - 0.2:   # อะไรมั่นคงไม่เปลี่ยนแปลง
        space_panel(g, 60, 420, 1020, 1240)
        stars(g, t, 18, (60, 420, 1020, 1240))
        light_beam(g, 100, 820, 980, 1.0, t, 16)
        for i, s in enumerate(("?", "?", "?")):
            g.label(s, 280 + i * 260, 640 + 20 * math.sin(t * 3 + i), 110, color=GOLD2, sc=ap(t, L[4] + i * 0.3))
        g.label("อะไรที่ไม่เปลี่ยนแปลง?", CX, 360, 72, sc=ap(t, L[3]), rot=-3)
        return
    with g.at(CX + 120, 650, ap(t, L[5])):   # ชวนคอมเมนต์
        g.bubble(0, 0, 520, 240, WHITE, tail=(-1, 1))
        for i in range(3):
            g.circle(-110 + i * 110, 0, 24 + 6 * math.sin(t * 6 - i), INK, 0)
    person(g, 260, GROUND, KID, 0.9, mood="smile", pose="wave", turn=0.3, seed=40, talk=True)
    ruler(g, 700, 1180, 420, 0.8 * ap(t, L[5] + 0.4), label="1 เมตร")
    g.label("คอมเมนต์คุยกันได้เลย!", 700, 1000, 58, color=RED, sc=ap(t, L[5] + 0.4))


SCENES = {
    "hook": s_hook, "bar": s_bar, "risk": s_risk, "paris": s_paris, "define": s_define, "impact": s_impact,
    "lesson": s_lesson, "outro": s_outro,
}
NO_IRIS = set()
