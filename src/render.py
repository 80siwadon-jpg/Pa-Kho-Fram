"""เรนเดอร์วิดีโอ 1080x1920 @60fps

python3 src/render.py                 # เรนเดอร์ทั้งคลิป -> build/video.mp4 (ยังไม่มีเสียง)
python3 src/render.py --still 12.5    # ส่งออกภาพนิ่งเวลา 12.5s -> build/still_12.50.png
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
from gfx import INK, PAPER, W, H, Draw, GREY, LGREY, e_back, e_io, hn, seg, text_sprite  # noqa: E402
from scenes import CUES, NO_IRIS, SCENES  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUILD = os.path.join(ROOT, "build")
FPS = 60
IRIS = 0.42
SUB_Y = 1470

TL = None
POST = None


def load_timeline():
    with open(os.path.join(BUILD, "timeline.json"), encoding="utf-8") as f:
        tl = json.load(f)
    for s in tl["scenes"]:
        s["L"] = [ln["start"] - s["start"] for ln in tl["lines"] if ln["scene"] == s["name"]]
    return tl


def write_cues(tl):
    out = []
    for s in tl["scenes"]:
        for li, off, name in CUES.get(s["name"], []):
            out.append({"t": round(s["start"] + s["L"][li] + off, 3), "sfx": name, "scene": s["name"]})
    with open(os.path.join(BUILD, "cues.json"), "w") as f:
        json.dump(out, f, indent=1)


# ------------------------------------------------------------------ film post
def make_post():
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    nx, ny = (xx - W / 2) / (W / 2), (yy - H / 2) / (H / 2)
    r = np.sqrt(nx ** 2 * 1.0 + ny ** 2 * 0.85)
    vig = np.clip(1.0 - 0.22 * np.clip(r - 0.55, 0, None) ** 1.6, 0, 1)
    tint = np.array([0.975, 0.99, 1.0], np.float32)          # BGR: อุ่นขึ้นเล็กน้อยแบบฟิล์ม
    vig3 = (vig[..., None] * tint[None, None, :]).astype(np.float32)
    rng = np.random.default_rng(7)
    grain = [rng.normal(0, 7.0, (H // 2, W // 2)).astype(np.float32) for _ in range(10)]
    grain = [np.repeat(np.repeat(gm, 2, 0), 2, 1)[..., None] for gm in grain]
    return vig3, grain


def film_overlay(g, frame):
    """ฝุ่น เส้นขีด ขนแมว แบบฟิล์มเก่า (วาดด้วย cairo)"""
    c = g.c
    step = frame // 3
    for i in range(2):   # เส้นขีดแนวตั้ง
        if hn(step, i, 1) > 0.35:
            x = (hn(step // 4, i, 2) * 0.5 + 0.5) * W
            c.set_source_rgba(*GREY[:3], 0.25 + 0.2 * hn(step, i, 3))
            c.set_line_width(1.5 + abs(hn(step, i, 4)) * 2)
            c.move_to(x, 0)
            c.line_to(x + 12 * hn(step, i, 5), H)
            c.stroke()
    n = int(4 + 4 * (hn(frame, 9) * 0.5 + 0.5))
    for i in range(n):   # ฝุ่น
        if hn(frame, i, 11) < 0.1:
            continue
        x = (hn(frame, i, 12) * 0.5 + 0.5) * W
        y = (hn(frame, i, 13) * 0.5 + 0.5) * H
        r = 1.5 + 3.5 * abs(hn(frame, i, 14))
        c.set_source_rgba(*INK[:3], 0.55)
        c.arc(x, y, r, 0, 2 * math.pi)
        c.fill()
    if hn(frame // 4, 21) > 0.82:   # ขนเส้นโค้ง
        x = (hn(frame // 4, 22) * 0.5 + 0.5) * W
        y = (hn(frame // 4, 23) * 0.5 + 0.5) * H
        c.set_source_rgba(*INK[:3], 0.5)
        c.set_line_width(2)
        c.move_to(x, y)
        c.curve_to(x + 30, y - 40, x + 60, y + 30, x + 90 + 30 * hn(frame // 4, 24), y - 10)
        c.stroke()


# ------------------------------------------------------------------ UI layers
def header(g, t, tl):
    start = tl["scenes"][1]["start"] + 2.6
    if t < start:
        return
    k = e_back(min((t - start) / 0.5, 1))
    with g.at(W / 2, -80 + 230 * k):
        g.rrect(-290, -42, 580, 84, 42, (1, 1, 1, 1), 6)
        g.circle(-240, 0, 20, (0.78, 0.33, 0.24, 1), 5)
        g.circle(-240, 0, 6, PAPER, 0)
        g.text("วันนี้ในอดีต · 18 ต.ค. 1867", 20, -2, 40, "kanit")


def subtitles(g, t, tl):
    lines = tl["lines"]
    for i, ln in enumerate(lines):
        nxt = lines[i + 1]["start"] if i + 1 < len(lines) else tl["duration"]
        end = min(ln["end"] + 0.45, nxt - 0.02)
        if ln["start"] - 0.06 <= t < end:
            k = e_back(min((t - ln["start"] + 0.06) / 0.22, 1), 2.4)
            a = min(1, (end - t) / 0.08)
            _, _, sw, _ = text_sprite(ln["text"], 70, "mali", INK, 12, PAPER, 960)
            fit = min(1.0, 990 / sw)   # บรรทัดไทยที่ไม่มีเว้นวรรค ตัดคำไม่ได้ -> ย่อให้พอดี
            g.text(ln["text"], W / 2, SUB_Y, 70, "mali", INK, sc=(0.85 + 0.15 * k) * fit, a=a,
                   stroke=12, stroke_color=PAPER, maxw=960)
            return


def progress(g, t, tl):
    p = t / tl["duration"]
    g.c.set_source_rgba(*LGREY[:3], 1)
    g.c.rectangle(0, H - 14, W, 14)
    g.c.fill()
    g.c.set_source_rgba(*INK[:3], 1)
    g.c.rectangle(0, H - 14, W * p, 14)
    g.c.fill()


def scene_at(tl, t):
    for i, s in enumerate(tl["scenes"]):
        if s["start"] <= t < s["end"] or i == len(tl["scenes"]) - 1:
            return i, s


def draw_scene(g, s, t):
    SCENES[s["name"]](g, t - s["start"], s["L"], s["end"] - s["start"])


def render_frame(frame):
    global POST
    tl = TL
    if POST is None:
        POST = make_post()
    t = frame / FPS
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    ctx = cairo.Context(surf)
    ctx.set_source_rgba(*PAPER)
    ctx.paint()
    g = Draw(ctx, t, frame)
    # gate weave (ฟิล์มส่ายนิด ๆ)
    st = frame // 5
    ctx.save()
    ctx.translate(1.6 * hn(st, 1), 2.2 * hn(st, 2))

    i, s = scene_at(tl, t)
    lt = t - s["start"]
    if i > 0 and lt < IRIS and (tl["scenes"][i - 1]["name"], s["name"]) not in NO_IRIS:
        prev = tl["scenes"][i - 1]
        draw_scene(g, prev, t)
        r = e_io(lt / IRIS) * 1250
        ctx.save()
        ctx.arc(W / 2, 860, r, 0, 2 * math.pi)
        ctx.clip()
        ctx.set_source_rgba(*PAPER)
        ctx.paint()
        draw_scene(g, s, t)
        ctx.restore()
        ctx.set_source_rgba(*INK)
        ctx.set_line_width(14)
        ctx.arc(W / 2, 860, r, 0, 2 * math.pi)
        ctx.stroke()
    else:
        draw_scene(g, s, t)
    ctx.restore()

    header(g, t, tl)
    subtitles(g, t, tl)

    # ม่านวงกลมปิดท้าย (iris out)
    end_k = seg(t, tl["duration"] - 1.0, tl["duration"] - 0.25)
    if end_k > 0:
        r = (1 - e_io(end_k)) * 1300
        ctx.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
        ctx.rectangle(-10, -10, W + 20, H + 20)
        ctx.arc(W / 2, 1000, max(r, 0.1), 0, 2 * math.pi)
        ctx.set_source_rgba(*INK)
        ctx.fill()
        ctx.set_fill_rule(cairo.FILL_RULE_WINDING)

    film_overlay(g, frame)
    progress(g, t, tl)

    surf.flush()
    buf = np.ndarray((H, W, 4), np.uint8, surf.get_data())
    vig3, grain = POST
    flick = 1.0 + 0.022 * hn(frame // 2, 77)
    img = buf[..., :3].astype(np.float32) * vig3 * flick + grain[frame % len(grain)]
    return np.clip(img, 0, 255).astype(np.uint8)   # BGR


def render_chunk(args):
    a, b, path = args
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgr24",
           "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium",
           "-crf", "23", "-pix_fmt", "yuv420p", "-threads", "2", path]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for f in range(a, b):
        p.stdin.write(render_frame(f).tobytes())
        if (f - a) % 300 == 0:
            print(f"  [{path[-12:]}] {f - a}/{b - a}", flush=True)
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
    ap.add_argument("--start", type=float, default=0.0)
    ap.add_argument("--end", type=float, default=None)
    args = ap.parse_args()
    TL = load_timeline()
    write_cues(TL)
    if args.still:
        from PIL import Image
        for s in args.still:
            img = render_frame(int(round(s * FPS)))
            Image.fromarray(img[..., ::-1]).save(os.path.join(BUILD, f"still_{s:05.2f}.png"))
        return
    end = args.end if args.end is not None else TL["duration"]
    f0, f1 = int(args.start * FPS), int(end * FPS)
    n = args.workers * 3
    bounds = [f0 + (f1 - f0) * i // n for i in range(n + 1)]
    jobs = [(bounds[i], bounds[i + 1], os.path.join(BUILD, f"chunk_{i:03d}.mp4")) for i in range(n)]
    with Pool(args.workers, initializer=init_worker) as pool:
        paths = pool.map(render_chunk, jobs, chunksize=1)
    lst = os.path.join(BUILD, "chunks.txt")
    with open(lst, "w") as f:
        for p in paths:
            f.write(f"file '{p}'\n")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst,
                    "-c", "copy", os.path.join(BUILD, "video.mp4")], check=True)
    for p in paths:
        os.remove(p)
    print("video ->", os.path.join(BUILD, "video.mp4"))


if __name__ == "__main__":
    main()
