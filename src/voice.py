"""ใช้เสียงอัดของคุณเองเป็นเสียงพากย์

วิธีทำเสียง: อ่าน/สร้างเสียงจากบท output/script_*.txt ตามลำดับ เว้นจังหวะระหว่างบรรทัด
(ช่วงหยุดระหว่างบรรทัดต้องยาวกว่าช่วงหยุดภายในบรรทัด เช่น ขึ้นบรรทัดใหม่/จุด ในเครื่องมือสร้างเสียง)
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
    out = []
    for a, b in merged:   # เผื่อขอบ 40ms แต่ไม่ให้ทับช่วงก่อนหน้า
        a = max(a * hop - pad, out[-1][1] if out else 0)
        out.append((a, min(b * hop + pad, len(x))))
    return out


def split_lines(x, runs, weights, keep_gap=0.15):
    """จัดช่วงพูด (runs) เป็นบรรทัดตามบท ด้วย dynamic programming:
    ความยาวแต่ละบรรทัดควรใกล้สัดส่วนจำนวนตัวอักษร และควรตัดตรงช่วงหยุดยาว"""
    n, m = len(weights), len(runs)
    if m < n:
        sys.exit(f"เจอช่วงพูด {m} ช่วง แต่บทมี {n} บรรทัด — เว้นจังหวะระหว่างบรรทัดให้ชัดขึ้นนะ")
    dur = np.array([(b - a) / SR for a, b in runs])
    gap = np.array([(runs[i + 1][0] - runs[i][1]) / SR for i in range(m - 1)] + [0.0])
    csum = np.concatenate([[0], np.cumsum(dur)])
    w = np.asarray(weights, float)
    exp = csum[-1] * w / w.sum()
    INF = 1e18
    cost = np.full((n + 1, m + 1), INF)
    back = np.zeros((n + 1, m + 1), int)
    cost[0, 0] = 0
    for k in range(1, n + 1):
        for j in range(k, m - (n - k) + 1):          # บรรทัด k จบที่ run j-1
            for i in range(k - 1, j):                 # เริ่มที่ run i
                if cost[k - 1, i] >= INF:
                    continue
                d = csum[j] - csum[i]
                c = cost[k - 1, i] + (d - exp[k - 1]) ** 2 / exp[k - 1] - 4.0 * gap[j - 1] * (k < n)
                if c < cost[k, j]:
                    cost[k, j], back[k, j] = c, i
    bounds, j = [], m
    for k in range(n, 0, -1):
        i = back[k, j]
        bounds.append((i, j))
        j = i
    lines = []
    for i, j in reversed(bounds):
        parts = []
        for r in range(i, j):
            if parts:   # ช่องเงียบภายในบรรทัด: ย่อให้ไม่เกิน keep_gap (ไม่ยืด)
                parts.append(np.zeros(int(min(gap[r - 1], keep_gap) * SR), np.float32))
            parts.append(x[runs[r][0]:runs[r][1]])
        lines.append(np.concatenate(parts))
    return lines


def weight(text):
    """น้ำหนักความยาวพูดโดยประมาณ: ตัวอักษรไทยที่ไม่ใช่สระบน/ล่าง/วรรณยุกต์ + ตัวเลขนับหนักกว่า"""
    marks = set("\u0e31\u0e34\u0e35\u0e36\u0e37\u0e38\u0e39\u0e3a\u0e47\u0e48\u0e49\u0e4a\u0e4b\u0e4c\u0e4d")
    return sum(3 if c.isdigit() else 1 for c in text if c not in marks and not c.isspace() and c not in '."?!')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("audio")
    ap.add_argument("--tempo", type=float, default=1.0, help="1.1 = เร็วขึ้น 10%%")
    ap.add_argument("--gap", type=float, default=0.3, help="ช่วงหายใจระหว่างบรรทัด (วินาที)")
    ap.add_argument("--out", default=os.path.join("build", os.environ.get("EPISODE", "alaska")))
    a = ap.parse_args()
    items = [(scene, disp) for scene, lines in SCENES for disp, _ in lines]
    x = load(a.audio, a.tempo)
    runs = speech_runs(x)
    lines = split_lines(x, runs, [weight(d) for _, d in items])
    for (scene, disp), y in zip(items, lines):
        print(f"{len(y) / SR:5.2f}s  {disp}")
    timeline.build([(s, d, y) for (s, d), y in zip(items, lines)], a.out, a.gap, a.gap + 0.15)


if __name__ == "__main__":
    main()
