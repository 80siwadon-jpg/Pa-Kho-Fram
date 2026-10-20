"""ตัวละครและพร็อพ: ข้อมติสมัชชาใหญ่ UN ที่ 2758 (25 ต.ค. 1971) — ห้องประชุมสมัชชาใหญ่, กระดานคะแนน, เก้าอี้ "CHINA"
เล่าเป็นกลาง: ธงสองฝ่ายวาดตามจริงแบบเรียบง่าย ไม่ล้อเลียนฝ่ายใด"""
import math

from gfx import GOLD, GOLD2, GREY, INK, NAVY, RED, WHITE, hexc
from people import Look, _rr, _shade, _smooth_path, _stroke

UN_BLUE = hexc("#4b92db")
HALL = hexc("#2f5a7a")
CN_RED = hexc("#de2910")
CN_YEL = hexc("#ffde00")
ROC_BLUE = hexc("#000095")
ASIA_SKIN = hexc("#eac39e")

# เจียง ไคเชก: ศีรษะล้าน หนวดบางสีเทา เครื่องแบบคอปิดสีกากี
CHIANG = Look(hair="bald", hair_col=hexc("#9a948a"), suit=hexc("#b8a77a"), collar=hexc("#b8a77a"), outfit="tunic",
              pants=hexc("#b8a77a"), facial="mustache", w=55, jaw=0.35, nose=0.95, brow=0.7, age=0.75,
              skin=ASIA_SKIN)
# เหมา เจ๋อตง: หน้าผากกว้าง ผมหวีเสยไปด้านหลัง หน้ากลม ชุดจงซานสีเทา
MAO = Look(hair="slick", hair_col=hexc("#1f1b18"), suit=hexc("#8a8e86"), collar=hexc("#8a8e86"), outfit="tunic",
           pants=hexc("#8a8e86"), w=61, jaw=0.75, jowls=0.25, nose=0.95, brow=0.8, age=0.5, build=1.12,
           skin=ASIA_SKIN)
# ผู้แทนไต้หวันในห้องประชุม (โจว ซูไข่ — ไม่ใส่ชื่อในคลิป เพราะบทไม่เอ่ยชื่อ)
ROC_DELEGATE = Look(hair="slick", hair_col=hexc("#1f1b18"), suit=hexc("#2f3036"), tie=hexc("#2b3f63"),
                    glasses="thick", w=56, age=0.55, skin=ASIA_SKIN)
DELEGATES = [   # ผู้แทนประเทศต่าง ๆ ปี 1971
    Look(hair="short", hair_col=hexc("#1b1714"), suit=hexc("#3a3a40"), tie=hexc("#3c8d4f"), skin=hexc("#7a4a2c"),
         w=57, age=0.4),
    Look(hair="part", hair_col=hexc("#6a5a4a"), suit=hexc("#2f3a4a"), tie=hexc("#7a2e2e"), w=56, age=0.6,
         glasses="thin"),
    Look(hair="slick", hair_col=hexc("#1b1714"), suit=hexc("#4a4038"), tie=hexc("#d9a441"), skin=hexc("#c99a6a"),
         w=56, age=0.45, facial="mustache"),
    Look(hair="afro", hair_col=hexc("#1b1714"), suit=hexc("#2b2622"), tie=hexc("#e8892e"), skin=hexc("#5a3a26"),
         w=56, age=0.3),
    Look(hair="bun", hair_col=hexc("#5a4a3a"), outfit="dress", suit=hexc("#6a3a4a"), w=54, age=0.45, height=0.93),
]


