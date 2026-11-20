"""Extract and chart SEDLAC education wage ratios from the public workbook."""

import csv
import html
from pathlib import Path

import openpyxl

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
SOURCE = ROOT / "work/raw/2026_Act1_wages_hours_LAC.xlsx"
SOURCE_URL = "https://www.cedlas.econo.unlp.edu.ar/wp/wp-content/uploads/2026_Act1_wages_hours_LAC.xlsx"

wb = openpyxl.load_workbook(SOURCE, read_only=True, data_only=True)
ws = wb["wagegaps"]
assert ws.cell(3, 1).value == "Ratio of hourly wages"
assert ws.cell(5, 1).value == "Prime-age males"
assert [ws.cell(7, c).value for c in (2, 3, 4)] == ["High/Medium", "High/Low", "Medium/Low"]

raw = {"Brazil": [], "Mexico": []}
country = None
section = ""
for rownum, row in enumerate(ws.iter_rows(values_only=True), 1):
    first = row[0]
    if first in raw:
        country, section = first, ""
    elif country and isinstance(first, str):
        if first in ("With Rural North", "PNADC", "New Methodology"):
            section = first
        elif first not in ("New PNAD",):
            country = None
    elif country and isinstance(first, int) and all(isinstance(v, (int, float)) for v in row[1:4]):
        raw[country].append((first, *map(float, row[1:4]), section, rownum))

# Use the original PNAD sequence, selecting the expanded rural-North 2004 row
# for continuity with the 2005–2014 observations. Exclude the separate PNADC.
brazil = {}
for year, hm, hl, ml, section, rownum in raw["Brazil"]:
    if 2003 <= year <= 2014 and section != "PNADC":
        brazil[year] = (hm, hl, ml, section, rownum)
mexico = {}
for year, hm, hl, ml, section, rownum in raw["Mexico"]:
    if 1997 <= year <= 2014 and section != "New Methodology":
        mexico[year] = (hm, hl, ml, section, rownum)
assert sorted(brazil) == [2003, 2004, 2005, 2006, 2007, 2008, 2009, 2011, 2012, 2013, 2014]
assert sorted(mexico) == [1998, 2000, 2002, 2008, 2010, 2012, 2014]
assert brazil[2004][4] == 129
assert abs(brazil[2003][1] - 6.1680647) < 1e-7
assert abs(mexico[2014][1] - 4.1971589) < 1e-7

