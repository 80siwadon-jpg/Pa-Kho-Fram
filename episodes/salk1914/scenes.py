"""ฉากตอน: วันเกิดโจนัส ซอล์ก (28 ต.ค. 1914) — วัคซีนโปลิโอที่ไม่จดสิทธิบัตร"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from chars import (KIDS, MURROW, PARENTS, PUPILS, SALK, SALK_KID, SALK_LAB, SONS, WIFE, bell, compound_scope,  # noqa: E402
                   crutches, dead_virus, globe, headline, heart, house_closed, iron_lung, money, patent,
                   pool_closed, price_tag, sun, syringe, tv, vial, virus)
from gfx import GOLD, GOLD2, GREY, INK, NAVY, RED, W, WHITE, e_io, e_out, hexc, lerp, pop, seg  # noqa: E402
from people import person  # noqa: E402

CX = W / 2
GROUND = 1270
GOLDTXT = hexc("#b37a12")
GREEN = hexc("#3c8d4f")
TEAL = hexc("#2b7a8a")

CAMERA = {"hook": "push_in", "young": "pan_right", "polio": "dutch", "lab": "push_in", "sun": "pull_out",
          "legacy": "pan_left", "lesson": "push_in", "outro": "pan_right"}
TRANSITIONS = {"young": "zoom", "polio": "whip", "lab": "iris", "sun": "fade", "legacy": "zoom", "lesson": "fade",
               "outro": "whip"}


def ap(t, a, dur=0.38):
    return pop(t, a - 0.2, dur)


def title(g, t, a, txt, col=INK, size=84, y=380):
    g.label(txt, CX, y, size, color=col, sc=ap(t, a), rot=-3)


def salk(g, x, look=SALK_LAB, sc=0.82, mood="smile", pose="down", turn=0.3, talk=False):
    person(g, x, GROUND, look, sc, mood=mood, pose=pose, turn=turn, seed=3, talk=talk)


def kids_row(g, t, x0=200, dx=230, sc=0.62, mood="smile", n=3, seed=40):
    looks = PUPILS + KIDS
    for i in range(n):
        person(g, x0 + i * dx, GROUND, looks[i % len(looks)], sc, mood=mood, pose="wave" if i % 2 else "down",
               turn=0.3 - 0.2 * i, seed=seed + i)


# ------------------------------------------------------------------ 1. hook
def s_hook(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # ปฏิเสธเงินกว่าสองแสนล้านบาท
        salk(g, 300, SALK, 0.82, "smile", "stop", 0.4)
        g.name_tag(t, L[1] + 0.1, 760, 1120, "ดร.โจนัส ซอล์ก", "ผู้พัฒนาวัคซีนโปลิโอ", side=-1)
        title(g, t, L[1], "ปฏิเสธเงินกว่าสองแสนล้านบาท!", GOLDTXT, 80)
        return
    if t < L[3] - 0.2:   # สละสิทธิบัตร ให้เด็กทั้งโลกเข้าถึงฟรี
        vial(g, 760, 920, 1.1, 5, glow=1.0)
        kids_row(g, t, 170, 190, 0.55, n=3)
        g.label("ฟรี!", 760, 560, 100, color=GREEN, sc=ap(t, L[2] + 1.0), rot=6)
        title(g, t, L[2], "สละสิทธิบัตร ให้ทุกคนเข้าถึงได้", GREEN, 78)
        return
    sun(g, CX, 800, 170, t)   # จดสิทธิบัตรดวงอาทิตย์?
    patent(g, 840, 1080, 0.5 * ap(t, L[3] + 1.0) + 0.01, 8, seg(t, L[3] + 2.0, L[3] + 2.8))
    title(g, t, L[3], "\"จดสิทธิบัตรดวงอาทิตย์ได้ยังไง?\"", GOLDTXT, 74)


# ------------------------------------------------------------------ 2. young
def s_young(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:   # 28 ต.ค. 1914 นิวยอร์ก
        g.calendar(CX, 860, 1.25 * ap(t, L[0]) + 0.01, 28, "พุธ", "ต.ค. 1914")
        g.label("มหานครนิวยอร์ก", CX, 1150, 62, color=NAVY, sc=ap(t, L[0] + 1.6))
        title(g, t, L[0], "28 ตุลาคม 1914", TEAL, 92)
        return
    if t < L[4] - 0.2:   # ครอบครัวผู้อพยพยากจน / พ่อแม่ไม่ได้เรียน / ทุ่มเทให้ลูกเรียน
        for i, lk in enumerate(PARENTS):
            person(g, 220 + i * 600, GROUND, lk, 0.76, mood="smile" if t > L[3] - 0.2 else "neutral",
                   pose="down", turn=0.4 - 0.8 * i, seed=10 + i)
        person(g, CX, GROUND, SALK_KID, 0.85, mood="smile", pose="hold" if t > L[3] - 0.2 else "down", turn=0.0,
               seed=12)
        if t < L[2] - 0.2:
            title(g, t, L[1], "ครอบครัวผู้อพยพชาวยิวที่ยากจน", INK, 78)
        elif t < L[3] - 0.2:
            title(g, t, L[2], "พ่อแม่แทบไม่ได้เรียนหนังสือ", GREY, 82)
        else:
            with g.at(CX + 110, 900, ap(t, L[3] + 0.2), -10):
                g.rrect(-60, -80, 120, 160, 8, hexc("#3f6496"), 5)
            title(g, t, L[3], "ทุ่มเททุกอย่างให้ลูกได้เรียน", GREEN, 82)
        return
    salk(g, 320, SALK_LAB, 0.84, "smile", "down", 0.4)   # เติบโตเป็นแพทย์-นักวิจัย
    compound_scope(g, 760, GROUND, 1.1)
    title(g, t, L[4], "แพทย์และนักวิจัยผู้มุ่งมั่น", TEAL, 86)


# ------------------------------------------------------------------ 3. polio
def s_polio(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # ทศวรรษ 40-50 โปลิโอคือฝันร้าย
        virus(g, CX, 860, 200 * ap(t, L[0] + 0.3) + 1, t, "angry", hexc("#d9665a"))
        if t < L[1] - 0.2:
            title(g, t, L[0], "ทศวรรษ 1940 - 1950", INK, 92)
        else:
            g.label("โปลิโอ", CX, 1150, 90, color=RED, sc=ap(t, L[1]))
            title(g, t, L[1], "ฝันร้ายที่สุดของมนุษยชาติ", RED, 84)
        return
    if t < L[3] - 0.2:   # ทุกฤดูร้อน ปิดบ้าน ปิดสระ
        house_closed(g, 260, GROUND, 0.9)
        pool_closed(g, 720, GROUND - 20, 0.75, t)
        g.circle(840, 520, 70, GOLD2, 6)
        title(g, t, L[2], "ฤดูร้อนแห่งความหวาดผวา", GOLDTXT, 86)
        return
    if t < L[4] - 0.2:   # พุ่งเป้าทำร้ายเด็ก
        kids_row(g, t, 200, 230, 0.62, "worry", 3, 50)
        for i in range(3):
            virus(g, 200 + i * 230 + 60 * math.sin(t + i), 620 + 30 * math.sin(t * 2 + i), 50, t, "angry",
                  hexc("#d9665a"))
        title(g, t, L[3], "ไวรัสพุ่งเป้าทำร้ายเด็ก ๆ", RED, 84)
        return
    if t < L[5] - 0.2:   # อัมพาต แขนขาลีบ (ไม้ค้ำ)
        person(g, 340, GROUND, PUPILS[0], 0.66, mood="sad", pose="down", turn=0.3, seed=60)
        crutches(g, 340, GROUND, 0.85)
        title(g, t, L[4], "อัมพาต แขนขาลีบ", INK, 92)
        return
    iron_lung(g, 480, GROUND - 20, 1.0, t)   # ปอดเหล็ก
    g.label("\"ปอดเหล็ก\"", 480, 680, 80, color=NAVY, sc=ap(t, L[5] + 0.4))
    title(g, t, L[5], "ต้องนอนในปอดเหล็กเพื่อหายใจ", INK, 80)


# ------------------------------------------------------------------ 4. lab
def s_lab(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:   # ทุ่มเทในห้องทดลอง
        salk(g, 300, SALK_LAB, 0.82, "firm", "hold", 0.4)
        compound_scope(g, 730, GROUND, 1.1)
        for i in range(3):
            u = (t * 0.5 + i / 3) % 1
            g.circle(560 + 40 * i, 760 - 200 * u, 14, (*TEAL[:3], 1 - u), 3)
        title(g, t, L[0], "ทุ่มเทในห้องทดลองไม่รู้เหน็ดเหนื่อย", TEAL, 74)
        return
    if t < L[3] - 0.2:   # วัคซีนจากเชื้อตาย ขัดความเชื่อเดิม
        dead_virus(g, 330, 840, 150, t, e_io(seg(t, L[1] + 0.6, L[1] + 1.6)))
        g.label("→", CX, 860, 100, color=GREY, sc=ap(t, L[1] + 1.4))
        vial(g, 770, 1000, 1.0, 5, glow=ap(t, L[1] + 1.8))
        if t < L[2] - 0.2:
            title(g, t, L[1], "วัคซีนจาก \"เชื้อที่ตายแล้ว\"", TEAL, 84)
        else:
            g.label("ขัดความเชื่อเดิม!", CX, 600, 70, color=RED, sc=ap(t, L[2] + 0.2), rot=-5)
            title(g, t, L[2], "กล้าคิดต่างจากวงการแพทย์", RED, 82)
        return
    if t < L[5] - 0.2:   # ทดลองในสัตว์สำเร็จ / พิสูจน์ความปลอดภัย
        compound_scope(g, 300, GROUND, 1.0)
        with g.at(760, 860, ap(t, L[3] + 0.2)):
            g.circle(0, 0, 130, WHITE, 8, stroke=GREEN)
            g.line([(-60, 0), (-15, 50), (70, -50)], 18, GREEN, amp=0)
        if t < L[4] - 0.2:
            title(g, t, L[3], "ทดลองในสัตว์สำเร็จ!", GREEN, 90)
        else:
            title(g, t, L[4], "พิสูจน์ความปลอดภัยให้ถึงที่สุด", INK, 82)
        return
    if t < L[6] - 0.2:   # ฉีดให้ภรรยา ลูกสามคน และตัวเอง
        salk(g, 190, SALK_LAB, 0.72, "smile", "hold", 0.4)
        person(g, 410, GROUND, WIFE, 0.68, mood="smile", pose="down", turn=0.2, seed=20)
        for i, lk in enumerate(SONS):
            person(g, 600 + i * 150, GROUND, lk, 0.72, mood="smile", pose="wave" if i == 1 else "down",
                   turn=-0.2, seed=21 + i)
        syringe(g, 300, 660, 0.6, -20, 1 - seg(t, L[5] + 1.0, L[5] + 3.0))
        title(g, t, L[5], "ฉีดให้ครอบครัวและตัวเองก่อน!", RED, 80)
        return
    if t < L[7] - 0.2:   # ทดลองในเด็กเกือบสองล้านคน
        kids_row(g, t, 170, 185, 0.5, "smile", 5, 70)
        n = int(lerp(1, 1_800_000, e_out(seg(t, L[6], L[6] + 2.2))))
        g.label(f"{n:,} คน", CX, 620, 92, color=TEAL, sc=ap(t, L[6] + 0.2))
        title(g, t, L[6], "ทดลองในเด็กเกือบสองล้านคน", TEAL, 82)
        return
    if t < L[10] - 0.2:   # 12 เม.ย. 1955 ประกาศ ได้ผลและปลอดภัย
        if t < L[9] - 0.2:
            g.calendar(CX, 860, 1.2 * ap(t, L[7]) + 0.01, 12, "อังคาร", "เม.ย. 1955")
            title(g, t, L[7] if t < L[8] - 0.2 else L[8], "12 เมษายน 1955" if t < L[8] - 0.2 else
                  "ข่าวดีที่ทั้งโลกรอคอย!", GREEN, 88)
        else:
            headline(g, CX, 880, 0.95 * ap(t, L[9]) + 0.01, -3 + 2 * math.sin(t * 2))
            title(g, t, L[9], "วัคซีนได้ผลและปลอดภัย!", GREEN, 88)
        return
    bell(g, CX, 640, 1.0, t, 1.0)   # ระฆังดัง ผู้คนกอดกันร้องไห้
    kids_row(g, t, 200, 230, 0.6, "smile", 3, 80)
    for i in range(4):
        u = (t * 0.7 + i / 4) % 1
        heart(g, 200 + i * 230, 1000 - 300 * u, 26, RED, 1 - u)
    title(g, t, L[10], "ระฆังดังสนั่น ผู้คนโล่งอก!", GOLDTXT, 84)


# ------------------------------------------------------------------ 5. sun
def s_sun(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:   # ยิ่งใหญ่กว่านักวิทยาศาสตร์
        salk(g, CX, SALK, 0.86, "smile", "down", 0.0)
        for i in range(6):
            g.sparkle(CX + 330 * math.cos(i * 1.05 + t), 820 + 260 * math.sin(i * 1.05 + t), 26)
        title(g, t, L[0], "วีรบุรุษที่ยิ่งใหญ่กว่านักวิทยาศาสตร์", GOLDTXT, 74)
        return
    if t < L[3] - 0.2:   # เมอร์โรว์ถามในทีวี
        tv(g, 680, 840, 1.0, t, True, MURROW)
        salk(g, 220, SALK, 0.72, "neutral", "down", 0.4)
        g.name_tag(t, L[1] + 0.2, 700, 1130, "เอ็ดเวิร์ด อาร์. เมอร์โรว์", "นักข่าวโทรทัศน์ชื่อดัง", side=-1)
        if t < L[2] - 0.2:
            title(g, t, L[1], "นักข่าวชื่อดังถามออกทีวี", NAVY, 84)
        else:
            title(g, t, L[2], "\"ใครเป็นเจ้าของสิทธิบัตร?\"", RED, 86)
        return
    if t < L[4] - 0.2:   # ตอบทันทีด้วยรอยยิ้ม
        salk(g, CX, SALK, 0.86, "smile", "down", 0.0, talk=True)
        title(g, t, L[3], "ตอบทันทีด้วยรอยยิ้ม...", INK, 88)
        return
    if t < L[5] - 0.2:   # ก็ประชาชนน่ะสิ ไม่มีสิทธิบัตร
        salk(g, 280, SALK, 0.8, "smile", "wave", 0.3, talk=True)
        kids_row(g, t, 600, 180, 0.5, "smile", 3, 90)
        title(g, t, L[4], "\"ก็ประชาชนน่ะสิครับ\"", GREEN, 92)
        return
    salk(g, 260, SALK, 0.78, "smile", "point", 0.3, talk=True)   # จดสิทธิบัตรดวงอาทิตย์?
    sun(g, 740, 760, 150 * ap(t, L[5]) + 1, t)
    title(g, t, L[5], "\"จดสิทธิบัตรดวงอาทิตย์ได้ยังไง?\"", GOLDTXT, 74)


# ------------------------------------------------------------------ 6. legacy
def s_legacy(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # ไม่จดสิทธิบัตร → แจกจ่ายทั่วโลกราคาทุน
        if t < L[1] - 0.2:
            patent(g, CX, 860, 1.0, -3, e_io(seg(t, L[0] + 0.5, L[0] + 1.3)))
            title(g, t, L[0], "ไม่จดสิทธิบัตร!", RED, 96)
        else:
            globe(g, 400, 860, 220, t)
            for i in range(6):
                a = t * 1.2 + i * 1.05
                vial(g, 400 + 300 * math.cos(a), 860 + 300 * math.sin(a) + 60, 0.35, 0)
            price_tag(g, 820, 1100, 0.8 * ap(t, L[1] + 0.8) + 0.01, -6)
            title(g, t, L[1], "แจกจ่ายทั่วโลกในราคาทุน", GREEN, 84)
        return
    if t < L[4] - 0.2:   # ช่วยเด็กนับล้าน / โปลิโอเกือบหมดจากโลก
        if t < L[3] - 0.2:
            kids_row(g, t, 200, 230, 0.64, "smile", 3, 100)
            for i in range(3):
                heart(g, 200 + i * 230, 620 - 10 * math.sin(t * 3 + i), 32 * ap(t, L[2] + 0.3 * i, 0.3) + 0.1)
            title(g, t, L[2], "เด็กนับล้านไม่ต้องพิการ", GREEN, 86)
        else:
            globe(g, CX, 860, 240, t)
            dead_virus(g, CX + 210, 660, 70, t, 1.0)
            k = seg(t, L[3] + 0.4, L[3] + 1.0)
            if k > 0:
                g.line([(CX + 120, 570), (CX + 120 + 180 * k, 570 + 180 * k)], 14, RED, amp=0)
            title(g, t, L[3], "โปลิโอเกือบหมดไปจากโลก", GREEN, 84)
        return
    salk(g, 280, SALK, 0.8, "smile", "stop", 0.4)   # ถ้าจดจะรวย 7,000 ล้านดอลลาร์
    money(g, 760, 1150, 1.3, t)
    if t < L[5] - 0.2:
        title(g, t, L[4], "ถ้าเขาจดสิทธิบัตร...", INK, 90)
    elif t < L[6] - 0.2:
        g.label("$7,000,000,000", 740, 700, 70, color=GREEN, sc=ap(t, L[5] + 0.2), rot=-4)
        title(g, t, L[5], "รวยกว่า 7,000 ล้านดอลลาร์!", GOLDTXT, 84)
    else:
        g.label("> 200,000,000,000 ฿", 740, 700, 60, color=GOLDTXT, sc=ap(t, L[6]), rot=-4)
        title(g, t, L[6], "หรือกว่าสองแสนล้านบาท!", GOLDTXT, 86)


# ------------------------------------------------------------------ 7. lesson
def s_lesson(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:
        salk(g, CX, SALK, 0.86, "smile", "down", 0.0)
        title(g, t, L[0], "เรื่องราวนี้เตือนใจเราว่า...", INK, 84)
        return
    if t < L[2] - 0.2:   # ไม่ได้วัดที่ตัวเลขในบัญชี
        with g.at(CX, 860, ap(t, L[1] + 0.2), -3):
            g.rrect(-280, -180, 560, 360, 20, WHITE, 8)
            g.text("บัญชี", 0, -120, 50, "kanit", INK)
            g.text("$ 0", 0, 20, 110, "kanit", GREY)
        title(g, t, L[1], "ไม่ได้วัดที่ตัวเลขในบัญชี", INK, 84)
        return
    kids_row(g, t, 200, 230, 0.62, "smile", 3, 110)   # คุณค่าที่มอบให้เพื่อนมนุษย์
    heart(g, CX, 640 + 10 * math.sin(t * 3), 110 * ap(t, L[2]) + 1)
    title(g, t, L[2], "คุณค่าที่มอบให้เพื่อนมนุษย์", RED, 84)


# ------------------------------------------------------------------ 8. outro
def s_outro(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:
        salk(g, 300, SALK, 0.8, "smile", "wave", 0.3)
        heart(g, 760, 760, 100 + 10 * math.sin(t * 4))
        title(g, t, L[0], "รู้สึกอย่างไรกันบ้าง?", INK, 92)
        return
    if t < L[4] - 0.2:   # เสียสละ vs จดสิทธิบัตร
        vial(g, CX, 1000, 1.0, 0, glow=1.0)
        if t > L[2] - 0.2:
            with g.at(250, 760, ap(t, L[2]), -6):
                g.rrect(-180, -90, 360, 180, 20, WHITE, 8, stroke=GREEN)
                g.label("เสียสละ", 0, 0, 64, color=GREEN)
        if t > L[3] - 0.2:
            with g.at(830, 760, ap(t, L[3]), 6):
                g.rrect(-180, -90, 360, 180, 20, WHITE, 8, stroke=GOLDTXT)
                g.label("จดสิทธิบัตร", 0, 0, 56, color=GOLDTXT)
        if t < L[2] - 0.2:
            title(g, t, L[1], "ถ้าคุณถือสิ่งที่ทั้งโลกต้องการ...", INK, 78)
        else:
            title(g, t, L[2] if t < L[3] - 0.2 else L[3], "เสียสละเพื่อโลก หรือ จดสิทธิบัตร?", RED, 76)
        return
    with g.at(CX + 170, 640, ap(t, L[4])):   # ชวนคอมเมนต์
        g.bubble(0, 0, 460, 220, WHITE, tail=(-1, 1))
        for i in range(3):
            g.circle(-110 + i * 110, 0, 24 + 6 * math.sin(t * 6 - i), INK, 0)
    salk(g, 260, SALK, 0.8, "smile", "wave", 0.3, talk=True)
    title(g, t, L[4], "มาแลกเปลี่ยนกันในคอมเมนต์!", RED, 70)


SCENES = {
    "hook": s_hook, "young": s_young, "polio": s_polio, "lab": s_lab, "sun": s_sun, "legacy": s_legacy,
    "lesson": s_lesson, "outro": s_outro,
}
NO_IRIS = set()
