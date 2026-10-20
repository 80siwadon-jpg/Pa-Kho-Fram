"""มาสคอตพิธีกรช่อง "วันนี้ในอดีต" (ตามชีตออกแบบที่เจ้าของช่องส่งมา)
หนุ่มผมหยิกสีน้ำตาลเข้ม ตาโตเป็นประกาย เสื้อเบลเซอร์กรมท่าพับแขน เสื้อกั๊กเขียวมะกอก เชิ้ตขาว
กระเป๋าสะพายหนัง นาฬิกาพก กางเกงน้ำตาลพับขา รองเท้าบูท

    host(g, x, y, sc, expr="smile", pose="idle", t=t, prop=None, talk=False)
    expr: smile / excited / curious / surprised / thoughtful / worry
    pose: idle / point (ชี้ขึ้นแบบเปิดคลิป) / wave / think (มือแตะคาง) / hold (ถือของหน้าอก) / hips (เท้าเอว) / present (กางมือ)
    prop (เฉพาะ pose="hold"): ("book",) / ("calendar", "26", "ต.ค.") / ("glass",)
x, y = ปลายเท้า, ความสูงทั้งตัว ≈ 1040 × sc"""
import math

from gfx import GOLD, INK, WHITE, hexc
from people import _rr, _shade, _smooth_path, _stroke

NAVY = hexc("#2f3f5f")
OLIVE = hexc("#6b7247")
LEATHER = hexc("#7a4e2e")
SKIN = hexc("#f6d2b4")
HAIR = hexc("#4a2d1c")
PANTS = hexc("#8c7356")
SHIRT = hexc("#f7f1e3")
BOOT = hexc("#5a3a24")
IRIS = hexc("#5a3a22")
BRASS = hexc("#d4a23a")

# มุมแขน (องศาจากแนวดิ่งลง, + = กางออกนอกตัว) ต้นแขน, ปลายแขน — ข้างซ้ายจอ, ข้างขวาจอ
POSES = {
    "idle":    ((38, -42), (8, 4)),
    "point":   ((8, 4), (150, 178)),
    "wave":    ((8, 4), (115, 168)),
    "think":   ((8, 4), (-25, 175)),
    "hold":    ((40, -93), (40, -93)),
    "hips":    ((38, -42), (38, -42)),
    "present": ((8, 4), (70, 95)),
}
L1, L2 = 150, 145
SHOULDER_Y = -720


def _arm_pts(sx, a1, a2):
    r1, r2 = math.radians(a1), math.radians(a2)
    s = (sx * 92, SHOULDER_Y + 12)
    e = (s[0] + sx * L1 * math.sin(r1), s[1] + L1 * math.cos(r1))
    h = (e[0] + sx * L2 * math.sin(r2), e[1] + L2 * math.cos(r2))
    return s, e, h


def _arm(g, sx, a1, a2, hand="open", t=0.0):
    c = g.c
    s, e, h = _arm_pts(sx, a1, a2)
    _stroke(c, [s, e], 58, INK, smooth=False)
    _stroke(c, [s, e], 48, NAVY, smooth=False)
    cuff = (e[0] + (h[0] - e[0]) * 0.32, e[1] + (h[1] - e[1]) * 0.32)
    _stroke(c, [e, cuff], 52, INK, smooth=False)
    _stroke(c, [e, cuff], 42, NAVY, smooth=False)
    c.new_path()
    c.arc(e[0], e[1], 22, 0, 2 * math.pi)
    c.set_source_rgba(*NAVY)
    c.fill()
    cuff2 = (e[0] + (h[0] - e[0]) * 0.46, e[1] + (h[1] - e[1]) * 0.46)
    _stroke(c, [cuff, cuff2], 46, INK, smooth=False)
    _stroke(c, [cuff, cuff2], 38, SHIRT, smooth=False)   # แขนเสื้อเชิ้ตพับ
    _stroke(c, [cuff2, h], 34, INK, smooth=False)
    _stroke(c, [cuff2, h], 26, SKIN, smooth=False)
    _hand(g, h, sx, hand, math.atan2(h[1] - e[1], h[0] - e[0]), t)
    return h


