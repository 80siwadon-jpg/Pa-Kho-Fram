"""สังเคราะห์ดนตรีประกอบ + เสียงเอฟเฟกต์การ์ตูน + เสียงฟิล์มเก่า แล้วมิกซ์กับเสียงพากย์
-> build/mix.wav   (ทุกอย่างสร้างด้วยโค้ด ไม่มีปัญหาลิขสิทธิ์)
"""
import json
import os
import wave

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUILD = os.path.join(ROOT, "build")
SR = 48000
RNG = np.random.default_rng(3)


def read_wav(p):
    with wave.open(p) as w:
        x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    return x


def tt(d):
    return np.arange(int(d * SR)) / SR


def env(n, a=0.005, r=0.2):
    t = np.arange(n) / SR
    e = np.minimum(t / a, 1.0) * np.exp(-t / r)
    return e.astype(np.float32)


def freq(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def lowpass(x, k=0.2):
    # one-pole low-pass ทำเป็น convolution กับ impulse response ที่ตัดปลาย
    n = int(4 / k)
    kern = k * (1 - k) ** np.arange(n)
    return np.convolve(x, kern)[: len(x)].astype(np.float32)


# ------------------------------------------------------------------ instruments
def pluck(m, d=0.6, bright=0.5):
    """Karplus-Strong แบบอูคูเลเล่"""
    f = freq(m)
    N = int(SR / f)
    n = int(d * SR)
    out = np.zeros(n, np.float32)
    buf = RNG.uniform(-1, 1, N).astype(np.float32)
    buf = lowpass(buf, bright)
    pos = 0
    while pos < n:
        k = min(N, n - pos)
        out[pos:pos + k] = buf[:k]
        nb = 0.5 * (buf + np.roll(buf, -1)) * 0.996
        buf = nb.astype(np.float32)
        pos += N
    return out * env(n, 0.002, d * 0.6)


def glock(m, d=0.9):
    t = tt(d)
    f = freq(m)
    x = np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t * 8) + 0.15 * np.sin(2 * np.pi * f * 5.4 * t) * np.exp(-t * 14)
    return (x * env(len(t), 0.002, 0.35)).astype(np.float32)


def bass(m, d=0.5):
    t = tt(d)
    f = freq(m)
    x = np.sin(2 * np.pi * f * t) + 0.3 * np.sin(2 * np.pi * 2 * f * t)
    return (x * env(len(t), 0.01, 0.25)).astype(np.float32)


def kick():
    t = tt(0.25)
    f = 110 * np.exp(-t * 25) + 45
    return (np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 14)).astype(np.float32)


def shaker():
    n = int(0.06 * SR)
    x = RNG.normal(0, 1, n).astype(np.float32)
    x = x - lowpass(x, 0.3)
    return x * env(n, 0.004, 0.02)


def pad(ms, d):
    t = tt(d)
    x = sum(np.sin(2 * np.pi * freq(m) * t + np.sin(2 * np.pi * 0.3 * t)) for m in ms) / len(ms)
    e = np.minimum(t / 0.4, 1) * np.minimum((d - t) / 0.4, 1)
    return (x * e).astype(np.float32)


def mx(*xs):
    """รวมเสียงหลายท่อนที่ยาวไม่เท่ากัน"""
    out = np.zeros(max(len(x) for x in xs), np.float32)
    for x in xs:
        out[: len(x)] += x
    return out


def add(buf, x, t, g=1.0):
    i = int(t * SR)
    if i >= len(buf) or i + len(x) <= 0:
        return
    if i < 0:
        x = x[-i:]
        i = 0
    j = min(len(buf), i + len(x))
    buf[i:j] += x[: j - i] * g


# ------------------------------------------------------------------ sfx
def sweep(f0, f1, d, wave_="sin", decay=None):
    t = tt(d)
    f = f0 * (f1 / f0) ** (t / d)
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = np.sin(ph) if wave_ == "sin" else np.sign(np.sin(ph)) * 0.5
    e = np.minimum(t / 0.005, 1) * (np.exp(-t / decay) if decay else np.minimum((d - t) / 0.03, 1))
    return (x * e).astype(np.float32)


