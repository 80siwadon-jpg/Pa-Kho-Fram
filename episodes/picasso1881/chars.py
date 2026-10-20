"""ตัวละครและพร็อพ: ปาโบล ปิกัสโซ (เกิด 25 ต.ค. 1881) — ภาพคิวบิสม์วาดเองแบบการ์ตูน ไม่ลอกภาพจริง
เกอร์นิกา: วาดเป็นผืนผ้าใบขาวดำโทนเทา รูปทรงเหลี่ยม ๆ (วัว ม้า หลอดไฟ) แบบสื่อความ ไม่แสดงความรุนแรง"""
import importlib.util
import math
import os

from gfx import GOLD, GOLD2, GREY, INK, NAVY, RED, WHITE, hexc
from people import Look, _rr, _shade, _smooth_path, _stroke

_spec = importlib.util.spec_from_file_location(
    "leeu_chars", os.path.join(os.path.dirname(__file__), "..", "leeuwenhoek1632", "chars.py"))
_lv = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_lv)
cradle = _lv.cradle

SKIN_ES = hexc("#e2b28c")
CANVAS = hexc("#f4eedf")
WOOD = hexc("#a8784a")
PAL = [hexc("#e05a4a"), hexc("#3d6fa8"), hexc("#f2c25c"), hexc("#4f8a52"), hexc("#7a4a9a"), hexc("#e8892e")]

# ปิกัสโซวัยชรา (ภาพจำ): ศีรษะล้าน ตาดำโต คิ้วเข้ม เสื้อลายขวางทหารเรือ
PICASSO = Look(hair="bald", hair_col=hexc("#d9d5cc"), outfit="stripe", suit=WHITE, pants=hexc("#5a4a3a"),
               skin=SKIN_ES, w=58, jaw=0.55, nose=1.05, brow=1.4, age=0.6, build=1.05, height=0.95)
# ปิกัสโซวัยหนุ่ม (ยุคคิวบิสม์ ~1907): ผมดำปรกหน้าผาก
YOUNG = Look(hair="part", hair_col=hexc("#1b1714"), outfit="vest", suit=hexc("#3a3a40"), shirt=WHITE,
             tie=hexc("#2b2622"), skin=SKIN_ES, w=56, jaw=0.5, brow=1.3, age=0.15)
TEEN = Look(hair="part", hair_col=hexc("#1b1714"), outfit="vest", suit=hexc("#5a4a3a"), shirt=WHITE,
            tie=hexc("#7a2e2e"), skin=SKIN_ES, w=55, brow=1.2, age=0.0, height=0.85, headsc=1.15)
# ลุงซัลวาดอร์ หมอสูบซิการ์ (หนวดใหญ่)
UNCLE = Look(hair="part", hair_col=hexc("#3a2a1e"), outfit="vest", suit=hexc("#2b2622"), shirt=WHITE,
             tie=hexc("#2b2622"), facial="mustache", skin=SKIN_ES, w=58, jaw=0.55, age=0.45)
MIDWIFE = Look(hair="bun", hair_col=hexc("#3a2a1e"), outfit="dress", suit=hexc("#e8e0cc"), skin=SKIN_ES, w=54,
               age=0.5, height=0.93)
CRITICS = [
    Look(hair="part", hair_col=hexc("#9a948a"), suit=hexc("#2b2622"), tie=hexc("#7a2e2e"), facial="beard", w=57,
         age=0.75, hat="tophat"),
    Look(hair="slick", hair_col=hexc("#3a2a1e"), suit=hexc("#3a3f48"), tie=hexc("#2b2622"), facial="mustache",
         w=56, age=0.5, glasses="round"),
    Look(hair="bun", hair_col=hexc("#5a4a3a"), outfit="dress", suit=hexc("#6a3a4a"), w=54, age=0.5, height=0.93,
         hat="bowler"),
]


def cigar(g, x, y, sc=1.0, rot=0.0, t=0.0, smoke=1.0):
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -70, -10, 140, 20, 9)
        _shade(c, hexc("#7a4a2a"), 4, 0.3)
        _rr(c, 40, -10, 14, 20, 2)
        _shade(c, hexc("#d9a441"), 2, 0)
        g.circle(72, 0, 8, hexc("#f08a3a"), 0)
    if smoke > 0:
        smoke_puffs(g, x + 80 * sc, y - 20 * sc, t, smoke, sc)


