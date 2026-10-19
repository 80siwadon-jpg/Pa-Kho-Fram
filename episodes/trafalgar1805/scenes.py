"""ฉากตอน: ยุทธนาวีทราฟัลการ์ (21 ต.ค. 1805) — ตัวละครแบบกึ่งเสมือนจริง (src/people.py)"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from chars import (HARDY, NAPOLEON, NELSON, SAILORS, cannonball, europe_map, lantern, sea, ship, ship_icon,  # noqa: E402
                   signal_flags, smoke)
from gfx import (GOLD, GOLD2, GREY, INK, LGREY, NAVY, RED, W, WHITE, e_in, e_io, e_out, hexc, hn, lerp,  # noqa: E402
                 pop, seg, text_sprite)
from people import _rr, _shade, person  # noqa: E402

CX = W / 2
GROUND = 1270
SEA_Y = 980
GREEN = hexc("#3c8d4f")
GOLDTXT = hexc("#b37a12")
WOOD = hexc("#b98a5a")
WOOD2 = hexc("#8a5a36")

CAMERA = {"hook": "push_in", "odds": "pan_right", "plan": "tilt_up", "charge": "push_in", "shot": "dutch",
          "death": "push_in", "legacy": "tilt_up", "lesson": "pull_out", "outro": "pull_out"}
TRANSITIONS = {"charge": "whip", "shot": "zoom", "death": "fade", "legacy": "iris"}


def show(t, a, b=None, fade=0.25):
    k = seg(t, a - fade, a)
    if b is not None:
        k = min(k, 1 - seg(t, b - fade, b))
    return k


def deck(g, t, y=GROUND - 40, rail=True, mast=True):
    """ดาดฟ้าเรือไม้ + ราวกันตก + เสากระโดง"""
    c = g.c
    if mast:
        _rr(c, 820, -400, 60, y + 400, 10)
        _shade(c, WOOD2, 6, 0.3)
        g.line([(850, 120), (1300, 420)], 5, amp=0)
        g.line([(850, 220), (-300, 520)], 5, amp=0)
    if rail:
        _rr(c, -400, y - 230, W + 800, 28, 6)
        _shade(c, WOOD2, 5, 0.3)
        for xx in range(-380, W + 400, 110):
            _rr(c, xx, y - 210, 22, 210, 6)
            _shade(c, WOOD2, 4, 0.3)
    _rr(c, -400, y, W + 800, 1400 - y - 80, 0)
    _shade(c, WOOD, 6, 0.0)
    for j in range(5):
        g.line([(-400, y + 22 + j * 22), (W + 400, y + 22 + j * 22)], 3, (0.4, 0.25, 0.12, 0.5), amp=0)


def wall_of_ships(g, t, n, side_cols, y, x0=90, x1=990, k=1.0, s=0.55, rot=0.0):
    for i in range(int(n * k)):
        x = lerp(x0, x1, i / max(n - 1, 1))
        ship_icon(g, x, y + 4 * math.sin(t * 2 + i), s, side_cols[i % len(side_cols)], rot)


def tactical_bg(g, y0=300, y1=1240):
    """แผงทะเลสำหรับแผนผังยุทธวิธี (มองจากด้านบน)"""
    _rr(g.c, 50, y0, 980, y1 - y0, 30)
    _shade(g.c, hexc("#dcebf6"), 6, 0.0)
    for i in range(10):
        x, y = 120 + (i * 197) % 860, y0 + 60 + (i * 131) % (y1 - y0 - 120)
        g.line([(x - 20, y), (x, y - 8), (x + 20, y)], 3, (1, 1, 1, 1), amp=0)


def counter(g, x, y, value, label, col, size=96, k=1.0):
    if k <= 0:
        return
    g.label(f"{value}", x, y, size, color=col, sc=k)
    g.label(label, x, y + size * 0.85, 44, sc=k)


def flash(g, x, y, r, a=1.0):
    with g.alpha(a):
        g.sparkle(x, y, r, (1, 0.85, 0.4, 1), 0)
        g.circle(x, y, r * 0.45, (1, 0.95, 0.7, 1), 0)


def book(g, x, y, sc, tear=0.0):
    with g.at(x, y, sc):
        for sx in (-1, 1):
            with g.at(sx * 30 * tear, 0, 1, sx * 25 * tear):
                c = g.c
                _rr(c, -150 if sx < 0 else 0, -110, 150, 220, 6)
                _shade(c, hexc("#7a2e2e"), 6, 0.2)
        if tear < 0.2:
            g.label("ตำราพิชัยสงคราม", 0, 0, 34, color=GOLD2)


def nelson_column(g, x, y, sc=1.0):
    """เสาเนลสัน จัตุรัสทราฟัลการ์ ลอนดอน"""
    with g.at(x, y, sc):
        g.rrect(-120, -120, 240, 120, 6, LGREY, 6)
        g.rrect(-50, -760, 100, 650, 8, hexc("#e9e2d4"), 6)
        for k in range(4):
            g.line([(-40 + k * 26, -740), (-40 + k * 26, -130)], 3, GREY, amp=0)
        g.rrect(-70, -790, 140, 40, 8, GOLD, 5)
    person(g, x, y - 790 * sc, NELSON, 0.22 * sc, mood="firm", seed=1, shadow=False)


# ------------------------------------------------------------------ 1. hook
def s_hook(g, t, L, d):
    if t < L[1] - 0.2:
        sea(g, SEA_Y, t)
        for i, x in enumerate((200, 520, 860)):
            ship(g, x, SEA_Y + 60, 0.3, "uk" if i == 1 else "fr", t, flip=i > 1)
        g.label("วันนี้ในอดีต", CX, 470, 104, sc=lerp(2.0, 1, e_out(seg(t, 0.1, 0.4))) if t > 0.1 else 0, rot=-4)
        g.label("21 ตุลาคม 1805", CX, 610, 84, color=RED, sc=pop(t, 0.8))
        return
    if t < L[2] - 0.2:
        europe_map(g, t, trafalgar=pop(t, L[1] + 0.3))
        return
    if t < L[3] - 0.2:   # มหาศึกกลางสมุทร
        sea(g, SEA_Y, t)
        smoke(g, 540, 700, t, 6, 1.2)
        ship(g, 280, SEA_Y + 80, 0.62, "uk", t, fire=True)
        ship(g, 820, SEA_Y + 80, 0.62, "fr", t, flip=True, fire=True)
        g.label("มหาศึกกลางสมุทร!", CX, 380, 90, color=RED, sc=pop(t, L[2]), rot=-3)
        return
    if t < L[5] - 0.2:   # นโปเลียนจะบดขยี้อังกฤษ
        g.ground(GROUND, WHITE)
        for i in range(3):
            ship(g, 760 + i * 120, 820 + i * 40, 0.25, "fr", t, flip=True)
        pose = "tuck" if t < L[4] - 0.2 else "point"
        person(g, 300, GROUND, NAPOLEON, 0.9, mood="smug", pose=pose, turn=0.3, seed=2)
        g.name_tag(t, L[3] + 0.3, 740, 420, "นโปเลียน โบนาปาร์ต", "จักรพรรดิแห่งฝรั่งเศส", side=-1)
        if t > L[4] - 0.2:
            with g.at(830, 1100, pop(t, L[4] - 0.1)):
                g.blob(0, 0, 120, 90, hexc("#f3dccb"), 6, 3)
                g.label("อังกฤษ", 0, 0, 44)
            g.label("บดขยี้ให้สิ้นซาก!", 760, 940, 60, color=RED, sc=pop(t, L[4] + 0.5))
        return
    if t < L[6] - 0.2:   # จำนวนเรือน้อยกว่า
        g.ground(GROUND, WHITE)
        tactical_bg(g)
        wall_of_ships(g, t, 11, ["fr", "es"], 560, k=seg(t, L[5], L[5] + 0.8), s=0.7)
        wall_of_ships(g, t, 7, ["uk"], 900, 220, 860, k=seg(t, L[5] + 0.8, L[5] + 1.6), s=0.7)
        g.label("ศัตรู", CX, 430, 60, color=NAVY, sc=pop(t, L[5]))
        g.label("อังกฤษ: น้อยกว่า", CX, 1060, 60, sc=pop(t, L[5] + 1.0))
        return
    # แม่ทัพแขนด้วนตาบอดข้างเดียว -> เนลสัน
    g.ground(GROUND, WHITE)
    reveal = seg(t, L[7] - 0.2, L[7] + 0.4)
    if reveal < 1:
        with g.alpha(1 - reveal), g.silhouette(INK, 0.92):
            person(g, CX, GROUND, NELSON, 0.95, mood="firm", seed=1)
        g.label("แขนด้วน", 260, 640, 60, color=RED, sc=pop(t, L[6] + 0.2) * (1 - reveal))
        g.label("ตาบอด 1 ข้าง", 820, 470, 60, color=RED, sc=pop(t, L[6] + 0.8) * (1 - reveal))
    if reveal > 0:
        g.sunburst(CX, 700, 250, 620, 22, t * 10, 12, (0.95, 0.85, 0.55, 0.8 * reveal))
        with g.alpha(reveal):
            person(g, CX, GROUND, NELSON, 0.95, mood="firm", seed=1)
        g.label('"โฮราทิโอ เนลสัน"', CX, 330, 96, color=GOLDTXT, sc=pop(t, L[7] + 0.2), rot=-3)
        g.name_tag(t, L[7] + 0.6, 880, 1120, "โฮราทิโอ เนลสัน", "พลเรือเอกแห่งราชนาวีอังกฤษ", side=-1)


# ------------------------------------------------------------------ 2. odds
def s_odds(g, t, L, d):
    if t < L[2] - 0.2:
        europe_map(g, t, army=pop(t, 0.4))
        g.label("กองทัพมหึมา", 620, 600, 54, color=NAVY, sc=pop(t, 0.8))
        if t > L[1] - 0.2:
            k = e_out(seg(t, L[1], L[1] + 1.0))
            g.line([(500, 680), (lerp(500, 440, k), lerp(680, 540, k))], 14, RED, amp=0)
            g.label("บุกยึด!", 250, 640, 70, color=RED, sc=pop(t, L[1] + 0.6))
        return
    g.ground(GROUND, WHITE)
    tactical_bg(g)
    wall_of_ships(g, t, 33, ["fr", "es"], 520, 80, 1000, k=seg(t, L[2], L[2] + 1.4), s=0.4)
    counter(g, CX, 380, 33, "ลำ · ฝรั่งเศส + สเปน", NAVY, 90, pop(t, L[2] + 0.3))
    if t > L[3] - 0.2:   # กำแพงเหล็ก
        with g.alpha(show(t, L[3]) * 0.5):
            _rr(g.c, 50, 488, 980, 64, 12)
            _shade(g.c, GREY, 0, 0)
        g.label("กำแพงเหล็ก", CX, 640, 64, color=GREY, sc=pop(t, L[3] + 0.3))
    if t > L[4] - 0.2:
        for i in range(27):
            ship_icon(g, 300 + (i % 9) * 80, 800 + (i // 9) * 95, 0.62 * pop(t, L[4] + i * 0.03), "uk", -90)
        counter(g, 160, 830, 27, "ลำ", INK, 80, pop(t, L[4] + 0.2))
    if t > L[5] - 0.2:
        g.label("แพ้สถานเดียว!", CX, 1100, 90, color=RED, sc=pop(t, L[5] + 0.2), rot=-4)


# ------------------------------------------------------------------ 3. plan
def s_plan(g, t, L, d):
    if t < L[3] - 0.2:
        deck(g, t)
        pose = "down" if t < L[1] else "point" if t < L[2] else "salute"
        person(g, 300, GROUND - 40, NELSON, 0.72, mood="firm", pose=pose, turn=0.3, seed=1, talk=t > L[2])
        if t < L[1] - 0.2:
            g.label("แผนบ้าระห่ำที่สุด!", CX, 380, 84, color=RED, sc=pop(t, 0.6), rot=-3)
        else:
            signal_flags(g, 850, 120, 1060, 760, 9, t, seg(t, L[1], L[1] + 2.0))
            if t > L[2] - 0.2:
                with g.at(CX - 60, 400, pop(t, L[2])):
                    g.bubble(0, 0, 820, 260, WHITE, tail=(-1, 1))
                    g.label('"อังกฤษคาดหวังว่า', 0, -50, 56)
                    g.label('ชายทุกคนจะทำหน้าที่ของตน"', 0, 30, 56, color=NAVY)
                g.label("England expects that every man will do his duty", CX - 60, 570, 30, color=GREY,
                        sc=pop(t, L[2] + 0.6))
        return
    if t < L[4] - 0.2:   # ฉีกตำรา
        g.ground(GROUND, WHITE)
        book(g, CX, 760, 1.6 * pop(t, L[3] - 0.1), e_out(seg(t, L[3] + 0.9, L[3] + 1.6)))
        g.label("ฉีกตำราทิ้ง!", CX, 380, 96, color=RED, sc=pop(t, L[3] + 1.0), rot=-4)
        return
    # แผนผังยุทธวิธี: แบบเดิม (ขนาน) -> แบบเนลสัน (สองสายตั้งฉาก)
    g.ground(GROUND, WHITE)
    tactical_bg(g)
    wall_of_ships(g, t, 11, ["fr", "es"], 520, 110, 970, s=0.62)
    g.label("ศัตรู", 960, 440, 46, color=NAVY)
    if t < L[5] - 0.2:   # แบบเดิม: แล่นขนาน ยิงโต้ตอบ
        for i in range(8):
            ship_icon(g, 150 + i * 110, 720, 0.6, "uk")
        for i in range(4):
            g.line([(220 + i * 200, 690), (220 + i * 200, 560)], 4, GREY, amp=0)
        g.label("แบบเดิม: แล่นขนาน", CX, 860, 56, color=GREY, sc=pop(t, L[4]))
        return
    split = e_io(seg(t, L[5], L[5] + 1.2))
    adv = e_io(seg(t, L[6], L[6] + 1.6))
    for col, cx in enumerate((340, 720)):
        for i in range(5):
            x = lerp(CX, cx, split)
            y = 1180 - i * 90 - adv * 380
            ship_icon(g, x, y, 0.62, "uk", -90)
        if adv > 0:
            g.line([(cx, 1160), (cx, lerp(1160, 640, adv))], 8, RED, amp=0)
    g.label("แบ่ง 2 สาย", CX, 1220, 56, sc=pop(t, L[5] + 0.3))
    if t > L[6]:
        g.label("พุ่งชนแบบตั้งฉาก!", CX, 380, 84, color=RED, sc=pop(t, L[6] + 0.4), rot=-3)


# ------------------------------------------------------------------ 4. charge
def s_charge(g, t, L, d):
    if t < L[3] - 0.2:
        sea(g, SEA_Y, t)
        if t < L[1] - 0.1:
            ship(g, CX, SEA_Y + 80, 0.7, "uk", t)
            g.label("นั่นหมายความว่า...", CX, 380, 80, sc=pop(t, 0.1))
            return
        if t < L[2] - 0.2:   # ฝ่าห่ากระสุน ยิงสวนไม่ได้
            ship(g, 330, SEA_Y + 80, 0.62, "uk", t)
            for i in range(9):
                p = ((t - L[1]) * 0.9 + i / 9) % 1
                cannonball(g, lerp(1150, 500, p), 560 + 40 * math.sin(i * 2.3) + 180 * p * p, 14)
            for i in range(4):
                flash(g, 1080, 520 + i * 90, 40 + 10 * math.sin(t * 9 + i), 0.8)
            g.label("ห่ากระสุนนับพันนัด", CX, 330, 70, color=RED, sc=pop(t, L[1] + 0.3))
            g.label("นานหลายสิบนาที", CX, 430, 56, sc=pop(t, L[1] + 2.5))
            return
        # บนดาดฟ้า: ยิงสวนไม่ได้
        deck(g, t)
        person(g, 230, GROUND - 40, SAILORS[0], 0.78, mood="worry", turn=0.3, seed=3)
        person(g, 520, GROUND - 40, SAILORS[1], 0.78, mood="shock", turn=0.2, seed=4)
        person(g, 760, GROUND - 40, NELSON, 0.8, mood="firm", seed=1)
        for i in range(4):
            p = ((t - L[2]) * 1.2 + i / 4) % 1
            cannonball(g, lerp(1150, -100, p), 420 + i * 70 + 40 * p, 14)
        g.label("ยิงสวนไม่ได้แม้แต่นัดเดียว!", CX, 330, 66, color=RED, sc=pop(t, L[2] + 0.3))
        return
    if t < L[4] - 0.2:   # ควันไฟ เสียงระเบิด
        sea(g, SEA_Y, t)
        ship(g, CX, SEA_Y + 80, 0.7, "uk", t, damage=0.6, fire=True)
        for i in range(4):
            smoke(g, 150 + i * 260, 900, t + i, 4, 1.3)
        for i in range(3):
            flash(g, 200 + i * 340, 600 + 80 * math.sin(t * 3 + i), 60 * abs(math.sin(t * 4 + i * 2)), 0.9)
        g.label("ไม้ฉีกขาด · ระเบิด · ควันไฟ", CX, 330, 62, sc=pop(t, L[3] + 0.3))
        return
    if t < L[6] - 0.2:   # ทะลวงแนวข้าศึก -> แตกพ่าย
        g.ground(GROUND, WHITE)
        tactical_bg(g)
        brk = e_io(seg(t, L[4] + 0.2, L[4] + 2.0))
        scat = e_out(seg(t, L[5], L[5] + 1.4))
        for i in range(11):
            x = lerp(70, 1010, i / 10)
            side = "fr" if i % 2 else "es"
            dy = 200 * scat * hn(i, 5)
            ship_icon(g, lerp(110, 970, i / 10) + 40 * scat * hn(i, 9), 640 + dy, 0.62, side, 70 * scat * hn(i, 3))
        for cx in (340, 720):
            for i in range(5):
                y = 1180 - i * 90 - brk * 640
                ship_icon(g, cx, y, 0.62, "uk", -90)
        g.label("ทะลวงแนวข้าศึก!", CX, 380, 80, color=RED, sc=pop(t, L[4] + 1.6))
        if t > L[5]:
            g.label("แตกพ่ายไม่เป็นท่า!", CX, 1180, 70, color=NAVY, sc=pop(t, L[5] + 0.6))
        return
    # ระยะประชิด
    sea(g, SEA_Y, t)
    ship(g, 340, SEA_Y + 80, 0.6, "uk", t, fire=True)
    ship(g, 740, SEA_Y + 90, 0.6, "fr", t, flip=True, damage=0.8)
    smoke(g, 540, 820, t, 5, 1.0)
    g.label("ระยะประชิด: อังกฤษถนัดที่สุด!", CX, 340, 62, color=GREEN, sc=pop(t, L[6] + 0.3))


# ------------------------------------------------------------------ 5. shot
def s_shot(g, t, L, d):
    deck(g, t)
    for i in range(3):
        smoke(g, 150 + i * 380, 700, t + i, 4, 1.1, col=hexc("#d9d0c4"))
    if t < L[2] - 0.2:
        person(g, 260, GROUND - 40, HARDY, 0.68, mood="firm", turn=0.3, seed=5)
        person(g, 640, GROUND - 40, NELSON, 0.66, mood="firm", seed=1, turn=0.2)
        g.label("เปลวไฟแห่งชัยชนะ", CX, 330, 72, color=GOLDTXT, sc=pop(t, 0.3))
        if t > L[1] - 0.2:   # พลแม่นปืนบนเสากระโดงเรือฝรั่งเศส (เงา + แสงวาบ)
            with g.silhouette(INK, 0.9):
                person(g, 1000, 520, SAILORS[2], 0.32, pose="spy", turn=-0.4, seed=6, shadow=False)
            if (t - L[1]) % 2.2 < 0.15:
                flash(g, 930, 300, 50, 1.0)
            g.label("พลแม่นปืนฝรั่งเศส", 760, 470, 50, color=RED, sc=pop(t, L[1] + 0.4))
        g.name_tag(t, 0.6, 450, 470, "โทมัส ฮาร์ดี", "กัปตันเรือหลวงวิกตอรี", side=1)
        return
    # ไม่แสดงบาดแผล: แสงวาบ หมวกร่วงลงพื้น แล้วเนลสันล้มลง
    if t < L[3] - 0.2:
        person(g, 260, GROUND - 40, HARDY, 0.68, mood="worry", turn=0.3, seed=5)
        person(g, 640, GROUND - 40, NELSON, 0.66, mood="shock", seed=1)
        g.label("ไหล่ → ปอด → กระดูกสันหลัง", CX, 330, 56, color=RED, sc=pop(t, L[2] + 0.3))
        if L[2] - 0.2 < t < L[2] + 0.25:   # แสงวาบขาวแทนภาพกระสุน
            with g.alpha(1 - seg(t, L[2], L[2] + 0.25)):
                g.c.rectangle(-400, -400, W + 800, 1700)
                g.c.set_source_rgba(1, 1, 1, 0.9)
                g.c.fill()
        return
    # ล้มลงบนดาดฟ้า
    fall = e_out(seg(t, L[3] - 0.2, L[3] + 0.6))
    person(g, 260, GROUND - 40, HARDY, 0.68, mood="shock", turn=0.3, seed=5)
    person(g, 860, GROUND - 40, NELSON, 0.66, mood="worry", seed=1, lean=-82 * fall, shadow=False)
    hk = e_in(seg(t, L[3] - 0.1, L[3] + 0.5))
    with g.at(lerp(860, 960, hk), lerp(560, GROUND - 60, hk), 0.66, 200 * hk):
        g.poly([(-90, 0), (0, -60), (90, 0), (0, -14)], INK, 4)
    if t > L[4] - 0.2:
        g.label("สู้จนวินาทีสุดท้าย...", CX, 360, 76, color=NAVY, sc=pop(t, L[4]))


# ------------------------------------------------------------------ 6. death
def s_death(g, t, L, d):
    c = g.c
    # ห้องใต้ท้องเรือที่มืดสลัว: คานไม้ + โคมไฟ (พื้นยังขาว ใช้แสงโคมสีอุ่น)
    for i in range(6):
        _rr(c, -300 + i * 300, 260, 60, 60, 4)
        _shade(c, WOOD2, 4, 0.3)
    _rr(c, -400, 230, W + 800, 40, 4)
    _shade(c, WOOD2, 5, 0.3)
    lantern(g, 760, 330, 1.0, t)
    dim = seg(t, L[5] + 1.5, d)
    _rr(c, 60, 1090, 820, 100, 20)
    _shade(c, hexc("#e9e2d4"), 5, 0.2)
    person(g, 130, 1100, NELSON, 0.66, mood="smile" if t > L[4] - 0.2 else "worry", seed=1,
           lean=90, shadow=False, talk=L[5] < t < L[5] + 2.5)
    _rr(c, 90, 1050, 380, 70, 30)   # ผ้าห่มคลุมตัว
    _shade(c, WHITE, 5, 0.15)
    person(g, 940, GROUND, HARDY, 0.7, mood="sad" if t < L[2] else "smile", turn=-0.4, seed=5,
           talk=L[1] < t < L[4])
    if t > L[1] - 0.2 and t < L[4] - 0.2:
        with g.at(480, 520, pop(t, L[1])):
            g.bubble(0, 0, 520, 300, WHITE, tail=(1, 1))
            if t < L[2] - 0.2:
                g.label("รายงาน!", 0, 0, 64)
            elif t < L[3] - 0.2:
                g.label("ยึด/ทำลาย 22 ลำ", 0, -50, 56, color=NAVY)
                for i in range(int(min(22, 22 * seg(t, L[2], L[2] + 1.6)))):
                    ship_icon(g, -200 + (i % 11) * 40, 40 + (i // 11) * 50, 0.28, "fr" if i % 2 else "es")
            else:
                g.label("อังกฤษไม่จม", 0, -40, 56, color=GREEN)
                g.label("แม้แต่ลำเดียว!", 0, 40, 56, color=GREEN)
    if t > L[4] - 0.2 and t < L[5] - 0.2:
        g.label("ยิ้มรับชัยชนะทั้งน้ำตา", 480, 600, 58, sc=pop(t, L[4] + 0.3))
    if t > L[5] - 0.2:
        g.label('"ขอบคุณพระเจ้า', 480, 520, 66, color=NAVY, sc=pop(t, L[5]))
        g.label('ผมได้ทำหน้าที่ของผมแล้ว"', 480, 610, 66, color=NAVY, sc=pop(t, L[5] + 0.4))
        g.label("Thank God I have done my duty", 480, 700, 34, color=GREY, sc=pop(t, L[5] + 0.9))
    if dim > 0:
        with g.alpha(0.35 * dim):
            c.rectangle(-400, -400, W + 800, 1700)
            c.set_source_rgba(0.55, 0.5, 0.45, 1)
            c.fill()


# ------------------------------------------------------------------ 7. legacy
def s_legacy(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:
        nelson_column(g, CX, GROUND, 0.8 * pop(t, 0.2))
        g.label("ชัยชนะที่แลกด้วยชีวิต", CX, 300, 72, color=GOLDTXT, sc=pop(t, 0.6))
        g.label("เสาเนลสัน · ลอนดอน", 300, 1100, 40, color=GREY, sc=pop(t, 1.2))
        return
    if t < L[2] - 0.2:
        person(g, 330, GROUND, NAPOLEON, 0.86, mood="sad", pose="tuck", turn=-0.4, seed=2)
        with g.at(800, 900, 1.0):
            g.blob(0, 0, 150, 110, hexc("#f3dccb"), 6, 3)
            g.label("อังกฤษ", 0, 0, 48)
        g.label("ฝันบุกอังกฤษ...", CX, 360, 76, sc=pop(t, L[1] + 0.2))
        g.label("ดับไปตลอดกาล", CX, 470, 70, color=RED, sc=pop(t, L[1] + 1.2))
        return
    sea(g, SEA_Y, t)
    g.sunburst(CX, 700, 200, 620, 20, t * 10, 10, (0.95, 0.85, 0.55, 0.8))
    ship(g, CX, SEA_Y + 80, 0.7, "uk", t)
    g.label("เจ้าแห่งท้องทะเล", CX, 340, 90, color=GOLDTXT, sc=pop(t, L[2] + 0.2), rot=-3)
    g.label("เกือบ 100 ปี", CX, 460, 70, sc=pop(t, L[2] + 1.0))


# ------------------------------------------------------------------ 8. lesson
def s_lesson(g, t, L, d):
    g.ground(GROUND, WHITE)
    g.label("บทเรียน", CX, 380, 100, sc=pop(t, 0.1), rot=-3)
    if t < L[2] - 0.2:
        if t > L[1] - 0.2:
            k = e_io(seg(t, L[1] + 0.5, L[1] + 2.0))
            gap = 30 * k + 140 * e_out(seg(t, L[1] + 2.0, L[2]))   # กรอบเดิมแตกออกจากกัน
            for i in range(3):   # กรอบเดิม: เส้นขนาน
                tilt = 18 * seg(t, L[1] + 2.0, L[2]) * (1 if i % 2 else -1)
                g.line([(150 - gap * 0.3, 640 + i * 60), (CX - gap, 640 + i * 60 + tilt)], 8, GREY, amp=0)
                g.line([(CX + gap, 640 + i * 60 - tilt), (930 + gap * 0.3, 640 + i * 60)], 8, GREY, amp=0)
            for i in range(4):
                g.sparkle(CX + (i - 1.5) * 120, 560 + 30 * math.sin(t * 4 + i), 16 * seg(t, L[1] + 1.8, L[1] + 2.2))
            g.line([(CX, 1100), (CX, lerp(1100, 560, k))], 16 + 4 * math.sin(t * 6) * seg(t, L[1] + 2.0, L[1] + 2.4), RED, amp=0)
            g.poly([(CX - 30, lerp(1100, 560, k) + 20), (CX, lerp(1100, 560, k) - 30), (CX + 30, lerp(1100, 560, k) + 20)], RED, 0)
            g.label("กล้าฉีกกรอบเดิม", CX, 1180, 66, color=RED, sc=pop(t, L[1] + 1.0))
        return
    for i in range(6):
        a = t * 1.2 + i * 1.05
        g.sparkle(CX + 330 * math.cos(a), 780 + 260 * math.sin(a), 18 + 6 * math.sin(t * 4 + i))
    with g.at(CX, 780 + 12 * math.sin(t * 2.2), pop(t, L[2] - 0.1) * (1 + 0.04 * math.sin(t * 3))):
        g.sunburst(0, 0, 150, 300, 16, t * 15, 10, (0.95, 0.83, 0.48, 0.8))
        g.circle(0, 0, 120, GOLD, 8)
        g.star(0, 0, 70, GOLD2, 6)
        g.poly([(-60, 100), (-90, 260), (-20, 220), (0, 120)], RED, 5)
        g.poly([(60, 100), (90, 260), (20, 220), (0, 120)], NAVY, 5)
    g.label("ความเสียสละอันสูงสุด", CX, 1150, 66, color=GOLDTXT, sc=pop(t, L[2] + 0.4))


# ------------------------------------------------------------------ 9. outro
def s_outro(g, t, L, d):
    if t < L[4] - 0.2:
        deck(g, t)
        person(g, 400, GROUND - 40, SAILORS[0], 0.72, mood="worry" if t < L[3] else "firm", turn=0.3, seed=3,
               pose="down" if t < L[3] else "fist")
        g.label("ถ้าเป็นคุณ?", CX, 380, 90, sc=pop(t, 0.1))
        if t > L[2] - 0.2:
            for i in range(4):
                p = ((t - L[2]) * 1.1 + i / 4) % 1
                cannonball(g, lerp(1150, 650, p), 520 + i * 80, 14)
        if t > L[3] - 0.2:
            g.label("เอาชนะความกลัว?", 720, 1150, 66, color=RED, sc=pop(t, L[3] + 0.2))
        return
    if t < L[5] - 0.2:
        g.ground(GROUND, WHITE)
        person(g, CX, GROUND, NELSON, 0.75, mood="firm", seed=1, pose="down", pose2="salute",
               k=e_io(seg(t, L[4] + 1.2, L[4] + 2.2)) - e_io(seg(t, L[4] + 3.4, L[4] + 4.2)))
        for i in range(5):
            g.sparkle(180 + i * 180, 1150 + 20 * math.sin(t * 3 + i), 14 * pop(t, L[4] + 0.5 + i * 0.3))
        g.label("อะไรทำให้ยอมสละชีวิต", CX, 340, 66, sc=pop(t, L[4] + 0.2))
        g.label("เพื่อหน้าที่?", CX, 440, 76, color=NAVY, sc=pop(t, L[4] + 0.8))
        return
    g.ground(GROUND, WHITE)
    k = pop(t, L[5] - 0.1)
    with g.at(CX, 760, k):
        g.bubble(0, 0, 640, 300, WHITE, tail=(-1, 1))
        for i in range(3):
            g.circle(-120 + i * 120, 0, 26 + 6 * math.sin(t * 6 - i), INK, 0)
    g.label("คอมเมนต์คุยกันได้เลย!", CX, 1080, 70, color=RED, sc=pop(t, L[5] + 0.4))


SCENES = {
    "hook": s_hook, "odds": s_odds, "plan": s_plan, "charge": s_charge, "shot": s_shot, "death": s_death,
    "legacy": s_legacy, "lesson": s_lesson, "outro": s_outro,
}
NO_IRIS = set()
