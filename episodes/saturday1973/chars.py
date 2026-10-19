"""ตัวละครและพร็อพ: การสังหารหมู่คืนวันเสาร์ 20 ต.ค. 1973 (คนแบบกึ่งเสมือนจริงจาก src/people.py)"""
import math

import cairo

from gfx import BROWN, BROWN2, GOLD, GOLD2, GREY, ICE, INK, LGREY, NAVY, RED, WHITE, hexc
from people import Look, _rr, _shade, _smooth_path, _stroke

# ริชาร์ด นิกสัน: ผมดำหวีเสยเป็นลอน หน้าผากเถิกสองข้าง จมูกยาวปลายงุ้ม แก้มย้อย หนวดเคราเขียว สูทกรมท่า เข็มกลัดธงชาติ
NIXON = Look(hair="nixon", hair_col=hexc("#2e2723"), suit=hexc("#283550"), tie=hexc("#5b2530"), w=62, jaw=0.75,
             jowls=1.0, nose=1.35, brow=1.35, stubble=1.0, age=0.8, build=1.05, pin=True)
# อาร์ชิบัลด์ ค็อกซ์: ผมสั้นเกรียนสีเทา (ทรงคูรว์คัต) หน้าผอมยาว หูกระต่าย เสื้อสูททวีดน้ำตาล
COX = Look(hair="crew", hair_col=hexc("#9a958c"), suit=hexc("#6a5844"), tie=hexc("#2b3f63"), bowtie=True, w=56,
           jaw=0.2, nose=1.1, brow=0.9, age=0.9, build=0.92, height=1.03)
# เอลเลียต ริชาร์ดสัน (อัยการสูงสุด): สูงโปร่ง หน้าผากสูง ผมเสยเรียบสีเทาเข้ม สูทเทา
RICHARDSON = Look(hair="slick", hair_col=hexc("#4b4741"), suit=hexc("#4a4f58"), tie=hexc("#2f4a6e"), w=57, jaw=0.35,
                  nose=1.15, brow=0.95, age=0.7, build=0.95, height=1.06)
# วิลเลียม รัคเคิลส์เฮาส์ (รองอัยการสูงสุด): แว่นกรอบดำหนา ผมดำแสกข้าง สูทถ่าน
RUCKELSHAUS = Look(hair="part", hair_col=hexc("#26211e"), suit=hexc("#36393f"), tie=hexc("#7a2e2e"), w=60, jaw=0.6,
                   nose=1.0, brow=1.1, glasses="thick", age=0.4, build=1.02)
# โรเบิร์ต บอร์ก (Solicitor General): ผมดำหนา จอนยาว แว่นกรอบบาง ร่างท้วม
BORK = Look(hair="full", hair_col=hexc("#2a2420"), suit=hexc("#3b3a36"), tie=hexc("#4a5a3a"), w=64, jaw=0.7,
            nose=1.05, brow=1.2, glasses="thin", age=0.5, build=1.15)
AGENT = Look(hair="short", hair_col=hexc("#3a2f28"), suit=hexc("#232327"), tie=hexc("#232327"), w=58, jaw=0.6, age=0.3)
AGENT2 = Look(hair="short", hair_col=hexc("#6b4a33"), suit=hexc("#232327"), tie=hexc("#232327"), w=58, jaw=0.5, age=0.2,
              skin=hexc("#d9a37e"))
CITIZENS = [
    Look(hair="full", hair_col=hexc("#6b4a33"), suit=hexc("#7d6a4f"), tie=hexc("#c8553d"), w=58, age=0.1),
    Look(hair="short", hair_col=hexc("#2b2622"), suit=hexc("#3f6496"), tie=hexc("#e3a92b"), w=60, age=0.3, skin=hexc("#b9825c")),
    Look(hair="part", hair_col=hexc("#a8763e"), suit=hexc("#5f7f55"), tie=hexc("#2b3f63"), w=57, age=0.2),
    Look(hair="crew", hair_col=hexc("#2b2622"), suit=hexc("#8a6a9a"), tie=hexc("#1b1916"), w=60, age=0.5, skin=hexc("#8a5a3c")),
]

WOOD = hexc("#8a5a36")
WOOD2 = hexc("#6e4528")
NIGHT = hexc("#1f2a44")


def desk(g, x, y, w=620, sc=1.0):
    """โต๊ะทำงานไม้ (Resolute Desk) — x,y = กลางขอบบนโต๊ะ"""
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -w / 2, 0, w, 34, 8)
        _shade(c, WOOD, 5, 0.3)
        _rr(c, -w / 2 + 20, 30, w - 40, 300, 6)
        _shade(c, WOOD2, 5, 0.35)
        for sx in (-1, 1):
            _rr(c, sx * (w / 2 - 130) - 90, 60, 180, 230, 10)
            _shade(c, WOOD, 4, 0.25)
            c.new_path()
            c.arc(sx * (w / 2 - 130), 175, 30, 0, 2 * math.pi)
            _shade(c, GOLD, 3, 0.2)
        c.new_path()
        c.arc(0, 150, 46, 0, 2 * math.pi)
        _shade(c, GOLD2, 4, 0.3)
        g.star(0, 150, 22, WHITE, 3)


