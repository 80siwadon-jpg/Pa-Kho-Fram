"""ตัวละคร/พร็อพ/ฉากหลังของตอน room404 (การ์ตูนโทนมืด เขียวหม่น + เหลืองซีด แนวนอน 1920x1080)"""
import math
import os
import sys

import cairo

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))
from gfx import INK, WHITE, H, W, hexc, hn, lerp, seg, e_io, e_out  # noqa: E402
from people import Look, _rr, _shade, _smooth_path, _stroke, head, person  # noqa: E402

# ---------------------------------------------------------------- palette
BG = hexc("#0b1619")
NIGHT = hexc("#0f2227")
TEAL = hexc("#2a5a5c")
TEAL2 = hexc("#3d7f7a")
TEAL3 = hexc("#6fb3a6")
NEON = hexc("#a6f0cf")
YEL = hexc("#d8c45c")
YEL2 = hexc("#f1e6a0")
TILE = hexc("#4f7f71")
TILE2 = hexc("#3f685d")
CONC = hexc("#3f4a4c")
CONC2 = hexc("#56625f")
FLOOR = hexc("#2b3534")
WOOD = hexc("#6a4a30")
WOOD2 = hexc("#4b3322")
TEAK = hexc("#7a5332")
RUST = hexc("#9a5126")
TALIS = hexc("#a82a2a")
TALIS2 = hexc("#7a1f20")
GOWN = hexc("#e7ece6")
GHOST_SKIN = hexc("#c4cecb")
BLACKHAIR = hexc("#0c0d10")
GOLDC = hexc("#e2b33b")
BLOOD = hexc("#6e1d1d")
PALE_BLUE = hexc("#9db7c9")

# ---------------------------------------------------------------- looks
EK = Look(hair="crew", hair_col=hexc("#17140f"), skin=hexc("#d9a77f"), outfit="tee", suit=hexc("#2c3e5c"),
          pants=hexc("#3a3f45"), shoes=hexc("#222222"), stubble=0.55, jaw=0.5, age=0.25, w=58, print_txt="")
LANDLORD = Look(hair="slick", hair_col=hexc("#b9b6ae"), skin=hexc("#e2b28c"), outfit="flannel", suit=hexc("#3b2a3a"),
                pants=hexc("#2a2a2c"), jowls=0.75, jaw=0.85, w=68, build=1.35, age=0.8, brow=1.2, nose=1.2)
SRI = Look(hair="bun", hair_col=hexc("#a9a7a2"), skin=hexc("#d7a885"), outfit="dress", suit=hexc("#6b5a78"),
           age=0.95, w=54, build=0.85, height=0.9, jaw=0.2)
DAO = Look(hair="long", hair_col=BLACKHAIR, skin=hexc("#dcb59a"), outfit="tee", suit=PALE_BLUE, pants=hexc("#55606a"),
           w=52, build=0.72, jaw=0.1, age=0.1, height=0.95)
GHOST = Look(hair="long", hair_col=BLACKHAIR, skin=GHOST_SKIN, outfit="gown", suit=GOWN, w=52, build=0.8, jaw=0.1,
             age=0.1, height=1.0)


def flick(t, seed=1, rate=1.0):
    """ความสว่างนีออนกะพริบ 0.25..1 (กะพริบเป็นจังหวะไม่สม่ำเสมอ)"""
    u = t * rate + seed * 3.7
    v = 1.0
    if (u % 4.3) < 0.18 or (u % 7.1) < 0.09:
        v = 0.3 + 0.2 * (hn(int(t * 30), seed) * 0.5 + 0.5)
    return v


# ---------------------------------------------------------------- atmosphere
def fill_rect(c, x, y, w, h, col):
    c.rectangle(x, y, w, h)
    c.set_source_rgba(*col)
    c.fill()


