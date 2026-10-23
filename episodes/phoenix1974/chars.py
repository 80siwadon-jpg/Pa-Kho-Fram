"""ตัวละครและพร็อพ: วันเกิดวาคีน ฟินิกซ์ (28 ต.ค. 1974)
ไม่วาดการตาย/การใช้ยา: ใช้ไซเรน แสงไฟรถพยาบาล โทรศัพท์ เทียน แทน
ไม่ใช้ภาพจริง/โลโก้ของภาพยนตร์ Joker/Gladiator/Her และไม่วาดรูปปั้นออสการ์จริง (ใช้ถ้วยทองทั่วไป)"""
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


_sn = _load("snoop1971")
_kp = _load("katyperry1984")
_cr = _load("crichton1942")
_gt = _load("gates1955")
_sk = _load("salk1914")
streetlight, microphone, sound_waves, crowd = _sn.streetlight, _sn.microphone, _sn.sound_waves, _sn.crowd
guitar, spotlight, tear_drops = _kp.guitar, _kp.spotlight, _kp.tear_drops
clapper = _cr.clapper
heart = _gt.heart
globe = _sk.globe

JOKER_RED = hexc("#c8423a")
JOKER_ORANGE = hexc("#d9823a")
JOKER_GREEN = hexc("#3c7a4a")

# วาคีน ฟินิกซ์ ปัจจุบัน: ผมเทาหวีเสยไปด้านหลัง เคราเต็มน้ำตาลแซมเทา คิ้วเข้ม สูทดำลายเส้น
JOAQUIN = Look(hair="slick", hair_col=hexc("#6b5a48"), suit=hexc("#22252c"), tie=hexc("#1b1714"), w=60, jaw=0.6,
               nose=1.1, brow=1.25, age=0.55, facial="beard")
# ช่วงหนุ่ม (ยุค 90): ผมดำยาวปรกหน้า หน้าเด็ก
JOAQUIN_TEEN = Look(hair="long", hair_col=hexc("#2b2622"), outfit="flannel", suit=hexc("#5a6a4a"),
                    pants=hexc("#3a3a40"), w=55, jaw=0.4, age=0.0, brow=1.1)
JOAQUIN_KID = Look(hair="long", hair_col=hexc("#5a3a22"), outfit="tee", suit=hexc("#d9a441"), pants=hexc("#5a6a8a"),
                   w=55, age=0.0, height=0.6, headsc=1.45)
# ช่วงผอมเพื่อบทตัวตลก (ไม่ใช้หน้าตาตัวละครลิขสิทธิ์จริง): สูทแดง เสื้อกั๊กส้ม เชิ้ตเขียว
JOAQUIN_THIN = Look(hair="long", hair_col=hexc("#2b2f3a"), suit=JOKER_RED, shirt=JOKER_GREEN, tie=JOKER_ORANGE,
                    outfit="vest", w=54, jaw=0.4, age=0.4, build=0.72, brow=1.2)
# ริเวอร์ ฟินิกซ์: ผมทองปัดยาว หน้าหล่อ ยิ้ม
RIVER = Look(hair="full", hair_col=hexc("#c99a52"), outfit="tee", suit=hexc("#e8e0cc"), pants=hexc("#3a4a6a"), w=56,
             jaw=0.4, age=0.0)
RIVER_KID = Look(hair="full", hair_col=hexc("#d9b070"), outfit="tee", suit=hexc("#5a8ab8"), pants=hexc("#3a3a40"),
                 w=55, age=0.0, height=0.68, headsc=1.4)
