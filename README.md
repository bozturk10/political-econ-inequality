# Brazil–Mexico inequality figures

Run `python3 program_comparison_infographics.py` to create two English-language
program infographics in `figures/`: a Bolsa Família–Prospera comparison
with a 2018 program snapshot, 2004–2014 country-level inequality changes and
published program outcomes; plus a separate 1997–2026 program timeline.
The script fetches 2018 population denominators from the World Bank API and
reads WDI/SEDLAC metric extracts from `data/`. Values, methods and source links
are recorded in `data/cct_infographic_sources.md`. It writes SVG files and, when
`rsvg-convert` is installed, PNG copies.

Run `python3 gini_figure.py` to fetch the World Bank Gini series and create:

- `data/gini_brazil_mexico_1997_2026.csv`: observed country/year values and API URL.
- `figures/gini_brazil_mexico_1997_2026.svg`: editable vector figure.
- `figures/gini_brazil_mexico_1997_2026.png`: generated when `rsvg-convert` is available.

The script uses only Python's standard library. It requests the World Bank indicator
[`SI.POV.GINI`](https://data.worldbank.org/indicator/SI.POV.GINI) for Brazil and Mexico.
The API endpoint and program date sources are listed at the top of the script.
Missing survey years are not filled. The figure is descriptive; it cannot identify
the causal effect of a cash transfer program on inequality.

For the complementary figures, install the small plotting/Excel dependencies and run:

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python additional_figures.py
.venv/bin/python bottom20_annotated.py
```

Run `bottom20_annotated.py` after `additional_figures.py` to rebuild the
annotated bottom-20 figure from the saved WDI CSV. It needs `rsvg-convert` for
the PNG export. Annotation sources and interpretation are documented in
`comparison_window_decision.md`.

This generates PNG, SVG and cleaned CSV files for:

1. Bottom 20% income share (World Bank WDI `SI.DST.FRST.20`).
2. Urban-to-rural mean per capita income ratio (SEDLAC; within-country ratio).
3. Rural minus urban poverty rate at $6.85/day, 2017 PPP (SEDLAC).
4. Coverage and beneficiary incidence for the poorest quintile in the conditional
   cash transfer category (World Bank ASPIRE; pre-transfer welfare ranking).
5. Conditional cash transfer category coverage of the total population (World Bank
   ASPIRE; direct and indirect beneficiaries).
6. Approximate people below the SEDLAC $6.85/day (2017 PPP) poverty line.
7. Approximate people covered by the ASPIRE conditional cash transfer category.
8. Poverty rate and CCT coverage as percentages of total population, in separate
   Brazil and Mexico panels. The groups may overlap, so the gap between the rates
   is not the share of poor people without benefits.

The last two multiply the survey percentage by same-year World Bank population
(`SP.POP.TOTL`). These are rounded estimates, not administrative headcounts.

All figures are in English. Downloaded source workbooks are cached under `work/raw/`
and ignored by Git. Source URLs are in `additional_figures.py` and the cleaned CSVs.
SEDLAC uses different survey methods over time, including a Brazil break around
2012 and a Mexico break in 2016. ASPIRE is a survey-based *program category*,
not a Bolsa Família or Prospera impact estimate; its 2006–2018 observations are sparse.
