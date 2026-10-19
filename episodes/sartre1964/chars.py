"""ตัวละครและพร็อพ: ซาร์ตร์ปฏิเสธโนเบล 22 ต.ค. 1964 — คนแบบกึ่งเสมือนจริงจาก src/people.py"""
import math

from gfx import GOLD, GOLD2, GREY, INK, LGREY, NAVY, RED, WHITE, hexc, lerp
from gfx import hn as _hn
from people import Look, _rr, _shade, _smooth_path, _stroke

PAPERC = hexc("#f4efe2")
WOOD = hexc("#8a5a36")


def hn(*a):
    return (_hn(*a) + 1) / 2


# ฌอง-ปอล ซาร์ตร์ (59): ร่างเล็ก ผมเสยเรียบหน้าผากกว้าง แว่นกรอบกลมหนา สูทลายทางเทาเข้ม เนกไทลายแดง
SARTRE = Look(hair="slick", hair_col=hexc("#3a2f28"), suit=hexc("#33363d"), tie=hexc("#9a3a3a"), glasses="round",
              w=60, jaw=0.45, jowls=0.4, nose=1.15, brow=0.8, age=0.6, build=0.95, height=0.88)
# ซีมอน เดอ โบวัวร์: มวยผม ผ้าโพก (คู่ชีวิต — ปรากฏเป็นฉากหลัง)
COMMITTEE = [
    Look(hair="crew", hair_col=hexc("#d9d5cc"), suit=hexc("#1f1f24"), tie=hexc("#1f1f24"), bowtie=True, w=60,
         jaw=0.6, jowls=0.5, nose=1.2, age=0.85),
    Look(hair="part", hair_col=hexc("#9a948a"), suit=hexc("#2f3a4a"), tie=hexc("#2b3f63"), glasses="thin", w=58,
         age=0.7),
    Look(hair="slick", hair_col=hexc("#b9b4aa"), suit=hexc("#3b4250"), tie=hexc("#7a2e2e"), facial="mustache",
         w=58, age=0.75),
]
CRITICS = [
    Look(hair="part", hair_col=hexc("#6b4a33"), suit=hexc("#5a4a3a"), tie=hexc("#7a2e2e"), w=57, age=0.4),
    Look(hair="bun", hair_col=hexc("#2b2622"), suit=hexc("#8a4a5a"), outfit="dress", w=54, age=0.4, height=0.93),
    Look(hair="crew", hair_col=hexc("#3a2f28"), suit=hexc("#2f3a4a"), tie=hexc("#8a6a2a"), glasses="thick", w=58,
         age=0.5),
]


def pipe(g, x, y, sc=1.0, rot=0.0, t=0.0, smoke=True):
    c = g.c
    with g.at(x, y, sc, rot):
        _stroke(c, [(0, 0), (60, 6), (90, 10)], 8, hexc("#2b2622"))
        _rr(c, 84, -30, 40, 50, 10)
        _shade(c, hexc("#5a3a22"), 4, 0.2)
        if smoke:
            for i in range(3):
                u = (t * 0.5 + i / 3) % 1
                g.circle(104 + 20 * math.sin(t * 2 + i), -40 - u * 140, 10 + 18 * u, (0.75, 0.75, 0.78, 0.6 * (1 - u)), 0)


def medal(g, x, y, r, sc=1.0, rot=0.0, label="", dim=0.0):
    c = g.c
    with g.at(x, y, sc, rot):
        c.new_path()
        c.arc(0, 0, r, 0, 2 * math.pi)
        _shade(c, GOLD, 7, 0.3)
        c.new_path()
        c.arc(0, 0, r * 0.8, 0, 2 * math.pi)
        _shade(c, GOLD2, 4, 0.15)
        _smooth_path(c, [(-r * 0.35, -r * 0.45), (r * 0.1, -r * 0.55), (r * 0.3, -r * 0.3), (r * 0.4, -r * 0.05),
                         (r * 0.25, r * 0.1), (r * 0.3, r * 0.4), (-r * 0.1, r * 0.55), (-r * 0.4, r * 0.3)])
        _shade(c, hexc("#d9a441"), 3, 0.3)
        if dim > 0:
            c.new_path()
            c.arc(0, 0, r, 0, 2 * math.pi)
            c.set_source_rgba(1, 1, 1, 0.6 * dim)
            c.fill()
        if label:
            g.label(label, 0, r + 50, 40)


def legion(g, x, y, sc=1.0, rot=0.0):
    """เครื่องอิสริยาภรณ์เลฌียงดอเนอร์ (ดาวห้าแฉกขาว ริบบิ้นแดง)"""
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -30, -170, 60, 90, 4)
        _shade(c, RED, 4, 0.2)
        g.star(0, 0, 80, WHITE, 6, pts=5, inner=0.55)
        g.circle(0, 0, 26, GOLD, 4)


