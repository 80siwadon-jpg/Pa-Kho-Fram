"""ฉากตอน: ผู้ป่วยไข้ทรพิษตามธรรมชาติคนสุดท้าย (26 ต.ค. 1977) — ไม่แสดงอาการน่ากลัว"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from chars import (ALI, ALI_OLD, DOCTOR, KIDS, WHO_BLUE, WORKERS, certificate, contact_web, drops,  # noqa: E402
                   emblem, hospital, ring, skull_scale, somalia_map, spots, stopwatch_globe, syringe,
                   thermometer, virus)
from gfx import GOLD, GOLD2, GREY, INK, NAVY, RED, W, WHITE, e_io, e_out, hexc, lerp, pop, seg  # noqa: E402
from people import person  # noqa: E402

CX = W / 2
GROUND = 1270
GOLDTXT = hexc("#b37a12")
GREEN = hexc("#3c8d4f")
DARK = hexc("#4a3a3a")

CAMERA = {"hook": "push_in", "ali": "pan_right", "killer": "dutch", "hunt": "pan_left", "win": "push_in",
          "polio": "pan_right", "lesson": "pull_out", "outro": "pan_left"}
TRANSITIONS = {"ali": "fade", "killer": "whip", "hunt": "zoom", "win": "iris", "polio": "fade", "lesson": "whip",
               "outro": "zoom"}


def ap(t, a, dur=0.38):
    return pop(t, a - 0.2, dur)


def title(g, t, a, txt, col=INK, size=84, y=380):
    g.label(txt, CX, y, size, color=col, sc=ap(t, a), rot=-3)


def ali(g, x, sc=0.8, mood="worry", pose="down", sick=0.0, t=0.0, turn=0.3, look=ALI):
    person(g, x, GROUND, look, sc, mood=mood, pose=pose, turn=turn, seed=3)
    if sick > 0:
        spots(g, x, GROUND - 815 * sc, 1.0, sick, 11)


# ------------------------------------------------------------------ 1. hook
def s_hook(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:
        virus(g, CX, 860, 160 * pop(t, 0.3) + 1, t)
        g.label("วันนี้ในอดีต", CX, 380, 104, sc=lerp(2.0, 1, e_out(seg(t, 0.1, 0.4))) if t > 0.1 else 0, rot=-3)
        g.label("26 ตุลาคม 1977", CX, 520, 84, color=GOLDTXT, sc=pop(t, 0.6))
        return
    if t < L[2] - 0.2:   # พ่อครัวในโรงพยาบาล ติดเชื้อปริศนา
        hospital(g, 740, GROUND, 0.8)
        ali(g, 280, 0.82, "worry", "think", e_io(seg(t, L[1] + 0.5, L[1] + 1.8)), t)
        title(g, t, L[1], "ตุ่มหนองปริศนา!", RED, 96)
        return
    if t < L[3] - 0.2:   # มนุษย์คนสุดท้ายของโลก
        ali(g, CX, 0.9, "firm", "down", 0.0, t, 0)
        g.label("1", CX + 260, 700, 220, color=RED, sc=ap(t, L[2] + 0.3), rot=8)
        title(g, t, L[2], "\"มนุษย์คนสุดท้ายของโลก\"", NAVY, 80)
        return
    virus(g, 320, 820, 130, t)
    with g.at(320, 820, ap(t, L[3] + 0.4)):
        g.line([(-180, -180), (180, 180)], 18, RED, amp=0)
    skull_scale(g, 760, 820, 0.7, e_out(seg(t, L[3], L[3] + 1.2)))
    g.label("หลายร้อยล้านชีวิต", 760, 1080, 56, color=DARK, sc=ap(t, L[3] + 0.3))
    title(g, t, L[3], "ปิดฉากมัจจุราชตลอดกาล!", GREEN, 84)


# ------------------------------------------------------------------ 2. ali
def s_ali(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # 1977 เมอร์กา โซมาเลีย
        if t < L[1] - 0.2:
            g.calendar(CX, 820, 1.1 * pop(t, 0.2), "26", "พุธ", "ต.ค. 1977")
            title(g, t, L[0], "26 ตุลาคม 1977", GOLDTXT, 92)
        else:
            somalia_map(g, CX, 840, 1.1, t, ap(t, L[1] + 0.4))
            title(g, t, L[1], "เมืองเมอร์กา ประเทศโซมาเลีย", INK, 76)
        return
    if t < L[5] - 0.2:   # อาลี 23 ปี ไข้สูง ตุ่ม
        ali(g, 290, 0.85, "smile" if t < L[3] - 0.2 else "worry", "down" if t < L[3] - 0.2 else "think",
            e_io(seg(t, L[4], L[4] + 1.2)), t)
        g.name_tag(t, L[2] + 0.1, 680, 1150, "อาลี มาว มาอลิน", "พ่อครัวโรงพยาบาล วัย 23 ปี")
        if t < L[3] - 0.2:
            title(g, t, L[2], "พ่อครัวหนุ่มวัย 23 ปี", NAVY, 86)
        elif t < L[4] - 0.2:
            thermometer(g, 740, 900, 1.2 * ap(t, L[3]) + 0.01, 10, e_out(seg(t, L[3], L[3] + 1.0)))
            g.sweat(330, 470 + 10 * math.sin(t * 5), 1.5)
            title(g, t, L[3], "ไข้สูง ปวดเมื่อยตามตัว", RED, 86)
        else:
            title(g, t, L[4], "ตุ่มหนองผุดทั่วใบหน้า!", RED, 86)
        return
    if t < L[6] - 0.2:   # หมอคิดว่าอีสุกอีใส
        person(g, 260, GROUND, DOCTOR, 0.8, mood="smile", pose="point", turn=0.4, seed=4, talk=True)
        ali(g, 840, 0.75, "worry", "down", 1.0, t, -0.4)
        with g.at(560, 600, ap(t, L[5])):
            g.bubble(0, 0, 300, 130, WHITE, tail=(-1, 1))
            g.label("อีสุกอีใสน่า", 0, 0, 50, color=GREEN)
        title(g, t, L[5], "หมอคิดว่าแค่อีสุกอีใส", INK, 84, y=330)
        return
    if t < L[8] - 0.2:   # แล็บยืนยัน -> เหงื่อตก
        if t < L[7] - 0.2:
            with g.at(CX, 820, ap(t, L[6]), 4 * math.sin(t * 2)):
                g.rrect(-260, -300, 520, 600, 12, WHITE, 7)
                g.label("LAB RESULT", 0, -220, 56, color=WHO_BLUE)
                for i in range(4):
                    g.line([(-200, -120 + i * 60), (200 - 60 * (i % 2), -120 + i * 60)], 6, GREY, amp=0)
                g.label("POSITIVE", 0, 170, 70, color=RED, sc=ap(t, L[6] + 0.8), rot=-8)
            title(g, t, L[6], "ผลแล็บยืนยันออกมา...", INK, 86)
        else:
            for i in range(3):
                person(g, 230 + i * 300, GROUND, WORKERS[i], 0.58, mood="shock", pose="shrug", turn=0.2 - 0.2 * i,
                       seed=10 + i)
                g.sweat(270 + i * 300, 650 + 10 * math.sin(t * 6 + i), 1.3)
            title(g, t, L[7], "สาธารณสุขทั่วโลกเหงื่อตก!", RED, 82)
        return
    virus(g, CX, 820, 200 * ap(t, L[8]) + 1, t)
    title(g, t, L[8], "\"ไข้ทรพิษ\" หรือ \"ฝีดาษ\"!", RED, 92)


# ------------------------------------------------------------------ 3. killer
def s_killer(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:   # หลายพันปี
        for i in range(5):
            virus(g, 180 + i * 180, 780 + 80 * math.sin(t * 1.5 + i), 60, t + i)
        yr = int(lerp(-3000, 1977, e_io(seg(t, 0.2, L[1] - 0.3))))
        g.label(f"{abs(yr)} {'ปีก่อน ค.ศ.' if yr < 0 else ''}".strip(), CX, 1080, 70, color=DARK)
        title(g, t, L[0], "หลอกหลอนมนุษย์นับพันปี", DARK, 84)
        return
    if t < L[2] - 0.2:   # 300 ล้านคน
        skull_scale(g, CX, 820, 1.4, e_out(seg(t, L[1], L[1] + 1.5)))
        n = int(lerp(0, 300, e_out(seg(t, L[1], L[1] + 1.5))))
        g.label(f"{n} ล้านคน", CX, 1150, 90, color=RED, sc=ap(t, L[1]))
        title(g, t, L[1], "ศตวรรษที่ 20 เพียงศตวรรษเดียว", INK, 76)
        return
    for i, (lab, h, col) in enumerate((("ไข้ทรพิษ", 600, RED), ("สงครามโลก\nทุกครั้ง", 330, GREY))):   # เปรียบเทียบ
        x = 330 + i * 420
        hh = h * e_out(seg(t, L[2], L[2] + 1.2))
        g.rrect(x - 110, GROUND - hh, 220, hh + 1, 10, col, 6)
        for j, ln in enumerate(lab.split("\n")):
            g.label(ln, x, GROUND - hh - 90 + j * 56 - 28 * (lab.count("\n")), 52, color=col)
    title(g, t, L[2], "มากกว่าสงครามโลกรวมกัน!", RED, 84)


# ------------------------------------------------------------------ 4. hunt
def s_hunt(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # WHO โค้งสุดท้าย
        emblem(g, CX, 800, 160 * ap(t, L[0]) + 1, t)
        if t < L[1] - 0.2:
            title(g, t, L[0], "องค์การอนามัยโลก (WHO)", WHO_BLUE, 84)
        else:
            for i in range(6):
                a = i * 1.047 + t * 0.5
                virus(g, CX + 330 * math.cos(a), 800 + 300 * math.sin(a), 34, t, col=hexc("#c9ced6"))
            title(g, t, L[1], "โค้งสุดท้ายของการกวาดล้าง", NAVY, 78)
        return
    if t < L[4] - 0.2:   # ผู้ป่วยคนเดียว = สะเก็ดไฟ
        somalia_map(g, CX, 840, 1.0, t, 1.0)
        if t > L[3] - 0.2:
            for i in range(8):
                u = (t * 1.5 + i / 8) % 1
                g.star(CX - 60 + 120 * math.cos(i) * u * 2, 1000 - 200 * u, 22 * (1 - u) + 4,
                       (0.98, 0.6, 0.2, 1 - u), 0, pts=6, inner=0.5)
            title(g, t, L[3], "สะเก็ดไฟที่พร้อมลุกโชน!", RED, 84)
        else:
            title(g, t, L[2], "พบผู้ป่วยเพียงคนเดียว...", DARK, 84)
        return
    if t < L[6] - 0.2:   # ล่าแต้ม / กักตัว
        if t < L[5] - 0.2:
            for i in range(3):
                person(g, 200 + i * 300, GROUND, WORKERS[i], 0.62, mood="firm", pose="fist" if i == 1 else "point",
                       turn=0.3, seed=10 + i)
            title(g, t, L[4], "เปิดปฏิบัติการล่าแต้ม!", WHO_BLUE, 86)
        else:
            ali(g, CX, 0.75, "worry", "down", 1.0, t, 0)
            ring(g, CX, 900, 330, t, 1.0, RED)
            title(g, t, L[5], "กักตัวอาลีอย่างแน่นหนา", RED, 84)
        return
    if t < L[8] - 0.2:   # แกะรอย 161 คน
        k = 0.15 + 0.85 * e_out(seg(t, L[6] - 0.2, L[7] + 1.0))
        g.label("อาลี", CX, 1000, 50, color=RED)
        with g.at(CX, 820, 1 + 0.04 * math.sin(t * 2), 6 * math.sin(t * 0.8)):
            contact_web(g, 0, 0, t, k, 161, 330)
        if t < L[7] - 0.2:
            title(g, t, L[6], "แกะรอยทุกคนที่เจอเขา", NAVY, 84)
        else:
            g.label(f"{int(161 * k)} คน", CX, 1220, 90, color=RED, sc=ap(t, L[7]))
            title(g, t, L[7], "รวมกว่า 161 คน!", RED, 92)
        return
    contact_web(g, CX, 820, t, 1.0, 161, 300)   # ล้อมรั้วไข่แดง
    ring(g, CX, 820, 370, t, e_out(seg(t, L[8], L[8] + 1.2)))
    if t > L[9] - 0.2:
        for i in range(6):
            a = i * 1.047 + t * 0.4
            syringe(g, CX + 440 * math.cos(a), 820 + 420 * math.sin(a), 0.35, math.degrees(a) + 180, 1.0)
        title(g, t, L[9], "ไม่ให้เชื้อเล็ดลอดแม้ก้าวเดียว", NAVY, 78, y=330)
    else:
        title(g, t, L[8], "ฉีดวัคซีน \"ล้อมรั้วไข่แดง\"", WHO_BLUE, 80, y=330)


# ------------------------------------------------------------------ 5. win
def s_win(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[3] - 0.2:   # ปาฏิหาริย์ หายดี ไม่มีใครติด
        heal = 1 - e_io(seg(t, L[1], L[1] + 1.5))
        ali(g, 300, 0.85, "smile" if t > L[1] else "worry", "v" if t > L[2] - 0.2 else "down", heal, t)
        if t < L[1] - 0.2:
            for i in range(5):
                g.sparkle(300 + 280 * math.cos(i * 1.26 + t), 760 + 260 * math.sin(i * 1.26 + t), 30)
            title(g, t, L[0], "ปาฏิหาริย์เกิดขึ้นจริง...", GOLDTXT, 86)
        elif t < L[2] - 0.2:
            title(g, t, L[1], "อาลีรักษาจนหายดี!", GREEN, 90)
        else:
            g.label("0", 760, 760, 260, color=GREEN, sc=ap(t, L[2] + 0.2))
            g.label("ผู้ติดเชื้อต่อ", 760, 1000, 60, color=GREEN, sc=ap(t, L[2] + 0.4))
            title(g, t, L[2], "ไม่มีใครติดต่อแม้แต่คนเดียว!", GREEN, 78)
        return
    if t < L[4] - 0.2:   # คนสุดท้ายในประวัติศาสตร์
        ali(g, CX, 0.9, "smile", "down", 0.0, t, 0)
        with g.at(CX, 470, ap(t, L[3]), -4):
            g.rrect(-330, -70, 660, 140, 36, WHITE, 8, stroke=RED)
            g.label("ผู้ติดเชื้อตามธรรมชาติคนสุดท้าย", 0, 0, 46, color=RED)
        title(g, t, L[3], "คนสุดท้ายในประวัติศาสตร์!", NAVY, 82, y=330)
        return
    certificate(g, 330, 860, 0.95 * ap(t, L[4]) + 0.01, -4, t)   # ประกาศ 1980
    stopwatch_globe(g, 790, 820, 150, t, e_io(seg(t, L[4], L[4] + 1.5)))
    for i in range(5):
        g.sparkle(790 + 220 * math.cos(i * 1.26 + t), 820 + 220 * math.sin(i * 1.26 + t), 28)
    title(g, t, L[4], "WHO ประกาศกวาดล้างสำเร็จ 1980!", GREEN, 74)


# ------------------------------------------------------------------ 6. polio
def s_polio(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # อุทิศชีวิต รณรงค์โปลิโอ
        ali(g, 300, 0.85, "smile", "hold", 0.0, t, 0.4, ALI_OLD)
        drops(g, 520, 760, 0.9, t)
        if t < L[1] - 0.2:
            for i in range(4):
                g.sparkle(300 + 220 * math.cos(i * 1.57 + t), 700 + 200 * math.sin(i * 1.57 + t), 28)
            title(g, t, L[0], "หลังจากรอดตาย...", GOLDTXT, 90)
        else:
            title(g, t, L[1], "อาสารณรงค์วัคซีนโปลิโอ", WHO_BLUE, 82)
        return
    if t < L[3] - 0.2:   # ปกป้องเด็ก ๆ
        ali(g, 240, 0.8, "smile", "point", 0.0, t, 0.4, ALI_OLD)
        drops(g, 400, 700, 0.6, t)
        for i, k in enumerate(KIDS):
            person(g, 640 + i * 230, GROUND, k, 0.8, mood="smile", pose="wave" if i else "down", turn=-0.3,
                   seed=40 + i)
        title(g, t, L[2], "ปกป้องเด็ก ๆ จากโรคร้าย", GREEN, 84)
        return
    c = g.c   # เสียชีวิตขณะปฏิบัติหน้าที่ (ภาพสงบ: เทียน + รูปแบบไอคอน)
    with g.at(CX, 800, ap(t, L[3])):
        g.rrect(-220, -280, 440, 520, 16, hexc("#f4eedf"), 8)
        g.circle(0, -80, 90, hexc("#6e4a30"), 6)
        g.rrect(-130, 30, 260, 150, 60, WHO_BLUE, 6)
        g.label("อาลี มาว มาอลิน", 0, 210, 40)
    for sx in (-1, 1):
        x = CX + sx * 320
        g.rrect(x - 26, 1000, 52, 200, 8, WHITE, 5)
        g.poly([(x, 930 + 6 * math.sin(t * 7 + sx)), (x + 18, 990), (x, 1005), (x - 18, 990)], GOLD2, 3, amp=0,
               smooth=True)
    title(g, t, L[3], "จากไปขณะปฏิบัติหน้าที่", NAVY, 84)


# ------------------------------------------------------------------ 7. lesson
def s_lesson(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:
        for i in range(3):
            person(g, 200 + i * 340, GROUND, WORKERS[i], 0.65, mood="smile", pose="v" if t > L[1] - 0.2 else "down",
                   turn=0.2 - 0.2 * i, seed=10 + i)
        if t < L[1] - 0.2:
            title(g, t, L[0], "เรื่องนี้พิสูจน์ให้เห็นว่า...", INK, 84)
        else:
            title(g, t, L[1], "วิทยาศาสตร์ + ความร่วมมือ", WHO_BLUE, 84)
        return
    stopwatch_globe(g, CX, 840, 200, t, 1.0)
    if t < L[3] - 0.2:
        virus(g, CX + 260, 600, 80, t)
        title(g, t, L[2], "แม้โรคร้ายที่น่ากลัวที่สุด...", DARK, 82)
    else:
        for i in range(6):
            g.sparkle(CX + 300 * math.cos(i * 1.05 + t), 840 + 300 * math.sin(i * 1.05 + t), 32)
        title(g, t, L[3], "ก็แพ้พลังแห่งความหวัง!", GREEN, 86)


# ------------------------------------------------------------------ 8. outro
def s_outro(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[3] - 0.2:
        person(g, 260, GROUND, WORKERS[0], 0.8, mood="smile" if t < L[1] - 0.2 else "think",
               pose="wave" if t < L[1] - 0.2 else "think", turn=0.4, seed=10, talk=True)
        if t < L[1] - 0.2:
            certificate(g, 740, 820, 0.6, 5, t)
            title(g, t, L[0], "ชัยชนะเหนือไข้ทรพิษ", GREEN, 86)
        elif t < L[2] - 0.2:
            for i in range(3):
                virus(g, 600 + i * 160, 700 + 120 * (i % 2), 55, t + i, col=hexc("#c86a8a"))
            title(g, t, L[1], "โรคระบาดใหม่เกิดบ่อยขึ้น...", DARK, 80)
        else:
            stopwatch_globe(g, 740, 820, 140, t, 0.5)
            for i in range(6):
                a = i * 1.047 + t * 0.4
                g.circle(740 + 210 * math.cos(a), 820 + 210 * math.sin(a), 28, hexc("#f2c9a8"), 5)
            title(g, t, L[2], "ยังจับมือกันได้อยู่ไหม?", NAVY, 84)
        return
    with g.at(CX + 170, 640, ap(t, L[3])):   # ชวนคอมเมนต์
        g.bubble(0, 0, 460, 220, WHITE, tail=(-1, 1))
        for i in range(3):
            g.circle(-110 + i * 110, 0, 24 + 6 * math.sin(t * 6 - i), INK, 0)
    ali(g, 250, 0.8, "smile", "wave", 0.0, t, 0.3)
    title(g, t, L[3], "คอมเมนต์แลกเปลี่ยนกันได้เลย!", RED, 64)


SCENES = {
    "hook": s_hook, "ali": s_ali, "killer": s_killer, "hunt": s_hunt, "win": s_win, "polio": s_polio,
    "lesson": s_lesson, "outro": s_outro,
}
NO_IRIS = set()
