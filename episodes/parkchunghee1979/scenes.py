"""ฉากตอน: การลอบสังหารประธานาธิบดีพัก จ็อง-ฮี (26 ต.ค. 1979) — ไม่แสดงการยิง/บาดแผล (ความมืด แสงวาบ เก้าอี้ล้ม)"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from chars import (CHA, CHUN, GUESTS, KIM, KIM_GEN, PARK, PROTESTERS, candle, chair, flash, gavel, house,  # noqa: E402
                   night, pistol, placard, table, taegeuk, tank)
from gfx import GOLD, GOLD2, GREY, INK, NAVY, RED, W, WHITE, e_io, e_out, hexc, lerp, pop, seg  # noqa: E402
from people import head, person  # noqa: E402

CX = W / 2
GROUND = 1270
GOLDTXT = hexc("#b37a12")
LIGHT = hexc("#f2c94c")   # หัวข้อบนฉากมืด (WHITE + ขอบขาวมองไม่เห็น)
DARK = hexc("#4a3a3a")
KBLUE = hexc("#1f4a8a")

CAMERA = {"hook": "push_in", "dinner": "pan_right", "tension": "dutch", "shots": "push_in", "after": "pan_left",
          "lesson": "pull_out", "outro": "pan_right"}
TRANSITIONS = {"dinner": "fade", "tension": "whip", "shots": "fade", "after": "iris", "lesson": "fade",
               "outro": "whip"}


def ap(t, a, dur=0.38):
    return pop(t, a - 0.2, dur)


def title(g, t, a, txt, col=INK, size=84, y=380):
    g.label(txt, CX, y, size, color=col, sc=ap(t, a), rot=-3)


def dinner(g, t, glow=1.0, park_mood="smile", kim_mood="neutral", cha_mood="neutral", talk=None, empty=()):
    """โต๊ะดินเนอร์: พัก (กลาง) คิม (ซ้าย) ชา (ขวา)"""
    seats = ((200, KIM, kim_mood, 0.4), (CX, PARK, park_mood, 0.0), (880, CHA, cha_mood, -0.4))
    for i, (x, lk, md, tr) in enumerate(seats):
        if i in empty:
            continue
        person(g, x, GROUND - 60, lk, 0.62, mood=md, pose="down", turn=tr, seed=10 + i, talk=talk == i, legs=False)
    table(g, CX, GROUND - 40, 900, t)


# ------------------------------------------------------------------ 1. hook
def s_hook(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:
        house(g, CX, GROUND, 1.0, t)
        night(g, 0.6)
        house(g, CX, GROUND, 1.0, t)
        g.label("วันนี้ในอดีต", CX, 380, 104, sc=lerp(2.0, 1, e_out(seg(t, 0.1, 0.4))) if t > 0.1 else 0, rot=-3)
        g.label("26 ตุลาคม 1979", CX, 520, 84, color=GOLDTXT, sc=pop(t, 0.6))
        return
    if t < L[3] - 0.2:   # เสียงปืนกลางเซฟเฮาส์ ผู้นำเผด็จการ
        night(g, 0.85, 0.6, CX, 900)
        table(g, CX, GROUND - 40, 900, t, spill=1.0 if t > L[1] + 0.6 else 0.0)
        flash(g, 300, 760, 180, (t * 1.3) % 1 if t > L[1] + 0.3 else 0)
        chair(g, 860, GROUND, 0.9, -50 * e_out(seg(t, L[1] + 0.5, L[1] + 0.9)))
        if t < L[2] - 0.2:
            title(g, t, L[1], "เสียงปืนลั่นโต๊ะอาหารค่ำ!", RED, 84)
        else:
            title(g, t, L[2], "ผู้นำเผด็จการถูกสังหาร", LIGHT, 84)
        return
    if t < L[4] - 0.2:   # ไม่ใช่เกาหลีเหนือ
        with g.at(CX, 820, ap(t, L[3])):
            g.rrect(-300, -200, 600, 400, 30, WHITE, 8, stroke=GREY)
            g.label("เกาหลีเหนือ?", 0, 0, 80, color=GREY)
            g.line([(-260, -170), (260, 170)], 16, RED, amp=0)
        title(g, t, L[3], "ไม่ใช่ศัตรูจากเกาหลีเหนือ", DARK, 82)
        return
    person(g, 280, GROUND, PARK, 0.82, mood="smile", pose="down", turn=0.4, seed=1)   # แต่เป็นเพื่อนสนิท
    person(g, 800, GROUND, KIM, 0.85, mood="firm", pose="down", turn=-0.4, seed=2)
    g.label("?!", CX + 20, 700, 120, color=RED, sc=ap(t, L[4] + 0.4))
    title(g, t, L[4], "แต่เป็นเพื่อนสนิทคู่ใจ!", RED, 86)


# ------------------------------------------------------------------ 2. dinner
def s_dinner(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # คืน 26 ต.ค. 1979 เซฟเฮาส์ โซล
        night(g, 0.7)
        house(g, CX, GROUND, 1.0, t)
        if t < L[1] - 0.2:
            title(g, t, L[0], "ค่ำคืน 26 ตุลาคม 1979", GOLDTXT, 86)
        else:
            title(g, t, L[1], "เซฟเฮาส์ลับ กรุงโซล", LIGHT, 86)
        return
    if t < L[4] - 0.2:   # พัก จ็อง-ฮี 18 ปี
        person(g, 300, GROUND, PARK, 0.85, mood="firm", pose="down", turn=0.3, seed=1)
        g.name_tag(t, L[2] + 0.1, 300, 1150, "พัก จ็อง-ฮี", "ประธานาธิบดีเกาหลีใต้ (1963–1979)")
        taegeuk(g, 760, 760, 120 * ap(t, L[2] + 0.4) + 1, t)
        if t < L[3] - 0.2:
            title(g, t, L[2], "ประธานาธิบดีพัก จ็อง-ฮี", KBLUE, 84)
        else:
            g.label("18 ปี", 760, 1000, 110, color=RED, sc=ap(t, L[3]))
            title(g, t, L[3], "กุมอำนาจเบ็ดเสร็จ 18 ปี", RED, 82)
        return
    if t < L[7] - 0.2:   # ดินเนอร์ส่วนตัว ดื่ม ฟังดนตรี
        night(g, 0.6, 1.0, CX, 820)
        dinner(g, t, park_mood="smile", kim_mood="neutral", cha_mood="smug")
        if t > L[5] - 0.2:
            for i in range(3):
                u = (t * 0.6 + i / 3) % 1
                g.label("~", 300 + i * 240, 620 - 160 * u, 70, color=(1, 0.9, 0.6, 1 - u))
        title(g, t, L[4] if t < L[5] - 0.2 else (L[5] if t < L[6] - 0.2 else L[6]),
              "ดินเนอร์ส่วนตัว" if t < L[5] - 0.2 else ("ดื่มสุรา ฟังดนตรี" if t < L[6] - 0.2 else "แขกเพียงไม่กี่คน"),
              GOLD2, 88)
        return
    if t < L[9] - 0.2:   # คิม แจ-กยู ผอ. KCIA
        person(g, 300, GROUND, KIM, 0.85, mood="neutral", pose="down", turn=0.3, seed=2)
        g.name_tag(t, L[7] + 0.1, 300, 1150, "คิม แจ-กยู", "ผู้อำนวยการ KCIA")
        if t > L[8] - 0.2:
            with g.at(760, 760, ap(t, L[8]), 4):
                g.rrect(-180, -110, 360, 220, 20, hexc("#2b2f3a"), 7)
                g.label("KCIA", 0, -20, 90, color=WHITE)
                g.label("หน่วยข่าวกรองกลาง", 0, 60, 36, color=WHITE)
        title(g, t, L[7] if t < L[8] - 0.2 else L[8], "หนึ่งในนั้นคือ คิม แจ-กยู" if t < L[8] - 0.2
              else "ผู้อำนวยการ KCIA", NAVY, 82)
        return
    person(g, 300, GROUND, PARK, 0.75, mood="smile", pose="down", turn=0.4, seed=1)   # เพื่อนตายสมัยทหาร
    person(g, 780, GROUND, KIM, 0.75, mood="smile", pose="down", turn=-0.4, seed=2)
    with g.at(CX + 20, 620, ap(t, L[9])):
        g.rrect(-200, -60, 400, 120, 30, WHITE, 7, stroke=GOLDTXT)
        g.label("เพื่อนร่วมรุ่นทหาร", 0, 0, 46, color=GOLDTXT)
    title(g, t, L[9], "เพื่อนตายตั้งแต่สมัยทหาร", GOLDTXT, 84)


# ------------------------------------------------------------------ 3. tension
def s_tension(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # เบื้องหลังแก้วเหล้า ตึงเครียด
        night(g, 0.6, 1.0, CX, 820)
        dinner(g, t, park_mood="neutral", kim_mood="worry", cha_mood="angry")
        if t > L[1] - 0.2:
            for x in (200, 880):
                g.sweat(x + 30, 560 + 10 * math.sin(t * 6), 1.3)
        title(g, t, L[0] if t < L[1] - 0.2 else L[1], "เบื้องหลังแก้วเหล้า..." if t < L[1] - 0.2
              else "ตึงเครียดจนแทบระเบิด!", LIGHT if t < L[1] - 0.2 else RED, 86)
        return
    if t < L[4] - 0.2:   # ประท้วงหลายหมื่นคน
        for i in range(3):
            person(g, 200 + i * 340, GROUND, PROTESTERS[i], 0.62, mood="shout", pose="fist", turn=0.2 - 0.2 * i,
                   seed=30 + i, talk=True)
            placard(g, 330 + i * 340, GROUND - 200, 0.7, -6 + 6 * i)
        title(g, t, L[2] if t < L[3] - 0.2 else L[3], "เกาหลีใต้ลุกเป็นไฟ!" if t < L[3] - 0.2
              else "ประท้วงเรียกร้องประชาธิปไตย", RED, 82)
        return
    if t < L[7] - 0.2:   # ชา จี-ชอล ด่าคิม
        person(g, 280, GROUND, CHA, 0.85, mood="shout", pose="point", turn=0.4, seed=12, talk=True)
        if t < L[5] - 0.2:
            g.name_tag(t, L[4] + 0.1, 680, 1150, "ชา จี-ชอล", "หัวหน้าหน่วยอารักขาประธานาธิบดี")
            title(g, t, L[4], "ชา จี-ชอล หัวหน้าหน่วยอารักขา", DARK, 76)
        else:
            person(g, 900, GROUND, KIM, 0.75, mood="angry", pose="down", turn=-0.4, seed=2)
            with g.at(620, 600, ap(t, L[5] + 0.2), -5):
                g.bubble(0, 0, 340, 140, WHITE, tail=(-1, 1))
                g.label("ไร้น้ำยา!", 0, 0, 64, color=RED)
            title(g, t, L[5], "ด่าทอคิม แจ-กยูกลางโต๊ะ", RED, 80)
        return
    tank(g, lerp(1300, 700, e_io(seg(t, L[7], L[7] + 2.0))) + 12 * math.sin(t * 3), GROUND - 6 * abs(math.sin(t * 9)), 1.0, True, t)   # ยุให้ใช้รถถัง
    person(g, 230, GROUND, CHA, 0.8, mood="smug", pose="point", turn=0.4, seed=12, talk=True)
    if t < L[8] - 0.2:
        title(g, t, L[7], "ยุให้ใช้ทหารและรถถังบดขยี้!", RED, 78)
    else:
        g.label("แม้ต้องสังหารนับล้าน!", 680, 640, 64, color=RED, sc=ap(t, L[8]), rot=-4)
        title(g, t, L[8], "ไร้ความปรานี", DARK, 92)


# ------------------------------------------------------------------ 4. shots
def s_shots(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # พักเข้าข้างชา -> สั่งนองเลือด
        person(g, 300, GROUND, PARK, 0.8, mood="smug", pose="point", turn=0.4, seed=1, talk=True)
        person(g, 800, GROUND, CHA, 0.8, mood="smug", pose="cross", turn=-0.4, seed=12)
        title(g, t, L[0] if t < L[1] - 0.2 else L[1], "พักเข้าข้างหัวหน้าอารักขา" if t < L[1] - 0.2
              else "พร้อมสั่งนองเลือดประชาชน", RED, 78)
        return
    if t < L[3] - 0.2:   # คิมเดินออกไปหยิบปืน
        u = e_io(seg(t, L[2], L[3] - 0.5))
        g.rrect(820, 500, 260, GROUND - 500, 6, hexc("#7a5a3a"), 7)
        person(g, lerp(300, 900, u), GROUND, KIM, 0.75, mood="angry", pose="down", turn=0.9, seed=2)
        title(g, t, L[2], "เดินออกไปหยิบปืนพก...", DARK, 82)
        return
    if t < L[6] - 0.2:   # กลับมา จ้องหน้า ตะโกน
        with g.at(CX, 860, 1.7, 2 * math.sin(t * 9) * (t > L[4])):
            head(g, KIM, "shout" if t > L[4] - 0.2 else "angry", 1 if t > L[5] - 0.2 else 0, 0)
        if t > L[5] - 0.2:
            with g.at(CX, 520, ap(t, L[5]), -6):
                g.bubble(0, 0, 520, 150, WHITE, tail=(0, 1))
                g.label("แกมันเศษสวะ!", 0, 0, 72, color=RED)
        title(g, t, L[3] if t < L[4] - 0.2 else L[4], "กลับเข้ามา จ้องหน้าพัก" if t < L[4] - 0.2
              else "หันไปตะโกนใส่ชา จี-ชอล", RED, 80, y=330)
        return
    # ความมืด + แสงวาบ (ไม่แสดงการยิงโดน)
    night(g, 0.9, 0.4, CX, 900)
    table(g, CX, GROUND - 40, 900, t, spill=1.0)
    if t < L[7] - 0.2:
        chair(g, 860, GROUND, 0.9, -70 * e_out(seg(t, L[6] + 0.3, L[6] + 0.7)))
        flash(g, 300, 720, 200, seg(t, L[6] + 0.1, L[6] + 0.6))
        title(g, t, L[6], "เสียงปืนนัดแรกดังขึ้น!", RED, 84)
        return
    chair(g, 860, GROUND, 0.9, -70)
    if t < L[9] - 0.2:
        chair(g, CX, GROUND, 0.9, -60 * e_out(seg(t, L[8], L[8] + 0.4)))
        flash(g, 320, 700, 200, seg(t, L[8] - 0.1, L[8] + 0.4))
        title(g, t, L[7] if t < L[8] - 0.2 else L[8], "หันปืนไปที่ประธานาธิบดี" if t < L[8] - 0.2
              else "เหนี่ยวไกระยะเผาขน!", RED, 80)
        return
    if t < L[10] - 0.2:   # ปืนขัด
        pistol(g, CX, 800, 1.8, -6 + 4 * math.sin(t * 8), ap(t, L[9] + 0.3))
        title(g, t, L[9], "ปืนขัดลำกล้อง!", LIGHT, 92)
        return
    if t < L[11] - 0.2:   # เปลี่ยนปืน ยิงซ้ำ
        u = seg(t, L[10], L[11])
        flash(g, 320, 700, 220, seg(t, L[10] + 1.6, L[10] + 2.2))
        g.label("ปัง!", 760, 640, 100, color=(1, 0.85, 0.4, 1), sc=ap(t, L[10] + 1.7), rot=-8)
        title(g, t, L[10], "เปลี่ยนปืนแล้วกลับมายิงซ้ำ", LIGHT, 80)
        return
    candle(g, 300, GROUND - 20, 1.0, t)   # ปิดฉาก 62 ปี
    candle(g, 780, GROUND - 20, 1.0, t + 1)
    with g.at(CX + 20, 760, ap(t, L[11])):
        g.rrect(-170, -220, 340, 440, 10, hexc("#2b2622"), 8)
        g.rrect(-140, -190, 280, 330, 6, hexc("#e8e0cc"), 4)
        g.label("พัก จ็อง-ฮี", 0, -30, 46)
        g.label("1917–1979", 0, 40, 40, color=GREY)
        g.label("62 ปี", 0, 175, 44, color=WHITE)
    title(g, t, L[11], "ปิดฉากผู้นำเผด็จการ", LIGHT, 86)


# ------------------------------------------------------------------ 5. after
def s_after(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[3] - 0.2:   # ศาล: อ้างกอบกู้ประชาธิปไตย / ประหาร
        person(g, 300, GROUND, KIM, 0.82, mood="firm" if t < L[3] else "sad", pose="down", turn=0.4, seed=2,
               talk=L[1] - 0.2 < t < L[3] - 0.2)
        gavel(g, 780, 760, 1.1 * ap(t, L[0]) + 0.01, lerp(-30, 10, e_io(seg(t, L[0] + 0.4, L[0] + 0.7))))
        if t < L[1] - 0.2:
            title(g, t, L[0], "การลอบสังหารสะเทือนโลก", RED, 82)
        else:
            with g.at(700, 560, ap(t, L[1]), -4):
                g.bubble(0, 0, 420, 140, WHITE, tail=(-1, 1))
                g.label("กอบกู้ประชาธิปไตย!", 0, 0, 50, color=KBLUE)
            title(g, t, L[1] if t < L[2] - 0.2 else L[2], "คิมอ้างในชั้นศาล" if t < L[2] - 0.2
                  else "หยุดเพื่อนรักไม่ให้ฆ่าประชาชน", NAVY, 76, y=360)
        return
    if t < L[4] - 0.2:   # ถูกประหาร
        gavel(g, CX, 820, 1.4, 10)
        with g.at(CX, 1070, ap(t, L[3]), -4):
            g.rrect(-260, -60, 520, 120, 20, WHITE, 8, stroke=RED)
            g.label("โทษประหารชีวิต", 0, 0, 56, color=RED)
        title(g, t, L[3], "ถูกตัดสินประหารชีวิต", DARK, 86)
        return
    if t < L[5] - 0.2:   # ไม่ได้ประชาธิปไตยทันที
        taegeuk(g, CX, 820, 170, t)
        g.label("ประชาธิปไตย?", CX, 1080, 70, color=GREY, sc=ap(t, L[4] + 0.3))
        title(g, t, L[4], "ประชาธิปไตยยังไม่มาทันที", DARK, 80)
        return
    if t < L[6] - 0.2:   # ชอน ดู-ฮวาน รัฐประหาร
        person(g, 300, GROUND, CHUN, 0.85, mood="smug", pose="cross", turn=0.3, seed=40)
        g.name_tag(t, L[5] + 0.1, 300, 1150, "ชอน ดู-ฮวาน", "นายพลผู้ก่อรัฐประหาร (12 ธ.ค. 1979)")
        tank(g, 820, GROUND, 0.7, True, t)
        title(g, t, L[5], "ชอน ดู-ฮวานยึดอำนาจ", RED, 84)
        return
    for i in range(5):   # โศกนาฏกรรมกวางจู (เทียนไว้อาลัย)
        candle(g, 160 + i * 190, GROUND - 20 * (i % 2), 0.8, t + i)
    with g.at(CX, 640, ap(t, L[6]), -3):
        g.rrect(-260, -70, 520, 140, 30, WHITE, 8, stroke=DARK)
        g.label("กวางจู · พ.ค. 1980", 0, 0, 56, color=DARK)
    title(g, t, L[6], "โศกนาฏกรรมนองเลือดที่กวางจู", DARK, 76)


# ------------------------------------------------------------------ 6. lesson
def s_lesson(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:
        person(g, CX, GROUND, PARK, 0.85, mood="firm", pose="cross", turn=0, seed=1)
        with g.at(CX, 470, ap(t, L[1])):
            g.rrect(-280, -60, 560, 120, 30, WHITE, 7, stroke=RED)
            g.label("อำนาจไร้การตรวจสอบ", 0, 0, 52, color=RED)
        title(g, t, L[0], "คืนนั้นเตือนใจเราว่า...", INK, 84, y=330)
        return
    person(g, 260, GROUND, PARK, 0.75, mood="neutral", pose="down", turn=0.4, seed=1)
    if t < L[3] - 0.2:   # ศัตรูไกลตัว
        tank(g, 900, GROUND - 300, 0.35, True, t)
        g.label("ศัตรูไกลตัว", 900, 760, 56, color=GREY, sc=ap(t, L[2]))
        title(g, t, L[2], "ไม่ได้มาจากศัตรูไกลตัว", GREY, 82)
    else:
        person(g, 560, GROUND, KIM, 0.75, mood="angry", pose="down", turn=-0.4, seed=2)
        g.label("คนใกล้ชิด", 560, 560, 60, color=RED, sc=ap(t, L[3] + 0.3), rot=-6)
        title(g, t, L[3], "แต่มาจากคนใกล้ตัวที่สุด", RED, 82)


# ------------------------------------------------------------------ 7. outro
def s_outro(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:
        person(g, 300, GROUND, KIM, 0.85, mood="firm", pose="down", turn=0.3, seed=2)
        with g.at(760, 640, ap(t, L[0])):
            g.bubble(0, 0, 360, 240, WHITE, tail=(-1, 1))
            g.label("?", 0, 0, 140, color=KBLUE)
        title(g, t, L[0], "มองคิม แจ-กยูอย่างไร?", INK, 86)
        return
    if t < L[3] - 0.2:   # วีรบุรุษ vs คนทรยศ
        for i, (txt, sub, col) in enumerate((("วีรบุรุษ", "หยุดยั้งเผด็จการ", KBLUE),
                                             ("คนทรยศ", "ฆาตกรรมเพื่อนรัก", RED))):
            k = ap(t, L[1] if i == 0 else L[2])
            if k < 0.02:
                continue
            with g.at(CX + 10 * math.sin(t * 2 + i * 2), 620 + i * 300, k, -3 + 6 * i + 2 * math.sin(t * 1.7 + i)):
                g.rrect(-300, -100, 600, 200, 40, WHITE, 8, stroke=col)
                g.label(txt, 0, -20, 72, color=col)
                g.label(sub, 0, 50, 40, color=GREY)
        g.label("หรือ", CX, 775, 56, sc=ap(t, L[2]))
        title(g, t, L[1], "คุณมองแบบไหน?", NAVY, 88, y=360)
        return
    with g.at(CX + 170, 640, ap(t, L[3])):   # ชวนคอมเมนต์
        g.bubble(0, 0, 460, 220, WHITE, tail=(-1, 1))
        for i in range(3):
            g.circle(-110 + i * 110, 0, 24 + 6 * math.sin(t * 6 - i), INK, 0)
    person(g, 250, GROUND, PROTESTERS[0], 0.8, mood="smile", pose="wave", turn=0.3, seed=70, talk=True)
    title(g, t, L[3], "คอมเมนต์แลกเปลี่ยนกันได้เลย!", RED, 64)


SCENES = {
    "hook": s_hook, "dinner": s_dinner, "tension": s_tension, "shots": s_shots, "after": s_after,
    "lesson": s_lesson, "outro": s_outro,
}
NO_IRIS = set()
