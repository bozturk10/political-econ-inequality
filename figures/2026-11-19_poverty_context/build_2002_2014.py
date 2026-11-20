"""Balanced 2002–2014 regional poverty chart from SEDLAC."""

from collections import defaultdict
from pathlib import Path
import csv

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from openpyxl import load_workbook

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
SOURCE = ROOT / "work/raw/sedlac_poverty.xlsx"

# Fixed group with national poverty observations bracketing 2002–2014.
# Argentina is urban-only; Chile ends in 2013; Ecuador starts in 2003;
# Uruguay's national series starts in 2006.
COUNTRIES = [
    "Bolivia", "Brazil", "Colombia", "Costa Rica", "Dominican Republic",
    "El Salvador", "Guatemala", "Honduras", "Mexico", "Nicaragua",
    "Panama", "Paraguay", "Peru",
]
RAW_NAMES = {
    "Argentina": None,
    "Bolivia": "Bolivia", "Brazil": "Brazil", "Colombia": "Colombia",
    "Chile": None,
    "Costa Rica ": "Costa Rica", "Dominican Rep. ": "Dominican Republic",
    "Ecuador": "Ecuador", "El Salvador": "El Salvador", "Guatemala": "Guatemala",
    "Honduras": "Honduras", "Mexico": "Mexico", "Nicaragua": "Nicaragua",
    "Panama": "Panama", "Paraguay": "Paraguay", "Peru": "Peru",
    "Uruguay": "Uruguay",
}
SHORT = {"Dominican Republic": "Dominican Rep."}
BLUE, ORANGE = "#1F527A", "#D65E13"
INK, MUTED, GRID, GREY = "#172734", "#5C6972", "#DCE3E7", "#AAB5BB"

ws = load_workbook(SOURCE, read_only=True, data_only=True)["poverty USD6.85"]
raw = defaultdict(list)
country = None
segment = ""
for row_number, row in enumerate(ws.iter_rows(min_row=10, max_row=465, values_only=True), 10):
    item = row[0]
    if item in RAW_NAMES:
        country = RAW_NAMES[item]
        segment = ""
    elif country and isinstance(item, str):
        segment = item
    elif country and isinstance(item, int) and 1997 <= item <= 2014 and isinstance(row[1], (int, float)):
        # For Brazil use the original PNAD throughout 2002–2014, avoiding its
        # overlapping PNAD Continua estimates in 2012–2014.
        if country == "Brazil" and segment == "New PNADC":
            continue
        # Uruguay's pre-2006 series is urban; use its national series only.
        if country == "Uruguay" and segment != "National":
            continue
        # Where parallel definitions overlap, use the later workbook segment.
        raw[country].append((item, float(row[1]), segment, row_number))

observed = {}
for c in COUNTRIES:
    by_year = {}
    for year, value, segment, row_number in raw[c]:
        by_year[year] = (value, segment, row_number)
    assert min(by_year) <= 2002 and max(by_year) >= 2014, c
    observed[c] = by_year

years = list(range(2002, 2015))
interpolated = {}
for c in COUNTRIES:
    xs = sorted(observed[c])
    ys = [observed[c][x][0] for x in xs]
    interpolated[c] = np.interp(years, xs, ys)
mean = np.mean([interpolated[c] for c in COUNTRIES], axis=0)

with (OUT / "poverty_chart_values_2002_2014.csv").open("w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["country", "year", "poverty_headcount_percent", "observed_survey_year",
                     "workbook_segment", "method"])
    for c in COUNTRIES:
        for i, year in enumerate(years):
            obs = observed[c].get(year)
            writer.writerow([c, year, round(float(interpolated[c][i]), 6), bool(obs),
                             obs[1] if obs else "", "observed" if obs else "linear interpolation"])
    for i, year in enumerate(years):
        writer.writerow(["13-country unweighted mean", year, round(float(mean[i]), 6),
                         "", "", "mean of country estimates"])

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 13, "axes.edgecolor": "#9EABB2",
    "xtick.color": MUTED, "ytick.color": MUTED, "figure.facecolor": "white",
    "savefig.facecolor": "white",
})
fig = plt.figure(figsize=(16, 9))
ax = fig.add_axes([.075, .20, .725, .57])
fig.text(.075, .925, "Poverty across Latin America", fontsize=26, weight="bold", color=INK)
fig.text(.075, .875,
         "13 countries and their unweighted average · $6.85/day (2017 PPP) · 2002–2014",
         fontsize=14.5, color=MUTED)
fig.text(.075, .128,
         "Dots mark survey observations. Lines and the fixed-country mean interpolate between survey years.",
         fontsize=11.2, color=MUTED)
fig.text(.075, .103,
         "Some national survey methods change within this period; trends are descriptive.",
         fontsize=10.8, color=MUTED)
fig.text(.075, .073,
         "Source: SEDLAC (CEDLAS and World Bank), poverty workbook, September 2024. Headcount rate (%).",
         fontsize=10.5, color=MUTED)
ax.spines[["top", "right"]].set_visible(False)
ax.grid(axis="y", color=GRID, lw=1)
ax.set_axisbelow(True)
ax.set_title("Population below the poverty line (%)", loc="left", pad=14, fontsize=18, color=INK)
ax.set_xlim(2002, 2019.5)
ax.set_ylim(0, 70)
ax.set_xticks([2002, 2004, 2006, 2008, 2010, 2012, 2014])
ax.set_yticks([0, 10, 20, 30, 40, 50, 60, 70])
ax.tick_params(axis="y", labelsize=17, pad=10)
ax.tick_params(axis="x", labelsize=14)

for c in COUNTRIES:
    color = BLUE if c == "Brazil" else ORANGE if c == "Mexico" else GREY
    focus = c in ("Brazil", "Mexico")
    ax.plot(years, interpolated[c], color=color, lw=3.0 if focus else 1.4,
            alpha=1 if focus else .68, zorder=4 if focus else 2)
    observed_years = [y for y in years if y in observed[c]]
    ax.scatter(observed_years, [observed[c][y][0] for y in observed_years],
               color=color, s=24 if focus else 11, alpha=1 if focus else .66,
               zorder=5 if focus else 3)
ax.plot(years, mean, color=INK, lw=3.5, zorder=6)

labels = [(c, float(interpolated[c][-1])) for c in COUNTRIES]
labels.append(("13-country mean", float(mean[-1])))
labels.sort(key=lambda item: item[1])
gap = 3.35
positions = [max(v, 2 + i * gap) for i, (_, v) in enumerate(labels)]
for i in range(len(positions) - 2, -1, -1):
    positions[i] = min(positions[i], positions[i + 1] - gap)
if positions[-1] > 67:
    shift = positions[-1] - 67
    positions = [p - shift for p in positions]
for (c, actual), ypos in zip(labels, positions):
    focus = c in ("Brazil", "Mexico", "13-country mean")
    color = BLUE if c == "Brazil" else ORANGE if c == "Mexico" else INK if c == "13-country mean" else MUTED
    ax.plot([2014.08, 2014.65], [actual, ypos], color=color, lw=.8, alpha=.7, clip_on=False)
    ax.text(2014.8, ypos, f"{SHORT.get(c,c)}  {actual:.1f}%", color=color, va="center",
            fontsize=14.5 if focus else 10.0, weight="bold" if focus else "normal")

for ext in ("png", "svg"):
    fig.savefig(OUT / f"latin_america_poverty_2002_2014.{ext}", dpi=200)
plt.close(fig)
print(f"Wrote poverty chart for {len(COUNTRIES)} countries; 2014 mean {mean[-1]:.1f}%")
