"""ฉากตอน: มาเรีย เทเรซา (20 ต.ค. 1740) — ฟังก์ชันรับ (g, t, L, d)"""
import math
import os
import sys

import cairo

sys.path.insert(0, os.path.dirname(__file__))
from chars import (PRUSSIAN, candle, charles, crown, frederick, maria, noble, scroll,  # noqa: E402
                   wolf)
from fx import confetti  # noqa: E402
from gfx import (BLUE, BROWN2, GOLD, GOLD2, GREY, ICE, INK, LGREY, RED, W, WHITE, e_back, e_in,  # noqa: E402
                 e_io, e_out, hexc, hn, lerp, pop, seg)

CX = W / 2
GROUND = 1180
AUSTRIA = hexc("#f1d9a6")
FRANCE = [BLUE, WHITE, RED]
SPAIN = [RED, GOLD, RED]
BAVARIA = [hexc("#5a8fd0"), WHITE, hexc("#5a8fd0")]
PRUSSIA_FLAG = [INK, WHITE, INK]


def dim(g, a, y1=GROUND):
    if a > 0:
        grad = cairo.LinearGradient(0, -500, 0, y1 + 60)
        grad.add_color_stop_rgba(0, 0.12, 0.12, 0.16, a)
        grad.add_color_stop_rgba(0.75, 0.12, 0.12, 0.16, a * 0.8)
        grad.add_color_stop_rgba(1, 0.12, 0.12, 0.16, 0)
        g.c.rectangle(-500, -500, W + 1000, y1 + 560)
        g.c.set_source(grad)
        g.c.fill()


def cloud(g, x, y, s=1.0, col=GREY):
    with g.at(x, y, s):
        for dx, dy, r in ((-70, 10, 55), (0, -20, 70), (75, 8, 55), (0, 25, 60)):
            g.circle(dx, dy, r, col, 6)


def bolt(g, x, y, s=1.0, a=1.0):
    with g.alpha(a):
        with g.at(x, y, s):
            g.poly([(0, 0), (40, 0), (10, 70), (50, 70), (-20, 190), (5, 95), (-30, 95)], GOLD2, 6)


def europe(g, x, y, s=1.0, t=0.0, silesia_out=0.0, fire=0.0):
    """แผนที่สัญลักษณ์: อาณาจักรฮับส์บูร์กตรงกลาง + เพื่อนบ้าน"""
    with g.at(x, y, s):
        for name, (bx, by, rx, ry), col in (("ปรัสเซีย", (-40, -330, 230, 110), hexc("#c9d4e6")),
                                             ("ฝรั่งเศส", (-370, -40, 150, 190), hexc("#d8e0f0")),
                                             ("บาวาเรีย", (-170, 40, 95, 90), hexc("#dbe8f5")),
                                             ("สเปน", (-400, 260, 120, 90), hexc("#f3dccb"))):
            g.blob(bx, by, rx, ry, col, 6, int(bx) % 13)
            g.text(name, bx, by, 40, "kanit", GREY)
        g.blob(110, 60, 240, 170, AUSTRIA, 8, 5)
        g.text("ออสเตรีย", 110, 70, 56, "kanit")
        # ไซลีเชีย: ชิ้นด้านบนของออสเตรีย ถูกดึงไปทางปรัสเซีย
        k = e_io(silesia_out)
        with g.at(lerp(130, 40, k), lerp(-120, -250, k), 1, -12 * k):
            g.blob(0, 0, 95, 50, hexc("#e9c47c"), 6, 9)
            g.text("ไซลีเชีย", 0, 0, 36, "kanit")
        if fire > 0:
            for i in range(9):
                fx_, fy_ = 110 + 180 * hn(i, 1), 60 + 120 * hn(i, 2)
                h = (50 + 30 * math.sin(t * 9 + i)) * fire
                with g.at(fx_, fy_):
                    g.c.move_to(0, -h)
                    g.c.curve_to(h * 0.5, -h * 0.3, h * 0.4, h * 0.3, 0, h * 0.35)
                    g.c.curve_to(-h * 0.4, h * 0.3, -h * 0.5, -h * 0.3, 0, -h)
                    g.fs((0.95, 0.55, 0.2, 0.9), 4)