def _hand(g, h, sx, kind, ang, t):
    c = g.c
    x, y = h
    if kind == "chin":   # นิ้วชี้แตะคาง
        _stroke(c, [(x, y - 4), (x - 10 * sx, y - 44)], 20, INK)
        _stroke(c, [(x, y - 4), (x - 10 * sx, y - 44)], 12, SKIN)
    if kind == "point":   # กำมือ ชูนิ้วชี้ขึ้น
        _stroke(c, [(x, y - 4), (x + 2 * sx, y - 62)], 20, INK)
        _stroke(c, [(x, y - 4), (x + 2 * sx, y - 62)], 12, SKIN)
    c.new_path()
    c.arc(x, y, 24, 0, 2 * math.pi)
    _shade(c, SKIN, 4.5, 0.15)
    if kind == "palm":
        for k in range(4):
            a = ang - 0.9 + k * 0.6
            _stroke(c, [(x + 18 * math.cos(a), y + 18 * math.sin(a)), (x + 40 * math.cos(a), y + 40 * math.sin(a))],
                    14, INK)
            _stroke(c, [(x + 18 * math.cos(a), y + 18 * math.sin(a)), (x + 40 * math.cos(a), y + 40 * math.sin(a))],
                    8, SKIN)


def _legs(g, t, walk=0.0):
    c = g.c
    for sx in (-1, 1):
        sw = 10 * math.sin(t * 8 + (0 if sx < 0 else math.pi)) * walk + sx * 14
        _smooth_path(c, [(sx * 8, -480), (sx * 80, -480), (sx * 74 + sw, -260), (sx * 70 + sw, -110),
                         (sx * 16 + sw, -110), (sx * 12 + sw * 0.5, -300)])
        _shade(c, PANTS, 5, 0.3 if sx < 0 else 0.45)
        _rr(c, sx * 43 - 30 + sw, -150, 60, 42, 10)   # ขากางเกงพับ
        _shade(c, hexc("#a08a6c"), 4.5, 0.15)
        _smooth_path(c, [(sx * 18 + sw, -112), (sx * 70 + sw, -112), (sx * 76 + sw, -40), (sx * 108 + sw, -26),
                         (sx * 110 + sw, 0), (sx * 12 + sw, 0), (sx * 14 + sw, -60)])
        _shade(c, BOOT, 5, 0.25)
        _stroke(c, [(sx * 30 + sw, -92), (sx * 60 + sw, -86)], 3, hexc("#c9a46a"), smooth=False)
        _stroke(c, [(sx * 30 + sw, -74), (sx * 62 + sw, -68)], 3, hexc("#c9a46a"), smooth=False)


def _torso(g, t):
    c = g.c
    # เชิ้ตขาว
    _smooth_path(c, [(-80, -720), (80, -720), (86, -470), (-86, -470)])
    _shade(c, SHIRT, 5, 0.15)
    # เสื้อกั๊กเขียวมะกอก คอวี
    _smooth_path(c, [(-80, -705), (-20, -640), (0, -600), (20, -640), (80, -705), (90, -470), (40, -455), (0, -470),
                     (-40, -455), (-90, -470)])
    _shade(c, OLIVE, 5, 0.3)
    for k in range(3):
        c.new_path()
        c.arc(-8, -580 + k * 38, 5, 0, 2 * math.pi)
        c.set_source_rgba(*BRASS)
        c.fill()
    # สายนาฬิกาพก + นาฬิกา
    pts = [(-6, -545), (14, -528), (38, -524), (52, -536)]
    _stroke(c, pts, 4, BRASS)
    c.new_path()
    c.arc(58, -530, 13, 0, 2 * math.pi)
    _shade(c, BRASS, 3.5, 0.2)
    # เข็มขัด
    _rr(c, -88, -488, 176, 24, 4)
    _shade(c, LEATHER, 4, 0.1)
    _rr(c, -14, -490, 28, 28, 4)
    _shade(c, BRASS, 3, 0)
    # เบลเซอร์กรมท่า (เปิดหน้า) + ปกเสื้อ
    for sx in (-1, 1):
        _smooth_path(c, [(sx * 40, -730), (sx * 112, -716), (sx * 118, -600), (sx * 112, -430), (sx * 74, -420),
                         (sx * 62, -560), (sx * 48, -650)])
        _shade(c, NAVY, 5, 0.25 if sx < 0 else 0.42)
        _smooth_path(c, [(sx * 34, -732), (sx * 62, -728), (sx * 74, -660), (sx * 52, -600), (sx * 46, -660)])
        _shade(c, hexc("#3b4d72"), 4, 0.1)
    # คอเสื้อเชิ้ต
    for sx in (-1, 1):
        c.new_path()
        for p in [(0, -712), (sx * 40, -742), (sx * 46, -704)]:
            c.line_to(*p)
        c.close_path()
        _shade(c, SHIRT, 4, 0.1)
    # สายกระเป๋าเฉียงจากไหล่ซ้ายจอ -> สะโพกขวาจอ
    _stroke(c, [(-74, -726), (10, -610), (112, -470)], 30, INK, smooth=False)
    _stroke(c, [(-74, -726), (10, -610), (112, -470)], 22, LEATHER, smooth=False)


