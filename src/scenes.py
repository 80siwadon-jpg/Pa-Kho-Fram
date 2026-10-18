"""ฉากทั้งหมด  แต่ละฟังก์ชันรับ (g, t, L, d)
g = Draw, t = เวลาภายในฉาก, L = เวลาเริ่มของแต่ละบรรทัดพากย์ (ภายในฉาก), d = ความยาวฉาก
"""
import math

from gfx import (ALASKA, BLUE, BROWN, BROWN2, COAT, TUNIC, GOLD, GOLD2, GREY, H, INK, LGREY, MINT, NAVY, PAPER, RED, SKIN,
                 THAILAND, WHITE, W, e_back, e_in, e_io, e_out, hn, lerp, poly_area, pop, seg, spring)

CX = W / 2
GROUND = 1180


def confetti(g, t, n=60, seed=3, t0=0.0):
    cols = [RED, BLUE, GOLD, MINT, GREY]
    for i in range(n):
        tt = t - t0 - 0.3 * (hn(i, seed + 9) * 0.5 + 0.5)
        if tt < 0:
            continue
        x = (hn(i, seed) * 0.5 + 0.5) * W + 40 * math.sin(tt * 3 + i)
        y = 250 + tt * (300 + 200 * (hn(i, seed + 1) * 0.5 + 0.5)) - 100
        if y > H:
            continue
        with g.at(x, y, 1, tt * 300 * hn(i, seed + 2)):
            g.rrect(-12, -7, 24, 14, 3, cols[i % len(cols)], 3)


def burst(g, x, y, t, t0, n=10, r=200, size=30, kind="spark", seed=5):
    tt = t - t0
    if tt < 0 or tt > 1.2:
        return
    k = e_out(seg(tt, 0, 0.7))
    a = 1 - seg(tt, 0.6, 1.2)
    with g.alpha(a):
        for i in range(n):
            ang = 2 * math.pi * i / n + hn(i, seed) * 0.3
            rr = r * k * (0.7 + 0.3 * hn(i, seed + 1))
            px, py = x + math.cos(ang) * rr, y + math.sin(ang) * rr + 120 * tt * tt
            if kind == "spark":
                g.sparkle(px, py, size * (1 - 0.5 * k))
            elif kind == "coin":
                g.coin(px, py, size, "$", tt * 400 + i * 30)
            elif kind == "oil":
                g.blob(px, py, size, size * 1.2, INK, 0, i)


def haha(g, t, items, t0):
    for i, (x, y, rot) in enumerate(items):
        s = pop(t, t0 + i * 0.18, 0.3)
        if s > 0:
            g.text("ฮ่า!", x, y + 8 * math.sin(t * 14 + i), 64, "kanit", sc=s, rot=rot)


