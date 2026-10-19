"""ฉากตอน: การสังหารหมู่คืนวันเสาร์ (20 ต.ค. 1973) — ตัวละครแบบกึ่งเสมือนจริง (src/people.py)"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from chars import (AGENT, AGENT2, BORK, CITIZENS, COX, NIXON, RICHARDSON, RUCKELSHAUS, WOOD2, capitol, clock,  # noqa: E402
                   desk, flag_us, mic, nail_lid, newspaper, paper, phone, reel_recorder, sign, tape_reel,
                   watergate, white_house, window_night)
from gfx import (BROWN2, GOLD, GOLD2, GREY, INK, LGREY, NAVY, RED, W, WHITE, e_back, e_in, e_io,  # noqa: E402
                 e_out, hexc, hn, lerp, pop, seg)
from people import _rr, _shade, _stroke, head, person  # noqa: E402

CX = W / 2
GROUND = 1270
DESK_Y = 930            # ขอบบนโต๊ะ (คนนั่งหลังโต๊ะ เท้าอยู่ราว GROUND)
DARK_RED = hexc("#a83a2c")

CAMERA = {"hook": "push_in", "cox": "pan_right", "order": "push_in", "richardson": "pull_out",
          "third": "tilt_down", "backfire": "dutch", "fall": "push_in", "lesson": "tilt_up", "outro": "pull_out"}
TRANSITIONS = {"second": "whip", "backfire": "zoom", "fall": "fade"}


def show(t, a, b=None, fade=0.25):
    """ความทึบของสิ่งที่แสดงช่วง [a, b)"""
    k = seg(t, a - fade, a)
    if b is not None:
        k = min(k, 1 - seg(t, b - fade, b))
    return k


def room(g, night=True):
    """ห้องทำงานรูปไข่แบบสัญลักษณ์: พื้น + หน้าต่างกลางคืน + ธง"""
    g.ground(GROUND, WHITE)
    if night:
        window_night(g, 300, 560, 260, 380)
        window_night(g, 780, 560, 260, 380, moon=False)


def nixon_at_desk(g, t, mood="neutral", pose="down", pose2=None, k=0.0, talk=False, turn=0.0, x=CX, papers=0):
    person(g, x, DESK_Y + 430 * 0.82, NIXON, 0.82, mood=mood, pose=pose, pose2=pose2, k=k, talk=talk, turn=turn,
           seed=3, shadow=False)
    desk(g, x, DESK_Y, 700)
    for i in range(papers):
        paper(g, x - 160 + i * 34, DESK_Y - 8 - i * 8, 0.5, -8 + i * 6, "ใบลาออก", 3)


def cross_out(g, x, y, r, k):
    """กากบาทแดงทับ (k 0..1 = ลากเส้น)"""
    for i, (a, b) in enumerate((((-1, -1), (1, 1)), ((1, -1), (-1, 1)))):
        kk = seg(k, i * 0.5, i * 0.5 + 0.5)
        if kk > 0:
            p0 = (x + a[0] * r, y + a[1] * r)
            p1 = (x + lerp(a[0], b[0], kk) * r, y + lerp(a[1], b[1], kk) * r)
            g.line([p0, p1], 22, RED, amp=0)


def revolver(g, x, y, sc=1.0):
    with g.at(x, y, sc):
        g.poly([(-150, -40), (110, -40), (110, -6), (-150, -6)], GREY, 6)
        g.rrect(-40, -62, 110, 90, 26, LGREY, 6)
        g.poly([(30, 20), (90, 20), (130, 140), (70, 150)], hexc("#7a5136"), 6, smooth=False)
        g.arc(30, 40, 26, 0, 180, 6)


def drop(g, x, y, sc=1.0):
    with g.at(x, y, sc):
        g.c.move_to(0, -110)
        g.c.curve_to(50, -30, 80, 10, 0, 80)
        g.c.curve_to(-80, 10, -50, -30, 0, -110)
        g.fs(hexc("#d24a3c"), 7)
        g.blob(-24, 10, 12, 22, (1, 1, 1, 0.5), 0)


def crack(g, x, y, k, seed=1, size=260):
    """รอยร้าวแตกออกจากจุดกลาง"""
    for i in range(6):
        a = i * 1.05 + 0.3 * hn(i, seed)
        pts = [(x, y)]
        r = 0
        for j in range(5):
            r += size / 5 * k
            a += 0.35 * hn(i, j, seed)
            pts.append((x + math.cos(a) * r, y + math.sin(a) * r))
        g.line(pts, 7, INK, amp=0)


def portrait(g, x, y, sc, t, cracked=0.0, grey=0.0):
    """กรอบรูปประธานาธิบดี"""
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -190, -230, 380, 460, 14)
        _shade(c, GOLD, 8, 0.3)
        _rr(c, -160, -200, 320, 400, 8)
        _shade(c, hexc("#e9eef5"), 5, 0.1)
        c.save()
        _rr(c, -160, -200, 320, 400, 8)
        c.clip()
        with g.at(0, 10, 1.45):
            head(g, NIXON, "smile" if cracked < 0.3 else "worry", seed=4)
        _rr(c, -160, 150, 320, 60, 0)
        _shade(c, NIXON.suit, 0, 0.3)
        if grey > 0:
            c.set_source_rgba(0.55, 0.55, 0.58, 0.55 * grey)
            c.paint()
        c.restore()
        if cracked > 0:
            crack(g, 30, -40, cracked, 3, 230)


def magnifier(g, x, y, sc=1.0, rot=-30):
    with g.at(x, y, sc, rot):
        g.rrect(-14, 70, 28, 130, 10, hexc("#5a3a22"), 6)
        g.circle(0, 0, 80, (0.85, 0.93, 1.0, 0.35), 10)


def briefcase(g, x, y, sc=1.0):
    with g.at(x, y, sc):
        g.rrect(-90, -70, 180, 130, 14, hexc("#6e4528"), 6)
        g.rrect(-34, -96, 68, 30, 10, None, 7)
        g.line([(-90, -20), (90, -20)], 5, amp=0)


def chair(g, x, y, sc=1.0, glow=0.0):
    with g.at(x, y, sc):
        if glow > 0:
            g.sunburst(0, -150, 130, 230, 14, g.t * 20, 9, (0.95, 0.83, 0.48, glow))
        g.rrect(-80, -330, 160, 200, 30, hexc("#7a2e2e"), 6)
        g.rrect(-100, -150, 200, 50, 16, hexc("#7a2e2e"), 6)
        for sx in (-1, 1):
            g.line([(sx * 80, -100), (sx * 90, 0)], 10)


def helicopter(g, x, y, sc=1.0, t=0.0):
    with g.at(x, y, sc):
        g.rrect(-260, -150, 420, 150, 70, hexc("#3e5a47"), 7)
        g.rrect(140, -110, 260, 40, 16, hexc("#3e5a47"), 7)
        g.rrect(-200, -120, 120, 70, 24, hexc("#cfe0ea"), 5)
        g.line([(-100, -150), (-100, -190)], 10)
        r = 340 * abs(math.cos(t * 30))
        g.line([(-100 - r, -195), (-100 + r, -195)], 10, amp=0)
        g.line([(-200, 0), (100, 0)], 9, amp=0)
        g.label("UNITED STATES OF AMERICA", -40, -30, 26)


def hammer(g, x, y, sc=1.0, rot=0.0):
    with g.at(x, y, sc, rot):
        g.rrect(-14, -10, 28, 220, 10, BROWN2, 6)
        g.rrect(-80, -60, 160, 60, 10, GREY, 6)


def envelope(g, x, y, sc=1.0, rot=0.0):
    with g.at(x, y, sc, rot):
        g.rrect(-60, -38, 120, 76, 6, hexc("#f2ecdc"), 5)
        g.line([(-60, -38), (0, 6), (60, -38)], 5, amp=0)


def scale_balance(g, x, y, sc, tilt):
    """ตาชั่ง: tilt > 0 = ฝั่งขวาลง"""
    with g.at(x, y, sc):
        g.rrect(-12, -300, 24, 300, 8, GOLD, 6)
        g.rrect(-90, -20, 180, 30, 10, GOLD, 6)
        a = math.radians(tilt)
        for sx in (-1, 1):
            px, py = sx * 220 * math.cos(a), -300 + sx * 220 * math.sin(a)
            g.line([(px, py), (px - 70, py + 120), (px + 70, py + 120), (px, py)], 4, amp=0)
            g.arc(px, py + 120, 72, 0, 180, 7)
        g.line([(-220 * math.cos(a), -300 - 220 * math.sin(a)), (220 * math.cos(a), -300 + 220 * math.sin(a))], 12, amp=0)
        g.circle(0, -300, 16, GOLD2, 5)


def door(g, x, y, sc=1.0, bright=False, k=0.0):
    with g.at(x, y, sc):
        if bright:
            g.sunburst(0, -200, 160, 260 + 30 * k, 16, g.t * 15, 10, (0.95, 0.83, 0.48, 0.8))
        g.rrect(-110, -420, 220, 420, 10, hexc("#fff4cf") if bright else hexc("#5a5550"), 7)
        g.rrect(-90, -400, 180 * (1 - 0.7 * k), 400, 6, hexc("#9b6a3e") if bright else hexc("#3a3632"), 6)
        g.circle(60 - 126 * k, -200, 9, GOLD, 4)


# ------------------------------------------------------------------ 1. hook
def s_hook(g, t, L, d):
    if t < L[3] - 0.2:
        white_house(g, CX, 1150, 1.15, night=True)
        g.circle(840, 420, 60, hexc("#f4eccf"), 5)
        for i in range(8):
            g.sparkle(120 + i * 120, 380 + 60 * ((i * 37) % 3), 12 + 4 * math.sin(t * 3 + i))
        if t < L[1] - 0.2:
            g.label("วันนี้ในอดีต", CX, 470, 104, sc=lerp(2.0, 1, e_out(seg(t, 0.1, 0.4))) if t > 0.1 else 0, rot=-4)
            g.label("20 ตุลาคม 1973", CX, 610, 84, color=RED, sc=pop(t, 0.8))
        else:
            g.label("คืนวันเสาร์", CX, 470, 90, sc=pop(t, L[1] - 0.1))
            if t > L[2] - 0.2:
                g.label('"การสังหารหมู่คืนวันเสาร์"', CX, 610, 78, color=RED, sc=pop(t, L[2] - 0.1), rot=-3)
                g.label("Saturday Night Massacre", CX, 700, 46, color=GREY, sc=pop(t, L[2] + 0.3))
        return
    if t < L[5] - 0.2:
        g.ground(GROUND, WHITE)
        revolver(g, 300, 760, 1.2 * pop(t, L[3] - 0.2))
        cross_out(g, 300, 780, 170, seg(t, L[3] + 0.6, L[3] + 1.4))
        g.label("ไม่มีเสียงปืน", 300, 1040, 60, sc=pop(t, L[3] + 0.4))
        if t > L[4] - 0.3:
            drop(g, 780, 760, 1.3 * pop(t, L[4] - 0.3))
            cross_out(g, 780, 770, 160, seg(t, L[4] + 0.6, L[4] + 1.4))
            g.label("ไม่มีเลือด", 780, 1040, 60, sc=pop(t, L[4] + 0.4))
        return
    # การเชือดเฉือนทางอำนาจ -> ดับอนาคตประธานาธิบดี
    g.ground(GROUND, WHITE)
    k = seg(t, L[6] + 0.8, L[6] + 2.0)
    portrait(g, CX, 720, 1.05 * pop(t, L[5] - 0.2), t, cracked=e_out(k), grey=k)
    for sx in (-1, 1):   # ปากกาสองด้ามฟันกันเหมือนดาบ
        a = sx * (35 + 12 * math.sin(t * 6))
        with g.at(CX + sx * 330, 1120, 1.0, a):
            g.rrect(-12, -260, 24, 260, 10, NAVY if sx < 0 else DARK_RED, 6)
            g.poly([(-12, -260), (12, -260), (0, -300)], GOLD2, 5)
    if t > L[6]:
        g.label("ดับอนาคต", CX, 1060, 80, color=RED, sc=pop(t, L[6] + 1.0), rot=-4)


# ------------------------------------------------------------------ 2. watergate
def s_watergate(g, t, L, d):
    if t < L[2] - 0.2:
        g.ground(GROUND, WHITE)
        white_house(g, CX + 250, 820, 0.7)
        flag_us(g, 160, GROUND - 30, 1.0, t)
        person(g, 470, GROUND, NIXON, 0.86, mood="smile" if t < L[1] + 1.2 else "worry",
               pose="v" if t < L[1] + 1.2 else "down", talk=False, seed=3)
        g.name_tag(t, L[1] - 0.1, 780, 480, "ริชาร์ด นิกสัน", "ประธานาธิบดีสหรัฐฯ คนที่ 37", side=-1)
        return
    g.ground(GROUND, WHITE)
    watergate(g, CX, GROUND - 40, 1.25 * pop(t, L[2] - 0.2))
    g.label('"คดีวอเตอร์เกต"', CX, 300, 90, color=RED, sc=pop(t, L[2] + 0.3), rot=-3)
    if t > L[3] - 0.2:   # คนแอบเข้าไปติดเครื่องดักฟัง (เงาดำ + ไฟฉาย)
        k = e_out(seg(t, L[3] - 0.2, L[3] + 0.8))
        for i, xx in enumerate((300, 520)):
            with g.silhouette(INK, 0.92):
                person(g, lerp(-120, xx, k), GROUND + 10, AGENT, 0.62, pose="hold", seed=10 + i, shadow=False)
            g.c.move_to(lerp(-120, xx, k) + 40, GROUND - 330)
            g.c.line_to(lerp(-120, xx, k) + 260, GROUND - 420)
            g.c.line_to(lerp(-120, xx, k) + 260, GROUND - 260)
            g.c.close_path()
            g.c.set_source_rgba(1, 0.92, 0.5, 0.45)
            g.c.fill()
        mic(g, 760, 820, 1.6 * pop(t, L[3] + 0.8))
        g.label("เครื่องดักฟัง", 760, 700, 54, sc=pop(t, L[3] + 1.0))


# ------------------------------------------------------------------ 3. cox
def s_cox(g, t, L, d):
    if t < L[3] - 0.2:
        g.ground(GROUND, WHITE)
        for i in range(5):
            paper(g, 760 + 30 * math.sin(i * 2.1), 1150 - i * 26, 0.7, -10 + 7 * i, "", 4)
        x = lerp(-200, 380, e_out(seg(t, 0, 1.4)))
        person(g, x, GROUND, COX, 0.88, mood="firm", pose="hold" if t < L[2] else "down", seed=5, turn=0.2,
               talk=False)
        if t < L[2] - 0.2:
            briefcase(g, x + 150, GROUND - 50, 0.9)
        g.name_tag(t, L[1] - 0.1, 760, 380, "อาร์ชิบัลด์ ค็อกซ์", "อัยการพิเศษคดีวอเตอร์เกต", side=-1)
        if t > L[2] - 0.2:
            mx = 760 + 90 * math.sin((t - L[2]) * 2.2)
            magnifier(g, mx, 860, 1.3 * pop(t, L[2] - 0.2))
            g.label("ความลับสุดยอด", 760, 520, 64, color=RED, sc=pop(t, L[2] + 0.4), rot=-4)
        return
    # ห้องทำงาน: ไมค์ซ่อนในโต๊ะ + เครื่องอัดเทปใต้ดิน
    room(g, night=False)
    flag_us(g, 150, GROUND - 60, 0.9, t)
    nixon_at_desk(g, t, mood="smug", turn=0.3)
    mic(g, CX - 240, DESK_Y - 20, 1.2 * pop(t, L[3] + 0.3))
    mic(g, CX + 240, DESK_Y - 20, 1.2 * pop(t, L[3] + 0.5))
    reel_recorder(g, CX, 1220, 1.1 * pop(t, L[3]), t, glow=0.5 + 0.5 * math.sin(t * 5))
    g.label("ระบบอัดเสียงลับ", CX, 300, 80, color=RED, sc=pop(t, L[3] + 0.6), rot=-3)


# ------------------------------------------------------------------ 4. tapes
def s_tapes(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:
        person(g, 330, GROUND, COX, 0.88, mood="firm", pose="hold", seed=5, turn=0.3, talk=True)
        paper(g, 330, 800, 0.95 * pop(t, 0.5), -6, "หมายเรียก", 5, stamp="SUBPOENA", stamp_k=seg(t, 1.6, 2.0))
        for i in range(6):
            tape_reel(g, 740 + (i % 2) * 150, 1180 - (i // 2) * 150, 0.95 * pop(t, 1.0 + i * 0.15),
                      t * 0.5 * (i % 2 * 2 - 1), "เทป" if i == 5 else None)
        return
    shake = 6 * math.sin(t * 40) * seg(t, L[2] - 0.2, L[2] + 0.2)
    with g.at(shake, 0):
        nixon_at_desk(g, t, mood="worry" if t < L[2] - 0.2 else "shock", turn=-0.2)
    g.sweat(CX + 90, 380, 1.2 * pop(t, L[1] + 0.5))
    for i in range(3):
        tape_reel(g, CX - 220 + i * 220, DESK_Y - 50 + 4 * math.sin(t * 6 + i), 0.7, t * (1 + i))
    if t > L[2] - 0.2:
        g.label("จบสิ้น!", CX, 300, 120, color=RED, sc=pop(t, L[2] - 0.1), rot=-5)


# ------------------------------------------------------------------ 5. order
def s_order(g, t, L, d):
    room(g)
    clock(g, CX, 360, 80, 20.3 + t * 0.02)
    if t < L[1] - 0.2:
        g.label("คืนวันเสาร์ 20 ต.ค. 1973", CX, 860, 72, sc=pop(t, 0.3))
        g.label("ตึงเครียดถึงขีดสุด", CX, 980, 64, color=RED, sc=pop(t, 1.2))
        return
    pose = "phone" if t < L[3] - 0.2 else "point"
    nixon_at_desk(g, t, mood="angry" if t < L[3] - 0.2 else "shout", pose=pose, talk=t < L[3] - 0.2, turn=0.25,
                  x=CX - 120)
    if t < L[3] - 0.2:
        phone(g, CX + 240, DESK_Y - 4, 0.7)
    if t > L[2] - 0.2:   # สายตรงถึงอัยการสูงสุด
        with g.alpha(show(t, L[2], L[4] + 0.3)):
            for i in range(3):
                p = (t * 1.5 + i / 3) % 1
                g.arc(CX + 300, 640, 50 + 80 * p, -50, 50, 8, (0.78, 0.33, 0.24, 1 - p))
            g.label("อัยการสูงสุด", CX + 330, 720, 54, maxw=360)
    if t > L[3] - 0.2:
        paper(g, CX + 300, 640, 0.9 * pop(t, L[3] - 0.2), 8, "คำสั่ง", 4, stamp="ปลด!", stamp_k=seg(t, L[3] + 0.5, L[3] + 0.9))
    if t > L[4] - 0.2:   # ฝังกลบความจริง: กล่อง "ความจริง" จมลงใต้กองเอกสาร
        k = e_in(seg(t, L[4], L[4] + 1.1))
        with g.at(CX + 330, 1060 + 160 * k):
            g.rrect(-110, -60, 220, 120, 12, GOLD2, 6)
            g.label("ความจริง", 0, 0, 44)
        for i in range(4):
            yy = lerp(700, 1000 - i * 30, e_out(seg(t, L[4] + i * 0.12, L[4] + 0.6 + i * 0.12)))
            paper(g, CX + 330 + 30 * hn(i, 2), yy, 0.55, 20 * hn(i, 4), "", 3)


# ------------------------------------------------------------------ 6. richardson
def s_richardson(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[3] - 0.2:
        rx = 770
        person(g, 220, GROUND, NIXON, 0.78, mood="smug" if t < L[2] else "shock", pose="point", turn=0.35, seed=3)
        chair(g, 990, GROUND, 0.8 * pop(t, L[1] + 0.6), glow=0.6 * show(t, L[1] + 0.6, L[2]))
        person(g, rx, GROUND, RICHARDSON, 0.88, mood="worry" if t < L[2] - 0.2 else "firm",
               pose="down" if t < L[2] - 0.2 else "stop", turn=-0.3, seed=6, talk=L[2] < t < L[2] + 1.5)
        g.name_tag(t, L[1] - 0.1, 700, 300, "เอลเลียต ริชาร์ดสัน", "อัยการสูงสุด", side=1)
        if t < L[1] - 0.2:
            g.label("เกียรติยศ?", CX, 300, 70, color=GREY, sc=pop(t, 0.5))
        if t > L[2] - 0.2:
            g.label("ไม่!", 960, 520, 130, color=RED, sc=pop(t, L[2]), rot=-6)
        return
    if t < L[4] - 0.2:   # สัญญากับสภา
        capitol(g, CX, 900, 1.4 * pop(t, L[3] - 0.2))
        g.label("สัญญาต่อสภา:", CX, 360, 70, sc=pop(t, L[3] + 0.2))
        g.label('"จะไม่แทรกแซงการสอบสวน"', CX, 470, 64, color=NAVY, sc=pop(t, L[3] + 0.6))
        person(g, 830, GROUND + 40, RICHARDSON, 0.6, mood="firm", pose="stop", turn=-0.3, seed=6)
        return
    # ใบลาออกฉบับแรก
    desk(g, CX - 140, DESK_Y, 620)
    k = e_out(seg(t, L[4], L[4] + 0.8))
    paper(g, lerp(CX + 300, CX - 200, k), lerp(600, DESK_Y - 30, k), 0.7, lerp(30, -6, k), "ใบลาออก", 4)
    walk = seg(t, L[4] + 1.0, d)
    person(g, lerp(860, 1300, walk), GROUND - 10, RICHARDSON, 0.78, mood="firm", turn=0.4, seed=6)
    g.label("ลาออกประท้วง!", CX, 420, 84, color=RED, sc=pop(t, L[4] + 0.3), rot=-4)


# ------------------------------------------------------------------ 7. second
def s_second(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:
        person(g, 220, GROUND, NIXON, 0.8, mood="shout" if t < L[1] - 0.2 else "shock", pose="point", turn=0.35,
               seed=3)
        person(g, 790, GROUND, RUCKELSHAUS, 0.86, mood="worry" if t < L[1] - 0.2 else "firm",
               pose="down" if t < L[1] - 0.2 else "stop", turn=-0.3, seed=7, talk=L[1] < t < L[1] + 1.5)
        g.name_tag(t, 1.2, 740, 300, "วิลเลียม รัคเคิลส์เฮาส์", "รองอัยการสูงสุด", side=1)
        if t > L[1] - 0.2:
            g.label("ไม่!", 560, 560, 130, color=RED, sc=pop(t, L[1]), rot=6)
        return
    desk(g, CX, DESK_Y, 700)
    paper(g, CX - 80, DESK_Y - 30, 0.7, -6, "ใบลาออก", 4)
    k = e_out(seg(t, L[2], L[2] + 0.8))
    paper(g, lerp(CX + 320, CX + 20, k), lerp(560, DESK_Y - 50, k), 0.7, lerp(-30, 8, k), "ใบลาออก", 4)
    g.label("ใบที่ 2!", CX, 480, 110, color=RED, sc=pop(t, L[2] + 0.7), rot=-5)
    g.label("ในคืนเดียวกัน", CX, 620, 64, sc=pop(t, L[2] + 1.2))


# ------------------------------------------------------------------ 8. third
def s_third(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:
        # ไล่ลำดับลงไป: 1 ✗  2 ✗  3 ✓
        steps = [(RICHARDSON, "1. อัยการสูงสุด", 230, 520), (RUCKELSHAUS, "2. รองอัยการสูงสุด", 540, 760),
                 (BORK, "3. Solicitor General", 850, 1000)]
        for i, (lk, txt, x, y) in enumerate(steps):
            k = pop(t, 0.2 + i * 0.6)
            if k <= 0:
                continue
            with g.at(x, y, 0.62 * k):
                head(g, lk, "firm" if i < 2 else "neutral", seed=6 + i)
            g.label(txt, x, y + 150, 40, sc=k)
            if i < 2:
                cross_out(g, x, y, 90, seg(t, 0.8 + i * 0.6, 1.3 + i * 0.6))
            elif t > L[1] - 0.2:
                g.circle(x, y, 120, None, 12, stroke=hexc("#3c8d4f"))
        if t > L[1] - 0.2:
            with g.alpha(show(t, L[1])):
                desk(g, 220, 1040, 400, 0.7)
                k = seg(t, L[1] + 0.4, L[1] + 1.6)
                paper(g, 220, 1010, 0.55, -4, "คำสั่งปลด", 3, stamp="ลงนาม" if k >= 1 else None)
            g.name_tag(t, L[1] - 0.1, 850, 760 - 280, "โรเบิร์ต บอร์ก", "Solicitor General · ลำดับที่ 3", side=-1)
        return
    # เอฟบีไอปิดตายสำนักงานกลางดึก
    window_night(g, 220, 480, 220, 300)
    with g.at(CX + 120, GROUND):
        _rr(g.c, -230, -620, 460, 620, 8)
        _shade(g.c, hexc("#e9e2d4"), 6, 0.15)
        door(g, 0, 0, 1.1)
        g.label("สำนักงานอัยการพิเศษ", 0, -560, 40)
        k = seg(t, L[2] + 0.8, L[2] + 2.0)
        for i, a in enumerate((-18, 14)):
            kk = seg(k, i * 0.4, i * 0.4 + 0.6)
            if kk > 0:
                with g.at(0, -260 + i * 120, 1, a):
                    g.rrect(-150 * kk, -24, 300 * kk, 48, 6, GOLD2, 5)
                    if kk >= 1:
                        g.text("ปิด · FBI", 0, 0, 30, "kanit")
    x = lerp(-300, 0, e_out(seg(t, L[2] - 0.2, L[2] + 0.8)))
    person(g, 160 + x, GROUND + 20, AGENT, 0.72, mood="firm", pose="cross", turn=0.3, seed=11)
    person(g, 360 + x, GROUND + 30, AGENT2, 0.7, mood="neutral", turn=0.3, seed=12)
    g.label("เอฟบีไอ · กลางดึก", CX + 120, 420, 64, color=NAVY, sc=pop(t, L[2] + 0.4))


# ------------------------------------------------------------------ 9. backfire
def s_backfire(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:
        wrong = t > L[1] - 0.1
        if wrong:
            crack(g, CX, 640, e_out(seg(t, L[1] - 0.1, L[1] + 0.4)), 5, 380)
        person(g, CX, GROUND, NIXON, 0.9, mood="shock" if wrong else "smug", pose="cross" if not wrong else "shrug",
               seed=3)
        if not wrong:
            g.label("ชนะแล้ว!", CX, 300, 90, sc=pop(t, 0.6), rot=-4)
        else:
            g.label("คิดผิดมหันต์!", CX, 340, 100, color=RED, sc=pop(t, L[1]), rot=-5)
        return
    if t < L[3] - 0.2:   # ข่าวแพร่สะพัด
        heads = [("2 ผู้บริหารลาออก!", "ประท้วงคำสั่งปลดอัยการพิเศษ"), ("ปลดค็อกซ์!", "คืนวันเสาร์ที่ทำเนียบขาว"),
                 ("นิกสันถูกวิจารณ์หนัก", "")]
        for i, (h1, h2) in enumerate(heads):
            k = e_out(seg(t, L[2] - 0.2 + i * 0.4, L[2] + 0.5 + i * 0.4))
            if k > 0:
                newspaper(g, lerp(CX + 900, 300 + i * 240, k), 760 + 40 * i, 0.95, lerp(40, -8 + 8 * i, k), h1, h2)
        return
    if t < L[4] - 0.2:   # ประชาชนลุกฮือ
        texts = ["IMPEACH NIXON", "HONK TO IMPEACH", "ไม่มีใคร\nอยู่เหนือกฎหมาย", "IMPEACH!"]
        for i in range(4):
            x = 150 + i * 260
            bob = 12 * math.sin(t * 5 + i)
            lk = CITIZENS[i]
            person(g, x, GROUND + 30 * (i % 2), lk, 0.62, mood="shout" if i % 2 else "angry", pose="fist", turn=0.2 - 0.1 * i,
                   seed=20 + i)
            sign(g, x + 90, 620 + bob + 30 * (i % 2), texts[i].replace("\n", " "), 0.85 * pop(t, L[3] + i * 0.15), -6 + 4 * i)
        g.label("ประชาชนโกรธแค้น", CX, 300, 80, color=RED, sc=pop(t, L[3] + 0.4))
        return
    if t < L[5] - 0.2:   # อำนาจอยู่เหนือกฎหมาย = เผด็จการ
        scale_balance(g, CX, 1150, 1.2 * pop(t, L[4] - 0.2), -18 * e_io(seg(t, L[4] + 0.3, L[4] + 1.2)))
        g.label("อำนาจ", CX - 260, 560, 64, sc=pop(t, L[4] + 0.3))
        g.label("กฎหมาย", CX + 260, 820, 64, sc=pop(t, L[4] + 0.5))
        g.label("เผด็จการ?", CX, 330, 90, color=RED, sc=pop(t, L[4] + 1.3), rot=-4)
        return
    # แรงกดดันถาโถมใส่ทำเนียบขาว: โทรเลขหลายแสนฉบับ
    white_house(g, CX, 1150, 1.15, night=False)
    for i in range(26):
        p = ((t - L[5]) * 0.9 + i / 26) % 1
        a = i * 2.39
        r = lerp(900, 120, e_in(p))
        envelope(g, CX + math.cos(a) * r, 820 + math.sin(a) * r * 0.45, 0.8, 30 * hn(i, 7))
    g.label("โทรเลขกว่า 4.5 แสนฉบับ", CX, 300, 64, sc=pop(t, L[5] + 0.4))


# ------------------------------------------------------------------ 10. fall
def s_fall(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:
        if t < L[1] - 0.2:
            paper(g, CX, 760, 1.4 * pop(t, 0.2), -4, "คำสั่งปลด", 5, stamp="ปลด!", stamp_k=seg(t, 0.8, 1.2))
            g.label("เพื่อเอาตัวรอด", CX, 360, 76, sc=pop(t, 1.0))
            return
        hits = (t - L[1] - 0.3) / 0.55
        n = int(max(hits, 0))
        frac = max(hits, 0) - n
        sink = min(n, 3) / 3
        nail_lid(g, CX, 1040, 1.2, sink)
        swing = -70 + 90 * e_in(frac) if n < 3 else -40
        hammer(g, CX + 120, 900, 1.1, swing)
        g.label("ตะปูตัวสุดท้าย", CX, 420, 90, color=RED, sc=pop(t, L[1] + 0.2), rot=-4)
        return
    if t < L[3] - 0.2:
        nixon_at_desk(g, t, mood="sad", pose="sign", turn=0.0)
        paper(g, CX + 40, DESK_Y + 60, 0.75, 4, "I hereby resign", 3)
        g.label("ลาออก · 9 ส.ค. 1974", CX, 300, 70, color=RED, sc=pop(t, L[2] + 0.3))
        return
    # ขึ้นเฮลิคอปเตอร์ ชูสองนิ้ว (ภาพจำวันลาออก)
    helicopter(g, CX + 120, GROUND - 120, 1.3, t)
    g.rrect(80, GROUND - 120, 140, 120, 6, LGREY, 5)
    person(g, 150, GROUND - 110, NIXON, 0.72, mood="sad", pose="v", seed=3)
    g.label("ประธานาธิบดีคนแรกที่ลาออก", CX, 340, 64, sc=pop(t, L[3] + 0.2))


# ------------------------------------------------------------------ 11. lesson
def s_lesson(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:
        g.label("บทเรียน", CX, 380, 100, sc=pop(t, 0.2), rot=-3)
        if t > L[1] - 0.3:
            k = e_in(seg(t, L[1] + 0.8, L[1] + 2.4))
            with g.alpha(1 - k), g.at(CX, 1050 + 120 * k, 1 - 0.3 * k, 30 * k):
                g.c.move_to(-140, 0)
                g.c.line_to(-160, -160)
                g.c.line_to(-70, -80)
                g.c.line_to(0, -190)
                g.c.line_to(70, -80)
                g.c.line_to(160, -160)
                g.c.line_to(140, 0)
                g.c.close_path()
                g.fs(GOLD, 7)
            with g.alpha(1 - k):
                crack(g, CX, 960 + 120 * k, seg(t, L[1] + 0.3, L[1] + 1.0), 9, 160)
            g.label("อำนาจไร้ความชอบธรรม", CX, 530, 70, sc=pop(t, L[1] - 0.1))
            g.label("แพ้ภัยตัวเอง", CX, 650, 80, color=RED, sc=pop(t, L[1] + 0.8))
        return
    g.sunburst(CX, 700, 260, 640, 22, t * 8, 12, (0.95, 0.85, 0.55, 0.8))
    person(g, 390, GROUND, RICHARDSON, 0.72, mood="firm", turn=0.25, seed=6)
    person(g, 690, GROUND, RUCKELSHAUS, 0.70, mood="firm", turn=-0.25, seed=7)
    g.label("ความกล้าหาญ", CX, 360, 96, color=hexc("#b37a12"), sc=pop(t, L[2] + 0.4), rot=-3)
    if t > L[3] - 0.2:
        g.label("ทรงพลังที่สุด", CX, 480, 70, sc=pop(t, L[3]))


# ------------------------------------------------------------------ 12. outro
def s_outro(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[3] - 0.2:
        boss = AGENT
        person(g, 220, GROUND, boss, 0.86, mood="angry", pose="point", turn=0.35, seed=30, talk=L[1] < t < L[3])
        person(g, 820, GROUND, CITIZENS[2], 0.84, mood="worry" if t > L[1] else "neutral", turn=-0.3, seed=31)
        if t > L[1] - 0.2:
            paper(g, CX, 520, 0.8 * pop(t, L[1] + 0.3), 6, "ปกปิด", 4, stamp="ลับ", stamp_k=seg(t, L[2], L[2] + 0.4))
        if t < L[1] - 0.2:
            g.label("แล้วถ้าเป็นคุณล่ะ?", CX, 320, 80, sc=pop(t, 0.2))
        return
    if t < L[5] - 0.2:   # ทางแยก
        door(g, 250, GROUND - 40, 1.0, False)
        door(g, 830, GROUND - 40, 1.0, True, e_out(seg(t, L[4] + 0.6, L[4] + 1.6)))
        g.label("ทำตาม", 250, 760, 64, color=GREY, sc=pop(t, L[3]))
        g.label("ศักดิ์ศรี", 830, 760, 70, color=hexc("#b37a12"), sc=pop(t, L[4]))
        walk = e_io(seg(t, L[4] + 1.0, L[5]))
        person(g, lerp(CX, 790, walk), GROUND + 40, CITIZENS[2], 0.7, mood="firm" if t > L[4] else "worry",
               turn=0.4 * walk if t > L[4] else 0, seed=31)
        return
    # ชวนคอมเมนต์
    k = pop(t, L[5] - 0.1)
    with g.at(CX, 760, k):
        g.bubble(0, 0, 640, 300, WHITE, tail=(-1, 1))
        for i in range(3):
            g.circle(-120 + i * 120, 0, 26 + 6 * math.sin(t * 6 - i), INK, 0)
    g.label("คอมเมนต์คุยกันได้เลย!", CX, 1080, 70, color=RED, sc=pop(t, L[5] + 0.4))


SCENES = {
    "hook": s_hook, "watergate": s_watergate, "cox": s_cox, "tapes": s_tapes, "order": s_order,
    "richardson": s_richardson, "second": s_second, "third": s_third, "backfire": s_backfire, "fall": s_fall,
    "lesson": s_lesson, "outro": s_outro,
}
NO_IRIS = set()
