"""ฉากตอน: วันสุดท้ายของกัดดาฟี (20 ต.ค. 2011)  — ฟังก์ชันรับ (g, t, L, d)
ไม่แสดงภาพความรุนแรง: การโจมตี = แสง/ควัน, การจับตัว = เงาและท่อว่าง
"""
import math
import os
import sys

import cairo

sys.path.insert(0, os.path.dirname(__file__))
from chars import (CITY, culvert, gaddafi, goat, green_book, guard, idris, jet, libya_map,  # noqa: E402
                   nasser, pickup, tent)
from fx import confetti  # noqa: E402
from gfx import (BLUE, BROWN2, GOLD, GOLD2, GREY, ICE, INK, LGREY, LYGREEN, NAVY, RED,  # noqa: E402
                 SAND, SAND2, W, WHITE, e_back, e_in, e_io, e_out, hn, lerp, pop, seg, spring)

CX = W / 2
GROUND = 1180


def dim(g, a, y1=GROUND):
    """โทนมืด/เศร้า: ท้องฟ้าเหนือพื้นเป็นสีเทา (พื้นล่างยังขาวเพื่อเว้นที่ให้ซับ)"""
    if a > 0:
        grad = cairo.LinearGradient(0, -500, 0, y1 + 60)
        grad.add_color_stop_rgba(0, 0.12, 0.12, 0.14, a)
        grad.add_color_stop_rgba(0.75, 0.12, 0.12, 0.14, a * 0.8)
        grad.add_color_stop_rgba(1, 0.12, 0.12, 0.14, 0)
        g.c.rectangle(-500, -500, W + 1000, y1 + 560)
        g.c.set_source(grad)
        g.c.fill()


def dunes(g, y, seed=1):
    g.poly([(-400, y)] + [(x, y - 60 - 40 * math.sin(x * 0.006 + seed)) for x in range(-400, W + 401, 80)]
           + [(W + 400, y)], SAND2, 6, seed=seed, smooth=True)
    g.ground(y, WHITE, seed=seed)


def smoke(g, x, y, t, t0, n=6, s=1.0):
    tt = t - t0
    if tt < 0:
        return
    for i in range(n):
        p = (tt * 0.35 + i / n) % 1
        a = math.sin(p * math.pi) * 0.85
        with g.alpha(a):
            g.blob(x + 30 * hn(i, 2) + 40 * p, y - 260 * p, (40 + 50 * p) * s, (34 + 44 * p) * s, LGREY, 5, i)


def flash(g, x, y, t, t0, label="ตูม!"):
    tt = t - t0
    if 0 <= tt < 0.9:
        k = e_out(seg(tt, 0, 0.25))
        a = 1 - seg(tt, 0.35, 0.9)
        with g.alpha(a):
            g.star(x, y, 180 * k, GOLD2, 7, pts=10, inner=0.55)
            g.star(x, y, 100 * k, WHITE, 5, pts=8, inner=0.6)
    g.text(label, x, y - 210, 110, "kanit", RED, sc=pop(t, t0 + 0.05) * (1 - seg(t, t0 + 1.4, t0 + 1.8)), rot=-8)


def year_badge(g, t, t0, x, y, txt):
    k = pop(t, t0)
    if k > 0:
        with g.at(x, y, k, -6):
            g.rrect(-150, -60, 300, 120, 40, GOLD2, 8)
            g.text(txt, 0, -2, 80, "kanit")


