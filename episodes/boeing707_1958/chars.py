"""ตัวละครและพร็อพ: เที่ยวบินโบอิ้ง 707 ข้ามแอตแลนติกเที่ยวแรกของแพนแอม (26 ต.ค. 1958)
ไม่ใช้โลโก้จริงของแพนแอม/โบอิ้ง — เขียนเป็นตัวหนังสือธรรมดาบนลำตัว"""
import math

from gfx import GOLD, GOLD2, GREY, INK, NAVY, RED, WHITE, hexc, hn
from people import Look, _rr, _shade, _smooth_path, _stroke

PA_BLUE = hexc("#1f5fa8")
SKY = hexc("#cfe6f5")
SEA = hexc("#bcd6e6")
LAND = hexc("#d9c48f")
METAL = hexc("#e9ecf0")

PILOT = Look(hair="part", hair_col=hexc("#5a4632"), suit=NAVY, tie=INK, w=58, jaw=0.6, age=0.5,
             hat="peaked", hat_trim=GOLD, epaulettes=True)
HOSTESS = Look(hair="bun", hair_col=hexc("#8a5a2a"), outfit="dress", suit=PA_BLUE, w=54, age=0.1, height=0.93,
               hat="garrison", hat_trim=PA_BLUE)
PAX = [
    Look(hair="part", hair_col=hexc("#3a2f28"), suit=hexc("#5a4a3a"), tie=hexc("#7a2e2e"), w=58, age=0.5,
         hat="porkpie", hat_trim=hexc("#4a3a2a")),
    Look(hair="bun", hair_col=hexc("#c99a52"), outfit="dress", suit=hexc("#c8553d"), w=54, age=0.2, height=0.93),
    Look(hair="slick", hair_col=hexc("#1b1714"), suit=hexc("#3a3f48"), tie=hexc("#2b3f63"), w=57, age=0.3,
         glasses="thick"),
    Look(hair="bun", hair_col=hexc("#2b2622"), outfit="dress", suit=hexc("#3c8d4f"), w=54, age=0.3, height=0.93),
    Look(hair="bowl" if False else "short", hair_col=hexc("#8a6a42"), suit=hexc("#2b4f6a"), tie=GOLD2, w=56,
         age=0.1, bowtie=True),
]
RICH = Look(hair="bald", suit=hexc("#1d1d21"), tie=INK, w=60, jaw=0.7, jowls=0.3, age=0.8, hat="tophat",
            facial="mustache", build=1.2)


