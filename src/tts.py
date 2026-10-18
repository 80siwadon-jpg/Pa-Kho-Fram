"""เสียงพากย์ไทยแบบออฟไลน์ (sherpa-onnx + Meta MMS Thai) ใช้เป็นเสียงชั่วคราว
ถ้ามีเสียงอัดเองให้ใช้ voice.py แทน

python3 src/tts.py --model models/vits-mms-tha --speed 1.4
"""
import argparse
import os
import sys

import numpy as np
import sherpa_onnx

sys.path.insert(0, os.path.dirname(__file__))
import timeline  # noqa: E402
from script_data import SCENES  # noqa: E402


def trim(x, thr=0.01):
    idx = np.where(np.abs(x) > thr)[0]
    if len(idx) == 0:
        return x
    return x[max(idx[0] - 200, 0): min(idx[-1] + 400, len(x))]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="models/vits-mms-tha")
    ap.add_argument("--speed", type=float, default=1.4, help=">1 = พูดเร็วขึ้น")
    ap.add_argument("--out", default="build")
    a = ap.parse_args()
    tts = sherpa_onnx.OfflineTts(sherpa_onnx.OfflineTtsConfig(
        model=sherpa_onnx.OfflineTtsModelConfig(
            vits=sherpa_onnx.OfflineTtsVitsModelConfig(
                model=os.path.join(a.model, "model.onnx"), lexicon="",
                tokens=os.path.join(a.model, "tokens.txt")),
            num_threads=4)))
    clips = []
    for scene, lines in SCENES:
        for disp, spoken in lines:
            # โมเดลไม่มีตัว "ำ" ให้แยกเป็น นิคหิต + า
            r = tts.generate(spoken.replace("ำ", "ํา"), sid=0, speed=a.speed)
            x = trim(np.array(r.samples, np.float32))
            n = int(len(x) * timeline.SR / r.sample_rate)
            x = np.interp(np.linspace(0, len(x) - 1, n), np.arange(len(x)), x).astype(np.float32)
            clips.append((scene, disp, x))
    timeline.build(clips, a.out)


if __name__ == "__main__":
    main()
