"""ตัวละครและพร็อพ: วันเกิดดีเอโก มาราโดนา (30 ต.ค. 1960)
ไม่วาดโลโก้สมาคม/สโมสร และไม่วาดถ้วยฟุตบอลโลกของจริง (ใช้ถ้วยทองทั่วไปแทน)
ด้านมืด (ยาเสพติด/มาเฟีย) ใช้พาดหัวข่าว/เงา ไม่แสดงยา"""
import importlib.util
import math
import os

from gfx import GOLD, GOLD2, GREY, INK, NAVY, RED, WHITE, hexc
from people import Look, _rr, _shade, _smooth_path, _stroke


def _load(ep):
    spec = importlib.util.spec_from_file_location(f"{ep}_chars",
                                                  os.path.join(os.path.dirname(__file__), "..", ep, "chars.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


_pe = _load("pele1940")
_cr = _load("crash1929")
ball, jersey = _pe.ball, _pe.jersey
headline = _cr.headline

ARG = hexc("#75aadb")
NAP = hexc("#1e7fcb")
ENG_NAVY = hexc("#22305a")
SKIN_D = hexc("#c9946a")
HAIR_D = hexc("#2b2018")
PITCH = hexc("#7fb069")
PITCH2 = hexc("#74a45f")

# ดีเอโก มาราโดนา: ตัวเตี้ยล่ำ ผมดำหยิกฟู ยิ้มกว้าง — เสื้อทีมชาติแถบฟ้า-ขาว กางเกงดำ ถุงเท้าขาว
MARADONA = Look(hair="afro", hair_col=HAIR_D, skin=SKIN_D, outfit="tee", suit=WHITE, vstripe=ARG, pants=INK,
                shorts=True, socks=WHITE, shoes=INK, w=58, jaw=0.55, nose=1.05, brow=1.2, age=0.1, build=1.08,
                height=0.88)
MARADONA_NAP = Look(hair="afro", hair_col=HAIR_D, skin=SKIN_D, outfit="tee", suit=NAP, pants=WHITE, shorts=True,
                    socks=WHITE, shoes=INK, w=58, jaw=0.55, nose=1.05, brow=1.2, age=0.15, build=1.08, height=0.88)
KID = Look(hair="afro", hair_col=HAIR_D, skin=SKIN_D, outfit="tee", suit=hexc("#d9cdb2"), pants=hexc("#5a5a60"),
           shorts=True, socks=SKIN_D, shoes=SKIN_D, w=54, age=0.0, height=0.6, headsc=1.45, build=0.9)
TEEN = Look(hair="afro", hair_col=HAIR_D, skin=SKIN_D, outfit="tee", suit=WHITE, vstripe=ARG, pants=INK,
            shorts=True, socks=WHITE, shoes=INK, w=56, age=0.0, height=0.8, headsc=1.15)
ENGLAND = [
    Look(hair="short", hair_col=hexc("#8a6a42"), outfit="tee", suit=WHITE, pants=ENG_NAVY, shorts=True, socks=WHITE,
         w=56, age=0.2),
    Look(hair="part", hair_col=hexc("#3a2f28"), outfit="tee", suit=WHITE, pants=ENG_NAVY, shorts=True, socks=WHITE,
         w=56, age=0.25, facial="mustache"),
    Look(hair="short", hair_col=hexc("#c9a46a"), outfit="tee", suit=WHITE, pants=ENG_NAVY, shorts=True, socks=WHITE,
         w=56, age=0.2),
]
KEEPER = Look(hair="part", hair_col=hexc("#5a4632"), outfit="tee", suit=hexc("#9aa3ad"), pants=INK, shorts=True,
              socks=hexc("#9aa3ad"), w=58, age=0.4)
FANS = [
    Look(hair="short", hair_col=HAIR_D, outfit="tee", suit=WHITE, vstripe=ARG, pants=hexc("#3a4a6a"), skin=SKIN_D,
         w=56),
    Look(hair="bun", hair_col=hexc("#3a2a1e"), outfit="dress", suit=ARG, skin=hexc("#e2b08a"), w=54, height=0.93),
    Look(hair="long", hair_col=HAIR_D, outfit="tee", suit=NAP, pants=hexc("#3a3a40"), skin=hexc("#d9a882"), w=55),
]


def trophy(g, x, y, sc=1.0, rot=0.0, t=0.0, shine=1.0):
    """ถ้วยแชมป์ทองทั่วไป (ไม่ใช่ถ้วยฟุตบอลโลกของจริง)"""
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -80, -70, 160, 70, 10)
        _shade(c, hexc("#2f6a3a"), 5, 0.2)
        _rr(c, -40, -160, 80, 100, 10)
        _shade(c, GOLD, 5, 0.3)
        _smooth_path(c, [(-110, -330), (110, -330), (90, -230), (0, -170), (-90, -230)])
        _shade(c, GOLD, 6, 0.35)
        for sx in (-1, 1):
            c.new_path()
            c.arc(sx * 115, -280, 40, 0, 2 * math.pi)
            c.set_source_rgba(*INK)
            c.set_line_width(14)
            c.stroke()
            c.new_path()
            c.arc(sx * 115, -280, 40, 0, 2 * math.pi)
            c.set_source_rgba(*GOLD)
            c.set_line_width(8)
            c.stroke()
        _stroke(c, [(-60, -310), (-50, -250)], 7, WHITE, 0.6)
    if shine > 0:
        g.sparkle(x + 70 * sc, y - 330 * sc, 28 * sc * (0.6 + 0.4 * math.sin(t * 6)), GOLD2)


def shack(g, x, y, sc=1.0, col=hexc("#b8865a"), roof=hexc("#8a9098")):
    """บ้านดิน/สังกะสีในสลัม"""
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -110, -170, 220, 170, 4)
        _shade(c, col, 6, 0.25)
        _smooth_path(c, [(-130, -160), (130, -190), (130, -170), (-130, -140)])
        _shade(c, roof, 5, 0.2)
        for k in range(5):
            _stroke(c, [(-110 + k * 52, -170 + k * -6), (-110 + k * 52, -155 + k * -6)], 3, INK, 0.4, smooth=False)
        _rr(c, -30, -100, 60, 100, 4)
        _shade(c, hexc("#5a3a22"), 4, 0.1)