def glow(g, x, y, r, col, a=0.5):
    c = g.c
    rg = cairo.RadialGradient(x, y, 0, x, y, r)
    rg.add_color_stop_rgba(0, col[0], col[1], col[2], a)
    rg.add_color_stop_rgba(1, col[0], col[1], col[2], 0)
    c.set_source(rg)
    c.arc(x, y, r, 0, 2 * math.pi)
    c.fill()


def vignette(g, k=0.75, cx=W / 2, cy=H / 2, r0=0.35, r1=0.85):
    c = g.c
    rg = cairo.RadialGradient(cx, cy, W * r0, cx, cy, W * r1)
    rg.add_color_stop_rgba(0, 0, 0, 0, 0)
    rg.add_color_stop_rgba(1, 0.01, 0.03, 0.04, k)
    c.set_source(rg)
    c.rectangle(-1500, -1500, W + 3000, H + 3000)
    c.fill()


def darken(g, a):
    """ความมืดทั้งจอ (ไฟดับ)"""
    if a <= 0:
        return
    fill_rect(g.c, -1500, -1500, W + 3000, H + 3000, (0.01, 0.02, 0.025, a))


def rain(g, t, a=0.5, n=110, seed=3, area=(-300, -100, W + 600, H + 200), speed=1500, ang=0.22, ln=60):
    c = g.c
    x0, y0, aw, ah = area
    c.set_line_width(2.4)
    c.set_line_cap(cairo.LINE_CAP_ROUND)
    for i in range(n):
        u = (hn(i, seed) * 0.5 + 0.5)
        v = (hn(i, seed + 1) * 0.5 + 0.5)
        sp = speed * (0.75 + 0.5 * v)
        y = y0 + ((u * ah + t * sp) % ah)
        x = x0 + v * aw - (y - y0) * ang
        c.set_source_rgba(0.75, 0.9, 0.88, a * (0.4 + 0.6 * u))
        c.move_to(x, y)
        c.line_to(x - ln * ang, y + ln)
        c.stroke()


def beam(g, x, y, ang, length=900, spread=18, a=0.35, col=YEL2):
    """ลำแสงไฟฉาย (กรวยแสง) จากจุด x,y ทิศ ang องศา"""
    c = g.c
    a0, a1 = math.radians(ang - spread), math.radians(ang + spread)
    p1 = (x + math.cos(a0) * length, y + math.sin(a0) * length)
    p2 = (x + math.cos(a1) * length, y + math.sin(a1) * length)
    lg = cairo.LinearGradient(x, y, x + math.cos(math.radians(ang)) * length, y + math.sin(math.radians(ang)) * length)
    lg.add_color_stop_rgba(0, col[0], col[1], col[2], a)
    lg.add_color_stop_rgba(1, col[0], col[1], col[2], 0)
    c.move_to(x, y)
    c.line_to(*p1)
    c.line_to(*p2)
    c.close_path()
    c.set_source(lg)
    c.fill()


def smoke(g, x, y, t, n=5, a=0.25, seed=2, rise=140):
    for i in range(n):
        u = ((t * 0.35 + i / n) % 1.0)
        px = x + 40 * math.sin(t * 1.3 + i * 1.7) * u + hn(i, seed) * 20
        py = y - u * rise * 3
        g.blob(px, py, 30 + 70 * u, 20 + 40 * u, (0.8, 0.85, 0.82, a * (1 - u)), 0, seed + i)


def lightning(t, times):
    """ความสว่างแสงฟ้าแลบ 0..1 ที่เวลา t (times = รายการเวลาแลบ)"""
    v = 0.0
    for t0 in times:
        d = t - t0
        if 0 <= d < 0.5:
            v = max(v, (1 - d / 0.5) ** 2 * (0.6 + 0.4 * (d < 0.06 or 0.12 < d < 0.18)))
    return v


