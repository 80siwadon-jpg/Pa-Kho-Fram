"""ฉากตอน: 30 ต.ค. 1974 The Rumble in the Jungle — อาลีพลิกน็อกโฟร์แมนด้วย Rope-a-dope"""
import math
import os
import sys

import cairo

sys.path.insert(0, os.path.dirname(__file__))
from chars import (ALI, ALI_SUIT, BLUE_C, FOREMAN, PUNDITS, RED_C, REFEREE, africa, battery, bell, belt,  # noqa: E402
                   count_card, crowd, globe, hammer, heat, impact, jungle, punch_bag, ring, stars, tv)
from gfx import GOLD, GOLD2, GREY, INK, NAVY, RED, W, WHITE, e_io, e_out, hexc, lerp, pop, seg  # noqa: E402
from people import person  # noqa: E402

CX = W / 2
GROUND = 1270
FLOOR = 1180    # พื้นเวที
GOLDTXT = hexc("#b37a12")
NIGHTTXT = hexc("#f2c94c")
GREEN = hexc("#3c8d4f")
NIGHT = hexc("#1d2a44")

CAMERA = {"hook": "push_in", "kinshasa": "pan_right", "fighters": "pan_left", "ropes": "dutch", "plan": "push_in",
          "ko": "push_in", "lesson": "pull_out", "outro": "pan_right"}
TRANSITIONS = {"kinshasa": "zoom", "fighters": "whip", "ropes": "zoom", "plan": "fade", "ko": "whip",
               "lesson": "iris", "outro": "whip"}


def ap(t, a, dur=0.38):
    return pop(t, a - 0.2, dur)


def title(g, t, a, txt, col=INK, size=84, y=380):
    g.label(txt, CX, y, size, color=col, sc=ap(t, a), rot=-3)


def arena(g, t, k=1.0, cheer=1.0, lights=True):
    """สนามยามค่ำ: แผงกรมท่า + ไฟสปอตไลต์ + ฝูงชน"""
    c = g.c
    lg = cairo.LinearGradient(0, 160, 0, GROUND)
    lg.add_color_stop_rgba(0, *NIGHT[:3], 0.95 * k)
    lg.add_color_stop_rgba(1, *NIGHT[:3], 0.45 * k)
    c.set_source(lg)
    c.rectangle(-600, 140, 2300, GROUND - 140)
    c.fill()
    if lights:
        for i, x in enumerate((180, 900)):
            c.save()
            c.new_path()
            c.move_to(x - 30, 170)
            c.line_to(x + 30, 170)
            c.line_to(CX + 260 * (1 if i else -1) * 0.2 + 300, 1150)
            c.line_to(CX - 300 + 260 * (1 if i else -1) * 0.2, 1150)
            c.close_path()
            c.set_source_rgba(1, 0.95, 0.75, 0.10 * k)
            c.fill()
            c.restore()
            g.circle(x, 175, 22, (1, 0.95, 0.7, k), 4)
    crowd(g, 900, t, 14, 0.9 * k, cheer)


def ali(g, x, sc=0.8, mood="smug", pose="guard", turn=0.3, talk=False, lean=0.0, look=ALI):
    person(g, x, FLOOR, look, sc, mood=mood, pose=pose, turn=turn, seed=1, talk=talk, lean=lean)


def foreman(g, x, sc=0.8, mood="angry", pose="guard", turn=-0.3, talk=False, lean=0.0, y=FLOOR):
    person(g, x, y, FOREMAN, sc, mood=mood, pose=pose, turn=turn, seed=2, talk=talk, lean=lean)


def chip(g, x, y, txt, col, k, rot=0.0, w=320):
    if k < 0.02:
        return
    with g.at(x, y, k, rot):
        g.rrect(-w / 2, -64, w, 128, 40, WHITE, 7, stroke=col)
        g.label(txt, 0, 0, 52, color=col)


def ropes_fight(g, t, t0, sag=1.0, hits=True, talk=False):
    """อาลีพิงเชือกซ้าย การ์ดแน่น — โฟร์แมนระดมหมัด"""
    ring(g, FLOOR, t, sag)
    lean = -8 * sag + 2 * math.sin(t * 9) * sag
    ali(g, 290, 0.74, "smug", "guard", 0.4, talk=talk, lean=lean)
    ph = (t * 3) % 1
    foreman(g, 690, 0.78, "angry", "punch" if ph < 0.5 else "guard", -0.4, lean=4 * math.sin(t * 6))
    if hits and ph < 0.5:
        impact(g, 400, 820 + 80 * math.sin(t * 7), 0.6, t, 1.0)