def jet(g, x, y, sc=1.0, rot=0.0, t=0.0, flip=False, trail=0.0, txt="PAN AMERICAN"):
    """โบอิ้ง 707 มองด้านข้าง หันขวา: ปีกลู่ เครื่องยนต์ไอพ่นใต้ปีก 4 ตัว (เห็นด้านหน้า 2 ตัว)"""
    c = g.c
    s = -sc if flip else sc
    with g.at(x, y, sc, rot, sx=s, sy=sc):
        if trail > 0:   # ไอพ่นเป็นทางยาว
            for k in range(2):
                yy = 40 + k * 26
                _rr(c, -380 - 600 * trail, yy - 8, 600 * trail, 16, 8)
                c.set_source_rgba(0.75, 0.82, 0.9, 0.55)
                c.fill()
        _smooth_path(c, [(-150, 10), (-250, 70), (-210, 80), (-30, 50)])   # ปีกฝั่งไกล
        _shade(c, hexc("#c9ced6"), 5, 0.2)
        _smooth_path(c, [(-330, -40), (-420, -200), (-370, -200), (-250, -40)])   # แพนหาง
        _shade(c, METAL, 6, 0.25)
        c.new_path()
        c.move_to(-400, -175)
        c.line_to(-372, -175)
        c.line_to(-300, -50)
        c.line_to(-330, -50)
        c.close_path()
        c.set_source_rgba(*PA_BLUE)
        c.fill()
        g.text("707", -350, -110, 30, "kanit", WHITE, rot=-58)
        c.new_path()   # ลำตัว
        c.move_to(-390, -30)
        c.curve_to(-300, -62, -100, -62, 250, -60)
        c.curve_to(330, -60, 380, -40, 400, 0)
        c.curve_to(380, 30, 330, 40, 250, 40)
        c.line_to(-280, 40)
        c.curve_to(-340, 40, -380, 10, -390, -30)
        c.close_path()
        _shade(c, METAL, 6, 0.3, horiz=False)
        c.save()
        c.move_to(-390, -30)
        c.curve_to(-300, -62, -100, -62, 250, -60)
        c.curve_to(330, -60, 380, -40, 400, 0)
        c.curve_to(380, 30, 330, 40, 250, 40)
        c.line_to(-280, 40)
        c.close_path()
        c.clip()
        c.rectangle(-420, -12, 840, 14)   # แถบสีน้ำเงินคาดลำตัว
        c.set_source_rgba(*PA_BLUE)
        c.fill()
        c.restore()
        for i in range(16):
            g.circle(-270 + i * 30, -28, 7, SKY, 2.5)
        _smooth_path(c, [(330, -40), (362, -40), (380, -22), (346, -22)])   # กระจกห้องนักบิน
        _shade(c, hexc("#2b3f63"), 3, 0)
        g.text(txt, -20, -46, 22, "kanit", PA_BLUE)
        _smooth_path(c, [(-110, 20), (-10, 20), (-200, 150), (-250, 150)])   # ปีกฝั่งใกล้ (ลู่หลัง)
        _shade(c, hexc("#d9dde3"), 6, 0.25)
        for ex, ey in ((-60, 60), (-170, 120)):   # เครื่องยนต์ไอพ่น 2 ตัว (ฝั่งใกล้)
            _rr(c, ex - 30, ey - 18, 110, 36, 18)
            _shade(c, hexc("#c3c9d1"), 5, 0.3)
            c.new_path()
            c.save()
            c.translate(ex + 80, ey)
            c.scale(0.4, 1)
            c.arc(0, 0, 16, 0, 2 * math.pi)
            c.restore()
            _shade(c, hexc("#3a3f48"), 3, 0)


def propliner(g, x, y, sc=1.0, rot=0.0, t=0.0, shake=1.0):
    """เครื่องบินใบพัดยุค 1950 (หางสามแฉกแบบ Constellation) เสียงดัง สั่น"""
    c = g.c
    jx = shake * 4 * math.sin(t * 37)
    jy = shake * 4 * math.sin(t * 29 + 1)
    with g.at(x + jx, y + jy, sc, rot + shake * 1.2 * math.sin(t * 23)):
        for dx in (-330, -380, -430):   # หางสามแฉก
            _smooth_path(c, [(dx + 10, -10), (dx - 10, -120), (dx + 30, -120), (dx + 40, -10)])
            _shade(c, hexc("#d9dde3"), 5, 0.2)
        c.new_path()   # ลำตัวโค้งแบบปลาโลมา
        c.move_to(-440, -40)
        c.curve_to(-200, -40, 0, -70, 250, -55)
        c.curve_to(330, -50, 370, -20, 380, 5)
        c.curve_to(360, 30, 300, 40, 220, 40)
        c.curve_to(0, 45, -200, 20, -440, -10)
        c.close_path()
        _shade(c, hexc("#e4e7eb"), 6, 0.3, horiz=False)
        _rr(c, -360, -18, 680, 10, 5)
        c.set_source_rgba(*RED)
        c.fill()
        for i in range(10):
            _rr(c, -200 + i * 45, -42, 22, 18, 6)
            _shade(c, SKY, 2.5, 0)
        _smooth_path(c, [(-60, 10), (60, 10), (20, 150), (-30, 150)])
        _shade(c, hexc("#cfd4da"), 5, 0.2)
        for ex, ey in ((40, 30), (25, 100)):   # เครื่องยนต์ลูกสูบ + ใบพัด
            _rr(c, ex - 40, ey - 18, 90, 36, 14)
            _shade(c, hexc("#b8bec8"), 4, 0.3)
            a = t * 50
            for k in range(3):
                ang = a + k * 2.094
                _stroke(c, [(ex + 55, ey), (ex + 55 + 8 * math.cos(ang), ey + 62 * math.sin(ang))], 7, INK,
                        smooth=False)
            g.circle(ex + 55, ey, 9, GREY, 3)


