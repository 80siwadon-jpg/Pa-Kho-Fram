"""ตัวละครและพร็อพ: เปิดพิพิธภัณฑ์กุกเกนไฮม์ 21 ต.ค. 1959 — คนแบบกึ่งเสมือนจริงจาก src/people.py"""
import math

from gfx import GOLD, GOLD2, GREY, INK, LGREY, NAVY, RED, WHITE, hexc, hn, lerp
from people import Look, _rr, _shade, _smooth_path, _stroke

CREAM = hexc("#f6f1e4")
CONCRETE = hexc("#9aa0ab")
CONCRETE2 = hexc("#c3c8d0")
GLASS_BLUE = hexc("#cfe3f3")
BLUEPRINT = hexc("#2f5f9a")

# แฟรงก์ ลอยด์ ไรต์: ชายชราผมขาวยาวปัดหลัง คิ้วบาง จมูกโด่ง หมวกพอร์คพายปีกกว้าง
# สูทสีครีม-น้ำตาล หูกระต่ายลายจุดเข้ม ผ้าคลุมไหล่ยาวสีดำ ถือไม้เท้า
WRIGHT = Look(hair="full", hair_col=hexc("#ece8df"), suit=hexc("#b9a27e"), tie=hexc("#3a2c3a"), bowtie=True,
              hat="porkpie", cape=hexc("#26252b"), w=56, jaw=0.35, nose=1.4, brow=0.6, age=0.95, build=0.9,
              height=0.96)
WRIGHT_YOUNG = Look(hair="full", hair_col=hexc("#d9d5cc"), suit=hexc("#b9a27e"), tie=hexc("#3a2c3a"), bowtie=True,
                    hat="porkpie", cape=hexc("#26252b"), w=56, jaw=0.35, nose=1.4, brow=0.7, age=0.8, build=0.92)
# นักวิจารณ์ยุค 50s: สูท แว่นกรอบหนา
CRITICS = [
    Look(hair="slick", hair_col=hexc("#3a2f28"), suit=hexc("#3b4250"), tie=hexc("#7a2e2e"), glasses="thick",
         w=60, jaw=0.6, jowls=0.4, nose=1.2, age=0.6),
    Look(hair="part", hair_col=hexc("#6b4a33"), suit=hexc("#5a4a3a"), tie=hexc("#2b3f63"), facial="mustache",
         w=57, age=0.5),
    Look(hair="crew", hair_col=hexc("#9a948a"), suit=hexc("#2f3a4a"), tie=hexc("#8a6a2a"), bowtie=True,
         glasses="thin", w=58, age=0.7),
]
# ศิลปินผู้ประท้วง: หมวกเบเร่ต์ เสื้อลำลอง
ARTISTS = [
    Look(hair="short", hair_col=hexc("#2b2622"), suit=hexc("#2a2a30"), outfit="tee", pants=hexc("#5a5a66"),
         hat="beret", hat_trim=hexc("#b8473a"), facial="goatee", w=56, age=0.4),
    Look(hair="bun", hair_col=hexc("#6b4a33"), suit=hexc("#3f6496"), outfit="dress", hat="beret",
         hat_trim=hexc("#2b2622"), w=54, age=0.3, height=0.94),
    Look(hair="part", hair_col=hexc("#9a6a3a"), suit=hexc("#e3a92b"), outfit="flannel", pants=hexc("#3a3a42"),
         hat="beret", hat_trim=hexc("#2f5a3a"), glasses="thick", w=58, age=0.5),
]
CROWD = [
    Look(hair="slick", hair_col=hexc("#3a2f28"), suit=hexc("#5a6b85"), tie=hexc("#7a2e2e"), w=58, age=0.4),
    Look(hair="bun", hair_col=hexc("#a8763e"), suit=hexc("#c8553d"), outfit="dress", w=54, age=0.3, height=0.93),
    Look(hair="crew", hair_col=hexc("#2b2622"), suit=hexc("#3a3a42"), tie=hexc("#2b3f63"), hat="porkpie",
         w=58, age=0.5),
    Look(hair="bun", hair_col=hexc("#2b2622"), suit=hexc("#3c8d4f"), outfit="dress", w=54, age=0.2, height=0.9),
    Look(hair="part", hair_col=hexc("#6b4a33"), suit=hexc("#8a6a4a"), tie=hexc("#2a2a30"), glasses="thin",
         w=57, age=0.6),
]


