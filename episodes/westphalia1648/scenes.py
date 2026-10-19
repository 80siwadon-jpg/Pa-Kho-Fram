"""ฉากตอน: สนธิสัญญาสันติภาพเวสต์ฟาเลีย (24 ต.ค. 1648) — ไม่แสดงความรุนแรงตรง ๆ"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from chars import (ENVOYS, PEASANTS, SOLDIER, church, crown, empty_bowl, europe_patchwork, grave_crosses,  # noqa: E402
                   papal_tiara, quill, shield, sword, table, treaty, village)
from gfx import GOLD2, GREY, INK, NAVY, RED, W, WHITE, e_io, e_out, hexc, lerp, pop, seg  # noqa: E402
from people import person  # noqa: E402

CX = W / 2
GROUND = 1270
GOLDTXT = hexc("#b37a12")
GREEN = hexc("#3c8d4f")
DARK = hexc("#4a3a3a")

CAMERA = {"hook": "push_in", "war": "pan_left", "treaty": "push_in", "sovereign": "pan_right", "legacy": "pull_out",
          "lesson": "tilt_up", "outro": "pan_left"}
TRANSITIONS = {"war": "fade", "treaty": "iris", "sovereign": "zoom", "legacy": "whip", "lesson": "fade",
               "outro": "whip"}


def ap(t, a, dur=0.38):
    return pop(t, a - 0.2, dur)


def haze(g, a=0.35):
    """ท้องฟ้าหม่นควันสงคราม"""
    c = g.c
    c.rectangle(-500, 140, 2100, 1130)
    c.set_source_rgba(0.45, 0.4, 0.38, a)
    c.fill()


def envoys(g, t, n=4, x0=150, gap=260, sc=0.6, mood="neutral", pose="down", talk=False):
    for i in range(n):
        person(g, x0 + i * gap, GROUND, ENVOYS[i % 4], sc, mood=mood, pose=pose if i % 2 == 0 else "down",
               turn=0.3 - 0.2 * i, seed=10 + i, talk=talk)


# ------------------------------------------------------------------ 1. hook
def s_hook(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[3] - 0.2:   # วันที่ -> ระฆังดังทั่วยุโรป -> 30 ปี
        ring = 0.0 if t < L[1] - 0.2 else 1.0
        church(g, CX if t < L[1] - 0.2 else 330, GROUND, 0.95 if t < L[1] - 0.2 else 0.8, t, ring)
        if t > L[1] - 0.2:
            church(g, 820, GROUND, 0.55, t + 0.5, ring)
        if t < L[1] - 0.2:
            g.label("วันนี้ในอดีต", CX, 380, 104, sc=lerp(2.0, 1, e_out(seg(t, 0.1, 0.4))) if t > 0.1 else 0, rot=-3)
            g.label("24 ตุลาคม 1648", CX, 520, 84, color=GOLDTXT, sc=pop(t, 0.8))
        elif t < L[2] - 0.2:
            g.label("ระฆังดังทั่วยุโรป!", CX, 380, 92, color=GOLDTXT, sc=ap(t, L[1]), rot=-3)
        else:
            g.label("สิ้นสุดฝันร้าย 30 ปี!", CX, 380, 92, color=GREEN, sc=ap(t, L[2]), rot=-3)
        return
    haze(g, 0.25)
    if t < L[4] - 0.2:   # เริ่มจากความขัดแย้งทางศาสนา
        for i, (txt, col, x) in enumerate((("คาทอลิก", RED, 260), ("โปรเตสแตนต์", NAVY, 820))):
            with g.at(x + (1 - 2 * i) * 20 * math.sin(t * 3), 700, ap(t, L[3] + 0.3 * i)):
                g.rrect(-180, -80, 360, 160, 30, WHITE, 7, stroke=col)
                g.line([(0, -60), (0, -20)], 8, col, amp=0)
                g.line([(-18, -46), (18, -46)], 8, col, amp=0)
                g.label(txt, 0, 34, 44, color=col)
        g.label("VS", CX, 700, 80, color=RED, sc=ap(t, L[3] + 0.6))
        g.label("ความขัดแย้งทางศาสนา", CX, 380, 80, sc=ap(t, L[3]), rot=-3)
        return
    village(g, GROUND, t, 1.0)   # เข่นฆ่า -> วันสิ้นโลก
    if t < L[5] - 0.2:
        g.label("โหดที่สุดในประวัติศาสตร์", CX, 380, 80, color=RED, sc=ap(t, L[4]), rot=-3)
    else:
        g.label("วันสิ้นโลก?!", CX, 380, 110, color=RED, sc=ap(t, L[5]), rot=-3)


# ------------------------------------------------------------------ 2. war
def s_war(g, t, L, d):
    g.ground(GROUND, WHITE)
    haze(g, 0.3)
    if t < L[1] - 0.2:   # สงครามสามสิบปี
        with g.at(CX, 760, ap(t, 0.2)):
            g.rrect(-260, -170, 520, 340, 24, WHITE, 8)
            g.label("1618", -130, -60, 70, color=GREY)
            g.label("→", 0, -60, 60, color=GREY)
            g.label("1648", 130, -60, 70, color=GREY)
            g.label("30 ปี", 0, 70, 110, color=RED)
        g.label('"สงครามสามสิบปี"', CX, 380, 100, color=DARK, sc=ap(t, 0.2), rot=-3)
        return
    if t < L[4] - 0.2:   # เยอรมันถูกเผา / ทหารรับจ้างปล้น / เผาหมู่บ้าน (เงาไกล ๆ)
        village(g, GROUND, t, e_io(seg(t, L[1], L[1] + 1.5)))
        if t < L[2] - 0.2:
            g.label("แผ่นดินเยอรมันถูกเผาราบ", CX, 380, 78, color=RED, sc=ap(t, L[1]), rot=-3)
        elif t < L[3] - 0.2:
            with g.silhouette((0.2, 0.18, 0.18), 0.85):
                for i in range(3):
                    person(g, 160 + i * 140 + (t - L[2]) * 60, GROUND + 20, SOLDIER, 0.5, pose="down", turn=0.6,
                           seed=30 + i, shadow=False)
            g.label("กองทัพรับจ้างปล้นสะดม", CX, 380, 78, color=RED, sc=ap(t, L[2]), rot=-3)
        else:
            g.label("เผาทุกหมู่บ้านที่ผ่าน", CX, 380, 84, color=RED, sc=ap(t, L[3]), rot=-3)
        return
    if t < L[5] - 0.2:   # ความอดอยาก
        for i, lk in enumerate(PEASANTS):
            person(g, 230 + i * 300, GROUND, lk, 0.62 if i < 2 else 0.6, mood="sad", pose="down", turn=0.1,
                   seed=40 + i)
        empty_bowl(g, CX, 1180, 0.9)
        g.label("ความอดอยากแสนสาหัส", CX, 380, 84, color=DARK, sc=ap(t, L[4]), rot=-3)
        return
    if t < L[7] - 0.2:   # โรคระบาด / ตายไปกว่าครึ่ง
        grave_crosses(g, CX, GROUND, 7, 1.1, seg(t, L[5], L[5] + 2.5))
        if t < L[6] - 0.2:
            g.label("โรคระบาดคร่าชีวิตทุกวัน", CX, 380, 80, color=DARK, sc=ap(t, L[5]), rot=-3)
        else:
            for i in range(10):   # ประชากร: ครึ่งหนึ่งจางหาย
                a = 1.0 if i < 5 else 1 - 0.8 * seg(t, L[6], L[6] + 1.2)
                with g.alpha(a):
                    g.circle(170 + i * 80, 720, 24, hexc("#6a5a52"), 4)
                    g.rrect(170 + i * 80 - 26, 752, 52, 70, 16, hexc("#6a5a52"), 4)
            g.label("ตายไปกว่าครึ่ง!", CX, 380, 100, color=RED, sc=ap(t, L[6]), rot=-3)
        return
    haze(g, 0.45)   # นรกบนดิน ไม่มีแสงสว่าง
    village(g, GROUND, t, 1.0, 0.8)
    if t < L[8] - 0.2:
        g.label("นรกบนดิน", CX, 380, 120, color=RED, sc=ap(t, L[7]), rot=-3)
    else:
        g.label("ไม่มีแสงสว่างเลย...", CX, 380, 92, color=DARK, sc=ap(t, L[8]), rot=-3)


# ------------------------------------------------------------------ 3. treaty
def s_treaty(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:   # หมดแรงจับดาบ
        person(g, 330, GROUND, SOLDIER, 0.8, mood="sad", pose="down", turn=0.3, seed=50)
        sword(g, 720, GROUND - 20, 1.2, lerp(0, 75, e_out(seg(t, 0.5, 2.0))))
        g.label("ไม่เหลือแรงจะจับดาบ", CX, 380, 84, color=DARK, sc=ap(t, 0.2), rot=-3)
        return
    if t < L[3] - 0.2:   # ตัวแทนกว่าร้อยรัฐ นั่งเจรจาหลายปี
        envoys(g, t, 4, 150, 260, 0.6, "neutral" if t < L[2] else "worry", "point", talk=True)
        if t < L[2] - 0.2:
            with g.at(860, 560, ap(t, L[1] + 0.4)):
                g.circle(0, 0, 110, WHITE, 7)
                g.label("100+", 0, -10, 70, color=GOLDTXT)
                g.label("รัฐ", 0, 50, 34, color=GREY)
            g.label("ตัวแทนกว่าร้อยรัฐ", CX, 380, 90, color=NAVY, sc=ap(t, L[1]), rot=-3)
        else:
            for i in range(3):
                u = (t * 0.5 + i / 3) % 1
                g.label("...", 150 + i * 360, 620 - 60 * u, 70, color=GREY, a=1 - u)
            with g.at(860, 560, ap(t, L[2] + 0.3)):
                g.rrect(-110, -70, 220, 140, 16, WHITE, 6)
                g.label("1643-1648", 0, 0, 36, color=GREY)
            g.label("เจรจายาวนานหลายปี", CX, 380, 86, color=DARK, sc=ap(t, L[2]), rot=-3)
        return
    if t < L[4] - 0.2:   # ลงนาม
        table(g, CX, GROUND - 240, 820)
        envoys(g, t, 3, 220, 320, 0.55, "smile")
        treaty(g, CX, GROUND - 420, 0.5, 0, 0, seg(t, L[3], L[4]))
        quill(g, CX + 60 + 30 * math.sin(t * 8), GROUND - 430, 0.6, 20)
        g.label("ร่วมกันลงนาม", CX, 380, 96, color=GOLDTXT, sc=ap(t, L[3]), rot=-3)
        return
    g.sunburst(CX, 800, 300, 660, 22, t * 8, 12, (0.98, 0.85, 0.4, 0.6))   # สนธิสัญญาเวสต์ฟาเลีย
    treaty(g, CX, 820, 1.0 * ap(t, L[4]), 3 * math.sin(t * 1.5), 3, 1.0)
    g.label('"สันติภาพเวสต์ฟาเลีย"!', CX, 340, 86, color=GOLDTXT, sc=ap(t, L[4]), rot=-3)


# ------------------------------------------------------------------ 4. sovereign
def s_sovereign(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # ดับไฟสงคราม -> ปฏิวัติโลก
        if t < L[1] - 0.2:
            village(g, GROUND, t, 1 - e_io(seg(t, 0.3, L[1] - 0.4)))
            g.label("ดับไฟสงคราม", CX, 380, 100, color=GREEN, sc=ap(t, 0.2), rot=-3)
        else:
            g.sunburst(CX, 800, 200, 560, 20, t * 12, 10, (0.98, 0.7, 0.4, 0.6))
            europe_patchwork(g, CX - 20, 840, 0.82, t, 1.0, 1.0)
            g.label('"ปฏิวัติโลก"!', CX, 380, 110, color=RED, sc=ap(t, L[1]), rot=-3)
        return
    if t < L[5] - 0.2:   # จักรพรรดิ/พระสันตะปาปาห้ามก้าวก่าย
        envoys(g, t, 2, 200, 640, 0.62, "firm", "stop")
        crown(g, 420, 700 + 10 * math.sin(t * 2), 1.0 * ap(t, L[3]))
        papal_tiara(g, 660, 760 + 10 * math.sin(t * 2 + 1), 0.9 * ap(t, L[3] + 0.4))
        if t > L[4] - 0.2:
            g.line([(330, 520), (760, 860)], 18, RED, amp=0)
            g.line([(760, 520), (330, 860)], 18, RED, amp=0)
        if t < L[3] - 0.2:
            g.label("ครั้งแรกในประวัติศาสตร์", CX, 380, 84, color=GOLDTXT, sc=ap(t, L[2]), rot=-3)
        elif t < L[4] - 0.2:
            g.label("จักรพรรดิ / พระสันตะปาปา", CX, 380, 74, color=NAVY, sc=ap(t, L[3]), rot=-3)
        else:
            g.label("ห้ามก้าวก่ายดินแดนอื่น!", CX, 380, 80, color=RED, sc=ap(t, L[4]), rot=-3)
        return
    europe_patchwork(g, CX - 20, 840, 0.82, t, 1.0 if t > L[7] - 0.2 else 0.0, 1.0)   # รัฐอธิปไตย
    if t < L[6] - 0.2:
        g.label('"รัฐอธิปไตยสมัยใหม่"', CX, 380, 84, color=GOLDTXT, sc=ap(t, L[5]), rot=-3)
    elif t < L[7] - 0.2:
        crown(g, 540, 800, 0.8 * ap(t, L[6]))
        g.label("อำนาจสูงสุดในการปกครองตนเอง", CX, 380, 56, color=NAVY, sc=ap(t, L[6]), rot=-3)
    elif t < L[8] - 0.2:
        g.label("พรมแดนที่ชัดเจน", CX, 380, 96, color=RED, sc=ap(t, L[7]), rot=-3)
    else:
        for i in range(3):
            g.line([(280 + i * 260, 760), (280 + i * 260, 700)], 8, INK, amp=0)
            g.line([(262 + i * 260, 716), (298 + i * 260, 716)], 8, INK, amp=0)
        g.label("เลือกศาสนาและวิถีชีวิตเอง", CX, 380, 72, color=GREEN, sc=ap(t, L[8]), rot=-3)


# ------------------------------------------------------------------ 5. legacy
def s_legacy(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # กระดาษสนธิสัญญา เกือบ 400 ปีก่อน
        village(g, GROUND, t, 0.4, 0.35)
        treaty(g, CX, 800, 0.9, -3 + 2 * math.sin(t), 3, 1.0)
        if t < L[1] - 0.2:
            g.label("ลงนามท่ามกลางซากปรักหักพัง", CX, 380, 68, color=DARK, sc=ap(t, 0.2), rot=-3)
        else:
            g.label("เกือบ 400 ปีก่อน", CX, 380, 96, color=GOLDTXT, sc=ap(t, L[1]), rot=-3)
        return
    if t < L[3] - 0.2:   # เสาเข็มกฎหมายระหว่างประเทศ
        with g.at(CX, GROUND - 40):
            for i in range(3):
                g.rrect(-320 + i * 240, -560, 160, 560, 10, hexc("#d8d3c7"), 6)
            g.rrect(-380, -640, 760, 90, 10, hexc("#bdb6a6"), 6)
            g.label("กฎหมายระหว่างประเทศ", 0, -595, 44, color=NAVY)
        treaty(g, CX, 1100, 0.35 * ap(t, L[2]), 0, 3)
        g.label("เสาเข็มต้นสำคัญ", CX, 380, 96, color=NAVY, sc=ap(t, L[2]), rot=-3)
        return
    europe_patchwork(g, CX - 20, 840, 0.82, t, 1.0, 1.0)   # ประเทศ + พรมแดน ถึงทุกวันนี้
    if t < L[4] - 0.2:
        g.label('รากฐานของ "ประเทศ" + "พรมแดน"', CX, 380, 66, color=GOLDTXT, sc=ap(t, L[3]), rot=-3)
    else:
        g.label("ที่เราอยู่จนถึงทุกวันนี้", CX, 380, 84, color=GREEN, sc=ap(t, L[4]), rot=-3)


# ------------------------------------------------------------------ 6. lesson
def s_lesson(g, t, L, d):
    g.ground(GROUND, WHITE)
    g.label("บทเรียน", CX, 340, 100, sc=ap(t, 0.2), rot=-3)
    if t < L[2] - 0.2:
        g.sunburst(CX, 820, 140, 320, 14, t * 10, 10, (0.98, 0.8, 0.35, 0.7 * ap(t, L[1])))
        treaty(g, CX, 840, 0.6 * ap(t, 0.4), 4 * math.sin(t), 3)
        if t > L[1] - 0.2:
            g.label("บทเรียนยิ่งใหญ่ที่สุด", CX, 490, 64, color=GOLDTXT, sc=ap(t, L[1]))
        return
    grave_crosses(g, CX, GROUND, 7, 1.0, 1.0)
    church(g, CX, GROUND - 200, 0.45, t, 0.6)
    g.label("แลกด้วยบาดแผลและความสูญเสีย", CX, 490, 60, color=RED, sc=ap(t, L[2]))


# ------------------------------------------------------------------ 7. outro
def s_outro(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[5] - 0.2:
        if t < L[3] - 0.2:
            europe_patchwork(g, CX - 20, 840, 0.82, t, 1.0, 1.0)
            if t > L[2] - 0.2:   # โลกเชื่อมถึงกัน
                for i in range(6):
                    a = i * math.pi / 3 + t * 0.3
                    g.line([(CX + 300 * math.cos(a), 820 + 300 * math.sin(a)),
                            (CX + 300 * math.cos(a + 2.1), 820 + 300 * math.sin(a + 2.1))], 5, (0.3, 0.5, 0.8, 0.6),
                           amp=0)
            if t < L[1] - 0.2:
                g.label('หลักการ "รัฐอธิปไตย"', CX, 380, 84, color=GOLDTXT, sc=ap(t, 0.2), rot=-3)
            elif t < L[2] - 0.2:
                g.label("ห้ามก้าวก่ายเรื่องภายใน", CX, 380, 80, color=NAVY, sc=ap(t, L[1]), rot=-3)
            else:
                g.label("โลกที่เชื่อมถึงกันหมด", CX, 380, 84, color=GREEN, sc=ap(t, L[2]), rot=-3)
            return
        shield(g, 300, 800 + 10 * math.sin(t * 2), 1.2 * ap(t, L[3]), t, seg(t, L[4], L[4] + 1.0))
        g.label("เกราะป้องกัน?", 300, 1080, 50, color=NAVY, sc=ap(t, L[3] + 0.3))
        if t > L[4] - 0.2:
            crown(g, 790, 640, 0.9 * ap(t, L[4]), 8 * math.sin(t * 2), hexc("#8a6a3a"))
            for i in range(3):
                person(g, 660 + i * 130, GROUND, PEASANTS[i % 3], 0.4, mood="worry", seed=60 + i, shadow=False)
            g.label("ข้ออ้างกดขี่?", 790, 760, 50, color=RED, sc=ap(t, L[4] + 0.3))
            g.label("หรือกลายเป็นข้ออ้าง?", CX, 380, 84, color=RED, sc=ap(t, L[4]), rot=-3)
        else:
            g.label("ยังเป็นเกราะที่ดีไหม?", CX, 380, 84, color=NAVY, sc=ap(t, L[3]), rot=-3)
        return
    with g.at(CX + 170, 640, ap(t, L[5])):   # ชวนคอมเมนต์
        g.bubble(0, 0, 460, 220, WHITE, tail=(-1, 1))
        for i in range(3):
            g.circle(-110 + i * 110, 0, 24 + 6 * math.sin(t * 6 - i), INK, 0)
    person(g, 250, GROUND, ENVOYS[0], 0.75, mood="smile", pose="wave", turn=0.3, seed=70, talk=True)
    g.label("คอมเมนต์แลกเปลี่ยนกันได้เลย!", CX, 360, 70, color=RED, sc=ap(t, L[5]), rot=-3)


SCENES = {
    "hook": s_hook, "war": s_war, "treaty": s_treaty, "sovereign": s_sovereign, "legacy": s_legacy,
    "lesson": s_lesson, "outro": s_outro,
}
NO_IRIS = set()