# ------------------------------------------------------------------ 1. hook
def s_hook(g, t, L, d):
    zoom = lerp(1.0, 1.06, t / d) + 0.04 * e_out(seg(t, L[3], L[3] + 0.4))
    wake = L[2] + 0.9
    with g.at(CX, 860, zoom):
        with g.at(-CX, -860):
            # หน้าต่าง: กลางคืน -> กลางวัน
            day = seg(t, L[2] + 0.2, L[2] + 0.9)
            g.rrect(620, 330, 300, 300, 18, WHITE, 8)
            if day < 1:
                with g.alpha(1 - day):
                    g.circle(770, 470, 55, LGREY, 6)
                    g.circle(795, 450, 50, WHITE, 0)
                    for i, (sx, sy) in enumerate([(680, 380), (870, 400), (700, 570), (860, 590)]):
                        g.star(sx, sy, 14 + 4 * math.sin(t * 4 + i), GOLD2, 4)
            if day > 0:
                with g.alpha(day):
                    g.sunburst(770, 480, 70, 120 + 10 * math.sin(t * 5), 12, t * 30, 8, GOLD)
                    g.circle(770, 480, 60, GOLD2, 7)
            g.line([(770, 330), (770, 630)], 7)
            g.line([(620, 480), (920, 480)], 7)
            # ปฏิทินบนผนัง
            cal_s = 0.95 + 0.15 * (pop(t, L[1] + 1.0, 0.35) if t < L[2] else 1) * (1 if t < L[2] else 0)
            ft = seg(t, L[2] - 0.05, L[2] + 0.85)
            day_num = 6 + int(12 * e_io(ft))
            flip = None
            if 0 < ft < 1:
                frac = (12 * e_io(ft)) % 1
                flip = (frac, day_num)
            shake = 6 * math.sin(t * 40) if L[3] < t < L[3] + 1.2 else 0
            g.calendar(270 + shake, 520, cal_s * 0.92, day_num, flip=flip)
            # เตียง
            g.rrect(150, 1000, 780, 180, 30, BROWN2, 8)
            g.rrect(130, 880, 60, 330, 20, BROWN2, 8)
            g.rrect(890, 940, 60, 270, 20, BROWN2, 8)
            g.blob(320, 940, 120, 55, WHITE, 8, 3)
            # เด็ก
            jump = spring(t - wake, 2.4, 4.5) if t > wake else 0
            hy = 900 - 170 * jump
            mood = "sleep" if t < wake else "shock"
            breath = 1 + 0.02 * math.sin(t * 2.5)
            if t < wake:
                g.blob(330, hy, 88, 82, SKIN, 7, 4)
                with g.at(330, hy):
                    g.face(80, mood)
                g.line([(310, hy - 78), (325, hy - 105), (340, hy - 76)], 7, smooth=True)
            else:
                g.kid(330, hy + 290 - 60, 1.0, mood, arms="up")
            g.blob(600, 1010 - 10 * (breath - 1) * 30, 330, 95 * breath, MINT, 8, 5)
            for i in range(5):
                g.line([(330 + i * 110, 950), (380 + i * 110, 1080)], 4, GREY)
            # Zzz
            if t < wake:
                for i in range(3):
                    p = ((t * 0.5 + i / 3) % 1)
                    g.text("Z", 440 + 90 * p + 15 * math.sin(p * 8), 820 - 260 * p, int(40 + 40 * p), "kanit",
                           a=math.sin(p * math.pi))
            else:
                s = pop(t, wake + 0.1)
                g.text("!?", 470, 520 - 170 * jump, 110, "kanit", sc=s, rot=12)
            # ? หมุนรอบหัว
            if t > L[3]:
                for i in range(4):
                    a = t * 2.5 + i * math.pi / 2
                    s = pop(t, L[3] + i * 0.12)
                    g.text("?", 330 + math.cos(a) * 190, 600 - 170 * jump + math.sin(a) * 60, 80, "kanit", sc=s)


# ------------------------------------------------------------------ 2. title
def s_title(g, t, L, d):
    out = e_io(seg(t, L[1] - 0.35, L[1] + 0.35))
    with g.at(0, -1400 * out):
        g.sunburst(CX, 820, 260, 620, 24, t * 12, 14, LGREY)
        s = pop(t, 0.05, 0.45)
        g.circle(CX, 820, 250 * s, WHITE, 10)
        g.text("วันนี้ในอดีต", CX, 650, 104, "kanit", sc=lerp(2.2, 1, e_out(seg(t, 0.05, 0.3))) if t > 0.05 else 0,
               rot=-6, a=seg(t, 0.05, 0.15), stroke=10)
        g.text("18", CX, 815, 230, "kanit", sc=pop(t, 0.6), color=RED, stroke=10)
        g.text("ตุลาคม", CX, 965, 78, "kanit", sc=pop(t, 0.9))
        sc = pop(t, 1.5)
        g.rrect(CX - 180 * sc, 1060 - 50 * sc, 360 * sc, 100 * sc, 30 * sc, GOLD2, 8 if sc > 0.1 else 0)
        g.text("ค.ศ. 1867", CX, 1058, 70, "kanit", sc=sc)
    with g.at(0, 1500 * (1 - out)):
        if out > 0:
            g.snow(t, 30, area=(0, 250, W, 1250))
            g.mountains(GROUND)
            g.ground(GROUND)
            for i, (px, s) in enumerate([(90, 1.0), (210, 0.75), (930, 1.1), (1020, 0.8)]):
                g.pine(px, GROUND + 20, s, seed=i)
            # ป้าย
            sc = pop(t, L[1] + 0.4)
            with g.at(CX, GROUND + 30, sc, 3 * math.sin(t * 2)):
                g.rrect(-12, -300, 24, 300, 6, BROWN2, 7)
                g.rrect(-230, -390, 460, 140, 20, WHITE, 8)
                g.text("อลาสกา", 0, -345, 82, "kanit")
                g.text("ALASKA", 0, -280, 30, "kanitr", color=GREY)
            # หมีขาวโผล่
            pk = e_back(seg(t, L[1] + 1.0, L[1] + 1.5))
            with g.at(820, GROUND + 140 - 150 * pk):
                g.blob(0, -50, 70, 62, WHITE, 7, 9)
                for sx in (-1, 1):
                    g.circle(sx * 50, -100, 18, WHITE, 6)
                with g.at(0, -50):
                    g.face(56, "happy")
                g.blob(0, -32, 10, 7, INK, 0, 2)
            g.c.rectangle(-400, GROUND + 60, W + 800, 800)
            g.fs(WHITE, 0)
            g.line([(-400, GROUND + 60), (W + 400, GROUND + 60)], 8)