# ------------------------------------------------------------------ 1. cold open (ตึงเครียด)
def s_cold_open(g, t, L, d):
    to_pipe = e_io(seg(t, L[3] + 1.2, L[4] - 0.2))   # กล้องค่อย ๆ ซูมเข้าท่อ
    zoom = lerp(1.0, 1.9, to_pipe)
    with g.at(CX, 1050, zoom):
        with g.at(-CX, -1050):
            sun = e_out(seg(t, 0, 2.5))
            g.circle(820, 900 - 160 * sun, 90, GOLD2, 7)
            dunes(g, 1000)
            culvert(g, CX, 1050 + 160, 0.9)
            # ขบวนรถ
            if t < L[3] + 1.0:
                for i in range(4):
                    px = lerp(-300, 1300, seg(t, L[1] - 0.5 + i * 0.35, L[2] + 2.2 + i * 0.35)) - i * 40
                    pickup(g, px, 965 + (i % 2) * 20, 0.8, t, seed=i)
                    for k in range(3):
                        with g.alpha(0.5):
                            g.blob(px - 120 - k * 40, 950 - k * 8, 26 + k * 6, 18 + k * 4, SAND2, 0, k + i)
            # เครื่องบิน + การโจมตี (ไม่แสดงความรุนแรง: แสงวาบ + ควัน)
            if L[2] - 0.3 < t < L[2] + 2.5:
                k = seg(t, L[2] - 0.3, L[2] + 1.6)
                jet(g, lerp(1300, -300, k), lerp(380, 520, k), 0.9, rot=-6)
            flash(g, 760, 900, t, L[2] + 0.8)
            if t < L[3] + 1.2:
                with g.alpha(1 - seg(t, L[3] + 0.4, L[3] + 1.2)):
                    smoke(g, 760, 960, t, L[2] + 0.9, 7, 1.0)
            # เงาชายชราวิ่งเข้าท่อ
            if L[3] - 0.2 < t < L[3] + 2.6:
                k = e_io(seg(t, L[3] - 0.2, L[3] + 2.0))
                fx, fy = lerp(150, CX - 90, k), lerp(1010, 1150, k)
                sc = lerp(0.5, 0.3, k)
                with g.silhouette(INK, 0.95):
                    gaddafi(g, fx, fy, sc, look="old", shades=False, rot=8 * math.sin(t * 14))
            if L[3] + 2.6 <= t:   # ตาคู่หนึ่งในความมืดของท่อ
                blink = (t * 0.7 % 2.5) < 0.12
                for sx in (-1, 1):
                    g.circle(CX - 90 + sx * 14, 1150, 6 if not blink else 1.5, WHITE, 0)
    if t > L[4] - 0.1:
        k = pop(t, L[4])
        with g.at(CX, 520, k, -4):
            g.rrect(-260, -110, 520, 220, 50, WHITE, 9)
            g.text("ปกครอง 42 ปี", 0, -5, 96, "kanit", RED)
    if t > L[5] - 0.1:
        g.text("?", CX + 300, 760, 220, "kanit", RED, sc=pop(t, L[5]), rot=10 * math.sin(t * 2))
    g.text("สิรต์, ลิเบีย", 220, 330, 56, "kanit", sc=pop(t, L[0] + 0.3) * (1 - seg(t, L[1], L[1] + 0.3)))
    g.text("20 ต.ค. 2011", 220, 260, 64, "kanit", RED, sc=pop(t, L[0]) * (1 - seg(t, L[1], L[1] + 0.3)))


# ------------------------------------------------------------------ 2. title
def s_title(g, t, L, d):
    g.sunburst(CX, 800, 240, 650, 24, t * 10, 14, LGREY)
    g.text("วันนี้ในอดีต", CX, 330, 104, "kanit", sc=lerp(2.0, 1, e_out(seg(t, 0.05, 0.3))) if t > 0.05 else 0,
           rot=-5, a=seg(t, 0.05, 0.15))
    g.text("20 ตุลาคม 2011", CX, 450, 84, "kanit", RED, sc=pop(t, 0.6))
    k = pop(t, L[1] - 0.2)
    if k > 0:
        with g.at(CX, 1060, k):
            g.c.save()
            g.c.scale(1, 1.12)
            g.circle(0, -220, 300, WHITE, 10)
            g.c.restore()
            gaddafi(g, 0, 50, 1.35, "happy", look="leader")
        g.name_tag(t, L[1] + 0.2, CX + 230, 700, "มูอัมมาร์ กัดดาฟี", "ผู้นำลิเบีย 1969–2011", dur=3.0)


