"""ตัวละคร/พร็อพ/ฉากของตอน funeral_photo — การ์ตูน 2D แบนเรียบ เส้นนุ่ม ฉากหลังเบลอ (สไตล์คลิปเล่าเรื่องผี)"""
import math
import os
import sys

import cairo
import numpy as np
from PIL import Image, ImageFilter

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))
from gfx import INK, WHITE, H, W, Draw, hexc, hn, lerp, seg, e_io, e_out  # noqa: E402
from people import Look, _rr, _shade, _smooth_path, _stroke, head, person  # noqa: E402

# ---------------------------------------------------------------- palette (หม่น อุ่น)
BG = hexc("#14171a")
NIGHT = hexc("#1b2530")
NIGHT2 = hexc("#2a3644")
WOOD = hexc("#7a5638")
WOOD2 = hexc("#5c3f29")
WOOD3 = hexc("#9a7350")
PLANK = hexc("#8a6646")
CREAM = hexc("#e9dfc8")
CREAM2 = hexc("#cfc3a6")
WALL = hexc("#b9a98a")
WALLN = hexc("#5d5a52")
LAMP = hexc("#f2d38a")
SCREEN = hexc("#a9d6e6")
SCREEN2 = hexc("#dcefff")
ORANGE = hexc("#e8762c")
TEMPLE_RED = hexc("#a8452f")
GOLD = hexc("#d9a63a")
GREEN = hexc("#5f8a5a")
HOSP = hexc("#cfe0e2")
SKY_DAY = hexc("#a9c9d8")
SKY_DUSK = hexc("#e9a77a")
GREY_PHOTO = hexc("#9b9b96")

# ---------------------------------------------------------------- looks
PETE = Look(hair="part", hair_col=hexc("#1c1814"), skin=hexc("#d39a6c"), outfit="hoodie", suit=hexc("#8d9298"),
            pants=hexc("#3b4250"), shoes=hexc("#2a2a2a"), glasses="thin", stubble=0.35, w=58, age=0.15, jaw=0.35, build=0.86)
MUN = Look(hair="bald", hair_col=hexc("#e8e6e0"), skin=hexc("#b88259"), outfit="tee", suit=hexc("#eeeae0"),
           pants=hexc("#6b4f39"), glasses="round", age=1.0, w=60, brow=1.4, jowls=0.3, build=0.95, height=0.92)
MOTHER = Look(hair="short", hair_col=hexc("#6d6a66"), skin=hexc("#d6a07a"), outfit="tee", suit=hexc("#a9c4d8"),
              pants=hexc("#a9c4d8"), age=0.6, w=54, build=0.85, jaw=0.2)
FON = Look(hair="long", hair_col=hexc("#1a1512"), skin=hexc("#dca880"), outfit="tee", suit=hexc("#26262b"),
           pants=hexc("#26262b"), w=52, build=0.8, jaw=0.1, age=0.05, height=0.95)
KENG = Look(hair="crew", hair_col=hexc("#17130f"), skin=hexc("#c48a5e"), outfit="tee", suit=hexc("#f2f2ee"),
            pants=hexc("#40454d"), w=54, jaw=0.25, age=0.05)
KILLER = Look(hair="buzz", hair_col=hexc("#1a1714"), skin=hexc("#a8714a"), outfit="tee", suit=hexc("#2b2f36"),
              pants=hexc("#2b2f36"), w=66, jaw=0.95, build=1.35, brow=1.4, age=0.5, stubble=0.6)
GRANDMA_BW = Look(hair="bun", hair_col=hexc("#5a5a58"), skin=hexc("#c9c9c4"), outfit="tee", suit=hexc("#e4e4e0"),
                  age=0.9, w=54, jaw=0.2, build=0.85)
POLICE = Look(hair="crew", hair_col=hexc("#1a1714"), skin=hexc("#d4a07a"), outfit="tee", suit=hexc("#7a5a3a"),
              pants=hexc("#5a4a38"), w=56)


# ---------------------------------------------------------------- basics
def fill_rect(c, x, y, w, h, col):
    c.rectangle(x, y, w, h)
    c.set_source_rgba(*col)
    c.fill()


def glow(g, x, y, r, col, a=0.5):
    c = g.c
    rg = cairo.RadialGradient(x, y, 0, x, y, r)
    rg.add_color_stop_rgba(0, col[0], col[1], col[2], a)
    rg.add_color_stop_rgba(1, col[0], col[1], col[2], 0)
    c.set_source(rg)
    c.arc(x, y, r, 0, 2 * math.pi)
    c.fill()


def vignette(g, k=0.55):
    c = g.c
    rg = cairo.RadialGradient(W / 2, H / 2, W * 0.32, W / 2, H / 2, W * 0.8)
    rg.add_color_stop_rgba(0, 0, 0, 0, 0)
    rg.add_color_stop_rgba(1, 0.02, 0.02, 0.03, k)
    c.set_source(rg)
    c.rectangle(-1500, -1500, W + 3000, H + 3000)
    c.fill()


def darken(g, a, col=(0.02, 0.025, 0.035)):
    if a > 0:
        fill_rect(g.c, -1500, -1500, W + 3000, H + 3000, (col[0], col[1], col[2], a))


def lerp_col(a, b, k):
    return tuple(lerp(x, y, k) for x, y in zip(a, b))


def smoke(g, x, y, t, n=4, a=0.22, seed=2, rise=50):
    for i in range(n):
        u = ((t * 0.3 + i / n) % 1.0)
        px = x + 30 * math.sin(t * 1.3 + i * 1.7) * u
        py = y - u * rise * 3
        g.blob(px, py, 8 + 30 * u, 8 + 18 * u, (0.85, 0.85, 0.85, a * (1 - u)), 0, seed + i)


# ---------------------------------------------------------------- ฉากหลังเบลอ (depth of field) — แคชต่อโปรเซส
_BG = {}
BLUR_PAD = 360


