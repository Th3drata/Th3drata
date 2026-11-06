"""Génère les SVG du README de profil (thèmes dark + light).
Usage : python3 assets/build.py  (depuis la racine du repo)
"""
import math
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).parent
SANS = "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, 'JetBrains Mono', Menlo, Consolas, monospace"

THEMES = {
    "dark": dict(bg="#0a0a0a", panel="#131315", line="#ffffff12", grid="#ffffff0b",
                 fg="#ededed", muted="#8b8b8b", soft="#c9c9c9", accent="#d4e157", dot="#ededed"),
    "light": dict(bg="#fafaf8", panel="#f1f1ee", line="#0000001a", grid="#0000000c",
                  fg="#0b0b0b", muted="#6b6b6b", soft="#333333", accent="#7a8c00", dot="#0b0b0b"),
}

MORPH = [("FR", "je développe"), ("PL", "rozwijam"), ("EN", "I develop"), ("DE", "ich entwickle")]


def globe(cx, cy, r, color, n=260, frames=36, dur=40):
    """Sphère de points (Fibonacci) qui tourne sur son axe vertical, animée en SMIL."""
    golden = math.pi * (3 - math.sqrt(5))
    tilt = math.radians(18)
    out = []
    for i in range(n):
        y = 1 - 2 * (i + 0.5) / n
        rad = math.sqrt(1 - y * y)
        lon0 = golden * i
        xs, ops, ys, rs = [], [], [], []
        for f in range(frames + 1):
            lon = lon0 + 2 * math.pi * f / frames
            x, z = rad * math.cos(lon), rad * math.sin(lon)
            # inclinaison de l'axe pour un rendu plus « globe »
            y2 = y * math.cos(tilt) - z * math.sin(tilt)
            z2 = y * math.sin(tilt) + z * math.cos(tilt)
            depth = (z2 + 1) / 2  # 0 = derrière, 1 = devant
            xs.append(f"{cx + r * x:.1f}")
            ys.append(f"{cy - r * y2:.1f}")
            ops.append(f"{0.08 + 0.82 * depth ** 1.6:.2f}")
            rs.append(f"{0.7 + 1.5 * depth:.2f}")
        out.append(
            f'<circle cx="{xs[0]}" cy="{ys[0]}" r="{rs[0]}" fill="{color}" opacity="{ops[0]}">'
            f'<animate attributeName="cx" dur="{dur}s" repeatCount="indefinite" values="{";".join(xs)}"/>'
            f'<animate attributeName="cy" dur="{dur}s" repeatCount="indefinite" values="{";".join(ys)}"/>'
            f'<animate attributeName="opacity" dur="{dur}s" repeatCount="indefinite" values="{";".join(ops)}"/>'
            f'<animate attributeName="r" dur="{dur}s" repeatCount="indefinite" values="{";".join(rs)}"/>'
            "</circle>"
        )
    return "".join(out)


def grid(w, h, step, color, fade_id):
    lines = [f'<path d="M{x} 0V{h}" />' for x in range(0, w + 1, step)]
    lines += [f'<path d="M0 {y}H{w}" />' for y in range(0, h + 1, step)]
    return f'<g stroke="{color}" stroke-width="1" mask="url(#{fade_id})">{"".join(lines)}</g>'


def header(t):
    W, H = 960, 320
    morph_css, morph_txt = [], []
    n, step = len(MORPH), 3.2
    for i, (code, word) in enumerate(MORPH):
        a, b = i / n * 100, (i + 1) / n * 100
        if i == 0:  # visible dès la première image (aperçus, captures)
            kf = f"0%,{b-2.5:.2f}%,100%{{opacity:1}}{b:.2f}%,97.5%{{opacity:0}}"
        else:
            kf = f"0%,{a:.2f}%,{b:.2f}%,100%{{opacity:0}}{a+2.5:.2f}%,{b-2.5:.2f}%{{opacity:1}}"
        morph_css.append(f"@keyframes m{i}{{{kf}}}.m{i}{{animation:m{i} {n*step}s infinite}}")
        morph_txt.append(
            f'<g class="m{i}"{"" if i == 0 else " opacity=\"0\""}><text x="64" y="256" font-family="{MONO}" font-size="15" fill="{t["accent"]}" letter-spacing="2">{code}</text>'
            f'<text x="102" y="256" font-family="{MONO}" font-size="15" fill="{t["soft"]}">{escape(word)}</text></g>'
        )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Oscar Albert, full-stack developer in Geneva">
