"""ฉากตอน: วันเกิดไมเคิล ไครช์ตัน (23 ต.ค. 1942) ผู้ให้กำเนิด Jurassic Park"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from chars import (CRICHTON, CROWD, SPIELBERG, STUDENT, amber, book, chip, clapper, cross_sign, dna,  # noqa: E402
                   microscope, money_rain, robot_cowboy, trex)
from gfx import GOLD2, GREY, INK, NAVY, RED, W, WHITE, e_io, e_out, hexc, lerp, pop, seg  # noqa: E402
from people import person  # noqa: E402

CX = W / 2
GROUND = 1270
GOLDTXT = hexc("#b37a12")
GREEN = hexc("#3c8d4f")

CAMERA = {"hook": "push_in", "doctor": "pan_right", "writer": "push_in", "jurassic": "dutch", "works": "pan_left",
          "lesson": "pull_out", "outro": "pan_right"}
TRANSITIONS = {"doctor": "fade", "writer": "zoom", "jurassic": "whip", "works": "iris", "lesson": "fade",
               "outro": "whip"}


def ap(t, a, dur=0.38):
    return pop(t, a - 0.2, dur)


def mc(g, x, sc=0.72, mood="smile", pose="down", turn=0.0, talk=False, look=None):
    person(g, x, GROUND, look or CRICHTON, sc, mood=mood, pose=pose, turn=turn, seed=8, talk=talk)


def jungle(g, t, a=1.0):
    """พุ่มไม้ป่าดึกดำบรรพ์ (เฟิร์น) ด้านหลัง"""
    with g.alpha(a):
        for i in range(9):
            x = -100 + i * 150
            for k in range(5):
                ang = math.radians(-150 + k * 30 + 4 * math.sin(t + i))
                g.line([(x, GROUND), (x + 220 * math.cos(ang), GROUND - 60 + 220 * math.sin(ang))], 16,
                       hexc("#9cbf7a"), amp=0)


# ------------------------------------------------------------------ 1. hook
def s_hook(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:   # วันที่ + ไข่ไดโนเสาร์สั่น
        with g.at(CX, 900, pop(t, 0.5), 8 * math.sin(t * 12) * seg(t, 1.0, 3.0)):
            g.blob(0, 0, 120, 160, hexc("#efe6cf"), 7)
            for i in range(5):
                g.circle(-50 + i * 25, -60 + (i % 2) * 70, 12, hexc("#c9b98f"), 0)
        g.label("วันนี้ในอดีต", CX, 380, 104, sc=lerp(2.0, 1, e_out(seg(t, 0.1, 0.4))) if t > 0.1 else 0, rot=-3)
        g.label("23 ตุลาคม 1942", CX, 520, 84, color=GREEN, sc=pop(t, 0.8))
        return
    if t < L[2] - 0.2:   # เด็กร่างโย่งในชิคาโก
        for i in range(6):   # เส้นขอบตึกชิคาโก
            g.rrect(-80 + i * 200, GROUND - 300 - (i * 97) % 280, 150, 300 + (i * 97) % 280, 4, hexc("#e7e1d3"), 4)
        mc(g, CX, 0.72, "smile", "wave", look=STUDENT)
        g.label("ชิคาโก", CX, 380, 100, color=NAVY, sc=ap(t, L[1]), rot=-3)
        g.label("เด็กชายร่างโย่ง", CX, 500, 58, color=GREY, sc=ap(t, L[1] + 0.4))
        return
    if t < L[4] - 0.2:   # นักศึกษาแพทย์ฮาร์วาร์ด + กล้องจุลทรรศน์
        mc(g, 260, 0.7, "neutral" if t < L[3] else "worry", "think" if t > L[3] else "down", 0.4, look=STUDENT)
        microscope(g, 760, GROUND, 1.3 * ap(t, L[2] + 0.3), t)
        if t < L[3] - 0.2:
            g.label("นักศึกษาแพทย์ฮาร์วาร์ด", CX, 380, 80, color=hexc("#a8323a"), sc=ap(t, L[2]), rot=-3)
        else:
            with g.at(800, 540, ap(t, L[3])):
                g.circle(0, 0, 140, WHITE, 8)
                for i in range(5):
                    a = t * 0.8 + i * 1.3
                    g.blob(60 * math.cos(a), 50 * math.sin(a * 1.3), 22, 16, (0.55, 0.8, 0.5, 1), 4, seed=i)
            g.label("ความน่ากลัวใต้กล้องจุลทรรศน์", CX, 360, 62, color=RED, sc=ap(t, L[3]), rot=-3)
        return
    if t < L[5] - 0.2:   # ปลุกไดโนเสาร์
        jungle(g, t, 0.7)
        trex(g, lerp(1300, 620, e_out(seg(t, L[4], L[4] + 2.0))), GROUND, 0.75, t, roar=max(0, math.sin(t * 3)),
             flip=True)
        g.label('ปลุก "ไดโนเสาร์" ฟื้นคืนชีพ!', CX, 380, 76, color=GREEN, sc=ap(t, L[4]), rot=-3)
        return
    mc(g, 300, 0.72, "smile", "point", 0.3)
    trex(g, 820, GROUND, 0.5, t, roar=0.3 + 0.3 * math.sin(t * 2), flip=True, walk=False)
    g.label('"ไมเคิล ไครช์ตัน"!', CX, 380, 96, color=GOLDTXT, sc=ap(t, L[5]), rot=-3)


# ------------------------------------------------------------------ 2. doctor
def s_doctor(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:
        mc(g, 300, 0.72, "smile", "down" if t < L[1] else "hold", 0.3)
        g.name_tag(t, 0.2, 790, 1130, "ไมเคิล ไครช์ตัน", "นักเขียน-ผู้กำกับ (1942–2008)", side=-1)
        if t < L[1] - 0.2:
            g.label("ไม่ใช่แค่นักเขียนนิยาย", CX, 380, 80, sc=ap(t, 0.2), rot=-3)
        else:
            with g.at(770, 640, ap(t, L[1]), -4):
                g.rrect(-170, -110, 340, 220, 16, WHITE, 7)
                g.label("หัวกะทิ", 0, -30, 60, color=hexc("#a8323a"))
                g.label("แพทย์ฮาร์วาร์ด", 0, 50, 40, color=GREY)
            g.label("นักเรียนแพทย์ระดับหัวกะทิ", CX, 380, 72, color=hexc("#a8323a"), sc=ap(t, L[1]), rot=-3)
        return
    if t < L[4] - 0.2:   # ใบประกอบวิชาชีพ -> หันหลังให้วงการแพทย์
        turn_away = t > L[3] - 0.2
        mc(g, 300 if not turn_away else 260, 0.72, "neutral" if turn_away else "smile", "stop" if turn_away else "down",
           -0.6 if turn_away else 0.3)
        with g.at(760, 700, ap(t, L[2]), 5):
            g.rrect(-200, -140, 400, 280, 12, hexc("#f4efe2"), 7)
            g.label("ใบประกอบวิชาชีพ", 0, -70, 40, color=NAVY)
            g.label("M.D.", 0, 20, 80, color=GOLDTXT)
            g.circle(130, 90, 34, RED, 4)
        if turn_away:
            g.label("หันหลังให้วงการแพทย์!", CX, 380, 78, color=RED, sc=ap(t, L[3]), rot=-3)
        else:
            g.label("กำลังจะคว้าใบประกอบ", CX, 380, 80, sc=ap(t, L[2]), rot=-3)
        return
    for i in range(6):   # วิทยาศาสตร์วิ่งเร็วเกินไป
        u = (t * 0.9 + i / 6) % 1
        x = -150 + 1350 * u
        y = 700 + (i % 3) * 140
        if i % 3 == 0:
            dna(g, x, y, 180, t, 0.6)
        elif i % 3 == 1:
            chip(g, x, y, 0.4, t)
        else:
            microscope(g, x, y + 120, 0.5, t)
        g.line([(x - 140, y), (x - 260, y)], 6, GREY, amp=0)
    if t < L[5] - 0.2:
        g.label("เทคโนโลยีวิ่งเร็วเกินไป!", CX, 380, 80, color=RED, sc=ap(t, L[4]), rot=-3)
    else:
        g.label("มนุษย์อาจควบคุมไม่ได้!", CX, 380, 80, color=RED, sc=ap(t, L[5]), rot=-3)


# ------------------------------------------------------------------ 3. writer
def s_writer(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[3] - 0.2:   # จับปากกา: วิทยาศาสตร์ + ระทึกขวัญ
        mc(g, 260, 0.72, "smile", "hold", 0.3)
        with g.at(720, 760, ap(t, 0.3)):
            g.rrect(-180, -240, 360, 480, 10, WHITE, 7)
            n = int(10 * seg(t, 0.4, L[3] - 0.4))
            for i in range(n):
                g.line([(-140, -190 + i * 42), (140 - 60 * (i % 3), -190 + i * 42)], 6, GREY, amp=0)
        if t < L[1] - 0.2:
            g.label("ผันตัวมาจับปากกา", CX, 380, 90, color=NAVY, sc=ap(t, 0.2), rot=-3)
        elif t < L[2] - 0.2:
            g.label("วิทยาศาสตร์ + ระทึกขวัญ", CX, 380, 80, color=GREEN, sc=ap(t, L[1]), rot=-3)
        else:
            g.label("ลายเซ็นเฉพาะตัว", CX, 380, 90, color=GOLDTXT, sc=ap(t, L[2]), rot=-3)
        return
    if t < L[5] - 0.2:   # คำถามบ้าคลั่ง
        mc(g, 300, 0.72, "smug", "think", 0.3)
        for i in range(3):
            u = (t * 0.5 + i / 3) % 1
            g.circle(400 + 60 * u, 560 - 240 * u, 14 + 24 * u, WHITE, 5)
        g.label("?", 760, 700, 220 + 10 * math.sin(t * 4), color=RED, sc=ap(t, L[4]))
        if t < L[4] - 0.2:
            g.label("ผลงานที่เปลี่ยนวงการหนัง", CX, 380, 74, sc=ap(t, L[3]), rot=-3)
        else:
            g.label("คำถามอันบ้าคลั่ง...", CX, 380, 90, color=RED, sc=ap(t, L[4]), rot=-3)
        return
    if t < L[6] - 0.2:   # ยุงในอำพัน -> ดีเอ็นเอ
        amber(g, 330, 800, 1.5 * ap(t, L[5]), t, 1.0)
        if t > L[5] + 0.8:
            dna(g, 800, 780, 500, t, ap(t, L[5] + 1.0))
        g.label("ดีเอ็นเอจากยุงในอำพัน", CX, 380, 78, color=GOLDTXT, sc=ap(t, L[5]), rot=-3)
        return
    dna(g, 220, 780, 500, t, 0.8)   # โคลนไดโนเสาร์
    trex(g, 760, GROUND, 0.75 * ap(t, L[6] + 0.3), t, roar=0.5, flip=True, walk=False)
    g.label("โคลนขึ้นมาใหม่...?", CX, 380, 96, color=GREEN, sc=ap(t, L[6]), rot=-3)


# ------------------------------------------------------------------ 4. jurassic
def s_jurassic(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:   # นวนิยาย Jurassic Park
        g.sunburst(CX, 760, 220, 520, 18, t * 10, 10, (0.98, 0.8, 0.35, 0.6))
        book(g, CX, 780, 1.4 * ap(t, 0.3), 4 * math.sin(t * 1.5))
        g.label('"Jurassic Park"!', CX, 360, 100, color=hexc("#c8323a"), sc=ap(t, 0.2), rot=-3)
        g.label("นวนิยาย 1990", CX, 1120, 56, color=GREY, sc=ap(t, 0.8))
        return
    if t < L[2] - 0.2:   # ถูกสัตว์ดึกดำบรรพ์ไล่ล่า (วิ่งหนี ไม่มีบาดเจ็บ)
        jungle(g, t, 0.6)
        run = (t - L[1]) * 260
        for i, lk in enumerate(CROWD[:2]):
            person(g, 980 - (run + i * 160) % 1300, GROUND, lk, 0.48, mood="shock", pose="v", turn=-0.6,
                   seed=20 + i, shadow=False)
        trex(g, 1250 - run % 1300 + 300, GROUND, 0.6, t, roar=1.0, flip=True)
        g.label("ถูกไดโนเสาร์ไล่ล่า!", CX, 380, 92, color=RED, sc=ap(t, L[1]), rot=-3)
        return
    if t < L[6] - 0.2:   # เตือนสติ: เล่นบทพระเจ้า -> ธรรมชาติลงโทษ
        dna(g, 300, 780, 520, t * (3 if t > L[4] else 1), 0.9)
        mc(g, 760, 0.62, "smug" if t < L[5] else "shock", "point" if t < L[5] else "stop", -0.3)
        if t < L[3] - 0.2:
            g.label("เตือนสติมนุษย์อย่างเจ็บแสบ", CX, 380, 72, color=RED, sc=ap(t, L[2]), rot=-3)
        elif t < L[4] - 0.2:
            g.label("เล่นบทเป็นพระเจ้า?", CX, 380, 92, color=GOLDTXT, sc=ap(t, L[3]), rot=-3)
        elif t < L[5] - 0.2:
            g.label("ควบคุมพันธุกรรมตามใจ", CX, 380, 80, color=NAVY, sc=ap(t, L[4]), rot=-3)
        else:
            for i in range(3):
                g.line([(80 + i * 140, 520 + i * 80), (180 + i * 140, 640 + i * 80)], 8, GREEN, amp=0)
            g.label("ธรรมชาติลงโทษเรา!", CX, 380, 92, color=GREEN, sc=ap(t, L[5]), rot=-3)
        return
    if t < L[7] - 0.2:   # สปีลเบิร์กสร้างหนัง
        person(g, 260, GROUND, SPIELBERG, 0.72, mood="smile", pose="point", turn=0.3, seed=30)
        clapper(g, 760, 820, 1.2 * ap(t, L[6]), e_io(seg(t, L[6] + 0.8, L[6] + 1.2)) * (1 - seg(t, L[6] + 1.4, L[6] + 1.7)))
        g.name_tag(t, L[6] + 0.2, 440, 1130, "สตีเวน สปีลเบิร์ก", "ผู้กำกับ Jurassic Park (1993)")
        g.label("สร้างเป็นภาพยนตร์!", CX, 380, 90, color=NAVY, sc=ap(t, L[6]), rot=-3)
        return
    if t < L[8] - 0.2:   # ไดโนเสาร์อาละวาด รายได้ถล่มทลาย
        money_rain(g, t)
        trex(g, CX + 60, GROUND, 0.8, t, roar=max(0.0, math.sin(t * 3)), flip=True, walk=False)
        g.label("รายได้ถล่มทลาย!", CX, 380, 100, color=GREEN, sc=ap(t, L[7]), rot=-3)
        return
    for i, lk in enumerate(CROWD):   # ไดโนเสาร์ฟีเวอร์ทั่วโลก
        x = 200 + i * 340
        person(g, x, GROUND, lk, 0.6, mood="smile", pose="wave" if i == 1 else "hold", turn=0.2 - 0.2 * i, seed=40 + i)
        with g.at(x + 90, GROUND - 330, 0.18, 0):
            trex(g, 0, 0, 1.0, t + i, walk=False)
    g.label("ไดโนเสาร์ฟีเวอร์ทั่วโลก!", CX, 380, 82, color=GOLDTXT, sc=ap(t, L[8]), rot=-3)


# ------------------------------------------------------------------ 5. works
def s_works(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:   # ER
        cross_sign(g, 720, 720 + 14 * math.sin(t * 2), 1.4 * ap(t, 0.3) * (1 + 0.04 * math.sin(t * 5)))
        mc(g, 260, 0.72, "smile", "point", 0.3)
        g.label('ซีรีส์การแพทย์ "ER"', CX, 380, 90, color=RED, sc=ap(t, 0.2), rot=-3)
        return
    reveal = e_io(seg(t, L[2], L[2] + 1.2))   # Westworld หุ่นยนต์คาวบอย
    with g.at(0, 0, 1, 0):
        robot_cowboy(g, 640 + 40 * math.sin(t * 1.5), GROUND, 1.2 * ap(t, L[1]), t, reveal)
    if t < L[2] - 0.2:
        g.label('"Westworld" (1973)', CX, 380, 90, color=GOLDTXT, sc=ap(t, L[1]), rot=-3)
        return
    chip(g, 230, 760 + 12 * math.sin(t * 2), 0.9 * ap(t, L[2] + 0.4), t)
    if t < L[3] - 0.2:
        g.label("ปัญญาประดิษฐ์", CX, 380, 100, color=NAVY, sc=ap(t, L[2]), rot=-3)
    else:
        g.label("ก่อนยุคอินเทอร์เน็ต!", CX, 380, 90, color=RED, sc=ap(t, L[3]), rot=-3)


# ------------------------------------------------------------------ 6. lesson
def s_lesson(g, t, L, d):
    g.ground(GROUND, WHITE)
    g.label("บทเรียน", CX, 340, 100, sc=ap(t, 0.2), rot=-3)
    if t < L[2] - 0.2:
        g.sunburst(CX, 820, 120, 300, 14, t * 10, 10, (0.98, 0.8, 0.35, 0.7 * ap(t, L[1])))
        dna(g, CX, 820, 460, t, ap(t, 0.4))
        if t > L[1] - 0.2:
            g.label("พลังอันยิ่งใหญ่", CX, 490, 66, color=GOLDTXT, sc=ap(t, L[1]))
        return
    if t < L[3] - 0.2:
        for i, (txt, col) in enumerate((("ความรับผิดชอบ", GREEN), ("จริยธรรม", NAVY))):
            with g.at(290 + i * 500, 800 + 10 * math.sin(t * 2 + i), ap(t, L[2] + 0.4 * i)):
                g.rrect(-210, -70, 420, 140, 30, WHITE, 7, stroke=col)
                g.label(txt, 0, 0, 50, color=col)
        g.label("ถ้าขาดสิ่งนี้...", CX, 490, 66, color=RED, sc=ap(t, L[2]))
        return
    trex(g, CX + 120, GROUND, 0.75, t, roar=max(0.0, math.sin(t * 3)), flip=True, walk=False)   # ย้อนกลับมากลืนกิน
    g.label("ย้อนกลับมากลืนกินเรา...", CX, 490, 66, color=RED, sc=ap(t, L[3]))


# ------------------------------------------------------------------ 7. outro
def s_outro(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:
        mc(g, CX, 0.72, "smile", "wave", 0.0, talk=True)
        g.label("แล้วทุกคนล่ะครับ", CX, 380, 90, sc=ap(t, 0.2), rot=-3)
        return
    if t < L[3] - 0.2:   # AI + พันธุวิศวกรรม -> โลกในนิยาย?
        chip(g, 280, 760 + 12 * math.sin(t * 2), 1.0 * ap(t, L[1]), t)
        dna(g, 780, 780, 480, t * 2, ap(t, L[1] + 0.4))
        if t < L[2] - 0.2:
            g.label("AI + พันธุวิศวกรรม", CX, 380, 90, color=NAVY, sc=ap(t, L[1]), rot=-3)
        else:
            book(g, CX, 1050, 0.6 * ap(t, L[2]), 6)
            g.label("ใกล้โลกในนิยายแล้วหรือยัง?", CX, 380, 70, color=RED, sc=ap(t, L[2]), rot=-3)
        return
    if t < L[5] - 0.2:   # ควรสร้าง Jurassic Park จริงไหม
        jungle(g, t, 0.5)
        trex(g, 620, GROUND, 0.7, t, roar=0.3, flip=True, walk=False)
        for i, (txt, col, x) in enumerate((("สร้าง!", GREEN, 220), ("ไม่ควร!", RED, 860))):
            with g.at(x, 600, ap(t, L[4] + 0.3 * i) * (1 + 0.04 * math.sin(t * 3 + i))):
                g.rrect(-130, -60, 260, 120, 30, WHITE, 7, stroke=col)
                g.label(txt, 0, 0, 52, color=col)
        if t < L[4] - 0.2:
            g.label("ถ้าโคลนไดโนเสาร์ได้จริง...", CX, 380, 74, sc=ap(t, L[3]), rot=-3)
        else:
            g.label('ควรสร้าง "Jurassic Park" ไหม?', CX, 380, 68, color=GOLDTXT, sc=ap(t, L[4]), rot=-3)
        return
    with g.at(CX + 170, 640, ap(t, L[5])):   # ชวนคอมเมนต์
        g.bubble(0, 0, 460, 220, WHITE, tail=(-1, 1))
        for i in range(3):
            g.circle(-110 + i * 110, 0, 24 + 6 * math.sin(t * 6 - i), INK, 0)
    mc(g, 250, 0.72, "smile", "wave", 0.3, talk=True)
    g.label("คอมเมนต์แลกเปลี่ยนกันได้เลย!", CX, 360, 70, color=RED, sc=ap(t, L[5]), rot=-3)


SCENES = {
    "hook": s_hook, "doctor": s_doctor, "writer": s_writer, "jurassic": s_jurassic, "works": s_works,
    "lesson": s_lesson, "outro": s_outro,
}
NO_IRIS = set()