def blurred(g, key, fn, radius=7):
    """วาดฉากหลังครั้งเดียว (ครึ่งความละเอียด) เบลอ แล้วแคช -> ระบายลงฉากทุกเฟรม"""
    if key not in _BG:
        pad, s = BLUR_PAD, 0.5
        w, h = int((W + 2 * pad) * s), int((H + 2 * pad) * s)
        surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
        c = cairo.Context(surf)
        c.scale(s, s)
        c.translate(pad, pad)
        g2 = Draw(c, 0.0, 0)
        fn(g2)
        surf.flush()
        arr = np.ndarray((h, w, 4), np.uint8, surf.get_data()).copy()
        if radius > 0:
            arr = np.asarray(Image.fromarray(arr, "RGBA").filter(ImageFilter.GaussianBlur(radius * s)))
        arr = np.array(arr, dtype=np.uint8, order='C', copy=True)
        out = cairo.ImageSurface.create_for_data(memoryview(arr), cairo.FORMAT_ARGB32, w, h, w * 4)
        _BG[key] = (out, arr)
        if len(_BG) > 40:   # กันหน่วยความจำบวม
            _BG.pop(next(iter(_BG)))
    surf, _ = _BG[key]
    c = g.c
    c.save()
    c.translate(-BLUR_PAD, -BLUR_PAD)
    c.scale(2, 2)
    c.set_source_surface(surf, 0, 0)
    c.get_source().set_filter(cairo.FILTER_GOOD)
    c.paint()
    c.restore()


# ---------------------------------------------------------------- sets (ฉากหลัง ใช้กับ blurred)
def frame_portrait(g, x, y, w, h, face_seed=0, ribbon=True, col=WOOD2, inner=CREAM2):
    c = g.c
    _rr(c, x - w / 2, y - h / 2, w, h, 4)
    _shade(c, col, 3, 0.2)
    fill_rect(c, x - w / 2 + 10, y - h / 2 + 10, w - 20, h - 20, inner)
    g.blob(x, y - h * 0.08, w * 0.2, h * 0.17, (0.55, 0.55, 0.52, 1), 0, face_seed)
    g.blob(x, y + h * 0.3, w * 0.33, h * 0.18, (0.45, 0.45, 0.43, 1), 0, face_seed + 1)
    if ribbon:
        g.poly([(x - w / 2 + 6, y - h / 2 + 6), (x - w / 2 + 50, y - h / 2 + 6), (x - w / 2 + 6, y - h / 2 + 50)],
               (0.1, 0.1, 0.1, 1), 0, amp=0)


def set_exterior(g, tod="night"):
    """ร้านเจริญศิลป์โฟโต้ ตรงข้ามประตูวัด"""
    c = g.c
    sky = {"night": NIGHT, "day": SKY_DAY, "dusk": SKY_DUSK, "dawn": hexc("#c9b8b0")}[tod]
    fill_rect(c, -800, -800, W + 1600, H + 1600, sky)
    lit = tod == "night"
    # วัดด้านซ้ายไกล ๆ
    g.poly([(-300, 520), (220, 520), (120, 360), (-200, 360)], TEMPLE_RED if not lit else hexc("#5a2c24"), 3, amp=0)
    g.poly([(-150, 360), (70, 360), (-40, 230)], TEMPLE_RED if not lit else hexc("#5a2c24"), 3, amp=0)
    fill_rect(c, -280, 520, 480, 320, CREAM if not lit else hexc("#5a5a55"))
    _stroke(c, [(-40, 230), (-40, 180)], 6, GOLD, 1.0)
    # ร้าน
    x0 = 520
    _rr(c, x0, 260, 900, 600, 6)
    _shade(c, WOOD if not lit else hexc("#4a3628"), 4, 0.2, horiz=False)
    for k in range(18):
        _stroke(c, [(x0 + 25 + k * 50, 270), (x0 + 25 + k * 50, 850)], 3, WOOD2, 0.5)
    g.poly([(x0 - 60, 270), (x0 + 960, 270), (x0 + 820, 150), (x0 + 80, 150)], WOOD2 if not lit else hexc("#3a2a1f"), 3, amp=0)
    _rr(c, x0 + 220, 175, 460, 70, 8)
    _shade(c, CREAM, 3, 0.1)
    g.text("เจริญศิลป์โฟโต้", x0 + 450, 210, 46, "kanit", hexc("#7a3a2a"))
    # หน้าต่างชั้นสอง
    for k in range(2):
        wx = x0 + 160 + k * 420
        fill_rect(c, wx, 300, 170, 150, LAMP if (lit and k == 1) else hexc("#2a2622") if lit else hexc("#7d8a8e"))
        _stroke(c, [(wx, 300), (wx + 170, 450)], 6, WOOD3, 1.0)
        _stroke(c, [(wx + 170, 300), (wx, 450)], 6, WOOD3, 1.0)
        if lit and k == 1:
            glow(g, wx + 85, 375, 260, LAMP, 0.35)
    # หน้าร้าน: ตู้กระจกรูปหน้าศพ + ประตูบานพับ
    fill_rect(c, x0 + 60, 560, 380, 220, hexc("#2b2f33") if lit else hexc("#6b7a80"))
    for k in range(4):
        frame_portrait(g, x0 + 110 + k * 92, 660, 70, 90, k)
    for k in range(6):
        fill_rect(c, x0 + 520 + k * 52, 520, 46, 330, WOOD3 if not lit else hexc("#5c4634"))
    # ถนน + เสาไฟ
    fill_rect(c, -800, 850, W + 1600, 800, hexc("#3a3d40") if lit else hexc("#8a8a84"))
    fill_rect(c, -800, 850, W + 1600, 30, hexc("#55585a") if lit else hexc("#a5a49c"))
    _stroke(c, [(1620, 880), (1620, 300), (1560, 280)], 10, hexc("#2a2c2e"), 1.0)
    if lit:
        glow(g, 1560, 300, 420, LAMP, 0.28)
    # ต้นไม้ขวา
    g.blob(1780, 380, 200, 230, GREEN if not lit else hexc("#24382a"), 3, 4)
    fill_rect(c, 1765, 560, 30, 300, WOOD2)


def set_city(g):
    c = g.c
    fill_rect(c, -800, -800, W + 1600, H + 1600, hexc("#b8c4cc"))
    for k in range(7):
        x = -200 + k * 330
        hh = 380 + 160 * (k % 3)
        _rr(c, x, 820 - hh, 280, hh + 100, 4)
        _shade(c, hexc("#8d9aa4"), 3, 0.15)
        for r in range(int(hh / 90)):
            for q in range(3):
                fill_rect(c, x + 30 + q * 80, 840 - hh + r * 90, 50, 50, hexc("#c9d6de"))
    fill_rect(c, -800, 860, W + 1600, 800, hexc("#9a9a94"))
    _rr(c, 760, 380, 520, 480, 6)   # ประตูกระจกออฟฟิศ
    _shade(c, hexc("#c9dfe6"), 4, 0.1)
    _rr(c, 900, 560, 240, 70, 6)
    _shade(c, hexc("#c84a3a"), 3, 0.1)
    g.text("ปิดกิจการ", 1020, 595, 40, "kanit", WHITE)