def smoke_puffs(g, x, y, t, k=1.0, sc=1.0, dx=1.0):
    for i in range(5):
        u = (t * 0.5 + i / 5) % 1
        g.circle(x + dx * 140 * u * sc + 20 * math.sin(t * 2 + i), y - 160 * u * sc, (14 + 34 * u) * sc,
                 (0.75, 0.75, 0.78, k * 0.7 * (1 - u)), 0)


def easel(g, x, y, sc=1.0, art="cubist", t=0.0, k=1.0):
    """ขาตั้งวาดภาพ + ผ้าใบ (art: blank / realist / cubist / child)"""
    c = g.c
    with g.at(x, y, sc):
        for a, b in (((-150, 0), (-60, -720)), ((150, 0), (60, -720)), ((0, 0), (0, -760))):
            _stroke(c, [a, b], 18, INK, smooth=False)
            _stroke(c, [a, b], 11, WOOD, smooth=False)
        _rr(c, -230, -330, 460, 26, 6)
        _shade(c, WOOD, 5, 0.2)
        _rr(c, -210, -720, 420, 400, 6)
        _shade(c, CANVAS, 7, 0.1)
        if art != "blank":
            painting(g, 0, -520, 1.0, art, t, k)


def painting(g, x, y, sc=1.0, art="cubist", t=0.0, k=1.0):
    """ภาพบนผ้าใบขนาด 400×380 ศูนย์กลาง (x, y)"""
    c = g.c
    with g.at(x, y, sc):
        c.save()
        c.rectangle(-200, -190, 400, 380)
        c.clip()
        if art == "realist":   # ภาพเหมือนจริงคลาสสิก: หน้าคนรูปไข่ แรเงานุ่ม
            c.set_source_rgb(0.42, 0.35, 0.28)
            c.paint()
            c.save()
            c.scale(1, 1.3)
            c.new_path()
            c.arc(0, -20, 90 * k, 0, 2 * math.pi)
            c.restore()
            _shade(c, hexc("#e8c09a"), 3, 0.35)
            _smooth_path(c, [(-110, 190), (-90, 90), (0, 70), (90, 90), (110, 190)])
            _shade(c, hexc("#3a2a1e"), 3, 0.2)
            for ex in (-32, 32):
                g.circle(ex, -40, 8, INK, 0)
            _stroke(c, [(0, -30), (-8, 10), (6, 14)], 4, hexc("#8a5a3a"))
            _stroke(c, [(-24, 50), (0, 58), (24, 50)], 5, hexc("#a8463a"))
        elif art == "child":   # ภาพแบบเด็ก ๆ: หน้ายิ้ม พระอาทิตย์ บ้าน
            c.set_source_rgb(1, 1, 1)
            c.paint()
            g.circle(130, -120, 40, GOLD2, 5)
            g.circle(-40, 20, 90, hexc("#f2c9a8"), 6)
            for ex in (-70, -10):
                g.circle(ex, 0, 10, INK, 0)
            g.arc(-40, 30, 40, 20, 160, 6, INK)
            g.line([(-40, 110), (-40, 180)], 6, INK, amp=0)
        else:   # คิวบิสม์: หน้าแตกเป็นเหลี่ยม ตาสองข้างคนละมุม จมูกด้านข้าง
            c.set_source_rgb(0.95, 0.93, 0.87)
            c.paint()
            shards = [[(-200, -190), (20, -190), (-60, 20), (-200, 60)],
                      [(20, -190), (200, -190), (200, 40), (-60, 20)],
                      [(-200, 60), (-60, 20), (0, 190), (-200, 190)],
                      [(-60, 20), (200, 40), (200, 190), (0, 190)]]
            for i, sh in enumerate(shards):
                c.new_path()
                for p in sh:
                    c.line_to(*p)
                c.close_path()
                col = [hexc("#6a8ab8"), hexc("#e8b07a"), hexc("#c86a4a"), hexc("#8aa86a")][i]
                c.set_source_rgba(*col[:3], 0.55 * k + 0.2)
                c.fill()
            wob = 4 * math.sin(t * 2)
            _smooth_path(c, [(-110, -140), (60, -150), (110, -20), (70, 120), (-40, 140), (-120, 40)])
            _shade(c, hexc("#f2c9a8"), 6, 0.0)
            c.new_path()   # ครึ่งหน้าด้านข้างสีเข้ม
            for p in [(0, -148), (60, -150), (110, -20), (70, 120), (10, 130)]:
                c.line_to(*p)
            c.close_path()
            c.set_source_rgba(0.85, 0.55, 0.4, 0.8)
            c.fill()
            # ตามองตรง (รูปอัลมอนด์) + ตามองข้าง (สามเหลี่ยม) คนละระดับ
            _smooth_path(c, [(-80, -70 + wob), (-50, -90 + wob), (-20, -70 + wob), (-50, -55 + wob)])
            _shade(c, WHITE, 4, 0)
            g.circle(-50, -72 + wob, 9, INK, 0)
            c.new_path()
            for p in [(40, -40 - wob), (85, -55 - wob), (70, -25 - wob)]:
                c.line_to(*p)
            c.close_path()
            _shade(c, WHITE, 4, 0)
            g.circle(68, -40 - wob, 7, INK, 0)
            c.new_path()   # จมูกด้านข้าง
            for p in [(0, -50), (-40, 30), (5, 30)]:
                c.line_to(*p)
            c.close_path()
            _shade(c, hexc("#e8a07a"), 4, 0)
            _smooth_path(c, [(-50, 70), (0, 60), (30, 80), (-10, 95)])   # ปากเบี้ยว
            _shade(c, hexc("#c84a4a"), 4, 0)
            for i in range(3):   # เส้นเหลี่ยมแบ่งระนาบ
                _stroke(c, [(-200 + 150 * i, -190), (-100 + 120 * i, 190)], 3, INK, 0.35, smooth=False)
        c.restore()
        c.new_path()
        c.rectangle(-200, -190, 400, 380)
        c.set_source_rgba(*INK[:3], 1)
        c.set_line_width(6)
        c.stroke()


