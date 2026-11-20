#!/usr/bin/env python3
"""Combined real minimum wage chart for the two requested program windows."""

import csv
from pathlib import Path

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "real_minimum_wage_program_windows.csv"
OUTPUT = ROOT / "output" / "minimum_wage_brazil_2003_mexico_1997_to_2014.png"

with SOURCE.open(newline="") as file:
    rows = list(csv.DictReader(file))

mexico = [(int(r["year"]), float(r["mexico_ilo_index_2000_100"])) for r in rows]
brazil = [(int(r["year"]), float(r["brazil_ilo_index_2000_100"])) for r in rows if r["brazil_ilo_index_2000_100"]]
assert mexico[0] == (1997, 102.5) and mexico[-1] == (2014, 101.7)
assert brazil[0] == (2003, 117.4) and brazil[-1] == (2014, 203.6)

def cumulative_change(series):
    base = series[0][1]
    return [year for year, _ in series], [(value / base - 1) * 100 for _, value in series]

mx_years, mx_change = cumulative_change(mexico)
br_years, br_change = cumulative_change(brazil)

plt.rcParams.update({"font.family": "DejaVu Sans"})
fig, ax = plt.subplots(figsize=(14, 7.875), dpi=190)
fig.patch.set_facecolor("#fbfcfc")
ax.set_facecolor("#fbfcfc")
ink, muted, grid = "#173047", "#536878", "#dce5e8"
teal, orange = "#137f87", "#d36d32"

ax.plot(mx_years, mx_change, color=orange, lw=4.5, solid_capstyle="round")
ax.plot(br_years, br_change, color=teal, lw=4.5, solid_capstyle="round")
ax.scatter([1997, 2014], [mx_change[0], mx_change[-1]], color=orange, s=75, zorder=5)
ax.scatter([2003, 2014], [br_change[0], br_change[-1]], color=teal, s=75, zorder=5)
ax.axhline(0, color="#aab8c0", lw=1.4)
ax.set_xlim(1996.7, 2018.8)
ax.set_ylim(-16, 83)
ax.set_xticks([1997, 2000, 2003, 2006, 2009, 2012, 2014])
ax.set_yticks([-10, 0, 20, 40, 60, 80])
ax.grid(axis="y", color=grid, lw=1)
ax.tick_params(axis="both", colors=muted, labelsize=13, length=0, pad=9)
for spine in ax.spines.values():
    spine.set_visible(False)

ax.text(2014.25, br_change[-1], "Brazil  +73%", color=teal, fontsize=19, fontweight="bold", va="center")
ax.text(2014.25, br_change[-1] - 6.5, "2003–2014  (117.4 to 203.6)", color=muted, fontsize=11, va="center")
ax.text(2014.25, -5.5, "Mexico  −0.8%", color=orange, fontsize=19, fontweight="bold", va="center")
ax.text(2014.25, -11.0, "1997–2014  (102.5 to 101.7)", color=muted, fontsize=11, va="center")

fig.text(0.075, 0.93, "Real minimum wage, Brazil and Mexico", color=ink, fontsize=28, fontweight="bold")
fig.text(0.075, 0.88, "Cumulative change from each country’s start year (%)", color=muted, fontsize=15)
fig.text(0.075, 0.102, "Values in parentheses: ILO real minimum wage index (2000 = 100).", color=muted, fontsize=11.5)
fig.text(0.075, 0.066, "Source: ILO Labour Overview 2008, Table 10-A (1997–2004); 2015, Table 10 (2005–2014).", color=muted, fontsize=10.5)
fig.subplots_adjust(left=0.075, right=0.92, top=0.80, bottom=0.19)
OUTPUT.parent.mkdir(exist_ok=True)
fig.savefig(OUTPUT, facecolor=fig.get_facecolor(), dpi=190)
print(OUTPUT)