def set_hospital(g):
    c = g.c
    fill_rect(c, -800, -800, W + 1600, H + 1600, HOSP)
    fill_rect(c, -800, 820, W + 1600, 800, hexc("#b9c8c6"))
    for k in range(3):   # ม่านกั้นเตียง
        _rr(c, -200 + k * 820, 120, 260, 700, 10)
        _shade(c, hexc("#9dbfc6"), 3, 0.2, horiz=False)
    _rr(c, 1350, 160, 380, 260, 8)   # หน้าต่าง
    _shade(c, hexc("#e9f3f5"), 4, 0.1)
    fill_rect(c, -800, 60, W + 1600, 30, hexc("#e9f3f5"))


def set_shop(g, tod="day"):
    """ชั้นล่างของร้าน: ผนังรูปหน้าศพ ตู้กระจก ฉากถ่ายรูป กล้องโบราณ"""
    c = g.c
    night = tod == "night"
    fill_rect(c, -800, -800, W + 1600, H + 1600, WALL if not night else WALLN)
    for k in range(5):
        for r in range(2):
            frame_portrait(g, 160 + k * 170, 180 + r * 200, 120, 160, k + r * 5)
    _rr(c, 1160, 120, 520, 620, 10)   # ฉากผ้าถ่ายรูป
    _shade(c, hexc("#7f8b96") if not night else hexc("#454b52"), 4, 0.25, horiz=False)
    fill_rect(c, -800, 820, W + 1600, 800, PLANK if not night else hexc("#4a3a2c"))
    for k in range(30):
        _stroke(c, [(-800 + k * 120, 820), (-800 + k * 120 - 60, 1700)], 3, WOOD2, 0.4)
    _rr(c, 120, 600, 900, 240, 8)   # ตู้กระจกเคาน์เตอร์
    _shade(c, WOOD2, 4, 0.2)
    fill_rect(c, 140, 620, 860, 120, hexc("#c9dce0") if not night else hexc("#3a4448"))
    for k in range(5):
        frame_portrait(g, 220 + k * 170, 680, 90, 100, k + 11)
    if not night:
        glow(g, 1500, 200, 700, LAMP, 0.25)


def set_workroom(g, tod="night"):
    """ห้องทำงานชั้นสอง: ผนังไม้ รูปเก่าเต็มผนัง หน้าต่าง ช่องบันได"""
    c = g.c
    night = tod != "day"
    base = hexc("#6b5440") if not night else hexc("#3b3028")
    fill_rect(c, -800, -800, W + 1600, H + 1600, base)
    for k in range(40):
        _stroke(c, [(-800 + k * 90, -800), (-800 + k * 90, 900)], 3, WOOD2, 0.35)
    for k in range(6):   # รูปเก่าเต็มผนัง
        for r in range(2):
            frame_portrait(g, 120 + k * 190 + 40 * (r % 2), 170 + r * 230, 130, 170, k * 3 + r, ribbon=False,
                           inner=hexc("#d8ceb4") if not night else hexc("#8a826e"))
    wx, wy = 1300, 120   # หน้าต่าง
    sky = {"night": hexc("#121c28"), "dawn": hexc("#e9c3a8"), "dusk": hexc("#d98a5a"), "day": SKY_DAY}[tod]
    fill_rect(c, wx, wy, 420, 360, sky)
    if tod in ("dawn", "dusk", "day"):
        g.poly([(wx + 40, wy + 360), (wx + 380, wy + 360), (wx + 300, wy + 220), (wx + 120, wy + 220)], TEMPLE_RED, 0, amp=0)
        g.poly([(wx + 150, wy + 220), (wx + 270, wy + 220), (wx + 210, wy + 130)], TEMPLE_RED, 0, amp=0)
    _stroke(c, [(wx + 210, wy), (wx + 210, wy + 360)], 10, WOOD3, 1.0)
    _stroke(c, [(wx, wy + 180), (wx + 420, wy + 180)], 10, WOOD3, 1.0)
    _rr(c, wx - 14, wy - 14, 448, 388, 6)
    c.set_source_rgba(*WOOD3)
    c.set_line_width(14)
    c.stroke()
    fill_rect(c, -800, 880, W + 1600, 800, hexc("#5a4434") if night else PLANK)
    # ช่องบันได (มืด) ด้านขวา
    g.poly([(1500, 880), (1900, 880), (2000, 1100), (1420, 1100)], (0.03, 0.03, 0.03, 1), 0, amp=0)
    _stroke(c, [(1500, 880), (1500, 520)], 8, WOOD3, 1.0)
    _stroke(c, [(1500, 600), (1900, 600)], 8, WOOD3, 1.0)


def set_temple_sala(g):
    c = g.c
    fill_rect(c, -800, -800, W + 1600, H + 1600, hexc("#d8cdb8"))
    for k in range(6):
        _rr(c, -200 + k * 440, 0, 60, 900, 4)
        _shade(c, CREAM, 3, 0.2, horiz=False)
    fill_rect(c, -800, 860, W + 1600, 800, hexc("#b39a7a"))
    _rr(c, 760, 420, 400, 440, 10)   # โต๊ะหมู่ + พวงดอกไม้
    _shade(c, GOLD, 3, 0.2)
    for k in range(9):
        g.blob(620 + k * 85, 860, 50, 60, WHITE, 0, k)
    _rr(c, 860, 230, 200, 250, 6)
    _shade(c, hexc("#2a2a2a"), 3, 0.1)


def set_road_night(g):
    c = g.c
    fill_rect(c, -800, -800, W + 1600, H + 1600, hexc("#141a22"))
    fill_rect(c, -800, 760, W + 1600, 900, hexc("#2a2c30"))
    for k in range(10):
        fill_rect(c, -600 + k * 330, 900, 160, 18, hexc("#c9b46a"))
    _stroke(c, [(1500, 780), (1500, 220), (1420, 200)], 12, hexc("#3a3c40"), 1.0)
    glow(g, 1420, 220, 600, LAMP, 0.35)
    for k in range(6):
        g.blob(-100 + k * 400, 640, 180, 160, hexc("#1c2a22"), 0, k)