# ---------------------------------------------------------------- building pieces
def tiles(g, x, y, w, h, col=TILE, col2=TILE2, size=46):
    c = g.c
    fill_rect(c, x, y, w, h, col)
    c.set_source_rgba(*col2)
    c.set_line_width(2)
    xx = x
    while xx <= x + w:
        c.move_to(xx, y)
        c.line_to(xx, y + h)
        xx += size
    yy = y
    while yy <= y + h:
        c.move_to(x, yy)
        c.line_to(x + w, yy)
        yy += size
    c.stroke()


def stains(g, x, y, w, h, n=6, seed=4, a=0.25):
    for i in range(n):
        px = x + (hn(i, seed) * 0.5 + 0.5) * w
        py = y + (hn(i, seed + 1) * 0.5 + 0.5) * h * 0.4
        g.blob(px, py + 40, 30 + 30 * abs(hn(i, seed + 2)), 60 + 80 * abs(hn(i, seed + 3)), (0.12, 0.16, 0.12, a), 0, i)


def neon_tube(g, x, y, w, t, seed=1, on=None):
    b = flick(t, seed) if on is None else on
    _rr(g.c, x - w / 2, y - 9, w, 18, 9)
    _shade(g.c, lerp_col(hexc("#55605c"), NEON, b), 4, 0.1)
    if b > 0.5:
        glow(g, x, y, w * 0.9, NEON, 0.22 * b)
    return b


def lerp_col(a, b, k):
    return tuple(lerp(x, y, k) for x, y in zip(a, b))


def door(g, x, y, w=300, h=560, num="404", open_k=0.0, lock=True, talisman=True, peep=True, col=WOOD, t=0.0, lock_k=0.0):
    """ประตูไม้ ศูนย์กลางล่าง = x,y (พื้น)"""
    c = g.c
    _rr(c, x - w / 2 - 22, y - h - 22, w + 44, h + 22, 4)
    _shade(c, CONC2, 5, 0.2)
    fill_rect(c, x - w / 2, y - h, w, h, (0.02, 0.03, 0.03, 1))
    if open_k > 0:   # ข้างในมืด
        glow(g, x, y - h * 0.5, w * 0.7, YEL, 0.08 * open_k)
    ww = w * (1 - 0.82 * open_k)
    _rr(c, x - w / 2, y - h, ww, h, 3)
    _shade(c, col, 5, 0.25, horiz=False)
    if open_k < 0.3:
        for i in range(2):
            _rr(c, x - w / 2 + 34, y - h + 40 + i * (h / 2 - 10), w - 68, h / 2 - 70, 6)
            _shade(c, None if False else lerp_col(col, (0, 0, 0, 1), 0.15), 3, 0.1)
        if num:
            _rr(c, x - 60, y - h + 70, 120, 56, 6)
            _shade(c, hexc("#c9b98a"), 3, 0.15)
            g.text(num, x, y - h + 98, 40, "kanit", INK)
        if peep:
            g.circle(x, y - h + 190, 13, hexc("#b0a070"), 3)
            g.circle(x, y - h + 190, 6, (0, 0, 0, 1), 0)
        g.circle(x + w / 2 - 36, y - h * 0.48, 15, hexc("#b39a5b"), 4)
        if talisman:
            with g.at(x - 10, y - h * 0.52, 1, -8):
                _rr(c, -26, -110, 52, 220, 3)
                _shade(c, hexc("#c9a35a"), 3, 0.12)
                for k in range(6):
                    _stroke(c, [(-14, -90 + k * 34), (0, -78 + k * 34), (14, -90 + k * 34)], 3, TALIS, 0.9)
        if lock:
            lx, ly = x + w / 2 - 36, y - h * 0.48 + 70
            fill_rect(c, lx - 30, ly - 10, 60, 18, RUST)
            sw = -lock_k * 70
            with g.at(lx, ly + 20, 1, sw):
                c.new_path()
                c.arc(0, -8, 20, math.pi, 0)
                c.set_source_rgba(*hexc("#7d6a55"))
                c.set_line_width(9)
                c.stroke()
                _rr(c, -28, -8, 56, 52, 8)
                _shade(c, RUST, 4, 0.3)
                g.circle(0, 14, 6, (0, 0, 0, 1), 0)