def noise_burst(d, k=0.3, decay=0.1, hp=False):
    n = int(d * SR)
    x = RNG.normal(0, 1, n).astype(np.float32)
    x = x - lowpass(x, k) if hp else lowpass(x, k)
    return x * env(n, 0.003, decay)


def whoosh(d=0.45):
    n = int(d * SR)
    x = RNG.normal(0, 1, n).astype(np.float32)
    t = np.arange(n) / n
    out = np.zeros(n, np.float32)
    for i, k in enumerate(np.linspace(0.05, 0.5, 6)):
        a, b = i * n // 6, (i + 1) * n // 6
        out[a:b] = lowpass(x[a:b], k)
    return out * np.sin(np.pi * t) * 1.6


def SFX(name):
    if name == "pop":
        return sweep(300, 1100, 0.09, decay=0.04) * 0.8
    if name == "tick":
        return np.concatenate([noise_burst(0.03, 0.5, 0.01, True) * 0.6, np.zeros(int(0.12 * SR), np.float32),
                               noise_burst(0.03, 0.6, 0.01, True) * 0.4])
    if name == "boing":
        t = tt(0.55)
        f = 180 + 120 * np.sin(2 * np.pi * 9 * t) * np.exp(-t * 4) + 200 * t
        return (np.sin(2 * np.pi * np.cumsum(f) / SR) * env(len(t), 0.005, 0.25)).astype(np.float32) * 0.8
    if name == "flip":
        out = np.zeros(int(1.0 * SR), np.float32)
        for i in range(12):
            add(out, noise_burst(0.05, 0.4, 0.02, True) * 0.7, 0.07 * i + 0.02 * np.sin(i))
        return out
    if name == "scratch":
        t = tt(0.35)
        x = RNG.normal(0, 1, len(t)).astype(np.float32)
        f = 0.05 + 0.4 * np.abs(np.sin(2 * np.pi * 4 * t))
        return lowpass(x, 0.25) * (f * np.exp(-t * 3)).astype(np.float32) * 2.5
    if name == "stamp":
        return mx(kick() * 1.1, noise_burst(0.12, 0.15, 0.04) * 0.6)
    if name == "ding":
        return mx(glock(88, 1.2) * 0.5, glock(95, 1.2) * 0.25)
    if name == "whoosh":
        return whoosh() * 0.7
    if name == "sad":
        t = tt(1.2)
        out = np.zeros(len(t), np.float32)
        for i, m in enumerate([62, 61, 60, 59]):
            x = sweep(freq(m), freq(m) * (0.94 if i == 3 else 1), 0.28 if i < 3 else 0.6, "sq")
            add(out, lowpass(x, 0.15) * 0.8, i * 0.28)
        return out
    if name == "sneak":
        out = np.zeros(int(1.2 * SR), np.float32)
        for i, m in enumerate([45, 47, 48, 50]):
            add(out, pluck(m, 0.3, 0.3) * 0.9, i * 0.22)
        return out
    if name == "drop":
        return sweep(1200, 200, 0.35) * 0.4
    if name == "coins" or name == "coin":
        out = np.zeros(int(1.0 * SR), np.float32)
        for i in range(8 if name == "coins" else 2):
            add(out, (glock(100 + (i % 3) * 2, 0.3)) * 0.35, i * 0.07)
        return out
    if name == "laugh":   # "ฮ่า ๆ" แบบทรัมเป็ต/คาซู
        out = np.zeros(int(1.4 * SR), np.float32)
        for i in range(5):
            x = sweep(freq(67 - i), freq(65 - i), 0.18, "sq")
            add(out, lowpass(x, 0.12) * 0.7, i * 0.2)
        return out
    if name == "spin":
        return mx(whoosh(0.7) * 0.6, sweep(400, 900, 0.7) * 0.08)
    if name == "drum":   # กลองรัวพิธี
        out = np.zeros(int(1.6 * SR), np.float32)
        for i in range(24):
            add(out, noise_burst(0.05, 0.2, 0.02) * (0.25 + 0.5 * i / 24), i * 0.055)
        add(out, kick() * 1.0, 1.35)
        return out
    if name == "lower":
        return sweep(600, 380, 1.4) * 0.12
    if name == "climb":
        out = np.zeros(int(1.4 * SR), np.float32)
        for i in range(10):
            add(out, sweep(500 + i * 60, 700 + i * 60, 0.06, decay=0.03) * 0.35, i * 0.12)
        return out
    if name == "fall":
        return sweep(1500, 250, 0.7) * 0.25
    if name == "thud":
        return mx(kick() * 1.2, noise_burst(0.08, 0.3, 0.02, True) * 0.4)
    if name == "faint":   # slide whistle ลง
        t = tt(0.9)
        f = 1300 * (300 / 1300) ** (t / 0.9) * (1 + 0.02 * np.sin(2 * np.pi * 6 * t))
        return (np.sin(2 * np.pi * np.cumsum(f) / SR) * np.minimum((0.9 - t) / 0.05, 1) * np.minimum(t / 0.02, 1)).astype(np.float32) * 0.3
    if name == "fanfare":
        out = np.zeros(int(1.6 * SR), np.float32)
        for i, (m, d) in enumerate([(67, 0.15), (72, 0.15), (76, 0.15), (79, 0.8)]):
            x = sweep(freq(m), freq(m), d + 0.05, "sq")
            add(out, lowpass(x, 0.18) * 0.45, [0, 0.15, 0.3, 0.45][i])
        return out
    if name == "gold":
        out = np.zeros(int(1.4 * SR), np.float32)
        for i, m in enumerate([84, 88, 91, 96, 100]):
            add(out, glock(m, 0.8) * 0.35, i * 0.07)
        return out
    if name == "gush":
        n = int(1.8 * SR)
        x = lowpass(RNG.normal(0, 1, n).astype(np.float32), 0.06)
        t = np.arange(n) / SR
        return x * np.minimum(t / 0.1, 1) * np.exp(-t / 1.0) * 3.0
    if name == "reveal":
        return _reveal()
    if name == "party":
        out = np.zeros(int(1.0 * SR), np.float32)
        add(out, noise_burst(0.15, 0.4, 0.06, True) * 0.8, 0)
        add(out, SFX("gold") * 0.8, 0.05)
        return out
    raise KeyError(name)


