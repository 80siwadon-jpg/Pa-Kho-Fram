"""ตัวละครและพร็อพของตอนกัดดาฟี"""
import math

from gfx import (BROWN, CREAM, GOLD, GOLD2, GREY, INK, KHAKI, LGREY, LYGREEN, NAVY, RED,
                 SAND, SAND2, SKIN, TAN, WHITE, hn)

MEDALS = [RED, GOLD, LYGREEN, NAVY, WHITE, RED, GOLD, LYGREEN]


def curly_hair(g, R, cy, col=INK, messy=0.0, seed=0):
    """ผมดำหยิกฟู: วงกลมเล็ก ๆ เรียงรอบหัว"""
    for i in range(15):
        a = math.radians(160 + i * 15.7)
        rr = R * (1.0 + 0.08 * hn(i, seed) + messy * 0.12 * hn(i, seed + 3))
        g.circle(math.cos(a) * rr, cy + math.sin(a) * rr * 0.95, R * 0.27, col, 5)


def gaddafi(g, x, y, sc=1.0, mood="happy", rot=0, look="leader", shades=True, arm=0.0, seed=201):
    """มูอัมมาร์ กัดดาฟี: ผมดำหยิกฟู แว่นกันแดด
    look: kid (เด็กเบดูอิน), young (ร้อยเอกปี 1969 ชุดกากี), leader (เครื่องแบบขาว เหรียญเต็มอก หมวกทหาร),
          old (ปี 2011 ชุดกากี ผมยุ่ง)"""
    with g.at(x, y, sc, rot):
        if look == "kid":
            g.poly([(-50, -150), (50, -150), (70, 0), (-70, 0)], CREAM, 6, seed=seed)      # เสื้อคลุมยาว
            g.line([(-40, -140), (-70, -90)], 12)
            g.line([(40, -140), (70, -90 - 60 * arm)], 12)
            curly_hair(g, 70, -215, seed=seed)
            g.circle(0, -215, 68, TAN, 6)
            with g.at(0, -212):
                g.face(64, mood, seed=seed)
            return
        coat = {"young": KHAKI, "leader": CREAM, "old": KHAKI}[look]
        for sx in (-1, 1):
            g.rrect(sx * 22 - 13, -70, 26, 70, 8, coat, 6)
            g.blob(sx * 26, -6, 26, 12, INK, 0, seed + sx)
        g.line([(70, -175), (96 + 22 * arm, -105 - 120 * arm)], 15, coat)
        g.line([(-70, -175), (-96, -105)], 15, coat)
        g.rrect(-76, -205, 152, 145, 34, coat, 7, seed=seed)
        if look == "leader":
            for r in range(3):                       # เหรียญตราเต็มอก
                for k in range(4):
                    g.rrect(-62 + k * 15, -180 + r * 16, 13, 11, 2, MEDALS[(r * 4 + k) % 8], 2)
            for sx in (-1, 1):
                g.blob(sx * 72, -200, 30, 13, GOLD, 5, seed + 4 + sx)
            g.line([(-74, -120), (74, -120)], 6, GOLD, amp=0)
        else:
            for sx in (-1, 1):
                g.rrect(sx * 34 - 18, -165, 36, 26, 5, coat, 4)               # กระเป๋าเสื้อ
        g.rrect(-28, -222, 56, 24, 8, coat, 5)
        curly_hair(g, 80, -290, messy=1.0 if look == "old" else 0.0, seed=seed)
        g.blob(0, -285, 76, 84, TAN, 7, seed + 7)
        with g.at(0, -285):
            g.face(70, mood, seed=seed)
            if look == "old":
                for sx in (-1, 1):
                    g.arc(sx * 25, 14, 14, 20, 160, 3, GREY)                 # ถุงใต้ตา
        if shades and look != "young":
            for sx in (-1, 1):
                g.rrect(sx * 30 - 25, -307, 50, 34, 14, INK, 0)
                g.rrect(sx * 30 - 17, -302, 14, 8, 4, GREY, 0)
            g.line([(-6, -292), (6, -292)], 5)
        if look in ("young", "leader"):              # หมวกทหาร
            cap = KHAKI if look == "young" else CREAM
            g.c.move_to(-74, -345)
            g.c.curve_to(-70, -410, 70, -410, 74, -345)
            g.c.close_path()
            g.fs(cap, 6)
            g.rrect(-78, -352, 156, 22, 8, INK if look == "leader" else BROWN, 5)
            g.poly([(-60, -332), (60, -332), (40, -314), (-40, -314)], INK, 0)
            g.star(0, -375, 13, GOLD, 3)
            if look == "leader":
                g.line([(-60, -341), (60, -341)], 5, GOLD, amp=0)