# ---------------------------------------------------------------- อาคาร
def guggenheim(g, x, y, sc=1.0, k=1.0, t=0.0, glow=0.0):
    """พิพิธภัณฑ์กุกเกนไฮม์ (มองด้านหน้า): วงเกลียวซ้อนบานออกด้านบน + อาคารเตี้ยด้านข้าง — x,y = กึ่งกลางฐาน
    k 0..1 สร้างขึ้นทีละชั้น"""
    c = g.c
    with g.at(x, y, sc):
        # อาคารเตี้ยด้านซ้าย (monitor building)
        _rr(c, -560, -230, 300, 230, 30)
        _shade(c, CREAM, 6, 0.2)
        _rr(c, -540, -120, 260, 40, 6)
        _shade(c, GLASS_BLUE, 4, 0)
        # ฐาน
        _rr(c, -300, -90, 600, 90, 6)
        _shade(c, CREAM, 6, 0.25)
        _rr(c, -280, -70, 560, 40, 4)
        _shade(c, GLASS_BLUE, 4, 0)
        g.label("GUGGENHEIM", -10, -48, 30, "kanit", INK) if k > 0.98 else None
        # วงเกลียว 4 ชั้น บานออกด้านบน
        n = 4
        for i in range(n):
            a = max(0.0, min(1.0, k * n - i))
            if a <= 0:
                continue
            w0 = 250 + i * 34
            w1 = w0 + 30
            y0 = -90 - i * 110
            with g.alpha(a):
                c.new_path()
                for px, py in [(-w0, y0), (w0, y0), (w1, y0 - 95), (-w1, y0 - 95)]:
                    c.line_to(px, py)
                c.close_path()
                _shade(c, CREAM, 6, 0.3)
                _stroke(c, [(-w0 + 6, y0 - 4), (w0 - 6, y0 - 4)], 8, (0, 0, 0, 0.12), smooth=False)
                _rr(c, -w0 + 10, y0 - 18, 2 * w0 - 20, 14, 4)   # ช่องแสงแนวยาว
                _shade(c, GLASS_BLUE, 3, 0)
        # โดมกระจกด้านบน
        if k > 0.98:
            c.new_path()
            c.save()
            c.translate(0, -90 - n * 110 + 15)
            c.scale(1, 0.35)
            c.arc(0, 0, 200, math.pi, 2 * math.pi)
            c.restore()
            _shade(c, GLASS_BLUE, 5, 0.1)
            if glow > 0:
                g.sunburst(0, -560, 230, 420, 18, t * 10, 9, (0.95, 0.83, 0.48, 0.7 * glow))