# ------------------------------------------------------------------ 3. origins (อบอุ่น)
def s_origins(g, t, L, d):
    g.circle(860, 420, 80, GOLD2, 7)
    dunes(g, GROUND - 40, 3)
    tent(g, 300, GROUND - 20, 1.15)
    for i, gx in enumerate((640, 800, 930)):
        if t > 0.6 + i * 0.3:
            goat(g, gx + 60, GROUND + 60 + (i % 2) * 30, 1.0 * pop(t, 0.6 + i * 0.3), t, seed=i)
    kid_mood = "laugh" if t > L[2] else "happy"
    gaddafi(g, 600, GROUND + 90, 1.35 * pop(t, 0.5), kid_mood, look="kid", arm=0.6 if t > L[2] else 0.0)
    if t < L[2] - 0.3:
        year_badge(g, t, 0.25, 230, 520, "1942")
    if t > L[1] - 0.2:
        g.text("ชาวเบดูอิน", 330, GROUND + 70, 54, "kanit", sc=pop(t, L[1]) * (1 - seg(t, L[2] - 0.3, L[2])))
    if t > L[2] - 0.2:
        k = pop(t, L[2] - 0.2)
        with g.at(800, 690, k):
            for i, (bx, by, r) in enumerate([(-170, 230, 14), (-130, 190, 22)]):
                g.circle(bx, by, r, WHITE, 6)
            g.blob(0, 0, 210, 190, WHITE, 8, 9)
            nasser(g, 0, 10, 0.95)
        g.name_tag(t, L[2] + 0.3, 330, 470, "ญะมาล อับดุล นัสเซอร์", "ประธานาธิบดีอียิปต์", dur=2.6)
        for i in range(3):
            g.star(470 + i * 60, 820 - 40 * math.sin(t * 4 + i), 18, GOLD2, 4)


# ------------------------------------------------------------------ 4. coup (ตื่นเต้น)
def s_coup(g, t, L, d):
    night = seg(t, L[1] - 0.4, L[1] + 0.2) * (1 - seg(t, L[3] - 0.2, L[3] + 0.4))
    # พระราชวัง
    g.rrect(140, GROUND - 330, 800, 330, 10, WHITE, 8)
    g.c.move_to(400, GROUND - 330)
    g.c.curve_to(400, GROUND - 520, 680, GROUND - 520, 680, GROUND - 330)
    g.c.close_path()
    g.fs(GOLD2, 8)
    for k in range(5):
        g.rrect(190 + k * 150, GROUND - 260, 70, 120, 35, ICE, 5)
    g.rrect(860, GROUND - 650, 12, 330, 4, LGREY, 4)
    flag_k = e_io(seg(t, L[2] + 0.4, L[2] + 1.4))
    if flag_k < 1:
        g.flag(872, lerp(GROUND - 640, GROUND - 400, flag_k), 150, 95, "ly", t, 0.8)
    if flag_k > 0:
        g.flag(872, lerp(GROUND - 400, GROUND - 640, flag_k), 150, 95, "lyg", t, 0.8)
    g.ground(GROUND, WHITE)
    # กษัตริย์อิดริสโบกมือขึ้นเครื่องบินไปต่างประเทศ
    if t < L[1]:
        fly = seg(t, L[0] + 2.4, L[1] - 0.2)
        if fly <= 0:
            idris(g, 300, GROUND + 70, 0.95, "happy", wave=seg(t, 0.5, 2.0))
        else:
            jet(g, lerp(300, 1300, e_in(fly)), lerp(GROUND - 150, 300, e_in(fly)), 0.8, rot=-20)
        g.name_tag(t, 0.3, 330, 640, "กษัตริย์อิดริสที่ 1", "กษัตริย์องค์แรกและองค์เดียวของลิเบีย", dur=2.6)
        g.text("ไปรักษาพระองค์", 760, 520, 52, "kanit", sc=pop(t, 2.6) * (1 - seg(t, L[1] - 0.6, L[1] - 0.3)))
    dim(g, 0.45 * night)
    if night > 0:
        g.circle(900, 330, 60, GOLD2, 6)
    # ร้อยเอกหนุ่มบุก
    if t > L[1] - 0.3:
        k = e_out(seg(t, L[1] - 0.3, L[1] + 0.6))
        for i in range(3):
            g.soldier(lerp(-200, 120 + i * 95, k), GROUND + 160, 0.85, (0.72, 0.63, 0.42, 1), 300 + i)
        gaddafi(g, lerp(-100, 470, k), GROUND + 80, 0.9, "happy" if t < L[3] else "laugh", look="young",
                arm=e_back(seg(t, L[3], L[3] + 0.4)))
        year_badge(g, t, L[1], 230, 470, "1969")
        g.text("อายุ 27 ปี", 470, 650, 60, "kanit", RED, sc=pop(t, L[1] + 0.5) * (1 - seg(t, L[2], L[2] + 0.3)))
    if t > L[3]:
        confetti(g, t, 40, t0=L[3])


