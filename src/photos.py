"""ภาพถ่ายจริง (สถานที่/เหตุการณ์จริง) ใส่ในคลิป — เฉพาะภาพสาธารณสมบัติ/ครีเอทีฟคอมมอนส์จาก Wikimedia Commons

1) ระบุภาพใน episodes/<ตอน>/photos.json:
   [{"id": "pentagon", "file": "File:The Pentagon January 2008.jpg", "search": "Pentagon aerial"}, ...]
   (ลองชื่อไฟล์ก่อน ไม่เจอ/สัญญาอนุญาตไม่ผ่าน -> ค้นด้วย search แล้วเลือกภาพแรกที่สัญญาอนุญาตผ่าน)
2) EPISODE=<ตอน> python3 src/photos.py  -> ดาวน์โหลดไว้ assets/photos/<ตอน>/<id>.jpg + credits.json
3) ในฉาก: if not photo(g, "pentagon", x, y, w, h): <วาดการ์ตูนแทน>
   ภาพที่มีลิขสิทธิ์ (เช่นภาพข่าวรางวัล) ห้ามใช้ -> วาดเป็นการ์ตูนแทน
"""
import json
import os
import re
import sys
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EP = os.environ.get("EPISODE", "alaska")
DIR = os.path.join(ROOT, "assets", "photos", EP)
API = "https://commons.wikimedia.org/w/api.php"
OK_LICENSE = re.compile(r"^(public domain|pd|cc0|cc by(-sa)? [0-9.]+)", re.I)
UA = {"User-Agent": "PaKhoFram/1.0 (history shorts; educational)"}

_cache = {}
_credits = None


def _get(params):
    url = API + "?" + urllib.parse.urlencode({**params, "format": "json"})
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
        return json.load(r)


def _info(title):
    r = _get({"action": "query", "titles": title, "prop": "imageinfo", "iiprop": "url|extmetadata",
              "iiurlwidth": 1600})
    for p in r["query"]["pages"].values():
        if "imageinfo" in p:
            ii = p["imageinfo"][0]
            md = ii.get("extmetadata", {})
            val = lambda k: re.sub(r"<[^>]+>", "", md.get(k, {}).get("value", "")).strip()  # noqa: E731
            return {"url": ii.get("thumburl") or ii["url"], "license": val("LicenseShortName"),
                    "artist": val("Artist")[:80], "title": title}
    return None


def _search(q):
    r = _get({"action": "query", "list": "search", "srsearch": q, "srnamespace": 6, "srlimit": 15})
    return [s["title"] for s in r["query"]["search"] if s["title"].lower().endswith((".jpg", ".jpeg", ".png"))]


def fetch():
    spec = json.load(open(os.path.join(ROOT, "episodes", EP, "photos.json"), encoding="utf-8"))
    os.makedirs(DIR, exist_ok=True)
    credits = {}
    old = {}
    if os.path.exists(os.path.join(DIR, "credits.json")):
        old = json.load(open(os.path.join(DIR, "credits.json"), encoding="utf-8"))
    for item in spec:
        if os.path.exists(os.path.join(DIR, item["id"] + ".jpg")):   # มีไฟล์แล้ว (โหลดไว้ก่อน/เจ้าของช่องใส่เอง)
            credits[item["id"]] = old.get(item["id"]) or {"artist": item.get("credit", ""), "license": item.get("license", "")}
            print(f"= {item['id']}: มีไฟล์อยู่แล้ว")
            continue
        cands = ([item["file"]] if item.get("file") else []) + (_search(item["search"]) if item.get("search") else [])
        for title in cands:
            info = _info(title)
            if not info or not OK_LICENSE.match(info["license"]):
                print(f"  ข้าม {title} ({info and info['license']})")
                continue
            data = urllib.request.urlopen(urllib.request.Request(info["url"], headers=UA), timeout=60).read()
            with open(os.path.join(DIR, item["id"] + ".jpg"), "wb") as f:
                f.write(data)
            credits[item["id"]] = info
            print(f"✓ {item['id']}: {title} · {info['license']} · {info['artist']}")
            break
        else:
            print(f"✗ {item['id']}: ไม่พบภาพที่สัญญาอนุญาตใช้ได้")
    json.dump(credits, open(os.path.join(DIR, "credits.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def _load(pid):
    if pid not in _cache:
        p = os.path.join(DIR, pid + ".jpg")
        _cache[pid] = None
        if os.path.exists(p):
            from PIL import Image
            from gfx import _to_surface
            im = Image.open(p).convert("RGBA")
            surf, buf = _to_surface(im)   # buf ต้องอยู่คู่ surface (ข้อมูลภาพจริง)
            _cache[pid] = (surf, im.width, im.height, buf)
    return _cache[pid]


_spec = None


def portrait(name):
    """id ภาพจริงของบุคคลตามชื่อในป้ายชื่อ (photos.json: "tag") — ใช้โดย Draw.name_tag"""
    global _spec
    if _spec is None:
        p = os.path.join(ROOT, "episodes", EP, "photos.json")
        _spec = json.load(open(p, encoding="utf-8")) if os.path.exists(p) else []
    for item in _spec:
        if item.get("tag") == name and _load(item["id"]) is not None:
            return item["id"]
    return None


def credit(pid):
    global _credits
    if _credits is None:
        p = os.path.join(DIR, "credits.json")
        _credits = json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {}
    c = _credits.get(pid, {})
    who = c.get("artist") or "Wikimedia Commons"
    return f"ภาพจริง: {who} · {c.get('license', '')}".strip(" ·")


def photo(g, pid, x, y, w, h, rot=0.0, k=1.0, zoom=1.0, pan=(0.0, 0.0), label=None):
    """ภาพถ่ายจริงในกรอบขาว (โพลารอยด์) + เครดิต — x,y = กึ่งกลาง; k = สเกลเด้งเข้า; zoom/pan = เคนเบิร์นส์
    คืน False ถ้ายังไม่มีไฟล์ภาพ (ให้ฉากวาดการ์ตูนแทน)"""
    s = _load(pid)
    if s is None:
        return False
    if k <= 0:
        return True
    surf, iw, ih, _ = s
    import cairo
    from gfx import INK, GREY
    from people import _rr, _shade
    c = g.c
    pad, foot = 22, 84
    with g.at(x, y, k, rot):
        c.save()   # เงา
        _rr(c, -w / 2 - pad + 10, -h / 2 - pad + 14, w + 2 * pad, h + pad + foot, 10)
        c.set_source_rgba(0, 0, 0, 0.18)
        c.fill()
        c.restore()
        _rr(c, -w / 2 - pad, -h / 2 - pad, w + 2 * pad, h + pad + foot, 10)
        _shade(c, (1, 1, 1, 1), 5, 0.0)
        c.save()
        c.rectangle(-w / 2, -h / 2, w, h)
        c.clip()
        sc = max(w / iw, h / ih) * zoom
        c.translate(pan[0] * w * 0.1, pan[1] * h * 0.1)
        c.scale(sc, sc)
        c.set_source_surface(surf, -iw / 2, -ih / 2)
        c.get_source().set_filter(cairo.FILTER_GOOD)
        c.paint()
        c.restore()
        c.rectangle(-w / 2, -h / 2, w, h)
        c.set_source_rgba(*INK)
        c.set_line_width(3)
        c.stroke()
        if label:
            g.text(label, 0, h / 2 + 30, 38, "kanit", INK, maxw=w)
        g.text(credit(pid), 0, h / 2 + foot - 22, 20, "kanitm", GREY, maxw=w)
    return True


if __name__ == "__main__":
    fetch()