def flag_us(g, x, y, sc=1.0, t=0.0):
    """ธงชาติสหรัฐฯ บนเสา"""
    with g.at(x, y, sc):
        g.rrect(-6, -520, 12, 520, 4, GOLD, 4)
        g.circle(0, -526, 12, GOLD2, 4)
        g.flag(6, -500, 230, 150, "us", t, 0.6)


def window_night(g, x, y, w=300, h=420, moon=True):
    c = g.c
    with g.at(x, y):
        _rr(c, -w / 2 - 22, -h / 2 - 22, w + 44, h + 44, 10)
        _shade(c, hexc("#e9e2d4"), 5, 0.15)
        _rr(c, -w / 2, -h / 2, w, h, 4)
        gr = cairo.LinearGradient(0, -h / 2, 0, h / 2)
        gr.add_color_stop_rgba(0, *NIGHT[:3], 1)
        gr.add_color_stop_rgba(1, 0.25, 0.32, 0.5, 1)
        c.set_source(gr)
        c.fill_preserve()
        c.set_source_rgba(*INK)
        c.set_line_width(5)
        c.stroke()
        if moon:
            g.circle(w * 0.2, -h * 0.25, 34, hexc("#f4eccf"), 0)
            g.circle(w * 0.2 + 14, -h * 0.25 - 8, 30, NIGHT, 0)
        for i in range(6):
            g.circle(-w * 0.35 + i * w * 0.13, -h * 0.35 + (i * 37 % 60), 2.5, WHITE, 0)
        g.line([(0, -h / 2), (0, h / 2)], 8, hexc("#e9e2d4"), amp=0)
        g.line([(-w / 2, 0), (w / 2, 0)], 8, hexc("#e9e2d4"), amp=0)


def white_house(g, x, y, sc=1.0, night=False, lit=True):
    """ทำเนียบขาวด้านหน้า (มีเสาโค้งระเบียง)"""
    c = g.c
    with g.at(x, y, sc):
        wall = hexc("#f7f5ef") if not night else hexc("#dfe3ea")
        _rr(c, -380, -260, 760, 260, 4)
        _shade(c, wall, 6, 0.18)
        c.new_path()
        c.move_to(-150, -260)
        c.line_to(0, -340)
        c.line_to(150, -260)
        c.close_path()
        _shade(c, wall, 6, 0.15)
        _rr(c, -400, -278, 800, 22, 4)
        _shade(c, wall, 5, 0.1)
        for k in range(-3, 4):
            _rr(c, k * 42 - 9, -250, 18, 240, 4)
            _shade(c, WHITE, 3, 0.25)
        for row in (-200, -110):
            for k in (-330, -270, -210, 210, 270, 330):
                _rr(c, k - 18, row, 36, 56, 3)
                _shade(c, GOLD2 if (night and lit) else ICE, 3, 0.2)
        _rr(c, -26, -80, 52, 80, 4)
        _shade(c, WOOD2, 3, 0.2)
        g.line([(0, -340), (0, -400)], 5)
        g.flag(0, -400, 70, 44, "us", g.t, 0.6)


def watergate(g, x, y, sc=1.0):
    """อาคารวอเตอร์เกต: ตึกโค้งระเบียงฟันปลา"""
    c = g.c
    with g.at(x, y, sc):
        _smooth_path(c, [(-300, 0), (-310, -420), (0, -470), (310, -420), (300, 0)], True)
        _shade(c, hexc("#f2efe8"), 6, 0.2)
        for row in range(8):
            yy = -40 - row * 50
            pts = [(-300 + i * 30, yy + 14 * math.sin(i * 0.9)) for i in range(21)]
            _stroke(c, pts, 4, INK, 0.6)
            for i in range(0, 20, 2):
                gx, gy = -294 + i * 30, yy - 30 + 14 * math.sin(i * 0.9)
                _rr(c, gx, gy, 20, 24, 3)
                lit = (row * 7 + i) % 5 == 0
                _shade(c, GOLD2 if lit else hexc("#5f6f88"), 0, 0)
        g.text("WATERGATE", 0, -500, 46, "kanit", stroke=8, stroke_color=WHITE)