def set_station(g):
    c = g.c
    fill_rect(c, -800, -800, W + 1600, H + 1600, hexc("#20262c"))
    fill_rect(c, -800, 820, W + 1600, 800, hexc("#2c3036"))
    _rr(c, 300, 300, 900, 520, 10)   # รถกระบะกู้ภัย
    _shade(c, hexc("#c9c4ba"), 4, 0.2)
    _rr(c, 500, 200, 300, 120, 10)
    _shade(c, ORANGE, 3, 0.1)
    glow(g, 650, 200, 300, ORANGE, 0.4)
    for k in range(2):
        g.circle(450 + k * 600, 820, 90, hexc("#1a1a1a"), 4)


# ---------------------------------------------------------------- foreground props (คมชัด)
def desk(g, x, y, w=1100, h=200, col=WOOD):
    c = g.c
    _rr(c, x - w / 2, y, w, 36, 6)
    _shade(c, col, 3, 0.2)
    fill_rect(c, x - w / 2 + 20, y + 36, w - 40, h, WOOD2)


def incense(g, x, y, t, lit=True, burn=0.0, sc=1.0):
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -36, -40, 72, 40, 10)
        _shade(c, hexc("#b59a5a"), 3, 0.25)
        top = -40 - 140 * (1 - burn)
        _stroke(c, [(0, -40), (0, top)], 5, hexc("#9a3a2a"), 1.0)
        if lit:
            glow(g, 0, top, 14, (1, 0.55, 0.25, 1), 0.9)
            smoke(g, 0, top - 6, t, 4, 0.25, 3, 40)


def crt(g, x, y, sc=1.0, screen=None, on=True):
    """คอมพิวเตอร์จอตู้สีครีม (x,y = กลางฐาน); screen(g) วาดเนื้อหาจอในกรอบ -230..230 x -360..-40"""
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -300, -440, 600, 420, 30)
        _shade(c, hexc("#ddd4bd"), 3.5, 0.25)
        _rr(c, -250, -390, 500, 330, 24)
        _shade(c, hexc("#2b2e30"), 3, 0.1)
        if on:
            fill_rect(c, -230, -370, 460, 290, SCREEN)
            if screen:
                c.save()
                c.rectangle(-230, -370, 460, 290)
                c.clip()
                screen(g)
                c.restore()
            glow(g, 0, -225, 360, SCREEN2, 0.18)
        _rr(c, -120, -20, 240, 30, 8)
        _shade(c, hexc("#cfc6ae"), 3, 0.2)
        g.circle(230, -50, 8, hexc("#7ad07a") if on else hexc("#555555"), 0)


def editor_ui(g, img_fn, zoom_label=None):
    """หน้าต่างโปรแกรมแต่งรูปแบบเก่าในจอ (พิกัดจอ -230..230, -370..-80)"""
    c = g.c
    fill_rect(c, -230, -370, 460, 22, hexc("#3a5a8a"))
    fill_rect(c, -230, -348, 40, 268, hexc("#c9c9c4"))
    for k in range(6):
        fill_rect(c, -224, -340 + k * 34, 28, 26, hexc("#a9a9a4"))
    fill_rect(c, -190, -348, 420, 268, hexc("#6b6b68"))
    c.save()
    c.rectangle(-180, -340, 400, 250)
    c.clip()
    img_fn(g)
    c.restore()
    if zoom_label:
        fill_rect(c, 120, -100, 100, 20, hexc("#e9e9e4"))
        g.text(zoom_label, 170, -90, 16, "kanit", INK)


def speakers(g, x, y, sc=1.0, plug_dangle=True):
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -40, -150, 80, 150, 10)
        _shade(c, hexc("#ddd4bd"), 3, 0.25)
        g.circle(0, -95, 22, hexc("#4a4a48"), 2)
        g.circle(0, -35, 12, hexc("#4a4a48"), 2)
        if plug_dangle:
            _stroke(c, [(30, -10), (70, 40), (60, 180), (80, 260)], 5, hexc("#2a2a2a"), 1.0)
            _rr(c, 66, 250, 30, 40, 4)
            _shade(c, hexc("#e0e0dc"), 2, 0.1)
            for k in (-6, 6):
                _stroke(c, [(81 + k, 290), (81 + k, 310)], 4, hexc("#c9b46a"), 1.0)


def wall_clock(g, x, y, r, hh, mm):
    c = g.c
    g.circle(x, y, r, CREAM, 4)
    for k in range(12):
        a = k * math.pi / 6
        _stroke(c, [(x + math.cos(a) * r * 0.82, y + math.sin(a) * r * 0.82), (x + math.cos(a) * r * 0.92, y + math.sin(a) * r * 0.92)], 3, INK, 1.0)
    am = math.radians(mm * 6 - 90)
    ah = math.radians((hh % 12 + mm / 60) * 30 - 90)
    hand = hexc("#2a2622")
    _stroke(c, [(x, y), (x + math.cos(am) * r * 0.75, y + math.sin(am) * r * 0.75)], max(6, r * 0.04), hand, 1.0)
    _stroke(c, [(x, y), (x + math.cos(ah) * r * 0.5, y + math.sin(ah) * r * 0.5)], max(9, r * 0.06), hand, 1.0)
    g.circle(x, y, max(8, r * 0.05), hand, 0)


def camera_antique(g, x, y, sc=1.0, flash=0.0):
    """กล้องไม้แบบมีเบลโลว์บนขาตั้ง (x,y = ปลายขาตั้งที่พื้น)"""
    c = g.c
    with g.at(x, y, sc):
        for dx in (-120, 0, 120):
            _stroke(c, [(0, -520), (dx, 0)], 12, WOOD2, 1.0)
        _rr(c, -120, -680, 160, 170, 8)
        _shade(c, WOOD3, 3, 0.25)
        g.poly([(40, -660), (170, -640), (170, -550), (40, -530)], hexc("#2a2420"), 3, amp=0)
        _rr(c, 160, -640, 60, 80, 6)
        _shade(c, WOOD3, 3, 0.25)
        g.circle(225, -600, 26, hexc("#3a3a38"), 3)
        _stroke(c, [(-60, -680), (-60, -760)], 6, hexc("#6a6a66"), 1.0)   # ถาดแฟลช
        _rr(c, -110, -780, 100, 22, 4)
        _shade(c, hexc("#8a8a84"), 2, 0.1)
        if flash > 0:
            glow(g, -60, -790, 900 * flash, (1, 1, 0.95, 1), 0.95 * flash)


def envelope(g, x, y, sc=1.0, rot=0, open_=False):
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -160, -100, 320, 200, 6)
        _shade(c, hexc("#b8925e"), 3, 0.2)
        if open_:
            g.poly([(-160, -100), (160, -100), (0, -220)], hexc("#a68250"), 2, amp=0)
        else:
            _stroke(c, [(-160, -100), (0, 10), (160, -100)], 3, hexc("#7a5a30"), 0.8)


