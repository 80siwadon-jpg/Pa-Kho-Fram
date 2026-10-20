"""ตัวละครและพร็อพ: เคที เพร์รี (เกิด 25 ต.ค. 1984) — สไตล์ป๊อปทันสมัย: การ์ดสติกเกอร์เงาออฟเซ็ต ไฮไลต์นีออน ลูกกวาด
ไม่วาดหน้าตาคนดังคนอื่น (ไมเคิล แจ็กสัน / บริตนีย์ / อดีตสามี) — ใช้ไอคอน/ข้อความแทน"""
import importlib.util
import math
import os

from gfx import GOLD, GOLD2, GREY, INK, NAVY, RED, WHITE, hexc
from people import Look, _rr, _shade, _smooth_path, _stroke

_spec = importlib.util.spec_from_file_location(
    "wp_chars", os.path.join(os.path.dirname(__file__), "..", "westphalia1648", "chars.py"))
_wp = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_wp)
church = _wp.church

PINK = hexc("#ff4fa3")
MINT = hexc("#3fd6b0")
LEMON = hexc("#ffd84a")
GRAPE = hexc("#8a5cf6")
SKYB = hexc("#4fb3ff")
CANDY = [PINK, MINT, LEMON, GRAPE, SKYB]

# เคที เพร์รี: ผมยาวดำอมม่วงลอนใหญ่ ปากแดง ตาสีฟ้า
KATY = Look(hair="long", hair_col=hexc("#3a1f4a"), outfit="dress", suit=PINK, w=54, jaw=0.25, nose=0.85, brow=0.75,
            age=0.0, height=0.95)
KATY_GOSPEL = Look(hair="long", hair_col=hexc("#6b4a33"), outfit="dress", suit=hexc("#e8e0cc"), w=54, jaw=0.25, brow=0.75,
                   nose=0.85, age=0.0, height=0.88, headsc=1.1)
KATY_LA = Look(hair="long", hair_col=hexc("#1f1a24"), outfit="hoodie", suit=hexc("#5a5f6a"), pants=hexc("#3a4a6a"),
               w=54, jaw=0.25, nose=0.85, brow=0.75, age=0.0, height=0.95)
PASTOR = Look(hair="part", hair_col=hexc("#6a5a4a"), suit=hexc("#2b2622"), collar=WHITE, outfit="tunic",
              pants=hexc("#2b2622"), w=57, age=0.5, glasses="thin")
MOM = Look(hair="bun", hair_col=hexc("#8a6a4a"), outfit="dress", suit=hexc("#5a6a8a"), w=54, age=0.45, height=0.93)
EXECS = [
    Look(hair="slick", hair_col=hexc("#1b1714"), suit=hexc("#2b2622"), tie=hexc("#7a2e2e"), w=57, age=0.5,
         glasses="shades"),
    Look(hair="bald", suit=hexc("#3a3f48"), tie=hexc("#2b2622"), w=58, age=0.6, facial="goatee"),
    Look(hair="part", hair_col=hexc("#9a7a52"), suit=hexc("#4a4038"), tie=hexc("#d9a441"), w=56, age=0.4),
]


def sticker(g, x, y, w, h, fill=WHITE, shadow=PINK, sc=1.0, rot=0.0, r=34, lw=7):
    """การ์ดสติกเกอร์สไตล์ neo-brutal: ขอบดำหนา + เงาสีทึบเยื้อง"""
    with g.at(x, y, sc, rot):
        g.rrect(-w / 2 + 16, -h / 2 + 16, w, h, r, shadow, lw)
        g.rrect(-w / 2, -h / 2, w, h, r, fill, lw)


def confetti(g, t, n=18, seed=0, y0=180, y1=1250, a=0.9):
    """คอนเฟตติพาสเทลลอยช้า ๆ (ของประดับ ไม่บังเนื้อหา)"""
    for i in range(n):
        ph = i * 2.39 + seed
        x = (i * 173 + seed * 61) % 1180 - 50 + 30 * math.sin(t * 0.8 + ph)
        y = y0 + ((i * 97 + t * 60 * (0.5 + (i % 3) * 0.3)) % (y1 - y0))
        col = (*CANDY[i % 5][:3], a)
        with g.at(x, y, 1, t * 90 * (1 if i % 2 else -1) + i * 30):
            if i % 3 == 0:
                g.rrect(-12, -5, 24, 10, 4, col, 0)
            elif i % 3 == 1:
                g.circle(0, 0, 8, col, 0)
            else:
                g.poly([(-9, 7), (9, 7), (0, -9)], col, 0, amp=0)