def slum(g, y, t=0.0):
    cols = [hexc("#b8865a"), hexc("#c9a070"), hexc("#a8765a"), hexc("#d0b080")]
    for i in range(6):
        shack(g, 60 + i * 190, y - 10 * (i % 2), 0.7 + 0.1 * (i % 2), cols[i % 4])


def pitch(g, x, y, w, h, t=0.0):
    """สนามมองจากบน (ครึ่งสนาม ประตูอยู่ด้านขวา)"""
    c = g.c
    with g.at(x, y):
        _rr(c, -w / 2, -h / 2, w, h, 10)
        _shade(c, PITCH, 6, 0.05)
        for k in range(6):
            if k % 2:
                c.rectangle(-w / 2 + k * w / 6, -h / 2, w / 6, h)
                c.set_source_rgba(*PITCH2[:3], 1)
                c.fill()
        _stroke(c, [(-w / 2, -h / 2), (-w / 2, h / 2)], 5, WHITE, 1, smooth=False)
        c.new_path()
        c.arc(-w / 2, 0, h * 0.18, -math.pi / 2, math.pi / 2)
        c.set_source_rgba(*WHITE)
        c.set_line_width(5)
        c.stroke()
        bx = w / 2 - 160
        c.rectangle(bx, -h * 0.3, 160, h * 0.6)
        c.stroke()
        c.rectangle(w / 2 - 60, -h * 0.14, 60, h * 0.28)
        c.stroke()
        _rr(c, w / 2, -h * 0.09, 26, h * 0.18, 4)
        _shade(c, WHITE, 4, 0.1)