def banknote(g, x, y, sc=1.0, rot=0, wet=True):
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -110, -50, 220, 100, 6)
        _shade(c, hexc("#a9906a") if wet else hexc("#c9b48a"), 2.5, 0.2)
        g.text("1000", 60, -24, 22, "kanit", hexc("#5a4a2a"))
        g.circle(-50, 0, 28, hexc("#8a7652"), 0)
        if wet:
            for k in range(3):
                g.blob(-60 + k * 50, 30, 18, 10, (0.4, 0.45, 0.5, 0.3), 0, k)


def id_card(g, x, y, sc, t, look=None, bruise=1.0):
    """รูปใบขับขี่เก่าของเก่ง"""
    c = g.c
    look = look or KENG
    with g.at(x, y, sc):
        _rr(c, -260, -160, 520, 320, 18)
        _shade(c, hexc("#d9e2d6"), 3, 0.15)
        fill_rect(c, -260, -160, 520, 46, hexc("#5a7a9a"))
        g.text("ใบอนุญาตขับขี่", 0, -136, 26, "kanit", WHITE)
        fill_rect(c, -230, -100, 170, 220, hexc("#c9d6e0"))
        c.save()
        c.rectangle(-230, -100, 170, 220)
        c.clip()
        with g.at(-145, 20, 1.1):
            head(g, look, "neutral", 0.0, 0.0, (0, 0), 3)
            if bruise > 0:
                g.blob(-24, -2, 18, 12, (0.45, 0.3, 0.5, 0.6 * bruise), 0, 3)
        c.restore()
        g.text("นายเก่ง", 90, -60, 34, "kanit", INK)
        for k in range(4):
            _stroke(c, [(-20, -10 + k * 34), (220, -10 + k * 34)], 6, hexc("#9aa6a0"), 1.0)


def phone(g, x, y, sc, rot=0, screen=None, hand=True, skin=None):
    c = g.c
    with g.at(x, y, sc, rot):
        if hand:
            g.blob(0, 140, 150, 110, skin or PETE.skin, 3, 2)
        _rr(c, -110, -220, 220, 440, 28)
        _shade(c, hexc("#1d1f22"), 3, 0.1)
        fill_rect(c, -96, -196, 192, 392, hexc("#f2f2f0"))
        if screen:
            c.save()
            c.rectangle(-96, -196, 192, 392)
            c.clip()
            screen(g)
            c.restore()
        if hand:
            for k in range(3):
                _rr(c, 90, -40 + k * 50, 60, 40, 18)
                _shade(c, skin or PETE.skin, 3, 0.2)


def vest(g, x, y, sc, look=KILLER):
    """เสื้อกั๊กกู้ภัยสีส้มทับบนตัว (เรียกหลัง person ด้วย x,y,sc เดียวกัน) — ไม่มีโลโก้"""
    c = g.c
    with g.at(x, y, sc * look.height):
        bw = look.build
        g.poly([(-118 * bw, -722), (-58, -745), (-28, -560), (28, -560), (58, -745), (118 * bw, -722),
                (112 * bw, -440), (-112 * bw, -440)], ORANGE, 3, amp=0)
        for yy in (-640, -520):
            fill_rect(c, -112 * bw, yy, 224 * bw, 18, hexc("#2a2a2a"))
            fill_rect(c, -112 * bw, yy + 5, 224 * bw, 6, hexc("#e9e9e0"))


def pipe(g, x, y, sc=1.0, rot=0):
    with g.at(x, y, sc, rot):
        _rr(g.c, -10, -300, 20, 320, 8)
        _shade(g.c, hexc("#7a7f84"), 3, 0.3)


def knife(g, x, y, sc=1.0, rot=0):
    with g.at(x, y, sc, rot):
        _rr(g.c, -14, -10, 28, 90, 8)
        _shade(g.c, hexc("#2a2a2a"), 3, 0.1)
        g.poly([(-14, -10), (14, -10), (6, -210), (-14, -150)], hexc("#d9dee2"), 3, amp=0)


def crowbar(g, x, y, sc=1.0, rot=0):
    with g.at(x, y, sc, rot):
        _stroke(g.c, [(0, 0), (0, -420), (30, -460), (60, -450)], 18, hexc("#8a2a2a"), 1.0)


def usb(g, x, y, sc=1.0, rot=0):
    with g.at(x, y, sc, rot):
        _rr(g.c, -30, -60, 60, 100, 10)
        _shade(g.c, hexc("#3a6ab0"), 3, 0.2)
        fill_rect(g.c, -18, -86, 36, 30, hexc("#c9c9c4"))


def big_eye(g, x, y, sc, pupil=(0.0, 0.0), bw=True, iris_fn=None, glow_k=0.0):
    """ดวงตาภาพใหญ่ (ในจอ) — pupil = การเลื่อนรูม่านตา (-1..1)"""
    c = g.c
    with g.at(x, y, sc):
        white = hexc("#e6e6e2") if bw else hexc("#f2ece4")
        skin = hexc("#bdbdb8") if bw else KENG.skin
        fill_rect(c, -600, -400, 1200, 800, skin)
        _smooth_path(c, [(-320, 0), (-150, -150), (150, -160), (330, -10), (150, 130), (-160, 130)])
        _shade(c, white, 4, 0.15)
        c.save()
        _smooth_path(c, [(-320, 0), (-150, -150), (150, -160), (330, -10), (150, 130), (-160, 130)])
        c.clip()
        ix, iy = pupil[0] * 140, pupil[1] * 50
        g.circle(ix, iy, 120, hexc("#5a5a58") if bw else hexc("#4a3424"), 0)
        if iris_fn:
            c.save()
            c.arc(ix, iy, 112, 0, 2 * math.pi)
            c.clip()
            iris_fn(g, ix, iy)
            c.restore()
        g.circle(ix, iy, 52, hexc("#141414"), 0)
        g.circle(ix - 40, iy - 45, 18, (1, 1, 1, 0.8), 0)
        if glow_k > 0:
            glow(g, ix, iy, 180, (0.85, 0.95, 1.0, 1), 0.4 * glow_k)
        c.restore()
        _stroke(c, [(-330, -10), (-150, -170), (150, -180), (340, -20)], 10, hexc("#3a3a38"), 1.0)
        for k in range(7):
            xx = -220 + k * 70
            _stroke(c, [(xx, -165 + abs(k - 3) * 6), (xx - 10, -215 + abs(k - 3) * 6)], 5, hexc("#3a3a38"), 1.0)


