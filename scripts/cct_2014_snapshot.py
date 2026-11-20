#!/usr/bin/env python3
"""Rebuild the 2014 CCT snapshot (within the 1997–2014 study window).

Run: python3 scripts/cct_2014_snapshot.py
Inputs are frozen in data/cct_2014_snapshot.csv and documented in
data/cct_2014_snapshot_sources.md. No network request is required.
"""

from __future__ import annotations

import csv
import shutil
import subprocess
from pathlib import Path

from program_comparison_infographics import bar, line, rect, svg_start, txt


ROOT = Path(__file__).resolve().parents[1]
FIGURES = ROOT / "figures"
INPUT = ROOT / "data" / "cct_2014_snapshot.csv"
STEM = FIGURES / "cct_program_comparison_2014_snapshot"


def load() -> dict[str, dict[str, float]]:
    with INPUT.open(newline="", encoding="utf-8") as stream:
        rows = {row["country"]: row for row in csv.DictReader(stream)}
    if set(rows) != {"BRA", "MEX"}:
        raise ValueError("Expected exactly BRA and MEX")
    data = {}
    for code, row in rows.items():
        values = {key: float(value) for key, value in row.items()
                  if key != "country" and value}
        if any(values[key] <= 0 for key in ("households", "covered_people", "population")):
            raise ValueError(f"Invalid count for {code}")
        values["coverage_pct"] = 100 * values["covered_people"] / values["population"]
        if code == "BRA":
            values["rural_household_pct"] = 100 * values["rural_households"] / values["rural_denominator"]
        if not 0 <= values["female_holder_pct"] <= 100 or not 0 <= values["rural_household_pct"] <= 100:
            raise ValueError(f"Invalid percentage for {code}")
        data[code] = values
    return data


def render(data: dict[str, dict[str, float]]) -> Path:
    FIGURES.mkdir(exist_ok=True)
    colors = {"BRA": "#147d86", "MEX": "#d77237"}
    parts = svg_start(1600, 900)
    parts += [txt(70, 63, "Brazil and Mexico: conditional cash transfers", 36, weight="bold"),
              txt(70, 101, "1997–2014 study window  |  Program rules and 2014 reach", 21, "#5b6570"),
              line(70, 123, 1530, 123),
              txt(70, 164, "PROGRAM DETAILS", 23, weight="bold")]
    for code, x, name, program, launch, details in [
        ("BRA", 70, "BRAZIL", "Bolsa Família", "From 2003", [
            ("EDUCATION", ["School attendance: 85% (ages 6–15);", "75% (ages 16–17)."]),
            ("HEALTH", ["Child vaccination and growth/nutrition checks;", "prenatal and postpartum care."]),
            ("PAYMENT", ["Preferentially to the woman holder", "through a Caixa payment card or account."]),
        ]),
        ("MEX", 830, "MEXICO", "Oportunidades / Prospera", "Progresa from 1997; renamed 2014", [
            ("EDUCATION", ["School enrollment and regular attendance."]),
            ("HEALTH", ["Scheduled clinic visits and health workshops;", "older-adult benefit: a visit every six months.*"]),
            ("PAYMENT", ["Generally to the mother as named holder", "through payment points or an account."]),
        ]),
    ]:
        color = colors[code]
        parts += [rect(x, 188, 700, 357, "#f7f9fa", 14), rect(x, 188, 8, 357, color),
                  txt(x + 30, 229, name, 22, color, "bold"),
                  txt(x + 30, 263, program, 28, weight="bold"),
                  txt(x + 30, 288, launch, 17, "#5b6570")]
        for y, (heading, lines) in zip((329, 404, 482), details):
            parts.append(txt(x + 30, y, heading, 16, color, "bold"))
            for i, value in enumerate(lines):
                parts.append(txt(x + 30, y + 27 + 24 * i, value, 19))

    parts += [txt(70, 571, "2014 REACH", 23, weight="bold"),
              txt(275, 571, "A snapshot within the study window", 18, "#5b6570"),
              line(70, 588, 1530, 588)]
    for code, x, name, program, timing in [
        ("BRA", 70, "BRAZIL", "Bolsa Família", "December 2014"),
        ("MEX", 830, "MEXICO", "Oportunidades / Prospera", "September 2014"),
    ]:
        item = data[code]
        color = colors[code]
        parts += [rect(x, 605, 700, 220, "#f7f9fa", 14), rect(x, 605, 8, 220, color),
                  txt(x + 30, 639, name, 20, color, "bold"),
                  txt(x + 665, 639, timing, 16, "#5b6570", anchor="end"),
                  txt(x + 30, 687, f'{item["households"] / 1e6:.2f}m', 34, color, "bold"),
                  txt(x + 30, 711, "households", 17, "#5b6570"),
                  txt(x + 348, 687, f'~{item["covered_people"] / 1e6:.1f}m', 34, color, "bold"),
                  txt(x + 348, 711, "people in covered households", 17, "#5b6570"),
                  txt(x + 30, 751, f'~{item["coverage_pct"]:.1f}% of national population', 20, weight="bold")]
        bar(parts, x + 30, 762, item["coverage_pct"], color, 640)
        parts += [txt(x + 30, 807, f'Women holders  {item["female_holder_pct"]:.0f}%', 18, color, "bold"),
                  txt(x + 364, 807, f'Rural households  {item["rural_household_pct"]:.1f}%', 18, color, "bold")]

    parts += [txt(70, 852, "* Older-adult visit applies to that specific benefit; its certification also served as proof of life.", 15, "#5b6570"),
              txt(70, 876, "Dates and denominators differ; Mexico's ~27m people is from an early-2015 report. Sources: data/cct_2014_snapshot_sources.md", 15, "#5b6570"),
              "</svg>"]
    svg = STEM.with_suffix(".svg")
    svg.write_text("\n".join(parts) + "\n", encoding="utf-8")
    converter = shutil.which("rsvg-convert")
    if converter:
        with STEM.with_suffix(".png").open("wb") as output:
            subprocess.run([converter, "-w", "3200", str(svg)], stdout=output, check=True)
    return svg


if __name__ == "__main__":
    print(render(load()))
