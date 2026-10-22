"""เรนเดอร์วิดีโอ 1080x1920 @60fps พร้อมเสียงพากย์ -> output/<name>.mp4

python3 src/render.py                 # เรนเดอร์ทั้งคลิป
python3 src/render.py --still 12.5    # ภาพนิ่งเวลา 12.5s -> build/still_12.50.png
"""
import argparse
import json
import math
import os
import subprocess
import sys
from multiprocessing import Pool

import cairo
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
import camera  # noqa: E402
from gfx import INK, PAPER, W, H, Draw, e_back, e_io, text_sprite  # noqa: E402
from script_data import COVER, HEADER  # noqa: E402
import importlib.util  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EPISODE = os.environ.get("EPISODE", "alaska")
_spec = importlib.util.spec_from_file_location("scenes", os.path.join(ROOT, "episodes", EPISODE, "scenes.py"))
_scenes = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_scenes)
SCENES, NO_IRIS = _scenes.SCENES, getattr(_scenes, "NO_IRIS", set())
CAMERA = getattr(_scenes, "CAMERA", {})
TRANSITIONS = getattr(_scenes, "TRANSITIONS", {})
OWN_COVER = getattr(_scenes, "OWN_COVER", False)   # ตอนที่วาดหน้าปกเองใน s_hook

BUILD = os.path.join(ROOT, "build", EPISODE)
FPS = 60
# ย่อฉากเข้าด้านบน เว้นพื้นที่ล่าง 15% และขอบขวาให้ชื่อ/คำอธิบาย/ปุ่มของแพลตฟอร์ม
SAFE_SCALE = 0.92
SAFE_TOP = 50
SAFE_BOTTOM = int(H * 0.85)   # ห้ามมีอะไรต่ำกว่านี้ (พิกัดจอ)
SCENE_BOTTOM = 1420           # ขอบล่างของภาพในพิกัดฉาก (ใต้นี้เป็นที่ของซับ)
SUB_TOP = 1380   # ขอบบนของซับ พิกัดจอ (ซับวาดนอกการย่อฉาก; 2 บรรทัดยังจบเหนือ SAFE_BOTTOM)
SUB_SIZE = 74
SUB_W = 900

TL = None


def load_timeline():
    with open(os.path.join(BUILD, "timeline.json"), encoding="utf-8") as f:
        tl = json.load(f)
    for i, s in enumerate(tl["scenes"]):
        s["idx"] = i
        s["L"] = [ln["start"] - s["start"] for ln in tl["lines"] if ln["scene"] == s["name"]]
    return tl


def header(g, t, tl):
    start = tl["scenes"][1]["start"] + 2.0
    if t < start:
        return
    k = e_back(min((t - start) / 0.4, 1))
    with g.at(W / 2, -80 + 230 * k):
        g.rrect(-290, -42, 580, 84, 42, (1, 1, 1, 1), 6)
        g.circle(-240, 0, 20, (0.78, 0.33, 0.24, 1), 5)
        g.circle(-240, 0, 6, PAPER, 0)
        g.text(HEADER, 20, -2, 40, "kanit")


def subtitles(g, t, tl):
    lines = tl["lines"]
    for i, ln in enumerate(lines):
        nxt = lines[i + 1]["start"] if i + 1 < len(lines) else tl["duration"]
        end = min(ln["end"] + 0.3, nxt - 0.02)
        if ln["start"] - 0.05 <= t < end:
            k = e_back(min((t - ln["start"] + 0.05) / 0.18, 1), 2.4)
            _, _, sw, sh = text_sprite(ln["text"], SUB_SIZE, "kanitsb", INK, 0, PAPER, SUB_W)
            fit = min(1.0, (SUB_W + 40) / sw, (SAFE_BOTTOM - SUB_TOP - 10) / sh)   # ย่อให้พอดีกรอบ
            g.text(ln["text"], W / 2, SUB_TOP + sh * fit / 2, SUB_SIZE, "kanitsb", INK,
                   sc=(0.85 + 0.15 * k) * fit, maxw=SUB_W)
            return


def scene_at(tl, t):
    for i, s in enumerate(tl["scenes"]):
        if s["start"] <= t < s["end"] or i == len(tl["scenes"]) - 1:
            return i, s


def draw_scene(g, s, t, extra=(1.0, 1.0, 0, 0)):
    """วาดฉากผ่านกล้อง; extra = (alpha, zoom เพิ่ม, dx, dy) สำหรับทรานซิชัน"""
    lt, d = t - s["start"], s["end"] - s["start"]
    move = camera.MOVES[camera.move_for(s["idx"], s["name"], CAMERA)]
    z, dx, dy, rot = move(camera.progress(lt, s["L"], d))
    a, ez, ex, ey = extra
    cam = (z * ez, dx + ex, dy + ey, rot)
    with g.alpha(a):
        g.scene_m = tuple(g.c.get_matrix())   # พิกัดฉากก่อนกล้อง (ใช้ย่อตัวหนังสือไม่ให้ล้นขอบ)
        with camera.apply(g, cam):
            SCENES[s["name"]](g, lt, s["L"], d)


