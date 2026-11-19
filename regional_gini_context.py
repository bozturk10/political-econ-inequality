"""Plot ECLAC's published annual Gini changes for Latin America."""

import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "data/eclac_gini_annual_change_2002_2014.csv"
OUT = ROOT / "figures"
OUT.mkdir(exist_ok=True)

with SOURCE.open(newline="") as handle:
    rows = list(csv.DictReader(handle))

rows = [r for r in rows if r["country"] != "Costa Rica"]
rows.sort(key=lambda r: float(r["early_annual_percent"]))
names = [r["country"] for r in rows]
early = np.array([float(r["early_annual_percent"]) for r in rows])
late = np.array([float(r["late_annual_percent"]) for r in rows])
y = np.arange(len(rows))

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10})
fig, ax = plt.subplots(figsize=(10.5, 9.6), dpi=180)
fig.patch.set_facecolor("#fbfaf7")
ax.set_facecolor("#fbfaf7")

for i, name in enumerate(names):
    if name in {"Brazil", "Mexico"}:
        ax.axhspan(i - 0.46, i + 0.46, color="#f0e9d8", zorder=0)

ax.axvline(0, color="#777777", linewidth=1.1, zorder=1)
ax.grid(axis="x", color="#e4e1da", linewidth=0.7, zorder=0)
for i in range(len(rows)):
    ax.plot([early[i], late[i]], [i, i], color="#c5c2bc", linewidth=1.5, zorder=2)

ax.scatter(early, y, color="#20557a", s=56, label="Early period (around 2002–2008)", zorder=3)
ax.scatter(late, y, color="#c26032", marker="s", s=44, label="Later period (around 2008–2014)", zorder=4)

for i, name in enumerate(names):
    if name in {"Brazil", "Mexico", "Latin America (simple average)"}:
        ax.annotate(f"{early[i]:+.1f}", (early[i], i), xytext=(0, -13), textcoords="offset points",
                    ha="center", color="#20557a", fontsize=8.5, fontweight="bold")
        ax.annotate(f"{late[i]:+.1f}", (late[i], i), xytext=(0, 8), textcoords="offset points",
                    ha="center", color="#a84b25", fontsize=8.5, fontweight="bold")

ax.set_yticks(y, names)
ax.invert_yaxis()
for label in ax.get_yticklabels():
    if label.get_text() in {"Brazil", "Mexico"}:
        label.set_fontweight("bold")

ax.set_xlim(-3.35, 1.72)
ax.set_xticks([-3, -2, -1, 0, 1])
ax.set_xlabel("Annual change in Gini (%)   ← faster decline     increase →", labelpad=12)
fig.text(0.30, 0.965, "Latin America's inequality decline was uneven", ha="left",
         fontsize=18, fontweight="bold")
fig.text(0.30, 0.942, "Brazil and Mexico highlighted · negative values mean less inequality",
         ha="left", color="#555555", fontsize=10)
ax.legend(loc="lower left", bbox_to_anchor=(0, -0.135), ncol=2, frameon=False, fontsize=9)
for spine in ax.spines.values():
    spine.set_visible(False)

fig.text(0.15, 0.025,
         "Source: ECLAC, Social Panorama of Latin America 2017, Table I.1 (BADEHOG). "
         "Country reference years vary; Costa Rica excluded because later-period change is not comparable. "
         "Annual percentage changes, not Gini-index-point changes. Descriptive, not CCT effects.",
         ha="left", va="bottom", fontsize=7.5, color="#555555", wrap=True)
fig.subplots_adjust(left=0.30, right=0.96, top=0.90, bottom=0.15)

for suffix in ("png", "svg"):
    fig.savefig(OUT / f"latin_america_gini_change_2002_2014.{suffix}",
                dpi=180, facecolor=fig.get_facecolor())
