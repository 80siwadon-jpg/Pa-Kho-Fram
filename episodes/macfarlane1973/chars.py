"""ตัวละครและพร็อพ: เซธ แมกฟาร์เลน (เกิด 26 ต.ค. 1973)
ไม่วาดตัวละคร Family Guy / หมี Ted ของจริง (ลิขสิทธิ์) — ใช้ทีวี ไมค์ ป้ายชื่อเสียง และหมีเท็ดดี้ทั่วไปแทน"""
import math

from gfx import GOLD, GOLD2, GREY, INK, NAVY, RED, WHITE, hexc
from people import Look, _rr, _shade, _smooth_path, _stroke

FG_BLUE = hexc("#1e9ad6")
FG_YEL = hexc("#f2c94c")
TEDDY = hexc("#c08a52")

# เซธ แมกฟาร์เลน: ผมดำน้ำตาลหวีเสยไปด้านหลัง ยิ้มกว้าง เบลเซอร์กรมท่าเข้ม + เสื้อยืดดำ
SETH = Look(hair="slick", hair_col=hexc("#2b1f18"), suit=hexc("#1f2333"), shirt=hexc("#1b1b1f"), tie=hexc("#1b1b1f"),
            w=58, jaw=0.6, jowls=0.1, nose=1.05, brow=0.85, age=0.35)
SETH_KID = Look(hair="slick", hair_col=hexc("#3a2a1e"), outfit="tee", suit=hexc("#d76b5a"), pants=hexc("#3a4a6a"),
                w=55, age=0.0, height=0.62, headsc=1.45)
EXECS = [
    Look(hair="bald", suit=hexc("#2b2622"), tie=hexc("#7a2e2e"), w=58, age=0.6, glasses="thick"),
    Look(hair="part", hair_col=hexc("#8a7a62"), suit=hexc("#3a3f48"), tie=hexc("#2b3f63"), w=57, age=0.55),
]
FANS = [
    Look(hair="short", hair_col=hexc("#3a2a1e"), outfit="tee", suit=FG_BLUE, pants=hexc("#3a3a40"), w=55, age=0.1),
    Look(hair="bun", hair_col=hexc("#8a5a2a"), outfit="dress", suit=hexc("#d76b5a"), w=54, height=0.93),
    Look(hair="buzz", hair_col=hexc("#1b1714"), outfit="hoodie", suit=hexc("#3c8d4f"), pants=hexc("#3a4a6a"),
         skin=hexc("#7a4a2c"), w=55, age=0.1),
]


def tv(g, x, y, sc=1.0, t=0.0, screen="title", rot=0.0, static=0.0):
    """ทีวีรุ่นเก่า + หนวดกุ้ง; screen: title / off / static / up"""
    c = g.c
    with g.at(x, y, sc, rot):
        for sx in (-1, 1):
            _stroke(c, [(sx * 20, -250), (sx * 110, -380)], 8, INK, smooth=False)
            g.circle(sx * 110, -380, 12, GREY, 4)
        _rr(c, -280, -250, 560, 420, 40)
        _shade(c, hexc("#c9915a"), 7, 0.25)
        _rr(c, -240, -210, 400, 330, 30)
        if screen == "off":
            _shade(c, hexc("#2b2b30"), 5, 0)
        elif screen == "static":
            _shade(c, hexc("#9a9aa0"), 5, 0)
            for i in range(40):
                px = -230 + (i * 97 + int(t * 30) * 41) % 380
                py = -200 + (i * 53 + int(t * 30) * 17) % 310
                c.rectangle(px, py, 14, 6)
                c.set_source_rgba(1, 1, 1, 0.8)
                c.fill()
        else:
            _shade(c, FG_YEL, 5, 0.1)
            g.label("Family", -40, -100, 70, color=FG_BLUE, rot=-4)
            g.label("Guy", -40, -10, 80, color=FG_BLUE, rot=-4)
        for k in range(2):
            g.circle(210, -150 + k * 90, 22, hexc("#7a4a2a"), 4)
        for sx in (-1, 1):
            _rr(c, sx * 200 - 15, 170, 30, 50, 4)
            _shade(c, hexc("#7a4a2a"), 4, 0)


def stamp(g, x, y, txt, sc=1.0, rot=-14, col=RED, k=1.0):
    if k < 0.02:
        return
    with g.at(x, y, sc * (1 + 0.6 * (1 - k)), rot):
        g.rrect(-220, -70, 440, 140, 14, (1, 1, 1, 0), 10, stroke=col)
        g.label(txt, 0, 0, 70, color=col)


def comic(g, x, y, sc=1.0, rot=0.0):
    """การ์ตูนช่องในหนังสือพิมพ์"""
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -260, -170, 520, 340, 6)
        _shade(c, hexc("#f2ede0"), 6, 0.1)
        g.text("THE KENT", 0, -135, 34, "kanit", INK)
        for i in range(3):
            _rr(c, -240 + i * 165, -100, 150, 240, 4)
            _shade(c, WHITE, 4, 0)
            g.circle(-165 + i * 165, 20, 30, hexc("#f2c9a8"), 3)
            g.circle(-175 + i * 165, 14, 4, INK, 0)
            g.circle(-155 + i * 165, 14, 4, INK, 0)
        g.bubble(-150, -40, 100, 50, WHITE, tail=(0, 1))


def pencil(g, x, y, sc=1.0, rot=0.0):
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -18, -200, 36, 220, 6)
        _shade(c, FG_YEL, 5, 0.2)
        c.new_path()
        for p in [(-18, 20), (18, 20), (0, 70)]:
            c.line_to(*p)
        c.close_path()
        _shade(c, hexc("#e8c89a"), 4, 0)
        g.circle(0, 62, 6, INK, 0)
        _rr(c, -18, -230, 36, 34, 6)
        _shade(c, hexc("#e88a8a"), 4, 0)


