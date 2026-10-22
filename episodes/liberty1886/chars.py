"""ตัวละครและพร็อพ: พิธีเปิดอนุสาวรีย์เทพีเสรีภาพ (28 ต.ค. 1886)"""
import importlib.util
import math
import os

from gfx import GOLD, GOLD2, GREY, INK, NAVY, RED, WHITE, hexc, lerp
from people import Look, _rr, _shade, _smooth_path, _stroke


def _load(ep):
    spec = importlib.util.spec_from_file_location(f"{ep}_chars",
                                                  os.path.join(os.path.dirname(__file__), "..", ep, "chars.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


_b = _load("boeing707_1958")
liner, sea, cloud = _b.liner, _b.sea, _b.cloud

COPPER = hexc("#c8743a")
VERDIGRIS = hexc("#7fbfa8")
STONE = hexc("#d9cbb0")
WOOD = hexc("#c99a62")
FR_BLUE = hexc("#2b4f9a")

# โกรเวอร์ คลีฟแลนด์: ร่างใหญ่ ศีรษะล้านด้านบน หนวดดกห้อย หน้ากลม คอใหญ่ สูทดำ
CLEVELAND = Look(hair="bald", hair_col=hexc("#6b5a48"), suit=hexc("#1d1d21"), tie=INK, w=70, jaw=0.9, jowls=0.7,
                 nose=1.0, brow=0.9, age=0.5, build=1.35, facial="walrus", bowtie=True)
# โจเซฟ พูลิทเซอร์: ผอมสูง เคราแหลมสีน้ำตาลแดง แว่นหนีบจมูก จมูกโด่ง
PULITZER = Look(hair="part", hair_col=hexc("#8a4a2a"), suit=hexc("#2b2622"), tie=INK, w=56, jaw=0.3, nose=1.3,
                brow=1.0, age=0.4, build=0.9, height=1.04, facial="beard", glasses="thin")
# กุสตาฟ ไอเฟล: เคราและหนวดสีเทาขาวเต็มคาง ผมเทาหวีเรียบ
EIFFEL = Look(hair="part", hair_col=hexc("#b9b4aa"), suit=hexc("#3a3632"), tie=INK, w=60, jaw=0.6, age=0.6,
              facial="beard", bowtie=True)
IMMIGRANTS = [
    Look(hair="short", hair_col=hexc("#3a2a1e"), outfit="vest", suit=hexc("#6b5a48"), w=57, age=0.3,
         hat="bowler", facial="mustache"),
    Look(hair="bun", hair_col=hexc("#8a5a2a"), outfit="dress", suit=hexc("#7a4a5a"), w=54, age=0.2, height=0.93),
    Look(hair="short", hair_col=hexc("#c99a52"), outfit="vest", suit=hexc("#4a5a6a"), w=55, age=0.0, height=0.62,
         headsc=1.45),
    Look(hair="bun", hair_col=hexc("#2b2622"), outfit="dress", suit=hexc("#3a5a4a"), w=54, age=0.5, height=0.93),
]
DONORS = [
    Look(hair="short", hair_col=hexc("#3a2a1e"), outfit="vest", suit=hexc("#5a6a8a"), w=55, age=0.0, height=0.62,
         headsc=1.45),
    Look(hair="bun", hair_col=hexc("#a8763e"), outfit="dress", suit=hexc("#c8553d"), w=54, age=0.3, height=0.93),
    Look(hair="part", hair_col=hexc("#5a4632"), outfit="vest", suit=hexc("#6b5a48"), w=57, age=0.5, hat="bowler"),
]


def statue(g, x, y, sc=1.0, col=VERDIGRIS, t=0.0, torch=True, glow=0.0):
    """เทพีเสรีภาพ มองด้านหน้า (x,y = กึ่งกลางเท้า); ชูคบเพลิงมือขวา (ซ้ายจอ) ถือแผ่นจารึกมือซ้าย"""
    c = g.c
    dark = tuple(max(0, v * 0.75) for v in col[:3]) + (1,)
    with g.at(x, y, sc):
        if glow > 0:
            g.circle(-150, -1020, 90 + 10 * math.sin(t * 5), (1, 0.85, 0.3, 0.35 * glow), 0)
        # แขนขวาชูคบเพลิง
        _smooth_path(c, [(-80, -620), (-150, -880), (-170, -930), (-125, -940), (-100, -880), (-40, -640)])
        _shade(c, col, 6, 0.25)
        _rr(c, -168, -980, 36, 60, 8)
        _shade(c, col, 5, 0.2)
        _smooth_path(c, [(-185, -985), (-115, -985), (-125, -1005), (-175, -1005)])
        _shade(c, dark, 5, 0.1)
        if torch:
            f = 6 * math.sin(t * 7)
            g.poly([(-150, -1075 + f), (-122, -1015), (-150, -1000), (-178, -1015)], GOLD2, 5, amp=0, smooth=True)
        # เสื้อคลุม
        _smooth_path(c, [(-150, 0), (-125, -380), (-110, -620), (-60, -680), (60, -680), (110, -600), (130, -380),
                         (150, 0)])
        _shade(c, col, 7, 0.3)
        for k in range(5):
            xx = -100 + k * 50
            _stroke(c, [(xx - 10, -560 + 30 * (k % 2)), (xx, -300), (xx + 6, -20)], 3.5, dark, 0.8)
        _smooth_path(c, [(-120, -560), (40, -660), (120, -560), (-60, -470)])   # ผ้าพาดไหล่
        _shade(c, col, 5, 0.2)
        # แผ่นจารึก (มือซ้าย)
        with g.at(110, -470, 1, -18):
            _rr(c, -45, -110, 90, 180, 8)
            _shade(c, col, 5, 0.2)
            g.text("JULY IV", 0, -30, 18, "kanit", dark)
            g.text("MDCCLXXVI", 0, 0, 14, "kanit", dark)
        g.circle(92, -400, 22, col, 5)   # มือซ้าย
        # คอ + หัว + มงกุฎ 7 แฉก
        _rr(c, -26, -730, 52, 60, 12)
        _shade(c, col, 5, 0.2)
        for i in range(7):
            a = math.radians(-160 + i * 23.3)
            ex, ey = 150 * math.cos(a), -790 + 150 * math.sin(a)
            g.poly([(32 * math.cos(a - 0.15), -790 + 32 * math.sin(a - 0.15)), (ex, ey),
                    (32 * math.cos(a + 0.15), -790 + 32 * math.sin(a + 0.15))], col, 4, amp=0)
        c.new_path()
        c.save()
        c.translate(0, -780)
        c.scale(0.85, 1)
        c.arc(0, 0, 62, 0, 2 * math.pi)
        c.restore()
        _shade(c, col, 6, 0.25)
        _rr(c, -62, -838, 124, 34, 10)
        _shade(c, dark, 5, 0.1)
        for sx in (-1, 1):
            _stroke(c, [(sx * 24 - 10, -782), (sx * 24 + 10, -782)], 4, INK, smooth=False)
        _stroke(c, [(0, -775), (-4, -752), (4, -750)], 3, INK)
        _stroke(c, [(-12, -735), (12, -735)], 3.5, INK, smooth=False)


def pedestal(g, x, y, sc=1.0, k=1.0):
    """ฐานหินแกรนิต/คอนกรีต (k = ความสูงที่สร้างแล้ว 0..1)"""
    c = g.c
    with g.at(x, y, sc):
        h = 520 * k
        if h <= 2:
            return
        c.save()
        c.rectangle(-400, -h, 800, h + 4)
        c.clip()
        _smooth_path(c, [(-230, 0), (-200, -120), (-170, -520), (170, -520), (200, -120), (230, 0)])
        _shade(c, STONE, 7, 0.3)
        _rr(c, -200, -330, 400, 50, 6)
        _shade(c, STONE, 5, 0.2)
        for i in range(4):
            _rr(c, -130 + i * 70, -260, 40, 120, 4)
            _shade(c, hexc("#b8a88a"), 4, 0.1)
        for j in range(5):
            _stroke(c, [(-210, -40 - j * 22), (210, -40 - j * 22)], 2.5, INK, 0.25, smooth=False)
        c.restore()


def crate(g, x, y, sc=1.0, rot=0.0, label=""):
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -100, -170, 200, 170, 6)
        _shade(c, WOOD, 6, 0.25)
        for yy in (-120, -60):
            _stroke(c, [(-100, yy), (100, yy)], 3, INK, 0.5, smooth=False)
        _stroke(c, [(-100, -170), (100, 0)], 8, hexc("#a8784a"), smooth=False)
        if label:
            g.text(label, 0, -85, 34, "kanit", INK)


def statue_part(g, x, y, sc=1.0, kind="head", col=COPPER, rot=0.0):
    """ชิ้นส่วนรูปปั้น (หัว/มือ/คบเพลิง) สำหรับฉากขนส่ง"""
    c = g.c
    with g.at(x, y, sc, rot):
        if kind == "head":
            c.new_path()
            c.save()
            c.scale(0.85, 1)
            c.arc(0, 0, 100, 0, 2 * math.pi)
            c.restore()
            _shade(c, col, 6, 0.3)
            for i in range(5):
                a = math.radians(-150 + i * 30)
                g.poly([(60 * math.cos(a - 0.12), 60 * math.sin(a - 0.12)), (200 * math.cos(a), 200 * math.sin(a)),
                        (60 * math.cos(a + 0.12), 60 * math.sin(a + 0.12))], col, 4, amp=0)
            for sx in (-1, 1):
                _stroke(c, [(sx * 35 - 14, 0), (sx * 35 + 14, 0)], 5, INK, smooth=False)
        elif kind == "torch":
            _rr(c, -30, -40, 60, 200, 10)
            _shade(c, col, 5, 0.25)
            g.poly([(0, -170), (40, -60), (0, -40), (-40, -60)], GOLD2, 5, amp=0, smooth=True)


def tricolor(g, x, y, w, h, t=0.0):
    """ธงฝรั่งเศส (น้ำเงิน-ขาว-แดง) โบกเบา ๆ"""
    c = g.c
    for i, col in enumerate((FR_BLUE, WHITE, RED)):
        c.new_path()
        for p in [(x + i * w / 3, y + 6 * math.sin(t * 3 + i)), (x + (i + 1) * w / 3, y + 6 * math.sin(t * 3 + i + 1)),
                  (x + (i + 1) * w / 3, y + h + 6 * math.sin(t * 3 + i + 1)), (x + i * w / 3, y + h + 6 * math.sin(t * 3 + i))]:
            c.line_to(*p)
        c.close_path()
        _shade(c, col, 0, 0)
    c.rectangle(x, y - 6, w, h + 12)
    c.new_path()
    _stroke(c, [(x, y), (x, y + h)], 5, INK, smooth=False)


def rain(g, t, k=1.0, n=40):
    for i in range(n):
        u = (t * 1.3 + i * 0.137) % 1
        x = -100 + (i * 131) % 1300
        y = 150 + 1150 * u
        g.line([(x, y), (x - 14, y + 44)], 3, (0.45, 0.55, 0.7, 0.55 * k), amp=0)


def fog(g, t, k=1.0):
    for i in range(4):
        x = 540 + 500 * math.sin(t * 0.2 + i * 1.7)
        g.blob(x, 500 + i * 230, 520, 90, (0.85, 0.87, 0.9, 0.45 * k), 0, seed=i)


def newspaper(g, x, y, sc=1.0, rot=0.0, head="THE WORLD"):
    c = g.c
    with g.at(x, y, sc, rot):
        _rr(c, -230, -300, 460, 600, 6)
        _shade(c, hexc("#f4eedf"), 6, 0.1)
        g.text(head, 0, -240, 60, "kanit", INK)
        _stroke(c, [(-200, -200), (200, -200)], 4, INK, smooth=False)
        g.text("$100,000", 0, -140, 56, "kanit", RED)
        for i in range(7):
            _stroke(c, [(-200, -70 + i * 40), (i % 2 * 60 + 140, -70 + i * 40)], 4, GREY, 0.6, smooth=False)
        statue(g, 140, 270, 0.17, COPPER)


def coin(g, x, y, r=40, rot=0.0):
    with g.at(x, y, 1, rot):
        g.circle(0, 0, r, GOLD, 5)
        g.circle(0, 0, r * 0.7, GOLD2, 3)
        g.text("¢", 0, 0, int(r), "kanit", INK)


def jar(g, x, y, sc=1.0, fill=0.0):
    """โหลรับบริจาค"""
    c = g.c
    with g.at(x, y, sc):
        _smooth_path(c, [(-110, 0), (-130, -200), (-90, -260), (90, -260), (130, -200), (110, 0)])
        c.set_source_rgba(0.85, 0.92, 0.98, 0.8)
        c.fill_preserve()
        c.set_source_rgba(*INK)
        c.set_line_width(6)
        c.stroke()
        hh = 230 * fill
        if hh > 0:
            for i in range(int(fill * 18)):
                g.circle(-80 + (i % 5) * 40, -20 - (i // 5) * 40, 20, GOLD, 3)
        _rr(c, -100, -290, 200, 34, 8)
        _shade(c, hexc("#3a3f48"), 4, 0.1)


def iron_frame(g, x, y, sc=1.0, k=1.0):
    """โครงเหล็กภายใน (เสากลาง + โครงถัก) แบบไอเฟล"""
    c = g.c
    with g.at(x, y, sc):
        H = 900 * k
        for sx in (-1, 1):
            _stroke(c, [(sx * 70, 0), (sx * 40, -H)], 10, hexc("#7a4a2a"), smooth=False)
        for i in range(int(12 * k)):
            yy = -i * 75
            w = 70 - 30 * (i * 75) / 900
            _stroke(c, [(-w, yy), (w, yy - 75)], 5, hexc("#7a4a2a"), smooth=False)
            _stroke(c, [(w, yy), (-w, yy - 75)], 5, hexc("#7a4a2a"), smooth=False)
            for sx in (-1, 1):
                _stroke(c, [(sx * w, yy - 40), (sx * (w + 120), yy - 60)], 3, hexc("#a8683a"), 0.7, smooth=False)


def eiffel_tower(g, x, y, sc=1.0):
    c = g.c
    with g.at(x, y, sc):
        _smooth_path(c, [(-200, 0), (-60, -400), (-20, -800), (20, -800), (60, -400), (200, 0), (120, 0), (0, -200),
                         (-120, 0)])
        _shade(c, hexc("#8a6a4a"), 6, 0.2)
        _rr(c, -110, -330, 220, 26, 4)
        _shade(c, hexc("#7a5a3a"), 4, 0)
        _rr(c, -60, -560, 120, 20, 4)
        _shade(c, hexc("#7a5a3a"), 4, 0)


def chains(g, x, y, sc=1.0, broken=1.0):
    """โซ่ตรวนที่ขาด (สัญลักษณ์การสิ้นสุดระบอบทาส)"""
    with g.at(x, y, sc):
        for i in range(6):
            off = (i - 2.5) * 70
            gap = 40 * broken if i in (2, 3) else 0
            xx = off + (gap if i >= 3 else -gap)
            with g.at(xx, 0, 1, 90 if i % 2 else 0):
                g.c.new_path()
                g.c.save()
                g.c.scale(1, 0.6)
                g.c.arc(0, 0, 40, 0, 2 * math.pi)
                g.c.restore()
                g.c.set_source_rgba(*GREY)
                g.c.set_line_width(14)
                g.c.stroke()


def skyline(g, y, t=0.0):
    """เส้นขอบฟ้านิวยอร์กยุค 1880 (เตี้ย ๆ) ไกล ๆ"""
    c = g.c
    for i in range(9):
        x = 120 + i * 95
        h = 60 + (i * 37) % 80
        _rr(c, x, y - h, 70, h, 2)
        _shade(c, hexc("#c9cdd2"), 3, 0)
