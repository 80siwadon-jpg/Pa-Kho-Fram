"""เสียงพากย์จริงของช่อง: Google Gemini TTS (เสียงเดียวกับ Google AI Studio)
เสียง Enceladus, สไตล์ Promo/hype, จังหวะ Rapid fire

ต้องมี env GEMINI_API_KEY
python3 src/gemini_tts.py [--tempo 1.1]

- ขอเสียงทั้งบทในครั้งเดียว (ฟรีเทียร์ได้ 10 ครั้ง/วัน/โมเดล) แคชไว้ใน build/tts_cache
- ใช้รูปแบบ "Director's notes" ไม่งั้นโมเดลจะอ่านคำสั่งสไตล์ออกเสียงไปด้วย
- โควตาโมเดลหนึ่งหมด -> ลองโมเดล TTS ถัดไปอัตโนมัติ
- แบ่งเสียงเป็นบรรทัดด้วย voice.split_lines (ช่วงหยุด + สัดส่วนความยาวข้อความ)
"""
import argparse
import base64
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
import wave

sys.path.insert(0, os.path.dirname(__file__))
import timeline  # noqa: E402
import voice  # noqa: E402
from script_data import SCENES  # noqa: E402

API = "https://generativelanguage.googleapis.com/v1beta"
PROMPT = """# AUDIO PROFILE: Thai history storyteller
## THE SCENE: A short vertical video about an event on this day in history.
### DIRECTOR'S NOTES
Style: Promo/hype. Energetic, exciting, makes viewers want to keep watching.
Pace: Rapid fire, but take a short clear pause at the end of every line.
Language: Thai.
#### TRANSCRIPT
{text}"""
SR_IN = 24000


class QuotaError(Exception):
    pass


def call(path, body=None, key=None, tries=4):
    req = urllib.request.Request(f"{API}/{path}", data=json.dumps(body).encode() if body else None,
                                 headers={"x-goog-api-key": key, "Content-Type": "application/json"})
    for i in range(tries):
        try:
            with urllib.request.urlopen(req, timeout=300) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            msg = e.read().decode(errors="replace")
            if e.code == 429 and "PerDay" in msg:
                raise QuotaError(path)
            if e.code in (429, 500, 503) and i < tries - 1:
                wait = 2 ** i * 5
                print(f"  HTTP {e.code} รอ {wait}s แล้วลองใหม่", flush=True)
                time.sleep(wait)
                continue
            sys.exit(f"Gemini API error {e.code}: {msg[:300]}")


def tts_models(key):
    """โมเดล TTS เรียงจากใหม่สุด (ตัวเต็มก่อน preview, ไม่เอา lite)"""
    names = [m["name"].split("/")[-1] for m in call("models?pageSize=200", key=key).get("models", [])]

    def rank(n):
        v = re.search(r"gemini-(\d+(?:\.\d+)?)", n)
        return (float(v.group(1)) if v else 0, "preview" not in n)
    return sorted((n for n in names if "tts" in n and "lite" not in n), key=rank, reverse=True)


def speak(text, models, voice_name, key, cache):
    """คืน (path ของ wav 24k, ชื่อโมเดลที่ใช้)"""
    for model in models:
        h = hashlib.sha1(f"{model}|{voice_name}|{PROMPT}|{text}".encode()).hexdigest()[:16]
        p = os.path.join(cache, h + ".wav")
        if os.path.exists(p):
            return p, model
    for model in models:
        body = {
            "contents": [{"parts": [{"text": PROMPT.format(text=text)}]}],
            "generationConfig": {
                "responseModalities": ["AUDIO"],
                "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voice_name}}},
            },
        }
        try:
            r = call(f"models/{model}:generateContent", body, key)
        except QuotaError:
            print(f"  โควตารายวันของ {model} หมด ลองโมเดลถัดไป")
            continue
        pcm = base64.b64decode(r["candidates"][0]["content"]["parts"][0]["inlineData"]["data"])
        h = hashlib.sha1(f"{model}|{voice_name}|{PROMPT}|{text}".encode()).hexdigest()[:16]
        p = os.path.join(cache, h + ".wav")
        with wave.open(p, "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(SR_IN)
            w.writeframes(pcm)
        return p, model
    sys.exit("โควตาฟรีของทุกโมเดล TTS หมดแล้ววันนี้ — รอรีเซ็ต (ประมาณ 14:00 เวลาไทย) หรือเปิด billing")


def clean(s):
    return s.replace("...", "").replace('"', "").replace("\u200b", "")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default=None, help="ไม่ระบุ = โมเดล TTS ใหม่สุด แล้วไล่ลงถ้าโควตาหมด")
    ap.add_argument("--voice", default="Enceladus")
    ap.add_argument("--tempo", type=float, default=1.0, help="เร่งความเร็วเพิ่ม เช่น 1.1")
    ap.add_argument("--gap", type=float, default=0.2, help="ช่วงหายใจระหว่างบรรทัด")
    ap.add_argument("--out", default="build")
    a = ap.parse_args()
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        sys.exit("ไม่พบ GEMINI_API_KEY")
    cache = os.path.join(a.out, "tts_cache")
    os.makedirs(cache, exist_ok=True)

    items = [(scene, disp) for scene, lines in SCENES for disp, _ in lines]
    texts = [clean(d) for _, d in items]
    models = [a.model] if a.model else tts_models(key)
    path, model = speak("\n".join(texts), models, a.voice, key, cache)
    print("model:", model, "voice:", a.voice)

    x = voice.load(path, a.tempo)
    runs = voice.speech_runs(x, min_gap=0.04)
    lines = voice.split_lines(x, runs, [voice.weight(t) for t in texts], keep_gap=0.08)
    for (_, disp), y in zip(items, lines):
        print(f"  {len(y) / timeline.SR:4.1f}s  {disp}")
    timeline.build([(s, d, y) for (s, d), y in zip(items, lines)], a.out, a.gap, a.gap + 0.12)


if __name__ == "__main__":
    main()
