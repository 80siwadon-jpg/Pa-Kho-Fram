"""ฉากตอน: วันเกิดจูเลีย โรเบิร์ตส์ (28 ต.ค. 1967)"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from chars import (ACTOR, ERIC, EXEC, FAMILIES, JULIA, JULIA_ERIN, JULIA_KID, JULIA_RED, JULIA_YOUNG, PW_RED,  # noqa: E402
                   STARS, balance, boxoffice, clapper, confetti, dog, factory, film_strip, gavel, glass_ceiling,
                   golden_statue, heart, hollywood, money, nyc, paw, price_card, smile_icon, spotlight, suitcase,
                   vet_kit)
from gfx import GOLD, GOLD2, GREY, INK, NAVY, RED, W, WHITE, e_io, e_out, hexc, lerp, pop, seg  # noqa: E402
from people import person  # noqa: E402

CX = W / 2
GROUND = 1270
GOLDTXT = hexc("#b37a12")
GREEN = hexc("#3c8d4f")
PINK = hexc("#d9506a")
DARK = hexc("#3a3f48")

CAMERA = {"hook": "push_in", "young": "pan_right", "pretty": "dutch", "erin": "push_in", "lesson": "pull_out",
          "outro": "pan_right"}
TRANSITIONS = {"young": "zoom", "pretty": "whip", "erin": "iris", "lesson": "fade", "outro": "whip"}


def ap(t, a, dur=0.38):
    return pop(t, a - 0.2, dur)


def title(g, t, a, txt, col=INK, size=84, y=380):
    g.label(txt, CX, y, size, color=col, sc=ap(t, a), rot=-3)


def julia(g, x, look=JULIA, sc=0.82, mood="smile", pose="down", turn=0.3, talk=False, seed=3):
    person(g, x, GROUND, look, sc, mood=mood, pose=pose, turn=turn, seed=seed, talk=talk)


# ------------------------------------------------------------------ 1. hook
def s_hook(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # รอยยิ้มที่ผู้กำกับเกือบมองข้าม
        smile_icon(g, 720, 760, 150 * ap(t, L[1] + 0.2) + 1, t)
        julia(g, 280, JULIA, 0.8, "smile", "wave", 0.3)
        g.name_tag(t, L[1] + 0.1, 330, 1100, "จูเลีย โรเบิร์ตส์", "นักแสดงรางวัลออสการ์", side=1)
        title(g, t, L[1], "รอยยิ้มที่เกือบถูกมองข้าม", PINK, 84)
        return
    if t < L[3] - 0.2:   # หญิงข้างถนน → เทพนิยายโมเดิร์น
        julia(g, 320, JULIA_RED, 0.82, "smile", "wave", 0.3)
        for i in range(5):
            g.sparkle(320 + 220 * math.cos(i * 1.25 + t * 1.5), 760 + 260 * math.sin(i * 1.25 + t * 1.5), 24)
        film_strip(g, 760, 860, 0.8 * ap(t, L[2] + 0.6) + 0.01, 5, "Pretty Woman", PW_RED, t)
        title(g, t, L[2], "เทพนิยายโมเดิร์น", PINK, 92)
        return
    k = e_io(seg(t, L[3] + 0.6, L[3] + 2.2))   # ค่าตัว 20 ล้านดอลลาร์ เทียบดาราชาย
    balance(g, CX, GROUND - 40, 0.95, 1 - k, t)
    g.label("$20,000,000", CX, 560, 90, color=GREEN, sc=ap(t, L[3] + 0.3), rot=-4)
    title(g, t, L[3] if t < L[4] - 0.2 else L[4], "หญิงคนแรกที่ค่าตัว 20 ล้านดอลลาร์" if t < L[4] - 0.2 else
          "เทียบชั้นดาราชายฮอลลีวูด!", GOLDTXT, 76)


# ------------------------------------------------------------------ 2. young
def s_young(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # 28 ต.ค. 1967 จอร์เจีย
        if t < L[1] - 0.2:
            g.calendar(CX, 860, 1.25 * ap(t, L[0]) + 0.01, 28, "เสาร์", "ต.ค. 1967")
            g.label("รัฐจอร์เจีย", CX, 1150, 66, color=GREEN, sc=ap(t, L[0] + 1.6))
            title(g, t, L[0], "28 ตุลาคม 1967", PINK, 92)
        else:
            julia(g, CX, JULIA_KID, 0.9, "smile", "wave", 0.0)
            title(g, t, L[1], "จูเลีย ฟิโอนา โรเบิร์ตส์", INK, 86)
        return
    if t < L[4] - 0.2:   # ไม่ฝันเป็นดารา รักสัตว์ อยากเป็นสัตวแพทย์
        julia(g, 300, JULIA_KID, 0.88, "smile", "down" if t < L[3] - 0.2 else "hold", 0.4)
        if t < L[3] - 0.2:
            g.label("ดารา?", 760, 720, 90, color=GREY, sc=ap(t, L[2] + 0.3), rot=6)
            k = seg(t, L[2] + 1.0, L[2] + 1.5)
            if k > 0:
                g.line([(640, 640), (640 + 240 * k, 640 + 170 * k)], 14, RED, amp=0)
            title(g, t, L[2], "ไม่เคยฝันอยากเป็นดารา", INK, 86)
        else:
            dog(g, 700, GROUND, 1.2, t)
            vet_kit(g, 760, 720, 0.9 * ap(t, L[3] + 0.4) + 0.01)
            title(g, t, L[3], "รักสัตว์ อยากเป็นสัตวแพทย์", GREEN, 84)
        return
    if t < L[6] - 0.2:   # พี่ชายเข้าวงการ → เข้านิวยอร์ก
        if t < L[5] - 0.2:
            spotlight(g, 760, GROUND, t, 1.0)
            person(g, 760, GROUND, ERIC, 0.8, mood="smile", pose="wave", turn=-0.4, seed=10)
            julia(g, 300, JULIA_YOUNG, 0.78, "smile", "down", 0.4)
            g.label("พี่ชาย", 760, 520, 60, color=GOLDTXT, sc=ap(t, L[4] + 0.4))
            title(g, t, L[4], "พี่ชายเข้าสู่วงการบันเทิง", INK, 84)
        else:
            nyc(g, GROUND, t)
            suitcase(g, 760, GROUND, 0.7)
            julia(g, lerp(200, 400, e_io(seg(t, L[5], L[6]))), JULIA_YOUNG, 0.78, "smile", "down", 0.6)
            title(g, t, L[5], "เข้านิวยอร์กเสี่ยงโชค!", NAVY, 90)
        return
    if t < L[7] - 0.2:   # ตัวประกอบเล็ก ๆ หนังอินดี้
        film_strip(g, 760, 880 + 15 * math.sin(t * 2), 0.8, 4 * math.sin(t * 1.5), "INDIE", GREY, t)
        julia(g, 300, JULIA_YOUNG, 0.76, "smile", "hold", 0.3)
        title(g, t, L[6], "บทตัวประกอบเล็ก ๆ หนังอินดี้", GREY, 82)
        return
    spotlight(g, 360, GROUND, t, 1.0)   # โอกาสทอง Pretty Woman (1990)
    julia(g, 360, JULIA_RED, 0.82, "smile", "wave", 0.2)
    for i in range(5):
        g.star(360 + 260 * math.cos(i * 1.25 + t), 700 + 200 * math.sin(i * 1.25 + t), 22, GOLD2, 4)
    if t > L[8] - 0.2:
        film_strip(g, 770, 900, 0.8 * ap(t, L[8]) + 0.01, 5, "Pretty Woman", PW_RED, t)
        g.label("1990", 770, 1080, 60, color=PW_RED, sc=ap(t, L[8] + 0.3))
    title(g, t, L[7] if t < L[8] - 0.2 else L[8], "โอกาสทองเปลี่ยนชีวิต!" if t < L[8] - 0.2 else
          "Pretty Woman (1990)", PW_RED, 88)


# ------------------------------------------------------------------ 3. pretty
def s_pretty(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # ชื่อเดิม $3,000 / ดราม่ามืดมน
        if t < L[1] - 0.2:
            price_card(g, CX, 840, 1.2 * ap(t, L[0] + 0.3) + 0.01, -4 + 2 * math.sin(t * 2), "$3,000", DARK)
            g.label("ชื่อเดิมของหนัง", CX, 1060, 60, color=GREY, sc=ap(t, L[0] + 0.8))
            title(g, t, L[0], "เดิมทีชื่อว่า \"$3,000\"", DARK, 88)
        else:
            import cairo
            c = g.c
            gr = cairo.LinearGradient(0, 140, 0, GROUND)
            gr.add_color_stop_rgba(0, 0.1, 0.12, 0.2, 0.8)
            gr.add_color_stop_rgba(1, 0.1, 0.12, 0.2, 0.3)
            c.rectangle(-500, 140, 2100, GROUND - 140)
            c.set_source(gr)
            c.fill()
            nyc(g, GROUND, t)
            for i in range(2):
                a = math.radians(-90 + 25 * math.sin(t * 0.9 + i * 2))
                g.line([(300 + i * 480, GROUND), (300 + i * 480 + 900 * math.cos(a), GROUND + 900 * math.sin(a))], 30,
                       (1, 0.95, 0.7, 0.25), amp=0)
            for i in range(6):
                u = (t * 0.3 + i / 6) % 1
                g.circle(150 + 780 * u, GROUND - 20, 10, (1, 0.85, 0.4, 0.9), 0)
            title(g, t, L[1], "ดราม่ามืดมนในลอสแอนเจลิส", hexc("#f2c94c"), 80)
        return
    if t < L[3] - 0.2:   # นักแสดงหญิงหลายคนปฏิเสธ
        for i, lk in enumerate(STARS):
            person(g, 260 + i * 260, GROUND, lk, 0.74, mood="neutral", pose="stop", turn=0.3 - 0.3 * i, seed=20 + i)
        with g.at(800, 860, ap(t, L[2] + 0.4), 6):
            g.rrect(-110, -150, 220, 300, 10, hexc("#f4eedf"), 6)
            g.text("Vivian", 0, -80, 36, "kanit", PW_RED)
            g.line([(-80, 30), (80, 30)], 4, GREY, amp=0)
            g.line([(-80, 70), (60, 70)], 4, GREY, amp=0)
        title(g, t, L[2], "ดาราแถวหน้าพากันปฏิเสธบท", INK, 82)
        return
    if t < L[6] - 0.2:   # จูเลียวัย 22 + รอยยิ้มพันล้าน เปลี่ยนโทนหนัง
        julia(g, 300, JULIA_RED, 0.84, "smile", "wave" if t > L[4] - 0.2 else "down", 0.3, talk=t > L[4] - 0.2)
        if t < L[4] - 0.2:
            with g.at(760, 760, ap(t, L[3] + 0.3), 5):
                g.circle(0, 0, 110, PINK, 7)
                g.text("22", 0, -10, 80, "kanit", WHITE)
                g.text("ปี", 0, 50, 34, "kanitsb", WHITE)
            title(g, t, L[3], "บทตกถึงมือจูเลียวัย 22", PINK, 86)
        elif t < L[5] - 0.2:
            smile_icon(g, 760, 760, 130, t)
            title(g, t, L[4], "\"รอยยิ้มพันล้าน\"", GOLDTXT, 96)
        else:
            heart(g, 760, 760, 90 + 8 * math.sin(t * 4))
            confetti(g, t, 14)
            title(g, t, L[5], "กลายเป็นโรแมนติกคอมเมดี้สุดคลาสสิก", PINK, 74)
        return
    if t < L[7] - 0.2:   # รายได้ 460 ล้านดอลลาร์
        boxoffice(g, 640, 860, 1.0, seg(t, L[6], L[6] + 1.8), t)
        money(g, 230, 1150, 0.9, t)
        n = int(lerp(10, 460, e_out(seg(t, L[6], L[6] + 1.8))))
        g.label(f"${n}M+", 640, 560, 90, color=GREEN, sc=ap(t, L[6] + 0.3))
        title(g, t, L[6], "รายได้ทั่วโลกกว่า 460 ล้านดอลลาร์", GREEN, 76)
        return
    hollywood(g, GROUND, t)   # America's Sweetheart ขวัญใจทั้งโลก
    julia(g, CX, JULIA_RED, 0.82, "smile", "wave", 0.0)
    confetti(g, t, 16)
    for i in range(4):
        u = (t * 0.6 + i / 4) % 1
        heart(g, 240 + i * 200, 1000 - 300 * u, 26, RED, 1 - u)
    title(g, t, L[7] if t < L[8] - 0.2 else L[8], "\"America's Sweetheart\"" if t < L[8] - 0.2 else
          "ขวัญใจคนทั้งโลกชั่วข้ามคืน!", PINK, 86)


# ------------------------------------------------------------------ 4. erin
def s_erin(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # ไม่หยุดแค่หนังรัก → ดราม่าเข้มข้น
        julia(g, 300, JULIA_ERIN, 0.82, "firm", "fist" if t > L[1] - 0.2 else "down", 0.3)
        if t < L[1] - 0.2:
            heart(g, 760, 760, 80)
            title(g, t, L[0], "ไม่หยุดแค่นางเอกหนังรัก", INK, 86)
        else:
            film_strip(g, 760, 860, 0.8, 5, "DRAMA", DARK, t)
            title(g, t, L[1], "ท้าทายด้วยบทดราม่าเข้มข้น", NAVY, 82)
        return
    if t < L[4] - 0.2:   # Erin Brockovich (2000) แม่เลี้ยงเดี่ยวสู้บริษัทยักษ์
        if t < L[3] - 0.2:
            film_strip(g, CX, 820, 1.2 * ap(t, L[2]) + 0.01, -3, "Erin Brockovich", hexc("#2b6f8a"), t)
            g.label("2000", CX, 1080, 70, color=hexc("#2b6f8a"), sc=ap(t, L[2] + 0.4))
            title(g, t, L[2], "Erin Brockovich (2000)", hexc("#2b6f8a"), 86)
        else:
            factory(g, 700, GROUND, 0.85, t)
            julia(g, 230, JULIA_ERIN, 0.78, "firm", "point", 0.4, talk=True)
            title(g, t, L[3], "แม่เลี้ยงเดี่ยวสู้บริษัทยักษ์!", NAVY, 84)
        return
    if t < L[6] - 0.2:   # กวาดทุกรางวัล + ออสการ์
        julia(g, 300, JULIA, 0.8, "smile", "hold", 0.3)
        n = 3 if t < L[5] - 0.2 else 4
        for i in range(n):
            golden_statue(g, 600 + (i % 2) * 180 + (i // 2) * 90, GROUND, 0.6 * ap(t, L[4] + 0.3 * i, 0.3) + 0.01, 0,
                          1.0 if i == 3 else 0.0, t)
        if t < L[5] - 0.2:
            title(g, t, L[4], "กวาดทุกรางวัลใหญ่", GOLDTXT, 92)
        else:
            title(g, t, L[5], "ออสการ์ นักแสดงนำหญิงยอดเยี่ยม!", GOLDTXT, 80)
        return
    if t < L[7] - 0.2:   # ทุบเพดานกระจก
        glass_ceiling(g, CX, 640, 760, e_io(seg(t, L[6] + 0.6, L[6] + 2.0)), t)
        julia(g, CX, JULIA, 0.82, "firm", "fist", 0.0)
        title(g, t, L[6], "ทุบเพดานกระจกของฮอลลีวูด!", PINK, 84)
        return
    if t < L[8] - 0.2:   # หญิงคนแรกค่าตัว 20 ล้าน
        julia(g, 280, JULIA, 0.8, "smile", "wave", 0.3)
        money(g, 760, 1150, 1.0, t)
        n = int(lerp(1, 20, e_out(seg(t, L[7], L[7] + 2.0))))
        g.label(f"${n},000,000", 720, 700, 76, color=GREEN, sc=ap(t, L[7] + 0.3), rot=-4)
        title(g, t, L[7], "หญิงคนแรก ค่าตัว 20 ล้านดอลลาร์", GREEN, 78)
        return
    balance(g, CX, GROUND - 40, 0.95, 0, t)   # ยุติความเหลื่อมล้ำ
    for i in range(4):
        g.sparkle(CX + 330 * math.cos(i * 1.6 + t), 760 + 140 * math.sin(i * 1.6 + t), 24)
    title(g, t, L[8], "ยุติความเหลื่อมล้ำรายได้ระหว่างเพศ", GOLDTXT, 76)


# ------------------------------------------------------------------ 5. lesson
def s_lesson(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:
        julia(g, CX, JULIA, 0.86, "smile", "down", 0.0)
        title(g, t, L[0], "เส้นทางของเธอพิสูจน์ว่า...", INK, 84)
        return
    if t < L[2] - 0.2:   # ไม่ใช่ความสมบูรณ์แบบตามแบบแผน
        with g.at(CX, 840, ap(t, L[1] + 0.2), -3 + 2 * math.sin(t * 2)):
            g.rrect(-250, -250, 500, 500, 10, (1, 1, 1, 0), 8, stroke=GREY)
            g.text("PERFECT", 0, 0, 70, "kanit", GREY)
        k = seg(t, L[1] + 1.0, L[1] + 1.7)
        if k > 0:
            g.line([(CX - 270, 590), (CX - 270 + 540 * k, 590 + 500 * k)], 16, RED, amp=0)
        title(g, t, L[1], "ไม่ใช่ความสมบูรณ์แบบตามแบบแผน", INK, 78)
        return
    julia(g, 280, JULIA, 0.82, "smile", "wave", 0.3)   # ความจริงใจ มั่นใจ รอยยิ้ม
    if t < L[3] - 0.2:
        for i, (txt, col) in enumerate((("จริงใจ", PINK), ("มั่นใจ", NAVY))):
            k = ap(t, L[2] + 0.6 * i, 0.3)
            if k > 0.02:
                with g.at(760, 720 + i * 230, k, -4 + 8 * i):
                    g.rrect(-170, -70, 340, 140, 40, WHITE, 7, stroke=col)
                    g.label(txt, 0, 0, 60, color=col)
        title(g, t, L[2], "ความจริงใจ ความมั่นใจในตัวเอง", PINK, 78)
    else:
        smile_icon(g, 760, 820, 130, t)
        title(g, t, L[3], "รอยยิ้มที่สะกดคนทั้งโลก", GOLDTXT, 86)


# ------------------------------------------------------------------ 6. outro
def s_outro(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:
        julia(g, CX, JULIA, 0.84, "smile", "wave", 0.0, talk=True)
        title(g, t, L[0], "ชอบผลงานไหนที่สุด?", INK, 90)
        return
    if t < L[3] - 0.2:   # Pretty Woman / Notting Hill / Erin Brockovich
        items = (("Pretty Woman", PW_RED), ("Notting Hill", hexc("#3f6496")), ("Erin Brockovich", hexc("#2b6f8a")))
        for i, (txt, col) in enumerate(items):
            k = ap(t, L[1] + 1.2 * i, 0.3) if i < 2 else ap(t, L[2])
            if k > 0.02:
                film_strip(g, 300 + (i % 2) * 460 if i < 2 else CX, 760 + (i // 2) * 320 + 20 * math.sin(t * 2 + i),
                           0.72 * k, -5 + 5 * i, txt, col, t)
        title(g, t, L[1], "ผลงานในความทรงจำ", PINK, 88)
        return
    with g.at(CX + 170, 640, ap(t, L[3])):   # ชวนคอมเมนต์
        g.bubble(0, 0, 460, 220, WHITE, tail=(-1, 1))
        for i in range(3):
            g.circle(-110 + i * 110, 0, 24 + 6 * math.sin(t * 6 - i), INK, 0)
    julia(g, 260, JULIA, 0.8, "smile", "wave", 0.3, talk=True)
    title(g, t, L[3], "มาแลกเปลี่ยนกันในคอมเมนต์!", RED, 70)


SCENES = {
    "hook": s_hook, "young": s_young, "pretty": s_pretty, "erin": s_erin, "lesson": s_lesson, "outro": s_outro,
}
NO_IRIS = set()