def reel_recorder(g, x, y, sc=1.0, t=0.0, spin=True, glow=0.0):
    """เครื่องอัดเทปแบบม้วน (ระบบอัดเสียงลับ)"""
    c = g.c
    with g.at(x, y, sc):
        if glow > 0:
            rg = cairo.RadialGradient(0, -60, 0, 0, -60, 260)
            rg.add_color_stop_rgba(0, 1, 0.3, 0.2, 0.35 * glow)
            rg.add_color_stop_rgba(1, 1, 0.3, 0.2, 0)
            c.set_source(rg)
            c.arc(0, -60, 260, 0, 2 * math.pi)
            c.fill()
        _rr(c, -170, -150, 340, 160, 14)
        _shade(c, hexc("#5a5550"), 5, 0.3)
        _rr(c, -150, -40, 300, 34, 6)
        _shade(c, hexc("#2c2a28"), 3, 0)
        for sx in (-1, 1):
            cx, cy = sx * 80, -150
            c.new_path()
            c.arc(cx, cy, 70, 0, 2 * math.pi)
            _shade(c, hexc("#3d3936"), 5, 0.3)
            c.new_path()
            c.arc(cx, cy, 44, 0, 2 * math.pi)
            _shade(c, hexc("#8a5a36"), 3, 0.2)
            a0 = t * 5 * (1 if spin else 0)
            for i in range(3):
                a = a0 + i * 2.094
                c.new_path()
                c.arc(cx + 24 * math.cos(a), cy + 24 * math.sin(a), 10, 0, 2 * math.pi)
                _shade(c, hexc("#3d3936"), 0, 0)
            c.new_path()
            c.arc(cx, cy, 8, 0, 2 * math.pi)
            _shade(c, LGREY, 3, 0)
        _stroke(c, [(-80, -80), (0, -40), (80, -80)], 3, hexc("#3a2a1c"), smooth=False)
        g.circle(130, -110, 10, RED if (int(t * 2) % 2 == 0) else hexc("#7a2e2e"), 3)
        for k in (-100, -60, -20, 20):
            _rr(c, k, -110, 26, 18, 4)
            _shade(c, LGREY, 2.5, 0.1)


def tape_reel(g, x, y, sc=1.0, rot=0.0, label=None):
    c = g.c
    with g.at(x, y, sc, rot):
        c.new_path()
        c.arc(0, 0, 70, 0, 2 * math.pi)
        _shade(c, hexc("#4a4440"), 5, 0.3)
        c.new_path()
        c.arc(0, 0, 50, 0, 2 * math.pi)
        _shade(c, hexc("#8a5a36"), 3, 0.2)
        for i in range(3):
            a = i * 2.094
            c.new_path()
            c.arc(26 * math.cos(a), 26 * math.sin(a), 11, 0, 2 * math.pi)
            _shade(c, hexc("#4a4440"), 0, 0)
        g.circle(0, 0, 8, LGREY, 3)
        if label:
            _rr(c, -44, 74, 88, 30, 4)
            _shade(c, WHITE, 3, 0)
            g.text(label, 0, 89, 22, "kanit")


def mic(g, x, y, sc=1.0):
    with g.at(x, y, sc):
        g.line([(0, 0), (0, 40)], 5)
        g.rrect(-14, -40, 28, 44, 12, GREY, 4)
        for k in (-28, -18, -8):
            g.line([(-10, k), (10, k)], 2, LGREY, amp=0)


def paper(g, x, y, sc=1.0, rot=0.0, title="", lines=4, stamp=None, stamp_k=1.0, col=WHITE, w=230, h=300):
    """เอกสาร: หัวเรื่อง + เส้นบรรทัด + ตราประทับ"""
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -w / 2 + 8, -h / 2 + 10, w, h, 6)
        c.set_source_rgba(0, 0, 0, 0.12)
        c.fill()
        _rr(c, -w / 2, -h / 2, w, h, 6)
        _shade(c, col, 4.5, 0.12)
        top = -h / 2 + 40
        if title:
            g.text(title, 0, top, 30, "kanit")
            top += 40
        for i in range(lines):
            yy = top + i * 28
            if yy > h / 2 - 50:
                break
            _stroke(c, [(-w / 2 + 26, yy), (w / 2 - 26 - (40 if i == lines - 1 else 0), yy)], 4, GREY, 0.6, smooth=False)
        _stroke(c, [(w / 2 - 110, h / 2 - 34), (w / 2 - 70, h / 2 - 46), (w / 2 - 30, h / 2 - 32)], 3.5, NAVY)   # ลายเซ็น
        if stamp and stamp_k > 0:
            from gfx import e_back
            s = max(e_back(min(stamp_k, 1.0)), 0.01) if stamp_k < 1 else 1.0
            with g.at(0, 30, s * (1 + 0.6 * (1 - min(stamp_k, 1))), -14):
                g.rrect(-92, -36, 184, 72, 10, None, 7, stroke=RED)
                g.text(stamp, 0, 0, 40, "kanit", RED)


