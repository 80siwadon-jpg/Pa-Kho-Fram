"""ตัวละครและพร็อพ: โทรเลขข้ามทวีปสายแรก 24 ต.ค. 1861 / ปิดฉากโพนี เอ็กซ์เพรส"""
import math

from gfx import GOLD, GOLD2, GREY, INK, NAVY, RED, WHITE, hexc
from people import Look, _rr, _shade, _smooth_path, _stroke

SAND = hexc("#ecd9a8")
HORSE = hexc("#8a5a36")
HORSE2 = hexc("#6e4528")
WOOD = hexc("#8a6a42")
COPPER = hexc("#c87a3a")

# อับราฮัม ลินคอล์น (52): สูงผอม เคราคางไม่มีหนวด ผมดำยุ่ง หน้ายาว กรามชัด สูทดำ หูกระต่ายดำ
LINCOLN = Look(hair="edison", hair_col=hexc("#1f1a17"), suit=hexc("#1d1c20"), tie=hexc("#1d1c20"), bowtie=True,
               facial="beard", w=54, jaw=0.7, jowls=0.2, nose=1.3, brow=1.1, age=0.7, height=1.08, build=0.9)
RIDER = Look(hair="short", hair_col=hexc("#8a5a36"), outfit="flannel", suit=hexc("#c8553d"), pants=hexc("#5a4a3a"),
             w=54, age=0.05, hat="porkpie", hat_trim=hexc("#8a6a42"))
OPERATOR = Look(hair="part", hair_col=hexc("#4a3424"), outfit="vest", suit=hexc("#4a4038"), shirt=hexc("#f2ece0"),
                tie=hexc("#2b2622"), facial="mustache", w=56, age=0.4)
TOWNS = [
    Look(hair="short", hair_col=hexc("#6b4a33"), outfit="vest", suit=hexc("#5a4a3a"), shirt=WHITE, tie=hexc("#7a2e2e"),
         w=56, hat="bowler"),
    Look(hair="bun", hair_col=hexc("#5a3a22"), outfit="dress", suit=hexc("#6a7f9a"), w=54, height=0.93),
    Look(hair="short", hair_col=hexc("#2b2622"), outfit="vest", suit=hexc("#3a4a3a"), shirt=WHITE, tie=hexc("#2b2622"),
         w=56, facial="beard", hat="tophat"),
]


def horse(g, x, y, sc=1.0, t=0.0, gallop=1.0, rider=True, flip=False):
    """ม้าวิ่งมองด้านข้าง หันขวา + คนขี่ (ถุงจดหมาย) — x,y = พื้น"""
    from people import head
    c = g.c
    ph = t * 12 * gallop
    by = -14 * abs(math.sin(ph)) * gallop
    with g.at(x, y + by, sc, 0, sx=-sc if flip else sc, sy=sc):
        for k, (lx, off) in enumerate(((-110, 0), (-70, 1.6), (90, 3.1), (130, 4.7))):
            a = 30 * math.sin(ph + off) * gallop
            with g.at(lx, -230, 1, a):
                _stroke(c, [(0, 0), (6, 110), (0, 210)], 30, INK)
                _stroke(c, [(0, 0), (6, 110), (0, 210)], 22, HORSE2 if k % 2 == 0 else HORSE)
                _rr(c, -16, 200, 32, 22, 6)
                _shade(c, INK, 0, 0)
        _smooth_path(c, [(-170, -260), (-120, -330), (80, -340), (170, -300), (180, -230), (120, -190), (-120, -190),
                         (-180, -220)])
        _shade(c, HORSE, 6, 0.3)
        _smooth_path(c, [(120, -310), (180, -420), (230, -450), (290, -400), (280, -370), (220, -380), (190, -260)])
        _shade(c, HORSE, 6, 0.3)
        g.circle(250, -420, 6, INK, 0)
        _stroke(c, [(130, -320), (170, -410), (220, -455)], 14, hexc("#3a2614"))   # แผงคอ
        _stroke(c, [(-170, -260), (-240, -240 + 20 * math.sin(ph)), (-260, -170)], 16, hexc("#3a2614"))   # หาง
        if rider:
            _rr(c, -60, -380, 90, 70, 10)   # ถุงจดหมาย (mochila)
            _shade(c, hexc("#a8693a"), 5, 0.2)
            g.text("MAIL", -15, -345, 22, "kanit", WHITE)
            _smooth_path(c, [(-30, -340), (40, -340), (50, -470), (-20, -480)])
            _shade(c, RIDER.suit, 5, 0.3)
            _stroke(c, [(30, -440), (120, -380), (190, -400)], 16, INK)
            _stroke(c, [(30, -440), (120, -380), (190, -400)], 10, RIDER.suit)
            _stroke(c, [(0, -340), (40, -280), (20, -220)], 18, INK)
            _stroke(c, [(0, -340), (40, -280), (20, -220)], 12, RIDER.pants)
            with g.at(14, -540, 0.62):
                head(g, RIDER, "smile", 0, 0.4, (0, 0), 2, 4.5)