# ------------------------------------------------------------------ 5. quirks (สนุก)
def s_quirks(g, t, L, d):
    if t < L[1]:   # น้ำมัน -> ถนน โรงเรียน โรงพยาบาล
        for i, x in enumerate((240, 840)):
            with g.at(x, GROUND, 1, sy=pop(t, 0.1 + i * 0.2), sx=1):
                g.poly([(-80, 0), (80, 0), (18, -330), (-18, -330)], None, 8)
                for j in range(4):
                    g.line([(-80 + 15 * j, -80 * j), (80 - 15 * (j + 1), -80 * j - 80)], 5)
            if t > 0.6:
                for k in range(8):
                    p = (t * 1.2 + k / 8) % 1
                    g.blob(x + 120 * p * math.cos(k * 2.4), GROUND - 360 - 160 * math.sin(p * math.pi), 12, 16, INK, 0, k)
        for i, (lbl, x) in enumerate((("ถนน", 210), ("โรงเรียน", CX), ("โรงพยาบาล", 870))):
            k = pop(t, L[0] + 1.6 + i * 0.5)
            if k > 0:
                with g.at(x, 520 + 40 * (i % 2), k):
                    g.rrect(-140, -70, 280, 140, 26, WHITE, 7)
                    g.text(lbl, 0, 0, 50, "kanit")
        g.text("น้ำมัน", CX, GROUND - 100, 60, "kanit", sc=pop(t, 0.4))
        g.ground(GROUND, WHITE)
        return
    # ผู้นำสุดแปลก: สปอตไลต์ -> กระโจมกลางเมือง -> องครักษ์หญิง -> สมุดปกเขียว
    if t < L[2] - 0.2:
        g.sunburst(CX, 800, 200, 650, 20, t * 20, 12, GOLD2)
    if t > L[2] - 0.2:   # ตึกเมืองนอก + กระโจม
        for i, (bx, bh) in enumerate([(80, 520), (220, 680), (900, 600), (1020, 460)]):
            g.rrect(bx - 70, GROUND - bh, 140, bh, 6, ICE, 6)
            for r in range(int(bh / 90)):
                g.rrect(bx - 40, GROUND - bh + 30 + r * 90, 30, 40, 4, WHITE, 3)
                g.rrect(bx + 10, GROUND - bh + 30 + r * 90, 30, 40, 4, WHITE, 3)
        tent(g, CX, GROUND - 10, 0.9 * pop(t, L[2] - 0.2))
        g.text("กลางเมืองต่างประเทศ", CX, 430, 54, "kanit", sc=pop(t, L[2]) * (1 - seg(t, L[3] - 0.3, L[3])))
    g.ground(GROUND, WHITE)
    gx = CX if t < L[2] else CX + 10
    gaddafi(g, gx, GROUND + 90, 0.95 * pop(t, L[1] - 0.2), "happy", look="leader",
            arm=e_back(seg(t, L[4], L[4] + 0.4)))
    if t > L[3] - 0.2:
        for i, sx in enumerate((-1, 1)):
            k = e_out(seg(t, L[3] - 0.2 + i * 0.2, L[3] + 0.4 + i * 0.2))
            guard(g, CX + sx * lerp(700, 250, k), GROUND + 120, 1.15)
    if t > L[4] - 0.2:
        k = spring(t - L[4] + 0.2, 2.2, 5)
        green_book(g, CX + 150, lerp(GROUND, 600, k), 1.0, -8)
        if t > L[4] + 0.3:
            for i in range(10):
                a = math.radians(i * 36 + t * 40)
                g.line([(CX + 150 + math.cos(a) * 150, 600 + math.sin(a) * 160),
                        (CX + 150 + math.cos(a) * 200, 600 + math.sin(a) * 210)], 7, GOLD, amp=0)


