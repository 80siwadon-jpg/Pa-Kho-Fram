"""ฉากตอน: 30 ต.ค. 1961 ซาร์ บอมบา — ระเบิดที่รุนแรงที่สุดที่มนุษย์เคยจุดชนวน
ไม่แสดงคนบาดเจ็บ: ลูกไฟ/ควันดอกเห็ด/วงคลื่นกระแทก/บ้านร้างพังราบแทน"""
import math
import os
import sys

import cairo

sys.path.insert(0, os.path.dirname(__file__))
from chars import (ARCTIC, GENERAL, JFK, KHRUSHCHEV, PILOT, SCIENTISTS, SOV, US, arctic, atom, balance,  # noqa: E402
                   bomber, calendar, cloud, crown, dial, dove, everest, fallout, fireball, flat_house, globe, hands,
                   missile, mushroom, parachute, seismo, shield, shock_ring, time_bomb, treaty, trefoil, tsar)
from gfx import GOLD, GOLD2, GREY, INK, NAVY, RED, W, WHITE, e_io, e_out, hexc, lerp, pop, seg  # noqa: E402
from people import person  # noqa: E402

CX = W / 2
GROUND = 1270
GOLDTXT = hexc("#b37a12")
NIGHTTXT = hexc("#f2c94c")
GREEN = hexc("#3c8d4f")
NIGHT = hexc("#1d2a44")

CAMERA = {"hook": "push_in", "coldwar": "pan_right", "flight": "pan_left", "blast": "push_in", "damage": "dutch",
          "treaty": "pull_out", "lesson": "push_in", "outro": "pan_right"}
TRANSITIONS = {"coldwar": "zoom", "flight": "whip", "blast": "fade", "damage": "zoom", "treaty": "iris",
               "lesson": "fade", "outro": "whip"}


def ap(t, a, dur=0.38):
    return pop(t, a - 0.2, dur)


def title(g, t, a, txt, col=INK, size=84, y=380):
    g.label(txt, CX, y, size, color=col, sc=ap(t, a), rot=-3)


def sky(g, k=1.0, flash=0.0, y1=1270):
    """ท้องฟ้าอาร์กติกยามมืด (แผงกรมท่าจางลงหาขอบฟ้า) + แสงวาบจากขอบฟ้า"""
    if k <= 0:
        return
    c = g.c
    lg = cairo.LinearGradient(0, 160, 0, y1)
    a = 0.95 * k * (1 - 0.85 * flash)
    lg.add_color_stop_rgba(0, *NIGHT[:3], a)
    lg.add_color_stop_rgba(0.8, *NIGHT[:3], a * 0.75)
    lg.add_color_stop_rgba(1, *NIGHT[:3], a * 0.35)
    c.set_source(lg)
    c.rectangle(-600, 140, 2300, y1 - 140)
    c.fill()
    for i in range(18):   # ดาว
        sx, sy = (i * 197) % 1100 - 10, 200 + (i * 83) % 600
        g.circle(sx, sy, 3 + (i % 3), (1, 1, 1, 0.6 * k * (1 - flash)), 0)


def chip(g, x, y, txt, col, k, rot=0.0, w=320):
    if k < 0.02:
        return
    with g.at(x, y, k, rot):
        g.rrect(-w / 2, -64, w, 128, 40, WHITE, 7, stroke=col)
        g.label(txt, 0, 0, 52, color=col)


def ruler(g, x, y0, y1, ticks, k=1.0, col=INK):
    """ไม้วัดความสูงแนวตั้ง y0 (พื้น) → y1 (ยอด)"""
    if k <= 0:
        return
    yt = lerp(y0, y1, k)
    g.line([(x, y0), (x, yt)], 6, col, amp=0)
    for frac, txt in ticks:
        if frac <= k + 1e-6:
            yy = lerp(y0, y1, frac)
            g.line([(x - 18, yy), (x + 18, yy)], 6, col, amp=0)
            g.label(txt, x + 30, yy, 44, color=col, anchor="l")


def khrushchev(g, x, sc=0.8, mood="firm", pose="down", turn=-0.3, talk=False):
    person(g, x, GROUND, KHRUSHCHEV, sc, mood=mood, pose=pose, turn=turn, seed=2, talk=talk)


