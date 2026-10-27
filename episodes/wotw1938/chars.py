"""ตัวละครและพร็อพ: ละครวิทยุ The War of the Worlds (30 ต.ค. 1938)
ยานสามขา/ชาวดาวอังคารวาดเองตามนิยาย เอช. จี. เวลส์ (สาธารณสมบัติ) แบบการ์ตูนน่ารัก — ไม่มีภาพคนบาดเจ็บ
Citizen Kane: ไม่ใช้โปสเตอร์จริง วาดม้วนฟิล์ม/ป้ายชื่อเรื่องแทน"""
import importlib.util
import math
import os

from gfx import GOLD, GOLD2, GREY, INK, NAVY, RED, WHITE, hexc
from people import Look, _rr, _shade, _smooth_path, _stroke


def _load(ep):
    spec = importlib.util.spec_from_file_location(f"{ep}_chars",
                                                  os.path.join(os.path.dirname(__file__), "..", ep, "chars.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


_cu = _load("cuba1962")
_st = _load("saturday1973")
_cr = _load("crash1929")
_wp = _load("westphalia1648")
_bo = _load("boeing707_1958")
_bd = _load("border1818")
_kp = _load("katyperry1984")
_fi = _load("fisher1956")
_al = _load("alamein1942")
_me = _load("metre1983")
FAMILY = _cu.FAMILY
rotary_phone = _st.phone
headline = _cr.headline
church = _wp.church
house, globe = _bo.house, _bo.globe
old_car = _bd.car
smartphone = _kp.phone
microphone = _fi.microphone
smoke = _al.smoke
planet = _me.planet

WOOD = hexc("#8a5a3a")
MARS = hexc("#c8553d")
MARTIAN = hexc("#7fb069")
GAS = (0.32, 0.34, 0.3)
HEAT = (1, 0.55, 0.2)

# ออร์สัน เวลส์ วัย 23: หน้ากลมอ่อนเยาว์ ผมดำหยักเสยหลัง คิ้วเข้ม ตัวสูงใหญ่ สูทเข้มเนกไท
WELLES = Look(hair="full", hair_col=hexc("#2b2018"), suit=hexc("#2f3036"), tie=hexc("#6a2a2a"), w=64, jaw=0.35,
              nose=0.95, brow=1.35, age=0.0, build=1.1, height=1.02)
ANNOUNCER = Look(hair="part", hair_col=hexc("#5a4632"), suit=hexc("#4a4d55"), tie=hexc("#2b2f3a"), w=58, age=0.4,
                 facial="mustache")
ASTRONOMER = Look(hair="edison", hair_col=hexc("#b9b4aa"), suit=hexc("#5a5d63"), tie=INK, w=58, age=0.75,
                  glasses="thin", facial="beard")
LISTENERS = [
    Look(hair="part", hair_col=hexc("#3a2f28"), outfit="vest", suit=hexc("#6a5a4a"), w=58, age=0.4,
         facial="mustache"),
    Look(hair="bun", hair_col=hexc("#8a5a2a"), outfit="dress", suit=hexc("#6a7a9a"), w=54, age=0.3, height=0.93),
    Look(hair="short", hair_col=hexc("#3a2a1e"), outfit="tee", suit=hexc("#c8553d"), pants=hexc("#3a4a6a"), w=54,
         height=0.6, headsc=1.45),
    Look(hair="slick", hair_col=hexc("#1b1714"), suit=hexc("#3a3f48"), tie=hexc("#7a2e2e"), w=57, age=0.2,
         hat="bowler"),
]


def radio(g, x, y, sc=1.0, t=0.0, on=1.0, col=hexc("#c8553d")):
    """วิทยุตู้ไม้ทรงโค้งยุค 30 + คลื่นเสียง"""
    c = g.c
    with g.at(x, y, sc):
        _smooth_path(c, [(-200, 0), (-200, -220), (-150, -330), (0, -370), (150, -330), (200, -220), (200, 0)])
        _shade(c, WOOD, 7, 0.3)
        _smooth_path(c, [(-150, -150), (-150, -230), (-100, -300), (0, -320), (100, -300), (150, -230),
                         (150, -150)])
        _shade(c, hexc("#e8dcc0"), 5, 0.05)
        for i in range(7):
            _stroke(c, [(-110 + i * 37, -290 + 20 * abs(i - 3) ** 1.1), (-110 + i * 37, -160)], 4,
                    hexc("#a8946a"), smooth=False)
        _rr(c, -120, -120, 240, 46, 8)
        _shade(c, hexc("#f2d68a"), 4, 0)
        nx = -100 + 200 * (0.5 + 0.5 * math.sin(t * 0.7))
        _stroke(c, [(nx, -116), (nx, -78)], 4, RED, smooth=False)
        for i in range(2):
            g.circle(-90 + i * 180, -40, 24, hexc("#3a2a1e"), 4)
    if on > 0:
        for i in range(3):
            u = (t * 1.2 + i / 3) % 1
            g.arc(x, y - 200 * sc, (230 + 240 * u) * sc, -50, 50, 8, (*col[:3], (1 - u) * on))
            g.arc(x, y - 200 * sc, (230 + 240 * u) * sc, 130, 230, 8, (*col[:3], (1 - u) * on))


def note(g, x, y, s=1.0, col=INK, rot=0.0):
    """โน้ตดนตรี (วาดเอง ไม่ใช้อักขระ)"""
    with g.at(x, y, s, rot):
        g.c.save()
        g.c.translate(0, 0)
        g.c.scale(1.3, 1)
        g.c.new_path()
        g.c.arc(0, 0, 20, 0, 2 * math.pi)
        g.c.restore()
        g.c.set_source_rgba(*col)
        g.c.fill()
        g.line([(24, -4), (24, -90)], 7, col, amp=0)
        g.line([(24, -90), (54, -64)], 9, col, amp=0)


def flash_bulletin(g, x, y, sc=1.0, rot=0.0, txt="ข่าวด่วน!"):
    with g.at(x, y, sc, rot):
        g.rrect(-200, -70, 400, 140, 24, RED, 7)
        g.text(txt, 0, 0, 70, "kanit", WHITE)


def martian(g, x, y, sc=1.0, t=0.0):
    """ชาวดาวอังคารคล้ายปลาหมึก (การ์ตูน)"""
    c = g.c
    with g.at(x, y, sc):
        for i in range(6):
            a = -0.9 + i * 0.36
            ph = t * 4 + i
            pts = [(30 * math.sin(a), 0)]
            for k in range(1, 5):
                pts.append((pts[-1][0] + 26 * math.sin(a) + 10 * math.sin(ph + k), pts[-1][1] + 34))
            _stroke(c, pts, 16, MARTIAN, 1)
            _stroke(c, pts, 3, INK, 0.5)
        g.blob(0, -60, 90, 80, MARTIAN, 6, seed=3)
        for sx in (-1, 1):
            g.circle(sx * 32, -70, 24, WHITE, 5)
            g.circle(sx * 32 + 4 * math.sin(t), -66, 10, INK, 0)


def tripod(g, x, y, sc=1.0, t=0.0, ray=0.0, ray_to=None, walk=0.0):
    """ยานรบสามขา (ตามนิยาย) — ray 0..1 ยิงแสงความร้อนไปที่ ray_to (พิกัดจอ)"""
    c = g.c
    hx, hy = x, y - 620 * sc
    for i, dx in enumerate((-240, 0, 240)):
        st = 30 * math.sin(t * 3 + i * 2.1) * walk
        kx, ky = x + (dx * 0.55 + st * 0.5) * sc, y - 320 * sc
        fx, fy = x + (dx + st) * sc, y
        _stroke(c, [(hx + dx * 0.15 * sc, hy + 60 * sc), (kx, ky)], 22 * sc, hexc("#6a6e78"), 1, smooth=False)
        _stroke(c, [(kx, ky), (fx, fy)], 18 * sc, hexc("#6a6e78"), 1, smooth=False)
        g.circle(kx, ky, 18 * sc, hexc("#4a4d55"), 4)
    with g.at(hx, hy, sc):
        _smooth_path(c, [(-180, 40), (-150, -60), (0, -110), (150, -60), (180, 40), (0, 80)])
        _shade(c, hexc("#9aa0aa"), 7, 0.35)
        _rr(c, -110, -40, 220, 40, 16)
        _shade(c, hexc("#3a3d45"), 4, 0)
        g.circle(0, -20, 18, (1, 0.4, 0.2, 0.6 + 0.4 * math.sin(t * 6)), 3)
        _stroke(c, [(140, 30), (210, 70)], 14, hexc("#6a6e78"), 1, smooth=False)
    if ray > 0 and ray_to:
        sx, sy = hx + 210 * sc, hy + 70 * sc
        ex, ey = sx + (ray_to[0] - sx) * ray, sy + (ray_to[1] - sy) * ray
        _stroke(c, [(sx, sy), (ex, ey)], 26 * sc, (*HEAT, 0.5), 1, smooth=False)
        _stroke(c, [(sx, sy), (ex, ey)], 10 * sc, (1, 0.95, 0.7, 1), 1, smooth=False)
        g.circle(ex, ey, 40 * sc + 8 * math.sin(t * 20), (*HEAT, 0.7), 0)


def gas_cloud(g, x, y, s=1.0, t=0.0, k=1.0):
    if k <= 0.02:
        return
    for i in range(8):
        a = i * 0.8 + t * 0.2
        g.circle(x + s * (140 * math.cos(a) + 30 * math.sin(t + i)), y + s * 50 * math.sin(a), s * (90 + 12 * (i % 3)),
                 (*GAS, 0.75 * k), 0)


def cylinder(g, x, y, sc=1.0, t=0.0, open_k=0.0):
    """อุกกาบาต/กระบอกโลหะตกในหลุม"""
    c = g.c
    with g.at(x, y, sc):
        g.c.save()
        g.c.scale(1, 0.3)
        g.c.new_path()
        g.c.arc(0, 0, 300, 0, 2 * math.pi)
        g.c.restore()
        _shade(c, hexc("#a8865a"), 6, 0.3)
        with g.at(0, -40, 1, -18):
            _rr(c, -170, -90, 340, 180, 90)
            _shade(c, hexc("#8a8e98"), 7, 0.35)
            g.circle(160, 0, 80, hexc("#6a6e78"), 6)
            if open_k > 0:
                g.circle(160, 0, 70 * open_k, (1, 0.8, 0.4, 0.9), 0)
    for i in range(4):
        smoke(g, x - 120 * sc + i * 80 * sc, y - 120 * sc, 40 * sc, t, n=3, seed=i)


def wet_towel_face(g, x, y, sc=1.0, t=0.0):
    """ผ้าเปียกคลุมหน้า (ภาพใกล้ หัว + ผ้า)"""
    c = g.c
    with g.at(x, y, sc):
        g.circle(0, 0, 120, hexc("#f0c8a0"), 6)
        g.c.save()
        g.c.new_path()
        g.c.arc(0, 0, 118, 0, 2 * math.pi)
        g.c.clip()
        _rr(c, -140, -10, 280, 160, 10)
        _shade(c, hexc("#a8c8e0"), 5, 0.2)
        g.c.restore()
        for sx in (-1, 1):
            g.circle(sx * 42, -40, 14, INK, 0)
            g.line([(sx * 70, -78), (sx * 20, -68)], 6, INK, amp=0)
        for i in range(3):
            u = (t * 1.5 + i / 3) % 1
            g.poly([(-60 + i * 60, 130 + 50 * u), (-50 + i * 60, 150 + 50 * u), (-70 + i * 60, 150 + 50 * u)],
                   (0.55, 0.8, 1, 1 - u), 0, amp=0)


def pumpkin(g, x, y, sc=1.0, t=0.0):
    c = g.c
    with g.at(x, y, sc, 4 * math.sin(t * 2)):
        for dx, w in ((-60, 70), (60, 70), (0, 80)):
            g.blob(dx, 0, w, 90, hexc("#e8833a"), 6, seed=int(dx) + 5)
        _rr(c, -12, -110, 24, 36, 6)
        _shade(c, hexc("#4a6a2a"), 4, 0)
        for sx in (-1, 1):
            g.poly([(sx * 50, -30), (sx * 30, -6), (sx * 70, -6)], INK, 0, amp=0)
        g.poly([(-60, 30), (-30, 50), (0, 30), (30, 50), (60, 30), (30, 60), (-30, 60)], INK, 0, amp=0)


def film_reel(g, x, y, r, t=0.0):
    c = g.c
    with g.at(x, y, 1, math.degrees(t * 0.8)):
        g.circle(0, 0, r, hexc("#3a3d45"), 7)
        for i in range(6):
            a = i * math.pi / 3
            g.circle(r * 0.55 * math.cos(a), r * 0.55 * math.sin(a), r * 0.2, WHITE, 4)
        g.circle(0, 0, r * 0.12, GREY, 4)


def deepfake(g, x, y, sc=1.0, t=0.0, glitch=1.0):
    """จอมือถือหน้าคนครึ่งจริงครึ่งปลอม (สัญลักษณ์ Deepfake)"""
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -150, -280, 300, 560, 40)
        _shade(c, hexc("#1d1d21"), 7, 0.1)
        _rr(c, -130, -250, 260, 500, 26)
        _shade(c, hexc("#dfe8f0"), 3, 0)
        g.circle(0, -40, 90, hexc("#f0c8a0"), 5)
        c.save()
        c.rectangle(0, -140, 100, 200)
        c.clip()
        g.circle(0, -40, 90, hexc("#b8d8a8"), 5)
        for i in range(5):
            yy = -120 + ((i * 47 + int(t * 12) * 31) % 160)
            c.rectangle(0, yy, 100, 8)
            c.set_source_rgba(0.3, 0.9, 1, 0.6 * glitch)
            c.fill()
        c.restore()
        for sx in (-1, 1):
            g.circle(sx * 30, -55, 10, INK, 0)
        g.arc(0, -20, 36, 20, 160, 6, INK)
        g.text("AI?", 0, 160, 60, "kanit", RED)


def traffic(g, y, t=0.0, n=6, sc=0.8, jam=1.0):
    cols = [hexc("#3f6496"), hexc("#c8553d"), hexc("#3c8d4f"), hexc("#e3a92b"), hexc("#5a5d63"), hexc("#8a5a6a")]
    for i in range(n):
        x = 120 + i * 170 + (1 - jam) * ((t * 200) % 170)
        with g.at(x, y + 3 * math.sin(t * 20 + i), sc):
            g.rrect(-90, -70, 180, 50, 16, cols[i % 6], 6)
            g.rrect(-50, -110, 100, 46, 16, cols[i % 6], 6)
            g.rrect(-36, -102, 72, 30, 8, hexc("#cfe6f5"), 4)
            g.rrect(-40, -140, 80, 30, 6, hexc("#a8865a"), 4)   # ข้าวของบนหลังคา
            for k in (-55, 55):
                g.circle(k, -18, 20, INK, 0)
    if jam > 0.5:
        for i in range(3):
            g.label("ปี๊น!", 220 + i * 320, y - 200 + 10 * math.sin(t * 8 + i), 44, color=RED,
                    sc=0.6 + 0.4 * abs(math.sin(t * 4 + i)))