def corridor(g, t, vx=960, vy=470, light=1.0, end_door=True, lock=True, open_k=0.0, wet=True, side_doors=True, seed=1):
    """ทางเดินแบบมุมมองจุดเดียว: ปลายทางคือประตู 404"""
    c = g.c
    b = flick(t, seed) * light
    fill_rect(c, -1500, -1500, W + 3000, H + 3000, lerp_col(NIGHT, TILE2, 0.35 * b))
    # พื้น/เพดาน/ผนัง (สี่เหลี่ยมคางหมู)
    ex0, ex1, ey0, ey1 = vx - 230, vx + 230, vy - 330, vy + 330
    wall = lerp_col(hexc("#1c2c2a"), TILE, 0.75 * b)
    for pts, col in (
        ([(-1500, -1500), (W + 1500, -1500), (ex1, ey0), (ex0, ey0)], lerp_col(hexc("#121a1a"), CONC, 0.7 * b)),
        ([(-1500, H + 1500), (W + 1500, H + 1500), (ex1, ey1), (ex0, ey1)], lerp_col(hexc("#0f1514"), FLOOR, b)),
        ([(-1500, -1500), (ex0, ey0), (ex0, ey1), (-1500, H + 1500)], wall),
        ([(W + 1500, -1500), (ex1, ey0), (ex1, ey1), (W + 1500, H + 1500)], wall),
    ):
        g.poly(pts, col, 4, amp=0)
    # เส้นกระเบื้องตามแนวลึก
    c.set_source_rgba(0.1, 0.18, 0.16, 0.6)
    c.set_line_width(2)
    for k in range(1, 9):
        yy = lerp(ey0, ey1, k / 9)
        for xe, xo in ((ex0, -1500), (ex1, W + 1500)):
            c.move_to(xe, yy)
            c.line_to(xo, vy + (yy - vy) * (abs(xo - vx) / abs(xe - vx)))
    c.stroke()
    # ขอบประตูข้าง ๆ
    if side_doors:
        for d in (0.18, 0.42, 0.7):
            for sx in (-1, 1):
                xe = vx + sx * 230
                xa = lerp(xe, vx + sx * 2200, d)
                xb = lerp(xe, vx + sx * 2200, d + 0.09)
                fa = (xa - vx) / (xe - vx)
                fb = (xb - vx) / (xe - vx)
                g.poly([(xa, vy - 140 * fa), (xb, vy - 140 * fb), (xb, vy + 330 * fb), (xa, vy + 330 * fa)],
                       lerp_col(WOOD2, WOOD, 0.6 * b), 3, amp=0)
    # ปลายทาง
    fill_rect(c, ex0, ey0, ex1 - ex0, ey1 - ey0, lerp_col(hexc("#13201e"), TILE, 0.55 * b))
    if end_door:
        with g.at(vx, ey1, 0.85):
            door(g, 0, 0, 300, 560, open_k=open_k, lock=lock, t=t)
    # นีออนบนเพดาน
    for k, d in enumerate((0.25, 0.6)):
        yy = lerp(ey0, -400, d)
        f = (vy - yy) / (vy - ey0)
        bb = neon_tube(g, vx, yy, 120 * f, t, seed + k, on=b if k == 0 else max(0.4, b))
    if wet:   # แสงสะท้อนพื้นเปียก
        glow(g, vx, ey1 + 240, 300, NEON, 0.08 * b)
    return b


def window_rain(g, x, y, w, h, t, a=0.6):
    c = g.c
    _rr(c, x - 12, y - 12, w + 24, h + 24, 4)
    _shade(c, CONC2, 4, 0.2)
    fill_rect(c, x, y, w, h, hexc("#0d1d22"))
    c.save()
    c.rectangle(x, y, w, h)
    c.clip()
    rain(g, t, a, 40, 9, (x - 100, y - 50, w + 200, h + 100), 900, 0.1, 40)
    c.restore()
    c.set_source_rgba(*INK)
    c.set_line_width(5)
    c.move_to(x + w / 2, y)
    c.line_to(x + w / 2, y + h)
    c.move_to(x, y + h / 2)
    c.line_to(x + w, y + h / 2)
    c.stroke()


