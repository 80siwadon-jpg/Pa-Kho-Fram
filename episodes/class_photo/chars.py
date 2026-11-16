"""ตัวละคร/ฉากตอน class_photo (เจริญศิลป์โฟโต้ ตอน 2) — ต่อยอดจาก episodes/funeral_photo/chars.py"""
import importlib.util
import math
import cairo
import os
import sys

_FP = os.path.join(os.path.dirname(__file__), "..", "funeral_photo", "chars.py")
_spec = importlib.util.spec_from_file_location("fp_chars", _FP)
_fp = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_fp)
globals().update({k: v for k, v in vars(_fp).items() if not k.startswith("__")})

from gfx import INK, WHITE, H, W, hexc, hn, lerp  # noqa: E402,F401
from people import Look, _rr, _shade, _smooth_path, _stroke, person  # noqa: E402,F401

head = _fp.flat_head
_fp.STYLE = "sigma"   # หน้าตาแบบคลิปต้นแบบ: ตาเล็ก คิ้วสั้น หัวกลม ไหล่พอง

# ---------------------------------------------------------------- looks
TON = Look(hair="buzz", hair_col=hexc("#3a2c22"), skin=hexc("#c98f63"), outfit="gown", suit=hexc("#e07a1f"),
           w=56, height=0.66, headsc=1.35, build=0.8, jaw=0.15, age=0.0)
SOMJAI = Look(hair="bun", hair_col=hexc("#5f5a55"), skin=hexc("#d4a07a"), outfit="tee", suit=hexc("#c9b6d6"),
              pants=hexc("#4a4458"), glasses="thin", age=0.65, w=54, build=0.9, jaw=0.2, height=0.94)
FAI = Look(hair="long", hair_col=hexc("#151316"), skin=hexc("#b7c2c2"), outfit="dress", suit=hexc("#eef0ee"),
           w=50, height=0.6, headsc=1.4, build=0.7, jaw=0.05, age=0.0)
FAI_ALIVE = Look(hair="long", hair_col=hexc("#1a1512"), skin=hexc("#c99168"), outfit="dress", suit=hexc("#f2f2ee"),
                 w=50, height=0.6, headsc=1.4, build=0.7, jaw=0.05, age=0.0)
PHIAN = Look(hair="bun", hair_col=hexc("#d8d6d0"), skin=hexc("#b8835c"), outfit="dress", suit=hexc("#7d6a55"),
             age=1.0, w=52, build=0.8, height=0.86, jaw=0.15)
COP = Look(hair="bald", hair_col=hexc("#2a221c"), skin=hexc("#c48a5e"), outfit="tee", suit=hexc("#7a5a3a"),
           pants=hexc("#5a4a38"), w=58, build=1.05)
OUAN = Look(hair="crew", hair_col=hexc("#1a1512"), skin=hexc("#d29a6c"), outfit="tee", suit=hexc("#3f6d8a"),
            pants=hexc("#3a3f45"), w=66, build=1.45, jaw=0.9)
MATHT = Look(hair="part", hair_col=hexc("#1a1512"), skin=hexc("#d8a57c"), outfit="tee", suit=hexc("#6a8a5a"),
             pants=hexc("#3a3f45"), glasses="round", w=56)
CLASSMATES = [COP, OUAN, MATHT,
              Look(hair="long", hair_col=hexc("#2a1f18"), skin=hexc("#dcab84"), outfit="tee", suit=hexc("#b84a4a"), w=52, build=0.85),
              Look(hair="short", hair_col=hexc("#1a1512"), skin=hexc("#c48a5e"), outfit="tee", suit=hexc("#d9c27a"), w=54),
              Look(hair="bun", hair_col=hexc("#2a1f18"), skin=hexc("#e0b08a"), outfit="tee", suit=hexc("#4a7a8a"), w=52, build=0.85)]

UNIFORM_W = hexc("#f2f2ee")
UNIFORM_SKIRT = hexc("#2b3f63")
UNIFORM_SHORTS = hexc("#3a3a40")
POND = hexc("#1f3a38")
LOTUS = hexc("#e8a6b8")
LEAF = hexc("#3f6b46")