def noise_lines(g, x, y, t, k=1.0, n=3):
    """เส้นคลื่นเสียงดัง"""
    for i in range(n):
        u = (t * 1.8 + i / n) % 1
        g.arc(x, y, 60 + 120 * u, -40, 40, 8, (*INK[:3], (1 - u) * k))


def cloud(g, x, y, s=1.0, col=WHITE, lw=6):
    with g.at(x, y, s):
        for dx, dy, r in ((-80, 15, 55), (0, -20, 75), (85, 10, 58), (0, 30, 60)):
            g.circle(dx, dy, r, col, lw)
        for dx, dy, r in ((-80, 15, 55), (0, -20, 75), (85, 10, 58), (0, 30, 60)):
            g.circle(dx, dy, r - lw / 2, col, 0)


def storm(g, x, y, s=1.0, t=0.0):
    """เมฆฝนฟ้าคะนอง (สภาพอากาศแปรปรวน)"""
    cloud(g, x, y, s, hexc("#9aa3ad"))
    with g.at(x, y, s):
        if math.sin(t * 5) > 0.3:
            g.poly([(0, 40), (40, 40), (10, 110), (50, 110), (-20, 230), (5, 135), (-30, 135)], GOLD2, 5)
        for i in range(6):
            u = (t * 1.5 + i / 6) % 1
            g.line([(-90 + i * 36, 70 + 120 * u), (-100 + i * 36, 100 + 120 * u)], 5, (*PA_BLUE[:3], 1 - u), amp=0)


def atlantic(g, x, y, w, h, k=0.0, t=0.0, plane_sc=0.18, labels=True):
    """แผนที่แอตแลนติกเหนือ: นิวยอร์ก → ปารีส เส้นทางโค้ง k = 0..1"""
    c = g.c
    with g.at(x, y):
        _rr(c, -w / 2, -h / 2, w, h, 30)
        _shade(c, SEA, 7, 0.1)
        c.save()
        _rr(c, -w / 2, -h / 2, w, h, 30)
        c.clip()
        g.blob(-w / 2 + 40, 40, w * 0.22, h * 0.5, LAND, 5, seed=4)   # อเมริกาเหนือ
        g.blob(w / 2 - 20, -10, w * 0.2, h * 0.45, LAND, 5, seed=8)   # ยุโรป
        for i in range(6):   # คลื่น
            wx = -w / 2 + 120 + (i * 137 + t * 30) % (w - 200)
            wy = -h / 2 + 60 + (i * 89) % (h - 120)
            g.arc(wx, wy, 18, 200, 340, 4, (1, 1, 1, 0.8))
        c.restore()
        p0 = (-w / 2 + 120, 30)
        p1 = (w / 2 - 110, -10)
        cx, cy = 0, -h / 2 - 20

        def bez(u):
            return ((1 - u) ** 2 * p0[0] + 2 * (1 - u) * u * cx + u * u * p1[0],
                    (1 - u) ** 2 * p0[1] + 2 * (1 - u) * u * cy + u * u * p1[1])
        n = 30
        for i in range(n):
            u0, u1 = i / n, (i + 0.5) / n
            if u1 > k:
                break
            g.line([bez(u0), bez(u1)], 8, RED, amp=0)
        g.circle(*p0, 16, RED, 5)
        g.circle(*p1, 16, RED if k >= 0.99 else WHITE, 5)
        if labels:
            g.label("นิวยอร์ก", p0[0] + 10, p0[1] + 70, 46)
            g.label("ปารีส", p1[0] - 10, p1[1] + 70, 46)
        if 0 < k < 1:
            px, py = bez(k)
            qx, qy = bez(min(1, k + 0.01))
            ang = math.degrees(math.atan2(qy - py, qx - px))
            jet(g, px, py, plane_sc, ang, t)