def mic(g, x, y, sc=1.0, rot=0.0, col=PINK):
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -16, 0, 32, 190, 14)
        _shade(c, hexc("#2b2b30"), 5, 0.2)
        c.new_path()
        c.arc(0, -30, 56, 0, 2 * math.pi)
        _shade(c, hexc("#c9ced6"), 6, 0.3)
        for k in range(-2, 3):
            _stroke(c, [(-46, -30 + k * 16), (46, -30 + k * 16)], 2.5, INK, 0.4, smooth=False)
        _rr(c, -22, 6, 44, 22, 6)
        _shade(c, col, 4, 0.1)


def guitar(g, x, y, sc=1.0, rot=0.0):
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -12, -330, 24, 260, 6)
        _shade(c, hexc("#6e4528"), 4, 0.2)
        _rr(c, -22, -380, 44, 60, 8)
        _shade(c, hexc("#3a2614"), 4, 0)
        _smooth_path(c, [(-80, -90), (-60, -130), (60, -130), (80, -90), (110, 0), (90, 80), (0, 100), (-90, 80),
                         (-110, 0)])
        _shade(c, hexc("#d9a46a"), 6, 0.3)
        g.circle(0, -40, 26, hexc("#3a2614"), 4)
        for k in (-6, 0, 6):
            _stroke(c, [(k, -330), (k, 40)], 1.5, WHITE, 0.8, smooth=False)


def cd(g, x, y, r=110, t=0.0, label="", col=LEMON, spin=True):
    c = g.c
    with g.at(x, y, 1, (t * 120) % 360 if spin else 0):
        c.new_path()
        c.arc(0, 0, r, 0, 2 * math.pi)
        _shade(c, hexc("#dfe4ea"), 6, 0.2)
        for k, a in ((0.85, 0.35), (0.6, 0.25)):
            c.new_path()
            c.arc(0, 0, r * k, 0.3, 1.3)
            c.set_source_rgba(1, 1, 1, a + 0.3)
            c.set_line_width(6)
            c.stroke()
        c.new_path()
        c.arc(0, 0, r * 0.38, 0, 2 * math.pi)
        _shade(c, col, 4, 0.1)
        g.circle(0, 0, r * 0.1, WHITE, 4)
    if label:
        g.label(label, x, y + r + 50, 44)


def contract(g, x, y, sc=1.0, rot=0.0, tear=0.0, logo="LABEL"):
    """สัญญาค่ายเพลง ฉีกเป็นสองท่อน (tear 0..1)"""
    c = g.c
    with g.at(x, y, sc, rot):
        for side in (-1, 1):
            dx = side * 70 * tear
            ang = side * 12 * tear
            with g.at(dx, 30 * tear, 1, ang):
                c.save()
                c.new_path()
                pts = [(0, -220), (-25, -150), (15, -80), (-20, 0), (20, 80), (-15, 160), (0, 220)]
                if side < 0:
                    c.move_to(-160, -220)
                    for p in pts:
                        c.line_to(*p)
                    c.line_to(-160, 220)
                else:
                    c.move_to(160, -220)
                    for p in pts:
                        c.line_to(*p)
                    c.line_to(160, 220)
                c.close_path()
                c.clip()
                _rr(c, -160, -220, 320, 440, 10)
                _shade(c, WHITE, 6, 0.1)
                g.text("CONTRACT", 0, -170, 36, "kanit", INK)
                g.text(logo, 0, -120, 30, "kanit", PINK)
                for i in range(6):
                    _stroke(c, [(-120, -60 + i * 34), (120 - 40 * (i % 2), -60 + i * 34)], 4, INK, 0.35, smooth=False)
                _stroke(c, [(20, 160), (60, 140), (100, 165), (130, 150)], 4, NAVY)
                c.restore()