def goal(g, x, y, sc=1.0, ball_in=0.0, t=0.0):
    """ประตูฟุตบอล (มองด้านหน้า) + ตาข่าย"""
    c = g.c
    with g.at(x, y, sc):
        for i in range(9):
            _stroke(c, [(-300 + i * 75, -300), (-300 + i * 75, 0)], 2.5, GREY, 0.7, smooth=False)
        for j in range(5):
            _stroke(c, [(-300, -300 + j * 75), (300, -300 + j * 75)], 2.5, GREY, 0.7, smooth=False)
        _stroke(c, [(-300, 0), (-300, -300), (300, -300), (300, 0)], 16, WHITE, 1, smooth=False)
        _stroke(c, [(-300, 0), (-300, -300), (300, -300), (300, 0)], 4, INK, 0.6, smooth=False)
    if ball_in > 0:
        ball(g, x + 120 * sc, y - 120 * sc - 10 * math.sin(t * 8) * (1 - ball_in), 40 * sc)


def falklands(g, x, y, sc=1.0, t=0.0, k=1.0):
    """แผนที่อเมริกาใต้ปลายล่าง + หมู่เกาะฟอล์กแลนด์ (อย่างง่าย)"""
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -320, -360, 640, 720, 30)
        _shade(c, hexc("#bcd8ec"), 6, 0.05)
        _smooth_path(c, [(-200, -360), (40, -360), (60, -200), (0, -40), (-40, 120), (-80, 300), (-120, 340),
                         (-170, 200), (-200, 0), (-230, -200)])
        _shade(c, hexc("#e9dfc8"), 5, 0.1)
        g.label("อาร์เจนตินา", -120, -100, 40, color=INK)
        with g.at(150, 230, k):
            g.blob(-30, 0, 50, 26, hexc("#e9dfc8"), 5, seed=3)
            g.blob(40, 6, 46, 24, hexc("#e9dfc8"), 5, seed=5)
            for i in range(3):
                u = (t * 0.8 + i / 3) % 1
                g.circle(0, 0, 70 + 70 * u, (0.75, 0.2, 0.2, 0.3 * (1 - u)), 4)
        g.label("ฟอล์กแลนด์", 150, 310, 40, color=RED, sc=k)


def hand_ball(g, x, y, sc=1.0, t=0.0):
    """มือซ้ายปัดบอล (ภาพใกล้)"""
    c = g.c
    with g.at(x, y, sc, -20 + 6 * math.sin(t * 3)):
        _rr(c, -40, 0, 80, 200, 30)
        _shade(c, SKIN_D, 6, 0.25)
        _smooth_path(c, [(-60, 20), (-70, -80), (-50, -110), (50, -110), (70, -70), (60, 20)])
        _shade(c, SKIN_D, 6, 0.25)
        for k in (-40, -14, 12, 38):
            _stroke(c, [(k, -110), (k, -150)], 22, SKIN_D, 1, smooth=False)
            _stroke(c, [(k, -110), (k, -150)], 3, INK, 0.3, smooth=False)
    ball(g, x + 40 * sc, y - 230 * sc, 70 * sc, t * 2)


def halo(g, x, y, r, col=GOLD2):
    c = g.c
    c.save()
    c.translate(x, y)
    c.scale(1, 0.3)
    c.new_path()
    c.arc(0, 0, r, 0, 2 * math.pi)
    c.restore()
    c.set_source_rgba(*INK)
    c.set_line_width(14)
    c.stroke()
    c.save()
    c.translate(x, y)
    c.scale(1, 0.3)
    c.new_path()
    c.arc(0, 0, r, 0, 2 * math.pi)
    c.restore()
    c.set_source_rgba(*col)
    c.set_line_width(8)
    c.stroke()


def horns(g, x, y, s=1.0):
    for sx in (-1, 1):
        g.poly([(x + sx * 40 * s, y), (x + sx * 70 * s, y - 70 * s), (x + sx * 80 * s, y + 5 * s)], RED, 5, amp=0)


