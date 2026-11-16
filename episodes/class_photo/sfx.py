"""เสียงประกอบตอน class_photo (คลังเสียง earshot + เสียงระฆังสังเคราะห์)
EPISODE=class_photo python3 episodes/class_photo/sfx.py -> build/class_photo/sfx.wav
"""
import importlib.util
import json
import os
import sys

import numpy as np
import soundfile as sf

_p = os.path.join(os.path.dirname(__file__), "..", "funeral_photo", "sfx.py")
_s = importlib.util.spec_from_file_location("fp_sfx", _p)
FP = importlib.util.module_from_spec(_s)
_s.loader.exec_module(FP)
SR, BUILD, render, pick = FP.SR, FP.BUILD, FP.render, FP.pick

# (ฉาก, บรรทัดที่, [เวลาหลังต้นบรรทัด], id ในคลัง, dB, pitch)
CUES = [
    ("hook", 3, [0.4], "SUBDROP", -10, None),                        # เด็กที่เกินมาโผล่
    ("recap", 1, [0.6, 1.4], "click/soft", -18, None),
    ("crew", 5, [0.3, 0.6, 0.9, 1.2], "knock/wood", -18, "C4"),        # ฝีเท้าวิ่งหนี
    ("teacher", 0, [0.3, 1.1], "knock/wood", -18, "C4"),
    ("teacher", 4, [0.3, 0.9, 1.5, 2.1], "fit/tick/domino", -16, None),  # นับคน
    ("night1", 0, [0.7], "click/snap", -12, None),                   # จุดธูป
    ("night1", 1, [0.5, 1.3, 2.0], "click/soft", -20, None),
    ("night1", 4, [0.1], "cut_hit/sub", -9, None),
    ("delete", 0, [0.4, 1.1], "click/thock", -12, None),
    ("delete", 1, [0.2], "cut_hit/rumble", -16, None),               # เครื่องพิมพ์
    ("delete", 5, [0.1], "SUBDROP", -9, None),
    ("night2", 0, [0.2, 1.2, 2.2], "fit/tick/domino", -15, None),
    ("night2", 4, [0.4], "NOTIFY", -12, None),                       # กล่องข้อความเด้ง
    ("footprints", 1, [0.3, 1.0, 1.7, 2.4], "click/soft", -14, None),  # หยดน้ำ
    ("footprints", 4, [0.2], "cut_hit/sub", -8, None),
    ("sleepover", 3, [0.0], "WHOOSH", -10, None),
    ("sleepover", 4, [0.3], "cut_hit/sub", -9, None),
    ("search", 3, [1.5], "NOTIFY", -14, None),
    ("search", 5, [0.4], "swipe/paper", -12, None),
    ("visit", 1, [0.45], "impact/classic", -8, None),                # แก้วแตก
    ("flashback", 0, [0.0], "WHOOSH", -12, None),
    ("flashback", 5, [0.2], "SUBDROP", -10, None),
    ("night3", 0, [1.0], "click/thock", -10, None),                  # จอเปิดเอง
    ("night3", 3, [0.0], "cut_hit/sub", -7, None),
    ("night3", 5, [0.1, 0.7, 1.4], "click/snap", -12, None),          # ไฟกะพริบ
    ("night3", 6, [0.2, 0.45, 0.7, 0.95, 1.2, 1.45, 1.7], "knock/desk", -15, None),  # ฝ่ามือตบกระจก
    ("dusk", 1, [0.6], "cut_hit/rumble", -10, None),                 # ไฟดับ
    ("dusk", 4, [1.0], "cut_hit/sub", -8, None),                     # 33
    ("pond", 0, [0.2], "WHOOSH", -12, None),
    ("pond", 2, [0.2, 0.55, 0.9, 1.25, 1.6, 1.95], "knock/wood", -16, "C4"),  # วิ่ง
    ("rollcall", 6, [0.1], "SUBDROP", -10, None),                    # "มาค่ะ"
    ("found", 4, [1.3], "cut_hit/punch", -10, None),                 # ล้มตึง
    ("photo", 2, [0.0], "impact/classic", -7, None),                 # แฟลช
    ("photo", 2, [0.0], "WHOOSH", -10, None),
    ("after", 3, [0.0, 0.8], "NOTIFY", -15, None),
    ("cliff", 0, [0.2, 1.2, 2.2], "fit/tick/domino", -13, None),
    ("cliff", 1, [0.3], "swipe/paper", -9, None),
    ("cliff", 4, [0.4], "cut_hit/sub", -7, None),
    ("cliff", 6, [2.6], "SUBDROP", -8, None),
]
BELL = ("dusk", 2, 0.3, -14)   # ระฆังโรงเรียนดังเอง


def bell(dur=3.0):
    t = np.arange(int(dur * SR)) / SR
    y = sum(a * np.sin(2 * np.pi * f * t) * np.exp(-t * d) for f, a, d in
            ((620, 0.6, 1.2), (1545, 0.35, 2.0), (2480, 0.2, 3.0), (3390, 0.1, 4.0)))
    return (y * np.minimum(1.0, t / 0.004)).astype(np.float32)


def main():
    tl = json.load(open(os.path.join(BUILD, "timeline.json"), encoding="utf-8"))
    starts = {}
    for ln in tl["lines"]:
        starts.setdefault(ln["scene"], []).append(ln["start"])
    out = np.zeros(int((tl["duration"] + 2) * SR), np.float32)
    alias = {"NOTIFY": pick("notify"), "WHOOSH": pick("whoosh_fast"), "SUBDROP": pick("sub_drop")}

    def put(y, t0, db):
        i = int(t0 * SR)
        if i < len(out):
            out[i:i + len(y)] += (y * 10 ** (db / 20))[: len(out) - i]
    n = 0
    for scene, li, offs, sid, db, pitch in CUES:
        if scene not in starts or li >= len(starts[scene]):
            print("skip", scene, li)
            continue
        y = render(alias.get(sid, sid), pitch)
        for o in offs:
            put(y, starts[scene][li] + o, db)
            n += 1
    sc, li, off, db = BELL
    for k in range(3):   # ก๊ง ก๊ง ก๊ง
        put(bell(), starts[sc][li] + off + k * 0.9, db)
    peak = float(np.max(np.abs(out))) or 1.0
    if peak > 0.95:
        out *= 0.95 / peak
    sf.write(os.path.join(BUILD, "sfx.wav"), out, SR)
    print(f"sfx: {n} cues + bell -> {os.path.join(BUILD, 'sfx.wav')}")


if __name__ == "__main__":
    sys.exit(main())
