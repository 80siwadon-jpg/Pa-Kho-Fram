"""ตัวละครและพร็อพ: วันเกิดเปเล่ 23 ต.ค. 1940 — ชุดนักฟุตบอลบราซิล เสื้อเหลืองคอเขียว เบอร์ 10 กางเกงน้ำเงิน ถุงเท้าขาว"""
import math

from gfx import GOLD, GOLD2, GREY, INK, NAVY, RED, WHITE, hexc
from people import Look, _rr, _shade, _smooth_path, _stroke

BR_YEL = hexc("#f6d03b")
BR_GRN = hexc("#2f9a4f")
BR_BLU = hexc("#2b4c9a")
SKIN_P = hexc("#6b4428")
DIRT = hexc("#c98a5a")

# เปเล่ (ผู้ใหญ่): ผิวเข้ม ผมสั้นเกรียนหยิก ยิ้มกว้าง เสื้อบราซิลเหลืองเบอร์ 10
PELE = Look(hair="buzz", hair_col=hexc("#1b1714"), skin=SKIN_P, outfit="tee", suit=BR_YEL, shirt=BR_GRN,
            pants=BR_BLU, shorts=True, socks=WHITE, shoes=hexc("#1b1916"), print_txt="10", w=56, jaw=0.55, nose=1.1,
            brow=0.8, age=0.2, height=0.95)
# เปเล่วัยเด็ก: ตัวผอม เท้าเปล่า เสื้อยืดเก่า
KID = Look(hair="buzz", hair_col=hexc("#1b1714"), skin=SKIN_P, outfit="tee", suit=hexc("#d9cdb2"), pants=hexc("#7a6a52"),
           shorts=True, socks=SKIN_P, shoes=SKIN_P, w=54, age=0.0, height=0.62, headsc=1.45, build=0.85)
# ดงดินโย (พ่อ) — อดีตนักฟุตบอล
DAD = Look(hair="buzz", hair_col=hexc("#1b1714"), skin=hexc("#5e3b22"), outfit="tee", suit=hexc("#e8e2d0"),
           pants=hexc("#5a5a60"), w=58, age=0.5, facial="mustache", jaw=0.6)
FANS = [
    Look(hair="short", hair_col=hexc("#2b2622"), outfit="tee", suit=BR_YEL, pants=BR_BLU, skin=hexc("#c99a72"), w=56),
    Look(hair="afro", hair_col=hexc("#1b1714"), outfit="tee", suit=BR_GRN, pants=hexc("#3a3a40"), skin=hexc("#7a5030"),
         w=56),
    Look(hair="bun", hair_col=hexc("#2b2622"), outfit="dress", suit=BR_YEL, skin=hexc("#e2b08a"), w=54, height=0.93),
]
SOLDIERS = [   # ทหารสองฝ่ายสงครามกลางเมืองไนจีเรีย (วางปืน)
    Look(hair="buzz", hair_col=hexc("#1b1714"), outfit="fatigue", suit=hexc("#5f6b45"), pants=hexc("#4a5538"),
         skin=hexc("#5e3b22"), w=56),
    Look(hair="buzz", hair_col=hexc("#1b1714"), outfit="fatigue", suit=hexc("#7a6a45"), pants=hexc("#5a4a32"),
         skin=hexc("#6b4428"), w=56, hat="beret", hat_trim=hexc("#3a3a40")),
]


def ball(g, x, y, r=60, rot=0.0, kind="modern"):
    """ลูกฟุตบอล: modern (ขาวดำ) / leather (หนังน้ำตาลยุค 50) / sock (ถุงเท้ายัดเศษผ้า ผูกเชือก)"""
    c = g.c
    with g.at(x, y, r / 60, rot):
        if kind == "sock":
            _smooth_path(c, [(-58, -10), (-40, -50), (10, -60), (52, -30), (60, 15), (35, 52), (-15, 58), (-55, 30)])
            _shade(c, hexc("#c9c1b0"), 5, 0.3)
            for a in (-0.6, 0.5):
                _stroke(c, [(-60 * math.cos(a), -60 * math.sin(a)), (60 * math.cos(a), 60 * math.sin(a))], 4,
                        hexc("#8a6a42"))
            _stroke(c, [(-20, -40), (-10, -15), (-25, 10)], 3, hexc("#9a917f"))
            return
        col = WHITE if kind == "modern" else hexc("#a8693a")
        c.new_path()
        c.arc(0, 0, 60, 0, 2 * math.pi)
        _shade(c, col, 5, 0.3)
        if kind == "modern":
            g.poly([(0, -22), (21, -7), (13, 18), (-13, 18), (-21, -7)], INK, 0, amp=0)
            for i in range(5):
                a = i * 2 * math.pi / 5 - math.pi / 2
                g.circle(52 * math.cos(a), 52 * math.sin(a), 13, INK, 0)
        else:
            for k in (-25, 0, 25):
                _stroke(c, [(-55, k), (55, k)], 3, hexc("#6e4528"), 0.7)
            _stroke(c, [(0, -30), (0, 30)], 4, hexc("#3a2614"), smooth=False)