def clock(g, x, y, r, hrs, t=0.0, col=RED, label=""):
    """นาฬิกา เข็มหมุนตามจำนวนชั่วโมง hrs + วงชั่วโมงสะสม"""
    c = g.c
    with g.at(x, y):
        g.circle(0, 0, r, WHITE, 8)
        frac = min(hrs, 12) / 12
        if frac > 0:
            c.new_path()
            c.move_to(0, 0)
            c.arc(0, 0, r - 12, -math.pi / 2, -math.pi / 2 + 2 * math.pi * frac)
            c.close_path()
            c.set_source_rgba(*col[:3], 0.25)
            c.fill()
        if hrs > 12:
            c.new_path()
            c.arc(0, 0, r + 14, -math.pi / 2, -math.pi / 2 + 2 * math.pi * (hrs - 12) / 12)
            c.set_source_rgba(*col)
            c.set_line_width(14)
            c.stroke()
        for i in range(12):
            a = i * math.pi / 6
            g.line([(0.8 * r * math.sin(a), -0.8 * r * math.cos(a)), (0.9 * r * math.sin(a), -0.9 * r * math.cos(a))],
                   6, INK, amp=0)
        a = 2 * math.pi * hrs
        g.line([(0, 0), (0.75 * r * math.sin(a), -0.75 * r * math.cos(a))], 8, INK, amp=0)
        a = 2 * math.pi * hrs / 12
        g.line([(0, 0), (0.5 * r * math.sin(a), -0.5 * r * math.cos(a))], 12, INK, amp=0)
        g.circle(0, 0, 12, col, 0)
        if label:
            g.label(label, 0, r + 70, 64, color=col)


def liner(g, x, y, sc=1.0, t=0.0):
    """เรือเดินสมุทร 3 ปล่อง"""
    c = g.c
    with g.at(x, y + 6 * math.sin(t * 1.5), sc, 1.2 * math.sin(t * 1.1)):
        _smooth_path(c, [(-340, -90), (320, -90), (380, -150), (280, 30), (-300, 30), (-350, -40)])
        _shade(c, hexc("#2b2f3a"), 6, 0.2)
        _rr(c, -280, -160, 520, 70, 6)
        _shade(c, WHITE, 5, 0.15)
        for i in range(10):
            g.circle(-240 + i * 50, -125, 8, SKY, 2.5)
        for i in range(3):
            _rr(c, -170 + i * 130, -260, 70, 100, 8)
            _shade(c, RED, 5, 0.2)
            _rr(c, -170 + i * 130, -260, 70, 26, 8)
            _shade(c, INK, 0, 0)
            for k in range(3):
                u = (t * 0.6 + k / 3 + i * 0.2) % 1
                g.circle(-135 + i * 130 - 60 * u, -290 - 120 * u, 20 + 30 * u, (0.8, 0.8, 0.82, 1 - u), 0)


def sea(g, y, t, x0=-600, x1=1700, h=None):
    c = g.c
    if h is None:
        h = max(20, 1420 - y)   # ไม่ลงไปในพื้นที่ล่าง 15% ของจอ
    c.new_path()
    c.move_to(x0, y)
    for i in range(int((x1 - x0) / 20) + 1):
        xx = x0 + i * 20
        c.line_to(xx, y + 10 * math.sin(xx * 0.02 + t * 2))
    c.line_to(x1, y + h)
    c.line_to(x0, y + h)
    c.close_path()
    _shade(c, SEA, 5, 0.15)


def tower(g, x, y, sc=1.0, t=0.0):
    """หอบังคับการบินสนามบิน"""
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -40, -380, 80, 380, 6)
        _shade(c, hexc("#e8dcc0"), 5, 0.25)
        _smooth_path(c, [(-110, -380), (110, -380), (90, -470), (-90, -470)])
        _shade(c, hexc("#9ad0f5"), 5, 0.1)
        _rr(c, -120, -500, 240, 34, 8)
        _shade(c, hexc("#3a3f48"), 5, 0.1)
        g.circle(0, -520, 14, (1, 0.3, 0.3, 0.6 + 0.4 * math.sin(t * 6)), 3)


def runway(g, y, t=0.0, x0=-600, x1=1700, speed=0.0):
    c = g.c
    c.rectangle(x0, y, x1 - x0, 90)
    c.set_source_rgba(0.55, 0.57, 0.6, 1)
    c.fill()
    for i in range(14):
        xx = x0 + ((i * 180 - t * speed) % (x1 - x0))
        c.rectangle(xx, y + 38, 100, 14)
        c.set_source_rgba(1, 1, 1, 1)
        c.fill()
    _stroke(c, [(x0, y), (x1, y)], 6, INK, smooth=False)


