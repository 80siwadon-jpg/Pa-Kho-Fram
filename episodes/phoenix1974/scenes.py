"""ฉากตอน: วันเกิดวาคีน ฟินิกซ์ (28 ต.ค. 1974)"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from chars import (JOAQUIN, JOAQUIN_KID, JOAQUIN_TEEN, JOAQUIN_THIN, JOKER_RED, PRESS, RIVER, RIVER_KID,  # noqa: E402
                   SIBS, candle, clapper, club_front, crowd, film_strip, globe, golden_statue, guitar, hat, heart,
                   laughing_tears, leaf, microphone, paw, payphone, phoenix_bird, poem, scale_weigh, siren,
                   spotlight, stairs, streetlight, tear_drops)
from gfx import GOLD, GOLD2, GREY, INK, NAVY, RED, W, WHITE, e_io, e_out, hexc, lerp, pop, seg  # noqa: E402
from people import person  # noqa: E402

CX = W / 2
GROUND = 1270
GOLDTXT = hexc("#b37a12")
GREEN = hexc("#3c8d4f")
NIGHT = hexc("#1c2236")
PURPLE = hexc("#6a4a8a")
FIRE = hexc("#d9502a")

CAMERA = {"hook": "push_in", "young": "pan_right", "river": "dutch", "joker": "push_in", "speech": "pull_out",
          "lesson": "pan_left", "outro": "pan_right"}
TRANSITIONS = {"young": "zoom", "river": "fade", "joker": "iris", "speech": "zoom", "lesson": "fade",
               "outro": "whip"}


def ap(t, a, dur=0.38):
    return pop(t, a - 0.2, dur)


def title(g, t, a, txt, col=INK, size=84, y=380):
    g.label(txt, CX, y, size, color=col, sc=ap(t, a), rot=-3)


def jq(g, x, look=JOAQUIN, sc=0.82, mood="smile", pose="down", turn=0.3, talk=False, seed=3):
    person(g, x, GROUND, look, sc, mood=mood, pose=pose, turn=turn, seed=seed, talk=talk)


def night(g, k=1.0):
    """ฟ้ากลางคืน: แผงกรมท่าไล่จางลงสู่พื้น (บนพื้นขาว)"""
    import cairo
    if k <= 0:
        return
    c = g.c
    gr = cairo.LinearGradient(0, 140, 0, GROUND)
    gr.add_color_stop_rgba(0, *NIGHT[:3], 0.85 * k)
    gr.add_color_stop_rgba(1, *NIGHT[:3], 0.35 * k)
    c.rectangle(-500, 140, 2100, GROUND - 140)
    c.set_source(gr)
    c.fill()


LIGHT = hexc("#f2c94c")


# ------------------------------------------------------------------ 1. hook
def s_hook(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[3] - 0.2:   # โทรศัพท์ฉุกเฉินกลางดึก (ไม่แสดงร่างพี่ชาย: ไซเรน + โทรศัพท์)
        night(g, 1.0)
        g.circle(820, 520, 60, hexc("#f6e7a8"), 6)
        g.circle(850, 500, 52, NIGHT, 0)
        streetlight(g, 220, GROUND, 1.0)
        payphone(g, 420, GROUND, 0.9, t, 1.0)
        if t > L[2] - 0.2:
            person(g, 640, GROUND, JOAQUIN_TEEN, 0.74, mood="shock", pose="phone", turn=-0.3, seed=4, talk=True)
            tear_drops(g, 640, 600, t)
            siren(g, 820, 1050, 0.8, t, 1.0)
            title(g, t, L[2], "เสียงกรีดร้องขอความช่วยเหลือ...", LIGHT, 76)
        else:
            sound_k = ap(t, L[1] + 0.3)
            for i in range(3):
                u = (t * 1.6 + i / 3) % 1
                g.arc(300, 600, 60 + 120 * u, -50, 50, 6, (1, 1, 1, (1 - u) * sound_k))
            title(g, t, L[1], "โทรศัพท์ฉุกเฉินกลางดึก", LIGHT, 84)
        return
    if t < L[5] - 0.2:   # แบกความสูญเสีย → กลายเป็นตัวตลกที่สะกดคนทั้งโลก
        if t < L[4] - 0.2:
            candle(g, 760, GROUND - 60, 1.4, t)
            jq(g, 320, JOAQUIN_TEEN, 0.8, "sad", "down", 0.3)
            title(g, t, L[3], "แบกความสูญเสียและรอยแผลใจ", NAVY, 80)
        else:
            stairs(g, 640, GROUND, 1.0)
            spotlight(g, 360, GROUND, t, 1.0)
            jq(g, 360, JOAQUIN_THIN, 0.8, "smile", "v", 0.2)
            g.label("\"โจ๊กเกอร์\"", 700, 640, 90, color=JOKER_RED, sc=ap(t, L[4] + 0.8), rot=-6)
            title(g, t, L[4], "สะกดคนทั้งโลก!", JOKER_RED, 92)
        return
    golden_statue(g, 760, GROUND - 40, 1.1 * ap(t, L[5]) + 0.01, 0, 1.0, t)   # คว้าออสการ์
    jq(g, 300, JOAQUIN, 0.8, "smile", "wave", 0.3)
    g.name_tag(t, L[5] - 0.1, 330, 1080, "วาคีน ฟินิกซ์", "นักแสดงรางวัลออสการ์", dur=2.6, side=1)
    title(g, t, L[5], "คว้าออสการ์อย่างยิ่งใหญ่!", GOLDTXT, 88)


# ------------------------------------------------------------------ 2. young
def s_young(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # 28 ต.ค. 1974
        if t < L[1] - 0.2:
            g.calendar(CX, 860, 1.25 * ap(t, L[0]) + 0.01, 28, "จันทร์", "ต.ค. 1974")
            title(g, t, L[0], "28 ตุลาคม 1974", PURPLE, 92)
        else:
            jq(g, CX, JOAQUIN_KID, 0.9, "smile", "wave", 0.0)
            title(g, t, L[1], "เด็กชาย วาคีน ฟินิกซ์", INK, 88)
        return
    if t < L[4] - 0.2:   # วัยเด็กแปลกแยก เร่ร่อนอเมริกาใต้
        x = lerp(220, 520, e_io(seg(t, L[2], L[4])))
        for i, lk in enumerate((RIVER_KID, JOAQUIN_KID, SIBS[0])):
            person(g, x + i * 150, GROUND, lk, 0.8, mood="worry" if t > L[3] - 0.2 else "neutral", pose="down",
                   turn=0.6, seed=10 + i)
        if t < L[3] - 0.2:
            title(g, t, L[2], "วัยเด็กแปลกแยกและผาดโผน", INK, 84)
        else:
            with g.at(830, 640, ap(t, L[3] + 0.6), 6):
                g.rrect(-130, -70, 260, 140, 20, WHITE, 7, stroke=GREEN)
                g.label("อเมริกาใต้", 0, 0, 48, color=GREEN)
            title(g, t, L[3], "เร่ร่อนไปตามประเทศต่าง ๆ", NAVY, 82)
        return
    if t < L[6] - 0.2:   # เปลี่ยนนามสกุลเป็นฟินิกซ์ = เกิดใหม่จากเถ้าถ่าน
        phoenix_bird(g, CX, GROUND - 60, 1.1, t, e_out(seg(t, L[4] + 0.4, L[5] + 0.6)))
        if t < L[5] - 0.2:
            g.label("PHOENIX", CX, 560, 90, color=FIRE, sc=ap(t, L[4] + 0.6))
            title(g, t, L[4], "เปลี่ยนนามสกุลเป็น \"ฟินิกซ์\"", FIRE, 84)
        else:
            title(g, t, L[5], "เกิดใหม่จากเถ้าถ่าน", FIRE, 92)
        return
    for i, lk in enumerate((RIVER_KID, JOAQUIN_KID, SIBS[0], SIBS[1])):   # ร้องเพลงเปิดหมวกข้างถนน
        person(g, 180 + i * 170, GROUND, lk, 0.8, mood="smile", pose="wave" if i % 2 else "hold",
               turn=0.2 - 0.15 * i, seed=20 + i, talk=i == 0)
    guitar(g, 200, GROUND - 260, 0.55, -20)
    hat(g, 840, GROUND - 10, 0.8, t, int(seg(t, L[6], L[7] + 0.8) * 5))
    sound_waves(g, 260, 700, t)
    title(g, t, L[6] if t < L[7] - 0.2 else L[7], "ร้องเพลงเปิดหมวกข้างถนน" if t < L[7] - 0.2 else
          "เพื่อหาเงินประทังชีวิต", GOLDTXT, 84)


def sound_waves(g, x, y, t, n=3):
    for i in range(n):
        u = (t * 1.2 + i / n) % 1
        nx, ny, a = x + 120 * u + 40 * i, y - 200 * u, 1 - u
        g.circle(nx, ny, 14, (*INK[:3], a), 0)
        g.line([(nx + 12, ny), (nx + 12, ny - 50), (nx + 34, ny - 40)], 5, (*INK[:3], a), amp=0)


# ------------------------------------------------------------------ 3. river
def s_river(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # โศกนาฏกรรม คืนฮาโลวีน 1993
        night(g, 0.9)
        g.circle(780, 560, 70, hexc("#f6e7a8"), 6)
        for i in range(3):   # ฟักทองฮาโลวีน
            x = 220 + i * 260
            g.blob(x, GROUND - 60, 70, 55, hexc("#e8843a"), 6, seed=i)
            g.line([(x, GROUND - 115), (x + 10, GROUND - 145)], 8, GREEN, amp=0)
            g.poly([(x - 30, GROUND - 80), (x - 15, GROUND - 100), (x, GROUND - 80)], (1, 0.85, 0.3, 1), 0, amp=0)
            g.poly([(x + 10, GROUND - 80), (x + 25, GROUND - 100), (x + 40, GROUND - 80)], (1, 0.85, 0.3, 1), 0,
                   amp=0)
        if t < L[1] - 0.2:
            title(g, t, L[0], "โศกนาฏกรรมที่บีบหัวใจ", LIGHT, 88)
        else:
            g.label("31 ต.ค. 1993", CX, 700, 90, color=LIGHT, sc=ap(t, L[1] + 0.3))
            title(g, t, L[1], "คืนวันฮาโลวีน ปี 1993", LIGHT, 88)
        return
    if t < L[4] - 0.2:   # ริเวอร์ ฟินิกซ์ ดาราดาวรุ่ง ไอดอลของวาคีน
        spotlight(g, 320, GROUND, t, 1.0)
        person(g, 320, GROUND, RIVER, 0.84, mood="smile", pose="wave", turn=0.3, seed=30)
        person(g, 760, GROUND, JOAQUIN_TEEN, 0.74, mood="smile", pose="down", turn=-0.4, seed=4)
        g.name_tag(t, L[2], 330, 1080, "ริเวอร์ ฟินิกซ์", "พี่ชาย ดาราดาวรุ่ง", side=1)
        for i in range(4):
            g.star(320 + 230 * math.cos(i * 1.6 + t), 560 + 80 * math.sin(i * 1.6 + t), 22, GOLD2, 4)
        if t > L[3] - 0.2:
            heart(g, 700, 600, 40 * ap(t, L[3] + 0.6) + 1)
            title(g, t, L[3], "ดาวรุ่งอันดับหนึ่ง & ไอดอลของวาคีน", GOLDTXT, 72)
        else:
            title(g, t, L[2], "ริเวอร์ ฟินิกซ์ พี่ชายแท้ ๆ", INK, 86)
        return
    if t < L[5] - 0.2:   # ล้มลงหน้าไนท์คลับ (ไม่แสดงร่าง: ไซเรนหน้าคลับ)
        night(g, 0.9)
        club_front(g, CX, GROUND, 0.95, t)
        siren(g, CX, GROUND - 600, 0.7, t, 1.0)
        title(g, t, L[4], "ล้มลงหน้าร้านไนท์คลับ", LIGHT, 86)
        return
    if t < L[7] - 0.2:   # วาคีน 19 ปี โทร 911
        night(g, 0.9)
        payphone(g, 300, GROUND, 0.9, t, 1.0)
        person(g, 560, GROUND, JOAQUIN_TEEN, 0.78, mood="shock", pose="phone", turn=-0.3, seed=4, talk=True)
        tear_drops(g, 560, 580, t)
        siren(g, 830, 1060, 0.7, t, 1.0)
        if t < L[6] - 0.2:
            g.label("911", 300, 560, 100, color=RED, sc=ap(t, L[5] + 0.4))
            title(g, t, L[5], "วาคีนวัย 19 โทรแจ้ง 911", LIGHT, 84)
        else:
            title(g, t, L[6], "เสียงสั่นเครือ กรีดร้องหมดหนทาง", LIGHT, 76)
        return
    if t < L[8] - 0.2:   # ยื้อชีวิตไม่ได้
        candle(g, CX, GROUND - 60, 1.6, t)
        title(g, t, L[7], "ไม่อาจยื้อชีวิตพี่ชายไว้ได้", GREY, 84)
        return
    if t < L[9] - 0.2:   # สื่อเปิดเสียง 911 ซ้ำ ๆ
        for i, lk in enumerate(PRESS):
            person(g, 230 + i * 220, GROUND, lk, 0.66, mood="neutral", pose="hold", turn=0.4, seed=40 + i)
        with g.at(780, 820, 1, 4 * math.sin(t * 3)):
            g.rrect(-150, -110, 300, 220, 20, hexc("#3a3f48"), 6)
            g.text("911", 0, -30, 70, "kanit", RED)
            g.text("▶ ▶ ▶", 0, 50, 40, "kanit", WHITE)
        title(g, t, L[8], "สื่อนำเสียง 911 ไปเปิดซ้ำ ๆ", RED, 82)
        return
    jq(g, lerp(560, 220, e_io(seg(t, L[9], L[9] + 2.2))), JOAQUIN_TEEN, 0.76, "sad", "down", 0.6)   # หนีออกจากวงการ
    clapper(g, 800, 960, 0.8, 0.0, t)
    title(g, t, L[9], "หนีออกจากวงการไปนานนับปี", NAVY, 84)


# ------------------------------------------------------------------ 4. joker
def s_joker(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[3] - 0.2:   # กลับมา เปลี่ยนความเจ็บปวดเป็นเชื้อเพลิง
        if t < L[1] - 0.2:
            clapper(g, 760, 920, 0.9, e_io(seg(t, L[0] + 0.4, L[0] + 1.2)), t)
            jq(g, 300, JOAQUIN_TEEN, 0.8, "firm", "down", 0.3)
            title(g, t, L[0], "เมื่อเขากลับมาสู่วงการแสดง", INK, 84)
        else:
            phoenix_bird(g, CX, GROUND - 60, 1.15, t, 0.3 + 0.7 * e_out(seg(t, L[1] - 0.3, L[2])))
            if t < L[2] - 0.2:
                title(g, t, L[1], "เปลี่ยนความเจ็บปวด...", NAVY, 92)
            else:
                title(g, t, L[2], "เป็นเชื้อเพลิงแห่งการแสดง!", FIRE, 86)
        return
    if t < L[5] - 0.2:   # ไม่ใช่แค่ท่องบท / Method Actor
        if t < L[4] - 0.2:
            jq(g, 300, JOAQUIN, 0.82, "neutral", "hold", 0.3)
            with g.at(560, GROUND - 420, 1, -10):
                g.rrect(-90, -120, 180, 240, 8, hexc("#f4eedf"), 5)
            k = seg(t, L[3] + 0.6, L[3] + 1.2)
            if k > 0:
                g.line([(450, 680), (450 + 220 * k, 680 + 260 * k)], 14, RED, amp=0)
            title(g, t, L[3], "ไม่ใช่แค่ท่องบท", INK, 92)
        else:
            laughing_tears(g, CX, 820, 1.4 * ap(t, L[4]) + 0.01, t)
            g.label("Method Actor", CX, 1120, 76, color=PURPLE, sc=ap(t, L[4] + 0.4))
            title(g, t, L[4], "ดำดิ่งกลืนกินจิตวิญญาณตัวละคร", PURPLE, 76)
        return
    if t < L[7] - 0.2:   # ลดน้ำหนัก 23 กก. เพื่อ Joker
        u = e_io(seg(t, L[5], L[5] + 2.5))
        look = JOAQUIN if u < 0.5 else JOAQUIN_THIN
        jq(g, 320, look, 0.82, "firm", "down", 0.3)
        scale_weigh(g, 320, GROUND + 4, 0.8, 23 * u)
        g.label(f"-{int(23 * u)} กก.", 760, 720, 110, color=RED, sc=ap(t, L[5] + 0.3), rot=-5)
        if t > L[6] - 0.2:
            film_strip(g, 760, 1020, 0.9, 4, "JOKER", JOKER_RED, t)
        title(g, t, L[5] if t < L[6] - 0.2 else L[6], "ลดน้ำหนักกว่า 23 กิโลกรัม!" if t < L[6] - 0.2 else
              "เพื่อบทในภาพยนตร์ Joker", JOKER_RED, 82)
        return
    if t < L[9] - 0.2:   # หัวเราะทั้งน้ำตา สะกดคนดู
        stairs(g, 640, GROUND, 1.0)
        spotlight(g, 380, GROUND, t, 1.0)
        bob = 10 * math.sin(t * 4)
        with g.at(0, bob):
            jq(g, 380, JOAQUIN_THIN, 0.8, "smile", "v" if math.sin(t * 2) > 0 else "wave", 0.2)
        tear_drops(g, 380, 560, t)
        if t < L[8] - 0.2:
            title(g, t, L[7], "หัวเราะทั้งน้ำตา แววตาแตกสลาย", JOKER_RED, 76)
        else:
            title(g, t, L[8], "สะกดคนดูจนอยู่หมัด!", JOKER_RED, 90)
        return
    jq(g, 300, JOAQUIN, 0.8, "smile", "hold", 0.3)   # กวาดรางวัล + ออสการ์
    n = 3 if t < L[10] - 0.2 else 4
    for i in range(n):
        golden_statue(g, 600 + (i % 2) * 180 + (i // 2) * 90, GROUND - (i // 2) * 0, 0.6 * ap(t, L[9] + 0.3 * i, 0.3)
                      + 0.01, 0, 1.0 if i == 3 else 0.0, t)
    if t < L[10] - 0.2:
        title(g, t, L[9], "กวาดรางวัลนักแสดงนำชายยอดเยี่ยม", GOLDTXT, 76)
    else:
        title(g, t, L[10], "รวมถึงรางวัลออสการ์!", GOLDTXT, 92)


# ------------------------------------------------------------------ 5. speech
def s_speech(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # ค่ำคืนรับออสการ์ ไม่หลงแสงสี
        spotlight(g, 360, GROUND, t, 1.0)
        jq(g, 360, JOAQUIN, 0.82, "neutral" if t > L[1] - 0.2 else "smile", "hold", 0.2)
        golden_statue(g, 470, GROUND - 400, 0.5, -10)
        crowd(g, 760, GROUND + 20, 300, t, 4)
        if t < L[1] - 0.2:
            title(g, t, L[0], "ค่ำคืนรับรางวัลออสการ์", GOLDTXT, 86)
        else:
            title(g, t, L[1], "ชายผู้ไม่เคยหลงแสงสี", INK, 88)
        return
    if t < L[3] - 0.2:   # มนุษย์ สิ่งแวดล้อม สัตว์
        jq(g, 260, JOAQUIN, 0.8, "firm", "point", 0.3, talk=True)
        microphone(g, 470, GROUND - 260, 0.7)
        for i, (fn, txt, col) in enumerate(((lambda x, y, k: heart(g, x, y, 50 * k + 0.1), "เพื่อนมนุษย์", RED),
                                            (lambda x, y, k: globe(g, x, y, 60 * k + 1, t), "สิ่งแวดล้อม", GREEN),
                                            (lambda x, y, k: paw(g, x, y, 60 * k + 1), "สัตว์โลก", hexc("#7a5a3a")))):
            k = ap(t, L[2] + 0.6 * i, 0.3) * (1 + 0.08 * math.sin(t * 4 + i))
            y = 620 + i * 210
            fn(780, y, k)
            g.label(txt, 780, y + 90, 44, color=col, sc=k)
        title(g, t, L[2], "พูดเพื่อโลกและสิ่งมีชีวิต", GREEN, 82)
        return
    if t < L[5] - 0.2:   # อ่านบทกวีของริเวอร์ทั้งน้ำตา
        poem(g, 720, 880 - 15 * math.sin(t * 2), 0.95, 4 + 4 * math.sin(t * 1.5), e_io(seg(t, L[2] + 2, L[4] + 2)))
        jq(g, 280, JOAQUIN, 0.8, "sad", "hold", 0.4, talk=True)
        tear_drops(g, 280, 560, t)
        if t < L[4] - 0.2:
            title(g, t, L[3], "ปิดท้ายด้วยบทกวี...", NAVY, 90)
        else:
            title(g, t, L[4], "ที่ริเวอร์เขียนไว้ตอนอายุ 17", NAVY, 82)
        return
    for i in range(5):   # "จงวิ่งไปหาความรัก... สันติภาพจะตามมา"
        u = (t * 0.5 + i / 5) % 1
        heart(g, 200 + i * 170, 1100 - 500 * u, 30, RED, 1 - u)
    for i in range(3):
        leaf(g, 260 + i * 280, 640 + 20 * math.sin(t * 2 + i), 0.8, -20 + 20 * i)
    title(g, t, L[5], "\"วิ่งไปหาความรัก แล้วสันติภาพจะตามมา\"", PURPLE, 70)


# ------------------------------------------------------------------ 6. lesson
def s_lesson(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:
        jq(g, CX, JOAQUIN, 0.86, "smile", "down", 0.0)
        title(g, t, L[0], "เรื่องราวนี้พิสูจน์ว่า...", INK, 86)
        return
    phoenix_bird(g, CX, GROUND - 60, 1.2, t, 0.25 + 0.75 * e_out(seg(t, L[1] - 0.2, L[2] + 1.0)))
    if t < L[2] - 0.2:
        title(g, t, L[1], "บาดแผลไม่ได้มีไว้ให้ยอมจำนน", NAVY, 80)
    else:
        title(g, t, L[2], "แต่เปลี่ยนเป็นพลังเพื่อก้าวต่อไป", FIRE, 80)


# ------------------------------------------------------------------ 7. outro
def s_outro(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:
        jq(g, CX, JOAQUIN, 0.84, "smile", "wave", 0.0, talk=True)
        title(g, t, L[0], "ประทับใจบทบาทไหนที่สุด?", INK, 88)
        return
    if t < L[3] - 0.2:   # Joker / Gladiator / Her
        for i, (txt, col) in enumerate((("Joker", JOKER_RED), ("Gladiator", GOLDTXT), ("Her", hexc("#d9665a")))):
            k = ap(t, L[1] + 1.2 * i, 0.3) if i < 2 else ap(t, L[2])
            if k > 0.02:
                film_strip(g, 280 + i * 260, 800 + (i % 2) * 220, 0.75 * k, -6 + 6 * i, txt, col, t)
        title(g, t, L[1], "Joker · Gladiator · Her", PURPLE, 88)
        return
    with g.at(CX + 170, 640, ap(t, L[3])):   # ชวนคอมเมนต์
        g.bubble(0, 0, 460, 220, WHITE, tail=(-1, 1))
        for i in range(3):
            g.circle(-110 + i * 110, 0, 24 + 6 * math.sin(t * 6 - i), INK, 0)
    jq(g, 260, JOAQUIN, 0.8, "smile", "wave", 0.3, talk=True)
    title(g, t, L[3], "มาแลกเปลี่ยนกันในคอมเมนต์!", RED, 70)


SCENES = {
    "hook": s_hook, "young": s_young, "river": s_river, "joker": s_joker, "speech": s_speech,
    "lesson": s_lesson, "outro": s_outro,
}
NO_IRIS = set()
