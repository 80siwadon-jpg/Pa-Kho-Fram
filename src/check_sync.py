"""ตรวจซับตรงเสียงทุกบรรทัด: ถอดเสียง 1.6 วิแรกของแต่ละบรรทัดเทียบกับข้อความ
EPISODE=<ตอน> python3 src/check_sync.py <โฟลเดอร์ whisper>"""
import difflib
import json
import os
import sys
import wave

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
import voice  # noqa: E402

ep = os.environ.get("EPISODE", "alaska")
build = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "build", ep)
tl = json.load(open(os.path.join(build, "timeline.json"), encoding="utf-8"))
w = wave.open(os.path.join(build, "narration.wav"))
x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
texts = [ln["text"] for ln in tl["lines"]]
ref = voice.WhisperRefiner(sys.argv[1], texts, sr=w.getframerate())
import difflib as _d  # noqa: E402
bad = 0
for i, ln in enumerate(tl["lines"]):
    a = int(ln["start"] * w.getframerate())
    b = int(ln["end"] * w.getframerate())
    heard = ref.hear(x, a, b)
    want = voice.skeleton(ln["text"])
    prev = voice.skeleton(texts[i - 1])[-6:] if i else ""
    nxt = voice.skeleton(texts[i + 1])[:6] if i + 1 < len(texts) else ""
    r = _d.SequenceMatcher(None, heard, want).ratio()
    # ได้ยินคำของบรรทัดข้างเคียงชัด ๆ = ตัดผิด
    leak = (nxt and _d.SequenceMatcher(None, heard[-len(nxt):], nxt).ratio() > 0.7) or \
           (prev and _d.SequenceMatcher(None, heard[:len(prev)], prev).ratio() > 0.7)
    ok = r >= 0.5 and not leak
    bad += not ok
    print(f"{'✓' if ok else '✗'} {i:2d} {r:.2f}{' รั่ว' if leak else ''} {ln['text'].replace(chr(0x200b), ' ')[:30]:<30} | {heard[:24]}")
print(f"\nไม่ตรง {bad}/{len(texts)} บรรทัด")
