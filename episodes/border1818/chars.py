"""ตัวละครและพร็อพ: อนุสัญญาปี 1818 / เส้นขนานที่ 49"""
import math

from gfx import BLUE, BROWN, BROWN2, GOLD, GOLD2, GREY, ICE, INK, LGREY, NAVY, RED, SKIN, WHITE, hexc

UK_RED = hexc("#b8473a")
CANADA = hexc("#f3dccb")
USA = hexc("#dbe6f3")
LAKE = hexc("#9cc3e0")
FOREST = hexc("#7ea36f")


def union_jack(g, x, y, w, h):
    """ธงยูเนียนแจ็กแบบย่อ (ใช้บนเสื้อกั๊กจอห์น บูล)"""
    c = g.c
    c.save()
    c.rectangle(x, y, w, h)
    c.clip()
    g.c.rectangle(x, y, w, h)
    g.fs(NAVY, 0)
    for (ax, ay, bx, by) in ((x, y, x + w, y + h), (x + w, y, x, y + h)):
        g.line([(ax, ay), (bx, by)], h * 0.22, WHITE, amp=0)
        g.line([(ax, ay), (bx, by)], h * 0.08, UK_RED, amp=0)
    g.line([(x + w / 2, y), (x + w / 2, y + h)], w * 0.26, WHITE, amp=0)
    g.line([(x, y + h / 2), (x + w, y + h / 2)], h * 0.32, WHITE, amp=0)
    g.line([(x + w / 2, y), (x + w / 2, y + h)], w * 0.14, UK_RED, amp=0)
    g.line([(x, y + h / 2), (x + w, y + h / 2)], h * 0.18, UK_RED, amp=0)
    c.restore()
    g.rrect(x, y, w, h, 4, None, 4)


def john_bull(g, x, y, sc=1.0, mood="happy", rot=0, arm=0.0, seed=401):
    """จอห์น บูล (สัญลักษณ์อังกฤษ): อ้วนท้วน หมวกทรงสูงเตี้ย จอนยาว เสื้อโค้ตแดง เสื้อกั๊กลายยูเนียนแจ็ก"""
    with g.at(x, y, sc, rot):
        for sx in (-1, 1):
            g.rrect(sx * 26 - 15, -70, 30, 70, 8, WHITE, 6)
            g.rrect(sx * 28 - 20, -34, 40, 34, 8, BROWN, 6)
        g.line([(80, -165), (110 + 25 * arm, -100 - 110 * arm)], 16, UK_RED)
        g.line([(-80, -165), (-110, -100)], 16, UK_RED)
        g.blob(0, -125, 95, 85, UK_RED, 7, seed)
        union_jack(g, -48, -190, 96, 120)
        g.blob(0, -265, 74, 68, SKIN, 7, seed + 1)
        for sx in (-1, 1):
            g.blob(sx * 64, -248, 18, 34, BROWN2, 5, seed + 2 + sx)
        with g.at(0, -268):
            g.face(64, mood, seed=seed)
        g.rrect(-80, -325, 160, 18, 8, INK, 0)
        g.rrect(-52, -395, 104, 76, 8, INK, 0)


def gallatin(g, x, y, sc=1.0, mood="happy", rot=0, arm=0.0, seed=411):
    """อัลเบิร์ต แกลลาทิน (ทูตสหรัฐฯ): หัวเถิกกลาง ผมข้างหูฟู จมูกโด่ง ผ้าผูกคอขาว เสื้อโค้ตดำ"""
    with g.at(x, y, sc, rot):
        for sx in (-1, 1):
            g.rrect(sx * 22 - 13, -70, 26, 70, 8, INK, 0)
        g.line([(68, -175), (92 + 25 * arm, -105 - 110 * arm)], 14, INK)
        g.line([(-68, -175), (-92, -105)], 14, INK)
        g.poly([(-74, -200), (74, -200), (84, -60), (-84, -60)], hexc("#2c2c33"), 7, seed=seed, smooth=True)
        g.poly([(-24, -205), (24, -205), (12, -150), (-12, -150)], WHITE, 5)
        for sx in (-1, 1):
            g.blob(sx * 70, -268, 22, 32, LGREY, 5, seed + sx)
        g.blob(0, -270, 70, 80, SKIN, 7, seed + 2)
        with g.at(0, -276):
            g.face(64, mood, seed=seed, mouth_dy=20)
        g.poly([(-4, -270), (8, -270), (24, -238), (8, -232)], SKIN, 5, smooth=True)


