#!/usr/bin/env python3
"""Fetch World Bank Gini data and draw a Brazil–Mexico comparison figure.

Run: python3 gini_figure.py
Rebuild from the saved CSV without fetching: python3 gini_figure.py --cached

Data source (World Bank, Poverty and Inequality Platform via WDI):
https://data.worldbank.org/indicator/SI.POV.GINI
https://api.worldbank.org/v2/country/BRA;MEX/indicator/SI.POV.GINI
API documentation: https://datahelpdesk.worldbank.org/knowledgebase/articles/898581-api-basic-call-structures

"""

from __future__ import annotations

import csv
import html
import json
import shutil
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen

from window_timeline_svg import timeline_svg


ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
FIGURE_DIR = ROOT / "figures"
START_YEAR, END_YEAR = 1997, 2024
FOCUS_START = {"BRA": 2003, "MEX": 1998}
FOCUS_END = 2014
INDICATOR = "SI.POV.GINI"
BASE_URL = f"https://api.worldbank.org/v2/country/BRA;MEX/indicator/{INDICATOR}"
API_URL = BASE_URL + "?" + urlencode(
    {"date": f"{START_YEAR}:{END_YEAR}", "format": "json", "per_page": 1000}
)


def fetch_data() -> dict[str, dict[int, float]]:
    with urlopen(API_URL, timeout=30) as response:
        payload = json.load(response)
    if not isinstance(payload, list) or len(payload) != 2 or "message" in payload[0]:
        raise RuntimeError(f"Unexpected World Bank API response: {payload!r}")
    if int(payload[0].get("pages", 1)) != 1:
        raise RuntimeError("API response has more than one page; increase per_page")

    result: dict[str, dict[int, float]] = {"BRA": {}, "MEX": {}}
    for row in payload[1]:
        code = row["countryiso3code"]
        if code in result and row["value"] is not None:
            result[code][int(row["date"])] = float(row["value"])
    if not all(result.values()):
        raise RuntimeError("Missing observations for one or both countries")
    return result


def save_csv(data: dict[str, dict[int, float]]) -> Path:
    DATA_DIR.mkdir(exist_ok=True)
    path = DATA_DIR / "gini_brazil_mexico_1997_2026.csv"
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["country_code", "year", "gini_index_0_100", "indicator", "source_url"])
        for country in ("BRA", "MEX"):
            for year, value in sorted(data[country].items()):
                writer.writerow([country, year, value, INDICATOR, API_URL])
    return path


def load_csv() -> dict[str, dict[int, float]]:
    path = DATA_DIR / "gini_brazil_mexico_1997_2026.csv"
    data: dict[str, dict[int, float]] = {"BRA": {}, "MEX": {}}
    with path.open(newline="", encoding="utf-8") as file:
        for row in csv.DictReader(file):
            data[row["country_code"]][int(row["year"])] = float(row["gini_index_0_100"])
    return data