# ------------------------------------------------------------------ 6. dark (น่ากลัว)
def s_dark(g, t, L, d):
    if t < L[2] - 0.2:
        # เงายักษ์ด้านหลังรอยยิ้ม
        k = e_out(seg(t, 0.3, 1.6))
        with g.silhouette(INK, 0.85 * k):
            gaddafi(g, CX, GROUND + 60, lerp(1.0, 2.2, k), look="leader", arm=0.3)
        gaddafi(g, CX, GROUND + 80, 0.8, "happy", look="leader")
        if t > L[1] - 0.2:   # คนคิดต่างหายไป
            for i, x in enumerate((150, 300, 780, 930)):
                gone = i == 2
                a = 1 - seg(t, L[1] + 0.8, L[1] + 1.6) if gone else 1
                with g.alpha(a * pop(t, L[1] - 0.2 + i * 0.1)):
                    g.person(x, GROUND + 160, 0.7, "worry", hat="none", seed=320 + i, mustache=False,
                             col=[GREY, NAVY, BROWN2, LGREY][i])
                if gone and t > L[1] + 1.2:
                    g.text("?", x, GROUND - 60, 150, "kanit", RED, sc=pop(t, L[1] + 1.2))
        g.ground(GROUND + 160, WHITE)
        return
    # ล็อกเกอร์บี -> คว่ำบาตร
    k = e_out(seg(t, L[2] - 0.2, L[2] + 0.5))
    with g.at(CX, 700, k, (1 - k) * 540 - 3):
        g.rrect(-330, -250, 660, 500, 10, (0.97, 0.95, 0.89, 1), 8)
        g.text("WORLD NEWS · 1988", 0, -210, 32, "kanitr")
        g.line([(-300, -180), (300, -180)], 5)
        g.text("เครื่องบินระเบิดเหนือล็อกเกอร์บี", 0, -120, 46, "kanit", maxw=600)
        jet(g, -140, 40, 0.8, rot=8)
        for i in range(6):
            g.line([(20, -20 + i * 32), (290 - (i % 3) * 40, -20 + i * 32)], 6, LGREY)
    if t > L[3] - 0.2:
        ks = pop(t, L[3])
        with g.at(CX, 1080, ks, -10):
            g.rrect(-250, -70, 500, 140, 20, None, 10, stroke=RED)
            g.text("คว่ำบาตร", 0, 0, 96, "kanit", RED)


