"""ตัวละครและพร็อพ: สนูป ด็อกก์ (เกิด 20 ต.ค. 1971) — คนแบบกึ่งเสมือนจริงจาก src/people.py"""
import math

import cairo

from gfx import BLUE, BROWN, BROWN2, GOLD, GOLD2, GREY, ICE, INK, LGREY, NAVY, RED, WHITE, hexc
from people import Look, _rr, _shade, _smooth_path, _stroke

DARK_SKIN = hexc("#7b4a30")
DARK_SKIN2 = hexc("#8d5a3b")
KHAKI = hexc("#c9b083")

# สนูป ด็อกก์ยุค 90: ผอมสูง ผมถักเปียยาวสองข้าง หนวดบาง เสื้อเชิ้ตลายสก็อตตัวโคร่ง กางเกงกากี รองเท้าผ้าใบขาว
SNOOP90 = Look(hair="braids", hair_col=hexc("#1c1714"), skin=DARK_SKIN, suit=hexc("#41608e"), pants=KHAKI,
               shoes=hexc("#f2f2f2"), outfit="flannel", facial="mustache", w=55, jaw=0.25, nose=1.15, brow=0.9,
               age=0.1, build=0.92, height=1.1)
# สนูปยุคปัจจุบัน: แว่นดำ หนวดเครา ฮู้ดสีสด ยิ้มอารมณ์ดี
SNOOP_NOW = Look(hair="braids", hair_col=hexc("#1c1714"), skin=DARK_SKIN, suit=hexc("#3c8d4f"), pants=hexc("#2b2b30"),
                 shoes=hexc("#f2f2f2"), outfit="hoodie", facial="goatee", glasses="shades", w=55, jaw=0.3, nose=1.15,
                 age=0.6, build=0.92, height=1.1)
# สนูปในชุดสูทขึ้นศาล
SNOOP_COURT = Look(hair="braids", hair_col=hexc("#1c1714"), skin=DARK_SKIN, suit=hexc("#232327"), tie=hexc("#2b3f63"),
                   facial="mustache", w=55, jaw=0.25, nose=1.15, brow=0.9, age=0.15, build=0.92, height=1.1)
# วัยรุ่นในย่านเสี่ยง
SNOOP_TEEN = Look(hair="buzz", hair_col=hexc("#1c1714"), skin=DARK_SKIN, suit=hexc("#3a3a42"), pants=hexc("#5a6b85"),
                  shoes=hexc("#f2f2f2"), outfit="hoodie", w=55, jaw=0.2, nose=1.1, age=0.0, build=0.88, height=1.04)
# แคลวินตอนเด็ก
KID = Look(hair="buzz", hair_col=hexc("#1c1714"), skin=DARK_SKIN, suit=hexc("#e3a92b"), pants=hexc("#3f6496"),
           shoes=hexc("#f2f2f2"), outfit="tee", w=58, jaw=0.05, nose=0.8, brow=0.7, age=0.0, build=0.8, height=0.62,
           headsc=1.45)
# แม่ (เบเวอร์ลี เทต)
MOM = Look(hair="bun", hair_col=hexc("#1c1714"), skin=DARK_SKIN2, suit=hexc("#b8473a"), outfit="dress",
           shoes=hexc("#5a3a22"), w=54, jaw=0.1, nose=0.9, brow=0.7, age=0.2, build=0.88)
# ดร.เดร ยุค 90: ผมสั้นเกรียน หนวดเครา ร่างบึก เสื้อยืดดำ
DRE = Look(hair="buzz", hair_col=hexc("#1c1714"), skin=hexc("#6e4128"), suit=hexc("#1f1f24"), pants=hexc("#2b3a55"),
           shoes=hexc("#1f1f24"), outfit="tee", facial="goatee", w=62, jaw=0.75, nose=1.1, brow=1.2, age=0.3,
           build=1.15)
JUDGE = Look(hair="slick", hair_col=hexc("#b9b4aa"), suit=hexc("#141416"), tie=hexc("#141416"), w=60, jaw=0.6,
             age=0.9, glasses="thin")