def make_svg(data: dict[str, dict[int, float]], annotated: bool) -> Path:
    FIGURE_DIR.mkdir(exist_ok=True)
    version = "annotated" if annotated else "clean"
    path = FIGURE_DIR / f"gini_brazil_mexico_1997_2024_{version}.svg"
    width, height = 1700, 960
    left, right, top, bottom = 85, 1250, 105, 495
    min_gini, max_gini = 40, 62

    def px(year: float) -> float:
        return left + (year - START_YEAR) / (END_YEAR - START_YEAR) * (right - left)

    def py(value: float) -> float:
        return bottom - (value - min_gini) / (max_gini - min_gini) * (bottom - top)

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        '<style>text{font-family:Arial,Helvetica,sans-serif;fill:#222} '
        '.small{font-size:16px;fill:#555}</style>',
        '<text x="85" y="45" font-size="30" font-weight="bold">Brazil and Mexico: Gini index, 1997–2024</text>',
        '<circle cx="94" cy="78" r="6" fill="#147d86" stroke="white" stroke-width="1.5"/>',
        '<text x="110" y="83" font-size="15" fill="#555">Observed survey year</text>',
        '<line x1="308" y1="78" x2="365" y2="78" stroke="#147d86" stroke-width="3.6" '
        'stroke-dasharray="1 11" stroke-linecap="round"/>',
        '<text x="377" y="83" font-size="15" fill="#555">Gap between observations; no annual estimate</text>',
    ]
    for tick in (40, 45, 50, 55, 60):
        yy = py(tick)
        svg.extend([
            f'<line x1="{left}" y1="{yy:.1f}" x2="{right}" y2="{yy:.1f}" stroke="#ddd"/>',
            f'<text x="{left-12}" y="{yy+5:.1f}" text-anchor="end" class="small">{tick}</text>',
        ])
    for year in (1997, 2000, 2003, 2006, 2009, 2012, 2015, 2018, 2021, 2024):
        xx = px(year)
        anchor = "end" if year == 2024 else "middle"
        svg.append(f'<text x="{xx:.1f}" y="{bottom+26}" text-anchor="{anchor}" class="small">{year}</text>')

    for country, label, color in (
        ("BRA", "Brazil", "#147d86"),
        ("MEX", "Mexico", "#d77237"),
    ):
        observations = sorted(data[country].items())
        # Missing intervening years are joined by dashed lines; only observed
        # years receive markers.
        for (year_a, value_a), (year_b, value_b) in zip(observations, observations[1:]):
            if (country == "BRA" and (year_a, year_b) == (2011, 2012)) or (
                country == "MEX" and (year_a, year_b) in ((2006, 2008), (2014, 2016))
            ):
                continue
            dash = ' stroke-dasharray="1 11" stroke-linecap="round"' if year_b - year_a > 1 else ''
            stroke_width = 3.6 if FOCUS_START[country] <= year_a and year_b <= FOCUS_END else 2.5
            svg.append(
                f'<line x1="{px(year_a):.1f}" y1="{py(value_a):.1f}" '
                f'x2="{px(year_b):.1f}" y2="{py(value_b):.1f}" '
                f'stroke="{color}" stroke-width="{stroke_width}"{dash}/>'
            )
        for year, value in observations:
            radius = 8.5 if year in (FOCUS_START[country], FOCUS_END) else 6
            svg.append(
                f'<circle cx="{px(year):.1f}" cy="{py(value):.1f}" r="{radius}" '
                f'fill="{color}" stroke="white" stroke-width="1.5">'
                f'<title>{html.escape(label)} {year}: {value:g}</title></circle>'
            )
        last_year, last_value = observations[-1]
        label_x = right + 18
        label_y = py(last_value)
        svg.append(
            f'<text x="{label_x}" y="{label_y:.1f}" font-size="20" '
            f'font-weight="bold" style="fill:{color}">{label} {last_value:g} ({last_year})</text>'
        )

    if annotated:
        svg.extend([
        f'<line x1="{px(2020):.1f}" y1="{top+78}" x2="{px(2020):.1f}" '
        f'y2="{py(data["BRA"][2020])-13:.1f}" stroke="#75828c" stroke-width="1.3"/>',
        f'<path d="M {px(2020)-5:.1f} {py(data["BRA"][2020])-19:.1f} '
        f'L {px(2020):.1f} {py(data["BRA"][2020])-12:.1f} '
        f'L {px(2020)+5:.1f} {py(data["BRA"][2020])-19:.1f}" '
        'fill="none" stroke="#75828c" stroke-width="1.3"/>',
        f'<text x="{px(2020):.1f}" y="{top+47}" text-anchor="middle" '
        'font-size="13" fill="#344451">Brazil: 2020 emergency cash aid</text>',
        f'<line x1="{px(2014):.1f}" y1="555" x2="{px(2019):.1f}" y2="555" '
        'stroke="#866b5e" stroke-width="1.5"/>',
        f'<line x1="{px(2014):.1f}" y1="547" x2="{px(2014):.1f}" y2="563" '
        'stroke="#866b5e" stroke-width="1.5"/>',
        f'<line x1="{px(2019):.1f}" y1="547" x2="{px(2019):.1f}" y2="563" '
        'stroke="#866b5e" stroke-width="1.5"/>',
        f'<text x="{(px(2014)+px(2019))/2:.1f}" y="588" text-anchor="middle" '
        'font-size="13" fill="#344451">Brazil: crisis &amp; slow recovery</text>',
        ])
    svg.extend(timeline_svg(data, "gini"))
    svg.extend([
        '<text x="85" y="901" font-size="14" fill="#666">Dashed program lines continue beyond the selected window. Brazil: Auxílio Brasil (2021–23), then Bolsa Família resumed; Mexico: Prospera (2014–19).</text>',
        '<text x="85" y="926" font-size="14" fill="#666">Descriptive changes; survey-method breaks within these intervals. Source: World Bank, WDI (SI.POV.GINI); Brazil MDS; Mexico government.</text>',
        '</svg>',
    ])
    path.write_text("\n".join(svg), encoding="utf-8")
    return path


def main() -> None:
    if "--cached" in sys.argv:
        data = load_csv()
        csv_path = DATA_DIR / "gini_brazil_mexico_1997_2026.csv"
    else:
        data = fetch_data()
        csv_path = save_csv(data)
    print(f"Saved {csv_path}")
    converter = shutil.which("rsvg-convert")
    for annotated in (False, True):
        svg_path = make_svg(data, annotated)
        print(f"Saved {svg_path}")
        if converter:
            png_path = svg_path.with_suffix(".png")
            subprocess.run([converter, "-w", "3400", "-h", "1920", str(svg_path), "-o", str(png_path)], check=True)
            print(f"Saved {png_path}")
        if annotated:
            shutil.copyfile(svg_path, FIGURE_DIR / "gini_brazil_mexico_1997_2026.svg")
            if converter:
                shutil.copyfile(png_path, FIGURE_DIR / "gini_brazil_mexico_1997_2026.png")
    if not converter:
        print("PNGs skipped (optional rsvg-convert is not installed); SVGs are ready to use.")


if __name__ == "__main__":
    main()