def flag(g, x, y, w, kind, t=0.0, pole=True, k=1.0):
    """ธงโบกที่มุมบนซ้าย (x, y): kind = prc / roc / un"""
    if k < 0.02:
        return
    c = g.c
    h = w * 2 / 3
    with g.at(x, y, k):
        if pole:
            g.line([(0, -20), (0, h + 260)], 7, hexc("#8a8a8a"), amp=0)
        n = 14

        def pt(u, v):
            return u * w, v * h + h * 0.06 * math.sin(t * 5 + u * 5) * u

        c.save()
        c.new_path()
        for i in range(n + 1):
            c.line_to(*pt(i / n, 0))
        for i in range(n, -1, -1):
            c.line_to(*pt(i / n, 1))
        c.close_path()
        c.clip_preserve()
        base = {"prc": CN_RED, "roc": CN_RED, "un": UN_BLUE}[kind]
        c.set_source_rgba(*base)
        c.fill()
        if kind == "prc":
            sx, sy = pt(0.17, 0.25)
            g.star(sx, sy, h * 0.15, CN_YEL, 0, stroke=CN_YEL)
            for (u, v, r) in ((0.33, 0.1, 0), (0.4, 0.2, 20), (0.4, 0.35, 0), (0.33, 0.45, 20)):
                px, py = pt(u, v)
                g.star(px, py, h * 0.05, CN_YEL, 0, rot=-90 + r, stroke=CN_YEL)
        elif kind == "roc":
            c.new_path()
            x0, y0 = pt(0, 0)
            c.rectangle(x0, y0 - 4, w * 0.5, h * 0.5 + 4)
            c.set_source_rgba(*ROC_BLUE)
            c.fill()
            cx, cy = pt(0.25, 0.25)
            for i in range(12):
                a = i * math.pi / 6
                c.new_path()
                c.move_to(cx + h * 0.08 * math.cos(a + 0.26), cy + h * 0.08 * math.sin(a + 0.26))
                c.line_to(cx + h * 0.19 * math.cos(a), cy + h * 0.19 * math.sin(a))
                c.line_to(cx + h * 0.08 * math.cos(a - 0.26), cy + h * 0.08 * math.sin(a - 0.26))
                c.close_path()
                c.set_source_rgb(1, 1, 1)
                c.fill()
            c.new_path()
            c.arc(cx, cy, h * 0.1, 0, 2 * math.pi)
            c.set_source_rgba(*ROC_BLUE)
            c.fill()
            c.new_path()
            c.arc(cx, cy, h * 0.085, 0, 2 * math.pi)
            c.set_source_rgb(1, 1, 1)
            c.fill()
        else:
            cx, cy = pt(0.5, 0.5)
            c.new_path()
            c.arc(cx, cy, h * 0.25, 0, 2 * math.pi)
            c.set_source_rgb(1, 1, 1)
            c.set_line_width(5)
            c.stroke()
            for a in (-0.5, 0.5):
                _stroke(c, [(cx - h * 0.25, cy + a * h * 0.2), (cx + h * 0.25, cy + a * h * 0.2)], 3, WHITE)
        c.restore()
        c.new_path()
        for i in range(n + 1):
            c.line_to(*pt(i / n, 0))
        for i in range(n, -1, -1):
            c.line_to(*pt(i / n, 1))
        c.close_path()
        c.set_source_rgba(*INK[:3], 1)
        c.set_line_width(5)
        c.stroke()


def emblem(g, x, y, r, t=0.0):
    """ตราลูกโลก+ช่อมะกอกบนผนังห้องประชุม (การ์ตูน ไม่ใช่โลโก้จริง)"""
    c = g.c
    c.new_path()
    c.arc(x, y, r, 0, 2 * math.pi)
    _shade(c, GOLD, 6, 0.25)
    for k in (0.33, 0.66):
        c.new_path()
        c.arc(x, y, r * k, 0, 2 * math.pi)
        c.set_source_rgba(*INK[:3], 0.4)
        c.set_line_width(3)
        c.stroke()
    _stroke(c, [(x - r, y), (x + r, y)], 3, INK, 0.4, smooth=False)
    _stroke(c, [(x, y - r), (x, y + r)], 3, INK, 0.4, smooth=False)
    for sx in (-1, 1):
        for i in range(6):
            a = math.pi / 2 + sx * (0.35 + i * 0.27)
            lx, ly = x + (r + 30) * math.cos(a) * -1, y + (r + 30) * math.sin(a)
            c.save()
            c.translate(lx, ly)
            c.rotate(a)
            c.scale(1, 0.45)
            c.new_path()
            c.arc(0, 0, 22, 0, 2 * math.pi)
            c.restore()
            _shade(c, GOLD2, 3, 0.15)


def hall(g, y_floor, t=0.0, a=1.0):
    """ห้องประชุมสมัชชาใหญ่: ผนังทอง + ตรากลาง + แท่นประธาน"""
    c = g.c
    c.save()
    c.rectangle(-500, 120, 2100, y_floor - 120)
    c.clip()
    grad_top = hexc("#e9d9a6")
    c.set_source_rgba(*grad_top[:3], 0.55 * a)
    c.paint()
    for i in range(-6, 16):
        _stroke(c, [(i * 90, 120), (i * 90, y_floor)], 3, hexc("#c9b273"), 0.5 * a, smooth=False)
    c.restore()
    emblem(g, 540, 580, 90, t)


def rostrum(g, x, y, sc=1.0):
    """แท่นประธานสมัชชา"""
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -260, -260, 520, 260, 10)
        _shade(c, hexc("#5a7a8a"), 6, 0.25)
        _rr(c, -200, -200, 400, 120, 8)
        _shade(c, hexc("#4a6a7a"), 4, 0.1)
        _rr(c, -60, -320, 120, 70, 8)
        _shade(c, hexc("#3a4a5a"), 4, 0.1)


def board(g, x, y, sc=1.0, yes=76, no=35, ab=17, k=1.0, t=0.0):
    """กระดานคะแนนเสียงไฟฟ้า"""
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -330, -230, 660, 460, 24)
        _shade(c, hexc("#20283a"), 7, 0.15)
        rows = (("YES", yes, hexc("#5bd06a")), ("NO", no, hexc("#f05a5a")), ("ABSTAIN", ab, hexc("#f2c94c")))
        for i, (lab, n, col) in enumerate(rows):
            yy = -130 + i * 130
            g.text(lab, -150, yy, 54, fnt="kanit", color=col)
            v = int(round(n * k))
            g.text(str(v), 180, yy, 84, fnt="kanit", color=col)
            if i == 0 and k >= 1:
                for j in range(3):
                    g.sparkle(270 + 30 * j, yy - 60 + 20 * math.sin(t * 6 + j), 14)


