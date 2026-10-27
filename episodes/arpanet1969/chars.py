"""ตัวละครและพร็อพ: ข้อความแรกบน ARPANET "LO" (29 ต.ค. 1969)"""
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


_gt = _load("gates1955")
_st = _load("saturday1973")
_kp = _load("katyperry1984")
_sk = _load("salk1914")
mainframe, teletype, window_screen = _gt.mainframe, _gt.teletype, _gt.window_screen
desk_phone = _st.phone
smartphone = _kp.phone
globe = _sk.globe

TERM_GREEN = (0.4, 1, 0.5, 1)
UCLA_BLUE = hexc("#2b6fb8")
SRI_RED = hexc("#a8233a")

# ชาร์ลี ไคลน์ นักศึกษา UCLA ปี 1969: ผมดำสั้นหวีข้าง แว่นกรอบหนา เชิ้ตแขนยาวไม่ผูกเนกไท
KLINE = Look(hair="part", hair_col=hexc("#2b2622"), outfit="vest", suit=hexc("#e8e0cc"), shirt=hexc("#e8e0cc"),
             tie=hexc("#e8e0cc"), pants=hexc("#3a3f48"), w=56, jaw=0.4, age=0.05, glasses="thick")
# วิศวกรฝั่ง SRI
DUVALL = Look(hair="short", hair_col=hexc("#8a6a42"), outfit="vest", suit=hexc("#9ab0c8"), shirt=hexc("#9ab0c8"),
              tie=hexc("#9ab0c8"), pants=hexc("#3a3a40"), w=57, age=0.1, glasses="thin")
USERS = [
    Look(hair="short", hair_col=hexc("#2b2622"), outfit="hoodie", suit=hexc("#3f6496"), pants=hexc("#3a3a40"), w=55),
    Look(hair="bun", hair_col=hexc("#8a5a2a"), outfit="tee", suit=hexc("#d76b5a"), pants=hexc("#3a4a6a"), w=54,
         height=0.93),
    Look(hair="buzz", hair_col=hexc("#1b1714"), outfit="flannel", suit=hexc("#5a8a5a"), pants=hexc("#3a3a40"),
         skin=hexc("#7a4a2c"), w=55),
]


def terminal(g, x, y, sc=1.0, text="", t=0.0, crash=0.0, cursor=True):
    """จอเทอร์มินัลเขียวยุค 60 + ข้อความ"""
    c = g.c
    jx = 8 * math.sin(t * 50) * crash
    with g.at(x + jx, y, sc):
        _rr(c, -260, -220, 520, 400, 30)
        _shade(c, hexc("#c9c2b2"), 7, 0.25)
        _rr(c, -220, -180, 440, 300, 20)
        _shade(c, hexc("#0e1a10"), 4, 0)
        if crash > 0.5:
            for i in range(14):
                yy = -170 + (i * 37 + int(t * 30) * 13) % 280
                c.rectangle(-210, yy, 420, 6 + (i % 3) * 4)
                c.set_source_rgba(0.4, 1, 0.5, 0.25 + 0.3 * ((i * 7) % 3) / 3)
                c.fill()
            g.text("SYSTEM CRASH", 0, -20, 50, "kanit", (1, 0.35, 0.3, 1))
        else:
            g.text(text if text else "", 0, -40, 110, "kanit", TERM_GREEN)
            if cursor and math.sin(t * 6) > 0:
                c.rectangle(-30 + 35 * len(text), 20, 40, 10)
                c.set_source_rgba(*TERM_GREEN)
                c.fill()
        _rr(c, -280, 190, 560, 70, 10)
        _shade(c, hexc("#b8b0a0"), 5, 0.2)
        for i in range(12):
            g.circle(-240 + i * 44, 225, 12, hexc("#3a3f48"), 2)


def key_cap(g, x, y, sc, ch, press=0.0, col=WHITE):
    with g.at(x, y + 12 * press, sc):
        g.rrect(-70, -70, 140, 140, 20, hexc("#3a3f48"), 6)
        g.rrect(-58, -64, 116, 110, 16, col, 4)
        g.text(ch, 0, -10, 70, "kanit", INK)


