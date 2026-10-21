"""ฉากตอน: วันเสาร์ทมิฬ 27 ต.ค. 1962 — วาซิลี อาร์คีปอฟ ไม่ยอมยิงตอร์ปิโดนิวเคลียร์"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from chars import (ARKHIPOV, CREW, GENERALS, JFK, KHRUSHCHEV, POLIT, SAVITSKY, battery, calendar, clock_face,  # noqa: E402
                   cuba, depth_charge, dove, fire_button, gauge, globe, helmet, no_sign, radar, radio, ribbon,
                   shock_ring, smoke_trail, sub_room, submarine, sweat, thermometer, torpedo, u2, underwater,
                   vote_card, warship)
from gfx import GOLD, GOLD2, GREY, INK, NAVY, RED, W, WHITE, e_io, e_out, hexc, lerp, pop, seg  # noqa: E402
from people import person  # noqa: E402

CX = W / 2
GROUND = 1270
GOLDTXT = hexc("#b37a12")
GREEN = hexc("#3c8d4f")
SOV = hexc("#b8473a")
US = hexc("#3f6496")
SURF = 560   # ระดับผิวน้ำในฉากใต้ทะเล

CAMERA = {"hook": "push_in", "saturday": "pan_right", "sub": "tilt_down", "vote": "push_in", "saved": "pull_out",
          "lesson": "pan_left", "outro": "pan_right"}
TRANSITIONS = {"saturday": "zoom", "sub": "whip", "vote": "iris", "saved": "fade", "lesson": "zoom",
               "outro": "whip"}


def ap(t, a, dur=0.38):
    return pop(t, a - 0.2, dur)


def title(g, t, a, txt, col=INK, size=84, y=380):
    g.label(txt, CX, y, size, color=col, sc=ap(t, a), rot=-3)


def arkhipov(g, x, sc=0.8, mood="firm", pose="down", turn=0.2, talk=False, y=GROUND):
    person(g, x, y, ARKHIPOV, sc, mood=mood, pose=pose, turn=turn, seed=7, talk=talk)


# ------------------------------------------------------------------ 1. hook
def s_hook(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:   # วันนี้ในอดีต
        fire_button(g, CX, 960, 1.4 * pop(t, 0.2) + 0.01, 0, 0, t)
        g.label("วันนี้ในอดีต", CX, 380, 104, sc=lerp(2.0, 1, e_out(seg(t, 0.1, 0.4))) if t > 0.1 else 0, rot=-3)
        g.label("27 ตุลาคม 1962", CX, 520, 84, color=SOV, sc=pop(t, 0.5))
        return
    if t < L[2] - 0.2:   # ชายคนเดียว "ไม่กดปุ่ม"
        fire_button(g, 690, 1150, 0.9, 1.0, 0, t)
        arkhipov(g, 300, 0.8, "firm", "stop", 0.3)
        no_sign(g, 690, 760, 0.9 * ap(t, L[1] + 0.4) + 0.01, -6 + 3 * math.sin(t * 3), t)
        title(g, t, L[1], "ชายคนเดียว \"ไม่กดปุ่ม\"", SOV, 86)
        return
    if t < L[3] - 0.2:   # รอดสงครามนิวเคลียร์อย่างฉิวเฉียด
        globe(g, 380, 880, 230, t)
        clock_face(g, 790, 760, 130, lerp(5, 0.6, e_io(seg(t, L[2], L[3]))))
        g.label("ฉิวเฉียด!", 790, 960, 64, color=RED, sc=ap(t, L[2] + 1.6), rot=6)
        title(g, t, L[2], "รอดจากสงครามนิวเคลียร์", INK, 82)
        return
    clock_face(g, CX, 860, 230, lerp(12, 1, e_io(seg(t, L[3], L[3] + 1.8))))   # 24 ชั่วโมงบีบหัวใจ
    g.label("24 ชั่วโมง", CX, 1190, 92, color=RED, sc=ap(t, L[3] + 0.2))
    title(g, t, L[3], "บีบหัวใจที่สุด!", INK, 92)


# ------------------------------------------------------------------ 2. saturday
def s_saturday(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # 27 ต.ค. 1962 → วันเสาร์ทมิฬ
        dark = t > L[1] - 0.2
        calendar(g, CX, 860, 1.25 * ap(t, L[0]) + 0.01, rot=-3 + 2 * math.sin(t * 1.5), col=INK if dark else SOV)
        if not dark:
            title(g, t, L[0], "27 ตุลาคม 1962", SOV, 92)
        else:
            g.label("Black Saturday", CX, 520, 64, color=GREY, sc=ap(t, L[1] + 0.4))
            title(g, t, L[1], "\"วันเสาร์ทมิฬ\"", INK, 110)
        return
    if t < L[3] - 0.2:   # พร้อมระเบิดเป็นสงครามโลกครั้งที่ 3
        cuba.caribbean_map(g, CX, 840, 0.8, t, missiles=1.0, ring=1.0, ships=1.0, range_k=0.6)
        cuba.time_bomb(g, 790, 1120, 0.6 * ap(t, L[2] + 1.0) + 0.01, t, 1 - seg(t, L[2], L[3] + 2))
        title(g, t, L[2], "จ่อเป็นสงครามโลกครั้งที่ 3!", RED, 80)
        return
    if t < L[4] - 0.2:   # U-2
        cuba.caribbean_map(g, CX, 860, 0.8, t, missiles=1.0)
        u2(g, lerp(300, 620, seg(t, L[3] - 0.2, L[4] + 1)), lerp(1060, 760, seg(t, L[3] - 0.2, L[4] + 1)), 0.55, 40)
        title(g, t, L[3], "เครื่องบินสอดแนม U-2", US, 86)
        return
    if t < L[5] - 0.2:   # ถูกยิงตก (จอเรดาร์ + ควัน — ไม่แสดงการระเบิด)
        k = seg(t, L[4] + 0.3, L[4] + 2.2)
        radar(g, CX, 840, 300, t, 1.0, max(0.0, (k - 0.75) * 4))
        pts = [(lerp(260, CX + 120, i / 14), lerp(1140, 750, i / 14) - 40 * math.sin(i / 14 * 3)) for i in range(15)]
        smoke_trail(g, pts, t, min(1, k * 1.3))
        title(g, t, L[4], "ถูกขีปนาวุธโซเวียตยิงตก", RED, 82)
        return
    if t < L[6] - 0.2:   # นักบินเสียชีวิต
        helmet(g, CX, 920, 1.2, 4 * math.sin(t))
        ribbon(g, CX + 170, 760, 1.0 * ap(t, L[5] + 0.3) + 0.01)
        g.label("พันตรี รูดอล์ฟ แอนเดอร์สัน", CX, 1160, 54, color=GREY, sc=ap(t, L[5] + 0.3))
        title(g, t, L[5], "นักบินเสียชีวิตทันที", INK, 90)
        return
    # นายพลกดดันเคนเนดี
    for i, lk in enumerate(GENERALS):
        person(g, 680 + i * 190, GROUND, lk, 0.66, mood="angry", pose="fist" if i == 0 else "cross",
               turn=-0.4, seed=20 + i, talk=True)
    if t < L[7] - 0.2:
        cuba.red_phone(g, 270, 1100, 0.9, 1.0, t)
        title(g, t, L[6], "เสียงเรียกร้องจากเหล่านายพล", US, 78)
    else:
        person(g, 250, GROUND, JFK, 0.74, mood="worry", pose="think", turn=0.4, seed=1)
        sweat_k = ap(t, L[7] + 1)
        if sweat_k > 0.5:
            sweat(g, 280, 590, t, 2, 0.8)
        g.name_tag(t, L[7] + 0.2, 470, 1120, "จอห์น เอฟ. เคนเนดี", "ประธานาธิบดีสหรัฐฯ", side=-1)
        title(g, t, L[7], "\"ทิ้งระเบิดถล่มคิวบาเดี๋ยวนี้!\"", RED, 76)


# ------------------------------------------------------------------ 3. sub
def sea_scene(g, t, ships=False):
    underwater(g, SURF, t)
    if ships:
        for i, x in enumerate((260, 800)):
            warship(g, x, SURF - 30, 0.42, t, flip=i == 1, col=hexc("#7b8794"))


def s_sub(g, t, L, d):
    if t < L[1] - 0.2:   # ความตายไม่ได้อยู่แค่บนฟ้า
        sea_scene(g, t, ships=True)
        u2(g, 780, 470, 0.22, 90 + 10 * math.sin(t))
        title(g, t, L[0], "ความตายไม่ได้อยู่แค่บนฟ้า...", INK, 80)
        return
    if t < L[3] - 0.2:   # ใต้ทะเลแคริบเบียน / B-59 + ตอร์ปิโดนิวเคลียร์
        sea_scene(g, t, ships=False)
        submarine(g, lerp(380, CX, e_out(seg(t, L[1] - 0.2, L[2]))), 1040, 0.85, t)
        if t < L[2] - 0.2:
            title(g, t, L[1], "ลึกลงไปใต้ทะเลแคริบเบียน", NAVY, 80)
        else:
            torpedo(g, CX, 760, 0.85 * ap(t, L[2] + 1.2) + 0.01, -3 + 2 * math.sin(t * 2), 0.5 + 0.5 * math.sin(t * 4))
            title(g, t, L[2], "เรือดำน้ำโซเวียต B-59", SOV, 86)
            g.label("ตอร์ปิโดหัวรบนิวเคลียร์", CX, 520, 58, color=RED, sc=ap(t, L[2] + 1.2))
        return
    if t < L[4] - 0.2:   # ถูกล้อม + ระเบิดน้ำลึก
        sea_scene(g, t, ships=True)
        sx, sy = CX, 1130
        submarine(g, sx, sy, 0.6, t)
        for i in range(3):
            u = ((t - L[3]) * 0.6 + i / 3) % 1
            dx = 300 + i * 240
            depth_charge(g, dx, lerp(SURF + 40, sy - 60, u), 0.5, 40 * u + i * 20)
            shock_ring(g, sx + (i - 1) * 160, sy, ((t - L[3]) * 0.8 + i / 3) % 1)
        title(g, t, L[3], "ถูกล้อม + ระเบิดน้ำลึก!", RED, 86)
        return
    shake = 6 * math.sin(t * 27) * (0.5 + 0.5 * math.sin(t * 3))
    with g.at(shake, 0):
        heat = seg(t, L[5], L[6] + 1)
        sub_room(g, t, heat=heat)
        if t < L[5] - 0.2:   # ขาดการติดต่อกับมอสโก
            radio(g, 640, 880, 1.1, t)
            person(g, 260, GROUND, CREW, 0.72, mood="worry", pose="phone", turn=0.4, seed=30)
            g.label("มอสโก...?", 640, 620, 70, color=SOV, sc=ap(t, L[4] + 0.6), rot=-4)
            title(g, t, L[4], "ขาดการติดต่อกับมอสโก", INK, 82)
        elif t < L[6] - 0.2:   # อากาศหมด แบตใกล้ดับ
            gauge(g, 330, 820, 150, lerp(0.7, 0.12, seg(t, L[5], L[6])), RED, "ออกซิเจน")
            battery(g, 740, 820, 1.2 * ap(t, L[5] + 0.8) + 0.01, lerp(0.6, 0.12, seg(t, L[5], L[6])), t)
            g.label("แบตเตอรี่", 740, 1010, 40, color=INK, sc=ap(t, L[5] + 0.8))
            title(g, t, L[5], "อากาศเริ่มหมด แบตใกล้ดับ", RED, 80)
        else:   # ร้อนกว่า 50 องศา
            thermometer(g, 760, 1010, 1.2, lerp(0.5, 0.95, e_io(seg(t, L[6], L[6] + 1.6))))
            person(g, 340, GROUND, CREW, 0.74, mood="worry", pose="down", turn=0.3, seed=31)
            sweat(g, 370, 560, t, 3, 1.0)
            v = int(lerp(35, 50, e_io(seg(t, L[6], L[6] + 1.6))))
            g.label(f"{v}°C+", 760, 620, 100, color=RED, sc=ap(t, L[6] + 0.2), rot=6)
            title(g, t, L[6], "ร้อนกว่า 50 องศาเซลเซียส!", RED, 82)


# ------------------------------------------------------------------ 4. vote
def s_vote(g, t, L, d):
    if t >= L[7] - 0.2:   # ลอยลำขึ้นผิวน้ำ
        g.c.rectangle(-500, 140, 2100, SURF - 140)
        g.c.set_source_rgba(1, 1, 1, 1)
        g.c.fill()
        underwater(g, SURF + 200, t)
        k = e_io(seg(t, L[7], L[7] + 2.4))
        submarine(g, CX, lerp(1180, SURF + 190, k), 0.75, t, tilt=-8 * math.sin(math.pi * k))
        if k > 0.9:
            g.sparkle(CX + 60, SURF + 20, 30)
        title(g, t, L[7], "สั่งลอยลำขึ้นผิวน้ำ เพื่อเจรจา!", GREEN, 78)
        return
    alarm = 1.0 if t < L[4] - 0.2 else 0.3
    sub_room(g, t, heat=0.6, alarm=alarm)
    if t < L[2] - 0.2:   # กัปตันเชื่อว่าสงครามเริ่ม → สั่งเตรียมยิง
        person(g, 300, GROUND, SAVITSKY, 0.8, mood="shout" if t > L[1] - 0.2 else "angry",
               pose="point" if t > L[1] - 0.2 else "fist", turn=0.4, seed=40, talk=True)
        sweat(g, 320, 540, t, 2, 0.8)
        if t < L[1] - 0.2:
            g.label("สงครามโลกครั้งที่ 3 ?!", 680, 860, 66, color=RED, sc=ap(t, L[0] + 1.0), rot=5)
            title(g, t, L[0], "กัปตันเชื่อว่าสงครามเริ่มแล้ว", INK, 78)
        else:
            torpedo(g, 650, 760, 0.6, -2 + 2 * math.sin(t * 3), 1.0)
            fire_button(g, 720, 1080, 0.8, seg(t, L[1] + 0.6, L[1] + 1.4), 0, t)
            title(g, t, L[1], "สั่งเตรียมยิงตอร์ปิโดนิวเคลียร์!", RED, 76)
        return
    names = ("กัปตัน", "นายทหารการเมือง", "อาร์คีปอฟ")
    if t < L[4] - 0.2:   # ต้องเห็นชอบ 3 นาย / 2 คนแรกอนุมัติ
        for i in range(3):
            k = ap(t, L[2] + 0.3 * i, 0.3)
            ok = None if t < L[3] - 0.2 + 0.4 * i or i == 2 else True
            if ok:
                vote_card(g, 230 + i * 300, 860, 0.95, -4 + 4 * i, True, names[i], k)
            elif k > 0.02:
                with g.at(230 + i * 300, 860, 0.95 * k, -4 + 4 * i):
                    g.rrect(-130, -170, 260, 340, 18, hexc("#f4eedf"), 6)
                    g.text("?", 0, 0, 140, "kanit", GREY)
                    g.text(names[i], 0, 135, 30, "kanitsb", INK)
        if t < L[3] - 0.2:
            title(g, t, L[2], "ต้องเห็นชอบจากนายทหาร 3 นาย", INK, 76)
        else:
            title(g, t, L[3], "2 คนแรก อนุมัติแล้ว...", GREEN, 84)
        return
    # อาร์คีปอฟ คนสุดท้าย
    for i, lk in enumerate((SAVITSKY, POLIT)):
        person(g, 650 + i * 200, GROUND, lk, 0.62, mood="angry", pose="cross" if i else "fist", turn=-0.4,
               seed=41 + i)
    stop = t > L[6] - 0.2
    arkhipov(g, 280, 0.82, "firm", "stop" if stop else "down", 0.35, talk=stop)
    g.name_tag(t, L[4] + 0.3, 500, 1120, "วาซิลี อาร์คีปอฟ", "รองผู้บังคับการกองเรือ", side=-1)
    if t < L[6] - 0.2:
        title(g, t, L[4], "เหลือเสียงเดียว...", INK, 92)
    else:
        no_sign(g, 740, 720, 0.75 * ap(t, L[6] + 0.2) + 0.01, -8 + 3 * math.sin(t * 3), t)
        title(g, t, L[6], "ปฏิเสธเสียงแข็ง ห้ามยิงเด็ดขาด!", RED, 76)


# ------------------------------------------------------------------ 5. saved
def s_saved(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:   # คัดค้านเพียงเสียงเดียว
        arkhipov(g, 300, 0.82, "firm", "down", 0.3)
        vote_card(g, 720, 860, 1.1, 5 + 2 * math.sin(t * 2), False, "อาร์คีปอฟ", ap(t, L[0] + 0.3))
        g.label("1 เสียง", 720, 600, 80, color=RED, sc=ap(t, L[0] + 0.8))
        title(g, t, L[0], "เสียงคัดค้านเพียงเสียงเดียว", INK, 78)
        return
    if t < L[2] - 0.2:   # หยุดหายนะ ร้อยล้านชีวิต
        k = e_io(seg(t, L[1], L[1] + 3.0))
        globe(g, 360, 880, 230, t, dim=1 - k)
        clock_face(g, 790, 780, 120, lerp(0.5, 7, k))
        g.label("ร้อยล้านชีวิต", 360, 1180, 66, color=GREEN, sc=ap(t, L[1] + 2.0))
        title(g, t, L[1], "หยุดหายนะนิวเคลียร์ได้หวุดหวิด", GREEN, 76)
        return
    if t < L[3] - 0.2:   # วันถัดมา
        calendar(g, CX, 860, 1.2, "28", "ต.ค. 1962", "อาทิตย์", 3 * math.sin(t * 1.5), GREEN)
        title(g, t, L[2], "วันถัดมา...", INK, 100)
        return
    k = e_io(seg(t, L[3] + 0.4, L[3] + 2.4))   # สองผู้นำถอยคนละก้าว
    person(g, lerp(390, 250, k), GROUND, JFK, 0.72, mood="neutral" if k < 1 else "smile", pose="down", turn=0.5,
           seed=1)
    person(g, lerp(690, 830, k), GROUND, KHRUSHCHEV, 0.72, mood="neutral" if k < 1 else "smile", pose="down",
           turn=-0.5, seed=2)
    g.name_tag(t, L[3] + 0.3, 800, 520, "นิกิตา ครุสชอฟ", "ผู้นำสหภาพโซเวียต", side=-1)
    if t < L[4] - 0.2:
        for sx in (-1, 1):
            g.label("←" if sx < 0 else "→", CX + sx * 120, 860, 90, color=GREY, sc=ap(t, L[3] + 0.6))
        title(g, t, L[3], "ยอมถอยคนละก้าว", INK, 92)
    else:
        dove(g, CX, 780 + 20 * math.sin(t * 2), 1.3 * ap(t, L[4]) + 0.01, t)
        title(g, t, L[4], "วิกฤตคลี่คลายในที่สุด", GREEN, 86)


# ------------------------------------------------------------------ 6. lesson
def s_lesson(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:
        calendar(g, CX, 860, 1.15, rot=-3 + 2 * math.sin(t * 1.4), col=INK)
        title(g, t, L[0], "\"วันเสาร์ทมิฬ\" พิสูจน์ว่า...", INK, 84)
        return
    if t < L[2] - 0.2:   # ความตึงเครียดพร้อมระเบิด
        cuba.thread(g, 200, 880, 860, 1.0, t)
        cuba.time_bomb(g, CX, 1130, 0.7, t, 0.3)
        title(g, t, L[1], "ความตึงเครียดที่พร้อมระเบิด", RED, 78)
        return
    if t < L[3] - 0.2:   # ไม่ใช่การชักอาวุธ
        torpedo(g, CX, 860, 1.0, -3 + 2 * math.sin(t * 2))
        k = seg(t, L[2] + 1.6, L[2] + 2.4)
        if k > 0:
            g.line([(CX - 320, 700), (CX - 320 + 640 * k, 700 + 320 * k)], 18, RED, amp=0)
        title(g, t, L[2], "ไม่ใช่การชักอาวุธ", INK, 90)
        return
    if t < L[4] - 0.2:   # กล้าพูดคำว่า "ไม่"
        arkhipov(g, 300, 0.82, "firm", "stop", 0.35, talk=True)
        no_sign(g, 730, 780, 1.0 * ap(t, L[3] + 0.2) + 0.01, -5 + 3 * math.sin(t * 3), t)
        title(g, t, L[3], "กล้าพูดคำว่า \"ไม่\"", RED, 96)
        return
    globe(g, CX, 900, 250, t)
    dove(g, CX + 30, 600 + 15 * math.sin(t * 2), 1.0 * ap(t, L[4]) + 0.01, t)
    title(g, t, L[4], "หยุดความบ้าคลั่งของสงคราม", GREEN, 78)


# ------------------------------------------------------------------ 7. outro
def s_outro(g, t, L, d):
    if t < L[1] - 0.2:   # คิดอย่างไร
        g.ground(GROUND, WHITE)
        arkhipov(g, 300, 0.8, "smile", "down", 0.3)
        with g.at(720, 760, ap(t, L[0] + 0.3)):
            g.bubble(0, 0, 360, 200, WHITE, tail=(-1, 1))
            g.label("?", 0, 0, 120, color=INK)
        title(g, t, L[0], "คิดอย่างไรกันบ้าง?", INK, 92)
        return
    if t < L[3] - 0.2:   # ถ้าคุณอยู่ในเรือดำน้ำ
        shake = (8 * math.sin(t * 29)) if t > L[2] - 0.2 else 0
        with g.at(shake, 0):
            sub_room(g, t, heat=0.8, alarm=0.6 if t > L[2] - 0.2 else 0)
            radio(g, 700, 800, 0.9, t)
            person(g, 300, GROUND, CREW, 0.75, mood="worry", pose="down", turn=0.3, seed=50)
            sweat(g, 330, 540, t, 3, 0.9)
            if t > L[2] - 0.2:
                shock_ring(g, 700, 1100, (t * 0.9) % 1)
                title(g, t, L[2], "โดนถล่มด้วยระเบิดน้ำลึก", RED, 80)
            else:
                title(g, t, L[1], "ร้อนระอุ ขาดการติดต่อ", INK, 86)
        return
    if t < L[4] - 0.2:   # มีสติพอไม่กดปุ่มไหม
        g.ground(GROUND, WHITE)
        fire_button(g, CX, 980, 1.4, 1.0, 0, t)
        g.label("?", CX + 240, 720, 160, color=RED, sc=ap(t, L[3] + 0.5), rot=8)
        title(g, t, L[3], "คุณจะไม่กดปุ่มไหม?", RED, 92)
        return
    g.ground(GROUND, WHITE)
    with g.at(CX + 170, 640, ap(t, L[4])):   # ชวนคอมเมนต์
        g.bubble(0, 0, 460, 220, WHITE, tail=(-1, 1))
        for i in range(3):
            g.circle(-110 + i * 110, 0, 24 + 6 * math.sin(t * 6 - i), INK, 0)
    arkhipov(g, 270, 0.78, "smile", "wave", 0.3, talk=True)
    title(g, t, L[4], "มาแลกเปลี่ยนกันในคอมเมนต์!", RED, 70)


SCENES = {
    "hook": s_hook, "saturday": s_saturday, "sub": s_sub, "vote": s_vote, "saved": s_saved,
    "lesson": s_lesson, "outro": s_outro,
}
NO_IRIS = set()