def frame(g, x, y, sc=1.0, art="cubist", t=0.0, rot=0.0):
    """กรอบรูปทองแขวนผนัง"""
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -240, -230, 480, 460, 8)
        _shade(c, GOLD, 7, 0.3)
        painting(g, 0, 0, 1.0, art, t)


def guernica(g, x, y, sc=1.0, t=0.0, k=1.0):
    """ผ้าใบขนาดยักษ์โทนขาวดำ-เทา: รูปทรงเหลี่ยม (หัววัว หัวม้า หลอดไฟรูปดวงตา) — สื่อความ ไม่ลอกภาพจริง"""
    c = g.c
    with g.at(x, y, sc):
        c.save()
        c.rectangle(-500, -230, 1000, 460)
        c.clip()
        c.set_source_rgb(0.86, 0.86, 0.86)
        c.paint()
        tris = [[(-500, -230), (-200, -230), (-380, 230)], [(-200, -230), (100, -230), (-80, 100)],
                [(100, -230), (500, -230), (300, 230)], [(-380, 230), (-80, 100), (60, 230)],
                [(-80, 100), (300, 230), (60, 230)]]
        for i, tr in enumerate(tris):
            c.new_path()
            for p in tr:
                c.line_to(*p)
            c.close_path()
            v = [0.25, 0.55, 0.4, 0.7, 0.32][i]
            c.set_source_rgba(v, v, v, 0.85)
            c.fill()
        # หลอดไฟรูปดวงตาด้านบน
        _smooth_path(c, [(-120, -170), (0, -210), (120, -170), (0, -140)])
        _shade(c, hexc("#f0f0f0"), 5, 0)
        c.new_path()
        c.arc(0, -175, 22 + 4 * math.sin(t * 6), 0, 2 * math.pi)
        c.set_source_rgb(0.95, 0.95, 0.75)
        c.fill()
        for i in range(10):
            a = math.pi + i * math.pi / 9
            _stroke(c, [(70 * math.cos(a), -175 + 50 * math.sin(a)), (100 * math.cos(a), -175 + 70 * math.sin(a))],
                    4, INK, smooth=False)
        # หัววัว (ซ้าย) — เหลี่ยม เขาโค้ง
        c.new_path()
        for p in [(-420, -120), (-300, -150), (-260, -40), (-340, 30), (-430, -10)]:
            c.line_to(*p)
        c.close_path()
        _shade(c, hexc("#f2f2f2"), 5, 0)
        _stroke(c, [(-410, -125), (-450, -200), (-400, -190)], 7, INK)
        _stroke(c, [(-310, -150), (-280, -215), (-250, -190)], 7, INK)
        g.circle(-360, -80, 10, INK, 0)
        g.circle(-310, -60, 6, INK, 0)
        # หัวม้า (กลาง) — ร้องเงยหน้า ปากสามเหลี่ยม
        c.new_path()
        for p in [(-40, 0), (60, -80), (140, -30), (110, 40), (20, 60)]:
            c.line_to(*p)
        c.close_path()
        _shade(c, hexc("#e8e8e8"), 5, 0)
        c.new_path()
        for p in [(110, -40), (170, -70), (140, 0)]:
            c.line_to(*p)
        c.close_path()
        _shade(c, hexc("#555555"), 4, 0)
        g.circle(70, -40, 8, INK, 0)
        # ตะเกียงยื่นจากหน้าต่าง (ขวา)
        _stroke(c, [(420, -120), (260, -60)], 10, hexc("#f0f0f0"))
        g.circle(250, -55, 24, hexc("#f5f0d0"), 4)
        # เส้นสั้น ๆ แบบลายหนังสือพิมพ์
        for i in range(12):
            _stroke(c, [(-60 + 10 * i, 80), (-60 + 10 * i, 110)], 2, INK, 0.5, smooth=False)
        c.restore()
        c.new_path()
        c.rectangle(-500, -230, 1000, 460)
        c.set_source_rgba(*INK[:3], 1)
        c.set_line_width(8)
        c.stroke()
        if k < 1:   # ผ้าใบคลี่ออกจากกลาง
            c.rectangle(-500, -230, 1000 * (1 - k) / 2, 460)
            c.rectangle(500 - 1000 * (1 - k) / 2, -230, 1000 * (1 - k) / 2, 460)
            c.set_source_rgb(1, 1, 1)
            c.fill()


