"""ฉากตอน: 30 ต.ค. 1960 วันเกิดดีเอโก มาราโดนา — จากสลัมสู่หัตถ์พระเจ้าและประตูแห่งศตวรรษ"""
import math
import os
import sys

import cairo

sys.path.insert(0, os.path.dirname(__file__))
from chars import (ARG, ENGLAND, FANS, KEEPER, KID, MARADONA, MARADONA_NAP, NAP, TEEN, ball, falklands,  # noqa: E402
                   goal, halo, hand_ball, headline, heart, horns, italy, jersey, pitch, scudetto, shack, slum,
                   sword, trophy, vesuvius)
from gfx import GOLD, GOLD2, GREY, INK, NAVY, RED, W, WHITE, e_io, e_out, hexc, lerp, pop, seg  # noqa: E402
from people import person  # noqa: E402

CX = W / 2
GROUND = 1270
GOLDTXT = hexc("#b37a12")
NIGHTTXT = hexc("#f2c94c")
GREEN = hexc("#3c8d4f")
NIGHT = hexc("#1d2a44")
ARGTXT = hexc("#3a7ab8")

CAMERA = {"hook": "push_in", "fiorito": "pan_right", "mexico": "push_in", "hand": "dutch", "goal": "pan_left",
          "napoli": "pan_right", "dark": "push_in", "lesson": "pull_out", "outro": "pan_right"}
TRANSITIONS = {"fiorito": "zoom", "mexico": "whip", "hand": "zoom", "goal": "whip", "napoli": "iris", "dark": "fade",
               "lesson": "zoom", "outro": "whip"}


def ap(t, a, dur=0.38):
    return pop(t, a - 0.2, dur)


def title(g, t, a, txt, col=INK, size=84, y=380):
    g.label(txt, CX, y, size, color=col, sc=ap(t, a), rot=-3)


def diego(g, x, sc=0.84, mood="smile", pose="down", turn=0.3, look=MARADONA, talk=False):
    person(g, x, GROUND, look, sc, mood=mood, pose=pose, turn=turn, seed=1, talk=talk)


def chip(g, x, y, txt, col, k, rot=0.0, w=320):
    if k < 0.02:
        return
    with g.at(x, y, k, rot):
        g.rrect(-w / 2, -64, w, 128, 40, WHITE, 7, stroke=col)
        g.label(txt, 0, 0, 52, color=col)


def dark_panel(g, k=1.0):
    c = g.c
    lg = cairo.LinearGradient(0, 160, 0, GROUND)
    lg.add_color_stop_rgba(0, *NIGHT[:3], 0.95 * k)
    lg.add_color_stop_rgba(1, *NIGHT[:3], 0.45 * k)
    c.set_source(lg)
    c.rectangle(-600, 140, 2300, GROUND - 140)
    c.fill()


def kick_ball(g, x, y, t, r=50):
    ball(g, x, y - 60 * abs(math.sin(t * 4)), r, t * 3)


