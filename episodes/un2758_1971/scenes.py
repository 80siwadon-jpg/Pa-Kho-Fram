"""ฉากตอน: ข้อมติสมัชชาใหญ่ UN ที่ 2758 (25 ต.ค. 1971) — เล่าเป็นกลาง ไม่ล้อเลียนฝ่ายใด"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from chars import (CHIANG, DELEGATES, MAO, ROC_DELEGATE, UN_BLUE, ballot, board, crowd_icon, desk, door,  # noqa: E402
                   emblem, flag, gavel, hall, island, rostrum, seat, veto_stamp)
from gfx import GOLD, GOLD2, GREY, INK, NAVY, RED, W, WHITE, e_io, e_out, hexc, lerp, pop, seg  # noqa: E402
from people import person  # noqa: E402

CX = W / 2
GROUND = 1270
GOLDTXT = hexc("#b37a12")
GREEN = hexc("#3c8d4f")
CNRED = hexc("#c8281a")
PURPLE = hexc("#7a4a9a")

CAMERA = {"hook": "push_in", "night": "tilt_up", "seat": "pan_right", "vote": "push_in", "walkout": "pan_left",
          "after": "pull_out", "lesson": "dutch", "outro": "pan_right"}
TRANSITIONS = {"night": "fade", "seat": "whip", "vote": "iris", "walkout": "zoom", "after": "whip", "lesson": "fade",
               "outro": "zoom"}


def ap(t, a, dur=0.38):
    return pop(t, a - 0.2, dur)


def title(g, t, a, txt, col=INK, size=84, y=380):
    g.label(txt, CX, y, size, color=col, sc=ap(t, a), rot=-3)


def delegates(g, t, x0=130, gap=210, sc=0.55, mood="neutral", pose="down", n=5, dance=False, talk=False):
    for i in range(n):
        if dance:
            k = 0.5 + 0.5 * math.sin(t * 7 + i * 1.3)
            person(g, x0 + i * gap, GROUND - 20 * abs(math.sin(t * 7 + i * 1.3)), DELEGATES[i % 5], sc, mood="smile",
                   pose="v", pose2="wave", k=k, seed=10 + i, turn=0.3 * math.sin(t * 3 + i), talk=True)
        else:
            person(g, x0 + i * gap, GROUND, DELEGATES[i % 5], sc, mood=mood, pose=pose if i % 2 == 0 else "down",
                   turn=0.3 - 0.15 * i, seed=10 + i, talk=talk)


def night_sky(g, a=1.0):
    """ฟ้ากลางคืน: แผงกรมท่าไล่จาง"""
    import cairo
    c = g.c
    gr = cairo.LinearGradient(0, 140, 0, GROUND)
    gr.add_color_stop_rgba(0, 0.12, 0.17, 0.3, 0.95 * a)
    gr.add_color_stop_rgba(1, 0.12, 0.17, 0.3, 0.0)
    c.rectangle(-500, 140, 2100, GROUND - 140)
    c.set_source(gr)
    c.fill()


def un_tower(g, x, y, sc=1.0, t=0.0):
    """ตึกสำนักงานใหญ่ UN (ตึกแผ่นสูง) + หน้าต่างไฟสว่าง"""
    c = g.c
    with g.at(x, y, sc):
        g.rrect(-120, -760, 240, 760, 6, hexc("#7fa6b8"), 6)
        for r in range(18):
            for k in range(5):
                on = (r * 7 + k * 3) % 5 != 0
                col = (1, 0.88, 0.5, 0.95) if on else (0.35, 0.45, 0.55, 1)
                c.rectangle(-100 + k * 42, -730 + r * 40, 30, 24)
                c.set_source_rgba(*col)
                c.fill()
        g.rrect(-320, -200, 200, 200, 6, hexc("#b9c4c8"), 6)


def skyline(g, y, a=1.0):
    c = g.c
    for i in range(12):
        x = -300 + i * 150
        h = 260 + (i * 97) % 300
        c.rectangle(x, y - h, 120, h)
        c.set_source_rgba(0.22, 0.27, 0.38, a)
        c.fill()
        for r in range(int(h / 50)):
            if (i + r) % 3:
                c.rectangle(x + 20, y - h + 20 + r * 50, 20, 18)
                c.rectangle(x + 70, y - h + 20 + r * 50, 20, 18)
                c.set_source_rgba(1, 0.85, 0.45, 0.8 * a)
                c.fill()


def moon(g, x, y, r=60):
    c = g.c
    c.new_path()
    c.arc(x, y, r, 0, 2 * math.pi)
    c.set_source_rgb(0.98, 0.95, 0.8)
    c.fill()
    c.new_path()
    c.arc(x + r * 0.45, y - r * 0.2, r * 0.85, 0, 2 * math.pi)
    c.set_source_rgba(0.12, 0.17, 0.3, 0.95)
    c.fill()


def clock(g, x, y, r, t, k=1.0):
    if k < 0.02:
        return
    with g.at(x, y, k):
        g.circle(0, 0, r, WHITE, 8)
        for i in range(12):
            a = i * math.pi / 6
            g.line([(r * 0.8 * math.cos(a), r * 0.8 * math.sin(a)), (r * 0.9 * math.cos(a), r * 0.9 * math.sin(a))],
                   5, INK, amp=0)
        a = t * 3
        g.line([(0, 0), (r * 0.7 * math.sin(a), -r * 0.7 * math.cos(a))], 8, RED, amp=0)
        g.line([(0, 0), (r * 0.45 * math.sin(a / 12), -r * 0.45 * math.cos(a / 12))], 10, INK, amp=0)
        g.circle(0, 0, 10, INK, 0)


def mainland_island(g, x, y, sc=1.0, t=0.0, split=1.0):
    """แผ่นดินใหญ่ (ซ้าย) กับเกาะ (ขวา) แบบการ์ตูนเรียบง่าย"""
    c = g.c
    from people import _shade, _smooth_path
    with g.at(x, y, sc):
        c.new_path()
        c.rectangle(-700, -40, 1400, 400)
        c.set_source_rgba(0.55, 0.75, 0.92, 0.6)
        c.fill()
        _smooth_path(c, [(-560, -320), (-200, -380), (60, -300), (120, -120), (40, 60), (-120, 200), (-420, 220),
                         (-600, 60)])
        _shade(c, hexc("#e9d29a"), 6, 0.2)
        dx = 80 * split
        _smooth_path(c, [(260 + dx, 40), (300 + dx, 0), (330 + dx, 60), (320 + dx, 180), (280 + dx, 200), (250 + dx, 120)])
        _shade(c, hexc("#a8d08a"), 6, 0.2)


def seesaw(g, x, y, ang, left, right, t):
    """กระดานหก: ขั้วอำนาจ"""
    with g.at(x, y):
        g.poly([(-50, 0), (50, 0), (0, -90)], hexc("#8a8a8a"), 6)
        with g.at(0, -90, 1, ang):
            g.rrect(-420, -16, 840, 32, 10, hexc("#b88a52"), 6)
            flag(g, -380, -300, 180, left, t)
            flag(g, 260, -300, 180, right, t)


# ------------------------------------------------------------------ 1. hook
def s_hook(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:
        emblem(g, CX, 840, 150 * pop(t, 0.2) + 1, t)
        g.label("วันนี้ในอดีต", CX, 380, 104, sc=lerp(2.0, 1, e_out(seg(t, 0.1, 0.4))) if t > 0.1 else 0, rot=-3)
        g.label("25 ตุลาคม 1971", CX, 520, 84, color=GOLDTXT, sc=pop(t, 0.6))
        return
    if t < L[2] - 0.2:   # กระดาษใบเดียว + ไม่กี่นาที
        ballot(g, 330, 820, 1.4 * ap(t, L[1]) + 0.01, -6 + 3 * math.sin(t * 2))
        clock(g, 780, 820, 150, t, ap(t, L[1] + 0.4))
        title(g, t, L[1], "กระดาษใบเดียว · ไม่กี่นาที", INK, 76)
        return
    if t < L[3] - 0.2:   # ตกจากเก้าอี้
        u = e_io(seg(t, L[2] + 0.4, L[2] + 1.6))
        seat(g, lerp(720, 900, u), GROUND, 1.0, lerp(0, 14, u), "CHINA")
        person(g, 230, GROUND, ROC_DELEGATE, 0.75, mood="shock", pose="shrug", turn=0.4, seed=3)
        title(g, t, L[2], "ผู้ร่วมก่อตั้ง UN ตกจากเก้าอี้!", RED, 76)
        return
    ang = lerp(0, -14, e_io(seg(t, L[3], L[3] + 1.2)))   # เปลี่ยนขั้วอำนาจ
    seesaw(g, CX, GROUND, ang, "roc", "prc", t)
    title(g, t, L[3], "เปลี่ยนขั้วอำนาจโลก!", CNRED, 88)


# ------------------------------------------------------------------ 2. night
def s_night(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # คืน 25 ต.ค. 1971 นิวยอร์ก
        night_sky(g)
        moon(g, 840, 600)
        skyline(g, GROUND, 0.8)
        un_tower(g, 420, GROUND, 1.0, t)
        if t < L[1] - 0.2:
            title(g, t, L[0], "คืนวันที่ 25 ต.ค. 1971", GOLDTXT, 84)
        else:
            title(g, t, L[1], "สำนักงานใหญ่ UN นิวยอร์ก", UN_BLUE, 78)
        return
    hall(g, GROUND, t)
    if t < L[3] - 0.2:   # ตึงเครียดจนแทบระเบิด
        delegates(g, t, mood="worry")
        for i in range(4):
            g.sweat(150 + i * 230, 720 + 10 * math.sin(t * 6 + i), 1.2)
        title(g, t, L[2], "ตึงเครียดจนแทบระเบิด!", CNRED, 84)
        return
    if t < L[4] - 0.2:   # ข้อมติที่ 2758
        rostrum(g, CX, GROUND, 1.0)
        ballot(g, CX, 840, 1.3 * ap(t, L[3]) + 0.01, 4)
        title(g, t, L[3], "\"ข้อมติที่ 2758\"", UN_BLUE, 96)
        return
    if t < L[5] - 0.2:   # คาราคาซังกว่า 20 ปี
        clock(g, CX, 820, 200, t * 6, ap(t, L[4]))
        g.label("20+ ปี", CX, 1130, 90, color=RED, sc=ap(t, L[4] + 0.3))
        title(g, t, L[4], "คาราคาซังกว่า 20 ปี", INK, 84)
        return
    flag(g, 120, 640, 300, "roc", t, k=ap(t, L[5]))   # ใครคือตัวแทนชาวจีน?
    flag(g, 660, 640, 300, "prc", t, k=ap(t, L[5] + 0.2))
    g.label("?", CX, 760, 200, color=PURPLE, sc=ap(t, L[5] + 0.4), rot=8 * math.sin(t * 3))
    title(g, t, L[5], "ใครคือตัวแทนชาวจีนทั้งปวง?", PURPLE, 74)


# ------------------------------------------------------------------ 3. seat
def s_seat(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # หลังสงครามกลางเมือง: แผ่นดินใหญ่ / ไต้หวัน
        mainland_island(g, CX + 20, 980, 0.72, t, e_io(seg(t, 0.2, 1.4)))
        g.label("แผ่นดินใหญ่", CX - 130, 920, 54, color=CNRED, sc=pop(t, 0.6))
        g.label("ไต้หวัน", CX + 300, 1150, 50, color=NAVY, sc=pop(t, 1.0))
        if t < L[1] - 0.2:
            title(g, t, L[0], "สงครามกลางเมืองสิ้นสุด (1949)", INK, 72)
        else:
            flag(g, 760, 560, 200, "roc", t, k=ap(t, L[1]))
            title(g, t, L[1], "สาธารณรัฐจีน (ไต้หวัน)", NAVY, 80)
        return
    if t < L[5] - 0.2:   # เจียง ไคเชก นั่งเก้าอี้สมาชิกถาวร
        person(g, 300, GROUND, CHIANG, 0.85, mood="firm", pose="down" if t < L[3] else "point", turn=0.3, seed=5)
        g.name_tag(t, L[2] + 0.1, 300, 1150, "เจียง ไคเชก", "ผู้นำสาธารณรัฐจีน")
        if t < L[3] - 0.2:
            flag(g, 640, 560, 240, "roc", t)
            title(g, t, L[2], "ภายใต้การนำของเจียง ไคเชก", NAVY, 76)
        elif t < L[4] - 0.2:
            seat(g, 760, GROUND, 1.0 * ap(t, L[3]) + 0.01, 0, "CHINA")
            title(g, t, L[3], "สมาชิกถาวรคณะมนตรีความมั่นคง", UN_BLUE, 70)
        else:
            seat(g, 760, GROUND, 1.0, 0, "CHINA")
            with g.at(760, 600, ap(t, L[4]), -8):
                g.rrect(-170, -70, 340, 140, 30, WHITE, 7, stroke=GOLDTXT)
                g.label("ผู้ก่อตั้ง 1945", 0, 0, 52, color=GOLDTXT)
            title(g, t, L[4], "หนึ่งในผู้ร่วมก่อตั้ง UN", GOLDTXT, 78)
        return
    if t < L[7] - 0.2:   # เหมา เจ๋อตง + ประชากรหลายร้อยล้าน
        person(g, 260, GROUND, MAO, 0.85, mood="smile", pose="down", turn=0.3, seed=6)
        g.name_tag(t, L[5] + 0.1, 260, 1150, "เหมา เจ๋อตง", "ผู้นำพรรคคอมมิวนิสต์จีน")
        if t < L[6] - 0.2:
            flag(g, 600, 560, 260, "prc", t, k=ap(t, L[5]))
            title(g, t, L[5], "พรรคคอมมิวนิสต์จีน", CNRED, 84)
        else:
            for i in range(20):
                crowd_icon(g, 560 + (i % 5) * 90, 640 + (i // 5) * 150, 0.9 * pop(t, L[6] - 0.2 + 0.04 * i),
                           [CNRED, GOLD, GREY, hexc("#d76b5a")][i % 4])
            title(g, t, L[6], "ประชากรหลายร้อยล้านคน", CNRED, 80)
        return
    door(g, 640, GROUND, 1.0)   # ถูกปิดประตูกั้นนอกเวทีโลก
    person(g, 230, GROUND, MAO, 0.75, mood="firm", pose="cross", turn=0.4, seed=6)
    emblem(g, 640, 560, 70 * ap(t, L[7]) + 1, t)
    title(g, t, L[7], "ถูกกันอยู่นอกเวทีโลก", INK, 84)


# ------------------------------------------------------------------ 4. vote
def s_vote(g, t, L, d):
    g.ground(GROUND, WHITE)
    hall(g, GROUND, t)
    if t < L[1] - 0.2:   # แต่ในค่ำคืนนั้น...
        delegates(g, t, mood="worry")
        title(g, t, L[0], "แต่ในค่ำคืนนั้น...", INK, 90)
        return
    if t < L[3] - 0.2:   # กระดานพลิก 76 ประเทศ
        k = e_out(seg(t, L[1], L[2] + 0.8))
        board(g, CX, 860, 1.25 * ap(t, L[1]) + 0.01, k=k, t=t)
        if t < L[2] - 0.2:
            title(g, t, L[1], "กระดานคะแนนพลิกถล่มทลาย!", CNRED, 76)
        else:
            title(g, t, L[2], "76 ประเทศเห็นด้วย!", GREEN, 90)
        return
    if t < L[5] - 0.2:   # แอลจีเรีย + โลกที่สาม + ยุโรป
        delegates(g, t, mood="smile", pose="v" if t > L[4] - 0.2 else "wave", n=5, sc=0.48)
        with g.at(CX, 500, ap(t, L[3]), -3):
            g.rrect(-380, -70, 760, 140, 36, WHITE, 7, stroke=GREEN)
            g.label("แอลจีเรีย + โลกที่สาม", 0, 0, 58, color=GREEN)
        if t > L[4] - 0.2:
            with g.at(CX, 650, ap(t, L[4]), 3):
                g.rrect(-260, -60, 520, 120, 36, WHITE, 7, stroke=UN_BLUE)
                g.label("+ ชาติในยุโรป", 0, 0, 54, color=UN_BLUE)
        title(g, t, L[3], "ใครโหวตรับรอง?", INK, 84, y=330)
        return
    if t < L[6] - 0.2:   # รับรอง PRC
        u = e_io(seg(t, L[5], L[5] + 1.5))
        g.line([(CX - 30, GROUND), (CX - 30, 520)], 8, hexc("#8a8a8a"), amp=0)
        flag(g, CX - 30, lerp(1000, 540, u), 300, "prc", t, pole=False)
        title(g, t, L[5], "สาธารณรัฐประชาชนจีน", CNRED, 84)
        return
    seat(g, CX, GROUND, 1.1, 0, "CHINA")   # ตัวแทนหนึ่งเดียว
    flag(g, CX + 230, 640, 200, "prc", t, k=ap(t, L[6]))
    g.sparkle(CX - 180, 700, 40 * ap(t, L[6] + 0.3) + 1)
    title(g, t, L[6], "ตัวแทนหนึ่งเดียวของจีนใน UN", CNRED, 74)


# ------------------------------------------------------------------ 5. walkout
def s_walkout(g, t, L, d):
    g.ground(GROUND, WHITE)
    hall(g, GROUND, t)
    if t < L[3] - 0.2:   # ผู้แทนไต้หวันลุกขึ้น เดินออกเงียบ ๆ
        if t > L[1] - 0.2:
            door(g, 860, GROUND, 0.9, lock=False)
        if t < L[1] - 0.2:
            board(g, 740, 820, 0.6, k=0.85, t=t)
            person(g, 330, GROUND, ROC_DELEGATE, 0.75, mood="worry", pose="down", turn=0.3, seed=4)
            title(g, t, L[0], "ผลโหวตไม่อาจต้านทาน", INK, 80)
        elif t < L[2] - 0.2:
            person(g, 330, GROUND, ROC_DELEGATE, 0.75, mood="sad", pose="down", turn=0.6, seed=4)
            title(g, t, L[1], "ผู้แทนไต้หวันลุกขึ้นยืน", NAVY, 80)
        else:
            u = e_io(seg(t, L[2], L[3] - 0.3))
            x = lerp(330, 860, u)
            person(g, x, GROUND, ROC_DELEGATE, 0.75 * (1 - 0.25 * u), mood="sad", pose="down", turn=0.9, seed=4,
                   lean=4 * math.sin(t * 8))
            title(g, t, L[2], "เดินออกไปอย่างเงียบงัน...", GREY, 80)
        return
    if t < L[4] - 0.2:   # ประธานกำลังจะประกาศผล
        rostrum(g, CX, GROUND, 1.1)
        gavel(g, CX + 40, 840, 1.2 * ap(t, L[3]) + 0.01, lerp(-40, 10, e_io(seg(t, L[3] + 0.6, L[3] + 1.0))))
        title(g, t, L[3], "ก่อนประกาศผลเพียงเสี้ยววินาที", INK, 72)
        return
    if t < L[5] - 0.2:   # ปรบมือ เฮลั่น
        delegates(g, t, mood="smile", pose="v", talk=True)
        for i in range(5):
            g.label("เฮ!", 150 + i * 200, 620 - 30 * abs(math.sin(t * 5 + i)), 56, color=RED, sc=ap(t, L[4] + 0.1 * i))
        title(g, t, L[4], "ปรบมือ เฮลั่น!", RED, 96)
        return
    delegates(g, t, dance=True)   # เต้นฉลอง
    for i in range(6):
        u = (t * 0.6 + i / 6) % 1
        g.star(100 + i * 170, 560 + 300 * u, 22, [GOLD2, RED, UN_BLUE][i % 3], 4, rot=t * 90)
    title(g, t, L[5], "เต้นระบำฉลองชัย!", GREEN, 92)


# ------------------------------------------------------------------ 6. after
def s_after(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:
        ballot(g, CX, 820, 1.5 * ap(t, L[0]) + 0.01, 4 * math.sin(t * 2))
        g.sparkle(CX + 200, 600, 40)
        title(g, t, L[0], "ข้อมติเพียงฉบับเดียว", INK, 84)
        return
    if t < L[2] - 0.2:   # ริบเก้าอี้ ไต้หวันออกจาก UN
        u = e_io(seg(t, L[1] + 0.3, L[2] - 0.5))
        seat(g, 700, GROUND, 1.0, 0, "CHINA")
        g.line([(260, GROUND), (260, 500)], 8, hexc("#8a8a8a"), amp=0)
        flag(g, 260, lerp(520, 1000, u), 240, "roc", t, pole=False)
        title(g, t, L[1], "ไต้หวันออกจากสหประชาชาติ", NAVY, 76)
        return
    if t < L[4] - 0.2:   # ปักกิ่ง -> มหาอำนาจ + วีโต้
        person(g, 280, GROUND, MAO, 0.8, mood="smile", pose="wave" if t < L[3] else "point", turn=0.3, seed=6)
        if t < L[3] - 0.2:
            flag(g, 600, 560, 280, "prc", t, k=ap(t, L[2]))
            title(g, t, L[2], "ปักกิ่งก้าวขึ้นเป็นมหาอำนาจ", CNRED, 76)
        else:
            veto_stamp(g, 720, 800, 1.2 * ap(t, L[3]) + 0.01)
            title(g, t, L[3], "มีสิทธิ์วีโต้บนเวทีโลก", RED, 80)
        return
    island(g, CX, 960, 1.4, t)   # โดดเดี่ยวทางการทูต
    if t < L[5] - 0.2:
        title(g, t, L[4], "ภาวะโดดเดี่ยวทางการทูต", NAVY, 80)
    else:
        title(g, t, L[5], "จนถึงทุกวันนี้", INK, 96)
        g.label("1971 → 2026", CX, 560, 70, color=GOLDTXT, sc=ap(t, L[5] + 0.3))


# ------------------------------------------------------------------ 7. lesson
def s_lesson(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # การทูตและภูมิรัฐศาสตร์ = กระดานหมากรุก
        with g.at(CX, 900, ap(t, L[0]), -4):
            for r in range(4):
                for k in range(6):
                    g.rrect(-300 + k * 100, -200 + r * 100, 100, 100, 0, INK if (r + k) % 2 else WHITE, 3)
        for i, (x, col) in enumerate(((330, CNRED), (540, UN_BLUE), (750, NAVY))):
            with g.at(x, 760 - 20 * abs(math.sin(t * 3 + i)), ap(t, L[1] + 0.2 * i)):
                g.circle(0, -60, 34, col, 5)
                g.poly([(-40, 40), (40, 40), (20, -40), (-20, -40)], col, 5)
        if t < L[1] - 0.2:
            title(g, t, L[0], "เรื่องนี้พิสูจน์ว่า...", INK, 88)
        else:
            title(g, t, L[1], "โลกของการทูตและภูมิรัฐศาสตร์", PURPLE, 72)
        return
    if t < L[3] - 0.2:   # ไม่มีมิตรแท้ ไม่มีสถานะค้ำฟ้า
        for i, (txt, col) in enumerate((("ไม่มีมิตรแท้", RED), ("ไม่มีสถานะค้ำฟ้า", NAVY))):
            with g.at(CX, 700 + i * 260, ap(t, L[2] + 0.6 * i), -3 + 6 * i):
                g.rrect(-320, -90, 640, 180, 40, WHITE, 8, stroke=col)
                g.label(txt, 0, 0, 70, color=col)
        title(g, t, L[2], "บทเรียน", GOLDTXT, 96)
        return
    with g.at(CX, 820, ap(t, L[3])):   # ผลประโยชน์เขียนกฎ
        g.rrect(-240, -300, 480, 600, 12, WHITE, 7)
        g.label("กฎเกณฑ์", 0, -220, 60, color=INK)
        for i in range(5):
            g.line([(-180, -120 + i * 70), (180 - 50 * (i % 2), -120 + i * 70)], 6, GREY, amp=0)
        with g.at(150 + 30 * math.sin(t * 6), 80, 1, 30):
            g.rrect(-14, -200, 28, 220, 8, GOLD, 5)
    title(g, t, L[3], "ผลประโยชน์คือผู้เขียนกฎ", RED, 80)


# ------------------------------------------------------------------ 8. outro
def s_outro(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # มองอย่างไร? การตัดสินใจของ UN
        emblem(g, CX, 820, 170 * ap(t, L[0]) + 1, t)
        if t < L[1] - 0.2:
            title(g, t, L[0], "ทุกคนมองเหตุการณ์นี้อย่างไร?", INK, 72)
        else:
            title(g, t, L[1], "การตัดสินใจของ UN ในวันนั้น", UN_BLUE, 74)
        return
    if t < L[4] - 0.2:   # ยอมรับความจริงตามประชากร หรือ อยุติธรรมต่อผู้ร่วมก่อตั้ง
        for i, (txt, col, kind) in enumerate((("ยอมรับความจริง\nตามประชากร", GREEN, "prc"),
                                              ("อยุติธรรม\nต่อผู้ร่วมก่อตั้ง", RED, "roc"))):
            y = 620 + i * 440
            k = ap(t, L[2] if i == 0 else L[3])
            if k < 0.02:
                continue
            with g.at(CX + 15 * math.sin(t * 3 + i), y, k, -3 + 6 * i):
                g.rrect(-330, -150, 660, 300, 40, WHITE, 8, stroke=col)
                for j, line in enumerate(txt.split("\n")):
                    g.label(line, 0, -45 + j * 90, 66, color=col)
        g.label("หรือ", CX, 840, 70, sc=ap(t, L[3]))
        title(g, t, L[2], "คุณมองแบบไหน?", PURPLE, 88, y=330)
        return
    with g.at(CX + 170, 640, ap(t, L[4])):   # ชวนคอมเมนต์
        g.bubble(0, 0, 460, 220, WHITE, tail=(-1, 1))
        for i in range(3):
            g.circle(-110 + i * 110, 0, 24 + 6 * math.sin(t * 6 - i), INK, 0)
    person(g, 250, GROUND, DELEGATES[1], 0.75, mood="smile", pose="wave", turn=0.3, seed=70, talk=True)
    title(g, t, L[4], "คอมเมนต์แลกเปลี่ยนกันได้เลย!", RED, 64)


SCENES = {
    "hook": s_hook, "night": s_night, "seat": s_seat, "vote": s_vote, "walkout": s_walkout, "after": s_after,
    "lesson": s_lesson, "outro": s_outro,
}
NO_IRIS = set()
