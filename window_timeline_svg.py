"""Aligned program windows and endpoint statistics for the inequality figures."""
from __future__ import annotations

def timeline_svg(
    data: dict[str, dict[int, float]],
    metric: str,
) -> list[str]:
    if metric not in ("gini", "bottom20"):
        raise ValueError(metric)

    def px(year: float) -> float:
        return 500 + (year - 1997) / 27 * 780

    def summary(code: str, start: int, end: int = 2014) -> tuple[str, str, str]:
        first, last = data[code][start], data[code][end]
        change = last - first
        relative = 100 * change / first
        if metric == "gini":
            return f"{first:.1f}", f"{last:.1f}", f"{change:+.1f} Gini pts ({relative:+.1f}%)"
        return f"{first:.1f}%", f"{last:.1f}%", f"{change:+.1f} pp ({relative:+.1f}%)"

    rows = (
        ("MEX", 1998, 675, "#d77237", "Progresa → Oportunidades", "Program began 1997"),
        ("BRA", 2003, 755, "#147d86", "Bolsa Família", "Program began 2003"),
    )
    svg = ['<text x="85" y="607" font-size="23" font-weight="bold" fill="#344451">Comparison windows and observed changes</text>']
    for code, start, y, color, label, subtitle in rows:
        x1, x2 = px(start), px(2014)
        first, last, change_line = summary(code, start)
        svg.extend([
            f'<text x="85" y="{y-9}" font-size="22" font-weight="bold" style="fill:{color}">{label}</text>',
            f'<text x="85" y="{y+18}" font-size="16" style="fill:{color}">{subtitle}</text>',
            f'<text x="{x1:.1f}" y="{y-19}" text-anchor="middle" font-size="23" font-weight="bold" style="fill:{color}">{first}</text>',
            f'<text x="{x2:.1f}" y="{y-19}" text-anchor="middle" font-size="23" font-weight="bold" style="fill:{color}">{last}</text>',
            f'<text x="{x2+42:.1f}" y="{y-19}" font-size="22" font-weight="bold" style="fill:{color}">{change_line}</text>',
            f'<line x1="{x1:.1f}" y1="{y}" x2="{x2:.1f}" y2="{y}" stroke="{color}" stroke-width="5"/>',
            f'<circle cx="{x1:.1f}" cy="{y}" r="5.5" fill="{color}"/>',
            f'<circle cx="{x2:.1f}" cy="{y}" r="5.5" fill="{color}"/>',
            f'<text x="{x1:.1f}" y="{y+27}" text-anchor="middle" font-size="19" style="fill:{color}">{start}</text>',
            f'<text x="{x2:.1f}" y="{y+27}" text-anchor="middle" font-size="19" style="fill:{color}">2014</text>',
        ])

    # Programme lineages after the selected endpoint. Bolsa Família was
    # replaced by Auxílio Brasil in 2021 and relaunched in 2023.
    svg.extend([
        f'<line x1="{px(2014):.1f}" y1="675" x2="{px(2019):.1f}" y2="675" stroke="#d77237" stroke-width="2.4" stroke-dasharray="10 8" opacity="0.75"/>',
        f'<line x1="{px(2014):.1f}" y1="755" x2="{px(2021):.1f}" y2="755" stroke="#147d86" stroke-width="2.4" stroke-dasharray="10 8" opacity="0.75"/>',
        f'<line x1="{px(2023):.1f}" y1="755" x2="{px(2024):.1f}" y2="755" stroke="#147d86" stroke-width="2.4" stroke-dasharray="6 6" opacity="0.75"/>',
    ])

    common_y = 840
    x1, x2 = px(2004), px(2014)
    svg.extend([
        '<text x="85" y="827" font-size="23" font-weight="bold" fill="#56636d">Common observed</text>',
        '<text x="85" y="856" font-size="23" font-weight="bold" fill="#56636d">endpoints</text>',
        f'<line x1="{x1:.1f}" y1="{common_y}" x2="{x2:.1f}" y2="{common_y}" stroke="#56636d" stroke-width="5"/>',
        f'<circle cx="{x1:.1f}" cy="{common_y}" r="5.5" fill="#56636d"/>',
        f'<circle cx="{x2:.1f}" cy="{common_y}" r="5.5" fill="#56636d"/>',
        f'<text x="{x1:.1f}" y="{common_y+27}" text-anchor="middle" font-size="19" fill="#56636d">2004</text>',
        f'<text x="{x2:.1f}" y="{common_y+27}" text-anchor="middle" font-size="19" fill="#56636d">2014</text>',
    ])
    bra_first, bra_last, bra_change = summary("BRA", 2004)
    mex_first, mex_last, mex_change = summary("MEX", 2004)
    svg.extend([
        f'<text x="{x2+42:.1f}" y="827" font-size="22" style="fill:#147d86">Brazil {bra_first} → {bra_last}; <tspan font-weight="bold">{bra_change}</tspan></text>',
        f'<text x="{x2+42:.1f}" y="857" font-size="22" style="fill:#d77237">Mexico {mex_first} → {mex_last}; <tspan font-weight="bold">{mex_change}</tspan></text>',
    ])
    return svg