def phone(g, x, y, sc=1.0, ring=0.0):
    """โทรศัพท์แบบหมุน"""
    c = g.c
    with g.at(x + (4 * math.sin(g.t * 60) if ring else 0), y, sc):
        _smooth_path(c, [(-80, 0), (-60, -70), (60, -70), (80, 0)])
        _shade(c, hexc("#2d2b29"), 5, 0.3)
        c.new_path()
        c.arc(0, -36, 26, 0, 2 * math.pi)
        _shade(c, LGREY, 3, 0.1)
        _rr(c, -90, -104, 180, 34, 16)
        _shade(c, hexc("#2d2b29"), 5, 0.3)


def clock(g, x, y, r=90, hour=21.0):
    c = g.c
    with g.at(x, y):
        c.new_path()
        c.arc(0, 0, r, 0, 2 * math.pi)
        _shade(c, WHITE, 6, 0.12)
        for i in range(12):
            a = i * math.pi / 6
            g.line([(math.sin(a) * r * 0.78, -math.cos(a) * r * 0.78), (math.sin(a) * r * 0.9, -math.cos(a) * r * 0.9)], 4, amp=0)
        ah = (hour % 12) / 12 * 2 * math.pi
        am = (hour % 1) * 2 * math.pi
        g.line([(0, 0), (math.sin(ah) * r * 0.5, -math.cos(ah) * r * 0.5)], 8, amp=0)
        g.line([(0, 0), (math.sin(am) * r * 0.75, -math.cos(am) * r * 0.75)], 5, amp=0)
        g.circle(0, 0, 7, INK, 0)


def capitol(g, x, y, sc=1.0):
    """อาคารรัฐสภา (แคปิตอล)"""
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -300, -120, 600, 120, 4)
        _shade(c, hexc("#f4f1ea"), 5, 0.15)
        _rr(c, -110, -200, 220, 90, 4)
        _shade(c, hexc("#f4f1ea"), 5, 0.15)
        c.new_path()
        c.arc(0, -200, 100, math.pi, 2 * math.pi)
        c.close_path()
        _shade(c, hexc("#f4f1ea"), 5, 0.25)
        _rr(c, -14, -330, 28, 40, 4)
        _shade(c, hexc("#f4f1ea"), 4, 0.1)
        for k in range(-5, 6):
            g.line([(k * 50, -110), (k * 50, -10)], 4, LGREY, amp=0)


def newspaper(g, x, y, sc=1.0, rot=0.0, head1="", head2=""):
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -170, -220, 340, 440, 4)
        _shade(c, hexc("#f2ecdc"), 5, 0.15)
        g.text("THE DAILY NEWS", 0, -185, 26, "kanit")
        g.line([(-150, -162), (150, -162)], 3, amp=0)
        g.text(head1, 0, -118, 50, "kanit", maxw=310)
        if head2:
            g.text(head2, 0, -50, 30, "kanitm", maxw=310)
        _rr(c, -150, -10, 140, 110, 3)
        _shade(c, LGREY, 3, 0.2)
        for i in range(7):
            _stroke(c, [(10, -4 + i * 18), (150, -4 + i * 18)], 3, GREY, 0.6, smooth=False)
        for i in range(5):
            _stroke(c, [(-150, 120 + i * 18), (150, 120 + i * 18)], 3, GREY, 0.6, smooth=False)


def sign(g, x, y, text, sc=1.0, rot=0.0, col=WHITE, w=260):
    """ป้ายประท้วงบนไม้"""
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -8, -20, 16, 220, 3)
        _shade(c, BROWN2, 4, 0.2)
        _rr(c, -w / 2, -150, w, 130, 8)
        _shade(c, col, 5, 0.12)
        g.text(text, 0, -86, 44, "kanit", RED if col == WHITE else INK, maxw=w - 20)


def nail_lid(g, x, y, sc=1.0, k=0.0):
    """ตะปูตัวสุดท้าย: ค้อนตอกตะปูลงแผ่นไม้ฝา (k 0..1 = ตะปูจมลง)"""
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -360, -40, 720, 90, 8)
        _shade(c, hexc("#a8774c"), 6, 0.3)
        for xx in (-280, -120, 60, 220):
            _stroke(c, [(xx, -20), (xx + 70, -16)], 3, WOOD2, 0.6)
        for nx in (-300, 300):
            g.circle(nx, 4, 13, GREY, 4)
        depth = 80 * k
        _rr(c, -6, -120 + depth, 12, 120, 3)
        _shade(c, LGREY, 4, 0.3)
        _rr(c, -26, -132 + depth, 52, 14, 4)
        _shade(c, GREY, 4, 0.3)
