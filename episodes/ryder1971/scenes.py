"""ฉากตอน: วันเกิดวิโนนา ไรเดอร์ (29 ต.ค. 1971)"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from chars import (BURTON, DEPP, JOYCE, KIDS, PAPS, WINONA, WINONA_90S, WINONA_KID, axe, broken_wall,  # noqa: E402
                   bulbs_wall, camera_flash, candle, cuffs, film_strip, golden_statue, heart, hollywood,
                   phoenix_rise, shopping_bag, siren, spotlight, tabloid, tear_drops, tv_series)
from gfx import GOLD, GOLD2, GREY, INK, NAVY, RED, W, WHITE, e_io, e_out, hexc, lerp, pop, seg  # noqa: E402
from people import person  # noqa: E402

CX = W / 2
GROUND = 1270
GOLDTXT = hexc("#b37a12")
PURPLE = hexc("#6a4a8a")
ST_RED = hexc("#c8322a")

CAMERA = {"hook": "push_in", "young": "pan_right", "fame": "push_in", "fall": "dutch", "comeback": "pull_out",
          "lesson": "pan_left", "outro": "pan_right"}
TRANSITIONS = {"young": "zoom", "fame": "whip", "fall": "fade", "comeback": "iris", "lesson": "zoom",
               "outro": "whip"}


def ap(t, a, dur=0.38):
    return pop(t, a - 0.2, dur)


def title(g, t, a, txt, col=INK, size=84, y=380):
    g.label(txt, CX, y, size, color=col, sc=ap(t, a), rot=-3)


def wn(g, x, look=WINONA, sc=0.82, mood="smile", pose="down", turn=0.3, talk=False, seed=3):
    person(g, x, GROUND, look, sc, mood=mood, pose=pose, turn=turn, seed=seed, talk=talk)


def paps(g, t, x0=560, n=3, sc=0.6):
    for i in range(n):
        person(g, x0 + i * 140, GROUND, PAPS[i % 3], sc, mood="neutral", pose="hold", turn=-0.4, seed=40 + i)
        camera_flash(g, x0 + i * 140 - 30, GROUND - 360 * sc / 0.6 - 20 * i, 0.55, t, i)


# ------------------------------------------------------------------ 1. hook
def s_hook(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # ไอคอนยุค 90s เจ้าแม่สายกอธิก
        spotlight(g, 320, GROUND, t, 1.0)
        wn(g, 320, WINONA, 0.84, "smug", "down", 0.3)
        for i in range(4):
            g.star(720 + 120 * math.cos(i * 1.6 + t), 760 + 140 * math.sin(i * 1.6 + t), 26, PURPLE, 4)
        g.name_tag(t, L[1] + 0.2, 720, 1080, "วิโนนา ไรเดอร์", "นักแสดงไอคอนยุค 90s", side=-1)
        title(g, t, L[1], "ไอคอนสายกอธิกแห่งยุค 90s", PURPLE, 84)
        return
    if t < L[3] - 0.2:   # สื่อรุมขย้ำจากคดีขโมยเสื้อผ้า
        tabloid(g, 300, 860, 0.85, -6 + 2 * math.sin(t * 2))
        paps(g, t, 600, 3, 0.58)
        title(g, t, L[2], "ถูกสื่อรุมขย้ำจนแทบจมดิน", RED, 84)
        return
    bulbs_wall(g, CX, GROUND - 60, 820, t, "")   # คุณแม่แห่งฮอว์กินส์
    wn(g, CX, JOYCE, 0.82, "firm", "fist", 0.0)
    title(g, t, L[3], "คัมแบ็กในฐานะคุณแม่ผู้ไม่ยอมแพ้!", ST_RED, 78)


# ------------------------------------------------------------------ 2. young
def s_young(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[3] - 0.2:   # 29 ต.ค. 1971 มินนิโซตา / วิโนนา ลอรา โฮโรวิทซ์
        if t < L[1] - 0.2:
            g.calendar(CX, 860, 1.25 * ap(t, L[0]) + 0.01, 29, "ศุกร์", "ต.ค. 1971")
            g.label("รัฐมินนิโซตา", CX, 1150, 64, color=NAVY, sc=ap(t, L[0] + 1.4))
            title(g, t, L[0], "29 ตุลาคม 1971", PURPLE, 92)
        else:
            wn(g, CX, WINONA_KID, 0.9, "smile", "wave", 0.0)
            if t < L[2] - 0.2:
                title(g, t, L[1], "วิโนนา ลอรา โฮโรวิทซ์", INK, 86)
            else:
                g.label("\"วิโนนา ไรเดอร์\"", CX, 540, 76, color=PURPLE, sc=ap(t, L[2] + 0.3), rot=-4)
                title(g, t, L[2], "ที่โลกรู้จักในนาม...", INK, 86)
        return
    if t < L[5] - 0.2:   # ครอบครัวโบฮีเมียน คอมมูนไม่มีไฟฟ้า
        if t < L[4] - 0.2:
            wn(g, 300, WINONA_KID, 0.88, "smile", "hold", 0.4)
            with g.at(720, 860, ap(t, L[3] + 0.3), 6):
                g.rrect(-120, -160, 240, 320, 10, hexc("#f4eedf"), 6)
                for i in range(5):
                    g.line([(-80, -110 + i * 50), (80, -110 + i * 50)], 4, GREY, amp=0)
            title(g, t, L[3], "ครอบครัวนักเขียนและศิลปิน", INK, 84)
        else:
            candle(g, 720, GROUND - 40, 1.5, t)
            wn(g, 300, WINONA_KID, 0.88, "neutral", "down", 0.4)
            g.label("ไม่มีไฟฟ้า", 720, 640, 60, color=GREY, sc=ap(t, L[4] + 0.6))
            title(g, t, L[4], "ชุมชนคอมมูนที่ไม่มีไฟฟ้า", NAVY, 84)
        return
    if t < L[6] - 0.2:   # ถูกกลั่นแกล้ง
        wn(g, 280, WINONA_KID, 0.88, "sad", "down", 0.3)
        for i, lk in enumerate(KIDS):
            person(g, 640 + i * 200, GROUND, lk, 0.9, mood="smug", pose="point", turn=-0.4, seed=20 + i)
        tear_drops(g, 280, 760, t)
        title(g, t, L[5], "แปลกแยก จนถูกกลั่นแกล้งหนัก", INK, 82)
        return
    spotlight(g, 320, GROUND, t, 1.0)   # ทิม เบอร์ตัน → Beetlejuice (1988)
    wn(g, 320, WINONA_90S, 0.82, "smile", "down", 0.3)
    person(g, 760, GROUND, BURTON, 0.8, mood="smile", pose="think", turn=-0.4, seed=25)
    if t < L[7] - 0.2:
        g.name_tag(t, L[6] + 0.4, 760, 1080, "ทิม เบอร์ตัน", "ผู้กำกับ", side=-1)
        title(g, t, L[6], "ดวงตาที่เตะตา ทิม เบอร์ตัน", PURPLE, 82)
    else:
        film_strip(g, 560, 560, 0.7 * ap(t, L[7]) + 0.01, -5, "Beetlejuice", hexc("#3a8a4a"), t)
        title(g, t, L[7], "บท ลิเดีย ดีตซ์ (1988)", INK, 86)


# ------------------------------------------------------------------ 3. fame
def s_fame(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[3] - 0.2:   # ดังเป็นพลุแตก / Gen X / ราชินีสายดาร์ก
        spotlight(g, CX, GROUND, t, 1.0)
        wn(g, CX, WINONA, 0.86, "smug" if t > L[2] - 0.2 else "smile", "wave", 0.0)
        for i in range(6):
            u = (t * 0.6 + i / 6) % 1
            g.star(CX + 330 * math.cos(i * 1.05), 820 - 260 * u, 24, (*GOLD2[:3], 1 - u), 4)
        if t < L[1] - 0.2:
            title(g, t, L[0], "ดังเป็นพลุแตกชั่วข้ามคืน!", GOLDTXT, 86)
        elif t < L[2] - 0.2:
            title(g, t, L[1], "ตัวแทนวัยรุ่นยุค Gen X", INK, 88)
        else:
            title(g, t, L[2], "ราชินีสายดาร์กแห่งยุค 90s", PURPLE, 84)
        return
    if t < L[4] - 0.2:   # มาสเตอร์พีซ
        for i, (txt, col) in enumerate((("Edward Scissorhands", hexc("#3a3f6a")), ("Heathers", RED),
                                        ("Dracula", hexc("#6a1f2a")))):
            k = ap(t, L[3] + 0.8 * i, 0.3)
            if k > 0.02:
                film_strip(g, 300 + (i % 2) * 440 if i < 2 else CX, 700 + (i // 2) * 330 + 15 * math.sin(t * 2 + i),
                           0.85 * k, -5 + 5 * i, txt, col, t)
        title(g, t, L[3], "ผลงานระดับมาสเตอร์พีซ", GOLDTXT, 86)
        return
    if t < L[6] - 0.2:   # เข้าชิงออสการ์ 2 ครั้ง
        wn(g, 280, WINONA, 0.82, "smile", "down", 0.3)
        for i in range(2):
            golden_statue(g, 640 + i * 200, GROUND, 0.7 * ap(t, L[4] + 0.4 * i, 0.3) + 0.01, 0, 0.5, t)
        g.label("เข้าชิง ×2", 740, 640, 70, color=GOLDTXT, sc=ap(t, L[4] + 1.0))
        if t < L[5] - 0.2:
            title(g, t, L[4], "เข้าชิงออสการ์ 2 ครั้ง!", GOLDTXT, 90)
        else:
            title(g, t, L[5], "นักแสดงพรสวรรค์สูงสุดแห่งยุค", INK, 82)
        return
    spotlight(g, 360, GROUND, t, 1.0)   # จอห์นนี เดปป์ / สปอตไลต์
    spotlight(g, 720, GROUND, t + 1.5, 1.0)
    wn(g, 380, WINONA, 0.8, "smile", "down", 0.3)
    person(g, 700, GROUND, DEPP, 0.84, mood="smile", pose="down", turn=-0.3, seed=30)
    heart(g, 540, 600 + 15 * math.sin(t * 3), 60 * ap(t, L[6] + 0.4) + 1)
    if t < L[7] - 0.2:
        title(g, t, L[6], "ความรักกับ จอห์นนี เดปป์", RED, 86)
    else:
        title(g, t, L[7], "สปอตไลต์ทุกดวงจับจ้อง", GOLDTXT, 86)


# ------------------------------------------------------------------ 4. fall
def s_fall(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # 2001 ถูกจับข้อหาขโมย
        if t < L[1] - 0.2:
            with g.at(CX, 860, ap(t, L[0]), -4):
                g.rrect(-200, -100, 400, 200, 30, WHITE, 8, stroke=RED)
                g.text("2001", 0, 0, 110, "kanit", RED)
            title(g, t, L[0], "ชีวิตพลิกคว่ำในปี 2001", RED, 88)
        else:
            shopping_bag(g, 320, GROUND - 40, 1.0, -6)
            cuffs(g, 720, 860, 1.2 * ap(t, L[1] + 0.6) + 0.01, 10 * math.sin(t * 2))
            title(g, t, L[1], "ถูกจับข้อหาขโมยเสื้อผ้า", RED, 86)
        return
    if t < L[3] - 0.2:   # แท็บลอยด์กระหน่ำ
        tabloid(g, 320, 860, 0.85, -6 + 2 * math.sin(t * 2))
        paps(g, t, 600, 3, 0.58)
        title(g, t, L[2], "แท็บลอยด์กระหน่ำตีข่าว", RED, 86)
        return
    if t < L[4] - 0.2:   # วงการหันหลัง
        wn(g, 280, WINONA, 0.82, "sad", "down", 0.3)
        for i in range(3):
            person(g, 600 + i * 150, GROUND, PAPS[i], 0.62, mood="neutral", pose="cross", turn=0.9, seed=50 + i)
        title(g, t, L[3], "วงการพร้อมใจหันหลังให้", INK, 86)
        return
    x = lerp(CX, 260, e_io(seg(t, L[4], L[4] + 2.5)))   # เฟดตัว รักษาใจ
    a = lerp(1.0, 0.45, e_io(seg(t, L[4], L[5] + 2)))
    with g.alpha(a):
        wn(g, x, WINONA, 0.82, "sad", "down", 0.6)
    candle(g, 760, GROUND - 40, 1.4, t)
    tear_drops(g, x, 560, t)
    if t < L[5] - 0.2:
        title(g, t, L[4], "เฟดตัวเพื่อรักษาบาดแผลในใจ", NAVY, 84)
    else:
        title(g, t, L[5], "ภาวะซึมเศร้าและความกดดันสะสม", GREY, 80)


# ------------------------------------------------------------------ 5. comeback
def s_comeback(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:   # ไม่ให้อดีตนิยามชีวิต
        phoenix_rise(g, CX, GROUND - 60, 1.1, t, e_out(seg(t, L[0], L[0] + 2.5)))
        title(g, t, L[0], "ไม่ให้อดีตนิยามทั้งชีวิต...", PURPLE, 84)
        return
    if t < L[3] - 0.2:   # 2016 Stranger Things / Joyce
        tv_series(g, CX, 820, 1.0 * ap(t, L[1]) + 0.01, t, "STRANGER THINGS")
        if t > L[2] - 0.2:
            wn(g, 220, JOYCE, 0.78, "firm", "wave", 0.4)
            title(g, t, L[2], "บท จอยซ์ ไบเออร์ส", ST_RED, 92)
        else:
            g.label("2016", CX, 1110, 70, color=ST_RED, sc=ap(t, L[1] + 0.4))
            title(g, t, L[1], "คัมแบ็กครั้งยิ่งใหญ่ปี 2016!", ST_RED, 84)
        return
    if t < L[4] - 0.2:   # ทุบกำแพงตามหาลูก
        bulbs_wall(g, 640, GROUND - 60, 640, t, "")
        broken_wall(g, 640, 980, e_out(seg(t, L[3] + 1.0, L[3] + 1.6)))
        wn(g, 230, JOYCE, 0.8, "shout", "fist", 0.4)
        axe(g, 330, 880, 0.9, -30 + 40 * math.sin(t * 4))
        title(g, t, L[3], "ทุบกำแพงบ้านเพื่อตามหาลูก!", ST_RED, 84)
        return
    if t < L[6] - 0.2:   # ระเบิดอารมณ์ / ซีรีส์ฮิตทั่วโลก
        bulbs_wall(g, CX, GROUND - 60, 820, t, "")
        wn(g, CX, JOYCE, 0.82, "shout" if t < L[5] - 0.2 else "smile", "fist" if t < L[5] - 0.2 else "wave", 0.0,
           talk=True)
        if t < L[5] - 0.2:
            title(g, t, L[4], "การแสดงที่ระเบิดอารมณ์และจริงใจ", ST_RED, 78)
        else:
            title(g, t, L[5], "ซีรีส์ฮิตถล่มทลายทั่วโลก!", GOLDTXT, 84)
        return
    spotlight(g, CX, GROUND, t, 1.0)   # ฝีมือระดับตำนานเปล่งประกาย
    wn(g, CX, WINONA, 0.86, "smile", "wave", 0.0)
    for i in range(6):
        g.sparkle(CX + 330 * math.cos(i * 1.05 + t), 820 + 260 * math.sin(i * 1.05 + t), 26)
    if t < L[7] - 0.2:
        title(g, t, L[6], "พิสูจน์ให้ทุกคนเห็นว่า...", INK, 88)
    else:
        title(g, t, L[7], "ฝีมือระดับตำนานไม่มีวันเสื่อม!", GOLDTXT, 82)


# ------------------------------------------------------------------ 6. lesson
def s_lesson(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # ล้มต่อหน้าคนทั้งโลก
        wn(g, CX, WINONA, 0.84, "sad" if t > L[1] - 0.2 else "smile", "down", 0.0)
        if t > L[1] - 0.2:
            paps(g, t, 760, 1, 0.6)
            camera_flash(g, 220, 700, 0.6, t, 2)
            title(g, t, L[1], "แม้จะล้มต่อหน้าคนทั้งโลก", INK, 84)
        else:
            title(g, t, L[0], "เรื่องราวนี้พิสูจน์ว่า...", INK, 88)
        return
    if t < L[3] - 0.2:   # ไม่ยอมแพ้ ลุกขึ้นใหม่
        phoenix_rise(g, CX, GROUND - 60, 1.15, t, 0.3 + 0.7 * e_out(seg(t, L[2] - 0.2, L[3])))
        title(g, t, L[2], "ไม่ยอมแพ้ กล้าลุกขึ้นใหม่", PURPLE, 86)
        return
    with g.at(CX, 860, ap(t, L[3]), -3 + 2 * math.sin(t * 2)):   # เขียนบทชีวิตบทใหม่
        g.rrect(-240, -300, 480, 600, 10, hexc("#f4eedf"), 6)
        g.text("บทใหม่", 0, -220, 56, "kanit", PURPLE)
        for i in range(int(7 * e_io(seg(t, L[3], L[3] + 2.5)))):
            g.line([(-180, -130 + i * 55), (180 - (i % 3) * 50, -130 + i * 55)], 5, NAVY, amp=0)
    title(g, t, L[3], "เขียนบทชีวิตใหม่ที่สง่างามกว่าเดิม", PURPLE, 76)


# ------------------------------------------------------------------ 7. outro
def s_outro(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:
        wn(g, CX, WINONA, 0.84, "smile", "wave", 0.0, talk=True)
        title(g, t, L[0], "ชอบบทบาทไหนที่สุด?", INK, 90)
        return
    if t < L[3] - 0.2:
        items = (("Beetlejuice", hexc("#3a8a4a")), ("Edward Scissorhands", hexc("#3a3f6a")),
                 ("Stranger Things", ST_RED))
        for i, (txt, col) in enumerate(items):
            k = ap(t, L[1] + 1.2 * i, 0.3) if i < 2 else ap(t, L[2])
            if k > 0.02:
                film_strip(g, 300 + (i % 2) * 460 if i < 2 else CX, 760 + (i // 2) * 320 + 20 * math.sin(t * 2 + i),
                           0.85 * k, -5 + 5 * i, txt, col, t)
        title(g, t, L[1], "บทบาทในความทรงจำ", PURPLE, 88)
        return
    with g.at(CX + 170, 640, ap(t, L[3])):   # ชวนคอมเมนต์
        g.bubble(0, 0, 460, 220, WHITE, tail=(-1, 1))
        for i in range(3):
            g.circle(-110 + i * 110, 0, 24 + 6 * math.sin(t * 6 - i), INK, 0)
    wn(g, 260, WINONA, 0.8, "smile", "wave", 0.3, talk=True)
    title(g, t, L[3], "มาแลกเปลี่ยนกันในคอมเมนต์!", RED, 70)


SCENES = {
    "hook": s_hook, "young": s_young, "fame": s_fame, "fall": s_fall, "comeback": s_comeback,
    "lesson": s_lesson, "outro": s_outro,
}
NO_IRIS = set()
