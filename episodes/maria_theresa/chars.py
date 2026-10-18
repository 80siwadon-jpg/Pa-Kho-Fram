"""ตัวละครและพร็อพ: ตอนมาเรีย เทเรซา (1740)"""
import math

from gfx import GOLD, GOLD2, GREY, INK, LGREY, RED, SKIN, WHITE, hexc, hn

ROYAL_BLUE = hexc("#7fa6d6")
PRUSSIAN = hexc("#2f4a7a")
ERMINE = hexc("#fbfaf6")
BLONDE = hexc("#e8c98a")
BLACK_DRESS = hexc("#2b2a2e")
HU_RED = hexc("#b8473a")
HU_GREEN = hexc("#4f7d4f")
FUR = hexc("#5b4636")


def wig_curls(g, R, cy, rows=4, col=WHITE, seed=0):
    """วิกผมหยิกยาวแบบบาโรก: ลอนวงกลมห้อยสองข้างลงมาถึงไหล่"""
    for sx in (-1, 1):
        for r in range(rows):
            for k in range(2):
                g.circle(sx * (R * 0.85 + k * R * 0.28), cy + r * R * 0.42 - R * 0.2, R * 0.24, col, 5)
    for i in range(7):
        a = math.radians(200 + i * 23.3)
        g.circle(math.cos(a) * R * 0.98, cy + math.sin(a) * R * 0.95, R * 0.27, col, 5)


def charles(g, x, y, sc=1.0, mood="happy", rot=0, arm=0.0, seed=301):
    """จักรพรรดิชาร์ลส์ที่ 6: วิกขาวยาวหยิก กรามยื่น (ฮับส์บูร์ก) ฉลองพระองค์แดงขลิบเออร์มิน สร้อยขนแกะทองคำ"""
    with g.at(x, y, sc, rot):
        g.poly([(-80, -210), (80, -210), (120, 0), (-120, 0)], RED, 7, seed=seed)
        g.poly([(-30, -210), (30, -210), (40, 0), (-40, 0)], ERMINE, 5, seed=seed + 1)
        for k in range(5):
            g.circle(0, -180 + k * 38, 4, INK, 0)
        g.line([(80, -190), (110 + 20 * arm, -110 - 100 * arm)], 15, RED)
        g.line([(-80, -190), (-110, -110)], 15, RED)
        wig_curls(g, 82, -290, seed=seed)
        g.blob(0, -285, 72, 82, SKIN, 7, seed + 2)
        with g.at(0, -292):
            g.face(66, mood, seed=seed, mouth_dy=10)
        g.blob(0, -222, 34, 16, SKIN, 5, seed + 3)          # กรามยื่น
        g.line([(-40, -205), (0, -175), (40, -205)], 5, GOLD, amp=0)
        g.sparkle(0, -172, 14, GOLD, 3)                      # ขนแกะทองคำ


def crown(g, x, y, sc=1.0, rot=0, hungarian=False):
    with g.at(x, y, sc, rot):
        g.poly([(-60, 0), (-70, -60), (-35, -30), (0, -75), (35, -30), (70, -60), (60, 0)], GOLD, 6)
        for k in (-40, 0, 40):
            g.circle(k, -16, 8, RED if k else ROYAL_BLUE, 3)
        if hungarian:   # มงกุฎเซนต์สตีเฟนกับกางเขนเอียง
            with g.at(0, -75, 1, 14):
                g.line([(0, 0), (0, -38)], 7, GOLD, amp=0)
                g.line([(-14, -24), (14, -24)], 7, GOLD, amp=0)