def trophy(g, x, y, sc=1.0, rot=0.0, t=0.0):
    """ถ้วยฟุตบอลโลกยุคนั้น (ถ้วยจูลส์ ริเมต์: เทพีปีกกางชูถ้วย บนฐานสี่เหลี่ยม)"""
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -70, -90, 140, 90, 8)
        _shade(c, hexc("#3a5a8a"), 5, 0.2)
        _rr(c, -54, -140, 108, 52, 6)
        _shade(c, GOLD, 5, 0.3)
        _smooth_path(c, [(-30, -140), (30, -140), (20, -260), (-20, -260)])
        _shade(c, GOLD, 5, 0.35)   # ลำตัวเทพี
        for sx in (-1, 1):   # ปีก
            _smooth_path(c, [(sx * 18, -250), (sx * 110, -330), (sx * 90, -260), (sx * 30, -200)])
            _shade(c, GOLD2, 5, 0.3)
        _smooth_path(c, [(-60, -340), (60, -340), (40, -280), (-40, -280)])
        _shade(c, GOLD, 5, 0.3)   # ถ้วยแปดเหลี่ยม
        c.new_path()
        c.arc(0, -258, 16, 0, 2 * math.pi)
        _shade(c, GOLD, 4, 0.2)
        _stroke(c, [(-30, -320), (-24, -290)], 6, WHITE, 0.5)


def radio(g, x, y, sc=1.0, t=0.0, on=True):
    """วิทยุตั้งโต๊ะยุค 50"""
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -170, -220, 340, 220, 40)
        _shade(c, hexc("#8a5a36"), 6, 0.3)
        _rr(c, -140, -190, 160, 160, 20)
        _shade(c, hexc("#e8d6b0"), 4, 0.1)
        for i in range(6):
            _stroke(c, [(-130, -170 + i * 26), (10, -170 + i * 26)], 3, hexc("#8a6a42"), 0.6, smooth=False)
        for k in range(2):
            g.circle(90, -160 + k * 80, 26, hexc("#d9b26a"), 4)
        if on:
            for i in range(3):
                g.arc(-60, -110, 170 + i * 40 + 20 * math.sin(t * 4), -60, 60, 5, (0.3, 0.3, 0.3, 0.5 - i * 0.12))


def favela(g, y, t=0.0, a=1.0):
    """ชุมชนแออัดบนเนินเขา (บ้านหลังเล็กหลากสี)"""
    c = g.c
    cols = [hexc("#e8a33d"), hexc("#8fc7e0"), hexc("#e2788f"), hexc("#9fd08a"), hexc("#f2c94c"), hexc("#d8d3c7")]
    with g.alpha(a):
        _smooth_path(c, [(-500, y), (-100, y - 300), (400, y - 420), (900, y - 300), (1500, y)])
        _shade(c, hexc("#9cbf7a"), 5, 0.2)
        for r in range(3):
            for i in range(9):
                x = -60 + i * 140 + r * 60
                hy = y - 80 - r * 110 - 60 * math.sin((x + 100) / 1300 * math.pi)
                _rr(c, x - 50, hy - 70, 100, 70, 4)
                _shade(c, cols[(i + r) % 6], 4, 0.2)
                _rr(c, x - 15, hy - 50, 30, 30, 2)
                _shade(c, hexc("#3a3a40"), 2, 0)
                _stroke(c, [(x - 56, hy - 70), (x + 56, hy - 70)], 6, hexc("#8a6a52"), smooth=False)


def jersey(g, x, y, sc=1.0, body=BR_YEL, trim=BR_GRN, num="10", stripes=None, rot=0.0):
    """เสื้อฟุตบอล (ไอคอน): stripes = สีแถบตั้ง (อาร์เจนตินา)"""
    c = g.c
    with g.at(x, y, sc, rot):
        pts = [(-60, -150), (-150, -100), (-120, -30), (-90, -50), (-90, 150), (90, 150), (90, -50), (120, -30),
               (150, -100), (60, -150), (30, -130), (-30, -130)]
        c.new_path()
        for p in pts:
            c.line_to(*p)
        c.close_path()
        _shade(c, body, 6, 0.25)
        if stripes:
            c.save()
            c.new_path()
            for p in pts:
                c.line_to(*p)
            c.close_path()
            c.clip()
            for k in (-60, 0, 60):
                _rr(c, k - 15, -160, 30, 320, 0)
                _shade(c, stripes, 0, 0)
            c.restore()
        _stroke(c, [(-30, -130), (0, -100), (30, -130)], 10, trim)
        g.text(num, 0, 20, 110, "kanit", trim)


def gun_down(g, x, y, sc=1.0, rot=0.0):
    """ปืนไรเฟิลวางพิงพื้น (ไม่ได้ใช้งาน)"""
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -160, -12, 220, 24, 6)
        _shade(c, hexc("#4a4a4a"), 4, 0.2)
        _smooth_path(c, [(40, -14), (170, -24), (180, 24), (40, 14)])
        _shade(c, hexc("#7a5230"), 4, 0.2)
