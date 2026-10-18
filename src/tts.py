"""สร้างเสียงพากย์ไทยแบบออฟไลน์ (sherpa-onnx + Meta MMS Thai) ทีละบรรทัด
แล้ววางลงไทม์ไลน์ -> build/narration.wav + build/timeline.json

python3 src/tts.py --model models/vits-mms-tha --target 88
"""
import argparse
import json
import os
import sys
import wave

import numpy as np
import sherpa_onnx

sys.path.insert(0, os.path.dirname(__file__))
from script_data import SCENES  # noqa: E402

SR_OUT = 48000
LEAD_IN = 0.5       # วินาทีก่อนเริ่มพูดประโยคแรก
LINE_GAP = 0.15     # ช่องว่างระหว่างบรรทัด
SCENE_GAP = 0.4    # ช่องว่างระหว่างฉาก
TAIL = 1.8          # เผื่อท้ายคลิป


def load_tts(model_dir):
    cfg = sherpa_onnx.OfflineTtsConfig(
        model=sherpa_onnx.OfflineTtsModelConfig(
            vits=sherpa_onnx.OfflineTtsVitsModelConfig(
                model=os.path.join(model_dir, "model.onnx"),
                lexicon="",
                tokens=os.path.join(model_dir, "tokens.txt"),
            ),
            num_threads=4,
        )
    )
    return sherpa_onnx.OfflineTts(cfg)


def normalize(text):
    # โมเดลไม่มีตัว "ำ" ให้แยกเป็น นิคหิต + า
    return text.replace("ำ", "ํา")


def trim(x, thr=0.01):
    idx = np.where(np.abs(x) > thr)[0]
    if len(idx) == 0:
        return x
    a = max(idx[0] - 400, 0)
    b = min(idx[-1] + 800, len(x))
    return x[a:b]


def resample(x, sr_in, sr_out):
    n = int(round(len(x) * sr_out / sr_in))
    t_in = np.arange(len(x)) / sr_in
    t_out = np.arange(n) / sr_out
    return np.interp(t_out, t_in, x).astype(np.float32)


def synth_all(tts, speed):
    clips = []
    for scene, lines in SCENES:
        for disp, spoken in lines:
            a = tts.generate(normalize(spoken), sid=0, speed=speed)
            x = trim(np.array(a.samples, dtype=np.float32))
            clips.append((scene, disp, resample(x, a.sample_rate, SR_OUT)))
    return clips


def layout(clips):
    t = LEAD_IN
    prev_scene = None
    events = []
    for scene, disp, x in clips:
        if prev_scene is not None:
            t += SCENE_GAP if scene != prev_scene else LINE_GAP
        dur = len(x) / SR_OUT
        events.append({"scene": scene, "text": disp, "start": round(t, 3), "end": round(t + dur, 3)})
        t += dur
        prev_scene = scene
    return events, t + TAIL


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="models/vits-mms-tha")
    ap.add_argument("--target", type=float, default=88.0, help="ความยาวคลิปที่ต้องการ (วินาที)")
    ap.add_argument("--out", default="build")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)

    tts = load_tts(args.model)
    speed = 1.0
    for _ in range(4):
        clips = synth_all(tts, speed)
        events, total = layout(clips)
        print(f"speed={speed:.3f} total={total:.2f}s")
        if abs(total - args.target) < 1.0:
            break
        speech = sum(len(c[2]) for c in clips) / SR_OUT
        speed *= speech / max(speech + (args.target - total), 1.0)  # speed>1 = พูดเร็วขึ้น

    # ไทม์ไลน์ฉาก: ฉากเริ่มที่บรรทัดแรก ลบนิดหน่อยให้ภาพนำเสียง
    scenes = []
    for e in events:
        if not scenes or scenes[-1]["name"] != e["scene"]:
            scenes.append({"name": e["scene"], "start": max(e["start"] - 0.35, 0.0)})
    scenes[0]["start"] = 0.0
    for i, s in enumerate(scenes):
        s["end"] = scenes[i + 1]["start"] if i + 1 < len(scenes) else total

    buf = np.zeros(int(total * SR_OUT) + SR_OUT, dtype=np.float32)
    for (_, _, x), e in zip(clips, events):
        i = int(e["start"] * SR_OUT)
        buf[i:i + len(x)] += x
    buf = buf[: int(total * SR_OUT)]
    buf = buf / (np.max(np.abs(buf)) + 1e-9) * 0.9
    with wave.open(os.path.join(args.out, "narration.wav"), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR_OUT)
        w.writeframes((buf * 32767).astype(np.int16).tobytes())

    with open(os.path.join(args.out, "timeline.json"), "w", encoding="utf-8") as f:
        json.dump({"duration": round(total, 3), "speed": speed, "lines": events, "scenes": scenes},
                  f, ensure_ascii=False, indent=1)
    print(json.dumps(scenes, ensure_ascii=False))


if __name__ == "__main__":
    main()