def grandma_photo(g, x, y, sc, t, restore=1.0, damage=True, smile=False):
    """รูปขาวดำคุณยายผิน: restore 0..1 = ส่วนที่ซ่อมแล้ว (จากซ้ายไปขวา)"""
    c = g.c
    with g.at(x, y, sc):
        fill_rect(c, -200, -260, 400, 520, hexc("#d8d6cf"))
        c.save()
        c.rectangle(-200, -260, 400, 520)
        c.clip()
        fill_rect(c, -200, -260, 400, 520, hexc("#b9b8b1"))
        g.blob(0, 230, 190, 120, GRANDMA_BW.suit, 3, 2)   # ไหล่ เสื้อลูกไม้
        with g.at(0, -30, 2.3):
            head(g, GRANDMA_BW, "smile" if smile else "neutral", 0.0, 0.0, (0, 0), 5)
        if damage and restore < 1:
            c.save()
            c.rectangle(-200 + 400 * restore, -260, 400, 520)
            c.clip()
            for k in range(9):
                g.blob(-80 + 40 * hn(k, 2) * 2 + 60, -90 + 50 * hn(k, 3) * 2, 70 + 30 * abs(hn(k, 4)), 60 + 30 * abs(hn(k, 5)),
                       (0.85, 0.84, 0.8, 0.85), 0, k)
            c.restore()
        c.restore()


def keng_face(g, x, y, sc, t, bruise=1.0, mood="neutral"):
    with g.at(x, y, sc):
        fill_rect(g.c, -260, -320, 520, 640, hexc("#c9d6e0"))
        with g.at(0, 30, 2.2):
            head(g, KENG, mood, 0.0, 0.0, (0, 0), 3)
            if bruise > 0:
                g.blob(-24, -4, 22, 14, (0.45, 0.3, 0.55, 0.65 * bruise), 0, 3)
                g.blob(8, 34, 10, 4, (0.6, 0.2, 0.2, 0.6 * bruise), 0, 4)


def killer_reflection(g, cx, cy, sc=1.0, raise_k=1.0):
    """ภาพเล็ก ๆ ในกระจกตา: ชายเสื้อกั๊กส้มเงื้อท่อนเหล็ก ใต้เสาไฟ (ไม่แสดงการฟาด)"""
    c = g.c
    with g.at(cx, cy, sc):
        fill_rect(c, -200, -200, 400, 400, hexc("#1a2028"))
        glow(g, 80, -80, 160, LAMP, 0.6)
        person(g, -10, 110, KILLER, 0.24, mood="angry", pose="down", pose2="v", k=raise_k, turn=-0.2, seed=6,
               shadow=False)
        vest(g, -10, 110, 0.24)
        pipe(g, 20, lerp(40, -130, raise_k), 0.4, 20)


# ================================================================ หัวสไตล์การ์ตูนแบนเรียบ (ทรงไข่ คอยาว หน้าเรียบง่าย)
import people as _people  # noqa: E402


def _darker(col, k=0.78):
    return (col[0] * k, col[1] * k, col[2] * k, col[3] if len(col) > 3 else 1.0)


def _egg(c, w, top=-92, chin=74, fx=0.0):
    """หน้ากลม แก้มอิ่ม คางมน"""
    pts = [(0, top), (w * 0.74, top + 12), (w * 1.04, -34), (w * 1.06, 8), (w * 0.9, 46),
           (w * 0.55, 70), (fx * 0.4 + w * 0.2, chin + 2), (fx * 0.4, chin + 4)]
    full = pts + [(-x + fx * 0.8 if y > 20 else -x, y) for x, y in reversed(pts[1:-1])]
    _smooth_path(c, full)
    return full


def _fill_grad(c, col, dark=0.82):
    x0, y0, x1, y1 = c.fill_extents()
    c.set_source_rgba(*col)
    c.fill_preserve()
    lg = cairo.LinearGradient(x0, y0, x1, y0)
    lg.add_color_stop_rgba(0, 1, 1, 1, 0.06)
    lg.add_color_stop_rgba(0.55, 0, 0, 0, 0)
    lg.add_color_stop_rgba(1, 0.1, 0.05, 0.05, 1 - dark)
    c.set_source(lg)
    c.fill()


