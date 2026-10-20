"""ตัวละครและพร็อพ: การบุกของกองพลทหารม้าเบา ยุทธการบาลาคลาวา 25 ต.ค. 1854 (สงครามไครเมีย)
ไม่แสดงความรุนแรงตรง ๆ: ใช้ควันปืน แสงวาบ ม้าไร้คนขี่ หมวกตกพื้น เงาทหาร แทนภาพการบาดเจ็บ/เสียชีวิต"""
import importlib.util
import math
import os

from gfx import GOLD, GOLD2, GREY, INK, NAVY, RED, WHITE, hexc
from people import Look, _rr, _shade, _smooth_path, _stroke

_spec = importlib.util.spec_from_file_location(
    "alamein_chars", os.path.join(os.path.dirname(__file__), "..", "alamein1942", "chars.py"))
_al = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_al)
blast, smoke, artillery_al = _al.blast, _al.smoke, _al.artillery

GRASS = hexc("#cfd9a0")
HILL = hexc("#b9b98a")
HORSE = hexc("#8a5a36")
HORSE2 = hexc("#6e4528")
HUSSAR = hexc("#1f2b4a")     # เสื้อน้ำเงินเข้มทหารม้าฮุสซาร์
CHERRY = hexc("#a0283a")     # กางเกงแดงเชอร์รีของกรมทหารม้าฮุสซาร์ที่ 11 (ของคาร์ดิแกน)
RU_GREEN = hexc("#3f5a3a")
FIRE = hexc("#f2a93b")

# ลอร์ดแร็กแลน ผู้บัญชาการสูงสุด: ผมขาว แขนขวาด้วน (เสียแขนที่วอเตอร์ลู) หมวกสองแฉก เสื้อโค้ตน้ำเงิน
RAGLAN = Look(hair="nelson", hair_col=hexc("#e0dcd2"), suit=hexc("#1f2b4a"), pants=hexc("#2b2f3a"),
              shoes=hexc("#1b1916"), outfit="naval", hat="bicorne", hat_trim=GOLD, epaulettes=True, empty_arm=-1,
              w=55, jaw=0.35, nose=1.15, brow=0.7, age=0.85, build=0.9)
# ลอร์ดลูคัน ผู้บัญชาการกองพลทหารม้า: หนวดหนา ผมเทา หมวกสองแฉก
LUCAN = Look(hair="short", hair_col=hexc("#8a847a"), suit=hexc("#2b3f2f"), pants=hexc("#2b2f3a"),
             shoes=hexc("#1b1916"), outfit="naval", hat="bicorne", epaulettes=True, facial="mustache",
             w=56, jaw=0.5, nose=1.1, age=0.7)
# ลอร์ดคาร์ดิแกน ผู้นำกองพลทหารม้าเบา: หนวดและจอนยาว หมวกขนฮุสซาร์ เสื้อน้ำเงิน กางเกงเชอร์รี
CARDIGAN = Look(hair="short", hair_col=hexc("#c9b38a"), suit=HUSSAR, shirt=hexc("#2b3a6a"), collar=GOLD, pants=CHERRY,
                shoes=hexc("#1b1916"), outfit="naval", hat="busby", epaulettes=True, facial="beard", w=56,
                jaw=0.4, nose=1.15, age=0.6)
# นายพลบอสเกต์ นักสังเกตการณ์ชาวฝรั่งเศส: หมวกเคปิ หนวดเครา
BOSQUET = Look(hair="short", hair_col=hexc("#2b2622"), suit=hexc("#2b2f5a"), collar=hexc("#b8283a"),
               pants=hexc("#b8283a"), shoes=hexc("#1b1916"), outfit="naval", hat="kepi", epaulettes=True,
               facial="goatee", w=57, jaw=0.55, age=0.45)
