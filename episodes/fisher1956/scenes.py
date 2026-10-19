"""ฉากตอน: แครี ฟิชเชอร์ (เกิด 21 ต.ค. 1956) — ไม่ใช้โลโก้/ตัวอักษรภาพยนตร์ วาดเครื่องแต่งกายแบบทั่วไป"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from chars import (CARRIE, CARRIE_TEEN, EXECS, FANS, LEIA, PINK, blaster, book, camera, frame_box, heart,  # noqa: E402
                   microphone, pill, scale_weigh, space_panel, spotlight, stars, storm_cloud, tape)
from gfx import (GOLD, GOLD2, GREY, INK, LGREY, NAVY, RED, W, WHITE, e_io, e_out, hexc, lerp, pop,  # noqa: E402
                 seg)
from people import _rr, _shade, head, person  # noqa: E402
from photos import photo  # noqa: E402

CX = W / 2
GROUND = 1270
GOLDTXT = hexc("#b37a12")
GREEN = hexc("#3c8d4f")
PINKTXT = hexc("#d9608c")

CAMERA = {"hook": "push_in", "pain": "pan_right", "hollywood": "dutch", "fight": "push_in", "legacy": "tilt_up",
          "lesson": "pull_out", "outro": "push_in"}
TRANSITIONS = {"pain": "fade", "hollywood": "whip", "fight": "zoom", "legacy": "iris", "lesson": "fade"}


def ap(t, a, dur=0.38):
    return pop(t, a - 0.2, dur)


def crib(g, x, y, sc, t):
    c = g.c
    with g.at(x, y, sc, 3 * math.sin(t * 1.5)):
        c.new_path()
        c.arc(0, -80, 180, 0.15 * math.pi, 0.85 * math.pi)
        c.close_path()
        _shade(c, hexc("#f2c4d0"), 6, 0.25)
        g.circle(-60, -60, 46, hexc("#efc4a1"), 5)
        g.blob(30, -50, 110, 50, hexc("#f8dce4"), 5, 3)
        heart(g, 0, -260, 0.7, PINK)


# ------------------------------------------------------------------ 1. hook
def s_hook(g, t, L, d):
    if t < L[2] - 0.2:   # วันที่ + เด็กหญิงเกิด
        g.ground(GROUND, WHITE)
        crib(g, CX, 980, 1.2 * ap(t, L[1] + 0.3) if t > L[1] - 0.2 else 0.0, t)
        stars(g, t, 14, (60, 600, 1020, 1200))
        g.label("วันนี้ในอดีต", CX, 380, 104, sc=lerp(2.0, 1, e_out(seg(t, 0.1, 0.4))) if t > 0.1 else 0, rot=-4)
        g.label("21 ตุลาคม 1956", CX, 520, 84, color=RED, sc=pop(t, 0.8))
        return
    space_panel(g)   # สัญลักษณ์ความกล้าหาญของกาแล็กซี
    stars(g, t)
    g.ground(GROUND, WHITE)
    if t < L[3] - 0.2:
        g.sunburst(CX, 760, 200, 520, 20, t * 10, 10, (1, 0.9, 0.6, 0.5))
        with g.silhouette(INK, 0.9):
            person(g, CX, GROUND, LEIA, 0.92, seed=1)
        g.label("ความกล้าหาญแห่งกาแล็กซี", CX, 380, 66, color=GOLDTXT, sc=ap(t, L[2]), rot=-3)
        return
    if t < L[6] - 0.2:   # ปืนบลัสเตอร์ / มวยผม / ไม่กลัวจักรวรรดิ
        pose = "point" if t > L[3] - 0.2 else "down"
        person(g, 420, GROUND, LEIA, 0.92, mood="firm" if t < L[5] else "smug", pose=pose, turn=0.3, seed=1)
        blaster(g, 778, 692, 0.42 * ap(t, L[3]), 0, shot=seg(t, L[3] + 0.6, L[3] + 1.0) * (1 - seg(t, L[3] + 1.2, L[3] + 1.5)))
        if t > L[4] - 0.2:
            g.label("มวยผมซาลาเปา!", 760, 820, 60, color=PINKTXT, sc=ap(t, L[4]), rot=-4)
            with g.at(420, GROUND - 850 * 0.92 - 0, 1):
                for sx in (-1, 1):
                    g.sparkle(sx * 90, 0, 18 * ap(t, L[4] + 0.2), GOLD2)
        if t > L[5] - 0.2:
            g.label("ไม่กลัวจักรวรรดิใด ๆ", CX, 1180, 60, color=GOLDTXT, sc=ap(t, L[5]))
        g.label("เจ้าหญิงนักสู้", CX, 380, 84, color=GOLDTXT, sc=ap(t, L[3]), rot=-3)
        return
    k = ap(t, L[6])   # แครี ฟิชเชอร์!
    g.sunburst(CX, 760, 220, 620, 22, t * 12, 12, (1, 0.9, 0.6, 0.7))
    person(g, CX, GROUND, LEIA, 0.92, mood="smile", pose="wave", turn=0.15, seed=1)
    g.label('"แครี ฟิชเชอร์"!', CX, 370, 96, color=GOLDTXT, sc=k, rot=-4)
    g.name_tag(t, L[6] - 0.1, 800, 1120, "แครี ฟิชเชอร์", "นักแสดง · นักเขียน (1956–2016)", side=-1)


# ------------------------------------------------------------------ 2. pain
def s_pain(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:   # เบื้องหลังรอยยิ้ม (ภาพจริง ถ้ามี)
        if not photo(g, "carrie_portrait", CX, 790, 720, 600, -2, ap(t, 0.2), 1.0 + 0.04 * t,
                     label="แครี ฟิชเชอร์ ในบทเจ้าหญิงเลอา"):
            with g.at(CX, 760, 1.9):
                head(g, LEIA, "smile" if t < 2.0 else "sad", turn=0.1)
        g.label("เบื้องหลังรอยยิ้ม...", CX, 360, 80, sc=ap(t, 0.2), rot=-3)
        return
    if t < L[2] - 0.2:   # มรสุมชีวิต
        storm_cloud(g, CX, 470, 1.1, t, seg(t, L[1] + 0.6, L[1] + 0.9))
        person(g, CX, GROUND, CARRIE_TEEN, 0.68, mood="sad", pose="down", turn=0.1, seed=2)
        g.label("มรสุมและความเจ็บปวด", CX, 360, 72, color=NAVY, sc=ap(t, L[1]), rot=-3)
        return
    if t < L[3] - 0.2:   # ครอบครัวคนดัง แสงสีโหดร้าย
        for i, (x, a) in enumerate(((120, -20), (960, 20), (540, 0))):
            spotlight(g, x, 300, a + 6 * math.sin(t * 1.5 + i))
        person(g, CX, GROUND, CARRIE_TEEN, 0.75, mood="worry", pose="down", turn=0.0, seed=2)
        for i in range(3):
            fl = max(0.0, 1 - abs(((t * 1.3 + i * 0.37) % 1) - 0.1) / 0.1)
            camera(g, 180 + i * 360, 1120, 0.6, fl)
        g.label("ครอบครัวคนดัง", CX, 360, 80, color=GOLDTXT, sc=ap(t, L[2]), rot=-3)
        return
    # ไบโพลาร์ + ยาเสพติด (สื่อด้วยสัญลักษณ์)
    sw = math.sin(t * 2.2)
    with g.at(CX, 760):
        g.circle(-170, 0, 130, hexc("#f2c230"), 6)
        g.circle(170, 0, 130, hexc("#9fb4d6"), 6)
        g.label("สูง", -170, 0, 56)
        g.label("ต่ำ", 170, 0, 56)
        g.line([(-170 * sw, -200), (-170 * sw, 200)], 8, RED, amp=0)
    for i in range(4):
        pill(g, 200 + i * 230, 1100 + 20 * math.sin(t * 2 + i), 30 * i - 40, 0.9 * ap(t, L[3] + 1.0 + i * 0.2))
    g.label("ไบโพลาร์ · ยาเสพติด", CX, 360, 76, color=NAVY, sc=ap(t, L[3]), rot=-3)


# ------------------------------------------------------------------ 3. hollywood
def s_hollywood(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:   # ถูกตราหน้า / มาตรฐานความงาม
        person(g, CX, GROUND, CARRIE, 0.82, mood="worry", pose="down", turn=0.0, seed=3)
        for i, (x, y, r, s) in enumerate(((290, 520, -12, "ไม่สวยพอ"), (800, 640, 10, "ไม่ผอมพอ"), (300, 920, 6, "ต้องเพอร์เฟกต์"))):
            if t > 0.4 + i * 0.6:
                with g.at(0, 0, 1):
                    tape(g, x, y, 300, r, s)
        g.label("มาตรฐานความงาม", CX, 360, 80, color=RED, sc=ap(t, 0.2), rot=-3)
        return
    if t < L[2] - 0.2:   # บังคับลดน้ำหนัก
        for i, lk in enumerate(EXECS):
            person(g, 170 + i * 760, GROUND, lk, 0.7, mood="angry", pose="point", turn=0.4 - 0.8 * i, seed=10 + i, talk=True)
        scale_weigh(g, CX, GROUND, 1.1, 0.5 + 0.3 * math.sin(t * 3))
        g.label("ต้องลดน้ำหนัก!", CX, 360, 86, color=RED, sc=ap(t, L[1]), rot=-4)
        return
    person(g, CX, GROUND, LEIA, 0.85, mood="sad", pose="down", turn=0.0, seed=1)   # แค่สัญลักษณ์ทางเพศ
    for i in range(4):
        fl = max(0.0, 1 - abs(((t * 1.1 + i * 0.29) % 1) - 0.1) / 0.1)
        camera(g, 150 + (i % 2) * 780, 640 + (i // 2) * 360, 0.55, fl)
    g.label("แค่ภาพลักษณ์?", CX, 360, 86, color=RED, sc=ap(t, L[2]), rot=-3)
    g.label("ไม่ใช่แค่ฝีมือการแสดง", CX, 1180, 54, color=GREY, sc=ap(t, L[2] + 0.8))


# ------------------------------------------------------------------ 4. fight
def s_fight(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # ไม่ยอมจำนน / อารมณ์ขันเป็นอาวุธ
        person(g, CX, GROUND, CARRIE, 0.85, mood="firm" if t < L[1] else "smug", pose="fist", turn=0.1, seed=3)
        if t < L[1] - 0.2:
            g.label("ไม่ยอมจำนน!", CX, 360, 96, color=RED, sc=ap(t, 0.2), rot=-4)
        else:
            for i, s in enumerate(("ฮา!", "แสบ!", "จริง!")):
                g.label(s, 230 + i * 310, 640 + 30 * math.sin(t * 3 + i), 70, color=[GOLDTXT, PINKTXT, GREEN][i],
                        sc=ap(t, L[1] + 0.3 + i * 0.3), rot=(i - 1) * 8)
            g.label("อารมณ์ขันคืออาวุธ", CX, 360, 76, sc=ap(t, L[1]), rot=-3)
        return
    if t < L[4] - 0.2:   # พูดความจริงเรื่องซึมเศร้า/เสพติด เพื่อช่วยผู้อื่น
        microphone(g, 760, 700, 1.0)
        person(g, 380, GROUND, CARRIE, 0.85, mood="smile", pose="hold", turn=0.3, seed=3, talk=True)
        book(g, 860, 1080, 0.7 * ap(t, L[2] + 0.6), 6)
        if t < L[3] - 0.2:
            g.label("พูดความจริงอย่างเปิดเผย", CX, 360, 72, sc=ap(t, L[2]), rot=-3)
        else:
            g.label("เพื่อช่วยคนอื่น", CX, 360, 84, color=GREEN, sc=ap(t, L[3]), rot=-3)
        return
    if t < L[5] - 0.2:   # กระบอกเสียงของคนตัวเล็ก
        microphone(g, CX, 640, 0.8)
        for i, lk in enumerate(FANS):
            x = 140 + i * 260
            person(g, x, GROUND, lk, 0.55, mood="smile", pose="wave" if (int(t * 2) + i) % 2 else "down",
                   turn=0.2 * (1.5 - i), seed=20 + i)
        for i in range(3):
            u = (t * 0.8 + i / 3) % 1
            g.arc(CX, 560, 80 + 200 * u, math.radians(200), math.radians(340), 6, (*GOLD[:3], 1 - u))
        g.label("กระบอกเสียงของคนตัวเล็ก", CX, 360, 70, color=GOLDTXT, sc=ap(t, L[4]), rot=-3)
        return
    k = e_io(seg(t, L[5], L[5] + 1.6))   # ทวงคืนความเท่าเทียม: ตาชั่งสมดุล
    tilt = lerp(-18, 0, k) + 2 * math.sin(t * 2)
    with g.at(CX, 760, 1, tilt):
        g.line([(-320, 0), (320, 0)], 12, INK, amp=0)
        for sx, lbl in ((-1, "เธอ"), (1, "เขา")):
            g.line([(sx * 300, 0), (sx * 300, 120)], 4, INK, amp=0)
            g.poly([(sx * 300 - 90, 120), (sx * 300 + 90, 120), (sx * 300 + 60, 170), (sx * 300 - 60, 170)],
                   GOLD if sx < 0 else LGREY, 6)
            g.label(lbl, sx * 300, 230, 50)
    g.poly([(CX - 40, 1180), (CX, 770), (CX + 40, 1180)], hexc("#a8763e"), 6)
    if t < L[6] - 0.2:
        g.label("ทวงคืนความเท่าเทียม", CX, 360, 76, color=GREEN, sc=ap(t, L[5]), rot=-3)
    else:
        g.label("แสบ · จริงใจ · ไม่เหมือนใคร", CX, 360, 66, color=PINKTXT, sc=ap(t, L[6]), rot=-3)


# ------------------------------------------------------------------ 5. legacy
def s_legacy(g, t, L, d):
    space_panel(g)
    stars(g, t, 40)
    g.ground(GROUND, WHITE)
    k = ap(t, 0.3)
    with g.alpha(lerp(1.0, 0.75, seg(t, 0.4, 2.0))):
        person(g, CX, GROUND, LEIA, 0.85, mood="smile", pose="salute" if t > L[1] else "down", turn=0.1, seed=1)
    for i in range(8):
        a = t * 0.5 + i * math.pi / 4
        g.sparkle(CX + 380 * math.cos(a), 760 + 300 * math.sin(a), 16 + 6 * math.sin(t * 4 + i), GOLD2)
    if t < L[1] - 0.2:
        g.label("จากไปในปี 2016", CX, 380, 76, color=NAVY, sc=k, rot=-3)
    elif t < L[2] - 0.2:
        g.label("จิตวิญญาณและรอยยิ้ม", CX, 380, 74, color=GOLDTXT, sc=ap(t, L[1]), rot=-3)
    else:
        g.label("ส่องประกายตลอดไป", CX, 380, 80, color=GOLDTXT, sc=ap(t, L[2]), rot=-3)
        for i in range(5):
            heart(g, 160 + i * 190, 1180 + 15 * math.sin(t * 3 + i), 0.6 * ap(t, L[2] + 0.3 + i * 0.15), PINK)


# ------------------------------------------------------------------ 6. lesson
def s_lesson(g, t, L, d):
    g.ground(GROUND, WHITE)
    g.label("บทเรียน", CX, 340, 100, sc=ap(t, 0.2), rot=-3)
    brk = e_out(seg(t, L[3] + 0.4, L[3] + 1.6))
    if t < L[2] - 0.2:   # ความงามไม่ใช่ความไร้ที่ติ
        with g.at(CX, 780, ap(t, 0.4)):
            g.rrect(-220, -280, 440, 560, 30, (0.95, 0.97, 1, 1), 8)
            with g.at(0, 20, 1.3):
                head(g, CARRIE, "smile", turn=0.1)
        if t > L[1] - 0.2:
            for i in range(3):
                g.line([(CX - 120 + i * 70, 560), (CX - 80 + i * 70, 640)], 5, GREY, amp=0)
            g.label("ไม่ต้องไร้ที่ติ", CX, 1160, 66, color=PINKTXT, sc=ap(t, L[1]))
        return
    frame_box(g, CX, 800, 560, 640, brk)   # กล้าเป็นตัวเอง แม้โลกจะตีกรอบ
    person(g, CX, GROUND, CARRIE, 0.7, mood="smile" if brk > 0.5 else "firm", pose="v" if brk > 0.5 else "down",
           turn=0.0, seed=3)
    if t < L[3] - 0.2:
        g.label("กล้าเป็นตัวของตัวเอง", CX, 1180, 64, color=GOLDTXT, sc=ap(t, L[2]))
    else:
        g.label("แม้โลกจะตีกรอบ", CX, 1180, 64, color=NAVY, sc=ap(t, L[3]))


# ------------------------------------------------------------------ 7. outro
def s_outro(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[3] - 0.2:   # เลอา หรือ แครีตัวจริง?
        person(g, 270, GROUND, LEIA, 0.75, mood="smile", pose="down", turn=0.3, seed=1)
        person(g, 810, GROUND, CARRIE, 0.75, mood="smile", pose="down", turn=-0.3, seed=3)
        g.label("หรือ", CX, 760, 64, color=GREY, sc=ap(t, L[1] + 0.3))
        if t < L[2] - 0.2:
            g.label("บนจอ · นอกจอ", CX, 360, 80, sc=ap(t, L[1]), rot=-3)
        else:
            heart(g, CX, 560, 1.2 * ap(t, L[2]) * (1 + 0.08 * math.sin(t * 6)), PINK)
            g.label("แรงบันดาลใจของคุณ?", CX, 360, 76, color=PINKTXT, sc=ap(t, L[2]), rot=-3)
        return
    with g.at(CX + 120, 650, ap(t, L[3])):   # ชวนคอมเมนต์
        g.bubble(0, 0, 520, 240, WHITE, tail=(-1, 1))
        for i in range(3):
            g.circle(-110 + i * 110, 0, 24 + 6 * math.sin(t * 6 - i), INK, 0)
    person(g, 250, GROUND, CARRIE, 0.75, mood="smile", pose="wave", turn=0.3, seed=3, talk=True)
    for i in range(5):
        g.sparkle(160 + i * 190, 1180 + 20 * math.sin(t * 3 + i), 14 * ap(t, L[3] + 0.5 + i * 0.2), GOLD2)
    g.label("คอมเมนต์คุยกันได้เลย!", 700, 1000, 58, color=RED, sc=ap(t, L[3] + 0.4))


SCENES = {
    "hook": s_hook, "pain": s_pain, "hollywood": s_hollywood, "fight": s_fight, "legacy": s_legacy,
    "lesson": s_lesson, "outro": s_outro,
}
NO_IRIS = set()
