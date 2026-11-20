#!/usr/bin/env python3
"""Fetch and plot complementary Brazil–Mexico inequality indicators.

Run after installing requirements.txt: python3 scripts/additional_figures.py

Primary data sources:
World Bank WDI (bottom 20% income share):
  https://data.worldbank.org/indicator/SI.DST.FRST.20
SEDLAC (CEDLAS and World Bank; income and poverty workbooks):
  https://www.cedlas.econo.unlp.edu.ar/wp/estadisticas/sedlac/estadisticas/
ASPIRE (World Bank; survey-based CCT category indicators):
  https://www.worldbank.org/en/data/datatopics/aspire/about
  https://www.worldbank.org/en/data/datatopics/aspire/documentation
"""

from __future__ import annotations

import csv
import json
import shutil
import subprocess
import tempfile
import urllib.request
from pathlib import Path
from zipfile import ZipFile

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from openpyxl import load_workbook


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "work" / "raw"
DATA = ROOT / "data"
FIGURES = ROOT / "figures"
for folder in (RAW, DATA, FIGURES):
    folder.mkdir(parents=True, exist_ok=True)

SOURCES = {
    "sedlac_income.xlsx": "https://www.cedlas.econo.unlp.edu.ar/wp/wp-content/uploads/2026_Act1_incomes_LAC.xlsx",
    "sedlac_poverty.xlsx": "https://www.cedlas.econo.unlp.edu.ar/wp/wp-content/uploads/2024_Act1_poverty_LAC.xlsx",
    "aspire_performance.zip": "https://datacatalogfiles.worldbank.org/ddh-published/0037942/DR0087109/ASPIRE%20performance%20indicators.zip",
}
BOTTOM20_URL = (
    "https://api.worldbank.org/v2/country/BRA;MEX/indicator/SI.DST.FRST.20"
    "?date=1997:2026&format=json&per_page=1000"
)
POPULATION_URL = (
    "https://api.worldbank.org/v2/country/BRA;MEX/indicator/SP.POP.TOTL"
    "?date=1997:2026&format=json&per_page=1000"
)
COLORS = {"Brazil": "#147d86", "Mexico": "#d77237"}
SEDLAC_COUNTRIES = {
    "Argentina", "Bahamas", "Belize", "Bolivia", "Brazil", "Colombia", "Costa Rica",
    "Chile", "Ecuador", "El Salvador", "Guatemala", "Guyana", "Haiti", "Honduras",
    "Jamaica", "Mexico", "Nicaragua", "Panama", "Paraguay", "Peru",
    "Dominican Republic", "Suriname", "Uruguay", "Venezuela",
}


def get_file(name: str) -> Path:
    target = RAW / name
    if not target.exists() or target.stat().st_size == 0:
        print(f"Downloading {name}...")
        urllib.request.urlretrieve(SOURCES[name], target)
    return target


def write_rows(name: str, header: list[str], rows: list[tuple]) -> None:
    with (DATA / name).open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(rows)


def style_plot(ax, title: str, ylabel: str, xlim=(1997, 2026)) -> None:
    ax.set_title(title, loc="left", fontsize=13, weight="bold")
    ax.set_ylabel(ylabel)
    ax.set_xlim(*xlim)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", alpha=0.25)
    ax.tick_params(labelsize=9)