# ------------------------------------------------------------------ 7. uprising (ระทึก)
def s_uprising(g, t, L, d):
    if t < L[1] - 0.2:   # คลื่นอาหรับสปริงซัดเข้าแผนที่
        libya_map(g, CX, 860, 760, SAND, 8, [("ตริโปลี", CITY["ตริโปลี"]), ("เบงกาซี", CITY["เบงกาซี"])])
        k = e_io(seg(t, 0.4, 2.8))
        wx = lerp(1400, -300, k)
        g.poly([(wx, 420), (wx + 140, 380), (wx + 260, 460), (wx + 220, 1200), (wx, 1200)], (0.56, 0.72, 0.87, 0.75), 7,
               smooth=True)
        g.text("อาหรับสปริง", CX, 330, 80, "kanit", BLUE, sc=pop(t, 0.3))
        year_badge(g, t, 0.2, 230, 1150, "2011")
        return
    if t < L[3] - 0.2:   # ฝูงชนเบงกาซี + คำประกาศ
        g.ground(GROUND, WHITE)
        for i in range(7):
            x = 90 + i * 150
            k = pop(t, L[1] - 0.2 + i * 0.08)
            bob = 12 * abs(math.sin(t * 7 + i))
            if k > 0:
                g.person(x, GROUND + 200 - bob, 0.75 * k, "shock" if t > L[2] else "happy", hat="none", seed=400 + i,
                         mustache=i % 2 == 0, col=[GREY, NAVY, BROWN2, LGREY][i % 4])
                if i % 2 == 0:
                    g.line([(x + 60, GROUND + 60 - bob), (x + 60, GROUND - 210 - bob)], 6, BROWN2)
                    g.flag(x + 60, GROUND - 210 - bob, 120, 75, "ly", t + i, 0.8)
        g.text("เบงกาซี", 230, 380, 64, "kanit", sc=pop(t, L[1]) * (1 - seg(t, L[2] - 0.4, L[2] - 0.2)))
        if t > L[2] - 0.2:
            k = pop(t, L[2] - 0.2)
            with g.at(800, 560, k):
                g.rrect(-130, 160, 260, 300, 18, BROWN2, 8)
                gaddafi(g, 0, 190, 1.0, "worry", look="leader", arm=0.8 + 0.2 * math.sin(t * 9))
            g.bubble(420, 380, 480, 150, WHITE, (1, 1))
            g.text("บ้านต่อบ้าน!", 420, 365, 70, "kanit", RED, sc=pop(t, L[2] + 0.3))
        return
    if t < L[4] - 0.2:   # สงครามกลางเมือง + นาโต้ (ไม่แสดงความรุนแรงโดยตรง)
        dunes(g, GROUND, 5)
        for i in range(3):
            smoke(g, 200 + i * 340, GROUND - 40, t, L[3] - 0.2 + i * 0.3, 5, 1.0)
        k = seg(t, L[3] + 1.0, L[3] + 3.0)
        for i in range(2):
            jet(g, lerp(1400, -400, k) + i * 220, 360 + i * 110, 0.75, rot=-4)
        g.text("สงครามกลางเมือง", CX, 700, 76, "kanit", RED, sc=pop(t, L[3]))
        g.text("นาโต้", CX, 820, 64, "kanit", NAVY, sc=pop(t, L[3] + 1.6))
        return
    if t < L[5] - 0.2:   # ตริโปลีแตก: ธงเขียวลง ธงสามสีขึ้น
        g.ground(GROUND, WHITE)
        g.rrect(CX - 9, 400, 18, GROUND - 400, 8, LGREY, 6)
        k = e_io(seg(t, L[4] + 0.3, L[4] + 1.6))
        g.flag(CX + 9, lerp(410, 900, k), 260, 165, "lyg", t, 1.0)
        if k > 0.5:
            g.flag(CX + 9, lerp(900, 410, e_io(seg(t, L[4] + 1.0, L[4] + 2.3))), 260, 165, "ly", t, 1.0)
        g.text("ตริโปลี · ส.ค. 2011", CX, 300, 64, "kanit", sc=pop(t, L[4]))
        confetti(g, t, 30, t0=L[4] + 2.0)
        return
    # หนีกลับสิรต์
    libya_map(g, CX, 860, 760, SAND, 8, [("ตริโปลี", CITY["ตริโปลี"]), ("สิรต์", CITY["สิรต์"])])
    k = e_io(seg(t, L[5] + 0.2, L[5] + 2.0))
    ax, ay = CX + (0.12 - 0.5) * 760, 860 + (0.06 - 0.5) * 760
    bx, by = CX + (0.45 - 0.5) * 760, 860 + (0.22 - 0.5) * 760
    pts = [(lerp(ax, bx, k * i / 20), lerp(ay, by, k * i / 20) - 120 * math.sin(math.pi * k * i / 20)) for i in range(21)]
    g.line(pts, 9, RED, amp=0)
    pickup(g, pts[-1][0], pts[-1][1] + 20, 0.5, t)


