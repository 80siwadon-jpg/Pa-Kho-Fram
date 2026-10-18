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


def subdivide(x, runs, min_len=0.18):
    """ซอย run ยาว ๆ ที่จุดเสียงเบาลงระหว่างพยางค์ (energy dip) ให้ตัดบรรทัดได้แม้ผู้พูดไม่หยุด"""
    hop = int(HOP * SR)
    out = []
    for a, b in runs:
        n = (b - a) // hop
        if n < 2 * min_len / HOP:
            out.append((a, b))
            continue
        e = np.sqrt(np.mean(x[a:a + n * hop].reshape(n, hop) ** 2, axis=1) + 1e-12)
        e = np.convolve(e, np.ones(5) / 5, mode="same")
        win = int(0.15 / HOP)
        cuts, last = [], 0
        for i in range(win, n - win):
            seg = e[i - win:i + win + 1]
            if e[i] == seg.min() and e[i] < 0.6 * seg.max() and (i - last) * HOP >= min_len \
                    and (n - i) * HOP >= min_len:
                cuts.append(i)
                last = i
        edges = [a] + [a + c * hop for c in cuts] + [b]
        out += list(zip(edges[:-1], edges[1:]))
    return out


def split_lines(x, runs, weights, keep_gap=0.15, refine=None, labels=None, label_w=10.0):
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
    if labels is not None:   # lab_cost[k, j] = ผลรวมความไม่ตรงของ run 0..j-1 ถ้าเป็นบรรทัด k (ถ่วงด้วยความยาว)
        lab = np.asarray(labels, float)
        miss = np.where(lab[None, :] < 0, 0.0,
                        np.minimum(np.abs(lab[None, :] - np.arange(n)[:, None]), 3.0)) * dur[None, :]
        lab_cost = np.concatenate([np.zeros((n, 1)), np.cumsum(miss, axis=1)], axis=1)
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
                if labels is not None:   # ถอดเสียงบอกว่า run นี้น่าจะเป็นบรรทัดไหน
                    c += label_w * float(lab_cost[k - 1, j] - lab_cost[k - 1, i])
                if c < cost[k, j]:
                    cost[k, j], back[k, j] = c, i
    bounds, j = [], m
    for k in range(n, 0, -1):
        i = back[k, j]
        bounds.append((i, j))
        j = i
    bounds = list(reversed(bounds))
    if refine is not None:
        bounds = refine(x, runs, bounds)
    lines = []
    for i, j in bounds:
        parts = []
        for r in range(i, j):
            if parts:   # ช่องเงียบภายในบรรทัด: ย่อให้ไม่เกิน keep_gap (ไม่ยืด)
                parts.append(np.zeros(int(min(gap[r - 1], keep_gap) * SR), np.float32))
            parts.append(x[runs[r][0]:runs[r][1]])
        lines.append(np.concatenate(parts))
    return lines


def align(h, s):
    """Needleman-Wunsch: คืน pos[i] = ตำแหน่งใน s ที่ตัวอักษร h[i] จับคู่ (หรือใกล้ที่สุด)"""
    n, m = len(h), len(s)
    D = np.zeros((n + 1, m + 1), np.int32)
    D[:, 0] = np.arange(n + 1)
    D[0, :] = np.arange(m + 1)
    sarr = np.frombuffer(s.encode("utf-32-le"), np.uint32)
    for i in range(1, n + 1):
        sub = D[i - 1, :-1] + (sarr != ord(h[i - 1]))
        row = np.minimum(sub, D[i - 1, 1:] + 1)
        # การลบใน s (เดินแนวนอน) ต้องสะสมทีละช่อง
        for j in range(1, m + 1):
            v = row[j - 1]
            w = D[i, j - 1] + 1
            D[i, j] = v if v < w else w
    pos = [0] * n
    i, j = n, m
    while i > 0 and j > 0:
        if D[i, j] == D[i - 1, j - 1] + (s[j - 1] != h[i - 1]):
            pos[i - 1] = j - 1
            i, j = i - 1, j - 1
        elif D[i, j] == D[i - 1, j] + 1:
            pos[i - 1] = j - 1
            i -= 1
        else:
            j -= 1
    while i > 0:
        pos[i - 1] = 0
        i -= 1
    return pos


