"""ฉากตอน: Windows XP วางจำหน่าย (25 ต.ค. 2001) — ไม่ใช้โลโก้จริง"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from chars import (USERS, XP_BLUE, XP_GREEN, box, calendar_mourn, crt, hourglass, keyboard, note,  # noqa: E402
                   quake_lines, timeline_bar, tower, xp_box)
from gfx import GOLD, GOLD2, GREY, INK, NAVY, RED, W, WHITE, e_io, e_out, hexc, lerp, pop, seg  # noqa: E402
from people import person  # noqa: E402

CX = W / 2
GROUND = 1270
GOLDTXT = hexc("#b37a12")
PURPLE = hexc("#7a4a9a")

CAMERA = {"hook": "push_in", "launch": "pan_right", "before": "dutch", "luna": "push_in", "sticky": "pan_left",
          "lesson": "pull_out", "outro": "pan_right"}
TRANSITIONS = {"launch": "fade", "before": "whip", "luna": "iris", "sticky": "zoom", "lesson": "fade",
               "outro": "whip"}


def ap(t, a, dur=0.38):
    return pop(t, a - 0.2, dur)


def title(g, t, a, txt, col=INK, size=84, y=380):
    g.label(txt, CX, y, size, color=col, sc=ap(t, a), rot=-3)


def desk(g, y=GROUND - 330, x0=-300, x1=1400):
    g.rrect(x0, y, x1 - x0, 36, 8, hexc("#b88a52"), 6)


def notes(g, x, y, t, k=1.0, n=4):
    for i in range(n):
        u = (t * 0.6 + i / n) % 1
        note(g, x + 160 * math.sin(i * 2.1 + u * 2), y - 260 * u, 0.9 * k,
             (*[XP_BLUE, XP_GREEN, GOLD, RED][i % 4][:3], 1 - u), 15 * math.sin(t * 3 + i))


# ------------------------------------------------------------------ 1. hook
def s_hook(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:
        crt(g, CX, 860, 1.0, "off", t)
        g.label("วันนี้ในอดีต", CX, 380, 104, sc=lerp(2.0, 1, e_out(seg(t, 0.1, 0.4))) if t > 0.1 else 0, rot=-3)
        g.label("25 ตุลาคม 2001", CX, 520, 84, color=GOLDTXT, sc=pop(t, 0.6))
        return
    if t < L[3] - 0.2:   # เสียงเปิดเครื่อง + ทุ่งหญ้าฟ้าคราม
        crt(g, CX, 860, lerp(1.0, 1.25, e_io(seg(t, L[2], L[2] + 1.5))), "bliss", t)
        notes(g, CX, 600, t, ap(t, L[1]))
        if t < L[2] - 0.2:
            title(g, t, L[1], "เสียงเปิดเครื่องไม่กี่วินาที", XP_BLUE, 78)
        else:
            title(g, t, L[2], "ทุ่งหญ้าเขียว ใต้ฟ้าคราม", XP_GREEN, 80)
        return
    if t < L[4] - 0.2:   # ความทรงจำร่วมของคนทั้งโลก
        crt(g, CX, 640, 0.6, "bliss", t)
        for i in range(4):
            person(g, 160 + i * 250, GROUND, USERS[i], 0.5, mood="smile", pose="wave" if i % 2 else "down",
                   turn=0.2 - 0.15 * i, seed=10 + i)
        title(g, t, L[3], "ความทรงจำร่วมของคนทั้งโลก", INK, 76)
        return
    crt(g, CX, 840, 1.05, "desktop", t, win=ap(t, L[4] + 0.3))
    g.sparkle(CX + 300, 560, 40 * ap(t, L[4] + 0.5) + 1)
    title(g, t, L[4], "เปลี่ยนโลกคอมพิวเตอร์!", RED, 84)


# ------------------------------------------------------------------ 2. launch
def s_launch(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # 25 ต.ค. 2001 เปิดตัว Windows XP
        xp_box(g, CX, 840, 1.5 * ap(t, L[0]) + 0.01, 4 * math.sin(t * 2))
        if t < L[1] - 0.2:
            title(g, t, L[0], "25 ตุลาคม 2001", GOLDTXT, 92)
        else:
            for i in range(5):
                g.sparkle(CX + 300 * math.cos(i * 1.3 + t), 840 + 280 * math.sin(i * 1.3 + t), 30)
            title(g, t, L[1], "เปิดตัว \"Windows XP\"", XP_BLUE, 90)
        return
    if t < L[4] - 0.2:   # ตึงเครียดหลัง 9/11
        c = g.c
        c.rectangle(-500, 140, 2100, 1130)
        c.set_source_rgba(0.35, 0.37, 0.42, 0.25)
        c.fill()
        calendar_mourn(g, CX, 820, 1.3 * ap(t, L[2]) + 0.01)
        if t < L[3] - 0.2:
            title(g, t, L[2], "บรรยากาศตึงเครียดในสหรัฐฯ", INK, 78)
        else:
            g.label("เพียงเดือนเศษ", CX, 1150, 70, color=RED, sc=ap(t, L[3]))
            title(g, t, L[3], "หลังเหตุการณ์ 9/11", INK, 88)
        return
    crt(g, CX, 840, 1.0, "desktop", t, shake=1.0 if t > L[5] - 0.2 else 0.0)
    if t < L[5] - 0.2:
        title(g, t, L[4], "ระบบปฏิบัติการตัวใหม่...", XP_BLUE, 84)
    else:
        quake_lines(g, CX, 840, 380, t, ap(t, L[5]))
        title(g, t, L[5], "แรงสั่นสะเทือนครั้งใหญ่ที่สุด!", RED, 78)


# ------------------------------------------------------------------ 3. before
def s_before(g, t, L, d):
    g.ground(GROUND, WHITE)
    desk(g)
    tower(g, 980, GROUND - 330, 0.55)
    if t < L[2] - 0.2:   # ก่อนหน้านั้น ทนทุกข์กับความไม่เสถียร
        crt(g, 640, 700, 0.7, "bliss" if t < L[1] - 0.2 else "off", t)
        person(g, 230, GROUND, USERS[0], 0.72, mood="neutral" if t < L[1] - 0.2 else "worry", pose="down", turn=0.4,
               seed=1)
        if t < L[1] - 0.2:
            title(g, t, L[0], "ก่อนหน้านั้น...", INK, 92)
        else:
            g.sweat(330, 470, 1.6)
            title(g, t, L[1], "ทนทุกข์กับความไม่เสถียร", RED, 80)
        return
    if t < L[3] - 0.2:   # จอฟ้ามรณะ
        crt(g, 640, 700, 0.7, "bsod", t, shake=0.3)
        person(g, 230, GROUND, USERS[0], 0.72, mood="shock", pose="shrug", turn=0.4, seed=1)
        title(g, t, L[2], "\"จอฟ้ามรณะ\"", hexc("#0a24a8"), 96)
        return
    crt(g, 640, 700, 0.7, "desktop", t, win=1.0)   # ค้าง งานหาย
    hourglass(g, 700, 690, 1.0, t)
    person(g, 230, GROUND, USERS[0], 0.72, mood="angry", pose="fist", turn=0.4, seed=1)
    for i in range(3):
        u = (t * 0.5 + i / 3) % 1
        g.rrect(820 + 60 * i + 80 * u, 560 - 200 * u, 70, 90, 6, (1, 1, 1, 1 - u), 4, stroke=(0, 0, 0, 1 - u))
    title(g, t, L[3], "เครื่องค้าง งานหาย!", RED, 90)


# ------------------------------------------------------------------ 4. luna
def s_luna(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # ปฏิวัติ + เสถียรระดับองค์กร
        crt(g, CX, 800, 1.0, "desktop", t)
        if t < L[1] - 0.2:
            for i in range(6):
                a = i * math.pi / 3 + t
                g.sparkle(CX + 420 * math.cos(a), 800 + 340 * math.sin(a), 30)
            title(g, t, L[0], "ปฏิวัติใหม่หมดจด!", XP_GREEN, 92)
        else:
            with g.at(CX + 300, 560, ap(t, L[1]), 8):
                g.rrect(-200, -60, 400, 120, 30, WHITE, 7, stroke=NAVY)
                g.label("เสถียรระดับองค์กร", 0, 0, 48, color=NAVY)
            title(g, t, L[1], "ความเสถียรระดับองค์กร", NAVY, 80)
        return
    if t < L[5] - 0.2:   # Luna: ปุ่ม start + taskbar
        zoom = 1.0 if t < L[3] - 0.2 else lerp(1.0, 1.5, e_io(seg(t, L[3] - 0.2, L[3] + 0.8)))
        cx = CX + (0 if t < L[3] - 0.2 else lerp(0, 260, e_io(seg(t, L[3] - 0.2, L[3] + 0.8))))
        crt(g, cx, 800, zoom, "desktop", t, win=0.0 if t > L[3] - 0.2 else 1.0,
            start_glow=0.5 + 0.5 * math.sin(t * 6) if t > L[3] - 0.2 else 0.0)
        if t < L[3] - 0.2:
            title(g, t, L[2], "อินเทอร์เฟซ \"Luna\"", XP_BLUE, 90)
        elif t < L[4] - 0.2:
            title(g, t, L[3], "ปุ่ม Start สีเขียวสดใส", XP_GREEN, 84)
        else:
            title(g, t, L[4], "แถบ Taskbar สีน้ำเงิน", XP_BLUE, 84)
        return
    desk(g)   # เข้าถึงง่าย เป็นมิตรกับทุกคน
    crt(g, 620, 700, 0.6, "desktop", t)
    for i in range(3):
        person(g, 150 + i * 200 if i < 2 else 940, GROUND, USERS[[1, 2, 3][i]], 0.6, mood="smile",
               pose="wave" if i == 1 else "down", turn=0.3 - 0.3 * i, seed=20 + i)
    title(g, t, L[5], "เข้าถึงง่าย เป็นมิตรกับทุกคน", GOLDTXT, 76)


# ------------------------------------------------------------------ 5. sticky
def s_sticky(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # เหนียวแน่นที่สุด / สิบปี
        xp_box(g, 680, 880, 1.1, 6 * math.sin(t * 2))
        person(g, 300, GROUND, USERS[0], 0.75, mood="smile", pose="hold", turn=0.4, seed=1)
        if t < L[1] - 0.2:
            title(g, t, L[0], "เหนียวแน่นที่สุดในโลก!", XP_GREEN, 84)
        else:
            yr = int(lerp(2001, 2011, e_io(seg(t, L[1], L[2]))))
            g.label(str(yr), 680, 560, 90, color=GOLDTXT, sc=ap(t, L[1]))
            title(g, t, L[1], "ผ่านไปเป็นสิบปี", INK, 88)
        return
    if t < L[5] - 0.2:   # Vista / 7 vs กอด XP ไว้แน่น
        box(g, 760, 760, 0.8 * ap(t, L[2]) + 0.01, 8, "Vista")
        box(g, 900, 980, 0.7 * ap(t, L[2] + 0.4) + 0.01, -6, "7", hexc("#2b4f8a"), hexc("#7ac0f0"))
        xp_box(g, 360, 880, 0.9, -4 + 3 * math.sin(t * 3))
        if t > L[3] - 0.2:
            for i in range(3):
                g.circle(360 + 200 * math.cos(t + i * 2.1), 880 + 230 * math.sin(t + i * 2.1), 20,
                         (0.85, 0.25, 0.35, 0.9), 0)
        if t < L[3] - 0.2:
            title(g, t, L[2], "เวอร์ชันใหม่ Vista · Windows 7", INK, 74)
        elif t < L[4] - 0.2:
            title(g, t, L[3], "ผู้ใช้นับร้อยล้านยังกอด XP ไว้แน่น", XP_BLUE, 70)
        else:
            with g.at(760, 600, ap(t, L[4]), -10):
                g.rrect(-200, -60, 400, 120, 20, WHITE, 8, stroke=RED)
                g.label("ไม่เปลี่ยน!", 0, 0, 66, color=RED)
            title(g, t, L[4], "ไม่ยอมเปลี่ยนไปไหน", RED, 84)
        return
    k = e_io(seg(t, L[5], L[6] + 1.2))   # ขยายเวลาสนับสนุน 12+ ปี
    timeline_bar(g, 140, 940, 900, k, t)
    g.label("XP", lerp(140, 940, k), 820, 60, color=XP_GREEN)
    if t < L[6] - 0.2:
        title(g, t, L[5], "ต้องยอมขยายเวลาสนับสนุน", NAVY, 80)
    else:
        g.label("12+ ปี!", CX, 650, 130, color=RED, sc=ap(t, L[6]), rot=-4)
        title(g, t, L[6], "ยาวนานกว่า 12 ปีเต็ม!", RED, 84)


# ------------------------------------------------------------------ 6. lesson
def s_lesson(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:
        crt(g, CX, 820, 0.95, "bliss", t)
        if t < L[1] - 0.2:
            title(g, t, L[0], "เรื่องราวของ XP พิสูจน์ว่า", INK, 80)
        else:
            for i in range(4):
                u = (t * 0.5 + i / 4) % 1
                g.star(CX - 300 + i * 200, 560 - 120 * u, 26, (*GOLD2[:3], 1 - u), 4)
            title(g, t, L[1], "ครองใจผู้คนได้ยาวนานที่สุด", GOLDTXT, 78)
        return
    if t < L[3] - 0.2:   # ไม่ต้องล้ำยุคจนซับซ้อน
        c = g.c
        with g.at(CX, 820, ap(t, L[2]), 6 * math.sin(t * 3)):
            for i in range(8):
                a = i * math.pi / 4 + t
                g.circle(180 * math.cos(a), 180 * math.sin(a), 40, [XP_BLUE, RED, GOLD, XP_GREEN][i % 4], 5)
                g.line([(0, 0), (180 * math.cos(a), 180 * math.sin(a))], 5, INK, amp=0)
            g.circle(0, 0, 70, GREY, 6)
        g.line([(CX - 260, 560), (CX - 260 + 520 * ap(t, L[2] + 0.3), 560 + 520 * ap(t, L[2] + 0.3))], 16, RED, amp=0)
        title(g, t, L[2], "ไม่ต้องล้ำยุคจนซับซ้อน", RED, 82)
        return
    for i, (txt, col) in enumerate((("เสถียร", XP_BLUE), ("ใช้งานง่าย", XP_GREEN), ("ตอบโจทย์ชีวิตจริง", GOLDTXT))):
        k = ap(t, L[3] - 0.15 + 0.3 * i, 0.3) if i < 2 else ap(t, L[4])
        if k < 0.02:
            continue
        with g.at(CX, 620 + i * 220, k, -3 + 3 * i):
            g.rrect(-320, -80, 640, 160, 40, WHITE, 8, stroke=col)
            g.label(txt, 0, 0, 70, color=col)
    title(g, t, L[3], "สิ่งที่ครองใจผู้คนจริง ๆ", INK, 80)


# ------------------------------------------------------------------ 7. outro
def s_outro(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # ทันใช้ XP ไหม / คิดถึงเสียงเปิดเครื่อง
        crt(g, 680, 760, 0.7, "bliss", t)
        person(g, 220, GROUND, USERS[0], 0.75, mood="smile", pose="wave", turn=0.4, seed=1, talk=True)
        if t < L[1] - 0.2:
            title(g, t, L[0], "ทันใช้ Windows XP กันไหม?", XP_BLUE, 80)
        else:
            notes(g, 680, 560, t, 1.0)
            title(g, t, L[1], "คิดถึงเสียงเปิดเครื่อง", XP_GREEN, 84)
        return
    if t < L[3] - 0.2:   # พินบอล
        desk(g)
        crt(g, 620, 700, 0.75, "pinball", t)
        keyboard(g, 620, GROUND - 360, 0.7, t, 1.0)
        person(g, 160, GROUND, USERS[2], 0.75, mood="smile", pose="hold", turn=0.5, seed=3)
        title(g, t, L[2], "เกมพินบอลในตำนาน!", PURPLE, 84)
        return
    with g.at(CX + 170, 640, ap(t, L[3])):   # ชวนคอมเมนต์
        g.bubble(0, 0, 460, 220, WHITE, tail=(-1, 1))
        for i in range(3):
            g.circle(-110 + i * 110, 0, 24 + 6 * math.sin(t * 6 - i), INK, 0)
    person(g, 250, GROUND, USERS[1], 0.75, mood="smile", pose="wave", turn=0.3, seed=70, talk=True)
    title(g, t, L[3], "คอมเมนต์รำลึกความหลังกันได้เลย!", RED, 62)


SCENES = {
    "hook": s_hook, "launch": s_launch, "before": s_before, "luna": s_luna, "sticky": s_sticky,
    "lesson": s_lesson, "outro": s_outro,
}
NO_IRIS = set()
