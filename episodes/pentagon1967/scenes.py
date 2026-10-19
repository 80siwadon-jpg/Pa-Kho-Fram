"""ฉากตอน: เดินขบวนสู่เพนตากอน "ดอกไม้ในปลายกระบอกปืน" (21 ต.ค. 1967)
ภาพถ่ายจริง (สาธารณสมบัติ) ผ่าน src/photos.py — ถ้ายังไม่มีไฟล์ภาพ จะวาดการ์ตูนแทนอัตโนมัติ"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from chars import (GEORGE, JAN, OLIVE, PINK, PROTESTERS, SOLDIERS, bouquet, camera_flash, carnation,  # noqa: E402
                   chrysanthemum, coffin, crowd_mass, flag_us, lincoln_memorial, peace_sign, pentagon_top,
                   pentagon_wall, rifle, sign)
from gfx import (GOLD, GOLD2, GREY, INK, LGREY, NAVY, RED, W, WHITE, e_io, e_out, hexc, hn, lerp,  # noqa: E402
                 pop, seg)
from people import _rr, _shade, head, person  # noqa: E402
from photos import photo  # noqa: E402

CX = W / 2
GROUND = 1270
GREEN = hexc("#3c8d4f")
PINKTXT = hexc("#d9608c")
GOLDTXT = hexc("#b37a12")

CAMERA = {"hook": "push_in", "war": "pan_left", "march": "pan_right", "standoff": "push_in", "flower": "pull_out",
          "girl": "push_in", "photo": "tilt_up", "legacy": "pull_out", "outro": "push_in"}
TRANSITIONS = {"war": "fade", "march": "whip", "standoff": "zoom", "flower": "iris", "photo": "fade"}


def ap(t, a, dur=0.38):
    return pop(t, a - 0.2, dur)


def soldier_row(g, t, x0, n, sc=0.62, gap=150, aim=0.0, flowers=0, mood="firm", seed=0, mum_last=False):
    """แถวทหาร (หันขวา) ถือปืน: aim 0 = ถือเฉียงแนบอก, 1 = เล็งตรงไปทางขวา; flowers = จำนวนกระบอกที่มีดอกไม้"""
    for i in range(n):
        x = x0 + i * gap
        lk = SOLDIERS[(i + seed) % len(SOLDIERS)]
        person(g, x, GROUND, lk, sc, mood=mood, pose="hold", turn=0.35, seed=50 + i, shadow=True)
        rot = lerp(-60, -4, aim)
        rx = x + lerp(0, -40, aim) * sc / 0.75
        ry = GROUND - lerp(480, 520, aim) * sc / 0.75
        fk = max(0.0, min(1.0, flowers - i))
        rifle(g, rx, ry, 1.07 * sc, rot, flower=fk, t=t, mum=mum_last and i == n - 1)


# ------------------------------------------------------------------ 1. hook
def s_hook(g, t, L, d):
    if t < L[1] - 0.2:   # วันที่ + เพนตากอนมองบน
        g.ground(GROUND, WHITE)
        pentagon_top(g, CX, 860, 330, t)
        g.label("วันนี้ในอดีต", CX, 380, 104, sc=lerp(2.0, 1, e_out(seg(t, 0.1, 0.4))) if t > 0.1 else 0, rot=-4)
        g.label("21 ตุลาคม 1967", CX, 520, 84, color=RED, sc=pop(t, 0.8))
        return
    if t < L[3] - 0.2:   # หน้าอาคารเพนตากอน ศูนย์บัญชาการทรงอำนาจที่สุด
        g.ground(GROUND, WHITE)
        z = 1.0 + 0.05 * seg(t, L[1], L[3])
        if not photo(g, "pentagon", CX, 780, 860, 600, -2, ap(t, L[1]), z, label="เพนตากอน · รัฐเวอร์จิเนีย สหรัฐฯ"):
            pentagon_top(g, CX, 800, 360, t, ap(t, L[1]))
            g.label("เพนตากอน", CX, 1170, 70, sc=ap(t, L[1] + 0.3))
        if t > L[2] - 0.2:
            g.label("ทรงอำนาจที่สุดในโลก", CX, 380, 76, color=NAVY, sc=ap(t, L[2]), rot=-3)
        return
    if t < L[4] - 0.2:   # สมรภูมินองเลือด?
        g.ground(GROUND, WHITE)
        pentagon_wall(g, GROUND, t)
        for i in range(2):
            a = 0.5 + 0.5 * math.sin(t * 6 + i * math.pi)
            g.circle(160 + i * 760, 520, 60, (0.85, 0.2, 0.2, 0.3 + 0.5 * a), 6)
        g.label("สมรภูมินองเลือด?", CX, 380, 90, color=RED, sc=ap(t, L[3]), rot=-4)
        return
    if t < L[5] - 0.2:   # ฝูงชนเรือนหมื่นประชิดรั้ว
        g.ground(GROUND, WHITE)
        k = e_out(seg(t, L[4] - 0.2, L[4] + 1.6))
        with g.at(lerp(500, 0, k), 0):
            crowd_mass(g, 300, 1500, GROUND, t, rows=6)
        for i in range(9):   # แนวรั้ว
            g.line([(60 + i * 40, GROUND), (60 + i * 40, GROUND - 200)], 6, GREY, amp=0)
        g.line([(40, GROUND - 190), (420, GROUND - 190)], 6, GREY, amp=0)
        g.label("ฝูงชนเรือนหมื่น", CX, 380, 84, sc=ap(t, L[4]), rot=-3)
        return
    if t < L[7] - 0.2:   # ทหารติดอาวุธครบมือ เล็งเข้าใส่
        g.ground(GROUND, WHITE)
        soldier_row(g, t, 110, 5, 0.6, 160, aim=e_io(seg(t, L[6] - 0.2, L[6] + 1.0)))
        g.label("ติดอาวุธครบมือ", CX, 380, 84, color=OLIVE, sc=ap(t, L[5]), rot=-3)
        if t > L[6] - 0.2:
            g.label("ดาบปลายปืน", 820, 560, 56, color=RED, sc=ap(t, L[6] + 0.6))
        return
    if t < L[8] - 0.2:   # กระสุนนัดแรก?
        g.ground(GROUND, WHITE)
        shake = 3 * math.sin(t * 40) * seg(t, L[7] + 1.0, L[8])
        rifle(g, 260 + shake, 800, 1.9, 0, bayonet=True)
        g.label("นัดแรก...?", CX, 380, 96, color=RED, sc=ap(t, L[7]), rot=-4)
        for i in range(3):
            g.circle(860 + i * 50, 800, 10 + 4 * i, (0.85, 0.2, 0.2, 0.25 + 0.2 * i), 0)
        return
    if t < L[9] - 0.2:   # ไม่ใช่หินหรือระเบิด
        g.ground(GROUND, WHITE)
        g.blob(320, 800, 130, 100, GREY, 7, 3)
        with g.at(760, 800):
            g.circle(0, 0, 110, INK, 0)
            g.line([(60, -80), (100, -150)], 10, hexc("#a8763e"), amp=0)
        for x in (320, 760):
            g.line([(x - 150, 650), (x + 150, 950)], 18, RED, amp=0)
            g.line([(x + 150, 650), (x - 150, 950)], 18, RED, amp=0)
        g.label("ไม่ใช่หิน · ไม่ใช่ระเบิด", CX, 380, 76, sc=ap(t, L[8]), rot=-3)
        return
    g.ground(GROUND, WHITE)   # แต่คือดอกไม้!
    k = e_out(seg(t, L[9] - 0.2, L[9] + 0.6))
    g.sunburst(CX, 760, 240, 600, 22, t * 10, 12, (0.98, 0.75, 0.85, 0.7 * k))
    rifle(g, 180, 820, 1.7, -8, flower=k, t=t)
    for i in range(5):
        a = t * 1.3 + i * 1.26
        carnation(g, CX + 360 * math.cos(a), 760 + 300 * math.sin(a), 0.5 * k, t)
    g.label('"ดอกไม้"!', CX, 380, 110, color=PINKTXT, sc=ap(t, L[9]), rot=-4)


# ------------------------------------------------------------------ 2. war
def s_war(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:
        g.calendar(CX, 760, 1.5, "1967", "สงครามเวียดนาม", "ย้อนกลับไป")
        return
    if t < L[2] - 0.2:   # กลืนกินชีวิตวัยรุ่น: ทหารหนุ่มเดินหายเข้าหมอก
        for i in range(5):
            u = ((t - L[1]) * 0.12 + i / 5) % 1
            x = lerp(80, 900, u)
            with g.alpha(1 - u):
                person(g, x, GROUND, SOLDIERS[i % 4], 0.5 + 0.15 * (1 - u), mood="worry", turn=0.5, seed=60 + i)
        g.label("สงครามเวียดนาม", CX, 380, 84, color=OLIVE, sc=ap(t, L[1]), rot=-3)
        g.label("วันแล้ววันเล่า", CX, 500, 60, color=GREY, sc=ap(t, L[1] + 1.0))
        return
    if t < L[3] - 0.2:   # โลงศพคลุมธงชาติ
        for i in range(3):
            coffin(g, CX + (i - 1) * 60, GROUND - i * 120, 1.2 - 0.15 * i)
        for i in range(3):
            g.sparkle(200 + i * 340, 520 + 20 * math.sin(t * 2 + i), 12, WHITE)
        g.label("กลับบ้านไม่เว้นแต่ละวัน", CX, 380, 70, color=NAVY, sc=ap(t, L[2]), rot=-3)
        return
    for i, lk in enumerate(PROTESTERS[:3]):   # โกรธแค้นและคราบน้ำตา
        x = 190 + i * 340
        person(g, x, GROUND, lk, 0.66, mood="sad" if i == 1 else "angry", pose="fist" if i != 1 else "down",
               turn=0.2 * (1 - i), seed=70 + i, talk=i != 1)
    sign(g, 900, 560, "STOP THE WAR", 0.7, 6 * math.sin(t))
    g.label("ปะทุถึงขีดสุด!", CX, 380, 84, color=RED, sc=ap(t, L[3]), rot=-4)


# ------------------------------------------------------------------ 3. march
def s_march(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:   # กว่าหนึ่งแสนคนที่วอชิงตัน
        if not photo(g, "rally", CX, 760, 860, 600, 2, ap(t, 0.2), 1.0 + 0.05 * seg(t, 0, L[1]),
                     label="ชุมนุมที่อนุสรณ์สถานลินคอล์น 21 ต.ค. 1967"):
            lincoln_memorial(g, CX, 980, 1.1)
            crowd_mass(g, -100, 1200, GROUND, t, rows=5)
        n = int(lerp(0, 100000, e_io(seg(t, 0.2, L[1] - 0.6))))
        g.label(f"{n:,} คน" if n < 100000 else "กว่า 100,000 คน", CX, 380, 90, color=RED, sc=ap(t, 0.2))
        return
    if t < L[3] - 0.2:   # ห้าหมื่นคนเดินขบวนไปเพนตากอน
        if t > L[2] - 0.2 and photo(g, "march", CX, 760, 860, 600, -2, ap(t, L[2]), 1.0 + 0.05 * seg(t, L[2], L[3]),
                                    label="ผู้ชุมนุมหน้าเพนตากอน 21 ต.ค. 1967"):
            g.label("ปิดล้อมเพนตากอน", CX, 380, 80, color=NAVY, sc=ap(t, L[2]), rot=-3)
            return
        pentagon_top(g, 860, 760, 150, t)
        g.label("ดี.ซี.", 180, 1000, 56)
        k = e_io(seg(t, L[1], L[2] + 1.0))
        pts = [(lerp(200, 720, u), 960 - 200 * u - 60 * math.sin(u * math.pi)) for u in [i / 30 * k for i in range(31)]]
        g.line(pts, 16, RED, amp=0)
        for i in range(8):   # คลื่นคนเดินตามเส้นทาง
            u = ((t * 0.15 + i / 8) % 1) * k
            g.circle(lerp(200, 720, u), 960 - 200 * u - 60 * math.sin(u * math.pi) - 20, 14, NAVY, 3)
        g.label("กว่า 50,000 คน", CX, 380, 84, color=RED, sc=ap(t, L[1]), rot=-3)
        g.label("ปิดล้อมเพนตากอน", CX, 1150, 62, sc=ap(t, L[2]))
        return
    for i, lk in enumerate(PROTESTERS[1:4]):   # หยุดส่งลูกหลานไปตาย
        x = 190 + i * 340
        person(g, x, GROUND, lk, 0.62, mood="shout", pose="sign" if i == 1 else "fist", turn=0.2 * (1 - i),
               seed=80 + i, talk=True)
    sign(g, CX, 640, "BRING THEM HOME", 0.8, -4 + 3 * math.sin(t * 2))
    g.label("หยุดส่งลูกหลานไปตาย!", CX, 380, 74, color=RED, sc=ap(t, L[3]), rot=-3)


# ------------------------------------------------------------------ 4. standoff
def s_standoff(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:   # ตึงเครียดจนแทบหยุดหายใจ
        pentagon_wall(g, GROUND, t)
        beat = 1 + 0.15 * max(0, math.sin(t * 7)) ** 6
        g.label("ตึงเครียด...", CX, 760, 110 * beat, color=RED, sc=ap(t, 0.2), rot=-3)
        return
    if t < L[3] - 0.2:   # สารวัตรทหาร + กองกำลังพิทักษ์มาตุภูมิ ตั้งกำแพงมนุษย์
        if t > L[2] - 0.2 and photo(g, "line", CX, 760, 860, 600, 2, ap(t, L[2]), 1.0 + 0.05 * seg(t, L[2], L[3]),
                                    label="แนวทหารหน้าเพนตากอน 1967"):
            g.label("กำแพงมนุษย์", CX, 380, 84, color=OLIVE, sc=ap(t, L[2]), rot=-3)
            return
        soldier_row(g, t, 120, 5, 0.6, 165)
        g.label("สารวัตรทหาร + กองกำลังพิทักษ์ฯ", CX, 380, 62, color=OLIVE, sc=ap(t, L[1]), rot=-3)
        if t > L[2] - 0.2:
            g.label("กำแพงมนุษย์", CX, 500, 70, sc=ap(t, L[2]))
        return
    if t < L[5] - 0.2:   # เรียงแถวหน้ากระดาน ยกปืนเล็ง
        aim = e_io(seg(t, L[4] - 0.2, L[4] + 1.2))
        soldier_row(g, t, 90, 3, 0.62, 160, aim=aim)
        crowd_mass(g, 700, 1300, GROUND, t, rows=5)
        if t < L[4] - 0.2:
            g.label("เรียงแถวหน้ากระดาน", CX, 380, 76, color=OLIVE, sc=ap(t, L[3]), rot=-3)
        else:
            g.label("ระยะเผาขน!", CX, 380, 90, color=RED, sc=ap(t, L[4]), rot=-4)
        return
    if t < L[7] - 0.2:   # แววตากดดัน / ขยับผิดจังหวะ
        with g.at(270, 760, 1.6):
            head(g, SOLDIERS[0], "firm", turn=0.4, look_at=(1, 0))
        with g.at(810, 760, 1.6):
            head(g, PROTESTERS[0], "worry", turn=-0.4, look_at=(-1, 0))
        for i in range(3):
            g.sweat(380 + i * 20, 560 + ((t * 0.8 + i / 3) % 1) * 80, 1.3)
        if t < L[6] - 0.2:
            g.label("ความเงียบงัน...", CX, 380, 84, color=GREY, sc=ap(t, L[5]), rot=-3)
        else:
            g.label("ขยับผิดจังหวะ = ?", CX, 380, 80, color=RED, sc=ap(t, L[6]), rot=-3)
        return
    pentagon_wall(g, GROUND, t)   # โศกนาฏกรรมรออยู่
    with g.alpha(0.3 + 0.1 * math.sin(t * 4)):
        _rr(g.c, -400, 300, 1880, 1000, 0)
        _shade(g.c, (0.16, 0.18, 0.28, 1), 0, 0)
    g.label("โศกนาฏกรรม?", CX, 760, 100, color=RED, sc=ap(t, L[7]), rot=-3)


# ------------------------------------------------------------------ 5. flower
def s_flower(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:   # ท่ามกลางความหวาดกลัว
        soldier_row(g, t, 90, 3, 0.6, 160, aim=1.0)
        crowd_mass(g, 700, 1300, GROUND, t, rows=5)
        g.label("แต่แล้ว...", CX, 380, 96, sc=ap(t, 0.2), rot=-3)
        return
    if t < L[4] - 0.2:   # วัยรุ่นชายก้าวออกมา ไม่มีอาวุธ มีแต่ดอกคาร์เนชัน
        step = e_out(seg(t, L[1], L[1] + 1.4))
        person(g, lerp(900, 640, step), GROUND, GEORGE, 0.8, mood="firm", pose="down" if t < L[3] else "hold",
               turn=-0.3, seed=1)
        soldier_row(g, t, 90, 2, 0.6, 170, aim=1.0)
        g.name_tag(t, L[1] + 0.6, 780, 440, "จอร์จ แฮร์ริส", "วัยรุ่นอายุ 18 ปี", side=1)
        if t > L[2] - 0.2 and t < L[3] - 0.2:
            g.label("มือเปล่า · ไม่มีอาวุธ", CX, 1180, 60, color=GREY, sc=ap(t, L[2]))
        if t > L[3] - 0.2:
            bouquet(g, 720, 980, 0.9 * ap(t, L[3]), t)
            g.label("คาร์เนชันสีชมพู", CX, 1180, 64, color=PINKTXT, sc=ap(t, L[3] + 0.4))
        return
    # เสียบดอกไม้ลงในลำกล้องทีละกระบอก
    n = 0 if t < L[5] else 1 + (t - L[5]) / 1.6
    soldier_row(g, t, 120, 4, 0.58, 150, aim=0.0, flowers=n, mood="worry")
    reach = e_io(seg(t, L[4], L[4] + 1.6))
    gx = lerp(880, 820 - min(3, int(n)) * 0, reach)
    person(g, gx, GROUND, GEORGE, 0.62, mood="smile", pose="point" if t < L[5] else "hold", turn=-0.4, seed=1)
    if t < L[5] - 0.2:
        g.label("ปลายกระบอกปืนที่เย็นเฉียบ", CX, 380, 64, color=NAVY, sc=ap(t, L[4]), rot=-3)
    else:
        g.label("ทีละกระบอก...", CX, 380, 84, color=PINKTXT, sc=ap(t, L[5]), rot=-3)


# ------------------------------------------------------------------ 6. girl
def s_girl(g, t, L, d):
    g.ground(GROUND, WHITE)
    soldier_row(g, t, 140, 2, 0.66, 180, aim=0.15, flowers=2, mood="neutral")
    person(g, 760, GROUND, JAN, 0.72, mood="smile", pose="hold", turn=-0.4, look_at=(-1, -0.2), seed=2)
    chrysanthemum(g, 650, 760, 0.9 * ap(t, 0.4), t)
    g.name_tag(t, 0.6, 790, 420, "แจน โรส แคสเมียร์", "เด็กสาวอายุ 17 ปี", side=1)
    if t > L[1] - 0.2:
        g.line([(480, 640), (640, 640)], 6, RED, amp=0)
        g.label("ห่างไม่กี่นิ้ว", 560, 1180, 62, color=RED, sc=ap(t, L[1] + 0.3))
        g.label("ดอกเบญจมาศ", 760, 1060, 60, color=GOLDTXT, sc=ap(t, L[1]))
    if t > L[2] - 0.2:
        for i in range(4):
            g.sparkle(560 + 140 * math.cos(t * 1.5 + i * 1.57), 600 + 90 * math.sin(t * 1.5 + i * 1.57), 14, PINK)
        g.label("แววตาแห่งความเมตตา", CX, 380, 70, color=PINKTXT, sc=ap(t, L[2]), rot=-3)


# ------------------------------------------------------------------ 7. photo
def s_photo(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:   # ช่างภาพกดชัตเตอร์
        fl = max(0.0, 1 - abs(t - 2.4) / 0.35)
        camera_flash(g, CX, 800, 1.6, fl)
        g.label("แชะ!", 760, 520, 90, color=RED, sc=ap(t, 2.3), rot=-8)
        g.label("ช่างภาพในเหตุการณ์", CX, 380, 72, sc=ap(t, 0.2), rot=-3)
        return
    if t < L[2] - 0.2:   # ภาพสะเทือนอารมณ์คนทั้งโลก (วาดจำลอง — ภาพต้นฉบับมีลิขสิทธิ์)
        k = ap(t, L[1])
        with g.at(CX, 780, k, -3):
            g.rrect(-430, -330, 860, 700, 12, WHITE, 6)
            g.c.save()
            g.c.rectangle(-400, -300, 800, 560)
            g.c.clip()
            g.rrect(-400, -300, 800, 560, 0, hexc("#e9e4da"), 0)
            for i in range(3):
                rifle(g, -330, -150 + i * 120, 0.9, -6, flower=1.0, t=t)
            person(g, 300, 240, GEORGE, 0.5, mood="smile", pose="hold", turn=-0.4, seed=1, shadow=False)
            g.c.restore()
            g.text("ภาพวาดจำลองเหตุการณ์", 0, 315, 30, "kanitm", GREY)
        for i in range(5):
            g.sparkle(140 + i * 200, 1200 + 20 * math.sin(t * 3 + i), 16 * ap(t, L[1] + 0.5 + i * 0.15))
        g.label("สะเทือนใจคนทั้งโลก!", CX, 380, 80, color=RED, sc=ap(t, L[1]), rot=-3)
        return
    if t < L[4] - 0.2:   # ทั้งสองฝ่ายวัยเดียวกัน
        with g.at(280, 780, 1.6):
            head(g, GEORGE, "smile", turn=0.3)
        with g.at(800, 780, 1.6):
            head(g, SOLDIERS[0], "worry", turn=-0.3)
        g.label("=", CX, 780, 120, sc=ap(t, L[2] + 0.4))
        if t < L[3] - 0.2:
            g.label("คนถือดอกไม้ · คนถือปืน", CX, 380, 68, sc=ap(t, L[2]), rot=-3)
        else:
            g.label("วัยเดียวกัน!", CX, 380, 96, color=RED, sc=ap(t, L[3]), rot=-4)
            g.label("ราว 18–20 ปี", CX, 1150, 62, color=GREY, sc=ap(t, L[3] + 0.5))
        return
    if t < L[5] - 0.2:   # ฝ่ายหนึ่งสู้เพื่อเพื่อน
        for i, lk in enumerate(PROTESTERS[:3]):
            person(g, 190 + i * 340, GROUND, lk, 0.62, mood="firm", pose="sign" if i == 1 else "fist",
                   turn=0.2 * (1 - i), seed=90 + i)
        peace_sign(g, CX, 560, 90, k=ap(t, L[4] + 0.3))
        g.label("ไม่ให้เพื่อนต้องไปตาย", CX, 380, 70, color=NAVY, sc=ap(t, L[4]), rot=-3)
        return
    sad = seg(t, L[6] - 0.2, L[6] + 0.8)   # อีกฝ่ายจำใจทำตามคำสั่ง
    person(g, CX - 60, GROUND, SOLDIERS[2], 0.85, mood="sad" if sad > 0.5 else "worry", pose="hold", turn=0.2, seed=3)
    rifle(g, CX - 60, GROUND - 544, 0.91, lerp(-60, -75, sad), t=t)
    if t < L[6] - 0.2:
        g.label("จำใจทำตามคำสั่ง", CX, 380, 76, color=OLIVE, sc=ap(t, L[5]), rot=-3)
    else:
        g.label("ไม่อยากเหนี่ยวไก", CX, 380, 76, color=NAVY, sc=ap(t, L[6]), rot=-3)
        for i in range(2):
            g.sweat(CX - 10 + i * 20, 560 + ((t * 0.6 + i / 2) % 1) * 60, 1.1)


# ------------------------------------------------------------------ 8. legacy
def s_legacy(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # ดอกไม้ไม่กี่ดอก ปลดอาวุธกองทัพ
        for i in range(4):
            rifle(g, 140, 560 + i * 150, 1.1, -4 * (i - 1.5), flower=ap(t, 0.3 + i * 0.4), t=t, mum=i == 3)
        if t < L[1] - 0.2:
            g.label("ดอกไม้ไม่กี่ดอก", CX, 380, 84, color=PINKTXT, sc=ap(t, 0.2), rot=-3)
        else:
            g.label("ปลดอาวุธกองทัพ!", CX, 380, 84, color=GREEN, sc=ap(t, L[1]), rot=-4)
        return
    k = ap(t, L[2])   # สัญลักษณ์แห่งสันติภาพ
    g.sunburst(CX, 780, 220, 560, 20, t * 8, 10, (0.98, 0.8, 0.88, 0.6))
    peace_sign(g, CX, 780, 200, k=k)
    for i in range(8):
        a = t * 0.6 + i * math.pi / 4
        carnation(g, CX + 300 * math.cos(a), 780 + 300 * math.sin(a), 0.45 * k, t) if i % 2 else \
            chrysanthemum(g, CX + 300 * math.cos(a), 780 + 300 * math.sin(a), 0.45 * k, t)
    if t < L[3] - 0.2:
        g.label("สัญลักษณ์แห่งสันติภาพ", CX, 380, 74, sc=ap(t, L[2]), rot=-3)
    else:
        g.label("ความอ่อนโยน", CX, 340, 80, color=PINKTXT, sc=ap(t, L[3]), rot=-3)
        g.label("ชนะความรุนแรง", CX, 450, 70, color=GREEN, sc=ap(t, L[3] + 0.4))


# ------------------------------------------------------------------ 9. outro
def s_outro(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[3] - 0.2:   # ถ้าคุณเป็นทหาร...
        person(g, 300, GROUND, SOLDIERS[1], 0.8, mood="worry" if t < L[2] else "sad", pose="hold", turn=0.35, seed=4)
        rifle(g, 300, GROUND - 512, 0.86, lerp(-60, -45, seg(t, L[1], L[1] + 1)), flower=ap(t, L[1] + 0.6), t=t)
        for i in range(5):   # กลีบดอกไม้ปลิว
            u = (t * 0.12 + i / 5) % 1
            carnation(g, lerp(1100, 450, u), 520 + i * 110 + 40 * math.sin(t * 2 + i), 0.22, t * 3 + i)
        if t < L[2] - 0.2:
            g.label("ถ้าคุณเป็นทหาร...", CX, 380, 80, sc=ap(t, 0.2), rot=-3)
        else:
            for i in range(3):
                g.label("?", 620 + i * 110, 640 + 20 * math.sin(t * 3 + i), 110, color=RED, sc=ap(t, L[2] + i * 0.2))
            g.label("รู้สึกอย่างไร?", CX, 380, 84, color=RED, sc=ap(t, L[2]), rot=-3)
        return
    if t < L[5] - 0.2:   # อ่อนโยน vs รุนแรง ชนะทุกครั้ง?
        tilt = 8 * math.sin(t * 1.2)
        with g.at(CX, 760, 1, tilt):
            g.line([(-340, 0), (340, 0)], 12, INK, amp=0)
            carnation(g, -300, -80, 0.9, t)
            g.c.new_path()
            g.c.arc(300, -60, 70, 0, 2 * math.pi)
            _shade(g.c, GREY, 6, 0.2)
        g.poly([(CX - 40, 1180), (CX, 770), (CX + 40, 1180)], hexc("#a8763e"), 6)
        g.label("ชนะได้ทุกครั้งจริงไหม?", CX, 380, 70, color=NAVY, sc=ap(t, L[3]), rot=-3)
        return
    with g.at(CX + 120, 650, ap(t, L[5])):   # ชวนคอมเมนต์
        g.bubble(0, 0, 520, 240, WHITE, tail=(-1, 1))
        for i in range(3):
            g.circle(-110 + i * 110, 0, 24 + 6 * math.sin(t * 6 - i), INK, 0)
    person(g, 250, GROUND, GEORGE, 0.75, mood="smile", pose="wave", turn=0.3, seed=1, talk=True)
    for i in range(5):
        carnation(g, 160 + i * 190, 1190 + 15 * math.sin(t * 3 + i), 0.35 * ap(t, L[5] + 0.5 + i * 0.2), t)
    g.label("คอมเมนต์คุยกันได้เลย!", 750, 1150, 56, color=RED, sc=ap(t, L[5] + 0.4))


SCENES = {
    "hook": s_hook, "war": s_war, "march": s_march, "standoff": s_standoff, "flower": s_flower, "girl": s_girl,
    "photo": s_photo, "legacy": s_legacy, "outro": s_outro,
}
NO_IRIS = set()
