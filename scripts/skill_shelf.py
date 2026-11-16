"""Generate an animated bookshelf SVG of skills. Usage: python scripts/skill_shelf.py assets/skill-shelf.svg"""
import sys
from xml.sax.saxutils import escape

SHELVES = [
    ("Languages", ["TypeScript", "JavaScript", "Python", "SQL", "Rust", "Go", "Kotlin"]),
    ("AI & LLMs", ["OpenAI", "AI SDK", "PydanticAI", "Claude", "Gemini", "RAG", "Agents", "MCP", "LiveKit", "OCR"]),
    ("Frontend", ["Next.js", "React", "React Native", "Tailwind", "shadcn/ui", "TanStack", "Zustand", "Motion", "GSAP", "Three.js"]),
    ("Backend", ["Node.js", "FastAPI", "Fastify", "Hono", "Express", "tRPC", "WebSockets", "Celery", "Inngest"]),
    ("Databases", ["PostgreSQL", "Drizzle", "Prisma", "SQLAlchemy", "Convex", "Redis", "pgvector"]),
    ("Cloud & DevOps", ["AWS", "Cloudflare", "Vercel", "Railway", "Docker", "CI/CD"]),
    ("Payments & APIs", ["Razorpay", "Cashfree", "ICICI PG", "e-Sign", "WhatsApp API", "Telegram", "Google APIs"]),
    ("Design & More", ["Figma", "UI/UX", "Design Systems", "Playwright", "Tauri", "Android", "WebRTC"]),
]

# (spine color, text color)
PALETTE = [
    ("#b4413c", "#fff4e6"), ("#2f5d8a", "#f1f5fb"), ("#3f7d58", "#f0faf3"), ("#d9a441", "#2a1a08"),
    ("#6b4c9a", "#f6f0ff"), ("#1f2937", "#f3f4f6"), ("#c26a3d", "#fff6ee"), ("#4a8c8c", "#effafa"),
    ("#8c3b5a", "#fff0f6"), ("#e6d3a3", "#3b2a14"), ("#355c4b", "#eef8f2"), ("#5a6fb0", "#f2f4ff"),
]

W = 940
COL_W = 440
PAD_X = 20
TOP = 70
SHELF_H = 175
PLANK_H = 16
BOOK_W = 36
GAP = 4
FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"


def book_height(label, i):
    base = max(len(label) * 7.6 + 34, 104)
    jitter = [0, 14, 6, 20, 2, 12, 8][i % 7]
    return min(base + jitter, SHELF_H - 22)


def main(out):
    rows = (len(SHELVES) + 1) // 2
    H = TOP + rows * SHELF_H + 40
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        f'role="img" aria-label="Skill bookshelf">',
        "<style>",
        f"text{{font-family:{FONT};}}",
        ".book{animation:drop .55s cubic-bezier(.2,.9,.3,1.2) both;}",
        "@keyframes drop{from{opacity:0;transform:translateY(-26px)}to{opacity:1;transform:translateY(0)}}",
        "@media (prefers-reduced-motion:reduce){.book{animation:none;opacity:1}}",
        "</style>",
        "<defs>",
        '<linearGradient id="wood" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8a5a36"/>'
        '<stop offset="1" stop-color="#5e3b22"/></linearGradient>',
        '<linearGradient id="back" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a1c13"/>'
        '<stop offset="1" stop-color="#1c120c"/></linearGradient>',
        '<linearGradient id="gloss" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#000" stop-opacity=".25"/>'
        '<stop offset=".25" stop-color="#fff" stop-opacity=".12"/><stop offset=".6" stop-color="#fff" stop-opacity="0"/>'
        '<stop offset="1" stop-color="#000" stop-opacity=".3"/></linearGradient>',
        "</defs>",
        # outer frame
        f'<rect x="0" y="0" width="{W}" height="{H}" rx="18" fill="url(#wood)"/>',
        f'<rect x="{PAD_X - 6}" y="{TOP - 14}" width="{W - 2 * (PAD_X - 6)}" height="{H - TOP + 2}" rx="8" fill="url(#back)"/>',
        f'<text x="{W / 2}" y="40" text-anchor="middle" font-size="22" font-weight="700" fill="#f7e7c8" '
        f'letter-spacing="1">My Skill Shelf</text>',
    ]

    # vertical divider between columns
    div_x = PAD_X + COL_W + (W - 2 * PAD_X - 2 * COL_W) / 2
    parts.append(f'<rect x="{div_x - 6}" y="{TOP - 14}" width="12" height="{H - TOP + 2}" fill="url(#wood)"/>')

    delay = 0.0
    color_i = 0
    for idx, (name, books) in enumerate(SHELVES):
        col, row = idx % 2, idx // 2
        x0 = PAD_X + col * (W - 2 * PAD_X - COL_W)
        floor = TOP + (row + 1) * SHELF_H - PLANK_H - 10
        total = len(books) * BOOK_W + (len(books) - 1) * GAP
        bx = x0 + 14
        for i, label in enumerate(books):
            h = book_height(label, i + idx)
            w = BOOK_W + (4 if i % 3 == 1 else 0) - (3 if i % 4 == 2 else 0)
            fill, ink = PALETTE[color_i % len(PALETTE)]
            color_i += 1
            y = floor - h
            cx, cy = bx + w / 2, y + h / 2
            lean = (i == len(books) - 1 and len(books) < 9)
            g_attr = f'transform="rotate(7 {bx + w} {floor})"' if lean else ""
            parts.append(f'<g {g_attr}><g class="book" style="animation-delay:{delay:.2f}s">')
            parts.append(f'<rect x="{bx}" y="{y}" width="{w}" height="{h}" rx="3" fill="{fill}"/>')
            parts.append(f'<rect x="{bx}" y="{y}" width="{w}" height="{h}" rx="3" fill="url(#gloss)"/>')
            parts.append(f'<rect x="{bx}" y="{y + 9}" width="{w}" height="3" fill="{ink}" opacity=".35"/>')
            parts.append(f'<rect x="{bx}" y="{y + h - 12}" width="{w}" height="3" fill="{ink}" opacity=".35"/>')
            parts.append(
                f'<text x="{cx}" y="{cy}" transform="rotate(-90 {cx} {cy})" text-anchor="middle" '
                f'dominant-baseline="central" font-size="12.5" font-weight="600" fill="{ink}">{escape(label)}</text>'
            )
            parts.append("</g></g>")
            bx += w + GAP
            delay += 0.03
        # plank + brass label
        parts.append(f'<rect x="{x0}" y="{floor}" width="{COL_W}" height="{PLANK_H}" rx="2" fill="url(#wood)"/>')
        parts.append(f'<rect x="{x0}" y="{floor}" width="{COL_W}" height="3" fill="#a87447"/>')
        lw = len(name) * 7.4 + 22
        lx = x0 + COL_W - lw - 12
        parts.append(f'<rect x="{lx}" y="{floor + 2}" width="{lw}" height="{PLANK_H - 4}" rx="3" fill="#d8b46a"/>')
        parts.append(
            f'<text x="{lx + lw / 2}" y="{floor + PLANK_H / 2 + 0.5}" text-anchor="middle" dominant-baseline="central" '
            f'font-size="10.5" font-weight="700" fill="#3b2410" letter-spacing=".6">{escape(name.upper())}</text>'
        )
        assert total + 14 < COL_W, (name, total)

    parts.append("</svg>")
    with open(out, "w") as f:
        f.write("\n".join(parts))


if __name__ == "__main__":
    main(sys.argv[1])
