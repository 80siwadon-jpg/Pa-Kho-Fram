"""ฉากตอน: พิธีเปิดอนุสาวรีย์เทพีเสรีภาพ (28 ต.ค. 1886)"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from chars import (CLEVELAND, COPPER, DONORS, EIFFEL, IMMIGRANTS, PULITZER, VERDIGRIS, chains, cloud, coin,  # noqa: E402
                   crate, eiffel_tower, fog, iron_frame, jar, liner, newspaper, pedestal, rain, sea, skyline,
                   statue, statue_part, tricolor)
from gfx import GOLD, GOLD2, GREY, INK, NAVY, RED, W, WHITE, e_io, e_out, hexc, lerp, pop, seg  # noqa: E402
from people import person  # noqa: E402
from photos import photo  # noqa: E402

CX = W / 2
GROUND = 1270
GOLDTXT = hexc("#b37a12")
GREEN = hexc("#3a8a72")
COPTXT = hexc("#b0582a")
FR_BLUE = hexc("#2b4f9a")

CAMERA = {"hook": "tilt_up", "open": "pan_right", "money": "dutch", "copper": "push_in", "hope": "pan_left",
          "lesson": "pull_out", "outro": "pan_right"}
TRANSITIONS = {"open": "zoom", "money": "whip", "copper": "iris", "hope": "zoom", "lesson": "fade", "outro": "whip"}


def ap(t, a, dur=0.38):
    return pop(t, a - 0.2, dur)


def title(g, t, a, txt, col=INK, size=84, y=380):
    g.label(txt, CX, y, size, color=col, sc=ap(t, a), rot=-3)


def mixc(a, b, u):
    return tuple(lerp(a[i], b[i], u) for i in range(3)) + (1,)


def monument(g, x, y, sc, col=VERDIGRIS, t=0.0, k=1.0, glow=0.0):
    """ฐาน + เทพี (y = พื้น)"""
    pedestal(g, x, y, sc, k)
    if k >= 1:
        statue(g, x, y - 520 * sc, sc * 0.85, col, t, glow=glow)


# ------------------------------------------------------------------ 1. hook
def s_hook(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # กล่องไม้กว่า 200 ลัง
        n = 1 if t < L[1] - 0.2 else int(lerp(1, 9, seg(t, L[1], L[2] - 0.4)))
        slots = [(CX, GROUND), (CX - 210, GROUND), (CX + 210, GROUND), (CX - 105, GROUND - 170),
                 (CX + 105, GROUND - 170), (CX - 315, GROUND - 170), (CX + 315, GROUND - 170), (CX, GROUND - 340),
                 (CX - 210, GROUND - 340)]
        for i in range(n):
            x, y = slots[i]
            crate(g, x, y, 1.0 * pop(t, (L[1] + 0.15 * i) if i else 0.2) + 0.01, 3 * math.sin(i * 2.1),
                  "FRAGILE" if i == 0 else "")
        if t < L[1] - 0.2:
            g.label("วันนี้ในอดีต", CX, 380, 104, sc=lerp(2.0, 1, e_out(seg(t, 0.1, 0.4))) if t > 0.1 else 0, rot=-3)
            g.label("28 ตุลาคม 1886", CX, 520, 84, color=GOLDTXT, sc=pop(t, 0.5))
        else:
            g.label(f"{int(lerp(1, 214, e_out(seg(t, L[1], L[2]))))} ลัง!", CX, 560, 96, color=RED, sc=ap(t, L[1] + 0.2))
            title(g, t, L[1], "กล่องไม้ยักษ์กว่า 200 ลัง", INK, 84)
        return
    if t < L[3] - 0.2:   # ข้ามมหาสมุทร → ประกอบร่าง
        sea(g, 1150, t)
        k = e_io(seg(t, L[2] + 1.6, L[3] - 0.4))
        if k < 0.05:
            liner(g, lerp(250, 560, seg(t, L[2] - 0.2, L[2] + 1.6)), 1130, 0.75, t)
        else:
            monument(g, CX, 1160, 0.5, COPPER, t, min(1, k * 2))
        title(g, t, L[2], "ข้ามมหาสมุทรมาประกอบร่าง!", NAVY, 82)
        return
    if not photo(g, "statue", CX, 860, 520, 760, -3, ap(t, L[3]), 1.0 + 0.03 * (t - L[3]),   # ภาพจริง
                 label="เทพีเสรีภาพ นิวยอร์ก"):
        monument(g, CX, GROUND, 0.7, VERDIGRIS, t)
    title(g, t, L[3], "ประตูแห่งความหวังของคนทั้งโลก!", GREEN, 78)


# ------------------------------------------------------------------ 2. open
def s_open(g, t, L, d):
    if t < L[1] - 0.2:   # 28 ต.ค. 1886
        g.ground(GROUND, WHITE)
        g.calendar(CX, 860, 1.25 * ap(t, L[0]) + 0.01, 28, "พฤหัสบดี", "ต.ค. 1886")
        title(g, t, L[0], "28 ตุลาคม 1886", GOLDTXT, 92)
        return
    if t < L[2] - 0.2:   # ฝนโปรย หมอกควันหนา
        sea(g, 1150, t)
        skyline(g, 1150, t)
        monument(g, CX, 1170, 0.5, COPPER, t)
        fog(g, t, ap(t, L[1] + 0.5))
        rain(g, t, ap(t, L[1]))
        title(g, t, L[1], "ฝนโปรย หมอกควันหนาทึบ", NAVY, 84)
        return
    if t < L[4] - 0.2:   # คลีฟแลนด์เป็นประธานพิธี
        g.ground(GROUND, WHITE)
        rain(g, t, 0.5, 20)
        monument(g, 720, GROUND, 0.5, COPPER, t)
        person(g, 300, GROUND, CLEVELAND, 0.82, mood="smile", pose="wave" if t > L[3] - 0.2 else "down", turn=0.3,
               seed=1, talk=t > L[3] - 0.2)
        g.name_tag(t, L[2] + 0.1, 330, 1040, "โกรเวอร์ คลีฟแลนด์", "ประธานาธิบดีสหรัฐฯ", side=1)
        if t < L[3] - 0.2:
            title(g, t, L[2], "ประธานาธิบดีคลีฟแลนด์", INK, 86)
        else:
            title(g, t, L[3], "เปิด \"อนุสาวรีย์เทพีเสรีภาพ\"", GREEN, 80)
        return
    g.ground(GROUND, WHITE)
    if t < L[5] - 0.2:   # ของขวัญจากฝรั่งเศส
        tricolor(g, 170, 520, 230, 150, t)
        with g.at(CX + 60, 940, ap(t, L[4] + 0.2), 3 * math.sin(t * 2)):
            g.rrect(-260, -200, 520, 400, 20, hexc("#f2ead6"), 7)
            g.rrect(-30, -200, 60, 400, 0, RED, 0)
            g.rrect(-260, -30, 520, 60, 0, RED, 0)
            g.circle(0, -210, 50, RED, 6)
            g.text("FRANCE ♥ USA", 0, 140, 40, "kanit", FR_BLUE)
        title(g, t, L[4], "ของขวัญมิตรภาพจากชาวฝรั่งเศส", FR_BLUE, 76)
        return
    if t < L[6] - 0.2:   # ครบรอบ 100 ปี
        g.flag(380, 620, 300, 190, "us", t)
        g.line([(380, 620), (380, GROUND)], 8, INK, amp=0)
        yr = int(lerp(1776, 1876, e_io(seg(t, L[5] + 0.3, L[5] + 2.2))))
        with g.at(720, 960, ap(t, L[5] + 0.2), 4):
            g.rrect(-190, -110, 380, 220, 30, WHITE, 8, stroke=NAVY)
            g.text(str(yr), 0, -20, 96, "kanit", NAVY)
            g.text("100 ปี", 0, 66, 44, "kanitsb", RED)
        title(g, t, L[5], "ฉลอง 100 ปีอิสรภาพสหรัฐฯ", NAVY, 80)
        return
    chains(g, CX, 860, 1.6, e_io(seg(t, L[6], L[6] + 0.8)))   # สิ้นสุดระบอบทาส
    for i in range(4):
        g.sparkle(CX + 300 * math.cos(i * 1.6 + t), 860 + 200 * math.sin(i * 1.6 + t), 26)
    title(g, t, L[6], "และการสิ้นสุดของระบอบทาส!", RED, 82)


# ------------------------------------------------------------------ 3. money
def s_money(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # เกือบล้มเหลว
        monument(g, CX, GROUND, 0.54, COPPER, t)
        if t > L[1] - 0.2:
            with g.at(CX, 800, ap(t, L[1]) * 1.0, -12):
                g.rrect(-260, -80, 520, 160, 16, (1, 1, 1, 0.85), 10, stroke=RED)
                g.label("เกือบล้มเหลว!", 0, 0, 72, color=RED)
        title(g, t, L[0] if t < L[1] - 0.2 else L[1], "เบื้องหลังการยืนตระหง่าน" if t < L[1] - 0.2 else
              "มหากาพย์ความล้มเหลว...", INK, 84)
        return
    if t < L[4] - 0.2:   # ฝรั่งเศสสร้างตัว / อเมริกาสร้างฐาน
        tricolor(g, 150, 520, 200, 130, t)
        statue(g, 300, GROUND, 0.56, COPPER, t)
        g.label("ตัวเทพี", 300, 1210, 50, color=FR_BLUE, sc=ap(t, L[2] + 0.4))
        k = ap(t, L[3])
        if k > 0.02:
            g.flag(690, 520, 200, 130, "us", t)
            with g.at(780, GROUND, k):
                g.c.set_dash([16, 12])
                g.rrect(-200, -500, 400, 500, 10, (1, 1, 1, 0), 6, stroke=GREY)
                g.c.set_dash([])
            g.label("ฐาน", 780, 1000, 64, color=NAVY, sc=k)
        if t < L[3] - 0.2:
            title(g, t, L[2], "ฝรั่งเศสสร้างตัวเทพี", FR_BLUE, 86)
        else:
            title(g, t, L[3], "อเมริกาสร้างฐาน", NAVY, 92)
        return
    if t < L[6] - 0.2:   # ถังแตก เกือบส่งคืน
        if t < L[5] - 0.2:
            jar(g, CX, GROUND - 40, 1.4, 0.0)
            g.label("$0", CX, 760, 120, color=RED, sc=ap(t, L[4] + 0.3), rot=-6)
            title(g, t, L[4], "อเมริกาถังแตก!", RED, 96)
        else:
            for i in range(3):
                crate(g, 300 + i * 220, GROUND, 0.9, 2 * math.sin(i), "")
            g.label("← ส่งคืน?", CX, 880, 90, color=RED, sc=ap(t, L[5] + 0.3), rot=-4)
            title(g, t, L[5], "เกือบต้องส่งรูปปั้นคืน!", RED, 86)
        return
    if t < L[7] - 0.2:   # โจเซฟ พูลิทเซอร์
        person(g, 280, GROUND, PULITZER, 0.82, mood="smile", pose="hold", turn=0.4, seed=2, talk=True)
        newspaper(g, 720, 860, 0.9 * ap(t, L[6] + 0.4) + 0.01, 5 + 2 * math.sin(t * 2))
        g.name_tag(t, L[6] + 0.1, 330, 1080, "โจเซฟ พูลิทเซอร์", "เจ้าของหนังสือพิมพ์ The World", side=1)
        title(g, t, L[6], "โจเซฟ พูลิทเซอร์", INK, 92)
        return
    if t < L[8] - 0.2:   # บริจาคคนละไม่กี่เซนต์
        u = seg(t, L[7], L[8])
        jar(g, CX, GROUND - 330, 1.0, u)
        for i, lk in enumerate(DONORS):
            person(g, 200 + i * 340, GROUND, lk, 0.55, mood="smile", pose="hold", turn=0.3 - 0.3 * i, seed=10 + i)
        for i in range(5):
            v = ((t - L[7]) * 1.2 + i / 5) % 1
            coin(g, lerp(200 + (i % 3) * 340, CX, v), lerp(800, GROUND - 560, v) - 160 * math.sin(math.pi * v), 26)
        g.label("กว่าแสนคน!", CX, 540, 76, color=GOLDTXT, sc=ap(t, L[7] + 0.6))
        title(g, t, L[7], "บริจาคคนละไม่กี่เซนต์", GOLDTXT, 84)
        return
    k = e_io(seg(t, L[8] - 0.2, L[8] + 1.3))   # สร้างฐานสำเร็จ
    pedestal(g, CX, GROUND, 1.1, k)
    if k >= 1:
        for i in range(4):
            g.sparkle(CX + 300 * math.cos(i * 1.6 + t), 800 + 160 * math.sin(i * 1.6 + t), 26)
    title(g, t, L[8], "ฐานมหึมาสร้างสำเร็จ!", GREEN, 88)


# ------------------------------------------------------------------ 4. copper
def s_copper(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:
        statue(g, CX, GROUND, 0.74, COPPER, t)
        g.label("!", 820, 640, 160, color=RED, sc=ap(t, L[0] + 0.2), rot=10)
        title(g, t, L[0], "สิ่งที่น่าทึ่งคือ...", INK, 92)
        return
    if t < L[3] - 0.2:   # โครงสร้างภายใน กุสตาฟ ไอเฟล
        with g.alpha(0.35):
            statue(g, 620, GROUND, 0.72, COPPER, t)
        iron_frame(g, 620, GROUND - 40, 0.72, e_io(seg(t, L[1], L[1] + 2.5)))
        person(g, 240, GROUND, EIFFEL, 0.78, mood="smile", pose="point", turn=0.4, seed=3)
        g.name_tag(t, L[1] + 0.2, 280, 1080, "กุสตาฟ ไอเฟล", "วิศวกรชาวฝรั่งเศส", side=1)
        if t < L[2] - 0.2:
            title(g, t, L[1], "โครงสร้างภายในโดยไอเฟล", INK, 84)
        else:
            eiffel_tower(g, 820, 820, 0.55 * ap(t, L[2]) + 0.01)
            title(g, t, L[2], "ผู้สร้างหอไอเฟล!", COPTXT, 92)
        return
    if t < L[4] - 0.2:   # ไม่ได้เป็นสีเขียว
        statue(g, CX, GROUND, 0.74, VERDIGRIS, t)
        k = seg(t, L[3] + 1.2, L[3] + 1.9)
        if k > 0:
            g.line([(CX - 300, 560), (CX - 300 + 600 * k, 560 + 640 * k)], 18, RED, amp=0)
        title(g, t, L[3], "ตอนเปิดตัว ไม่ใช่ \"สีเขียว\"!", RED, 82)
        return
    if t < L[5] - 0.2:   # ทองแดงสีส้มแวววาว
        statue(g, CX, GROUND, 0.74, COPPER, t)
        for i in range(5):
            g.sparkle(CX + 280 * math.cos(i * 1.3 + t * 1.5), 800 + 300 * math.sin(i * 1.3 + t * 1.5), 30)
        title(g, t, L[4], "ทองแดงสีส้มอมน้ำตาลแวววาว", COPTXT, 80)
        return
    u = e_io(seg(t, L[5] + 0.5, L[6] + 2.0))   # เปลี่ยนเป็นสีเขียว
    statue(g, 420, GROUND, 0.74, mixc(COPPER, VERDIGRIS, u), t)
    yr = int(lerp(1886, 1920, u))
    with g.at(800, 760, ap(t, L[5] + 0.3), 5):
        g.rrect(-150, -80, 300, 160, 24, WHITE, 7)
        g.text(str(yr), 0, 0, 80, "kanit", mixc(COPTXT, GREEN, u))
    if t < L[6] - 0.2:
        title(g, t, L[5], "กาลเวลา + ปฏิกิริยาเคมีกับอากาศ", INK, 76)
    else:
        title(g, t, L[6], "กลายเป็นสีเขียวคราบสนิมทองแดง", GREEN, 76)


# ------------------------------------------------------------------ 5. hope
def s_hope(g, t, L, d):
    if t < L[2] - 0.2:   # ผู้อพยพนั่งเรือ
        if t < L[1] - 0.2:
            sea(g, 1150, t)
            liner(g, lerp(330, 600, seg(t, L[0] - 0.2, L[1])), 1130, 0.85, t)
            title(g, t, L[0], "ผู้อพยพและผู้ลี้ภัยนับล้าน", NAVY, 80)
        else:
            g.ground(GROUND, WHITE)
            sea(g, 860, t, h=120)
            for i, lk in enumerate(IMMIGRANTS):
                person(g, 180 + i * 240, GROUND, lk, 0.62, mood="worry" if i % 2 else "sad", pose="down",
                       turn=0.3 - 0.2 * i, seed=20 + i)
            title(g, t, L[1], "ข้ามน้ำข้ามทะเลมาอย่างเหน็ดเหนื่อย", INK, 72)
        return
    if t < L[3] - 0.2:   # แตะขอบฟ้าโลกใหม่
        sea(g, 1100, t)
        monument(g, 760, 1110, 0.42, VERDIGRIS, t, glow=1.0)
        liner(g, 330, 1120, 0.6, t)
        title(g, t, L[2], "ขอบฟ้าของโลกใหม่", GREEN, 90)
        return
    if t < L[5] - 0.2:   # คบเพลิงมือขวา = แสงนำทาง
        g.ground(GROUND, WHITE)
        for i in range(10):
            a = math.radians(-90 + (i - 4.5) * 14 + 4 * math.sin(t))
            g.line([(CX, 640), (CX + 600 * math.cos(a), 640 + 600 * math.sin(a))], 10, (1, 0.85, 0.35, 0.35), amp=0)
        g.circle(CX, 640, 110 + 8 * math.sin(t * 4), (1, 0.85, 0.3, 0.3), 0)
        statue_part(g, CX, 760, 1.6, "torch", COPPER if False else VERDIGRIS, 3 * math.sin(t * 2))
        if t < L[4] - 0.2:
            title(g, t, L[3], "คบเพลิงในมือขวาของเทพี", GOLDTXT, 84)
        else:
            g.label("อิสรภาพ · ชีวิตใหม่", CX, 1120, 66, color=GREEN, sc=ap(t, L[4] + 0.3))
            title(g, t, L[4], "แสงนำทางสู่อิสรภาพ", GOLDTXT, 88)
        return
    g.ground(GROUND, WHITE)   # สัญลักษณ์อมตะแห่งความหวัง
    g.sunburst(CX, 760, 260, 560, 20, t * 6, 10, (1, 0.9, 0.5, 0.6))
    monument(g, CX, GROUND, 0.54, VERDIGRIS, t, glow=1.0)
    title(g, t, L[5], "สัญลักษณ์แห่งความหวังที่ไม่มีวันดับ", GREEN, 74)


# ------------------------------------------------------------------ 6. lesson
def s_lesson(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:
        if not photo(g, "statue", CX, 860, 480, 720, 3, ap(t, L[0]), 1.0 + 0.03 * t, label="เทพีเสรีภาพ"):
            monument(g, CX, GROUND, 0.62, VERDIGRIS, t)
        title(g, t, L[0], "เรื่องราวนี้ทำให้เห็นว่า...", INK, 86)
        return
    if t < L[2] - 0.2:   # ไม่ได้มาจากทองแดง/คอนกรีต
        with g.at(330, 860, ap(t, L[1]), -6):
            g.rrect(-150, -110, 300, 220, 10, COPPER, 7)
            g.text("ทองแดง", 0, 0, 50, "kanit", WHITE)
        with g.at(750, 880, ap(t, L[1] + 0.6), 5):
            g.rrect(-150, -110, 300, 220, 10, hexc("#c9c2b2"), 7)
            g.text("คอนกรีต", 0, 0, 50, "kanit", INK)
        k = seg(t, L[1] + 1.8, L[1] + 2.5)
        if k > 0:
            g.line([(160, 700), (160 + 760 * k, 700 + 360 * k)], 18, RED, amp=0)
        title(g, t, L[1], "เสรีภาพไม่ได้สร้างจากวัตถุ", INK, 82)
        return
    statue(g, CX, GROUND, 0.56, VERDIGRIS, t, glow=0.6)   # หยาดเหงื่อ + ความร่วมมือ
    looks = [IMMIGRANTS[0], DONORS[1], IMMIGRANTS[1], PULITZER]
    for i, (lk, x) in enumerate(zip(looks, (180, 330, 750, 900))):
        person(g, x, GROUND, lk, 0.5, mood="smile", pose="wave" if i in (1, 2) else "down",
               turn=0.3 if i < 2 else -0.3, seed=40 + i)
    title(g, t, L[2], "หยาดเหงื่อของผู้คนธรรมดา", GREEN, 82)


# ------------------------------------------------------------------ 7. outro
def s_outro(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:
        monument(g, 380, GROUND, 0.54, VERDIGRIS, t)
        with g.at(780, 700, ap(t, L[0] + 0.3)):
            g.bubble(0, 0, 300, 200, WHITE, tail=(-1, 1))
            g.label("?", 0, 0, 120, color=INK)
        title(g, t, L[0], "นึกถึงอะไรเป็นสิ่งแรก?", INK, 88)
        return
    if t < L[3] - 0.2:   # เสรีภาพ เมื่อก่อน vs ปัจจุบัน
        for i, (yr, col) in enumerate((("1886", COPPER), ("2026", VERDIGRIS))):
            x = 290 + i * 500
            statue(g, x, GROUND, 0.56, col, t)
            g.label(yr, x, 560, 70, color=COPTXT if i == 0 else GREEN, sc=ap(t, L[1] + 0.4 * i))
        g.label("=?", CX, 900, 110, color=RED, sc=ap(t, L[2]))
        if t < L[2] - 0.2:
            title(g, t, L[1], "ความหมายของ \"เสรีภาพ\"", NAVY, 86)
        else:
            title(g, t, L[2], "ยังเหมือนเดิมไหม?", RED, 96)
        return
    with g.at(CX + 170, 640, ap(t, L[3])):   # ชวนคอมเมนต์
        g.bubble(0, 0, 460, 220, WHITE, tail=(-1, 1))
        for i in range(3):
            g.circle(-110 + i * 110, 0, 24 + 6 * math.sin(t * 6 - i), INK, 0)
    statue(g, 270, GROUND, 0.66, VERDIGRIS, t, glow=0.6)
    title(g, t, L[3], "มาแลกเปลี่ยนกันในคอมเมนต์!", RED, 70)


SCENES = {
    "hook": s_hook, "open": s_open, "money": s_money, "copper": s_copper, "hope": s_hope,
    "lesson": s_lesson, "outro": s_outro,
}
NO_IRIS = set()
