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
TAGS = []   # แท็กกำกับอารมณ์ต่อบรรทัด (สำหรับ Gemini TTS) เช่น "[whispering] ก๊อก..." -> ซับไม่แสดงแท็ก


def _line(ln):
    import re
    disp, spoken = ln if isinstance(ln, tuple) else (ln, None)
    m = re.match(r"^((?:\[[^\]]*\]\s*)+)(.*)$", disp)
    TAGS.append(m.group(1).strip() if m else "")
    if m:
        disp = m.group(2)
    return disp, spoken if spoken is not None else disp.replace("\u200b", " ")


SCENES = [(name, [_line(ln) for ln in lines]) for name, lines in _mod.SCENES]
HEADER = getattr(_mod, "HEADER", "วันนี้ในอดีต")
# หน้าปกโพลารอยด์: {"date": "28 ตุลาคม 1886", "title": "...", "photo": "<id>" หรือไม่ใส่, "art": <วินาที>}
COVER = getattr(_mod, "COVER", None)
ELLIPSIS = getattr(_mod, "ELLIPSIS", None)      # แทน ... ในเสียง Gemini (ไม่ใส่ = ตัดทิ้งแบบเดิม)
VOICE = getattr(_mod, "VOICE", None)            # เสียง Gemini ของตอนนี้ (ไม่ใส่ = Enceladus ของช่อง)
TTS_PROMPT = getattr(_mod, "TTS_PROMPT", None)  # Director's notes ของตอนนี้ (ต้องมี {text})