def idris(g, x, y, sc=1.0, mood="happy", rot=0, wave=0.0, seed=231):
    """กษัตริย์อิดริสที่ 1: ชราผอม แว่นกลม หนวดเคราสีเทา ชุดคลุมขาว เสื้อคลุมเข้ม หมวกทรงกระบอกสีเข้ม"""
    with g.at(x, y, sc, rot):
        g.poly([(-46, -200), (46, -200), (74, 0), (-74, 0)], WHITE, 6, seed=seed)
        g.poly([(-60, -205), (-20, -205), (-50, 0), (-90, 0)], NAVY, 6, seed=seed + 1)
        g.poly([(60, -205), (20, -205), (50, 0), (90, 0)], NAVY, 6, seed=seed + 2)
        g.line([(60, -190), (95 + 10 * math.sin(wave * 12), -260 - 40 * wave)], 13, NAVY)
        g.blob(0, -275, 66, 78, SKIN, 7, seed + 3)
        with g.at(0, -275):
            g.face(62, mood, seed=seed)
        g.poly([(-34, -236), (0, -228), (34, -236), (28, -210), (0, -196), (-28, -210)], LGREY, 5,
               seed=seed + 4, smooth=True)                                       # เคราสั้นสีเทา
        for sx in (-1, 1):
            g.circle(sx * 23, -277, 18, None, 4)                                 # แว่นกลม
        g.line([(-5, -277), (5, -277)], 4)
        g.rrect(-52, -372, 104, 62, 10, INK, 0)                                 # หมวก
        g.line([(-52, -318), (52, -318)], 5, GOLD, amp=0)


def nasser(g, x, y, sc=1.0, seed=241):
    """ญะมาล อับดุล นัสเซอร์ (รูปครึ่งตัวในกรอบ): ผมดำเถิก หนวด ยิ้มกว้าง สูทเข้ม"""
    with g.at(x, y, sc):
        g.rrect(-110, -150, 220, 260, 30, WHITE, 7)
        g.c.save()
        g.c.rectangle(-104, -144, 208, 248)
        g.c.clip()
        g.blob(0, 110, 95, 70, NAVY, 6, seed)
        g.poly([(-18, 45), (18, 45), (0, 95)], WHITE, 4)
        g.blob(0, -10, 62, 70, TAN, 6, seed + 1)
        g.c.move_to(-62, -20)
        g.c.curve_to(-60, -90, 60, -90, 62, -20)
        g.c.curve_to(40, -60, -20, -66, -40, -40)
        g.c.close_path()
        g.fs(INK, 4)
        with g.at(0, -10):
            g.face(58, "laugh", seed=seed)
        g.blob(0, 2, 26, 7, INK, 0, seed + 2)
        g.c.restore()


def guard(g, x, y, sc=1.0, seed=251):
    """องครักษ์หญิง: เครื่องแบบเขียว หมวกเบเร่ต์แดง ผมยาว แว่นดำ"""
    with g.at(x, y, sc):
        g.line([(-14, -60), (-14, 0)], 10)
        g.line([(14, -60), (14, 0)], 10)
        g.rrect(-34, -135, 68, 85, 20, LYGREEN, 6, seed=seed)
        g.blob(0, -165, 40, 70, INK, 0, seed + 1)
        g.circle(0, -180, 34, TAN, 6)
        with g.at(0, -180):
            g.face(32, "flat", seed=seed)
        for sx in (-1, 1):
            g.rrect(sx * 13 - 11, -192, 22, 14, 6, INK, 0)
        g.blob(6, -212, 40, 14, RED, 5, seed + 2)


