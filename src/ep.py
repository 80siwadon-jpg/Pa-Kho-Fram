"""คำสั่งรวมสำหรับทำแต่ละตอน (ลดขั้นตอนมือ):
  EPISODE=<ตอน> python3 src/ep.py verify <บทต้นฉบับ.txt>   ตรวจว่าบรรทัดใน script.py ตรงบทต้นฉบับทุกคำ + ประมาณความยาว
  EPISODE=<ตอน> python3 src/ep.py sheet [ทุกกี่วิ=3] [เริ่ม] [จบ]  เรนเดอร์ภาพนิ่ง แล้วรวมเป็นแผ่น build/<ตอน>/sheet_N.png
  EPISODE=<ตอน> python3 src/ep.py final [whisper]             เรนเดอร์ mp4 -> qa.py -> check_sync (แสดงเฉพาะบรรทัดที่ต้องดู)
"""
import importlib.util
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EP = os.environ.get("EPISODE", "alaska")
BUILD = os.path.join(ROOT, "build", EP)
WHISPER = "/tmp/claude-0/-home-user-Pa-Kho-Fram/65f45883-1f5d-52ad-a32b-20e3500913fa/scratchpad/models/sherpa-onnx-whisper-small"
SEC_PER_CHAR = 0.0705   # Enceladus Rapid fire, --tempo 1.1 (วัดจาก 3 ตอนล่าสุด)


def script_lines():
    spec = importlib.util.spec_from_file_location("s", os.path.join(ROOT, "episodes", EP, "script.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return [ln for _, lines in m.SCENES for ln in lines]


def verify(orig):
    norm = lambda s: re.sub(r"[\s​]", "", s)  # noqa: E731
    lines = script_lines()
    a, b = norm("".join(lines)), norm(open(orig, encoding="utf-8").read())
    n = sum(len(norm(ln)) for ln in lines)
    print(f"{len(lines)} บรรทัด, {n} ตัวอักษร ≈ {n * SEC_PER_CHAR:.0f} วิ (เพดาน 180)")
    if a == b:
        print("ตรงบทต้นฉบับทุกคำ ✓")
        return 0
    i = next(k for k in range(min(len(a), len(b))) if a[k] != b[k]) if a[:len(b)] != b[:len(a)] else min(len(a), len(b))
    print(f"ไม่ตรงที่ตัวอักษร {i}:\n  script : …{a[max(0, i - 20):i + 30]}\n  ต้นฉบับ: …{b[max(0, i - 20):i + 30]}")
    return 1


def grid(paths, out, cols=6, tw=360, th=640):
    from PIL import Image, ImageDraw, ImageFont
    font = ImageFont.truetype(os.path.join(ROOT, "assets/fonts/Kanit-Bold.ttf"), 26)
    rows = (len(paths) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tw, rows * (th + 34)), "white")
    d = ImageDraw.Draw(sheet)
    for i, (t, p) in enumerate(paths):
        x, y = (i % cols) * tw, (i // cols) * (th + 34)
        sheet.paste(Image.open(p).convert("RGB").resize((tw, th)), (x, y + 34))
        d.text((x + 8, y + 2), f"{t:g}s", fill=(0, 0, 0), font=font)
    sheet.save(out)


def sheet(step=3.0, t0=1.0, t1=None):
    tl = json.load(open(os.path.join(BUILD, "timeline.json"), encoding="utf-8"))
    t1 = t1 or tl["duration"] - 0.5
    ts = []
    t = t0
    while t <= t1:
        ts.append(round(t, 2))
        t += step
    subprocess.run([sys.executable, os.path.join(ROOT, "src/render.py"), "--still", *map(str, ts)], check=True,
                   stdout=subprocess.DEVNULL)
    paths = [(t, os.path.join(BUILD, f"still_{t:05.2f}.png")) for t in ts]
    outs = []
    for k in range(0, len(paths), 24):
        out = os.path.join(BUILD, f"sheet_{k // 24 + 1}.png")
        grid(paths[k:k + 24], out)
        outs.append(out)
    print("\n".join(outs))


def final(whisper=WHISPER):
    tl = json.load(open(os.path.join(BUILD, "timeline.json"), encoding="utf-8"))
    out = os.path.join(ROOT, "output", f"{EP}_1080p60.mp4")
    for f in os.listdir(os.path.join(ROOT, "output")):
        if f.startswith(EP + "_") and f.endswith(".mp4"):
            out = os.path.join(ROOT, "output", f)
    if len(sys.argv) > 3:
        out = sys.argv[3]
    py = sys.executable
    subprocess.run([py, os.path.join(ROOT, "src/render.py"), "--out", out], check=True)
    subprocess.run([py, os.path.join(ROOT, "src/qa.py"), out], check=False)
    r = subprocess.run([py, os.path.join(ROOT, "src/check_sync.py"), whisper], capture_output=True, text=True)
    lines = r.stdout.strip().splitlines()
    bad = [ln for ln in lines if ln.startswith("✗")]
    print(f"ซิงก์ซับ: {len(tl['lines']) - len(bad)}/{len(tl['lines'])} ✓  (บรรทัด ✗ ให้ดูว่าต้นคำที่ได้ยินตรงบทไหม)")
    print("\n".join(bad))


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "verify":
        sys.exit(verify(sys.argv[2]))
    elif cmd == "sheet":
        sheet(*map(float, sys.argv[2:5]))
    elif cmd == "final":
        final(*sys.argv[2:3])
    else:
        print(__doc__)
