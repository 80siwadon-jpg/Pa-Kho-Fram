"""ฉากตอน class_photo: เจริญศิลป์โฟโต้ ตอน 2 — รูปหมู่ที่เกินมาหนึ่งคน (1 ช็อตต่อ 1 บรรทัด)"""
import importlib.util
import math
import os
import sys

import cairo

sys.path.insert(0, os.path.dirname(__file__))
import chars as C  # noqa: E402

_FPS = os.path.join(os.path.dirname(__file__), "..", "funeral_photo", "scenes.py")
_spec = importlib.util.spec_from_file_location("fp_scenes", _FPS)
FP = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(FP)

from gfx import INK, WHITE, H, W, e_io, e_out, hexc, hn, lerp, pop  # noqa: E402
from people import _rr, _shade, _stroke, person  # noqa: E402
import people as _people  # noqa: E402

head = C.flat_head
CX, CY = W / 2, H / 2
run_shots, bg, ws, shop, ext, ots, slide = FP.run_shots, FP.bg, FP.ws, FP.shop, FP.ext, FP.ots, FP.slide
shoulders, desk, crt, phone, envelope = FP.shoulders, C.desk, C.crt, C.phone, C.envelope
darken, glow, fill_rect, vignette, incense = C.darken, C.glow, C.fill_rect, C.vignette, C.incense

# ค่าทั่วไปเหมือนตอน 1 (ซับ, เสียงบรรยากาศ, เกรดสีหนัง, ชื่อช่อง)
SUB_COLOR, SUB_STROKE, SUB_PHRASES, SUB_SIZE, SUB_TOP = FP.SUB_COLOR, FP.SUB_STROKE, True, FP.SUB_SIZE, FP.SUB_TOP
AMBIENCE = {"rain": 0.02, "drone": 0.11}
POST = FP.POST
FP.LIGHTS.update({
    "school_dusk": (300, 250, (1.0, 0.7, 0.45), 0.55), "school_night": (1700, 300, (1.0, 0.82, 0.55), 0.55),
    "classroom": (1500, 200, (1.0, 0.9, 0.7), 0.4), "classroom_dark": (960, 0, (0.7, 0.85, 1.0), 0.6),
    "pond": (1500, 200, (0.75, 0.85, 1.0), 0.6), "phian": (1460, 300, (1.0, 0.92, 0.75), 0.5),
})

_names = ["hook", "recap", "crew", "teacher", "night1", "delete", "night2", "footprints", "sleepover", "search",
          "visit", "flashback", "reflect", "night3", "advice", "mother", "reunion", "dusk", "pond", "rollcall",
          "found", "photo", "gift", "lesson", "after", "cliff"]
CAMERA = {n: ("push_in", "pan_right", "pull_out", "pan_left")[i % 4] for i, n in enumerate(_names)}
CAMERA.update({"night2": "push_in", "night3": "push_in", "pond": "dutch", "rollcall": "push_in", "cliff": "push_in"})
TRANSITIONS = {n: "fade" for n in _names}
TRANSITIONS.update({"night1": "zoom", "flashback": "zoom", "night3": "zoom", "dusk": "zoom"})
NO_IRIS = set()


def school(g, dark=0.0, zoom=1.0, fx=CX, fy=CY):
    key = "school_dusk" if dark < 0.5 else "school_night"
    bg(g, key, lambda g2: C.set_school_dusk(g2, 0.25 if dark < 0.5 else 0.9), zoom, fx, fy)


def classroom(g, dark=0.0, zoom=1.0, fx=CX, fy=CY):
    key = "classroom" if dark < 0.5 else "classroom_dark"
    bg(g, key, lambda g2: C.set_classroom(g2, 0.0 if dark < 0.5 else 0.85), zoom, fx, fy)


def pond(g, zoom=1.0, fx=CX, fy=CY):
    bg(g, "pond", C.set_pond_night, zoom, fx, fy)


def phian_house(g, zoom=1.0, fx=CX, fy=CY):
    bg(g, "phian", C.set_phian_house, zoom, fx, fy)


def face(g, look, x, y, sc, mood="neutral", talk=0.0, turn=0.0, look_at=(0, 0), seed=0):
    shoulders(g, look, x, y, sc)
    with g.at(x, y, sc):
        head(g, look, mood, talk, turn, look_at, seed)


def talk(t):
    return 0.6 * max(0.0, math.sin(t * 8))


def ton(g, x, y, sc, mood="smile", pose="down", turn=0.0, talk_=False, lean=0.0, pose2=None, k=0.0):
    person(g, x, y, C.TON, sc, mood=mood, pose=pose, pose2=pose2, k=k, turn=turn, seed=11, talk=talk_, lean=lean)
    C.robe(g, x, y, sc)


def photo_screen(extra=0, extra_k=1.0, zoom=1.0, fx=0.0, fy=0.0, dialog=None):
    mx, my = max(0.0, 190 - 200 / zoom), max(0.0, 125 - 125 / zoom)
    fx, fy = max(-mx, min(mx, fx)), max(-my, min(my, fy))

    def scr(g2):
        def img(g3):
            with g3.at(20 - fx * zoom, -215 - fy * zoom, zoom):
                C.class_photo(g3, 0, 0, 380, g3.t, extra, extra_k)
        C.editor_ui(g2, img)
        if dialog:
            _rr(g2.c, -150, -290, 300, 110, 10)
            _shade(g2.c, hexc("#ecebe6"), 2, 0.1)
            fill_rect(g2.c, -150, -290, 300, 22, hexc("#3a5a8a"))
            g2.text(dialog, 0, -225, 22, "kanitm", INK)
    return scr


def mon(g, t, scr, sc=2.1):
    FP.monitor_close(g, t, scr, sc)


def sepia(g):
    """เกรดภาพย้อนอดีต: ลดสี + โทนน้ำตาลอุ่น"""
    c = g.c
    c.save()
    c.set_operator(cairo.OPERATOR_HSL_SATURATION)
    c.set_source_rgba(0.5, 0.5, 0.5, 0.75)
    c.paint()
    c.set_operator(cairo.OPERATOR_SOFT_LIGHT)
    c.set_source_rgba(0.85, 0.65, 0.4, 0.55)
    c.paint()
    c.restore()


# ================================================================ 1 hook
def s_hook(g, t, L, d):
    def tbl(g):
        fill_rect(g.c, -800, -800, W + 1600, H + 1600, hexc("#2a2018"))
        glow(g, CX, CY, 900, C.LAMP, 0.3)

    def a(g, t, lt):
        tbl(g)
        C.class_photo(g, CX, 500, 1150 + 40 * slide(lt), t, 0)

    def b(g, t, lt):
        tbl(g)
        with g.at(CX, 520, 1.7):
            C.class_photo(g, 0, 0, 1150, t, 0)

    def c_(g, t, lt):
        FP.desk_scene(g, t, photo_screen(0), "neutral", look=(1, 0))

    def d_(g, t, lt):
        tbl(g)
        with g.at(CX - 400, 640, 2.3):
            C.class_photo(g, 0, 0, 1150, t, 1, min(lt / 1.5, 1.0))
    run_shots(g, t, L, d, [a, b, c_, d_])