def tent(g, x, y, sc=1.0, seed=261):
    with g.at(x, y, sc):
        g.poly([(-220, 0), (-160, -150), (0, -200), (160, -150), (220, 0)], SAND2, 8, seed=seed, smooth=True)
        for k in range(-2, 3):
            g.line([(k * 70, -175 + abs(k) * 20), (k * 95, 0)], 5, BROWN)
        g.poly([(-50, 0), (0, -120), (50, 0)], BROWN, 6)
        g.line([(-220, 0), (-260, 10)], 4, BROWN)
        g.line([(220, 0), (260, 10)], 4, BROWN)


def goat(g, x, y, sc=1.0, t=0.0, seed=271):
    with g.at(x, y - 8 * abs(math.sin(t * 6 + seed)), sc):
        for k in (-35, -15, 15, 35):
            g.line([(k, -20), (k, 15)], 7)
        g.blob(0, -45, 55, 32, WHITE, 6, seed)
        g.blob(55, -75, 24, 22, WHITE, 6, seed + 1)
        g.line([(52, -95), (40, -118)], 5)
        g.line([(62, -95), (70, -118)], 5)
        g.circle(62, -78, 3.5, INK, 0)
        g.blob(60, -50, 6, 9, WHITE, 3, seed + 2)


def pickup(g, x, y, sc=1.0, t=0.0, seed=281):
    with g.at(x, y + 2 * math.sin(t * 30 + seed), sc):
        g.rrect(-110, -70, 220, 50, 12, SAND2, 6, seed=seed)
        g.rrect(-20, -115, 80, 50, 12, SAND2, 6, seed=seed + 1)
        g.rrect(-5, -105, 50, 30, 6, LGREY, 4)
        for k in (-65, 65):
            g.circle(k, -15, 22, INK, 0)
            g.circle(k, -15, 9, GREY, 0)


def jet(g, x, y, sc=1.0, rot=0):
    with g.at(x, y, sc, rot):
        g.poly([(-120, 0), (60, -18), (120, 0), (60, 18)], GREY, 6)
        g.poly([(-10, -8), (40, -8), (-30, -80), (-55, -80)], GREY, 5)
        g.poly([(-10, 8), (40, 8), (-30, 80), (-55, 80)], GREY, 5)
        g.poly([(-110, -2), (-80, -2), (-110, -45)], GREY, 5)
        g.rrect(40, -10, 40, 14, 6, LGREY, 3)


def culvert(g, x, y, sc=1.0, dark=1.0):
    """ท่อระบายน้ำคอนกรีตใต้ถนน 2 ท่อ"""
    with g.at(x, y, sc):
        g.poly([(-330, 0), (-250, -170), (250, -170), (330, 0)], SAND2, 8, smooth=False)
        g.rrect(-260, -190, 520, 28, 6, GREY, 6)
        for k in (-100, 100):
            g.circle(k, -60, 70, LGREY, 8)
            g.circle(k, -60, 52, (0.15, 0.14, 0.13, dark), 6)


def libya_map(g, x, y, w, fill=SAND, lw=8, cities=()):
    pts = LIBYA
    g.shape(pts, x, y, w, fill, lw)
    for name, (u, v) in cities:
        px, py = x + (u - 0.5) * w, y + (v - 0.5) * w
        g.circle(px, py, 12, RED, 4)
        g.text(name, px, py + 42, 40, "kanit")


LIBYA = [(0.08, 0.02), (0.20, 0.05), (0.30, 0.08), (0.38, 0.15), (0.45, 0.22), (0.55, 0.18), (0.62, 0.08),
         (0.70, 0.00), (0.85, 0.02), (0.98, 0.06), (1.00, 0.25), (1.00, 0.75), (0.62, 0.92), (0.55, 0.98),
         (0.35, 0.85), (0.12, 0.75), (0.08, 0.55), (0.00, 0.35), (0.05, 0.02)]
CITY = {"ตริโปลี": (0.12, 0.06), "สิรต์": (0.45, 0.22), "เบงกาซี": (0.69, 0.05), "มิสราตา": (0.28, 0.09)}


def green_book(g, x, y, sc=1.0, rot=0):
    with g.at(x, y, sc, rot):
        g.rrect(-90, -120, 180, 240, 14, LYGREEN, 8)
        g.rrect(-90, -120, 26, 240, 8, (0.18, 0.45, 0.25, 1), 6)
        g.text("สมุดปกเขียว", 12, -30, 34, "kanit", WHITE)
        g.circle(12, 40, 30, GOLD2, 5)