GRANDMA = Look(hair="bun", hair_col=hexc("#d9d5cc"), suit=hexc("#8a6a9a"), outfit="dress", shoes=hexc("#5a3a22"),
               w=56, age=1.0, build=0.9, height=0.95)
FANS = [
    Look(hair="afro", hair_col=hexc("#1c1714"), skin=DARK_SKIN2, suit=hexc("#e3a92b"), pants=hexc("#2b3a55"),
         outfit="tee", w=56, age=0.1, shoes=hexc("#f2f2f2")),
    Look(hair="part", hair_col=hexc("#a8763e"), suit=hexc("#c8553d"), pants=hexc("#2b3a55"), outfit="hoodie",
         w=56, age=0.1, shoes=hexc("#f2f2f2")),
    Look(hair="short", hair_col=hexc("#2b2622"), skin=hexc("#d9a37e"), suit=hexc("#3f6496"), pants=KHAKI,
         outfit="tee", w=58, age=0.2, shoes=hexc("#f2f2f2")),
]


# ---------------------------------------------------------------- พร็อพ
def tv(g, x, y, sc=1.0, t=0.0, show=True):
    """ทีวีจอตู้ยุค 70 ฉายการ์ตูนหมาสีขาว"""
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -200, -160, 400, 300, 30)
        _shade(c, hexc("#8a5a36"), 6, 0.3)
        _rr(c, -170, -130, 280, 220, 40)
        _shade(c, hexc("#cfe3d7") if show else hexc("#55585e"), 5, 0.2)
        for k in (-80, 80):
            g.line([(k * 0.4, -160), (k, -260)], 5)
        g.circle(160, -60, 14, GOLD, 4)
        g.circle(160, 0, 14, GOLD, 4)
        if show:   # หมาการ์ตูนขาวหูดำ กระโดดดุ๊กดิ๊ก
            hop = abs(math.sin(t * 5)) * 18
            with g.at(-30, 20 - hop, 0.8):
                g.blob(0, 0, 70, 50, WHITE, 5)
                g.blob(40, -50, 46, 40, WHITE, 5)
                g.blob(20, -40, 14, 30, INK, 0)
                g.circle(80, -50, 9, INK, 0)
                g.circle(50, -60, 5, INK, 0)
                for lx in (-40, 30):
                    g.line([(lx, 40), (lx, 66)], 8)


def streetlight(g, x, y, sc=1.0, on=True):
    with g.at(x, y, sc):
        if on:
            c = g.c
            c.move_to(60, -560)
            c.line_to(-60, 0)
            c.line_to(200, 0)
            c.close_path()
            c.set_source_rgba(1, 0.92, 0.55, 0.3)
            c.fill()
        g.rrect(-10, -600, 20, 600, 6, GREY, 5)
        g.line([(0, -590), (60, -600), (80, -575)], 10)
        g.rrect(50, -585, 60, 26, 10, GOLD2 if on else LGREY, 5)


def wall(g, x0, x1, y0, y1, tag=True):
    """กำแพงอิฐ + กราฟฟิตี้"""
    c = g.c
    _rr(c, x0, y0, x1 - x0, y1 - y0, 4)
    _shade(c, hexc("#c99a7a"), 6, 0.15)
    c.save()
    _rr(c, x0, y0, x1 - x0, y1 - y0, 4)
    c.clip()
    for j in range(int((y1 - y0) / 50) + 1):
        yy = y0 + j * 50
        _stroke(c, [(x0, yy), (x1, yy)], 3, INK, 0.25, smooth=False)
        off = 50 if j % 2 else 0
        for xx in range(int(x0) + off, int(x1), 100):
            _stroke(c, [(xx, yy), (xx, yy + 50)], 3, INK, 0.25, smooth=False)
    c.restore()
    if tag:
        g.label("LBC", (x0 + x1) / 2, y0 + 100, 90, color=hexc("#3f6496"), rot=-8)


def jail_bars(g, x, y, w=440, h=520, a=1.0):
    c = g.c
    with g.alpha(a):
        _rr(c, x - w / 2, y - h, w, h, 6)
        c.set_source_rgba(0.85, 0.85, 0.88, 0.5)
        c.fill()
        for i in range(7):
            xx = x - w / 2 + 20 + i * (w - 40) / 6
            g.rrect(xx - 9, y - h, 18, h, 8, GREY, 4)
        g.rrect(x - w / 2, y - h * 0.62, w, 22, 6, GREY, 4)
        g.rrect(x - w / 2 - 10, y - h - 20, w + 20, 30, 8, GREY, 5)