# ------------------------------------------------------------------ 1. hook
def s_hook(g, t, L, d):
    # L0 ไตเติล
    if t < L[1] + 0.2:
        a = 1 - seg(t, L[1] - 0.3, L[1] + 0.2)
        with g.alpha(a):
            g.sunburst(CX, 760, 220, 620, 24, t * 10, 14, LGREY)
            g.text("วันนี้ในอดีต", CX, 650, 104, "kanit", sc=lerp(2.0, 1, e_out(seg(t, 0.1, 0.4))) if t > 0.1 else 0,
                   rot=-5)
            g.text("20 ตุลาคม 1740", CX, 790, 84, "kanit", RED, sc=pop(t, 0.8))
            crown(g, CX, 1000, 1.4 * pop(t, 1.4))
    # L1 จักรพรรดิสวรรคต
    if L[1] - 0.2 < t < L[2]:
        lit = 1 - seg(t, L[1] + 2.2, L[1] + 2.6)
        g.ground(GROUND, WHITE)
        charles(g, 430, GROUND + 80, 1.15 * pop(t, L[1] - 0.2), "happy" if lit > 0.5 else "sleep")
        candle(g, 820, GROUND + 20, 1.1, t, lit)
        g.name_tag(t, L[1] + 0.3, 520, 560, "จักรพรรดิชาร์ลส์ที่ 6", "จักรพรรดิแห่งราชวงศ์ฮับส์บูร์ก", dur=2.4)
        dim(g, 0.35 * (1 - lit))
    # L2-L3 พายุแห่งการหักหลังเหนือยุโรป
    if L[2] - 0.2 < t < L[4] - 0.2:
        europe(g, CX, 930, 1.0, t, fire=0.0)
        dim(g, 0.35 * seg(t, L[2] - 0.2, L[2] + 0.4))
        for i in range(4):
            cloud(g, 140 + i * 270 + 20 * math.sin(t + i), 420 + 30 * (i % 2), 0.9, GREY)
        for i, tb in enumerate((L[2] + 0.6, L[3] + 0.3, L[3] + 2.0)):
            if tb < t < tb + 0.5:
                bolt(g, 260 + i * 260, 470, 1.1, 1 - seg(t, tb + 0.2, tb + 0.5))
        if t > L[3]:   # รอยร้าว
            k = seg(t, L[3], L[3] + 1.5)
            pts = [(CX - 300 + 600 * i / 10, 930 + 60 * math.sin(i * 1.7) * (1 if i % 2 else -1)) for i in range(int(1 + 10 * k))]
            if len(pts) > 1:
                g.line(pts, 9, INK, amp=0)
    # L4-L5 มงกุฎลอยลงสู่... ผู้หญิง!
    if t > L[4] - 0.2:
        g.ground(GROUND, WHITE)
        down = e_io(seg(t, L[4], L[5] - 0.1))
        if t < L[5] - 0.1:
            crown(g, CX, lerp(400, 820, down), 2.4, 10 * math.sin(t * 3))
            g.text("?", CX + 260, 640, 160, "kanit", RED, sc=pop(t, L[4] + 0.6), rot=12)
        else:
            maria(g, CX, GROUND + 80, 1.2 * pop(t, L[5] - 0.1), "shock", crown_on=e_back(seg(t, L[5], L[5] + 0.4)))
            g.text("!", CX + 230, 560, 200, "kanit", RED, sc=pop(t, L[5] + 0.2))


