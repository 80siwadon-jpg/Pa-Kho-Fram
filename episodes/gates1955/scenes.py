"""ฉากตอน: วันเกิดบิล เกตส์ (28 ต.ค. 1955)"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from chars import (ALLEN, GATES, GATES_KID, GATES_MID, GATES_YOUNG, KIDS, MS_BLUE, PARENTS, altair, crown,  # noqa: E402
                   diploma, floppy, garage, grad_cap, hall, heart, ibm_pc, key, magazine, mainframe,
                   money, mosquito, pie, syringe, teletype, virus, window_screen)
from gfx import GOLD, GOLD2, GREY, INK, NAVY, RED, W, WHITE, e_io, e_out, hexc, lerp, pop, seg  # noqa: E402
from people import person  # noqa: E402

CX = W / 2
GROUND = 1270
GOLDTXT = hexc("#b37a12")
GREEN = hexc("#3c8d4f")
CRIMSON = hexc("#a51c30")

CAMERA = {"hook": "push_in", "young": "pan_right", "dropout": "dutch", "deal": "push_in", "giving": "pan_left",
          "lesson": "pull_out", "outro": "pan_right"}
TRANSITIONS = {"young": "zoom", "dropout": "whip", "deal": "iris", "giving": "zoom", "lesson": "fade",
               "outro": "whip"}


def ap(t, a, dur=0.38):
    return pop(t, a - 0.2, dur)


def title(g, t, a, txt, col=INK, size=84, y=380):
    g.label(txt, CX, y, size, color=col, sc=ap(t, a), rot=-3)


def gates(g, x, look=GATES, sc=0.8, mood="smile", pose="down", turn=0.3, talk=False, seed=3):
    person(g, x, GROUND, look, sc, mood=mood, pose=pose, turn=turn, seed=seed, talk=talk)


# ------------------------------------------------------------------ 1. hook
def s_hook(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # เด็กเนิร์ดทิ้งปริญญาฮาร์วาร์ด
        gates(g, 220, GATES_YOUNG, 0.8, "smug", "hold", 0.4)
        diploma(g, 400, 1170, 0.5, 8, e_io(seg(t, L[1] + 1.2, L[1] + 2.0)))
        g.name_tag(t, L[1] + 0.2, 740, 1120, "บิล เกตส์", "ผู้ก่อตั้งไมโครซอฟท์", side=-1)
        title(g, t, L[1], "ทิ้งปริญญาฮาร์วาร์ด!", CRIMSON, 92)
        return
    if t < L[3] - 0.2:   # เดิมพันกล่องคอมพิวเตอร์
        altair(g, CX, 1000, 1.2 * ap(t, L[2]) + 0.01, t)
        g.label("?", CX + 260, 700, 130, color=GREY, sc=ap(t, L[2] + 0.6), rot=8)
        title(g, t, L[2], "เดิมพันกับกล่องคอมพิวเตอร์", MS_BLUE, 82)
        return
    if t < L[4] - 0.2:   # มหาเศรษฐีอันดับหนึ่ง
        money(g, 760, 1150, 1.3, t)
        crown(g, 300, 720 - 10 * math.sin(t * 2), 0.9 * ap(t, L[3] + 0.3) + 0.01, -6)
        gates(g, 300, GATES_MID, 0.72, "smile", "wave", 0.3)
        title(g, t, L[3], "มหาเศรษฐีอันดับหนึ่งของโลก", GOLDTXT, 80)
        return
    for i in range(3):   # เปลี่ยนวิถีชีวิตมนุษยชาติ
        window_screen(g, 250 + i * 290, 800 + 40 * (i % 2), 0.5 * ap(t, L[4] + 0.25 * i, 0.3) + 0.01, t + i)
    for i in range(4):
        g.sparkle(CX + 350 * math.cos(i * 1.6 + t), 1080 + 60 * math.sin(i * 1.6 + t), 26)
    title(g, t, L[4], "เปลี่ยนวิถีชีวิตมนุษยชาติไปตลอดกาล!", MS_BLUE, 74)


# ------------------------------------------------------------------ 2. young
def s_young(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:   # 28 ต.ค. 1955
        g.calendar(CX, 860, 1.25 * ap(t, L[0]) + 0.01, 28, "ศุกร์", "ต.ค. 1955")
        title(g, t, L[0], "28 ตุลาคม 1955", MS_BLUE, 92)
        return
    if t < L[3] - 0.2:   # วิลเลียม เฮนรี เกตส์ ที่สาม / ซีแอตเทิล
        for i, lk in enumerate(PARENTS):
            person(g, 220 + i * 600, GROUND, lk, 0.74, mood="smile", pose="down", turn=0.4 - 0.8 * i, seed=10 + i)
        gates(g, CX, GATES_KID, 0.85, "smile", "wave", 0.0)
        if t < L[2] - 0.2:
            g.label("\"บิล เกตส์\"", CX, 520, 84, color=RED, sc=ap(t, L[1] + 1.4), rot=-4)
            title(g, t, L[1], "วิลเลียม เฮนรี เกตส์ ที่สาม", INK, 80)
        else:
            title(g, t, L[2], "เกิดที่เมืองซีแอตเทิล", GREEN, 88)
        return
    if t < L[5] - 0.2:   # หลงรักการเขียนโค้ดตั้งแต่ 13 / คอมใหญ่เท่าตู้
        if t < L[4] - 0.2:
            teletype(g, 680, GROUND - 60, 1.0, t)
            gates(g, 300, GATES_KID, 0.9, "smile", "point", 0.4)
            with g.at(820, 620, ap(t, L[3] + 0.5), 6):
                g.circle(0, 0, 90, WHITE, 7)
                g.text("13", 0, -10, 70, "kanit", RED)
                g.text("ขวบ", 0, 45, 30, "kanitsb", INK)
            title(g, t, L[3], "หลงรักการเขียนโค้ดตั้งแต่ 13 ปี", MS_BLUE, 76)
        else:
            mainframe(g, 600, GROUND, 1.0, t)
            gates(g, 200, GATES_KID, 0.8, "shock", "down", 0.4)
            g.label("$$$", 840, 620, 80, color=GOLDTXT, sc=ap(t, L[4] + 0.8), rot=8)
            title(g, t, L[4], "คอมพิวเตอร์ใหญ่เท่าตู้เสื้อผ้า!", INK, 78)
        return
    # แอบย่องออกจากบ้านกลางดึก → ฝึกเขียนโปรแกรมอย่างบ้าคลั่ง
    g.circle(820, 520, 60, hexc("#f6e7a8"), 6)
    g.circle(850, 500, 52, WHITE, 0)
    for i in range(5):
        g.star(180 + i * 140, 560 + 40 * math.sin(i * 2.1), 12 + 3 * math.sin(t * 3 + i), GOLD2, 3)
    if t < L[6] - 0.2:
        x = lerp(220, 640, e_io(seg(t, L[5], L[6])))
        gates(g, x, GATES_YOUNG, 0.75, "smug", "down", 0.6)
        title(g, t, L[5], "แอบย่องออกจากบ้านกลางดึก!", NAVY, 82)
    else:
        mainframe(g, 690, GROUND, 0.85, t)
        gates(g, 260, GATES_YOUNG, 0.75, "smile", "point", 0.4)
        title(g, t, L[6], "ฝึกเขียนโปรแกรมอย่างบ้าคลั่ง!", RED, 80)


# ------------------------------------------------------------------ 3. dropout
def s_dropout(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # ที่ฮาร์วาร์ด เห็นนิตยสาร
        if t < L[1] - 0.2:
            hall(g, 640, GROUND, 0.75, t)
            gates(g, 220, GATES_YOUNG, 0.72, "smile", "down", 0.4)
            title(g, t, L[0], "ระหว่างเรียนที่ฮาร์วาร์ด", CRIMSON, 86)
        else:
            magazine(g, 690, 840, 0.95, 5 + 2 * math.sin(t * 2), t)
            gates(g, 260, GATES_YOUNG, 0.8, "shock", "hold", 0.4)
            title(g, t, L[1], "ไมโครคอมพิวเตอร์รุ่นแรก!", RED, 84)
        return
    if t < L[5] - 0.2:   # มองเห็นอนาคต: ทุกโต๊ะ ทุกบ้าน
        if t < L[4] - 0.2:
            for i in range(3):
                u = (t * 1.0 + i / 3) % 1
                g.arc(CX, 860, 120 + 260 * u, 0, 360, 6, (*MS_BLUE[:3], 1 - u))
            gates(g, CX, GATES_YOUNG, 0.82, "smile", "think", 0.0)
            title(g, t, L[2] if t < L[3] - 0.2 else L[3], "มองเห็นอนาคตทันที" if t < L[3] - 0.2 else
                  "ไม่ได้อยู่แค่ในห้องแล็บ", MS_BLUE, 86)
        else:
            for i in range(4):
                x = 200 + (i % 2) * 460
                y = 760 + (i // 2) * 330
                with g.at(x + 100, y, 1):
                    g.rrect(-150, 80, 300, 24, 6, hexc("#b88a52"), 5)
                    window_screen(g, 0, 0, 0.42 * ap(t, L[4] + 0.2 * i, 0.3) + 0.01, t + i)
            title(g, t, L[4], "\"บนทุกโต๊ะทำงานและในทุกบ้าน\"", MS_BLUE, 76)
        return
    if t < L[7] - 0.2:   # พ่อแม่ช็อก / ลาออกจากฮาร์วาร์ด
        for i, lk in enumerate(PARENTS):
            person(g, 640 + i * 220, GROUND, lk, 0.7, mood="shock", pose="down", turn=-0.4, seed=10 + i)
        gates(g, 260, GATES_YOUNG, 0.76, "firm", "down" if t < L[6] - 0.2 else "stop", 0.4)
        if t > L[6] - 0.2:
            diploma(g, 450, 1100, 0.45, -8, e_io(seg(t, L[6] + 0.3, L[6] + 1.0)))
            title(g, t, L[6], "\"ลาออกจากฮาร์วาร์ด\"!", CRIMSON, 92)
        else:
            title(g, t, L[5], "พ่อแม่แทบช็อก!", RED, 96)
        return
    if t < L[8] - 0.2:   # จับมือกับพอล อัลเลน
        gates(g, 320, GATES_YOUNG, 0.8, "smile", "down", 0.4)
        person(g, 760, GROUND, ALLEN, 0.82, mood="smile", pose="wave", turn=-0.4, seed=12)
        g.name_tag(t, L[7] + 0.1, 760, 520, "พอล อัลเลน", "ผู้ร่วมก่อตั้งไมโครซอฟท์", side=-1)
        title(g, t, L[7], "จับมือกับเพื่อนสนิท พอล อัลเลน", INK, 78)
        return
    garage(g, CX, GROUND, 1.0, "Microsoft" if t > L[8] + 1.2 else "")   # ก่อตั้งไมโครซอฟท์
    for i in range(4):
        g.sparkle(CX + 360 * math.cos(i * 1.6 + t), 760 + 140 * math.sin(i * 1.6 + t), 24)
    title(g, t, L[8], "ก่อตั้ง \"ไมโครซอฟท์\"", MS_BLUE, 92)


# ------------------------------------------------------------------ 4. deal
def s_deal(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # สายตาธุรกิจ / ดีลกับ IBM
        gates(g, 280, GATES_MID, 0.82, "smug", "point" if t > L[1] - 0.2 else "think", 0.4, talk=t > L[1] - 0.2)
        if t > L[1] - 0.2:
            with g.at(760, 820, ap(t, L[1] + 0.2), 4):
                g.rrect(-180, -110, 360, 220, 20, hexc("#2b4f8a"), 7)
                g.text("IBM", 0, 0, 110, "kanit", WHITE)
            title(g, t, L[1], "ดีลประวัติศาสตร์กับ IBM", NAVY, 86)
        else:
            title(g, t, L[0], "สายตาทางธุรกิจอันเฉียบคม", INK, 82)
        return
    if t < L[4] - 0.2:   # ขาย MS-DOS แต่เก็บกรรมสิทธิ์
        ibm_pc(g, 640, GROUND - 40, 0.9, t)
        floppy(g, 250, 800, 0.9, -8 + 3 * math.sin(t * 2))
        if t > L[3] - 0.2:
            key(g, 260, 1080, 0.9 * ap(t, L[3]) + 0.01, -15)
            title(g, t, L[3], "แต่ยังเก็บกรรมสิทธิ์ไว้เอง!", GOLDTXT, 82)
        else:
            title(g, t, L[2], "ขายระบบปฏิบัติการ MS-DOS", MS_BLUE, 82)
        return
    if t < L[6] - 0.2:   # Windows ครองกว่า 90%
        if t < L[5] - 0.2:
            window_screen(g, CX, 860, 1.2 * ap(t, L[4]) + 0.01, t)
            title(g, t, L[4], "ต่อยอดเป็น \"Windows\"", MS_BLUE, 92)
        else:
            pie(g, CX, 860, 250, 0.9 * e_out(seg(t, L[5], L[5] + 1.6)), MS_BLUE,
                f"{int(90 * e_out(seg(t, L[5], L[5] + 1.6)))}%+")
            title(g, t, L[5], "ครองคอมพิวเตอร์กว่า 90% ทั่วโลก", MS_BLUE, 78)
        return
    gates(g, 300, GATES_MID, 0.8, "smile", "wave", 0.3)   # เศรษฐีอายุน้อยที่สุด / รวยที่สุดหลายสิบปี
    money(g, 760, 1150, 1.2, t)
    if t < L[7] - 0.2:
        with g.at(760, 700, ap(t, L[6] + 0.3), 6):
            g.circle(0, 0, 110, GOLD, 7)
            g.text("31", 0, -10, 80, "kanit", INK)
            g.text("ปี", 0, 50, 34, "kanitsb", INK)
        title(g, t, L[6], "มหาเศรษฐีสร้างตัวเองที่อายุน้อยที่สุด", GOLDTXT, 72)
    else:
        crown(g, 300, 560 - 10 * math.sin(t * 2), 0.7 * ap(t, L[7]) + 0.01, -6)
        title(g, t, L[7], "รวยที่สุดในโลกหลายสิบปี!", GOLDTXT, 84)


# ------------------------------------------------------------------ 5. giving
def s_giving(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[3] - 0.2:   # ยิ่งใหญ่กว่าเงิน / จุดสูงสุด / วางมือ
        money(g, 760, 1150, 1.2, t)
        gates(g, 300, GATES, 0.82, "smile", "down" if t < L[2] - 0.2 else "wave", 0.3)
        if t < L[1] - 0.2:
            heart(g, 760, 760, 90 * ap(t, L[0] + 0.6) + 1)
            title(g, t, L[0], "ยิ่งใหญ่กว่ากองเงินกองทอง", RED, 84)
        elif t < L[2] - 0.2:
            for i in range(4):
                g.sparkle(300 + 220 * math.cos(i * 1.6 + t), 640 + 120 * math.sin(i * 1.6 + t), 24)
            title(g, t, L[1], "ณ จุดสูงสุดของชีวิต", GOLDTXT, 88)
        else:
            title(g, t, L[2], "วางมือจากไมโครซอฟท์", MS_BLUE, 88)
        return
    if t < L[4] - 0.2:   # มูลนิธิ ทุ่มเงินนับล้านล้านบาท
        gates(g, 280, GATES, 0.8, "smile", "hold", 0.4)
        for i in range(5):
            u = (t * 0.8 + i / 5) % 1
            heart(g, 560 + 80 * i * u, 900 - 300 * u, 30, RED, 1 - u)
        with g.at(760, 1000, ap(t, L[3] + 0.4), 4):
            g.rrect(-220, -90, 440, 180, 20, WHITE, 7, stroke=GREEN)
            g.label("มูลนิธิ", 0, -30, 50, color=GREEN)
            g.label("บิล แอนด์ เมลินดา เกตส์", 0, 34, 36, color=INK)
        title(g, t, L[3], "ทุ่มเงินนับล้านล้านบาท", GOLDTXT, 86)
        return
    if t < L[5] - 0.2:   # กวาดล้างโปลิโอ มาลาเรีย
        virus(g, 300, 820, 120, t, "angry")
        mosquito(g, 760, 820, 1.6, t)
        k = seg(t, L[4] + 1.0, L[4] + 1.6)
        for x in (300, 760):
            if k > 0:
                g.line([(x - 150, 680), (x - 150 + 300 * k, 680 + 300 * k)], 16, RED, amp=0)
        g.label("โปลิโอ", 300, 1060, 52, color=INK)
        g.label("มาลาเรีย", 760, 1060, 52, color=INK)
        title(g, t, L[4], "กวาดล้างโปลิโอ มาลาเรีย", RED, 86)
        return
    for i, lk in enumerate(KIDS[:3]):   # วัคซีนช่วยชีวิตเด็ก
        person(g, 200 + i * 230, GROUND, lk, 0.62, mood="smile", pose="wave" if i == 1 else "down",
               turn=0.3 - 0.2 * i, seed=30 + i)
    syringe(g, 820, 820, 1.0, -30 + 4 * math.sin(t * 2), 1.0)
    for i in range(3):
        heart(g, 200 + i * 230, 620 - 10 * math.sin(t * 3 + i), 30 * ap(t, L[5] + 0.3 * i, 0.3) + 0.1)
    title(g, t, L[5], "วัคซีนช่วยชีวิตเด็กนับล้าน", GREEN, 84)


# ------------------------------------------------------------------ 6. lesson
def s_lesson(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:
        gates(g, CX, GATES, 0.86, "smile", "down", 0.0)
        title(g, t, L[0], "ชีวิตของบิล เกตส์ พิสูจน์ว่า...", INK, 82)
        return
    if t < L[2] - 0.2:   # กล้าทิ้งความมั่นคง
        diploma(g, 300, 820, 0.8, -6, e_io(seg(t, L[1] + 0.5, L[1] + 1.4)))
        g.label("→", CX, 840, 100, color=GREY, sc=ap(t, L[1] + 0.8))
        altair(g, 780, 900, 0.6 * ap(t, L[1] + 1.2) + 0.01, t)
        title(g, t, L[1], "กล้าเสี่ยงทิ้งความมั่นคงเดิม", RED, 82)
        return
    x = lerp(220, 520, e_io(seg(t, L[2], L[2] + 2.5)))   # วิ่งตามสิ่งที่มองเห็นก่อนคนอื่น
    gates(g, x, GATES_YOUNG, 0.78, "smile", "point", 0.5)
    g.sunburst(860, 700, 70, 170, 14, t * 8, 8, (1, 0.85, 0.4, 0.6))
    g.star(860, 700, 60, GOLD2, 5)
    title(g, t, L[2], "วิ่งตามสิ่งที่เห็นก่อนคนอื่น", MS_BLUE, 82)


# ------------------------------------------------------------------ 7. outro
def s_outro(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:
        gates(g, CX, GATES, 0.82, "smile", "wave", 0.0, talk=True)
        title(g, t, L[0], "ประทับใจมุมไหนที่สุด?", INK, 90)
        return
    if t < L[3] - 0.2:   # ทิ้งปริญญาสร้างไมโครซอฟท์ vs มหาเศรษฐีใจบุญ
        gates(g, 200, GATES_YOUNG, 0.7, "smile", "down", 0.3)
        garage(g, 470, GROUND, 0.42, "Microsoft")
        k = ap(t, L[2])
        if k > 0.02:
            gates(g, 800, GATES, 0.7 * k, "smile", "hold", -0.3)
            heart(g, 800, 560, 60 * k)
        g.label("vs", 650, 760, 90, color=GREY, sc=ap(t, L[2] - 0.1))
        if t < L[2] - 0.2:
            title(g, t, L[1], "ทิ้งปริญญามาสร้างไมโครซอฟท์", MS_BLUE, 80)
        else:
            title(g, t, L[2], "หรือมหาเศรษฐีใจบุญ?", RED, 90)
        return
    with g.at(CX + 170, 640, ap(t, L[3])):   # ชวนคอมเมนต์
        g.bubble(0, 0, 460, 220, WHITE, tail=(-1, 1))
        for i in range(3):
            g.circle(-110 + i * 110, 0, 24 + 6 * math.sin(t * 6 - i), INK, 0)
    gates(g, 260, GATES, 0.8, "smile", "wave", 0.3, talk=True)
    title(g, t, L[3], "มาแลกเปลี่ยนกันในคอมเมนต์!", RED, 70)


SCENES = {
    "hook": s_hook, "young": s_young, "dropout": s_dropout, "deal": s_deal, "giving": s_giving,
    "lesson": s_lesson, "outro": s_outro,
}
NO_IRIS = set()
