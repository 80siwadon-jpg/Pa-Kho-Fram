"""ตัวละครและพร็อพ: 28 ต.ค. 1962 ครุชชอฟประกาศทางวิทยุมอสโกว่าจะถอนขีปนาวุธจากคิวบา
ใช้ตัวละคร/พร็อพจากตอน cuba1962 และ arkhipov1962"""
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


cuba = _load("cuba1962")
ark = _load("arkhipov1962")
JFK, KHRUSHCHEV, ADVISORS, FAMILY = cuba.JFK, cuba.KHRUSHCHEV, cuba.ADVISORS, cuba.FAMILY
GENERALS = ark.GENERALS
caribbean_map, missile, time_bomb, red_phone = cuba.caribbean_map, cuba.missile, cuba.time_bomb, cuba.red_phone
clock_face, dove, warship, cargo_ship, sea, tv = cuba.clock_face, cuba.dove, cuba.warship, cuba.cargo_ship, cuba.sea, cuba.tv
globe, calendar = ark.globe, ark.calendar

SOV = hexc("#b8473a")
US = hexc("#3f6496")
WOOD = hexc("#8a5a3a")


def radio_set(g, x, y, sc=1.0, t=0.0, on=1.0):
    """วิทยุตู้ไม้ยุค 60 + คลื่นเสียงแผ่ออก"""
    c = g.c
    with g.at(x, y, sc):
        _smooth_path(c, [(-220, 0), (-220, -230), (-170, -300), (170, -300), (220, -230), (220, 0)])
        _shade(c, WOOD, 7, 0.3)
        _rr(c, -180, -250, 220, 200, 20)
        _shade(c, hexc("#e8dcc0"), 5, 0.05)
        for i in range(6):
            _stroke(c, [(-165, -225 + i * 32), (25, -225 + i * 32)], 4, hexc("#a8946a"), smooth=False)
        _rr(c, 70, -240, 120, 60, 8)
        _shade(c, hexc("#f2d68a"), 4, 0)
        _stroke(c, [(90 + 60 * (0.5 + 0.5 * math.sin(t)), -235), (90 + 60 * (0.5 + 0.5 * math.sin(t)), -186)], 4,
                RED, smooth=False)
        for i in range(2):
            g.circle(100 + i * 60, -110, 26, hexc("#3a2a1e"), 4)
        g.text("МОСКВА", -70, -30, 30, "kanit", INK)
    if on > 0:
        for i in range(3):
            u = (t * 1.2 + i / 3) % 1
            g.arc(x, y - 160 * sc, (240 + 260 * u) * sc, -60, 60, 8, (*SOV[:3], (1 - u) * on))
            g.arc(x, y - 160 * sc, (240 + 260 * u) * sc, 120, 240, 8, (*SOV[:3], (1 - u) * on))


def old_mic(g, x, y, sc=1.0):
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -8, -10, 16, 200, 4)
        _shade(c, GREY, 3, 0.2)
        _rr(c, -50, -130, 100, 130, 30)
        _shade(c, hexc("#c9ced6"), 5, 0.3)
        for k in range(4):
            _stroke(c, [(-40, -110 + k * 26), (40, -110 + k * 26)], 2.5, INK, 0.4, smooth=False)
        _rr(c, -60, 180, 120, 26, 8)
        _shade(c, hexc("#3a3f48"), 4, 0)


def defcon(g, x, y, sc=1.0, level=3, t=0.0):
    """มาตรวัดความพร้อมรบ DEFCON 5..1"""
    cols = [hexc("#3c8d4f"), hexc("#8ab84a"), hexc("#e3c13a"), hexc("#e3843a"), RED]
    with g.at(x, y, sc):
        g.rrect(-260, -230, 520, 460, 24, WHITE, 7)
        g.text("DEFCON", 0, -180, 50, "kanit", INK)
        for i in range(5):
            lv = 5 - i
            on = lv == level
            a = 0.5 + 0.5 * math.sin(t * 8) if on else 1
            g.rrect(-220 + i * 90, -110, 76, 260, 12, (*cols[i][:3], a if on else 0.25), 5)
            g.text(str(lv), -182 + i * 90, 20, 56, "kanit", INK if on else GREY)


def alarm_clock(g, x, y, sc=1.0, t=0.0, ring=1.0):
    c = g.c
    with g.at(x + ring * 4 * math.sin(t * 40), y, sc):
        for sx in (-1, 1):
            g.circle(sx * 60, -130, 34, GOLD, 5)
        c.new_path()
        c.arc(0, -40, 110, 0, 2 * math.pi)
        _shade(c, RED, 7, 0.25)
        g.circle(0, -40, 84, WHITE, 4)
        g.line([(0, -40), (0, -105)], 7, INK, amp=0)
        g.line([(0, -40), (40, -40)], 9, INK, amp=0)
        for sx in (-1, 1):
            g.line([(sx * 70, 50), (sx * 90, 90)], 10, INK, amp=0)


def missile_ship(g, x, y, sc=1.0, t=0.0, flip=True):
    """เรือขนส่งบรรทุกขีปนาวุธกลับบ้าน"""
    cargo_ship(g, x, y, sc, t, flip)
    with g.at(x, y - 60 * sc + 5 * math.sin(t * 1.6 + x), sc, 0, sx=-sc if flip else sc, sy=sc):
        with g.at(-20, -40, 0.8, 0):
            _smooth_path(g.c, [(-200, -14), (150, -14), (210, 0), (150, 14), (-200, 14)])
            _shade(g.c, hexc("#e9e2d4"), 4, 0.2)
        g.rrect(-240, -90, 380, 40, 6, (0.4, 0.45, 0.35, 0.8), 4)