# ---------------------------------------------------------------- props
def mini_kid(g, x, y, sc, seed, girl=None, ghost=0.0, blur=0.0, smile=True):
    """เด็กนักเรียนตัวเล็กในรูปหมู่ (วาดเร็ว): หัวกลม ผม เสื้อนักเรียน"""
    c = g.c
    girl = (hn(seed, 3) > 0) if girl is None else girl
    skin = lerp_col(hexc("#c48a5e"), hexc("#e0b08a"), hn(seed, 4) * 0.5 + 0.5)
    if ghost:
        skin = lerp_col(skin, hexc("#b7c2c2"), ghost)
    with g.alpha(1.0 - 0.35 * blur):
        with g.at(x + 6 * blur * math.sin(g.t * 3 + seed), y, sc):
            _rr(c, -30, -10, 60, 70, 18)
            _shade(c, UNIFORM_W, 2, 0.15)
            _rr(c, -30, 50, 60, 30, 8)
            _shade(c, UNIFORM_SKIRT if girl else UNIFORM_SHORTS, 2, 0.1)
            g.circle(0, -42, 30, skin, 0)
            hair = hexc("#151316") if ghost else hexc("#1a1512")
            if girl:
                g.blob(0, -58, 34, 22, hair, 0, seed)
                for sx in (-1, 1):
                    g.blob(sx * 26, -30, 9, 22 + 8 * ghost, hair, 0, seed + sx)
            else:
                g.blob(0, -62, 30, 14, hair, 0, seed)
            for sx in (-1, 1):
                g.circle(sx * 10, -44, 3.5, INK, 0)
            if smile and not ghost:
                _stroke(c, [(-8, -30), (0, -26), (8, -30)], 2.2, hexc("#6a2e26"), 1.0)
            elif ghost:
                _stroke(c, [(-6, -29), (6, -29)], 2, hexc("#4a4a4a"), 1.0)
            if ghost > 0.5:   # หยดน้ำ
                for k in range(3):
                    yy = ((g.t * 40 + k * 23 + seed * 7) % 70)
                    g.circle(-20 + k * 20, 10 + yy, 3, (0.7, 0.85, 0.95, 0.8), 0)


