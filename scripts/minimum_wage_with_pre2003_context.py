#!/usr/bin/env python3
"""Combined wage chart with Brazil's pre-2003 history shown as context."""

import csv
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import ConnectionPatch


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "real_minimum_wage_full_1997_2014.csv"
OUTPUT = ROOT / "output" / "minimum_wage_brazil_mexico_common_1997_baseline.png"

with SOURCE.open(newline="") as file:
    rows = list(csv.DictReader(file))

years = [int(r["year"]) for r in rows]
brazil_index = [float(r["brazil_ilo_index_2000_100"]) for r in rows]
mexico_index = [float(r["mexico_ilo_index_2000_100"]) for r in rows]
assert years == list(range(1997, 2015))

brazil_base = brazil_index[0]
mexico_base = mexico_index[0]
brazil_change = [(value / brazil_base - 1) * 100 for value in brazil_index]
mexico_change = [(value / mexico_base - 1) * 100 for value in mexico_index]

plt.rcParams.update({"font.family": "DejaVu Sans"})
fig, ax = plt.subplots(figsize=(14, 7.875), dpi=190)
fig.patch.set_facecolor("#fbfcfc")
ax.set_facecolor("#fbfcfc")
ink, muted, grid = "#173047", "#536878", "#dce5e8"
teal, orange = "#137f87", "#d36d32"

ax.plot(years, mexico_change, color=orange, lw=4.5, solid_capstyle="round")
pre_years = [year for year in years if year <= 2003]
post_years = [year for year in years if year >= 2003]
ax.plot(pre_years, brazil_change[:len(pre_years)], color=teal, lw=4.3,
        ls=(0, (5, 3)), solid_capstyle="round")
ax.plot(post_years, brazil_change[years.index(2003):], color=teal, lw=4.5,
        solid_capstyle="round")
ax.scatter([1997, 2014], [mexico_change[0], mexico_change[-1]], color=orange, s=75, zorder=5)
ax.scatter([2003, 2014], [brazil_change[years.index(2003)], brazil_change[-1]], color=teal, s=75, zorder=5)
ax.axhline(0, color="#aab8c0", lw=1.4)
ax.set_xlim(1996.7, 2018.8)
ax.set_ylim(-15, 137)
ax.set_xticks([1997, 2000, 2003, 2006, 2009, 2012, 2014])
ax.set_yticks([-10, 0, 25, 50, 75, 100, 125])
ax.grid(axis="y", color=grid, lw=1)
ax.tick_params(axis="both", colors=muted, labelsize=13, length=0, pad=9)
for spine in ax.spines.values():
    spine.set_visible(False)

ax.text(2014.25, brazil_change[-1], "Brazil  +121%", color=teal, fontsize=19, fontweight="bold", va="center")
ax.text(2014.25, brazil_change[-1] - 8, "1997–2014  (92.3 to 203.6)", color=muted, fontsize=11, va="center")
ax.text(2014.25, brazil_change[-1] - 17, "2003–2014: +73%  (117.4 to 203.6)", color=teal, fontsize=11.5, va="center")
ax.text(2014.25, -4.0, "Mexico  −0.8%", color=orange, fontsize=19, fontweight="bold", va="center")
ax.text(2014.25, -10.5, "1997–2014  (102.5 to 101.7)", color=muted, fontsize=11, va="center")

fig.text(0.075, 0.93, "Real minimum wage, Brazil and Mexico", color=ink, fontsize=28, fontweight="bold")
fig.text(0.075, 0.88,
         "0% = each country’s own 1997 real minimum wage (not an equal wage level)",
         color=muted, fontsize=14)

timeline = fig.add_axes([0.075, 0.775, 0.845, 0.078], sharex=ax)
timeline.set_ylim(0, 2)
timeline.barh(1.47, 17, left=1997, height=0.52, color="#f8e8dd", edgecolor="none")
timeline.barh(0.55, 11, left=2003, height=0.52, color="#d9eeeb", edgecolor="none")
timeline.text(1997.25, 1.47, "Mexico: Progresa / Oportunidades",
              color=orange, fontsize=14, fontweight="bold", va="center")
timeline.text(2003.25, 0.55, "Brazil: Bolsa Família",
              color=teal, fontsize=14, fontweight="bold", va="center")
timeline.set_yticks([])
timeline.tick_params(axis="x", bottom=False, labelbottom=False)
for spine in timeline.spines.values():
    spine.set_visible(False)

for year, start_on_band, start_on_line, color in [
    (1997, 1.20, 0, orange),
    (2003, 0.28, brazil_change[years.index(2003)], teal),
]:
    fig.add_artist(ConnectionPatch(
        xyA=(year, start_on_band), coordsA=timeline.transData,
        xyB=(year, start_on_line), coordsB=ax.transData,
        color=color, lw=1.5, linestyle=(0, (2, 4)), alpha=0.55, zorder=1,
    ))

fig.text(0.075, 0.102, "Values in parentheses: ILO real minimum wage index (2000 = 100).", color=muted, fontsize=11.5)
fig.text(0.075, 0.066, "Source: ILO Labour Overview 2008, Table 10-A (1997–2004); 2015, Table 10 (2005–2014).", color=muted, fontsize=10.5)
fig.subplots_adjust(left=0.075, right=0.92, top=0.75, bottom=0.19)
OUTPUT.parent.mkdir(exist_ok=True)
fig.savefig(OUTPUT, facecolor=fig.get_facecolor(), dpi=190)
print(OUTPUT)
