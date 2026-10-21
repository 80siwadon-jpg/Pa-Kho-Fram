"""ฉากตอน: ธีโอดอร์ โรสเวลต์ (เกิด 27 ต.ค. 1858) — จากเด็กหอบหืดสู่ชายเหล็กที่ถูกยิงแล้วปราศรัยต่อ"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from chars import (AIDE, FATHER, RIDERS, TEDDY, TEDDY_FIT, TEDDY_KID, TEDDY_RR, _load, ambulance, bed, brain,  # noqa: E402
                   canal, crowd_mass, dna, dumbbell, flash, glasses_case, glove, gunman, horse, lungs, monopoly,
                   moose, mountain, podium, speech, stain, stick, tree, wheeze)
from gfx import GOLD, GOLD2, GREY, INK, NAVY, RED, W, WHITE, e_io, e_out, hexc, lerp, pop, seg  # noqa: E402
from people import person  # noqa: E402
from photos import photo  # noqa: E402

clock = _load("boeing707_1958").clock

CX = W / 2
GROUND = 1270
GOLDTXT = hexc("#b37a12")
GREEN = hexc("#3c8d4f")
BROWN = hexc("#7a4a2a")

CAMERA = {"hook": "push_in", "child": "pan_right", "train": "dutch", "president": "pan_left", "shot": "push_in",
          "lesson": "pull_out", "outro": "pan_right"}
TRANSITIONS = {"child": "zoom", "train": "whip", "president": "iris", "shot": "zoom", "lesson": "fade",
               "outro": "whip"}


def ap(t, a, dur=0.38):
    return pop(t, a - 0.2, dur)


def title(g, t, a, txt, col=INK, size=84, y=380):
    g.label(txt, CX, y, size, color=col, sc=ap(t, a), rot=-3)


def teddy(g, x, sc=0.82, mood="firm", pose="down", turn=0.2, talk=False, look=TEDDY, seed=3):
    person(g, x, GROUND, look, sc, mood=mood, pose=pose, turn=turn, seed=seed, talk=talk)


def kid(g, x, sc=0.85, mood="worry", pose="down", turn=0.3, look=TEDDY_KID, talk=False):
    person(g, x, GROUND, look, sc, mood=mood, pose=pose, turn=turn, seed=5, talk=talk)


def rally(g, t, x=CX, k=1.0):
    """ฝูงชนเรือนหมื่นด้านหน้าเวที"""
    crowd_mass(g, 120, 960, GROUND + 10, t, rows=3, k=k)


def year_card(g, x, y, sc, txt, col=INK, rot=0.0):
    with g.at(x, y, sc, rot):
        g.rrect(-190, -90, 380, 180, 30, WHITE, 8, stroke=col)
        g.text(txt, 0, 0, 100, "kanit", col)


# ------------------------------------------------------------------ 1. hook
def s_hook(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:   # วันนี้ในอดีต
        moose(g, CX, 980, 1.0 * pop(t, 0.2) + 0.01, t)
        g.label("วันนี้ในอดีต", CX, 380, 104, sc=lerp(2.0, 1, e_out(seg(t, 0.1, 0.4))) if t > 0.1 else 0, rot=-3)
        g.label("27 ตุลาคม 1858", CX, 520, 84, color=GOLDTXT, sc=pop(t, 0.5))
        return
    if t < L[2] - 0.2:   # ถูกยิงในระยะเผาขน (เงา + แสงวาบ ไม่แสดงการโดน)
        gunman(g, 840, GROUND, 0.78, ap(t, L[1]))
        teddy(g, 300, 0.82, "shock" if t > L[1] + 1.0 else "firm", "down", 0.4)
        flash(g, 580, 760, 120, seg(t, L[1] + 0.8, L[1] + 1.3))
        if t > L[1] + 2.4:
            g.label("ไม่ไปโรงพยาบาล!", 320, 600, 62, color=RED, sc=ap(t, L[1] + 2.4), rot=-5)
        title(g, t, L[1], "ถูกยิงแสกหน้าอกในระยะเผาขน!", RED, 76)
        return
    if t < L[3] - 0.2:   # ขึ้นเวทีปราศรัย 90 นาที
        teddy(g, 380, 0.75, "firm", "point", 0.3, talk=True)
        stain(g, 400, 820, 18 * ap(t, L[2] + 1))
        podium(g, 540, GROUND - 120, 0.8)
        rally(g, t)
        clock(g, 800, 700, 100, lerp(0, 18, seg(t, L[2], L[3])) % 12 + 0.01, t, RED)
        g.label("90 นาที!", 800, 860, 64, color=RED, sc=ap(t, L[2] + 0.8))
        title(g, t, L[2], "ปราศรัยต่อ 90 นาที ทั้งที่เลือดโชก!", INK, 72)
        return
    teddy(g, 700, 0.84, "firm" if t < L[4] - 0.2 else "smile", "fist" if t < L[4] - 0.2 else "wave", -0.2)
    for i in range(4):
        g.sparkle(700 + 260 * math.cos(i * 1.6 + t), 820 + 240 * math.sin(i * 1.6 + t), 24)
    g.name_tag(t, L[3] + 0.2, 330, 1020, "ธีโอดอร์ โรสเวลต์", "ประธานาธิบดีสหรัฐฯ คนที่ 26", dur=4.0, side=1)
    if t < L[4] - 0.2:   # ชายผู้แข็งแกร่งที่สุด + ภาพจริง
        title(g, t, L[3], "ชายผู้แข็งแกร่งที่สุด!", GOLDTXT, 92)
    else:
        title(g, t, L[4], "\"ธีโอดอร์ โรสเวลต์\"", NAVY, 96)


# ------------------------------------------------------------------ 2. child
def s_child(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:   # 27 ต.ค. 1858 นิวยอร์ก
        g.calendar(CX, 860, 1.25 * ap(t, L[0]) + 0.01, 27, "พุธ", "ต.ค. 1858")
        g.label("นครนิวยอร์ก", CX, 1150, 64, color=NAVY, sc=ap(t, L[0] + 1.2))
        title(g, t, L[0], "27 ตุลาคม 1858", GOLDTXT, 92)
        return
    if t < L[3] - 0.2:   # เท็ดดี้ลืมตาดูโลก / ไม่มีใครคิดว่าจะรอด
        kid(g, CX, 0.85, "smile" if t < L[2] - 0.2 else "worry", "down", 0.0)
        if t < L[2] - 0.2:
            g.label("\"เท็ดดี้\"", CX, 560, 90, color=RED, sc=ap(t, L[1] + 0.3), rot=-4)
            title(g, t, L[1], "เด็กชายธีโอดอร์ ลืมตาดูโลก", INK, 78)
        else:
            for i, sx in enumerate((-1, 1)):
                g.label("?", CX + sx * 260, 700 + 20 * math.sin(t * 3 + i), 130, color=GREY, sc=ap(t, L[2] + 0.2 * i))
            title(g, t, L[2], "จะรอดจนโตไหม?", GREY, 92)
        return
    if t < L[6] - 0.2:   # หอบหืด / ผอม / ทรมาน
        if t < L[4] - 0.2 or t > L[5] - 0.2:
            bed(g, CX, GROUND, 1.0, t)
            with g.at(CX - 120, GROUND - 165, 0.55):
                from people import head
                head(g, TEDDY_KID, "worry", 0, 0.4, (0, 0), 5, 4.5)
            wheeze(g, CX - 40, GROUND - 230, t)
            if t < L[4] - 0.2:
                title(g, t, L[3], "โรคหอบหืดรุนแรง", RED, 92)
            else:
                g.label("หายใจไม่ออก...", CX + 120, 760, 66, color=GREY, sc=ap(t, L[5] + 0.3), rot=4)
                title(g, t, L[5], "ทรมานอยู่บ่อยครั้ง", NAVY, 92)
        else:
            kid(g, CX, 0.85, "sad", "down", 0.0)
            g.label("ผอมแห้ง", CX - 250, 820, 60, color=GREY, sc=ap(t, L[4]), rot=-6)
            g.label("อ่อนแอ", CX + 250, 900, 60, color=GREY, sc=ap(t, L[4] + 0.5), rot=6)
            title(g, t, L[4], "ร่างกายผอมแห้ง อ่อนแอ", INK, 86)
        return
    # คำพูดของพ่อ
    person(g, 300, GROUND, FATHER, 0.82, mood="firm", pose="point" if t > L[8] - 0.2 else "down", turn=0.4,
           seed=9, talk=True)
    kid(g, 780, 0.8, "smile" if t > L[8] + 1.0 else "worry", "fist" if t > L[8] + 1.0 else "down", -0.4)
    if t < L[7] - 0.2:
        title(g, t, L[6], "ประโยคเปลี่ยนชีวิตจากพ่อ", INK, 82)
    elif t < L[8] - 0.2:
        brain(g, 760, 640, 0.8 * ap(t, L[7]) + 0.01, t)
        title(g, t, L[7], "\"สมองยอดเยี่ยม แต่ร่างกายต้องสู้\"", NAVY, 72)
    else:
        title(g, t, L[8], "\"สร้างร่างกายขึ้นมาใหม่!\"", RED, 82)


# ------------------------------------------------------------------ 3. train
def s_train(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:   # ออกกำลังกายอย่างบ้าคลั่ง
        y = 20 * abs(math.sin(t * 6))
        with g.at(0, -y):
            kid(g, CX, 0.85, "firm", "v" if math.sin(t * 6) > 0 else "fist", 0.0)
        title(g, t, L[0], "ออกกำลังกายอย่างบ้าคลั่ง!", RED, 82)
        return
    if t < L[2] - 0.2:   # มวย / น้ำหนัก / ปีนเขา / ม้า
        items = [(glove, 290, 600, "ชกมวย"), (dumbbell, 790, 600, "ยกน้ำหนัก")]
        for i, (fn, x, y, txt) in enumerate(items):
            k = ap(t, L[1] + 0.5 * i, 0.3)
            if k > 0.02:
                fn(g, x, y, 0.8 * k, 10 * math.sin(t * 3 + i))
                g.label(txt, x, y + 130, 50, color=INK, sc=k)
        k = ap(t, L[1] + 1.0, 0.3)
        if k > 0.02:
            mountain(g, 290, GROUND, 0.55 * k, t)
            g.label("ปีนเขา", 290, GROUND - 300, 50, sc=k)
        k = ap(t, L[1] + 1.5, 0.3)
        if k > 0.02:
            horse(g, 740, GROUND, 0.5 * k, t, 1.0, TEDDY_FIT, 0.0)
            g.label("ควบม้า", 790, GROUND - 330, 50, sc=k)
        title(g, t, L[1], "ฝึกหนักทุกรูปแบบ", INK, 88)
        return
    if t < L[4] - 0.2:   # ชีวิตกลางแจ้ง → ชายเหล็ก
        if t < L[3] - 0.2:
            mountain(g, 760, GROUND, 0.9, t)
            for i, x in enumerate((180, 330)):
                tree(g, x, GROUND, 0.8, t)
            teddy(g, 520, 0.78, "smile", "wave", 0.0, look=TEDDY_FIT)
            title(g, t, L[2], "ชีวิตกลางแจ้งสุดสมบุกสมบัน", GREEN, 76)
        else:
            teddy(g, CX, 0.88, "firm", "fist", 0.0, look=TEDDY_FIT)
            for i in range(3):
                u = (t * 1.2 + i / 3) % 1
                g.arc(CX, 800, 300 + 120 * u, 200, 340, 8, (*GOLD2[:3], 1 - u))
            title(g, t, L[3], "\"ชายเหล็ก\" ผู้ไม่กลัวสิ่งใด!", GOLDTXT, 82)
        return
    if t < L[6] - 0.2:   # รัฟ ไรเดอร์ส / สงครามสเปน-อเมริกา
        horse(g, lerp(380, 560, seg(t, L[4], L[6])), GROUND, 0.72, t, 1.0, TEDDY_RR, 0.9)
        if t < L[5] - 0.2:
            g.label("Rough Riders", CX, 520, 64, color=BROWN, sc=ap(t, L[4] + 0.5))
            title(g, t, L[4], "ผู้นำฝูงรบ \"รัฟ ไรเดอร์ส\"", BROWN, 82)
        else:
            year_card(g, 820, 620, 0.7 * ap(t, L[5]) + 0.01, "1898", RED, 6)
            title(g, t, L[5], "สงครามสเปน-อเมริกา", RED, 86)
        return
    teddy(g, 320, 0.82, "smile", "wave", 0.3)   # ประธานาธิบดีอายุน้อยที่สุด
    g.flag(640, 560, 260, 170, "us", t)
    g.line([(640, 560), (640, GROUND)], 8, INK, amp=0)
    if t < L[7] - 0.2:
        title(g, t, L[6], "ประธานาธิบดีที่อายุน้อยที่สุด!", NAVY, 80)
    else:
        with g.at(780, 960, ap(t, L[7]) * (1 + 0.04 * math.sin(t * 5)), 6):
            g.circle(0, 0, 150, GOLD, 8)
            g.text("42", 0, -10, 130, "kanit", INK)
            g.text("ปี", 0, 80, 46, "kanitsb", INK)
        title(g, t, L[7], "ด้วยวัยเพียง 42 ปี", RED, 92)


# ------------------------------------------------------------------ 4. president
def s_president(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # พูดจาอ่อนหวาน ถือไม้พลอง
        teddy(g, 330, 0.84, "smile", "down" if t < L[1] - 0.2 else "hold", 0.3, talk=True)
        if t < L[1] - 0.2:
            title(g, t, L[0], "ปรัชญาของผู้นำ", INK, 92)
        else:
            stick(g, 470, GROUND - 160, 1.0 * ap(t, L[1] + 0.3) + 0.01, 20 + 4 * math.sin(t * 2))
            with g.at(760, 660, ap(t, L[1])):
                g.bubble(0, 0, 340, 170, WHITE, tail=(-1, 1))
                g.label("พูดอ่อนหวาน", 0, 0, 52, color=GREEN)
            title(g, t, L[1], "แต่ถือไม้พลองกระบองยักษ์!", BROWN, 80)
        return
    if t < L[3] - 0.2:   # ทลายกลุ่มทุนผูกขาด
        monopoly(g, 640, GROUND, 1.0, e_io(seg(t, L[2] + 0.6, L[2] + 1.4)))
        teddy(g, 240, 0.72, "angry", "fist", 0.4)
        title(g, t, L[2], "ทลายกลุ่มทุนผูกขาด!", RED, 88)
        return
    if t < L[4] - 0.2:   # 230 ล้านเอเคอร์
        for i in range(6):
            k = ap(t, L[3] + 0.2 * i, 0.3)
            if k > 0.02:
                tree(g, 170 + i * 150, GROUND - (i % 2) * 40, (0.7 + 0.15 * (i % 3)) * k, t)
        g.label("230 ล้านเอเคอร์", CX, 600, 96, color=GREEN, sc=ap(t, L[3] + 0.8), rot=-3)
        title(g, t, L[3], "ปกป้องป่าไม้และอุทยานแห่งชาติ", GREEN, 76)
        return
    if t < L[5] - 0.2:   # คลองปานามา
        canal(g, CX, 1100, 1.0, t)
        title(g, t, L[4], "ผลักดันคลองปานามาจนสำเร็จ", NAVY, 78)
        return
    if t < L[7] - 0.2:   # 1912 เดินสายหาเสียง
        teddy(g, CX, 0.8, "smile", "wave", 0.0, talk=True)
        rally(g, t)
        year_card(g, 800, 620, 0.7 * ap(t, L[5]) + 0.01, "1912", RED, 6)
        if t < L[6] - 0.2:
            title(g, t, L[5], "ความอึดระดับตำนาน", GOLDTXT, 88)
        else:
            title(g, t, L[6], "ระหว่างเดินสายหาเสียง", INK, 86)
        return
    gunman(g, 840, GROUND, 0.78, 1.0)   # มือปืน (เงา) — ตัดก่อนกระสุนโดน
    teddy(g, 300, 0.8, "shock", "down", 0.4)
    flash(g, 580, 760, 140, seg(t, L[7] + 1.0, L[7] + 1.6))
    title(g, t, L[7], "มือปืนชักปืนยิงใส่หน้าอก!", RED, 80)


# ------------------------------------------------------------------ 5. shot
def s_shot(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:   # กระเป๋าแว่นโลหะ + สุนทรพจน์ 50 แผ่น
        glasses_case(g, 320, 760, 1.0 * ap(t, L[0] + 0.2) + 0.01, -8 + 2 * math.sin(t * 2))
        speech(g, 720, 900, 1.0 * ap(t, L[0] + 1.6) + 0.01, 6 + 2 * math.sin(t * 2))
        g.label("กระเป๋าแว่นโลหะ", 320, 600, 50, color=GREY, sc=ap(t, L[0] + 0.4))
        title(g, t, L[0], "โชคดี! มีของกันกระสุน", GREEN, 86)
        return
    if t < L[2] - 0.2:   # ไม่โดนปอด
        lungs(g, CX, 860, 1.6, ap(t, L[1] + 1.0) > 0.5)
        g.label("ไม่โดนปอด!", CX, 1170, 80, color=GREEN, sc=ap(t, L[1] + 1.0))
        title(g, t, L[1], "กระสุนฝังในกล้ามเนื้อหน้าอก", INK, 78)
        return
    if t < L[3] - 0.2:   # ไม่ขึ้นรถพยาบาล
        ambulance(g, 720, GROUND, 0.9, 0)
        teddy(g, 260, 0.78, "firm", "stop", 0.4)
        g.c.save()
        g.line([(560, 760), (900, 1100)], 18, RED, amp=0)
        g.c.restore()
        title(g, t, L[2], "ไม่ยอมขึ้นรถพยาบาล!", RED, 86)
        return
    if t < L[4] - 0.2:   # ไอเช็คเลือด
        teddy(g, 340, 0.84, "firm", "fist", 0.3)
        for i in range(3):
            u = (t * 1.6 + i / 3) % 1
            g.arc(470 + 60 * u, 590, 30 + 30 * u, -50, 50, 6, (*GREY[:3], 1 - u))
        g.label("แค่ก ๆ!", 640, 600, 64, color=GREY, sc=ap(t, L[3] + 0.2), rot=5)
        with g.at(760, 860, ap(t, L[3] + 1.0)):
            g.circle(0, 0, 110, WHITE, 8, stroke=GREEN)
            g.line([(-50, 0), (-10, 40), (60, -40)], 16, GREEN, amp=0)
        g.label("ไม่มีเลือด", 760, 1030, 52, color=GREEN, sc=ap(t, L[3] + 1.0))
        title(g, t, L[3], "ไอเช็คว่าไม่มีเลือด", INK, 86)
        return
    if t < L[5] - 0.2:   # ไปหอประชุมทันที
        teddy(g, 300, 0.82, "firm", "point", 0.4, talk=True)
        person(g, 800, GROUND, AIDE, 0.72, mood="shock", pose="down", turn=-0.4, seed=11)
        title(g, t, L[4], "\"พาผมไปหอประชุมเดี๋ยวนี้!\"", RED, 78)
        return
    # บนเวที
    podium(g, 640, GROUND - 120, 0.8)
    rally(g, t)
    if t < L[7] - 0.2:
        teddy(g, 360, 0.76, "firm", "hold" if t < L[6] - 0.2 else "point", 0.3, talk=t > L[6] - 0.2)
        stain(g, 380, 830, 26 * ap(t, L[5] + 0.8))
        if t < L[6] - 0.2:
            title(g, t, L[5], "ปลดกระดุมเสื้อให้ทุกคนเห็น", INK, 78)
        else:
            title(g, t, L[6], "แล้วกล่าวอย่างเลือดเย็น...", NAVY, 84)
        return
    if t < L[8] - 0.2:   # Bull Moose
        moose(g, CX - 40, 1000, 1.0, t)
        with g.at(CX, 640, ap(t, L[7])):
            g.bubble(0, 0, 760, 200, WHITE, tail=(-1, 1))
            g.label("\"แค่นี้ฆ่ากวางมูสอย่างผมไม่ได้!\"", 0, 0, 52, color=BROWN)
        title(g, t, L[7], "Bull Moose!", BROWN, 96)
        return
    teddy(g, 340, 0.76, "firm", "point", 0.3, talk=True)   # ชั่วโมงครึ่ง
    stain(g, 360, 830, 26)
    clock(g, 800, 680, 110, lerp(0, 1.5, seg(t, L[8], L[8] + 2.0)), t, RED)
    g.label("ชั่วโมงครึ่ง!", 800, 850, 60, color=RED, sc=ap(t, L[8] + 0.6))
    title(g, t, L[8], "ปราศรัยจนจบ!", RED, 96)


# ------------------------------------------------------------------ 6. lesson
def s_lesson(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:
        if not photo(g, "teddy", CX, 840, 460, 560, -3, ap(t, L[0]), 1.0 + 0.03 * t, label="ธีโอดอร์ โรสเวลต์"):
            teddy(g, CX, 0.86, "firm", "down", 0.0)
        title(g, t, L[0], "เรื่องราวนี้พิสูจน์ว่า...", INK, 86)
        return
    if t < L[2] - 0.2:   # จุดเริ่มต้นที่อ่อนแอไม่ใช่ข้ออ้าง
        k = e_io(seg(t, L[1] + 0.3, L[1] + 1.8))
        kid(g, 280, 0.8, "worry", "down", 0.3)
        g.label("→", CX, 860, 110, color=GREY, sc=ap(t, L[1] + 0.6))
        if k > 0.02:
            teddy(g, 790, 0.8 * k, "firm", "fist", -0.2)
        title(g, t, L[1], "จุดเริ่มต้นที่อ่อนแอไม่ใช่ข้ออ้าง", INK, 76)
        return
    if t < L[3] - 0.2:   # ไม่ได้มาจากพันธุกรรม
        dna(g, CX, 860, 1.0, t)
        k = seg(t, L[2] + 1.0, L[2] + 1.8)
        if k > 0:
            g.line([(CX - 260, 620), (CX - 260 + 520 * k, 620 + 500 * k)], 18, RED, amp=0)
        title(g, t, L[2], "ไม่ได้มาจากพันธุกรรม", NAVY, 86)
        return
    teddy(g, CX, 0.88, "firm", "fist", 0.0)   # จิตใจไม่ยอมแพ้
    for i in range(6):
        g.sparkle(CX + 330 * math.cos(i * 1.05 + t), 820 + 260 * math.sin(i * 1.05 + t), 26)
    title(g, t, L[3], "จิตใจที่ไม่ยอมแพ้ต่อโชคชะตา", GOLDTXT, 76)


# ------------------------------------------------------------------ 7. outro
def s_outro(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:
        teddy(g, 300, 0.82, "smile", "wave", 0.3, look=TEDDY_RR)
        moose(g, 760, 1080, 0.6, t)
        title(g, t, L[0], "รู้สึกอย่างไรกันบ้าง?", INK, 90)
        return
    if t < L[3] - 0.2:   # อะไรทำให้ยืนพูดต่อได้
        podium(g, 640, GROUND - 120, 0.8)
        rally(g, t)
        teddy(g, 360, 0.76, "firm", "point", 0.3, talk=True)
        stain(g, 380, 830, 26)
        if t < L[2] - 0.2:
            title(g, t, L[1], "ถ้าคุณโดนยิงขนาดนั้น...", RED, 84)
        else:
            g.label("?", 800, 700, 160, color=RED, sc=ap(t, L[2] + 0.4), rot=8)
            title(g, t, L[2], "อะไรทำให้ยังยืนพูดต่อได้?", INK, 80)
        return
    if t < L[4] - 0.2:   # ชอบมุมไหน
        for i, (lk, txt, col) in enumerate(((TEDDY_RR, "ทหารม้า", BROWN), (TEDDY, "ผู้นำ", NAVY),
                                            (TEDDY_FIT, "นักสู้", RED))):
            k = ap(t, L[3] + 0.3 * i, 0.3)
            if k > 0.02:
                person(g, 230 + i * 290, GROUND, lk, 0.62 * k, mood="smile", pose="down", turn=0.2 - 0.2 * i,
                       seed=20 + i)
                g.label(txt, 230 + i * 290, 600, 56, color=col, sc=k)
        title(g, t, L[3], "ชอบมุมไหนเป็นพิเศษ?", GOLDTXT, 86)
        return
    with g.at(CX + 170, 640, ap(t, L[4])):   # ชวนคอมเมนต์
        g.bubble(0, 0, 460, 220, WHITE, tail=(-1, 1))
        for i in range(3):
            g.circle(-110 + i * 110, 0, 24 + 6 * math.sin(t * 6 - i), INK, 0)
    teddy(g, 270, 0.8, "smile", "wave", 0.3, talk=True)
    title(g, t, L[4], "มาแลกเปลี่ยนกันในคอมเมนต์!", RED, 70)


SCENES = {
    "hook": s_hook, "child": s_child, "train": s_train, "president": s_president, "shot": s_shot,
    "lesson": s_lesson, "outro": s_outro,
}
NO_IRIS = set()