SIBS = [
    Look(hair="long", hair_col=hexc("#8a5a2a"), outfit="dress", suit=hexc("#c8553d"), w=54, height=0.62,
         headsc=1.45),
    Look(hair="long", hair_col=hexc("#5a3a22"), outfit="dress", suit=hexc("#3c8d4f"), w=54, height=0.55,
         headsc=1.45),
]
PRESS = [
    Look(hair="part", hair_col=hexc("#3a2f28"), suit=hexc("#3a3f48"), tie=hexc("#7a2e2e"), w=58, age=0.4),
    Look(hair="bun", hair_col=hexc("#8a5a2a"), outfit="dress", suit=hexc("#3f6496"), w=54, age=0.3, height=0.93),
]


def payphone(g, x, y, sc=1.0, t=0.0, ring=0.0):
    """โทรศัพท์สาธารณะติดเสา + หูโทรศัพท์สั่น"""
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -14, -500, 28, 500, 6)
        _shade(c, GREY, 4, 0.2)
        _rr(c, -110, -800, 220, 320, 20)
        _shade(c, hexc("#3a5a8a"), 6, 0.25)
        _rr(c, -80, -760, 160, 50, 8)
        _shade(c, WHITE, 3, 0)
        g.text("911", 0, -735, 34, "kanit", RED)
        for r in range(4):
            for i in range(3):
                g.circle(-40 + i * 40, -670 + r * 40, 13, hexc("#c9ced6"), 3)
        jx = ring * 6 * math.sin(t * 40)
        with g.at(-150 + jx, -650, 1, -10):
            _rr(c, -26, -110, 52, 220, 20)
            _shade(c, INK, 4, 0)
        _stroke(c, [(-150, -540), (-130, -470), (-60, -500)], 5, INK)


def siren(g, x, y, sc=1.0, t=0.0, k=1.0):
    """ไฟไซเรน แดง-น้ำเงินสลับ (สื่อเหตุฉุกเฉิน)"""
    on = math.sin(t * 9) > 0
    with g.at(x, y, sc):
        g.rrect(-120, -40, 240, 70, 20, hexc("#3a3f48"), 5)
        g.rrect(-110, -100, 100, 60, 20, RED if on else hexc("#7a2e2e"), 5)
        g.rrect(10, -100, 100, 60, 20, hexc("#2b6fd1") if not on else hexc("#1f3a6a"), 5)
    if k > 0:
        col = (1, 0.2, 0.2) if on else (0.2, 0.4, 1)
        for i in range(3):
            u = (t * 1.5 + i / 3) % 1
            g.arc(x, y - 70 * sc, (150 + 260 * u) * sc, 200, 340, 8, (*col, (1 - u) * 0.7 * k))


def club_front(g, x, y, sc=1.0, t=0.0):
    """หน้าร้านไนท์คลับกลางคืน (ประตู + ป้ายไฟนีออน)"""
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -320, -520, 640, 520, 6)
        _shade(c, hexc("#2b2b33"), 6, 0.1)
        _rr(c, -90, -300, 180, 300, 8)
        _shade(c, hexc("#141416"), 4, 0)
        a = 0.6 + 0.4 * math.sin(t * 5)
        g.rrect(-220, -470, 440, 100, 30, (0.1, 0.1, 0.12, 1), 6, stroke=(1, 0.3, 0.6, a))
        g.text("CLUB", 0, -420, 64, "kanit", (1, 0.4, 0.7, a))


def candle(g, x, y, sc=1.0, t=0.0):
    c = g.c
    with g.at(x, y, sc):
        g.circle(0, -230, 80 + 6 * math.sin(t * 6), (1, 0.85, 0.4, 0.25), 0)
        _rr(c, -26, -200, 52, 200, 8)
        _shade(c, WHITE, 5, 0.15)
        g.poly([(0, -280 + 6 * math.sin(t * 7)), (20, -220), (0, -200), (-20, -220)], GOLD2, 3, amp=0, smooth=True)