def newspaper(g, x, y, sc=1.0, rot=0.0, head="", sub=""):
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -280, -360, 560, 720, 6)
        _shade(c, PAPERC, 6, 0.2)
        g.text("LE FIGARO", 0, -310, 50, "kanit", INK)
        _stroke(c, [(-250, -276), (250, -276)], 4, INK, smooth=False)
        g.text("1964", 0, -256, 22, "kanitm", GREY)
        if head:
            g.text(head, 0, -170, 50, "kanit", INK, maxw=500)
        if sub:
            g.text(sub, 0, -90, 30, "kanitsb", INK, maxw=500)
        _rr(c, -100, -40, 200, 240, 4)
        _shade(c, hexc("#d9d2c2"), 5, 0.1)
        for k in range(6):
            _stroke(c, [(-250, 240 + k * 18), (250 - (k == 5) * 180, 240 + k * 18)], 6, LGREY, smooth=False)
            if k < 5:
                _stroke(c, [(120, -20 + k * 40), (250, -20 + k * 40)], 6, LGREY, smooth=False)
                _stroke(c, [(-250, -20 + k * 40), (-120, -20 + k * 40)], 6, LGREY, smooth=False)


def chain(g, x0, y0, x1, y1, brk=0.0, n=8, col=GREY):
    for i in range(n):
        u = i / (n - 1)
        px, py = lerp(x0, x1, u), lerp(y0, y1, u)
        off = (1 if u > 0.5 else -1) * brk * 120 * abs(u - 0.5) * 2
        with g.at(px + off, py + brk * 40 * math.sin(i), 1, (90 if i % 2 else 0) + brk * 40 * (u - 0.5)):
            g.c.new_path()
            g.c.save()
            g.c.scale(1, 0.55)
            g.c.arc(0, 0, 36, 0, 2 * math.pi)
            g.c.restore()
            g.c.set_source_rgba(*col[:3], 1)
            g.c.set_line_width(12)
            g.c.stroke()


def books(g, x, y, n=6, sc=1.0):
    cols = [hexc("#7a2e2e"), hexc("#2f5a3a"), hexc("#2b3f63"), hexc("#a8763e"), hexc("#5a4a3a"), hexc("#8a6a9a")]
    with g.at(x, y, sc):
        xx = 0
        for i in range(n):
            w = 40 + 14 * hn(i, 3)
            h = 200 + 60 * hn(i, 4)
            _rr(g.c, xx, -h, w, h, 4)
            _shade(g.c, cols[i % 6], 4, 0.25)
            _stroke(g.c, [(xx + 8, -h + 30), (xx + w - 8, -h + 30)], 3, GOLD2, 0.8, smooth=False)
            xx += w + 4


def bookshelf(g, x0, x1, y0, y1):
    c = g.c
    _rr(c, x0, y0, x1 - x0, y1 - y0, 6)
    _shade(c, WOOD, 6, 0.25)
    rows = 3
    h = (y1 - y0) / rows
    for r in range(rows):
        _rr(c, x0 + 16, y0 + r * h + 14, x1 - x0 - 32, h - 28, 4)
        _shade(c, hexc("#5a3a22"), 3, 0)
        bs = min(0.55, (h - 40) / 270)
        books(g, x0 + 30, y0 + (r + 1) * h - 16, int((x1 - x0 - 60) / (52 * bs)), bs)


def money_stack(g, x, y, n=5, sc=1.0):
    with g.at(x, y, sc):
        for i in range(n):
            _rr(g.c, -110, -i * 26 - 26, 220, 26, 4)
            _shade(g.c, hexc("#8fbf6a"), 4, 0.2)
            g.circle(0, -i * 26 - 13, 9, hexc("#5a8a3a"), 2)


def envelope(g, x, y, sc=1.0, rot=0.0, label="ข้อบังคับ"):
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -160, -100, 320, 200, 8)
        _shade(c, PAPERC, 5, 0.15)
        g.line([(-160, -100), (0, 20), (160, -100)], 5, amp=0)
        g.circle(0, 20, 26, RED, 4)
        if label:
            g.label(label, 0, 140, 40, color=NAVY)


def bird_free(g, x, y, s=1.0, t=0.0):
    """นกบินอิสระ (เส้นปีกรูปตัว M)"""
    flap = math.sin(t * 8 + x * 0.01)
    with g.at(x, y, s):
        g.line([(-70, -10 * flap), (-35, -40 - 20 * flap), (0, 0), (35, -40 - 20 * flap), (70, -10 * flap)], 10, INK,
               amp=0, smooth=True)