def telegraph_line(g, x0, x1, y, t=0.0, n=4, pulse=1.0, h=420, k=1.0):
    """เสาโทรเลข + สายทองแดง + สัญญาณมอร์สวิ่ง (k = สัดส่วนที่ปักเสาแล้ว)"""
    c = g.c
    xs = [x0 + (x1 - x0) * i / (n - 1) for i in range(n)]
    m = max(1, int(n * k + 0.999))
    for xx in xs[:m]:
        g.line([(xx, y), (xx, y - h)], 12, WOOD, amp=0)
        g.line([(xx - 60, y - h + 40), (xx + 60, y - h + 40)], 9, WOOD, amp=0)
        g.circle(xx - 50, y - h + 28, 8, WHITE, 3)
    for i in range(m - 1):
        pts = [(xs[i] + (xs[i + 1] - xs[i]) * u / 10, y - h + 28 + 36 * math.sin(math.pi * u / 10)) for u in range(11)]
        _stroke(c, pts, 4, COPPER)
    if pulse > 0 and m > 1:
        span = xs[m - 1] - xs[0]
        for j in range(3):
            u = (t * 0.9 + j / 3) % 1
            px = xs[0] + span * u
            seg_i = min(int((px - xs[0]) / max(1, (xs[1] - xs[0]))), m - 2)
            v = (px - xs[seg_i]) / max(1, (xs[1] - xs[0]))
            py = y - h + 28 + 36 * math.sin(math.pi * v)
            g.circle(px, py, 12, GOLD2, 3)


def morse_key(g, x, y, sc=1.0, t=0.0, tap=True):
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -160, -30, 320, 30, 6)
        _shade(c, WOOD, 5, 0.25)
        d = 10 * (1 if tap and int(t * 6) % 2 else 0)
        with g.at(-100, -60, 1, d * 0.5):
            _rr(c, 0, -10, 200, 20, 6)
            _shade(c, hexc("#c9a24a"), 4, 0.2)
            g.circle(200, 0, 24, INK, 3)
        _rr(c, -120, -80, 30, 50, 6)
        _shade(c, hexc("#c9a24a"), 4, 0.2)
        if tap:
            g.text("· — · —", 40, -130, 40, "kanit", NAVY)


