"""ตัวละครและพร็อพ: แอปเปิลเปิดตัว iPod รุ่นแรก 23 ต.ค. 2001 (ไม่วาดโลโก้จริง ใช้ผลแอปเปิลการ์ตูนแทน)"""
import math

from gfx import GOLD, GOLD2, GREY, INK, LGREY, NAVY, RED, WHITE, hexc
from people import Look, _rr, _shade, _smooth_path, _stroke

LCD = hexc("#c9cdb4")
CHROME = hexc("#cfd3d8")
APPLE_RED = hexc("#d8473d")
GREEN = hexc("#3c8d4f")

# สตีฟ จ็อบส์ (46): เสื้อคอเต่าสีดำ ยีนส์ฟ้า รองเท้าผ้าใบเทา แว่นกลมไร้ขอบ ผมสั้นเถิกสีเทาเข้ม หนวดเคราเขียวครึ้ม
JOBS = Look(hair="buzz", hair_col=hexc("#5a524c"), outfit="turtleneck", suit=hexc("#1d1d21"), pants=hexc("#4a6a96"),
            shoes=hexc("#a4a6ab"), glasses="roundthin", stubble=0.6, w=55, jaw=0.3, jowls=0.0, nose=1.1, brow=0.8,
            age=0.45)
CRITICS = [
    Look(hair="part", hair_col=hexc("#6b4a33"), suit=hexc("#3b4250"), tie=hexc("#7a2e2e"), w=58, age=0.4,
         glasses="thin"),
    Look(hair="bun", hair_col=hexc("#2b2622"), outfit="dress", suit=hexc("#8a4a5a"), w=54, age=0.35, height=0.93),
    Look(hair="crew", hair_col=hexc("#3a2f28"), outfit="flannel", suit=hexc("#6a7f9a"), pants=hexc("#3a3a40"),
         w=58, age=0.3, glasses="thick"),
]
TEENS = [
    Look(hair="short", hair_col=hexc("#2b2622"), outfit="hoodie", suit=hexc("#e8892e"), pants=hexc("#3f5f8a"),
         w=56, age=0.1, height=0.9),
    Look(hair="long", hair_col=hexc("#5a3a22"), outfit="tee", suit=hexc("#3c8d9f"), pants=hexc("#2f3a4a"), w=54,
         age=0.05, height=0.88),
    Look(hair="afro", hair_col=hexc("#221e1c"), outfit="tee", suit=hexc("#c8553d"), pants=hexc("#3a3a40"), w=56,
         age=0.1, skin=hexc("#8a5a3c"), height=0.92),
]


def ipod(g, x, y, sc=1.0, rot=0.0, t=0.0, screen=True, sel=0, glow=0.0):
    """iPod รุ่นแรก: หน้าขาว จอ LCD ขาวดำ วงล้อหมุน ปุ่มกลาง — x,y = กลางเครื่อง (สูง ~400)"""
    c = g.c
    with g.at(x, y, sc, rot):
        if glow > 0:
            g.sunburst(0, 0, 230, 380, 16, t * 10, 10, (1, 0.9, 0.6, 0.6 * glow))
        _rr(c, -130, -200, 260, 400, 34)   # ขอบโครเมียมด้านหลัง
        _shade(c, CHROME, 6, 0.35)
        _rr(c, -122, -192, 244, 384, 28)
        _shade(c, WHITE, 3, 0.12)
        _rr(c, -92, -160, 184, 126, 8)
        _shade(c, LCD, 4, 0.05)
        if screen:
            _rr(c, -86, -156, 172, 20, 2)
            _shade(c, hexc("#a9ad96"), 0, 0)
            g.text("iPod", 0, -146, 15, "kanit", INK)
            for i, it in enumerate(("Playlists", "Artists", "Songs", "Settings", "About")):
                yy = -124 + i * 18
                if i == sel:
                    _rr(c, -86, yy - 9, 172, 18, 1)
                    _shade(c, hexc("#2b2b2b"), 0, 0)
                g.text(it, -36, yy, 14, "kanit", WHITE if i == sel else INK)
                g.text(">", 74, yy, 14, "kanit", WHITE if i == sel else INK)
        c.new_path()   # วงล้อ
        c.arc(0, 80, 92, 0, 2 * math.pi)
        _shade(c, hexc("#f4f5f6"), 4, 0.15)
        g.text("MENU", 0, 8, 15, "kanit", GREY)
        g.text("◀◀", -70, 82, 12, "kanit", GREY)
        g.text("▶▶", 70, 82, 12, "kanit", GREY)
        c.new_path()
        c.arc(0, 80, 34, 0, 2 * math.pi)
        _shade(c, WHITE, 3.5, 0.15)