def vesuvius(g, y, t=0.0):
    """อ่าวเนเปิลส์ + ภูเขาไฟวิสุเวียส"""
    c = g.c
    _smooth_path(c, [(-400, y), (250, y - 420), (420, y - 440), (600, y - 300), (1500, y)])
    _shade(c, hexc("#a89a8a"), 6, 0.2)
    for i in range(3):
        u = (t * 0.2 + i / 3) % 1
        g.circle(330 + 30 * math.sin(i + t), y - 460 - 120 * u, 40 + 30 * u, (0.85, 0.85, 0.88, 0.7 * (1 - u)), 0)
    cols = [hexc("#e8c87a"), hexc("#e8a07a"), hexc("#f2ead6"), hexc("#d9b08a")]
    for i in range(8):
        x = 40 + i * 130
        h = 90 + (i * 37) % 60
        _rr(c, x - 55, y - h, 110, h, 4)
        _shade(c, cols[i % 4], 4, 0.2)
        for k in range(2):
            _rr(c, x - 30 + k * 40, y - h + 20, 20, 24, 2)
            _shade(c, hexc("#3a5a8a"), 2, 0)


def italy(g, x, y, sc=1.0, t=0.0, south=1.0):
    """แผนที่อิตาลีอย่างง่าย: เหนือ (รวย) vs ใต้ (เนเปิลส์)"""
    c = g.c
    with g.at(x, y, sc):
        _smooth_path(c, [(-180, -380), (120, -390), (80, -280), (20, -150), (90, -40), (180, 60), (230, 150),
                         (170, 170), (240, 260), (180, 330), (110, 220), (40, 120), (-60, 20), (-140, -120),
                         (-200, -250)])
        _shade(c, hexc("#e9dfc8"), 6, 0.15)
        g.label("เหนือ", -40, -270, 50, color=GREY)
        with g.at(60, 70, south):
            g.circle(0, 0, 26, NAP, 5)
        g.label("เนเปิลส์", 140, 20, 50, color=NAP, sc=south)


def scudetto(g, x, y, sc=1.0, rot=0.0):
    """โล่สามสีแชมป์ลีกอิตาลี (ทั่วไป)"""
    c = g.c
    with g.at(x, y, sc, rot):
        pts = [(-110, -140), (110, -140), (110, 20), (0, 150), (-110, 20)]
        _smooth_path(c, pts)
        _shade(c, WHITE, 7, 0.1)
        c.save()
        _smooth_path(c, pts)
        c.clip()
        c.rectangle(-110, -150, 74, 320)
        c.set_source_rgba(*hexc("#2f9a4f")[:3], 1)
        c.fill()
        c.rectangle(36, -150, 74, 320)
        c.set_source_rgba(*hexc("#d64040")[:3], 1)
        c.fill()
        c.restore()
        _smooth_path(c, pts)
        c.set_source_rgba(*INK)
        c.set_line_width(7)
        c.stroke()


def sword(g, x, y, sc=1.0, rot=0.0, split=1.0):
    """ดาบสองคม: ครึ่งสว่าง/ครึ่งมืด"""
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -20, 40, 40, 160, 10)
        _shade(c, hexc("#6e4528"), 5, 0.2)
        _rr(c, -110, 20, 220, 30, 10)
        _shade(c, GOLD, 5, 0.3)
        pts = [(-40, 20), (-40, -440), (0, -520), (40, -440), (40, 20)]
        _smooth_path(c, pts)
        _shade(c, hexc("#e9ecf0"), 6, 0.1)
        if split > 0:
            c.save()
            _smooth_path(c, pts)
            c.clip()
            c.rectangle(0, -530, 50, 560)
            c.set_source_rgba(0.15, 0.15, 0.2, 0.85 * split)
            c.fill()
            c.restore()


def heart(g, x, y, s=1.0, col=RED):
    c = g.c
    with g.at(x, y, s):
        c.new_path()
        c.move_to(0, 40)
        c.curve_to(-90, -20, -50, -90, 0, -45)
        c.curve_to(50, -90, 90, -20, 0, 40)
        c.close_path()
        _shade(c, col, 5, 0.2)