def maria(g, x, y, sc=1.0, mood="happy", rot=0, dress="blue", baby=0.0, crown_on=0.0, arm=0.0, seed=311):
    """มาเรีย เทเรซา: ผมบลอนด์เกล้าสูง สร้อยไข่มุก ชุดกระโปรงบาน (blue = ราชินี, black = ชุดไว้ทุกข์)"""
    col = ROYAL_BLUE if dress == "blue" else BLACK_DRESS
    with g.at(x, y, sc, rot):
        g.c.move_to(-30, -175)
        g.c.curve_to(-80, -110, -140, -40, -135, 0)
        g.c.line_to(135, 0)
        g.c.curve_to(140, -40, 80, -110, 30, -175)
        g.c.close_path()
        g.fs(col, 7)
        if dress == "blue":
            for k in range(3):
                g.arc(0, -175 + 55 * (k + 1) - 640, 640, 83, 97, 5, WHITE)
        g.rrect(-34, -215, 68, 52, 16, col, 6)
        if baby > 0:   # อุ้มทารกในผ้าห่อตัว
            with g.at(0, -150, baby):
                g.blob(0, 0, 58, 36, WHITE, 6, seed)
                g.circle(-34, -6, 22, SKIN, 5)
                with g.at(-34, -6):
                    g.face(20, "sleep", seed=seed + 1)
            g.line([(-40, -200), (-60, -150), (30, -140)], 12, col)
            g.line([(40, -200), (60, -150), (-10, -132)], 12, col)
        else:
            g.line([(-38, -200), (-70, -130)], 12, col)
            g.line([(38, -200), (70 + 20 * arm, -130 - 110 * arm)], 12, col)
        for k in range(7):   # สร้อยไข่มุก
            a = math.radians(200 + k * 23)
            g.circle(math.cos(a) * 30, -205 - math.sin(a) * 14, 5, WHITE, 2)
        g.blob(0, -290, 34, 50, BLONDE, 5, seed + 2)          # มวยผมสูงด้านหลัง
        g.circle(0, -250, 58, SKIN, 7)
        g.c.move_to(-60, -255)
        g.c.curve_to(-62, -320, 62, -320, 60, -255)
        g.c.curve_to(40, -292, -40, -292, -60, -255)
        g.c.close_path()
        g.fs(BLONDE, 5)
        g.circle(0, -330, 22, BLONDE, 5)
        with g.at(0, -246):
            g.face(54, mood, seed=seed)
        if dress == "black":
            g.c.move_to(-66, -260)
            g.c.curve_to(-70, -350, 70, -350, 66, -260)
            g.c.line_to(80, -170)
            g.c.line_to(64, -175)
            g.c.curve_to(56, -300, -56, -300, -64, -175)
            g.c.line_to(-80, -170)
            g.c.close_path()
            g.fs(BLACK_DRESS, 5)                               # ผ้าคลุมไว้ทุกข์
        if crown_on > 0:
            crown(g, 0, lerp_(-470, -312, crown_on), 0.65, hungarian=True)


def lerp_(a, b, k):
    return a + (b - a) * k


def frederick(g, x, y, sc=1.0, mood="smug", rot=0, arm=0.0, seed=321):
    """พระเจ้าฟรีดริชที่ 2 แห่งปรัสเซีย: หมวกสามมุมดำ วิกขาวมัดหาง เครื่องแบบน้ำเงินปรัสเซีย ปกแดง ดาวอินทรีดำ"""
    with g.at(x, y, sc, rot):
        for sx in (-1, 1):
            g.rrect(sx * 22 - 13, -70, 26, 70, 8, WHITE, 6)
            g.rrect(sx * 24 - 17, -32, 34, 32, 8, INK, 0)
        g.line([(68, -175), (96 + 30 * arm, -105 - 110 * arm)], 15, PRUSSIAN)
        g.line([(-68, -175), (-96, -105)], 15, PRUSSIAN)
        g.rrect(-74, -205, 148, 145, 30, PRUSSIAN, 7, seed=seed)
        g.rrect(-74, -205, 30, 145, 14, RED, 5)
        g.rrect(44, -205, 30, 145, 14, RED, 5)
        g.star(-6, -150, 20, LGREY, 4, pts=8, inner=0.5)
        g.circle(-6, -150, 8, INK, 0)
        for sx in (-1, 1):   # ลอนวิกข้างหู
            g.circle(sx * 64, -270, 20, WHITE, 5)
            g.circle(sx * 64, -238, 18, WHITE, 5)
        g.blob(0, -275, 66, 76, SKIN, 7, seed + 1)
        with g.at(0, -280):
            g.face(62, mood, seed=seed)
        g.poly([(-110, -330), (0, -380), (110, -330), (70, -312), (0, -336), (-70, -312)], INK, 0)   # หมวกสามมุม
        g.line([(-100, -330), (0, -372), (100, -330)], 5, GOLD, amp=0)