def satchel(g, x, y, sc=1.0, rot=0.0):
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -70, -60, 140, 110, 18)
        _shade(c, LEATHER, 5, 0.3)
        _smooth_path(c, [(-72, -62), (72, -62), (66, 10), (-66, 10)])
        _shade(c, hexc("#8e5c38"), 4.5, 0.2)
        _rr(c, -10, -10, 20, 26, 4)
        _shade(c, BRASS, 3, 0)


def book(g, x, y, sc=1.0, rot=0.0):
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -90, -120, 180, 240, 10)
        _shade(c, hexc("#6e4528"), 6, 0.3)
        _rr(c, -76, -106, 152, 212, 6)
        c.set_source_rgba(0.85, 0.65, 0.3, 0.35)
        c.set_line_width(4)
        c.stroke()
        c.new_path()
        c.arc(0, 0, 42, 0, 2 * math.pi)
        c.set_source_rgba(*BRASS)
        c.set_line_width(5)
        c.stroke()
        for k in range(8):
            a = k * math.pi / 4
            _stroke(c, [(10 * math.cos(a), 10 * math.sin(a)), (40 * math.cos(a), 40 * math.sin(a))], 3, BRASS,
                    smooth=False)


def magnifier(g, x, y, sc=1.0, rot=0.0):
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -12, 60, 24, 130, 10)
        _shade(c, hexc("#6e4528"), 5, 0.2)
        c.new_path()
        c.arc(0, 0, 66, 0, 2 * math.pi)
        _shade(c, BRASS, 6, 0.2)
        c.new_path()
        c.arc(0, 0, 52, 0, 2 * math.pi)
        c.set_source_rgba(0.85, 0.94, 1, 1)
        c.fill()
        _stroke(c, [(-30, -20), (-14, -36)], 6, WHITE)


def _blobs(c, circles, col, lw=5):
    for x, y, r in circles:
        c.new_path()
        c.arc(x, y, r + lw, 0, 2 * math.pi)
        c.set_source_rgba(*INK[:3], 1)
        c.fill()
    for x, y, r in circles:
        c.new_path()
        c.arc(x, y, r, 0, 2 * math.pi)
        c.set_source_rgba(*col)
        c.fill()


