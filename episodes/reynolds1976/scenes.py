"""ฉากตอน: วันเกิดไรอัน เรย์โนลด์ส (23 ต.ค. 1976)"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from chars import (DP_RED, EXECS, FANS, GL_GREEN, RYAN, RYAN_YOUNG, camera, flop_chart, hero, laptop,  # noqa: E402
                   maple, money_rain, poison, rated_r, ring, star_walk, zipper_mouth)
from gfx import GOLD2, GREY, INK, NAVY, RED, W, WHITE, e_io, e_out, hexc, lerp, pop, seg  # noqa: E402
from people import person  # noqa: E402

CX = W / 2
GROUND = 1270
GOLDTXT = hexc("#b37a12")
GREEN = hexc("#3c8d4f")

CAMERA = {"hook": "push_in", "flops": "dutch", "dream": "pan_right", "success": "push_in", "lesson": "pull_out",
          "outro": "pan_left"}
TRANSITIONS = {"flops": "whip", "dream": "fade", "success": "zoom", "lesson": "iris", "outro": "whip"}


def ap(t, a, dur=0.38):
    return pop(t, a - 0.2, dur)


def ryan(g, x, sc=0.8, mood="smug", pose="down", turn=0.0, talk=False):
    person(g, x, GROUND, RYAN, sc, mood=mood, pose=pose, turn=turn, seed=5, talk=talk)


def execs(g, t, mood="smug", pose="cross", x0=170, gap=330, sc=0.6):
    for i, lk in enumerate(EXECS):
        person(g, x0 + i * gap, GROUND, lk, sc, mood=mood, pose=pose if i != 1 else "point", turn=0.3 - 0.3 * i,
               seed=20 + i, talk=True)


# ------------------------------------------------------------------ 1. hook
def s_hook(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:
        with g.at(CX, 860, pop(t, 0.5), 6 * math.sin(t * 2)):
            maple(g, 0, 0, 1.6)
        g.label("วันนี้ในอดีต", CX, 380, 104, sc=lerp(2.0, 1, e_out(seg(t, 0.1, 0.4))) if t > 0.1 else 0, rot=-3)
        g.label("23 ตุลาคม 1976", CX, 520, 84, color=RED, sc=pop(t, 0.8))
        return
    if t < L[2] - 0.2:   # แวนคูเวอร์ แคนาดา
        for i in range(7):
            h = 260 + (i * 131) % 300
            g.rrect(-60 + i * 170, GROUND - h, 130, h, 4, hexc("#dfe8ee"), 4)
        person(g, CX, GROUND, RYAN_YOUNG, 1.1, mood="smile", pose="wave", turn=0.1, seed=2)
        maple(g, 860, 560 + 10 * math.sin(t * 2), 0.6 * ap(t, L[1] + 0.3), 8 * math.sin(t))
        g.label("แวนคูเวอร์ แคนาดา", CX, 380, 90, color=RED, sc=ap(t, L[1]), rot=-3)
        return
    if t < L[5] - 0.2:   # หนุ่มหล่อ -> ยาพิษบ็อกซ์ออฟฟิศ -> เจ๊ง
        ryan(g, 280, 0.82, "smile" if t < L[3] else "worry", "down" if t < L[4] else "shrug", 0.3)
        if t < L[3] - 0.2:
            for i in range(3):
                u = (t * 0.6 + i / 3) % 1
                g.sparkle(380 + 80 * i, 560 - 60 * u, 22, GOLD2)
            g.label("นักแสดงหนุ่มหน้าหล่อ", CX, 380, 84, color=NAVY, sc=ap(t, L[2]), rot=-3)
        elif t < L[4] - 0.2:
            poison(g, 760, 980 + 10 * math.sin(t * 2), 1.3 * ap(t, L[3]), 6 * math.sin(t * 1.5))
            g.label('"ยาพิษแห่งบ็อกซ์ออฟฟิศ"', CX, 380, 78, color=hexc("#6a3f8a"), sc=ap(t, L[3]), rot=-3)
        else:
            flop_chart(g, 560, 1150, 420, 460, e_io(seg(t, L[4], L[4] + 1.5)))
            g.label("เจ๊งยับเยิน!", CX, 380, 110, color=RED, sc=ap(t, L[4]), rot=-3)
        return
    g.sunburst(CX, 760, 260, 640, 20, t * 10, 10, (0.98, 0.7, 0.6, 0.5))   # ซูเปอร์ฮีโร่ พันล้าน
    if t < L[6] - 0.2:
        money_rain(g, t)
        hero(g, CX, GROUND, 0.82, "point", 0.1)
        g.label("ซูเปอร์ฮีโร่สุดเกรียน", CX, 360, 84, color=RED, sc=ap(t, L[5]), rot=-3)
        g.label("รายได้ระดับพันล้าน!", CX, 480, 60, color=GREEN, sc=ap(t, L[5] + 0.5))
        return
    ryan(g, CX, 0.85, "smug", "cross", 0.0)
    g.label('"ไรอัน เรย์โนลด์ส"!', CX, 380, 96, color=GOLDTXT, sc=ap(t, L[6]), rot=-3)


# ------------------------------------------------------------------ 2. flops
def s_flops(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # ไม่ได้โรยด้วยกลีบกุหลาบ / บทตลกและหนังรัก
        ryan(g, 300, 0.82, "smile", "wave" if t > L[1] else "down", 0.3, talk=t > L[1])
        g.name_tag(t, 0.2, 790, 1130, "ไรอัน เรย์โนลด์ส", "นักแสดงชาวแคนาดา (เกิด 1976)", side=-1)
        if t < L[1] - 0.2:
            g.label("เส้นทางไม่ได้โรยด้วยกลีบกุหลาบ", CX, 380, 64, sc=ap(t, 0.2), rot=-3)
        else:
            for i, (txt, col) in enumerate((("หนังตลก", GOLDTXT), ("หนังรักคอมเมดี้", RED))):
                with g.at(760, 600 + i * 170, ap(t, L[1] + 0.4 * i), (i * 2 - 1) * 4):
                    g.rrect(-170, -55, 340, 110, 20, WHITE, 6, stroke=col)
                    g.label(txt, 0, 0, 44, color=col)
            g.label("เล่นมานับไม่ถ้วน", CX, 380, 90, color=NAVY, sc=ap(t, L[1]), rot=-3)
        return
    if t < L[6] - 0.2:   # โลกซูเปอร์ฮีโร่ -> Green Lantern เจ๊ง -> โดนล้อ
        if t < L[3] - 0.2:
            ryan(g, 300, 0.82, "smile", "point", 0.3)
            g.label("ก้าวสู่โลกซูเปอร์ฮีโร่", CX, 380, 84, color=NAVY, sc=ap(t, L[2]), rot=-3)
            for i in range(4):
                g.star(560 + i * 120, 760 + 20 * math.sin(t * 3 + i), 30, GOLD2, 4)
            return
        if t < L[4] - 0.2:
            ryan(g, 300, 0.82, "shock", "down", 0.3)
            g.label("โชคชะตาเล่นตลก...", CX, 380, 90, color=RED, sc=ap(t, L[3]), rot=-3)
            return
        dim = e_io(seg(t, L[4] + 0.6, L[4] + 1.6))
        ring(g, 330, 840, 1.6 * ap(t, L[4]), t, 1 - dim, dim)
        flop_chart(g, 560, 1150, 400, 420, e_io(seg(t, L[4], L[4] + 1.5)))
        if t < L[5] - 0.2:
            g.label("Green Lantern เจ๊ง!", CX, 380, 90, color=GL_GREEN, sc=ap(t, L[4]), rot=-3)
        else:
            for i in range(4):
                u = (t * 0.6 + i / 4) % 1
                g.label("ฮ่า ๆ", 180 + i * 240, 700 - 120 * u, 52, color=RED, a=1 - u)
            g.label("ตราบาปที่ถูกล้อเลียน", CX, 380, 84, color=RED, sc=ap(t, L[5]), rot=-3)
        return
    if t < L[8] - 0.2:   # Wolverine เวอร์ชันแรก: เดดพูลถูกปิดปาก
        hero(g, 300, GROUND, 0.82, "down", 0.2, "worry")
        zipper_mouth(g, 760, 760 + 10 * math.sin(t * 2), 1.4 * ap(t, L[6] + 0.5))
        if t < L[7] - 0.2:
            g.label("Wolverine เวอร์ชันแรก (2009)", CX, 380, 70, color=hexc("#a8771e"), sc=ap(t, L[6]), rot=-3)
        else:
            g.label("ถูกเย็บปากปิดสนิท!", CX, 380, 86, color=RED, sc=ap(t, L[7]), rot=-3)
        return
    execs(g, t)   # ผู้บริหารฟันธง
    if t < L[9] - 0.2:
        g.label("เสน่ห์ความกวนพังพินาศ", CX, 380, 80, color=GREY, sc=ap(t, L[8]), rot=-3)
    elif t < L[10] - 0.2:
        for i in range(3):
            g.label("ไม่!", 170 + i * 330, 560 + 15 * math.sin(t * 6 + i), 60, color=RED, sc=ap(t, L[9] + 0.2 * i))
        g.label("ผู้บริหารส่ายหน้า", CX, 380, 90, color=NAVY, sc=ap(t, L[9]), rot=-3)
    else:
        g.label("ไม่มีวันเป็นพระเอกแถวหน้า!", CX, 380, 72, color=RED, sc=ap(t, L[10]), rot=-3)


# ------------------------------------------------------------------ 3. dream
def s_dream(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[3] - 0.2:   # ไม่ยอมแพ้ + รักเดดพูล + เกิดมาเพื่อบทนี้
        ryan(g, 280, 0.82, "firm" if t < L[1] else "smile", "fist" if t < L[1] else "hold", 0.3)
        if t < L[1] - 0.2:
            g.label("ไม่ยอมให้ความฝันจบลง!", CX, 380, 80, color=NAVY, sc=ap(t, 0.2), rot=-3)
            return
        hero(g, 780, GROUND, 0.75, "wave", -0.3)
        for i in range(3):
            u = (t * 0.6 + i / 3) % 1
            g.label("รัก", 520 + 30 * i, 640 - 140 * u, 44, color=RED, a=1 - u)
        if t < L[2] - 0.2:
            g.label('หลงรัก "เดดพูล"', CX, 380, 96, color=DP_RED, sc=ap(t, L[1]), rot=-3)
        else:
            g.label("บทที่เกิดมาเพื่อเขา", CX, 380, 90, color=GOLDTXT, sc=ap(t, L[2]), rot=-3)
        return
    if t < L[4] - 0.2:   # 10 ปีที่ไม่มีใครเหลียวแล
        with g.at(CX, 760, ap(t, L[3])):
            g.rrect(-220, -150, 440, 300, 24, WHITE, 8)
            g.rrect(-220, -150, 440, 90, 24, GREY, 8)
            g.text("รอคอย", 0, -105, 44, "kanit", WHITE)
            n = 2004 + int(10 * seg(t, L[3] + 0.2, L[4] - 0.5))
            g.label(str(n), 0, 50, 120)
        g.label("กว่า 10 ปีที่ไม่มีใครเหลียวแล", CX, 380, 70, color=GREY, sc=ap(t, L[3]), rot=-3)
        return
    if t < L[6] - 0.2:   # ควักเงินตัวเอง จ้างคนเขียนบท / ถ่ายฟุตเทจทดสอบ
        ryan(g, 280, 0.8, "smile", "point" if t > L[5] else "hold", 0.3)
        if t < L[5] - 0.2:
            with g.at(760, 820, ap(t, L[4]), 4 * math.sin(t * 2)):
                g.rrect(-180, -230, 360, 460, 10, WHITE, 7)
                for i in range(8):
                    g.line([(-140, -180 + i * 50), (140 - 50 * (i % 3), -180 + i * 50)], 6, GREY, amp=0)
            money_rain(g, t, 4, 500, 1000, 400, 1100)
            g.label("ควักเงินตัวเอง จ้างคนเขียนบท", CX, 380, 66, sc=ap(t, L[4]), rot=-3)
        else:
            camera(g, 760, 820, 1.1 * ap(t, L[5]), t)
            g.label("แอบถ่ายฟุตเทจทดสอบ", CX, 380, 80, color=RED, sc=ap(t, L[5]), rot=-3)
        return
    if t < L[7] - 0.2:   # มืดแปดด้าน
        g.c.rectangle(-500, 140, 2100, 1130)
        g.c.set_source_rgba(0.12, 0.14, 0.22, 0.85)
        g.c.fill()
        ryan(g, CX, 0.82, "sad", "think", 0.0)
        g.label("มืดแปดด้าน...", CX, 380, 100, color=hexc("#2b3a5a"), sc=ap(t, L[6]), rot=-3)
        return
    laptop(g, CX, 1100, 1.4, t, ap(t, L[7] + 0.4))   # ฟุตเทจหลุด!
    for i in range(5):
        u = (t * 0.8 + i / 5) % 1
        g.label("?", 150 + i * 200, 900 - 300 * u, 70, color=RED, a=1 - u)
    g.label('ฟุตเทจลับ "หลุด"!', CX, 380, 100, color=RED, sc=ap(t, L[7]), rot=-3)


# ------------------------------------------------------------------ 4. success
def s_success(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # แฟนหนังกรีดร้อง เรียกร้อง
        for i, lk in enumerate(FANS):
            person(g, 200 + i * 340, GROUND, lk, 0.62, mood="shock" if t < L[1] else "smile", pose="wave",
                   turn=0.2 - 0.2 * i, seed=30 + i, talk=True)
        for i in range(5):
            u = (t * 0.7 + i / 5) % 1
            g.label("สร้างเลย!", 160 + i * 200, 700 - 200 * u, 40, color=RED, a=1 - u)
        if t < L[1] - 0.2:
            g.label("คลิปแพร่ไปทั่วโลก!", CX, 380, 88, color=RED, sc=ap(t, 0.2), rot=-3)
        else:
            g.label("ค่ายหนังต้านไม่ไหว!", CX, 380, 90, color=GREEN, sc=ap(t, L[1]), rot=-3)
        return
    if t < L[3] - 0.2:   # Deadpool 2016 เรต R
        hero(g, 300, GROUND, 0.82, "point", 0.3)
        rated_r(g, 760, 820, 1.3 * ap(t, L[2] + 0.4), 6 * math.sin(t * 2))
        g.label("Deadpool (2016)", CX, 380, 100, color=DP_RED, sc=ap(t, L[2]), rot=-3)
        return
    if t < L[4] - 0.2:   # ใส่จิตวิญญาณ ความบ้าบิ่น อารมณ์ขัน
        hero(g, CX + 100 * math.sin(t * 2), GROUND, 0.82, "fist" if int(t * 2) % 2 else "point",
             0.4 * math.sin(t * 2))
        for i, txt in enumerate(("จิตวิญญาณ", "บ้าบิ่น", "อารมณ์ขัน")):
            g.label(txt, 200 + i * 340, 1150 + 20 * math.sin(t * 3 + i), 52, color=(RED, NAVY, GOLDTXT)[i],
                    sc=ap(t, L[3] + 0.4 * i))
        g.label("ใส่ลงไปทุกฉาก!", CX, 380, 96, sc=ap(t, L[3]), rot=-3)
        return
    if t < L[6] - 0.2:   # รายได้ถล่มทลาย ปรากฏการณ์
        money_rain(g, t, 10)
        hero(g, CX, GROUND, 0.8, "wave", 0.0, "smile")
        if t < L[5] - 0.2:
            g.label("รายได้ถล่มทลายทั่วโลก!", CX, 380, 84, color=GREEN, sc=ap(t, L[4]), rot=-3)
        else:
            g.label("ปรากฏการณ์ครั้งใหญ่!", CX, 380, 90, color=GOLDTXT, sc=ap(t, L[5]), rot=-3)
        return
    if t < L[7] - 0.2:   # จากดาราขาลง
        flop_chart(g, 560, 1150, 400, 420, 1.0)
        ryan(g, 280, 0.8, "worry", "shrug", 0.3)
        g.label("จากดาราขาลง...", CX, 380, 96, color=GREY, sc=ap(t, L[6]), rot=-3)
        return
    g.sunburst(CX, 760, 260, 640, 20, t * 10, 10, (0.98, 0.85, 0.4, 0.6))   # ไอคอน + นักธุรกิจ
    star_walk(g, 820, 1100, 0.8 * ap(t, L[7] + 0.4), "RYAN REYNOLDS")
    ryan(g, 330, 0.85, "smug", "cross", 0.3)
    g.label("ไอคอนระดับโลก + นักธุรกิจ", CX, 380, 72, color=GOLDTXT, sc=ap(t, L[7]), rot=-3)


# ------------------------------------------------------------------ 5. lesson
def s_lesson(g, t, L, d):
    g.ground(GROUND, WHITE)
    g.label("บทเรียน", CX, 340, 100, sc=ap(t, 0.2), rot=-3)
    if t < L[2] - 0.2:
        flop_chart(g, 160, 1150, 760, 520, 1.0)
        if t > L[1] - 0.2:
            g.label("ล้มเหลวนับครั้งไม่ถ้วน", CX, 490, 64, color=RED, sc=ap(t, L[1]))
        return
    ryan(g, CX, 0.72, "smile" if t < L[3] else "smug", "fist" if t < L[3] else "cross", 0.0, talk=t > L[3])
    if t < L[3] - 0.2:
        g.label("เชื่อมั่นในตัวเอง", CX, 490, 70, color=GREEN, sc=ap(t, L[2]))
    else:
        for i in range(4):
            u = (t * 0.6 + i / 4) % 1
            g.label("ฮ่า ๆ", 200 + i * 230, 900 - 200 * u, 48, color=GOLDTXT, a=1 - u)
        g.label("หัวเราะเยาะความผิดพลาด", CX, 490, 64, color=GOLDTXT, sc=ap(t, L[3]))


# ------------------------------------------------------------------ 6. outro
def s_outro(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[3] - 0.2:
        ryan(g, 280, 0.8, "smug", "point", 0.3)
        hero(g, 800, GROUND, 0.75, "shrug", -0.3)
        if t < L[1] - 0.2:
            g.label("ชอบบทไหนที่สุด?", CX, 380, 96, sc=ap(t, 0.2), rot=-3)
        elif t < L[2] - 0.2:
            g.label("เสน่ห์ความกวนใน Deadpool", CX, 380, 74, color=DP_RED, sc=ap(t, L[1]), rot=-3)
        else:
            g.label("?", 560, 700, 160, color=RED, sc=ap(t, L[2]))
            g.label("ใครเล่นแทนได้อีกไหม?", CX, 380, 84, color=GOLDTXT, sc=ap(t, L[2]), rot=-3)
        return
    with g.at(CX + 170, 640, ap(t, L[3])):   # ชวนคอมเมนต์
        g.bubble(0, 0, 460, 220, WHITE, tail=(-1, 1))
        for i in range(3):
            g.circle(-110 + i * 110, 0, 24 + 6 * math.sin(t * 6 - i), INK, 0)
    ryan(g, 250, 0.8, "smile", "wave", 0.3, talk=True)
    g.label("คอมเมนต์แลกเปลี่ยนกันได้เลย!", CX, 360, 70, color=RED, sc=ap(t, L[3]), rot=-3)


SCENES = {
    "hook": s_hook, "flops": s_flops, "dream": s_dream, "success": s_success, "lesson": s_lesson, "outro": s_outro,
}
NO_IRIS = set()