def save_figure(fig, stem: str) -> None:
    png = FIGURES / f"{stem}.png"
    svg = FIGURES / f"{stem}.svg"
    fig.savefig(svg, bbox_inches="tight")
    converter = shutil.which("rsvg-convert")
    if converter:
        subprocess.run([converter, "-z", "2", str(svg), "-o", str(png)], check=True)
    else:
        fig.savefig(png, dpi=180, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved figures/{stem}.png and .svg")


def bottom20() -> None:
    with urllib.request.urlopen(BOTTOM20_URL, timeout=30) as response:
        payload = json.load(response)
    if not isinstance(payload, list) or len(payload) != 2 or "message" in payload[0]:
        raise RuntimeError(f"Unexpected World Bank API response: {payload!r}")
    rows = []
    for item in payload[1]:
        if item["value"] is not None and item["countryiso3code"] in ("BRA", "MEX"):
            rows.append((item["countryiso3code"], int(item["date"]), float(item["value"]), BOTTOM20_URL))
    rows.sort()
    write_rows("bottom20_income_share.csv", ["country_code", "year", "income_share_percent", "source_url"], rows)

    fig, ax = plt.subplots(figsize=(10, 4.8), layout="constrained")
    for code, name in (("BRA", "Brazil"), ("MEX", "Mexico")):
        points = [(year, value) for country, year, value, _ in rows if country == code]
        ax.plot(*zip(*points), marker="o", markersize=3.5, linewidth=1.5, label=name, color=COLORS[name])
    style_plot(ax, "Income share held by the bottom 20%", "% of total income")
    ax.set_xlabel("Year")
    ax.legend(frameon=False)
    fig.text(0.01, -0.035, "Source: World Bank SI.DST.FRST.20. Dots are survey observations; lines bridge gaps.", fontsize=8)
    save_figure(fig, "bottom20_income_share")


def sedlac_income_ratio() -> None:
    sheet = load_workbook(get_file("sedlac_income.xlsx"), read_only=True, data_only=True)["deciles_pci"]
    cells = list(sheet.values)
    if cells[35][0] != "Mean" or cells[49][0] != "Mean":
        raise RuntimeError("SEDLAC income workbook layout changed; inspect mean rows")
    chosen: dict[tuple[str, int], tuple] = {}
    for j, (country, year) in enumerate(zip(cells[6], cells[7])):
        country = str(country).strip()
        if country not in COLORS or not str(year).isdigit():
            continue
        year = int(year)
        if not 1997 <= year <= 2026:
            continue
        urban, rural = cells[35][j], cells[49][j]  # URBAN/RURAL Mean rows
        if isinstance(urban, (int, float)) and isinstance(rural, (int, float)) and rural > 0:
            # Where a year is repeated under a revised survey method, use its last column.
            chosen[(country, year)] = (country, year, float(urban), float(rural), float(urban / rural), j + 1, SOURCES["sedlac_income.xlsx"])
    rows = sorted(chosen.values())
    write_rows(
        "sedlac_urban_rural_income_ratio.csv",
        ["country", "year", "urban_mean_local_currency", "rural_mean_local_currency", "urban_to_rural_ratio", "source_column", "source_url"],
        rows,
    )
    fig, ax = plt.subplots(figsize=(10, 4.8), layout="constrained")
    for name in COLORS:
        points = [(r[1], r[4]) for r in rows if r[0] == name]
        ax.plot(*zip(*points), marker="o", markersize=3, linewidth=1.4, label=name, color=COLORS[name])
    style_plot(ax, "Urban-to-rural mean income ratio", "Urban / rural per capita income")
    ax.set_xlabel("Year")
    ax.legend(frameon=False)
    fig.text(0.01, -0.035,
             "Source: SEDLAC (CEDLAS/World Bank). Survey method breaks: Brazil 2012; Mexico 2016.", fontsize=8)
    save_figure(fig, "sedlac_urban_rural_income_ratio")


def sedlac_poverty_gap() -> None:
    sheet = load_workbook(get_file("sedlac_poverty.xlsx"), read_only=True, data_only=True)["poverty USD6.85"]
    if sheet.cell(8, 6).value != "Headcount" or sheet.cell(8, 10).value != "Headcount":
        raise RuntimeError("SEDLAC poverty workbook layout changed; inspect headcount columns")
    chosen: dict[tuple[str, int], tuple] = {}
    country = ""
    for row in sheet.values:
        first = row[0]
        if isinstance(first, str) and first.strip() in SEDLAC_COUNTRIES:
            country = first.strip()
        if country in COLORS and isinstance(first, (int, float)) and 1997 <= first <= 2026:
            national, urban, rural = row[1], row[5], row[9]  # National/Urban/Rural FGT(0)
            if all(isinstance(v, (int, float)) for v in (national, urban, rural)):
                year = int(first)
                chosen[(country, year)] = (
                    country, year, float(national), float(urban), float(rural),
                    float(rural - urban), SOURCES["sedlac_poverty.xlsx"],
                )
    rows = sorted(chosen.values())
    write_rows(
        "sedlac_rural_urban_poverty_gap.csv",
        ["country", "year", "national_headcount_percent", "urban_headcount_percent",
         "rural_headcount_percent", "rural_minus_urban_pp", "source_url"],
        rows,
    )
    fig, ax = plt.subplots(figsize=(10, 4.8), layout="constrained")
    for name in COLORS:
        points = [(r[1], r[5]) for r in rows if r[0] == name]
        ax.plot(*zip(*points), marker="o", markersize=3, linewidth=1.4, label=name, color=COLORS[name])
    style_plot(ax, "Rural–urban poverty gap", "Rural minus urban (percentage points)")
    ax.set_xlabel("Year")
    ax.legend(frameon=False)
    fig.text(0.01, -0.035,
             "Source: SEDLAC (CEDLAS/World Bank), $6.85/day (2017 PPP). Method breaks: Brazil 2012; Mexico 2016.", fontsize=8)
    save_figure(fig, "sedlac_rural_urban_poverty_gap")


def aspire_coverage_targeting() -> None:
    zip_path = get_file("aspire_performance.zip")
    codes = {
        "per_sa_cc.cov_pop_tot": "population_coverage",
        "per_sa_cc.cov_q1_preT_tot": "coverage",
        "per_sa_cc.bry_q1_preT_tot": "beneficiary_incidence",
    }
    records = []
    with tempfile.TemporaryDirectory() as tmp:
        with ZipFile(zip_path) as archive:
            dta_path = Path(tmp) / "aspire.dta"
            with archive.open(archive.namelist()[0]) as source, dta_path.open("wb") as target:
                while block := source.read(1024 * 1024):
                    target.write(block)
        for chunk in pd.read_stata(
            dta_path, chunksize=100_000, convert_categoricals=False,
            columns=["Country_Code", "Year", "Indicator_Code", "val"],
        ):
            part = chunk[chunk.Country_Code.isin(["BRA", "MEX"]) & chunk.Indicator_Code.isin(codes)]
            records.extend(part.itertuples(index=False, name=None))
    rows = sorted(
        (country, int(year), codes[code], float(value), SOURCES["aspire_performance.zip"])
        for country, year, code, value in records
        if pd.notna(value) and str(year).isdigit() and int(year) <= 2018
    )
    write_rows(
        "aspire_cct_coverage_targeting.csv",
        ["country_code", "year", "measure", "percent", "source_url"], rows,
    )
    population_rows = [r for r in rows if r[2] == "population_coverage"]
    write_rows(
        "aspire_cct_population_coverage.csv",
        ["country_code", "year", "measure", "percent", "source_url"], population_rows,
    )
    population_fig, population_ax = plt.subplots(figsize=(10, 4.8), layout="constrained")
    for code, name in (("BRA", "Brazil"), ("MEX", "Mexico")):
        points = [(year, value) for country, year, _, value, _ in population_rows if country == code]
        population_ax.plot(*zip(*points), marker="o", markersize=4, linewidth=1.2,
                           linestyle="--", label=name, color=COLORS[name])
    style_plot(population_ax, "Conditional cash transfer coverage of the population",
               "% of total population covered", (2005, 2019))
    population_ax.set_xlabel("Survey year")
    population_ax.legend(frameon=False)
    population_fig.text(0.01, -0.035,
                        "Source: World Bank ASPIRE (per_sa_cc.cov_pop_tot). Includes direct and indirect beneficiaries.", fontsize=8)
    save_figure(population_fig, "aspire_cct_population_coverage")

    fig, axes = plt.subplots(2, 1, figsize=(10, 7), sharex=True, layout="constrained")
    for ax, measure, title, ylabel in (
        (axes[0], "coverage", "Coverage of the poorest quintile", "% of poorest quintile covered"),
        (axes[1], "beneficiary_incidence", "Beneficiary incidence in the poorest quintile", "% of CCT beneficiaries"),
    ):
        for code, name in (("BRA", "Brazil"), ("MEX", "Mexico")):
            points = [(year, value) for country, year, m, value, _ in rows if country == code and m == measure]
            ax.plot(*zip(*points), marker="o", markersize=4, linewidth=1.2, linestyle="--", label=name, color=COLORS[name])
        style_plot(ax, title, ylabel, (2005, 2019))
        ax.legend(frameon=False, loc="best")
    axes[-1].set_xlabel("Survey year")
    fig.suptitle("Conditional cash transfer category: coverage and targeting", fontsize=15, weight="bold")
    fig.text(0.01, -0.035,
             "Source: World Bank ASPIRE. Pre-transfer welfare quintiles; survey-based CCT category.", fontsize=8)
    save_figure(fig, "aspire_cct_coverage_targeting")


def population_figures() -> None:
    """Turn survey percentages into approximate people counts using WDI population."""
    with urllib.request.urlopen(POPULATION_URL, timeout=30) as response:
        payload = json.load(response)
    if not isinstance(payload, list) or len(payload) != 2 or "message" in payload[0]:
        raise RuntimeError(f"Unexpected World Bank population API response: {payload!r}")
    populations = {
        (item["countryiso3code"], int(item["date"])): int(item["value"])
        for item in payload[1]
        if item["value"] is not None and item["countryiso3code"] in ("BRA", "MEX")
    }

    poverty = pd.read_csv(DATA / "sedlac_rural_urban_poverty_gap.csv")
    poverty_rows = []
    for row in poverty.itertuples(index=False):
        code = "BRA" if row.country == "Brazil" else "MEX"
        population = populations.get((code, int(row.year)))
        if population is not None:
            estimated = population * row.national_headcount_percent / 100
            poverty_rows.append((code, int(row.year), population, row.national_headcount_percent,
                                 round(estimated), row.source_url, POPULATION_URL))
    write_rows("estimated_people_below_poverty_line.csv",
               ["country_code", "year", "population", "poverty_headcount_percent",
                "estimated_people_below_line", "poverty_source_url", "population_source_url"],
               poverty_rows)

    coverage = pd.read_csv(DATA / "aspire_cct_population_coverage.csv")
    beneficiary_rows = []
    for row in coverage.itertuples(index=False):
        population = populations.get((row.country_code, int(row.year)))
        if population is not None:
            estimated = population * row.percent / 100
            beneficiary_rows.append((row.country_code, int(row.year), population, row.percent,
                                     round(estimated), row.source_url, POPULATION_URL))
    write_rows("estimated_people_covered_by_cct.csv",
               ["country_code", "year", "population", "coverage_percent",
                "estimated_people_covered", "coverage_source_url", "population_source_url"],
               beneficiary_rows)

    for rows, stem, title, note, xlim in (
        (poverty_rows, "estimated_people_below_poverty_line",
         "Estimated people below the poverty line",
         "SEDLAC $6.85/day (2017 PPP) headcount × World Bank population; approximate counts.",
         (1997, 2026)),
        (beneficiary_rows, "estimated_people_covered_by_cct",
         "Estimated people covered by CCTs",
         "World Bank ASPIRE coverage × World Bank population; includes direct and indirect beneficiaries.",
         (2005, 2019)),
    ):
        fig, ax = plt.subplots(figsize=(10, 4.8), layout="constrained")
        for code, name in (("BRA", "Brazil"), ("MEX", "Mexico")):
            points = [(row[1], row[4] / 1_000_000) for row in rows if row[0] == code]
            ax.plot(*zip(*points), marker="o", markersize=3.5, linewidth=1.3,
                    linestyle="--", label=name, color=COLORS[name])
        style_plot(ax, title, "Millions of people", xlim)
        ax.set_xlabel("Survey year")
        ax.legend(frameon=False)
        fig.text(0.01, -0.035, note, fontsize=8)
        save_figure(fig, stem)


def poverty_vs_cct_coverage_percent() -> None:
    """Compare rates with the same population denominator, without implying overlap."""
    poverty = pd.read_csv(DATA / "sedlac_rural_urban_poverty_gap.csv")
    poverty = poverty.rename(columns={
        "national_headcount_percent": "poverty_percent",
        "source_url": "poverty_source_url",
    })[["country", "year", "poverty_percent", "poverty_source_url"]]
    poverty["country_code"] = poverty["country"].map({"Brazil": "BRA", "Mexico": "MEX"})
    coverage = pd.read_csv(DATA / "aspire_cct_population_coverage.csv")
    coverage = coverage.rename(columns={
        "percent": "cct_coverage_percent",
        "source_url": "coverage_source_url",
    })[["country_code", "year", "cct_coverage_percent", "coverage_source_url"]]
    combined = poverty.merge(coverage, on=["country_code", "year"], how="outer")
    combined = combined.loc[combined["year"].between(2006, 2018)].copy()
    combined["country"] = combined["country_code"].map({"BRA": "Brazil", "MEX": "Mexico"})
    combined = combined.sort_values(["country_code", "year"])
    combined[["country", "country_code", "year", "poverty_percent", "cct_coverage_percent",
              "poverty_source_url", "coverage_source_url"]].to_csv(
                  DATA / "poverty_vs_cct_coverage_percent.csv", index=False)

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.8), sharey=True, layout="constrained")
    for ax, country in zip(axes, ("Brazil", "Mexico")):
        rows = combined.loc[combined["country"] == country]
        poor = rows.dropna(subset=["poverty_percent"])
        covered = rows.dropna(subset=["cct_coverage_percent"])
        ax.plot(poor["year"], poor["poverty_percent"], marker="o", markersize=3.5,
                linewidth=1.4, color="#d77237", label="Below poverty line")
        ax.scatter(covered["year"], covered["cct_coverage_percent"], marker="s", s=36,
                   color="#147d86", label="CCT coverage", zorder=3)
        style_plot(ax, country, "% of total population", (2005.5, 2018.5))
        ax.set_xlabel("Survey year")
        ax.set_ylim(bottom=0)
        ax.set_xticks([2006, 2009, 2012, 2015, 2018])
        ax.legend(frameon=False, loc="upper right", fontsize=8)
    fig.suptitle("Poverty rate and CCT coverage", fontsize=15, weight="bold")
    fig.text(0.01, -0.055,
             "Poverty: below $6.85/day (2017 PPP), SEDLAC. CCT: people in recipient households, ASPIRE."
             " Groups may overlap; coverage is not an impact estimate.", fontsize=8)
    save_figure(fig, "poverty_vs_cct_coverage_percent")


if __name__ == "__main__":
    bottom20()
    sedlac_income_ratio()
    sedlac_poverty_gap()
    aspire_coverage_targeting()
    population_figures()
    poverty_vs_cct_coverage_percent()
