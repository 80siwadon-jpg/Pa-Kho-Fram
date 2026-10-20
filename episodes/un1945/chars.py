"""ตัวละครและพร็อพ: กำเนิดองค์การสหประชาชาติ 24 ต.ค. 1945 (ไม่ใช้โลโก้ UN จริง ใช้ลูกโลก+ช่อมะกอกแบบการ์ตูน)"""
import math

from gfx import GOLD, GOLD2, GREY, INK, NAVY, RED, WHITE, hexc
from people import Look, _rr, _shade, _smooth_path, _stroke

UN_BLUE = hexc("#4b92db")
OLIVE = hexc("#5f8a46")
RUBBLE = hexc("#bdb6a6")

DELEGATES = [   # ผู้แทนประเทศต่าง ๆ ปี 1945
    Look(hair="slick", hair_col=hexc("#2b2622"), suit=hexc("#2f3036"), tie=hexc("#2b3f63"), w=56, age=0.5),
    Look(hair="part", hair_col=hexc("#9a948a"), suit=hexc("#3b3f48"), tie=hexc("#7a2e2e"), glasses="round", w=57,
         age=0.7, facial="mustache"),
    Look(hair="short", hair_col=hexc("#1b1714"), suit=hexc("#4a4038"), tie=hexc("#d9a441"), skin=hexc("#8a5a3c"),
         w=56, age=0.4),
    Look(hair="slick", hair_col=hexc("#1b1714"), suit=hexc("#1f2a44"), tie=hexc("#3c8d4f"), skin=hexc("#e8c09a"),
         w=55, age=0.45, glasses="thin"),
    Look(hair="bun", hair_col=hexc("#5a4a3a"), outfit="dress", suit=hexc("#2f3a4a"), w=54, age=0.45, height=0.93),
]
# ดาก ฮัมมาร์เฮิลด์ (เลขาธิการ UN คนที่ 2) — ผู้กล่าวประโยค "ไม่ใช่เพื่อพาไปสวรรค์ แต่กันไม่ให้ตกนรก"
HAMMARSKJOLD = Look(hair="slick", hair_col=hexc("#8a7a62"), suit=hexc("#2f3036"), tie=hexc("#2b2622"), w=56,
                    jaw=0.35, nose=1.15, brow=0.8, age=0.5)
WORKERS = [   # เจ้าหน้าที่มนุษยธรรม (เสื้อฟ้า)
    Look(hair="short", hair_col=hexc("#2b2622"), outfit="tee", suit=UN_BLUE, pants=hexc("#3a3a40"), w=56,
         hat="brodie", hat_trim=UN_BLUE),
    Look(hair="bun", hair_col=hexc("#5a3a22"), outfit="tee", suit=WHITE, pants=hexc("#3a4a6a"), w=54, height=0.93),
]


def globe(g, x, y, r, t=0.0, olive=True):
    """ลูกโลกเส้นรุ้งแวง + ช่อมะกอกโอบ (สัญลักษณ์สันติภาพแบบการ์ตูน)"""
    c = g.c
    with g.at(x, y):
        c.new_path()
        c.arc(0, 0, r, 0, 2 * math.pi)
        _shade(c, hexc("#dcebf8"), 6, 0.15)
        c.save()
        c.new_path()
        c.arc(0, 0, r, 0, 2 * math.pi)
        c.clip()
        for k in range(-2, 3):   # เส้นรุ้ง
            g.line([(-r, k * r * 0.35), (r, k * r * 0.35)], 3, UN_BLUE, amp=0)
        for k in range(5):   # เส้นแวงหมุน
            ph = (t * 0.4 + k / 5) % 1
            w = r * math.cos(ph * math.pi)
            c.save()
            c.scale(max(0.02, abs(w) / r), 1)
            c.new_path()
            c.arc(0, 0, r, 0, 2 * math.pi)
            c.restore()
            c.set_source_rgba(*UN_BLUE[:3], 0.8)
            c.set_line_width(3)
            c.stroke()
        for (px, py, s) in ((-0.3, -0.2, 0.35), (0.35, 0.1, 0.3), (0.0, 0.45, 0.2)):   # ทวีป
            g.blob(px * r + 20 * math.sin(t * 0.4), py * r, s * r, s * r * 0.7, (0.6, 0.8, 0.55, 0.9), 0,
                   seed=int(px * 10 + 5))
        c.restore()
        if olive:
            for sx in (-1, 1):
                for i in range(7):
                    a = math.pi / 2 + sx * (0.4 + i * 0.32)
                    lx, ly = (r + 40) * math.cos(a), (r + 40) * math.sin(a)
                    with g.at(lx, ly, 1, math.degrees(a) + 90 * sx):
                        g.blob(0, 0, 14, 30, OLIVE, 3, seed=i)