def jfk(g, x, sc=0.8, mood="firm", pose="down", turn=0.3, talk=False):
    person(g, x, GROUND, JFK, sc, mood=mood, pose=pose, turn=turn, seed=1, talk=talk)


# ------------------------------------------------------------------ 1. hook
def s_hook(g, t, L, d):
    if t < L[1] - 0.2:   # วันนี้ในอดีต: ความมืดเหนืออาร์กติก
        sky(g, 1.0)
        arctic(g, 1150, t)
        g.circle(CX, 1080, 10 + 6 * math.sin(t * 6), (1, 0.9, 0.6, 1), 0)
        g.label("วันนี้ในอดีต...", CX, 600, 100, color=NIGHTTXT, sc=ap(t, L[0] + 0.25), rot=-3)
        return
    if t < L[2] - 0.2:   # แฟลชเห็นได้ไกลเกือบ 1,000 กม.
        fl = e_out(seg(t, L[1] - 0.2, L[1] + 0.8))
        sky(g, 1.0, 0.6 * fl)
        arctic(g, 1150, t)
        g.c.save()
        g.c.rectangle(-600, 140, 2300, 1130)
        g.c.clip()
        g.sunburst(260, 1080, 120, 120 + 700 * fl, 22, t * 10, 14, (1, 0.95, 0.75, 0.75))
        g.c.restore()
        fireball(g, 260, 1080, 60 + 60 * fl, t, 1)
        u = e_io(seg(t, L[1] + 0.6, L[1] + 2.0))
        g.line([(300, 1220), (lerp(300, 880, u), 1220)], 8, NIGHTTXT, amp=0)
        if u > 0.95:
            g.poly([(880, 1195), (920, 1220), (880, 1245)], NIGHTTXT, 0, amp=0)
        g.label("เกือบ 1,000 กม.", 600, 1130, 60, color=NIGHTTXT, sc=ap(t, L[1] + 1.2))
        g.label("แฟลชแสงสีขาว", CX, 420, 92, color=NIGHTTXT, sc=ap(t, L[1] + 0.2), rot=-3)
        return
    if t < L[3] - 0.2:   # คลื่นกระแทกวนรอบโลก 3 รอบ
        globe(g, CX, 840, 300, t)
        p = seg(t, L[2] - 0.1, L[3] - 0.4) * 3
        n = min(3, int(p) + 1)
        u = p % 1 if p < 3 else 1
        a = u * 2 * math.pi - math.pi / 2
        g.arc(CX, 840, 350, -90, math.degrees(a), 14, (*RED[:3], 0.9))
        g.circle(CX + 350 * math.cos(a), 840 + 350 * math.sin(a), 26, GOLD2, 5)
        g.star(CX, 560, 50, (1, 0.75, 0.35, 1), 5, pts=10, inner=0.5)
        g.label(f"รอบที่ {n}", CX, 1270, 80, color=RED, sc=ap(t, L[2] + 0.2))
        title(g, t, L[2], "คลื่นกระแทกวนรอบโลก 3 รอบ!", RED, 80)
        return
    sky(g, 0.85)   # ระเบิดที่รุนแรงที่สุด
    arctic(g, 1250, t)
    k = e_out(seg(t, L[3] - 0.3, L[3] + 2.6))
    mushroom(g, CX, 1230, 640, 0.25 + 0.75 * k, t, 1.0)
    title(g, t, L[3] + 0.3, "ระเบิดที่รุนแรงที่สุดในโลก!", NIGHTTXT, 84, 300)


