"""ฉากตอน: 30 ต.ค. 1938 ละครวิทยุ The War of the Worlds ของออร์สัน เวลส์ — ดาวอังคารบุกโลก"""
import math
import os
import sys

import cairo

sys.path.insert(0, os.path.dirname(__file__))
from chars import (ANNOUNCER, ASTRONOMER, FAMILY, LISTENERS, MARS, WELLES, church, cylinder, deepfake,  # noqa: E402
                   film_reel, flash_bulletin, gas_cloud, globe, headline, house, martian, microphone, note,
                   planet, pumpkin, radio, rotary_phone, smartphone, smoke, traffic, tripod, wet_towel_face)
from gfx import GOLD, GOLD2, GREY, INK, NAVY, RED, W, WHITE, e_io, e_out, hexc, lerp, pop, seg  # noqa: E402
from people import person  # noqa: E402

CX = W / 2
GROUND = 1270
GOLDTXT = hexc("#b37a12")
NIGHTTXT = hexc("#f2c94c")
GREEN = hexc("#3c8d4f")
NIGHT = hexc("#1d2a44")
CBS = hexc("#2b4a7a")

CAMERA = {"hook": "push_in", "welles": "pan_right", "bulletin": "push_in", "attack": "dutch", "why": "pan_left",
          "panic": "pan_right", "morning": "push_in", "lesson": "pull_out", "outro": "pan_right"}
TRANSITIONS = {"welles": "zoom", "bulletin": "whip", "attack": "zoom", "why": "fade", "panic": "whip",
               "morning": "iris", "lesson": "fade", "outro": "whip"}


def ap(t, a, dur=0.38):
    return pop(t, a - 0.2, dur)


def title(g, t, a, txt, col=INK, size=84, y=380):
    g.label(txt, CX, y, size, color=col, sc=ap(t, a), rot=-3)


def night(g, k=1.0, glow=0.0):
    """ท้องฟ้ากลางคืน (แผงกรมท่าจางลงหาพื้น)"""
    c = g.c
    lg = cairo.LinearGradient(0, 160, 0, GROUND)
    a = 0.95 * k
    lg.add_color_stop_rgba(0, *NIGHT[:3], a)
    lg.add_color_stop_rgba(0.8, *NIGHT[:3], a * 0.75)
    lg.add_color_stop_rgba(1, *NIGHT[:3], a * 0.35)
    c.set_source(lg)
    c.rectangle(-600, 140, 2300, GROUND - 140)
    c.fill()
    for i in range(16):
        g.circle((i * 197) % 1100 - 10, 200 + (i * 83) % 500, 3 + (i % 3), (1, 1, 1, 0.6 * k), 0)
    if glow > 0:
        rg = cairo.RadialGradient(CX, GROUND, 50, CX, GROUND, 800)
        rg.add_color_stop_rgba(0, 1, 0.6, 0.3, 0.7 * glow)
        rg.add_color_stop_rgba(1, 1, 0.6, 0.3, 0)
        c.set_source(rg)
        c.rectangle(-600, 140, 2300, GROUND - 140)
        c.fill()


def chip(g, x, y, txt, col, k, rot=0.0, w=320):
    if k < 0.02:
        return
    with g.at(x, y, k, rot):
        g.rrect(-w / 2, -64, w, 128, 40, WHITE, 7, stroke=col)
        g.label(txt, 0, 0, 52, color=col)


def notes(g, x, y, t, k=1.0, n=4):
    for i in range(n):
        u = (t * 0.5 + i / n) % 1
        note(g, x - 150 + i * 100 + 30 * math.sin(t * 2 + i), y - 220 * u, 0.9 * k, (*INK[:3], (1 - u) * k),
             10 * math.sin(t * 3 + i))


def welles(g, x, sc=0.84, mood="smile", pose="down", turn=0.3, talk=False):
    person(g, x, GROUND, WELLES, sc, mood=mood, pose=pose, turn=turn, seed=3, talk=talk)


