"""ตัวละครและพร็อพ: เดินขบวนสู่เพนตากอน 21 ต.ค. 1967 — คนแบบกึ่งเสมือนจริงจาก src/people.py
ภาพข่าวต้นฉบับ (Bernie Boston "Flower Power", Marc Riboud) มีลิขสิทธิ์ -> วาดฉากนั้นเป็นการ์ตูน"""
import math

from gfx import GOLD, GOLD2, GREY, INK, LGREY, NAVY, RED, WHITE, hexc, hn, lerp
from people import Look, _rr, _shade, _smooth_path, _stroke

OLIVE = hexc("#5d6b3f")
OLIVE2 = hexc("#4f5a3a")
PINK = hexc("#f28cb1")
PINK2 = hexc("#d9608c")
MUM = hexc("#f6d24a")
STEM = hexc("#4f8a3a")
PENT = hexc("#c9cdd3")

# จอร์จ แฮร์ริส (18): ผมน้ำตาลยาวระต้นคอ เสื้อสเวตเตอร์คอเต่าสีเข้ม — ภาพ "Flower Power"
GEORGE = Look(hair="full", hair_col=hexc("#6b4a33"), suit=hexc("#2f3a4a"), outfit="tee", pants=hexc("#4a4a52"),
              w=56, jaw=0.3, nose=1.0, age=0.05, build=0.9)
# แจน โรส แคสเมียร์ (17): ผมยาวสีน้ำตาลอ่อน เสื้อโค้ตสีครีม ถือดอกเบญจมาศ
JAN = Look(hair="long", hair_col=hexc("#9a6a3a"), suit=hexc("#e9e0cf"), outfit="dress", w=52, jaw=0.2, nose=0.9,
           age=0.0, height=0.92, shoes=hexc("#5a3a22"))
# สารวัตรทหาร: ชุดสนามสีเขียวขี้ม้า หมวกเหล็ก MP
SOLDIERS = [
    Look(hair="buzz", hair_col=hexc("#6b4a33"), suit=OLIVE, outfit="fatigue", pants=OLIVE2, hat="helmet", w=56,
         age=0.05, jaw=0.5),
    Look(hair="buzz", hair_col=hexc("#2b2622"), suit=OLIVE, outfit="fatigue", pants=OLIVE2, hat="helmet", w=56,
         age=0.1, jaw=0.4, skin=hexc("#d9a37e")),
    Look(hair="buzz", hair_col=hexc("#a8763e"), suit=OLIVE, outfit="fatigue", pants=OLIVE2, hat="helmet", w=56,
         age=0.05, jaw=0.6),
    Look(hair="buzz", hair_col=hexc("#2b2622"), suit=OLIVE, outfit="fatigue", pants=OLIVE2, hat="helmet", w=56,
         age=0.1, jaw=0.5, skin=hexc("#8a5a3c")),
]
# ผู้ชุมนุมยุค 60s
PROTESTERS = [
    Look(hair="long", hair_col=hexc("#3a2c22"), suit=hexc("#c8553d"), outfit="tee", pants=hexc("#3f6496"),
         hat="headband", hat_trim=hexc("#e3a92b"), w=56, age=0.05),
    Look(hair="full", hair_col=hexc("#a8763e"), suit=hexc("#e3a92b"), outfit="flannel", pants=hexc("#3f6496"),
         facial="mustache", w=57, age=0.15),
    Look(hair="long", hair_col=hexc("#2b2622"), suit=hexc("#6b8f3a"), outfit="dress", w=52, age=0.0, height=0.93),
    Look(hair="afro", hair_col=hexc("#1c1714"), skin=hexc("#7b4a30"), suit=hexc("#8a6a9a"), outfit="tee",
         pants=hexc("#2b2b30"), glasses="thin", w=56, age=0.1),
    Look(hair="part", hair_col=hexc("#6b4a33"), suit=hexc("#3a3a42"), tie=hexc("#7a2e2e"), glasses="thick",
         w=58, age=0.4),
]


# ---------------------------------------------------------------- พร็อพ
def pentagon_top(g, x, y, r, t=0.0, k=1.0):
    """เพนตากอนมองจากด้านบน: ห้าเหลี่ยมซ้อน 5 วง + ลานกลาง"""
    c = g.c
    with g.at(x, y, k, 0.4 * math.sin(t * 0.3)):
        for i, rr in enumerate((1.0, 0.82, 0.64, 0.46)):
            c.new_path()
            for j in range(5):
                a = math.radians(-90 + j * 72)
                c.line_to(math.cos(a) * r * rr, math.sin(a) * r * rr)
            c.close_path()
            _shade(c, PENT if i % 2 == 0 else hexc("#aeb3bb"), 6, 0.2)
        c.new_path()
        for j in range(5):
            a = math.radians(-90 + j * 72)
            c.line_to(math.cos(a) * r * 0.3, math.sin(a) * r * 0.3)
        c.close_path()
        _shade(c, hexc("#8fbf6a"), 5, 0.1)


