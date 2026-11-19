#!/usr/bin/env python3
"""Slide-ready income inequality comparison for the requested program windows."""
from __future__ import annotations

import csv
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "figures"
START = {"BRA": 2003, "MEX": 1998}  # WDI has no Mexico observation for 1997.
END = 2014
NAME = {"BRA": "Brazil", "MEX": "Mexico"}
COLOR = {"BRA": "#147d86", "MEX": "#d77237"}
SERIES = {
    "gini": (ROOT / "data/gini_brazil_mexico_1997_2026.csv", "gini_index_0_100"),
    "bottom20": (ROOT / "data/bottom20_income_share.csv", "income_share_percent"),
}


def read_series() -> dict[str, dict[str, dict[int, float]]]:
    result = {}
    for key, (path, column) in SERIES.items():
        result[key] = {"BRA": {}, "MEX": {}}
        with path.open(newline="", encoding="utf-8") as stream:
            for row in csv.DictReader(stream):
                code, year = row["country_code"], int(row["year"])
                if code in START and START[code] <= year <= END:
                    result[key][code][year] = float(row[column])
        for code in START:
            assert START[code] in result[key][code] and END in result[key][code]
    return result


def main() -> None:
    data = read_series()
    OUT.mkdir(exist_ok=True)
    width, height = 1600, 850
    specs = [
        ("gini", 102, 736, 47, 59, [48, 50, 52, 54, 56, 58], "Gini index"),
        ("bottom20", 866, 1500, 2.3, 5.2, [2.5, 3, 3.5, 4, 4.5, 5], "Bottom 20%'s income share"),
    ]
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#fff"/>',
        '<style>text{font-family:Arial,Helvetica,sans-serif;fill:#25313b}</style>',
        '<text x="102" y="56" font-size="32" font-weight="700">Income inequality during the program eras</text>',
        '<text x="102" y="89" font-size="17" fill="#5f6b75">Brazil 2003–2014  •  Mexico 1998–2014 (first available WDI observation)</text>',
        '<text x="102" y="115" font-size="14" fill="#63717a">Source: World Bank, World Development Indicators (SI.POV.GINI; SI.DST.FRST.20)</text>',
    ]
    for key, left, right, ymin, ymax, ticks, title in specs:
        top, bottom = 190, 546

        def x(year: int) -> float:
            return left + (year - 1998) / 16 * (right - left)

        def y(value: float) -> float:
            return bottom - (value - ymin) / (ymax - ymin) * (bottom - top)

        svg.append(f'<text x="{left}" y="162" font-size="23" font-weight="700">{title}</text>')
        for tick in ticks:
            yy = y(tick)
            svg.extend([
                f'<line x1="{left}" y1="{yy:.1f}" x2="{right}" y2="{yy:.1f}" stroke="#e7ebee"/>',
                f'<text x="{left-12}" y="{yy+5:.1f}" text-anchor="end" font-size="14" fill="#66717a">{tick:g}</text>',
            ])
        for year in (1998, 2002, 2006, 2010, 2014):
            svg.append(f'<text x="{x(year):.1f}" y="573" text-anchor="middle" font-size="14" fill="#66717a">{year}</text>')
        for code in ("BRA", "MEX"):
            points = sorted(data[key][code].items())
            for (ya, va), (yb, vb) in zip(points, points[1:]):
                dash = ' stroke-dasharray="10 9"' if yb - ya > 1 else ""
                svg.append(f'<line x1="{x(ya):.1f}" y1="{y(va):.1f}" x2="{x(yb):.1f}" y2="{y(vb):.1f}" stroke="{COLOR[code]}" stroke-width="3.5"{dash}/>' )
            for year, value in points:
                radius = 6.5 if year in (START[code], END) else 3.6
                svg.append(f'<circle cx="{x(year):.1f}" cy="{y(value):.1f}" r="{radius}" fill="{COLOR[code]}"/>')
            end = data[key][code][END]
            label_y = y(end) + (23 if code == "MEX" and key == "gini" else -13)
            svg.append(f'<text x="{right-6}" y="{label_y:.1f}" text-anchor="end" font-size="17" font-weight="700" style="fill:{COLOR[code]}">{NAME[code]}</text>')
        for col, code in enumerate(("BRA", "MEX")):
            start = data[key][code][START[code]]
            end = data[key][code][END]
            delta = end - start
            pct = 100 * delta / start
            bx = left + col * 318
            suffix = " Gini points" if key == "gini" else " percentage points"
            value_text = f"{start:.1f} → {end:.1f}" if key == "gini" else f"{start:.1f}% → {end:.1f}%"
            svg.extend([
                f'<rect x="{bx}" y="620" width="298" height="116" rx="13" fill="#fafbfc" stroke="#e4e9ec"/>',
                f'<text x="{bx+16}" y="649" font-size="16" font-weight="700" style="fill:{COLOR[code]}">{NAME[code]}  {START[code]}–2014</text>',
                f'<text x="{bx+16}" y="682" font-size="22" font-weight="700">{value_text}</text>',
                f'<text x="{bx+16}" y="712" font-size="17" font-weight="700">{delta:+.1f}{suffix}  ({pct:+.1f}%)</text>',
            ])
    svg.append('<text x="102" y="797" font-size="14" fill="#68757e">Descriptive endpoints; survey breaks affect Brazil (2012) and Mexico (2006–08). These changes are not program effects.</text>')
    svg.append('</svg>')
    path = OUT / "program_window_inequality_brazil_mexico_2003_1998_2014.svg"
    path.write_text("\n".join(svg), encoding="utf-8")
    print(path)
    converter = shutil.which("rsvg-convert")
    if converter:
        png = path.with_suffix(".png")
        subprocess.run([converter, "-w", "3200", "-h", "1700", str(path), "-o", str(png)], check=True)
        print(png)


if __name__ == "__main__":
    main()
