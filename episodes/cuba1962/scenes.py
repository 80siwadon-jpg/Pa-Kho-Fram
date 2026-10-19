"""ฉากตอน: วิกฤตขีปนาวุธคิวบา (22 ต.ค. 1962) — ไม่แสดงภาพนิวเคลียร์ทำลายล้าง ใช้สัญลักษณ์แทน"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from chars import (ADVISORS, FAMILY, JFK, KHRUSHCHEV, SOV_RED, US_BLUE, caribbean_map, cans, cargo_ship,  # noqa: E402
                   clock_face, dove, jet, missile, red_phone, sea, shelter_sign, thread, time_bomb, tv, warship)
from gfx import (GOLD, GOLD2, GREY, INK, LGREY, NAVY, RED, W, WHITE, e_io, e_out, hexc, lerp, pop,  # noqa: E402
                 seg)
from people import _rr, _shade, head, person  # noqa: E402
from photos import photo  # noqa: E402

CX = W / 2
GROUND = 1270
GOLDTXT = hexc("#b37a12")
GREEN = hexc("#3c8d4f")
SEA_Y = 1000

CAMERA = {"hook": "push_in", "coldwar": "pan_right", "blockade": "pan_left", "days": "dutch", "deal": "push_in",
          "lesson": "pull_out", "outro": "push_in"}
TRANSITIONS = {"coldwar": "fade", "blockade": "whip", "days": "zoom", "deal": "iris", "lesson": "fade"}


def ap(t, a, dur=0.38):
    return pop(t, a - 0.2, dur)


def alert(g, t, a=1.0):
    """ไฟเตือนสีแดงกะพริบรอบขอบ"""
    k = (0.5 + 0.5 * math.sin(t * 6)) * a
    g.c.rectangle(-400, 250, W + 800, 30)
    g.c.rectangle(-400, 1250, W + 800, 30)
    g.c.set_source_rgba(0.85, 0.2, 0.2, 0.5 * k)
    g.c.fill()


# ------------------------------------------------------------------ 1. hook
def s_hook(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:
        clock_face(g, CX, 820, 220, lerp(10, 3, e_io(seg(t, 0.4, L[1]))))
        g.label("วันนี้ในอดีต", CX, 380, 104, sc=lerp(2.0, 1, e_out(seg(t, 0.1, 0.4))) if t > 0.1 else 0, rot=-4)
        g.label("22 ตุลาคม 1962", CX, 520, 84, color=RED, sc=pop(t, 0.8))
        return
    if t < L[2] - 0.2:   # ขอบเหวแห่งความตาย
        alert(g, t)
        time_bomb(g, CX, 820, 1.4 * ap(t, L[1]), t, 1 - seg(t, L[1], L[2]) * 0.6)
        g.label("ขอบเหวแห่งความตาย!", CX, 380, 84, color=RED, sc=ap(t, L[1]), rot=-3)
        return
    if t < L[5] - 0.2:   # เคนเนดีออกทีวี
        for i, lk in enumerate(FAMILY):
            person(g, 150 + i * 120, GROUND, lk, 0.5 if i < 2 else 0.6, mood="worry", turn=0.5, seed=10 + i, shadow=False)
        tv(g, 700, 900, 1.05, t, True, JFK)
        g.name_tag(t, L[2] + 0.4, 700, 470, "จอห์น เอฟ. เคนเนดี", "ประธานาธิบดีสหรัฐฯ คนที่ 35", side=1)
        if t > L[3] - 0.2:
            g.label("ใบหน้าเคร่งเครียด", 700, 1200, 56, color=NAVY, sc=ap(t, L[3]))
        if t > L[4] - 0.2:
            g.label("ข่าวด่วนที่สุดในประวัติศาสตร์", CX, 360, 64, color=RED, sc=ap(t, L[4]), rot=-3)
        return
    # ขีปนาวุธโซเวียตบนเกาะคิวบา ห่างแค่เอื้อม
    mk = ap(t, L[5] + 0.3)
    rk = e_out(seg(t, L[7] - 0.2, L[7] + 1.4))
    caribbean_map(g, CX, 800, 0.95, t, missiles=mk, range_k=rk)
    if t < L[6] - 0.2:
        g.label("ฐานขีปนาวุธนิวเคลียร์!", CX, 330, 74, color=RED, sc=ap(t, L[5]), rot=-3)
    elif t < L[7] - 0.2:
        g.label("แอบติดตั้งบนเกาะคิวบา", CX, 330, 70, color=SOV_RED, sc=ap(t, L[6]), rot=-3)
    else:
        g.label("แค่เอื้อมมือ!", CX, 330, 90, color=RED, sc=ap(t, L[7]), rot=-4)


# ------------------------------------------------------------------ 2. coldwar
def s_coldwar(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # สงครามเย็น สองมหาอำนาจ
        tug = 30 * math.sin(t * 1.5)
        person(g, 240 + tug, GROUND, JFK, 0.82, mood="firm", pose="point", turn=0.4, seed=1)
        person(g, 840 + tug, GROUND, KHRUSHCHEV, 0.82, mood="angry", pose="fist", turn=-0.4, seed=2)
        g.name_tag(t, 0.6, 840, 470, "นิกิตา ครุสชอฟ", "ผู้นำสหภาพโซเวียต", side=-1)
        if t < L[1] - 0.2:
            g.label("สงครามเย็น", CX, 360, 96, color=NAVY, sc=ap(t, 0.2), rot=-3)
        else:
            g.label("ตึงเครียดถึงขีดสุด!", CX, 360, 84, color=RED, sc=ap(t, L[1]), rot=-3)
        return
    if t < L[4] - 0.2:   # แอบซ่อนอาวุธหน้าบ้านศัตรู
        g.c.save()
        for i in range(3):
            g.poly([(80 + i * 120, GROUND), (140 + i * 120, GROUND - 140), (200 + i * 120, GROUND)], hexc("#6b8f3a"), 6)
        g.c.restore()
        missile(g, 620, GROUND - 40, 1.1 * ap(t, L[2] + 0.3), -12 * e_io(seg(t, L[2] + 1.0, L[4] - 0.4)))
        for i in range(3):   # ไฟฉายสอดส่องในความมืด
            ax = 620 + 260 * math.sin(t * 1.3 + i * 2.1)
            g.circle(ax, 760 + 60 * i, 50, (1, 0.95, 0.6, 0.25), 0)
        with g.alpha(0.6 + 0.4 * math.sin(t * 3)):
            g.label("ชู่ว์...", 330, 900, 70, color=GREY, sc=ap(t, L[2] + 0.8), rot=-8)
        if t < L[3] - 0.2:
            g.label("อาวุธมหาประลัย", CX, 360, 84, color=SOV_RED, sc=ap(t, L[2]), rot=-3)
        else:
            g.label("ไม่มีใครทันตั้งตัว!", CX, 360, 80, color=RED, sc=ap(t, L[3]), rot=-3)
        return
    alert(g, t)   # ระเบิดเวลา
    time_bomb(g, CX, 820, 1.6, t, 1 - seg(t, L[4], L[4] + 4.0) * 0.8)
    g.label("ระเบิดเวลา!", CX, 360, 96, color=RED, sc=ap(t, L[4]), rot=-4)


# ------------------------------------------------------------------ 3. blockade
def s_blockade(g, t, L, d):
    if t < L[1] - 0.2:   # ไม่มีทางเลือก
        g.ground(GROUND, WHITE)
        person(g, CX, GROUND, JFK, 0.9, mood="worry", pose="think", turn=0.1, seed=1)
        g.label("ไม่มีทางเลือกอื่น", CX, 360, 84, sc=ap(t, 0.2), rot=-3)
        return
    if t < L[2] - 0.2:   # ปิดล้อมทางเรือ
        g.ground(GROUND, WHITE)
        caribbean_map(g, CX, 800, 0.95, t, missiles=1.0, ring=e_io(seg(t, L[1] + 0.2, L[2] - 0.4)),
                      ships=seg(t, L[1] + 1.0, L[2] - 0.4))
        g.label('"ปิดล้อมทางเรือ"', CX, 330, 90, color=US_BLUE, sc=ap(t, L[1]), rot=-3)
        return
    sea(g, SEA_Y, t)
    g.ground(GROUND, WHITE)
    if t < L[3] - 0.2:   # กองเรือรบ + เครื่องบินรบ
        warship(g, 300, SEA_Y + 90, 0.8 * ap(t, L[2]), t)
        warship(g, 800, SEA_Y + 150, 0.6 * ap(t, L[2] + 0.4), t)
        for i in range(3):
            jet(g, lerp(-200, 1300, ((t - L[2]) * 0.25 + i / 3) % 1), 520 + i * 90, 0.6, 0)
        g.label("กองเรือรบ + เครื่องบินรบ", CX, 360, 72, color=US_BLUE, sc=ap(t, L[2]), rot=-3)
        return
    # เส้นกั้น: เรือโซเวียตเข้าใกล้ — ห้ามข้าม
    k = e_io(seg(t, L[3], L[5] + 2.0))
    g.line([(CX, 500), (CX, SEA_Y + 260)], 12, US_BLUE, amp=0)
    cargo_ship(g, lerp(1250, 760, k), SEA_Y + 120, 0.65, t, flip=True)
    warship(g, 250, SEA_Y + 120, 0.7, t)
    if t < L[4] - 0.2:
        g.label("ห้ามฝ่าฝืนเส้นกั้น!", CX, 380, 80, color=RED, sc=ap(t, L[3]), rot=-3)
    elif t < L[5] - 0.2:
        alert(g, t)
        g.label("พร้อมเปิดฉากยิง!", CX, 380, 84, color=RED, sc=ap(t, L[4]), rot=-4)
    else:
        alert(g, t)
        g.label("= สงครามนิวเคลียร์", CX, 380, 80, color=RED, sc=ap(t, L[5]), rot=-3)
        g.label("ไม่มีใครรอด!", CX, 500, 70, color=INK, sc=ap(t, L[5] + 0.6))


# ------------------------------------------------------------------ 4. days
def s_days(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # 13 วัน เส้นด้ายตึง
        day = min(13, 1 + int(seg(t, 0.2, L[2] - 0.4) * 13))
        g.calendar(CX, 700, 1.2, str(day), "วันที่", "ต.ค. 1962")
        thread(g, 140, 940, 1100, 1.0, t)
        g.label("13 วันเต็ม", CX, 360, 96, color=RED, sc=ap(t, 0.2), rot=-3)
        if t > L[1] - 0.2:
            g.label("ตึงจนแทบขาด", CX, 1180, 58, color=NAVY, sc=ap(t, L[1]))
        return
    if t < L[3] - 0.2:   # กักตุนอาหาร ขุดหลุมหลบภัย
        cans(g, 760, GROUND, 6, 1.1 * ap(t, L[2]))
        shelter_sign(g, 760, 600, 0.9 * ap(t, L[2] + 0.8))
        for i, lk in enumerate(FAMILY):
            person(g, 150 + i * 150, GROUND, lk, 0.6 if i < 2 else 0.7, mood="worry", pose="hold" if i == 0 else "down",
                   turn=0.3, seed=20 + i)
        g.label("กักตุน · ขุดหลุมหลบภัย", CX, 360, 70, sc=ap(t, L[2]), rot=-3)
        return
    alert(g, t)   # รอจุดจบ
    clock_face(g, CX, 800, 240, lerp(3, 0.5, seg(t, L[3], L[3] + 3.0)))
    g.label("อีกไม่กี่นาที...?", CX, 360, 84, color=RED, sc=ap(t, L[3]), rot=-3)


# ------------------------------------------------------------------ 5. deal
def s_deal(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[3] - 0.2:   # เบื้องหลังฉาก: เกมการทูต
        person(g, 200, GROUND, JFK, 0.75, mood="firm", pose="phone", turn=0.4, seed=1, talk=(int(t * 1.5) % 2) == 0)
        person(g, 880, GROUND, KHRUSHCHEV, 0.75, mood="firm", pose="phone", turn=-0.4, seed=2, talk=(int(t * 1.5) % 2) == 1)
        red_phone(g, CX, 960, 0.9, ring=1.0 if t < L[1] else 0.0, t=t)
        for i in range(4):   # ข้อความวิ่งระหว่างกัน
            u = ((t * 0.4 + i / 4) % 1)
            x = lerp(330, 750, u if i % 2 == 0 else 1 - u)
            g.rrect(x - 30, 600 - 20, 60, 40, 6, WHITE, 4)
        if t < L[1] - 0.2:
            g.label("เบื้องหลังฉาก...", CX, 360, 84, sc=ap(t, 0.2), rot=-3)
        elif t < L[2] - 0.2:
            g.label("เกมการทูต", CX, 360, 96, color=NAVY, sc=ap(t, L[1]), rot=-3)
        else:
            g.label("เดิมพันร้อยล้านชีวิต", CX, 360, 78, color=RED, sc=ap(t, L[2]), rot=-3)
        return
    if t < L[5] - 0.2:   # ถอยคนละก้าว ปลดชนวน
        k = e_io(seg(t, L[3] + 0.3, L[3] + 2.0))
        person(g, lerp(380, 220, k), GROUND, JFK, 0.75, mood="neutral", turn=0.3, seed=1)
        person(g, lerp(700, 860, k), GROUND, KHRUSHCHEV, 0.75, mood="neutral", turn=-0.3, seed=2)
        fuse = 0.3 if t < L[4] else 0.0
        with g.at(CX, 740):
            time_bomb(g, 0, 0, 0.8, t, fuse)
            if t > L[4] - 0.2:
                g.line([(-30, -150), (40, -220)], 10, GREEN, amp=0)
        if t < L[4] - 0.2:
            g.label("ถอยคนละก้าว", CX, 360, 90, color=NAVY, sc=ap(t, L[3]), rot=-3)
        else:
            g.label("ปลดชนวนวินาทีสุดท้าย!", CX, 360, 76, color=GREEN, sc=ap(t, L[4]), rot=-3)
        return
    k = ap(t, L[5])   # โลกรอด
    g.sunburst(CX, 800, 220, 600, 22, t * 10, 12, (0.85, 0.95, 0.85, 0.7))
    with g.at(CX, 800):
        g.c.new_path()
        g.c.arc(0, 0, 200 * k, 0, 2 * math.pi)
        _shade(g.c, hexc("#8fb8de"), 6, 0.3)
    dove(g, CX + 40, 520, 1.8 * k, t)
    g.label("โลกรอดอย่างฉิวเฉียด!", CX, 360, 80, color=GREEN, sc=k, rot=-3)


# ------------------------------------------------------------------ 6. lesson
def s_lesson(g, t, L, d):
    g.ground(GROUND, WHITE)
    g.label("บทเรียน", CX, 340, 100, sc=ap(t, 0.2), rot=-3)
    if t < L[2] - 0.2:
        thread(g, 160, 920, 820, 1.0, t)
        if t > L[1] - 0.2:
            g.label("ความขัดแย้งเกือบทำลายทุกสิ่ง", CX, 1150, 58, color=RED, sc=ap(t, L[1]))
        return
    bal = 6 * math.sin(t * 1.5) * (1 - seg(t, L[2], L[3] + 1.0))   # ความอดกลั้น + สติปัญญา ค้ำสันติภาพ
    with g.at(CX, 780, 1, bal):
        g.line([(-320, 0), (320, 0)], 12, INK, amp=0)
        g.label("อดกลั้น", -230, -70, 54, color=NAVY, sc=ap(t, L[2]))
        g.label("สติปัญญา", 220, -70, 54, color=NAVY, sc=ap(t, L[2] + 0.4))
    g.poly([(CX - 40, 1180), (CX, 790), (CX + 40, 1180)], hexc("#a8763e"), 6)
    if t > L[3] - 0.2:
        dove(g, CX, 590, 1.4 * ap(t, L[3]), t)
        g.label("ค้ำจุนสันติภาพ", CX, 1180, 64, color=GREEN, sc=ap(t, L[3] + 0.3))


# ------------------------------------------------------------------ 7. outro
def s_outro(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[5] - 0.2:   # ถ้าคุณเป็นผู้นำ: กำลัง vs เจรจา
        if t < L[3] - 0.2:
            caribbean_map(g, CX, 800, 0.85, t, missiles=1.0, range_k=0.6)
            g.label("ถ้าคุณเป็นผู้นำ...", CX, 330, 84, sc=ap(t, L[1]), rot=-3)
            return
        for i, (txt, col, x) in enumerate((("ใช้กำลัง", RED, 270), ("เจรจา", GREEN, 810))):
            k = ap(t, L[3] + i * (L[4] - L[3]))
            with g.at(x, 780, k * (1 + 0.04 * math.sin(t * 3 + i))):
                g.rrect(-200, -240, 400, 480, 40, WHITE, 7)
                if i == 0:
                    jet(g, 0, -40, 0.7, -20)
                else:
                    red_phone(g, 0, 0, 0.9)
                g.label(txt, 0, 160, 66, color=col)
        g.label("หรือ", CX, 780, 60, color=GREY, sc=ap(t, L[4]))
        g.label("คุณจะเลือกทางไหน?", CX, 330, 78, sc=ap(t, L[3]), rot=-3)
        return
    with g.at(CX + 120, 650, ap(t, L[5])):   # ชวนคอมเมนต์
        g.bubble(0, 0, 520, 240, WHITE, tail=(-1, 1))
        for i in range(3):
            g.circle(-110 + i * 110, 0, 24 + 6 * math.sin(t * 6 - i), INK, 0)
    person(g, 250, GROUND, JFK, 0.75, mood="smile", pose="wave", turn=0.3, seed=1, talk=True)
    dove(g, 760, 1130, 1.0, t)
    g.label("คอมเมนต์คุยกันได้เลย!", 700, 960, 58, color=RED, sc=ap(t, L[5] + 0.4))


SCENES = {
    "hook": s_hook, "coldwar": s_coldwar, "blockade": s_blockade, "days": s_days, "deal": s_deal,
    "lesson": s_lesson, "outro": s_outro,
}
NO_IRIS = set()
