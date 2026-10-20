"""ตัวละครและพร็อพ: เบนจามิน โอ. เดวิส ซีเนียร์ นายพลผิวดำคนแรกของกองทัพสหรัฐฯ (25 ต.ค. 1940)
การเหยียดสีผิว: สื่อด้วยป้ายแบ่งแยก/เส้นกั้น/บันได ไม่แสดงความรุนแรง"""
import math

from gfx import GOLD, GOLD2, GREY, INK, NAVY, RED, WHITE, hexc
from people import Look, _rr, _shade, _smooth_path, _stroke

OLIVE = hexc("#5f5a3a")
KHAKI = hexc("#b8a576")
SILVER = hexc("#d9dde3")
DAVIS_SKIN = hexc("#b07a52")

# เดวิส ซีเนียร์ (63 ปี): ผมสั้นสีเทาเกรียน หนวดเทาเล็ก แว่นกรอบลวดกลม เครื่องแบบสีเขียวมะกอก หมวกหนีบติดดาว
DAVIS = Look(hair="short", hair_col=hexc("#a8a49c"), suit=OLIVE, shirt=KHAKI, tie=hexc("#4a4630"), glasses="roundthin",
             facial="mustache", skin=DAVIS_SKIN, w=57, jaw=0.5, jowls=0.2, nose=1.05, brow=0.8, age=0.75,
             hat="garrison", hat_trim=OLIVE, stars=1)
DAVIS_COL = Look(hair="short", hair_col=hexc("#a8a49c"), suit=OLIVE, shirt=KHAKI, tie=hexc("#4a4630"),
                 glasses="roundthin", facial="mustache", skin=DAVIS_SKIN, w=57, jaw=0.5, jowls=0.2, nose=1.05,
                 brow=0.8, age=0.75)
# พลทหารเดวิสวัยหนุ่ม (ปี 1899)
DAVIS_YOUNG = Look(hair="short", hair_col=hexc("#1b1714"), suit=hexc("#2b3a5a"), shirt=hexc("#2b3a5a"),
                   tie=hexc("#2b3a5a"), outfit="tunic", pants=hexc("#5a6a8a"), skin=DAVIS_SKIN, w=55, age=0.0,
                   hat="kepi", hat_trim=hexc("#2b3a5a"))
# แฟรงกลิน ดี. โรสเวลต์: ผมเทาหวีเรียบ แว่นหนีบจมูก กรามกว้าง ยิ้ม สูทเทา
FDR = Look(hair="part", hair_col=hexc("#9a948a"), suit=hexc("#4a4f58"), tie=hexc("#2b3f63"), glasses="roundthin",
           w=60, jaw=0.75, jowls=0.15, nose=1.05, brow=0.9, age=0.65, build=1.1)
# ลูกชาย: เดวิส จูเนียร์ นักบินทัสคีกี
SON = Look(hair="short", hair_col=hexc("#1b1714"), suit=hexc("#6b5a3a"), shirt=KHAKI, tie=hexc("#4a4630"),
           facial="mustache", skin=DAVIS_SKIN, w=56, jaw=0.5, age=0.2, hat="garrison", hat_trim=hexc("#6b5a3a"))
SOLDIERS_B = [   # ทหารผิวดำ
    Look(hair="buzz", hair_col=hexc("#1b1714"), suit=OLIVE, shirt=KHAKI, tie=OLIVE, skin=hexc("#7a4a2c"), w=55,
         age=0.1, hat="garrison", hat_trim=OLIVE),
    Look(hair="buzz", hair_col=hexc("#1b1714"), suit=OLIVE, shirt=KHAKI, tie=OLIVE, skin=hexc("#5a3a26"), w=56,
         age=0.2, hat="garrison", hat_trim=OLIVE),
]
OFFICERS_W = [   # นายทหารผิวขาวที่ดูถูก
    Look(hair="slick", hair_col=hexc("#8a6a42"), suit=OLIVE, shirt=KHAKI, tie=OLIVE, w=57, age=0.5, facial="mustache"),
    Look(hair="part", hair_col=hexc("#3a2a1e"), suit=OLIVE, shirt=KHAKI, tie=OLIVE, w=56, age=0.4),
]


def star(g, x, y, r, k=1.0, col=SILVER):
    if k < 0.02:
        return
    g.star(x, y, r * k, col, 6)
    g.sparkle(x + r * 0.9, y - r * 0.9, r * 0.35 * k)


def order_paper(g, x, y, sc=1.0, rot=0.0, sign=1.0):
    """คำสั่งเลื่อนยศ + ลายเซ็นประธานาธิบดี"""
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -170, -230, 340, 460, 8)
        _shade(c, hexc("#f4eedf"), 6, 0.12)
        c.new_path()
        c.arc(0, -150, 40, 0, 2 * math.pi)
        _shade(c, GOLD, 4, 0.2)
        g.star(0, -150, 18, WHITE, 0)
        g.text("BRIGADIER GENERAL", 0, -80, 30, "kanit", INK)
        for i in range(5):
            _stroke(c, [(-130, -30 + i * 32), (130 - 40 * (i % 2), -30 + i * 32)], 4, INK, 0.35, smooth=False)
        if sign > 0:
            n = int(12 * min(1, sign))
            pts = [(-90 + i * 16, 170 + 14 * math.sin(i * 1.3)) for i in range(n + 1)]
            if len(pts) > 1:
                _stroke(c, pts, 4, NAVY)


