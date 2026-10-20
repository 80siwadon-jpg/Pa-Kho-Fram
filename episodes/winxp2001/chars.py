"""ตัวละครและพร็อพ: Windows XP วางจำหน่าย 25 ต.ค. 2001 — จอ CRT, ทุ่งหญ้าใต้ฟ้าคราม, Luna, จอฟ้า
ไม่ใช้โลโก้จริงของไมโครซอฟท์ (เขียนชื่อ "Windows XP" เป็นตัวหนังสือแทน)"""
import math

import cairo

from gfx import GOLD, GOLD2, GREY, INK, NAVY, RED, WHITE, hexc
from people import Look, _rr, _shade, _smooth_path, _stroke

BEIGE = hexc("#e6dfcc")
SKY = hexc("#3d86d8")
HILL = hexc("#5aa83a")
XP_BLUE = hexc("#2459c8")
XP_GREEN = hexc("#3d9a3a")
BSOD = hexc("#0a24a8")

USERS = [   # ผู้ใช้คอมพิวเตอร์ตามบ้านยุค 2001
    Look(hair="short", hair_col=hexc("#3a2a1e"), outfit="tee", suit=hexc("#d76b5a"), pants=hexc("#3a4a6a"), w=56,
         age=0.3, glasses="thin"),
    Look(hair="bun", hair_col=hexc("#5a3a22"), outfit="dress", suit=hexc("#6a8ab8"), w=54, age=0.35, height=0.93),
    Look(hair="buzz", hair_col=hexc("#221e1c"), outfit="hoodie", suit=hexc("#3c8d4f"), pants=hexc("#4a4a52"), w=56,
         height=0.62, headsc=1.4),
    Look(hair="part", hair_col=hexc("#6a5a4a"), suit=hexc("#3a3f48"), tie=hexc("#2b4f8a"), w=57, age=0.55),
]


def bliss(g, x0, y0, w, h, t=0.0):
    """วอลเปเปอร์ทุ่งหญ้าเขียวใต้ฟ้าคราม + เมฆ (วาดเอง)"""
    c = g.c
    c.save()
    c.rectangle(x0, y0, w, h)
    c.clip()
    lg = cairo.LinearGradient(0, y0, 0, y0 + h)
    lg.add_color_stop_rgb(0, 0.16, 0.43, 0.85)
    lg.add_color_stop_rgb(1, 0.62, 0.8, 0.96)
    c.set_source(lg)
    c.paint()
    for i in range(3):
        cx = x0 + w * ((0.2 + 0.33 * i + t * 0.01) % 1.1)
        cy = y0 + h * (0.18 + 0.08 * (i % 2))
        for k, (dx, r) in enumerate(((-0.08, 0.07), (0, 0.1), (0.09, 0.075))):
            c.new_path()
            c.arc(cx + dx * w, cy, r * w * 0.6, 0, 2 * math.pi)
            c.set_source_rgba(1, 1, 1, 0.9)
            c.fill()
    c.new_path()
    c.move_to(x0 - 10, y0 + h * 0.75)
    c.curve_to(x0 + w * 0.3, y0 + h * 0.48, x0 + w * 0.7, y0 + h * 0.5, x0 + w + 10, y0 + h * 0.7)
    c.line_to(x0 + w + 10, y0 + h + 10)
    c.line_to(x0 - 10, y0 + h + 10)
    c.close_path()
    lg = cairo.LinearGradient(0, y0 + h * 0.5, 0, y0 + h)
    lg.add_color_stop_rgb(0, 0.42, 0.75, 0.25)
    lg.add_color_stop_rgb(1, 0.2, 0.5, 0.12)
    c.set_source(lg)
    c.fill()
    c.restore()