TROOPERS = [   # พลทหารม้าเบา (หน้าหนุ่ม)
    Look(hair="short", hair_col=hexc("#6b4a33"), suit=HUSSAR, shirt=hexc("#2b3a6a"), collar=GOLD, pants=CHERRY, shoes=hexc("#1b1916"),
         outfit="naval", hat="busby", w=55, age=0.1, facial="mustache"),
    Look(hair="short", hair_col=hexc("#2b2622"), suit=HUSSAR, shirt=hexc("#2b3a6a"), collar=GOLD, pants=hexc("#2b2f3a"),
         shoes=hexc("#1b1916"), outfit="naval", hat="busby", hat_trim=hexc("#e8c45a"), w=55, age=0.05),
    Look(hair="short", hair_col=hexc("#a8784a"), suit=hexc("#2b3a5a"), collar=hexc("#e8e0cc"),
         pants=hexc("#2b2f3a"), shoes=hexc("#1b1916"), outfit="naval", hat="busby", w=55, age=0.1),
]


def horse(g, x, y, sc=1.0, t=0.0, gallop=1.0, rider=None, sabre=1.0, flip=False, col=HORSE, seed=0):
    """ม้าวิ่งมองด้านข้าง หันขวา + ทหารม้าชูดาบ (rider=Look หรือ None = ม้าไร้คนขี่) — x,y = พื้น"""
    from people import head
    c = g.c
    ph = t * 12 * gallop + seed
    by = -14 * abs(math.sin(ph)) * gallop
    with g.at(x, y + by, sc, 0, sx=-sc if flip else sc, sy=sc):
        for k, (lx, off) in enumerate(((-110, 0), (-70, 1.6), (90, 3.1), (130, 4.7))):
            a = 30 * math.sin(ph + off) * gallop
            with g.at(lx, -230, 1, a):
                _stroke(c, [(0, 0), (6, 110), (0, 210)], 30, INK)
                _stroke(c, [(0, 0), (6, 110), (0, 210)], 22, HORSE2 if k % 2 == 0 else col)
                _rr(c, -16, 200, 32, 22, 6)
                _shade(c, INK, 0, 0)
        _smooth_path(c, [(-170, -260), (-120, -330), (80, -340), (170, -300), (180, -230), (120, -190), (-120, -190),
                         (-180, -220)])
        _shade(c, col, 6, 0.3)
        _smooth_path(c, [(120, -310), (180, -420), (230, -450), (290, -400), (280, -370), (220, -380), (190, -260)])
        _shade(c, col, 6, 0.3)
        g.circle(250, -420, 6, INK, 0)
        _stroke(c, [(130, -320), (170, -410), (220, -455)], 14, hexc("#3a2614"))   # แผงคอ
        _stroke(c, [(-170, -260), (-240, -240 + 20 * math.sin(ph)), (-260, -170)], 16, hexc("#3a2614"))   # หาง
        _rr(c, -70, -350, 120, 30, 8)   # อานม้า + ผ้ารองอาน
        _shade(c, hexc("#2b3a5a"), 4, 0.1)
        if rider is not None:
            _smooth_path(c, [(-30, -340), (40, -340), (50, -480), (-20, -490)])
            _shade(c, rider.suit, 5, 0.3)
            for k in range(4):
                _stroke(c, [(-5, -460 + k * 28), (35, -460 + k * 28)], 3, GOLD, smooth=False)
            _stroke(c, [(0, -340), (40, -280), (20, -220)], 18, INK)
            _stroke(c, [(0, -340), (40, -280), (20, -220)], 12, rider.pants or rider.suit)
            # แขนชูดาบ
            ang = math.radians(lerp_ang(sabre))
            hx, hy = 30 + 120 * math.cos(ang), -460 + 120 * math.sin(ang)
            _stroke(c, [(30, -460), (hx, hy)], 16, INK)
            _stroke(c, [(30, -460), (hx, hy)], 10, rider.suit)
            bx, by2 = hx + 190 * math.cos(ang - 0.25), hy + 190 * math.sin(ang - 0.25)
            _stroke(c, [(hx, hy), (bx, by2)], 9, INK, smooth=False)
            _stroke(c, [(hx, hy), (bx, by2)], 5, hexc("#dfe4ea"), smooth=False)
            g.circle(hx, hy, 9, GOLD, 3)
            with g.at(14, -560, 0.62):
                head(g, rider, "firm", 0, 0.4, (0, 0), 2, 4.5)