def flat_head(g, look, mood="neutral", talk=0.0, turn=0.0, look_at=(0, 0), seed=0, lw=4.5):
    """หัวที่จุดกำเนิด = กลางหน้า (ระดับตา ~ -8) — อินเทอร์เฟซเดียวกับ people.head"""
    c, t, w = g.c, g.t, look.w * 0.98
    fx = turn * w * 0.32
    hair = look.hair_col
    skin = look.skin
    # ผมด้านหลัง
    if look.hair in ("long",):
        _smooth_path(c, [(-w * 1.05, -60), (0, -112), (w * 1.05, -60), (w * 1.12, 120), (w * 0.9, 210), (-w * 0.9, 210), (-w * 1.12, 120)])
        _fill_grad(c, hair, 0.75)
    if look.hair == "bun":
        g.circle(0, -122, w * 0.42, hair, 0)
    # คอ (ยาว เรียว)
    _rr(c, -w * 0.36, 30, w * 0.72, 110, 12)
    _fill_grad(c, _darker(skin, 0.92), 0.8)
    # หู
    for sx in (-1, 1):
        if sx * turn > 0.5:
            continue
        c.save()
        c.translate(sx * w * 0.93 + fx * 0.2, 0)
        c.scale(1, 1.6)
        c.new_path()
        c.arc(0, 0, w * 0.15, 0, 2 * math.pi)
        c.restore()
        _fill_grad(c, _darker(skin, 0.95), 0.85)
    # เงาคางตกบนคอ
    c.save()
    _rr(c, -w * 0.36, 30, w * 0.72, 110, 12)
    c.clip()
    sg = cairo.LinearGradient(0, 70, 0, 120)
    sg.add_color_stop_rgba(0, 0.12, 0.05, 0.04, 0.45)
    sg.add_color_stop_rgba(1, 0.12, 0.05, 0.04, 0.0)
    c.set_source(sg)
    c.paint()
    c.restore()
    # หน้า + แสงเงา (แสงจากซ้ายบน)
    _egg(c, w, fx=fx)
    _fill_grad(c, skin, 0.86)
    c.save()
    _egg(c, w, fx=fx)
    c.clip()
    rg = cairo.RadialGradient(-w * 0.45 + fx * 0.3, -55, w * 0.1, -w * 0.2, -20, w * 1.7)
    rg.add_color_stop_rgba(0, 1, 0.96, 0.88, 0.32)
    rg.add_color_stop_rgba(0.45, 1, 0.95, 0.9, 0.0)
    rg.add_color_stop_rgba(1, 0.18, 0.06, 0.05, 0.42)
    c.set_source(rg)
    c.paint()
    glow(g, w * 0.95 + fx * 0.2, -10, w * 0.5, (1, 0.85, 0.7, 1), 0.12)   # แสงขอบ (rim)
    c.restore()
    # แก้ม + เงาใต้คาง
    for sx in (-1, 1):
        glow(g, sx * w * 0.5 + fx, 30, w * 0.32, (0.88, 0.45, 0.4, 1), 0.18)
    if look.stubble > 0.3:
        c.save()
        _egg(c, w, fx=fx)
        c.clip()
        sg = cairo.LinearGradient(0, 30, 0, 80)
        sg.add_color_stop_rgba(0, 0.15, 0.12, 0.12, 0)
        sg.add_color_stop_rgba(1, 0.15, 0.12, 0.12, 0.18 * look.stubble)
        c.set_source(sg)
        c.paint()
        c.restore()
    # ริ้วรอย (คนแก่: เส้นบาง ๆ ใต้ตา หน้าผาก)
    line = _darker(skin, 0.6)
    if look.age > 0.55:
        for k in range(2):
            _stroke(c, [(-w * 0.32 + fx, -62 + k * 10), (fx, -65 + k * 10), (w * 0.32 + fx, -62 + k * 10)], 2.2, line, 0.6)
        for sx in (-1, 1):
            _stroke(c, [(sx * w * 0.5 + fx, 10), (sx * w * 0.36 + fx, 16), (sx * w * 0.22 + fx, 12)], 2, line, 0.55)
            _stroke(c, [(sx * w * 0.26 + fx, 40), (sx * w * 0.32 + fx, 62)], 2, line, 0.5)
    # ตาโต
    blink = mood not in ("shock", "shout") and ((t * 0.45 + seed * 0.37) % 3.6) < 0.1
    ey = -4
    sad = mood in ("sad", "worry")
    for sx in (-1, 1):
        ex = sx * w * 0.42 + fx
        ew = w * 0.27
        eh = w * (0.25 if mood != "shock" else 0.31) * (0.8 if mood in ("angry", "smug") else 1.0)
        if blink:
            _stroke(c, [(ex - ew, ey), (ex, ey + 6), (ex + ew, ey)], 3.5, hexc("#2a1d16"), 1.0)
            continue
        c.save()
        c.translate(ex, ey)
        c.scale(1, eh / ew)
        c.new_path()
        c.arc(0, 0, ew, 0, 2 * math.pi)
        c.restore()
        c.set_source_rgba(0.99, 0.98, 0.96, 1)
        c.fill_preserve()
        c.save()
        c.clip()
        ix, iy = ex + look_at[0] * ew * 0.3, ey + 2 + look_at[1] * eh * 0.25
        ir = eh * 0.86
        ig = cairo.RadialGradient(ix, iy + ir * 0.4, ir * 0.1, ix, iy, ir)
        bw = abs(skin[0] - skin[2]) < 0.03   # รูปขาวดำ -> ตาเทา
        ig.add_color_stop_rgba(0, *((0.6, 0.6, 0.58) if bw else (0.62, 0.42, 0.26)), 1)
        ig.add_color_stop_rgba(1, *((0.18, 0.18, 0.18) if bw else (0.2, 0.12, 0.08)), 1)
        c.set_source(ig)
        c.arc(ix, iy, ir, 0, 2 * math.pi)
        c.fill()
        g.circle(ix, iy, ir * 0.48, hexc("#0e0906"), 0)
        g.circle(ix - ir * 0.36, iy - ir * 0.38, ir * 0.3, (1, 1, 1, 0.95), 0)
        g.circle(ix + ir * 0.34, iy + ir * 0.3, ir * 0.13, (1, 1, 1, 0.8), 0)
        shade = cairo.LinearGradient(0, ey - eh, 0, ey)   # เงาเปลือกตาบนทับลูกตา
        shade.add_color_stop_rgba(0, 0.2, 0.1, 0.08, 0.35)
        shade.add_color_stop_rgba(1, 0.2, 0.1, 0.08, 0.0)
        c.set_source(shade)
        c.paint()
        c.restore()
        _stroke(c, [(ex - ew * 1.08, ey + 2), (ex - ew * 0.3, ey - eh * 1.05), (ex + ew * 0.5, ey - eh * 1.02), (ex + ew * 1.1, ey - 1)],
                4, hexc("#21160f"), 1.0)
        _stroke(c, [(ex - ew * 0.7, ey + eh * 0.95), (ex + ew * 0.6, ey + eh * 0.92)], 1.8, line, 0.45)
        if sad or look.age > 0.55:
            _stroke(c, [(ex - ew * 0.7, ey + eh * 1.35), (ex + ew * 0.7, ey + eh * 1.35)], 2, line, 0.5)
    # คิ้ว
    tilt = {"angry": -0.32, "shout": -0.32, "firm": -0.15, "sad": 0.3, "worry": 0.3, "shock": 0.0, "smug": -0.1}.get(mood, 0.0)
    by = ey - w * 0.46 - (8 if mood == "shock" else 0)
    for sx in (-1, 1):
        bx = sx * w * 0.42 + fx
        inner = by - tilt * w * 0.25
        outer = by + tilt * w * 0.12
        _stroke(c, [(bx - sx * w * 0.2, inner), (bx + sx * w * 0.22, outer)], 3.5 * look.brow + 1.5, hexc("#2a1d16") if look.hair != "bald" else hexc("#d9d6cf"), 1.0)
    # จมูก (เงาเล็ก ๆ)
    glow(g, fx + w * 0.08, 26, w * 0.12, _darker(skin, 0.6), 0.28)   # จมูก = เงานุ่ม ๆ
    _stroke(c, [(fx - w * 0.06, 34), (fx + w * 0.08, 35)], 2.2, line, 0.55)
    # ปาก
    my = 48
    open_ = 0.0
    if talk:
        open_ = max(0.0, math.sin(t * 15 + seed)) * float(talk) * 0.8
    if mood in ("shock", "shout"):
        open_ = max(open_, 1.0)
    mw = w * (0.18 if mood != "shout" else 0.3)
    if open_ > 0.15:
        c.save()
        c.translate(fx, my)
        c.scale(1, (0.4 + 0.6 * open_))
        c.new_path()
        c.arc(0, 0, mw, 0, 2 * math.pi)
        c.restore()
        c.set_source_rgba(0.35, 0.12, 0.12, 1)
        c.fill()
    else:
        curve = {"smile": 7, "smug": 4, "sad": -6, "worry": -4, "angry": -4, "firm": -1}.get(mood, 1)
        _stroke(c, [(fx - mw, my - curve * 0.4), (fx, my + curve * 0.6), (fx + mw * (1.3 if mood == "smug" else 1), my - curve * (0.8 if mood == "smug" else 0.4))],
                3, hexc("#6a2e26"), 0.9)
    # ผมด้านหน้า
    h = look.hair
    if h == "bald":   # ศีรษะล้าน + ผมขาวเป็นวงรอบข้าง
        for sx in (-1, 1):
            _smooth_path(c, [(sx * w * 0.55, -80), (sx * w * 0.98, -50), (sx * w * 1.0, -10), (sx * w * 0.86, -16), (sx * w * 0.8, -60)])
            _fill_grad(c, hair, 0.85)
        c.save()
        _egg(c, w, fx=fx)
        c.clip()
        glow(g, -w * 0.3, -80, w * 0.5, (1, 1, 1, 1), 0.18)
        c.restore()
    elif h in ("part", "crew", "short", "buzz", "long", "bun"):
        cap = {"part": 0.45, "crew": 0.42, "short": 0.5, "buzz": 0.3, "long": 0.5, "bun": 0.45}[h]
        c.save()
        top = -96
        hairline = top + (96 + 84) * cap * 0.42
        pts = [(-w * 1.0, -20), (-w * 0.98, -60), (-w * 0.6, top - 8), (0, top - 14), (w * 0.6, top - 8), (w * 0.98, -60), (w * 1.0, -20)]
        if h == "part":   # ผมแสกมีปอยหน้าม้า
            pts += [(w * 0.85, -48), (w * 0.4, hairline - 8), (w * 0.1, hairline + 6), (-w * 0.3, hairline - 2), (-w * 0.85, -42)]
        elif h in ("long", "bun"):
            pts += [(w * 0.8, -40), (w * 0.3, hairline - 18), (0, hairline - 28), (-w * 0.3, hairline - 18), (-w * 0.8, -40)]
        elif h == "short":
            pts += [(w * 0.9, -10), (w * 0.7, -50), (w * 0.2, hairline - 6), (-w * 0.5, hairline - 4), (-w * 0.9, -10)]
        else:
            pts += [(w * 0.88, -46), (w * 0.4, hairline - 4), (-w * 0.4, hairline - 4), (-w * 0.88, -46)]
        _smooth_path(c, pts)
        _fill_grad(c, hair, 0.8)
        if h == "buzz":
            _smooth_path(c, pts)
            c.set_source_rgba(*skin[:3], 0.12)
            c.fill()
        for k in range(3):   # ปอยผมไฮไลต์
            _stroke(c, [(-w * 0.4 + k * w * 0.3, top), (-w * 0.3 + k * w * 0.3, top + 20)], 2, (1, 1, 1, 1), 0.12)
        c.restore()
        if h == "long":   # ผมยาวด้านข้างทับหน้า
            for sx in (-1, 1):
                _smooth_path(c, [(sx * w * 0.8, -40), (sx * w * 1.05, -30), (sx * w * 1.0, 120), (sx * w * 0.82, 130), (sx * w * 0.86, 20)])
                _fill_grad(c, hair, 0.8)
    # แว่น
    if look.glasses:
        col = hexc("#2a2622")
        rnd = look.glasses.startswith("round")
        for sx in (-1, 1):
            ex = sx * w * 0.42 + fx
            c.new_path()
            if rnd:
                c.arc(ex, ey, w * 0.34, 0, 2 * math.pi)
            else:
                _rr(c, ex - w * 0.36, ey - w * 0.28, w * 0.72, w * 0.54, 10)
            c.set_source_rgba(0.85, 0.92, 0.95, 0.18)
            c.fill_preserve()
            c.set_source_rgba(*col)
            c.set_line_width(3.2 if not look.glasses.endswith("thin") else 3.0)
            c.stroke()
        _stroke(c, [(fx - w * 0.07, ey - 4), (fx + w * 0.07, ey - 4)], 3, col, 1.0)


