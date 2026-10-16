#!/usr/bin/env python3
"""Generate the README artwork for TREND-PREDICTOR.

Same design system as PARADIGMA (adapted from the Cal.com DESIGN.md, VoltAgent/awesome-design-md),
with PARADIGMA's light pink swapped for a light blue so the two skills read as a pair.
- White canvas, near-black ink for text, one sans-serif family.
- Display type at weight 600 with negative tracking.
- Soft-rounded cards (12-16px), 1px hairlines, no heavy shadows.
- Show the product (a requirement card from a report), not an illustration of it.

GitHub renders README images as <img>, so only system fonts are available.

    python3 tools/make_assets.py   -> writes assets/*.svg
"""
import math
import os
import random

OUT = os.path.join(os.path.dirname(__file__), "..", "assets")
SANS = "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"

C = dict(
    canvas="#FFFFFF",
    wash="#F4F8FD",       # surface-soft
    card="#E3EFFA",       # surface-card
    mist="#C9DDF2",       # hairline / strong surface
    sky="#8DB8E3",        # soft accent
    deep="#2F6FB5",       # data accent (curves, highlights)
    ink="#111111",
    body="#3D3D44",
    muted="#7A7A85",
)


def svg(w, h, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'role="img" aria-label="{title}" font-family="{SANS}">\n<title>{title}</title>\n{body}\n</svg>\n')


def t(x, y, s, size, fill, weight=400, anchor="start", extra=""):
    return (f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{fill}" '
            f'text-anchor="{anchor}" {extra}>{s}</text>')


def pill(x, y, label, fill, color, size=13, pad=12, h=26, weight=500):
    w = len(label) * size * 0.56 + pad * 2
    return (f'<rect x="{x}" y="{y}" width="{w:.0f}" height="{h}" rx="{h/2}" fill="{fill}"/>'
            + t(x + w / 2, y + h / 2 + size * 0.36, label, size, color, weight, "middle")), w