def earbuds(g, x, y, sc=1.0, t=0.0, x2=None, y2=None):
    """หูฟังสีขาว + สายสีขาว จาก (x,y) ยาวลงไปที่ (x2,y2)"""
    c = g.c
    with g.at(x, y, sc):
        for sx in (-1, 1):
            _stroke(c, [(sx * 70, 0), (sx * 40, 120), (0, 220)], 7, INK)
            _stroke(c, [(sx * 70, 0), (sx * 40, 120), (0, 220)], 4, WHITE)
            c.new_path()
            c.arc(sx * 70, 0, 22, 0, 2 * math.pi)
            _shade(c, WHITE, 4, 0.15)
        _stroke(c, [(0, 220), (10, 320), (-20, 420)], 7, INK)
        _stroke(c, [(0, 220), (10, 320), (-20, 420)], 4, WHITE)


def apple(g, x, y, r, col=APPLE_RED, bite=False):
    """ผลแอปเปิลการ์ตูน (แทนบริษัทแอปเปิล — ไม่ใช่โลโก้จริง)"""
    c = g.c
    with g.at(x, y, r / 100):
        _smooth_path(c, [(0, -70), (50, -95), (95, -50), (95, 20), (60, 90), (20, 100), (0, 88), (-20, 100), (-60, 90),
                         (-95, 20), (-95, -50), (-50, -95)])
        _shade(c, col, 6, 0.3)
        _stroke(c, [(0, -70), (6, -110), (14, -130)], 8, hexc("#6e4528"))
        _smooth_path(c, [(10, -110), (60, -140), (80, -110), (40, -95)])
        _shade(c, GREEN, 4, 0.2)
        if bite:
            c.new_path()
            c.arc(100, -10, 34, 0, 2 * math.pi)
            c.set_source_rgba(1, 1, 1, 1)
            c.fill()
        _stroke(c, [(-55, -50), (-65, 0)], 10, WHITE, 0.5)


def cards(g, x, y, sc=1.0, rot=0.0):
    """ตลับไพ่ (เทียบขนาด)"""
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -110, -160, 220, 320, 14)
        _shade(c, hexc("#c8553d"), 6, 0.3)
        _rr(c, -86, -136, 172, 272, 10)
        _shade(c, hexc("#f4efe2"), 4, 0.1)
        # รูปโพดำ
        _smooth_path(c, [(0, -70), (60, 0), (40, 40), (10, 30), (20, 70), (-20, 70), (-10, 30), (-40, 40), (-60, 0)])
        _shade(c, INK, 3, 0)


def stage(g, y, w=1400, small=True, t=0.0):
    """เวทีหอประชุมเล็ก + เก้าอี้ผู้ชมไม่กี่แถว"""
    c = g.c
    _rr(c, -w / 2 + 540, y - 30, w, 60, 6)
    _shade(c, hexc("#5a4a3a"), 5, 0.25)
    for r in range(2):
        for i in range(6):
            x = 60 + i * 190 + r * 90
            yy = y + 150 + r * 70
            _rr(c, x - 60, yy - 50, 120, 70, 12)
            _shade(c, hexc("#7a2e3a"), 4, 0.25)


def mac(g, x, y, sc=1.0, col=hexc("#5aa0c8")):
    """iMac G3 ทรงไข่ใสสี (ยุคเดียวกัน)"""
    c = g.c
    with g.at(x, y, sc):
        _smooth_path(c, [(-170, -360), (170, -360), (190, -120), (130, 0), (-130, 0), (-190, -120)])
        _shade(c, col, 6, 0.3)
        _rr(c, -120, -320, 240, 190, 14)
        _shade(c, hexc("#2b3440"), 4, 0.1)
        _stroke(c, [(-100, -300), (-40, -300)], 6, WHITE, 0.3)
        _rr(c, -60, -70, 120, 14, 6)
        _shade(c, hexc("#2b3440"), 2, 0)