def _reveal():
    d = 1.8
    out = pad([72, 76, 79, 84], d) * 0.28
    g = SFX("gold")
    add(out, g, 0.1)
    return out


# ------------------------------------------------------------------ music
# สเกล/คอร์ด (MIDI root ของคอร์ด)
MAJOR = [(48, [60, 64, 67]), (45, [57, 60, 64]), (41, [57, 60, 65]), (43, [55, 59, 62])]   # C Am F G
MINOR = [(45, [57, 60, 64]), (40, [55, 59, 64]), (41, [57, 60, 65]), (40, [56, 59, 64])]   # Am Em F E
MELODY = [[72, 76, 79, 76], [72, 69, 72, 76], [77, 76, 72, 69], [74, 71, 74, 79]]

# scene -> (drums, pluck, bass, glock, minor)
STYLE = {
    "hook": (0, 0.7, 0.0, 1.0, 0),
    "title": (1, 1, 1, 1, 0), "russia": (1, 1, 1, 0.6, 0), "deal": (1, 1, 1, 1, 0),
    "map": (1, 1, 1, 1, 0), "laugh": (1, 1, 1, 1, 0),
    "ceremony": (0, 0.5, 0.6, 0.0, 1), "calendar": (0.5, 1, 1, 1, 0),
    "twist": (1, 1, 1, 1, 0), "today": (1, 1, 1, 1, 0), "outro": (0.6, 1, 1, 1, 0),
}


