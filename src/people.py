"""คนแบบกึ่งเสมือนจริง (ภาพประกอบสารคดี): สัดส่วนคนจริง ~6.5 หัว, หน้าตามีจมูก/คิ้ว/ตาจริง, แรเงานุ่ม ๆ
ใช้: from people import Look, person
    NIXON = Look(hair="nixon", jowls=1.0, nose=1.4, suit=hexc("#27324a"), ...)
    person(g, x, y, NIXON, sc=1.0, mood="angry", pose="point", talk=True, turn=0.3)
จุดกำเนิด = ปลายเท้า, ความสูงราว 900 หน่วยที่ sc=1 (หัวอยู่ราว y=-850)
mood: neutral, smile, smug, angry, shout, worry, shock, firm, sad
pose: down, point, fist, v, hold, stop, phone, cross, sign, think, wave
"""
import math
from dataclasses import dataclass

import cairo

from gfx import INK, WHITE, hexc, lerp

SKIN_R = hexc("#efc4a1")
SHADOW = (0.12, 0.09, 0.1)


@dataclass
class Look:
    hair: str = "short"            # nixon, crew, slick, part, full, bald
    hair_col: tuple = hexc("#3a2f28")
    skin: tuple = SKIN_R
    suit: tuple = hexc("#30343c")
    shirt: tuple = WHITE
    tie: tuple = hexc("#7a2e2e")
    bowtie: bool = False
    w: float = 60.0                # ครึ่งความกว้างหัว
    jaw: float = 0.4               # 0 = คางแหลม, 1 = กรามใหญ่
    jowls: float = 0.0             # แก้มย้อย (นิกสัน)
    nose: float = 1.0              # ความยาว/ขนาดจมูก
    brow: float = 1.0              # ความหนาคิ้ว
    glasses: str = ""              # "" / thick / thin
    stubble: float = 0.0
    age: float = 0.5               # ริ้วรอย
    build: float = 1.0             # ความกว้างลำตัว
    height: float = 1.0
    pin: bool = False              # เข็มกลัดธงชาติ


def _shade(c, fill, lw=4.5, dark=0.24, horiz=True, stroke=INK):
    """เติมสี + ไล่เงาจากด้านซ้ายบน (แสง) ไปขวาล่าง แล้วตัดเส้น — ต้องสร้าง path ไว้ก่อนเรียก"""
    x0, y0, x1, y1 = c.fill_extents()
    c.set_source_rgba(*fill)
    c.fill_preserve()
    if dark > 0 and x1 > x0:
        g = cairo.LinearGradient(x0, y0, x1, y0) if horiz else cairo.LinearGradient(x0, y0, x0, y1)
        g.add_color_stop_rgba(0.0, 1, 1, 1, 0.10)
        g.add_color_stop_rgba(0.45, *SHADOW, 0.0)
        g.add_color_stop_rgba(1.0, *SHADOW, dark)
        c.set_source(g)
        c.fill_preserve()
    if lw:
        c.set_source_rgba(*stroke)
        c.set_line_width(lw)
        c.set_line_join(cairo.LINE_JOIN_ROUND)
        c.set_line_cap(cairo.LINE_CAP_ROUND)
        c.stroke()
    else:
        c.new_path()


def _stroke(c, pts, lw=4, col=INK, a=1.0, smooth=True):
    from gfx import Draw
    c.new_path()
    if smooth and len(pts) > 2:
        Draw.smooth(_Fake(c), pts, closed=False)
    else:
        c.move_to(*pts[0])
        for p in pts[1:]:
            c.line_to(*p)
    c.set_source_rgba(col[0], col[1], col[2], a * (col[3] if len(col) > 3 else 1))
    c.set_line_width(lw)
    c.set_line_cap(cairo.LINE_CAP_ROUND)
    c.set_line_join(cairo.LINE_JOIN_ROUND)
    c.stroke()


class _Fake:
    def __init__(self, c):
        self.c = c


def _smooth_path(c, pts, closed=True):
    from gfx import Draw
    c.new_path()
    Draw.smooth(_Fake(c), pts, closed)


