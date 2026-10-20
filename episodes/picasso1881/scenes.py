"""ฉากตอน: ปาโบล ปิกัสโซ (เกิด 25 ต.ค. 1881) — ภาพคิวบิสม์/เกอร์นิกาวาดเองแบบสื่อความ"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from chars import (CRITICS, MIDWIFE, PAL, PICASSO, TEEN, UNCLE, YOUNG, brush, cigar, easel, frame,  # noqa: E402
                   guernica, hammer, mirror, painting, palette, school, smoke_puffs)
from gfx import GOLD, GOLD2, GREY, INK, NAVY, RED, W, WHITE, e_io, e_out, hexc, lerp, pop, seg  # noqa: E402
from people import _rr, _shade, head, person  # noqa: E402

CX = W / 2
GROUND = 1270
GOLDTXT = hexc("#b37a12")
GREEN = hexc("#3c8d4f")
BLUE = hexc("#3d6fa8")
PURPLE = hexc("#7a4a9a")

CAMERA = {"hook": "push_in", "birth": "pan_right", "prodigy": "push_in", "cubism": "dutch", "guernica": "pan_left",
          "lesson": "pull_out", "outro": "pan_right"}
TRANSITIONS = {"birth": "fade", "prodigy": "whip", "cubism": "zoom", "guernica": "iris", "lesson": "fade",
               "outro": "whip"}


def ap(t, a, dur=0.38):
    return pop(t, a - 0.2, dur)


def title(g, t, a, txt, col=INK, size=84, y=380):
    g.label(txt, CX, y, size, color=col, sc=ap(t, a), rot=-3)


def baby_table(g, x, y, t, cry=0.0, sc=1.0):
    """โต๊ะ + ทารกห่อผ้า (cry 1 = ร้องไห้ ขยับ)"""
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -260, -320, 520, 34, 8)
        _shade(c, hexc("#a8784a"), 6, 0.25)
        for sx in (-1, 1):
            g.line([(sx * 220, -290), (sx * 220, 0)], 14, INK, amp=0)
        wig = 6 * math.sin(t * 14) * cry
        with g.at(0, -350 + wig * 0.3, 1, wig):
            g.blob(20, 0, 140, 50, hexc("#cfe0f0"), 5)
            g.circle(-110, -10, 48, hexc("#f2c9a8"), 5)
            if cry > 0.5:
                g.circle(-110, 8, 14, hexc("#7a2e2e"), 3)
                for ex in (-130, -92):
                    g.line([(ex - 9, -24), (ex + 9, -20)], 4, INK, amp=0)
                for i in range(3):
                    g.arc(-110, -10, 70 + 26 * i + 10 * ((t * 3) % 1), 200, 250, 5, (0.8, 0.3, 0.2, 0.8))
            else:
                for ex in (-130, -92):
                    g.line([(ex - 9, -22), (ex + 9, -22)], 4, INK, amp=0)


# ------------------------------------------------------------------ 1. hook
def s_hook(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:
        easel(g, CX, GROUND, 0.9, "cubist", t, e_io(seg(t, 0.2, 1.5)))
        g.label("วันนี้ในอดีต", CX, 380, 104, sc=lerp(2.0, 1, e_out(seg(t, 0.1, 0.4))) if t > 0.1 else 0, rot=-3)
        g.label("25 ตุลาคม 1881", CX, 520, 84, color=GOLDTXT, sc=pop(t, 0.6))
        return
    if t < L[3] - 0.2:   # ทารกนิ่ง -> ควันซิการ์
        baby_table(g, 600, GROUND, t, 1.0 if t > L[2] + 0.8 else 0.0, 1.1)
        if t < L[2] - 0.2:
            title(g, t, L[1], "ทารกนอนแน่นิ่ง...", GREY, 92)
        else:
            cigar(g, 860, 820, 1.0, -15, t, 1.0)
            smoke_puffs(g, 760, 880, t, 1.0, 1.4, -1)
            title(g, t, L[2], "ฟื้นด้วยควันซิการ์!", RED, 92)
        return
    if t < L[4] - 0.2:   # ฉีกหน้ามนุษย์ให้เบี้ยว
        person(g, 250, GROUND, PICASSO, 0.8, mood="smug", pose="hold", turn=0.4, seed=1)
        frame(g, 720, 820, 0.95, "cubist", t, 4 * math.sin(t * 2))
        title(g, t, L[3], "ฉีกหน้ามนุษย์ให้เบี้ยวบิด!", PURPLE, 80)
        return
    for i, art in enumerate(("realist", "cubist")):
        frame(g, 300 + i * 480, 820, 0.8, art, t, -4 + 8 * i)
    g.label("→", CX, 820, 120, color=RED, sc=ap(t, L[4]))
    title(g, t, L[4], "เปลี่ยนศิลปะโลกตลอดกาล!", RED, 82)


# ------------------------------------------------------------------ 2. birth
def s_birth(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[3] - 0.2:   # 1881 มาลากา ปาโบล ไม่ร้อง ไม่หายใจ
        if t < L[2] - 0.2:
            g.calendar(CX, 820, 1.0 * pop(t, 0.2), "25", "อังคาร", "ต.ค. 1881")
            if t < L[1] - 0.2:
                title(g, t, L[0], "25 ตุลาคม 1881", GOLDTXT, 92)
            else:
                g.label("มาลากา · สเปน", CX, 1120, 76, color=RED, sc=ap(t, L[1]))
                title(g, t, L[1], "เมืองมาลากา ประเทศสเปน", INK, 80)
            return
        baby_table(g, CX, GROUND, t, 0.0, 1.2)
        if t < L[3] - 0.2:
            title(g, t, L[2], "ปาโบล ปิกัสโซ", PURPLE, 100)
        return
    if t < L[6] - 0.2:   # ไม่ร้อง ไม่หายใจ / หมอทิ้งไว้บนโต๊ะ
        baby_table(g, 700, GROUND, t, 0.0, 1.0)
        person(g, 220, GROUND, MIDWIFE, 0.75, mood="sad", pose="shrug" if t > L[4] - 0.2 else "down", turn=0.4,
               seed=2)
        if t < L[4] - 0.2:
            for i, txt in enumerate(("ไม่ร้อง", "ไม่หายใจ")):
                with g.at(700, 600 + i * 130, ap(t, L[3] + 0.4 * i), -4 + 8 * i):
                    g.rrect(-170, -50, 340, 100, 26, WHITE, 6, stroke=RED)
                    g.label(txt, 0, 0, 56, color=RED)
            title(g, t, L[3], "ไม่ร้อง ไม่หายใจ...", GREY, 88)
        elif t < L[5] - 0.2:
            title(g, t, L[4], "หมอหมดหวัง ทิ้งไว้บนโต๊ะ", INK, 78)
        else:
            title(g, t, L[5], "คิดว่าตายแล้ว...", GREY, 92)
        return
    if t < L[8] - 0.2:   # ลุงหมอสูบซิการ์ พ่นควัน
        cry = 0.0
        baby_table(g, 760, GROUND, t, cry, 0.9)
        person(g, 300, GROUND, UNCLE, 0.8, mood="smug", pose="phone", turn=0.5, seed=3)
        cigar(g, 420, 545, 0.55, -10, t, 0.0)
        g.name_tag(t, L[6] + 0.1, 300, 1140, "ลุงซัลวาดอร์", "หมอ น้องชายของพ่อ")
        if t < L[7] - 0.2:
            title(g, t, L[6], "คุณลุงหมอสูบซิการ์!", GOLDTXT, 84)
        else:
            smoke_puffs(g, 470, 560, t, 1.0, 1.8)
            title(g, t, L[7], "พ่นควันใส่หน้าทารก!", RED, 84)
        return
    baby_table(g, CX, GROUND, t, 1.0, 1.2)   # สำลัก ร้องลั่น รอด
    smoke_puffs(g, CX - 200, 780, t, 0.5, 1.2)
    if t < L[9] - 0.2:
        g.label("แง!!", CX + 260, 700, 110, color=RED, sc=ap(t, L[8] + 0.3), rot=10 * math.sin(t * 8))
        title(g, t, L[8], "สำลักควัน ร้องลั่น!", RED, 90)
    else:
        for i in range(5):
            g.sparkle(CX + 330 * math.cos(i * 1.25 + t), 860 + 250 * math.sin(i * 1.25 + t), 34)
        title(g, t, L[9], "รอดราวกับปาฏิหาริย์!", GREEN, 88)


# ------------------------------------------------------------------ 3. prodigy
def s_prodigy(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # วาดก่อนพูด
        person(g, 300, GROUND, TEEN, 0.75, mood="smile", pose="sign", turn=0.4, seed=4)
        easel(g, 720, GROUND, 0.8, "child", t)
        if t < L[1] - 0.2:
            title(g, t, L[0], "ตั้งแต่จำความได้...", INK, 88)
        else:
            with g.at(560, 560, ap(t, L[1])):
                g.bubble(0, 0, 200, 140, WHITE, tail=(-1, 1))
                brush(g, 0, 40, 0.5, 30)
            title(g, t, L[1], "วาดรูปได้ก่อนพูดเป็นคำ!", PURPLE, 80)
        return
    if t < L[4] - 0.2:   # 14 ปี ภาพเหมือนจริงเหนือผู้ใหญ่
        person(g, 260, GROUND, TEEN, 0.85, mood="smug", pose="hold", turn=0.4, seed=4)
        easel(g, 740, GROUND, 0.85, "realist", t)
        if t < L[3] - 0.2:
            g.label("14", 260, 560, 150, color=GOLDTXT, sc=ap(t, L[2]))
            title(g, t, L[2], "ในวัยเพียง 14 ปี", GOLDTXT, 90)
        else:
            title(g, t, L[3], "วาดเก่งเกินผู้ใหญ่!", BLUE, 90)
        return
    if t < L[5] - 0.2:   # สอบเข้าโรงเรียนศิลปะ
        school(g, 700, GROUND, 1.0)
        person(g, 230, GROUND, TEEN, 0.8, mood="smile", pose="v", turn=0.4, seed=4)
        with g.at(700, 520, ap(t, L[4] + 0.4), -10):
            g.rrect(-150, -60, 300, 120, 20, WHITE, 8, stroke=GREEN)
            g.label("ผ่าน!", 0, 0, 72, color=GREEN)
        title(g, t, L[4], "สอบผ่านในไม่กี่วัน!", GREEN, 88, y=330)
        return
    person(g, 260, GROUND, YOUNG, 0.8, mood="firm" if t < L[6] - 0.2 else "smug", pose="think", turn=0.4, seed=5)
    easel(g, 740, GROUND, 0.85, "realist", t)
    if t < L[6] - 0.2:
        title(g, t, L[5], "แต่เขาไม่เหมือนใคร...", PURPLE, 88)
    else:
        with g.at(740, 860, ap(t, L[6])):
            g.line([(-200, -200), (200, 200)], 16, RED, amp=0)
        title(g, t, L[6], "ไม่พอใจแค่ \"เหมือนจริง\"!", RED, 84)


# ------------------------------------------------------------------ 4. cubism
def s_cubism(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[3] - 0.2:   # คำพูด ราฟาเอล / วาดให้เหมือนเด็ก
        person(g, 240, GROUND, PICASSO, 0.8, mood="smile", pose="point", turn=0.4, seed=1, talk=True)
        g.name_tag(t, L[0] + 0.1, 240, 1140, "ปาโบล ปิกัสโซ", "ศิลปินชาวสเปน (1881–1973)")
        if t < L[1] - 0.2:
            frame(g, 760, 780, 0.8, "realist", t)
            title(g, t, L[0], "เขาเคยกล่าวไว้ว่า...", INK, 88)
        elif t < L[2] - 0.2:
            frame(g, 760, 780, 0.8, "realist", t)
            g.label("ราฟาเอล", 760, 1070, 60, color=GOLDTXT, sc=ap(t, L[1]))
            title(g, t, L[1], "\"วาดเหมือนราฟาเอลได้...\"", GOLDTXT, 80)
        else:
            frame(g, 760, 780, 0.8, "child", t, 3 * math.sin(t * 2))
            title(g, t, L[2], "\"...ทั้งชีวิตเพื่อวาดให้เหมือนเด็ก\"", BLUE, 68)
        return
    if t < L[6] - 0.2:   # ฉีกกรอบ / สลายร่างเป็นเรขาคณิต / หลายมุมมอง
        if t < L[4] - 0.2:
            hammer(g, 760, 820, 1.0 * ap(t, L[3]) + 0.01, lerp(-30, 30, (math.sin(t * 6) + 1) / 2))
            frame(g, 400, 820, 0.7, "realist", t, -6)
            title(g, t, L[3], "ฉีกทุกกรอบความงามแบบเดิม!", RED, 78)
        elif t < L[5] - 0.2:
            for i in range(9):
                a = i * 0.7 + t * 0.3
                sz = 60 + 20 * (i % 3)
                with g.at(CX + 300 * math.cos(a) * ap(t, L[4]), 820 + 260 * math.sin(a) * ap(t, L[4]), 1, t * 30 + i * 40):
                    if i % 3 == 0:
                        g.poly([(-sz, sz), (sz, sz), (0, -sz)], PAL[i % 6], 5, amp=0)
                    elif i % 3 == 1:
                        g.rrect(-sz, -sz, 2 * sz, 2 * sz, 4, PAL[i % 6], 5)
                    else:
                        g.circle(0, 0, sz, PAL[i % 6], 5)
            title(g, t, L[4], "สลายเป็นรูปทรงเรขาคณิต", PURPLE, 80)
        else:
            with g.at(CX, 820 + 15 * math.sin(t * 2), (1.5 + 0.06 * math.sin(t * 1.7)) * ap(t, L[5]) + 0.01,
                      5 * math.sin(t * 1.4)):
                painting(g, 0, 0, 1.0, "cubist", t)
            for i, (lx, ly, txt) in enumerate(((180, 640, "ตา"), (900, 760, "จมูก"), (220, 1080, "ปาก"))):
                g.label(txt, lx, ly + 10 * math.sin(t * 3 + i), 60, color=PURPLE, sc=ap(t, L[5] + 0.4 + 0.3 * i))
            title(g, t, L[5], "ตา จมูก ปาก หลายมุมพร้อมกัน!", PURPLE, 74)
        return
    if t < L[8] - 0.2:   # คิวบิซึม
        with g.at(CX, 820 + 15 * math.sin(t * 2), 1.5 + 0.05 * math.sin(t * 1.5), 4 * math.sin(t * 1.3)):
            painting(g, 0, 0, 1.0, "cubist", t)
        for i in range(4):
            g.sparkle(CX + 380 * math.cos(i * 1.57 + t * 0.8), 820 + 380 * math.sin(i * 1.57 + t * 0.8), 26)
        g.label("CUBISM", CX, 520, 110, color=BLUE, sc=ap(t, L[7]), rot=-4) if t > L[7] - 0.2 else None
        title(g, t, L[6] if t < L[7] - 0.2 else L[7], "หลายมุมมองในภาพเดียว" if t < L[7] - 0.2 else "ลัทธิ \"คิวบิซึม\"",
              PURPLE, 84, y=330)
        return
    frame(g, CX, 640, 0.7, "cubist", t, 3 * math.sin(t * 9) * (t > L[8] - 0.2))   # วงการสั่นสะเทือน วิจารณ์ว่าบ้า
    for i in range(3):
        person(g, 180 + i * 360, GROUND, CRITICS[i], 0.55, mood="shock" if t < L[9] - 0.2 else "angry",
               pose="shrug" if i != 1 else "point", turn=0.3 - 0.3 * i, seed=30 + i, talk=t > L[9] - 0.2)
    if t < L[9] - 0.2:
        title(g, t, L[8], "วงการศิลปะสั่นสะเทือน!", RED, 84, y=330)
    else:
        for i, x in enumerate((180, 900)):
            g.label("บ้า!", x, 760, 70, color=RED, sc=ap(t, L[9] + 0.2 * i), rot=-10 + 20 * i)
        title(g, t, L[9], "รุมวิจารณ์ว่าเขาบ้า!", RED, 88, y=330)


# ------------------------------------------------------------------ 5. guernica
def s_guernica(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # ภาพเบี้ยว ๆ แฝงพลังอารมณ์
        frame(g, CX, 820, 0.95, "cubist", t)
        if t < L[1] - 0.2:
            title(g, t, L[0], "แต่ภาพเบี้ยว ๆ เหล่านั้น...", INK, 82)
        else:
            for i in range(3):
                g.arc(CX, 820, 300 + 40 * i + 20 * math.sin(t * 4), 0, 360, 6, (0.8, 0.3, 0.3, 0.5 - 0.15 * i))
            title(g, t, L[1], "พลังอารมณ์รุนแรงที่สุด!", RED, 84)
        return
    if t < L[5] - 0.2:   # เกอร์นิกา
        guernica(g, CX, 840, 1.0, t, e_io(seg(t, L[2] - 0.2, L[2] + 1.0)))
        if t < L[3] - 0.2:
            title(g, t, L[2], "\"เกอร์นิกา\" (Guernica)", INK, 92)
        elif t < L[4] - 0.2:
            g.label("ภาพขาวดำขนาด 3.5 × 7.8 เมตร", CX, 1160, 50, color=GREY, sc=ap(t, L[3] + 0.3))
            title(g, t, L[3], "สะท้อนความโหดร้ายของสงคราม", INK, 76)
        else:
            c = g.c
            c.rectangle(-500, 140, 2100, 1130)
            c.set_source_rgba(0.2, 0.2, 0.22, 0.15)
            c.fill()
            title(g, t, L[4], "ทรงพลังจนกองทัพนาซีผวา!", RED, 80)
        return
    if t < L[7] - 0.2:   # 50,000 ชิ้น
        person(g, 230, GROUND, PICASSO, 0.75, mood="smile", pose="hold", turn=0.4, seed=1)
        for i in range(12):
            k = pop(t, L[5] - 0.2 + 0.07 * i)
            if k < 0.02:
                continue
            frame(g, 520 + (i % 4) * 140, 560 + (i // 4) * 220, 0.27 * k, ["cubist", "realist", "child"][i % 3], t,
                  -6 + 4 * (i % 4))
        n = int(lerp(0, 50000, e_out(seg(t, L[5], L[5] + 1.6))))
        g.label(f"{n:,} ชิ้น", 730, 1180, 76, color=GOLDTXT, sc=ap(t, L[5]))
        title(g, t, L[5] if t < L[6] - 0.2 else L[6], "ผลงานกว่า 50,000 ชิ้น!" if t < L[6] - 0.2 else "และพิสูจน์ให้เห็นว่า...",
              GOLDTXT if t < L[6] - 0.2 else INK, 84)
        return
    if t < L[8] - 0.2:   # ไม่ใช่กระจกเงา
        mirror(g, CX, 820, 1.2 * ap(t, L[7]) + 0.01, 0.0)
        title(g, t, L[7], "ไม่ใช่แค่กระจกเงา...", BLUE, 88)
        return
    mirror(g, 380, 820, 1.0, e_out(seg(t, L[8] + 0.3, L[8] + 0.6)))   # ค้อนทุบกรอบเดิม
    hammer(g, 640, 700, 1.1, lerp(30, -40, e_io(seg(t, L[8], L[8] + 0.4))))
    if t < L[9] - 0.2:
        title(g, t, L[8], "แต่คือค้อนทุบกรอบเดิม!", RED, 84)
    else:
        frame(g, 780, 980, 0.5 * ap(t, L[9]) + 0.01, "cubist", t, 6)
        title(g, t, L[9], "สร้างมุมมองใหม่ให้โลก", GREEN, 84)


# ------------------------------------------------------------------ 6. lesson
def s_lesson(g, t, L, d):
    g.ground(GROUND, WHITE)
    person(g, 250, GROUND, PICASSO, 0.8, mood="smile", pose="hold" if t < L[2] - 0.2 else "v", turn=0.4, seed=1)
    if t < L[1] - 0.2:
        palette(g, 740, 820, 1.1 * ap(t, L[0]) + 0.01, 8 * math.sin(t * 2))
        title(g, t, L[0], "ปิกัสโซเตือนใจเราว่า...", INK, 84)
    elif t < L[2] - 0.2:
        frame(g, 740, 820, 0.8, "realist", t)
        with g.at(740, 820, ap(t, L[1])):
            g.line([(-200, -200), (200, 200)], 14, RED, amp=0)
        title(g, t, L[1], "ไม่ใช่ความสวยไร้ที่ติ", GREY, 84)
    else:
        frame(g, 740, 820, 0.8, "cubist", t, 4 * math.sin(t * 3))
        for i in range(4):
            g.sparkle(740 + 260 * math.cos(i * 1.6 + t), 820 + 260 * math.sin(i * 1.6 + t), 34)
        title(g, t, L[2], "แต่คือความกล้าที่จะแตกต่าง!", RED, 78)


# ------------------------------------------------------------------ 7. outro
def s_outro(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:
        frame(g, 720, 800, 0.8, "cubist", t, 3 * math.sin(t * 2))
        person(g, 240, GROUND, CRITICS[1], 0.75, mood="neutral" if t < L[1] - 0.2 else "think", pose="think",
               turn=0.4, seed=40)
        title(g, t, L[0] if t < L[1] - 0.2 else L[1], "ทุกคนล่ะครับ..." if t < L[1] - 0.2 else "มองแล้วรู้สึกอย่างไร?",
              INK, 88)
        return
    if t < L[4] - 0.2:   # อัจฉริยะ หรือ แปลก
        frame(g, CX, 1060, 0.5, "cubist", t)
        for i, (txt, col) in enumerate((("อัจฉริยะล้ำยุค", GREEN), ("ภาพแปลก เข้าถึงยาก", RED))):
            k = ap(t, L[2] + 0.2) if i == 0 else ap(t, L[3])
            if k < 0.02:
                continue
            with g.at(CX, 540 + i * 220, k, -3 + 6 * i):
                g.rrect(-320, -75, 640, 150, 36, WHITE, 8, stroke=col)
                g.label(txt, 0, 0, 60, color=col)
        g.label("หรือ", CX, 650, 56, sc=ap(t, L[3]))
        title(g, t, L[2], "คุณมองแบบไหน?", PURPLE, 88, y=360)
        return
    with g.at(CX + 170, 640, ap(t, L[4])):   # ชวนคอมเมนต์
        g.bubble(0, 0, 460, 220, WHITE, tail=(-1, 1))
        for i in range(3):
            g.circle(-110 + i * 110, 0, 24 + 6 * math.sin(t * 6 - i), INK, 0)
    person(g, 250, GROUND, PICASSO, 0.75, mood="smile", pose="wave", turn=0.3, seed=70, talk=True)
    title(g, t, L[4], "คอมเมนต์แลกเปลี่ยนกันได้เลย!", RED, 64)


SCENES = {
    "hook": s_hook, "birth": s_birth, "prodigy": s_prodigy, "cubism": s_cubism, "guernica": s_guernica,
    "lesson": s_lesson, "outro": s_outro,
}
NO_IRIS = set()