def _head(g, expr, t, talk, look, seed):
    c = g.c
    hy = -880
    # ผมด้านหลัง: ลอนหยิกฟูเป็นก้อน ๆ (ขอบดำก่อน แล้วเติมสี = ขอบรวมเป็นก้อนเดียว)
    back = [(0, -940, 100)]
    for k in range(9):
        a = math.radians(180 + k * 22.5)
        back.append((112 * math.cos(a), -925 + 100 * math.sin(a), 26 + 6 * (k % 2)))
    _blobs(c, back, HAIR)
    # หู
    for sx in (-1, 1):
        c.new_path()
        c.arc(sx * 100, hy + 10, 19, 0, 2 * math.pi)
        _shade(c, SKIN, 4.5, 0.2)
    # คอ
    _rr(c, -26, -800, 52, 90, 10)
    _shade(c, hexc("#e9bf9c"), 4.5, 0.1)
    # หน้า
    _smooth_path(c, [(-100, -900), (-97, -845), (-80, -800), (-42, -770), (0, -762), (42, -770), (80, -800), (97, -845),
                     (100, -900), (82, -960), (0, -985), (-82, -960)])
    _shade(c, SKIN, 5, 0.15)
    # แก้มแดง
    for sx in (-1, 1):
        c.save()
        c.translate(sx * 62, hy + 40)
        c.scale(1.4, 0.8)
        c.new_path()
        c.arc(0, 0, 13, 0, 2 * math.pi)
        c.restore()
        c.set_source_rgba(1, 0.55, 0.5, 0.35)
        c.fill()
    # ตาโต
    lx, ly = look
    blink = ((t * 0.45 + seed * 0.31) % 3.3) < 0.1 and expr not in ("surprised",)
    happy = expr == "excited"
    for sx in (-1, 1):
        ex, ey = sx * 40, hy - 2
        if happy or blink:
            c.new_path()
            c.arc(ex, ey + 8, 22, math.pi * 1.1, math.pi * 1.9)
            c.set_source_rgba(*INK[:3], 1)
            c.set_line_width(7)
            c.set_line_cap(1)
            c.stroke()
            continue
        ry = 33 if expr == "surprised" else 30
        c.save()
        c.translate(ex, ey)
        c.scale(1, ry / 24)
        c.new_path()
        c.arc(0, 0, 24, 0, 2 * math.pi)
        c.restore()
        c.set_source_rgb(1, 1, 1)
        c.fill_preserve()
        c.set_source_rgba(*INK[:3], 1)
        c.set_line_width(4)
        c.stroke()
        ix, iy = ex + lx * 6, ey + 4 + ly * 6
        c.save()
        c.translate(ix, iy)
        c.scale(1, 1.18)
        c.new_path()
        c.arc(0, 0, 17 if expr != "surprised" else 13, 0, 2 * math.pi)
        c.restore()
        c.set_source_rgba(*IRIS)
        c.fill()
        c.new_path()
        c.arc(ix, iy + 2, 8, 0, 2 * math.pi)
        c.set_source_rgba(*INK[:3], 1)
        c.fill()
        for (dx, dy, r) in ((-6, -9, 6), (6, 7, 3)):   # ประกายตา
            c.new_path()
            c.arc(ix + dx, iy + dy, r, 0, 2 * math.pi)
            c.set_source_rgb(1, 1, 1)
            c.fill()
        c.new_path()   # ขนตาบน
        c.arc(ex, ey + 2, 27, math.pi * 1.12, math.pi * 1.88)
        c.set_source_rgba(*INK[:3], 1)
        c.set_line_width(7)
        c.stroke()
    # คิ้ว
    tilt = {"curious": (8, -6), "surprised": (-8, -8), "thoughtful": (4, 2), "worry": (10, 10)}.get(expr, (0, 0))
    for sx in (-1, 1):
        dy = tilt[0] if sx < 0 else tilt[1]
        _stroke(c, [(sx * 62, hy - 48 + dy), (sx * 40, hy - 56 + dy * 0.5), (sx * 18, hy - 50)], 7, HAIR)
    # จมูก
    _stroke(c, [(4, hy + 22), (8, hy + 36), (0, hy + 40)], 3.5, hexc("#c98a6a"))
    # ปาก
    my = hy + 70
    op = (0.5 + 0.5 * math.sin(t * 16)) if talk else 0.0
    if expr == "excited" or (talk and op > 0.35):
        h = 30 if expr == "excited" else 14 + 18 * op
        c.new_path()
        c.move_to(-34, my - 6)
        c.curve_to(-30, my + h, 30, my + h, 34, my - 6)
        c.close_path()
        c.set_source_rgba(0.45, 0.15, 0.15, 1)
        c.fill_preserve()
        c.set_source_rgba(*INK[:3], 1)
        c.set_line_width(4.5)
        c.stroke()
        c.new_path()
        c.arc(0, my + h * 0.55, 12, math.pi, 2 * math.pi)
        c.set_source_rgba(0.95, 0.5, 0.5, 1)
        c.fill()
    elif expr == "surprised":
        c.save()
        c.translate(0, my + 4)
        c.scale(0.8, 1)
        c.new_path()
        c.arc(0, 0, 13, 0, 2 * math.pi)
        c.restore()
        c.set_source_rgba(0.45, 0.15, 0.15, 1)
        c.fill_preserve()
        c.set_source_rgba(*INK[:3], 1)
        c.set_line_width(4)
        c.stroke()
    elif expr in ("thoughtful", "curious"):
        _stroke(c, [(-18, my + 4), (6, my + 6), (24, my - 4)], 5, INK)
    elif expr == "worry":
        _stroke(c, [(-20, my + 8), (0, my), (20, my + 8)], 5, INK)
    else:
        _stroke(c, [(-26, my - 4), (0, my + 12), (26, my - 4)], 5, INK)
    # ผมหน้าม้าหยิกเป็นลอน (เห็นหน้าผากและคิ้ว)
    front = [(0, -1010, 78), (-80, -982, 22), (-44, -994, 24), (-4, -988, 22), (36, -998, 24), (74, -984, 22),
             (102, -950, 16), (-104, -948, 16), (-56, -1036, 30), (12, -1050, 32), (68, -1030, 28)]
    _blobs(c, front, HAIR)
    for (x0, y0, r, a0) in ((-60, -1030, 22, 3.6), (10, -1045, 24, 3.4), (70, -1025, 20, 3.8), (-46, -975, 16, 3.3),
                            (32, -978, 16, 3.5)):
        c.new_path()
        c.arc(x0, y0, r, a0, a0 + 2.2)
        c.set_source_rgba(1, 1, 1, 0.25)
        c.set_line_width(4)
        c.stroke()
    _stroke(c, [(0, -1076), (12, -1104), (34, -1108), (40, -1088), (24, -1082)], 9, INK)   # ปอยผมชี้
    _stroke(c, [(0, -1076), (12, -1104), (34, -1108), (40, -1088), (24, -1082)], 4, HAIR)