def lerp_ang(sabre):
    """sabre 1 = ชูดาบชี้ไปข้างหน้าเฉียงขึ้น, 0 = ลดดาบ"""
    return -50 * sabre + 20 * (1 - sabre)


def cannon(g, x, y, sc=1.0, t=0.0, fire=0.0, flip=False):
    """ปืนใหญ่สนามรัสเซียยุค 1850 (ลำกล้องสำริด ล้อไม้)"""
    c = g.c
    with g.at(x, y, sc, 0, sx=-sc if flip else sc, sy=sc):
        rec = -14 * fire
        with g.at(rec, -110, 1, -8):
            _smooth_path(c, [(-70, -26), (220, -18), (230, 18), (-70, 26), (-90, 0)])
            _shade(c, hexc("#b88a3a"), 5, 0.3)
            _rr(c, 210, -22, 24, 44, 6)
            _shade(c, hexc("#a8782a"), 4, 0.2)
            if fire > 0:
                g.star(260, 0, 90 * fire, FIRE, 4, pts=9, inner=0.4)
                g.star(260, 0, 45 * fire, hexc("#fff1c4"), 0, pts=9, inner=0.5)
        _stroke(c, [(-40, -90), (-220, 0)], 22, INK, smooth=False)
        _stroke(c, [(-40, -90), (-220, 0)], 14, RU_GREEN, smooth=False)
        c.new_path()
        c.arc(0, -60, 62, 0, 2 * math.pi)
        _shade(c, hexc("#8a6a42"), 6, 0.2)
        for k in range(6):
            a = k * math.pi / 3
            _stroke(c, [(0, -60), (56 * math.cos(a), -60 + 56 * math.sin(a))], 5, INK, smooth=False)
        c.new_path()
        c.arc(0, -60, 14, 0, 2 * math.pi)
        _shade(c, hexc("#5a4a3a"), 3, 0)


def hills(g, y, t=0.0, a=1.0):
    """เนินเขาสองข้างหุบ (ฉากหลัง)"""
    c = g.c
    _smooth_path(c, [(-600, y), (-600, y - 360), (-200, y - 520), (200, y - 400), (420, y - 300), (420, y)])
    _shade(c, HILL, 6, 0.2)
    _smooth_path(c, [(660, y), (660, y - 300), (900, y - 420), (1300, y - 520), (1700, y - 360), (1700, y)])
    _shade(c, HILL, 6, 0.35)


