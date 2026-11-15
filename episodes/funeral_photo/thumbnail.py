"""ปกคลิป 1280x720: หน้าพีทตกใจ แสงจอสาด + ดวงตาคุณยายในจอมองกลับมา + ข้อความ 3 คำ
EPISODE=funeral_photo python3 episodes/funeral_photo/thumbnail.py -> output/funeral_photo_thumbnail.png"""
import os
import sys

import cairo

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.dirname(__file__))
import chars as C  # noqa: E402
from gfx import Draw, H, W, hexc  # noqa: E402
from people import _rr, _shade  # noqa: E402

TEXT = "ห้ามจ้องตา"

surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
ctx = cairo.Context(surf)
g = Draw(ctx, 0.0, 0)
C.blurred(g, "work_night", lambda g2: C.set_workroom(g2, "night"), 9)
C.darken(g, 0.55)
# จอใหญ่ด้านขวา: ดวงตาคุณยายมองตรงมาที่คนดู
with g.at(1330, 1000, 2.5):
    C.crt(g, 0, 0, 1.0, lambda g2: C.editor_ui(g2, lambda g3: C.big_eye(g3, 20, -215, 0.62, (0.15, 0.0), True, None, 0.9)))
C.glow(g, 1330, 470, 700, (0.7, 0.88, 1.0, 1), 0.35)
# หน้าพีทซ้าย แสงจอสาดจากขวา
with g.at(520, 610, 4.4):
    g.blob(0, 175, 150, 95, C.PETE.suit, 3, 7)
    C.flat_head(g, C.PETE, "shock", 0.0, 0.45, (1, 0), 99)
C.light_pass(g, 1330, 470, (0.7, 0.88, 1.0), 0.7, 1500, dust=False)
C.vignette(g, 0.6)
# ข้อความ 3 คำ: ใหญ่ ขาว ขอบดำหนา + ขีดแดง
g.text(TEXT, 520, 140, 170, "kanit", (1, 1, 1, 1), stroke=16, stroke_color=(0.05, 0.03, 0.03, 1))
_rr(ctx, 210, 240, 620, 22, 8)
_shade(ctx, hexc("#d42a2a"), 0, 0)
surf.flush()
from PIL import Image  # noqa: E402
import numpy as np  # noqa: E402
arr = np.ndarray((H, W, 4), np.uint8, surf.get_data())
out = os.path.join(ROOT, "output", "funeral_photo_thumbnail.png")
Image.fromarray(arr[..., [2, 1, 0]].copy()).resize((1280, 720), Image.LANCZOS).save(out)
print(out)