# ------------------------------------------------------------------ 3. russia
def s_russia(g, t, L, d):
    worry = t > L[1]
    mood = "happy" if not worry else ("worry" if t < L[2] + 0.3 else "shock")
    bx = 360 + (8 * math.sin(t * 35) if t > L[2] + 0.4 else 0)
    # แผนที่อลาสกาพร้อมธงรัสเซีย
    ms = pop(t, 0.3)
    with g.at(780, 700, ms, 4 * math.sin(t * 2)):
        g.shape(ALASKA, 0, 0, 420, ICE_FILL, 7)
        g.line([(-40, -10), (-40, -170)], 6)
        g.flag(-40, -170, 110, 70, "ru", t, 0.6)
        g.text("อลาสกา", 0, 175, 52, "kanit")
    g.ground(GROUND + 40, WHITE)
    g.tsar(bx, GROUND + 60, pop(t, 0.0, 0.45) * 1.1, mood, pockets=pop(t, L[1] + 0.3))
    g.name_tag(t, 0.4, 380, 640, "พระเจ้าซาร์อเล็กซานเดอร์ที่ 2", "จักรพรรดิรัสเซีย", dur=L[1] - 0.2)
    # กระเป๋าว่าง: แมลงเม่าบินออก + เหรียญ 0
    if t > L[1] + 0.4:
        tt = t - L[1] - 0.4
        mx, my = bx + 110 + tt * 90, GROUND - 120 - tt * 120 + 25 * math.sin(tt * 9)
        if my > 200:
            with g.at(mx, my):
                for sx in (-1, 1):
                    g.blob(sx * 20, 0, 20, 14 + 8 * abs(math.sin(tt * 18)), LGREY, 4, sx)
                g.blob(0, 0, 6, 14, GREY, 3, 4)
        g.text("เงิน = 0", bx - 10, GROUND - 470, 66, "kanit", color=RED, sc=pop(t, L[1] + 0.6), rot=-5, stroke=8)
        for i in range(2):
            g.sweat(bx + 95 + i * 30, GROUND - 330 + ((t * 120 + i * 40) % 80), 1.2)
    # สิงโตอังกฤษแอบมอง
    if t > L[2] - 0.1:
        k = e_back(seg(t, L[2] - 0.1, L[2] + 0.5))
        lx = lerp(1300, 920, k) + 10 * math.sin(t * 3)
        g.lion(lx, 1030, 0.95, "think")
        g.text("อังกฤษ", lx - 20, 1215, 54, "kanit", sc=pop(t, L[2] + 0.5), stroke=8)
        g.text("!", bx + 120, GROUND - 450, 120, "kanit", sc=pop(t, L[2] + 0.4), color=RED)


ICE_FILL = (0.86, 0.92, 0.95, 1)


# ------------------------------------------------------------------ 4. deal
def s_deal(g, t, L, d):
    slide = e_out(seg(t, 0.0, 0.5))
    hand = e_back(seg(t, 0.55, 0.9))
    bx, sx = lerp(-200, 300, slide), lerp(1280, 780, slide)
    g.ground(GROUND + 40, WHITE)
    # มือจับกัน
    hx = CX + 0 * hand
    if hand > 0:
        g.line([(bx + 85, GROUND - 120), (lerp(bx + 120, hx - 10, hand), lerp(GROUND - 110, 900, hand))], 17, TUNIC)
        g.line([(sx - 60, GROUND - 120), (lerp(sx - 90, hx + 10, hand), lerp(GROUND - 110, 900, hand))], 16, COAT)
        g.circle(hx, 900 + 6 * math.sin(t * 25) * (t < 1.6), 30, SKIN, 7)
    g.tsar(bx, GROUND + 60, 1.0, "happy" if t < L[1] else "laugh")
    g.seward(sx, GROUND + 60, 1.0, "happy")
    g.name_tag(t, 0.6, sx - 60, 560, "วิลเลียม ซิวเวิร์ด", "รัฐมนตรีต่างประเทศสหรัฐฯ", dur=L[1] - 0.8, side=-1)
    burst(g, hx, 900, t, 0.85, 10, 180, 30)
    if t < L[1]:
        g.text("ดีล!", hx, 760, 100, "kanit", sc=pop(t, 0.9), rot=-8, color=RED, stroke=10)
    # แผนที่ลอยจากซาร์ไปซิวเวิร์ด
    mk = e_io(seg(t, 0.9, 1.7))
    with g.at(lerp(bx, sx, mk), 520 - 120 * math.sin(mk * math.pi), pop(t, 0.2) * 0.9):
        g.shape(ALASKA, 0, 0, 250, ICE_FILL, 6)
    # ถุงเงิน
    if t > L[1] - 0.1:
        dy = spring(t - L[1] + 0.1, 2.2, 5.0)
        with g.at(CX, lerp(-300, 1000, dy)):
            g.money_bag(0, 0, 0.9)
        burst(g, CX, 1000, t, L[1] + 0.25, 12, 330, 34, "coin")
        cnt = int(7_200_000 * e_out(seg(t, L[1] + 0.1, L[1] + 1.3)))
        g.text(f"${cnt:,}", CX, 560, 100, "kanit", sc=pop(t, L[1]), stroke=10)
        g.text("7.2 ล้านดอลลาร์", CX, 670, 56, "kanit", sc=pop(t, L[1] + 1.3), color=RED, stroke=8)


