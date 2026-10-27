"""ฉากตอน: อังคารทมิฬ 29 ต.ค. 1929 — ใช้ตัวละคร/พร็อพจากตอน crash1929"""
import importlib.util
import math
import os
import sys

from gfx import GOLD, GOLD2, GREY, INK, NAVY, RED, W, WHITE, e_io, e_out, hexc, lerp, pop, seg  # noqa: E402
from people import _rr, _shade, person  # noqa: E402

_spec = importlib.util.spec_from_file_location(
    "crash_chars", os.path.join(os.path.dirname(__file__), "..", "crash1929", "chars.py"))
cr = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cr)
BROKERS, COMMON, BANKER = cr.BROKERS, cr.COMMON, cr.BANKER

CX = W / 2
GROUND = 1270
GOLDTXT = hexc("#b37a12")
GREEN = hexc("#3c8d4f")
DARK = hexc("#3a3f48")
UP = [(0, 0.1), (0.2, 0.25), (0.4, 0.35), (0.6, 0.55), (0.8, 0.75), (1, 0.95)]
DOWN = [(0, 0.95), (0.15, 0.9), (0.3, 0.6), (0.5, 0.45), (0.7, 0.2), (1, 0.05)]

CAMERA = {"hook": "push_in", "roaring": "pan_right", "panic": "dutch", "loss": "push_in", "sec": "pull_out",
          "lesson": "pan_left", "outro": "pan_right"}
TRANSITIONS = {"roaring": "zoom", "panic": "whip", "loss": "iris", "sec": "fade", "lesson": "zoom", "outro": "whip"}


def ap(t, a, dur=0.38):
    return pop(t, a - 0.2, dur)


def title(g, t, a, txt, col=INK, size=84, y=380):
    g.label(txt, CX, y, size, color=col, sc=ap(t, a), rot=-3)


def papers(g, t, n=10, k=1.0, x0=140, x1=940):
    """ใบหุ้นปลิวว่อน"""
    for i in range(n):
        u = (t * 0.35 + i / n) % 1
        x = x0 + (x1 - x0) * ((i * 0.37) % 1) + 50 * math.sin(t * 2 + i)
        y = 480 + 760 * u
        with g.at(x, y, 0.5 * k, 40 * math.sin(t * 3 + i)):
            g.rrect(-60, -40, 120, 80, 6, (0.96, 0.94, 0.88, 1 - u * 0.5), 4)
            g.line([(-40, -10), (40, -10)], 3, GREY, amp=0)
            g.line([(-40, 12), (20, 12)], 3, GREY, amp=0)


def crowd(g, t, x0=140, n=5, sc=0.6, mood="shock", pose="v", seed=10):
    looks = BROKERS + COMMON
    for i in range(n):
        p = pose if i % 2 == 0 else "point"
        person(g, x0 + i * 165, GROUND, looks[i % len(looks)], sc, mood=mood, pose=p, turn=0.3 - 0.15 * i,
               seed=seed + i, talk=True)


def sell_bubble(g, x, y, sc, t, rot=0.0):
    if sc < 0.02:
        return
    with g.at(x, y + 8 * math.sin(t * 6), sc, rot):
        g.bubble(0, 0, 260, 120, WHITE, tail=(-1, 1))
        g.label("ขาย!", 0, 0, 60, color=RED)


def coin_btc(g, x, y, r, t=0.0):
    with g.at(x, y, 1, 10 * math.sin(t * 2)):
        g.circle(0, 0, r, GOLD, 6)
        g.circle(0, 0, r * 0.78, GOLD2, 3)
        g.text("BTC", 0, 0, int(r * 0.55), "kanit", INK)


def courthouse(g, x, y, sc=1.0, label="SEC"):
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -300, -60, 600, 60, 4)
        _shade(c, cr.STONE, 5, 0.2)
        for i in range(5):
            _rr(c, -250 + i * 120, -380, 50, 320, 6)
            _shade(c, WHITE, 4, 0.15)
        c.new_path()
        for p in [(-320, -380), (0, -520), (320, -380)]:
            c.line_to(*p)
        c.close_path()
        _shade(c, cr.STONE, 5, 0.25)
        g.text(label, 0, -430, 60, "kanit", NAVY)