# ---------------------------------------------------------------- ท่าทาง (มุมต้นแขน, มุมแขนท่อน่าง) องศา 0 = ห้อยลง, + = กางออกด้านข้าง
POSES = {
    "down":  ((6, 2), (6, 2), "open", "open"),
    "point": ((6, 2), (78, 92), "open", "point"),
    "fist":  ((6, 2), (35, 165), "open", "fist"),
    "v":     ((150, 160), (150, 160), "v", "v"),
    "hold":  ((10, -70), (10, -70), "open", "open"),
    "stop":  ((6, 2), (30, 160), "open", "palm"),
    "phone": ((6, 2), (-18, -172), "open", "fist"),
    "cross": ((12, -95), (12, -95), "fist", "fist"),
    "sign":  ((6, 2), (14, -75), "open", "pen"),
    "think": ((6, 2), (-12, -168), "open", "fist"),
    "wave":  ((6, 2), (100, 172), "open", "palm"),
    "shrug": ((28, 100), (28, 100), "palm", "palm"),
    "slam":  ((6, 2), (30, 60), "open", "fist"),
}


def _arm(c, look, sx, ang, hand, lw, t):
    """แขนข้างหนึ่ง (sx=-1 ซ้ายจอ, +1 ขวาจอ) จากไหล่"""
    a1, a2 = math.radians(ang[0]), math.radians(ang[1])
    L1, L2 = 150, 140
    sh = (sx * 112 * look.build, -705)
    el = (sh[0] + sx * math.sin(a1) * L1, sh[1] + math.cos(a1) * L1)
    wr = (el[0] + sx * math.sin(a2) * L2, el[1] + math.cos(a2) * L2)
    for wd, col in ((50 + 2 * lw, INK), (50, look.suit)):
        _stroke(c, [sh, el, wr], wd, col, smooth=False)
    # ไล่เงาที่แขนเสื้อ
    _stroke(c, [(sh[0] + sx * 10, sh[1] + 6), (el[0] + sx * 10, el[1]), (wr[0] + sx * 8, wr[1])], 13, (*SHADOW, 0.22), smooth=False)
    # ข้อมือเสื้อเชิ้ต
    d = (wr[0] - el[0], wr[1] - el[1])
    n = math.hypot(*d) or 1
    ux, uy = d[0] / n, d[1] / n
    cf = (wr[0] - ux * 4, wr[1] - uy * 4)
    _stroke(c, [(cf[0] - uy * 24, cf[1] + ux * 24), (cf[0] + uy * 24, cf[1] - ux * 24)], 14 + 2 * lw, INK, smooth=False)
    _stroke(c, [(cf[0] - uy * 24, cf[1] + ux * 24), (cf[0] + uy * 24, cf[1] - ux * 24)], 14, look.shirt, smooth=False)
    _hand(c, look, wr[0] + ux * 22, wr[1] + uy * 22, math.atan2(uy, ux), hand, sx, lw)
    return wr


def _hand(c, look, x, y, ang, kind, sx, lw):
    c.save()
    c.translate(x, y)
    c.rotate(ang - math.pi / 2)
    if sx < 0:
        c.scale(-1, 1)
    sk = look.skin
    if kind == "fist":
        c.new_path()
        c.rectangle(-22, -14, 44, 36)
        _rr(c, -22, -14, 44, 38, 14)
        _shade(c, sk, lw)
        for k in (-8, 4):
            _stroke(c, [(k, 12), (k, 24)], 2.5, INK, 0.6)
    elif kind in ("open", "palm"):
        _smooth_path(c, [(-20, -12), (20, -12), (24, 18), (14, 40), (-6, 44), (-20, 26)])
        _shade(c, sk, lw)
        _stroke(c, [(20, 0), (32, 10), (30, 22)], lw, INK)   # นิ้วโป้ง
        for k in (-8, 2, 11):
            _stroke(c, [(k, 26), (k + 1, 40)], 2.5, INK, 0.5)
    elif kind == "point":
        _rr(c, -22, -14, 44, 36, 14)
        _shade(c, sk, lw)
        _rr(c, -6, 14, 13, 46, 6)
        _shade(c, sk, lw)
    elif kind == "v":
        for dx, rot in ((-6, -0.22), (8, 0.22)):
            c.save()
            c.translate(dx, 10)
            c.rotate(rot)
            _rr(c, -6, 0, 13, 50, 6)
            _shade(c, sk, lw)
            c.restore()
        _rr(c, -22, -14, 44, 32, 14)
        _shade(c, sk, lw)
    elif kind == "pen":
        _rr(c, -22, -14, 44, 36, 14)
        _shade(c, sk, lw)
        _stroke(c, [(10, 10), (34, 52)], 7, INK, smooth=False)
    c.restore()