def cal_map(g, x, y, sc=1.0, k=1.0, t=0.0, crash=0.0):
    """แผนที่แคลิฟอร์เนีย: UCLA (ลอสแอนเจลิส) → SRI (สแตนฟอร์ด) เส้นเชื่อม"""
    c = g.c
    with g.at(x, y, sc):
        _rr(c, -320, -420, 640, 840, 30)
        _shade(c, hexc("#bcd8ec"), 6, 0.05)
        c.save()
        _rr(c, -320, -420, 640, 840, 30)
        c.clip()
        _smooth_path(c, [(-200, -420), (-160, -250), (-120, -50), (-30, 150), (80, 300), (180, 420), (330, 420),
                         (330, -420)])
        _shade(c, hexc("#e9dfc8"), 5, 0.1)
        c.restore()
        a = (-110, -220)
        b = (90, 260)
        g.circle(*a, 22, SRI_RED, 5)
        g.circle(*b, 22, UCLA_BLUE, 5)
        g.label("SRI", a[0] + 100, a[1], 50, color=SRI_RED)
        g.label("UCLA", b[0] + 120, b[1], 50, color=UCLA_BLUE)
        n = 24
        for i in range(n):
            u0, u1 = i / n, (i + 0.5) / n
            if u1 > k:
                break
            p0 = (b[0] + (a[0] - b[0]) * u0, b[1] + (a[1] - b[1]) * u0)
            p1 = (b[0] + (a[0] - b[0]) * u1, b[1] + (a[1] - b[1]) * u1)
            g.line([p0, p1], 8, RED if crash > 0.5 else GOLD, amp=0)
        if 0 < k < 1 and crash < 0.5:
            px, py = b[0] + (a[0] - b[0]) * k, b[1] + (a[1] - b[1]) * k
            g.circle(px, py, 18, GOLD2, 4)
        if crash > 0.5:
            mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
            g.star(mx, my, 60, (1, 0.4, 0.3, 1), 5, pts=8, inner=0.45)
        g.label("500+ กม.", -40, 40, 44, color=INK)


def bug(g, x, y, sc=1.0, t=0.0):
    c = g.c
    with g.at(x, y, sc, 8 * math.sin(t * 6)):
        for sx in (-1, 1):
            for i in range(3):
                _stroke(c, [(sx * 30, -20 + i * 25), (sx * 70, -30 + i * 30 + 6 * math.sin(t * 12 + i))], 5, INK)
        g.blob(0, 0, 40, 55, hexc("#3c8d4f"), 5, seed=2)
        g.circle(0, -60, 26, hexc("#2b6a3a"), 5)
        for sx in (-1, 1):
            g.circle(sx * 10, -66, 6, WHITE, 0)
            _stroke(c, [(sx * 10, -82), (sx * 26, -110)], 4, INK)


def sparks(g, x, y, t, k=1.0):
    for i in range(8):
        u = (t * 2 + i / 8) % 1
        a = i * 0.785
        r = 40 + 120 * u
        g.star(x + r * math.cos(a), y + r * math.sin(a), 18 * (1 - u) + 2, (1, 0.8, 0.3, (1 - u) * k), 0, pts=5)


def web(g, x, y, r, t=0.0, k=1.0):
    """ใยแมงมุมโลก: โหนดบนลูกโลกเชื่อมกัน"""
    globe(g, x, y, r, t)
    pts = []
    for i in range(10):
        a = i * 0.628 + t * 0.15
        pts.append((x + r * 0.85 * math.cos(a), y + r * 0.55 * math.sin(a * 1.3)))
    n = int(len(pts) * k)
    for i in range(n):
        for j in (i + 3, i + 5):
            if j < n:
                g.line([pts[i], pts[j]], 4, (*GOLD2[:3], 0.9), amp=0)
    for p in pts[:n]:
        g.circle(*p, 10, GOLD, 3)


def lo_sign(g, x, y, sc=1.0, t=0.0, glow=1.0):
    if glow > 0:
        g.sunburst(x, y, 170 * sc, 300 * sc, 18, t * 8, 10, (1, 0.85, 0.4, 0.6 * glow))
    with g.at(x, y, sc):
        g.rrect(-220, -130, 440, 260, 30, hexc("#0e1a10"), 8)
        g.text("LO", 0, -6, 180, "kanit", TERM_GREEN)
