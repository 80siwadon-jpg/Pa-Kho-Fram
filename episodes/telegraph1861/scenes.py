"""ฉากตอน: โทรเลขข้ามทวีปสายแรก (24 ต.ค. 1861) ปิดฉากโพนี เอ็กซ์เพรส"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from chars import (LINCOLN, OPERATOR, SAND, TOWNS, chip, envelope, horse, morse_key, sign_closed,  # noqa: E402
                   telegram, telegraph_line, us_map, wagon)
from gfx import GOLD2, GREY, INK, NAVY, RED, W, WHITE, e_io, e_out, hexc, lerp, pop, seg  # noqa: E402
from people import person  # noqa: E402

CX = W / 2
GROUND = 1270
GOLDTXT = hexc("#b37a12")
GREEN = hexc("#3c8d4f")
BROWN = hexc("#8a5a36")

CAMERA = {"hook": "push_in", "distance": "pan_left", "riders": "pan_right", "wire": "push_in", "closure": "dutch",
          "lesson": "pull_out", "outro": "pan_right"}
TRANSITIONS = {"distance": "fade", "riders": "whip", "wire": "zoom", "closure": "iris", "lesson": "fade",
               "outro": "whip"}


def ap(t, a, dur=0.38):
    return pop(t, a - 0.2, dur)


def lincoln(g, x, sc=0.75, mood="smile", pose="hold", turn=0.2):
    person(g, x, GROUND, LINCOLN, sc, mood=mood, pose=pose, turn=turn, seed=4)


def prairie(g, t, speed=0.0):
    """ทุ่งกว้าง: เนินไกล + พุ่มหญ้าเลื่อน"""
    c = g.c
    c.new_path()
    c.move_to(-500, GROUND - 120)
    for i in range(53):
        x = -500 + i * 40
        c.line_to(x, GROUND - 120 + 30 * math.sin(x * 0.005 + 1))
    c.line_to(1600, GROUND)
    c.line_to(-500, GROUND)
    c.close_path()
    c.set_source_rgba(*SAND[:3], 0.6)
    c.fill()
    for i in range(8):
        x = (i * 170 - t * speed) % 1400 - 150
        g.line([(x, GROUND - 4), (x + 10, GROUND - 40)], 5, hexc("#9cbf7a"), amp=0)
        g.line([(x + 14, GROUND - 4), (x + 30, GROUND - 34)], 5, hexc("#9cbf7a"), amp=0)


# ------------------------------------------------------------------ 1. hook
def s_hook(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:   # วันที่ + สัญญาณมอร์ส
        morse_key(g, CX, 1050, 1.5 * pop(t, 0.4), t)
        g.label("วันนี้ในอดีต", CX, 380, 104, sc=lerp(2.0, 1, e_out(seg(t, 0.1, 0.4))) if t > 0.1 else 0, rot=-3)
        g.label("24 ตุลาคม 1861", CX, 520, 84, color=RED, sc=pop(t, 0.8))
        return
    if t < L[4] - 0.2:   # ห้องทำงานวอชิงตัน ลินคอล์นอ่านโทรเลข
        with g.at(860, 700):
            g.rrect(-120, -170, 240, 300, 8, hexc("#dfe8ee"), 6)   # หน้าต่าง
            g.line([(0, -170), (0, 130)], 6, INK, amp=0)
            g.line([(-120, -20), (120, -20)], 6, INK, amp=0)
        lincoln(g, 330, 0.76, "smile" if t > L[3] else "neutral", "hold", 0.3)
        g.name_tag(t, L[2] + 0.2, 780, 1140, "อับราฮัม ลินคอล์น", "ประธานาธิบดีสหรัฐฯ คนที่ 16", side=-1)
        if t > L[3] - 0.2:
            telegram(g, 620, 760 + 8 * math.sin(t * 2), 0.9 * ap(t, L[3]), -4)
        if t < L[2] - 0.2:
            g.label("วอชิงตัน ดี.ซี.", CX, 380, 96, color=NAVY, sc=ap(t, L[1]), rot=-3)
        elif t < L[3] - 0.2:
            g.label("ประธานาธิบดีลินคอล์น", CX, 380, 84, sc=ap(t, L[2]), rot=-3)
        else:
            g.label("จากแคลิฟอร์เนีย ในไม่กี่นาที!", CX, 380, 74, color=RED, sc=ap(t, L[3]), rot=-3)
        return
    if t < L[6] - 0.2:   # สัญญาณข้ามทวีปสำเร็จ = เฉลิมฉลองเทคโนโลยี
        us_map(g, CX, 800, 1.05, t, e_io(seg(t, L[4], L[4] + 1.5)))
        if t < L[5] - 0.2:
            g.label("สัญญาณข้ามทวีปสำเร็จ!", CX, 380, 84, color=GOLDTXT, sc=ap(t, L[4]), rot=-3)
        else:
            for i in range(6):
                u = (t * 0.6 + i / 6) % 1
                g.star(120 + i * 170, 1150 - 500 * u, 22, GOLD2, 4)
            g.label("เทคโนโลยีล้ำหน้า!", CX, 380, 96, color=GREEN, sc=ap(t, L[5]), rot=-3)
        return
    prairie(g, t)   # ระฆังมรณะของม้าเร็ว
    horse(g, lerp(560, 420, seg(t, L[6], d)), GROUND, 0.8, t, 0.35)
    if t < L[7] - 0.2:
        g.label("แต่... เสียงระฆังมรณะ", CX, 380, 84, color=RED, sc=ap(t, L[6]), rot=-3)
    else:
        g.label("ปิดฉากตำนานม้าเร็ว!", CX, 380, 86, color=RED, sc=ap(t, L[7]), rot=-3)


# ------------------------------------------------------------------ 2. distance
def s_distance(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[3] - 0.2:
        us_map(g, CX, 800, 1.05, t, 0.0, seg(t, L[2], L[3]) if t > L[2] - 0.2 else 0.0)
        if t < L[1] - 0.2:
            g.label("ย้อนกลับไป...", CX, 380, 100, sc=ap(t, 0.2), rot=-3)
        elif t < L[2] - 0.2:
            g.line([(CX - 380, 1060), (CX + 370, 1060)], 8, RED, amp=0)
            g.label("3,000+ กม.", CX, 1120, 64, color=RED, sc=ap(t, L[1] + 0.3))
            g.label("ห่างกันกว่า 3,000 กิโลเมตร", CX, 380, 74, color=NAVY, sc=ap(t, L[1]), rot=-3)
        else:
            g.label("ทะเลทราย ภูเขาหิมะ ป่าเถื่อน", CX, 380, 70, color=BROWN, sc=ap(t, L[2]), rot=-3)
        return
    if t < L[4] - 0.2:   # เรือ/เกวียน นานนับเดือน
        prairie(g, t)
        wagon(g, lerp(150, 420, seg(t, L[3], L[4])), GROUND, 1.0, t)
        with g.at(800, 640, ap(t, L[3] + 0.4)):
            g.rrect(-150, -110, 300, 220, 20, WHITE, 7)
            g.rrect(-150, -110, 300, 60, 20, RED, 7)
            g.label("นับเดือน", 0, 30, 60)
        envelope(g, 800, 950, 0.8 * ap(t, L[3] + 0.8))
        g.label("ส่งจดหมายใช้เวลานับเดือน", CX, 380, 76, sc=ap(t, L[3]), rot=-3)
        return
    prairie(g, t, 300)   # โพนี เอ็กซ์เพรส!
    g.sunburst(CX, 820, 220, 560, 18, t * 10, 10, (0.98, 0.8, 0.4, 0.5))
    horse(g, CX - 30, GROUND, 0.95, t, 1.0)
    g.label('"โพนี เอ็กซ์เพรส"!', CX, 360, 100, color=BROWN, sc=ap(t, L[4]), rot=-3)
    g.label("Pony Express (1860)", CX, 480, 52, color=GREY, sc=ap(t, L[4] + 0.4))


# ------------------------------------------------------------------ 3. riders
def s_riders(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[3] - 0.2:   # ควบม้าเต็มฝีเท้า / ฝ่าพายุหิมะ / 10 วัน
        prairie(g, t, 400)
        horse(g, 520 + 30 * math.sin(t), GROUND, 0.9, t, 1.0)
        for i in range(3):
            u = (t * 1.5 + i / 3) % 1
            g.circle(200 - 300 * u, GROUND - 40 - 30 * u, 30 + 30 * u, (0.85, 0.75, 0.55, 0.5 * (1 - u)), 0)
        if t < L[1] - 0.2:
            g.label("เด็กหนุ่มใจกล้า", CX, 380, 96, color=BROWN, sc=ap(t, 0.2), rot=-3)
        elif t < L[2] - 0.2:
            for i in range(20):
                u = (t * 0.6 + i * 0.05) % 1
                g.circle((i * 97) % 1100, 300 + 900 * u, 8, (0.85, 0.9, 1.0, 0.9), 2)
            g.label("วันละร้อยกิโลเมตร ฝ่าพายุหิมะ", CX, 380, 66, color=NAVY, sc=ap(t, L[1]), rot=-3)
        else:
            with g.at(850, 620, ap(t, L[2] + 0.3)):
                g.circle(0, 0, 120, WHITE, 8)
                g.label("10", 0, -14, 100, color=RED)
                g.label("วัน", 0, 66, 36, color=GREY)
            g.label("ข้ามทวีปใน 10 วัน!", CX, 380, 90, color=RED, sc=ap(t, L[2]), rot=-3)
        return
    if t < L[4] - 0.2:   # ฮีโร่ของชาติ
        for i, lk in enumerate(TOWNS):
            person(g, 160 + i * 230, GROUND, lk, 0.55, mood="smile", pose="wave", turn=0.4, seed=10 + i,
                   shadow=False)
        horse(g, 820, GROUND, 0.6, t, 0.3)
        g.label("ฮีโร่ของคนทั้งประเทศ", CX, 380, 86, color=GOLDTXT, sc=ap(t, L[3]), rot=-3)
        return
    prairie(g, t, 300)   # ไม่มีวันถูกโค่น
    horse(g, CX, GROUND, 0.9, t, 1.0)
    with g.at(CX, 620, ap(t, L[4] + 0.3) * (1 + 0.04 * math.sin(t * 4))):
        g.rrect(-220, -60, 440, 120, 30, WHITE, 7, stroke=GREEN)
        g.label("ไม่มีวันถูกโค่น!", 0, 0, 52, color=GREEN)
    if t < L[5] - 0.2:
        g.label("ใคร ๆ ก็คิดว่า...", CX, 380, 92, sc=ap(t, L[4]), rot=-3)
    else:
        g.label("ทรหดเกินใครจะล้ม", CX, 380, 88, color=BROWN, sc=ap(t, L[5]), rot=-3)


# ------------------------------------------------------------------ 4. wire
def s_wire(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[3] - 0.2:   # สายทองแดง + เสาไม้ ข้ามทวีป
        if t < L[1] - 0.2:
            with g.at(CX, 760, ap(t, 0.2), 4 * math.sin(t * 6)):
                g.label("!", 0, 0, 260, color=RED)
            g.label("แต่แล้ว...", CX, 380, 110, color=RED, sc=ap(t, 0.2), rot=-3)
            return
        if t < L[2] - 0.2:
            telegraph_line(g, 80, 1000, GROUND, t, 5, 0.0, 440, e_io(seg(t, L[1], L[2] - 0.3)))
            g.label("ลวดทองแดง + เสาไม้", CX, 380, 88, color=hexc("#a85a2a"), sc=ap(t, L[1]), rot=-3)
            return
        us_map(g, CX, 800, 1.05, t, e_io(seg(t, L[2], L[2] + 1.6)))
        g.label("โทรเลขข้ามทวีปสายแรก!", CX, 380, 84, color=GOLDTXT, sc=ap(t, L[2]), rot=-3)
        return
    if t < L[5] - 0.2:   # 10 วัน vs ไม่กี่วินาที
        telegraph_line(g, 80, 1000, GROUND - 330, t, 4, 1.0, 300)
        horse(g, 300 + 40 * math.sin(t), GROUND, 0.5, t, 0.8)
        g.label("10 วัน", 300, GROUND - 480, 54, color=BROWN, sc=ap(t, L[3] + 0.3))
        if t > L[4] - 0.2:
            g.label("ไม่กี่วินาที!", 760, 580, 64, color=GOLDTXT, sc=ap(t, L[4] + 0.2))
        if t < L[4] - 0.2:
            g.label("จากจดหมาย 10 วัน...", CX, 380, 84, color=BROWN, sc=ap(t, L[3]), rot=-3)
        else:
            g.label("รหัสมอร์สไม่กี่วินาที!", CX, 380, 84, color=RED, sc=ap(t, L[4]), rot=-3)
        return
    if t < L[6] - 0.2:   # ต่างกันราวฟ้ากับเหว
        for i, (txt, col, y) in enumerate((("โทรเลข: วินาที", GOLDTXT, 620), ("ม้าเร็ว: 10 วัน", BROWN, 980))):
            with g.at(CX, y, ap(t, L[5] + 0.3 * i)):
                g.rrect(-260, -70, 520, 140, 30, WHITE, 7, stroke=col)
                g.label(txt, 0, 0, 52, color=col)
        g.label("ต่างกันราวฟ้ากับเหว", CX, 380, 86, sc=ap(t, L[5]), rot=-3)
        return
    prairie(g, t)   # ล้าสมัยชั่วข้ามคืน
    horse(g, 520, GROUND, 0.8, t, 0.0 if t > L[7] - 0.2 else 0.3)
    telegraph_line(g, 80, 1000, GROUND - 600, t, 4, 1.0, 200)
    if t < L[7] - 0.2:
        g.label("ความกล้าหาญ หยาดเหงื่อ", CX, 380, 80, color=BROWN, sc=ap(t, L[6]), rot=-3)
    else:
        g.label("ล้าสมัยในชั่วข้ามคืน", CX, 380, 86, color=GREY, sc=ap(t, L[7]), rot=-3)


# ------------------------------------------------------------------ 5. closure
def s_closure(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[3] - 0.2:   # 2 วันหลัง / 18 เดือน / ยังไม่ถอนทุน
        if t < L[1] - 0.2:
            with g.at(CX, 760, ap(t, 0.2)):
                g.rrect(-200, -150, 400, 300, 20, WHITE, 8)
                g.rrect(-200, -150, 400, 80, 20, RED, 8)
                g.text("ตุลาคม 1861", 0, -110, 38, "kanit", WHITE)
                g.label("24 → 26", 0, 40, 90)
            g.label("เพียงสองวันต่อมา...", CX, 380, 90, sc=ap(t, 0.2), rot=-3)
        elif t < L[2] - 0.2:
            horse(g, 360, GROUND, 0.8, t, 0.2)
            with g.at(830, 640, ap(t, L[1] + 0.3)):
                g.circle(0, 0, 120, WHITE, 8)
                g.label("18", 0, -14, 100, color=BROWN)
                g.label("เดือน", 0, 66, 36, color=GREY)
            g.label("เปิดมาได้แค่ 18 เดือน", CX, 380, 84, color=BROWN, sc=ap(t, L[1]), rot=-3)
        else:
            horse(g, 360, GROUND, 0.8, t, 0.0)
            for i in range(4):
                u = (t * 0.5 + i / 4) % 1
                g.label("$", 760 + 60 * math.sin(i), 600 + 400 * u, 70, color=RED, a=1 - u)
            g.label("ยังไม่ทันถอนทุน", CX, 380, 90, color=RED, sc=ap(t, L[2]), rot=-3)
        return
    sign_closed(g, CX, 820, 1.3 * ap(t, L[3]), 4 * math.sin(t * 1.5))   # ปิดตัว
    horse(g, lerp(700, 1300, e_io(seg(t, L[4], d))), GROUND, 0.6, t, 0.4, flip=False)
    if t < L[4] - 0.2:
        g.label("ปิดตัวและล้มละลาย!", CX, 380, 90, color=RED, sc=ap(t, L[3]), rot=-3)
    else:
        g.label("เหลือเพียงตำนาน", CX, 380, 96, color=GOLDTXT, sc=ap(t, L[4]), rot=-3)


# ------------------------------------------------------------------ 6. lesson
def s_lesson(g, t, L, d):
    g.ground(GROUND, WHITE)
    g.label("บทเรียน", CX, 340, 100, sc=ap(t, 0.2), rot=-3)
    if t < L[2] - 0.2:   # คลื่นลูกใหม่ไม่รอใคร
        for i in range(3):
            ph = t * 2 + i
            x0 = (t * 160 + i * 400) % 1400 - 300
            pts = [(x0 + k * 30, 900 + i * 90 + 60 * math.sin(k * 0.5 + ph)) for k in range(12)]
            g.line(pts, 14, (0.35, 0.6, 0.85, 0.8), amp=0)
        if t > L[1] - 0.2:
            g.label("คลื่นเทคโนโลยีไม่รอใคร", CX, 490, 64, color=NAVY, sc=ap(t, L[1]))
        return
    horse(g, 330, GROUND, 0.6, t, 0.6)
    telegraph_line(g, 600, 1000, GROUND, t, 2, 1.0, 420)
    g.label("ต้านความเปลี่ยนแปลงไม่ได้", CX, 490, 62, color=RED, sc=ap(t, L[2]))


# ------------------------------------------------------------------ 7. outro
def s_outro(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[4] - 0.2:
        if t < L[1] - 0.2:
            horse(g, CX, GROUND, 0.8, t, 0.2)
            g.label("รู้สึกอย่างไร?", CX, 380, 100, sc=ap(t, 0.2), rot=-3)
            return
        chip(g, 780, 740 + 12 * math.sin(t * 2), 1.2 * ap(t, L[1]))
        person(g, 280, GROUND, OPERATOR, 0.72, mood="worry" if t > L[3] else "neutral",
               pose="think" if t > L[2] else "down", turn=0.3, seed=20)
        if t < L[2] - 0.2:
            g.label("ยุค AI เปลี่ยนโลก", CX, 380, 96, color=NAVY, sc=ap(t, L[1]), rot=-3)
        elif t < L[3] - 0.2:
            g.label("อาชีพ/ทักษะของเรา?", CX, 380, 90, sc=ap(t, L[2]), rot=-3)
        else:
            horse(g, 760, GROUND, 0.4, t, 0.6)
            g.label('จะเป็น "โพนี เอ็กซ์เพรส" ไหม?', CX, 380, 70, color=RED, sc=ap(t, L[3]), rot=-3)
        return
    with g.at(CX + 170, 640, ap(t, L[4])):   # ชวนคอมเมนต์
        g.bubble(0, 0, 460, 220, WHITE, tail=(-1, 1))
        for i in range(3):
            g.circle(-110 + i * 110, 0, 24 + 6 * math.sin(t * 6 - i), INK, 0)
    lincoln(g, 250, 0.72, "smile", "wave", 0.3)
    g.label("คอมเมนต์แลกเปลี่ยนกันได้เลย!", CX, 360, 70, color=RED, sc=ap(t, L[4]), rot=-3)


SCENES = {
    "hook": s_hook, "distance": s_distance, "riders": s_riders, "wire": s_wire, "closure": s_closure,
    "lesson": s_lesson, "outro": s_outro,
}
NO_IRIS = set()