def rubble(g, y, t=0.0, smoke=True):
    """ซากเมืองหลังสงคราม (ไม่มีคน)"""
    c = g.c
    for i in range(7):
        x = -60 + i * 170
        h = 120 + (i * 71) % 200
        c.new_path()
        pts = [(x - 70, y), (x - 70, y - h), (x - 30, y - h - 30), (x + 10, y - h + 20), (x + 60, y - h - 10),
               (x + 70, y)]
        for p in pts:
            c.line_to(*p)
        c.close_path()
        _shade(c, RUBBLE, 5, 0.3)
        for k in range(2):
            _rr(c, x - 40 + k * 50, y - h + 50, 26, 34, 2)
            _shade(c, hexc("#4a4a4a"), 2, 0)
        if smoke:
            for j in range(2):
                u = (t * 0.3 + j / 2 + i * 0.17) % 1
                g.circle(x + 20 * math.sin(t + i), y - h - 40 - 220 * u, 30 + 40 * u, (0.6, 0.58, 0.55, 0.5 * (1 - u)),
                         0)


def charter(g, x, y, sc=1.0, rot=0.0, sigs=1.0, title="CHARTER OF THE UNITED NATIONS"):
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -240, -330, 480, 660, 8)
        _shade(c, hexc("#f4ecd4"), 6, 0.2)
        g.text(title, 0, -270, 28, "kanit", NAVY, maxw=420)
        g.line([(-200, -240), (200, -240)], 4, NAVY, amp=0)
        for i in range(6):
            g.line([(-190, -200 + i * 36), (190 - 60 * (i % 2), -200 + i * 36)], 5, hexc("#a8a08a"), amp=0)
        n = int(12 * sigs)
        for i in range(n):
            sx, sy = -170 + (i % 4) * 115, 60 + (i // 4) * 70
            pts = [(sx + k * 12, sy + 10 * math.sin(k * 1.7 + i)) for k in range(8)]
            _stroke(c, pts, 3, INK)


def table_round(g, x, y, w=900, sc=1.0):
    """โต๊ะประชุมรูปเกือกม้า (คณะมนตรีความมั่นคง)"""
    c = g.c
    with g.at(x, y, sc):
        c.new_path()
        c.arc(0, 0, w / 2, math.pi, 2 * math.pi)
        c.arc_negative(0, 0, w / 2 - 70, 2 * math.pi, math.pi)
        c.close_path()
        _shade(c, hexc("#c9a24a"), 5, 0.25)


def flags_row(g, x0, y, n=8, t=0.0, k=1.0, gap=110):
    """แถวเสาธงหลากสี (ประเทศสมาชิก — ธงสมมติ ไม่ใช่ธงจริง)"""
    c = g.c
    cols = [(RED, WHITE), (UN_BLUE, WHITE), (hexc("#3c8d4f"), hexc("#f2c94c")), (hexc("#f2c94c"), RED),
            (NAVY, RED), (WHITE, hexc("#3c8d4f")), (hexc("#e8892e"), WHITE), (hexc("#8a4a8a"), hexc("#f2c94c"))]
    for i in range(n):
        kk = max(0.0, min(1.0, k * n - i))
        if kk < 0.02:
            continue
        xx = x0 + i * gap
        g.line([(xx, y), (xx, y - 300 * kk)], 6, hexc("#8a8a8a"), amp=0)
        a, b = cols[i % len(cols)]
        top = y - 300 * kk
        wv = 6 * math.sin(t * 5 + i)
        c.new_path()
        for p in [(xx, top), (xx + 80, top + wv), (xx + 80, top + 50 + wv), (xx, top + 50)]:
            c.line_to(*p)
        c.close_path()
        _shade(c, a, 3, 0.1)
        c.new_path()
        for p in [(xx, top + 17), (xx + 80, top + 17 + wv), (xx + 80, top + 33 + wv), (xx, top + 33)]:
            c.line_to(*p)
        c.close_path()
        _shade(c, b, 0, 0)


def paper_tiger(g, x, y, sc=1.0, t=0.0):
    """เสือกระดาษ (พับกระดาษ)"""
    c = g.c
    with g.at(x, y, sc, 3 * math.sin(t * 2)):
        g.poly([(-180, 0), (-140, -140), (60, -150), (120, -60), (160, 0)], hexc("#f4ecd4"), 5, amp=0)
        g.poly([(80, -150), (130, -260), (230, -220), (220, -120), (120, -60)], hexc("#f4ecd4"), 5, amp=0)
        for k in range(4):
            g.line([(-120 + k * 50, -130), (-100 + k * 50, -40)], 6, hexc("#e8a33d"), amp=0)
        g.poly([(140, -250), (150, -300), (175, -255)], hexc("#f4ecd4"), 4, amp=0)
        g.circle(180, -200, 8, INK, 0)
        g.line([(-180, -60), (-260, -120)], 6, INK, amp=0)
        for k in range(4):
            g.line([(-160 + k * 90, 0), (-160 + k * 90, 40)], 8, INK, amp=0)


def red_button(g, x, y, sc=1.0, cover=0.0):
    """ปุ่มยิงสีแดง + ฝาครอบ (ปิดไว้ = ไม่กด)"""
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -130, -40, 260, 60, 12)
        _shade(c, hexc("#3a3a40"), 5, 0.2)
        c.new_path()
        c.arc(0, -40, 70, math.pi, 2 * math.pi)
        c.close_path()
        _shade(c, RED, 5, 0.3)
        if cover > 0:
            with g.at(-110, -40, 1, -80 * (1 - cover)):
                c.new_path()
                c.arc(110, 0, 100, math.pi, 2 * math.pi)
                c.close_path()
                c.set_source_rgba(0.8, 0.9, 1.0, 0.5)
                c.fill_preserve()
                c.set_source_rgba(*INK[:3], 1)
                c.set_line_width(5)
                c.stroke()


