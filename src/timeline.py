"""วางคลิปเสียงทีละบรรทัดต่อกันแบบกระชับ -> build/narration.wav + build/timeline.json
ใช้ร่วมกันทั้งเสียง TTS (tts.py) และเสียงอัดเอง (voice.py)
"""
import json
import os
import wave

import numpy as np

SR = 48000
LEAD_IN = 0.3      # วินาทีก่อนเริ่มพูด
LINE_GAP = 0.08    # ช่องว่างระหว่างบรรทัด (สั้น = กระชับ)
SCENE_GAP = 0.18   # ช่องว่างระหว่างฉาก
TAIL = 1.2         # เผื่อท้ายคลิป


def build(clips, out_dir, line_gap=LINE_GAP, scene_gap=SCENE_GAP):
    """clips = [(scene, text, samples@48k float32), ...]"""
    os.makedirs(out_dir, exist_ok=True)
    t, prev, lines = LEAD_IN, None, []
    for scene, text, x in clips:
        if prev is not None:
            t += scene_gap if scene != prev else line_gap
        dur = len(x) / SR
        lines.append({"scene": scene, "text": text, "start": round(t, 3), "end": round(t + dur, 3)})
        t += dur
        prev = scene
    total = t + TAIL

    # ภาพนำเสียงเล็กน้อย
    scenes = []
    for ln in lines:
        if not scenes or scenes[-1]["name"] != ln["scene"]:
            scenes.append({"name": ln["scene"], "start": max(ln["start"] - 0.2, 0.0)})
    scenes[0]["start"] = 0.0
    for i, s in enumerate(scenes):
        s["end"] = scenes[i + 1]["start"] if i + 1 < len(scenes) else total

    buf = np.zeros(int(total * SR), np.float32)
    for (_, _, x), ln in zip(clips, lines):
        i = int(ln["start"] * SR)
        buf[i:i + len(x)] += x[: len(buf) - i]
    buf = buf / (np.max(np.abs(buf)) + 1e-9) * 0.9
    with wave.open(os.path.join(out_dir, "narration.wav"), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((buf * 32767).astype(np.int16).tobytes())
    with open(os.path.join(out_dir, "timeline.json"), "w", encoding="utf-8") as f:
        json.dump({"duration": round(total, 3), "lines": lines, "scenes": scenes}, f, ensure_ascii=False, indent=1)
    print(f"timeline: {len(lines)} lines, {total:.1f}s")
    return total
