"""ฉากตอน: การบุกของกองพลทหารม้าเบา ยุทธการบาลาคลาวา (25 ต.ค. 1854) — ไม่แสดงความรุนแรงตรง ๆ"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from chars import (BOSQUET, CARDIGAN, CHERRY, LUCAN, RAGLAN, RU_GREEN, TROOPERS, blast, bugle,  # noqa: E402
                   busby_hat, cannon, cross_grave, hills, horse, order_paper, smoke, telescope, valley_map)
from gfx import GOLD, GOLD2, GREY, INK, NAVY, RED, W, WHITE, e_io, e_out, hexc, lerp, pop, seg  # noqa: E402
from people import person  # noqa: E402

CX = W / 2
GROUND = 1270
GOLDTXT = hexc("#b37a12")
GREEN = hexc("#3c8d4f")
DARK = hexc("#4a3a3a")
SMOKE = (0.62, 0.6, 0.57)

CAMERA = {"hook": "push_in", "order": "pan_right", "valley": "tilt_up", "duty": "push_in", "charge": "pan_left",
          "cost": "pull_out", "lesson": "dutch", "outro": "pan_right"}
TRANSITIONS = {"order": "fade", "valley": "whip", "duty": "iris", "charge": "zoom", "cost": "fade", "lesson": "whip",
               "outro": "fade"}


def ap(t, a, dur=0.38):
    return pop(t, a - 0.2, dur)


def title(g, t, a, txt, col=INK, size=84, y=380):
    g.label(txt, CX, y, size, color=col, sc=ap(t, a), rot=-3)


def cavalry(g, t, x0, n=4, gap=260, sc=0.55, y=GROUND, speed=1.0, sabre=1.0, empty=(), seed=0):
    """แถวทหารม้าวิ่งไปทางขวา"""
    for i in range(n):
        x = x0 + i * gap + 30 * math.sin(t * 2 + i)
        horse(g, x, y - (i % 2) * 40, sc, t * speed, 1.0, None if i in empty else TROOPERS[i % 3], sabre,
              seed=i * 1.7 + seed)


def banner(g, x, y, w, col, txt, t, k=1.0):
    if k < 0.02:
        return
    with g.at(x, y, k):
        g.line([(0, 0), (0, 380)], 7, hexc("#8a8a8a"), amp=0)
        pts = [(0, 0)] + [(w * u / 10, 8 * math.sin(t * 5 + u)) for u in range(1, 11)] + \
              [(w * u / 10, 150 + 8 * math.sin(t * 5 + u)) for u in range(10, -1, -1)]
        g.poly(pts, col, 6, amp=0)
        g.label(txt, w / 2, 75, 44, color=col)


# ------------------------------------------------------------------ 1. hook
def s_hook(g, t, L, d):
    g.ground(GROUND, WHITE)
    hills(g, GROUND, t)
    if t < L[1] - 0.2:
        cavalry(g, t, -300 + 120 * t, 3, 300, 0.5)
        g.label("วันนี้ในอดีต", CX, 380, 104, sc=lerp(2.0, 1, e_out(seg(t, 0.1, 0.4))) if t > 0.1 else 0, rot=-3)
        g.label("25 ตุลาคม 1854", CX, 520, 84, color=GOLDTXT, sc=pop(t, 0.6))
        return
    if t < L[2] - 0.2:   # 600 นายพุ่งเข้าหุบเหวแห่งความตาย
        u = seg(t, L[1], L[2])
        cavalry(g, t, lerp(-200, 120, u), 4, 230, 0.5)
        for i in range(3):
            smoke(g, 900 + 60 * i, 900, 70, t, 4, SMOKE, 0.6, i)
        title(g, t, L[1], "\"หุบเหวแห่งความตาย\"", RED, 90)
        g.label("ทหารม้า 600+ นาย", CX, 520, 66, color=NAVY, sc=ap(t, L[1] + 0.4))
        return
    order_paper(g, 720, 820, 1.2 * ap(t, L[2]) + 0.01, 6 * math.sin(t * 2), blur=0.0 if t < L[3] - 0.2 else 1.0)
    person(g, 260, GROUND, RAGLAN, 0.8, mood="firm" if t < L[3] - 0.2 else "smug", pose="point", turn=0.4, seed=1)
    if t < L[3] - 0.2:
        title(g, t, L[2], "คำสั่งที่ได้รับ...", INK, 90)
    else:
        with g.at(720, 1050, ap(t, L[3]), -12):
            g.rrect(-200, -60, 400, 120, 20, WHITE, 8, stroke=RED)
            g.label("ผิดพลาด!", 0, 0, 72, color=RED)
        title(g, t, L[3], "ความผิดพลาดของเจ้านาย!", RED, 80)


# ------------------------------------------------------------------ 2. order
def s_order(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[3] - 0.2:   # 1854 บาลาคลาวา ไครเมีย / อังกฤษ+ฝรั่งเศส vs รัสเซีย
        hills(g, GROUND, t)
        if t < L[2] - 0.2:
            g.calendar(CX, 820, 1.0 * pop(t, 0.2), "25", "พุธ", "ต.ค. 1854") if t < L[1] - 0.2 else None
            if t < L[1] - 0.2:
                title(g, t, L[0], "25 ตุลาคม 1854", GOLDTXT, 92)
            else:
                g.label("บาลาคลาวา", CX, 760, 110, color=NAVY, sc=ap(t, L[1]), rot=-2)
                g.label("สงครามไครเมีย", CX, 900, 70, color=DARK, sc=ap(t, L[1] + 0.3))
                title(g, t, L[1], "ทุ่งบาลาคลาวา", INK, 84)
            return
        banner(g, 90, 600, 340, NAVY, "อังกฤษ + ฝรั่งเศส", t, ap(t, L[2]))
        banner(g, 640, 600, 300, RU_GREEN, "รัสเซีย", t, ap(t, L[2] + 0.4))
        g.label("VS", CX, 680, 90, color=RED, sc=ap(t, L[2] + 0.6))
        title(g, t, L[2], "ศึกขับเคี่ยวสุดดุเดือด", RED, 84)
        return
    if t < L[6] - 0.2:   # แร็กแลนบนยอดเขา ออกคำสั่งคลุมเครือ
        c = g.c
        from people import _shade, _smooth_path
        _smooth_path(c, [(-300, GROUND), (-200, 1120), (200, 1060), (520, 1100), (640, GROUND)])
        _shade(c, hexc("#b9b98a"), 6, 0.2)
        person(g, 260, 1080, RAGLAN, 0.58, mood="firm", pose="point" if t > L[5] - 0.2 else "spy", turn=0.4, seed=1)
        if t < L[4] - 0.2:
            title(g, t, L[3], "ความผิดพลาดครั้งประวัติศาสตร์", RED, 74)
            g.label("?", 760, 800, 220, color=RED, sc=ap(t, L[3] + 0.3), rot=10 * math.sin(t * 3))
        elif t < L[5] - 0.2:
            telescope(g, 360, 640, 0.8 * ap(t, L[4]) + 0.01, -10)
            g.name_tag(t, L[4] + 0.1, 640, 1140, "ลอร์ดแร็กแลน", "ผู้บัญชาการสูงสุดกองทัพอังกฤษ")
            title(g, t, L[4], "ผู้บัญชาการยืนมองจากยอดเขา", NAVY, 74)
        else:
            order_paper(g, 760, 760, 1.0 * ap(t, L[5]) + 0.01, 8, blur=e_io(seg(t, L[5] + 0.3, L[5] + 1.2)))
            title(g, t, L[5], "คำสั่งที่คลุมเครือ", RED, 88)
        return
    if t < L[7] - 0.2:   # ทหารม้าเบาเคลื่อนพลไปสกัด
        hills(g, GROUND, t)
        horse(g, lerp(150, 700, seg(t, L[6], L[7])), GROUND, 0.7, t, 1.0, TROOPERS[0], 0.0)
        order_paper(g, 860, 620, 0.5, 10 + 6 * math.sin(t * 3))
        title(g, t, L[6], "สั่งทหารม้าเบาไปสกัดกั้น!", NAVY, 80)
        return
    hills(g, GROUND, t)   # รัสเซียลากปืนใหญ่หนี
    u = seg(t, L[7], L[7] + 2.5)
    cannon(g, lerp(500, 820, u), GROUND, 0.9, t, flip=True)
    horse(g, lerp(820, 1140, u), GROUND, 0.6, t, 0.6, None, col=hexc("#5a4a3a"))
    g.line([(lerp(560, 880, u), GROUND - 60), (lerp(700, 1020, u), GROUND - 230)], 6, INK, amp=0)
    title(g, t, L[7], "ไม่ให้รัสเซียลากปืนใหญ่หนี", RU_GREEN, 76)


# ------------------------------------------------------------------ 3. valley
def s_valley(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # คำสั่งถึงก้นหุบ แต่มองไม่เห็นปืน
        hills(g, GROUND, t)
        for i in range(3):
            person(g, 160 + i * 180, GROUND, TROOPERS[i], 0.55, mood="worry", pose="salute" if i == 1 else "down",
                   turn=0.4, seed=20 + i)
        if t < L[1] - 0.2:
            order_paper(g, 800, 760, 0.8 * ap(t, L[0]) + 0.01, -6)
            title(g, t, L[0], "คำสั่งถึงก้นหุบเขา...", INK, 84)
        else:
            g.label("?", 800, 760, 200, color=RED, sc=ap(t, L[1]), rot=10 * math.sin(t * 3))
            title(g, t, L[1], "มองไม่เห็นปืนที่ถอยหนี!", RED, 82)
        return
    fire = 0.0 if t < L[4] - 0.2 else 1.0
    valley_map(g, CX, 820, 0.85, t, fire=fire, right=1.0 if t < L[3] else 0.0)
    if t < L[3] - 0.2:
        with g.at(CX, 400, ap(t, L[2]), -2):
            g.rrect(-300, -60, 600, 120, 30, WHITE, 7, stroke=RU_GREEN)
            g.label("รังปืนใหญ่หลักของรัสเซีย", 0, 0, 52, color=RU_GREEN)
        g.circle(CX, 410, 100 * ap(t, L[2] + 0.4) + 1, (0, 0, 0, 0), 0)
    elif t < L[4] - 0.2:
        title(g, t, L[3], "ตั้งตระหง่านสุดปลายหุบเขา", RU_GREEN, 74, y=300)
    elif t < L[5] - 0.2:
        title(g, t, L[4], "หน้า · ซ้าย · ขวา", RED, 96, y=300)
    else:
        for i in range(9):   # ลูกกรง
            g.line([(CX - 360 + i * 90, 300), (CX - 360 + i * 90, 1300)], 12, (0.15, 0.15, 0.15, 0.7 * ap(t, L[5])),
                   amp=0)
        title(g, t, L[5], "กรงขังมรณะ!", RED, 110, y=300)


# ------------------------------------------------------------------ 4. duty
def s_duty(g, t, L, d):
    g.ground(GROUND, WHITE)
    hills(g, GROUND, t)
    if t < L[2] - 0.2:   # ลูคัน + คาร์ดิแกน รู้ว่าฆ่าตัวตาย
        person(g, 270, GROUND, LUCAN, 0.78, mood="worry" if t > L[1] - 0.2 else "firm", pose="think", turn=0.3,
               seed=30)
        person(g, 820, GROUND, CARDIGAN, 0.78, mood="worry" if t > L[1] - 0.2 else "firm", pose="cross", turn=-0.3,
               seed=31)
        g.name_tag(t, L[0] + 0.1, 270, 1140, "ลอร์ดลูคัน", "ผู้บัญชาการกองพลทหารม้า")
        g.name_tag(t, L[0] + 0.7, 820, 1140, "ลอร์ดคาร์ดิแกน", "ผู้นำกองพลทหารม้าเบา")
        if t < L[1] - 0.2:
            title(g, t, L[0], "ผู้คุมกองพลทหารม้า", NAVY, 84)
        else:
            for x in (270, 820):
                g.sweat(x + 40, 560 + 10 * math.sin(t * 6), 1.4)
            title(g, t, L[1], "ภารกิจฆ่าตัวตายชัด ๆ!", RED, 86)
        return
    for i in range(3):   # วินัยทหาร: ห้ามถาม ห้ามค้าน ต้องปฏิบัติตาม
        person(g, 200 + i * 340, GROUND, [LUCAN, CARDIGAN, TROOPERS[0]][i], 0.6, mood="firm",
               pose="salute" if t > L[4] - 0.2 or i == 2 else "down", turn=0.2, seed=40 + i)
    if t < L[3] - 0.2:
        title(g, t, L[2], "กฎเหล็กของวินัยทหาร", INK, 86)
    elif t < L[4] - 0.2:
        for i, txt in enumerate(("ห้ามถาม", "ห้ามค้าน")):
            with g.at(300 + i * 480, 500, ap(t, L[3] + 0.4 * i), -4 + 8 * i):
                g.rrect(-180, -60, 360, 120, 30, WHITE, 7, stroke=RED)
                g.label(txt, 0, 0, 60, color=RED)
        title(g, t, L[3], "ไม่มีสิทธิ์ถาม ไม่มีสิทธิ์ค้าน", RED, 72, y=360)
    else:
        title(g, t, L[4], "มีเพียงหน้าที่ต้องทำตาม!", NAVY, 82)


# ------------------------------------------------------------------ 5. charge
def s_charge(g, t, L, d):
    g.ground(GROUND, WHITE)
    hills(g, GROUND, t)
    if t < L[1] - 0.2:   # เสียงแตร
        bugle(g, CX, 800, 1.6 * ap(t, L[0]) + 0.01, -10, t, 1.0)
        title(g, t, L[0], "เสียงแตรศึกดังลั่น!", RED, 92)
        return
    if t < L[3] - 0.2:   # 670 นาย พุ่งทะยาน
        u = seg(t, L[1], L[3])
        cavalry(g, t, lerp(-260, 60, u), 4, 250, 0.55)
        cavalry(g, t, lerp(-400, -80, u), 4, 250, 0.42, y=GROUND - 160, seed=3)
        if t < L[2] - 0.2:
            title(g, t, L[1], "ทหารม้าเบา 670 นาย", NAVY, 88)
        else:
            title(g, t, L[2], "กล้าหาญสุดขีด!", GOLDTXT, 96)
        return
    if t < L[4] - 0.2:   # ปืนใหญ่ระดมยิงจากสามทิศ
        valley_map(g, CX, 820, 0.85, t, charge=e_io(seg(t, L[3], L[4])) * 0.5, fire=1.0)
        title(g, t, L[3], "ระดมยิงจากสามทิศทาง!", RED, 80, y=300)
        return
    # ห่ากระสุน / ควัน / ม้าไร้คนขี่ / ผู้รอดฝ่าไปต่อ
    dark = 0.25 if t < L[7] - 0.2 else 0.15
    c = g.c
    c.rectangle(-500, 140, 2100, 1130)
    c.set_source_rgba(0.3, 0.27, 0.25, dark)
    c.fill()
    if t < L[6] - 0.2:
        cavalry(g, t, 80 + 40 * math.sin(t), 3, 300, 0.55, sabre=0.6)
        for i in range(6):
            blast(g, 120 + i * 170, 700 + 120 * math.sin(i * 2.1), 140, (t * 1.3 + i * 0.29) % 1)
        for i in range(5):
            smoke(g, 60 + i * 230, 1000, 110, t, 5, SMOKE, 0.75, i * 0.3)
        if t < L[5] - 0.2:
            title(g, t, L[4], "ห่ากระสุนถล่มทั้งคนและม้า", RED, 76)
        else:
            title(g, t, L[5], "หุบเขาแห่งความโกลาหล", DARK, 80)
        return
    if t < L[7] - 0.2:   # ม้าไร้คนขี่ + หมวกตกพื้น
        u = seg(t, L[6], L[7])
        horse(g, lerp(100, 600, u), GROUND, 0.6, t, 1.0, None)
        horse(g, lerp(-200, 300, u), GROUND - 120, 0.45, t, 1.0, None, seed=2, col=hexc("#5a4a3a"))
        busby_hat(g, 820, GROUND, 0.8, -25)
        busby_hat(g, 640, GROUND, 0.6, 30)
        for i in range(3):
            smoke(g, 200 + i * 330, 1050, 90, t, 4, SMOKE, 0.6, i)
        title(g, t, L[6], "ตกม้าตัวแล้วตัวเล่า...", DARK, 84)
        return
    u = seg(t, L[7], L[7] + 3)
    cavalry(g, t, lerp(0, 200, u), 2, 380, 0.6, sabre=1.0)
    for i in range(4):
        smoke(g, 100 + i * 280, 1050, 100, t, 4, SMOKE, 0.65, i * 0.4)
        blast(g, 150 + i * 260, 650, 120, (t * 1.1 + i * 0.31) % 1)
    title(g, t, L[7], "ฝ่าดงกระสุนต่อไป!", RED, 90)


# ------------------------------------------------------------------ 6. cost
def s_cost(g, t, L, d):
    g.ground(GROUND, WHITE)
    hills(g, GROUND, t)
    if t < L[1] - 0.2:   # บุกถึงรังปืน
        for i in range(3):
            cannon(g, 500 + i * 230, GROUND, 0.7, t, fire=0.0, flip=True)
        horse(g, lerp(100, 300, seg(t, 0, L[1])), GROUND, 0.6, t, 1.0, TROOPERS[0], 1.0)
        for i in range(3):
            smoke(g, 500 + i * 230, 1000, 100, t, 4, SMOKE, 0.7, i)
        title(g, t, L[0], "บุกทะลวงถึงรังปืนใหญ่!", NAVY, 82)
        return
    if t < L[3] - 0.2:   # หายนะ / รอดกลับไม่ถึงครึ่ง
        if t < L[2] - 0.2:
            for i in range(5):
                cross_grave(g, 180 + i * 180, GROUND, 1.0 * pop(t, L[1] - 0.2 + 0.15 * i))
            busby_hat(g, CX, GROUND - 200, 0.9, -15)
            title(g, t, L[1], "หายนะที่ประเมินค่าไม่ได้", DARK, 80)
        else:
            for i in range(10):
                alive = i < 4
                x = 150 + (i % 5) * 190
                y = 780 + (i // 5) * 260
                k = pop(t, L[2] - 0.2 + 0.05 * i)
                with g.at(x, y, k):
                    g.circle(0, -60, 34, NAVY if alive else (0.8, 0.8, 0.8, 1), 5)
                    g.rrect(-44, -24, 88, 100, 30, NAVY if alive else (0.8, 0.8, 0.8, 1), 5)
            g.label("รอดกลับมาไม่ถึงครึ่ง", CX, 1220, 64, color=RED, sc=ap(t, L[2] + 0.5))
            title(g, t, L[2], "เมื่อถึงเวลาถอยทัพ...", INK, 84)
        return
    person(g, 260, GROUND, BOSQUET, 0.82, mood="shock" if t > L[4] - 0.2 else "firm",
           pose="spy" if t < L[4] - 0.2 else "shrug", turn=0.4, seed=50, talk=t > L[4] - 0.2)
    if t < L[4] - 0.2:   # นายพลฝรั่งเศสเฝ้ามอง
        telescope(g, 380, 520, 0.8, -10)
        g.name_tag(t, L[3] + 0.1, 680, 1140, "นายพลบอสเกต์", "นักสังเกตการณ์ชาวฝรั่งเศส")
        title(g, t, L[3], "นายพลฝรั่งเศสถึงกับอุทาน...", NAVY, 76)
        return
    with g.at(720, 700, ap(t, L[4])):   # คำพูดอมตะ
        g.bubble(0, 0, 520, 420, WHITE, tail=(-1, 1))
        if t < L[5] - 0.2:
            g.label("งดงาม", 0, -80, 76, color=GOLDTXT)
            g.label("และกล้าหาญ...", 0, 40, 66, color=GOLDTXT)
        else:
            g.label("ไม่ใช่สงคราม", 0, -80, 66, color=INK)
            g.label("คือความบ้าคลั่ง!", 0, 40, 66, color=RED)
    title(g, t, L[4], "\"C'est magnifique...\"", GOLDTXT, 76, y=330)


# ------------------------------------------------------------------ 7. lesson
def s_lesson(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:
        busby_hat(g, CX, GROUND - 20, 1.6 * ap(t, L[0]) + 0.01, -10)
        for i in range(3):
            cross_grave(g, 180 + i * 360, GROUND, 0.8)
        if t < L[1] - 0.2:
            title(g, t, L[0], "วีรกรรมอันสูญเปล่า", DARK, 90)
        else:
            title(g, t, L[1], "บทเรียนราคาแพงที่สุด", RED, 86)
        return
    c = g.c   # ผู้นำบนยอดเขา vs ผู้น้อยในหุบ
    from people import _shade, _smooth_path
    _smooth_path(c, [(560, GROUND), (640, 1000), (880, 900), (1300, 940), (1400, GROUND)])
    _shade(c, hexc("#b9b98a"), 6, 0.25)
    person(g, 840, 920, RAGLAN, 0.5, mood="smug", pose="point", turn=-0.4, seed=1)
    for i in range(3):
        person(g, 120 + i * 150, GROUND, TROOPERS[i], 0.55, mood="firm", pose="salute", turn=0.4, seed=60 + i)
    if t < L[3] - 0.2:
        title(g, t, L[2], "ความกล้าหาญของผู้น้อย", NAVY, 84)
    else:
        title(g, t, L[3], "ถูกสังเวยให้ความผิดพลาดของผู้นำ", RED, 66)
        g.label("หยิ่งผยอง", 600, 760, 56, color=RED, sc=ap(t, L[3] + 0.5), rot=6)


# ------------------------------------------------------------------ 8. outro
def s_outro(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[3] - 0.2:   # รู้สึกอย่างไร / คำสั่งผิดพลาด / หายนะ
        person(g, 260, GROUND, TROOPERS[1], 0.72, mood="worry" if t > L[1] - 0.2 else "neutral",
               pose="think", turn=0.4, seed=70)
        if t < L[1] - 0.2:
            with g.at(760, 640, ap(t, L[0])):
                g.bubble(0, 0, 360, 240, WHITE, tail=(-1, 1))
                g.label("?", 0, 0, 140, color=RED)
            title(g, t, L[0], "ทุกคนรู้สึกอย่างไร?", INK, 86)
        else:
            order_paper(g, 760, 760, 1.0, 8 + 4 * math.sin(t * 2), blur=0.0)
            if t > L[2] - 0.2:
                with g.at(760, 980, ap(t, L[2]), -12):
                    g.rrect(-180, -60, 360, 120, 20, WHITE, 8, stroke=RED)
                    g.label("หายนะ!", 0, 0, 72, color=RED)
            title(g, t, L[1], "ถ้าคำสั่งเบื้องบนผิดพลาด...", RED, 78)
        return
    if t < L[5] - 0.2:   # ทำตามหน้าที่ หรือ ปฏิเสธ
        person(g, 260, GROUND, TROOPERS[0], 0.62, mood="firm", pose="salute", turn=0.3, seed=71)
        person(g, 820, GROUND, TROOPERS[2], 0.62, mood="firm", pose="stop", turn=-0.3, seed=72)
        with g.at(260, 490, ap(t, L[3]), -4):
            g.rrect(-200, -60, 400, 120, 30, WHITE, 7, stroke=NAVY)
            g.label("ทำตามหน้าที่", 0, 0, 52, color=NAVY)
        with g.at(820, 490, ap(t, L[4]), 4):
            g.rrect(-200, -60, 400, 120, 30, WHITE, 7, stroke=RED)
            g.label("กล้าปฏิเสธ", 0, 0, 52, color=RED)
        g.label("หรือ", CX, 500, 60, sc=ap(t, L[4] + 0.2))
        title(g, t, L[3], "คุณจะเลือกแบบไหน?", INK, 88, y=360)
        return
    with g.at(CX + 170, 640, ap(t, L[5])):   # ชวนคอมเมนต์
        g.bubble(0, 0, 460, 220, WHITE, tail=(-1, 1))
        for i in range(3):
            g.circle(-110 + i * 110, 0, 24 + 6 * math.sin(t * 6 - i), INK, 0)
    person(g, 250, GROUND, TROOPERS[1], 0.68, mood="smile", pose="wave", turn=0.3, seed=73, talk=True)
    title(g, t, L[5], "คอมเมนต์แลกเปลี่ยนกันได้เลย!", RED, 64)


SCENES = {
    "hook": s_hook, "order": s_order, "valley": s_valley, "duty": s_duty, "charge": s_charge, "cost": s_cost,
    "lesson": s_lesson, "outro": s_outro,
}
NO_IRIS = set()
