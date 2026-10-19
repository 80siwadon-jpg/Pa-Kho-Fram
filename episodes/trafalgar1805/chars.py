"""ตัวละครและพร็อพ: ยุทธนาวีทราฟัลการ์ 21 ต.ค. 1805 — คนแบบกึ่งเสมือนจริงจาก src/people.py"""
import math

import cairo

from gfx import BROWN, BROWN2, GOLD, GOLD2, GREY, ICE, INK, LGREY, NAVY, RED, WHITE, hexc, hn
from people import Look, _rr, _shade, _smooth_path, _stroke

GOLDC = hexc("#e3a92b")
RN_BLUE = hexc("#1f2b4a")
FR_BLUE = hexc("#2b3f8a")
SEA = hexc("#bcd8ec")
SEA2 = hexc("#8fb8de")

# โฮราทิโอ เนลสัน: ร่างเล็ก ผมเทาขาวปัดหน้า หน้าผอม จมูกโด่ง แขนขวาด้วน (แขนเสื้อพับกลัดที่อก)
# โค้ตพลเรือเอกสีกรมท่า อินทรธนูทอง ดาวเครื่องราชฯ 4 ดวงที่อกซ้าย หมวกสองแฉกขอบทอง
NELSON = Look(hair="nelson", hair_col=hexc("#d9d5cc"), suit=RN_BLUE, pants=WHITE, shoes=hexc("#1b1916"),
              outfit="naval", hat="bicorne", hat_trim=GOLDC, epaulettes=True, stars=4, empty_arm=-1, w=54,
              jaw=0.2, nose=1.35, brow=0.8, age=0.7, build=0.85, height=0.95)
# นโปเลียน: ผมดำสั้นปอยหน้าม้า หมวกสองแฉกดำสวมขวาง โค้ตเขียวปกแดง เสื้อกั๊กขาว มือสอดในเสื้อ
NAPOLEON = Look(hair="napoleon", hair_col=hexc("#2b2622"), suit=hexc("#2f5a3a"), collar=hexc("#b8473a"),
                pants=WHITE, shoes=hexc("#1b1916"), outfit="naval", hat="bicorne", epaulettes=True, stars=1,
                w=60, jaw=0.5, nose=1.1, brow=1.0, age=0.3, build=1.0, height=0.9)
# โทมัส ฮาร์ดี: กัปตันเรือวิกตอรี ร่างสูงใหญ่
HARDY = Look(hair="short", hair_col=hexc("#6b4a33"), suit=RN_BLUE, pants=WHITE, shoes=hexc("#1b1916"),
             outfit="naval", hat="bicorne", epaulettes=True, w=60, jaw=0.6, nose=1.1, age=0.4, build=1.12,
             height=1.08)
SAILORS = [
    Look(hair="short", hair_col=hexc("#6b4a33"), suit=WHITE, pants=hexc("#e9e2d4"), shoes=hexc("#1b1916"),
         outfit="stripe", w=58, age=0.2),
    Look(hair="short", hair_col=hexc("#2b2622"), suit=WHITE, pants=hexc("#e9e2d4"), shoes=hexc("#1b1916"),
         outfit="stripe", w=58, age=0.3, skin=hexc("#d9a37e")),
    Look(hair="buzz", hair_col=hexc("#a8763e"), suit=WHITE, pants=hexc("#e9e2d4"), shoes=hexc("#1b1916"),
         outfit="stripe", w=58, age=0.1),
]