def building(g, t, x=960, base=1000, floors=5, cols=5, lit=None, sign=True, w404_glow=0.0, ghost=None):
    """ตึกอพาร์ตเมนต์เก่าด้านหน้า: ระเบียงลูกกรงสนิม ป้ายนีออน"""
    c = g.c
    fw, fh = 230, 170
    bw = cols * fw + 80
    x0 = x - bw / 2
    top = base - floors * fh - 60
    _rr(c, x0, top, bw, base - top + 400, 6)
    _shade(c, hexc("#33403f"), 6, 0.3)
    stains(g, x0, top, bw, 400, 10, 5, 0.35)
    lit = lit or {}
    for f in range(floors):
        for k in range(cols):
            wx = x0 + 40 + k * fw + 20
            wy = base - (f + 1) * fh + 10
            key = (f + 1, k)
            on = lit.get(key, 0.15 + 0.15 * (hn(f, k, 3) > 0.3))
            col = lerp_col(hexc("#0c1414"), YEL, on)
            fill_rect(c, wx, wy, fw - 40, fh - 70, col)
            if on > 0.4:
                glow(g, wx + (fw - 40) / 2, wy + 50, 140, YEL, 0.15 * on)
            # ระเบียง
            c.set_source_rgba(*hexc("#5b4033"))
            c.set_line_width(4)
            for j in range(9):
                xx = wx - 6 + j * (fw - 28) / 8
                c.move_to(xx, wy + fh - 110)
                c.line_to(xx, wy + fh - 60)
            c.move_to(wx - 10, wy + fh - 110)
            c.line_to(wx + fw - 30, wy + fh - 110)
            c.stroke()
            fill_rect(c, wx - 14, wy + fh - 62, fw - 12, 10, CONC2)
    if sign:
        b = flick(t, 7)
        with g.at(x0 + 40, top + 130, 1, -2):
            _rr(c, -10, -40, 330, 80, 10)
            _shade(c, hexc("#14201f"), 4, 0.1)
            g.text("ห้องพักรายเดือน", 155, 0, 44, "kanit", lerp_col(hexc("#2c4a42"), NEON, b))
            if b > 0.6:
                glow(g, 155, 0, 260, NEON, 0.18)
    return x0, fw, fh, base


def balcony_xy(x0, fw, fh, base, floor, col):
    return x0 + 40 + col * fw + 20 + (fw - 40) / 2, base - (floor + 1) * fh + 10 + fh - 110


# ---------------------------------------------------------------- characters
def ghost_back(g, x, y, sc, t, brush=1.0, a=1.0, seed=3):
    """ผู้หญิงชุดขาวหันหลัง ผมดำยาวถึงเอว กำลังแปรงผมช้า ๆ (x,y = ปลายเท้า)"""
    c = g.c
    with g.alpha(a):
        with g.at(x, y, sc):
            _smooth_path(c, [(-70, -720), (-40, -760), (40, -760), (70, -720), (110, -300), (150, -10), (0, 0), (-150, -10), (-110, -300)])
            _shade(c, GOWN, 4.5, 0.3, horiz=False)
            # หัว (ด้านหลัง)
            g.blob(0, -830, 58, 66, BLACKHAIR, 4.5, seed)
            sway = 6 * math.sin(t * 0.8)
            _smooth_path(c, [(-62, -840), (62, -840), (78 + sway, -600), (66 + sway, -430), (0, -400 + sway), (-66 + sway, -430), (-78 + sway, -600)])
            _shade(c, BLACKHAIR, 4.5, 0.1)
            for k in range(5):
                _stroke(c, [(-40 + k * 20, -800), (-44 + k * 22 + sway, -600), (-42 + k * 21 + sway, -440)], 2.5, (0.25, 0.3, 0.32, 1), 0.5)
            # แขนแปรงผม: ยกขึ้นลงช้า ๆ
            ph = (math.sin(t * 1.4) * 0.5 + 0.5) * brush
            hx, hy = 70, lerp(-820, -560, ph)
            _stroke(c, [(78, -700), (120, -720 + 60 * ph), (hx + 6, hy)], 26, GOWN, 1.0)
            _stroke(c, [(78, -700), (120, -720 + 60 * ph), (hx + 6, hy)], 4.5, INK, 1.0)
            g.circle(hx + 8, hy, 16, GHOST_SKIN, 4)
            with g.at(hx, hy - 6, 1, -70):
                _rr(c, -10, -60, 20, 70, 6)
                _shade(c, hexc("#6d4d35"), 3.5, 0.2)


