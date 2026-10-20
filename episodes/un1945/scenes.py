"""ฉากตอน: กำเนิดองค์การสหประชาชาติ (24 ต.ค. 1945) — วันสหประชาชาติ"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from chars import (DELEGATES, HAMMARSKJOLD, UN_BLUE, WORKERS, aid_box, charter, dove, flags_row, globe,  # noqa: E402
                   paper_tiger, red_button, rubble, scales, syringe, table_round)
from gfx import GOLD2, GREY, INK, NAVY, RED, W, WHITE, e_io, e_out, hexc, lerp, pop, seg  # noqa: E402
from people import person  # noqa: E402

CX = W / 2
GROUND = 1270
GOLDTXT = hexc("#b37a12")
GREEN = hexc("#3c8d4f")
DARK = hexc("#4a3a3a")

CAMERA = {"hook": "push_in", "charter": "pan_right", "mission": "pan_left", "critics": "dutch", "hope": "push_in",
          "lesson": "pull_out", "outro": "pan_right"}
TRANSITIONS = {"charter": "fade", "mission": "zoom", "critics": "whip", "hope": "iris", "lesson": "fade",
               "outro": "whip"}


def ap(t, a, dur=0.38):
    return pop(t, a - 0.2, dur)


def delegates(g, t, x0=130, gap=210, sc=0.55, mood="neutral", pose="down", talk=False, n=5):
    for i in range(n):
        person(g, x0 + i * gap, GROUND, DELEGATES[i % 5], sc, mood=mood, pose=pose if i % 2 == 0 else "down",
               turn=0.3 - 0.15 * i, seed=10 + i, talk=talk, shadow=False)


def haze(g, a):
    g.c.rectangle(-500, 140, 2100, 1130)
    g.c.set_source_rgba(0.5, 0.47, 0.44, a)
    g.c.fill()


# ------------------------------------------------------------------ 1. hook
def s_hook(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:
        globe(g, CX, 820, 230 * pop(t, 0.4) + 1, t)
        g.label("วันนี้ในอดีต", CX, 380, 104, sc=lerp(2.0, 1, e_out(seg(t, 0.1, 0.4))) if t > 0.1 else 0, rot=-3)
        g.label("24 ตุลาคม 1945", CX, 510, 84, color=UN_BLUE, sc=pop(t, 0.8))
        return
    if t < L[3] - 0.2:   # ซากปรักหักพัง 70 ล้านชีวิต
        haze(g, 0.25)
        rubble(g, GROUND, t)
        if t < L[2] - 0.2:
            g.label("ซากสงครามโลกครั้งที่ 2", CX, 380, 84, color=DARK, sc=ap(t, L[1]), rot=-3)
        else:
            n = int(70 * e_out(seg(t, L[2], L[2] + 1.6)))
            with g.at(CX, 720, ap(t, L[2])):
                g.rrect(-260, -130, 520, 260, 30, WHITE, 8)
                g.label(f"{n} ล้าน+", 0, -20, 100, color=RED)
                g.label("ชีวิตที่สูญเสีย", 0, 80, 40, color=GREY)
            g.label("ความสูญเสียมหาศาล", CX, 380, 90, color=RED, sc=ap(t, L[2]), rot=-3)
        return
    if t < L[6] - 0.2:   # ถ้ามีสงครามโลกอีกครั้ง...
        g.sunburst(CX, 820, 120, 520, 18, t * 6, 10, (0.9, 0.5, 0.4, 0.35))
        globe(g, CX + 6 * math.sin(t * 20) * (t > L[5] - 0.2), 820, 220, t, olive=False)
        if t < L[4] - 0.2:
            g.label("เกือบทำลายล้างกันเอง", CX, 380, 84, color=DARK, sc=ap(t, L[3]), rot=-3)
        elif t < L[5] - 0.2:
            g.label("ความจริงอันโหดร้าย", CX, 380, 90, color=RED, sc=ap(t, L[4]), rot=-3)
        else:
            g.label("ถ้าเกิดสงครามโลกอีก...", CX, 380, 84, color=RED, sc=ap(t, L[5]), rot=-3)
        return
    haze(g, 0.4 * ap(t, L[6]))   # ไม่มีใครเหลือรอด
    globe(g, CX, 820, 220, t, olive=False)
    g.label("?", CX, 820, 260, color=RED, sc=ap(t, L[6] + 0.3))
    g.label("ไม่มีใครเหลือรอด!", CX, 380, 100, color=RED, sc=ap(t, L[6]), rot=-3)


# ------------------------------------------------------------------ 2. charter
def s_charter(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # จากเถ้าถ่าน -> 51 ประเทศ
        if t < L[1] - 0.2:
            rubble(g, GROUND, t, False)
        else:
            flags_row(g, 60, GROUND - 20, 9, t, 0.15 + 0.85 * e_io(seg(t, L[1] - 0.3, L[1] + 2.0)), 112)
        if t < L[1] - 0.2:
            dove(g, lerp(-100, CX, e_out(seg(t, 0.2, L[1]))), 640, 1.4, t)
            g.label("จากเถ้าถ่านแห่งความพินาศ", CX, 380, 76, color=DARK, sc=ap(t, 0.2), rot=-3)
        else:
            with g.at(CX, 620, ap(t, L[1] + 0.4)):
                g.circle(0, 0, 120, WHITE, 8)
                g.label("51", 0, -14, 100, color=UN_BLUE)
                g.label("ประเทศ", 0, 66, 34, color=GREY)
            g.label("ตัวแทน 51 ประเทศ", CX, 380, 92, color=UN_BLUE, sc=ap(t, L[1]), rot=-3)
        return
    if t < L[4] - 0.2:   # ลงนามกฎบัตร / มีผลวันนี้
        delegates(g, t, 120, 220, 0.5, "smile")
        charter(g, CX, 620, 0.55 * ap(t, L[2]), -2 + math.sin(t), e_io(seg(t, L[2], L[4] - 0.4)))
        if t < L[3] - 0.2:
            g.label('ลงนาม "กฎบัตรสหประชาชาติ"', CX, 380, 72, color=NAVY, sc=ap(t, L[2]), rot=-3)
        else:
            g.label("มีผลบังคับใช้วันนี้!", CX, 380, 90, color=GREEN, sc=ap(t, L[3]), rot=-3)
        return
    if t < L[7] - 0.2:   # กำเนิด UN / พันธสัญญา
        g.sunburst(CX, 800, 260, 620, 22, t * 8, 12, (0.6, 0.8, 1.0, 0.6))
        globe(g, CX, 800, 230, t)
        if t < L[5] - 0.2:
            g.label('"องค์การสหประชาชาติ" (UN)', CX, 380, 74, color=UN_BLUE, sc=ap(t, L[4]), rot=-3)
        elif t < L[6] - 0.2:
            g.label("พันธสัญญาเดียว...", CX, 380, 96, color=NAVY, sc=ap(t, L[5]), rot=-3)
        else:
            with g.at(CX, 1160, ap(t, L[6])):
                g.rrect(-380, -60, 760, 120, 30, WHITE, 7, stroke=RED)
                g.label("ห้ามนองเลือดซ้ำรอยอีก!", 0, 0, 52, color=RED)
            g.label("พันธสัญญาเดียว...", CX, 380, 96, color=NAVY, rot=-3)
        return
    with g.at(CX, 760, ap(t, L[7]) * (1 + 0.03 * math.sin(t * 3)), -3):   # วันสหประชาชาติ
        g.rrect(-260, -200, 520, 400, 30, WHITE, 8)
        g.rrect(-260, -200, 520, 110, 30, UN_BLUE, 8)
        g.text("ตุลาคม", 0, -145, 50, "kanit", WHITE)
        g.label("24", 0, 30, 160)
        g.label("UN Day", 0, 150, 44, color=UN_BLUE)
    g.label('"วันสหประชาชาติ"', CX, 380, 100, color=UN_BLUE, sc=ap(t, L[7]), rot=-3)


# ------------------------------------------------------------------ 3. mission
def s_mission(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[3] - 0.2:   # ไม่มีกองทัพ / ไม่มีอำนาจเบ็ดเสร็จ / ใช้โต๊ะเจรจา
        if t < L[1] - 0.2 or t > L[2] - 0.2:
            table_round(g, CX, GROUND - 40, 860)
            delegates(g, t, 170, 190, 0.45, "neutral", "point", True)
        if t < L[1] - 0.2:
            g.label("ภารกิจไม่ง่าย", CX, 380, 100, sc=ap(t, 0.2), rot=-3)
        elif t < L[2] - 0.2:
            with g.at(CX, 760, ap(t, L[1])):
                g.circle(0, 0, 200, WHITE, 10)
                for k in range(3):
                    g.rrect(-110 + k * 80, -60, 50, 140, 8, hexc("#5f6b45"), 5)
                g.line([(-150, -150), (150, 150)], 22, RED, amp=0)
            g.label("ไม่มีกองทัพเป็นของตัวเอง", CX, 380, 74, color=RED, sc=ap(t, L[1]), rot=-3)
        else:
            g.label("ไม่มีอำนาจสั่งการเบ็ดเสร็จ", CX, 380, 72, color=GREY, sc=ap(t, L[2]), rot=-3)
        return
    if t < L[4] - 0.2:   # โต๊ะเจรจา / กฎบัตร / ความร่วมมือ
        for i, (txt, col) in enumerate((("โต๊ะเจรจา", NAVY), ("กฎบัตร", GOLDTXT), ("ความร่วมมือ", GREEN))):
            with g.at(CX, 620 + i * 200, ap(t, L[3] + 0.5 * i) * (1 + 0.03 * math.sin(t * 3 + i))):
                g.rrect(-260, -70, 520, 140, 30, WHITE, 7, stroke=col)
                g.label(txt, 0, 0, 56, color=col)
        g.label("อาวุธของ UN คือ...", CX, 380, 90, color=UN_BLUE, sc=ap(t, L[3]), rot=-3)
        return
    if t < L[5] - 0.2:   # หยุดสงคราม / ช่วยเหลือมนุษยธรรม
        for i, lk in enumerate(WORKERS):
            person(g, 230 + i * 260, GROUND, lk, 0.62, mood="smile", pose="hold", turn=0.4, seed=30 + i)
        for i in range(3):
            aid_box(g, 700 + i * 120 - 60 * (i == 2), GROUND - (i == 2) * 150, 0.8 * ap(t, L[4] + 0.2 * i))
        dove(g, 760 + 30 * math.sin(t), 560, 1.0, t)
        g.label("หยุดสงคราม ส่งความช่วยเหลือ", CX, 380, 68, color=GREEN, sc=ap(t, L[4]), rot=-3)
        return
    syringe(g, 300, 900 + 10 * math.sin(t * 2), 1.2 * ap(t, L[5]), 20)   # โรคระบาด / สิทธิมนุษยชน
    scales(g, 700, GROUND - 20, 1.0 * ap(t, L[5] + 0.6), t)
    g.label("ปราบโรค ปกป้องสิทธิมนุษยชน", CX, 380, 70, color=UN_BLUE, sc=ap(t, L[5]), rot=-3)


# ------------------------------------------------------------------ 4. critics
def s_critics(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # 80 ปี คำวิจารณ์
        globe(g, CX, 820, 200, t)
        if t < L[1] - 0.2:
            with g.at(CX, 1150, ap(t, 0.3)):
                g.rrect(-180, -50, 360, 100, 20, WHITE, 6)
                g.label("1945 → 2026", 0, 0, 44, color=GREY)
            g.label("กว่า 80 ปี", CX, 380, 110, color=UN_BLUE, sc=ap(t, 0.2), rot=-3)
        else:
            for i in range(6):
                u = (t * 0.6 + i / 6) % 1
                g.label("ห่วย!" if i % 2 else "ไร้น้ำยา!", 150 + i * 160, 1100 - 600 * u, 40, color=RED, a=1 - u)
            g.label("เสียงวิพากษ์วิจารณ์นับไม่ถ้วน", CX, 380, 66, color=RED, sc=ap(t, L[1]), rot=-3)
        return
    if t < L[4] - 0.2:   # เสือกระดาษ
        paper_tiger(g, CX, 1080, 1.4 * ap(t, L[2]), t)
        if t < L[3] - 0.2:
            g.label('"เสือกระดาษ"', CX, 380, 110, color=GOLDTXT, sc=ap(t, L[2]), rot=-3)
        else:
            g.label("ทำอะไรไม่ได้เมื่อมหาอำนาจขัดแย้ง", CX, 380, 60, color=RED, sc=ap(t, L[3]), rot=-3)
        return
    person(g, 260, GROUND, HAMMARSKJOLD, 0.75, mood="smile" if t > L[5] else "neutral", pose="point" if t > L[5]
           else "down", turn=0.3, seed=40, talk=t > L[5])
    g.name_tag(t, L[4] + 0.2, 430, 1140, "ดาก ฮัมมาร์เฮิลด์", "เลขาธิการ UN (1953–1961)")
    if t < L[5] - 0.2:
        g.label("นักการทูตชื่อดังกล่าวว่า...", CX, 380, 76, sc=ap(t, L[4]), rot=-3)
        return
    with g.at(720, 700 + 8 * math.sin(t * 1.5), ap(t, L[5])):
        g.bubble(0, 0, 560, 420, WHITE, tail=(-1, 1))
        g.label("ไม่ได้พาไป", 0, -110, 52, color=GREY)
        g.label("สวรรค์", 0, -40, 62, color=GOLDTXT)
        if t > L[6] - 0.2:
            g.label("แต่กันไม่ให้ตก", 0, 60, 50, sc=ap(t, L[6]))
            g.label("นรก!", 0, 140, 70, color=RED, sc=ap(t, L[6] + 0.2))
    if t > L[6] - 0.2:
        g.label("ปกป้องไม่ให้ตกนรก", CX, 380, 84, color=UN_BLUE, sc=ap(t, L[6]), rot=-3)


# ------------------------------------------------------------------ 5. hope
def s_hope(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # ผู้นำชาตินิวเคลียร์นั่งคุยกัน
        table_round(g, CX, GROUND - 40, 900)
        delegates(g, t, 170, 190, 0.45, "neutral", "point", True)
        if t < L[1] - 0.2:
            with g.at(CX, 620, ap(t, 0.3)):
                g.circle(0, 0, 80, hexc("#f2c94c"), 6)
                for k in range(3):
                    a = math.radians(-90 + k * 120 + t * 30)
                    g.poly([(0, 0), (70 * math.cos(a - 0.5), 70 * math.sin(a - 0.5)),
                            (70 * math.cos(a + 0.5), 70 * math.sin(a + 0.5))], INK, 0, amp=0)
            g.label("ผู้นำชาตินิวเคลียร์", CX, 380, 86, color=DARK, sc=ap(t, 0.2), rot=-3)
        else:
            g.label("ยังนั่งคุยกันในห้องเดียวกัน", CX, 380, 70, color=NAVY, sc=ap(t, L[1]), rot=-3)
        return
    if t < L[3] - 0.2:   # แทนที่จะกดปุ่ม
        red_button(g, CX, 1000, 1.8 * ap(t, L[2]), e_io(seg(t, L[2] + 0.4, L[2] + 1.4)))
        g.label("แทนที่จะกดปุ่มยิง", CX, 380, 92, color=RED, sc=ap(t, L[2]), rot=-3)
        return
    g.sunburst(CX, 800, 230, 580, 20, t * 8, 12, (0.98, 0.85, 0.4, 0.6))   # โลกยังมีหวัง
    globe(g, CX, 800, 200, t)
    dove(g, CX + 230 * math.cos(t), 800 + 230 * math.sin(t), 0.8, t)
    g.label("โลกยังคงมีหวัง", CX, 380, 100, color=GREEN, sc=ap(t, L[3]), rot=-3)


# ------------------------------------------------------------------ 6. lesson
def s_lesson(g, t, L, d):
    g.ground(GROUND, WHITE)
    g.label("บทเรียน", CX, 340, 100, sc=ap(t, 0.2), rot=-3)
    dove(g, CX + 40 * math.sin(t), 800 + 20 * math.sin(t * 2), 1.8 * ap(t, 0.4), t)
    if t < L[1] - 0.2:
        return
    if t < L[2] - 0.2:
        g.label("สันติภาพไม่ได้มาฟรี", CX, 490, 70, color=RED, sc=ap(t, L[1]))
        return
    for i in range(4):   # มือหลายคนช่วยประคอง
        a = math.radians(200 + i * 45)
        g.circle(CX + 260 * math.cos(a), 1000 + 120 * math.sin(a) + 120, 34, (hexc("#efc4a1"), hexc("#8a5a3c"),
                 hexc("#e8c09a"), hexc("#c99a72"))[i], 5)
    g.label("ต้องช่วยกันประคับประคองทุกวัน", CX, 490, 60, color=GREEN, sc=ap(t, L[2]))


# ------------------------------------------------------------------ 7. outro
def s_outro(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[3] - 0.2:
        if t < L[1] - 0.2:
            globe(g, CX, 820, 220, t)
            g.label("รู้สึกอย่างไร?", CX, 380, 100, sc=ap(t, 0.2), rot=-3)
            return
        for i, (txt, col) in enumerate((("ยังดีพอ", GREEN), ("ต้องปฏิรูป", RED))):
            k = ap(t, (L[1], L[2])[i] + 0.2)
            with g.at(290 + i * 500, 780 + 10 * math.sin(t * 2 + i), k):
                g.rrect(-210, -200, 420, 400, 30, WHITE, 7, stroke=col)
                if i == 0:
                    dove(g, 0, -40, 1.0, t)
                else:
                    g.label("!", 0, -40, 140, color=RED)
                g.label(txt, 0, 130, 52, color=col)
        if t < L[2] - 0.2:
            g.label("UN ยังปกป้องสันติภาพได้ไหม?", CX, 380, 70, color=UN_BLUE, sc=ap(t, L[1]), rot=-3)
        else:
            g.label("หรือถึงเวลาปฏิรูปครั้งใหญ่?", CX, 380, 72, color=RED, sc=ap(t, L[2]), rot=-3)
        return
    with g.at(CX + 170, 640, ap(t, L[3])):   # ชวนคอมเมนต์
        g.bubble(0, 0, 460, 220, WHITE, tail=(-1, 1))
        for i in range(3):
            g.circle(-110 + i * 110, 0, 24 + 6 * math.sin(t * 6 - i), INK, 0)
    person(g, 250, GROUND, DELEGATES[3], 0.75, mood="smile", pose="wave", turn=0.3, seed=70, talk=True)
    g.label("คอมเมนต์แลกเปลี่ยนกันได้เลย!", CX, 360, 70, color=RED, sc=ap(t, L[3]), rot=-3)


SCENES = {
    "hook": s_hook, "charter": s_charter, "mission": s_mission, "critics": s_critics, "hope": s_hope,
    "lesson": s_lesson, "outro": s_outro,
}
NO_IRIS = set()