# ================================================================ 2 recap
def s_recap(g, t, L, d):
    def a(g, t, lt):
        ext(g, "night")
        vignette(g, 0.5)

    def b(g, t, lt):
        ws(g, "night")
        darken(g, 0.2)
        desk(g, CX, 880, 1500)
        crt(g, 960, 880, 0.95, lambda g2: fill_rect(g2.c, -230, -370, 460, 290, C.SCREEN))
        with g.at(1180, 620, 1.0, 6):   # เคสคอมเปิดข้าง ช่องฮาร์ดดิสก์ว่าง
            _rr(g.c, -90, -150, 180, 300, 10)
            _shade(g.c, hexc("#ddd4bd"), 3, 0.2)

    def c_(g, t, lt):
        ws(g, "night")
        darken(g, 0.3)
        face(g, C.PETE, CX, 600, 3.4, "neutral", 0.0, 0.2, (-0.4, 0), 1)

    def d_(g, t, lt):   # โน้ตแปะจอ
        ws(g, "night")
        darken(g, 0.3)
        crt(g, CX, 1020, 2.1, lambda g2: fill_rect(g2.c, -230, -370, 460, 290, C.SCREEN))
        with g.at(CX + 330, 330, 1.0, 5):
            _rr(g.c, -170, -110, 340, 220, 4)
            _shade(g.c, hexc("#f4e27a"), 2, 0.1)
            g.text("รับเฉพาะงานของ", 0, -40, 34, "kanitm", INK)
            g.text("ลูกค้าที่ล่วงลับแล้ว", 0, 20, 34, "kanitm", INK)
    run_shots(g, t, L, d, [a, b, c_, d_])


# ================================================================ 3 crew
def s_crew(g, t, L, d):
    def a(g, t, lt):
        shop(g, "day")
        person(g, 600, 1180, C.MOTHER, 0.8, mood="smile", pose="hold", turn=0.4, seed=3)
        person(g, 1050, 1220, C.PETE, 0.84, mood="neutral", pose="hold", turn=-0.3, seed=1)
        ton(g, 1450, 1180, 0.85, "smile", "down", -0.4)

    def b(g, t, lt):
        shop(g, "day", 1.3, 600, 500)
        face(g, C.MOTHER, 800, 600, 3.2, "smile", talk(t), 0.3, (0.5, 0), 3)

    def c_(g, t, lt):   # แม่ยื่นจานข้าว
        shop(g, "day")
        person(g, 700, 1180, C.MOTHER, 0.85, mood="worry", pose="present", turn=0.4, seed=3, talk=True)
        hx, hy = C.hand_xy(700, 1180, C.MOTHER, 0.85, "present", 1)
        with g.at(hx - 10, hy - 30):
            g.blob(0, 0, 110, 30, WHITE, 3, 2)
            g.blob(0, -14, 70, 26, hexc("#f2ead8"), 0, 3)
        person(g, 1250, 1220, C.PETE, 0.84, mood="smug", pose="down", turn=-0.5, seed=1)

    def d_(g, t, lt):   # เณรต้นเดินเข้าร้าน
        ext(g, "day")
        x = lerp(1900, 1250, slide(lt, 0, 1, 2.0))
        ton(g, x, 1060, 0.62, "smile", "down", -0.6)

    def e(g, t, lt):
        shop(g, "day", 1.4, 1200, 500)
        face(g, C.TON, CX, 640, 3.2, "smug", talk(t), 0.0, (0, 0), 11)
        with g.at(CX, 640, 3.2):
            C.robe  # noqa: B018

    def f(g, t, lt):   # วิ่งหนีเป็นคนแรก
        shop(g, "day")
        x = lerp(1300, -300, e_io(min(lt / 1.6, 1.0)))
        ton(g, x, 1180, 0.85, "shock", "v", -0.8, lean=-12)
        person(g, 1500, 1220, C.PETE, 0.84, mood="smug", pose="down", turn=-0.6, seed=1)
    run_shots(g, t, L, d, [a, b, c_, d_, e, f])