def ghost_face(g, x, y, sc, t, grin=1.0, eyes=1.0, a=1.0, seed=5):
    """ใบหน้าซีด ตาเบิกโพลง ยิ้มฉีกกว้าง (การ์ตูน ไม่มีเลือด)"""
    c = g.c
    with g.alpha(a):
        with g.at(x, y, sc):
            _smooth_path(c, [(-160, -210), (0, -250), (160, -210), (200, 60), (170, 330), (-170, 330), (-200, 60)])
            _shade(c, BLACKHAIR, 5, 0.05)
            g.blob(0, 0, 135, 170, GHOST_SKIN, 5, seed)
            _smooth_path(c, [(-140, -100), (-60, -190), (60, -190), (140, -100), (110, -150), (0, -175), (-110, -150)])
            _shade(c, BLACKHAIR, 0, 0.0)
            # ตาวงดำรอบตา
            for sx in (-1, 1):
                g.blob(sx * 52, -20, 44, 36, (0.45, 0.5, 0.52, 0.7), 0, seed + sx)
                g.blob(sx * 52, -20, 30 * eyes + 6, 28 * eyes + 6, WHITE, 4)
                g.circle(sx * 52 + 2 * math.sin(t), -20, 8, INK, 0)
                for k in range(3):
                    _stroke(c, [(sx * (30 + k * 10), -30 + k * 8), (sx * (40 + k * 10), -24 + k * 8)], 1.8, (0.7, 0.2, 0.2, 1), 0.6)
            # ยิ้มฉีก
            gw = 50 + 70 * grin
            _smooth_path(c, [(-gw, 70 - 20 * grin), (0, 95 + 25 * grin), (gw, 70 - 20 * grin), (0, 108 + 40 * grin)])
            _shade(c, (0.1, 0.06, 0.07, 1), 4, 0.0)
            for k in range(-4, 5):
                xx = k * gw / 5.5
                yy = 75 + 22 * grin * (1 - (k / 5) ** 2)
                fill_rect(c, xx - 6, yy, 11, 12 * grin, (0.92, 0.92, 0.86, 1))
            # ผมเปียกห้อยหน้า
            for k, xx in enumerate((-120, -95, 100, 125)):
                _stroke(c, [(xx, -150), (xx + 6, 20), (xx - 4, 200)], 10, BLACKHAIR, 1.0)


