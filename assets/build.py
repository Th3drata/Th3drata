"""Génère les SVG du README de profil (thèmes dark + light), style suisse.
Usage : python3 assets/build.py  (depuis la racine du repo)
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).parent
SANS = "'Helvetica Neue', Helvetica, Arial, 'Inter', sans-serif"

THEMES = {
    "dark": dict(bg="#111111", fg="#f2f2f2", muted="#8c8c8c", rule="#f2f2f2", hair="#ffffff26", red="#ff3b30"),
    "light": dict(bg="#ffffff", fg="#111111", muted="#6e6e6e", rule="#111111", hair="#00000022", red="#e30613"),
}


def svg(w, h, label, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'role="img" aria-label="{escape(label)}">{body}</svg>')


def text(x, y, s, size, fill, weight=400, ls=0, anchor="start", dot=None):
    # dot : couleur d'un point final intégré au texte (suit la police, quelle qu'elle soit)
    tail = f'<tspan fill="{dot}">.</tspan>' if dot else ""
    return (f'<text x="{x}" y="{y}" font-family="{SANS}" font-size="{size}" font-weight="{weight}" '
            f'letter-spacing="{ls}" fill="{fill}" text-anchor="{anchor}">{escape(s)}{tail}</text>')


def header(t):
    W, H = 880, 380
    facts = [("Role", "Full-stack developer"), ("Based in", "Geneva, Switzerland"),
             ("Studying", "BSc Maths & CS, UNIGE"), ("Running", "Belvédère, web studio")]
    col = 560
    rows = "".join(
        f'<path d="M{col} {108 + i * 58}H{W}" stroke="{t["hair"]}"/>'
        + text(col, 130 + i * 58, k.upper(), 11, t["muted"], 500, 1.6)
        + text(col, 152 + i * 58, v, 17, t["fg"], 500, -0.2)
        for i, (k, v) in enumerate(facts)
    )
    body = (
        # ponytail: fond transparent, se fond dans celui de GitHub (dark comme light)
        f'<rect x="0" y="20" width="22" height="22" fill="{t["red"]}"/>'
        + text(36, 37, "PROFILE", 12, t["fg"], 700, 3)
        + text(W, 37, "2026", 12, t["muted"], 500, 3, "end")
        + f'<path d="M0 66H{W}" stroke="{t["rule"]}" stroke-width="3"/>'
        + text(-1, 196, "Oscar", 128, t["fg"], 700, -7)
        + text(-1, 308, "Albert", 128, t["fg"], 700, -7, dot=t["red"])
        + rows
        + f'<path d="M0 {H - 30}H{W}" stroke="{t["hair"]}"/>'
        + text(0, H - 8, "Websites and web apps, from the first mockup to production.", 12, t["muted"], 500, 0.4)
    )
    return svg(W, H, "Oscar Albert, full-stack developer in Geneva", body)


def link(t, n, label):
    w = 30 + len(label) * 9.6 + 34
    body = (f'<path d="M0 1.5H{w}" stroke="{t["rule"]}" stroke-width="3"/>'
            + text(0, 30, f"{n:02d}", 11, t["red"], 700, 1)
            + text(26, 31, label, 16, t["fg"], 600, -0.2)
            + text(w, 31, "↗", 15, t["muted"], 400, 0, "end"))
    return svg(round(w) + 1, 42, label, body)


def section(t, idx, title):
    W = 880
    body = (f'<path d="M0 1.5H{W}" stroke="{t["rule"]}" stroke-width="3"/>'
            + text(0, 52, idx, 40, t["red"], 700, -1.5)
            + text(70, 52, title, 40, t["fg"], 700, -1.5))
    return svg(W, 72, title, body)


def wrap(s, width):
    out, cur = [], ""
    for w in s.split():
        if cur and len(cur) + len(w) + 1 > width:
            out.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}".strip()
    return out + [cur]


def card(t, idx, name, kind, desc, stack):
    W, H = 430, 230
    lines = wrap(desc, 48)
    assert len(lines) <= 3, (name, lines)
    body = (
        f'<path d="M0 1.5H{W}" stroke="{t["rule"]}" stroke-width="3"/>'
        + text(0, 40, f"{idx:02d}", 13, t["red"], 700, 1)
        + text(34, 40, kind.upper(), 11, t["muted"], 500, 1.6)
        + text(W, 40, "↗", 16, t["muted"], 400, 0, "end")
        + text(-2, 92, name, 38, t["fg"], 700, -1.6)
        + "".join(text(0, 128 + i * 21, l, 15, t["fg"], 400, -0.1) for i, l in enumerate(lines))
        + f'<path d="M0 {H - 34}H{W}" stroke="{t["hair"]}"/>'
        + text(0, H - 12, "  /  ".join(stack), 12, t["muted"], 500, 0.6)
    )
    return svg(W, H, f"{name}: {desc}", body)


def footer(t):
    W, H = 880, 200
    body = (
        f'<path d="M0 1.5H{W}" stroke="{t["rule"]}" stroke-width="3"/>'
        + text(-3, 92, "Let's work", 64, t["fg"], 700, -3)
        + text(-3, 160, "together", 64, t["fg"], 700, -3, dot=t["red"])
        + text(W, 128, "oscar.albert@free.fr", 17, t["fg"], 600, -0.2, "end")
        + text(W, 154, "oscaralbert.fr", 17, t["muted"], 500, -0.2, "end")
        + f'<path d="M0 {H - 18}H{W}" stroke="{t["hair"]}"/>'
        + text(0, H - 2, "OSCAR ALBERT", 10.5, t["muted"], 600, 2.5)
        + text(W, H - 2, "GENEVA", 10.5, t["muted"], 600, 2.5, "end")
    )
    return svg(W, H, "Let's work together: oscar.albert@free.fr", body)


def stack(t):
    W, H = 880, 210
    cols = [("Web", ["TypeScript", "JavaScript", "React", "Next.js", "Node.js", "Supabase", "SQL"]),
            ("Languages", ["Swift", "Python", "C", "C++", "Bash"]),
            ("Tools", ["Git", "Vercel", "Linux", "Docker (basics)", "OpenAI & Anthropic APIs"]),
            ("Speaks", ["French, native", "Polish, native", "English, B2", "German, B2"])]
    cw = W / len(cols)
    body = "".join(
        text(round(i * cw), 22, head.upper(), 11, t["red"], 700, 1.6)
        + "".join(text(round(i * cw), 54 + j * 22, item, 15, t["fg"], 400, -0.1) for j, item in enumerate(items))
        for i, (head, items) in enumerate(cols)
    )
    return svg(W, H, "Stack: " + "; ".join(h + ": " + ", ".join(it) for h, it in cols), body)


LINKS = [("web", "Website"), ("in", "LinkedIn"), ("mail", "Email"), ("cv", "Resume")]

PROJECTS = [
    ("parseledger", "Parseledger", "Fintech web app",
     "Turns bank statements (PDFs and scans) into accounting-ready data, with every figure checked to reconcile to the cent.",
     ["TypeScript", "CSV", "Excel", "QBO", "Xero"]),
    ("virtulouvre", "VirtuLouvre", "3D game, team project",
     "A 3D game set in the Louvre: six night missions, with every character, texture and sound generated in code.",
     ["Python", "OpenGL", "NumPy", "Trophées NSI"]),
    ("monetia", "Monetia", "iOS app",
     "A native personal finance app: income and expenses, budgets and multiple accounts.",
     ["Swift", "SwiftUI"]),
    ("securedroplite", "SecureDropLite", "Security web app",
     "Encrypted file sharing through a unique link, self-destructing after download or expiry.",
     ["Python", "Flask", "Encryption"]),
]

SECTIONS = [("about", "01", "About"), ("now", "02", "Now"), ("work", "03", "Selected work"), ("stack", "04", "Stack")]

for old in OUT.glob("*.svg"):
    old.unlink()
for name, t in THEMES.items():
    (OUT / f"header-{name}.svg").write_text(header(t))
    (OUT / f"footer-{name}.svg").write_text(footer(t))
    (OUT / f"stack-{name}.svg").write_text(stack(t))
    for i, (slug, label) in enumerate(LINKS, 1):
        (OUT / f"link-{slug}-{name}.svg").write_text(link(t, i, label))
    for i, (slug, title, kind, desc, tech) in enumerate(PROJECTS, 1):
        (OUT / f"card-{slug}-{name}.svg").write_text(card(t, i, title, kind, desc, tech))
    for slug, idx, title in SECTIONS:
        (OUT / f"section-{slug}-{name}.svg").write_text(section(t, idx, title))
print("ok")