def listener_family(g, t, x0=170, mood="worry", pose="down"):
    for i, lk in enumerate(FAMILY[:3]):
        person(g, x0 + i * 230, GROUND, lk, 0.66, mood=mood, pose=pose, turn=0.3 - 0.2 * i, seed=20 + i)


# ------------------------------------------------------------------ 1. hook
def s_hook(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:   # วันนี้ในอดีต: วิทยุในบ้านยามค่ำ
        radio(g, CX, 1180, 1.25, t, 1.0, GOLD)
        notes(g, CX, 640, t)
        pumpkin(g, 830, 1200, 0.6, t)
        title(g, t, L[0] + 0.2, "วันนี้ในอดีต...", INK, 100)
        return
    if t < L[2] - 0.2:   # เพลงแทงโก้ถูกตัด
        cut = t > L[1] + 1.0
        radio(g, CX, 1180, 1.25, t, 1.0, RED if cut else GOLD)
        if not cut:
            notes(g, CX, 640, t)
            title(g, t, L[1], "เพลงแทงโก้...", GOLDTXT, 96)
        else:
            flash_bulletin(g, CX, 640, ap(t, L[1] + 1.0), -4 + 3 * math.sin(t * 9))
            title(g, t, L[1] + 1.0, "ตัดสัญญาณด่วน!", RED, 96)
        return
    if t < L[4] - 0.2:   # ผู้ประกาศเสียงสั่น: ดาวอังคารบุกโลก
        person(g, 300, GROUND, ANNOUNCER, 0.8, mood="worry", pose="down", turn=0.3, seed=5, talk=True)
        microphone(g, 520, 760, 0.9)
        if t > L[3] - 0.2:
            planet(g, 800, 700, 130 * ap(t, L[3]) + 1, MARS)
            martian(g, 800, 1050, 0.75 * ap(t, L[3] + 0.4) + 0.01, t)
            title(g, t, L[3], "\"ดาวอังคารบุกโลก!\"", RED, 96)
        else:
            for i in range(3):   # เสียงสั่น
                u = (t * 1.5 + i / 3) % 1
                g.arc(560, 680, 60 + 80 * u, -40, 40, 6, (*RED[:3], 1 - u))
            title(g, t, L[2], "ผู้ประกาศเสียงสั่นเครือ", INK, 86)
        return
    night(g, 0.9)   # ผู้คนแตกตื่นวิ่งหนี / คืนก่อนฮาโลวีน
    u = seg(t, L[4] - 0.2, L[5] + 2)
    for i, lk in enumerate(LISTENERS):
        x = 900 - ((t * 160 + i * 230) % 900)
        person(g, x, GROUND, lk, 0.62, mood="shock", pose="shrug" if i % 2 else "stop", turn=-0.6, seed=30 + i)
    if t > L[5] - 0.2:
        pumpkin(g, 820, 700, 0.9 * ap(t, L[5]) + 0.01, t)
        title(g, t, L[5], "คืนก่อนวันฮาโลวีน!", NIGHTTXT, 96)
    else:
        title(g, t, L[4], "ผู้คนแตกตื่นวิ่งหนี!", NIGHTTXT, 96)


# ------------------------------------------------------------------ 2. welles
def s_welles(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:   # คืน 30 ต.ค. 1938
        with g.at(CX, 860, ap(t, L[0]), -3 + 2 * math.sin(t)):
            g.rrect(-200, -190, 400, 380, 30, WHITE, 8)
            g.rrect(-200, -190, 400, 100, 30, hexc("#e8833a"), 8)
            g.text("ต.ค. 1938", 0, -140, 50, "kanit", WHITE)
            g.text("30", 0, 10, 150, "kanit", INK)
            g.text("อาทิตย์", 0, 130, 40, "kanitsb", GREY)
        pumpkin(g, 820, 1180, 0.6, t)
        title(g, t, L[0], "คืน 30 ตุลาคม 1938", INK, 92)
        return
    if t < L[2] - 0.2:   # สถานีวิทยุ CBS
        c = g.c
        with g.at(CX, GROUND):
            g.rrect(-260, -420, 520, 420, 10, hexc("#e8e0cc"), 7)
            for i in range(3):
                for j in range(3):
                    g.rrect(-200 + i * 150, -360 + j * 110, 90, 70, 6, hexc("#f2d68a"), 4)
            g.line([(0, -420), (0, -640)], 10, INK, amp=0)
            for k in range(3):
                g.line([(-50 + k * 15, -420 - k * 70), (50 - k * 15, -420 - k * 70)], 6, INK, amp=0)
        for i in range(3):
            u = (t * 1.2 + i / 3) % 1
            g.arc(CX, GROUND - 640, 40 + 160 * u, -150, -30, 7, (*CBS[:3], 1 - u))
        g.label("CBS", CX, 1150, 70, color=CBS, sc=ap(t, L[1] + 0.4))
        title(g, t, L[1], "สถานีวิทยุซีบีเอส สหรัฐฯ", CBS, 86)
        return
    if t < L[5] - 0.2:   # ออร์สัน เวลส์ วัย 23 + คณะเมอร์คิวรี
        welles(g, 300 if t > L[4] - 0.2 else CX - 120, 0.86, "smile", "point" if t > L[3] - 0.2 else "down", 0.3,
               talk=True)
        if t < L[4] - 0.2:
            microphone(g, CX + 150, 760, 0.95)
            g.label("23 ปี", 820, 640, 90, color=GOLDTXT, sc=ap(t, L[2] + 0.4), rot=6)
        g.name_tag(t, L[3] + 0.1, CX - 120 if t < L[4] - 0.2 else 300, 1070, "ออร์สัน เวลส์", "นักแสดง/ผู้กำกับ วัย 23",
                   side=1)
        if t > L[4] - 0.2:   # คณะละคร
            for i, lk in enumerate(LISTENERS[:2] + [ANNOUNCER]):
                person(g, 560 + i * 140, GROUND, lk, 0.55, mood="smile", pose="wave" if i == 1 else "down",
                       turn=-0.3, seed=40 + i)
            g.label("คณะละครเมอร์คิวรี", 700, 640, 64, color=INK, sc=ap(t, L[4] + 0.3))
            title(g, t, L[4], "MERCURY THEATRE", GOLDTXT, 80)
        else:
            title(g, t, L[2], "ชายหนุ่มผู้เปี่ยมพรสวรรค์", INK, 86)
        return
    if t < L[7] - 0.2:   # นิยาย The War of the Worlds ของ เอช. จี. เวลส์
        with g.at(330, 900, ap(t, L[5]), -6):
            g.rrect(-180, -250, 360, 500, 14, hexc("#7a2e2e"), 7)
            g.text("THE WAR", 0, -130, 48, "kanit", NIGHTTXT)
            g.text("OF THE", 0, -70, 38, "kanit", NIGHTTXT)
            g.text("WORLDS", 0, -10, 48, "kanit", NIGHTTXT)
            g.text("H.G. WELLS", 0, 170, 34, "kanitsb", WHITE)
            tripod(g, 0, 130, 0.12, t)
        if t > L[6] - 0.3:
            g.label("→", CX + 40, 900, 110, color=GREY, sc=ap(t, L[6] - 0.1))
            radio(g, 770, 1150, 0.8 * ap(t, L[6]) + 0.01, t, 1.0)
        if t > L[6] - 0.2:
            pumpkin(g, 870, 700, 0.5 * ap(t, L[6] + 0.4) + 0.01, t)
            title(g, t, L[6], "ดัดแปลงเป็นละครวิทยุ", INK, 86)
        else:
            title(g, t, L[5], "นิยายวิทยาศาสตร์ของ เอช. จี. เวลส์", INK, 74)
        return
    night(g, 0.85)   # เล่าสมจริงจนน่าขนลุก
    radio(g, CX, 1200, 1.1, t, 1.0, RED)
    for i in range(2):
        u = seg(t, L[8] + 0.2 * i, L[8] + 0.6 + 0.2 * i)
        if u > 0:
            with g.at(240 + i * 600, 760, u, 10 * math.sin(t * 6 + i)):
                g.label("!", 0, 0, 160, color=NIGHTTXT)
    if t > L[8] - 0.2:
        title(g, t, L[8], "สมจริงจนน่าขนลุก!", NIGHTTXT, 96)
    else:
        title(g, t, L[7], "คืนที่กลายเป็นประวัติศาสตร์", NIGHTTXT, 84)


# ------------------------------------------------------------------ 3. bulletin
def s_bulletin(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # ไม่เล่าแบบละคร เปิดด้วยเพลงเต้นรำ
        welles(g, 260, 0.82, "smile", "point" if t < L[1] - 0.2 else "down", 0.3, talk=True)
        radio(g, 700, 1180, 0.95, t, 1.0, GOLD)
        notes(g, 700, 640, t, ap(t, L[1]))
        if t > L[1] - 0.2:
            title(g, t, L[1], "เปิดด้วยเพลงเต้นรำธรรมดา ๆ", GOLDTXT, 80)
        else:
            chip(g, 700, 620, "ละครปกติ", GREY, ap(t, L[0] + 0.3), 4)
            g.line([(570, 620), (830, 620)], 12, RED, amp=0) if t > L[0] + 1.2 else None
            title(g, t, L[0], "ไม่เล่าแบบละครปกติ", INK, 86)
        return
    if t < L[3] - 0.2:   # ข่าวด่วนตัดเข้า เป็นระยะ
        radio(g, CX, 1180, 1.2, t, 1.0, RED)
        for i in range(3):
            k = ap(t, L[2] + 0.6 * i)
            flash_bulletin(g, 280 + i * 260, 560 + i * 90, 0.62 * k + 0.01, -8 + i * 8)
        title(g, t, L[2], "\"ข่าวด่วนตัดเข้าสู่รายการ\"", RED, 82)
        return
    if t < L[4] - 0.2:   # นักดาราศาสตร์: ระเบิดบนดาวอังคาร
        person(g, 260, GROUND, ASTRONOMER, 0.8, mood="worry", pose="point", turn=0.3, seed=7, talk=True)
        planet(g, 740, 740, 170, MARS)
        for i in range(3):
            k = ap(t, L[3] + 0.8 + 0.5 * i)
            g.star(700 + i * 50, 690 + (i % 2) * 70, 40 * k + 1, (1, 0.85, 0.4, 1), 4, pts=8, inner=0.45)
        title(g, t, L[3], "ระเบิดประหลาดบนดาวอังคาร", MARS, 84)
        return
    cylinder(g, 600, 1180, 1.0 * ap(t, L[4] + 0.3) + 0.01, t, 0.0)   # อุกกาบาตตกที่โกรเวอร์สมิลล์
    if t < L[4] + 0.4:
        u = seg(t, L[4] - 0.3, L[4] + 0.4)
        g.circle(lerp(1000, 650, u), lerp(400, 1100, u), 50, (1, 0.6, 0.2, 1), 5)
    with g.at(220, GROUND, ap(t, L[4] + 1.0)):
        g.line([(0, 0), (0, -260)], 10, WOODC, amp=0)
        g.rrect(-150, -330, 300, 110, 10, WHITE, 6)
        g.text("GROVER'S MILL", 0, -290, 32, "kanit", INK)
        g.text("NEW JERSEY", 0, -248, 28, "kanitsb", GREY)
    title(g, t, L[4], "อุกกาบาตตกที่โกรเวอร์สมิลล์!", RED, 80)


WOODC = hexc("#8a5a3a")


# ------------------------------------------------------------------ 4. attack
def s_attack(g, t, L, d):
    night(g, 0.85, 0.3 * seg(t, L[2] - 0.2, L[2] + 0.5))
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:   # รายงานภาคสนามสด
        cylinder(g, 680, 1200, 0.8, t, 0.3)
        person(g, 250, GROUND, ANNOUNCER, 0.76, mood="worry", pose="hold", turn=0.4, seed=5, talk=True)
        microphone(g, 380, 860, 0.6)
        with g.at(260, 560, ap(t, L[0] + 0.4)):
            g.rrect(-130, -50, 260, 100, 20, RED, 5)
            g.text("LIVE", 0, 0, 56, "kanit", WHITE)
        title(g, t, L[0], "รายงานภาคสนามสด (จำลอง)", NIGHTTXT, 80)
        return
    if t < L[2] - 0.2:   # โลหะเสียดสี: ฝาเปิด ยานโผล่
        cylinder(g, 600, 1200, 0.8, t, ap(t, L[1]))
        rise = e_out(seg(t, L[1], L[2]))
        tripod(g, 600, GROUND + 300 * (1 - rise), 0.7 * rise + 0.01, t)
        for i in range(4):
            g.label("แกร๊ก!", 220 + (i % 2) * 600, 700 + i * 90, 66, color=NIGHTTXT,
                    sc=0.5 + 0.5 * abs(math.sin(t * 5 + i)))
        title(g, t, L[1], "เสียงโลหะเสียดสี...", NIGHTTXT, 90)
        return
    if t < L[3] - 0.2:   # แสงความร้อน
        house(g, 260, GROUND, 0.7)
        k = e_io(seg(t, L[2], L[2] + 0.8))
        tripod(g, 700, GROUND, 0.75, t, k, (260, GROUND - 160))
        if k > 0.9:
            smoke(g, 260, GROUND - 200, 60, t, n=4)
        title(g, t, L[2], "แสงความร้อนแผดเผา!", NIGHTTXT, 92)
        return
    if t < L[4] - 0.2:   # ฝูงชนกรีดร้อง (วิ่งหนี ไม่มีคนเจ็บ)
        tripod(g, 820, GROUND, 0.6, t, 0, walk=1)
        for i, lk in enumerate(LISTENERS):
            x = 650 - ((t * 140 + i * 160) % 600)
            person(g, x, GROUND, lk, 0.58, mood="shock", pose="v" if i % 2 else "stop", turn=-0.6, seed=30 + i)
        title(g, t, L[3], "เสียงกรีดร้องของฝูงชน!", NIGHTTXT, 90)
        return
    tripod(g, 700, GROUND, 0.78, t, 0, walk=0.5)   # ปลาหมึกยักษ์ + แก๊สพิษ
    if t < L[5] - 0.2:
        martian(g, 330, 960, 1.3 * ap(t, L[4]) + 0.01, t)
        title(g, t, L[4], "สัตว์ประหลาดคล้ายปลาหมึกยักษ์", NIGHTTXT, 78)
        return
    gas_cloud(g, 360, 1150, 1.1, t, e_out(seg(t, L[5], L[5] + 1.5)))
    title(g, t, L[5], "ยานรบสามขา พ่นแก๊สพิษ!", NIGHTTXT, 88)


# ------------------------------------------------------------------ 5. why
def s_why(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:   # ประกาศเตือน 4 ครั้ง
        radio(g, 300, 1180, 0.85, t, 1.0, GREEN)
        for i in range(4):
            k = ap(t, L[0] + 0.5 + 0.45 * i)
            with g.at(650 + (i % 2) * 200, 640 + (i // 2) * 230, k):
                g.rrect(-90, -90, 180, 180, 30, WHITE, 7, stroke=GREEN)
                g.text(str(i + 1), 0, 0, 100, "kanit", GREEN)
        g.label("\"นี่เป็นแค่ละคร\"", 750, 1150, 60, color=GREEN, sc=ap(t, L[0] + 2.2))
        title(g, t, L[0], "เตือนว่าเป็นละครถึง 4 ครั้ง", GREEN, 84)
        return
    if t < L[3] - 0.2:   # หมุนคลื่นมาเจอกลางรายการ
        listener_family(g, t, 150, "worry" if t > L[2] - 0.2 else "neutral")
        with g.at(800, 860, 1.0):
            g.circle(0, 0, 130, hexc("#3a2a1e"), 7)
            with g.at(0, 0, 1, 40 * math.sin(t * 2)):
                g.line([(0, 0), (0, -110)], 14, GOLD2, amp=0)
            g.text("หมุน!", 0, 190, 50, "kanit", INK)
        if t > L[2] - 0.2:
            g.label("?", 380, 640, 160, color=RED, sc=ap(t, L[2]))
            title(g, t, L[2], "กลับไม่รู้เรื่อง!", RED, 96)
        else:
            title(g, t, L[1], "หมุนคลื่นมาเจอกลางรายการ", INK, 84)
        return
    if t < L[5] - 0.2:   # บรรยากาศสงครามในยุโรป
        globe(g, CX, 840, 260, t)
        with g.at(CX + 30, 700, 1):
            for i in range(5):
                smoke(g, -40 + i * 20, 0, 40, t, n=3, seed=i * 0.2)
        g.label("ยุโรป 1938", CX, 1200, 70, color=RED, sc=ap(t, L[3] + 0.5))
        if t > L[4] - 0.2:
            title(g, t, L[4], "หวาดผวาภัยสงครามในยุโรป", RED, 84)
        else:
            title(g, t, L[3], "บรรยากาศในยุคนั้น...", INK, 90)
        return
    listener_family(g, t, 150, "shock")   # เชื่อข่าวร้ายทันที
    radio(g, 830, 1180, 0.7, t, 1.0, RED)
    chip(g, CX, 650, "เชื่อทันที!", RED, ap(t, L[5] + 0.3), -4, 360)
    title(g, t, L[5], "พร้อมเชื่อข่าวร้ายทันที!", RED, 88)


# ------------------------------------------------------------------ 6. panic
def s_panic(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:   # โกลาหลทั่วประเทศ
        with g.at(CX, 860, ap(t, L[0])):
            g.blob(0, 0, 400, 250, hexc("#e8d6b0"), 7, seed=9)
            for i in range(9):
                a = i * 0.7 + t
                g.label("!", 260 * math.cos(a) * (0.4 + 0.6 * ((i * 37) % 10) / 10),
                        150 * math.sin(a * 1.3) * 0.8, 70, color=RED)
            g.text("U.S.A.", 0, 0, 80, "kanit", INK)
        title(g, t, L[0], "โกลาหลทั่วประเทศ!", RED, 96)
        return
    if t < L[3] - 0.2:   # สายด่วนล่ม / โทรร่ำลาญาติ
        for i in range(3):
            if i == 1 and t > L[2] - 0.2:
                continue
            rotary_phone(g, 210 + i * 310, 820 + 40 * (i % 2), 1.1, ring=1.0)
        if t > L[2] - 0.2:
            person(g, CX, GROUND, LISTENERS[1], 0.6, mood="sad", pose="phone", turn=0.2, seed=31)
            title(g, t, L[2], "โทรหาญาติเพื่อร่ำลา", INK, 90)
        else:
            for i, lab in enumerate(("ตำรวจ", "โรงพยาบาล", "สำนักข่าว")):
                g.label(lab, 210 + i * 310, 1000, 46, color=INK, sc=ap(t, L[1] + 0.3 * i))
            g.label("ระบบล่ม!", CX, 1180, 90, color=RED, sc=ap(t, L[1] + 1.4), rot=-4)
            title(g, t, L[1], "สายด่วนถูกโทรเข้าจนล่ม!", RED, 86)
        return
    if t < L[4] - 0.2:   # ผ้าเปียกคลุมหน้า
        wet_towel_face(g, CX, 860, 1.6, t)
        title(g, t, L[3], "ผ้าเปียกคลุมหน้ากันแก๊สพิษ", INK, 82)
        return
    if t < L[6] - 0.2:   # ขับรถหนี รถติด
        house(g, 160, 1050, 0.55)
        traffic(g, GROUND, t, 6, 0.85, seg(t, L[5] - 0.4, L[5] + 0.3))
        if t > L[5] - 0.2:
            title(g, t, L[5], "รถติดเป็นอัมพาต!", RED, 96)
        else:
            title(g, t, L[4], "ขนของขึ้นรถ ขับหนีออกนอกเมือง", INK, 80)
        return
    church(g, 700, GROUND, 0.75, t, 1.0)   # โบสถ์ / วันสิ้นโลก
    for i, lk in enumerate(LISTENERS[:2]):
        person(g, 220 + i * 170, GROUND, lk, 0.6, mood="shock" if t > L[7] - 0.2 else "sad", pose="sign", turn=0.5,
               seed=50 + i)
    if t > L[7] - 0.2:
        title(g, t, L[7], "คิดว่าวันสิ้นโลกมาถึงแล้ว!", RED, 86)
    else:
        title(g, t, L[6], "คุกเข่าสวดอ้อนวอนในโบสถ์", INK, 84)


# ------------------------------------------------------------------ 7. morning
def s_morning(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:   # หนังสือพิมพ์ประณาม
        headline(g, CX, 860, 0.95 * ap(t, L[0]) + 0.01, -4 + 2 * math.sin(t), "RADIO PANIC!",
                 "FAKE WAR SCARES NATION", "OCT. 31, 1938")
        title(g, t, L[0], "หนังสือพิมพ์ประณามดุเดือด", RED, 84)
        return
    if t < L[3] - 0.2:   # แถลงข่าวขอโทษ
        welles(g, 330, 0.86, "sad", "stop" if t > L[2] - 0.2 else "down", 0.3, talk=True)
        for i in range(3):
            microphone(g, 620 + i * 110, 820 + i * 20, 0.7)
        for i in range(3):   # แฟลชกล้อง
            if math.sin(t * 6 + i * 2) > 0.8:
                g.star(640 + i * 120, 600, 50, (1, 1, 0.85, 0.9), 0, pts=8, inner=0.35)
        if t > L[2] - 0.2:
            title(g, t, L[2], "\"ไม่ได้ตั้งใจหลอกใคร\"", INK, 90)
        else:
            title(g, t, L[1], "แถลงข่าวขอโทษ", INK, 96)
        return
    if t < L[4] - 0.2:   # คนดังชั่วข้ามคืน
        welles(g, CX, 0.86, "smile", "wave", 0.0)
        for i in range(8):
            a = i * 0.785 + t * 0.6
            g.star(CX + 340 * math.cos(a), 760 + 200 * math.sin(a), 30, GOLD2, 4)
        title(g, t, L[3], "คนดังระดับตำนานชั่วข้ามคืน!", GOLDTXT, 84)
        return
    welles(g, 280, 0.82, "smile", "point", 0.3)   # Citizen Kane
    film_reel(g, 720, 760, 150, t)
    if t > L[5] - 0.2:
        with g.at(720, 1080, ap(t, L[5]), -3):
            g.rrect(-220, -70, 440, 140, 16, INK, 6)
            g.text("CITIZEN KANE", 0, -14, 52, "kanit", NIGHTTXT)
            g.text("1941", 0, 38, 32, "kanitsb", WHITE)
        title(g, t, L[5], "Citizen Kane", INK, 96)
    else:
        title(g, t, L[4], "ใบเบิกทางสู่ผู้กำกับภาพยนตร์", INK, 82)


# ------------------------------------------------------------------ 8. lesson
def s_lesson(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:   # กรณีศึกษาสื่อสารมวลชน
        with g.at(CX, 880 + 12 * math.sin(t * 2), ap(t, L[0]), -3 + 3 * math.sin(t * 1.5)):
            g.rrect(-240, -170, 480, 340, 20, hexc("#e8d6a8"), 7)
            g.line([(0, -170), (0, 170)], 6, INK, amp=0)
            g.text("กรณีศึกษา", -120, -20, 44, "kanit", INK)
            g.text("1938", -120, 50, 40, "kanitsb", GREY)
            radio(g, 120, 90, 0.4, t, 1.0)
        title(g, t, L[0], "กรณีศึกษาคลาสสิกของสื่อ", INK, 86)
        return
    microphone(g, 300, 760, 1.1)   # พลังของสื่อ ชี้นำความกลัว
    if t > L[2] - 0.2:
        listener_family(g, t, 520, "shock")
        for i in range(3):
            u = (t * 1.2 + i / 3) % 1
            g.arc(300, 700, 100 + 300 * u, -40, 40, 8, (*RED[:3], 1 - u))
        if t > L[3] - 0.2:
            title(g, t, L[3], "ทรงพลังเพียงใด...", RED, 96)
        else:
            title(g, t, L[2], "ชี้นำความคิด ควบคุมความกลัว", RED, 84)
    else:
        chip(g, 700, 760, "เทคนิคการเล่าเรื่อง", GOLDTXT, ap(t, L[1] + 0.6), 4, 440)
        title(g, t, L[1], "พลังของสื่อ", GOLDTXT, 100)


# ------------------------------------------------------------------ 9. outro
def s_outro(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:
        radio(g, 300, 1180, 0.8, t, 1.0)
        martian(g, 760, 980, 0.9, t)
        g.label("?", 760, 640 + 15 * math.sin(t * 3), 200, color=RED, sc=ap(t, L[0] + 0.2))
        title(g, t, L[0] if t < L[1] - 0.2 else L[1], "รู้สึกอย่างไรกันบ้าง?", INK, 92)
        return
    if t < L[4] - 0.2:   # ยุคโซเชียล + Deepfake
        smartphone(g, 300, 880, 1.0, -6, "ด่วน!!", 1.0, t) if t < L[3] - 0.2 else None
        if t > L[3] - 0.2:
            deepfake(g, CX, 860, 1.0, t)
            title(g, t, L[3], "โซเชียล + Deepfake", RED, 90)
        else:
            for i in range(3):
                g.label("แชร์!", 700, 640 + i * 150, 60, color=RED, sc=ap(t, L[2] + 0.4 + 0.3 * i), rot=5)
            title(g, t, L[2], "ถ้าเกิดในยุคนี้...", INK, 92)
        return
    if t < L[6] - 0.2:   # มีสติ หรือ ตื่นตระหนกกว่าเดิม
        chip(g, 300, 760, "แยกแยะออก", GREEN, ap(t, L[4] + 0.3), -4, 340)
        g.label("หรือ", CX, 900, 70, color=GREY, sc=ap(t, L[5] - 0.1))
        chip(g, 780, 1040, "ตื่นตระหนกกว่า!", RED, ap(t, L[5]), 4, 380)
        smartphone(g, 780, 700, 0.6, 6, "!!!", 1.0, t)
        title(g, t, L[4], "มีสติ หรือ ตื่นตระหนก?", INK, 88)
        return
    with g.at(CX + 170, 640, ap(t, L[6])):   # ชวนคอมเมนต์
        g.bubble(0, 0, 460, 220, WHITE, tail=(-1, 1))
        for i in range(3):
            g.circle(-110 + i * 110, 0, 24 + 6 * math.sin(t * 6 - i), INK, 0)
    martian(g, 300, 900 + 15 * math.sin(t * 2), 0.9, t)
    title(g, t, L[6], "มาแลกเปลี่ยนกันในคอมเมนต์!", RED, 70)


SCENES = {
    "hook": s_hook, "welles": s_welles, "bulletin": s_bulletin, "attack": s_attack, "why": s_why,
    "panic": s_panic, "morning": s_morning, "lesson": s_lesson, "outro": s_outro,
}
NO_IRIS = set()