# ================================================================ 4 teacher
def s_teacher(g, t, L, d):
    def a(g, t, lt):
        shop(g, "day")
        x = lerp(1850, 1300, slide(lt, 0, 1, 2.2))
        person(g, x, 1180, C.SOMJAI, 0.82, mood="sad", pose="present", turn=-0.6, seed=12)
        person(g, 500, 1220, C.PETE, 0.84, mood="neutral", pose="hold", turn=0.5, seed=1)

    def b(g, t, lt):
        shop(g, "day", 1.4, 1200, 500)
        face(g, C.SOMJAI, CX, 620, 3.2, "sad", 0.0, -0.2, (0, 0.2), 12)

    def c_(g, t, lt):   # รูปเก่าในมือ คราบน้ำ
        shop(g, "day", 1.3)
        darken(g, 0.2)
        C.class_photo(g, CX, 520, 1000, t, 0)
        for k in range(5):
            g.blob(400 + k * 260, 300 + 160 * (k % 2), 110, 70, (0.55, 0.5, 0.4, 0.25), 0, k)
        for sx in (-1, 1):
            C.hand_blob(g, CX + sx * 520, 760, C.SOMJAI.skin, 1.8, sx * 90)

    def d_(g, t, lt):
        shop(g, "day", 1.5, 1200, 500)
        face(g, C.SOMJAI, 1050, 620, 3.0, "sad", talk(t), -0.3, (-0.3, 0.1), 12)
        ots(g, C.PETE, 300, 840, 1.1)

    def e(g, t, lt):   # พีทนับคน
        shop(g, "day", 1.3)
        darken(g, 0.2)
        C.class_photo(g, CX, 520, 1150, t, 0)
        n = min(int(lt * 9), 31)
        kx = lerp(500, 1450, (n % 11) / 10)
        ky = 420 + 140 * (n // 11)
        _stroke(g.c, [(kx, ky), (kx + 60, ky + 220)], 34, C.PETE.skin, 1.0)

    def f(g, t, lt):
        shop(g, "day")
        x = lerp(1200, 2100, e_io(min(lt / 2.0, 1.0)))
        person(g, x, 1180, C.SOMJAI, 0.82, mood="sad", pose="down", turn=0.7, seed=12)
        person(g, 520, 1220, C.PETE, 0.84, mood="worry", pose="hold", turn=0.6, seed=1)
    run_shots(g, t, L, d, [a, b, c_, d_, e, f])


# ================================================================ 5 night1
def s_night1(g, t, L, d):
    def a(g, t, lt):
        ws(g, "night")
        darken(g, 0.45)
        incense(g, CX, 900, t, lt > 0.8, 0.0, 3.0)

    def b(g, t, lt):
        FP.desk_scene(g, t, photo_screen(0), "neutral", look=(1, 0))

    def c_(g, t, lt):
        mon(g, t, photo_screen(0, 1.0, 1.6 + 0.2 * slide(lt), 0, 60))

    def d_(g, t, lt):
        mon(g, t, photo_screen(0, 1.0, 2.0, 120, -40))

    def e(g, t, lt):
        mon(g, t, photo_screen(1, min(lt / 1.2, 1.0), 2.4, 170, -45))

    def f(g, t, lt):
        mon(g, t, photo_screen(1, 1.0, 3.2, 170, -45))

    def h(g, t, lt):
        ws(g, "night")
        darken(g, 0.45)
        glow(g, 1300, 560, 600, (0.66, 0.84, 0.9, 1), 0.3)
        face(g, C.PETE, 860, 600, 3.6, "worry", 0.0, 0.7, (1, 0), 1)
    run_shots(g, t, L, d, [a, b, c_, d_, e, f, h])


# ================================================================ 6 delete
def s_delete(g, t, L, d):
    def a(g, t, lt):
        mon(g, t, photo_screen(1, max(0.0, 1 - lt / 2.0), 2.4, 170, -45))

    def b(g, t, lt):   # เครื่องพิมพ์
        ws(g, "night")
        darken(g, 0.3)
        desk(g, CX, 820, 1600)
        _rr(g.c, CX - 320, 560, 640, 260, 20)
        _shade(g.c, hexc("#ddd4bd"), 3, 0.2)
        k = slide(lt, 0, 1, 2.5)
        fill_rect(g.c, CX - 230, 560 - 260 * k, 460, 260 * k, hexc("#f2f0e8"))

    def c_(g, t, lt):
        shop(g, "day")
        ton(g, 900, 1180, 0.9, "smile", "present", 0.2)
        hx, hy = C.hand_xy(900, 1180, C.TON, 0.9, "present", 1)
        C.class_photo(g, hx + 60, hy - 30, 210, t, 1)

    def d_(g, t, lt):
        shop(g, "day", 1.3)
        darken(g, 0.15)
        C.class_photo(g, CX, 520, 1150, t, 1)
        _stroke(g.c, [(lerp(500, 1450, (lt % 2) / 2), 360), (lerp(540, 1490, (lt % 2) / 2), 600)], 30, C.TON.skin, 1.0)

    def e(g, t, lt):
        shop(g, "day", 1.4, 1200, 500)
        face(g, C.TON, CX, 640, 3.2, "shock", talk(t), 0.0, (0, 0), 11)

    def f(g, t, lt):
        shop(g, "day", 1.3)
        darken(g, 0.25)
        with g.at(CX - 600, 640, 2.4 + 0.2 * slide(lt)):
            C.class_photo(g, 0, 0, 1150, t, 1)
    run_shots(g, t, L, d, [a, b, c_, d_, e, f])


# ================================================================ 7 night2
def s_night2(g, t, L, d):
    def a(g, t, lt):
        ws(g, "night")
        darken(g, 0.4)
        C.wall_clock(g, CX, 520, 300, 2, 5)

    def b(g, t, lt):
        mon(g, t, photo_screen(2))

    def c_(g, t, lt):
        mon(g, t, photo_screen(2, 1.0, 2.6 + 0.3 * slide(lt), 23, -5))

    def d_(g, t, lt):   # ผมเปียก หยดน้ำ (ใกล้มาก)
        fill_rect(g.c, -800, -800, W + 1600, H + 1600, hexc("#5f6466"))
        glow(g, CX, 500, 700, (0.75, 0.88, 1.0, 1), 0.25)
        face(g, C.FAI, CX, 640, 3.4, "sad", 0.0, 0.0, (0, 0.6), 7)
        for k in range(4):
            y = (t * 60 + k * 41) % 260
            g.blob(CX - 190 + k * 120, 700 + y, 6, 10, (0.7, 0.85, 0.95, 0.85), 0, k)
        vignette(g, 0.6)

    def e(g, t, lt):
        mon(g, t, photo_screen(2, 1.0, 1.0, 0, 0, "..." if lt < 1.0 else ""))

    def f(g, t, lt):
        mon(g, t, photo_screen(2, 1.0, 1.0, 0, 0, "หนูอยากถ่ายรูปด้วย"))
    run_shots(g, t, L, d, [a, b, c_, d_, e, f])


# ================================================================ 8 footprints
def s_footprints(g, t, L, d):
    def a(g, t, lt):
        FP.desk_scene(g, t, photo_screen(2, 1.0, 1.0, 0, 0, "หนูอยากถ่ายรูปด้วย"), "worry", look=(0.5, 0))

    def b(g, t, lt):   # หยดน้ำบนบันได
        bg(g, "stairs", FP.stairs_down)
        darken(g, 0.4)
        for k in range(3):
            y = 200 + ((lt * 300 + k * 160) % 500)
            g.blob(900 + k * 120, y, 7, 11, (0.65, 0.8, 0.9, 0.9), 0, k)

    def c_(g, t, lt):
        ws(g, "night")
        darken(g, 0.55)
        C.beam(g, 300, 200, 40, 1500, 18, 0.35)
        C.footprints(g, [(420 + i * 150, 830 - i * 45, 10 * (i % 2) - 5) for i in range(8)], t, L[2] - 0.2 + 0.3, 1.8)

    def d_(g, t, lt):
        ws(g, "night")
        darken(g, 0.5)
        C.chair_back(g, 1300, 1000, 1.1)
        C.footprints(g, [(300 + i * 140, 840 - i * 15, 8 * (i % 2) - 4) for i in range(7)], t, -10, 1.8)

    def e(g, t, lt):   # ข้างหลังพีท
        ws(g, "night")
        darken(g, 0.5)
        with g.alpha(0.25 + 0.1 * math.sin(t * 2)):
            person(g, 1180, 1200, C.FAI, 1.05, mood="sad", pose="down", turn=-0.3, seed=7)
        ots(g, C.PETE, 380, 800, 1.3)
        vignette(g, 0.7)
    run_shots(g, t, L, d, [a, b, c_, d_, e])


# ================================================================ 9 sleepover
def s_sleepover(g, t, L, d):
    def a(g, t, lt):
        ws(g, "night")
        darken(g, 0.2)
        ton(g, 900, 1180, 0.9, "smug", "present", 0.2)
        hx, hy = C.hand_xy(900, 1180, C.TON, 0.9, "present", 1)
        with g.at(hx - 10, hy - 20):
            _rr(g.c, -70, -50, 140, 100, 6)
            _shade(g.c, hexc("#8a2a2a"), 2, 0.2)

    def b(g, t, lt):
        ws(g, "night")
        darken(g, 0.3)
        face(g, C.TON, CX, 640, 3.2, "neutral", talk(t), 0.0, (0, 0.4), 11)

    def c_(g, t, lt):   # หลับคาหนังสือ
        ws(g, "night")
        darken(g, 0.35)
        desk(g, CX, 820, 1600)
        g.blob(CX + 150, 800, 300, 120, hexc("#d9731f"), 3, 4)
        _stroke(g.c, [(CX + 40, 790), (CX - 180, 800)], 70, hexc("#d9731f"), 1.0)
        with g.at(CX, 700, 2.4, 70):
            head(g, C.TON, "sad", 0.0, 0.0, (0, 1), 11)
        _rr(g.c, CX + 80, 760, 300, 60, 6)
        _shade(g.c, hexc("#8a2a2a"), 2, 0.2)

    def d_(g, t, lt):
        ws(g, "night")
        darken(g, 0.35)
        ton(g, 700, 1180, 0.9, "shock", "point", 0.4)
        _rr(g.c, 1150, 300, 520, 650, 10)   # ตู้กระจก
        _shade(g.c, hexc("#3a4448"), 4, 0.1)

    def e(g, t, lt):   # เงาสะท้อนในกระจก
        ws(g, "night")
        darken(g, 0.5)
        _rr(g.c, 300, 80, 1320, 900, 14)
        _shade(g.c, hexc("#1f2a2e"), 6, 0.1)
        with g.alpha(0.45):
            person(g, 700, 1050, C.TON, 0.75, mood="shock", pose="down", turn=0.2, seed=11)
            person(g, 1100, 1080, C.PETE, 0.78, mood="worry", pose="down", turn=-0.2, seed=1)
        with g.alpha(0.3 * (0.6 + 0.4 * math.sin(t * 3))):
            person(g, 1450, 1050, C.FAI, 0.75, mood="sad", pose="down", turn=-0.3, seed=7)

    def f(g, t, lt):
        ws(g, "night")
        darken(g, 0.5)
        _rr(g.c, 300, 80, 1320, 900, 14)
        _shade(g.c, hexc("#1f2a2e"), 6, 0.1)
        with g.alpha(0.45):
            person(g, 700, 1050, C.TON, 0.75, mood="worry", pose="down", turn=0.2, seed=11)
            person(g, 1100, 1080, C.PETE, 0.78, mood="worry", pose="down", turn=-0.2, seed=1)

    def h(g, t, lt):   # น้ำนองหน้าตู้
        ws(g, "night")
        darken(g, 0.45)
        fill_rect(g.c, -800, 800, W + 1600, 800, hexc("#3a2c22"))
        g.blob(CX, 900, 360, 80, (0.55, 0.7, 0.75, 0.45), 0, 3)
        glow(g, CX, 880, 300, (0.7, 0.85, 1.0, 1), 0.15)
    run_shots(g, t, L, d, [a, b, c_, d_, e, f, h])


# ================================================================ 10 search
def fb(lines, photo=False, deleted=False, comment=None):
    def scr(g2):
        c = g2.c
        fill_rect(c, -96, -196, 192, 392, hexc("#eef1f5"))
        fill_rect(c, -96, -196, 192, 40, hexc("#3b5998"))
        g2.text("คืนสู่เหย้า ป.6/2542", 0, -176, 15, "kanit", WHITE)
        y = -140
        for ln in lines:
            g2.text(ln, -84, y, 14, "kanitm", INK, anchor="l")
            y += 22
        if photo:
            with g2.at(0, y + 50, 1.0):
                C.class_photo(g2, 0, 0, 170, g2.t, 2)
            y += 120
        if comment:
            _rr(c, -86, y, 172, 70, 10)
            _shade(c, hexc("#dfe3ea"), 1, 0.05)
            g2.text(comment[0], -78, y + 20, 13, "kanitm", INK, anchor="l")
            g2.text(comment[1], -78, y + 44, 13, "kanitm", INK, anchor="l")
        if deleted:
            fill_rect(c, -96, -150, 192, 340, (0.9, 0.9, 0.9, 0.95))
            g2.text("โพสต์นี้ถูกลบแล้ว", 0, 0, 18, "kanit", hexc("#8a8a8a"))
    return scr


def _name_tag_close(g, t, lt):
    fill_rect(g.c, -800, -800, W + 1600, H + 1600, hexc("#9b9890"))
    C.mini_kid(g, CX, 560 + 30 * slide(lt), 5.0, 77, True, 1.0, 0.0, False)
    with g.at(CX + 60, 690 + 30 * slide(lt), 1.0, -4):
        _rr(g.c, -90, -36, 180, 72, 6)
        _shade(g.c, hexc("#f4f2ea"), 2, 0.1)
        g.text("ฝ้าย", 0, 0, 52, "kanitm", hexc("#2b3f63"))
    vignette(g, 0.6)


def s_search(g, t, L, d):
    def ph(g, scr, sc=1.7):
        ws(g, "day")
        darken(g, 0.2)
        phone(g, CX, 580, sc, -3, scr)

    names = ["1. ด.ช.สมชาย", "2. ด.ญ.พิมพ์ใจ", "3. ด.ช.อ้วน", "4. ด.ญ.แก้ว", "...", "32. ด.ช.ต้นกล้า"]
    shots = [lambda g, t, lt: ph(g, fb(["สมาชิก 31 คน"])),
             lambda g, t, lt: ph(g, fb(names)),
             lambda g, t, lt: ph(g, fb(["ใครรู้จักน้องคนนี้ไหมครับ"], True)),
             lambda g, t, lt: ph(g, fb(["ใครรู้จักน้องคนนี้ไหมครับ"], True, False, ("แก้ว: ไม่รู้จักเลย...", "")) if lt < 1.5
                                 else fb(["ใครรู้จักน้องคนนี้ไหมครับ"], True, False, ("แก้ว: ป้ายชื่อเขียนว่า", "ฝ้าย"))),
             lambda g, t, lt: _name_tag_close(g, t, lt),
             lambda g, t, lt: ph(g, fb(["ใครรู้จักน้องคนนี้ไหมครับ"], True, True))]
    run_shots(g, t, L, d, shots)


# ================================================================ 11 visit
def s_visit(g, t, L, d):
    def a(g, t, lt):
        phian_house(g)
        person(g, 1250, 1180, C.SOMJAI, 0.82, mood="neutral", pose="hold", turn=-0.5, seed=12)
        person(g, 650, 1220, C.PETE, 0.84, mood="worry", pose="present", turn=0.5, seed=1)
        hx, hy = C.hand_xy(650, 1220, C.PETE, 0.84, "present", 1)
        C.class_photo(g, hx + 20, hy - 70, 230, t, 2)

    def b(g, t, lt):   # แก้วหล่นแตก
        phian_house(g, 1.4, 900, 800)
        k = min(lt / 0.5, 1.0)
        if k < 1:
            with g.at(CX, lerp(400, 900, k * k)):
                _rr(g.c, -40, -60, 80, 120, 10)
                _shade(g.c, (0.8, 0.9, 0.95, 0.7), 2, 0.1)
        else:
            for i in range(9):
                with g.at(CX + 260 * hn(i, 2), 920 + 30 * hn(i, 3), 1.0, 90 * hn(i, 4)):
                    g.poly([(0, 0), (40, 10), (12, 34)], (0.8, 0.9, 0.95, 0.7), 1, amp=0)
            g.blob(CX, 940, 220, 30, (0.6, 0.75, 0.85, 0.5), 0, 2)

    def c_(g, t, lt):
        phian_house(g, 1.4, 1200, 500)
        face(g, C.SOMJAI, CX, 620, 3.2, "shock", talk(t) * 0.5, 0.0, (0, 0.3), 12)

    def d_(g, t, lt):
        phian_house(g, 1.4, 1200, 500)
        face(g, C.SOMJAI, 1050, 620, 3.0, "sad", 0.0, -0.3, (-0.2, 0.5), 12)
        for k in range(2):
            y = (t * 40 + k * 30) % 60
            g.blob(1000, 640 + y, 5, 8, (0.7, 0.85, 0.95, 0.8), 0, k)
        ots(g, C.PETE, 300, 840, 1.1)
    run_shots(g, t, L, d, [a, b, c_, d_])


# ================================================================ 12 flashback (2542, sepia)
def s_flashback(g, t, L, d):
    def kids_room(g, fai_x=1400, extra=None):
        classroom(g)
        for r in range(2):
            for k in range(6):
                if (r, k) == (1, 4):
                    continue
                C.mini_kid(g, 240 + k * 280 + 140 * r, 600 + r * 170, 1.5, r * 6 + k + 1)

    def a(g, t, lt):   # เก็บค่ารูป
        kids_room(g)
        person(g, 950, 1180, C.SOMJAI_YOUNG, 0.82, mood="firm", pose="present", turn=0.1, seed=13)
        hx, hy = C.hand_xy(950, 1180, C.SOMJAI_YOUNG, 0.82, "present", 1)
        C.coin_jar(g, hx, hy - 50, 0.55)
        sepia(g)

    def b(g, t, lt):   # ฝ้ายนั่งคนเดียว เสื้อปะ
        classroom(g, 0.0, 1.5, 1300, 700)
        person(g, 1100, 1180, C.FAI_ALIVE, 1.0, mood="sad", pose="hold", turn=-0.2, seed=7)
        g.blob(1080, 700, 30, 22, hexc("#c9b8a0"), 2, 3)   # รอยปะ
        sepia(g)

    def c_(g, t, lt):   # ครูชี้ต่อหน้าห้อง
        kids_room(g)
        person(g, 900, 1180, C.SOMJAI_YOUNG, 0.85, mood="angry", pose="point", turn=0.5, seed=13, talk=True)
        sepia(g)

    def d_(g, t, lt):
        classroom(g, 0.0, 1.5, 1300, 600)
        face(g, C.FAI_ALIVE, CX, 600, 3.4, "sad", 0.0, 0.0, (0, 0.8), 7)
        g.blob(CX - 50, 650 + (t * 30) % 40, 6, 10, (0.7, 0.85, 0.95, 0.8), 0, 2)
        sepia(g)

    def e(g, t, lt):   # สระบัวยามเย็น
        bg(g, "pond_dusk", C.set_pond_night)
        glow(g, 300, 200, 900, hexc("#e9a77a"), 0.4)
        x = lerp(500, 820, slide(lt, 0, 1, 3.0))
        person(g, x, 1000, C.FAI_ALIVE, 0.6, mood="neutral", pose="hold", turn=0.6, seed=7)
        fill_rect(g.c, -800, 960, W + 1600, 60, C.POND)
        sepia(g)

    def f(g, t, lt):   # เหลือแต่ดอกบัวลอย (ไม่แสดงภาพการเสียชีวิต)
        bg(g, "pond_dusk", C.set_pond_night)
        for k in range(3):
            r = 40 + ((t * 40 + k * 60) % 200)
            g.c.set_source_rgba(0.8, 0.9, 0.95, 0.4 * (1 - (r - 40) / 200))
            g.c.set_line_width(3)
            g.c.arc(900, 760, r, 0, 2 * math.pi)
            g.c.stroke()
        g.poly([(880, 760), (900, 720), (920, 760)], C.LOTUS, 2, amp=0)
        sepia(g)

    def h(g, t, lt):   # วันถ่ายรูป: โต๊ะว่าง
        kids_room(g)
        _rr(g.c, 1300, 780, 220, 40, 6)
        _shade(g.c, C.WOOD3, 3, 0.2)
        glow(g, 1410, 760, 200, (1, 1, 1, 1), 0.15)
        sepia(g)

    def i_(g, t, lt):
        phian_house(g, 1.4, 1200, 500)
        face(g, C.SOMJAI, CX, 620, 3.2, "sad", talk(t), 0.0, (0, 0.4), 12)
        for k in range(2):
            g.blob(CX - 60 + k * 120, 640 + (t * 40 + k * 30) % 60, 5, 8, (0.7, 0.85, 0.95, 0.8), 0, k)
    run_shots(g, t, L, d, [a, b, c_, d_, e, f, h, i_])


# ================================================================ 13 reflect
def s_reflect(g, t, L, d):
    shots = [lambda g, t, lt: (ext(g, "dusk"), person(g, 1000, 1060, C.PETE, 0.5, mood="sad", pose="down", turn=-0.4, seed=1)),
             lambda g, t, lt: (ext(g, "dusk", 1.5, 1000, 700), face(g, C.PETE, CX, 600, 3.0, "sad", 0.0, -0.3, (-0.5, 0.3), 1)),
             lambda g, t, lt: (ext(g, "dusk", 1.3, 300, 400)),
             lambda g, t, lt: (ext(g, "dusk", 1.6, 1000, 700), C.class_photo(g, CX, 560, 700, t, 2))]
    run_shots(g, t, L, d, shots)


# ================================================================ 14 night3
def s_night3(g, t, L, d):
    def a(g, t, lt):
        ws(g, "night")
        darken(g, 0.6)
        desk(g, CX, 880, 1500)
        on = lt > 1.0
        crt(g, 960, 880, 0.95, photo_screen(3) if on else None, on=on)

    def b(g, t, lt):
        mon(g, t, photo_screen(3))

    def c_(g, t, lt):
        mon(g, t, photo_screen(3, 1.0, 3.0 + 0.3 * slide(lt), -46, 35))

    def d_(g, t, lt):   # หน้าเด็กผู้หญิงจ้องออกมา
        fill_rect(g.c, -800, -800, W + 1600, H + 1600, hexc("#0c1014"))
        glow(g, CX, 520, 700, (0.7, 0.85, 1.0, 1), 0.2)
        face(g, C.FAI, CX, 620, 3.6 + 0.2 * slide(lt), "sad", 0.0, 0.0, (0, 0), 7)
        vignette(g, 0.7)

    def e(g, t, lt):
        mon(g, t, photo_screen(3, 1.0, 1.0, 0, 0, "ครูไม่นับหนู"))

    def f(g, t, lt):
        shop(g, "night")
        darken(g, 0.4 + 0.4 * (C.flick(t, 3, 2.0) < 0.6))

    def h(g, t, lt):   # รอยฝ่ามือเปียกเต็มกระจก
        ext(g, "night", 3.0, 800, 640)
        darken(g, 0.4)
        C.handprints(g, 26, t, L[6] - 0.2 + 0.2, (150, 120, 1550, 700), 0.18)
    run_shots(g, t, L, d, [a, b, c_, d_, e, f, h])


# ================================================================ 15 advice
def s_advice(g, t, L, d):
    def tc(g, t, lt, z=1.4):
        shop(g, "day", z, 1200, 500)
        face(g, C.TON, CX, 640, 3.2, "firm", talk(t), 0.0, (0, 0), 11)
    shots = [lambda g, t, lt: tc(g, t, lt),
             lambda g, t, lt: (ext(g, "day", 1.6, 300, 450), ton(g, 1100, 1060, 0.62, "firm", "think", -0.3, True)),
             lambda g, t, lt: tc(g, t, lt, 1.6),
             lambda g, t, lt: FP.desk_scene(g, t, photo_screen(3), "firm", tod="day", look=(1, 0)),
             lambda g, t, lt: (shop(g, "day", 1.3, 1500, 600), C.camera_antique(g, CX + 80, 1250, 1.6))]
    run_shots(g, t, L, d, shots)


# ================================================================ 16 mother
def s_mother(g, t, L, d):
    def a(g, t, lt):
        phian_house(g, 1.0 + 0.04 * lt / 3)
        x = lerp(-100, 500, slide(lt, 0, 1, 3.0))
        person(g, x, 1220, C.PETE, 0.84, mood="neutral", pose="down", turn=0.6, seed=1)

    def b(g, t, lt):
        phian_house(g)
        person(g, 900, 1150, C.PHIAN, 0.85, mood="neutral", pose="hold", turn=0.4, seed=14)

    def c_(g, t, lt):
        phian_house(g, 1.4, 1300, 450)
        face(g, C.PHIAN, CX, 620, 3.2, "smile", talk(t), 0.4, (0.6, -0.4), 14)

    def d_(g, t, lt):
        phian_house(g)
        person(g, 900, 1150, C.PHIAN, 0.85, mood="smile", pose="present", turn=0.3, seed=14)
        hx, hy = C.hand_xy(900, 1150, C.PHIAN, 0.85, "present", 1)
        C.coin_jar(g, hx - 10, hy - 60, 0.7)

    def e(g, t, lt):
        phian_house(g, 1.5, 900, 700)
        C.coin_jar(g, CX, 560, 2.4)
        for sx in (-1, 1):
            C.hand_blob(g, CX + sx * 170, 700, C.PHIAN.skin, 2.0, sx * 90)

    def f(g, t, lt):
        phian_house(g, 1.4, 600, 450)
        face(g, C.PETE, 800, 600, 3.2, "sad", 0.0, -0.8, (-1, 0.2), 1)
    run_shots(g, t, L, d, [a, b, c_, d_, e, f])


# ================================================================ 17 reunion
def s_reunion(g, t, L, d):
    def crowd(g, t, xs=(250, 520, 790, 1060, 1330, 1600), sc=0.62):
        for i, (x, lk) in enumerate(zip(xs, C.CLASSMATES)):
            person(g, x, 1060, lk, sc, mood="smile", pose="down" if i % 2 else "hold", turn=0.2 * hn(i, 3), seed=20 + i,
                   talk=i in (1, 4))
    shots = [lambda g, t, lt: (school(g), crowd(g, t)),
             lambda g, t, lt: (school(g, 0, 1.4, 500, 500), face(g, C.COP, CX, 620, 3.0, "smile", talk(t), 0.2, (0, 0), 21)),
             lambda g, t, lt: (school(g, 0, 1.4, 1100, 500), face(g, C.MATHT, CX, 620, 3.0, "smug", 0.0, -0.2, (0, 0), 22)),
             lambda g, t, lt: (school(g, 0, 1.3, 900, 600), ton(g, CX, 1250, 1.0, "smug", "down", 0.0), malas(g, CX, 1250, 1.0)),
             lambda g, t, lt: (school(g), crowd(g, t, (200, 420, 1500, 1720, 1950, 2200)),
                               person(g, lerp(1300, 1000, slide(lt)), 1060, C.SOMJAI, 0.62, mood="worry", pose="down", turn=-0.3, seed=12),
                               person(g, lerp(1450, 1150, slide(lt)), 1060, C.MATHT, 0.62, mood="neutral", pose="hold", turn=-0.5, seed=22))]
    run_shots(g, t, L, d, shots)


# ================================================================ 18 dusk
def s_dusk(g, t, L, d):
    def a(g, t, lt):
        school(g, 0.3)
        C.camera_antique(g, 400, 1100, 0.9)
        person(g, 650, 1100, C.PETE, 0.7, mood="neutral", pose="hold", turn=-0.6, seed=1)
        for i, lk in enumerate(C.CLASSMATES[:4]):
            person(g, 1100 + i * 200, 1000, lk, 0.5, mood="neutral", pose="down", turn=-0.3, seed=30 + i)

    def b(g, t, lt):
        school(g, 1.0)
        darken(g, 0.35 if lt > 0.6 else 0.0)

    def c_(g, t, lt):
        school(g, 1.0, 1.3, 1750, 500)
        C.school_bell(g, CX, 700, 1.6, t, 1.0)

    def d_(g, t, lt):
        classroom(g, 1.0)
        k = min(lt / 2.0, 1.0)
        for i in range(int(32 * k)):
            gx, gy = 470 + (i // 5) * 120, 260 + 0
            x = 470 + (i // 5) * 110 + (i % 5) * 16
            _stroke(g.c, [(x, 260), (x if i % 5 != 4 else x - 70, 360)], 5, (0.9, 0.9, 0.86, 0.9), 1.0)

    def e(g, t, lt):
        classroom(g, 1.0, 1.6, 960, 360)
        g.text("32", 760, 380, 160, "kanit", (0.92, 0.92, 0.88, 1))
        g.text("33", 1180, 380, 160, "kanit", (0.92, 0.92, 0.88, min(lt / 1.2, 1.0)))
    run_shots(g, t, L, d, [a, b, c_, d_, e])


# ================================================================ 19 pond
def s_pond(g, t, L, d):
    def a(g, t, lt):
        school(g, 1.0)
        for i, lk in enumerate(C.CLASSMATES[:4]):
            person(g, 400 + i * 360, 1060, lk, 0.62, mood="shock", pose="point" if i == 1 else "down", turn=0.3, seed=30 + i)
        C.beam(g, 760, 760, -20, 900, 10, 0.3)

    def b(g, t, lt):
        school(g, 1.0, 1.5, 300, 600)
        darken(g, 0.4)
        C.beam(g, 0, 700, -10, 1400, 12, 0.35)

    def c_(g, t, lt):
        school(g, 1.0)
        for i, lk in enumerate((C.PETE, C.COP, C.MATHT)):
            x = lerp(300 + i * 250, 1300 + i * 200, slide(lt, 0, 1, 3))
            person(g, x, 1060, lk, 0.62, mood="worry", pose="down", turn=0.7, seed=1 + i, lean=8)
            C.beam(g, x + 60, 700, 0, 700, 10, 0.25)

    def d_(g, t, lt):   # ฟองอากาศผุด
        pond(g, 1.4, 900, 700)
        for k in range(6):
            yy = 760 - ((t * 60 + k * 37) % 120)
            g.circle(820 + k * 45, yy, 14 + 4 * (k % 3), (0.75, 0.88, 0.92, 0.7), 2)

    def e(g, t, lt):   # ครูเดินลงสระ
        pond(g)
        y = lerp(980, 1180, slide(lt, 0, 1, 3))
        person(g, 900, y, C.SOMJAI, 0.75, mood="sad", pose="down", turn=0.2, seed=12)
        fill_rect(g.c, -800, 900, W + 1600, 400, (0.12, 0.23, 0.22, 0.85))
        C.fireflies(g, t, 12)

    def f(g, t, lt):
        pond(g, 1.3, 900, 500)
        face(g, C.SOMJAI, CX, 600, 3.2, "sad", talk(t), 0.0, (0, -0.2), 12)
        fill_rect(g.c, -800, 920, W + 1600, 400, (0.12, 0.23, 0.22, 0.9))
    run_shots(g, t, L, d, [a, b, c_, d_, e, f])


# ================================================================ 20 rollcall
def s_rollcall(g, t, L, d):
    def wading(g, t, lt, talk_=False):
        pond(g)
        person(g, 900, 1180, C.SOMJAI, 0.75, mood="sad", pose="present", turn=0.1, seed=12, talk=talk_)
        hx, hy = C.hand_xy(900, 1180, C.SOMJAI, 0.75, "present", 1)
        C.roll_book(g, hx - 10, hy - 50, 0.32)
        fill_rect(g.c, -800, 900, W + 1600, 400, (0.12, 0.23, 0.22, 0.85))
        C.fireflies(g, t, 10)

    shots = [lambda g, t, lt: wading(g, t, lt),
             lambda g, t, lt: (pond(g, 1.4, 900, 500), C.roll_book(g, CX, 520, 1.4)),
             lambda g, t, lt: (pond(g, 1.0, CX, 300),
                               [person(g, 200 + i * 300, 1060, lk, 0.55, mood="sad", pose="down", turn=0.2, seed=40 + i, talk=True)
                                for i, lk in enumerate(C.CLASSMATES)]),
             lambda g, t, lt: (pond(g, 1.4, 900, 500), C.roll_book(g, CX, 520, 1.4, 0, True)),
             lambda g, t, lt: (pond(g, 1.3, 900, 500), face(g, C.SOMJAI, CX, 600, 3.2, "sad", talk(t), 0.0, (0, 0.6), 12),
                               fill_rect(g.c, -800, 920, W + 1600, 400, (0.12, 0.23, 0.22, 0.9))),
             lambda g, t, lt: (pond(g), C.fireflies(g, t, 22), vignette(g, 0.6)),
             lambda g, t, lt: (pond(g), C.fireflies(g, t, 22),
                               g.alpha(0.0) and None,
                               _ghost_on_lotus(g, t, lt))]
    run_shots(g, t, L, d, shots)


def _ghost_on_lotus(g, t, lt):
    k = min(lt / 1.5, 1.0) * (0.55 + 0.1 * math.sin(t * 2))
    with g.alpha(k):
        person(g, 1350, 760, C.FAI, 0.4, mood="smile", pose="down", turn=-0.2, seed=7, shadow=False)
    glow(g, 1350, 620, 220, (0.85, 0.95, 1.0, 1), 0.25 * k)
    vignette(g, 0.6)


# ================================================================ 21 found
def s_found(g, t, L, d):
    shots = [lambda g, t, lt: (school(g, 1.0), C.beam(g, 1900, 400, 160, 1300, 12, 0.35),
                               person(g, lerp(500, 800, slide(lt)), 1060, C.PETE, 0.62, mood="shock", pose="down", turn=0.7, seed=1),
                               person(g, lerp(300, 600, slide(lt)), 1060, C.COP, 0.62, mood="worry", pose="down", turn=0.7, seed=21)),
             lambda g, t, lt: (school(g, 1.0), C.fireflies(g, t, 10),
                               _people.bust(g, 1000, 1010, C.OUAN, 0.62, mood="worry", pose="hold", turn=0.0, seed=31),
                               g.blob(1000, 1030, 280, 50, hexc("#2c3a2a"), 0, 3)),
             lambda g, t, lt: (school(g, 1.0, 1.4, 900, 500), face(g, C.OUAN, CX, 620, 3.0, "worry", talk(t), 0.0, (0.3, 0), 31),
                               C.fireflies(g, t, 8)),
             lambda g, t, lt: (school(g, 1.0, 1.4, 1200, 500), face(g, C.TON, CX, 640, 3.2, "neutral", talk(t), 0.0, (0, 0), 11)),
             lambda g, t, lt: (school(g, 1.0),
                               person(g, 700, 1060, C.OUAN, 0.62, mood="shock", pose="down", seed=31,
                                      lean=lerp(0, 85, e_io(min(max(lt - 1.2, 0) / 0.8, 1.0)))),
                               ton(g, 1350, 1060, 0.62, "shock", "down", -0.3))]
    run_shots(g, t, L, d, shots)


# ================================================================ 22 photo
def s_photo(g, t, L, d):
    def group(g, t, lt, gap=True):
        school(g, 1.0)
        glow(g, CX, 700, 900, C.LAMP, 0.3)
        xs = [450, 650, 1250, 1450, 1650] if gap else [450, 650, 850, 1250, 1450]
        for i, (x, lk) in enumerate(zip(xs, C.CLASSMATES)):
            person(g, x, 1000, lk, 0.55, mood="smile", pose="down", turn=0.0, seed=50 + i)
        person(g, 1000, 1000, C.SOMJAI, 0.55, mood="smile", pose="hold", turn=0.0, seed=12)
    shots = [lambda g, t, lt: group(g, t, lt),
             lambda g, t, lt: (school(g, 1.0, 1.5, 1000, 650), person(g, 1000, 1150, C.SOMJAI, 0.85, mood="smile", pose="hold", seed=12),
                               glow(g, 820, 900, 160, (1, 1, 1, 1), 0.08)),
             lambda g, t, lt: (school(g, 1.0), C.camera_antique(g, CX, 1350, 1.5, flash=max(0.0, 1 - lt / 0.6)),
                               fill_rect(g.c, -800, -800, W + 1600, H + 1600, (1, 1, 0.97, max(0.0, 0.8 - lt)))),
             lambda g, t, lt: (shop(g, "night", 1.3), darken(g, 0.3), C.class_photo(g, CX, 520, 1100, t, 4, min(lt / 2, 1), False)),
             lambda g, t, lt: (shop(g, "night", 1.3), darken(g, 0.3), _zoom_photo(g, t, lt))]
    run_shots(g, t, L, d, shots)


def _zoom_photo(g, t, lt):
    with g.at(CX + 300, 560, 2.6 + 0.2 * slide(lt)):
        C.class_photo(g, 0, 0, 1100, t, 4, 1.0, False)


def malas(g, x, y, sc):
    """พระเครื่อง/ลูกประคำ 3 เส้นคล้องคอเณรต้น"""
    c = g.c
    with g.at(x, y, sc):
        for k in range(3):
            r = 70 + k * 16
            for i in range(14):
                a = 0.35 + (math.pi - 0.7) * i / 13
                g.circle(r * math.cos(a), -560 + 40 + r * math.sin(a) * 1.1, 7, hexc(("#5a3a2a", "#c9a24a", "#2a2a2a")[k]), 0)
            g.circle(0, -560 + 40 + r * 1.1 + 16, 14, hexc("#d8c27a"), 2)


# ================================================================ 23 gift
def s_gift(g, t, L, d):
    def a(g, t, lt):
        phian_house(g)
        person(g, 1150, 1150, C.PHIAN, 0.85, mood="neutral", pose="hold", turn=-0.3, seed=14)
        person(g, 600, 1220, C.PETE, 0.84, mood="smile", pose="present", turn=0.5, seed=1)
        hx, hy = C.hand_xy(600, 1220, C.PETE, 0.84, "present", 1)
        C.class_photo(g, hx + 30, hy - 70, 230, t, 4, 1.0, False)

    def b(g, t, lt):
        phian_house(g, 1.4)
        C.class_photo(g, CX, 520, 1000, t, 4, 1.0, False)
        fx = lerp(500, 1300, (math.sin(t * 0.8) + 1) / 2)
        _stroke(g.c, [(fx + 120, 1200), (fx + 30, 720)], 90, hexc("#7a6a5a"), 1.0)
        C.hand_blob(g, fx + 20, 680, C.PHIAN.skin, 1.8, -10)

    def c_(g, t, lt):
        phian_house(g, 1.4)
        C.class_photo(g, CX, 520, 1000, t, 4, 1.0, False)
        _stroke(g.c, [(1050, 1200), (900, 740)], 90, hexc("#7a6a5a"), 1.0)
        C.hand_blob(g, 880, 690, C.PHIAN.skin, 1.8, -20)
        _stroke(g.c, [(1350, 1200), (1010, 790)], 100, hexc("#6a7c94"), 1.0)
        C.hand_blob(g, 960, 740, C.PETE.skin, 2.0, -40)

    def d_(g, t, lt):
        phian_house(g, 1.4, 1300, 450)
        face(g, C.PHIAN, CX, 620, 3.2, "smile", talk(t), 0.0, (0, 0.5), 14)
        for k in range(2):
            g.blob(CX - 60 + k * 120, 640 + (t * 30 + k * 30) % 60, 5, 8, (0.7, 0.85, 0.95, 0.8), 0, k)

    def e(g, t, lt):
        phian_house(g)
        person(g, 1150, 1150, C.PHIAN, 0.85, mood="smile", pose="present", turn=-0.3, seed=14)
        hx, hy = C.hand_xy(1150, 1150, C.PHIAN, 0.85, "present", 1)
        C.coin_jar(g, hx - 10, hy - 60, 0.7)
        person(g, 600, 1220, C.PETE, 0.84, mood="worry", pose="stop", turn=0.5, seed=1)

    def f(g, t, lt):
        phian_house(g, 1.4, 1300, 450)
        face(g, C.PHIAN, 1050, 620, 3.0, "smile", talk(t), -0.3, (-0.4, 0.3), 14)
        ots(g, C.PETE, 300, 840, 1.1)
    run_shots(g, t, L, d, [a, b, c_, d_, e, f])


# ================================================================ 24 lesson
def s_lesson(g, t, L, d):
    shots = [lambda g, t, lt: ext(g, "dusk", 1.0 + 0.04 * lt / 3),
             lambda g, t, lt: (ext(g, "dusk", 1.5, 1000, 700), face(g, C.PETE, CX, 600, 3.0, "smile", 0.0, -0.2, (-0.3, -0.2), 1)),
             lambda g, t, lt: (shop(g, "day", 1.3, 700, 400), C.class_photo(g, 700, 460, 520, t, 4, 1.0, False),
                               C.framed_grandma(g, 1250, 460, 0.45, t) if hasattr(C, "framed_grandma") else None)]
    run_shots(g, t, L, d, shots)


# ================================================================ 25 after
def s_after(g, t, L, d):
    shots = [lambda g, t, lt: (shop(g, "day"), person(g, 700, 1180, C.MOTHER, 0.85, mood="worry", pose="point", turn=0.5, seed=3, talk=True),
                               person(g, 1300, 1220, C.PETE, 0.84, mood="smile", pose="hold", turn=-0.5, seed=1)),
             lambda g, t, lt: (shop(g, "day", 1.4, 1200, 500), face(g, C.TON, CX, 640, 3.2, "smug", talk(t), 0.0, (0, 0), 11)),
             lambda g, t, lt: (shop(g, "day", 1.4, 1200, 500), face(g, C.TON, CX, 640, 3.2, "smile", talk(t), 0.2, (0.3, 0), 11)),
             lambda g, t, lt: (bg(g, "hosp", C.set_hospital, 1.3, 1200, 500), face(g, C.MUN, 960, 600, 3.2, "worry", talk(t), 0.2, (0.3, 0), 2),
                               phone(g, 1195, 620, 0.62, 12, None, hand=True, skin=C.MUN.skin)),
             lambda g, t, lt: (ws(g, "day"), face(g, C.PETE, 860, 620, 3.2, "smug", talk(t), 0.3, (0.4, 0), 1),
                               phone(g, 1095, 620, 0.62, 12, None, hand=True))]
    run_shots(g, t, L, d, shots)


# ================================================================ 26 cliff
def old_shop_photo(g, x, y, w, t, pete_k=1.0, zoom=1.0, fx=0.0, fy=0.0):
    """รูปขาวดำวันเปิดร้าน 2522: ลุงมั่นตอนหนุ่ม + ผู้ชายใส่แว่นหน้าเหมือนพีทยืนข้างหลัง"""
    c = g.c
    h = w * 0.7
    with g.at(x, y):
        _rr(c, -w / 2 - 16, -h / 2 - 16, w + 32, h + 32, 6)
        _shade(c, hexc("#e9e4d6"), 2, 0.1)
        c.save()
        c.rectangle(-w / 2, -h / 2, w, h)
        c.clip()
        with g.at(-fx * zoom, -fy * zoom, zoom):
            s = w / 1200
            fill_rect(c, -w, -h, 2 * w, 2 * h, (0.62, 0.62, 0.6, 1))
            _rr(c, -w * 0.45, -h * 0.42, w * 0.9, h * 0.62, 4)
            _shade(c, (0.42, 0.42, 0.4, 1), 2, 0.15)
            _rr(c, -w * 0.25, -h * 0.4, w * 0.5, h * 0.1, 4)
            _shade(c, (0.85, 0.85, 0.82, 1), 2, 0.1)
            g.text("เจริญศิลป์โฟโต้", 0, -h * 0.35, int(60 * s * 1.6), "kanit", (0.2, 0.2, 0.2, 1))
            with g.alpha(pete_k):
                person(g, w * 0.16, h * 0.36, C.PETE_BW, s * 0.42, mood="neutral", pose="down", turn=-0.2, seed=60, shadow=False)
            person(g, -w * 0.1, h * 0.44, C.MUN_YOUNG_BW, s * 0.46, mood="smile", pose="hold", turn=0.2, seed=61, shadow=False)
            g.text("2522", w * 0.4, h * 0.42, int(40 * s * 1.6), "kanit", (0.95, 0.95, 0.92, 1))
        c.restore()
        C.sepia(g) if hasattr(C, "sepia") else None


def s_cliff(g, t, L, d):
    def tbl(g):
        fill_rect(g.c, -800, -800, W + 1600, H + 1600, hexc("#1c1814"))
        glow(g, CX, CY, 900, C.LAMP, 0.25)

    te = max(2.5, d - L[-1] + 0.2 - 3.4)
    shots = [lambda g, t, lt: (ws(g, "night"), darken(g, 0.4), C.wall_clock(g, CX, 520, 300, 0, 0)),
             lambda g, t, lt: (shop(g, "night", 1.5, 1300, 900), darken(g, 0.5), fill_rect(g.c, 300, 960, 1500, 14, (0.95, 0.85, 0.6, 0.8)),
                               envelope(g, lerp(1300, 900, slide(lt, 0, 1, 1.2)), 900, 1.0, 4)),
             lambda g, t, lt: (tbl(g), old_shop_photo(g, CX, 520, 1100, t)),
             lambda g, t, lt: (tbl(g), old_shop_photo(g, CX, 520, 1100, t, 1.0, 2.0, -110, 40)),
             lambda g, t, lt: (tbl(g), old_shop_photo(g, CX, 520, 1100, t, 1.0, 2.6 + 0.3 * slide(lt), 175, 30)),
             lambda g, t, lt: (tbl(g), _photo_back(g, t, lt, False)),
             lambda g, t, lt: (tbl(g), _photo_back(g, t, lt, True), _end_card(g, lt, te))]
    run_shots(g, t, L, d, shots)


def _photo_back(g, t, lt, close):
    with g.at(CX, 520, 1.0 if not close else 1.5, -2):
        _rr(g.c, -550, -380, 1100, 760, 6)
        _shade(g.c, hexc("#e2dccb"), 2, 0.1)
        g.text("ถึงเวลาซ่อมรูปนี้แล้ว ไอ้พีท", 0, -20, 64, "kanitm", hexc("#2a3a6a"), rot=-3)


def _end_card(g, lt, te):
    if lt > te:
        darken(g, min((lt - te) / 0.4, 1.0), (0, 0, 0))
        k = pop(lt, te + 0.5, 0.5)
        g.text("เจริญศิลป์โฟโต้", CX, CY - 60, 90, "kanit", hexc("#e9e4d6"), k)
        g.text("ตอนที่ 3 · เร็ว ๆ นี้", CX, CY + 60, 54, "kanitm", hexc("#c9b48a"), k)


SCENES = {n: globals()["s_" + n] for n in _names}