def cassette(g, x, y, sc=1.0, rot=0.0, t=0.0, label="DEMO"):
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -150, -95, 300, 190, 16)
        _shade(c, hexc("#2d2b29"), 6, 0.3)
        _rr(c, -120, -70, 240, 70, 10)
        _shade(c, WHITE, 4, 0.05)
        g.text(label, 0, -50, 30, "kanit", RED)
        _rr(c, -90, 10, 180, 60, 12)
        _shade(c, hexc("#55585e"), 4, 0.2)
        for sx in (-1, 1):
            g.circle(sx * 55, 40, 22, WHITE, 4)
            for k in range(6):
                a = t * 6 + k * math.pi / 3
                g.line([(sx * 55, 40), (sx * 55 + 16 * math.cos(a), 40 + 16 * math.sin(a))], 3, amp=0)


def microphone(g, x, y, sc=1.0, rot=0.0, glow=0.0):
    c = g.c
    with g.at(x, y, sc, rot):
        if glow > 0:
            g.sunburst(0, -120, 110, 230, 16, g.t * 25, 10, (0.95, 0.83, 0.48, glow))
        _rr(c, -18, -40, 36, 230, 14)
        _shade(c, hexc("#2d2b29"), 5, 0.3)
        c.new_path()
        c.arc(0, -110, 70, 0, 2 * math.pi)
        _shade(c, LGREY, 5, 0.35)
        for k in range(-3, 4):
            _stroke(c, [(k * 18, -170), (k * 18, -50)], 2.5, GREY, 0.8, smooth=False)


def sound_waves(g, x, y, t, n=3, col=None, side=1):
    for i in range(n):
        p = (t * 1.4 + i / n) % 1
        g.arc(x, y, 50 + 140 * p, -40 if side > 0 else 140, 40 if side > 0 else 220, 8,
              col or (0.24, 0.39, 0.59, 1 - p))


def console(g, x, y, sc=1.0, t=0.0):
    """โต๊ะมิกซ์เสียงในสตูดิโอ"""
    c = g.c
    with g.at(x, y, sc):
        c.new_path()
        for p in [(-330, 0), (330, 0), (290, -150), (-290, -150)]:
            c.line_to(*p)
        c.close_path()
        _shade(c, hexc("#3a3a42"), 6, 0.3)
        for i in range(12):
            xx = -260 + i * 47
            g.line([(xx, -130), (xx, -30)], 4, GREY, amp=0)
            yy = -90 + 40 * math.sin(t * 3 + i)
            g.rrect(xx - 12, yy - 8, 24, 16, 4, LGREY, 3)
        _rr(c, -330, 0, 660, 160, 8)
        _shade(c, hexc("#2d2b29"), 6, 0.3)


def headphones(g, x, y, sc=1.0):
    with g.at(x, y, sc):
        g.arc(0, 0, 80, 180, 360, 14)
        for sx in (-1, 1):
            g.rrect(sx * 80 - 22, -10, 44, 70, 18, INK, 0)


def gold_record(g, x, y, sc=1.0, rot=0.0, label="1993"):
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -170, -200, 340, 400, 10)
        _shade(c, hexc("#2d2b29"), 6, 0.2)
        c.new_path()
        c.arc(0, -20, 135, 0, 2 * math.pi)
        _shade(c, GOLD, 5, 0.35)
        for r in (110, 90, 70):
            g.arc(0, -20, r, 0, 360, 2, GOLD2)
        g.circle(0, -20, 34, RED, 4)
        g.text(label, 0, 150, 38, "kanit", GOLD2)