HERE.mkdir(parents=True, exist_ok=True)
with (HERE / "sedlac_education_hourly_wage_ratios_brazil_mexico.csv").open("w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["country", "year", "high_to_low", "high_to_medium", "medium_to_low", "survey_section", "source_sheet", "source_row", "source_url"])
    for name, series in (("Brazil", brazil), ("Mexico", mexico)):
        for year, (hm, hl, ml, section, rownum) in sorted(series.items()):
            writer.writerow([name, year, hl, hm, ml, section or "Original series", "wagegaps", rownum, SOURCE_URL])

def element(tag, attrs, body=""):
    return "<" + tag + " " + " ".join(f'{k.replace("_", "-")}="{html.escape(str(v), quote=True)}"' for k, v in attrs.items()) + ">" + body + "</" + tag + ">"

def text(x, y, value, size=24, weight=400, fill="#20303A", anchor="start"):
    return element("text", {"x": x, "y": y, "font-family": "Arial, Helvetica, sans-serif", "font-size": size,
                            "font-weight": weight, "fill": fill, "text-anchor": anchor}, html.escape(str(value)))

def line(x1, y1, x2, y2, stroke="#DCE4E8", width=2, dash=None, cap=None):
    attrs = {"x1": x1, "y1": y1, "x2": x2, "y2": y2, "stroke": stroke, "stroke-width": width}
    if dash:
        attrs["stroke_dasharray"] = dash
    if cap:
        attrs["stroke_linecap"] = cap
    return element("line", attrs)

W, H = 1920, 1080
L, R, T, B = 145, 1415, 285, 760
X = lambda year: L + (year - 1997) / 17 * (R - L)
Y = lambda ratio: B - (ratio - 3) / 3.5 * (B - T)
TEAL, ORANGE, MUTED = "#147D86", "#D77237", "#5B6972"
svg = [element("rect", {"x": 0, "y": 0, "width": W, "height": H, "fill": "white"}),
       text(95, 100, "The education wage gap narrowed in Brazil", 48, 700),
       text(95, 151, "Mexico ended above its first observed year", 29, 500, MUTED),
       line(95, 183, 1825, 183),
       text(95, 238, "Hourly wage of high-educated workers / low-educated workers", 27, 700)]
for tick in [3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5]:
    yy = Y(tick)
    svg += [line(L, yy, R, yy), text(L - 16, yy + 7, f"{tick:.1f}", 19, fill=MUTED, anchor="end")]
for year in [1997, 2000, 2003, 2006, 2009, 2012, 2014]:
    svg.append(text(X(year), B + 39, year, 19, fill=MUTED, anchor="middle"))
svg.append(line(L, B, R, B, "#9EADB4", 2))

for name, series, color in (("Brazil", brazil, TEAL), ("Mexico", mexico, ORANGE)):
    points = [(year, values[1]) for year, values in sorted(series.items())]
    for (year_a, value_a), (year_b, value_b) in zip(points, points[1:]):
        gap = year_b - year_a > 1
        svg.append(line(X(year_a), Y(value_a), X(year_b), Y(value_b), color, 4.5,
                        "1 11" if gap else None, "round"))
    for year, value in points:
        svg.append(element("circle", {"cx": X(year), "cy": Y(value), "r": 7,
                                      "fill": color, "stroke": "white", "stroke-width": 2},
                           element("title", {}, f"{name} {year}: {value:.3f}")))

svg += [element("rect", {"x": 1480, "y": 300, "width": 345, "height": 190, "rx": 14, "fill": "#E9F4F4"}),
        text(1510, 350, "BRAZIL  2003–2014", 21, 700, TEAL),
        text(1510, 407, "6.17 → 4.36", 37, 700, TEAL),
        text(1510, 453, "−29.3%", 31, 700, TEAL),
        element("rect", {"x": 1480, "y": 520, "width": 345, "height": 190, "rx": 14, "fill": "#FFF1E9"}),
        text(1510, 570, "MEXICO  1998–2014", 21, 700, ORANGE),
        text(1510, 627, "3.75 → 4.20", 37, 700, ORANGE),
        text(1510, 673, "+12.0%", 31, 700, ORANGE),
        element("circle", {"cx": 115, "cy": 858, "r": 7, "fill": TEAL, "stroke": "white", "stroke-width": 2}),
        text(133, 866, "Survey observation", 21, fill=MUTED),
        line(360, 858, 425, 858, TEAL, 4.5, "1 11", "round"),
        text(441, 866, "Years without observations; no annual values estimated", 21, fill=MUTED),
        text(95, 930, "Mexico has no 1997 observation; 1998 is the first within its 1997–2014 study window.", 19, fill=MUTED),
        text(95, 961, "Brazil: PNAD coverage expands to rural North in 2004. Mexico: no observations in 2003–2007.", 19, fill=MUTED),
        text(95, 1005, "Source: SEDLAC (CEDLAS and World Bank), wages and hours workbook, Nov 2026, ‘wagegaps’ sheet.", 18, fill=MUTED),
        text(95, 1034, "Prime-age males; low = 0–8 years of schooling, high = 14+ years. Ratios are descriptive, not causal.", 18, fill=MUTED)]
(HERE / "01_education_wage_premium_high_low.svg").write_text(
    '<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080" viewBox="0 0 1920 1080">' + "".join(svg) + "</svg>",
    encoding="utf-8",
)