# ------------------------------------------------------------------ 5. map
def s_map(g, t, L, d):
    aw = 860
    shift = e_io(seg(t, L[1] - 0.2, L[1] + 0.4))
    aw2 = lerp(aw, 640, shift)
    th_w = math.sqrt(poly_area(ALASKA) * aw2 * aw2 / 2.9 / poly_area(THAILAND))  # สเกลพื้นที่จริง ~2.9 เท่า
    s = pop(t, 0.0, 0.5)
    ax, ay = lerp(CX, 380, shift), lerp(800, 700, shift)
    with g.at(ax, ay, s):
        g.shape(ALASKA, 0, 0, aw2, ICE_FILL, 9)
        for i in range(4):  # หมู่เกาะอะลูเชียน
            g.circle(-aw2 * 0.38 - i * 30, aw2 * 0.42 + i * 6, 9 - i, ICE_FILL, 5)
        g.text("อลาสกา", -aw2 * 0.05, -aw2 * 0.05, 60, "kanit", sc=pop(t, 0.3))
    # ป้ายราคา 2 เซนต์
    ps = pop(t, 0.5) * (1 - e_io(seg(t, L[1] - 0.3, L[1])))
    if ps > 0:
        with g.at(300, 1210, ps, 6 * math.sin(t * 3)):
            g.line([(0, -110), (0, -40)], 5)
            g.rrect(-170, -40, 340, 150, 24, WHITE, 8)
            g.circle(-105, 35, 48, GOLD, 6)
            g.text("2¢", -105, 37, 54, "kanit")
            g.text("/เอเคอร์", 50, 35, 50, "kanit")
        burst(g, 200, 1240, t, 0.6, 8, 160, 22)
    if t > L[1] - 0.1:
        ts = pop(t, L[1] - 0.1)
        tx, ty = 850, 820
        with g.at(tx, ty, ts):
            g.shape(THAILAND, 0, 0, th_w, GOLD2, 8)
        g.text("ไทย", tx + 20, ty - th_w * 0.18, 54, "kanit", sc=ts, stroke=8)
        # ×3 badge
        bs = pop(t, L[1] + 0.9)
        with g.at(CX, 1235, bs, -3):
            g.rrect(-330, -85, 660, 170, 40, WHITE, 8)
            for i in range(3):
                k = pop(t, L[1] + 1.1 + i * 0.3)
                with g.at(-230 + i * 115, 0, k):
                    g.shape(THAILAND, 0, 0, 120, GOLD2, 5)
            g.text("≈ อลาสกา", 160, 0, 60, "kanit", sc=pop(t, L[1] + 2.0), color=RED)


# ------------------------------------------------------------------ 6. laugh
LAUGHERS = [(150, "top", 81, False), (390, "bowler", 82, True), (650, "top", 83, True), (900, "bowler", 84, False)]


def crowd(g, t, mood, t0=0.0, y=GROUND + 200, sc=0.95):
    for i, (x, hat, seed, mus) in enumerate(LAUGHERS):
        k = pop(t, t0 + i * 0.1)
        bob = 14 * abs(math.sin(t * 9 + i)) if mood == "laugh" else 0
        if k > 0:
            g.person(x, y - bob, sc * k, mood, hat, seed, mus, col=[GREY, NAVY, BROWN2, LGREY][i])


def newspaper(g, x, y, sc, rot, title, sub):
    with g.at(x, y, sc, rot):
        g.rrect(-330, -230, 660, 460, 10, (0.97, 0.95, 0.89, 1), 8)
        g.text("THE DAILY NEWS · 1867", 0, -195, 32, "kanitr")
        g.line([(-300, -170), (300, -170)], 5)
        g.text(title, 0, -110, 66, "kanit", maxw=600)
        g.text(sub, 0, -40, 34, "kanitr", color=GREY)
        g.fridge(-170, 190, 0.38)
        for i in range(6):
            g.line([(-50, 20 + i * 30), (290 - (i % 3) * 40, 20 + i * 30)], 6, LGREY)


