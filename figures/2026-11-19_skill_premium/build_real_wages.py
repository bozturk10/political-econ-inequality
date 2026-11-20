"""Deflate SEDLAC education-specific wages with WDI CPI and chart changes."""

import csv
import html
from pathlib import Path

import openpyxl

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
SOURCE = ROOT / "work/raw/2026_Act1_wages_hours_LAC.xlsx"
CPI_FILE = HERE / "wdi_cpi_observed_wage_years.csv"
SEDLAC_URL = "https://www.cedlas.econo.unlp.edu.ar/wp/wp-content/uploads/2026_Act1_wages_hours_LAC.xlsx"
WDI_URL = "https://data.worldbank.org/indicator/FP.CPI.TOTL"

cpi = {}
with CPI_FILE.open(newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        cpi[row["country"], int(row["year"])] = float(row["cpi_2010_100"])

wb = openpyxl.load_workbook(SOURCE, read_only=True, data_only=True)
ws = wb["wage_1"]
assert ws.cell(3, 1).value == "Hourly wage in main activity in nominal LCU"
assert [ws.cell(7, col).value for col in (11, 12, 13)] == ["Low", "Mid", "High"]

raw = {"Brazil": [], "Mexico": []}
assert ws.cell(105, 1).value == "Brazil" and ws.cell(159, 1).value == "Chile"
assert ws.cell(378, 1).value == "Mexico" and ws.cell(398, 1).value == "Nicaragua"
for country, start_row, end_row in (("Brazil", 105, 158), ("Mexico", 378, 397)):
    section = "PNAD" if country == "Brazil" else "ENIGH"
    for rownum in range(start_row, end_row + 1):
        row = [ws.cell(rownum, col).value for col in (1, 11, 12, 13)]
        first = row[0]
        if first == "With Rural North":
            section = "PNAD with rural North"
        elif first in ("PNADC", "New Methodology"):
            section = first
        elif isinstance(first, int) and all(isinstance(v, (int, float)) for v in row[1:]):
            raw[country].append((first, *map(float, row[1:]), section, rownum))

series = {"Brazil": {}, "Mexico": {}}
for year, low, mid, high, section, rownum in raw["Brazil"]:
    if 2003 <= year <= 2014 and section != "PNADC":
        series["Brazil"][year] = (low, mid, high, section, rownum)
for year, low, mid, high, section, rownum in raw["Mexico"]:
    if 1997 <= year <= 2014 and section != "New Methodology":
        series["Mexico"][year] = (low, mid, high, section, rownum)
assert sorted(series["Brazil"]) == [2003, 2004, 2005, 2006, 2007, 2008, 2009, 2011, 2012, 2013, 2014]
assert sorted(series["Mexico"]) == [1998, 2000, 2002, 2008, 2010, 2012, 2014]
assert series["Brazil"][2004][4] == 134
assert series["Mexico"][2014][4] == 391

records = []
for country, by_year in series.items():
    first_year = min(by_year)
    for group, index in (("Low", 0), ("Middle", 1), ("High", 2)):
        first_real = by_year[first_year][index] * 100 / cpi[country, first_year]
        for year, values in sorted(by_year.items()):
            nominal = values[index]
            real = nominal * 100 / cpi[country, year]
            records.append({"country": country, "year": year, "education": group,
                            "nominal_hourly_local_currency": nominal,
                            "cpi_2010_100": cpi[country, year],
                            "real_hourly_2010_local_currency": real,
                            "index_first_observed_100": 100 * real / first_real,
                            "source_row": values[4], "survey_section": values[3] or "Original series"})

with (HERE / "sedlac_real_hourly_wage_by_education_brazil_mexico.csv").open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["country", "year", "education", "nominal_hourly_local_currency",
                                           "cpi_2010_100", "real_hourly_2010_local_currency",
                                           "index_first_observed_100", "source_row", "survey_section"])
    writer.writeheader()
    writer.writerows(records)

def el(tag, attrs, body=""):
    return "<" + tag + " " + " ".join(f'{k.replace("_", "-")}="{html.escape(str(v), quote=True)}"' for k, v in attrs.items()) + ">" + body + "</" + tag + ">"

def txt(x, y, value, size=24, weight=400, fill="#20303A", anchor="start"):
    return el("text", {"x": x, "y": y, "font-family": "Arial, Helvetica, sans-serif", "font-size": size,
                       "font-weight": weight, "fill": fill, "text-anchor": anchor}, html.escape(str(value)))