def cabin(g, x, y, sc=1.0, t=0.0, calm=True):
    """ห้องโดยสารหรู: หน้าต่างวงรีเห็นเมฆเลื่อน เก้าอี้ แก้วน้ำบนถาด"""
    c = g.c
    jx = 0 if calm else 5 * math.sin(t * 31)
    with g.at(x + jx, y, sc):
        _rr(c, -380, -380, 760, 520, 60)
        _shade(c, hexc("#f2ead6"), 7, 0.15)
        for i in range(3):
            wx = -240 + i * 240
            c.save()
            c.new_path()
            c.save()
            c.translate(wx, -230)
            c.scale(0.75, 1)
            c.arc(0, 0, 80, 0, 2 * math.pi)
            c.restore()
            c.clip_preserve()
            c.set_source_rgba(*SKY)
            c.fill()
            if calm:
                for k in range(2):
                    cloud(g, wx + ((k * 160 - t * 90) % 320) - 160, -200 + k * 50, 0.4)
            else:
                cloud(g, wx + 20 * math.sin(t * 2 + i), -220, 0.6, hexc("#9aa3ad"))
            c.restore()
            c.new_path()
            c.save()
            c.translate(wx, -230)
            c.scale(0.75, 1)
            c.arc(0, 0, 80, 0, 2 * math.pi)
            c.restore()
            c.set_source_rgba(*INK)
            c.set_line_width(7)
            c.stroke()
        for i in range(2):   # พนักเก้าอี้
            sx = -170 + i * 340
            _rr(c, sx - 120, -60, 240, 220, 40)
            _shade(c, PA_BLUE if calm else hexc("#8a6a42"), 6, 0.25)
            _rr(c, sx - 100, -60, 200, 40, 16)
            _shade(c, WHITE, 4, 0)
        _rr(c, -60, 40, 120, 14, 4)   # ถาด
        _shade(c, hexc("#b88a52"), 4, 0)
        tilt = 0 if calm else 18 * math.sin(t * 9)
        with g.at(0, 40, 1, tilt):
            _smooth_path(c, [(-22, 0), (-28, -70), (28, -70), (22, 0)])
            _shade(c, hexc("#e6eef4"), 4, 0.1)
            _rr(c, -24, -46, 48, 40, 4)
            _shade(c, hexc("#e8c45a"), 0, 0)


def suitcase(g, x, y, sc=1.0, rot=0.0, stickers=("PARIS", "LONDON", "ROME", "TOKYO")):
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -60, -230, 120, 50, 20)
        _shade(c, INK, 0, 0)
        _rr(c, -45, -215, 90, 30, 12)
        _shade(c, WHITE, 0, 0)
        _rr(c, -220, -190, 440, 300, 30)
        _shade(c, hexc("#b8753a"), 7, 0.25)
        cols = [RED, PA_BLUE, hexc("#3c8d4f"), GOLD2]
        for i, s in enumerate(stickers):
            with g.at(-110 + (i % 2) * 220, -100 + (i // 2) * 140, 1, -12 + 9 * i):
                c.new_path()
                c.arc(0, 0, 62, 0, 2 * math.pi)
                _shade(c, cols[i % 4], 5, 0)
                g.text(s, 0, 0, 26, "kanit", WHITE)


def crown(g, x, y, sc=1.0, rot=0.0):
    with g.at(x, y, sc, rot):
        g.poly([(-120, 60), (-140, -60), (-70, 0), (0, -90), (70, 0), (140, -60), (120, 60)], GOLD, 7)
        for px in (-140, 0, 140):
            g.circle(px, -60 if px else -90, 16, RED, 4)


def globe(g, x, y, r, t=0.0):
    c = g.c
    c.new_path()
    c.arc(x, y, r, 0, 2 * math.pi)
    _shade(c, hexc("#8fb8de"), 6, 0.3)
    c.save()
    c.arc(x, y, r, 0, 2 * math.pi)
    c.clip()
    for i in range(5):
        cx = x + ((i * 0.37 + t * 0.08) % 1 * 2.4 - 1.2) * r
        g.blob(cx, y + (hn(i, 7) - 0.5) * r * 1.2, r * 0.3, r * 0.2, LAND, 0, 3 + i)
    c.restore()
    c.new_path()
    c.arc(x, y, r, 0, 2 * math.pi)
    c.set_source_rgba(*INK)
    c.set_line_width(6)
    c.stroke()


def house(g, x, y, sc=1.0, col=hexc("#f2ead6"), roof=RED):
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -130, -200, 260, 200, 6)
        _shade(c, col, 6, 0.2)
        c.new_path()
        for p in [(-160, -190), (0, -310), (160, -190)]:
            c.line_to(*p)
        c.close_path()
        _shade(c, roof, 6, 0.2)
        _rr(c, -30, -110, 60, 110, 10)
        _shade(c, hexc("#7a4a2a"), 4, 0.1)
        _rr(c, -110, -160, 60, 50, 4)
        _shade(c, SKY, 4, 0)


def ticket(g, x, y, sc=1.0, rot=0.0, price=""):
    """ตั๋วเครื่องบิน"""
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -220, -100, 440, 200, 16)
        _shade(c, WHITE, 6, 0.1)
        _rr(c, -220, -100, 440, 56, 16)
        _shade(c, PA_BLUE, 0, 0)
        g.text("JET CLIPPER", 0, -72, 30, "kanit", WHITE)
        g.text("NEW YORK  →  PARIS", 0, -8, 32, "kanit", INK)
        g.text("26 OCT 1958", 0, 50, 30, "kanitsb", GREY)


