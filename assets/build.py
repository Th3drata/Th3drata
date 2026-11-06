"""Génère les SVG du README de profil : une page de manuel `man oscar` (thèmes dark + light).
Usage : python3 assets/build.py  (depuis la racine du repo)

La page est découpée en bandes empilées pour que chaque projet et chaque lien
de SEE ALSO soit cliquable (un lien dans un SVG en <img> ne l'est pas).
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).parent
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"
W, FS, LH, IND = 880, 14, 24, 56  # largeur, taille de police, interligne, retrait des paragraphes

THEMES = {
    "dark": dict(fg="#c9d1d9", bold="#f0f6fc", muted="#8b949e", opt="#ffa657", ok="#7ee787", rule="#30363d"),
    "light": dict(fg="#1f2328", bold="#1f2328", muted="#59636e", opt="#bc4c00", ok="#1a7f37", rule="#d1d9e0"),
}

# --- contenu ------------------------------------------------------------------

DESCRIPTION = [
    "Takes an idea and ships it: web apps in TypeScript, native iOS apps in Swift,",
    "and tools that run close to the metal in C and C++. Plays CTFs on HackTheBox",
    "and TryHackMe in its spare cycles.",
]
OPTIONS = [
    ("--web", "TypeScript, React, Next.js, Node.js, Supabase, SQL"),
    ("--ios", "Swift, SwiftUI"),
    ("--low-level", "C, C++, Python, Bash, Linux"),
]
EXAMPLES = [
    ("parseledger", "Bank statements in, accounting data out, reconciled to the cent."),
    ("virtulouvre", "A 3D game in the Louvre, everything generated in code."),
    ("monetia", "A SwiftUI app to keep track of your money."),
    ("securedroplite", "Encrypted file drops that delete themselves."),
]
ENVIRONMENT = [
    "University of Geneva, BSc in Mathematics, Computer Science and Digital Sciences.",
    "Speaks French, Polish, English and German.",
]
BUGS = ["Still looking for a summer 2027 job. Reports welcome."]
SEE_ALSO = [("linkedin", "linkedin(1)"), ("mail", "mail(1)"), ("resume", "resume(1)")]

# --- primitives ---------------------------------------------------------------


def svg(h, label, body, style=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" viewBox="0 0 {W} {h}" '
            f'role="img" aria-label="{escape(label)}"><style>text{{font-family:{MONO};font-size:{FS}px}}{style}</style>'
            f"{body}</svg>")


def t(x, y, s, fill, weight=400, anchor="start", under=False):
    deco = ' text-decoration="underline"' if under else ""
    return (f'<text x="{x}" y="{y}" fill="{fill}" font-weight="{weight}" text-anchor="{anchor}"{deco} '
            f'xml:space="preserve">{escape(s)}</text>')


def heading(c, y, s):
    return t(0, y, s, c["bold"], 700)


def para(c, y, lines):
    return "".join(t(IND, y + i * LH, l, c["fg"]) for i, l in enumerate(lines))


# --- bandes -------------------------------------------------------------------


def top(c):
    y, b = 22, []
    # invite : « man oscar » se tape tout seul, une lettre toutes les 90 ms
    cmd = "man oscar"
    widths = ";".join(str(round(8.6 * i)) for i in range(len(cmd) + 1))
    b.append(t(0, y, "~ $", c["ok"]))
    b.append(f'<clipPath id="type"><rect x="36" y="0" height="40" width="{round(8.6 * len(cmd))}">'
             f'<animate attributeName="width" begin="0s" dur="{0.09 * len(cmd):.2f}s" calcMode="discrete" '
             f'values="{widths}" fill="freeze"/></rect></clipPath>')
    b.append(f'<g clip-path="url(#type)">{t(36, y, cmd, c["fg"])}</g>')
    y += 44
    b.append(t(0, y, "OSCAR(1)", c["muted"]) + t(W / 2, y, "User Commands", c["muted"], anchor="middle")
             + t(W, y, "OSCAR(1)", c["muted"], anchor="end"))
    b.append(f'<path d="M0 {y + 12.5}H{W}" stroke="{c["rule"]}"/>')
    y += 48
    b.append(heading(c, y, "NAME"))
    y += LH + 6
    b.append(t(IND, y, "oscar", c["bold"], 700) + t(IND + 52, y, "— Oscar Albert, software developer and maths & CS student", c["fg"]))
    y += 46
    b.append(heading(c, y, "SYNOPSIS"))
    y += LH + 6
    x = IND
    for part, kind in [("oscar", "b"), (" [", "f"), ("--web", "o"), ("] [", "f"), ("--ios", "o"), ("] [", "f"),
                       ("--low-level", "o"), ("] ", "f"), ("idea", "u")]:
        col = {"b": c["bold"], "f": c["fg"], "o": c["opt"], "u": c["opt"]}[kind]
        b.append(t(x, y, part, col, 700 if kind == "b" else 400, under=kind == "u"))
        x += len(part) * 8.43
    y += 46
    b.append(heading(c, y, "DESCRIPTION"))
    y += LH + 6
    b.append(para(c, y, DESCRIPTION))
    y += LH * len(DESCRIPTION) + 22
    b.append(heading(c, y, "OPTIONS"))
    y += LH + 6
    for i, (opt, desc) in enumerate(OPTIONS):
        b.append(t(IND, y + i * LH, opt, c["opt"]) + t(IND + 128, y + i * LH, desc, c["fg"]))
    y += LH * len(OPTIONS) + 22
    b.append(heading(c, y, "EXAMPLES"))
    return svg(y + 10, "man oscar: Oscar Albert, software developer and maths and CS student. "
               "Builds web apps in TypeScript, iOS apps in Swift and low-level tools in C and C++.", "".join(b))


def example(c, name, desc):
    return svg(LH, f"{name}: {desc}", t(IND, 17, name, c["bold"], 700) + t(IND + 152, 17, desc, c["fg"]))


def middle(c):
    y, b = 30, []
    b.append(heading(c, y, "ENVIRONMENT"))
    y += LH + 6
    b.append(para(c, y, ENVIRONMENT))
    y += LH * len(ENVIRONMENT) + 22
    b.append(heading(c, y, "BUGS"))
    y += LH + 6
    b.append(para(c, y, BUGS))
    y += LH * len(BUGS) + 22
    b.append(heading(c, y, "SEE ALSO"))
    return svg(y + 10, "Environment: University of Geneva, BSc in Mathematics, Computer Science and Digital "
               "Sciences. Speaks French, Polish, English and German. Bugs: still looking for a summer 2027 job.",
               "".join(b))


def see_also(c, label, first, last):
    x0 = IND if first else 0
    w = x0 + len(label) * 8.43 + (0 if last else 20)
    body = t(x0, 17, label, c["opt"], under=True) + ("" if last else t(x0 + len(label) * 8.43, 17, ", ", c["fg"]))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w:.0f}" height="{LH}" viewBox="0 0 {w:.0f} {LH}" '
            f'role="img" aria-label="{escape(label)}"><style>text{{font-family:{MONO};font-size:{FS}px}}</style>{body}</svg>')


def bottom(c):
    y, b = 20, []
    b.append(f'<path d="M0 {y}.5H{W}" stroke="{c["rule"]}"/>')
    y += 28
    b.append(t(0, y, "Oscar Albert", c["muted"]) + t(W / 2, y, "2026", c["muted"], anchor="middle")
             + t(W, y, "OSCAR(1)", c["muted"], anchor="end"))
    y += 44
    b.append(t(0, y, "~ $", c["ok"]))
    b.append(f'<rect class="cur" x="36" y="{y - 13}" width="9" height="17" fill="{c["ok"]}"/>')
    style = "@keyframes b{0%,49%{opacity:1}50%,100%{opacity:0}}.cur{animation:b 1.1s steps(1) infinite}"
    return svg(y + 12, "Oscar Albert, 2026", "".join(b), style)


for old in OUT.glob("*.svg"):
    old.unlink()
for name, c in THEMES.items():
    (OUT / f"top-{name}.svg").write_text(top(c))
    (OUT / f"middle-{name}.svg").write_text(middle(c))
    (OUT / f"bottom-{name}.svg").write_text(bottom(c))
    for slug, desc in EXAMPLES:
        (OUT / f"ex-{slug}-{name}.svg").write_text(example(c, slug, desc))
    for i, (slug, label) in enumerate(SEE_ALSO):
        (OUT / f"see-{slug}-{name}.svg").write_text(see_also(c, label, i == 0, i == len(SEE_ALSO) - 1))
print("ok")

# --- README -------------------------------------------------------------------

REPOS = {"parseledger": "Parseledger", "virtulouvre": "VirtuLouvre", "monetia": "Monetia", "securedroplite": "SecureDropLite"}
LINKS = {"linkedin": ("https://www.linkedin.com/in/oscar-albert", "LinkedIn"),
         "mail": ("mailto:oscar.albert@free.fr", "Email: oscar.albert@free.fr"),
         "resume": ("https://www.oscaralbert.fr/resume", "Resume (PDF)")}


def pic(name, alt, width="100%"):
    return (f'<picture><source media="(prefers-color-scheme: dark)" srcset="assets/{name}-dark.svg">'
            f'<img alt="{escape(alt)}" src="assets/{name}-light.svg" width="{width}"></picture>')


def see_width(slug):
    import re
    return float(re.search(r'width="([\d.]+)"', (OUT / f"see-{slug}-light.svg").read_text()).group(1))


lines = ["<!-- Généré par assets/build.py : une page de manuel `man oscar`. -->", "<p>",
         pic("top", "man oscar. NAME: oscar, Oscar Albert, software developer and maths and CS student. "
             "SYNOPSIS: oscar [--web] [--ios] [--low-level] idea. DESCRIPTION: " + " ".join(DESCRIPTION) + " OPTIONS: "
             + " ".join(f"{o} {d}." for o, d in OPTIONS)) + "<br>"]
for slug, desc in EXAMPLES:
    lines.append(f'<a href="https://github.com/Th3drata/{REPOS[slug]}">' + pic(f"ex-{slug}", f"{REPOS[slug]}: {desc}") + "</a><br>")
lines.append(pic("middle", "ENVIRONMENT: " + " ".join(ENVIRONMENT) + " BUGS: " + " ".join(BUGS)) + "<br>")
lines.append("".join(f'<a href="{LINKS[s][0]}">' + pic(f"see-{s}", LINKS[s][1], f"{see_width(s) / W * 100:.1f}%") + "</a>"
                     for s, _ in SEE_ALSO) + "<br>")
lines += [pic("bottom", "Oscar Albert, 2026"), "</p>"]
(OUT.parent / "README.md").write_text("\n".join(lines) + "\n")
print("README ok")