def seat(g, x, y, sc=1.0, rot=0.0, plate="CHINA", empty=True):
    """เก้าอี้ผู้แทน + ป้ายชื่อประเทศ"""
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -110, -360, 220, 230, 30)
        _shade(c, hexc("#2f6f9a"), 6, 0.3)
        _rr(c, -130, -150, 260, 60, 16)
        _shade(c, hexc("#2f6f9a"), 6, 0.2)
        for sx in (-1, 1):
            g.line([(sx * 100, -90), (sx * 110, 0)], 10, INK, amp=0)
        if plate:
            _rr(c, -150, -470, 300, 80, 8)
            _shade(c, WHITE, 5, 0.1)
            g.text(plate, 0, -432, 50, fnt="kanit", color=INK)


def desk(g, x, y, w=900, plate="", sc=1.0):
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -w / 2, -150, w, 150, 10)
        _shade(c, hexc("#b88a52"), 6, 0.25)
        if plate:
            _rr(c, -120, -220, 240, 70, 6)
            _shade(c, WHITE, 4, 0.1)
            g.text(plate, 0, -186, 42, fnt="kanit", color=INK)


def ballot(g, x, y, sc=1.0, rot=0.0, title="A/RES/2758"):
    """กระดาษข้อมติ"""
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -150, -200, 300, 400, 8)
        _shade(c, WHITE, 6, 0.12)
        g.text(title, 0, -140, 36, fnt="kanit", color=UN_BLUE)
        for i in range(7):
            _stroke(c, [(-110, -80 + i * 34), (110 - 40 * (i % 3), -80 + i * 34)], 4, INK, 0.4, smooth=False)
        c.new_path()
        c.arc(80, 150, 30, 0, 2 * math.pi)
        c.set_source_rgba(*UN_BLUE[:3], 0.8)
        c.set_line_width(4)
        c.stroke()


def gavel(g, x, y, sc=1.0, rot=0.0):
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -10, -20, 20, 220, 8)
        _shade(c, hexc("#8a5a3a"), 5, 0.2)
        _rr(c, -80, -70, 160, 70, 20)
        _shade(c, hexc("#6a3a22"), 6, 0.25)


def door(g, x, y, sc=1.0, closed=1.0, lock=True):
    """ประตูบานใหญ่ปิดตาย"""
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -220, -560, 440, 560, 20)
        _shade(c, hexc("#7a5a3a"), 7, 0.25)
        g.line([(0, -560), (0, 0)], 6, INK, amp=0)
        for sx in (-1, 1):
            _rr(c, sx * 110 - 70, -500, 140, 200, 8)
            _shade(c, hexc("#6a4a2e"), 4, 0.1)
            _rr(c, sx * 110 - 70, -260, 140, 200, 8)
            _shade(c, hexc("#6a4a2e"), 4, 0.1)
        if lock:
            _rr(c, -260, -320, 520, 50, 8)
            _shade(c, hexc("#8a8a8a"), 5, 0.2)
            _rr(c, -45, -340, 90, 90, 14)
            _shade(c, GOLD, 5, 0.25)


def veto_stamp(g, x, y, sc=1.0, rot=-12):
    with g.at(x, y, sc, rot):
        g.rrect(-200, -80, 400, 160, 20, (1, 1, 1, 0), 10, stroke=RED)
        g.text("VETO", 0, 0, 96, fnt="kanit", color=RED)


def island(g, x, y, sc=1.0, t=0.0):
    """เกาะลอยกลางทะเล (ภาวะโดดเดี่ยว)"""
    c = g.c
    with g.at(x, y, sc):
        for i in range(3):
            u = (t * 0.4 + i / 3) % 1
            c.new_path()
            c.save()
            c.scale(1, 0.3)
            c.arc(0, 40, 200 + 260 * u, 0, 2 * math.pi)
            c.restore()
            c.set_source_rgba(0.3, 0.55, 0.8, 0.6 * (1 - u))
            c.set_line_width(5)
            c.stroke()
        _smooth_path(c, [(-80, -150), (0, -190), (70, -120), (90, 0), (40, 120), (-20, 90), (-70, -20)])
        _shade(c, hexc("#6fae5a"), 6, 0.3)
        _smooth_path(c, [(-20, -80), (20, -110), (40, -30), (0, 20), (-30, -20)])
        _shade(c, hexc("#4f8a42"), 3, 0.2)


def crowd_icon(g, x, y, sc=1.0, col=GREY):
    with g.at(x, y, sc):
        g.circle(0, -60, 22, col, 4)
        g.rrect(-30, -34, 60, 60, 24, col, 4)