def ln(x1, y1, x2, y2, stroke="#DDE5E8", width=2, dash=None):
    attrs = {"x1": x1, "y1": y1, "x2": x2, "y2": y2, "stroke": stroke, "stroke-width": width}
    if dash:
        attrs.update({"stroke_dasharray": dash, "stroke_linecap": "round"})
    return el("line", attrs)

colors = {"Low": "#137F88", "Middle": "#D99A35", "High": "#284F8C"}
muted = "#5C6A73"
W, H = 1920, 1080
connectors = []
body = [el("rect", {"x": 0, "y": 0, "width": W, "height": H, "fill": "white"}),
        txt(95, 103, "Real hourly wages by education level", 49, 700),
        txt(95, 153, "Within-country change; each education group’s first observed year = 100", 27, fill=muted),
        ln(95, 183, 1825, 183),
        txt(95, 237, "Brazil · 2003–2014", 29, 700, "#147D86"),
        txt(1010, 237, "Mexico · 1998–2014", 29, 700, "#D77237")]
for i, (group, color) in enumerate(colors.items()):
    x = 95 + i * 195
    body += [el("circle", {"cx": x + 8, "cy": 275, "r": 7, "fill": color}),
             txt(x + 25, 283, group, 21, fill=muted)]

for country, left, right, start, end in (("Brazil", 145, 835, 2003, 2014), ("Mexico", 1060, 1750, 1998, 2014)):
    top, bottom = 342, 725
    px = lambda year: left + (year - start) / (end - start) * (right - left)
    py = lambda value: bottom - (value - 70) / 110 * (bottom - top)
    for tick in (80, 100, 120, 140, 160, 180):
        y = py(tick)
        body += [ln(left, y, right, y), txt(left - 13, y + 7, tick, 19, fill=muted, anchor="end")]
    for year in ([2003, 2006, 2009, 2012, 2014] if country == "Brazil" else [1998, 2002, 2006, 2010, 2014]):
        body.append(txt(px(year), bottom + 38, year, 19, fill=muted, anchor="middle"))
    body.append(ln(left, bottom, right, bottom, "#9CAEB7", 2))
    for group, color in colors.items():
        points = [(r["year"], r["index_first_observed_100"]) for r in records
                  if r["country"] == country and r["education"] == group]
        for (ya, va), (yb, vb) in zip(points, points[1:]):
            segment = ln(px(ya), py(va), px(yb), py(vb), color, 4, "1 11" if yb - ya > 1 else None)
            connectors.append(segment)
            body.append(segment)
        for year, value in points:
            body.append(el("circle", {"cx": px(year), "cy": py(value), "r": 6,
                                      "fill": color, "stroke": "white", "stroke-width": 1.5}))
    changes = {group: next(r["index_first_observed_100"] for r in records
                           if r["country"] == country and r["education"] == group and r["year"] == end) - 100
               for group in colors}
    for i, (group, value) in enumerate(changes.items()):
        x = left + i * 225
        body.append(txt(x, 840, f"{group}: {value:+.0f}%", 23, 700, colors[group]))

body += [txt(95, 907, "Real wage = nominal local-currency hourly wage ÷ CPI × 100 (2010-price local currency).", 20, fill=muted),
         txt(95, 938, "Each line is rebased separately: compare changes within a country, not wage levels across countries.", 20, fill=muted),
         txt(95, 978, "Source: SEDLAC (CEDLAS / World Bank), wage_1; World Bank WDI, FP.CPI.TOTL. Observed years only.", 18, fill=muted),
         txt(95, 1007, "These education groups cover all sexes and ages in wage_1, unlike the prime-age male wage-gap figure.", 18, fill=muted),
         txt(95, 1036, "Brazil’s PNAD expands to rural North in 2004; Mexico has no 1997 wage observation and no 2003–07 observations.", 18, fill=muted)]
(HERE / "02_real_hourly_wages_by_education.svg").write_text(
    '<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080" viewBox="0 0 1920 1080">' + "".join(body) + "</svg>",
    encoding="utf-8",
)

# Companion version: display observed survey years as separate points only.
points_only = [part for part in body if part not in connectors]
points_only = [part.replace('r="6"', 'r="8"') for part in points_only]
points_only = [part.replace("Within-country change; each education group’s first observed year = 100",
                                 "Observed survey years only; each education group’s first year = 100")
               .replace("Each line is rebased separately: compare changes within a country, not wage levels across countries.",
                        "Each series is rebased separately: compare changes within a country, not wage levels across countries.")
               for part in points_only]
(HERE / "02_real_hourly_wages_by_education_points_only.svg").write_text(
    '<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080" viewBox="0 0 1920 1080">' + "".join(points_only) + "</svg>",
    encoding="utf-8",
)