def music(tl):
    dur = tl["duration"]
    buf = np.zeros(int((dur + 2) * SR), np.float32)
    bpm = 112
    beat = 60 / bpm
    nbeats = int(dur / beat) + 1

    def style_at(t):
        for s in tl["scenes"]:
            if s["start"] <= t < s["end"]:
                return s["name"], STYLE[s["name"]]
        return "outro", STYLE["outro"]

    for b in range(nbeats):
        t = b * beat
        name, (dr, pl, bs, gl, mi) = style_at(t)
        bar = b // 4
        pos = b % 4
        prog = MINOR if mi else MAJOR
        root, chord = prog[bar % 4]
        if name == "ceremony":
            # ช่วงพิธี: ช้าลงครึ่งหนึ่ง เศร้าและตึงเครียด
            if pos == 0:
                add(buf, pad([m - 12 for m in chord], beat * 4) * 0.22, t)
                add(buf, bass(root - 12, beat * 3) * 0.35, t)
            add(buf, pluck(chord[pos % 3] + 12, 0.5, 0.25) * 0.18, t)
            continue
        if bs and pos in (0, 2):
            add(buf, bass(root - 12 + (7 if pos == 2 else 0), beat * 1.6) * 0.38 * bs, t)
        if dr:
            if pos in (0, 2):
                add(buf, kick() * 0.5 * dr, t)
            add(buf, shaker() * 0.16 * dr, t + beat / 2)
            if pos in (1, 3):
                add(buf, noise_burst(0.12, 0.35, 0.05) * 0.18 * dr, t)   # snare เบา ๆ
        if pl:
            for h in range(2):
                m = chord[(pos * 2 + h) % 3] + (12 if h else 0)
                add(buf, pluck(m, 0.45, 0.45) * 0.26 * pl, t + h * beat / 2 + 0.004 * h)
        if gl and (bar % 2 == 0 or pos in (0, 2)):
            m = MELODY[bar % 4][pos]
            add(buf, glock(m, 0.8) * 0.13 * gl, t)
    # ending chord
    add(buf, pad([60, 64, 67, 72], 2.5) * 0.25, dur - 2.2)
    add(buf, glock(84, 2.0) * 0.25, dur - 2.2)
    return buf[: int(dur * SR)]


def film_noise(dur):
    n = int(dur * SR)
    hiss = lowpass(RNG.normal(0, 1, n).astype(np.float32), 0.5) * 0.010
    crackle = np.zeros(n, np.float32)
    idx = RNG.integers(0, n, int(dur * 18))
    crackle[idx] = RNG.uniform(-1, 1, len(idx)) * 0.25
    crackle = lowpass(crackle, 0.6)
    t = np.arange(n) / SR
    proj = (np.maximum(np.sin(2 * np.pi * 24 * t), 0) ** 30) * 0.012   # เสียงเครื่องฉายหมุน
    proj = lowpass(proj.astype(np.float32) * RNG.normal(1, 0.3, n).astype(np.float32), 0.3)
    return hiss + crackle + proj


def main():
    with open(os.path.join(BUILD, "timeline.json"), encoding="utf-8") as f:
        tl = json.load(f)
    with open(os.path.join(BUILD, "cues.json")) as f:
        cues = json.load(f)
    dur = tl["duration"]
    n = int(dur * SR)
    voice = read_wav(os.path.join(BUILD, "narration.wav"))[:n]
    voice = np.pad(voice, (0, n - len(voice)))

    mus = music(tl)
    mus = np.pad(mus, (0, max(0, n - len(mus))))[:n]
    # ducking: ลดเพลงลงเมื่อมีเสียงพูด
    venv = np.convolve(np.abs(voice), np.ones(2400) / 2400, mode="same")
    duck = 1.0 - 0.55 * np.clip(venv / 0.04, 0, 1)
    duck = np.convolve(duck, np.ones(4800) / 4800, mode="same")
    t = np.arange(n) / SR
    fade = np.clip((dur - t) / 1.5, 0, 1) ** 0.5
    mus *= duck * fade

    sfx = np.zeros(n + 3 * SR, np.float32)
    for c in cues:
        add(sfx, SFX(c["sfx"]), c["t"], 0.55)
    sfx = sfx[:n]

    mix = voice * 1.0 + mus * 0.55 + sfx + film_noise(dur)
    mix = np.tanh(mix * 1.1) / np.tanh(1.1)
    mix = mix / (np.max(np.abs(mix)) + 1e-9) * 0.95
    st = np.stack([mix, mix], 1)
    with wave.open(os.path.join(BUILD, "mix.wav"), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((st * 32767).astype(np.int16).tobytes())
    print("mix ->", os.path.join(BUILD, "mix.wav"), f"{dur:.2f}s")


if __name__ == "__main__":
    main()