def us_map(g, x, y, sc=1.0, t=0.0, line=0.0, pony=0.0):
    """แผนที่สหรัฐฯ เชิงสัญลักษณ์: ฝั่งตะวันออก (วอชิงตัน) -> ตะวันตก (แคลิฟอร์เนีย)"""
    c = g.c
    with g.at(x, y, sc):
        _smooth_path(c, [(-430, -160), (-250, -230), (0, -220), (250, -240), (420, -170), (440, 40), (300, 160),
                         (60, 190), (-200, 170), (-400, 100)])
        _shade(c, hexc("#e8dcb8"), 6, 0.15)
        for i in range(4):   # ภูเขา
            mx = -260 + i * 70
            c.new_path()
            for p in [(mx - 50, 40), (mx, -60), (mx + 50, 40)]:
                c.line_to(*p)
            c.close_path()
            _shade(c, hexc("#b9c7c2"), 4, 0.2)
            _smooth_path(c, [(mx - 16, -30), (mx, -60), (mx + 16, -30)])
            _shade(c, WHITE, 2, 0)
        g.circle(-380, 0, 14, RED, 4)
        g.text("แคลิฟอร์เนีย", -330, 50, 30, "kanit", INK)
        g.circle(370, -60, 14, NAVY, 4)
        g.text("วอชิงตัน", 350, -10, 30, "kanit", INK)
        if line > 0:
            px = 370 - 750 * line
            _stroke(c, [(370, -60), (px, -60 + 60 * line)], 8, COPPER, smooth=False)
        if pony > 0:
            g.text("~", -380 + 750 * pony, -100, 60, "kanit", HORSE)


def envelope(g, x, y, sc=1.0, rot=0.0):
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -110, -70, 220, 140, 8)
        _shade(c, hexc("#f4efe2"), 5, 0.15)
        _stroke(c, [(-110, -70), (0, 10), (110, -70)], 4, INK, smooth=False)
        g.circle(0, 10, 16, RED, 3)


def telegram(g, x, y, sc=1.0, rot=0.0, text="CALIFORNIA → LINCOLN"):
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -180, -120, 360, 240, 6)
        _shade(c, hexc("#f6efd6"), 5, 0.12)
        g.text("TELEGRAM", 0, -80, 36, "kanit", RED)
        g.text(text, 0, -20, 24, "kanit", INK, maxw=320)
        for i in range(3):
            g.line([(-140, 30 + i * 30), (140 - 50 * i, 30 + i * 30)], 4, GREY, amp=0)


def wagon(g, x, y, sc=1.0, t=0.0):
    """เกวียนผ้าใบ (ช้า)"""
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -170, -150, 340, 90, 8)
        _shade(c, WOOD, 5, 0.25)
        _smooth_path(c, [(-160, -150), (-150, -290), (0, -330), (150, -290), (160, -150)])
        _shade(c, hexc("#f4efe2"), 5, 0.2)
        for wx in (-110, 110):
            with g.at(wx, -50, 1, t * 30):
                c.new_path()
                c.arc(0, 0, 50, 0, 2 * math.pi)
                _shade(c, hexc("#6e4528"), 5, 0.1)
                for k in range(4):
                    a = k * math.pi / 4
                    _stroke(c, [(-46 * math.cos(a), -46 * math.sin(a)), (46 * math.cos(a), 46 * math.sin(a))], 4,
                            INK, smooth=False)


def sign_closed(g, x, y, sc=1.0, rot=0.0):
    c = g.c
    with g.at(x, y, sc, rot):
        g.line([(-120, -200), (0, -280), (120, -200)], 5, INK, amp=0)
        _rr(c, -220, -200, 440, 150, 10)
        _shade(c, WOOD, 6, 0.3)
        g.text("PONY EXPRESS", 0, -160, 40, "kanit", hexc("#f4efe2"))
        _rr(c, -180, -120, 360, 56, 6)
        _shade(c, RED, 3, 0.1)
        g.text("CLOSED", 0, -92, 42, "kanit", WHITE)


def chip(g, x, y, sc=1.0, label="AI"):
    c = g.c
    with g.at(x, y, sc):
        for i in range(5):
            for s in (-1, 1):
                _stroke(c, [(-80 + i * 40, s * 100), (-80 + i * 40, s * 140)], 8, GREY, smooth=False)
                _stroke(c, [(s * 100, -80 + i * 40), (s * 140, -80 + i * 40)], 8, GREY, smooth=False)
        _rr(c, -100, -100, 200, 200, 20)
        _shade(c, hexc("#2b3440"), 6, 0.2)
        g.text(label, 0, 0, 80, "kanit", hexc("#5ad0f0"))
