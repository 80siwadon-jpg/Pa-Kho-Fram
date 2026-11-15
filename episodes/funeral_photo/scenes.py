"""ฉากตอน funeral_photo: รับจ้างซ่อมรูปถ่ายหน้าศพ — การ์ตูน 2D แบนเรียบ ฉากหลังเบลอ เปลี่ยนช็อตทุกบรรทัด"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from chars import (BG, CREAM, FON, GOLD, GRANDMA_BW, HOSP, KENG, KILLER, LAMP, MOTHER, MUN, NIGHT, ORANGE,  # noqa: E402
                   PETE, POLICE, SCREEN, WOOD, WOOD2, WOOD3, banknote, big_eye, blurred, camera_antique,
                   crowbar, crt, darken, desk, editor_ui, envelope, fill_rect, glow, grandma_photo, id_card,
                   incense, keng_face, killer_reflection, knife, lerp_col, phone, pipe, set_city, set_exterior,
                   set_hospital, set_road_night, set_shop, set_station, set_temple_sala, set_workroom, smoke,
                   speakers, usb, vest, vignette, wall_clock)
from chars import light_pass  # noqa: E402
from gfx import INK, WHITE, H, W, e_io, e_out, hexc, hn, lerp, pop, seg  # noqa: E402
from people import _rr, _shade, _stroke, head, person  # noqa: E402

CX, CY = W / 2, H / 2
FLOOR = 1040
SUB_COLOR = hexc("#ffffff")
SUB_STROKE = (5, (0.05, 0.05, 0.06, 1))
SUB_PHRASES = True
SUB_SIZE = 58
AMBIENCE = {"rain": 0.025, "drone": 0.12}   # โทนห้องเงียบ ๆ + เสียงต่ำ ใต้เสียงพากย์

CAMERA = {}
TRANSITIONS = {}
NO_IRIS = set()
_names = ["hook", "pete", "mother", "mun", "rules", "night1", "grandma", "retouch", "five", "pupil", "speaker", "dawn",
          "fon", "reflect", "envelope", "keng", "incense", "zoom", "reflection", "news", "call", "night3", "bang",
          "crowbar", "knife", "flash", "fall", "ending"]
for _i, _n in enumerate(_names):
    CAMERA[_n] = ("push_in", "pan_right", "pull_out", "pan_left")[_i % 4]
    TRANSITIONS[_n] = "fade"
CAMERA.update({"five": "push_in", "pupil": "push_in", "zoom": "push_in", "reflection": "push_in", "bang": "dutch",
               "crowbar": "dutch", "knife": "dutch"})
TRANSITIONS.update({"pete": "zoom", "night1": "zoom", "envelope": "zoom", "night3": "zoom"})


# ---------------------------------------------------------------- helpers
def shoulders(g, look, x, y, sc):
    """ไหล่ + คอ ใต้หัวภาพใกล้ (ไม่ให้หัวลอย)"""
    if sc < 1.8:
        return
    with g.at(x, y, sc):
        _rr(g.c, -22, 40, 44, 60, 10)
        _shade(g.c, look.skin, 3, 0.3)
        g.blob(0, 175, 150, 95, look.suit, 3, 7)


def beat(t, L):
    i = 0
    for k, x in enumerate(L):
        if t >= x - 0.2:
            i = k
    return i


def run_shots(g, t, L, d, shots):
    """หนึ่งช็อตต่อหนึ่งบรรทัด: shots[i](g, t, lt) lt = เวลานับจากต้นช็อต"""
    i = beat(t, L)
    fn = shots[min(i, len(shots) - 1)]
    t0 = L[i] - 0.2 if i < len(L) else 0
    g.light = None
    fn(g, t, max(t - t0, 0.0))
    lx, ly, col, k = g.light or (CX, -200, (0.95, 0.92, 0.86), 0.35)
    light_pass(g, lx, ly, col, k)


LIGHTS = {   # แหล่งแสงหลักของแต่ละฉาก (x, y, สี, ความแรง)
    "work_night": (1150, 560, (0.75, 0.88, 1.0), 0.6), "work_dawn": (1500, 280, (1.0, 0.82, 0.7), 0.55),
    "work_dusk": (1500, 280, (1.0, 0.66, 0.4), 0.6), "work_day": (1500, 280, (1.0, 0.95, 0.85), 0.4),
    "shop_day": (1550, 150, (1.0, 0.88, 0.66), 0.5), "shop_night": (1300, 980, (1.0, 0.8, 0.5), 0.6),
    "ext_night": (1560, 300, (1.0, 0.82, 0.55), 0.6), "ext_day": (1700, -100, (1.0, 0.95, 0.8), 0.4),
    "ext_dawn": (300, 300, (1.0, 0.78, 0.65), 0.55), "ext_dusk": (1700, 200, (1.0, 0.65, 0.4), 0.55),
    "hosp": (1550, 280, (0.92, 0.97, 1.0), 0.45), "city": (CX, -200, (1.0, 0.97, 0.9), 0.35),
    "sala": (960, 250, (1.0, 0.86, 0.6), 0.5), "road": (1420, 220, (1.0, 0.8, 0.5), 0.65),
    "station": (650, 200, (1.0, 0.6, 0.3), 0.6), "stairs": (300, 0, (1.0, 0.82, 0.55), 0.55),
}


def bg(g, key, fn, zoom=1.0, fx=CX, fy=CY, radius=7):
    """ฉากหลังเบลอ ซูมเข้าหา (fx, fy) ได้ (ช็อตใกล้จากฉากเดียวกัน) + ตั้งแหล่งแสงของฉาก"""
    if key in LIGHTS:
        lx, ly, col, k = LIGHTS[key]
        g.light = (CX + (lx - fx) * zoom, CY + (ly - fy) * zoom, col, k)
    if zoom == 1.0:
        blurred(g, key, fn, radius)
        return
    with g.at(CX, CY, zoom):
        with g.at(-fx, -fy):
            blurred(g, key, fn, radius)


def ws(g, tod="night"):
    bg(g, "work_" + tod, lambda g2: set_workroom(g2, tod))


def shop(g, tod="day", zoom=1.0, fx=CX, fy=CY):
    bg(g, "shop_" + tod, lambda g2: set_shop(g2, tod), zoom, fx, fy)


def ext(g, tod="night", zoom=1.0, fx=CX, fy=CY):
    bg(g, "ext_" + tod, lambda g2: set_exterior(g2, tod), zoom, fx, fy, radius=5)


def slide(lt, a=0.0, b=1.0, dur=3.0):
    return lerp(a, b, e_io(min(lt / dur, 1.0)))


def tilt_shift_dark(g, k=0.45):
    vignette(g, k)


def grandma_screen(restore=1.0, smile=False, sc=0.45, t=0.0):
    return lambda g2: editor_ui(g2, lambda g3: grandma_photo(g3, 20, -215, sc, t, restore, True, smile))


def keng_screen(t, bruise=1.0, sc=0.38, zoom_label=None):
    return lambda g2: editor_ui(g2, lambda g3: keng_face(g3, 20, -215, sc, t, bruise), zoom_label)


def desk_scene(g, t, screen, pete_mood="neutral", tod="night", pete=True, lit_incense=True, burn=0.0, look=(1, 0),
               pose="hold", talk=False):
    """ช็อตกว้างห้องทำงาน: พีทนั่งหน้าคอม"""
    ws(g, tod)
    if tod == "night":
        glow(g, 1080, 520, 520, LAMP, 0.12)
    if pete:
        person(g, 640, 1180, PETE, 0.78, mood=pete_mood, pose=pose, turn=0.75, seed=1, look_at=look, talk=talk)
    desk(g, 1000, 880, 1300)
    crt(g, 1150, 880, 0.75, screen)
    speakers(g, 1450, 880, 0.75)
    incense(g, 820, 880, t, lit_incense, burn, 0.8)
    if tod == "night":
        darken(g, 0.18)


def monitor_close(g, t, screen, sc=2.1, dy=0):
    """ช็อตใกล้หน้าจอ"""
    ws(g, "night")
    darken(g, 0.35)
    crt(g, CX, 1020 + 260 * (sc - 2.1) + dy, sc, screen)


# ================================================================ 1 hook
def s_hook(g, t, L, d):
    def a(g, t, lt):   # ร้านหน้าวัด กลางดึก
        ext(g, "night", 1.0 + 0.04 * lt / 3)
        vignette(g, 0.5)

    def b(g, t, lt):   # ซูมหน้าต่างชั้นสอง
        ext(g, "night", 1.8, 1195, 380)
        vignette(g, 0.55)

    def c_(g, t, lt):   # รูปหน้าศพในตู้กระจก
        ext(g, "night", 3.6, 790, 660)
        vignette(g, 0.6)

    def d_(g, t, lt):   # ดวงตาในรูป
        fill_rect(g.c, -800, -800, W + 1600, H + 1600, BG)
        big_eye(g, CX, CY, 1.3 + 0.05 * lt, (0, 0))
        vignette(g, 0.7)

    def e(g, t, lt):
        ext(g, "night", 1.25, 1000, 520)
        vignette(g, 0.5)
    run_shots(g, t, L, d, [a, b, c_, d_, e])


# ================================================================ 2 pete
def s_pete(g, t, L, d):
    def a(g, t, lt):
        bg(g, "city", set_city)
        person(g, 900, 1250, PETE, 0.85, mood="neutral", pose="hold", turn=0.0, seed=1)
        with g.at(900, 760):
            _rr(g.c, -170, -40, 340, 160, 8)
            _shade(g.c, hexc("#b8925e"), 3, 0.2)
            _rr(g.c, -60, -110, 80, 80, 6)
            _shade(g.c, hexc("#4a4a4a"), 3, 0.2)

    def b(g, t, lt):
        bg(g, "city", set_city, 1.3, 1000, 640)
        person(g, 700, 1300, PETE, 0.9, mood="sad", pose="down", turn=0.4, seed=1)

    def c_(g, t, lt):   # หน้าพีทใกล้ (แนะนำตัว)
        bg(g, "city", set_city, 1.6, 600, 500)
        shoulders(g, PETE, 960, 620, 3.4)
        with g.at(960, 620, 3.4):
            head(g, PETE, "neutral", 0.4 * max(0, math.sin(t * 9)), 0.1, (0, 0), 1)
        g.blob(960, 1100, 360, 250, PETE.suit, 3, 2)

    def d_(g, t, lt):
        bg(g, "city", set_city, 1.0)
        person(g, lerp(900, 1500, slide(lt, 0, 1, 4)), 1250, PETE, 0.8, mood="sad", pose="hold", turn=0.7, seed=1)
    run_shots(g, t, L, d, [a, b, c_, d_])


# ================================================================ 3 mother
def bed(g, x, y, sc=1.0):
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -420, -200, 840, 140, 20)
        _shade(c, hexc("#e9eef0"), 3, 0.2)
        _rr(c, -420, -60, 840, 60, 8)
        _shade(c, hexc("#9aa6aa"), 3, 0.2)
        _rr(c, -440, -330, 40, 330, 8)
        _shade(c, hexc("#c9d2d6"), 3, 0.2)


def monitor_heart(g, x, y, t, sc=1.0):
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -150, -110, 300, 220, 14)
        _shade(c, hexc("#3a4448"), 3, 0.2)
        fill_rect(c, -130, -90, 260, 180, hexc("#0e1a16"))
        pts = []
        for k in range(60):
            xx = -125 + k * 250 / 60
            ph = (k / 60 * 2 + t * 0.8) % 1
            yy = -60 * math.exp(-((ph - 0.5) * 25) ** 2) + 10 * math.exp(-((ph - 0.58) * 20) ** 2)
            pts.append((xx, yy))
        _stroke(c, pts, 4, hexc("#5ef0a0"), 1.0, smooth=False)


def s_mother(g, t, L, d):
    def a(g, t, lt):
        bg(g, "hosp", set_hospital)
        monitor_heart(g, 1400, 520, t, 1.4)
        with g.at(700, 760):
            bed(g, 0, 200, 1.1)
            shoulders(g, MOTHER, -300, -40, 2.0)
            with g.at(-300, -40, 2.0):
                head(g, MOTHER, "sad", 0.0, 0.5, (0.5, 0), 3)

    def b(g, t, lt):   # ใบแจ้งค่าใช้จ่าย
        bg(g, "hosp", set_hospital, 1.5, 1300, 600)
        with g.at(CX, CY, 1.0 + 0.03 * lt, -3):
            _rr(g.c, -360, -420, 720, 840, 8)
            _shade(g.c, WHITE, 3, 0.1)
            g.text("ใบแจ้งค่ารักษา", 0, -330, 52, "kanit", INK)
            for k in range(5):
                _stroke(g.c, [(-280, -220 + k * 70), (280, -220 + k * 70)], 6, hexc("#c9c9c4"), 1.0)
            g.text("รวม 280,000 บาท", 0, 260, 64, "kanit", hexc("#b23a2a"))

    def c_(g, t, lt):   # แอปธนาคาร เหลือไม่ถึงหมื่น
        bg(g, "hosp", set_hospital, 1.3, 700, 500)

        def scr(g2):
            fill_rect(g2.c, -96, -196, 192, 392, hexc("#eef3f6"))
            fill_rect(g2.c, -96, -196, 192, 70, hexc("#3a6a9a"))
            g2.text("ยอดคงเหลือ", 0, -60, 22, "kanitm", INK)
            g2.text("8,412.50", 0, -10, 34, "kanit", hexc("#b23a2a"))
        phone(g, CX, 600, 1.5 + 0.03 * lt, -4, scr)

    def d_(g, t, lt):   # มือแม่จับมือพีท
        bg(g, "hosp", set_hospital)
        with g.at(800, 760):
            bed(g, 0, 200, 1.1)
            shoulders(g, MOTHER, -300, -40, 2.0)
            with g.at(-300, -40, 2.0):
                head(g, MOTHER, "smile", 0.6 * max(0, math.sin(t * 8)), 0.5, (0.6, 0.1), 3)
        person(g, 1380, 1250, PETE, 0.85, mood="sad", pose="hold", turn=-0.7, seed=1)
        g.blob(1100, 820, 60, 40, MOTHER.skin, 3, 2)
        g.blob(1150, 830, 60, 40, PETE.skin, 3, 3)

    def e(g, t, lt):   # พีทนอนไม่หลับ
        fill_rect(g.c, -800, -800, W + 1600, H + 1600, hexc("#1a2028"))
        glow(g, 1400, 300, 500, hexc("#8aa6c9"), 0.2)
        _rr(g.c, 200, 700, 1300, 250, 30)
        _shade(g.c, hexc("#4a5666"), 3, 0.2)
        shoulders(g, PETE, 500, 640, 1.9)
        with g.at(500, 640, 1.9):
            head(g, PETE, "worry", 0.0, 0.4, (0.3, -0.6), 1)
        g.blob(1000, 720, 520, 110, hexc("#6a7a8e"), 3, 2)
        vignette(g, 0.6)
    run_shots(g, t, L, d, [a, b, c_, d_, e])


# ================================================================ 4 mun
def s_mun(g, t, L, d):
    def a(g, t, lt):   # โพสต์ในกลุ่มเฟซบุ๊ก
        fill_rect(g.c, -800, -800, W + 1600, H + 1600, hexc("#1a2028"))
        glow(g, CX, CY, 700, hexc("#a9c4e6"), 0.2)

        def scr(g2):
            fill_rect(g2.c, -96, -196, 192, 392, hexc("#eef1f5"))
            fill_rect(g2.c, -96, -196, 192, 50, hexc("#3b5998"))
            g2.text("กลุ่มคนอำเภอ", 0, -170, 18, "kanit", WHITE)
            _rr(g2.c, -86, -130, 172, 220, 8)
            _shade(g2.c, WHITE, 2, 0.05)
            g2.text("รับคนซ่อมรูปถ่าย", 0, -95, 18, "kanit", INK)
            g2.text("กะดึก ค่าแรงดี", 0, -68, 18, "kanit", INK)
            fill_rect(g2.c, -76, -45, 152, 110, hexc("#c9b8a0"))
        phone(g, CX, 560, 1.6, 0, scr)

    def b(g, t, lt):
        a(g, t, lt)
        with g.at(CX, 440, pop(lt, 0.2, 0.3) * 1.0):
            _rr(g.c, -300, -40, 600, 80, 30)
            _shade(g.c, hexc("#fff6d8"), 3, 0.1)

    def c_(g, t, lt):   # ลุงมั่น
        shop(g, "day")
        person(g, 900, 1180, MUN, 0.82, mood="smile", pose="hold", turn=0.2, seed=2)
        _rr(g.c, 900 - 180, 1180 - 0.82 * 0.92 * 430, 30, 400, 6)   # ไม้เท้า
        _shade(g.c, WOOD2, 2, 0.1)

    def d_(g, t, lt):   # ป้ายร้าน
        ext(g, "day", 2.4, 970, 230)

    def e(g, t, lt):
        shop(g, "day", 1.2, 1300, 600)
        person(g, 700, 1180, MUN, 0.8, mood="sad", pose="down", turn=0.4, seed=2)
        person(g, 1350, 1220, PETE, 0.84, mood="neutral", pose="hold", turn=-0.5, seed=1)
        camera_antique(g, 1700, 1080, 0.7)
    run_shots(g, t, L, d, [a, b, c_, d_, e])


# ================================================================ 5 rules
def fingers(g, x, y, n, sc=1.0, skin=None):
    skin = skin or MUN.skin
    c = g.c
    with g.at(x, y, sc):
        g.blob(0, 60, 110, 90, skin, 3, 2)
        for k in range(4):
            up = k < n
            _rr(c, -75 + k * 48, -150 if up else 10, 38, 170 if up else 60, 18)
            _shade(c, skin, 3, 0.2)


def s_rules(g, t, L, d):
    def a(g, t, lt):
        shop(g, "day", 1.3, 900, 500)
        shoulders(g, MUN, 860, 600, 3.2)
        with g.at(860, 600, 3.2):
            head(g, MUN, "firm", 0.6 * max(0, math.sin(t * 8)), 0.2, (0.3, 0), 2)

    def b(g, t, lt):   # ข้อหนึ่ง: นิ้วหนึ่ง + ธูป
        shop(g, "day", 1.6, 600, 700)
        darken(g, 0.2)
        fingers(g, 600, 560, 1, 1.6)
        incense(g, 1250, 900, t, True, 0.0, 2.0)

    def c_(g, t, lt):   # ข้อสอง: นิ้วสอง + ดวงตาในรูป
        shop(g, "day", 1.6, 600, 700)
        darken(g, 0.3)
        fingers(g, 520, 560, 2, 1.6)
        with g.at(1250, 520, 0.7):
            big_eye(g, 0, 0, 0.9, (0, 0))

    def d_(g, t, lt):   # ข้อสาม: นิ้วสาม + ประตู + นาฬิกา
        shop(g, "night", 1.2, 1000, 500)
        darken(g, 0.35)
        fingers(g, 520, 560, 3, 1.6)
        for k in range(6):
            fill_rect(g.c, 1000 + k * 90, 260, 84, 760, WOOD3)
        wall_clock(g, 1270, 180, 90, 0, 0)

    def e(g, t, lt):   # พีทยิ้มฝืด
        shop(g, "day", 1.3, 1300, 600)
        shoulders(g, PETE, 960, 600, 3.2)
        with g.at(960, 600, 3.2):
            head(g, PETE, "smug", 0.0, 0.2, (-0.4, 0), 1)

    def f(g, t, lt):
        shop(g, "day")
        person(g, 650, 1180, MUN, 0.8, mood="neutral", pose="hold", turn=0.5, seed=2)
        person(g, 1250, 1220, PETE, 0.84, mood="smile", pose="hold", turn=-0.5, seed=1)
        with g.at(1050, 560, pop(lt, 0.6, 0.4)):
            _rr(g.c, -110, -60, 220, 120, 10)
            _shade(g.c, hexc("#c9e6c0"), 3, 0.1)
            g.text("5,000", 0, 0, 52, "kanit", hexc("#2a6a2a"))
    run_shots(g, t, L, d, [a, b, c_, d_, e, f])


# ================================================================ 6 night1
def s_night1(g, t, L, d):
    def a(g, t, lt):   # บันไดไม้ (เท้าเหยียบ)
        fill_rect(g.c, -800, -800, W + 1600, H + 1600, hexc("#2a221c"))
        for k in range(7):
            y = 1080 - k * 150 + 40
            _rr(g.c, 300 + k * 60, y - 40, 1200, 40, 4)
            _shade(g.c, WOOD3, 3, 0.25)
            fill_rect(g.c, 300 + k * 60, y, 1200, 110, WOOD2)
        step = min(int(lt / 0.9), 3)
        with g.at(800 + step * 60, 1080 - step * 150 + 20, 1.3):
            _rr(g.c, -70, -40, 160, 50, 20)
            _shade(g.c, hexc("#2a2a2a"), 3, 0.1)
            _rr(g.c, -40, -260, 90, 230, 30)
            _shade(g.c, PETE.pants, 3, 0.2)
        glow(g, 1400, 0, 700, LAMP, 0.15)
        vignette(g, 0.6)

    def b(g, t, lt):
        a(g, t, lt + 1.0)

    def c_(g, t, lt):   # คอมเก่า จอตู้ครีม
        ws(g, "night")
        darken(g, 0.2)
        desk(g, CX, 880, 1500)
        crt(g, 960, 880, 0.95, None, on=lt > 0.8)
        with g.at(1400, 880, 0.9):   # สแกนเนอร์
            _rr(g.c, -170, -60, 340, 60, 10)
            _shade(g.c, hexc("#d6cdb6"), 3, 0.2)
            fill_rect(g.c, -150, -66, 300, 10, hexc("#6a7a7e"))

    def d_(g, t, lt):   # กระถางธูปข้างคีย์บอร์ด
        ws(g, "night")
        darken(g, 0.3)
        desk(g, CX, 760, 2400)
        _rr(g.c, 760, 700, 700, 60, 10)   # คีย์บอร์ด
        _shade(g.c, hexc("#d6cdb6"), 3, 0.2)
        for k in range(14):
            fill_rect(g.c, 780 + k * 48, 712, 38, 16, hexc("#bdb39a"))
        incense(g, 560, 760, t, False, 0.0, 2.2)
    run_shots(g, t, L, d, [a, b, c_, d_])


# ================================================================ 7 grandma
def s_grandma(g, t, L, d):
    def a(g, t, lt):   # รูปเปียกในมือ
        ws(g, "night")
        darken(g, 0.35)
        grandma_photo(g, CX, 520, 1.3, t, 0.0)
        for sx in (-1, 1):
            g.blob(CX + sx * 300, 860, 80, 60, PETE.skin, 3, sx)

    def b(g, t, lt):   # ลายมือหลังรูป
        ws(g, "night")
        darken(g, 0.35)
        with g.at(CX, 520, 1.3):
            fill_rect(g.c, -200, -260, 400, 520, hexc("#e9e4d6"))
            g.text("ยายผิน", 0, -40, 70, "kanitm", hexc("#4a4a6a"), rot=-6)
            for k in range(3):
                g.blob(-90 + k * 80, 150, 50, 30, (0.75, 0.72, 0.65, 0.6), 0, k)

    def c_(g, t, lt):
        ws(g, "night")
        darken(g, 0.4)
        grandma_photo(g, CX, 540, 1.6 + 0.05 * lt, t, 0.0)

    def d_(g, t, lt):   # จุดธูป
        ws(g, "night")
        darken(g, 0.45)
        incense(g, CX, 900, t, lt > 1.0, 0.0, 3.0)
        if lt < 1.4:
            g.blob(CX + 120, 480, 60, 40, PETE.skin, 3, 2)
            glow(g, CX + 60, 470, 60, (1, 0.7, 0.3, 1), 0.8 * (lt > 0.6))

    def e(g, t, lt):   # พีทไหว้ กระซิบ
        desk_scene(g, t, grandma_screen(0.0), "neutral", pose="hold", look=(1, -0.2))
    run_shots(g, t, L, d, [a, b, c_, d_, e])


# ================================================================ 8 retouch
def s_retouch(g, t, L, d):
    def a(g, t, lt):
        monitor_close(g, t, grandma_screen(slide(lt, 0.0, 0.35, 3.5)))

    def b(g, t, lt):   # ปากกาแท็บเล็ต
        ws(g, "night")
        darken(g, 0.35)
        with g.at(CX, 700, 1.0):
            _rr(g.c, -500, -60, 1000, 300, 20)
            _shade(g.c, hexc("#2a2c30"), 3, 0.1)
            px = 200 * math.sin(t * 2.2)
            g.blob(px - 60, 40, 130, 90, PETE.skin, 3, 2)
            _stroke(g.c, [(px, 10), (px + 160, -150)], 16, hexc("#3a3a3a"), 1.0)

    def c_(g, t, lt):   # หน้าพีท แสงจอสะท้อน
        ws(g, "night")
        darken(g, 0.45)
        glow(g, 1300, 560, 600, (0.66, 0.84, 0.9, 1), 0.25)
        shoulders(g, PETE, 860, 600, 3.6)
        with g.at(860, 600, 3.6):
            head(g, PETE, "neutral", 0.0, 0.6, (1, 0.2), 1)

    def d_(g, t, lt):   # นาฬิกา 02:15
        ws(g, "night")
        darken(g, 0.3)
        wall_clock(g, CX, 520, 300, 2, 15)
    run_shots(g, t, L, d, [a, b, c_, d_])


# ================================================================ 9 five
def eye_screen(pupil=(0, 0), bw=True, iris_fn=None, glow_k=0.0, zoom_label=None):
    def scr(g2):
        def img(g3):
            big_eye(g3, 20, -215, 0.62, pupil, bw, iris_fn, glow_k)
        editor_ui(g2, img, zoom_label)
    return scr


def s_five(g, t, L, d):
    def a(g, t, lt):
        monitor_close(g, t, grandma_screen(0.75), 2.1)

    def b(g, t, lt):
        monitor_close(g, t, eye_screen(), 2.1 + 0.1 * slide(lt))

    def c_(g, t, lt):   # จอเต็ม ดวงตา
        fill_rect(g.c, -800, -800, W + 1600, H + 1600, hexc("#0c1014"))
        big_eye(g, CX, CY, 1.25 + 0.04 * lt, (0, 0))
        glow(g, CX, CY, 700, (0.66, 0.84, 0.9, 1), 0.08)

    def d_(g, t, lt):   # หน้าพีทนิ่ง ตาไม่กะพริบ
        fill_rect(g.c, -800, -800, W + 1600, H + 1600, hexc("#0c1014"))
        glow(g, CX, 520, 700, (0.66, 0.84, 0.9, 1), 0.25)
        shoulders(g, PETE, CX, 600, 4.0 + 0.1 * lt)
        with g.at(CX, 600, 4.0 + 0.1 * lt):
            head(g, PETE, "neutral", 0.0, 0.0, (0, 0), 99)
    run_shots(g, t, L, d, [a, b, c_, d_])


# ================================================================ 10 pupil
def s_pupil(g, t, L, d):
    def eye(g, px, lt, gk=0.0):
        fill_rect(g.c, -800, -800, W + 1600, H + 1600, hexc("#0a0d10"))
        big_eye(g, CX, CY, 1.3, (px, 0), True, None, gk)
        vignette(g, 0.6)

    def a(g, t, lt):
        eye(g, 0, lt)

    def b(g, t, lt):
        eye(g, -0.6 * slide(lt, 0, 1, 3.0), lt)

    def c_(g, t, lt):
        eye(g, -0.6, lt)

    def d_(g, t, lt):   # หันมามองที่ผม
        eye(g, lerp(-0.6, 0.15, e_out(min(lt / 0.8, 1))), lt, 0.6)

    def e(g, t, lt):   # มือแข็งค้างบนเมาส์
        ws(g, "night")
        darken(g, 0.5)
        with g.at(CX, 700, 2.0):
            _rr(g.c, -120, -60, 240, 260, 110)
            _shade(g.c, hexc("#d6cdb6"), 3, 0.2)
            g.blob(0, 10, 150, 110, PETE.skin, 3, 2)
            for k in range(4):
                _rr(g.c, -110 + k * 55, -150, 44, 150, 20)
                _shade(g.c, PETE.skin, 3, 0.2)
    run_shots(g, t, L, d, [a, b, c_, d_, e])


# ================================================================ 11 speaker
def rings(g, x, y, t, n=3, col=(0.85, 0.92, 0.95)):
    for k in range(n):
        r = 30 + ((t * 70 + k * 50) % 150)
        g.c.set_source_rgba(col[0], col[1], col[2], 0.55 * (1 - (r - 30) / 150))
        g.c.set_line_width(5)
        g.c.arc(x, y, r, -0.7, 0.7)
        g.c.stroke()


def s_speaker(g, t, L, d):
    def a(g, t, lt):
        ws(g, "night")
        darken(g, 0.4)
        desk(g, CX, 900, 2400)
        speakers(g, 860, 900, 2.2, True)
        rings(g, 980, 690, t)

    def b(g, t, lt):   # สายไฟห้อย ไม่ได้เสียบ
        ws(g, "night")
        darken(g, 0.5)
        with g.at(-300, -250, 1.0):
            speakers(g, 860, 900, 3.0, True)
        with g.at(1400, 760, 1.2):   # ปลั๊กผนังว่าง
            _rr(g.c, -90, -120, 180, 240, 14)
            _shade(g.c, hexc("#e9e4d6"), 3, 0.15)
            for k in (-30, 30):
                fill_rect(g.c, k - 8, -30, 16, 50, hexc("#2a2a2a"))

    def c_(g, t, lt):   # คุณยายในจอยิ้ม
        monitor_close(g, t, grandma_screen(1.0, smile=True), 2.2)
        rings(g, 1500, 560, t, 3, (0.95, 0.95, 0.9))
        glow(g, CX, 560, 500, (0.9, 0.95, 1, 1), 0.08 * (1 + math.sin(t * 2)))
    run_shots(g, t, L, d, [a, b, c_])


# ================================================================ 12 dawn
def s_dawn(g, t, L, d):
    def a(g, t, lt):
        ws(g, "dawn")
        glow(g, 1500, 300, 700, hexc("#f2c9a0"), 0.3)
        with g.at(800, 700, 1.6):
            g.blob(0, 140, 170, 160, PETE.suit, 3, 2)
            head(g, PETE, "worry", 0.0, 0.5, (0.8, 0), 1)

    def b(g, t, lt):
        desk_scene(g, t, grandma_screen(1.0, True), "worry", tod="dawn", lit_incense=False, burn=1.0)

    def c_(g, t, lt):   # หลังคาโบสถ์ + พระบิณฑบาต
        ext(g, "dawn", 1.6, 300, 450)
        glow(g, 300, 300, 600, hexc("#f7d9a8"), 0.4 * slide(lt, 0.3, 1, 4))
    run_shots(g, t, L, d, [a, b, c_])


# ================================================================ 13 fon
def framed_grandma(g, x, y, sc, t):
    with g.at(x, y, sc):
        _rr(g.c, -230, -290, 460, 580, 10)
        _shade(g.c, WOOD2, 3, 0.2)
        grandma_photo(g, 0, 0, 1.0, t, 1.0, False, True)
        for k in range(8):
            g.circle(-200 + k * 57, -290, 14, WHITE, 2)


def s_fon(g, t, L, d):
    def a(g, t, lt):
        shop(g, "day")
        x = lerp(1900, 1250, slide(lt, 0, 1, 2.5))
        person(g, x, 1180, FON, 0.82, mood="sad", pose="down", turn=-0.5, seed=4)
        person(g, 520, 1220, PETE, 0.84, mood="neutral", pose="hold", turn=0.5, seed=1)

    def b(g, t, lt):   # ใบหน้าฝน ตาบวม
        shop(g, "day", 1.4, 1300, 500)
        shoulders(g, FON, CX, 600, 3.3)
        with g.at(CX, 600, 3.3):
            head(g, FON, "sad", 0.0, -0.2, (0, 0.2), 4)
            for sx in (-1, 1):
                g.blob(sx * 22, -6, 16, 7, (0.85, 0.45, 0.45, 0.5), 0, sx)

    def c_(g, t, lt):   # ยื่นกรอบรูป
        shop(g, "day", 1.2, CX, 600)
        framed_grandma(g, CX, 560, 0.9, t)
        for sx in (-1, 1):
            g.blob(CX + sx * 250, 760, 70, 50, PETE.skin, 3, sx)

    def d_(g, t, lt):   # ร้องไห้โฮ
        shop(g, "day")
        person(g, 1150, 1180, FON, 0.85, mood="sad", pose="hold", turn=-0.3, seed=4)
        framed_grandma(g, 1150, 760, 0.42, t)
        person(g, 560, 1220, PETE, 0.84, mood="worry", pose="down", turn=0.5, seed=1)

    def e(g, t, lt):   # ฝนพูด (ใกล้)
        shop(g, "day", 1.5, 1200, 500)
        shoulders(g, FON, 900, 620, 3.0)
        with g.at(900, 620, 3.0):
            head(g, FON, "sad", 0.5 * max(0, math.sin(t * 7)), -0.3, (0.3, 0.2), 4)
            for k in range(2):
                y = (t * 40 + k * 30) % 60
                g.blob(-24, 10 + y, 5, 8, (0.7, 0.85, 0.95, 0.8), 0, k)

    def f(g, t, lt):   # รูปเปียกน้ำท่วม (ภาพย้อน)
        fill_rect(g.c, -800, -800, W + 1600, H + 1600, hexc("#5a6a72"))
        fill_rect(g.c, -800, 700, W + 1600, 800, (0.45, 0.55, 0.6, 0.9))
        with g.at(CX, 700, 1.0, 12 * math.sin(t)):
            grandma_photo(g, 0, 0, 0.9, t, 0.0)
        fill_rect(g.c, -800, 760 + 10 * math.sin(t * 2), W + 1600, 800, (0.4, 0.5, 0.55, 0.5))

    def h(g, t, lt):   # รูปคุณยาย (ยิ้ม) เต็มจอ
        shop(g, "day", 1.3)
        framed_grandma(g, CX, 540, 1.3 + 0.03 * lt, t)
    run_shots(g, t, L, d, [a, b, c_, d_, e, f, h])


# ================================================================ 14 reflect
def s_reflect(g, t, L, d):
    def a(g, t, lt):
        ext(g, "day")
        person(g, 1050, 1060, PETE, 0.5, mood="neutral", pose="down", turn=-0.6, seed=1)

    def b(g, t, lt):   # ศาลาสวดศพ รูปคุณยายบนโต๊ะหมู่
        bg(g, "sala", set_temple_sala)
        framed_grandma(g, 960, 360, 0.42, t)

    def c_(g, t, lt):
        bg(g, "sala", set_temple_sala, 1.6, 960, 400)
        framed_grandma(g, 960, 500, 0.7, t)

    def d_(g, t, lt):
        ext(g, "day", 1.5, 1000, 700)
        shoulders(g, PETE, 960, 560, 3.0)
        with g.at(960, 560, 3.0):
            head(g, PETE, "smile", 0.0, -0.3, (-0.5, 0), 1)

    def e(g, t, lt):   # เงารูปบนผนังร้าน
        shop(g, "night", 1.3, 600, 300)
        darken(g, 0.45)
        vignette(g, 0.7)
    run_shots(g, t, L, d, [a, b, c_, d_, e])


# ================================================================ 15 envelope
def s_envelope(g, t, L, d):
    def a(g, t, lt):
        ws(g, "night")
        darken(g, 0.4)
        wall_clock(g, CX, 520, 300, 0, 40)

    def b(g, t, lt):   # ซองไถเข้ามาใต้ประตู
        shop(g, "night", 1.5, 1300, 900)
        darken(g, 0.5)
        fill_rect(g.c, 300, 960, 1500, 14, (0.95, 0.85, 0.6, 0.8))
        envelope(g, lerp(1300, 900, slide(lt, 0, 1, 1.2)), 1010, 1.0, 4)

    def c_(g, t, lt):   # เท้าลงบันได
        fill_rect(g.c, -800, -800, W + 1600, H + 1600, hexc("#1c1814"))
        for k in range(5):
            y = 300 + k * 160
            fill_rect(g.c, 200 + k * 80, y, 1300, 50, WOOD3)
            fill_rect(g.c, 200 + k * 80, y + 50, 1300, 110, WOOD2)
        envelope(g, 1500, 1040, 0.8, 6)
        vignette(g, 0.65)

    def d_(g, t, lt):   # ช่องแสงใต้ประตู ไม่มีเงาคน
        fill_rect(g.c, -800, -800, W + 1600, H + 1600, hexc("#12100e"))
        for k in range(8):
            fill_rect(g.c, 100 + k * 220, 100, 210, 780, hexc("#3a2e24"))
        fill_rect(g.c, -100, 880, 2200, 26, (0.95, 0.85, 0.6, 0.9))
        glow(g, CX, 900, 900, LAMP, 0.15)
        vignette(g, 0.6)
    run_shots(g, t, L, d, [a, b, c_, d_])


# ================================================================ 16 keng
def s_keng(g, t, L, d):
    def table(g):
        fill_rect(g.c, -800, -800, W + 1600, H + 1600, hexc("#3a2c20"))
        glow(g, CX, CY, 900, LAMP, 0.3)

    def a(g, t, lt):
        table(g)
        envelope(g, 400, 760, 1.2, -10, True)
        id_card(g, CX + 120, 520, 1.25 * pop(lt, 0.0, 0.4), t)

    def b(g, t, lt):   # ธนบัตรเปียก น้ำหยด
        table(g)
        for k in range(3):
            banknote(g, 760 + k * 160, 560 + k * 40, 1.6, -8 + k * 8)
        y = 300 + (lt * 260) % 500
        g.blob(1240, y, 10, 14, (0.6, 0.8, 0.95, 0.8), 0, 2)
        g.blob(1240, 820, 80, 20, (0.4, 0.5, 0.6, 0.35), 0, 3)

    def c_(g, t, lt):   # โน้ต
        table(g)
        with g.at(CX, 540, 1.3, 3):
            _rr(g.c, -360, -220, 720, 440, 6)
            _shade(g.c, hexc("#f0ead8"), 3, 0.1)
            for k in range(4):
                _stroke(g.c, [(-300, -120 + k * 80), (300, -120 + k * 80)], 2, hexc("#9ab0c9"), 1.0)

    def d_(g, t, lt):
        c_(g, t, lt)
        with g.at(CX, 540, 1.3, 3):
            g.text("ช่วยลบรอยช้ำบนหน้าให้หน่อย", 0, -90, 40, "kanitm", hexc("#2a3a6a"))
            g.text("พรุ่งนี้จะเอาไปตั้งงานศพ", 0, -10, 40, "kanitm", hexc("#2a3a6a"))

    def e(g, t, lt):   # พีทลังเล มองประตู
        desk_scene(g, t, None, "worry", look=(-1, 0.3), lit_incense=False)

    def f(g, t, lt):   # นึกถึงค่ายาแม่
        table(g)
        for k in range(3):
            banknote(g, 700 + k * 160, 560, 1.4, -8 + k * 8)
        with g.at(1380, 560, 1.0):
            _rr(g.c, -110, -170, 220, 340, 20)
            _shade(g.c, WHITE, 3, 0.1)
            g.text("ยา", 0, -40, 60, "kanit", hexc("#3a6a9a"))
            for k in range(3):
                g.circle(-50 + k * 50, 80, 18, hexc("#e9c4c4"), 2)
    run_shots(g, t, L, d, [a, b, c_, d_, e, f])


# ================================================================ 17 incense
def s_incense(g, t, L, d):
    def a(g, t, lt):
        desk_scene(g, t, keng_screen(t), "neutral", pose="hold", burn=0.1)

    def b(g, t, lt):
        monitor_close(g, t, keng_screen(t, 1.0), 2.1)

    def c_(g, t, lt):   # เกือบหลุดปาก
        ws(g, "night")
        darken(g, 0.35)
        shoulders(g, PETE, CX, 600, 3.6)
        with g.at(CX, 600, 3.6):
            head(g, PETE, "shock", 0.8, 0.2, (0.6, 0), 1)

    def d_(g, t, lt):   # ปิดปากตัวเอง
        ws(g, "night")
        darken(g, 0.35)
        shoulders(g, PETE, CX, 600, 3.6)
        with g.at(CX, 600, 3.6):
            head(g, PETE, "worry", 0.0, 0.2, (0.6, 0), 1)
        g.blob(CX + 40, 720, 130, 80, PETE.skin, 3, 2)

    def e(g, t, lt):   # ธูปไหม้เร็วผิดปกติ
        ws(g, "night")
        darken(g, 0.55)
        incense(g, CX, 960, t * 2.5, True, slide(lt, 0.1, 0.9, 3.0), 3.2)
        glow(g, CX, 500, 500, (1, 0.5, 0.3, 1), 0.1)
    run_shots(g, t, L, d, [a, b, c_, d_, e])


# ================================================================ 18 zoom
def s_zoom(g, t, L, d):
    def a(g, t, lt):
        monitor_close(g, t, keng_screen(t, 1.0, 0.38 + 0.1 * slide(lt)), 2.1)

    def b(g, t, lt):   # 200 → 500 → 1000%
        k = min(int(lt / 0.9), 2)
        lab = ("200%", "500%", "1000%")[k]
        sc = (0.6, 0.9, 1.3)[k]
        monitor_close(g, t, eye_screen((0, 0), False, None, 0.0, lab) if k == 2 else keng_screen(t, 1.0, sc, lab), 2.1)

    def c_(g, t, lt):   # ดวงตาเป็นพิกเซล
        fill_rect(g.c, -800, -800, W + 1600, H + 1600, hexc("#0c1014"))
        big_eye(g, CX, CY, 1.3, (0, 0), False)
        c = g.c
        c.set_source_rgba(0, 0, 0, 0.12)
        c.set_line_width(2)
        for k in range(0, W, 40):
            c.move_to(k, 0)
            c.line_to(k, H)
        for k in range(0, H, 40):
            c.move_to(0, k)
            c.line_to(W, k)
        c.stroke()

    def d_(g, t, lt):   # เงาสะท้อนเล็ก ๆ ในกระจกตา
        fill_rect(g.c, -800, -800, W + 1600, H + 1600, hexc("#0c1014"))
        big_eye(g, CX, CY, 1.3 + 0.3 * slide(lt), (0, 0), False,
                lambda g3, ix, iy: killer_reflection(g3, ix, iy, 0.35, 0.0))

    def e(g, t, lt):   # พีทโน้มเข้าหาจอ
        ws(g, "night")
        darken(g, 0.5)
        glow(g, 1300, 560, 600, (0.66, 0.84, 0.9, 1), 0.3)
        with g.at(lerp(860, 1000, slide(lt)), 600, 3.8):
            head(g, PETE, "worry", 0.0, 0.7, (1, 0), 1)
    run_shots(g, t, L, d, [a, b, c_, d_, e])


# ================================================================ 19 reflection
def s_reflection(g, t, L, d):
    def iris_k(g, t, lt, sc, raise_k, sharp):
        fill_rect(g.c, -800, -800, W + 1600, H + 1600, hexc("#0c1014"))
        big_eye(g, CX, CY, sc, (0, 0), False, lambda g3, ix, iy: killer_reflection(g3, ix, iy, 0.5, raise_k))
        if sharp < 1:
            darken(g, 0.4 * (1 - sharp))

    def a(g, t, lt):   # แถบความคมชัด
        iris_k(g, t, lt, 1.8, 0.0, slide(lt, 0.2, 0.6))
        with g.at(CX, 980):
            _rr(g.c, -400, -14, 800, 28, 14)
            _shade(g.c, hexc("#c9c9c4"), 2, 0.1)
            g.circle(-400 + 800 * slide(lt, 0.2, 0.8, 3), 0, 26, WHITE, 3)

    def b(g, t, lt):
        iris_k(g, t, lt, 2.6, 0.0, slide(lt, 0.6, 1.0))

    def c_(g, t, lt):   # ภาพในตาเต็มจอ: ชายเสื้อกั๊กส้ม
        bg(g, "road", set_road_night)
        person(g, 900, 1150, KILLER, 0.95, mood="angry", pose="down", turn=-0.3, seed=6)
        vest(g, 900, 1150, 0.95)
        darken(g, 0.2)
        vignette(g, 0.7)

    def d_(g, t, lt):   # เงื้อท่อนเหล็ก (ค้างก่อนลงมือ)
        bg(g, "road", set_road_night)
        k = slide(lt, 0, 1, 1.5)
        person(g, 900, 1150, KILLER, 0.95, mood="angry", pose="down", pose2="v", k=k, turn=-0.3, seed=6)
        vest(g, 900, 1150, 0.95)
        pipe(g, 980, lerp(900, 320, k), 1.3, 20)
        darken(g, 0.25)
        vignette(g, 0.75)

    def e(g, t, lt):   # หน้าพีทช็อก
        ws(g, "night")
        darken(g, 0.5)
        shoulders(g, PETE, CX, 600, 3.8)
        with g.at(CX, 600, 3.8):
            head(g, PETE, "shock", 0.0, 0.0, (0, 0), 1)
    run_shots(g, t, L, d, [a, b, c_, d_, e])


# ================================================================ 20 news
def news_screen(highlight=False):
    def scr(g2):
        c = g2.c
        fill_rect(c, -96, -196, 192, 392, WHITE)
        fill_rect(c, -96, -196, 192, 40, hexc("#b23a2a"))
        g2.text("ข่าวท้องถิ่น", 0, -176, 18, "kanit", WHITE)
        g2.text("หนุ่มขี่มอเตอร์ไซค์ล้ม", 0, -130, 16, "kanit", INK)
        g2.text("หัวฟาดขอบถนน", 0, -108, 16, "kanit", INK)
        fill_rect(c, -86, -90, 172, 140, hexc("#2a3038"))
        _rr(c, -60, 20, 90, 20, 6)
        _shade(c, WHITE, 1, 0.1)
        with g2.at(40, 45, 0.11):
            person(g2, 0, 0, KILLER, 1.0, mood="neutral", pose="down", seed=6, shadow=False)
            vest(g2, 0, 0, 1.0)
        if highlight:
            c.set_source_rgba(0.9, 0.2, 0.2, 1)
            c.set_line_width(4)
            c.arc(40, -20, 34, 0, 2 * math.pi)
            c.stroke()
        for k in range(4):
            _stroke(c, [(-80, 80 + k * 22), (80, 80 + k * 22)], 6, hexc("#c9c9c4"), 1.0)
    return scr


def s_news(g, t, L, d):
    def a(g, t, lt):
        ws(g, "night")
        darken(g, 0.5)

        def scr(g2):
            fill_rect(g2.c, -96, -196, 192, 392, WHITE)
            _rr(g2.c, -86, -180, 172, 40, 20)
            _shade(g2.c, hexc("#eeeeee"), 2, 0.05)
            g2.text("เก่ง"[: max(1, int(lt * 3))], -40, -160, 20, "kanitm", INK, anchor="l")
        phone(g, CX, 580, 1.7, -3, scr)

    def b(g, t, lt):
        ws(g, "night")
        darken(g, 0.5)
        phone(g, CX, 580 - 60 * slide(lt), 1.7, -3, news_screen())

    def c_(g, t, lt):
        ws(g, "night")
        darken(g, 0.55)
        phone(g, CX, 640, 2.4, 0, news_screen(), hand=False)

    def d_(g, t, lt):   # รูปประกอบข่าว เต็มจอ
        bg(g, "road", set_road_night)
        _rr(g.c, 380, 760, 620, 90, 40)
        _shade(g.c, WHITE, 3, 0.1)
        person(g, 1350, 1100, KILLER, 0.8, mood="neutral", pose="down", turn=-0.4, seed=6)
        vest(g, 1350, 1100, 0.8)

    def e(g, t, lt):   # เทียบภาพ
        fill_rect(g.c, -800, -800, W + 1600, H + 1600, hexc("#0c1014"))
        with g.at(520, CY):
            phone(g, 0, 0, 1.8, 0, news_screen(True), hand=False)
        big_eye(g, 1400, CY, 0.75, (0, 0), False, lambda g3, ix, iy: killer_reflection(g3, ix, iy, 0.5, 0.0))

    def f(g, t, lt):
        d_(g, t, lt)
        with g.at(1350, 1100 - 0.8 * 830, 1.0):
            g.c.set_source_rgba(0.9, 0.2, 0.2, pop(lt, 0.3))
            g.c.set_line_width(8)
            g.c.arc(0, 0, 120, 0, 2 * math.pi)
            g.c.stroke()
    run_shots(g, t, L, d, [a, b, c_, d_, e, f])


# ================================================================ 21 call
def s_call(g, t, L, d):
    def pete_side(g, t, mood="worry"):
        ws(g, "night")
        darken(g, 0.4)
        shoulders(g, PETE, 860, 620, 3.2)
        with g.at(860, 620, 3.2):
            head(g, PETE, mood, 0.0, 0.3, (0.4, 0), 1)
        phone(g, 1130, 650, 0.9, 20, None, hand=True)

    def killer_side(g, t):
        bg(g, "station", set_station)
        darken(g, 0.3)
        shoulders(g, KILLER, 960, 600, 3.0)
        with g.at(960, 600, 3.0):
            head(g, KILLER, "smug", 0.4 * max(0, math.sin(t * 6)), -0.4, (-0.3, 0), 6)
        darken(g, 0.0)
        vignette(g, 0.7)

    def a(g, t, lt):
        pete_side(g, t, "sad")

    def b(g, t, lt):
        pete_side(g, t, "worry")

    def c_(g, t, lt):   # แบ่งจอ
        c = g.c
        c.save()
        c.rectangle(-800, -800, CX + 800, H + 1600)
        c.clip()
        with g.at(-480, 0):
            pete_side(g, t)
        c.restore()
        c.save()
        c.rectangle(CX, -800, CX + 800, H + 1600)
        c.clip()
        with g.at(480, 0):
            bg(g, "station", set_station)
            darken(g, 0.4)
            g.blob(900, 640, 150, 110, KILLER.skin, 3, 2)
            phone(g, 900, 560, 0.9, -15, None, hand=False)
        c.restore()
        fill_rect(c, CX - 4, -800, 8, H + 1600, (0, 0, 0, 1))

    def d_(g, t, lt):
        killer_side(g, t)

    def e(g, t, lt):   # วางสาย มือสั่น
        ws(g, "night")
        darken(g, 0.5)
        phone(g, CX + 6 * math.sin(t * 40), 600, 1.6, 10, lambda g2: fill_rect(g2.c, -96, -196, 192, 392, hexc("#2a2a2a")))

    def f(g, t, lt):
        pete_side(g, t, "shock")
    run_shots(g, t, L, d, [a, b, c_, d_, e, f])


# ================================================================ 22 night3
def stairwell(g, t, light=0.0):
    ws(g, "night")
    darken(g, 0.5)
    if light > 0:
        glow(g, 1700, 1000, 500 * light, ORANGE, 0.35 * light)


def s_night3(g, t, L, d):
    def a(g, t, lt):
        ws(g, "night")
        darken(g, 0.4)
        wall_clock(g, CX, 520, 300, 1, 30)

    def b(g, t, lt):   # ก๊อปไฟล์ลงแฟลชไดรฟ์
        def scr(g2):
            fill_rect(g2.c, -230, -370, 460, 290, hexc("#d6d6d2"))
            g2.text("กำลังคัดลอก...", 0, -260, 30, "kanitm", INK)
            _rr(g2.c, -180, -210, 360, 30, 6)
            _shade(g2.c, WHITE, 2, 0.1)
            fill_rect(g2.c, -178, -208, 356 * min(lt / 3.0, 1), 26, hexc("#3a6ab0"))
        monitor_close(g, t, scr, 2.1)

    def c_(g, t, lt):
        ws(g, "night")
        darken(g, 0.4)
        big_hand = PETE.skin
        g.blob(CX, 640, 160, 110, big_hand, 3, 2)
        usb(g, CX + 40, 520, 2.4, 10)

    def d_(g, t, lt):   # ช่องบันไดมืด
        stairwell(g, t, 0.0)
        desk_scene(g, t, keng_screen(t), "neutral", look=(-1, 0.3))
        darken(g, 0.25)

    def e(g, t, lt):   # เอี๊ยด — แสงไฟฉายไต่ขึ้น
        ws(g, "night")
        darken(g, 0.55)
        glow(g, 1700, 1100 - 300 * slide(lt), 500, ORANGE, 0.3)
        vignette(g, 0.7)

    def f(g, t, lt):   # พีทหันขวับ
        ws(g, "night")
        darken(g, 0.45)
        glow(g, 1700, 800, 500, ORANGE, 0.3)
        shoulders(g, PETE, 860, 600, 3.6)
        with g.at(860, 600, 3.6):
            head(g, PETE, "shock", 0.0, 0.8, (1, 0.3), 1)
    run_shots(g, t, L, d, [a, b, c_, d_, e, f])


# ================================================================ 23 bang
def door_shake(g, t, k, light=1.0, shadow_feet=True):
    ws(g, "night")
    darken(g, 0.45)
    sh = 10 * k * math.sin(t * 70)
    for i in range(5):
        fill_rect(g.c, 640 + sh + i * 130, 160, 124, 880, WOOD3)
    g.circle(1240 + sh, 600, 16, GOLD, 3)
    fill_rect(g.c, 600, 1030, 720, 16, (0.95, 0.6, 0.3, 0.8 * light))
    if shadow_feet:
        for x in (840, 1020):
            fill_rect(g.c, x, 1030, 90, 16, (0.05, 0.05, 0.05, 1))


def s_bang(g, t, L, d):
    def a(g, t, lt):   # ลากโต๊ะดันประตู
        door_shake(g, t, 0.0, 0.0, False)
        x = lerp(200, 700, slide(lt, 0, 1, 2.0))
        person(g, x - 200, 1250, PETE, 0.8, mood="worry", pose="hold", turn=0.8, seed=1, lean=10)
        desk(g, x + 200, 860, 500)

    def b(g, t, lt):   # ปัง ปัง ปัง
        k = max(0.0, math.sin(lt * 9)) ** 4
        door_shake(g, t, k)
        desk(g, 950, 860, 600)

    def c_(g, t, lt):   # เสียงตะโกน + เงาเท้า
        door_shake(g, t, max(0.0, math.sin(lt * 7)) ** 6, 1.0, True)
        darken(g, 0.1)

    def d_(g, t, lt):   # พีทนึกถึงกฎข้อสาม
        ws(g, "night")
        darken(g, 0.5)
        shoulders(g, PETE, 800, 600, 3.2)
        with g.at(800, 600, 3.2):
            head(g, PETE, "worry", 0.0, 0.4, (0.6, 0), 1)
        fingers(g, 1400, 560, 3, 1.2, MUN.skin)

    def e(g, t, lt):
        door_shake(g, t, 0.2, 1.0, True)
        person(g, 500, 1250, PETE, 0.8, mood="shock", pose="stop", turn=0.7, seed=1)
    run_shots(g, t, L, d, [a, b, c_, d_, e])


# ================================================================ 24 crowbar
def s_crowbar(g, t, L, d):
    def a(g, t, lt):   # กด 191
        ws(g, "night")
        darken(g, 0.5)

        def scr(g2):
            fill_rect(g2.c, -96, -196, 192, 392, hexc("#1d1f22"))
            g2.text("191"[: 1 + int(lt * 1.5) % 3], 0, -120, 46, "kanit", WHITE)
            for r in range(4):
                for q in range(3):
                    g2.circle(-60 + q * 60, -30 + r * 55, 22, hexc("#3a3c40"), 0)
        phone(g, CX + 5 * math.sin(t * 40), 580, 1.7, 0, scr)

    def b(g, t, lt):   # เงียบ
        door_shake(g, t, 0.0, 1.0, True)
        darken(g, 0.2)

    def c_(g, t, lt):   # ชะแลงงัดร่องประตู
        door_shake(g, t, 0.15, 1.0, True)
        crowbar(g, 1225, 640 - 40 * math.sin(t * 6), 1.0, 8)

    def d_(g, t, lt):
        door_shake(g, t, 0.4, 1.0, True)
        crowbar(g, 1225, 620, 1.0, 14)
        darken(g, 0.1)

    def e(g, t, lt):   # ประตูแตก
        ws(g, "night")
        darken(g, 0.4)
        k = e_out(min(lt / 0.4, 1))
        for i in range(5):
            with g.at(640 + i * 130 + 62, 600, 1.0, (i - 2) * 18 * k):
                fill_rect(g.c, -62, -440, 124, 880, WOOD3)
        glow(g, 960, 600, 600, ORANGE, 0.4 * k)
        for i in range(10):
            g.poly([(0, 0), (40, 10), (10, 40)], WOOD3, 2, amp=0) if False else None
            with g.at(960 + 600 * hn(i, 2) * k, 600 + 300 * hn(i, 3) * k, 1.0, 90 * hn(i, 4) * k):
                g.poly([(0, 0), (50, 10), (16, 46)], WOOD3, 2, amp=0)
        desk(g, 960 + 500 * k, 860 + 100 * k, 600)
    run_shots(g, t, L, d, [a, b, c_, d_, e])


# ================================================================ 25 knife
def s_knife(g, t, L, d):
    def a(g, t, lt):   # ร่างใหญ่บังประตู
        ws(g, "night")
        darken(g, 0.4)
        glow(g, 1100, 400, 700, ORANGE, 0.35)
        with g.silhouette((0.05, 0.05, 0.06, 1), 1.0):
            person(g, 1100, 1350, KILLER, 1.25, mood="angry", pose="down", turn=-0.2, seed=6)
        vignette(g, 0.6)

    def b(g, t, lt):   # มีดสะท้อนแสงจอ
        ws(g, "night")
        darken(g, 0.6)
        knife(g, CX, 640, 3.0, -30)
        glow(g, CX + 40, 420, 120, (0.7, 0.9, 1.0, 1), 0.6)

    def c_(g, t, lt):   # พีทถอยชนกล้องโบราณ
        ws(g, "night")
        darken(g, 0.3)
        camera_antique(g, 380, 1150, 1.0)
        person(g, 640, 1250, PETE, 0.85, mood="shock", pose="stop", turn=0.7, seed=1, lean=-6)
        person(g, 1450, 1300, KILLER, 0.95, mood="angry", pose="down", turn=-0.6, seed=6)
        vest(g, 1450, 1300, 0.95)

    def d_(g, t, lt):   # เงื้อมีด (ค้าง)
        ws(g, "night")
        darken(g, 0.35)
        k = slide(lt, 0, 1, 1.2)
        person(g, 1200, 1350, KILLER, 1.15, mood="angry", pose="down", pose2="v", k=k, turn=-0.4, seed=6)
        vest(g, 1200, 1350, 1.15)
        knife(g, 1200 + 240 * 1.15 * 0.0 + 260, lerp(980, 420, k), 1.4, 20)
        vignette(g, 0.7)
    run_shots(g, t, L, d, [a, b, c_, d_])


# ================================================================ 26 flash
def keng_ghost(g, x, y, sc, a=0.85, turn=0.0):
    with g.alpha(a):
        person(g, x, y, KENG, sc, mood="sad", pose="shrug", turn=turn, seed=3)
        with g.at(x, y, sc):
            g.blob(-30, -560, 70, 120, (0.5, 0.15, 0.15, 0.35), 0, 3)
            g.blob(20, -470, 50, 60, (0.5, 0.15, 0.15, 0.3), 0, 4)
    glow(g, x, y - 400 * sc, 500 * sc, (0.85, 0.95, 1.0, 1), 0.25 * a)


def s_flash(g, t, L, d):
    def a(g, t, lt):   # แฟลชระเบิด
        ws(g, "night")
        camera_antique(g, CX, 1350, 1.5, flash=max(0.0, 1 - lt / 0.6))
        fill_rect(g.c, -800, -800, W + 1600, H + 1600, (1, 1, 0.97, max(0.0, 1 - lt / 0.5)))

    def b(g, t, lt):
        ws(g, "night")
        camera_antique(g, 600, 1200, 1.2, flash=0.6 + 0.3 * math.sin(t * 20))
        fill_rect(g.c, -800, -800, W + 1600, H + 1600, (1, 1, 0.97, 0.35))

    def c_(g, t, lt):   # ขาวโพลน
        fill_rect(g.c, -800, -800, W + 1600, H + 1600, hexc("#f2f2ee"))
        with g.silhouette((0.75, 0.75, 0.72, 1), 0.6):
            camera_antique(g, 380, 1150, 1.0)

    def d_(g, t, lt):   # เงาเก่งยืนขวาง
        fill_rect(g.c, -800, -800, W + 1600, H + 1600, hexc("#e6e6e0"))
        with g.silhouette((0.55, 0.55, 0.52, 1), 0.7):
            person(g, 1500, 1300, KILLER, 0.95, mood="angry", pose="stop", turn=-0.6, seed=6)
        keng_ghost(g, CX, 1250, 0.95, fade_k(lt))

    def e(g, t, lt):   # เสื้อขาวเปื้อน
        fill_rect(g.c, -800, -800, W + 1600, H + 1600, hexc("#d6d6d0"))
        keng_ghost(g, CX, 1700, 1.6, 0.9)

    def f(g, t, lt):   # หน้าเก่งหันมามอง (เศร้า)
        fill_rect(g.c, -800, -800, W + 1600, H + 1600, hexc("#c9cdd0"))
        glow(g, CX, 560, 700, WHITE, 0.4)
        with g.alpha(0.9):
            shoulders(g, KENG, CX, 600, 3.4)
            with g.at(CX, 600, 3.4):
                head(g, KENG, "sad", 0.0, 0.3, (0.4, 0), 3)
    run_shots(g, t, L, d, [a, b, c_, d_, e, f])


def fade_k(lt, dur=0.8):
    return e_io(min(lt / dur, 1.0))


# ================================================================ 27 fall
def stairs_down(g):
    c = g.c
    fill_rect(c, -800, -800, W + 1600, H + 1600, hexc("#1e1914"))
    for k in range(8):
        x = 300 + k * 140
        y = 160 + k * 120
        fill_rect(c, x, y, 900, 40, WOOD3)
        fill_rect(c, x, y + 40, 900, 80, WOOD2)


def s_fall(g, t, L, d):
    def a(g, t, lt):   # ร้องลั่น ยกแขนบังตา
        ws(g, "night")
        darken(g, 0.2)
        fill_rect(g.c, -800, -800, W + 1600, H + 1600, (1, 1, 0.95, max(0.0, 0.5 - lt * 0.2)))
        x = lerp(1100, 1450, slide(lt, 0, 1, 2.5))
        person(g, x, 1300, KILLER, 1.0, mood="shout", pose="think", turn=-0.5, seed=6, lean=-8)
        vest(g, x, 1300, 1.0)

    def b(g, t, lt):   # ส้นเท้าพลาดขอบบันได
        bg(g, "stairs", stairs_down)
        darken(g, 0.2)
        k = slide(lt, 0, 1, 1.6)
        person(g, 560, 640, KILLER, 0.6, mood="shout", pose="think", turn=0.3, seed=6, lean=lerp(0, -25, k))
        vest(g, 560, 640, 0.6)

    def c_(g, t, lt):   # ร่วงลงบันได (เงาบนผนัง)
        bg(g, "stairs", stairs_down)
        darken(g, 0.4)
        k = slide(lt, 0, 1, 1.2)
        with g.silhouette((0.02, 0.02, 0.02, 1), 0.7):
            person(g, lerp(500, 1300, k), lerp(500, 1150, k), KILLER, 0.7, pose="v", lean=lerp(0, 120, k), seed=6)

    def d_(g, t, lt):   # เงียบ
        bg(g, "stairs", stairs_down)
        darken(g, 0.6)
        vignette(g, 0.8)

    def e(g, t, lt):   # ไซเรน
        ext(g, "night")
        r = 0.5 + 0.5 * math.sin(t * 7)
        glow(g, 300, 700, 900, (0.95, 0.2, 0.2, 1), 0.3 * r)
        glow(g, 1700, 700, 900, (0.2, 0.35, 0.95, 1), 0.3 * (1 - r))

    def f(g, t, lt):   # ตำรวจใส่กุญแจมือ
        shop(g, "night")
        darken(g, 0.3)
        r = 0.5 + 0.5 * math.sin(t * 7)
        glow(g, 1600, 500, 900, (0.95, 0.2, 0.2, 1), 0.2 * r)
        glow(g, 300, 500, 900, (0.2, 0.35, 0.95, 1), 0.2 * (1 - r))
        person(g, 1250, 900, KILLER, 0.55, mood="sad", pose="down", lean=-90, seed=6, shadow=False)
        person(g, 1300, 1150, POLICE, 0.75, mood="firm", pose="hold", turn=-0.5, seed=8)
        person(g, 500, 1150, POLICE, 0.75, mood="firm", pose="point", turn=0.5, seed=9)

    def h(g, t, lt):   # แฟลชไดรฟ์ = หลักฐาน
        shop(g, "night", 1.3)
        darken(g, 0.3)
        g.blob(CX - 60, 620, 160, 110, PETE.skin, 3, 2)
        usb(g, CX, 520, 2.6, -8)
        g.blob(CX + 200, 470, 140, 100, POLICE.skin, 3, 4)
    run_shots(g, t, L, d, [a, b, c_, d_, e, f, h])


# ================================================================ 28 ending
def s_ending(g, t, L, d):
    def a(g, t, lt):   # แม่หลังผ่าตัด (สว่าง อบอุ่น)
        bg(g, "hosp", set_hospital)
        glow(g, 1500, 200, 900, hexc("#fff2c9"), 0.35)
        with g.at(700, 760):
            bed(g, 0, 200, 1.1)
            shoulders(g, MOTHER, -300, -40, 2.0)
            with g.at(-300, -40, 2.0):
                head(g, MOTHER, "smile", 0.0, 0.5, (0.6, 0), 3)
        person(g, 1350, 1250, PETE, 0.85, mood="smile", pose="hold", turn=-0.7, seed=1)

    def b(g, t, lt):
        bg(g, "hosp", set_hospital, 1.4, 700, 500)
        monitor_heart(g, 1300, 520, t * 0.8, 1.6)
        shoulders(g, MOTHER, 700, 620, 2.6)
        with g.at(700, 620, 2.6):
            head(g, MOTHER, "smile", 0.4 * max(0, math.sin(t * 7)), 0.3, (0.5, 0), 3)

    def c_(g, t, lt):   # พีทเปิดร้าน
        ext(g, "day")
        person(g, 1180, 1060, PETE, 0.5, mood="smile", pose="wave", turn=-0.2, seed=1)

    def d_(g, t, lt):   # ผนังร้าน: รูปคุณยาย + เก่ง
        shop(g, "day", 1.3, 700, 400)
        framed_grandma(g, 700, 500, 0.6, t)
        with g.at(1250, 500, 0.6):
            _rr(g.c, -230, -290, 460, 580, 10)
            _shade(g.c, WOOD2, 3, 0.2)
            keng_face(g, 0, 0, 0.82, t, 0.0, "smile")

    def e(g, t, lt):   # เย็น ชั้นสอง โทรศัพท์ดัง
        ws(g, "dusk")
        glow(g, 1500, 300, 800, hexc("#f2a76a"), 0.3)
        person(g, 640, 1180, PETE, 0.78, mood="neutral", pose="phone", turn=0.6, seed=1)
        desk(g, 1000, 880, 1300)
        crt(g, 1150, 880, 0.75, None)

    def f(g, t, lt):   # ลุงมั่นในโรงพยาบาล
        bg(g, "hosp", set_hospital, 1.3, 1200, 500)
        shoulders(g, MUN, 960, 600, 3.2)
        with g.at(960, 600, 3.2):
            head(g, MUN, "worry", 0.6 * max(0, math.sin(t * 8)), 0.2, (0.3, 0), 2)
        phone(g, 1260, 640, 0.8, 20, None, hand=False)

    def h(g, t, lt):   # เคสคอมเปิดข้าง ช่องฮาร์ดดิสก์ว่าง หยากไย่
        ws(g, "dusk")
        darken(g, 0.4)
        c = g.c
        with g.at(CX, 560, 1.6):
            _rr(c, -260, -320, 520, 640, 14)
            _shade(c, hexc("#ddd4bd"), 3, 0.25)
            fill_rect(c, -230, -290, 460, 580, hexc("#2a2826"))
            _rr(c, -150, -200, 300, 80, 6)
            _shade(c, hexc("#3a3836"), 2, 0.1)
            g.text("ว่าง", 0, -160, 30, "kanitm", hexc("#7a7a74"))
            for k in range(6):
                _stroke(c, [(-230, -290), (-230 + 60 * k, -100 + 30 * k)], 1.5, (0.9, 0.9, 0.9, 1), 0.4)

    def i_(g, t, lt):   # หน้าพีทซีด
        ws(g, "dusk")
        darken(g, 0.5)
        shoulders(g, PETE, CX, 600, 3.6)
        with g.at(CX, 600, 3.6):
            head(g, PETE, "shock", 0.0, 0.0, (0, 0), 1)

    def j(g, t, lt):   # จอยังสว่าง... ไฟล์ใหม่เปิดเอง แล้วตัดดำ
        ws(g, "night")
        darken(g, 0.55)

        def scr(g2):
            editor_ui(g2, lambda g3: fill_rect(g3.c, -180, -340, 400, 250, hexc("#e9e9e4")))
        crt(g, CX, 1000, 2.1, scr)
        te = 4.5
        if lt > te:   # ตัดดำ + ชื่อเรื่อง
            darken(g, min((lt - te) / 0.3, 1.0), (0, 0, 0))
            g.text("รับจ้างซ่อมรูปถ่ายหน้าศพ", CX, CY, 84, "kanit", hexc("#e9e4d6"), pop(lt, te + 0.5, 0.5))
    run_shots(g, t, L, d, [a, b, c_, d_, e, f, h, i_, j])


SCENES = {n: globals()["s_" + n] for n in _names}