def _rr(c, x, y, w, h, r):
    c.new_path()
    c.new_sub_path()
    c.arc(x + w - r, y + r, r, -math.pi / 2, 0)
    c.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    c.arc(x + r, y + h - r, r, math.pi / 2, math.pi)
    c.arc(x + r, y + r, r, math.pi, 1.5 * math.pi)
    c.close_path()


# ---------------------------------------------------------------- หัว
def head(g, look, mood="neutral", talk=0.0, turn=0.0, look_at=(0, 0), seed=0, lw=4.5):
    """หัวที่จุดกำเนิด = กลางหน้า (ระดับตา ~ -8)"""
    c, t, w = g.c, g.t, look.w
    fx = turn * w * 0.28      # หน้าหันข้าง: ตา/จมูก/ปากเลื่อน

    # ผมด้านหลัง (อยู่หลังหัว)
    _hair_back(c, look, w, lw)
    # หู
    for sx in (-1, 1):
        if sx * turn > 0.5:
            continue
        ex = sx * w * (0.98 - 0.12 * sx * turn)
        c.save()
        c.translate(ex, 4)
        c.scale(1, 1.7)
        c.new_path()
        c.arc(0, 0, 13, 0, 2 * math.pi)
        c.restore()
        _shade(c, look.skin, lw)
        _stroke(c, [(ex - sx * 3, -6), (ex + sx * 4, 4), (ex - sx * 2, 14)], 2.5, INK, 0.5)
    # คอ
    _rr(c, -w * 0.5, 40, w, 70, 10)
    _shade(c, look.skin, lw, 0.35)
    # ทรงหน้า
    j, jw = look.jaw, look.jowls
    pts = [(0, -84), (w * 0.72, -76), (w * 0.98, -46), (w * 1.0, -8), (w * 0.95, 22),
           (w * (0.80 + 0.14 * j + 0.10 * jw), 48 + 6 * jw), (w * (0.46 + 0.22 * j + 0.12 * jw), 72 + 4 * jw),
           (fx * 0.5, 82 + 3 * jw)]
    full = pts + [(-x, y) for x, y in reversed(pts[1:-1])]
    _smooth_path(c, full)
    c.set_source_rgba(*look.skin)
    c.fill_preserve()
    c.save()
    c.clip()
    # หนวดเคราเขียว ๆ (ไล่จางขึ้นไป)
    if look.stubble > 0:
        sg = cairo.LinearGradient(0, 20, 0, 60)
        sg.add_color_stop_rgba(0, 0.2, 0.2, 0.25, 0.0)
        sg.add_color_stop_rgba(1, 0.2, 0.2, 0.25, 0.13 * look.stubble)
        c.set_source(sg)
        c.paint()
    # แก้มแดงอ่อน
    for sx in (-1, 1):
        rg = cairo.RadialGradient(sx * w * 0.55 + fx, 26, 0, sx * w * 0.55 + fx, 26, 22)
        rg.add_color_stop_rgba(0, 0.9, 0.45, 0.4, 0.22)
        rg.add_color_stop_rgba(1, 0.9, 0.45, 0.4, 0.0)
        c.set_source(rg)
        c.paint()
    c.restore()
    _smooth_path(c, full)
    _shade(c, (0, 0, 0, 0), lw, 0.2)
    # ริ้วรอย
    if look.age > 0.4:
        for k in range(int(look.age * 3)):
            _stroke(c, [(-w * 0.35 + fx, -52 + k * 9), (fx, -55 + k * 9), (w * 0.35 + fx, -52 + k * 9)], 2, INK, 0.25)
    if jw > 0:
        for sx in (-1, 1):
            _stroke(c, [(sx * w * 0.36 + fx, 34), (sx * w * 0.5 + fx, 58), (sx * w * 0.62 + fx * 0.5, 74)], 3, INK, 0.45 * jw)
    # ร่องแก้มข้างจมูก
    for sx in (-1, 1):
        _stroke(c, [(sx * 16 + fx, 30), (sx * 24 + fx, 46), (sx * 26 + fx, 58)], 2.5, INK, 0.35 + 0.2 * look.age)

    # ตา
    blink = ((t * 0.5 + seed * 0.37) % 3.4) < 0.09 and mood not in ("shock", "shout")
    ey = -10
    open_ = {"shock": 1.5, "angry": 0.75, "smug": 0.6, "firm": 0.85, "sad": 0.7}.get(mood, 1.0)
    lx, ly = look_at[0] * 5 + turn * 3, look_at[1] * 3
    for sx in (-1, 1):
        ex = sx * w * 0.38 + fx * (1.15 if sx * turn > 0 else 0.85)
        ew = 17 * (1 - 0.25 * max(sx * turn, 0))
        eh = 9 * open_
        if blink:
            _stroke(c, [(ex - ew, ey), (ex, ey + 3), (ex + ew, ey)], 3.5)
        else:
            _smooth_path(c, [(ex - ew, ey), (ex - ew * 0.3, ey - eh), (ex + ew * 0.5, ey - eh * 0.9), (ex + ew, ey),
                             (ex + ew * 0.2, ey + eh * 0.75), (ex - ew * 0.5, ey + eh * 0.6)])
            c.save()
            c.set_source_rgba(1, 1, 1, 1)
            c.fill_preserve()
            c.clip()
            c.new_path()
            c.arc(ex + lx, ey + ly, 7.5, 0, 2 * math.pi)
            c.set_source_rgba(0.33, 0.25, 0.18, 1)
            c.fill()
            c.arc(ex + lx, ey + ly, 3.6, 0, 2 * math.pi)
            c.set_source_rgba(*INK)
            c.fill()
            c.arc(ex + lx - 2.5, ey + ly - 2.5, 1.8, 0, 2 * math.pi)
            c.set_source_rgba(1, 1, 1, 1)
            c.fill()
            c.restore()
            _stroke(c, [(ex - ew - 2, ey + 1), (ex - ew * 0.3, ey - eh - 1), (ex + ew * 0.5, ey - eh * 0.9 - 1), (ex + ew + 2, ey)], 4)
            _stroke(c, [(ex - ew * 0.6, ey - eh - 7), (ex + ew * 0.6, ey - eh - 6)], 2, INK, 0.35)   # ชั้นตา
            _stroke(c, [(ex - ew * 0.5, ey + eh * 0.7 + 4), (ex + ew * 0.4, ey + eh * 0.8 + 3)], 2, INK, 0.3)   # ถุงใต้ตา
        # คิ้ว
        tilt = {"angry": -11, "shout": -12, "worry": 9, "sad": 8, "firm": -4, "smug": -3, "shock": 6}.get(mood, 0)
        by = ey - 24 - (8 if mood == "shock" else 0)
        bw = 22
        inner, outer = (ex - sx * bw * 0.1, by - tilt * 0.5), (ex + sx * bw, by + tilt * 0.5 - 2)
        mid = ((inner[0] + outer[0]) / 2, (inner[1] + outer[1]) / 2 - 5)
        _stroke(c, [(ex - sx * bw, by + 2 + tilt * (-0.6)), mid, outer], 6.5 * look.brow, look.hair_col if look.hair != "bald" else INK)

    # แว่น
    if look.glasses:
        th = 6 if look.glasses == "thick" else 3
        for sx in (-1, 1):
            ex = sx * w * 0.38 + fx
            _rr(c, ex - 24, ey - 17, 48, 32, 10)
            c.set_source_rgba(0.85, 0.92, 0.97, 0.18)
            c.fill_preserve()
            c.set_source_rgba(*INK)
            c.set_line_width(th)
            c.stroke()
        _stroke(c, [(-w * 0.38 + fx + 24, ey - 6), (fx, ey - 10), (w * 0.38 + fx - 24, ey - 6)], th * 0.8, smooth=False)

    # จมูก
    nl = look.nose
    nx = fx * 1.25
    side = 1 if turn >= 0 else -1
    _stroke(c, [(nx + side * 5, ey + 14 * nl), (nx + side * 9 * nl, ey + 28 * nl), (nx + side * 7 * nl, ey + 34 * nl)], 3, INK, 0.55)
    c.new_path()
    c.save()
    c.translate(nx + side * 1.5 * nl, ey + 38 * nl)
    c.scale(1, 0.8)
    c.arc(0, 0, 9 * nl, 0.15 * math.pi, 0.85 * math.pi)
    c.restore()
    c.set_source_rgba(*INK)
    c.set_line_width(3.5)
    c.stroke()
    for sx in (-1, 1):
        _stroke(c, [(nx + sx * 9 * nl, ey + 32 * nl), (nx + sx * 14 * nl, ey + 37 * nl), (nx + sx * 8 * nl, ey + 41 * nl)], 3, INK, 0.7)

    # ปาก
    my = ey + 38 * nl + 22
    mx = fx * 1.1
    mw = 25
    op = 0.0
    if talk:
        op = max(0.0, math.sin(t * 22 + seed)) * 0.6 + 0.2 * max(0.0, math.sin(t * 13.7 + seed))
    if mood == "shout":
        op = 0.9 + 0.1 * math.sin(t * 20)
    if mood == "shock":
        op = 0.8
    if op > 0.12:
        oh = 26 * op
        _smooth_path(c, [(mx - mw * 0.9, my), (mx, my - 4), (mx + mw * 0.9, my), (mx + mw * 0.5, my + oh), (mx - mw * 0.5, my + oh)])
        c.set_source_rgba(0.35, 0.12, 0.12, 1)
        c.fill_preserve()
        c.save()
        c.clip()
        c.rectangle(mx - mw, my - 6, mw * 2, 9)
        c.set_source_rgba(1, 1, 1, 1)
        c.fill()
        c.restore()
        _smooth_path(c, [(mx - mw * 0.9, my), (mx, my - 4), (mx + mw * 0.9, my), (mx + mw * 0.5, my + oh), (mx - mw * 0.5, my + oh)])
        c.set_source_rgba(*INK)
        c.set_line_width(3.5)
        c.stroke()
    else:
        curve = {"smile": 9, "smug": 5, "angry": -6, "worry": -5, "sad": -8, "firm": -1, "shock": 0}.get(mood, 1)
        if mood == "smug":
            _stroke(c, [(mx - mw * 0.8, my + 2), (mx, my + 3), (mx + mw, my - 6)], 4)
        else:
            _stroke(c, [(mx - mw, my - curve * 0.4), (mx, my + curve * 0.6), (mx + mw, my - curve * 0.4)], 4)
        _stroke(c, [(mx - 9, my + 13), (mx + 9, my + 13)], 2.5, INK, 0.35)   # ริมฝีปากล่าง

    # ผมด้านหน้า
    _hair_front(c, look, w, lw, fx)


