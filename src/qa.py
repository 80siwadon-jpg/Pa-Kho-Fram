"""ตรวจคลิปรอบสุดท้ายก่อนเผยแพร่ (ตรวจจาก mp4 ที่เรนเดอร์แล้วจริง)

EPISODE=gaddafi python3 src/qa.py output/gaddafi_20oct_1080p60.mp4 [--whisper models/sherpa-onnx-whisper-small]

ตรวจอัตโนมัติ:
  - สเปก: 1080x1920, 60fps, ยาวไม่เกิน 3 นาที, มีเสียง
  - ความดังเสียง (LUFS) และช่วงเงียบผิดปกติ
  - พื้นที่ล่าง 25% ต้องว่าง (ไม่ให้ชื่อ/คำอธิบายของแพลตฟอร์มบังเนื้อหา)
  - เฟรมดำ/เฟรมค้าง (ภาพไม่ขยับนานเกินไป)
  - ซับตรงเสียง (สุ่มถอดเสียงด้วย whisper ถ้าระบุโมเดล)
สร้างแผ่นรวมภาพทุก 1 วินาที (build/<ตอน>/qa_sheet_*.png) ไว้ดูการเคลื่อนไหวทั้งคลิปด้วยตา
"""
import argparse
import json
import os
import re
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EPISODE = os.environ.get("EPISODE", "alaska")
BUILD = os.path.join(ROOT, "build", EPISODE)
W, H = 1080, 1920
SAFE_Y = int(H * 0.85)   # พื้นที่ล่าง 15% ต้องว่าง


def probe(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                          "stream=codec_type,width,height,r_frame_rate:format=duration", "-of", "json", path],
                         capture_output=True, text=True, check=True).stdout
    return json.loads(out)


def frames(path, fps, w, h):
    """อ่านเฟรมแบบย่อ (w x h) ทีละเฟรม"""
    p = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-i", path, "-vf", f"fps={fps},scale={w}:{h}",
                          "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    n = w * h * 3
    while True:
        buf = p.stdout.read(n)
        if len(buf) < n:
            break
        yield np.frombuffer(buf, np.uint8).reshape(h, w, 3)
    p.wait()


