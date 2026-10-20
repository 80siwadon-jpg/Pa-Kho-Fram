"""ฉากตอน: เซธ แมกฟาร์เลน (เกิด 26 ต.ค. 1973)"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from chars import (EXECS, FANS, FG_BLUE, FG_YEL, SETH, SETH_KID, chart, clapper, comic, dvd_stack, mic,  # noqa: E402
                   money, pencil, placard, stamp, teddy, tv, voice_card)
from gfx import GOLD, GOLD2, GREY, INK, NAVY, RED, W, WHITE, e_io, e_out, hexc, lerp, pop, seg  # noqa: E402
from people import person  # noqa: E402

CX = W / 2
GROUND = 1270
GOLDTXT = hexc("#b37a12")
GREEN = hexc("#3c8d4f")
DARK = hexc("#4a3a3a")
PURPLE = hexc("#7a4a9a")

CAMERA = {"hook": "push_in", "young": "pan_right", "cancel": "dutch", "revive": "push_in", "ted": "pan_left",
          "lesson": "pull_out", "outro": "pan_right"}
TRANSITIONS = {"young": "zoom", "cancel": "whip", "revive": "iris", "ted": "zoom", "lesson": "fade", "outro": "whip"}


def ap(t, a, dur=0.38):
    return pop(t, a - 0.2, dur)


def title(g, t, a, txt, col=INK, size=84, y=380):
    g.label(txt, CX, y, size, color=col, sc=ap(t, a), rot=-3)


def seth(g, x, sc=0.85, mood="smile", pose="down", turn=0.3, talk=False):
    person(g, x, GROUND, SETH, sc, mood=mood, pose=pose, turn=turn, seed=3, talk=talk)


# ------------------------------------------------------------------ 1. hook
def s_hook(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:   # พิธีกรเปิดคลิป
        seth(g, 300, 0.85, "smile", "point", 0.3, talk=True)
        with g.at(780, 820, pop(t, 0.3), 4 * math.sin(t * 2)):
            g.calendar(0, 0, 1.0, "26", "ศุกร์", "ต.ค. 1973")
        g.label("วันนี้ในอดีต", CX, 380, 104, sc=lerp(2.0, 1, e_out(seg(t, 0.1, 0.4))) if t > 0.1 else 0, rot=-3)
        return
    if t < L[2] - 0.2:   # การ์ตูนโดนแคนเซิล 2 ครั้ง
        tv(g, CX, 960, 1.15, t, "static" if t > L[1] + 1.2 else "title")
        stamp(g, CX, 640, "CANCELLED × 2", 0.95, -12, RED, ap(t, L[1] + 0.8))
        title(g, t, L[1], "การ์ตูนที่ถูกแคนเซิล 2 ครั้ง!", RED, 80, y=330)
        return
    if t < L[3] - 0.2:   # ฟื้นคืนชีพ อาณาจักรหมื่นล้าน
        tv(g, 330, 1000, 0.75, t, "title", 4 * math.sin(t * 3))
        money(g, 700, 1000, 0.9 * ap(t, L[2] + 0.4) + 0.01, t)
        for i in range(4):
            g.sparkle(330 + 260 * math.cos(i * 1.57 + t), 820 + 200 * math.sin(i * 1.57 + t), 30)
        title(g, t, L[2], "ฟื้นคืนชีพ สร้างอาณาจักรหมื่นล้าน!", GOLDTXT, 74)
        return
    seth(g, 300, 0.85, "smile", "down")   # เซธ แมกฟาร์เลน
    pencil(g, 860, 760, 0.8, 20 + 6 * math.sin(t * 3))
    g.name_tag(t, L[3] + 0.1, 640, 1150, "เซธ แมกฟาร์เลน", "ผู้สร้าง Family Guy และ Ted")
    title(g, t, L[3], "\"เซธ แมกฟาร์เลน\"", FG_BLUE, 96)


# ------------------------------------------------------------------ 2. young
def s_young(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # เกิด 1973 รักการวาด
        person(g, 300, GROUND, SETH_KID, 0.95, mood="smile", pose="sign" if t > L[2] - 1.6 else "wave", turn=0.3,
               seed=4)
        if t < L[1] - 0.2:
            g.calendar(760, 820, 1.0 * ap(t, L[0]) + 0.01, "26", "ศุกร์", "ต.ค. 1973")
            title(g, t, L[0], "26 ตุลาคม 1973", GOLDTXT, 92)
        else:
            pencil(g, 720, 840, 1.1 * ap(t, L[1]) + 0.01, 20 + 8 * math.sin(t * 3))
            title(g, t, L[1], "เด็กชายเซธ แมกฟาร์เลน", FG_BLUE, 84)
        return
    if t < L[3] - 0.2:   # รักการ์ตูน
        person(g, 260, GROUND, SETH_KID, 0.95, mood="smile", pose="sign", turn=0.4, seed=4)
        for i in range(3):
            g.label(["ปัง!", "ฮ่า ๆ", "ว้าว"][i], 620 + i * 140, 640 + 60 * math.sin(t * 2 + i), 60,
                    color=[RED, FG_BLUE, GREEN][i], sc=ap(t, L[2] + 0.2 * i), rot=-8 + 8 * i)
        title(g, t, L[2], "หลงรักการ์ตูนตั้งแต่จำความได้", PURPLE, 76)
        return
    if t < L[5] - 0.2:   # 9 ขวบ ขายการ์ตูนช่อง
        person(g, 230, GROUND, SETH_KID, 0.9, mood="smile", pose="hold", turn=0.4, seed=4)
        comic(g, 700, 820, 0.9 * ap(t, L[3] + 0.3) + 0.01, 4 * math.sin(t * 2))
        if t < L[4] - 0.2:
            g.label("9 ขวบ", 700, 1080, 90, color=RED, sc=ap(t, L[3]))
            title(g, t, L[3], "อายุเพียง 9 ขวบ", RED, 92)
        else:
            title(g, t, L[4], "ขายการ์ตูนให้หนังสือพิมพ์!", GOLDTXT, 80)
        return
    seth(g, 280, 0.85, "smile", "point" if t > L[6] - 0.2 else "down", 0.3, talk=t > L[6] - 0.2)   # เสนอไอเดียให้ Fox
    if t < L[6] - 0.2:
        title(g, t, L[5], "เส้นทางสู่ฮอลลีวูด", NAVY, 90)
        g.label("HOLLYWOOD", 720, 700, 80, color=GOLDTXT, sc=ap(t, L[5] + 0.3), rot=-4)
    elif t < L[7] - 0.2:
        person(g, 860, GROUND, EXECS[0], 0.75, mood="neutral", pose="cross", turn=-0.4, seed=10)
        with g.at(860, 470, ap(t, L[6] + 0.3), -4):
            g.rrect(-110, -50, 220, 100, 20, WHITE, 6, stroke=FG_BLUE)
            g.label("FOX", 0, 0, 56, color=FG_BLUE)
        title(g, t, L[6], "เสนอไอเดียการ์ตูนสุดเพี้ยน", PURPLE, 80, y=330)
    else:
        tv(g, 760, 960, 0.85 * ap(t, L[7]) + 0.01, t, "title", 4 * math.sin(t * 3))
        title(g, t, L[7], "Family Guy!", FG_BLUE, 110)


# ------------------------------------------------------------------ 3. cancel
def s_cancel(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[3] - 0.2:   # มุกตลกร้าย จิกกัด
        tv(g, 330, 960, 0.8, t, "title", 3 * math.sin(t * 4))
        for i, (txt, col) in enumerate((("ตลกร้าย", RED), ("จิกกัดสังคม", PURPLE), ("เล่นกับศีลธรรม", DARK))):
            k = ap(t, L[i] + 0.3)
            if k < 0.02:
                continue
            with g.at(800, 560 + i * 200, k, -4 + 4 * i):
                g.rrect(-190, -60, 380, 120, 30, WHITE, 7, stroke=col)
                g.label(txt, 0, 0, 50, color=col)
        title(g, t, L[0] if t < L[1] - 0.2 else L[1], "เส้นทางไม่ได้โรยด้วยกลีบกุหลาบ" if t < L[1] - 0.2
              else "มุกแรงแบบไม่ไว้หน้าใคร", INK, 76, y=360)
        return
    if t < L[4] - 0.2:   # โดนถล่ม
        for i in range(3):
            person(g, 180 + i * 330, GROUND, FANS[i], 0.6, mood="angry", pose="fist" if i != 1 else "point",
                   turn=0.2 - 0.2 * i, seed=20 + i, talk=True)
        title(g, t, L[3], "โดนถล่มจากหลายกลุ่ม!", RED, 86)
        return
    if t < L[6] - 0.2:   # ผังเวลาชนรายการยักษ์ / เรตติ้งดิ่ง
        person(g, 230, GROUND, EXECS[1], 0.75, mood="smug", pose="point", turn=0.4, seed=11)
        if t < L[5] - 0.2:
            tv(g, 640, 900, 0.55, t, "title", -6)
            with g.at(860, 760, ap(t, L[4] + 0.4), 8):
                g.rrect(-120, -90, 240, 180, 20, NAVY, 7)
                g.label("รายการยักษ์", 0, 0, 40, color=GOLD2)
            title(g, t, L[4], "ย้ายผังไปชนรายการยักษ์ใหญ่", DARK, 76)
        else:
            chart(g, 720, 840, 0.8, e_out(seg(t, L[5] - 0.2, L[5] + 1.2)), False, RED)
            title(g, t, L[5], "เรตติ้งดิ่งเหว!", RED, 96)
        return
    tv(g, 640, 1000, 0.9, t, "static" if t > L[6] + 0.4 else "title")   # ยกเลิก 2 ครั้ง / ตายสนิท
    stamp(g, 640, 650, "CANCELLED", 0.9, -12, RED, ap(t, L[6] + 0.3))
    if t > L[6] + 1.4 and t < L[7] - 0.2:
        stamp(g, 660, 800, "CANCELLED", 0.9, 10, RED, ap(t, L[6] + 1.5))
    if t < L[7] - 0.2:
        title(g, t, L[6], "ถูกยกเลิกถึง 2 ครั้ง!", RED, 90)
    else:
        title(g, t, L[7], "ใครก็คิดว่าตายสนิทแล้ว...", DARK, 82)


# ------------------------------------------------------------------ 4. revive
def s_revive(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:
        seth(g, CX, 0.9, "firm", "fist", 0)
        title(g, t, L[0], "แต่เซธไม่ยอมแพ้...", NAVY, 90)
        return
    if t < L[2] - 0.2:   # DVD + รีรัน พุ่ง
        dvd_stack(g, 300, 1150, 1.1, int(lerp(1, 9, e_out(seg(t, L[1], L[1] + 2.0)))), t)
        chart(g, 760, 840, 0.7, e_out(seg(t, L[1] + 0.3, L[1] + 1.8)), True, GREEN)
        title(g, t, L[1], "ดีวีดีขายถล่มทลาย!", GREEN, 90)
        return
    if t < L[4] - 0.2:   # แฟนเรียกร้อง / Fox ดึงกลับ
        if t < L[3] - 0.2:
            for i in range(3):
                person(g, 160 + i * 300, GROUND, FANS[i], 0.6, mood="shout", pose="fist", turn=0.2 - 0.2 * i,
                       seed=20 + i, talk=True)
                placard(g, 290 + i * 300, GROUND - 200, 0.65, -6 + 6 * i)
            title(g, t, L[2], "แฟน ๆ รวมตัวเรียกร้อง!", FG_BLUE, 84)
        else:
            tv(g, CX, 960, 1.1, t, "title")
            for i in range(6):
                g.sparkle(CX + 380 * math.cos(i * 1.05 + t), 900 + 300 * math.sin(i * 1.05 + t), 34)
            stamp(g, CX, 640, "IS BACK!", 1.0, -8, GREEN, ap(t, L[3] + 0.3))
            title(g, t, L[3], "Family Guy กลับมาแล้ว!", GREEN, 84, y=330)
        return
    if t < L[6] - 0.2:   # เขียนบท + พากย์เกือบครึ่งเรื่อง
        seth(g, 260, 0.85, "smile", "phone", 0.4, talk=True)
        mic(g, 400, 820, 0.7, -10)
        if t < L[5] - 0.2:
            pencil(g, 760, 820, 1.0, 20)
            title(g, t, L[4], "ไม่ได้แค่เขียนบท...", NAVY, 88)
        else:
            g.label("ทึ่ง!", 800, 760, 90, color=RED, sc=ap(t, L[5] + 0.3), rot=8)
            title(g, t, L[5], "พากย์เองเกือบครึ่งเรื่อง!", RED, 86)
        return
    seth(g, 230, 0.8, "smile", "phone", 0.4, talk=True)   # ปีเตอร์ สตีวี ไบรอัน
    cards = (("ปีเตอร์ กริฟฟิน", "พ่อจอมป่วน", FG_BLUE, L[6]), ("สตีวี", "ทารกอัจฉริยะสุดแสบ", RED, L[6] + 1.3),
             ("ไบรอัน", "สุนัขพูดได้", GREEN, L[7]))
    for i, (nm, sub, col, a) in enumerate(cards):
        k = ap(t, a)
        if k < 0.02:
            continue
        with g.at(0, 8 * math.sin(t * 2 + i)):
            voice_card(g, 700, 560 + i * 230, 0.9 * k, -3 + 3 * i, nm, sub, col)
    title(g, t, L[6], "เสียงของเซธทั้งหมด!", PURPLE, 84, y=360)


# ------------------------------------------------------------------ 5. ted
def s_ted(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[3] - 0.2:   # Ted หมีเท็ดดี้ / กำกับ เขียนบท โมแคป
        if t < L[1] - 0.2:
            seth(g, CX, 0.9, "smug", "fist", 0)
            title(g, t, L[0], "ความเกรียนยังไม่หยุดแค่นั้น!", RED, 80)
        else:
            clapper(g, 300, 760, 1.0 * ap(t, L[1]) + 0.01, -6, t)
            teddy(g, 760, GROUND, 1.0 * ap(t, L[1] + 0.3) + 0.01, 4 * math.sin(t * 2), t)
            if t < L[2] - 0.2:
                title(g, t, L[1], "ภาพยนตร์เรื่อง Ted", GOLDTXT, 92)
            else:
                g.circle(860, 900 - 40 * ((t * 0.6) % 1), 26, (0.8, 0.8, 0.82, 1 - (t * 0.6) % 1), 0)
                title(g, t, L[2], "หมีเท็ดดี้สุดหยาบคาย", RED, 88)
        return
    if t < L[4] - 0.2:   # กำกับ เขียนบท โมแคป
        seth(g, 280, 0.85, "smile", "point", 0.4, talk=True)
        for i, (txt, col) in enumerate((("กำกับ", NAVY), ("เขียนบท", PURPLE), ("โมชั่นแคปเจอร์ + พากย์", RED))):
            with g.at(760, 560 + i * 200, ap(t, L[3] + 0.4 * i), -4 + 4 * i):
                g.rrect(-220, -60, 440, 120, 30, WHITE, 7, stroke=col)
                g.label(txt, 0, 0, 46, color=col)
        title(g, t, L[3], "ทำเองแทบทุกอย่าง!", GOLDTXT, 88, y=360)
        return
    teddy(g, 300, GROUND, 0.85, 0, t)   # หนัง R ทำเงินสูงสุด / 500 ล้าน
    money(g, 700, 1050, 0.9, t)
    if t < L[5] - 0.2:
        with g.at(760, 640, ap(t, L[4]), -6):
            g.rrect(-120, -80, 240, 160, 20, RED, 7)
            g.label("R", 0, 0, 110, color=GOLD2)
        title(g, t, L[4], "หนังตลกเรต R ทำเงินสูงสุด!", RED, 80)
    else:
        n = int(lerp(0, 500, e_out(seg(t, L[5], L[5] + 1.5))))
        g.label(f"${n} ล้าน", 760, 700, 100, color=GREEN, sc=ap(t, L[5]))
        title(g, t, L[5], "กวาดเงินกว่า 500 ล้านดอลลาร์!", GREEN, 76)


# ------------------------------------------------------------------ 6. lesson
def s_lesson(g, t, L, d):
    g.ground(GROUND, WHITE)
    seth(g, 280, 0.85, "smile", "down" if t < L[3] - 0.2 else "wave", 0.3)
    if t < L[1] - 0.2:
        pencil(g, 760, 820, 1.0, 20 + 6 * math.sin(t * 3))
        title(g, t, L[0], "ชีวิตของเซธพิสูจน์ว่า...", INK, 84)
    elif t < L[2] - 0.2:
        for i, txt in enumerate(("ถูกมองข้าม", "ถูกต่อต้าน")):
            with g.at(780, 600 + i * 220, ap(t, L[1] + 0.4 * i), -4 + 8 * i):
                g.rrect(-190, -60, 380, 120, 30, WHITE, 7, stroke=RED)
                g.label(txt, 0, 0, 52, color=RED)
        title(g, t, L[1], "ความคิดแหวกขนบในตอนแรก", PURPLE, 78)
    elif t < L[3] - 0.2:
        with g.at(780, 760, ap(t, L[2]), -4):
            g.rrect(-220, -80, 440, 160, 40, WHITE, 8, stroke=GREEN)
            g.label("ซื่อสัตย์กับตัวเอง", 0, 0, 50, color=GREEN)
        title(g, t, L[2], "ซื่อสัตย์กับอารมณ์ขันของเรา", GREEN, 76)
    else:
        for i in range(6):
            g.sparkle(780 + 220 * math.cos(i * 1.05 + t), 780 + 220 * math.sin(i * 1.05 + t), 32)
        title(g, t, L[3], "โลกจะเปิดรับในที่สุด!", GOLDTXT, 88)


# ------------------------------------------------------------------ 7. outro
def s_outro(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[3] - 0.2:
        seth(g, 250, 0.8, "smile", "think" if t > L[2] - 0.2 else "down", 0.3, talk=True)
        if t < L[2] - 0.2:
            tv(g, 740, 760, 0.55, t, "title", -4)
            teddy(g, 760, GROUND, 0.55, 4 * math.sin(t * 2), t)
            title(g, t, L[0] if t < L[1] - 0.2 else L[1], "ชอบผลงานไหนที่สุด?" if t < L[1] - 0.2
                  else "Ted หรือ Family Guy?", FG_BLUE, 88)
        else:
            with g.at(760, 760, ap(t, L[2]), -4):
                g.rrect(-230, -110, 460, 220, 40, WHITE, 8, stroke=RED)
                g.label("ตลกร้าย", 0, -30, 70, color=RED)
                g.label("ยังจำเป็นไหม?", 0, 50, 46, color=GREY)
            title(g, t, L[2], "มุกตลกร้ายยุคนี้?", RED, 88)
        return
    with g.at(CX + 170, 640, ap(t, L[3])):   # ชวนคอมเมนต์
        g.bubble(0, 0, 460, 220, WHITE, tail=(-1, 1))
        for i in range(3):
            g.circle(-110 + i * 110, 0, 24 + 6 * math.sin(t * 6 - i), INK, 0)
    seth(g, 250, 0.8, "smile", "wave", 0.3, talk=True)
    title(g, t, L[3], "คอมเมนต์แลกเปลี่ยนกันได้เลย!", RED, 64)


SCENES = {
    "hook": s_hook, "young": s_young, "cancel": s_cancel, "revive": s_revive, "ted": s_ted, "lesson": s_lesson,
    "outro": s_outro,
}
NO_IRIS = set()
