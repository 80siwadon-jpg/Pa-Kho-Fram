"""ตัวละครและพร็อพ: สนธิสัญญาสันติภาพเวสต์ฟาเลีย 24 ต.ค. 1648
ไม่แสดงความรุนแรง/ความทุกข์ทรมานตรง ๆ: ใช้ควัน เปลวไฟไกล ๆ บ้านไหม้เป็นเงา ชามเปล่า ไม้กางเขนป้ายหลุมศพ"""
import math

from gfx import GOLD, GOLD2, GREY, INK, NAVY, RED, WHITE, hexc
from people import Look, _rr, _shade, _smooth_path, _stroke

PARCH = hexc("#f1e3c0")
WAX = hexc("#b8232e")
FIRE = hexc("#f2a93b")

# ทูตเจรจาสันติภาพ (ศตวรรษที่ 17): ผมยาวประบ่า หนวดเคราแหลม ปกลูกไม้ขาว เสื้อคลุมเข้ม หมวกปีกกว้าง
ENVOYS = [
    Look(hair="long", hair_col=hexc("#4a3a2c"), suit=hexc("#2b2622"), outfit="vest", shirt=hexc("#2b2622"),
         tie=hexc("#2b2622"), band=True, facial="goatee", w=56, age=0.55, hat="cavalier"),
    Look(hair="long", hair_col=hexc("#8a6a42"), suit=hexc("#3a2a4a"), outfit="vest", shirt=hexc("#3a2a4a"),
         tie=hexc("#3a2a4a"), band=True, facial="mustache", w=57, age=0.5),
    Look(hair="long", hair_col=hexc("#d9d5cc"), suit=hexc("#5a1f24"), outfit="vest", shirt=hexc("#5a1f24"),
         tie=hexc("#5a1f24"), band=True, facial="goatee", w=58, age=0.75, jowls=0.3),
    Look(hair="long", hair_col=hexc("#2b2622"), suit=hexc("#1f3a2a"), outfit="vest", shirt=hexc("#1f3a2a"),
         tie=hexc("#1f3a2a"), band=True, facial="mustache", w=56, age=0.4, hat="cavalier", hat_trim=hexc("#3a2a1a")),
]
PEASANTS = [
    Look(hair="short", hair_col=hexc("#6b4a33"), outfit="tee", suit=hexc("#8a7a5a"), pants=hexc("#5a4a3a"), w=56,
         age=0.5, stubble=0.5),
    Look(hair="bun", hair_col=hexc("#5a3a22"), outfit="dress", suit=hexc("#7a6a52"), w=54, age=0.4, height=0.93),
    Look(hair="short", hair_col=hexc("#8a6a42"), outfit="tee", suit=hexc("#9a8a6a"), pants=hexc("#5a4a3a"), w=54,
         height=0.62, headsc=1.4),
]
SOLDIER = Look(hair="long", hair_col=hexc("#4a3a2c"), suit=hexc("#6b5a3a"), outfit="vest", shirt=hexc("#6b5a3a"),
               tie=hexc("#6b5a3a"), facial="mustache", w=56, age=0.45, hat="cavalier", hat_trim=hexc("#4a3a2a"))


def church(g, x, y, sc=1.0, t=0.0, ring=0.0):
    """โบสถ์ยอดแหลม + ระฆังแกว่ง + คลื่นเสียง"""
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -200, -300, 400, 300, 4)
        _shade(c, hexc("#e8e0cc"), 6, 0.2)
        _rr(c, -40, -150, 80, 150, 40)
        _shade(c, hexc("#6e4528"), 5, 0.2)
        _rr(c, -90, -620, 180, 330, 4)
        _shade(c, hexc("#e8e0cc"), 6, 0.25)
        c.new_path()
        for p in [(-110, -620), (0, -880), (110, -620)]:
            c.line_to(*p)
        c.close_path()
        _shade(c, hexc("#5a7a8a"), 6, 0.3)
        g.line([(0, -880), (0, -960)], 8, INK, amp=0)
        g.line([(-28, -930), (28, -930)], 8, INK, amp=0)
        _rr(c, -60, -560, 120, 140, 50)
        _shade(c, hexc("#3a3a40"), 4, 0)
        with g.at(0, -540, 1, 25 * math.sin(t * 5) * ring):
            _smooth_path(c, [(-36, 60), (-28, 0), (0, -14), (28, 0), (36, 60)])
            _shade(c, GOLD, 5, 0.3)
            g.circle(0, 66, 10, GOLD2, 3)
        if ring > 0:
            for i in range(3):
                u = (t * 0.8 + i / 3) % 1
                g.arc(0, -500, 120 + 220 * u, -60, 60, 7, (0.7, 0.55, 0.2, ring * (1 - u)))
                g.arc(0, -500, 120 + 220 * u, 120, 240, 7, (0.7, 0.55, 0.2, ring * (1 - u)))


