"""Generate the README header banner and animated code card.

Usage: python scripts/profile_art.py assets
"""
import os
import sys
from xml.sax.saxutils import escape

SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"


def header():
    w, h = 1200, 260
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Hey, I'm Piyush">
<style>
text{{font-family:{SANS};}}
.t{{animation:rise .9s ease-out both;}}
.d{{animation:rise .9s .35s ease-out both;}}
@keyframes rise{{from{{opacity:0;transform:translateY(12px)}}to{{opacity:1;transform:translateY(0)}}}}
.w1{{animation:sway 9s ease-in-out infinite alternate;}}
.w2{{animation:sway 12s ease-in-out infinite alternate-reverse;}}
@keyframes sway{{from{{transform:translateX(0)}}to{{transform:translateX(-120px)}}}}
@media (prefers-reduced-motion:reduce){{.t,.d,.w1,.w2{{animation:none}}}}
</style>
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0f172a"/><stop offset=".55" stop-color="#312e81"/><stop offset="1" stop-color="#6366f1"/></linearGradient>
<clipPath id="c"><rect width="{w}" height="{h}" rx="16"/></clipPath>
</defs>
<g clip-path="url(#c)">
<rect width="{w}" height="{h}" fill="url(#bg)"/>
<circle cx="1040" cy="40" r="120" fill="#818cf8" opacity=".18"/>
<circle cx="140" cy="210" r="90" fill="#22d3ee" opacity=".10"/>
<path class="w1" d="M0 205 C150 170 300 240 450 205 S750 170 900 205 S1200 240 1350 205 L1350 260 L0 260Z" fill="#818cf8" opacity=".25"/>
<path class="w2" d="M0 225 C160 195 320 255 480 225 S800 195 960 225 S1280 255 1440 225 L1440 260 L0 260Z" fill="#a5b4fc" opacity=".18"/>
<text class="t" x="600" y="112" text-anchor="middle" font-size="58" font-weight="800" fill="#ffffff">Hey, I'm Piyush</text>
<text class="d" x="600" y="160" text-anchor="middle" font-size="21" font-weight="500" fill="#c7d2fe">CTO @ Scoutly  •  AI &amp; Full-Stack Developer @ KAN Universal</text>
</g>
</svg>
'''


# Each line is a list of (text, color) tokens.
K, S, P, N, C = "#bb9af7", "#9ece6a", "#c0caf5", "#7aa2f7", "#565f89"
CODE = [
    [("const ", K), ("piyush", N), (" = {", P)],
    [("  role", P), (": [", P), ('"CTO @ Scoutly"', S), (",", P)],
    [("         ", P), ('"AI & Full-Stack @ KAN"', S), ("],", P)],
    [("  based", P), (": ", P), ('"Delhi, India"', S), (",", P)],
    [("  stack", P), (": [", P), ('"Next.js"', S), (", ", P), ('"FastAPI"', S), (",", P)],
    [("          ", P), ('"Postgres"', S), (", ", P), ('"OpenAI"', S), ("],", P)],
    [("  loves", P), (": ", P), ('"shipping AI that works"', S), (",", P)],
    [("  speed", P), (": ", P), ('"idea → prod in days"', S), (",", P)],
    [("};", P)],
    [("", P)],
    [("// let's build something", C)],
]


def code_card():
    w, h = 470, 330
    top, lh, x0 = 62, 22, 22
    char_w = 7.9
    cycle = 14.0
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Animated code card">',
        f"<style>text{{font-family:{MONO};font-size:13.5px;white-space:pre;}}"
        ".cur{animation:blink 1s steps(1) infinite;}@keyframes blink{50%{opacity:0}}</style>",
        "<defs>",
    ]
    lines_svg = []
    t = 0.6
    for i, toks in enumerate(CODE):
        length = sum(len(s) for s, _ in toks)
        lw = max(length * char_w + 4, 1)
        dur = max(length * 0.035, 0.15)
        start, end = t / cycle, (t + dur) / cycle
        t += dur + 0.12
        y = top + i * lh
        parts.append(
            f'<clipPath id="l{i}"><rect x="{x0}" y="{y - 15}" height="{lh}" width="0">'
            f'<animate attributeName="width" dur="{cycle}s" repeatCount="indefinite" '
            f'values="0;0;{lw:.0f};{lw:.0f};0" keyTimes="0;{start:.4f};{end:.4f};0.94;1"/></rect></clipPath>'
        )
        tspans = "".join(f'<tspan fill="{c}">{escape(s)}</tspan>' for s, c in toks)
        lines_svg.append(f'<text x="{x0}" y="{y}" clip-path="url(#l{i})" xml:space="preserve">{tspans}</text>')
    parts.append("</defs>")
    parts += [
        f'<rect width="{w}" height="{h}" rx="14" fill="#1a1b26"/>',
        f'<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="14" fill="none" stroke="#2f334d"/>',
        f'<rect width="{w}" height="36" rx="14" fill="#16161e"/><rect y="22" width="{w}" height="14" fill="#16161e"/>',
        '<circle cx="22" cy="18" r="6" fill="#f7768e"/><circle cx="42" cy="18" r="6" fill="#e0af68"/><circle cx="62" cy="18" r="6" fill="#9ece6a"/>',
        f'<text x="{w / 2}" y="22" text-anchor="middle" fill="#565f89" style="font-size:12px">piyush.ts</text>',
    ]
    parts += lines_svg
    last_y = top + (len(CODE) - 1) * lh
    parts.append(f'<rect class="cur" x="{x0}" y="{last_y + 8}" width="8" height="2" fill="#7aa2f7"/>')
    parts.append("</svg>")
    return "\n".join(parts)


def main(out_dir):
    with open(os.path.join(out_dir, "header.svg"), "w") as f:
        f.write(header())
    with open(os.path.join(out_dir, "code-card.svg"), "w") as f:
        f.write(code_card())


if __name__ == "__main__":
    main(sys.argv[1])