<style>
{"".join(morph_css)}
@keyframes blink{{0%,49%{{opacity:1}}50%,100%{{opacity:0}}}}
.cur{{animation:blink 1.1s steps(1) infinite}}
@media (prefers-reduced-motion: reduce){{*{{animation:none!important}} .m1,.m2,.m3{{opacity:0}}}}
</style>
<defs>
  <linearGradient id="fade" x1="0" x2="1"><stop offset="0.35" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#fff"/></linearGradient>
  <mask id="gm"><rect width="{W}" height="{H}" fill="url(#fade)"/></mask>
  <clipPath id="clip"><rect width="{W}" height="{H}" rx="18"/></clipPath>
</defs>
<g clip-path="url(#clip)">
  <rect width="{W}" height="{H}" fill="{t["bg"]}"/>
  <path d="M400 0H690L530 {H}H240Z" fill="{t["panel"]}"/>
  {grid(W, H, 40, t["grid"], "gm")}
  <g opacity="0.95">{globe(765, 160, 118, t["dot"], n=220)}</g>
  <g><text x="64" y="96" font-family="{MONO}" font-size="13" letter-spacing="4.5" fill="{t["muted"]}">GENEVA · SWITZERLAND</text></g>
  <g><text x="60" y="170" font-family="{SANS}" font-size="78" font-weight="800" letter-spacing="-3" fill="{t["fg"]}">Oscar Albert</text></g>
  <g>
    <text x="64" y="212" font-family="{SANS}" font-size="23" font-weight="500" letter-spacing="-0.4" fill="{t["soft"]}">Full-stack developer<tspan fill="{t["accent"]}"> · </tspan>Maths &amp; CS at UNIGE</text>
  </g>
  {"".join(morph_txt)}
  <rect class="cur" x="64" y="268" width="10" height="2" fill="{t["accent"]}"/>
  <rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="18" fill="none" stroke="{t["line"]}"/>
</g>
</svg>'''


def pill(t, label, value, w):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="44" viewBox="0 0 {w} 44" role="img" aria-label="{escape(label)}: {escape(value)}">
<rect x="0.5" y="0.5" width="{w-1}" height="43" rx="22" fill="{t["panel"]}" stroke="{t["line"]}"/>
<circle cx="24" cy="22" r="3.5" fill="{t["accent"]}"/>
<text x="38" y="27" font-family="{MONO}" font-size="12" letter-spacing="1.5" fill="{t["muted"]}">{escape(label)}</text>
<text x="{38 + len(label) * 8.2 + 10:.0f}" y="27.5" font-family="{SANS}" font-size="14.5" font-weight="600" fill="{t["fg"]}">{escape(value)}</text>
</svg>'''


def wrap(text, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > width and cur:
            lines.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}".strip()
    lines.append(cur)
    return lines


def card(t, idx, name, kind, desc, chips):
    W, H = 440, 200
    lines = wrap(desc, 50)
    desc_svg = "".join(
        f'<text x="28" y="{104 + i * 20}" font-family="{SANS}" font-size="14" fill="{t["soft"]}">{escape(l)}</text>'
        for i, l in enumerate(lines[:3])
    )
    x, chip_svg = 28, []
    for c in chips:
        cw = len(c) * 7.2 + 20
        chip_svg.append(
            f'<rect x="{x}" y="154" width="{cw:.0f}" height="24" rx="12" fill="none" stroke="{t["line"]}"/>'
            f'<text x="{x + 10}" y="170.5" font-family="{MONO}" font-size="11.5" fill="{t["muted"]}">{escape(c)}</text>'
        )
        x += cw + 8
    assert len(lines) <= 2, (name, lines)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{escape(name)}: {escape(desc)}">
