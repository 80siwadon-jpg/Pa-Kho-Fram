"""ไลบรารีวาดการ์ตูนลายเส้นหมึก (Cairo) + ตัวหนังสือไทย (PIL/raqm)"""
import math
import os
import re
from contextlib import contextmanager

import cairo
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = {
    "kanitsb": os.path.join(ROOT, "assets/fonts/Kanit-SemiBold.ttf"),
    "kanitm": os.path.join(ROOT, "assets/fonts/Kanit-Medium.ttf"),
    "kanit": os.path.join(ROOT, "assets/fonts/Kanit-Bold.ttf"),
    "kanitr": os.path.join(ROOT, "assets/fonts/Kanit-Regular.ttf"),
}


def hexc(h, a=1.0):
    h = h.lstrip("#")
    return (int(h[0:2], 16) / 255, int(h[2:4], 16) / 255, int(h[4:6], 16) / 255, a)


# พาเลตต์: หมึกดำ + สีพาสเทลหม่น ๆ
PAPER = hexc("#ffffff")
INK = hexc("#1b1916")
WHITE = hexc("#ffffff")
RED = hexc("#c8553d")
BLUE = hexc("#3f6496")
NAVY = hexc("#2b3f63")
GOLD = hexc("#e3a92b")
GOLD2 = hexc("#f4d27a")
SKIN = hexc("#f6d5b5")
BLUSH = hexc("#ef9a8a", 0.75)
BROWN = hexc("#9b6a3e")
BROWN2 = hexc("#d8b48a")
GREY = hexc("#8d8a84")
LGREY = hexc("#d9d5cc")
GREEN = hexc("#5f7f55")
MINT = hexc("#cfe3d7")
PURPLE = hexc("#8a6a9a")
MUSTARD = hexc("#d9a441")
ICE = hexc("#cfe0ea")
COAT = hexc("#33343d")
TUNIC = hexc("#3e5a47")
SKYBLUE = hexc("#8fb8de")
HAIR = hexc("#6b4a33")
LYGREEN = hexc("#3c8d4f")
SAND = hexc("#f3e2bf")
SAND2 = hexc("#e2c48e")
TAN = hexc("#e6b48a")
KHAKI = hexc("#b9a06a")
CREAM = hexc("#f2ecdc")


# ---------------------------------------------------------------- easing
def clamp(x, a=0.0, b=1.0):
    return a if x < a else b if x > b else x


def seg(t, a, b):
    if b <= a:
        return 1.0 if t >= b else 0.0
    return clamp((t - a) / (b - a))


def e_out(x):
    return 1 - (1 - x) ** 3


def e_in(x):
    return x ** 3


def e_io(x):
    return 4 * x ** 3 if x < 0.5 else 1 - (-2 * x + 2) ** 3 / 2


def e_back(x, s=1.9):
    x -= 1
    return 1 + x * x * ((s + 1) * x + s)


def spring(t, f=2.6, d=5.5):
    if t <= 0:
        return 0.0
    return 1 - math.exp(-d * t) * math.cos(2 * math.pi * f * t)


def pop(t, t0, dur=0.38):
    """สเกล 0 -> 1 แบบเด้ง"""
    if t < t0:
        return 0.0
    return max(e_back(seg(t, t0, t0 + dur)), 0.0)


def lerp(a, b, x):
    return a + (b - a) * x


def hn(*a):
    """hash noise -> [-1, 1]"""
    v = 0.0
    for i, x in enumerate(a):
        v += x * (12.9898, 78.233, 37.719, 4.581, 93.989)[i % 5]
    v = math.sin(v) * 43758.5453
    return (v - math.floor(v)) * 2 - 1


# ---------------------------------------------------------------- text sprites
_FONT_CACHE = {}
_SPRITES = {}


def font(name, size):
    k = (name, size)
    if k not in _FONT_CACHE:
        _FONT_CACHE[k] = ImageFont.truetype(FONTS[name], size, layout_engine=ImageFont.Layout.RAQM)
    return _FONT_CACHE[k]


def _to_surface(img):
    a = np.asarray(img.convert("RGBA")).astype(np.float32)
    al = a[..., 3:4] / 255.0
    pm = a[..., :3] * al
    bgra = np.dstack([pm[..., 2], pm[..., 1], pm[..., 0], a[..., 3]]).astype(np.uint8)
    bgra = np.ascontiguousarray(bgra)
    h, w = bgra.shape[:2]
    surf = cairo.ImageSurface.create_for_data(memoryview(bgra), cairo.FORMAT_ARGB32, w, h, w * 4)
    return surf, bgra