# ------------------------------------------------------------------ 2. coldwar
def s_coldwar(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:   # 30 ต.ค. 1961
        calendar(g, CX, 860, 1.25 * ap(t, L[0]) + 0.01, "30", "ต.ค. 1961", "จันทร์", -3 + 2 * math.sin(t), RED)
        title(g, t, L[0], "30 ตุลาคม 1961", RED, 92)
        return
    if t < L[2] - 0.2:   # สงครามเย็นระอุ
        chip(g, 300, 760, "สหรัฐฯ", US, ap(t, L[1] + 0.1), -5, 300)
        chip(g, 780, 760, "โซเวียต", SOV, ap(t, L[1] + 0.4), 5, 300)
        missile(g, 300, 1180, 0.8, 30 + 3 * math.sin(t * 3))
        missile(g, 780, 1180, 0.8, -30 - 3 * math.sin(t * 3))
        time_bomb(g, CX, 1050, 0.75, t, 0.4)
        for i in range(3):   # ไอร้อน
            u = (t * 0.8 + i / 3) % 1
            g.line([(CX - 60 + i * 60 + 12 * math.sin(t * 4 + i), 880 - 120 * u),
                    (CX - 60 + i * 60 - 12 * math.sin(t * 4 + i), 820 - 120 * u)], 6, (*RED[:3], 1 - u), amp=0)
        title(g, t, L[1], "สงครามเย็น ระอุถึงขีดสุด", RED, 82)
        return
    if t < L[5] - 0.2:   # ครุชชอฟ แสดงแสนยานุภาพ สั่งทดสอบ "อีวาน"
        if t > L[3] - 0.2:
            for i in range(3):
                missile(g, 620 + i * 130, 1180, 0.55 * ap(t, L[3] + 0.2 * i) + 0.01, 0)
        pose = "down" if t < L[3] - 0.2 else ("fist" if t < L[4] - 0.2 else "point")
        khrushchev(g, 300, 0.84, "angry" if t > L[3] - 0.2 else "firm", pose, 0.3, talk=True)
        g.name_tag(t, L[2] + 0.1, 300, 1060, "นิกิตา ครุชชอฟ", "ผู้นำสหภาพโซเวียต", side=1)
        if t > L[4] - 0.2:   # แฟ้มลับ "อีวาน"
            with g.at(760, 620, ap(t, L[4] + 0.3), 6):
                g.rrect(-190, -140, 380, 280, 14, hexc("#e8d6a8"), 6)
                g.text("อีวาน", 0, -20, 90, "kanit", INK)
                with g.at(80, 80, 1, -14):
                    g.rrect(-90, -36, 180, 72, 10, WHITE, 6, stroke=RED)
                    g.text("ลับ", 0, 0, 48, "kanit", RED)
            title(g, t, L[4], "ทดสอบระเบิดไฮโดรเจน", SOV, 84)
        elif t > L[3] - 0.2:
            title(g, t, L[3], "ข่มขวัญชาติตะวันตก!", SOV, 88)
        else:
            title(g, t, L[2], "สหภาพโซเวียต", SOV, 92)
        return
    tsar(g, CX, 960, 1.05 * ap(t, L[5]) + 0.01, -4 + 2 * math.sin(t * 1.5))   # ซาร์ บอมบา + มงกุฎ
    if t > L[6] - 0.2:
        crown(g, CX + 30, 790 + 10 * math.sin(t * 3), 0.9 * ap(t, L[6]) + 0.01, 8)
        g.label("ราชาแห่งระเบิด", CX, 1210, 80, color=GOLDTXT, sc=ap(t, L[6] + 0.2))
    g.label("Tsar Bomba", CX, 560, 64, color=GREY, sc=ap(t, L[5] + 0.6))
    title(g, t, L[5], "\"ซาร์ บอมบา\"", RED, 110)


# ------------------------------------------------------------------ 3. flight
def s_flight(g, t, L, d):
    if t < L[1] - 0.2:   # ตู-95 สีขาว
        for i in range(3):
            g.c.save()
            cloud(g, (i * 420 - t * 120) % 1500 - 200, 1180 + i * 40, 0.7, hexc("#eef3f7"), 5)
            g.c.restore()
        bomber(g, CX, 820 + 20 * math.sin(t * 1.4), 1.05, -2, t, 1.0)
        g.label("ตู-95 (Tu-95)", CX, 1060, 70, color=SOV, sc=ap(t, L[0] + 0.5))
        title(g, t, L[0], "ทูโพเลฟ ตู-95 ดัดแปลงพิเศษ", INK, 82)
        return
    if t < L[2] - 0.2:   # ระเบิดหนัก 27 ตัน
        g.ground(GROUND, WHITE)
        tsar(g, CX, 1120, 1.15, 0)
        with g.at(CX, 780 + 12 * math.sin(t * 3), ap(t, L[1] + 0.4), -4):
            g.poly([(-150, 90), (-110, -80), (110, -80), (150, 90)], hexc("#3a3f48"), 7, amp=0)
            g.circle(0, -100, 34, WHITE, 7)
            g.text("27 ตัน", 0, 20, 64, "kanit", WHITE)
        title(g, t, L[1], "ระเบิดยักษ์ หนัก 27 ตัน", INK, 86)
        return
    if t < L[3] - 0.2:   # ปิดประตูห้องทิ้งระเบิดไม่มิด
        bomber(g, CX + 40, 760, 1.55, 0, t, 1.0)
        k = ap(t, L[2] + 0.5)
        if k > 0.02:
            g.c.new_path()
            g.c.arc(CX + 40 - 30 * 1.55, 760 + 50 * 1.55, 210 * k, 0, 2 * math.pi)
            g.c.set_source_rgba(*RED)
            g.c.set_line_width(10)
            g.c.stroke()
        g.label("ปิดไม่มิด!", CX, 1150, 96, color=RED, sc=ap(t, L[2] + 0.9), rot=-4)
        title(g, t, L[2], "ระเบิดใหญ่เกินห้องทิ้งระเบิด", INK, 80)
        return
    if t < L[4] - 0.2:   # เหนือเกาะเซแวร์นี มหาสมุทรอาร์กติก
        arctic(g, 1150, t)
        x = lerp(-200, 1250, seg(t, L[3] - 0.3, L[4] + 0.3))
        bomber(g, x, 720, 0.55, -3, t, 1.0)
        g.label("เกาะเซแวร์นี", 560, 1090, 64, color=INK, sc=ap(t, L[3] + 0.6))
        g.label("มหาสมุทรอาร์กติก", CX, 1240, 56, color=NAVY, sc=ap(t, L[3] + 1.2))
        title(g, t, L[3], "ทะยานสู่ขั้วโลกเหนือ", NAVY, 86)
        return
    if t < L[6] - 0.2:   # ร่มชูชีพ + นักบินบินหนี
        arctic(g, 1250, t, island=True)
        u = seg(t, L[4] - 0.2, L[6])
        by = lerp(860, 1000, u)
        parachute(g, 250, by - 70, 0.7, ap(t, L[4] + 0.3), t)
        tsar(g, 250, by, 0.4, 90)
        if t > L[5] - 0.2:
            v = e_io(seg(t, L[5] - 0.2, L[6]))
            bx = lerp(700, 780, v)
            bomber(g, bx, 600 - 60 * v, 0.3 - 0.1 * v, -8, t, 0.0)
            for i in range(4):
                g.line([(bx - 160 - i * 30, 560 + i * 25), (bx - 260 - i * 30, 560 + i * 25)], 6, GREY, amp=0)
            title(g, t, L[5], "บินหนีให้ไกลที่สุด!", RED, 90, 330)
        else:
            title(g, t, L[4], "ร่มชูชีพยักษ์ ชะลอการตก", INK, 82, 330)
        return
    g.ground(GROUND, WHITE)   # นักวิทยาศาสตร์คำนวณ / โอกาสรอด 50/50
    if t < L[7] - 0.2:
        with g.at(720, 760, ap(t, L[6])):
            g.rrect(-230, -170, 460, 340, 16, hexc("#2f4a3a"), 8)
            for i, s in enumerate(["E = mc²", "50 Mt ÷ ...", "t = 188 วิ?"]):
                g.text(s, 0, -100 + i * 90, 50, "kanitsb", WHITE)
        for i, lk in enumerate(SCIENTISTS):
            person(g, 230 + i * 160, GROUND, lk, 0.7, mood="worry", pose="think" if i else "point", turn=0.4,
                   seed=30 + i, talk=i == 0)
        title(g, t, L[6], "นักวิทยาศาสตร์คำนวณไว้...", INK, 84)
        return
    person(g, 280, GROUND, PILOT, 0.84, mood="worry", pose="down", turn=0.3, seed=40)
    k = ap(t, L[7] + 0.3)
    if k > 0.02:   # เหรียญ 50/50
        with g.at(720, 820, k, 10 * math.sin(t * 2)):
            g.c.new_path()
            g.c.arc(0, 0, 200, math.pi / 2, 3 * math.pi / 2)
            g.c.close_path()
            g.c.set_source_rgba(*GREEN)
            g.c.fill()
            g.c.new_path()
            g.c.arc(0, 0, 200, -math.pi / 2, math.pi / 2)
            g.c.close_path()
            g.c.set_source_rgba(*RED)
            g.c.fill()
            g.circle(0, 0, 200, (0, 0, 0, 0), 8)
            g.text("50/50", 0, 0, 100, "kanit", WHITE)
    title(g, t, L[7], "โอกาสรอดของนักบิน", RED, 88)


# ------------------------------------------------------------------ 4. blast
def s_blast(g, t, L, d):
    if t < L[1] - 0.2:   # ปลดระเบิด จุดชนวนที่ 4,000 ม.
        sky(g, 1.0)
        arctic(g, 1250, t)
        u = e_io(seg(t, L[0], L[1] - 0.3))
        yb = lerp(600, 820, u)
        parachute(g, 520, yb - 70, 0.75, 1, t)
        tsar(g, 520, yb, 0.3, 90)
        ruler(g, 740, 1240, 520, [(0, "0 ม."), (0.5, "2,000"), (1, "4,000 ม.")], e_out(seg(t, L[0], L[0] + 1.5)),
              NIGHTTXT)
        title(g, t, L[0], "จุดชนวนที่ 4,000 เมตร", NIGHTTXT, 86, 300)
        return
    if t < L[2] - 0.2:   # นรกบนดินปะทุ (แฟลช)
        fl = seg(t, L[1] - 0.2, L[2])
        g.c.set_source_rgba(1, 0.97, 0.85, 1 - 0.6 * fl)
        g.c.rectangle(-600, 140, 2300, 1130)
        g.c.fill()
        g.c.save()
        g.c.rectangle(-600, 140, 2300, 1130)
        g.c.clip()
        g.sunburst(CX, 820, 150, 900, 24, t * 12, 16, (1, 0.75, 0.3, 0.7))
        g.c.restore()
        fireball(g, CX, 820, 120 + 160 * e_out(fl), t, 1)
        title(g, t, L[1], "นรกบนดินปะทุขึ้น!", RED, 100)
        return
    if t < L[4] - 0.2:   # ลูกไฟกว้างเกือบ 10 กม. / แผดเผาทุกสิ่ง
        sky(g, 0.6, 0.3)
        arctic(g, 1250, t)
        k = e_out(seg(t, L[2] - 0.2, L[4]))
        r = 180 + 120 * k
        if t > L[3] - 0.2:
            g.sunburst(CX, 880, r, r + 350, 20, t * 10, 14, (1, 0.8, 0.35, 0.6))
        fireball(g, CX, 880, r, t, 1)
        g.line([(CX - r, 1220), (CX + r, 1220)], 8, INK, amp=0)
        for sx in (-1, 1):
            g.line([(CX + sx * r, 1195), (CX + sx * r, 1245)], 8, INK, amp=0)
        g.label("≈ 10 กม.", CX, 1170, 64, color=INK, sc=ap(t, L[2] + 0.5))
        if t > L[3] - 0.2:
            title(g, t, L[3], "สว่างวาบ แผดเผาทุกสิ่ง!", RED, 88)
        else:
            title(g, t, L[2], "ลูกไฟกว้างเกือบ 10 กิโลเมตร", RED, 80)
        return
    if t < L[6] - 0.2:   # ดอกเห็ดสูง 67 กม. = เอเวอเรสต์ × 7
        k = e_out(seg(t, L[4] - 0.3, L[5]))
        mushroom(g, 440, 1240, 700, 0.3 + 0.7 * k, t, 0.6, 0.85)
        if t < L[5] - 0.2:
            ruler(g, 760, 1240, 520, [(0, "0"), (1, "67 กม.")], k)
        if t > L[5] - 0.2:
            for i in range(7):   # เอเวอเรสต์ 7 ลูกซ้อน
                yy = 1240 - i * 120
                everest(g, 700, yy, 120 * ap(t, L[5] + 0.12 * i) + 0.01)
            g.label("เอเวอเรสต์ × 7", 700, 300, 70, color=GOLDTXT, sc=ap(t, L[5] + 0.9), rot=-3)
            return
        title(g, t, L[4], "ควันดอกเห็ดสูง 67 กม.", INK, 86, 300)
        return
    if t < L[7] - 0.2:   # 50 เมกะตัน
        g.ground(GROUND, WHITE)
        v = 50 * e_out(seg(t, L[6], L[6] + 1.8))
        dial(g, CX, 1000, 1.25, v, 100)
        title(g, t, L[6], "50 เมกะตัน!", RED, 110)
        return
    g.ground(GROUND, WHITE)   # ฮิโรชิมา × 3,300
    with g.at(270, 900, ap(t, L[7])):
        g.circle(0, 0, 50, hexc("#5f6b5a"), 6)
        g.label("ฮิโรชิมา", 0, 110, 50, color=INK)
    g.label("×", 470, 900, 110, color=GREY, sc=ap(t, L[7] + 0.4))
    n = int(120 * e_out(seg(t, L[7] + 0.5, L[7] + 2.5)))
    for i in range(n):
        g.circle(600 + (i % 10) * 32, 720 + (i // 10) * 32 + 6 * math.sin(t * 4 + i * 0.4), 12, hexc("#5f6b5a"), 0)
    g.label("3,300 เท่า!", 740, 1180, 100, color=RED, sc=ap(t, L[7] + 1.2), rot=-4)
    title(g, t, L[7], "มากกว่าฮิโรชิมา", INK, 92)


# ------------------------------------------------------------------ 5. damage
def s_damage(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # หมู่บ้านร้าง 55 กม. ถูกบดราบ
        crush = e_io(seg(t, L[1] + 0.3, L[1] + 1.4))
        if t > L[1] - 0.2:
            r = 200 + 1200 * seg(t, L[1] - 0.2, L[1] + 1.4)
            g.c.save()
            g.c.rectangle(-600, 140, 2300, GROUND - 140)
            g.c.clip()
            shock_ring(g, -300, 1100, r, 1 - seg(t, L[1] + 0.9, L[1] + 1.6), lw=16)
            g.c.restore()
        for i in range(4):
            flat_house(g, 220 + i * 210, GROUND, 0.62, min(1, crush * (1.2 - 0.05 * i)), i)
        g.line([(150, 640), (900, 640)], 8, INK, amp=0)
        g.label("55 กม.", CX, 590, 66, color=INK, sc=ap(t, L[0] + 0.5))
        if t > L[1] - 0.2:
            title(g, t, L[1], "ราบเป็นหน้ากลอง!", RED, 96)
        else:
            title(g, t, L[0], "หมู่บ้านร้าง ห่างออกไป 55 กม.", INK, 80)
        return
    if t < L[3] - 0.2:   # คลื่นความร้อน 100 กม.
        cx, cy = CX, 860
        for i, (r, lab) in enumerate(((330, "100 กม."), (200, "55 กม."), (80, ""))):
            k = ap(t, L[2] + 0.3 * (2 - i))
            g.circle(cx, cy, r * k * (1 + 0.03 * math.sin(t * 3 - i)) + 1, (1, 0.6 - 0.15 * i, 0.25, 0.25 + 0.15 * i), 5)
            if lab:
                g.label(lab, cx + r * 0.72, cy - r * 0.72, 48, color=RED, sc=k)
        fireball(g, cx, cy, 40, t, 1)
        title(g, t, L[2], "คลื่นความร้อน ไกลกว่า 100 กม.", RED, 80)
        return
    if t < L[4] - 0.2:   # แผ่นดินไหว 5 ริกเตอร์
        seismo(g, CX, 860, 1.1, t, ap(t, L[3] + 0.3))
        g.label("≈ 5 ริกเตอร์", CX, 1150, 80, color=RED, sc=ap(t, L[3] + 1.0))
        title(g, t, L[3], "สั่นสะเทือนเท่าแผ่นดินไหว", INK, 84)
        return
    if t < L[5] - 0.2:   # สิ่งที่น่ากลัวที่สุด
        g.label("?", CX, 880, 360, color=RED, sc=ap(t, L[4]), rot=6 * math.sin(t * 2))
        title(g, t, L[4], "ที่น่ากลัวที่สุดคือ...", RED, 92)
        return
    if t < L[7] - 0.2:   # ออกแบบไว้ 100 Mt → ลดเหลือ 50
        v = 100 * e_out(seg(t, L[5], L[5] + 1.5))
        if t > L[6] - 0.2:
            v = lerp(100, 50, e_io(seg(t, L[6] + 0.4, L[6] + 1.8)))
            for i, lk in enumerate(SCIENTISTS):
                person(g, 200 + i * 680, GROUND, lk, 0.62, mood="worry", pose="stop" if i == 0 else "think",
                       turn=0.4 - 0.8 * i, seed=30 + i)
        dial(g, CX, 980, 1.05, v + 1.5 * math.sin(t * 9), 100)
        trefoil(g, CX, 640, 50 + 6 * math.sin(t * 3), rot=t * 20)
        if t > L[6] - 0.2:
            title(g, t, L[6], "ลดลงครึ่งหนึ่ง นาทีสุดท้าย!", GREEN, 84)
        else:
            title(g, t, L[5], "ออกแบบไว้ 100 เมกะตัน!", RED, 86)
        return
    with g.at(CX, 1100):   # กัมมันตรังสีย้อนกลับมาโซเวียต
        for i in range(3):
            g.c.save()
            flat_house(g, -260 + i * 260, 170, 0.5, 0, i)
            g.c.restore()
    g.label("ดินแดนโซเวียต", CX, 1210, 56, color=SOV, sc=ap(t, L[7] + 0.4))
    u = e_io(seg(t, L[7] - 0.2, L[7] + 2.5))
    fallout(g, lerp(1000, 640, u), 760, 1.0, t, ap(t, L[7]))
    for i in range(4):
        g.line([(lerp(1200, 860, u) + i * 40, 720 + i * 30), (lerp(1300, 960, u) + i * 40, 720 + i * 30)], 6,
               GREY, amp=0)
    title(g, t, L[7], "กลัวกัมมันตรังสีย้อนกลับมา!", RED, 82)


# ------------------------------------------------------------------ 6. treaty
def s_treaty(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:   # อานุภาพน่าสะพรึง
        mushroom(g, CX, 1240, 620, 1.0, t, 0.5)
        title(g, t, L[0], "อานุภาพที่น่าสะพรึงกลัว", RED, 84)
        return
    if t < L[3] - 0.2:   # สองขั้วมหาอำนาจตระหนัก / จุดเปลี่ยน
        globe(g, CX, 720, 170, t)
        jfk(g, 220, 0.78, "worry", "think", 0.4)
        khrushchev(g, 860, 0.78, "worry", "think", -0.4)
        g.name_tag(t, L[1] + 0.2, 220, 1060, "จอห์น เอฟ. เคนเนดี", "ประธานาธิบดีสหรัฐฯ", side=1)
        if t > L[2] - 0.2:
            with g.at(CX, 1060, ap(t, L[2] + 0.2)):
                g.rrect(-150, -60, 300, 120, 30, GOLD2, 6)
                g.text("จุดเปลี่ยน", 0, 0, 52, "kanit", INK)
            title(g, t, L[2], "จุดเปลี่ยนสำคัญ", GREEN, 92)
        else:
            title(g, t, L[1], "สองมหาอำนาจตระหนักถึงหายนะ", INK, 78)
        return
    if t < L[4] - 0.2:   # ห้ามทดลองในบรรยากาศ อวกาศ ใต้น้ำ
        for i, (lab, col) in enumerate((("บรรยากาศ", hexc("#8fb8de")), ("อวกาศ", NAVY), ("ใต้น้ำ", hexc("#3f8ab8")))):
            x = 240 + i * 300
            k = ap(t, L[3] + 0.5 * i)
            if k < 0.02:
                continue
            with g.at(x, 860, k):
                g.circle(0, 0, 120, col, 6)
                if i == 0:
                    g.blob(-10, 10, 60, 34, WHITE, 4, seed=3)
                elif i == 1:
                    for j in range(5):
                        g.star(-60 + j * 30, -40 + (j * 37) % 80, 12, GOLD2, 0)
                else:
                    for j in range(3):
                        g.line([(-80, -30 + j * 30), (80, -30 + j * 30)], 6, WHITE, amp=0, smooth=True)
                g.line([(-90, -90), (90, 90)], 18, RED, amp=0)
            g.label(lab, x, 1040, 56, color=INK, sc=k)
        title(g, t, L[3], "ห้ามทดลองอาวุธนิวเคลียร์", RED, 86)
        return
    treaty(g, 400, 880, 0.75 * ap(t, L[4]) + 0.01, -4)   # PTBT 1963
    g.label("1963", 400, 590, 80, color=GOLDTXT, sc=ap(t, L[4] + 0.5))
    dove(g, 780, 760 + 15 * math.sin(t * 2), 1.2, t)
    g.label("อีก 2 ปีต่อมา", 780, 1100, 64, color=GREEN, sc=ap(t, L[4] + 1.0))
    title(g, t, L[4], "Partial Test Ban Treaty", INK, 76)


# ------------------------------------------------------------------ 7. lesson
def s_lesson(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:
        with g.at(CX, 860, ap(t, L[0]), -3):   # สมุดบันทึก
            g.rrect(-220, -160, 440, 320, 20, hexc("#e8d6a8"), 7)
            g.line([(0, -160), (0, 160)], 6, INK, amp=0)
            g.text("บทเรียน", -110, 0, 50, "kanit", INK)
            trefoil(g, 110, 0, 70)
        title(g, t, L[0], "เรื่องนี้เตือนใจเราว่า...", INK, 88)
        return
    if t < L[3] - 0.2:   # พลังเทพเจ้าในมือมนุษย์ / ขาดสติ
        bad = t > L[2] - 0.2
        shake = 6 * math.sin(t * 30) * seg(t, L[2], L[2] + 1)
        hands(g, CX + shake, 1100, 1.2)
        atom(g, CX + shake, 820, 170, t * (2.5 if bad else 1), 1.0)
        if bad:
            g.circle(CX, 820, 230, (0.85, 0.2, 0.2, 0.2), 0)
            title(g, t, L[2], "ถ้าขาดสติ ยับยั้งชั่งใจ...", RED, 86)
        else:
            title(g, t, L[1], "พลังเทพเจ้าในมือมนุษย์", GOLDTXT, 86)
        return
    globe(g, CX, 860, 250, t)   # บ้านหลังเดียวของเรา
    with g.at(CX, 610, ap(t, L[3] + 0.2)):
        g.poly([(-90, 0), (0, -80), (90, 0)], RED, 6, amp=0)
    time_bomb(g, 830, 1150, 0.5, t, 1 - seg(t, L[3], L[3] + d))
    title(g, t, L[3], "บ้านหลังเดียวของเรา", INK, 90)


# ------------------------------------------------------------------ 8. outro
def s_outro(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:
        mushroom(g, 330, 1240, 520, 1.0, t, 0.4, 0.8)
        g.label("?", 760, 800 + 15 * math.sin(t * 3), 260, color=RED, sc=ap(t, L[0] + 0.2))
        title(g, t, L[0] if t < L[1] - 0.2 else L[1], "รู้สึกอย่างไรกันบ้าง?", INK, 92)
        return
    if t < L[5] - 0.2:   # เกราะป้องกัน หรือ ระเบิดเวลา
        tilt = 8 * math.sin(t * 1.5)
        pans = balance(g, CX, 1230, 1.0, tilt)
        if t > L[3] - 0.2:
            shield(g, pans[0][0], pans[0][1] - 150, 0.85 * ap(t, L[3]) + 0.01)
        if t > L[4] - 0.2:
            time_bomb(g, pans[1][0], pans[1][1] - 150, 0.75 * ap(t, L[4]) + 0.01, t, 0.6)
        if t < L[3] - 0.2:
            missile(g, CX, 700, 0.7, 4 * math.sin(t * 2))
            title(g, t, L[2], "ความน่าสะพรึงของนิวเคลียร์", RED, 80)
        elif t < L[4] - 0.2:
            chip(g, 300, 600, "เกราะป้องกัน?", US, ap(t, L[3] + 0.3), -4, 360)
            title(g, t, L[3], "กันสงครามโลกครั้งที่ 3?", US, 86)
        else:
            chip(g, 300, 600, "เกราะป้องกัน?", US, 1, -4, 360)
            chip(g, 780, 600, "ระเบิดเวลา?", RED, ap(t, L[4] + 0.3), 4, 340)
            title(g, t, L[4], "หรือระเบิดเวลา?", RED, 92)
        return
    with g.at(CX + 170, 640, ap(t, L[5])):   # ชวนคอมเมนต์
        g.bubble(0, 0, 460, 220, WHITE, tail=(-1, 1))
        for i in range(3):
            g.circle(-110 + i * 110, 0, 24 + 6 * math.sin(t * 6 - i), INK, 0)
    dove(g, 300, 760 + 15 * math.sin(t * 2), 1.2, t)
    title(g, t, L[5], "มาแลกเปลี่ยนกันในคอมเมนต์!", RED, 70)


SCENES = {
    "hook": s_hook, "coldwar": s_coldwar, "flight": s_flight, "blast": s_blast, "damage": s_damage,
    "treaty": s_treaty, "lesson": s_lesson, "outro": s_outro,
}
NO_IRIS = set()