_people.head = flat_head
head = flat_head


# ================================================================ แสงเงาทั้งเฟรม (บรรยากาศเสมือนจริง)
def light_pass(g, lx, ly, col=(1.0, 0.86, 0.62), k=0.55, r=1300, dust=True):
    """แสงจากแหล่งเดียวทาบทั้งฉาก+ตัวละคร (soft light) + แสงฟุ้ง (screen) + ฝุ่นลอยในแสง"""
    c = g.c
    big = (-1500, -1500, W + 3000, H + 3000)
    c.save()
    c.set_operator(cairo.OPERATOR_SOFT_LIGHT)
    rg = cairo.RadialGradient(lx, ly, 0, lx, ly, r)
    rg.add_color_stop_rgba(0, col[0], col[1], col[2], k)
    rg.add_color_stop_rgba(0.45, 0.5, 0.5, 0.5, 0.0)
    rg.add_color_stop_rgba(1, 0.02, 0.03, 0.06, k)
    c.set_source(rg)
    c.rectangle(*big)
    c.fill()
    c.set_operator(cairo.OPERATOR_SCREEN)
    rg = cairo.RadialGradient(lx, ly, 0, lx, ly, r * 0.45)
    rg.add_color_stop_rgba(0, col[0], col[1], col[2], 0.22 * k)
    rg.add_color_stop_rgba(1, col[0], col[1], col[2], 0.0)
    c.set_source(rg)
    c.rectangle(*big)
    c.fill()
    c.restore()
    if dust:
        t = g.t
        for i in range(26):
            u = (hn(i, 31) * 0.5 + 0.5)
            v = (hn(i, 32) * 0.5 + 0.5)
            px = lx + (u - 0.5) * r * 0.9 + 30 * math.sin(t * 0.4 + i)
            py = ly + ((v * r * 0.7 + t * 12 * (0.5 + u)) % (r * 0.7)) - r * 0.2
            d = math.hypot(px - lx, py - ly) / (r * 0.5)
            if d < 1:
                g.circle(px, py, 2 + 2.5 * u, (1, 0.95, 0.85, 0.35 * (1 - d)), 0)