# ------------------------------------------------------------------ 8. capture (เศร้า)
def s_capture(g, t, L, d):
    dunes(g, 1000, 7)
    culvert(g, CX, 1210, 1.0)
    if t > L[1] - 0.2:   # เงานักรบเดินเข้ามา
        k = e_out(seg(t, L[1] - 0.2, L[1] + 1.2))
        with g.silhouette(INK, 0.8):
            for i in range(3):
                g.soldier(lerp(-200, 120 + i * 110, k), 1050, 0.95, GREY, 500 + i)
    if L[2] - 0.2 < t < L[3] - 0.3:
        k = pop(t, L[2] - 0.2)
        with g.at(CX + 120, 760, k):
            g.bubble(0, 0, 620, 170, WHITE, (-1, 1))
            g.text("\"ฉันทำอะไรให้พวกคุณ?\"", 0, -12, 58, "kanit")
    sad = seg(t, L[3] - 0.4, L[3] + 0.6)
    dim(g, 0.45 * sad, 1000)
    if t > L[3] - 0.2:   # ข่าวด่วนทางทีวี
        k = pop(t, L[3] - 0.2)
        with g.at(CX, 700, k):
            g.rrect(-300, -200, 600, 400, 30, WHITE, 9)
            g.rrect(-260, -160, 520, 300, 14, NAVY, 6)
            g.rrect(-260, 60, 520, 80, 0, RED, 0)
            g.text("ข่าวด่วน", 0, 100, 56, "kanit", WHITE)
            gaddafi(g, 0, 70, 0.5, "flat", look="leader")
            g.line([(-120, 200), (-160, 260)], 8)
            g.line([(120, 200), (160, 260)], 8)
    if t > L[4] - 0.2:   # ไทม์ไลน์ 1969 —— 2011 ดับลง
        k = pop(t, L[4] - 0.2)
        with g.at(CX, 1120, k):
            g.rrect(-420, -40, 840, 80, 40, WHITE, 7)
            fill = 1 - e_in(seg(t, L[4] + 0.4, L[4] + 1.8))
            g.rrect(-410, -30, 820 * fill, 60, 30, LYGREEN, 0)
            g.text("1969", -330, -90, 50, "kanit", WHITE)
            g.text("2011", 330, -90, 50, "kanit", WHITE)


# ------------------------------------------------------------------ 9. aftermath
def s_aftermath(g, t, L, d):
    split = e_out(seg(t, L[1] - 0.1, L[1] + 0.9))
    pieces = [(-1, -1, -8), (1, -1, 6), (0, 1, -3)]
    for i, (dx, dy, rot) in enumerate(pieces):
        with g.at(CX + dx * 120 * split, 850 + dy * 90 * split, 1, rot * split):
            g.c.save()
            if i == 0:
                g.c.rectangle(-1000, -1000, 1000, 1000)
            elif i == 1:
                g.c.rectangle(0, -1000, 1000, 1000)
            else:
                g.c.rectangle(-1000, 0, 2000, 1000)
            g.c.clip()
            libya_map(g, 0, 0, 820, [SAND, SAND2, (0.93, 0.86, 0.75, 1)][i], 8)
            g.c.restore()
    if split > 0.3:
        for i, (x, y) in enumerate([(260, 560), (840, 560), (CX, 1110)]):
            g.text("!", x, y, 120, "kanit", RED, sc=pop(t, L[1] + 0.5 + i * 0.2))
    g.text("ลิเบียวันนี้", CX, 270, 72, "kanit", sc=pop(t, 0.2))