# ---------------------------------------------------------------- เรือ
def ship(g, x, y, sc=1.0, side="uk", t=0.0, flip=False, sails=1.0, damage=0.0, fire=False, bob=True):
    """เรือรบสามชั้นปืน (ship of the line) มองด้านข้าง — x,y = กลางแนวน้ำ
    side: uk (ลายตารางดำ-เหลือง "Nelson chequer") / fr / es"""
    c = g.c
    by = 6 * math.sin(t * 1.8 + x * 0.01) if bob else 0
    rock = 1.2 * math.sin(t * 1.3 + x * 0.02) if bob else 0
    with g.at(x, y + by, sc, rock, sx=-sc if flip else sc, sy=sc):
        hull_col = {"uk": hexc("#2a2622"), "fr": hexc("#3a3330"), "es": hexc("#5a2a22")}[side]
        stripe = {"uk": hexc("#d9a441"), "fr": hexc("#b8473a"), "es": hexc("#d9a441")}[side]
        # เสากระโดง 3 ต้น + ใบเรือ
        for mx, mh in ((-170, 520), (0, 600), (170, 470)):
            g.line([(mx, -110), (mx, -110 - mh * (1 - 0.25 * damage * (mx == 170)))], 10, hexc("#6e4528"), amp=0)
            for k in range(3):
                sw = (120 - k * 22) * sails
                sy0 = -150 - k * mh * 0.3
                if sw > 4:
                    _smooth_path(c, [(mx - sw, sy0), (mx + sw, sy0), (mx + sw * 0.92, sy0 - mh * 0.24), (mx - sw * 0.92, sy0 - mh * 0.24)])
                    _shade(c, hexc("#f4efe2"), 4, 0.15)
                    if damage > 0.3 and k == 1:
                        g.circle(mx + 30, sy0 - mh * 0.12, 12 * damage, hexc("#cfc6b2"), 0)
        # ธงท้ายเรือ
        fx = -300
        g.line([(fx, -110), (fx - 30, -240)], 6, hexc("#6e4528"), amp=0)
        with g.at(fx - 30, -240):
            wv = 6 * math.sin(t * 6)
            if side == "uk":
                _rr(c, -110, 0, 110, 70, 2)
                _shade(c, WHITE, 3, 0)
                g.line([(-110, 35), (0, 35)], 14, RED, amp=0)
                g.line([(-55, 0), (-55, 70)], 14, RED, amp=0)
                _rr(c, -110, 0, 50, 32, 1)   # มุมธงยูเนียน (White Ensign)
                _shade(c, hexc("#2b3f63"), 2, 0)
                g.line([(-110, 0), (-60, 32)], 4, WHITE, amp=0)
                g.line([(-60, 0), (-110, 32)], 4, WHITE, amp=0)
            elif side == "fr":
                for i, col in enumerate((hexc("#2b3f8a"), WHITE, hexc("#c8553d"))):
                    _rr(c, -110 + i * 36.7, wv * 0.2, 36.7, 70, 1)
                    _shade(c, col, 2, 0)
                c.new_path()
                c.rectangle(-110, 0, 110, 70)
                c.set_source_rgba(*INK)
                c.set_line_width(3)
                c.stroke()
            else:
                for i, col in enumerate((hexc("#c8553d"), GOLD2, hexc("#c8553d"))):
                    _rr(c, -110, i * 23, 110, 24 if i != 1 else 23, 1)
                    _shade(c, col, 2, 0)
        # ตัวเรือ
        _smooth_path(c, [(-340, -130), (330, -130), (380, -170), (350, -60), (280, 40), (-280, 40), (-330, -40)])
        _shade(c, hull_col, 6, 0.3)
        for k in range(3):   # แถบสีพร้อมช่องปืน 3 ชั้น
            yy = -110 + k * 46
            _stroke(c, [(-320 + k * 14, yy), (330 - k * 30, yy)], 18, stripe, smooth=False)
            for i in range(11):
                gx = -280 + i * 54 + k * 6
                if gx > 300 - k * 30:
                    continue
                _rr(c, gx, yy - 8, 18, 16, 2)
                _shade(c, INK, 0, 0)
                if fire and int(t * 6 + i + k) % 7 == 0:   # แสงวาบปากกระบอก
                    g.circle(gx - 20, yy, 26, (1, 0.85, 0.4, 0.9), 0)
        _rr(c, -300, -150, 120, 24, 6)
        _shade(c, hexc("#6e4528"), 4, 0.2)


def ship_icon(g, x, y, s, side="uk", rot=0.0, t=0.0):
    """เรือมองจากด้านบน (แผนที่ยุทธวิธี)"""
    col = {"uk": hexc("#2a2622"), "fr": hexc("#2b3f8a"), "es": hexc("#b8473a")}[side]
    with g.at(x, y, s, rot):
        _smooth_path(g.c, [(-46, 0), (-30, -14), (36, -14), (56, 0), (36, 14), (-30, 14)])
        _shade(g.c, col, 3.5, 0.2)
        g.line([(-20, 0), (30, 0)], 3, WHITE, amp=0)


def sea(g, y0, t, y1=1300, col=SEA):
    """ทะเล: แถบสีฟ้าอ่อน + คลื่นเส้นโค้ง (กว้างเกินขอบเผื่อกล้องแพน)"""
    c = g.c
    c.new_path()
    c.move_to(-3000, y1)
    for xx in range(-3000, 4100, 60):
        c.line_to(xx, y0 + 10 * math.sin(xx * 0.012 + t * 1.6))
    c.line_to(4100, y1)
    c.close_path()
    gr = cairo.LinearGradient(0, y0, 0, y1)
    gr.add_color_stop_rgba(0, *col[:3], 1)
    gr.add_color_stop_rgba(1, *SEA2[:3], 1)
    c.set_source(gr)
    c.fill_preserve()
    c.set_source_rgba(*INK)
    c.set_line_width(5)
    c.stroke()
    for i in range(14):
        wx = (i * 173 + t * 40) % 1500 - 200
        wy = y0 + 50 + (i * 61) % max(60, int(y1 - y0 - 70))
        _stroke(c, [(wx - 40, wy), (wx - 20, wy - 10), (wx, wy), (wx + 20, wy - 10), (wx + 40, wy)], 4, WHITE, 0.8)