# ------------------------------------------------------------------ 1. hook
def s_hook(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:   # วันนี้ในอดีต: ลูกบอลเด้ง
        kick_ball(g, CX, 1150, t, 90)
        title(g, t, L[0] + 0.2, "วันนี้ในอดีต...", INK, 100)
        return
    if t < L[3] - 0.2:   # เด็กสลัมร่างเตี้ย / เท้าซ้ายร่ายเวทมนตร์
        slum(g, GROUND, t)
        person(g, 330, GROUND, KID, 0.9, mood="smile", pose="down", turn=0.3, seed=3)
        kick_ball(g, 470, GROUND - 40, t, 40)
        if t > L[2] - 0.2:
            for i in range(5):
                a = t * 3 + i * 1.25
                g.star(470 + 110 * math.cos(a), 1150 + 40 * math.sin(a), 18, GOLD2, 3)
            title(g, t, L[2], "เท้าซ้ายร่ายเวทมนตร์", GOLDTXT, 90)
        else:
            title(g, t, L[1], "เด็กสลัมจากบัวโนสไอเรส", INK, 86)
        return
    if t < L[4] - 0.2:   # มือซ้ายแห่งพระเจ้า
        hand_ball(g, CX, 1000, 1.3, t)
        halo(g, CX + 50, 520, 120)
        title(g, t, L[3], "\"มือซ้ายแห่งพระเจ้า\"", RED, 96)
        return
    diego(g, CX, 0.84, "smile", "v", 0.0)   # พระเจ้าที่มีลมหายใจ
    halo(g, CX, 470, 110)
    for i, lk in enumerate(FANS[:2]):
        person(g, 160 + i * 760, GROUND, lk, 0.58, mood="smile", pose="wave", turn=0.4 - 0.8 * i, seed=20 + i)
    title(g, t, L[4], "พระเจ้าของชาวอาร์เจนตินา!", ARGTXT, 84, 330)


# ------------------------------------------------------------------ 2. fiorito
def s_fiorito(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:   # 30 ต.ค. 1960
        with g.at(CX, 860, ap(t, L[0]), -3 + 2 * math.sin(t)):
            g.rrect(-200, -190, 400, 380, 30, WHITE, 8)
            g.rrect(-200, -190, 400, 100, 30, ARG, 8)
            g.text("ต.ค. 1960", 0, -140, 50, "kanit", WHITE)
            g.text("30", 0, 10, 150, "kanit", INK)
            g.text("อาทิตย์", 0, 130, 40, "kanitsb", GREY)
        title(g, t, L[0], "30 ตุลาคม 1960", ARGTXT, 92)
        return
    if t < L[3] - 0.2:   # วิลลา ฟิโอริโต สลัม
        slum(g, GROUND, t)
        with g.at(CX, 700, ap(t, L[1] + 0.2), -3):
            g.rrect(-230, -60, 460, 120, 14, WHITE, 6)
            g.text("VILLA FIORITO", 0, 0, 52, "kanit", INK)
        if t > L[2] - 0.2:
            title(g, t, L[2], "สลัมชานกรุงบัวโนสไอเรส", INK, 84)
        else:
            title(g, t, L[1], "วิลลา ฟิโอริโต", INK, 96)
        return
    if t < L[4] - 0.2:   # ดีเอโกลืมตาดูโลก
        with g.at(CX, 900, ap(t, L[3])):
            g.blob(0, 0, 160, 110, hexc("#f2ead6"), 6, seed=4)
            g.circle(-60, -20, 70, hexc("#c9946a"), 6)
            g.circle(-80, -30, 8, INK, 0)
            g.circle(-40, -30, 8, INK, 0)
            g.arc(-60, -5, 20, 20, 160, 5, INK)
        for i in range(5):
            a = t + i * 1.25
            g.star(CX + 260 * math.cos(a), 900 + 160 * math.sin(a), 22, GOLD2, 3)
        g.label("ดีเอโก อาร์มันโด มาราโดนา", CX, 1160, 64, color=ARGTXT, sc=ap(t, L[3] + 0.6))
        title(g, t, L[3], "ลืมตาดูโลก!", GOLDTXT, 100)
        return
    if t < L[5] - 0.2:   # บ้านดิน ไม่มีน้ำไฟ
        shack(g, CX, GROUND, 1.6)
        for i, (lab, x) in enumerate((("น้ำประปา", 260), ("ไฟฟ้า", 820))):
            k = ap(t, L[4] + 0.6 + 0.4 * i)
            chip(g, x, 620, lab, GREY, k, -4 + 8 * i, 260)
            if k > 0.5:
                g.line([(x - 120, 560), (x + 120, 680)], 12, RED, amp=0)
        title(g, t, L[4], "บ้านดิน ไม่มีน้ำ ไม่มีไฟ", INK, 88)
        return
    if t < L[7] - 0.2:   # ลูกบอลเก่าคือของเล่นชิ้นเดียว
        person(g, 300, GROUND, KID, 0.9, mood="smile", pose="down" if t < L[6] - 0.2 else "v", turn=0.3, seed=3)
        bx = lerp(460, 820, 0.5 + 0.5 * math.sin(t * 1.5)) if t > L[6] - 0.2 else 520
        kick_ball(g, bx, 1200, t, 60)
        if t > L[6] - 0.2:
            g.label("อวัยวะชิ้นที่ 33", 720, 700, 72, color=GOLDTXT, sc=ap(t, L[6] + 0.5), rot=4)
            title(g, t, L[6], "เตะไปทุกที่!", INK, 96)
        else:
            title(g, t, L[5], "ของเล่นชิ้นเดียว: ลูกบอลเก่า", INK, 84)
        return
    if t < L[8] - 0.2:   # ทีมชาติตั้งแต่ 16
        person(g, 330, GROUND, TEEN, 0.9, mood="smile", pose="point", turn=0.3, seed=4)
        jersey(g, 760, 820 + 15 * math.sin(t * 2), 1.1 * ap(t, L[7] + 0.3) + 0.01, WHITE, ARG, "10", ARG,
               6 * math.sin(t * 1.5))
        g.label("16 ปี", 760, 1120, 90, color=GOLDTXT, sc=ap(t, L[7] + 0.9), rot=-4)
        title(g, t, L[7], "ติดทีมชาติชุดใหญ่!", ARGTXT, 92)
        return
    diego(g, CX, 0.84, "smile", "wave", 0.0)   # ความหวังของคนทั้งประเทศ
    for i, lk in enumerate(FANS[:2]):
        person(g, 170 + i * 740, GROUND, lk, 0.6, mood="smile", pose="v" if i else "wave", turn=0.4 - 0.8 * i,
               seed=20 + i)
    title(g, t, L[8], "ความหวังของคนทั้งประเทศ", ARGTXT, 84)


# ------------------------------------------------------------------ 3. mexico
def s_mexico(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # ยอดเขาโอลิมปัส / ฟุตบอลโลก 1986 เม็กซิโก
        if t < L[1] - 0.2:
            c = g.c
            _mt = [(-300, GROUND), (CX - 80, 560), (CX + 80, 560), (1400, GROUND)]
            c.new_path()
            for p in _mt:
                c.line_to(*p)
            c.close_path()
            c.set_source_rgba(0.75, 0.78, 0.82, 1)
            c.fill_preserve()
            c.set_source_rgba(*INK)
            c.set_line_width(6)
            c.stroke()
            for i in range(5):
                a = t * 0.8 + i * 1.25
                g.star(CX + 160 * math.cos(a), 470 + 40 * math.sin(a), 24, GOLD2, 3)
            ball(g, CX, 500, 60, t)
            title(g, t, L[0], "ยอดเขาโอลิมปัสแห่งฟุตบอล", GOLDTXT, 84)
        else:
            trophy(g, CX, 1150, 1.4 * ap(t, L[1]) + 0.01, 0, t)
            with g.at(CX, 620, ap(t, L[1] + 0.5), -4):
                g.rrect(-260, -60, 520, 120, 24, hexc("#2f6a3a"), 6)
                g.text("MEXICO 1986", 0, 0, 60, "kanit", WHITE)
            title(g, t, L[1], "ฟุตบอลโลก 1986 เม็กซิโก", GREEN, 86)
        return
    if t < L[3] - 0.2:   # รอบ 8 ทีม พบอังกฤษ
        diego(g, 290, 0.8, "firm", "down", 0.4)
        person(g, 790, GROUND, ENGLAND[0], 0.82, mood="firm", pose="cross", turn=-0.4, seed=10)
        g.label("VS", CX, 900, 120, color=RED, sc=ap(t, L[2] + 0.3))
        g.name_tag(t, L[2] + 0.1, 290, 1080, "ดีเอโก มาราโดนา", "กัปตันทีมชาติอาร์เจนตินา", side=1)
        title(g, t, L[2], "รอบ 8 ทีม พบอังกฤษ!", RED, 92)
        return
    falklands(g, CX, 870, 1.0, t, ap(t, L[3] + 0.4))   # สงครามฟอล์กแลนด์
    title(g, t, L[3], "รอยแผลสงครามฟอล์กแลนด์ (1982)", RED, 78)


# ------------------------------------------------------------------ 4. hand
def s_hand(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:   # 4 นาที
        with g.at(CX, 860, ap(t, L[0])):
            g.circle(0, 0, 230, WHITE, 8)
            for i in range(12):
                a = i * math.pi / 6
                g.line([(200 * math.cos(a), 200 * math.sin(a)), (220 * math.cos(a), 220 * math.sin(a))], 6, INK,
                       amp=0)
            a = -math.pi / 2 + seg(t, L[0], L[1]) * math.pi * 0.4
            g.line([(0, 0), (170 * math.cos(a), 170 * math.sin(a))], 12, RED, amp=0)
            g.circle(0, 0, 16, INK, 0)
        g.label("4 นาที", CX, 1180, 90, color=RED, sc=ap(t, L[0] + 0.6))
        title(g, t, L[0], "ห่างกันเพียง 4 นาที", INK, 92)
        return
    if t < L[3] - 0.2:   # ปีศาจ + พระเจ้า
        diego(g, CX, 0.84, "smug" if t < L[2] - 0.2 else "smile", "shrug", 0.0)
        if t > L[1] - 0.2:
            horns(g, CX - 230, 640, ap(t, L[1] + 0.3) * 1.3 + 0.01)
            chip(g, 220, 620, "ปีศาจ", RED, ap(t, L[1] + 0.3), -6, 220)
        if t > L[2] - 0.2:
            halo(g, CX + 230, 560, 70 * ap(t, L[2] + 0.2) + 1)
            chip(g, 860, 620, "พระเจ้า", GOLDTXT, ap(t, L[2] + 0.3), 6, 220)
            title(g, t, L[2], "ความงดงามของพระเจ้า", GOLDTXT, 88)
        else:
            title(g, t, L[1], "ความเจ้าเล่ห์ของปีศาจ", RED, 90)
        return
    if t < L[4] - 0.2:   # กระโดดเทกตัว ใช้มือซ้ายปัด
        goal(g, 700, GROUND, 0.9, 1.0 if t > L[3] + 2.2 else 0, t)
        u = e_io(seg(t, L[3], L[3] + 2.2))
        person(g, 640, GROUND, KEEPER, 0.74, mood="shock", pose="v", turn=-0.3, seed=11)
        with g.at(0, -120 * math.sin(u * math.pi)):
            diego(g, 320, 0.74, "firm", "v", 0.4)
        if t < L[3] + 2.2:
            ball(g, lerp(380, 820, u), lerp(500, 1060, u) - 120 * math.sin(u * math.pi), 36, t * 4)
        title(g, t, L[3], "แอบใช้มือซ้ายปัด!", RED, 96)
        return
    hand_ball(g, CX - 120, 1000, 1.2, t)   # Hand of God
    halo(g, CX - 80, 560, 110)
    with g.at(CX + 230, 760, ap(t, L[4] + 0.5), 6):
        g.rrect(-180, -80, 360, 160, 24, GOLD2, 6)
        g.text("HAND", 0, -30, 56, "kanit", INK)
        g.text("OF GOD", 0, 34, 52, "kanit", INK)
    title(g, t, L[4], "\"หัตถ์ของพระเจ้า\"", GOLDTXT, 100)


# ------------------------------------------------------------------ 5. goal
def s_goal(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:   # อีก 4 นาที
        g.label("+4 นาที", CX, 860, 160, color=RED, sc=ap(t, L[0]), rot=-4 + 3 * math.sin(t * 3))
        kick_ball(g, CX, 1200, t, 50)
        return
    if t < L[2] - 0.2:   # ประตูแห่งศตวรรษ
        trophy(g, 260, 1150, 0.6, 0, t)
        with g.at(CX + 60, 820, ap(t, L[1] + 0.3), -4):
            g.rrect(-330, -110, 660, 220, 30, hexc("#2f6a3a"), 8)
            g.text("GOAL OF", 0, -40, 70, "kanit", NIGHTTXT)
            g.text("THE CENTURY", 0, 44, 66, "kanit", WHITE)
        title(g, t, L[1], "\"ประตูแห่งศตวรรษ\"", GREEN, 100)
        return
    if t < L[4] - 0.2:   # เลี้ยงเดี่ยว 60 หลา แหวก 5 คน (สนามมองจากบน)
        pitch(g, CX, 860, 940, 640, t)
        path = [(130, 900), (260, 860), (380, 960), (500, 840), (620, 940), (760, 860), (900, 860)]
        u = seg(t, L[2] - 0.2, L[4] - 0.4)
        n = u * (len(path) - 1)
        i0 = min(len(path) - 2, int(n))
        f = n - i0
        px, py = lerp(path[i0][0], path[i0 + 1][0], f), lerp(path[i0][1], path[i0 + 1][1], f)
        for k in range(i0 + 1):
            g.line([path[k], path[k + 1] if k < i0 else (px, py)], 8, (1, 1, 1, 0.9), amp=0)
        defenders = [(270, 790), (390, 1030), (510, 770), (630, 1010), (770, 790)]
        for j, (dx, dy) in enumerate(defenders):
            beaten = n > j + 1
            g.circle(dx + (20 if beaten else 0), dy, 30, WHITE, 6)
            if t > L[3] - 0.2:
                g.label(str(j + 1), dx, dy - 60, 40, color=RED, sc=ap(t, L[3] + 0.2 * j))
        g.circle(840, 860, 30, hexc("#9aa3ad"), 6)   # ผู้รักษาประตู
        g.circle(px, py, 34, ARG, 6)
        ball(g, px + 34, py + 10, 16, t * 6)
        g.label("60+ หลา", CX, 1240, 64, color=GREEN, sc=ap(t, L[2] + 0.4))
        if t > L[3] - 0.2:
            title(g, t, L[3], "แหวก 5 คน รวมผู้รักษาประตู!", RED, 80)
        else:
            title(g, t, L[2], "เลี้ยงเดี่ยวกว่า 60 หลา!", GREEN, 90)
        return
    if t < L[5] - 0.2:   # เข้าก้นตาข่าย
        goal(g, CX, GROUND - 100, 1.1, 1.0, t)
        for i in range(6):
            a = t * 3 + i
            g.star(CX + 300 * math.cos(a), 700 + 120 * math.sin(a), 26, GOLD2, 3)
        g.label("GOAL!", CX, 560, 130, color=RED, sc=ap(t, L[4] + 0.4), rot=-5)
        return
    diego(g, 400, 0.84, "smile", "v", 0.2)   # ชูถ้วยแชมป์โลก
    trophy(g, 830, 1230, 0.8, 4 * math.sin(t * 2), t)
    for i in range(12):
        u = (t * 0.6 + i / 12) % 1
        g.rrect(100 + (i * 97) % 880, 300 + 900 * u, 20, 30, 4, (ARG, WHITE, GOLD2)[i % 3], 0)
    title(g, t, L[5], "ชูถ้วยแชมป์โลก!", GOLDTXT, 100, 300)


# ------------------------------------------------------------------ 6. napoli
def s_napoli(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # เนเปิลส์ อิตาลี
        vesuvius(g, GROUND, t)
        if t > L[1] - 0.2:
            diego(g, 260, 0.7, "smile", "wave", 0.3, MARADONA_NAP)
            title(g, t, L[1], "ปาฏิหาริย์ที่เมืองเนเปิลส์", NAP, 86)
        else:
            title(g, t, L[0], "ไม่เพียงแค่อาร์เจนตินา...", INK, 90)
        return
    if t < L[4] - 0.2:   # ทีมคนจนแดนใต้ ล้มยักษ์เหนือ
        italy(g, 380, 840, 1.0, t, ap(t, L[2] + 0.3))
        diego(g, 780, 0.8, "smile", "fist", -0.3, MARADONA_NAP)
        if t > L[3] - 0.2:
            g.label("ล้มยักษ์ใหญ่!", 380, 520, 70, color=RED, sc=ap(t, L[3] + 0.3), rot=-4)
            title(g, t, L[3], "ล้มยักษ์ใหญ่แดนเหนือ!", RED, 88)
        else:
            title(g, t, L[2], "แบกทีมคนจนแดนใต้ \"นาโปลี\"", NAP, 82)
        return
    if t < L[5] - 0.2:   # แชมป์ครั้งแรก
        scudetto(g, CX, 840, 1.6 * ap(t, L[4]) + 0.01, 4 * math.sin(t * 2))
        g.label("ครั้งแรก!", CX, 1160, 100, color=NAP, sc=ap(t, L[4] + 0.5), rot=-4)
        title(g, t, L[4], "แชมป์เซเรีย อา ครั้งแรก", NAP, 88)
        return
    vesuvius(g, GROUND, t)   # เทพเจ้าองค์ที่สองของเมือง
    diego(g, CX, 0.8, "smile", "v", 0.0, MARADONA_NAP)
    halo(g, CX, 500, 100)
    for i, lk in enumerate(FANS[1:]):
        person(g, 190 + i * 700, GROUND, lk, 0.58, mood="smile", pose="wave", turn=0.4 - 0.8 * i, seed=22 + i)
    title(g, t, L[5], "เทพเจ้าองค์ที่สองของเมือง", NAP, 84, 330)


# ------------------------------------------------------------------ 7. dark
def s_dark(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:   # ดาบสองคม
        sword(g, CX, 1100, 1.2, 4 * math.sin(t * 1.5), ap(t, L[0] + 0.6))
        title(g, t, L[0], "ชีวิตดั่งดาบสองคม", INK, 96)
        return
    if t < L[2] - 0.2:   # ด้านสว่าง
        diego(g, 330, 0.84, "smile", "point", 0.3)
        g.sunburst(780, 820, 120, 240, 16, t * 6, 10, (1, 0.85, 0.4, 0.6))
        ball(g, 780, 820, 90, t)
        title(g, t, L[1], "ด้านสว่าง: อัจฉริยะลูกหนัง", GOLDTXT, 84)
        return
    dark_panel(g, 0.9)   # ด้านมืด: ข่าวฉาว
    diego(g, 300, 0.8, "sad", "down", 0.3)
    if t < L[3] - 0.2:
        with g.at(760, 820, 1):
            g.circle(0, 0, 150, (0.1, 0.1, 0.14, 0.9), 5)
            g.label("?", 0, 0, 160, color=NIGHTTXT)
        g.c.save()
        with g.at(760, 640, ap(t, L[2] + 0.6)):
            g.rrect(-150, -26, 300, 52, 10, (0.08, 0.08, 0.1, 1), 4)   # หมวกมาเฟีย (เงา)
            g.rrect(-90, -110, 180, 100, 20, (0.08, 0.08, 0.1, 1), 4)
        g.c.restore()
        title(g, t, L[2], "ด้านมืด: ยาเสพติด มาเฟีย", NIGHTTXT, 84)
        return
    headline(g, 700, 840, 0.68 * ap(t, L[3]) + 0.01, 5 + 2 * math.sin(t), "SCANDAL!", "DIEGO IN TROUBLE", "")
    title(g, t, L[3], "ข่าวฉาว... จุดดิ่งลงของชีวิต", NIGHTTXT, 82)


# ------------------------------------------------------------------ 8. lesson
def s_lesson(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:   # ไม่สมบูรณ์แบบ
        diego(g, CX, 0.84, "smile", "shrug", 0.0)
        title(g, t, L[0], "ไม่ใช่ชีวิตที่สมบูรณ์แบบ", INK, 86)
        return
    if t < L[3] - 0.2:   # ความดิบ จริงใจ มนต์สะกด → คนรัก
        diego(g, 280, 0.8, "smile", "wave", 0.3)
        if t < L[2] - 0.2:
            for i, (txt, col) in enumerate((("ความดิบ", RED), ("ความจริงใจ", GREEN), ("มนต์สะกดปลายสตั๊ด", GOLDTXT))):
                chip(g, 740, 560 + i * 190, txt, col, ap(t, L[1] + 0.5 * i), 4 - 4 * i, 400)
        else:
            for i in range(6):
                u = (t * 0.6 + i / 6) % 1
                heart(g, 560 + (i * 73) % 360, 1150 - 600 * u, 0.6 + 0.3 * (i % 2), (*RED[:3], 1 - u))
            title(g, t, L[2], "ทั้งโลกพร้อมให้อภัยและรัก", RED, 86)
        return
    if t < L[4] - 0.2:   # ไม่ใช่แค่นักกีฬา
        jersey(g, CX, 860, 1.3, WHITE, ARG, "10", ARG, 4 * math.sin(t * 1.5))
        title(g, t, L[3], "ไม่ใช่แค่นักกีฬา", INK, 96)
        return
    slum(g, GROUND, t)   # คนตัวเล็กจากสลัมสยบโลก
    diego(g, CX, 0.78, "smile", "v", 0.0)
    ball(g, CX + 160, GROUND - 40, 50, t)
    title(g, t, L[4], "คนตัวเล็กที่สยบโลกทั้งใบ", ARGTXT, 86, 330)


# ------------------------------------------------------------------ 9. outro
def s_outro(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:
        diego(g, 300, 0.8, "smile", "point", 0.3)
        g.label("?", 760, 780 + 15 * math.sin(t * 3), 240, color=RED, sc=ap(t, L[0] + 0.2))
        title(g, t, L[0] if t < L[1] - 0.2 else L[1], "นึกถึงภาพไหนเป็นสิ่งแรก?", INK, 86)
        return
    if t < L[4] - 0.2:   # หัตถ์พระเจ้า / ประตูแห่งศตวรรษ
        with g.at(300, 820, ap(t, L[2])):
            hand_ball(g, 0, 250, 0.7, t)
        chip(g, 300, 1160, "หัตถ์พระเจ้า", RED, ap(t, L[2] + 0.3), -4, 320)
        if t > L[3] - 0.2:
            with g.at(780, 820, ap(t, L[3])):
                g.rrect(-160, -110, 320, 220, 24, hexc("#2f6a3a"), 6)
                g.text("GOAL OF", 0, -36, 50, "kanit", NIGHTTXT)
                g.text("THE CENTURY", 0, 36, 42, "kanit", WHITE)
            chip(g, 780, 1160, "ประตูแห่งศตวรรษ", GREEN, ap(t, L[3] + 0.3), 4, 380)
        title(g, t, L[2] if t < L[3] - 0.2 else L[3], "ภาพไหนกัน?", INK, 96)
        return
    if t < L[6] - 0.2:   # ใครจะลึกซึ้งเท่า
        trophy(g, CX, 1180, 0.9, 5 * math.sin(t * 1.8), t)
        diego(g, 230, 0.7, "smile", "wave", 0.3)
        g.label("?", 830, 760, 200, color=RED, sc=ap(t, L[5]))
        title(g, t, L[4], "จะมีใครเหมือนชายคนนี้อีกไหม?", INK, 80)
        return
    with g.at(CX + 170, 640, ap(t, L[6])):   # ชวนคอมเมนต์
        g.bubble(0, 0, 460, 220, WHITE, tail=(-1, 1))
        for i in range(3):
            g.circle(-110 + i * 110, 0, 24 + 6 * math.sin(t * 6 - i), INK, 0)
    diego(g, 260, 0.7, "smile", "wave", 0.3)
    kick_ball(g, 450, 1220, t, 36)
    title(g, t, L[6], "มาแลกเปลี่ยนกันในคอมเมนต์!", RED, 70)


SCENES = {
    "hook": s_hook, "fiorito": s_fiorito, "mexico": s_mexico, "hand": s_hand, "goal": s_goal, "napoli": s_napoli,
    "dark": s_dark, "lesson": s_lesson, "outro": s_outro,
}
NO_IRIS = set()
