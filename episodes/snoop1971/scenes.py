"""ฉากตอน: สนูป ด็อกก์ (เกิด 20 ต.ค. 1971) — ตัวละครแบบกึ่งเสมือนจริง (src/people.py)"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from chars import (DRE, FANS, GRANDMA, JUDGE, KID, MOM, SNOOP90, SNOOP_COURT, SNOOP_NOW, SNOOP_TEEN,  # noqa: E402
                   bench, cassette, console, crowd, door_light, gavel, gold_record, headphones, heart, jail_bars,
                   microphone, money, newspaper, sound_waves, stage, streetlight, tv, wall)
from gfx import (BLUE, GOLD, GOLD2, GREY, INK, LGREY, NAVY, RED, W, WHITE, e_in, e_io, e_out, hexc, hn,  # noqa: E402
                 lerp, pop, seg)
from people import _rr, _shade, person  # noqa: E402

CX = W / 2
GROUND = 1270
GREEN = hexc("#3c8d4f")
GOLDTXT = hexc("#b37a12")

CAMERA = {"hook": "push_in", "dark": "tilt_down", "music": "pan_right", "rise": "tilt_up", "trial": "dutch",
          "acquit": "push_in", "reborn": "pull_out", "outro": "pull_out"}
TRANSITIONS = {"rise": "zoom", "trial": "whip", "acquit": "iris", "reborn": "fade"}


def show(t, a, b=None, fade=0.25):
    k = seg(t, a - fade, a)
    if b is not None:
        k = min(k, 1 - seg(t, b - fade, b))
    return k


def baby(g, x, y, sc=1.0, t=0.0):
    """ทารกห่อผ้า"""
    with g.at(x, y + 4 * math.sin(t * 3), sc):
        g.blob(0, 40, 150, 90, hexc("#cfe0ea"), 6, 3)
        g.blob(-40, -40, 80, 74, hexc("#7b4a30"), 6, 4)
        for sx in (-1, 1):
            g.arc(-40 + sx * 26, -44, 10, 20, 160, 4)
        g.arc(-40, -16, 14, 20, 160, 4)
        g.blob(-40, -110, 34, 12, hexc("#1c1714"), 0, 5)
        g.blob(60, 20, 110, 70, hexc("#cfe0ea"), 6, 6)


def cloud(g, x, y, s=1.0, col=LGREY, rain=0.0, t=0.0):
    with g.at(x, y, s):
        if rain > 0:
            for i in range(10):
                p = (t * 1.6 + i * 0.37) % 1
                xx = -140 + i * 30
                with g.alpha(rain * (1 - p)):
                    g.line([(xx, 40 + 160 * p), (xx - 8, 70 + 160 * p)], 5, hexc("#7fb2d8"), amp=0)
        for dx, dy, r in ((-90, 10, 70), (0, -30, 90), (90, 10, 70), (0, 30, 80)):
            g.circle(dx, dy, r, col, 0)
        g.c.new_path()


def siren(g, x, y, t, s=1.0):
    on = int(t * 4) % 2
    with g.at(x, y, s):
        g.rrect(-90, -30, 180, 60, 26, LGREY, 5)
        g.circle(-45, 0, 26, (0.85, 0.2, 0.2, 1) if on else (0.5, 0.2, 0.2, 1), 4)
        g.circle(45, 0, 26, (0.2, 0.4, 0.9, 1) if not on else (0.2, 0.25, 0.5, 1), 4)


def signpost(g, x, y, text, s=1.0, d=1, col=WHITE):
    with g.at(x, y, s):
        g.rrect(-10, -360, 20, 360, 6, hexc("#9b6a3e"), 5)
        pts = [(-150 * d, -340), (130 * d, -340), (170 * d, -290), (130 * d, -240), (-150 * d, -240)]
        g.poly(pts, col, 6)
        g.text(text, 0, -290, 42, "kanit", maxw=260)


def calendar_year(g, x, y, s, year):
    with g.at(x, y, s):
        g.rrect(-150, -170, 300, 340, 22, WHITE, 8)
        g.rrect(-150, -170, 300, 80, 22, RED, 8)
        g.text(str(year), 0, 40, 96, "kanit")


# ------------------------------------------------------------------ 1. hook
def s_hook(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:
        for i in range(7):
            g.sparkle(160 + i * 130, 760 + 70 * ((i * 37) % 3), 14 + 5 * math.sin(t * 3 + i))
        baby(g, CX, 1080, 1.2 * pop(t, 0.6))
        g.label("วันนี้ในอดีต", CX, 420, 104, sc=lerp(2.0, 1, e_out(seg(t, 0.1, 0.4))) if t > 0.1 else 0, rot=-4)
        g.label("20 ตุลาคม 1971", CX, 560, 84, color=RED, sc=pop(t, 0.8))
        if t > L[1] - 0.2:
            g.label("เด็กชายคนหนึ่งเกิดมา", CX, 680, 56, sc=pop(t, L[1]))
        return
    if t < L[3] - 0.2:   # ย่านอันตราย
        wall(g, -200, W + 200, 520, GROUND, tag=True)
        streetlight(g, 860, GROUND, 1.0)
        siren(g, 300, 760, t, 1.2 * pop(t, L[2] + 0.4))
        g.label("ลองบีช, แคลิฟอร์เนีย", CX, 380, 70, sc=pop(t, L[2]))
        g.label("ย่านอันตราย", CX, 470, 60, color=RED, sc=pop(t, L[2] + 0.5))
        return
    if t < L[5] - 0.2:   # ค้ายา ติดคุก คดีฆาตกรรม
        jail_bars(g, CX, 1180, 520, 620, show(t, L[3] + 0.4))
        with g.silhouette(INK, 0.9):
            person(g, CX, 1150, SNOOP_TEEN, 0.62, pose="cross", seed=2, shadow=False)
        for i, (txt, x, y, t0) in enumerate((("ค้ายา", 230, 470, L[3] + 0.2), ("ติดคุก", 850, 470, L[3] + 1.4),
                                              ("คดีฆาตกรรม", CX, 380, L[4] + 0.2))):
            g.label(txt, x, y, 76, color=RED if i == 2 else INK, sc=pop(t, t0), rot=-5 + 5 * i)
        if t > L[4]:
            gavel(g, 860, 760, 0.9 * pop(t, L[4] + 0.5), -30 + 20 * e_in(seg(t, L[4] + 1.0, L[4] + 1.3)))
        return
    # เฉลย: สนูป ด็อกก์
    g.sunburst(CX, 700, 250, 640, 24, t * 10, 14, (0.95, 0.85, 0.55, 0.8))
    person(g, CX, GROUND, SNOOP_NOW, 0.74 * pop(t, L[5] - 0.1), mood="smile", pose="v", seed=1)
    g.label('"สนูป ด็อกก์"', CX, 330, 104, color=GOLDTXT, sc=pop(t, L[5] + 0.4), rot=-3)
    g.name_tag(t, L[5] + 1.0, 850, 1000, "สนูป ด็อกก์", "แร็ปเปอร์ระดับตำนาน", side=-1)


# ------------------------------------------------------------------ 2. childhood
def s_childhood(g, t, L, d):
    g.ground(GROUND, WHITE)
    dull = e_io(seg(t, L[2], L[2] + 1.0))
    if t > L[1] - 0.3 or True:
        tv(g, 800, 960, 1.0 * pop(t, L[1] - 0.3), t, show=dull < 0.5)
    person(g, 230, GROUND, MOM, 0.8, mood="smile" if dull < 0.5 else "worry", turn=0.3, seed=3,
           talk=L[1] < t < L[1] + 2.5)
    person(g, 470, GROUND, KID, 0.95, mood="smile" if dull < 0.5 else "sad", turn=0.4 if t > L[1] else 0,
           pose="wave" if t < L[1] else "down", seed=4)
    g.name_tag(t, L[0] + 0.3, 470, 470, "แคลวิน บรอดัส จูเนียร์", "ชื่อจริงของสนูป ด็อกก์", side=1)
    g.name_tag(t, L[1] - 0.1, 250, 440, "เบเวอร์ลี เทต", "แม่ของสนูป", side=-1)
    if t > L[1] + 0.4:
        g.label('"สนูปี้"', 800, 680, 90, color=BLUE, sc=pop(t, L[1] + 0.6) * (1 - dull), rot=-5)
    if t > L[2] - 0.2:
        cloud(g, 470, 450, 1.0 * pop(t, L[2] - 0.1), GREY, rain=dull, t=t)
        g.label("ชีวิตจริงไม่สดใส...", 800, 640, 60, sc=pop(t, L[2] + 0.8))


# ------------------------------------------------------------------ 3. dark
def s_dark(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[3] - 0.2:
        wall(g, -200, W + 200, 500, GROUND, tag=True)
        streetlight(g, 900, GROUND, 1.0, on=(t * 7) % 5 > 0.6)
        if t < L[2] - 0.2:
            walk = e_io(seg(t, 0, 4.5))
            person(g, lerp(-150, CX - 60, walk), GROUND, SNOOP_TEEN, 0.86, mood="worry" if t < L[1] else "firm",
                   pose="down" if t < L[1] else "cross", turn=0.2, seed=5)
            if t < L[1] - 0.2:
                g.label("ด้านมืด", CX, 380, 90, color=INK, sc=pop(t, 1.0))
            else:
                g.label("แก๊งข้างถนน", CX, 380, 84, color=RED, sc=pop(t, L[1] + 0.2))
            if t > L[1] - 0.2:
                for i, xx in enumerate((150, 860)):
                    with g.silhouette(INK, 0.85):
                        person(g, xx, GROUND + 10, FANS[i], 0.8, pose="cross", seed=6 + i, shadow=False)
                for i in range(5):
                    money(g, 260 + i * 140, 1215 + 8 * math.sin(t * 3 + i), 0.6 * pop(t, L[1] + 0.3 + i * 0.1),
                          20 * hn(i, 3))
            return
        # เข้าออกคุก
        person(g, CX, GROUND, SNOOP_TEEN, 0.86, mood="sad", seed=5)
        jail_bars(g, CX, GROUND + 10, 560, 780, show(t, L[2] + 0.6))
        cap_k = e_out(seg(t, L[2], L[2] + 0.8))
        with g.at(lerp(CX + 300, 900, cap_k), lerp(900, 560, cap_k), 1.0, 360 * cap_k):
            g.poly([(-90, 0), (0, -40), (90, 0), (0, 40)], INK, 4)
            g.line([(60, 0), (80, 70)], 5, GOLD)
        g.label("จบมัธยม → เข้าคุก", CX, 380, 70, color=RED, sc=pop(t, L[2] + 0.7))
        return
    # ทางแยกสองทาง
    person(g, CX, GROUND, SNOOP_TEEN, 0.8, mood="worry", seed=5)
    g.label("จุดจบแค่ 2 ทาง?", CX, 380, 80, sc=pop(t, L[3] + 0.2))
    if t > L[4] - 0.2:
        signpost(g, 230, GROUND, "ข้างถนน", 1.0 * pop(t, L[4] - 0.2), -1)
        siren(g, 230, 760, t, 0.9 * pop(t, L[4] + 0.2))
    if t > L[5] - 0.2:
        signpost(g, 850, GROUND, "ในตาราง", 1.0 * pop(t, L[5] - 0.2), 1)
        jail_bars(g, 850, 820, 200, 220, pop(t, L[5] + 0.2))


# ------------------------------------------------------------------ 4. music
def s_music(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:
        microphone(g, CX, 860, 1.6 * pop(t, 0.2), 0, glow=0.9)
        g.label("อาวุธลับ", CX, 400, 110, color=GOLDTXT, sc=pop(t, 0.8), rot=-4)
        return
    if t < L[3] - 0.2:
        person(g, 330, GROUND, SNOOP90, 0.86, mood="smile", pose="hold", talk=True, turn=0.35, seed=7)
        microphone(g, 420, 640, 0.6, -20)
        sound_waves(g, 500, 560, t)
        if t < L[2] - 0.2:
            g.label("เสียงนุ่มลึก", 790, 520, 70, sc=pop(t, L[1] + 0.3))
            g.label("แร็ปลื่นไหล", 790, 640, 70, color=BLUE, sc=pop(t, L[1] + 1.4))
        else:
            cassette(g, 790, 700, 1.0 * pop(t, L[2] - 0.1), -6, t)
            g.label("ดนตรี = ทางรอด", 790, 470, 66, color=GREEN, sc=pop(t, L[2] + 0.3))
        return
    # เทปไปถึงหู ดร.เดร
    person(g, 780, 1310, DRE, 0.82, mood="firm" if t < L[3] + 2.0 else "smile", turn=-0.3, seed=8,
           legs=False, shadow=False)
    headphones(g, 780, 1310 - 842 * 0.82 - 50, 0.95)
    console(g, 600, GROUND - 120, 0.95)
    k = e_io(seg(t, L[3], L[3] + 1.2))
    cassette(g, lerp(150, 520, k), lerp(500, 870, k), 0.7, 360 * k, t)
    g.name_tag(t, L[3] + 0.4, 300, 420, "ดร.เดร", "โปรดิวเซอร์ระดับตำนาน", side=1)
    if t > L[3] + 2.0:
        g.label("!!", 940, 380, 110, color=RED, sc=pop(t, L[3] + 2.0), rot=8)


# ------------------------------------------------------------------ 5. rise
def s_rise(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.1:
        k = e_io(seg(t, 0.1, 1.3))
        g.circle(lerp(200, 880, k), 700 - 300 * math.sin(k * math.pi), 80, GOLD2 if k > 0.5 else hexc("#f4eccf"), 6)
        g.label("ชั่วข้ามคืน", CX, 420, 100, sc=pop(t, 0.2))
        return
    if t < L[2] - 0.2:
        stage(g, CX, GROUND - 260, t)
        person(g, CX, GROUND - 260, SNOOP90, 0.62, mood="smile", pose="wave" if (t % 2) < 1 else "fist", talk=True,
               seed=7)
        crowd(g, CX, GROUND + 30, 1100, t, 9)
        g.label("จุดสูงสุดของฮิปฮอป", CX, 330, 76, color=GOLDTXT, sc=pop(t, L[1] + 0.3), rot=-3)
        return
    for i in range(5):
        a = t * 0.8 + i * 1.26
        g.sparkle(CX + 380 * math.cos(a), 760 + 300 * math.sin(a), 20)
    gold_record(g, CX, 800, 1.3 * pop(t, L[2] - 0.1), 4 * math.sin(t * 2), "Doggystyle · 1993")
    g.label("อัลบั้มแรก", CX, 330, 84, sc=pop(t, L[2] + 0.2))
    g.label("ขายถล่มทลายทั่วโลก!", CX, 1170, 66, color=RED, sc=pop(t, L[2] + 0.9))


# ------------------------------------------------------------------ 6. trial
def s_trial(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # ซูเปอร์สตาร์ -> พายุอดีตกลับมา
        storm = e_io(seg(t, L[1], L[1] + 1.0))
        stage(g, CX, GROUND - 260, t, lights=storm < 0.5)
        person(g, CX, GROUND - 260, SNOOP90, 0.62, mood="smile" if storm < 0.5 else "shock",
               pose="wave" if storm < 0.5 else "down", seed=7)
        crowd(g, CX, GROUND + 30, 1100, t, 9, 1 - storm)
        if storm > 0:
            for i in range(3):
                cloud(g, 220 + i * 320, lerp(-200, 320, storm), 0.8, GREY)
            if int(t * 3) % 4 == 0:
                g.poly([(880, 420), (820, 560), (880, 560), (820, 700)], None, 10, stroke=GOLD)
            g.label("อดีตย้อนกลับมา!", CX, 1180, 80, color=RED, sc=pop(t, L[1] + 0.5), rot=-4)
        else:
            g.label("ซูเปอร์สตาร์", CX, 380, 84, color=GOLDTXT, sc=pop(t, 0.3))
        return
    if t < L[3] - 0.2:
        newspaper(g, CX, 780, 1.45 * pop(t, L[2] - 0.2), -3, "ตั้งข้อหาฆาตกรรม!",
                  "สนูป ด็อกก์ · ก.ย. 1993")
        return
    # ศาล
    person(g, 680, 921, JUDGE, 0.5, mood="firm", seed=9, legs=False, shadow=False)
    bench(g, 680, 860, 0.75)
    person(g, 220, GROUND, SNOOP_COURT, 0.66, mood="worry" if t < L[5] else "sad", turn=0.3, seed=10)
    if t < L[4] - 0.2:
        g.label("จากเวที → ศาล", CX, 340, 76, sc=pop(t, L[3] + 0.3))
    elif t < L[5] - 0.2:
        g.label("เดิมพัน: อิสรภาพตลอดชีวิต", CX, 340, 62, color=RED, sc=pop(t, L[4]))
    else:
        for i, (x, y) in enumerate(((880, 560), (880, 1020), (560, 1110))):
            g.label("อาชญากร?", x, y + 8 * math.sin(t * 3 + i), 56, color=GREY, sc=pop(t, L[5] + 0.3 + i * 0.5),
                    rot=-8 + 8 * i)
        if t > L[6]:
            g.label("แค่อาชญากรข้างถนน?", CX, 340, 66, color=RED, sc=pop(t, L[6] + 0.3))


# ------------------------------------------------------------------ 7. acquit
def s_acquit(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:
        if t < L[1] - 0.2:
            years = [1993, 1994, 1995, 1996]
            i = min(int(seg(t, 0.4, 3.0) * 3.99), 3)
            calendar_year(g, CX, 780, 1.4 * pop(t, 0.1), years[i])
            g.label("เกือบ 3 ปีเต็ม", CX, 380, 84, sc=pop(t, 0.4))
            return
        person(g, 680, 921, JUDGE, 0.5, mood="neutral", seed=9, legs=False, shadow=False)
        bench(g, 680, 860, 0.75)
        hit = e_in(seg(t, L[1] + 0.2, L[1] + 0.5))
        gavel(g, 930, 640, 0.8, -40 + 50 * hit)
        person(g, 220, GROUND, SNOOP_COURT, 0.66, mood="smile" if t > L[1] + 0.5 else "worry", pose="v" if t > L[1] + 1.2 else "down",
               turn=0.3, seed=10)
        g.label("พ้นผิด!", CX, 330, 110, color=GREEN, sc=pop(t, L[1] + 0.5), rot=-5)
        g.label("ก.พ. 1996", CX, 450, 50, color=GREY, sc=pop(t, L[1] + 1.0))
        return
    door_light(g, 800, GROUND, 1.0, e_out(seg(t, L[2] - 0.2, L[2] + 0.8)))
    if t < L[3] - 0.2:
        walk = e_io(seg(t, L[2] + 0.4, L[3] + 0.4))
        person(g, lerp(250, 560, walk), GROUND + 10, SNOOP_COURT, 0.8, mood="firm", turn=0.4, seed=10)
    else:
        person(g, 420, GROUND + 10, SNOOP_COURT, 0.84, mood="firm", pose="stop", turn=0.1, seed=10)
        g.label("จะไม่กลับไปจุดเดิมอีก", CX, 360, 76, color=NAVY, sc=pop(t, L[3] + 0.3))


# ------------------------------------------------------------------ 8. reborn
def s_reborn(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:   # ทิ้งชีวิตแก๊งสเตอร์
        wall(g, -200, 520, 500, GROUND, tag=True)
        walk = e_io(seg(t, 0.4, L[1]))
        person(g, lerp(380, 760, walk), GROUND, SNOOP90, 0.84, mood="firm", turn=0.4, seed=7)
        k = e_in(seg(t, 0.6, 1.4))
        with g.at(lerp(560, 520, k), lerp(900, GROUND - 20, k), 0.8, 200 * k):
            g.poly([(-60, -30), (60, -30), (0, 40)], BLUE, 5)
        g.label("ทิ้งชีวิตแก๊งสเตอร์", CX, 360, 76, sc=pop(t, 0.3))
        return
    if t < L[2] - 0.2:   # สร้างตัวใหม่: แสงวาบเปลี่ยนลุค
        k = seg(t, L[1] + 0.3, L[1] + 0.9)
        g.sunburst(CX, 760, 220, 600, 20, t * 20, 12, (0.95, 0.85, 0.55, k))
        person(g, CX, GROUND, SNOOP90 if k < 0.5 else SNOOP_NOW, 0.86, mood="firm" if k < 0.5 else "smile", seed=7)
        with g.alpha(math.sin(k * math.pi)):
            g.circle(CX, 700, 500, WHITE, 0)
        g.label("สร้างตัวเองใหม่", CX, 360, 84, color=GOLDTXT, sc=pop(t, L[1] + 0.4))
        return
    if t < L[3] - 0.2:   # จากแร็ปเปอร์ที่คนเคยหวาดกลัว
        with g.silhouette(INK, 0.9):
            person(g, CX, GROUND, SNOOP90, 0.86, mood="angry", pose="cross", seed=7, shadow=False)
        for i, x in enumerate((140, 940)):
            person(g, x, GROUND + 20, FANS[i], 0.6, mood="worry", turn=0.4 if x < CX else -0.4, seed=11 + i)
        g.label("เคยน่ากลัว", CX, 360, 84, color=GREY, sc=pop(t, L[2]))
        return
    if t < L[4] - 0.2:   # ไอคอนแห่งความสุข + นักธุรกิจ
        person(g, CX, GROUND, SNOOP_NOW, 0.84, mood="smile", pose="wave", seed=1)
        g.label("ไอคอนแห่งความสุข", 250, 560, 54, color=GOLDTXT, sc=pop(t, L[3] + 0.2), rot=-5)
        g.label("นักธุรกิจระดับพันล้าน", 820, 760, 50, color=GREEN, sc=pop(t, L[3] + 1.6), rot=4)
        g.sparkle(200, 680, 30 * pop(t, L[3] + 0.4))
        for i in range(3):
            money(g, 760 + 60 * i, 880 + 20 * i, 0.7 * pop(t, L[3] + 1.8 + i * 0.1), -10 + 10 * i)
        return
    # มิตรภาพทุกเจเนอเรชัน
    person(g, CX, GROUND, SNOOP_NOW, 0.82, mood="smile", pose="wave", seed=1)
    person(g, 180, GROUND, KID, 0.82, mood="smile", pose="wave", turn=0.3, seed=12)
    person(g, 900, GROUND, GRANDMA, 0.66, mood="smile", pose="wave", turn=-0.3, seed=13)
    for i in range(4):
        heart(g, 200 + i * 230, 480 + 30 * math.sin(t * 3 + i), 0.9 * pop(t, L[4] + 0.3 + i * 0.15))
    g.label("ทุกเจเนอเรชันหลงรัก", CX, 340, 74, color=RED, sc=pop(t, L[4] + 0.6))


# ------------------------------------------------------------------ 9. lesson
def s_lesson(g, t, L, d):
    g.ground(GROUND, WHITE)
    steps = 5
    for i in range(steps):   # บันไดจากล่างซ้ายขึ้นขวาบน
        k = pop(t, 0.2 + i * 0.12)
        if k <= 0:
            continue
        x, y = 140 + i * 190, GROUND - i * 95
        _rr(g.c, x - 95, y - 30, 190 * k, 30 + i * 95, 6)
        _shade(g.c, LGREY if i < 2 else hexc("#f4e2b0"), 5, 0.2)
    g.label("บทเรียน", CX, 360, 100, sc=pop(t, 0.1), rot=-3)
    p = e_io(seg(t, L[1] + 0.5, L[3]))
    i = p * (steps - 1)
    x = 140 + i * 190
    j = math.floor(i + 0.0001)
    y = GROUND - 30 - j * 95 - 95 * max(0.0, (i - j) * 2 - 1) - 40 * math.sin((i - j) * math.pi)
    look = SNOOP_TEEN if p < 0.5 else SNOOP_NOW
    person(g, x, y, look, 0.5, mood="worry" if p < 0.3 else "smile", turn=0.4, seed=5)
    if L[1] - 0.2 < t < L[3] - 0.2:
        g.label("จุดเริ่มต้นเลวร้าย", 240, 560, 52, color=GREY, sc=pop(t, L[1]))
    if L[2] - 0.2 < t < L[3] - 0.2:
        g.label("≠ ตอนจบของชีวิต", 240, 680, 52, color=GREEN, sc=pop(t, L[2]))
    if t > L[3] - 0.2:
        g.label("โอกาสครั้งที่สอง", 420, 560, 64, color=GOLDTXT, sc=pop(t, L[3] + 0.3))


# ------------------------------------------------------------------ 10. outro
def s_outro(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[3] - 0.2:
        person(g, 300, GROUND, SNOOP_NOW, 0.84, mood="smile", pose="wave" if t < L[1] + 0.5 else "point", turn=0.35,
               seed=1, talk=False)
        g.label("แล้วทุกคนล่ะ?", 680, 400, 84, sc=pop(t, 0.1))
        if t > L[1] - 0.2:
            g.label("?", 800, 760 + 15 * math.sin(t * 3), 260, color=RED, sc=pop(t, L[1]), rot=8)
        if t > L[2] - 0.2:
            g.label("อะไรสำคัญที่สุด?", 790, 1060, 56, sc=pop(t, L[2]))
        return
    if t < L[4] - 0.2:
        person(g, CX, GROUND, SNOOP_NOW, 0.84, mood="smile", pose="wave", seed=1)
        for i in range(3):
            hx, hy = ((170, 640), (910, 640), (170, 940))[i]
            heart(g, hx, hy + 25 * math.sin(t * 3 + i), 0.8 * pop(t, L[3] + 0.3 + i * 0.2))
        g.label("ป๋าสนูป", CX, 340, 100, color=GOLDTXT, sc=pop(t, L[3] + 0.2), rot=-3)
        return
    k = pop(t, L[4] - 0.1)
    with g.at(CX, 760, k):
        g.bubble(0, 0, 640, 300, WHITE, tail=(-1, 1))
        for i in range(3):
            g.circle(-120 + i * 120, 0, 26 + 6 * math.sin(t * 6 - i), INK, 0)
    g.label("คอมเมนต์คุยกันได้เลย!", CX, 1080, 70, color=RED, sc=pop(t, L[4] + 0.4))


SCENES = {
    "hook": s_hook, "childhood": s_childhood, "dark": s_dark, "music": s_music, "rise": s_rise, "trial": s_trial,
    "acquit": s_acquit, "reborn": s_reborn, "lesson": s_lesson, "outro": s_outro,
}
NO_IRIS = set()
