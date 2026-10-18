"""เสียงพากย์จริงของช่อง: Google Gemini TTS (เสียงเดียวกับ Google AI Studio)
เสียง Enceladus, สไตล์ Promo/hype, จังหวะ Rapid fire

ต้องมี env GEMINI_API_KEY
python3 src/gemini_tts.py [--model gemini-2.5-flash-preview-tts] [--voice Enceladus]

สร้างทีละฉาก (เสียงต่อเนื่องเป็นธรรมชาติ) แล้วแบ่งเป็นบรรทัดจากช่วงหยุด
ถ้าแบ่งไม่ได้ จะสร้างใหม่ทีละบรรทัดเฉพาะฉากนั้น  ผลลัพธ์ถูกแคชไว้ใน build/tts_cache
"""
import argparse
import base64
import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.request

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
import timeline  # noqa: E402
import voice  # noqa: E402
from script_data import SCENES  # noqa: E402

API = "https://generativelanguage.googleapis.com/v1beta"
STYLE = ("อ่านบทภาษาไทยต่อไปนี้ด้วยสไตล์ Promo/hype เร้าใจ ชวนติดตาม จังหวะเร็วแบบ rapid fire "
         "ออกเสียงตัวเลขปี ค.ศ. เป็นภาษาไทย และหยุดสั้น ๆ ให้ชัดเจนระหว่างแต่ละบรรทัด:")
SR_IN = 24000


def call(path, body=None, key=None, tries=5):
    req = urllib.request.Request(f"{API}/{path}", data=json.dumps(body).encode() if body else None,
                                 headers={"x-goog-api-key": key, "Content-Type": "application/json"})
    for i in range(tries):
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            msg = e.read().decode(errors="replace")[:300]
            if e.code in (429, 500, 503) and i < tries - 1:
                wait = 2 ** i * 5
                print(f"  HTTP {e.code} รอ {wait}s แล้วลองใหม่", flush=True)
                time.sleep(wait)
                continue
            sys.exit(f"Gemini API error {e.code}: {msg}")


def pick_model(key):
    names = [m["name"].split("/")[-1] for m in call("models?pageSize=200", key=key).get("models", [])]
    tts = sorted(n for n in names if "tts" in n)
    if not tts:
        sys.exit("ไม่พบโมเดล TTS ใน API key นี้")
    pro = [n for n in tts if "pro" in n]
    return (pro or tts)[-1]


def speak(text, model, voice_name, key, cache):
    h = hashlib.sha1(f"{model}|{voice_name}|{STYLE}|{text}".encode()).hexdigest()[:16]
    p = os.path.join(cache, h + ".npy")
    if os.path.exists(p):
        return np.load(p)
    body = {
        "contents": [{"parts": [{"text": f"{STYLE}\n{text}"}]}],
        "generationConfig": {
            "responseModalities": ["AUDIO"],
            "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voice_name}}},
        },
    }
    r = call(f"models/{model}:generateContent", body, key)
    data = base64.b64decode(r["candidates"][0]["content"]["parts"][0]["inlineData"]["data"])
    x = np.frombuffer(data, np.int16).astype(np.float32) / 32768
    n = int(len(x) * timeline.SR / SR_IN)
    x = np.interp(np.linspace(0, len(x) - 1, n), np.arange(len(x)), x).astype(np.float32)
    np.save(p, x)
    return x


def clean(s):
    return s.replace("...", "").replace('"', "").replace("ฯ", "")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default=None, help="ไม่ระบุ = เลือกโมเดล TTS ล่าสุดอัตโนมัติ")
    ap.add_argument("--voice", default="Enceladus")
    ap.add_argument("--gap", type=float, default=0.22, help="ช่วงหายใจระหว่างบรรทัด")
    ap.add_argument("--out", default="build")
    a = ap.parse_args()
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        sys.exit("ไม่พบ GEMINI_API_KEY")
    model = a.model or pick_model(key)
    print("model:", model, "voice:", a.voice)
    cache = os.path.join(a.out, "tts_cache")
    os.makedirs(cache, exist_ok=True)

    clips = []
    for scene, lines in SCENES:
        texts = [clean(d) for d, _ in lines]
        x = speak("\n".join(texts), model, a.voice, key, cache)
        runs = voice.speech_runs(x, min_gap=0.12)
        if len(runs) >= len(texts):
            parts = voice.split_lines(x, runs, len(texts), keep_gap=0.1)
        else:   # แบ่งไม่ได้ -> สร้างทีละบรรทัด
            print(f"  {scene}: แบ่งบรรทัดไม่ได้ ({len(runs)}/{len(texts)}) สร้างทีละบรรทัด")
            parts = []
            for t in texts:
                y = speak(t, model, a.voice, key, cache)
                rr = voice.speech_runs(y)
                parts.append(y[rr[0][0]: rr[-1][1]] if rr else y)
        for (disp, _), y in zip(lines, parts):
            print(f"  {len(y) / timeline.SR:4.1f}s  {disp}")
            clips.append((scene, disp, y))
    timeline.build(clips, a.out, a.gap, a.gap + 0.12)


if __name__ == "__main__":
    main()
