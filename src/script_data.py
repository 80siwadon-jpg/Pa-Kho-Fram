"""โหลดบทของตอนที่เลือก: episodes/<EPISODE>/script.py  (env EPISODE, ค่าเริ่มต้น alaska)"""
import importlib.util
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EPISODE = os.environ.get("EPISODE", "alaska")
_path = os.path.join(ROOT, "episodes", EPISODE, "script.py")
_spec = importlib.util.spec_from_file_location(f"script_{EPISODE}", _path)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
# บรรทัดเป็น str ได้ (ข้อความซับ = ข้อความที่อ่าน) หรือ (ซับ, คำอ่านสำหรับ TTS ชั่วคราว)
SCENES = [(name, [ln if isinstance(ln, tuple) else (ln, ln.replace("\u200b", " ")) for ln in lines])
          for name, lines in _mod.SCENES]
HEADER = getattr(_mod, "HEADER", "วันนี้ในอดีต")