def wolf(g, x, y, sc=1.0, t=0.0, flag=None, mood="smug", seed=331):
    """หมาป่าการ์ตูน (แทนมหาอำนาจที่รุมทึ้ง) พร้อมธงชาติบนหลัง"""
    with g.at(x, y + 6 * math.sin(t * 6 + seed), sc):
        for k in (-40, -15, 20, 45):
            g.line([(k, -30), (k, 10)], 10)
        g.blob(0, -60, 70, 42, GREY, 6, seed)
        g.poly([(-70, -70), (-110, -90), (-80, -50)], GREY, 5)
        g.blob(70, -100, 46, 40, GREY, 6, seed + 1)
        g.poly([(50, -130), (60, -175), (80, -135)], GREY, 5)
        g.poly([(85, -130), (100, -170), (108, -125)], GREY, 5)
        g.blob(108, -88, 26, 16, LGREY, 4, seed + 2)
        g.circle(128, -92, 7, INK, 0)
        with g.at(66, -104):
            g.face(30, mood, seed=seed)
        if flag:
            g.line([(-20, -95), (-20, -200)], 5, GREY)
            fw, fh = 84, 54
            n = len(flag)
            for i, col in enumerate(flag):
                g.c.rectangle(-20 + fw * i / n, -200, fw / n, fh)
                g.fs(col, 0)
            g.rrect(-20, -200, fw, fh, 2, None, 4)


def noble(g, x, y, sc=1.0, mood="happy", sword=0.0, t=0.0, seed=341):
    """ขุนนางฮังการี: หมวกขนสัตว์มีขนนก หนวดเฟิ้ม เสื้อดอลมานแดง/เขียว ดาบโค้ง"""
    coat = HU_RED if seed % 2 else HU_GREEN
    with g.at(x, y, sc):
        g.line([(-14, -60), (-14, 0)], 12)
        g.line([(14, -60), (14, 0)], 12)
        g.rrect(-42, -150, 84, 100, 24, coat, 6, seed=seed)
        for k in range(4):
            g.line([(-24, -130 + k * 20), (24, -130 + k * 20)], 4, GOLD, amp=0)
        g.circle(0, -185, 40, SKIN, 6)
        with g.at(0, -185):
            g.face(38, mood, seed=seed)
        g.blob(-14, -170, 18, 6, INK, 0, seed + 1)
        g.blob(14, -170, 18, 6, INK, 0, seed + 2)
        g.rrect(-36, -248, 72, 46, 16, FUR, 5)
        g.line([(20, -246), (34, -300), (44, -320)], 6, WHITE)
        # ดาบ: 0 = อยู่ในฝัก, 1 = ชูขึ้นฟ้า
        ang = -100 + 70 * (1 - sword) + 6 * math.sin(t * 8 + seed) * sword
        with g.at(44, -130 + 40 * (1 - sword), 1, ang):
            g.line([(0, 0), (130, 0)], 9, LGREY, amp=0)
            g.line([(-10, -14), (-10, 14)], 7, GOLD, amp=0)


def scroll(g, x, y, sc=1.0, rot=0, seal=RED, torn=0.0):
    with g.at(x, y, sc, rot):
        if torn <= 0:
            g.rrect(-70, -95, 140, 190, 10, ERMINE, 6)
            for k in range(5):
                g.line([(-48, -60 + k * 24), (48 - (k % 2) * 20, -60 + k * 24)], 4, LGREY)
            g.circle(30, 62, 18, seal, 4)
        else:
            for i in range(4):
                dx = (i - 1.5) * 40 * torn
                dy = (hn(i, 3) * 60 + 80 * i) * torn
                with g.at(dx, dy, 1, (hn(i, 4) * 60) * torn):
                    g.poly([(-35 + i * 0, -95 + i * 47), (35, -95 + i * 47), (30, -48 + i * 47), (-30, -52 + i * 47)],
                           ERMINE, 4, seed=i)


def candle(g, x, y, sc=1.0, t=0.0, lit=1.0):
    with g.at(x, y, sc):
        g.rrect(-22, -150, 44, 150, 8, ERMINE, 6)
        g.line([(0, -150), (0, -168)], 4)
        if lit > 0:
            with g.alpha(lit):
                fl = 1 + 0.12 * math.sin(t * 17)
                g.c.save()
                g.c.translate(0, -195)
                g.c.scale(1, fl)
                g.c.move_to(0, -36)
                g.c.curve_to(22, -6, 18, 22, 0, 26)
                g.c.curve_to(-18, 22, -22, -6, 0, -36)
                g.fs(GOLD2, 4)
                g.c.restore()
        else:
            for k in range(3):
                g.circle(8 * math.sin(t * 3 + k), -190 - k * 26, 8 + k * 3, LGREY, 0)
