"""ปกคลิป 1280x720: รูปหมู่ในจอ มีเด็กผู้หญิงเปียกน้ำเกินมา 1 คน (วงแดง) + หน้าพีทตกใจ + ข้อความ 3 คำ
EPISODE=class_photo python3 episodes/class_photo/thumbnail.py -> output/class_photo_thumbnail.png"""
import os
import sys

import cairo

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.dirname(__file__))
import chars as C  # noqa: E402
from gfx import Draw, H, W, hexc  # noqa: E402
from people import _rr, _shade  # noqa: E402

TEXT = "เกินมาหนึ่งคน"

surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
ctx = cairo.Context(surf)
g = Draw(ctx, 0.0, 0)
C.blurred(g, "work_night", lambda g2: C.set_workroom(g2, "night"), 9)
C.darken(g, 0.55)
# รูปหมู่ขยายใหญ่ด้านขวา (ซูมแถวกลาง) — เด็กผู้หญิงผมเปียกอยู่กลางรูป
with g.at(1330, 640, 1.0):
    ctx.save()
    _rr(ctx, -560, -420, 1120, 840, 10)
    ctx.clip()
    with g.at(-1.0 * 0.06 * 1100 * 2.4, -0.08 * 1100 * 0.66 * 2.4 + 60, 2.4):
        C.class_photo(g, 0, 0, 1100, 0.0, 0, 1.0)
    ctx.restore()
with g.alpha(0.9):   # เด็กผู้หญิงที่เกินมา: ชัดกว่าในคลิปให้อ่านออกบนปกเล็ก
    C.mini_kid(g, 1335, 740, 2.61, 77, True, 1.0, 0.0, False)
with g.at(1330, 640, 1.0):
    _rr(ctx, -560, -420, 1120, 840, 10)
    ctx.set_source_rgba(*hexc("#e9e4d6"))
    ctx.set_line_width(14)
    ctx.stroke()
C.glow(g, 1330, 600, 700, (0.7, 0.88, 1.0, 1), 0.25)
# วงแดงรอบเด็กที่เกินมา
ctx.save()
ctx.translate(1335, 610)
ctx.scale(1.0, 1.25)
ctx.arc(0, 0, 165, 0, 6.283)
ctx.restore()
ctx.set_source_rgba(*hexc("#e02a2a"))
ctx.set_line_width(14)
ctx.stroke()
# หน้าพีทซ้าย
with g.at(470, 640, 4.2):
    g.blob(0, 175, 150, 95, C.PETE.suit, 3, 7)
    C.flat_head(g, C.PETE, "shock", 0.0, 0.45, (1, 0), 99)
C.light_pass(g, 1330, 470, (0.7, 0.88, 1.0), 0.7, 1500, dust=False)
C.vignette(g, 0.6)
g.text(TEXT, 520, 140, 150, "kanit", (1, 1, 1, 1), stroke=16, stroke_color=(0.05, 0.03, 0.03, 1))
_rr(ctx, 130, 236, 780, 22, 8)
_shade(ctx, hexc("#d42a2a"), 0, 0)
surf.flush()
from PIL import Image  # noqa: E402
import numpy as np  # noqa: E402
arr = np.ndarray((H, W, 4), np.uint8, surf.get_data())
out = os.path.join(ROOT, "output", "class_photo_thumbnail.png")
Image.fromarray(arr[..., [2, 1, 0]].copy()).resize((1280, 720), Image.LANCZOS).save(out)
print(out)
