"""ฉากตอน room404: เสียงเคาะจากห้อง 404 — การ์ตูนสยองโทนมืด แนวนอน 1920x1080"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from chars import (BG, BLACKHAIR, CONC, CONC2, DAO, EK, FLOOR, GHOST, GHOST_SKIN, GOLDC, GOWN, LANDLORD, NEON,  # noqa: E402
                   NIGHT, RUST, SRI, TALIS, TEAK, TEAL, TEAL2, TEAL3, TILE, TILE2, WOOD, WOOD2, YEL, YEL2, apron,
                   beam, bound_dao, building, balcony_xy, corridor, darken, door, fill_rect, flashlight, flick,
                   ghost_back, ghost_face, glow, gold_chain, lerp_col, lightning, neon_tube, rain, shadow_crawler,
                   sledgehammer, smoke, stains, tiles, vignette, wardrobe, window_rain, yantra_cloth)
from gfx import INK, WHITE, H, W, e_io, e_out, hexc, hn, lerp, pop, seg  # noqa: E402
from people import _rr, _shade, _stroke, head, person  # noqa: E402

CX, CY = W / 2, H / 2
GROUND = 1000
DARKTXT = (0.02, 0.04, 0.05, 1)
SUB_COLOR = hexc("#f3f0e2")
SUB_STROKE = (6, DARKTXT)
SUB_PHRASES = True   # ซับสั้นทีละวลี (สไตล์คลิปเล่าเรื่องผีแนวตั้ง)
SUB_SIZE = 64
AMBIENCE = {"rain": 0.07, "drone": 0.14}   # ฝนพรำ + โทนต่ำ ๆ ใต้เสียงพากย์

CAMERA = {"open": "push_in", "lock": "push_in", "knock": "push_in", "back": "pan_left", "owner": "pan_right",
          "balcony": "tilt_up", "logbook": "push_in", "empty": "pull_out", "cry": "pan_right", "peephole": "push_in",
          "sri": "still", "yantra": "push_in", "doubt": "dutch", "key": "pan_left", "closet": "push_in",
          "dao": "push_in", "slam": "dutch", "truth": "pull_out", "shadow": "tilt_down", "reveal": "push_in",
          "dark": "still", "escape": "pan_right", "merit": "pan_left", "final": "push_in"}
TRANSITIONS = {n: "fade" for n in CAMERA}
TRANSITIONS.update({"back": "zoom", "closet": "zoom", "escape": "whip"})
NO_IRIS = {("peephole", "sri"), ("dark", "escape")}   # ตัดฉับ


def ap(t, a, dur=0.38):
    """เด้งขึ้นก่อนจุดเริ่มบรรทัด 0.2 วิ"""
    return pop(t, a - 0.2, dur)


def fade_in(t, a, dur=0.6):
    return e_io(seg(t, a - 0.2, a - 0.2 + dur))


def beat(t, L):
    """บรรทัดปัจจุบัน (ภาพเปลี่ยนก่อนเสียง 0.2 วิ)"""
    i = 0
    for k, x in enumerate(L):
        if t >= x - 0.2:
            i = k
    return i


CAPS = False   # สไตล์คลิปเล่าเรื่องผี: แทบไม่มีตัวหนังสือบนภาพ (เหลือเฉพาะ keep=True)
KEEP = {"02:17 น.", "2 คืนก่อน", "ย้อนกลับไป...", "คืนที่สอง", "คืนที่สาม", "คืนที่สาม · ห้อง 404", "ปัง!",
        "เสียงเคาะจากห้อง 404", "The Knock from Room 404", "1 เดือนต่อมา", "“ขอบคุณนะ...”", "บางเสียงเคาะ...",
        "ไม่ได้ต้องการให้คุณกลัว", "ก๊อก", "เช้า", "3 ปีก่อน", "1", "2"}


def cap(g, s, x, y, size=80, col=YEL2, sc=1.0, rot=0, a=1.0):
    """ตัวหนังสือบนภาพ (โทนมืด): ตัวเหลืองซีด ขอบเข้ม"""
    if not CAPS and s not in KEEP:
        return
    g.text(s, x, y, size, "kanit", col, sc, rot, a, stroke=max(8, int(size * 0.12)), stroke_color=DARKTXT)


def knock_txt(g, t, t0, x, y, n=3, gap=0.85, size=96, rot=-4):
    """ข้อความ ก๊อก เด้งขึ้นทีละครั้ง"""
    hits = 0
    for i in range(n):
        tt = t0 + i * gap
        if t >= tt:
            hits += 1
            k = pop(t, tt, 0.25)
            cap(g, "ก๊อก", x + i * 210, y + (i % 2) * 40, size, YEL2, k, rot + i * 4)
    return hits


def knock_shake(t, t0, n=3, gap=0.85):
    v = 0.0
    for i in range(n):
        d = t - (t0 + i * gap)
        if 0 <= d < 0.25:
            v = max(v, (1 - d / 0.25))
    return v


def flash(g, a, col=(0.75, 0.92, 0.98)):
    if a > 0:
        fill_rect(g.c, -1500, -1500, W + 3000, H + 3000, (col[0], col[1], col[2], 0.55 * a))


def floor(g, y=GROUND, col=FLOOR):
    fill_rect(g.c, -1500, y, W + 3000, 2000, col)
    g.c.set_source_rgba(*INK)
    g.c.set_line_width(5)
    g.c.move_to(-1500, y)
    g.c.line_to(W + 1500, y)
    g.c.stroke()


def room_bg(g, t, light=1.0, patch=0.0, window=True, lt_times=()):
    """ภายในห้อง 404: ผนังคราบเชื้อรา, ผ้ายันต์, หน้าต่างตอกไม้, ชั้นวางกระถางธูป"""
    c = g.c
    wall = lerp_col(hexc("#121c1b"), hexc("#3c5650"), light)
    fill_rect(c, -1500, -1500, W + 3000, 3000, wall)
    stains(g, -200, 80, 2300, 600, 14, 8, 0.35)
    if patch > 0:   # ผนังฉาบปูนใหม่ด้านเดียว (ซ้าย) + คราบรูปคน
        with g.alpha(patch):
            fill_rect(c, 140, 60, 620, GROUND - 60, lerp_col(hexc("#2a302f"), hexc("#7b8582"), light))
            for i in range(7):
                _stroke(c, [(200 + i * 80, 120 + 40 * hn(i, 2)), (230 + i * 80, 260), (210 + i * 80, 380 + 30 * hn(i, 5))], 2.5, INK, 0.35)
            g.blob(450, 470, 95, 250, (0.12, 0.14, 0.12, 0.45), 0, 4)
            g.blob(450, 250, 58, 66, (0.12, 0.14, 0.12, 0.45), 0, 5)
            for k in range(4):
                yantra_cloth(g, 220 + k * 160, 150, 0.4, hn(k, 3) * 10, seed=k)
    if window:
        lt = lightning(t, lt_times)
        x, y, w, h = 1430, 170, 300, 330
        window_rain(g, x, y, w, h, t, 0.5)
        if lt > 0:
            fill_rect(c, x, y, w, h, (0.8, 0.95, 1.0, 0.8 * lt))
        for k, (a0, a1) in enumerate(((0.1, 0.9), (0.9, 0.2), (0.0, 0.55))):   # ไม้ตอกปิด
            with g.at(x + w / 2, y + h * (0.25 + 0.25 * k), 1, (k - 1) * 14):
                _rr(c, -w / 2 - 30, -16, w + 60, 32, 4)
                _shade(c, WOOD, 4, 0.25)
                g.circle(-w / 2 - 10, 0, 5, (0.2, 0.2, 0.2, 1), 0)
                g.circle(w / 2 + 10, 0, 5, (0.2, 0.2, 0.2, 1), 0)
    floor(g, GROUND, lerp_col(hexc("#0d1312"), FLOOR, light))


def shelf_incense(g, x, y, t, smoke_on=True):
    c = g.c
    _rr(c, x - 110, y, 220, 20, 4)
    _shade(c, WOOD, 4, 0.2)
    _rr(c, x - 40, y - 60, 80, 60, 12)
    _shade(c, hexc("#8a7a5c"), 4, 0.2)
    for k in range(3):
        _stroke(c, [(x - 20 + k * 20, y - 60), (x - 26 + k * 24, y - 150)], 4, hexc("#8a3a2a"), 1.0)
        if smoke_on:
            glow(g, x - 26 + k * 24, y - 150, 10, (1, 0.6, 0.3, 1), 0.9)
    if smoke_on:
        smoke(g, x, y - 160, t, 4, 0.18, 3, 60)


def bed_covered(g, x, y):
    c = g.c
    _rr(c, x - 260, y - 190, 520, 190, 30)
    _shade(c, hexc("#9aa29d"), 5, 0.3)
    for k in range(4):
        _stroke(c, [(x - 220 + k * 120, y - 180), (x - 200 + k * 120, y - 20)], 3, INK, 0.2)


def ladder(g, x, y, h=420):
    c = g.c
    for sx in (-1, 1):
        _stroke(c, [(x + sx * 70, y), (x + sx * 40, y - h)], 12, hexc("#a9b2b5"), 1.0)
        _stroke(c, [(x + sx * 70, y), (x + sx * 40, y - h)], 3, INK, 1.0)
    for k in range(1, 5):
        yy = y - k * h / 5
        ww = lerp(70, 40, k / 5)
        _stroke(c, [(x - ww, yy), (x + ww, yy)], 8, hexc("#a9b2b5"), 1.0)


def key_prop(g, x, y, sc=1.0, rot=0, label="404"):
    c = g.c
    with g.at(x, y, sc, rot):
        g.circle(-70, 0, 34, hexc("#c8a64a"), 5)
        g.circle(-70, 0, 13, (0.05, 0.05, 0.05, 1), 0)
        _rr(c, -40, -10, 150, 20, 6)
        _shade(c, hexc("#c8a64a"), 5, 0.25)
        g.poly([(80, 8), (80, 34), (96, 34), (96, 24), (108, 24), (108, 8)], hexc("#c8a64a"), 4, amp=0)
        if label:
            with g.at(-70, 70, 1, 8):
                _rr(c, -44, -24, 88, 48, 8)
                _shade(c, hexc("#e9e1c8"), 3, 0.1)
                g.text(label, 0, 0, 30, "kanit", INK)


def big_hand(g, x, y, sc=1.0, rot=0, skin=EK.skin, sleeve=EK.suit):
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -330, -60, 260, 120, 30)
        _shade(c, sleeve, 5, 0.3)
        g.blob(-40, 0, 90, 70, skin, 5, 3)
        for k in range(4):
            _rr(c, 10, -56 + k * 30, 90 - k * 8, 28, 13)
            _shade(c, skin, 4, 0.2)


# ================================================================ 1 ตีสองสิบเจ็ดนาที
def s_open(g, t, L, d):
    b = corridor(g, t, light=0.75)
    rain(g, t, 0.35, 60, 4, (-600, -100, 700, 1300))   # ฝนที่ช่องลมซ้าย
    i = beat(t, L)
    if i < 3:
        with g.at(960, 800, 0.36):   # เอกตัวเล็ก ๆ ที่ปลายทางเดิน
            person(g, -150, 0, EK, 1.0, mood="worry", pose="hold", turn=0.85, seed=1)
            flashlight(g, -60, -560, -10, True, 260, 0.35)
        cap(g, "02:17 น.", 300, 170, 110, YEL2, ap(t, L[0]), -3)
        cap(g, "ชั้น 4", 300, 300, 64, TEAL3, ap(t, L[1]), -3)
    else:   # เอกยืนตัวสั่นหน้าประตู
        darken(g, 0.35)
        door(g, 1220, 1080, 420, 900, lock=True)
        shake = 3 * math.sin(t * 40)
        person(g, 640 + shake, 1450, EK, 1.0, mood="worry", pose="hold", turn=0.9, seed=1, look_at=(1, 0))
        flashlight(g, 860, 820, -18, True, 600, 0.4)
    vignette(g, 0.85)


# ================================================================ 2 กุญแจสำรอง
def s_lock(g, t, L, d):
    i = beat(t, L)
    if i < 2:
        corridor(g, t, light=0.6, end_door=False)
        darken(g, 0.3)
        person(g, 900, 1500, EK, 1.0, mood="worry", pose="hold", turn=0.2, seed=1, talk=False)
        flashlight(g, 1030, 900, 10, True, 700, 0.35)
        g.name_tag(t, L[0], 1360, 400, "เอก", "ช่างซ่อมบำรุงกะดึก วัย 30")
    elif i == 2:   # กุญแจในมือ
        fill_rect(g.c, -1500, -1500, W + 3000, 3000, NIGHT)
        glow(g, 960, 540, 700, YEL, 0.12)
        k = ap(t, L[2])
        big_hand(g, 780, 600, 1.6 * k, -8)
        key_prop(g, 1000, 560, 1.6 * k, -12 + 4 * math.sin(t * 9), "404")
        cap(g, "กุญแจสำรอง", 960, 180, 84, YEL2, ap(t, L[2] + 0.4), -2)
    else:   # ประตู 404 + แม่กุญแจสนิม (ปิดตาย 3 ปี)
        fill_rect(g.c, -1500, -1500, W + 3000, 3000, CONC)
        lk = seg(t, d - 1.6, d - 1.2)
        with g.at(960, 1700, 2.2):
            door(g, 0, 0, 300, 560, lock=True, lock_k=lk)
        if i >= 4:
            for k in range(5):   # หยากไย่
                _stroke(g.c, [(1500, 0), (1500 + 60 * k, 140 + 30 * k), (1920, 120 + 70 * k)], 2, (0.8, 0.85, 0.82, 1), 0.35)
            cap(g, "ปิดตาย 3 ปี", 470, 230, 96, YEL2, ap(t, L[4]), -4)
        flashlight(g, 1600, 1000, -150, True, 900, 0.3)
    vignette(g, 0.85)


# ================================================================ 3 กลิ่นธูป + เสียงเคาะ
def s_knock(g, t, L, d):
    i = beat(t, L)
    if i < 3:   # ประตูแง้ม ควันธูปลอยออกมา
        corridor(g, t, light=0.55, end_door=False)
        darken(g, 0.3)
        ok = e_io(seg(t, 0.0, 2.0))
        door(g, 1280, 1080, 420, 900, lock=False, open_k=ok)
        red = 0.0 if i < 1 else 1.0
        for k in range(5):
            u = ((t * 0.25 + k / 5) % 1.0)
            g.blob(1240 - 420 * u, 640 - 80 * u + 40 * math.sin(t + k), 60 + 120 * u, 40 + 60 * u,
                   lerp_col((0.8, 0.85, 0.8, 0.22), (0.6, 0.25, 0.25, 0.25), red * u), 0, k)
        person(g, 560, 1450, EK, 1.0, mood="shock" if i >= 2 else "worry", pose="think" if i >= 1 else "hold",
               turn=0.9, seed=1)
        if i == 2:
            cap(g, "คาว...", 1000, 220, 110, hexc("#d98a7a"), ap(t, L[2]), -4)
        if i == 0:
            cap(g, "กลิ่นธูป", 1000, 220, 90, YEL2, ap(t, L[0] + 1.5), -3)
    else:   # ภายในห้อง: ตู้เสื้อผ้าสั่นตามเสียงเคาะ
        room_bg(g, t, 0.55)
        bed_covered(g, 520, GROUND)
        shelf_incense(g, 860, 520, t)
        sh = knock_shake(t, L[4] + 0.3) if i >= 4 else 0.0
        wardrobe(g, 1200 + 8 * sh * math.sin(t * 70), GROUND, 440, 780, 0.0, 0, True, t=t)
        beam(g, 0, 700, -12, 1400, 10, 0.3)
        if i >= 4:
            knock_txt(g, t, L[4] + 0.3, 900, 200)
        if i >= 5:
            cap(g, "ในตู้เสื้อผ้า", 1200, 120, 80, YEL2, ap(t, L[5] + 1.6), -2)
        # ไตเติลเรื่อง
        tt = L[5] + 4.6
        if t > tt:
            a = e_io(seg(t, tt, tt + 0.5))
            darken(g, 0.93 * a)
            cap(g, "เสียงเคาะจากห้อง 404", CX, CY - 30, 120, hexc("#e9e4d0"), pop(t, tt + 0.1, 0.5), 0, a)
            cap(g, "The Knock from Room 404", CX, CY + 90, 50, TEAL3, 1.0, 0, a * seg(t, tt + 0.4, tt + 0.8))
    vignette(g, 0.9)


# ================================================================ 4 ย้อนกลับไปสองคืนก่อน
def s_back(g, t, L, d):
    c = g.c
    fill_rect(c, -1500, -1500, W + 3000, 3000, hexc("#1d3436"))   # ฟ้าสลัวหัวค่ำ
    glow(g, 300, 900, 900, hexc("#8a7a4a"), 0.25)
    building(g, t, 1000, 980, 5, 5)
    fill_rect(c, -1500, 980, W + 3000, 600, hexc("#1a2223"))
    for k in range(6):   # สายไฟระโยงระยาง
        c.set_source_rgba(0.02, 0.02, 0.02, 0.9)
        c.set_line_width(3)
        c.move_to(-200, 120 + k * 22)
        c.curve_to(600, 260 + k * 30, 1300, 200 + k * 10, 2200, 90 + k * 26)
        c.stroke()
    rain(g, t, 0.25, 70)
    i = beat(t, L)
    if i >= 2:
        x = lerp(1900, 1350, e_out(seg(t, L[2] - 0.2, L[2] + 3)))
        person(g, x, 1060, EK, 0.42, mood="neutral", pose="down", turn=-0.6, seed=1)
    if i == 1:   # นาฬิกาหมุนย้อน
        k = ap(t, L[1])
        with g.at(CX, CY - 40, k):
            g.circle(0, 0, 210, hexc("#e9e4d0"), 8)
            for h in range(12):
                a = h * math.pi / 6
                _stroke(c, [(math.cos(a) * 175, math.sin(a) * 175), (math.cos(a) * 195, math.sin(a) * 195)], 6, INK, 1.0)
            ang = -t * 5
            _stroke(c, [(0, 0), (math.cos(ang) * 150, math.sin(ang) * 150)], 10, INK, 1.0)
            _stroke(c, [(0, 0), (math.cos(ang / 12) * 100, math.sin(ang / 12) * 100)], 14, INK, 1.0)
        cap(g, "2 คืนก่อน", CX, 870, 110, YEL2, ap(t, L[1] + 0.5), -3)
    if i == 0:
        cap(g, "ย้อนกลับไป...", CX, 160, 96, YEL2, ap(t, L[0] + 1.0), -3)
    vignette(g, 0.75)


# ================================================================ 5 เจ้าของตึก
def office_bg(g, t, light=1.0, hook_hi=0.0):
    c = g.c
    fill_rect(c, -1500, -1500, W + 3000, 3000, lerp_col(hexc("#141d1c"), hexc("#4b5a4c"), light))
    stains(g, -100, 60, 2100, 500, 10, 3, 0.3)
    # บอร์ดกุญแจ
    _rr(c, 1260, 150, 440, 330, 10)
    _shade(c, WOOD, 5, 0.25)
    for r in range(3):
        for k in range(5):
            x, y = 1310 + k * 82, 200 + r * 100
            g.circle(x, y, 7, (0.6, 0.55, 0.4, 1), 2)
            lab = f"{r + 2}0{k + 1}" if not (r == 2 and k == 3) else "404"
            if lab != "404":
                key_prop(g, x + 4, y + 40, 0.3, 90, None)
            g.text(lab, x, y + 78, 18, "kanit", hexc("#e9e1c8"))
    if hook_hi > 0:
        x, y = 1310 + 3 * 82, 400
        c.set_source_rgba(0.85, 0.25, 0.2, hook_hi)
        c.set_line_width(7)
        c.arc(x, y + 30, 58, 0, 2 * math.pi)
        c.stroke()
    # ศาลพระ
    _rr(c, 160, 230, 220, 24, 4)
    _shade(c, WOOD2, 4, 0.2)
    g.blob(270, 180, 34, 46, GOLDC, 4, 2)
    g.circle(270, 125, 18, GOLDC, 4)
    for sx in (-1, 1):
        g.blob(270 + sx * 80, 205, 22, 22, hexc("#e2932b"), 3, 3 + sx)
    # พัดลมเพดาน
    with g.at(960, 40):
        for k in range(3):
            a = t * 7 + k * 2.09
            g.blob(math.cos(a) * 110, math.sin(a) * 16, 110, 14, hexc("#3a3a36"), 3, k)
        g.circle(0, 0, 18, hexc("#4a4a44"), 3)


def desk(g, x, y, w=1000, h=260):
    c = g.c
    _rr(c, x - w / 2, y - h, w, 40, 6)
    _shade(c, WOOD, 5, 0.25)
    _rr(c, x - w / 2 + 20, y - h + 40, w - 40, h - 40, 4)
    _shade(c, WOOD2, 5, 0.3, horiz=False)
    for k in range(3):   # ของบนโต๊ะ
        _rr(c, x - 380 + k * 70, y - h - 30 - k * 8, 60, 30 + k * 8, 3)
        _shade(c, (0.8, 0.78, 0.7, 1), 3, 0.1)
    _rr(c, x + 260, y - h - 80, 120, 80, 6)   # ทีวีเล็ก
    _shade(c, hexc("#222222"), 4, 0.1)
    fill_rect(c, x + 270, y - h - 70, 100, 56, lerp_col(TEAL, NEON, 0.5 + 0.5 * math.sin(c.get_matrix()[4] * 0.0)))


def s_owner(g, t, L, d):
    i = beat(t, L)
    if i < 4:
        office_bg(g, t, 0.85, hook_hi=ap(t, L[3] + 1.0) if i == 3 else 0.0)
        floor(g, 1000, hexc("#2c2a24"))
        if i == 1:   # หน้าใกล้: รอยยิ้มที่ไม่ถึงดวงตา
            with g.at(860, 560, 4.2 * (0.95 + 0.05 * seg(t, L[1], d))):
                head(g, LANDLORD, "smug", 0.0, 0.1, (0.3, 0), 2)
            cap(g, "ยิ้ม...", 1450, 260, 90, YEL2, ap(t, L[1] + 1.0), -4)
            cap(g, "แต่ตาไม่ยิ้ม", 1450, 380, 70, hexc("#d98a7a"), ap(t, L[1] + 2.0), -4)
        else:
            person(g, 820, 1200, LANDLORD, 0.95, mood="smug" if i != 3 else "firm",
                   pose="point" if i >= 2 else "down", turn=0.35, seed=2, talk=i >= 2)
            gold_chain(g, 820, 1200 - 0.95 * 0.0 - 640, 50)
            desk(g, 820, 1100)
            person(g, 1520, 1300, EK, 0.8, mood="worry" if i >= 3 else "neutral", pose="hold", turn=-0.6, seed=1)
            g.name_tag(t, L[0], 420, 360, "เสี่ยวิโรจน์", "เจ้าของตึก วัย 60")
            if i == 3:
                cap(g, "ห้าม!", 520, 250, 120, hexc("#e0705e"), ap(t, L[3] + 0.3), -6)
    else:   # พื้นหน้าห้องแห้งสนิท
        corridor(g, t, light=0.7, end_door=True)
        darken(g, 0.2)
        person(g, 520, 1250, EK, 0.75, mood="think" if False else "worry", pose="think", turn=0.6, seed=1)
        glow(g, 960, 840, 220, YEL2, 0.18)
        cap(g, "ท่อแตก 3 ปี?", 1450, 230, 84, YEL2, ap(t, L[4]), -3)
        if i >= 5:
            cap(g, "แต่พื้นแห้งสนิท", 1450, 360, 72, hexc("#d98a7a"), ap(t, L[5]), -3)
            for k in range(3):
                g.sparkle(900 + k * 60, 860 + 20 * hn(k, 2), 16 * ap(t, L[5] + 0.3 * k), YEL2, 3)
    vignette(g, 0.85)


# ================================================================ 6 ผู้หญิงที่ระเบียง
def s_balcony(g, t, L, d):
    c = g.c
    i = beat(t, L)
    if i < 2:   # ลานจอดรถหลังตึก
        fill_rect(c, -1500, -1500, W + 3000, 3000, NIGHT)
        building(g, t, 960, 900, 5, 5, lit={(4, 2): 0.9}, sign=False)
        fill_rect(c, -1500, 900, W + 3000, 600, hexc("#141b1b"))
        for k in range(3):   # รถจอด
            _rr(c, 200 + k * 560, 820, 380, 120, 40)
            _shade(c, hexc("#2b3337"), 5, 0.3)
        rain(g, t, 0.45, 110)
        person(g, 960, 1060, EK, 0.32, mood="worry", pose="hold", turn=0.0, seed=1)
        flashlight(g, 1000, 900, -80 if i >= 1 else -20, True, 500, 0.35, 0.5)
        if i >= 1:
            x0, fw, fh, base = 960 - (5 * 230 + 80) / 2, 230, 170, 900
            bx, by = balcony_xy(x0, fw, fh, base, 3, 2)
            ghost_back(g, bx, by + 50, 0.13, t, 1.0, ap(t, L[1] + 1.2))
    elif i < 4:   # ระเบียงชั้นสี่ใกล้ขึ้น
        fill_rect(c, -1500, -1500, W + 3000, 3000, hexc("#2f3c3b"))
        stains(g, -200, 0, 2300, 400, 12, 6, 0.4)
        fill_rect(c, 560, 120, 800, 680, lerp_col(YEL, YEL2, 0.2))
        glow(g, 960, 460, 700, YEL, 0.35)
        ghost_back(g, 960, 840, 0.82, t, 1.0, fade_in(t, L[2], 1.0))
        c.set_source_rgba(*hexc("#5b4033"))
        c.set_line_width(12)
        for j in range(15):
            xx = 400 + j * 80
            c.move_to(xx, 640)
            c.line_to(xx, 860)
        c.move_to(380, 640)
        c.line_to(1540, 640)
        c.stroke()
        fill_rect(c, -1500, 860, W + 3000, 70, CONC2)
        rain(g, t, 0.45, 120)
    elif i == 4:   # แปรงผมช้า ๆ (ใกล้)
        fill_rect(c, -1500, -1500, W + 3000, 3000, lerp_col(YEL, NIGHT, 0.55))
        glow(g, 960, 300, 900, YEL2, 0.25)
        ghost_back(g, 900, 1900, 1.9, t * 0.8, 1.0)
        rain(g, t, 0.3, 80)
    else:   # ป้าย 404 ที่ระเบียง + เอกตกใจ
        fill_rect(c, -1500, -1500, W + 3000, 3000, NIGHT)
        glow(g, 1300, 400, 600, YEL, 0.3)
        with g.at(1320, 420, 1.4 * ap(t, L[5])):
            _rr(c, -130, -60, 260, 120, 10)
            _shade(c, hexc("#c9b98a"), 6, 0.2)
            g.text("404", 0, 0, 80, "kanit", INK)
        with g.at(600, 600, 3.4):
            head(g, EK, "shock", 0.0, 0.5, (0.8, -0.8), 1)
        rain(g, t, 0.4, 90)
    vignette(g, 0.85)


# ================================================================ 7 สมุดป้อมยาม
def s_logbook(g, t, L, d):
    c = g.c
    i = beat(t, L)
    fill_rect(c, -1500, -1500, W + 3000, 3000, hexc("#231d15"))
    glow(g, 960, 520, 900, YEL, 0.35 * flick(t, 3))
    if i == 0:   # ป้อมยาม
        fill_rect(c, -1500, -1500, W + 3000, 3000, NIGHT)
        _rr(c, 560, 260, 800, 760, 20)
        _shade(c, hexc("#c9c0a0"), 6, 0.25)
        fill_rect(c, 640, 340, 640, 330, lerp_col(YEL, YEL2, 0.3))
        glow(g, 960, 500, 500, YEL, 0.3)
        g.text("ป้อมยาม", 960, 300, 44, "kanit", INK)
        x = lerp(1900, 1100, e_out(seg(t, 0, 2.5)))
        person(g, x, 1150, EK, 0.6, mood="worry", pose="down", turn=-0.5, seed=1)
        rain(g, t, 0.45, 110)
        vignette(g, 0.85)
        return
    # สมุดเปิดบนโต๊ะ (มองจากบน)
    _rr(c, 300, 90, 1320, 900, 14)
    _shade(c, hexc("#e9dfbf"), 6, 0.15)
    _stroke(c, [(960, 100), (960, 980)], 5, INK, 0.5)
    rows = ["401", "402", "403", "404", "405", "406", "407"]
    names = ["นายสมชาย ใจดี", "นางสาวพิมพ์ รุ่งเรือง", "นายณัฐ ทองดี", "", "นางมาลี ศรีสุข", "นายวิทย์ แสงทอง", "นายต้น สายลม"]
    for r, (rm, nm) in enumerate(zip(rows, names)):
        y = 200 + r * 110
        _stroke(c, [(990, y + 45), (1580, y + 45)], 2, hexc("#7a90b0"), 0.8)
        g.text(rm, 1040, y, 44, "kanit", INK)
        if nm:
            g.text(nm, 1300, y, 40, "kanitm", hexc("#2b3f7a"))
    g.text("ทะเบียนผู้เช่า ชั้น 4", 640, 200, 52, "kanit", INK)
    g.text("ตรวจล่าสุด: 3 ปีก่อน", 640, 300, 36, "kanitm", hexc("#7a5a3a"))
    # นิ้วไล่ลง
    row = 0 if i < 2 else min(3, int(seg(t, L[2], L[3] - 0.3) * 3)) if i == 2 else 3
    fy = 200 + row * 110
    with g.at(1000, fy + 60, 1.0, -30):
        big_hand(g, 0, 0, 0.9, 0)
    if i >= 3:
        k = ap(t, L[3])
        c.set_source_rgba(0.82, 0.22, 0.18, 0.9)
        c.set_line_width(8)
        c.save()
        c.translate(1300, 530)
        c.scale(max(k, 0.01) * 1.0, max(k, 0.01) * 0.36)
        c.arc(0, 0, 300, 0, 2 * math.pi)
        c.restore()
        c.stroke()
        cap(g, "ว่างเปล่า", 640, 610, 80, hexc("#e0705e"), ap(t, L[3] + 0.6), -3)
    if i >= 4:
        with g.at(620, 520, ap(t, L[4]), -10):
            c.set_source_rgba(0.75, 0.2, 0.18, 0.85)
            c.set_line_width(6)
            c.rectangle(-170, -60, 340, 120)
            c.stroke()
            g.text("ปิดตั้งแต่ 3 ปีก่อน", 0, 0, 38, "kanit", hexc("#b23a2a"))
    vignette(g, 0.8)


# ================================================================ 8 ระเบียงว่างเปล่า
def curtain(g, x, y, w, h, t, sway=1.0, torn=True):
    c = g.c
    pts = []
    for k in range(9):
        u = k / 8
        pts.append((x + u * w + 18 * sway * math.sin(t * 1.6 + u * 4), y + h - (40 * hn(k, 2) if torn else 0)))
    path = [(x, y), (x + w, y)] + pts[::-1]
    g.poly(path, (0.88, 0.9, 0.86, 0.85), 4, amp=0, smooth=False)
    for k in range(5):
        xx = x + (k + 0.5) * w / 5
        _stroke(c, [(xx, y), (xx + 14 * sway * math.sin(t * 1.6 + k), y + h - 30)], 2.5, INK, 0.3)


def s_empty(g, t, L, d):
    c = g.c
    i = beat(t, L)
    if i == 0:   # วิ่งกลับไปดู
        fill_rect(c, -1500, -1500, W + 3000, 3000, NIGHT)
        building(g, t, 960, 900, 5, 5, lit={(4, 2): 0.35}, sign=False)
        fill_rect(c, -1500, 900, W + 3000, 600, hexc("#141b1b"))
        x = lerp(-200, 900, e_io(seg(t, 0, 2.4)))
        person(g, x, 1250, EK, 0.6, mood="shock", pose="fist", turn=0.6, seed=1, lean=8)
        rain(g, t, 0.5, 120)
    elif i < 3:
        fill_rect(c, -1500, -1500, W + 3000, 3000, hexc("#2f3c3b"))
        stains(g, -200, 0, 2300, 400, 12, 6, 0.4)
        fill_rect(c, 560, 120, 800, 680, hexc("#0f1717"))
        sc = 1.0 if i == 1 else 1.0
        curtain(g, 600, 140, 720, 600, t, 1.0)
        c.set_source_rgba(*hexc("#5b4033"))
        c.set_line_width(12)
        for j in range(15):
            xx = 400 + j * 80
            c.move_to(xx, 640)
            c.line_to(xx, 860)
        c.move_to(380, 640)
        c.line_to(1540, 640)
        c.stroke()
        _stroke(c, [(1100, 640), (1150, 700), (1130, 780)], 2, (0.02, 0.02, 0.02, 1), 1.0)   # เส้นผมติดราว
        fill_rect(c, -1500, 860, W + 3000, 70, CONC2)
        cap(g, "ว่างเปล่า", 1660, 420, 84, YEL2, ap(t, L[1] + 0.3), -4)
        rain(g, t, 0.45, 120)
    else:   # ประตูกระจกตอกตะปูปิดตาย
        fill_rect(c, -1500, -1500, W + 3000, 3000, hexc("#2f3c3b"))
        fill_rect(c, 520, 80, 880, 900, hexc("#152323"))
        curtain(g, 560, 100, 800, 820, t, 0.7)
        for k in range(4):
            fill_rect(c, 520 + k * 220, 80, 6, 900, (0.6, 0.75, 0.75, 0.35))
        for k, (y, r) in enumerate(((300, -12), (520, 10), (740, -6))):
            with g.at(960, y, ap(t, L[3] + 0.3 * k), r):
                _rr(c, -520, -34, 1040, 68, 6)
                _shade(c, WOOD, 5, 0.3)
                for sx in (-1, 1):
                    g.circle(sx * 470, 0, 9, (0.15, 0.15, 0.15, 1), 0)
        cap(g, "ตอกปิด", 1680, 380, 84, hexc("#e0705e"), ap(t, L[3] + 1.2), -4)
        cap(g, "จากด้านนอก", 1680, 490, 60, hexc("#e0705e"), ap(t, L[3] + 1.5), -4)
        rain(g, t, 0.3, 70)
    vignette(g, 0.85)


# ================================================================ 9 คืนที่สอง: เสียงร้องไห้
def s_cry(g, t, L, d):
    c = g.c
    i = beat(t, L)
    if i == 0:
        fill_rect(c, -1500, -1500, W + 3000, 3000, hexc("#101a1c"))
        with g.at(960, 520, 3.0):
            head(g, EK, "worry", 0.0, 0.2, (0, 0.6), 1)
        cap(g, "คืนที่สอง", 1500, 200, 100, YEL2, ap(t, L[0]), -3)
        cap(g, "แค่ตาฝาด...", 1500, 330, 70, TEAL3, ap(t, L[0] + 2.0), -3)
        vignette(g, 0.85)
        return
    b = corridor(g, t, light=0.6, vx=1250)
    darken(g, 0.15)
    ladder(g, 600, 1050, 460)
    turn = -0.2 if i < 2 else lerp(-0.2, 0.9, e_io(seg(t, L[2], L[2] + 0.8)))
    person(g, 600, 1050 - 290, EK, 0.6, mood="worry" if i >= 2 else "neutral", pose="v" if i < 2 else "hold",
           turn=turn, seed=1, legs=True)
    if i >= 2:   # คลื่นเสียงสะอื้นจากประตู
        for k in range(3):
            r = 60 + ((t * 80 + k * 70) % 210)
            c.set_source_rgba(*YEL2[:3], 0.45 * (1 - (r - 60) / 210))
            c.set_line_width(5)
            c.arc(1250, 650, r, math.pi * 0.7, math.pi * 1.3)
            c.stroke()
        cap(g, "ฮือ...", 1450, 330, 80, YEL2, ap(t, L[2] + 1.0), -6)
        cap(g, "ฮึก...", 1600, 450, 60, YEL2, ap(t, L[2] + 2.2), 5)
    vignette(g, 0.85)


# ================================================================ 10 ตาแมว
def s_peephole(g, t, L, d):
    c = g.c
    i = beat(t, L)
    if i == 0:   # ย่องเข้าไป
        corridor(g, t, light=0.5)
        darken(g, 0.3)
        x = lerp(300, 650, e_io(seg(t, 0, L[1])))
        person(g, x, 1300, EK, 0.75, mood="worry", pose="hold", turn=0.8, seed=1, lean=10)
    elif i == 1:   # ก้มลงแนบตา
        fill_rect(c, -1500, -1500, W + 3000, 3000, NIGHT)
        door(g, 1400, 1700, 900, 1600, lock=False, talisman=True)
        with g.at(lerp(820, 1000, e_io(seg(t, L[1], L[1] + 2.5))), 560, 3.2, 8):
            head(g, EK, "worry", 0.0, 0.95, (1, 0), 1)
        glow(g, 1400, 1700 - 1600 + 190 * 1, 60, YEL2, 0.3)
    else:   # มองผ่านตาแมว (เลนส์ตาปลา)
        fill_rect(c, -1500, -1500, W + 3000, 3000, (0, 0, 0, 1))
        R = 470
        c.save()
        c.arc(CX, CY, R, 0, 2 * math.pi)
        c.clip()
        fill_rect(c, 0, 0, W, H, hexc("#05090a"))
        if i >= 3:   # ความมืดขยับ
            g.blob(CX + 80 * math.sin(t * 1.5), CY, 260, 300, (0.08, 0.1, 0.1, 1), 0, 3)
        if i >= 4:
            k = e_out(seg(t, L[4] - 0.25, L[4] + 0.15))
            grin = 0.2 + 0.8 * e_io(seg(t, L[6] - 0.2, L[6] + 2.5))
            ghost_face(g, CX, CY + 20, 0.6 + 1.0 * k, t, grin, 1.0, k)
        rg_r = R
        import cairo
        rg = cairo.RadialGradient(CX, CY, rg_r * 0.4, CX, CY, rg_r)
        rg.add_color_stop_rgba(0, 0, 0, 0, 0)
        rg.add_color_stop_rgba(1, 0, 0, 0, 0.9)
        c.set_source(rg)
        c.paint()
        c.restore()
        c.set_source_rgba(*hexc("#2a2a26"))
        c.set_line_width(26)
        c.arc(CX, CY, R, 0, 2 * math.pi)
        c.stroke()
        if i == 2:
            cap(g, "มืดสนิท...", CX, 960, 70, TEAL3, ap(t, L[2] + 0.4), -2)
        if t > d - 0.5:   # ตัดดำ
            darken(g, seg(t, d - 0.5, d - 0.2))
        return
    vignette(g, 0.85)


# ================================================================ 11 ป้าศรี (เช้า)
def stair_bg(g, t):
    c = g.c
    fill_rect(c, -1500, -1500, W + 3000, 3000, hexc("#5a6663"))
    for r in range(4):   # ผนังบล็อกช่องลม
        for k in range(5):
            x, y = 1300 + k * 100, 120 + r * 100
            _rr(c, x, y, 90, 90, 6)
            _shade(c, hexc("#9aa5a0"), 4, 0.2)
            g.circle(x + 45, y + 45, 28, hexc("#c9d2cc"), 3)
    for k in range(7):   # ขั้นบันได
        y = 760 + k * 50
        fill_rect(c, -1500, y, 1300 + k * 40 + 1500, 50, hexc("#7b8582") if k % 2 else hexc("#6d7774"))
        _stroke(c, [(-1500, y), (k * 40 - 200 + 1500, y)], 3, INK, 0.5)
    fill_rect(c, -1500, 1000, W + 3000, 600, hexc("#5f6966"))


def broom(g, x, y, rot, sc=1.0):
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -8, -420, 16, 380, 6)
        _shade(c, hexc("#8a6a44"), 3.5, 0.2)
        for k in range(14):
            _stroke(c, [(0, -60), (-60 + k * 9, 60)], 3, hexc("#b39a5b"), 1.0)


def s_sri(g, t, L, d):
    stair_bg(g, t)
    i = beat(t, L)
    if i < 2:
        person(g, 760, 1080, EK, 0.78, mood="sad", pose="down", turn=0.3, seed=1)
        for k in range(2):   # ขอบตาคล้ำ
            pass
        cap(g, "ไม่ได้นอนทั้งคืน", 1400, 620, 70, hexc("#f1ead2"), ap(t, L[0] + 0.5), -3)
        if i == 1:
            cap(g, "เช้า", 280, 160, 90, hexc("#f1ead2"), ap(t, L[1]), -3)
    else:
        person(g, 520, 1080, EK, 0.78, mood="worry", pose="hold", turn=0.6, seed=1, talk=True)
        fall = e_io(seg(t, L[3] + 1.6, L[3] + 2.3)) if i >= 3 else 0.0
        person(g, 1180, 1080, SRI, 0.86, mood="shock" if i >= 3 else "neutral",
               pose="hold" if fall < 0.5 else "stop", turn=-0.5, seed=4)
        apron(g, 1180, 1080, 0.86)
        broom(g, 1100 + 120 * fall, 900 + 120 * fall, lerp(-10, 75, fall), 0.9)
        g.name_tag(t, L[2], 1450, 330, "ป้าศรี", "แม่บ้านเก่าแก่ เกือบ 20 ปี", side=-1)
        if i >= 3:
            cap(g, "404?!", 1200, 140, 100, hexc("#e0705e"), ap(t, L[3] + 1.6), -5)
    vignette(g, 0.6)


# ================================================================ 12 ผ้ายันต์แดง
def bulb_light(g, t, x, y0, length=260):
    sw = 10 * math.sin(t * 1.3)
    ang = math.radians(sw)
    bx, by = x + math.sin(ang) * length, y0 + math.cos(ang) * length
    _stroke(g.c, [(x, y0), (bx, by)], 3, INK, 1.0)
    glow(g, bx, by, 700, YEL, 0.35)
    g.circle(bx, by + 18, 22, YEL2, 4)
    return bx, by


def store_bg(g, t):
    c = g.c
    fill_rect(c, -1500, -1500, W + 3000, 3000, hexc("#1c2220"))
    for r in range(3):   # ชั้นวางของ
        y = 260 + r * 250
        fill_rect(c, 1250, y, 600, 18, WOOD)
        for k in range(5):
            _rr(c, 1270 + k * 112, y - 120 + 20 * (k % 2), 80, 120 - 20 * (k % 2), 10)
            _shade(c, (hexc("#8fb0c0"), hexc("#d1c38a"), hexc("#b58a8a"))[(k + r) % 3], 3.5, 0.25)
    fill_rect(c, -1500, 1000, W + 3000, 600, hexc("#232826"))


def s_yantra(g, t, L, d):
    c = g.c
    i = beat(t, L)
    store_bg(g, t)
    bulb_light(g, t, 960, -20)
    if i < 2:
        person(g, 620, 1150, EK, 0.82, mood="worry", pose="hold", turn=0.5, seed=1)
        person(g, 1180, 1150, SRI, 0.9, mood="worry", pose="hold" if i == 1 else "down", turn=-0.5, seed=4)
        apron(g, 1180, 1150, 0.9)
        if i == 0:
            cap(g, "ห้องเก็บของ", 380, 180, 70, YEL2, ap(t, L[0] + 0.6), -3)
    elif i == 2:   # ผ้ายันต์ใกล้ ๆ
        darken(g, 0.4)
        k = ap(t, L[2])
        big_hand(g, 500, 700, 1.4 * k, -20, SRI.skin, SRI.suit)
        yantra_cloth(g, 980, 520, 2.6 * k, -6 + 2 * math.sin(t), 1)
        cap(g, "ผ้ายันต์แดง", 980, 930, 84, YEL2, ap(t, L[2] + 0.7), -2)
    else:   # ป้าศรีกระซิบ + ภาพเล่าในวงกลม
        with g.at(520, 640, 3.6):
            head(g, SRI, "worry" if i < 5 else "shock", 0.6 * (0.5 + 0.5 * math.sin(t * 9)), 0.4, (1, 0), 4)
        k = ap(t, L[3])
        with g.at(1350, 470, k):
            g.circle(0, 0, 380, hexc("#16211f"), 8)
            c.save()
            c.arc(0, 0, 372, 0, 2 * math.pi)
            c.clip()
            glow(g, 0, 60, 380, YEL, 0.3)
            if i == 3:   # หมอผีทำพิธี (เงา) + ด้ายสายสิญจน์ + เทียน
                with g.silhouette((0.03, 0.04, 0.04, 1)):
                    person(g, 0, 330, EK, 0.6, pose="hold", seed=9)
                for sx in (-1, 1):
                    for kk in range(2):
                        x = sx * (130 + kk * 100)
                        fill_rect(c, x - 10, 200, 20, 80, hexc("#eadfc0"))
                        glow(g, x, 190, 40, YEL2, 0.9)
                c.set_source_rgba(0.95, 0.95, 0.9, 0.8)
                c.set_line_width(3)
                c.move_to(-380, -80)
                c.curve_to(-100, -40, 100, -120, 380, -60)
                c.stroke()
            elif i == 4:   # ตู้เสื้อผ้าในอดีต (ไม่แสดงภาพการตาย)
                wardrobe(g, 0, 330, 300, 520, 0.0, 0, True, t=t)
                cap(g, "ดาว?", 0, -200, 70, YEL2, ap(t, L[4] + 0.5), -3)
            else:
                yantra_cloth(g, 0, 0, 1.6, 5, 2)
                glow(g, 0, 0, 300, (0.9, 0.2, 0.2, 1), 0.3 * (0.5 + 0.5 * math.sin(t * 6)))
            c.restore()
        if i == 5:
            cap(g, "ของแตก!", 1350, 950, 80, hexc("#e0705e"), ap(t, L[5] + 2.0), -4)
    vignette(g, 0.85)


# ================================================================ 13 สิ่งที่ไม่เข้ากัน
def staff_room(g, t):
    c = g.c
    fill_rect(c, -1500, -1500, W + 3000, 3000, hexc("#162021"))
    window_rain(g, 1250, 150, 360, 380, t, 0.5)
    fill_rect(c, -1500, 1000, W + 3000, 600, hexc("#1d2524"))
    _rr(c, 250, 760, 900, 120, 20)
    _shade(c, hexc("#55606a"), 5, 0.3)
    _rr(c, 250, 860, 900, 140, 8)
    _shade(c, WOOD2, 5, 0.3)


def s_doubt(g, t, L, d):
    c = g.c
    i = beat(t, L)
    if i < 2:
        staff_room(g, t)
        glow(g, 700, 600, 500, YEL, 0.15)
        person(g, 700, 1180, EK, 0.78, mood="worry", pose="hold", turn=0.2, seed=1)
        yantra_cloth(g, 700, 690, 0.55, -5)
        cap(g, "เอะใจ...", 1450, 760, 80, YEL2, ap(t, L[0] + 1.0), -3)
    elif i == 2:   # เปรียบเทียบ: คอขาวเนียน ไม่มีรอยเชือก
        fill_rect(c, -1500, -1500, W + 3000, 3000, NIGHT)
        glow(g, 960, 400, 800, YEL, 0.2)
        with g.at(800, 560, 3.2):
            g.blob(0, 140, 40, 70, GHOST_SKIN, 4.5, 3)   # คอ
            g.blob(0, 0, 60, 70, GHOST_SKIN, 4.5, 4)
            _rr(c, -70, 190, 140, 120, 30)
            _shade(c, GOWN, 4.5, 0.2)
            for sx in (-1, 1):
                _stroke(c, [(sx * 50, -70), (sx * 70, 60), (sx * 64, 220)], 18, BLACKHAIR, 1.0)
            g.blob(0, -40, 66, 40, BLACKHAIR, 0, 2)
        k = ap(t, L[2] + 1.0)
        with g.at(1450, 450, k):   # เชือก + กากบาท
            c.set_source_rgba(*hexc("#c9a35a"))
            c.set_line_width(14)
            c.arc(0, 0, 110, 0, 2 * math.pi)
            c.stroke()
            c.set_source_rgba(0.9, 0.3, 0.25, 1)
            c.set_line_width(22)
            c.move_to(-140, -140)
            c.line_to(140, 140)
            c.move_to(140, -140)
            c.line_to(-140, 140)
            c.stroke()
        cap(g, "ไม่มีรอยเชือก", 1450, 700, 76, YEL2, ap(t, L[2] + 1.5), -3)
    elif i < 5:   # เสียงเคาะ
        fill_rect(c, -1500, -1500, W + 3000, 3000, hexc("#100d0a"))
        wardrobe(g, 960, 1250, 900, 1300, 0.0, 0, False, t=t)
        sh = knock_shake(t, L[4] + 0.3)
        with g.at(960 + 20 * sh, 560):
            for k in range(3):
                g.circle(-120 + k * 120, 0, 14 + 30 * knock_shake(t, L[4] + 0.3 + k * 0.85, 1), YEL2, 0)
        if i >= 4:
            knock_txt(g, t, L[4] + 0.3, 600, 260)
    else:   # เหมือนคนขอความช่วยเหลือ
        fill_rect(c, -1500, -1500, W + 3000, 3000, hexc("#100d0a"))
        wardrobe(g, 960, 1250, 900, 1300, 0.0, 0, False, t=t)
        if i == 5:
            cap(g, "ไม่ใช่เสียงหลอกหลอน", CX, 320, 84, TEAL3, ap(t, L[5]), -2)
        else:
            glow(g, 960, 560, 300, YEL2, 0.2)
            cap(g, "“ช่วยด้วย”", CX, 520, 140, YEL2, ap(t, L[6] + 1.2), -3)
    vignette(g, 0.85)


# ================================================================ 14 ขโมยกุญแจ + ถุงปูน
def cement_bag(g, x, y, sc=1.0):
    c = g.c
    with g.at(x, y, sc):
        g.poly([(-150, 0), (150, 0), (170, -260), (90, -300), (-100, -290), (-170, -250)], hexc("#b8b29a"), 5, amp=0)
        g.text("ปูน", 0, -140, 70, "kanit", hexc("#7a3a2a"))
        g.blob(110, -290, 60, 26, hexc("#9a9a90"), 4, 2)


def rice_box(g, x, y, sc=1.0, label=True):
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -100, -70, 200, 70, 12)
        _shade(c, hexc("#e7e2d2"), 4, 0.15)
        _rr(c, -100, -90, 200, 26, 10)
        _shade(c, (0.85, 0.9, 0.9, 0.8), 3.5, 0.1)
        if label:
            _rr(c, -60, -56, 120, 40, 5)
            _shade(c, hexc("#f2d36a"), 2.5, 0.0)
            g.text("ผลิตวันนี้", 0, -36, 22, "kanit", INK)


def bottle(g, x, y, sc=1.0):
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -26, -150, 52, 150, 14)
        _shade(c, (0.75, 0.88, 0.95, 0.85), 4, 0.15)
        _rr(c, -14, -175, 28, 28, 4)
        _shade(c, hexc("#3a6aa0"), 3, 0.1)


def s_key(g, t, L, d):
    c = g.c
    i = beat(t, L)
    if i < 3:
        office_bg(g, t, 0.25)
        floor(g, 1000, hexc("#151513"))
        desk(g, 900, 1000)
        darken(g, 0.35)
        lx, ly = 900, 560
        if i == 0:
            cap(g, "คืนที่สาม", 400, 180, 100, YEL2, ap(t, L[0]), -3)
            beam(g, 1900, 200, 160, 1300, 8, 0.25 * max(0, math.sin(t * 2)))   # ไฟรถผ่าน
            person(g, 1500, 1260, EK, 0.75, mood="worry", pose="hold", turn=-0.5, seed=1)
        else:
            person(g, 1300, 1300, EK, 0.8, mood="worry", pose="hold", turn=-0.6, seed=1)
            flashlight(g, 1180, 760, 170 if i == 1 else 150, True, 800, 0.4)
            # ลิ้นชักเปิดทีละชั้น
            for k in range(3):
                ok = ap(t, L[1] + 0.8 * k) if i == 1 else 1.0
                _rr(c, 520 + 40 * ok, 800 + k * 60, 340, 52, 4)
                _shade(c, WOOD, 4, 0.25)
            if i == 2:   # กล่องพระ + กุญแจ
                k = ap(t, L[2])
                with g.at(700, 520, 1.8 * k):
                    _rr(c, -80, -60, 160, 70, 10)
                    _shade(c, hexc("#8a2a2a"), 4, 0.25)
                    g.circle(0, -25, 18, GOLDC, 3)
                    key_prop(g, 30, 30, 0.6, -8 + 30 * seg(t, L[2] + 1.5, L[2] + 2.5), "404")
                glow(g, 700, 520, 160, YEL2, 0.4 * k)
    else:   # ห้องเก็บของหลังโต๊ะ
        store_bg(g, t)
        darken(g, 0.45)
        sweep = lerp(200, 340, e_io(seg(t, L[3], L[4] + 2.0)))
        beam(g, 1900, 520, sweep - 160 + 180, 1500, 14, 0.35)
        cement_bag(g, 560, 1000, 1.25 * ap(t, L[3]))
        with g.at(860, 990, ap(t, L[3] + 0.8), -15):   # เกรียงคราบปูน
            g.poly([(-90, 0), (90, 0), (0, -110)], hexc("#a9a9a0"), 4, amp=0)
            _rr(c, -10, -190, 20, 90, 6)
            _shade(c, WOOD, 3, 0.2)
        if i >= 4:
            for k in range(4):
                bottle(g, 1080 + k * 70, 1000, 1.0 * ap(t, L[4] + 0.15 * k))
            for k in range(3):
                rice_box(g, 1500, 1000 - k * 76, 1.0 * ap(t, L[4] + 0.6 + 0.2 * k), k == 2)
            cap(g, "ยังไม่หมดอายุ...", 1400, 300, 80, hexc("#e0705e"), ap(t, L[4] + 2.0), -3)
        cap(g, "ถุงปูน", 560, 230, 80, YEL2, ap(t, L[3] + 1.0), -3)
    vignette(g, 0.85)


# ================================================================ 15 กลับมาที่ห้อง 404
def s_closet(g, t, L, d):
    c = g.c
    i = beat(t, L)
    if i < 4:
        room_bg(g, t, 0.45)
        bed_covered(g, 380, GROUND)
        shelf_incense(g, 700, 520, t)
        sh = knock_shake(t, L[2] + 0.3) if i >= 2 else 0
        wardrobe(g, 1350 + 8 * sh * math.sin(t * 70), GROUND, 440, 780, 0.0, 0, True, t=t)
        reach = e_io(seg(t, L[3], L[3] + 2.0)) if i >= 3 else 0
        person(g, 860 + 80 * reach, 1300, EK, 0.82, mood="worry", pose="hold" if i < 3 else "point",
               turn=0.9, seed=1)
        flashlight(g, 1000, 760, -8, True, 600, 0.35)
        if i == 0:
            cap(g, "คืนที่สาม · ห้อง 404", 520, 160, 76, YEL2, ap(t, L[0] + 0.5), -3)
        if i >= 2:
            knock_txt(g, t, L[2] + 0.3, 900, 200)
    elif i == 4:   # นับ หนึ่ง สอง (มือจับลูกบิด)
        fill_rect(c, -1500, -1500, W + 3000, 3000, TEAK)
        for k in range(4):
            _stroke(c, [(-100, 200 + k * 220), (2100, 160 + k * 230)], 4, WOOD2, 0.5)
        g.circle(1100, 560, 70, hexc("#b39a5b"), 6)
        big_hand(g, 1080, 600, 2.0, -5)
        cap(g, "1", 500, 380, 220, YEL2, ap(t, L[4] + 0.1), -6)
        cap(g, "2", 760, 420, 220, YEL2, ap(t, L[4] + 1.0), 6)
    else:   # กระชากเปิด!
        room_bg(g, t, 0.45)
        k = e_out(seg(t, L[5] - 0.1, L[5] + 0.35))
        wardrobe(g, 960, GROUND + 60, 620, 1000, k, 0, True, t=t,
                 inside=lambda g2: glow(g2, 960, 600, 300, YEL2, 0.25 * k))
        flash(g, 1 - seg(t, L[5], L[5] + 0.5))
    vignette(g, 0.9)


# ================================================================ 16 สิ่งที่อยู่ในตู้: ดาว
def dao_in_wardrobe(g, t, sc, bang=0.0, tape=1.0, look_up=0.0, light=1.0):
    def inside(g2):
        fill_rect(g2.c, 0, 0, W, H, (0.05, 0.05, 0.05, 1))
        for k in range(6):   # รอยข่วนในตู้
            _stroke(g2.c, [(760 + k * 30, 300), (780 + k * 26, 520)], 3, (0.6, 0.55, 0.5, 1), 0.5)
        bound_dao(g2, 870, GROUND + 40, 1.05, t, bang, tape, look_up)
    wardrobe(g, 960, GROUND + 60, 620, 1000, 1.0, 0, True, t=t, inside=inside)
    beam(g, 1900, 1100, -150, 1500, 10, 0.32 * light)


def s_dao(g, t, L, d):
    c = g.c
    i = beat(t, L)
    room_bg(g, t, 0.4)
    bang = max(0.0, math.sin(t * 5.5)) ** 3 if i == 3 else 0.0
    tape = 1.0 - e_io(seg(t, L[4] - 0.4, L[4] + 0.4)) if i >= 4 else 1.0
    lu = e_io(seg(t, L[4], L[4] + 0.8)) if i >= 4 else 0.0
    zoom = [1.0, 1.25, 1.55, 1.35, 1.6][i]
    with g.at(CX, CY, zoom):
        with g.at(-CX, -CY + (120 if i == 2 else 0)):
            dao_in_wardrobe(g, t, 1.0, bang, tape, lu)
    if i == 0:
        cap(g, "ไม่ใช่ผี...", 1500, 200, 96, YEL2, ap(t, L[0] + 0.8), -3)
    if i == 2:
        cap(g, "ถูกมัด", 1520, 220, 90, hexc("#e0705e"), ap(t, L[2] + 0.4), -4)
    vignette(g, 0.92)


# ================================================================ 17 ประตูปิดกระแทก
LT17 = []


def s_slam(g, t, L, d):
    c = g.c
    i = beat(t, L)
    if i < 2:   # ตัดเชือกด้วยคัตเตอร์
        fill_rect(c, -1500, -1500, W + 3000, 3000, hexc("#0b0d0d"))
        glow(g, 960, 540, 700, YEL, 0.2)
        _stroke(c, [(200, 600), (1700, 560)], 40, hexc("#3e78b8"), 1.0)
        _stroke(c, [(200, 600), (1700, 560)], 4, INK, 1.0)
        cut = e_io(seg(t, 1.0, 3.0))
        big_hand(g, 900 + 120 * cut, 470, 1.7, 15)
        with g.at(1060 + 120 * cut, 520, 1.7, 15):
            _rr(c, -10, -20, 170, 40, 8)
            _shade(c, hexc("#e0b030"), 4, 0.2)
            g.poly([(160, -14), (240, -4), (160, 12)], hexc("#c9ced0"), 3, amp=0)
        if i == 1:
            cap(g, "เส้นที่สอง...", 960, 900, 80, YEL2, ap(t, L[1] + 0.4), -2)
    elif i == 2:   # ปัง!
        room_bg(g, t, 0.4, window=False)
        k = e_out(seg(t, L[2] - 0.2, L[2]))
        sh = 18 * (1 - seg(t, L[2], L[2] + 0.5)) * math.sin(t * 90)
        door(g, 960 + sh, GROUND, 420, 800, open_k=1 - k, lock=False, talisman=False)
        cap(g, "ปัง!", 960 + sh, 300, 220, hexc("#f1e6a0"), pop(t, L[2] - 0.05, 0.25), -6)
        flash(g, 0.7 * (1 - seg(t, L[2], L[2] + 0.3)), (1, 1, 1))
    else:
        lt = lightning(t, [L[4] + 0.4, L[4] + 2.0, L[5] - 0.1, L[5] + 1.8])
        if i == 3:   # ไฟฉายดับ
            fill_rect(c, -1500, -1500, W + 3000, 3000, (0.01, 0.015, 0.02, 1))
            on = t < L[3] + 1.2
            flashlight(g, 700, 600, -10, on, 900, 0.4, 2.0)
            cap(g, "พรึ่บ", 1300, 300, 110, TEAL3, ap(t, L[3] + 1.2), -4)
        else:
            room_bg(g, t, 0.05 + 0.6 * lt, window=True, lt_times=[L[4] + 0.4, L[4] + 2.0, L[5] - 0.1, L[5] + 1.8])
            darken(g, 0.75 * (1 - lt))
            if i >= 5:   # ร่างคนยืนขวางประตู
                door(g, 960, GROUND, 420, 800, open_k=0, lock=False, talisman=False)
                with g.silhouette((0.02, 0.025, 0.03, 1), 1.0 - 0.6 * lt):
                    person(g, 960, GROUND + 10, LANDLORD, 0.85, mood="smug", pose="hold", seed=2)
                    sledgehammer(g, 960, GROUND - 60, 0.95, 25)
                if lt > 0.15:
                    person(g, 960, GROUND + 10, LANDLORD, 0.85, mood="smug", pose="hold", seed=2)
                    sledgehammer(g, 960, GROUND - 60, 0.95, 25)
                    darken(g, 0.55 * (1 - lt))
            flash(g, lt)
    vignette(g, 0.92)


# ================================================================ 18 ความจริงจากปากเจ้าของตึก
def s_truth(g, t, L, d):
    c = g.c
    i = beat(t, L)
    lts = [L[1] + 0.5, L[3] + 1.0, L[5] + 0.3]
    lt = lightning(t, lts)
    room_bg(g, t, 0.35 + 0.4 * lt, patch=1.0 if i >= 5 else 0.0, lt_times=lts)
    if i in (0, 2, 3):   # หน้าใกล้ เย็นชา
        with g.at(960, 560, 4.0):
            head(g, LANDLORD, "smug", 0.7 * (0.5 + 0.5 * math.sin(t * 8)), 0.0, (0, 0), 2)
        if i == 2:
            cap(g, "ฉันปล่อยข่าวเอง", 1550, 240, 70, hexc("#e0705e"), ap(t, L[2] + 1.0), -3)
    elif i == 1:   # ลากค้อน
        x = lerp(1250, 980, e_io(seg(t, L[1], L[2])))
        person(g, x, 1120, LANDLORD, 0.95, mood="smug", pose="hold", turn=-0.3, seed=2)
        gold_chain(g, x, 1120 - 650 * 0.95 + 30, 45)
        sledgehammer(g, x - 140, 1100, 1.0, -70)
        bound_dao(g, 1700, GROUND + 60, 0.6, t)
    elif i == 4:   # "มันเป็นลูกฉัน" — กรอบรูปพ่อลูก
        darken(g, 0.4)
        k = ap(t, L[4])
        with g.at(960, 500, k, -4):
            _rr(c, -360, -300, 720, 560, 12)
            _shade(c, hexc("#c9a35a"), 8, 0.2)
            fill_rect(c, -320, -260, 640, 480, hexc("#3f5a5a"))
            c.save()
            c.rectangle(-320, -260, 640, 480)
            c.clip()
            person(g, -110, 560, LANDLORD, 0.62, mood="smile", pose="down", turn=0.2, seed=2)
            person(g, 130, 560, DAO, 0.62, mood="smile", pose="down", turn=-0.2, seed=7)
            c.restore()
            _stroke(c, [(-320, -100), (40, 60), (320, -20)], 3, (0.9, 0.9, 0.9, 1), 0.7)   # กระจกร้าว
        cap(g, "ลูกสาว", 1600, 200, 100, hexc("#e0705e"), ap(t, L[4] + 1.6), -3)
    else:   # ผนังฉาบปูนใหม่ด้านเดียว
        person(g, 1300, 1150, EK, 0.8, mood="shock", pose="hold", turn=-0.8, seed=1)
        cap(g, "ผนังฉาบใหม่", 1000, 200, 84, YEL2, ap(t, L[5] + 1.0), -3)
    flash(g, lt * 0.6)
    vignette(g, 0.9)


# ================================================================ 19 เงาบนเพดาน
def s_shadow(g, t, L, d):
    c = g.c
    i = beat(t, L)
    room_bg(g, t, 0.35, patch=1.0)
    if i < 1 or i == 1:
        if i == 0:
            with g.at(960, 560, 3.6):
                head(g, EK, "shock", 0.0, 0.1, (0.3, -1.0), 1)
            cap(g, "เพดาน...", 1550, 240, 80, YEL2, ap(t, L[0] + 2.0), -3)
            vignette(g, 0.9)
            return
    # เจ้าของตึกหันหลังให้ผนัง เงาคลานลงมาด้านหลัง
    desc = e_io(seg(t, L[1], L[3] + 3.0))
    shadow_crawler(g, 470, lerp(-200, 420, desc), 0.75, t, desc)
    person(g, 760, 1180, LANDLORD, 1.0, mood="smug", pose="hold", turn=0.3, seed=2)
    sledgehammer(g, 900, 1150, 1.0, -20)
    if i >= 3:
        for k in range(8):   # เศษปูนร่วง
            y = (t * 300 + k * 140) % 900
            g.circle(400 + k * 30, y, 5, (0.6, 0.62, 0.6, 1), 0)
    vignette(g, 0.92)


# ================================================================ 20 เฉลยความจริง
def wall_woman(g, t, a=1.0, eyes_open=0.0):
    c = g.c
    with g.alpha(a):
        fill_rect(c, 560, 60, 800, 960, hexc("#5f6966"))
        for k in range(18):
            x = 560 + (k % 6) * 140
            y = 60 + (k // 6) * 320
            _rr(c, x + 6, y + 6, 128, 300, 4)
            _shade(c, hexc("#727b78"), 3, 0.15)
        fill_rect(c, 760, 140, 400, 820, hexc("#3a4140"))
        with g.alpha(0.75):
            person(g, 960, 960, GHOST, 0.82, mood="sad" if eyes_open < 0.5 else "neutral", pose="down", seed=8)
        glow(g, 960, 500, 400, TEAL3, 0.3)


def s_reveal(g, t, L, d):
    c = g.c
    i = beat(t, L)
    fill_rect(c, -1500, -1500, W + 3000, 3000, hexc("#0c1617"))
    if i == 0:
        with g.at(960, 560, 3.6):
            head(g, EK, "shock", 0.0, 0.0, (0, 0), 1)
        glow(g, 960, 540, 800, TEAL3, 0.15)
    elif i == 1:   # ภาพย้อนสองภาพ
        for k, (x, rot) in enumerate(((560, -4), (1360, 4))):
            kk = ap(t, L[1] + 1.2 * k)
            if kk < 0.02:
                continue
            with g.at(x, 520, kk, rot):
                _rr(c, -330, -260, 660, 520, 14)
                _shade(c, hexc("#e9e4d0"), 8, 0.1)
                c.save()
                c.rectangle(-300, -230, 600, 460)
                c.clip()
                fill_rect(c, -300, -230, 600, 460, lerp_col(YEL, NIGHT, 0.5) if k == 0 else (0.02, 0.02, 0.02, 1))
                if k == 0:
                    ghost_back(g, 0, 300, 0.55, t)
                else:
                    ghost_face(g, 0, 0, 0.8, t, 1.0)
                c.restore()
    elif i == 2:
        darken(g, 0.4)
        cap(g, "ไม่เคยเป็นดาว", CX, CY, 130, YEL2, ap(t, L[2]), -3)
    elif i == 3:
        wall_woman(g, t, fade_in(t, L[3], 1.0))
        cap(g, "3 ปีก่อน", 300, 160, 90, YEL2, ap(t, L[3] + 1.5), -3)
    else:   # เธอเรียกเขามาช่วยดาว
        wall_woman(g, t, 0.35)
        person(g, 600, 1080, GHOST, 0.9, mood="sad" if i == 4 else "smile", pose="down" if i == 4 else "point",
               turn=0.6, seed=8)
        if i == 5:
            dao_x = 1450
            bound_dao(g, dao_x, 1000, 0.75, t)
            glow(g, dao_x + 60, 700, 300, YEL2, 0.3)
            cap(g, "ช่วยดาว", 1450, 200, 100, YEL2, ap(t, L[5] + 1.0), -3)
    vignette(g, 0.88)


# ================================================================ 21 ในความมืด
def s_dark(g, t, L, d):
    c = g.c
    i = beat(t, L)
    lts = [L[2] - 0.1]
    lt = lightning(t, lts)
    if i < 2 or (i == 2 and t < L[2] + 0.3):
        room_bg(g, t, 0.35 + 0.6 * lt, patch=1.0, lt_times=lts)
        raise_k = e_io(seg(t, L[0], L[0] + 1.6))
        person(g, 900, 1150, LANDLORD, 1.0, mood="angry", pose="down", pose2="v", k=raise_k, turn=0.4, seed=2)
        sledgehammer(g, 900 + 60 * raise_k, lerp(1150, 400, raise_k), 1.0, lerp(-60, 10, raise_k))
        shadow_crawler(g, 560, 420, 0.75, t, 1.0)
        flash(g, lt)
    else:
        fill_rect(c, -1500, -1500, W + 3000, 3000, (0.005, 0.008, 0.01, 1))
        if i == 3:   # เส้นผมแวบในความมืด
            for k in range(7):
                x = 860 + k * 30 + 40 * math.sin(t * 3 + k)
                _stroke(c, [(x, 0), (x + 20, 400), (x - 10, 760)], 6, (0.12, 0.15, 0.15, 1), 0.7)
        if i >= 5:   # ค้อนตก + สร้อยทองแวบ
            k = fade_in(t, L[5] + 0.6, 1.5)
            glow(g, 960, 860, 500, TEAL3, 0.18 * k)
            with g.alpha(k):
                sledgehammer(g, 960, 900, 1.0, -88)
                c.new_path()
                c.arc(1300, 900, 60, math.radians(10), math.radians(170))
                c.set_source_rgba(*GOLDC)
                c.set_line_width(8)
                c.stroke()
                g.sparkle(1320, 950, 22 * k, YEL2, 0)
                _stroke(c, [(1500, 880), (1700, 860), (1900, 900)], 5, (0.1, 0.12, 0.12, 1), 0.8)   # เส้นผมลากหายไป
    vignette(g, 0.95)


# ================================================================ 22 หนีออกจากตึก
def police_lights(g, t, a=1.0):
    r = 0.5 + 0.5 * math.sin(t * 8)
    glow(g, 200, 700, 900, (0.9, 0.15, 0.15, 1), 0.28 * r * a)
    glow(g, 1700, 700, 900, (0.15, 0.3, 0.95, 1), 0.28 * (1 - r) * a)


def s_escape(g, t, L, d):
    c = g.c
    i = beat(t, L)
    if i < 3:
        fill_rect(c, -1500, -1500, W + 3000, 3000, NIGHT)
        building(g, t, 960, 900, 5, 5, lit={(4, 2): 0.0}, sign=True)
        fill_rect(c, -1500, 900, W + 3000, 600, hexc("#121818"))
        for k in range(8):   # น้ำท่วมขังสะท้อนแสง
            g.blob(200 + k * 230, 1000 + 20 * (k % 2), 120, 14, (0.6, 0.8, 0.85, 0.12), 0, k)
        x = lerp(700, 1150, e_io(seg(t, L[1], d))) if i >= 1 else 700
        y = 1180
        with g.at(x - 70, y - 0.72 * 900, 0.72):   # ดาวขี่หลัง (อยู่หลังเอก หัวพาดไหล่)
            g.blob(-20, 200, 100, 150, DAO.suit, 4.5, 3)
            head(g, DAO, "sad", 0.0, 0.4, (0, 0.3), 7)
        person(g, x, y, EK, 0.72, mood="worry", pose="hold", turn=0.5, seed=1, lean=6)
        with g.at(x - 70, y - 0.72 * 900, 0.72):   # แขนดาวโอบคอเอก
            _stroke(c, [(20, 170), (110, 230), (190, 230)], 30, DAO.suit, 1.0)
            _stroke(c, [(20, 170), (110, 230), (190, 230)], 4.5, INK, 1.0)
            g.circle(196, 230, 16, DAO.skin, 4)
        if i >= 1:
            police_lights(g, t, fade_in(t, L[2], 1.5))
        rain(g, t, 0.55, 140)
    elif i < 5:   # ตำรวจทุบผนัง + ผ้าคลุม (ไม่แสดงร่าง)
        room_bg(g, t, 0.6, patch=0.0, window=False)
        fill_rect(c, 140, 60, 620, GROUND - 60, hexc("#6d7774"))
        g.blob(450, 470, 170, 300, (0.05, 0.05, 0.05, 1), 6, 4)   # รูผนัง
        for k in range(10):
            g.blob(300 + k * 40, GROUND - 20, 30, 16, hexc("#7b8582"), 4, k)
        if i == 4:
            _rr(c, 850, GROUND - 330, 600, 90, 30)
            _shade(c, WHITE, 5, 0.2)
            for k in range(3):
                with g.at(950 + k * 200, GROUND - 360, ap(t, L[4] + 0.4 * k)):
                    g.poly([(-30, 0), (30, 0), (0, -60)], hexc("#f2c94c"), 4, amp=0)
                    g.text(str(k + 1), 0, -20, 26, "kanit", INK)
        _stroke(c, [(-200, 300), (2200, 360)], 34, hexc("#f2c94c"), 1.0)
        g.text("POLICE LINE · ห้ามผ่าน · POLICE LINE · ห้ามผ่าน", 960, 330, 26, "kanit", INK, rot=1.4)
        police_lights(g, t, 0.6)
        cap(g, "เช้ามืด", 1600, 170, 80, YEL2, ap(t, L[3]), -3)
    else:   # หนังสือพิมพ์
        fill_rect(c, -1500, -1500, W + 3000, 3000, hexc("#1c2422"))
        k = ap(t, L[5])
        with g.at(960, 540, k, -3 + 360 * (1 - k)):
            _rr(c, -560, -380, 1120, 760, 6)
            _shade(c, hexc("#e9e4d0"), 6, 0.12)
            g.text("ข่าวด่วน", -380, -300, 50, "kanit", hexc("#a82a2a"))
            g.text("พบโครงกระดูกในผนัง", 0, -190, 84, "kanit", INK)
            g.text("เจ้าของตึกเสียชีวิตปริศนา", 0, -80, 64, "kanit", INK)
            for r in range(5):
                _stroke(c, [(60, 20 + r * 60), (500, 20 + r * 60)], 8, LGREY_SAFE, 1.0)
            _rr(c, -500, 0, 480, 320, 6)
            _shade(c, hexc("#4a5452"), 4, 0.1)
            with g.at(-260, 330, 0.3):
                building(g, t, 0, 0, 3, 3, sign=False)
    vignette(g, 0.85)


LGREY_SAFE = hexc("#9a968c")


# ================================================================ 23 หนึ่งเดือนต่อมา: ทำบุญ
def temple_bg(g, t):
    c = g.c
    fill_rect(c, -1500, -1500, W + 3000, 3000, hexc("#9fb3a8"))
    glow(g, 1500, 200, 900, hexc("#f4e2a6"), 0.5)
    for k in range(6):   # เสาศาลา
        _rr(c, -200 + k * 440, 0, 60, 1000, 4)
        _shade(c, hexc("#e8e0cc"), 5, 0.2, horiz=False)
    g.poly([(-400, 0), (2400, 0), (2200, -200), (-200, -200)], hexc("#a8452f"), 5, amp=0)
    fill_rect(c, -1500, 1000, W + 3000, 600, hexc("#c9b48a"))
    for k in range(5):   # กระดิ่งลม
        x = 300 + k * 330
        _stroke(c, [(x, 0), (x, 120)], 3, INK, 1.0)
        g.blob(x, 140 + 6 * math.sin(t * 2 + k), 18, 24, GOLDC, 3, k)


def s_merit(g, t, L, d):
    c = g.c
    i = beat(t, L)
    temple_bg(g, t)
    if i == 0:
        cap(g, "1 เดือนต่อมา", CX, 260, 110, hexc("#fff8e0"), ap(t, L[0]), -3)
    # สองคนนั่งพับเพียบกรวดน้ำ
    for x, look, seed in ((760, EK, 1), (1100, DAO, 7)):
        with g.at(x, 1000, 0.85):
            g.blob(0, -120, 150, 130, look.suit, 4.5, seed)
            with g.at(0, -330):
                head(g, look, "sad" if i < 3 else "smile", 0.0, 0.3, (0.5, 0.6), seed)
    with g.at(930, 800, 0.9):   # คนโทกรวดน้ำ + สายน้ำ
        g.blob(0, 0, 50, 40, GOLDC, 4, 2)
        _stroke(c, [(40, -10), (80, -30)], 10, GOLDC, 1.0)
        c.set_source_rgba(0.6, 0.85, 0.95, 0.8)
        c.set_line_width(5)
        c.move_to(82, -28)
        c.curve_to(110, 20, 100, 80, 95, 160)
        c.stroke()
        g.blob(95, 180, 50, 20, hexc("#c9c2a8"), 4, 3)
    if i >= 2:   # กรอบรูปไร้ชื่อ + ดาวเรือง
        k = ap(t, L[2])
        with g.at(1550, 600, k):
            _rr(c, -130, -170, 260, 320, 8)
            _shade(c, hexc("#2a2a2a"), 6, 0.1)
            fill_rect(c, -100, -140, 200, 260, hexc("#d9d6cc"))
            g.blob(0, -40, 50, 60, (0.6, 0.6, 0.6, 1), 0, 2)
            g.blob(0, 80, 80, 60, (0.6, 0.6, 0.6, 1), 0, 3)
            g.text("?", 0, -40, 70, "kanit", WHITE)
            for kk in range(6):
                g.blob(-150 + kk * 60, 190, 28, 26, hexc("#e2932b"), 3, kk)
    if i >= 3:   # วิญญาณยิ้มจาง ๆ
        with g.alpha(0.35 * fade_in(t, L[3], 1.5)):
            person(g, 1850, 1000, GHOST, 0.8, mood="smile", pose="down", turn=-0.4, seed=8)
    smoke(g, 1550, 820, t, 3, 0.15, 5, 50) if i >= 2 else None


# ================================================================ 24 เสียงเคาะครั้งสุดท้าย
def s_final(g, t, L, d):
    c = g.c
    i = beat(t, L)
    fill_rect(c, -1500, -1500, W + 3000, 3000, hexc("#101a1d"))
    window_rain(g, 160, 160, 360, 400, t, 0.4)
    glow(g, 340, 360, 500, TEAL3, 0.12)
    fill_rect(c, -1500, 1000, W + 3000, 600, hexc("#141c1d"))
    # เตียง + เอกนอนตะแคงลืมตา
    _rr(c, 120, 760, 1000, 240, 30)
    _shade(c, hexc("#4a5a6a"), 5, 0.3)
    with g.at(380, 700, 1.6):
        head(g, EK, "worry" if i >= 3 else "neutral", 0.0, 0.6, (1, 0), 1)
    _rr(c, 420, 720, 680, 200, 60)
    _shade(c, hexc("#6a7f8f"), 5, 0.3)
    # ตู้เสื้อผ้าขาว (ห้องใหม่)
    sh = knock_shake(t, L[3] + 0.3) if i >= 3 else 0.0
    crack = 0.06 * e_io(seg(t, L[4], L[4] + 2.0)) if i >= 4 else 0.0
    wx = 1500

    def inside(g2):
        if i >= 5:
            fx = wx - 10
            ret = e_io(seg(t, L[5] + 1.8, L[5] + 3.0))
            for k in range(4):
                g2.blob(fx + 10 * k - 20 * ret, 560 + k * 26, 18, 10, GHOST_SKIN, 3, k)
            for k in range(4):
                _stroke(g2.c, [(fx - 10 + 6 * k, 300), (fx - 6 + 6 * k, 520)], 3, BLACKHAIR, 1.0)
    wardrobe(g, wx + 6 * sh * math.sin(t * 70), 1000, 460, 840, crack, 0, False, t=t, inside=inside)
    if i == 0:
        cap(g, "ห้องเช่าใหม่", 760, 160, 80, YEL2, ap(t, L[0] + 0.6), -3)
    if i >= 3 and i < 5:
        knock_txt(g, t, L[3] + 0.3, 1150, 200, size=80)
    if i >= 5:
        cap(g, "“ขอบคุณนะ...”", 960, 260, 96, hexc("#cfe7df"), ap(t, L[5] + 0.3), -2,
            1 - seg(t, L[5] + 3.0, L[5] + 3.6))
    # ตัดดำ + ข้อความปิด
    te = L[5] + 3.4
    if t > te:
        darken(g, e_io(seg(t, te, te + 0.4)))
        cap(g, "บางเสียงเคาะ...", CX, CY - 50, 90, hexc("#e9e4d0"), pop(t, te + 0.6, 0.5))
        cap(g, "ไม่ได้ต้องการให้คุณกลัว", CX, CY + 70, 80, hexc("#e9e4d0"), pop(t, te + 1.4, 0.5))
        return
    vignette(g, 0.9)


SCENES = {
    "open": s_open, "lock": s_lock, "knock": s_knock, "back": s_back, "owner": s_owner, "balcony": s_balcony,
    "logbook": s_logbook, "empty": s_empty, "cry": s_cry, "peephole": s_peephole, "sri": s_sri, "yantra": s_yantra,
    "doubt": s_doubt, "key": s_key, "closet": s_closet, "dao": s_dao, "slam": s_slam, "truth": s_truth,
    "shadow": s_shadow, "reveal": s_reveal, "dark": s_dark, "escape": s_escape, "merit": s_merit, "final": s_final,
}