def receipt(g, x, y, sc=1.0, rot=0.0, k=1.0):
    c = g.c
    with g.at(x, y, sc, rot):
        h = 520 * k
        c.new_path()
        c.move_to(-170, -260)
        c.line_to(170, -260)
        c.line_to(170, -260 + h)
        for i in range(9):
            c.line_to(170 - (i + 0.5) * 340 / 9, -260 + h + (12 if i % 2 == 0 else 0))
        c.line_to(-170, -260 + h)
        c.close_path()
        _shade(c, WHITE, 5, 0.05)
        g.text("บิลความโลภ", 0, -210, 40, "kanit", INK)
        for i in range(int(6 * k)):
            g.line([(-130, -150 + i * 50), (60, -150 + i * 50)], 3, GREY, amp=0)
            g.text("$$$", 110, -150 + i * 50, 26, "kanit", RED)
        if k >= 1:
            g.text("รวม: แพงที่สุด!", 0, 200, 40, "kanit", RED)


# ------------------------------------------------------------------ 1. hook
def s_hook(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # เสียงกรีดร้องลั่นตลาดหุ้นนิวยอร์ก
        cr.exchange(g, CX, GROUND - 200, 0.6, t, 0.5)
        crowd(g, t, 160, 5, 0.58)
        for i in range(3):
            sell_bubble(g, 220 + i * 300, 560 + 40 * (i % 2), 0.7 * ap(t, L[1] + 0.3 * i, 0.3), t + i, -6 + 6 * i)
        title(g, t, L[1], "เสียงกรีดร้องลั่นตลาดหุ้นนิวยอร์ก", RED, 76)
        return
    if t < L[3] - 0.2:   # 16 ล้านหุ้นเหมือนเศษกระดาษ
        papers(g, t, 14)
        n = int(lerp(1, 16, e_out(seg(t, L[2], L[2] + 2.0))))
        g.label(f"{n} ล้านหุ้น!", CX, 820, 120, color=RED, sc=ap(t, L[2] + 0.2), rot=-4)
        title(g, t, L[2], "เทขายเหมือนเศษกระดาษ!", INK, 86)
        return
    cr.chart(g, 160, 1150, 760, 600, DOWN, e_io(seg(t, L[3] - 0.2, L[4] + 0.5)), RED)   # ดิ่งลงเหว
    if t < L[4] - 0.2:
        title(g, t, L[3], "จุดเริ่มเศรษฐกิจตกต่ำครั้งใหญ่", INK, 80)
    else:
        title(g, t, L[4], "ลากทั้งโลกดิ่งลงเหว!", RED, 92)


# ------------------------------------------------------------------ 2. roaring
def s_roaring(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # 29 ต.ค. 1929 อังคารทมิฬ
        dark = t > L[1] - 0.2
        g.calendar(CX, 860, 1.25 * ap(t, L[0]) + 0.01, 29, "อังคาร", "ต.ค. 1929")
        if dark:
            g.label("Black Tuesday", CX, 1160, 70, color=INK, sc=ap(t, L[1] + 0.3))
            title(g, t, L[1], "\"อังคารทมิฬ\"", INK, 110)
        else:
            title(g, t, L[0], "29 ตุลาคม 1929", RED, 92)
        return
    if t < L[4] - 0.2:   # Roaring Twenties หุ้นขึ้นไม่มีวันลง
        cr.chart(g, 160, 1150, 760, 600, UP, e_io(seg(t, L[2], L[3] + 1.5)), GREEN)
        for i in range(5):
            g.sparkle(240 + i * 150, 560 + 40 * math.sin(t * 3 + i), 24)
        if t < L[3] - 0.2:
            title(g, t, L[2], "\"Roaring Twenties\" ยุคทอง", GOLDTXT, 86)
        else:
            title(g, t, L[3], "เชื่อว่าหุ้นมีแต่ขึ้น!", GREEN, 92)
        return
    if t < L[6] - 0.2:   # ทุกคนกู้เงินมาเก็งกำไร
        for i, lk in enumerate(COMMON + [BROKERS[0]]):
            person(g, 190 + i * 230, GROUND, lk, 0.62, mood="smile", pose="hold", turn=0.3 - 0.2 * i, seed=20 + i)
        if t > L[5] - 0.2:
            cr.money_stack(g, CX, 640, 5, 0.8 * ap(t, L[5]) + 0.01)
            title(g, t, L[5], "กู้เงินก้อนโตมาเก็งกำไร", GOLDTXT, 86)
        else:
            title(g, t, L[4], "คนกวาดถนน คนขับแท็กซี่ นักธุรกิจ", INK, 74)
        return
    k = e_io(seg(t, L[6] + 1.2, L[6] + 2.2))
    cr.bubble_burst(g, CX, 840, 250, k, t)   # ฟองสบู่แตก
    if k > 0.3:
        papers(g, t, 10, min(1, (k - 0.3) * 2))
        g.label("ปัง!", CX, 840, 130, color=RED, sc=ap(t, L[6] + 1.4), rot=-8)
    title(g, t, L[6], "ฟองสบู่ความโลภถึงจุดระเบิด!", RED, 84)


# ------------------------------------------------------------------ 3. panic
def s_panic(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[3] - 0.2:   # ระฆังเปิดตลาด → พฤหัสทมิฬ → ปะทุ
        if t < L[1] - 0.2:
            cr.bell(g, CX, 860, 1.2, t, 1.0)
            cr.clock(g, 820, 600, 100, 10, 0)
            title(g, t, L[0], "ระฆังเปิดตลาดดังขึ้น", GOLDTXT, 88)
        else:
            g.calendar(330, 860 + 12 * math.sin(t * 2), 0.85, 24, "พฤหัส", "ต.ค. 1929")
            g.label("→", CX, 860, 100, color=GREY, sc=ap(t, L[1] + 0.4))
            g.calendar(760, 860 - 12 * math.sin(t * 2), (0.85 + 0.04 * math.sin(t * 5)) * ap(t, L[1] + 0.8) + 0.01, 29,
                       "อังคาร", "ต.ค. 1929")
            for i in range(3):
                u = (t * 1.5 + i / 3) % 1
                g.arc(760, 860, 160 + 120 * u, -40, 40, 6, (*RED[:3], 1 - u))
            if t < L[2] - 0.2:
                title(g, t, L[1], "ต่อเนื่องจาก \"พฤหัสบดีทมิฬ\"", INK, 82)
            else:
                title(g, t, L[2], "ความตื่นตระหนกปะทุ!", RED, 92)
        return
    if t < L[6] - 0.2:   # ขาย ขาย ขาย! ไม่มีใครซื้อ
        crowd(g, t, 210, 5, 0.55, "shout")
        for i in range(4):
            sell_bubble(g, 200 + i * 230, 560 + 50 * (i % 2), 0.6 * ap(t, L[3] + 0.25 * i, 0.3), t + i, -8 + 5 * i)
        if t < L[4] - 0.2:
            title(g, t, L[3], "\"ขาย ขาย ขาย!\"", RED, 104)
        elif t < L[5] - 0.2:
            title(g, t, L[4], "ทิ้งหุ้นทุกตัวในมือ", INK, 92)
        else:
            g.label("ผู้ซื้อ: 0", CX, 880, 110, color=RED, sc=ap(t, L[5] + 0.2), rot=-5)
            title(g, t, L[5], "ไม่มีใครยอมซื้อเลย!", RED, 92)
        return
    cr.ticker(g, 220, 1000, 1.2, t, 4.0, 520)   # Ticker Tape ช้าหลายชั่วโมง
    cr.clock(g, 790, 640, 110, int(10 + 5 * seg(t, L[6], L[7] + 2)) % 12 or 12, 0)
    if t < L[7] - 0.2:
        title(g, t, L[6], "Ticker Tape ช้าไปหลายชั่วโมง", NAVY, 80)
    else:
        g.label("?", 790, 860, 120, color=RED, sc=ap(t, L[7] + 0.4))
        title(g, t, L[7], "ยิ่งตื่นตระหนกทวีคูณ!", RED, 90)


# ------------------------------------------------------------------ 4. loss
def s_loss(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # 16.4 ล้านหุ้น / 14,000 ล้านดอลลาร์หายวับ
        if t < L[1] - 0.2:
            papers(g, t, 12)
            n = lerp(1, 16.4, e_out(seg(t, L[0], L[0] + 1.8)))
            g.label(f"{n:.1f} ล้านหุ้น", CX, 840, 110, color=RED, sc=ap(t, L[0] + 0.2), rot=-4)
            title(g, t, L[0], "ในวันเดียว!", INK, 100)
        else:
            cr.money_stack(g, CX, 1150, 6, 1.4, e_io(seg(t, L[1], L[1] + 2.5)))
            n = int(lerp(0, 14000, e_out(seg(t, L[1], L[1] + 2.0))))
            g.label(f"-${n:,} ล้าน", CX, 620, 96, color=RED, sc=ap(t, L[1] + 0.2), rot=-4)
            title(g, t, L[1], "ความมั่งคั่งหายวับกว่า 14,000 ล้านดอลลาร์", RED, 70)
        return
    if t < L[4] - 0.2:   # ทั้งสัปดาห์ > งบรัฐบาลทั้งปีหลายเท่า
        k = e_io(seg(t, L[2], L[3] + 1.0))
        for i, (lab, h, col) in enumerate((("งบรัฐบาล 1 ปี", 0.18, NAVY), ("เงินที่หายไป 1 สัปดาห์", 0.9, RED))):
            hh = 600 * h * (k if i else 1)
            g.rrect(230 + i * 380 - 110, 1150 - hh, 220, hh, 10, col, 6)
            g.label(lab, 230 + i * 380, 1210, 40, color=col)
        if t < L[3] - 0.2:
            title(g, t, L[2], "เมื่อรวมตลอดสัปดาห์นั้น...", INK, 86)
        else:
            title(g, t, L[3], "มากกว่างบรัฐบาลทั้งปีหลายเท่า!", RED, 80)
        return
    if t < L[6] - 0.2:   # หมดตัว / ธนาคารล้ม ธุรกิจปิดเป็นโดมิโน
        if t < L[5] - 0.2:
            person(g, CX, GROUND, BROKERS[2], 0.86, mood="sad", pose="down", turn=0.0, seed=30)
            with g.at(CX + 210, 760, ap(t, L[4] + 0.3), 8):
                g.rrect(-110, -60, 220, 120, 14, WHITE, 6, stroke=RED)
                g.text("$0", 0, 0, 70, "kanit", RED)
            title(g, t, L[4], "หมดเนื้อหมดตัวชั่วข้ามคืน", INK, 84)
        else:
            cr.bank(g, 290, GROUND, 0.75, seg(t, L[5], L[5] + 1.0))
            cr.factory(g, 760, GROUND, 0.7, t, seg(t, L[5] + 1.0, L[5] + 2.2))
            title(g, t, L[5], "ธนาคารล้ม ธุรกิจปิดเป็นโดมิโน", RED, 80)
        return
    if t < L[7] - 0.2:   # Great Depression
        cr.headline(g, CX, 840, 1.0 * ap(t, L[6]) + 0.01, -3 + 2 * math.sin(t * 2), "THE GREAT", "DEPRESSION", "1930s")
        title(g, t, L[6], "\"ภาวะเศรษฐกิจตกต่ำครั้งใหญ่\"", INK, 82)
        return
    cr.soup_line(g, 160, GROUND, 6, 0.55, t)   # ตกงาน ต่อคิวรับอาหาร / ยาวนานนับสิบปี
    if t < L[8] - 0.2:
        title(g, t, L[7], "ตกงานนับสิบล้าน ต่อคิวรับอาหาร", NAVY, 78)
    else:
        n = int(lerp(1929, 1939, e_io(seg(t, L[8], L[8] + 2.0))))
        g.label(str(n), CX, 620, 110, color=GREY, sc=ap(t, L[8] + 0.2))
        title(g, t, L[8], "ยาวนานนับสิบปีทั่วโลก", INK, 86)


# ------------------------------------------------------------------ 5. sec
def s_sec(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:
        receipt(g, CX, 840, 1.0, -3 + 2 * math.sin(t * 2), e_io(seg(t, L[0], L[0] + 2.5)))
        title(g, t, L[0], "บทเรียนราคาแพงที่สุด", RED, 90)
        return
    courthouse(g, CX, GROUND, 1.0 * ap(t, L[1]) + 0.01)
    if t < L[2] - 0.2:
        title(g, t, L[1], "ก่อตั้ง SEC กำกับตลาดหุ้น", NAVY, 86)
    elif t < L[3] - 0.2:
        with g.at(800, 620, ap(t, L[2] + 0.2), 8):
            g.rrect(-130, -160, 260, 320, 10, hexc("#f4eedf"), 6)
            g.text("กฎหมาย", 0, -100, 40, "kanit", NAVY)
            for i in range(4):
                g.line([(-90, -30 + i * 45), (90, -30 + i * 45)], 4, GREY, amp=0)
        title(g, t, L[2], "กฎหมายควบคุมการเงินเข้มงวด", NAVY, 82)
    else:
        k = seg(t, L[3] + 0.3, L[3] + 1.0)
        g.label("1929", CX, 640, 100, color=GREY, sc=ap(t, L[3]))
        if k > 0:
            g.line([(CX - 160, 590), (CX - 160 + 320 * k, 590 + 100 * k)], 14, RED, amp=0)
        title(g, t, L[3], "ไม่ให้ประวัติศาสตร์ซ้ำรอย", GREEN, 86)


# ------------------------------------------------------------------ 6. lesson
def s_lesson(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # ไม่มีอะไรขึ้นไปบนฟ้าได้ตลอดกาล
        u = (t * 0.25) % 1
        cr.chart(g, 160, 1150, 760, 600, UP[:4] + [(0.8, 1.0), (1, 0.2)], e_io(seg(t, L[0], L[1] + 2.0)), GOLD)
        if t < L[1] - 0.2:
            title(g, t, L[0], "Black Tuesday เตือนใจว่า...", INK, 84)
        else:
            title(g, t, L[1], "ไม่มีอะไรขึ้นไปบนฟ้าได้ตลอดกาล", RED, 76)
        return
    receipt(g, 720, 860, 1.0, 4 + 2 * math.sin(t * 2), e_io(seg(t, L[2], L[3] + 1.0)))   # บิลความโลภ
    person(g, 260, GROUND, BROKERS[2], 0.8, mood="worry", pose="down", turn=0.4, seed=40)
    if t < L[3] - 0.2:
        title(g, t, L[2], "ความโลภที่ไร้สติ...", RED, 92)
    else:
        title(g, t, L[3], "ทิ้งบิลแพงที่สุดไว้ให้จ่าย!", RED, 84)


# ------------------------------------------------------------------ 7. outro
def s_outro(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:
        g.calendar(CX, 860, 1.1, 29, "อังคาร", "ต.ค. 1929")
        title(g, t, L[0], "คิดอย่างไรกันบ้าง?", INK, 92)
        return
    if t < L[3] - 0.2:   # คริปโต ผันผวน / เรียนรู้หรือยัง
        coin_btc(g, 300, 760, 120, t)
        pts = [(0, 0.3), (0.15, 0.7), (0.3, 0.2), (0.5, 0.9), (0.65, 0.35), (0.85, 0.8), (1, 0.4)]
        cr.chart(g, 520, 1150, 400, 450, pts, e_io(seg(t, L[1], L[2] + 1.0)), hexc("#e3843a"), 9)
        if t < L[2] - 0.2:
            title(g, t, L[1], "การเงินและคริปโตผันผวนสูง", hexc("#d9732a"), 82)
        else:
            g.label("?", 300, 1040, 120, color=RED, sc=ap(t, L[2] + 0.3))
            title(g, t, L[2], "มนุษย์เรียนรู้แล้วหรือยัง?", RED, 86)
        return
    with g.at(CX + 170, 640, ap(t, L[3])):   # ชวนคอมเมนต์
        g.bubble(0, 0, 460, 220, WHITE, tail=(-1, 1))
        for i in range(3):
            g.circle(-110 + i * 110, 0, 24 + 6 * math.sin(t * 6 - i), INK, 0)
    person(g, 260, GROUND, BROKERS[1], 0.8, mood="smile", pose="wave", turn=0.3, seed=50, talk=True)
    title(g, t, L[3], "มาแลกเปลี่ยนกันในคอมเมนต์!", RED, 70)


SCENES = {
    "hook": s_hook, "roaring": s_roaring, "panic": s_panic, "loss": s_loss, "sec": s_sec, "lesson": s_lesson,
    "outro": s_outro,
}
NO_IRIS = set()