def stage(g, x, y, t, w=900, lights=True):
    """เวทีคอนเสิร์ต + ไฟสปอตไลต์"""
    c = g.c
    with g.at(x, y):
        if lights:
            for i, sx in enumerate((-1, 1)):
                a = 0.3 * math.sin(t * 1.5 + i * 2)
                c.save()
                c.translate(sx * w * 0.45, -900)
                c.rotate(a - sx * 0.35)
                c.move_to(0, 0)
                c.line_to(-140, 900)
                c.line_to(140, 900)
                c.close_path()
                c.set_source_rgba(1, 0.9, 0.5, 0.28)
                c.fill()
                c.restore()
        _rr(c, -w / 2, 0, w, 90, 6)
        _shade(c, hexc("#2d2b29"), 6, 0.2)


def crowd(g, x, y, w, t, n=9, a=1.0):
    """ฝูงคนดูเป็นเงา โบกมือ"""
    with g.silhouette(INK, 0.85 * a):
        for i in range(n):
            xx = x - w / 2 + i * w / (n - 1)
            bob = 10 * math.sin(t * 6 + i * 1.3)
            g.blob(xx, y - 60 + bob, 52, 70, INK, 0, i)
            g.circle(xx, y - 150 + bob, 36, INK, 0)
            if i % 2:
                g.line([(xx + 40, y - 90 + bob), (xx + 70, y - 220 + bob + 20 * math.sin(t * 8 + i))], 18)


def bench(g, x, y, sc=1.0):
    """บัลลังก์ศาล"""
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -330, -300, 660, 300, 8)
        _shade(c, hexc("#7a4b2a"), 6, 0.3)
        for k in (-220, 0, 220):
            _rr(c, k - 80, -250, 160, 200, 6)
            _shade(c, hexc("#8a5a36"), 4, 0.2)
        c.new_path()
        c.arc(0, -150, 50, 0, 2 * math.pi)
        _shade(c, GOLD, 4, 0.3)


def gavel(g, x, y, sc=1.0, rot=0.0):
    with g.at(x, y, sc, rot):
        g.rrect(-10, -10, 20, 200, 8, hexc("#7a4b2a"), 5)
        g.rrect(-80, -60, 160, 70, 18, hexc("#8a5a36"), 6)
        g.rrect(-90, -55, 22, 60, 6, GOLD, 4)
        g.rrect(68, -55, 22, 60, 6, GOLD, 4)


def newspaper(g, x, y, sc=1.0, rot=0.0, head1="", head2=""):
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -170, -220, 340, 440, 4)
        _shade(c, hexc("#f2ecdc"), 5, 0.15)
        g.text("DAILY NEWS", 0, -185, 26, "kanit")
        g.line([(-150, -162), (150, -162)], 3, amp=0)
        g.text(head1, 0, -105, 50, "kanit", maxw=310)
        if head2:
            g.text(head2, 0, 5, 26, "kanitm", maxw=310)
        _rr(c, -150, 35, 140, 90, 3)
        _shade(c, LGREY, 3, 0.2)
        for i in range(6):
            _stroke(c, [(10, 6 + i * 18), (150, 6 + i * 18)], 3, GREY, 0.6, smooth=False)
        for i in range(4):
            _stroke(c, [(-150, 130 + i * 18), (150, 130 + i * 18)], 3, GREY, 0.6, smooth=False)


def money(g, x, y, sc=1.0, rot=0.0):
    with g.at(x, y, sc, rot):
        g.rrect(-80, -40, 160, 80, 8, hexc("#9cc39a"), 5)
        g.circle(0, 0, 24, hexc("#cfe3d7"), 4)
        g.text("$", 0, 0, 34, "kanit", hexc("#3c6b3a"))


def door_light(g, x, y, sc=1.0, k=1.0):
    """ประตูเปิดออกสู่แสง"""
    with g.at(x, y, sc):
        g.sunburst(0, -260, 170, 330, 18, g.t * 15, 10, (0.95, 0.83, 0.48, 0.8 * k))
        g.rrect(-130, -500, 260, 500, 8, hexc("#fff4cf"), 7)
        g.rrect(-130, -500, 260 * (1 - 0.8 * k), 500, 6, hexc("#7a4b2a"), 6)


def heart(g, x, y, s=1.0, col=RED):
    with g.at(x, y, s):
        c = g.c
        c.move_to(0, 30)
        c.curve_to(-70, -20, -40, -80, 0, -40)
        c.curve_to(40, -80, 70, -20, 0, 30)
        g.fs(col, 5)