def aid_box(g, x, y, sc=1.0, rot=0.0, label="AID"):
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -90, -150, 180, 150, 8)
        _shade(c, hexc("#d9b26a"), 5, 0.25)
        _stroke(c, [(-90, -110), (90, -110)], 6, hexc("#a8834f"), smooth=False)
        g.text(label, 0, -60, 46, "kanit", UN_BLUE)


def syringe(g, x, y, sc=1.0, rot=0.0):
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -30, -160, 60, 200, 10)
        _shade(c, hexc("#eaf4fb"), 5, 0.1)
        _rr(c, -26, -60, 52, 96, 6)
        _shade(c, hexc("#8fd0a8"), 0, 0)
        g.line([(0, 40), (0, 120)], 5, GREY, amp=0)
        _rr(c, -50, -180, 100, 24, 6)
        _shade(c, GREY, 4, 0.2)


def scales(g, x, y, sc=1.0, t=0.0):
    """ตาชั่งความยุติธรรม (สิทธิมนุษยชน)"""
    c = g.c
    tilt = 8 * math.sin(t * 1.5)
    with g.at(x, y, sc):
        g.line([(0, 0), (0, -300)], 10, GOLD2, amp=0)
        with g.at(0, -300, 1, tilt):
            g.line([(-160, 0), (160, 0)], 8, GOLD2, amp=0)
            for sx in (-1, 1):
                g.line([(sx * 160, 0), (sx * 160 - 50, 110)], 3, INK, amp=0)
                g.line([(sx * 160, 0), (sx * 160 + 50, 110)], 3, INK, amp=0)
                c.new_path()
                c.arc(sx * 160, 110, 70, 0, math.pi)
                c.close_path()
                _shade(c, GOLD, 4, 0.2)
        _rr(c, -80, -10, 160, 24, 8)
        _shade(c, GOLD, 4, 0.2)


def dove(g, x, y, sc=1.0, t=0.0):
    c = g.c
    fl = abs(math.sin(t * 8))
    with g.at(x, y, sc):
        _smooth_path(c, [(-70, 0), (-20, -30), (50, -24), (90, -40), (80, -10), (40, 20), (-40, 20)])
        _shade(c, WHITE, 5, 0.15)
        _smooth_path(c, [(-10, -20), (-40, -90 * (0.4 + 0.6 * fl)), (30, -70 * (0.4 + 0.6 * fl)), (30, -20)])
        _shade(c, WHITE, 5, 0.2)
        g.circle(70, -30, 5, INK, 0)
        g.line([(95, -34), (140, -20)], 5, OLIVE, amp=0)
        for i in range(3):
            g.circle(108 + i * 14, -32 + i * 4, 7, OLIVE, 2)
