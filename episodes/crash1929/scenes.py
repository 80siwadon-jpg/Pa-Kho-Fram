"""ฉากตอน: วันพฤหัสทมิฬ (24 ต.ค. 1929) — ตลาดหุ้นวอลล์สตรีทพัง"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from chars import (BANKER, BROKERS, COMMON, bank, bell, bubble_burst, chart, clock, exchange, factory,  # noqa: E402
                   headline, money_stack, soup_line, ticker)
from gfx import GOLD2, GREY, INK, NAVY, RED, W, WHITE, e_io, e_out, hexc, lerp, pop, seg  # noqa: E402
from people import person  # noqa: E402

CX = W / 2
GROUND = 1270
GOLDTXT = hexc("#b37a12")
GREEN = hexc("#3c8d4f")
DARK = hexc("#2b2622")

CAMERA = {"hook": "push_in", "boom": "pan_right", "crash": "dutch", "panic": "pan_left", "depression": "pull_out",
          "lesson": "tilt_up", "outro": "pan_right"}
TRANSITIONS = {"boom": "fade", "crash": "zoom", "panic": "whip", "depression": "iris", "lesson": "fade",
               "outro": "whip"}

UP = [(0, 0.1), (0.2, 0.2), (0.4, 0.35), (0.6, 0.55), (0.8, 0.75), (1, 0.95)]
DOWN = [(0, 0.95), (0.15, 0.9), (0.3, 0.7), (0.5, 0.45), (0.7, 0.3), (0.85, 0.12), (1, 0.03)]


def ap(t, a, dur=0.38):
    return pop(t, a - 0.2, dur)


def crowd(g, t, looks, x0=150, gap=280, sc=0.6, mood="smile", pose="down", talk=False, jitter=0.0):
    for i, lk in enumerate(looks):
        person(g, x0 + i * gap + jitter * math.sin(t * 7 + i * 2), GROUND, lk, sc, mood=mood,
               pose=pose if i % 2 == 0 else ("point" if pose == "v" else pose), turn=0.3 - 0.2 * i, seed=10 + i,
               talk=talk)


# ------------------------------------------------------------------ 1. hook
def s_hook(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:
        exchange(g, CX, GROUND, 0.95 * pop(t, 0.4), t)
        g.label("วันนี้ในอดีต", CX, 300, 104, sc=lerp(2.0, 1, e_out(seg(t, 0.1, 0.4))) if t > 0.1 else 0, rot=-3)
        g.label("24 ตุลาคม 1929", CX, 430, 84, color=RED, sc=pop(t, 0.8))
        return
    if t < L[2] - 0.2:   # ระฆังเปิดตลาด 10 โมง
        bell(g, 330, 760, 1.2 * ap(t, L[1]), t, 1.0)
        clock(g, 800, 760, 170, 10, 0, ap(t, L[1] + 0.3))
        g.label("ระฆังเปิดตลาด 10:00", CX, 380, 84, color=GOLDTXT, sc=ap(t, L[1]), rot=-3)
        return
    if t < L[4] - 0.2:   # สัญญาณหายนะ
        exchange(g, CX, GROUND, 0.95, t)
        for i in range(3):
            u = (t * 0.8 + i / 3) % 1
            g.label("!", 200 + i * 340, 900 - 200 * u, 100, color=RED, a=1 - u)
        if t < L[3] - 0.2:
            g.label("สัญญาณหายนะ...", CX, 380, 96, color=RED, sc=ap(t, L[2]), rot=-3)
        else:
            g.label("ครั้งใหญ่ที่สุดในประวัติศาสตร์!", CX, 380, 72, color=RED, sc=ap(t, L[3]), rot=-3)
        return
    if t < L[5] - 0.2:   # ความมั่งคั่งละลาย
        money_stack(g, CX, 1150, 7, 1.4, e_io(seg(t, L[4] + 0.3, L[5] - 0.3)))
        g.label("ความมั่งคั่งละลายหายไป", CX, 380, 80, color=GREEN, sc=ap(t, L[4]), rot=-3)
        return
    with g.at(CX, 780, ap(t, L[5]) * (1 + 0.03 * math.sin(t * 4)), -3):   # Black Thursday
        g.rrect(-330, -150, 660, 300, 24, DARK, 8)
        g.text("BLACK", 0, -50, 110, "kanit", WHITE)
        g.text("THURSDAY", 0, 70, 90, "kanit", hexc("#ff7a6a"))
    g.label('"วันพฤหัสทมิฬ"', CX, 380, 110, color=DARK, sc=ap(t, L[5]), rot=-3)


# ------------------------------------------------------------------ 2. boom
def s_boom(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[3] - 0.2:   # ยุคทอง หุ้นพุ่ง
        g.sunburst(CX, 760, 200, 600, 20, t * 8, 10, (0.98, 0.85, 0.4, 0.5))
        chart(g, 160, 1150, 760, 600, UP, e_io(seg(t, 0.3, L[3] - 0.5)))
        if t < L[1] - 0.2:
            g.label("ทศวรรษ 1920", CX, 380, 100, sc=ap(t, 0.2), rot=-3)
        elif t < L[2] - 0.2:
            g.label("ยุคทองแห่งความเฟื่องฟู!", CX, 380, 80, color=GOLDTXT, sc=ap(t, L[1]), rot=-3)
        else:
            g.label("หุ้นไม่มีวันร่วง!", CX, 380, 96, color=GREEN, sc=ap(t, L[2]), rot=-3)
        return
    if t < L[5] - 0.2:   # คนธรรมดากู้เงินซื้อหุ้น
        crowd(g, t, COMMON, 170, 340, 0.62, "smile", "hold")
        names = ("คนกวาดถนน", "คนขับแท็กซี่", "แม่บ้าน")
        for i, nm in enumerate(names):
            g.label(nm, 170 + i * 340, 1150, 40, color=GREY, sc=ap(t, L[3] + 0.3 * i))
        if t > L[4] - 0.2:
            for i in range(3):
                with g.at(250 + i * 340, 640 + 10 * math.sin(t * 3 + i), ap(t, L[4] + 0.2 * i)):
                    g.rrect(-80, -40, 160, 80, 12, hexc("#f4efe2"), 5)
                    g.text("กู้!", 0, 0, 40, "kanit", RED)
            g.label("กู้หนี้ยืมสินมาซื้อหุ้น", CX, 380, 80, color=RED, sc=ap(t, L[4]), rot=-3)
        else:
            g.label("คนธรรมดาก็เล่นหุ้น", CX, 380, 86, sc=ap(t, L[3]), rot=-3)
        return
    money_stack(g, 230, 1180, 6, 1.0)   # ทางลัดสู่เศรษฐี / เต้นรำบนภาพลวงตา
    money_stack(g, 860, 1180, 6, 1.0)
    for i, lk in enumerate(BROKERS[:2] + COMMON[2:]):
        x = 380 + i * 160 + 30 * math.sin(t * 4 + i)
        person(g, x, GROUND - 60 * abs(math.sin(t * 4 + i)), lk, 0.5, mood="smile", pose="wave", turn=0.2,
               seed=20 + i, shadow=False)
    if t < L[6] - 0.2:
        g.label("ทางลัดสู่เศรษฐี!", CX, 380, 96, color=GOLDTXT, sc=ap(t, L[5]), rot=-3)
    else:
        bubble_burst(g, CX, 640, 110 + 10 * math.sin(t * 2), 0.0, t)
        g.label("เต้นรำบนภาพลวงตา", CX, 380, 86, color=NAVY, sc=ap(t, L[6]), rot=-3)


# ------------------------------------------------------------------ 3. crash
def s_crash(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:   # ฟองสบู่แตก
        k = seg(t, 0.8, 1.6)
        bubble_burst(g, CX, 780, 260, k, t)
        g.label("ฟองสบู่แตกโพล๊ะ!", CX, 380, 100, color=RED, sc=ap(t, 0.2), rot=-3)
        return
    if t < L[4] - 0.2:   # เทขาย / ดิ่งลงเหว / ตื่นตระหนก
        chart(g, 160, 1150, 760, 600, DOWN, e_io(seg(t, L[1], L[3])), RED)
        for i in range(4):
            u = (t * 0.9 + i / 4) % 1
            with g.at(220 + i * 220, 500 + 500 * u, 1, 20 * math.sin(t * 3 + i)):
                g.rrect(-70, -36, 140, 72, 10, WHITE, 5, stroke=RED)
                g.text("ขาย!", 0, 0, 36, "kanit", RED)
        if t < L[2] - 0.2:
            g.label("คลื่นเทขายถาโถม!", CX, 380, 92, color=RED, sc=ap(t, L[1]), rot=-3)
        elif t < L[3] - 0.2:
            g.label("ราคาดิ่งลงเหว!", CX, 380, 100, color=RED, sc=ap(t, L[2]), rot=-3)
        else:
            g.label("ยิ่งตก ยิ่งตื่นตระหนก", CX, 380, 86, color=DARK, sc=ap(t, L[3]), rot=-3)
        return
    ticker(g, 220, 1000, 1.2, t, 4.0, 520)   # เครื่องพิมพ์ราคาหุ้นตามไม่ทัน
    for i in range(3):
        g.label("?", 760 + i * 90, 640 + 20 * math.sin(t * 5 + i), 70, color=RED, sc=ap(t, L[4] + 0.3 * i))
    g.label("เครื่องพิมพ์ราคาตามไม่ทัน!", CX, 380, 78, color=RED, sc=ap(t, L[4]), rot=-3)


# ------------------------------------------------------------------ 4. panic
def s_panic(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # ห้องค้าหุ้นโกลาหล
        crowd(g, t, BROKERS, 170, 350, 0.58, "shout", "v", True, 12)
        for i in range(8):
            u = (t * 0.7 + i / 8) % 1
            with g.at(80 + i * 130, 400 + 900 * u, 1, t * 200 + i * 40):
                g.rrect(-30, -20, 60, 40, 3, hexc("#f4efe2"), 3)
        if t < L[1] - 0.2:
            g.label("วุ่นวายโกลาหล!", CX, 380, 100, color=RED, sc=ap(t, 0.2), rot=-3)
        else:
            g.label("เสียงตะโกนสิ้นหวัง!", CX, 380, 92, color=DARK, sc=ap(t, L[1]), rot=-3)
        return
    exchange(g, CX, GROUND - 160, 0.6, t, 0.5)   # ฝูงชนนับหมื่นล้อมวอลล์สตรีท
    for r in range(2):
        for i in range(7):
            lk = (COMMON + BROKERS)[(i + r) % 6]
            person(g, 80 + i * 150 + r * 70, GROUND + r * 40, lk, 0.42 + r * 0.06, mood="worry" if r else "shock",
                   pose="down", turn=-0.2, seed=40 + i + r * 7, shadow=False)
    if t < L[3] - 0.2:
        g.label("ฝูงชนนับหมื่นล้อมวอลล์สตรีท", CX, 380, 68, sc=ap(t, L[2]), rot=-3)
    else:
        money_stack(g, 820, 760, 4, 0.7, e_io(seg(t, L[3], L[3] + 2.0)))
        g.label("เงินเก็บทั้งชีวิตมลายหาย", CX, 380, 74, color=RED, sc=ap(t, L[3]), rot=-3)


# ------------------------------------------------------------------ 5. depression
def s_depression(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[3] - 0.2:   # นายธนาคารลงขันพยุงตลาด -> หยุดไม่ได้
        person(g, 300, GROUND, BANKER, 0.75, mood="firm" if t < L[2] else "worry", pose="hold" if t < L[2] else
               "shrug", turn=0.3, seed=50)
        with g.at(0, -20 * abs(math.sin(t * 2.5))):
            money_stack(g, 760, 1180, 6, 1.0)
        if t < L[1] - 0.2:
            g.label("นายธนาคารลงขันหลายสิบล้าน", CX, 380, 70, color=GREEN, sc=ap(t, 0.2), rot=-3)
        elif t < L[2] - 0.2:
            chart(g, 600, 900, 320, 260, [(0, 0.3), (0.5, 0.5), (1, 0.6)], e_io(seg(t, L[1], L[2])), GREEN, 8)
            g.label("ช้อนซื้อพยุงตลาด", CX, 380, 90, color=GREEN, sc=ap(t, L[1]), rot=-3)
        else:
            g.label("หยุดความตื่นตระหนกไม่ได้...", CX, 380, 74, color=RED, sc=ap(t, L[2]), rot=-3)
        return
    if t < L[4] - 0.2:   # เกือบ 13 ล้านหุ้น
        n = 12.9 * e_out(seg(t, L[3], L[4] - 0.6))
        ticker(g, 200, 1150, 0.9, t, 3.0, 400)
        with g.at(720, 700, ap(t, L[3])):
            g.circle(0, 0, 190, WHITE, 8)
            g.label(f"{n:.1f}", 0, -30, 110, color=RED)
            g.label("ล้านหุ้น", 0, 80, 44, color=GREY)
        g.label("หุ้นเปลี่ยนมือในวันเดียว", CX, 380, 80, sc=ap(t, L[3]), rot=-3)
        return
    if t < L[6] - 0.2:   # ประตูนรก -> Great Depression
        g.c.rectangle(-500, 140, 2100, 1130)
        g.c.set_source_rgba(0.2, 0.2, 0.22, 0.25 * ap(t, L[4]))
        g.c.fill()
        headline(g, CX, 800, 0.9 * ap(t, L[4]), -3 + math.sin(t), "THE GREAT", "DEPRESSION 1929-1939")
        if t < L[5] - 0.2:
            g.label("เปิดประตูสู่...", CX, 380, 96, color=DARK, sc=ap(t, L[4]), rot=-3)
        else:
            g.label("ภาวะเศรษฐกิจตกต่ำครั้งใหญ่", CX, 380, 72, color=RED, sc=ap(t, L[5]), rot=-3)
        return
    if t < L[7] - 0.2:   # ธนาคารล้ม โรงงานปิด
        bank(g, 280, GROUND, 0.9, ap(t, L[6] + 0.4))
        factory(g, 780, GROUND, 0.9, t, 1.0 if t > L[6] + 1.2 else 0.0)
        g.label("ธนาคารล้ม โรงงานปิด", CX, 380, 86, color=RED, sc=ap(t, L[6]), rot=-3)
        return
    soup_line(g, 120, GROUND, 7, 0.5, t)   # คนไร้บ้าน / อดอยาก (แถวรอรับอาหาร)
    if t < L[8] - 0.2:
        g.label("ผู้คนนับล้านไร้บ้าน", CX, 380, 90, color=DARK, sc=ap(t, L[7]), rot=-3)
    else:
        with g.at(CX, 620, ap(t, L[8])):
            g.rrect(-200, -60, 400, 120, 20, WHITE, 6)
            g.label("10 ปี", 0, 0, 70, color=RED)
        g.label("ความอดอยากทั่วโลก", CX, 380, 88, color=RED, sc=ap(t, L[8]), rot=-3)


# ------------------------------------------------------------------ 6. lesson
def s_lesson(g, t, L, d):
    g.ground(GROUND, WHITE)
    g.label("บทเรียน", CX, 340, 100, sc=ap(t, 0.2), rot=-3)
    if t < L[3] - 0.2:
        person(g, 330, GROUND, BROKERS[0], 0.72, mood="smug" if t < L[2] else "shock", pose="hold", turn=0.3,
               seed=60)
        money_stack(g, 780, 1180, 5, 0.9)
        if t > L[1] - 0.2:
            g.label("ความโลภบังตา", CX, 490, 70, color=GOLDTXT, sc=ap(t, L[1]))
        if t > L[2] - 0.2:
            g.label("!", 780, 760, 140, color=RED, sc=ap(t, L[2]))
        return
    chart(g, 160, 1150, 760, 560, UP[:4] + [(0.75, 0.62), (0.9, 0.2), (1, 0.08)], e_io(seg(t, L[3], L[3] + 2.0)), RED)
    g.label("ไม่มีอะไรขึ้นไปได้ตลอดกาล", CX, 490, 62, color=RED, sc=ap(t, L[3]))


# ------------------------------------------------------------------ 7. outro
def s_outro(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[3] - 0.2:
        if t < L[1] - 0.2:
            with g.at(CX, 780 + 16 * math.sin(t * 2), 0.8 * ap(t, 0.2) * (1 + 0.04 * math.sin(t * 3)), -3 + 3 * math.sin(t * 1.5)):
                g.rrect(-330, -150, 660, 300, 24, DARK, 8)
                g.text("BLACK", 0, -50, 110, "kanit", WHITE)
                g.text("THURSDAY", 0, 70, 90, "kanit", hexc("#ff7a6a"))
            g.label("คิดอย่างไรกันบ้าง?", CX, 380, 92, sc=ap(t, 0.2), rot=-3)
            return
        if t < L[2] - 0.2:
            for i, txt in enumerate(("หุ้นเก็งกำไร", "คริปโต", "กู้มาลงทุน")):
                with g.at(CX, 620 + i * 190, ap(t, L[1] + 0.35 * i) * (1 + 0.03 * math.sin(t * 3 + i))):
                    g.rrect(-220, -65, 440, 130, 30, WHITE, 7, stroke=GOLDTXT)
                    g.label(txt, 0, 0, 52, color=GOLDTXT)
            g.label("ยุคเก็งกำไรวันนี้", CX, 380, 90, color=NAVY, sc=ap(t, L[1]), rot=-3)
            return
        g.sunburst(860, 560, 110, 260, 14, t * 15, 8, (0.98, 0.6, 0.5, 0.5))
        with g.at(0, 12 * math.sin(t * 2.2)):
            chart(g, 160, 1150, 760, 560, UP[:5] + [(0.9, 0.85)], e_io(seg(t, L[2] - 0.2, L[3] - 0.5)))
        g.label("?", 860 + 20 * math.sin(t * 3), 560 + 20 * math.sin(t * 2), 170, color=RED, sc=ap(t, L[2] + 0.3),
                rot=10 * math.sin(t * 2))
        g.label("ประวัติศาสตร์จะซ้ำรอยไหม?", CX, 380, 76, color=RED, sc=ap(t, L[2]), rot=-3)
        return
    with g.at(CX + 170, 640, ap(t, L[3])):   # ชวนคอมเมนต์
        g.bubble(0, 0, 460, 220, WHITE, tail=(-1, 1))
        for i in range(3):
            g.circle(-110 + i * 110, 0, 24 + 6 * math.sin(t * 6 - i), INK, 0)
    person(g, 250, GROUND, BROKERS[1], 0.75, mood="smile", pose="wave", turn=0.3, seed=70, talk=True)
    g.label("คอมเมนต์แลกเปลี่ยนกันได้เลย!", CX, 360, 70, color=RED, sc=ap(t, L[3]), rot=-3)


SCENES = {
    "hook": s_hook, "boom": s_boom, "crash": s_crash, "panic": s_panic, "depression": s_depression,
    "lesson": s_lesson, "outro": s_outro,
}
NO_IRIS = set()