def mp3(g, x, y, sc=1.0, rot=0.0, col=hexc("#7a8a9a")):
    """เครื่องเล่น MP3 ทั่วไป (ปุ่มเยอะ จอเล็ก)"""
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -70, -120, 140, 240, 30)
        _shade(c, col, 5, 0.3)
        _rr(c, -50, -95, 100, 60, 6)
        _shade(c, hexc("#9fc4a8"), 3, 0)
        for i in range(6):
            g.circle(-34 + (i % 3) * 34, 10 + (i // 3) * 40, 12, hexc("#3a3a40"), 3)


def price_tag(g, x, y, sc=1.0, rot=0.0, text="$399"):
    c = g.c
    with g.at(x, y, sc, rot):
        _smooth_path(c, [(-140, -60), (100, -60), (150, 0), (100, 60), (-140, 60)])
        _shade(c, hexc("#f2c94c"), 6, 0.2)
        g.circle(90, 0, 12, WHITE, 4)
        g.text(text, -20, 0, 66, "kanit", INK)


def chart(g, x, y, w, h, pts, k=1.0, col=GREEN, lw=12):
    """กราฟเส้น pts = [(u,v)] ในช่วง 0..1 (v ขึ้น = ค่ามาก)"""
    c = g.c
    g.line([(x, y), (x + w, y)], 6, INK, amp=0)
    g.line([(x, y), (x, y - h)], 6, INK, amp=0)
    n = max(2, int(len(pts) * k + 0.99))
    path = [(x + u * w, y - v * h) for u, v in pts[:n]]
    _stroke(c, path, lw + 6, INK, smooth=False)
    _stroke(c, path, lw, col, smooth=False)
    if k >= 1:
        ex, ey = path[-1]
        g.circle(ex, ey, 16, col, 5)


def silhouette_dancer(g, x, y, sc=1.0, t=0.0, ph=0.0):
    """เงาคนเต้นสีดำ + หูฟังสีขาว (แบบโฆษณา iPod ยุคนั้น)"""
    c = g.c
    b = math.sin(t * 6 + ph)
    with g.at(x, y, sc, 6 * b):
        for sx in (-1, 1):   # ขา
            _stroke(c, [(sx * 20, -260), (sx * (40 + 20 * b * sx), -130), (sx * 30, 0)], 34, INK)
        _smooth_path(c, [(-55, -500), (55, -500), (45, -250), (-45, -250)])
        _shade(c, INK, 0, 0)
        _stroke(c, [(-50, -480), (-120, -560 - 40 * b), (-100, -660)], 26, INK)   # แขนชูขึ้น
        _stroke(c, [(50, -480), (120, -400 + 30 * b), (90, -330)], 26, INK)
        c.new_path()
        c.arc(0, -560, 50, 0, 2 * math.pi)
        _shade(c, INK, 0, 0)
        _stroke(c, [(-30, -555), (-35, -480), (10, -400), (60, -350)], 6, WHITE)   # สายหูฟังขาว
        g.circle(-34, -556, 10, WHITE, 0)
        _rr(c, 40, -380, 40, 64, 8)
        _shade(c, WHITE, 3, 0)


def iphone(g, x, y, sc=1.0, rot=0.0, t=0.0):
    """iPhone รุ่นแรก (2007): จอใหญ่เต็มหน้า ปุ่มโฮมกลม"""
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -130, -250, 260, 500, 40)
        _shade(c, hexc("#2b2b30"), 6, 0.3)
        _rr(c, -110, -200, 220, 370, 8)
        _shade(c, hexc("#3f7fc0"), 3, 0.2)
        for i in range(12):
            col = (hexc("#f2c94c"), hexc("#3c8d4f"), hexc("#d8473d"), WHITE)[i % 4]
            _rr(c, -90 + (i % 4) * 46, -180 + (i // 4) * 60, 36, 36, 9)
            _shade(c, col, 2.5, 0.2)
        c.new_path()
        c.arc(0, 208, 22, 0, 2 * math.pi)
        _shade(c, hexc("#2b2b30"), 4, 0)
        _rr(c, -8, 200, 16, 16, 3)
        c.set_source_rgba(1, 1, 1, 0.5)
        c.set_line_width(2)
        c.stroke()


def ipod_family(g, x, y, sc=1.0, t=0.0, k=1.0):
    """iPod หลายรุ่น: classic / mini / nano / shuffle"""
    c = g.c
    items = [(-330, 1.0, WHITE), (-110, 0.8, hexc("#8fc7e0")), (90, 0.6, hexc("#e2788f")), (260, 0.35, hexc("#9fd08a"))]
    with g.at(x, y, sc):
        for i, (dx, s, col) in enumerate(items):
            kk = max(0.0, min(1.0, k * 4 - i))
            if kk < 0.02:
                continue
            with g.at(dx, 10 * math.sin(t * 2 + i), s * kk):
                _rr(c, -100, -170, 200, 340, 28)
                _shade(c, col, 5, 0.25)
                if i < 3:
                    _rr(c, -70, -140, 140, 100, 6)
                    _shade(c, LCD, 3, 0.05)
                c.new_path()
                c.arc(0, 60 if i < 3 else 0, 66, 0, 2 * math.pi)
                _shade(c, hexc("#f4f5f6"), 3, 0.15)
                c.new_path()
                c.arc(0, 60 if i < 3 else 0, 24, 0, 2 * math.pi)
                _shade(c, col, 3, 0.1)