def class_photo(g, x, y, w, t, extra=0, extra_k=1.0, bw=True, teacher=True, fai_smile=False):
    """รูปหมู่ ป.6 ปี 2542 (32 คน) — extra: 0 ไม่มีเด็กเกิน, 1 แถวหลังริมขวา(เบลอ), 2 แถวกลาง, 3 แถวหน้า,
    4 = ภาพใหม่ (ฝ้ายนั่งข้างครู ยิ้ม)"""
    c = g.c
    h = w * 0.66
    sc = w / 1200
    with g.at(x, y):
        _rr(c, -w / 2 - 14, -h / 2 - 14, w + 28, h + 28, 6)
        _shade(c, hexc("#e9e4d6"), 2, 0.1)
        c.save()
        c.rectangle(-w / 2, -h / 2, w, h)
        c.clip()
        fill_rect(c, -w / 2, -h / 2, w, h, hexc("#a8a49a") if bw else hexc("#9ab0a8"))
        fill_rect(c, -w / 2, -h / 2, w, h * 0.45, hexc("#c9c4b6") if bw else hexc("#d8cfb0"))   # ผนังอาคาร
        for k in range(6):
            fill_rect(c, -w / 2 + 40 * sc + k * 200 * sc, -h / 2 + 30 * sc, 120 * sc, 90 * sc, hexc("#8a8678"))
        rows = [(-h * 0.12, 12, 0.9), (h * 0.08, 11, 0.95), (h * 0.28, 10, 1.0)]   # 12+11+9 = 32 คน
        n = 0
        for ri, (ry, cnt, rs) in enumerate(rows):
            for k in range(cnt):
                if ri == 2 and k == cnt // 2 and teacher:
                    continue
                kx = (k - (cnt - 1) / 2) * (w * 0.86 / cnt)
                mini_kid(g, kx, ry, sc * 1.25 * rs, seed=n + 1)
                n += 1
        if teacher:   # ครูนั่งกลางแถวหน้า (ผมมวย แว่น เสื้อม่วง)
            tx = (10 // 2 - 4.5) * (w * 0.86 / 10)
            with g.at(tx, rows[2][0] - 6 * sc, sc * 1.4):
                _rr(c, -34, -12, 68, 82, 18)
                _shade(c, hexc("#b7a6c9"), 2, 0.15)
                g.circle(0, -44, 30, hexc("#d9a982"), 0)
                g.blob(0, -64, 30, 14, hexc("#2a2420"), 0, 9)
                g.circle(0, -80, 12, hexc("#2a2420"), 0)
                for sx in (-1, 1):
                    g.circle(sx * 11, -44, 7, None, 2)
                    g.circle(sx * 11, -44, 3, INK, 0)
                _stroke(c, [(-7, -30), (0, -27), (7, -30)], 2.2, hexc("#6a2e26"), 1.0)
        # เด็กผู้หญิงที่เกินมา
        if extra and extra_k > 0.01:
            pos = {1: (w * 0.44, rows[0][0], 0.9, 1.0), 2: (w * 0.06, rows[1][0], 0.95, 0.4),
                   3: (-w * 0.12, rows[2][0] + 20 * sc, 1.05, 0.0), 4: (-w * 0.1, rows[2][0], 1.0, 0.0)}[extra]
            ex, ey, es, eb = pos
            with g.alpha(extra_k):
                if extra == 4:
                    mini_kid(g, ex, ey, sc * 1.25 * es, 77, True, 0.25, 0.0, True)
                else:
                    mini_kid(g, ex, ey, sc * 1.25 * es, 77, True, 1.0, eb, False)
        c.restore()


def footprints(g, pts, t, t0, sc=1.0, gap=0.35):
    """รอยเท้าเปียกเล็ก ๆ ปรากฏทีละรอย"""
    for i, (x, y, rot) in enumerate(pts):
        a = min(max((t - t0 - i * gap) / 0.25, 0.0), 1.0)
        if a <= 0:
            continue
        with g.at(x, y, sc, rot):
            g.blob(0, 0, 14, 26, (0.55, 0.7, 0.75, 0.55 * a), 0, i)
            for k in range(4):
                g.circle(-9 + k * 6, -30, 4, (0.55, 0.7, 0.75, 0.5 * a), 0)


def handprints(g, n, t, t0, area=(300, 150, 1300, 650), gap=0.25):
    x0, y0, aw, ah = area
    for i in range(n):
        a = min(max((t - t0 - i * gap) / 0.2, 0.0), 1.0)
        if a <= 0:
            continue
        x = x0 + (hn(i, 41) * 0.5 + 0.5) * aw
        y = y0 + (hn(i, 42) * 0.5 + 0.5) * ah
        with g.at(x, y, 0.9 + 0.2 * hn(i, 43), 25 * hn(i, 44)):
            g.blob(0, 0, 22, 26, (0.75, 0.85, 0.88, 0.4 * a), 0, i)
            for k in range(5):
                ang = math.radians(-60 + k * 28)
                g.blob(math.sin(ang) * 30, -math.cos(ang) * 30 - 8, 6, 14, (0.75, 0.85, 0.88, 0.4 * a), 0, i + k)


def coin_jar(g, x, y, sc=1.0):
    c = g.c
    with g.at(x, y, sc):
        g.blob(0, 0, 70, 80, (0.75, 0.85, 0.82, 0.55), 3, 2)
        _rr(c, -40, -96, 80, 22, 6)
        _shade(c, hexc("#c84a3a"), 2, 0.2)
        for k in range(8):
            g.circle(-35 + (k % 4) * 23, 40 - (k // 4) * 18, 11, hexc("#c9a64a"), 1.5)


def roll_book(g, x, y, sc=1.0, rot=0, highlight=False):
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -300, -200, 600, 400, 10)
        _shade(c, hexc("#efe6cf"), 3, 0.1)
        _stroke(c, [(0, -200), (0, 200)], 4, hexc("#9a8a6a"), 0.8)
        for k in range(9):
            _stroke(c, [(-280, -160 + k * 38), (-30, -160 + k * 38)], 2, hexc("#9ab0c9"), 1.0)
            _stroke(c, [(30, -160 + k * 38), (280, -160 + k * 38)], 2, hexc("#9ab0c9"), 1.0)
        g.text("ด.ญ.ฝ้าย ใจดี", 150, 150, 30, "kanitm", hexc("#8a8a90"), rot=-2)
        if highlight:
            c.set_source_rgba(0.95, 0.75, 0.2, 0.9)
            c.set_line_width(5)
            _rr(c, 20, 125, 260, 52, 12)
            c.stroke()


def fireflies(g, t, n=18, area=(0, 200, W, 700), seed=5):
    x0, y0, aw, ah = area
    for i in range(n):
        px = x0 + (hn(i, seed) * 0.5 + 0.5) * aw + 30 * math.sin(t * 0.7 + i)
        py = y0 + (hn(i, seed + 1) * 0.5 + 0.5) * ah + 20 * math.sin(t * 0.9 + i * 1.3)
        b = 0.5 + 0.5 * math.sin(t * 2.3 + i * 2.1)
        glow(g, px, py, 18, (0.85, 1.0, 0.6, 1), 0.7 * b)


def school_bell(g, x, y, sc, t, ring=0.0):
    c = g.c
    with g.at(x, y, sc):
        _stroke(c, [(-160, -260), (160, -260)], 14, WOOD2, 1.0)
        for sx in (-1, 1):
            _stroke(c, [(sx * 150, -260), (sx * 150, 300)], 14, WOOD2, 1.0)
        with g.at(0, -250, 1.0, 14 * ring * math.sin(t * 18)):
            _smooth_path(c, [(-70, 0), (70, 0), (90, 150), (-90, 150)])
            _shade(c, hexc("#a8873a"), 3, 0.3)
            g.circle(0, 160, 14, hexc("#5a4a2a"), 0)


# ---------------------------------------------------------------- sets
def set_school_dusk(g, dark=0.0):
    """ลานหน้าเสาธง + อาคารเรียนไม้ เวลาพลบค่ำ"""
    c = g.c
    sky = lerp_col(hexc("#d98a5a"), hexc("#1b2530"), dark)
    fill_rect(c, -800, -800, W + 1600, H + 1600, sky)
    _rr(c, 200, 300, 1400, 450, 6)   # อาคารเรียนไม้สองชั้น
    _shade(c, lerp_col(WOOD, hexc("#3a2c22"), dark), 4, 0.25)
    g.poly([(150, 300), (1650, 300), (1500, 160), (300, 160)], lerp_col(TEMPLE_RED, hexc("#3a1f18"), dark), 3, amp=0)
    for r in range(2):
        for k in range(7):
            fill_rect(c, 260 + k * 190, 340 + r * 200, 120, 120, lerp_col(hexc("#c9d6d8"), hexc("#1a2028"), dark))
    fill_rect(c, -800, 750, W + 1600, 800, lerp_col(hexc("#b8a37a"), hexc("#2a2620"), dark))
    _stroke(c, [(1750, 760), (1750, 120)], 10, hexc("#d8d6d0"), 1.0)   # เสาธง
    g.poly([(1755, 130), (1880, 160), (1755, 200)], hexc("#c84a3a"), 0, amp=0)


def set_classroom(g, dark=0.0):
    c = g.c
    fill_rect(c, -800, -800, W + 1600, H + 1600, lerp_col(hexc("#c9b48a"), hexc("#2a241c"), dark))
    _rr(c, 380, 150, 1160, 480, 8)   # กระดานดำ
    _shade(c, lerp_col(hexc("#2f4a3a"), hexc("#141c18"), dark), 6, 0.2)
    fill_rect(c, 380, 630, 1160, 20, WOOD2)
    fill_rect(c, -800, 820, W + 1600, 800, lerp_col(PLANK, hexc("#2a1f18"), dark))
    for k in range(4):   # โต๊ะเรียน
        _rr(c, 120 + k * 450, 760, 320, 40, 6)
        _shade(c, WOOD3, 3, 0.2)
        fill_rect(c, 140 + k * 450, 800, 18, 140, WOOD2)
        fill_rect(c, 400 + k * 450, 800, 18, 140, WOOD2)


def set_pond_night(g):
    c = g.c
    fill_rect(c, -800, -800, W + 1600, H + 1600, hexc("#0f1a22"))
    for k in range(9):   # ต้นไม้ดำ ๆ หลังสระ
        g.blob(-200 + k * 300, 380, 200, 220, hexc("#14221c"), 0, k)
    fill_rect(c, -800, 520, W + 1600, 900, POND)
    for k in range(14):   # ใบบัว + ดอกบัว
        x = -100 + (hn(k, 7) * 0.5 + 0.5) * 2200
        y = 600 + (hn(k, 8) * 0.5 + 0.5) * 300
        g.blob(x, y, 70, 22, LEAF, 2, k)
        if k % 3 == 0:
            g.poly([(x - 18, y - 10), (x, y - 50), (x + 18, y - 10)], LOTUS, 2, amp=0)
    fill_rect(c, -800, 980, W + 1600, 400, hexc("#2a3a2a"))   # ฝั่งหญ้า


def set_phian_house(g):
    c = g.c
    fill_rect(c, -800, -800, W + 1600, H + 1600, hexc("#cdb895"))
    for k in range(30):
        _stroke(c, [(-800 + k * 110, -800), (-800 + k * 110, 900)], 4, hexc("#a8906a"), 0.5)
    _rr(c, 1250, 160, 420, 360, 6)   # หน้าต่างเห็นสระบัว
    _shade(c, hexc("#9ab8b0"), 6, 0.1)
    g.blob(1460, 430, 180, 40, LEAF, 0, 3)
    fill_rect(c, -800, 860, W + 1600, 800, hexc("#7a5a3c"))
    _rr(c, 200, 700, 700, 160, 20)   # แคร่ไม้
    _shade(c, WOOD3, 3, 0.25)


def robe(g, x, y, sc, look=TON):
    """ทับชุดเป็นจีวรเณร: ผ้าห่มเฉียงพาดไหล่ซ้าย เปิดไหล่ขวา (วาดหลัง person ด้วย x,y,sc เดียวกัน)"""
    c = g.c
    s = sc * look.height
    with g.at(x, y, s):
        g.poly([(-125, -735), (-40, -750), (110, -560), (130, -420), (150, -30), (-150, -30), (-140, -420)],
               look.suit, 3, amp=0)
        _stroke(c, [(-40, -748), (120, -540)], 10, hexc("#b85c12"), 0.9)   # ขอบผ้าพาด
        for k in range(4):
            _stroke(c, [(-100 + k * 60, -400), (-110 + k * 65, -60)], 3, hexc("#b85c12"), 0.45)


TON.hair_col = hexc("#9a6a48")   # หัวโกนเกรียน (สีผิวเข้มกว่าเล็กน้อย)
SOMJAI_YOUNG = Look(hair="long", hair_col=hexc("#1a1512"), skin=hexc("#d4a07a"), outfit="tee", suit=hexc("#c9b6d6"),
                    pants=hexc("#4a4458"), age=0.1, w=54, build=0.85, jaw=0.2, height=0.94)
GREY = lambda v: (v, v, v, 1.0)   # noqa: E731
MUN_YOUNG_BW = Look(hair="part", hair_col=GREY(0.15), skin=GREY(0.72), outfit="tee", suit=GREY(0.88), pants=GREY(0.35),
                    w=58, age=0.1, jaw=0.4)
PETE_BW = Look(hair="part", hair_col=GREY(0.12), skin=GREY(0.68), outfit="tee", suit=GREY(0.5), pants=GREY(0.3),
               glasses="thin", w=58, age=0.15, jaw=0.35, build=0.86)


def beam(g, x, y, ang, length, spread=12, k=0.3):
    """ลำแสงไฟฉาย: จาก (x,y) ทำมุม ang องศา (0 = ขวา, บวก = ลง) กว้าง spread องศา"""
    c = g.c
    a0, a1 = math.radians(ang - spread), math.radians(ang + spread)
    pat = cairo.RadialGradient(x, y, 0, x, y, length)
    pat.add_color_stop_rgba(0, 1.0, 0.96, 0.8, k)
    pat.add_color_stop_rgba(1, 1.0, 0.96, 0.8, 0.0)
    c.save()
    c.move_to(x, y)
    c.line_to(x + length * math.cos(a0), y + length * math.sin(a0))
    c.line_to(x + length * math.cos(a1), y + length * math.sin(a1))
    c.close_path()
    c.set_source(pat)
    c.fill()
    c.restore()


def flick(t, seed=0, rate=2.0):
    """ค่า 0..1 กะพริบแบบสุ่มนิ่ง (ไฟติด ๆ ดับ ๆ)"""
    return 0.5 + 0.5 * hn(int(t * rate * 6), seed)