def _hair_back(c, look, w, lw):
    if look.hair in ("nixon", "full", "part"):
        _smooth_path(c, [(-w * 1.06, 10), (-w * 1.1, -50), (-w * 0.7, -92), (0, -100), (w * 0.7, -92), (w * 1.1, -50), (w * 1.06, 10),
                         (w * 0.9, -10), (-w * 0.9, -10)])
        _shade(c, look.hair_col, lw, 0.3)


def _hair_front(c, look, w, lw, fx):
    h, col = look.hair, look.hair_col
    if h == "nixon":
        # หน้าผากเถิกสองข้าง จุกกลาง (widow's peak) หวีเสยไปด้านหลังเป็นลอน
        _smooth_path(c, [(-w * 1.04, 4), (-w * 1.04, -52), (-w * 0.7, -90), (0, -104), (w * 0.72, -90), (w * 1.06, -50), (w * 1.04, 4),
                         (w * 0.92, -18), (w * 0.86, -50), (w * 0.55, -60), (w * 0.22, -68), (fx * 0.3, -60), (-w * 0.22, -68),
                         (-w * 0.55, -60), (-w * 0.86, -50), (-w * 0.92, -18)])
        _shade(c, col, lw, 0.3)
        for k in (-0.5, -0.1, 0.3):
            _stroke(c, [(w * k, -70), (w * (k + 0.12), -88), (w * (k + 0.35), -96)], 2.5, WHITE, 0.25)
    elif h == "crew":
        _smooth_path(c, [(-w * 1.02, -18), (-w * 1.0, -66), (-w * 0.6, -94), (0, -98), (w * 0.6, -94), (w * 1.0, -66), (w * 1.02, -18),
                         (w * 0.9, -44), (w * 0.5, -66), (0, -70), (-w * 0.5, -66), (-w * 0.9, -44)])
        _shade(c, col, lw, 0.25)
        for i in range(12):
            x = -w * 0.8 + i * w * 0.145
            _stroke(c, [(x, -76 + abs(x) * 0.12), (x + 2, -88 + abs(x) * 0.08)], 2, INK, 0.25)
    elif h == "slick":
        # เถิกสูง เสยเรียบไปด้านหลัง
        _smooth_path(c, [(-w * 1.04, 0), (-w * 1.02, -58), (-w * 0.6, -94), (0, -100), (w * 0.6, -94), (w * 1.02, -58), (w * 1.04, 0),
                         (w * 0.94, -30), (w * 0.8, -66), (w * 0.4, -80), (0, -84), (-w * 0.4, -80), (-w * 0.8, -66), (-w * 0.94, -30)])
        _shade(c, col, lw, 0.25)
        for k in (-0.4, 0, 0.4):
            _stroke(c, [(w * k, -84), (w * k * 1.2, -96)], 2.2, WHITE, 0.3)
    elif h == "part":
        # แสกข้าง หวีปัด
        _smooth_path(c, [(-w * 1.05, 6), (-w * 1.06, -56), (-w * 0.6, -98), (w * 0.2, -104), (w * 0.8, -88), (w * 1.06, -54), (w * 1.04, 6),
                         (w * 0.94, -30), (w * 0.7, -52), (w * 0.1, -58), (-w * 0.5, -54), (-w * 0.9, -34)])
        _shade(c, col, lw, 0.3)
        _stroke(c, [(-w * 0.35, -98), (-w * 0.3, -70)], 2.5, WHITE, 0.4)
        _stroke(c, [(-w * 0.2, -66), (w * 0.4, -80), (w * 0.85, -70)], 2.5, WHITE, 0.25)
    elif h == "full":
        _smooth_path(c, [(-w * 1.08, 20), (-w * 1.08, -56), (-w * 0.6, -100), (0, -106), (w * 0.6, -100), (w * 1.08, -56), (w * 1.08, 20),
                         (w * 0.94, 0), (w * 0.9, -46), (w * 0.4, -60), (0, -56), (-w * 0.4, -62), (-w * 0.9, -46), (-w * 0.94, 0)])
        _shade(c, col, lw, 0.3)
        for k in (-0.6, -0.2, 0.2, 0.6):
            _stroke(c, [(w * k, -60), (w * k * 1.1, -84), (w * k * 0.9, -98)], 2.2, WHITE, 0.22)
    elif h == "short":
        _smooth_path(c, [(-w * 1.03, -10), (-w * 1.0, -62), (-w * 0.6, -96), (0, -100), (w * 0.6, -96), (w * 1.0, -62), (w * 1.03, -10),
                         (w * 0.9, -40), (w * 0.4, -64), (-w * 0.4, -64), (-w * 0.9, -40)])
        _shade(c, col, lw, 0.3)