# ------------------------------------------------------------------ banner
def banner():
    W, H = 1280, 440
    b = [f'<rect width="{W}" height="{H}" rx="20" fill="{C["wash"]}"/>']
    b.append(t(72, 166, "TREND-PREDICTOR", 64, C["ink"], 600,
               extra='letter-spacing="-2" textLength="540" lengthAdjust="spacingAndGlyphs"'))
    b.append(t(74, 222, "Project the constraints your project", 24, C["body"]))
    b.append(t(74, 254, "depends on 5 and 10 years ahead, and", 24, C["body"]))
    b.append(t(74, 286, "see when it becomes feasible.", 24, C["body"]))
    x = 74
    for lab in ["Agent skill", "Claude Code", "OpenCode", "Codex"]:
        p, w = pill(x, 330, lab, C["canvas"], C["ink"], 14, 14, 32)
        b.append(f'<rect x="{x-0.5}" y="329.5" width="{w+1:.0f}" height="33" rx="16.5" fill="none" stroke="{C["mist"]}"/>')
        b.append(p)
        x += w + 10

    # right: a requirement card with a fan forecast
    X, Y, CW, CH = 668, 56, 548, 328
    b.append(f'<rect x="{X}" y="{Y+4}" width="{CW}" height="{CH}" rx="16" fill="{C["mist"]}" opacity="0.45"/>')
    b.append(f'<rect x="{X}" y="{Y}" width="{CW}" height="{CH}" rx="16" fill="{C["canvas"]}" stroke="{C["mist"]}"/>')
    b.append(t(X + 28, Y + 44, "Actuator cost per joint", 20, C["ink"], 600))
    b.append(t(X + 28, Y + 68, "USD, history and forecast with 80% range", 14, C["muted"]))
    gx0, gy0, gx1, gy1 = X + 28, Y + 92, X + CW - 28, Y + 236
    for i in range(4):
        y = gy0 + i * (gy1 - gy0) / 3
        b.append(f'<line x1="{gx0}" y1="{y:.1f}" x2="{gx1}" y2="{y:.1f}" stroke="{C["card"]}" stroke-width="1"/>')
    random.seed(7)
    split = gx0 + 0.55 * (gx1 - gx0)
    n = 10
    hist = []
    for i in range(n):
        x = gx0 + 8 + i * (split - gx0 - 8) / (n - 1)
        y = gy0 + 16 + i * 0.55 * (gy1 - gy0 - 30) / (n - 1) + random.uniform(-6, 6)
        hist.append((x, y))
    x0, y0 = hist[-1]
    fx = [x0 + k * (gx1 - x0) / 8 for k in range(9)]
    med = [y0 + k * 7.2 for k in range(9)]
    up = [m - 4 - 26 * math.sqrt(k / 8) for k, m in enumerate(med)]
    lo = [m + 4 + 26 * math.sqrt(k / 8) for k, m in enumerate(med)]
    band = " ".join(f"{x:.1f},{y:.1f}" for x, y in zip(fx, up)) + " " + " ".join(
        f"{x:.1f},{y:.1f}" for x, y in reversed(list(zip(fx, lo))))
    b.append(f'<polygon points="{band}" fill="{C["card"]}"/>')
    b.append(f'<polyline points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in zip(fx, med))}" fill="none" '
             f'stroke="{C["deep"]}" stroke-width="2" stroke-dasharray="6 5"/>')
    b.append(f'<polyline points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in hist)}" fill="none" stroke="{C["ink"]}" '
             f'stroke-width="2.2" stroke-linejoin="round"/>')
    for x, y in hist[::3] + [hist[-1]]:
        b.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.6" fill="{C["canvas"]}" stroke="{C["ink"]}" stroke-width="1.8"/>')
    ty = gy0 + 0.80 * (gy1 - gy0)
    b.append(f'<line x1="{gx0}" y1="{ty:.1f}" x2="{gx1}" y2="{ty:.1f}" stroke="{C["deep"]}" stroke-width="1.5"/>')
    b.append(t(gx0 + 4, ty - 8, "target from unit economics", 12, C["deep"]))
    b.append(f'<line x1="{split:.1f}" y1="{gy0}" x2="{split:.1f}" y2="{gy1}" stroke="{C["mist"]}" stroke-width="1"/>')
    b.append(t(gx0, gy1 + 20, "2010", 12, C["muted"]))
    b.append(t(split, gy1 + 20, "today", 12, C["muted"], 400, "middle"))
    b.append(t(gx1, gy1 + 20, "+10 y", 12, C["muted"], 400, "end"))
    sy = Y + 286
    stats = [("8%", "met by +5 y"), ("61%", "met by +10 y"), ("B", "data grade"), ("2031", "start building")]
    colw = (CW - 56) / 4
    for i, (big, small) in enumerate(stats):
        sx = X + 28 + i * colw
        b.append(t(sx, sy, big, 20, C["ink"], 600))
        b.append(t(sx, sy + 20, small, 12, C["muted"]))
    b.append(t(X + CW - 20, Y + CH + 30, "Illustrative example", 12, C["muted"], 400, "end"))
    return svg(W, H, "\n".join(b), "TREND-PREDICTOR: project the constraints your project depends on 5 and 10 years ahead, and see when it becomes feasible")


# ---------------------------------------------------------------- pipeline
STEPS = [
    ("Requirements", "What must be true, with targets"),
    ("History", "10+ years per curve, sourced"),
    ("Hindcast check", "Would it have worked before?"),
    ("Forecast", "Calibrated ranges, auto-repaired"),
    ("Dated events", "Laws, patents, factories, status"),
    ("Readiness", "TRL steps, judgment inputs"),
    ("Score", "Weakest link, start window"),
    ("Verify + report", "Fresh agent re-opens sources"),
]


