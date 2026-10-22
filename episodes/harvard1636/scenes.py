"""ฉากตอน: ก่อตั้งวิทยาลัยที่กลายเป็นมหาวิทยาลัยฮาร์วาร์ด (28 ต.ค. 1636)"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from chars import (CRIMSON, JOHN, MODERN, PURITANS, TEACHER, book, cabin, candle, forest, grad_cap, hall,  # noqa: E402
                   medal, nine_students, pounds, president_icon, quill, seedling, shelf, tree, watering_can,
                   will_scroll)
from gfx import GOLD, GOLD2, GREY, INK, NAVY, RED, W, WHITE, e_io, e_out, hexc, lerp, pop, seg  # noqa: E402
from people import person  # noqa: E402

CX = W / 2
GROUND = 1270
GOLDTXT = hexc("#b37a12")
GREEN = hexc("#3c8d4f")

CAMERA = {"hook": "push_in", "founding": "pan_right", "humble": "dutch", "john": "push_in", "grow": "tilt_up",
          "lesson": "pull_out", "outro": "pan_right"}
TRANSITIONS = {"founding": "zoom", "humble": "whip", "john": "iris", "grow": "zoom", "lesson": "fade",
               "outro": "whip"}


def ap(t, a, dur=0.38):
    return pop(t, a - 0.2, dur)


def title(g, t, a, txt, col=INK, size=84, y=380):
    g.label(txt, CX, y, size, color=col, sc=ap(t, a), rot=-3)


def year_card(g, x, y, sc, txt, col=INK, rot=0.0):
    if sc < 0.02:
        return
    with g.at(x, y, sc, rot):
        g.rrect(-180, -85, 360, 170, 30, WHITE, 8, stroke=col)
        g.text(txt, 0, 0, 96, "kanit", col)


# ------------------------------------------------------------------ 1. hook
def s_hook(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # ก่อนสหรัฐฯ ประกาศอิสรภาพกว่าร้อยปี
        g.flag(640, 600, 260, 170, "us", t)
        g.line([(640, 600), (640, GROUND)], 8, INK, amp=0)
        year_card(g, 780, 900, 0.8, "1776", NAVY, 5)
        year_card(g, 280, 900, 0.9 * ap(t, L[1] + 1.4), "1636", CRIMSON, -5)
        g.label("← 140 ปี", 530, 1100, 64, color=RED, sc=ap(t, L[1] + 2.0))
        title(g, t, L[1], "ก่อนอเมริกาจะเกิดกว่าร้อยปี", INK, 80)
        return
    if t < L[3] - 0.2:   # สถาบันเล็ก ๆ กลางป่ารกร้าง
        forest(g, GROUND, t)
        cabin(g, CX, GROUND, 0.7 * ap(t, L[2] + 0.3) + 0.01)
        title(g, t, L[2], "สถาบันเล็ก ๆ กลางป่ารกร้าง", GREEN, 82)
        return
    hall(g, CX, GROUND, 1.0 * ap(t, L[3]) + 0.01, t)   # มหาวิทยาลัยทรงอิทธิพลที่สุด
    for i in range(6):
        g.sparkle(CX + 380 * math.cos(i * 1.05 + t), 820 + 260 * math.sin(i * 1.05 + t), 26)
    title(g, t, L[3], "มหาวิทยาลัยทรงอิทธิพลที่สุดในโลก!", CRIMSON, 76)


# ------------------------------------------------------------------ 2. founding
def s_founding(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # 28 ต.ค. 1636 อาณานิคมแมสซาชูเซตส์ เบย์
        if t < L[1] - 0.2:
            g.calendar(CX, 860, 1.25 * ap(t, L[0]) + 0.01, 28, "อาทิตย์", "ต.ค. 1636")
            title(g, t, L[0], "28 ตุลาคม 1636", CRIMSON, 92)
        else:
            forest(g, GROUND, t, n=10)
            for i, x in enumerate((300, 640)):
                cabin(g, x, GROUND, 0.55)
            title(g, t, L[1], "อาณานิคมแมสซาชูเซตส์ เบย์", GREEN, 80)
        return
    if t < L[4] - 0.2:   # พิวริตันลงมติ 400 ปอนด์
        for i, lk in enumerate(PURITANS):
            person(g, 200 + i * 200, GROUND, lk, 0.66, mood="firm", pose="v" if (t > L[3] - 0.2 and i == 0) else "down",
                   turn=0.3 - 0.2 * i, seed=10 + i, talk=i == 0)
        if t < L[3] - 0.2:
            title(g, t, L[2], "ผู้ตั้งถิ่นฐานชาวอังกฤษยุคพิวริตัน", INK, 76)
        else:
            pounds(g, 830, 860, 0.9 * ap(t, L[3] + 0.3) + 0.01, t)
            title(g, t, L[3], "ลงมติจัดงบ 400 ปอนด์", GOLDTXT, 86)
        return
    if t < L[5] - 0.2:   # วิทยาลัยแห่งใหม่
        forest(g, GROUND, t, n=8)
        cabin(g, CX, GROUND, 0.9, "")
        with g.at(CX, 620, ap(t, L[4] + 0.3), -4):
            g.rrect(-260, -60, 520, 120, 16, WHITE, 7, stroke=CRIMSON)
            g.label("New College", 0, 0, 60, color=CRIMSON)
        title(g, t, L[4], "ก่อตั้ง \"วิทยาลัยแห่งใหม่\"", CRIMSON, 86)
        return
    # ฝึกบาทหลวงรุ่นใหม่ ไม่ให้คำสอนสูญหาย
    person(g, 300, GROUND, TEACHER, 0.8, mood="smile", pose="hold", turn=0.4, seed=20, talk=True)
    book(g, 420, GROUND - 400, 0.8, -10, PURITANS[0].suit, open_=True)
    if t < L[6] - 0.2:
        person(g, 760, GROUND, PURITANS[1], 0.62, mood="smile", pose="down", turn=-0.4, seed=21)
        title(g, t, L[5], "ฝึกอบรมบาทหลวงรุ่นใหม่", INK, 86)
    elif t < L[7] - 0.2:
        for i in range(4):
            u = (t * 0.6 + i / 4) % 1
            g.text("✝", 700 + 60 * i, 800 - 200 * u, 50, "kanit", (*GREY[:3], 1 - u))
        title(g, t, L[6], "ไม่ให้คำสอนศาสนาสูญหาย", NAVY, 84)
    else:
        candle(g, 760, GROUND - 40, 1.4, t)
        title(g, t, L[7], "เมื่อนักบวชรุ่นแรกล้มหายตายจาก", GREY, 74)


# ------------------------------------------------------------------ 3. humble
def s_humble(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:   # ไม่มีอาคารมั่นคง
        forest(g, GROUND, t, n=8)
        with g.at(CX, GROUND, 1, 4 * math.sin(t * 3)):
            cabin(g, 0, 0, 0.85)
        g.label("?!", 780, 700, 120, color=RED, sc=ap(t, L[0] + 0.6), rot=8)
        title(g, t, L[0], "ไม่มีแม้แต่อาคารเรียนที่มั่นคง", INK, 78)
        return
    if t < L[2] - 0.2:   # อาจารย์คนเดียว
        person(g, CX, GROUND, TEACHER, 0.85, mood="smile", pose="wave", turn=0.0, seed=20)
        g.label("1", 800, 700, 160, color=CRIMSON, sc=ap(t, L[1] + 0.2))
        title(g, t, L[1], "อาจารย์เพียงคนเดียว", INK, 90)
        return
    n = seg(t, L[2] + 0.2, L[2] + 1.8)   # นักศึกษา 9 คน
    nine_students(g, CX, GROUND, t, max(0.12, n))
    g.label(f"{max(1, int(9 * n + 0.999))} คน", CX, 620, 110, color=CRIMSON, sc=ap(t, L[2] + 0.2))
    title(g, t, L[2], "นักศึกษาเพียง 9 คน!", RED, 92)


# ------------------------------------------------------------------ 4. john
def s_john(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # สองปีต่อมา / จอห์น ฮาร์วาร์ด
        if t < L[1] - 0.2:
            year_card(g, 330, 860, 0.9, "1636", GREY, -4)
            g.label("→", CX, 860, 100, color=GREY, sc=ap(t, L[0] + 0.4))
            year_card(g, 760, 860, 0.9 * ap(t, L[0] + 0.8), "1638", CRIMSON, 4)
            title(g, t, L[0], "สองปีต่อมา... จุดเปลี่ยน!", INK, 86)
        else:
            person(g, 320, GROUND, JOHN, 0.84, mood="smile", pose="hold", turn=0.4, seed=30, talk=True)
            book(g, 450, GROUND - 400, 0.7, -8, CRIMSON)
            g.name_tag(t, L[1] + 0.2, 720, 1060, "จอห์น ฮาร์วาร์ด", "ศาสนาจารย์หนุ่ม", side=-1)
            title(g, t, L[1], "ศาสนาจารย์ \"จอห์น ฮาร์วาร์ด\"", NAVY, 80)
        return
    if t < L[3] - 0.2:   # ป่วยและเสียชีวิตในวัย 30
        candle(g, 700, GROUND - 120, 1.6, t)
        person(g, 330, GROUND, JOHN, 0.84, mood="sad", pose="down", turn=0.3, seed=30)
        g.label("วัย 30 ปี", 700, 640, 70, color=GREY, sc=ap(t, L[2] + 0.4))
        title(g, t, L[2], "ล้มป่วยและจากไปในวัย 30", GREY, 84)
        return
    if t < L[5] - 0.2:   # พินัยกรรม ครึ่งหนึ่ง + หนังสือ 400 เล่ม
        will_scroll(g, 320, 880, 0.9, -5 + 2 * math.sin(t * 1.5), e_io(seg(t, L[3], L[3] + 1.5)))
        quill(g, 470, 760, 0.9, 30)
        if t > L[4] - 0.2:
            shelf(g, 760, GROUND, 0.75, e_io(seg(t, L[4], L[4] + 2.2)), t)
            title(g, t, L[4], "ห้องสมุดกว่า 400 เล่ม!", CRIMSON, 86)
        else:
            title(g, t, L[3], "บริจาคทรัพย์สินครึ่งหนึ่ง", GOLDTXT, 86)
        return
    shelf(g, 280, GROUND, 0.6, 1.0, t)   # เปลี่ยนชื่อเป็นวิทยาลัยฮาร์วาร์ด
    cabin(g, 720, GROUND, 0.75)
    k = ap(t, L[6] + 0.2)
    if k > 0.02:
        with g.at(720, 680, k, -4):
            g.rrect(-250, -70, 500, 140, 16, WHITE, 8, stroke=CRIMSON)
            g.label("Harvard College", 0, 0, 56, color=CRIMSON)
    if t < L[6] - 0.2:
        title(g, t, L[5], "เพื่อเป็นเกียรติแก่ผู้มีพระคุณ", NAVY, 80)
    else:
        title(g, t, L[6], "\"วิทยาลัยฮาร์วาร์ด\"", CRIMSON, 96)


# ------------------------------------------------------------------ 5. grow
def s_grow(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # โรงเรียนเล็กกลางป่า → ผ่านร้อนผ่านหนาว
        k = e_io(seg(t, L[1], L[2]))
        forest(g, GROUND, t, n=8)
        if k < 0.5:
            cabin(g, CX, GROUND, 0.8)
        else:
            hall(g, CX, GROUND, 0.75, t)
        yr = int(lerp(1638, 1800, k))
        year_card(g, 820, 620, 0.6, str(yr), CRIMSON, 5)
        if t < L[1] - 0.2:
            title(g, t, L[0], "จากโรงเรียนเล็ก ๆ กลางป่า", GREEN, 82)
        else:
            title(g, t, L[1], "ผ่านร้อนผ่านหนาว ขยายรากฐาน", INK, 78)
        return
    if t < L[3] - 0.2:   # วิทยาศาสตร์ การแพทย์ กฎหมาย
        for i, (txt, col) in enumerate((("วิทยาศาสตร์", hexc("#3f6496")), ("การแพทย์", RED), ("กฎหมาย", GOLDTXT))):
            k = ap(t, L[2] + 0.6 * i, 0.3)
            if k > 0.02:
                book(g, 230 + i * 310, 1000 - 15 * abs(math.sin(t * 2.5 + i)), 1.0 * k, -6 + 6 * i + 4 * math.sin(t * 2 + i), col)
                g.label(txt, 230 + i * 310, 1100, 50, color=col, sc=k)
        title(g, t, L[2], "หลักสูตรครอบคลุมทุกศาสตร์", INK, 84)
        return
    if t < L[5] - 0.2:   # มหาวิทยาลัยฮาร์วาร์ด เก่าแก่ที่สุดในสหรัฐฯ
        hall(g, CX, GROUND, 1.0, t)
        if t < L[4] - 0.2:
            title(g, t, L[3], "\"มหาวิทยาลัยฮาร์วาร์ด\"", CRIMSON, 92)
        else:
            year_card(g, 820, 600, 0.6 * ap(t, L[4] + 0.3), "1636", CRIMSON, 6)
            title(g, t, L[4], "เก่าแก่ที่สุดในสหรัฐฯ", NAVY, 92)
        return
    if t < L[6] - 0.2:   # ประธานาธิบดี 8 คน
        for i in range(8):
            president_icon(g, 200 + (i % 4) * 230, 800 + (i // 4) * 300, 1.4, ap(t, L[5] + 0.15 * i, 0.3))
        title(g, t, L[5], "ประธานาธิบดีสหรัฐฯ 8 คน", NAVY, 86)
        return
    if t < L[7] - 0.2:   # โนเบลกว่า 160 คน
        medal(g, CX, 860, 210, 1.0 * ap(t, L[6]) + 0.01, 4 * math.sin(t * 2))
        n = int(lerp(1, 160, e_out(seg(t, L[6], L[6] + 1.8))))
        g.label(f"{n}+", CX, 1170, 100, color=GOLDTXT, sc=ap(t, L[6] + 0.2))
        title(g, t, L[6], "รางวัลโนเบลกว่า 160 คน", GOLDTXT, 86)
        return
    for i, lk in enumerate(MODERN):   # มหาเศรษฐีและผู้นำนับไม่ถ้วน
        person(g, 240 + i * 300, GROUND, lk, 0.66, mood="smile", pose="v" if i == 1 else "wave",
               turn=0.3 - 0.3 * i, seed=40 + i)
        grad_cap(g, 240 + i * 300, 560 - 20 * math.sin(t * 2 + i), 0.5, 10 * math.sin(t + i), t)
    title(g, t, L[7], "ผู้นำที่เปลี่ยนโลกนับไม่ถ้วน", CRIMSON, 82)


# ------------------------------------------------------------------ 6. lesson
def s_lesson(g, t, L, d):
    g.ground(GROUND, WHITE)
    k = e_io(seg(t, L[2] - 0.2, L[3] + 1.5))
    seedling(g, CX + 60, GROUND - 20, k, t, 1.0)
    if t < L[2] - 0.2:   # หนังสือเปิด แสงแห่งปัญญาส่องลงเมล็ด
        g.sunburst(CX + 60, 760, 90, 200, 14, t * 8, 8, (1, 0.85, 0.4, 0.6))
        book(g, CX + 60, 820 + 12 * math.sin(t * 2), 1.2, 0, CRIMSON, open_=True)
        for i in range(4):
            u = (t * 0.7 + i / 4) % 1
            g.circle(CX + 60 + 40 * math.sin(i * 2 + t), 840 + 330 * u, 8, (*GOLD2[:3], 1 - u), 0)
    if t < L[1] - 0.2:
        title(g, t, L[0], "เรื่องราวนี้พิสูจน์ว่า...", INK, 86)
    elif t < L[2] - 0.2:
        g.label("ผืนดินแร้นแค้น", CX, 1120, 56, color=hexc("#8a6a42"), sc=ap(t, L[1] + 0.4))
        title(g, t, L[1], "เมล็ดพันธุ์แห่งปัญญา", GREEN, 92)
    elif t < L[3] - 0.2:
        watering_can(g, 330, 760, 1.0, 20, t)
        title(g, t, L[2], "รดน้ำด้วยวิสัยทัศน์และการศึกษา", NAVY, 76)
    else:
        for i in range(5):
            g.sparkle(CX + 60 + 320 * math.cos(i * 1.25 + t), 760 + 200 * math.sin(i * 1.25 + t), 26)
        title(g, t, L[3], "ร่มเงาที่ค้ำจุนโลกทั้งใบ", GREEN, 88)


# ------------------------------------------------------------------ 7. outro
def s_outro(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:
        hall(g, 640, GROUND, 0.75, t)
        person(g, 230, GROUND, MODERN[1], 0.7, mood="neutral", pose="think", turn=0.4, seed=50)
        for i in range(4):
            u = (t * 0.5 + i / 4) % 1
            g.label("?", 380 + 150 * (i % 2), 820 - 300 * u, 70, color=(*CRIMSON[:3], 1 - u))
        g.label("?", 420, 640 + 40 * math.sin(t * 3), 110, color=CRIMSON, sc=ap(t, L[0] + 0.5), rot=10 * math.sin(t * 2))
        title(g, t, L[0], "คิดอย่างไรกันบ้าง?", INK, 92)
        return
    if t < L[4] - 0.2:   # ชื่อสถาบัน vs ทักษะจริง
        with g.at(300, 820, ap(t, L[1] + 0.2), -5):
            g.rrect(-200, -110, 400, 220, 20, WHITE, 8, stroke=CRIMSON)
            g.label("ชื่อสถาบัน", 0, 0, 60, color=CRIMSON)
        g.label("vs", CX, 900, 80, color=GREY, sc=ap(t, L[3] - 0.1))
        with g.at(780, 1000, ap(t, L[3]), 5):
            g.rrect(-200, -110, 400, 220, 20, WHITE, 8, stroke=GREEN)
            g.label("ทักษะจริง", 0, 0, 60, color=GREEN)
        if t < L[3] - 0.2:
            person(g, 780, GROUND, MODERN[1], 0.66, mood="neutral", pose="think", turn=-0.4, seed=52)
            grad_cap(g, 300, 1080, 0.6 * ap(t, L[2]) + 0.01, -8, t)
            title(g, t, L[1], "ชื่อเสียงยังเป็นใบเบิกทาง?", CRIMSON, 82)
        else:
            title(g, t, L[3], "หรือทักษะจริงสำคัญกว่า?", GREEN, 86)
        return
    with g.at(CX + 170, 640, ap(t, L[4])):   # ชวนคอมเมนต์
        g.bubble(0, 0, 460, 220, WHITE, tail=(-1, 1))
        for i in range(3):
            g.circle(-110 + i * 110, 0, 24 + 6 * math.sin(t * 6 - i), INK, 0)
    person(g, 250, GROUND, MODERN[0], 0.75, mood="smile", pose="wave", turn=0.3, seed=51, talk=True)
    grad_cap(g, 250, 520, 0.5, 8, t)
    title(g, t, L[4], "มาแลกเปลี่ยนกันในคอมเมนต์!", RED, 70)


SCENES = {
    "hook": s_hook, "founding": s_founding, "humble": s_humble, "john": s_john, "grow": s_grow,
    "lesson": s_lesson, "outro": s_outro,
}
NO_IRIS = set()
