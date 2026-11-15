"""เสียงประกอบ (SFX) ของตอน funeral_photo จากคลังเสียงของ earshot (เสียงสร้างด้วยโค้ด ไม่ใช่เสียงบันทึกจริง)
EPISODE=funeral_photo python3 episodes/funeral_photo/sfx.py   -> build/funeral_photo/sfx.wav (วางตามเวลาบรรทัดพากย์)
ไซเรนตำรวจสังเคราะห์เอง (สองโทน) เพราะคลังไม่มี
"""
import json
import os
import subprocess
import sys

import numpy as np
import soundfile as sf

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
EP = os.environ.get("EPISODE", "funeral_photo")
BUILD = os.path.join(ROOT, "build", EP)
CACHE = os.path.join(BUILD, "sfx_cache")
SR = 48000

# (ฉาก, บรรทัดที่, [เวลาหลังต้นบรรทัด], id ในคลัง, dB, pitch)
CUES = [
    ("night1", 0, [0.3, 1.35, 2.4], "knock/wood", -16, "C4"),        # ฝีเท้าบนบันไดไม้
    ("night1", 1, [0.2, 1.2], "knock/wood", -16, "C4"),
    ("grandma", 3, [0.8], "click/snap", -12, None),                    # ไฟแช็ก
    ("retouch", 0, [0.5, 1.2, 1.6, 2.4], "click/soft", -20, None),     # คลิกเมาส์
    ("retouch", 1, [0.4, 1.0, 1.9, 2.6], "click/soft", -20, None),
    ("retouch", 3, [0.2, 1.2, 2.2], "fit/tick/domino", -14, None),    # นาฬิกา 02:15
    ("five", 1, [0.6, 1.6], "click/thock", -14, None),
    ("five", 2, [0.0, 0.9, 1.8], "fit/tick/domino", -13, None),       # หนึ่ง สอง สาม
    ("pupil", 3, [0.05], "cut_hit/sub", -9, None),                     # ตาหันมามอง
    ("envelope", 0, [0.2, 1.2, 2.2], "fit/tick/domino", -15, None),
    ("envelope", 1, [0.25], "swipe/paper", -9, None),                  # แซ่ก
    ("incense", 0, [0.6], "click/snap", -12, None),
    ("zoom", 1, [0.7, 1.7, 2.8], "click/thock", -11, None),            # 200 500 1000%
    ("reflection", 3, [0.6], "cut_hit/sub", -9, None),
    ("call", 4, [0.15], "click/double", -10, None),                    # วางสาย
    ("night3", 1, [1.6], "NOTIFY", -16, None),                         # ก๊อปเสร็จ
    ("night3", 4, [0.0], "knock/wood", -10, "C4"),                     # เอี๊ยด (บันไดขั้นแรก)
    ("bang", 0, [0.4, 1.4], "knock/desk", -14, None),                  # ลากโต๊ะ/ล็อกประตู
    ("bang", 1, [0.0, 0.45, 0.9], "cut_hit/punch", -5, None),          # ปัง ปัง ปัง
    ("bang", 1, [0.0, 0.45, 0.9], "knock/wood", -6, "C4"),
    ("crowbar", 2, [0.3], "cut_hit/rumble", -11, None),                # งัดประตู
    ("crowbar", 4, [0.0], "impact/classic", -5, None),                 # ประตูแตก
    ("knife", 0, [0.1], "WHOOSH", -10, None),
    ("flash", 0, [0.0], "impact/classic", -6, None),                   # แฟลช
    ("flash", 0, [0.0], "WHOOSH", -9, None),
    ("fall", 1, [0.4], "swish/flick", -10, None),                      # ส้นเท้าพลาด
    ("fall", 3, [0.0, 0.75], "cut_hit/punch", -5, None),               # โครม โครม
    ("ending", 4, [1.8, 3.4], "NOTIFY", -13, None),                    # โทรศัพท์ดัง
    ("ending", 8, [3.0], "SUBDROP", -8, None),                         # ตัดจบ
]
SIREN = ("fall", 4, -18, 7.0)   # ไซเรนตำรวจ: ฉาก บรรทัด dB ยาว(วิ)


def pick(category):
    out = subprocess.run(["earshot", "sfx", "list", "--category", category], capture_output=True, text=True).stdout
    rows = [ln.split()[0] for ln in out.splitlines()[2:] if ln.strip()]
    return rows[0]


def render(sid, pitch):
    os.makedirs(CACHE, exist_ok=True)
    key = (sid + ("_" + pitch if pitch else "")).replace("/", "__")
    p = os.path.join(CACHE, key + ".wav")
    if not os.path.exists(p):
        cmd = ["earshot", "sfx", "render", sid, "-o", p] + (["--pitch", pitch] if pitch else [])
        if subprocess.run(cmd, capture_output=True).returncode != 0:   # pitch นอกช่วงของเสียงนั้น -> ใช้โน้ตเดิม
            subprocess.run(["earshot", "sfx", "render", sid, "-o", p], check=True, capture_output=True)
    y, sr = sf.read(p, always_2d=True)
    y = y.mean(axis=1)
    if sr != SR:
        y = np.interp(np.linspace(0, len(y) - 1, int(len(y) * SR / sr)), np.arange(len(y)), y)
    return y.astype(np.float32)


def siren(dur):
    t = np.arange(int(dur * SR)) / SR
    f = np.where((t % 1.2) < 0.6, 960.0, 770.0)          # สองโทน hi-lo
    ph = 2 * np.pi * np.cumsum(f) / SR
    y = 0.6 * np.sin(ph) + 0.25 * np.sin(2 * ph)
    env = np.minimum(1.0, t / 3.0) * np.minimum(1.0, (dur - t) / 1.0)   # ค่อย ๆ ดังเข้ามาจากไกล
    lp = np.convolve(y * env, np.ones(24) / 24, mode="same")             # อู้อี้เหมือนอยู่ไกล
    return lp.astype(np.float32)


def main():
    tl = json.load(open(os.path.join(BUILD, "timeline.json"), encoding="utf-8"))
    starts = {}
    for ln in tl["lines"]:
        starts.setdefault(ln["scene"], []).append(ln["start"])
    out = np.zeros(int((tl["duration"] + 2) * SR), np.float32)
    alias = {"NOTIFY": pick("notify"), "WHOOSH": pick("whoosh_fast"), "SUBDROP": pick("sub_drop")}

    def put(y, t0, db):
        i = int(t0 * SR)
        if i >= len(out):
            return
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
    sc, li, db, dur = SIREN
    put(siren(dur), starts[sc][li], db)
    peak = float(np.max(np.abs(out))) or 1.0
    if peak > 0.95:
        out *= 0.95 / peak
    sf.write(os.path.join(BUILD, "sfx.wav"), out, SR)
    print(f"sfx: {n} cues + siren -> {os.path.join(BUILD, 'sfx.wav')}")


if __name__ == "__main__":
    sys.exit(main())