def host(g, x, y, sc=1.0, expr="smile", pose="idle", t=0.0, prop=None, talk=False, look=(0, 0), seed=0,
         walk=0.0, flip=False, shadow=True):
    c = g.c
    (a_l1, a_l2), (a_r1, a_r2) = POSES.get(pose, POSES["idle"])
    bob = 6 * math.sin(t * 2.4 + seed) + (-10 * abs(math.sin(t * 8)) * walk)
    with g.at(x, y, sc, 0, sx=-sc if flip else sc, sy=sc):
        if shadow:
            c.save()
            c.scale(1, 0.16)
            c.new_path()
            c.arc(0, 0, 150, 0, 2 * math.pi)
            c.restore()
            c.set_source_rgba(0, 0, 0, 0.12)
            c.fill()
        _legs(g, t, walk)
        with g.at(0, bob * 0.3):
            satchel(g, 128, -440, 0.9, 6 + 3 * math.sin(t * 2.4 + seed))
            _torso(g, t)
            hands = {"point": "point", "wave": "palm", "present": "palm", "think": "chin"}
            if pose == "hold":
                _arm(g, -1, a_l1, a_l2, "open", t)
                _arm(g, 1, a_r1, a_r2, "open", t)
                if prop:
                    kind = prop[0]
                    if kind == "book":
                        book(g, 0, -600, 0.75, -6)
                    elif kind == "calendar":
                        g.calendar(0, -600, 0.6, prop[1] if len(prop) > 1 else "1", "",
                                   prop[2] if len(prop) > 2 else "")
                    elif kind == "glass":
                        magnifier(g, 0, -660, 0.75, -15)
                for sx, (a1, a2) in ((-1, (a_l1, a_l2)), (1, (a_r1, a_r2))):   # มือทับของที่ถือ
                    _, _, h = _arm_pts(sx, a1, a2)
                    _hand(g, h, sx, "open", 0, t)
            else:
                _arm(g, -1, a_l1, a_l2, "open", t)
                _arm(g, 1, a_r1, a_r2 + 4 * math.sin(t * 6) * (pose == "wave"), hands.get(pose, "open"), t)
            with g.at(0, bob * 0.7, 1, 2 * math.sin(t * 1.7 + seed)):
                _head(g, expr, t, talk, look, seed)
        if pose in ("think",) and expr == "curious":
            g.label("?", 150, -1060, 90, color=hexc("#7a4a9a"))


def host_head(g, x, y, sc=1.0, expr="smile", t=0.0, talk=False, look=(0, 0), seed=0):
    """หัวพิธีกรอย่างเดียว (มุมจอ/ภาพใกล้) — x, y = กลางหน้า"""
    with g.at(x, y + 880 * sc, sc):
        _head(g, expr, t, talk, look, seed)