def phoenix_bird(g, x, y, sc=1.0, t=0.0, k=1.0):
    """นกฟีนิกซ์ปีกไฟ ลุกขึ้นจากกองเถ้า (k = ระดับลุกขึ้น)"""
    c = g.c
    with g.at(x, y, sc):
        g.blob(0, 60, 200, 40, hexc("#8a8a8a"), 5, seed=3)   # กองเถ้า
        for i in range(5):
            u = (t * 0.6 + i / 5) % 1
            g.circle(-120 + i * 60, 40 - 120 * u, 10, (0.5, 0.5, 0.5, 1 - u), 0)
        if k <= 0.02:
            return
        with g.at(0, -100 * k, k):
            flap = math.sin(t * 5)
            for sx in (-1, 1):
                with g.at(0, -60, 1, sx * (10 + 15 * flap)):
                    _smooth_path(c, [(0, 0), (sx * 120, -140), (sx * 260, -160), (sx * 200, -90), (sx * 240, -60),
                                     (sx * 150, -30), (sx * 170, 0), (sx * 60, 20)])
                    _shade(c, hexc("#e8743a"), 6, 0.2)
                    _smooth_path(c, [(sx * 40, -10), (sx * 150, -110), (sx * 190, -100), (sx * 80, 0)])
                    _shade(c, GOLD2, 0, 0)
            g.blob(0, -40, 60, 90, hexc("#d9502a"), 6, seed=5)
            g.circle(0, -150, 46, hexc("#e8743a"), 6)
            g.circle(14, -158, 8, INK, 0)
            g.poly([(40, -150), (80, -140), (40, -130)], GOLD, 4, amp=0)
            for i in range(3):
                g.poly([(-20 + i * 20, -190), (-30 + i * 20, -250 - 10 * math.sin(t * 6 + i)), (-5 + i * 20, -195)],
                       GOLD2, 3, amp=0)
            for i in range(3):
                _smooth_path(c, [(-20 + i * 20, 40), (-50 + i * 30, 150 + 10 * math.sin(t * 4 + i)), (-5 + i * 20, 45)])
                _shade(c, hexc("#e8743a"), 4, 0.1)


def hat(g, x, y, sc=1.0, t=0.0, coins=0):
    """หมวกเปิดรับเงินข้างถนน"""
    c = g.c
    with g.at(x, y, sc):
        c.save()
        c.scale(1, 0.35)
        c.new_path()
        c.arc(0, 0, 120, 0, 2 * math.pi)
        c.restore()
        _shade(c, hexc("#5a3a22"), 5, 0.2)
        _smooth_path(c, [(-70, 0), (-60, -80), (60, -80), (70, 0)])
        _shade(c, hexc("#6e4528"), 5, 0.2)
        for i in range(coins):
            g.circle(-50 + i * 30, -10 - (i % 2) * 8, 14, GOLD, 3)


def golden_statue(g, x, y, sc=1.0, rot=0.0, glow=0.0, t=0.0):
    """ถ้วยรางวัลรูปคนสีทอง (ทั่วไป ไม่ใช่ออสการ์ของจริง)"""
    c = g.c
    with g.at(x, y, sc, rot):
        if glow > 0:
            g.sunburst(0, -200, 120, 260, 16, t * 10, 8, (1, 0.85, 0.4, 0.6 * glow))
        _rr(c, -90, -60, 180, 60, 8)
        _shade(c, hexc("#2b2622"), 5, 0.1)
        _rr(c, -60, -100, 120, 40, 8)
        _shade(c, GOLD, 5, 0.2)
        _smooth_path(c, [(-30, -100), (-36, -260), (-50, -330), (50, -330), (36, -260), (30, -100)])
        _shade(c, GOLD, 6, 0.3)
        g.circle(0, -370, 38, GOLD, 6)
        for sx in (-1, 1):
            _stroke(c, [(sx * 40, -320), (sx * 20, -260), (0, -250)], 10, INK)
            _stroke(c, [(sx * 40, -320), (sx * 20, -260), (0, -250)], 6, GOLD)