def mic(g, x, y, sc=1.0, rot=0.0):
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -10, 40, 20, 260, 6)
        _shade(c, hexc("#4a4d55"), 4, 0.2)
        _rr(c, -60, -110, 120, 160, 60)
        _shade(c, hexc("#c9ced6"), 6, 0.3)
        for k in range(5):
            _stroke(c, [(-50, -80 + k * 26), (50, -80 + k * 26)], 2.5, INK, 0.4, smooth=False)
        g.arc(0, -10, 120, 30, 150, 8, hexc("#4a4d55"))


def chart(g, x, y, sc=1.0, k=1.0, up=False, col=RED):
    """กราฟเรตติ้ง (ดิ่งลง / พุ่งขึ้น)"""
    with g.at(x, y, sc):
        g.rrect(-280, -220, 560, 440, 20, WHITE, 7)
        g.line([(-240, 180), (240, 180)], 6, INK, amp=0)
        g.line([(-240, 180), (-240, -190)], 6, INK, amp=0)
        pts = [(-220, -120), (-120, -60), (-20, -90), (80, 40), (200, 150)] if not up else \
              [(-220, 150), (-120, 90), (-20, 30), (80, -60), (200, -170)]
        n = max(2, int(len(pts) * k + 0.999))
        g.line(pts[:n], 14, col, amp=0)
        ex, ey = pts[n - 1]
        g.star(ex, ey, 22, col, 4)


def dvd_stack(g, x, y, sc=1.0, n=5, t=0.0):
    c = g.c
    with g.at(x, y, sc):
        for i in range(n):
            with g.at(6 * math.sin(i * 1.7), -i * 40, 1, 3 * math.sin(i * 2.3)):
                _rr(c, -150, -38, 300, 38, 6)
                _shade(c, FG_BLUE if i % 2 else FG_YEL, 4, 0.2)
                g.text("DVD", 0, -19, 26, "kanit", WHITE if i % 2 else INK)


def placard(g, x, y, sc=1.0, rot=0.0, txt="SAVE FAMILY GUY!"):
    with g.at(x, y, sc, rot):
        g.line([(0, 0), (0, -260)], 10, hexc("#8a6a42"), amp=0)
        g.rrect(-150, -390, 300, 140, 10, WHITE, 6)
        g.text(txt, 0, -320, 30, "kanit", RED)


def voice_card(g, x, y, sc=1.0, rot=0.0, name="ปีเตอร์", sub="", col=FG_BLUE):
    """การ์ดชื่อตัวละครที่เซธพากย์ (ไม่วาดตัวละครลิขสิทธิ์)"""
    with g.at(x, y, sc, rot):
        g.rrect(-200, -80, 400, 160, 30, WHITE, 7, stroke=col)
        g.label(name, 0, -18, 56, color=col)
        if sub:
            g.label(sub, 0, 44, 32, color=GREY)


def teddy(g, x, y, sc=1.0, rot=0.0, t=0.0, smug=True):
    """หมีเท็ดดี้ทั่วไป (ไม่ใช่ตัวละคร Ted ของจริง)"""
    c = g.c
    with g.at(x, y, sc, rot):
        for sx in (-1, 1):
            g.blob(sx * 60, -40, 45, 50, TEDDY, 6, seed=3 + sx)   # ขา
        g.blob(0, -180, 110, 130, TEDDY, 6, seed=5)   # ตัว
        g.blob(0, -180, 60, 80, hexc("#e8c89a"), 4, seed=6)
        for sx in (-1, 1):
            g.blob(sx * 120, -200 + 20 * math.sin(t * 3 + sx), 40, 70, TEDDY, 6, seed=7 + sx)   # แขน
        for sx in (-1, 1):
            g.circle(sx * 75, -440, 38, TEDDY, 6)
            g.circle(sx * 75, -440, 18, hexc("#e8c89a"), 0)
        g.blob(0, -360, 105, 95, TEDDY, 6, seed=9)   # หัว
        g.blob(0, -330, 48, 36, hexc("#e8c89a"), 4, seed=10)
        g.circle(0, -350, 14, INK, 0)
        for sx in (-1, 1):
            if smug:
                g.line([(sx * 52 - 14, -395), (sx * 52 + 14, -392)], 7, INK, amp=0)
            else:
                g.circle(sx * 45, -395, 10, INK, 0)
        g.arc(0, -330, 24, 20, 160, 5, INK)


def clapper(g, x, y, sc=1.0, rot=0.0, t=0.0):
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -150, -60, 300, 180, 8)
        _shade(c, hexc("#2b2b30"), 6, 0.1)
        with g.at(-150, -60, 1, -20 * abs(math.sin(t * 3))):
            _rr(c, 0, -50, 300, 50, 6)
            _shade(c, hexc("#2b2b30"), 6, 0)
            for k in range(5):
                c.new_path()
                for p in [(20 + k * 60, -50), (50 + k * 60, -50), (30 + k * 60, 0), (0 + k * 60, 0)]:
                    c.line_to(*p)
                c.close_path()
                c.set_source_rgb(1, 1, 1)
                c.fill()
        g.text("TED", 0, 40, 60, "kanit", WHITE)


def money(g, x, y, sc=1.0, t=0.0):
    with g.at(x, y, sc):
        for i in range(5):
            with g.at(-120 + i * 60, -i * 30, 1, -10 + 5 * i):
                g.rrect(-90, -45, 180, 90, 8, hexc("#8ac47a"), 5)
                g.circle(0, 0, 26, hexc("#5a9a4a"), 3)
                g.text("$", 0, 0, 36, "kanit", WHITE)
