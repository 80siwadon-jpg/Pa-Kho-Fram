"""ฉากตอน: รัชกาลที่ 5 เสด็จสวรรคต (23 ต.ค. 1910) — โทนสุภาพ สง่างาม"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from chars import (MOURNERS, RAMA5, SLAVES, TODAY, arrow, book, candle, chain, crown, dove, flower, gunboat, heart,  # noqa: E402
                   ministry, portrait_frame, ribbon, school, sea, siam_disc, statue, telegraph, throne_hall, train,
                   wreath)
from gfx import GOLD, GOLD2, GREY, INK, LGREY, NAVY, RED, W, WHITE, e_io, e_out, hexc, lerp, pop, seg  # noqa: E402
from people import person  # noqa: E402

CX = W / 2
GROUND = 1270
GOLDTXT = hexc("#b37a12")
GREEN = hexc("#3c8d4f")
FR = hexc("#2b4c9a")
UK = hexc("#b8473a")

CAMERA = {"hook": "push_in", "legacy": "pan_right", "colonial": "pan_left", "reform": "push_in", "slavery": "tilt_up",
          "today": "pull_out", "lesson": "push_in", "outro": "pan_right"}
TRANSITIONS = {"legacy": "fade", "colonial": "whip", "reform": "zoom", "slavery": "fade", "today": "iris",
               "lesson": "fade", "outro": "zoom"}


def ap(t, a, dur=0.38):
    return pop(t, a - 0.2, dur)


def king(g, x, sc=0.85, mood="neutral", pose="down", turn=0.0, k=0.0, pose2=None):
    person(g, x, GROUND, RAMA5, sc, mood=mood, pose=pose, pose2=pose2, k=k, turn=turn, seed=5)


def petals(g, t, n=14, seed=0):
    """ดอกไม้ร่วงช้า ๆ (โทนไว้อาลัย)"""
    for i in range(n):
        u = (t * 0.12 + i * 0.137 + seed) % 1
        x = (i * 211 + seed * 97) % 1100 - 10 + 40 * math.sin(t + i)
        flower(g, x, 260 + u * 1000, 16, WHITE if i % 3 else hexc("#f2c94c"), t * 40 + i * 30)


def mourners(g, t, x0, gap, sc=0.55, mood="sad", n=5, seed=10):
    for i in range(n):
        person(g, x0 + i * gap, GROUND, MOURNERS[i % len(MOURNERS)], sc, mood=mood, pose="down", turn=0.1,
               seed=seed + i, shadow=False)


def tear(g, x, y, t, ph=0.0):
    u = (t * 0.9 + ph) % 1
    g.circle(x, y + 60 * u, 9, hexc("#9fd0f0"), 3)


# ------------------------------------------------------------------ 1. hook
def s_hook(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:   # วันที่
        candle(g, 300, 1150, 1.2, t)
        candle(g, 780, 1150, 1.2, t + 1)
        ribbon(g, CX, 800, 1.6 * pop(t, 0.6), 3 * math.sin(t * 1.5))
        g.label("วันนี้ในอดีต", CX, 380, 104, sc=lerp(2.0, 1, e_out(seg(t, 0.1, 0.4))) if t > 0.1 else 0, rot=-3)
        g.label("23 ตุลาคม 1910", CX, 520, 84, color=GOLDTXT, sc=pop(t, 0.8))
        return
    if t < L[2] - 0.2:   # คลื่นความโศกเศร้าปกคลุมสยาม
        mourners(g, t, 170, 190, 0.6)
        for i in range(5):
            tear(g, 170 + i * 190 + 18, GROUND - 500 * 0.6 * 1.0 - 255, t, i * 0.3)
        petals(g, t)
        g.label("ความโศกเศร้าทั่วสยาม", CX, 380, 80, color=NAVY, sc=ap(t, L[1]), rot=-3)
        return
    if t < L[4] - 0.2:   # พระบาทสมเด็จพระจุลจอมเกล้าเจ้าอยู่หัว
        g.sunburst(CX, 760, 260, 620, 20, t * 6, 10, (0.95, 0.85, 0.55, 0.5))
        king(g, CX, 0.92, mood="smile" if t > L[3] else "neutral", turn=0.05)
        g.name_tag(t, L[2] + 0.2, 800, 1140, "รัชกาลที่ 5", "พระจุลจอมเกล้าเจ้าอยู่หัว", side=-1)
        if t < L[3] - 0.2:
            g.label("พระจุลจอมเกล้าเจ้าอยู่หัว", CX, 340, 72, color=GOLDTXT, sc=ap(t, L[2]), rot=-2)
        else:
            g.label("เป็นที่รักยิ่งของปวงชน", CX, 340, 74, color=RED, sc=ap(t, L[3]), rot=-2)
            for i in range(4):
                u = (t * 0.5 + i / 4) % 1
                heart(g, 200 + i * 230, 1100 - 400 * u, 0.8, a=1 - u)
        return
    # เสด็จสวรรคต: พระบรมฉายาลักษณ์ + ผ้าไว้ทุกข์ + เทียน
    portrait_frame(g, CX, 760 + 8 * math.sin(t * 1.2), 380, 470, t, ap(t, L[4] + 0.3))
    candle(g, 220, 1200, 1.1, t)
    candle(g, 860, 1200, 1.1, t + 2)
    g.label("เสด็จสวรรคต", CX, 340, 92, sc=ap(t, L[4]))


# ------------------------------------------------------------------ 2. legacy
def s_legacy(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # การสูญเสีย / น้ำตาทั้งแผ่นดิน
        n = 5 if t < L[1] - 0.2 else 8
        for i in range(n):
            x = 120 + i * (840 / (n - 1))
            sc = 0.5 if n == 5 else 0.42
            person(g, x, GROUND - (0 if i % 2 else 40), MOURNERS[i % 5], sc, mood="sad", turn=0.1, seed=20 + i,
                   shadow=False)
        petals(g, t, 10, 0.4)
        if t < L[1] - 0.2:
            g.label("การสูญเสียครั้งใหญ่", CX, 380, 82, sc=ap(t, 0.2), rot=-3)
        else:
            for i in range(8):
                tear(g, 120 + i * 120 + 14, 860 + (40 if i % 2 == 0 else 0), t, i * 0.2)
            g.label("น้ำตาของคนไทยทั้งแผ่นดิน", CX, 380, 72, color=NAVY, sc=ap(t, L[1]), rot=-3)
        return
    if t < L[3] - 0.2:   # ประวัติศาสตร์จารึก
        book(g, CX, 960, 3.2 * ap(t, L[2]), -2 + math.sin(t))
        k = seg(t, L[2] + 0.3, L[3] - 0.4)
        for i in range(3):
            w = 220 * max(0.0, min(1.0, k * 3 - i))
            if w > 2:
                g.line([(CX + 50, 700 + i * 70), (CX + 50 + w, 690 + i * 70)], 7, GOLDTXT, amp=0)
        g.label("ประวัติศาสตร์จารึกไว้", CX, 380, 80, color=GOLDTXT, sc=ap(t, L[2]), rot=-3)
        return
    g.sunburst(CX, 760, 260, 640, 22, t * 8, 12, (0.95, 0.85, 0.55, 0.55))
    if t < L[4] - 0.2:   # พระปิยมหาราช
        king(g, CX, 0.92, mood="smile")
        g.label('"พระปิยมหาราช"', CX, 360, 104, color=GOLDTXT, sc=ap(t, L[3]), rot=-3)
        g.label("พระราชาผู้เป็นที่รัก", CX, 500, 52, color=GREY, sc=ap(t, L[3] + 0.6))
        return
    king(g, 330, 0.85, mood="firm", turn=0.3)   # อุทิศพระวรกายเพื่ออนาคตของชาติ
    for i, lk in enumerate((MOURNERS[4], TODAY[3], MOURNERS[1])):
        person(g, 640 + i * 140, GROUND, lk, 0.5, mood="smile", pose="wave" if i == 1 else "down", turn=-0.2,
               seed=30 + i, shadow=False)
    g.label("เพื่ออนาคตของชาติ", CX, 380, 82, color=NAVY, sc=ap(t, L[4]), rot=-3)


# ------------------------------------------------------------------ 3. colonial
def s_colonial(g, t, L, d):
    if t < L[2] - 0.2:   # มหาอำนาจล่าอาณานิคม กลืนกินดินแดนรอบข้าง
        sea(g, 1080, t, h=330)
        gunboat(g, lerp(-200, 260, e_out(seg(t, 0, 1.4))), 1080, 0.8, t, "uk")
        gunboat(g, lerp(1300, 820, e_out(seg(t, 0.3, 1.7))), 1080, 0.8, t, "fr", flip=True)
        if t < L[1] - 0.2:
            g.label("ยุคล่าอาณานิคม", CX, 360, 92, color=RED, sc=ap(t, 0.2), rot=-3)
            g.label("อังกฤษ", 260, 640, 60, color=UK, sc=ap(t, 0.8))
            g.label("ฝรั่งเศส", 820, 640, 60, color=FR, sc=ap(t, 1.1))
            return
        g.label("กลืนกินดินแดนรอบข้าง", CX, 360, 76, color=RED, sc=ap(t, L[1]), rot=-3)
        for i, (txt, col) in enumerate((("พม่า", UK), ("มลายู", UK), ("ญวน", FR), ("เขมร", FR))):
            x = 170 + i * 250
            k = ap(t, L[1] + 0.3 * i)
            with g.at(x, 640, k):
                g.rrect(-100, -55, 200, 110, 24, WHITE, 6, stroke=col)
                g.label(txt, 0, 0, 46, color=col)
        return
    g.ground(GROUND, WHITE)
    if t < L[3] - 0.2:   # หน้าสิ่วหน้าขวาน: ถูกบีบสองด้าน
        sh = 6 * math.sin(t * 9)
        siam_disc(g, CX + sh, 780, 230)
        g.label("สยาม", CX + sh, 780, 80, color=GOLDTXT)
        squeeze = 20 * math.sin(t * 3)
        for sx, txt, col in ((-1, "อังกฤษ", UK), (1, "ฝรั่งเศส", FR)):
            x = CX + sx * (390 - squeeze)
            with g.at(x, 780, ap(t, L[2])):
                g.rrect(-100, -160, 200, 320, 30, WHITE, 7, stroke=col)
                g.label(txt, 0, 0, 40, color=col)
            arrow(g, CX + sx * 300, 1060, -sx, col, ap(t, L[2] + 0.3))
        g.label("หน้าสิ่วหน้าขวาน", CX, 360, 96, color=RED, sc=ap(t, L[2]), rot=-3)
        return
    lost = e_io(seg(t, L[3], L[4] - 0.3))
    king(g, 210, 0.72, mood="firm" if t < L[4] else "smile", turn=0.4)
    siam_disc(g, 700, 780, 220, lost, t)
    if t < L[4] - 0.2:
        g.label("ยอมเสียสละบางส่วน", CX, 360, 80, color=NAVY, sc=ap(t, L[3]), rot=-3)
    else:   # รักษาเอกราช
        g.sunburst(700, 780, 170, 300, 14, t * 10, 8, (0.95, 0.85, 0.55, 0.6 * ap(t, L[4])))
        siam_disc(g, 700, 780, 220, 1.0, t)
        g.label("เอกราช", 700, 780, 70, color=GOLDTXT, sc=ap(t, L[4] + 0.2))
        g.label("รักษาเอกราชไว้ได้", CX, 360, 84, color=GREEN, sc=ap(t, L[4]), rot=-3)


# ------------------------------------------------------------------ 4. reform
def s_reform(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:   # ทรงงานหนัก
        king(g, 300, 0.82, mood="firm", pose="point", turn=0.3)
        for i in range(4):
            with g.at(760 + 20 * math.sin(t * 2 + i), 1060 - i * 70, ap(t, 0.2 + 0.15 * i), -6 + 4 * i):
                g.rrect(-140, -30, 280, 60, 6, hexc("#f4efe2"), 5)
        g.label("ทรงงานอย่างหนัก", CX, 360, 90, sc=ap(t, 0.2), rot=-3)
        return
    if t < L[2] - 0.2:   # ปฏิรูประบบราชการ ตั้งกระทรวง
        for i, nm in enumerate(("มหาดไทย", "กลาโหม", "คลัง")):
            ministry(g, 200 + i * 340, 1240, 0.7 * ap(t, L[1] + 0.25 * i), nm)
        g.label("ปฏิรูประบบราชการ", CX, 340, 84, color=NAVY, sc=ap(t, L[1]), rot=-3)
        g.label("ตั้งกระทรวง", CX, 470, 64, color=GOLDTXT, sc=ap(t, L[1] + 0.6))
        return
    if t < L[3] - 0.2:   # รถไฟ + โทรเลข
        telegraph(g, 120, 980, 880, t)
        train(g, lerp(-100, 900, e_out(seg(t, L[2] - 0.2, L[3]))), 1240, 0.6, t)
        g.label("รถไฟและโทรเลข", CX, 340, 88, color=RED, sc=ap(t, L[2]), rot=-3)
        return
    school(g, 560, 1240, 1.0 * ap(t, L[3]))   # รากฐานการศึกษา
    for i in range(3):
        person(g, 180 + i * 130 + 20 * math.sin(t * 3 + i), GROUND, (MOURNERS[4], TODAY[3], SLAVES[2])[i], 0.5,
               mood="smile", pose="wave" if i == 1 else "down", turn=0.4, seed=40 + i, shadow=False)
    book(g, 840, 560 + 14 * math.sin(t * 2), 0.9 * ap(t, L[3] + 0.4), 6 * math.sin(t))
    g.label("รากฐานการศึกษา", CX, 340, 88, color=GREEN, sc=ap(t, L[3]), rot=-3)


# ------------------------------------------------------------------ 5. slavery
def s_slavery(g, t, L, d):
    g.ground(GROUND, WHITE)
    free = t > L[1] + 0.6
    for i, lk in enumerate(SLAVES):
        x = 230 + i * 300
        person(g, x, GROUND, lk, 0.62 if i < 2 else 0.58, mood="smile" if free else "sad",
               pose="v" if free and i == 2 else ("wave" if free else "down"), turn=0.1, seed=50 + i)
    br = e_out(seg(t, L[1] + 0.3, L[1] + 1.2))
    if t < L[2] - 0.2:
        chain(g, 120, 1000, 960, 1000, br)
    if t < L[1] - 0.2:
        g.label('"เลิกทาส"', CX, 360, 120, color=RED, sc=ap(t, 0.2), rot=-3)
        g.label("ยิ่งใหญ่ที่สุด", CX, 520, 60, color=GOLDTXT, sc=ap(t, 0.8))
        return
    if t < L[2] - 0.2:
        g.label("ปลดแอกโซ่ตรวนศักดินา", CX, 360, 76, color=NAVY, sc=ap(t, L[1]), rot=-3)
        return
    for i in range(3):
        dove(g, (180 + i * 330 + (t - L[2]) * 120) % 1200 - 60, 560 + 40 * math.sin(t * 2 + i), 0.9, t + i)
    g.label("ไม่นองเลือดแม้แต่หยดเดียว", CX, 360, 70, color=GREEN, sc=ap(t, L[2]), rot=-3)
    g.label("พ.ร.บ.เลิกทาส ร.ศ.124 (1905)", CX, 480, 44, color=GREY, sc=ap(t, L[2] + 0.5))


# ------------------------------------------------------------------ 6. today
def s_today(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # กว่าร้อยปี / ความรักความกตัญญู
        portrait_frame(g, CX, 760, 340, 420, t, 0.0)
        if t < L[1] - 0.2:
            yr = int(lerp(1910, 2026, e_io(seg(t, 0.4, L[1] - 0.4))))
            g.label(str(yr), CX, 1140, 96, color=GOLDTXT, sc=ap(t, 0.3))
            g.label("กว่าร้อยปี", CX, 360, 92, sc=ap(t, 0.2), rot=-3)
        else:
            for i in range(5):
                u = (t * 0.45 + i / 5) % 1
                heart(g, 180 + i * 180, 1200 - 600 * u, 0.8, a=1 - u)
            g.label("ความรักและความกตัญญู", CX, 360, 76, color=RED, sc=ap(t, L[1]), rot=-3)
        return
    if t < L[4] - 0.2:   # ทุก 23 ต.ค. คนนับล้านมาวางพวงมาลา
        for i, lk in enumerate(TODAY if t < L[3] - 0.2 else ()):
            x = (i * 260 + (t - L[2]) * 70) % 1200 - 60
            person(g, x, GROUND, lk, 0.55, mood="neutral", pose="hold", turn=0.5, seed=60 + i, shadow=False)
            if i < 2:
                wreath(g, x + 90, GROUND - 520, 0.4)
        if t < L[3] - 0.2:
            with g.at(CX, 600, 0.85 * ap(t, L[2])):
                g.rrect(-230, -170, 460, 340, 24, WHITE, 7)
                g.rrect(-230, -170, 460, 100, 24, RED, 7)
                g.text("ตุลาคม", 0, -120, 50, "kanit", WHITE)
                g.label("23", 0, 30, 140, color=INK)
                g.label("วันปิยมหาราช", 0, 130, 38, color=GOLDTXT)
            g.label("ทุกวันที่ 23 ตุลาคม", CX, 360, 84, sc=ap(t, L[2]), rot=-3)
        else:
            g.label("วางพวงมาลา", CX, 360, 92, color=GOLDTXT, sc=ap(t, L[3]), rot=-3)
            for i, (lk, x) in enumerate(((TODAY[0], 170), (TODAY[1], 910))):
                person(g, x + 15 * math.sin(t * 2 + i), GROUND, lk, 0.6, mood="neutral", pose="hold",
                       turn=0.5 if i == 0 else -0.5, seed=60 + i)
            wreath(g, CX, 720 + 10 * math.sin(t * 2), 1.0 * ap(t, L[3]), 2 * math.sin(t))
        return
    throne_hall(g, CX, 1150, 0.95)   # พระบรมรูปทรงม้า
    statue(g, CX, 1250, 0.78 * ap(t, L[4]) if t < L[4] + 0.4 else 0.78)
    for i, x in enumerate((180, 880)):
        wreath(g, x, 1000, 0.6 * ap(t, L[4] + 0.4 + 0.2 * i))
    if t < L[5] - 0.2:
        g.label("พระบรมรูปทรงม้า", CX, 340, 92, color=GOLDTXT, sc=ap(t, L[4]), rot=-3)
    else:
        g.sunburst(CX, 450, 80, 260, 14, t * 8, 8, (0.95, 0.85, 0.55, 0.5))
        g.label("รำลึกพระมหากรุณาธิคุณ", CX, 340, 74, color=GOLDTXT, sc=ap(t, L[5]), rot=-3)


# ------------------------------------------------------------------ 7. lesson
def s_lesson(g, t, L, d):
    g.ground(GROUND, WHITE)
    g.label("บทเรียน", CX, 340, 100, sc=ap(t, 0.2), rot=-3)
    if t < L[1] - 0.2:
        king(g, CX, 0.85, mood="smile")
        return
    if t < L[2] - 0.2:   # ไม่ได้วัดที่อำนาจ
        crown(g, CX, 960 + 14 * math.sin(t * 2), 1.4 * ap(t, L[1]), 3 * math.sin(t * 1.5))
        g.label("อำนาจ", CX, 1100, 70, color=GOLDTXT, sc=ap(t, L[1] + 0.2))
        if t > L[1] + 1.0:
            g.line([(CX - 200, 620), (CX + 200, 1060)], 14, RED, amp=0)
        g.label("ไม่ได้วัดที่อำนาจ", CX, 480, 66, color=RED, sc=ap(t, L[1] + 0.4))
        return
    # วัดที่สิ่งที่ทิ้งไว้ให้คนรุ่นหลัง
    for i, lk in enumerate(TODAY):
        person(g, 160 + i * 230, GROUND, lk, 0.5, mood="smile", pose="wave" if i == 3 else "down", turn=0.2,
               seed=70 + i, shadow=False)
    items = [lambda x, y, k: train(g, x + 60, y + 40, 0.18 * k, t), lambda x, y, k: school(g, x, y + 60, 0.3 * k),
             lambda x, y, k: book(g, x, y + 40, 0.6 * k), lambda x, y, k: dove(g, x, y, 0.8 * k, t)]
    for i, f in enumerate(items):
        f(180 + i * 240, 740 + 14 * math.sin(t * 2 + i), ap(t, L[2] + 0.3 * i))
    g.label("สิ่งที่ทิ้งไว้ให้คนรุ่นหลัง", CX, 480, 66, color=GREEN, sc=ap(t, L[2]))


# ------------------------------------------------------------------ 8. outro
def s_outro(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[3] - 0.2:
        if t < L[1] - 0.2:
            king(g, CX, 0.85, mood="smile")
            g.label("แล้วทุกคนล่ะครับ", CX, 360, 88, sc=ap(t, 0.2), rot=-3)
            return
        g.label("ประทับใจเรื่องไหนที่สุด?", CX, 340, 76, sc=ap(t, L[1]), rot=-3)
        names = ("รักษาเอกราช", "ปฏิรูปประเทศ", "รถไฟ-โทรเลข", "เลิกทาส")
        for i, nm in enumerate(names):
            x, y = 290 + (i % 2) * 500, 640 + (i // 2) * 380
            k = ap(t, L[1] + 0.3 * i) * (1 + 0.04 * math.sin(t * 3 + i))
            if k < 0.02:   # สเกลซ้อนเล็กเกินทำให้ cairo พัง
                continue
            with g.at(x, y, k):
                g.rrect(-220, -150, 440, 300, 30, WHITE, 7)
                if i == 0:
                    siam_disc(g, 0, -30, 80)
                elif i == 1:
                    ministry(g, 0, 40, 0.3, "")
                elif i == 2:
                    train(g, 60, 30, 0.2, t)
                else:
                    chain(g, -110, -30, 110, -30, 0.35, 5)
                g.label(nm, 0, 100, 44, color=GOLDTXT)
            if t > L[2] - 0.2:
                u = (t * 0.6 + i / 4) % 1
                heart(g, x + 170, y - 110 - 80 * u, 0.6, a=(1 - u) * ap(t, L[2]))
        return
    with g.at(CX + 170, 640, ap(t, L[3])):   # ชวนคอมเมนต์
        g.bubble(0, 0, 460, 220, WHITE, tail=(-1, 1))
        for i in range(3):
            g.circle(-110 + i * 110, 0, 24 + 6 * math.sin(t * 6 - i), INK, 0)
    person(g, 250, GROUND, TODAY[0], 0.75, mood="smile", pose="wave", turn=0.3, seed=80, talk=True)
    g.label("คอมเมนต์แลกเปลี่ยนกันได้เลย!", CX, 360, 70, color=RED, sc=ap(t, L[3]), rot=-3)
    heart(g, 760, 960 + 20 * math.sin(t * 3), 1.2 * ap(t, L[3] + 0.5))


SCENES = {
    "hook": s_hook, "legacy": s_legacy, "colonial": s_colonial, "reform": s_reform, "slavery": s_slavery,
    "today": s_today, "lesson": s_lesson, "outro": s_outro,
}
NO_IRIS = set()
