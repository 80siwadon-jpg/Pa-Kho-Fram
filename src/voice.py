"""ใช้เสียงอัดของคุณเองเป็นเสียงพากย์

วิธีอัด: อ่านบทใน script_data.py ตามลำดับ (ข้อความซับ) เว้นจังหวะ ~1 วินาทีระหว่างบรรทัด
ไฟล์อะไรก็ได้ที่ ffmpeg อ่านได้ (m4a, mp3, wav ...)

python3 src/voice.py my_voice.m4a --tempo 1.1

- ตัดช่องเงียบให้กระชับอัตโนมัติ  - เร่งความเร็วได้โดยเสียงไม่เพี้ยน (--tempo)
- แบ่งบรรทัดจากช่วงหยุดที่ยาวที่สุด แล้ววางซับให้ตรงเสียง
"""
import argparse
import os
import subprocess
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
import timeline  # noqa: E402
from script_data import SCENES  # noqa: E402

SR = timeline.SR
HOP = 0.01   # 10 ms


def load(path, tempo):
    af = f"highpass=f=70,atempo={tempo},acompressor=threshold=-20dB:ratio=3:attack=5:release=80"
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", path, "-af", af, "-ac", "1",
                          "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).copy()


def speech_runs(x, min_gap=0.18):
    """คืนช่วงที่มีเสียงพูด [(a, b), ...] หน่วยเป็น sample"""
    hop = int(HOP * SR)
    n = len(x) // hop
    rms = np.sqrt(np.mean(x[: n * hop].reshape(n, hop) ** 2, axis=1) + 1e-12)
    db = 20 * np.log10(rms)
    thr = max(np.percentile(db, 95) - 35, np.percentile(db, 10) + 6)
    voiced = db > thr
    runs, i = [], 0
    while i < n:
        if voiced[i]:
            j = i
            while j < n and voiced[j]:
                j += 1
            runs.append([i, j])
            i = j
        else:
            i += 1
    merged = []   # รวมช่องว่างสั้น ๆ ภายในประโยค
    for r in runs:
        if merged and (r[0] - merged[-1][1]) * HOP < min_gap:
            merged[-1][1] = r[1]
        elif (r[1] - r[0]) * HOP >= 0.06:
            merged.append(r)
    pad = int(0.04 * SR)
    return [(max(a * hop - pad, 0), min(b * hop + pad, len(x))) for a, b in merged]


def split_lines(x, runs, n_lines, keep_gap=0.1):
    if len(runs) < n_lines:
        sys.exit(f"เจอช่วงพูด {len(runs)} ช่วง แต่บทมี {n_lines} บรรทัด — เว้นจังหวะระหว่างบรรทัดให้ชัดขึ้นนะ")
    gaps = [runs[i + 1][0] - runs[i][1] for i in range(len(runs) - 1)]
    cut = set(sorted(np.argsort(gaps)[::-1][: n_lines - 1]))
    lines, cur = [], []
    keep = np.zeros(int(keep_gap * SR), np.float32)
    for i, (a, b) in enumerate(runs):
        if cur:
            cur.append(keep)     # ช่องเงียบภายในบรรทัด -> สั้นลง
        cur.append(x[a:b])
        if i in cut or i == len(runs) - 1:
            lines.append(np.concatenate(cur))
            cur = []
    return lines


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("audio")
    ap.add_argument("--tempo", type=float, default=1.0, help="1.1 = เร็วขึ้น 10%%")
    ap.add_argument("--out", default="build")
    a = ap.parse_args()
    items = [(scene, disp) for scene, lines in SCENES for disp, _ in lines]
    x = load(a.audio, a.tempo)
    runs = speech_runs(x)
    lines = split_lines(x, runs, len(items))
    for (scene, disp), y in zip(items, lines):
        print(f"{len(y) / SR:5.2f}s  {disp}")
    timeline.build([(s, d, y) for (s, d), y in zip(items, lines)], a.out)


if __name__ == "__main__":
    main()