def s_laugh(g, t, L, d):
    up = e_io(seg(t, L[2] - 0.2, L[2] + 0.4))
    if t > L[1] - 0.2:
        k = e_out(seg(t, L[1] - 0.2, L[1] + 0.5))
        newspaper(g, CX, lerp(700, 520, up), k * lerp(1.0, 0.72, up), (1 - k) * 720 + lerp(-3, 6, up),
                  "ตู้เย็นของซิวเวิร์ด!", "SEWARD'S ICEBOX")
    if t > L[2] - 0.1:
        k = e_back(seg(t, L[2], L[2] + 0.5))
        with g.at(CX, lerp(1700, 1130, k)):
            g.rrect(-190, -470, 380, 450, 190, WHITE, 9)
            g.seward(0, -40, 0.95, "worry")
            g.rrect(-170, -60, 340, 80, 20, GOLD2, 7)
            g.text("ซิวเวิร์ด", 0, -20, 54, "kanit")
        for i in range(2):
            g.sweat(CX + 120 + i * 30, 790 + ((t * 120 + i * 40) % 70), 1.3)
    show_crowd = 1 - e_io(seg(t, L[2] - 0.2, L[2] + 0.3))
    if show_crowd > 0:
        with g.at(0, 400 * (1 - show_crowd)):
            crowd(g, t, "laugh", 0.0, GROUND + 110)
            if t < L[1] - 0.2:
                haha(g, t, [(200, 650, -12), (480, 560, 8), (760, 640, -5), (900, 500, 12), (340, 430, 4)], 0.2)
            else:
                haha(g, t, [(110, 1080, -12), (970, 1050, 10)], L[1])
    else:
        haha(g, t, [(160, 1250, -12), (930, 1260, 10), (180, 650, 6)], L[2] + 0.3)


# ------------------------------------------------------------------ 7. ceremony
def ceremony_bg(g, t, ru_y=None, ru_crumple=0.0, us_y=None, salute=0.0):
    g.mountains(GROUND - 60, 0.5)
    g.ground(GROUND)
    # ป้อมไม้
    g.rrect(40, GROUND - 260, 260, 260, 6, BROWN2, 7)
    g.poly([(20, GROUND - 260), (170, GROUND - 360), (320, GROUND - 260)], BROWN, 7)
    g.rrect(140, GROUND - 120, 60, 120, 6, INK, 0)
    # เสาธง
    g.rrect(CX - 9, 330, 18, GROUND - 330, 8, LGREY, 6)
    g.circle(CX, 322, 18, GOLD, 6)
    if ru_y is not None:
        g.flag(CX + 9, ru_y, 260, 165, "ru", t, 1.0, ru_crumple)
    if us_y is not None:
        g.flag(CX + 9, us_y, 280, 170, "us", t, 1.0)


def soldiers(g, t, salute=0.0, flag_on=0.0):
    for i in range(3):
        g.soldier(110 + i * 105, GROUND + 175, 0.95, GREY, 61 + i, salute)
        g.soldier(680 + i * 105, GROUND + 175, 0.95, BLUE, 71 + i, salute)
    if flag_on > 0:   # ธงรัสเซียตกบนดาบปลายปืน
        with g.at(800, GROUND - 60, flag_on, -8):
            g.flag(-130, -60, 230, 120, "ru", t * 0.3, 0.5, 0.2)
            for k in range(3):
                g.circle(-60 + k * 65, -20 + 15 * k, 9, PAPER, 4)


