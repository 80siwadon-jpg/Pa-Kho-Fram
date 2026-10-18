"""เอฟเฟกต์ที่ใช้ร่วมกันทุกตอน"""
import math

from gfx import BLUE, GOLD, GREY, H, INK, MINT, RED, W, e_out, hn, seg


def confetti(g, t, n=60, seed=3, t0=0.0):
    cols = [RED, BLUE, GOLD, MINT, GREY]
    for i in range(n):
        tt = t - t0 - 0.3 * (hn(i, seed + 9) * 0.5 + 0.5)
        if tt < 0:
            continue
        x = (hn(i, seed) * 0.5 + 0.5) * W + 40 * math.sin(tt * 3 + i)
        y = 250 + tt * (300 + 200 * (hn(i, seed + 1) * 0.5 + 0.5)) - 100
        if y > H:
            continue
        with g.at(x, y, 1, tt * 300 * hn(i, seed + 2)):
            g.rrect(-12, -7, 24, 14, 3, cols[i % len(cols)], 3)


def burst(g, x, y, t, t0, n=10, r=200, size=30, kind="spark", seed=5):
    tt = t - t0
    if tt < 0 or tt > 1.2:
        return
    k = e_out(seg(tt, 0, 0.7))
    a = 1 - seg(tt, 0.6, 1.2)
    with g.alpha(a):
        for i in range(n):
            ang = 2 * math.pi * i / n + hn(i, seed) * 0.3
            rr = r * k * (0.7 + 0.3 * hn(i, seed + 1))
            px, py = x + math.cos(ang) * rr, y + math.sin(ang) * rr + 120 * tt * tt
            if kind == "spark":
                g.sparkle(px, py, size * (1 - 0.5 * k))
            elif kind == "coin":
                g.coin(px, py, size, "$", tt * 400 + i * 30)
            elif kind == "oil":
                g.blob(px, py, size, size * 1.2, INK, 0, i)