def village(g, y, t=0.0, burn=0.0, a=1.0):
    """หมู่บ้านเยอรมันบ้านโครงไม้ — burn = เงาบ้านไหม้ + ควัน (ไกล ๆ ไม่มีคน)"""
    c = g.c
    with g.alpha(a):
        for i in range(6):
            x = -40 + i * 200
            h = 200 + (i * 53) % 80
            col = hexc("#efe6cf") if burn < 0.5 else hexc("#5a4a42")
            _rr(c, x - 80, y - h, 160, h, 2)
            _shade(c, col, 5, 0.2)
            c.new_path()
            for p in [(x - 100, y - h), (x, y - h - 110), (x + 100, y - h)]:
                c.line_to(*p)
            c.close_path()
            _shade(c, hexc("#a8473a") if burn < 0.5 else hexc("#3a2e2a"), 5, 0.2)
            if burn < 0.5:
                for k in (-1, 1):
                    _stroke(c, [(x + k * 60, y - h), (x - k * 60, y - 10)], 5, hexc("#6e4528"), 0.8, smooth=False)
            if burn > 0:
                for j in range(3):
                    u = (t * 0.4 + j / 3 + i * 0.13) % 1
                    g.circle(x + 20 * math.sin(t + j + i), y - h - 120 - 300 * u, 40 + 50 * u,
                             (0.35, 0.33, 0.32, 0.6 * burn * (1 - u)), 0)
                fl = 1 + 0.15 * math.sin(t * 9 + i)
                with g.at(x, y - h - 40, burn * fl):
                    _smooth_path(c, [(-50, 40), (-30, -40), (0, -90), (30, -40), (50, 40)])
                    _shade(c, FIRE, 3, 0)


def empty_bowl(g, x, y, sc=1.0):
    c = g.c
    with g.at(x, y, sc):
        _smooth_path(c, [(-110, -60), (110, -60), (80, 20), (-80, 20)])
        _shade(c, hexc("#8a6a42"), 6, 0.3)
        _rr(c, -120, -72, 240, 20, 10)
        _shade(c, hexc("#a8834f"), 4, 0.1)


def grave_crosses(g, x, y, n=7, sc=1.0, k=1.0):
    with g.at(x, y, sc):
        for i in range(n):
            kk = max(0.0, min(1.0, k * n - i))
            if kk < 0.02:
                continue
            with g.at(-n * 70 + 70 + i * 140, 0, kk, (i % 3 - 1) * 5):
                g.line([(0, 0), (0, -140)], 14, hexc("#6e4528"), amp=0)
                g.line([(-40, -100), (40, -100)], 14, hexc("#6e4528"), amp=0)


def sword(g, x, y, sc=1.0, rot=0.0):
    c = g.c
    with g.at(x, y, sc, rot):
        _smooth_path(c, [(-12, -300), (0, -340), (12, -300), (10, 0), (-10, 0)])
        _shade(c, hexc("#c9ced6"), 5, 0.3)
        _rr(c, -70, 0, 140, 22, 8)
        _shade(c, GOLD, 4, 0.2)
        _rr(c, -12, 22, 24, 90, 8)
        _shade(c, hexc("#6e4528"), 4, 0.2)


def treaty(g, x, y, sc=1.0, rot=0.0, seals=3, lines=1.0, t=0.0):
    """เอกสารสนธิสัญญา + ตราประทับครั่ง"""
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -240, -320, 480, 640, 8)
        _shade(c, PARCH, 6, 0.2)
        g.text("PAX", 0, -250, 60, "kanit", hexc("#6e4528"))
        n = int(9 * lines)
        for i in range(n):
            g.line([(-190, -170 + i * 38), (190 - 40 * (i % 3), -170 + i * 38)], 5, hexc("#a8834f"), amp=0)
        for i in range(seals):
            sx = -150 + i * 150
            g.line([(sx, 210), (sx - 20, 300)], 8, hexc("#d9a441"), amp=0)
            g.circle(sx, 220, 40, WAX, 5)
            g.circle(sx, 220, 22, hexc("#8a1a22"), 0)