# ------------------------------------------------------------------ 10. lesson
def s_lesson(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[3] - 0.2:
        # หอคอยแห่งความกลัว: ค่อย ๆ สูง แล้วพังในพริบตา
        grow = seg(t, L[1] - 0.2, L[2] - 0.2)
        fall = e_in(seg(t, L[2] + 0.6, L[2] + 1.6))
        n = 7
        for i in range(n):
            if grow * n < i:
                break
            bx = CX + fall * (i - 3) * 90 * (1 + i * 0.2)
            by = GROUND - 40 - i * 95 + fall * (i * 95 - 10) + fall * fall * 60
            with g.at(bx, by, 1, fall * (i * 25 - 60)):
                g.rrect(-130 + i * 8, -45, 260 - i * 16, 90, 10, [LGREY, GREY][i % 2], 7)
                if i == 3:
                    g.text("ความกลัว", 0, 0, 48, "kanit", WHITE)
        if grow > 0.95 and fall < 0.05:
            gaddafi(g, CX, GROUND - 40 - n * 95 + 60, 0.45, "happy", look="leader")
        if t < L[1]:
            k = pop(t, 0.1)
            with g.at(CX, 650, k):
                g.circle(0, 0, 120, GOLD2, 9)
                g.rrect(-50, 110, 100, 70, 14, LGREY, 7)
                for i in range(8):
                    a = math.radians(i * 45)
                    g.line([(math.cos(a) * 150, math.sin(a) * 150), (math.cos(a) * 190, math.sin(a) * 190)], 8, GOLD, amp=0)
        return
    # โค่น = วันเดียว  vs  สร้าง = หลายปี
    for i, (x, lbl, sub) in enumerate(((290, "โค่นล้ม", "1 วัน"), (790, "สร้างใหม่", "หลายปี"))):
        k = pop(t, L[3] - 0.1 + i * 0.6)
        if k <= 0:
            continue
        with g.at(x, 880, k):
            g.rrect(-220, -300, 440, 560, 30, WHITE, 8)
            g.text(lbl, 0, -240, 60, "kanit")
            g.text(sub, 0, 200, 64, "kanit", RED)
            if i == 0:
                hk = math.sin(t * 9) * 25
                with g.at(0, -40, 1, hk):
                    g.rrect(-14, -20, 28, 200, 8, BROWN2, 6)
                    g.rrect(-80, -60, 160, 70, 12, GREY, 7)
            else:
                prog = 0.15 + 0.1 * math.sin(t)
                g.rrect(-120, 120 - 240 * prog, 240, 240 * prog, 6, SAND2, 6)
                g.line([(140, 130), (140, -150), (-60, -150)], 8, GOLD)
                g.line([(-40, -150), (-40, -40)], 4)


# ------------------------------------------------------------------ 11. outro
def s_outro(g, t, L, d):
    k = pop(t, 0.1)
    with g.at(CX, 800, k, -3 + 3 * math.sin(t * 3)):
        g.bubble(0, 0, 640, 360, WHITE, (-1, 1))
        for i in range(3):
            g.circle(-140 + i * 140, -10 + 12 * math.sin(t * 6 + i), 34, [RED, GOLD, LYGREEN][i], 6)
    gaddafi(g, 250, GROUND + 120, 0.9 * pop(t, 0.4), "think", look="leader")


SCENES = {
    "cold_open": s_cold_open, "title": s_title, "origins": s_origins, "coup": s_coup, "quirks": s_quirks,
    "dark": s_dark, "uprising": s_uprising, "capture": s_capture, "aftermath": s_aftermath,
    "lesson": s_lesson, "outro": s_outro,
}
NO_IRIS = set()
