# Figures for the Brazil–Mexico presentation

All figures are 16:9, with 1920 × 1080 SVG originals and 3840 × 2160 PNG exports. Brazil is teal and Mexico is orange. The supplied PPTX was not edited.

## Presentation-ready figures

1. `01_same_gini_different_bottom20` — outcome/puzzle, 2008–2014. WDI Gini fell 1.9 points in each country; the income share of the bottom 20% rose 0.4 percentage points in Brazil and 0.8 in Mexico. Data points are observed surveys only. Mexico has no 2009, 2011 or 2013 point; Brazil has no 2010 point. The lines join observations but do not estimate missing years. Sources: [Gini](https://data.worldbank.org/indicator/SI.POV.GINI) and [bottom 20% income share](https://data.worldbank.org/indicator/SI.DST.FRST.20). Prepared CSV: `../data/outcomes_wdi_2008_2014.csv`.
2. `02_real_minimum_wage` — labor-market mechanism, 2003–2014. Real national minimum wage index, 2000 = 100, from [ILO Labour Overview 2013](https://www.ilo.org/sites/default/files/wcmsp5/groups/public/%40americas/%40ro-lima/documents/publication/wcms_242634.pdf) and [ILO Labour Overview 2015, Table 10](https://www.ilo.org/sites/default/files/wcmsp5/groups/public/%40americas/%40ro-lima/documents/publication/wcms_450098.pdf). The 2008–2014 within-country increase was 26.6% in Brazil and 1.2% in Mexico. Index levels do not compare wages' purchasing power between countries. Prepared CSV: `../data/ilo_real_minimum_wage_2003_2014.csv`.
3. `03_uhc_service_coverage` — health service coverage context, 2000/2005/2010/2015. Values are from [WHO/World Bank, Tracking Universal Health Coverage 2021, Annex 3](https://cdn.who.int/media/docs/default-source/world-health-data-platform/events/tracking-universal-health-coverage-2021-global-monitoring-report_uhc-day.pdf?download=true). Use it as a service coverage index, not as a measure of the legal architecture of health insurance, segmentation, or financial protection. The historical index has since been revised; do not mix it with a newer vintage. Prepared CSV: `../data/welfare_uhc_service_coverage_2000_2015.csv`.

## Provisional figure

4. `04_out_of_pocket_health_provisional` — national out-of-pocket spending share. The indicator is [WHO GHED / World Bank WDI, SH.XPD.OOPC.CH.ZS](https://data.worldbank.org/indicator/SH.XPD.OOPC.CH.ZS). Historical values were retrieved from a third-party WDI mirror because the official API did not respond in this environment. **Confirm every plotted value against a current official WHO or World Bank export before using this slide.** National spending share does not show the burden on poor households. Prepared CSV: `../data/welfare_oop_health_2000_2014.csv`.

## Data still needed

- ECLAC publishes spending by non-contributory program, but a comparable annual total for pensions plus transfers was not confirmed. Avoid a national-total chart until the included programs and double-counting rules are set.
- V-Dem's relevant series are `v2xpas_economic_government` for the governing coalition and `v2x_cspart` for civil society participation. The latter is not `v2csprtcpr`, which appears in the source document. Numeric extracts were unavailable here. The coalition series is election-year rather than annual.
- SEDLAC provides wage statistics by education, but the workbook could not be retrieved here; a Brazil–Mexico skill-premium series was not verified.
- Local union-density values conflict with an ILO publication for Brazil in 2014, so no union-density plot was produced.

## PPTX consistency note

The new title is supported **for 2008–2014** by the WDI endpoints. Current PPTX slides 5 and 7 still use the older claim that Brazil reduced inequality much more than Mexico, and slide 4 compares different program windows with SWIID data. Those claims should be revised or clearly separated from the 2008–2014 WDI puzzle. The charts are descriptive and do not estimate effects of CCTs or other policies.