def quill(g, x, y, sc=1.0, rot=0.0):
    c = g.c
    with g.at(x, y, sc, rot):
        _smooth_path(c, [(0, 0), (-30, -200), (-10, -320), (30, -200)])
        _shade(c, WHITE, 4, 0.15)
        _stroke(c, [(0, 0), (-10, -300)], 3, GREY, smooth=False)
        g.line([(0, 0), (6, 40)], 6, INK, amp=0)


def table(g, x, y, w=800, sc=1.0):
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -w / 2, -40, w, 40, 6)
        _shade(c, hexc("#2f6a3a"), 5, 0.2)   # ผ้าปูโต๊ะเขียว
        _rr(c, -w / 2 + 10, 0, w - 20, 110, 4)
        _shade(c, hexc("#2a5a32"), 5, 0.3)


def europe_patchwork(g, x, y, sc=1.0, t=0.0, borders=1.0, n=1.0):
    """ยุโรปเป็นแปลงหลากสี (รัฐอธิปไตย) + เส้นพรมแดน — ภาพเชิงสัญลักษณ์"""
    c = g.c
    cols = [hexc("#f2c94c"), hexc("#8fc7e0"), hexc("#e2788f"), hexc("#9fd08a"), hexc("#d9b26a"), hexc("#b8a0d0"),
            hexc("#f0a070"), hexc("#a0d0c0"), hexc("#e8d080")]
    with g.at(x, y, sc):
        k = 0
        for r in range(3):
            for q in range(3):
                kk = max(0.0, min(1.0, n * 9 - k))
                cx, cy = -260 + q * 260 + (r % 2) * 40, -260 + r * 260
                if kk > 0.02:
                    with g.at(cx, cy, kk, (k * 17) % 9 - 4):
                        g.blob(0, 0, 120, 110, cols[k], 0, seed=k + 3, amp=0.12)
                        if borders > 0:
                            with g.alpha(borders):
                                g.blob(0, 0, 120, 110, (1, 1, 1, 0), 6, seed=k + 3, amp=0.12)
                k += 1


def crown(g, x, y, sc=1.0, rot=0.0, col=GOLD):
    c = g.c
    with g.at(x, y, sc, rot):
        _smooth_path(c, [(-90, 0), (-100, -110), (-50, -50), (0, -130), (50, -50), (100, -110), (90, 0)])
        _shade(c, col, 6, 0.3)
        for k in (-60, 0, 60):
            g.circle(k, -20, 12, RED, 3)


def papal_tiara(g, x, y, sc=1.0, rot=0.0):
    """มงกุฎสามชั้นของพระสันตะปาปา (สัญลักษณ์)"""
    c = g.c
    with g.at(x, y, sc, rot):
        _smooth_path(c, [(-70, 0), (-60, -140), (-30, -200), (30, -200), (60, -140), (70, 0)])
        _shade(c, WHITE, 6, 0.25)
        for yy in (-40, -100, -160):
            _stroke(c, [(-62 + (yy < -120) * 20, yy), (62 - (yy < -120) * 20, yy)], 12, GOLD, smooth=False)
        g.line([(0, -200), (0, -240)], 6, INK, amp=0)
        g.line([(-14, -226), (14, -226)], 6, INK, amp=0)


def shield(g, x, y, sc=1.0, t=0.0, crack=0.0):
    c = g.c
    with g.at(x, y, sc):
        _smooth_path(c, [(-130, -150), (130, -150), (120, 40), (0, 160), (-120, 40)])
        _shade(c, hexc("#5a7a9a"), 7, 0.3)
        _smooth_path(c, [(-90, -110), (90, -110), (84, 20), (0, 110), (-84, 20)])
        _shade(c, hexc("#8fb0d0"), 4, 0.15)
        if crack > 0:
            _stroke(c, [(0, -150), (20, -60), (-20, 10), (10, 80)][:2 + int(2 * crack)], 7, INK, smooth=False)
