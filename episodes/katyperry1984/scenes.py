"""ฉากตอน: เคที เพร์รี (เกิด 25 ต.ค. 1984) — สไตล์ป๊อปทันสมัย (เจ้าของช่องขอ)
- หัวข้อมีแถบไฮไลต์นีออนปาดเข้าจากซ้าย (ตัวหนังสือยังเป็น g.label ดำขอบขาว)
- การ์ดสติกเกอร์ขอบดำเงาสีเยื้อง, ของเด้งแบบ overshoot, คอนเฟตติพาสเทลบนพื้นขาว"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from chars import (CANDY, EXECS, GRAPE, KATY, KATY_GOSPEL, KATY_LA, LEMON, MINT, MOM, PASTOR, PINK, SKYB,  # noqa: E402
                   bill, car, cd, chart, church, confetti, contract, crown, cupcake, curtain, glove, guitar,
                   hollywood, lollipop, mic, phone, spotlight, sticker, suitcase, tear_drops)
from gfx import GOLD, GOLD2, GREY, INK, NAVY, RED, W, WHITE, e_back, e_io, e_out, hexc, lerp, pop, seg  # noqa: E402
from people import person  # noqa: E402

CX = W / 2
GROUND = 1270

CAMERA = {"hook": "push_in", "born": "pan_right", "la": "dutch", "boom": "push_in", "tears": "pan_left",
          "lesson": "pull_out", "outro": "pan_right"}
TRANSITIONS = {"born": "zoom", "la": "whip", "boom": "zoom", "tears": "fade", "lesson": "whip", "outro": "zoom"}


def ap(t, a, dur=0.38):
    return pop(t, a - 0.2, dur)


def bounce(t, a, dur=0.45):
    """เด้งแบบ overshoot เร็ว ๆ (สไตล์รีลสมัยใหม่)"""
    if t < a - 0.2:
        return 0.0
    return e_back(min(1.0, (t - a + 0.2) / dur))


def kicker(g, t, a, txt, hl=PINK, size=80, y=370, rot=-2):
    """หัวข้อ + แถบไฮไลต์นีออนปาดจากซ้าย"""
    u = e_out(seg(t, a - 0.2, a + 0.15))
    if u <= 0:
        return
    from gfx import text_sprite
    _, _, w, h = text_sprite(txt, size, "kanit", INK, 8, WHITE)
    with g.at(CX, y, 1, rot):
        bw = (w + 50) * u
        g.rrect(-w / 2 - 25, -h * 0.05, bw, h * 0.5, 14, (*hl[:3], 0.85), 0)
    g.label(txt, CX, y, size, sc=bounce(t, a), rot=rot)


def chip(g, t, a, x, y, txt, shadow=MINT, size=54, rot=0.0, w=None):
    k = bounce(t, a)
    if k < 0.02:
        return
    ww = w or (len(txt) * size * 0.42 + 90)
    with g.at(x, y, k, rot):
        sticker(g, 0, 0, ww, size * 2.0, WHITE, shadow, 1.0, 0, 30, 6)
        g.label(txt, 0, 0, size)


def bg(g, t, seed=0):
    g.ground(GROUND, WHITE)
    confetti(g, t, 14, seed)


# ------------------------------------------------------------------ 1. hook
def s_hook(g, t, L, d):
    bg(g, t)
    if t < L[1] - 0.2:
        mic(g, CX, 860, 1.6 * bounce(t, 0.3) + 0.01, 8 * math.sin(t * 3))
        g.label("วันนี้ในอดีต", CX, 380, 104, sc=bounce(t, 0.15), rot=-3)
        chip(g, t, 0.7, CX, 530, "25 ตุลาคม 1984", LEMON, 56)
        return
    if t < L[3] - 0.2:   # ครอบครัวบาทหลวง ห้ามเพลงป๊อป
        church(g, 840, GROUND, 0.5, t, 0.0)
        person(g, 300, GROUND, KATY_GOSPEL, 0.75, mood="sad" if t > L[2] - 0.2 else "neutral", pose="down",
               turn=0.3, seed=1)
        if t < L[2] - 0.2:
            kicker(g, t, L[1], "ครอบครัวบาทหลวงเคร่งศาสนา", LEMON, 72)
        else:
            with g.at(560, 640, bounce(t, L[2])):
                g.circle(0, 0, 110, WHITE, 10, stroke=RED)
                g.label("POP", 0, 0, 64, color=PINK)
                g.line([(-78, -78), (78, 78)], 14, RED, amp=0)
            kicker(g, t, L[2], "ห้ามฟังเพลงป๊อปเด็ดขาด!", PINK, 80)
        return
    if t < L[4] - 0.2:   # ฉีกสัญญา 3 ครั้ง
        for i in range(3):
            k = bounce(t, L[3] + 0.35 * i)
            if k > 0.02:
                contract(g, 220 + i * 320, 820 + 14 * math.sin(t * 2.2 + i), 0.6 * k, -8 + 8 * i + 4 * math.sin(t * 1.7 + i), e_io(seg(t, L[3] + 0.35 * i + 0.3,
                                                                              L[3] + 0.35 * i + 0.8)))
        chip(g, t, L[3] + 0.6, CX, 1130, "ฉีกสัญญา × 3", PINK, 64)
        kicker(g, t, L[3], "ถูกค่ายเพลงทิ้ง 3 ครั้งติด!", SKYB, 78)
        return
    person(g, 300, GROUND, KATY, 0.8, mood="smile", pose="v" if t > L[5] - 0.2 else "wave", turn=0.3, seed=2)
    if t < L[5] - 0.2:
        glove(g, 780, 800, 1.0 * bounce(t, L[4]) + 0.01, 8 * math.sin(t * 2), t)
        kicker(g, t, L[4], "สถิติเทียบชั้นไมเคิล แจ็กสัน", LEMON, 72)
    else:
        crown(g, 300, 470, 0.9 * bounce(t, L[5]) + 0.01, 6 * math.sin(t * 3))
        chart(g, 780, 860, 0.55, e_out(seg(t, L[5], L[5] + 1.2)), t)
        kicker(g, t, L[5], "ราชินีเพลงป๊อปของโลก!", PINK, 84)


# ------------------------------------------------------------------ 2. born
def s_born(g, t, L, d):
    bg(g, t, 3)
    if t < L[3] - 0.2:   # เกิด 1984 แคทเธอรีน ฮัดสัน = เคที เพร์รี
        if t < L[1] - 0.2:
            g.calendar(CX, 820, 1.1 * bounce(t, 0.2) + 0.01, "25", "พฤหัส", "ต.ค. 1984")
            kicker(g, t, L[0], "25 ตุลาคม 1984", LEMON, 92)
        elif t < L[2] - 0.2:
            person(g, CX, GROUND, KATY_GOSPEL, 0.8, mood="smile", pose="wave", turn=0, seed=1)
            chip(g, t, L[1], CX, 520, "แคทเธอรีน ฮัดสัน", MINT, 60)
            kicker(g, t, L[1], "ชื่อจริงของเธอคือ...", SKYB, 80)
        else:
            person(g, 290, GROUND, KATY, 0.85, mood="smile", pose="v", turn=0.3, seed=2)
            g.name_tag(t, L[2] + 0.1, 760, 1140, "เคที เพร์รี", "นักร้องป๊อป (เกิด 1984)")
            mic(g, 760, 760, 0.9 * bounce(t, L[2] + 3.5) + 0.01, -10)   # รอป้ายชื่อ+ภาพจริงหายก่อน
            kicker(g, t, L[2], "\"เคที เพร์รี\"", PINK, 100)
        return
    if t < L[6] - 0.2:   # คำสอนเข้มงวด เพลงสรรเสริญเท่านั้น
        church(g, 800, GROUND, 0.55, t, 1.0 if t > L[4] - 0.2 else 0.0)
        person(g, 200, GROUND, PASTOR, 0.7, mood="firm", pose="stop", turn=0.4, seed=3)
        person(g, 470, GROUND, KATY_GOSPEL, 0.6, mood="neutral" if t < L[4] - 0.2 else "smile", pose="hold",
               turn=0.3, seed=1)
        if t < L[4] - 0.2:
            kicker(g, t, L[3], "กรอบคำสอนอันเข้มงวด", LEMON, 82)
        else:
            chip(g, t, L[4] + 0.3, 800, 520, "เพลงโบสถ์เท่านั้น", MINT, 50)
            kicker(g, t, L[4], "เพลงเดียวที่ร้องได้...", SKYB, 82, y=340)
        return
    if t < L[7] - 0.2:   # อัลบั้มกอสเปลอายุ 16
        guitar(g, 300, 1100, 1.1, -12 + 4 * math.sin(t * 3))
        cd(g, 760, 780, 170 * bounce(t, L[6]) + 1, t, "", LEMON)
        chip(g, t, L[6] + 0.4, 760, 1050, "อัลบั้มกอสเปล · 16 ปี", LEMON, 50)
        kicker(g, t, L[6], "อัลบั้มแรกในชีวิต", MINT, 86)
        return
    cd(g, 720, 800, 150, t * 0.2, "", hexc("#c9ced6"))
    with g.at(720, 800, bounce(t, L[7] + 0.3), -12):
        sticker(g, 0, 0, 420, 130, WHITE, RED, 1.0, 0, 26, 6)
        g.label("ขายได้ ~200 แผ่น", 0, 0, 52, color=RED)
    person(g, 230, GROUND, KATY_GOSPEL, 0.75, mood="sad", pose="down", turn=0.4, seed=1)
    kicker(g, t, L[7], "ล้มเหลวไม่เป็นท่า!", RED, 90)


# ------------------------------------------------------------------ 3. la
def s_la(g, t, L, d):
    bg(g, t, 5)
    if t < L[2] - 0.2:   # ไม่ยอมแพ้ แบกกระเป๋าไป LA
        if t > L[1] - 0.2:
            hollywood(g, GROUND, t)
        u = e_io(seg(t, L[1], L[2]))
        person(g, lerp(250, 520, u), GROUND, KATY_LA, 0.8, mood="firm", pose="fist", turn=0.6, seed=4)
        suitcase(g, lerp(380, 650, u), GROUND, 0.8)
        if t < L[1] - 0.2:
            kicker(g, t, L[0], "แต่เคทีไม่ยอมแพ้!", PINK, 92)
        else:
            kicker(g, t, L[1], "บุกลอสแอนเจลิส ไล่ล่าฝัน!", LEMON, 78)
        return
    if t < L[4] - 0.2:   # ฝันร้าย: ค่ายใหญ่ฉีกสัญญา 3 ค่าย
        for i, (logo, col) in enumerate((("ค่ายที่ 1", PINK), ("ค่ายที่ 2", SKYB), ("ค่ายที่ 3", GRAPE))):
            k = bounce(t, L[3] + 0.4 * i) if t > L[3] - 0.2 else (1.0 if i == 0 else 0.0)
            if k < 0.02:
                continue
            contract(g, 220 + i * 320, 800 + 14 * math.sin(t * 2.2 + i), 0.62 * k, -8 + 8 * i + 4 * math.sin(t * 1.7 + i),
                     e_io(seg(t, L[3] + 0.4 * i + 0.3, L[3] + 0.4 * i + 0.8)), logo)
        if t < L[3] - 0.2:
            kicker(g, t, L[2], "เส้นทางกลายเป็นฝันร้าย", GRAPE, 82)
        else:
            chip(g, t, L[3] + 1.4, CX, 1140, "ฉีกทิ้ง × 3 ค่าย", PINK, 60)
            kicker(g, t, L[3], "เซ็นแล้วฉีกทิ้งซ้ำแล้วซ้ำเล่า!", RED, 74)
        return
    if t < L[6] - 0.2:   # รถถูกยึด / ไม่มีค่าเช่า
        if t < L[5] - 0.2:
            car(g, lerp(500, 760, e_io(seg(t, L[4] + 0.3, L[5]))), 1050, 1.2, 1.0, t)
            chip(g, t, L[4] + 0.3, CX, 560, "ยึดรถ!", RED, 70)
            kicker(g, t, L[4], "รถยนต์ถูกยึด", SKYB, 92)
        else:
            bill(g, 720, 820, 1.2 * bounce(t, L[5]) + 0.01, 8 * math.sin(t * 2), t)
            person(g, 260, GROUND, KATY_LA, 0.8, mood="worry", pose="shrug", turn=0.4, seed=4)
            kicker(g, t, L[5], "ไม่มีเงินจ่ายค่าเช่าห้อง", LEMON, 80)
        return
    for i in range(3):   # คนในวงการตราหน้า + ยุคบริตนีย์
        person(g, 160 + i * 220, GROUND, EXECS[i], 0.55, mood="smug", pose="cross" if i == 1 else "point",
               turn=0.3, seed=10 + i)
    person(g, 900, GROUND, KATY_LA, 0.6, mood="sad", pose="down", turn=-0.4, seed=4)
    if t < L[7] - 0.2:
        chip(g, t, L[6] + 0.3, CX, 560, "\"ไม่มีวันดังหรอก!\"", RED, 56)
        kicker(g, t, L[6], "ถูกตราหน้าว่าไม่มีวันดัง", RED, 80)
    else:
        crown(g, CX, 560, 0.8 * bounce(t, L[7]) + 0.01, -10)
        chip(g, t, L[7] + 0.3, CX, 700, "ยุคบริตนีย์ครองเมือง", LEMON, 52)
        kicker(g, t, L[7], "ยุคที่บริตนีย์ สเปียส์ครองเมือง!", PINK, 72)


# ------------------------------------------------------------------ 4. boom
def s_boom(g, t, L, d):
    bg(g, t, 7)
    if t < L[2] - 0.2:   # 2008 ระเบิดความกล้า
        person(g, CX, GROUND, KATY, 0.85, mood="smile", pose="v" if t > L[1] - 0.2 else "fist", turn=0, seed=2)
        if t > L[1] - 0.2:
            for i in range(10):
                a = i * 0.63 + t
                r = 380 * e_out(seg(t, L[1] - 0.2, L[1] + 0.6))
                g.star(CX + r * math.cos(a), 760 + r * 0.8 * math.sin(a), 30, CANDY[i % 5], 4)
        if t < L[1] - 0.2:
            chip(g, t, L[0], CX, 520, "2008", LEMON, 90)
            kicker(g, t, L[0], "จนกระทั่งปี...", SKYB, 84)
        else:
            kicker(g, t, L[1], "ความกล้าฉีกกรอบระเบิดออกมา!", PINK, 72)
        return
    if t < L[4] - 0.2:   # I Kissed a Girl -> อันดับ 1
        cd(g, 720, 800, 200 * bounce(t, L[2]) + 1, t, "", PINK)
        mic(g, 260, 900, 1.1, -12)
        if t < L[3] - 0.2:
            chip(g, t, L[2] + 0.3, 720, 1100, "I Kissed a Girl", PINK, 56)
            kicker(g, t, L[2], "ซิงเกิลสุดแสบ จุดชนวนดราม่า!", RED, 72)
        else:
            with g.at(720, 560, bounce(t, L[3]), -8):
                g.circle(0, 0, 110, LEMON, 8)
                g.label("#1", 0, 0, 110)
            kicker(g, t, L[3], "พุ่งขึ้นอันดับ 1 ชั่วข้ามคืน!", LEMON, 76)
        return
    if t < L[6] - 0.2:   # Teenage Dream + 5 เพลงอันดับ 1
        if t < L[5] - 0.2:
            with g.at(CX, 820, bounce(t, L[4]), 4 * math.sin(t * 2)):
                sticker(g, 0, 0, 520, 520, hexc("#bfe8ff"), PINK, 1.0, 0, 30, 8)
                lollipop(g, -120, 120, 0.8, -15, t, PINK)
                cupcake(g, 120, 120, 0.8, t)
                g.label("Teenage Dream", 0, -170, 60)
            kicker(g, t, L[4], "อัลบั้มประวัติศาสตร์!", GRAPE, 86)
        else:
            chart(g, CX, 900, 0.75, e_out(seg(t, L[5] - 0.2, L[5] + 2.0)), t)
            kicker(g, t, L[5], "5 เพลงอันดับ 1 จากอัลบั้มเดียว!", LEMON, 72)
        return
    glove(g, 300, 800, 1.1, -8 + 6 * math.sin(t * 2), t)   # เทียบไมเคิล แจ็กสัน / ศิลปินหญิงคนแรก
    g.label("=", CX, 800, 140, color=PINK, sc=bounce(t, L[6] + 0.3))
    crown(g, 780, 800, 1.2 * bounce(t, L[6] + 0.5) + 0.01, 6 * math.sin(t * 3))
    if t < L[7] - 0.2:
        chip(g, t, L[6] + 0.2, 300, 1080, "Bad (1987)", SKYB, 50)
        chip(g, t, L[6] + 0.7, 780, 1080, "Teenage Dream (2010)", PINK, 44)
        kicker(g, t, L[6], "เทียบเท่าราชาเพลงป๊อป!", LEMON, 80)
    else:
        chip(g, t, L[7] + 0.2, CX, 1100, "ศิลปินหญิงคนเดียวในประวัติศาสตร์", MINT, 48)
        kicker(g, t, L[7], "ยังไม่มีศิลปินหญิงคนไหนทำได้!", PINK, 74)


# ------------------------------------------------------------------ 5. tears
def s_tears(g, t, L, d):
    if t < L[2] - 0.2:   # แสงสีลูกกวาด -> น้ำตา
        bg(g, t, 9)
        person(g, 300, GROUND, KATY, 0.85, mood="smile" if t < L[1] - 0.2 else "sad", pose="v" if t < L[1] - 0.2
               else "down", turn=0.3, seed=2)
        if t < L[1] - 0.2:
            lollipop(g, 760, 900, 1.0, 10 * math.sin(t * 2), t, MINT)
            cupcake(g, 900, 1200, 0.8, t)
            kicker(g, t, L[0], "เบื้องหลังคอสตูมลูกกวาด...", PINK, 76)
        else:
            tear_drops(g, 340, 470, t, 1.0)
            kicker(g, t, L[1], "ชีวิตจริงแลกด้วยน้ำตา", SKYB, 84)
        return
    g.ground(GROUND, WHITE)
    if t < L[5] - 0.2:   # สารคดี + ข้อความขอหย่า ก่อนขึ้นเวที
        if t < L[3] - 0.2:
            with g.at(CX, 820, bounce(t, L[2])):
                sticker(g, 0, 0, 640, 420, hexc("#2b2b30"), PINK, 1.0, 0, 30, 8)
                g.poly([(-40, -60), (60, 0), (-40, 60)], WHITE, 0, amp=0)
            chip(g, t, L[2] + 0.4, CX, 1120, "Katy Perry: Part of Me (2012)", LEMON, 44)
            kicker(g, t, L[2], "ฉากบีบหัวใจในสารคดีของเธอ", GRAPE, 74)
        else:
            phone(g, 720, 820, 1.2 * bounce(t, L[3]) + 0.01, 6, "ขอหย่า", 1.0 if t < L[4] else 0.0, t)
            person(g, 260, GROUND, KATY, 0.8, mood="shock", pose="phone", turn=0.3, seed=2)
            if t < L[4] - 0.2:
                kicker(g, t, L[3], "ข้อความขอหย่าจากสามี", RED, 82)
            else:
                chip(g, t, L[4] + 0.2, 720, 450, "อีกไม่กี่นาทีขึ้นเวที!", LEMON, 52)
                kicker(g, t, L[4], "แฟนเพลงนับหมื่นรออยู่...", SKYB, 76, y=330)
        return
    if t < L[6] - 0.2:   # ร้องไห้หลังเวที
        c = g.c
        c.rectangle(-500, 140, 2100, 1130)
        c.set_source_rgba(0.2, 0.2, 0.28, 0.18)
        c.fill()
        person(g, CX, GROUND, KATY, 0.85, mood="sad", pose="think", turn=0, seed=2, lean=4 * math.sin(t * 3))
        tear_drops(g, CX + 30, 470, t, 1.2)
        kicker(g, t, L[5], "ร้องไห้แทบขาดใจหลังเวที", SKYB, 78)
        return
    # ไฟเปิด -> ปาดน้ำตา ยิ้ม -> ออกไปมอบความสุข
    op = e_io(seg(t, L[6], L[6] + 1.0))
    curtain(g, op, t)
    spotlight(g, CX, 160, t, op)
    if t < L[8] - 0.2:
        person(g, CX, GROUND, KATY, 0.85, mood="sad" if t < L[7] else "smile", pose="think" if t < L[7] else "wave",
               turn=0, seed=2)
        kicker(g, t, L[6] if t < L[7] - 0.2 else L[7], "สัญญาณไฟเปิด!" if t < L[7] - 0.2 else "ปาดน้ำตา ฉีกยิ้ม",
               LEMON if t < L[7] - 0.2 else PINK, 88)
    else:
        u = e_io(seg(t, L[8], L[8] + 1.5))
        person(g, CX, GROUND, KATY, lerp(0.85, 0.95, u), mood="smile", pose="v", turn=0, seed=2, talk=True)
        mic(g, CX + 120, 520, 0.6, -20)
        confetti(g, t, 26, 11)
        kicker(g, t, L[8], "มอบความสุขราวกับไม่มีอะไรเกิดขึ้น!", PINK, 68)


# ------------------------------------------------------------------ 6. lesson
def s_lesson(g, t, L, d):
    bg(g, t, 13)
    if t < L[2] - 0.2:
        for i in range(3):
            contract(g, 220 + i * 320, 1000, 0.42, -8 + 8 * i, 1.0)
        person(g, CX, GROUND - 120, KATY, 0.7, mood="firm", pose="fist", turn=0, seed=2)
        if t < L[1] - 0.2:
            kicker(g, t, L[0], "ชีวิตของเคทีพิสูจน์ว่า...", SKYB, 82)
        else:
            chip(g, t, L[1] + 0.2, CX, 520, "ล้มเหลว = บททดสอบ", MINT, 62)
            kicker(g, t, L[1], "ความล้มเหลวคือบททดสอบ", LEMON, 80, y=340)
        return
    spotlight(g, CX, 160, t, 1.0)
    person(g, CX, GROUND, KATY, 0.9, mood="smile", pose="v", turn=0, seed=2)
    for i in range(8):
        a = i * 0.785 + t * 0.6
        g.sparkle(CX + 360 * math.cos(a), 760 + 300 * math.sin(a), 30)
    if t < L[3] - 0.2:
        kicker(g, t, L[2], "คนที่ส่องประกายเจิดจ้าที่สุด", LEMON, 76)
    else:
        mic(g, CX + 140, 520, 0.6, -20)
        kicker(g, t, L[3], "คือคนที่กล้าร้องเพลงต่อ!", PINK, 84)


# ------------------------------------------------------------------ 7. outro
def s_outro(g, t, L, d):
    bg(g, t, 17)
    if t < L[2] - 0.2:
        person(g, 250, GROUND, KATY, 0.8, mood="smile", pose="wave", turn=0.3, seed=2, talk=True)
        if t < L[1] - 0.2:
            for i, (song, col) in enumerate((("Roar", PINK), ("Firework", LEMON), ("Teenage Dream", SKYB),
                                              ("Dark Horse", GRAPE))):
                chip(g, t, L[0] + 0.3 * i, 720, 560 + i * 170, song, col, 50, -3 + 2 * i, w=400)
            kicker(g, t, L[0], "ชอบเพลงไหนที่สุด?", PINK, 90)
        else:
            with g.at(740, 780, bounce(t, L[1])):
                g.circle(0, 0, 170, LEMON, 8)
                g.label("PRO", 0, -20, 90)
                g.label("สปิริตมืออาชีพ", 0, 70, 40)
            kicker(g, t, L[1], "ประทับใจสปิริตมืออาชีพ?", MINT, 82)
        return
    with g.at(CX + 170, 640, bounce(t, L[2])):   # ชวนคอมเมนต์
        sticker(g, 0, 0, 460, 220, WHITE, PINK, 1.0, 0, 50, 7)
        for i in range(3):
            g.circle(-110 + i * 110, 0, 24 + 6 * math.sin(t * 6 - i), INK, 0)
    person(g, 250, GROUND, KATY, 0.8, mood="smile", pose="wave", turn=0.3, seed=2, talk=True)
    kicker(g, t, L[2], "คอมเมนต์แลกเปลี่ยนกันได้เลย!", LEMON, 64)


SCENES = {
    "hook": s_hook, "born": s_born, "la": s_la, "boom": s_boom, "tears": s_tears, "lesson": s_lesson,
    "outro": s_outro,
}
NO_IRIS = set()
