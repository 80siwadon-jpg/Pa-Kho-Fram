"""ฉากตอน: เปิดพิพิธภัณฑ์กุกเกนไฮม์ (21 ต.ค. 1959) — ตัวละครแบบกึ่งเสมือนจริง (src/people.py)"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from chars import (ARTISTS, CREAM, CRITICS, CROWD, GLASS_BLUE, WRIGHT, blueprint, box_building, cane,  # noqa: E402
                   city_row, drafting_table, empty_chair, guggenheim, letter, painting, rule_book, spiral_cut,
                   toilet, washing_machine)
from gfx import (GOLD, GOLD2, GREY, INK, LGREY, NAVY, RED, W, WHITE, e_io, e_out, hexc, hn, lerp,  # noqa: E402
                 pop, seg)
from people import _rr, _shade, person  # noqa: E402

CX = W / 2
GROUND = 1270
GOLDTXT = hexc("#b37a12")
GREEN = hexc("#3c8d4f")

CAMERA = {"hook": "push_in", "wright": "pan_right", "spiral": "tilt_up", "mock": "dutch", "artists": "pan_left",
          "fight": "push_in", "death": "pull_out", "opening": "tilt_up", "lesson": "pull_out", "outro": "push_in"}
TRANSITIONS = {"wright": "iris", "spiral": "zoom", "mock": "whip", "death": "fade", "opening": "zoom"}


def ap(t, a, dur=0.38):
    """เด้งขึ้นทันทีที่ช่วงเริ่ม (เริ่มก่อนจุดตัด 0.2 วิ) — กันเฟรมว่างตอนเปลี่ยนช่วง"""
    return pop(t, a - 0.2, dur)


def hat_and_cane(g, x, y, sc=1.0, glow=0.0, t=0.0):
    """หมวกพอร์คพาย + ไม้เท้าของไรต์ (สัญลักษณ์แทนตัวเขาหลังจากไป)"""
    c = g.c
    if glow > 0:
        g.sunburst(x, y - 120 * sc, 120 * sc, 260 * sc, 16, t * 8, 8, (0.95, 0.83, 0.48, 0.6 * glow))
    cane(g, x + 110 * sc, y, sc, 8)
    with g.at(x, y - 60 * sc, sc):
        _rr(c, -60, -110, 120, 70, 14)
        _shade(c, hexc("#2c2a2e"), 6, 0.15)
        _rr(c, -60, -60, 120, 16, 3)
        _shade(c, hexc("#5a4a3a"), 3, 0)
        g.c.new_path()
        g.c.save()
        g.c.translate(0, -40)
        g.c.scale(1, 0.25)
        g.c.arc(0, 0, 130, 0, 2 * math.pi)
        g.c.restore()
        _shade(c, hexc("#2c2a2e"), 6, 0.0)


def book(g, x, y, sc, tear=0.0, title="ตำราสถาปัตย์"):
    with g.at(x, y, sc):
        for sx in (-1, 1):
            with g.at(sx * 40 * tear, 30 * tear * tear, 1, sx * 28 * tear):
                _rr(g.c, -150 if sx < 0 else 0, -110, 150, 220, 6)
                _shade(g.c, hexc("#2f5a3a"), 6, 0.2)
        if tear < 0.2:
            g.label(title, 0, 0, 34, color=GOLD2)


def rotunda_up(g, cx, cy, t, k=1.0):
    """มองขึ้นจากโถงกลาง: วงทางลาดซ้อนเป็นเกลียว + ช่องแสงโดมตรงกลาง"""
    c = g.c
    for i in range(6, 0, -1):
        r = 70 + i * 62 * k
        c.new_path()
        c.save()
        c.translate(cx, cy)
        c.scale(1, 0.92)
        c.arc(0, 0, r, 0, 2 * math.pi)
        c.restore()
        _shade(c, CREAM if i % 2 else hexc("#ece4d2"), 6, 0.15)
        for j in range(3):   # คนบนทางลาด
            a = t * (0.25 + i * 0.03) + j * 2.1 + i
            g.circle(cx + math.cos(a) * (r - 30), cy + math.sin(a) * (r - 30) * 0.92, 8,
                     [RED, NAVY, GREEN, GOLD][(i + j) % 4], 3)
    g.sunburst(cx, cy, 30, 66, 12, t * 20, 5, (1, 1, 1, 0.9))
    g.circle(cx, cy, 64, GLASS_BLUE, 5)


def sky_city(g, t, gap=None):
    g.ground(GROUND, WHITE)
    city_row(g, -320, 1400, GROUND, 3, gap)


# ------------------------------------------------------------------ 1. hook
def s_hook(g, t, L, d):
    if t < L[1] - 0.2:   # วันที่ + กุกเกนไฮม์
        g.ground(GROUND, WHITE)
        g.sunburst(CX, 900, 300, 640, 22, t * 8, 10, (0.95, 0.85, 0.55, 0.7))
        guggenheim(g, CX + 60, GROUND, 0.85, 1.0, t)
        g.label("วันนี้ในอดีต", CX, 380, 104, sc=lerp(2.0, 1, e_out(seg(t, 0.1, 0.4))) if t > 0.1 else 0, rot=-4)
        g.label("21 ตุลาคม 1959", CX, 520, 84, color=RED, sc=pop(t, 0.8))
        return
    if t < L[3] - 0.2:   # ป่าคอนกรีตนิวยอร์ก ตึกสี่เหลี่ยม
        sky_city(g, t)
        g.label("ป่าคอนกรีต · นิวยอร์ก", CX, 360, 80, sc=ap(t, L[1]), rot=-3)
        if t > L[2] - 0.2:
            for i in range(4):
                x = 140 + i * 250
                with g.alpha(0.85):
                    g.line([(x - 70, 1180), (x + 70, 1180)], 10, RED, amp=0)
            g.label("สี่เหลี่ยม · สี่เหลี่ยม · สี่เหลี่ยม", CX, 480, 56, color=GREY, sc=ap(t, L[2]))
        return
    if t < L[4] - 0.2:   # อาคารประหลาดผุดขึ้นกลางเมือง
        sky_city(g, t, gap=(260, 820))
        guggenheim(g, 560, GROUND, 0.7, e_out(seg(t, L[3] - 0.2, L[3] + 1.6)), t)
        g.label('"เปลือกหอยสังข์สีขาว"', CX, 360, 74, color=GOLDTXT, sc=ap(t, L[3] + 1.4), rot=-3)
        return
    if t < L[5] - 0.2:   # เปิดประตูต้อนรับครั้งแรก
        g.ground(GROUND, WHITE)
        guggenheim(g, CX + 60, GROUND, 0.8, 1.0, t, glow=ap(t, L[4]))
        for i in range(6):
            u = ((t - L[4]) * 0.25 + i / 6) % 1
            person(g, lerp(-80, 420, u), GROUND + 4, CROWD[i % 5], 0.3, seed=10 + i, turn=0.5, shadow=False)
        g.label("เปิดครั้งแรก!", CX, 360, 90, color=RED, sc=ap(t, L[4]), rot=-4)
        return
    if t < L[6] - 0.2:   # ตัวตลกของวงการศิลปะ
        g.ground(GROUND, WHITE)
        guggenheim(g, 640, GROUND, 0.62, 1.0, t)
        person(g, 160, GROUND, CRITICS[0], 0.62, mood="smile", pose="point", turn=0.4, talk=True, seed=3)
        for i in range(3):
            u = (t * 0.7 + i / 3) % 1
            g.label("ฮ่า ๆ", 260 + i * 200, 620 - 140 * u, 50, color=GREY, a=1 - u)
        g.label("ตัวตลกของวงการศิลปะ?", CX, 360, 70, color=RED, sc=ap(t, L[5]), rot=-3)
        return
    if t < L[8] - 0.2:   # หยาดเหงื่อ + ลมหายใจสุดท้ายของสถาปนิก (เงา)
        g.ground(GROUND, WHITE)
        drafting_table(g, 650, GROUND, 1.0)
        with g.silhouette(INK, 0.9):
            person(g, 300, GROUND, WRIGHT, 0.85, pose="hold", turn=0.4, seed=1)
        for i in range(3):   # หยดเหงื่อ
            u = (t * 0.9 + i / 3) % 1
            g.sweat(380 + i * 30, 360 + u * 120, 1.1)
        g.label("หยาดเหงื่อ", 720, 420, 70, sc=ap(t, L[6]), rot=-3)
        if t > L[7] - 0.2:
            g.label("ลมหายใจสุดท้าย", 720, 1150, 62, color=NAVY, sc=ap(t, L[7]))
        return
    # ไม่ได้เห็นวันเปิดตัว: หมวก + ไม้เท้า บนเก้าอี้ว่าง หันหน้าหาตึก
    g.ground(GROUND, WHITE)
    guggenheim(g, 700, GROUND, 0.55, 1.0, t)
    empty_chair(g, 200, GROUND, 0.9)
    hat_and_cane(g, 200, GROUND - 210, 0.7, glow=seg(t, L[8], L[8] + 1.5), t=t)
    g.label("ไม่มีโอกาสได้เห็น", CX, 360, 76, color=NAVY, sc=ap(t, L[8]), rot=-3)


# ------------------------------------------------------------------ 2. wright
def s_wright(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:   # ย้อนกลับไป 1943
        g.calendar(CX, 760, 1.5, "1943", "ย้อนไป", "กว่า 15 ปีก่อน", flip=None)
        g.label("ย้อนกลับไป...", CX, 360, 84, sc=ap(t, 0.2), rot=-3)
        return
    if t < L[2] - 0.2:   # แฟรงก์ ลอยด์ ไรต์
        g.sunburst(CX, 720, 260, 640, 22, t * 10, 12, (0.95, 0.85, 0.55, 0.8))
        person(g, CX, GROUND, WRIGHT, 0.92, mood="smug", seed=1, turn=0.15, pose="down")
        cane(g, CX + 120, GROUND, 0.9, 4)
        g.label('"แฟรงก์ ลอยด์ ไรต์"', CX, 340, 84, color=GOLDTXT, sc=ap(t, L[1]), rot=-3)
        g.name_tag(t, L[1] + 0.5, 790, 1120, "แฟรงก์ ลอยด์ ไรต์", "สถาปนิกชาวอเมริกัน", side=-1)
        return
    if t < L[3] - 0.2:   # โจทย์: พิพิธภัณฑ์กุกเกนไฮม์
        person(g, 260, GROUND, WRIGHT, 0.8, mood="smile", pose="hold", turn=0.3, seed=1)
        letter(g, 700, 720, 0.95, -4, "โจทย์ใหม่")
        g.label("พิพิธภัณฑ์", 700, 700, 60, color=NAVY, sc=ap(t, L[2] + 0.5))
        g.label("กุกเกนไฮม์", 700, 780, 66, color=NAVY, sc=ap(t, L[2] + 0.8))
        return
    if t < L[4] - 0.2:   # ตึกสี่เหลี่ยมแบ่งห้องแบบเดิม ๆ
        box_building(g, 660, GROUND, 520, 760, 1.0)
        person(g, 200, GROUND, WRIGHT, 0.75, mood="neutral", pose="think", turn=0.4, seed=1)
        g.label("แบบเดิม ๆ", 660, 380, 84, color=GREY, sc=ap(t, L[3]), rot=-3)
        return
    tear = e_out(seg(t, L[4] + 0.3, L[4] + 1.0))   # ฉีกตำราทิ้ง
    person(g, 230, GROUND, WRIGHT, 0.8, mood="smug", pose="fist", turn=0.3, seed=1)
    book(g, 680, 760, 1.6, tear)
    g.label("ฉีกทุกตำรา!", 680, 1100, 80, color=RED, sc=ap(t, L[4] + 0.6), rot=-4)


# ------------------------------------------------------------------ 3. spiral
def s_spiral(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:   # ทางลาดวนเป็นเกลียว
        k = e_io(seg(t, 0.1, 2.6))
        blueprint(g, 220, 420, 0.5 * ap(t, 0.2), -6)
        spiral_cut(g, 580, 520, 1180, t, walkers=False, k=k)
        g.label("ทางลาดเกลียว", 580, 360, 76, sc=ap(t, 0.6), rot=-3)
        return
    if t < L[2] - 0.2:   # ขึ้นลิฟต์ไปชั้นบนสุด
        spiral_cut(g, CX, 520, 1180, t, walkers=False, car=False)
        u = e_io(seg(t, L[1], L[1] + 1.6))
        _rr(g.c, CX - 24, lerp(1120, 470, u), 48, 56, 4)
        _shade(g.c, RED, 4, 0.2)
        g.line([(CX + 90, 1000), (CX + 90, 640)], 14, RED, amp=0)
        g.poly([(CX + 60, 650), (CX + 90, 600), (CX + 120, 650)], RED, 0)
        g.label("ขึ้นลิฟต์ไปชั้นบนสุด", CX, 360, 70, sc=ap(t, L[1]), rot=-3)
        return
    spiral_cut(g, CX, 520, 1180, t * 3, walkers=True, wall_art=True)   # เดินไหลลงเหมือนสายน้ำ
    for i in range(3):
        y = 1210 + i * 18
        g.line([(140 + j * 40, y + 8 * math.sin(t * 4 + j + i)) for j in range(21)], 5, hexc("#8fb8de"), amp=0)
    g.label("ไหลลงเหมือนสายน้ำ", CX, 360, 74, color=NAVY, sc=ap(t, L[2]), rot=-3)


# ------------------------------------------------------------------ 4. mock
def s_mock(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # คำดูถูก + แบบแปลนถูกเปิดเผย
        for i, (lk, x) in enumerate(zip(CRITICS, (180, CX, 880))):
            person(g, x, GROUND + 8 * abs(math.sin(t * 8 + i)), lk, 0.7, mood="smile" if t > L[1] else "smug",
                   turn=0.2 * (1 - i), seed=5 + i, talk=t > L[1])
        if t < L[1] - 0.2:
            g.label("คำดูถูกแสนสาหัส", CX, 360, 80, color=RED, sc=ap(t, 0.2), rot=-3)
        else:
            blueprint(g, CX, 420, 0.75 * ap(t, L[1]), 3)
            for i in range(4):   # แฟลชกล้องนักข่าว
                if (t * 3 + i * 0.37) % 1 < 0.15:
                    g.sparkle(160 + i * 250, 600 + 60 * (i % 2), 30, WHITE)
        return
    if t < L[3] - 0.2:   # เครื่องซักผ้ายักษ์
        guggenheim(g, 300, GROUND, 0.45, 1.0, t)
        g.label("=", 560, 1000, 110, sc=ap(t, L[2] + 0.3))
        washing_machine(g, 800, GROUND, 1.0, t)
        g.label("เครื่องซักผ้ายักษ์!", CX, 380, 80, color=RED, sc=ap(t, L[2]), rot=-4)
        return
    guggenheim(g, 300, GROUND, 0.45, 1.0, t)   # โถส้วมยักษ์
    g.label("=", 560, 1000, 110, sc=ap(t, L[3] + 0.3))
    toilet(g, 800, GROUND, 1.1)
    g.label("โถส้วมยักษ์กลางเมือง!", CX, 380, 74, color=RED, sc=ap(t, L[3]), rot=-4)


# ------------------------------------------------------------------ 5. artists
def s_artists(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:   # ศิลปินรวมตัวส่งจดหมายประท้วง
        for i, (lk, x) in enumerate(zip(ARTISTS, (170, CX, 870))):
            person(g, x, GROUND, lk, 0.68, mood="angry", pose="fist" if (int(t * 2) + i) % 2 else "down",
                   turn=0.2 * (1 - i), seed=20 + i, talk=True)
        letter(g, CX, 520, 0.7 * ap(t, 0.8), 5 * math.sin(t))
        g.label("ศิลปินชื่อดังประท้วง!", CX, 340, 72, color=RED, sc=ap(t, 0.2), rot=-3)
        return
    if t < L[2] - 0.2:   # ภาพสี่เหลี่ยมบนผนังโค้ง
        c = g.c
        c.new_path()
        c.arc(CX, 1800, 1100, math.radians(235), math.radians(305))
        c.set_source_rgba(*INK)
        c.set_line_width(10)
        c.stroke()
        for i, a in enumerate((250, 270, 290)):
            r = math.radians(a)
            painting(g, CX + math.cos(r) * 1030, 1800 + math.sin(r) * 1030, 170, 130, a - 270 + 12 * math.sin(t * 2 + i),
                     seed=i)
        g.label("ภาพสี่เหลี่ยม", CX, 360, 72, sc=ap(t, L[1]), rot=-3)
        g.label("บนผนังโค้ง?!", CX, 1140, 72, color=RED, sc=ap(t, L[1] + 0.8))
        return
    spiral_cut(g, CX, 520, 1180, t * 3, walkers=False, wall_art=True)   # พื้นลาดแย่งซีน
    person(g, 140, GROUND, ARTISTS[0], 0.5, mood="angry", pose="point", turn=0.4, seed=20, shadow=False)
    g.label("แย่งซีนงานศิลปะ!", CX, 360, 76, color=RED, sc=ap(t, L[2]), rot=-4)


# ------------------------------------------------------------------ 6. fight
def s_fight(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:   # ต่อสู้กว่า 15 ปีกับคำถากถาง
        drafting_table(g, 660, GROUND, 1.1)
        person(g, 260, GROUND, WRIGHT, 0.8, mood="firm", pose="hold", turn=0.4, seed=1)
        yr = int(lerp(1943, 1958, e_io(seg(t, 0.3, L[1] - 0.3))))
        g.label(str(yr), 660, 420, 110, color=RED, sc=ap(t, 0.2))
        for i, s in enumerate(("บ้าไปแล้ว!", "ไม่มีทาง!")):
            with g.at(760 - i * 80, 640 + i * 150, ap(t, 1.2 + i * 0.8)):
                g.bubble(0, 0, 300, 100, WHITE, tail=(-1, 1))
                g.label(s, 0, 0, 40, color=GREY)
        return
    if t < L[2] - 0.2:   # กฎหมายอาคาร
        rule_book(g, 420, 780, 1.4 * ap(t, L[1]))
        with g.at(720, 900, ap(t, L[1] + 0.8), -12):
            g.rrect(-170, -60, 340, 120, 14, (1, 1, 1, 0), 8, stroke=RED)
            g.label("ไม่อนุมัติ", 0, 0, 56, color=RED)
        g.label("กฎหมายเข้มงวด", CX, 360, 76, sc=ap(t, L[1]), rot=-3)
        return
    if t < L[3] - 0.2:   # โจทย์วิศวกรรม
        spiral_cut(g, CX, 560, 1180, t, walkers=False, k=1.0)
        for i in range(5):
            x, y = 180 + i * 180, 520 + 40 * math.sin(t * 2 + i)
            g.label("?", x, y, 80 + 10 * math.sin(t * 3 + i), color=RED, sc=ap(t, L[2] + i * 0.15))
        g.label("วิศวกรรมแทบเป็นไปไม่ได้", CX, 360, 64, sc=ap(t, L[2]), rot=-3)
        return
    if t < L[4] - 0.2:   # แบบร่างกว่า 700 ชิ้น
        n = int(lerp(0, 749, e_io(seg(t, L[3], L[4] - 0.6))))
        for i in range(min(14, 2 + n // 55)):
            blueprint(g, 300 + (i % 2) * 40 + hn(i, 4) * 30, 1150 - i * 26, 0.6, (hn(i, 5) - 0.5) * 16, spiral=i % 3 == 0)
        person(g, 800, GROUND, WRIGHT, 0.7, mood="firm", pose="fist", turn=-0.3, seed=1)
        g.label(f"{n} ชิ้น" if n < 700 else "กว่า 700 ชิ้น!", 360, 380, 96, color=RED, sc=ap(t, L[3]))
        g.label("แบบร่าง", 360, 480, 56, sc=ap(t, L[3] + 0.2))
        return
    k = e_out(seg(t, L[4] + 0.4, L[4] + 1.6))   # ไม่ต้องขังในกล่อง: เกลียวพุ่งออกจากกล่อง
    c = g.c
    for sx in (-1, 1):
        with g.at(CX + sx * 300 * k, 1000, 1, sx * 30 * k):
            _rr(c, -180 if sx < 0 else 0, -260, 180, 520, 4)
            _shade(c, LGREY, 6, 0.25)
    guggenheim(g, CX, GROUND - 40, 0.35 + 0.35 * k, 1.0, t, glow=k)
    g.label("ไม่ต้องอยู่ในกล่อง!", CX, 360, 80, color=GOLDTXT, sc=ap(t, L[4] + 0.6), rot=-3)


# ------------------------------------------------------------------ 7. death
def s_death(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # โชคชะตาเล่นตลก / ตึกใกล้เสร็จ
        k = 0.7 + 0.25 * e_io(seg(t, 0.2, L[2]))
        guggenheim(g, 560, GROUND, 0.75, k, t)
        c = g.c   # เครนก่อสร้าง
        g.line([(900, GROUND), (900, 380)], 16, GOLD, amp=0)
        g.line([(560, 400), (980, 400)], 14, GOLD, amp=0)
        g.line([(640 + 40 * math.sin(t), 400), (640 + 40 * math.sin(t), 520)], 4, INK, amp=0)
        _rr(c, 610 + 40 * math.sin(t), 520, 60, 40, 4)
        _shade(c, CREAM, 4, 0.2)
        if t < L[1] - 0.2:
            g.label("โชคชะตาเล่นตลก...", CX, 300, 72, color=NAVY, sc=ap(t, 0.2), rot=-3)
        else:
            g.label(f"สร้างเสร็จ {int(k * 100)}%", CX, 300, 72, sc=ap(t, L[1]), rot=-3)
        return
    if t < L[3] - 0.2:   # จากไปในวัย 91 ปี — แทนด้วยเก้าอี้ว่าง หมวก ไม้เท้า
        empty_chair(g, CX, GROUND, 1.2)
        hat_and_cane(g, CX, GROUND - 280, 0.9, glow=seg(t, L[2] + 0.5, L[2] + 1.5), t=t)
        g.label("แฟรงก์ ลอยด์ ไรต์", CX, 340, 72, sc=ap(t, L[2]))
        g.label("1867 – 1959 · วัย 91 ปี", CX, 440, 56, color=GREY, sc=ap(t, L[2] + 0.6))
        return
    g.calendar(380, 760, 1.2, "6", "เดือน", "เม.ย. → ต.ค.")   # เพียงแค่ 6 เดือน
    guggenheim(g, 820, GROUND, 0.35, 1.0, t)
    g.label("ก่อนวันเปิดจริง", 700, 360, 72, color=RED, sc=ap(t, L[3]), rot=-3)


# ------------------------------------------------------------------ 8. opening
def s_opening(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:   # ต่อแถวยาวเหยียด
        guggenheim(g, 820, GROUND, 0.5, 1.0, t)
        for i in range(9):
            x = 80 + i * 66 + 6 * math.sin(t * 3 + i)
            person(g, x, GROUND + 4, CROWD[i % 5], 0.36, seed=30 + i, turn=0.5, shadow=False,
                   mood="smile")
        g.label("ต่อแถวยาวเหยียด!", CX, 360, 80, sc=ap(t, 0.2), rot=-3)
        g.label("นับพันคน", 300, 760, 62, color=RED, sc=ap(t, 1.0))
        return
    if t < L[2] - 0.2:   # สัมผัสความมหัศจรรย์ (มองขึ้นจากโถงกลาง)
        rotunda_up(g, CX, 800, t, e_out(seg(t, L[1] - 0.2, L[1] + 0.8)))
        g.label("ว้าว!", CX, 340, 96, color=GOLDTXT, sc=ap(t, L[1] + 0.4), rot=-4)
        return
    if t < L[3] - 0.2:   # เคยถูกถ่มถุย
        with g.at(CX, 760, 1.2, -6 + 4 * math.sin(t)):
            g.rrect(-260, -170, 520, 340, 8, hexc("#f4efe2"), 6)
            g.label("โถส้วมยักษ์!", 0, -40, 66, color=GREY)
            g.label("เครื่องซักผ้า!", 0, 50, 52, color=GREY)
        g.label("เคยถูกถ่มถุย", CX, 360, 76, color=NAVY, sc=ap(t, L[2]), rot=-3)
        return
    if t < L[4] - 0.2:   # คำสบประมาท -> เสียงชื่นชม
        for i, (lk, x) in enumerate(zip(CROWD[:3], (180, CX, 880))):
            person(g, x, GROUND, lk, 0.62, mood="smile", pose="wave" if (int(t * 3) + i) % 2 else "down",
                   seed=40 + i, turn=0.2 * (1 - i))
        for i in range(6):
            a = t * 1.2 + i * 1.05
            g.sparkle(CX + 380 * math.cos(a), 600 + 140 * math.sin(a), 18)
        g.label("เสียงชื่นชม!", CX, 360, 86, color=GREEN, sc=ap(t, L[3]), rot=-3)
        return
    guggenheim(g, CX + 60, GROUND, 0.8, 1.0, t, glow=1.0)   # สถาปัตยกรรมยิ่งใหญ่แห่งศตวรรษที่ 20
    with g.at(200, 520, ap(t, L[4] + 0.6)):
        g.circle(0, 0, 90, GOLD, 7)
        g.star(0, 0, 50, GOLD2, 5)
        g.poly([(-50, 70), (-80, 200), (-15, 165), (0, 90)], RED, 5)
        g.poly([(50, 70), (80, 200), (15, 165), (0, 90)], NAVY, 5)
    g.label("ยิ่งใหญ่ที่สุด", CX, 340, 84, color=GOLDTXT, sc=ap(t, L[4]), rot=-3)
    g.label("แห่งศตวรรษที่ 20", CX, 450, 62, sc=ap(t, L[4] + 0.4))


# ------------------------------------------------------------------ 9. lesson
def s_lesson(g, t, L, d):
    g.ground(GROUND, WHITE)
    g.label("บทเรียน", CX, 340, 100, sc=ap(t, 0.2), rot=-3)
    if t < L[3] - 0.2:
        n = 5
        for i in range(n):   # กล่องสี่เหลี่ยมเรียงแถว + เกลียวหนึ่งเดียว
            x = 150 + i * 195
            if i == 2:
                guggenheim(g, x + 30, 1080, 0.24, 1.0, t, glow=ap(t, L[1]))
                continue
            look = 0 if t < L[2] else (1 if i < 2 else -1)
            with g.at(x, 1080):
                _rr(g.c, -70, -260, 140, 260, 4)
                _shade(g.c, LGREY, 6, 0.25)
                if t > L[2] - 0.2:   # กล่องหันมองแบบไม่เข้าใจ
                    for sx in (-1, 1):
                        g.circle(sx * 26, -170, 18, WHITE, 4)
                        g.circle(sx * 26 + look * 8, -170, 7, INK, 0)
                    g.line([(-26, -110), (26, -118)], 5, amp=0)
        if t > L[1] - 0.2:
            g.label("ล้ำเกินยุค", 540, 1180, 64, color=GOLDTXT, sc=ap(t, L[1]))
        if t > L[2] - 0.2:
            g.label("แปลกแยก?", CX, 520, 70, color=GREY, sc=ap(t, L[2]))
        return
    glow = seg(t, L[4] - 0.2, L[4] + 1.0)
    guggenheim(g, 700, GROUND, 0.5, 1.0, t, glow=glow)
    empty_chair(g, 210, GROUND, 0.8)
    hat_and_cane(g, 210, GROUND - 190, 0.6, glow=glow, t=t)
    for i in range(5):
        g.sparkle(160 + i * 190, 1150 + 20 * math.sin(t * 3 + i), 14 * ap(t, L[4] + i * 0.2))
    if t < L[4] - 0.2:
        g.label("แม้ผู้สร้างจะจากไป", CX, 480, 64, color=NAVY, sc=ap(t, L[3]))
    else:
        g.label("อยู่เหนือกาลเวลา", CX, 480, 70, color=GOLDTXT, sc=ap(t, L[4]))


# ------------------------------------------------------------------ 10. outro
def s_outro(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # เสียดายแทนไหม
        guggenheim(g, 720, GROUND, 0.42, 1.0, t)
        person(g, 250, GROUND, WRIGHT, 0.8, mood="sad" if t < L[1] else "smile", pose="down", turn=0.4,
               look_at=(1, -0.2), seed=1)
        g.label("เสียดายแทนไหม?", CX, 360, 80, color=NAVY, sc=ap(t, 0.2), rot=-3)
        if t > L[1] - 0.2:
            g.label("ทุ่มเท 15 ปี", 720, 560, 66, color=RED, sc=ap(t, L[1]))
        return
    if t < L[4] - 0.2:   # หรือคุ้มค่าแล้ว — สองทางเลือก
        for i, (txt, col, x) in enumerate((("เสียดาย", NAVY, 260), ("คุ้มค่า!", GREEN, 820))):
            with g.at(x, 760, ap(t, L[2] + i * 0.5) * (1 + 0.04 * math.sin(t * 3 + i))):
                g.rrect(-180, -220, 360, 440, 40, WHITE, 7)
                g.label(txt, 0, 140, 64, color=col)
                if i == 0:
                    g.sweat(0, -60, 4.0)
                else:
                    g.star(0, -60, 90, GOLD2, 6)
        g.label("หรือ", CX, 760, 60, color=GREY, sc=ap(t, L[2] + 0.3))
        g.label("ลงมือจนสุดทาง", CX, 360, 76, sc=ap(t, L[2]), rot=-3)
        return
    with g.at(CX + 120, 650, ap(t, L[4])):   # ชวนคอมเมนต์
        g.bubble(0, 0, 520, 240, WHITE, tail=(-1, 1))
        for i in range(3):
            g.circle(-110 + i * 110, 0, 24 + 6 * math.sin(t * 6 - i), INK, 0)
    person(g, 250, GROUND, WRIGHT, 0.75, mood="smile", pose="wave", turn=0.3, seed=1, talk=True)
    for i in range(5):
        g.sparkle(160 + i * 190, 1180 + 20 * math.sin(t * 3 + i), 14 * ap(t, L[4] + 0.5 + i * 0.3))
    g.label("คอมเมนต์คุยกันได้เลย!", 700, 1150, 58, color=RED, sc=ap(t, L[4] + 0.4))


SCENES = {
    "hook": s_hook, "wright": s_wright, "spiral": s_spiral, "mock": s_mock, "artists": s_artists,
    "fight": s_fight, "death": s_death, "opening": s_opening, "lesson": s_lesson, "outro": s_outro,
}
NO_IRIS = set()
