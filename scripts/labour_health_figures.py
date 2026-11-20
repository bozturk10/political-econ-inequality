"""Plot observed ILO labour indicators for the Brazil–Mexico comparison."""

import csv
import gzip
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
SOURCES = {
    "union": ROOT / "work/raw/ILR_TUMT_NOC_RT_A-20261116.csv.gz",
    "informal": ROOT / "work/raw/EMP_NIFL_SEX_RT_A-20261116.csv.gz",
}
COLORS = {"BRA": "#217a57", "MEX": "#c85c39"}
NAMES = {"BRA": "Brazil", "MEX": "Mexico"}


def load(path):
    with gzip.open(path, "rt", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


fig, axes = plt.subplots(1, 2, figsize=(11.6, 4.4), sharex=True)
for ax, key, title in zip(
    axes,
    ("union", "informal"),
    ("Trade union density", "Informal employment"),
):
    rows = load(SOURCES[key])
    for country in ("BRA", "MEX"):
        values = {
            int(r["time"]): float(r["obs_value"])
            for r in rows
            if r["ref_area"] == country
            and (key == "union" or r["sex"] == "SEX_T")
            and r["obs_value"]
        }
        years = range(2008, 2015)
        ax.plot(
            years,
            [values.get(y, float("nan")) for y in years],
            marker="o",
            linewidth=2.2,
            markersize=5,
            color=COLORS[country],
            label=NAMES[country],
        )
    ax.set(title=title, ylabel="Percent", xlim=(2007.8, 2014.2))
    ax.set_xticks([2008, 2010, 2012, 2014])
    ax.grid(axis="y", alpha=0.2)
    ax.spines[["top", "right"]].set_visible(False)
axes[0].legend(frameon=False, loc="upper right")
fig.suptitle("Brazil and Mexico: labour market indicators, 2008–2014", fontsize=14)
fig.text(
    0.5,
    0.01,
    "Observed years only; missing years are not interpolated. Source: ILOSTAT bulk downloads, 16 Nov 2026.",
    ha="center",
    fontsize=8,
    color="#555555",
)
fig.tight_layout(rect=(0, 0.04, 1, 0.95))
out = ROOT / "figures/labour_union_informality_brazil_mexico_2008_2014.png"
fig.savefig(out, dpi=220, bbox_inches="tight", facecolor="white")
print(out)

# Presentation version: percent axes share an honest zero baseline and range.
for ax in axes:
    ax.set_ylim(0, 100)
    ax.set_yticks([0, 20, 40, 60, 80, 100])
fig.suptitle("Brazil and Mexico: labour market levels, 2008–2014", fontsize=14)
zero_out = ROOT / "figures/labour_union_informality_brazil_mexico_2008_2014_zero_baseline.png"
fig.savefig(zero_out, dpi=220, bbox_inches="tight", facecolor="white")
print(zero_out)