def shadow_crawler(g, x, y, sc, t, k=1.0, a=1.0):
    """เงาดำทมิฬคลานหัวลงมาตามผนัง แขนขายาวผิดรูป (x,y = หัว)"""
    c = g.c
    with g.alpha(a):
        with g.at(x, y, sc):
            ph = math.sin(t * 2.2)
            col = (0.015, 0.02, 0.025, 1)
            # ลำตัวยาวขึ้นไปด้านบน (หัวลง)
            _smooth_path(c, [(-60, -40), (60, -40), (80, -420), (40, -700), (-40, -700), (-80, -420)])
            _shade(c, col, 0, 0.0)
            for sx in (-1, 1):   # แขนยาว + ขา (ข้อต่อหักมุม)
                j = ph * sx * 30
                _stroke(c, [(sx * 50, -120), (sx * (230 + j), -260), (sx * (300 + j), 60 + j)], 30, col, 1.0)
                _stroke(c, [(sx * 40, -620), (sx * (260 - j), -560), (sx * (320 - j), -820)], 32, col, 1.0)
                for f in range(4):
                    _stroke(c, [(sx * (300 + j), 60 + j), (sx * (300 + j + (f - 1.5) * 18), 110 + j)], 7, col, 1.0)
            g.blob(0, 0, 70, 82, col, 0, 9)
            for i in range(9):   # ผมห้อยลง
                xx = -60 + i * 15
                _stroke(c, [(xx, 40), (xx + 6 * math.sin(t + i), 200 + 40 * k), (xx - 4, 330 * k + 60)], 8, col, 1.0)
            for sx in (-1, 1):   # ตาเรือง ๆ จาง ๆ
                g.circle(sx * 26, -6, 7, (0.75, 0.85, 0.8, 0.55 * k), 0)


def gold_chain(g, x, y, w=70):
    c = g.c
    c.new_path()
    c.arc(x, y - 30, w, math.radians(25), math.radians(155))
    c.set_source_rgba(*GOLDC)
    c.set_line_width(8)
    c.stroke()


def apron(g, x, y, sc):
    with g.at(x, y, sc * SRI.height):
        _rr(g.c, -80, -620, 160, 380, 18)
        _shade(g.c, hexc("#c9c3b1"), 4, 0.2)


def flashlight(g, x, y, ang, on=True, length=900, a=0.4, sc=1.0):
    if on:
        beam(g, x, y, ang, length, 17, a)
    with g.at(x, y, sc, ang):
        _rr(g.c, -70, -14, 70, 28, 8)
        _shade(g.c, hexc("#303438"), 4, 0.2)
        if on:
            glow(g, 0, 0, 40, YEL2, 0.7)


def sledgehammer(g, x, y, sc=1.0, rot=0):
    with g.at(x, y, sc, rot):
        _rr(g.c, -9, -460, 18, 470, 6)
        _shade(g.c, hexc("#8a6a44"), 4, 0.2)
        _rr(g.c, -70, -520, 140, 76, 8)
        _shade(g.c, hexc("#4b5052"), 5, 0.35)


def wardrobe(g, x, y, w=420, h=760, open_k=0.0, shake=0.0, talis=True, inside=None, t=0.0):
    """ตู้เสื้อผ้าไม้สัก (x,y = กลางล่าง); inside(g) วาดของในตู้ (พิกัดเดียวกัน)"""
    c = g.c
    x += shake * math.sin(t * 60)
    _rr(c, x - w / 2 - 14, y - h - 30, w + 28, h + 30, 6)
    _shade(c, WOOD2, 5, 0.3, horiz=False)
    fill_rect(c, x - w / 2, y - h, w, h, (0.02, 0.025, 0.03, 1))
    if inside and open_k > 0.05:
        c.save()
        c.rectangle(x - w / 2, y - h, w, h)
        c.clip()
        inside(g)
        c.restore()
    for sx in (-1, 1):   # บานคู่ เปิดออกด้านข้าง (หดความกว้าง)
        dw = (w / 2) * (1 - 0.88 * open_k)
        xx = x if sx > 0 else x - dw
        if sx > 0:
            xx = x + (w / 2 - dw) * 0 + (w / 2) * open_k * 0.9 + 0 if False else x + w / 2 * open_k * 0.88 * 0
        x_left = x - w / 2 if sx < 0 else x + w / 2 - dw
        _rr(c, x_left, y - h, dw, h, 3)
        _shade(c, TEAK, 4, 0.28, horiz=False)
        if open_k < 0.5:
            _rr(c, x_left + 22, y - h + 30, dw - 44, h * 0.42, 6)
            _shade(c, lerp_col(TEAK, (0, 0, 0, 1), 0.15), 3, 0.1)
            _rr(c, x_left + 22, y - h + 60 + h * 0.42, dw - 44, h * 0.42, 6)
            _shade(c, lerp_col(TEAK, (0, 0, 0, 1), 0.15), 3, 0.1)
            g.circle(x - sx * 18 + (0 if sx < 0 else 0), y - h * 0.5, 9, hexc("#b39a5b"), 3) if True else None
    if talis:
        for k, (xx, yy, r) in enumerate(((x - w / 2 - 4, y - h + 60, -12), (x + w / 2 + 4, y - h + 90, 10), (x - w / 2 + 6, y - h * 0.45, 6))):
            yantra_cloth(g, xx, yy, 0.45, r, seed=k)


