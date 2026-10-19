"""ฉากตอน: ยุทธการเอล-อาลาเมนครั้งที่สอง (23 ต.ค. 1942) — ไม่แสดงความรุนแรง ใช้แสงวาบ/ควัน/ฝุ่นแทน"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from chars import (CHURCHILL, MONTY, ROMMEL, SAND, SAND2, TOMMY, artillery, blast, bolt, chess_piece,  # noqa: E402
                   derrick, dunes, egypt_map, jerrycan, mine, night_sky, smoke, storm, tank, warn_sign)
from gfx import GOLD, GOLD2, GREY, INK, NAVY, RED, W, WHITE, e_io, e_out, hexc, lerp, pop, seg  # noqa: E402
from people import person  # noqa: E402

CX = W / 2
GROUND = 1270
GOLDTXT = hexc("#b37a12")
GREEN = hexc("#3c8d4f")
DE = hexc("#5a5448")

CAMERA = {"hook": "push_in", "rommel": "pan_right", "monty": "push_in", "mines": "tilt_down", "battle": "dutch",
          "fuel": "pan_left", "churchill": "push_in", "lesson": "pull_out", "outro": "pan_right"}
TRANSITIONS = {"rommel": "whip", "monty": "zoom", "mines": "fade", "battle": "whip", "fuel": "iris",
               "churchill": "zoom", "lesson": "fade", "outro": "whip"}


def ap(t, a, dur=0.38):
    return pop(t, a - 0.2, dur)


def desert(g, t=0.0):
    dunes(g, GROUND - 120, t, SAND2)
    g.ground(GROUND, WHITE)   # พื้นล่างขาว (สไตล์ช่อง) เหลือแค่แนวเนินทราย


def rommel(g, x, sc=0.85, mood="smug", pose="down", turn=0.2, pose2=None, k=0.0, talk=False):
    person(g, x, GROUND, ROMMEL, sc, mood=mood, pose=pose, pose2=pose2, k=k, turn=turn, seed=3, talk=talk)


def monty(g, x, sc=0.85, mood="firm", pose="down", turn=-0.2, pose2=None, k=0.0, talk=False):
    person(g, x, GROUND, MONTY, sc, mood=mood, pose=pose, pose2=pose2, k=k, turn=turn, seed=7, talk=talk)


def flashes(g, t, t0, n=5, y=1150, seed=0):
    """แสงวาบปืนใหญ่ตามแนวขอบฟ้า (เป็นจังหวะ)"""
    for i in range(n):
        ph = ((t - t0) * 1.3 + i * 0.37 + seed) % 1
        blast(g, 80 + i * 230 + 30 * math.sin(i * 3), y - 20 * (i % 2), 90, ph)


# ------------------------------------------------------------------ 1. hook
def s_hook(g, t, L, d):
    if t < L[5] - 0.2:   # ค่ำคืนในทะเลทราย -> ฟ้าสว่างวาบ -> ปืนใหญ่ -> ชื่อยุทธการ
        fl = 0.0
        if t > L[2] - 0.2:
            fl = 0.55 + 0.45 * abs(math.sin((t - L[2]) * 5))
        night_sky(g, 1.0, fl)
        for i in range(12):   # ดาว
            g.sparkle(60 + i * 90, 260 + (i * 137) % 500, 9 + 3 * math.sin(t * 3 + i), (1, 1, 1, 0.8 * (1 - fl)), 0)
        desert(g, t)
        if t < L[2] - 0.2:
            g.label("วันนี้ในอดีต", CX, 380, 104, sc=lerp(2.0, 1, e_out(seg(t, 0.1, 0.4))) if t > 0.1 else 0, rot=-3)
            g.label("23 ตุลาคม 1942", CX, 520, 84, color=GOLDTXT, sc=pop(t, 0.8))
            if t > L[1] - 0.2:
                g.label("ทะเลทรายอียิปต์", CX, 1120, 64, color=NAVY, sc=ap(t, L[1]))
            return
        for i in range(4):
            artillery(g, 150 + i * 260, GROUND + 10, 0.7, t, fire=max(0.0, math.sin((t - L[2]) * 5 + i * 1.3)))
        flashes(g, t, L[2], 4, 900)
        if t < L[3] - 0.2:
            g.label("สว่างวาบราวกลางวัน!", CX, 380, 84, color=GOLDTXT, sc=ap(t, L[2]), rot=-3)
        elif t < L[4] - 0.2:
            g.label("ปืนใหญ่นับพันกระบอก!", CX, 380, 84, color=RED, sc=ap(t, L[3]), rot=-3)
        else:
            g.label("ยุทธการเอล-อาลาเมน", CX, 360, 92, color=GOLDTXT, sc=ap(t, L[4]), rot=-3)
            g.label("ครั้งที่สอง", CX, 490, 72, color=GOLDTXT, sc=ap(t, L[4] + 0.4))
        return
    desert(g, t)
    if t < L[6] - 0.2:   # ศึกชี้ชะตาสงครามโลก
        tank(g, 280, GROUND - 10, 0.75, "uk", t, turret=-3)
        tank(g, 820, GROUND - 10, 0.75, "de", t, flip=True, turret=-3)
        with g.at(CX, 760, ap(t, L[5])):
            g.rrect(-90, -90, 180, 180, 90, WHITE, 7)
            g.label("VS", 0, 0, 80, color=RED)
        g.label("ศึกชี้ชะตาสงครามโลก!", CX, 380, 84, color=RED, sc=ap(t, L[5]), rot=-3)
        return
    if t < L[7] - 0.2:   # เดิมพันบ่อน้ำมัน
        derrick(g, 330, GROUND, 1.2 * ap(t, L[6]), t)
        derrick(g, 760, GROUND, 0.9 * ap(t, L[6] + 0.3), t)
        g.label("เดิมพัน: บ่อน้ำมัน", CX, 380, 86, color=GOLDTXT, sc=ap(t, L[6]), rot=-3)
        g.label("ตะวันออกกลาง", CX, 520, 60, color=GREY, sc=ap(t, L[6] + 0.4))
        return
    for i, lk in enumerate(TOMMY):   # ลมหายใจสุดท้ายของสัมพันธมิตร
        person(g, 330 + i * 400, GROUND, lk, 0.75, mood="worry", pose="down", turn=0.2 - 0.4 * i, seed=10 + i)
    g.sweat(330 + 60, GROUND - 720, 1.0 + 0.1 * math.sin(t * 6))
    g.label("ลมหายใจสุดท้าย", CX, 380, 92, color=RED, sc=ap(t, L[7]), rot=-3)
    g.label("ของฝ่ายสัมพันธมิตร", CX, 520, 62, color=NAVY, sc=ap(t, L[7] + 0.3))


# ------------------------------------------------------------------ 2. rommel
def s_rommel(g, t, L, d):
    desert(g, t)
    if t < L[2] - 0.2:   # จิ้งจอกทะเลทราย เออร์วิน รอมเมล ไร้เทียมทาน
        tank(g, 820, GROUND - 10, 0.7, "de", t, flip=True)
        rommel(g, 330, 0.76, mood="smug", pose="point" if t > L[1] else "down", turn=0.3)
        g.name_tag(t, L[1] - 0.1, 760, 1100, "เออร์วิน รอมเมล", "จอมพลเยอรมัน (1891–1944)", side=-1)
        if t < L[1] - 0.2:
            g.label('"จิ้งจอกทะเลทราย"', CX, 360, 90, color=GOLDTXT, sc=ap(t, 0.2), rot=-3)
        else:
            g.label("ไร้เทียมทาน!", CX, 360, 100, color=RED, sc=ap(t, L[1]), rot=-3)
        return
    if t < L[4] - 0.2:   # รุกคืบจ่อคอหอยอียิปต์ ใกล้คลองสุเอซ
        egypt_map(g, CX, 780, 1.0, t, arrow=e_io(seg(t, L[2], L[2] + 2.0)), suez=t > L[3] - 0.2)
        if t > L[3] - 0.2:
            g.label("ใกล้คลองสุเอซแค่เอื้อม!", CX, 360, 76, color=RED, sc=ap(t, L[3]), rot=-3)
        else:
            g.label("รุกคืบจ่อคอหอยอียิปต์", CX, 360, 78, color=RED, sc=ap(t, L[2]), rot=-3)
        return
    if t < L[5] - 0.2:   # ยึดแหล่งน้ำมัน
        derrick(g, 280, GROUND, 1.0, t)
        derrick(g, 640, GROUND, 0.8, t)
        with g.at(800, 700, ap(t, L[4] + 0.4), 8):
            g.rrect(-150, -70, 300, 140, 20, WHITE, 7, stroke=RED)
            g.label("ยึด!", 0, 0, 80, color=RED)
        g.label("หากจุดนี้แตก...", CX, 360, 84, sc=ap(t, L[4]), rot=-3)
        return
    for i in range(3):   # ตัดเส้นทางเสบียงอังกฤษ
        x = (220 + i * 340 + (t - L[5]) * 90) % 1300 - 100
        jerrycan(g, x, GROUND - 20, 0.6, 3 * math.sin(t * 2 + i), col=hexc("#9a8a5a"))
    k = e_out(seg(t, L[5] + 0.3, L[5] + 1.0))
    g.line([(80, 980), (1000, 980)], 10, GREY, amp=0)
    with g.at(CX, 980, 1.6 * k, 20):
        g.line([(-70, -70), (70, 70)], 18, RED, amp=0)
        g.line([(-70, 70), (70, -70)], 18, RED, amp=0)
    g.label("ตัดเส้นทางเสบียงอังกฤษ", CX, 360, 76, color=RED, sc=ap(t, L[5]), rot=-3)


# ------------------------------------------------------------------ 3. monty
def s_monty(g, t, L, d):
    desert(g, t)
    if t < L[3] - 0.2:
        g.sunburst(CX, 760, 260, 640, 20, t * 8, 10, (0.95, 0.85, 0.55, 0.5 * ap(t, L[1])))
        monty(g, CX, 0.8, mood="neutral" if t < L[1] else "firm", pose="cross" if t > L[2] else "down", turn=0.0)
        g.name_tag(t, L[1] + 0.1, 800, 1120, "เบอร์นาร์ด มอนต์โกเมอรี", "แม่ทัพกองทัพที่ 8 อังกฤษ", side=-1)
        if t < L[1] - 0.2:
            g.label("ความหวังสุดท้าย", CX, 360, 96, color=NAVY, sc=ap(t, 0.2), rot=-3)
        elif t < L[2] - 0.2:
            g.label("นายพลมอนต์โกเมอรี", CX, 360, 88, color=GOLDTXT, sc=ap(t, L[1]), rot=-3)
        else:
            g.label("กองทัพที่ 8 อังกฤษ", CX, 360, 88, color=NAVY, sc=ap(t, L[2]), rot=-3)
        return
    monty(g, 260, 0.85, mood="firm", pose="point", turn=0.3)   # หยุดปีศาจแห่งทะเลทราย
    rommel(g, 860, 0.8, mood="smug", pose="cross", turn=-0.3)
    with g.at(CX + 30, 640, ap(t, L[3] + 0.3)):
        g.rrect(-110, -80, 220, 160, 30, WHITE, 7, stroke=RED)
        g.label("หยุด!", 0, 0, 72, color=RED)
    g.label("หยุดปีศาจแห่งทะเลทราย", CX, 360, 78, color=RED, sc=ap(t, L[3]), rot=-3)


# ------------------------------------------------------------------ 4. mines
def s_mines(g, t, L, d):
    desert(g, t)
    if t < L[1] - 0.2:   # ไม่ใช่แค่กองทัพเยอรมัน
        for i in range(3):
            tank(g, 200 + i * 340, GROUND - 10, 0.55, "de", t, flip=True, move=False)
        g.label("ไม่ใช่แค่กองทัพเยอรมัน...", CX, 380, 78, sc=ap(t, 0.2), rot=-3)
        return
    if t < L[3] - 0.2:   # สวนปีศาจ: ทุ่งกับระเบิดนับแสน
        for r in range(3):
            for i in range(5):
                x = 120 + i * 210 + (r % 2) * 100
                y = GROUND - 30 + r * 55
                mine(g, x, y, 0.65 * ap(t, L[1] + 0.06 * (i + r * 5)), 0.4)
        warn_sign(g, 860, GROUND - 120, 0.9 * ap(t, L[1] + 0.3), 4 * math.sin(t * 2))
        if t < L[2] - 0.2:
            g.label('"สวนปีศาจ"', CX, 380, 110, color=RED, sc=ap(t, L[1]), rot=-3)
        else:
            g.label("กับระเบิดนับแสนลูก!", CX, 380, 86, color=RED, sc=ap(t, L[2]), rot=-3)
            g.label("ที่รอมเมลฝังไว้", CX, 520, 58, color=GREY, sc=ap(t, L[2] + 0.5))
        return
    if t < L[4] - 0.2:   # พายุทราย + แดดแผดเผา
        g.sunburst(830, 560, 110, 230, 14, t * 15, 10, (0.98, 0.7, 0.3, 0.8))
        g.circle(830, 560, 100, hexc("#f6a845"), 6)
        storm(g, 330, 780, 1.2, t)
        for i in range(10):
            u = (t * 0.8 + i * 0.1) % 1
            g.line([(-100 + u * 1300, 620 + i * 60), (-20 + u * 1300, 620 + i * 60)], 5, (0.75, 0.62, 0.38, 0.7), amp=0)
        g.label("พายุทราย + แดดแผดเผา", CX, 360, 78, color=hexc("#b8473a"), sc=ap(t, L[3]), rot=-3)
        return
    for i in range(5):   # ทหารช่างกวาดกับระเบิด เปิดทางทีละคืบ
        mine(g, 160 + i * 220, GROUND + 20, 0.6, 0.4)
    step = (t - L[4]) * 30
    for i, lk in enumerate(TOMMY):
        x = 260 + i * 420 + step
        sw = 30 * math.sin(t * 3 + i)
        g.line([(x + 80, GROUND - 330 * 0.6), (x + 190 + sw, GROUND - 10)], 7, INK, amp=0)
        g.circle(x + 200 + sw, GROUND - 14, 26, hexc("#6a645a"), 4)
        person(g, x, GROUND, lk, 0.6, mood="worry", pose="hold", turn=0.5, seed=20 + i)
    g.line([(60, GROUND + 50), (1040, GROUND + 50)], 5, WHITE, amp=0)
    g.label("คลานเปิดทางทีละคืบ", CX, 380, 84, color=NAVY, sc=ap(t, L[4]), rot=-3)
    for i in range(6):
        g.line([(100 + i * 170, GROUND - 4), (150 + i * 170, GROUND - 4)], 6, GOLD2, amp=0)


# ------------------------------------------------------------------ 5. battle
def s_battle(g, t, L, d):
    desert(g, t)
    smoke(g, 250, 1000, 150, t, 5, seed=0.1)
    smoke(g, 820, 980, 160, t, 5, seed=0.5)
    if t < L[2] - 0.2:   # ระเบิด ควันปืน / เศษเหล็กรถถัง
        tank(g, 260, GROUND - 10, 0.65, "uk", t, fire=max(0.0, math.sin(t * 4)))
        tank(g, 820, GROUND - 10, 0.65, "de", t, flip=True, fire=max(0.0, math.sin(t * 4 + 2)),
             dead=1.0 if t > L[1] else 0.0, move=t < L[1])
        flashes(g, t, 0, 4, 860, 0.3)
        if t < L[1] - 0.2:
            g.label("ระเบิด! ควันปืนตลบ!", CX, 380, 86, color=RED, sc=ap(t, 0.2), rot=-3)
        else:
            for i in range(5):   # เศษเหล็กปลิว (ไม่มีคน)
                u = (t - L[1]) * 0.8 + i * 0.2
                u = u % 1
                with g.at(820 + (i - 2) * 120 * u, 1050 - 300 * u + 400 * u * u, 1, t * 200 + i * 40):
                    g.rrect(-18, -10, 36, 20, 3, hexc("#6a645a"), 4)
            g.label("เศษเหล็กปลิวว่อน", CX, 380, 86, color=GREY, sc=ap(t, L[1]), rot=-3)
        return
    if t < L[3] - 0.2:   # 12 วันเต็ม
        with g.at(CX, 780, ap(t, L[2])):
            g.rrect(-220, -200, 440, 400, 30, WHITE, 8)
            g.rrect(-220, -200, 440, 100, 30, RED, 8)
            g.text("ปะทะต่อเนื่อง", 0, -150, 44, "kanit", WHITE)
            n = 1 + int(11 * seg(t, L[2] + 0.3, L[3] - 0.6))
            g.label(str(n), 0, 20, 150)
            g.label("วัน", 0, 140, 50, color=GREY)
        flashes(g, t, 0, 3, 1150, 0.7)
        g.label("บ้าคลั่ง 12 วันเต็ม!", CX, 360, 86, color=RED, sc=ap(t, L[2]), rot=-3)
        return
    sway = 10 * math.sin(t * 2)   # แลกหมัดจนแทบไม่เหลือแรง
    monty(g, 280, 0.8, mood="worry", pose="fist", turn=0.4)
    rommel(g, 820, 0.8, mood="angry", pose="fist", turn=-0.4)
    g.sweat(330, GROUND - 720, 1.0)
    g.sweat(870, GROUND - 720, 1.0)
    with g.at(CX, 760 + sway, ap(t, L[3])):
        g.star(0, 0, 90, GOLD2, 6, pts=8, inner=0.5)
    g.label("แลกหมัดกันจนหมดแรง", CX, 380, 80, sc=ap(t, L[3]), rot=-3)


# ------------------------------------------------------------------ 6. fuel
def s_fuel(g, t, L, d):
    desert(g, t)
    if t < L[2] - 0.2:   # มอนต์โกเมอรีวางแผนสุขุม -> ตัดน้ำมัน
        monty(g, 260, 0.85, mood="smug", pose="think" if t < L[1] else "point", turn=0.3)
        if t < L[1] - 0.2:
            chess_piece(g, 760, 1080 + 10 * math.sin(t * 2), 1.4 * ap(t, 0.3))
            g.label("วางแผนอย่างสุขุม", CX, 360, 88, color=NAVY, sc=ap(t, 0.2), rot=-3)
        else:
            lvl = 1 - e_io(seg(t, L[1] + 0.2, L[2] - 0.4))
            jerrycan(g, 760, GROUND - 10, 1.4 * ap(t, L[1]), 3 * math.sin(t * 2), level=lvl)
            g.label("ตัดน้ำมันเยอรมันจนแห้ง!", CX, 360, 80, color=RED, sc=ap(t, L[1]), rot=-3)
        return
    if t < L[4] - 0.2:   # รถถังน่าเกรงขาม -> เศษเหล็กที่ขยับไม่ได้
        dead = t > L[3] - 0.2
        for i in range(2):
            tank(g, 300 + i * 480, GROUND - 10, 0.7, "de", t, move=not dead, dead=1.0 if dead else 0.0)
        if not dead:
            g.label("รถถังที่เคยน่าเกรงขาม", CX, 360, 80, sc=ap(t, L[2]), rot=-3)
        else:
            g.label("ขยับไม่ได้!", CX, 360, 100, color=RED, sc=ap(t, L[3]), rot=-3)
            for i in range(2):
                jerrycan(g, 430 + i * 480, 960, 0.4, 0, level=0.0)
        return
    if t < L[5] - 0.2:   # จิ้งจอกที่ไร้พ่าย
        rommel(g, CX, 0.8, mood="worry", pose="think", turn=0.0)
        g.sweat(CX + 70, GROUND - 780, 1.0 + 0.1 * math.sin(t * 6))
        g.label("จิ้งจอกที่ไร้พ่าย...", CX, 360, 88, color=GOLDTXT, sc=ap(t, L[4]), rot=-3)
        return
    run = e_io(seg(t, L[5], d))   # สั่งถอยทัพ
    rommel(g, lerp(560, 230, run), 0.82, mood="shock", pose="point", turn=-0.6)
    for i in range(2):
        tank(g, lerp(900, 420, run) + i * 340, GROUND - 10, 0.5, "de", t, flip=True)
    smoke(g, 1000, 1150, 90, t, 4, (0.8, 0.72, 0.55), 0.6)
    g.label("ถอยทัพ!", CX, 360, 110, color=RED, sc=ap(t, L[5]), rot=-4)
    g.label("อย่างไม่เป็นขบวน", CX, 500, 60, color=GREY, sc=ap(t, L[5] + 0.4))


# ------------------------------------------------------------------ 7. churchill
def s_churchill(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # ชัยชนะ / ดับความหวังฮิตเลอร์ในแอฟริกาเหนือ
        if t < L[1] - 0.2:
            for i, lk in enumerate(TOMMY):
                person(g, 190 + i * 700, GROUND, lk, 0.62, mood="smile", pose="wave", turn=0.2 - 0.4 * i, seed=30 + i)
            monty(g, CX, 0.75, mood="smile", pose="wave", turn=0.0)
            for i in range(6):
                u = (t * 0.4 + i / 6) % 1
                g.star(100 + i * 180, 500 + 500 * u, 18, GOLD2, 4)
            g.label("ชัยชนะครั้งประวัติศาสตร์!", CX, 360, 80, color=GREEN, sc=ap(t, 0.2), rot=-3)
            return
        egypt_map(g, CX, 780, 1.0, t, arrow=1 - e_io(seg(t, L[1], L[2] - 0.6)))
        with g.at(CX, 780, ap(t, L[1] + 0.8), -10):
            g.rrect(-260, -70, 520, 140, 20, (1, 1, 1, 0.9), 9, stroke=RED)
            g.label("ความหวังของฮิตเลอร์ดับ", 0, 0, 46, color=RED)
        g.label("แอฟริกาเหนือ", CX, 360, 90, color=NAVY, sc=ap(t, L[1]), rot=-3)
        return
    person(g, 260, GROUND, CHURCHILL, 0.85, mood="smile" if t > L[3] else "neutral",
           pose="sign" if t > L[2] + 0.5 else "down", turn=0.3, seed=40, talk=True)
    if t < L[2] + 3.2:
        g.name_tag(t, L[2] + 0.1, 780, 1140, "วินสตัน เชอร์ชิลล์", "นายกรัฐมนตรีอังกฤษ", side=-1)
    if t < L[3] - 0.2:
        g.label("ประโยคอมตะ", CX, 360, 96, color=GOLDTXT, sc=ap(t, L[2]), rot=-3)
        return
    with g.at(700, 700 + 10 * math.sin(t * 1.5), ap(t, L[3])):   # คำพูด
        g.bubble(0, 0, 560, 420, WHITE, tail=(-1, 1))
        g.label("ไม่ใช่จุดจบ", 0, -120, 54, color=GREY)
        g.label("ไม่ใช่จุดเริ่มต้นของจุดจบ", 0, -40, 40, color=GREY)
        if t > L[4] - 0.2:
            g.label("แต่คือ", 0, 50, 46, sc=ap(t, L[4]))
            g.label("จุดสิ้นสุดของจุดเริ่มต้น!", 0, 130, 46, color=RED, sc=ap(t, L[4] + 0.2))
    g.label('"End of the Beginning"', CX, 360, 70, color=NAVY, sc=ap(t, L[4]), rot=-3)


# ------------------------------------------------------------------ 8. lesson
def s_lesson(g, t, L, d):
    g.ground(GROUND, WHITE)
    g.label("บทเรียน", CX, 340, 100, sc=ap(t, 0.2), rot=-3)
    calm = e_io(seg(t, L[4] - 0.2, L[4] + 1.2))
    storm(g, CX, 830, 1.1, t, calm)
    if t < L[1] - 0.2:
        return
    if t < L[2] - 0.2:
        g.label("คู่แข่งที่ดูเหมือนชนะไม่ได้", CX, 490, 62, color=RED, sc=ap(t, L[1]))
        return
    if t < L[4] - 0.2:
        for i, (txt, col) in enumerate((("อดทน", GREEN), ("วางแผนรัดกุม", NAVY), ("รอจังหวะ", GOLDTXT))):
            t0 = L[2] + 0.5 * i if i < 2 else L[3]
            with g.at(200 + i * 340, 1150, ap(t, t0)):
                g.rrect(-150, -55, 300, 110, 30, WHITE, 6, stroke=col)
                g.label(txt, 0, 0, 44, color=col)
        return
    g.label("พายุร้ายย่อมสงบลงได้", CX, 1150, 70, color=GOLDTXT, sc=ap(t, L[4]))


# ------------------------------------------------------------------ 9. outro
def s_outro(g, t, L, d):
    desert(g, t)
    if t < L[1] - 0.2:
        rommel(g, 270, 0.82, mood="smug", turn=0.3)
        monty(g, 810, 0.82, mood="firm", turn=-0.3)
        g.label("แล้วทุกคนล่ะครับ", CX, 360, 90, sc=ap(t, 0.2), rot=-3)
        return
    if t < L[4] - 0.2:   # ดุดัน-ไหวพริบ vs สุขุม-เตรียมพร้อม
        rk = 1.0 if t > L[2] - 0.2 else 1.08 + 0.03 * math.sin(t * 4)
        mk = 1.08 + 0.03 * math.sin(t * 4) if t > L[2] - 0.2 else 1.0
        rommel(g, 270, 0.6 * (rk if t < L[3] - 0.2 else 1), mood="smug", pose="fist", turn=0.3)
        monty(g, 810, 0.6 * (mk if t < L[3] - 0.2 else 1), mood="smug", pose="cross", turn=-0.3)
        bolt(g, 270, 500 + 10 * math.sin(t * 3), 0.55 * ap(t, L[1]))
        chess_piece(g, 810, 610 + 10 * math.sin(t * 3 + 1), 0.6 * ap(t, L[2]))
        g.label("ดุดัน+ไหวพริบ", 270, 1120, 46, color=RED, sc=ap(t, L[1] + 0.3))
        g.label("สุขุม+เตรียมพร้อม", 810, 1120, 46, color=NAVY, sc=ap(t, L[2] + 0.3))
        if t < L[3] - 0.2:
            g.label("รอมเมล หรือ มอนต์โกเมอรี?", CX, 360, 70, sc=ap(t, L[1]), rot=-3)
        else:
            g.label("หัวใจของผู้นำในภาวะวิกฤต?", CX, 360, 70, color=GOLDTXT, sc=ap(t, L[3]), rot=-3)
        return
    with g.at(CX + 150, 650, ap(t, L[4])):   # ชวนคอมเมนต์
        g.bubble(0, 0, 480, 220, WHITE, tail=(-1, 1))
        for i in range(3):
            g.circle(-110 + i * 110, 0, 24 + 6 * math.sin(t * 6 - i), INK, 0)
    person(g, 250, GROUND, TOMMY[0], 0.8, mood="smile", pose="wave", turn=0.3, seed=50, talk=True)
    g.label("คอมเมนต์แลกเปลี่ยนกันได้เลย!", CX, 360, 70, color=RED, sc=ap(t, L[4]), rot=-3)


SCENES = {
    "hook": s_hook, "rommel": s_rommel, "monty": s_monty, "mines": s_mines, "battle": s_battle, "fuel": s_fuel,
    "churchill": s_churchill, "lesson": s_lesson, "outro": s_outro,
}
NO_IRIS = set()