# ------------------------------------------------------------------ 1. hook
def s_hook(g, t, L, d):
    if t < L[1] - 0.2:   # วันนี้ในอดีต: สนามมวยยามค่ำ
        arena(g, t)
        ring(g, FLOOR, t)
        bell(g, CX, 700, 0.9, t, 1.0)
        title(g, t, L[0] + 0.2, "วันนี้ในอดีต...", NIGHTTXT, 100)
        return
    if t < L[2] - 0.2:   # ชายวัย 32 ที่เซียนฟันธงว่าจะโดนต่อยดับ
        g.ground(GROUND, WHITE)
        ali(g, 280, 0.74, "smug", "cross", 0.3, look=ALI)
        for i, lk in enumerate(PUNDITS):
            person(g, 640 + i * 230, GROUND, lk, 0.62, mood="shout", pose="point", turn=-0.5, seed=10 + i,
                   talk=True)
        g.label("32 ปี", 560, 600, 80, color=GOLDTXT, sc=ap(t, L[1] + 0.3), rot=-5)
        title(g, t, L[1] + 0.2, "\"ต่อยดับคาสังเวียน!\"", RED, 92)
        return
    arena(g, t, 0.9)
    if t < L[3] - 0.2:   # พิงเชือกให้ทุบจนหมดแรง
        ropes_fight(g, t, L[2])
        title(g, t, L[2], "ยืนพิงเชือกให้ทุบ!", NIGHTTXT, 96)
        return
    if t < L[4] - 0.2:   # พลิกน็อก
        ring(g, FLOOR, t)
        u = e_out(seg(t, L[3], L[3] + 0.8))
        ali(g, 300, 0.74, "shout", "punch" if u < 0.8 else "v", 0.4)
        foreman(g, 760, 0.62, "shock", "down", -0.4, lean=lerp(0, -82, u))
        impact(g, 520, 720, 1.0, t, 1 - seg(t, L[3] + 0.5, L[3] + 1.2))
        a = math.radians(lerp(0, -82, u))
        stars(g, 760 + 560 * math.sin(a), FLOOR - 560 * math.cos(a) - 40, t, 90, 5, u)
        title(g, t, L[3], "พลิกน็อก!", NIGHTTXT, 120)
        return
    ring(g, FLOOR, t)   # ศึกที่ยิ่งใหญ่ที่สุด
    ali(g, CX, 0.84, "shout", "v", 0.0)
    belt(g, CX, 560, 0.75 * ap(t, L[4] + 0.4) + 0.01, -4, 1, t)
    title(g, t, L[4], "ศึกมวยที่ยิ่งใหญ่ที่สุด!", NIGHTTXT, 88, 330)


