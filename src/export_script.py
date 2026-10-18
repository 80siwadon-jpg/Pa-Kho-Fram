"""ส่งออกบทเป็นไฟล์ข้อความสำหรับวางในเครื่องมือสร้างเสียง -> output/script_<name>.txt
บรรทัดละ 1 ประโยค เว้นบรรทัดว่างระหว่างฉาก
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from script_data import SCENES  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
name = sys.argv[1] if len(sys.argv) > 1 else "clip"
path = os.path.join(ROOT, "output", f"script_{name}.txt")
os.makedirs(os.path.dirname(path), exist_ok=True)
with open(path, "w", encoding="utf-8") as f:
    f.write("\n\n".join("\n".join(d.replace("...", "") for d, _ in lines) for _, lines in SCENES) + "\n")
print(path, sum(len(lines) for _, lines in SCENES), "บรรทัด")