def valley_map(g, x, y, sc=1.0, t=0.0, charge=0.0, fire=0.0, wrong=0.0, right=0.0):
    """แผนที่มองบน: หุบเขายาว ปืนรัสเซียปลายหุบ + บนเนินซ้าย-ขวา, ลูกศรทหารม้าวิ่งเข้าไป"""
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -380, -560, 760, 1120, 30)
        _shade(c, GRASS, 6, 0.1)
        for sx in (-1, 1):
            _smooth_path(c, [(sx * 380, -560), (sx * 200, -520), (sx * 170, 0), (sx * 210, 480), (sx * 380, 560)])
            _shade(c, HILL, 5, 0.25)
        g.label("หุบเหวแห่งความตาย", 0, 140, 46, color=hexc("#5a5a3a"))
        guns = [(-60, -470), (0, -480), (60, -470)] + [(-260, -300 + 150 * i) for i in range(4)] + \
               [(260, -300 + 150 * i) for i in range(4)]
        for i, (gx, gy) in enumerate(guns):
            g.circle(gx, gy, 20, RU_GREEN, 4)
            if fire > 0:
                u = (t * 2 + i * 0.37) % 1
                g.circle(gx, gy, 20 + 30 * u, (0.98, 0.66, 0.23, fire * (1 - u)), 0)
        if right > 0:   # ปืนที่รัสเซียกำลังลากหนี (เป้าหมายจริง บนเนินขวา) — มองไม่เห็นจากก้นหุบ
            with g.at(300, 330, right):
                g.circle(0, 0, 22, RU_GREEN, 4)
                g.line([(-30, 30), (30, 70)], 6, INK, amp=0)
        if charge > 0:
            yy = 480 - 900 * charge
            g.line([(0, 480), (0, yy)], 18, CHERRY, amp=0)
            c.new_path()
            for p in [(-40, yy + 30), (0, yy - 30), (40, yy + 30)]:
                c.line_to(*p)
            c.close_path()
            _shade(c, CHERRY, 4, 0)
        if wrong > 0:
            g.line([(-40, 400), (-40, 400 - 700 * wrong)], 10, (0.2, 0.2, 0.2, 0.5), amp=0)


def order_paper(g, x, y, sc=1.0, rot=0.0, blur=0.0):
    """จดหมายคำสั่ง (ข้อความคลุมเครือ)"""
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -170, -220, 340, 440, 8)
        _shade(c, hexc("#f1e3c0"), 6, 0.15)
        g.text("ORDER", 0, -160, 44, "kanit", INK)
        for i in range(7):
            ww = 260 - 60 * (i % 3)
            _stroke(c, [(-130, -90 + i * 40), (-130 + ww, -90 + i * 40 + 6 * math.sin(i * 3 + blur * 4) * blur)],
                    5, INK, 0.5, smooth=False)
        g.text("?", 110, 150, 90 * blur + 1, "kanit", RED)


def bugle(g, x, y, sc=1.0, rot=0.0, t=0.0, blow=0.0):
    c = g.c
    with g.at(x, y, sc, rot):
        _stroke(c, [(-200, 0), (-60, 0), (40, -30), (40, 30), (-60, 0)], 16, INK)
        _stroke(c, [(-200, 0), (-60, 0), (40, -30), (40, 30), (-60, 0)], 10, GOLD)
        _smooth_path(c, [(40, -30), (140, -90), (150, 90), (40, 30)])
        _shade(c, GOLD, 6, 0.3)
        if blow > 0:
            for i in range(3):
                u = (t * 1.5 + i / 3) % 1
                g.arc(160, 0, 60 + 120 * u, -40, 40, 8, (0.7, 0.55, 0.2, blow * (1 - u)))


def busby_hat(g, x, y, sc=1.0, rot=0.0):
    """หมวกทหารม้าตกอยู่บนพื้น (แทนการสูญเสีย)"""
    c = g.c
    with g.at(x, y, sc, rot):
        _smooth_path(c, [(-60, 0), (-64, -120), (-40, -140), (40, -140), (64, -120), (60, 0)])
        _shade(c, hexc("#2b2420"), 5, 0.2)
        _smooth_path(c, [(20, -130), (14, -200), (34, -220), (40, -140)])
        _shade(c, WHITE, 3, 0.15)


def telescope(g, x, y, sc=1.0, rot=-15):
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, 0, -14, 160, 28, 6)
        _shade(c, GOLD, 4, 0.25)
        _rr(c, 150, -18, 60, 36, 6)
        _shade(c, hexc("#3a3632"), 4, 0.1)


def cross_grave(g, x, y, sc=1.0):
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -10, -160, 20, 160, 3)
        _shade(c, hexc("#e8e0cc"), 4, 0.1)
        _rr(c, -50, -125, 100, 20, 3)
        _shade(c, hexc("#e8e0cc"), 4, 0.1)
