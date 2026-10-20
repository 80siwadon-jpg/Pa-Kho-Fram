"""ฉากตอน: เบนจามิน โอ. เดวิส ซีเนียร์ นายพลผิวดำคนแรก (25 ต.ค. 1940)"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from chars import (DAVIS, DAVIS_COL, DAVIS_YOUNG, FDR, OFFICERS_W, OLIVE, SOLDIERS_B, SON, barrier,  # noqa: E402
                   broom, calendar_years, ladder, order_paper, plane, shoulder, sign_board, star)
from gfx import GOLD, GOLD2, GREY, INK, NAVY, RED, W, WHITE, e_io, e_out, hexc, lerp, pop, seg  # noqa: E402
from people import person  # noqa: E402

CX = W / 2
GROUND = 1270
GOLDTXT = hexc("#b37a12")
GREEN = hexc("#3c8d4f")
DARK = hexc("#4a3a3a")

CAMERA = {"hook": "push_in", "promo": "pan_right", "era": "dutch", "climb": "tilt_up", "legacy": "pull_out",
          "lesson": "push_in", "outro": "pan_left"}
TRANSITIONS = {"promo": "fade", "era": "whip", "climb": "zoom", "legacy": "iris", "lesson": "fade", "outro": "whip"}


def ap(t, a, dur=0.38):
    return pop(t, a - 0.2, dur)


def title(g, t, a, txt, col=INK, size=84, y=380):
    g.label(txt, CX, y, size, color=col, sc=ap(t, a), rot=-3)


def flag_us(g, x, y, w, t):
    g.line([(x, y), (x, y + 640)], 8, hexc("#8a8a8a"), amp=0)
    g.flag(x, y, w, w * 0.6, "us", t)


# ------------------------------------------------------------------ 1. hook
def s_hook(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:
        shoulder(g, CX, 860, 1.2, 1, pop(t, 0.6), t)
        g.label("วันนี้ในอดีต", CX, 380, 104, sc=lerp(2.0, 1, e_out(seg(t, 0.1, 0.4))) if t > 0.1 else 0, rot=-3)
        g.label("25 ตุลาคม 1940", CX, 520, 84, color=GOLDTXT, sc=pop(t, 0.6))
        return
    if t < L[2] - 0.2:   # พลทหารตัวเล็ก ๆ ถูกกดทับ
        person(g, 320, GROUND, DAVIS_YOUNG, 0.75, mood="firm", pose="salute", turn=0.3, seed=1)
        sign_board(g, 800, GROUND, 1.0, 4 * math.sin(t * 2))
        title(g, t, L[1], "พลทหารที่ถูกเหยียดสีผิว", DARK, 84)
        return
    if t < L[3] - 0.2:   # ก้าวข้ามกำแพง
        u = e_io(seg(t, L[2], L[3] - 0.3))
        g.rrect(560, 900, 120, GROUND - 900, 6, hexc("#9a948a"), 7)
        for r in range(4):
            g.line([(560, 900 + r * 92), (680, 900 + r * 92)], 4, INK, amp=0)
        person(g, lerp(330, 860, u), GROUND - 300 * math.sin(math.pi * u), DAVIS_COL, 0.65, mood="firm",
               pose="fist", turn=0.5, seed=2)
        title(g, t, L[2], "ก้าวข้ามกำแพงความอยุติธรรม", NAVY, 78)
        return
    person(g, 300, GROUND, DAVIS, 0.85, mood="smile", pose="salute", turn=0.3, seed=3)   # นายพลผิวดำคนแรก
    star(g, 760, 760, 150, ap(t, L[3]))
    title(g, t, L[3], "\"นายพลผิวดำคนแรก\"!", GOLDTXT, 92)


# ------------------------------------------------------------------ 2. promo
def s_promo(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:
        g.calendar(CX, 820, 1.1 * pop(t, 0.2), "25", "ศุกร์", "ต.ค. 1940")
        title(g, t, L[0], "25 ตุลาคม 1940", GOLDTXT, 92)
        return
    if t < L[2] - 0.2:   # โรสเวลต์ลงนาม
        flag_us(g, 820, 520, 220, t)
        person(g, 330, GROUND, FDR, 0.85, mood="smile", pose="sign", turn=0.4, seed=4)
        order_paper(g, 640, 1000, 0.7, -6, e_io(seg(t, L[1] + 0.6, L[2] - 0.4)))
        g.name_tag(t, L[1] + 0.1, 330, 1150, "แฟรงกลิน ดี. โรสเวลต์", "ประธานาธิบดีสหรัฐฯ")
        title(g, t, L[1], "โรสเวลต์ลงนามครั้งประวัติศาสตร์", NAVY, 74)
        return
    if t < L[4] - 0.2:   # พันเอกเดวิส -> นายพลจัตวา
        person(g, 300, GROUND, DAVIS_COL if t < L[3] - 0.2 else DAVIS, 0.85, mood="firm" if t < L[3] - 0.2
               else "smile", pose="salute" if t > L[3] - 0.2 else "down", turn=0.3, seed=3)
        g.name_tag(t, L[2] + 0.1, 300, 1150, "เบนจามิน โอ. เดวิส ซีเนียร์", "นายทหารกองทัพบกสหรัฐฯ")
        if t < L[3] - 0.2:
            order_paper(g, 760, 800, 0.9 * ap(t, L[2]) + 0.01, 6, 1.0)
            title(g, t, L[2], "พันเอกเบนจามิน โอ. เดวิส ซีเนียร์", INK, 70)
        else:
            shoulder(g, 760, 820, 0.75, 1, ap(t, L[3] + 0.3), t)
            title(g, t, L[3], "ขึ้นเป็น \"นายพลจัตวา\"!", GOLDTXT, 88)
        return
    sign_board(g, 300, GROUND, 1.0, -4 + 4 * math.sin(t * 2.3))   # ยุคเหยียดสีผิวถูกกฎหมาย
    sign_board(g, 780, GROUND, 0.85, 5 + 4 * math.sin(t * 2 + 1), "COLORED", hexc("#4a4a52"))
    g.line([(CX, 520), (CX, GROUND)], 10, RED, amp=0)
    title(g, t, L[4], "ยุคที่การเหยียดสีผิวยังถูกกฎหมาย!", RED, 72)


# ------------------------------------------------------------------ 3. era
def s_era(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # แบ่งแยกสีผิว / มองว่าไร้ความสามารถ
        for i in range(2):
            person(g, 160 + i * 190, GROUND, OFFICERS_W[i], 0.62, mood="smug", pose="cross" if i else "point",
                   turn=0.4, seed=10 + i)
        for i in range(2):
            person(g, 740 + i * 190, GROUND, SOLDIERS_B[i], 0.62, mood="sad" if t > L[1] - 0.2 else "firm",
                   pose="down", turn=-0.3, seed=20 + i)
        barrier(g, 520, 600, GROUND, t, 1.0)
        if t < L[1] - 0.2:
            title(g, t, L[0], "กองทัพแบ่งแยกสีผิว", RED, 88)
        else:
            with g.at(220, 560, ap(t, L[1]), -6):
                g.bubble(0, 0, 300, 120, WHITE, tail=(1, 1))
                g.label("ไร้ความสามารถ!", 0, 0, 44, color=RED)
            title(g, t, L[1], "ถูกมองว่าไร้ความสามารถ", DARK, 84)
        return
    person(g, 320, GROUND, SOLDIERS_B[0], 0.8, mood="sad", pose="hold", turn=0.4, seed=20)
    if t < L[3] - 0.2:   # งานชั้นล่าง
        broom(g, 520, GROUND, 1.1, 10 + 8 * math.sin(t * 4))
        for i in range(3):
            u = (t * 0.8 + i / 3) % 1
            g.circle(600 + 160 * u, GROUND - 30 - 60 * u, 20 + 20 * u, (0.7, 0.65, 0.55, 0.6 * (1 - u)), 0)
        title(g, t, L[2], "ทำได้แค่งานชั้นล่าง", DARK, 88)
    else:   # แทบไม่มีโอกาสเลื่อนขั้น
        ladder(g, 760, GROUND, 900, 1.0, 1.0)
        g.sweat(390, 470 + 10 * math.sin(t * 5), 1.4)
        g.rrect(640, 520, 240, 30, 6, RED, 5)
        g.label("ห้ามขึ้น!", 760, 470, 60, color=RED, sc=ap(t, L[3]))
        title(g, t, L[3], "แทบไม่มีโอกาสเลื่อนขั้น", RED, 84, y=330)


# ------------------------------------------------------------------ 4. climb
def s_climb(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # พลทหารธรรมดา ไม่ยอมจำนน
        person(g, 330, GROUND, DAVIS_YOUNG, 0.85, mood="firm", pose="salute" if t < L[1] - 0.2 else "fist",
               turn=0.3, seed=1)
        with g.at(0, 20 * math.sin(t * 2), 1, 3 * math.sin(t * 1.6)):
            calendar_years(g, 790, 760, 1899, 1899, 0)
        if t < L[1] - 0.2:
            title(g, t, L[0], "เริ่มจาก \"พลทหารธรรมดา ๆ\"", NAVY, 80)
        else:
            title(g, t, L[1], "ไม่ยอมจำนนต่อโชคชะตา!", RED, 84)
        return
    if t < L[4] - 0.2:   # กลืนความอยุติธรรม / ระเบียบวินัย
        person(g, CX, GROUND, DAVIS_YOUNG, 0.85, mood="firm", pose="salute" if t > L[3] - 0.2 else "down",
               turn=0, seed=1)
        if t < L[3] - 0.2:
            for i, x in enumerate((180, 900)):
                with g.at(x, 600 + 40 * i, ap(t, L[2] + 0.3 * i), -6 + 12 * i):
                    g.bubble(0, 0, 260, 110, WHITE, tail=(1 - 2 * i, 1))
                    g.label(["ดูถูก!", "ไม่มีทาง!"][i], 0, 0, 46, color=RED)
            title(g, t, L[2], "กลืนความอยุติธรรมลงคอ", DARK, 84)
        else:
            title(g, t, L[3], "ยึดมั่นในระเบียบวินัย", NAVY, 86)
        return
    u = e_io(seg(t, L[4] - 0.2, L[5] + 3.0))   # ไต่บันได 40+ ปี
    ladder(g, 700, GROUND, 760, 1.0, 1.0)
    y = lerp(GROUND, GROUND - 300, u)
    person(g, 700, y, DAVIS_COL if u > 0.5 else DAVIS_YOUNG, 0.5, mood="firm", pose="fist", turn=0, seed=2)
    calendar_years(g, 260, 760, 1899, 1940, u)
    if t < L[5] - 0.2:
        title(g, t, L[4], "พิสูจน์ตัวเองซ้ำแล้วซ้ำเล่า", NAVY, 80)
    else:
        title(g, t, L[5], "ไต่เต้ายาวนานกว่า 40 ปี!", GOLDTXT, 84)


# ------------------------------------------------------------------ 5. legacy
def s_legacy(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[3] - 0.2:   # ดาวบนบ่า ทลายกำแพง
        if t < L[2] - 0.2:
            shoulder(g, CX, 860, 1.2, 1, 1.0, t)
            for i in range(5):
                g.sparkle(CX + 340 * math.cos(i * 1.26 + t), 860 + 260 * math.sin(i * 1.26 + t), 30)
            title(g, t, L[0] if t < L[1] - 0.2 else L[1], "ดาวบนบ่าในวันนั้น" if t < L[1] - 0.2
                  else "สร้างประวัติศาสตร์หน้าใหม่", GOLDTXT, 86)
        else:
            k = e_out(seg(t, L[2], L[2] + 0.8))
            for r in range(5):
                for i in range(3):
                    x = 440 + i * 70 + (-1 if i < 1.5 else 1) * 300 * k * (1 if i > 0 else -1)
                    g.rrect(x, 600 + r * 120, 66, 110, 4, hexc("#9a948a"), 5)
            person(g, CX, GROUND, DAVIS, 0.7, mood="smile", pose="v", turn=0, seed=3)
            title(g, t, L[2], "ทลายกำแพงสีผิว!", RED, 92)
        return
    if t < L[5] - 0.2:   # แรงบันดาลใจให้ลูกชาย ฝูงบินทัสคีกี
        person(g, 240, GROUND, DAVIS, 0.75, mood="smile", pose="point", turn=0.4, seed=3)
        person(g, 520, GROUND, SON, 0.72, mood="smile", pose="salute", turn=0.3, seed=5)
        g.name_tag(t, L[3] + 0.1, 760, 1150, "เบนจามิน โอ. เดวิส จูเนียร์", "ลูกชาย · ผู้นำฝูงบินทัสคีกี")
        if t < L[4] - 0.2:
            title(g, t, L[3], "แรงบันดาลใจให้ลูกชาย", NAVY, 84)
        else:
            plane(g, lerp(-200, 1200, seg(t, L[4], L[5])), 500, 0.6, -6, t)
            title(g, t, L[4], "ผู้นำฝูงบินทัสคีกี!", RED, 88, y=330)
        return
    person(g, 300, GROUND, SON, 0.82, mood="smile", pose="salute", turn=0.3, seed=5)
    plane(g, 760, 640, 0.7, -8 + 4 * math.sin(t * 2), t)
    star(g, 760, 960, 90, ap(t, L[5]))
    title(g, t, L[5], "นายพลผิวดำคนแรกของกองทัพอากาศ", NAVY, 68)


# ------------------------------------------------------------------ 6. lesson
def s_lesson(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:
        person(g, 300, GROUND, DAVIS, 0.85, mood="smile", pose="salute", turn=0.3, seed=3)
        star(g, 760, 760, 120, 1.0)
        title(g, t, L[0], "เรื่องของเดวิส ซีเนียร์พิสูจน์ว่า", INK, 72)
        return
    if t < L[2] - 0.2:   # อยุติธรรมชะลอได้
        u = seg(t, L[1], L[2])
        g.rrect(600, 640, 60, GROUND - 640, 6, hexc("#9a948a"), 6)
        person(g, lerp(260, 470, e_out(u * 0.6)), GROUND, DAVIS_COL, 0.7, mood="firm", pose="fist", turn=0.5,
               seed=2)
        title(g, t, L[1], "ความอยุติธรรมอาจชะลอเราได้", DARK, 78)
        return
    u = e_io(seg(t, L[2], L[2] + 1.5))   # แต่หยุดไม่ได้
    for i in range(4):
        g.rrect(600 - 60 * i * u - 200 * u, 640 + 160 * i, 60, 150, 6, hexc("#9a948a"), 6)
    person(g, lerp(470, 860, u), GROUND, DAVIS, 0.7, mood="smile", pose="v", turn=0.4, seed=3)
    title(g, t, L[2], "แต่หยุดคนที่สู้ไม่ถอยไม่ได้!", RED, 80)


# ------------------------------------------------------------------ 7. outro
def s_outro(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[3] - 0.2:
        person(g, 260, GROUND, SOLDIERS_B[0], 0.8, mood="smile" if t < L[1] else "think", pose="wave" if t < L[1]
               else "think", turn=0.4, seed=20, talk=True)
        if t < L[1] - 0.2:
            with g.at(760, 640, ap(t, L[0])):
                g.bubble(0, 0, 360, 240, WHITE, tail=(-1, 1))
                g.label("?", 0, 0, 140, color=NAVY)
            title(g, t, L[0], "ทุกคนรู้สึกอย่างไร?", INK, 88)
        elif t < L[2] - 0.2:
            barrier(g, 560, 960, GROUND, t, 1.0)
            title(g, t, L[1], "เมื่อถูกตีกรอบจากสังคม...", DARK, 82)
        else:
            ladder(g, 760, GROUND, 900, 1.0, 1.0)
            star(g, 760, 330 + 380, 70, ap(t, L[2]))
            title(g, t, L[2], "อะไรช่วยให้เราก้าวข้าม?", NAVY, 84)
        return
    with g.at(CX + 170, 640, ap(t, L[3])):   # ชวนคอมเมนต์
        g.bubble(0, 0, 460, 220, WHITE, tail=(-1, 1))
        for i in range(3):
            g.circle(-110 + i * 110, 0, 24 + 6 * math.sin(t * 6 - i), INK, 0)
    person(g, 250, GROUND, DAVIS, 0.75, mood="smile", pose="wave", turn=0.3, seed=70, talk=True)
    title(g, t, L[3], "คอมเมนต์แลกเปลี่ยนกันได้เลย!", RED, 64)


SCENES = {
    "hook": s_hook, "promo": s_promo, "era": s_era, "climb": s_climb, "legacy": s_legacy, "lesson": s_lesson,
    "outro": s_outro,
}
NO_IRIS = set()
