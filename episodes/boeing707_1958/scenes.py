"""ฉากตอน: โบอิ้ง 707 ของแพนแอม บินข้ามแอตแลนติกเที่ยวแรก (26 ต.ค. 1958) — ไม่ใช้โลโก้จริง"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from chars import (HOSTESS, PA_BLUE, PAX, PILOT, RICH, SKY, atlantic, bizcase, cabin, camera, clock,  # noqa: E402
                   cloud, crown, globe, house, jet, jet_top, liner, noise_lines, propliner, runway, sea, storm,
                   suitcase, ticket, tower)
from gfx import GOLD, GOLD2, GREY, INK, NAVY, RED, W, WHITE, e_io, e_out, hexc, lerp, pop, seg  # noqa: E402
from people import person  # noqa: E402

CX = W / 2
GROUND = 1270
GOLDTXT = hexc("#b37a12")
GREEN = hexc("#3c8d4f")

CAMERA = {"hook": "push_in", "launch": "pan_right", "before": "dutch", "jet": "push_in", "legacy": "pan_left",
          "lesson": "pull_out", "outro": "pan_right"}
TRANSITIONS = {"launch": "zoom", "before": "whip", "jet": "iris", "legacy": "zoom", "lesson": "fade",
               "outro": "whip"}


def ap(t, a, dur=0.38):
    return pop(t, a - 0.2, dur)


def title(g, t, a, txt, col=INK, size=84, y=380):
    g.label(txt, CX, y, size, color=col, sc=ap(t, a), rot=-3)


def sky_clouds(g, t, y0=560, n=3, speed=60):
    for i in range(n):
        x = 1100 - ((t * speed + i * 420) % 1400)
        cloud(g, x, y0 + (i % 2) * 260 + 30 * math.sin(i * 2.3), 0.7 + 0.15 * (i % 2))


def orbit_jet(g, cx, cy, rx, ry, a, sc, t):
    """เครื่องบินบินวนรอบโลก หันหัวตามทิศทาง"""
    dx, dy = -rx * math.sin(a), ry * math.cos(a)
    ang = math.degrees(math.atan2(dy, dx))
    flip = dx < 0
    jet(g, cx + rx * math.cos(a), cy + ry * math.sin(a), sc, ang - 180 if flip else ang, t, flip=flip)


def chip(g, x, y, txt, col, k, rot=0.0, w=300):
    if k < 0.02:
        return
    with g.at(x, y, k, rot):
        g.rrect(-w / 2, -64, w, 128, 40, WHITE, 7, stroke=col)
        g.label(txt, 0, 0, 50, color=col)


def cross(g, x, y, r, k):
    if k <= 0:
        return
    g.line([(x - r, y - r), (x - r + 2 * r * min(1, 2 * k), y - r + 2 * r * min(1, 2 * k))], 16, RED, amp=0)
    if k > 0.5:
        u = (k - 0.5) * 2
        g.line([(x + r, y - r), (x + r - 2 * r * u, y - r + 2 * r * u)], 16, RED, amp=0)


# ------------------------------------------------------------------ 1. hook
def s_hook(g, t, L, d):
    if t < L[1] - 0.2:   # วันนี้ในอดีต
        sky_clouds(g, t, 700)
        jet(g, lerp(380, CX, e_out(seg(t, 0.0, L[1]))), 940, 0.8 * pop(t, 0.0, 0.4) + 0.01, -4, t, trail=0.6)
        g.label("วันนี้ในอดีต", CX, 380, 104, sc=lerp(2.0, 1, e_out(seg(t, 0.1, 0.4))) if t > 0.1 else 0, rot=-3)
        g.label("26 ตุลาคม 1958", CX, 520, 84, color=GOLDTXT, sc=pop(t, 0.5))
        return
    if t < L[2] - 0.2:   # นกเหล็กยักษ์คำรามเหนือแอตแลนติก
        sea(g, 1150, t)
        sky_clouds(g, t, 640, 2, 120)
        jx = lerp(400, 600, e_io(seg(t, L[1], L[2])))
        jet(g, jx, 860, 0.85, -3, t, trail=0.8)
        noise_lines(g, jx + 340, 860, t, ap(t, L[1] + 0.3))
        title(g, t, L[1], "นกเหล็กยักษ์ เหนือแอตแลนติก!", PA_BLUE, 80)
        return
    if t < L[3] - 0.2:   # ครึ่งค่อนวัน → ไม่กี่ชั่วโมง
        u = e_io(seg(t, L[2] + 0.6, L[3] - 0.6))
        hrs = lerp(15, 8.5, u)
        clock(g, CX, 860, 230, hrs, t, RED if u < 0.5 else GREEN)
        g.label(f"{hrs:.1f} ชม.".replace(".0 ", " "), CX, 1200, 80, color=RED if u < 0.5 else GREEN,
                sc=ap(t, L[2] + 0.2))
        title(g, t, L[2], "ครึ่งค่อนวัน → ไม่กี่ชั่วโมง", INK, 80)
        return
    if t < L[4] - 0.2:   # ยุคเครื่องบินเจ็ท
        sky_clouds(g, t, 800, 2, 90)
        k = e_out(seg(t, L[3] - 0.2, L[4]))
        jet(g, lerp(400, 620, k), lerp(1100, 720, k), 0.75, -14, t, trail=0.9)
        for i in range(5):
            g.sparkle(CX + 330 * math.cos(i * 1.3 + t), 760 + 260 * math.sin(i * 1.3 + t), 26)
        title(g, t, L[3], "\"ยุคเครื่องบินเจ็ท\"", RED, 104)
        return
    r = lerp(330, 170, e_io(seg(t, L[4], L[4] + 1.8)))   # ย่อโลกให้เล็กลง
    globe(g, CX, 860, r, t)
    orbit_jet(g, CX, 860, r + 110, (r + 110) * 0.45, t * 2.2, 0.22, t)
    title(g, t, L[4], "ย่อโลกให้เล็กลงในพริบตา!", GOLDTXT, 82)


# ------------------------------------------------------------------ 2. launch
def moon_night(g, t):
    g.circle(800, 560, 70, hexc("#f6e7a8"), 6)
    g.circle(830, 540, 60, WHITE, 0)
    for i in range(6):
        g.star(180 + i * 120, 540 + 60 * math.sin(i * 2.1), 14 + 4 * math.sin(t * 3 + i), GOLD2, 3)


def s_launch(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:   # ค่ำคืน 26 ต.ค. 1958
        moon_night(g, t)
        with g.at(CX, 880, ap(t, L[0]), -3 + 2 * math.sin(t * 1.5)):
            g.rrect(-230, -190, 460, 380, 30, WHITE, 8)
            g.rrect(-230, -190, 460, 100, 30, RED, 8)
            g.text("ต.ค. 1958", 0, -140, 52, "kanit", WHITE)
            g.text("26", 0, 40, 180, "kanit", INK)
        title(g, t, L[0], "ค่ำคืน 26 ตุลาคม 1958", NAVY, 84)
        return
    if t < L[3] - 0.2:   # แพนแอม สร้างประวัติศาสตร์
        runway(g, GROUND - 90, t)
        tower(g, 820, GROUND - 90, 0.8, t)
        jet(g, 470, GROUND - 230, 0.8, 0, t)
        if t < L[2] - 0.2:
            g.label("Pan American World Airways", CX, 560, 50, color=GREY, sc=ap(t, L[1] + 0.4))
            title(g, t, L[1], "สายการบินแพนแอม", PA_BLUE, 92)
        else:
            for i in range(4):
                g.sparkle(250 + i * 180, 640 + 40 * math.sin(t * 3 + i), 30)
            title(g, t, L[2], "ประวัติศาสตร์หน้าใหม่!", GOLDTXT, 90)
            g.label("การบินพาณิชย์", CX, 510, 60, color=INK, sc=ap(t, L[2] + 0.4))
        return
    if t < L[4] - 0.2:   # โบอิ้ง 707
        jet(g, CX, 900, 0.95 * ap(t, L[3]) + 0.01, 3 * math.sin(t * 1.5), t)
        with g.at(CX, 620, ap(t, L[3] + 0.5), -4):
            g.rrect(-220, -60, 440, 120, 30, PA_BLUE, 7)
            g.text("BOEING 707", 0, 0, 64, "kanit", WHITE)
        title(g, t, L[3], "เครื่องบินโดยสารไอพ่น", INK, 82)
        return
    if t < L[5] - 0.2:   # ทะยานจากไอดิลไวลด์
        k = e_io(seg(t, L[4], L[5] + 0.2))
        runway(g, GROUND - 90, t, speed=900 * (1 - k))
        tower(g, 820 - 500 * k, GROUND - 90, 0.8, t)
        jet(g, lerp(420, 620, k), lerp(GROUND - 230, 760, k * k), 0.75, -16 * min(1, 2 * k), t, trail=k)
        title(g, t, L[4], "ทะยานจากสนามบินไอดิลไวลด์", PA_BLUE, 74)
        g.label("นิวยอร์ก", CX, 500, 60, color=GOLDTXT, sc=ap(t, L[4] + 0.4))
        return
    if t < L[6] - 0.2:   # มุ่งหน้าปารีส
        atlantic(g, CX, 860, 820, 520, e_io(seg(t, L[5] - 0.2, L[6] + 0.4)), t)
        title(g, t, L[5], "มุ่งหน้าสู่ปารีส ฝรั่งเศส", RED, 84)
        return
    # 111 ชีวิต
    crew = [PILOT, PAX[0], PAX[1], HOSTESS, PAX[2]]
    for i, lk in enumerate(crew):
        k = ap(t, L[6] + 0.15 * i)
        if k > 0.02:
            person(g, 170 + i * 175, GROUND, lk, 0.55 * k, mood="smile", pose="wave" if i in (0, 3) else "down",
                   turn=0.3 - 0.15 * i, seed=10 + i)
    n = int(lerp(1, 111, e_out(seg(t, L[6], L[6] + 1.6))))
    g.label(f"{n} ชีวิต", CX, 380, 110, color=RED, sc=ap(t, L[6]), rot=-3)
    g.label("ผู้โดยสาร + ลูกเรือ", CX, 510, 56, color=GREY, sc=ap(t, L[6] + 0.4))


# ------------------------------------------------------------------ 3. before
def s_before(g, t, L, d):
    if t < L[2] - 0.2:   # ก่อนหน้านี้ เครื่องบินใบพัด
        sea(g, 1150, t)
        sky_clouds(g, t, 650, 2, 40)
        propliner(g, lerp(380, 600, seg(t, 0, L[2])), 880, 0.8 * ap(t, L[0]) + 0.01, 0, t, 0.6)
        if t < L[1] - 0.2:
            title(g, t, L[0], "ก่อนหน้านี้...", GREY, 100)
        else:
            title(g, t, L[1], "เครื่องบินใบพัด", INK, 92)
            g.label("ข้ามแอตแลนติก", CX, 510, 60, color=PA_BLUE, sc=ap(t, L[1] + 0.3))
        return
    if t < L[3] - 0.2:   # เสียงดังกึกก้อง
        propliner(g, 480, 880, 0.9, -2, t, 1.0)
        noise_lines(g, 830, 870, t, 1.0, 4)
        with g.at(800, 600, ap(t, L[2] + 0.3), 8 * math.sin(t * 9)):
            g.label("ครืนนน!", 0, 0, 90, color=RED)
        title(g, t, L[2], "เสียงเครื่องยนต์ดังกึกก้อง", RED, 80)
        return
    if t < L[4] - 0.2:   # สั่นตลอดทาง
        cabin(g, CX, 960, 1.0, t, calm=False)
        title(g, t, L[3], "สั่นสะเทือนตลอดทาง", NAVY, 86)
        return
    u = e_io(seg(t, L[4], L[4] + 1.6))   # 14-15 ชั่วโมง
    clock(g, CX, 840, 230, lerp(0, 15, u), t, RED)
    g.label("14–15 ชั่วโมง", CX, 1190, 86, color=RED, sc=ap(t, L[4] + 0.3))
    title(g, t, L[4], "ใช้เวลานานแสนนาน", INK, 84)


# ------------------------------------------------------------------ 4. jet
def s_jet(g, t, L, d):
    if t < L[1] - 0.2:   # ทว่า โบอิ้ง 707
        sky_clouds(g, t, 700, 2, 80)
        jet(g, lerp(380, CX, e_out(seg(t, L[0] - 0.2, L[0] + 0.8))), 860, 0.85, 2 * math.sin(t * 1.5), t, trail=0.7)
        title(g, t, L[0], "ทว่า... โบอิ้ง 707", PA_BLUE, 96)
        return
    if t < L[2] - 0.2:   # เครื่องยนต์ไอพ่น 4 ตัว
        jet_top(g, CX, 900, 0.95, 0, seg(t, L[1], L[2] - 0.4), t)
        title(g, t, L[1], "เครื่องยนต์ไอพ่น 4 ตัว", INK, 86)
        return
    if t < L[3] - 0.2:   # สูงกว่าชั้นเมฆ
        g.circle(780, 560, 70, GOLD2, 6)
        for i in range(3):
            storm(g, 240 + i * 280, 1130, 0.9, t + i)
        jet(g, CX, 760 + 12 * math.sin(t * 1.4), 0.8, -2, t, trail=0.6)
        g.line([(140, 960), (940, 960)], 5, GREY, amp=0)
        title(g, t, L[2], "บินสูงเหนือชั้นเมฆ", PA_BLUE, 88)
        return
    if t < L[4] - 0.2:   # ราบรื่น นุ่มนวล เงียบสงบ
        cabin(g, CX, 1000, 0.9, t, calm=True)
        for i, (txt, col) in enumerate((("ราบรื่น", PA_BLUE), ("นุ่มนวล", GREEN), ("เงียบสงบ", GOLDTXT))):
            chip(g, 260 + i * 280, 560, txt, col, ap(t, L[3] + 0.6 * i, 0.3), -4 + 4 * i, 250)
        title(g, t, L[3], "การเดินทางที่แสนสบาย", INK, 80)
        return
    if t < L[5] - 0.2:   # และที่สำคัญที่สุด...
        with g.at(CX, 860, ap(t, L[4]) * (1 + 0.05 * math.sin(t * 6))):
            g.circle(0, 0, 200, GOLD2, 8)
            g.label("!", 0, 0, 260, color=RED)
        title(g, t, L[4], "และที่สำคัญที่สุด...", INK, 88)
        return
    atlantic(g, CX, 800, 820, 460, e_io(seg(t, L[5], L[5] + 2.2)), t, labels=False)   # 8 ชั่วโมงครึ่ง
    clock(g, CX, 1180, 110, lerp(0, 8.5, e_io(seg(t, L[5], L[5] + 2.2))), t, GREEN)
    g.label("8 ชม.ครึ่ง!", 250, 1180, 64, color=GREEN, sc=ap(t, L[5] + 1.6), rot=-6)
    g.label("ไม่ใช่ 15", 830, 1180, 54, color=RED, sc=ap(t, L[5] + 2.0), rot=6)
    title(g, t, L[5], "ถึงยุโรปในเวลาเพียงราว", INK, 78)


# ------------------------------------------------------------------ 5. legacy
def s_legacy(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:   # ก้าวกระโดดทางวิศวกรรม
        with g.at(CX, 860, ap(t, L[0]), -2 + 2 * math.sin(t * 1.3)):
            g.rrect(-390, -270, 780, 540, 24, hexc("#2b4f8a"), 8)
            for i in range(9):
                g.line([(-390 + i * 97, -270), (-390 + i * 97, 270)], 2, (1, 1, 1, 0.25), amp=0)
            jet_top(g, 0, 0, 0.5, 90, 0, t)
            g.text("707", 260, 200, 60, "kanit", WHITE)
        title(g, t, L[0], "ก้าวกระโดดทางวิศวกรรม", PA_BLUE, 80)
        return
    if t < L[2] - 0.2:   # ปฏิวัติวิถีชีวิต
        for i in range(4):
            person(g, 240 + i * 200, GROUND, PAX[i], 0.55, mood="smile", pose="v" if i % 2 == 0 else "wave",
                   turn=0.2 - 0.15 * i, seed=20 + i)
        for i in range(6):
            u = (t * 0.5 + i / 6) % 1
            g.star(180 + i * 140, 800 - 200 * u, 20, (*GOLD2[:3], 1 - u), 4)
        title(g, t, L[1], "ปฏิวัติวิถีชีวิตมนุษย์!", RED, 86)
        return
    if t < L[3] - 0.2:   # ไม่จำกัดแค่มหาเศรษฐี
        person(g, 260, GROUND, RICH, 0.75, mood="smug", pose="cross", turn=0.3, seed=30)
        k = ap(t, L[2] + 1.2)
        for i in range(3):
            if k > 0.02:
                person(g, 520 + i * 170, GROUND, PAX[i + 1], 0.55 * k, mood="smile", pose="wave" if i == 1 else "down",
                       turn=-0.3, seed=31 + i)
        title(g, t, L[2], "ไม่ใช่แค่มหาเศรษฐีอีกต่อไป", GOLDTXT, 76)
        return
    if t < L[4] - 0.2:   # ล่องเรือเป็นสัปดาห์
        sea(g, 1080, t)
        liner(g, 480, 1060, 0.85, t)
        with g.at(800, 620, ap(t, L[3] + 0.3), 6):
            g.rrect(-120, -90, 240, 180, 20, WHITE, 7)
            g.label("7 วัน", 0, 0, 64, color=NAVY)
        cross(g, 800, 620, 110, seg(t, L[3] + 1.0, L[3] + 1.6))
        title(g, t, L[3], "ไม่ต้องล่องเรือเป็นสัปดาห์", NAVY, 78)
        return
    if t < L[5] - 0.2:   # ธุรกิจ ท่องเที่ยว ระหว่างประเทศ
        bizcase(g, 250, 860, 0.8 * ap(t, L[4]) + 0.01, -6 + 3 * math.sin(t * 2))
        camera(g, CX, 860, 0.8 * ap(t, L[4] + 1.0) + 0.01, 4 * math.sin(t * 2), t)
        globe(g, 830, 860, 100 * ap(t, L[4] + 2.0) + 1, t)
        for i, (txt, col) in enumerate((("ธุรกิจ", hexc("#7a4a2a")), ("ท่องเที่ยว", RED), ("ต่างประเทศ", PA_BLUE))):
            g.label(txt, 250 + i * 290, 1070, 46, color=col, sc=ap(t, L[4] + i))
        title(g, t, L[4], "โลกถูกเชื่อมถึงกัน", INK, 86)
        return
    if t < L[6] - 0.2:   # เชื่อมถึงกันรวดเร็ว
        globe(g, CX, 860, 300, t)
        pts = [(330, 760), (720, 700), (460, 1000), (760, 960), (560, 640)]
        for i in range(len(pts)):
            a, b = pts[i], pts[(i + 2) % len(pts)]
            k = seg(t, L[5] - 0.2 + 0.15 * i, L[5] + 0.5 + 0.15 * i)
            if k > 0:
                g.line([a, (lerp(a[0], b[0], k), lerp(a[1], b[1], k))], 7, RED, amp=0)
            g.circle(*a, 14, GOLD, 4)
        title(g, t, L[5], "เชื่อมถึงกันอย่างรวดเร็ว", RED, 84)
        return
    if t < L[7] - 0.2:   # Jet Set
        suitcase(g, CX, 1020, 1.0 * ap(t, L[6]) + 0.01, 3 * math.sin(t * 2))
        with g.at(CX, 620, ap(t, L[6] + 0.2) * (1 + 0.04 * math.sin(t * 5)), -6):
            g.rrect(-300, -100, 600, 200, 100, RED, 9)
            g.text("JET SET", 0, 0, 110, "kanit", WHITE)
        return
    if t < L[8] - 0.2:   # บินไปไหนมาไหนรอบโลก
        globe(g, 640, 820, 210, t)
        orbit_jet(g, 640, 820, 290, 140, t * 1.8, 0.2, t)
        person(g, 230, GROUND, PAX[3], 0.7, mood="smile", pose="wave", turn=0.4, seed=40)
        suitcase(g, 390, GROUND, 0.4, 0, ("PARIS", "ROME", "TOKYO", "NY"))
        title(g, t, L[7], "บินไปไหนมาไหนได้รอบโลก", PA_BLUE, 78)
        return
    jet(g, CX, 920, 0.8, -3 + 2 * math.sin(t * 1.4), t, trail=0.5)   # ราชาแห่งอุตสาหกรรมการบิน
    crown(g, CX + 30, 700 - 10 * math.sin(t * 2), 0.9 * ap(t, L[8] + 0.6) + 0.01, 8)
    for i in range(5):
        g.sparkle(CX + 340 * math.cos(i * 1.25 + t), 820 + 200 * math.sin(i * 1.25 + t), 26)
    title(g, t, L[8], "โบอิ้ง ราชาแห่งการบินโลก", GOLDTXT, 80)


# ------------------------------------------------------------------ 6. lesson
def s_lesson(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:
        sky_clouds(g, t, 760, 2, 70)
        jet(g, lerp(380, 620, seg(t, 0, L[1])), 880, 0.7, -6, t, trail=0.8)
        title(g, t, L[0], "เรื่องราวนี้พิสูจน์ว่า...", INK, 84)
        return
    if t < L[2] - 0.2:   # ความเร็วก้าวล้ำ
        for i in range(7):
            u = (t * 2.5 + i / 7) % 1
            y = 640 + i * 70
            g.line([(920 - 600 * u, y), (920 - 600 * u - 140, y)], 8, (*PA_BLUE[:3], 1 - u), amp=0)
        jet(g, CX + 60, 880, 0.75, -3, t, trail=1.0)
        title(g, t, L[1], "ความเร็วที่ก้าวล้ำเพียงก้าวเดียว", PA_BLUE, 72)
        return
    k = e_io(seg(t, L[3] - 0.2, L[3] + 1.2))   # พรมแดนห่าง → เพื่อนบ้าน
    lx, rx = lerp(220, 380, k), lerp(860, 700, k)
    house(g, lx, GROUND, 0.7, roof=RED)
    house(g, rx, GROUND, 0.7, roof=PA_BLUE)
    if k < 0.5:
        for i in range(12):
            g.line([(CX, 760 + i * 42), (CX, 780 + i * 42)], 6, (*GREY[:3], 1 - 2 * k), amp=0)
        if k < 0.02:
            sea(g, GROUND - 6, t, 380, 700, 20)
    jet(g, CX, 620 + 10 * math.sin(t * 2), 0.32, 0, t)
    if t < L[3] - 0.2:
        title(g, t, L[2], "พรมแดนที่ห่างไกล", GREY, 88)
    else:
        for sx in (-1, 1):
            person(g, CX + sx * 85, GROUND, PAX[0] if sx < 0 else PAX[1], 0.5, mood="smile",
                   pose="wave", turn=-0.5 * sx, seed=50 + sx)
        g.sparkle(CX, 860, 30)
        title(g, t, L[3], "เพื่อนบ้านใกล้แค่เอื้อม", GREEN, 88)


# ------------------------------------------------------------------ 7. outro
def s_outro(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:   # วิวัฒนาการการบินพาณิชย์
        propliner(g, 330, 600, 0.38 * ap(t, L[0]) + 0.01, 0, t, 0.3)
        g.label("→", CX + 40, 620, 90, color=GREY, sc=ap(t, L[0] + 0.6))
        jet(g, 760, 620, 0.38 * ap(t, L[0] + 1.2) + 0.01, 0, t)
        person(g, CX, GROUND, PAX[2], 0.55, mood="smile", pose="think", turn=0.1, seed=60, talk=True)
        title(g, t, L[0], "วิวัฒนาการการบินพาณิชย์", PA_BLUE, 80)
        return
    if t < L[2] - 0.2:   # ย้อนเวลา
        clock(g, CX, 860, 220, 12 - (t - L[1]) * 6, t, PA_BLUE)
        g.label("1958", CX, 1180, 90, color=GOLDTXT, sc=ap(t, L[1] + 0.4))
        title(g, t, L[1], "ถ้าย้อนเวลากลับไปได้...", INK, 84)
        return
    if t < L[3] - 0.2:   # นั่งเจ็ทสุดหรู
        cabin(g, 600, 1060, 0.8, t, calm=True)
        person(g, 200, GROUND, HOSTESS, 0.72, mood="smile", pose="hold", turn=0.5, seed=70)
        title(g, t, L[2], "นั่งเครื่องบินเจ็ทสุดหรู", GOLDTXT, 84)
        return
    if t < L[4] - 0.2:   # ยุคบุกเบิก 1958
        ticket(g, CX, 840, 1.3 * ap(t, L[3]) + 0.01, -5 + 2 * math.sin(t * 2))
        title(g, t, L[3], "ยุคบุกเบิกปี 1958", RED, 90)
        return
    with g.at(CX + 170, 640, ap(t, L[4])):   # ชวนคอมเมนต์
        g.bubble(0, 0, 460, 220, WHITE, tail=(-1, 1))
        for i in range(3):
            g.circle(-110 + i * 110, 0, 24 + 6 * math.sin(t * 6 - i), INK, 0)
    person(g, 250, GROUND, PAX[1], 0.75, mood="smile", pose="wave", turn=0.3, seed=80, talk=True)
    jet(g, 700, 1000, 0.3, -6, t)
    title(g, t, L[4], "มาแลกเปลี่ยนกันในคอมเมนต์!", RED, 70)


SCENES = {
    "hook": s_hook, "launch": s_launch, "before": s_before, "jet": s_jet, "legacy": s_legacy,
    "lesson": s_lesson, "outro": s_outro,
}
NO_IRIS = set()