# ---------------------------------------------------------------- ตัวเต็ม
def person(g, x, y, look, sc=1.0, mood="neutral", pose="down", pose2=None, k=0.0, talk=False,
           turn=0.0, look_at=(0, 0), seed=0, legs=True, lean=0.0, shadow=True):
    """คนเต็มตัว: pose -> pose2 ตามสัดส่วน k (ใช้ทำท่าขยับนุ่ม ๆ)"""
    c = g.c
    lw = 4.5
    p1 = POSES[pose]
    p2 = POSES[pose2] if pose2 else p1
    kk = k if pose2 else 0.0
    hands = p2[2:] if kk > 0.5 else p1[2:]
    ang = [tuple(lerp(a, b, kk) for a, b in zip(p1[i], p2[i])) for i in (0, 1)]
    breath = 1 + 0.006 * math.sin(g.t * 2.4 + seed)
    with g.at(x, y, sc * look.height):
        if shadow:
            c.save()
            c.scale(1, 0.14)
            rg = cairo.RadialGradient(0, 0, 0, 0, 0, 170)
            rg.add_color_stop_rgba(0, 0, 0, 0, 0.18)
            rg.add_color_stop_rgba(1, 0, 0, 0, 0.0)
            c.set_source(rg)
            c.arc(0, 0, 170, 0, 2 * math.pi)
            c.fill()
            c.restore()
        c.save()
        c.rotate(math.radians(lean))
        if legs:
            for sx in (-1, 1):
                _smooth_path(c, [(sx * 6, -440), (sx * 96, -440), (sx * 84, -200), (sx * 74, -40), (sx * 22, -40), (sx * 16, -220)])
                _shade(c, look.suit, lw, 0.3)
                c.save()
                c.translate(sx * 52, -22)
                c.scale(1.35, 0.6)
                c.new_path()
                c.arc(sx * 8, 0, 40, math.pi, 2 * math.pi)
                c.line_to(sx * 8 + 40, 10)
                c.line_to(sx * 8 - 40, 10)
                c.close_path()
                c.restore()
                _shade(c, hexc("#211d1a"), lw, 0.0)
                _stroke(c, [(sx * 32, -42), (sx * 70, -42)], 3, WHITE, 0.25)
        c.save()
        c.translate(0, -430)
        c.scale(1, breath)
        c.translate(0, 430)
        bw = look.build
        # แขนด้านหลัง (ข้างซ้ายจอ) วาดก่อนลำตัวถ้ายกขึ้นน้อย
        back_first = ang[0][0] < 60
        if back_first:
            _arm(c, look, -1, ang[0], hands[0], lw, g.t)
        # ลำตัว (เสื้อสูท)
        _smooth_path(c, [(-118 * bw, -722), (-60, -752), (60, -752), (118 * bw, -722), (128 * bw, -650), (114 * bw, -470),
                         (108 * bw, -414), (0, -406), (-108 * bw, -414), (-114 * bw, -470), (-128 * bw, -650)])
        _shade(c, look.suit, lw, 0.32)
        # เสื้อเชิ้ต + เนกไท
        c.new_path()
        c.move_to(-48, -752)
        c.line_to(48, -752)
        c.line_to(0, -560)
        c.close_path()
        _shade(c, look.shirt, lw, 0.1)
        if look.bowtie:
            for sx in (-1, 1):
                c.new_path()
                c.move_to(0, -738)
                c.line_to(sx * 34, -756)
                c.line_to(sx * 34, -718)
                c.close_path()
                _shade(c, look.tie, 3.5, 0.2)
            c.new_path()
            c.arc(0, -737, 8, 0, 2 * math.pi)
            _shade(c, look.tie, 3.5, 0.0)
        else:
            c.new_path()
            for p in [(-12, -746), (12, -746), (8, -728), (16, -610), (0, -588), (-16, -610), (-8, -728)]:
                c.line_to(*p)
            c.close_path()
            _shade(c, look.tie, 3.5, 0.25)
        # ปกเสื้อ
        for sx in (-1, 1):
            c.new_path()
            for p in [(sx * 50, -754), (sx * 6, -560), (sx * 42, -620), (sx * 76, -640), (sx * 62, -690), (sx * 82, -742)]:
                c.line_to(*p)
            c.close_path()
            _shade(c, look.suit, lw, 0.15 if sx < 0 else 0.4)
        _stroke(c, [(4, -500), (4, -440), (-6, -408)], 3, INK, 0.6)   # ชายเสื้อแยก
        for by in (-540, -470):
            c.new_path()
            c.arc(10, by, 6, 0, 2 * math.pi)
            _shade(c, INK, 0, 0)
        _stroke(c, [(70, -520), (112, -520)], 3, INK, 0.5)   # กระเป๋า
        if look.pin:
            _rr(c, -98, -664, 22, 14, 2)
            _shade(c, hexc("#c8553d"), 2, 0)
            _rr(c, -98, -664, 10, 7, 1)
            _shade(c, hexc("#3f6496"), 0, 0)
        if not back_first:
            _arm(c, look, -1, ang[0], hands[0], lw, g.t)
        with g.at(0, -842):
            head(g, look, mood, talk, turn, look_at, seed, lw)
        _arm(c, look, 1, ang[1], hands[1], lw, g.t)
        c.restore()
        c.restore()


def bust(g, x, y, look, sc=1.0, **kw):
    """ครึ่งตัว (ตัดที่เอว) — x,y = ระดับเอว"""
    person(g, x, y + 430 * sc * look.height, look, sc, legs=False, shadow=False, **kw)
