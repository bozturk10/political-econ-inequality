#!/usr/bin/env python3
"""Two-panel real minimum wage comparison, with a common 2003 baseline."""

import csv
from pathlib import Path

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "real_minimum_wage_2003_2014.csv"
OUTPUT = ROOT / "output" / "minimum_wage_brazil_mexico_two_panels_2003_2014.png"

with SOURCE.open(newline="") as file:
    rows = list(csv.DictReader(file))

years = [int(r["year"]) for r in rows]
assert years == list(range(2003, 2015))

series = {
    "Brazil": [float(r["brazil_index_2000_100"]) for r in rows],
    "Mexico": [float(r["mexico_index_2000_100"]) for r in rows],
}
colors = {"Brazil": "#137f87", "Mexico": "#d36d32"}
ink, muted, grid = "#173047", "#536878", "#dce5e8"

plt.rcParams.update({"font.family": "DejaVu Sans"})
fig, axes = plt.subplots(1, 2, figsize=(14, 7.875), dpi=190)
fig.patch.set_facecolor("#fbfcfc")

for ax, (country, values) in zip(axes, series.items()):
    change = [(value / values[0] - 1) * 100 for value in values]
    ax.set_facecolor("#fbfcfc")
    ax.plot(years, change, color=colors[country], lw=4.5, solid_capstyle="round")
    ax.scatter([2003, 2014], [change[0], change[-1]], color=colors[country], s=75, zorder=5)
    ax.axhline(0, color="#aab8c0", lw=1.4)
    ax.set_xlim(2002.7, 2016)
    ax.set_xticks([2003, 2006, 2009, 2012, 2014])
    if country == "Brazil":
        ax.set_ylim(-5, 80)
        ax.set_yticks([0, 20, 40, 60, 80])
    else:
        ax.set_ylim(-2, 2)
        ax.set_yticks([-2, -1, 0, 1, 2])
    ax.grid(axis="y", color=grid, lw=1)
    ax.tick_params(axis="both", colors=muted, labelsize=12, length=0, pad=9)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_title(country, loc="left", fontsize=21, fontweight="bold", color=colors[country], pad=22)
    label_y = change[-1] if country == "Brazil" else 0.85
    ax.text(2014.2, label_y,
            f"+{change[-1]:.0f}%" if country == "Brazil" else f"+{change[-1]:.1f}%",
            color=colors[country], fontsize=20, fontweight="bold", va="center")
    ax.text(0.02, 0.94, f"(ILO index, 2000=100: {values[0]:.1f} to {values[-1]:.1f})",
            transform=ax.transAxes, color=muted, fontsize=11, va="center")

fig.text(0.075, 0.93, "Real minimum wage, 2003–2014", color=ink, fontsize=28, fontweight="bold")
fig.text(0.075, 0.88, "Cumulative change since 2003 (%)", color=muted, fontsize=15)
fig.text(0.075, 0.075, "Source: ILO Labour Overview 2008, Table 10-A (2003–2004); 2015, Table 10 (2005–2014).", color=muted, fontsize=10.5)

fig.subplots_adjust(left=0.075, right=0.92, top=0.79, bottom=0.19, wspace=0.18)
OUTPUT.parent.mkdir(exist_ok=True)
fig.savefig(OUTPUT, facecolor=fig.get_facecolor(), dpi=190)
print(OUTPUT)