def bizcase(g, x, y, sc=1.0, rot=0.0):
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -40, -150, 80, 40, 14)
        _shade(c, INK, 0, 0)
        _rr(c, -150, -120, 300, 200, 18)
        _shade(c, hexc("#5a3a22"), 6, 0.25)
        _rr(c, -20, -40, 40, 30, 4)
        _shade(c, GOLD, 4, 0)


def camera(g, x, y, sc=1.0, rot=0.0, t=0.0):
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -130, -80, 260, 160, 24)
        _shade(c, hexc("#3a3f48"), 6, 0.25)
        g.circle(20, 0, 60, hexc("#c9ced6"), 6)
        g.circle(20, 0, 32, hexc("#2b2f3a"), 4)
        _rr(c, -110, -110, 60, 30, 6)
        _shade(c, hexc("#c9ced6"), 4, 0)
        if math.sin(t * 2.5) > 0.85:
            g.star(-80, -140, 40, GOLD2, 0, pts=8)


def jet_top(g, x, y, sc=1.0, rot=0.0, hl=0.0, t=0.0):
    """707 มองจากด้านบน หัวชี้ขึ้น: ปีกลู่ เครื่องยนต์ 4 ตัว (hl = ไฮไลต์เลขเครื่องยนต์ 0..1)"""
    c = g.c
    with g.at(x, y, sc, rot):
        _smooth_path(c, [(-30, 120), (-280, 230), (-290, 260), (-20, 210), (20, 210), (290, 260), (280, 230),
                         (30, 120)])   # ปีกหลัก
        _shade(c, hexc("#d9dde3"), 6, 0.2)
        _smooth_path(c, [(-20, 400), (-130, 470), (-130, 490), (0, 470), (130, 490), (130, 470), (20, 400)])
        _shade(c, hexc("#d9dde3"), 5, 0.2)
        _rr(c, -36, -330, 72, 820, 36)
        _shade(c, METAL, 6, 0.3)
        _rr(c, -10, -330, 20, 820, 10)
        c.set_source_rgba(*PA_BLUE, )
        c.fill()
        _smooth_path(c, [(-22, -290), (22, -290), (16, -260), (-16, -260)])
        _shade(c, hexc("#2b3f63"), 3, 0)
        for i, (ex, ey) in enumerate(((-210, 190), (-110, 150), (110, 150), (210, 190))):
            _rr(c, ex - 18, ey - 70, 36, 90, 16)
            _shade(c, hexc("#c3c9d1"), 5, 0.3)
            if hl > 0:
                k = max(0.0, min(1.0, hl * 4 - i))
                if k > 0:
                    with g.at(ex, ey - 130, k):
                        g.circle(0, 0, 40, GOLD, 5)
                        g.text(str(i + 1), 0, 0, 46, "kanit", INK)