def palette(g, x, y, sc=1.0, rot=0.0):
    c = g.c
    with g.at(x, y, sc, rot):
        _smooth_path(c, [(-150, -60), (-40, -110), (120, -90), (160, 0), (110, 90), (-60, 100), (-160, 40)])
        _shade(c, hexc("#d8b07a"), 6, 0.2)
        c.new_path()
        c.arc(-90, 30, 26, 0, 2 * math.pi)
        c.set_source_rgb(1, 1, 1)
        c.fill()
        for i, (px, py) in enumerate(((-60, -60), (10, -70), (80, -50), (110, 20), (50, 60), (-20, 60))):
            g.circle(px, py, 20, PAL[i], 3)


def brush(g, x, y, sc=1.0, rot=0.0, col=RED):
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -8, -160, 16, 160, 6)
        _shade(c, WOOD, 4, 0.2)
        _rr(c, -10, -10, 20, 30, 3)
        _shade(c, hexc("#bbbbbb"), 3, 0)
        _smooth_path(c, [(-10, 20), (10, 20), (6, 60), (0, 70), (-6, 60)])
        _shade(c, col, 3, 0)


def hammer(g, x, y, sc=1.0, rot=0.0):
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -12, -40, 24, 240, 8)
        _shade(c, WOOD, 5, 0.25)
        _rr(c, -90, -100, 180, 70, 10)
        _shade(c, hexc("#7a7f88"), 6, 0.3)


def mirror(g, x, y, sc=1.0, crack=0.0):
    c = g.c
    with g.at(x, y, sc):
        c.save()
        c.scale(1, 1.3)
        c.new_path()
        c.arc(0, 0, 140, 0, 2 * math.pi)
        c.restore()
        _shade(c, hexc("#cfe3ef"), 10, 0.25)
        _stroke(c, [(-60, -100), (-20, -140)], 6, WHITE, 0.8)
        if crack > 0:
            for a in range(6):
                ang = a * 1.05 + 0.3
                _stroke(c, [(0, 0), (130 * crack * math.cos(ang), 170 * crack * math.sin(ang))], 4, INK)


def school(g, x, y, sc=1.0):
    """อาคารโรงเรียนศิลปะ"""
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -260, -360, 520, 360, 6)
        _shade(c, hexc("#e8dcc0"), 6, 0.2)
        c.new_path()
        for p in [(-290, -360), (0, -480), (290, -360)]:
            c.line_to(*p)
        c.close_path()
        _shade(c, hexc("#b8644a"), 6, 0.2)
        for k in range(3):
            _rr(c, -200 + k * 150, -300, 100, 140, 40)
            _shade(c, hexc("#9ab8d0"), 4, 0.1)
        _rr(c, -50, -130, 100, 130, 40)
        _shade(c, hexc("#6e4528"), 4, 0.1)
        palette(g, 0, -420, 0.35)
