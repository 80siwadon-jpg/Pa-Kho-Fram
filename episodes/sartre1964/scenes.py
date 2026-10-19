"""ฉากตอน: ซาร์ตร์ปฏิเสธรางวัลโนเบลวรรณกรรม (22 ต.ค. 1964)"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from chars import (COMMITTEE, CRITICS, SARTRE, bird_free, books, bookshelf, chain, envelope, legion,  # noqa: E402
                   medal, money_stack, newspaper, pipe)
from gfx import (GOLD, GOLD2, GREY, INK, LGREY, NAVY, RED, W, WHITE, e_io, e_out, hexc, lerp, pop,  # noqa: E402
                 seg)
from people import _rr, _shade, head, person  # noqa: E402

CX = W / 2
GROUND = 1270
GOLDTXT = hexc("#b37a12")
GREEN = hexc("#3c8d4f")

CAMERA = {"hook": "push_in", "philosophy": "pan_right", "stance": "pan_left", "refuse": "dutch", "lesson": "pull_out",
          "outro": "push_in"}
TRANSITIONS = {"philosophy": "fade", "stance": "whip", "refuse": "zoom", "lesson": "iris"}


def ap(t, a, dur=0.38):
    return pop(t, a - 0.2, dur)


def sartre(g, x, sc=0.85, mood="smug", pose="down", turn=0.2, t=0.0, smoke=True, talk=False):
    """ซาร์ตร์ + กล้องยาสูบที่ปาก"""
    person(g, x, GROUND, SARTRE, sc, mood=mood, pose=pose, turn=turn, seed=1, talk=talk)
    hy = GROUND - 842 * sc * SARTRE.height
    pipe(g, x + 6 * sc + turn * 20 * sc, hy + 58 * sc, 0.55 * sc / 0.85, 0, t, smoke)


def stamp(g, x, y, txt, k, rot=-12, col=RED, w=520):
    if k <= 0:
        return
    with g.at(x, y, k * (1 + 0.6 * (1 - min(1, k))), rot):
        g.rrect(-w / 2, -70, w, 140, 16, (1, 1, 1, 0.85), 10, stroke=col)
        g.label(txt, 0, 0, 74, color=col)


# ------------------------------------------------------------------ 1. hook
def s_hook(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # วันที่ + โนเบลช็อก
        medal(g, CX, 860, 230, 1.0, 6 * math.sin(t))
        g.sunburst(CX, 860, 260, 520, 20, t * 10, 10, (0.95, 0.85, 0.55, 0.6))
        if t < L[1] - 0.2:
            g.label("วันนี้ในอดีต", CX, 380, 104, sc=lerp(2.0, 1, e_out(seg(t, 0.1, 0.4))) if t > 0.1 else 0, rot=-4)
            g.label("22 ตุลาคม 1964", CX, 520, 84, color=RED, sc=pop(t, 0.8))
        else:
            g.label("คณะกรรมการโนเบลช็อก!", CX, 400, 80, color=RED, sc=ap(t, L[1]), rot=-4)
            for i in range(3):
                g.label("!", 160 + i * 380, 1150 + 20 * math.sin(t * 6 + i), 90, color=RED, sc=ap(t, L[1] + 0.2 * i))
        return
    if t < L[4] - 0.2:   # นักปราชญ์ชาวฝรั่งเศส ฌอง-ปอล ซาร์ตร์
        bookshelf(g, -100, 1180, 380, 1060)
        sartre(g, CX, 0.9, mood="smug", t=t)
        if t < L[3] - 0.2:
            g.label("นักปราชญ์ชาวฝรั่งเศส", CX, 330, 74, color=NAVY, sc=ap(t, L[2]), rot=-3)
        else:
            g.label('"ฌอง-ปอล ซาร์ตร์"', CX, 330, 88, color=GOLDTXT, sc=ap(t, L[3]), rot=-3)
        g.name_tag(t, L[3] + 0.1, 800, 1120, "ฌอง-ปอล ซาร์ตร์", "นักปรัชญา-นักเขียน (1905–1980)", side=-1)
        return
    if t < L[6] - 0.2:   # ได้รับรางวัล แต่ไม่ไปรับ
        sartre(g, 260, 0.8, mood="neutral" if t < L[5] else "smug", pose="cross" if t > L[5] else "down", turn=0.4, t=t)
        k = ap(t, L[4])
        medal(g, 740, 720, 170, k, 8 * math.sin(t * 2), label="โนเบลวรรณกรรม")
        if t > L[5] - 0.2:
            g.line([(600, 1080), (900, 1080)], 10, GREY, amp=0)
            g.label("ไม่ไปรับ?", 750, 1160, 62, color=GREY, sc=ap(t, L[5]))
        g.label("ผู้ชนะรางวัลโนเบล!", CX, 340, 80, color=GOLDTXT, sc=k, rot=-3)
        return
    if t < L[7] - 0.2:   # ประกาศผ่านหนังสือพิมพ์
        newspaper(g, CX, 780, 0.95 * ap(t, L[6]), -3 + math.sin(t), "SARTRE REFUSE LE PRIX NOBEL")
        return
    sartre(g, 300, 0.85, mood="firm", pose="stop", turn=0.3, t=t, smoke=False)   # "ผมขอปฏิเสธ!"
    medal(g, 790, 720, 150, 1.0, 0, dim=0.6)
    stamp(g, 780, 720, "ปฏิเสธ!", ap(t, L[7] + 0.1), -14, RED, 380)
    g.label('"ผมขอปฏิเสธ!"', CX, 340, 96, color=RED, sc=ap(t, L[7]), rot=-4)


# ------------------------------------------------------------------ 2. philosophy
def s_philosophy(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:   # โนเบลคือความฝันของนักเขียน
        for i, lk in enumerate(CRITICS):
            person(g, 170 + i * 180, GROUND, lk, 0.55, mood="smile", pose="wave" if i == 1 else "down", turn=0.3, seed=10 + i,
                   shadow=False)
        medal(g, 800, 760, 150, 1.0 + 0.04 * math.sin(t * 3))
        g.sunburst(800, 760, 170, 320, 16, t * 10, 8, (0.95, 0.85, 0.55, 0.6))
        g.label("ความฝันสูงสุดของนักเขียน", CX, 360, 70, color=GOLDTXT, sc=ap(t, 0.2), rot=-3)
        return
    if t < L[3] - 0.2:   # อัตถิภาวนิยม: อิสรภาพกำหนดชีวิตตัวเอง
        sartre(g, 280, 0.82, mood="smug", pose="think", turn=0.4, t=t)
        with g.at(760, 760 + 14 * math.sin(t * 2), ap(t, L[1] + 0.2), 3 * math.sin(t * 1.5)):
            g.rrect(-230, -160, 460, 320, 30, WHITE, 6)
            g.label("อัตถิภาวนิยม", 0, -60, 56, color=NAVY)
            g.label("Existentialism", 0, 20, 44, color=GREY)
        for i in range(3):   # ความคิดลอยขึ้นจากหัว
            u = (t * 0.45 + i / 3) % 1
            g.circle(330 + 40 * u + 20 * math.sin(t * 2 + i), 560 - 260 * u, 14 + 22 * u, WHITE, 5)
        if t > L[2] - 0.2:
            bird_free(g, lerp(560, 960, (t - L[2]) * 0.2 % 1), 500 - 40 * math.sin(t), 0.9 * ap(t, L[2]), t)
            g.label("อิสรภาพสูงสุด", 760, 1100, 66, color=GREEN, sc=ap(t, L[2] + 0.3))
        return
    # รับรางวัล = โซ่ตรวนทางความคิด
    sartre(g, CX, 0.82, mood="worry" if t > L[4] else "neutral", pose="down", turn=0.0, t=t)
    if t < L[4] - 0.2:
        medal(g, 260, 640, 110, ap(t, L[3]))
        money_stack(g, 820, 760, 5, ap(t, L[3] + 0.4))
        g.label("เงิน + เกียรติยศจากสถาบัน", CX, 360, 66, sc=ap(t, L[3]), rot=-3)
    else:
        k = e_out(seg(t, L[4] - 0.2, L[4] + 0.8))
        chain(g, CX - 300 * k, 760, CX + 300 * k, 760, 0.0)
        g.label('"โซ่ตรวนทางความคิด"', CX, 360, 78, color=RED, sc=ap(t, L[4]), rot=-3)
        if t > L[5] - 0.2:
            g.label("กรอบชนชั้นสูง", CX, 520, 60, color=GREY, sc=ap(t, L[5]))


# ------------------------------------------------------------------ 3. stance
def s_stance(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[4] - 0.2:   # ปฏิเสธเกียรติยศทุกรูปแบบ
        sartre(g, 260, 0.8, mood="firm", pose="stop", turn=0.4, t=t, smoke=False)
        if t < L[2] - 0.2:
            g.label("จุดยืนชัดเจน", CX, 360, 90, sc=ap(t, 0.2), rot=-3)
            for i in range(3):
                g.label("✕".replace("✕", "ไม่"), 600 + i * 150, 760 + 30 * math.sin(t * 3 + i), 60, color=RED,
                        sc=ap(t, L[1] + 0.3 * i), rot=(i - 1) * 10)
            return
        if t < L[3] - 0.2:
            legion(g, 760, 760, 1.4 * ap(t, L[2]))
            stamp(g, 760, 800, "ไม่รับ", ap(t, L[2] + 1.2), 12, RED, 300)
            g.label("เลฌียงดอเนอร์", CX, 360, 80, color=RED, sc=ap(t, L[2]), rot=-3)
        else:
            with g.at(760, 780, ap(t, L[3])):
                g.rrect(-220, -180, 440, 360, 16, hexc("#f4efe2"), 6)
                g.label("ศาสตราจารย์", 0, -60, 56, color=NAVY)
                g.label("วิทยาลัยฝรั่งเศส", 0, 20, 40, color=GREY)
            stamp(g, 760, 820, "ไม่รับ", ap(t, L[3] + 1.0), 12, RED, 300)
            g.label("ตำแหน่งศาสตราจารย์", CX, 360, 74, color=RED, sc=ap(t, L[3]), rot=-3)
        return
    if t < L[6] - 0.2:   # อิสระทางจิตวิญญาณ / ไม่ให้ใครตีตรา
        sartre(g, CX, 0.85, mood="smile", pose="down", turn=0.0, t=t)
        for i in range(6):
            a = t * 0.8 + i * math.pi / 3
            bird_free(g, CX + 340 * math.cos(a), 700 + 200 * math.sin(a), 0.5, t + i)
        if t < L[5] - 0.2:
            g.label('"อิสระทางจิตวิญญาณ"', CX, 360, 76, color=GREEN, sc=ap(t, L[4]), rot=-3)
        else:
            g.label("ไม่ให้ใครตีตราคุณค่า", CX, 360, 76, color=NAVY, sc=ap(t, L[5]), rot=-3)
        return
    # ไม่เป็นเครื่องมือของฝ่ายใด: ทุนนิยม vs คอมมิวนิสต์ ดึงคนละข้าง
    pull = 20 * math.sin(t * 2)
    sartre(g, CX, 0.8, mood="firm", pose="cross", turn=0.0, t=t, smoke=False)
    for i, (txt, col, x) in enumerate((("ทุนนิยม", hexc("#3f6496"), 220), ("คอมมิวนิสต์", RED, 850))):
        with g.at(x + (pull if i == 0 else -pull), 640, ap(t, L[6] + 0.4 * i)):
            g.rrect(-115, -60, 230, 120, 30, WHITE, 6, stroke=col)
            g.label(txt, 0, 0, 40, color=col)
        if ap(t, L[6] + 0.4 * i) > 0.5:
            g.line([(x + (115 if i == 0 else -115), 640), (CX + (-60 if i == 0 else 60), 760)], 5, col, amp=0)
    if t < L[7] - 0.2:
        g.label("ไม่เป็นเครื่องมือของใคร", CX, 360, 74, sc=ap(t, L[6]), rot=-3)
    else:
        g.label("ไม่เลือกข้าง!", CX, 360, 90, color=GOLDTXT, sc=ap(t, L[7]), rot=-3)


# ------------------------------------------------------------------ 4. refuse
def s_refuse(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[3] - 0.2:   # ข้อบังคับ + เงินรางวัล -> ยืนกรานปฏิเสธ
        for i, lk in enumerate(COMMITTEE[:2]):
            person(g, 140 + i * 200, GROUND, lk, 0.6, mood="worry", pose="hold" if i == 0 else "point", turn=0.4,
                   seed=20 + i, shadow=False)
        sartre(g, 860, 0.78, mood="firm", pose="stop", turn=-0.4, t=t, smoke=False)
        k = e_io(seg(t, 0.3, L[2]))
        if t < L[1] - 0.2:
            envelope(g, lerp(380, 600, k), 520, 0.7)
            g.label("งัดข้อบังคับ!", CX, 360, 84, color=NAVY, sc=ap(t, 0.2), rot=-3)
        elif t < L[2] - 0.2:
            money_stack(g, lerp(420, 600, seg(t, L[1], L[2])), 860, 7, 1.0)
            g.label("ส่งเงินรางวัลมหาศาล", CX, 360, 78, color=GREEN, sc=ap(t, L[1]), rot=-3)
        else:
            money_stack(g, lerp(600, 380, e_io(seg(t, L[2], L[2] + 1.2))), 860, 7, 1.0)
            g.label("ปฏิเสธไร้เยื่อใย!", CX, 360, 86, color=RED, sc=ap(t, L[2]), rot=-4)
        return
    for i, lk in enumerate(CRITICS):   # เสียงวิพากษ์วิจารณ์ทั่วโลก
        x = 170 + i * 370
        person(g, x, GROUND, lk, 0.62, mood="angry" if i != 1 else "shock", pose="point" if i == 0 else "down",
               turn=0.3 - 0.3 * i, seed=30 + i, talk=True)
    if t < L[4] - 0.2:
        for i in range(4):
            u = (t * 0.7 + i / 4) % 1
            g.label("?!", 180 + i * 240, 620 - 120 * u, 70, color=RED, a=1 - u)
        g.label("ตกตะลึงไปทั้งโลก!", CX, 360, 82, color=RED, sc=ap(t, L[3]), rot=-3)
        return
    for i, (txt, col, x) in enumerate((("เย่อหยิ่ง?", RED, 290), ("ซื่อตรง?", GREEN, 790))):   # เย่อหยิ่ง หรือ ซื่อตรง
        with g.at(x, 640, ap(t, L[4] + i * (L[5] - L[4])) * (1 + 0.05 * math.sin(t * 3 + i))):
            g.bubble(0, 0, 360, 140, WHITE, tail=(1 if i == 0 else -1, 1))
            g.label(txt, 0, 0, 62, color=col)
    g.label("หรือ", CX, 640, 54, color=GREY, sc=ap(t, L[5]))


# ------------------------------------------------------------------ 5. lesson
def s_lesson(g, t, L, d):
    g.ground(GROUND, WHITE)
    g.label("บทเรียน", CX, 340, 100, sc=ap(t, 0.2), rot=-3)
    if t < L[2] - 0.2:   # ทุกคนวิ่งไล่ตามคำยกย่อง
        for i, lk in enumerate(CRITICS):
            x = (i * 300 + (t - L[1]) * 260) % 1400 - 200
            person(g, x, GROUND, lk, 0.5, pose="point", turn=0.6, seed=40 + i, shadow=False)
        medal(g, (2 * 300 + (t - L[1]) * 260) % 1400 + 80, 900, 70, ap(t, L[1]))
        if t > L[1] - 0.2:
            g.label("วิ่งไล่ตามคำยกย่อง", CX, 520, 66, color=GREY, sc=ap(t, L[1]))
        return
    sartre(g, CX, 0.85, mood="smile", pose="down", turn=0.0, t=t)   # จิตวิญญาณมั่นคง
    g.sunburst(CX, 740, 260, 560, 18, t * 8, 10, (0.95, 0.85, 0.55, 0.5))
    if t < L[3] - 0.2:
        g.label('รักษา "จิตวิญญาณ"', CX, 520, 70, color=GOLDTXT, sc=ap(t, L[2]))
    else:
        g.label("ยากและมีค่าที่สุด", CX, 520, 76, color=GOLDTXT, sc=ap(t, L[3]))


# ------------------------------------------------------------------ 6. outro
def s_outro(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[5] - 0.2:   # ถ้าคุณเป็นซาร์ตร์: รับ vs ปฏิเสธ
        if t < L[3] - 0.2:
            with g.at(0, 18 * math.sin(t * 2)):
                money_stack(g, 360, 980, 8, 1.2 * ap(t, 0.3))
            g.sunburst(760, 760, 190, 300, 14, t * 12, 8, (0.95, 0.85, 0.55, 0.5 * ap(t, 0.6)))
            medal(g, 760, 760 - 16 * math.sin(t * 2 + 1), 160, ap(t, 0.6), 10 * math.sin(t * 1.6))
            if t > L[2] - 0.2:
                chain(g, 140, 1080, 940, 1080, 0.0, 10)
            g.label("ถ้าคุณเป็นซาร์ตร์...", CX, 360, 80, sc=ap(t, 0.2), rot=-3)
            return
        for i, (txt, col, x) in enumerate((("รับไว้", GOLDTXT, 270), ("ปฏิเสธ", GREEN, 810))):
            k = ap(t, L[3] + i * (L[4] - L[3]))
            with g.at(x, 780, k * (1 + 0.04 * math.sin(t * 3 + i))):
                g.rrect(-200, -240, 400, 480, 40, WHITE, 7)
                if i == 0:
                    money_stack(g, 0, 40, 5, 0.9)
                else:
                    bird_free(g, 0, -20, 1.0, t)
                g.label(txt, 0, 160, 66, color=col)
        g.label("หรือ", CX, 780, 60, color=GREY, sc=ap(t, L[4]))
        g.label("คุณจะเลือกแบบไหน?", CX, 360, 78, sc=ap(t, L[3]), rot=-3)
        return
    with g.at(CX + 120, 650, ap(t, L[5])):   # ชวนคอมเมนต์
        g.bubble(0, 0, 520, 240, WHITE, tail=(-1, 1))
        for i in range(3):
            g.circle(-110 + i * 110, 0, 24 + 6 * math.sin(t * 6 - i), INK, 0)
    sartre(g, 250, 0.8, mood="smile", pose="wave", turn=0.3, t=t, talk=True)
    g.label("คอมเมนต์คุยกันได้เลย!", 700, 1000, 58, color=RED, sc=ap(t, L[5] + 0.4))


SCENES = {
    "hook": s_hook, "philosophy": s_philosophy, "stance": s_stance, "refuse": s_refuse, "lesson": s_lesson,
    "outro": s_outro,
}
NO_IRIS = set()
