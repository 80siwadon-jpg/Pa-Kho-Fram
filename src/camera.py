"""กล้องเสมือน: ซูมเข้า/ออก, แพน, ทิลต์, เอียง (dutch) + ทรานซิชันเปลี่ยนฉากแบบลื่นไหล

ทุกฉากได้ท่ากล้องอัตโนมัติ (วนตาม MOVE_ORDER) และกล้องจะ "ขยับต่อ" ทุกครั้งที่ขึ้นบรรทัดพากย์ใหม่
แล้วค่อย ๆ นิ่ง (เหมือนช่างภาพสารคดีจัดเฟรมตามจังหวะเล่า)
ตอนไหนอยากกำหนดเอง ใส่ใน scenes.py ของตอนนั้น:
    CAMERA = {"hook": "push_in", "treaty": "pan_right"}
    TRANSITIONS = {"treaty": "whip"}          # ทรานซิชันที่ใช้ "เข้าสู่" ฉากนั้น
"""
import math

from gfx import e_in, e_io, e_out

CENTER = (540, 820)      # จุดศูนย์กลางเวที (พิกัดฉาก)
TR = 0.55                # ความยาวทรานซิชัน (วินาที)

# ท่ากล้อง: p 0..1 -> (zoom, dx, dy, rot องศา)   dx/dy คือการเลื่อนภาพ (กล้องแพนขวา = ภาพเลื่อนซ้าย)
MOVES = {
    "push_in":    lambda p: (1.0 + 0.14 * p, 0, 0, 0),
    "pull_out":   lambda p: (1.16 - 0.16 * p, 0, 0, 0),
    "pan_right":  lambda p: (1.12, 60 - 120 * p, 0, 0),
    "pan_left":   lambda p: (1.12, -60 + 120 * p, 0, 0),
    "tilt_up":    lambda p: (1.12, 0, -45 + 90 * p, 0),
    "tilt_down":  lambda p: (1.12, 0, 45 - 90 * p, 0),
    "dutch":      lambda p: (1.06 + 0.06 * p, 0, 0, -2.5 + 5 * p),
    "still":      lambda p: (1.0, 0, 0, 0),
}
MOVE_ORDER = ["push_in", "pan_right", "tilt_up", "pull_out", "pan_left", "dutch", "tilt_down"]
TRANS_ORDER = ["fade", "zoom", "whip", "fade", "iris", "zoom", "whip"]


def progress(lt, L, d):
    """ความคืบหน้ากล้อง 0..1 แบบขั้นบันไดนุ่ม ๆ: ขยับตอนเริ่มแต่ละบรรทัด แล้วค่อย ๆ นิ่ง"""
    beats = [0.0] + [x for x in L if 0 < x < d] + [d]
    n = len(beats) - 1
    for i in range(n):
        a, b = beats[i], beats[i + 1]
        if lt < b or i == n - 1:
            local = min(max((lt - a) / max(min(b - a, 1.6), 0.1), 0.0), 1.0)   # ขยับ ~1.6 วิแรกของบรรทัด
            return (i + e_io(local)) / n
    return 1.0


def move_for(idx, name, overrides):
    return overrides.get(name) or MOVE_ORDER[idx % len(MOVE_ORDER)]


def transition_for(idx, name, overrides):
    return overrides.get(name) or TRANS_ORDER[idx % len(TRANS_ORDER)]


def apply(g, cam):
    """เปิด transform กล้อง (ใช้กับ with)"""
    z, dx, dy, rot = cam
    cx, cy = CENTER
    return _Cam(g, cx + dx, cy + dy, z, rot)


class _Cam:
    def __init__(self, g, x, y, z, rot):
        self.g, self.x, self.y, self.z, self.rot = g, x, y, z, rot

    def __enter__(self):
        c = self.g.c
        c.save()
        c.translate(self.x, self.y)
        if self.rot:
            c.rotate(math.radians(self.rot))
        c.scale(self.z, self.z)
        c.translate(-CENTER[0], -CENTER[1])

    def __exit__(self, *a):
        self.g.c.restore()


def transition_frames(kind, k):
    """คืนพารามิเตอร์ (ฉากเก่า, ฉากใหม่) ระหว่างเปลี่ยนฉาก k 0..1
    แต่ละอัน = (alpha, extra_zoom, dx, dy)"""
    if kind == "zoom":     # ซูมทะลุ: ฉากเก่าพุ่งเข้าหา+จางหาย ฉากใหม่ขยายจากเล็กมาเต็ม
        return (1 - e_in(k), 1 + 0.35 * e_in(k), 0, 0), (e_out(k), 0.88 + 0.12 * e_out(k), 0, 0)
    if kind == "whip":     # whip pan: ฉากเก่าเหวี่ยงออกซ้าย ฉากใหม่เหวี่ยงเข้าจากขวา
        return (1.0, 1.0, -1300 * e_in(k), 0), (1.0, 1.0, 1300 * (1 - e_out(k)), 0)
    # fade: ครอสเฟดนุ่ม ๆ + ซูมเล็กน้อย
    return (1 - e_io(k), 1 + 0.04 * k, 0, 0), (e_io(k), 1.04 - 0.04 * k, 0, 0)