<defs><clipPath id="c"><rect width="{W}" height="{H}" rx="16"/></clipPath>
<linearGradient id="g" x1="0" x2="1" y1="0" y2="1"><stop offset="0" stop-color="{t["accent"]}" stop-opacity="0.10"/><stop offset="0.5" stop-color="{t["accent"]}" stop-opacity="0"/></linearGradient></defs>
<g clip-path="url(#c)">
<rect width="{W}" height="{H}" fill="{t["panel"]}"/>
<rect width="{W}" height="{H}" fill="url(#g)"/>
<text x="28" y="42" font-family="{MONO}" font-size="11.5" letter-spacing="2.5" fill="{t["accent"]}">{idx:02d}</text>
<text x="56" y="42" font-family="{MONO}" font-size="11.5" letter-spacing="2.5" fill="{t["muted"]}">{escape(kind.upper())}</text>
<text x="28" y="74" font-family="{SANS}" font-size="24" font-weight="700" letter-spacing="-0.6" fill="{t["fg"]}">{escape(name)}</text>
<text x="{W-28}" y="74" text-anchor="end" font-family="{SANS}" font-size="20" fill="{t["muted"]}">↗</text>
{desc_svg}
{"".join(chip_svg)}
<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="16" fill="none" stroke="{t["line"]}"/>
</g></svg>'''


def section(t, idx, title):
    W = 880
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="56" viewBox="0 0 {W} 56" role="img" aria-label="{escape(title)}">
<text x="0" y="34" font-family="{MONO}" font-size="13" letter-spacing="4" fill="{t["accent"]}">{idx}</text>
<text x="40" y="34" font-family="{MONO}" font-size="13" letter-spacing="4" fill="{t["muted"]}">{escape(title.upper())}</text>
<path d="M{56 + len(title) * 12.2:.0f} 29.5H{W}" stroke="{t["line"]}"/>
</svg>'''


def footer(t):
    W, H = 880, 120
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="oscaralbert.fr">
<defs><linearGradient id="f" x1="0" x2="1"><stop offset="0" stop-color="{t["accent"]}" stop-opacity="0"/><stop offset="0.5" stop-color="{t["accent"]}"/><stop offset="1" stop-color="{t["accent"]}" stop-opacity="0"/></linearGradient></defs>
<path d="M0 20H{W}" stroke="url(#f)" stroke-width="1"/>
<text x="{W/2}" y="72" text-anchor="middle" font-family="{SANS}" font-size="22" font-weight="700" letter-spacing="-0.5" fill="{t["fg"]}">Let's build something.</text>
<text x="{W/2}" y="100" text-anchor="middle" font-family="{MONO}" font-size="12.5" letter-spacing="3" fill="{t["muted"]}">OSCAR ALBERT · GENEVA · 2026</text>
</svg>'''


PILLS = [("WEB", "oscaralbert.fr"), ("IN", "LinkedIn"), ("MAIL", "oscar.albert@free.fr"), ("CV", "Resume")]

PROJECTS = [
    ("parseledger", "Parseledger", "Fintech · Web app",
     "Bank statements (PDFs, scans) to accounting-ready data, every figure checked to the cent.",
     ["TypeScript", "CSV · Excel · QBO · Xero"]),
    ("virtulouvre", "VirtuLouvre", "Game · Team project",
     "A 3D game in the Louvre: six night missions, with characters and sound all made in code.",
     ["Python", "OpenGL", "NumPy", "Trophées NSI"]),
    ("monetia", "Monetia", "iOS app",
     "A native personal finance app: income, expenses, budgets and multiple accounts.",
     ["Swift", "SwiftUI"]),
    ("securedroplite", "SecureDropLite", "Security · Web app",
     "Encrypted file sharing through a unique link, self-destructing after download or expiry.",
     ["Python", "Flask", "Encryption"]),
]

SECTIONS = [("about", "01", "About"), ("now", "02", "Now"), ("work", "03", "Selected work"), ("stack", "04", "Stack")]

for name, t in THEMES.items():
    (OUT / f"header-{name}.svg").write_text(header(t))
    (OUT / f"footer-{name}.svg").write_text(footer(t))
    for label, value in PILLS:
        w = round(38 + len(label) * 8.2 + 10 + len(value) * 8.4 + 26)
        (OUT / f"pill-{label.lower()}-{name}.svg").write_text(pill(t, label, value, w))
    for i, (slug, title, kind, desc, chips) in enumerate(PROJECTS, 1):
        (OUT / f"card-{slug}-{name}.svg").write_text(card(t, i, title, kind, desc, chips))
    for slug, idx, title in SECTIONS:
        (OUT / f"section-{slug}-{name}.svg").write_text(section(t, idx, title))
print("ok")
