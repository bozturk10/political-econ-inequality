#!/usr/bin/env python3
"""Compare Brazil and Mexico in separate Gini-decomposition and wage figures."""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


OUT = Path(__file__).resolve().parent / "figures"
OUT.mkdir(exist_ok=True)
BRAZIL, MEXICO = "#147d86", "#d77237"
INK, MUTED, GRID = "#17232b", "#5e6e77", "#e2e8eb"
plt.rcParams.update({"font.family": "DejaVu Sans", "svg.fonttype": "none"})


def header(fig, title, subtitle):
    fig.text(.075, .936, title, fontsize=25, fontweight="bold", color=INK)
    fig.text(.075, .891, subtitle, fontsize=13.5, color=MUTED)
    fig.add_artist(plt.Line2D([.075, .925], [.858, .858], transform=fig.transFigure,
                              color=GRID, linewidth=1.4))


def legend(fig, x=.66, y=.813):
    for name, color, offset in [("Brazil", BRAZIL, 0), ("Mexico", MEXICO, .13)]:
        fig.add_artist(plt.Line2D([x + offset, x + offset + .02], [y, y],
                                  transform=fig.transFigure, color=color, linewidth=8))
        fig.text(x + offset + .027, y - .007, name, fontsize=12, color=INK)


def save(fig, stem):
    for suffix in ("png", "svg"):
        path = OUT / f"{stem}.{suffix}"
        fig.savefig(path, dpi=190 if suffix == "png" else None, facecolor="white")
        print(path)
    plt.close(fig)


def gini_figure():
    categories = [
        "Labor income per employed adult", "Transfers per adult",
        "Pensions per adult", "Adults' share of household",
        "Other nonlabor income per adult", "Share of adults employed",
        "Capital income per adult",
    ]
    brazil = np.array([45, 20, 18, 13, 8, -4, 0])
    mexico = np.array([68, 17, -3, 6, 26, -13, -1])
    factor_colors = [
        "#3056a3",  # labor income
        "#2b8a57",  # transfers
        "#7555a8",  # pensions
        "#be791d",  # household composition
        "#22899a",  # other nonlabor income
        "#b85b46",  # employment share
        "#777f88",  # capital income
    ]
    fig = plt.figure(figsize=(16, 9), facecolor="white")
    header(fig, "Income inequality | What accounts for the Gini decline?",
           "Shapley decomposition  •  Brazil 2001–2011: −6.5 Gini points  •  Mexico 2000–2010: −6.2 Gini points")
    fig.text(.075, .810, "Share of each country's observed decline (%)", fontsize=14.5,
             fontweight="bold", color=INK)
    yy = np.arange(len(categories))
    for name, values, left in [("BRAZIL", brazil, .34), ("MEXICO", mexico, .645)]:
        fig.text(left, .762, name, fontsize=17, fontweight="bold", color=INK)
        ax = fig.add_axes([left, .215, .25, .515])
        ax.set_xlim(-18, 76)
        ax.set_ylim(-.5, len(categories) - .5)
        ax.invert_yaxis()
        ax.set_yticks(yy, categories if name == "BRAZIL" else [],
                      fontsize=12, color=INK)
        ax.tick_params(axis="y", length=0, pad=13)
        ax.set_xticks([-10, 0, 20, 40, 60], ["−10%", "0", "20%", "40%", "60%"])
        ax.tick_params(axis="x", length=0, pad=9, labelsize=10.5, colors=MUTED)
        ax.set_axisbelow(True)
        ax.grid(axis="x", color=GRID)
        ax.axvline(0, color="#798790", linewidth=1.3)
        for spine in ax.spines.values():
            spine.set_visible(False)
        for y, value, color in zip(yy, values, factor_colors):
            if value:
                ax.barh(y, value, height=.48, color=color, zorder=3)
            x = value + 1.3 if value >= 0 else value - 1.3
            ax.text(x, y, f"{value:+d}%" if value else "0%",
                    ha="left" if value >= 0 else "right", va="center",
                    fontsize=11.3, fontweight="bold", color=INK)
    fig.add_artist(plt.Line2D([.615, .615], [.215, .765], transform=fig.transFigure,
                              color=GRID, linewidth=1.2))

    fig.text(.075, .140,
             "Labor income was the largest single contributor in both countries: 45% in Brazil and 68% in Mexico.",
             fontsize=11.4, fontweight="bold", color=INK)
    fig.text(.075, .105,
             "Positive shares helped reduce Gini; negative shares offset the decline. Transfers include public and private payments.",
             fontsize=10.4, color=MUTED)
    fig.text(.075, .074,
             "Source: Azevedo, Inchauste & Sanfelice (2013), World Bank Policy Research Working Paper 6715, Fig. 7;",
             fontsize=9.5, color=MUTED)
    fig.text(.075, .053,
             "survey years: Appendix Table A1 (SEDLAC/PNAD and ENIGH). Descriptive accounting, not a causal programme estimate.",
             fontsize=9.5, color=MUTED)
    save(fig, "gini_decomposition_brazil_mexico_comparison")


