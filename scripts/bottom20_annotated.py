#!/usr/bin/env python3
"""Build matching clean and context-annotated bottom-20 income-share figures."""
from __future__ import annotations

import csv
import html
import shutil
import subprocess
from pathlib import Path

from window_timeline_svg import timeline_svg

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/bottom20_income_share.csv"
FIGURES = ROOT / "figures"
START_YEAR, END_YEAR = 1997, 2024
FOCUS_START = {"BRA": 2003, "MEX": 1998}
FOCUS_END = 2014
COLORS = {"BRA": "#147d86", "MEX": "#d77237"}


def load_data() -> dict[str, dict[int, float]]:
    result: dict[str, dict[int, float]] = {"BRA": {}, "MEX": {}}
    with DATA.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            country, year = row["country_code"], int(row["year"])
            if country in result and START_YEAR <= year <= END_YEAR:
                result[country][year] = float(row["income_share_percent"])
    return result


def make_svg(data: dict[str, dict[int, float]], annotated: bool) -> Path:
    FIGURES.mkdir(exist_ok=True)
    version = "annotated" if annotated else "clean"
    path = FIGURES / f"bottom20_income_share_1997_2024_{version}.svg"
    width, height = 1700, 960
    left, right, top, bottom = 85, 1250, 130, 495
    min_share, max_share = 2.0, 6.0

    def px(year: float) -> float:
        return left + (year - START_YEAR) / (END_YEAR - START_YEAR) * (right - left)

    def py(value: float) -> float:
        return bottom - (value - min_share) / (max_share - min_share) * (bottom - top)

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        '<style>text{font-family:Arial,Helvetica,sans-serif;fill:#222}.small{font-size:16px;fill:#555}</style>',
        '<text x="85" y="45" font-size="30" font-weight="bold">Income share held by the bottom 20%: Brazil and Mexico</text>',
        '<text x="85" y="76" font-size="14" fill="#666">Source: World Bank, WDI (SI.DST.FRST.20)</text>',
        '<text x="85" y="111" font-size="16" fill="#555">Share of national income (%)</text>',
    ]
    for tick in (2, 3, 4, 5, 6):
        yy = py(tick)
        svg.extend([
            f'<line x1="{left}" y1="{yy:.1f}" x2="{right}" y2="{yy:.1f}" stroke="#ddd"/>',
            f'<text x="{left-12}" y="{yy+5:.1f}" text-anchor="end" class="small">{tick}</text>',
        ])
    for year in (1997, 2000, 2003, 2006, 2009, 2012, 2015, 2018, 2021, 2024):
        anchor = "end" if year == 2024 else "middle"
        svg.append(f'<text x="{px(year):.1f}" y="{bottom+26}" text-anchor="{anchor}" class="small">{year}</text>')

    for country, label in (("BRA", "Brazil"), ("MEX", "Mexico")):
        color = COLORS[country]
        observations = sorted(data[country].items())
        for (year_a, value_a), (year_b, value_b) in zip(observations, observations[1:]):
            # Survey breaks are left disconnected.
            if (country == "BRA" and (year_a, year_b) == (2011, 2012)) or (
                country == "MEX" and (year_a, year_b) in ((2006, 2008), (2014, 2016))
            ):
                continue
            dash = ' stroke-dasharray="16 10"' if year_b - year_a > 1 else ''
            stroke_width = 3.6 if FOCUS_START[country] <= year_a and year_b <= FOCUS_END else 2.5
            svg.append(
                f'<line x1="{px(year_a):.1f}" y1="{py(value_a):.1f}" '
                f'x2="{px(year_b):.1f}" y2="{py(value_b):.1f}" '
                f'stroke="{color}" stroke-width="{stroke_width}"{dash}/>'
            )
        for year, value in observations:
            radius = 6.5 if year in (FOCUS_START[country], FOCUS_END) else 4
            svg.append(
                f'<circle cx="{px(year):.1f}" cy="{py(value):.1f}" r="{radius}" fill="{color}">'
                f'<title>{html.escape(label)} {year}: {value:g}%</title></circle>'
            )
        last_year, last_value = observations[-1]
        label_y = py(last_value)
        svg.append(
            f'<text x="{right+18}" y="{label_y:.1f}" font-size="20" font-weight="bold" '
            f'style="fill:{color}">{label} {last_value:g}% ({last_year})</text>'
        )

    if annotated:
        aid_x, aid_y = px(2020), py(data["BRA"][2020])
        svg.extend([
            f'<line x1="{aid_x:.1f}" y1="240" x2="{aid_x:.1f}" y2="{aid_y-13:.1f}" '
            'stroke="#75828c" stroke-width="1.3"/>',
            f'<path d="M {aid_x-5:.1f} {aid_y-19:.1f} L {aid_x:.1f} {aid_y-12:.1f} '
            f'L {aid_x+5:.1f} {aid_y-19:.1f}" fill="none" stroke="#75828c" stroke-width="1.3"/>',
            f'<text x="{aid_x:.1f}" y="232" text-anchor="middle" font-size="13" '
            'fill="#344451">Brazil: 2020 emergency cash aid</text>',
            f'<line x1="{px(2014):.1f}" y1="555" x2="{px(2019):.1f}" y2="555" '
            'stroke="#866b5e" stroke-width="1.5"/>',
            f'<line x1="{px(2014):.1f}" y1="547" x2="{px(2014):.1f}" y2="563" '
            'stroke="#866b5e" stroke-width="1.5"/>',
            f'<line x1="{px(2019):.1f}" y1="547" x2="{px(2019):.1f}" y2="563" '
            'stroke="#866b5e" stroke-width="1.5"/>',
            f'<text x="{(px(2014)+px(2019))/2:.1f}" y="588" text-anchor="middle" '
            'font-size="13" fill="#344451">Brazil: crisis &amp; slow recovery</text>',
        ])
    svg.extend(timeline_svg(data, "bottom20"))
    svg.extend([
        '<text x="85" y="901" font-size="14" fill="#666">Dashed program lines continue beyond the selected window. Brazil: Auxílio Brasil (2021–23), then Bolsa Família resumed; Mexico: Prospera (2014–19).</text>',
        '<text x="85" y="926" font-size="14" fill="#666">Descriptive changes; survey-method breaks within these intervals. Sources: World Bank WDI; Brazil MDS; Mexico government.</text>',
        '</svg>',
    ])
    path.write_text("\n".join(svg), encoding="utf-8")
    return path


def main() -> None:
    data = load_data()
    converter = shutil.which("rsvg-convert")
    for annotated in (False, True):
        svg_path = make_svg(data, annotated)
        print(f"Saved {svg_path}")
        if converter:
            png_path = svg_path.with_suffix(".png")
            subprocess.run([converter, "-w", "3400", "-h", "1920", str(svg_path), "-o", str(png_path)], check=True)
            print(f"Saved {png_path}")
        if annotated:
            shutil.copyfile(svg_path, FIGURES / "bottom20_income_share.svg")
            if converter:
                shutil.copyfile(png_path, FIGURES / "bottom20_income_share.png")
    if not converter:
        print("PNGs skipped (optional rsvg-convert is not installed).")


if __name__ == "__main__":
    main()