def stairs(g, x, y, sc=1.0, n=7):
    """บันไดยาวในเมือง (ภาพจำของฉากเต้นในภาพยนตร์)"""
    c = g.c
    with g.at(x, y, sc):
        for i in range(n):
            _rr(c, -300 + i * 70, -i * 60 - 60, 600 - i * 70, 60, 2)
            _shade(c, hexc("#c9c2b2"), 4, 0.15)
        _stroke(c, [(-300, -40), (190, -460)], 6, GREY, smooth=False)


def scale_weigh(g, x, y, sc=1.0, kg=0.0):
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -150, -60, 300, 60, 14)
        _shade(c, hexc("#e9ecf0"), 6, 0.2)
        _rr(c, -60, -50, 120, 40, 8)
        _shade(c, hexc("#1b2a1c"), 3, 0)
        g.text(f"-{kg:.0f} kg", 0, -30, 30, "kanit", (0.4, 1, 0.5, 1))


def laughing_tears(g, x, y, sc=1.0, t=0.0):
    """หน้ากากละคร หัวเราะ/ร้องไห้"""
    with g.at(x, y, sc, 6 * math.sin(t * 2)):
        for i, (dx, rot, sad) in enumerate(((-70, -12, False), (70, 12, True))):
            with g.at(dx, 0, 1, rot):
                g.blob(0, 0, 90, 110, WHITE if not sad else hexc("#d9d5e8"), 6, seed=4 + i)
                for sx in (-1, 1):
                    g.arc(sx * 32, -20, 18, 200 if not sad else 20, 340 if not sad else 160, 6, INK)
                if sad:
                    g.arc(0, 60, 30, 200, 340, 7, INK)
                    g.circle(28, 10, 8, (0.5, 0.75, 1, 1), 0)
                else:
                    g.arc(0, 30, 34, 20, 160, 7, INK)


def paw(g, x, y, r, col=hexc("#7a5a3a")):
    g.circle(x, y + r * 0.3, r * 0.6, col, 4)
    for i in range(4):
        a = math.radians(-150 + i * 40)
        g.circle(x + r * 0.7 * math.cos(a), y + r * 0.7 * math.sin(a) - r * 0.1, r * 0.25, col, 3)


def leaf(g, x, y, sc=1.0, rot=0.0):
    with g.at(x, y, sc, rot):
        g.poly([(0, -80), (40, -20), (0, 60), (-40, -20)], hexc("#3c8d4f"), 5, amp=0, smooth=True)
        g.line([(0, -70), (0, 60)], 3, INK, amp=0)


def poem(g, x, y, sc=1.0, rot=0.0, write=1.0):
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -200, -260, 400, 520, 8)
        _shade(c, hexc("#f4eedf"), 6, 0.1)
        g.text("River, 17", 60, -200, 30, "kanitm", GREY)
        for k in range(int(8 * write)):
            _stroke(c, [(-150, -130 + k * 44 + 3 * math.sin(k)), (150 - (k % 3) * 40, -130 + k * 44)], 4, NAVY, 0.8)
        heart(g, -110, 200, 30, RED)


def film_strip(g, x, y, sc=1.0, rot=0.0, label="", col=INK, t=0.0):
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -170, -120, 340, 240, 10)
        _shade(c, hexc("#2b2b30"), 5, 0)
        for i in range(6):
            _rr(c, -150 + i * 54, -110, 30, 20, 3)
            c.set_source_rgba(1, 1, 1, 1)
            c.fill()
            _rr(c, -150 + i * 54, 90, 30, 20, 3)
            c.set_source_rgba(1, 1, 1, 1)
            c.fill()
        _rr(c, -150, -76, 300, 152, 6)
        _shade(c, col, 3, 0)
        if label:
            from gfx import text_sprite
            size = 52
            while size > 24 and text_sprite(label, size, "kanit")[2] > 280:
                size -= 2
            g.text(label, 0, 0, size, "kanit", WHITE)