def cover_overlay(g, t, tl):
    """หน้าปกโพลารอยด์เปิดคลิป (COVER ใน script.py): เฟรมแรก = ปก ค้างถึงบรรทัดที่ 2 แล้วปลิวออกขวา
    ไม่มีภาพจริง -> ภาพในกรอบ = ฉากการ์ตูนของตอนเอง ณ เวลา COVER["art"] (ตัดส่วนหัวข้อด้านบนออก)"""
    if not COVER or OWN_COVER:
        return
    import photos
    t_out = tl["lines"][1]["start"] + 0.4 if len(tl["lines"]) > 1 else 1.5
    if t >= t_out + 0.3:
        return
    u = e_io(min(max((t - t_out) / 0.3, 0), 1))
    if u == 0:
        g.c.save()
        g.c.rectangle(-W, -H, 3 * W, 3 * H)
        g.c.set_source_rgba(*PAPER)
        g.c.fill()
        g.c.restore()
    art_t = COVER.get("art")

    def art(g2, w, h):
        if art_t is None:
            return
        _, s = scene_at(tl, art_t)
        lt = art_t - s["start"]
        sc = w / COVER.get("crop_w", 860)
        cy = COVER.get("crop_y", 960)
        with g2.at(0, 0, sc):
            g2.c.translate(-W / 2, -cy)
            g2.scene_m = tuple(g2.c.get_matrix())
            SCENES[s["name"]](g2, lt, s["L"], s["end"] - s["start"])
    g.label("วันนี้ในอดีต", W / 2, 250 - 300 * u, 80, rot=-2)
    photos.cover(g, COVER.get("photo"), COVER["date"], COVER["title"], 1 - 0.4 * u, -2 - 25 * u,
                 zoom=1.0 + 0.04 * t, x=W / 2 + 900 * u, y=690, w=600, h=700, fallback=art)


def render_frame(frame):
    tl = TL
    t = frame / FPS
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    ctx = cairo.Context(surf)
    ctx.set_source_rgba(*PAPER)
    ctx.paint()
    g = Draw(ctx, t, frame)
    ctx.save()
    ctx.translate(W / 2, SAFE_TOP)
    ctx.scale(SAFE_SCALE, SAFE_SCALE)
    ctx.translate(-W / 2, -SAFE_TOP)

    i, s = scene_at(tl, t)
    lt = t - s["start"]
    prev = tl["scenes"][i - 1] if i > 0 else None
    kind = "cut" if prev is None or (prev["name"], s["name"]) in NO_IRIS else \
        camera.transition_for(i, s["name"], TRANSITIONS)
    if prev is not None and lt < camera.TR and kind == "iris":
        draw_scene(g, prev, t)
        r = e_io(lt / camera.TR) * 1250
        ctx.save()
        ctx.arc(W / 2, 860, r, 0, 2 * math.pi)
        ctx.clip()
        ctx.set_source_rgba(*PAPER)
        ctx.paint()
        draw_scene(g, s, t)
        ctx.restore()
        ctx.save()
        ctx.rectangle(-W, -H, 3 * W, H + SCENE_BOTTOM)   # เส้นม่านไม่ลงพื้นที่ซับ/พื้นที่ล่าง
        ctx.clip()
        ctx.set_source_rgba(*INK)
        ctx.set_line_width(12)
        ctx.arc(W / 2, 860, r, 0, 2 * math.pi)
        ctx.stroke()
        ctx.restore()
    elif prev is not None and lt < camera.TR and kind != "cut":
        old, new = camera.transition_frames(kind, lt / camera.TR)
        draw_scene(g, prev, t, old)
        draw_scene(g, s, t, new)
    else:
        draw_scene(g, s, t)
    header(g, t, tl)
    cover_overlay(g, t, tl)
    ctx.restore()
    subtitles(g, t, tl)
    surf.flush()
    return np.ndarray((H, W, 4), np.uint8, surf.get_data())   # BGRA


def render_chunk(args):
    a, b, path = args
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra",
           "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium",
           "-crf", "20", "-pix_fmt", "yuv420p", "-threads", "2", path]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for f in range(a, b):
        p.stdin.write(render_frame(f).tobytes())
    p.stdin.close()
    p.wait()
    return path


def init_worker():
    global TL
    TL = load_timeline()


def main():
    global TL
    ap = argparse.ArgumentParser()
    ap.add_argument("--still", type=float, nargs="*")
    ap.add_argument("--workers", type=int, default=os.cpu_count())
    ap.add_argument("--out", default=os.path.join(ROOT, "output", "clip.mp4"))
    args = ap.parse_args()
    TL = load_timeline()
    if args.still:
        from PIL import Image
        for s in args.still:
            img = render_frame(int(round(s * FPS)))
            Image.fromarray(img[..., [2, 1, 0]].copy()).save(os.path.join(BUILD, f"still_{s:05.2f}.png"))
        return
    n_frames = int(TL["duration"] * FPS)
    n = args.workers * 3
    bounds = [n_frames * i // n for i in range(n + 1)]
    jobs = [(bounds[i], bounds[i + 1], os.path.join(BUILD, f"chunk_{i:03d}.mp4")) for i in range(n)]
    with Pool(args.workers, initializer=init_worker) as pool:
        paths = pool.map(render_chunk, jobs, chunksize=1)
    lst = os.path.join(BUILD, "chunks.txt")
    with open(lst, "w") as f:
        f.writelines(f"file '{p}'\n" for p in paths)
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst,
                    "-i", os.path.join(BUILD, "narration.wav"), "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11",
                    "-ar", "48000", "-shortest", "-movflags", "+faststart", args.out], check=True)
    for p in paths:
        os.remove(p)
    print("done ->", args.out)


if __name__ == "__main__":
    main()