def luna_desktop(g, x0, y0, w, h, t=0.0, win=1.0, start_glow=0.0):
    """เดสก์ท็อปสไตล์ Luna: taskbar น้ำเงิน + ปุ่ม start เขียว + หน้าต่างหัวน้ำเงิน"""
    c = g.c
    bliss(g, x0, y0, w, h, t)
    tb = h * 0.1
    c.save()
    c.rectangle(x0, y0, w, h)
    c.clip()
    lg = cairo.LinearGradient(0, y0 + h - tb, 0, y0 + h)
    lg.add_color_stop_rgb(0, 0.25, 0.45, 0.9)
    lg.add_color_stop_rgb(1, 0.1, 0.3, 0.75)
    c.rectangle(x0, y0 + h - tb, w, tb)
    c.set_source(lg)
    c.fill()
    sw = w * 0.26
    c.new_path()
    c.move_to(x0, y0 + h - tb)
    c.line_to(x0 + sw - tb * 0.4, y0 + h - tb)
    c.curve_to(x0 + sw, y0 + h - tb, x0 + sw, y0 + h, x0 + sw - tb * 0.4, y0 + h)
    c.line_to(x0, y0 + h)
    c.close_path()
    gg = 0.6 + 0.4 * start_glow
    c.set_source_rgb(0.24 * gg + 0.2 * start_glow, 0.62 * gg + 0.2 * start_glow, 0.23 * gg)
    c.fill()
    g.text("start", x0 + sw * 0.5, y0 + h - tb / 2, int(tb * 0.55), "kanit", WHITE)
    if win > 0.02:   # หน้าต่างโปรแกรม
        ww, wh = w * 0.55 * win, h * 0.5 * win
        wx, wy = x0 + w * 0.3, y0 + h * 0.15
        _rr(c, wx, wy, ww, wh, 10)
        c.set_source_rgb(0.96, 0.95, 0.9)
        c.fill()
        _rr(c, wx, wy, ww, wh * 0.16, 10)
        c.set_source_rgb(0.12, 0.35, 0.85)
        c.fill()
        c.new_path()
        c.rectangle(wx + ww - wh * 0.15, wy + wh * 0.02, wh * 0.12, wh * 0.12)
        c.set_source_rgb(0.85, 0.3, 0.2)
        c.fill()
        for k in range(3):
            c.rectangle(wx + ww * 0.08, wy + wh * (0.3 + 0.18 * k), ww * (0.7 - 0.15 * k), wh * 0.08)
            c.set_source_rgba(0.5, 0.5, 0.55, 0.6)
            c.fill()
    c.restore()


def bsod_screen(g, x0, y0, w, h):
    c = g.c
    c.save()
    c.rectangle(x0, y0, w, h)
    c.set_source_rgba(*BSOD)
    c.fill()
    for k in range(8):
        ww = w * (0.85 - 0.25 * ((k * 37) % 3) / 3)
        c.rectangle(x0 + w * 0.06, y0 + h * (0.12 + 0.1 * k), ww, h * 0.04)
        c.set_source_rgba(1, 1, 1, 0.85)
        c.fill()
    c.restore()


def pinball_screen(g, x0, y0, w, h, t=0.0):
    """โต๊ะพินบอลอวกาศ (วาดเอง)"""
    c = g.c
    c.save()
    c.rectangle(x0, y0, w, h)
    c.set_source_rgb(0.08, 0.06, 0.25)
    c.fill()
    for i in range(14):
        c.new_path()
        c.arc(x0 + w * ((i * 0.37) % 1), y0 + h * ((i * 0.61) % 1), 2.5, 0, 2 * math.pi)
        c.set_source_rgb(1, 1, 1)
        c.fill()
    for i, (u, v, col) in enumerate(((0.3, 0.3, (0.95, 0.3, 0.3)), (0.62, 0.25, (0.95, 0.8, 0.2)),
                                     (0.48, 0.48, (0.3, 0.8, 0.95)))):
        c.new_path()
        c.arc(x0 + w * u, y0 + h * v, w * 0.07 * (1 + 0.1 * math.sin(t * 8 + i)), 0, 2 * math.pi)
        c.set_source_rgb(*col)
        c.fill()
    fa = 0.3 * math.sin(t * 6)
    for sx in (-1, 1):
        c.save()
        c.translate(x0 + w * (0.5 + sx * 0.18), y0 + h * 0.85)
        c.rotate(sx * (0.35 + fa))
        c.rectangle(-sx * w * 0.16 if sx > 0 else 0, -8, w * 0.16, 16)
        c.set_source_rgb(0.9, 0.9, 0.95)
        c.fill()
        c.restore()
    bx = x0 + w * (0.5 + 0.3 * math.sin(t * 2.3))
    by = y0 + h * (0.55 + 0.25 * math.sin(t * 3.1))
    c.new_path()
    c.arc(bx, by, w * 0.03, 0, 2 * math.pi)
    c.set_source_rgb(0.85, 0.85, 0.9)
    c.fill()
    c.restore()


