"""ฉากตอน: ดวลปืนที่โอเค คอร์รัล (26 ต.ค. 1881) — ไม่แสดงความรุนแรงตรง ๆ (ควัน แสงวาบ หมวกตกพื้น)"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from chars import (COWBOYS, DOC, MORGAN, SAND, TOWNS, VIRGIL, WYATT, badge, clock, corral, film,  # noqa: E402
                   gold_pile, hat_on_ground, revolver, smoke, snow, town, tumbleweed, wanted)
from gfx import GOLD, GOLD2, GREY, INK, NAVY, RED, W, WHITE, e_io, e_out, hexc, lerp, pop, seg  # noqa: E402
from people import person  # noqa: E402

CX = W / 2
GROUND = 1270
GOLDTXT = hexc("#b37a12")
DUST = hexc("#a8784a")
DARK = hexc("#4a3a3a")

CAMERA = {"hook": "push_in", "town": "pan_right", "walk": "pan_left", "standoff": "push_in", "fight": "dutch",
          "legacy": "pull_out", "lesson": "tilt_up", "outro": "pan_right"}
TRANSITIONS = {"town": "fade", "walk": "whip", "standoff": "zoom", "fight": "whip", "legacy": "fade", "lesson": "iris",
               "outro": "whip"}


def ap(t, a, dur=0.38):
    return pop(t, a - 0.2, dur)


def title(g, t, a, txt, col=INK, size=84, y=380):
    g.label(txt, CX, y, size, color=col, sc=ap(t, a), rot=-3)


def earps(g, t, x0=150, gap=200, sc=0.55, walk=0.0, mood="firm", pose="down"):
    for i, lk in enumerate((VIRGIL, WYATT, MORGAN, DOC)):
        bob = -8 * abs(math.sin(t * 6 + i)) * walk
        person(g, x0 + i * gap, GROUND + bob, lk, sc, mood=mood, pose=pose if i == 1 else "down", turn=0.5,
               seed=10 + i)


def cowboys(g, t, x0=560, gap=150, sc=0.5, mood="angry", n=4):
    for i in range(n):
        person(g, x0 + i * gap, GROUND, COWBOYS[i], sc, mood=mood, pose="cross" if i % 2 else "down", turn=-0.5,
               seed=20 + i)


def flashes(g, t, n=6, y0=620, y1=1050, k=1.0, seed=0):
    from chars import _shade   # noqa: F401
    for i in range(n):
        u = (t * 2.2 + i * 0.37 + seed) % 1
        if u < 0.25:
            a = 1 - u / 0.25
            x = 180 + (i * 173 + int(t * 3) * 61) % 700
            y = y0 + (i * 97) % max(1, y1 - y0)
            g.star(x, y, 70 * k * (0.5 + u * 2), (0.98, 0.66, 0.23, a), 0, pts=9, inner=0.45)
            g.star(x, y, 32 * k, (1, 0.95, 0.75, a), 0, pts=9, inner=0.5)


# ------------------------------------------------------------------ 1. hook
def s_hook(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:
        town(g, GROUND)
        tumbleweed(g, lerp(-100, 900, (t * 0.25) % 1), GROUND - 50, 50, t)
        g.label("วันนี้ในอดีต", CX, 380, 104, sc=lerp(2.0, 1, e_out(seg(t, 0.1, 0.4))) if t > 0.1 else 0, rot=-3)
        g.label("26 ตุลาคม 1881", CX, 520, 84, color=GOLDTXT, sc=pop(t, 0.6))
        return
    if t < L[2] - 0.2:   # 30 นัดใน 30 วินาที
        clock(g, 300, 820, 170, t, ap(t, L[1]))
        revolver(g, 720, 820, 1.0 * ap(t, L[1] + 0.3) + 0.01, -8, (t * 3) % 1 if t > L[1] + 0.5 else 0)
        g.label("30 นัด · 30 วินาที", CX, 1120, 76, color=RED, sc=ap(t, L[1] + 0.4))
        title(g, t, L[1], "เสียงปืนดังระงม!", RED, 96)
        return
    if t < L[3] - 0.2:   # ตรอกแคบ = นรกบนดิน
        corral(g, CX, GROUND, 700, 1.0)
        for i in range(4):
            smoke(g, 200 + i * 220, 1100, 100, t, 5, 0.75, i * 0.3)
        flashes(g, t, 5, 700, 1000)
        title(g, t, L[2], "ตรอกแคบกลายเป็นนรกบนดิน", DARK, 80)
        return
    person(g, 300, GROUND, WYATT, 0.85, mood="firm", pose="down", turn=0.3, seed=1)   # ตำนาน
    person(g, 760, GROUND, DOC, 0.8, mood="smug", pose="cross", turn=-0.3, seed=2)
    for i in range(4):
        g.sparkle(CX + 380 * math.cos(i * 1.57 + t), 700 + 200 * math.sin(i * 1.57 + t), 30)
    title(g, t, L[3], "ตำนานดวลปืนที่โด่งดังที่สุด!", GOLDTXT, 80)


# ------------------------------------------------------------------ 2. town
def s_town(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[3] - 0.2:   # ทูมสโตน เมืองเหมือง
        town(g, GROUND)
        if t < L[1] - 0.2:
            title(g, t, L[0], "26 ตุลาคม 1881", GOLDTXT, 92)
        elif t < L[2] - 0.2:
            title(g, t, L[1], "เมืองทูมสโตน แอริโซนา", DUST, 84)
        else:
            gold_pile(g, 300, 760, 1.2 * ap(t, L[2]) + 0.01, t)
            wanted(g, 720, 760, 0.8 * ap(t, L[2] + 0.4) + 0.01, 6)
            title(g, t, L[2], "ทองคำ เงินตรา กฎหมายไร้ความหมาย", INK, 70)
        return
    if t < L[6] - 0.2:   # ตระกูลเอิร์ป vs เดอะคาวบอยส์
        if t < L[5] - 0.2:
            earps(g, t, 160, 210, 0.58)
            badge(g, 760, 640, 0.9 * ap(t, L[3]) + 0.01, 6 * math.sin(t * 2), t)
            g.name_tag(t, L[4] + 0.1, 360, 1150, "ไวแอตต์ เอิร์ป", "ผู้รักษากฎหมายแห่งทูมสโตน")
            title(g, t, L[3] if t < L[4] - 0.2 else L[4], "\"ตระกูลเอิร์ป\" ผู้รักษากฎหมาย" if t < L[4] - 0.2
                  else "นำโดย ไวแอตต์ เอิร์ป", NAVY, 80)
        else:
            cowboys(g, t, 180, 210, 0.58, "smug")
            title(g, t, L[5], "\"เดอะ คาวบอยส์\" นอกกฎหมาย", RED, 80)
        return
    earps(g, t, 170, 100, 0.42)   # จุดแตกหัก ขู่ฆ่า
    cowboys(g, t, 610, 92, 0.42)
    if t < L[7] - 0.2:
        g.label("VS", CX + 40, 700, 110, color=RED, sc=ap(t, L[6]))
        title(g, t, L[6], "ความตึงเครียดถึงจุดแตกหัก!", RED, 80)
    else:
        for i, (x, txt) in enumerate(((260, "เจอกันแน่!"), (800, "แกตายแน่!"))):
            with g.at(x, 600, ap(t, L[7] + 0.3 * i), -5 + 10 * i):
                g.bubble(0, 0, 300, 120, WHITE, tail=(1 - 2 * i, 1))
                g.label(txt, 0, 0, 46, color=RED)
        title(g, t, L[7], "ปะทะคารม ขู่ฆ่ากันหลายวัน", DARK, 78, y=360)


# ------------------------------------------------------------------ 3. walk
def s_walk(g, t, L, d):
    g.ground(GROUND, WHITE)
    snow(g, t)
    if t < L[1] - 0.2:   # หิมะ หนาวเหน็บ
        town(g, GROUND)
        title(g, t, L[0], "บ่ายวันนั้น หิมะโปรยปราย", NAVY, 82)
        return
    if t < L[4] - 0.2:   # ไวแอตต์ พี่น้อง + ด็อก
        if t < L[2] - 0.2:
            for i, lk in enumerate((VIRGIL, WYATT, MORGAN)):
                person(g, 200 + i * 300, GROUND, lk, 0.65, mood="firm", turn=0.3, seed=10 + i)
            title(g, t, L[1], "ไวแอตต์ และพี่น้องอีกสองคน", NAVY, 78)
        else:
            person(g, 300, GROUND, DOC, 0.85, mood="smug", pose="cross" if t < L[3] - 0.2 else "down", turn=0.3,
                   seed=13)
            g.name_tag(t, L[2] + 0.1, 680, 1150, "ด็อก ฮอลลิเดย์", "อดีตทันตแพทย์ · มือปืน")
            if t < L[3] - 0.2:
                title(g, t, L[2], "เพื่อนสนิท \"ด็อก ฮอลลิเดย์\"", GOLDTXT, 80)
            else:
                with g.at(720, 700, ap(t, L[3])):   # ฟัน + ปืน
                    g.blob(-90, 0, 60, 70, WHITE, 6)
                    revolver(g, 60, 20, 0.6, -10)
                title(g, t, L[3], "ทันตแพทย์ป่วยวัณโรค มือปืนพระกาฬ", DARK, 70)
        return
    u = e_io(seg(t, L[4] - 0.2, L[6] + 1.5))   # เดินเรียงหน้ากระดาน -> โอเค คอร์รัล
    if t > L[5] - 0.2:
        corral(g, 780, GROUND, 360, 0.8)
    earps(g, t, lerp(140, 200, u), 140, 0.5, walk=1.0)
    if t < L[5] - 0.2:
        title(g, t, L[4], "เดินเรียงหน้ากระดาน โค้ตยาวสีดำ", INK, 74)
    elif t < L[6] - 0.2:
        title(g, t, L[5], "มุ่งสู่ \"โอเค คอร์รัล\"", DUST, 86)
    else:
        with g.at(CX, 560, ap(t, L[6]), -4):
            g.rrect(-300, -60, 600, 120, 26, WHITE, 7, stroke=RED)
            g.label("ห้ามพกปืนในเมือง!", 0, 0, 56, color=RED)
        title(g, t, L[6], "ไปปลดอาวุธกลุ่มคาวบอย!", NAVY, 80, y=360)


# ------------------------------------------------------------------ 4. standoff
def s_standoff(g, t, L, d):
    g.ground(GROUND, WHITE)
    snow(g, t, 25)
    if t < L[2] - 0.2:   # ห่างไม่ถึง 2 เมตร / เงียบงัน
        earps(g, t, 170, 105, 0.45)
        cowboys(g, t, 620, 92, 0.45)
        if t < L[1] - 0.2:
            g.line([(520, 560), (640, 560)], 6, RED, amp=0)
            g.label("< 2 ม.", 580, 500, 56, color=RED, sc=ap(t, L[0] + 0.3))
            title(g, t, L[0], "ประจันหน้าไม่ถึง 2 เมตร!", RED, 84, y=330)
        else:
            tumbleweed(g, lerp(150, 950, seg(t, L[1], L[2])), GROUND - 40, 40, t)
            title(g, t, L[1], "ความเงียบงันบีบหัวใจ...", DARK, 84, y=330)
        return
    if t < L[4] - 0.2:   # ไวแอตต์ตะโกน
        person(g, 300, GROUND, WYATT, 0.9, mood="shout", pose="stop", turn=0.4, seed=1, talk=True)
        with g.at(740, 640, ap(t, L[2] + 0.2)):
            g.bubble(0, 0, 420, 260, WHITE, tail=(-1, 1))
            g.label("ยอมจำนนซะ!", 0, -40, 60, color=RED)
            if t > L[3] - 0.2:
                g.label("ถูกปลดอาวุธแล้ว!", 0, 40, 46, sc=ap(t, L[3]))
        title(g, t, L[2], "ไวแอตต์ตะโกนสั่ง...", NAVY, 86, y=330)
        return
    revolver(g, CX, 820, 1.6, -6, ap(t, L[4] + 0.6))   # คำตอบคือเสียงเหนี่ยวไก
    g.label("คลิก!", CX - 160, 1050, 70, color=RED, sc=ap(t, L[4] + 0.2), rot=-8)
    title(g, t, L[4], "คำตอบคือเสียงเหนี่ยวไก!", RED, 86)


# ------------------------------------------------------------------ 5. fight
def s_fight(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[3] - 0.2:   # ปืนระเบิด ควันคลุ้ง ชาวบ้านหนี
        c = g.c
        c.rectangle(-500, 140, 2100, 1130)
        c.set_source_rgba(0.35, 0.32, 0.3, 0.18)
        c.fill()
        corral(g, CX, GROUND, 760, 1.0, sign=False)
        for i in range(5):
            smoke(g, 140 + i * 190, 1150, 120, t, 6, 0.8, i * 0.27)
        flashes(g, t, 7, 600, 1050)
        if t < L[1] - 0.2:
            title(g, t, L[0], "เสียงปืนระเบิดขึ้นอย่างบ้าคลั่ง!", RED, 76)
        elif t < L[2] - 0.2:
            n = int(lerp(1, 30, e_out(seg(t, L[1], L[2]))))
            g.label(f"{n} นัด", CX, 560, 120, color=RED, sc=ap(t, L[1]))
            title(g, t, L[1], "ควันดินปืนคลุ้งทั่วตรอก", DARK, 80)
        else:
            u = seg(t, L[2], L[3])
            for i, lk in enumerate(TOWNS):
                person(g, lerp(600 + 150 * i, 220 + 150 * i, u), GROUND, lk, 0.55, mood="shock", pose="v", turn=-0.8,
                       seed=30 + i)
            title(g, t, L[2], "ชาวบ้านวิ่งหนีตายจ้าละหวั่น!", RED, 78)
        return
    if t < L[6] - 0.2:   # ครึ่งนาที / 3 ศพ / บาดเจ็บ
        if t < L[4] - 0.2:
            clock(g, CX, 820, 200, 15 + t * 0.2)
            smoke(g, CX, 1100, 120, t, 5, 0.5)
            title(g, t, L[3], "สงบลงในเวลาเพียงครึ่งนาที...", DARK, 80)
        elif t < L[5] - 0.2:
            for i, col in enumerate((hexc("#8a6a42"), hexc("#a8844f"), hexc("#6b5a3a"))):
                hat_on_ground(g, 260 + i * 280, GROUND - 10, 1.0 * ap(t, L[4] + 0.3 * i) + 0.01, -15 + 15 * i, col)
            smoke(g, CX, 1100, 120, t, 5, 0.4)
            g.label("ฝ่ายคาวบอย เสียชีวิต 3 ศพ", CX, 760, 66, color=DARK, sc=ap(t, L[4]))
            title(g, t, L[4], "การสูญเสียในตรอกแคบ", DARK, 84)
        else:
            for i, lk in enumerate((VIRGIL, MORGAN, DOC)):
                person(g, 200 + i * 300, GROUND, lk, 0.6, mood="worry", pose="down", turn=0.3, seed=40 + i,
                       lean=8 * (i % 2 * 2 - 1))
                g.rrect(170 + i * 300, 660, 60, 22, 6, WHITE, 4)
            title(g, t, L[5], "ฝ่ายเอิร์ปบาดเจ็บสาหัส", RED, 84)
        return
    smoke(g, 200, 1150, 110, t, 5, 0.5)   # ไวแอตต์ยืนตระหง่าน ไม่มีรอยขีดข่วน
    smoke(g, 880, 1150, 110, t, 5, 0.5, 0.5)
    person(g, CX, GROUND, WYATT, 0.9, mood="firm", pose="down", turn=0, seed=1)
    if t < L[7] - 0.2:
        title(g, t, L[6], "มีเพียงไวแอตต์ที่ยืนตระหง่าน", NAVY, 78)
    else:
        for i in range(5):
            g.sparkle(CX + 300 * math.cos(i * 1.26 + t), 760 + 280 * math.sin(i * 1.26 + t), 32)
        title(g, t, L[7], "ไม่มีแม้แต่รอยขีดข่วน!", GOLDTXT, 86)


# ------------------------------------------------------------------ 6. legacy
def s_legacy(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # ไม่จบ -> สงครามล้างแค้น
        if t < L[1] - 0.2:
            clock(g, 300, 820, 150, 30)
            g.label("ยังไม่จบ...", 720, 820, 90, color=RED, sc=ap(t, L[0] + 0.4))
            title(g, t, L[0], "ความขัดแย้งยังไม่จบลง", DARK, 82)
        else:
            for i in range(3):
                wanted(g, 220 + i * 320, 820, 0.75 * ap(t, L[1] + 0.25 * i) + 0.01, -8 + 8 * i,
                       ["REVENGE", "WANTED", "WANTED"][i])
            title(g, t, L[1], "จุดชนวนสงครามล้างแค้น!", RED, 82)
        return
    if t < L[3] - 0.2:   # สัญลักษณ์ยุคคาวบอยแดนเถื่อน
        badge(g, 300, 800, 1.2, 6 * math.sin(t * 2), t)
        revolver(g, 720, 820, 1.0, -10)
        tumbleweed(g, lerp(150, 950, (t * 0.3) % 1), GROUND - 50, 50, t)
        title(g, t, L[2], "สัญลักษณ์ \"ยุคคาวบอยแดนเถื่อน\"", DUST, 76)
        return
    film(g, 300, 800, 1.2, t)   # หนังและนิยาย
    with g.at(720, 820, ap(t, L[3] + 0.3), 6):
        g.rrect(-150, -200, 300, 400, 10, hexc("#7a3a2a"), 7)
        g.rrect(-110, -150, 220, 120, 6, hexc("#f1e3c0"), 4)
        g.label("O.K. Corral", 0, -90, 40)
        hat_on_ground(g, 0, 120, 0.8)
    title(g, t, L[3], "หนังและนิยายจนถึงปัจจุบัน", NAVY, 82)


# ------------------------------------------------------------------ 7. lesson
def s_lesson(g, t, L, d):
    g.ground(GROUND, WHITE)
    person(g, 260, GROUND, WYATT, 0.8, mood="firm", pose="down", turn=0.4, seed=1)
    person(g, 820, GROUND, COWBOYS[0], 0.8, mood="smug", pose="cross", turn=-0.4, seed=20)
    if t < L[1] - 0.2:
        title(g, t, L[0], "เรื่องนี้เตือนใจเราว่า...", INK, 84)
    else:
        k = ap(t, L[1])
        g.line([(CX, 520), (CX, 520 + 700 * k)], 4, RED, amp=0)
        badge(g, 260, 560, 0.5 * k + 0.01, 0, t, "LAW")
        wanted(g, 820, 520, 0.4 * k + 0.01, 6, "OUTLAW")
        if t < L[2] - 0.2:
            title(g, t, L[1], "เส้นแบ่งผู้พิทักษ์กับคนนอกกฎหมาย", NAVY, 68)
        else:
            title(g, t, L[2], "บางเฉียบเหลือเกิน...", RED, 92)


# ------------------------------------------------------------------ 8. outro
def s_outro(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:
        person(g, 280, GROUND, WYATT, 0.82, mood="firm", pose="down", turn=0.4, seed=1)
        with g.at(740, 640, ap(t, L[0])):
            g.bubble(0, 0, 360, 240, WHITE, tail=(-1, 1))
            g.label("?", 0, 0, 140, color=DUST)
        title(g, t, L[0] if t < L[1] - 0.2 else L[1], "มองศึกนี้อย่างไร?" if t < L[1] - 0.2
              else "การตัดสินใจของไวแอตต์...", INK, 84)
        return
    if t < L[4] - 0.2:   # ยุติธรรม vs อารมณ์
        for i, (txt, col) in enumerate((("ความเด็ดขาด", NAVY), ("ใช้อารมณ์", RED))):
            k = ap(t, L[2] if i == 0 else L[3])
            if k < 0.02:
                continue
            with g.at(CX, 620 + i * 300, k, -3 + 6 * i):
                g.rrect(-300, -100, 600, 200, 40, WHITE, 8, stroke=col)
                g.label(txt, 0, -20, 70, color=col)
                g.label(["ผดุงความยุติธรรม", "จนเรื่องบานปลาย"][i], 0, 50, 40, color=GREY)
        g.label("หรือ", CX, 775, 56, sc=ap(t, L[3]))
        title(g, t, L[2], "คุณมองแบบไหน?", DUST, 88, y=360)
        return
    with g.at(CX + 170, 640, ap(t, L[4])):   # ชวนคอมเมนต์
        g.bubble(0, 0, 460, 220, WHITE, tail=(-1, 1))
        for i in range(3):
            g.circle(-110 + i * 110, 0, 24 + 6 * math.sin(t * 6 - i), INK, 0)
    person(g, 250, GROUND, DOC, 0.8, mood="smug", pose="wave", turn=0.3, seed=70, talk=True)
    title(g, t, L[4], "คอมเมนต์แลกเปลี่ยนกันได้เลย!", RED, 64)


SCENES = {
    "hook": s_hook, "town": s_town, "walk": s_walk, "standoff": s_standoff, "fight": s_fight, "legacy": s_legacy,
    "lesson": s_lesson, "outro": s_outro,
}
NO_IRIS = set()
