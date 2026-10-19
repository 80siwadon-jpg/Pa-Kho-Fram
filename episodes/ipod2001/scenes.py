"""ฉากตอน: แอปเปิลเปิดตัว iPod รุ่นแรก (23 ต.ค. 2001)"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from chars import (CRITICS, JOBS, TEENS, apple, cards, chart, earbuds, iphone, ipod, ipod_family, mac,  # noqa: E402
                   mp3, price_tag, silhouette_dancer, stage)
from gfx import GOLD2, GREY, INK, NAVY, RED, W, WHITE, e_io, e_out, hexc, lerp, pop, seg  # noqa: E402
from people import person  # noqa: E402
from photos import photo  # noqa: E402

CX = W / 2
GROUND = 1270
GOLDTXT = hexc("#b37a12")
GREEN = hexc("#3c8d4f")

CAMERA = {"hook": "push_in", "context": "pan_right", "reveal": "push_in", "critics": "dutch", "vision": "pan_left",
          "iphone": "tilt_up", "lesson": "pull_out", "outro": "pan_right"}
TRANSITIONS = {"context": "fade", "reveal": "zoom", "critics": "whip", "vision": "iris", "iphone": "zoom",
               "lesson": "fade", "outro": "whip"}


def ap(t, a, dur=0.38):
    return pop(t, a - 0.2, dur)


def jobs(g, x, sc=0.85, mood="smile", pose="down", turn=0.0, talk=False, pose2=None, k=0.0):
    person(g, x, GROUND, JOBS, sc, mood=mood, pose=pose, pose2=pose2, k=k, turn=turn, seed=4, talk=talk)


def notes(g, t, x0, y0, x1, y1, n=5, seed=0):
    """โน้ตเพลงลอยจาก (x0,y0) ไป (x1,y1)"""
    for i in range(n):
        u = (t * 0.5 + i / n + seed) % 1
        x = lerp(x0, x1, u) + 40 * math.sin(t * 3 + i)
        y = lerp(y0, y1, u) - 80 * math.sin(math.pi * u)
        note(g, x, y, 1.0, (NAVY, RED, GREEN, GOLDTXT)[i % 4], math.sin(math.pi * u), i % 2)


def note(g, x, y, sc=1.0, col=INK, a=1.0, double=False):
    """โน้ตดนตรี (วาดเอง — ฟอนต์ Kanit ไม่มีสัญลักษณ์ ♪)"""
    if a <= 0.02:
        return
    with g.at(x, y, sc, -12), g.alpha(a):
        heads = [(-22, 20), (30, 8)] if double else [(0, 20)]
        for hx, hy in heads:
            g.circle(hx, hy, 15, col, 4)
            g.line([(hx + 13, hy), (hx + 13, hy - 60)], 6, INK, amp=0)
        if double:
            g.line([(-9, -40), (43, -52)], 10, INK, amp=0)
        else:
            g.line([(13, -40), (32, -20)], 6, INK, amp=0)


def real_ipod(g, x, y, k, t, label="iPod รุ่นแรก (2001)"):
    if not photo(g, "ipod_real", x, y, 440, 500, -3, k, 1.0 + 0.03 * math.sin(t), label=label):
        ipod(g, x, y, 1.1 * k, -3, t, glow=1.0)


# ------------------------------------------------------------------ 1. hook
def s_hook(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:   # วันที่ + กล่องปริศนา
        with g.at(CX, 860 + 14 * math.sin(t * 2), pop(t, 0.6), 4 * math.sin(t * 1.5)):
            g.rrect(-130, -200, 260, 400, 34, WHITE, 7)
            g.label("?", 0, 0, 160, color=GREY)
        g.label("วันนี้ในอดีต", CX, 380, 104, sc=lerp(2.0, 1, e_out(seg(t, 0.1, 0.4))) if t > 0.1 else 0, rot=-3)
        g.label("23 ตุลาคม 2001", CX, 520, 84, color=RED, sc=pop(t, 0.8))
        return
    if t < L[2] - 0.2:   # ขนาดเท่าตลับไพ่
        cards(g, 330, 820, 1.1 * ap(t, L[1]), -6)
        ipod(g, 750, 820, 0.85 * ap(t, L[1] + 0.4), 5, t)
        g.label("=", CX + 0, 820, 110, color=GREY, sc=ap(t, L[1] + 0.8))
        g.label("ขนาดเท่าตลับไพ่", CX, 380, 90, sc=ap(t, L[1]), rot=-3)
        return
    if t < L[3] - 0.2:   # เปิดตัวเงียบ ๆ ในหอประชุมเล็ก
        stage(g, GROUND - 80, t=t)
        jobs(g, CX, 0.62, "smile", "hold", 0.0)
        ipod(g, CX + 90, GROUND - 80 - 430, 0.22, 0, t)
        g.label("หอประชุมเล็ก ๆ", CX, 380, 90, color=NAVY, sc=ap(t, L[2]), rot=-3)
        g.label("เปิดตัวแบบเงียบเหงา", CX, 500, 56, color=GREY, sc=ap(t, L[2] + 0.5))
        return
    if t < L[4] - 0.2:   # พลิกฟื้นบริษัทที่เกือบเจ๊ง
        k = e_io(seg(t, L[3] + 0.3, L[4] - 0.3))
        chart(g, 160, 1150, 760, 560, [(0, 0.6), (0.3, 0.15), (0.55, 0.3), (0.8, 0.7), (1, 0.95)], 0.3 + 0.7 * k)
        apple(g, 300, 980, 90 * (0.6 + 0.4 * k), hexc("#9a8a7a") if k < 0.4 else hexc("#d8473d"), True)
        g.label("บริษัทที่เกือบเจ๊ง → พลิกฟื้น", CX, 380, 74, color=GREEN, sc=ap(t, L[3]), rot=-3)
        return
    g.sunburst(CX, 820, 240, 560, 20, t * 10, 10, (0.95, 0.85, 0.55, 0.6))   # มหาอำนาจเทคโนโลยีอันดับหนึ่ง
    apple(g, CX, 840 - 30 * e_out(seg(t, L[4], L[4] + 1.0)), 210 * ap(t, L[4]), bite=True)
    g.label("อันดับ 1 ของโลก!", CX, 380, 100, color=GOLDTXT, sc=ap(t, L[4]), rot=-3)


# ------------------------------------------------------------------ 2. context
def s_context(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[4] - 0.2:
        if t < L[2] - 0.2:   # แอปเปิลเพิ่งรอดล้มละลาย
            with g.at(CX, 640, ap(t, 0.2)):
                g.rrect(-200, -110, 400, 220, 24, WHITE, 7)
                g.rrect(-200, -110, 400, 70, 24, RED, 7)
                g.text("ปี", 0, -76, 34, "kanit", WHITE)
                g.label("2001", 0, 30, 100)
            if t > L[1] - 0.2:
                apple(g, CX, 1080, 110 * ap(t, L[1]), hexc("#b79a7a"), True)
                g.sweat(CX + 110, 980, 1.0)
                g.label("เพิ่งรอดจากล้มละลาย", CX, 380, 78, color=RED, sc=ap(t, L[1]), rot=-3)
            else:
                g.label("ย้อนกลับไป...", CX, 380, 96, sc=ap(t, 0.2), rot=-3)
            return
        if t < L[3] - 0.2:   # โลกตะลึงกับ 9/11 (หนังสือพิมพ์ ไม่แสดงภาพเหตุการณ์)
            with g.at(CX, 800, ap(t, L[2]), -3 + math.sin(t)):
                g.rrect(-330, -260, 660, 520, 10, hexc("#f4efe2"), 7)
                g.label("11 ก.ย. 2001", 0, -170, 70, color=RED)
                for i in range(5):
                    g.line([(-270, -60 + i * 60), (270 - 80 * (i % 2), -60 + i * 60)], 10, hexc("#c9c4b8"), amp=0)
            g.label("โลกตกตะลึงกับเหตุการณ์ 9/11", CX, 380, 70, sc=ap(t, L[2]), rot=-3)
            return
        chart(g, 160, 1150, 760, 560, [(0, 0.85), (0.3, 0.7), (0.5, 0.75), (0.75, 0.35), (1, 0.12)],
              e_io(seg(t, L[3], L[4] - 0.4)), RED)
        g.label("เศรษฐกิจดิ่งลงเหว", CX, 380, 90, color=RED, sc=ap(t, L[3]), rot=-3)
        return
    if t < L[6] - 0.2:   # สตีฟ จ็อบส์ ขึ้นเวที
        jobs(g, 330, 0.9, "smile" if t < L[5] else "smug", "down" if t < L[5] else "point", 0.3, talk=t > L[5])
        g.name_tag(t, L[4] + 0.1, 780, 1130, "สตีฟ จ็อบส์", "ผู้ก่อตั้งและซีอีโอแอปเปิล", side=-1)
        if t < L[5] - 0.2:
            g.label("ไม่ยอมจำนนต่อกรอบเดิม ๆ", CX, 360, 74, color=NAVY, sc=ap(t, L[4]), rot=-3)
        else:
            with g.at(760, 640, ap(t, L[5])):
                g.bubble(0, 0, 400, 200, WHITE, tail=(-1, 1))
                g.label("ประโยคเดียว...", 0, 0, 50)
            g.label("ขึ้นเวที", CX, 360, 90, color=NAVY, sc=ap(t, L[5]), rot=-3)
        return
    jobs(g, 280, 0.85, "smile", "hold", 0.3, talk=True)   # 1,000 เพลงในกระเป๋า
    notes(g, t, 900, 500, 330, 1000, 7)
    g.label('"1,000 เพลง', 720, 560, 84, color=RED, sc=ap(t, L[6]), rot=-4)
    g.label('ในกระเป๋าของคุณ"', 720, 680, 64, color=NAVY, sc=ap(t, L[6] + 0.3), rot=-4)


# ------------------------------------------------------------------ 3. reveal
def s_reveal(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # ล้วงออกจากกระเป๋ากางเกงยีนส์
        k = e_out(seg(t, 0.4, L[2] - 0.4))
        jobs(g, 380, 0.92, "smug", "down", 0.3, pose2="hold", k=k)
        ipod(g, lerp(470, 560, k), lerp(GROUND - 380, GROUND - 640, k), lerp(0.12, 0.32, k), lerp(20, 0, k), t)
        g.label("ล้วงจากกระเป๋ายีนส์...", CX, 360, 78, sc=ap(t, 0.2), rot=-3)
        if t > L[1] - 0.2:
            g.label("วงล้อหมุนประหลาด", 820, 640, 50, color=GREY, sc=ap(t, L[1]))
        return
    g.sunburst(CX, 800, 330, 560, 20, t * 10, 10, (0.95, 0.85, 0.55, 0.5))
    real_ipod(g, CX, 800, ap(t, L[2] + 0.1), t)   # ภาพจริง iPod รุ่นแรก (เจ้าของช่องส่งมา)
    g.label('"iPod รุ่นแรก"!', CX, 330, 100, color=RED, sc=ap(t, L[2]), rot=-3)


# ------------------------------------------------------------------ 4. critics
def s_critics(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # สื่อรุมสับ หัวเราะเยาะ
        for i, lk in enumerate(CRITICS):
            person(g, 190 + i * 350, GROUND, lk, 0.62, mood="smug" if t > L[1] else "neutral",
                   pose="point" if i == 0 and t > L[1] else "down", turn=0.2 - 0.2 * i, seed=10 + i, talk=t > L[1])
        if t < L[1] - 0.2:
            g.label("ไม่ได้โรยด้วยกลีบกุหลาบ", CX, 380, 76, color=RED, sc=ap(t, 0.2), rot=-3)
            return
        for i in range(4):
            u = (t * 0.6 + i / 4) % 1
            g.label("ฮ่า ๆ", 200 + i * 230, 700 - 120 * u, 50, color=RED, a=1 - u)
        g.label("รุมสับ + หัวเราะเยาะ", CX, 380, 84, color=RED, sc=ap(t, L[1]), rot=-3)
        return
    if t < L[3] - 0.2:   # MP3 เกลื่อนตลาด
        cols = [hexc("#7a8a9a"), hexc("#c8553d"), hexc("#3c8d9f"), hexc("#8a6a9a"), hexc("#e3a92b"), hexc("#4a5a6a")]
        for i in range(6):
            mp3(g, 180 + (i % 3) * 360, 760 + (i // 3) * 300 + 10 * math.sin(t * 3 + i), 0.9 * ap(t, L[2] + 0.12 * i),
                (i - 2.5) * 6, cols[i])
        g.label("เครื่องเล่น MP3 เกลื่อนตลาด", CX, 380, 74, sc=ap(t, L[2]), rot=-3)
        return
    if t < L[4] - 0.2:   # ราคาเกือบ 400 ดอลลาร์
        ipod(g, 300, 820, 0.8, -4, t)
        price_tag(g, 760, 720, 1.2 * ap(t, L[3]), 8 * math.sin(t * 2))
        g.label("มากกว่าหมื่นบาท!", 760, 920, 60, color=RED, sc=ap(t, L[3] + 0.8))
        g.label("ใครจะยอมจ่าย?", CX, 380, 92, sc=ap(t, L[3]), rot=-3)
        return
    if t < L[5] - 0.2:   # ใช้ได้แค่กับ Mac
        mac(g, 340, GROUND - 40, 1.1)
        ipod(g, 800, 880, 0.75, 4, t)
        g.line([(520, 900), (680, 900)], 8, GREY, amp=0)
        with g.at(CX + 70, 520, ap(t, L[4] + 0.4), 4):
            g.rrect(-190, -60, 380, 120, 24, WHITE, 7, stroke=RED)
            g.label("Mac เท่านั้น!", 0, 0, 56, color=RED)
        g.label("ใช้ได้แค่กับ Mac?", CX, 360, 86, sc=ap(t, L[4]), rot=-3)
        return
    for i, lk in enumerate(CRITICS):   # ฟันธง: หายนะครั้งใหม่
        person(g, 190 + i * 350, GROUND, lk, 0.62, mood="smug", pose="point" if i != 1 else "cross",
               turn=0.2 - 0.2 * i, seed=10 + i, talk=True)
    if t > L[6] - 0.2:
        chart(g, 600, 760, 380, 240, [(0, 0.9), (0.5, 0.6), (1, 0.05)], e_io(seg(t, L[6], L[6] + 1.5)), RED, 9)
        g.label("หายนะครั้งใหม่?", CX, 380, 96, color=RED, sc=ap(t, L[6]), rot=-3)
    else:
        g.label("ฟันธง!", CX, 380, 110, color=RED, sc=ap(t, L[5]), rot=-3)


# ------------------------------------------------------------------ 5. vision
def s_vision(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[3] - 0.2:   # มองเห็นสิ่งที่คนอื่นไม่เห็น: เปลี่ยนวิถีชีวิต
        jobs(g, 280, 0.85, "smug", "think" if t < L[1] else "point", 0.3)
        if t < L[1] - 0.2:
            g.sunburst(760, 640, 90, 200, 12, t * 12, 8, (0.98, 0.8, 0.35, 0.8))
            g.circle(760, 640, 80, hexc("#f6c445"), 6)
            g.label("มองเห็นสิ่งที่คนอื่นไม่เห็น", CX, 360, 70, color=GOLDTXT, sc=ap(t, 0.2), rot=-3)
        elif t < L[2] - 0.2:
            ipod(g, 760, 760, 0.7 * ap(t, L[1]), 0, t)
            g.label("ไม่ใช่แค่เครื่องเล่นเพลง", CX, 360, 74, sc=ap(t, L[1]), rot=-3)
        else:
            for i, lk in enumerate(TEENS[:2]):
                person(g, 620 + i * 240, GROUND, lk, 0.55, mood="smile", pose="wave" if i else "down", turn=-0.3,
                       seed=20 + i)
            notes(g, t, 640, 700, 900, 520, 4)
            g.label("เปลี่ยนวิถีชีวิตผู้คน", CX, 360, 84, color=GREEN, sc=ap(t, L[2]), rot=-3)
        return
    if t < L[6] - 0.2:   # iTunes / ความเรียบง่าย
        if t < L[4] - 0.2:
            notes(g, t, 330, 760, 560, 480, 4)
            with g.at(330, 780 + 14 * math.sin(t * 2), ap(t, L[3]), 6 * math.sin(t * 1.5)):
                g.circle(0, 0, 170, WHITE, 8)
                g.circle(0, 0, 50, hexc("#8fc7e0"), 5)
                note(g, 0, 0, 1.3, NAVY, 1.0, True)
            with g.at(780, 780 + 10 * math.sin(t * 2 + 1), ap(t, L[3] + 0.5)):
                g.label("ละเมิด", 0, -20, 60, color=RED)
                g.line([(-140, -120), (140, 100)], 16, RED, amp=0)
            g.label("ระบบ iTunes", CX, 360, 92, color=NAVY, sc=ap(t, L[3]), rot=-3)
            g.label("กอบกู้อุตสาหกรรมดนตรี", CX, 1120, 58, color=GREEN, sc=ap(t, L[3] + 0.4))
            return
        ipod(g, CX, 800, 1.1, 0, t, glow=ap(t, L[4]), sel=int(t * 1.5) % 5)
        if t < L[5] - 0.2:
            g.label("คนทั่วไปเริ่มหลงรัก", CX, 360, 84, color=RED, sc=ap(t, L[4]), rot=-3)
        else:
            g.label("ความเรียบง่าย", CX, 360, 96, color=NAVY, sc=ap(t, L[5]), rot=-3)
            g.label("ประสบการณ์แบบแอปเปิล", CX, 1170, 56, color=GREY, sc=ap(t, L[5] + 0.4))
        return
    if t < L[7] - 0.2:   # จากสินค้าที่คนสบประมาท
        for i, lk in enumerate(CRITICS):
            person(g, 190 + i * 350, GROUND, lk, 0.62, mood="shock", pose="down", turn=0.2 - 0.2 * i, seed=10 + i)
        g.label("จากที่เคยสบประมาท...", CX, 380, 84, color=GREY, sc=ap(t, L[6]), rot=-3)
        return
    if t < L[8] - 0.2:   # ไอคอนแห่งยุค: เงาคนเต้น + หูฟังขาว
        for i in range(3):
            silhouette_dancer(g, 220 + i * 330, GROUND, 0.95, t, i * 1.3)
        g.label("ไอคอนแห่งยุคสมัย!", CX, 360, 90, color=GOLDTXT, sc=ap(t, L[7]), rot=-3)
        return
    for i, lk in enumerate(TEENS):   # วัยรุ่นทั่วโลกกับหูฟังสีขาว
        x = 200 + i * 340
        person(g, x, GROUND, lk, 0.6, mood="smile", pose="down", turn=0.2, seed=30 + i, k=0)
        hy = GROUND - 842 * 0.6 * lk.height
        for sx in (-1, 1):
            g.circle(x + sx * 36, hy + 4, 9, WHITE, 3)
        g.line([(x - 36, hy + 12), (x - 20, hy + 120), (x + 40, GROUND - 330)], 4, WHITE, amp=0)
        g.line([(x - 36, hy + 12), (x - 20, hy + 120), (x + 40, GROUND - 330)], 1.5, GREY, amp=0)
    notes(g, t, 150, 520, 950, 520, 6, 0.3)
    g.label("สายหูฟังสีขาว", CX, 360, 96, color=NAVY, sc=ap(t, L[8]), rot=-3)


# ------------------------------------------------------------------ 6. iphone
def s_iphone(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[3] - 0.2:   # บทเรียนจาก iPod: วงล้อ / พลังงาน / จอเล็ก -> ดีเอ็นเอ
        ipod(g, CX, 820, 0.95, 0, t)
        if t > L[1] - 0.2:
            for i, (txt, x, y) in enumerate((("วงล้อหมุน", 230, 1000), ("การจัดการพลังงาน", 860, 1110),
                                             ("หน้าจอเล็ก", 860, 600))):
                g.label(txt, x, y, 46, color=NAVY, sc=ap(t, L[1] + 0.5 * i))
        if t < L[2] - 0.2:
            g.label("บทเรียนจาก iPod", CX, 360, 90, sc=ap(t, 0.2), rot=-3)
        else:
            for i in range(14):   # เกลียวดีเอ็นเอ
                yy = 480 + i * 50
                ph = t * 2 + i * 0.6
                g.circle(120 + 50 * math.sin(ph), yy, 12, RED, 3)
                g.circle(120 - 50 * math.sin(ph), yy, 12, NAVY, 3)
            g.label("รากฐาน + ดีเอ็นเอ", CX, 360, 90, color=GREEN, sc=ap(t, L[2]), rot=-3)
        return
    if t < L[4] - 0.2:   # iPhone 6 ปีต่อมา
        ipod(g, 280, 820, 0.7, -5, t)
        g.label("→", CX, 820, 110, color=GREY, sc=ap(t, L[3] + 0.4))
        iphone(g, 780, 820, 1.0 * ap(t, L[3] + 0.6), 5 * math.sin(t), t)
        g.label('"iPhone" (2007)', CX, 360, 96, color=NAVY, sc=ap(t, L[3]), rot=-3)
        return
    if t < L[5] - 0.2:   # จากบริษัทคอมพิวเตอร์ธรรมดา
        mac(g, CX, GROUND - 40, 1.4, hexc("#9aa4ae"))
        g.label("บริษัทคอมพิวเตอร์ธรรมดา ๆ", CX, 360, 72, color=GREY, sc=ap(t, L[4]), rot=-3)
        return
    chart(g, 140, 1170, 800, 640, [(0, 0.02), (0.2, 0.04), (0.4, 0.12), (0.6, 0.3), (0.8, 0.6), (1, 0.98)],
          e_io(seg(t, L[5], L[5] + 2.0)))
    apple(g, 300, 640, 90 * ap(t, L[5] + 0.3), bite=True)
    g.label("มูลค่าสูงที่สุดในประวัติศาสตร์", CX, 360, 66, color=GOLDTXT, sc=ap(t, L[5]), rot=-3)


# ------------------------------------------------------------------ 7. lesson
def s_lesson(g, t, L, d):
    g.ground(GROUND, WHITE)
    g.label("บทเรียน", CX, 340, 100, sc=ap(t, 0.2), rot=-3)
    if t < L[2] - 0.2:
        g.sunburst(CX, 800, 120, 300, 14, t * 10, 10, (0.98, 0.8, 0.35, 0.7 * ap(t, L[1])))
        ipod(g, CX, 800, 0.8 * ap(t, 0.4), 4 * math.sin(t * 1.5), t)
        if t > L[1] - 0.2:
            g.label("นวัตกรรมที่เปลี่ยนโลก", CX, 490, 64, color=GREEN, sc=ap(t, L[1]))
        return
    for i, lk in enumerate(CRITICS):   # คนส่วนใหญ่มองข้าม
        person(g, 170 + i * 200, GROUND, lk, 0.55, mood="neutral", pose="cross", turn=-0.8, seed=40 + i, shadow=False)
    ipod(g, 860, 900 + 10 * math.sin(t * 2), 0.6, 8, t, glow=0.8)
    g.label("มักถูกมองข้าม", CX, 490, 70, color=RED, sc=ap(t, L[2]))


# ------------------------------------------------------------------ 8. outro
def s_outro(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:   # ทันใช้รุ่นไหน
        ipod_family(g, CX + 30, 840, 1.0, t, e_out(seg(t, 0.2, 1.6)))
        g.label("ทันใช้ iPod รุ่นไหน?", CX, 360, 90, sc=ap(t, 0.2), rot=-3)
        return
    if t < L[3] - 0.2:
        if t < L[2] - 0.2:   # ถ้าจ็อบส์ยอมถอย
            jobs(g, 300, 0.82, "worry", "shrug", 0.3)
            for i in range(3):
                u = (t * 0.6 + i / 3) % 1
                g.label("ไม่รอดหรอก!", 780, 900 - 300 * u - i * 40, 44, color=RED, a=1 - u)
            g.label("ถ้าวันนั้นยอมถอย...", CX, 360, 84, color=NAVY, sc=ap(t, L[1]), rot=-3)
            return
        iphone(g, CX, 800, 1.1, 4 * math.sin(t), t)
        g.label("?", CX + 230, 600, 140, color=RED, sc=ap(t, L[2] + 0.3))
        g.label("โลกสมาร์ตโฟนจะต่างไปแค่ไหน?", CX, 360, 66, sc=ap(t, L[2]), rot=-3)
        return
    with g.at(CX + 170, 640, ap(t, L[3])):   # ชวนคอมเมนต์
        g.bubble(0, 0, 460, 220, WHITE, tail=(-1, 1))
        for i in range(3):
            g.circle(-110 + i * 110, 0, 24 + 6 * math.sin(t * 6 - i), INK, 0)
    jobs(g, 250, 0.8, "smile", "wave", 0.3, talk=True)
    g.label("คอมเมนต์แลกเปลี่ยนกันได้เลย!", CX, 360, 70, color=RED, sc=ap(t, L[3]), rot=-3)


SCENES = {
    "hook": s_hook, "context": s_context, "reveal": s_reveal, "critics": s_critics, "vision": s_vision,
    "iphone": s_iphone, "lesson": s_lesson, "outro": s_outro,
}
NO_IRIS = set()