def robinson(g, x, y, sc=1.0, mood="happy", rot=0, arm=0.0, seed=421):
    """เฟรเดอริก โรบินสัน (ทูตอังกฤษ): ผมหยิกน้ำตาล จอนยาว คอเสื้อตั้ง เสื้อโค้ตแดงเลือดหมู"""
    with g.at(x, y, sc, rot):
        for sx in (-1, 1):
            g.rrect(sx * 22 - 13, -70, 26, 70, 8, WHITE, 6)
        g.line([(68, -175), (92 + 25 * arm, -105 - 110 * arm)], 14, hexc("#7a2e2e"))
        g.line([(-68, -175), (-92, -105)], 14, hexc("#7a2e2e"))
        g.poly([(-74, -200), (74, -200), (84, -60), (-84, -60)], hexc("#7a2e2e"), 7, seed=seed, smooth=True)
        for sx in (-1, 1):
            g.poly([(sx * 6, -195), (sx * 44, -214), (sx * 38, -176)], WHITE, 5)
        g.blob(0, -270, 70, 80, SKIN, 7, seed + 2)
        for i in range(9):
            a = math.radians(195 + i * 18.7)
            g.circle(math.cos(a) * 70, -275 + math.sin(a) * 72, 20, BROWN, 5)
        for sx in (-1, 1):
            g.blob(sx * 64, -240, 14, 30, BROWN, 4, seed + 3 + sx)
        with g.at(0, -272):
            g.face(64, mood, seed=seed)


def mountie_flag(g, x, y, w, h, kind, t):
    """ธงเล็ก: us (ดาวและแถบ) / uk (ยูเนียนแจ็ก)"""
    if kind == "uk":
        union_jack(g, x, y, w, h)
    else:
        g.flag(x, y, w, h, "us", t, 0.6)


def white_house(g, x, y, sc=1.0):
    with g.at(x, y, sc):
        g.rrect(-220, -200, 440, 200, 6, WHITE, 7)
        g.poly([(-90, -200), (0, -280), (90, -200)], WHITE, 7)
        for k in range(-2, 3):
            g.rrect(k * 45 - 10, -190, 20, 180, 4, LGREY, 4)
        for k in (-180, -140, 140, 180):
            g.rrect(k - 14, -160, 28, 50, 4, ICE, 4)


def bomb(g, x, y, sc=1.0, t=0.0, lit=True):
    with g.at(x, y, sc):
        g.circle(0, 0, 90, INK, 0)
        g.circle(-30, -30, 20, GREY, 0)
        g.rrect(-24, -118, 48, 34, 8, GREY, 5)
        g.line([(0, -118), (20, -160), (50, -170)], 6, BROWN2)
        if lit:
            for i in range(6):
                a = t * 12 + i
                g.line([(50, -170), (50 + 26 * math.cos(a), -170 + 26 * math.sin(a))], 5, GOLD, amp=0)
            g.circle(50, -170, 9, GOLD2, 3)


def tipi(g, x, y, sc=1.0):
    with g.at(x, y, sc):
        g.poly([(-80, 0), (0, -170), (80, 0)], BROWN2, 7)
        g.poly([(-22, 0), (0, -60), (22, 0)], BROWN, 5)
        for k in (-14, 0, 14):
            g.line([(0, -165), (k * 1.6, -205)], 5, BROWN)
        g.line([(-60, -50), (60, -50)], 5, RED)


def pine(g, x, y, sc=1.0):
    with g.at(x, y, sc):
        g.rrect(-8, -30, 16, 32, 3, BROWN, 4)
        for i in range(3):
            w = 50 - i * 12
            g.poly([(-w, -30 - i * 34), (w, -30 - i * 34), (0, -100 - i * 34)], FOREST, 5)


def car(g, x, y, sc=1.0, t=0.0, flip=False):
    with g.at(x, y + 2 * math.sin(t * 25), sc, sx=-sc if flip else sc, sy=sc):
        g.rrect(-90, -70, 180, 50, 16, BLUE, 6)
        g.rrect(-50, -110, 100, 46, 16, BLUE, 6)
        g.rrect(-36, -102, 72, 30, 8, ICE, 4)
        for k in (-55, 55):
            g.circle(k, -18, 20, INK, 0)
            g.circle(k, -18, 8, GREY, 0)


def school(g, x, y, sc=1.0, label="โรงเรียน", cross=False):
    with g.at(x, y, sc):
        g.rrect(-110, -150, 220, 150, 8, WHITE, 7)
        g.poly([(-130, -150), (0, -230), (130, -150)], RED if not cross else WHITE, 7)
        g.rrect(-24, -80, 48, 80, 6, BROWN2, 5)
        if cross:
            g.rrect(-12, -215, 24, 60, 3, RED, 0)
            g.rrect(-30, -197, 60, 24, 3, RED, 0)
        g.text(label, 0, -115, 36, "kanit")