def text_sprite(s, size, fnt="kanitsb", color=INK, stroke=0, stroke_color=PAPER, maxw=None, spacing=8):
    key = (s, size, fnt, color, stroke, stroke_color, maxw)
    if key in _SPRITES:
        return _SPRITES[key]
    f = font(fnt, size)
    lines = wrap(s, f, maxw) if maxw else [s]
    tmp = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
    boxes = [tmp.textbbox((0, 0), ln, font=f, stroke_width=stroke) for ln in lines]
    asc, desc = f.getmetrics()
    lh = asc + desc + spacing
    wmax = max(b[2] - b[0] for b in boxes) + 2 * stroke + 20
    hh = lh * len(lines) + 2 * stroke + 30
    img = Image.new("RGBA", (int(wmax), int(hh)), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    c255 = tuple(int(v * 255) for v in color[:3])
    s255 = tuple(int(v * 255) for v in stroke_color[:3])
    for i, ln in enumerate(lines):
        b = boxes[i]
        x = (wmax - (b[2] - b[0])) / 2 - b[0]
        d.text((x, stroke + 10 + i * lh), ln, font=f, fill=c255,
               stroke_width=stroke, stroke_fill=s255)
    bb = img.getbbox() or (0, 0, 1, 1)
    img = img.crop((0, bb[1] - 2 if bb[1] >= 2 else 0, img.width, min(bb[3] + 2, img.height)))
    surf, arr = _to_surface(img)
    _SPRITES[key] = (surf, arr, img.width, img.height)
    return _SPRITES[key]


def _thai_words(s):
    """ตัดคำไทยด้วย pythainlp (ถ้ามี) ไม่งั้นตัดที่ช่องว่างอย่างเดียว"""
    try:
        from pythainlp.tokenize import word_tokenize
        return word_tokenize(s, engine="newmm", keep_whitespace=True)
    except ImportError:
        return re.split("( |\u200b)", s)


def wrap(s, f, maxw):
    """ตัดซับเป็นไม่เกิน 2 บรรทัดที่ยาวใกล้กัน: ตัดได้ทุกขอบคำ (ตัดคำไทยอัตโนมัติ)
    แต่ชอบตัดตรงช่องว่าง / \u200b (จุดตัดที่ผู้เขียนบทใส่ไว้) มากกว่า"""
    tmp = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
    if tmp.textlength(s, font=f) <= maxw:
        return [s]
    toks = [t for t in _thai_words(s) if t != ""]
    best, best_score = [s], 1e9
    for i in range(1, len(toks)):
        a, b = "".join(toks[:i]), "".join(toks[i:])
        explicit = a.endswith((" ", "\u200b")) or b.startswith((" ", "\u200b"))
        a, b = a.rstrip(" \u200b"), b.lstrip(" \u200b")
        if not a or not b or b[0] in "?!.,ๆ…":
            continue
        if (b[0] == '"' and b.count('"') % 2) or (a[-1] == '"' and a.count('"') % 2):   # อย่าแยกเครื่องหมายคำพูดจากคำ
            continue
        score = max(tmp.textlength(a, font=f), tmp.textlength(b, font=f)) - (110 if explicit else 0)
        if a[-1].isdigit():   # อย่าแยกตัวเลขออกจากคำที่ตามมา เช่น "20 ตุลาคม"
            score += 150
        if min(tmp.textlength(a, font=f), tmp.textlength(b, font=f)) < 0.3 * maxw:   # กันคำสั้นค้างบรรทัด
            score += 160
        if score < best_score:
            best, best_score = [a, b], score
    return best


# ---------------------------------------------------------------- drawer
class Draw:
    def __init__(self, ctx, t, frame):
        self.c = ctx
        self.t = t
        self.frame = frame
        self.boil = 0   # ลายเส้นนิ่ง (ไม่สั่นแบบวาดมือ)

    # ---- state helpers
    @contextmanager
    def at(self, x=0, y=0, sc=1.0, rot=0.0, sx=None, sy=None):
        c = self.c
        c.save()
        c.translate(x, y)
        if rot:
            c.rotate(math.radians(rot))
        kx = sx if sx is not None else sc
        ky = sy if sy is not None else sc
        c.scale(kx if abs(kx) > 1e-4 else 1e-4, ky if abs(ky) > 1e-4 else 1e-4)
        try:
            yield
        finally:
            c.restore()

    @contextmanager
    def silhouette(self, col=INK, a=1.0):
        """วาดสิ่งที่อยู่ข้างในเป็นเงาสีเดียว"""
        self.c.push_group()
        try:
            yield
        finally:
            pat = self.c.pop_group()
            self.c.set_source_rgba(col[0], col[1], col[2], a)
            self.c.mask(pat)

    @contextmanager
    def alpha(self, a):
        if a >= 0.999:
            yield
            return
        self.c.push_group()
        try:
            yield
        finally:
            self.c.pop_group_to_source()
            self.c.paint_with_alpha(max(a, 0.0))

    def fs(self, fill, lw=7, stroke=INK):
        c = self.c
        if fill is not None:
            c.set_source_rgba(*fill)
            if lw:
                c.fill_preserve()
            else:
                c.fill()
        if lw:
            c.set_source_rgba(*stroke)
            c.set_line_width(lw)
            c.set_line_join(cairo.LINE_JOIN_ROUND)
            c.set_line_cap(cairo.LINE_CAP_ROUND)
            c.stroke()
        elif fill is None:
            c.new_path()

    # ---- primitives
    def smooth(self, pts, closed=True):
        c = self.c
        n = len(pts)
        c.move_to(*pts[0])
        rng = range(n) if closed else range(n - 1)
        for i in rng:
            p0 = pts[i - 1] if (closed or i > 0) else pts[0]
            p1 = pts[i]
            p2 = pts[(i + 1) % n]
            p3 = pts[(i + 2) % n] if (closed or i + 2 < n) else pts[-1]
            c.curve_to(p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6,
                       p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6, p2[0], p2[1])
        if closed:
            c.close_path()

    def blob(self, x, y, rx, ry, fill, lw=7, seed=1, amp=0.025, n=22, stroke=INK):
        pts = []
        for i in range(n):
            a = 2 * math.pi * i / n
            k = 1 + amp * hn(i, seed, self.boil)
            pts.append((x + math.cos(a) * rx * k, y + math.sin(a) * ry * k))
        self.smooth(pts)
        self.fs(fill, lw, stroke)

    def poly(self, pts, fill, lw=7, seed=1, amp=1.6, closed=True, smooth=False, stroke=INK):
        q = [(p[0] + amp * hn(i, seed, self.boil), p[1] + amp * hn(i, seed + 7, self.boil))
             for i, p in enumerate(pts)]
        if smooth:
            self.smooth(q, closed)
        else:
            self.c.move_to(*q[0])
            for p in q[1:]:
                self.c.line_to(*p)
            if closed:
                self.c.close_path()
        self.fs(fill if closed else None, lw, stroke)

    def line(self, pts, lw=7, col=INK, seed=3, amp=1.2, smooth=False):
        self.poly(pts, None, lw, seed, amp, closed=False, smooth=smooth, stroke=col)

    def circle(self, x, y, r, fill, lw=7, stroke=INK):
        self.c.arc(x, y, r, 0, 2 * math.pi)
        self.fs(fill, lw, stroke)

    def rrect(self, x, y, w, h, r, fill, lw=7, stroke=INK, seed=5):
        c = self.c
        j = lambda i: 1.3 * hn(i, seed, self.boil)  # noqa: E731
        r = min(r, w / 2, h / 2)
        c.new_sub_path()
        c.arc(x + w - r + j(1), y + r + j(2), r, -math.pi / 2, 0)
        c.arc(x + w - r + j(3), y + h - r + j(4), r, 0, math.pi / 2)
        c.arc(x + r + j(5), y + h - r + j(6), r, math.pi / 2, math.pi)
        c.arc(x + r + j(7), y + r + j(8), r, math.pi, 1.5 * math.pi)
        c.close_path()
        self.fs(fill, lw, stroke)

    def arc(self, x, y, r, a0, a1, lw=7, col=INK):
        self.c.new_path()
        self.c.arc(x, y, r, math.radians(a0), math.radians(a1))
        self.fs(None, lw, col)

    def star(self, x, y, r, fill, lw=6, pts=5, inner=0.48, rot=-90, stroke=INK):
        q = []
        for i in range(pts * 2):
            rr = r if i % 2 == 0 else r * inner
            a = math.radians(rot + 180 * i / pts)
            q.append((x + math.cos(a) * rr, y + math.sin(a) * rr))
        self.poly(q, fill, lw, seed=int(x) % 17, amp=0.8, stroke=stroke)

    def sparkle(self, x, y, r, fill=GOLD2, lw=5):
        q = []
        for i in range(8):
            rr = r if i % 2 == 0 else r * 0.28
            a = math.radians(-90 + 45 * i)
            q.append((x + math.cos(a) * rr, y + math.sin(a) * rr))
        self.poly(q, fill, lw, amp=0.5)

    def text(self, s, x, y, size, fnt="kanitsb", color=INK, sc=1.0, rot=0.0, a=1.0,
             stroke=0, stroke_color=PAPER, maxw=None, anchor="c"):
        if sc <= 0.001 or a <= 0.001:
            return 0, 0
        surf, _, w, h = text_sprite(s, size, fnt, color, stroke, stroke_color, maxw)
        c = self.c
        c.save()
        c.translate(x, y)
        if rot:
            c.rotate(math.radians(rot))
        c.scale(sc, sc)
        ox = {"c": -w / 2, "l": 0, "r": -w}[anchor]
        c.set_source_surface(surf, ox, -h / 2)
        c.get_source().set_filter(cairo.FILTER_GOOD)
        c.paint_with_alpha(a)
        c.restore()
        return w * sc, h * sc

    # ขอบปลอดภัยของตัวหนังสือในพิกัดฉาก (ก่อนกล้อง): กล้องซูม 1.12 + แพน ±60 + ปุ่มด้านขวาของแอป
    SAFE_X0, SAFE_X1 = 100, 960

    def _fit(self, s, x, y, size, fnt, sc, stroke, maxw, anchor):
        """ย่อตัวหนังสือที่ยาวเกินขอบปลอดภัย (คิดในพิกัดฉาก ไม่ขึ้นกับการขยับกล้อง)"""
        m = getattr(self, "scene_m", None)
        if m is None or sc <= 0.001:
            return sc
        _, _, w, _ = text_sprite(s, size, fnt, INK, stroke, WHITE, maxw)
        ox = {"c": -w / 2, "l": 0, "r": -w}[anchor]
        c = self.c
        inv = cairo.Matrix(*m)
        inv.invert()
        xs = []
        for lx in (ox, ox + w):
            dx, dy = c.user_to_device(x + lx * sc, y)
            xs.append(inv.transform_point(dx, dy)[0])
        cx, _ = inv.transform_point(*c.user_to_device(x, y))
        f = 1.0
        lo, hi = min(xs), max(xs)
        if lo < self.SAFE_X0 and cx - lo > 1:
            f = min(f, max(0.3, (cx - self.SAFE_X0) / (cx - lo)))
        if hi > self.SAFE_X1 and hi - cx > 1:
            f = min(f, max(0.3, (self.SAFE_X1 - cx) / (hi - cx)))
        return sc * f

    def label(self, s, x, y, size, fnt="kanit", color=INK, sc=1.0, rot=0.0, a=1.0, maxw=None, anchor="c"):
        """ตัวหนังสือบนภาพ: มีขอบขาวรอบตัวอักษร อ่านง่ายแม้ทับภาพ (ซับด้านล่างไม่ใช้ขอบ)
        ย่ออัตโนมัติถ้ายาวเกินขอบปลอดภัยของจอ"""
        stroke = max(6, int(size * 0.14))
        sc = self._fit(s, x, y, size, fnt, sc, stroke, maxw, anchor)
        return self.text(s, x, y, size, fnt, color, sc, rot, a, stroke=stroke,
                         stroke_color=WHITE, maxw=maxw, anchor=anchor)

    # ---- faces & characters (origin = กลางหัว สำหรับ face, ปลายเท้า สำหรับตัวละคร)
    def face(self, R, mood="happy", look=(0, 0), seed=0, mouth_dy=0.0):
        t = self.t
        ex, ey, er = R * 0.36, -R * 0.02, R * 0.11
        lx, ly = look[0] * R * 0.06, look[1] * R * 0.06
        blink = mood == "happy" and ((t * 0.55 + seed * 0.37) % 3.1) < 0.09
        lw = max(R * 0.07, 3)
        if mood in ("happy", "worry", "sad", "flat", "think"):
            for sx in (-1, 1):
                if blink:
                    self.line([(sx * ex - er, ey), (sx * ex + er, ey)], lw)
                else:
                    self.circle(sx * ex + lx, ey + ly, er, INK, 0)
                    self.circle(sx * ex + lx - er * 0.35, ey + ly - er * 0.4, er * 0.32, WHITE, 0)
        if mood in ("sleep", "laugh"):
            for sx in (-1, 1):
                if mood == "sleep":
                    self.arc(sx * ex, ey - er * 0.6, er * 1.2, 20, 160, lw)
                else:
                    self.arc(sx * ex, ey + er * 0.8, er * 1.2, 200, 340, lw)
        if mood == "shock":
            for sx in (-1, 1):
                self.circle(sx * ex, ey - R * 0.05, er * 2.0, WHITE, lw)
                self.circle(sx * ex + lx, ey - R * 0.05 + ly, er * 0.6, INK, 0)
        if mood == "dizzy":
            for sx in (-1, 1):
                pts = []
                for i in range(30):
                    a = i * 0.55 + t * 8 * sx
                    rr = er * 1.8 * i / 30
                    pts.append((sx * ex + math.cos(a) * rr, ey + math.sin(a) * rr))
                self.line(pts, lw * 0.7, amp=0)
        if mood == "smug":
            self.arc(-ex, ey + er * 0.8, er * 1.2, 200, 340, lw)
            self.circle(ex, ey, er, INK, 0)
        # brows
        if mood in ("worry", "sad"):
            for sx in (-1, 1):
                self.line([(sx * ex - er * 1.5 * sx, ey - R * 0.30), (sx * ex + er * 1.3 * sx, ey - R * 0.20)], lw)
        # blush
        for sx in (-1, 1):
            self.c.save()
            self.c.translate(sx * R * 0.58, R * 0.22)
            self.c.scale(1, 0.6)
            self.circle(0, 0, R * 0.14, BLUSH, 0)
            self.c.restore()
        # mouth
        my = R * 0.30 + mouth_dy
        if mood in ("happy", "smug"):
            self.arc(0, my - R * 0.1, R * 0.16, 25, 155, lw)
        elif mood == "think":
            self.line([(R * 0.0, my), (R * 0.18, my - R * 0.03)], lw)
        elif mood == "sleep":
            self.circle(0, my + R * 0.02, R * 0.06, INK, 0)
        elif mood == "shock":
            self.c.save()
            self.c.translate(0, my + R * 0.08)
            self.c.scale(1, 1.3)
            self.circle(0, 0, R * 0.12, INK, 0)
            self.c.restore()
        elif mood == "laugh":
            self.c.move_to(-R * 0.25, my - R * 0.05)
            self.c.line_to(R * 0.25, my - R * 0.05)
            self.c.curve_to(R * 0.25, my + R * 0.35, -R * 0.25, my + R * 0.35, -R * 0.25, my - R * 0.05)
            self.c.close_path()
            self.fs(INK, lw)
            self.c.save()
            self.c.translate(0, my + R * 0.16)
            self.c.scale(1, 0.55)
            self.circle(0, 0, R * 0.12, RED, 0)
            self.c.restore()
        elif mood in ("worry", "sad", "dizzy"):
            pts = [(-R * 0.2 + R * 0.4 * i / 8, my + R * 0.04 * math.sin(i * 1.6)) for i in range(9)]
            self.line(pts, lw, amp=0)
        elif mood == "flat":
            self.line([(-R * 0.15, my), (R * 0.15, my)], lw)

    def sweat(self, x, y, s=1.0):
        with self.at(x, y, s):
            self.c.move_to(0, -22)
            self.c.curve_to(10, -4, 14, 8, 0, 12)
            self.c.curve_to(-14, 8, -10, -4, 0, -22)
            self.fs(ICE, 4)

    def kid(self, x, y, sc=1.0, mood="happy", rot=0, hat=None, arms="down", seed=11):
        with self.at(x, y, sc, rot):
            self.blob(-26, -8, 22, 12, INK, 0, seed)
            self.blob(26, -8, 22, 12, INK, 0, seed + 1)
            ay = -95
            if arms == "up":
                self.line([(-45, ay), (-90, ay - 70)], 12)
                self.line([(45, ay), (90, ay - 70)], 12)
            elif arms == "chin":
                self.line([(45, ay), (70, ay - 50), (35, -175)], 12)
                self.line([(-45, ay), (-70, ay + 30)], 12)
            else:
                self.line([(-45, ay), (-75, ay + 45)], 12)
                self.line([(45, ay), (75, ay + 45)], 12)
            self.blob(0, -70, 58, 66, MUSTARD, 7, seed + 2)
            self.blob(0, -195, 86, 80, SKIN, 7, seed + 3)
            self.line([(-20, -272), (-6, -300), (4, -270), (20, -295), (24, -268)], 7, smooth=True)
            with self.at(0, -190):
                self.face(80, mood, seed=seed)
            if hat == "miner":
                self.c.move_to(-95, -240)
                self.c.curve_to(-80, -330, 80, -330, 95, -240)
                self.c.close_path()
                self.fs(BROWN2, 7)
                self.rrect(-120, -250, 240, 22, 10, BROWN, 6)
            if hat == "party":
                self.poly([(-35, -262), (35, -262), (5, -365)], RED, 6)
                self.circle(5, -368, 12, GOLD, 5)

    def bear(self, x, y, sc=1.0, mood="happy", rot=0, hat=True, pockets=0.0, seed=21):
        with self.at(x, y, sc, rot):
            self.blob(-40, -10, 36, 18, BROWN, 7, seed)
            self.blob(40, -10, 36, 18, BROWN, 7, seed + 1)
            self.blob(-88, -110, 26, 50, BROWN, 7, seed + 2)
            self.blob(88, -110, 26, 50, BROWN, 7, seed + 3)
            self.blob(0, -100, 95, 102, BROWN, 7, seed + 4)
            self.blob(0, -85, 58, 62, BROWN2, 0, seed + 5)
            if pockets > 0:
                for sx in (-1, 1):
                    with self.at(sx * 98, -60, pockets):
                        self.blob(sx * 18, 0, 26, 32, WHITE, 6, seed + 6 + sx)
            for sx in (-1, 1):
                self.circle(sx * 62, -310, 28, BROWN, 7)
                self.circle(sx * 62, -310, 13, BROWN2, 0)
            self.blob(0, -245, 88, 80, BROWN, 7, seed + 8)
            self.blob(0, -215, 40, 28, BROWN2, 5, seed + 9)
            self.blob(0, -228, 13, 9, INK, 0, seed + 10)
            with self.at(0, -255):
                self.face(70, mood, seed=seed)
            if hat:
                self.c.move_to(-82, -280)
                self.c.curve_to(-80, -370, 80, -370, 82, -280)
                self.c.close_path()
                self.fs(GREY, 7)
                self.rrect(-90, -300, 180, 34, 14, LGREY, 6)
                for sx in (-1, 1):
                    self.blob(sx * 88, -250, 20, 42, LGREY, 6, seed + 11 + sx)
                self.star(0, -335, 15, RED, 4)

    def sam(self, x, y, sc=1.0, mood="happy", rot=0, seed=31, arm=0.0):
        with self.at(x, y, sc, rot):
            self.blob(-30, -8, 30, 14, INK, 0, seed)
            self.blob(30, -8, 30, 14, INK, 0, seed + 1)
            self.line([(-62, -150), (-80 - 20 * arm, -80 - 90 * arm)], 13)
            self.line([(62, -150), (85, -80)], 13)
            self.blob(0, -95, 75, 98, BLUE, 7, seed + 2)
            self.poly([(-18, -185), (18, -185), (0, -120)], WHITE, 5)
            self.blob(0, -235, 72, 70, SKIN, 7, seed + 3)
            self.poly([(-28, -195), (28, -195), (0, -150)], WHITE, 6)
            with self.at(0, -240):
                self.face(62, mood, seed=seed)
            self.rrect(-95, -305, 190, 22, 10, WHITE, 6)
            self.rrect(-55, -420, 110, 120, 8, WHITE, 6)
            self.rrect(-55, -335, 110, 26, 0, BLUE, 5)
            self.star(0, -322, 13, WHITE, 3)
            for i in range(3):
                self.line([(-38 + i * 38, -412), (-38 + i * 38, -340)], 9, RED, amp=0.6)

    def seward(self, x, y, sc=1.0, mood="happy", rot=0, seed=41, arm=0.0):
        """วิลเลียม เอช. ซิวเวิร์ด: จมูกโด่งงุ้มใหญ่ ผมขาวฟูกระเซิง คิ้วดก คอเสื้อขาวตั้ง โบว์ดำ เสื้อโค้ตยาวสีเข้ม"""
        with self.at(x, y, sc, rot):
            for sx in (-1, 1):   # ขา + รองเท้า
                self.rrect(sx * 22 - 13, -70, 26, 70, 8, COAT, 6)
                self.blob(sx * 26, -6, 26, 12, INK, 0, seed + sx)
            self.line([(68, -175), (95 + 25 * arm, -110 - 120 * arm)], 15)        # แขน
            self.line([(-68, -175), (-92, -105)], 15)
            self.poly([(-78, -195), (78, -195), (92, -55), (40, -40), (0, -70), (-40, -40), (-92, -55)],
                      COAT, 7, seed=seed, smooth=True)                              # โค้ตหางยาว
            self.poly([(-30, -200), (30, -200), (14, -100), (-14, -100)], WHITE, 5, seed=seed + 1)
            for sx in (-1, 1):   # ผมขาวฟูข้างหู
                self.poly([(sx * 58, -330), (sx * 98, -322), (sx * 86, -300), (sx * 112, -286), (sx * 90, -268),
                           (sx * 104, -246), (sx * 72, -240)], WHITE, 6, seed=seed + 4 + sx, smooth=True)
            self.blob(0, -275, 76, 86, SKIN, 7, seed + 7)
            self.poly([(-50, -340), (-30, -372), (-6, -352), (10, -380), (26, -354), (52, -366), (56, -334)],
                      WHITE, 6, seed=seed + 8, smooth=True)                         # ปอยผมกระเซิงบนหัว
            self.poly([(-5, -268), (7, -268), (30, -240), (26, -226), (6, -226), (-4, -238)],
                      SKIN, 6, seed=seed + 11, smooth=True)                         # จมูกโด่งงุ้ม
            with self.at(0, -282):
                self.face(70, mood, seed=seed, mouth_dy=40)
            for sx in (-1, 1):   # ปกคอเสื้อขาวตั้งสูง
                self.poly([(sx * 4, -186), (sx * 46, -204), (sx * 40, -166)], WHITE, 5, seed=seed + 2 + sx)
            self.poly([(-40, -184), (0, -172), (40, -184), (40, -156), (0, -168), (-40, -156)], INK, 0)  # โบว์ใหญ่
            self.circle(0, -170, 9, INK, 0)
            for sx in (-1, 1):   # คิ้วดก
                self.poly([(sx * 10, -306), (sx * 42, -318), (sx * 50, -304), (sx * 14, -296)], LGREY, 4, seed=seed + 9 + sx)

    def tsar(self, x, y, sc=1.0, mood="happy", rot=0, seed=141, pockets=0.0, arm=0.0):
        """พระเจ้าซาร์อเล็กซานเดอร์ที่ 2: หนวดใหญ่ต่อจอนยาว ผมเถิก เครื่องแบบทหารเขียวเข้ม อินทรธนูทอง สายสะพายฟ้า"""
        with self.at(x, y, sc, rot):
            for sx in (-1, 1):
                self.rrect(sx * 24 - 15, -75, 30, 75, 8, NAVY, 6)
                self.line([(sx * 24, -70), (sx * 24, -8)], 4, RED, amp=0)
                self.blob(sx * 28, -6, 28, 13, INK, 0, seed + sx)
            if pockets > 0:
                for sx in (-1, 1):
                    with self.at(sx * 82, -80, pockets):
                        self.blob(sx * 14, 0, 24, 30, WHITE, 6, seed + 3 + sx)
            self.line([(74, -180), (98 + 20 * arm, -105 - 110 * arm)], 16, TUNIC)
            self.line([(-74, -180), (-98, -105)], 16, TUNIC)
            self.rrect(-80, -205, 160, 140, 34, TUNIC, 7, seed=seed)
            self.poly([(-70, -195), (-48, -200), (72, -92), (58, -76)], SKYBLUE, 0)   # สายสะพาย
            for i in range(4):
                self.circle(-6, -180 + i * 28, 6, GOLD, 3)
            self.star(-40, -150, 12, GOLD, 3)
            for sx in (-1, 1):   # อินทรธนูทองพร้อมพู่
                self.blob(sx * 76, -200, 32, 14, GOLD, 5, seed + 5 + sx)
                for k in range(4):
                    self.line([(sx * (58 + k * 11), -190), (sx * (58 + k * 11), -172)], 4, GOLD, amp=0)
            self.rrect(-34, -222, 68, 26, 8, RED, 5)                                   # คอตั้งแดง
            self.line([(-30, -200), (30, -200)], 4, GOLD, amp=0)
            self.blob(0, -290, 78, 84, SKIN, 7, seed + 7)
            self.c.move_to(-74, -300)                                                   # ผมเถิกหวีข้าง
            self.c.curve_to(-70, -380, 66, -380, 74, -300)
            self.c.curve_to(50, -350, -10, -362, -40, -322)
            self.c.curve_to(-55, -320, -68, -310, -74, -300)
            self.c.close_path()
            self.fs(HAIR, 6)
            with self.at(0, -290):
                self.face(70, mood, seed=seed)
            for sx in (-1, 1):   # จอนยาวลงมาต่อหนวด
                self.poly([(sx * 66, -318), (sx * 84, -282), (sx * 78, -236), (sx * 44, -238), (sx * 56, -280)],
                          HAIR, 5, seed=seed + 9 + sx, smooth=True)
            self.poly([(-66, -246), (-30, -262), (0, -254), (30, -262), (66, -246), (88, -262), (74, -230),
                       (30, -238), (0, -244), (-30, -238), (-74, -230), (-88, -262)],
                      HAIR, 5, seed=seed + 12, smooth=True)                             # หนวดใหญ่ปลายงอน
            self.blob(0, -268, 11, 9, SKIN, 4, seed + 13)

    def lion(self, x, y, sc=1.0, mood="think", rot=0, seed=51):
        with self.at(x, y, sc, rot):
            self.star(0, 0, 135, MUSTARD, 7, pts=14, inner=0.78)
            self.blob(0, 0, 88, 82, GOLD2, 7, seed)
            for sx in (-1, 1):
                self.circle(sx * 62, -64, 20, GOLD2, 6)
            with self.at(0, 0):
                self.face(78, mood, look=(1, 0), seed=seed)
                for sx in (-1, 1):  # ตาเจ้าเล่ห์ (เปลือกตาครึ่ง)
                    self.c.rectangle(sx * 28 - 16, -26, 32, 14)
                    self.fs(GOLD2, 0)
                    self.line([(sx * 28 - 16, -12), (sx * 28 + 16, -12)], 5)
            self.blob(0, 28, 20, 14, INK, 0, seed + 2)
            self.poly([(-40, -95), (-30, -135), (-12, -110), (0, -145), (12, -110), (30, -135), (40, -95)], GOLD, 5)

    def soldier(self, x, y, sc=1.0, coat=GREEN, seed=61, salute=0.0, rifle=True):
        with self.at(x, y, sc):
            self.line([(-14, -60), (-14, 0)], 10)
            self.line([(14, -60), (14, 0)], 10)
            self.rrect(-30, -125, 60, 75, 18, coat, 6, seed=seed)
            self.circle(0, -150, 28, SKIN, 6)
            with self.at(0, -150):
                self.face(26, "flat", seed=seed)
            self.rrect(-22, -215, 44, 45, 5, INK, 0, seed=seed + 1)
            if rifle:
                self.line([(42, -20), (42, -175)], 7, BROWN)
                self.poly([(38, -175), (46, -175), (42, -215)], LGREY, 4)
            if salute > 0:
                self.line([(-28, -110), (-40, -150), (-20 - 0 * salute, -175)], 8)

    def lady(self, x, y, sc=1.0, rot=0, mood="happy", seed=71):
        """สุภาพสตรียุค 1860: กระโปรงสุ่มบาน ผมแสกกลางเกล้ามวยต่ำ"""
        with self.at(x, y, sc, rot):
            self.c.move_to(-28, -150)
            self.c.curve_to(-70, -100, -120, -30, -115, 0)
            self.c.line_to(115, 0)
            self.c.curve_to(120, -30, 70, -100, 28, -150)
            self.c.close_path()
            self.fs(PURPLE, 7)
            for k in range(3):
                self.arc(0, -150 + 50 * (k + 1) - 600, 600, 84, 96, 4, LGREY)
            self.line([(-25, -140), (-60, -90)], 10)
            self.line([(25, -140), (60, -90)], 10)
            self.rrect(-30, -175, 60, 40, 14, PURPLE, 6)
            for sx in (-1, 1):
                self.blob(sx * 42, -232, 22, 30, HAIR, 5, seed + sx)
            self.circle(0, -205, 52, SKIN, 7)
            self.c.move_to(-52, -210)
            self.c.curve_to(-50, -270, 50, -270, 52, -210)
            self.c.curve_to(30, -250, 4, -252, 0, -238)
            self.c.curve_to(-4, -252, -30, -250, -52, -210)
            self.c.close_path()
            self.fs(HAIR, 5)
            with self.at(0, -200):
                self.face(48, mood, seed=seed)

    def name_tag(self, t, t0, x, y, name, role, dur=3.2, side=1):
        """ป้ายชื่อตัวละคร แสดงครั้งแรกที่ปรากฏตัว: เด้งขึ้น ค้างไว้ แล้วจางหาย"""
        if t < t0 or t > t0 + dur:
            return
        k = pop(t, t0, 0.35)
        a = min(1.0, (t0 + dur - t) / 0.35)
        import photos   # ภาพจริงของบุคคล (ถ้ามีใน photos.json "tag") ขึ้นเหนือป้ายชื่อ
        pid = photos.portrait(name)
        if pid:
            px = min(max(x, 230), 780)
            py = max(y - 330, 450)
            with self.alpha(a):
                photos.photo(self, pid, px, py, 300, 360, -4 * side, pop(t, t0 + 0.15, 0.4), 1.0 + 0.03 * (t - t0))
        _, _, w1, _ = text_sprite(name, 50, "kanit")
        _, _, w2, _ = text_sprite(role, 36, "kanitm", GREY)
        w = max(w1, w2) + 40
        x = min(max(x, self.SAFE_X0 + w / 2), self.SAFE_X1 - w / 2)   # ป้ายชื่อไม่ล้นขอบจอ
        with self.alpha(a):
            with self.at(x, y, k):
                self.rrect(-w / 2, -66, w, 132, 28, WHITE, 6)
                self.poly([(-side * 30, 64), (side * 10, 64), (-side * 50, 102)], WHITE, 0)
                self.line([(-side * 30, 67), (-side * 50, 102), (side * 10, 67)], 6)
                self.c.rectangle(-w / 2 + 3, -66 + 3, 9, 126)
                self.fs(RED, 0)
                self.text(name, 6, -22, 50, "kanit")
                self.text(role, 6, 34, 36, "kanitm", GREY)

    def person(self, x, y, sc=1.0, mood="laugh", hat="top", seed=81, mustache=True, col=GREY):
        with self.at(x, y, sc):
            self.blob(0, -60, 65, 70, col, 7, seed)
            self.blob(0, -170, 70, 66, SKIN, 7, seed + 1)
            with self.at(0, -175):
                self.face(62, mood, seed=seed)
            if mustache:
                self.blob(-14, -150, 16, 7, INK, 0, seed + 2)
                self.blob(14, -150, 16, 7, INK, 0, seed + 3)
            if hat == "top":
                self.rrect(-62, -238, 124, 16, 6, INK, 0)
                self.rrect(-40, -320, 80, 90, 5, INK, 0)
            elif hat == "bowler":
                self.c.move_to(-55, -228)
                self.c.curve_to(-50, -300, 50, -300, 55, -228)
                self.c.close_path()
                self.fs(INK, 0)
                self.rrect(-72, -236, 144, 14, 7, INK, 0)

    # ---- props
    def calendar(self, x, y, sc, day, dayname="ศุกร์", month="ต.ค. 1867", flip=None, seed=91):
        with self.at(x, y, sc):
            self.rrect(-150, -170, 300, 340, 22, WHITE, 8, seed=seed)
            self.rrect(-150, -170, 300, 80, 22, RED, 8, seed=seed + 1)
            self.text(month, 0, -128, 40, "kanit", WHITE)
            for sx in (-1, 1):
                self.rrect(sx * 80 - 9, -195, 18, 50, 9, LGREY, 6)
            self.text(dayname, 0, -50, 46, "kanit")
            self.text(str(day), 0, 60, 150, "kanit")
            if flip is not None:   # หน้ากระดาษที่กำลังปลิว (prog 0..1, เลข)
                prog, num = flip
                with self.at(0, -90 - 200 * prog, 1, -40 * prog + 25 * math.sin(prog * 9), sy=1 - 0.6 * prog):
                    self.rrect(-150, 0, 300, 260, 18, WHITE, 7)
                    self.text(str(num), 0, 140, 150, "kanit")

    def money_bag(self, x, y, sc=1.0, rot=0, seed=101):
        with self.at(x, y, sc, rot):
            self.blob(0, 0, 150, 140, BROWN2, 8, seed)
            self.poly([(-50, -120), (50, -120), (80, -190), (-80, -190)], BROWN2, 7, seed=seed + 1)
            self.rrect(-62, -140, 124, 30, 12, BROWN, 6)
            self.text("$", 0, 10, 160, "kanit")

    def coin(self, x, y, r=40, label="$", rot=0):
        with self.at(x, y, 1, rot, sx=abs(math.cos(math.radians(rot * 3))) * 0.8 + 0.2, sy=1):
            self.circle(0, 0, r, GOLD, 6)
            self.circle(0, 0, r * 0.72, GOLD2, 4)
            self.text(label, 0, 2, int(r * 1.0), "kanit")

    def fridge(self, x, y, sc=1.0, open_amt=0.0, inside="cold", seed=111, glow=0.0):
        with self.at(x, y, sc):
            self.rrect(-150, -470, 300, 470, 26, MINT, 8, seed=seed)
            if open_amt > 0:
                self.rrect(-135, -455, 270, 440, 16, GOLD2 if inside == "gold" else ICE, 6)
                if inside == "gold":
                    for i, (bx, by) in enumerate([(-60, -60), (20, -60), (-20, -110), (60, -110), (-80, -260), (10, -280)]):
                        self.poly([(bx - 40, by), (bx + 40, by), (bx + 28, by - 40), (bx - 28, by - 40)], GOLD, 5, seed=i)
                    self.blob(60, -270, 30, 38, INK, 5, seed + 3)
                    self.text("น้ำมัน", 60, -200, 30, "kanit")
                else:
                    for i in range(3):
                        self.line([(-120, -340 + i * 110), (120, -340 + i * 110)], 5, GREY)
                if glow > 0:
                    for i in range(14):
                        a = math.radians(-90 + (i - 6.5) * 13)
                        L = 260 + 60 * math.sin(self.t * 6 + i)
                        with self.alpha(0.55 * glow):
                            self.line([(math.cos(a) * 60, -240 + math.sin(a) * 60),
                                       (math.cos(a) * L, -240 + math.sin(a) * L)], 9, GOLD, amp=0)
            with self.at(-150, 0, 1, sx=max(1 - open_amt * 1.6, -0.6), sy=1):
                self.rrect(0, -470, 300, 470, 26, MINT, 8, seed=seed + 1)
                self.line([(0, -320), (300, -320)], 7)
                self.rrect(250, -440, 18, 90, 9, LGREY, 5)
                self.rrect(250, -280, 18, 120, 9, LGREY, 5)
                self.rrect(70, -230, 160, 60, 10, WHITE, 5)
                self.text("ALASKA", 150, -200, 34, "kanit")

    def flag(self, x, y, w, h, kind, t, wave=1.0, crumple=0.0):
        """ธงติดเสาที่ (x,y) มุมบนซ้าย"""
        c = self.c
        n = 18
        amp = h * 0.10 * wave
        def yoff(u):
            return amp * math.sin(u * 5 - t * 7) * u
        if kind == "ru":
            bands = [WHITE, BLUE, RED]
        elif kind == "us":
            bands = [RED, WHITE, RED, WHITE, RED, WHITE, RED]
        elif kind == "ly":     # ธงลิเบีย แดง-ดำ-เขียว (ฝ่ายต่อต้าน 2011 / ปัจจุบัน)
            bands = [RED, INK, INK, LYGREEN]
        elif kind == "lyg":    # ธงเขียวล้วนยุคกัดดาฟี
            bands = [LYGREEN]
        else:
            bands = [NAVY]
        nb = len(bands)
        sx = 1 - 0.65 * crumple
        with self.at(x, y, 1, 30 * crumple * math.sin(t * 9), sx=sx, sy=1):
            for b, col in enumerate(bands):
                top, bot = h * b / nb, h * (b + 1) / nb
                pts = [(w * i / n, top + yoff(i / n)) for i in range(n + 1)]
                pts += [(w * i / n, bot + yoff(i / n)) for i in range(n, -1, -1)]
                c.move_to(*pts[0])
                for p in pts[1:]:
                    c.line_to(*p)
                c.close_path()
                self.fs(col, 0)
            if kind == "us":
                cw, ch = w * 0.42, h * 4 / 7
                pts = [(cw * i / 8, yoff(cw * i / 8 / w)) for i in range(9)]
                pts += [(cw * i / 8, ch + yoff(cw * i / 8 / w)) for i in range(8, -1, -1)]
                c.move_to(*pts[0])
                for p in pts[1:]:
                    c.line_to(*p)
                c.close_path()
                self.fs(NAVY, 0)
                for i in range(3):
                    for j in range(2):
                        u = (0.2 + 0.3 * i) * cw
                        self.star(u, (0.3 + 0.4 * j) * ch + yoff(u / w), 9, WHITE, 0)
            if kind == "ak":
                stars = [(0.12, 0.62), (0.22, 0.58), (0.30, 0.66), (0.38, 0.72), (0.40, 0.88), (0.54, 0.88), (0.55, 0.72), (0.86, 0.22)]
                for i, (u, v) in enumerate(stars):
                    self.star(u * w, v * h + yoff(u), 22 if i == 7 else 13, GOLD, 3)
            if kind == "ly":
                u = 0.5
                self.circle(u * w, h / 2 + yoff(u), h * 0.15, WHITE, 0)
                self.circle(u * w + h * 0.05, h / 2 + yoff(u), h * 0.13, INK, 0)
                self.star(u * w + h * 0.12, h / 2 + yoff(u), h * 0.07, WHITE, 0)
            pts = [(w * i / n, yoff(i / n)) for i in range(n + 1)]
            pts += [(w * i / n, h + yoff(i / n)) for i in range(n, -1, -1)]
            c.move_to(*pts[0])
            for p in pts[1:]:
                c.line_to(*p)
            c.close_path()
            self.fs(None, 7)

    def mountains(self, y, alpha=1.0, seed=121):
        with self.alpha(alpha):
            for i, (mx, mh, mw) in enumerate([(180, 520, 330), (560, 680, 400), (900, 480, 320)]):
                self.poly([(mx - mw, y), (mx, y - mh), (mx + mw, y)], LGREY, 8, seed=seed + i)
                k = 0.3
                self.poly([(mx - mw * k, y - mh * (1 - k)), (mx, y - mh),
                           (mx + mw * k, y - mh * (1 - k)), (mx + mw * 0.15, y - mh * (1 - k) + 30),
                           (mx, y - mh * (1 - k) + 5), (mx - mw * 0.14, y - mh * (1 - k) + 35)],
                          WHITE, 6, seed=seed + 10 + i)

    def pine(self, x, y, sc=1.0, seed=131):
        with self.at(x, y, sc):
            self.rrect(-12, -40, 24, 45, 4, BROWN, 6)
            for i in range(3):
                yy = -40 - i * 60
                wdt = 90 - i * 22
                self.poly([(-wdt, yy), (wdt, yy), (0, yy - 110)], GREEN, 7, seed=seed + i)

    def snow(self, t, n=40, seed=7, area=(0, 300, W, 1350)):
        x0, y0, x1, y1 = area
        for i in range(n):
            sx = x0 + (hn(i, seed) * 0.5 + 0.5) * (x1 - x0)
            sp = 70 + 50 * (hn(i, seed + 3) * 0.5 + 0.5)
            yy = y0 + ((hn(i, seed + 1) * 0.5 + 0.5) * (y1 - y0) + t * sp) % (y1 - y0)
            xx = sx + 18 * math.sin(t * 1.5 + i)
            r = 6 + 4 * (hn(i, seed + 2) * 0.5 + 0.5)
            self.circle(xx, yy, r, WHITE, 3, stroke=GREY)

    def ground(self, y, fill=WHITE, seed=141):
        # กว้าง ±3000px: กล้องแพน/เหวี่ยงแรง ๆ จะได้ไม่เห็นขอบข้างของพื้น
        pts = [(x, y + 10 * math.sin(x * 0.01 + seed)) for x in range(-3000, W + 3001, 60)] + \
              [(W + 3000, H + 3000), (-3000, H + 3000)]
        self.poly(pts, fill, 8, seed=seed, amp=1.0)

    def sunburst(self, x, y, r0, r1, n=20, rot=0, lw=10, col=LGREY):
        for i in range(n):
            a = math.radians(rot + 360 * i / n)
            self.line([(x + math.cos(a) * r0, y + math.sin(a) * r0), (x + math.cos(a) * r1, y + math.sin(a) * r1)], lw, col, amp=0.5)

    def bubble(self, x, y, w, h, fill=WHITE, tail=(-1, 1)):
        self.rrect(x - w / 2, y - h / 2, w, h, h * 0.4, fill, 7)
        tx, ty = x + tail[0] * w * 0.2, y + h / 2 - 4
        self.poly([(tx - 20, ty), (tx + 20, ty), (tx + tail[0] * 40, ty + 50)], fill, 0)
        self.line([(tx - 20, ty + 3), (tx + tail[0] * 40, ty + 50), (tx + 20, ty + 3)], 7)

    def shape(self, pts, x, y, w, fill, lw=8, seed=151, aspect=1.0):
        q = [(x + (px - 0.5) * w, y + (py - 0.5) * w * aspect) for px, py in pts]
        self.poly(q, fill, lw, seed=seed, amp=1.5)


ALASKA = [(0.20, 0.12), (0.35, 0.05), (0.55, 0.06), (0.70, 0.10), (0.70, 0.36), (0.70, 0.62), (0.74, 0.62),
          (0.82, 0.70), (0.92, 0.80), (0.98, 0.92), (0.95, 0.94), (0.86, 0.85), (0.78, 0.76), (0.70, 0.70),
          (0.62, 0.66), (0.55, 0.68), (0.50, 0.62), (0.44, 0.66), (0.38, 0.72), (0.30, 0.78), (0.22, 0.84),
          (0.15, 0.88), (0.17, 0.84), (0.26, 0.76), (0.30, 0.70), (0.22, 0.66), (0.14, 0.62), (0.12, 0.54),
          (0.18, 0.48), (0.10, 0.42), (0.06, 0.34), (0.12, 0.30), (0.08, 0.24), (0.14, 0.18)]
THAILAND = [(0.25, 0.0), (0.35, 0.03), (0.42, 0.10), (0.52, 0.12), (0.62, 0.18), (0.80, 0.22), (0.95, 0.28),
            (0.98, 0.38), (0.90, 0.46), (0.78, 0.48), (0.70, 0.52), (0.66, 0.58), (0.60, 0.60), (0.52, 0.56),
            (0.45, 0.55), (0.42, 0.62), (0.40, 0.70), (0.38, 0.80), (0.42, 0.88), (0.48, 0.95), (0.52, 1.0),
            (0.46, 1.0), (0.38, 0.94), (0.32, 0.86), (0.30, 0.76), (0.33, 0.66), (0.32, 0.58), (0.28, 0.50),
            (0.22, 0.42), (0.18, 0.32), (0.12, 0.22), (0.15, 0.12)]
THAILAND = [((x - 0.5) * 0.55 + 0.5, y) for x, y in THAILAND]   # ไทยแคบกว่าความสูง


def poly_area(pts):
    return abs(sum(pts[i][0] * pts[i - 1][1] - pts[i - 1][0] * pts[i][1] for i in range(len(pts)))) / 2