def crt(g, x, y, sc=1.0, screen="bliss", t=0.0, rot=0.0, win=1.0, start_glow=0.0, shake=0.0):
    """จอ CRT สีครีมยุค 2001 (x, y = กลางจอ)"""
    c = g.c
    with g.at(x + shake * 8 * math.sin(t * 40), y, sc, rot):
        _rr(c, -150, 250, 300, 50, 10)   # ฐานจอ
        _shade(c, BEIGE, 5, 0.25)
        _rr(c, -70, 200, 140, 60, 8)
        _shade(c, BEIGE, 5, 0.3)
        _rr(c, -330, -270, 660, 500, 36)
        _shade(c, BEIGE, 7, 0.25)
        sx0, sy0, sw, sh = -280, -225, 560, 400
        _rr(c, sx0 - 8, sy0 - 8, sw + 16, sh + 16, 18)
        _shade(c, hexc("#2b2b30"), 4, 0)
        if screen == "bliss":
            bliss(g, sx0, sy0, sw, sh, t)
        elif screen == "desktop":
            luna_desktop(g, sx0, sy0, sw, sh, t, win, start_glow)
        elif screen == "bsod":
            bsod_screen(g, sx0, sy0, sw, sh)
        elif screen == "pinball":
            pinball_screen(g, sx0, sy0, sw, sh, t)
        elif screen == "off":
            c.rectangle(sx0, sy0, sw, sh)
            c.set_source_rgb(0.15, 0.16, 0.18)
            c.fill()
        c.new_path()   # แสงสะท้อนจอแก้ว
        c.move_to(sx0 + 20, sy0 + 20)
        c.line_to(sx0 + 160, sy0 + 20)
        c.line_to(sx0 + 20, sy0 + 120)
        c.close_path()
        c.set_source_rgba(1, 1, 1, 0.18)
        c.fill()
        g.circle(260, 205, 9, XP_GREEN, 3)


def tower(g, x, y, sc=1.0):
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -110, -480, 220, 480, 14)
        _shade(c, BEIGE, 6, 0.3)
        for k in range(2):
            _rr(c, -80, -440 + k * 60, 160, 40, 6)
            _shade(c, hexc("#d6ceb8"), 4, 0.1)
        g.circle(0, -200, 22, hexc("#d6ceb8"), 4)
        g.circle(0, -200, 8, XP_GREEN, 0)


def keyboard(g, x, y, sc=1.0, t=0.0, typing=0.0):
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -300, -40, 600, 80, 14)
        _shade(c, BEIGE, 5, 0.2)
        for r in range(3):
            for k in range(12):
                down = typing > 0 and (int(t * 12) + k * 7 + r * 3) % 9 == 0
                _rr(c, -270 + k * 45, -28 + r * 22 + (3 if down else 0), 36, 16, 3)
                _shade(c, hexc("#f4f0e4"), 2, 0)


