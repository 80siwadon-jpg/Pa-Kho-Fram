"""ฉากตอน: 28 ต.ค. 1962 ครุชชอฟประกาศถอนขีปนาวุธจากคิวบา — จุดจบวิกฤตการณ์ 13 วัน"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from chars import (FAMILY, GENERALS, JFK, KHRUSHCHEV, SOV, US, alarm_clock, building, calendar,  # noqa: E402
                   caribbean_map, clock_face, deal_table, defcon, dove, exhale, globe, hotline, missile, missile_ship,
                   old_mic, radio_set, red_phone, sea, time_bomb, turkey_map, warship)
from gfx import GOLD, GOLD2, GREY, INK, NAVY, RED, W, WHITE, e_io, e_out, hexc, lerp, pop, seg  # noqa: E402
from people import person  # noqa: E402
from photos import cover  # noqa: E402

CX = W / 2
GROUND = 1270
GOLDTXT = hexc("#b37a12")
GREEN = hexc("#3c8d4f")

CAMERA = {"hook": "push_in", "tension": "dutch", "radio": "pan_right", "deal": "push_in", "hotline": "pan_left",
          "lesson": "pull_out", "outro": "pan_right"}
TRANSITIONS = {"tension": "zoom", "radio": "whip", "deal": "iris", "hotline": "zoom", "lesson": "fade",
               "outro": "whip"}


def ap(t, a, dur=0.38):
    return pop(t, a - 0.2, dur)


def title(g, t, a, txt, col=INK, size=84, y=380):
    g.label(txt, CX, y, size, color=col, sc=ap(t, a), rot=-3)


def khrushchev(g, x, sc=0.8, mood="firm", pose="down", turn=-0.3, talk=False):
    person(g, x, GROUND, KHRUSHCHEV, sc, mood=mood, pose=pose, turn=turn, seed=2, talk=talk)


def jfk(g, x, sc=0.8, mood="firm", pose="down", turn=0.3, talk=False):
    person(g, x, GROUND, JFK, sc, mood=mood, pose=pose, turn=turn, seed=1, talk=talk)


def chip(g, x, y, txt, col, k, rot=0.0, w=320):
    if k < 0.02:
        return
    with g.at(x, y, k, rot):
        g.rrect(-w / 2, -64, w, 128, 40, WHITE, 7, stroke=col)
        g.label(txt, 0, 0, 52, color=col)


# ------------------------------------------------------------------ 1. hook
def _cover_art(t):
    def art(g, w, h):
        g.c.set_source_rgba(0.86, 0.92, 0.97, 1)
        g.c.paint()
        radio_set(g, 0, 170, 1.0, t, 1.0)
        dove(g, 120, -230, 1.1, t)
    return art


def s_hook(g, t, L, d):
    t_out = L[1] + 0.4
    if t < t_out + 0.3:   # หน้าปกโพลารอยด์ (เฟรมแรก)
        u = e_io(seg(t, t_out, t_out + 0.3))
        g.label("วันนี้ในอดีต", CX, 250 - 300 * u, 80, rot=-2)
        cover(g, None, "28 ตุลาคม 1962", "วันที่โลกรอดจากสงครามนิวเคลียร์", 1 - 0.4 * u, -2 - 25 * u,
              x=CX + 900 * u, y=690, w=600, h=700, fallback=_cover_art(t))
        if t < t_out:
            return
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # วิทยุมอสโก ยอมถอย
        radio_set(g, CX, 1100, 1.2, t, ap(t, L[1] + 0.5))
        g.label("ยอมถอย!", CX, 560, 110, color=SOV, sc=ap(t, L[1] + 1.4), rot=-5)
        title(g, t, L[1] + 0.4, "คลื่นวิทยุจากมอสโก", SOV, 92)
        return
    fuse = 1 - seg(t, L[2], L[2] + 1.8) * 0.6   # ปลดชนวนระเบิดเวลา
    cut = t > L[2] + 1.8
    time_bomb(g, CX, 900, 1.3, t if not cut else 0, 0.0 if cut else fuse)
    if cut:
        g.label("ปลดชนวน!", CX, 600, 100, color=GREEN, sc=ap(t, L[2] + 2.0), rot=-4)
    title(g, t, L[2], "เกือบเป็นเถ้าถ่านนิวเคลียร์!", RED, 82)


# ------------------------------------------------------------------ 2. tension
def s_tension(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # 28 ต.ค. / ข้ามคืนจากวันเสาร์ทมิฬ
        if t < L[1] - 0.2:
            calendar(g, CX, 860, 1.25 * ap(t, L[0]) + 0.01, "28", "ต.ค. 1962", "อาทิตย์", -3 + 2 * math.sin(t), RED)
            title(g, t, L[0], "28 ตุลาคม 1962", RED, 92)
        else:
            calendar(g, 330, 880, 0.9, "27", "ต.ค. 1962", "เสาร์", -6, INK)
            g.label("→", CX, 880, 110, color=GREY, sc=ap(t, L[1] + 0.4))
            calendar(g, 760, 880, 0.9 * ap(t, L[1] + 0.8) + 0.01, "28", "ต.ค. 1962", "อาทิตย์", 5, RED)
            title(g, t, L[1], "เพิ่งผ่าน \"วันเสาร์ทมิฬ\" ข้ามคืน", INK, 78)
        return
    if t < L[3] - 0.2:   # ตึงเครียดจุดเดือด
        caribbean_map(g, CX, 860, 0.85, t, missiles=1.0, ring=1.0, ships=1.0, range_k=0.7)
        time_bomb(g, 800, 1130, 0.55, t, 0.25)
        title(g, t, L[2], "วิกฤตขีปนาวุธคิวบา ถึงจุดเดือด!", RED, 78)
        return
    if t < L[4] - 0.2:   # สหรัฐฯ ยกระดับความพร้อมรบ
        defcon(g, 690, 760, 0.9, 2, t)
        person(g, 250, GROUND, GENERALS[0], 0.78, mood="angry", pose="fist", turn=0.4, seed=10, talk=True)
        title(g, t, L[3], "สหรัฐฯ เตรียมบุกคิวบา", US, 86)
        return
    if t < L[5] - 0.2:   # โซเวียตพร้อมสวนกลับ
        missile(g, CX, 1000, 1.4, 4 * math.sin(t * 2))
        g.label("พร้อมยิง!", CX, 640, 90, color=SOV, sc=ap(t, L[4] + 0.4), rot=4)
        title(g, t, L[4], "โซเวียตพร้อมเหนี่ยวไกสวนกลับ", SOV, 80)
        return
    if t < L[6] - 0.2:   # ผู้คนตื่นมาด้วยความกลัว
        for i, lk in enumerate(FAMILY):
            person(g, 230 + i * 250, GROUND, lk, 0.68, mood="worry", pose="down", turn=0.2 - 0.2 * i, seed=20 + i)
        alarm_clock(g, 840, 700, 0.7, t, 1.0)
        title(g, t, L[5], "ผู้คนนับร้อยล้านตื่นมาด้วยความกลัว", INK, 74)
        return
    clock_face(g, CX, 860, 260, lerp(5, 0.5, e_io(seg(t, L[6], L[6] + 1.6))))   # วันสุดท้ายของโลก?
    title(g, t, L[6], "วันสุดท้ายของโลก?", RED, 96)


# ------------------------------------------------------------------ 3. radio
def s_radio(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # เช้าวันนั้น วิทยุมอสโกตัดเข้าแถลงการณ์ด่วน
        sun_y = lerp(1000, 640, e_out(seg(t, L[0] - 0.2, L[1])))
        g.sunburst(CX, sun_y, 130, 260, 16, t * 6, 10, (1, 0.85, 0.4, 0.6))
        g.circle(CX, sun_y, 110, GOLD2, 6)
        if t < L[1] - 0.2:
            title(g, t, L[0], "เช้าวันนั้น...", GOLDTXT, 100)
        else:
            radio_set(g, CX, GROUND, 1.2, t, 1.0)
            with g.at(800, 700, ap(t, L[1] + 0.3), 8 + 4 * math.sin(t * 8)):
                g.rrect(-130, -60, 260, 120, 20, RED, 6)
                g.text("ด่วน!", 0, 0, 64, "kanit", WHITE)
            title(g, t, L[1], "วิทยุมอสโก แถลงการณ์ด่วน!", SOV, 82)
        return
    if t < L[4] - 0.2:   # ครุชชอฟประกาศ
        khrushchev(g, 330, 0.84, "firm", "down" if t < L[3] - 0.2 else "stop", 0.3, talk=True)
        old_mic(g, 580, GROUND - 330, 0.9)
        g.name_tag(t, L[2] + 0.1, 330, 1080, "นิกิตา ครุชชอฟ", "ผู้นำสูงสุดสหภาพโซเวียต", side=1)
        if t > L[3] - 0.2:
            globe(g, 790, 680, 120, t)
            for i in range(3):
                u = (t * 1.2 + i / 3) % 1
                g.arc(790, 680, 140 + 100 * u, 0, 360, 5, (*SOV[:3], 1 - u))
            title(g, t, L[3], "ประกาศต่อหน้าคนทั้งโลก", SOV, 84)
        else:
            title(g, t, L[2], "นิกิตา ครุชชอฟ", SOV, 96)
        return
    if t < L[6] - 0.2:   # หยุดสร้าง / รื้อถอนฐานยิงทั้งหมด
        if t < L[5] - 0.2:
            missile(g, CX, 1000, 1.3, 0)
            with g.at(CX + 200, 700, ap(t, L[4] + 0.3), -8):
                g.circle(0, 0, 120, RED, 8)
                g.text("STOP", 0, 0, 64, "kanit", WHITE)
            title(g, t, L[4], "หยุดงานก่อสร้าง!", RED, 96)
        else:
            caribbean_map(g, CX, 860, 0.85, t, missiles=1 - seg(t, L[5] + 0.3, L[5] + 2.2))
            title(g, t, L[5], "รื้อถอนฐานยิงทั้งหมด!", GREEN, 88)
        return
    sea(g, 1000, t, GROUND)   # บรรทุกกลับบ้าน
    missile_ship(g, lerp(560, 280, seg(t, L[6] - 0.2, L[6] + 2.5)), 1050, 0.95, t, True)
    g.label("← กลับบ้าน", 760, 760, 80, color=SOV, sc=ap(t, L[6] + 0.3), rot=-4)
    title(g, t, L[6], "บรรทุกกลับบ้าน!", SOV, 96)


# ------------------------------------------------------------------ 4. deal
def s_deal(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # ลมหายใจโล่งอกหลัง 13 วัน
        relief = t > L[1] - 0.2
        for i, lk in enumerate(FAMILY):
            person(g, 230 + i * 250, GROUND, lk, 0.68, mood="smile" if relief else "worry",
                   pose="v" if relief and i != 1 else "down", turn=0.2 - 0.2 * i, seed=20 + i)
            exhale(g, 260 + i * 250, 640 + (i == 2) * 260, t, 1.0 if relief else 0.0)
        if not relief:
            with g.at(820, 640, ap(t, L[0] + 0.3), 6):
                g.circle(0, 0, 100, WHITE, 7)
                g.text("13", 0, -10, 80, "kanit", RED)
                g.text("วัน", 0, 50, 36, "kanitsb", INK)
            title(g, t, L[0], "กลั้นหายใจมา 13 วันเต็ม", INK, 82)
        else:
            title(g, t, L[1], "โล่งอกอย่างที่สุด!", GREEN, 96)
        return
    if t < L[4] - 0.2:   # ไม่ใช่การยอมแพ้ไร้เงื่อนไข
        khrushchev(g, 330, 0.82, "smug", "cross", 0.3)
        if t > L[3] - 0.2:
            with g.at(760, 820, ap(t, L[3])):
                g.line([(0, 200), (0, -160)], 8, hexc("#8a6a42"), amp=0)
                g.rrect(0, -160, 200, 130, 6, WHITE, 6)
            k = seg(t, L[3] + 0.6, L[3] + 1.2)
            if k > 0:
                g.line([(640, 600), (640 + 300 * k, 600 + 400 * k)], 16, RED, amp=0)
            title(g, t, L[3], "ไม่ใช่การยอมแพ้!", RED, 92)
        else:
            title(g, t, L[2], "แต่เบื้องหลังการยอมถอย...", INK, 84)
        return
    if t < L[6] - 0.2:   # ดีลลับใต้โต๊ะ + เคนเนดี
        deal_table(g, CX, 1000, 1.0, t, e_io(seg(t, L[4] + 0.2, L[4] + 1.6)))
        if t < L[5] - 0.2:
            title(g, t, L[4], "\"ดีลลับใต้โต๊ะ\"", GOLDTXT, 100)
        else:
            jfk(g, 300, 0.7, "firm", "point", 0.3, talk=True)
            g.name_tag(t, L[5] + 0.1, 600, 560, "จอห์น เอฟ. เคนเนดี", "ประธานาธิบดีสหรัฐฯ", side=-1)
            title(g, t, L[5], "เคนเนดียอมแลก...", US, 92)
        return
    if t < L[7] - 0.2:   # สัญญาไม่บุกคิวบา
        caribbean_map(g, CX, 860, 0.85, t, missiles=0.0, ring=0.0, ships=0.0)
        with g.at(CX + 160, 760, ap(t, L[6] + 0.3), -8):
            g.rrect(-220, -70, 440, 140, 16, WHITE, 8, stroke=GREEN)
            g.label("ไม่บุกคิวบา", 0, 0, 64, color=GREEN)
        title(g, t, L[6], "สัญญาไม่บุกคิวบาเด็ดขาด", US, 84)
        return
    turkey_map(g, CX, 880, 1.2, t, e_io(seg(t, L[7] + 1.6, L[7] + 3.4)))   # ถอนจูปิเตอร์จากตุรกี
    g.label("อย่างลับ ๆ", CX, 1180, 64, color=GREY, sc=ap(t, L[7] + 1.0))
    title(g, t, L[7], "ถอนขีปนาวุธจูปิเตอร์ออกจากตุรกี", US, 76)


# ------------------------------------------------------------------ 5. hotline
def s_hotline(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[2] - 0.2:   # ปิดฉากด้วยการทูต
        jfk(g, 260, 0.74, "smile", "down", 0.4)
        khrushchev(g, 820, 0.74, "smile", "down", -0.4)
        if t < L[1] - 0.2:
            clock_face(g, CX, 760, 150, lerp(0.5, 15, e_io(seg(t, L[0], L[0] + 2.5))))
            title(g, t, L[0], "วิกฤต 13 วัน ปิดฉากแล้ว", INK, 86)
        else:
            dove(g, CX, 720 + 15 * math.sin(t * 2), 1.4 * ap(t, L[1]) + 0.01, t)
            title(g, t, L[1], "ด้วยการทูตและสติ", GREEN, 92)
        return
    if t < L[4] - 0.2:   # บทเรียน → สายด่วนฮอตไลน์สีแดง
        if t < L[3] - 0.2:
            time_bomb(g, CX, 900, 1.1, 0, 0.0)
            title(g, t, L[2], "บทเรียนที่เกือบสิ้นชาติ", RED, 88)
        else:
            red_phone(g, CX, 1000, 1.6, ap(t, L[3] + 0.5), t)
            title(g, t, L[3], "\"สายด่วนฮอตไลน์\" สีแดง", RED, 88)
        return
    building(g, 250, GROUND, 0.75, "white")   # ทำเนียบขาว ↔ เครมลิน
    building(g, 820, GROUND, 0.75, "kremlin")
    g.label("ทำเนียบขาว", 250, GROUND - 260, 46, color=US)
    g.label("เครมลิน", 820, GROUND - 360, 46, color=SOV)
    hotline(g, 330, 760, 860, t, e_io(seg(t, L[4], L[4] + 1.6)))
    red_phone(g, CX, 800, 0.5, 0.3, t)
    if t < L[5] - 0.2:
        title(g, t, L[4], "เชื่อมตรงทำเนียบขาว-เครมลิน", INK, 80)
    else:
        title(g, t, L[5], "ไม่ให้สื่อสารผิดพลาดอีก!", GREEN, 86)


# ------------------------------------------------------------------ 6. lesson
def s_lesson(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:
        calendar(g, CX, 860, 1.1, "28", "ต.ค. 1962", "อาทิตย์", -3 + 2 * math.sin(t), GREEN)
        title(g, t, L[0], "เรื่องราวนี้พิสูจน์ว่า...", INK, 86)
        return
    if t < L[2] - 0.2:   # ถอยหนึ่งก้าวไม่ใช่พ่ายแพ้
        x = lerp(560, 400, e_io(seg(t, L[1] + 0.3, L[1] + 1.4)))
        khrushchev(g, x, 0.8, "smile", "down", 0.3)
        g.label("← 1 ก้าว", 790, 760, 80, color=GREY, sc=ap(t, L[1] + 0.4))
        title(g, t, L[1], "ถอยหนึ่งก้าว ≠ พ่ายแพ้", INK, 86)
        return
    if t < L[3] - 0.2:   # การตัดสินใจที่ยิ่งใหญ่ที่สุด
        jfk(g, 280, 0.74, "firm", "down", 0.4)
        khrushchev(g, 800, 0.74, "firm", "down", -0.4)
        for i in range(5):
            g.sparkle(CX + 120 * math.cos(i * 1.25 + t), 760 + 120 * math.sin(i * 1.25 + t), 30)
        title(g, t, L[2], "การตัดสินใจที่ยิ่งใหญ่ที่สุด", GOLDTXT, 82)
        return
    globe(g, CX, 900, 260, t)   # รักษาชีวิตมนุษยชาติ
    dove(g, CX + 40, 590 + 15 * math.sin(t * 2), 1.0 * ap(t, L[3]) + 0.01, t)
    title(g, t, L[3], "รักษาชีวิตของมวลมนุษยชาติ", GREEN, 82)


# ------------------------------------------------------------------ 7. outro
def s_outro(g, t, L, d):
    g.ground(GROUND, WHITE)
    if t < L[1] - 0.2:
        jfk(g, 270, 0.76, "neutral", "think", 0.4)
        khrushchev(g, 810, 0.76, "neutral", "think", -0.4)
        g.label("?", CX, 760, 180, color=RED, sc=ap(t, L[0] + 0.4))
        title(g, t, L[0], "รู้สึกอย่างไรกันบ้าง?", INK, 92)
        return
    if t < L[3] - 0.2:   # ศักดิ์ศรี vs สันติภาพ
        chip(g, 300, 780, "ศักดิ์ศรีชาติ", RED, ap(t, L[1] + 0.2), -5, 340)
        g.label("vs", CX, 900, 80, color=GREY, sc=ap(t, L[2] - 0.1))
        chip(g, 780, 1000, "สันติภาพโลก", GREEN, ap(t, L[2]), 5, 340)
        if t > L[2] - 0.2:
            dove(g, 780, 820, 0.8, t)
        title(g, t, L[1], "ศักดิ์ศรี หรือ สันติภาพ?", INK, 86)
        return
    if t < L[4] - 0.2:   # ผู้นำยุคปัจจุบันจะกล้าไหม
        globe(g, CX, 860, 230, t)
        for i, sx in enumerate((-1, 1)):
            g.label("?", CX + sx * 320, 760 + 20 * math.sin(t * 3 + i), 130, color=RED, sc=ap(t, L[3] + 0.3 * i))
        title(g, t, L[3], "ผู้นำวันนี้จะกล้าไหม?", RED, 92)
        return
    with g.at(CX + 170, 640, ap(t, L[4])):   # ชวนคอมเมนต์
        g.bubble(0, 0, 460, 220, WHITE, tail=(-1, 1))
        for i in range(3):
            g.circle(-110 + i * 110, 0, 24 + 6 * math.sin(t * 6 - i), INK, 0)
    dove(g, 300, 760 + 15 * math.sin(t * 2), 1.2, t)
    title(g, t, L[4], "มาแลกเปลี่ยนกันในคอมเมนต์!", RED, 70)


SCENES = {
    "hook": s_hook, "tension": s_tension, "radio": s_radio, "deal": s_deal, "hotline": s_hotline,
    "lesson": s_lesson, "outro": s_outro,
}
NO_IRIS = set()