def s_ceremony(g, t, L, d):
    zoom = lerp(1.18, 1.0, e_out(seg(t, 0, 1.4)))
    lower = e_io(seg(t, L[2], L[3] - 0.1)) * 0.55
    ru_y = lerp(340, 860, lower)
    stuck = t > L[3] - 0.1
    crumple = e_back(seg(t, L[3] - 0.1, L[3] + 0.3)) if stuck else 0
    fall = seg(t, L[5] - 0.1, L[5] + 0.6)
    climb = e_io(seg(t, L[4], L[5] - 0.2))
    shake = (10 * math.sin(t * 45) if L[3] < t < L[3] + 0.8 else 0) + (14 * math.sin(t * 50) * (1 - seg(t, L[5] + 0.5, L[5] + 0.9)) if L[5] + 0.5 < t < L[5] + 0.9 else 0)
    with g.at(CX + shake, 900, zoom):
        with g.at(-CX, -900):
            g.text("18 ต.ค. 1867", 250, 330, 64, "kanit", sc=pop(t, 0.2), stroke=8)
            ry = None if fall > 0 else ru_y
            ceremony_bg(g, t, ry, crumple)
            if fall > 0 and fall < 1:   # ธงร่วง
                fx = lerp(CX + 60, 800 - 130, fall)
                fy = lerp(ru_y, GROUND - 120, e_in(fall))
                with g.at(fx, fy, 1, fall * 200):
                    g.flag(0, 0, 200, 130, "ru", t, 1.5, 0.3)
            if t > L[4] - 0.1 and t < L[5] + 0.8:
                cy = lerp(GROUND + 30, ru_y + 230, climb)
                k = math.sin(t * 16) * (0 < climb < 1)
                with g.at(CX - 30, cy):
                    g.line([(-8, -110), (-40, -150 - 20 * k)], 9)
                    g.line([(8, -110), (40, -150 + 20 * k)], 9)
                g.soldier(CX - 30, cy, 0.85, GREY, 99, rifle=False)
            soldiers(g, t, 0, 1.0 if fall >= 1 else 0)
            if fall >= 1:
                g.text("ฉึก!", 860, GROUND - 240, 96, "kanit", color=RED, sc=pop(t, L[5] + 0.55), rot=10, stroke=10)
            if stuck and t < L[5]:
                g.text("!!", CX + 190, ru_y - 30, 110, "kanit", color=RED, sc=pop(t, L[3]))
            if t > L[1] - 0.1:
                g.text("เมืองซิตกา", 170, GROUND - 400, 54, "kanit", sc=pop(t, L[1]), rot=-4, stroke=8)
    # ภรรยาผู้ว่าการเป็นลม (foreground)
    if t > L[6] - 0.5:
        k = e_out(seg(t, L[6] - 0.5, L[6] - 0.1))
        faint = e_in(seg(t, L[6] + 0.3, L[6] + 0.9))
        lx = lerp(1250, 930, k)
        g.lady(lx, 1290, 0.95, -82 * faint, "shock" if faint < 0.5 else "dizzy")
        g.name_tag(t, L[6] - 0.3, 760, 1000, "เจ้าหญิงมาเรีย มักซูโตวา", "ภรรยาผู้ว่าการอลาสกา", dur=2.6)
        if faint >= 1:
            for i in range(3):
                a = t * 4 + i * 2.1
                g.star(lx - 210 + math.cos(a) * 60, 1230 + math.sin(a) * 22, 18, GOLD2, 4)


# ------------------------------------------------------------------ 8. calendar
def s_calendar(g, t, L, d):
    pan = e_io(seg(t, L[1] - 0.4, L[1] + 0.3))
    rise = e_out(seg(t, 0.1, L[1] - 0.5))
    if pan < 1:
        with g.at(0, 1500 * pan):
            ceremony_bg(g, t, None, 0, lerp(GROUND - 200, 340, rise))
            soldiers(g, t, e_out(seg(t, 0.4, 0.8)), 1.0)
            g.lady(930, 1290, 0.95, -82, "dizzy")
            burst(g, CX + 150, 400, t, L[1] - 0.6, 12, 200, 28)
    if pan > 0:
        with g.at(0, -1500 * (1 - pan)):
            jump = seg(t, L[2] + 0.3, L[2] + 1.3)
            num = 6 if jump <= 0 else 6 + int(12 * e_io(jump))
            flip = ((12 * e_io(jump)) % 1, num) if 0 < jump < 1 else None
            twin = e_io(seg(t, L[3] - 0.2, L[3] + 0.4))
            cx1 = lerp(CX, 290, twin)
            g.calendar(cx1, 760, 1.35 - 0.4 * twin, 6 if twin > 0 else num, flip=None if twin > 0 else flip)
            if twin > 0:
                g.calendar(lerp(CX, 790, twin), 760, 1.35 - 0.4 * twin, 18)
                g.text("→", CX + 10, 790, 120, "kanit", sc=pop(t, L[3] + 0.3))
                for i, x in enumerate((290, 790)):
                    k = pop(t, L[3] + 0.5 + i * 0.25)
                    if k <= 0.001:
                        continue
                    with g.alpha(0.9):
                        g.c.save()
                        g.c.translate(x, 707)
                        g.c.scale(k, 0.45 * k)
                        g.arc(0, 0, 105, 0, 360, 7, RED)
                        g.c.restore()
                g.text("ศุกร์ × 2", CX, 1080, 96, "kanit", color=RED, sc=pop(t, L[3] + 1.0), rot=-4, stroke=10)
            elif jump > 0:
                g.text("+12 วัน!", CX + 250, 470, 72, "kanit", color=RED, sc=pop(t, L[2] + 0.4), rot=12, stroke=8)
                # ลูกศรโค้ง
                g.line([(CX - 250 + 500 * i / 12, 470 - 120 * math.sin(math.pi * i / 12)) for i in range(13)][:int(1 + 12 * jump)], 7)
            g.kid(880 if twin <= 0 else CX, 1330 if twin <= 0 else 1340, 0.75 * pop(t, L[2] + 1.0), "laugh",
                  arms="up" if twin > 0 else "down")