def loudness(path):
    err = subprocess.run(["ffmpeg", "-i", path, "-af", "ebur128", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    m = re.findall(r"I:\s+(-?[\d.]+) LUFS", err)
    return float(m[-1]) if m else None


def silences(path, min_len=1.2):
    err = subprocess.run(["ffmpeg", "-i", path, "-af", f"silencedetect=n=-45dB:d={min_len}", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", err)]
    ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", err)]
    return list(zip(starts, ends))


def sheets(path, dur, out_prefix, per_sheet=24, cols=8):
    font = ImageFont.truetype(os.path.join(ROOT, "assets/fonts/Kanit-Bold.ttf"), 18)
    tw, th = 216, 384
    imgs = list(frames(path, 1, tw, th))
    paths = []
    for s in range(0, len(imgs), per_sheet):
        chunk = imgs[s:s + per_sheet]
        rows = (len(chunk) + cols - 1) // cols
        sheet = Image.new("RGB", (cols * tw, rows * (th + 24)), "white")
        d = ImageDraw.Draw(sheet)
        for i, im in enumerate(chunk):
            x, y = (i % cols) * tw, (i // cols) * (th + 24)
            sheet.paste(Image.fromarray(im), (x, y + 24))
            d.rectangle([x, y + 24, x + tw - 1, y + 24 + th - 1], outline=(200, 200, 200))
            d.line([x, y + 24 + th * SAFE_Y / H, x + tw, y + 24 + th * SAFE_Y / H], fill=(230, 80, 80))
            d.text((x + 6, y + 2), f"{s + i}s", fill=(0, 0, 0), font=font)
        p = f"{out_prefix}_{s // per_sheet + 1}.png"
        sheet.save(p)
        paths.append(p)
    return paths


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--whisper", default=None, help="โฟลเดอร์โมเดล sherpa-onnx-whisper-small (ถ้าต้องการตรวจซับ)")
    a = ap.parse_args()
    problems, notes = [], []

    info = probe(a.video)
    v = next(s for s in info["streams"] if s["codec_type"] == "video")
    has_audio = any(s["codec_type"] == "audio" for s in info["streams"])
    dur = float(info["format"]["duration"])
    num, den = map(int, v["r_frame_rate"].split("/"))
    fps = num / den
    notes.append(f"สเปก {v['width']}x{v['height']} @ {fps:g}fps, ยาว {dur:.1f} วิ, เสียง {'มี' if has_audio else 'ไม่มี'}")
    if (v["width"], v["height"]) != (W, H):
        problems.append("ความละเอียดไม่ใช่ 1080x1920")
    if abs(fps - 60) > 0.01:
        problems.append(f"fps = {fps:g} ไม่ใช่ 60")
    if dur > 180:
        problems.append(f"ยาว {dur:.0f} วิ เกิน 3 นาที")
    if not has_audio:
        problems.append("ไม่มีเสียง")

    lufs = loudness(a.video)
    notes.append(f"ความดัง {lufs} LUFS (เป้า -14)")
    if lufs is not None and not -16.5 <= lufs <= -11.5:
        problems.append(f"ความดัง {lufs} LUFS ห่างจาก -14 เกินไป")
    for s0, s1 in silences(a.video):
        if s1 < dur - 1.5:
            problems.append(f"เสียงเงียบนาน {s1 - s0:.1f} วิ ที่ {s0:.1f}-{s1:.1f}")

    # ตรวจทุกเฟรม (ย่อ) ที่ 10 fps: พื้นที่ล่าง, เฟรมดำ, ภาพค้าง
    small_w, small_h = 270, 480
    sy = int(small_h * SAFE_Y / H) + 2
    prev, still_since, black, intrusions = None, 0.0, [], []
    edge_hits = []   # ของ (เส้นดำ/ตัวหนังสือ) แตะขอบซ้าย-ขวาของจอ = ล้นออกนอกจอ
    ey0, ey1 = int(small_h * 0.06), int(small_h * 0.58)
    still_spans = []
    for i, f in enumerate(frames(a.video, 10, small_w, small_h)):
        t = i / 10
        g = f.mean(axis=2)
        if g.mean() < 20:
            black.append(t)
        strip = np.concatenate([g[ey0:ey1, :3], g[ey0:ey1, -3:]], axis=1)
        if (strip < 170).mean() > 0.02:
            edge_hits.append(t)
        bottom = g[sy:, :]
        if (bottom < 200).mean() > 0.002:
            intrusions.append(t)
        if prev is not None:
            moving = np.abs(g - prev).mean() > 0.15
            if moving:
                if t - still_since > 3.0:
                    still_spans.append((still_since, t))
                still_since = t
        prev = g
    if t - still_since > 3.0:
        still_spans.append((still_since, t))
    if black:
        problems.append(f"เฟรมดำ {len(black)} จุด เช่น {black[:3]}")
    if intrusions:
        spans, s = [], intrusions[0]
        for x, y in zip(intrusions, intrusions[1:] + [None]):
            if y is None or y - x > 0.15:
                spans.append((s, x))
                s = y
        problems.append("มีภาพในพื้นที่ล่าง 25%: " + ", ".join(f"{p:.1f}-{q:.1f}s" for p, q in spans[:8]))
    if edge_hits:
        spans, s0 = [], edge_hits[0]
        for x, y in zip(edge_hits, edge_hits[1:] + [None]):
            if y is None or y - x > 0.15:
                if x - s0 >= 0.3:   # แตะขอบสั้น ๆ ตอนทรานซิชัน/whip ไม่นับ
                    spans.append((s0, x))
                s0 = y
        if spans:
            problems.append("ภาพล้นขอบจอซ้าย/ขวา: " + ", ".join(f"{p:.1f}-{q:.1f}s" for p, q in spans[:10]))
    for p0, p1 in still_spans:
        problems.append(f"ภาพค้างไม่ขยับ {p1 - p0:.1f} วิ ที่ {p0:.1f}-{p1:.1f}s")

    # ซับตรงเสียง
    tl_path = os.path.join(BUILD, "timeline.json")
    if a.whisper and os.path.exists(tl_path):
        import sherpa_onnx
        M = a.whisper.rstrip("/") + "/"
        rec = sherpa_onnx.OfflineRecognizer.from_whisper(
            encoder=M + "small-encoder.int8.onnx", decoder=M + "small-decoder.int8.onnx",
            tokens=M + "small-tokens.txt", language="th", task="transcribe", num_threads=4)
        tl = json.load(open(tl_path, encoding="utf-8"))
        idx = np.linspace(0, len(tl["lines"]) - 1, 6).astype(int)
        for i in idx:
            ln = tl["lines"][i]
            raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-ss", str(ln["start"]), "-t",
                                  str(ln["end"] - ln["start"]), "-i", a.video, "-ac", "1", "-ar", "16000",
                                  "-f", "f32le", "-"], capture_output=True).stdout
            s = rec.create_stream()
            s.accept_waveform(16000, np.frombuffer(raw, np.float32).copy())
            rec.decode_stream(s)
            want = ln["text"].replace("\u200b", "").replace(" ", "")[:6]
            got = s.result.text.replace(" ", "")
            ok = sum(c in got[:12] for c in want) >= 3
            notes.append(f"ซับ {ln['start']:6.1f}s {'✓' if ok else '✗'} {ln['text'][:30]} | ได้ยิน: {s.result.text[:30]}")
            if not ok:
                problems.append(f"ซับอาจไม่ตรงเสียงที่ {ln['start']:.1f}s")

    os.makedirs(BUILD, exist_ok=True)
    paths = sheets(a.video, dur, os.path.join(BUILD, "qa_sheet"))
    print("\n".join(notes))
    print("\nแผ่นตรวจภาพ:", *paths, sep="\n  ")
    print("\nผลตรวจ:", "ผ่าน ✓" if not problems else f"พบ {len(problems)} จุด")
    for p in problems:
        print("  ✗", p)
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