def deal_table(g, x, y, sc=1.0, t=0.0, k=1.0):
    """ดีลลับใต้โต๊ะ: โต๊ะ + มือสองข้างส่งซองเอกสารลับใต้โต๊ะ"""
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -380, -40, 760, 50, 10)
        _shade(c, WOOD, 6, 0.25)
        for sx in (-1, 1):
            _rr(c, sx * 330 - 15, 10, 30, 260, 6)
            _shade(c, hexc("#6e4528"), 5, 0.2)
        # ใต้โต๊ะ: ซองลับเลื่อนจากซ้ายไปขวา
        ex = -120 + 240 * k
        with g.at(ex, 140, 1, -4):
            _rr(c, -90, -55, 180, 110, 6)
            _shade(c, hexc("#e8d6a8"), 5, 0.1)
            g.text("ลับ", 0, 0, 44, "kanit", RED)
        for sx, col in ((-1, US), (1, SOV)):
            hx = sx * 220 + (60 if sx < 0 else -60) * k
            _stroke(c, [(sx * 420, 120), (hx, 130)], 34, INK)
            _stroke(c, [(sx * 420, 120), (hx, 130)], 26, col)
            g.circle(hx, 130, 26, hexc("#f0c8a8"), 4)


def turkey_map(g, x, y, sc=1.0, t=0.0, k=0.0):
    """แผนที่ตุรกีอย่างย่อ + ขีปนาวุธจูปิเตอร์ (k = ถอนออก 0..1)"""
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -300, -220, 600, 440, 30)
        _shade(c, hexc("#bcd8ec"), 6, 0.05)
        c.save()
        _rr(c, -300, -220, 600, 440, 30)
        c.clip()
        _smooth_path(c, [(-260, -40), (-120, -110), (60, -100), (250, -120), (300, -40), (260, 80), (40, 90),
                         (-160, 80), (-270, 40)])
        _shade(c, hexc("#e9dfc8"), 5, 0.1)
        c.restore()
        g.text("ตุรกี", 0, 150, 50, "kanit", INK)
        for i in range(3):
            with g.at(-120 + i * 120, -20 - 300 * k * k, 1, 0):
                g.c.set_source_rgba(1, 1, 1, 1)
                _smooth_path(c, [(-14, 40), (-14, -60), (0, -90), (14, -60), (14, 40)])
                _shade(c, hexc("#e9e2d4") if k < 0.5 else (0.9, 0.9, 0.9, 1 - k), 4, 0.2)
        g.text("JUPITER", 0, -170, 40, "kanit", US)


def building(g, x, y, sc=1.0, kind="white"):
    """ทำเนียบขาว / เครมลิน (ทรงไอคอน)"""
    c = g.c
    with g.at(x, y, sc):
        if kind == "white":
            _rr(c, -200, -200, 400, 200, 4)
            _shade(c, WHITE, 6, 0.15)
            c.new_path()
            for p in [(-90, -200), (0, -270), (90, -200)]:
                c.line_to(*p)
            c.close_path()
            _shade(c, WHITE, 5, 0.1)
            for i in range(6):
                _rr(c, -160 + i * 60, -190, 18, 180, 4)
                _shade(c, hexc("#e9ecf0"), 3, 0)
        else:
            _rr(c, -180, -220, 360, 220, 4)
            _shade(c, hexc("#c8553d"), 6, 0.2)
            for sx in (-120, 0, 120):
                _rr(c, sx - 34, -340, 68, 130, 6)
                _shade(c, hexc("#d9a37e"), 5, 0.2)
                c.new_path()
                c.arc(sx, -350, 38, math.pi, 2 * math.pi)
                c.line_to(sx, -420)
                c.close_path()
                _shade(c, GOLD, 4, 0.2)
                g.star(sx, -432, 14, RED, 3)
            for i in range(4):
                _rr(c, -140 + i * 80, -150, 40, 70, 4)
                _shade(c, hexc("#f2d68a"), 3, 0)


def hotline(g, x0, x1, y, t=0.0, k=1.0):
    """สายด่วนเชื่อมสองฝั่ง + จุดสัญญาณวิ่ง"""
    xm = x0 + (x1 - x0) * k
    pts = []
    for i in range(21):
        xx = x0 + (xm - x0) * i / 20
        pts.append((xx, y + 30 * math.sin(i / 20 * math.pi)))
    if len(pts) > 1:
        g.line(pts, 10, RED, amp=0)
    if k >= 1:
        for j in range(2):
            u = (t * 0.7 + j * 0.5) % 1
            g.circle(x0 + (x1 - x0) * u, y + 30 * math.sin(u * math.pi), 14, GOLD2, 4)


def exhale(g, x, y, t, k=1.0):
    """ลมหายใจโล่งอก"""
    for i in range(3):
        u = (t * 0.9 + i / 3) % 1
        g.arc(x + 80 * u, y - 10 * i, 30 + 40 * u, -40, 40, 6, (0.5, 0.65, 0.85, (1 - u) * k))
