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
from script_data import ELLIPSIS, SCENES, TAGS, TTS_PROMPT, VOICE  # noqa: E402

API = "https://generativelanguage.googleapis.com/v1beta"
PROMPT = """# AUDIO PROFILE: Thai history storyteller
## THE SCENE: A short vertical video about an event on this day in history.
### DIRECTOR'S NOTES
Style: Promo/hype. Energetic, exciting, makes viewers want to keep watching.
Pace: Rapid fire, but take a short clear pause at the end of every line.
Language: Thai.
#### TRANSCRIPT
{text}"""
PROMPT = TTS_PROMPT or PROMPT
SR_IN = 24000
PAUSE = "\n[short pause]\n"
MAX_CHARS = int(os.environ.get("TTS_MAX_CHARS", 1400))   # บางโมเดล (3.1-preview) รับก้อนยาวไม่ได้ -> ลดลง


STRICT = ("IMPORTANT: Start reading the transcript immediately. Read ONLY the transcript below, word for word, "
          "in order, exactly once. Do not add any introduction, commentary or extra words.\n")


def expected_seconds(text):
    """ความยาวเสียงโดยประมาณของบท (ไทย ~0.09 วิ/ตัวอักษร + ช่วงหยุดระหว่างบรรทัด)"""
    body = re.sub(r"\[[^\]]*\]", "", text)
    return len(body.replace(" ", "")) * 0.09 + body.count("\n") * 0.4


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
    for model in models:   # ไล่ตามลำดับที่ต้องการ: ใช้แคชของโมเดลนั้นถ้ามี ไม่งั้นขอใหม่ (ไม่ข้ามไปใช้แคชโมเดลอื่นก่อน)
        h = hashlib.sha1(f"{model}|{voice_name}|{PROMPT}|{text}".encode()).hexdigest()[:16]
        p = os.path.join(cache, h + ".wav")
        if os.path.exists(p):
            return p, model
        body = {
            "contents": [{"parts": [{"text": PROMPT.format(text=text)}]}],
            "generationConfig": {
                "responseModalities": ["AUDIO"],
                "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voice_name}}},
            },
        }
        pcm = None
        keys = list(key) if isinstance(key, list) else [key]
        for attempt in range(2):   # บางครั้งตอบกลับแบบไม่มีเสียง (finishReason SAFETY/OTHER) -> ลองใหม่ 1 ครั้ง
            r = None
            while keys:   # หลายคีย์ (GEMINI_API_KEYS): โควตาคีย์หนึ่งหมด -> ใช้คีย์ถัดไปกับโมเดลเดิม
                try:
                    r = call(f"models/{model}:generateContent", body, keys[0])
                    break
                except QuotaError:
                    print(f"  โควตารายวันของ {model} (คีย์ที่ใช้อยู่) หมด ลองคีย์ถัดไป")
                    keys.pop(0)
            if r is None:
                print(f"  โควตา {model} หมดทุกคีย์ ลองโมเดลถัดไป")
                break
            cand = r["candidates"][0]
            if "content" in cand:
                pcm = base64.b64decode(cand["content"]["parts"][0]["inlineData"]["data"])
                dur, exp = len(pcm) / 2 / SR_IN, expected_seconds(text)
                if dur > exp * 2.2 + 8 and attempt == 0:
                    # โมเดลพูดเกินบท (ด้นเนื้อหาเอง/อ่านซ้ำ) -> ขอใหม่ครั้งเดียวด้วยคำสั่งให้อ่านตามบทคำต่อคำ
                    print(f"  {model} ให้เสียงยาวผิดปกติ {dur:.0f}s (ควรราว {exp:.0f}s) ขอใหม่แบบอ่านตามบทเท่านั้น")
                    body["contents"][0]["parts"][0]["text"] = PROMPT.replace("#### TRANSCRIPT", STRICT + "#### TRANSCRIPT").format(text=text)
                    pcm = None
                    continue
                if dur > exp * 2.2 + 8:
                    print(f"  คำเตือน: เสียงยังยาวผิดปกติ {dur:.0f}s (ควรราว {exp:.0f}s) ตรวจด้วย check_sync")
                break
            print(f"  {model} ไม่ส่งเสียงกลับ ({cand.get('finishReason')}) ลองใหม่")
        if pcm is None:
            continue
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
    # ELLIPSIS ใน script.py (เช่น ",") = เก็บจังหวะหยุดสั้นตรง ... ไว้ให้เล่าเป็นธรรมชาติ
    return s.replace("...", ELLIPSIS or "").replace('"', "").replace("\u200b", "")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default=None, help="ไม่ระบุ = โมเดล TTS ใหม่สุด แล้วไล่ลงถ้าโควตาหมด")
    ap.add_argument("--voice", default=VOICE or "Enceladus")
    ap.add_argument("--tempo", type=float, default=1.0, help="เร่งความเร็วเพิ่ม เช่น 1.1")
    ap.add_argument("--gap", type=float, default=0.2, help="ช่วงหายใจระหว่างบรรทัด")
    ap.add_argument("--out", default=os.path.join("build", os.environ.get("EPISODE", "alaska")))
    a = ap.parse_args()
    key = os.environ.get("GEMINI_API_KEY")
    keys = [k.strip() for k in os.environ.get("GEMINI_API_KEYS", "").split(",") if k.strip()]
    if not key and not keys:
        sys.exit("ไม่พบ GEMINI_API_KEY")
    key = keys or key
    cache = os.path.join(a.out, "tts_cache")
    os.makedirs(cache, exist_ok=True)

    items = [(scene, disp) for scene, lines in SCENES for disp, _ in lines]
    models = [a.model] if a.model else tts_models(key[0] if isinstance(key, list) else key)

    # บทยาวเกิน ~1400 ตัวอักษร โมเดลส่งเสียงไม่จบ -> แบ่งเป็นก้อนตามฉาก (บทสั้นยังเป็นก้อนเดียว แคชเดิมใช้ได้)
    chunks, cur, n, gi = [], [], 0, 0
    for scene, lines in SCENES:
        size = sum(len(clean(d)) for d, _ in lines)
        if cur and n + size > MAX_CHARS:
            chunks.append(cur)
            cur, n = [], 0
        for d, _ in lines:   # แท็กกำกับอารมณ์นำหน้าบรรทัด (ถ้ามีใน script.py) ส่งให้โมเดล แต่ไม่ขึ้นซับ
            tg = TAGS[gi] if gi < len(TAGS) else ""
            cur.append((scene, (tg + " " + d) if tg else d, d))
            gi += 1
        n += size
    chunks.append(cur)

    # ทุกก้อนต้องใช้โมเดลเดียวกัน (เสียงจะได้สม่ำเสมอ): ถ้าโควตาหมดกลางทางจนต้องเปลี่ยนโมเดล
    # ให้สร้างก้อนก่อนหน้าใหม่ด้วยโมเดลที่ใช้ได้ (ก้อนที่แคชไว้แล้วไม่เสียโควตา)
    for _ in range(len(models)):
        used = []
        for chunk in chunks:
            texts = [clean(d) for _, d, _ in chunk]
            _, model = speak(PAUSE.join(texts), models, a.voice, key, cache)
            used.append(model)
            models = [model] + [m for m in models if m != model]
        if len(set(used)) == 1:
            break
        models = [used[-1]] + [m for m in models if m != used[-1]]
        print(f"  โมเดลไม่ตรงกันระหว่างก้อน {used} -> สร้างใหม่ทั้งหมดด้วย {used[-1]}")

    lines = []
    for ci, chunk in enumerate(chunks):
        texts = [clean(d) for _, d, _ in chunk]
        plain = [clean(d) for _, _, d in chunk]
        # แท็ก [short pause] ทำให้เกิดช่วงหยุดชัด ๆ ระหว่างบรรทัด (โมเดลไม่อ่านออกเสียง) -> ตัดบรรทัดได้แม่น
        path, model = speak(PAUSE.join(texts), models, a.voice, key, cache)
        models = [model] + [m for m in models if m != model]   # ใช้โมเดลเดียวกันทุกก้อน เสียงจะได้เหมือนกัน
        print(f"chunk {ci + 1}/{len(chunks)} model: {model} voice: {a.voice}")
        x = voice.load(path, a.tempo)
        runs = voice.speech_runs(x, min_gap=0.04)
        # WHISPER=<โฟลเดอร์ sherpa-onnx-whisper-small> = ขยับจุดตัดบรรทัดให้ตรงคำพูดจริง (บทที่มีจังหวะหยุดกลางบรรทัด)
        wdir = os.environ.get("WHISPER")
        ref = voice.WhisperRefiner(wdir, [d for _, _, d in chunk], span=int(os.environ.get("WHISPER_SPAN", 4))) if wdir else None
        labs = None
        if ref:   # ถอดเสียงจัดตำแหน่งเทียบบท (แคชผลไว้ ไม่ต้องถอดซ้ำทุกครั้ง)
            lk = os.path.join(cache, os.path.basename(path)[:-4] + f"_labels_{a.tempo}.json")
            if os.path.exists(lk):
                labs = json.load(open(lk))
            if not labs or len(labs) != len(runs):
                labs = voice.whisper_labels(x, runs, [d for _, _, d in chunk], ref)
                json.dump(labs, open(lk, "w"))
        lines += voice.split_lines(x, runs, [voice.weight(t) for t in plain], keep_gap=0.08, refine=ref, labels=labs)
    for (_, disp), y in zip(items, lines):
        print(f"  {len(y) / timeline.SR:4.1f}s  {disp}")
    timeline.build([(s, d, y) for (s, d), y in zip(items, lines)], a.out, a.gap, a.gap + 0.12)


if __name__ == "__main__":
    main()