def shoulder(g, x, y, sc=1.0, stars=1, k=1.0, t=0.0):
    """บ่าเครื่องแบบใกล้ ๆ + ดาวติดบ่า"""
    c = g.c
    with g.at(x, y, sc):
        _smooth_path(c, [(-320, 200), (-300, -60), (-180, -140), (200, -150), (320, -60), (340, 200)])
        _shade(c, OLIVE, 7, 0.3)
        _rr(c, -200, -120, 360, 70, 30)
        _shade(c, hexc("#6a6444"), 5, 0.2)
        g.circle(150, -85, 16, GOLD, 4)
        for i in range(stars):
            star(g, -60 + i * 90, -85, 44, k)


def sign_board(g, x, y, sc=1.0, rot=0.0, txt="WHITE ONLY", col=RED):
    with g.at(x, y, sc, rot):
        g.line([(0, 0), (0, -300)], 12, hexc("#6e4528"), amp=0)
        g.rrect(-180, -420, 360, 140, 10, WHITE, 7, stroke=col)
        g.text(txt, 0, -350, 46, "kanit", col)


def barrier(g, x0, x1, y, t=0.0, k=1.0):
    """เส้นกั้นแบ่งแยก (เชือก + เสาสองต้น)"""
    for x in (x0, x1):
        g.rrect(x - 14, y - 260, 28, 260, 8, hexc("#c9a24a"), 5)
    sag = 40
    pts = [(x0 + (x1 - x0) * u / 10, y - 230 + sag * math.sin(math.pi * u / 10)) for u in range(11)]
    n = max(2, int(11 * k))
    g.line(pts[:n], 14, RED, amp=0)


def broom(g, x, y, sc=1.0, rot=0.0):
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -8, -320, 16, 300, 6)
        _shade(c, hexc("#a8784a"), 4, 0.2)
        _smooth_path(c, [(-50, -30), (50, -30), (70, 60), (-70, 60)])
        _shade(c, hexc("#d9b46a"), 5, 0.2)
        for k in range(-3, 4):
            _stroke(c, [(k * 16, -20), (k * 20, 58)], 3, INK, 0.4, smooth=False)


def ladder(g, x, y, h=900, sc=1.0, k=1.0):
    c = g.c
    with g.at(x, y, sc):
        for sx in (-90, 90):
            _rr(c, sx - 10, -h, 20, h, 6)
            _shade(c, hexc("#a8784a"), 4, 0.2)
        n = 9
        for i in range(n):
            if i / n > k:
                break
            yy = -60 - i * (h - 80) / (n - 1)
            _rr(c, -90, yy - 8, 180, 16, 4)
            _shade(c, hexc("#c99a62"), 3, 0.1)


def plane(g, x, y, sc=1.0, rot=0.0, t=0.0):
    """เครื่องบินขับไล่ P-51 หางแดง (ฝูงบินทัสคีกี "Red Tails")"""
    c = g.c
    with g.at(x, y, sc, rot):
        _smooth_path(c, [(-260, -10), (-200, -40), (180, -40), (260, -10), (260, 14), (-200, 24), (-260, 14)])
        _shade(c, hexc("#c9ced6"), 6, 0.3)
        _smooth_path(c, [(-240, -10), (-300, -110), (-250, -110), (-190, -30)])
        _shade(c, RED, 5, 0.1)   # หางแดง
        _smooth_path(c, [(-60, 0), (60, 0), (20, 140), (-30, 140)])
        _shade(c, hexc("#b8bec8"), 5, 0.2)
        _smooth_path(c, [(30, -40), (90, -80), (150, -40)])
        _shade(c, hexc("#9ad0f5"), 4, 0)
        _rr(c, 250, -16, 30, 40, 6)
        _shade(c, RED, 4, 0)
        a = t * 40
        for k in range(3):
            ang = a + k * 2.094
            _stroke(c, [(285, 4), (285 + 10 * math.cos(ang), 4 + 70 * math.sin(ang))], 6, INK, smooth=False)
        g.circle(-120, -8, 22, WHITE, 3)
        g.star(-120, -8, 14, NAVY, 0)


def calendar_years(g, x, y, y0, y1, u):
    with g.at(x, y):
        g.rrect(-170, -110, 340, 220, 24, WHITE, 8)
        g.rrect(-170, -110, 340, 60, 24, NAVY, 8)
        yr = int(round(y0 + (y1 - y0) * u))
        g.text(str(yr), 0, 30, 96, "kanit", INK)