def skyscraper(g, x, y, w, h, col=CONCRETE, seed=1, lit=0.0):
    """ตึกสูงสี่เหลี่ยม (ป่าคอนกรีต) — x,y = มุมซ้ายล่าง"""
    c = g.c
    _rr(c, x, y - h, w, h, 3)
    _shade(c, col, 6, 0.3)
    cols = max(1, int((w - 24) // 36))
    rows = max(1, int((h - 30) // 50))
    for r in range(rows):
        for q in range(cols):
            on = lit > 0 and hn(r * 7 + q, seed) < lit
            _rr(c, x + 14 + q * 36, y - h + 18 + r * 50, 22, 30, 2)
            _shade(c, hexc("#ffd27a") if on else hexc("#e3edf5"), 2, 0)


def city_row(g, x0, x1, y, seed=3, gap=None, h0=420, h1=780):
    """แถวตึกสูงเรียงกัน เว้นช่องว่างตรง gap=(xa, xb) ไว้ให้กุกเกนไฮม์"""
    x = x0
    i = 0
    while x < x1:
        w = 120 + int(hn(i, seed) * 90)
        h = h0 + int(hn(i, seed + 1) * (h1 - h0))
        if gap and gap[0] - w < x < gap[1]:
            x = gap[1]
            continue
        skyscraper(g, x, y, w, h, CONCRETE if i % 2 else CONCRETE2, seed + i)
        x += w + 10
        i += 1


def spiral_cut(g, cx, top, bottom, t, walkers=True, k=1.0, wall_art=False, car=True):
    """ภาพตัดด้านข้าง: ทางลาดวนเป็นเกลียว (เส้นซิกแซกลาดลง) + โถงกลาง + ลิฟต์ + คนเดินไหลลง"""
    c = g.c
    levels = 5
    lh = (bottom - top) / levels
    half = 330
    pts = []
    for i in range(levels + 1):
        yy = top + i * lh
        side = -1 if i % 2 == 0 else 1
        pts.append((cx + side * half, yy))
    shown = k * levels
    # ทางลาด
    for i in range(levels):
        a = max(0.0, min(1.0, shown - i))
        if a <= 0:
            continue
        (xa, ya), (xb, yb) = pts[i], pts[i + 1]
        xe, ye = lerp(xa, xb, a), lerp(ya, yb, a)
        g.line([(xa, ya), (xe, ye)], 22, INK, amp=0)
        g.line([(xa, ya), (xe, ye)], 12, CREAM, amp=0)
        if wall_art and a >= 1:
            for q in range(3):   # ภาพวาดสี่เหลี่ยมบนผนังโค้ง
                u = 0.25 + q * 0.25
                px, py = lerp(xa, xb, u), lerp(ya, yb, u) - 60
                with g.at(px, py, 1, (yb - ya) / (xb - xa) * 57.3 * 0.5):
                    _rr(c, -26, -30, 52, 40, 2)
                    _shade(c, [hexc("#c8553d"), hexc("#3f6496"), hexc("#e3a92b")][(i + q) % 3], 3, 0.1)
    # ลิฟต์ (กลางโถง)
    if k >= 1:
        _rr(c, cx - 30, top - 40, 60, bottom - top + 40, 6)
        _shade(c, (0.9, 0.93, 0.97, 1), 4, 0)
        if car:
            ly = lerp(bottom - 60, top - 30, (math.sin(t * 0.9) + 1) / 2)
            _rr(c, cx - 24, ly, 48, 56, 4)
            _shade(c, GOLD, 3, 0.2)
    # คนเดินไหลลง (จุดสีเล็ก ๆ ไหลตามทางลาด)
    if walkers and k >= 1:
        cols = [hexc("#c8553d"), hexc("#3f6496"), hexc("#3c8d4f"), hexc("#e3a92b"), NAVY]
        for j in range(12):
            u = (t * 0.06 + j / 12) % 1
            seg_i = int(u * levels)
            f = u * levels - seg_i
            (xa, ya), (xb, yb) = pts[seg_i], pts[seg_i + 1]
            px, py = lerp(xa, xb, f), lerp(ya, yb, f)
            g.circle(px, py - 30, 9, cols[j % 5], 3)
            _rr(c, px - 9, py - 21, 18, 22, 6)
            _shade(c, cols[j % 5], 3, 0)
    return pts


def box_building(g, x, y, w, h, sc=1.0):
    """กล่องสี่เหลี่ยมแบ่งห้อง (แบบเดิม ๆ)"""
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -w / 2, -h, w, h, 4)
        _shade(c, CONCRETE2, 6, 0.25)
        for r in range(3):
            for q in range(3):
                _rr(c, -w / 2 + 20 + q * (w - 40) / 3, -h + 20 + r * (h - 40) / 3, (w - 40) / 3 - 14, (h - 40) / 3 - 14, 3)
                _shade(c, WHITE, 3, 0)


def washing_machine(g, x, y, sc=1.0, t=0.0):
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -150, -320, 300, 320, 22)
        _shade(c, WHITE, 6, 0.2)
        _rr(c, -150, -320, 300, 60, 18)
        _shade(c, LGREY, 5, 0.1)
        for k in range(3):
            g.circle(-100 + k * 40, -290, 10, GREY, 3)
        c.new_path()
        c.arc(0, -140, 92, 0, 2 * math.pi)
        _shade(c, CONCRETE2, 6, 0.1)
        c.new_path()
        c.arc(0, -140, 70, 0, 2 * math.pi)
        _shade(c, hexc("#bcd8ec"), 5, 0.1)
        for k in range(3):   # ฟองหมุน
            a = t * 3 + k * 2.1
            g.circle(30 * math.cos(a), -140 + 30 * math.sin(a), 14, WHITE, 3)


def toilet(g, x, y, sc=1.0):
    """โถส้วม (มองด้านหน้า แบบการ์ตูน) — ใช้เปรียบเทียบคำล้อเลียน"""
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -110, -420, 220, 170, 16)
        _shade(c, WHITE, 6, 0.15)
        _smooth_path(c, [(-150, -250), (150, -250), (120, -150), (60, -90), (-60, -90), (-120, -150)])
        _shade(c, WHITE, 6, 0.2)
        _smooth_path(c, [(-80, -90), (80, -90), (64, 0), (-64, 0)])
        _shade(c, WHITE, 6, 0.25)
        _rr(c, -20, -390, 40, 14, 6)
        _shade(c, LGREY, 3, 0)


def letter(g, x, y, sc=1.0, rot=0.0, title="จดหมายประท้วง"):
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -170, -220, 340, 440, 8)
        _shade(c, CREAM, 6, 0.15)
        g.label(title, 0, -160, 40, color=RED)
        for k in range(7):
            _stroke(c, [(-130, -90 + k * 34), (130 - (k == 6) * 120, -90 + k * 34)], 6, LGREY, smooth=False)
        for k in range(5):   # ลายเซ็น
            sx = -120 + k * 60
            _stroke(c, [(sx, 170), (sx + 14, 150), (sx + 26, 176), (sx + 40, 156)], 3, NAVY)