# ------------------------------------------------------------------ 9. twist
def s_twist(g, t, L, d):
    g.ground(GROUND + 20)
    # ทอง
    if t > L[1] - 0.1:
        k = spring(t - L[1] + 0.1, 2, 6)
        for i in range(7):
            gx = 160 + (i % 4) * 80 + (i // 4) * 40
            gy = GROUND + 10 - (i // 4) * 50 - 90 * k * (0.5 + 0.5 * hn(i, 3))
            g.blob(gx, gy, 38, 28, GOLD, 6, i)
        burst(g, 260, GROUND - 120, t, L[1], 10, 230, 32)
        g.kid(280, GROUND + 200, 0.75 * pop(t, L[1] + 0.2), "laugh", hat="miner", arms="up")
        g.text("ทอง!", 270, 640, 110, "kanit", color=GOLD, sc=pop(t, L[1] + 0.1), rot=-8, stroke=12)
    # น้ำมัน
    if t > L[2] - 0.2:
        k = e_back(seg(t, L[2] - 0.2, L[2] + 0.3))
        with g.at(830, GROUND + 20, 1, sy=k, sx=1):
            g.poly([(-110, 0), (110, 0), (25, -420), (-25, -420)], None, 9)
            for j in range(5):
                y0 = -80 * j
                g.line([(-110 + 17 * j, y0), (110 - 17 * (j + 1), y0 - 80)], 5)
                g.line([(110 - 17 * j, y0), (-110 + 17 * (j + 1), y0 - 80)], 5)
        if t > L[2] + 0.3:
            gt = t - L[2] - 0.3
            hgt = min(gt * 900, 420)
            g.rrect(810, GROUND - 400 - hgt, 40, hgt, 20, INK, 0)
            for i in range(16):
                p = (gt * 1.3 + i / 16) % 1
                ang = math.radians(-90 + (hn(i, 4) * 70))
                px = 830 + math.cos(ang) * 320 * p
                py = GROUND - 400 - hgt + math.sin(ang) * 260 * p + 500 * p * p
                g.blob(px, py, 16, 22, INK, 0, i)
            g.text("น้ำมัน!", 760, 520, 104, "kanit", sc=pop(t, L[2] + 0.3), rot=6, stroke=12)
    # ตู้เย็นเปิด
    if t > L[3] - 0.2:
        k = e_back(seg(t, L[3] - 0.2, L[3] + 0.3))
        op = e_out(seg(t, L[3] + 0.2, L[3] + 0.7))
        with g.alpha(k if k < 1 else 1):
            g.c.rectangle(-400, -400, W + 800, H + 800)
            g.c.set_source_rgba(*PAPER[:3], 0.85 * k)
            g.c.fill()
            g.sunburst(CX, 820, 240, 650, 22, t * 20, 16, GOLD2)
            g.fridge(CX, 1130, 1.25 * k, op, "gold", glow=op)
            g.seward(CX + 280, 1350, 0.85 * pop(t, L[3] + 0.5), "smug")
            burst(g, CX, 800, t, L[3] + 0.6, 12, 300, 34)
    # คนหัวเราะ -> เงียบ (ด้านหน้า)
    if t < L[1] + 0.3 or True:
        y = GROUND + 110
        fade = 1 - seg(t, L[1] - 0.2, L[1] + 0.2)
        if fade > 0:
            with g.alpha(fade):
                crowd(g, t, "flat" if t < L[1] - 0.1 else "shock", -1, y)
            if t < L[1]:
                g.bubble(CX, 760, 260, 150)
                g.text("...", CX, 745, 96, "kanit", sc=pop(t, 0.3))
                for i in range(len(LAUGHERS)):
                    g.sweat(LAUGHERS[i][0] + 70, y - 330 + ((t * 100 + i * 30) % 60), 1.1)


# ------------------------------------------------------------------ 10. today
def s_today(g, t, L, d):
    g.sunburst(CX, 700, 180, 700, 28, t * 15, 12, LGREY)
    with g.at(CX, 330):
        g.rrect(-12, 0, 24, 600, 8, LGREY, 6)
    fs = pop(t, 0.1, 0.5)
    with g.at(CX + 12, 340, fs):
        g.flag(0, 0, 380, 250, "ak", t, 1.0)
    g.text("ธงอลาสกา", CX + 200, 640, 44, "kanit", sc=fs, stroke=6)
    ss = pop(t, 0.6)
    with g.at(250, 720, ss * 0.85, 8 * math.sin(t * 2)):
        g.star(0, 0, 170, GOLD2, 9)
        g.text("รัฐที่", 0, -38, 44, "kanit")
        g.text("49", 0, 35, 110, "kanit")
    if t > L[1] - 0.2:
        bs = pop(t, L[1] - 0.2)
        with g.at(CX, 1000, bs, -3 + 2 * math.sin(t * 3)):
            g.poly([(-430, -80), (430, -80), (400, 0), (430, 80), (-430, 80), (-400, 0)], RED, 9)
            g.text("วันอลาสกา  18 ต.ค.", 0, 0, 74, "kanit", WHITE)
        confetti(g, t, 70, t0=L[1])
    dance = math.sin(t * 8)
    g.seward(230, 1350, 0.72 * pop(t, 1.0), "laugh", rot=6 * dance)
    g.kid(CX, 1350, 0.72 * pop(t, 1.2), "laugh", rot=-6 * dance, hat="party", arms="up")
    g.sam(850, 1350, 0.72 * pop(t, 1.4), "laugh", rot=6 * dance, arm=0.5 + 0.5 * dance)


# ------------------------------------------------------------------ 11. outro
def s_outro(g, t, L, d):
    a = 1 - e_io(seg(t, L[2] - 0.3, L[2] + 0.1))
    if a > 0:
        with g.alpha(a):
            crowd(g, t, "laugh", 0.0, 820, 0.7)
            with g.at(CX, 930):
                g.line([(-260, 0), (260, 0)], 10)
                g.poly([(240, -30), (290, 0), (240, 30)], INK, 6)
            # หีบสมบัติ
            cs = pop(t, L[1])
            op = e_out(seg(t, L[1] + 0.3, L[1] + 0.8))
            with g.at(CX, 1190, cs):
                if op > 0:
                    g.sunburst(0, -120, 120, 330, 14, t * 30, 12, GOLD2)
                g.rrect(-170, -120, 340, 160, 18, BROWN2, 8)
                with g.at(0, -120, 1, sy=1 - 1.8 * op, sx=1):
                    g.rrect(-170, -90, 340, 90, 40, BROWN2, 8)
                if op > 0:
                    for i in range(5):
                        g.coin(-110 + i * 55, -140 - 30 * math.sin(i), 30, "$", t * 100 + i * 40)
                g.rrect(-25, -95, 50, 60, 10, GOLD, 6)
            burst(g, CX, 1090, t, L[1] + 0.5, 12, 280, 30)
    if t > L[2] - 0.2:
        g.kid(290, 1330, 0.9 * pop(t, L[2] - 0.2), "think", arms="chin")
        g.text("?", 520, 720, 260, "kanit", sc=pop(t, L[2]), rot=10 * math.sin(t * 3), color=RED, stroke=12)
        for i, (lbl, col, x) in enumerate([("ซื้อ!", GOLD2, 760), ("ไม่ซื้อ", LGREY, 760)]):
            k = pop(t, L[2] + 0.3 + i * 0.2)
            bob = 1 + 0.06 * math.sin(t * 7 + i * math.pi)
            with g.at(x, 1000 + i * 220, k * bob):
                g.rrect(-180, -75, 360, 150, 75, col, 9)
                g.text(lbl, 0, -4, 76, "kanit")
    if t > L[3] - 0.1:
        k = pop(t, L[3])
        with g.at(CX, 420, k, -4 + 3 * math.sin(t * 4)):
            g.bubble(0, 0, 680, 220, WHITE, (1, 1))
            g.text("เมนต์บอกกันนะ!", 0, -10, 84, "kanit")
        g.text("พรุ่งนี้เจอกัน!", CX, 1780, 60, "kanit", sc=pop(t, L[3] + 1.2), color=RED)


SCENES = {
    "hook": s_hook, "title": s_title, "russia": s_russia, "deal": s_deal, "map": s_map,
    "laugh": s_laugh, "ceremony": s_ceremony, "calendar": s_calendar, "twist": s_twist,
    "today": s_today, "outro": s_outro,
}
# ฉากที่ต่อกันไม่ต้องมีม่านวงกลม
NO_IRIS = {("ceremony", "calendar")}

