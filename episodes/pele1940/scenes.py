"""ฉากตอน: วันเกิดเปเล่ ราชาลูกหนัง (23 ต.ค. 1940)"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from chars import (BR_BLU, BR_GRN, BR_YEL, DAD, DIRT, FANS, KID, PELE, SOLDIERS, ball, favela, gun_down,  # noqa: E402
                   jersey, radio, trophy)
from gfx import GOLD, GOLD2, GREY, INK, NAVY, RED, W, WHITE, e_io, e_out, hexc, lerp, pop, seg  # noqa: E402
from people import person  # noqa: E402

CX = W / 2
GROUND = 1270
GOLDTXT = hexc("#b37a12")
GREEN = hexc("#3c8d4f")

CAMERA = {"hook": "push_in", "childhood": "pan_right", "promise": "push_in", "champion": "dutch",
          "ceasefire": "pan_left", "legacy": "pull_out", "lesson": "tilt_up", "outro": "pan_right"}
TRANSITIONS = {"childhood": "fade", "promise": "iris", "champion": "zoom", "ceasefire": "whip", "legacy": "zoom",
               "lesson": "fade", "outro": "whip"}


def ap(t, a, dur=0.38):
    return pop(t, a - 0.2, dur)


def pele(g, x, sc=0.85, mood="smile", pose="down", turn=0.0, talk=False, pose2=None, k=0.0):
    person(g, x, GROUND, PELE, sc, mood=mood, pose=pose, pose2=pose2, k=k, turn=turn, seed=6, talk=talk)


def kid(g, x, sc=1.0, mood="smile", pose="down", turn=0.0):
    person(g, x, GROUND, KID, sc, mood=mood, pose=pose, turn=turn, seed=9)


def bounce(t, period=0.7, h=160):
    return h * abs(math.sin(math.pi * t / period))


def dirt_road(g):
    c = g.c
    c.new_path()
    for p in [(-500, GROUND - 6), (1600, GROUND - 6), (1600, GROUND + 60), (-500, GROUND + 60)]:
        c.line_to(*p)
    c.close_path()
    c.set_source_rgba(*DIRT[:3], 0.55)
    c.fill()


def tear(g, x, y, t, ph=0.0):
    u = (t * 0.9 + ph) % 1
    g.circle(x, y + 50 * u, 8, hexc("#9fd0f0"), 3)


# ------------------------------------------------------------------ 1. hook
def s_hook(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:   # วันที่ + ลูกบอลเด้ง
        ball(g, CX, GROUND - 60 - bounce(t), 60, t * 200)
        g.label("วันนี้ในอดีต", CX, 380, 104, sc=lerp(2.0, 1, e_out(seg(t, 0.1, 0.4))) if t > 0.1 else 0, rot=-3)
        g.label("23 ตุลาคม 1940", CX, 520, 84, color=BR_GRN, sc=pop(t, 0.8))
        return
    if t < L[5] - 0.2:   # สลัมบราซิล -> เด็กผอม -> ไม่มีรองเท้า -> ไม่มีเงินซื้อลูกบอล
        favela(g, GROUND, t, 0.55)
        if t < L[2] - 0.2:
            g.label("สลัมอันยากจนของบราซิล", CX, 380, 78, sc=ap(t, L[1]), rot=-3)
            return
        kid(g, CX - 120, 1.15, "neutral" if t < L[4] else "worry", "shrug" if t > L[4] - 0.2 else "down", 0.1)
        if t < L[3] - 0.2:
            g.label("เด็กชายตัวผอมกะหร่อง", CX, 380, 80, color=NAVY, sc=ap(t, L[2]), rot=-3)
        elif t < L[4] - 0.2:
            with g.at(820, 1170, ap(t, L[3])):
                g.label("ไม่มีรองเท้า", 0, 0, 52, color=RED)
            g.line([(CX - 210, GROUND - 10), (CX - 30, GROUND - 10)], 8, RED, amp=0)
            g.label("เท้าเปล่า", CX, 380, 96, color=RED, sc=ap(t, L[3]), rot=-3)
        else:
            with g.at(800, 760, ap(t, L[4]), 4 * math.sin(t * 2)):
                ball(g, 0, 0, 90)
                g.line([(-110, -110), (110, 110)], 16, RED, amp=0)
            g.label("ไม่มีเงินซื้อลูกบอล", CX, 380, 84, color=RED, sc=ap(t, L[4]), rot=-3)
        return
    if t < L[6] - 0.2:   # เด็กขัดรองเท้า
        kid(g, 300, 1.1, "smile", "hold", 0.3)
        with g.at(620, GROUND - 60):
            g.rrect(-110, -70, 220, 120, 10, hexc("#8a5a36"), 6)
            g.rrect(-40, -120, 80, 54, 10, hexc("#6e4528"), 5)
        with g.at(830, GROUND - 40 + 8 * math.sin(t * 8)):
            g.c.new_path()
            g.rrect(-90, -50, 180, 60, 26, hexc("#2b2622"), 6)
        g.label("เด็กขัดรองเท้า", CX, 380, 100, color=GOLDTXT, sc=ap(t, L[5]), rot=-3)
        return
    if t < L[7] - 0.2:   # หยุดสงครามกลางเมือง
        for i, lk in enumerate(SOLDIERS):
            person(g, 220 + i * 640, GROUND, lk, 0.7, mood="smile", pose="wave" if i == 0 else "down",
                   turn=0.3 - 0.6 * i, seed=20 + i)
        gun_down(g, 320, GROUND - 20, 0.8, 4)
        gun_down(g, 760, GROUND - 20, 0.8, -4)
        ball(g, CX, GROUND - 60 - bounce(t, 0.8, 200), 60, t * 200)
        g.label("หยุดสงครามกลางเมือง!", CX, 380, 84, color=RED, sc=ap(t, L[6]), rot=-3)
        return
    g.sunburst(CX, 760, 260, 620, 20, t * 8, 10, (0.98, 0.85, 0.4, 0.6))   # ราชาลูกหนัง 3 สมัย
    if t < L[8] - 0.2:
        pele(g, CX, 0.85, "smile", "wave", 0.0)
        g.label('"ราชาลูกหนังโลก"', CX, 380, 96, color=GOLDTXT, sc=ap(t, L[7]), rot=-3)
        return
    for i in range(3):
        trophy(g, 230 + i * 310, GROUND - 40 - 20 * abs(math.sin(t * 3 + i)), 1.1 * ap(t, L[8] + 0.25 * i))
    g.label("แชมป์โลก 3 สมัย!", CX, 380, 100, color=BR_GRN, sc=ap(t, L[8]), rot=-3)
    g.label("คนเดียวในประวัติศาสตร์", CX, 510, 58, color=GREY, sc=ap(t, L[8] + 0.6))


# ------------------------------------------------------------------ 2. childhood
def s_childhood(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # เอดซอน อารันเตส ดู นาสซิเมนโต = เปเล่
        pele(g, 300, 0.88, "smile", "wave" if t > L[1] else "down", 0.3)
        g.name_tag(t, L[1] + 0.1, 790, 1130, "เปเล่", "ราชาลูกหนัง (1940–2022)", side=-1)
        if t < L[1] - 0.2:
            with g.at(750, 640, ap(t, 0.3), -3):
                g.rrect(-280, -120, 560, 240, 20, WHITE, 7)
                g.label("ชื่อจริง", 0, -60, 40, color=GREY)
                g.label("Edson Arantes", 0, 6, 52)
                g.label("do Nascimento", 0, 66, 52)
            g.label("เอดซอน อารันเตส ดู นาสซิเมนโต", CX, 360, 58, sc=ap(t, 0.2), rot=-3)
        else:
            g.label('"เปเล่"!', CX, 360, 130, color=BR_GRN, sc=ap(t, L[1]), rot=-3)
        return
    favela(g, GROUND, t, 0.4)
    dirt_road(g)
    if t < L[3] - 0.2:   # ผูกพันกับความยากจน
        kid(g, CX, 1.1, "neutral", "down")
        g.label("ชีวิตที่ยากจน", CX, 380, 96, color=NAVY, sc=ap(t, L[2]), rot=-3)
        return
    if t < L[4] - 0.2:   # ถุงเท้ายัดเศษผ้า ผูกเชือก
        kid(g, 260, 1.05, "smile", "hold", 0.3)
        k = e_io(seg(t, L[3] + 0.3, L[4] - 0.4))
        with g.at(720, 820):
            if k < 0.5:
                g.rrect(-40, -160, 80, 260, 30, hexc("#c9c1b0"), 6)   # ถุงเท้า
                for i in range(3):
                    g.circle(-140 + 40 * i + 120 * k * 2, -40 + 30 * i, 22, hexc("#d9b26a"), 4)   # เศษผ้า
            else:
                ball(g, 0, 0, 90 * e_out((k - 0.5) * 2) + 1, t * 30, "sock")
        g.label("ถุงเท้า + เศษผ้า = ลูกบอล", CX, 380, 74, color=GOLDTXT, sc=ap(t, L[3]), rot=-3)
        return
    run = (t - L[4]) * 180   # เตะบนถนนดินลูกรัง
    kx = 200 + run % 600
    kid(g, kx, 1.0, "smile", "point", 0.6)
    ball(g, kx + 170, GROUND - 40 - bounce(t, 0.5, 90), 40, t * 400, "sock")
    for i in range(3):
        u = (t * 1.5 + i / 3) % 1
        g.circle(kx - 60 - 120 * u, GROUND - 20 - 20 * u, 20 + 20 * u, (0.8, 0.6, 0.4, 0.5 * (1 - u)), 0)
    g.label("ถนนดินลูกรัง", CX, 380, 96, color=hexc("#a8693a"), sc=ap(t, L[4]), rot=-3)


# ------------------------------------------------------------------ 3. promise
def s_promise(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # ปี 1950 บราซิลแพ้นัดชิงคาบ้าน
        radio(g, 300, GROUND, 1.1, t)
        with g.at(760, 720, ap(t, 0.3)):
            g.rrect(-230, -150, 460, 300, 20, hexc("#2b2826"), 7)
            g.text("1950 รอบชิง", 0, -95, 40, "kanit", GOLD2)
            g.text("บราซิล 1-2 อุรุกวัย", 0, 10, 52, "kanit", WHITE)
            if t > L[1] - 0.2:
                g.text("แพ้คาบ้าน!", 0, 95, 46, "kanit", hexc("#ff7a6a"))
        g.label("ปี 1950", CX, 380, 100, sc=ap(t, 0.2), rot=-3)
        return
    sad = t < L[4] - 0.2
    person(g, 640, GROUND, DAD, 0.82, mood="sad" if sad else "smile", pose="think" if sad else "down", turn=-0.2,
           seed=12)
    if sad:
        for i in range(2):
            tear(g, 640 + (i * 2 - 1) * 26, GROUND - 0.82 * 842 + 20, t, i * 0.5)
    kid(g, 330, 1.0, "worry" if t < L[3] else "smile", "point" if t > L[3] - 0.2 else "down", 0.4)
    if t < L[3] - 0.2:
        g.label("พ่อร้องไห้อย่างหมดหวัง", CX, 380, 80, color=NAVY, sc=ap(t, L[2]), rot=-3)
        g.label("เปเล่ 9 ขวบ", 330, 1150, 48, color=GREY, sc=ap(t, L[2] + 0.5))
        return
    if t < L[4] - 0.2:
        g.label("คำมั่นสัญญา", CX, 380, 100, color=GOLDTXT, sc=ap(t, L[3]), rot=-3)
        return
    with g.at(CX + 30, 620, ap(t, L[4])):
        g.bubble(0, 0, 640, 240, WHITE, tail=(-1, 1))
        if t < L[5] - 0.2:
            g.label("พ่ออย่าร้องไห้เลยนะ...", 0, 0, 54)
        else:
            g.label("ผมจะเอาแชมป์โลก", 0, -36, 54, color=BR_GRN)
            g.label("มาให้พ่อเอง!", 0, 36, 54, color=BR_GRN)
    if t > L[5] - 0.2:
        trophy(g, 900, GROUND - 20, 0.7 * ap(t, L[5] + 0.3))


# ------------------------------------------------------------------ 4. champion
def s_champion(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # ทำได้จริง! แชมป์โลก 1958 วัย 17
        g.sunburst(CX, 760, 260, 640, 22, t * 10, 10, (0.98, 0.85, 0.4, 0.6))
        pele(g, 360, 0.82, "smile", "wave" if t < L[1] else "hold", 0.2)
        trophy(g, 800, GROUND - 40, 1.2 * ap(t, L[1] - 0.2 if t > L[1] - 0.4 else 0.3))
        if t < L[1] - 0.2:
            g.label("ทำได้จริง!", CX, 380, 110, color=BR_GRN, sc=ap(t, 0.2), rot=-3)
        else:
            g.label("แชมป์โลก 1958", CX, 360, 92, color=GOLDTXT, sc=ap(t, L[1]), rot=-3)
            g.label("วัยเพียง 17 ปี!", CX, 480, 60, color=RED, sc=ap(t, L[1] + 0.5))
        return
    if t < L[4] - 0.2:   # ลีลาแซมบ้า / ยิงประตูบ้าคลั่ง
        x = 300 + 120 * math.sin(t * 2.2)
        pele(g, x, 0.8, "smile", "point" if int(t * 2) % 2 else "fist", 0.5 * math.sin(t * 2.2))
        bx = x + 160 + 60 * math.sin(t * 6)
        ball(g, bx, GROUND - 40 - bounce(t, 0.4, 80), 40, t * 500)
        for i in range(4):
            g.line([(bx - 60 - i * 50, GROUND - 60 - i * 20), (bx - 120 - i * 50, GROUND - 60 - i * 20)], 5,
                   (BR_GRN, GOLD2)[i % 2], amp=0)
        if t < L[3] - 0.2:
            g.label("ลีลาแซมบ้า!", CX, 380, 110, color=BR_GRN, sc=ap(t, L[2]), rot=-3)
        else:
            with g.at(860, 900):   # ประตู
                g.line([(-120, 0), (-120, -260), (120, -260), (120, 0)], 10, INK, amp=0)
                for k in range(5):
                    g.line([(-120 + k * 60, -260), (-120 + k * 60, 0)], 2, GREY, amp=0)
                ball(g, 30 * math.sin(t * 4), -120, 36, t * 400)
            g.label("ยิงประตูอย่างบ้าคลั่ง!", CX, 380, 80, color=RED, sc=ap(t, L[3]), rot=-3)
        return
    for i, yr in enumerate(("1958", "1962", "1970")):   # 3 สมัย
        if i > 0 and t < L[4] - 0.2:
            continue
        x = 220 + i * 320
        trophy(g, x, GROUND - 120, 1.0 * ap(t, (L[4] if i else 0) + 0.3 * i) * (1 + 0.03 * math.sin(t * 3 + i)))
        g.label(yr, x, GROUND - 40, 56, color=GOLDTXT, sc=ap(t, (L[4] if i else 0) + 0.3 * i))
    if t < L[5] - 0.2:
        g.label("อีก 2 ครั้ง: 1962 + 1970", CX, 380, 74, color=NAVY, sc=ap(t, L[4]), rot=-3)
    elif t < L[6] - 0.2:
        g.label("ชูถ้วยฟุตบอลโลก 3 สมัย!", CX, 380, 80, color=BR_GRN, sc=ap(t, L[5]), rot=-3)
    else:
        g.sunburst(CX, 560, 60, 180, 12, t * 12, 8, (0.98, 0.85, 0.4, 0.6))
        g.label("ยังไม่มีใครทำลายได้!", CX, 380, 84, color=RED, sc=ap(t, L[6]), rot=-3)


# ------------------------------------------------------------------ 5. ceasefire
def flag_ng(g, x, y, w, h, t):
    with g.at(x, y + 4 * math.sin(t * 5)):
        for i, col in enumerate((hexc("#2f8a4f"), WHITE, hexc("#2f8a4f"))):
            g.rrect(i * w / 3, 0, w / 3, h, 0, col, 4)


def s_ceasefire(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # มหัศจรรย์นอกสนาม -> ไนจีเรีย 1969
        pele(g, 300, 0.85, "smile", "wave", 0.3)
        if t < L[1] - 0.2:
            g.label("มหัศจรรย์นอกสนาม", CX, 380, 90, color=GOLDTXT, sc=ap(t, 0.2), rot=-3)
        else:
            flag_ng(g, 640, 560, 270, 170, t)
            g.line([(640, 560), (640, 1000)], 7, INK, amp=0)
            g.label("ไนจีเรีย 1969", CX, 380, 96, color=GREEN, sc=ap(t, L[1]), rot=-3)
        return
    calm = t > L[3] - 0.2
    for i, lk in enumerate(SOLDIERS):   # สองฝ่ายสงครามกลางเมือง -> หยุดยิง
        x = 200 + i * 680
        person(g, x, GROUND, lk, 0.75, mood="smile" if calm else "angry", pose="wave" if calm and t > L[4] else
               ("hold" if not calm else "down"), turn=0.4 - 0.8 * i, seed=30 + i)
        if calm:
            gun_down(g, x + (1 - 2 * i) * 60, GROUND - 14, 0.8)
    if t < L[3] - 0.2:
        g.label("สงครามกลางเมืองดุเดือด", CX, 380, 80, color=RED, sc=ap(t, L[2]), rot=-3)
        return
    if t < L[4] - 0.2:
        with g.at(CX, 760, ap(t, L[3])):
            g.circle(0, 0, 160, WHITE, 8)
            g.label("48", 0, -10, 120, color=RED)
            g.label("ชั่วโมง", 0, 80, 40, color=GREY)
        g.label('"หยุดยิง!"', CX, 380, 110, color=GREEN, sc=ap(t, L[3]), rot=-3)
        return
    ball(g, CX, GROUND - 60 - bounce(t, 0.7, 260), 60, t * 300)   # วางปืนมาดูเปเล่เตะบอล
    g.label("วางปืนมาดูเปเล่เตะบอล!", CX, 380, 78, color=BR_GRN, sc=ap(t, L[4]), rot=-3)


# ------------------------------------------------------------------ 6. legacy
def s_legacy(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:   # 1,000+ ประตู
        n = int(1000 * e_out(seg(t, 0.3, L[1] - 0.6)))
        for i in range(10):
            u = (t * 0.8 + i / 10) % 1
            ball(g, 120 + i * 95, 1150 - 500 * u, 28, t * 200 + i * 30)
        g.label(f"{n:,}+", CX, 760, 170, color=BR_GRN)
        g.label("ประตูตลอดชีวิตค้าแข้ง", CX, 380, 74, sc=ap(t, 0.2), rot=-3)
        return
    if t < L[2] - 0.2:   # ฟุตบอล = ศิลปะ
        pele(g, 300, 0.8, "smile", "wave", 0.3)
        for i, col in enumerate((RED, BR_GRN, BR_BLU, GOLD2)):
            g.arc(760, 1200, 200 + i * 40, 180, 180 + 180 * seg(t, L[1], L[1] + 1.2), 14, col)
        ball(g, 800 + 30 * math.sin(t * 2), 700, 50, t * 200)
        g.label("ฟุตบอล = ศิลปะชั้นยอด", CX, 380, 80, color=NAVY, sc=ap(t, L[1]), rot=-3)
        return
    favela(g, GROUND, t, 0.4)
    for i in range(3):   # เด็กยากจนทั่วโลกเล่นบอล
        x = 200 + i * 320 + 30 * math.sin(t * 2 + i)
        person(g, x, GROUND, KID, 0.95, mood="smile", pose="wave" if i == 1 else "down", turn=0.3, seed=40 + i)
    ball(g, 380 + 200 * math.sin(t * 1.5), GROUND - 50 - bounce(t, 0.6, 140), 40, t * 300, "sock")
    if t < L[3] - 0.2:
        g.label("ความหวังของเด็กยากจน", CX, 380, 80, color=GOLDTXT, sc=ap(t, L[2]), rot=-3)
    else:
        g.label("ความจนกักขังความฝันไม่ได้", CX, 380, 74, color=BR_GRN, sc=ap(t, L[3]), rot=-3)


# ------------------------------------------------------------------ 7. lesson
def s_lesson(g, t, L, d):
    g.ground(GROUND, WHITE)
    g.label("บทเรียน", CX, 340, 100, sc=ap(t, 0.2), rot=-3)
    if t < L[1] - 0.2:
        kid(g, 300, 1.0, "smile", "down", 0.3)
        g.label("→", CX, 900, 120, color=GREY, sc=ap(t, 0.6))
        pele(g, 780, 0.8, "smile", "wave", -0.2)
        return
    k = e_io(seg(t, L[1], L[1] + 2.5))   # จากติดลบ -> สูงสุด
    pts = [(0, 0.05), (0.25, 0.12), (0.5, 0.35), (0.75, 0.65), (1, 0.95)]
    n = max(2, int(len(pts) * k + 0.99))
    path = [(160 + u * 760, 1150 - v * 560) for u, v in pts[:n]]
    g.line(path, 14, BR_GRN, amp=0)
    g.label("จุดเริ่มต้นติดลบ", 260, 1210, 44, color=RED, sc=ap(t, L[1]))
    if k > 0.95:
        trophy(g, path[-1][0] - 40, path[-1][1] - 10, 0.6 * ap(t, L[1] + 2.6))
    g.label("ไม่อาจขวางคนมุ่งมั่น", CX, 480, 64, color=GREEN, sc=ap(t, L[1] + 0.4))


# ------------------------------------------------------------------ 8. outro
def s_outro(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:
        pele(g, CX, 0.85, "smile", "wave", 0.0, talk=True)
        g.label("แล้วทุกคนล่ะครับ", CX, 360, 90, sc=ap(t, 0.2), rot=-3)
        return
    if t < L[3] - 0.2:   # 4 ตำนาน
        legends = [("เปเล่", BR_YEL, BR_GRN, "10", None), ("มาราโดนา", WHITE, hexc("#2b2622"), "10", hexc("#8fc7e8")),
                   ("เมสซี", WHITE, hexc("#2b2622"), "10", hexc("#8fc7e8")),
                   ("โรนัลโด", hexc("#c8323a"), hexc("#2f9a4f"), "7", None)]
        for i, (nm, body, trim, num, st) in enumerate(legends):
            x, y = 290 + (i % 2) * 500, 640 + (i // 2) * 360
            k = ap(t, L[1] + 0.35 * i)
            if k < 0.02:
                continue
            jersey(g, x, y + 8 * math.sin(t * 2 + i), 0.85 * k, body, trim, num, st, 4 * math.sin(t * 1.5 + i))
            g.label(nm, x, y + 170, 50, sc=k)
        if t < L[2] - 0.2:
            g.label("ใครคือที่สุด?", CX, 360, 96, sc=ap(t, L[1]), rot=-3)
        else:
            g.label("ราชาลูกหนังตลอดกาล?", CX, 360, 84, color=GOLDTXT, sc=ap(t, L[2]), rot=-3)
        return
    with g.at(CX + 170, 640, ap(t, L[3])):   # ชวนคอมเมนต์
        g.bubble(0, 0, 460, 220, WHITE, tail=(-1, 1))
        for i in range(3):
            g.circle(-110 + i * 110, 0, 24 + 6 * math.sin(t * 6 - i), INK, 0)
    pele(g, 250, 0.8, "smile", "wave", 0.3, talk=True)
    g.label("คอมเมนต์แลกเปลี่ยนกันได้เลย!", CX, 360, 70, color=RED, sc=ap(t, L[3]), rot=-3)


SCENES = {
    "hook": s_hook, "childhood": s_childhood, "promise": s_promise, "champion": s_champion,
    "ceasefire": s_ceasefire, "legacy": s_legacy, "lesson": s_lesson, "outro": s_outro,
}
NO_IRIS = set()