def whisper_labels(x, runs, texts, refiner, seg_len=1.0):
    """ติดป้าย 'บรรทัดที่น่าจะเป็น' ให้แต่ละ run: ถอดเสียงเป็นท่อน ~1.4 วิ แล้วจัดตำแหน่งตัวอักษรเทียบบท"""
    S, line_of = "", []
    for k, t in enumerate(texts):
        sk = skeleton(t)
        S += sk
        line_of += [k] * len(sk)
    segs, cur = [], []
    for r, (a, b) in enumerate(runs):
        cur.append(r)
        if (runs[cur[-1]][1] - runs[cur[0]][0]) / SR >= seg_len:
            segs.append(cur)
            cur = []
    if cur:
        segs.append(cur)
    H, owner = "", []
    for si, seg in enumerate(segs):
        h = refiner.hear(x, runs[seg[0]][0], runs[seg[-1]][1])
        H += h
        owner += [si] * len(h)
    pos = align(H, S) if H else []
    labels = [-1] * len(runs)
    for si, seg in enumerate(segs):
        idx = [line_of[pos[i]] for i in range(len(H)) if owner[i] == si]
        if not idx:
            continue
        a0, a1 = runs[seg[0]][0], runs[seg[-1]][1]
        for r in seg:   # run ในท่อน -> ตำแหน่งตามสัดส่วนเวลา
            f = ((runs[r][0] + runs[r][1]) / 2 - a0) / max(a1 - a0, 1)
            labels[r] = idx[min(int(f * len(idx)), len(idx) - 1)]
    return labels


CONS = set("กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธนบปผฝพฟภมยรลวศษสหฬอฮ0123456789")


def skeleton(text):
    """เหลือแต่พยัญชนะ/ตัวเลข ให้เทียบกับผลถอดเสียงที่สะกดผิดได้"""
    return "".join(c for c in text if c in CONS)


class WhisperRefiner:
    """ขยับจุดตัดบรรทัดให้ตรงคำพูดจริง: ลองช่วงหยุดใกล้ ๆ จุดที่ DP เลือก
    แล้วถอดเสียงช่วงต้นของบรรทัดถัดไปมาเทียบกับข้อความ"""

    def __init__(self, model_dir, texts, sr=SR, span=3):
        import sherpa_onnx
        m = model_dir.rstrip("/") + "/"
        self.rec = sherpa_onnx.OfflineRecognizer.from_whisper(
            encoder=m + "small-encoder.int8.onnx", decoder=m + "small-decoder.int8.onnx",
            tokens=m + "small-tokens.txt", language="th", task="transcribe", num_threads=4)
        self.texts, self.sr, self.span = texts, sr, span

    def hear(self, x, a, b):
        y = x[a:b]
        n = int(len(y) * 16000 / self.sr)
        y = np.interp(np.linspace(0, len(y) - 1, n), np.arange(len(y)), y).astype(np.float32)
        s = self.rec.create_stream()
        s.accept_waveform(16000, y)
        self.rec.decode_stream(s)
        return skeleton(s.result.text)

    def score(self, x, runs, r, k):
        """r = run แรกของบรรทัด k: เสียง 1.6 วิแรกควรขึ้นต้นด้วยข้อความบรรทัด k"""
        import difflib
        a = runs[r][0]
        heard = self.hear(x, a, min(a + int(1.6 * self.sr), len(x)))
        want = skeleton(self.texts[k])[:max(len(heard), 4)]
        return difflib.SequenceMatcher(None, heard[:len(want) + 2], want).ratio()

    def __call__(self, x, runs, bounds):
        starts = [i for i, _ in bounds]
        m = len(runs)
        for k in range(1, len(starts)):
            lo = max(starts[k - 1] + 1, starts[k] - self.span)
            hi = min(m - (len(starts) - k), starts[k] + self.span)
            cands = range(lo, hi + 1)
            best = max(cands, key=lambda r: (round(self.score(x, runs, r, k), 2), -abs(r - starts[k])))
            starts[k] = best
        return [(starts[k], starts[k + 1] if k + 1 < len(starts) else m) for k in range(len(starts))]


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