# ------------------------------------------------------------------ 2. deal
def s_deal(g, t, L, d):
    g.ground(GROUND, WHITE)
    alive = t < L[3] + 0.4
    charles(g, 300, GROUND + 80, 1.0, "happy" if alive else "sleep", arm=0.6 * e_out(seg(t, 0.4, 1.0)) if alive else 0)
    candle(g, 120, GROUND + 10, 0.8, t, 1 - seg(t, L[3] + 0.2, L[3] + 0.6))
    if t < L[1]:   # ถุงเงิน + ดินแดน
        for i, lbl in enumerate(("เงิน", "ดินแดน")):
            k = pop(t, 0.6 + i * 0.5)
            with g.at(560 + i * 230, 760, k):
                g.blob(0, 0, 90, 80, GOLD2 if i == 0 else hexc("#e9c47c"), 7, i)
                g.text(lbl, 0, 0, 50, "kanit")
    if t > L[1] - 0.2:   # สัญญาจากกษัตริย์ทั่วยุโรป
        torn = e_in(seg(t, L[4], L[4] + 1.0))
        for i in range(5):
            k = pop(t, L[1] - 0.2 + i * 0.25)
            sx = 560 + (i % 3) * 170
            sy = 560 + (i // 3) * 260
            scroll(g, sx, sy + 200 * torn, 0.95 * k, -8 + i * 5, [RED, BLUE, GOLD, PRUSSIAN, RED][i], torn)
        if t < L[4]:
            g.text("สัญญารับรองสิทธิ", 730, 380, 54, "kanit", sc=pop(t, L[1] + 0.4))
        else:
            g.text("เศษกระดาษ!", 730, 380, 80, "kanit", RED, sc=pop(t, L[4] + 0.3), rot=-6)
    if t > L[2] - 0.2 and t < L[4]:
        maria(g, 520, GROUND + 80, 0.75 * pop(t, L[2] - 0.2), "happy")
    dim(g, 0.3 * seg(t, L[3], L[3] + 0.6))


# ------------------------------------------------------------------ 3. crisis
def s_crisis(g, t, L, d):
    g.ground(GROUND, WHITE)
    dim(g, 0.22 * seg(t, L[2] - 0.3, L[2] + 0.5))
    # ภาพพ่อติดริบบิ้นไว้ทุกข์
    if t > L[1] - 0.3:
        k = pop(t, L[1] - 0.3)
        with g.at(830, 520, k):
            g.rrect(-110, -140, 220, 280, 16, GOLD2, 8)
            g.c.save()
            g.c.rectangle(-95, -125, 190, 250)
            g.c.clip()
            charles(g, 0, 235, 0.8, "sleep")
            g.c.restore()
            g.poly([(40, -140), (110, -140), (110, -70)], INK, 0)
    mood = "worry" if t < L[3] else "sad"
    maria(g, CX if t < L[3] - 0.3 else 380, GROUND + 80, 1.1, mood)
    g.name_tag(t, 0.4, CX - 170, 520, "มาเรีย เทเรซา", "พระธิดาองค์โตของจักรพรรดิ", dur=2.6)
    if t > L[1]:
        g.text("23 ปี", 250, 760, 70, "kanit", RED, sc=pop(t, L[1]) * (1 - seg(t, L[3] - 0.5, L[3] - 0.2)))
    if t > L[3] - 0.3:   # คลังหลวงว่าง + กองทัพเสื่อม
        k = pop(t, L[3] - 0.3)
        with g.at(800, GROUND, k):
            g.rrect(-130, -150, 260, 150, 14, BROWN2, 8)
            g.c.save()
            g.c.translate(0, -150)
            g.c.rotate(-0.6)
            g.rrect(-130, -40, 260, 40, 12, BROWN2, 7)
            g.c.restore()
            g.text("คลังหลวง", 0, -75, 44, "kanit")
            g.text("0", 0, -230, 90, "kanit", RED)
        g.soldier(620, GROUND + 150, 0.8 * k, GREY, 801, rifle=False)
        g.line([(660, GROUND + 70), (720, GROUND + 140)], 7, LGREY)
    if t > L[4] - 0.2:   # ขุนนางมองดูแคลน
        for i, x in enumerate((140, 960)):
            k = e_out(seg(t, L[4] - 0.2 + i * 0.2, L[4] + 0.4 + i * 0.2))
            g.person(lerp(-200 if i == 0 else 1300, x, k), GROUND + 160, 0.8, "smug", "bowler", 811 + i, True,
                     [LGREY, GREY][i])
            g.bubble(lerp(-200 if i == 0 else 1300, x, k), GROUND - 330, 170, 100, WHITE, (1 - 2 * i, 1))
            g.text("หึ...", lerp(-200 if i == 0 else 1300, x, k), GROUND - 340, 44, "kanit", sc=k)


# ------------------------------------------------------------------ 4. wolves
def s_wolves(g, t, L, d):
    if t < L[2] - 0.2:   # ดวงตาหมาป่าในความมืด -> ฟรีดริชฉีกสัญญา
        dim(g, 0.55)
        g.ground(GROUND, WHITE)
        for i in range(6):
            x, y = 140 + i * 165, 520 + 120 * math.sin(i * 2.1)
            if t > 0.2 + i * 0.15:
                blink = (t * 0.8 + i) % 3 < 0.1
                for sx in (-1, 1):
                    g.circle(x + sx * 18, y, 9 if not blink else 2, GOLD2, 0)
        if t > L[1] - 0.2:
            k = e_out(seg(t, L[1] - 0.2, L[1] + 0.5))
            frederick(g, lerp(1300, 700, k), GROUND + 80, 1.1, "smug", arm=0.6)
            scroll(g, lerp(1300, 700, k) - 160, 820, 1.0, -10, PRUSSIAN, e_in(seg(t, L[1] + 0.8, L[1] + 1.6)))
            g.name_tag(t, L[1] + 0.2, 420, 560, "พระเจ้าฟรีดริชที่ 2", "กษัตริย์แห่งปรัสเซีย", dur=2.4, side=-1)
        return
    out = seg(t, L[2] + 0.3, L[2] + 1.8)
    fire = seg(t, L[5] + 0.5, L[6] + 0.5)
    europe(g, CX + 40, 860, 1.0, t, silesia_out=out, fire=fire)
    if L[2] < t < L[3]:
        g.line([(CX + 40, 860 - 120), (CX - 30, 860 - 260)], 8, RED, amp=0)
        g.text("บุกยึด!", CX + 230, 520, 80, "kanit", RED, sc=pop(t, L[2] + 0.3), rot=-6)
    if t > L[3] - 0.2:   # หมาป่ารุมทึ้ง
        for i, (fl, x, y) in enumerate(((FRANCE, 170, 1080), (SPAIN, 900, 1120), (BAVARIA, 420, 1210))):
            k = e_out(seg(t, L[3] - 0.2 + i * 0.3, L[3] + 0.6 + i * 0.3))
            wolf(g, lerp(-300 if x < CX else 1400, x, k), y, 1.0, t, fl, "laugh" if t > L[4] else "smug", seed=331 + i)
        if t > L[4] - 0.2 and t < L[5]:
            maria(g, CX + 120, 980, 0.5 * pop(t, L[4] - 0.2), "sad")
            for i in range(2):
                g.sweat(CX + 120 - 10 + i * 20, 850 + ((t * 80 + i * 30) % 40), 1.0)
    if t > L[5] - 0.2:
        k = pop(t, L[5] - 0.2)
        with g.at(CX, 400, k, -3):
            g.poly([(-470, -80), (470, -80), (440, 0), (470, 80), (-470, 80), (-440, 0)], RED, 9)
            g.text("สงครามสืบราชบัลลังก์ออสเตรีย", 0, 0, 56, "kanit", WHITE)
        g.text("1740–1748", CX, 520, 56, "kanit", sc=pop(t, L[5] + 0.6))


# ------------------------------------------------------------------ 5. gamble
def hall(g):
    for i in range(4):
        x = 110 + i * 287
        g.rrect(x - 30, 330, 60, GROUND - 330, 10, ICE, 6)
    g.c.move_to(80, 330)
    for i in range(3):
        x0 = 140 + i * 287
        g.c.curve_to(x0 + 40, 220, x0 + 190, 220, x0 + 227, 330)
    g.fs(None, 8)
    g.line([(60, 330), (1020, 330)], 8)


def s_gamble(g, t, L, d):
    if t < L[2] - 0.2:   # ที่ปรึกษาบอกให้ยอมแพ้
        g.ground(GROUND, WHITE)
        maria(g, CX, GROUND + 80, 1.1, "worry" if t < L[1] else "happy")
        for i, x in enumerate((150, 930)):
            k = e_out(seg(t, 0.2 + i * 0.2, 0.8 + i * 0.2))
            g.person(lerp(-200 if i == 0 else 1300, x, k), GROUND + 160, 0.8, "worry", "bowler", 820 + i, True, GREY)
            if t < L[1]:
                g.bubble(lerp(-200 if i == 0 else 1300, x, k), GROUND - 330, 230, 110, WHITE, (1 - 2 * i, 1))
                g.text("ยอมแพ้เถอะ!", lerp(-200 if i == 0 else 1300, x, k), GROUND - 340, 40, "kanit", sc=k)
        if t > L[1]:
            g.text("เดิมพันครั้งสุดท้าย", CX, 420, 76, "kanit", RED, sc=pop(t, L[1] + 0.3), rot=-4)
            for i in range(6):
                a = math.radians(i * 60 + t * 50)
                g.sparkle(CX + math.cos(a) * 220, 760 + math.sin(a) * 160, 22)
        return
    # ห้องประชุมสภาขุนนางฮังการี
    hall(g)
    g.ground(GROUND, WHITE)
    for i, x in enumerate((110, 250, 830, 970)):
        noble(g, x, GROUND + 170, 0.85 * pop(t, L[3] + i * 0.15), "flat" if t < L[6] else "sad", 0.0, t, seed=841 + i)
    baby = pop(t, L[3] - 0.2)
    maria(g, CX, GROUND + 90, 1.2 * pop(t, L[2] - 0.2), "sad" if t > L[4] else "flat", dress="black", baby=baby)
    if L[4] < t < L[6]:   # น้ำตาคลอ
        for sx in (-1, 1):
            g.sweat(CX + sx * 26, 840 + ((t * 40) % 30), 0.8)
    if t > L[5] - 0.2:
        k = pop(t, L[5] - 0.2)
        with g.at(CX, 420, k):
            g.bubble(0, 0, 780, 200, WHITE, (-1, 1))
            g.text("คนทั้งโลกทอดทิ้งฉันแล้ว..." if t < L[6] else "อัศวินฮังการี ช่วยปกป้องแผ่นดินนี้!",
                   0, -8, 50, "kanit")
    g.text("สภาขุนนางฮังการี", CX, 280, 50, "kanit", sc=pop(t, L[3]) * (1 - seg(t, L[5] - 0.4, L[5] - 0.2)))


# ------------------------------------------------------------------ 6. oath
def s_oath(g, t, L, d):
    hall(g)
    g.ground(GROUND, WHITE)
    up = e_back(seg(t, L[1] - 0.1, L[1] + 0.6))
    xs = (90, 230, 370, 710, 850, 990)
    for i, x in enumerate(xs):
        noble(g, x, GROUND + 170, 0.85, "laugh" if t > L[1] else "shock", up, t, seed=851 + i)
    maria(g, CX, GROUND + 90, 1.15, "happy" if t > L[1] else "sad", dress="black", baby=1.0)
    if t > L[1] + 0.3:
        for i in range(12):
            a = math.radians(i * 30 + t * 40)
            g.sparkle(CX + math.cos(a) * 330, 700 + math.sin(a) * 260, 18)
    if t > L[3] - 0.2:
        k = pop(t, L[3] - 0.2)
        with g.at(CX, 400, k * (1 + 0.04 * math.sin(t * 8)), -3):
            g.rrect(-430, -80, 860, 160, 40, GOLD2, 9)
            g.text("Vitam et sanguinem!", 0, -6, 70, "kanit")
        g.text("\"ชีวิตและเลือดของเรา!\"", CX, 520, 48, "kanit", RED, sc=pop(t, L[3] + 0.4))


# ------------------------------------------------------------------ 7. rise
def lamb(g, x, y, s):
    with g.at(x, y, s):
        for k in (-25, 25):
            g.line([(k, -10), (k, 20)], 8)
        for i in range(7):
            a = math.radians(i * 52)
            g.circle(math.cos(a) * 40, -40 + math.sin(a) * 25, 24, WHITE, 5)
        g.blob(50, -60, 22, 20, LGREY, 5, 2)
        g.circle(56, -64, 3, INK, 0)


def s_rise(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:   # ลูกแกะในดงหมาป่า
        lamb(g, CX, GROUND + 40, 1.4 * pop(t, 0.2))
        for i, (fl, x) in enumerate(((FRANCE, 170), (PRUSSIA_FLAG, 900))):
            wolf(g, x, GROUND + 40, 0.9, t, fl, "smug", seed=361 + i)
        return
    if t < L[3] - 0.2:   # ปฏิรูปกองทัพ บัญชาการรบ
        for i in range(5):
            g.soldier(560 + i * 110, GROUND + 160, 0.85 * pop(t, L[1] + 0.2 + i * 0.1), WHITE, 871 + i,
                      salute=1.0 if t > L[1] + 1.2 else 0.0)
        maria(g, 300, GROUND + 90, 1.05, "happy", arm=e_back(seg(t, L[1], L[1] + 0.5)))
        if t > L[2] - 0.2:   # ปฏิทิน 1740 -> 1748
            k = seg(t, L[2] - 0.2, L[2] + 1.6)
            yr = 1740 + int(8 * e_io(k))
            with g.at(CX, 470, pop(t, L[2] - 0.2)):
                g.rrect(-190, -110, 380, 220, 26, WHITE, 8)
                g.rrect(-190, -110, 380, 60, 26, RED, 8)
                g.text(str(yr), 0, 30, 110, "kanit")
            g.text("8 ปีเต็ม!", CX + 300, 330, 64, "kanit", RED, sc=pop(t, L[2] + 1.6), rot=8)
        return
    # บนบัลลังก์ + มงกุฎ
    g.sunburst(CX, 760, 220, 650, 24, t * 15, 14, GOLD2)
    g.rrect(CX - 170, GROUND - 420, 340, 420, 60, RED, 9)
    g.rrect(CX - 210, GROUND - 120, 420, 120, 20, GOLD, 8)
    maria(g, CX, GROUND + 60, 1.2, "smug" if t > L[4] else "happy", crown_on=e_back(seg(t, L[3], L[3] + 0.5)))
    if t > L[4]:
        confetti(g, t, 40, t0=L[4])
        g.text("จักรพรรดินี", CX, 330, 80, "kanit", sc=pop(t, L[4] + 0.2))


# ------------------------------------------------------------------ 8. lesson
def heart(g, x, y, s, col=RED):
    with g.at(x, y, s):
        g.c.move_to(0, 60)
        g.c.curve_to(-140, -30, -70, -130, 0, -60)
        g.c.curve_to(70, -130, 140, -30, 0, 60)
        g.fs(col, 8)


def s_lesson(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # โลกหันหลังให้
        for i, x in enumerate((140, 330, 750, 940)):
            with g.silhouette(GREY, 0.9):
                g.person(x, GROUND + 160, 0.8 * pop(t, L[1] - 0.2 + i * 0.12), "flat", "bowler", 891 + i, False, GREY)
        scroll(g, CX, 640, 1.0, 0, RED, e_in(seg(t, L[1] + 1.2, L[1] + 2.2)))
        maria(g, CX, GROUND + 80, 0.8, "sad")
        return
    beat = 1 + 0.08 * abs(math.sin(t * 4))
    for i in range(10):
        a = math.radians(i * 36 + t * 30)
        g.line([(CX + math.cos(a) * 200, 640 + math.sin(a) * 200), (CX + math.cos(a) * 260, 640 + math.sin(a) * 260)],
               8, GOLD, amp=0)
    heart(g, CX, 660, 1.4 * pop(t, L[2] - 0.2) * beat)
    g.text("ไม่ยอมแพ้", CX, 640, 40, "kanit", WHITE, sc=pop(t, L[3]) * beat)


# ------------------------------------------------------------------ 9. outro
def s_outro(g, t, L, d):
    g.ground(GROUND, WHITE)
    for i, (lbl, x, col, rot) in enumerate((("ยอมถอย", 230, LGREY, -6), ("สู้ตาย", 850, GOLD2, 6))):
        k = pop(t, L[3] - 0.2 + (0 if i == 0 else 2.2))
        if k > 0:
            with g.at(x, GROUND + 20, k):
                g.rrect(-12, -380, 24, 380, 6, BROWN2, 6)
                with g.at(0, -340, 1, rot):
                    g.poly([(-150, -55), (120, -55), (165, 0), (120, 55), (-150, 55)] if i else
                           [(150, -55), (-120, -55), (-165, 0), (-120, 55), (150, 55)], col, 8)
                    g.text(lbl, 0, 0, 58, "kanit")
    maria(g, CX, GROUND + 80, 1.0, "think" if t < L[5] else "happy", dress="black" if t < L[3] else "blue")
    if t < L[3] - 0.2:
        for i in range(3):
            g.text("?", CX - 140 + i * 140, 520 + 20 * math.sin(t * 4 + i), 110, "kanit", RED, sc=pop(t, 0.3 + i * 0.2))
    if t > L[5] - 0.2:
        k = pop(t, L[5] - 0.2)
        with g.at(CX, 420, k, -3 + 3 * math.sin(t * 3)):
            g.bubble(0, 0, 560, 260, WHITE, (-1, 1))
            for i in range(3):
                g.circle(-130 + i * 130, -10 + 12 * math.sin(t * 6 + i), 30, [RED, GOLD, BLUE][i], 6)


SCENES = {
    "hook": s_hook, "deal": s_deal, "crisis": s_crisis, "wolves": s_wolves, "gamble": s_gamble,
    "oath": s_oath, "rise": s_rise, "lesson": s_lesson, "outro": s_outro,
}
NO_IRIS = set()