def painting(g, x, y, w, h, rot=0.0, col=None, seed=1):
    c = g.c
    with g.at(x, y, 1, rot):
        _rr(c, -w / 2 - 12, -h / 2 - 12, w + 24, h + 24, 4)
        _shade(c, GOLD, 5, 0.2)
        _rr(c, -w / 2, -h / 2, w, h, 2)
        _shade(c, CREAM, 3, 0)
        cols = [hexc("#c8553d"), hexc("#3f6496"), hexc("#e3a92b"), hexc("#3c8d4f")]
        g.circle(-w * 0.15, -h * 0.1, min(w, h) * 0.25, cols[seed % 4], 4)
        _rr(c, w * 0.05, -h * 0.05, w * 0.3, h * 0.35, 2)
        _shade(c, cols[(seed + 1) % 4], 4, 0)


def blueprint(g, x, y, sc=1.0, rot=0.0, spiral=True):
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -200, -140, 400, 280, 6)
        _shade(c, BLUEPRINT, 6, 0.15)
        for k in range(-3, 4):
            _stroke(c, [(k * 54, -130), (k * 54, 130)], 1.5, WHITE, 0.25, smooth=False)
        if spiral:
            pts = []
            for i in range(80):
                a = i * 0.25
                r = 10 + i * 1.3
                pts.append((r * math.cos(a), r * math.sin(a) * 0.9))
            _stroke(c, pts, 3, WHITE, 0.9)
        else:
            _rr(c, -90, -90, 180, 180, 2)
            c.set_source_rgba(1, 1, 1, 0.9)
            c.set_line_width(3)
            c.stroke()


def cane(g, x, y, sc=1.0, rot=0.0):
    with g.at(x, y, sc, rot):
        g.line([(0, 0), (0, -420)], 10, hexc("#5a3a22"), amp=0)
        g.arc(-26, -420, 26, math.pi, 2 * math.pi, 10, hexc("#5a3a22"))


def drafting_table(g, x, y, sc=1.0):
    """โต๊ะเขียนแบบเอียง — x,y = พื้น"""
    c = g.c
    with g.at(x, y, sc):
        for sx in (-1, 1):
            g.line([(sx * 150, 0), (sx * 60, -420)], 12, hexc("#7a5230"), amp=0)
        with g.at(0, -440, 1, -14):
            _rr(c, -240, -20, 480, 40, 6)
            _shade(c, hexc("#a8763e"), 6, 0.2)
            _rr(c, -210, -24, 420, 10, 2)
            _shade(c, WHITE, 3, 0)


def rule_book(g, x, y, sc=1.0, title="กฎหมายอาคาร"):
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -150, -200, 300, 400, 10)
        _shade(c, hexc("#7a2e2e"), 6, 0.25)
        _rr(c, -130, -180, 260, 360, 6)
        c.set_source_rgba(1, 1, 1, 0.12)
        c.fill()
        g.label(title, 0, -40, 40, color=GOLD2)
        g.label("§", 0, 60, 90, color=GOLD2)


def empty_chair(g, x, y, sc=1.0):
    c = g.c
    with g.at(x, y, sc):
        for lx in (-80, 80):
            g.line([(lx, 0), (lx, -220)], 12, hexc("#7a5230"), amp=0)
        _rr(c, -110, -240, 220, 34, 8)
        _shade(c, hexc("#a8763e"), 6, 0.2)
        _rr(c, -100, -520, 200, 280, 14)
        _shade(c, hexc("#8a5a36"), 6, 0.25)