def car(g, x, y, sc=1.0, tow=0.0, t=0.0):
    """รถเก๋งถูกลากยึด (ยกท้ายเอียง)"""
    c = g.c
    with g.at(x, y, sc, -12 * tow):
        _smooth_path(c, [(-220, -40), (-200, -110), (-110, -120), (-60, -190), (90, -190), (150, -120), (220, -100),
                         (230, -40)])
        _shade(c, SKYB, 6, 0.3)
        _smooth_path(c, [(-50, -180), (80, -180), (130, -125), (-90, -125)])
        _shade(c, hexc("#dff1ff"), 4, 0)
        for wx in (-130, 140):
            c.new_path()
            c.arc(wx, -40, 44, 0, 2 * math.pi)
            _shade(c, hexc("#2b2b30"), 5, 0.1)
            g.circle(wx, -40, 16, hexc("#c9ced6"), 3)
    if tow > 0:
        g.line([(x + 230 * sc, y - 90 * sc), (x + 420 * sc, y - 300 * sc)], 8, INK, amp=0)


def bill(g, x, y, sc=1.0, rot=0.0, t=0.0):
    """ใบแจ้งค่าเช่า ตัวแดง"""
    with g.at(x, y, sc, rot):
        g.rrect(-150, -190, 300, 380, 12, WHITE, 6)
        g.text("RENT", 0, -130, 52, "kanit", INK)
        g.text("$$$", 0, -40, 70, "kanit", RED)
        g.rrect(-110, 60, 220, 70, 14, (1, 1, 1, 0), 6, stroke=RED)
        g.text("OVERDUE", 0, 95, 34, "kanit", RED)


def chart(g, x, y, sc=1.0, k=1.0, t=0.0, n=5):
    """อันดับ 1 บิลบอร์ด 5 เพลง (การ์ดซ้อนเด้งขึ้นทีละใบ)"""
    titles = ["California Gurls", "Teenage Dream", "Firework", "E.T.", "Last Friday Night"]
    with g.at(x, y, sc):
        for i in range(n):
            kk = max(0.0, min(1.0, k * n - i))
            if kk < 0.02:
                continue
            yy = -300 + i * 140
            with g.at(0, yy, 0.6 + 0.4 * kk, 0):
                sticker(g, 0, 0, 640, 110, WHITE, CANDY[i % 5], 1.0, 0, 26, 6)
                g.circle(-260, 0, 38, LEMON, 5)
                g.text("#1", -260, 0, 40, "kanit", INK)
                g.text(titles[i], 50, 0, 44, "kanit", INK)


def crown(g, x, y, sc=1.0, rot=0.0, col=GOLD):
    with g.at(x, y, sc, rot):
        g.poly([(-100, 50), (-100, -40), (-50, 10), (0, -70), (50, 10), (100, -40), (100, 50)], col, 6, amp=0)
        for px, pc in ((-50, PINK), (0, MINT), (50, SKYB)):
            g.circle(px, 25, 14, pc, 4)


def glove(g, x, y, sc=1.0, rot=0.0, t=0.0):
    """ถุงมือประกายข้างเดียว (ไอคอนราชาเพลงป๊อป)"""
    c = g.c
    with g.at(x, y, sc, rot):
        _smooth_path(c, [(-70, 120), (-80, -20), (-90, -120), (-60, -130), (-40, -40), (-30, -160), (0, -165),
                         (10, -50), (25, -150), (55, -145), (50, -40), (75, -110), (100, -100), (80, 30), (60, 120)])
        _shade(c, hexc("#f4f6fa"), 6, 0.25)
        for i in range(16):
            px, py = -60 + (i * 37) % 130, -100 + (i * 53) % 200
            g.circle(px, py, 4, hexc("#c9ced6"), 0)
        g.sparkle(70, -130, 26 * (0.7 + 0.3 * math.sin(t * 5)))


def lollipop(g, x, y, sc=1.0, rot=0.0, t=0.0, col=PINK):
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -7, 0, 14, 200, 6)
        _shade(c, WHITE, 4, 0.1)
        c.new_path()
        c.arc(0, -70, 80, 0, 2 * math.pi)
        _shade(c, col, 6, 0.2)
        for k in range(3):
            g.arc(0, -70, 20 + 18 * k, t * 90 + k * 60, t * 90 + k * 60 + 200, 7, (1, 1, 1, 0.8))