def pentagon_wall(g, y, t=0.0):
    """ผนังด้านหน้าเพนตากอน (เสาและหน้าต่าง) เป็นฉากหลัง — y = แนวพื้น"""
    c = g.c
    _rr(c, -400, y - 520, 1880, 520, 0)
    _shade(c, PENT, 6, 0.1, horiz=False)
    for r in range(4):
        for q in range(-3, 22):
            _rr(c, q * 70 + 10, y - 480 + r * 100, 34, 60, 2)
            _shade(c, hexc("#7b8794"), 2, 0)
    _rr(c, -400, y - 540, 1880, 30, 0)
    _shade(c, hexc("#b0b5bd"), 5, 0)


def rifle(g, x, y, sc=1.0, rot=0.0, flower=0.0, bayonet=True, t=0.0, mum=False):
    """ปืนไรเฟิล M14 + ดาบปลายปืน — x,y = ด้ามจับ, rot องศา (0 = ชี้ขวา); flower 0..1 ดอกไม้ในลำกล้อง"""
    c = g.c
    with g.at(x, y, sc, rot):
        _smooth_path(c, [(-150, -6), (-40, -14), (-30, 20), (-120, 34), (-160, 26)])   # พานท้าย
        _shade(c, hexc("#7a5230"), 5, 0.2)
        _rr(c, -40, -16, 260, 26, 6)   # ตัวปืน
        _shade(c, hexc("#7a5230"), 5, 0.2)
        _rr(c, 0, -26, 300, 14, 4)   # ลำกล้อง
        _shade(c, hexc("#3a3a40"), 4, 0.1)
        _rr(c, 40, 8, 40, 34, 6)   # ซองกระสุน
        _shade(c, hexc("#3a3a40"), 4, 0.1)
        if bayonet:
            c.new_path()
            for px, py in [(296, -24), (390, -19), (296, -14)]:
                c.line_to(px, py)
            c.close_path()
            _shade(c, hexc("#d9dde3"), 3, 0.1)
        if flower > 0:   # ก้านดอกไม้เสียบในปากลำกล้อง
            with g.at(300, -19, flower):
                _stroke(c, [(0, 0), (40, -30), (70, -70)], 6, STEM)
                carnation(g, 74, -78, 0.6, t=t) if not mum else chrysanthemum(g, 74, -78, 0.6, t=t)


def carnation(g, x, y, s=1.0, t=0.0, col=PINK):
    c = g.c
    with g.at(x, y, s, 6 * math.sin(t * 2 + x * 0.01)):
        for i in range(9):
            a = i * 2 * math.pi / 9
            _smooth_path(c, [(0, 0), (math.cos(a - 0.35) * 46, math.sin(a - 0.35) * 46),
                             (math.cos(a) * 54, math.sin(a) * 54), (math.cos(a + 0.35) * 46, math.sin(a + 0.35) * 46)])
            _shade(c, col, 3.5, 0.15)
        c.new_path()
        c.arc(0, 0, 22, 0, 2 * math.pi)
        _shade(c, PINK2, 3, 0.1)


def chrysanthemum(g, x, y, s=1.0, t=0.0):
    c = g.c
    with g.at(x, y, s, 5 * math.sin(t * 1.7 + x * 0.01)):
        for i in range(16):
            a = i * 2 * math.pi / 16
            with g.at(math.cos(a) * 26, math.sin(a) * 26, 1, math.degrees(a)):
                _rr(c, -4, -9, 40, 18, 9)
                _shade(c, MUM, 3, 0.15)
        c.new_path()
        c.arc(0, 0, 24, 0, 2 * math.pi)
        _shade(c, hexc("#e3a92b"), 3, 0.2)


def bouquet(g, x, y, s=1.0, t=0.0, n=5):
    with g.at(x, y, s):
        for i in range(n):
            a = -0.6 + 1.2 * i / max(n - 1, 1)
            _stroke(g.c, [(0, 0), (math.sin(a) * 90, -150)], 6, STEM)
        for i in range(n):
            a = -0.6 + 1.2 * i / max(n - 1, 1)
            carnation(g, math.sin(a) * 90, -160 - 10 * (i % 2), 0.55, t=t + i)


def peace_sign(g, x, y, r, col=INK, lw=14, k=1.0):
    if k <= 0:
        return
    with g.at(x, y, k):
        g.circle(0, 0, r, (1, 1, 1, 1), lw, stroke=col)
        g.line([(0, -r), (0, r)], lw, col, amp=0)
        g.line([(0, 0), (-r * 0.7, r * 0.7)], lw, col, amp=0)
        g.line([(0, 0), (r * 0.7, r * 0.7)], lw, col, amp=0)


