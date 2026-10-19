"""ฉากตอน: อนุสัญญาปี 1818 — เส้นขนานที่ 49 (20 ต.ค. 1818)"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from chars import (CANADA, LAKE, USA, bomb, car, gallatin, john_bull, pine, robinson, school,  # noqa: E402
                   tipi, union_jack, white_house)
from fx import confetti  # noqa: E402
from gfx import (BLUE, BROWN, BROWN2, GOLD, GOLD2, GREY, INK, LGREY, NAVY, RED, W, WHITE, e_back, e_in,  # noqa: E402
                 e_io, e_out, hexc, hn, lerp, pop, seg)

CX = W / 2
GROUND = 1180
LINE_Y = 760          # เส้นขนานที่ 49 บนแผนที่
LAKE_X = 820          # ทะเลสาบออฟเดอะวูดส์
ROCKY_X = 230         # เทือกเขาร็อกกี
PAPER_MAP = hexc("#f7efd9")

CAMERA = {"hook": "push_in", "frontier": "tilt_down", "treaty": "push_in", "weird": "pan_right",
          "peace": "pull_out"}


def smoke(g, x, y, t, n=5, s=1.0):
    for i in range(n):
        p = (t * 0.35 + i / n) % 1
        with g.alpha(math.sin(p * math.pi) * 0.8):
            g.blob(x + 20 * hn(i, 2) + 30 * p, y - 220 * p, (36 + 40 * p) * s, (30 + 36 * p) * s, LGREY, 5, i)


def na_map(g, t, border=0.0, wavy=1.0, angle=0.0, glow=0.0, x0=60, x1=1020, y0=380, y1=1140, frame=True):
    """แผนที่อเมริกาเหนือแบบสัญลักษณ์: แคนาดา (บน) / สหรัฐฯ (ล่าง)
    border = ความคืบหน้าการลากเส้นตรง 0..1 (จากทะเลสาบไปทางตะวันตก), wavy = ความชัดของพรมแดนคลุมเครือเดิม"""
    g.rrect(x0, y0, x1 - x0, y1 - y0, 30, PAPER_MAP, 8 if frame else 0)
    g.c.save()
    g.c.rectangle(x0 + 6, y0 + 6, x1 - x0 - 12, y1 - y0 - 12)
    g.c.clip()
    g.c.rectangle(x0, y0, x1 - x0, LINE_Y - y0)
    g.fs(CANADA, 0)
    g.c.rectangle(x0, LINE_Y, x1 - x0, y1 - LINE_Y)
    g.fs(USA, 0)
    g.text("แคนาดา (อังกฤษ)", CX + 120, y0 + 60, 46, "kanit", GREY)
    g.text("สหรัฐอเมริกา", CX + 120, y1 - 50, 46, "kanit", GREY)
    for i in range(3):   # เทือกเขาร็อกกี
        mx = ROCKY_X - 60 + i * 60
        g.poly([(mx - 70, LINE_Y + 120), (mx, LINE_Y - 110 + 30 * (i % 2)), (mx + 70, LINE_Y + 120)], LGREY, 6)
        g.poly([(mx - 22, LINE_Y - 50 + 30 * (i % 2)), (mx, LINE_Y - 110 + 30 * (i % 2)),
                (mx + 22, LINE_Y - 50 + 30 * (i % 2))], WHITE, 4)
    g.blob(LAKE_X + 20, LINE_Y + 10, 80, 55, LAKE, 6, 3)                 # ทะเลสาบออฟเดอะวูดส์
    if wavy > 0:   # พรมแดนเดิมที่คลุมเครือ (เส้นประคดเคี้ยว)
        with g.alpha(wavy):
            pts = [(x, LINE_Y + 70 * math.sin(x * 0.012 + 1) + 30 * math.sin(x * 0.04)) for x in range(x0, x1, 18)]
            for i in range(0, len(pts) - 1, 2):
                g.line([pts[i], pts[i + 1]], 7, RED, amp=0)
    if angle > 0:   # นอร์ทเวสต์ แองเกิล: ติ่งแผ่นดินสหรัฐฯ เหนือเส้น
        with g.alpha(angle):
            g.poly([(LAKE_X + 50, LINE_Y - 70), (LAKE_X + 110, LINE_Y - 85), (LAKE_X + 120, LINE_Y - 30),
                    (LAKE_X + 60, LINE_Y - 20)], USA, 5, stroke=NAVY)
    if border > 0:
        xe = lerp(LAKE_X - 40, ROCKY_X + 50, border)
        lw = 10 + 6 * glow
        if glow > 0:
            g.line([(LAKE_X - 40, LINE_Y), (xe, LINE_Y)], lw + 18, (0.95, 0.82, 0.4, 0.6 * glow), amp=0)
        g.line([(LAKE_X - 40, LINE_Y), (xe, LINE_Y)], lw, NAVY, amp=0)
    g.c.restore()


def pen_and_ruler(g, x, y, s=1.0, rot=-20):
    with g.at(x, y, s, rot):
        g.poly([(0, 0), (-14, -40), (14, -40)], INK, 0)
        g.rrect(-14, -230, 28, 190, 10, GOLD, 6)
        g.rrect(-14, -250, 28, 30, 6, INK, 0)


def ruler(g, x0, x1, y, a=1.0):
    with g.alpha(a):
        g.rrect(x0, y - 70, x1 - x0, 50, 6, hexc("#f2d27b"), 6)
        for i in range(int((x1 - x0) / 30)):
            g.line([(x0 + 15 + i * 30, y - 70), (x0 + 15 + i * 30, y - 70 + (20 if i % 2 else 12))], 4, BROWN)


def badge(g, t, t0, x, y, txt, col=GOLD2, size=70, rot=-5):
    k = pop(t, t0)
    if k > 0:
        with g.at(x, y, k, rot):
            from gfx import text_sprite
            _, _, w, _ = text_sprite(txt, size, "kanit")
            g.rrect(-w / 2 - 30, -size * 0.8, w + 60, size * 1.6, size * 0.7, col, 8)
            g.text(txt, 0, -2, size, "kanit")


# ------------------------------------------------------------------ 1. hook
def s_hook(g, t, L, d):
    if t < L[2] - 0.2:
        g.sunburst(CX, 760, 220, 640, 24, t * 10, 14, LGREY)
        g.text("วันนี้ในอดีต", CX, 620, 104, "kanit", sc=lerp(2.0, 1, e_out(seg(t, 0.1, 0.4))) if t > 0.1 else 0, rot=-5)
        g.text("20 ตุลาคม 1818", CX, 760, 84, "kanit", RED, sc=pop(t, 0.8))
        if t > L[1] - 0.2:
            g.text("?", CX, 960, 220, "kanit", RED, sc=pop(t, L[1]), rot=10 * math.sin(t * 3))
        return
    if t < L[3] - 0.2:   # เส้นตรงเส้นเดียว ลากด้วยไม้บรรทัด
        prog = e_io(seg(t, L[2] + 0.3, L[3] - 0.4))
        na_map(g, t, border=prog, wavy=0.0)
        ruler(g, 120, 960, LINE_Y, 1.0)
        pen_and_ruler(g, lerp(LAKE_X - 40, ROCKY_X + 50, prog), LINE_Y - 4, 1.0)
        return
    g.ground(GROUND, WHITE)
    peace = e_out(seg(t, L[4] - 0.1, L[4] + 0.7))
    sx = lerp(260, 400, peace)
    bx = lerp(820, 680, peace)
    g.sam(sx, GROUND + 80, 1.05, "worry" if peace < 0.5 else "laugh", arm=peace)
    john_bull(g, bx, GROUND + 80, 1.05, "worry" if peace < 0.5 else "laugh", arm=peace)
    if peace < 0.5:
        g.text("!!", CX, 640, 130, "kanit", RED, sc=pop(t, L[3]), rot=-6)
    else:
        for i in range(3):
            a = t * 2 + i * 2.1
            g.star(CX + math.cos(a) * 120, 650 + math.sin(a) * 40, 22, GOLD2, 4)
        g.text("เพื่อนบ้าน", CX, 520, 76, "kanit", sc=pop(t, L[4] + 0.6))


# ------------------------------------------------------------------ 2. tension
def s_tension(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[3] - 0.2:
        badge(g, t, 0.2, CX, 420, "สงคราม 1812–1815")
        g.sam(300, GROUND + 80, 1.05, "worry" if t < L[2] else "sad")
        john_bull(g, 780, GROUND + 80, 1.05, "smug")
        if t > L[2] - 0.2:   # ความแค้นคุกรุ่น
            for i, x in enumerate((300, 780)):
                for k in range(3):
                    p = (t * 0.8 + k / 3) % 1
                    with g.alpha(math.sin(p * math.pi)):
                        g.blob(x + 40 * math.sin(k + t), 760 - 120 * p, 26 + 20 * p, 22 + 16 * p, LGREY, 4, k)
            g.text("ความแค้น", CX, 560, 70, "kanit", RED, sc=pop(t, L[2]))
        return
    white_house(g, CX, GROUND - 40, 1.4 * pop(t, L[3] - 0.2))
    smoke(g, CX - 140, GROUND - 330, t, 5, 1.1)
    smoke(g, CX + 140, GROUND - 330, t + 1.3, 5, 1.0)
    badge(g, t, L[3] + 0.3, CX, 440, "ทำเนียบขาว · 1814", WHITE, 60)


# ------------------------------------------------------------------ 3. frontier
def s_frontier(g, t, L, d):
    na_map(g, t, border=0.0, wavy=pop(t, 0.2))
    if t > L[1] - 0.2:
        union_jack(g, 110, 420, 120 * pop(t, L[1] - 0.2), 70 * pop(t, L[1] - 0.2))
    if t > L[2] - 0.2:
        for i, (x, y) in enumerate(((300, 700), (560, 820), (760, 690))):
            g.text("?", x, y + 10 * math.sin(t * 4 + i), 110, "kanit", RED, sc=pop(t, L[2] - 0.2 + i * 0.2))
    if t > L[3] - 0.2:
        for i in range(6):
            pine(g, 380 + i * 70, 690 + (i % 2) * 25, 0.9 * pop(t, L[3] - 0.2 + i * 0.08))
        pts = [(380 + i * 30, 1000 + 40 * math.sin(i * 0.8)) for i in range(16)]
        g.line(pts[:max(2, int(16 * seg(t, L[3], L[3] + 1.5)))], 14, hexc("#7fb2d8"), amp=0)
    if t > L[4] - 0.2:
        bomb(g, CX + 30, 800 + 6 * math.sin(t * 20), 1.1 * pop(t, L[4] - 0.2), t)
        g.text("ระเบิดเวลา!", CX + 30, 1000, 76, "kanit", RED, sc=pop(t, L[4] + 0.4), rot=-6, stroke=10)


# ------------------------------------------------------------------ 4. treaty
def s_treaty(g, t, L, d):
    if t < L[4] - 0.2:
        g.ground(GROUND, WHITE)
        if t < L[1] - 0.2:   # ความตึงเครียดพุ่งถึงขีดสุด
            k = e_out(seg(t, 0.2, L[1] - 0.4))
            g.rrect(CX - 50, 380, 100, 640, 50, WHITE, 8)
            g.rrect(CX - 36, 1006 - 610 * k, 72, 610 * k, 36, RED, 0)
            g.circle(CX, 1040, 80, RED, 8)
            g.text("ความตึงเครียด", CX, 1170, 56, "kanit", sc=pop(t, 0.3))
            return
        k = e_out(seg(t, L[1] - 0.2, L[1] + 0.5))
        gallatin(g, lerp(-200, 290, k), GROUND + 80, 1.05, "happy", arm=0.3 if t > L[2] else 0)
        robinson(g, lerp(1300, 790, k), GROUND + 80, 1.05, "happy", arm=0.3 if t > L[2] else 0)
        g.name_tag(t, L[1] + 0.4, 300, 600, "อัลเบิร์ต แกลลาทิน", "ทูตสหรัฐฯ", dur=2.6)
        g.name_tag(t, L[1] + 0.9, 780, 760, "เฟรเดอริก โรบินสัน", "ทูตอังกฤษ", dur=2.6, side=-1)
        if t > L[2] - 0.2:   # อนุสัญญา
            kd = pop(t, L[2] - 0.2)
            with g.at(CX, 560, kd, -3):
                g.rrect(-180, -150, 360, 300, 14, WHITE, 8)
                g.text("อนุสัญญา", 0, -90, 56, "kanit")
                g.text("ปี 1818", 0, -30, 56, "kanit", RED)
                for i in range(3):
                    g.line([(-130, 30 + i * 30), (130 - i * 30, 30 + i * 30)], 5, LGREY)
                g.circle(-80, 115, 26, RED, 4)
                g.circle(80, 115, 26, BLUE, 4)
        if t > L[3] - 0.2:   # ไม่ส่งทหารไปตาย
            ks = pop(t, L[3] - 0.2)
            for i, x in enumerate((CX - 90, CX + 90)):
                g.soldier(x, GROUND + 170, 0.8 * ks, GREY, 900 + i)
            with g.at(CX, GROUND - 40, ks):
                g.line([(-160, -140), (160, 100)], 18, RED, amp=0)
                g.line([(160, -140), (-160, 100)], 18, RED, amp=0)
        return
    # กางแผนที่ -> ลากเส้นขนานที่ 49
    unroll = e_out(seg(t, L[4] - 0.2, L[4] + 0.8))
    g.c.save()
    g.c.rectangle(-400, 340, W + 800, 40 + 820 * unroll)
    g.c.clip()
    prog = e_io(seg(t, L[5] + 0.3, L[6] + 0.6))
    na_map(g, t, border=prog, wavy=1 - seg(t, L[5], L[5] + 0.8))
    g.c.restore()
    if 0 < prog < 1:
        ruler(g, 120, 960, LINE_Y, 1.0)
        pen_and_ruler(g, lerp(LAKE_X - 40, ROCKY_X + 50, prog), LINE_Y - 4, 1.0)
    if t > L[5] + 0.4:
        badge(g, t, L[5] + 0.6, CX, 330, "เส้นขนานที่ 49", GOLD2, 56)
    if t > L[6] - 0.2:
        g.text("← นับพันกิโลเมตร →", CX + 40, LINE_Y + 70, 48, "kanit", NAVY, sc=pop(t, L[6]))
    if t > L[7] - 0.2:
        g.text("ทะเลสาบออฟเดอะวูดส์", LAKE_X - 20, LINE_Y + 150, 40, "kanit", sc=pop(t, L[7]))
        g.text("เทือกเขาร็อกกี", ROCKY_X + 40, LINE_Y - 190, 44, "kanit", sc=pop(t, L[7] + 0.6))


# ------------------------------------------------------------------ 5. weird
def s_weird(g, t, L, d):
    if t < L[3] - 0.2:
        g.ground(GROUND, WHITE)
        # เส้นตรงผ่าป่า: ต้นไม้/กระโจมถูกแบ่งสองฝั่ง
        g.line([(-400, 860), (W + 400, 860)], 12, NAVY, amp=0)
        g.text("เส้นขนานที่ 49", 160, 820, 44, "kanit", NAVY, sc=pop(t, 0.3))
        for i in range(7):
            x = 90 + i * 150
            pine(g, x, 860 - 40 + (i % 2) * 20, 1.3 * pop(t, 0.2 + i * 0.07))
        if t > L[1] - 0.2:
            g.text("สุดพิลึก!", CX, 520, 90, "kanit", RED, sc=pop(t, L[1]), rot=-6)
        if t > L[2] - 0.2:
            for i, (x, y) in enumerate(((330, 760), (720, 1100))):
                tipi(g, x, y, 1.1 * pop(t, L[2] - 0.2 + i * 0.2))
            for i, (x, y, side) in enumerate(((470, 760, 1), (600, 1100, -1))):
                g.person(x, y + 140, 0.65 * pop(t, L[2] + 0.4 + i * 0.2), "sad", "none", 930 + i, False, BROWN2)
            g.text("ชนเผ่าพื้นเมือง", 850, 980, 50, "kanit", sc=pop(t, L[2] + 0.6))
        return
    # นอร์ทเวสต์ แองเกิล: ซูม 3 เท่าเข้าไปที่ติ่งแผ่นดินเหนือเส้น (จุด AX, AY ไปอยู่กลางจอ)
    AX, AY, Z = LAKE_X + 85, LINE_Y - 50, 3.0
    zoom = e_io(seg(t, L[3] - 0.2, L[3] + 1.0))
    s_ = lerp(1.0, Z, zoom)
    tx = lerp(CX, CX - Z * (AX - CX), zoom)
    ty = lerp(760, 760 - Z * (AY - 760), zoom)
    g.c.save()
    g.c.rectangle(60, 380, 960, 760)          # จำกัดในกรอบแผนที่ ไม่ล้นลงพื้นที่ซับ
    g.c.clip()
    with g.at(tx, ty, s_):
        with g.at(-CX, -760):
            na_map(g, t, border=1.0, wavy=0.0, angle=1.0, frame=zoom < 0.05)
    g.c.restore()
    g.rrect(60, 380, 960, 760, 30, None, 8)
    by = ty + s_ * (LINE_Y - 760)              # เส้นพรมแดนหลังซูม
    if t > L[3] + 0.6:
        badge(g, t, L[3] + 0.8, CX, 330, "นอร์ทเวสต์ แองเกิล", GOLD2, 58)
    if t > L[4] - 0.2:   # ธงสหรัฐฯ บนติ่งแผ่นดิน ล้อมรอบด้วยแคนาดา
        k = pop(t, L[4] - 0.2)
        g.rrect(CX + 60 - 4, 600, 8, 160 * k, 3, GREY, 3)
        g.flag(CX + 64, 600, 110 * k, 70 * k, "us", t, 0.7)
        union_jack(g, 130, 450, 130 * k, 80 * k)
        g.text("แคนาดา", 195, 580, 50, "kanit", sc=k)
        g.text("สหรัฐฯ", 230, by + 80, 50, "kanit", NAVY, sc=k)
    if t > L[5] - 0.2:   # ขับรถจากติ่งแผ่นดิน ข้ามแคนาดา ลงไปฝั่งสหรัฐฯ
        p = seg(t, L[5], L[6] + 1.5)
        path = [(CX + 40, 800), (300, 800), (300, by + 120), (CX + 80, by + 120)]
        q = p * 3
        i = min(int(q), 2)
        (ax, ay), (bx, bb) = path[i], path[i + 1]
        f = q - i
        g.line(path, 6, GREY, amp=0)
        car(g, lerp(ax, bx, f), lerp(ay, bb, f) + 30, 0.6, t, flip=bx < ax)
        g.text("ผ่านแคนาดา", 330, 740, 44, "kanit", RED, sc=pop(t, L[5] + 0.6))
    if t > L[6] - 0.2:
        school(g, CX + 230, by + 200, 0.55 * pop(t, L[6] - 0.2))
        school(g, CX + 400, by + 200, 0.55 * pop(t, L[6]), "โรงพยาบาล", True)


# ------------------------------------------------------------------ 6. peace
def s_peace(g, t, L, d):
    if t < L[3] - 0.2:
        glow = seg(t, L[1] - 0.2, L[1] + 0.6)
        na_map(g, t, border=1.0, wavy=0.0, angle=1.0, glow=glow)
        if t > L[1]:
            for i in range(8):
                g.sparkle(160 + i * 105, LINE_Y - 50 + 30 * math.sin(t * 3 + i), 22 * pop(t, L[1] + i * 0.05))
        if t > L[2] - 0.4:   # ไฟแค้นดับ
            f = 1 - seg(t, L[2], L[2] + 1.6)
            for i in range(5):
                h = (60 + 20 * math.sin(t * 9 + i)) * f
                with g.at(220 + i * 160, LINE_Y - 10):
                    if h > 2:
                        g.c.move_to(0, -h)
                        g.c.curve_to(h * 0.5, -h * 0.3, h * 0.4, h * 0.3, 0, h * 0.35)
                        g.c.curve_to(-h * 0.4, h * 0.3, -h * 0.5, -h * 0.3, 0, -h)
                        g.fs((0.95, 0.55, 0.2, 0.9), 4)
        return
    if t < L[6] - 0.2:
        g.ground(GROUND, WHITE)
        g.line([(CX, 380), (CX, GROUND + 60)], 10, NAVY, amp=0)
        badge(g, t, L[3], CX, 330, "พรมแดนที่ยาวที่สุดในโลก", GOLD2, 50)
        for i, side in enumerate((-1, 1)):   # บ้านสองฝั่ง ไม่มีป้อม
            with g.at(CX + side * 260, GROUND, pop(t, L[4] - 0.2 + i * 0.2)):
                g.rrect(-100, -140, 200, 140, 8, WHITE, 7)
                g.poly([(-120, -140), (0, -220), (120, -140)], RED if i else BLUE, 7)
        if t > L[4] + 0.4:
            g.text("ไม่มีป้อมปราการ", CX, 700, 60, "kanit", sc=pop(t, L[4] + 0.6))
        if t > L[5] - 0.2:   # ควันปืนกลายเป็นดอกไม้
            for i in range(10):
                x = 120 + i * 95
                k = pop(t, L[5] + i * 0.08)
                g.circle(x, GROUND - 10, 18 * k, [RED, GOLD2, hexc("#e58fb0")][i % 3], 4)
                g.line([(x, GROUND - 10 + 18 * k), (x, GROUND + 40)], 4, hexc("#5f7f55"))
        return
    g.ground(GROUND, WHITE)
    shake = e_back(seg(t, L[6] - 0.2, L[6] + 0.4))
    g.sam(lerp(200, 400, shake), GROUND + 80, 1.05, "laugh", arm=shake)
    john_bull(g, lerp(880, 680, shake), GROUND + 80, 1.05, "laugh", arm=shake)
    badge(g, t, L[6], CX, 420, "สันติภาพกว่า 200 ปี", GOLD2, 60)
    if t > L[6] + 0.3:
        confetti(g, t, 40, t0=L[6] + 0.3)
    if t > L[7] - 0.2:   # หยดหมึกหยดเดียว
        k = e_in(seg(t, L[7] - 0.2, L[7] + 0.6))
        with g.at(CX, lerp(520, 760, k)):
            g.c.move_to(0, -40)
            g.c.curve_to(26, -6, 24, 30, 0, 34)
            g.c.curve_to(-24, 30, -26, -6, 0, -40)
            g.fs(NAVY, 5)


# ------------------------------------------------------------------ 7. lesson
def s_lesson(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:
        k = pop(t, 0.2)
        with g.at(CX, 700, k):
            g.circle(0, 0, 120, GOLD2, 9)
            g.rrect(-50, 110, 100, 70, 14, LGREY, 7)
        return
    # ปืนใหญ่ vs โต๊ะเจรจา
    can = pop(t, L[1] - 0.2)
    with g.at(270, GROUND, can):
        g.rrect(-140, -120, 260, 70, 30, GREY, 7)
        g.circle(-40, -30, 50, BROWN2, 7)
        if t > L[2]:
            g.line([(-180, -200), (180, 60)], 18, RED, amp=0)
            g.line([(180, -200), (-180, 60)], 18, RED, amp=0)
    with g.at(800, GROUND, pop(t, L[2] - 0.2)):
        g.rrect(-180, -180, 360, 40, 10, BROWN2, 7)
        g.line([(-150, -140), (-150, 0)], 12, BROWN)
        g.line([(150, -140), (150, 0)], 12, BROWN)
    if t > L[3] - 0.2:   # ถอยคนละก้าว
        step = e_out(seg(t, L[3], L[3] + 1.2))
        gallatin(g, 800 - 120 - 60 * step, GROUND + 80, 0.75, "happy")
        robinson(g, 800 + 120 + 60 * step, GROUND + 80, 0.75, "happy")
        g.text("← ถอยคนละก้าว →", 800, 760, 50, "kanit", RED, sc=pop(t, L[3] + 0.6))


# ------------------------------------------------------------------ 8. outro
def s_outro(g, t, L, d):
    g.ground(GROUND, WHITE)
    tilt = 8 * math.sin(t * 1.3)
    with g.at(CX, 780, pop(t, 0.2), tilt):
        g.rrect(-12, 0, 24, 380, 6, BROWN2, 6)
        g.line([(-300, 0), (300, 0)], 12, BROWN)
        for i, (lbl, col) in enumerate((("เจรจา", GOLD2), ("กำลังทหาร", LGREY))):
            x = -300 if i == 0 else 300
            g.line([(x, 0), (x - 70, 150), (x + 70, 150), (x, 0)], 4, GREY, amp=0)
            g.rrect(x - 120, 150, 240, 70, 30, col, 7)
            g.text(lbl, x, 185, 46, "kanit")
    g.text("?", CX, 560, 160, "kanit", RED, sc=pop(t, L[2]) * (1 - seg(t, L[4] - 0.4, L[4] - 0.2)))
    if t > L[4] - 0.2:
        k = pop(t, L[4] - 0.2)
        with g.at(CX, 470, k, -3 + 3 * math.sin(t * 3)):
            g.bubble(0, 0, 560, 240, WHITE, (-1, 1))
            for i in range(3):
                g.circle(-130 + i * 130, -10 + 12 * math.sin(t * 6 + i), 30, [RED, GOLD, BLUE][i], 6)


SCENES = {
    "hook": s_hook, "tension": s_tension, "frontier": s_frontier, "treaty": s_treaty, "weird": s_weird,
    "peace": s_peace, "lesson": s_lesson, "outro": s_outro,
}
NO_IRIS = set()