def yantra_cloth(g, x, y, sc=1.0, rot=0, seed=1, torn=True):
    c = g.c
    with g.at(x, y, sc, rot):
        pts = [(-120, -80), (120, -86), (126, 60), (90, 70), (70, 96), (40, 74), (-20, 92), (-60, 70), (-118, 84)]
        g.poly(pts, TALIS2, 4, seed=seed, amp=0)
        c.set_source_rgba(0.06, 0.04, 0.03, 0.9)
        c.set_line_width(4)
        c.rectangle(-80, -50, 160, 100)
        c.stroke()
        c.move_to(-80, -50)
        c.line_to(80, 50)
        c.move_to(80, -50)
        c.line_to(-80, 50)
        c.stroke()
        c.arc(0, 0, 30, 0, 2 * math.pi)
        c.stroke()
        for k in range(5):
            _stroke(c, [(-100 + k * 48, -66), (-90 + k * 48, -72), (-80 + k * 48, -64)], 3, (0.06, 0.04, 0.03, 1), 0.9)


def bound_dao(g, x, y, sc, t, bang=0.0, tape=1.0, look_up=0.0):
    """ดาวนั่งกอดเข่าในตู้ มือเท้าถูกมัด (x,y = ก้น) หันหน้าไปทางขวา"""
    c = g.c
    rope = hexc("#3e78b8")
    with g.at(x, y, sc):
        # ลำตัวเอนพิงผนังตู้
        _smooth_path(c, [(-90, -380), (40, -400), (80, -30), (-100, -20)])
        _shade(c, DAO.suit, 4.5, 0.3)
        # เข่าชันอยู่หน้าลำตัว
        _smooth_path(c, [(-20, -40), (60, -250), (150, -270), (190, -230), (170, -20)])
        _shade(c, DAO.pants, 4.5, 0.3)
        for sx in (0, 40):
            _rr(c, 150 + sx * 0.3, -40, 70, 34, 14)
            _shade(c, hexc("#2a2a2a"), 4, 0.2)
        fill_rect(c, 150, -110, 70, 18, rope)   # เชือกข้อเท้า
        # แขนกอดเข่า ข้อมือมัด
        _stroke(c, [(-20, -340), (60, -250), (150, -200)], 34, DAO.suit, 1.0)
        _stroke(c, [(-20, -340), (60, -250), (150, -200)], 4.5, INK, 1.0)
        g.circle(160, -196, 20, DAO.skin, 4)
        fill_rect(c, 136, -214, 22, 36, rope)
        tilt = -16 * bang + 10 * look_up
        with g.at(-10, -470, 1, tilt):
            head(g, DAO, "worry" if look_up < 0.5 else "shock", 0.0, 0.35, (0.6, -0.4 * look_up), 7)
            if tape > 0:
                _rr(c, -28, 24, 84, 30 * tape, 4)
                _shade(c, hexc("#aeb3a8"), 3, 0.1)
            g.blob(14, -56, 14, 8, (0.55, 0.22, 0.22, 0.85), 0, 2)   # รอยช้ำที่หน้าผาก (ไม่มีเลือด)


def ek_head_light(g, x, y, sc):
    glow(g, x, y, 260 * sc, YEL2, 0.18)