# ------------------------------------------------------------------ 2. kinshasa
def s_kinshasa(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:   # เช้ามืด 30 ต.ค. 1974
        arena(g, t, 0.9, 0.3, lights=False)
        with g.at(CX, 760, ap(t, L[0]), -3 + 2 * math.sin(t)):
            g.rrect(-200, -190, 400, 380, 30, WHITE, 8)
            g.rrect(-200, -190, 400, 100, 30, RED_C, 8)
            g.text("ต.ค. 1974", 0, -140, 50, "kanit", WHITE)
            g.text("30", 0, 10, 150, "kanit", INK)
            g.text("ตี 4", 0, 130, 44, "kanitsb", GREY)
        title(g, t, L[0], "เช้ามืด 30 ตุลาคม 1974", NIGHTTXT, 86)
        return
    if t < L[3] - 0.2:   # กินชาซา ซาอีร์ (คองโก)
        africa(g, CX, 830, 1.15, ap(t, L[1] + 0.4), t)
        g.label("กินชาซา", CX + 170, 780, 64, color=RED_C, sc=ap(t, L[1] + 0.8))
        if t > L[2] - 0.2:
            chip(g, CX, 1180, "ซาอีร์ = คองโก (DRC)", GREEN, ap(t, L[2]), -3, 520)
        title(g, t, L[1], "กรุงกินชาซา ประเทศซาอีร์", INK, 84)
        return
    if t < L[4] - 0.2:   # 6 หมื่นในสนาม + พันล้านทั่วโลก
        arena(g, t, 1.0, 1.0)
        ring(g, FLOOR, t)
        g.label("60,000 คน", 300, 600, 70, color=NIGHTTXT, sc=ap(t, L[3] + 0.2), rot=-4)
        globe(g, 800, 620, 110 * ap(t, L[3] + 1.2) + 1, t)
        g.label("1,000,000,000+", 760, 780, 50, color=NIGHTTXT, sc=ap(t, L[3] + 1.5))
        title(g, t, L[3], "ทั้งโลกเฝ้ารอชม!", NIGHTTXT, 96)
        return
    arena(g, t, 1.0, 1.0)   # ชิงแชมป์เฮฟวี่เวต: The Rumble in the Jungle
    jungle(g, GROUND, t, 0.9)
    ring(g, FLOOR, t)
    belt(g, CX, 800, 0.9 * ap(t, L[4] + 0.2) + 0.01, 0, 1, t)
    if t > L[5] - 0.2:
        with g.at(CX, 560, ap(t, L[5] + 0.3), -4):
            g.rrect(-380, -80, 760, 160, 30, hexc("#2f6a3a"), 7)
            g.text("THE RUMBLE", 0, -28, 64, "kanit", NIGHTTXT)
            g.text("IN THE JUNGLE", 0, 38, 50, "kanit", WHITE)
    else:
        title(g, t, L[4], "ชิงแชมป์โลกรุ่นเฮฟวี่เวต", NIGHTTXT, 86)


# ------------------------------------------------------------------ 3. fighters
def s_fighters(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # มุมแดง: โฟร์แมน
        c = g.c
        c.rectangle(-600, 140, 2300, GROUND - 140)
        c.set_source_rgba(*RED_C[:3], 0.12)
        c.fill()
        foreman(g, 330, 0.88, "angry", "fist" if t < L[1] - 0.2 else "punch", 0.2, y=GROUND)
        g.name_tag(t, L[0] + 0.1, 330, 1080, "จอร์จ โฟร์แมน", "แชมป์โลกไร้พ่าย วัย 25", side=1)
        if t > L[1] - 0.2:
            hammer(g, 780, 900, 1.1, 20 * math.sin(t * 5))
            for i in range(2):
                chip(g, 790, 600 + i * 0, "KO ≤ 2 ยก", RED_C, ap(t, L[1] + 0.6), 4, 330) if i == 0 else None
            title(g, t, L[1], "สัตว์ประหลาดหมัดเหล็ก!", RED_C, 90)
        else:
            chip(g, 780, 700, "มุมแดง", RED_C, ap(t, L[0] + 0.3), 4)
            title(g, t, L[0], "มุมแดง: จอร์จ โฟร์แมน", RED_C, 86)
        return
    if t < L[4] - 0.2:   # มุมน้ำเงิน: อาลี / ถูกริบเข็มขัด แบน
        c = g.c
        c.rectangle(-600, 140, 2300, GROUND - 140)
        c.set_source_rgba(*BLUE_C[:3], 0.10)
        c.fill()
        if t < L[3] - 0.2:
            ali(g, 300, 0.74, "smug", "cross", 0.3, look=ALI)
            g.name_tag(t, L[2] + 0.1, 300, 1080, "มูฮัมหมัด อาลี", "อดีตแชมป์โลก วัย 32", side=1)
            chip(g, 780, 700, "มุมน้ำเงิน", BLUE_C, ap(t, L[2] + 0.3), 4)
            title(g, t, L[2], "มุมน้ำเงิน: มูฮัมหมัด อาลี", BLUE_C, 84)
        else:
            person(g, 300, GROUND, ALI_SUIT, 0.84, mood="firm", pose="stop", turn=0.3, seed=1, talk=True)
            belt(g, 760, 760, 0.6, 8)
            k = ap(t, L[3] + 0.5)
            if k > 0.02:
                g.line([(560, 620), (960, 900)], 22 * k, RED, amp=0)
            chip(g, 760, 1080, "แบน 1967–1970", RED, ap(t, L[3] + 1.0), -4, 380)
            title(g, t, L[3], "ถูกริบเข็มขัด แบนหลายปี", INK, 86)
        return
    for i, lk in enumerate(PUNDITS):   # เซียนมวยฟันธง
        person(g, 220 + i * 230, GROUND, lk, 0.68, mood="shout" if t > L[6] - 0.2 else "firm",
               pose="point" if i == 0 else "shrug", turn=0.4, seed=10 + i, talk=True)
    if t < L[5] - 0.2:
        g.label("?", 830, 760, 200, color=GREY, sc=ap(t, L[4] + 0.3))
        title(g, t, L[4], "เซียนมวยลงความเห็นตรงกัน", INK, 84)
        return
    if t < L[6] - 0.2:
        chip(g, 820, 640, "แก่เกินไป", RED, ap(t, L[5]), -4, 300)
        chip(g, 820, 840, "ช้าเกินไป", RED, ap(t, L[5] + 1.0), 4, 300)
        title(g, t, L[5], "อาลีหมดยุคแล้ว?", RED, 92)
        return
    with g.at(820, 760, ap(t, L[6]), 6 * math.sin(t * 3)):
        g.circle(0, 0, 150, WHITE, 7)
        g.text("!!", 0, 0, 140, "kanit", RED)
    title(g, t, L[6], "\"โดนต่อยตายคาเวที\"!", RED, 92)


# ------------------------------------------------------------------ 4. ropes
def s_ropes(g, t, L, d):
    arena(g, t, 1.0, 1.0)
    if t < L[1] - 0.2:   # ระฆังดัง
        ring(g, FLOOR, t)
        bell(g, CX, 720, 1.1, t, 1.0)
        title(g, t, L[0], "เสียงระฆังดังขึ้น!", NIGHTTXT, 96)
        return
    if t < L[3] - 0.2:   # อาลี โบมาเย!
        crowd(g, 1150, t, 12, 1.0, 1.5, (0.25, 0.28, 0.38))
        with g.at(CX, 720, ap(t, L[1] + 0.3), -4 + 3 * math.sin(t * 6)):
            g.rrect(-380, -110, 760, 220, 40, RED_C, 8)
            g.text("อาลี โบมาเย!", 0, 0, 96, "kanit", WHITE)
        if t > L[2] - 0.2:
            g.label("= อาลี ฆ่ามัน!", CX, 930, 70, color=NIGHTTXT, sc=ap(t, L[2] + 0.2))
        title(g, t, L[1], "แฟนมวยทั้งสนามตะโกน", NIGHTTXT, 86)
        return
    if t < L[5] - 0.2:   # ไม่มีใครคาดคิด / ไม่เต้นฟุตเวิร์ก
        ring(g, FLOOR, t)
        foreman(g, 760, 0.76, "angry", "guard", -0.4)
        if t > L[4] - 0.2:
            ali(g, 330, 0.76, "firm", "guard", 0.4, lean=0)
            g.label("ฟุตเวิร์ก?", 330, 560, 70, color=NIGHTTXT, sc=ap(t, L[4] + 0.3))
            k = ap(t, L[4] + 0.9)
            if k > 0.02:
                g.line([(200, 540), (460, 590)], 14 * k, RED, amp=0)
            title(g, t, L[4], "ไม่เต้นพริ้วเหมือนในอดีต", NIGHTTXT, 84)
        else:
            ali(g, 330 + 40 * math.sin(t * 6), 0.76, "smug", "guard", 0.4)
            g.label("?", CX, 640, 160, color=NIGHTTXT, sc=ap(t, L[3] + 0.2))
            title(g, t, L[3], "สิ่งที่ไม่มีใครคาดคิด...", NIGHTTXT, 88)
        return
    if t < L[7] - 0.2:   # ถอยพิงเชือก โฟร์แมนระดมหมัด
        sag = e_io(seg(t, L[5] - 0.2, L[5] + 0.8))
        ropes_fight(g, t, L[5], sag, t > L[6] - 0.2)
        if t > L[6] - 0.2:
            hammer(g, 860, 620, 0.6, 30 * math.sin(t * 12))
            title(g, t, L[6], "หมัดหนักราวค้อนปอนด์!", NIGHTTXT, 88)
        else:
            title(g, t, L[5], "ถอยพิงเชือก ยกการ์ดแน่น", NIGHTTXT, 86)
        return
    ropes_fight(g, t, L[7], 1.0, True, talk=True)   # กระซิบเย้ย
    with g.at(380, 560, ap(t, L[7] + 0.4)):
        g.bubble(0, 0, 500, 200, WHITE, tail=(-1, 1))
        g.text("แค่นี้เหรอ จอร์จ?", 0, 0, 52, "kanit", INK)
    title(g, t, L[7], "กระซิบเย้ยข้างหู", NIGHTTXT, 90, 330)


# ------------------------------------------------------------------ 5. plan
def s_plan(g, t, L, d):
    if t < L[1] - 0.2:   # Rope-a-dope
        arena(g, t, 0.9, 0.5)
        ropes_fight(g, t, L[0], 1.0)
        with g.at(CX, 560, ap(t, L[0] + 0.6), -5):
            g.rrect(-320, -80, 640, 160, 30, GOLD2, 7)
            g.text("ROPE-A-DOPE", 0, 0, 80, "kanit", INK)
        return
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # เชือกช่วยซับแรง (ภาพขยาย)
        ring(g, GROUND, t, 0.5 + 0.5 * math.sin(t * 4))
        for i in range(3):
            u = (t * 1.5 + i / 3) % 1
            g.arc(200, 900, 80 + 160 * u, -60, 60, 8, (*GREEN[:3], 1 - u))
        chip(g, 700, 620, "เชือกช่วยซับแรง", GREEN, ap(t, L[1] + 0.4), 4, 420)
        title(g, t, L[1], "อาศัยความหย่อนของเชือก", INK, 86)
        return
    if t < L[3] - 0.2:   # ยอมเจ็บ กัดฟันทน
        punch_bag(g, 330, 1150, 1.1, t, 1.0)
        ph = (t * 3) % 1
        if ph < 0.5:
            impact(g, 420, 950, 0.6, t, 1)
        ali(g, 760, 0.8, "firm", "guard", -0.3)
        g.label("ทน!", 760, 520, 90, color=RED, sc=ap(t, L[2] + 0.5), rot=5)
        title(g, t, L[2], "ยอมเจ็บ กัดฟันทน", INK, 92)
        return
    if t < L[4] - 0.2:   # ล่อให้โฟร์แมนหมดก๊อก
        foreman(g, 330, 0.84, "angry", "punch" if (t * 2) % 1 < 0.5 else "guard", 0.3, y=GROUND)
        lv = 1 - e_io(seg(t, L[3], L[4]))
        battery(g, 760, 760, 1.0, max(0.05, lv))
        title(g, t, L[3], "ระบายพลังจนหมดก๊อก!", RED, 90)
        return
    jungle(g, GROUND, t)   # ร้อนชื้น อบอ้าว
    g.sunburst(CX, 700, 130, 260, 16, t * 6, 10, (1, 0.7, 0.3, 0.6))
    g.circle(CX, 700, 110, GOLD2, 6)
    heat(g, CX, 1100, t, 3)
    with g.at(CX, 1000, ap(t, L[4] + 0.6)):
        g.rrect(-130, -60, 260, 120, 24, WHITE, 6, stroke=RED)
        g.text("ร้อนชื้น", 0, 0, 56, "kanit", RED)
    title(g, t, L[4], "ป่าดงดิบแอฟริกา ร้อนอบอ้าว!", RED, 84)


# ------------------------------------------------------------------ 6. ko
def s_ko(g, t, L, d):
    arena(g, t, 1.0, 1.0)
    if t < L[1] - 0.2:   # ยกที่ 8
        ring(g, FLOOR, t)
        with g.at(CX, 760, ap(t, L[0]), -4 + 3 * math.sin(t * 2)):
            g.rrect(-200, -200, 400, 400, 30, WHITE, 8)
            g.text("ยก", 0, -110, 60, "kanit", INK)
            g.text("8", 0, 40, 220, "kanit", RED_C)
        return
    if t < L[3] - 0.2:   # โฟร์แมนหมดแรง
        ring(g, FLOOR, t, 0.6)
        ali(g, 290, 0.74, "smug", "guard", 0.4, lean=-6)
        foreman(g, 690, 0.78, "worry", "down", -0.4, lean=6 + 4 * math.sin(t * 1.5))
        for i in range(3):   # เหงื่อ
            u = (t * 0.9 + i / 3) % 1
            g.circle(640 + i * 50, 480 + 120 * u, 10, (0.55, 0.8, 1, 1 - u), 3)
        battery(g, 830, 600, 0.5, 0.12)
        if t > L[2] - 0.2:
            title(g, t, L[2], "หมดแรงอย่างเห็นได้ชัด...", NIGHTTXT, 86, 330)
        else:
            title(g, t, L[1], "หมัดช้าลง ขาก้าวไม่ออก", NIGHTTXT, 86, 330)
        return
    if t < L[6] - 0.2:   # ดีดออกจากเชือก คอมโบ ฮุกขวา
        ring(g, FLOOR, t, 1 - e_out(seg(t, L[3] - 0.2, L[3] + 0.4)))
        dx = 140 * e_out(seg(t, L[3] - 0.2, L[3] + 0.6))
        combo = t > L[4] - 0.2
        ph = (t * 4) % 1
        ali(g, 290 + dx, 0.78, "shout", "punch" if (combo and ph < 0.5) or t > L[5] - 0.2 else "guard", 0.4)
        foreman(g, 760, 0.7, "shock", "down", -0.4, lean=-6 if combo else 4)
        if combo and (ph < 0.5 or t > L[5] - 0.2):
            impact(g, 590, 640 + (0 if t > L[5] - 0.2 else 80 * math.sin(t * 9)), 0.8 if t < L[5] - 0.2 else 1.2,
                   t, 1)
        if t > L[5] - 0.2:
            title(g, t, L[5], "ฮุกขวาเต็มขากรรไกร!", NIGHTTXT, 92, 330)
        elif combo:
            title(g, t, L[4], "ชุดหมัดคอมโบ!", NIGHTTXT, 100, 330)
        else:
            title(g, t, L[3], "ดีดตัวออกจากเชือก!", NIGHTTXT, 96, 330)
        return
    if t < L[7] - 0.2:   # โฟร์แมนหมุนคว้างล้ม
        ring(g, FLOOR, t)
        u = e_io(seg(t, L[6] - 0.2, L[6] + 1.2))
        ali(g, 300, 0.74, "smug", "guard", 0.4)
        lean = lerp(-6, -86, u)
        foreman(g, 760, lerp(0.7, 0.62, u), "shock", "down", -0.4, lean=lean)
        a = math.radians(lean)
        stars(g, 760 + 560 * math.sin(a), FLOOR - 560 * math.cos(a) - 40, t, 90, 5, 1)
        title(g, t, L[6], "โฟร์แมนล้มคว่ำ!", NIGHTTXT, 100, 330)
        return
    if t < L[8] - 0.2:   # กรรมการนับสิบ
        ring(g, FLOOR, t)
        person(g, 860, FLOOR, REFEREE, 0.72, mood="firm", pose="stop", turn=-0.4, seed=7, talk=True)
        foreman(g, 760, 0.62, "shock", "down", -0.4, lean=-86)
        stars(g, 200, FLOOR - 80, t, 80, 5, 1)
        n = min(10, 1 + int(seg(t, L[7] - 0.1, L[8] - 0.4) * 10))
        count_card(g, 500, 620, n, 0.9)
        title(g, t, L[7], "กรรมการนับสิบ!", NIGHTTXT, 96, 330)
        return
    ring(g, FLOOR, t)   # ทวงบัลลังก์
    ali(g, CX, 0.84, "shout", "v", 0.0)
    belt(g, CX, 1220 - 100, 0.6 * ap(t, L[8] + 0.6) + 0.01, 0, 1, t)
    for i in range(10):
        u = (t * 0.6 + i / 10) % 1
        g.rrect(100 + (i * 97) % 880, 300 + 900 * u, 20, 30, 4, (GOLD2, RED_C, WHITE, BLUE_C)[i % 4], 0)
    title(g, t, L[8], "ทวงบัลลังก์แชมป์โลกคืน!", NIGHTTXT, 86, 330)


# ------------------------------------------------------------------ 7. lesson
def s_lesson(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:
        with g.at(CX, 860, ap(t, L[0]), -3 + 2 * math.sin(t * 1.5)):
            g.rrect(-380, -110, 760, 220, 30, hexc("#2f6a3a"), 7)
            g.text("THE RUMBLE IN THE JUNGLE", 0, 0, 50, "kanit", NIGHTTXT)
        title(g, t, L[0], "พิสูจน์ให้เห็นว่า...", INK, 96)
        return
    if t < L[3] - 0.2:   # กล้ามเนื้อไม่ใช่ทุกอย่าง
        foreman(g, 330, 0.84, "angry", "fist", 0.3, y=GROUND)
        if t > L[2] - 0.2:
            chip(g, 780, 700, "พละกำลัง ≠ ชัยชนะ", RED, ap(t, L[2] + 0.3), 4, 440)
            title(g, t, L[2], "กล้ามเนื้อไม่ใช่ทุกอย่าง", INK, 88)
        else:
            impact(g, 780, 760, 0.8, t, 1)
            title(g, t, L[1], "ในการต่อสู้ที่ดุเดือดที่สุด", INK, 86)
        return
    if t < L[4] - 0.2:   # สติปัญญา ความอดทน ใจไม่ยอมแพ้
        ali(g, 280, 0.8, "smug", "think", 0.3, look=ALI)
        for i, (txt, col) in enumerate((("สติปัญญา", NAVY), ("ความอดทน", GREEN), ("ใจไม่ยอมแพ้", RED))):
            chip(g, 760, 560 + i * 200, txt, col, ap(t, L[3] + 0.5 * i), 4 - 4 * i, 360)
        return
    ali(g, CX, 0.84, "smile", "v", 0.0)   # ตำนานเหนือกาลเวลา
    for i in range(8):
        a = i * 0.785 + t * 0.6
        g.star(CX + 360 * math.cos(a), 720 + 220 * math.sin(a), 30, GOLD2, 4)
    title(g, t, L[4], "ผู้เป็นรอง → ตำนาน", GOLDTXT, 96, 330)


# ------------------------------------------------------------------ 8. outro
def s_outro(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:
        ali(g, 300, 0.8, "smug", "guard", 0.3)
        g.label("?", 760, 760 + 15 * math.sin(t * 3), 220, color=RED, sc=ap(t, L[0] + 0.2))
        with g.at(760, 1050, ap(t, L[1])):
            g.rrect(-220, -50, 440, 100, 24, GOLD2, 6)
            g.text("ROPE-A-DOPE", 0, 0, 52, "kanit", INK)
        title(g, t, L[0] if t < L[1] - 0.2 else L[1], "รู้สึกอย่างไรกันบ้าง?", INK, 92)
        return
    if t < L[5] - 0.2:   # อัจฉริยะ หรือ เสี่ยงตาย
        punch_bag(g, CX, 1150, 1.0, t, 1.0)
        if t > L[3] - 0.2:
            chip(g, 270, 640, "อัจฉริยะ?", GOLDTXT, ap(t, L[3] + 0.2), -4, 300)
        if t > L[4] - 0.2:
            chip(g, 810, 820, "เสี่ยงตาย?", RED, ap(t, L[4] + 0.2), 4, 300)
        title(g, t, L[2] if t < L[3] - 0.2 else (L[3] if t < L[4] - 0.2 else L[4]),
              "ยอมเป็นกระสอบทราย..." if t < L[3] - 0.2 else ("ความอัจฉริยะระดับตำนาน?" if t < L[4] - 0.2
                                                        else "หรือเดิมพันที่เสี่ยงตาย?"),
              INK if t < L[3] - 0.2 else (GOLDTXT if t < L[4] - 0.2 else RED), 84)
        return
    with g.at(CX + 170, 640, ap(t, L[5])):   # ชวนคอมเมนต์
        g.bubble(0, 0, 460, 220, WHITE, tail=(-1, 1))
        for i in range(3):
            g.circle(-110 + i * 110, 0, 24 + 6 * math.sin(t * 6 - i), INK, 0)
    ali(g, 260, 0.7, "smile", "wave", 0.3)
    title(g, t, L[5], "มาแลกเปลี่ยนกันในคอมเมนต์!", RED, 70)


SCENES = {
    "hook": s_hook, "kinshasa": s_kinshasa, "fighters": s_fighters, "ropes": s_ropes, "plan": s_plan, "ko": s_ko,
    "lesson": s_lesson, "outro": s_outro,
}
NO_IRIS = set()
