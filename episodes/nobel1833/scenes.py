"""ฉากตอน: อัลเฟรด โนเบล (เกิด 21 ต.ค. 1833) — ภาพจริงผ่าน src/photos.py (ไม่มีไฟล์ = วาดการ์ตูนแทน)
เรื่องการเสียชีวิต/สงคราม: ไม่แสดงความรุนแรง ใช้แสงวาบ ควัน เงา"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from chars import (EMIL, LUDVIG, NOBEL, NOBEL_OLD, NOBEL_YOUNG, WORKERS, boom, candle, coin_stack, desk,  # noqa: E402
                   dynamite, flask, globe, hn, icon, medal, mountain, newspaper, quill, smoke, will_doc)
from gfx import (GOLD, GOLD2, GREY, INK, LGREY, NAVY, RED, W, WHITE, e_io, e_out, hexc, lerp, pop,  # noqa: E402
                 seg)
from people import _rr, _shade, head, person  # noqa: E402
from photos import photo  # noqa: E402

CX = W / 2
GROUND = 1270
GOLDTXT = hexc("#b37a12")
GREEN = hexc("#3c8d4f")
DARK = hexc("#2a3150")

CAMERA = {"hook": "push_in", "chemist": "pan_right", "brother": "dutch", "rich": "tilt_up", "obit": "push_in",
          "shock": "pull_out", "will": "pan_left", "lesson": "pull_out", "outro": "push_in"}
TRANSITIONS = {"chemist": "iris", "brother": "fade", "rich": "zoom", "obit": "whip", "will": "fade"}


def has_photo(pid):
    return os.path.exists(os.path.join(os.path.dirname(__file__), "..", "..", "assets", "photos", "nobel1833", pid + ".jpg"))


def ap(t, a, dur=0.38):
    return pop(t, a - 0.2, dur)


def gloom(g, a):
    """เงามืดรอบขอบ (อารมณ์หม่น) บนพื้นขาว"""
    if a <= 0:
        return
    import cairo
    c = g.c
    rg = cairo.RadialGradient(CX, 800, 300, CX, 800, 900)
    rg.add_color_stop_rgba(0, *DARK[:3], 0)
    rg.add_color_stop_rgba(1, *DARK[:3], 0.55 * a)
    c.set_source(rg)
    c.rectangle(-400, 250, W + 800, 1050)
    c.fill()


def cradle(g, x, y, sc, t):
    c = g.c
    with g.at(x, y, sc, 4 * math.sin(t * 1.5)):
        c.new_path()
        c.arc(0, -80, 180, 0.15 * math.pi, 0.85 * math.pi)
        c.close_path()
        _shade(c, hexc("#a8763e"), 6, 0.25)
        g.arc(0, 30, 200, 0.2 * math.pi, 0.8 * math.pi, 10, hexc("#7a5230"))
        g.circle(-60, -60, 46, hexc("#efc4a1"), 5)
        g.blob(30, -50, 110, 50, hexc("#8fb8de"), 5, 3)


# ------------------------------------------------------------------ 1. hook
def s_hook(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:
        medal(g, CX, 840, 230, 1.0, 6 * math.sin(t))
        g.sunburst(CX, 840, 260, 520, 20, t * 10, 10, (0.95, 0.85, 0.55, 0.6))
        g.label("วันนี้ในอดีต", CX, 380, 104, sc=lerp(2.0, 1, e_out(seg(t, 0.1, 0.4))) if t > 0.1 else 0, rot=-4)
        g.label("21 ตุลาคม 1833", CX, 520, 84, color=RED, sc=pop(t, 0.8))
        return
    if t < L[2] - 0.2:   # เด็กชายเกิดที่สตอกโฮล์ม
        for i in range(5):   # หลังคาบ้านสตอกโฮล์ม
            x = 120 + i * 210
            h = 260 + 60 * (i % 2)
            g.poly([(x - 90, GROUND), (x - 90, GROUND - h), (x, GROUND - h - 100), (x + 90, GROUND - h), (x + 90, GROUND)],
                   [hexc("#e3a92b"), hexc("#c8553d"), hexc("#f4efe2"), hexc("#d9a37e"), hexc("#8fb8de")][i], 6)
        cradle(g, CX, 760, ap(t, L[1] + 0.3), t)
        g.label("สตอกโฮล์ม · สวีเดน", CX, 380, 80, color=NAVY, sc=ap(t, L[1]), rot=-3)
        return
    if t < L[4] - 0.2:   # หลายสิบปีต่อมา อ่านข่าวงานศพตัวเอง
        yr = int(lerp(1833, 1888, e_io(seg(t, L[2], L[2] + 2.4))))
        if t < L[3] - 0.2:
            g.calendar(CX, 780, 1.4, str(yr), "", "หลายสิบปีต่อมา")
            return
        person(g, 260, GROUND, NOBEL, 0.8, mood="shock", pose="hold", turn=0.4, seed=1)
        newspaper(g, 700, 760, 0.8 * ap(t, L[3]), -6, "ข่าวมรณกรรม", "", fr=False)
        g.label("ข่าวงานศพของตัวเอง!?", CX, 360, 76, color=RED, sc=ap(t, L[3] + 0.6), rot=-3)
        return
    if t < L[5] - 0.2:   # พ่อค้าความตาย
        gloom(g, 0.8)
        newspaper(g, CX, 780, 1.0 * ap(t, L[4]), 3, "พ่อค้าความตาย!", "", fr=False)
        return
    if t < L[6] - 0.2:   # ความเข้าใจผิดในเช้าวันนั้น
        person(g, CX, GROUND, NOBEL, 0.85, mood="worry", pose="think", turn=0.1, seed=1)
        for i in range(3):
            g.label("?", 200 + i * 340, 420 + 20 * math.sin(t * 3 + i), 110, color=RED, sc=ap(t, L[5] + 0.2 * i))
        return
    k = ap(t, L[6])   # เปลี่ยนประวัติศาสตร์โลก
    globe(g, CX, 780, 260, t)
    medal(g, CX + 230, 1020, 110, k, 10 * math.sin(t * 2))
    g.label("เปลี่ยนโลกไปตลอดกาล!", CX, 360, 76, color=GOLDTXT, sc=k, rot=-3)


# ------------------------------------------------------------------ 2. chemist
def s_chemist(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # อัลเฟรด โนเบล นักเคมี
        g.sunburst(CX, 720, 260, 620, 22, t * 10, 12, (0.95, 0.85, 0.55, 0.8))
        person(g, CX, GROUND, NOBEL, 0.9, mood="firm",
               pose="down" if t < 1.5 else "hold", turn=0.2, seed=1)
        g.label('"อัลเฟรด โนเบล"', CX, 340, 92, color=GOLDTXT, sc=ap(t, 0.2), rot=-3)
        g.name_tag(t, 0.8, 800, 1120, "อัลเฟรด โนเบล", "นักเคมี-นักประดิษฐ์ชาวสวีเดน", side=-1)
        if t > L[1] - 0.2:
            flask(g, 860, 900, 0.6 * ap(t, L[1]), t)
        return
    if t < L[4] - 0.2:   # ไม่ใช่อาวุธ แต่ควบคุมสารอันตราย
        person(g, 260, GROUND, NOBEL_YOUNG, 0.82, mood="firm", pose="hold", turn=0.4, seed=1)
        flask(g, 700, 1000, 1.4, t, shake=0.6 if t > L[3] - 0.2 else 0.0)
        if t < L[3] - 0.2:
            g.label("ไม่ใช่อาวุธสังหาร", CX, 360, 80, color=GREEN, sc=ap(t, L[2]), rot=-3)
        else:
            g.label("อันตรายสุดขีด!", CX, 360, 86, color=RED, sc=ap(t, L[3]), rot=-3)
            g.label("ไนโตรกลีเซอรีน", 700, 1150, 54, sc=ap(t, L[3] + 0.6))
        return
    tun = e_out(seg(t, L[5] - 0.2, L[5] + 1.6))   # ระเบิดภูเขา สร้างถนน อุโมงค์ เหมือง
    mountain(g, 80, 1000, GROUND, 600, t, tunnel=tun, blast=seg(t, L[4] + 0.6, L[4] + 2.2) * (1 - tun))
    g.line([(-400, GROUND - 4), (540 - 110 * tun, GROUND - 4)], 16, hexc("#5a5f75"), amp=0)
    person(g, 950, GROUND, WORKERS[0], 0.5, mood="smile", pose="point", turn=-0.4, seed=7, shadow=False)
    if t < L[5] - 0.2:
        g.label("ระเบิดภูเขา · สร้างถนน", CX, 360, 74, sc=ap(t, L[4]), rot=-3)
    else:
        g.label("ขุดอุโมงค์ · ทำเหมือง", CX, 360, 74, sc=ap(t, L[5]), rot=-3)


# ------------------------------------------------------------------ 3. brother
def s_brother(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # ระเบิดครั้งใหญ่ พรากชีวิตน้องชาย (แสงวาบ + ควัน ไม่แสดงร่าง)
        k = seg(t, 0.8, 1.8)
        if k < 0.3:
            person(g, CX, GROUND, EMIL, 0.8, mood="smile", pose="hold", turn=0.0, seed=2)
            flask(g, CX + 150, 820, 0.5, t, shake=1.0)
        smoke(g, CX, 1100, t, 6, 2.0, 0.7 * k)
        boom(g, CX, 800, 520, k, t)
        g.label("ระเบิดครั้งใหญ่!", CX, 360, 86, color=RED, sc=ap(t, 0.2), rot=-3)
        if t > L[1] - 0.2:
            g.name_tag(t, L[1], CX, 1060, "เอมิล โนเบล", "น้องชายคนเล็ก (ปี 1864)", side=1)
        return
    if t < L[3] - 0.2:   # กัดฟันค้นคว้าต่อ
        gloom(g, 0.6)
        desk(g, -200, 1280, 900)
        candle(g, 820, 900, 1.0, t)
        person(g, 330, GROUND, NOBEL_YOUNG, 0.82, mood="sad" if t < L[2] + 1.2 else "firm", pose="hold", turn=0.4,
               seed=1)
        flask(g, 600, 900, 0.6, t)
        g.label("กัดฟันสู้ต่อ", CX, 360, 84, sc=ap(t, L[2]), rot=-3)
        return
    k = ap(t, L[3])   # ไดนาไมต์สำเร็จ!
    g.sunburst(CX, 800, 220, 600, 22, t * 12, 12, (0.98, 0.85, 0.5, 0.7))
    dynamite(g, CX, 920, 1.6 * k, 6 * math.sin(t * 2), 3, 0.0 if t < L[3] + 1.0 else 0.4, t)
    g.label('"ไดนาไมต์"!', CX, 360, 104, color=RED, sc=k, rot=-4)
    g.label("ปี 1867", CX, 1150, 62, color=GREY, sc=ap(t, L[3] + 0.6))


# ------------------------------------------------------------------ 4. rich
def s_rich(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:   # วิศวกรรมก้าวกระโดด
        mountain(g, 120, 960, GROUND, 520, t, tunnel=1.0)
        u = (t * 0.25) % 1   # รถไฟวิ่งผ่านอุโมงค์
        with g.alpha(1 - max(0, u - 0.8) * 5):
            _rr(g.c, lerp(-200, 520, u), GROUND - 100, 200, 90, 14)
            _shade(g.c, RED, 6, 0.2)
        g.label("วิศวกรรมก้าวกระโดด!", CX, 360, 76, color=GREEN, sc=ap(t, 0.2), rot=-3)
        return
    if t < L[2] - 0.2:   # มหาเศรษฐี
        person(g, 300, GROUND, NOBEL, 0.85, mood="smug", pose="cross", turn=0.3, seed=1)
        for i in range(4):
            coin_stack(g, 600 + i * 110, GROUND, int(3 + 3 * i * ap(t, L[1] + i * 0.25)), 1.0)
        g.label("มหาเศรษฐี", CX, 360, 90, color=GOLDTXT, sc=ap(t, L[1]), rot=-3)
        return
    if t < L[3] - 0.2:   # เหรียญสองด้าน
        flip = math.cos(seg(t, L[2] + 0.6, L[2] + 1.6) * math.pi)
        with g.at(CX, 800, 1, 0, sx=max(0.05, abs(flip)), sy=1):
            g.circle(0, 0, 230, GOLD if flip > 0 else hexc("#6b6f78"), 8)
            g.circle(0, 0, 180, GOLD2 if flip > 0 else hexc("#4a4d55"), 4)
            g.label("สร้าง" if flip > 0 else "ทำลาย", 0, 0, 80, color=GREEN if flip > 0 else RED)
        g.label("เหรียญมีสองด้าน...", CX, 360, 80, sc=ap(t, L[2]), rot=-3)
        return
    if t < L[6] - 0.2:   # มหาอำนาจนำไปใช้ในสงคราม (เงาเท่านั้น)
        gloom(g, 0.7)
        for i in range(5):   # ทหารเงาเดินแถว
            x = (i * 230 + (t - L[3]) * 60) % 1300 - 150
            with g.silhouette(INK, 0.85):
                person(g, x, GROUND, WORKERS[1], 0.55, pose="hold", turn=0.5, seed=60 + i, shadow=False)
        smoke(g, 300, 900, t, 5, 1.6, 0.5)
        smoke(g, 800, 950, t + 1, 5, 1.4, 0.5)
        if t < L[5] - 0.2:
            g.label("สู่สมรภูมิรบ", CX, 360, 86, color=RED, sc=ap(t, L[3]), rot=-3)
        else:
            g.label("เครื่องมือบุกเบิก...", CX, 360, 74, color=GREY, sc=ap(t, L[5]), rot=-3)
        return
    gloom(g, 0.9)   # อาวุธคร่าชีวิตนับไม่ถ้วน
    for i in range(12):
        x = 100 + (i % 6) * 175
        y = 1000 + (i // 6) * 140
        g.circle(x, y, 26, (0.5, 0.5, 0.55, 0.9), 4)
        _rr(g.c, x - 30, y + 26, 60, 80, 20)
        _shade(g.c, (0.5, 0.5, 0.55, 0.9), 4, 0)
    g.label("คร่าชีวิตนับไม่ถ้วน", CX, 360, 80, color=RED, sc=ap(t, L[6]), rot=-3)


# ------------------------------------------------------------------ 5. obit
def s_obit(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:   # จุดเปลี่ยน 1888
        g.calendar(CX, 780, 1.5, "1888", "", "จุดเปลี่ยน")
        return
    if t < L[3] - 0.2:   # พี่ชายเสียชีวิตที่ฝรั่งเศส สื่อเข้าใจผิด
        if t < L[2] - 0.2:
            with g.alpha(0.55):
                person(g, 330, GROUND, LUDVIG, 0.8, mood="neutral", turn=0.3, seed=3)
            candle(g, 720, GROUND, 1.1, t)
            g.label("ลุดวิก (พี่ชาย)", 330, 380, 66, sc=ap(t, L[1]))
            g.label("ฝรั่งเศส", 720, 960, 60, color=NAVY, sc=ap(t, L[1] + 0.5))
        else:
            for i, lk in enumerate((LUDVIG, NOBEL)):
                with g.at(300 + i * 480, 760, 1.4):
                    head(g, lk, "neutral", turn=0.3 - 0.6 * i)
            g.label("=", CX, 760, 120, color=RED, sc=ap(t, L[2] + 0.3))
            g.label("สื่อเข้าใจผิด!", CX, 360, 90, color=RED, sc=ap(t, L[2]), rot=-4)
        return
    if t < L[5] - 0.2:   # เปิดหนังสือพิมพ์ เช้าวันนั้น
        person(g, 260, GROUND, NOBEL, 0.82, mood="neutral" if t < L[4] else "shock", pose="hold", turn=0.4, seed=1)
        newspaper(g, 720, 760, 0.75 * ap(t, L[3]), -5, "LE MARCHAND DE LA MORT EST MORT",
                  k_head=seg(t, L[4], L[4] + 1.0))
        g.label("เช้าวันนั้น...", CX, 360, 80, sc=ap(t, L[3]), rot=-3)
        return
    gloom(g, 0.5)   # พาดหัวเต็มจอ
    newspaper(g, CX, 900, 1.0, -2 + math.sin(t), "LE MARCHAND DE LA MORT EST MORT",
              "Le Dr. Alfred Nobel..." if t > L[6] - 0.2 else "")
    if t < L[6] - 0.2:
        g.label('"พ่อค้าความตาย ได้ตายลงแล้ว"', CX, 360, 66, color=RED, sc=ap(t, L[5]), rot=-3)
    elif t < L[7] - 0.2:
        g.label("ร่ำรวยจากการฆ่าคน", CX, 360, 76, color=RED, sc=ap(t, L[6]), rot=-3)
    else:
        g.label("...เมื่อวานนี้", CX, 360, 80, color=GREY, sc=ap(t, L[7]), rot=-3)


# ------------------------------------------------------------------ 6. shock
def s_shock(g, t, L, d):
    g.ground(GROUND, WHITE)
    gloom(g, 0.6 + 0.2 * math.sin(t))
    if t < L[1] - 0.2:   # หัวใจแหลกสลาย
        with g.at(CX, 760, 1.9):
            head(g, NOBEL, "sad", turn=0.1)
        crack = seg(t, 0.8, 2.4)
        with g.at(820, 480, ap(t, 0.4)):
            g.c.new_path()
            g.c.move_to(0, 60)
            g.c.curve_to(-80, -10, -50, -80, 0, -40)
            g.c.curve_to(50, -80, 80, -10, 0, 60)
            _shade(g.c, RED, 5, 0.2)
            if crack > 0:
                g.line([(0, -40), (-12, -10), (10, 10), (-6, 50 * crack)], 6, WHITE, amp=0)
        g.label("หัวใจแทบแหลกสลาย", CX, 360, 74, color=NAVY, sc=ap(t, 0.2), rot=-3)
        return
    desk(g, -200, 1280, 960)   # นั่งตัวชา คำถาม
    person(g, CX - 80, GROUND, NOBEL_OLD, 0.82, mood="sad", pose="think", turn=0.1, seed=1)
    newspaper(g, 760, 940, 0.35, 70, "MORT", photo=False)
    candle(g, 220, 960, 0.9, t)
    if t < L[2] - 0.2:
        g.label("นั่งตัวชา...", CX, 360, 84, color=GREY, sc=ap(t, L[1]), rot=-3)
    else:
        g.label("โลกจะจดจำเราแบบนี้หรือ?", CX, 360, 70, color=RED, sc=ap(t, L[2]), rot=-3)


# ------------------------------------------------------------------ 7. will
def s_will(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:   # ไม่ยอมให้ชื่อแปดเปื้อน
        person(g, CX, GROUND, NOBEL_OLD, 0.85, mood="firm", pose="fist", turn=0.1, seed=1)
        g.label("ไม่ยอม!", CX, 360, 100, color=RED, sc=ap(t, 0.6), rot=-4)
        return
    if t < L[3] - 0.2:   # แอบเขียนพินัยกรรมอย่างลับ ๆ / 94%
        desk(g, -200, 1280, 960)
        candle(g, 180, 960, 0.8, t)
        if not (t > L[2] and photo(g, "will", 660, 680, 440, 560, 3, ap(t, L[2] + 0.2), 1.04, label="พินัยกรรมของโนเบล 1895")):
            will_doc(g, 660, 680, 0.9, 3, seg(t, L[1], L[3]))
            quill(g, 760 - 30 * math.sin(t * 6), 800, 1.0, 10)
        person(g, 260, GROUND, NOBEL_OLD, 0.75, mood="firm", pose="hold", turn=0.4, seed=1)
        if t < L[2] - 0.2:
            g.label("พินัยกรรมลับ", CX, 360, 84, sc=ap(t, L[1]), rot=-3)
        else:
            n = int(lerp(0, 94, e_io(seg(t, L[2], L[2] + 1.6))))
            g.label(f"{n}%", 300, 420, 120, color=GOLDTXT, sc=ap(t, L[2]))
            g.label("ของทรัพย์สิน", 300, 520, 50, sc=ap(t, L[2] + 0.2))
        return
    if t < L[5] - 0.2:   # กองทุนมอบรางวัล ผู้สร้างประโยชน์แก่มนุษยชาติ
        globe(g, CX, 820, 220, t)
        for i in range(6):
            a = t * 0.8 + i * math.pi / 3
            coin_stack(g, CX + 340 * math.cos(a), 900 + 260 * math.sin(a), 3, 0.7)
        if t < L[4] - 0.2:
            g.label("กองทุนรางวัล", CX, 360, 90, color=GOLDTXT, sc=ap(t, L[3]), rot=-3)
        else:
            g.label("เพื่อมนุษยชาติ", CX, 360, 90, color=GREEN, sc=ap(t, L[4]), rot=-3)
        return
    if t < L[6] - 0.2:   # 5 สาขา
        kinds = [("physics", "ฟิสิกส์"), ("chem", "เคมี"), ("med", "การแพทย์"), ("lit", "วรรณกรรม"), ("peace", "สันติภาพ")]
        for i, (kd, nm) in enumerate(kinds):
            x, y = (240 + (i % 3) * 300, 640) if i < 3 else (390 + (i - 3) * 300, 980)
            k = ap(t, L[5] + i * 0.5)
            icon(g, kd, x, y, 1.0, k)
            g.label(nm, x, y + 130, 44, sc=k)
        return
    k = ap(t, L[6])   # รางวัลโนเบล!
    g.sunburst(CX, 800, 260, 640, 24, t * 10, 12, (0.95, 0.85, 0.5, 0.7))
    if not photo(g, "medal", CX, 800, 520, 520, -2, k, 1.04, label="เหรียญรางวัลโนเบล"):
        medal(g, CX, 800, 240, k, 6 * math.sin(t * 2))
    g.label('"รางวัลโนเบล"', CX, 340, 100, color=GOLDTXT, sc=k, rot=-4)
    if t > L[7] - 0.2:
        g.label("เกียรติยศสูงสุดของโลก", CX, 1160, 64, sc=ap(t, L[7]))


# ------------------------------------------------------------------ 8. lesson
def s_lesson(g, t, L, d):
    g.ground(GROUND, WHITE)
    g.label("บทเรียน", CX, 340, 100, sc=ap(t, 0.2), rot=-3)
    if t < L[2] - 0.2:
        beat = 1 + 0.08 * math.sin(t * 5)
        with g.at(CX, 780, ap(t, 0.4) * beat):
            g.c.new_path()
            g.c.move_to(0, 120)
            g.c.curve_to(-170, -20, -100, -170, 0, -90)
            g.c.curve_to(100, -170, 170, -20, 0, 120)
            _shade(g.c, RED, 6, 0.2)
        if t > L[1] - 0.2:
            g.label("ตราบที่ยังมีลมหายใจ", CX, 1100, 64, color=NAVY, sc=ap(t, L[1]))
        return
    will_doc(g, CX - 40, 800, 0.95, -3, 1.0, ap(t, L[2] + 1.6), title="ตอนจบของฉัน")   # เขียนตอนจบใหม่
    quill(g, CX + 160 + 20 * math.sin(t * 5), 980, 1.2, 15)
    g.label("เขียนตอนจบใหม่ได้เสมอ", CX, 1180, 62, color=GOLDTXT, sc=ap(t, L[2]))


# ------------------------------------------------------------------ 9. outro
def s_outro(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[4] - 0.2:   # ข้อความที่คนอื่นเขียนถึงคุณ
        k = ap(t, L[1])
        with g.at(CX, 780, k, -3):
            g.rrect(-320, -280, 640, 560, 16, hexc("#f4efe2"), 6)
            g.label("ข้อความถึงคุณ...", 0, -200, 54)
            for i in range(5):
                w = 480 * seg(t, L[1] + 0.4 + i * 0.4, L[1] + 0.8 + i * 0.4)
                if w > 0:
                    g.line([(-240, -100 + i * 60), (-240 + w, -100 + i * 60)], 8, LGREY, amp=0)
        if t < L[1] - 0.2:
            g.label("แล้วทุกคนล่ะ?", CX, 760, 96, color=RED, sc=ap(t, 0.2), rot=-3)
        elif t > L[3] - 0.2:
            g.label("อยากถูกจดจำแบบไหน?", CX, 360, 74, color=NAVY, sc=ap(t, L[3]), rot=-3)
        else:
            g.label("วันที่คุณไม่อยู่แล้ว...", CX, 360, 74, color=GREY, sc=ap(t, L[1]), rot=-3)
        return
    if t < L[6] - 0.2:   # อยากแก้ไขเรื่องอะไร
        quill(g, 700 + 30 * math.sin(t * 3), 900, 2.0, 20)
        for i in range(3):
            g.label("?", 260 + i * 140, 700 + 20 * math.sin(t * 3 + i), 110, color=RED, sc=ap(t, L[4] + i * 0.3))
        g.label("อยากแก้ไขเรื่องไหน?", CX, 360, 76, sc=ap(t, L[4]), rot=-3)
        return
    with g.at(CX + 120, 650, ap(t, L[6])):   # ชวนคอมเมนต์
        g.bubble(0, 0, 520, 240, WHITE, tail=(-1, 1))
        for i in range(3):
            g.circle(-110 + i * 110, 0, 24 + 6 * math.sin(t * 6 - i), INK, 0)
    person(g, 250, GROUND, NOBEL, 0.75, mood="smile", pose="wave", turn=0.3, seed=1, talk=True)
    medal(g, 760, 1120, 70, ap(t, L[6] + 0.3), 20 * math.sin(t * 2))
    g.label("คอมเมนต์คุยกันได้เลย!", 700, 960, 58, color=RED, sc=ap(t, L[6] + 0.4))


SCENES = {
    "hook": s_hook, "chemist": s_chemist, "brother": s_brother, "rich": s_rich, "obit": s_obit, "shock": s_shock,
    "will": s_will, "lesson": s_lesson, "outro": s_outro,
}
NO_IRIS = set()
