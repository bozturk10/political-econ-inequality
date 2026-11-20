# Brazil–Mexico inequality research figures

Python scripts, source extracts, and slide-ready figures for a comparison of
inequality and conditional cash transfers in Brazil and Mexico. The main study
window is **1997–2014**; individual charts state their own years and measures.

## Quick start

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python scripts/cct_2014_snapshot.py
```

## Where to look

| Path | Purpose |
| --- | --- |
| `scripts/` | Main figure builders; `gini_figure.py`, `additional_figures.py`, and `program_comparison_infographics.py` fetch current source data. |
| `docs/` | Research notes, window decisions, and slide references. |
| `data/` | Cleaned CSVs, frozen snapshot inputs, and source notes. |
| `figures/` | Slide-ready PNGs, editable SVGs, and dated figure sets. Dated sets include their own `build.py` and `FIGURE_GUIDE.md` where applicable. |
| `output/` | Presentation and figure exports. |

For the broader figure set, run `scripts/additional_figures.py` before
`scripts/bottom20_annotated.py`. The 2018 CCT infographic and program timeline come
from `scripts/program_comparison_infographics.py`. Some builders download data and need
internet; downloaded workbooks are cached in ignored `work/raw/`.

## Main data sources

- [World Bank Indicators API](https://datahelpdesk.worldbank.org/knowledgebase/articles/889392): Gini (`SI.POV.GINI`), bottom-20 income share (`SI.DST.FRST.20`), and population (`SP.POP.TOTL`). The country queries are in the Python scripts.
- [SEDLAC (CEDLAS and World Bank)](https://www.cedlas.econo.unlp.edu.ar/wp/en/statistics/sedlac/statistics-3/): rural–urban poverty, income, and wage workbooks.
- [World Bank ASPIRE](https://www.worldbank.org/en/data/datatopics/aspire/indicator/performance): survey-based social-protection coverage and targeting. These are program-category estimates, not Bolsa Família or Prospera impact estimates.
- [ILOSTAT](https://ilostat.ilo.org/data/): monthly minimum-wage series. The two original CSV exports are in `data/ilostat_exports/`; rebuild with `python3 figures/2026-11-19_ilostat_minimum_wage/build.py`.
- [SWIID 8.0](https://doi.org/10.7910/DVN/LM4OWF): market- and disposable-income Gini series used in `figures/2026-11-19_swiid_sequence/`.

Source URLs, date choices, and caveats for individual figures are in nearby
`FIGURE_GUIDE.md` files and `data/*sources.md`. SEDLAC surveys and definitions
can change across years; inspect each figure's guide before interpreting a trend.

## Data and reuse

The committed CSVs contain analysis inputs or selected series; figure scripts
and source notes document their provenance. The original SEDLAC wages and hours
workbook is deliberately not redistributed. To rebuild the education wage
figures, download the [November 2026 workbook](https://www.cedlas.econo.unlp.edu.ar/wp/wp-content/uploads/2026_Act1_wages_hours_LAC.xlsx)
to `work/raw/2026_Act1_wages_hours_LAC.xlsx`, then run the two scripts in
`figures/2026-11-19_skill_premium/`. The `work/` directory is ignored by Git.

Data and figures retain their source-specific rights. Cite SEDLAC data as
“Source: SEDLAC (CEDLAS and The World Bank)” with the access date, and see the
individual figure guides for other sources. A license for this repository's
code would not relicense third-party data.