def smoke(g, x, y, t, n=5, s=1.0, col=None):
    for i in range(n):
        p = (t * 0.35 + i / n) % 1
        with g.alpha(math.sin(p * math.pi) * 0.85):
            g.blob(x + 30 * hn(i, 2) + 40 * p, y - 240 * p, (40 + 46 * p) * s, (34 + 40 * p) * s, col or LGREY, 0, i)


def signal_flags(g, x0, y0, x1, y1, n, t, k=1.0):
    """ธงสัญญาณเรียงบนเชือก (k = สัดส่วนที่ชักขึ้นแล้ว)"""
    cols = [(hexc("#c8553d"), GOLD2), (hexc("#2b3f8a"), WHITE), (GOLD2, hexc("#2b3f8a")), (WHITE, hexc("#c8553d")),
            (hexc("#1b1916"), GOLD2)]
    g.line([(x0, y0), (x1, y1)], 3, amp=0)
    m = int(n * k)
    for i in range(m):
        u = (i + 0.5) / n
        fx, fy = x0 + (x1 - x0) * u, y0 + (y1 - y0) * u
        a, b = cols[i % len(cols)]
        sw = 4 * math.sin(t * 5 + i)
        _rr(g.c, fx - 22, fy + 4, 44, 40 + sw, 2)
        _shade(g.c, a, 3, 0)
        _rr(g.c, fx - 22, fy + 4, 22, 20, 1)
        _shade(g.c, b, 0, 0)


def cannonball(g, x, y, r=16):
    g.circle(x, y, r, INK, 0)
    g.circle(x - r * 0.3, y - r * 0.3, r * 0.3, GREY, 0)


def lantern(g, x, y, sc=1.0, t=0.0):
    with g.at(x, y, sc):
        rg = cairo.RadialGradient(0, 60, 0, 0, 60, 420)
        rg.add_color_stop_rgba(0, 1, 0.85, 0.45, 0.45 + 0.05 * math.sin(t * 7))
        rg.add_color_stop_rgba(1, 1, 0.85, 0.45, 0)
        g.c.set_source(rg)
        g.c.arc(0, 60, 420, 0, 2 * math.pi)
        g.c.fill()
        g.line([(0, -60), (0, 0)], 4, amp=0)
        _rr(g.c, -36, 0, 72, 110, 14)
        _shade(g.c, GOLD2, 5, 0.2)
        g.circle(0, 55, 16, hexc("#f4a63a"), 0)


def europe_map(g, t, x0=60, x1=1020, y0=360, y1=1180, napoleon_k=0.0, army=0.0, trafalgar=0.0):
    """แผนที่สัญลักษณ์: อังกฤษ / ฝรั่งเศส / สเปน + แหลมทราฟัลการ์"""
    c = g.c
    _rr(c, x0, y0, x1 - x0, y1 - y0, 30)
    _shade(c, SEA, 7, 0.0)
    c.save()
    _rr(c, x0 + 4, y0 + 4, x1 - x0 - 8, y1 - y0 - 8, 28)
    c.clip()
    land = hexc("#efe4c8")
    # อังกฤษ
    _smooth_path(c, [(380, 380), (450, 400), (470, 470), (500, 540), (470, 600), (380, 610), (330, 560), (360, 480)])
    _shade(c, hexc("#f3dccb"), 5, 0.1)
    # ฝรั่งเศส + ยุโรป
    _smooth_path(c, [(420, 680), (560, 650), (800, 600), (1100, 560), (1100, 1000), (760, 900), (620, 880), (500, 840), (430, 760)])
    _shade(c, land, 5, 0.1)
    # สเปน
    _smooth_path(c, [(230, 880), (480, 860), (560, 900), (540, 1060), (420, 1130), (260, 1110), (200, 1000)])
    _shade(c, hexc("#ecd9b0"), 5, 0.1)
    c.restore()
    g.label("อังกฤษ", 420, 500, 44)
    g.label("ฝรั่งเศส", 700, 760, 44)
    g.label("สเปน", 380, 990, 44)
    if army > 0:   # กองทัพนโปเลียนริมฝั่ง (บูโลญ)
        for i in range(8):
            g.circle(470 + (i % 4) * 26, 690 + (i // 4) * 26, 11 * army, hexc("#2b3f8a"), 3)
        g.line([(520, 670), (480, 600)], 8 * army, RED, amp=0)
        g.poly([(468, 590), (500, 610), (470, 630)], RED, 0) if army > 0.5 else None
    if trafalgar > 0:
        g.circle(250, 1100, 22 * trafalgar, RED, 5)
        g.label("แหลมทราฟัลการ์", 330, 1160, 40, color=RED, sc=trafalgar)