def pipeline():
    W, H = 1200, 330
    b = [f'<rect width="{W}" height="{H}" rx="20" fill="{C["wash"]}"/>']
    cw, ch, gx, gy, x0, y0 = 264, 122, 24, 22, 36, 31
    for i, (name, desc) in enumerate(STEPS):
        r, c = divmod(i, 4)
        x, y = x0 + c * (cw + gx), y0 + r * (ch + gy)
        hl = i in (2, 6)
        b.append(f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="12" fill="{C["card"] if hl else C["canvas"]}" stroke="{C["mist"]}"/>')
        b.append(f'<circle cx="{x+36}" cy="{y+38}" r="15" fill="{C["deep"] if hl else C["card"]}"/>')
        b.append(t(x + 36, y + 43.5, str(i + 1), 15, C["canvas"] if hl else C["deep"], 600, "middle"))
        b.append(t(x + 22, y + 84, name, 19, C["ink"], 600))
        b.append(t(x + 22, y + 106, desc, 14, C["muted"]))
    return svg(W, H, "\n".join(b), "TREND-PREDICTOR in eight steps, from requirements to the report")


# ------------------------------------------------------------ feasibility
def feasibility():
    W, H = 900, 580
    b = [f'<rect width="{W}" height="{H}" rx="20" fill="{C["wash"]}"/>']
    b.append(t(48, 64, "Feasibility: laundry-folding home robot under $2,000", 20, C["ink"], 600))
    b.append(t(48, 90, "Probability each requirement is met", 14, C["muted"]))
    reqs = [("R1 Actuators ≤ $40 per joint", .08, .61, True),
            ("R2 Grasping model reaches TRL 9", .55, .88, False),
            ("R3 Safety standard published", .82, .95, False),
            ("R4 Battery ≥ 4 h at 300 W", .70, .93, False),
            ("R5 Buyers trust it in the home", .35, .62, False)]
    X0, BW, y = 330, 500, 128
    for name, p5, p10, weak in reqs:
        b.append(t(48, y + 22, name, 15, C["deep"] if weak else C["body"], 600 if weak else 400))
        b.append(f'<rect x="{X0}" y="{y+2}" width="{BW}" height="16" rx="8" fill="{C["canvas"]}" stroke="{C["mist"]}"/>')
        b.append(f'<rect x="{X0}" y="{y+2}" width="{BW*p5:.0f}" height="16" rx="8" fill="{C["sky"]}"/>')
        b.append(f'<rect x="{X0}" y="{y+22}" width="{BW}" height="16" rx="8" fill="{C["canvas"]}" stroke="{C["mist"]}"/>')
        b.append(f'<rect x="{X0}" y="{y+22}" width="{BW*p10:.0f}" height="16" rx="8" fill="{C["deep"]}"/>')
        b.append(t(X0 + BW + 10, y + 15, f"{p5:.0%}", 12, C["muted"]))
        b.append(t(X0 + BW + 10, y + 35, f"{p10:.0%}", 12, C["ink"], 600))
        if weak:
            p, w = pill(48, y + 30, "weakest link", C["card"], C["deep"], 11, 9, 20)
            b.append(p)
        y += 62
    lx = X0
    for lab, col in (("by +5 years", C["sky"]), ("by +10 years", C["deep"])):
        b.append(f'<rect x="{lx}" y="{y+6}" width="14" height="14" rx="4" fill="{col}"/>')
        b.append(t(lx + 22, y + 18, lab, 13, C["body"]))
        lx += 140
    y += 52
    b.append(f'<rect x="48" y="{y}" width="{W-96}" height="56" rx="12" fill="{C["canvas"]}" stroke="{C["mist"]}"/>')
    b.append(t(70, y + 34, "+5 y: UNLIKELY", 16, C["ink"], 600))
    b.append(t(250, y + 34, "+10 y: LONG SHOT (joint 29%, weakest R1 61%)", 16, C["ink"], 600))
    b.append(t(W - 70, y + 34, "start by 2031", 16, C["deep"], 600, "end"))
    return svg(W, H, "\n".join(b), "Feasibility chart: probability each requirement is met at +5 and +10 years, weakest link and verdict")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for f in os.listdir(OUT):
        if f.endswith(".svg"):
            os.remove(os.path.join(OUT, f))
    for name, fn in [("banner", banner), ("pipeline", pipeline), ("feasibility", feasibility)]:
        p = os.path.join(OUT, f"{name}.svg")
        open(p, "w").write(fn())
        print("wrote", os.path.relpath(p))