def hourglass(g, x, y, sc=1.0, t=0.0):
    c = g.c
    with g.at(x, y, sc, 180 * ((t * 0.6) % 1 > 0.85)):
        c.new_path()
        for p in [(-40, -60), (40, -60), (0, 0), (40, 60), (-40, 60), (0, 0)]:
            c.line_to(*p)
        c.close_path()
        _shade(c, WHITE, 5, 0.1)
        c.new_path()
        for p in [(-22, 40), (22, 40), (36, 56), (-36, 56)]:
            c.line_to(*p)
        c.close_path()
        _shade(c, GOLD, 0, 0)


def note(g, x, y, sc=1.0, col=INK, rot=0.0):
    """โน้ตดนตรี (วาดเอง — Kanit ไม่มีสัญลักษณ์ ♪)"""
    c = g.c
    with g.at(x, y, sc, rot):
        c.save()
        c.translate(0, 0)
        c.scale(1.3, 1)
        c.new_path()
        c.arc(0, 0, 18, 0, 2 * math.pi)
        c.restore()
        c.set_source_rgba(*col)
        c.fill()
        _stroke(c, [(20, -4), (20, -90)], 7, col, smooth=False)
        _stroke(c, [(20, -90), (50, -70), (48, -50)], 7, col)


def box(g, x, y, sc=1.0, rot=0.0, title="Vista", col=hexc("#2b2b30"), accent=hexc("#4ab0e0")):
    """กล่องซอฟต์แวร์"""
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -130, -180, 260, 360, 12)
        _shade(c, col, 6, 0.3)
        c.new_path()
        c.arc(0, -30, 70, 0, 2 * math.pi)
        _shade(c, accent, 4, 0.3)
        g.text(title, 0, 120, 46, "kanit", WHITE)


def xp_box(g, x, y, sc=1.0, rot=0.0):
    """กล่อง Windows XP: ทุ่งหญ้าฟ้าคราม + ชื่อ"""
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -130, -180, 260, 360, 12)
        _shade(c, WHITE, 6, 0.1)
        bliss(g, -120, -170, 240, 230)
        g.text("Windows XP", 0, 110, 40, "kanit", XP_BLUE)


def timeline_bar(g, x0, x1, y, k=1.0, t=0.0):
    """แถบเวลา 2001 → 2014"""
    c = g.c
    _rr(c, x0, y - 22, x1 - x0, 44, 22)
    _shade(c, hexc("#e8e8ec"), 5, 0)
    xe = x0 + (x1 - x0) * k
    if k > 0.02:
        _rr(c, x0, y - 22, xe - x0, 44, 22)
        _shade(c, XP_GREEN, 5, 0.2)
    for yr, u in ((2001, 0.0), (2007, 0.46), (2009, 0.62), (2014, 1.0)):
        xx = x0 + (x1 - x0) * u
        g.line([(xx, y + 30), (xx, y + 60)], 5, INK, amp=0)
        g.label(str(yr), xx, y + 100, 44)


def calendar_mourn(g, x, y, sc=1.0):
    """ปฏิทิน 11 ก.ย. พร้อมริบบิ้นดำ (ไม่แสดงภาพเหตุการณ์)"""
    c = g.c
    with g.at(x, y, sc):
        g.rrect(-150, -170, 300, 340, 22, WHITE, 8)
        g.rrect(-150, -170, 300, 80, 22, hexc("#3a3a40"), 8)
        g.text("ก.ย. 2001", 0, -130, 40, "kanit", WHITE)
        g.text("9/11", 0, 0, 100, "kanit", INK)
        _smooth_path(c, [(90, 70), (130, 110), (120, 160), (100, 130), (80, 160), (60, 110)])
        _shade(c, hexc("#1b1916"), 4, 0)


def quake_lines(g, x, y, r, t, k=1.0):
    for i in range(3):
        u = (t * 1.8 + i / 3) % 1
        for sx in (-1, 1):
            g.arc(x, y, r + 120 * u, 90 - 40 + (0 if sx > 0 else 180), 90 + 40 + (0 if sx > 0 else 180), 8,
                  (0.85, 0.3, 0.2, k * (1 - u)))