def sign(g, x, y, text, sc=1.0, rot=0.0, col=WHITE):
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -10, 0, 20, 300, 4)
        _shade(c, hexc("#a8763e"), 4, 0.2)
        _rr(c, -170, -130, 340, 140, 8)
        _shade(c, col, 5, 0.1)
        g.text(text, 0, -60, 40, "kanit", INK, maxw=310)


def flag_us(g, x, y, w, h, t=0.0):
    c = g.c
    with g.at(x, y):
        for i in range(7):
            _rr(c, -w / 2, -h / 2 + i * h / 7 * 1.0, w, h / 14, 0)
            _shade(c, RED, 0, 0)
        _rr(c, -w / 2, -h / 2, w * 0.42, h * 0.54, 0)
        _shade(c, NAVY, 0, 0)
        for r in range(3):
            for q in range(4):
                g.sparkle(-w / 2 + 24 + q * w * 0.1, -h / 2 + 22 + r * h * 0.16, 7, WHITE, 0)
        c.rectangle(-w / 2, -h / 2, w, h)
        c.set_source_rgba(*INK)
        c.set_line_width(4)
        c.stroke()


def coffin(g, x, y, sc=1.0):
    """โลงศพคลุมธงชาติ (มองด้านข้าง) — x,y = กึ่งกลางฐาน"""
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -200, -90, 400, 90, 10)
        _shade(c, hexc("#7a5230"), 6, 0.25)
        flag_us(g, 0, -122, 420, 70)
        for sx in (-1, 1):   # ชายธงห้อยด้านข้าง
            _rr(c, sx * 210 - 8, -122, 16, 50, 3)
            _shade(c, RED, 3, 0)


def camera_flash(g, x, y, sc=1.0, flash=0.0):
    """กล้องถ่ายรูปยุค 60s (ใช้ฟิล์ม) + แฟลช"""
    c = g.c
    with g.at(x, y, sc):
        if flash > 0:
            g.sunburst(0, -40, 120, 300 + 200 * flash, 16, 0, 12, (1, 0.95, 0.7, flash))
        _rr(c, -130, -80, 260, 160, 18)
        _shade(c, hexc("#2b2b30"), 6, 0.2)
        _rr(c, -130, -80, 260, 40, 10)
        _shade(c, hexc("#c9cdd3"), 5, 0.1)
        c.new_path()
        c.arc(0, 10, 60, 0, 2 * math.pi)
        _shade(c, hexc("#4a4a52"), 6, 0.1)
        c.new_path()
        c.arc(0, 10, 34, 0, 2 * math.pi)
        _shade(c, hexc("#8fb8de"), 4, 0.1)
        _rr(c, 60, -112, 50, 30, 4)
        _shade(c, WHITE if flash > 0 else LGREY, 4, 0)


def lincoln_memorial(g, x, y, sc=1.0):
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -360, -60, 720, 60, 4)
        _shade(c, hexc("#ece6d8"), 6, 0.15)
        for i in range(9):
            _rr(c, -320 + i * 80, -300, 34, 240, 4)
            _shade(c, hexc("#f4efe2"), 5, 0.2)
        _rr(c, -370, -360, 740, 64, 4)
        _shade(c, hexc("#ece6d8"), 6, 0.15)
        _rr(c, -300, -400, 600, 40, 4)
        _shade(c, hexc("#e3dccb"), 5, 0.1)


def crowd_mass(g, x0, x1, y, t, rows=4, seed=2, k=1.0):
    """ฝูงชนหนาแน่น (หัว+ไหล่ หลายแถว) + ป้าย"""
    cols = [hexc("#c8553d"), hexc("#3f6496"), hexc("#e3a92b"), hexc("#6b8f3a"), hexc("#8a6a9a"), hexc("#3a3a42")]
    skins = [hexc("#efc4a1"), hexc("#d9a37e"), hexc("#8a5a3c"), hexc("#f2d0b5")]
    hairs = [hexc("#2b2622"), hexc("#6b4a33"), hexc("#a8763e"), hexc("#1c1714")]
    n = int((x1 - x0) / 52)
    for r in range(rows):
        for i in range(int(n * k)):
            px = x0 + i * 52 + (r % 2) * 26 + 8 * math.sin(t * 2 + i + r)
            py = y - r * 46 + 4 * math.sin(t * 3 + i * 1.3)
            j = int(hn(i * 7 + r, seed) * 100)
            g.c.new_path()
            _rr(g.c, px - 24, py - 20, 48, 60, 18)
            _shade(g.c, cols[j % 6], 3, 0.2)
            g.circle(px, py - 36, 19, skins[j % 4], 3)
            g.c.new_path()
            g.c.arc(px, py - 42, 19, math.pi, 2 * math.pi)
            _shade(g.c, hairs[(j // 3) % 4], 0, 0)
