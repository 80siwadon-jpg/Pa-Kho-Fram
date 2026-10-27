"""ฉากตอน: ข้อความแรกบน ARPANET "LO" (29 ต.ค. 1969)"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from chars import (DUVALL, KLINE, SRI_RED, UCLA_BLUE, USERS, bug, cal_map, desk_phone, globe, key_cap,  # noqa: E402
                   lo_sign, mainframe, smartphone, sparks, teletype, terminal, web, window_screen)
from gfx import GOLD, GOLD2, GREY, INK, NAVY, RED, W, WHITE, e_io, e_out, hexc, lerp, pop, seg  # noqa: E402
from people import person  # noqa: E402

CX = W / 2
GROUND = 1270
GOLDTXT = hexc("#b37a12")
GREEN = hexc("#2f8a4a")
TEAL = hexc("#2b6f8a")

CAMERA = {"hook": "push_in", "lab": "pan_right", "login": "push_in", "lo": "pull_out", "web": "pan_left",
          "lesson": "push_in", "outro": "pan_right"}
TRANSITIONS = {"lab": "zoom", "login": "whip", "lo": "iris", "web": "zoom", "lesson": "fade", "outro": "whip"}


def ap(t, a, dur=0.38):
    return pop(t, a - 0.2, dur)


def title(g, t, a, txt, col=INK, size=84, y=380):
    g.label(txt, CX, y, size, color=col, sc=ap(t, a), rot=-3)


def kline(g, x, sc=0.8, mood="smile", pose="down", turn=0.3, talk=False):
    person(g, x, GROUND, KLINE, sc, mood=mood, pose=pose, turn=turn, seed=3, talk=talk)


def split_call(g, t, txt_left, txt_right, k_left, k_right, letter=""):
    """จอแยกสองฝั่ง: UCLA (ซ้าย) — สายโทรศัพท์ — SRI (ขวา)"""
    g.line([(CX, 520), (CX, GROUND)], 4, GREY, amp=0)
    g.label("UCLA", 270, 520, 50, color=UCLA_BLUE)
    g.label("SRI", 810, 520, 50, color=SRI_RED)
    person(g, 230, GROUND, KLINE, 0.62, mood="smile", pose="phone", turn=0.3, seed=3, talk=k_left > 0.5)
    person(g, 850, GROUND, DUVALL, 0.62, mood="smile", pose="phone", turn=-0.3, seed=4, talk=k_right > 0.5)
    for sx, x in ((1, 360), (-1, 720)):
        pts = [(x, 640), (x + sx * 60, 700 + 20 * math.sin(t * 4)), (CX, 690)]
        g.line(pts, 4, INK, amp=0, smooth=True)
    if letter:
        for i, (x, k) in enumerate(((370, k_left), (710, k_right))):
            if k > 0.02:
                with g.at(x, 900, k):
                    g.rrect(-80, -80, 160, 160, 20, hexc("#0e1a10"), 6)
                    g.text(letter, 0, -4, 110, "kanit", (0.4, 1, 0.5, 1))
    if txt_left and k_left > 0.02:
        with g.at(330, 760, k_left):
            g.bubble(0, 0, 260, 110, WHITE, tail=(-1, 1))
            g.label(txt_left, 0, 0, 44, color=UCLA_BLUE)
    if txt_right and k_right > 0.02:
        with g.at(750, 760, k_right):
            g.bubble(0, 0, 260, 110, WHITE, tail=(1, 1))
            g.label(txt_right, 0, 0, 44, color=SRI_RED)


# ------------------------------------------------------------------ 1. hook
def s_hook(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # สองตัวอักษรจากระบบพัง
        crash = 1.0 if t > L[1] + 3.5 else 0.0
        terminal(g, CX, 880, 1.25, "LO" if t > L[1] + 1.2 else ("L" if t > L[1] + 0.4 else ""), t, crash)
        if crash:
            sparks(g, CX + 200, 700, t)
        title(g, t, L[1], "แค่ 2 ตัวอักษร จากระบบที่พัง!", RED, 82)
        return
    if t < L[3] - 0.2:   # คำแรกที่ให้กำเนิดอินเทอร์เน็ต
        lo_sign(g, CX, 860, 1.1 * ap(t, L[2]) + 0.01, t)
        title(g, t, L[2], "คำแรกของ \"โลกอินเทอร์เน็ต\"", GREEN, 86)
        return
    web(g, CX, 860, 260, t, e_io(seg(t, L[3] - 0.2, L[3] + 1.6)))   # เชื่อมมนุษยชาติ
    title(g, t, L[3], "เชื่อมมนุษยชาติไปตลอดกาล!", NAVY, 86)


# ------------------------------------------------------------------ 2. lab
def s_lab(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # คืน 29 ต.ค. 1969 / แล็บ UCLA
        if t < L[1] - 0.2:
            g.calendar(CX, 860, 1.25 * ap(t, L[0]) + 0.01, 29, "พุธ", "ต.ค. 1969")
            g.circle(820, 560, 50, hexc("#f6e7a8"), 5)
            g.circle(845, 545, 44, WHITE, 0)
            title(g, t, L[0], "คืนวันที่ 29 ตุลาคม 1969", NAVY, 86)
        else:
            mainframe(g, 640, GROUND, 0.9, t)
            g.label("UCLA", 640, 560, 80, color=UCLA_BLUE, sc=ap(t, L[1] + 0.3))
            title(g, t, L[1], "แล็บคอมพิวเตอร์ UCLA", UCLA_BLUE, 88)
        return
    if t < L[4] - 0.2:   # ชาร์ลี ไคลน์ + คอมพิวเตอร์เท่าตู้เสื้อผ้า
        mainframe(g, 700, GROUND, 0.9, t)
        kline(g, 260, 0.8, "smile", "wave" if t < L[3] - 0.2 else "point", 0.4)
        g.name_tag(t, L[2] + 0.1, 300, 1080, "ชาร์ลี ไคลน์", "นักศึกษา UCLA", side=1)
        if t < L[3] - 0.2:
            title(g, t, L[2], "นักศึกษา ชาร์ลี ไคลน์", INK, 88)
        else:
            title(g, t, L[3], "คอมพิวเตอร์ใหญ่เท่าตู้เสื้อผ้า!", INK, 82)
        return
    if t < L[6] - 0.2:   # เป้าหมาย: ส่งข้อความดิจิทัลไปอีกเครื่อง
        teletype(g, 280, GROUND - 60, 0.75, t)
        mainframe(g, 780, GROUND, 0.55, t)
        for i in range(4):
            u = (t * 0.7 + i / 4) % 1
            x = lerp(400, 680, u)
            g.text("01"[i % 2], x, 760 - 60 * math.sin(math.pi * u), 50, "kanit", (*GREEN[:3], 1 - abs(u - 0.5) * 1.6))
        if t < L[5] - 0.2:
            g.label("?", CX, 560, 120, color=GREY, sc=ap(t, L[4] + 0.3))
            title(g, t, L[4], "เป้าหมายที่ไม่มีใครจินตนาการออก", INK, 78)
        else:
            title(g, t, L[5], "ส่ง \"ข้อความดิจิทัล\" ข้ามเครื่อง", GREEN, 80)
        return
    k = e_io(seg(t, L[6] - 0.2, L[7] + 1.5))   # SRI ห่าง 500 กม. ผ่าน ARPANET
    cal_map(g, CX, 840, 0.85, k, t)
    if t < L[7] - 0.2:
        title(g, t, L[6], "สถาบันวิจัยสแตนฟอร์ด (SRI)", SRI_RED, 84)
    elif t < L[8] - 0.2:
        title(g, t, L[7], "ห่างออกไปกว่า 500 กิโลเมตร", INK, 84)
    else:
        title(g, t, L[8], "ผ่านเครือข่ายทดลอง ARPANET", NAVY, 82)


# ------------------------------------------------------------------ 3. login
def s_login(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # คุยโทรศัพท์ยืนยันแบบเรียลไทม์
        split_call(g, t, "", "", 0, 0)
        desk_phone(g, CX, GROUND - 40, 0.9, 1.0 if t < L[1] else 0.0)
        if t < L[1] - 0.2:
            title(g, t, L[0], "ยืนยันว่าส่งข้อมูลได้จริง", INK, 86)
        else:
            title(g, t, L[1], "คุยโทรศัพท์กันแบบเรียลไทม์", NAVY, 84)
        return
    if t < L[4] - 0.2:   # คำว่า LOGIN / พิมพ์ทีละตัว
        for i, ch in enumerate("LOGIN"):
            key_cap(g, 200 + i * 170, 880, 0.9 * ap(t, L[2] + 0.12 * i, 0.3) + 0.01, ch,
                    abs(math.sin(t * 3 + i)) if t > L[3] - 0.2 else 0.0)
        if t < L[3] - 0.2:
            title(g, t, L[2], "ตั้งใจพิมพ์คำว่า \"LOGIN\"", GREEN, 88)
        else:
            title(g, t, L[3], "กดแป้นพิมพ์ทีละตัวอักษร...", INK, 86)
        return
    if t < L[6] - 0.2:   # L
        k_r = ap(t, L[5])
        split_call(g, t, "กด L แล้ว!", "เห็น L แล้ว!", ap(t, L[4]), k_r if t > L[5] - 0.2 else 0, "L")
        title(g, t, L[4], "\"L\"", UCLA_BLUE, 120)
        return
    if t < L[8] - 0.2:   # O
        k_r = ap(t, L[7])
        split_call(g, t, "กด O แล้ว!", "เห็น O แล้ว!", ap(t, L[6]), k_r if t > L[7] - 0.2 else 0, "O")
        title(g, t, L[6], "\"O\"", UCLA_BLUE, 120)
        return
    if t < L[9] - 0.2:   # G...
        key_cap(g, CX, 880, 1.4, "G", abs(math.sin(t * 4)), hexc("#f2d68a"))
        title(g, t, L[8], "ตัวที่สาม \"G\"...", GOLDTXT, 100)
        return
    terminal(g, CX, 880, 1.2, "", t, 1.0)   # System Crash
    bug(g, 830, 640, 1.0, t)
    sparks(g, 300, 700, t)
    title(g, t, L[9], "ระบบล่ม! (System Crash)", RED, 92)


# ------------------------------------------------------------------ 4. lo
def s_lo(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # ข้อความแรก ไม่ใช่สุนทรพจน์
        terminal(g, CX, 880, 1.2, "LO", t, 0.0)
        if t > L[1] - 0.2:
            with g.at(800, 560, ap(t, L[1]), 8):
                g.rrect(-150, -100, 300, 200, 10, hexc("#f4eedf"), 6)
                g.text("สุนทรพจน์", 0, -40, 40, "kanit", GREY)
            k = seg(t, L[1] + 0.6, L[1] + 1.2)
            if k > 0:
                g.line([(650, 470), (650 + 300 * k, 470 + 180 * k)], 12, RED, amp=0)
            title(g, t, L[1], "ไม่ใช่สุนทรพจน์ที่ยิ่งใหญ่", INK, 86)
        else:
            title(g, t, L[0], "ข้อความแรกผ่านอินเทอร์เน็ต...", GREEN, 82)
        return
    if t < L[3] - 0.2:   # แค่ "LO"
        lo_sign(g, CX, 860, 1.3 * ap(t, L[2]) + 0.01, t)
        title(g, t, L[2], "แค่สองตัวอักษร \"LO\"!", GREEN, 92)
        return
    if t < L[4] - 0.2:   # อุบัติเหตุทางเทคนิค
        bug(g, CX, 900, 1.6, t)
        title(g, t, L[3], "ฟังดูเหมือนอุบัติเหตุทางเทคนิค", INK, 82)
        return
    lo_sign(g, CX, 920, 0.9, t, 1.0)   # Lo and behold!
    for i in range(5):
        g.sparkle(CX + 340 * math.cos(i * 1.25 + t), 920 + 220 * math.sin(i * 1.25 + t), 26)
    if t < L[5] - 0.2:
        g.label("\"Lo and behold!\"", CX, 600, 84, color=GOLDTXT, sc=ap(t, L[4] + 1.0), rot=-4)
        title(g, t, L[4], "คำพ้องกับ \"Lo and behold!\"", GOLDTXT, 82)
    else:
        title(g, t, L[5], "\"จงดูเถิด สิ่งมหัศจรรย์ปรากฏแล้ว!\"", GOLDTXT, 74)


# ------------------------------------------------------------------ 5. web
def s_web(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # ซ่อมเสร็จ ส่ง LOGIN สำเร็จ
        if t < L[1] - 0.2:
            terminal(g, CX, 880, 1.1, "", t, 0.0)
            for i in range(3):   # เฟืองซ่อมระบบหมุน
                with g.at(300 + i * 240, 600, 1, t * 90 * (1 if i % 2 else -1)):
                    g.star(0, 0, 50, GREY, 5, pts=8, inner=0.7)
                    g.circle(0, 0, 16, WHITE, 4)
            title(g, t, L[0], "ซ่อมระบบไม่กี่ชั่วโมงต่อมา...", INK, 84)
        else:
            terminal(g, CX, 880, 1.1, "LOGIN", t, 0.0)
            with g.at(800, 600, ap(t, L[1] + 0.6)):
                g.circle(0, 0, 90, WHITE, 8, stroke=GREEN)
                g.line([(-40, 0), (-10, 35), (50, -40)], 16, GREEN, amp=0)
            title(g, t, L[1], "ส่ง \"LOGIN\" สำเร็จ!", GREEN, 92)
        return
    if t < L[3] - 0.2:   # สองมหาวิทยาลัย
        cal_map(g, CX, 840, 0.8, 1.0, t)
        title(g, t, L[2], "การทดลองเล็ก ๆ ระหว่างสองสถาบัน", INK, 80)
        return
    if t < L[4] - 0.2:   # รากฐาน World Wide Web
        web(g, CX, 860, 280, t, e_io(seg(t, L[3] - 0.2, L[3] + 2.0)))
        g.label("WWW", CX, 1200, 80, color=NAVY, sc=ap(t, L[3] + 1.0))
        title(g, t, L[3], "รากฐานของโครงข่ายระดับโลก", NAVY, 82)
        return
    for i, lk in enumerate(USERS):   # สื่อสาร ทำธุรกิจ หลายพันล้านคน
        person(g, 220 + i * 320, GROUND, lk, 0.66, mood="smile", pose="phone" if i != 1 else "wave",
               turn=0.3 - 0.3 * i, seed=20 + i)
    globe(g, CX, 640, 110, t)
    for i in range(4):
        u = (t * 0.7 + i / 4) % 1
        g.circle(lerp(220, 860, u), 760 - 140 * math.sin(math.pi * u), 14, (*GOLD[:3], 1), 3)
    if t < L[5] - 0.2:
        title(g, t, L[4], "สื่อสาร ทำธุรกิจ", GREEN, 92)
    else:
        title(g, t, L[5], "เปลี่ยนชีวิตคนหลายพันล้าน", NAVY, 86)


# ------------------------------------------------------------------ 6. lesson
def s_lesson(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:
        kline(g, CX, 0.86, "smile", "down", 0.0)
        if t < L[1] - 0.2:
            title(g, t, L[0], "คืนนั้นพิสูจน์ให้เห็นว่า...", INK, 86)
        else:
            for i in range(5):
                g.sparkle(CX + 300 * math.cos(i * 1.25 + t), 820 + 260 * math.sin(i * 1.25 + t), 26)
            title(g, t, L[1], "ก้าวแรกของนวัตกรรมที่ยิ่งใหญ่", GOLDTXT, 84)
        return
    if t < L[3] - 0.2:   # ไม่สมบูรณ์แบบ
        terminal(g, CX, 880, 1.1, "LO", t, 0.0)
        g.label("ไม่สมบูรณ์แบบ", CX, 560, 66, color=RED, sc=ap(t, L[2] + 0.4), rot=-5)
        title(g, t, L[2], "ไม่ได้เริ่มอย่างสมบูรณ์แบบ", INK, 84)
        return
    key_cap(g, CX, 900, 1.8 * ap(t, L[3]) + 0.01, "GO", abs(math.sin(t * 3)), hexc("#9ad0a8"))   # กล้ากดปุ่มแรก
    g.label("ปุ่มแรก", CX, 1170, 66, color=GREEN, sc=ap(t, L[3] + 0.8))
    title(g, t, L[3], "ความกล้าที่จะกดปุ่มแรก!", GREEN, 88)


# ------------------------------------------------------------------ 7. outro
def s_outro(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:
        lo_sign(g, 760, 760, 0.65, t)
        person(g, 250, GROUND, USERS[0], 0.78, mood="smile", pose="think", turn=0.4, seed=30)
        title(g, t, L[0], "คิดเห็นอย่างไรกันบ้าง?", INK, 90)
        return
    if t < L[3] - 0.2:   # ถ้าไม่มีอินเทอร์เน็ต 24 ชม.
        smartphone(g, 300, 860 + 15 * math.sin(t * 2), 1.2, -6 + 4 * math.sin(t * 1.5), "ไม่มีสัญญาณ", 0.6, t)
        k = seg(t, L[1] + 0.6, L[1] + 1.2)
        if k > 0:
            g.line([(170, 640), (170 + 260 * k, 640 + 440 * k)], 16, RED, amp=0)
        if t > L[2] - 0.2:
            with g.at(770, 860, ap(t, L[2] + 0.2) * (1 + 0.05 * math.sin(t * 4)), 6 + 4 * math.sin(t * 2)):
                g.circle(0, 0, 150, WHITE, 8, stroke=RED)
                g.text("24", 0, -20, 110, "kanit", RED)
                g.text("ชั่วโมง", 0, 70, 40, "kanitsb", INK)
            title(g, t, L[2], "อยู่ได้เกิน 24 ชั่วโมงไหม?", RED, 86)
        else:
            title(g, t, L[1], "ถ้าโลกไม่มีอินเทอร์เน็ต...", INK, 88)
        return
    with g.at(CX + 170, 640, ap(t, L[3])):   # ชวนคอมเมนต์
        g.bubble(0, 0, 460, 220, WHITE, tail=(-1, 1))
        for i in range(3):
            g.circle(-110 + i * 110, 0, 24 + 6 * math.sin(t * 6 - i), INK, 0)
    person(g, 260, GROUND, USERS[1], 0.8, mood="smile", pose="wave", turn=0.3, seed=31, talk=True)
    title(g, t, L[3], "มาแลกเปลี่ยนกันในคอมเมนต์!", RED, 70)


SCENES = {
    "hook": s_hook, "lab": s_lab, "login": s_login, "lo": s_lo, "web": s_web, "lesson": s_lesson,
    "outro": s_outro,
}
NO_IRIS = set()
