import json
import os

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]
INPUT_FILE = "data/contributions.json"
OUTPUT_FILE = "contrib-heatmap.svg"

def render_heatmap():
    if not os.path.exists(INPUT_FILE): return
    with open(INPUT_FILE, "r") as f:
        data = json.load(f)

    days = data.get("days", [])
    total = data.get("total", 0)

    box_size, gap, margin_x, margin_y = 11, 3, 30, 20
    width = margin_x * 2 + (53 * (box_size + gap))
    height = margin_y + (7 * (box_size + gap)) + 40 

    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" font-family="sans-serif">'
    svg += '<style>.c{opacity:0;animation:s .4s ease-out forwards;transform-box:fill-box;transform-origin:center}@keyframes s{0%{opacity:0;transform:translateY(-8px) scale(.5)}100%{opacity:1;transform:translateY(0) scale(1)}}@media(prefers-reduced-motion:reduce){.c{animation:none;opacity:1}}text{fill:#7d8590;font-size:10px}text.t{fill:#e6edf3;font-size:12px;font-weight:bold}</style>'

    for i, day in enumerate(days):
        week, day_of_week = i // 7, i % 7
        x = margin_x + (week * (box_size + gap))
        y = margin_y + (day_of_week * (box_size + gap))
        color = PALETTE[day.get("level", 0)]
        delay = (week + day_of_week) * 0.015
        svg += f'<rect class="c" x="{x}" y="{y}" width="{box_size}" height="{box_size}" rx="2" fill="{color}" style="animation-delay:{delay}s"/>'

    legend_y = height - 15
    svg += f'<text x="{margin_x}" y="{legend_y}">Less</text>'
    for i, color in enumerate(PALETTE):
        svg += f'<rect x="{margin_x + 30 + (i * 14)}" y="{legend_y - 9}" width="11" height="11" rx="2" fill="{color}"/>'
    svg += f'<text x="{margin_x + 30 + (len(PALETTE) * 14) + 2}" y="{legend_y}">More</text>'
    svg += f'<text class="t" x="{width - margin_x}" y="{legend_y}" text-anchor="end">{total:,} contributions in the last year</text></svg>'

    with open(OUTPUT_FILE, "w") as f:
        f.write(svg)

if __name__ == "__main__":
    render_heatmap()