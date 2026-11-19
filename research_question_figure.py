#!/usr/bin/env python3
"""Make a two-panel 2008–2014 inequality research-puzzle figure."""
from __future__ import annotations

import csv
import html
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FIGURES = ROOT / "figures"
DATASETS = {
    "gini": (ROOT / "data/gini_brazil_mexico_1997_2026.csv", "gini_index_0_100"),
    "bottom20": (ROOT / "data/bottom20_income_share.csv", "income_share_percent"),
}
COLORS = {"BRA": "#147d86", "MEX": "#d77237"}
NAMES = {"BRA": "Brazil", "MEX": "Mexico"}


def load_data() -> dict[str, dict[str, dict[int, float]]]:
    data = {}
    for name, (path, field) in DATASETS.items():
        data[name] = {"BRA": {}, "MEX": {}}
        with path.open(newline="", encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                year = int(row["year"])
                country = row["country_code"]
                if country in data[name] and 2008 <= year <= 2014:
                    data[name][country][year] = float(row[field])
    for name in data:
        for country in ("BRA", "MEX"):
            assert 2008 in data[name][country] and 2014 in data[name][country]
    return data


def main() -> None:
    data = load_data()
    FIGURES.mkdir(exist_ok=True)
    width, height = 1600, 850
    top, bottom = 175, 545
    panel_specs = [
        ("gini", 105, 725, 47.0, 55.0, (47, 49, 51, 53, 55), "Gini index"),
        ("bottom20", 875, 1495, 3.0, 5.0, (3, 3.5, 4, 4.5, 5), "Income share of the bottom 20% (%)"),
    ]
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        '<style>text{font-family:Arial,Helvetica,sans-serif;fill:#222}</style>',
        '<text x="105" y="58" font-size="31" font-weight="bold">Brazil and Mexico: income inequality, 2008–2014</text>',
        '<text x="105" y="91" font-size="15" fill="#666">Source: World Bank, WDI (SI.POV.GINI and SI.DST.FRST.20)</text>',
    ]

    for key, left, right, ymin, ymax, ticks, title in panel_specs:
        def px(year: float) -> float:
            return left + (year - 2008) / 6 * (right - left)

        def py(value: float) -> float:
            return bottom - (value - ymin) / (ymax - ymin) * (bottom - top)

        svg.append(f'<text x="{left}" y="145" font-size="22" font-weight="bold">{html.escape(title)}</text>')
        for tick in ticks:
            y = py(tick)
            svg.extend([
                f'<line x1="{left}" y1="{y:.1f}" x2="{right}" y2="{y:.1f}" stroke="#e1e4e6"/>',
                f'<text x="{left-14}" y="{y+5:.1f}" text-anchor="end" font-size="14" fill="#555">{tick:g}</text>',
            ])
        for year in (2008, 2010, 2012, 2014):
            svg.append(f'<text x="{px(year):.1f}" y="{bottom+29}" text-anchor="middle" font-size="14" fill="#555">{year}</text>')

        for country in ("BRA", "MEX"):
            color = COLORS[country]
            points = sorted(data[key][country].items())
            for (year_a, value_a), (year_b, value_b) in zip(points, points[1:]):
                dash = ' stroke-dasharray="12 8"' if year_b - year_a > 1 else ''
                svg.append(
                    f'<line x1="{px(year_a):.1f}" y1="{py(value_a):.1f}" '
                    f'x2="{px(year_b):.1f}" y2="{py(value_b):.1f}" '
                    f'stroke="{color}" stroke-width="3"{dash}/>'
                )
            for year, value in points:
                radius = 6 if year in (2008, 2014) else 4
                svg.append(
                    f'<circle cx="{px(year):.1f}" cy="{py(value):.1f}" r="{radius}" fill="{color}">'
                    f'<title>{NAMES[country]} {year}: {value:g}</title></circle>'
                )
            svg.append(
                f'<text x="{right-12}" y="{py(data[key][country][2014])-15:.1f}" '
                f'text-anchor="end" font-size="15" font-weight="bold" '
                f'style="fill:{color}">{NAMES[country]}</text>'
            )

        for index, country in enumerate(("BRA", "MEX")):
            color = COLORS[country]
            x = left + index * 320
            start, end = data[key][country][2008], data[key][country][2014]
            delta, relative = end - start, 100 * (end / start - 1)
            if key == "gini":
                value_line = f"{start:.1f} → {end:.1f}"
                delta_line = f"{delta:+.1f} Gini points"
            else:
                value_line = f"{start:.1f}% → {end:.1f}%"
                delta_line = f"{delta:+.1f} pp"
            svg.extend([
                f'<rect x="{x}" y="630" width="300" height="128" rx="12" fill="white" '
                f'stroke="{color}" stroke-width="1.8"/>',
                f'<text x="{x+150}" y="660" text-anchor="middle" font-size="18" font-weight="bold" '
                f'style="fill:{color}">{NAMES[country]}</text>',
                f'<text x="{x+150}" y="696" text-anchor="middle" font-size="22" font-weight="bold" '
                f'style="fill:{color}">{value_line}</text>',
                f'<text x="{x+150}" y="730" text-anchor="middle" font-size="17" '
                f'style="fill:{color}"><tspan font-weight="bold">{delta_line}</tspan>'
                f'<tspan dx="6">({relative:+.1f}%)</tspan></text>',
            ])

    svg.append('</svg>')
    svg_path = FIGURES / "research_question_inequality_2008_2014.svg"
    svg_path.write_text("\n".join(svg), encoding="utf-8")
    print(f"Saved {svg_path}")
    converter = shutil.which("rsvg-convert")
    if converter:
        png_path = svg_path.with_suffix(".png")
        subprocess.run([converter, "-w", "3200", "-h", "1700", str(svg_path), "-o", str(png_path)], check=True)
        print(f"Saved {png_path}")


if __name__ == "__main__":
    main()