def wage_figure():
    groups = [
        ("BOTTOM 20%", (8.0, 6.7), (1.2, 2.6)),
        ("ALL HOUSEHOLDS", (3.9, 3.8), (-1.7, .6)),
        ("TOP 20%", (2.5, 2.8), (-3.3, .3)),
    ]
    fig = plt.figure(figsize=(16, 9), facecolor="white")
    header(fig, "Hourly earnings | Brazil and Mexico",
           "Annualized change in the main job  •  Brazil 2001–2011  •  Mexico 2000–2010")
    fig.text(.075, .810, "Average change per year (%)", fontsize=14.5,
             fontweight="bold", color=INK)
    legend(fig, .645, .811)
    for i, (heading, brazil, mexico) in enumerate(groups):
        left = .075 + .295 * i
        fig.text(left, .746, heading, fontsize=16, fontweight="bold", color=INK)
        fig.text(left, .717, "Household income group" if i != 1 else "Full sample",
                 fontsize=10.5, color=MUTED)
        ax = fig.add_axes([left + .035, .255, .245, .425])
        yy = np.array([0, 1])
        ax.barh(yy - .17, brazil, height=.30, color=BRAZIL, zorder=3)
        ax.barh(yy + .17, mexico, height=.30, color=MEXICO, zorder=3)
        ax.set_xlim(-5, 10.2)
        ax.set_ylim(-.5, 1.5)
        ax.invert_yaxis()
        ax.set_yticks(yy, ["Men", "Women"], fontsize=12.5, color=INK)
        ax.tick_params(axis="y", length=0, pad=8)
        ax.set_xticks([-4, 0, 4, 8], ["−4%", "0", "4%", "8%"])
        ax.tick_params(axis="x", length=0, pad=10, labelsize=10.5, colors=MUTED)
        ax.set_axisbelow(True)
        ax.grid(axis="x", color=GRID)
        ax.axvline(0, color="#798790", linewidth=1.2)
        for spine in ax.spines.values():
            spine.set_visible(False)
        for values, offset in [(brazil, -.17), (mexico, .17)]:
            for y, value in zip(yy, values):
                ax.text(value + (.15 if value >= 0 else -.15), y + offset, f"{value:+.1f}%",
                        ha="left" if value >= 0 else "right", va="center",
                        fontsize=11, fontweight="bold", color=INK)
        if i < 2:
            x_sep = left + .282
            fig.add_artist(plt.Line2D([x_sep, x_sep], [.29, .76],
                                      transform=fig.transFigure, color=GRID, linewidth=1.2))

    fig.text(.075, .112,
             "Source: Azevedo, Inchauste & Sanfelice (2013), World Bank Policy Research Working Paper 6715, Table 2;",
             fontsize=9.5, color=MUTED)
    fig.text(.075, .090,
             "survey years: Appendix Table A1. Authors' estimates from SEDLAC household survey data.",
             fontsize=9.5, color=MUTED)
    save(fig, "hourly_earnings_brazil_mexico_comparison")


if __name__ == "__main__":
    gini_figure()
    wage_figure()
