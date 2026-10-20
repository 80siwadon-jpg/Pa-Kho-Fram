"""ฉากตอน: อันโตนี ฟาน เลเวนฮุก (เกิด 24 ต.ค. 1632) — พ่อค้าผ้าผู้ค้นพบจุลินทรีย์"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from chars import (BUG, LEEU, SCHOLARS, beetle, book, cloth_bolts, compound_scope, cradle, crossed,  # noqa: E402
                   drop, dutch_houses, key, lens_bead, lens_view, letter, medicine, microbes, microscope, tooth,
                   university, weave, windmill)
from gfx import GOLD2, GREY, INK, NAVY, RED, W, WHITE, e_io, e_out, hexc, lerp, pop, seg  # noqa: E402
from people import head, person  # noqa: E402

CX = W / 2
GROUND = 1270
GOLDTXT = hexc("#b37a12")
GREEN = hexc("#3c8d4f")
BLUE = hexc("#3d6fa8")
PURPLE = hexc("#7a4a9a")

CAMERA = {"hook": "push_in", "draper": "pan_right", "lens": "push_in", "look": "pan_left", "wow": "dutch",
          "name": "pull_out", "doubt": "pan_right", "proof": "push_in", "legacy": "tilt_up", "lesson": "pull_out",
          "outro": "pan_left"}
TRANSITIONS = {"draper": "fade", "lens": "zoom", "look": "whip", "wow": "iris", "name": "zoom", "doubt": "whip",
               "proof": "fade", "legacy": "zoom", "lesson": "fade", "outro": "whip"}


def ap(t, a, dur=0.38):
    return pop(t, a - 0.2, dur)


def title(g, t, a, txt, col=INK, size=84, y=380):
    g.label(txt, CX, y, size, color=col, sc=ap(t, a), rot=-3)


def leeu(g, x, sc=0.8, mood="smile", pose="down", turn=0.2, talk=False, t=0.0):
    person(g, x, GROUND + 6 * math.sin(t * 2.2), LEEU, sc, mood=mood, pose=pose, turn=turn, talk=talk, seed=5)


def scholars(g, t, x0=170, gap=300, sc=0.62, mood="smug", talk=False, shake=0.0, pose="down"):
    for i in range(3):
        tr = 0.4 * math.sin(t * 9 + i) * shake + 0.3 - 0.3 * i
        person(g, x0 + i * gap, GROUND, SCHOLARS[i], sc, mood=mood, pose=pose if i != 1 else "cross", turn=tr,
               talk=talk, seed=20 + i)


def crowd_icon(g, x, y, sc=1.0, col=GREY):
    with g.at(x, y, sc):
        g.circle(0, -60, 22, col, 4)
        g.rrect(-30, -34, 60, 60, 24, col, 4)


# ------------------------------------------------------------------ 1. hook
def s_hook(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # วันที่ + ทารกในเดลฟท์
        dutch_houses(g, GROUND, -420, 9, 0.9)
        windmill(g, 900, GROUND, 0.7, t)
        cradle(g, CX - 100, GROUND - 40, 1.15 * pop(t, 0.3), t)
        if t < L[1] - 0.2:
            g.label("วันนี้ในอดีต", CX, 380, 104, sc=lerp(2.0, 1, e_out(seg(t, 0.1, 0.4))) if t > 0.1 else 0, rot=-3)
            g.label("24 ตุลาคม 1632", CX, 520, 84, color=GOLDTXT, sc=pop(t, 0.8))
        else:
            title(g, t, L[1], "เมืองเดลฟท์ เนเธอร์แลนด์", BLUE, 78)
        return
    if t < L[4] - 0.2:   # พ่อค้าผ้าธรรมดา ไม่เรียนมหาลัย ไม่รู้ละติน
        cloth_bolts(g, 760, 900, 0.7, t)
        leeu(g, 300, 0.75, "smile", "hold", t=t)
        if t < L[3] - 0.2:
            title(g, t, L[2], "พ่อค้าผ้าธรรมดา ๆ")
        else:
            university(g, 780, 560, 0.55 * ap(t, L[3]))
            crossed(g, 780, 470, 0.9, ap(t, L[3] + 0.3))
            book(g, 690, 1100, 0.6 * ap(t, L[3] + 0.6), -8, "Latin")
            crossed(g, 690, 1100, 0.8, ap(t, L[3] + 0.9))
            title(g, t, L[3], "ไม่เคยเรียนมหาวิทยาลัย", RED, 76, y=300)
        return
    if t < L[6] - 0.2:   # ประตูสู่จักรวาลลี้ลับ
        k = ap(t, L[4])
        with g.at(CX + 120, 760, k):
            g.rrect(-200, -330, 400, 640, 30, hexc("#20304a"), 8)
            microbes(g, 0, 0, 190, t, 0.8, 3)
            op = e_io(seg(t, L[4] + 0.3, L[4] + 1.6))
            with g.at(-200, 0, 1, sx=max(0.05, 1 - op), sy=1):
                g.rrect(0, -330, 400, 640, 20, hexc("#8a5a3a"), 8)
                g.circle(340, 0, 18, GOLD2, 4)
        leeu(g, 220, 0.7, "shock", "point", turn=0.4, t=t)
        if t < L[5] - 0.2:
            title(g, t, L[4], "ประตูสู่จักรวาลลี้ลับ", PURPLE, 80, y=300)
        else:
            title(g, t, L[5], "ทั้งโลกได้รู้ว่า...", INK, 84, y=300)
        return
    # สิ่งมีชีวิตนับล้านบนร่างกายเรา
    with g.at(380, 0, 1.0):
        person(g, 0, GROUND, SCHOLARS[1], 0.85, mood="shock", pose="shrug", turn=0, seed=9)
    lens_view(g, 760, 820, 230 * ap(t, L[6]), t, "bugs", 1.0, 1) if ap(t, L[6]) > 0.05 else None
    g.line([(520, 900), (600, 860)], 8, INK, amp=0)
    title(g, t, L[6], "สิ่งมีชีวิตนับล้านบนตัวเรา!", RED, 74, y=330)


# ------------------------------------------------------------------ 2. draper
def s_draper(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # ชื่อ + ร้านผ้า
        cloth_bolts(g, 760, 640, 0.7, t)
        cloth_bolts(g, 760, 1130, 0.75 * ap(t, L[0] + 3.4), t)
        leeu(g, 260, 0.85, "smile", "wave" if t < L[1] else "hold", t=t)
        g.name_tag(t, L[0] + 0.1, 700, 1150, "อันโตนี ฟาน เลเวนฮุก", "พ่อค้าผ้าแห่งเมืองเดลฟท์")
        if t > L[1] - 0.2:
            title(g, t, L[1], "เปิดร้านขายผ้า", GOLDTXT, 88)
        return
    if t < L[4] - 0.2:   # สนใจเลนส์ -> ส่องเส้นด้าย
        leeu(g, 260, 0.75, "smile", "spy", turn=0.5, t=t)
        k = ap(t, L[2])
        lens_bead(g, 420, 640, 34 * k, t) if k > 0.05 else None
        if t > L[3] - 0.2:
            weave(g, 720, 760, 230 * ap(t, L[3]) + 1, 1.0)
            title(g, t, L[3], "ส่องเส้นด้ายในเนื้อผ้า", BLUE, 80, y=330)
        else:
            title(g, t, L[2], "สนใจเลนส์ขยาย", BLUE, 88, y=330)
        return
    # ย้อมแมวขาย
    weave(g, 340, 780, 200, 1.0)
    weave(g, 760, 780, 200 * ap(t, L[4]) + 1, 0.45)
    g.label("ผ้าดี", 340, 1040, 56, color=GREEN)
    g.label("ผ้าโกง", 760, 1040, 56, color=RED, sc=ap(t, L[4]))
    crossed(g, 760, 780, 1.2, ap(t, L[4] + 0.4))
    title(g, t, L[4], "ไม่ให้โดนย้อมแมวขาย!", RED, 84, y=380)


# ------------------------------------------------------------------ 3. lens
def s_lens(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # หลงใหล -> ฝนเลนส์อย่างบ้าคลั่ง
        leeu(g, 320, 0.85, "smile" if t < L[1] else "firm", "hold", turn=0.3, t=t)
        g.rrect(-200, GROUND - 330, 1500, 40, 8, hexc("#8a6a42"), 6) if False else None
        if t < L[1] - 0.2:
            for i in range(5):
                lens_bead(g, 640 + 70 * math.cos(t * 1.4 + i * 1.26), 760 + 70 * math.sin(t * 1.4 + i * 1.26), 26, t + i)
            title(g, t, L[0], "ความหลงใหลพาถลำลึก", PURPLE, 80)
        else:
            with g.at(700, 900, ap(t, L[1]), 20 * math.sin(t * 14)):
                g.rrect(-120, -40, 240, 80, 20, hexc("#9aa0a8"), 6)   # หินฝน
            lens_bead(g, 700 + 30 * math.sin(t * 14), 830, 30, t)
            for i in range(6):   # ประกายฝน
                u = (t * 2 + i / 6) % 1
                g.sparkle(700 + 160 * math.cos(i), 830 - 120 * u, 18 * (1 - u))
            title(g, t, L[1], "ฝนเลนส์อย่างบ้าคลั่ง!", RED, 84)
        return
    if t < L[4] - 0.2:   # เท่าหัวเข็มหมุด -> 300 เท่า
        if t < L[3] - 0.2:
            k = ap(t, L[2])
            with g.at(CX, 820, k):
                g.line([(-40, -320), (60, 300)], 10, GREY, amp=0)   # เข็มหมุด
                g.circle(-46, -340, 46, RED, 6)
                lens_bead(g, 160, -330, 40, t)
            g.label("หัวเข็มหมุด", CX - 160, 560, 54, sc=k)
            g.label("เลนส์", CX + 170, 560, 54, color=BLUE, sc=k)
            title(g, t, L[2], "เล็กเท่าหัวเข็มหมุด", INK, 84, y=330)
        else:
            microscope(g, 300, 760, 1.1 * ap(t, L[3]), 8 * math.sin(t * 2), t)
            n = int(lerp(1, 300, e_out(seg(t, L[3], L[3] + 1.6))))
            g.label(f"x{n}", 720, 780, 170, color=RED, sc=ap(t, L[3]))
            title(g, t, L[3], "ขยายเกือบ 300 เท่า!", RED, 88, y=330)
        return
    # ล้ำหน้ากล้องของนักวิทยาศาสตร์ยุคนั้น
    compound_scope(g, 300, 1100, 0.9 * ap(t, L[4]))
    microscope(g, 760, 800, 0.9 * ap(t, L[4] + 0.3), 6 * math.sin(t * 2), t)
    g.label("ภาพมัว", 300, 1180, 54, color=GREY, sc=ap(t, L[4]))
    g.label("คมชัดกว่า!", 760, 1180, 60, color=GREEN, sc=ap(t, L[4] + 0.3))
    if t < L[5] - 0.2:
        title(g, t, L[4], "ล้ำหน้ากล้องจุลทรรศน์ยุคนั้น", BLUE, 74)
    else:
        title(g, t, L[5], "หลายเท่าตัว!", RED, 100)
        g.star(560, 640, 46 * ap(t, L[5]) + 1, GOLD2, 5)


# ------------------------------------------------------------------ 4. look
def s_look(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # อยากรู้อยากเห็น -> ส่องทุกอย่าง
        leeu(g, 300, 0.85, "smile", "spy", turn=0.5, t=t)
        microscope(g, 430, 650, 0.35, 10, t)
        for i in range(3):
            g.label("?", 650 + i * 120, 600 - 40 * math.sin(t * 3 + i), 110 - i * 15, color=PURPLE, sc=ap(t, L[0] + 0.2 * i))
        if t < L[1] - 0.2:
            title(g, t, L[0], "ความอยากรู้อยากเห็น", PURPLE, 84)
        else:
            title(g, t, L[1], "ส่องทุกสิ่งรอบตัว!", BLUE, 88)
        return
    if t < L[3] - 0.2:   # น้ำฝน ทะเลสาบ เลือด แมลง
        items = [(250, 650, "น้ำฝน"), (760, 650, "ทะเลสาบ"), (250, 1060, "เลือด"), (760, 1060, "แมลง")]
        for i, (x, y, txt) in enumerate(items):
            k = ap(t, L[2] + 0.4 * i)
            if k < 0.02:
                continue
            with g.at(x, y + 8 * math.sin(t * 2 + i), k):
                if i == 0:
                    drop(g, 0, 0, 70, hexc("#9ad0f5"))
                elif i == 1:
                    g.blob(0, 20, 170, 70, hexc("#6aaee0"), 6)
                    g.line([(-80, 10), (-30, 0), (20, 10)], 5, WHITE, amp=0)
                elif i == 2:
                    drop(g, 0, 0, 70, hexc("#d23a3a"))
                else:
                    beetle(g, 0, 0, 1.2, t)
                g.label(txt, 0, 150, 54)
        title(g, t, L[2], "ส่องดูทุกอย่าง", INK, 84, y=330)
        return
    if t < L[4] - 0.2:   # จนกระทั่งวันหนึ่ง...
        leeu(g, CX, 0.85, "smug", "think", turn=0, t=t)
        title(g, t, L[3], "จนกระทั่งวันหนึ่ง...", PURPLE, 90)
        return
    # ขูดคราบพลัคจากฟัน -> ส่องผ่านเลนส์
    if t < L[5] - 0.2:
        tooth(g, 700, 800, 1.5 * ap(t, L[4]) + 0.01, 1.0)
        with g.at(560 + 40 * math.sin(t * 5), 640, ap(t, L[4] + 0.5), -30):   # ไม้ขูด
            g.rrect(-12, -200, 24, 220, 10, hexc("#c9a46a"), 5)
        leeu(g, 220, 0.75, "smile", "point", turn=0.4, t=t)
        title(g, t, L[4], "ขูดคราบพลัคตามซอกฟัน", GOLDTXT, 80, y=330)
    else:
        leeu(g, 300, 0.85, "smile", "spy", turn=0.5, t=t)
        microscope(g, 640, 760, 1.0 * ap(t, L[5]), 6 * math.sin(t * 2), t)
        g.circle(750, 700, 14 * ap(t, L[5] + 0.3) + 0.1, hexc("#efe2a0"), 3)
        title(g, t, L[5], "ส่องผ่านเลนส์!", BLUE, 92, y=330)


# ------------------------------------------------------------------ 5. wow
def s_wow(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:   # แทบหยุดหายใจ
        with g.at(CX, 860, 1.9 * ap(t, L[0]) + 0.01, 3 * math.sin(t * 20)):
            head(g, LEEU, "shock", 0, 0)
        title(g, t, L[0], "แทบหยุดหายใจ!", RED, 100, y=330)
        return
    if t < L[3] - 0.2:   # ไม่ใช่เศษอาหาร
        r = 340
        lens_view(g, CX, 820, r * ap(t, L[1]) + 1, t, "bugs", 0.25 if t < L[2] - 0.2 else 0.0, 2)
        if t > L[2] - 0.2:
            for i in range(5):
                g.blob(CX - 160 + i * 80, 820 + 60 * math.sin(i * 2), 26, 18, hexc("#e8d8a0"), 4, seed=i)
            crossed(g, CX, 820, 1.4, ap(t, L[2] + 0.3))
            title(g, t, L[2], "ไม่ใช่แค่เศษอาหาร!", RED, 86, y=330)
        else:
            title(g, t, L[1], "สิ่งที่ปรากฏตรงหน้า...", INK, 84, y=330)
        return
    if t < L[6] - 0.2:   # นับพันนับหมื่นตัว ว่าย กระดิกหาง รวดเร็ว
        speed = 1.0 if t < L[5] - 0.2 else 2.6
        lens_view(g, CX, 820, 360, t * speed, "bugs", lerp(0.4, 1.6, e_out(seg(t, L[3] - 0.2, L[3] + 1.5))), 4)
        if t < L[4] - 0.2:
            title(g, t, L[3], "สิ่งมีชีวิตจิ๋วนับหมื่น!", GREEN, 84, y=330)
        elif t < L[5] - 0.2:
            title(g, t, L[4], "แหวกว่าย กระดิกหาง", BLUE, 86, y=330)
        else:
            title(g, t, L[5], "มีชีวิตชีวา!", RED, 100, y=330)
        return
    if t < L[7] - 0.2:   # บันทึก
        leeu(g, 280, 0.8, "shock", "sign", turn=0.4, t=t)
        letter(g, 720, 860, 1.3 * ap(t, L[6]) + 0.01, 6, seal=False)
        title(g, t, L[6], "รีบบันทึกไว้!", GOLDTXT, 92, y=330)
        return
    # ในปากเรา > ประชากรทั้งประเทศ
    if t < L[8] - 0.2:
        with g.at(CX, 860, ap(t, L[7])):
            g.blob(0, 0, 320, 220, hexc("#c84a5a"), 8)
            g.blob(0, 30, 250, 150, hexc("#5a1f2a"), 5)
            for i in range(6):
                g.rrect(-200 + i * 70, -170, 56, 60, 12, WHITE, 4)
            microbes(g, 0, 40, 220, t, 0.9, 6)
        title(g, t, L[7], "ในปากของเรา...", RED, 90, y=330)
        return
    k = ap(t, L[8])
    with g.at(300, 820, 1):
        microbes(g, 0, 0, 230, t, 1.4, 7)
    g.label("สัตว์จิ๋วในปาก 1 คน", 300, 1120, 48, color=GREEN)
    for i in range(12):
        crowd_icon(g, 640 + (i % 4) * 90, 700 + (i // 4) * 150, 0.9 * pop(t, L[8] - 0.2 + 0.05 * i))
    g.label("ประชากรทั้งประเทศ", 770, 1120, 48, color=GREY, sc=k)
    g.label(">", 520, 820, 130, color=RED, sc=k)
    title(g, t, L[8], "มากกว่าคนทั้งประเทศ!", RED, 86, y=330)


# ------------------------------------------------------------------ 6. name
def s_name(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # แอนิมอลคูลส์ สัตว์ตัวจิ๋ว
        lens_view(g, CX, 820, 310, t, "bugs", 0.6, 9)
        title(g, t, L[0], "ตั้งชื่ออย่างน่ารักว่า...", INK, 72, y=300)
        if t > L[1] - 0.2:
            g.label("\"Animalcules\"", CX, 440, 96, color=PURPLE, sc=ap(t, L[1]), rot=-3)
            g.label("สัตว์ตัวจิ๋ว", CX, 1220, 80, color=GREEN, sc=ap(t, L[1] + 0.5))
        return
    microbes(g, 300, 820, 260, t, 0.7, 11)
    microbes(g, 760, 820, 260, t, 0.7, 12)
    title(g, t, L[2], "แบคทีเรียและจุลินทรีย์", GREEN, 84, y=330)
    if t > L[3] - 0.2:
        with g.at(CX, 860, ap(t, L[3]), -4):
            g.rrect(-330, -90, 660, 180, 40, WHITE, 8, stroke=RED)
            g.label("ค้นพบครั้งแรกของโลก!", 0, 0, 64, color=RED)


# ------------------------------------------------------------------ 7. doubt
def s_doubt(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # ส่งจดหมายไปราชสมาคมลอนดอน
        if t < L[1] - 0.2:
            u = e_io(seg(t, 0.2, L[1] - 0.3))
            letter(g, lerp(200, 820, u), lerp(1000, 640, u) - 80 * math.sin(u * math.pi), 0.8, lerp(-10, 15, u))
            g.label("เดลฟท์", 180, 1180, 56, color=BLUE)
            g.label("ลอนดอน", 860, 1180, 56, color=RED, sc=pop(t, 0.5))
            title(g, t, L[0], "ส่งจดหมายถึงลอนดอน", INK, 84, y=330)
        else:
            scholars(g, t, mood="firm")
            title(g, t, L[1], "นักวิทยาศาสตร์ชั้นนำของโลก", NAVY, 74, y=330)
        return
    if t < L[5] - 0.2:   # หัวเราะเยาะ ส่ายหน้า เพ้อเจ้อ โกหก
        laugh = t < L[3] - 0.2
        scholars(g, t, mood="smug" if laugh else "angry", talk=True, shake=0.0 if laugh else 1.0,
                 pose="shrug" if laugh else "down")
        if laugh:
            for i in range(3):
                g.label("ฮ่า ๆ", 170 + i * 300, 640 - 20 * math.sin(t * 8 + i), 60, color=RED, sc=ap(t, L[2] + 0.2 * i),
                        rot=-8 + 8 * i)
            title(g, t, L[2], "มีแต่เสียงหัวเราะเยาะ!", RED, 84, y=330)
        elif t < L[4] - 0.2:
            title(g, t, L[3], "ส่ายหน้า ตราหน้าว่า...", INK, 80, y=330)
        else:
            for i, txt in enumerate(("เพ้อเจ้อ!", "โกหก!")):
                with g.at(300 + i * 480, 600, ap(t, L[4] + 0.3 * i), -5 + 10 * i):
                    g.bubble(0, 0, 360, 150, WHITE, tail=(1 - 2 * i, 1))
                    g.label(txt, 0, 0, 64, color=RED)
            title(g, t, L[4], "พ่อค้าผ้ากำลังโกหก!", RED, 80, y=330)
        return
    # ยุคนั้นไม่มีใครเชื่อสิ่งที่ตามองไม่เห็น
    with g.at(CX, 860, ap(t, L[5])):
        g.circle(0, 0, 160, WHITE, 8)
        g.circle(0, 0, 70, NAVY, 0)
        g.circle(-24, -24, 22, WHITE, 0)
        g.line([(-200, -200), (200, 200)], 14, RED, amp=0)
    for i in range(6):
        a = t * 0.8 + i
        g.blob(CX + 300 * math.cos(a), 860 + 260 * math.sin(a), 22, 14, BUG[i % 5], 3, seed=i) \
            if t > L[6] - 0.2 else None
    if t < L[6] - 0.2:
        title(g, t, L[5], "ยุคนั้นไม่มีใครเชื่อ", INK, 84, y=330)
    else:
        title(g, t, L[6], "สิ่งมีชีวิตที่ตามองไม่เห็น?", PURPLE, 76, y=330)


# ------------------------------------------------------------------ 8. proof
def s_proof(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:   # ส่งทีมมาพิสูจน์ที่เนเธอร์แลนด์
        windmill(g, 820, GROUND, 0.8, t)
        u = e_io(seg(t, 0.2, L[1] - 0.4))
        for i in range(3):
            person(g, lerp(-200, 200, u) + i * 170, GROUND, SCHOLARS[i], 0.5, mood="firm", turn=0.6, seed=30 + i,
                   pose="down")
        title(g, t, L[0], "เดินทางมาพิสูจน์ถึงเนเธอร์แลนด์", BLUE, 68, y=330)
        return
    if t < L[2] - 0.2:   # ก้มลงมองผ่านเลนส์
        microscope(g, 560, 820, 0.8, 5, t)
        person(g, 340, GROUND, SCHOLARS[0], 0.75, mood="shock", pose="spy", turn=0.5, lean=10, seed=40)
        leeu(g, 860, 0.7, "smug", "down", turn=-0.4, t=t)
        lens_view(g, 720, 560, 160 * ap(t, L[1] + 0.8) + 1, t, "bugs", 0.5, 13)
        title(g, t, L[1], "ก้มลงมองผ่านเลนส์...", INK, 80, y=300)
        return
    # ก้มหัวยอมรับ
    for i in range(3):
        person(g, 130 + i * 200, GROUND, SCHOLARS[i], 0.6, mood="worry", pose="down",
               lean=lerp(0, 10, e_io(seg(t, L[2], L[2] + 0.8))), seed=50 + i, turn=0.4)
    leeu(g, 880, 0.7, "smile", "fist", turn=-0.4, t=t)
    g.sparkle(880, 560, 40 * ap(t, L[2] + 0.4) + 1)
    title(g, t, L[2], "ยอมรับความจริง!", GREEN, 96, y=330)


# ------------------------------------------------------------------ 9. legacy
def s_legacy(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # กำเนิดจุลชีววิทยา
        leeu(g, 260, 0.75, "smile", "hold", turn=0.3, t=t)
        book(g, 720, 860, 1.4 * ap(t, L[1]) + 0.01, 4, "จุลชีววิทยา", hexc("#3c8d4f"))
        microbes(g, 720, 840, 70, t, 0.3, 14) if ap(t, L[1]) > 0.9 else None
        if t < L[1] - 0.2:
            title(g, t, L[0], "พ่อค้าผ้าผู้ไม่ยอมจำนน", GOLDTXT, 80)
        else:
            title(g, t, L[1], "กำเนิด \"จุลชีววิทยา\"", GREEN, 88)
        return
    if t < L[3] - 0.2:   # กุญแจสู่การแพทย์ เข้าใจเชื้อโรค
        key(g, 380, 820, 1.2 * ap(t, L[2]) + 0.01, -10 + 6 * math.sin(t * 2))
        medicine(g, 800, 1050, 1.2 * ap(t, L[2] + 0.4) + 0.01, t)
        title(g, t, L[2], "กุญแจสู่การเข้าใจเชื้อโรค", BLUE, 78)
        return
    # ช่วยชีวิตผู้คนนับร้อยล้าน
    for i in range(16):
        crowd_icon(g, 180 + (i % 8) * 100, 820 + (i // 8) * 180, 0.9 * pop(t, L[3] + 0.06 * i),
                   [GREEN, BLUE, GOLD2, hexc("#d76b5a")][i % 4])
    medicine(g, CX, 700, 0.6 * ap(t, L[3]) + 0.01, t)
    title(g, t, L[3], "ช่วยชีวิตนับร้อยล้านคน!", GREEN, 84)


# ------------------------------------------------------------------ 10. lesson
def s_lesson(g, t, L, d):
    g.ground(GROUND, WHITE)
    leeu(g, 300, 0.85, "smile", "spy" if t < L[1] else "fist", turn=0.4, t=t)
    if t < L[1] - 0.2:
        title(g, t, L[0], "เรื่องราวของเลเวนฮุกพิสูจน์ว่า", INK, 70)
        lens_bead(g, 720, 760, 70 * ap(t, L[0]) + 1, t)
        return
    if t < L[2] - 0.2:
        for i, (txt, col) in enumerate((("อยากรู้อยากเห็น", PURPLE), ("ช่างสังเกต", BLUE))):
            with g.at(740, 640 + i * 240, ap(t, L[1] + 0.5 * i), -3 + 6 * i):
                g.rrect(-230, -70, 460, 140, 36, WHITE, 7, stroke=col)
                g.label(txt, 0, 0, 56, color=col)
        title(g, t, L[1], "ไร้ขีดจำกัด", PURPLE, 90)
        return
    g.label("คนธรรมดา", 760, 1060, 60, color=GREY, sc=ap(t, L[2]))
    g.line([(760, 1000), (760, 800)], 10, GREEN, amp=0)
    g.line([(720, 840), (760, 790), (800, 840)], 10, GREEN, amp=0)
    g.star(760, 680, 90 * ap(t, L[2] + 0.6) + 1, GOLD2, 6)
    title(g, t, L[2], "พลิกโฉมประวัติศาสตร์โลก!", RED, 80)


# ------------------------------------------------------------------ 11. outro
def s_outro(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:   # รู้สึกอย่างไร
        leeu(g, 300, 0.85, "smile", "wave", turn=0.3, talk=True, t=t)
        with g.at(760, 640, ap(t, L[0])):
            g.bubble(0, 0, 360, 240, WHITE, tail=(-1, 1))
            g.label("?", 0, 0, 140, color=PURPLE)
        title(g, t, L[0], "ทุกคนรู้สึกอย่างไรบ้าง?", INK, 80)
        return
    if t < L[3] - 0.2:   # ถ้ามีคนมาบอกว่าในปากมีสัตว์ประหลาดตัวจิ๋ว
        person(g, 220, GROUND, LEEU, 0.8, mood="smile", pose="point", turn=0.5, seed=7, talk=True)
        person(g, 900, GROUND, SCHOLARS[2], 0.75, mood="shock" if t > L[2] else "neutral", pose="shrug", turn=-0.4,
               seed=8)
        if t > L[2] - 0.2:
            lens_view(g, CX + 40, 620, 170 * ap(t, L[2]) + 1, t, "bugs", 0.6, 15)
            title(g, t, L[2], "สัตว์ประหลาดจิ๋วในปากคุณ!", RED, 76, y=300)
        else:
            title(g, t, L[1], "ถ้าคุณเกิดในยุคนั้น...", INK, 84, y=300)
        return
    if t < L[4] - 0.2:   # เชื่อ หรือ บ้า
        for i, (txt, col) in enumerate((("เชื่อ", GREEN), ("บ้าแน่ ๆ!", RED))):
            with g.at(250 + i * 530, 780 + 20 * math.sin(t * 3 + i), ap(t, L[3] + 0.4 * i), -4 + 8 * i):
                g.rrect(-160, -100, 320, 200, 40, WHITE, 8, stroke=col)
                g.label(txt, 0, 0, 64, color=col)
        g.label("หรือ", 515, 780, 60, sc=ap(t, L[3] + 0.2))
        title(g, t, L[3], "คุณจะเชื่อเขาไหม?", PURPLE, 88)
        return
    with g.at(CX + 170, 640, ap(t, L[4])):   # ชวนคอมเมนต์
        g.bubble(0, 0, 460, 220, WHITE, tail=(-1, 1))
        for i in range(3):
            g.circle(-110 + i * 110, 0, 24 + 6 * math.sin(t * 6 - i), INK, 0)
    leeu(g, 260, 0.8, "smile", "wave", turn=0.3, talk=True, t=t)
    title(g, t, L[4], "คอมเมนต์แลกเปลี่ยนกันได้เลย!", RED, 62)


SCENES = {
    "hook": s_hook, "draper": s_draper, "lens": s_lens, "look": s_look, "wow": s_wow, "name": s_name,
    "doubt": s_doubt, "proof": s_proof, "legacy": s_legacy, "lesson": s_lesson, "outro": s_outro,
}
NO_IRIS = set()