def cupcake(g, x, y, sc=1.0, t=0.0):
    c = g.c
    with g.at(x, y, sc):
        _smooth_path(c, [(-80, -80), (80, -80), (60, 40), (-60, 40)])
        _shade(c, hexc("#c9915a"), 6, 0.2)
        for k in range(-3, 4):
            _stroke(c, [(k * 20, -78), (k * 16, 38)], 3, INK, 0.3, smooth=False)
        _smooth_path(c, [(-95, -80), (-90, -130), (-40, -170), (0, -210), (40, -170), (90, -130), (95, -80)])
        _shade(c, PINK, 6, 0.2)
        g.circle(0, -215, 18, RED, 4)
        for i in range(6):
            g.rrect(-60 + i * 22, -140 + 12 * (i % 2), 12, 5, 2, CANDY[(i + 1) % 5], 0)


def phone(g, x, y, sc=1.0, rot=0.0, msg="", buzz=0.0, t=0.0):
    c = g.c
    with g.at(x + 6 * buzz * math.sin(t * 50), y, sc, rot):
        _rr(c, -110, -210, 220, 420, 30)
        _shade(c, hexc("#2b2b30"), 6, 0.2)
        _rr(c, -95, -185, 190, 370, 18)
        _shade(c, hexc("#f4f6fa"), 3, 0)
        if msg:
            g.rrect(-80, -120, 160, 80, 18, hexc("#dfe6ef"), 3)
            g.text(msg, 0, -80, 30, "kanit", INK)
            for k in range(2):
                g.rrect(-80, -20 + k * 40, 140 - 40 * k, 22, 10, hexc("#dfe6ef"), 0)


def spotlight(g, x, y, t=0.0, k=1.0, col=(1, 0.95, 0.7)):
    c = g.c
    if k <= 0:
        return
    c.new_path()
    c.move_to(x - 30, y)
    c.line_to(x + 30, y)
    c.line_to(x + 260, 1270)
    c.line_to(x - 260, 1270)
    c.close_path()
    c.set_source_rgba(*col, 0.35 * k)
    c.fill()


def curtain(g, open_=0.0, t=0.0):
    """ม่านเวทีแดงสองข้าง (open_ 1 = เปิดสุด)"""
    for sx in (-1, 1):
        w = 560 * (1 - 0.75 * open_)
        x0 = -300 if sx < 0 else 1380 - w
        with g.at(0, 0):
            g.rrect(x0, 140, w, 1130, 0, hexc("#c0283a"), 6)
            for k in range(6):
                xx = x0 + w * (k + 0.5) / 6
                g.line([(xx, 160), (xx + 10 * math.sin(t + k), 1250)], 4, (0.5, 0.05, 0.1, 0.5), amp=0)


def tear_drops(g, x, y, t, k=1.0):
    for i in range(2):
        u = (t * 0.8 + i * 0.5) % 1
        with g.at(x + 20 * i, y + 120 * u, 0.6 * k):
            g.poly([(0, -24), (16, 6), (0, 20), (-16, 6)], (0.45, 0.7, 1, 1 - u), 3, amp=0, smooth=True)


def suitcase(g, x, y, sc=1.0, rot=0.0):
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -130, -180, 260, 180, 20)
        _shade(c, PINK, 6, 0.3)
        _rr(c, -45, -220, 90, 50, 14)
        _shade(c, (0, 0, 0, 0), 6, 0)
        for sx in (-80, 80):
            _stroke(c, [(sx, -180), (sx, 0)], 6, INK, 0.5, smooth=False)
        g.circle(-30, -100, 22, LEMON, 4)
        g.star(40, -100, 24, MINT, 4)


def hollywood(g, y, t=0.0):
    """เนินเขากับป้ายตัวอักษร LA (ไม่ใช้ป้ายจริง)"""
    c = g.c
    _smooth_path(c, [(-400, y), (-300, y - 300), (200, y - 420), (700, y - 340), (1500, y - 260), (1500, y)])
    _shade(c, hexc("#d9c27a"), 6, 0.2)
    for i in range(3):
        x = 80 + i * 380
        g.line([(x, y), (x + 10, y - 360)], 10, hexc("#6e4528"), amp=0)
        for k in range(5):
            a = -2.4 + k * 0.45 + 0.05 * math.sin(t * 2 + i)
            g.line([(x + 10, y - 360), (x + 10 + 120 * math.cos(a), y - 360 + 80 * math.sin(a) + 60)], 12,
                   hexc("#3c8d4f"), amp=0)
    for i, ch in enumerate("LOS ANGELES"):
        if ch != " ":
            g.label(ch, 130 + i * 80, y - 250 + 12 * math.sin(i), 70)
