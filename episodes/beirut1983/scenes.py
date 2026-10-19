"""ฉากตอน: ระเบิดค่ายทหารกองกำลังรักษาสันติภาพ เบรุต (23 ต.ค. 1983) — โทนสุภาพ ไม่แสดงความรุนแรง"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from chars import (MARINES, PARAS, RESCUE, barracks, barrier, bunk, candle, clock, dust, fence, flag_fr,  # noqa: E402
                   flag_lb, flash, memorial, mushroom, sandbags, scale, ship, skyline, sky, sun, truck)
from gfx import GOLD2, GREY, INK, NAVY, RED, W, WHITE, e_in, e_io, e_out, hexc, lerp, pop, seg  # noqa: E402
from people import person  # noqa: E402

CX = W / 2
GROUND = 1270
GOLDTXT = hexc("#b37a12")
GREEN = hexc("#3c8d4f")
FRB = hexc("#2b4c9a")

CAMERA = {"hook": "push_in", "peace": "pan_right", "truck": "pan_left", "collapse": "tilt_down", "toll": "pull_out",
          "legacy": "pan_right", "lesson": "push_in", "outro": "pan_left"}
TRANSITIONS = {"peace": "fade", "truck": "whip", "collapse": "zoom", "toll": "fade", "legacy": "iris",
               "lesson": "fade", "outro": "zoom"}


def ap(t, a, dur=0.38):
    return pop(t, a - 0.2, dur)


def soldier(g, x, look, sc=0.6, mood="neutral", pose="down", turn=0.0, seed=0):
    person(g, x, GROUND, look, sc, mood=mood, pose=pose, turn=turn, seed=seed)


def dove(g, x, y, sc=1.0, t=0.0):
    from people import _shade, _smooth_path
    c = g.c
    fl = abs(math.sin(t * 8))
    with g.at(x, y, sc):
        _smooth_path(c, [(-70, 0), (-20, -30), (50, -24), (90, -40), (80, -10), (40, 20), (-40, 20)])
        _shade(c, WHITE, 5, 0.15)
        _smooth_path(c, [(-10, -20), (-40, -90 * (0.4 + 0.6 * fl)), (30, -70 * (0.4 + 0.6 * fl)), (30, -20)])
        _shade(c, WHITE, 5, 0.2)
        g.circle(70, -30, 5, INK, 0)
        g.line([(95, -34), (140, -20)], 5, GREEN, amp=0)   # กิ่งมะกอก
        for i in range(3):
            g.circle(108 + i * 14, -32 + i * 4, 7, GREEN, 2)


# ------------------------------------------------------------------ 1. hook
def s_hook(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # วันที่ + เวลา 6:22
        sky(g, 0.8)
        sun(g, 820, 1150, 70, t)
        mm = 22 if t > L[1] - 0.2 else int(lerp(0, 22, e_out(seg(t, 0.4, 2.0))))
        clock(g, CX, 800, 210, 6, mm, pop(t, 0.3))
        if t < L[1] - 0.2:
            g.label("วันนี้ในอดีต", CX, 380, 104, sc=lerp(2.0, 1, e_out(seg(t, 0.1, 0.4))) if t > 0.1 else 0, rot=-3)
            g.label("23 ตุลาคม 1983", CX, 520, 84, color=RED, sc=pop(t, 0.8))
        else:
            g.label("06:22 น.", CX, 400, 120, color=NAVY, sc=ap(t, L[1]), rot=-3)
        return
    if t < L[5] - 0.2:   # เบรุตยามเช้า -> ระเบิด -> ควันดอกเห็ด
        sky(g, 1.0)
        sun(g, 200, 900, 60, t)
        boom = t > L[3] - 0.2
        sh = 8 * math.sin(t * 40) * max(0.0, 1 - (t - L[3]) / 1.5) if boom else 0
        with g.at(sh, 0):
            skyline(g, GROUND, t)
        if t < L[3] - 0.2:
            flag_lb(g, 830, 560, 150, 100, t)
            g.label("กรุงเบรุต ประเทศเลบานอน", CX, 380, 76, color=NAVY, sc=ap(t, L[2]), rot=-3)
            g.label("เงียบสงบ...", CX, 500, 60, color=GREY, sc=ap(t, L[2] + 0.6))
            return
        flash(g, 560, 1000, 700, seg(t, L[3] - 0.2, L[3] + 1.0))
        mushroom(g, 560, GROUND, e_out(seg(t, L[3] + 0.3, L[4] + 1.5)), t, 1.0)
        if t < L[4] - 0.2:
            g.label("เสียงระเบิดกึกก้อง!", CX, 380, 92, color=RED, sc=ap(t, L[3]), rot=-3)
        else:
            g.label("ควันรูปดอกเห็ดยักษ์", CX, 380, 84, color=GREY, sc=ap(t, L[4]), rot=-3)
        return
    sq = e_in(seg(t, L[6] - 0.4, L[6] + 0.6))   # ค่ายรักษาสันติภาพ -> สุสานคอนกรีต
    barracks(g, CX, GROUND, 0.95, 4, sq, "us", t)
    if sq > 0:
        dust(g, CX, GROUND - 100, 220, t, 8, 0.8)
    if t < L[6] - 0.2:
        g.label("ค่ายกองกำลังรักษาสันติภาพ", CX, 340, 72, color=NAVY, sc=ap(t, L[5]), rot=-3)
    else:
        g.label("สุสานคอนกรีตในพริบตา", CX, 340, 80, color=RED, sc=ap(t, L[6]), rot=-3)


# ------------------------------------------------------------------ 2. peace
def s_peace(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # นาวิกโยธินสหรัฐ + พลร่มฝรั่งเศส = กองกำลังรักษาสันติภาพ
        for i, lk in enumerate(MARINES[:2]):
            soldier(g, 150 + i * 190, lk, 0.62, "smile", "salute" if i == 0 and t > L[1] else "down", 0.2, 10 + i)
        for i, lk in enumerate(PARAS):
            soldier(g, 740 + i * 190, lk, 0.62, "smile", "down", -0.2, 20 + i)
        g.line([(250, 640), (250, 470)], 6, INK, amp=0)
        g.flag(250, 470, 130, 84, "us", t)
        g.line([(830, 640), (830, 470)], 6, INK, amp=0)
        flag_fr(g, 830, 470, 130, 84, t)
        if t < L[1] - 0.2:
            g.label("นาวิกโยธินสหรัฐฯ", 260, 1150, 44, color=NAVY, sc=ap(t, 0.3))
            g.label("พลร่มฝรั่งเศส", 830, 1150, 44, color=FRB, sc=ap(t, 0.6))
        else:
            dove(g, CX + 20 * math.sin(t), 560 + 20 * math.sin(t * 2), 1.1 * ap(t, L[1]), t)
            g.label("กองกำลังรักษาสันติภาพนานาชาติ", CX, 360, 62, color=GREEN, sc=ap(t, L[1]), rot=-3)
        return
    if t < L[3] - 0.2:   # ยุติสงครามกลางเมือง
        skyline(g, GROUND, t, 0.6)
        for i, x in enumerate((200, 760)):
            dust(g, x, 900, 120, t, 5, 0.5, i * 0.3)
        flag_lb(g, CX - 150, 600, 300, 200, t)
        g.label("สงครามกลางเมืองเลบานอน", CX, 380, 72, color=RED, sc=ap(t, L[2]), rot=-3)
        return
    if t < L[4] - 0.2:   # เช้าวันอาทิตย์
        sky(g, 0.7)
        sun(g, CX, 900, 120, t)
        with g.at(CX, 640, ap(t, L[3])):
            g.rrect(-200, -120, 400, 240, 24, WHITE, 7)
            g.rrect(-200, -120, 400, 80, 24, RED, 7)
            g.text("ตุลาคม 1983", 0, -80, 38, "kanit", WHITE)
            g.label("อาทิตย์ 23", 0, 40, 70)
        g.label("เช้าวันอาทิตย์ที่สงบสุข", CX, 360, 76, color=GOLDTXT, sc=ap(t, L[3]), rot=-3)
        return
    for i, lk in enumerate(MARINES[:2]):   # ทหารยังหลับอยู่
        bunk(g, 280 + i * 520, GROUND, 0.85, t + i, lk)
    g.label("ทหารส่วนใหญ่ยังหลับอยู่", CX, 360, 78, color=NAVY, sc=ap(t, L[4]), rot=-3)


# ------------------------------------------------------------------ 3. truck
def s_truck(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # ฝันร้าย: รถบรรทุกพุ่งเข้ามา
        if t < L[1] - 0.2:
            k = e_in(seg(t, 0, L[1]))
            truck(g, lerp(1300, 760, k), GROUND, lerp(0.35, 0.6, k), t, 1.0)
            g.label("ฝันร้ายพุ่งตรงเข้ามา...", CX, 380, 80, color=RED, sc=ap(t, 0.2), rot=-3)
            return
        truck(g, 500 + 10 * math.sin(t * 3), GROUND, 0.95, t, 1.0)
        with g.at(CX, 620, ap(t, L[1] + 0.3), -4):
            g.rrect(-280, -80, 560, 160, 24, WHITE, 8, stroke=RED)
            g.label("≈ TNT เกือบ 10 ตัน", 0, 0, 60, color=RED)
        g.label("รถบรรทุกระเบิด", CX, 380, 86, sc=ap(t, L[1]), rot=-3)
        return
    if t < L[3] - 0.2:   # พุ่งฝ่ารั้วลวดหนามและกระสอบทราย
        k = e_in(seg(t, L[2], L[3] - 0.3))
        brk = k > 0.55
        fence(g, -200, 1300, GROUND, (430, 700) if brk else None)
        sandbags(g, 760, GROUND, 4, 3, 0.8, e_out(seg(t, L[2] + 1.6, L[2] + 2.4)) if brk else 0.0)
        truck(g, lerp(-300, 1000, k), GROUND, 0.75, t, 1.0)
        g.label("ฝ่ารั้วลวดหนาม + กระสอบทราย", CX, 380, 66, color=RED, sc=ap(t, L[2]), rot=-3)
        return
    if t < L[4] - 0.2:   # ยามพยายามสกัด แต่สายเกินไป
        with g.at(220, GROUND):
            g.rrect(-110, -420, 220, 420, 10, hexc("#d8d3c7"), 6)
            g.rrect(-80, -360, 160, 120, 6, hexc("#bcd6e6"), 5)
        soldier(g, 380, MARINES[2], 0.62, "shock", "stop", 0.4, 30)
        k = e_in(seg(t, L[3], L[4]))
        truck(g, lerp(1300, 600, k), GROUND, 0.55, t, 1.0)
        g.label("!", 380, 560, 110, color=RED, sc=ap(t, L[3] + 0.2))
        g.label("ยามพยายามสกัด... สายเกินไป!", CX, 380, 66, color=RED, sc=ap(t, L[3]), rot=-3)
        return
    barracks(g, 640, GROUND, 0.85, 4, 0.0, "us", t)   # พุ่งเข้าล็อบบี้
    k = e_in(seg(t, L[4], L[5] - 0.2))
    if k < 0.98:
        with g.alpha(1 - max(0.0, (k - 0.75) * 4)):
            truck(g, lerp(-200, 560, k), GROUND, 0.45, t, 1.0)
    if t < L[5] - 0.2:
        g.label("พุ่งชนเข้าล็อบบี้อาคาร", CX, 360, 78, color=RED, sc=ap(t, L[4]), rot=-3)
        return
    flash(g, 640, GROUND - 200, 800, seg(t, L[5] - 0.1, L[5] + 1.0))
    dust(g, 640, GROUND - 120, 250, t, 8, 0.85)
    g.label("ระเบิดพลีชีพ", CX, 360, 92, color=RED, sc=ap(t, L[5]), rot=-3)


# ------------------------------------------------------------------ 4. collapse
def s_collapse(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # ตึก 4 ชั้นถล่มแบนเป็นหน้ากลอง
        sq = e_in(seg(t, L[1] - 0.1, L[1] + 0.7))
        barracks(g, CX, GROUND, 1.0, 4, sq, "us", t)
        if t < L[1] - 0.2:
            for f in range(4):
                g.label(f"ชั้น {f + 1}", CX - 420, GROUND - 65 - f * 130, 40, color=GREY, sc=ap(t, 0.3 + 0.25 * f))
            g.label("ตึกคอนกรีต 4 ชั้น", CX, 360, 86, sc=ap(t, 0.2), rot=-3)
        else:
            dust(g, CX, GROUND - 100, 260, t, 9, 0.85)
            g.label("ถล่มแบนเป็นหน้ากลอง", CX, 360, 82, color=RED, sc=ap(t, L[1]), rot=-3)
        return
    if t < L[3] - 0.2:   # ไม่กี่นาทีต่อมา: รถคันที่สอง
        clock(g, 300, 760, 150, 6, int(lerp(22, 26, seg(t, L[2], L[3]))), ap(t, L[2]))
        truck(g, lerp(1200, 820, e_out(seg(t, L[2], L[3]))), GROUND, 0.55, t, 1.0)
        g.label("ไม่กี่นาทีต่อมา... คันที่สอง", CX, 380, 74, color=RED, sc=ap(t, L[2]), rot=-3)
        return
    sq = e_in(seg(t, L[4] - 0.2, L[4] + 0.6))   # อาคารทหารฝรั่งเศส
    barracks(g, 700, GROUND, 0.8, 5, sq, "fr", t)
    g.line([(80, GROUND - 40), (420, GROUND - 40)], 5, GREY, amp=0)
    g.label("ห่างไม่กี่ กม.", 250, GROUND - 90, 42, color=GREY, sc=ap(t, L[3] + 0.5))
    if t < L[4] - 0.2:
        g.label("อาคารที่พักทหารฝรั่งเศส", CX, 360, 76, color=FRB, sc=ap(t, L[3]), rot=-3)
    else:
        dust(g, 700, GROUND - 100, 230, t, 8, 0.85, 0.4)
        g.label("ถล่มลงมาเช่นกัน", CX, 360, 86, color=RED, sc=ap(t, L[4]), rot=-3)


# ------------------------------------------------------------------ 5. toll
def s_toll(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # ฝุ่นควัน / ขุดซากด้วยน้ำตา
        barracks(g, CX, GROUND, 0.95, 4, 1.0, "us", t)
        dust(g, CX, GROUND - 60, 300, t, 10, 0.7 if t < L[1] - 0.2 else 0.4)
        if t > L[1] - 0.2:
            for i, lk in enumerate(RESCUE + [MARINES[0]]):
                x = 200 + i * 340
                person(g, x, GROUND, lk, 0.6, mood="sad", pose="hold", turn=0.3 - 0.3 * i, seed=40 + i,
                       k=0.5 + 0.5 * math.sin(t * 3 + i))
            g.label("ขุดซากทั้งน้ำตา", CX, 380, 86, color=NAVY, sc=ap(t, L[1]), rot=-3)
        else:
            g.label("ฝุ่นควันหนาทึบ", CX, 380, 90, color=GREY, sc=ap(t, 0.2), rot=-3)
        return
    if t < L[4] - 0.2:   # 241 + 58
        memorial(g, CX, GROUND, 1.0, 7, seg(t, L[2], L[2] + 1.5))
        n1 = int(241 * e_out(seg(t, L[2], L[2] + 1.6)))
        with g.at(330, 680, ap(t, L[2])):
            g.flag(-80, -230, 160, 100, "us", t)
            g.label(str(n1), 0, 20, 150, color=NAVY)
            g.label("ทหารสหรัฐฯ", 0, 130, 44, color=GREY)
        if t > L[3] - 0.2:
            n2 = int(58 * e_out(seg(t, L[3], L[3] + 1.2)))
            with g.at(770, 680, ap(t, L[3])):
                flag_fr(g, -80, -230, 160, 100, t)
                g.label(str(n2), 0, 20, 150, color=FRB)
                g.label("ทหารฝรั่งเศส", 0, 130, 44, color=GREY)
        g.label("ชีวิตที่สูญเสีย", CX, 360, 86, sc=ap(t, L[2]), rot=-3)
        return
    memorial(g, CX, GROUND, 1.1, 7, 1.0)   # สูญเสียมากที่สุดในวันเดียว
    hk = e_io(seg(t, L[4], L[4] + 1.5))
    g.line([(860, GROUND - 150), (860, 520)], 8, INK, amp=0)
    g.flag(860, lerp(520, 700, hk), 140, 90, "us", t)   # ลดธงครึ่งเสา
    candle(g, 160, GROUND - 160, 0.8, t)
    if t < L[5] - 0.2:
        g.label("สูญเสียมากที่สุดในวันเดียว", CX, 360, 70, color=RED, sc=ap(t, L[4]), rot=-3)
    else:
        g.label("นับตั้งแต่สงครามโลกครั้งที่ 2", CX, 360, 70, color=NAVY, sc=ap(t, L[5]), rot=-3)


# ------------------------------------------------------------------ 6. legacy
def s_legacy(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # ช็อกทั้งโลก / จุดเปลี่ยนยุทธศาสตร์
        for i in range(3):
            lk = (MARINES[2], PARAS[1], RESCUE[0])[i]
            person(g, 180 + i * 360, GROUND, lk, 0.62, mood="shock" if t < L[1] else "worry",
                   pose="phone" if i == 1 else "down", turn=0.2 - 0.2 * i, seed=50 + i)
        for i in range(3):
            u = (t * 0.6 + i / 3) % 1
            g.label("!", 260 + i * 300, 640 - 100 * u, 80, color=RED, a=1 - u)
        if t < L[1] - 0.2:
            g.label("ช็อกและโกรธแค้นทั้งโลก", CX, 360, 76, color=RED, sc=ap(t, 0.2), rot=-3)
        else:
            g.label("จุดเปลี่ยนยุทธศาสตร์ทางทหาร", CX, 360, 66, color=NAVY, sc=ap(t, L[1]), rot=-3)
        return
    if t < L[3] - 0.2:   # สหรัฐฯ ถอนทหาร
        g.c.rectangle(-500, GROUND - 60, 2100, 150)
        g.c.set_source_rgba(0.74, 0.84, 0.9, 1)
        g.c.fill()
        ship(g, lerp(560, 860, e_io(seg(t, L[2], L[3]))), GROUND - 40, 1.0, t)
        g.label("สหรัฐฯ ถอนทหารทั้งหมด", CX, 360, 80, color=NAVY, sc=ap(t, L[2]), rot=-3)
        g.label("ก.พ. 1984", CX, 480, 52, color=GREY, sc=ap(t, L[2] + 0.5))
        return
    skyline(g, GROUND, t, 0.5)   # ระเบิดพลีชีพ -> แบริเออร์คอนกรีตทั่วโลก
    for i in range(6):
        barrier(g, 110 + i * 175, GROUND + 10, 1.0 * ap(t, L[4] + 0.15 * i) if t > L[4] - 0.4 else 0)
    if t < L[4] - 0.2:
        with g.at(CX, 720, ap(t, L[3])):
            g.poly([(0, -200), (210, 160), (-210, 160)], hexc("#f2c94c"), 8, amp=0)
            g.label("!", 0, 40, 160)
        g.label('ความน่ากลัวของ "ระเบิดพลีชีพ"', CX, 360, 66, color=RED, sc=ap(t, L[3]), rot=-3)
    else:
        g.label("อาวุธร้ายแรงในสงครามยุคใหม่", CX, 360, 66, color=RED, sc=ap(t, L[4]), rot=-3)
        g.label("แท่งกันรถพุ่งชน มีทั่วโลก", CX, 480, 48, color=GREY, sc=ap(t, L[4] + 0.6))


# ------------------------------------------------------------------ 7. lesson
def s_lesson(g, t, L, d):
    g.ground(GROUND, WHITE)
    g.label("บทเรียน", CX, 340, 100, sc=ap(t, 0.2), rot=-3)
    memorial(g, CX, GROUND, 0.9, 7, 1.0)
    for i, x in enumerate((140, 940)):
        candle(g, x, GROUND - 10, 0.8, t + i)
    if t < L[2] - 0.2:
        dove(g, CX + 40 * math.sin(t * 0.8), 700 + 20 * math.sin(t * 2), 1.4 * ap(t, 0.3), t)
        if t > L[1] - 0.2:
            g.label("ความขัดแย้งของสงคราม", CX, 490, 60, color=GREY, sc=ap(t, L[1]))
        return
    soldier(g, CX, MARINES[0], 0.66, "sad", "salute", 0.0, 60)
    dove(g, CX + 260, 520 + 20 * math.sin(t * 2), 0.8, t)
    if t < L[3] - 0.2:
        g.label("จ่ายราคาแพงที่สุดด้วยชีวิต", CX, 480, 60, color=RED, sc=ap(t, L[2]))
    else:
        g.label("ผู้ที่ถูกส่งไปรักษาสันติภาพ", CX, 480, 60, color=GREEN, sc=ap(t, L[3]))


# ------------------------------------------------------------------ 8. outro
def s_outro(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[5] - 0.2:
        if t < L[1] - 0.2:
            for i, lk in enumerate((MARINES[1], PARAS[0])):
                soldier(g, 300 + i * 480, lk, 0.7, "neutral", "think" if i == 0 else "down", 0.3 - 0.6 * i, 70 + i)
            g.label("คิดเห็นอย่างไร?", CX, 360, 96, sc=ap(t, 0.2), rot=-3)
            return
        tilt = 0.6 * math.sin(t * 1.3)
        scale(g, CX, GROUND - 120, 1.0 * ap(t, L[1]), tilt, "", "", t)
        with g.at(CX - 300 * math.cos(math.radians(12 * tilt)), 960 + 300 * math.sin(math.radians(12 * tilt)),
                  ap(t, L[2])):
            dove(g, 0, -30, 0.6, t)
            g.label("ส่งกองกำลัง", 0, 60, 44, color=GREEN)
            g.label("รักษาสันติภาพ", 0, 112, 38, color=GREEN)
        with g.at(CX + 300 * math.cos(math.radians(12 * tilt)), 960 - 300 * math.sin(math.radians(12 * tilt)),
                  ap(t, L[4])):
            flag_lb(g, -60, -80, 120, 80, t)
            g.label("ให้คนในชาติ", 0, 60, 44, color=RED)
            g.label("แก้ปัญหากันเอง", 0, 112, 38, color=RED)
        if t < L[3] - 0.2:
            g.label("ความขัดแย้งที่หยั่งรากลึก", CX, 360, 70, sc=ap(t, L[1]), rot=-3)
        else:
            g.label("คุ้มค่ากับความสูญเสียไหม?", CX, 360, 74, color=GOLDTXT, sc=ap(t, L[3]), rot=-3)
        return
    with g.at(CX + 170, 640, ap(t, L[5])):   # ชวนคอมเมนต์
        g.bubble(0, 0, 460, 220, WHITE, tail=(-1, 1))
        for i in range(3):
            g.circle(-110 + i * 110, 0, 24 + 6 * math.sin(t * 6 - i), INK, 0)
    soldier(g, 250, MARINES[1], 0.78, "smile", "wave", 0.3, 80)
    g.label("คอมเมนต์แลกเปลี่ยนกันได้เลย", CX, 360, 70, color=RED, sc=ap(t, L[5]), rot=-3)


SCENES = {
    "hook": s_hook, "peace": s_peace, "truck": s_truck, "collapse": s_collapse, "toll": s_toll,
    "legacy": s_legacy, "lesson": s_lesson, "outro": s_outro,
}
NO_IRIS = set()
